"""Sinh 5 bài dự án PRJ L00–L04 (YAML + lab + mong_doi.txt + screen_code/PRJ.yaml)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "prj"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import data  # noqa: E402
import prj_builder  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

want = {a.upper() for a in sys.argv[1:]}
ledger = {}
for cfg in data.lessons():
    if want and cfg["id"] not in want:
        continue
    out_p, p_outs, lab_o = prj_builder.make_prj_lesson(cfg, ledger)
    print(f"OK {cfg['id']}: {out_p.relative_to(ROOT)} ({len(p_outs)} prog, lab={len(lab_o.splitlines())} dòng)")

if not want:
    sc_p = ak.write_screen_ledger("PRJ", ledger)
    print("Ghi sổ screen_code:", sc_p.relative_to(ROOT), f"({len(ledger)} khối)")
