"""Kiểm chung mọi lộ trình curriculum/*.yaml (lv.py curriculum chỉ kiểm từng khoá):
1) đồ thị tiên quyết TOÀN CỤC (requires + requires_ext, theo từng bài) không có chu trình; in thứ tự khoá theo tô pô;
2) mỗi “(VER X:Lyy)” trong `example` có dòng PASS đúng mã đó trong audit/verify_plan_curricula.py, và mã thuộc đúng bài đó;
3) liệt kê `example` có chữ số mà không dẫn VER (để người soạn xem: con số minh hoạ hay phải kiểm).
Chạy: .venv/Scripts/python audit/check_curricula_graph.py"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

cur = {}
for f in sorted((ROOT / "curriculum").glob("*.yaml")):
    c = lv.load_yaml(f)
    if isinstance(c, dict) and c.get("course"):
        cur[str(c["course"])] = c
nodes, edges = set(), []
for cid, c in cur.items():
    for l in c["lessons"]:
        u = f"{cid}:{l['id']}"
        nodes.add(u)
        edges += [(f"{cid}:{q}", u) for q in l.get("requires") or []]
        edges += [(str(q), u) for q in l.get("requires_ext") or []]
bad = [e for e in edges if e[0] not in nodes]
indeg = {n: 0 for n in nodes}
out = {n: [] for n in nodes}
for a, b in edges:
    if a in nodes:
        out[a].append(b); indeg[b] += 1
order, q = [], sorted(n for n in nodes if indeg[n] == 0)
while q:
    n = q.pop(0); order.append(n)
    for m in out[n]:
        indeg[m] -= 1
        if indeg[m] == 0:
            q.append(m)
cyc = sorted(n for n in nodes if indeg[n] > 0)
print(f"1) {len(cur)} lộ trình, {len(nodes)} bài, {len(edges)} cạnh tiên quyết; tham chiếu hỏng: {bad or 0}; bài nằm trên chu trình: {cyc or 0}")
# thứ tự khoá: khoá A trước B nếu có bài của A là tiên quyết của bài B
cedge = {(a.split(':')[0], b.split(':')[0]) for a, b in edges if a.split(':')[0] != b.split(':')[0]}
ck = {c: 0 for c in cur}
for a, b in cedge:
    ck[b] += 1
co, q = [], sorted(c for c in cur if ck[c] == 0)
while q:
    c = q.pop(0); co.append(c)
    for a, b in sorted(cedge):
        if a == c:
            ck[b] -= 1
            if ck[b] == 0:
                q.append(b)
print("   thứ tự khoá (tô pô):", " → ".join(co), "" if len(co) == len(cur) else f"| CHU TRÌNH giữa các khoá: {sorted(set(cur) - set(co))}")
res = subprocess.run([sys.executable, str(ROOT / "audit" / "verify_plan_curricula.py")], capture_output=True, text=True, encoding="utf-8")
status = {}
for line in res.stdout.splitlines():
    m = re.match(r"(PASS|FAIL) \| (\S+)", line)
    if m:
        status[m.group(2)] = m.group(1)
miss, wrong, nover = [], [], []
for cid, c in cur.items():
    for l in c["lessons"]:
        ex = str(l.get("example") or "")
        vers = re.findall(r"VER ([A-Z0-9]+:L\d+)", ex)
        for v in vers:
            if status.get(v) != "PASS":
                miss.append((f"{cid}:{l['id']}", v, status.get(v, "không có")))
            if v != f"{cid}:{l['id']}":
                wrong.append((f"{cid}:{l['id']}", v))
        if not vers and re.search(r"\d", ex) and "minh hoạ" not in ex and c.get("status") == "planned":
            nover.append(f"{cid}:{l['id']}")
print(f"2) VER dẫn tới mã không PASS: {miss or 0}; VER của bài khác: {wrong or 0}")
print(f"3) ví dụ có chữ số mà không dẫn VER ({len(nover)}): {', '.join(nover)}")
sys.exit(1 if (bad or cyc or miss or len(co) != len(cur)) else 0)
