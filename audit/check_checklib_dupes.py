"""Báo mọi tên hàm hay hằng ở cấp mô-đun bị định nghĩa HAI lần trong tools/checklib.py — bản sau âm thầm che bản trước và làm hỏng `checks`
của các bài cũ (đã xảy ra 2026-10-29: hàm sql của DAN che hàm sql của DBS). Chạy: .venv/Scripts/python audit/check_checklib_dupes.py → mã thoát 1 nếu trùng."""
import ast
import sys
from collections import Counter
from pathlib import Path

src = (Path(__file__).resolve().parents[1] / "tools" / "checklib.py").read_text(encoding="utf-8")
names = []
for node in ast.parse(src).body:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        names.append(node.name)
    elif isinstance(node, ast.Assign):
        names += [t.id for t in node.targets if isinstance(t, ast.Name)]
dup = sorted(n for n, c in Counter(names).items() if c > 1)
print("trùng:", dup if dup else "không có")
sys.exit(1 if dup else 0)
