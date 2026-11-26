import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import lv  # noqa: E402
import up_s9_llm_rl_cv as u  # noqa: E402

for (c, lid), cov in sorted(u.COVERS.items()):
    fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    objs = sp.get("objectives") or []
    kinds = {sc["id"]: sc["kind"] for sc in sp["scenes"]}
    for n, sid in cov:
        k = kinds.get(sid)
        txt = str(objs[n - 1]).strip().lower()
        if txt.startswith(lv.AF2_DO_VERBS) and k not in lv.AF2_DO_SCENES:
            print(f"E51: ({c!r}, {lid!r}) obj={n} {objs[n-1]!r} -> {sid!r} ({k!r}) | avail={[ (sc['id'], sc['kind']) for sc in sp['scenes'] if sc['kind'] in lv.AF2_DO_SCENES ]}")
