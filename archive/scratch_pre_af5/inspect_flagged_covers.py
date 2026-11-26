import ast
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

PAIRS = [
    ("aif", "L02"), ("aif", "L03"), ("aif", "L04"), ("aif", "L09"), ("aif", "L12"), ("aif", "L13"), ("aif", "L14"),
    ("irs", "L00"), ("irs", "L02"), ("irs", "L04"), ("irs", "L05"), ("irs", "L07"), ("irs", "L08"), ("irs", "L10"), ("irs", "L12"), ("irs", "L13"),
    ("agt", "L01"), ("agt", "L02"), ("agt", "L03"), ("agt", "L04"), ("agt", "L05"), ("agt", "L07"), ("agt", "L11"), ("agt", "L12"),
    ("llm", "L01"), ("llm", "L03"), ("llm", "L04"), ("llm", "L07"), ("llm", "L11"),
    ("rln", "L00"), ("rln", "L02"), ("rln", "L03"), ("rln", "L04"), ("rln", "L06"), ("rln", "L11"), ("rln", "L12"), ("rln", "L13"),
    ("cvi", "L00"), ("cvi", "L01"), ("cvi", "L02"), ("cvi", "L03"), ("cvi", "L04"), ("cvi", "L05"), ("cvi", "L06"), ("cvi", "L08"), ("cvi", "L09"), ("cvi", "L10"), ("cvi", "L11"), ("cvi", "L12"),
]

import glob
for c, lid in PAIRS:
    fp = sorted(glob.glob(str(ROOT / f"lessons/{c}/{lid}_*.yaml")))[0]
    d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
    objs = d.get("objectives", [])
    scs = [(s["id"], s.get("kind"), s.get("title", "")) for s in d.get("scenes", [])]
    cov = {x["objective"]: x["scene"] for x in d.get("covers", [])}
    print(f"=== {c.upper()} {lid} cov={cov} ===")
    for i, o in enumerate(objs, 1):
        do_flag = "DO" if str(o).strip().lower().startswith(AF2_DO_VERBS) else "CONCEPT"
        print(f"  obj{i} [{do_flag}]: {o}")
    print("  scenes:", [(sid, k, t[:30]) for sid, k, t in scs if sid not in ("hook", "prereq", "recap")])
