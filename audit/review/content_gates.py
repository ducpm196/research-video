"""11 cổng nội dung FAIL + 1 cổng WARN chuẩn AF5 (WP-1, plan_AF5_20261123T0110Z.md mục 6 WP-1).

Dùng:
  .venv/Scripts/python -B audit/review/content_gates.py [--root DIR] [--tsv OUT.tsv] [--ratchet BASELINE.tsv] [--run-cham] [KHOÁ ...]
Mã thoát:
  0 nếu không vi phạm (hoặc trong chế độ --ratchet: không phát sinh FAIL mới và khoá ĐÃ CHỐT không còn FAIL).
  1 nếu có vi phạm.
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = "bash"

FAIL_GATES = (
    "G-PRACTICE",
    "G-LEAK-DE",
    "G-ANTI-PRINT",
    "G-LABLANG",
    "G-COVERS",
    "G-LEN",
    "G-PAD",
    "G-BOILER",
    "G-CHECKS",
    "G-SCORE",
    "G-CODETABLE",
)

PYT_REQ_PATTERNS = (
    (re.compile(r"\bopen\s*\("), "PYT:L05"),
    (re.compile(r"^\s*class\s+\w+", re.M), "PYT:L06"),
    (re.compile(r"^\s*(?:try|raise)\b", re.M), "PYT:L07"),
    (re.compile(r"\b(?:import|from)\s+numpy\b"), "PYT:L09"),
    (re.compile(r"\b(?:import|from)\s+pandas\b"), "PYT:L10"),
    (re.compile(r"\b(?:import|from)\s+matplotlib\b"), "PYT:L11"),
)

DO_VERBS = (
    "viết", "tính", "cài", "dựng", "chạy", "dùng", "lập", "vẽ", "tạo", "chứng minh",
    "giải", "tìm", "mô phỏng", "đếm", "đọc", "đo", "phân tích", "chuyển", "thiết kế",
    "kiểm", "sửa", "so sánh", "chọn", "tách", "gắn", "chia",
)

STOPWORDS = {
    "và", "của", "cho", "với", "trong", "bằng", "từ", "đến", "tới", "về", "khi", "nếu",
    "một", "hai", "ba", "bốn", "năm", "các", "những", "này", "đó", "cùng", "để", "theo",
    "trên", "dưới", "qua", "ra", "vào", "lại", "không", "có", "được", "làm", "nêu", "hiểu",
    "biết", "giải", "thích", "viết", "tính", "dùng", "chạy", "đọc", "so", "sánh", "nhận",
    "phân", "biệt", "mô", "tả", "kiểm", "tra", "tự", "trước", "sau", "hơn", "nhiều", "ít",
    "bài", "cảnh", "hệ", "thống", "dữ", "liệu", "chương", "trình", "máy", "người", "học",
    "kết", "quả", "giá", "trị", "thực", "hiện", "cách", "đúng", "sai", "mới", "cũ",
    "điểm", "mức", "lần", "chọn", "bảng", "tổng", "chuẩn", "tế", "đầu", "cuối", "số",
    "câu", "dòng", "cột", "hàng", "lớn", "nhỏ", "cao", "thấp", "thêm", "bớt", "khiến",
}

TAUTOLOGY_CHECKS = {
    "1 + 1 == 2",
    "1+1==2",
    "127 != 0",
    "127!=0",
    "1.0 / (1.0 + 1.0) == 0.5",
    "1e-12 < 1e-9",
    "100 + 100 == 200",
    "127 + 1 == 128",
}


def strip_tags(s: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", s or "")
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def load_deny(root: Path) -> list[str]:
    for cand in (root / "audit" / "review" / "boiler_deny.txt", root / "boiler_deny.txt", DEFAULT_ROOT / "audit" / "review" / "boiler_deny.txt"):
        if cand.is_file():
            return [l.strip() for l in cand.read_text(encoding="utf-8").splitlines() if l.strip() and not l.strip().startswith("#")]
    return []


def load_curricula(root: Path) -> tuple[dict[str, dict], dict[str, dict[str, dict]]]:
    out = {}
    by_id = {}
    cur_dir = root / "curriculum"
    if not cur_dir.is_dir():
        return out, by_id
    for p in sorted(cur_dir.glob("*.yaml")):
        if p.name == "tracks.yaml":
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        if isinstance(d, dict) and d.get("course"):
            c = str(d["course"]).upper()
            out[c] = d
            by_id[c] = {str(l["id"]): l for l in (d.get("lessons") or [])}
    return out, by_id


def lesson_closure(cur_map: dict[str, dict], by_id: dict[str, dict[str, dict]], cache: dict, course: str, lid: str) -> set[str]:
    key = (course, lid)
    if key in cache:
        return cache[key]
    seen = set()
    stack = [f"{course}:{lid}"]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        c, _, l = node.partition(":")
        meta = by_id.get(c, {}).get(l)
        if not meta:
            continue
        for req in meta.get("requires") or []:
            stack.append(f"{c}:{req}")
        for req_e in meta.get("requires_ext") or []:
            stack.append(str(req_e))
        lab_req = (cur_map.get(c, {}).get("lab") or {}).get("requires") or []
        for lr in lab_req:
            stack.append(str(lr))
    cache[key] = seen
    return seen


def find_lab_dir(root: Path, course: str, lid: str, spec: dict) -> Path | None:
    for sc in spec.get("scenes") or []:
        if sc.get("kind") == "practice" and sc.get("lab"):
            p = root / str(sc["lab"]).strip().strip("/")
            if p.is_dir():
                return p
    cand = root / "labs" / course / lid
    return cand if cand.is_dir() else None


def check_g_practice(root: Path, course: str, lid: str, spec: dict, lab_d: Path | None) -> list[str]:
    prs = [sc for sc in (spec.get("scenes") or []) if sc.get("kind") == "practice"]
    if not prs:
        return ["thiếu cảnh practice"]
    errs = []
    for sc in prs:
        steps = sc.get("steps") or []
        if len(steps) < 3:
            errs.append(f"{sc.get('id')}: chỉ có {len(steps)} bước (< 3, thiếu gợi ý hoặc cấu trúc chuẩn)")
        if not any(st.get("pause") for st in steps):
            errs.append(f"{sc.get('id')}: thiếu bước pause")
        if steps:
            sh0 = strip_tags(str(steps[0].get("show") or ""))
            sh0_low = sh0.lower()
            if ("hướng dẫn tự làm" in sh0_low and "mở " in sh0_low) or (
                re.search(r"mở\s+(?:đề\s+tại\s+)?labs/", sh0_low) and len(sh0) < 180
            ):
                errs.append(f"{sc.get('id')}: bước 0 chỉ dẫn mở de.md, thiếu đề/dữ liệu trên màn hình")
        if lab_d and (lab_d / "mong_doi.txt").is_file():
            all_show = " ".join(strip_tags(str(st.get("show") or "")) for st in steps)
            wants = [l.strip() for l in (lab_d / "mong_doi.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
            if wants and not all(re.sub(r"\s+", " ", w) in all_show for w in wants):
                errs.append(f"{sc.get('id')}: chưa hiện đủ mong_doi.txt trên màn hình")
            sols = sorted(lab_d.glob("loi_giai.*"))
            if sols and sols[0].suffix != ".md":
                sol_lines = [l.strip() for l in sols[0].read_text(encoding="utf-8", errors="replace").splitlines()
                             if l.strip() and not l.strip().startswith(("#", "//", "--", "/*", "*"))]
                if len(sol_lines) >= 3:
                    hits = sum(1 for ln in sol_lines if re.sub(r"\s+", " ", ln) in all_show)
                    if hits == len(sol_lines):
                        errs.append(f"{sc.get('id')}: chiếu nguyên văn toàn bộ {sols[0].name} trong video")
    return errs


def check_g_leak_de(lab_d: Path | None) -> list[str]:
    if not lab_d or not (lab_d / "de.md").is_file() or not (lab_d / "mong_doi.txt").is_file():
        return []
    de_norm = re.sub(r"\s+", " ", (lab_d / "de.md").read_text(encoding="utf-8", errors="replace")).strip()
    wants = [re.sub(r"\s+", " ", l).strip() for l in (lab_d / "mong_doi.txt").read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    if wants and all(w in de_norm for w in wants):
        return [f"de.md lộ nguyên văn cả {len(wants)} dòng mong_doi.txt"]
    return []


def check_g_anti_print(root: Path, course: str, lid: str, lab_d: Path | None, contract: dict, run_cham: bool) -> list[str]:
    entry = contract.get(f"{course}/{lid}")
    if not entry:
        return ["thiếu mục trong labs/CONTRACT.yaml"] if contract else []
    ca_them = str(entry.get("ca_them") or "")
    if not ca_them.startswith("bat_buoc"):
        return []
    if not lab_d:
        return ["thiếu thư mục lab"]
    ca_dir = lab_d / "ca_an"
    has_hidden = (
        (ca_dir.is_dir() and (
            any(ca_dir.glob("*.in")) or any(ca_dir.glob("in_*.txt")) or any(ca_dir.glob("seed_*.sql")) or (ca_dir / "ham.json").is_file()
        ))
        or (lab_d / "kiem").is_dir()
    )
    if not has_hidden:
        return ["ca_them=bat_buoc nhưng chưa có ca_an/ hoặc kiem/"]
    if run_cham and (lab_d / "mong_doi.txt").is_file():
        sols = sorted(lab_d.glob("loi_giai.*"))
        if sols and sols[0].suffix in (".py", ".js", ".sh", ".c", ".java"):
            lines = (lab_d / "mong_doi.txt").read_text(encoding="utf-8").rstrip("\n").splitlines()
            tmp = Path(tempfile.mkdtemp())
            try:
                ext = sols[0].suffix
                hc = tmp / f"hc{ext}"
                if ext == ".py":
                    hc.write_text("for x in " + repr(lines) + ": print(x)\n", encoding="utf-8", newline="\n")
                elif ext == ".js":
                    hc.write_text("for (const x of " + repr(lines) + ") console.log(x);\n", encoding="utf-8", newline="\n")
                elif ext == ".sh":
                    hc.write_text("\n".join(f"echo '{l}'" for l in lines) + "\n", encoding="utf-8", newline="\n")
                cham_sh = root / "labs" / "cham.sh"
                if not cham_sh.is_file():
                    cham_sh = DEFAULT_ROOT / "labs" / "cham.sh"
                p = subprocess.run([BASH, str(cham_sh), str(lab_d), str(hc)], capture_output=True, text=True, timeout=30)
                if p.returncode == 0:
                    return ["tệp in cứng mong_doi.txt vẫn PASS qua cham.sh"]
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    return []


def check_g_lablang(cur_map: dict[str, dict], by_id: dict, closure_cache: dict, course: str, lid: str, lab_d: Path | None) -> list[str]:
    cur = cur_map.get(course)
    if not cur or not lab_d:
        return []
    lab_cfg = cur.get("lab") or {}
    allowed_langs = set(lab_cfg.get("lang") or [])
    if (lab_d / "loi_giai").is_dir():
        ext = "mvn" if (lab_d / "loi_giai" / "pom.xml").is_file() else "py"
        if allowed_langs and ext not in allowed_langs and "java" not in allowed_langs:
            return [f"du_an ({ext}) không thuộc lab.lang={sorted(allowed_langs)}"]
        return []
    sols = sorted(lab_d.glob("loi_giai.*"))
    if not sols:
        return []
    ext = sols[0].suffix.lstrip(".").lower()
    if allowed_langs and ext not in allowed_langs:
        return [f"loi_giai.{ext} không thuộc lab.lang={sorted(allowed_langs)}"]
    if ext == "py":
        # PYT L08 teaches venv + pip install and checks .__version__ of installed packages
        if course == "PYT" and lid == "L08":
            return []
        code = sols[0].read_text(encoding="utf-8", errors="replace")
        clos = lesson_closure(cur_map, by_id, closure_cache, course, lid)
        errs = []
        for rx, req in PYT_REQ_PATTERNS:
            if rx.search(code) and req not in clos:
                errs.append(f"loi_giai.py dùng cú pháp cần {req} nhưng chưa có trong bao đóng tiên quyết")
        return errs
    return []


def _keywords(text: str) -> set[str]:
    toks = re.findall(r"[^\W_]{3,}", text.lower())
    return {t for t in toks if t not in STOPWORDS and not t.isdigit()}


def check_g_covers(spec: dict, practice_errs: list[str], boiler_hits: list[str]) -> list[str]:
    objs = spec.get("objectives") or []
    covers = spec.get("covers") or []
    if not covers:
        return ["thiếu covers"]
    scs = {str(s.get("id")): s for s in (spec.get("scenes") or [])}
    errs = []
    for c in covers:
        oi, sid = c.get("objective"), str(c.get("scene"))
        if not isinstance(oi, int) or not 1 <= oi <= len(objs):
            errs.append(f"objective {oi} ngoài phạm vi")
            continue
        sc = scs.get(sid)
        if not sc:
            errs.append(f"mục tiêu {oi} trỏ tới cảnh '{sid}' không tồn tại")
            continue
        kind = sc.get("kind")
        if kind == "hook":
            errs.append(f"mục tiêu {oi} trỏ vào cảnh hook")
            continue
        if kind == "practice" and (practice_errs or boiler_hits):
            errs.append(f"mục tiêu {oi} trỏ vào cảnh Tự làm còn lỗi/khuôn mẫu")
            continue
        obj_s = str(objs[oi - 1]).strip()
        obj_low = obj_s.lower()
        shows = " ".join(str(st.get("show") or "") for st in sc.get("steps") or [])
        says = " ".join(str(st.get("say") or "") for st in sc.get("steps") or [])
        scene_txt = strip_tags(str(sc.get("title") or "") + " " + shows + " " + says)
        has_code = bool(re.search(r'class=["\']code["\']|<pre|\$\$', shows))
        has_num = bool(re.search(r"\d", strip_tags(shows)))
        if obj_low.startswith(DO_VERBS) and not obj_low.startswith("giải thích") and not (has_code or has_num):
            errs.append(f"mục tiêu {oi} (LÀM) trỏ '{sid}' không có mã hay phép tính")
        kw_obj = _keywords(obj_s)
        kw_sc = _keywords(scene_txt)
        need_hit = 2 if len(kw_obj) >= 3 else 1
        if kw_obj and len(kw_obj & kw_sc) < need_hit:
            errs.append(f"mục tiêu {oi} ít/không trùng từ khoá chủ đề với cảnh '{sid}'")
    return errs


def check_g_len(root: Path, course: str, lid: str, spec: dict, ignore_duration: bool = False) -> tuple[list[str], list[str]]:
    words = sum(len(str(st.get("say") or "").split()) for sc in (spec.get("scenes") or []) for st in (sc.get("steps") or []))
    pauses = sum(int(st.get("pause") or 0) for sc in (spec.get("scenes") or []) for st in (sc.get("steps") or []))
    errs, warns = [], []
    if words < 1300:
        errs.append(f"lời đọc {words} từ (< 1300)")
    br = root / "out" / course / lid / "build_report.json"
    if not ignore_duration and br.is_file():
        sec = float(json.loads(br.read_text(encoding="utf-8")).get("timeline_seconds") or 0)
        no_pause_min = (sec - pauses) / 60.0
        if no_pause_min < 9.0:
            errs.append(f"thời lượng không pause {no_pause_min:.2f} phút (< 9.0)")
    is_journey = spec.get("kind") == "journey" or spec.get("case") == "journey"
    if words > 2300 and not is_journey:
        warns.append(f"lời đọc {words} từ (> 2300)")
    if pauses > 300:
        warns.append(f"tổng pause {pauses} s (> 300)")
    return errs, warns


def check_g_pad(spec: dict) -> list[str]:
    errs = []
    tot_w = 0
    recap_w = 0
    for sc in spec.get("scenes") or []:
        sid = str(sc.get("id") or "")
        is_recap = sc.get("kind") == "recap"
        for i, st in enumerate(sc.get("steps") or []):
            w = len(str(st.get("say") or "").split())
            tot_w += w
            if is_recap:
                recap_w += w
            if not st.get("focus") and w > 120:
                errs.append(f"{sid}[{i}]: {w} từ (> 120) không đổi focus")
    if tot_w > 0 and (recap_w / tot_w) > 0.25:
        errs.append(f"recap chiếm {recap_w * 100 / tot_w:.1f}% lời đọc (> 25%)")
    return errs


def check_g_boiler(spec: dict, deny_list: list[str]) -> list[str]:
    blob = "\n".join(
        str(st.get("say") or "") + "\n" + str(st.get("show") or "")
        for sc in (spec.get("scenes") or [])
        for st in (sc.get("steps") or [])
    )
    hits = [d for d in deny_list if d in blob]
    return hits


def _norm_nums(text: str) -> set[str]:
    t = re.sub(r"(?<=\d)\s+(?=\d{3}\b)", "", text)
    t = re.sub(r"(?<=\d),(?=\d)", ".", t)
    nums = set(re.findall(r"\d+(?:\.\d+)?", t))
    for k in list(nums):
        if "." in k and k.endswith("0"):
            nums.add(k.rstrip("0").rstrip("."))
    return nums


def check_g_checks(spec: dict) -> list[str]:
    errs = []
    lesson_blob = " ".join(
        str(sc.get("title") or "") + " " + str(st.get("say") or "") + " " + strip_tags(str(st.get("show") or ""))
        for sc in (spec.get("scenes") or [])
        for st in (sc.get("steps") or [])
    )
    lesson_nums = _norm_nums(lesson_blob)
    for sc in spec.get("scenes") or []:
        sid = str(sc.get("id") or "")
        sc_text = strip_tags(
            str(sc.get("title") or "") + " " + " ".join(
                str(st.get("say") or "") + " " + str(st.get("show") or "")
                for st in (sc.get("steps") or [])
            )
        )
        sc_nums = _norm_nums(sc_text) | lesson_nums
        chks = list(sc.get("checks") or []) + [c for st in (sc.get("steps") or []) for c in (st.get("checks") or [])]
        for expr in chks:
            es = str(expr).strip()
            if es in TAUTOLOGY_CHECKS:
                errs.append(f"{sid}: check hằng đẳng thức '{es}'")
                continue
            if "alg." in es:
                continue
            nums = set(re.findall(r"\d+(?:\.\d+)?", es))
            if nums and not (nums & sc_nums):
                errs.append(f"{sid}: check '{es[:50]}' không dùng giá trị nào trong bài")
    return errs


def check_g_score(root: Path, spec: dict, lab_d: Path | None) -> list[str]:
    errs = []
    minus_rx = re.compile(r"\(-\d+đ\)")
    rubric_rx = re.compile(r"(?:thang|chấm|được)\s+\S+\s+điểm", re.I)
    for sc in spec.get("scenes") or []:
        is_pr = sc.get("kind") == "practice"
        for i, st in enumerate(sc.get("steps") or []):
            t = str(st.get("say") or "") + " " + strip_tags(str(st.get("show") or ""))
            if minus_rx.search(t) or (is_pr and rubric_rx.search(t)):
                errs.append(f"{sc.get('id')}[{i}]: chứa chữ chấm điểm giả")
    if lab_d and (lab_d / "de.md").is_file():
        dt = (lab_d / "de.md").read_text(encoding="utf-8", errors="replace")
        has_inline_grader = "def cham(" in dt and "THANG" in dt.upper() or ("def cham(" in dt and "(2/2)" in dt)
        if minus_rx.search(dt) or (not has_inline_grader and rubric_rx.search(dt)):
            errs.append("de.md: chứa chữ chấm điểm giả")
    prj_spec = root / "labs" / "PRJ" / "SPEC.md"
    if lab_d and lab_d.parent.name.upper() == "PRJ" and prj_spec.is_file():
        pt = prj_spec.read_text(encoding="utf-8", errors="replace")
        if minus_rx.search(pt) or rubric_rx.search(pt):
            errs.append("labs/PRJ/SPEC.md: chứa chữ chấm điểm giả")
    return errs


def _extract_code_blocks(html_s: str) -> str:
    """Trích toàn bộ nội dung <div class="code">...</div> (kể cả thẻ <div> lồng) và <pre>...</pre>."""
    out = []
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", html_s, re.S | re.I):
        out.append(strip_tags(m.group(1)))
    for m in re.finditer(r'<div[^>]*class=["\'][^"\']*\bcode\b[^"\']*["\'][^>]*>', html_s, re.I):
        pos = m.end()
        depth = 1
        for tm in re.finditer(r"<(/?)div\b[^>]*>", html_s[pos:], re.I):
            depth += -1 if tm.group(1) == "/" else 1
            if depth == 0:
                out.append(strip_tags(html_s[pos : pos + tm.start()]))
                break
    return "\n".join(out)


def check_g_codetable(spec: dict, lab_d: Path | None = None) -> list[str]:
    errs = []
    tbl_rx = re.compile(r"<table[^>]*>.*?</table>", re.S | re.I)
    row_rx = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
    td_rx = re.compile(r"<td[^>]*>(.*?)</td>", re.S | re.I)
    for sc in spec.get("scenes") or []:
        if sc.get("kind") == "symbol":
            continue
        sid = str(sc.get("id") or "")
        all_shows = "\n".join(str(st.get("show") or "") for st in (sc.get("steps") or []))
        code_blocks = _extract_code_blocks(all_shows)
        code_words = set(re.findall(r"\b\d[\d_]*\b|\b[A-Za-z_][A-Za-z0-9_]*\b", code_blocks))
        for tbl_m in tbl_rx.finditer(all_shows):
            tbl = tbl_m.group(0)
            if "viết trong mã" not in tbl.lower():
                continue
            for tr in row_rx.findall(tbl):
                tds = td_rx.findall(tr)
                if not tds:
                    continue
                left = strip_tags(tds[0])
                # Định dạng sai cú pháp kiểu {:.1f} không biến đứng trước ':' là sai nguyên văn
                fmt_holes = re.findall(r"\{:[^}]+\}", left)
                if any(h not in code_blocks for h in fmt_holes):
                    errs.append(f"{sid}: mục bảng '{left[:40]}' không xuất hiện đúng dạng trong mã cùng cảnh")
                    continue
                toks = re.findall(r"\b\d[\d_]+\b|\b[A-Za-z][A-Za-z0-9_]{1,}\b", left)
                if toks and not any(t in code_words or t in code_blocks for t in toks):
                    errs.append(f"{sid}: mục bảng '{left[:40]}' không xuất hiện trong mã cùng cảnh")
                elif any(re.fullmatch(r"\d+_\d+", t) and t not in code_words for t in toks):
                    errs.append(f"{sid}: mục bảng '{left[:40]}' số có gạch dưới không xuất hiện trong mã cùng cảnh")
    return errs


def check_g_labdata(spec: dict, lab_d: Path | None) -> str:
    if not lab_d or not (lab_d / "mong_doi.txt").is_file():
        return ""
    want = (lab_d / "mong_doi.txt").read_text(encoding="utf-8", errors="replace")
    nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", want))
    if not nums:
        return ""
    other_txt = " ".join(
        strip_tags(str(st.get("show") or ""))
        for sc in (spec.get("scenes") or []) if sc.get("kind") != "practice"
        for st in (sc.get("steps") or [])
    )
    other_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", other_txt))
    shared = len(nums & other_nums)
    if shared == len(nums) and len(nums) >= 2:
        return f"{shared}/{len(nums)} số mong_doi xuất hiện ngoài Tự làm"
    return ""


def audit_root(root: Path, courses_filter: set[str], run_cham: bool = False, ignore_duration: bool = False):
    deny_list = load_deny(root)
    cur_map, by_id = load_curricula(root)
    closure_cache = {}
    cf = root / "labs" / "CONTRACT.yaml"
    contract = (yaml.safe_load(cf.read_text(encoding="utf-8")) or {}).get("labs") or {} if cf.is_file() else {}

    rows = []
    lessons_dir = root / "lessons"
    spec_files = sorted(lessons_dir.glob("*/L*.yaml"))
    for sp_path in spec_files:
        course = sp_path.parent.name.upper()
        if courses_filter and course not in courses_filter:
            continue
        lid = sp_path.name.split("_")[0].upper()
        spec = yaml.safe_load(sp_path.read_text(encoding="utf-8")) or {}
        lab_d = find_lab_dir(root, course, lid, spec)

        gp = check_g_practice(root, course, lid, spec, lab_d)
        gb = check_g_boiler(spec, deny_list)
        gl, warns_len = check_g_len(root, course, lid, spec, ignore_duration=ignore_duration)
        res = {
            "G-PRACTICE": gp,
            "G-LEAK-DE": check_g_leak_de(lab_d),
            "G-ANTI-PRINT": check_g_anti_print(root, course, lid, lab_d, contract, run_cham),
            "G-LABLANG": check_g_lablang(cur_map, by_id, closure_cache, course, lid, lab_d),
            "G-COVERS": check_g_covers(spec, gp, gb),
            "G-LEN": gl,
            "G-PAD": check_g_pad(spec),
            "G-BOILER": gb,
            "G-CHECKS": check_g_checks(spec),
            "G-SCORE": check_g_score(root, spec, lab_d),
            "G-CODETABLE": check_g_codetable(spec),
        }
        w_lab = check_g_labdata(spec, lab_d)
        warns = warns_len + ([w_lab] if w_lab else [])
        rows.append((course, lid, res, warns))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--tsv", type=Path, default=None)
    ap.add_argument("--ratchet", type=Path, default=None)
    ap.add_argument("--run-cham", action="store_true")
    ap.add_argument("--ignore-duration", action="store_true")
    args = ap.parse_args()

    root = args.root.resolve()
    courses_filter = {c.upper() for c in args.courses}
    rows = audit_root(root, courses_filter, run_cham=args.run_cham, ignore_duration=args.ignore_duration)

    if args.tsv:
        lines = ["course\tlesson\t" + "\t".join(FAIL_GATES) + "\twarns"]
        for c, l, res, warns in rows:
            vals = ["FAIL" if res[g] else "PASS" for g in FAIL_GATES]
            lines.append("\t".join([c, l, *vals, "; ".join(warns)]))
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    gate_fail_cnt = {g: 0 for g in FAIL_GATES}
    cur_fails = set()
    for c, l, res, _ in rows:
        for g in FAIL_GATES:
            if res[g]:
                gate_fail_cnt[g] += 1
                cur_fails.add((c, l, g))

    if args.ratchet:
        base_lines = args.ratchet.read_text(encoding="utf-8").splitlines()
        hdr = base_lines[0].split("\t")
        base_fails = set()
        for ln in base_lines[1:]:
            cols = ln.split("\t")
            bc, bl = cols[0], cols[1]
            for idx, g in enumerate(hdr[2:-1], 2):
                if cols[idx] == "FAIL":
                    base_fails.add((bc, bl, g))
        qf = DEFAULT_ROOT / "audit" / "review" / "learn_start" / "quality.yaml"
        locked_courses = set()
        if qf.is_file():
            qd = yaml.safe_load(qf.read_text(encoding="utf-8")) or {}
            for kc, info in (qd.get("courses") or {}).items():
                if isinstance(info, dict) and info.get("label") == "ĐÃ CHỐT":
                    locked_courses.add(kc.upper())
        regressions = sorted(cur_fails - base_fails)
        locked_bad = sorted(x for x in cur_fails if x[0] in locked_courses)
        for c, l, g in regressions:
            print(f"FAIL NEW_REGRESSION {c} {l} {g}")
        for c, l, g in locked_bad:
            print(f"FAIL LOCKED_COURSE_FAIL {c} {l} {g}")
        print(f"content_gates ratchet: {len(rows)} bài, {len(cur_fails)} FAIL nền, {len(regressions)} hồi quy mới, {len(locked_bad)} lỗi khoá ĐÃ CHỐT")
        return 1 if (regressions or locked_bad) else 0

    for c, l, res, warns in rows:
        bad = [f"{g}: {res[g][0]}" for g in FAIL_GATES if res[g]]
        if bad and len(rows) <= 50:
            print(f"FAIL {c} {l}: " + " | ".join(bad))
    summary = " · ".join(f"{g}={gate_fail_cnt[g]}" for g in FAIL_GATES)
    print(f"content_gates: {len(rows)} bài · {len(cur_fails)} lượt FAIL ({summary})")
    return 1 if cur_fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
