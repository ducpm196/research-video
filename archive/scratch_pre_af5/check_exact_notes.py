import ast
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "scratch/fix_stage8_v3_go.py").read_text("utf-8")
tree = ast.parse(src)
enrich_list = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "ENRICH_S8" for t in node.targets):
        enrich_list = ast.literal_eval(node.value)

# First fix MLO L03 line 71 YAML syntax error if still present
p_mlo3 = ROOT / "lessons/mlo/L03_kiem_thu_he_ml.yaml"
s3 = p_mlo3.read_text("utf-8")
bad_line = '    <p class="note"><b>Tích hợp liên tục (CI):</b> quy trình tự động chạy toàn bộ kiểm thử dữ liệu và mô hình mỗi khi gộp mã mới gọi là <b>CI</b> (Continuous Integration).</p>\n'
if bad_line in s3:
    p_mlo3.write_text(s3.replace(bad_line, ""), "utf-8")
    print("FIXED MLO L03 line 71 YAML syntax error")

for rel, sid, n_html, n_say, _ in enrich_list:
    p = ROOT / rel
    if not p.exists():
        lid = p.name[:4]
        p = sorted((ROOT / p.parent).glob(f"{lid}*.yaml"))[0]
    txt = p.read_text("utf-8")
    d = yaml.safe_load(txt)
    prefix = n_html[:35]
    found_in = []
    for s in d["scenes"]:
        for ki, st in enumerate(s["steps"]):
            if prefix in str(st.get("show", "")):
                found_in.append((s["id"], ki))
    target_idx = len(next(s for s in d["scenes"] if s["id"] == sid)["steps"]) - 1
    if found_in and found_in != [(sid, target_idx)]:
        print(f"WRONG PLACE {p.relative_to(ROOT)} target=({sid},{target_idx}) actual={found_in} prefix={prefix!r}")
    elif not found_in:
        print(f"MISSING {p.relative_to(ROOT)} target=({sid},{target_idx}) prefix={prefix!r}")
    else:
        print(f"OK {p.relative_to(ROOT)} target=({sid},{target_idx})")
