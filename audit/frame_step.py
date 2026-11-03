"""Đổi (khoá, bài, khung) → cảnh.step: frame_step.py audit/layout_CS115.tsv CS115 → in bài, cảnh.step, các khung."""
import sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools")); sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
want = defaultdict(set)
for ln in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if ln.strip():
        lid, i, _ = ln.split("\t"); want[lid].add(int(i))
for lid, fs in sorted(want.items()):
    sp = lv.load_spec(next((ROOT / "lessons" / sys.argv[2].lower()).glob(lid + "_*.yaml")))
    i = 0
    for sc in sp["scenes"]:
        for k, st in enumerate(sc["steps"]):
            n = len(lv.sentences(st["say"]))
            hit = sorted(f for f in fs if i <= f < i + n)
            if hit:
                print(lid, f"{sc['id']}.{k}", hit, "clear" if st.get("clear") else "")
            i += n
