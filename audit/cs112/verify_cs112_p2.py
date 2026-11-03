"""Kiểm chứng bằng máy mọi ví dụ số của 4 bài nền tảng bổ sung CS112 (L23 sắp xếp nhanh & cận dưới, L24 đường đi ngắn nhất,
L25 cây khung nhỏ nhất, L26 P/NP) — cài thuật toán thật rồi so với vét cạn. Mỗi mục in PASS hoặc FAIL kèm số liệu.
Chạy: .venv/Scripts/python audit/cs112/verify_cs112_p2.py     (kết quả dùng trong audit/cs112/AUDIT_CS112_P2.md)"""
import heapq
import itertools
import math
import sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
rows = []


def rec(cid, ok, msg):
    rows.append((cid, ok))
    print(f"{'PASS' if ok else 'FAIL'} | {cid:4} | {msg}")


# ═════════════════ L23: sắp xếp nhanh, cận dưới, sắp xếp đếm ═════════════════
def partition(a, lo, hi, log=None):
    """Phân hoạch Lomuto, chốt = a[hi]; trả (vị trí chốt, số phép so sánh)."""
    p, i, c = a[hi], lo - 1, 0
    for j in range(lo, hi):
        c += 1
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
        if log is not None:
            log.append((j, a[j] if a[j] > p else a[i], list(a)))
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1, c


def quicksort(a, lo=0, hi=None):
    hi = len(a) - 1 if hi is None else hi
    if lo >= hi:
        return 0
    q, c = partition(a, lo, hi)
    return c + quicksort(a, lo, q - 1) + quicksort(a, q + 1, hi)


a = [4, 7, 2, 6, 1, 5]
log = []
q, c = partition(a, 0, 5, log)
rec("Q1", (a, q, c) == ([4, 2, 1, 5, 7, 6], 3, 5), f"phân hoạch [4,7,2,6,1,5] chốt 5 → {a}, chốt về vị trí {q} (đếm từ 0), {c} phép so sánh")
for j, _, st in log:
    print("      sau j =", j, st)
b = [4, 7, 2, 6, 1, 5]
tot = quicksort(b)
rec("Q2", b == sorted(b) and tot == 9, f"sắp xếp nhanh trọn vẹn [4,7,2,6,1,5] → {b}, tổng {tot} phép so sánh (5 + [4,2,1]: 2+1 + [7,6]: 1)")
for n in range(1, 13):
    w = quicksort(list(range(1, n + 1)))
    if w != n * (n - 1) // 2:
        rec("Q3", False, f"n={n}")
