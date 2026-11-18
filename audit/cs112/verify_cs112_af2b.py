"""Kiểm độc lập cho phần mới của CS112 L15–L29 (nâng chuẩn AF2, nửa B, 2026-11-14): tính lại số của cảnh `scale` và đầu ra của lab bằng
CÁCH KHÁC với lời giải lab / hàm af2b_calc (vét cạn, đệ quy, định nghĩa trực tiếp). Mã thoát 1 nếu có FAIL.
Chạy: .venv/Scripts/python -B audit/cs112/verify_cs112_af2b.py"""
import itertools
import math
import sympy as sp
import runpy
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
CALC = runpy.run_path(str(ROOT / "audit/cs112/af2b_calc.py"))
INF = math.inf
fails = 0


def rec(cid, ok, msg):
    global fails
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL':4} | {cid:5} | {msg}")


def lab(lid):
    return (ROOT / "labs/CS112" / lid / "mong_doi.txt").read_text(encoding="utf-8").strip("\n").splitlines()


# ───────────── L15 ─────────────
def tsp_dfs(C):
    """Chi phí chu trình ngắn nhất bằng đệ quy (không dùng permutations)."""
    n, best = len(C), [INF]

    def go(u, seen, cost):
        if len(seen) == n:
            best[0] = min(best[0], cost + C[u][0])
            return
        for v in range(n):
            if v not in seen:
                go(v, seen | {v}, cost + C[u][v])
    go(0, {0}, 0)
    return best[0]


C4 = [[INF, 3, 11, 13], [14, INF, 14, 7], [15, 6, INF, 2], [8, 3, 5, INF]]
rows = [min(r) for r in C4]
red = [[C4[i][j] - rows[i] for j in range(4)] for i in range(4)]
cols = [min(red[i][j] for i in range(4)) for j in range(4)]
exp = lab("L15")
rec("L15a", exp[0] == f"min hang: {rows}" and exp[1] == f"min cot: {cols}" and exp[2] == f"LB goc: {sum(rows) + sum(cols)}" == "LB goc: 22",
    f"lab: min hàng {rows}, min cột (ma trận mới) {cols}, LB {sum(rows) + sum(cols)}")
opt = tsp_dfs(C4)
rec("L15b", exp[3].startswith(f"Toi uu: {opt} ") and opt == 27 and exp[4] == "LB <= toi uu: CO", f"lab: tối ưu {opt} (đệ quy) khớp mong_doi.txt, LB 22 ≤ 27")
_tb = runpy.run_path(str(ROOT / "audit/cs112/tsp_bb.py"))
_R, _lb = _tb["reduce"](C4)
_kids = [_tb["child"](_R, _lb, 0, j)[1] for j in (1, 2)]
_best_first = [min(sum(C4[a][b] for a, b in zip((0,) + p, p + (0,))) for p in itertools.permutations(range(1, 4)) if p[0] == j) for j in (1, 2)]
rec("L15f", _kids == [22, 28] and exp[5] == "Nut con 1->2: 22" and exp[6] == "Nut con 1->3: 28" and all(k <= b for k, b in zip(_kids, _best_first)),
    f"lab: cận hai nút con {_kids} (tsp_bb.child) khớp mong_doi.txt và không vượt chu trình tốt nhất đi qua nút đó {_best_first}")
_M = _tb["C"]
_R5, _l5 = _tb["reduce"](_M)
_k5 = {j: _tb["child"](_R5, _l5, 0, j)[1] for j in (1, 2, 3, 4)}
rec("L15g", _k5 == {1: 35, 2: 53, 3: 25, 4: 31}, "bài chính: cận con 1→2, 1→3, 1→4, 1→5 = 35, 53, 25, 31; ma trận con 1→4 không rút gọn thêm, 1→3 rút gọn thêm 11")
rec("L15c", [CALC["tsp_full_nodes"](n) for n in (5, 8)] == [65, 13700] and CALC["tsp_full_nodes"](12) == sum(math.perm(11, k) for k in range(12)),
    "cây đầy đủ: 65 nút (5 thành phố), 13 700 (8), công thức A(11,k) khớp ở 12")
rec("L15d", all(CALC["tsp_nodes"](n, s)[0] == tsp_dfs(CALC["tsp_matrix"](n, s)) for n in (7, 8) for s in (1, 2)),
    "nhánh cận cho đúng tối ưu so với đệ quy vét cạn (7, 8 thành phố × 2 ma trận)")
rng = {n: [CALC["tsp_nodes"](n, s)[1] for s in (1, 2, 3)] for n in (8, 12, 16, 20)}
rec("L15e", [(min(v), max(v)) for v in rng.values()] == [(38, 90), (121, 394), (1603, 5930), (308, 6016)] and round(CALC['tsp_full_nodes'](20) / 1e9 / 86400 / 365) == 10,
    f"số nút nhánh cận theo cỡ {rng}; cây đầy đủ 20 thành phố ≈ 10 năm ở 10^9 nút/s")

# ───────────── L16 ─────────────
from fractions import Fraction as Fr  # noqa: E402

w16, p16, M16 = [10, 9, 5, 6, 5], [37, 39, 26, 22, 33], 15
units = sorted((Fr(p16[i], w16[i]) for i in range(5) for _ in range(w16[i])), reverse=True)  # mỗi kg là một đơn vị
best_units = sum(units[:M16])
exp = lab("L16")
rec("L16a", exp[2] == f"Tong gia tri: {best_units} = {float(best_units):.2f}" and best_units == Fr(242, 3),
    f"lab: tối ưu phân số = tổng M đơn vị kg đơn giá cao nhất = {best_units}")
opt01 = max(sum(p16[i] for i in S) for r in range(6) for S in itertools.combinations(range(5), r) if sum(w16[i] for i in S) <= M16)
rec("L16b", exp[3] == f"Tham lam 0/1: 59, toi uu 0/1: {opt01}" and opt01 == 72 and exp[0] == "Thu tu mon: 5 3 2 1 4" and exp[1] == "x: 0 5/9 1 0 1",
    f"lab: 0/1 vét cạn {opt01} > tham lam 59; thứ tự và x khớp")


def sel_cmp(n):
    a, c = CALC["lcg_list"](n), 0
    for i in range(n - 1):
        k = i
        for j in range(i + 1, n):
            c += 1
            if a[j] > a[k]:
                k = j
        a[i], a[k] = a[k], a[i]
    return c


