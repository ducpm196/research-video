"""Verify lint on the 6 touched LLM/RLN/CVI lessons + audit all Stage 9 & Stage 8 appended notes' focus[-1]."""
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

SIX = [
    "lessons/rln/L13_hanh_trinh_atari.yaml",
    "lessons/llm/L14_hanh_trinh_mo_rong.yaml",
    "lessons/rln/L04_monte_carlo_td.yaml",
    "lessons/cvi/L03_hieu_chuan_camera.yaml",
    "lessons/rln/L02_lap_chinh_sach.yaml",
    "lessons/rln/L11_khai_thac_phan_thuong.yaml",
]
for rel in SIX:
    print(">>> LINT", rel, flush=True)
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", rel], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {rel}"

# Check any step across Stage 9 & Stage 8 ending with `<p class="note"><b>` where focus[-1] != len(units)
COURSES = ("cs115", "aif", "irs", "agt", "llm", "rln", "cvi", "dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar")
suspects = []
for c in COURSES:
    for p in sorted((ROOT / f"lessons/{c}").glob("L*.yaml")):
        d = yaml.safe_load(p.read_text("utf-8"))
        for sc in d.get("scenes", []):
            if sc["id"] in ("recap", "practice", "hook", "prereq", "pitfalls", "quiz"):
                continue
            for ki, st in enumerate(sc["steps"]):
                show = str(st.get("show", "")).strip()
                if '<p class="note"><b>' in show and show.endswith("</p>"):
                    units = lv.html_units(show)
                    foc = st.get("focus")
                    if isinstance(foc, list) and foc and units:
                        last_f = foc[-1]
                        # check last_f highlights the final unit len(units)
                        if isinstance(last_f, int) and last_f != len(units) and last_f != 0:
                            suspects.append((c.upper(), d["id"], sc["id"], ki, f"last_f={last_f} != len(units)={len(units)}"))
print("SUSPECTS:", len(suspects))
for x in suspects:
    print(" ", x)
