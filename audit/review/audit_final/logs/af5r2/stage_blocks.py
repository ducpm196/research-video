"""CHỈ ĐỌC: với thành viên chặng tường minh (phương án v3), xét đồ thị phụ thuộc MỨC KHOÁ trong từng chặng:
khoá X -> khoá Y nếu có bài của X cần một bài của Y (cạnh thật, sau khi bỏ các cạnh trong DROP). Nếu không có chu trình thì
xếp nguyên khối từng khoá (0 lần đan xen). In chu trình (nếu có) và thứ tự khối đề xuất + số lần đổi khoá khi sắp tô pô theo thứ tự đó."""
import sys, itertools
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack
cur = pack.load_cur()
DROP = {tuple(a.split("<")) for a in sys.argv[1:]}
MEM = {"S01": ["FND", "JVA", "JV2", "PYT"], "S02": ["BNK"], "S03": ["BNX"], "S04": ["INT", "ACB"], "S05": ["DMS", "CS112", "CS115a"],
       "S06": ["CPR", "LNX", "CSA", "OSY", "NET"], "S07": ["SWF", "SDP", "DBS", "WEB", "SEC"],
       "S08": ["DSY", "EVT", "DEN", "CLD", "DVO", "CLC", "SAR"],
       "S09": ["CS115b", "AIF", "DAN", "DSC", "MLP", "MLO", "IRS", "LLM", "AGT", "RLN", "CVI"],
       "S10": ["TOC", "PLC", "PAR", "HCI", "SEP", "CAS"], "S11": ["RBM", "ESY", "ROB", "GFX", "BCH"]}
def blk(u):
    C, i = u.split(":")
    if C == "CS115":
        n = int(i[1:]); return "CS115a" if (n <= 21 or n >= 44) else "CS115b"
    return C
les, pre = pack.lesson_index(cur)
for st, cs in MEM.items():
    dep = defaultdict(set); ev = defaultdict(list)
    for u in les:
        if blk(u) not in cs: continue
        for q in pre[u]:
            if (u, q) in DROP: continue
            if blk(q) in cs and blk(q) != blk(u):
                dep[blk(u)].add(blk(q)); ev[(blk(u), blk(q))].append(f"{u}<-{q}")
    # tô pô mức khoá
    order, left = [], list(cs)
    while left:
        free = [c for c in left if not (dep[c] & set(left))]
        if not free: break
        order.append(free[0]); left.remove(free[0])
    if left:
        print(f"{st}: CHU TRÌNH mức khoá giữa {left}")
        for a in left:
            for b in dep[a] & set(left):
                print(f"    {a} cần {b}: {ev[(a, b)][:6]}")
    else:
        print(f"{st}: xếp nguyên khối được: {' → '.join(order)}")
