import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    spec = lv.load_spec(fp)
    words = sum(len((st.get("say") or "").split()) for sc in spec["scenes"] for st in sc["steps"])
    if words < 1645:
        need = 1650 - words
        in_ai = [sc for sc in spec["scenes"] if sc["id"] == "in_ai"]
        print(f"{lid}: words={words}, need=+{need}, has_in_ai={bool(in_ai)}, in_ai_focus={in_ai[0]['steps'][-1].get('focus') if in_ai else None}")
        if lid in ("L27", "L28", "L33") or (28 <= i <= 39):
            hk = spec["scenes"][0]["steps"][0]
            print(f"   hook focus={hk.get('focus')} sents={len(lv.sentences(hk['say']))} show={hk['show']!r}")
