"""In chỉ số khung (frames/NNNNN.png) của các step: step_frames.py L01 dot.2 quiz.1 …"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

COURSE = __import__("os").environ.get("LV_COURSE", "cs115")  # khoá: LV_COURSE=cs112

lid, want = sys.argv[1], set(sys.argv[2:])
sp = lv.load_spec(next((ROOT / "lessons" / COURSE).glob(lid + "_*.yaml")))
i = 0
for sc in sp["scenes"]:
    for ki, st in enumerate(sc["steps"]):
        n = len(lv.sentences(st["say"]))
        if f"{sc['id']}.{ki}" in want:
            print(f"{sc['id']}.{ki}", list(range(i, i + n)))
        i += n
