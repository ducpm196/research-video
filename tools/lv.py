"""lv — Lecture Video toolkit: biến một file đặc tả bài giảng (YAML) thành video giảng giải có giọng đọc + phụ đề.

Lệnh (chạy bằng python của .venv, từ thư mục gốc dự án):
  python tools/lv.py new        lessons/<id>.yaml --id L02 --title "..."   # tạo bài mới từ template
  python tools/lv.py lint       lessons/<id>.yaml   # cấu trúc, KaTeX, ký hiệu-trước-khi-dùng, phép tính, nhịp đọc
  python tools/lv.py preview    lessons/<id>.yaml   # storyboard HTML để duyệt trước (không cần mạng)
  python tools/lv.py tts        lessons/<id>.yaml   # sinh giọng đọc (edge-tts, có cache)
  python tools/lv.py render     lessons/<id>.yaml   # chụp khung hình 1920x1080 + kiểm tra tràn/lỗi công thức
  python tools/lv.py build      lessons/<id>.yaml   # lint -> tts -> render -> ghép mp4 + srt + chapters
  python tools/lv.py verify     lessons/<id>.yaml   # kiểm tra file mp4 cuối (luồng, thời lượng, khớp timeline)
  python tools/lv.py asr        lessons/<id>.yaml   # máy nghe lại giọng đọc (faster-whisper), gắn cờ câu đọc sai
  python tools/lv.py curriculum curriculum/<x>.yaml # kiểm tra đồ thị tiên quyết của cả khoá

Mã thoát: 0 = PASS, 1 = FAIL (có lỗi chặn), 2 = lỗi môi trường / thiếu công cụ.
"""
import argparse
import asyncio
import datetime
import hashlib
import json
import os
import math
import random
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import wave
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lv_profile import (DEFAULT_PROFILE, available as profiles_available, kind_labels, lint_profile_rules,  # noqa: E402
                        load_profile, profile_name, profile_of, voice_lang)

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
KATEX_DIR = TOOLS / "vendor" / "node_modules" / "katex" / "dist"
OUT = ROOT / "out"
CACHE = OUT / "_cache" / "tts"
FPS = 30
SR = 24000
KINDS = {"hook", "prereq", "intuition", "symbol", "concept", "formula", "example", "check",
         "pitfall", "quiz", "recap", "mindset"}
REQUIRED_KINDS = {"hook", "symbol", "example", "pitfall", "quiz", "recap"}
MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)
# Khoá step mà lint/render/player thật sự đọc (E34): khoá khác bị bỏ qua lặng lẽ nên phải báo
STEP_KEYS = {"show", "say", "focus", "forward_ref", "introduces", "notation_note", "pause", "clear", "keep",
             "layout", "voice", "hold"}
# Tên lệnh (≥ 3 chữ) mà biến số không bao giờ trùng — đứng trần trong công thức là đã mất dấu “\” (E33)
BARE_CMD_RE = re.compile(r"(?<![\\A-Za-z])(?:equiv|neg|land|lor|lnot|leftrightarrow|rightarrow|implies|iff|frac|dfrac|sqrt|"
                         r"cdot|cdots|ldots|times|approx|neq|leq|geq|infty|forall|exists|subseteq|emptyset|setminus|binom|"
                         r"bmod|pmod|nabla|partial|lambda|theta|sigma|alpha|epsilon|mathbb|mathcal|mathbf|hl|hlb|hlg|hlo)(?![A-Za-z])")


def katex_safe(show):
    r"""Chữ tiếng Việt mang HAI dấu (ố, ầ, ễ, ắ…) trong công thức: KaTeX tách thành chữ gốc + dấu tự dựng → dấu lệch
    (lỗi thật: “độ dốc” trong \text{} ở L05 khung 16, dấu sắc lệch khỏi chữ ô). Thay bằng {\char"XXXX}: KaTeX in nguyên
    glyph có sẵn của phông, không tách dấu. Chỉ đổi bên trong $…$ / $$…$$; ngoặc {} để chữ cái theo sau không bị đọc thành số hex."""
    def one(c):
        ch = c.group()
        return '{\\char"%X}' % ord(ch) if len(unicodedata.normalize("NFD", ch)) >= 3 else ch

    def fix(m):
        return re.sub(r"[^\x00-\x7f]", one, m.group(0))
    return MATH_RE.sub(fix, show)


SENT_RE = re.compile(r"(?<=[.!?…])\s+(?=[^\s])")
MAX_WORDS_SENTENCE = 38
# E38: biến thể chính tả → dạng chuẩn của kho (dạng đa số khi rà 2026-10-30). “mili giây” trên màn hình là chữ viết đúng, không xét.
SPELL_CANON = {"luỹ": "lũy", "tùy": "tuỳ", "hủy": "huỷ", "khỏe": "khoẻ", "logarit": "lôgarit", "tỷ": "tỉ", "vectơ": "vector"}
MAX_CAPTION_CHARS = 170
REASON_RE = r"\b(vì|nên|do|bởi|theo|thay|chuyển vế|nghĩa là|tức là|suy ra|nhớ lại|quy tắc|giống như)\b"
OPAQUE_SOURCE_RE = (r"(?i)tài liệu|\bslides?\b|\bdòng \d+|môn học|bài giảng (?:của|môn)|bài báo gốc|bản gốc|giáo trình"
                    r"|\b(?:ML|PR|AG)\d{2}\b")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class _StrictLoader(yaml.SafeLoader):
    """safe_load mà khoá trùng là LỖI — PyYAML mặc định lặng lẽ lấy giá trị sau (lỗi thật: 30 bài CS112 có hai `asr_reviewed`)."""


def _no_dup_mapping(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    dup = sorted({str(k) for k in keys if keys.count(k) > 1})
    if dup:
        raise yaml.constructor.ConstructorError(None, None, f"khoá trùng {dup}", node.start_mark)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dup_mapping)


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.load(f, Loader=_StrictLoader)


def load_spec(path):
    spec = load_yaml(path)
    spec["_path"] = str(path)
    return spec


def sentences(text):
    text = " ".join(str(text).split())
    return [s for s in SENT_RE.split(text) if s.strip()]


# Khoá học: bài không ghi `course` là CS115 (khoá đầu tiên) → luật đọc, sổ ký hiệu giữ nguyên như cũ.
# Mỗi khoá có thư mục ra riêng out/<course>/<id> (CS112 và CS115 cùng số hiệu L00… mà không đè nhau), lộ trình riêng
# (“bài N” tra theo curriculum cùng `course`), và phần PHỦ THÊM của lexicon/sổ ký hiệu trong
# tools/registry/lexicon_vi.<course>.yaml, symbols.<course>.yaml — thêm luật đọc cho khoá mới không đổi văn bản gửi TTS
# của khoá cũ (đổi lexicon chung làm video đã dựng thành STALE: lỗi thật L05).
DEFAULT_COURSE = "CS115"


def course_of(spec):
    return str(spec.get("course") or DEFAULT_COURSE)


_LEX = {}


def lexicon(course=DEFAULT_COURSE):
    """Luật phát âm đã biên dịch. Mỗi luật được bọc ranh giới từ Unicode nên chỉ khớp NGUYÊN TỪ.
    Luật riêng của khoá (lexicon_vi.<course>.yaml) chạy TRƯỚC luật chung; must_not_change, foreign_ok là hợp của hai."""
    if course not in _LEX:
        raws = [load_yaml(TOOLS / "registry" / "lexicon_vi.yaml")]
        extra = TOOLS / "registry" / f"lexicon_vi.{course}.yaml"
        if course != DEFAULT_COURSE and extra.exists():
            raws.insert(0, load_yaml(extra) or {})
        rules = [(r["pat"], re.compile(r"(?<!\w)(?:" + r["pat"] + r")(?!\w)", re.I if r.get("ci") else 0), r["say"])
                 for raw in raws for r in raw.get("rules") or []]
        _LEX[course] = {"rules": rules, "must_not_change": [w for raw in raws for w in raw.get("must_not_change") or []],
                        "foreign_ok": {w.lower() for raw in raws for w in raw.get("foreign_ok") or []}}
    return _LEX[course]


def registry(course=DEFAULT_COURSE):
    """Sổ ký hiệu: symbols.yaml chung + symbols.<course>.yaml của khoá (nối thêm ký hiệu, lệnh trình bày, luật nhất quán)."""
    reg = load_yaml(TOOLS / "registry" / "symbols.yaml")
    extra = TOOLS / "registry" / f"symbols.{course}.yaml"
    if course != DEFAULT_COURSE and extra.exists():
        ex = load_yaml(extra) or {}
        # `replaces: <id>`: ký hiệu của khoá mang nghĩa khác sổ chung (TOC: \Sigma là bảng chữ cái, không phải ma trận hiệp
        #   phương sai) → bỏ mục chung đó, để lint không đòi giới thiệu một nghĩa không có trong khoá.
        drop = {s["replaces"] for s in ex.get("symbols") or [] if s.get("replaces")}
        reg["symbols"] = [s for s in reg["symbols"] if s["id"] not in drop] + (ex.get("symbols") or [])
        reg["layout_commands"] = list(reg.get("layout_commands") or []) + (ex.get("layout_commands") or [])
        reg["consistency"] = list(reg.get("consistency") or []) + (ex.get("consistency") or [])
    return reg


def lexicon_apply(text, hits=None, course=DEFAULT_COURSE):
    for pat, rx, rep in lexicon(course)["rules"]:
        if hits is not None:
            hits.extend((pat, m.group(0), rep) for m in rx.finditer(text))
        text = rx.sub(rep, text)
    return text


_TONES = {"̀", "́", "̃", "̉", "̣"}
VI_SYLLABLE = re.compile(r"^(ngh|ng|gh|gi|kh|nh|ph|qu|th|tr|ch|[bcdđghklmnprstvx])?"
                         r"(uyê|ươ|iê|yê|uô|oa|oă|oe|uâ|uy|uê|[aăâeêioôơuưy]{1,3})"
                         r"(ch|ng|nh|[cmnpt])?$")


def is_vietnamese_syllable(word):
    import unicodedata
    base = "".join(ch for ch in unicodedata.normalize("NFD", word.lower()) if ch not in _TONES)
    return bool(VI_SYLLABLE.match(unicodedata.normalize("NFC", base)))


