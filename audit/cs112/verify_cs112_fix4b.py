"""Kiểm độc lập các số/điều kiện đã sửa ở fix4_CS112_B (CS112 L15–L29). Chạy: .venv/Scripts/python -B audit/cs112/verify_cs112_fix4b.py"""
import heapq
import itertools
import math
import runpy
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")
CALC = runpy.run_path("audit/cs112/af2b_calc.py")
fails = 0


def rec(name, ok, detail=""):
    global fails
    fails += 0 if ok else 1
    print(("PASS" if ok else "FAIL"), name, detail)


INF = math.inf
# L15: cận con 1→3 của ma trận 5x5: 53 khi cấm j→1, 42 khi bỏ cấm (tự rút gọn lại, không dùng tsp_bb)
C = [[INF, 20, 30, 10, 11], [15, INF, 16, 4, 2], [3, 5, INF, 2, 4], [19, 6, 18, INF, 3], [16, 4, 7, 16, INF]]


def reduce(M):
    M = [r[:] for r in M]
    t = 0
    for i in range(len(M)):
        m = min(M[i])
        if 0 < m < INF:
            M[i] = [v - m for v in M[i]]
            t += m
    for j in range(len(M)):
        m = min(r[j] for r in M)
        if 0 < m < INF:
            for r in M:
                r[j] -= m
            t += m
    return M, t


R0, lb0 = reduce(C)


def child(forbid):
    N = [r[:] for r in R0]
    c = N[0][2]
    for k in range(5):
        N[0][k] = INF
        N[k][2] = INF
    if forbid:
        N[2][0] = INF
    return lb0 + c + reduce(N)[1]


rec("L15 cận con 1→3", (lb0, child(True), child(False)) == (25, 53, 42), (lb0, child(True), child(False)))

# L18: cây lời gọi F(5) ghi nhớ có 9 nút (đếm đệ quy riêng)
seen, cnt = set(), [0]


def f(k):
    cnt[0] += 1
    if k in seen or k < 2:
        return
    seen.add(k)
    f(k - 1), f(k - 2)


f(5)
rec("L18 F(5) ghi nhớ 9 lời gọi (thô 15)", cnt[0] == 9 and CALC["fib_naive_calls"](5) == 15, cnt[0])


# L24: số lần nới đúng định nghĩa (chỉ cạnh tới đỉnh chưa chốt), quét mảng O(n^2), hoà theo chỉ số nhỏ
def dij_tried(n, E):
    adj = [[] for _ in range(n)]
    for u, v, w in E:
        adj[u].append((v, w))
    d = [INF] * n
    d[0] = 0
    done = [False] * n
    tried = 0
    h = [(0, 0)]
    while h:
        du, u = heapq.heappop(h)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            if not done[v]:
                tried += 1
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(h, (d[v], v))
    return tried


E1, E2 = CALC["sp_graph"](1000, 5000), CALC["sp_graph"](10000, 50000)
rec("L24 số lần nới 2455 / 25182", (dij_tried(1000, E1), dij_tried(10000, E2)) == (2455, 25182) and
    (CALC["dijkstra_ops"](1000, E1)[1], CALC["dijkstra_ops"](10000, E2)[1]) == (4967, 49641))

# L24: chu trình âm không tới được từ S: Bellman–Ford không thấy; tới được thì thấy
def bf_neg(vs, E, s):
    d = {v: INF for v in vs}
    d[s] = 0
    for _ in range(len(vs) - 1):
        for u, v, w in E:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return any(d[u] + w < d[v] for u, v, w in E)


rec("L24 chu trình âm không tới được từ S bị bỏ sót", bf_neg("SABC", [("S", "A", 1), ("B", "C", 1), ("C", "B", -3)], "S") is False
    and bf_neg("SAB", [("S", "A", 1), ("A", "B", 1), ("B", "A", -3)], "S") is True)


# L25: so sánh khi sắp cạnh TĂNG dần (sắp trộn từ trên xuống, ổn định): 195 / 54676 / 637336
def merge_cmp(a):
    c = 0

    def ms(v):
        nonlocal c
        if len(v) < 2:
            return v
        l, r = ms(v[:len(v) // 2]), ms(v[len(v) // 2:])
        o, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            c += 1
            if l[i] <= r[j]:
                o.append(l[i]); i += 1
            else:
                o.append(r[j]); j += 1
        return o + l[i:] + r[j:]
    assert ms(list(a)) == sorted(a)
    return c


got = tuple(merge_cmp([w for _, _, w in CALC["complete_graph"](n)]) for n in (10, 100, 300))
rec("L25 so sánh sắp tăng 195 / 54676 / 637336", got == (195, 54676, 637336), got)

# L28: sắp xếp nhanh trên mảng đã sắp, n = 16: 120 so sánh so với 16 log2 16 = 64; n = 6: 15 < 15,51 (không phân biệt)
def qs_cmp(a):
    c = 0

    def qs(lo, hi):
        nonlocal c
        if lo >= hi:
            return
        p, i = a[hi], lo - 1
        for j in range(lo, hi):
            c += 1
            if a[j] <= p:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        qs(lo, i)
        qs(i + 2, hi)
    qs(0, len(a) - 1)
    return c


rec("L28 bẫy 16", qs_cmp(list(range(16))) == 120 and 16 * math.log2(16) == 64 and qs_cmp(list(range(6))) == 15 and 6 * math.log2(6) > 15)

# L28 bẫy 18: tam giác 3, 3, 5, nguồn ở đỉnh giữa cạnh 5 và một cạnh 3 → cây đường ngắn nhất 8, cây khung nhỏ nhất 6; nguồn giữa hai cạnh 3 → 6
E = {("A", "B"): 3, ("B", "C"): 3, ("A", "C"): 5}
w = lambda x, y: E.get((x, y), E.get((y, x)))
d_A = {"A": 0, "B": 3, "C": min(5, 3 + 3)}
spt_A = sum(min(w(u, v) for u in "ABC" if u != v and d_A[u] + w(u, v) == d_A[v]) for v in "BC")
mst = min(w(*e) + w(*f2) for e, f2 in itertools.combinations([("A", "B"), ("B", "C"), ("A", "C")], 2))
d_B = {"B": 0, "A": 3, "C": 3}
spt_B = 3 + 3
rec("L28 bẫy 18", (spt_A, mst, spt_B) == (8, 6, 6), (spt_A, mst, spt_B))

# L27: ngoại suy vét cạn n = 20 từ n = 15 (nhân 3 mỗi bước): ≈ 520 s ≈ 9 phút
rec("L27 ngoại suy n=20", round(2138 * 3 ** 5 / 1000) == 520 and round(2138 * 3 ** 5 / 60000) == 9)

# L21: (24,0), (0,24) thuộc đường x1 + x2 = 24; gốc thoả bất đẳng thức
rec("L21 điểm trên đường", all(a + b == 24 for a, b in ((24, 0), (0, 24))) and 0 + 0 <= 24)

# L29: 2^26 phần tử × 8 = 536 870 912 > 500 triệu
rec("L29 2^26·8", 2 ** 26 * 8 == 536870912 > 5 * 10 ** 8)
print("FAIL" if fails else "ALL PASS", fails)
sys.exit(1 if fails else 0)
