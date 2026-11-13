"""In (cảnh.step → số khung đầu) của một bài FND để mở đúng khung PNG: frames_index.py L00 → out/FND/L00/frames/NNNNN.png."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

lid = sys.argv[1].upper()
sp = lv.load_spec(next((ROOT / "lessons" / "fnd").glob(lid + "_*.yaml")))
i = 0
out = []
for sc in sp["scenes"]:
    for k, st in enumerate(sc["steps"]):
        n = len(lv.sentences(st["say"]))
        out.append(f"{sc['id']}.{k}:{i:05d}")
        i += n
print(" ".join(out))
