"""Inspect Stage 8 Batch 8A (DAN, DSC, MLO) metrics safely (no side-effect imports)."""
import ast
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

up_src = (ROOT / "audit" / "s9_11" / "up_s9_data_ai.py").read_text(encoding="utf-8")
tree = ast.parse(up_src)
COVERS = None
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], "id", "") == "COVERS":
        COVERS = ast.literal_eval(node.value)
        break

for c in ("DAN", "DSC", "MLO"):
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c.lower()}.yaml")
    print(f"\n=== {c} ===", flush=True)
    for les in cur["lessons"]:
        lid = les["id"]
        fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        errs = list(res.errors)
        warns = list(res.warnings)
        cang = []
        for idx, sc in enumerate(sp["scenes"]):
            for st in sc["steps"]:
                for fld in ("say", "show"):
                    v = st.get(fld)
                    txts = [v] if isinstance(v, str) else ([str(x) for x in v] if isinstance(v, list) else [])
                    for t in txts:
                        if re.search(r"\bcàng\b", t, re.I):
                            cang.append(f"sc{idx}({sc.get('id')}).{fld}: {t[:100]}")
        ast_n = sum(1 for sc in sp["scenes"] for st in sc["steps"] if "Bảng đọc nhanh đoạn mã" in str(st.get("show") or ""))
        recap_2m = any("Hai mức quy mô" in str(st.get("show") or "") or "hai mức quy mô" in str(st.get("say") or "").lower()
                       for sc in sp["scenes"] if sc.get("id") == "recap" for st in sc["steps"])
        cov = COVERS[c][lid]
        print(f"  {lid}: w={w:4d} E={len(errs)} W={len(warns)} ast={ast_n} 2m={int(recap_2m)} cov={cov}", flush=True)
        if errs or warns:
            print(f"       lint: E={errs[:3]} W={warns[:3]}", flush=True)
        for cg in cang:
            print(f"       CANG: {cg}", flush=True)
