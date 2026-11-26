from pathlib import Path
import yaml

def dump_scene(course, lid, scene_ids):
    p = next(Path("lessons", course).glob(f"{lid}_*.yaml"))
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    print(f"\n=== {course.upper()} {p.name} covers={doc.get('covers')} ===")
    for i, obj in enumerate(doc.get("objectives", []), 1):
        print(f"  obj{i}: {obj}")
    for sc in doc.get("scenes", []):
        if sc["id"] in scene_ids:
            print(f"  --- scene {sc['id']} (kind={sc.get('kind')}) ---")
            for j, st in enumerate(sc.get("steps", [])):
                sh = (st.get("show") or "").strip().replace("\n", " | ")
                sy = (st.get("say") or "").strip()
                fc = st.get("focus")
                chk = st.get("checks")
                print(f"    step {j}: focus={fc} checks={chk}")
                print(f"      show={sh[:350]}")
                print(f"      say={sy[:300]}")

dump_scene("rbm", "L00", ["recap"])
dump_scene("rbm", "L10", ["ponly", "addi", "addd", "sym"])
dump_scene("rbm", "L13", ["recap"])
dump_scene("rob", "L03", ["pitfalls"])
dump_scene("esy", "L02", ["sym", "isr"])
dump_scene("esy", "L03", ["sym", "pwm", "pitfalls"])
dump_scene("esy", "L07", ["sym", "speed", "example"])
dump_scene("esy", "L08", ["sym", "i2c", "example"])
dump_scene("esy", "L15", ["stage5", "check", "quiz", "practice"])
dump_scene("bch", "L00", ["prereq", "sym"])
dump_scene("bch", "L01", ["sym", "pitfalls"])
dump_scene("bch", "L03", ["sym", "check", "practice", "quiz"])
dump_scene("bch", "L04", ["sym", "check", "pitfalls"])
dump_scene("bch", "L06", ["sym", "example", "check", "pitfalls"])
dump_scene("bch", "L07", ["prereq", "sym", "check", "example", "pitfalls"])
dump_scene("bch", "L10", ["sym", "pitfalls", "recap"])
dump_scene("bch", "L12", ["stage4", "stage5", "check", "quiz", "recap"])
