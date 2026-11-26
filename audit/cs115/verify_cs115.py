"""Kiểm tự động các bài lab CS115 L22..L43 qua labs/cham.sh (public + 2 ca_an)."""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = "bash"

R = []
for n in range(22, 44):
    lid = f"L{n:02d}"
    rp = subprocess.run([BASH, str(ROOT / "labs" / "cham.sh"), "CS115", lid], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    ok = rp.returncode == 0 and "PASS" in rp.stdout and "2 ca an" in rp.stdout
    R.append((lid, ok))
    print(f"{'PASS' if ok else 'FAIL'} CS115:{lid}:lab — cham.sh {lid} (public + 2 ca_an)")

n_ok = sum(o for _, o in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
