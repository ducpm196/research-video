"""Kiểm độc lập mọi khẳng định của khoá SWF — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Tìm kiếm: so với bisect của thư viện chuẩn. Bất biến: sympy cho bước duy trì, vét cạn n ≤ 300. Euclid: math.gcd. Tràn 32 bit: ctypes.c_int32.
Tam giác: phân loại lại bằng định nghĩa trên mọi bộ cạnh 0..6. Độ phủ: liệt kê bằng itertools. Tính chất: vét cạn. Cây/đống: kiểm bằng
định nghĩa “mọi cặp tổ tiên–con cháu”. Máy trạng thái: duyệt mọi dãy sự kiện độ dài ≤ 6. Đồng thời: liệt kê xen kẽ bằng hoán vị nhãn.
Khoảng tin cậy: hệ số Student bằng sympy.stats; tổng bình phương bằng Fraction. Hợp nhất: so với bảng luật diff3 viết tay. SQL: sqlite3 riêng.
Chạy: .venv/Scripts/python audit/swf/verify_swf.py → PASS/FAIL từng dòng và tổng."""
import bisect
import ctypes
import itertools
import math
import sqlite3
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp
import sympy.stats  # noqa: F401  (nạp mô-đun con sp.stats)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: tìm kiếm nhị phân so với bisect ──
def bs_ref(a, x):
    i = bisect.bisect_left(a, x)
    return i if i < len(a) and a[i] == x else -1


arrs = [[], [1], [2, 5, 8, 12, 16, 23, 38], [1, 3, 5, 7, 9, 11]]
rec("L00a", all(alg.bin_search(a, x)[0] == bs_ref(a, x) for a in arrs for x in range(-1, 40)), "bin_search = bisect trên mọi x −1..39")
rec("L00b", alg.bin_search([2, 5, 8, 12, 16, 23, 38], 23)[0] == 5 and bs_ref([1, 3, 5, 7, 9, 11], 9) == 4, "23 → 5; 9 → 4")
rec("L00c", alg.bin_search([5, 8, 2], 2)[0] == -1 and 2 in [5, 8, 2], "vi phạm tiền điều kiện: −1 dù có 2")
rec("L00d", math.ceil(math.log2(10 ** 6 + 1)) == 20 == len(alg.bin_search(list(range(10 ** 6)), -1)[1]), "một triệu phần tử: 20 bước")

