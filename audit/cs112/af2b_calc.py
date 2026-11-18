"""Hàm tính độc lập cho các cảnh quy mô (`scale`) và lab của CS112 L15–L29 (nâng chuẩn AF2, 2026-11-14).
Dùng từ `checks:` của bài:  __import__('runpy').run_path('audit/cs112/af2b_calc.py')['tsp_nodes'](12)
và từ audit/cs112/verify_cs112_af2b.py. Mọi số trên màn hình của cảnh quy mô đều lấy từ đây (đếm phép tính tất định, không đo giờ)."""
import heapq
import itertools
import math
import runpy

INF = math.inf
_TB = None


def _tsp():
    global _TB
    if _TB is None:
        _TB = runpy.run_path("audit/cs112/tsp_bb.py")
    return _TB


# ───────────── L15: nhánh cận TSP ─────────────
def tsp_matrix(n, seed=1):
    """Ma trận chi phí giả lập tất định: bộ sinh đồng dư tuyến tính, chi phí 1..50, đường chéo ∞."""
    x, M = seed, []
    for i in range(n):
        row = []
        for j in range(n):
            x = (x * 1103515245 + 12345) % 2147483648
            row.append(INF if i == j else 1 + (x >> 16) % 50)
        M.append(row)
    return M


def tsp_full_nodes(n):
    """Số nút của cây đầy đủ (kể cả gốc): tổng (n−1)!/(n−1−k)! với k = 0..n−1."""
    return sum(math.factorial(n - 1) // math.factorial(n - 1 - k) for k in range(n))


def tsp_nodes(n, seed=1):
    """(chi phí tối ưu, số nút nhánh cận sinh ra kể cả gốc) — mở nút có cận dưới nhỏ nhất trước."""
    tb = _tsp()
    reduce, child = tb["reduce"], tb["child"]
    C = tsp_matrix(n, seed)
    R0, lb0 = reduce(C)
    heap, best, nodes = [(lb0, [0], R0)], INF, 1
    while heap:
        lb, path, M = heapq.heappop(heap)
        if lb >= best:
            continue
        if len(path) == n:
            best = lb
            continue
        for j in range(n):
            if j not in path:
                M2, lb2 = child(M, lb, path[-1], j)
                nodes += 1
                if lb2 < best:
                    heapq.heappush(heap, (lb2, path + [j], M2))
    return best, nodes


def tsp_brute(C):
    n = len(C)
    return min(sum(C[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, n)))


def tsp5_child_lb(i, j, forbid=True):
    """Cận dưới của nút con i→j (0-based) của ma trận 5x5 của bài L15, có / không cấm đường j→1 (fix4_CS112_B)."""
    tb = _tsp()
    R0, lb0 = tb["reduce"](tb["C"])
    N = [r[:] for r in R0]
    cost = N[i][j]
    for k in range(len(N)):
        N[i][k] = INF
        N[k][j] = INF
    if forbid:
        N[j][0] = INF
    return lb0 + cost + tb["reduce"](N)[1]


# ───────────── L16: tham lam (cái túi phân số) ─────────────
def lcg_list(n, seed=1, mod=1000003):
    x, out = seed, []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(1 + (x >> 8) % mod)
    return out


def sort_compares(a, desc=True):
    """Số lần so sánh hai phần tử của sắp xếp trộn từ trên xuống (tự cài, đếm từng phép so sánh; không phụ thuộc phiên bản Python).
    desc=True: sắp giảm dần (L16, như cũ); desc=False: sắp TĂNG dần (Kruskal, L25: fix4_CS112_B)."""
    c = [0]

    def ms(v):
        if len(v) <= 1:
            return v
        mid = len(v) // 2
        l, r = ms(v[:mid]), ms(v[mid:])
        out, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            c[0] += 1
            if (l[i] >= r[j]) if desc else (l[i] <= r[j]):
                out.append(l[i]); i += 1
            else:
                out.append(r[j]); j += 1
        return out + l[i:] + r[j:]
    ms(list(a))
    return c[0]


def greedy_steps(n, seed=1):
    """(số lần so sánh khi sắp n đơn giá, n) — chi phí tham lam = sắp xếp + một vòng n bước."""
    return sort_compares(lcg_list(n, seed)), n


# ───────────── L17: xếp lịch hội trường ─────────────
def pick_events(ds, mode="end"):
    """Tham lam chọn sự kiện; mode: end (kết thúc sớm nhất), start (bắt đầu sớm nhất), len (ngắn nhất). Trả về số hiệu từ 1."""
    key = {"end": lambda i: ds[i][1], "start": lambda i: ds[i][0], "len": lambda i: ds[i][1] - ds[i][0]}[mode]
    last, out = -1, []
    for i in sorted(range(len(ds)), key=key):
        if ds[i][0] >= last:
            out.append(i + 1)
            last = ds[i][1]
    return out


def max_events(ds):
    """Số sự kiện lớn nhất không chồng giờ, vét cạn mọi tập con."""
    for k in range(len(ds), 0, -1):
        for S in itertools.combinations(ds, k):
            if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(S, 2)):
                return k


