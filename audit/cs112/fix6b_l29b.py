"""fix6 CS112 L29 (đợt 2). Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l29b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson  # noqa

P = lesson("L29")
edit(P, "Bài học sai thứ ba, của người đã đi làm, là đòi chứng minh mọi dòng mã mới dám dùng.", "Bài học sai thứ ba là đòi chứng minh mọi dòng mã mới dám dùng.")
