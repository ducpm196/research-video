"""Kiểm độc lập mọi khẳng định của khoá SDP — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Độ phức tạp vòng: đếm từ khoá bằng module tokenize (không dùng ast). Đọc số kiểu cũ: gọi atoi thật của thư viện C (msvcrt qua ctypes).
Lớp, mẫu: cài lại riêng ở đây. Đối tượng duy nhất: chạy hai TestCase thật bằng unittest theo hai thứ tự. Cây hợp thành: tạo thư mục thật
trên đĩa rồi cộng kích thước bằng os.walk. Ghi nhớ: functools.lru_cache.cache_info() và công thức 2·F(n+1) − 1. Tái cấu trúc: hạt giống
khác. Phiên bản: so thứ tự bằng packaging.version. Số tiền: Decimal / Fraction.
Chạy: .venv/Scripts/python audit/sdp/verify_sdp.py → PASS/FAIL từng dòng và tổng."""
import ctypes
import datetime
import functools
import io
import itertools
import math
import os
import random
import sys
import tempfile
import tokenize
import unittest
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path

import sympy as sp
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: độ phức tạp vòng đếm bằng tokenize ──
def mccabe_tok(src):
    kw = {"if", "elif", "for", "while", "except", "and", "or"}
    toks = [t.string for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type == tokenize.NAME]
    return 1 + sum(1 for t in toks if t in kw)


SRC0 = "def f(xs, lo, hi):\n    n = 0\n    if not xs:\n        return 0\n    for x in xs:\n        if x > lo and x < hi:\n            n += 1\n    return n\n"
SRCQ = "def g(x):\n    while x > 0:\n        x -= 1\n    if x == 0:\n        return 'a'\n    elif x < 0:\n        return 'b'\n    return 'c'\n"
rec("L00a", mccabe_tok(SRC0) == 5 == alg.mccabe(SRC0), "dem_trong_khoang: M = 5 (tokenize)")
rec("L00b", mccabe_tok(SRCQ) == 4 == alg.mccabe(SRCQ) and mccabe_tok("def h(a, b):\n    return a + b\n") == 1, "quiz M = 4; hàm không rẽ M = 1")

# ── L01: atoi thật của thư viện C ──
atoi = ctypes.cdll.msvcrt.atoi
rec("L01a", [atoi(s) for s in (b"12a", b"abc", b"0", b"3x5", b"x")] == [12, 0, 0, 3, 0]
    == [alg.parse_prefix(s.decode()) for s in (b"12a", b"abc", b"0", b"3x5", b"x")], "atoi: 12a→12, abc→0, 0→0, 3x5→3, x→0")
bad = []
for s in ("12a", "3x5", ""):
    try:
        int(s)
    except ValueError:
        bad.append(s)
rec("L01b", bad == ["12a", "3x5", ""] and int(" 7 ") == 7 and alg.int_or_error("12a") == "ValueError", "int() báo ValueError ngay")


# ── L02: tài khoản cài lại ──
class TK:
    def __init__(self, s):
        assert s >= 0
        self._s = s

    def nap(self, x):
        if x <= 0:
            raise ValueError
        self._s += x

    def rut(self, x):
        if x <= 0 or x > self._s:
            raise ValueError
        self._s -= x


def run_ops(start, ops):
    t, rej = TK(start), []
    for op, x in ops:
        try:
            getattr(t, op)(x)
        except ValueError:
            rej.append((op, x))
    return t._s, rej


rec("L02a", run_ops(100, [("rut", 150)]) == (100, [("rut", 150)]) and run_ops(200, [("nap", 50), ("rut", 100)])[0] == 150 and alg.account_demo() == ("ValueError", -50),
    "rút 150 từ 100 bị từ chối; 200 + 50 − 100 = 150; lớp lộ trường cho −50")
rec("L02b", run_ops(40, [("nap", 30), ("rut", 80), ("rut", 50)]) == (20, [("rut", 80)]), "quiz: rút 80 bị từ chối, còn 20")

# ── L03: diện tích chính xác bằng sympy ──
rec("L03a", sp.simplify(3 * 4 + sp.pi * 1 ** 2 + sp.Rational(6 * 2, 2) - (18 + sp.pi)) == 0 and round(float(18 + sp.pi), 2) == 21.14
    and abs(alg.total_area([alg.Rect(3, 4), alg.Circle(1), alg.Triangle(6, 2)]) - float(18 + sp.pi)) < 1e-12, "18 + π ≈ 21,14")
rec("L03b", round(float(10 + 4 * sp.pi + 6), 2) == 28.57 == round(alg.total_area([alg.Rect(2, 5), alg.Circle(2), alg.Triangle(4, 3)]), 2), "16 + 4π ≈ 28,57")

