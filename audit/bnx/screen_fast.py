"""Thử nhanh sổ mã trên màn hình của MỘT bài BNX (đợt BNX2): chỉ kiểm khối của bài đó và các nguồn trong audit/bnx/screen/lNN.yaml của nó,
không chạy lại cả khoá (screen_try.py chạy cả BNX, ≈ 12 phút vì Oracle/SQL Server/Kafka). Kết quả khớp cổng `check` cho các khối của bài.
Dùng: python -B audit/bnx/screen_fast.py L24 [L25 …]"""
import os
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
lids = [a.upper() for a in sys.argv[1:]]
blocks, sources = {}, {}
for lid in lids:
    d = yaml.safe_load((ROOT / "audit" / "bnx" / "screen" / f"{lid.lower()}.yaml").read_text(encoding="utf-8")) or {}
    blocks.update(d.get("blocks") or {})
    sources.update(d.get("sources") or {})
tmp = tempfile.mkdtemp()
Path(tmp, "BNX.yaml").write_text(yaml.safe_dump({"blocks": blocks, "sources": sources}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
os.environ["SC_REGDIR"] = tmp
sys.path.insert(0, str(ROOT / "audit" / "review"))
import screen_code as sc  # noqa: E402

allb = {k: t for k, t in sc.all_blocks("BNX").items() if k.split()[1] in lids}
reg = sc.load_reg("BNX")
g = sc.Gate(allb, reg)
res = {"PASS": 0, "FAIL": 0, "STALE": 0, "MISSING": 0}
for k, t in allb.items():
    e = reg.get(k)
    if e is None:
        res["MISSING"] += 1
        print("MISSING", k, "|", (t.splitlines() or [""])[0][:70])
    elif e.get("sha") != sc.digest(t):
        res["STALE"] += 1
        print("STALE", k)
    else:
        ok, msg, _, _ = g.check(k)
        res["PASS" if ok else "FAIL"] += 1
        if not ok:
            print("FAIL", k, msg)
for k in [k for k in reg if k.startswith("src:")]:
    ok, msg, _, _ = g.check(k)
    res["PASS" if ok else "FAIL"] += 1
    if not ok:
        print("FAIL", k, msg)
orphan = [k for k in reg if k not in allb and not k.startswith("src:")]
for k in orphan:
    print("ORPHAN", k)
print(f"screen_fast {lids}: {len(allb)} khối — PASS {res['PASS']} · FAIL {res['FAIL']} · STALE {res['STALE']} · MISSING {res['MISSING']} · ORPHAN {len(orphan)}")
sys.exit(1 if (res["FAIL"] or res["STALE"] or res["MISSING"] or orphan) else 0)
