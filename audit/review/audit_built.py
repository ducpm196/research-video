"""Rà soát mọi bài: lint lại bằng bộ luật hiện hành; với bài đã dựng, đọc build_report (giọng) và asr_report (câu chưa xem xét).
Chạy: .venv/Scripts/python audit/review/audit_built.py → bảng TSV audit/review/built_status.tsv và tóm tắt theo khoá."""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
PY = str(ROOT / ".venv" / "Scripts" / "python")
rows = []
for d in sorted((ROOT / "lessons").iterdir()):
    if not d.is_dir() or d.name.startswith("_"):
        continue
    for f in sorted(d.glob("L*_*.yaml")):
        out = subprocess.run([PY, str(ROOT / "tools" / "lv.py"), "lint", str(f)], capture_output=True, text=True, encoding="utf-8").stdout
        m = re.search(r"lint: (\d+) FAIL, (\d+) WARN", out)
        issues = [l for l in out.splitlines() if l.startswith("[FAIL]") or l.startswith("[WARN]")]
        lid = f.name.split("_")[0]
        od = ROOT / "out" / d.name.upper() / lid
        rep = od / "build_report.json"
        built = rep.exists()
        voices = ""
        if built:
            voices = ",".join(json.loads(rep.read_text(encoding="utf-8")).get("voices") or [])
        asr = od / "asr_report.md"
        unrev = ""
        if asr.exists():
            mm = re.search(r"chưa xem xét[^0-9]*(\d+)", asr.read_text(encoding="utf-8"))
            unrev = mm.group(1) if mm else "?"
        stale = built and f.stat().st_mtime > rep.stat().st_mtime
        rows.append((d.name.upper(), lid, m.group(1) if m else "?", m.group(2) if m else "?", built, stale, voices, unrev, " | ".join(issues)[:400]))
        print(d.name.upper(), lid, rows[-1][2], rows[-1][3], flush=True)
tsv = ROOT / "audit" / "review" / "built_status.tsv"
tsv.write_text("course\tid\tfail\twarn\tbuilt\tspec_newer\tvoices\tasr_unreviewed\tissues\n" + "\n".join("\t".join(map(str, r)) for r in rows), encoding="utf-8")
agg = defaultdict(lambda: [0, 0, 0, 0, 0, 0, set()])
for c, lid, fa, wa, b, st, v, u, _ in rows:
    a = agg[c]
    a[0] += 1; a[1] += fa != "0"; a[2] += wa != "0"; a[3] += b; a[4] += st; a[5] += int(u) if u.isdigit() else 0
    a[6] |= set(v.split(",")) - {""}
print("TÓM TẮT: khoá bài có_FAIL có_WARN đã_dựng đặc_tả_mới_hơn ASR_chưa_xem giọng")
for c, a in agg.items():
    print(c, *a[:6], sorted(a[6]))