# ───────────── L18: quy hoạch động ─────────────
def fib_naive_calls(n):
    """Số lời gọi của F(n) đệ quy thô = 2F(n+1) − 1 (tính bằng công thức đóng, kiểm bằng đếm thật ở verify)."""
    a, b = 0, 1
    for _ in range(n + 1):
        a, b = b, a + b
    return 2 * a - 1


def fib_memo_calls(n):
    memo, c = {}, [0]

    def F(k):
        c[0] += 1
        if k in memo:
            return memo[k]
        memo[k] = k if k < 2 else F(k - 1) + F(k - 2)
        return memo[k]
    F(n)
    return c[0]


def coin_calls(a, coins=(1, 3, 4)):
    """(số đồng ít nhất, số lời gọi) của đệ quy thô f(x) = 1 + min f(x − c); mỗi lần gọi f tính một lần, kể cả x = 0."""
    c = [0]

    def f(x):
        c[0] += 1
        return 0 if x == 0 else 1 + min(f(x - k) for k in coins if k <= x)
    return f(a), c[0]


def coin_memo_calls(a, coins=(1, 3, 4)):
    memo, c = {}, [0]

    def f(x):
        c[0] += 1
        if x in memo:
            return memo[x]
        memo[x] = 0 if x == 0 else 1 + min(f(x - k) for k in coins if k <= x)
        return memo[x]
    return f(a), c[0]


def coin_table_ops(a_max, coins=(1, 3, 4)):
    """Số phép 1 + dp[a − c] khi lập bảng từ dưới lên tới a_max: số cặp (a, c) với c ≤ a."""
    return sum(1 for a in range(1, a_max + 1) for c in coins if c <= a)


def coin_dp(a_max, coins):
    dp = [0] * (a_max + 1)
    for a in range(1, a_max + 1):
        dp[a] = 1 + min(dp[a - c] for c in coins if c <= a)
    return dp


def coin_greedy(a, coins):
    n = 0
    for c in sorted(coins, reverse=True):
        n += a // c
        a %= c
    return n


def coin_greedy_wrong(a_max, coins):
    dp = coin_dp(a_max, coins)
    return [a for a in range(1, a_max + 1) if coin_greedy(a, coins) > dp[a]]


# ───────────── L19: quy hoạch động theo đoạn ─────────────
def mcm_trials(n):
    """Số lần tính biểu thức trong min khi lập bảng nhân n ma trận: đếm cặp (đoạn, chỗ cắt) bằng ba vòng lặp thật."""
    c = 0
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            c += L - 1
    return c


def catalan(k):
    return math.comb(2 * k, k) // (k + 1)


def mcm_cost(p):
    """Số phép nhân ít nhất cho chuỗi ma trận cỡ p (chỉ số từ 1), bằng đệ quy ghi nhớ từ trên xuống (khác cách lập bảng của lab)."""
    memo = {}

    def f(i, j):
        if i == j:
            return 0
        if (i, j) not in memo:
            memo[(i, j)] = min(f(i, k) + f(k + 1, j) + p[i - 1] * p[k] * p[j] for k in range(i, j))
        return memo[(i, j)]
    return f(1, len(p) - 1)


# ───────────── L20: LIS và LCS ─────────────
def lis_table(a):
    """(bảng L, số lần so sánh a[j] < a[i]) của cách lập bảng Θ(n²), dãy con tăng hẳn."""
    n, L, c = len(a), [1] * len(a), 0
    for i in range(n):
        for j in range(i):
            c += 1
            if a[j] < a[i]:
                L[i] = max(L[i], L[j] + 1)
    return L, c


