from pathlib import Path
import yaml

targets = [
    ("gfx", "L13", ["stage4"]),
    ("esy", "L05", ["recap"]),
    ("esy", "L06", ["sym"]),
    ("esy", "L09", ["sym", "pitfalls"]),
    ("esy", "L10", ["sym", "pitfalls"]),
    ("esy", "L11", ["sym", "pitfalls", "queue"]),
    ("esy", "L14", ["sym", "boot"]),
    ("bch", "L03", ["check"]),
    ("bch", "L04", ["check"]),
    ("bch", "L06", ["example", "check"]),
    ("bch", "L07", ["example", "check"]),
    ("bch", "L12", ["stage1", "stage4", "stage5"]),
]

for course, lid, sids in targets:
    p = next(Path("lessons", course).glob(f"{lid}_*.yaml"))
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    print(f"=== {course.upper()} {p.name} ===")
    for sc in doc["scenes"]:
        if sc["id"] in sids:
            print(f"  -- scene {sc['id']} (kind={sc.get('kind')}) --")
            for idx, st in enumerate(sc["steps"]):
                print(f"    step {idx}: checks={st.get('checks')} focus={st.get('focus')}")
                print("      SHOW:", repr(st.get("show", "")))
                print("      SAY:", repr(st.get("say", "")))
