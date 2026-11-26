"""Kiểm độc lập mọi khẳng định của khoá CAS — tính lại bằng cách KHÁC checklib và khác `checks` của bài (datetime thay phép trừ phút,
Fraction thay số thực, liệt kê/mô phỏng thay công thức, numpy thay phép tính tay), rồi đối chiếu với con số trên màn hình.
Mỗi bài một tệp audit/cas/ver/Lxx.py (tách tệp để các bài soạn song song không sửa chung một tệp); tệp đó gọi rec("Lxxa", điều_kiện, "mô tả").
Thiếu tệp của một bài trong giáo án → FAIL (khoá chưa đủ).
Chạy: .venv/Scripts/python audit/cas/verify_cas.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402,F401
import yaml  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


cur = yaml.safe_load((ROOT / "curriculum" / "cas.yaml").read_text(encoding="utf-8"))
for les in cur["lessons"]:
    f = ROOT / "audit" / "cas" / "ver" / f"{les['id']}.py"
    print(f"\n── {les['id']}: {les['title']}")
    if not f.exists():
        rec(les["id"], False, f"thiếu {f.relative_to(ROOT)}")
        continue
    exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), {"rec": rec, "alg": alg, "ROOT": ROOT, "__name__": "cas_ver"})

bad = [c for c, ok in R if not ok]
# ── Kiểm tự động mọi lab (du_lieu.txt + ca_an/) qua cham.sh ──
import subprocess as _subp
from pathlib import Path as _LabPath
_BASH = r"C:\Program Files\Git\bin\bash.exe"
if not _LabPath(_BASH).exists():
    _BASH = "bash"
for _ld in sorted((ROOT / "labs" / "CAS").glob("L*")):
    _rp = _subp.run([_BASH, str(ROOT / "labs" / "cham.sh"), "CAS", _ld.name], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    rec(f"{_ld.name}:lab", _rp.returncode == 0 and "PASS" in _rp.stdout and "2 ca an" in _rp.stdout, f"cham.sh {_ld.name} (public + 2 ca_an)")

print(f"\nverify_cas: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