# ── L04: liệt kê tổ hợp bằng itertools ──
n48 = len(list(itertools.product(range(3), *[(0, 1)] * 4)))
n128 = len(list(itertools.product(range(4), *[(0, 1)] * 5)))
rec("L04a", (n48, 3 + 4, n128, 4 + 5) == (48, 7, 128, 9) == alg.coffee_classes(3, 4) + alg.coffee_classes(4, 5), "48 vs 7 lớp; 128 vs 9 lớp")
rec("L04b", sum([30, 5, 2]) == 37 == alg.AddOn(alg.AddOn(alg.Coffee(), 5), 2).cost() and sum([30, 5, 5, 8]) == 48, "giá 37; quiz 48")


# ── L05: Decimal ──
def d_round(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


v1 = d_round(Decimal(200000) * Decimal("1.1"))
v2 = d_round(Decimal(200000) * Decimal("1.1") * Decimal("0.95"))
v3 = d_round(Decimal(300000) * Decimal("1.1") * Decimal("0.8"))
rec("L05a", (v1, v2, v3) == (220000, 209000, 264000) == (alg.invoice(200000, [alg.Tax(0.1)]), alg.invoice(200000, [alg.Tax(0.1), alg.Discount(0.05)]),
                                                         alg.invoice(300000, [alg.Tax(0.1), alg.Discount(0.2)])), "220 000; 209 000; quiz 264 000")


# ── L06: chữ nhật / vuông cài lại ──
class CN:
    def __init__(self):
        self.w = self.h = 0

    def dat_rong(self, w):
        self.w = w

    def dat_cao(self, h):
        self.h = h


class Vg(CN):
    def dat_rong(self, w):
        self.w = self.h = w

    def dat_cao(self, h):
        self.w = self.h = h


def area_after(cls, w, h):
    o = cls()
    o.dat_rong(w)
    o.dat_cao(h)
    return o.w * o.h


rec("L06a", (area_after(CN, 5, 4), area_after(Vg, 5, 4)) == (20, 16) == (alg.lsp_demo(alg.Rectangle), alg.lsp_demo(alg.Square)), "5·4 = 20 nhưng vuông cho 16")
rec("L06b", (area_after(CN, 7, 3), area_after(Vg, 7, 3)) == (21, 9), "quiz: 21 và 9")


# ── L07: tiêm ngày ──
def chao(d):
    return "Chúc mừng năm mới" if d.strftime("%m-%d") == "01-01" else "Xin chào"


days = [datetime.date(2025, 1, 1), datetime.date(2025, 6, 15), datetime.date(2024, 12, 31), datetime.date(2030, 1, 1)]
rec("L07a", [chao(d) for d in days] == [alg.greeting(d) for d in days] == ["Chúc mừng năm mới", "Xin chào", "Xin chào", "Chúc mừng năm mới"], "1/1 → chúc mừng; ngày khác → xin chào")


# ── L08: hai TestCase thật dùng chung một đối tượng duy nhất ──
class _Dem:
    _i = None

    def __new__(cls):
        if cls._i is None:
            cls._i = super().__new__(cls)
            cls._i.n = 0
        return cls._i


class TA(unittest.TestCase):
    def test_a(self):
        c = _Dem()
        c.n += 1
        self.assertEqual(c.n, 1)


class TB(unittest.TestCase):
    def test_b(self):
        c = _Dem()
        c.n += 2


def run_order(order):
    _Dem._i = None
    suite = unittest.TestSuite([TA("test_a") if x == "A" else TB("test_b") for x in order])
    res = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    return res.wasSuccessful(), _Dem._i.n


rec("L08a", run_order("AB") == (True, 3) and run_order("BA") == (False, 3) and alg.singleton_order("A") and not alg.singleton_order("B"),
    "unittest: A rồi B đạt; B rồi A trượt (A thấy 3)")

# ── L09: độ F → độ C bằng phân số; cây thư mục thật trên đĩa ──
rec("L09a", Fraction("98.6") - 32 == Fraction(333, 5) and (Fraction("98.6") - 32) * Fraction(5, 9) == 37 and (Fraction(212) - 32) * Fraction(5, 9) == 100
    and alg.CelsiusAdapter(alg.FahrenheitSensor()).read_c() == 37.0, "98,6 °F = 37 °C đúng tuyệt đối; 212 °F = 100 °C")
with tempfile.TemporaryDirectory() as td:
    def mk(rel, size):
        p = Path(td, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"\0" * size)
    for rel, sz in (("g/a", 120), ("g/b", 30), ("g/c/d", 50), ("g/c/e", 20), ("q/a", 10), ("q/s/b", 5), ("q/s/t/c", 3), ("q/s/t/d", 2)):
        mk(rel, sz)

    def walk(top):
        return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(os.path.join(td, top)) for f in fs)
    rec("L09b", (walk("g"), walk("q")) == (220, 20) == (alg.Folder(alg.File(120), alg.File(30), alg.Folder(alg.File(50), alg.File(20))).size(),
                                                        alg.Folder(alg.File(10), alg.Folder(alg.File(5), alg.Folder(alg.File(3), alg.File(2)))).size()),
        "os.walk trên thư mục thật: 220 và 20")

