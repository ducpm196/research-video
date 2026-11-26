from contextlib import redirect_stdout
import io
from pathlib import Path
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

p30 = ROOT / "lessons" / "cs115" / "L30_gmm_em.yaml"
t30 = p30.read_text(encoding="utf-8")
assert "log hợp lý" in t30
p30.write_text(t30.replace("log hợp lý", "lôgarit hợp lý", 1), encoding="utf-8")

warns = []
for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    if res.errors or res.warnings:
        warns.append((lid, res.errors, res.warnings))
        print(f"FAIL/WARN {lid}: E={res.errors} W={res.warnings}", flush=True)
if not warns:
    print("ALL 22 L22..L43 LINT 0 FAIL 0 WARN!", flush=True)
assert not warns
