import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
PY = ".venv/Scripts/python.exe"
for c in ("DAN", "DSC", "MLO"):
    print(f">>> LAYOUT SCAN {c}", flush=True)
    r = subprocess.run([PY, "-B", "audit/layout_scan.py", c])
    assert r.returncode == 0, f"layout_scan failed: {c}"
print("BATCH 8A LAYOUT SCAN DONE!", flush=True)
