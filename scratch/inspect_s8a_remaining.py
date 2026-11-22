import glob
import re
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

SHORT_CHECKS = [
    (r"\bvs\b", "vs"),
    (r"\bmili giây\b", "mili_giay"),
    (r"\bO\([^)]+\)", "big_O"),
    (r"\b(?:alpha|RMSE|MAE|MAPE|WMAPE|IQR|MAD|VIF|PPV|FWER|API|GPU|TB|RAM|SQL|A/B)\b", "abbr"),
    (r"<\s*[0-9]", "unescaped_lt"),
    (r"63,6\b", "63_6"),
]

for c in ["dan", "dsc", "mlo"]:
    print(f"=== {c.upper()} ===")
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c}/L*.yaml"))):
        d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        lid = d["id"]
        words = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc.get("steps", []))
        hits = []
        for sc in d["scenes"]:
            for idx, st in enumerate(sc.get("steps", [])):
                sh = str(st.get("show") or "")
                sy = str(st.get("say") or "")
                for pat, name in SHORT_CHECKS:
                    if re.search(pat, sh + " " + sy):
                        # exclude math blocks $...$ for alpha/O/lt if obvious
                        if name == "unescaped_lt" and "<" not in re.sub(r"<[^>]+>", "", sh):
                            continue
                        if name == "unescaped_lt":
                            plain = re.sub(r"<[^>]+>", " ", re.sub(r"\$[^$]+\$", " ", sh))
                            if not re.search(r"<\s*[0-9]", plain):
                                continue
                        hits.append(f"{sc['id']}#{idx}:{name}")
        de = (ROOT / f"labs/{c.upper()}/{lid}/de.md").read_text(encoding="utf-8")
        de_hits = [name for pat, name in SHORT_CHECKS[:4] if re.search(pat, de)]
        if words < 1660 or hits or de_hits:
            print(f"  {lid} w={words} hits={sorted(set(hits))} de={sorted(set(de_hits))}")
