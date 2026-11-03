"""Tính lộ trình theo nghề từ curriculum/tracks.yaml: mục tiêu → bao đóng tiên quyết ở mức từng bài (requires trong khoá, requires_ext
giữa khoá) → sắp xếp tô pô toàn cục (Kahn, ưu tiên thứ tự khoá tô pô rồi số bài) → gom theo khoá thành các đoạn bài.
Kiểm: mục tiêu trỏ tới bài có thật; thứ tự in ra thoả MỌI cạnh tiên quyết (kiểm lại từng cạnh sau khi sắp).
Đọc trạng thái hoàn thiện từ audit/review/audit_all.tsv (nếu có) để ghi bao nhiêu bài của lộ trình đã có video hoàn thiện.
Chạy: .venv/Scripts/python audit/review/tracks.py → curriculum/TRACKS.md (sinh tự động)."""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
cur = {}
for f in sorted((ROOT / "curriculum").glob("*.yaml")):
    c = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    if isinstance(c, dict) and c.get("course"):
        cur[str(c["course"])] = c
pre = defaultdict(set)
title = {}
for C, c in cur.items():
    for l in c["lessons"]:
        u = f"{C}:{l['id']}"
        title[u] = l["title"]
        pre[u] |= {f"{C}:{q}" for q in l.get("requires") or []} | {str(q) for q in l.get("requires_ext") or []}
nodes = set(title)
# thứ tự khoá tô pô (như check_curricula_graph.py) để sắp ổn định
cedge = {(a.split(":")[0], u.split(":")[0]) for u in nodes for a in pre[u] if a.split(":")[0] != u.split(":")[0]}
indeg = {C: 0 for C in cur}
for a, b in cedge:
    indeg[b] += 1
corder, q = [], sorted(C for C in cur if indeg[C] == 0)
while q:
    C = q.pop(0); corder.append(C)
    for a, b in sorted(cedge):
        if a == C:
            indeg[b] -= 1
            if indeg[b] == 0:
                q.append(b)
_prefer = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8")).get("prefer") or []
assert sorted(_prefer) == sorted(cur), f"prefer phải liệt kê đủ mọi khoá: thiếu {sorted(set(cur) - set(_prefer))}, thừa {sorted(set(_prefer) - set(cur))}"
crank = {C: (_prefer.index(C), corder.index(C)) for C in cur}   # phá hoà theo thứ tự sư phạm; Kahn vẫn giữ mọi tiên quyết
lid = lambda u: int(u.split(":L")[1])


def expand(goal):
    if ":" not in goal:
        return [f"{goal}:{l['id']}" for l in cur[goal]["lessons"]]
    C, rng = goal.split(":")
    m = re.fullmatch(r"L(\d+)(?:-L(\d+))?", rng)
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    out = [f"{C}:L{k:02d}" for k in range(a, b + 1)]
    bad = [u for u in out if u not in nodes]
    assert not bad, f"mục tiêu {goal}: không có bài {bad}"
    return out


done = set()
tsv = ROOT / "audit" / "review" / "audit_all.tsv"
if tsv.exists():
    for line in tsv.read_text(encoding="utf-8").splitlines()[1:]:
        p = (line.split("\t") + [""] * 4)[:4]
        if p[2] == "đã dựng" and not p[3]:
            done.add(f"{p[0]}:{p[1]}")
tracks = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8"))["tracks"]
md = ["# Lộ trình theo nghề (SINH TỰ ĐỘNG — không sửa tay)", "",
      "Sinh bởi `audit/review/tracks.py` từ `curriculum/tracks.yaml` (mục tiêu của từng nghề) và tiên quyết của mọi lộ trình.",
      "Mỗi nghề liệt kê ĐÚNG các bài cần học — gồm mọi bài nền mà mục tiêu đòi hỏi — theo thứ tự thoả mọi tiên quyết (đã kiểm từng cạnh).",
      "“✓” = số bài đã có video hoàn thiện (theo `audit/review/audit_all.tsv`).", ""]
for tr in tracks:
    need, stack = set(), [u for g in tr["goals"] for u in expand(g)]
    while stack:
        u = stack.pop()
        if u in need:
            continue
        assert u in nodes, f"{tr['id']}: tiên quyết {u} không có"
        need.add(u); stack += list(pre[u])
    ind = {u: len(pre[u] & need) for u in need}
    order, ready = [], sorted((u for u in need if ind[u] == 0), key=lambda u: (crank[u.split(':')[0]], lid(u)))
    while ready:
        u = ready.pop(0); order.append(u)
        for v in need:
            if u in pre[v]:
                ind[v] -= 1
                if ind[v] == 0:
                    ready.append(v)
        ready.sort(key=lambda u: (crank[u.split(':')[0]], lid(u)))
    pos = {u: i for i, u in enumerate(order)}
    assert len(order) == len(need), f"{tr['id']}: chu trình"
    assert all(pos[a] < pos[u] for u in need for a in pre[u]), f"{tr['id']}: thứ tự vi phạm tiên quyết"
    # gom theo khoá, theo thứ tự lần đầu xuất hiện
    by, first = defaultdict(list), []
    for u in order:
        C = u.split(":")[0]
        if C not in by:
            first.append(C)
        by[C].append(lid(u))

    def ranges(xs):
        xs, out, s = sorted(xs), [], None
        for i, x in enumerate(xs):
            s = x if s is None else s
            if i == len(xs) - 1 or xs[i + 1] != x + 1:
                out.append(f"L{s:02d}" if s == x else f"L{s:02d}–L{x:02d}"); s = None
        return ", ".join(out)

    full = lambda C: len(by[C]) == len(cur[C]["lessons"])
    nd = sum(u in done for u in need)
    md += [f"## {tr['name']}", "", f"Mục tiêu: {', '.join(tr['goals'])} · **{len(need)} bài** · ✓ {nd}", "",
           " → ".join(f"**{C}**" + ("" if full(C) else f" ({ranges(by[C])})") for C in first), ""]
    print(f"{tr['id']}: {len(need)} bài, {len(first)} khoá, ✓ {nd}")
(ROOT / "curriculum" / "TRACKS.md").write_text("\n".join(md), encoding="utf-8")
print("→ curriculum/TRACKS.md")