def out_dir(spec):
    # Mỗi khoá một thư mục: out/CS115/L00, out/CS112/L00 (người dùng tổ chức lại 2026-10-27: lessons/cs115/, out/CS115/)
    d = OUT / course_of(spec) / spec["id"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        exe = shutil.which("ffmpeg")
        if not exe:
            print("ENV ERROR: không tìm thấy ffmpeg (cài imageio-ffmpeg trong .venv)")
            sys.exit(2)
        return exe


# ───────────────────────────── LINT ─────────────────────────────
class Report:
    def __init__(self):
        self.errors, self.warnings, self.passes = [], [], []

    def err(self, where, msg):
        self.errors.append(f"[FAIL] {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"[WARN] {where}: {msg}")

    def ok(self, msg):
        self.passes.append(f"[PASS] {msg}")

    def dump(self):
        for line in self.passes + self.warnings + self.errors:
            print(line)
        print(f"lint: {len(self.errors)} FAIL, {len(self.warnings)} WARN, {len(self.passes)} PASS")
        print("checked_at=" + now())
        return 1 if self.errors else 0


def iter_steps(spec):
    for si, sc in enumerate(spec.get("scenes", [])):
        for ki, st in enumerate(sc.get("steps", [])):
            yield si, sc, ki, st


def lesson_numbers(spec):
    """(số thứ tự của bài này, {số thứ tự: tên bài} của lộ trình CÙNG khoá). Bài thử nghiệm có thể đặt `ref_lesson_no`.
    Chỉ đọc lộ trình có `course` trùng khoá của bài: CS112 và CS115 cùng có L00…L24 nhưng là hai bài khác nhau."""
    m = re.fullmatch(r"L(\d+)", str(spec.get("id", "")))
    cur = spec.get("ref_lesson_no", int(m.group(1)) if m else None)
    known = {}
    for cp in sorted((ROOT / "curriculum").glob("*.yaml")):
        cur_yaml = load_yaml(cp) or {}
        if str(cur_yaml.get("course") or "") != course_of(spec):
            continue
        for l in cur_yaml.get("lessons", []):
            mm = re.fullmatch(r"L(\d+)", str(l.get("id", "")))
            if mm:
                known[int(mm.group(1))] = str(l.get("title", ""))
    return cur, known


def _bigrams(text):
    w = re.findall(r"\w+", text.lower())
    return {(a, b) for a, b in zip(w, w[1:]) if len(a) > 1 or len(b) > 1}


def lint(spec, quiet=False):
    r = Report()
    for key in ("id", "title", "series", "objectives", "scenes", "assumes"):
        if key not in spec:
            r.err("spec", f"thiếu trường bắt buộc `{key}`")
    if r.errors:
        return r
    # 1. cấu trúc sư phạm
    kinds = [sc.get("kind") for sc in spec["scenes"]]
    prof = profile_of(spec)                     # hồ sơ chuyên ngành (tools/profiles/*.yaml); mặc định stem = hành vi cũ
    p_kinds, p_req = set(prof["kinds"]), set(prof["required"])
    for si, sc in enumerate(spec["scenes"]):
        if sc.get("kind") not in p_kinds:
            r.err(f"scene#{si}", f"kind `{sc.get('kind')}` không hợp lệ với hồ sơ `{prof['name']}` ({sorted(p_kinds)})")
        if not sc.get("steps"):
            r.err(f"scene#{si}", "không có step nào")
        # E25: tiêu đề scene là chữ thường (không qua KaTeX) → “w_k”, “G_k” hiện nguyên dấu gạch (lỗi thật L09, L10)
        if re.search(r"[_^\\$]", str(sc.get("title", ""))):
            r.err(f"{sc.get('id', si)}.title", f"E25 tiêu đề scene có ký tự LaTeX (_ ^ \\ $) sẽ hiện nguyên: “{sc.get('title')}” "
                                               "— viết bằng lời hoặc ký tự Unicode (ŷ, ᵀ, ₖ)")
        # E34: khoá step lạ bị bỏ qua lặng lẽ (lỗi thật DMS L02 2026-10-27: dòng thừa `set: "\\{"` lọt qua lint)
        for ki, st in enumerate(sc.get("steps") or []):
            for k in sorted(set(st) - STEP_KEYS):
                r.err(f"{sc.get('id', si)}.{ki}", f"E34 khoá step `{k}` không có tác dụng (hợp lệ: {sorted(STEP_KEYS)}) — gõ nhầm hoặc thừa")
        # E27: mã nội bộ của bản rà soát (AUDIT A13, slide AG24) vô nghĩa với người học (lỗi thật L20–L29) — chỉ để ở source:/chú thích
        for ki, st in enumerate(sc.get("steps") or []):
            for fld, txt in (("title", sc.get("title")) if ki == 0 else (None, None), ("show", st.get("show")), ("say", st.get("say"))):
                m = fld and re.search(r"\b(?:(?:AUDIT|[Ss]lide) [A-Z]{1,2}\d+|[Ss]lide [A-Z]{2,}\b)|\((?:PR|AG|VC|T|A)\d+[a-z]?\)", str(txt or ""))
                if m:
                    r.err(f"{sc.get('id', si)}.{ki if fld != 'title' else 'title'}",
                          f"E27 mã nội bộ “{m.group(0)}” hiện cho người học — chỉ ghi ở `source:` hoặc chú thích #")
    # E29: người học CHỈ có video — “tài liệu gốc viết…”, “tài liệu dòng 266”, “slide môn học”, “bài báo gốc” trỏ tới thứ họ
    # không có (lỗi thật L00 phút 6:49, 312 chỗ ở 33 bài, 2026-10-27). Nêu thẳng điều đúng, hoặc gọi tên nguồn (tác giả, năm).
    seen = [("title", spec.get("title")), *(("objectives", o) for o in spec.get("objectives") or [])]
    for si, sc in enumerate(spec["scenes"]):
        seen.append((f"{sc.get('id', si)}.title", sc.get("title")))
        seen += [(f"{sc.get('id', si)}.{ki}", st.get(f)) for ki, st in enumerate(sc.get("steps") or []) for f in ("show", "say")]
    # `domain_terms: [dòng]`: “dòng N” là thuật ngữ của bài (dòng bộ nhớ đệm, CSA L10–L12), không phải trích tài liệu — chỉ bỏ đúng mẫu đó
    opaque = OPAQUE_SOURCE_RE.replace(r"|\bdòng \d+", "") if "dòng" in (spec.get("domain_terms") or []) else OPAQUE_SOURCE_RE
    for where, txt in seen:
        m = re.search(opaque, str(txt or ""))
        if m:
            r.err(where, f"E29 nhắc nguồn người xem không có: “{m.group(0)}” — nêu thẳng điều đúng, hoặc gọi tên nguồn (tác giả, năm)")
    missing = p_req - set(kinds)
    if missing:
        r.err("structure", f"thiếu phân cảnh bắt buộc cho người mới: {sorted(missing)}")
    else:
        r.ok(f"cấu trúc sư phạm đủ {sorted(p_req)} (hồ sơ {prof['name']})")
    if kinds and kinds[0] != "hook":
        r.warn("structure", "nên mở đầu bằng `hook` (vì sao cần học)")
    if kinds and kinds[-1] != "recap":
        r.warn("structure", "nên kết thúc bằng `recap` (chuỗi logic)")
    # 2. narration: không chứa LaTeX thô, độ dài câu
    words_total = 0
    for si, sc, ki, st in iter_steps(spec):
        where = f"{sc.get('id', si)}.{ki}"
        say = st.get("say")
        if not say or not str(say).strip():
            r.err(where, "thiếu `say` (lời giảng)")
            continue
        if "$" in say or "\\" in say:
            r.err(where, "`say` chứa LaTeX thô ($ hoặc \\) — TTS sẽ đọc sai; hãy viết thành lời")
        if re.search(r"[_^{}]", say):
            r.err(where, "`say` chứa ký tự _ ^ { } — viết thành lời (vd 'x một', 'mũ hai')")
        for s in sentences(say):
            n = len(s.split())
            words_total += n
            if n <= 2:
                r.warn(where, f"câu chỉ {n} từ (“{s}”) — TTS hay đọc méo/cắt câu cực ngắn (ASR L01: “Khớp.” nghe thành “cỡp”); ghép vào câu bên cạnh")
            if n > MAX_WORDS_SENTENCE:
                r.warn(where, f"câu {n} từ (> {MAX_WORDS_SENTENCE}) khó nghe với người mới: “{s[:60]}…”")
            if len(s) > MAX_CAPTION_CHARS:
                r.err(where, f"câu dài {len(s)} ký tự > {MAX_CAPTION_CHARS}, phụ đề sẽ tràn: “{s[:60]}…”")
        if "show" not in st and not st.get("keep"):
            r.warn(where, "step không có `show` — bảng giữ nguyên khung trước")
        # 2b. bước biến đổi trong phần công thức/kiểm tra phải nói LÝ DO, không chỉ đọc lại phép tính
        if sc.get("kind") in ("formula", "check") and re.search(r"=|\\implies|\\iff", str(st.get("show", ""))) \
                and not re.search(REASON_RE, say, re.I):
            r.warn(where, "bước biến đổi chưa nói lý do (vì/nên/do/theo/thay/chuyển vế/nghĩa là…) — người mới cần biết TẠI SAO")
    # 2d. trích dẫn bài khác (E22–E23, pedagogy.md luật 17). Người học CHƯA học bài sau: nhắc tới bài sau chỉ khi cần,
    #     giải thích bằng lời thường, và step phải có `forward_ref: true` (người soạn khẳng định đã giải thích). Nhắc bài
    #     trước phải nói lại kiến thức đó là gì — câu quá ngắn (“như bài 2”) bị cảnh báo. Số bài phải có trong lộ trình.
    cur_no, known = lesson_numbers(spec)
    if cur_no is not None:
        n_fw = n_bw = 0
        for si, sc, ki, st in iter_steps(spec):
            where = f"{sc.get('id', si)}.{ki}"
            text = str(st.get("say", "")) + " " + re.sub(r"<[^>]+>", " ", str(st.get("show", "")))
            refs = [int(m.group(1)) for m in re.finditer(r"\b[Bb]ài\s+(\d+)\b", text)]
            fw = [n for n in refs if n > cur_no] + (["sau"] if re.search(r"\b[Bb]ài (sau|tiếp theo)\b", text) else [])
            for n in refs:
                if known and n not in known:
                    r.err(where, f"E22 nhắc “bài {n}” nhưng lộ trình không có bài L{n:02d}")
            if fw:
                n_fw += 1
                if not st.get("forward_ref"):
                    r.err(where, f"E22 nhắc bài SAU ({', '.join(map(str, fw))}) mà step chưa có `forward_ref: true` — người học "
                                 "chưa học bài đó: giải thích bằng lời thường rồi mới đánh dấu, hoặc bỏ")
                if sc.get("kind") not in ("hook", "recap") and not str(sc.get("id", "")).startswith("in_ai"):
                    r.warn(where, "E22 nhắc bài sau giữa phần giảng (không phải hook/in_ai/recap) — dễ gây khó hiểu")
            for s in sentences(str(st.get("say", ""))):
                for m in re.finditer(r"\b[Bb]ài\s+(\d+)\b", s):
                    if int(m.group(1)) < cur_no:
                        n_bw += 1
                        # bỏ cụm “(như/theo/ở/từ/của…) bài N” — phần còn lại phải đủ để nói lại kiến thức đó là gì
                        rest = re.sub(r"\b(như|theo|ở|từ|của|trong|giống)?\s*(ở\s+)?[Bb]ài\s+\d+\b", " ", s)
                        if len(re.findall(r"\w+", rest)) < 6:
                            r.warn(where, f"E23 nhắc bài trước mà gần như không nói lại nội dung (“{s}”) — nói lại kiến thức đó là gì")
        # E24: câu giới thiệu “bài sau” phải đúng bài kế tiếp trong lộ trình (lỗi thật 2026-10-24: chèn bài hệ phương trình
        #      thành bài 3, câu cuối bài 2 vẫn nói “bài sau: Gram-Schmidt”). Số ghi kèm phải là bài hiện tại + 1; nội dung
        #      phải trùng ít nhất một cụm hai từ với tên bài kế tiếp (WARN — người soạn đọc lại).
        nxt = known.get(cur_no + 1)
        # cụm hai từ chung chung (“ma trận”, “vector riêng”…) có trong ≥ 3 tên bài thì không phân biệt được bài nào → bỏ
        df = {}
        for t in known.values():
            for g in _bigrams(t):
                df[g] = df.get(g, 0) + 1
        nxt_grams = {g for g in _bigrams(nxt or "") if df.get(g, 0) < 3}
        for si, sc, ki, st in iter_steps(spec):
            where = f"{sc.get('id', si)}.{ki}"
            text = str(st.get("say", "")) + " " + re.sub(r"<[^>]+>", " ", str(st.get("show", "")))
            for m in re.finditer(r"\b[Bb]ài (?:sau|tiếp theo)\b[^.]{0,25}?\b[Bb]ài (\d+)\b", text):
                if int(m.group(1)) != cur_no + 1:
                    r.err(where, f"E24 “bài sau” ghi là bài {m.group(1)} nhưng bài kế tiếp trong lộ trình là bài {cur_no + 1}")
            claim = re.sub(r"[Hh]ẹn gặp bạn ở bài (?:tiếp theo|sau|\d+)", " ", text)
            # “các bài sau” = nhiều bài về sau, không phải bài kế tiếp → không xét
            if nxt and re.search(r"(?<![Cc]ác )\b[Bb]ài (?:sau|tiếp theo)\b", claim) and not (_bigrams(claim) & nxt_grams):
                r.warn(where, f"E24 câu về “bài sau” không nhắc cụm nào trong tên bài kế tiếp (“{nxt[:60]}”) — kiểm lại "
                              "có đúng bài kế tiếp không")
        # E37: khoảng “bài a–b” phải trỏ tới bài có thật; một cảnh làm bản đồ khoá học (nhắc ≥ 60% số bài khác) phải phủ
        #      ĐỦ mọi bài (lỗi thật 2026-10-29: CS115 L00 ghi “bài 34–43: mở rộng” sau khi đã thêm L44); bài không có bài
        #      kế tiếp thì không được hẹn “bài sau” (audit/review/check_course_refs.py quét cả kho bằng cùng luật).
        dash = r"\s*(?:–|-|—|đến|tới)\s*(?:[Bb]ài\s+)?"
        others = {k for k in known if k > 0 and k != cur_no}
        cov_by_scene = {}
        for si, sc, ki, st in iter_steps(spec):
            where = f"{sc.get('id', si)}.{ki}"
            text = str(st.get("say", "")) + " " + re.sub(r"<[^>]+>", " ", str(st.get("show", "")))
            cov = cov_by_scene.setdefault(sc.get("id", si), set())
            for m in re.finditer(r"\b[Bb]ài\s+(\d+)" + dash + r"(\d+)\b", text):
                a, b = int(m.group(1)), int(m.group(2))
                if known and b not in known:
                    r.err(where, f"E37 khoảng “{m.group(0)}” trỏ tới bài {b} không có trong lộ trình")
                cov.update(range(a, b + 1))
            for m in re.finditer(r"\b[Bb]ài\s+\d+(?:" + dash + r"\d+)?((?:\s*(?:,|và|hoặc)\s*(?:[Bb]ài\s+)?\d+(?:" + dash + r"\d+)?)+)", text):
                for p in re.finditer(r"(\d+)(?:" + dash + r"(\d+))?", m.group(1)):
                    cov.update(range(int(p.group(1)), int(p.group(2) or p.group(1)) + 1))
            cov.update(int(m.group(1)) for m in re.finditer(r"\b[Bb]ài\s+(\d+)\b", text))
            if known and (cur_no + 1) not in known and \
                    re.search(r"(?<![Cc]ác )\b[Bb]ài (?:sau|tiếp theo)\b", str(st.get("say", ""))):
                r.err(where, f"E37 bài {cur_no} là bài cuối của lộ trình mà vẫn nhắc “bài sau/bài tiếp theo”")
        for scid, cov in cov_by_scene.items():
            if len(others) >= 5 and len(cov & others) >= 0.6 * len(others) and others - cov:
                r.err(scid, f"E37 bản đồ khoá học nhắc {len(cov & others)}/{len(others)} bài nhưng bỏ sót bài "
                            f"{', '.join(map(str, sorted(others - cov)))}")
        r.ok(f"trích dẫn bài khác: {n_fw} step nhắc bài sau, {n_bw} câu nhắc bài trước")
    # 2c. phát âm: luật lexicon không được làm hỏng từ tiếng Việt; từ ngoại phải có cách đọc
    crs = course_of(spec)
    lex = lexicon(crs)
    for w in lex["must_not_change"]:
        if lexicon_apply(w, course=crs) != w:
            r.err("lexicon", f"luật phát âm làm hỏng từ tiếng Việt “{w}” → “{lexicon_apply(w, course=crs)}”")
    hits, foreign = [], {}
    base_lang = voice_lang(spec.get("voice"))
    for si, sc, ki, st in iter_steps(spec):
        if not st.get("say") or voice_lang(st.get("voice") or spec.get("voice")) != base_lang:
            continue   # câu mẫu đọc bằng giọng bản ngữ (hồ sơ language): không áp lexicon tiếng Việt
        # E28: phiên âm tên riêng (Bay-ét, La-gơ-răng) gõ thẳng vào say → phụ đề hiện phiên âm thay tên thật (lỗi thật
        # L24, L30). Viết tên gốc; lexicon tự đổi khi gửi TTS. Tên chữ cái Hy Lạp (lam-đa) là lời nói thật, không chặn.
        for pat, rx, rep in lex["rules"]:
            if (("-" in rep and pat[:1].isupper()) or (pat.isalpha() and pat.isupper() and " " in rep)) and re.search(r"(?<!\w)" + re.escape(rep) + r"(?!\w)", str(st["say"])):
                r.err(f"{sc.get('id', si)}.{ki}", f"E28 lời đọc gõ phiên âm “{rep}” — phụ đề sẽ hiện phiên âm; "
                                                  f"viết tên gốc (lexicon tự đổi khi đọc)")
        spoken = lexicon_apply(str(st["say"]), hits, crs)
        for tok in re.findall(r"[^\W\d_]+", spoken):
            if len(tok) > 1 and not is_vietnamese_syllable(tok) and tok.lower() not in lex["foreign_ok"]:
                foreign.setdefault(tok, f"{sc.get('id', si)}.{ki}")
    for tok, where in sorted(foreign.items()):
        r.warn(where, f"từ “{tok}” không phải âm tiết tiếng Việt — thêm luật đọc vào lexicon_vi.yaml, "
                      f"hoặc thêm vào foreign_ok sau khi đã nghe/ASR xác nhận đọc đúng")
    used = sorted({f"{h[1]}→{h[2]}" for h in hits})
    r.ok(f"phát âm: {len(lex['must_not_change'])} từ tự kiểm không bị đổi; luật đã áp dụng: {used}")
    est_min = words_total / 150
    r.ok(f"ước lượng thời lượng lời đọc ≈ {est_min:.1f} phút ({words_total} từ, 150 từ/phút)")
    # 3. KaTeX parse
    items = []
    for si, sc, ki, st in iter_steps(spec):
        for mi, m in enumerate(MATH_RE.finditer(katex_safe(str(st.get("show", ""))))):
            tex = m.group(1) if m.group(1) is not None else m.group(2)
            items.append({"id": f"{sc.get('id', si)}.{ki}.m{mi}", "tex": tex, "display": m.group(1) is not None})
    if shutil.which("node") is None:
        r.err("katex", "không có node — không kiểm tra được công thức (NOT_VERIFIED)")
    else:
        res = subprocess.run(["node", str(TOOLS / "katex_check.js")], input=json.dumps(items),
                             capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            r.err("katex", f"katex_check.js lỗi: {res.stderr[:300]}")
        else:
            errs = json.loads(res.stdout or "[]")
            for e in errs:
                r.err(e["id"], f"KaTeX: {e['error']}  ←  {e['tex']}")
            if not errs:
                r.ok(f"KaTeX parse {len(items)} công thức không lỗi")
    # E36: chuỗi hệ 16 viết liền trong lời đọc (“3E200000”) — TTS có thể đọc “200000” thành “hai trăm nghìn”; hai mô hình ASR chép ra hai
    #      kiểu khác nhau (lỗi thật CSA L03 2026-10-29). Quy ước: đọc tách từng chữ số “3 E 2 0 0 0 0 0” (như OSY L09).
    for si, sc, ki, st in iter_steps(spec):
        for m in re.finditer(r"\b(?=[0-9A-F]*\d)(?=[0-9A-F]*[A-F])[0-9A-F]{4,}\b", str(st.get("say") or "")):
            r.warn(f"{sc.get('id', si)}.{ki}", f"E36 chuỗi hệ 16 “{m.group(0)}” viết liền trong lời đọc — tách từng chữ số: “{' '.join(m.group(0))}”")
    # E38: một từ chỉ một cách viết trên màn hình và phụ đề, toàn kho (lỗi thật 2026-10-30: “luỹ/lũy”, “tùy/tuỳ”, “logarit/lôgarit”
    #      lẫn trong cùng khoá). Dạng chuẩn = dạng chiếm đa số khi rà (audit/review/audit_all.py; 267 lũy / 75 luỹ …).
    for si, sc, ki, st in iter_steps(spec):
        vis = str(st.get("say", "")) + " " + re.sub(r"<[^>]+>", " ", str(st.get("show", "")))
        for w, canon in SPELL_CANON.items():
            if re.search(r"(?<!\w)" + w + r"(?!\w)", vis, re.I):
                r.warn(f"{sc.get('id', si)}.{ki}", f"E38 viết “{w}” — toàn kho thống nhất viết “{canon}”")
    # E33: tên lệnh mất dấu “\” vẫn qua KaTeX (in thành chữ nghiêng) — lỗi thật DMS L01 2026-10-27: sed nuốt “\” → $equiv$
    bare = 0
    for it in items:
        body = re.sub(r"\\(?:text|mathrm|operatorname|texttt|textbf|mathit)\{[^{}]*\}", " ", it["tex"])
        for m in BARE_CMD_RE.finditer(body):
            bare += 1
            r.err(it["id"], f"E33 “{m.group(0)}” trong công thức thiếu dấu \\ — KaTeX in ra chữ nghiêng thay vì ký hiệu; viết \\{m.group(0)}")
    if not bare:
        r.ok("E33 không có tên lệnh LaTeX thiếu dấu \\")
    # 4. ký hiệu phải được giải thích trước khi dùng
    regall = registry(course_of(spec))
    reg = regall["symbols"]
    known = set(spec.get("assumes") or []) | {s["id"] for s in reg if s.get("base")}
    ids = {s["id"] for s in reg}
    for a in spec.get("assumes") or []:
        if a not in ids:
            r.err("assumes", f"ký hiệu `{a}` không có trong tools/registry/symbols.yaml")
    introduced_all = set()
    for si, sc, ki, st in iter_steps(spec):
        where = f"{sc.get('id', si)}.{ki}"
        intro = set(st.get("introduces") or [])
        for i in intro:
            if i not in ids:
                r.err(where, f"introduces `{i}` không có trong registry")
        known |= intro
        introduced_all |= intro
        show = str(st.get("show", ""))
        if "<marker" in show and "userSpaceOnUse" not in show:
            r.err(where, "SVG <marker> thiếu markerUnits=\"userSpaceOnUse\" — đầu mũi tên sẽ phóng to theo độ dày nét")
        plain = re.sub(r"<[^>]+>", " ", MATH_RE.sub(" ", show))
        if re.search(r"[✗✘]", plain):
            r.err(where, "ký tự ✗/✘ hiển thị giống chữ X (dễ nhầm với biến x) — dùng chữ <b class=\"red\">(sai)</b>")
        for s in reg:
            if s["id"] not in known and s.get("unicode") and any(ch in plain for ch in s["unicode"]):
                r.err(where, f"ký tự “{s['unicode']}” ({s['name']}) xuất hiện trong chữ trước khi được giải thích")
                known.add(s["id"])
        for m in MATH_RE.finditer(show):
            tex = m.group(1) or m.group(2)
            for s in reg:
                if s["id"] not in known and re.search(s["pattern"], tex):
                    r.err(where, f"dùng ký hiệu “{s['name']}” (`{s['id']}`) trước khi giải thích — thêm `introduces: [{s['id']}]` "
                                 f"ở step giải thích nó, hoặc khai báo trong `assumes` nếu đã học ở bài trước. Trong: {tex[:50]}")
                    known.add(s["id"])  # báo một lần
    layout = set(regall.get("layout_commands") or [])
    unknown = {}
    for si, sc, ki, st in iter_steps(spec):
        for m in MATH_RE.finditer(str(st.get("show", ""))):
            tex = m.group(1) or m.group(2)
            for cm in re.finditer(r"\\([a-zA-Z]+)", tex):
                cmd, probe = cm.group(1), tex[cm.start():cm.start() + 24]  # lệnh + đối số thật của nó
                if cmd not in layout and not any(re.match(s["pattern"], probe) for s in reg):
                    unknown.setdefault(cmd, f"{sc.get('id', si)}.{ki}")
    for cmd, where in sorted(unknown.items()):
        r.warn(where, f"lệnh \\{cmd} chưa có trong registry — nếu là ký hiệu toán mới, hãy đăng ký và giải thích nó")
    # 4b. nhất quán ký hiệu: cùng một khái niệm không được viết hai kiểu trong một bài
    #      (ngoại lệ: step có `notation_note: true` — step giải thích sự tương đương)
    for rule in regall.get("consistency") or []:
        seen = {}
        for si, sc, ki, st in iter_steps(spec):
            if st.get("notation_note"):
                continue
            for m in MATH_RE.finditer(str(st.get("show", ""))):
                tex = m.group(1) or m.group(2)
                for vi, pat in enumerate(rule["variants"]):
                    if re.search(pat, tex):
                        seen.setdefault(vi, f"{sc.get('id', si)}.{ki}")
        if len(seen) > 1:
            locs = ", ".join(f"kiểu {vi + 1} ở {w}" for vi, w in sorted(seen.items()))
            r.err("notation", f"{rule['name']}: viết lẫn nhiều kiểu ({locs}). {rule['fix']}")
    # 4c. cùng một ký hiệu vừa gõ bằng ký tự Unicode trong chữ (⇒, ·, ⇔) vừa viết bằng LaTeX trong công thức (⟹, ⋅, ⟺):
    #     hai hình dạng khác nhau cho một nghĩa → người mới tưởng là hai ký hiệu
    for s in reg:
        if not s.get("unicode") or s.get("base"):
            continue
        in_text = in_math = None
        for si, sc, ki, st in iter_steps(spec):
            if st.get("notation_note"):
                continue
            show = str(st.get("show", ""))
            plain = re.sub(r"<[^>]+>", " ", MATH_RE.sub(" ", show))
            if in_text is None and any(ch in plain for ch in s["unicode"]):
                in_text = f"{sc.get('id', si)}.{ki}"
            if in_math is None and any(re.search(s["pattern"], m.group(1) or m.group(2)) for m in MATH_RE.finditer(show)):
                in_math = f"{sc.get('id', si)}.{ki}"
        if in_text and in_math:
            r.err("notation", f"“{s['name']}” vừa gõ ký tự “{s['unicode']}” trong chữ ({in_text}) vừa viết LaTeX trong công thức "
                              f"({in_math}) — hai hình dạng khác nhau; hãy đưa vào công thức ($...$) hoặc dùng lời")
    # 4d. kích thước ma trận viết bằng \sz{M}{N}: gõ \times trong số mũ (ℝ^{2×3}) làm lint không phân biệt được
    #     “2 hàng, 3 cột” với phép nhân hai số
    for si, sc, ki, st in iter_steps(spec):
        for m in MATH_RE.finditer(str(st.get("show", ""))):
            tex = m.group(1) or m.group(2)
            if re.search(r"\^\{[^{}]*\\times", tex):
                r.err(f"{sc.get('id', si)}.{ki}", f"kích thước ma trận gõ bằng \\times — dùng \\sz{{M}}{{N}}. Trong: {tex[:50]}")
    r.ok(f"ký hiệu được giới thiệu trong bài: {sorted(introduced_all)}")
    spec["_introduces"] = sorted(introduced_all)
    # 5. phép tính trong bài phải đúng (sympy/numpy)
    ns = _check_namespace()
    n_checks = 0
    for si, sc in enumerate(spec["scenes"]):
        for ci, expr in enumerate(sc.get("checks") or []):
            n_checks += 1
            # E26: “abs(4.8111 - 4.81) < 0.01” chỉ so hai số chép tay → luôn đúng, không kiểm gì (lỗi thật L10 bản nháp)
            if re.search(r"abs\(\s*-?[0-9.]+\s*-\s*-?[0-9.]+\s*\)", str(expr)):
                r.warn(f"{sc.get('id', si)}#check{ci}", "E26 check chỉ so hai hằng số chép tay — không kiểm được gì; "
                                                       "hãy tính lại giá trị trong biểu thức (mô phỏng, sympy)")
            # E35: một phép so sánh có hai vế giống hệt nhau (“[7, 5, 3] == [7, 5, 3]”) luôn đúng — check giả (lỗi thật OSY L03, L07 bản nháp)
            # Mức WARN: “a <= a” có thể là kiểm phản xạ có chủ đích — người viết phải xem và sửa hoặc giải thích.
            if (taut := _tautology(str(expr))):
                r.warn(f"{sc.get('id', si)}#check{ci}", f"E35 check có phép so sánh hai vế giống hệt nhau — luôn đúng, không kiểm gì: {taut}")
            try:
                val = eval(expr, dict(ns))
                if str(val) == "True":  # chỉ chấp nhận boolean True tường minh
                    r.ok(f"check {sc.get('id', si)}#{ci}: {expr}")
                else:
                    r.err(f"{sc.get('id', si)}#check{ci}", f"phép tính SAI: {expr}  → {val}")
            except Exception as e:
                r.err(f"{sc.get('id', si)}#check{ci}", f"không chạy được: {expr} → {type(e).__name__}: {e}")
    if prof.get("evidence") == "numbers" and any(sc.get("kind") == "example" for sc in spec["scenes"]) and not any(
            sc.get("checks") for sc in spec["scenes"] if sc.get("kind") in ("example", "check", "quiz")):
        r.err("checks", "có ví dụ số nhưng không có `checks` nào — mọi con số trên màn hình phải được máy kiểm chứng")
    elif n_checks:
        r.ok(f"đã chạy {n_checks} phép kiểm tra số học")
    lint_focus(spec, r)
    # E51: công thức $…$ bên trong <svg> không qua KaTeX — hiện nguyên dấu $ (suýt lọt ở AIF L03 bản đầu, 2026-10-31);
    # trong hình viết chữ thường hoặc ký tự Unicode, công thức đặt ngoài hình
    for si, sc, ki, st in iter_steps(spec):
        for svg in re.findall(r"<svg.*?</svg>", str(st.get("show", "")), re.S):
            if "$" in re.sub(r"<[^>]+>", "", svg):
                r.err(f"{sc.get('id', si)}.{ki}", "E51 có công thức $…$ trong <svg> — KaTeX không vẽ trong hình, sẽ hiện nguyên dấu $")
    lint_depth(spec, r)
    lint_profile_rules(spec, r, prof)
    # E30: ghi chú xem xét ASR cho câu không còn trong bài — ghi chú cũ che mất việc phải nghe lại câu mới
    caps = {s.strip() for _, _, _, st in iter_steps(spec) for s in sentences(st.get("say") or "")}
    for x in spec.get("asr_reviewed") or []:
        if str(x.get("sentence", "")).strip() not in caps:
            r.warn("asr_reviewed", f"E30 câu đã xem xét không còn trong bài: “{str(x.get('sentence'))[:60]}…” — xoá mục này")
    return r


VISUAL_RE = re.compile(r"<svg|<table|class=[\"']chain[\"']|\$\$|<pre|class=[\"']code[\"']")
DEPTH_MIN_WORDS = 900          # ≈ 6,5 phút ở 140 từ/phút; bài “mỏng” của đợt 2026-10-28 có trung vị ≈ 700 từ (4,9 phút)
DEPTH_MAX_TEXT_RUN = 3         # quá 3 khung liền chỉ có chữ thì người mất gốc mất dấu (pedagogy_scan: trung vị cũ là 5)


def lint_depth(spec, r):
    """E39 (bài khai `depth: full`, pedagogy.md luật 22): đủ cho người mới / mất gốc — ôn nền, hình cơ chế, làm từng bước,
    tự kiểm, đáp án từng bước, chuỗi logic. Lỗi thật (audit/review/PEDAGOGY_REVIEW.md, 2026-10-31): 270 bài của 19 khoá chỉ có
    6 phân cảnh, 1 step ví dụ, 0 hình, ≈ 4,5 phút — đúng nhưng nén, người mất gốc không theo được.
    E40 (bài khai `case: journey`, case-lessons.md mục 5): hành trình của một hệ thống thật theo trục thời gian, mỗi chặng có
    năm, quy mô, nguồn, thực hành rút ra và con số tính lại."""
    scenes = spec.get("scenes") or []
    kinds = {sc.get("kind") for sc in scenes}
    steps = [(sc, st) for sc in scenes for st in sc.get("steps") or []]
    dp = profile_of(spec).get("depth") or {}
    if spec.get("depth") == "full":
        miss = [k for k in dp.get("need", []) if k not in kinds] + \
            ["|".join(g) for g in dp.get("need_any", []) if not kinds & set(g)]
        if miss:
            r.err("depth", f"E39 bài `depth: full` thiếu phân cảnh {miss} — ôn nền, hình dung cơ chế, tự kiểm độc lập")
        vis_kinds = set(dp.get("visual_kinds", []))
        vis_re = r"<svg" if dp.get("visual") == "svg" else r"<svg|<img|<table|class=[\"']chain"
        if not any(re.search(vis_re, str(st.get("show", ""))) for sc, st in steps if sc.get("kind") in vis_kinds):
            r.err("depth", "E39 không có hình cơ chế (<svg>) ở phần giảng — người mới cần THẤY cơ chế, không chỉ đọc định nghĩa"
                  if dp.get("visual") == "svg" else "E39 phần giảng không có hình, bảng hay sơ đồ nào — người mới cần THẤY cấu trúc")
        n_ex = sum(sc.get("kind") in set(dp.get("worked_kinds", [])) for sc, _ in steps)
        if n_ex < dp.get("min_worked", 4):
            r.err("depth", f"E39 chỉ {n_ex} step làm mẫu ({' + '.join(dp.get('worked_kinds', []))}) — cần ≥ {dp.get('min_worked', 4)}, "
                           "mỗi bước một step")
        q = [st for sc, st in steps if sc.get("kind") == "quiz"]
        pi = next((i for i, st in enumerate(q) if st.get("pause")), None)
        if pi is None or len(q) - pi - 1 < 2:
            r.err("depth", "E39 quiz cần `pause` rồi ≥ 2 step đáp án (giải từng bước, không chỉ đáp số)")
        if not any(re.search(r"class=[\"']chain", str(st.get("show", ""))) for sc, st in steps if sc.get("kind") == "recap"):
            r.err("depth", "E39 recap thiếu chuỗi logic (class=\"chain\")")
        run = best = 0
        # hồ sơ visual: any (ngoại ngữ, kỹ năng mềm, xã hội…): hộp nhấn (box) cũng là một khối trực quan
        vis_run = re.compile(VISUAL_RE.pattern + (r"|class=[\"']box" if dp.get("visual") == "any" else ""))
        for sc, st in steps:
            show = str(st.get("show", "") or "")
            run = 0 if (not show.strip() or vis_run.search(show)) else run + 1
            best = max(best, run)
        if best > DEPTH_MAX_TEXT_RUN:
            r.warn("depth", f"E39 có {best} khung liền chỉ có chữ (> {DEPTH_MAX_TEXT_RUN}) — xen hình, bảng hoặc công thức")
        words = sum(len(str(st.get("say", "")).split()) for _, st in steps)
        if words < dp.get("min_words", DEPTH_MIN_WORDS):
            r.warn("depth", f"E39 lời giảng {words} từ (≈ {words / 140:.1f} phút) < {dp.get('min_words', DEPTH_MIN_WORDS)} — "
                            "thường là thiếu bước giải thích")
        if not (r.errors and any("E39" in e for e in r.errors)):
            r.ok("E39 đủ độ sâu cho người mới (ôn nền, hình cơ chế, ≥ 4 bước số, tự kiểm, đáp án từng bước, chuỗi logic)")
    if spec.get("case") == "journey":
        stages = [sc for sc in scenes if isinstance(sc.get("stage"), dict)]
        if len(stages) < 4:
            r.err("journey", f"E40 hành trình cần ≥ 4 chặng có `stage:` (khai sinh → tăng trưởng → quy mô lớn → ổn định/tiến hoá), "
                             f"đang có {len(stages)}")
        prev = 0
        for sc in stages:
            stg, where = sc["stage"], f"{sc.get('id')}.stage"
            for k in ("year", "scale", "source", "practice"):
                if not str(stg.get(k, "")).strip():
                    r.err(where, f"E40 chặng thiếu `{k}` (năm, quy mô, nguồn đã đọc nguyên văn, thực hành chuyên gia rút ra)")
            m = re.search(r"\d{4}", str(stg.get("year", "")))
            if m:
                if int(m.group(0)) < prev:
                    r.err(where, f"E40 chặng năm {m.group(0)} đứng sau chặng năm {prev} — hành trình phải theo trục thời gian")
                prev = max(prev, int(m.group(0)))
                if m.group(0) not in str(sc.get("title", "")):
                    r.warn(where, f"E40 tiêu đề chặng không ghi năm {m.group(0)} — người xem cần thấy mình đang ở mốc nào")
            if not sc.get("checks"):
                r.err(where, "E40 chặng không có `checks` — mỗi chặng tính lại ít nhất một con số (quy mô, chi phí, độ sẵn sàng)")
            # nguồn chặng ghi bằng nhãn ngắn [B15] (khai trong `source:` của bài) hoặc bằng đầu tên nguồn
            keys = re.findall(r"\[[A-Za-z0-9]+\]", str(stg.get("source", ""))) or \
                [re.split(r"[,(;§]", str(stg.get("source", "")))[0].strip()[:25]]
            for key in keys:
                if key and key not in str(spec.get("source", "")):
                    r.warn(where, f"E40 nguồn “{key}” của chặng chưa có trong `source:` của bài")
        if len(stages) >= 4 and not any("E40" in e for e in r.errors):
            r.ok(f"E40 hành trình {len(stages)} chặng theo trục thời gian, mỗi chặng có năm, quy mô, nguồn, thực hành và con số tính lại")


# ngưỡng E32: ≥ 2 câu trên khối ≥ 2 phần (trước 2026-10-27 là 3 và 3 — CS115 lọt 399/612 step thiếu focus: một dòng
# chữ + một công thức với 2 câu là dạng phổ biến nhất; audit/cs115/REVIEW_CS115_FOCUS.md)
DENSE_UNITS, DENSE_SENTENCES = 2, 2


def lint_focus(spec, r):
    """E31: `focus` phải có đúng một mục cho mỗi câu và trỏ tới phần có thật trên bảng.
    E32: step có ≥3 câu nói về một khối có ≥3 phần mà không có `focus` → người xem phải tự dò câu đang nói chỗ nào."""
    n_focus = 0
    for si, sc in enumerate(spec["scenes"]):
        blocks = []
        for ki, st in enumerate(sc.get("steps") or []):
            where = f"{sc.get('id', si)}.{ki}"
            if st.get("clear"):
                blocks = []
            if st.get("show"):
                blocks.append(html_units(str(st["show"])))
            sents = sentences(st.get("say") or "")
            foc = st.get("focus")
            if foc is None:
                if st.get("show") and len(blocks[-1]) >= DENSE_UNITS and len(sents) >= DENSE_SENTENCES:
                    r.warn(where, f"E32 {len(sents)} câu nói về khối có {len(blocks[-1])} phần mà không có `focus` — "
                                  "người xem không biết câu nào nói chỗ nào")
                elif not st.get("show") and len(blocks) >= DENSE_UNITS and len(sents) >= DENSE_SENTENCES:
                    r.warn(where, f"E32 {len(sents)} câu không có `show` mà nói tiếp về bảng {len(blocks)} khối, "
                                  "thiếu `focus` (“B1”, “B2:3”…) — người xem không biết câu nào nói khối nào")
                continue
            n_focus += 1
            if not isinstance(foc, list) or len(foc) != len(sents):
                r.err(where, f"E31 `focus` phải là danh sách đúng {len(sents)} mục (mỗi câu một mục), đang có "
                             f"{len(foc) if isinstance(foc, list) else type(foc).__name__}")
                continue
            for j, item in enumerate(foc):
                try:
                    targets = parse_focus(item)
                except ValueError as e:
                    r.err(where, f"E31 câu {j + 1}: {e}")
                    continue
                for b, u, v in targets:
                    if b is None and not st.get("show"):
                        r.err(where, f"E31 câu {j + 1}: step không có `show` — phải ghi khối, ví dụ “B1:2”")
                        continue
                    bi = len(blocks) - 1 if b is None else b
                    if not 0 <= bi < len(blocks):
                        r.err(where, f"E31 câu {j + 1}: bảng chỉ có {len(blocks)} khối, không có khối {bi + 1}")
                        continue
                    us = blocks[bi]
                    if u and u > len(us):
                        r.err(where, f"E31 câu {j + 1}: khối {bi + 1} chỉ có {len(us)} phần, không có phần {u}")
                    elif u and v and v > len(us[u - 1]["kids"]):
                        r.err(where, f"E31 câu {j + 1}: phần {u} của khối {bi + 1} chỉ có {len(us[u - 1]['kids'])} phần con")
    if n_focus:
        r.ok(f"{n_focus} step có `focus` theo câu")


def _tautology(expr):
    """Trả về đoạn so sánh nếu có phép ==/<=/>= mà hai vế kề nhau có VĂN BẢN NGUỒN giống hệt (bỏ khoảng trắng), ngược lại None.
    So văn bản chứ không so cây cú pháp: “0xFF == 255” là kiểm đổi hệ (hai cây giống nhau nhưng nguồn khác) — không báo."""
    import ast
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        return None
    src = lambda n: re.sub(r"\s+", "", ast.get_source_segment(expr, n) or "")
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            sides = [node.left] + node.comparators
            for op, a, b in zip(node.ops, sides, sides[1:]):
                if isinstance(op, (ast.Eq, ast.LtE, ast.GtE, ast.Is)) and src(a) and src(a) == src(b):
                    return ast.get_source_segment(expr, node)
    return None


def _check_namespace():
    import numpy as np
    import sympy as sp
    import checklib  # thuật toán tham chiếu (phân hoạch, Dijkstra, Kruskal…) cho check có nhiều bước — đối chiếu vét cạn ở
    #                  audit/cs112/verify_cs112_p2.py mục X1
    ns = {"sp": sp, "np": np, "math": math, "alg": checklib, "Fraction": __import__("fractions").Fraction}
    ns.update({k: getattr(sp, k) for k in ("Matrix", "Rational", "sqrt", "simplify", "symbols", "pi", "acos",
                                           "Abs", "nsimplify", "N", "deg", "atan2", "S", "diff", "solve")})
    return ns


# ───────────────────────────── FOCUS ─────────────────────────────
# `focus:` của một step = một mục cho MỖI câu của `say`: câu đang nói tới chỗ nào trên bảng thì chỗ đó được viền và
# các phần khác của khối mờ đi (người xem không phải tự dò). Mục: 0 = cả khối; 2 = phần thứ 2 của khối mới;
# “2.3” = phần con thứ 3 của phần 2 (dòng thứ 3 nếu phần 2 là bảng); “B1” = cả khối thứ 1 trên bảng; “B1:2” = phần 2
# của khối 1; danh sách [1, 3] = nhiều chỗ. “Phần” = phần tử cấp cao của khối (<p>, <div>, <table>, mỗi công thức $…$).
FOCUS_RE = re.compile(r"^(?:B(\d+)(?::(\d+)(?:\.(\d+))?)?|(\d+)(?:\.(\d+))?)$")


def parse_focus(item):
    """Mục focus của một câu → danh sách [khối (None = khối mới của step, 0-based), phần (1-based|None), phần con]."""
    if item in (None, 0, "0", ""):
        return []
    out = []
    for it in (item if isinstance(item, list) else [item]):
        m = FOCUS_RE.match(str(it).strip())
        if not m or str(it).strip() == "0":
            raise ValueError(f"mục focus không hợp lệ: {it!r}")
        if m.group(1):
            out.append([int(m.group(1)) - 1, int(m.group(2)) if m.group(2) else None, int(m.group(3)) if m.group(3) else None])
        else:
            out.append([None, int(m.group(4)), int(m.group(5)) if m.group(5) else None])
    return out


VOID_TAGS = {"br", "img", "hr", "input", "wbr", "col", "area", "source"}


def html_units(html):
    """Cây phần tử cấp cao của một khối, đếm GIỐNG trình duyệt sau KaTeX: mỗi công thức $…$/$$…$$ là một phần tử,
    <br> không tính, bảng thì phần con là các dòng <tr>. Trả về list các nút {tag, kids}."""
    from html.parser import HTMLParser
    html = MATH_RE.sub("<m></m>", html)
    root = {"tag": "root", "kids": []}
    stack = [root]

    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):
            node = {"tag": tag, "kids": []}
            if tag != "br":
                stack[-1]["kids"].append(node)
            if tag not in VOID_TAGS:
                stack.append(node)

        def handle_endtag(self, tag):
            for k in range(len(stack) - 1, 0, -1):
                if stack[k]["tag"] == tag:
                    del stack[k:]
                    break
    P().feed(html)

    def rows(n):   # trình duyệt chèn <tbody>: dòng của bảng là phần con trực tiếp
        if n["tag"] == "table":
            return [r for k in n["kids"] for r in (k["kids"] if k["tag"] in ("tbody", "thead") else [k]) if r["tag"] == "tr"]
        return n["kids"]
    for n in root["kids"]:
        n["kids"] = rows(n)
    return root["kids"]


# ───────────────────────────── TIMELINE ─────────────────────────────
def voice_override(spec):
    """out/<khoá>/<id>/voice_override.json {"voice": "vieneu:…", "reason": …}: giọng dự phòng cho CẢ bài (edge không ổn định).
    Một bài chỉ có MỘT giọng — không bao giờ trộn giọng trong bài, càng không trong một câu. Xoá tệp rồi build lại = về giọng gốc."""
    f = OUT / course_of(spec) / spec["id"] / "voice_override.json"
    return json.loads(f.read_text(encoding="utf-8"))["voice"] if f.exists() else None


def build_frames(spec):
    """Mỗi câu của `say` = 1 khung hình. Bảng trong 1 scene cộng dồn các `show`; `clear: true` để xoá bảng."""
    frames = []
    ov = voice_override(spec) if spec.get("id") and spec.get("_path") else None
    for si, sc in enumerate(spec["scenes"]):
        blocks = []
        for ki, st in enumerate(sc["steps"]):
            if st.get("clear"):
                blocks = []
            if st.get("show"):
                blocks.append(katex_safe(str(st["show"]).strip()))
            active = len(blocks) - 1 if st.get("show") else -1
            sents = sentences(st["say"])
            foc = st.get("focus") or []
            # hồ sơ language: step khai giọng bản ngữ → cả step đọc bằng giọng đó (giọng dự phòng của bài không đè lên)
            foreign = bool(st.get("voice")) and voice_lang(st["voice"]) != voice_lang(spec.get("voice"))
            for j, s in enumerate(sents):
                last = j == len(sents) - 1
                frames.append({
                    "scene": si, "scene_id": sc.get("id", f"s{si}"), "scene_title": sc["title"], "kind": sc["kind"],
                    "blocks": list(blocks), "active": active, "caption": s,
                    "focus": [[active if b is None else b, u, v] for b, u, v in parse_focus(foc[j] if j < len(foc) else 0)],
                    "tts": s if foreign else lexicon_apply(s, course=course_of(spec)),
                    "voice": st.get("voice") or ov or spec.get("voice", "vi-VN-HoaiMyNeural"),
                    "lang": voice_lang(st.get("voice") or spec.get("voice")),
                    "rate": spec.get("rate", "-5%"),
                    "pad": (float(st.get("hold", 0.35)) if last else 0.18) + (float(st.get("pause", 0)) if last else 0),
                    "pause": bool(st.get("pause")) and last,
                })
    return frames


def tts_key(fr):
    h = hashlib.sha256(f"{fr['voice']}|{fr['rate']}|{fr['tts']}".encode("utf-8")).hexdigest()[:24]
    return CACHE / f"{h}.wav"


# ───────────────────────────── TTS ─────────────────────────────
# Audio bị cắt cụt: lỗi thật L05 khung 75 — dịch vụ trả 0,72 s cho câu 16 từ (0,045 s/từ) mà không báo lỗi; ASR chỉ
# nghe được “Với hàm...”. Đo 923 câu L01–L05: trung vị 0,346 s/từ, nhanh nhất (ngoài câu lỗi) 0,256 s/từ.
MIN_SEC_PER_WORD = 0.15
# Câu ≥ 4 từ: ngưỡng chặt hơn. Lỗi thật 2026-10-30 (audit/review/tts_speed_scan.py trên 17 810 câu): AIF L08 0,175 s/từ,
# CSA L11 0,164, DBS L15 0,189 — cả ba cụt đuôi (small và medium cùng mất phần cuối) mà vẫn qua ngưỡng 0,15; không câu
# đủ nào trong kho dưới 0,22. Câu < 4 từ giữ 0,15 vì khoảng lặng đầu/cuối chi phối thời lượng.
MIN_SEC_PER_WORD_LONG = 0.20
TTS_TIMEOUT = 60  # giây cho mỗi lần gọi edge-tts
# Đo 2026-10-30 (audit/perf/tts_probe.py): edge-tts trả “NoAudioReceived” ~50 % số lần gọi kể cả khi gửi TỪNG câu một
# (đồng thời 1: 3/6 lỗi, 66 s; đồng thời 3: 0/6 lỗi, 26 s) → lỗi do phía dịch vụ, giảm đồng thời không giảm lỗi.
# Với ~50 % lỗi ngẫu nhiên, 7 lần thử/câu vẫn để ~0,8 % câu hỏng → ~25 % bài BLOCKED → hàng đợi chờ 10 phút
# (CLD 9/13 bài, +15–17 phút/bài). Nên: thử lại câu hỏng thêm TTS_ROUNDS lượt ngay trong lệnh `tts`, nghỉ tăng dần,
# trước khi báo BLOCKED. Các lượt chỉ gửi lại câu còn thiếu (câu đã đọc nằm trong cache) → không tăng tải vô ích.
TTS_CONCURRENCY = int(os.environ.get("LV_TTS_CONCURRENCY", "3"))
TTS_ROUNDS = int(os.environ.get("LV_TTS_ROUNDS", "3"))          # số lượt bổ sung cho câu còn hỏng
TTS_ROUND_PAUSE = (30, 60, 120)                                  # giây nghỉ trước lượt bổ sung 1, 2, 3…
TTS_STATS = {"retry": 0, "err": {}}


def tts_truncated(fr, wav):
    words = len(fr["tts"].replace("-", " ").split())
    return wav_seconds(wav) < (MIN_SEC_PER_WORD_LONG if words >= 4 else MIN_SEC_PER_WORD) * words


# Nguồn TTS dự phòng (2026-10-28, edge-tts bị chặn từng đợt — “NoAudioReceived”):
#  • edge → azure: CÙNG mô hình giọng Microsoft (vi-VN-NamMinhNeural) qua Azure Speech REST (cần AZURE_SPEECH_KEY +
#    AZURE_SPEECH_REGION; CITED learn.microsoft.com …/rest-text-to-speech). Cùng giọng nên thay được TỪNG CÂU, khoá cache giữ nguyên;
#    tệp <hash>.src ghi nguồn đã đọc câu đó (bằng chứng, build_report đếm).
#  • piper:<mô hình>[#người đọc]: giọng KHÁC, chạy cục bộ (tools/vendor/piper). Chỉ chọn qua trường `voice` cho CẢ bài — khoá cache
#    đổi theo voice nên cả bài đọc lại bằng một giọng, không bao giờ trộn giọng trong một bài. Đo giọng: audit/tts_fallback_probe.py.
def _azure_ready():
    return bool(os.environ.get("AZURE_SPEECH_KEY") and os.environ.get("AZURE_SPEECH_REGION"))


def _azure_synth(fr, out_wav_raw):
    import urllib.request
    from xml.sax.saxutils import escape
    lang = "-".join(fr["voice"].split("-")[:2])
    ssml = (f"<speak version='1.0' xml:lang='{lang}'><voice name='{fr['voice']}'><prosody rate='{fr['rate']}'>"
            f"{escape(fr['tts'])}</prosody></voice></speak>")
    req = urllib.request.Request(
        f"https://{os.environ['AZURE_SPEECH_REGION']}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml.encode("utf-8"),
        headers={"Ocp-Apim-Subscription-Key": os.environ["AZURE_SPEECH_KEY"], "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "lecture-video"}, method="POST")
    with urllib.request.urlopen(req, timeout=TTS_TIMEOUT) as r:
        out_wav_raw.write_bytes(r.read())


def _piper_synth(fr, out_wav_raw):
    from piper import PiperVoice, SynthesisConfig
    spec = fr["voice"].split(":", 1)[1]
    name, _, spk = spec.partition("#")
    model = ROOT / "tools" / "vendor" / "piper" / f"{name}.onnx"
    v = PiperVoice.load(str(model))
    # tốc độ: “-5%” của edge → length_scale 1/0,95 (dài hơn 5%)
    pct = float(str(fr["rate"]).rstrip("%") or 0)
    cfg = SynthesisConfig(speaker_id=int(spk) if spk else None, length_scale=1 / (1 + pct / 100))
    with wave.open(str(out_wav_raw), "wb") as w:
        v.synthesize_wav(fr["tts"], w, syn_config=cfg)


async def _tts_one(fr, sem, ff):
    import edge_tts
    wav = tts_key(fr)
    if wav.exists() and wav.stat().st_size > 1000:
        if not tts_truncated(fr, wav):
            return "cached"
        wav.unlink()  # bản cache bị cắt cụt → đọc lại
    mp3 = wav.with_suffix(".mp3")
    raw = wav.with_suffix(".raw.wav")
    async with sem:
        for attempt in range(7):
            try:
                if fr["voice"].startswith("piper:"):
                    await asyncio.to_thread(_piper_synth, fr, raw); src_file, src = raw, "piper"
                else:
                    try:
                        # thời hạn: websocket đứng giữa chừng thì `save` chờ mãi, vòng thử lại không bao giờ chạy
                        # (lỗi thật L07: build treo nhiều giờ, không in gì)
                        await asyncio.wait_for(
                            edge_tts.Communicate(fr["tts"], fr["voice"], rate=fr["rate"]).save(str(mp3)), TTS_TIMEOUT)
                        src_file, src = mp3, "edge"
                    except Exception:
                        if not _azure_ready():
                            raise
                        await asyncio.to_thread(_azure_synth, fr, raw); src_file, src = raw, "azure"
                subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(src_file), "-ac", "1", "-ar", str(SR), str(wav)],
                               check=True, timeout=120)
                raw.unlink(missing_ok=True)
                if tts_truncated(fr, wav):
                    raise RuntimeError(f"audio bị cắt cụt ({wav_seconds(wav):.2f} s)")
                wav.with_suffix(".src").write_text(src, encoding="utf-8")
                break
            except Exception as e:  # mạng chập chờn, hoặc audio bị cắt cụt
                wav.unlink(missing_ok=True)
                TTS_STATS["retry"] += 1
                TTS_STATS["err"][type(e).__name__] = TTS_STATS["err"].get(type(e).__name__, 0) + 1
                if attempt == 6:
                    # không raise: một câu lỗi không được huỷ cả lượt (lỗi thật L03: dịch vụ giới hạn tần suất,
                    # gather huỷ mọi câu đang đọc → mỗi lượt chỉ thêm vài câu vào cache)
                    print(f"[FAIL] tts “{fr['tts'][:60]}”: {type(e).__name__}: {e}")
                    return "fail"
                # lùi dần có nhiễu ngẫu nhiên: các câu đồng thời không cùng gửi lại một lúc
                await asyncio.sleep(min(15, 2 * (attempt + 1)) + random.uniform(0, 2))
    mp3.unlink(missing_ok=True)
    return "new"


def _vieneu_batch(frames, ff):
    """voice “vieneu:<giọng>” (cả bài): gom mọi câu chưa có cache vào MỘT lần gọi tools/tts_vieneu.py trong .venv-tts
    (nạp mô hình một lần). Trả về số câu lỗi."""
    todo = [fr for fr in frames if not (tts_key(fr).exists() and tts_key(fr).stat().st_size > 1000 and not tts_truncated(fr, tts_key(fr)))]
    if not todo:
        return 0
    py = ROOT / ".venv-tts" / "Scripts" / "python.exe"
    if not py.exists():
        py = ROOT / ".venv-tts" / "bin" / "python"
    jobs = [{"text": fr["tts"], "voice": fr["voice"].split(":", 1)[1], "out": str(tts_key(fr).with_suffix(".raw.wav"))} for fr in todo]
    r = subprocess.run([str(py), str(ROOT / "tools" / "tts_vieneu.py")], input=json.dumps(jobs, ensure_ascii=False),
                       capture_output=True, text=True, encoding="utf-8", timeout=6 * 3600)
    fails = 0
    for fr in todo:
        wav, raw = tts_key(fr), tts_key(fr).with_suffix(".raw.wav")
        if not raw.exists():
            fails += 1; print(f"[FAIL] tts vieneu “{fr['tts'][:60]}”"); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(raw), "-ac", "1", "-ar", str(SR), str(wav)], check=True, timeout=120)
        raw.unlink(missing_ok=True)
        if tts_truncated(fr, wav):
            wav.unlink(); fails += 1; print(f"[FAIL] tts vieneu cắt cụt “{fr['tts'][:60]}”"); continue
        wav.with_suffix(".src").write_text("vieneu", encoding="utf-8")
    if fails and r.stderr:
        print(r.stderr[-800:])
    return fails


