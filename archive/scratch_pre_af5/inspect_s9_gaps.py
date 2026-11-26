import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import lv  # noqa: E402
import ast_p1  # noqa: E402

MED_SPW, P5_SPW = 0.331, 0.305
S9 = ["IRS", "LLM", "RLN", "AGT", "CVI", "AIF", "CS115"]

for c in S9:
    tight, leaks, no_p9, cang, ast_diff = [], [], [], [], []
    err = warn = 0
    for yp in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")):
        lid = yp.stem.split("_")[0]
        if c == "CS115" and int(lid[1:]) < 22:
            continue
        raw = yp.read_text(encoding="utf-8")
        sp = lv.load_spec(yp)
        with redirect_stdout(io.StringIO()):
            r = lv.lint(sp, quiet=True)
        err += len(r.errors)
        warn += len(r.warnings)
        w = sum(len((s.get("say") or "").split()) for sc in sp["scenes"] for s in sc["steps"])
        pauses = sum(float(s.get("pause", 0) or 0) for sc in sp["scenes"] for s in sc["steps"])
        est_p5 = w * P5_SPW + pauses
        bp = ROOT / "out" / c.lower() / lid / "build_report.json"
        built = json.loads(bp.read_text(encoding="utf-8")).get("timeline_seconds") if bp.exists() else None
        if w < 1620 or est_p5 < 540 or (built is not None and built < 540):
            tight.append(f"{lid}({w}w,p5={est_p5:.0f}s)")
        recap_show = " ".join((s.get("show") or "") for sc in sp["scenes"] if sc["id"] == "recap" for s in sc["steps"])
        if "Hai mức quy mô" not in recap_show and "hai mức quy mô" not in recap_show.lower():
            no_p9.append(lid)
        if re.search(r"\bcàng\b", raw, re.I):
            cang.append(lid)
        # check P8 pre-pause leak & ast_p1 sync
        prac = next((sc for sc in sp["scenes"] if sc["id"] == "practice"), None)
        sol_p = ROOT / "labs" / c / lid / "loi_giai.py"
        exp_p = ROOT / "labs" / c / lid / "mong_doi.txt"
        if prac and sol_p.exists() and exp_p.exists():
            steps = prac["steps"]
            p_idx = next((i for i, s in enumerate(steps) if s.get("pause")), None)
            sol = sol_p.read_text(encoding="utf-8")
            exp = exp_p.read_text(encoding="utf-8").strip()
            if p_idx is None or any(exp in (st.get("show") or "") or sol.splitlines()[0] in (st.get("show") or "") for st in steps[:p_idx + 1]):
                leaks.append(lid)
            exp_rows = [k for k, _ in ast_p1.build_read_rows(sol)]
            tbl_html = " ".join((st.get("show") or "") for st in steps if "viết trong mã" in (st.get("show") or ""))
            actual_rows = re.findall(r"<tr><td><code>(.*?)</code></td>", tbl_html)
            import html
            actual_clean = [html.unescape(x) for x in actual_rows]
            if actual_clean != exp_rows:
                ast_diff.append(lid)
    print(f"=== {c} === lint FAIL={err} WARN={warn}")
    print(f"  tight(<1620w/p5): {len(tight)} -> {', '.join(tight)}")
    print(f"  no_P9_recap: {no_p9} | P8_leaks: {leaks} | ast_diff: {len(ast_diff)} {ast_diff[:6]} | cang: {cang}")