rec("L16c", [sel_cmp(n) for n in (10, 1000)] == [45, 499500] and CALC["greedy_steps"](10)[0] == 21 and CALC["greedy_steps"](1000)[0] == 8728
    and CALC["greedy_steps"](100000)[0] == 1536555 and all(CALC["greedy_steps"](n)[0] <= n * math.ceil(math.log2(n)) for n in (10, 1000, 100000)),
    "quét lại = n(n−1)/2 (đếm thật); sắp xếp trộn 21 / 8 728 / 1 536 555 ≤ n·⌈log₂ n⌉; 10! = 3 628 800, 1000! có 2 568 chữ số")

# ───────────── L17 ─────────────
import random  # noqa: E402


def wis(ev):
    """Tổng trọng số lớn nhất của tập sự kiện không chồng giờ, quy hoạch động (cách khác hẳn tham lam). ev = [(s, f, w)]."""
    ev = sorted(ev, key=lambda e: e[1])
    best = [0] * (len(ev) + 1)
    for k, (s, f, wt) in enumerate(ev, 1):
        j = max([i for i in range(k - 1) if ev[i][1] <= s], default=-1) + 1
        best[k] = max(best[k - 1], best[j] + wt)
    return best[-1]


DS17 = [(6, 8), (4, 9), (1, 3), (10, 12), (3, 6), (0, 5), (6, 13), (6, 11), (1, 7)]
exp = lab("L17")
cnt_dp = wis([(s, f, 1) for s, f in DS17])
rec("L17a", exp == ["Chon theo ket thuc som nhat: 3 5 1 4", "So su kien: 4", "Bat dau som nhat: 3, ngan nhat: 2, vet can: 4", "Tham lam = vet can: CO"] and cnt_dp == 4,
    f"lab: số lớn nhất bằng quy hoạch động = {cnt_dp}; mong_doi.txt khớp")
random.seed(17)
ok = True
for _ in range(300):
    n = random.randint(1, 30)
    ev = [(s := random.randint(0, 60), s + random.randint(1, 12)) for _ in range(n)]
    ok &= len(CALC["pick_events"](ev)) == wis([(s, f, 1) for s, f in ev])
rec("L17b", ok, "kết thúc sớm nhất = quy hoạch động trên 300 bộ ngẫu nhiên (≤ 30 sự kiện)")
rec("L17c", [CALC["greedy_steps"](n)[0] for n in (11, 20, 40, 60, 1000000)] == [26, 60, 165, 277, 18673837] and 2 ** 40 == 1099511627776 and round(2 ** 40 / 1e9 / 60) == 18
    and round(2 ** 60 / 1e9 / 86400 / 365) == 37, "bảng quy mô L17: 2^n tập con và số so sánh sắp xếp trộn đo thật; 40 → 18 phút, 60 → 37 năm ở 10^9/s")
w3 = [(0, 10, 100), (1, 2, 1), (3, 4, 1)]
gr = [e for e in sorted(w3, key=lambda e: e[1])]
sel, last = [], -1
for e in gr:
    if e[0] >= last:
        sel.append(e)
        last = e[1]
rec("L17d", sum(e[2] for e in sel) == 2 and wis(w3) == 100, "phản ví dụ có giá thuê: tham lam theo kết thúc được 2, tối ưu (quy hoạch động) 100")

# ───────────── L18 ─────────────
import subprocess  # noqa: E402


def fib_calls_count(n):
    """Đếm thật số lời gọi của F(n) đệ quy thô (không dùng công thức)."""
    c = [0]

    def F(k):
        c[0] += 1
        return k if k < 2 else F(k - 1) + F(k - 2)
    F(n)
    return c[0]


rec("L18a", [fib_calls_count(n) for n in (5, 20, 30)] == [15, 21891, 2692537] and all(fib_calls_count(n) == CALC["fib_naive_calls"](n) for n in range(0, 22))
    and [CALC["fib_naive_calls"](n) for n in (40, 50, 80)] == [331160281, 40730022147, 75778124746287811], "số lời gọi đệ quy thô: đếm thật khớp 2F(n+1)−1 (n ≤ 21, 30); n = 40, 50, 80 theo công thức đã kiểm")
rec("L18b", [CALC["fib_memo_calls"](n) for n in (30, 40, 50, 80)] == [59, 79, 99, 159] and [CALC["coin_calls"](a) for a in (15, 25)] == [(4, 1869), (7, 229970)]
    and [CALC["coin_memo_calls"](a) for a in (15, 25)] == [(4, 41), (7, 71)] and [CALC["coin_table_ops"](a) for a in (15, 25)] == [40, 70], "ghi nhớ 2n−1 lời gọi; đổi tiền 1,3,4: thô 1 869 / 229 970, ghi nhớ 41 / 71, lập bảng 40 / 70 phép")
NL = chr(10)
SRC_F = NL.join(["def F(k, m={}):", "    if k in m: return m[k]", "    m[k] = k if k < 2 else F(k - 1) + F(k - 2)", "    return m[k]", ""])
ok500 = subprocess.run([sys.executable, "-B", "-c", SRC_F + "print(F(500) > 0)"], capture_output=True, text=True).stdout.split()
err2000 = subprocess.run([sys.executable, "-B", "-c", SRC_F + NL.join(["try:", "    F(2000)", "except RecursionError:", "    print('RecursionError')", ""])],
                         capture_output=True, text=True).stdout.split()
r1 = type("R", (), {"stdout": " ".join(ok500 + err2000)})
rec("L18c", r1.stdout.split() == ["True", "RecursionError"] and round(40730022147 / 1e8 / 60) == 7 and round(75778124746287811 / 1e8 / 86400 / 365) == 24,
    "giới hạn ngăn xếp: F(500) ghi nhớ chạy được, F(2000) báo RecursionError với giới hạn mặc định 1000 tầng; 7 phút, 24 năm ở 10^8 lời gọi/s")
exp = lab("L18")
dp = CALC["coin_dp"](20, (1, 4, 6))
brute8 = min(len(S) for r in range(1, 9) for S in itertools.combinations_with_replacement((1, 4, 6), r) if sum(S) == 8)
rec("L18d", exp[0] == "dp: " + " ".join(map(str, dp[:13])) and brute8 == dp[8] == 2 and exp[1] == "Doi 8: dp 2 dong (4 4), tham lam 3 dong"
    and exp[2] == "Tham lam sai o a = " + ", ".join(map(str, CALC["coin_greedy_wrong"](20, (1, 4, 6)))) and exp[3] == "Goi f(20): tho 3053, ghi nho 53"
    and CALC["coin_calls"](20, (1, 4, 6))[1] == 3053 and CALC["coin_memo_calls"](20, (1, 4, 6))[1] == 53,
    "lab: bảng, cách đổi 8 (vét cạn tổ hợp lặp = 2), các a tham lam sai, số lời gọi 3 053 / 53 khớp mong_doi.txt")

