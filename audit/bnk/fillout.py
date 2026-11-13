"""Điền đầu ra THẬT vào các prog(..., out="X") của một bài: chạy từng chương trình (trình chạy của cổng screen_code) rồi thay
lần lượt các chỗ out="X" trong audit/bnk/src/lNN.py bằng đầu ra thật. Chỉ chạm các chỗ còn là "X".
Dùng: .venv/Scripts/python -B audit/bnk/fillout.py L01"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "audit" / "bnk"), str(ROOT / "audit" / "bnk" / "src"), str(ROOT / "audit" / "review")]
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402
import screen_code as sc  # noqa: E402

lid = sys.argv[1].upper()
lib.begin(lid)
importlib.import_module(lid.lower()).build()
path = ROOT / "audit" / "bnk" / "src" / f"{lid.lower()}.py"
src = path.read_text(encoding="utf-8")
todo = [p for p in lib.PROGRAMS if p["lesson"] == lid and p["out"] == "X"]
for p in todo:
    e = {"lang": p["lang"], "kind": "run", "code": p["code"], "no_claim_reason": "điền đầu ra", "_source": True}
    if p["lang"] == "java":
        e["java_class"] = p["name"]
    e.update(p["extra"])
    e.pop("expect_stdout", None)
    allreg = {}
    for q in lib.PROGRAMS:
        if q["lesson"] == lid:
            e2 = {"lang": q["lang"], "kind": "run", "code": q["code"], "no_claim_reason": "x", "_source": True}
            if q["lang"] == "java":
                e2["java_class"] = q["name"]
            e2.update(q["extra"])
            allreg[f"src:BNK:{lid}_{q['name']}"] = e2
    allreg["src:BNK:x"] = e
    g = sc.Gate({}, allreg)
    ok, msg, so, se = g.check("src:BNK:x")
    so = "\n".join(l.rstrip() for l in so.replace("\r\n", "\n").split("\n")).strip("\n")
    if not ok:
        print("LỖI chạy", p["name"], msg[:300], se[-300:])
        continue
    rep = f'out="""{so}"""' if "\n" in so else f'out="{so}"'
    src = src.replace('out="X"', rep, 1)
    print("điền", p["name"], "->", so.replace("\n", " ⏎ ")[:140])
path.write_text(src, encoding="utf-8", newline="\n")
