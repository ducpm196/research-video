import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("dan", "L02", ["1–N", ":memory:", "RAM"]),
    ("dan", "L04", ["cohort", "retention", "T1", "T2"]),
    ("dan", "L12", ["alpha"]),
    ("dsc", "L02", ["nhiều–nhiều", "N–M", "Đề-các", "Cartesian"]),
    ("dsc", "L06", ["Pearson"]),
    ("dsc", "L09", ["FWER"]),
    ("dsc", "L11", ["PPV"]),
    ("den", "L12", ["SCD"]),
    ("evt", "L00", ["bus", "p2p", "điểm–điểm"]),
    ("evt", "L03", ["NTP"]),
    ("evt", "L11", ["1 TB = 1000 GB", "1000 GB"]),
    ("mlo", "L02", ["TB", "petabyte"]),
    ("mlo", "L03", ["CI"]),
    ("mlo", "L06", ["req/s"]),
    ("mlo", "L13", ["API"]),
]

for c, lid, terms in CHECKS:
    p = sorted((ROOT / f"lessons/{c}").glob(f"{lid}_*.yaml"))[0]
    d = yaml.safe_load(p.read_text("utf-8"))
    body = "\n".join(str(st.get(k, "")) for s in d["scenes"] if s["id"] not in ("practice", "recap") for st in s["steps"] for k in ("show", "say"))
    recap_txt = "\n".join(str(st.get("show", "")) for s in d["scenes"] if s["id"] == "recap" for st in s["steps"])
    missing_body = [t for t in terms if re.search(rf"(?<!\w){re.escape(t)}(?!\w)", body, re.I) is None]
    print(f"{c.upper()} {lid}: missing_in_body={missing_body}")
    if missing_body and c == "evt" and lid == "L11":
        for s in d["scenes"]:
            for i, st in enumerate(s["steps"]):
                if "TB" in str(st.get("show", "")):
                    print("  EVT L11 TB at:", s["id"], i, repr(st["show"][:120]))

# Also print English acronyms in CLC & SAR `practice#0` / `de.md` not explained in `hook..quiz`
print("\n=== CLC & SAR ACRONYMS IN PRACTICE#0/DE NOT IN BODY ===")
for c, toks in [
    ("clc", ["AZ", "VPC", "IP", "subnet", "IAM", "Allow", "Deny", "Reserved", "On-Demand", "USD", "serverless", "RAM", "snapshot", "WAL", "Egress", "CDN", "cache", "KMS", "KB", "DEK", "Active-Active", "req/s", "N+1", "managed", "stateless", "SPOF"]),
    ("sar", ["P95", "P99", "SLO", "ADR", "RDBMS", "NoSQL", "ACID", "Sharding", "join", "QPS", "DAU", "req", "UI", "caller", "callee", "Cache", "RF", "shard", "parallel", "series", "downtime", "burst", "backlog", "drain", "SQLite", "ledger", "idem", "RTT", "sync", "async", "PRAGMA", "blast_radius"]),
]:
    for p in sorted((ROOT / f"lessons/{c}").glob("L*.yaml")):
        lid = p.name[:3]
        d = yaml.safe_load(p.read_text("utf-8"))
        body = "\n".join(str(st.get(k, "")) for s in d["scenes"] if s["id"] not in ("practice", "recap") for st in s["steps"] for k in ("show", "say"))
        prac = "\n".join(str(st.get("show", "")) for s in d["scenes"] if s["id"] == "practice" for st in s["steps"][:1])
        de = (ROOT / f"labs/{c}/{lid}/de.md").read_text("utf-8")
        used = [t for t in toks if re.search(rf"(?<!\w){re.escape(t)}(?!\w)", prac + "\n" + de)]
        miss = [t for t in used if re.search(rf"(?<!\w){re.escape(t)}(?!\w)", body, re.I) is None]
        if miss:
            print(f"{c.upper()} {lid}: miss={miss}")
