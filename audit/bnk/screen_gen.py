"""Sinh sổ mã trên màn hình khoá BNK (audit/review/screen_code/BNK.yaml) từ lib.PROGRAMS (audit/bnk/src), cùng cách
`screen_code.py gen-jva`: mỗi prog(...) là một NGUỒN chạy thật (src:BNK:<tên>); khối mã trên màn hình = fragment `within` nguồn
chứa nó; khối kết quả = output `of` nguồn. Mục sổ đã có (viết tay) mà không khớp chương trình nào được GIỮ nếu khối còn và sha còn đúng.
Dùng:  .venv/Scripts/python -B audit/bnk/screen_gen.py        (sinh lại toàn sổ BNK từ lessons/bnk hiện có)
Rồi:   .venv/Scripts/python -B audit/review/screen_code.py check --course BNK -v"""
import importlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "audit" / "bnk"), str(ROOT / "audit" / "bnk" / "src"), str(ROOT / "audit" / "review")]
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402
import screen_code as sc  # noqa: E402

for p in sorted((ROOT / "audit/bnk/src").glob("l*.py")):
    lib.begin(p.stem.upper())
    try:
        importlib.import_module(p.stem).build()
    except Exception as ex:  # bài đang soạn dở: bỏ qua, nhưng báo
        print("BỎ QUA", p.name, type(ex).__name__, ex)

sources, by_lesson, seen = {}, {}, {}
for pr in lib.PROGRAMS:
    key = (pr["lesson"], pr["lang"], pr["code"], pr["out"])
    if key in seen:
        continue
    n = f"{pr['lesson']}_{pr['name']}"
    i = 2
    while n in sources:
        n, i = f"{pr['lesson']}_{pr['name']}_{i}", i + 1
    seen[key] = n
    e = {"lang": pr["lang"]}
    if pr["lang"] == "java":
        e["java_class"] = pr["name"]
    e["expect_stdout"] = pr["out"]
    e.update(pr["extra"])
    e["code"] = pr["code"]
    sources[n] = e
    by_lesson.setdefault(pr["lesson"], []).append((n, pr))

blocks = sc.all_blocks("BNK")
out_path = ROOT / "audit/review/screen_code/BNK.yaml"
old = (yaml.safe_load(out_path.read_text(encoding="utf-8")) or {}) if out_path.exists() else {}
old_blocks = old.get("blocks") or {}
old_sources = old.get("sources") or {}
reg, unmatched = {}, []
for k, t in blocks.items():
    lid, frag, hit = k.split()[1], sc._dedent_lines(t), None
    tl = [l.rstrip() for l in t.split("\n")]
    for n, pr in by_lesson.get(lid, []):
        hl = pr["code"].split("\n")
        if any(sc._dedent_lines("\n".join(hl[i:i + len(frag)])) == frag for i in range(len(hl) - len(frag) + 1)):
            hit = {"sha": sc.digest(t), "kind": "fragment", "within": f"src:BNK:{n}",
                   "reason": f"dãy dòng của chương trình {pr['name']} (nguồn chạy thật)"}
            break
    if hit is None:
        same = {v["within"] for kk, v in reg.items() if kk.rsplit(" ", 1)[0] == k.rsplit(" ", 1)[0] and v.get("kind") == "fragment"}
        cands = sorted(by_lesson.get(lid, []), key=lambda x: f"src:BNK:{x[0]}" not in same)
        for n, pr in cands:
            outs = [l.rstrip() for l in pr["out"].split("\n")] if pr["out"] else []
            if outs and outs == tl[:len(outs)] and len(tl) == len(outs):
                hit = {"sha": sc.digest(t), "kind": "output", "of": f"src:BNK:{n}",
                       "reason": f"khối kết quả của chương trình {pr['name']}"}
                break
            if outs and all(o.count("|") >= 3 for o in outs) and tl == [o.split("|")[3].rstrip() for o in outs]:
                hit = {"sha": sc.digest(t), "kind": "output", "of": f"src:BNK:{n}", "field": 3,
                       "reason": f"cột kế hoạch (cột thứ tư của EXPLAIN QUERY PLAN) của chương trình {pr['name']}"}
                break
    if hit is None and k in old_blocks and old_blocks[k].get("sha") == sc.digest(t):
        hit = old_blocks[k]
        for fld in ("prelude_keys",):
            pass
    if hit:
        reg[k] = hit
    else:
        unmatched.append(k)
# nguồn tay (không do prog sinh) giữ nguyên nếu mục sổ còn dùng
for n, v in old_sources.items():
    if n not in sources and any(str(b.get("within") or b.get("of")) == f"src:BNK:{n}" for b in reg.values()):
        sources[n] = v
hdr = ("# Sổ mã trên màn hình khoá BNK — SINH bằng audit/bnk/screen_gen.py từ audit/bnk/src (lib.PROGRAMS); bài sinh từ audit/bnk/src/lNN.py.\n"
       "# Mục viết tay (khối không khớp chương trình nào) được giữ qua các lần sinh lại khi sha còn đúng.\n")
out_path.write_text(hdr + yaml.safe_dump({"blocks": reg, "sources": sources}, allow_unicode=True, sort_keys=False, width=200),
                    encoding="utf-8", newline="\n")
print(f"screen_gen: {len(blocks)} khối, ghi {len(reg)}, nguồn {len(sources)}, chưa khớp {len(unmatched)}")
for k in unmatched:
    print("  CHƯA KHỚP", k, "|", (blocks[k].splitlines() or [""])[0][:90])
