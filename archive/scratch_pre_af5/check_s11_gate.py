import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")

# 1. Lint all 75 lessons
r = subprocess.run([PY, "-B", "scratch/lint_stage11.py"], cwd=ROOT)
assert r.returncode == 0, "lint_stage11 failed"

# 2. Curriculum check for all 5 courses
for c in ("rbm", "esy", "rob", "gfx", "bch"):
    print(f"--- curriculum {c} ---", flush=True)
    rc = subprocess.run([PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c}.yaml"], cwd=ROOT)
    assert rc.returncode == 0, f"curriculum {c} failed"

# 3. Sync templates + screen_code check + verify_*.py
r = subprocess.run([PY, "-B", "audit/review/sync_tpl_from_lesson.py", "RBM", "ESY", "ROB", "GFX", "BCH", "--write"], cwd=ROOT)
assert r.returncode == 0, "sync_tpl failed"

for c in ("RBM", "ESY", "ROB", "GFX", "BCH"):
    print(f"--- screen_code {c} ---", flush=True)
    rs = subprocess.run([PY, "-B", "audit/review/screen_code.py", "check", "--course", c], cwd=ROOT)
    assert rs.returncode == 0, f"screen_code {c} failed"
    vp = ROOT / "audit" / c.lower() / f"verify_{c.lower()}.py"
    print(f"--- {vp.name} ---", flush=True)
    rv = subprocess.run([PY, "-B", str(vp)], cwd=ROOT)
    assert rv.returncode == 0, f"verify {c} failed"

# 4. Layout scan on all 5 courses (one course per call)
for c in ("RBM", "ESY", "ROB", "GFX", "BCH"):
    print(f"--- layout_scan {c} ---", flush=True)
    rl = subprocess.run([PY, "-B", "audit/layout_scan.py", c], cwd=ROOT)
    assert rl.returncode == 0, f"layout_scan {c} failed"

# 5. Direct python execution of all 75 labs/*/loi_giai.py == mong_doi.txt
for c in ("RBM", "ESY", "ROB", "GFX", "BCH"):
    ok = 0
    for ld in sorted((ROOT / "labs" / c).glob("L*")):
        res = subprocess.run([PY, "-B", str(ld / "loi_giai.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        exp = (ld / "mong_doi.txt").read_text(encoding="utf-8").strip()
        assert res.returncode == 0 and res.stdout.strip() == exp, f"{c} {ld.name}: got={res.stdout!r} exp={exp!r}"
        ok += 1
    print(f"labs {c}: {ok}/{ok} PASS", flush=True)

print("ALL STAGE 11 AUTOMATED GATES PASSED!", flush=True)
