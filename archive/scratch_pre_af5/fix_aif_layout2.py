"""Re-run AIF with 5-row reading tables so AIF L01 & L04 pass layout_scan with 0 overflow."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
r = subprocess.run([PY, "-B", "-u", "audit/s9_11/up_s9_data_ai.py", "AIF"], cwd=ROOT)
assert r.returncode == 0, "FAILED: up_s9_data_ai.py AIF"

for i in range(15):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    assert not res.errors and not res.warnings, f"{lid}: {res.errors} {res.warnings}"
    assert w >= 1645, f"{lid}: w={w}"
    print(f"AIF:{lid}: w={w} E=0 W=0", flush=True)

for cmd in (
    [PY, "-B", "-u", "audit/aif/verify_aif.py"],
    [PY, "-B", "-u", "audit/layout_scan.py", "AIF"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("AIF LAYOUT RECHECK DONE!", flush=True)
