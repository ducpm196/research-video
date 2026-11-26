import ast, sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

up_src = (ROOT / "audit" / "s9_11" / "up_s9_data_ai.py").read_text(encoding="utf-8")
tree = ast.parse(up_src)
COVERS = None
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", "") == "COVERS":
        COVERS = ast.literal_eval(n.value)
        break

do_verbs = getattr(lv, "AF2_DO_VERBS", None) or getattr(lv, "_AF2_DO_VERBS", ())
do_scenes = getattr(lv, "AF2_DO_SCENES", None) or {"example", "check", "practice"}
print("DO_VERBS:", do_verbs)
print("DO_SCENES:", do_scenes)

for c in ("DAN", "DSC", "MLO"):
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c.lower()}.yaml")
    for les in cur["lessons"]:
        lid = les["id"]
        fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        kind_by_id = {sc["id"]: sc["kind"] for sc in sp["scenes"]}
        for obj_i, sc_id in COVERS[c][lid]:
            obj_txt = les["objectives"][obj_i - 1]
            sc_kind = kind_by_id.get(sc_id, "MISSING")
            is_do = any(obj_txt.lower().startswith(v) for v in do_verbs)
            if sc_kind == "MISSING" or (is_do and sc_kind not in do_scenes):
                print(f"BAD E51 {c} {lid} obj{obj_i}='{obj_txt}' -> sc_id={sc_id} (kind={sc_kind})")
