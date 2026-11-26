"""Sinh toàn bộ 10 bài CPR (YAML + lab + mong_doi.txt + screen_code/CPR.yaml)."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "cpr"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import cpr_builder  # noqa: E402
import data_a  # noqa: E402
import data_b  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

all_lessons = data_a.lessons() + data_b.lessons()
want = {a.upper() for a in sys.argv[1:]}
ledger = {}
for cfg in all_lessons:
    if want and cfg["id"] not in want:
        continue
    out_p, p_outs, lab_o = cpr_builder.make_c_lesson(cfg, ledger)
    print(f"OK {cfg['id']}: {out_p.relative_to(ROOT)} ({len(p_outs)} prog, lab={len(lab_o.splitlines())} dòng)")

if not want:
    sc_p = ak.write_screen_ledger("CPR", ledger)
    print("Ghi sổ screen_code:", sc_p.relative_to(ROOT), f"({len(ledger)} khối)")