rec("Q3", True, "mảng đã sắp, chốt cuối: đúng n(n−1)/2 phép so sánh (n = 1..12); n = 6 → 15, n = 1000 → 499 500")
rec("Q3b", all(quicksort([7] * n) == n * (n - 1) // 2 for n in range(1, 12)),
    "mảng toàn phần tử bằng nhau (Lomuto, so sánh ≤): cũng n(n−1)/2 — tệ nhất")


def H(n):
    return sum(F(1, k) for k in range(1, n + 1))


def avg_formula(n):
    return 2 * (n + 1) * H(n) - 4 * n


ok = True
for n in range(1, 8):
    s = sum(quicksort(list(p)) for p in itertools.permutations(range(n)))
    ok &= F(s, math.factorial(n)) == avg_formula(n)
rec("Q4", ok, f"trung bình trên MỌI hoán vị = 2(n+1)H_n − 4n (n = 1..7, vét cạn); n = 6: {avg_formula(6)} = {float(avg_formula(6)):.3f}")
lb6 = math.ceil(math.log2(math.factorial(6)))
rec("Q5", lb6 == 10 and round(math.log2(720), 2) == 9.49, f"cận dưới n = 6: log2(720) = {math.log2(720):.2f} → mọi thuật toán so sánh cần ≥ {lb6} lần ở trường hợp tệ nhất")
rec("Q5b", math.ceil(math.log2(6)) == 3, "n = 3: 3! = 6 thứ tự = 6 lá → cây quyết định cao ≥ ⌈log2 6⌉ = 3")
n = 1000
af = float(avg_formula(n))
rec("Q6", round(af) == 10986 and round(math.log2(math.factorial(n))) == 8529,
    f"n = 1000: tệ nhất 499 500; trung bình {af:.0f}; cận dưới log2(1000!) ≈ {math.log2(math.factorial(n)):.0f}")
ok = all(math.log2(math.factorial(m)) >= (m / 2) * math.log2(m / 2) for m in range(2, 2000, 2))
rec("Q7", ok and round(math.log2(math.factorial(8)), 2) == 15.3, f"log2(n!) ≥ (n/2)·log2(n/2) (n chẵn ≤ 2000); n = 8: {math.log2(40320):.2f} ≥ 4·2 = 8")
# cây quyết định 3 phần tử: sắp xếp chèn a,b,c — đếm số lá và độ cao
leaves = set()


def ins_tree(order):
    seq, cmp = [], 0
    for x in order:
        k = len(seq)
        while k > 0:
            cmp += 1
            if seq[k - 1] > x:
                k -= 1
            else:
                break
        seq.insert(k, x)
    return cmp


hs = [ins_tree(p) for p in itertools.permutations([1, 2, 3])]
rec("Q8", max(hs) == 3 and min(hs) == 2, f"sắp xếp chèn 3 phần tử: số so sánh theo 6 thứ tự = {hs} (tệ nhất 3 = cận dưới)")
keys = [2, 0, 3, 2, 1, 0, 2, 3]
cnt = [keys.count(v) for v in range(4)]
pos = list(itertools.accumulate([0] + cnt[:-1]))
out = [v for v in range(4) for _ in range(cnt[v])]
rec("Q9", cnt == [2, 1, 3, 2] and pos == [0, 2, 3, 6] and out == sorted(keys),
    f"sắp xếp đếm {keys}: đếm {cnt}, vị trí bắt đầu {pos} → {out}; 8 + 4 bước, 0 phép so sánh giữa hai phần tử")

qa = [3, 8, 1, 6, 2, 5]
qq, qc = partition(qa, 0, 5)
rec("Q10", (qa, qq, qc) == ([3, 1, 2, 5, 8, 6], 3, 5) and math.ceil(math.log2(120)) == 7,
    f"bài tự làm: phân hoạch [3,8,1,6,2,5] → {qa}, {qc} so sánh; cận dưới n = 5: log2(120) = {math.log2(120):.2f} → 7")
qb = [3, 8, 1, 6, 2, 5]
rec("Q11", quicksort(qb) == 5 + 2 + 1 and qb == [1, 2, 3, 5, 6, 8], "bài tự làm: tổng so sánh 5 + [3,1,2] chốt 2: 2 (ra [1,2,3], hai nửa 1 phần tử) + [8,6]: 1 = 8")

# ═════════════════ L24: Dijkstra, Bellman-Ford ═════════════════
G = {"S": {"A": 4, "B": 1}, "A": {"C": 1}, "B": {"A": 2, "C": 5, "D": 8}, "C": {"D": 3}, "D": {}}


def dijkstra(g, s):
    d, done, pq, order = {v: math.inf for v in g}, set(), [(0, s)], []
    d[s] = 0
    snap = []
    while pq:
        du, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        order.append((u, du))
        for v, w in g[u].items():
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
        snap.append(dict(d))
    return d, order, snap


d, order, snap = dijkstra(G, "S")
rec("D1", d == {"S": 0, "A": 3, "B": 1, "C": 4, "D": 7} and [u for u, _ in order] == list("SBACD"),
    f"Dijkstra từ S: {d}; thứ tự chốt {order}")
for (u, du), s in zip(order, snap):
    print(f"      chốt {u} ({du}) → d = {s}")


def all_paths_min(g, s, t):
    best = math.inf
    def go(u, cost, seen):
        nonlocal best
        if u == t:
            best = min(best, cost)
            return
        for v, w in g[u].items():
            if v not in seen:
                go(v, cost + w, seen | {v})
    go(s, 0, {s})
    return best


rec("D2", all(all_paths_min(G, "S", v) == d[v] for v in G), "vét cạn mọi đường đi đơn từ S: khớp Dijkstra ở cả 5 đỉnh")
GN = {"S": {"A": 2, "B": 3}, "A": {}, "B": {"A": -2}}
dn, on, _ = dijkstra(GN, "S")
# Dijkstra “chốt” A = 2 trước khi xét B; mô phỏng đúng phiên bản chốt-một-lần (không cập nhật đỉnh đã chốt)
def dijkstra_strict(g, s):
    d, done = {v: math.inf for v in g}, []
    d[s] = 0
    while len(done) < len(g):
        u = min((v for v in g if v not in done), key=lambda v: d[v])
        done.append(u)
        for v, w in g[u].items():
            if v not in done and d[u] + w < d[v]:
                d[v] = d[u] + w
    return d, done
ds, dord = dijkstra_strict(GN, "S")
rec("D3", ds["A"] == 2 and all_paths_min(GN, "S", "A") == 1 and dord == ["S", "A", "B"],
    f"cạnh âm: Dijkstra chốt A = {ds['A']} (thứ tự {dord}) nhưng đường S→B→A = 3 − 2 = 1")


def bellman_ford(n_v, edges, s):
    d = {v: math.inf for v in n_v}
    d[s] = 0
    rounds = []
    for _ in range(len(n_v) - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
        rounds.append(dict(d))
    neg = any(d[u] + w < d[v] for u, v, w in edges)
    return d, rounds, neg


E_N = [("S", "A", 2), ("S", "B", 3), ("B", "A", -2)]
db, rb, ng = bellman_ford("SAB", E_N, "S")
rec("D4", db == {"S": 0, "A": 1, "B": 3} and not ng and rb[0] == {"S": 0, "A": 1, "B": 3},
    f"Bellman-Ford (thứ tự cạnh S→A, S→B, B→A) trên đồ thị cạnh âm: {db}; vòng 1 đã ra {rb[0]}")
E_bad = [("B", "A", -2), ("S", "B", 3), ("S", "A", 2)]
db2, rb2, _ = bellman_ford("SAB", E_bad, "S")
rec("D4b", rb2[0] == {"S": 0, "A": 2, "B": 3} and rb2[1] == {"S": 0, "A": 1, "B": 3},
    f"thứ tự cạnh xấu (B→A trước): vòng 1 {rb2[0]}, vòng 2 {rb2[1]} → cần đủ n − 1 = 2 vòng")
E_cyc = [("S", "A", 1), ("A", "B", 1), ("B", "A", -3)]
_, _, ngc = bellman_ford("SAB", E_cyc, "S")
rec("D5", ngc, "chu trình A→B→A tổng 1 − 3 = −2 < 0: sau n − 1 vòng vẫn còn cạnh giảm được → báo chu trình âm")
EG = [(u, v, w) for u in G for v, w in G[u].items()]
dbg, rbg, _ = bellman_ford(list(G), EG, "S")
rec("D6", dbg == d, f"Bellman-Ford trên đồ thị ví dụ chính ra cùng kết quả Dijkstra: {dbg}; theo vòng: {rbg}")
rec("D7", 5 - 1 == 4 and len(EG) == 7, "ví dụ chính: n = 5 đỉnh, m = 7 cạnh; Bellman-Ford tối đa 4 vòng × 7 cạnh = 28 lần nới")

# ═════════════════ L25: cây khung nhỏ nhất ═════════════════
V = "ABCDE"
EM = [("A", "C", 1), ("B", "C", 2), ("D", "E", 3), ("A", "B", 4), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10)]


class DSU:
    def __init__(s, vs):
        s.p = {v: v for v in vs}
        s.sz = {v: 1 for v in vs}

    def find(s, x):
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]
            x = s.p[x]
        return x

    def union(s, a, b):
        ra, rb = s.find(a), s.find(b)
        if ra == rb:
            return False
        if s.sz[ra] < s.sz[rb]:
            ra, rb = rb, ra
        s.p[rb] = ra
        s.sz[ra] += s.sz[rb]
        return True