def cmd_tts(spec):
    CACHE.mkdir(parents=True, exist_ok=True)
    frames = build_frames(spec)
    ff = ffmpeg_exe()
    if any(fr["voice"].startswith("vieneu:") for fr in frames):
        assert all(fr["voice"] == frames[0]["voice"] for fr in frames), "giọng vieneu phải dùng cho CẢ bài, không trộn giọng"
        n = _vieneu_batch(frames, ff)
        print(f"tts: {len(frames)} câu (vieneu, {n} lỗi)")
        if n:
            print("tts BLOCKED: chạy lại `tts` (cache giữ phần đã đọc)")
        return 1 if n else 0

    async def run(todo):
        sem = asyncio.Semaphore(TTS_CONCURRENCY)
        return await asyncio.gather(*[_tts_one(fr, sem, ff) for fr in todo])
    t0 = time.time()
    res = asyncio.run(run(frames))
    first_new = res.count("new")
    for rnd in range(TTS_ROUNDS):
        bad = [k for k, r in enumerate(res) if r == "fail"]
        if not bad:
            break
        pause = TTS_ROUND_PAUSE[min(rnd, len(TTS_ROUND_PAUSE) - 1)]
        print(f"tts: còn {len(bad)} câu hỏng → nghỉ {pause} s rồi đọc lại (lượt bổ sung {rnd + 1}/{TTS_ROUNDS})", flush=True)
        time.sleep(pause)
        for k, r in zip(bad, asyncio.run(run([frames[k] for k in bad]))):
            res[k] = r
    errs = ", ".join(f"{k}×{v}" for k, v in sorted(TTS_STATS["err"].items())) or "không"
    late = res.count("new") - first_new
    print(f"tts: {len(res)} câu ({res.count('new')} mới, {res.count('cached')} từ cache, {res.count('fail')} lỗi) "
          f"trong {time.time() - t0:.0f} s; thử lại {TTS_STATS['retry']} lần (lỗi: {errs}); đồng thời {TTS_CONCURRENCY}"
          + (f"; {late} câu xong ở lượt bổ sung" if late else ""), flush=True)
    if res.count("fail"):
        print("tts BLOCKED: chạy lại `tts` sau ít phút (cache giữ phần đã đọc)")
        return 1
    return 0


