"""Kiểm độc lập mọi khẳng định của khoá __COURSE__ — tính lại bằng cách KHÁC checklib (vòng lặp thuần, mô phỏng, sympy, chạy thật),
rồi đối chiếu với hàm checklib (alg) mà `checks` của bài dùng. Mỗi bài một dòng rec("Lxx", điều_kiện, "mô tả").
Chạy: .venv/Scripts/python audit/__COURSE_LC__/verify___COURSE_LC__.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402,F401

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: <khẳng định> — tính lại bằng <cách khác> ──
rec("L00", 2 * 3 == 6, "ví dụ: thay bằng phép kiểm thật của bài")

bad = [c for c, ok in R if not ok]
print(f"\nverify___COURSE_LC__: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
