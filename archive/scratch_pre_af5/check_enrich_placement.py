from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scratch"))

# Parse ENRICH_S8 markers directly from fix_stage8_v3_go.py without executing it
import ast
src = (ROOT / "scratch/fix_stage8_v3_go.py").read_text("utf-8")
tree = ast.parse(src)
enrich_list = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "ENRICH_S8" for t in node.targets):
        enrich_list = ast.literal_eval(node.value)

for rel, sid, n_html, n_say, marker in enrich_list:
    p = ROOT / rel
    if not p.exists():
        lid = p.name[:4]
        p = sorted((ROOT / p.parent).glob(f"{lid}*.yaml"))[0]
    txt = p.read_text("utf-8")
    # 1. YAML parse test
    try:
        d = yaml.safe_load(txt)
    except Exception as e:
        print(f"YAML_ERR {p.relative_to(ROOT)} ({sid}): {e}")
        continue
    # 2. Check marker is inside scene `sid`, NOT another scene!
    found_in = []
    for s in d["scenes"]:
        for ki, st in enumerate(s["steps"]):
            if marker in str(st.get("show", "")):
                found_in.append((s["id"], ki))
    if found_in != [(sid, len(next(s for s in d["scenes"] if s["id"] == sid)["steps"]) - 1)]:
        print(f"MISPLACED {p.relative_to(ROOT)} target={sid}: found_in={found_in}")
