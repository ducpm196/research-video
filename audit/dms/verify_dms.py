"""Bộ kiểm khoá DMS (nâng AF2, WP5, 2026-11-14). Chạy: .venv/Scripts/python -B audit/dms/verify_dms.py [-v]

KHÔNG sinh bài (bài DMS là YAML viết tay; L08, L16–L18 sinh từ mẫu audit/dms/src). Ba việc, độc lập với lời giải lab và với `checks:` của bài:
  A. Tính lại BẰNG CÁCH KHÁC (tập hợp, Fraction, phép bit, đếm vét cạn…) từng dòng của mọi lab labs/DMS/Lxx/mong_doi.txt; so từng dòng,
     và kiểm lời giải (loi_giai.py chạy thật, hoặc loi_giai.md có đủ dòng đáp số).
  B. Ghép NGUYÊN VĂN từng cặp (khối mã, khối kết quả) của cảnh quymo trong lessons/dms/*.yaml, CHẠY THẬT bằng Python, so với khối kết quả
     hiện trên màn hình (chuẩn hoá khoảng trắng); và tính lại bằng công thức độc lập các con số của cảnh quy mô.
  C. Hợp đồng AF2 của các bài đã nâng: af2 + covers + cảnh practice có lab, bài tự đứng được (không “như đã học ở khoá…”), lời đọc ≤ 2 300 từ.
Mã thoát 0 = đủ PASS."""
import io
import itertools
import math
import re
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
V = "-v" in sys.argv
sys.path.insert(0, str(ROOT / "audit" / "dms" / "vparts"))
from reg import LABS, QUY_MO  # noqa: E402
for _f in sorted((ROOT / "audit" / "dms" / "vparts").glob("l[0-9][0-9].py")):
    __import__(_f.stem)
res = []


def ok(name, cond, detail=""):
    res.append((bool(cond), name, detail))
    if V or not cond:
        print(("PASS " if cond else "FAIL ") + name + ((" :: " + str(detail)[:300]) if detail and not cond else ""))


def lab_dir(lid):
    return ROOT / "labs" / "DMS" / lid


def mong_doi(lid):
    return [l.rstrip() for l in (lab_dir(lid) / "mong_doi.txt").read_text(encoding="utf-8").strip("\n").split("\n")]


def spec(lid):
    f = next((ROOT / "lessons" / "dms").glob(f"{lid}_*.yaml"))
    return yaml.safe_load(f.read_text(encoding="utf-8"))


def run_code(code):
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "k.py"
        f.write_text(code.strip("\n") + "\n", encoding="utf-8")
        p = subprocess.run([sys.executable, "-B", str(f)], capture_output=True, text=True, encoding="utf-8", cwd=td,
                           env={"PYTHONIOENCODING": "utf-8", "SYSTEMROOT": "C:\\Windows"}, timeout=120)
    return p.returncode, [l.rstrip() for l in p.stdout.replace("\r\n", "\n").strip("\n").split("\n")], p.stderr


# ───────────────────────── A. lab: tính lại độc lập ─────────────────────────


def run_labs():
    for lid, fn in sorted(LABS.items()):
        want = fn()
        got = mong_doi(lid)
        ok(f"lab {lid}: mong_doi.txt = tính lại độc lập ({len(want)} dòng)", want == got, f"\nmong_doi={got}\ntính lại={want}")
        d = lab_dir(lid)
        sols = sorted(d.glob("loi_giai.*"))
        ok(f"lab {lid}: đúng một loi_giai.*", len(sols) == 1, sols)
        if sols and sols[0].suffix == ".py":
            rc, out, err = run_code(sols[0].read_text(encoding="utf-8"))
            ok(f"lab {lid}: loi_giai.py chạy thật = mong_doi.txt", rc == 0 and out == got, err[-200:] or out)
        elif sols and sols[0].suffix == ".md":
            md = sols[0].read_text(encoding="utf-8")
            miss = [l for l in got if l not in md]
            ok(f"lab {lid}: loi_giai.md có đủ dòng đáp số", not miss, miss)
        de = (d / "de.md").read_text(encoding="utf-8")
        ok(f"lab {lid}: de.md nêu lệnh chấm/đối chiếu", ("cham.sh DMS " + lid in de) or sols[0].suffix == ".md")


