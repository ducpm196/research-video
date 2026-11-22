import json, pathlib, sys
sys.path.insert(0, "tools")
import lv

stale = []
for p in sorted(pathlib.Path("lessons").glob("*/*.yaml")):
    c = p.parent.name.upper()
    lid = p.name.split("_")[0]
    sp = lv.load_spec(p)
    sd = lv.spec_digest(sp)
    fr = lv.build_frames(sp)
    td = lv.tts_digest(fr)
    br = pathlib.Path("out") / c / lid / "build_report.json"
    if not br.exists():
        stale.append((c, lid, "NO_BUILD"))
        continue
    j = json.loads(br.read_text("utf-8"))
    reasons = []
    if j.get("spec_sha256") != sd:
        reasons.append("SPEC")
    if j.get("tts_sha256") != td:
        reasons.append("TTS")
    if reasons:
        stale.append((c, lid, "+".join(reasons), str(p)))

print(f"TOTAL_STALE={len(stale)}")
for x in stale:
    print(x)
