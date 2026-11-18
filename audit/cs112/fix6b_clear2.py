"""fix6 CS112 L15–L29: bước gợi ý ("Nếu kẹt") và bước bảng đọc trong gợi ý bắt đầu bằng `clear: true` (tránh TRÀN bảng). Chạy: .venv/Scripts/python -B audit/cs112/fix6b_clear2.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import ensure_clear, lesson, tpl, regen  # noqa

TPL = {"L17", "L18", "L21", "L23", "L24", "L25", "L26"}
for n in range(15, 30):
    lid = f"L{n}"
    path = tpl(lid) if lid in TPL else lesson(lid)
    c = ensure_clear(path, "<b>Nếu kẹt:</b>") + ensure_clear(path, "cách viết trong gợi ý")
    print(lid, "thêm clear:", c)
    if lid in TPL:
        regen(lid)
