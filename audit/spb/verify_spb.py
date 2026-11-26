"""Verify 13 SPB labs (L00..L12) end-to-end via labs/cham.sh + checklib.spb_* helpers."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
BASH = GIT_BASH if Path(GIT_BASH).is_file() else (shutil.which("bash") or "bash")

rows = []


def rec(tag: str, ok: bool, detail: str):
    rows.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {tag}: {detail}")


# 1. Verify O(1) checklib helpers
rec(
    "SPB:checklib",
    alg.spb_n_plus_one(1000) == (1001, 1)
    and alg.spb_tx_connections(10, True) == (2, 20)
    and alg.spb_double_entry_sum([-300_000, 300_000]) == 0
    and alg.spb_prom_series(4, 3, 100_000) == (12, 1_200_000)
    and alg.spb_jvm_heap_mib(512, 75.0) == 384.0
    and alg.spb_tc_startup_s(50, 6, False) == 300
    and alg.spb_tc_startup_s(50, 6, True) == 6
    and alg.spb_test_pyramid_ms(200, 1) == 3000,
    "7 checklib.spb_* helpers pass exact assertions",
)

# 2. Verify all 13 Maven/Boot 4.1.3 labs sequentially via cham.sh (plus loi_sai anti-cheat)
for i in range(13):
    lid = f"L{i:02d}"
    r_ok = subprocess.run(
        [BASH, "labs/cham.sh", "SPB", lid],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    r_bad = subprocess.run(
        [BASH, "labs/cham.sh", "SPB", lid, "--du-an", f"labs/SPB/{lid}/loi_sai"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    passed = (r_ok.returncode == 0) and (r_bad.returncode != 0)
    summary_line = [ln for ln in r_ok.stdout.splitlines() if "PASS" in ln or "ĐÚNG" in ln]
    msg = summary_line[-1].strip() if summary_line else f"rc_ok={r_ok.returncode} rc_bad={r_bad.returncode}"
    rec(f"SPB:{lid}", passed, f"{msg} | anti_cheat={'FAIL_OK' if r_bad.returncode != 0 else 'LEAK!'}")
    if not passed:
        print(f"--- {lid} stdout/stderr tail ---\n{(r_ok.stdout + r_ok.stderr)[-1200:]}")

print(f"\nTỔNG SPB: {sum(rows)} PASS · {len(rows) - sum(rows)} FAIL")
sys.exit(0 if all(rows) else 1)