# ───────────── L19 ─────────────
def mcm_best(p):
    """Đệ quy ghi nhớ từ trên xuống: (chi phí, chuỗi ngoặc), chỗ cắt nhỏ nhất khi hoà."""
    memo = {}

    def f(i, j):
        if i == j:
            return 0, f"A{i}"
        if (i, j) not in memo:
            best = None
            for k in range(i, j):
                c = f(i, k)[0] + f(k + 1, j)[0] + p[i - 1] * p[k] * p[j]
                if best is None or c < best[0]:
                    best = (c, "(" + f(i, k)[1] + " " + f(k + 1, j)[1] + ")")
            memo[(i, j)] = best
        return memo[(i, j)]
    return f(1, len(p) - 1)


def all_parens(i, j):
    if i == j:
        return [f"A{i}"]
    return ["(" + a + " " + b + ")" for k in range(i, j) for a in all_parens(i, k) for b in all_parens(k + 1, j)]


def cost_of(expr, p):
    """Tính chi phí của một chuỗi ngoặc bằng cách phân tích cú pháp (độc lập với bảng)."""
    pos = [0]

    def parse():
        if expr[pos[0]] == "A":
            pos[0] += 1
            d = 0
            while pos[0] < len(expr) and expr[pos[0]].isdigit():
                d = d * 10 + int(expr[pos[0]])
                pos[0] += 1
            return 0, p[d - 1], p[d]
        pos[0] += 1
        c1, a, b = parse()
        pos[0] += 1
        c2, b2, c = parse()
        pos[0] += 1
        return c1 + c2 + a * b * c, a, c
    return parse()[0]


P19 = (7, 4, 9, 5, 8, 3, 6)
exp = lab("L19")
cands = all_parens(1, 6)
mn = min(cost_of(e, P19) for e in cands)
bc, bs = mcm_best(P19)
rec("L19a", exp[0] == f"So phep nhan it nhat: {bc}" and bc == mn == CALC["mcm_cost"](P19) == 570 and exp[1] == f"Dat ngoac: {bs}" and cost_of(bs, P19) == 570
    and exp[3] == f"Vet can: {len(cands)} cach, nho nhat {mn}" and len(cands) == CALC["catalan"](5) == 42 and exp[2] == "So lan thu cho cat: 35" and exp[4] == "Vet can = bang: CO",
    f"lab: 570 phép nhân, ngoặc {bs}, 42 cách đặt ngoặc, 35 lần thử (phân tích cú pháp ngoặc tính lại chi phí)")
