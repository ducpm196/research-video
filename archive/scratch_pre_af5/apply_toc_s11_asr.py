"""Apply verified HAND reasons for TOC + Stage 11 (RBM, ESY, ROB, GFX, BCH), sync_tpl_asr, regenerate asr_report, and confirm 0 flags."""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

ITEMS = [
    ("TOC", "TOC L04-L14 (2026-11-21)", "scratch/asr_toc.txt", ["L04", "L09", "L12", "L13", "L14"]),
    ("RBM", "RBM (2026-11-21)", "scratch/asr_rbm.txt", ["L01", "L02", "L04", "L06", "L09", "L10", "L14", "L17"]),
    ("ESY", "ESY (2026-11-21)", "scratch/asr_esy.txt", ["L00", "L02", "L07", "L08", "L11", "L13"]),
    ("ROB", "ROB (2026-11-21)", "scratch/asr_rob.txt", ["L01", "L02", "L06", "L11"]),
    ("GFX", "GFX (2026-11-21)", "scratch/asr_gfx.txt", ["L01", "L02", "L07", "L08", "L12"]),
    ("BCH", "BCH (2026-11-21)", "scratch/asr_bch.txt", ["L01", "L02", "L12"]),
]

hand_text = (ROOT / "audit/dms/asr_review_dms.py").read_text("utf-8")
for c, marker, draft, _ in ITEMS:
    if marker not in hand_text:
        subprocess.run([PY, "-B", "audit/review/asr_hand_insert.py", draft, marker], cwd=ROOT, check=True)
        hand_text = (ROOT / "audit/dms/asr_review_dms.py").read_text("utf-8")
    else:
        print(f"SKIP insert {marker} (already present)")

for c, _, _, lids in ITEMS:
    print(f">>> ASR_REVIEW {c} {lids}", flush=True)
    subprocess.run([PY, "-B", "audit/dms/asr_review_dms.py", "--course", c, *lids], cwd=ROOT, check=True)
    subprocess.run([PY, "-B", "audit/review/sync_tpl_asr.py", c, *lids], cwd=ROOT, check=True)
    for lid in lids:
        spec_p = next((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))
        rep_p = ROOT / "out" / c / lid / "build_report.json"
        b = json.loads(rep_p.read_text("utf-8"))
        assert b["spec_sha256"] == lv.spec_digest(lv.load_spec(spec_p)), f"DIGEST CHANGED: {c} {lid}"
        r = subprocess.run([PY, "-B", "tools/lv.py", "asr", str(spec_p.relative_to(ROOT))], cwd=ROOT)
        assert r.returncode == 0, f"lv.py asr rc={r.returncode} for {c} {lid}"
    out = subprocess.run([PY, "-B", "audit/review/asr_flags.py", c], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print(out.stderr.strip(), flush=True)
    assert ": 0 câu chưa xem xét" in out.stderr, f"Flags remain in {c}: {out.stdout}\n{out.stderr}"

print("ALL TOC + STAGE 11 ASR FLAGS CLEARED (0/6) & SPEC DIGESTS FRESH!", flush=True)