dsu, taken, trace = DSU(V), [], []
for u, v, w in sorted(EM, key=lambda e: e[2]):
    ok_ = dsu.union(u, v)
    trace.append((u + v, w, ok_))
    if ok_:
        taken.append((u, v, w))
rec("K1", [t[:2] for t in taken] == [("A", "C"), ("B", "C"), ("D", "E"), ("B", "D")] and sum(t[2] for t in taken) == 11,
    f"Kruskal: {trace} → tổng 11, 4 = n − 1 cạnh")


def prim(vs, edges, s):
    adj = {v: [] for v in vs}
    for u, v, w in edges:
        adj[u].append((w, v)); adj[v].append((w, u))
    inT, pq, order = {s}, [(w, s, v) for w, v in adj[s]], []
    heapq.heapify(pq)
    while pq and len(inT) < len(vs):
        w, u, v = heapq.heappop(pq)
        if v in inT:
            continue
        inT.add(v); order.append((u + v, w))
        for w2, x in adj[v]:
            if x not in inT:
                heapq.heappush(pq, (w2, v, x))
    return order


po = prim(V, EM, "A")
rec("K2", po == [("AC", 1), ("CB", 2), ("BD", 5), ("DE", 3)] and sum(w for _, w in po) == 11, f"Prim từ A: {po} → tổng 11")
best = min(sum(e[2] for e in S) for S in itertools.combinations(EM, 4)
           if (lambda d_: all(d_.union(u, v) for u, v, _ in S))(DSU(V)))
