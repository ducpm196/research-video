import glob, os, re, yaml

def words_in(data):
    w = 0
    for sc in data.get("scenes", []):
        for st in sc.get("steps", []):
            say = st.get("say", "") or ""
            w += len(say.split())
    return w

print("=== BATCH 8B (EVT, DEN, CLD, CLC, SAR) ===")
for c in ["evt", "den", "cld", "clc", "sar"]:
    paths = sorted(glob.glob(f"lessons/{c}/L*.yaml"))
    for p in paths:
        txt = open(p, encoding="utf-8").read()
        data = yaml.safe_load(txt)
        w = words_in(data)
        cang = txt.count("càng ")
        hmqm_show = "Hai mức quy mô" in txt
        recap = [sc for sc in data.get("scenes", []) if sc.get("id") == "recap"]
        hmqm_say = False
        recap_focus = None
        if recap:
            steps = recap[0].get("steps", [])
            if steps:
                last = steps[-1]
                recap_focus = last.get("focus")
                hmqm_say = ("quy mô" in (last.get("say") or "").lower() or "hai mức" in (last.get("say") or "").lower())
        flags = []
        if w < 1665: flags.append(f"w={w}")
        if cang: flags.append(f"cang={cang}")
        if not hmqm_show: flags.append("NO_HMQM_SHOW")
        if not hmqm_say: flags.append("NO_HMQM_SAY")
        if flags:
            print(f"{c.upper()} {os.path.basename(p)[:3]}: w={w} focus={recap_focus} {' '.join(flags)}")
