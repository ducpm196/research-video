"""Kiểm chứng bằng máy mọi ví dụ số và phát biểu đáng ngờ của bản thảo CS112 (audit/cs112/CS112_ban_thao_goc.yaml).
Mỗi mục in PASS (bản thảo đúng), FIX (bản thảo sai/thiếu điều kiện — video phải nói cách đúng) hoặc FAIL (kiểm không qua).
Chạy: .venv/Scripts/python audit/cs112/verify_cs112.py      (kết quả dùng trong audit/cs112/AUDIT_CS112.md)"""
import itertools
import math
import random
import sys

import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
n, x, k = sp.symbols("n x k", positive=True, integer=True)
rows = []


def rec(cid, status, msg):
    rows.append((cid, status, msg))
    print(f"{status:4} | {cid:4} | {msg}")


# ── C1. L00: vòng for(i = 1; i <= n; i++) so sánh n + 1 lần ──
def loop_cmp(nn):
    c, i = 0, 1
    while True:
        c += 1
        if not i <= nn:
            break
        i += 1
    return c
rec("C1", "PASS" if all(loop_cmp(m) == m + 1 for m in range(0, 50)) else "FAIL",
    "for i = 1..n: điều kiện i <= n được so sánh n + 1 lần (lần cuối trả sai để thoát), kể cả n = 0 (1 lần)")


# ── C2. L00: vòng trong j = n−y..y; tổng số lần so sánh điều kiện vòng trong ──
def inner_cmp(nn):
    c = 0
    for y in range(1, nn + 1):
        j = nn - y
        while True:
            c += 1
            if not j <= y:
                break
            j += 1
    return c
even_ok = all(inner_cmp(m) * 4 == m * m + 8 * m + 4 for m in range(2, 60, 2))
odd_ok = all(inner_cmp(m) * 4 == m * m + 8 * m + 3 for m in range(1, 60, 2))
cl_ok = all((max(0, 2 * y - m + 1) > 0) == (y >= math.ceil(m / 2)) for m in range(1, 40) for y in range(1, m + 1))
rec("C2", "PASS" if even_ok and cl_ok else "FAIL",
    "vòng trong chạy ⇔ y ≥ ⌈n/2⌉; tổng so sánh vòng trong = (n² + 8n + 4)/4 với n chẵn (mô phỏng n = 2..58)")
rec("C2b", "FIX" if odd_ok else "FAIL",
    "bản thảo chỉ cho n chẵn; n lẻ ra (n² + 8n + 3)/4 — video phải nói rõ công thức chỉ cho n chẵn")

# ── C3. đẳng thức a^(log_b c) = c^(log_b a) ──
ok = all(abs(a ** math.log(c, b) - c ** math.log(a, b)) < 1e-9 * max(1, a ** math.log(c, b))
         for a in (2, 3, 5) for b in (2, 10) for c in (4, 7, 9))
rec("C3", "PASS" if ok else "FAIL", "a^(log_b c) = c^(log_b a) (thử số)")

# ── C4. năm tổng Sigma ──
i = sp.symbols("i", integer=True, positive=True)
ok = (sp.simplify(sp.summation(i, (i, 1, n)) - n * (n + 1) / 2) == 0
      and sp.simplify(sp.summation(i ** 2, (i, 1, n)) - n * (n + 1) * (2 * n + 1) / 6) == 0
      and sp.simplify(sp.summation(2 ** i, (i, 0, n)) - (2 ** (n + 1) - 1)) == 0)
rec("C4", "PASS" if ok else "FAIL", "Σi = n(n+1)/2, Σi² = n(n+1)(2n+1)/6, Σ_{i=0..n} 2^i = 2^(n+1) − 1")
Hn = [sum(1 / j for j in range(1, m + 1)) for m in (10, 1000, 10 ** 6)]
diff = [h - math.log(m) for h, m in zip(Hn, (10, 1000, 10 ** 6))]
rec("C4b", "FIX", f"tổng điều hoà H_n KHÔNG bằng ln n: H_n − ln n → γ ≈ 0,5772 ({diff[-1]:.4f} ở n = 10⁶); đúng là H_n ∈ Θ(log n), "
    "ln n < H_n ≤ ln n + 1")

# ── C6. mảng động nhân đôi: tổng số lần chép ≤ 2n (khấu hao O(1)), nhưng một lần chèn xấu nhất chép n phần tử ──
def dyn(nn):
    cap, size, copies, worst = 1, 0, 0, 0
    for _ in range(nn):
        if size == cap:
            copies += size
            worst = max(worst, size)
            cap *= 2
        size += 1
    return copies, worst
ok = all(dyn(m)[0] < 2 * m for m in range(1, 5000))
rec("C6", "PASS" if ok else "FAIL", f"nhân đôi sức chứa: tổng chép < 2n với n = 1..4999; lần chèn tệ nhất ở n = 1025 chép {dyn(1025)[1]} phần tử")
rec("C6b", "FIX", "“amortized” = khấu hao trên CẢ DÃY thao tác (tất định), KHÔNG phải “trung bình” theo xác suất; câu fix "
    "của bản thảo lẫn hai khái niệm")