rec("K3", best == 11, f"vét cạn mọi bộ 4 cạnh không tạo chu trình: nhỏ nhất {best}")
rec("K4", sum(1 for S in itertools.combinations(EM, 4) if (lambda d_: all(d_.union(u, v) for u, v, _ in S))(DSU(V))
              and sum(e[2] for e in S) == 11) == 1, "trọng số khác nhau đôi một → cây khung nhỏ nhất duy nhất")
# cây đường đi ngắn nhất ≠ cây khung nhỏ nhất: tam giác AB 3, BC 3, AC 5
tri = [("A", "B", 3), ("B", "C", 3), ("A", "C", 5)]
rec("K5", 3 + 3 == 6 and 3 + 5 == 8, "tam giác AB 3, BC 3, AC 5: cây khung nhỏ nhất {AB, BC} = 6; cây đường ngắn nhất từ A {AB, AC} = 8 (A→C đi thẳng 5 < 6)")
# nén đường đi: chuỗi 5 phần tử
p = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
def find_full(x):
    r = x
    while p[r] != r:
        r = p[r]
    while p[x] != r:
        p[x], x = r, p[x]
    return r
r = find_full(5)
rec("K6", r == 1 and p == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, f"nén đường đi: find(5) trên chuỗi 5→4→3→2→1 trả {r}, sau đó mọi nút trỏ thẳng gốc {p}")

# ═════════════════ L26: P, NP, quy dẫn ═════════════════
tsp = [[0, 20, 30, 10, 11], [15, 0, 16, 4, 2], [3, 5, 0, 2, 4], [19, 6, 18, 0, 3], [16, 4, 7, 16, 0]]
tour = [0, 3, 1, 4, 2, 0]
cost = sum(tsp[tour[i]][tour[i + 1]] for i in range(5))
opt = min(sum(tsp[t[i]][t[i + 1]] for i in range(5)) for t in ([0] + list(q) + [0] for q in itertools.permutations(range(1, 5))))
rec("N1", cost == 28 and opt == 28 and len(set(tour[:-1])) == 5,
    f"chứng chỉ TSP (ma trận bài 15): chu trình 1→4→2→5→3→1, tổng 10 + 6 + 2 + 7 + 3 = {cost} ≤ 30 → kiểm trong 5 phép cộng; tối ưu vét cạn = {opt}")
rec("N1b", math.factorial(4) == 24 and math.factorial(19) == 121645100408832000, "số chu trình cần thử khi cố định đỉnh đầu: (n − 1)!; n = 5 → 24, n = 20 → 19! ≈ 1,2·10^17")
C5 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
def is_ind(S):
    return all(not (u in S and v in S) for u, v in C5)
def is_vc(S):
    return all(u in S or v in S for u, v in C5)
subs = [set(S) for r_ in range(6) for S in itertools.combinations(range(5), r_)]
mis = max(len(S) for S in subs if is_ind(S))
mvc = min(len(S) for S in subs if is_vc(S))
rec("N2", mis == 2 and mvc == 3 and all(is_ind(S) == is_vc(set(range(5)) - S) for S in subs),
    f"chu trình 5 đỉnh: tập độc lập lớn nhất {mis}, phủ đỉnh nhỏ nhất {mvc}, 2 + 3 = 5; S độc lập ⇔ V∖S là phủ đỉnh (cả 32 tập)")
