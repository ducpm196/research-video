import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

err = warn = 0
for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        with redirect_stdout(io.StringIO()):
            r = lv.lint(sp, quiet=True)
        w = sum(len((s.get("say") or "").split()) for sc in sp["scenes"] for s in sc["steps"])
        err += len(r.errors)
        warn += len(r.warnings)
        if r.errors or r.warnings or w < 1620:
            print(f"{c.upper()}:{sp['id']} w={w} FAIL={len(r.errors)} WARN={len(r.warnings)} {r.errors[:2]} {r.warnings[:2]}", flush=True)
print(f"TOTAL Stage 10 (80 lessons): FAIL={err}, WARN={warn}", flush=True)
assert err == 0 and warn == 0

for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    rc = subprocess.run([PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c}.yaml"], cwd=ROOT)
    assert rc.returncode == 0, f"curriculum {c} failed"

r = subprocess.run([PY, "-B", "audit/review/sync_tpl_from_lesson.py", "TOC", "PLC", "PAR", "HCI", "SEP", "CAS", "--write"], cwd=ROOT)
assert r.returncode == 0, "sync_tpl failed"

for c in ("TOC", "PLC", "PAR", "HCI", "SEP", "CAS"):
    rs = subprocess.run([PY, "-B", "audit/review/screen_code.py", "check", "--course", c], cwd=ROOT)
    assert rs.returncode == 0, f"screen_code {c} failed"
    vp = ROOT / "audit" / c.lower() / f"verify_{c.lower()}.py"
    rv = subprocess.run([PY, "-B", str(vp)], cwd=ROOT)
    assert rv.returncode == 0, f"verify {c} failed"
    ok = 0
    for ld in sorted((ROOT / "labs" / c).glob("L*")):
        res = subprocess.run([PY, "-B", str(ld / "loi_giai.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        exp = (ld / "mong_doi.txt").read_text(encoding="utf-8").strip()
        assert res.returncode == 0 and res.stdout.strip() == exp, f"{c} {ld.name}"
        ok += 1
    print(f"labs {c}: {ok}/{ok} PASS", flush=True)

for c in ("TOC", "PLC", "PAR", "HCI", "SEP", "CAS"):
    rl = subprocess.run([PY, "-B", "audit/layout_scan.py", c], cwd=ROOT)
    assert rl.returncode == 0, f"layout_scan {c} failed"
    rows = [l for l in (ROOT / "audit" / f"layout_{c}.tsv").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 0, f"{c} layout issues: {rows[:5]}"

print("ALL STAGE 10 AUTOMATED GATES PASSED!", flush=True)
