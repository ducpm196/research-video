"""Hạ tầng nâng DMS lên chuẩn AF2 (WP5, 2026-11-14). Mỗi bài có một tệp audit/dms/af2/lNN.py gọi `apply(...)`.

Bài DMS là YAML viết tay (L08, L16–L18 sinh từ mẫu audit/dms/src/*.tpl.yaml). `apply` KHÔNG sửa tại chỗ chồng lên chính nó: lần chạy đầu chép
bài (hoặc mẫu) gốc vào audit/dms/af2/base/, các lần sau luôn xuất phát từ bản gốc đó → chạy lại tệp lNN.py bao nhiêu lần cũng ra cùng kết quả.
Một lần `apply` làm: thêm `af2: true`, thay mục tiêu (nếu có), thêm `covers`, thêm cảnh mới (trước cảnh recap), thay chữ đúng-một-lần
(`repl`), ghi lab (labkit.write_lab; mong_doi.txt = ĐẦU RA THẬT của lời giải Python), và đồng bộ sổ screen_code DMS cho các khối mã mới.
Không chạy build/tts/asr/git."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "audit"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
from labkit import write_lab, out_html  # noqa: E402

BASE = HERE / "base"
LEDGER = ROOT / "audit" / "review" / "screen_code" / "DMS.yaml"
PY = sys.executable


class _D(yaml.SafeDumper):
    pass


def _str(d, s):
    if "\n" in s and not any(l != l.rstrip() for l in s.split("\n")):
        return d.represent_scalar("tag:yaml.org,2002:str", s, style="|")
    return d.represent_scalar("tag:yaml.org,2002:str", s)


_D.add_representer(str, _str)


def dump(obj):
    return yaml.dump(obj, Dumper=_D, allow_unicode=True, sort_keys=False, width=10 ** 6, default_flow_style=False)


def run_py(code, timeout=60):
    """chạy THẬT một đoạn Python (3.13 hệ thống, không phụ thuộc thư mục hiện tại); trả stdout đã bỏ dòng trắng cuối."""
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "chay.py"
        f.write_text(code.strip("\n") + "\n", encoding="utf-8", newline="\n")
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        p = subprocess.run([PY, "-B", str(f)], capture_output=True, text=True, encoding="utf-8", cwd=td, env=env, timeout=timeout)
    if p.returncode:
        raise SystemExit("mã lỗi:\n" + p.stderr)
    return "\n".join(l.rstrip() for l in p.stdout.replace("\r\n", "\n").split("\n")).strip("\n")


# ───────────────────────── dựng step / cảnh ─────────────────────────
def code_html(code):
    import html
    return '<div class="code">' + "".join(f"<div>{html.escape(l)}</div>" for l in code.strip("\n").split("\n")) + "</div>"


def run_html(code, out, label="Kết quả chạy thật"):
    return code_html(code) + f"<p><b>{label}</b></p>" + code_html(out)


def join_numbers(say):
    """lời đọc: số nhóm nghìn bằng dấu cách (“1 024”) máy đọc rời từng cụm → viết liền (“1024”); chỉ áp cho `say`"""
    return re.sub(r"(?<![\d,.])(\d{1,3})((?: \d{3})+)(?![\d])", lambda m: m.group(1) + m.group(2).replace(" ", ""), say)


def step(show, say, focus=None, clear=False, pause=None, introduces=None, forward_ref=False):
    say = join_numbers(say)
    d = {}
    if clear:
        d["clear"] = True
    d["show"] = show.strip("\n") + "\n"
    if focus is not None:
        d["focus"] = focus
    if introduces:
        d["introduces"] = introduces
    if pause:
        d["pause"] = pause
    if forward_ref:
        d["forward_ref"] = True
    d["say"] = say
    return d


def scene(sid, kind, title, steps, checks=None, lab=None):
    d = {"id": sid, "kind": kind, "title": title}
    if checks:
        d["checks"] = checks
    d["steps"] = steps
    if lab:
        d["lab"] = lab
    return d


def practice(lid, title, task_html, task_say, expected, filename, hint_html, hint_say, pause=120, focus1=None, focus3=None):
    """Cảnh Tự làm (E53): step 1 đề + pause; step 2 kết quả mong đợi (mọi dòng) + lệnh chấm; step 3 gợi ý."""
    import html
    cmd = f"bash labs/cham.sh DMS {lid} {filename}"
    s1 = step(task_html, task_say, focus=focus1, pause=pause)
    s2 = step(out_html(expected) + (f'<p class="note">Chấm bằng Git Bash: <code>{html.escape(cmd)}</code> — in <b>ĐÚNG</b> khi trùng.</p>'
                                    if filename else
                                    '<p class="note">Bài giấy bút: so từng dòng với <code>loi_giai.md</code> trong thư mục thực hành.</p>'),
              ("Đây là kết quả mong đợi. Bạn chạy chương trình của mình rồi so từng dòng với màn hình. Nếu muốn chấm bằng máy, dùng lệnh ở dưới màn hình; "
               "lệnh in chữ ĐÚNG khi đầu ra trùng, hoặc chỉ ra dòng nào khác.") if filename else
              ("Đây là đáp án để đối chiếu. Bài này làm bằng giấy bút, nên bạn so từng dòng của mình với lời giải trong thư mục thực hành, trong đó có cả cách tính."),
              focus=[2, 2, 3] if filename else [2, 3], clear=True)
    s3 = step(hint_html, hint_say, focus=focus3, clear=True)
    sc = scene("practice", "practice", title, [s1, s2, s3])
    sc["lab"] = f"labs/DMS/{lid}"
    return sc


def make_lab(lid, de_md, solution, ext="py", expected=None):
    """Ghi labs/DMS/<lid>; với .py thì mong_doi.txt = đầu ra thật của lời giải."""
    if ext == "py":
        expected = run_py(solution)
    assert expected, "bài giấy bút phải truyền expected"
    write_lab("DMS", lid, de_md, ext, solution, expected)
    return expected


# ───────────────────────── sửa bài ─────────────────────────
LEDGER_CRLF = True


def _write(path, text, crlf):
    """ghi giữ đúng kiểu xuống dòng của tệp gốc (kho có tệp CRLF)"""
    text = text.replace("\r\n", "\n")
    if crlf:
        text = text.replace("\n", "\r\n")
    Path(path).write_bytes(text.encode("utf-8"))


def _paths(lid):
    d = ROOT / "lessons" / "dms"
    f = next(d.glob(f"{lid}_*.yaml"))
    tpl = next((HERE.parent / "src").glob(f"{lid}_*.tpl.yaml"), None)
    return f, tpl


CURRICULUM = ROOT / "curriculum" / "dms.yaml"
PYT_EXT = '["PYT:L00", "PYT:L01", "PYT:L02", "PYT:L03"]'


def cur_set(lid, objectives=None, requires_ext=PYT_EXT):
    """đồng bộ curriculum/dms.yaml: mục tiêu của bài + requires_ext (Python cơ bản cho cảnh quy mô/lab); giữ CRLF"""
    raw = CURRICULUM.read_bytes()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(f"  - id: {lid}"))
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("  - id:")), len(lines))
    if objectives is not None:
        k = next(k for k in range(i, j) if lines[k].startswith("    objectives:"))
        lines[k] = "    objectives: [" + ", ".join(json.dumps(o, ensure_ascii=False) for o in objectives) + "]"
    if requires_ext and not any(lines[k].startswith("    requires_ext:") for k in range(i, j)):
        k = next(k for k in range(i, j) if lines[k].startswith("    requires:"))
        lines.insert(k + 1, "    requires_ext: " + requires_ext)
    _write(CURRICULUM, "\n".join(lines), crlf)


def apply(lid, objectives=None, covers=None, scenes=(), repl=(), header_repl=(), assumes_add=(), requires_ext=None, drop_asr=(), quiz_pause=None):
    f, tpl = _paths(lid)
    target = tpl or f
    BASE.mkdir(exist_ok=True)
    b = BASE / target.name
    if not b.exists():
        shutil.copyfile(target, b)
    t = b.read_text(encoding="utf-8")
    lines = t.split("\n")
    if "af2: true" not in t:
        i = next(k for k, l in enumerate(lines) if l.startswith("depth: full"))
        lines.insert(i + 1, "af2: true")
    # mục tiêu
    if objectives is not None:
        i = next(k for k, l in enumerate(lines) if l.startswith("objectives:"))
        j = i + 1
        while j < len(lines) and (lines[j].startswith("  -") or lines[j].startswith("   ")):
            j += 1
        lines[i + 1:j] = ["  - " + json.dumps(o, ensure_ascii=False) for o in objectives]
    t = "\n".join(lines)
    # covers: ngay sau khối objectives
    if covers:
        lines = t.split("\n")
        i = next(k for k, l in enumerate(lines) if l.startswith("objectives:"))
        j = i + 1
        while j < len(lines) and (lines[j].startswith("  -") or lines[j].startswith("   ")):
            j += 1
        blk = ["covers:"] + [f"  - {{objective: {n}, scene: {s}}}" for n, s in covers]
        lines[j:j] = blk
        t = "\n".join(lines)
    for old, new in header_repl:
        assert t.count(old) == 1, f"{lid}: chữ cần thay phải có đúng 1 lần ({t.count(old)}): {old[:70]}"
        t = t.replace(old, new)
    # cảnh mới: mặc định trước recap; (cảnh, "id") = trước cảnh có id đó (kể cả dòng chú thích tiêu đề của nó)
    for item in scenes:
        sc_, before = item if isinstance(item, tuple) else (item, "recap")
        lines = t.split("\n")
        i = next(k for k, l in enumerate(lines) if l.startswith(f"  - id: {before}"))
        while i > 0 and (lines[i - 1].startswith("  #") or lines[i - 1].strip() == ""):
            i -= 1
        txt = dump([sc_]).rstrip("\n")
        ins = [("  " + l) if l else l for l in txt.split("\n")] + [""]
        lines[i:i] = ins
        t = "\n".join(lines)
    for old, new in repl:
        assert t.count(old) == 1, f"{lid}: chữ cần thay phải có đúng 1 lần ({t.count(old)}): {old[:70]}"
        t = t.replace(old, new)
    for pre in drop_asr:   # câu `asr_reviewed` không còn trong bài (lint E30)
        ls = t.split("\n")
        keep = [l for l in ls if not l.startswith('  - {sentence: "' + pre)]
        assert len(keep) < len(ls), f"{lid}: không có mục asr_reviewed bắt đầu bằng {pre!r}"
        t = "\n".join(keep)
    for a in assumes_add:
        m = re.search(r"^assumes: \[(.*)\]$", t, re.M)
        assert m, f"{lid}: không có dòng assumes dạng [..]"
        ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
        if a not in ids:
            ids.append(a)
        t = t[:m.start()] + "assumes: [" + ", ".join(ids) + "]" + t[m.end():]
    if quiz_pause:   # thời gian dừng của cảnh quiz (reader B: 8–10 giây là quá ngắn cho hai câu có 3–4 bước tính)
        ls = t.split("\n")
        i0 = next((k for k, l in enumerate(ls) if l.startswith("  - id: quiz")), None)
        if i0 is not None:
            i1 = next((k for k in range(i0 + 1, len(ls)) if ls[k].startswith("  - id:")), len(ls))
            for k in range(i0, i1):
                ls[k] = re.sub(r"(\bpause: )\d+", lambda m: m.group(1) + str(quiz_pause), ls[k])
            t = "\n".join(ls)
    assert "\x08" not in t, "byte \\x08 trong bài (lỗi thoát chuỗi)"
    _write(target, t, crlf=b"\r\n" in b.read_bytes())
    cur_set(lid, objectives, requires_ext if requires_ext is not None else PYT_EXT)
    if tpl:
        figs = [a for a in re.findall(r"\{\{([A-Z_]+)\}\}", t)]
        return f, tpl, figs
    return f, None, []


# ───────────────────────── sổ screen_code ─────────────────────────
def ledger_sync(lid, claims=None, sids=("quymo", "practice")):
    """Khối mã mới của cảnh quymo/…: [mã (run) → kết quả (output of mã)]; khối của cảnh practice: output của nguồn lab.
    claims: {sid: 'điều bài nói về kết quả'}. Chỉ thêm/ghi đè mục của khối mà bài hiện có."""
    import screen_code as sc
    f, _ = _paths(lid)
    _, blocks = sc.blocks_of(f)
    led = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
    global LEDGER_CRLF
    LEDGER_CRLF = b"\r\n" in LEDGER.read_bytes()
    blk, srcs = led.get("blocks") or {}, led.get("sources") or {}
    lab = ROOT / "labs" / "DMS" / lid
    by_step = {}
    for sid, ti, bi, text in blocks:
        by_step.setdefault((sid, ti), []).append((bi, text))
    new = {}
    for (sid, ti), items in by_step.items():
        if sid not in sids:
            continue
        if sid == "practice":
            sol = next(lab.glob("loi_giai.py"), None)
            if sol is None:
                continue
            name = f"{lid}_lab"
            exp = (lab / "mong_doi.txt").read_text(encoding="utf-8").strip("\n")
            srcs[name] = {"lang": "python", "reason": f"lời giải của lab labs/DMS/{lid} (loi_giai.py), chạy nguyên văn; đầu ra = mong_doi.txt = chữ hiện trên màn hình",
                          "code": sol.read_text(encoding="utf-8"), "expect_stdout": exp}
            for bi, text in items:
                new[f"DMS {lid} {sid} {ti} {bi}"] = {"sha": sc.digest(text), "kind": "output", "of": f"src:DMS:{name}",
                                                        "reason": "khối kết quả mong đợi của cảnh Tự làm (đầu ra thật của lời giải lab)"}
            continue
        if f"DMS {lid} {sid} {ti} 0" in blk and blk[f"DMS {lid} {sid} {ti} 0"].get("hand"):
            continue
        items.sort()
        if len(items) % 2:
            raise SystemExit(f"{lid} {sid} step {ti}: số khối mã lẻ ({len(items)}) — cần cặp (mã, kết quả)")
        for k in range(0, len(items), 2):
            (b0, t0), (b1, t1) = items[k], items[k + 1]
            key0 = f"DMS {lid} {sid} {ti} {b0}"
            out = run_py(t0)
            cl = (claims or {}).get(sid)
            e0 = {"sha": sc.digest(t0), "kind": "run", "lang": "python", "expect_stdout": out}
            if cl:
                e0["claims"] = [cl]
            new[key0] = e0
            new[f"DMS {lid} {sid} {ti} {b1}"] = {"sha": sc.digest(t1), "kind": "output", "of": key0,
                                                    "reason": "khối kết quả chạy thật của khối mã ngay trước"}
    blk.update(new)
    # bỏ mục mồ côi của chính bài này (khối đã bị xoá khỏi bài)
    live = {f"DMS {lid} {sid} {ti} {bi}" for sid, ti, bi, _ in blocks}
    for k in [k for k in blk if k.startswith(f"DMS {lid} ") and k not in live and k.split()[2] in sids]:
        del blk[k]
    head = []
    for l in LEDGER.read_text(encoding="utf-8").split("\n"):
        if l.startswith("#"):
            head.append(l)
        else:
            break
    led["blocks"], led["sources"] = blk, srcs
    _write(LEDGER, "\n".join(head) + "\n" + yaml.safe_dump(led, allow_unicode=True, width=10 ** 6, sort_keys=False), crlf=LEDGER_CRLF)
    return sorted(new)


def fill(lid, mapping):
    """bài sinh từ mẫu: ghép mẫu (đã vá) + hình sinh bằng máy → lessons/dms/<bài> (như audit/cs112/fill_tpl.py); giữ CRLF của mẫu"""
    f, tpl = _paths(lid)
    raw = tpl.read_bytes()
    t = raw.decode("utf-8").replace("\r\n", "\n")
    for k, p in mapping.items():
        svg = (ROOT / p).read_text(encoding="utf-8").strip()
        assert "\n" not in svg and ("{{" + k + "}}") in t, k
        t = t.replace("{{" + k + "}}", svg)
    assert "{{" not in t, "còn chỗ chưa điền"
    _write(f, t, crlf=b"\r\n" in raw)
    return f
