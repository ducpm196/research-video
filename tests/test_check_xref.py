"""Kiểm thử check_xref.py: toàn kho sạch (rc=0) và bắt được ca âm tham chiếu chéo sang khoá khác (rc=1)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import check_xref  # noqa: E402


def main():
    fails = 0
    # 1. Ca dương: chạy trên toàn kho thật → rc=0
    p = subprocess.run([sys.executable, "-B", str(ROOT / "audit" / "review" / "check_xref.py")],
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    ok_repo = p.returncode == 0
    fails += not ok_repo
    print(f"{'PASS' if ok_repo else 'FAIL'} | check_xref toàn kho rc={p.returncode}: {p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ''}")

    # 2. Ca âm: câu tham chiếu sang khoá khác bị bắt; "khoá lập trình C" và "MLP" đứng lẻ không bị bắt nhầm
    neg = check_xref.find("Như đã học ở khoá DBS về chỉ mục.", "BNK")
    ok_neg = bool(neg) and any("DBS" in kind for _, kind in neg)
    fails += not ok_neg
    print(f"{'PASS' if ok_neg else 'FAIL'} | bắt ca âm 'như đã học ở khoá DBS': {neg}")

    ok_cpr = check_xref.find("Chào bạn đến với khoá lập trình C và quản lý bộ nhớ.", "CPR") == []
    fails += not ok_cpr
    print(f"{'PASS' if ok_cpr else 'FAIL'} | 'khoá lập trình C' không khớp nhầm JVA")

    ok_mlp = check_xref.find("Mạng perceptron nhiều lớp (MLP) không lồi.", "CS115") == []
    fails += not ok_mlp
    print(f"{'PASS' if ok_mlp else 'FAIL'} | 'MLP' đứng lẻ không khớp nhầm khoá MLP")

    print(f"test_check_xref: {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
