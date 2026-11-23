"""Mô phỏng (CHỈ ĐỌC) các phương án sửa dãy chặng của pack.stages() — không ghi tệp nào của kho.
Dùng: .venv/Scripts/python -B audit/review/audit_final/logs/af5r2/stage_sim.py <phương án>
  cur   = hiện trạng (bao đóng gồm cạnh ngầm L(k)->L(k+1))
  real  = bao đóng chỉ bằng requires + requires_ext; cạnh ngầm chỉ sắp thứ tự trong chặng
  planF = real + sửa của plan_AF5_final (S05 thêm CS115:L45-L46, DVO sang S08, 6 cạnh -> see_also)
  v3    = phương án đề xuất của lượt rà này (xem STAGE_EDIT/ DROP trong mã)
In: cỡ từng chặng, khoá lạ bị kéo vào (kèm cạnh kéo), vi phạm cạnh thật, vi phạm cạnh ngầm, vi phạm lời hẹn "Bài sau (bài N)"."""
import copy
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack  # noqa: E402

MODE = sys.argv[1] if len(sys.argv) > 1 else "cur"
cur = pack.load_cur()
STAGES = copy.deepcopy(pack.STAGES)
DROP = set()  # (bài, tiên quyết) bỏ khỏi cạnh thật (đổi sang see_also)
PLANF_DROP = {("WEB:L01", "TOC:L06"), ("WEB:L03", "PLC:L07"), ("WEB:L12", "ESY:L13"), ("SDP:L12", "PLC:L07"),
              ("SDP:L12", "PLC:L12"), ("SWF:L08", "TOC:L01"), ("SEC:L13", "DSC:L11")}


def edit(stage, add=(), remove=()):
    for i, s in enumerate(STAGES):
        if s[0] == stage:
            goals = [g for g in s[3] if g not in remove] + list(add)
            STAGES[i] = (s[0], s[1], s[2], goals, s[4])


if MODE in ("planF", "v3"):
    DROP |= PLANF_DROP
    edit("S05", add=["CS115:L45-L46"])
    edit("S07", remove=["DVO"])
    edit("S08", add=["DVO"])
if MODE == "v3":
    for a in sys.argv[2:]:  # tham số thêm: "drop=A:Lxx<B:Lyy" | "move=KHOÁ:Sxx>Syy"
        k, v = a.split("=")
        if k == "drop":
            u, q = v.split("<")
            DROP.add((u, q))
        elif k == "move":
            g, r = v.split(":S")
            src, dst = r.split(">S")
            edit("S" + src, remove=[g])
            edit("S" + dst, add=[g])
        elif k == "goal+":
            st, g = v.split("/")
            edit(st, add=[g])
        elif k == "goal-":
            st, g = v.split("/")
            edit(st, remove=[g])

les, pre0 = pack.lesson_index(cur)
real = {u: {q for q in v if (u, q) not in DROP} for u, v in pre0.items()}
imp = defaultdict(set)
for C, c in cur.items():
    ids = [l["id"] for l in c["lessons"]]
    for a, b in zip(ids, ids[1:]):
        imp[f"{C}:{b}"].add(f"{C}:{a}")
clo = {u: set(real[u]) | (imp[u] if MODE == "cur" else set()) for u in les}
order_pre = {u: set(real[u]) | imp[u] for u in les}

tr = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8"))
prefer = list(tr["prefer"])
for C in cur:
    if C not in prefer:
        prefer.append(C)
key = lambda u: (prefer.index(u.split(":")[0]), int(u.split(":L")[1]))
placed, pos, out, stage_of = set(), {}, [], {}
for k, name, level, goals, intro in STAGES:
    gs = [u for g in goals for u in pack.expand(cur, g)]
    goal_courses = {g.split(":")[0] for g in goals}
    need, stack, why = set(), [(u, None) for u in gs], {}
    while stack:
        u, frm = stack.pop()
        if u in need or u in placed:
            continue
        need.add(u)
        why[u] = frm
        stack += [(q, u) for q in clo[u]]
    ind = {u: len(order_pre[u] & need) for u in need}
    order, ready = [], sorted((u for u in need if ind[u] == 0), key=key)
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in need:
            if u in order_pre[v]:
                ind[v] -= 1
                if ind[v] == 0:
                    ready.append(v)
        ready.sort(key=key)
    if len(order) != len(need):
        print(f"!! chu trình trong {k}: {sorted(need - set(order))[:8]}")
    for u in order:
        pos[u] = len(pos)
        stage_of[u] = k
    placed |= need
    cnt = Counter(u.split(":")[0] for u in order)
    foreign = {C: n for C, n in cnt.items() if C not in goal_courses}
    print(f"{k} {len(order):4d}  " + " ".join(f"{C}{n}" for C, n in cnt.items()))
    if foreign:
        pulls = sorted({(why[u], u) for u in order if u.split(":")[0] not in goal_courses and why[u] and why[u].split(":")[0] in goal_courses})
        print(f"     khoá lạ: {foreign}")
        for a, b in pulls[:40]:
            print(f"       {a} <- {b}")
    out.append((k, order))
missing = set(les) - placed
print("thiếu chỗ:", sorted(missing)[:10])
bad_real = [(u, a) for u in les for a in real[u] if u in pos and a in pos and pos[a] >= pos[u]]
bad_imp = [(u, a) for u in les for a in imp[u] if u in pos and a in pos and pos[a] >= pos[u]]
print(f"vi phạm cạnh THẬT: {len(bad_real)}", bad_real[:10])
print(f"vi phạm cạnh ngầm (bài k+1 đứng trước bài k): {len(bad_imp)}", [(u, a, stage_of[u], stage_of[a]) for u, a in bad_imp][:20])

seq = [u for _, order in out for u in order]
nxt_same = {}
for n, u in enumerate(seq):
    C = u.split(":")[0]
    for v in seq[n + 1:]:
        if v.split(":")[0] == C:
            nxt_same[u] = v.split(":")[1]
            break
REF = re.compile(r"[Bb]ài sau \(bài (\d+)\)")
bad = tot = 0
for C, c in cur.items():
    for l in c["lessons"]:
        spec = l.get("spec")
        if not spec or not (ROOT / spec).exists():
            continue
        text = (ROOT / spec).read_text(encoding="utf-8")
        for m in REF.finditer(text):
            tot += 1
            ref, me = f"{C}:L{int(m.group(1)):02d}", f"{C}:{l['id']}"
            if ref not in pos:
                print(f"NEXT FAIL {me}: hẹn bài {m.group(1)} không có"); bad += 1
            elif pos[ref] <= pos[me]:
                print(f"NEXT FAIL {me}: hẹn {ref} nhưng {ref} đứng TRƯỚC ({stage_of[ref]} < {stage_of[me]})"); bad += 1
            elif nxt_same.get(me) and nxt_same[me] != f"L{int(m.group(1)):02d}":
                print(f"NEXT FAIL {me}: hẹn {ref} nhưng bài kế cùng khoá là {nxt_same[me]}"); bad += 1
print(f"next_refs: {tot} lời hẹn, {bad} lệch")
# khoá bị xé qua nhiều chặng
split = defaultdict(Counter)
for u in seq:
    split[u.split(":")[0]][stage_of[u]] += 1
print("khoá nằm ở > 1 chặng:", {C: dict(v) for C, v in split.items() if len(v) > 1 and C != "PRJ"})
