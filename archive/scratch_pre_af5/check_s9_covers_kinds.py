import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

AF2_DO_VERBS = (
    "viết", "tính", "dựng", "chạy", "cài", "kiểm", "chọn", "thiết kế", "vẽ", "đo",
    "cấu hình", "tạo", "sửa", "gỡ", "áp dụng", "đọc", "so sánh", "đếm", "xác định",
    "triển khai", "chứng minh", "giải", "lập",
)
AF2_DO_SCENES = {"example", "check", "practice", "formula"}

for c in ["aif", "irs", "agt", "llm", "rln", "cvi"]:
    print(f"=== {c.upper()} ===")
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c}/L*.yaml"))):
        d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        lid = d["id"]
        objs = d.get("objectives", [])
        scs = {s["id"]: s.get("kind") for s in d.get("scenes", [])}
        cov = {x["objective"]: x["scene"] for x in d.get("covers", [])}
        for idx, o in enumerate(objs, 1):
            cur = cov.get(idx)
            is_do = str(o).strip().lower().startswith(AF2_DO_VERBS)
            kind = scs.get(cur)
            if is_do and kind not in AF2_DO_SCENES:
                print(f"  [E51_NOW] {lid} obj{idx} cur={cur}({kind}) :: {o}")
        print(f"  {lid}: cov={cov} | scenes={scs}")
