"""Thêm một mục vào curriculum/bnx.yaml (cuối tệp) + dòng VER vào audit/verify_plan_curricula.py (trước dòng TỔNG).
Dùng: python addcur.py <tệp json: id, title, spec, requires, requires_ext, objectives, example, fix, ver>"""
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
cur = "D:/research-video/curriculum/bnx.yaml"
s = open(cur, encoding="utf-8").read()
lid = d["id"]
if f"  - id: {lid}\n" in s:
    print("đã có", lid)
    sys.exit(0)


def q(x):
    return json.dumps(x, ensure_ascii=False)


ent = (f"  - id: {lid}\n    title: {q(d['title'])}\n    spec: {d['spec']}\n    requires: {json.dumps(d['requires'])}\n"
       f"    requires_ext: {q(d['requires_ext'])}\n    objectives: {q(d['objectives'])}\n    example: {q(d['example'])}\n    fix: {q(d['fix'])}\n")
if not s.endswith("\n"):
    s += "\n"
open(cur, "w", encoding="utf-8", newline="\n").write(s + ent)
v = "D:/research-video/audit/verify_plan_curricula.py"
lines = open(v, encoding="utf-8").read().split("\n")
idx = max(i for i, l in enumerate(lines) if l.startswith('print(f"') and "TỔNG" in l)
# chèn trước dòng trống đứng ngay trước dòng TỔNG (nếu có)
at = idx - 1 if lines[idx - 1] == "" else idx
lines[at:at] = d["ver"].rstrip().split("\n")
open(v, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("ok", lid)
