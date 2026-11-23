"""Mô phỏng (CHỈ ĐỌC): chặng = thành viên KHAI TƯỜNG MINH (không kéo bao đóng). In mọi cạnh tiên quyết thật trỏ sang chặng SAU
(lỗi giáo án phải xử: dời khoá, đổi thứ tự, hoặc hạ cạnh xuống see_also) và chu trình trong chặng khi giữ thứ tự tác giả.
Tham số: move=KHOÁ:Sxx>Syy  drop=A:Lxx<B:Lyy  split=KHOÁ:Lxx-Lyy:Sxx (đặt một đoạn bài vào chặng khác với phần còn lại)"""
import copy, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack
cur = pack.load_cur()
STAGES = [(s[0], list(s[3])) for s in pack.STAGES]
DROP = set()
PREFER = None
def edit(stage, add=(), remove=()):
    for i, (k, goals) in enumerate(STAGES):
        if k == stage:
            STAGES[i] = (k, [g for g in goals if g not in remove] + list(add))
for a in sys.argv[1:]:
    k, v = a.split("=")
    if k == "drop":
        u, q = v.split("<"); DROP.add((u, q))
    elif k == "move":
        g, r = v.rsplit(":S", 1); src, dst = r.split(">S"); edit("S" + src, remove=[g]); edit("S" + dst, add=[g])
    elif k == "add":
        st, g = v.split("/"); edit(st, add=[g])
    elif k == "rm":
        st, g = v.split("/"); edit(st, remove=[g])
    elif k == "prefer":
        PREFER = v.split(",")
les, pre0 = pack.lesson_index(cur)
real = {u: {q for q in v if (u, q) not in DROP} for u, v in pre0.items()}
imp = defaultdict(set)
for C, c in cur.items():
    ids = [l["id"] for l in c["lessons"]]
    for a, b in zip(ids, ids[1:]):
        imp[f"{C}:{b}"].add(f"{C}:{a}")
stage_of = {}
order_idx = {k: i for i, (k, _) in enumerate(STAGES)}
for k, goals in STAGES:
    for g in goals:
        for u in pack.expand(cur, g):
            if u not in stage_of:
                stage_of[u] = k
print("chưa có chặng:", sorted(set(les) - set(stage_of))[:20])
cnt = defaultdict(Counter)
for u, k in stage_of.items():
    cnt[k][u.split(":")[0]] += 1
for k, _ in STAGES:
    print(k, sum(cnt[k].values()), dict(cnt[k]))
fwd = sorted((stage_of[u], u, q, stage_of[q]) for u in les for q in real[u] if u in stage_of and q in stage_of and order_idx[stage_of[q]] > order_idx[stage_of[u]])
print(f"cạnh THẬT trỏ sang chặng sau: {len(fwd)}")
for s, u, q, sq in fwd:
    print(f"  {s} {u} <- {q} ({sq})")
impf = sorted((u, q) for u in les for q in imp[u] if order_idx[stage_of[q]] > order_idx[stage_of[u]])
print("cạnh ngầm ngược (bài k ở chặng sau bài k+1):", impf)
# chu trình trong chặng với real + implicit
tr = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8"))
prefer = list(PREFER or tr["prefer"]); prefer += [C for C in cur if C not in prefer]
key = lambda u: (prefer.index(u.split(":")[0]), int(u.split(":L")[1]))
seq = []
for k, _ in STAGES:
    need = {u for u, s in stage_of.items() if s == k}
    op = {u: (real[u] | imp[u]) & need for u in need}
    ind = {u: len(op[u]) for u in need}
    order, ready = [], sorted((u for u in need if ind[u] == 0), key=key)
    while ready:
        u = ready.pop(0); order.append(u)
        for v in need:
            if u in op[v]:
                ind[v] -= 1
                if ind[v] == 0: ready.append(v)
        ready.sort(key=key)
    if len(order) != len(need):
        print(f"!! CHU TRÌNH trong {k}: còn {sorted(need - set(order))[:12]}")
    seq += order
    # mức đan xen: số lần đổi khoá
    sw = sum(1 for a, b in zip(order, order[1:]) if a.split(":")[0] != b.split(":")[0])
    print(f"{k}: {len(order)} bài, đổi khoá {sw} lần; dãy khoá: " + " ".join(dict.fromkeys(u.split(':')[0] for u in order)))
pos = {u: i for i, u in enumerate(seq)}
nxt_same = {}
for n, u in enumerate(seq):
    C = u.split(":")[0]
    for v in seq[n + 1:]:
        if v.split(":")[0] == C:
            nxt_same[u] = v.split(":")[1]; break
REF = re.compile(r"[Bb]ài sau \(bài (\d+)\)")
bad = tot = 0
for C, c in cur.items():
    for l in c["lessons"]:
        spec = l.get("spec")
        if not spec or not (ROOT / spec).exists(): continue
        text = (ROOT / spec).read_text(encoding="utf-8")
        for m in REF.finditer(text):
            tot += 1
            ref, me = f"{C}:L{int(m.group(1)):02d}", f"{C}:{l['id']}"
            if ref not in pos or me not in pos: print("NEXT ?", me, ref); bad += 1
            elif pos[ref] <= pos[me]: print(f"NEXT FAIL {me}: hẹn {ref} nhưng đứng TRƯỚC"); bad += 1
            elif nxt_same.get(me) and nxt_same[me] != f"L{int(m.group(1)):02d}": print(f"NEXT FAIL {me}: hẹn {ref} nhưng bài kế cùng khoá là {nxt_same[me]}"); bad += 1
print(f"next_refs: {tot} lời hẹn, {bad} lệch")
