"""Chạy audit/review/audit_all.py NGUYÊN VĂN, chỉ khác hai điều, đều ở trong bộ nhớ (không sửa tệp nào của kho):
  1. checklib.par_amdahl được thay bằng công thức đóng tương đương (không dựng danh sách n phần tử) — để đo xem sau khi sửa
     hàm này thì audit_all có còn tràn RAM không (giả thuyết PAR L12, plan AF5 Phụ lục A mục 2);
  2. kết quả ghi vào logs/af5r2/audit_all.patched.tsv thay cho audit/review/audit_all.tsv.
Cuối cùng in đỉnh RAM (PeakWorkingSetSize) của tiến trình này và thời gian chạy.
Dùng: .venv/Scripts/python -B audit/review/audit_final/logs/af5r2/audit_all_patched.py [khoá …]"""
import atexit
import ctypes
import ctypes.wintypes as wt
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SRC = ROOT / "audit" / "review" / "audit_all.py"
T0 = time.time()


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t), ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t)]


def peak():
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.GetCurrentProcess.restype = wt.HANDLE
    k.K32GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
    c = PMC()
    c.cb = ctypes.sizeof(PMC)
    k.K32GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return c.PeakWorkingSetSize / 2 ** 20, c.PeakPagefileUsage / 2 ** 20


def report():
    ws, pf = peak()
    print(f"\nPEAK_WORKING_SET_MB={ws:.0f} PEAK_COMMIT_MB={pf:.0f} ELAPSED_S={time.time() - T0:.0f}", flush=True)


atexit.register(report)
sys.path.insert(0, str(ROOT / "tools"))
import checklib  # noqa: E402

_old = checklib.par_amdahl
assert abs(_old(0.75, 16) - 1 / (0.25 + 0.75 / 16)) < 1e-12, "công thức đóng không tương đương bản gốc"
checklib.par_amdahl = lambda p, n: 1.0 / ((1 - p) + p / n)
src = SRC.read_text(encoding="utf-8")
old = '(ROOT / "audit" / "review" / "audit_all.tsv").write_text('
assert src.count(old) == 1
src = src.replace(old, f'(ROOT / "audit" / "review" / "audit_final" / "logs" / "af5r2" / "audit_all.patched.tsv").write_text(')
sys.argv = [str(SRC)] + sys.argv[1:]
exec(compile(src, str(SRC), "exec"), {"__name__": "__main__", "__file__": str(SRC)})