# ── L01: bất biến ──
i = sp.Symbol("i", integer=True, nonnegative=True)
rec("L01a", sp.simplify(i * (i - 1) / 2 + i - (i + 1) * i / 2) == 0, "duy trì: i(i−1)/2 + i = (i+1)i/2 (sympy)")
rec("L01b", all(s == sum(range(k)) == k * (k - 1) // 2 for n in range(300) for k, s in alg.sum_loop_invariant(n)), "bất biến đúng mọi vòng, n < 300")
rec("L01c", [max([3, 9, 2, 7][:k]) for k in range(1, 5)] == [3, 9, 9, 9], "quiz max: 9")

# ── L02: dừng ──
rec("L02a", all(alg.euclid_trace(a, b)[-1][0] == math.gcd(a, b) for a in range(1, 80) for b in range(0, 80)), "Euclid = math.gcd trên mọi cặp < 80")
rec("L02b", all(all(y2 < y1 for (_, y1), (_, y2) in zip(t, t[1:])) for t in (alg.euclid_trace(a, b) for a in range(1, 60) for b in range(1, 60))),
    "b giảm thật sự ở mọi bước")
rec("L02c", [b for _, b in alg.euclid_trace(252, 105)] == [105, 42, 21, 0] and [b for _, b in alg.euclid_trace(100, 35)] == [35, 30, 5, 0], "dãy b")
x, n = 1.0, 0
while x > 0:
    x = x * 0.5
    n += 1
rec("L02d", n == 1075 == alg.halving_steps(), "chia đôi 1.0 tới khi về 0: 1075 lần (nhân 0,5 thay cho chia 2)")


def collatz(m):
    c = 0
    while m != 1:
        m = m // 2 if m % 2 == 0 else 3 * m + 1
        c += 1
    return c


rec("L02e", collatz(27) == 111, "27 cần 111 bước")

# ── L03: biên, tràn ──
rec("L03a", len(range(0, 101, 10)) == 11 and len(range(3, 11)) == 8 and len(list(range(3, 12))) == 9 and len(range(5, 20)) == 15, "đếm cọc, khoảng")
c32 = lambda v: ctypes.c_int32(v).value  # noqa: E731
rec("L03b", c32((2 ** 31 - 2) + (2 ** 31 - 1)) == -3 == alg.wrap32((2 ** 31 - 2) + (2 ** 31 - 1)), "tổng quay vòng −3 (ctypes.c_int32)")
rec("L03c", int(c32(2147483640 + 2147483646) / 2) == -5 == alg.mid32(2147483640, 2147483646, False)
    and 2147483640 + (2147483646 - 2147483640) // 2 == 2147483643 == alg.mid32(2147483640, 2147483646, True), "quiz: −5 và 2147483643")
rec("L03d", alg.mixed_search([1, 3], 5) == "IndexError" and alg.mixed_search([1, 3], 0) == "vô hạn", "trộn khoảng: vượt mảng, lặp vô hạn")


# ── L04: tam giác theo định nghĩa ──
def tri_def(a, b, c):
    if min(a, b, c) <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return "không phải"
    k = len({a, b, c})
    return "đều" if k == 1 else "cân" if k == 2 else "thường"


rec("L04a", all(tri_def(*t) == alg.triangle(*t) for t in itertools.product(range(7), repeat=3)), "phân loại = định nghĩa trên mọi bộ 0..6")
bad = [t for t in itertools.product(range(1, 7), repeat=3) if alg.triangle_buggy(*t) != tri_def(*t)]
rec("L04b", all(sorted(t)[0] + sorted(t)[1] == sorted(t)[2] for t in bad) and (1, 2, 3) in bad and (2, 2, 4) in bad, f"bản lỗi chỉ sai trên biên x + y = z ({len(bad)} bộ)")

# ── L05: độ phủ ──
tests2 = [(True,) * 3, (False,) * 3]
br = {(k, t[k]) for t in tests2 for k in range(3)}
rec("L05a", len(br) == 6 and len(set(itertools.product([0, 1], repeat=3))) == 8 and alg.branch_path_cover(3, tests2) == (6, 6, 2, 8), "6 nhánh, 2 ca; 8 đường")
rec("L05b", 2 ** 10 == 1024 and 2 ** 4 == 16 and alg.branch_path_cover(4, [(True,) * 4, (False,) * 4])[:2] == (8, 8), "1024 đường; quiz 16")

# ── L06: tính chất (vét cạn) ──
L = [list(v) for k in range(5) for v in itertools.product(range(3), repeat=k)]
rec("L06a", len(L) == 121 == sum(3 ** k for k in range(5)), "121 danh sách")
first = next(x for x in L if sorted(set(x)) != sorted(x))
rec("L06b", first == [0, 0] == alg.find_counterexample(lambda x: sorted(sorted(set(x))) == sorted(x), L), "phản ví dụ ngắn nhất [0, 0]")
rec("L06c", all(sorted(sorted(v)) == sorted(v) for v in itertools.product(range(3), repeat=4)), "sorted thật qua 81 danh sách")
rec("L06d", next(x for x in L if sorted([0] * len(x)) != sorted(x)) == [1], "tính chất hoán vị bắt hàm toàn 0 ở [1]")
rb = lambda y: y[::-1][:-1] if y else []  # noqa: E731
rec("L06e", next(x for x in L if rb(rb(x)) != x) == [0], "quiz đảo ngược: [0]")


# ── L07: cây/đống theo định nghĩa tổ tiên–con cháu ──
def bst_def(t):
    def keys(n):
        return [] if n is None else keys(n[1]) + [n[0]] + keys(n[2])

    def ok(n):
        return n is None or (all(k < n[0] for k in keys(n[1])) and all(k > n[0] for k in keys(n[2])) and ok(n[1]) and ok(n[2]))
    return ok(t)


T1 = (10, (5, None, (12, None, None)), (15, None, None))
T2 = (8, (4, (2, None, None), (9, None, None)), (12, None, None))
rec("L07a", bst_def(T1) is False is alg.bst_ok(T1) and alg.bst_local_ok(T1), "cây ví dụ: kiểm cục bộ qua, định nghĩa sai")
rec("L07b", bst_def(T2) is False is alg.bst_ok(T2) and alg.inorder(T2) == [2, 4, 9, 8, 12], "quiz cây: sai, duyệt giữa 2,4,9,8,12")


def heap_def(a):
    return all(a[p] <= a[c] for c in range(len(a)) for p in range(len(a)) if c > 0 and p == (c - 1) // 2)


rec("L07c", [heap_def(a) for a in ([1, 3, 2, 7, 4], [1, 3, 2, 0], [2, 5, 3, 6, 4, 1])] == [True, False, False]
    == [alg.heap_ok(a) for a in ([1, 3, 2, 7, 4], [1, 3, 2, 0], [2, 5, 3, 6, 4, 1])], "đống: đúng, sai, sai")

# ── L08: máy trạng thái — duyệt mọi dãy sự kiện ──
ev = ["hết giờ", "bấm nút"]
pairs = set()
for k in range(1, 7):
    for seq in itertools.product(ev, repeat=k):
        st = alg.fsm_run(alg.TRAFFIC, "ĐỎ", list(seq))
        pairs |= set(zip(st, st[1:]))
rec("L08a", ("XANH", "ĐỎ") not in pairs and {s for p in pairs for s in p} == {"ĐỎ", "XANH", "VÀNG"}, "mọi dãy ≤ 6 sự kiện: không bao giờ XANH → ĐỎ")
rec("L08b", alg.fsm_run(alg.TRAFFIC, "XANH", ["bấm nút", "hết giờ", "bấm nút"])[-1] == "ĐỎ" and 2 ** 4 - 4 == 12 and 2 ** 3 - 3 == 5, "quiz; 5 và 12 tổ hợp vô nghĩa")


# ── L09: đồng thời — liệt kê bằng hoán vị nhãn ──
def finals(times):
    out = set()
    for pos in itertools.combinations(range(6 * times), 3 * times):
        order = ["A" if k in pos else "B" for k in range(6 * times)]
        out.add(alg.race_run("".join(order), times)[0])
    return out


rec("L09a", finals(2) == {2, 3, 4} == alg.race_finals(2) and math.comb(12, 6) == 924, "x += 1 hai lần mỗi luồng: {2, 3, 4} qua 924 cách")
rec("L09b", finals(1) == {1, 2} and math.comb(6, 3) == 20, "quiz: 20 cách, {1, 2}")
rec("L09c", [alg.deadlock_states(a, b) for a, b in (("AB", "BA"), ("AB", "AB"), ("ABC", "CAB"), ("ABC", "ACB"))] == [1, 0, 1, 0], "bế tắc: 1, 0, 1, 0")

# ── L10: thống kê ──
T = sp.stats.StudentT("T", 29)
q = float(sp.N(sp.stats.cdf(T)(sp.Rational(2045, 1000))))
rec("L10a", abs(q - 0.975) < 1e-4, f"hệ số Student 29 bậc tự do: P(T ≤ 2,045) = {q:.5f} ≈ 0,975")
A, B = alg.perf_data()
d = [Fraction(str(a)) - Fraction(str(b)) for a, b in zip(A, B)]
md = sum(d) / 30
sd = math.sqrt(float(sum((x - md) ** 2 for x in d) / 29))
lo, hi = float(md) - 2.045 * sd / math.sqrt(30), float(md) + 2.045 * sd / math.sqrt(30)
rec("L10b", (round(float(md), 2), round(lo, 2), round(hi, 2)) == (4.99, 3.99, 5.99), f"ghép cặp (Fraction): {float(md):.3f} [{lo:.3f}; {hi:.3f}]")
r = alg.unpaired_ci(A, B, 2.045)
rec("L10c", r[2] < 0 < r[3] and (round(r[2], 1), round(r[3], 1)) == (-16.5, 26.5), "không ghép cặp: chứa 0")
rec("L10d", (min(A), max(A)) == (82.7, 203.9) and sum([310, 142, 141, 143, 140]) / 5 == 175.2, "phạm vi A; khởi động")


# ── L11: hợp nhất — bảng luật viết tay ──
def diff3(o, a, b):
    if a == b:
        return a
    if a == o:
        return b
    if b == o:
        return a
    return "XUNG ĐỘT"


ok = True
for o, a, b in itertools.product("xyz", repeat=3):
    m = alg.merge3([o], [a], [b])[0]
    ok &= (m if isinstance(m, str) else "XUNG ĐỘT") == diff3(o, a, b)
rec("L11a", ok, "merge3 khớp bảng luật trên mọi bộ ba giá trị")
try:
    exec("def g(): return 1\ny = f()", {})
    e = None
except NameError:
    e = "NameError"
rec("L11b", e == "NameError" == alg.run_error("def g(): return 1\ny = f()"), "hợp nhất sạch nhưng NameError")

# ── L12: sqlite riêng ──
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE users(name TEXT, pw TEXT); INSERT INTO users VALUES ('alice','a1'),('bob','b2');")
inj = "' OR '1'='1"
n_concat = len(con.execute(f"SELECT name FROM users WHERE name = '{inj}'").fetchall())
n_param = len(con.execute("SELECT name FROM users WHERE name = ?", (inj,)).fetchall())
inj2 = "x' OR 1=1 --"
n2 = len(con.execute(f"SELECT name FROM users WHERE name = '{inj2}'").fetchall())
rec("L12a", (n_concat, n_param, n2) == (2, 0, 2) and alg.sql_concat_vs_param(inj)[1:] == (2, 0), "chèn: 2 dòng / 0 dòng; quiz 2")
try:
    con.execute("SELECT name FROM users WHERE name = 'O'Brien'")
    e2 = None
except sqlite3.OperationalError:
    e2 = "OperationalError"
rec("L12b", e2 == "OperationalError" == alg.sql_concat_error("O'Brien")[0], "tên có dấu nháy làm hỏng câu ghép chuỗi")
buf = bytearray(8) + bytearray([0]) + bytearray(8)
src = b"AAAAAAAAB\x00"
buf[0:len(src)] = src
rec("L12c", buf[8] == ord("B") == 66 == alg.overflow_sim("AAAAAAAAB")[0] and len(b"AAAAAAAAAAAA\x00") - 8 == 5, "tràn: cờ = 66; quiz 5 byte")
con.close()

# ── L13 (hành trình kho mã chung): đếm từng phút / từng phần / chia đôi mô phỏng, không gõ sẵn kết quả ──
per_day = sum(20 for _minute in range(24 * 60))                       # [ET11] “20+ changes per minute”
deps = {"thư viện chung": {"dự án A", "dự án B"}, "dự án A": {"dự án A"}, "dự án B": {"dự án B"}}
affected = {k: len(v) for k, v in deps.items()}                       # đồ thị minh hoạ: 2 bộ / 1 bộ
rec("L13a", per_day == 28800 and per_day // 24 // 60 == 20 and affected["thư viện chung"] == 2 and affected["dự án A"] == 1,
    f"chặng 1: 20 thay đổi/phút × 1440 phút = {per_day}; sửa thư viện chung → 2 bộ kiểm thử, sửa dự án A → 1")
sizes = [35000 // 3100 + (1 if i < 35000 % 3100 else 0) for i in range(3100)]  # chia đều 35 000 chỗ vào 3100 phần [CM13]
rec("L13b", sum(sizes) == 35000 and set(sizes) == {11, 12} and round(35000 / 3100, 1) == 11.3 and 45000 - 35000 == 10000
    and round(sum(2 for _ in range(3100)) / 60, 1) == 103.3,
    "chặng 2: 35 000 / 3100 ≈ 11,3 (mỗi phần 11 hoặc 12 chỗ); 10 000 chỗ còn lại; 3100 × 2 phút (minh hoạ) ≈ 103,3 giờ")
import random as _rnd
_g = _rnd.Random(13)
runs = [sum(_g.random() < 0.015 for _ in range(1000)) for _ in range(2000)]   # mô phỏng 1000 kiểm thử, 1,5% chập chờn [FT16]
mile = len(range(0, 24 * 60, 45))
rec("L13c", 1000 * 15 // 1000 == 15 and abs(sum(runs) / len(runs) - 15) < 0.5 and 15 * 3 == 45 and 24 * 60 // 45 == 32 and mile == 32,
    f"chặng 3: kỳ vọng 15 kiểm thử đỏ giả / 1000 (mô phỏng TB {sum(runs) / len(runs):.2f}); 15 phút × 3 lần = 45 phút; 32 mốc 45 phút / ngày")


def bisect_runs(n, bad):
    lo, hi, k = 0, n, 0                                                # tìm thay đổi gây lỗi trong lô bằng chia đôi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        k += 1
        if bad < mid:
            hi = mid
        else:
            lo = mid
    return k, lo


rec("L13d", 4 * 10 ** 9 // 50000 == 80000 and all(bisect_runs(16, b) == (4, b) for b in range(16))
    and all(bisect_runs(8, b) == (3, b) for b in range(8)) and round(15000 / 700, 1) == 21.4,
    "chặng 4: 4 tỉ / 50 000 = 80 000 ca mỗi thay đổi; lô 16 → đúng 4 lần chạy với mọi vị trí lỗi; lô 8 → 3; 15 000 / 700 ≈ 21,4 tệp")
rec("L13e", [1000 * p // 100 for p in (10, 20)] == [100, 200] and 12 // 6 == 2 and sum(2 for _ in range(40)) * 15 == 1200,
    "chặng 5 + quiz: 10–20% của 1000 = 100–200; 12/6 = 2 lần dựng lại mỗi năm; 40 người × 2 lần × 15 ngày = 1200 lần gộp")

n_ok = sum(o for _, o in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
