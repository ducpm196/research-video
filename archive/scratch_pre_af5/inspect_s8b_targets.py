"""Read-only inspection of Stage 8 Batch 8B (EVT, DEN, CLD, CLC, SAR) scenes, P1, math, and SVGs."""
import re, sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

ABBR_RE = re.compile(r"\b(?:[A-Z]{2,}[0-9A-Z\-]*|[A-Za-z]+(?:[A-Z][a-z]+)+)\b")
IGNORE = {"EVT", "DEN", "CLD", "CLC", "SAR", "L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15",
          "VER", "OK", "Python"}

for c in ("EVT", "DEN", "CLD", "CLC", "SAR"):
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c.lower()}.yaml")
    print(f"\n=== {c} ===")
    for les in cur["lessons"]:
        lid = les["id"]
        fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        sc_ids = [f"{sc['id']}({sc['kind']})" for sc in sp["scenes"]]
        recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
        r_txt = " ".join(str(st.get("show") or "") + " " + str(st.get("say") or "") for st in recap["steps"])
        r_plain = re.sub(r"<[^>]+>", " ", r_txt)
        r_abbrs = sorted({m for m in ABBR_RE.findall(r_plain) if m not in IGNORE})
        has_2m = "Hai mức quy mô" in r_plain or "hai mức quy mô" in r_plain.lower()
        de_p = ROOT / "labs" / c.lower() / lid / "de.md"
        d_abbrs = sorted({m for m in ABBR_RE.findall(de_p.read_text(encoding="utf-8")) if m not in IGNORE and m not in ("Lab", "Python")}) if de_p.exists() else []
        print(f"  {lid}: 2m={int(has_2m)} r_p1={r_abbrs} d_p1={d_abbrs}")
        print(f"       objs={les['objectives']}")
        print(f"       scs={sc_ids}")

for c, lid, a, b in [
    ("evt", "L05", 200, 236),
    ("sar", "L00", 230, 276),
    ("sar", "L01", 230, 276),
    ("clc", "L11", 65, 115),
    ("cld", "L10", 170, 210),
    ("den", "L08", 65, 105),
]:
    fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
    lines = fp.read_text(encoding="utf-8").splitlines()
    print(f"\n--- {c.upper()} {lid} [{a}:{b}] ---")
    for i, ln in enumerate(lines[a-1:b], a):
        print(f"  {i}: {ln[:220]}")
