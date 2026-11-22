import glob
import re
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

TECH_PAT = re.compile(
    r"\b(?:SQL|CTE|JOIN|GROUP BY|WHERE|SELECT|COHORT|FUNNEL|MA|MAE|MAPE|WMAPE|RMSE|"
    r"RFM|MAD|IQR|P95|P99|KPI|ROC|AUC|PR|PSI|CSI|MLOps|CI/CD|A/B|p-value|VIF|QPS|API|"
    r"RGB|CSV|JSON|YAML|ETL|ELT|SCD|OLAP|DAG|TTL|LRU|SLA|SLO|SLI|ADR|RTO|RPO|KMS|DEK|"
    r"CDN|IAM|VPC|CIDR|AZ|SPOF|DLQ|CQRS|CAP|BFT|TPS)\b"
)

for c in ["dan", "dsc", "mlo"]:
    print(f"=== {c.upper()} ===")
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c}/L*.yaml"))):
        d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        lid = d["id"]
        words = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc.get("steps", []))
        recs = [st.get("show", "") + " || SAY: " + st.get("say", "") for sc in d["scenes"] if sc["id"] == "recap" for st in sc.get("steps", [])]
        rec_hits = set(TECH_PAT.findall(" ".join(recs)))
        de_txt = (ROOT / f"labs/{c.upper()}/{lid}/de.md").read_text(encoding="utf-8")
        de_hits = set(TECH_PAT.findall(de_txt))
        if words < 1650 or rec_hits or de_hits:
            print(f"  {lid}: w={words} rec_terms={sorted(rec_hits)} de_terms={sorted(de_hits)}")