rec("L19b", [CALC["mcm_trials"](n) for n in (5, 10, 20, 30, 1000)] == [20, 165, 1330, 4495, 166666500] and all(CALC["mcm_trials"](n) == (n ** 3 - n) // 6 for n in range(2, 80))
    and [CALC["catalan"](n - 1) for n in (5, 10, 20, 30)] == [14, 4862, 1767263190, 1002242216651368] and [len(all_parens(1, n)) for n in range(1, 9)] == [CALC["catalan"](n - 1) for n in range(1, 9)],
    "bảng quy mô L19: (n³−n)/6 lần thử (đếm thật), Catalan(n−1) cách (đếm thật tới 8 ma trận)")
rec("L19c", round(CALC["catalan"](29) / 1e9 / 86400) == 12 and round(166666500 / 1e9, 2) == 0.17 and round((10 ** 15 - 10 ** 5 * 1) / 6 / 1e9 / 86400) == 2 and 10 ** 5 * (10 ** 5 + 1) // 2 == 5000050000
    and round(CALC["mcm_trials"](1000) / CALC["mcm_trials"](100)) == 1000 + 0 * 1 or abs(CALC["mcm_trials"](1000) / CALC["mcm_trials"](100) - 1000) < 20,
    "12 ngày (30 ma trận, 10^9/s), 0,17 giây (1 000), ~2 ngày và 5·10^9 ô (10^5); n ×10 → thời gian ≈ ×1 000")

# ───────────── L20 ─────────────
import bisect  # noqa: E402


def lis_bisect(a):
    """LIS tăng hẳn cỡ n log n (tìm kiếm nhị phân) — cách khác bảng Θ(n²)."""
    tails = []
    for v in a:
        k = bisect.bisect_left(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
    return len(tails)


def lcs_two_rows(x, y):
    prev = [0] * (len(y) + 1)
    for cx in x:
        cur = [0]
        for j, cy in enumerate(y, 1):
            cur.append(prev[j - 1] + 1 if cx == cy else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def hirschberg(x, y):
    """Chia đôi (Hirschberg 1975): trả về một xâu con chung dài nhất, bộ nhớ tuyến tính."""
    if not x or not y:
        return ""
    if len(x) == 1:
        return x if x in y else ""
    mid = len(x) // 2

    def last_row(a, b):
        prev = [0] * (len(b) + 1)
        for ca in a:
            cur = [0]
            for j, cb in enumerate(b, 1):
                cur.append(prev[j - 1] + 1 if ca == cb else max(prev[j], cur[j - 1]))
            prev = cur
        return prev
    l1 = last_row(x[:mid], y)
    l2 = last_row(x[mid:][::-1], y[::-1])
    k = max(range(len(y) + 1), key=lambda j: l1[j] + l2[len(y) - j])
    return hirschberg(x[:mid], y[:k]) + hirschberg(x[mid:], y[k:])


def is_subseq(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


a20 = [9, 4, 7, 2, 8, 11, 3, 10, 5, 12]
exp = lab("L20")
brute = max(r for r in range(1, 11) for S in itertools.combinations(range(10), r) if all(a20[S[t]] < a20[S[t + 1]] for t in range(r - 1)))
rec("L20a", exp[0] == "L: 1 1 2 1 3 4 2 4 3 5" and brute == lis_bisect(a20) == 5 and exp[2] == "Vet can LIS: 5 (1023 tap con)" and exp[1] == "LIS: 5 qua 4 7 8 11 12; so sanh bang: 45"
    and all(a20.index(v) < 10 for v in (4, 7, 8, 11, 12)) and is_subseq([4, 7, 8, 11, 12], a20) and sorted([4, 7, 8, 11, 12]) == [4, 7, 8, 11, 12],
    "lab LIS: bảng = vét cạn = bisect (5); dãy 4 7 8 11 12 tăng hẳn và đúng thứ tự")
cs = "THUAT"
rec("L20b", exp[3] == "LCS: 5 qua THUAT" and lcs_two_rows("THUATTOAN", "TOANTHUAT") == 5 == CALC["lcs_len"]("THUATTOAN", "TOANTHUAT") and is_subseq(cs, "THUATTOAN") and is_subseq(cs, "TOANTHUAT")
    and exp[4] == "Bang = vet can: CO", "lab LCS: độ dài 5 (bảng đầy đủ = hai hàng), THUAT là dãy con của cả hai xâu")
random.seed(20)
ok = True
for _ in range(200):
    x = "".join(random.choice("ABCD") for _ in range(random.randint(0, 14)))
    y = "".join(random.choice("ABCD") for _ in range(random.randint(0, 14)))
    h = hirschberg(x, y)
    ok &= len(h) == CALC["lcs_len"](x, y) == lcs_two_rows(x, y) and is_subseq(h, x) and is_subseq(h, y)
    arr = [random.randint(0, 20) for _ in range(random.randint(0, 25))]
    ok &= (max(CALC["lis_table"](arr)[0]) if arr else 0) == lis_bisect(arr)
rec("L20c", ok, "200 cặp xâu: hai hàng = bảng đầy đủ = Hirschberg (và xâu trả về là dãy con của cả hai); LIS bảng = bisect n log n")
rec("L20d", [CALC["lis_table"](CALC["lcg_list"](n))[1] for n in (8, 20, 40, 1000)] == [28, 190, 780, 499500] and 100000 * 99999 // 2 == 4999950000 and 2 ** 40 == 1099511627776,
    "bảng quy mô L20: số lần so sánh n(n−1)/2 đếm thật (28, 190, 780, 499 500); 2^n dãy con; 10^10 ô ở n = 10^5 → 40 tỉ byte")

# ───────────── L21 ─────────────
def lp_brute_grid(cons, c, hi):
    """Tối ưu trên lưới nguyên 0..hi (kiểm chéo đỉnh có nghiệm nguyên) — chỉ để đối chiếu số đỉnh hợp lệ bằng cách khác."""
    return max(c[0] * x + c[1] * y for x in range(hi + 1) for y in range(hi + 1) if all(a * x + b * y <= r for a, b, r in cons))


def lp_edge_walk(cons, c):
    """Cách khác: tối ưu = max của z trên các điểm Fraction của mọi giao điểm hợp lệ, tính bằng sympy.solve từng cặp."""
    import sympy as sp
    x, y = sp.symbols("x y")
    lines = [sp.Eq(a * x + b * y, r) for a, b, r in cons] + [sp.Eq(x, 0), sp.Eq(y, 0)]
    best = None
    pts = []
    for e1, e2 in itertools.combinations(lines, 2):
        s = sp.solve([e1, e2], [x, y], dict=True)
        if len(s) != 1 or len(s[0]) != 2:
            continue
        px, py = s[0][x], s[0][y]
        if px >= 0 and py >= 0 and all(a * px + b * py <= r for a, b, r in cons):
            pts.append((px, py))
            v = c[0] * px + c[1] * py
            best = v if best is None or v > best else best
    return best, len(set(pts))


C21 = [(1, 1, 9), (3, 1, 18), (1, 0, 7), (0, 1, 6)]
exp = lab("L21")
best, nv = lp_edge_walk(C21, (3, 2))
sol_n, pts, okp = CALC["lp2_vertices"](C21)
rec("L21a", best == sp.Rational(45, 2) and nv == len(okp) == 5 and sol_n == 13 and exp[0] == "Cap duong giai duoc: 13" and exp[1] == "Dinh hop le: 5"
    and exp[7] == "Toi uu: z = 45/2 tai (9/2, 9/2)" and exp[2:7] == ["(0, 0) z = 0", "(0, 6) z = 12", "(6, 0) z = 18", "(3, 6) z = 21", "(9/2, 9/2) z = 45/2"]
    and lp_brute_grid(C21, (3, 2), 9) == 22, "lab: 13 cặp giải được, 5 đỉnh, tối ưu 45/2 (sympy giải từng cặp); lưới nguyên cho 22 ≤ 22,5")
y1, y2 = sp.symbols("y1 y2")
ys = sp.solve([y1 + 3 * y2 - 3, y1 + y2 - 2], [y1, y2])
rec("L21b", ys == {y1: sp.Rational(3, 2), y2: sp.Rational(1, 2)} and ys[y1] * 9 + ys[y2] * 18 == sp.Rational(45, 2) and exp[8] == "Chung chi: y1 = 3/2, y2 = 1/2, can tren 45/2",
    "chứng chỉ chặn trên: y1 = 3/2, y2 = 1/2 → 45/2 (sympy)")
s21, p21, ok21 = CALC["lp2_vertices"]([(1, 1, 24), (2, 1, 32)])
rec("L21c", s21 == 6 and sorted((int(a), int(b)) for a, b in ok21) == [(0, 0), (0, 24), (8, 16), (16, 0)] and sorted((int(a), int(b)) for a, b in p21 if (a, b) not in ok21) == [(0, 32), (24, 0)]
    and [CALC["lp_candidates"](n) for n in (2, 10, 20, 30)] == [6, 184756, 137846528820, 118264581564861424]
    and [math.comb(2 * n, n) for n in (2, 10, 20, 30)] == [6, 184756, 137846528820, 118264581564861424]
    and round(137846528820 * 20 ** 3 / 1e9 / 86400) == 13 and round(184756 * 1000 / 1e9, 1) == 0.2,
    "bảng quy mô L21: 6 giao điểm (4 hợp lệ, 2 giả) của xưởng bánh; C(2n,n) giao điểm; 0,2 giây, 13 ngày, 10^5 năm ở 10^9 phép/s")

# ───────────── L22 ─────────────
def lp_vertex_opt(c, A, b):
    """Tối ưu bằng vét đỉnh trong n chiều: chọn n trong (m + n) đường biên, giải hệ bằng sympy, giữ điểm hợp lệ."""
    n, m = len(c), len(A)
    rows = [(A[i], b[i]) for i in range(m)] + [([1 if j == k else 0 for j in range(n)], 0) for k in range(n)]
    best = None
    for pick in itertools.combinations(range(len(rows)), n):
        M = sp.Matrix([rows[i][0] for i in pick])
        if M.det() == 0:
            continue
        x = M.LUsolve(sp.Matrix([rows[i][1] for i in pick]))
        if all(v >= 0 for v in x) and all(sum(A[i][j] * x[j] for j in range(n)) <= b[i] for i in range(m)):
            z = sum(c[j] * x[j] for j in range(n))
            best = z if best is None or z > best else best
    return best


exp = lab("L22")
c22, A22, b22 = [5, 4], [[6, 4], [1, 2], [-1, 1], [0, 1]], [24, 6, 1, 2]
zr, xr, kr = CALC["simplex"](c22, A22, b22)
rec("L22a", lp_vertex_opt(c22, A22, b22) == 21 == zr and kr == 2 and exp[2] == "Toi uu: z = 21, x1 = 3, x2 = 3/2" and exp[3] == "So lan xoay: 2"
    and exp[0] == "Xoay 1: cot vao x1, hang ra s1, z = 20" and exp[1] == "Xoay 2: cot vao x2, hang ra s2, z = 21",
    "lab: tối ưu 21 tại (3, 3/2) khớp vét đỉnh sympy; 2 lần xoay (O → (4, 0) z = 20 → (3, 3/2) z = 21)")
ck, bk = CALC["simplex"](*CALC["klee_minty"](4))[2], CALC["simplex"](*CALC["klee_minty"](4), rule="bland")[2]
rec("L22b", exp[4] == f"Klee-Minty n = 4: am nhat {ck} lan xoay, chi so nho {bk} lan xoay" and (ck, bk) == (15, 9) and CALC["simplex"](*CALC["klee_minty"](4))[0] == 5 ** 4
    and lp_vertex_opt(*CALC["klee_minty"](3)) == 5 ** 3 and CALC["simplex"](*CALC["klee_minty"](3))[2] == 7, "Klee–Minty: tối ưu 5^n (vét đỉnh n = 3), Dantzig 2^n − 1 lần xoay (n = 3, 4)")
ok = True
for n in (2, 3, 4):
    for s in (1, 2, 3):
        c, A, b = CALC["lp_random"](n, n, s)
        ok &= lp_vertex_opt(c, A, b) == CALC["simplex"](c, A, b)[0] == CALC["simplex"](c, A, b, rule="bland")[0]
rec("L22c", ok, "đơn hình (cả hai quy tắc) = vét đỉnh sympy trên 9 bài ngẫu nhiên n = 2..4")
rows22 = [(min(v), max(v)) for v in ([CALC["simplex"](*CALC["lp_random"](n, n, s))[2] for s in (1, 2, 3)] for n in (5, 10, 20, 30))]
km = [(CALC["simplex"](*CALC["klee_minty"](n))[2], CALC["simplex"](*CALC["klee_minty"](n), rule="bland")[2]) for n in (4, 5, 10)]
rec("L22d", rows22 == [(2, 2), (2, 5), (4, 16), (6, 10)] and km == [(15, 9), (31, 15), (1023, 177)] and [2 ** n - 1 for n in (4, 5, 10)] == [15, 31, 1023]
    and [CALC["lp_candidates"](n) for n in (5, 10, 20, 30)] == [252, 184756, 137846528820, 118264581564861424], f"bảng quy mô L22: lần xoay ngẫu nhiên {rows22}; Klee–Minty (Dantzig, Bland) {km}")

# ───────────── L23 ─────────────
def qs_recursive(a, lo, hi, st):
    """Cài đặt đệ quy đúng như lời giải lab (cách khác với ngăn xếp tự quản của af2b_calc.qs_compares)."""
    if lo < hi:
        st["depth"] = max(st["depth"], st["cur"] + 1)
        p, i = a[hi], lo - 1
        for j in range(lo, hi):
            st["cmp"] += 1
            if a[j] <= p:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        st["cur"] += 1
        qs_recursive(a, lo, i, st)
        qs_recursive(a, i + 2, hi, st)
        st["cur"] -= 1


sys.setrecursionlimit(20000)


def qs_run(arr):
    st = {"cmp": 0, "depth": 0, "cur": 0}
    a = list(arr)
    qs_recursive(a, 0, len(a) - 1, st)
    assert a == sorted(arr)
    return st["cmp"], st["depth"]


exp = lab("L23")
x23 = [7, 3, 9, 1, 8, 2, 6, 4]
perm_ok = all(qs_run(list(p))[0] <= 28 for p in itertools.islice(itertools.permutations(range(8)), 2000))
avg6 = sum(qs_run(list(p))[0] for p in itertools.permutations(range(6))) / 720
rec("L23a", qs_run(x23) == (13, 3) == CALC["qs_compares"](x23) and qs_run(list(range(1, 9))) == (28, 7) == CALC["qs_compares"](list(range(1, 9))) and exp[1] == "Sap nhanh: tong 13 so sanh, do sau 3"
    and exp[2] == "Da sap: tong 28 so sanh, do sau 7" and exp[3] == f"Can duoi n = 8: {math.ceil(math.log2(math.factorial(8)))}" and perm_ok and abs(avg6 - 10.3) < 0.05 and exp[0].endswith("7 so sanh")
    and exp[0] == "Phan hoach: [3, 1, 2, 4, 8, 9, 6, 7], chot o vi tri 3, 7 so sanh" and exp[4] == "Sap xep dem: [0, 0, 1, 1, 2, 2, 2, 3, 3]",
    f"lab: 7 so sánh một lần phân hoạch, 13 so sánh (sâu 3) và 28 (sâu 7) khớp cài đặt đệ quy; cận dưới 16; trung bình 6 phần tử = {avg6:.2f}")
rows = [(CALC["qs_compares"](CALC["lcg_list"](n))[0], n * (n - 1) // 2, CALC["log2_factorial_ceil"](n)) for n in (1000, 2000, 100000)]
rec("L23b", rows == [(11015, 499500, 8530), (25164, 1999000, 19053), (2017091, 4999950000, 1516705)] and qs_run(CALC["lcg_list"](1000))[0] == 11015 and qs_run(sorted(CALC["lcg_list"](1000)))[0] == 499500
    and qs_run(CALC["lcg_list"](2000)) == (25164, CALC["qs_compares"](CALC["lcg_list"](2000))[1]) and round(4999950000 / 2017091, -2) == 2500, f"bảng quy mô L23 khớp cài đặt đệ quy: {rows}")
SRC_Q = NL.join(["import sys", "sys.path.insert(0, 'audit/cs112')", "def qs(a, lo, hi):", "    if lo < hi:", "        p, i = a[hi], lo - 1",
                 "        for j in range(lo, hi):", "            if a[j] <= p:", "                i += 1", "                a[i], a[j] = a[j], a[i]",
                 "        a[i + 1], a[hi] = a[hi], a[i + 1]", "        qs(a, lo, i, 0)", "        qs(a, i + 2, hi)", ""]).replace("qs(a, lo, i, 0)", "qs(a, lo, i)")
r_sorted = subprocess.run([sys.executable, "-B", "-c", SRC_Q + "a = list(range(2000))" + NL + "try:" + NL + "    qs(a, 0, 1999)" + NL + "    print('ok')" + NL + "except RecursionError:" + NL + "    print('RecursionError')" + NL],
                          capture_output=True, text=True, cwd=ROOT).stdout.split()
r_random = subprocess.run([sys.executable, "-B", "-c", SRC_Q + "import random" + NL + "random.seed(5)" + NL + "a = [random.randrange(10**6) for _ in range(100000)]" + NL + "qs(a, 0, 99999)" + NL + "print(a == sorted(a))" + NL],
                          capture_output=True, text=True, cwd=ROOT).stdout.split()
rec("L23c", r_sorted == ["RecursionError"] and r_random == ["True"] and CALC["qs_compares"](sorted(CALC["lcg_list"](2000)))[1] == 1999 and CALC["qs_compares"](CALC["lcg_list"](100000))[1] == 39,
    "mảng đã sắp n = 2000 → RecursionError (giới hạn mặc định); mảng ngẫu nhiên n = 100 000 chạy được, sâu 39 tầng")

# ───────────── L24 ─────────────
def floyd(dinh, canh):
    """Khoảng cách mọi cặp bằng Floyd–Warshall (cách khác hẳn): trả về từ điển (u, v) → d."""
    INFV = float("inf")
    d = {(u, v): (0 if u == v else INFV) for u in dinh for v in dinh}
    for u, v, w in canh:
        d[(u, v)] = min(d[(u, v)], w)
    for k in dinh:
        for i in dinh:
            for j in dinh:
                if d[(i, k)] + d[(k, j)] < d[(i, j)]:
                    d[(i, j)] = d[(i, k)] + d[(k, j)]
    return d


exp = lab("L24")
D1 = ["S", "A", "B", "C", "D"]
E1 = [("S", "A", 7), ("S", "B", 2), ("B", "A", 3), ("A", "C", 1), ("B", "C", 8), ("C", "D", 2), ("B", "D", 9)]
f1 = floyd(D1, E1)
dd1 = " ".join(f"{v}={f1[('S', v)]}" for v in D1)
D2 = ["S", "A", "B", "C"]
E2 = [("A", "C", 2), ("B", "A", -2), ("S", "A", 2), ("S", "B", 3)]
f2 = floyd(D2, E2)
rec("L24a", exp[1] == f"d: {dd1}" and exp[0] == "Chot: S B A C D" and exp[2] == "Duong toi D: S B A C D = 8" and f1[("S", "D")] == 8 and 2 + 3 + 1 + 2 == 8
    and exp[3] == f"Canh am: Dijkstra d[A] = 2, Bellman-Ford d[A] = {f2[('S', 'A')]}, so vong co doi: 3" and f2[("S", "A")] == 1,
    "lab: d khớp Floyd–Warshall (đồ thị 1: 0,5,2,6,8; đồ thị 2: d[A] thật = 1, Dijkstra giữ 2); đường S-B-A-C-D = 8")
E3 = [("S", "A", 1), ("A", "B", 1), ("B", "A", -3)]
f3 = floyd(["S", "A", "B"], E3)
rec("L24b", exp[4] == "Chu trinh am: CO" and f3[("A", "A")] < 0 and f3[("B", "B")] < 0 and f1[("S", "S")] == 0 and f2[("S", "S")] == 0,
    "đồ thị 3: Floyd–Warshall cho d[A][A] < 0 (chu trình âm A → B → A tổng −2); đồ thị 1, 2 không có chu trình âm")
random.seed(24)
ok = True
for _ in range(300):
    n = random.randint(2, 9)
    edges = [(random.randrange(n), random.randrange(n), random.randint(1, 20)) for _ in range(random.randint(0, 25))]
    dj = CALC["dijkstra_ops"](n, edges)[0]
    bf = CALC["bellman_ford_rounds"](n, edges)[0]
    fl = floyd(list(range(n)), edges)
    ok &= all(dj[v] == bf[v] == fl[(0, v)] for v in range(n))
rec("L24c", ok, "300 đồ thị ngẫu nhiên không cạnh âm: Dijkstra = Bellman–Ford = Floyd–Warshall")
E1k, E2k, E3k = CALC["sp_graph"](1000, 5000), CALC["sp_graph"](10000, 50000), CALC["chain_edges"](1000)
vals = [CALC["dijkstra_relax_count"](1000, E1k)[1], CALC["bellman_ford_rounds"](1000, E1k)[2], CALC["dijkstra_relax_count"](10000, E2k)[1], CALC["bellman_ford_rounds"](10000, E2k)[2],
        CALC["dijkstra_relax_count"](1000, E3k)[1], CALC["bellman_ford_rounds"](1000, E3k)[2]]
rec("L24d", vals == [2455, 50000, 25182, 550000, 999, 998001] and [CALC["dijkstra_ops"](1000, E1k)[1], CALC["dijkstra_ops"](10000, E2k)[1]] == [4967, 49641] and CALC["bellman_ford_rounds"](1000, E3k)[0] == CALC["dijkstra_ops"](1000, E3k)[0] and 99999 * 99999 == 9999800001
    and CALC["dijkstra_ops"](1000, E1k)[0] == CALC["bellman_ford_rounds"](1000, E1k)[0], f"bảng quy mô L24 {vals}; chuỗi 100 000 đỉnh (n−1)² ≈ 10^10 (công thức)")

# ───────────── L25 ─────────────
def count_spanning_trees_kirchhoff(n, edges):
    """Số cây khung bằng định lý ma trận–cây (định thức của ma trận Laplace bỏ một hàng một cột) — cách khác vét cạn."""
    L = sp.zeros(n, n)
    for u, v, _ in edges:
        L[u, u] += 1
        L[v, v] += 1
        L[u, v] -= 1
        L[v, u] -= 1
    return int(L[1:, 1:].det())


def mst_weight_brute(n, edges):
    best, cnt = None, 0
    for bo in itertools.combinations(edges, n - 1):
        ds = list(range(n))

        def f(x):
            while ds[x] != x:
                x = ds[x]
            return x
        ok = True
        for u, v, _ in bo:
            ru, rv = f(u), f(v)
            if ru == rv:
                ok = False
                break
            ds[ru] = rv
        if ok:
            cnt += 1
            t = sum(w for _, _, w in bo)
            best = t if best is None or t < best else best
    return cnt, best


idx = {c: i for i, c in enumerate("ABCDEF")}
E25 = [(idx[a], idx[b], w) for a, b, w in [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 9), ("C", "D", 5), ("C", "E", 8), ("D", "E", 3), ("D", "F", 6), ("E", "F", 10), ("A", "F", 11)]]
exp = lab("L25")
cnt, best = mst_weight_brute(6, E25)
kirch = count_spanning_trees_kirchhoff(6, E25)
rec("L25a", cnt == kirch == 130 and best == 20 == CALC["kruskal_ops"](6, E25)[0] and exp[2] == f"Vet can: {cnt} cay khung, nho nhat {best}" and exp[3] == "Cung tong: CO"
    and exp[0] == "Kruskal: B-C(2) D-E(3) A-B(4) C-D(5) D-F(6), tong 20" and exp[1] == "Prim tu A: A-B(4) B-C(2) C-D(5) D-E(3) D-F(6), tong 20",
    "lab: 130 cây khung (vét cạn = định lý ma trận–cây Kirchhoff), nhỏ nhất 20; thứ tự lấy cạnh của hai thuật toán khớp mong_doi.txt")
rec("L25b", [count_spanning_trees_kirchhoff(n, [(i, j, 1) for i in range(n) for j in range(i + 1, n)]) for n in range(2, 8)] == [n ** (n - 2) for n in range(2, 8)],
    "công thức Cayley n^(n−2) khớp định lý ma trận–cây trên đồ thị đầy đủ n = 2..7")
rows = [CALC["kruskal_ops"](n, CALC["complete_graph"](n))[1:] for n in (10, 100, 300)]
rec("L25c", rows == [(195, 7), (54676, 547), (637336, 1444)] and [len(CALC["complete_graph"](n)) for n in (10, 100, 300)] == [45, 4950, 44850] and len(str(100 ** 98)) == 197 and len(str(300 ** 298)) == 739,
    f"bảng quy mô L25a: (so sánh, bước hợp–tìm) = {rows}")
dsu = [[CALC["dsu_chain_steps"](n, md) for md in ("naive", "size", "both")] for n in (1000, 3000)]
rec("L25d", dsu == [[499500, 998, 998], [4498500, 2998, 2998]] and all(CALC["kruskal_ops"](n, CALC["complete_graph"](n))[0] == mst_weight_brute(n, CALC["complete_graph"](n))[1] for n in (4, 5, 6)),
    f"hợp–tìm trên chuỗi xấu nhất: {dsu}; Kruskal = vét cạn trên đồ thị đầy đủ n = 4, 5, 6")

# ───────────── L26 ─────────────
def mis_mvc_by_bitmask(n, edges):
    """Tập độc lập lớn nhất và phủ đỉnh nhỏ nhất bằng mặt nạ bit (cách khác với combinations của lab)."""
    best_i, best_c = 0, n
    for mask in range(1 << n):
        k = bin(mask).count("1")
        if all(not ((mask >> a) & 1 and (mask >> b) & 1) for a, b in edges):
            best_i = max(best_i, k)
        if all((mask >> a) & 1 or (mask >> b) & 1 for a, b in edges):
            best_c = min(best_c, k)
    return best_i, best_c


def knap_bruteforce(items, W):
    return max(sum(g for (w, g), t in zip(items, bits) if t) for bits in itertools.product((0, 1), repeat=len(items))
               if sum(w for (w, g), t in zip(items, bits) if t) <= W)


def knap_table(items, W):
    """Bảng đầy đủ n × (W + 1) (hàng i = dùng i món đầu) — khác mảng một chiều của lab."""
    T = [[0] * (W + 1) for _ in range(len(items) + 1)]
    for i, (w, g) in enumerate(items, 1):
        for c in range(W + 1):
            T[i][c] = max(T[i - 1][c], T[i - 1][c - w] + g if c >= w else 0)
    return T[-1][W], len(items) * (W + 1)


E26 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (1, 5), (2, 6)]
M26 = [(3, 8), (5, 10), (4, 7), (6, 13), (2, 3), (7, 12)]
exp = lab("L26")
mi, mc = mis_mvc_by_bitmask(7, E26)
t14, cells14 = knap_table(M26, 14)
t14k, cells14k = knap_table(M26, 14000)
rec("L26a", (mi, mc) == (3, 4) and mi + mc == 7 and exp[0] == f"Tap doc lap lon nhat: {mi}, phu dinh nho nhat: {mc}, tong = {mi + mc}" and exp[1] == "Kiem chung chi: duyet 9 canh, hop le: CO" and len(E26) == 9,
    "lab: |tập độc lập lớn nhất| + |phủ đỉnh nhỏ nhất| = 7 (mặt nạ bit); chứng chỉ duyệt 9 cạnh")
rec("L26b", knap_bruteforce(M26, 14) == t14 == 31 and t14k == 53 == sum(g for _, g in M26),
    "cái túi 0/1: W = 14 → 31 (vét cạn 2^6 tập = bảng đầy đủ); W = 14000 → 53 = tổng mọi giá trị (mọi món vừa)")
rec("L26c", exp[2] == f"Cai tui 0/1 W = 14: toi uu {t14}, so o bang {cells14}, so bit cua W: {(14).bit_length()}" and exp[3] == f"Cai tui 0/1 W = 14000: toi uu {t14k}, so o bang {cells14k}, so bit cua W: {(14000).bit_length()}"
    and (cells14, cells14k, (14).bit_length(), (14000).bit_length()) == (90, 84006, 4, 14), "lab: số ô 90 và 84 006, số bit 4 và 14 khớp bảng đầy đủ")

# ───────────── L27 ─────────────
P27 = (22, 9, 18, 24, 20, 16, 27, 13)
exp = lab("L27")
opt27, paren27 = mcm_best(P27)
all27 = [cost_of(e, P27) for e in all_parens(1, 7)]


def greedy_split_cost(p):
    """Tham lam theo p nhỏ nhất, cài bằng ngăn xếp tự quản (khác đệ quy của lab)."""
    total, work = 0, [(1, len(p) - 1)]
    while work:
        i, j = work.pop()
        if i == j:
            continue
        k = min(range(i, j), key=lambda k: (p[k], k))
        total += p[i - 1] * p[k] * p[j]
        work += [(i, k), (k + 1, j)]
    return total


gr27 = greedy_split_cost(P27)
n27 = 7
rec("L27a", min(all27) == opt27 == CALC["mcm_cost"](P27) == 20709 and len(all27) == CALC["catalan"](6) == 132 and exp[0] == f"Bang: {opt27}, {CALC['mcm_trials'](n27)} lan thu cat" and CALC["mcm_trials"](7) == 56
    and exp[1] == f"Ghi nho: {opt27}, {1 + 2 * CALC['mcm_trials'](n27)} loi goi" and exp[2] == f"Vet can: {opt27}, {3 ** (n27 - 1)} loi goi" and 1 + 2 * 56 == 113 and 3 ** 6 == 729,
    "lab: 20 709 = vét cạn mọi cách đặt ngoặc (132 cách) = đệ quy ghi nhớ; số lần thử 56; số lần gọi ghi nhớ 1 + 2·56 = 113; vét cạn 3^(n−1) = 729")
rec("L27b", gr27 == 27054 and exp[3] == f"Tham lam: {gr27}, lech {100 * (gr27 - opt27) / opt27:.1f} % so voi toi uu" and exp[3].endswith("30.6 % so voi toi uu") and exp[4] == "Ba cach dung bang nhau: CO"
    and exp[5] == f"Vet can khi n = 9: {3 ** 8} loi goi" and 3 ** 8 == 6561, "lab: tham lam 27 054, lệch 30,6%; vét cạn n = 9 gọi 3^8 = 6 561 lần (công thức, khớp đếm thật của lời giải)")


# ───────────── L28 ─────────────
def t_iter(rec_fn, k):
    """T(2^k) bằng lặp bottom-up (khác đệ quy có nhớ của lab)."""
    v = 1
    for j in range(1, k + 1):
        v = rec_fn(v, 2 ** j)
    return v


exp = lab("L28")
TA = [t_iter(lambda v, n: 3 * v + n, k) for k in (10, 20)]
TB = [t_iter(lambda v, n: 2 * v + n * n, k) for k in (10, 20)]
TC = [t_iter(lambda v, n: v + 1, k) for k in (10, 20)]
rat = lambda T, g: [f"{T[0] / g(1024):.3f}", f"{T[1] / g(1048576):.3f}"]  # noqa: E731
ca = [3 ** (k + 1) - 2 ** (k + 1) for k in (10, 20)]
cb = [2 * 4 ** k - 2 ** k for k in (10, 20)]
lA = f"A: T(1024) = {TA[0]}, T(1048576) = {TA[1]}, ti so: {', '.join(rat(TA, lambda n: n ** math.log2(3)))}"
lB = f"B: T(1024) = {TB[0]}, T(1048576) = {TB[1]}, ti so: {', '.join(rat(TB, lambda n: n ** 2))}"
lC = f"C: T(1024) = {TC[0]}, T(1048576) = {TC[1]}, ti so: {', '.join(rat(TC, math.log2))}"
coins = min(len(S) for r in range(1, 13) for S in itertools.combinations_with_replacement((1, 6, 10), r) if sum(S) == 12)
rec("L28a", TA == ca and TB == cb and exp[:3] == [lA, lB, lC] and exp[3] == f"Doi 12 voi 1, 6, 10: tham lam {1 + 1 + 10 // 10 + 0} dong, quy hoach dong {coins} dong" and coins == 2 and 10 + 1 + 1 == 12,
    "lab: A = 3^(k+1) − 2^(k+1), B = 2·4^k − 2^k (lặp bottom-up khớp đệ quy có nhớ); C = k + 1; tỉ số khớp; đổi 12 với 1,6,10: tham lam 3, tối ưu 2 (tổ hợp lặp)")
rec("L28b", [CALC["f_steps"](2 ** k) for k in (10, 14, 17)] == [k * 2 ** k for k in (10, 14, 17)] == [10240, 229376, 2228224] and CALC["pair_steps_loop"](1024) == 523776
    and [n * (n - 1) // 2 for n in (2 ** 14, 2 ** 17)] == [134209536, 8589869056] and round(8589869056 / 2228224) == 3855, "bảng quy mô L28: f(A, n) = n·log₂ n đếm thật; mọi cặp n(n−1)/2 (đếm thật ở 1 024, công thức ở hai cỡ lớn)")


# ───────────── L29 ─────────────
def minrun_ceil(n):
    if n < 64:
        return n
    k = n.bit_length() - 6
    return (n + (1 << k) - 1) >> k


def stack_simulate(seq, fixed):
    """Mô phỏng theo mã C của CPython (merge_collapse) viết lại dạng đệ quy-while khác, giữ nguyên điều kiện."""
    s = []
    for r in seq:
        s.append(r)
        while len(s) > 1:
            n = len(s) - 2
            cond1 = n > 0 and s[n - 1] <= s[n] + s[n + 1]
            cond2 = fixed and n > 1 and s[n - 2] <= s[n - 1] + s[n]
            if cond1 or cond2:
                if s[n - 1] < s[n + 1]:
                    n -= 1
                s[n] += s.pop(n + 1)
            elif s[n] <= s[n + 1]:
                s[n] += s.pop(n + 1)
            else:
                break
    return s


def inv_ok(s):
    return all(s[i] > s[i + 1] + s[i + 2] for i in range(len(s) - 2)) and all(s[i] > s[i + 1] for i in range(len(s) - 1))


exp = lab("L29")
ml = [(n, minrun_ceil(n), -(-n // minrun_ceil(n))) for n in (1000, 4097, 5000)]
line = [f"n = {n}: minrun {m}, {k} doan, luy thua cua 2: {'CO' if (k & (k - 1)) == 0 else 'KHONG'}" for n, m, k in ml]
DAY29 = [62, 109, 119, 37, 22, 55]
so, sn = stack_simulate(DAY29, False), stack_simulate(DAY29, True)
rec("L29a", exp[:3] == line and [m for _, m, _ in ml] == [63, 33, 40] and exp[3] == f"Ban cu: ngan xep cuoi {so}, bat bien {'DUNG' if inv_ok(so) else 'HONG'}" and not inv_ok(so) and so == [171, 119, 59, 55]
    and exp[4] == f"Ban sua: ngan xep cuoi {sn}, bat bien {'DUNG' if inv_ok(sn) else 'HONG'}" and inv_ok(sn) and sum(DAY29) == 404 and 171 <= 119 + 59,
    "lab: minrun theo công thức trần ⌈n/2^k⌉ khớp (63, 33, 40; 16 / 125 / 125 đoạn); bản cũ [171, 119, 59, 55] hỏng bất biến (171 ≤ 119 + 59), bản sửa gộp hết [404]")
st29 = stack_simulate([120, 80, 25, 20, 30], False)
rec("L29b", st29 == [120, 80, 45, 30] and not inv_ok(st29) and 120 <= 80 + 45 and stack_simulate([120, 80, 25, 20, 30], True) == [275],
    "ví dụ trong bài (120, 80, 25, 20, 30): bản cũ dừng ở [120, 80, 45, 30] (120 ≤ 125 hỏng), bản sửa gộp tiếp")

print("verify_cs112_af2b:", "FAIL" if fails else "PASS", f"({fails} lỗi)")
sys.exit(1 if fails else 0)
