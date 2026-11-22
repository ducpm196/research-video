"""Re-upgrade 5 wrapped S9 lessons (IRS L02, AGT L01, CVI L08/09/12), sync all 5 S9 ledgers, run full gates + layout_scan on touched courses."""
from contextlib import redirect_stdout
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import lv  # noqa: E402
import af2_upgrader as up  # noqa: E402
import common  # noqa: E402
import up_s9_llm_rl_cv as u  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

TOUCHED = {("IRS", "L02"), ("AGT", "L01"), ("CVI", "L08"), ("CVI", "L09"), ("CVI", "L12")}

for c, items in u.DATA.items():
    for lid, hint, de_md, sol in items:
        if (c, lid) in TOUCHED:
            common.upgrade_lesson(c, lid, hint, de_md, sol, covers=u.COVERS[(c, lid)], force_code=True)
            print(f"RE-UPGRADED {c}:{lid}", flush=True)
    up.sync_course_ledger(c, default_lang="python")
    for lid, hint, de_md, sol in items:
        common.sync_practice_run_blocks(c, lid, sol)
    print(f"SYNCED LEDGER {c}", flush=True)

bad = []
for c in ("irs", "agt", "llm", "rln", "cvi"):
    for fp in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        lid = sp["id"]
        w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        if res.errors or res.warnings:
            bad.append(f"{c.upper()}:{lid} E={res.errors} W={res.warnings}")
        if w < 1645:
            bad.append(f"{c.upper()}:{lid} w={w}")
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                say = st.get("say") or ""
                foc = st.get("focus")
                sents = lv.sentences(say)
                if foc is not None and len(foc) != len(sents):
                    bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
                for s in sents:
                    if len(s) > 170: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >170 ({len(s)}): {s}")
                    if len(s.split()) > 38: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >38w ({len(s.split())}): {s}")
                    if "càng " in s.lower(): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} 'càng ': {s}")
                    if re.search(r"[$_^]", s): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} TeX: {s}")
        print(f"CHECK {c.upper()}:{lid} w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)

for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} issues"

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for c in ("IRS", "AGT", "LLM", "RLN", "CVI"):
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
    ):
        print(">>> RUN:", " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"FAILED: {cmd}"

for c in ("IRS", "AGT", "CVI"):
    cmd = [PY, "-B", "audit/layout_scan.py", c]
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
    tsv = (ROOT / "audit" / f"layout_{c}.tsv").read_text(encoding="utf-8").strip()
    assert not tsv, f"layout_{c}.tsv not empty:\n{tsv}"

print("STAGE 9 BATCH-2 (69 LESSONS) 100% GATES + LAYOUT CLEAN!", flush=True)
