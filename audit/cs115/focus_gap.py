"""Đo khoảng trống `focus` (pedagogy luật 19): step có ≥2 câu nói về một khối có ≥2 phần, hoặc step không `show` mà nói
tiếp về bảng có ≥2 khối, nhưng không có `focus` → người xem tự dò. So sánh hai khoá. Chạy: focus_gap.py cs115 [L05 …]"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

course, only = sys.argv[1], set(sys.argv[2:])
tot = {"cand": 0, "foc": 0}
for p in sorted((ROOT / "lessons" / course).glob("L??_*.yaml")):
    lid = p.name[:3]
    if only and lid not in only:
        continue
    sp = lv.load_spec(p)
    cand = foc = 0
    rows = []
    fi = 0
    for sc in sp["scenes"]:
        blocks = []
        for ki, st in enumerate(sc["steps"]):
            if st.get("clear"):
                blocks = []
            if st.get("show"):
                blocks.append(lv.html_units(str(st["show"])))
            n = len(lv.sentences(st["say"]))
            units = len(blocks[-1]) if st.get("show") else 0
            need = n >= 2 and (units >= 2 or (not st.get("show") and len(blocks) >= 2))
            if need:
                cand += 1
                if st.get("focus") is not None:
                    foc += 1
                else:
                    rows.append(f"  {lid} {sc['id']}.{ki} khung {fi}-{fi + n - 1}: {n} câu, khối {units} phần, bảng {len(blocks)} khối")
            fi += n
    tot["cand"] += cand; tot["foc"] += foc
    print(f"{lid}: {foc}/{cand} step cần focus đã có")
    if only:
        print("\n".join(rows))
print(f"TỔNG {course}: {tot['foc']}/{tot['cand']}")