def wav_seconds(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def timeline(spec, frames):
    t = 0.0
    for fr in frames:
        wav = tts_key(fr)
        speech = wav_seconds(wav) if wav.exists() else len(fr["caption"].split()) / 2.5
        nfr = math.ceil((speech + fr["pad"]) * FPS)
        fr["speech"], fr["dur"], fr["t0"] = speech, nfr / FPS, t
        t += fr["dur"]
    return t


# ───────────────────────────── RENDER ─────────────────────────────
def player_html(spec, frames, total, capture):
    tpl = (TOOLS / "templates" / "player.html").read_text(encoding="utf-8")
    css = (TOOLS / "templates" / "player.css").read_text(encoding="utf-8")
    macros = (TOOLS / "katex_macros.json").read_text(encoding="utf-8")
    data = {"title": spec["title"], "total": total,
            "frames": [{k: f[k] for k in ("scene_title", "kind", "blocks", "active", "caption", "pause", "t0", "focus")}
                       for f in frames]}
    katex = KATEX_DIR.as_uri() if capture else Path(__import__("os").path.relpath(KATEX_DIR, out_dir(spec))).as_posix()
    kinds = json.dumps(kind_labels(profile_of(spec)), ensure_ascii=False)
    return (tpl.replace("{{CSS}}", css).replace("{{MACROS}}", macros).replace("{{KATEX}}", katex).replace("{{KINDS}}", kinds)
            .replace("{{SERIES}}", spec["series"]).replace("{{TITLE}}", spec["title"])
            .replace("{{DATA}}", json.dumps(data, ensure_ascii=False)))


def cmd_preview(spec):
    frames = build_frames(spec)
    total = timeline(spec, frames)
    p = out_dir(spec) / "preview.html"
    p.write_text(player_html(spec, frames, total, capture=False), encoding="utf-8")
    print(f"preview: {p}  ({len(frames)} khung, ≈{total/60:.1f} phút)")
    return 0


def cmd_render(spec):
    from playwright.sync_api import sync_playwright
    frames = build_frames(spec)
    total = timeline(spec, frames)
    d = out_dir(spec) / "frames"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    page_file = out_dir(spec) / "_capture.html"
    page_file.write_text(player_html(spec, frames, total, capture=True), encoding="utf-8")
    problems = []
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="msedge")
        except Exception:
            browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.add_init_script("window.__CAPTURE__ = true;")
        page.goto(page_file.as_uri())
        page.wait_for_function("document.fonts.status === 'loaded'")
        stage = page.locator("#stage")
        for i, fr in enumerate(frames):
            st = page.evaluate(f"window.renderFrame({i})")
            page.evaluate("document.fonts.ready")
            if st["errs"]:
                problems.append(f"khung {i} ({fr['scene_id']}): {st['errs']} lỗi KaTeX")
            if st["overflow"]:
                problems.append(f"khung {i} ({fr['scene_id']}): nội dung TRÀN bảng — tách step hoặc dùng `clear: true`")
            if st["capOverflow"]:
                problems.append(f"khung {i} ({fr['scene_id']}): phụ đề tràn: “{fr['caption'][:50]}…”")
            for s in st.get("layout") or []:
                # chồng phần / công thức tràn / viền nhấn đè chữ (player.html layoutIssues; quét cả khoá: audit/layout_scan.py)
                problems.append(f"khung {i} ({fr['scene_id']}): bố cục — {s}")
            if st.get("headWrap"):
                problems.append(f"khung {i} ({fr['scene_id']}): dòng đầu trang hoặc tiêu đề phân cảnh xuống 2 dòng, "
                                "đè lên bảng — rút gọn `title` của bài hoặc `title` của phân cảnh")
            if st["focusMiss"]:
                problems.append(f"khung {i} ({fr['scene_id']}): `focus` trỏ tới phần không có trên bảng {fr['focus']}: "
                                f"“{fr['caption'][:50]}…”")
            stage.screenshot(path=str(d / f"{i:05d}.png"))
        browser.close()
    for p in problems:
        print("[FAIL] render " + p)
    print(f"render: {len(frames)} khung → {d}  ({len(problems)} vấn đề)")
    print("checked_at=" + now())
    return 1 if problems else 0


