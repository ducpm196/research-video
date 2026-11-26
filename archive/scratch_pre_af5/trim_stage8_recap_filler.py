import collections
import pathlib
import sys

import yaml

sys.path.insert(0, "tools")
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(r"D:/research-video")
COURSES = ["clc", "cld", "den", "evt", "sar"]
changed = []

for cname in COURSES:
    sents = collections.Counter()
    paths = sorted((ROOT / "lessons" / cname).glob("L*.yaml"))
    for p in paths:
        sp = lv.load_spec(p)
        for sc in sp.get("scenes", []):
            if sc.get("id") == "recap":
                for st in sc.get("steps", []):
                    for s in lv.sentences(st.get("say", "")):
                        sents[s] += 1
    bad = {s for s, n in sents.items() if n >= 3 and s != "Hẹn gặp bạn ở bài tiếp theo."}

    # Trim matching lessons and CLD tpl files cleanly via ruamel/yaml or text replacement on say line
    targets = list(paths)
    if cname == "cld":
        targets += sorted((ROOT / "audit/cld/src").glob("L*.tpl.yaml"))

    for p in targets:
        txt = p.read_text(encoding="utf-8")
        data = yaml.safe_load(txt)
        file_dirty = False
        for sc in data.get("scenes", []):
            if sc.get("id") == "recap":
                for st in sc.get("steps", []):
                    say = st.get("say", "")
                    ss = lv.sentences(say)
                    if not any(s in bad for s in ss):
                        continue
                    kept = [s for s in ss if s not in bad]
                    new_say = " ".join(kept)
                    assert new_say.strip() and say in txt, f"Exact match failed in {p}"
                    txt = txt.replace("say: " + say + "\n", "say: " + new_say + "\n", 1)
                    if "focus" in st and len(st["focus"]) == len(ss):
                        # Trim focus entries aligned with kept sentences
                        kept_idx = [i for i, s in enumerate(ss) if s not in bad]
                        new_foc = [st["focus"][i] for i in kept_idx]
                        old_foc_block = "focus:\n" + "\n".join(
                            f"    - {yaml.safe_dump(x, default_flow_style=True).strip().removesuffix('...')}"
                            for x in st["focus"]
                        )
                        # Simpler: inspect if any step besides DEN L10 had focus
                        print(f"NOTE focus on {p.name}: {len(ss)}->{len(kept)}")
                        st["focus"] = new_foc
                        txt = txt.replace(say, new_say)  # fallback ensure
                    file_dirty = True
        if file_dirty:
            # Verify valid YAML & sentence count
            data2 = yaml.safe_load(txt)
            p.write_text(txt, encoding="utf-8")
            changed.append(str(p.relative_to(ROOT)).replace("\\", "/"))

print(f"Updated {len(changed)} files:")
for c in changed:
    print(" ", c)
