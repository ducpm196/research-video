"""Inspect Stage 8 Batch 8B (EVT, DEN, CLD, CLC, SAR) metrics."""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

for c in ("EVT", "DEN", "CLD", "CLC", "SAR"):
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c.lower()}.yaml")
    print(f"\n=== {c} ===", flush=True)
    for les in cur["lessons"]:
        lid = les["id"]
        fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        errs = [e for e in res.errors]
        warns = [w0 for w0 in res.warnings]
        cang = []
        for idx, sc in enumerate(sp["scenes"]):
            for st in sc["steps"]:
                for fld in ("say", "show"):
                    v = st.get(fld)
                    txts = [v] if isinstance(v, str) else ([str(x) for x in v] if isinstance(v, list) else [])
                    for t in txts:
                        if "càng " in t.lower():
                            cang.append(f"sc{idx}({sc.get('id')}).{fld}: {t[:80]}")
        ast_n = sum(1 for sc in sp["scenes"] for st in sc["steps"] if "Bảng đọc nhanh đoạn mã" in str(st.get("show") or ""))
        recap_2m = any("Hai mức quy mô" in str(st.get("show") or "") or "hai mức quy mô" in str(st.get("say") or "").lower()
                       for sc in sp["scenes"] if sc.get("id") == "recap" for st in sc["steps"])
        print(f"  {lid}: w={w:4d} E={len(errs)} W={len(warns)} ast={ast_n} 2m={int(recap_2m)}", flush=True)
        if errs or warns:
            print(f"       lint: E={errs[:3]} W={warns[:3]}", flush=True)
        for cg in cang:
            print(f"       CANG: {cg}", flush=True)