def lcs_len(x, y):
    c = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            c[i][j] = c[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(c[i - 1][j], c[i][j - 1])
    return c[len(x)][len(y)]


# ───────────── L21: quy hoạch tuyến tính hai biến ─────────────
def lp2_vertices(cons):
    """cons = [(a, b, c)] nghĩa a·x1 + b·x2 ≤ c, thêm x1, x2 ≥ 0. Trả về (số cặp đường giải được, các giao điểm, đỉnh hợp lệ) bằng Fraction."""
    from fractions import Fraction
    lines = list(cons) + [(1, 0, 0), (0, 1, 0)]
    solved, pts, ok = 0, [], []
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        solved += 1
        x, y = Fraction(c1 * b2 - c2 * b1, det), Fraction(a1 * c2 - a2 * c1, det)
        pts.append((x, y))
        if x >= 0 and y >= 0 and all(a * x + b * y <= c for a, b, c in cons):
            ok.append((x, y))
    return solved, pts, sorted(set(ok))


def lp_candidates(n):
    """Số cách chọn n đường biên trong 2n đường (n ràng buộc + n điều kiện không âm)."""
    return math.comb(2 * n, n)


# ───────────── L22: đơn hình ─────────────
def simplex(c, A, b, rule="dantzig"):
    """Đơn hình bảng (Fraction): lớn nhất c·x với A x ≤ b, x ≥ 0, b ≥ 0 (gốc toạ độ hợp lệ).
    rule 'dantzig': cột vào = hệ số âm nhất (hoà → chỉ số nhỏ nhất); 'bland': cột vào = chỉ số nhỏ nhất có hệ số âm.
    Hàng ra = tỉ số nhỏ nhất trên hệ số dương, hoà → biến cơ sở có chỉ số nhỏ nhất. Trả về (z, x, số lần xoay) hoặc ('khong_chan', None, số lần xoay)."""
    from fractions import Fraction as Fr
    m, n = len(A), len(c)
    T = [[Fr(v) for v in A[i]] + [Fr(1) if j == i else Fr(0) for j in range(m)] + [Fr(b[i])] for i in range(m)]
    T.append([Fr(-v) for v in c] + [Fr(0)] * m + [Fr(0)])
    basis = [n + i for i in range(m)]
    piv = 0
    while True:
        z = T[-1]
        neg = [j for j in range(n + m) if z[j] < 0]
        if not neg:
            break
        col = min(neg) if rule == "bland" else min(neg, key=lambda j: (z[j], j))
        cand = [(T[i][-1] / T[i][col], basis[i], i) for i in range(m) if T[i][col] > 0]
        if not cand:
            return "khong_chan", None, piv
        _, _, row = min(cand)
        p = T[row][col]
        T[row] = [v / p for v in T[row]]
        for i in range(m + 1):
            if i != row and T[i][col] != 0:
                f = T[i][col]
                T[i] = [vi - f * vr for vi, vr in zip(T[i], T[row])]
        basis[row] = col
        piv += 1
    x = [Fr(0)] * (n + m)
    for i, bv in enumerate(basis):
        x[bv] = T[i][-1]
    return T[-1][-1], x[:n], piv


def lp_random(n, m, seed=1):
    """LP tất định: hệ số 1..9, vế phải 50..99, mục tiêu 1..9 (A > 0, b > 0 nên có chặn và gốc hợp lệ)."""
    lst = lcg_list(m * n + m + n, seed, 1000)
    A = [[1 + lst[i * n + j] % 9 for j in range(n)] for i in range(m)]
    b = [50 + lst[m * n + i] % 50 for i in range(m)]
    c = [1 + lst[m * n + m + j] % 9 for j in range(n)]
    return c, A, b


def klee_minty(n):
    """Khối Klee–Minty: lớn nhất Σ 2^(n−j) x_j, ràng buộc 2·Σ_{j<i} 2^(i−j) x_j + x_i ≤ 5^i."""
    c = [2 ** (n - j) for j in range(1, n + 1)]
    A = [[2 ** (i - j + 1) if j < i else (1 if j == i else 0) for j in range(1, n + 1)] for i in range(1, n + 1)]
    b = [5 ** i for i in range(1, n + 1)]
    return c, A, b


# ───────────── L23: sắp xếp nhanh ─────────────
def qs_compares(a):
    """Số phép so sánh a[j] ≤ chốt của sắp xếp nhanh (chốt = phần tử cuối, phân hoạch như bài), cài bằng ngăn xếp tự quản để không tràn ngăn xếp.
    Trả về (số so sánh, độ sâu đệ quy lớn nhất)."""
    a = list(a)
    cmp_n, depth_max = 0, 0
    stack = [(0, len(a) - 1, 1)]
    while stack:
        lo, hi, d = stack.pop()
        if lo >= hi:
            continue
        depth_max = max(depth_max, d)
        p, i = a[hi], lo - 1
        for j in range(lo, hi):
            cmp_n += 1
            if a[j] <= p:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        stack.append((lo, i, d + 1))
        stack.append((i + 2, hi, d + 1))
    return cmp_n, depth_max


def log2_factorial_ceil(n):
    return math.ceil(math.lgamma(n + 1) / math.log(2))


# ───────────── L24: đường đi ngắn nhất ─────────────
def sp_graph(n, m, seed=1):
    """Đồ thị có hướng ngẫu nhiên tất định: m cạnh (u, v, w), w ∈ 1..20."""
    lst = lcg_list(3 * m, seed, 10 ** 6)
    return [(lst[3 * i] % n, lst[3 * i + 1] % n, 1 + lst[3 * i + 2] % 20) for i in range(m)]


def dijkstra_ops(n, edges, s=0):
    """Dijkstra với đống nhị phân (heapq, xoá lười): (d, số lần nới cạnh được xét, số lần đẩy vào đống)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF_ = float("inf")
    d = [INF_] * n
    d[s] = 0
    h, done, relax, pushes = [(0, s)], [False] * n, 0, 1
    while h:
        du, u = heapq.heappop(h)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            relax += 1
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(h, (d[v], v))
                pushes += 1
    return d, relax, pushes


def dijkstra_relax_count(n, edges, s=0):
    """Dijkstra đúng như bài L24 (nới u→v CHỈ khi v chưa chốt): (d, số lần nới được thử). fix4_CS112_B: bảng quy mô dùng số này;
    dijkstra_ops đếm cả cạnh tới đỉnh đã chốt (4 967 / 49 641 ở 1 000 / 10 000 đỉnh) nên lớn hơn khoảng hai lần."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    d = [float("inf")] * n
    d[s] = 0
    h, done, tried = [(0, s)], [False] * n, 0
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
    return d, tried


def bellman_ford_rounds(n, edges, s=0):
    """Bellman–Ford nới mọi cạnh theo thứ tự cho trước, dừng khi một vòng không đổi gì: (d, số vòng có đổi, số lần nới đã làm kể cả vòng kiểm cuối)."""
    INF_ = float("inf")
    d = [INF_] * n
    d[s] = 0
    rounds = relaxes = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            relaxes += 1
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                changed = True
        if not changed:
            break
        rounds += 1
    return d, rounds, relaxes


def chain_edges(n):
    """Đồ thị chuỗi 0 → 1 → … → n−1, trọng số 1, cạnh liệt kê NGƯỢC chiều đường đi (thứ tự xấu cho Bellman–Ford)."""
    return [(i, i + 1, 1) for i in range(n - 2, -1, -1)]


# ───────────── L25: cây khung nhỏ nhất, hợp–tìm ─────────────
class DSU:
    """Hợp–tìm có đếm số bước lên cha. mode: 'naive' (gắn gốc a vào gốc b, không nén), 'size' (gắn nhóm nhỏ vào nhóm lớn), 'both' (thêm nén đường)."""

    def __init__(self, n, mode="both"):
        self.p, self.sz, self.mode, self.steps = list(range(n)), [1] * n, mode, 0

    def find(self, x):
        r = x
        while self.p[r] != r:
            r = self.p[r]
            self.steps += 1
        if self.mode == "both":
            while self.p[x] != r:
                self.p[x], x = r, self.p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.mode != "naive" and self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        return True


def dsu_chain_steps(n, mode):
    """Tổng số bước lên cha khi hợp (i, i+1) lần lượt rồi tìm gốc của đỉnh 0 mỗi lần sau khi hợp."""
    ds = DSU(n, mode)
    for i in range(n - 1):
        ds.union(i + 1, i) if mode == "naive" else ds.union(i, i + 1)
        ds.find(0)
    return ds.steps


def kruskal_ops(n, edges):
    """(tổng trọng số, số so sánh của sắp xếp trộn, số bước lên cha của hợp–tìm đầy đủ) trên danh sách cạnh (u, v, w)."""
    keys = [w for _, _, w in edges]
    cmp_n = sort_compares(keys, desc=False)  # Kruskal sắp cạnh từ nhẹ đến nặng
    es = sorted(edges, key=lambda e: e[2])
    ds = DSU(n, "both")
    total = taken = 0
    for u, v, w in es:
        if ds.union(u, v):
            total += w
            taken += 1
            if taken == n - 1:
                break
    return total, cmp_n, ds.steps


def complete_graph(n, seed=1):
    lst = lcg_list(n * (n - 1) // 2, seed, 10 ** 6)
    out, k = [], 0
    for i in range(n):
        for j in range(i + 1, n):
            out.append((i, j, lst[k]))
            k += 1
    return out


# ───────────── L28: tổng ôn ─────────────
def f_steps(n):
    """Số bước 'làm 1 bước' của hàm ví dụ bài 28: n bước rồi gọi hai nửa (n = 2^k), đếm bằng vòng lặp thật."""
    c = 0
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        for _ in range(m):
            c += 1
        stack.append(m // 2)
        stack.append(m // 2)
    return c


def pair_steps_loop(n):
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
    return c