# ───────────────────────────── BUILD ─────────────────────────────
def spec_digest(spec):
    """sha256 của các trường ẢNH HƯỞNG tới video (bỏ asr_reviewed và trường nội bộ) — sửa ghi chú xem xét không làm video STALE."""
    keep = {k: v for k, v in load_yaml(spec["_path"]).items() if k != "asr_reviewed"}
    return hashlib.sha256(json.dumps(keep, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def tts_digest(frames):
    """sha256 của đúng văn bản gửi TTS (đã qua lexicon) + giọng + tốc độ của mọi câu. Đổi lexicon làm audio cũ lỗi
    thời mà file đặc tả không đổi (lỗi thật L05: đổi cách đọc “gradient”, verify L04 vẫn PASS) — verify so cả dấu này."""
    rows = [[fr["tts"], fr["voice"], fr["rate"]] for fr in frames]
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode("utf-8")).hexdigest()


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def cmd_build(spec, skip_lint=False):
    if not skip_lint:
        r = lint(spec)
        if r.dump():
            print("build dừng: lint FAIL")
            return 1
    if cmd_tts(spec):
        return 1
    if cmd_render(spec):
        print("build dừng: render FAIL")
        return 1
    frames = build_frames(spec)
    total = timeline(spec, frames)
    od = out_dir(spec)
    ff = ffmpeg_exe()
    # audio: nối tất cả câu + khoảng lặng, mỗi đoạn dài đúng số frame -> không lệch tiếng/hình
    audio = od / "_audio.wav"
    with wave.open(str(audio), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(SR)
        for fr in frames:
            with wave.open(str(tts_key(fr))) as w:
                assert w.getframerate() == SR and w.getsampwidth() == 2 and w.getnchannels() == 1
                pcm = w.readframes(w.getnframes())
            need = round(fr["dur"] * SR) * 2
            pcm = pcm[:need] + b"\x00" * max(0, need - len(pcm))
            out.writeframes(pcm)
    concat = od / "_frames.txt"
    lines = []
    for i, fr in enumerate(frames):
        lines += [f"file 'frames/{i:05d}.png'", f"duration {fr['dur']:.6f}"]
    lines.append(f"file 'frames/{len(frames)-1:05d}.png'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    mp4 = od / f"{spec['id']}.mp4"
    cmd = [ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-i", str(audio),
           "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-crf", "20",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", str(mp4)]
    subprocess.run(cmd, check=True, cwd=str(od))
    audio.unlink(missing_ok=True)  # file trung gian ~40MB, tạo lại được
    # phụ đề + chương
    srt = []
    for i, fr in enumerate(frames, 1):
        srt.append(f"{i}\n{srt_time(fr['t0'])} --> {srt_time(fr['t0'] + fr['speech'])}\n{fr['caption']}\n")
    (od / f"{spec['id']}.srt").write_text("\n".join(srt), encoding="utf-8")
    chapters, seen = [], set()
    for fr in frames:
        if fr["scene"] not in seen:
            seen.add(fr["scene"])
            t = int(fr["t0"])
            chapters.append(f"{t//60:02d}:{t%60:02d} {fr['scene_title']}")
    (od / "chapters.txt").write_text("\n".join(chapters) + "\n", encoding="utf-8")
    report = {"id": spec["id"], "built_at": now(), "frames": len(frames), "timeline_seconds": round(total, 3),
              "spec_sha256": spec_digest(spec), "tts_sha256": tts_digest(frames), "mp4": str(mp4),
              # nguồn đọc từng câu (edge / azure / vieneu / piper; “edge?” = cache có từ trước khi ghi nguồn — mặc định edge)
              "tts_sources": {s: n for s in sorted({(tts_key(fr).with_suffix(".src").read_text(encoding="utf-8").strip()
                                                    if tts_key(fr).with_suffix(".src").exists() else "edge?") for fr in frames})
                              for n in [sum(1 for fr in frames if (tts_key(fr).with_suffix(".src").read_text(encoding="utf-8").strip()
                                                                    if tts_key(fr).with_suffix(".src").exists() else "edge?") == s)]},
              "voices": sorted({fr["voice"] for fr in frames})}
    (od / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"build: {mp4}  ({total/60:.1f} phút, {len(frames)} khung)")
    return cmd_verify(spec)


def cmd_verify(spec):
    od = out_dir(spec)
    mp4 = od / f"{spec['id']}.mp4"
    rep = json.loads((od / "build_report.json").read_text(encoding="utf-8")) if (od / "build_report.json").exists() else {}
    res = subprocess.run([ffmpeg_exe(), "-hide_banner", "-i", str(mp4)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = res.stderr
    fails = []
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None
    if dur is None:
        fails.append("không đọc được thời lượng mp4")
    if "Video: h264" not in info:
        fails.append("thiếu luồng video h264")
    if "Audio: aac" not in info:
        fails.append("thiếu luồng audio aac")
    if "1920x1080" not in info:
        fails.append("độ phân giải không phải 1920x1080")
    tl = rep.get("timeline_seconds")
    if dur is not None and tl is not None and abs(dur - tl) > 0.5:
        fails.append(f"thời lượng mp4 {dur:.2f}s lệch timeline {tl:.2f}s")
    spec_sha = spec_digest(spec)
    if rep.get("spec_sha256") != spec_sha:
        fails.append("video STALE: file đặc tả đã đổi sau lần build")
    if "tts_sha256" not in rep:
        fails.append("build_report thiếu tts_sha256 (build trước khi có kiểm tra lexicon) — build lại")
    elif rep["tts_sha256"] != tts_digest(build_frames(spec)):
        fails.append("video STALE: văn bản gửi TTS đã đổi (lexicon_vi.yaml hoặc giọng) sau lần build")
    # một bài một giọng: edge/azure là CÙNG giọng NamMinh; vieneu/piper là giọng khác — có cả hai nhóm là trộn giọng
    fam = {"edge": "ms", "edge?": "ms", "azure": "ms", "vieneu": "vieneu", "piper": "piper"}
    groups = {fam.get(s, s) for s in (rep.get("tts_sources") or {})}
    # hồ sơ language (luật target_language_voice): giọng bản ngữ ở step câu mẫu là CHỦ Ý, không phải trộn giọng — chỉ đếm giọng
    # của lời giảng (câu cùng ngôn ngữ với giọng của bài); giọng bản ngữ chỉ hợp lệ khi hồ sơ cho phép
    base = voice_lang(spec.get("voice"))
    frs = build_frames(spec)
    narr = {fr["voice"] for fr in frs if fr["lang"] == base}
    target = {fr["voice"] for fr in frs if fr["lang"] != base}
    if len(groups) > 1 or len(narr) > 1 or (target and "target_language_voice" not in profile_of(spec)["rules"]):
        fails.append(f"trộn giọng trong một bài: nguồn {rep.get('tts_sources')}, giọng {rep.get('voices')} — build lại bằng một giọng")
    for f in fails:
        print("[FAIL] verify " + f)
    print(f"verify: duration={dur}s timeline={tl}s streams={'h264' in info and 'aac' in info} → {'FAIL' if fails else 'PASS'}")
    print("checked_at=" + now())
    return 1 if fails else 0


# ───────────────────────────── ASR: máy nghe lại giọng đọc ─────────────────────────────
def load_audio_16k(path):
    """Giải mã bằng ffmpeg → float32 mono 16 kHz (tránh phụ thuộc PyAV, vốn lệch phiên bản với faster-whisper)."""
    import numpy as np
    raw = subprocess.run([ffmpeg_exe(), "-loglevel", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def missed_words(expected, heard):
    """Chỉ số các từ của `expected` không nằm trong khối khớp nào với `heard` (danh sách token đã chuẩn hoá)."""
    import difflib
    ok = set()
    for a, _, size in difflib.SequenceMatcher(None, expected, heard, autojunk=False).get_matching_blocks():
        ok.update(range(a, a + size))
    return {i for i in range(len(expected)) if i not in ok}


# ASR: GPU (CUDA, int8_float16) nếu có, không thì CPU int8. Đo 2026-10-30 trên RTX 2060 (audit/perf/asr_gpu_eq.py):
#   medium, câu 11,7 s ×2 lượt: CPU int8 23,1 s, GPU int8_float16 2,6 s. 120 câu ngẫu nhiên đã có bản chép CPU:
#   GPU giống hệt 77/120 (small), 95/120 (medium); tương đồng từ TB 0,983 / 0,991 — khác biệt kiểu giải mã (hai chiều),
#   không lệch hệ thống. Cache giữ khoá cũ (mô hình + băm wav): bản chép đã có — kể cả lý do HAND trích dẫn — không đổi;
#   câu mới ghi kèm tệp .dev nêu thiết bị đã nghe. Đổi bằng LV_ASR_DEVICE=auto|cuda|cpu.
ASR_DEVICE = os.environ.get("LV_ASR_DEVICE", "auto")


def _whisper_load(mname, prefer_gpu=True):
    """Trả (model, nhãn thiết bị). Lỗi thiếu cuBLAS/cuDNN chỉ lộ ra khi CHẠY → chạy thử 1 s im lặng trước khi nhận GPU."""
    from faster_whisper import WhisperModel
    import numpy as np
    if prefer_gpu and ASR_DEVICE in ("auto", "cuda"):
        try:
            import ctranslate2
            if ctranslate2.get_cuda_device_count() < 1:
                raise RuntimeError("không thấy GPU CUDA")
            m = WhisperModel(mname, device="cuda", compute_type="int8_float16")
            list(m.transcribe(np.zeros(16000, np.float32), language="vi")[0])
            return m, "cuda/int8_float16"
        except Exception as e:
            if ASR_DEVICE == "cuda":
                raise
            print(f"[WARN] ASR không chạy được trên GPU ({type(e).__name__}: {str(e)[:120]}) → dùng CPU", flush=True)
    return WhisperModel(mname, device="cpu", compute_type="int8"), "cpu/int8"


def cmd_asr(spec, model="small", threshold=0.8, recheck=None):
    """Nghe lại từng câu TTS bằng faster-whisper, so với lời kỳ vọng. Đây là bằng chứng GIÁN TIẾP về phát âm:
    câu bị gắn cờ phải được người/agent nghe hoặc xem xét; câu đã xem xét ghi vào `asr_reviewed` của bài."""
    import difflib
    sys.path.insert(0, str(TOOLS))
    from vi_text import normalize, canon_heard
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ENV ERROR: thiếu faster-whisper (pip install faster-whisper) → phát âm NOT_VERIFIED")
        return 2
    frames = build_frames(spec)
    acache = OUT / "_cache" / "asr"
    acache.mkdir(parents=True, exist_ok=True)
    models, used = {}, {}
    t_asr = time.time()
    reviewed = {str(x["sentence"]).strip(): x.get("reason", "") for x in spec.get("asr_reviewed") or []}

    EN_NUM = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                                 "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}

    def norm(text, lang):
        # tiếng Việt: đổi số → chữ (vi_text); ngôn ngữ khác: chữ thường, bỏ dấu câu; tiếng Anh: số đếm 0–20 viết bằng chữ → chữ số
        # (máy nghe chép “ten years” thành “10 years” — lỗi thật mẫu language 2026-10-31, không phải lỗi phát âm)
        if lang == "vi":
            return normalize(text)
        toks = re.findall(r"[^\W_]+", text.lower())
        return " ".join(EN_NUM.get(w, w) if lang == "en" else w for w in toks)

    def score(fr, wav, mname):
        lang = fr.get("lang", "vi")
        # khoá cache giữ nguyên cho tiếng Việt (không mất cache 476 bài); ngôn ngữ khác thêm mã ngôn ngữ
        key = acache / (f"{mname}_{hashlib.sha256(wav.read_bytes()).hexdigest()[:24]}.txt" if lang == "vi"
                        else f"{mname}_{lang}_{hashlib.sha256(wav.read_bytes()).hexdigest()[:24]}.txt")
        if key.exists():
            heard = key.read_text(encoding="utf-8")
            used["cache"] = used.get("cache", 0) + 1
        else:
            if mname not in models:
                models[mname] = _whisper_load(mname)
            audio = load_audio_16k(wav)
            try:
                segs, _ = models[mname][0].transcribe(audio, language=lang, beam_size=5, condition_on_previous_text=False)
                heard = " ".join(s.text.strip() for s in segs)
            except Exception as e:   # GPU hết bộ nhớ / lỗi driver giữa chừng → nạp lại trên CPU, nghe lại câu này
                if not models[mname][1].startswith("cuda"):
                    raise
                print(f"[WARN] ASR GPU lỗi ({type(e).__name__}: {str(e)[:120]}) → chuyển {mname} sang CPU", flush=True)
                models[mname] = _whisper_load(mname, prefer_gpu=False)
                segs, _ = models[mname][0].transcribe(audio, language=lang, beam_size=5, condition_on_previous_text=False)
                heard = " ".join(s.text.strip() for s in segs)
            key.write_text(heard, encoding="utf-8")
            key.with_suffix(".dev").write_text(models[mname][1], encoding="utf-8")
            used[models[mname][1]] = used.get(models[mname][1], 0) + 1
        best = None
        for ref in (fr["caption"], fr["tts"]):   # chấp nhận ASR viết theo chữ gốc hoặc theo cách đọc
            e = norm(ref, lang).split()
            h_ = canon_heard(norm(heard, lang).split(), e) if lang == "vi" else norm(heard, lang).split()
            ratio = difflib.SequenceMatcher(None, e, h_).ratio()
            if best is None or ratio > best[0]:
                best = (ratio, e, h_)
        ratio, e, h = best
        diff = [f"“{' '.join(e[a1:a2])}” → nghe thành “{' '.join(h[b1:b2])}”"
                for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, e, h).get_opcodes() if op != "equal"]
        # mức TỪ: so cách đọc (tts) với lời nghe được đã qua cùng lexicon (ASR viết “Vector” ↔ đọc “véc tơ”)
        e_tts = norm(fr["tts"], lang).split()
        miss = missed_words(e_tts, canon_heard(normalize(lexicon_apply(heard, course=course_of(spec))).split(), e_tts)
                            if lang == "vi" else norm(heard, lang).split())
        return round(ratio, 3), heard, diff, miss

    rows, missing = [], 0
    for i, fr in enumerate(frames):
        wav = tts_key(fr)
        if not wav.exists():
            missing += 1
            continue
        ratio, heard, diff, miss = score(fr, wav, model)
        row = {"frame": i, "ratio": ratio, "caption": fr["caption"], "heard": heard, "diff": diff,
               "reviewed": reviewed.get(fr["caption"].strip()), "both_missed": [], "both_missed_other": []}
        # Mô hình thứ hai nghe lại MỌI câu. Câu bị gắn cờ khi (a) cả hai mô hình đều khớp < ngưỡng, hoặc
        # (b) có TỪ RỦI RO mà cả hai mô hình đều nghe khác. (b) cần vì một từ đọc sai trong câu ~10 từ vẫn cho độ
        # khớp ≥ 0,8 (đối chứng 2026-10-22: “nghịch lý” thay “nghịch đảo” → medium 0,917). Từ rủi ro = nơi TTS thật
        # sự có thể đọc sai: từ do lexicon sinh ra, từ không phải âm tiết tiếng Việt, chữ cái đứng riêng (mọi lỗi
        # thật đã gặp: “hây ai”, “với đúc”, “vết to” đều thuộc nhóm này). Từ thuần Việt mà cả hai mô hình nghe khác
        # (thường là nhầm thanh: con/còn, một/mục) chỉ ghi tham khảo cho người nghe, không chặn.
        if recheck:
            r2, h2, d2, miss2 = score(fr, wav, recheck)
            tts_tok = norm(fr["tts"], fr.get("lang", "vi")).split()
            hits = []
            lexicon_apply(fr["caption"], hits, course_of(spec))
            lex_tok = {t for h in hits for t in normalize(h[2]).split()}
            # câu tiếng nước ngoài đọc bằng giọng bản ngữ: mọi từ đều “rủi ro” (người học bắt chước đúng từng từ)
            risk = set(range(len(tts_tok))) if fr.get("lang", "vi") != "vi" else \
                {k for k, t in enumerate(tts_tok) if len(t) == 1 or t in lex_tok or not is_vietnamese_syllable(t)}
            both = sorted(miss & miss2)
            row.update({"ratio_" + model: ratio, "ratio": max(ratio, r2), "heard_" + recheck: h2,
                        "both_missed": [tts_tok[k] for k in both if k in risk],
                        "both_missed_other": [tts_tok[k] for k in both if k not in risk]})
            if r2 > ratio:
                row.update({"heard": h2, "diff": d2})
        rows.append(row)
    flagged = [r_ for r_ in rows if r_["ratio"] < threshold or r_["both_missed"]]
    advisory = [r_ for r_ in rows if r_ not in flagged and r_["both_missed_other"]]
    open_ = [r_ for r_ in flagged if r_["reviewed"] is None]
    od = out_dir(spec)
    label = model + (f" + kiểm lại bằng {recheck}" if recheck else "")
    lines = [f"# ASR report {spec['id']} (model={label}, ngưỡng={threshold})", "",
             f"- câu: {len(rows)}, thiếu audio: {missing}, gắn cờ: {len(flagged)}, chưa xem xét: {len(open_)}",
             f"- gắn cờ khi độ khớp < {threshold}" + (f", hoặc có từ rủi ro (lexicon / từ ngoại / chữ cái) cả {model} và "
                                                       f"{recheck} đều nghe khác" if recheck else ""),
             f"- tham khảo (không chặn): {len(advisory)} câu có từ thuần Việt cả hai mô hình nghe khác",
             "- máy nghe: " + (", ".join(f"{k} {v} lượt" for k, v in sorted(used.items())) or "—"),
             f"- checked_at: {now()}", "",
             "| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro cả hai nghe khác | từ khác cả hai nghe khác | đã xem xét |",
             "|---|---|---|---|---|---|---|---|"]
    for r_ in sorted(flagged, key=lambda x: x["ratio"]):
        lines.append(f"| {r_['frame']} | {r_['ratio']} | {r_['caption']} | {r_['heard']} | {'; '.join(r_['diff'])} "
                     f"| {', '.join(r_['both_missed']) or '—'} | {', '.join(r_['both_missed_other']) or '—'} "
                     f"| {r_['reviewed'] or '—'} |")
    if advisory:
        lines += ["", "## Tham khảo cho người nghe: từ thuần Việt cả hai mô hình nghe khác (không chặn)", "",
                  "| khung | câu | từ | nghe được |", "|---|---|---|---|"]
        lines += [f"| {r_['frame']} | {r_['caption']} | {', '.join(r_['both_missed_other'])} | {r_['heard']} |"
                  for r_ in advisory]
    (od / "asr_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (od / "asr_report.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    mean = sum(r_["ratio"] for r_ in rows) / max(1, len(rows))
    for r_ in open_:
        both = f" | cả hai nghe khác: {', '.join(r_['both_missed'])}" if r_["both_missed"] else ""
        print(f"[FLAG] khung {r_['frame']} ({r_['ratio']}): {'; '.join(r_['diff'])[:160]}{both}")
    print(f"asr: {len(rows)} câu, độ khớp TB {mean:.3f}, gắn cờ {len(flagged)}, chưa xem xét {len(open_)}, tham khảo {len(advisory)} → {od / 'asr_report.md'}")
    print(f"asr: {time.time() - t_asr:.0f} s; máy nghe: " + (", ".join(f"{k} {v} lượt" for k, v in sorted(used.items())) or "—"))
    print("checked_at=" + now())
    return 1 if (open_ or missing) else 0


# ───────────────────────────── NEW / CURRICULUM ─────────────────────────────
def _course_series(course):
    """Tên chuỗi bài của khoá: lấy từ bài đã có (giữ đúng một kiểu), không có thì từ dòng đầu của lộ trình (“— KHOÁ · Tên”)."""
    for f in sorted((ROOT / "lessons" / course.lower()).glob("L*_*.yaml")):
        s = (load_yaml(f) or {}).get("series")
        if s:
            return str(s)
    cp = ROOT / "curriculum" / f"{course.lower()}.yaml"
    m = re.search(r"—\s*(\S+\s*·\s*.+)", cp.read_text(encoding="utf-8").splitlines()[0]) if cp.exists() else None
    return m.group(1).strip() if m else f"{course} · Tên khoá"


def cmd_new(path, lid, title, kind="lesson", profile=None):
    """Tạo đặc tả bài từ mẫu. Khoá lấy từ thư mục lessons/<khoá>/ (lỗi thật 2026-10-30: mẫu cũ ghi cứng chuỗi CS115, không có `course`)."""
    p = Path(path)
    if p.exists():
        print(f"đã tồn tại: {p} (không ghi đè)")
        return 1
    course = p.parent.name.upper() if p.parent.name.lower() != "lessons" else DEFAULT_COURSE
    prof = profile or profile_name({"course": course})
    if prof != DEFAULT_PROFILE and kind == "lesson":
        load_profile(prof)                                   # báo lỗi rõ nếu hồ sơ không có
        tpl = (TOOLS / "templates" / "profiles" / f"{prof}.yaml").read_text(encoding="utf-8")
        kind = f"lesson/{prof}"
    else:
        tpl_name = {"case": "case_lesson_template.yaml", "journey": "journey_lesson_template.yaml"}.get(kind, "lesson_template.yaml")
        tpl = (TOOLS / "templates" / tpl_name).read_text(encoding="utf-8")
    p.parent.mkdir(parents=True, exist_ok=True)
    out = (tpl.replace("__ID__", lid).replace("__TITLE__", title).replace("__COURSE_LC__", course.lower())
           .replace("__COURSE__", course).replace("__SERIES__", _course_series(course)))
    p.write_text(out, encoding="utf-8")
    print(f"tạo: {p} (khoá {course}, mẫu {kind})")
    return 0


def cmd_new_course(code, name, profile=DEFAULT_PROFILE):
    """Dựng khung một chuyên ngành mới: lộ trình, lớp phủ ký hiệu, lớp phủ phát âm, bộ kiểm độc lập, thư mục bài/dò phát âm.
    Không ghi đè tệp đã có. Quy trình đầy đủ: .claude/skills/lecture-video/references/new-domain.md"""
    C = code.upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]{1,5}", C):
        print(f"mã khoá “{code}” không hợp lệ (2–6 chữ in hoa/số, ví dụ GFX)")
        return 1
    if C.lower() in {"git"}:
        print("mã khoá trùng tên công cụ (Git) — chọn mã khác để người học không nhầm")
        return 1
    c, T = C.lower(), TOOLS / "templates"
    plan = [(T / "curriculum_template.yaml", ROOT / "curriculum" / f"{c}.yaml"),
            (T / "symbols_overlay.yaml", TOOLS / "registry" / f"symbols.{C}.yaml"),
            (T / "lexicon_overlay.yaml", TOOLS / "registry" / f"lexicon_vi.{C}.yaml"),
            (T / "verify_template.py", ROOT / "audit" / c / f"verify_{c}.py")]
    for src, dst in plan:
        if dst.exists():
            print(f"giữ nguyên (đã có): {dst.relative_to(ROOT)}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        body = src.read_text(encoding="utf-8").replace("__COURSE_LC__", c).replace("__COURSE__", C).replace("__NAME__", name)
        if dst.suffix == ".yaml" and dst.parent.name == "curriculum":
            load_profile(profile)                            # hồ sơ chuyên ngành của cả khoá (bài mới thừa hưởng)
            body = body.replace("course: " + C, f"course: {C}\nprofile: {profile}", 1)
        dst.write_text(body, encoding="utf-8")
        print(f"tạo: {dst.relative_to(ROOT)}")
    for d in (ROOT / "lessons" / c, ROOT / "audit" / c / "probes", ROOT / "audit" / c / "logs"):
        d.mkdir(parents=True, exist_ok=True)
    print(f"tiếp theo: soạn curriculum/{c}.yaml → mã VER trong audit/verify_plan_curricula.py → lv.py curriculum → "
          f"lv.py new lessons/{c}/L00_<slug>.yaml --id L00 --title \"…\"")
    return 0


def cmd_curriculum(path):
    cur = load_yaml(path)
    lessons = {l["id"]: l for l in cur["lessons"]}
    fails = []
    # đồ thị tiên quyết không chu trình + tham chiếu tồn tại
    state = {}

    def visit(n, stack):
        if state.get(n) == 1:
            fails.append(f"chu trình tiên quyết: {' -> '.join(stack + [n])}")
            return
        if state.get(n) == 2:
            return
        state[n] = 1
        for q in lessons[n].get("requires", []):
            if q not in lessons:
                fails.append(f"{n} requires `{q}` không tồn tại")
            else:
                visit(q, stack + [n])
        state[n] = 2
    for n in lessons:
        visit(n, [])
    order = [l["id"] for l in cur["lessons"]]
    # số hiệu = thứ tự học (L00, L01, … không trùng, không nhảy cóc) — người học nghe “bài 7” phải đúng là bài thứ 7
    if len(set(order)) != len(order):
        fails.append(f"số hiệu bị trùng: {sorted({x for x in order if order.count(x) > 1})}")
    for k, lid in enumerate(order):
        if lid != f"L{k:02d}":
            fails.append(f"số hiệu không tịnh tiến: vị trí {k} là {lid}, cần L{k:02d}")
    for l in cur["lessons"]:
        for q in l.get("requires", []):
            if q in order and order.index(q) > order.index(l["id"]):
                fails.append(f"{l['id']} đứng trước bài tiên quyết {q}")
    # không bỏ sót bài: mọi bài đứng trước bài cuối cùng đã có đặc tả cũng phải có đặc tả (lỗi thật 2026-10-24: L00 có
    # trong lộ trình nhưng chưa có bài, trong khi L01–L07 đã làm); `spec` phải trỏ tới file có thật, cùng `id`
    with_spec = [k for k, l in enumerate(cur["lessons"]) if l.get("spec")]
    for k, l in enumerate(cur["lessons"][:max(with_spec) + 1] if with_spec else []):
        if not l.get("spec"):
            fails.append(f"{l['id']} chưa có đặc tả (spec) dù các bài sau nó đã làm — bài bị bỏ sót")
            continue
        sp_ = ROOT / l["spec"]
        if not sp_.exists():
            fails.append(f"{l['id']}: spec `{l['spec']}` không tồn tại")
        elif load_yaml(sp_).get("id") != l["id"]:
            fails.append(f"{l['id']}: spec `{l['spec']}` có id `{load_yaml(sp_).get('id')}` khác lộ trình")
    # assumes của từng bài đã build phải được bài tiên quyết giới thiệu
    reg = registry(str(cur.get("course") or DEFAULT_COURSE))["symbols"]
    base = {s["id"] for s in reg if s.get("base")}
    intro = {}
    for l in cur["lessons"]:
        sp_ = ROOT / l["spec"] if l.get("spec") else None
        if sp_ and sp_.exists():
            spec = load_spec(sp_)
            intro[l["id"]] = {i for _, _, _, st in iter_steps(spec) for i in (st.get("introduces") or [])}

    def closure(n, seen=None):
        seen = seen or set()
        for q in lessons[n].get("requires", []):
            if q not in seen:
                seen.add(q); closure(q, seen)
        return seen

    # Ký hiệu do bài tiên quyết KHÁC KHOÁ dạy (requires_ext, lỗi thật OSY 2026-10-28: `sub`, `dots` dạy ở CS115, `shl` ở CSA —
    # trước đây phải khai tay assumes_external). Đi theo requires_ext, lấy bao đóng requires trong khoá đó, đệ quy qua khoá xa hơn.
    curs = {}
    for f in (ROOT / "curriculum").glob("*.yaml"):
        c = load_yaml(f)
        if isinstance(c, dict) and c.get("course"):
            curs[str(c["course"])] = {l["id"]: l for l in c.get("lessons") or []}

    def ext_intro(refs, seen):
        out = set()
        for ref in refs:
            c, _, lid = str(ref).partition(":")
            if (c, lid) in seen or lid not in curs.get(c, {}):
                continue
            stack = [lid]
            while stack:
                x = stack.pop()
                if (c, x) in seen or x not in curs[c]:
                    continue
                seen.add((c, x)); l = curs[c][x]
                if l.get("spec") and (ROOT / l["spec"]).exists():
                    out |= {i for _, _, _, st in iter_steps(load_spec(ROOT / l["spec"])) for i in (st.get("introduces") or [])}
                stack += list(l.get("requires") or [])
                out |= ext_intro(l.get("requires_ext") or [], seen)
        return out
    for lid, ids in intro.items():
        spec = load_spec(ROOT / lessons[lid]["spec"])
        refs = [r for q in closure(lid) | {lid} for r in (lessons[q].get("requires_ext") or [])]
        avail = base | set().union(*[intro.get(q, set()) for q in closure(lid)]) | set(lessons[lid].get("assumes_external", [])) \
            | ext_intro(refs, set())
        gap = set(spec.get("assumes") or []) - avail
        if gap:
            fails.append(f"{lid}: assumes {sorted(gap)} nhưng chưa bài tiên quyết nào giới thiệu")
    # tiên quyết khác khoá: requires_ext: ["CS115:L13", …] — khoá đó phải có lộ trình (trường `course`) và có bài đó
    others = {}
    for f in (ROOT / "curriculum").glob("*.yaml"):
        c = load_yaml(f)
        if isinstance(c, dict) and c.get("course"):
            others[str(c["course"])] = {l["id"]: l for l in c.get("lessons") or []}
    for l in cur["lessons"]:
        for ref in l.get("requires_ext") or []:
            c, _, lid = str(ref).partition(":")
            if c not in others:
                fails.append(f"{l['id']} requires_ext `{ref}`: không có lộ trình khoá {c}")
            elif lid not in others[c]:
                fails.append(f"{l['id']} requires_ext `{ref}`: khoá {c} không có bài {lid}")
    # mỗi bài kế hoạch phải có mục tiêu và ví dụ (giáo án dùng được để soạn đặc tả, không chỉ là tên bài)
    for l in cur["lessons"]:
        if cur.get("status") == "planned" and not (l.get("objectives") and l.get("example")):
            fails.append(f"{l['id']}: giáo án kế hoạch thiếu `objectives` hoặc `example`")
    for f in fails:
        print("[FAIL] " + f)
    built = sum(1 for l in cur["lessons"] if l.get("spec") and (ROOT / l["spec"]).exists())
    print(f"curriculum: {len(lessons)} bài, {built} đã có đặc tả, {len(fails)} lỗi")
    print("checked_at=" + now())
    return 1 if fails else 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["new", "new-course", "lint", "preview", "tts", "render", "build", "verify", "asr", "curriculum"])
    ap.add_argument("path", help="tệp đặc tả / lộ trình; với new-course là MÃ KHOÁ (ví dụ GFX)")
    ap.add_argument("--id"); ap.add_argument("--title", default="Tên bài")
    ap.add_argument("--kind", choices=["lesson", "case", "journey"], default="lesson",
                    help="new: mẫu bài thường, bài tình huống chuyên gia (sự cố), hay bài hành trình theo trục thời gian")
    ap.add_argument("--profile", default=None,
                    help=f"new / new-course: hồ sơ chuyên ngành ({', '.join(profiles_available())}); mặc định theo lộ trình, rồi stem")
    ap.add_argument("--model", default="small", help="mô hình faster-whisper cho lệnh asr")
    ap.add_argument("--recheck", default="medium", help="mô hình thứ hai kiểm lại câu bị gắn cờ ('' để tắt)")
    a = ap.parse_args()
    if a.cmd == "new":
        return cmd_new(a.path, a.id or "LXX", a.title, a.kind, a.profile)
    if a.cmd == "new-course":
        return cmd_new_course(a.path, a.title, a.profile or DEFAULT_PROFILE)
    if a.cmd == "curriculum":
        return cmd_curriculum(a.path)
    spec = load_spec(a.path)
    if a.cmd == "lint":
        return lint(spec).dump()
    if a.cmd == "asr":
        return cmd_asr(spec, model=a.model, recheck=a.recheck or None)
    return {"preview": cmd_preview, "tts": cmd_tts, "render": cmd_render, "build": cmd_build, "verify": cmd_verify}[a.cmd](spec)


if __name__ == "__main__":
    sys.exit(main())
