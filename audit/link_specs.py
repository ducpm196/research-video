"""Nối đặc tả bài vào lộ trình: với mỗi tệp lessons/<khoá>/Lxx_*.yaml, thêm `spec:` vào bài Lxx của curriculum/<khoá>.yaml nếu chưa có,
và báo bài nào có tên trong đặc tả KHÁC tên trong lộ trình (phải sửa tay, không tự đổi).
Chạy: .venv/Scripts/python audit/link_specs.py CSA"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

course = sys.argv[1].upper()
cp = ROOT / "curriculum" / f"{course.lower()}.yaml"
text = cp.read_text(encoding="utf-8")
cur = lv.load_yaml(cp)
added, diff = [], []
for f in sorted((ROOT / "lessons" / course.lower()).glob("L*_*.yaml")):
    sp = lv.load_yaml(f)
    lid = sp["id"]
    l = next((x for x in cur["lessons"] if x["id"] == lid), None)
    if l is None:
        print("KHÔNG CÓ trong lộ trình:", lid); continue
    tt = sp["title"].split(" — ", 1)[-1]
    if tt != l["title"]:
        diff.append((lid, tt, l["title"]))
    if l.get("spec"):
        continue
    m = re.search(rf'(\n  - id: {lid}\n    title: "[^\n]*"\n)', text)
    assert m, lid
    text = text.replace(m.group(1), m.group(1) + f"    spec: lessons/{course.lower()}/{f.name}\n", 1)
    added.append(lid)
cp.write_text(text, encoding="utf-8")
print("đã nối:", added or "không có")
for lid, a, b in diff:
    print(f"TÊN KHÁC {lid}: đặc tả “{a}” ≠ lộ trình “{b}”")