# ── C8. chiều cao cây nhị phân hoàn chỉnh n nút = ⌊log₂ n⌋ ──
ok = all(math.floor(math.log2(m)) == (m.bit_length() - 1) for m in range(1, 5000))
rec("C8", "PASS" if ok else "FAIL", "cây nhị phân HOÀN CHỈNH (complete) n nút cao ⌊log₂ n⌋ cạnh; “đầy đủ” (full) không xác định chiều cao")

# ── C7/C29. Build-Heap O(n): tổng số lần đổi chỗ khi sift-down ≤ n (xấu nhất là mảng tăng dần cho max-heap) ──
def build_heap_swaps(a):
    a = list(a); sw = 0; N = len(a)
    for s in range(N // 2 - 1, -1, -1):
        p = s
        while True:
            l, r = 2 * p + 1, 2 * p + 2; m = p
            if l < N and a[l] > a[m]: m = l
            if r < N and a[r] > a[m]: m = r
            if m == p: break
            a[p], a[m] = a[m], a[p]; sw += 1; p = m
    return sw, a
def is_heap(a):
    return all(a[(q - 1) // 2] >= a[q] for q in range(1, len(a)))
ok = all((lambda r: r[0] <= m and is_heap(r[1]))(build_heap_swaps(range(m))) for m in range(1, 3000, 7))
rec("C7", "PASS" if ok else "FAIL", "Build-Heap (sift-down từ ⌊n/2⌋−1 về 0) đổi chỗ ≤ n lần ở mảng tăng dần (n < 3000) ⇒ Θ(n), không phải n log n")
ok = all((2 * q + 1 - 1) // 2 == q and (2 * q + 2 - 1) // 2 == q for q in range(1000))
rec("C7b", "PASS" if ok else "FAIL", "chỉ số 0: con của i là 2i+1, 2i+2; cha của j là ⌊(j−1)/2⌋")

# ── C9. Θ: 3n² + 5n + 2 với c1 = 3, c2 = 10, n0 = 1 ──
ok = all(3 * m * m <= 3 * m * m + 5 * m + 2 <= 10 * m * m for m in range(1, 10000))
lim = sp.limit((3 * n ** 2 + 5 * n + 2) / n ** 2, n, sp.oo)
rec("C9", "PASS" if ok and lim == 3 else "FAIL", f"3n²+5n+2 ∈ Θ(n²): c1 = 3, c2 = 10, n0 = 1 (kiểm n < 10⁴), giới hạn = {lim}")
rec("C10", "FIX", "phương pháp giới hạn chỉ dùng được khi giới hạn TỒN TẠI: f(n) = n·(2 + (−1)ⁿ) ∈ Θ(n) nhưng f(n)/n dao động 1, 3 "
    "— không có giới hạn; bản thảo thiếu điều kiện này. L = 0 ⇒ o (và O); L = ∞ ⇒ ω (và Ω)")

# ── C11. chuỗi tăng trưởng: đếm số mục, kiểm từng cặp kề bằng giới hạn ──
chain = [sp.Integer(1), sp.log(sp.log(n)), sp.log(n), sp.log(n) ** 2, n ** sp.Rational(1, 3), sp.sqrt(n), n, n * sp.log(n),
         n ** 2, n ** 3, n ** 4, 2 ** n, 3 ** n, 4 ** n, sp.factorial(n), n ** n]
pairs_ok = []
for a, b in zip(chain, chain[1:]):
    if a.has(sp.factorial) or b.has(sp.factorial):
        # sympy không lấy được giới hạn có giai thừa: dùng Stirling bằng số
        f = sp.lambdify(n, sp.log(a) - sp.log(b) if not a.has(sp.factorial) else sp.loggamma(n + 1) - sp.log(b))
        g = sp.lambdify(n, sp.log(b) - sp.loggamma(n + 1)) if b.has(sp.factorial) else None
        vals = [(math.lgamma(m + 1) - m * math.log(4)) if b.has(sp.factorial) else (m * math.log(m) - math.lgamma(m + 1))
                for m in (10, 100, 1000, 10000)]
        pairs_ok.append(all(u < v for u, v in zip(vals, vals[1:])))
    else:
        pairs_ok.append(sp.limit(a / b, n, sp.oo) == 0)
rec("C11", "PASS" if all(pairs_ok) else "FAIL", f"mỗi hàm trong chuỗi tăng chậm hơn hẳn hàm kế (giới hạn tỉ số = 0): {sum(pairs_ok)}/{len(pairs_ok)} cặp")
rec("C11b", "FIX", f"bản thảo gọi “chuỗi 15 bậc” nhưng liệt kê {len(chain)} hàm")
rec("C12", "PASS" if sp.simplify(2 ** (2 * n) - 4 ** n) == 0 and sp.limit(4 ** n / 2 ** n, n, sp.oo) == sp.oo else "FAIL",
    "2^(2n) = 4^n và 4^n/2^n = 2^n → ∞ nên 2^(2n) ∈ ω(2^n)")
a1 = 10 * sp.log(n + 100, 2)            # lg((n+100)^10)
a2 = sp.log(n + 100, 2) ** 10           # (lg(n+100))^10
ln2 = sp.log(n) ** 2
rec("C13", "FIX", f"“5·lg(n+100)^10 < ln²n” chỉ đúng nếu hiểu là lg((n+100)¹⁰) = 10·lg(n+100) (giới hạn tỉ số với ln²n = "
    f"{sp.limit(a1 / ln2, n, sp.oo)}); nếu hiểu là (lg(n+100))¹⁰ thì ngược lại (giới hạn = {sp.limit(ln2 / a2, n, sp.oo)} "
    "⇒ (lg)^10 lớn hơn) — video phải viết ngoặc rõ ràng")
seq = [5 * 10 * sp.log(n + 100, 2), sp.log(n) ** 2, n ** sp.Rational(1, 3), sp.Rational(1, 1000) * n ** 4 + 3 * n ** 3 + 1, 3 ** n,
       2 ** (2 * n)]
ok = all(sp.limit(p / q, n, sp.oo) == 0 for p, q in zip(seq, seq[1:]))
okf = all(math.lgamma(m - 1) > 2 * m * math.log(2) for m in range(40, 400))
rec("C13b", "PASS" if ok and okf else "FAIL", "thứ tự 5·lg((n+100)¹⁰) < ln²n < n^(1/3) < 0,001n⁴+3n³+1 < 3ⁿ < 2^(2n) < (n−2)! (giới hạn tỉ số = 0)")

# ── C14. Tháp Hà Nội ──
def hanoi(m):
    return 1 if m == 1 else 2 * hanoi(m - 1) + 1
ok = all(hanoi(m) == 2 ** m - 1 for m in range(1, 25))
ii = sp.symbols("i", integer=True)
pat = all(hanoi(m) == 2 ** j * hanoi(m - j) + 2 ** j - 1 for m in range(2, 15) for j in range(0, m))
rec("C14", "PASS" if ok and pat else "FAIL", "T(n) = 2T(n−1) + 1, T(1) = 1 ⇒ T(n) = 2ⁿ − 1; quy luật sau i bước 2^i T(n−i) + 2^i − 1, dừng ở i = n − 1")

# ── C15. hàm sinh ──
G = x / ((1 - x) * (1 - 2 * x))
ser = sp.series(G, x, 0, 12).removeO()
ok = all(ser.coeff(x, m) == 2 ** m - 1 for m in range(1, 12))
pf = sp.apart(G, x)
ok2 = sp.simplify(pf - (1 / (1 - 2 * x) - 1 / (1 - x))) == 0
Gs = sp.symbols("G")
sol = sp.solve(sp.Eq(Gs - x, 2 * x * Gs + x ** 2 / (1 - x)), Gs)[0]
rec("C15", "PASS" if ok and ok2 and sp.simplify(sol - G) == 0 else "FAIL",
    f"G(x) − x = 2xG(x) + x²/(1−x) ⇒ G = x/((1−x)(1−2x)) = 1/(1−2x) − 1/(1−x); hệ số xⁿ = 2ⁿ − 1 (sympy apart: {pf})")

# ── C16. findMax: T(n) = 2T(n/2) + 2, T(1) = 0 ⇒ 2n − 2; T(n) = T(n/2) + 1 ⇒ log₂ n ──
def t2(m):
    return 0 if m == 1 else 2 * t2(m // 2) + 2
def t1(m):
    return 0 if m == 1 else t1(m // 2) + 1
ok = all(t2(2 ** e) == 2 * 2 ** e - 2 and t1(2 ** e) == e for e in range(0, 20))
rec("C16", "PASS" if ok else "FAIL", "T(n) = 2T(n/2) + 2 với T(1) = 0 ⇒ 2n − 2 (n = 2^e); T(n) = T(n/2) + 1, T(1) = 0 ⇒ log₂ n")
def t2b(m):
    return 1 if m == 1 else 2 * t2b(m // 2) + 2
ok = all(t2b(2 ** e) == 3 * 2 ** e - 2 for e in range(0, 20))
rec("C16b", "FIX" if ok else "FAIL", "bản thảo không ghi T(1); nghiệm 2n − 2 cần T(1) = 0 (một phần tử: không so sánh). "
    "Nếu T(1) = 1 thì T(n) = 3n − 2 (vẫn Θ(n)) — điều kiện cơ sở phải nêu rõ")
# phần dư quy nạp: giả thiết T(k) ≤ c·k thì T(n) ≤ c·n + 2 (dư +2 > 0, hỏng); giả thiết T(k) ≤ c·k − 2 thì T(n) ≤ c·n − 2
cc = sp.symbols("c", positive=True)
r1 = sp.expand(2 * (cc * n / 2) + 2 - cc * n)
r2 = sp.expand(2 * (cc * n / 2 - 2) + 2 - (cc * n - 2))
rec("C16c", "PASS" if r1 == 2 and r2 == 0 else "FAIL", f"phần dư quy nạp: giả thiết c·k ⇒ R(n) = {r1} > 0 (vỡ); giả thiết c·k − 2 ⇒ R(n) = {r2} ≤ 0")

# ── C17. T(n) = √n·T(√n) + n ──
def tsq(e, T2):   # n = 2^(2^e)
    return T2 if e == 0 else 2 ** (2 ** (e - 1)) * tsq(e - 1, T2) + 2 ** (2 ** e)
ok = all(tsq(e, T2) == 2 ** (2 ** e) * (e + sp.Rational(T2, 2)) for e in range(0, 6) for T2 in (1, 2, 5))
rec("C17", "PASS" if ok else "FAIL", "n = 2^(2^e): T(n) = n·(log₂log₂ n + T(2)/2) đúng tuyệt đối ⇒ Θ(n log log n)")

# ── C18. định lý thợ (Master) ──
rec("C18", "FIX", "TH3 cần điều kiện chính quy a·f(n/b) ≤ c·f(n) với c < 1 (bản thảo bỏ “c < 1”); b > 1 là hằng số thực "
    "(không cần nguyên); có khe hở: T(n) = 2T(n/2) + n·log n không thuộc 3 TH cơ bản (nghiệm Θ(n log² n))")
def ms(m):
    return 0 if m == 1 else 2 * ms(m // 2) + m
ok = all(ms(2 ** e) == 2 ** e * e for e in range(1, 20))
rec("C18b", "PASS" if ok else "FAIL", "T(n) = 2T(n/2) + n, T(1) = 0 ⇒ n·log₂ n (TH2, Θ(n log n))")
def gap(m):
    return 0 if m == 1 else 2 * gap(m // 2) + m * math.log2(m)
ok = all(abs(gap(2 ** e) - 2 ** e * e * (e + 1) / 2) < 1e-6 for e in range(1, 20))
rec("C18c", "PASS" if ok else "FAIL", "T(n) = 2T(n/2) + n·log₂ n ⇒ n·log₂n·(log₂n + 1)/2 = Θ(n log² n) — ngoài 3 TH cơ bản")

# ── C19. giảm để trị ──
def ins_cmp_worst(m):
    a = list(range(m, 0, -1)); c = 0
    for q in range(1, m):
        v = a[q]; p = q - 1
        while p >= 0:
            c += 1
            if a[p] > v:
                a[p + 1] = a[p]; p -= 1
            else:
                break
        a[p + 1] = v
    return c
ok = all(ins_cmp_worst(m) == m * (m - 1) // 2 for m in range(1, 80))
rec("C19", "PASS" if ok else "FAIL", "sắp xếp chèn, mảng giảm dần: n(n−1)/2 phép so sánh — đúng T(n) = T(n−1) + (n−1)")
rec("C19b", "FIX", "“sắp xếp trước để tìm Min/Max trong O(1)” gây hiểu sai: sắp xếp tốn Θ(n log n) trong khi tìm min/max chỉ cần "
    "n − 1 phép so sánh; ví dụ đúng của biến đổi để trị là kiểm phần tử trùng (Θ(n²) → Θ(n log n))")

# ── C20. quay lui hoán vị: có / không trả lại đánh dấu ──
def perms(m, unmark=True):
    out, used, cur = [], [False] * m, []
    def bt():
        if len(cur) == m:
            out.append(tuple(cur)); return
        for j in range(m):
            if not used[j]:
                used[j] = True; cur.append(j); bt(); cur.pop()
                if unmark:
                    used[j] = False
    bt()
    return out
ok = all(len(perms(m)) == math.factorial(m) and len(perms(m, False)) == 1 for m in range(1, 8))
rec("C20", "PASS" if ok else "FAIL", "liệt kê hoán vị: có trả lại đánh dấu ⇒ n! nghiệm; quên trả lại ⇒ chỉ 1 nghiệm (n = 1..7)")

# ── C21. TSP nhánh cận: ma trận 5×5 kinh điển (Horowitz–Sahni) ──
INF = math.inf
C = [[INF, 20, 30, 10, 11], [15, INF, 16, 4, 2], [3, 5, INF, 2, 4], [19, 6, 18, INF, 3], [16, 4, 7, 16, INF]]
rmin = [min(r) for r in C]
C1 = [[v - rmin[a] for v in C[a]] for a in range(5)]
cmin = [min(C1[a][b] for a in range(5)) for b in range(5)]
best = min((sum(C[t[q]][t[(q + 1) % 5]] for q in range(5)), t) for t in [(0,) + p for p in itertools.permutations(range(1, 5))])
rec("C21", "PASS" if rmin == [10, 2, 2, 3, 4] and cmin == [1, 0, 3, 0, 0] and sum(rmin) + sum(cmin) == 25 else "FAIL",
    f"rút gọn hàng {rmin} (= {sum(rmin)}), cột trên ma trận MỚI {cmin} (= {sum(cmin)}), cận dưới gốc 25; "
    f"tối ưu vét cạn = {best[0]} theo chu trình {[v + 1 for v in best[1]]}")
cmin_wrong = [min(C[a][b] for a in range(5)) for b in range(5)]
rec("C21b", "PASS", f"lỗi lấy min cột trên ma trận GỐC: {cmin_wrong} (tổng {sum(cmin_wrong)}) ≠ {cmin} — bẫy của bản thảo có thật")

# ── C22. ba lô phân số ──
M, w, p = 20, [18, 15, 10], [25, 24, 15]
order = sorted(range(3), key=lambda q: -p[q] / w[q])
rem, val, xs = M, sp.Integer(0), [0, 0, 0]
for q in order:
    take = min(1, sp.Rational(rem, w[q])); xs[q] = take; val += take * p[q]; rem -= take * w[q]
rec("C22", "PASS" if order == [1, 2, 0] and xs == [0, 1, sp.Rational(1, 2)] and val == sp.Rational(63, 2) else "FAIL",
    f"đơn giá {[round(p[q] / w[q], 3) for q in range(3)]}, thứ tự 2→3→1, x = {xs}, giá trị {val} = 31,5")
# 0/1: tham lam theo đơn giá sai
W2, w2, p2 = 50, [10, 20, 30], [60, 100, 120]
greedy01 = 0; r2_ = W2
for q in sorted(range(3), key=lambda q: -p2[q] / w2[q]):
    if w2[q] <= r2_:
        greedy01 += p2[q]; r2_ -= w2[q]
opt01 = max(sum(p2[q] for q in S) for L in range(4) for S in itertools.combinations(range(3), L) if sum(w2[q] for q in S) <= W2)
rec("C22b", "PASS" if greedy01 == 160 and opt01 == 220 else "FAIL",
    f"ba lô 0/1 (W = 50, w = 10, 20, 30, p = 60, 100, 120): tham lam theo đơn giá = {greedy01} < tối ưu {opt01}")

# ── C23. lập lịch hoạt động ──
def ef(acts):
    cnt, last = 0, -INF
    for s, f in sorted(acts, key=lambda a: a[1]):
        if s >= last:
            cnt += 1; last = f
    return cnt
def by_key(acts, key):
    cnt, chosen = 0, []
    for s, f in sorted(acts, key=key):
        if all(f <= s2 or f2 <= s for s2, f2 in chosen):
            chosen.append((s, f)); cnt += 1
    return cnt
def opt(acts):
    for L in range(len(acts), 0, -1):
        for S in itertools.combinations(acts, L):
            if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(S, 2)):
                return L
    return 0
random.seed(1)
ok = True
for _ in range(400):
    acts = [(s, s + random.randint(1, 6)) for s in (random.randint(0, 12) for _ in range(random.randint(1, 7)))]
    ok &= ef(acts) == opt(acts) and by_key(acts, lambda a: -a[0]) == opt(acts)
ce_start = [(0, 10), (1, 2), (3, 4)]
ce_short = [(0, 5), (4, 7), (6, 11)]
rec("C23", "PASS" if ok and by_key(ce_start, lambda a: a[0]) == 1 < opt(ce_start) and by_key(ce_short, lambda a: a[1] - a[0]) == 1 < opt(ce_short)
    else "FAIL", "kết thúc sớm nhất = tối ưu (400 bộ ngẫu nhiên, so vét cạn); bắt đầu sớm nhất sai với (0,10),(1,2),(3,4); "
    "ngắn nhất sai với (0,5),(4,7),(6,11)")
rec("C23b", "FIX", "“duy nhất xếp theo f_i là đúng” quá mạnh: chọn hoạt động BẮT ĐẦU MUỘN NHẤT (duyệt ngược) cũng tối ưu "
    "(đối xứng; kiểm cùng 400 bộ) — nói đúng là: tiêu chí đã chứng minh tối ưu là kết thúc sớm nhất")

# ── C24. đặt ngoặc biểu thức để giá trị lớn nhất ──
def expr_dp(vals, ops):
    m_ = len(vals); D = {}
    for q in range(m_):
        D[q, q] = sp.nsimplify(vals[q])
    for L in range(2, m_ + 1):
        for a in range(0, m_ - L + 1):
            b = a + L - 1
            D[a, b] = max((D[a, c] + D[c + 1, b]) if ops[c] == "+" else (D[a, c] * D[c + 1, b]) for c in range(a, b))
    return D
def all_vals(vals, ops):
    if len(vals) == 1:
        return {sp.nsimplify(vals[0])}
    res = set()
    for c in range(len(ops)):
        for u in all_vals(vals[:c + 1], ops[:c]):
            for v in all_vals(vals[c + 1:], ops[c + 1:]):
                res.add(u + v if ops[c] == "+" else (u * v if ops[c] == "*" else u - v))
    return res
D = expr_dp(["6", "0", "6", "0.1"], ["+", "*", "+"])
R = sp.Rational
ok = (D[0, 1] == 6 and D[1, 2] == 0 and D[2, 3] == R(61, 10) and D[0, 2] == 36 and D[1, 3] == R(1, 10) and D[0, 3] == R(183, 5)
      and max(all_vals(["6", "0", "6", "0.1"], ["+", "*", "+"])) == R(183, 5))
rec("C24", "PASS" if ok else "FAIL", "6 + 0 × 6 + 0,1: hàng L=2 [6, 0, 6,1]; L=3 [36; 0,1]; đích 36,6 tại cắt sau 0 (k=1, chỉ số từ 0); "
    "khớp vét cạn mọi cách đặt ngoặc")
# phản ví dụ: có phép trừ thì “chỉ lấy max” sai
def expr_dp_max_only(vals, ops):
    m_ = len(vals); D = {(q, q): sp.nsimplify(vals[q]) for q in range(m_)}
    f = {"+": lambda u, v: u + v, "-": lambda u, v: u - v, "*": lambda u, v: u * v}
    for L in range(2, m_ + 1):
        for a in range(0, m_ - L + 1):
            b = a + L - 1
            D[a, b] = max(f[ops[c]](D[a, c], D[c + 1, b]) for c in range(a, b))
    return D[0, m_ - 1]
ce = next(((v_, o_) for L in (3, 4) for v_ in itertools.product("0123", repeat=L)
           for o_ in itertools.product("+-*", repeat=L - 1)
           if expr_dp_max_only(list(v_), list(o_)) != max(all_vals(list(v_), list(o_)))), None)
v3, o3 = list(ce[0]), list(ce[1])
txt = " ".join(a_ + " " + b_ for a_, b_ in zip(v3, o3 + [""])).strip()
rec("C24b", "FIX" if ce else "FAIL",
    f"công thức chỉ-lấy-max đúng khi mọi số ≥ 0 và chỉ có + và × (hai phép đồng biến); phản ví dụ nhỏ nhất máy tìm được: "
    f"{txt}: chỉ-lấy-max = {expr_dp_max_only(v3, o3)} nhưng lớn nhất thật = {max(all_vals(v3, o3))} — có phép trừ thì phải giữ "
    "cả min. Bản thảo gọi bài này là “nhân chuỗi ma trận”: SAI, đó là hai bài toán khác nhau cùng khuôn DP theo đoạn")
# với + và × trên số không âm, max-only khớp vét cạn
random.seed(3)
ok = all(expr_dp_max_only(v_, o_) == max(all_vals(v_, o_)) for v_, o_ in
         (([str(random.randint(0, 9)) for _ in range(L)], [random.choice("+*") for _ in range(L - 1)])
          for L in (random.randint(1, 6) for _ in range(300))))
rec("C24c", "PASS" if ok else "FAIL", "chỉ + và ×, số không âm: max-only khớp vét cạn trên 300 biểu thức ngẫu nhiên")

# ── C25. nhân chuỗi ma trận ──
def mcm(pp):
    m_ = len(pp) - 1; Dm = {(q, q): 0 for q in range(1, m_ + 1)}; Sx = {}
    for L in range(2, m_ + 1):
        for a in range(1, m_ - L + 2):
            b = a + L - 1
            Dm[a, b], Sx[a, b] = min((Dm[a, c] + Dm[c + 1, b] + pp[a - 1] * pp[c] * pp[b], c) for c in range(a, b))
    return Dm, Sx
D1, _ = mcm([10, 30, 5, 60]); D2, S2 = mcm([40, 20, 30, 10, 30])
calls = []
def bf(a, b):
    calls.append(1)
    if a == b:
        return 0
    return min(bf(a, c) + bf(c + 1, b) for c in range(a, b))
ok3 = True
for m_ in range(1, 12):
    calls.clear(); bf(1, m_); ok3 &= len(calls) == 3 ** (m_ - 1)
cat = [math.comb(2 * (m_ - 1), m_ - 1) // m_ for m_ in range(1, 12)]
rec("C25", "PASS" if D1[1, 3] == 4500 and D2[1, 4] == 26000 and S2[1, 4] == 3 and ok3 else "FAIL",
    f"p = (10,30,5,60) ⇒ 4500; p = (40,20,30,10,30) ⇒ 26000, cắt cuối k = 3; vét cạn đệ quy gọi đúng 3^(n−1) lần (n ≤ 11)")
rec("C25b", "FIX", f"bản thảo BTL ghi vét cạn O(4ⁿ/n^1,5) (số Catalan = số CÁCH đặt ngoặc {cat[:8]}…) nhưng hàm đệ quy vét cạn "
    "gọi 3^(n−1) lần ⇒ Θ(3ⁿ); “p = [6, 0, 6, 0,1]” không phải kích thước ma trận hợp lệ")

# ── C26. LIS / LCS ──
def lis(a):
    L = [1] * len(a)
    for q in range(len(a)):
        for r in range(q):
            if a[r] < a[q]:
                L[q] = max(L[q], L[r] + 1)
    return max(L)
def lis_bf(a):
    return max(len(S) for r in range(len(a) + 1) for S in itertools.combinations(a, r) if all(u < v for u, v in zip(S, S[1:])))
def lcs(X, Y):
    c = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
    for q in range(1, len(X) + 1):
        for r in range(1, len(Y) + 1):
            c[q][r] = c[q - 1][r - 1] + 1 if X[q - 1] == Y[r - 1] else max(c[q - 1][r], c[q][r - 1])
    return c[-1][-1]
def lcs_bf(X, Y):
    subs = {S for r in range(len(X) + 1) for S in itertools.combinations(X, r)}
    def is_sub(S, T):
        it = iter(T); return all(ch in it for ch in S)
    return max(len(S) for S in subs if is_sub(S, Y))
random.seed(2)
ok = all(lis(a) == lis_bf(a) for a in ([random.randint(0, 9) for _ in range(random.randint(1, 9))] for _ in range(300)))
ok &= all(lcs(X, Y) == lcs_bf(X, Y) for X, Y in ((''.join(random.choice("ABC") for _ in range(random.randint(0, 7))),
                                                 ''.join(random.choice("ABC") for _ in range(random.randint(0, 7)))) for _ in range(300)))
rec("C26", "PASS" if ok else "FAIL", "truy hồi LIS O(n²) và LCS O(mn) khớp vét cạn trên 300 + 300 bộ ngẫu nhiên")

# ── C27. quy hoạch tuyến tính 2 biến ──
V = {"O": (0, 0), "A": (16, 0), "B": (8, 16), "C": (0, 24)}
z = {k_: 15 * a + 10 * b for k_, (a, b) in V.items()}
feas = all(a + b <= 24 and 2 * a + b <= 32 and a >= 0 and b >= 0 for a, b in V.values())
rec("C27", "PASS" if feas and z == {"O": 0, "A": 240, "B": 280, "C": 240} else "FAIL", f"đỉnh và giá trị z: {z}; z lớn nhất 280 tại B(8, 16)")
rec("C27b", "FIX", "“thiếu điều kiện không âm thì miền nghiệm vô hạn” đúng về MIỀN, nhưng ở ví dụ này z vẫn ≤ 280 vì "
    "15x₁ + 10x₂ = 5(x₁ + x₂) + 5(2x₁ + x₂) ≤ 5·24 + 5·32 = 280 — không được nói “sẽ ra kết quả sai” cho ví dụ này")

# ── C28. đơn hình trên cùng bài ──
T = [[1, 1, 1, 0, 24], [2, 1, 0, 1, 32]]; zrow = [-15, -10, 0, 0, 0]; basis = [2, 3]
steps = []
while min(zrow[:4]) < 0:
    e = min(range(4), key=lambda q: zrow[q])
    ratios = [(sp.Rational(T[r][4], T[r][e]), r) for r in range(2) if T[r][e] > 0]
    _, lr = min(ratios)
    piv = sp.Rational(T[lr][e]); T[lr] = [sp.Rational(v) / piv for v in T[lr]]
    for r in range(2):
        if r != lr:
            f = T[r][e]; T[r] = [u - f * v for u, v in zip(T[r], T[lr])]
    f = zrow[e]; zrow = [u - f * v for u, v in zip(zrow, T[lr])]; basis[lr] = e
    steps.append((e, lr))
sol = {basis[r]: T[r][4] for r in range(2)}
rec("C28", "PASS" if sol.get(0) == 8 and sol.get(1) == 16 and zrow[4] == 280 else "FAIL",
    f"đơn hình (cột vào = hệ số âm nhất, hàng ra = tỉ số nhỏ nhất): {len(steps)} lần xoay {steps}, nghiệm x₁ = 8, x₂ = 16, z = {zrow[4]}")

# ── C29. findMax của giao-an-dsa-cs112-toan-dien.tex (dòng 221–227): đúng khi nào, đếm bao nhiêu ──
def findmax_tex(a, l, r, cnt, count_max):
    if l == r:
        return a[l]
    m = (l + r) // 2
    cnt[0] += 1
    if a[m] < a[m + 1]:
        return findmax_tex(a, m + 1, r, cnt, count_max)
    cnt[0] += 1
    if a[m] > a[m + 1]:
        return findmax_tex(a, l, m, cnt, count_max)
    x, y = findmax_tex(a, m + 1, r, cnt, count_max), findmax_tex(a, l, m, cnt, count_max)
    cnt[0] += 1 if count_max else 0
    return max(x, y)
random.seed(4)
uni_ok = all(findmax_tex(a, 0, len(a) - 1, [0], True) == max(a)
             for a in (sorted(random.sample(range(100), p + 1)) + sorted(random.sample(range(-100, 0), q), reverse=True)
                       for p in range(0, 7) for q in range(0, 7) for _ in range(20)))
wrong = sum(findmax_tex(a, 0, len(a) - 1, [0], True) != max(a) for a in ([random.randint(0, 9) for _ in range(8)] for _ in range(1000)))
rec("C29", "FIX" if uni_ok and findmax_tex([5, 1, 2, 3], 0, 3, [0], True) == 3 else "FAIL",
    f"findMax của bản .tex chỉ đúng với dãy ĐƠN ĐỈNH (tăng rồi giảm): đúng trên mọi dãy đơn đỉnh thử; sai {wrong}/1000 mảng ngẫu nhiên; "
    "[5, 1, 2, 3] → 3 (thật 5). Bản thảo không nêu điều kiện này")
eq = [(lambda c: (findmax_tex([7] * n, 0, n - 1, c, False), c[0])[1])([0]) for n in (2, 4, 8, 16)]
eqm = [(lambda c: (findmax_tex([7] * n, 0, n - 1, c, True), c[0])[1])([0]) for n in (2, 4, 8, 16)]
inc = [(lambda c: (findmax_tex(list(range(n)), 0, n - 1, c, True), c[0])[1])([0]) for n in (2, 4, 8, 1024)]
rec("C29b", "FIX" if eq == [2 * n - 2 for n in (2, 4, 8, 16)] and eqm == [3 * n - 3 for n in (2, 4, 8, 16)] and inc == [1, 2, 3, 10] else "FAIL",
    f"mọi phần tử bằng nhau: {eq} = 2n − 2 nếu chỉ đếm 2 phép so sánh điều kiện (khớp 2T(n/2) + 2), {eqm} = 3n − 3 nếu đếm cả max; "
    f"dãy tăng: {inc} = log₂ n — phải nói rõ đếm phép so sánh nào")

# ───────── L29 — bài hành trình Timsort (audit/cs112/sources_L29.md) ─────────
from fractions import Fraction as _Fr


def _minrun_old(n):            # listsort.txt 2002: 6 bit đầu của n, cộng 1 nếu các bit còn lại khác 0
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def _minruns_new(n, k):        # listsort.txt 2025 (gen_minruns_simpler), chép nguyên ý
    e = 0
    while (n >> e) >= 64:
        e += 1
    mask, cur, out = (1 << e) - 1, 0, []
    for _ in range(k):
        cur += n
        out.append(cur >> e)
        cur &= mask
    return out


def _collapse_jdk7(st):        # mergeCollapse của jdk7 (CAV15 Listing 3), chép nguyên ý; chỉ cộng độ dài
    st = list(st)
    while len(st) > 1:
        n = len(st) - 2
        if n > 0 and st[n - 1] <= st[n] + st[n + 1]:
            if st[n - 1] < st[n + 1]:
                n -= 1
            st[n:n + 2] = [st[n] + st[n + 1]]
        elif st[n] <= st[n + 1]:
            st[n:n + 2] = [st[n] + st[n + 1]]
        else:
            break
    return st


def _inv_ok(st):               # bất biến trên CẢ ngăn xếp: A > B + C và B > C ở mọi vị trí
    return all(st[i] > st[i + 1] + st[i + 2] for i in range(len(st) - 2)) and all(st[i] > st[i + 1] for i in range(len(st) - 1))


rec("T29a", "PASS" if _minrun_old(2112) == 33 and divmod(2112, 32) == (66, 0) and divmod(2112, 33) == (64, 0) and _minrun_old(315) == 40
    and round(sum(math.log2(i) for i in range(1, 2 ** 20 + 1))) == 19458756 and round((19606028 / 19458756 - 1) * 100, 2) == 0.76 else "FAIL",
    "L29 chặng 1: minrun(2112) = 33 (32 → 66 đoạn, 33 → 64 đoạn), minrun(315) = 40; log₂(2^20)! ≈ 19 458 756 (bảng LS02), timsort hơn 0,76%")
_b = [0, 16]
while len(_b) < 60:
    _b.append(_b[-1] + _b[-2] + 1)
_bound = [next(B for B in range(60) if 1 + sum(_b[:B + 1]) > L) for L in (119, 1541, 119150, 2 ** 31 - 1)]
rec("T29b", "PASS" if _bound == [4, 9, 18, 39] and [x + 1 for x in _bound] == [5, 10, 19, 40] else "FAIL",
    f"L29 chặng 2: dãy b (0, 16, b+b+1) cho số ô đủ dùng {_bound} — mã Java 5/10/19/40 dư 1 ô (CAV15 §3.1)")
_after = _collapse_jdk7([120, 80, 25, 20, 30])
rec("T29c", "PASS" if _after == [120, 80, 45, 30] and not _inv_ok(_after) and _inv_ok(_after[1:]) and 80 + 45 == 125
    and 2 ** 26 == 67108864 else "FAIL",
    f"L29 chặng 3: mergeCollapse jdk7 trên 120, 80, 25, 20, 30 → {_after}: ba đoạn trên thoả, 120 ≤ 125 hỏng; 2^26 = 67 108 864")


def _power(s1, n1, n2, n):     # listsort.txt (powersort): L nhỏ nhất để ((s1 + n1/2)/n, (s2 + n2/2)/n] chứa J/2^L
    a, b = _Fr(2 * s1 + n1, 2 * n), _Fr(2 * (s1 + n1) + n2, 2 * n)
    return next(L for L in range(1, 64) if any(a < _Fr(J, 2 ** L) <= b for J in range(2 ** L + 1)))


rec("T29d", "PASS" if [_power(0, 4, 4, 8), _power(0, 2, 2, 8), _power(2, 2, 4, 8)] == [1, 2, 1] else "FAIL",
    "L29 chặng 4: sức của chỗ nối (n = 8): đoạn 4|4 → 1; đoạn 2|2|4 → 2 rồi 1 (đối chiếu định nghĩa bằng vét cạn J)")
_new = _minruns_new(315, 8)
_new2 = _minruns_new(32769, 1024)
rec("T29e", "PASS" if _new == [39, 39, 40, 39, 39, 40, 39, 40] and sum(_new) == 315
    and [_new[i] + _new[i + 1] for i in (0, 2, 4, 6)] == [78, 79, 79, 79]
    and sum(_new2) == 32769 and _new2.count(32) == 1023 and _new2.count(33) == 1 and _minrun_old(32769) == 33 and 32769 // 33 == 993
    and _new == [((i + 1) * 315 >> 3) - (i * 315 >> 3) for i in range(8)] else "FAIL",
    "L29 chặng 5: 315 → 39 39 40 39 39 40 39 40 (cộng dồn phần lẻ = hiệu phần nguyên), trộn 78 79 79 79 → 157 158 → 315; 32769: cũ 993 đoạn, mới 1024")
rec("T29f", "PASS" if math.factorial(10) == 3628800 and 2 ** 26 * 8 > 500 * 10 ** 6 and 33 * 64 == 2112 and 39 * 5 + 40 * 3 == 315 else "FAIL",
    "L29 tự kiểm và quiz: 10! = 3 628 800; 2^26 · 8 > 500 triệu; 33·64 = 2112; 5·39 + 3·40 = 315")

print()
print("tổng:", {s: sum(1 for r in rows if r[1] == s) for s in ("PASS", "FIX", "FAIL")})
sys.exit(1 if any(r[1] == "FAIL" for r in rows) else 0)