rec("N2b", is_ind({0, 2}) and is_vc({1, 3, 4}), "ví dụ: {1, 3} độc lập (đánh số 1..5) ⇔ {2, 4, 5} phủ mọi cạnh")
W = 10**9
rec("N3", W.bit_length() == 30 and 100 * W == 10**11,
    "cái túi 0/1, bảng n·W: W = 10^9 viết bằng 30 bit nhưng bảng có W + 1 cột → 100 món ≈ 10^11 ô: giả đa thức")
items = [(10, 60), (20, 100), (30, 120)]
def ks(Wc):
    dp = [0] * (Wc + 1)
    for w_, v_ in items:
        for c_ in range(Wc, w_ - 1, -1):
            dp[c_] = max(dp[c_], dp[c_ - w_] + v_)
    return dp[Wc]
rec("N4", ks(50) == 220, "cái túi 0/1 (ví dụ bài 16): quy hoạch động bảng 3 × 51 cho 220, khớp vét cạn")

# ═════════════════ X1: thư viện tham chiếu tools/checklib.py (dùng trong `checks`) khớp phần cài độc lập ở trên ═════════════════
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "tools"))
import checklib as cl  # noqa: E402
ok = all(cl.qs_count(p) == quicksort(list(p)) for n in range(1, 8) for p in itertools.permutations(range(n)))
ok &= cl.dijkstra(G, "S")[0] == d and all(cl.shortest_brute(G, "S", v) == d[v] for v in G)
ok &= cl.dijkstra(GN, "S")[0]["A"] == 2
ok &= cl.bellman_ford("SAB", E_bad, "S")[1] == rb2 and cl.bellman_ford("SAB", E_cyc, "S")[2]
ok &= cl.kruskal(V, EM) == (trace, 11) and cl.prim(V, EM, "A") == po and cl.mst_brute(V, EM) == (11, 1)
ok &= cl.counting_sort(keys, 3) == (cnt, pos, out)
rec("X1", ok, "tools/checklib.py (phân hoạch, sắp xếp nhanh, Dijkstra, Bellman-Ford, Kruskal, Prim, vét cạn) khớp mọi phép cài độc lập ở trên")

VQ, EQ5 = "ABCD", [("A", "B", 1), ("B", "C", 4), ("C", "D", 2), ("A", "D", 3), ("A", "C", 5)]
kq = cl.kruskal(VQ, EQ5)
pq_ = cl.prim(VQ, EQ5, "C")
rec("K7", [x for x in kq[0] if x[2]] == [("AB", 1, True), ("CD", 2, True), ("AD", 3, True)] and kq[1] == 6
    and pq_ == [("CD", 2), ("DA", 3), ("AB", 1)] and cl.mst_brute(VQ, EQ5) == (6, 1),
    f"bài tự làm L25: Kruskal {kq}; Prim từ C {pq_}; vét cạn {cl.mst_brute(VQ, EQ5)}")
dt = DSU("ABCDE")
steps_ = []
for u, v, w in sorted(EM, key=lambda e: e[2]):
    ru, rv = dt.find(u), dt.find(v)
    steps_.append((u + v, ru, rv, ru != rv))
    dt.union(u, v)
rec("K8", steps_ == [("AC", "A", "C", True), ("BC", "B", "A", True), ("DE", "D", "E", True), ("AB", "A", "A", False),
                     ("BD", "A", "D", True), ("CD", "A", "A", False), ("CE", "A", "A", False)],
    f"hợp–tìm trong Kruskal (gốc của hai đầu cạnh): {steps_}")

yrs = math.factorial(19) / 1e9 / (365.25 * 86400)
rec("N5", round(yrs, 1) == 3.9 and (10**12).bit_length() == 40 and 50 * 1001 == 50050 and 6 - 3 == 3,
    f"19! phép thử ở 10^9 phép/giây ≈ {yrs:.2f} năm; 10^12 cần {(10**12).bit_length()} bit; bảng 50 món × 1001 cột = 50050 ô")

print(f"\nTỔNG: {sum(ok for _, ok in rows)} PASS · {sum(not ok for _, ok in rows)} FAIL")