# ── L10: lệnh có hoàn tác; người nghe ──
hist, x = [], 10
for do, undo in ((lambda v: v + 5, lambda v: v - 5), (lambda v: v * 2, lambda v: v / 2), (lambda v: v - 3, lambda v: v + 3)):
    x = do(x)
    hist.append(undo)
after = x
u1 = hist.pop()(x)
u2 = hist.pop()(u1)
calls = []
subs = [calls.append for _ in range(3)]
for ev in range(4):
    for s in subs:
        s(ev)
rec("L10a", (after, u1, u2) == (27, 30, 15) == alg.command_demo() and len(calls) == 12 == alg.observer_calls(3, 4), "27 → 30 → 15; 3 · 4 = 12 lời gọi")
rec("L10b", alg.observer_calls(5, 6) == 30 and (6 * 3 + 4) - 4 == 18 and 7 // 2 * 2 == 6 != 7, "quiz 30 và 18; chia nguyên 7 không hoàn tác được")

# ── L11: bảng chuyển, sửa danh sách khi đang duyệt ──
S3 = ["MỚI", "ĐÃ TRẢ", "ĐÃ GIAO"]
fwd = {("MỚI", "ĐÃ TRẢ"), ("ĐÃ TRẢ", "ĐÃ GIAO")}
rec("L11a", len(list(itertools.product(S3, S3))) == 9 and {(s, v) for (s, e), v in alg.ORDER_FLOW.items() if v in S3} == fwd
    and alg.order_state(["trả tiền", "giao", "huỷ"])[1] == [("ĐÃ GIAO", "huỷ")], "9 cặp, 2 chuyển tiến hợp lệ; huỷ sau khi giao bị từ chối")
rec("L11b", alg.order_state(["giao", "trả tiền", "huỷ"]) == ("ĐÃ HUỶ", [("MỚI", "giao")]), "quiz: giao khi MỚI bị từ chối, cuối ĐÃ HUỶ")
xs, ys = [1, 2, 2, 3], [2, 4, 6, 7]
for v in xs:
    if v % 2 == 0:
        xs.remove(v)
for v in ys:
    if v % 2 == 0:
        ys.remove(v)
rec("L11c", (xs, ys) == ([1, 2, 3], [4, 7]), "xoá khi đang duyệt: [1, 2, 3] và [4, 7]")


# ── L12: lru_cache.cache_info và công thức số lời gọi ──
def fibn(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@functools.lru_cache(maxsize=None)
def fm(n):
    return n if n < 2 else fm(n - 1) + fm(n - 2)


fm(30)
ci30 = fm.cache_info()
fm.cache_clear()
fm(20)
ci20 = fm.cache_info()
rec("L12a", 2 * fibn(31) - 1 == 2692537 == alg.fib_calls(30, False)[1] and fibn(30) == 832040, "ngây thơ: 2·F(31) − 1 = 2 692 537 lời gọi")
rec("L12b", (ci30.misses, ci30.hits, ci30.misses + ci30.hits) == (31, 28, 59) and alg.fib_calls(30, True)[1:] == (59, 31), "lru_cache: 31 lần tính + 28 lần tra = 59 lời gọi")
rec("L12c", (ci20.misses, ci20.hits) == (21, 18) and 2 * fibn(21) - 1 == 21891 and fibn(29) == 514229, "quiz: 21 lần tính, 18 lần tra; f(2) bị gọi F(29) = 514 229 lần")


# ── L13: tái cấu trúc, hạt giống khác ──
def fee_ref(t, k):
    ship = 0 if t >= 500000 else 15000 + max(0, k - 5) * 4000
    return round(t * 1.1 + ship)


rr = random.Random(2026)
pairs = [(rr.randrange(0, 1000001, 1000), rr.randrange(0, 31)) for _ in range(10000)]
rec("L13a", all(alg.fee_old(t, k) == alg.fee_new(t, k) == fee_ref(t, k) for t, k in pairs) and alg.refactor_check(10000, 1), "bản cũ = bản mới trên 10 000 cặp (2 hạt giống)")
rec("L13b", (fee_ref(300000, 2), fee_ref(300000, 8), fee_ref(600000, 12), fee_ref(200000, 3), fee_ref(450000, 10)) == (345000, 357000, 660000, 235000, 530000)
    and round(300000 * 1.1 + 15000 + (2 - 5) * 4000) == 333000, "345 000 vs bản lỗi 333 000; 357 000; quiz 235 000, 530 000")

# ── L14: phiên bản ngữ nghĩa ──
nv = [alg.semver_bump("1.4.2", c) for c in ("sửa lỗi", "thêm tương thích", "phá vỡ")]
rec("L14a", nv == ["1.4.3", "1.5.0", "2.0.0"] and Version("1.4.2") < Version(nv[0]) < Version(nv[1]) < Version(nv[2]), "1.4.3 < 1.5.0 < 2.0.0")
rec("L14b", alg.semver_bump("3.9.7", "thêm tương thích") == "3.10.0" and Version("3.10.0") > Version("3.9.7") and alg.semver_bump("3.10.0", "phá vỡ") == "4.0.0",
    "quiz: 3.10.0 (lớn hơn 3.9.7), rồi 4.0.0")

# ── L15: độ bất ổn ──
rec("L15a", Fraction(1, 3 + 1) == Fraction(1, 4) and alg.instability(3, 1) == 0.25 and (alg.instability(0, 4), alg.instability(5, 0)) == (1.0, 0.0), "I = 1/4; biên 1 và 0")
rec("L15b", (Fraction(3, 4), Fraction(2, 4)) == (Fraction(alg.instability(1, 3)), Fraction(alg.instability(2, 2))) and Fraction(3, 4) > Fraction(1, 4), "quiz 0,75 và 0,5; đúng chiều")

# ── L16: giỏ hàng ──
d10 = lambda t: int(Decimal(t) * Decimal("0.9")) if t > 300000 else t  # noqa: E731
rec("L16a", (d10(450000), d10(250000), d10(350000), 350000 - 50000) == (405000, 250000, 315000, 300000)
    == (alg.cart_total([150000, 200000, 100000], lambda t: round(t * 0.9) if t > 300000 else t), alg.cart_total([100000, 150000], lambda t: round(t * 0.9) if t > 300000 else t),
        alg.cart_total([120000, 90000, 140000], lambda t: round(t * 0.9) if t > 300000 else t), alg.cart_total([120000, 90000, 140000], lambda t: t - 50000 if t >= 200000 else t)),
    "405 000; 250 000 giữ nguyên; quiz 315 000 và 300 000")

# ── L17 (hành trình nguyên khối mô-đun hoá): đếm trên đồ thị dựng thật / liệt kê tháng, không gõ sẵn kết quả ──
pairs10 = [(a, b) for a in range(10) for b in range(10) if a != b]               # 10 miền không tường (số minh hoạ)
dense = {u: [v for v in range(37) if v != u][:36 // 2 + 1] for u in range(37)}  # mỗi thành phần dựa vào “hơn nửa” 36 cái kia
n_edges = sum(len(vs) for vs in dense.values())
months = [(y, m) for y in range(2020, 2025) for m in range(1, 13) if (2020, 9) <= (y, m) < (2024, 1)]
rec("L17a", len(pairs10) == 90 and 2016 - 2006 == 10 and Fraction(6000 * 1, 60) == 100 and Fraction(100, 8) == Fraction(25, 2),
    "90 chiều gọi; 10 năm; 6000 lớp × 1 phút = 100 giờ = 12,5 ngày công")
rec("L17b", all(len(vs) * 2 > 36 for vs in dense.values()) and min(len(vs) for vs in dense.values()) == 19 and n_edges == 703
    and len([(u, v) for u in range(37) for v in range(37) if u != v]) == 1332 and round(n_edges / 1332, 2) == 0.53,
    "cận dưới 19 mỗi thành phần, 703 mũi tên trên tối đa 1332 (≈ 0,53)")
rec("L17c", len(range(0, 480, 5)) == 96 and 480 // 61 < 8 <= 480 // 60 and len(months) == 40 and round(37 / 3) == 12,
    "ngày 480 phút: 96 lần quét 5 phút, quét hơn 1 giờ ≤ 8 lần; 9/2020 → 1/2024 = 40 tháng; một phần ba của 37 ≈ 12")
rec("L17d", (alg.instability(36, 0), alg.instability(7, 0), alg.instability(0, 2)) == (0.0, 0.0, 1.0) and alg.instability(0, 2) > alg.instability(7, 0)
    and len([(a, b) for a in range(8) for b in range(8) if a != b]) == 56,
    "cửa hàng I = 0, thông báo I = 1: gọi thẳng cửa hàng → thông báo đi ngược chiều ổn định; 8 dịch vụ → 56 chiều gọi")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
