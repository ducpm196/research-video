"""Kiểm độc lập mọi khẳng định của khoá BNX — tính lại bằng cách KHÁC checklib (vòng lặp thuần, mô phỏng, chạy thật: git, openssl,
Oracle/SQL Server trong Docker), rồi đối chiếu với hàm checklib (alg.bnx_*) mà `checks` của bài dùng.
Mỗi bài một tệp audit/bnx/ver/lNN.py có hàm run(rec), gọi rec("Lxx", điều_kiện, "mô tả") cho từng khẳng định.
Chạy: .venv/Scripts/python -B audit/bnx/verify_bnx.py [L06 L07 …]   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)
Dòng "SKIP" (thiếu Docker/openssl) KHÔNG tính là PASS: tổng kết ghi số SKIP và thoát 1 nếu có."""
import importlib.util
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402,F401

R = []


def rec(code, ok, what):
    st = "SKIP" if ok is None else ("PASS" if ok else "FAIL")
    R.append((code, st))
    print(st, code, "—", what)


want = {a.upper() for a in sys.argv[1:]}
for f in sorted((ROOT / "audit" / "bnx" / "ver").glob("l*.py")):
    code = f.stem.upper()
    if want and code not in want:
        continue
    spec = importlib.util.spec_from_file_location(f"ver_{f.stem}", f)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        m.run(rec)
    except Exception:
        rec(code, False, "ngoại lệ khi chạy " + f.name + ": " + traceback.format_exc().strip().splitlines()[-1])

bad = [c for c, s in R if s == "FAIL"]
skip = [c for c, s in R if s == "SKIP"]
npass = sum(1 for _, s in R if s == "PASS")
print(f"\nverify_bnx: {npass}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else "") + (f"; SKIP: {skip}" if skip else ""))
sys.exit(1 if bad or skip or not R else 0)
