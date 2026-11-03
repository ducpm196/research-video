"""Sinh bảng HIỆN TRẠNG từ dữ liệu thật — không gõ tay số liệu vào ROADMAP (lỗi thật 2026-10-30: ROADMAP ghi “94 bài có video”,
“xếp hàng sau …” trong khi nhiều khoá đã dựng xong).
Nguồn: curriculum/*.yaml (số bài), lessons/<c>/ (đặc tả), out/<C>/<id>/build_report.json (đã dựng, thời lượng, giọng),
audit/review/audit_all.tsv (lint, STALE, ASR — chạy audit_all.py trước), bộ kiểm độc lập audit/<c>/verify_*.py (exit 0 = PASS).
Chạy: .venv/Scripts/python audit/review/audit_all.py && .venv/Scripts/python audit/review/status_report.py
Ghi: curriculum/STATUS.md (sinh tự động — không sửa tay)."""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
PY = str(ROOT / ".venv" / "Scripts" / "python")
# bộ kiểm độc lập của các khoá không theo mẫu audit/<c>/verify_<c>.py
EXTRA = {"CS115": ["audit/verify_cs115_tex.py", "audit/verify_cs115_l44.py"], "CS112": ["audit/cs112/verify_cs112.py", "audit/cs112/verify_cs112_p2.py"]}


def verifiers(C):
    return EXTRA.get(C) or sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "audit" / C.lower()).glob("verify_*.py"))


def run_verifier(rel):
    try:
        p = subprocess.run([PY, str(ROOT / rel)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=1200, cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return "quá giờ"
    out = p.stdout
    m = (re.findall(r"(\d+)/(\d+) PASS", out) or [None])[-1]
    if m:
        cnt = f"{m[0]}/{m[1]}"
    elif (m2 := re.findall(r"TỔNG: (\d+) PASS · (\d+) FAIL", out)):
        a, b = map(int, m2[-1]); cnt = f"{a}/{a + b}"
    elif (m3 := re.findall(r"TOTAL=(\d+) PASS=(\d+)", out)):
        t, a = m3[-1]; cnt = f"{a}/{t}"
    elif (m4 := re.findall(r"tổng: \{'PASS': (\d+), 'FIX': (\d+), 'FAIL': (\d+)\}", out)):
        a, f, b = map(int, m4[-1]); cnt = f"{a + f}/{a + f + b}"
    else:
        cnt = "?"
    return f"{cnt} {'PASS' if p.returncode == 0 else 'FAIL'}"


audit = {}
tsv = ROOT / "audit" / "review" / "audit_all.tsv"
for line in tsv.read_text(encoding="utf-8").splitlines()[1:]:
    c, lid, state, probs = (line.split("\t") + [""] * 4)[:4]
    audit[(c, lid)] = (state, probs)
stamp = datetime.datetime.fromtimestamp(tsv.stat().st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

rows, tot = [], dict(planned=0, spec=0, done=0, minutes=0.0)
skip_verify = "--no-verify" in sys.argv
for cp in sorted((ROOT / "curriculum").glob("*.yaml")):
    cur = yaml.safe_load(cp.read_text(encoding="utf-8")) or {}
    C = str(cur.get("course") or "")
    if not C:
        continue
    les = cur.get("lessons", [])
    specs = [l for l in les if l.get("spec") and (ROOT / l["spec"]).exists()]
    m = re.search(r"—\s*\S+\s*·\s*(.+)", cp.read_text(encoding="utf-8").splitlines()[0])
    series = m.group(1).strip() if m else ""
    if specs:
        series = str(yaml.safe_load((ROOT / specs[0]["spec"]).read_text(encoding="utf-8")).get("series", "")).split("·", 1)[-1].strip()
    done, minutes, voices, issues = 0, 0.0, set(), []
    for l in les:
        if not (l.get("spec") and (ROOT / l["spec"]).exists()):
            continue                      # bài mới ở mức giáo án: chưa có đặc tả, không phải lỗi
        st, probs = audit.get((C, str(l["id"])), ("?", "lỗi: chưa có trong audit_all.tsv"))
        rep = ROOT / "out" / C / str(l["id"]) / "build_report.json"
        if st == "đã dựng" and not probs:
            done += 1
            b = json.loads(rep.read_text(encoding="utf-8"))
            minutes += float(b.get("timeline_seconds") or 0) / 60
            voices |= set(b.get("voices") or [])
        elif probs:
            issues.append(f"{l['id']}: {probs.split(' | ')[0][:70]}")
    if not specs:
        ver = "chưa soạn bài (giáo án: verify_plan_curricula.py)"
    elif skip_verify:
        ver = "—"
    else:
        ver = "; ".join(f"{Path(v).name} {run_verifier(v)}" for v in verifiers(C)) or "phép kiểm `checks` trong từng bài (lint)"
    rows.append((C, series, len(les), len(specs), done, minutes, ver, issues))
    tot["planned"] += len(les); tot["spec"] += len(specs); tot["done"] += done; tot["minutes"] += minutes
    print(C, len(les), len(specs), done, round(minutes, 1), ver, flush=True)

md = [f"# Hiện trạng sản xuất (SINH TỰ ĐỘNG — không sửa tay)", "",
      f"Sinh bởi `audit/review/status_report.py` từ `audit/review/audit_all.tsv` (chạy lúc {stamp}) và `out/*/*/build_report.json`.",
      "“Hoàn thiện” = đã dựng, lint 0 FAIL 0 WARN, video khớp dấu băm đặc tả và lời đọc hiện tại, đúng một giọng, ASR 0 câu chưa xem xét.", "",
      f"**Tổng:** {tot['planned']} bài trong {len(rows)} lộ trình · {tot['spec']} có đặc tả · **{tot['done']} hoàn thiện** · "
      f"{tot['minutes']:.0f} phút video hoàn thiện.", "",
      "| Khoá | Tên | Bài | Đặc tả | Hoàn thiện | Phút | Bộ kiểm độc lập | Còn lại |", "|---|---|---|---|---|---|---|---|"]
for C, series, n, s, d, m, ver, issues in rows:
    rest = "—" if not issues else (f"{len(issues)} bài: " + "; ".join(issues[:3]) + (" …" if len(issues) > 3 else ""))
    md.append(f"| {C} | {series} | {n} | {s} | {d} | {m:.1f} | {ver} | {rest} |")
(ROOT / "curriculum" / "STATUS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"\nstatus_report: {tot['done']}/{tot['planned']} bài hoàn thiện, {tot['minutes']:.0f} phút → curriculum/STATUS.md")
