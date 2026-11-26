from pathlib import Path
import yaml

targets = [
    ("rbm", "L00", ["recap"]),
    ("rbm", "L13", ["recap"]),
    ("esy", "L02", ["isr"]),
    ("esy", "L03", ["sym", "pwm", "pitfalls"]),
    ("esy", "L07", ["speed"]),
    ("esy", "L08", ["sym", "i2c"]),
    ("esy", "L15", ["stage5"]),
    ("bch", "L00", ["prereq"]),
    ("bch", "L01", ["sym"]),
    ("bch", "L03", ["sym"]),
    ("bch", "L04", ["pitfalls"]),
    ("bch", "L07", ["sym"]),
    ("bch", "L10", ["sym", "recap"]),
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
