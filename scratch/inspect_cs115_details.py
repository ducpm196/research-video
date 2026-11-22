import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for lid in ["L27", "L28", "L33", "L42"]:
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    spec = lv.load_spec(fp)
    print(f"=== {lid} scenes ===")
    for sc in spec["scenes"]:
        if sc["kind"] in ("hook", "intuition", "concept", "practice", "recap") and (lid != "L42" or sc["kind"] in ("hook", "practice", "recap")):
            print(f"  [{sc['id']}] ({sc['kind']}) steps={len(sc['steps'])}")
            for idx, st in enumerate(sc["steps"]):
                if sc["kind"] == "practice" and idx > 0:
                    continue
                if sc["kind"] == "recap" and idx > 0:
                    continue
                print(f"    step#{idx} focus={st.get('focus')} say={st.get('say')!r}")
                if sc["kind"] == "practice":
                    print(f"    show={st.get('show')!r}")
