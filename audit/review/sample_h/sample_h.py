"""Mẫu H (AF5, 2026-11-22) — chọn 40 bài đọc độc lập, hạt giống 20261122, loại mọi bài đã vào Mẫu C–G.
Tầng: NEW (CPR, LNX, MLP, PRJ ×3) 12 · lộ trình JD chặng 1–4 12 · chặng 5 3 · chặng 6–11 nâng hàng loạt 13.
Chạy: .venv/Scripts/python -B audit/review/sample_h/sample_h.py  → sample_h.json (chia 4 phần, 10 bài/phần)."""
import hashlib, json, pathlib, random, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[3]
txt_c = (ROOT / "audit/review/sample_c/REPORT.md").read_text("utf-8")
ex = set(re.findall(r"^\|\s*([A-Z0-9]+)\s+(L\d+)\s*\|", txt_c, re.M))
line38 = next(ln for ln in txt_c.splitlines() if ln.startswith("25 bài còn lại"))
ex.update(re.findall(r"\b([A-Z0-9]+)\s+(L\d+)\b", line38))
ex.update(re.findall(r"\b([A-Z0-9]+)\s+(L\d+)\b", (ROOT / "audit/review/sample_d/REPORT.md").read_text("utf-8")))
for p in sorted((ROOT / "audit/review/sample_e").glob("part_*.md")):
    ex.update(re.findall(r"^\|\s*([A-Z0-9]+)\s+(L\d+)\s*\|", p.read_text("utf-8"), re.M))
for x in json.loads((ROOT / "audit/review/sample_f/sample_f.json").read_text("utf-8")):
    ex.add((x["course"], x["lesson"]))
n_cf = len(ex)
for x in json.loads((ROOT / "archive/scratch_pre_af5/sample_g.json").read_text("utf-8")):
    ex.add((x["course"], x["lesson"]))
r = random.Random(20261122)
def pick(c, k):
    cands = [p for p in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")) if (c, p.name[:3]) not in ex]
    return r.sample(cands, k)
plan = [("NEW", [("CPR", 3), ("LNX", 3), ("MLP", 3), ("PRJ", 3)]),
        ("JD14", [("BNX", 4), ("BNK", 2), ("FND", 1), ("JVA", 1), ("JV2", 1), ("PYT", 1), ("INT", 1), ("ACB", 1)]),
        ("S05", [("DMS", 1), ("CS112", 1), ("CS115", 1)])]
mass = ["CSA", "OSY", "NET", "SWF", "SDP", "DBS", "DVO", "WEB", "SEC", "DSY", "EVT", "DEN", "CLD", "CLC", "SAR", "AIF", "DAN", "DSC", "MLO", "IRS",
        "LLM", "AGT", "RLN", "CVI", "TOC", "PLC", "PAR", "HCI", "SEP", "CAS", "RBM", "ESY", "ROB", "GFX", "BCH"]
plan.append(("MASS", [(c, 1) for c in sorted(r.sample(mass, 13))]))
out = []
for stratum, items in plan:
    for c, k in items:
        for p in pick(c, k):
            out.append({"stratum": stratum, "course": c, "lesson": p.name[:3], "path": p.relative_to(ROOT).as_posix(),
                        "sha16": hashlib.sha256(p.read_bytes()).hexdigest()[:16]})
# chia 4 phần, mỗi phần trộn đều các tầng
for i, row in enumerate(out):
    row["part"] = i % 4 + 1
(ROOT / "audit/review/sample_h/sample_h.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"loại C–F: {n_cf} | loại C–G: {len(ex)} | Mẫu H: {len(out)}")
for part in (1, 2, 3, 4):
    print(f"-- phần {part}:", ", ".join(f"{x['course']} {x['lesson']}" for x in out if x["part"] == part))
