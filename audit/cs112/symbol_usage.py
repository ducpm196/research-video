"""Với mỗi bài CS112: ký hiệu trong `assumes` có thật sự xuất hiện trên màn hình không, và ký hiệu nào xuất hiện mà chưa được
bài tiên quyết dạy — dùng để sửa lỗi `curriculum` “assumes … nhưng chưa bài tiên quyết nào giới thiệu”.
Chạy: .venv/Scripts/python audit/cs112/symbol_usage.py"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

reg = {s["id"]: s for s in lv.registry("CS112")["symbols"]}
for p in sorted((ROOT / "lessons" / "cs112").glob("L*.yaml")):
    sp = lv.load_spec(p)
    maths = [m.group(1) or m.group(2) for _, _, _, st in lv.iter_steps(sp) for m in lv.MATH_RE.finditer(str(st.get("show", "")))]
    plain = " ".join(re.sub(r"<[^>]+>", " ", lv.MATH_RE.sub(" ", str(st.get("show", "")))) for _, _, _, st in lv.iter_steps(sp))
    used = {a for a in sp.get("assumes") or [] if any(re.search(reg[a]["pattern"], t) for t in maths)
            or (reg[a].get("unicode") and any(ch in plain for ch in reg[a]["unicode"]))}
    print(f"{p.name[:3]} assumes không dùng: {sorted(set(sp.get('assumes') or []) - used)}")
