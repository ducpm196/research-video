"""Kiểm độc lập mọi khẳng định của khoá IRS — tính lại bằng cách KHÁC `checks` của bài (liệt kê mọi thứ tự, mô phỏng từng lượt,
phân số chính xác, numpy, sinh dữ liệu ngẫu nhiên rồi đếm), rồi đối chiếu với con số hiện trên màn hình và với hàm checklib (alg).
Mỗi bài một tệp phần `audit/irs/verify_parts/Lxx.py` (chạy tuần tự trong cùng không gian tên, dùng hàm rec(mã, điều_kiện, mô_tả))
để nhiều người soạn không ghi đè lẫn nhau.
Chạy: .venv/Scripts/python audit/irs/verify_irs.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
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
    ns = {"rec": rec, "alg": alg, "__name__": f"verify_irs_{part.stem}"}
    try:
        exec(compile(part.read_text(encoding="utf-8"), str(part), "exec"), ns)
    except Exception as e:  # một phần hỏng không được che các phần khác
        rec(part.stem, False, f"lỗi khi chạy {part.name}: {e!r}")

bad = [c for c, ok in R if not ok]
# ── Kiểm tự động mọi lab (du_lieu.txt + ca_an/) qua cham.sh ──
import subprocess as _subp
from pathlib import Path as _LabPath
_BASH = r"C:\Program Files\Git\bin\bash.exe"
if not _LabPath(_BASH).exists():
    _BASH = "bash"
for _ld in sorted((ROOT / "labs" / "IRS").glob("L*")):
    _rp = _subp.run([_BASH, str(ROOT / "labs" / "cham.sh"), "IRS", _ld.name], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    rec(f"{_ld.name}:lab", _rp.returncode == 0 and "PASS" in _rp.stdout and "2 ca an" in _rp.stdout, f"cham.sh {_ld.name} (public + 2 ca_an)")

print(f"\nverify_irs: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad or not R else 0)
