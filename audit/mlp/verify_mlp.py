"""Kiểm độc lập 14 bài khoá MLP: chạy thật toàn bộ 14 lab trên labs/.venv-ml (du_lieu.txt + ca_an/) + cham.sh & tính tất định."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import af2_kit as ak  # noqa: E402

VENV_ML = ROOT / "labs" / ".venv-ml" / "Scripts" / "python.exe"
TOTAL_CHECKS = 0

for ldir in sorted((ROOT / "labs" / "MLP").glob("L*")):
    lid = ldir.name
    sol = ldir / "loi_giai.py"
    din = (ldir / "du_lieu.txt").read_text(encoding="utf-8")
    exp = (ldir / "mong_doi.txt").read_text(encoding="utf-8").strip()

    t0 = time.perf_counter()
    p1 = subprocess.run([str(VENV_ML), "-I", "-X", "utf8", "-B", str(sol)], input=din, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60)
    dt = time.perf_counter() - t0
    assert p1.returncode == 0, f"{lid} run1 failed: {p1.stderr}"
    assert dt <= 60.0, f"{lid} too slow: {dt:.2f}s"
    assert p1.stdout.strip() == exp, f"{lid} mismatch vs mong_doi.txt: {p1.stdout} != {exp}"
    TOTAL_CHECKS += 1

    p2 = subprocess.run([str(VENV_ML), "-I", "-X", "utf8", "-B", str(sol)], input=din, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert p2.stdout == p1.stdout, f"{lid} non-deterministic output!"
    TOTAL_CHECKS += 1

    chk = subprocess.run([ak.BASH_EXE, str(ROOT / "labs" / "cham.sh"), "MLP", lid],
                         cwd=ROOT, env=ak._tool_env(), capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert chk.returncode == 0 and "PASS" in chk.stdout, f"{lid} cham.sh failed: {chk.stdout} {chk.stderr}"
    TOTAL_CHECKS += 1
    print(f"PASS MLP {lid}: {dt:.2f}s, {len(exp.splitlines())} dòng, deterministic=OK, cham.sh={chk.stdout.strip()}")

print(f"verify_mlp: {TOTAL_CHECKS}/{TOTAL_CHECKS} PASS (0 FAIL)")
