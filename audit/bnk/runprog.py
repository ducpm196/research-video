"""Chạy THẬT các prog(...) của một bài BNK (bằng đúng trình chạy của cổng screen_code) và in đầu ra thật cạnh đầu ra khai.
Dùng khi soạn: .venv/Scripts/python -B audit/bnk/runprog.py L00 [tên_con ...]   — in "OK" nếu khớp, hoặc đầu ra thật để dán vào out=."""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "audit" / "bnk"), str(ROOT / "audit" / "bnk" / "src"), str(ROOT / "audit" / "review")]
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402
import screen_code as sc  # noqa: E402

lid = sys.argv[1].upper()
only = sys.argv[2:]
lib.begin(lid)
importlib.import_module(lid.lower()).build()
reg = {}
for pr in lib.PROGRAMS:
    if pr["lesson"] != lid or (only and not any(o in pr["name"] for o in only)):
        continue
    n = f"{lid}_{pr['name']}"
    e = {"lang": pr["lang"], "kind": "run", "code": pr["code"], "expect_stdout": pr["out"], "_source": True}
    if pr["lang"] == "java":
        e["java_class"] = pr["name"]
    e.update(pr["extra"])
    reg["src:BNK:" + n] = e
g = sc.Gate({}, reg)
bad = 0
for k, e in reg.items():
    e2 = dict(e)
    e2.pop("expect_stdout")
    e2["no_claim_reason"] = "xem"
    g.reg = dict(reg, **{k: e2})
    g.cache = {}
    ok, msg, so, se = g.check(k)
    want = "\n".join(l.rstrip() for l in e["expect_stdout"].split("\n")).strip("\n")
    got = "\n".join(l.rstrip() for l in so.replace("\r\n", "\n").split("\n")).strip("\n")
    if ok and got == want:
        print(f"OK   {k}")
    else:
        bad += 1
        print(f"DIFF {k}  [{msg[:200]}]\n--- đầu ra thật ---\n{got}\n--- stderr ---\n{se.strip()[-400:]}\n-------------------")
sys.exit(1 if bad else 0)
