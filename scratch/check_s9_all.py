import ast
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

def check_mod(path_str, is_llm_rl_cv):
    tree = ast.parse((ROOT / path_str).read_text(encoding="utf-8"))
    covers = data = None
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == "COVERS":
                    covers = ast.literal_eval(n.value)
                elif isinstance(t, ast.Name) and t.id == "DATA":
                    data = ast.literal_eval(n.value)
    issues = 0
    for c, items in data.items():
        if not is_llm_rl_cv and c != "AIF":
            continue
        for item in items:
            lid, hint, de, sol = item
            mlen = max((len(x) for x in sol.splitlines()), default=0)
            if mlen > 78:
                print(f"[LONG] {c} {lid}: max={mlen}")
                issues += 1
            if len(sol.splitlines()) > 15:
                print(f"[TALL] {c} {lid}: lines={len(sol.splitlines())}")
                issues += 1
            cov = covers[(c, lid)] if is_llm_rl_cv else covers[c][lid]
            fp = sorted(glob.glob(str(ROOT / f"lessons/{c.lower()}/{lid}_*.yaml")))[0]
            les = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
            sc_k = {s["id"]: s.get("kind") for s in les.get("scenes", [])}
            objs = les.get("objectives", [])
            seen = set()
            for idx, sid in cov:
                seen.add(idx)
                if sid not in sc_k:
                    print(f"[BAD_SC] {c} {lid} -> {sid}")
                    issues += 1
                    continue
                txt = str(objs[idx - 1]).strip().lower()
                is_do = txt.startswith(AF2_DO_VERBS) and not txt.startswith("giải thích")
                if is_do and sc_k[sid] not in AF2_DO_SCENES:
                    print(f"[E51] {c} {lid} obj{idx} '{objs[idx-1]}' -> {sid}({sc_k[sid]})")
                    issues += 1
            if sorted(seen) != list(range(1, len(objs) + 1)):
                print(f"[MISSING_OBJ] {c} {lid}: {seen} vs 1..{len(objs)}")
                issues += 1
    print(f"{path_str}: issues={issues}")
    return issues

tot = check_mod("audit/s9_11/up_s9_data_ai.py", False)
tot += check_mod("audit/s9_11/up_s9_llm_rl_cv.py", True)
sys.exit(1 if tot else 0)
