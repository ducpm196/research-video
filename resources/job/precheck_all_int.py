import glob
import subprocess
import sys

VENV_PY = r"D:\research-video\.venv\Scripts\python.exe"

print("1. CHECKING CURRICULUM...")
res = subprocess.run([VENV_PY, "tools/lv.py", "curriculum", "curriculum/int.yaml"], capture_output=True, text=True)
print(res.stdout)
assert res.returncode == 0, "Curriculum failed!"

print("2. LINTING ALL 8 LESSONS...")
files = sorted(glob.glob("lessons/int/*.yaml"))
assert len(files) == 8, f"Expected 8 files, got {len(files)}"
for f in files:
    res = subprocess.run([VENV_PY, "tools/lv.py", "lint", f], capture_output=True, text=True)
    last_line = [l for l in res.stdout.splitlines() if "lint:" in l]
    print(f"  {f}: {last_line[-1] if last_line else 'FAIL'}")
    assert res.returncode == 0 and "0 FAIL" in str(last_line), f"Lint failed on {f}"

print("3. RENDERING ALL 8 LESSONS...")
for f in files:
    res = subprocess.run([VENV_PY, "tools/lv.py", "render", f], capture_output=True, text=True)
    last_line = [l for l in res.stdout.splitlines() if "render:" in l]
    print(f"  {f}: {last_line[-1] if last_line else 'FAIL'}")
    assert res.returncode == 0 and "0 vấn đề" in str(last_line), f"Render failed on {f}"

print("\n>>> ALL 8 LESSONS PASSED CURRICULUM, LINT, AND RENDER (0 ISSUES)!")
