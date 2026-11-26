"""Scan DAN, DSC, MLO YAMLs + de.md for P1 abbreviations/English terms + word counts + checks."""
import re, sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

ABBR_RE = re.compile(r"\b(?:[A-Z]{2,}[0-9A-Z\-]*|[A-Za-z]+(?:[A-Z][a-z]+)+)\b")
IGNORE = {"DAN", "DSC", "MLO", "L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15",
          "VER", "OK", "KO07", "FH12", "AM12", "SC15", "Python", "SQLite"}

for c in ("DAN", "DSC", "MLO"):
    print(f"\n=== {c} P1 CHECK ===")
    for p in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")):
        sp = lv.load_spec(p)
        lid = sp["id"]
        recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
        r_txt = " ".join(str(st.get("show") or "") + " " + str(st.get("say") or "") for st in recap["steps"])
        r_plain = re.sub(r"<[^>]+>", " ", r_txt)
        de_txt = (ROOT / "labs" / c.lower() / lid / "de.md").read_text(encoding="utf-8")
        r_abbrs = sorted({m for m in ABBR_RE.findall(r_plain) if m not in IGNORE})
        d_abbrs = sorted({m for m in ABBR_RE.findall(de_txt) if m not in IGNORE and m not in ("Lab", "Python")})
        if r_abbrs or d_abbrs:
            print(f"  {lid}: recap={r_abbrs} | de={d_abbrs}")
