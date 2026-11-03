"""Kiểm độc lập mọi khẳng định của khoá RLN — tính lại bằng cách KHÁC `checks` của bài (giải hệ bằng sympy/ma trận, mô phỏng
Monte Carlo có hạt giống cố định, liệt kê hết các trường hợp, phân số chính xác), rồi đối chiếu với con số hiện trên màn hình
và với hàm checklib (alg.rln_*) mà `checks` dùng. Mỗi bài một tệp phần `audit/rln/verify_parts/Lxx.py` (chạy tuần tự trong cùng
không gian tên, dùng hàm rec(mã, điều_kiện, mô_tả)) để nhiều người soạn không ghi đè lẫn nhau.
Chạy: .venv/Scripts/python audit/rln/verify_rln.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
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


for part in sorted((Path(__file__).parent / "verify_parts").glob("L*.py")):
    ns = {"rec": rec, "alg": alg, "__name__": f"verify_rln_{part.stem}"}
    try:
        exec(compile(part.read_text(encoding="utf-8"), str(part), "exec"), ns)
    except Exception as e:  # một phần hỏng không được che các phần khác
        rec(part.stem, False, f"lỗi khi chạy {part.name}: {e!r}")

bad = [c for c, ok in R if not ok]
print(f"\nverify_rln: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad or not R else 0)
