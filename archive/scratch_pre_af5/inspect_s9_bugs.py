import sys
from pathlib import Path
import re

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv


def dump_lesson(course: str, lid: str, kinds=None):
    fp = sorted((ROOT / "lessons" / course).glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    print(f"=== {course.upper()}:{lid} ({fp.name}) ===")
    for sc in sp["scenes"]:
        if kinds and sc["id"] not in kinds and sc["kind"] not in kinds:
            continue
        print(f"  [{sc['id']}] ({sc['kind']}) title={sc['title']}")
        for idx, st in enumerate(sc["steps"]):
            sh = st.get("show") or ""
            say = st.get("say") or ""
            print(f"    step#{idx}: focus={st.get('focus')} show={sh!r}")
            print(f"      say={say!r}")


for c, l, k in [
    ("aif", "L01", {"example", "check"}),
    ("aif", "L04", {"example", "intuition"}),
    ("aif", "L05", {"sym", "example"}),
    ("aif", "L08", {"sym", "example", "intuition"}),
    ("aif", "L13", {"example", "intuition", "recap"}),
    ("aif", "L14", {"stage5", "check"}),
]:
    dump_lesson(c, l, k)