# ───────────────────────── B. cảnh quy mô: mã trên màn hình chạy thật ─────────────────────────
def screen_text(show):
    """các khối `div.code` của một step: [văn bản mỗi khối]"""
    import html
    out = []
    for m in re.finditer(r'<div class="code">(.*?)</div></div>|<div class="code">(.*?)</div>(?=<p|$)', show, re.S):
        body = m.group(1) or m.group(2) or ""
        out.append("\n".join(html.unescape(re.sub(r"<[^>]+>", "", l)).rstrip() for l in re.findall(r"<div>(.*?)</div>", body + "</div>", re.S)))
    return out


def blocks_of_step(show):
    import html
    res_ = []
    for m in re.finditer(r'<div class="code">((?:<div>.*?</div>)*)</div>', show, re.S):
        lines = re.findall(r"<div>(.*?)</div>", m.group(1), re.S)
        res_.append("\n".join(html.unescape(re.sub(r"<[^>]+>", "", l)).rstrip() for l in lines))
    return res_




def run_screen():
    n = 0
    for f in sorted((ROOT / "lessons" / "dms").glob("L*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in d["scenes"]:
            if sc["id"] != "quymo":
                continue
            for ti, st in enumerate(sc["steps"]):
                bl = blocks_of_step(str(st.get("show", "")))
                if not bl:
                    continue
                ok(f"{d['id']} quymo step {ti}: cặp (mã, kết quả)", len(bl) == 2, len(bl))
                if len(bl) == 2:
                    rc, out, err = run_code(bl[0])
                    shown = [l for l in bl[1].split("\n")]
                    ok(f"{d['id']} quymo step {ti}: mã trên màn hình chạy thật ra đúng kết quả hiện trên màn hình", rc == 0 and out == shown, (err[-200:], out, shown))
                    n += 1
    return n


def run_quymo_numbers():
    for lid, fn in sorted(QUY_MO.items()):
        for name, cond in fn():
            ok(f"{lid} quy mô: {name}", cond)


# ───────────────────────── C. hợp đồng AF2 ─────────────────────────
BAD_XREF = re.compile(r"như đã học ở khoá|khoá (CS115|CS112|NET|PYT|FND)", re.I)


def run_contract():
    for f in sorted((ROOT / "lessons" / "dms").glob("L*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not d.get("af2"):
            continue
        lid = d["id"]
        kinds = [s["kind"] for s in d["scenes"]]
        ok(f"{lid}: af2 + covers phủ mọi mục tiêu", sorted(c["objective"] for c in d.get("covers") or []) == list(range(1, len(d["objectives"]) + 1)))
        ok(f"{lid}: có cảnh practice trước recap có lab", "practice" in kinds and kinds.index("practice") < kinds.index("recap")
           and all((ROOT / s["lab"] / "mong_doi.txt").is_file() for s in d["scenes"] if s["kind"] == "practice"))
        ok(f"{lid}: có cảnh quymo (quy mô/thời gian) hoặc là bài hành trình có chặng theo thời gian", any(s["id"] == "quymo" for s in d["scenes"]) or (d.get("case") == "journey" and sum(1 for s in d["scenes"] if s.get("stage")) >= 4))
        words = sum(len(str(st.get("say", "")).split()) for s in d["scenes"] for st in s["steps"])
        ok(f"{lid}: lời đọc {words} từ ≤ 2 300", words <= 2300)
        txt = " ".join(str(st.get("say", "")) + str(st.get("show", "")) for s in d["scenes"] for st in s["steps"])
        ok(f"{lid}: không 'như đã học ở khoá…'", not BAD_XREF.search(txt))
        cur = yaml.safe_load((ROOT / "curriculum" / "dms.yaml").read_text(encoding="utf-8"))
        c = next(x for x in cur["lessons"] if x["id"] == lid)
        ok(f"{lid}: mục tiêu giáo án = mục tiêu bài", c["objectives"] == d["objectives"])


if __name__ == "__main__":
    run_labs()
    nscr = run_screen()
    run_quymo_numbers()
    run_contract()
    npass = sum(1 for r in res if r[0])
    print(f"verify_dms: {npass} PASS · {len(res) - npass} FAIL (lab {len(LABS)}, cảnh quy mô chạy thật {nscr})")
    sys.exit(0 if npass == len(res) else 1)
