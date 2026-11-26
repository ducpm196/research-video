import ast
import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

DO_VERBS = (
    "viết", "tính", "dựng", "chạy", "cài", "kiểm", "chọn", "thiết kế", "vẽ", "đo",
    "cấu hình", "tạo", "sửa", "gỡ", "áp dụng", "đọc", "so sánh", "đếm", "xác định",
    "triển khai", "chứng minh", "giải", "lập",
)
DO_SCENES = {"check", "practice", "formula", "example"}

COURSES = [
    ("EVT", ROOT / "audit/evt/af2/upgrade_evt.py"),
    ("DEN", ROOT / "audit/den/af2/upgrade_den.py"),
    ("CLD", ROOT / "audit/cld/af2/upgrade_cld.py"),
    ("CLC", ROOT / "audit/clc/af2/upgrade_clc.py"),
    ("SAR", ROOT / "audit/sar/af2/upgrade_sar.py"),
]

issues = 0
total_lessons = 0
for course, path in COURSES:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    covers = None
    lessons = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "COVERS_MAP":
                    covers = ast.literal_eval(node.value)
                elif isinstance(t, ast.Name) and t.id == "LESSONS":
                    lessons = ast.literal_eval(node.value)
    cur = yaml.safe_load((ROOT / f"curriculum/{course.lower()}.yaml").read_text(encoding="utf-8"))
    cur_objs = {b["id"]: b.get("objectives", []) for b in cur["lessons"]}

    for item in lessons:
        lid, _, _, _, sol = item
        total_lessons += 1
        max_len = max((len(ln) for ln in sol.splitlines()), default=0)
        if max_len > 78:
            print(f"[CODE_LONG] {course} {lid}: max_line={max_len}")
            issues += 1
        if len(sol.splitlines()) > 15:
            print(f"[CODE_TALL] {course} {lid}: lines={len(sol.splitlines())}")
            issues += 1

        fp = sorted(glob.glob(str(ROOT / f"lessons/{course.lower()}/{lid}_*.yaml")))[0]
        les = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        sc_kinds = {s["id"]: s.get("kind") for s in les.get("scenes", [])}
        objs = cur_objs[lid]
        cov = covers[lid]
        if len(cov) != len(objs):
            print(f"[LEN_MISMATCH] {course} {lid}: cov={len(cov)} vs objs={len(objs)}")
            issues += 1
            continue
        for idx, sid in cov:
            if sid not in sc_kinds:
                print(f"[MISSING_SCENE] {course} {lid}: {sid} not in {list(sc_kinds)}")
                issues += 1
                continue
            obj = objs[idx - 1].strip().lower()
            is_do = obj.startswith(DO_VERBS)
            kind = sc_kinds[sid]
            valid_do = (sid in DO_SCENES) or (kind == "example")
            if is_do and not valid_do:
                print(f"[E51_DO_MISMATCH] {course} {lid} obj#{idx}='{objs[idx-1]}' -> {sid} ({kind})")
                issues += 1

print(f"Checked {total_lessons} Batch 8B lessons -> issues={issues}")
sys.exit(1 if issues else 0)
