"""Kiểm chứng bằng máy mọi ví dụ có con số trong giáo án kế hoạch (curriculum/{dms,csa,osy,net,toc,rbm,swf,dbs,dsc,dsy,esy,cld,mlo}.yaml), TRƯỚC khi
soạn đặc tả bài. Mỗi mục: mã khoá:bài, PASS/FAIL, số liệu. Giáo án chỉ được ghi con số đã PASS ở đây.
Chạy: .venv/Scripts/python audit/verify_plan_curricula.py"""
import itertools
import math
import struct
import sys
from fractions import Fraction as F

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
rows = []


def rec(cid, ok, msg):
    rows.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} | {cid:9} | {msg}")


# ═══════════ DMS — Toán rời rạc ═══════════
TF = [True, False]
rec("DMS:L00", all((not p or q) == (not p or q) for p in TF for q in TF) and [(not p) or q for p in TF for q in TF] == [True, False, True, True],
    "p→q ≡ ¬p∨q; bảng chân trị (Đ,Đ),(Đ,S),(S,Đ),(S,S) → Đ,S,Đ,Đ: kéo theo đúng khi p sai")
rec("DMS:L01", all((not (p and q)) == ((not p) or (not q)) and (not (p or q)) == ((not p) and (not q)) for p in TF for q in TF), "De Morgan, cả 4 dòng")
rec("DMS:L02", all(x * x >= x for x in range(0, 10**4)) and any(x * x < x for x in [F(1, 2)]),
    "∀x∈ℕ: x² ≥ x đúng (kiểm 0..9999); trên ℚ thì sai: x = 1/2 cho 1/4 < 1/2 — phủ định ∀ là ∃¬")
rec("DMS:L04", all(sum(2 * k - 1 for k in range(1, n + 1)) == n * n for n in range(1, 200)), "1 + 3 + … + (2n − 1) = n² (n = 1..199)")
rec("DMS:L05", len(list(itertools.chain.from_iterable(itertools.combinations("abc", r) for r in range(4)))) == 8
    and sum(1 for x in range(1, 101) if x % 2 == 0 or x % 3 == 0) == 50 + 33 - 16 == 67,
    "|P({a,b,c})| = 8; số từ 1..100 chia hết cho 2 hoặc 3: 50 + 33 − 16 = 67")
rec("DMS:L06", 367 > 366 and 11 > 10, "367 người, 366 ngày (năm nhuận) → chắc chắn 2 người trùng sinh nhật; 11 khoá vào 10 ô băm → chắc chắn va chạm")
cls = {}
for x in range(9):
    cls.setdefault(x % 3, []).append(x)
rec("DMS:L07", cls == {0: [0, 3, 6], 1: [1, 4, 7], 2: [2, 5, 8]}, "đồng dư mod 3 trên {0..8}: 3 lớp tương đương, mỗi lớp 3 phần tử")
S = [1, 2, 3, 4, 6, 12]
cover = [(a, b) for a in S for b in S if a != b and b % a == 0 and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in S)]
rec("DMS:L08", len(cover) == 7, f"quan hệ chia hết trên {{1,2,3,4,6,12}}: biểu đồ Hasse có {len(cover)} cạnh {cover}")
rec("DMS:L09", 26 ** 8 == 208827064576, "mật khẩu 8 chữ thường: 26⁸ = 208 827 064 576")
rec("DMS:L10", math.comb(10, 3) == 120 and [math.comb(4, k) for k in range(5)] == [1, 4, 6, 4, 1] and sum(math.comb(7, k) for k in range(8)) == 2 ** 7,
    "C(10,3) = 120; hệ số (x+y)⁴: 1 4 6 4 1; Σ C(n,k) = 2ⁿ")
rec("DMS:L11", sum(1 for a in range(11) for b in range(11 - a)) == math.comb(12, 2) == 66, "x₁ + x₂ + x₃ = 10, xᵢ ≥ 0: C(12, 2) = 66 nghiệm (vét cạn)")
der = lambda n: sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))
rec("DMS:L12", der(4) == 9 and abs(sum((-1) ** k / math.factorial(k) for k in range(11)) - 1 / math.e) < 1e-7,
    f"hoán vị không điểm cố định D₄ = {der(4)}; D₁₀/10! ≈ {sum((-1) ** k / math.factorial(k) for k in range(11)):.5f} ≈ 1/e")
rec("DMS:L13", math.gcd(252, 198) == 18 and 252 * 4 - 198 * 5 == 18, "gcd(252, 198) = 18 = 252·4 − 198·5 (Euclid mở rộng)")
rec("DMS:L14", (3 * 5) % 7 == 1 and pow(3, 100, 7) == 4 and 100 % 6 == 4 and 3 ** 4 % 7 == 4,
    "3⁻¹ ≡ 5 (mod 7); 3¹⁰⁰ ≡ 3⁴ = 81 ≡ 4 (mod 7) theo Fermat nhỏ (3⁶ ≡ 1)")
n_, phi, e_, d_ = 33, 20, 3, 7
rec("DMS:L15", (e_ * d_) % phi == 1 and pow(4, 3, 33) == 31 and pow(31, 7, 33) == 4,
    "RSA đồ chơi: p = 3, q = 11, n = 33, φ = 20, e = 3, d = 7; mã hoá 4 → 4³ mod 33 = 31; giải 31⁷ mod 33 = 4")
rec("DMS:L16", sum([3, 3, 3, 5]) == 2 * 7 and all(d % 2 == 1 for d in [3, 3, 3, 5]),
    "Königsberg: bậc 3, 3, 3, 5 — tổng 14 = 2·7 cầu; 4 đỉnh bậc lẻ → không có chu trình Euler")
# Cayley: số cây có nhãn trên 4 đỉnh = 16 (vét cạn)
K4 = list(itertools.combinations(range(4), 2))
def is_tree(es, n=4):
    p = list(range(n))
    def f(x):
        while p[x] != x:
            x = p[x]
        return x
    for u, v in es:
        a, b = f(u), f(v)
        if a == b:
            return False
        p[a] = b
    return True
rec("DMS:L17", sum(1 for es in itertools.combinations(K4, 3) if is_tree(es)) == 4 ** 2 == 16, "Cayley: 4 đỉnh có nhãn → 4² = 16 cây (vét cạn)")
rec("DMS:L18", 4 - 6 + 4 == 2 and 10 > 3 * 5 - 6, "K₄ phẳng: V − E + F = 4 − 6 + 4 = 2; K₅: E = 10 > 3V − 6 = 9 → không phẳng")
p23 = 1 - math.prod((365 - k) / 365 for k in range(23))
rec("DMS:L19", round(p23, 4) == 0.5073, f"nghịch lý ngày sinh: 23 người, P(trùng) = {p23:.4f}")
rec("DMS:L20", round(2 ** (80 - 63.1)) == 122295 and 2 ** 63 == 9223372036854775808 and 2017 - 2006 == 11
    and round(math.comb(10000, 2) / 2 ** 32, 4) == 0.0116 and 2030 - 2022 == 8,
    "SHA-1: 2⁸⁰ / 2^63,1 = 2^16,9 ≈ 122 295 lần (> 100 000, ST17); 2⁶³ = 9 223 372 036 854 775 808 (GB17); 2017 − 2006 = 11 năm; "
    "C(10 000, 2) / 2³² ≈ 0,0116 cặp trùng (số minh hoạ); 2030 − 2022 = 8 năm (NI22)")

# ═══════════ CS115 — bài hành trình L45 (2026-11-02; các bài L00–L44 kiểm ở audit/verify_cs115_*.py) ═══════════
def _cs115_l45_reddi(ams, T=3000, C=3, eta=0.5):   # RK18 §3: β₁ = 0, β₂ = 1/(1 + C²), chiếu về [−1, 1], η_t = η/√t
    b2, v, vh, x = 1 / (1 + C * C), 0.0, 0.0, 0.0
    for t in range(1, T + 1):
        g = C if t % 3 == 1 else -1
        v = b2 * v + (1 - b2) * g * g
        vh = max(vh, v)
        x = max(-1.0, min(1.0, x - eta / math.sqrt(t) * g / math.sqrt(vh if ams else v)))
    return x
rec("CS115:L45", round(1 - 0.999 ** 1000, 3) == 0.632 and round((0.001 * 1e-4 / 0.1) / (0.001 * 1e-4 / 10)) == 100
    and _cs115_l45_reddi(False) == 1.0 and _cs115_l45_reddi(True) < -0.99
    and (__import__("datetime").date(2019, 8, 8) - __import__("datetime").date(2017, 11, 14)).days == 632,
    "1 − 0,999¹⁰⁰⁰ ≈ 0,632; phạt L2 qua phép chia lệch 100 lần (√ŝ = 10 và 0,1); ví dụ RK18 C = 3: Adam → +1, biến thể max → −1; "
    "14/11/2017 → 8/8/2019 = 632 ngày")

# ═══════════ CSA — Hệ thống máy tính ═══════════
rec("CSA:L00", 0x2F == 47 == 0b101111, "0x2F = 47 = 0b101111")
rec("CSA:L01", (-5) & 0xFF == 0b11111011 and ((127 + 1 + 128) % 256) - 128 == -128, "−5 trên 8 bit: 11111011; 127 + 1 tràn thành −128")
rec("CSA:L02", (12 & 11) == 8 and all((x & (x - 1) == 0) == (x & -x == x) for x in range(1, 4096)) and (13 << 3) == 104,
    "x & (x − 1) xoá bit 1 thấp nhất: 12 → 8; x là lũy thừa của 2 ⇔ x & (x − 1) = 0; 13 << 3 = 104 = 13·8")
rec("CSA:L03", 0.1 + 0.2 != 0.3 and repr(0.1 + 0.2) == "0.30000000000000004" and struct.pack(">f", 1.0).hex() == "3f800000",
    "0.1 + 0.2 = 0.30000000000000004 ≠ 0.3; float32 của 1,0 = 0x3F800000")
rec("CSA:L04", np.finfo(np.float64).eps == 2.0 ** -52 and (1e16 + 1) - 1e16 == 0.0, "ε máy (double) = 2⁻⁵² ≈ 2,22·10⁻¹⁶; (10¹⁶ + 1) − 10¹⁶ = 0")
rec("CSA:L05", [(a ^ b, a & b) for a in (0, 1) for b in (0, 1)] == [(0, 0), (1, 0), (1, 0), (0, 1)], "bộ cộng bán phần: tổng = a XOR b, nhớ = a AND b")
s4 = (7 + 5) & 0xF
rec("CSA:L06", s4 == 0b1100 and (s4 - 16 if s4 >= 8 else s4) == -4, "0111 + 0101 = 1100: không dấu 12, có dấu (bù 2, 4 bit) −4 → tràn có dấu")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "tools"))
import checklib as _cl
_r7, _n7, _t7 = _cl.run_asm(_cl.SUM_1_TO_10)
rec("CSA:L07", _r7["r1"] == 55 and _n7 == 33 == 3 + 10 * 3, f"vòng lặp cộng 1..10 trên máy ảo RISC tí hon: r1 = {_r7['r1']}, chạy {_n7} lệnh = 3 khởi tạo + 10 vòng × 3")
rec("CSA:L08", 1e9 * 1.5 / 2e9 == 0.75, "thời gian CPU = số lệnh · CPI / tần số = 10⁹ · 1,5 / 2·10⁹ = 0,75 s")
rec("CSA:L09", 100 + 5 - 1 == 104 and round(100 * 5 / 104, 2) == 4.81, "đường ống 5 tầng, 100 lệnh: 104 chu kỳ (so với 500) → nhanh 4,81 lần")
rec("CSA:L10", 1 + 0.05 * 100 == 6, "AMAT = 1 + 0,05·100 = 6 chu kỳ")
rec("CSA:L11", 32 * 1024 // 64 == 512 and int(math.log2(64)) == 6 and int(math.log2(512)) == 9 and 32 - 6 - 9 == 17,
    "cache 32 KiB, dòng 64 B: 512 dòng; địa chỉ 32 bit = 17 bit thẻ + 9 bit chỉ số + 6 bit độ dời")
def cache_sim(trace, sets, ways):
    c = [[] for _ in range(sets)]; hits = 0
    for a in trace:
        s = c[a % sets]
        if a in s:
            hits += 1; s.remove(a)
        elif len(s) == ways:
            s.pop(0)
        s.append(a)
    return hits
tr = [0, 4, 0, 4, 8, 0, 4]
rec("CSA:L12", cache_sim(tr, 4, 1) == 0 and cache_sim(tr, 2, 2) == 2,
    f"dãy khối {tr}: ánh xạ trực tiếp 4 dòng → 0 lần trúng (0, 4, 8 tranh cùng dòng); 2 tập × 2 đường, LRU → 2 lần trúng (0 và 4 cùng ở lại tới khi 8 đẩy 0 ra)")
rec("CSA:L13", round(1 / (0.1 + 0.9 / 8), 2) == 4.71 and round(1 / 0.1) == 10, "Amdahl: 90% song song được, 8 lõi → 4,71 lần; tối đa 10 lần")
rec("CSA:L14", 2 ** 32 // 4096 == 2 ** 20 and round(0.98 * (1 + 100) + 0.02 * (1 + 200), 2) == 103.0,
    "địa chỉ ảo 32 bit, trang 4 KiB: 2²⁰ mục bảng trang; TLB trúng 98% (1 ns), bộ nhớ 100 ns: EAT = 103 ns")
rec("CSA:L15", 1000 * 2e-6 == 0.002, "1000 ngắt/giây × 2 µs = 0,2% thời gian CPU")
_t16 = lambda f: 1e9 * 1.5 / f  # bài 8: T = N · CPI / f, N = 10⁹, CPI = 1,5
_s16 = lambda p, n: 1 / ((1 - p) + p / n)  # bài 13: Amdahl
rec("CSA:L16", _t16(2e9) == 0.75 and round(_t16(3.73e9), 2) == 0.40 and round(_t16(1e10), 2) == 0.15 and round(_s16(0.9, 2), 2) == 1.82
    and round(_s16(0.9, 100), 2) == 9.17 and sum(200 for k in range(100) if k >= 95) / 100 == 10 and min(200 * 4, 192) == 192 > 188
    and round(60 / _s16(0.8, 8), 1) == 18.0 and round(60 / _s16(0.2, 8), 1) == 49.5,
    "10⁹ lệnh, CPI 1,5: 2 GHz → 0,75 s; 3,73 GHz → 0,40 s (xu hướng 10 GHz → 0,15 s); Amdahl 90%: 2 lõi 1,82, 100 lõi 9,17; "
    "đoán đúng 95%, sai mất 200 chu kỳ → TB 10; 200 · 4 = 800 > 192 chỗ ROB, thí nghiệm 188 < 192; quiz 60 s, 80%/20% song song, 8 lõi → 18 s / 49,5 s")

# ═══════════ OSY — Hệ điều hành ═══════════
rec("OSY:L00", 1000 * 5e-6 == 0.005, "1000 lần chuyển ngữ cảnh/giây × 5 µs = 0,5% CPU")
rec("OSY:L01", 2 ** 3 == 8, "fork() 3 lần trong vòng lặp → 2³ = 8 tiến trình (kể cả tiến trình gốc)")
def waits(bursts):
    t, w = 0, []
    for b in bursts:
        w.append(t); t += b
    return w
rec("OSY:L02", sum(waits([24, 3, 3])) / 3 == 17 and sum(waits(sorted([24, 3, 3]))) / 3 == 3,
    "FCFS (24, 3, 3): chờ TB 17; SJF: 3")
def rr(bursts, q):
    rem, t, fin, queue = list(bursts), 0, [0] * len(bursts), list(range(len(bursts)))
    while queue:
        i = queue.pop(0); run = min(q, rem[i]); t += run; rem[i] -= run
        if rem[i]:
            queue.append(i)
        else:
            fin[i] = t
    return [fin[i] - bursts[i] for i in range(len(bursts))]
w = rr([24, 3, 3], 4)
rec("OSY:L03", w == [6, 4, 7] and round(sum(w) / 3, 2) == 5.67, f"Round Robin q = 4: chờ {w}, TB 17/3 ≈ 5,67")
# x++ = đọc, cộng, ghi; hai luồng, mỗi luồng 2 lần → các giá trị cuối có thể
def interleavings(a, b):
    if not a: yield list(b); return
    if not b: yield list(a); return
    for r in interleavings(a[1:], b): yield [a[0]] + r
    for r in interleavings(a, b[1:]): yield [b[0]] + r
ops = lambda t: [(t, k) for k in ("load", "add", "store") * 2]
finals = set()
for seq in interleavings(ops("A"), ops("B")):
    x, reg = 0, {"A": 0, "B": 0}
    for t, k in seq:
        if k == "load": reg[t] = x
        elif k == "add": reg[t] += 1
        else: x = reg[t]
    finals.add(x)
rec("OSY:L04", finals == {2, 3, 4}, f"hai luồng, mỗi luồng x++ hai lần (đọc–cộng–ghi), mọi cách xen kẽ: x cuối ∈ {sorted(finals)}, không chỉ 4")
alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
mx = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
avail = [3, 3, 2]
need = [[m - a for m, a in zip(mx[i], alloc[i])] for i in range(5)]
work, done, seq = avail[:], [False] * 5, []
while len(seq) < 5:
    for i in range(5):
        if not done[i] and all(n <= w_ for n, w_ in zip(need[i], work)):
            work = [w_ + a for w_, a in zip(work, alloc[i])]; done[i] = True; seq.append(i); break
    else:
        break
rec("OSY:L07", seq == [1, 3, 0, 2, 4] and sum(alloc[i][0] for i in range(5)) + 3 == 10,
    f"nhà băng (5 tiến trình, tài nguyên 10, 5, 7; còn rảnh 3, 3, 2): an toàn, một thứ tự an toàn P{seq}")
holes, req = [100, 500, 200, 300, 600], [212, 417, 112, 426]
def fit(holes, req, pick):
    h = holes[:]; out = []
    for r in req:
        c = [i for i in range(len(h)) if h[i] >= r]
        if not c: out.append(None); continue
        i = pick(c, h); out.append(i); h[i] -= r
    return out
ff = fit(holes, req, lambda c, h: c[0]); bf = fit(holes, req, lambda c, h: min(c, key=lambda i: h[i]))
rec("OSY:L08", ff == [1, 4, 1, None] and bf == [3, 1, 2, 4],
    f"lỗ trống {holes}, yêu cầu {req}: vừa đầu tiên {ff} (426 KB không chỗ); vừa nhất {bf} (đủ chỗ cho cả 4)")
rec("OSY:L09", (0x3A7F >> 12, 0x3A7F & 0xFFF) == (3, 0xA7F), "trang 4 KiB: địa chỉ 0x3A7F → trang 3, độ dời 0xA7F")
ref = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
def faults(ref, n, pol):
    mem, f = [], 0
    for i, p in enumerate(ref):
        if p in mem:
            if pol == "LRU": mem.remove(p); mem.append(p)
            continue
        f += 1
        if len(mem) == n:
            if pol == "OPT":
                fut = ref[i + 1:]
                v = max(mem, key=lambda q: fut.index(q) if q in fut else 10**9); mem.remove(v)
            else:
                mem.pop(0)
        mem.append(p)
    return f
fr = {(pol, n): faults(ref, n, pol) for pol in ("FIFO", "LRU", "OPT") for n in (3, 4)}
rec("OSY:L10", fr[("FIFO", 3)] == 9 and fr[("FIFO", 4)] == 10 and fr[("LRU", 3)] == 10 and fr[("OPT", 3)] == 7,
    f"chuỗi {ref}: {fr} — FIFO 3 khung 9 lỗi, 4 khung 10 lỗi (nghịch lý Belady)")
size = (12 + 1024 + 1024 ** 2 + 1024 ** 3) * 4096
rec("OSY:L12", round(size / 2 ** 40, 3) == 4.004, f"inode 12 trực tiếp + gián tiếp 1, 2, 3 tầng, khối 4 KiB, con trỏ 4 B: tối đa ≈ {size / 2**40:.3f} TiB")
q, head = [98, 183, 37, 122, 14, 124, 65, 67], 53
def fcfs(q, h): return sum(abs(b - a) for a, b in zip([h] + q, q))
def sstf(q, h):
    q = q[:]; t = 0
    while q:
        n = min(q, key=lambda x: abs(x - h)); t += abs(n - h); h = n; q.remove(n)
    return t
rec("OSY:L13", fcfs(q, head) == 640 and sstf(q, head) == 236, "đầu đọc ở 53, hàng đợi 98, 183, 37, 122, 14, 124, 65, 67: FCFS 640 trụ, SSTF 236 trụ")
rec("OSY:L14", int("750", 8) == 0b111101000, "quyền rwxr-x--- = 750 (bát phân)")


def _osy15_eevdf(sl, total):  # cài đặt độc lập với checklib: trễ hưởng = TB thời gian ảo − thời gian ảo; đủ điều kiện khi ≥ 0
    v, t, out = [0] * len(sl), 0, []
    while t < total:
        el = [k for k in range(len(sl)) if sum(v) / len(v) >= v[k]]
        i = sorted(el, key=lambda k: (v[k] + sl[k], k))[0]
        out.append(i); v[i] += sl[i]; t += sl[i]
    return out


def _osy15_share(weights, ms):  # luôn chạy tác vụ/nhóm có thời gian ảo (thời gian chạy · 1024 / trọng số) nhỏ nhất, 1 ms mỗi lượt
    run = [0] * len(weights)
    for _ in range(ms):
        i = sorted(range(len(weights)), key=lambda k: (run[k] * 1024 / weights[k], k))[0]; run[i] += 1
    return run


_o15 = _osy15_eevdf([9, 3], 36)
rec("OSY:L15", 1000 * 1000 == 10**6 and 7 / 8 == 0.875 and _osy15_share([1024, 1024], 40) == [20, 20] and _osy15_share([1024, 1024], 20) == [10, 10]
    and _osy15_share([2048, 1024], 30) == [20, 10] and _o15[0] == 1 and _o15.count(1) * 3 == _o15.count(0) * 9 == 18
    and _osy15_eevdf([9, 9], 18) == [0, 1] and round(8 * 2 / 3, 2) == 5.33 and (2024 - 2023) * 12 + 1 == 13,
    "1000 tiến trình × 1000 lần chọn/giây = 10⁶ lần xem; 7/8 = 87,5%; nhóm: người 1 (1 tác vụ) 20/40 = 50%, người 2 chia 20 → 25% + 25%;"
    " trọng số 2048/1024 → 20/10 ms trong 30 ms; hạn chót ảo lát 3 và 9 ms: A chạy trước, mỗi bên 18 ms trong 36 ms; 2/3 của 8 CPU ≈ 5,33")

# ═══════════ NET — Mạng máy tính ═══════════
rec("NET:L00", 1460 + 20 + 20 + 18 == 1518 and round(1460 / 1518, 3) == 0.962, "khung Ethernet đầy: 1460 dữ liệu + 20 TCP + 20 IP + 18 Ethernet = 1518 B, hiệu suất 96,2%")
rec("NET:L01", 1500 * 8 / 100e6 == 120e-6 and 1e6 / 2e8 == 0.005, "trễ truyền 1500 B ở 100 Mbps = 120 µs; trễ lan truyền 1000 km ở 2·10⁸ m/s = 5 ms")
rec("NET:L02", 100e6 * 0.05 / 8 == 625000, "tích băng thông–trễ: 100 Mbps × 50 ms = 625 000 B")
def crc(data, gen):
    d = [int(c) for c in data] + [0] * (len(gen) - 1); g = [int(c) for c in gen]
    for i in range(len(data)):
        if d[i]:
            for j in range(len(g)): d[i + j] ^= g[j]
    return "".join(map(str, d[-(len(gen) - 1):]))
rec("NET:L03", crc("11010011101100", "1011") == "100", "CRC: dữ liệu 11010011101100, đa thức sinh 1011 → phần dư 100")
rec("NET:L04", round(1 / (2 * math.e), 3) == 0.184 and round(1 / math.e, 3) == 0.368, "ALOHA thuần tối đa 1/(2e) ≈ 18,4%; ALOHA chia khe 1/e ≈ 36,8%")
rec("NET:L05", 2 ** (32 - 26) - 2 == 62 and 2 ** (26 - 24) == 4 and 64 - 1 == 63, "192.168.10.0/26: 4 mạng con của một /24, mỗi mạng 62 máy, quảng bá 192.168.10.63")
tbl = {("11001000000101110001", 20): "A", ("110010000001011100011", 21): "B"}
addr = "11001000000101110001100000000000"
best = max((k for k in tbl if addr.startswith(k[0])), key=lambda k: k[1])
rec("NET:L06", tbl[best] == "B", "khớp tiền tố dài nhất: địa chỉ khớp cả /20 (A) và /21 (B) → gửi theo B")
rec("NET:L10", round((8000 / 1e9) / (0.030 + 8000 / 1e9), 5) == 0.00027, "dừng–chờ: gói 8000 bit, 1 Gbps, RTT 30 ms → hiệu suất ≈ 0,00027")
cw, seq_ = 1, []
for _ in range(6):
    seq_.append(cw); cw = cw * 2 if cw < 16 else cw + 1
rec("NET:L11", seq_ == [1, 2, 4, 8, 16, 17], f"khởi động chậm tới ngưỡng 16 rồi tăng cộng: cửa sổ theo RTT {seq_}")
rec("NET:L12", 2 + 10 * 2 == 22, "trang 1 HTML + 10 đối tượng, HTTP không bền: 2 RTT mỗi đối tượng → 22 RTT (chưa kể truyền)")
p_, g_, a_, b_ = 23, 5, 6, 15
A_, B_ = pow(g_, a_, p_), pow(g_, b_, p_)
rec("NET:L13", (A_, B_, pow(B_, a_, p_), pow(A_, b_, p_)) == (8, 19, 2, 2), "Diffie–Hellman p = 23, g = 5, a = 6, b = 15: gửi 8 và 19, khoá chung 2")
rec("NET:L14", pow(4, 7, 33) == 16 and pow(16, 3, 33) == 4, "chữ ký RSA đồ chơi (n = 33, d = 7, e = 3): ký 4 → 16; kiểm 16³ mod 33 = 4")
rec("NET:L15", 32000 / 40 == 800 and 10e9 * 0.1 / 8 == 125e6 and round(9100 / 3.3) == 2758 and 1000 * 1500 * 8 / 10e6 == 1.2
    and min(10 * 1200, max(14720, 2 * 1200)) == 12000, "hành trình tắc nghẽn: 32 000/40 = 800; 10 tỉ bit/s × 100 ms = 125 MB; 9100/3,3 ≈ 2758; 1000 gói × 1500 B ở 10 triệu bit/s = 1,2 s; cửa sổ đầu QUIC gói 1200 B = 12 000 B")

# ═══════════ TOC — Lý thuyết tính toán ═══════════
rec("TOC:L00", sum(2 ** k for k in range(4)) == 15, "chuỗi nhị phân độ dài ≤ 3 (kể cả rỗng): 1 + 2 + 4 + 8 = 15")
def dfa3(s):
    r = 0
    for c in s: r = (2 * r + int(c)) % 3
    return r == 0
rec("TOC:L01", dfa3("110") and not dfa3("111") and all(dfa3(bin(n)[2:]) == (n % 3 == 0) for n in range(1, 2000)),
    "DFA 3 trạng thái (số dư) nhận số nhị phân chia hết cho 3: 110 (= 6) nhận, 111 (= 7) không; đúng với n = 1..1999")
# NFA “kết thúc bằng 01” → DFA bằng dựng tập con: đếm trạng thái tới được
nfa = {(0, "0"): {0, 1}, (0, "1"): {0}, (1, "1"): {2}}
start = frozenset({0}); seen, todo = {start}, [start]
while todo:
    S_ = todo.pop()
    for c in "01":
        T = frozenset(set().union(*[nfa.get((q, c), set()) for q in S_]))
        if T not in seen: seen.add(T); todo.append(T)
rec("TOC:L02", len(seen) == 3, f"NFA 3 trạng thái “kết thúc bằng 01” → dựng tập con được {len(seen)} trạng thái DFA tới được: {sorted(map(sorted, seen))}")
import re
rec("TOC:L03", all(bool(re.fullmatch("(0|1)*01", s)) == s.endswith("01") for n in range(9) for s in map("".join, itertools.product("01", repeat=n))),
    "(0|1)*01 khớp đúng các chuỗi kết thúc bằng 01 (mọi chuỗi độ dài ≤ 8)")
cat = lambda n: math.comb(2 * n, n) // (n + 1)
bal = sum(1 for s in itertools.product("()", repeat=6) if (lambda s: all(sum(1 if c == "(" else -1 for c in s[:i + 1]) >= 0 for i in range(6)) and s.count("(") == 3)(s))
rec("TOC:L06", bal == cat(3) == 5, "chuỗi ngoặc cân bằng độ dài 6: 5 = số Catalan C₃ (vét cạn)")
rec("TOC:L07", 1 + 2 * 3 == 7 and (1 + 2) * 3 == 9, "1 + 2 * 3: hai cây suy dẫn cho 7 và 9 → văn phạm mơ hồ; ưu tiên phép nhân chọn 7")
rec("TOC:L09", bin(0b1011 + 1) == "0b1100", "máy Turing cộng 1: 1011 → 1100 (đổi các 1 cuối thành 0, rồi 0 đầu tiên thành 1)")
rec("TOC:L14", 2 ** 29 == 536870912 and round(60 / 20e-6) == 3000000
    and [k * k + 7 * k + 15 for k in (1, 2, 3, 20)] == [23, 33, 45, 555]
    and _cl.thompson_match("a?" * 29 + "a" * 29, "a" * 29)[2] == 29 * 30
    and all(_cl.bt_match(p, s)[0] == _cl.thompson_match(p, s)[0] == bool(re.fullmatch(p, s))
            for p in ("a?a?a?aaa", ".*.*=.*", ".*.*=.*;", "a*b?.") for s in ("", "aaa", "x=x", "x=xx;", "ab", "aab")),
    "a? ×29 rồi a ×29: 2^29 = 536 870 912 cách chọn, 60 s / 20 µs = 3 000 000; k² + 7k + 15 qua 23, 33, 45 cho đúng 555 ở k = 20; "
    "cách giữ tập 29·30 = 870 lần xét; bt_match, thompson_match khớp re.fullmatch")

# ═══════════ RBM — Toán cho robot & hệ động lực ═══════════
Rz = lambda t: np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Rx = lambda t: np.array([[1, 0, 0], [0, math.cos(t), -math.sin(t)], [0, math.sin(t), math.cos(t)]])
R2 = Rz(math.pi / 2)[:2, :2]
rec("RBM:L00", np.allclose(R2 @ [1, 0], [0, 1]) and np.allclose(R2.T @ R2, np.eye(2)) and np.isclose(np.linalg.det(R2), 1), "quay 90°: (1, 0) → (0, 1); RᵀR = I; det R = 1")
rec("RBM:L01", not np.allclose(Rz(math.pi / 2) @ Rx(math.pi / 2), Rx(math.pi / 2) @ Rz(math.pi / 2)), "Rz(90°)·Rx(90°) ≠ Rx(90°)·Rz(90°): thứ tự quay quan trọng")
qv = np.array([math.cos(math.pi / 4), 0, 0, math.sin(math.pi / 4)])
def qrot(q, v):
    w, x, y, z = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)], [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                  [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])
    return R @ v
rec("RBM:L02", np.allclose(qrot(qv, [1, 0, 0]), [0, 1, 0]) and np.isclose(np.linalg.norm(qv), 1), "quaternion (cos 45°, 0, 0, sin 45°) quay (1, 0, 0) thành (0, 1, 0)")
T = np.array([[0, -1, 2], [1, 0, 0], [0, 0, 1]])
T2 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) @ np.array([[1, 0, 2], [0, 1, 0], [0, 0, 1]])
rec("RBM:L03", np.allclose(T @ [1, 0, 1], [2, 1, 1]) and np.allclose(T2 @ [1, 0, 1], [0, 3, 1]),
    "toạ độ thuần nhất: quay 90° rồi tịnh tiến (2, 0) đưa (1, 0) tới (2, 1); làm ngược thứ tự thì tới (0, 3)")
th1, th2 = math.radians(30), math.radians(60)
x_, y_ = math.cos(th1) + math.cos(th1 + th2), math.sin(th1) + math.sin(th1 + th2)
rec("RBM:L04", (round(x_, 3), round(y_, 3)) == (0.866, 1.5), "tay máy 2 khâu dài 1, θ₁ = 30°, θ₂ = 60°: đầu tay tại (0,866; 1,5)")
c2 = (x_ ** 2 + y_ ** 2 - 2) / 2
sols = []
for s2 in (math.sqrt(1 - c2 ** 2), -math.sqrt(1 - c2 ** 2)):
    t2 = math.atan2(s2, c2); t1 = math.atan2(y_, x_) - math.atan2(s2, 1 + c2); sols.append((round(math.degrees(t1), 1), round(math.degrees(t2), 1)))
rec("RBM:L05", sols == [(30.0, 60.0), (90.0, -60.0)], f"động học ngược cho (0,866; 1,5): hai nghiệm (θ₁, θ₂) = {sols} (khuỷu xuống / khuỷu lên)")
rec("RBM:L06", np.isclose(np.linalg.det(np.array([[-math.sin(th1) - math.sin(th1 + 0), -math.sin(th1)], [math.cos(th1) + math.cos(th1), math.cos(th1)]])), 0),
    "det J = L₁L₂ sin θ₂ → θ₂ = 0 (tay duỗi thẳng): kỳ dị, det J = 0")
xe = 1.0
for _ in range(10): xe += 0.1 * (-xe)
rec("RBM:L07", round(xe, 4) == 0.3487 and round(math.exp(-1), 4) == 0.3679, "x' = −x, x(0) = 1, Euler h = 0,1, 10 bước: 0,9¹⁰ = 0,3487 so với e⁻¹ = 0,3679")
xr = 1.0; f_ = lambda x: -x
for _ in range(10):
    k1 = f_(xr); k2 = f_(xr + 0.05 * k1); k3 = f_(xr + 0.05 * k2); k4 = f_(xr + 0.1 * k3); xr += 0.1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
rec("RBM:L08", abs(xr - math.exp(-1)) < 1e-6, f"Runge–Kutta 4 cùng bước: sai số {abs(xr - math.exp(-1)):.1e} (Euler: 1,9·10⁻²)")
rec("RBM:L09", sorted(np.linalg.eigvals(np.array([[0, 1], [-2, -3]])).real) == [-2.0, -1.0], "x' = Ax, A = [[0, 1], [−2, −3]]: trị riêng −1, −2 < 0 → ổn định")
rec("RBM:L10", 1 / (1 + 4) == 0.2, "điều khiển tỉ lệ cho hệ bậc nhất, hệ số vòng K = 4: sai số xác lập 1/(1 + K) = 0,2 — cần khâu tích phân để về 0")
rec("RBM:L11", abs(1 - 0.25 * 10) > 1 and abs(1 - 0.05 * 10) < 1, "x_{k+1} = (1 − h·a)x_k, a = 10: h = 0,25 → |−1,5| > 1 phân kỳ; h = 0,05 → 0,5 hội tụ")
rec("RBM:L12", (0 * 1 + 1 * 1) / 2 == 0.5 and 1 * 1 / (1 + 1) == 0.5, "Kalman 1 chiều: dự đoán 0 (phương sai 1), đo 1 (phương sai 1) → ước lượng 0,5, phương sai 0,5")
rec("RBM:L14", abs(7 - 10) == 3, "lấy mẫu 10 Hz tín hiệu 7 Hz → hiện thành 3 Hz (chồng phổ); Nyquist: cần > 14 Hz")
grid = ["....", ".##.", "...."]
import heapq
def astar(g, s, t):
    H = lambda p: abs(p[0] - t[0]) + abs(p[1] - t[1])
    pq, dist = [(H(s), 0, s)], {s: 0}
    while pq:
        _, d, p = heapq.heappop(pq)
        if p == t: return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q_ = (p[0] + dr, p[1] + dc)
            if 0 <= q_[0] < len(g) and 0 <= q_[1] < len(g[0]) and g[q_[0]][q_[1]] == "." and d + 1 < dist.get(q_, 1e9):
                dist[q_] = d + 1; heapq.heappush(pq, (d + 1 + H(q_), d + 1, q_))
rec("RBM:L15", astar(grid, (1, 0), (1, 3)) == 5, "A* trên lưới 3 × 4 có tường ở giữa: từ (1, 0) tới (1, 3) mất 5 bước (Manhattan ước lượng 3, không vượt thật)")
xs, ys = np.array([0, 1, 2, 3.0]), np.array([1, 3, 5.1, 6.9])
a1, a0 = np.polyfit(xs, ys, 1)
rec("RBM:L16", (round(a1, 2), round(a0, 2)) == (1.98, 1.03), f"hiệu chuẩn cảm biến: khớp đường thẳng qua (0, 1), (1, 3), (2, 5,1), (3, 6,9): y ≈ {a1:.2f}x + {a0:.2f}")
rec("RBM:L17", (1 + 0.5 * 1) / (1 + 0.5 * 1 + 1) == 0.6 and (1 + 0.5 * 4) / (1 + 0.5 * 4 + 1) == 0.75 and round(__import__("functools").reduce(lambda p, _: p / (p + 1), range(99), 1.0), 6) == 0.01 and round(__import__("functools").reduce(lambda p, _: (p + 0.1) / (p + 0.1 + 1), range(200), 1.0), 2) == 0.27 and round(0.7 ** 2 * 1 + 0.3 ** 2 * 4, 10) == 0.85 and 3 * (3 + 1) ** 0.5 == 6 and 2 ** 24 == 16777216 and 1e8 > 2 ** 24 > 1e4 and np.allclose(np.array([[1, 1], [0, 1]]) @ np.eye(2) @ np.array([[1, 1], [0, 1]]).T, [[2, 1], [1, 1]]), "Kalman Apollo → công nghiệp (MS85): K = 0,6 / 0,75 sau 1 / 4 giờ; Q = 0: 99 phép đo → P = 0,01; Q = 0,1 → K ≈ 0,27 (P sau đo = K khi R = 1); Joseph 0,85; ngưỡng 3σ = 6; 2²⁴ = 16 777 216; U D Uᵀ = [[2, 1], [1, 1]]")

# ═══════════ SWF — Nền tảng phần mềm đúng đắn ═══════════
rec("SWF:L01", all(sum(range(i)) == i * (i - 1) // 2 for i in range(200)), "bất biến vòng lặp s = 0 + 1 + … + (i − 1) = i(i − 1)/2 đúng trước mỗi vòng")
rec("SWF:L03", (2 ** 31 - 2 + 2 ** 31 - 1) > 2 ** 31 - 1 and (2 ** 31 - 2) + ((2 ** 31 - 1) - (2 ** 31 - 2)) // 2 <= 2 ** 31 - 1,
    "tìm kiếm nhị phân: (lo + hi)/2 tràn số nguyên 32 bit khi lo, hi gần 2³¹; lo + (hi − lo)/2 không tràn")
rec("SWF:L05", 2 ** 3 == 8, "3 câu if độc lập: phủ hết nhánh cần 2 ca, phủ hết đường cần 2³ = 8 ca")
rec("SWF:L06", all(sorted(sorted(v)) == sorted(v) for v in itertools.product(range(3), repeat=4)), "tính chất sort(sort(x)) = sort(x) đúng trên mọi dãy độ dài 4 giá trị 0..2")
rec("SWF:L13", sum(20 for _ in range(24 * 60)) == 28800 and round(35000 / 3100, 1) == 11.3 and 1000 * 15 // 1000 == 15
    and 4 * 10 ** 9 // 50000 == 80000 and len([16, 8, 4, 2]) == 4 == (16).bit_length() - 1,
    "hành trình kho mã chung: 20 thay đổi/phút → 28 800/ngày (ET11); 35 000 chỗ / 3100 phần ≈ 11,3 (CM13); 1,5% của 1000 kiểm thử = 15 (FT16); "
    "4 tỉ ca / 50 000 thay đổi = 80 000 (SE20); lô 16 chia đôi 4 lần")


# ═══════════ DBS — Cơ sở dữ liệu ═══════════
import sqlite3
import hashlib
from statistics import NormalDist
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE Lop(ma TEXT PRIMARY KEY, ten TEXT);
CREATE TABLE SinhVien(mssv INTEGER PRIMARY KEY, ten TEXT, lop TEXT REFERENCES Lop(ma), diem REAL);
INSERT INTO Lop VALUES ('K1','Khoa học máy tính'),('K2','Hệ thống thông tin');
INSERT INTO SinhVien VALUES (1,'An','K1',8.0),(2,'Bình','K1',6.5),(3,'Chi','K2',9.0),(4,'Dũng',NULL,7.0);
""")
db.execute("PRAGMA foreign_keys = ON")
try:
    db.execute("INSERT INTO SinhVien VALUES (5,'Em','K9',5.0)"); fk_ok = False
except sqlite3.IntegrityError:
    fk_ok = True
rec("DBS:L00", fk_ok, "khoá ngoại: thêm sinh viên lớp 'K9' không có trong bảng Lop → bị từ chối (sqlite, foreign_keys = ON)")
rec("DBS:L01", len(db.execute("SELECT * FROM SinhVien, Lop").fetchall()) == 4 * 2
    and len(db.execute("SELECT * FROM SinhVien s JOIN Lop l ON s.lop = l.ma").fetchall()) == 3,
    "tích Đề-các SinhVien × Lop = 4 × 2 = 8 dòng; nối theo khoá ngoại còn 3 dòng (Dũng lớp NULL bị loại)")
rec("DBS:L02", db.execute("SELECT ten FROM SinhVien WHERE diem >= 7 ORDER BY ten").fetchall() == [("An",), ("Chi",), ("Dũng",)],
    "SELECT ten FROM SinhVien WHERE diem >= 7 → An, Chi, Dũng")
g = db.execute("SELECT lop, COUNT(*), AVG(diem) FROM SinhVien GROUP BY lop ORDER BY lop").fetchall()
rec("DBS:L03", db.execute("SELECT COUNT(*), COUNT(lop) FROM SinhVien").fetchone() == (4, 3)
    and db.execute("SELECT COUNT(*) FROM SinhVien WHERE lop = NULL").fetchone() == (0,)
    and db.execute("SELECT COUNT(*) FROM SinhVien WHERE lop IS NULL").fetchone() == (1,)
    and g == [(None, 1, 7.0), ("K1", 2, 7.25), ("K2", 1, 9.0)],
    f"COUNT(*) = 4 nhưng COUNT(lop) = 3; “lop = NULL” cho 0 dòng, “lop IS NULL” cho 1; GROUP BY lop: {g}")
def closure(X, F):
    X = set(X)
    while True:
        new = X | {b for a, bs in F for b in bs if set(a) <= X}
        if new == X:
            return X
        X = new
Fd = [("A", "B"), ("B", "C")]
rec("DBS:L04", closure("A", Fd) == set("ABC") and closure("AD", Fd) == set("ABCD") and closure("D", Fd) == {"D"},
    "R(A, B, C, D), F = {A→B, B→C}: bao đóng A⁺ = {A, B, C}; (AD)⁺ = R nên AD là khoá; D⁺ = {D}")
# tách R(A,B,C) với A→B thành R1(A,B), R2(A,C): không mất mát vì R1 ∩ R2 = A là khoá của R1
rows_ = {(1, "x", 10), (1, "x", 20), (2, "y", 10)}
r1 = {(a, b) for a, b, c in rows_}; r2 = {(a, c) for a, b, c in rows_}
join = {(a, b, c) for a, b in r1 for a2, c in r2 if a == a2}
bad1 = {(b, a) for a, b, c in rows_}; bad2 = {(b, c) for a, b, c in rows_}
rows2 = {(1, "x", 10), (2, "x", 20)}
b1 = {(b, a) for a, b, c in rows2}; b2 = {(b, c) for a, b, c in rows2}
badjoin = {(a, b, c) for b, a in b1 for b_, c in b2 if b == b_}
rec("DBS:L05", join == rows_ and len(badjoin) == 4 > len(rows2),
    "tách theo A→B (chung thuộc tính A là khoá của R1(A,B)) nối lại đúng 3 dòng; tách theo B (không phải khoá) nối lại sinh 4 dòng giả từ 2 dòng")
rec("DBS:L07", math.ceil(10 ** 6 / 100) == 10000, "10⁶ dòng, 100 dòng/trang → 10 000 trang; quét toàn bảng = 10 000 lần đọc trang")
rec("DBS:L08", math.ceil(math.log(10 ** 6, 100)) == 3 and 100 ** 3 >= 10 ** 6 > 100 ** 2,
    "cây B+ bậc rẽ nhánh 100, 10⁶ khoá: chiều cao ⌈log₁₀₀ 10⁶⌉ = 3 lần đọc trang, so với 10 000 trang quét")
M_, N_ = 1000, 500
rec("DBS:L10", M_ + M_ * N_ == 501000 and 3 * (M_ + N_) == 4500,
    "nối R (1000 trang) với S (500 trang): vòng lặp lồng theo trang M + M·N = 501 000 lần đọc; nối băm (Grace) ≈ 3(M + N) = 4500")
# lost update: hai giao dịch đọc 100, mỗi bên +10, ghi → 110 thay vì 120
x = 100; t1 = x; t2 = x; x = t1 + 10; x = t2 + 10
rec("DBS:L11", x == 110, "mất cập nhật: T1, T2 cùng đọc 100, mỗi bên cộng 10 rồi ghi → 110 thay vì 120")
def has_cycle(edges):
    nodes = {u for e in edges for u in e}
    st = {}
    def dfs(u):
        st[u] = 1
        for a, b in edges:
            if a == u and (st.get(b) == 1 or (st.get(b) is None and dfs(b))):
                return True
        st[u] = 2
        return False
    return any(st.get(n) is None and dfs(n) for n in nodes)
sched = [("T1", "R", "A"), ("T2", "W", "A"), ("T2", "R", "B"), ("T1", "W", "B")]
prec = {(a[0], b[0]) for i, a in enumerate(sched) for b in sched[i + 1:] if a[0] != b[0] and a[2] == b[2] and "W" in (a[1], b[1])}
rec("DBS:L12", prec == {("T1", "T2"), ("T2", "T1")} and has_cycle(prec),
    "lịch R1(A) W2(A) R2(B) W1(B): đồ thị ưu tiên T1→T2 (A) và T2→T1 (B) có chu trình → không tuần tự hoá xung đột được")
_chunks = lambda rows, b: -(-rows // b)
rec("DBS:L17", _chunks(5_000_000, 1000) == 5000 and _chunks(5_000_000, 1000) * 0.5 == 2500 and divmod(2500, 60) == (41, 40)
    and 10 ** 8 / (365 * 24 * 3600) > 3 and _chunks(10 ** 8, 1000) == 100_000,
    "hành trình thêm cột: 5 000 000 dòng, lô 1000 dòng / 0,5 s (mặc định PT11) → 5000 lô, 2500 s = 41 phút 40 giây; "
    "10⁸ đối tượng × 1 s > 3 năm (ST17); 10⁸ / 1000 = 100 000 lô")

# ═══════════ DSC — Khoa học dữ liệu ═══════════
rec("DSC:L01", round(293.15 / 283.15, 3) == 1.035, "20 °C không “gấp đôi” 10 °C: theo kelvin chỉ gấp 293,15/283,15 ≈ 1,035 lần (°C là thang khoảng, không phải thang tỉ lệ)")
left = [("k", i) for i in range(2)]; right = [("k", j) for j in range(3)]
rec("DSC:L02", len([(a, b) for a in left for b in right if a[0] == b[0]]) == 6,
    "nối hai bảng mà khoá “k” trùng 2 lần bên trái, 3 lần bên phải → 6 dòng (nhân dòng ngầm)")
xs_ = [2.0, 4.0, None, 6.0, None, 8.0]
obs = [v for v in xs_ if v is not None]; mu = sum(obs) / len(obs)
filled = [v if v is not None else mu for v in xs_]
var = lambda a: sum((t - sum(a) / len(a)) ** 2 for t in a) / (len(a) - 1)
rec("DSC:L03", mu == 5.0 and round(var(obs), 3) == 6.667 and round(var(filled), 3) == 4.0,
    f"điền trung bình 5 vào 2 ô thiếu: phương sai mẫu giảm từ {var(obs):.3f} xuống {var(filled):.3f} — giả tạo độ chắc chắn")
d = [1, 2, 3, 4, 100]
rec("DSC:L04", sum(d) / 5 == 22 and sorted(d)[2] == 3, "{1, 2, 3, 4, 100}: trung bình 22 nhưng trung vị 3 — một ngoại lai kéo lệch trung bình")
rec("DSC:L05", (52 - 50) / (51 - 50) == 2.0 and round(52 / 51, 3) == 1.020,
    "cột 51 và 52 vẽ trục bắt đầu từ 50: cột sau trông cao gấp 2 lần, thật ra chỉ hơn 2%")
xa = [1, 2, 3, 4, 5]; ya = [2, 4, 5, 4, 5]
def pear(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
rec("DSC:L06", round(pear(xa, ya), 3) == 0.775 and round(pear(xa + [20], ya + [-10]), 3) < 0,
    f"r = {pear(xa, ya):.3f}; thêm một điểm ngoại lai (20, −10) → r = {pear(xa + [20], ya + [-10]):.3f} (đổi dấu)")
A_s, A_l, B_s, B_l = (81, 87), (192, 263), (234, 270), (55, 80)
pct = lambda a: a[0] / a[1]
rec("DSC:L07", pct(A_s) > pct(B_s) and pct(A_l) > pct(B_l)
    and (A_s[0] + A_l[0]) / (A_s[1] + A_l[1]) < (B_s[0] + B_l[0]) / (B_s[1] + B_l[1])
    and (A_s[0] + A_l[0], A_s[1] + A_l[1], B_s[0] + B_l[0], B_s[1] + B_l[1]) == (273, 350, 289, 350),
    "nghịch lý Simpson (sỏi thận, Charig 1986): A tốt hơn ở sỏi nhỏ 93% > 87% và sỏi lớn 73% > 69%, nhưng gộp lại A 273/350 = 78% < B 289/350 = 83%")
p1, p2, al, pw = 0.10, 0.11, 0.05, 0.80
za, zb = NormalDist().inv_cdf(1 - al / 2), NormalDist().inv_cdf(pw)
pb = (p1 + p2) / 2
nAB = math.ceil((za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2)
rec("DSC:L08", nAB == 14751, f"A/B: tỉ lệ chuyển đổi 10% → 11%, α = 0,05 hai phía, độ mạnh 80% → cần {nAB} người mỗi nhóm")
rec("DSC:L09", round(1 - 0.95 ** 20, 3) == 0.642 and 0.05 / 20 == 0.0025,
    "20 kiểm định độc lập ở α = 0,05 khi không có hiệu ứng nào: P(ít nhất 1 “có ý nghĩa”) = 1 − 0,95²⁰ ≈ 0,642; Bonferroni: α/20 = 0,0025")
rec("DSC:L10", (lambda tr, te: (sum(tr) / len(tr), sum(tr + te) / len(tr + te)))([1, 2, 3], [10]) == (2.0, 4.0),
    "rò rỉ: chuẩn hoá bằng trung bình tính trên cả tập (4,0) thay vì chỉ tập huấn luyện (2,0) đưa thông tin tập kiểm tra vào mô hình")
sens, spec, prev = 0.99, 0.95, 0.01
ppv = sens * prev / (sens * prev + (1 - spec) * (1 - prev))
rec("DSC:L11", round(ppv, 3) == 0.167 and 0.99 == 1 - prev,
    f"bệnh hiếm 1%, xét nghiệm nhạy 99%, đặc hiệu 95%: P(bệnh | dương tính) ≈ {ppv:.3f}; mô hình luôn đoán “không bệnh” đạt accuracy 99%")
r2 = 0.9
rec("DSC:L12", round(1 / (1 - r2 ** 2), 2) == 5.26, "hai biến tương quan r = 0,9: VIF = 1/(1 − 0,81) ≈ 5,26 — sai số chuẩn của hệ số phình √5,26 ≈ 2,3 lần")
se14 = math.sqrt(0.100 * 0.900 / 15000 + 0.112 * 0.888 / 15000)
rec("DSC:L14", (round(1.2, 1), round((0.012 - 1.96 * se14) * 100, 1), round((0.012 + 1.96 * se14) * 100, 1)) == (1.2, 0.5, 1.9),
    "báo cáo: 10,0% → 11,2% với 15 000 người mỗi nhóm → tăng 1,2 điểm phần trăm, khoảng tin cậy 95% [0,5; 1,9]")
T_ = [("100**", "2*", "cúm"), ("100**", "2*", "sốt"), ("101**", "3*", "ho"), ("101**", "3*", "cúm")]
from collections import Counter as _C
rec("DSC:L13", min(_C((a, b) for a, b, _ in T_).values()) == 2, "bảng đã khái quát (mã bưu chính 100**, tuổi 2*): mỗi tổ hợp xuất hiện ≥ 2 lần → 2-ẩn danh")
rec("DSC:L15", int(0.9525 * 0.9 * 10000) == 8572 and round((0.9514 - 0.8712) / 0.9514 * 100, 2) == 8.43 and round((0.9525 - 0.8567) / 0.9525 * 100, 2) == 10.06
    and round(0.856704, 4) == round(0.856714, 4) == 0.8567 and round(2 * 800 / (2817131 / 2), 5) == 0.00114
    and round(math.sqrt(0.8558 ** 2 + 0.00114) - 0.8558, 5) == 0.00067 and round(0.00067 / 0.00001) == 67 and round((0.88 - 0.8567) / 0.88 * 100, 1) == 2.6,
    "hành trình Netflix Prize: 0,9525 × 0,9 → 0,8572; 8,43% (2007); 10,06% (2009), hoà 0,856704 / 0,856714; lạc quan 2 × 800 / 1 408 566 ≈ 0,00114 → 0,00067, gấp 67 lần; thêm ≈ 2,6% sau 0,88")

# ═══════════ DSY — Hệ phân tán và dữ liệu lớn ═══════════
# Lamport: P1: a(1) send→ P2: b(1 local) then receive → max(1,1)+1 = 2
L_a = 1; L_b = 1; L_recv = max(L_b, L_a) + 1
rec("DSY:L01", L_recv == 2, "đồng hồ Lamport: P1 gửi ở thời điểm 1, P2 đã có sự kiện thời điểm 1 → nhận ở max(1, 1) + 1 = 2")
va, vb = (2, 0, 1), (1, 2, 0)
le = lambda u, v: all(x <= y for x, y in zip(u, v))
rec("DSY:L02", not le(va, vb) and not le(vb, va) and le((1, 0, 0), va), "đồng hồ vector (2,0,1) và (1,2,0) không so được → hai sự kiện đồng thời; (1,0,0) xảy ra trước (2,0,1)")
rec("DSY:L03", all((R + W > 3) == bool(set(range(W)) & set(range(3 - R, 3))) for R in range(1, 4) for W in range(1, 4)),
    "N = 3 bản sao: R + W > N ⇔ mọi tập đọc giao mọi tập ghi (kiểm mọi R, W từ 1 đến 3); R = W = 2 đọc luôn thấy bản ghi mới nhất")
rec("DSY:L05", [n // 2 for n in (3, 4, 5)] == [1, 2, 2] and [(n - 1) // 2 for n in (3, 4, 5)] == [1, 1, 2],
    "đồng thuận đa số: 5 nút chịu được 2 nút hỏng; 4 nút cũng chỉ chịu được 1 (đa số của 4 là 3) — số nút lẻ có lợi")
keys = range(100000)
moved = sum(1 for k in keys if k % 4 != k % 5) / len(keys)
import bisect
def ring(nodes, vn=200):
    pts = sorted((int(hashlib.md5(f"{n}#{i}".encode()).hexdigest(), 16), n) for n in nodes for i in range(vn))
    return pts
def owner(pts, k):
    h = int(hashlib.md5(str(k).encode()).hexdigest(), 16)
    i = bisect.bisect(pts, (h,))
    return pts[i % len(pts)][1]
r4, r5 = ring(range(4)), ring(range(5))
ks = range(20000)
mv = sum(1 for k in ks if owner(r4, k) != owner(r5, k)) / len(ks)
rec("DSY:L06", round(moved, 2) == 0.80 and 0.15 < mv < 0.25,
    f"thêm nút thứ 5: băm “k mod N” chuyển {moved:.0%} khoá; băm nhất quán (200 nút ảo/nút) chỉ chuyển ≈ {mv:.0%} ≈ 1/5")
text = "a b a c b a"
wc = _C(text.split())
rec("DSY:L07", dict(wc) == {"a": 3, "b": 2, "c": 1}, "MapReduce đếm từ trên “a b a c b a”: map phát (từ, 1), shuffle gom theo từ, reduce cộng → a 3, b 2, c 1")
tasks = [10] * 99 + [300]
rec("DSY:L08", max(tasks) == 300 and sum(tasks) / len(tasks) == 12.9, "100 tác vụ song song, 99 tác vụ 10 s và 1 tác vụ lệch 300 s: công việc xong sau 300 s dù trung bình chỉ 12,9 s")
ev = [1, 2, 3, 7, 8, 12]
win = _C(t // 5 for t in ev)
rec("DSY:L09", dict(win) == {0: 3, 1: 2, 2: 1}, "cửa sổ nhảy 5 s trên sự kiện ở giây 1, 2, 3, 7, 8, 12 → [0, 5): 3, [5, 10): 2, [10, 15): 1")
fp = (1 - math.exp(-7 / 10)) ** 7
rec("DSY:L10", round(fp, 4) == 0.0082 and round(10 * math.log(2)) == 7, f"bộ lọc Bloom 10 bit mỗi phần tử, k = 7 hàm băm: tỉ lệ dương tính giả ≈ {fp:.4f} (≈ 0,8%), không bao giờ âm tính giả")
from fractions import Fraction as Fr
def reservoir_prob(n, k):
    # xác suất phần tử i còn trong hồ chứa sau n bước, tính chính xác
    ps = []
    for i in range(1, n + 1):
        p = Fr(1) if i <= k else Fr(k, i)
        for j in range(max(i, k) + 1, n + 1):
            p *= 1 - Fr(k, j) * Fr(1, k)
        ps.append(p)
    return ps
rec("DSY:L11", all(p == Fr(2, 10) for p in reservoir_prob(10, 2)), "lấy mẫu hồ chứa k = 2 trên luồng 10 phần tử: mỗi phần tử ở lại với xác suất đúng 2/10 (tính chính xác bằng phân số)")
col = ["VN"] * 6 + ["US"] * 3 + ["VN"]
rle = []
for v in col:
    if rle and rle[-1][0] == v: rle[-1][1] += 1
    else: rle.append([v, 1])
cols = {f"c{i}": list(range(1000)) for i in range(8)}
rec("DSY:L12", rle == [["VN", 6], ["US", 3], ["VN", 1]] and len(cols["c3"]) / sum(len(v) for v in cols.values()) == 1 / 8,
    "nén theo loạt cột quốc gia VN×6, US×3, VN×1 → 3 cặp thay 10 giá trị; đọc 1 cột trong bảng 8 cột chỉ quét 1/8 dữ liệu")
_rows = (128 * 2 ** 20) // (1 * 2 ** 10)
_moved = sum(k % 4 != k % 5 for k in range(20)) / 20
rec("DSY:L15", _rows == 2 ** 17 and _rows * _rows == 2 ** 34 and 2 ** 34 * 128 * 2 ** 20 == 2 ** 61 and _moved == 0.8
    and 30 * 200 / 1000 == 6 and (1 + 7) / 2 == 4 and 2 * 4 == 8,
    "hành trình Bigtable→Spanner: bảng chỉ mục 128 MB / dòng 1 KB = 2^17 dòng, 3 tầng → 2^34 mảnh = 2^61 byte (BT06 §5.1); chia lại 4 → 5 mảnh theo số dư chuyển 80% khoá; "
    "30 s · 200 µs/s = 6 ms, ε từ 1 tới 7 ms, trung bình 4 ms → chờ cam kết ít nhất 2ε̄ = 8 ms (SP12 §3, §4.2.1)")

# ═══════════ ESY — Hệ thống nhúng ═══════════
reg = 0b00000000
reg |= 1 << 5; s1 = reg; reg &= ~(1 << 5) & 0xFF; s2 = reg; reg ^= 1 << 3; s3 = reg
rec("ESY:L01", (s1, s2, s3) == (0b00100000, 0, 0b00001000), "bật bit 5: reg |= 1 << 5 → 0b00100000; tắt: reg &= ~(1 << 5) → 0; đảo bit 3: reg ^= 1 << 3 → 0b00001000")
rec("ESY:L02", math.ceil(5 / 1) == 5, "phím nảy trong 5 ms, lấy mẫu mỗi 1 ms: chỉ chấp nhận sau 5 mẫu liên tiếp giống nhau")
rec("ESY:L03", 16_000_000 / (64 * (249 + 1)) == 1000 and 63 / 250 == 0.252,
    "PWM: xung nhịp 16 MHz, chia trước 64, TOP = 249 → 16·10⁶/(64·250) = 1000 Hz; so sánh ở 63 → độ rộng xung (63)/250 ≈ 25%")
lsb = 3.3 / 2 ** 10
rec("ESY:L04", round(lsb * 1000, 2) == 3.22 and round(512 * lsb, 2) == 1.65 and round(6.02 * 10 + 1.76, 2) == 61.96,
    f"ADC 10 bit, tham chiếu 3,3 V: mỗi mức ≈ {lsb * 1000:.2f} mV; đọc 512 → {512 * lsb:.2f} V; SNR lý tưởng 6,02·10 + 1,76 ≈ 61,96 dB")
a_ = 0.2; y_ = 0.0
for _ in range(10): y_ = y_ + a_ * (1.0 - y_)
rec("ESY:L05", round(y_, 4) == round(1 - 0.8 ** 10, 4) == 0.8926, "lọc thông thấp bậc nhất y ← y + 0,2(x − y), đầu vào nhảy từ 0 lên 1: sau 10 mẫu y = 1 − 0,8¹⁰ ≈ 0,8926")
q88 = lambda v: round(v * 256)
rec("ESY:L06", q88(1.5) == 384 and (q88(1.5) * q88(2.25)) >> 8 == q88(3.375) and 0x7FFF == 32767,
    "Q8.8: 1,5 → 384; nhân hai số Q8.8 rồi dịch phải 8: 384·576 >> 8 = 864 = 3,375; số 16 bit có dấu tràn sau 32767")
rec("ESY:L07", 115200 / 10 == 11520, "UART 8N1: mỗi byte 10 bit (1 start + 8 dữ liệu + 1 stop) → 115 200 baud = 11 520 byte/giây")
U = 1 / 4 + 1 / 5 + 2 / 10
bound = 3 * (2 ** (1 / 3) - 1)
def rta(tasks):
    res = []
    for i, (C, T) in enumerate(tasks):
        R = C
        while True:
            Rn = C + sum(math.ceil(R / Tj) * Cj for Cj, Tj in tasks[:i])
            if Rn == R: break
            R = Rn
        res.append(R)
    return res
# 2026-11-08: ví dụ giáo án đổi theo đúng bộ tác vụ của bài (lessons/esy/L09: (1,4), (2,6), (3,12) và phản ví dụ (2,4), (3,6))
_esy9 = [(1, 4), (2, 6), (3, 12)]
_esy9_U = sum(F(c, t) for c, t in _esy9)
rec("ESY:L09", _esy9_U == F(10, 12) and float(_esy9_U) > round(bound, 4) == 0.7798 and rta(_esy9) == [1, 3, 10]
    and all(r <= t for r, (_, t) in zip(rta(_esy9), _esy9)) and sum(F(c, t) for c, t in [(2, 4), (3, 6)]) == 1 and rta([(2, 4), (3, 6)])[1] > 6,
    "RMS: (C, T) = (1, 4), (2, 6), (3, 12): U = 10/12 ≈ 0,833 > cận Liu–Layland 0,7798 (điều kiện đủ, không kết luận); thời gian đáp ứng 1, 3, 10 ≤ chu kỳ → lập lịch được; (2, 4), (3, 6): U = 1, tác vụ 2 đáp ứng 7 > 6 → trượt hạn")
def _esy10_sim(tasks, horizon, edf):
    """Mô phỏng từng đơn vị thời gian; ưu tiên cố định theo chu kỳ ngắn (edf=False) hoặc hạn sớm nhất (edf=True). Trả danh sách (tác vụ, hạn) bị trễ."""
    jobs, miss = [], []
    for t in range(horizon):
        for i, (c, p) in enumerate(tasks):
            if t % p == 0:
                jobs.append([i, t + p, c])
        for j in [j for j in jobs if j[1] <= t and j[2] > 0]:
            miss.append((j[0], j[1])); jobs.remove(j)
        ready = [j for j in jobs if j[2] > 0]
        if ready:
            run = min(ready, key=(lambda j: (j[1], j[0])) if edf else (lambda j: (tasks[j[0]][1], j[0])))
            run[2] -= 1
            if run[2] == 0:
                jobs.remove(run)
    return miss
def _esy10_inv(mid_len, inherit):
    """Thấp giữ khoá còn 3 đơn vị; Cao tới lúc 1 cần khoá 1 đơn vị; Trung bình tới lúc 2 chạy mid_len. Trả lúc Cao xong."""
    low, high, mid, now = 3, 1, mid_len, 0
    while high:
        if now >= 1 and low == 0:
            high -= 1
        elif now >= 2 and mid and not (inherit and now >= 1 and low):
            mid -= 1
        else:
            low -= 1
        now += 1
    return now
rec("ESY:L10", sum(F(c, p) for c, p in [(2, 4), (3, 6)]) == 1 and _esy10_sim([(2, 4), (3, 6)], 12, False)[:1] == [(1, 6)]
    and _esy10_sim([(2, 4), (3, 6)], 12, True) == [] and _esy10_inv(4, False) - 1 == 7 and _esy10_inv(4, True) - 1 == 3,
    "(2, 4), (3, 6): U = 1; ưu tiên cố định trễ hạn ở 6, hạn sớm nhất kịp cả hai; đảo ngược ưu tiên: Cao đáp ứng 7, kế thừa ưu tiên còn 3 (mô phỏng từng đơn vị, khác cách của verify_esy)")
rec("ESY:L08", round(math.log(0.7 / 0.3) * 1, 4) == 0.8473 and round(300e-9 / (math.log(0.7 / 0.3) * 200e-12)) == 1770 and round((3.3 - 0.4) / 3e-3) == 967,
    "I²C 400 kHz (t_r ≤ 300 ns), bus 200 pF, nguồn 3,3 V: R kéo lên trong khoảng (3,3 − 0,4)/3 mA ≈ 967 Ω tới 300 ns/(0,8473 · 200 pF) ≈ 1770 Ω")
rec("ESY:L12", 100 > 60, "bộ giám sát hạn 100 ms, vòng chính dài nhất 60 ms: cho ăn mỗi vòng còn dư 40 ms; treo thì khởi động lại sau ≤ 100 ms")
avg = 10 * 0.01 + 0.010 * 0.99
rec("ESY:L13", round(avg, 4) == 0.1099 and round(1000 / avg / 24) == 379,
    f"thức 1% thời gian ở 10 mA, ngủ 10 µA: dòng trung bình ≈ {avg:.4f} mA; pin 1000 mAh ≈ {1000 / avg:.0f} giờ ≈ 379 ngày (bỏ qua tự xả)")
rec("ESY:L15", 1 / 8 == 0.125 and 40 + 60 + 2 + 15 == 117 > 110 >= 40 + 2 + 15 and 18 * 3600 * 8 == 518400 and 4096 // 256 == 16
    and round(1480 / 90 * 3, 1) == 49.3 and round(15 * 1480 / 1440, 1) == 15.4 and 800 // 256 == 3  # sol = 24 h 39 min 35 s ≈ 1480 phút (NASA Mars Fact Sheet); 1477 là ngày sao — sửa 2026-11-09 đợt C
    and round((__import__("datetime").date(2014, 8, 29) - __import__("datetime").date(2004, 1, 25)).days / 365.25, 1) == 10.6 and round(10.6 / 0.25) == 42 and round(6 / 7, 3) == 0.857,
    "8 Hz → 0,125 s; đảo ngược ưu tiên (mốc minh hoạ 40/60/2/15 ms): xong ở 117 > 110, kế thừa → 57; 18 h × 8 Hz = 518 400 chu kỳ (GR97); "
    "4096/256 = 16 lần nới vùng nhớ; mẫu đặt lại 15–15–60 phút, sol ≈ 1480 phút → ≈ 49,3 lần/sol (cận trên); sol 18 → 33 ≈ 15,4 ngày; ngưỡng 800 KB = 3 lần nới (RN05); "
    "Opportunity 25/1/2004 → 29/8/2014 ≈ 10,6 năm ≈ 42 × thiết kế 3 tháng; tránh dãy 7/7 → còn 6/7 ≈ 85,7% (JPL 2014–2015)")

# ═══════════ CLD — Microservice, container, Kubernetes ═══════════
rec("CLD:L03", round(0.999 ** 5, 4) == 0.995 and round((1 - 0.999 ** 5) * 30 * 24 * 60) == 216,
    "chuỗi 5 dịch vụ gọi tuần tự, mỗi dịch vụ sẵn sàng 99,9%: cả chuỗi ≈ 99,5% (≈ 216 phút ngừng mỗi tháng 30 ngày)")
rec("CLD:L04", 3 ** 3 == 27 and [min(100 * 2 ** i, 2000) for i in range(6)] == [100, 200, 400, 800, 1600, 2000],
    "3 tầng, mỗi tầng thử tối đa 3 lần → tầng dưới cùng nhận tới 3³ = 27 yêu cầu (bão thử lại); lùi lũy thừa 100, 200, 400, … ms, chặn trên 2000 ms")
rec("CLD:L06", math.floor(4 / 1.5) == 2 and 4 - 2 * 1.5 == 1.0, "nút 4 CPU, mỗi Pod yêu cầu 1,5 CPU → xếp được 2 Pod, thừa 1 CPU không dùng được cho Pod thứ ba")
hpa = lambda cur, m, t, tol=0.1: cur if abs(m / t - 1) <= tol else math.ceil(cur * m / t)
rec("CLD:L07", hpa(4, 90, 60) == 6 and hpa(4, 63, 60) == 4 and hpa(10, 20, 60) == 4,
    "HPA: desired = ⌈current × metric/target⌉ (tài liệu Kubernetes): 4 bản, CPU 90% mục tiêu 60% → 6; 63% (lệch 5% < dung sai 10%) → giữ 4; 10 bản ở 20% → 4")
rec("CLD:L08", math.floor(10 * 0.25) == 2 and math.ceil(10 * 0.25) == 3 and 10 - 2 == 8 and 10 + 3 == 13,
    "cập nhật cuốn chiếu 10 bản, maxUnavailable = maxSurge = 25% (mặc định): làm tròn xuống 2, lên 3 → luôn ≥ 8 bản sẵn sàng, tối đa 13 Pod")
import random
random.seed(1)
def lb(choices, n=20000, m=100):
    load = [0] * m
    for _ in range(n):
        c = random.sample(range(m), choices)
        load[min(c, key=lambda i: load[i])] += 1
    return max(load)
mx1, mx2 = lb(1), lb(2)
rec("CLD:L09", mx2 < mx1 and mx2 <= 205, f"20 000 yêu cầu vào 100 máy (trung bình 200): chọn ngẫu nhiên 1 máy → máy tải cao nhất {mx1}; chọn ít tải hơn trong 2 máy ngẫu nhiên → {mx2}")
W1 = 1 / (100 - 80); W2 = 1 / (100 - 95)
rec("CLD:L10", round(W1 * 1000) == 50 and round(W2 * 1000) == 200 and 80 * W1 == 4,
    "hàng đợi M/M/1, phục vụ 100 yêu cầu/s: tải 80/s → thời gian trong hệ 1/(100 − 80) = 50 ms, Little: L = 80 × 0,05 = 4; tải 95/s → 200 ms")
rec("CLD:L11", round(1 - 0.99 ** 100, 3) == 0.634, "một yêu cầu gọi tới 100 máy chủ, mỗi máy chậm ở 1% lần (p99): P(yêu cầu bị chậm) = 1 − 0,99¹⁰⁰ ≈ 0,634")
rec("CLD:L12", round((1 - 0.999) * 30 * 24 * 60, 1) == 43.2 and round((1 - 0.9999) * 30 * 24 * 60, 2) == 4.32,
    "SLO 99,9% trong 30 ngày → ngân sách lỗi 43,2 phút; 99,99% → 4,32 phút")
import datetime as _dt
_adj = [k for k in range(6) if {k, (k + 1) % 6} in ({0, 1}, {2, 3}, {4, 5})]
_far = [k for k in range(6) if {k, (k + 3) % 6} in ({0, 1}, {2, 3}, {4, 5})]
rec("CLD:L15", 10000 * 0.2 == 2000 and 10000 * 0.3 == 3000 and round((1 - 0.9999) * 30 * 24 * 60, 2) == 4.32
    and (_dt.date(2015, 7, 21) - _dt.date(2014, 6, 6)).days == 410 and _adj == [0, 2, 4] and _far == [],
    "hành trình Borg→Kubernetes: tách hai loại việc cần thêm 20–30% của ô ≈ 10 000 máy = 2000–3000 máy (B15 §5.2); 99,99% → 4,32 phút/30 ngày; "
    "6/6/2014 → 21/7/2015 = 410 ngày; bản sao kề nhau mất cả hai bản ở 3 lượt cập nhật, cách 3 thì 0")

# ═══════════ MLO — MLOps ═══════════
import random as _r
def split(seed):
    g = _r.Random(seed); idx = list(range(10)); g.shuffle(idx); return idx[:7]
rec("MLO:L01", split(42) == split(42) and split(42) != split(43), "cùng hạt giống 42 → cùng cách chia train/test; đổi hạt giống → chia khác: kết quả chỉ tái lập khi ghi lại hạt giống")
h1 = hashlib.sha256(b"id,label\n1,0\n2,1\n").hexdigest()[:12]; h2 = hashlib.sha256(b"id,label\n1,0\n2,0\n").hexdigest()[:12]
rec("MLO:L02", h1 != h2, f"băm nội dung tệp dữ liệu: đổi đúng một nhãn → mã băm đổi ({h1} → {h2}); phiên bản dữ liệu nhận ra bằng mã băm")
_r.seed(0)
best = max(sum(_r.random() < 0.5 for _ in range(100)) / 100 for _ in range(200))
rec("MLO:L04", best >= 0.6, f"200 “mô hình” đoán bừa (đúng 50%), chọn cái tốt nhất trên cùng tập kiểm định 100 mẫu → điểm {best:.2f}: quá khớp vào tập kiểm định")
mu_tr, sd_tr = 50.0, 10.0
rec("MLO:L05", (70 - mu_tr) / sd_tr == 2.0 and (70 - 60) / 10 == 1.0, "lệch huấn luyện–phục vụ: huấn luyện chuẩn hoá bằng (50, 10) nhưng phục vụ dùng (60, 10) → cùng giá trị 70 thành 2,0 và 1,0")
e_ = [0.25, 0.25, 0.25, 0.25]; a_2 = [0.10, 0.20, 0.30, 0.40]
psi = sum((a - e) * math.log(a / e) for a, e in zip(a_2, e_))
rec("MLO:L08", round(psi, 3) == 0.228, f"PSI giữa phân bố huấn luyện (25% mỗi khoảng) và hiện tại (10, 20, 30, 40%) ≈ {psi:.3f} (quy ước kinh nghiệm: dưới 0,1 ổn, 0,1–0,25 theo dõi, trên 0,25 trôi đáng kể)")
pr = [0.9, 0.8, 0.3, 0.6]; yy = [1, 1, 0, 0]
brier = sum((p - y) ** 2 for p, y in zip(pr, yy)) / 4
rec("MLO:L10", round(brier, 4) == 0.125, f"điểm Brier của dự đoán (0,9; 0,8; 0,3; 0,6) với nhãn (1, 1, 0, 0) = {brier:.4f}")
scale = 2.0 / 127
qv = round(1.3 / scale)
rec("MLO:L11", qv == 83 and round(qv * scale, 4) == 1.3071 and 4 * 7e9 / 1e9 == 28 and 1 * 7e9 / 1e9 == 7,
    "lượng tử hoá đối xứng int8, khoảng [−2, 2]: bước 2/127; 1,3 → 83 → 1,3071 (sai 0,007); 7 tỉ tham số: 28 GB ở float32, 7 GB ở int8")


rec("MLO:L03", _cl.invariance_failures(_cl.toy_sentiment, "{} nói dịch vụ này rất tốt", ["An", "Hùng", "Lan"]) == []
    and _cl.invariance_failures(lambda t: _cl.toy_sentiment(t, True), "{} nói dịch vụ này rất tốt", ["An", "Hùng", "Lan"]) == ["Hùng"],
    "kiểm thử bất biến: đổi tên riêng không được đổi nhãn — mô hình lỗi đổi nhãn khi gặp “Hùng”")
rec("MLO:L06", (32 - 1) / 100 * 1000 == 310 and 32 / 0.020 == 1600 and 1 / 0.005 == 200, "gộp lô 32 ở 100 yêu cầu/s: chờ thêm 310 ms; thông lượng 1600/s (lô 20 ms) so với 200/s (từng cái 5 ms)")
_sh, _ck = _cl.feedback_loop()
rec("MLO:L09", round(_sh[-1], 2) == 0.88 and _ck == [110, 110, 10, 10, 10], "vòng phản hồi gợi ý: sau 10 vòng, 2 món được hiện chiếm 88% lượt; 3 món kia đứng yên ở 10 lượt")
rec("MLO:L12", (846 + 75) / 1000 == 0.921 and 846 / 900 == 0.94 and 75 / 100 == 0.75, "độ chính xác chung 92,1% = (846 + 75)/1000, nhưng nhóm thiểu số chỉ 75%")
rec("MLO:L13", _cl.backdoor_demo() == (0.99, 0.75) and _cl.backdoor_demo(poison=0)[1] <= 0.02, "đầu độc 20/420 mẫu: sạch vẫn 99%, 75% mẫu gắn dấu hiệu bị đổi nhãn (không đầu độc: ≤ 2%)")
rec("MLO:L14", round(465 / 45, 1) == 10.3 and 100_000 * 5 // 100 == 5000 and 100_000 - 5000 == 95_000 and 1500 / 150 == 10 and round(500 / 75, 1) == 6.7
    and round(1_000_000 * 0.02) == 20_000 and 3 * 3 * 2 == 18 and 3 * 4 * 2 == 24 and 2017 - 2007 == 10,
    "hành trình nợ kỹ thuật → nền tảng ML: 465 triệu USD / 45 phút ≈ 10,3 triệu mỗi phút (SC15); hệ 100 000 dòng (số minh hoạ) "
    "5% = 5000 dòng mã học máy, 95 000 dòng mã keo; phân vị 99,9 khi nạp mô hình 500–1500 → 75–150 ms: 1500/150 = 10, 500/75 ≈ 6,7 (TX17); "
    "+2% lượt cài trên 1 000 000 (số minh hoạ) = 20 000; 3 · 3 · 2 = 18 cấu hình, thêm một bộ chạy → 24 (TH20)")

# ═══════════ DVO — DevOps: tích hợp và triển khai liên tục ═══════════
def _bis(n, bad):
    lo, hi, c = 0, n - 1, 0
    while lo < hi:
        m = (lo + hi) // 2; c += 1
        lo, hi = (lo, m) if bad <= m else (m + 1, hi)
    return c
rec("DVO:L00", max(_bis(3, b) for b in range(3)) == 2 and max(_bis(300, b) for b in range(300)) == 9 == math.ceil(math.log2(300)),
    "chia đôi tìm thay đổi gây lỗi: lô 3 thay đổi → tối đa 2 lần dựng-kiểm; lô 300 → 9 lần (⌈log₂ 300⌉)")
rec("DVO:L01", round(1 - 0.95 ** 40, 3) == 0.871 and round(1 - 0.95 ** 3, 3) == 0.143,
    "nhánh sửa 5/100 tệp, mỗi thay đổi khác sửa 1 tệp ngẫu nhiên: 40 thay đổi chen vào → P(xung đột) = 1 − 0,95⁴⁰ ≈ 0,871; 3 thay đổi → 0,143")
rec("DVO:L02", tuple(map(int, "1.10.0".split("."))) > tuple(map(int, "1.9.3".split("."))) and "1.10.0" < "1.9.3",
    "phiên bản ngữ nghĩa: 1.10.0 mới hơn 1.9.3 khi so từng số, nhưng so chuỗi lại cho 1.10.0 < 1.9.3 — sai")
rec("DVO:L03", round(1 - 0.995 ** 300, 3) == 0.778, "300 bài kiểm thử, mỗi bài “chập chờn” hỏng ngẫu nhiên 0,5% lần: P(cả đường ống đỏ dù mã đúng) = 1 − 0,995³⁰⁰ ≈ 0,778")
# DVO L04/L06/L08/L12: ví dụ giáo án có chữ số được đồng bộ từ bài ở đợt đọc kiểm C (2026-11-09) → kiểm lại bằng cách tự dựng
def _dvo_zip(mtime, data=b'print("xin chao")\n'):
    import io as _io, zipfile as _zf
    buf = _io.BytesIO()
    with _zf.ZipFile(buf, "w", _zf.ZIP_STORED) as z:
        z.writestr(_zf.ZipInfo("app.py", date_time=mtime), data)
    return buf.getvalue()
_za, _zb = _dvo_zip((2026, 10, 1, 9, 0, 0)), _dvo_zip((2026, 10, 2, 14, 30, 0))
import hashlib as _hl
rec("DVO:L04", _hl.sha256(_za).hexdigest()[:12] == "dac8a9bd655a" and _hl.sha256(_zb).hexdigest()[:12] == "9f8086ff674d"
    and len(_za) == len(_zb) == 128 and sum(x != y for x, y in zip(_za, _zb)) == 6 and _za == _dvo_zip((2026, 10, 1, 9, 0, 0)),
    "zip một tệp, cùng thời điểm → cùng băm dac8a9bd655a; khác thời điểm → 9f8086ff674d; hai gói 128 byte khác đúng 6 byte")
rec("DVO:L06", 90 / 2 == 45 and 7 / 2 == 3.5, "khoá lộ ngẫu nhiên trong chu kỳ xoay T còn dùng trung bình T/2: 90 → 45 ngày, 7 → 3,5 ngày")
_dvo_db = sqlite3.connect(":memory:")
_dvo_db.execute("CREATE TABLE kh(id INTEGER PRIMARY KEY, ten TEXT)"); _dvo_db.execute("INSERT INTO kh(ten) VALUES ('An'), ('Binh')")
_dvo_db.execute("ALTER TABLE kh ADD COLUMN ho_ten TEXT")                 # bước 1: thêm cột mới (bản cũ vẫn chạy)
_dvo_db.execute("UPDATE kh SET ho_ten = ten WHERE ho_ten IS NULL")       # bước 2–3: chép dữ liệu, chép bù
_dvo_db.execute("ALTER TABLE kh DROP COLUMN ten")                        # bước 4: bỏ cột cũ (SQLite ≥ 3.35)
rec("DVO:L08", [r[0] for r in _dvo_db.execute("SELECT ho_ten FROM kh ORDER BY id")] == ["An", "Binh"]
    and [c[1] for c in _dvo_db.execute("PRAGMA table_info(kh)")] == ["id", "ho_ten"],
    "đổi tên cột ten → ho_ten bốn bước (thêm, chép, chép bù, bỏ cột cũ) trên sqlite3: dữ liệu giữ nguyên")
_h = int(_hl.sha256(b"anh-web-1.4.3").hexdigest(), 16) % 3233
rec("DVO:L12", 61 * 53 == 3233 and (17 * 2753) % (60 * 52) == 1 and _h == 1917 and pow(_h, 2753, 3233) == 2336 and pow(2336, 17, 3233) == 1917
    and int(_hl.sha256(b"anh-web-1.4.3-sua").hexdigest(), 16) % 3233 == 3216 != 1917,
    "RSA đồ chơi n = 61·53 = 3233, e = 17, d = 2753: băm mod n = 1917, chữ ký 2336, kiểm ra 1917; gói sửa băm 3216 → từ chối")
state = {"web": 3}
def apply(desired, cur):
    return dict(desired)
s1 = apply({"web": 5}, state); s2 = apply({"web": 5}, s1)
inc = lambda cur: {"web": cur["web"] + 2}
rec("DVO:L05", s1 == s2 == {"web": 5} and inc(inc(state)) == {"web": 7},
    "hạ tầng dạng mã khai báo “web = 5 bản” áp 2 lần vẫn là 5 (lũy đẳng); lệnh mệnh lệnh “thêm 2 bản” chạy 2 lần thành 7")
def binom_tail(n, k, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
tail = binom_tail(1000, 20, 0.01)
rec("DVO:L07", tail < 0.005, f"triển khai canary: tỉ lệ lỗi nền 1%, bản mới gặp 20 lỗi / 1000 yêu cầu; nếu bản mới tốt như cũ, P(≥ 20 lỗi) ≈ {tail:.4f} → dừng triển khai")
rec("DVO:L09", 3 / 40 == 0.075 and round(sum([30, 90, 45]) / 3) == 55,
    "chỉ số DORA: 3 lần triển khai lỗi / 40 lần → tỉ lệ thay đổi thất bại 7,5%; thời gian khôi phục 30, 90, 45 phút → trung bình 55 phút")
rec("DVO:L09", round(40 / 30, 2) == 1.33 and sorted([2, 5, 26, 8, 3])[2] == 5, "40 lần triển khai / 30 ngày ≈ 1,33 lần/ngày; thời gian đưa lên 2, 5, 26, 8, 3 giờ → trung vị 5 (đồng bộ ví dụ, đợt C)")
rec("DVO:L10", round(720 / (720 + 1), 5) == 0.99861 and round(720 / (720 + 0.25), 5) == 0.99965,
    "sẵn sàng = MTBF/(MTBF + MTTR): hỏng mỗi 720 giờ, sửa 1 giờ → 99,861%; rút thời gian sửa còn 15 phút → 99,965%")
rec("DVO:L11", 1000 * 1 * 86400 / 1e6 == 86.4 and 86.4 * 30 == 2592,
    "nhật ký 1000 yêu cầu/s × 1 KB = 86,4 GB mỗi ngày, giữ 30 ngày ≈ 2,6 TB — phải lấy mẫu hoặc tổng hợp")
rec("DVO:L13", (2 + 12) / 2 == 7 and 4 * 365 == 1460 and round(1460 / 7, 1) == 208.6 and 3.5 * 43800 / 60 == 2555 and int(1460 / 1.5) == 973 and round(26940 / 60) == 449, "hành trình đo năng lực: nhóm thấp (2 + 12)/2 = 7 lần/năm, nhóm cao 4 × 365 = 1460 → ≈ 208,6 (SD16/SD19); 3,5 tháng × 43 800 phút / 60 = 2555 (SD16); 1460 / 1,5 ≈ 973 (SD21); 2017 tính lại 26 940 / 60 ≈ 449, báo cáo ghi 440")

# ═══════════ SAR — Kiến trúc hệ thống ═══════════
_lat = _cl.scenario_latencies()
rec("SAR:L00", _cl.percentile_nr(_lat, 0.95) == 147.7 and _cl.percentile_nr(_lat, 0.99) == 399.4, "kịch bản “95% dưới 200 ms”: phân vị 95 = 147,7 ms → đạt; phân vị 99 = 399,4 ms")
_w = 100e6 / (30 * 86400)
rec("SAR:L12", round(_w, 1) == 38.6 and round(_w * 100 * 3) == 11574 and 62 ** 7 == 3521614606208 and 100e6 * 12 * 5 * 500 / 1e12 == 3.0
    and round((6e9) ** 2 / (2 * 62 ** 7) / 1e6, 1) == 5.1, "rút gọn đường dẫn: 38,6 ghi/s, 11 574 đọc/s cao điểm, 62⁷ mã, 3 TB / 5 năm, ≈ 5,1 triệu va chạm nếu sinh ngẫu nhiên")
rec("SAR:L13", 500e6 * 200 / 1e9 == 100 and (30000 / 300, 30000 / 200) == (100, 150) and (10 + 10 + 3 * 10, 10 + 10 + 10) == (50, 30) and round(143199 / 25088, 1) == 5.7 and round(143199 / 6000) == 24 and round(300000 * (1 - 0.9999)) == 30 and round(1 - 0.99 ** 100, 3) == 0.634, "hành trình Twitter: 100 GB/ngày; 100–150 máy; 50 so với 30 ms; 5,7 và 24 lần; 30 lỗi/s; 63,4%")
avg_rps = 10e6 * 20 / 86400
rec("SAR:L02", round(avg_rps) == 2315 and round(avg_rps * 3) == 6944,
    f"ước lượng nhanh: 10 triệu người dùng/ngày × 20 yêu cầu = {avg_rps:.0f} yêu cầu/s trung bình; giờ cao điểm gấp 3 ≈ {avg_rps * 3:.0f}")
lat = lambda h: h * 1 + (1 - h) * 50
rec("SAR:L04", round(lat(0.9), 2) == 5.9 and round(lat(0.99), 2) == 1.49,
    "bộ nhớ đệm 1 ms, cơ sở dữ liệu 50 ms: trúng 90% → 5,9 ms trung bình; trúng 99% → 1,49 ms (mỗi “số 9” thêm cắt độ trễ ~4 lần)")
rec("SAR:L05", math.ceil(5000 / 500) * 3 == 30, "5 TB dữ liệu, mỗi nút 500 GB, hệ số sao chép 3 → ⌈5000/500⌉ × 3 = 30 nút")
rec("SAR:L06", round(1 - 0.01 ** 2, 4) == 0.9999 and round(0.99 * 0.99, 4) == 0.9801,
    "hai thành phần độc lập 99%: đặt song song (dự phòng) → 1 − 0,01² = 99,99%; nối tiếp (phụ thuộc nhau) → 98,01%")
def bucket(rate, burst, arrivals):
    tokens, last, ok = burst, 0.0, 0
    for t in arrivals:
        tokens = min(burst, tokens + (t - last) * rate); last = t
        if tokens >= 1:
            tokens -= 1; ok += 1
    return ok
arr = [i * 0.001 for i in range(5000)]
rec("SAR:L07", bucket(10, 20, arr) == 69,
    f"giới hạn tốc độ thùng token 10/s, sức chứa 20: dồn 1000 yêu cầu/s trong 5 s chỉ nhận {bucket(10, 20, arr)}: 20 token sẵn + nạp 10/s trong 4,999 s")
rec("SAR:L08", (120 - 100) * 3600 == 72000, "hàng đợi tách hai dịch vụ: gửi 120/s, xử lý 100/s → tồn đọng tăng 20/s, sau 1 giờ còn 72 000 thông điệp — hàng đợi giảm sốc chứ không thêm năng lực")
sent = set()
def pay(key, amount, ledger):
    if key in sent: return ledger
    sent.add(key); return ledger + amount
L_ = pay("k1", 100, 0); L_ = pay("k1", 100, L_); L_ = pay("k2", 50, L_)
rec("SAR:L09", L_ == 150, "khoá lũy đẳng: gửi lại yêu cầu trả tiền “k1” do mạng chập chờn không trừ tiền hai lần → sổ cái 150 thay vì 250")
rec("SAR:L10", 2 * 40 == 80, "ghi đồng bộ sang vùng khác cách 40 ms mỗi chiều: mỗi lần ghi chờ thêm ít nhất 1 vòng = 80 ms — cái giá của nhất quán mạnh")


# ═══════════ SEC — An toàn thông tin ═══════════
import hmac as _hmac
fast, slow = 26 ** 8 / 1e10, 26 ** 8 / 1e4
rec("SEC:L01", round(fast, 1) == 20.9 and round(slow / 86400) == 242,
    f"mật khẩu 8 chữ thường (26⁸ khả năng): băm nhanh 10¹⁰ lần/s thử hết trong {fast:.1f} s; hàm băm chậm 10⁴ lần/s mất ≈ {slow / 86400:.0f} ngày")
rec("SEC:L02", round(8 * math.log2(26), 1) == 37.6 and round(4 * math.log2(7776), 1) == 51.7,
    "entropy: 8 chữ thường ngẫu nhiên = 8·log₂26 ≈ 37,6 bit; 4 từ ngẫu nhiên từ danh sách 7776 từ ≈ 51,7 bit")
rec("SEC:L03", 3 / 10 ** 6 == 3e-6, "mã một lần 6 chữ số: đoán bừa 3 lần trong một cửa sổ trúng với xác suất 3/10⁶ — vì vậy phải khoá sau vài lần sai")
blocks = [b"ATTACK!!", b"AT DAWN.", b"ATTACK!!"]
E = lambda b: hashlib.sha256(b"key" + b).digest()[:8]       # hàm khối tất định bất kỳ (mô hình chế độ ECB)
ct = [E(b) for b in blocks]
rec("SEC:L07", ct[0] == ct[2] and ct[0] != ct[1], "chế độ ECB: hai khối bản rõ giống nhau → hai khối bản mã giống nhau (lộ cấu trúc) với MỌI hàm khối tất định")
tag = _hmac.new(b"k", b"chuyen 100", hashlib.sha256).hexdigest()
rec("SEC:L08", tag != _hmac.new(b"k", b"chuyen 900", hashlib.sha256).hexdigest()
    and not _hmac.compare_digest(tag, _hmac.new(b"k2", b"chuyen 100", hashlib.sha256).hexdigest()),
    "HMAC: sửa “100” thành “900” → mã xác thực khác hẳn; không có khoá thì không tạo được mã đúng")
n50 = math.sqrt(2 * math.log(2) * 2 ** 64)
rec("SEC:L10", round(n50 / 1e9, 2) == 5.06, f"tấn công ngày sinh: băm 64 bit có ≈ 50% va chạm sau ≈ {n50 / 1e9:.2f} tỉ giá trị (≈ 1,18·2³²) — vì vậy dùng băm ≥ 256 bit")
rec("SEC:L11", 2 ** 16 / 2 == 32768, "ngẫu nhiên hoá địa chỉ với 16 bit entropy: đoán vét trung bình 2¹⁶/2 = 32 768 lần")
prec_ = 0.99 * 1e-4 / (0.99 * 1e-4 + 0.01 * (1 - 1e-4))
rec("SEC:L13", round(prec_, 4) == 0.0098, f"phát hiện xâm nhập bắt 99% tấn công, báo nhầm 1%, tấn công chiếm 1/10 000 sự kiện → chỉ {prec_:.2%} cảnh báo là tấn công thật")

rec("SEC:L04", not _cl.rbac_allowed(["kiem_toan"], "hoa_don", "tạo") and _cl.rbac_allowed(["ke_toan"], "hoa_don", "tạo")
    and _cl.sod_violation([("lan", "tạo", "HD1"), ("minh", "duyệt", "HD1"), ("lan", "tạo", "HD2"), ("lan", "duyệt", "HD2")]) == ["HD2"], "phân quyền theo vai trò; tách bạch nhiệm vụ bắt HD2")
rec("SEC:L05", _cl.csrf_check("la.vn", "nganhang.vn", "POST", "None", False) == (True, False) and _cl.csrf_check("la.vn", "nganhang.vn", "POST", "Lax", True)[0] is False,
    "giả mạo yêu cầu chéo trang: không SameSite thì cookie đi kèm nhưng mã chống giả mạo chặn; SameSite=Lax không gửi cookie")
rec("SEC:L06", _cl.render_safe("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;", "mã hoá đầu ra HTML: <script> thành &lt;script&gt;")
_c, _r = _cl.toy_cert_chain(); _c2, _r2 = _cl.toy_cert_chain(True)
rec("SEC:L09", _cl.chain_verify(_c, _r)[0] and not _cl.chain_verify(_c2, _r2)[0] and not _cl.chain_verify(_c, {})[0], "chuỗi chứng chỉ đồ chơi: hợp lệ; sửa tên → sai chữ ký; thiếu gốc → từ chối")
_R = [("ung_dung", "csdl", "5432", "cho"), ("*", "csdl", "*", "chặn"), ("*", "web", "443", "cho")]
rec("SEC:L12", [_cl.firewall(_R, *x) for x in (("ung_dung", "csdl", "5432"), ("internet", "csdl", "5432"), ("internet", "web", "443"), ("internet", "web", "22"))] == ["cho", "chặn", "cho", "chặn"],
    "tường lửa khớp luật đầu tiên, mặc định chặn")
rec("SEC:L14", not _cl.backup_321([("đĩa", "tại chỗ", False), ("đĩa", "tại chỗ", False)])[0] and _cl.backup_321([("đĩa", "tại chỗ", False), ("băng", "tại chỗ", False), ("đám mây", "nơi khác", True)])[0],
    "quy tắc 3-2-1 có bản không ghi đè được")
rec("SEC:L15", 2 ** 16 == 65536 and 65536 // 1024 == 64 and (__import__("datetime").date(2014, 4, 7) - __import__("datetime").date(2012, 3, 14)).days == 754
    and 1000 * 10 // 100 - 100 * 14 // 100 == 86 and round(538 / 223, 2) == 2.41 and 45 * 2 // 3 == 30 and 60 - 45 == 15,
    "hành trình HTTPS: 2^16 B ≈ 64 KB; 754 ngày; 100 thay chứng chỉ − 14 giữ khoá = 86; 538/223 ≈ 2,41; 2/3 · 45 = 30; lịch 60 ngày hỏng 15 ngày")

# ═══════════ PLC — Ngôn ngữ lập trình và trình biên dịch ═══════════
import re as _re
toks = _re.findall(r"[A-Za-z_]\w*|\d+|[=+*()-]", "x1 = 42+y")
rec("PLC:L01", toks == ["x1", "=", "42", "+", "y"], "phân tích từ vựng “x1 = 42+y” → 5 từ tố: x1, =, 42, +, y")
def parse(s):
    ts = _re.findall(r"\d+|[+*()-]", s); i = [0]
    def peek(): return ts[i[0]] if i[0] < len(ts) else None
    def eat(): i[0] += 1; return ts[i[0] - 1]
    def atom():
        if peek() == "(":
            eat(); v = expr(); eat(); return v
        return int(eat())
    def term():
        v = atom()
        while peek() == "*":
            eat(); v = ("*", v, atom())
        return v
    def expr():
        v = term()
        while peek() in ("+", "-"):
            op = eat(); v = (op, v, term())
        return v
    return expr()
def ev(t):
    if isinstance(t, int): return t
    a, b = ev(t[1]), ev(t[2])
    return a + b if t[0] == "+" else a - b if t[0] == "-" else a * b
rec("PLC:L02", parse("1+2*3") == ("+", 1, ("*", 2, 3)) and ev(parse("1+2*3")) == 7 and ev(parse("(1+2)*3")) == 9,
    "phân tích đệ quy xuống với tầng nhân dưới tầng cộng: 1+2*3 → cây (+ 1 (* 2 3)) = 7; (1+2)*3 = 9")
rec("PLC:L03", ev(parse("8-3-2")) == 3 and 8 - (3 - 2) == 7, "kết hợp trái: 8-3-2 = (8-3)-2 = 3; nếu văn phạm kết hợp phải sẽ ra 8-(3-2) = 7")
# phạm vi tĩnh và động: x toàn cục 1; f trả về x; g đặt x cục bộ 2 rồi gọi f
def run_scope(mode):
    """trình thông dịch tí hon: hàm f (thân: trả x) định nghĩa ở toàn cục; g gán x = 2 cục bộ rồi gọi f"""
    glob = {"x": 1}
    defs = {"f": (glob, lambda env: lookup(env, "x"))}
    def lookup(env, k):
        while env is not None:
            if k in env["vars"]: return env["vars"][k]
            env = env["parent"]
    G = {"vars": glob, "parent": None}
    def call(name, caller_env):
        _, body = defs[name]
        parent = G if mode == "static" else caller_env   # tĩnh: môi trường nơi định nghĩa; động: nơi gọi
        return body({"vars": {}, "parent": parent})
    g_env = {"vars": {"x": 2}, "parent": G}
    return call("f", g_env)
static, dynamic = run_scope("static"), run_scope("dynamic")
rec("PLC:L04", (static, dynamic) == (1, 2), "x = 1 toàn cục; f() trả x; g() đặt x = 2 cục bộ rồi gọi f(): phạm vi tĩnh → 1, phạm vi động → 2")
def counter():
    n = 0
    def inc():
        nonlocal n; n += 1; return n
    return inc
c1, c2 = counter(), counter()
rec("PLC:L07", [c1(), c1(), c1(), c2()] == [1, 2, 3, 1], "bao đóng: mỗi lần gọi counter() tạo biến n riêng → c1 cho 1, 2, 3; c2 bắt đầu lại từ 1")
heap = {"A": ["B"], "B": ["C"], "C": [], "D": ["E"], "E": ["D"]}
seen, st = set(), ["A"]
while st:
    v = st.pop()
    if v not in seen: seen.add(v); st += heap[v]
refcnt = {k: sum(k in vs for vs in heap.values()) for k in heap}
rec("PLC:L08", seen == {"A", "B", "C"} and refcnt["D"] == 1 and refcnt["E"] == 1,
    "đánh dấu–quét từ gốc A giữ A, B, C, thu hồi D, E; đếm tham chiếu không thu hồi được D ↔ E vì mỗi cái vẫn còn 1 tham chiếu")
def bad(x, acc=[]):
    acc.append(x); return acc
rec("PLC:L09", bad(1) == [1] and bad(2) == [1, 2], "Python: tham số mặc định là danh sách được tạo MỘT lần — gọi bad(1) rồi bad(2) cho [1, 2] chứ không phải [2]")
def gen(t, out):
    if isinstance(t, int): out.append(("push", t)); return out
    gen(t[1], out); gen(t[2], out); out.append(({"+": "add", "-": "sub", "*": "mul"}[t[0]],)); return out
def vm(code):
    s = []
    for ins in code:
        if ins[0] == "push": s.append(ins[1])
        else:
            b, a = s.pop(), s.pop(); s.append(a + b if ins[0] == "add" else a - b if ins[0] == "sub" else a * b)
    return s
code = gen(parse("1+2*3"), [])
rec("PLC:L10", code == [("push", 1), ("push", 2), ("push", 3), ("mul",), ("add",)] and vm(code) == [7],
    "sinh mã máy ngăn xếp cho 1+2*3: push 1, push 2, push 3, mul, add → máy ảo chạy ra 7")
def fold(t):
    if isinstance(t, (int, str)): return t
    a, b = fold(t[1]), fold(t[2])
    if isinstance(a, int) and isinstance(b, int): return ev((t[0], a, b))
    return (t[0], a, b)
rec("PLC:L11", fold(("+", ("*", 2, 3), "x")) == ("+", 6, "x"), "gấp hằng số: 2*3 + x → 6 + x lúc biên dịch; phần có biến x giữ nguyên")
rec("PLC:L13", round((223 - 85) / 223 * 100, 1) == 61.9 and round(85 / 0.35) == 243 and abs(85 / 0.35 - 20 * 12) < 5
    and round(math.exp(5 / 2.5), 2) == 7.39 and 1 / 5 == 0.2 and round(1000 / 0.2) == 5000,
    "Android: 223 → 85 lỗ hổng bộ nhớ (−61,9%); 85 / 0,35 ≈ 243 ≈ 20 · 12; tuổi thọ 2,5 năm → mã 5 năm tuổi ít lỗi hơn e² ≈ 7,39 lần; Rust 0,2 mỗi triệu dòng so với ≈ 1000 → 5000 lần")


# ═══════════ SDP — Kỹ thuật lập trình và mẫu thiết kế ═══════════
import ast
import math
import random
from functools import lru_cache
_SRC = "def phi(x, ys):\n    if x < 0:\n        return -1\n    for y in ys:\n        if y > x and y % 2 == 0:\n            return y\n    return 0\n"
_tr = ast.parse(_SRC)
_mc = 1 + sum(isinstance(n, (ast.If, ast.For, ast.While, ast.IfExp, ast.ExceptHandler)) for n in ast.walk(_tr)) \
    + sum(len(n.values) - 1 for n in ast.walk(_tr) if isinstance(n, ast.BoolOp))
rec("SDP:L00", _mc == 5, f"độ phức tạp vòng McCabe của hàm có if, for, if … and …: M = {_mc}")
def _naive(s):
    v = 0
    for ch in s:
        if not ch.isdigit(): break
        v = v * 10 + int(ch)
    return v
try:
    int("12a"); _strict = False
except ValueError:
    _strict = True
rec("SDP:L01", _naive("12a") == 12 and _strict, "“12a”: hàm dừng ở kí tự lạ trả 12 (sai lặng lẽ); int() báo ValueError")
class _Acc:
    def __init__(s, b): s._b = b
    def withdraw(s, a):
        if a > s._b: raise ValueError("không đủ số dư")
        s._b -= a
class _Open:
    def __init__(s, b): s.balance = b
_a = _Acc(100)
try:
    _a.withdraw(150); _guard = False
except ValueError:
    _guard = True
_o = _Open(100); _o.balance -= 150
rec("SDP:L02", _guard and _a._b == 100 and _o.balance == -50, "lớp giữ bất biến chặn rút 150 từ 100; trường công khai để lọt số dư −50")
_shapes = [("rect", 3 * 4), ("circle", math.pi * 1 ** 2), ("tri", 6 * 2 / 2)]
rec("SDP:L03", round(sum(a for _, a in _shapes), 2) == 21.14, "tổng diện tích 12 + π + 6 ≈ 21,14")
rec("SDP:L04", len([(k, m) for k in range(3) for m in range(2 ** 4)]) == 48 and 3 + 4 == 7, "kế thừa: 3 · 2⁴ = 48 lớp; hợp thành: 3 + 4 = 7")
_rules = [lambda v: v * 1.10, lambda v: v * 0.95]
_v = 200000
for _r in _rules: _v = _r(_v)
rec("SDP:L05", round(_v) == 209000, "200 000 qua quy tắc thuế 10% rồi quy tắc giảm 5% (thêm lớp mới) = 209 000")
class _R:
    def __init__(s): s.w = s.h = 0
    def set_w(s, v): s.w = v
    def set_h(s, v): s.h = v
    def area(s): return s.w * s.h
class _Sq(_R):
    def set_w(s, v): s.w = s.h = v
    def set_h(s, v): s.w = s.h = v
def _lsp(c):
    o = c(); o.set_w(5); o.set_h(4); return o.area()
rec("SDP:L06", _lsp(_R) == 20 and _lsp(_Sq) == 16, "đặt rộng 5, cao 4: chữ nhật 20, hình vuông 16 — vi phạm Liskov")
import datetime as _dt
def _greet(clock): return "Chúc mừng năm mới" if (clock().month, clock().day) == (1, 1) else "Xin chào"
rec("SDP:L07", _greet(lambda: _dt.date(2026, 1, 1)) == "Chúc mừng năm mới" and _greet(lambda: _dt.date(2026, 5, 2)) == "Xin chào",
    "tiêm đồng hồ giả: kết quả xác định với mọi ngày chạy kiểm thử")
class _Counter:
    n = 0
def _test_a(): _Counter.n += 1; return _Counter.n == 1
def _test_b(): _Counter.n += 1; return True
_Counter.n = 0; _ab = (_test_a(), _test_b())
_Counter.n = 0; _ba = (_test_b(), _test_a())
rec("SDP:L08", _ab == (True, True) and _ba == (True, False), "Singleton bộ đếm: A trước B qua, B trước A thì A trượt — kiểm thử phụ thuộc thứ tự")
def _size(node): return node if isinstance(node, int) else sum(_size(c) for c in node)
rec("SDP:L09", 30 + 5 + 2 == 37 and _size([120, 30, [50, 20]]) == 220 and round((98.6 - 32) * 5 / 9, 1) == 37.0,
    "Decorator 30 + 5 + 2 = 37; Composite 220; Adapter 98,6 °F → 37,0 °C")
_calls = []
_subs = [lambda e, k=k: _calls.append((k, e)) for k in range(3)]
for _e in range(4):
    for _s in _subs: _s(_e)
_x, _hist = 10, []
for _op in (lambda v: v + 5, lambda v: v * 2, lambda v: v - 3):
    _hist.append(_x); _x = _op(_x)
_after1 = _hist.pop(); _after2 = _hist.pop()
rec("SDP:L10", len(_calls) == 12 and _x == 27 and (_after1, _after2) == (30, 15), "Observer 3 × 4 = 12 lần gọi; Command 10 → 27, hoàn tác → 30 → 15")
_ST = ["mới", "đã trả", "đã giao"]
_OK = {("mới", "đã trả"), ("đã trả", "đã giao"), ("mới", "đã huỷ")}
_pairs = [(a, b) for a in _ST for b in _ST]
rec("SDP:L11", sum((a, b) in _OK for a, b in _pairs) == 2 and len(_pairs) == 9 and ("đã giao", "đã huỷ") not in _OK,
    "trong 9 cặp trạng thái (mới, đã trả, đã giao) chỉ 2 chuyển tiến hợp lệ; huỷ sau khi giao bị từ chối")
_n = [0]
def _fib(k):
    _n[0] += 1
    return k if k < 2 else _fib(k - 1) + _fib(k - 2)
_fib(30); _naive_calls = _n[0]; _n[0] = 0
@lru_cache(None)
def _mfib(k):
    _n[0] += 1
    return k if k < 2 else _mfib(k - 1) + _mfib(k - 2)
_mfib(30)
rec("SDP:L12", _naive_calls == 2692537 and _n[0] == 31 and _cl.fib_calls(30, True)[1:] == (59, 31), f"fib(30): {_naive_calls} lần gọi ngây thơ; có ghi nhớ {_n[0]} lần thật sự tính (59 lời gọi kể cả tra bộ nhớ)")
def _old(p_, q_): return (p_ * 1.1 if p_ > 100 else p_) + (5 if q_ < 3 else 0)
def _tax(p_): return p_ * 1.1 if p_ > 100 else p_
def _ship(q_): return 5 if q_ < 3 else 0
_rnd = random.Random(0)
rec("SDP:L13", all(_old(a, b) == _tax(a) + _ship(b) for a, b in ((_rnd.uniform(0, 500), _rnd.randint(0, 9)) for _ in range(10000))),
    "tách hàm thuế và phí giao: cùng kết quả trên 10 000 đầu vào ngẫu nhiên")
def _bump(v, kind):
    M, m, pp = map(int, v.split("."))
    return {"major": f"{M + 1}.0.0", "minor": f"{M}.{m + 1}.0", "patch": f"{M}.{m}.{pp + 1}"}[kind]
rec("SDP:L14", (_bump("1.4.2", "patch"), _bump("1.4.2", "minor"), _bump("1.4.2", "major")) == ("1.4.3", "1.5.0", "2.0.0"),
    "phiên bản ngữ nghĩa từ 1.4.2: sửa lỗi 1.4.3, thêm tuỳ chọn 1.5.0, phá vỡ 2.0.0")
rec("SDP:L15", 1 / (3 + 1) == 0.25, "độ bất ổn I = Ce / (Ca + Ce) = 1 / (3 + 1) = 0,25")
_cart = [150000, 200000, 100000]
_disc = lambda tot: round(tot * 0.9) if tot > 300000 else tot
rec("SDP:L16", sum(_cart) == 450000 and _disc(sum(_cart)) == 405000 and _disc(250000) == 250000,
    "giỏ 450 000, chiến lược giảm 10% khi trên 300 000 → 405 000; giỏ 250 000 không giảm")
rec("SDP:L17", 10 * 9 == 90 and 6000 // 60 == 100 and 37 * (36 // 2 + 1) == 703 and 37 * 36 == 1332 and 480 // 5 == 96 and (2024 - 2020) * 12 + (1 - 9) == 40 and 0 / (7 + 0) == 0 and 2 / (0 + 2) == 1, "hành trình nguyên khối mô-đun hoá: 10 miền → 90 chiều gọi; 6000 lớp (DM19) × 1 phút = 100 giờ; 37 thành phần (UD20) × ít nhất 19 = 703 trên 1332; 480 / 5 = 96 lần quét; 9/2020 → 1/2024 = 40 tháng; I cửa hàng 0, thông báo 1")

# ═══════════ AIF — Nền tảng trí tuệ nhân tạo (thêm 2026-10-29) ═══════════
import hashlib as _hl
import heapq as _hq
import base64 as _b64
import ipaddress as _ip
import sqlite3 as _sq
import subprocess as _sp
import re as _re2
from collections import deque as _dq, Counter as _Ct
rec("AIF:L00", 2 * 2 ** 2 == 8, "máy hút bụi 2 ô: 2 vị trí × 4 tổ hợp bẩn–sạch = 8 trạng thái")
def _nb8(s):
    i = s.index(0); r, c = divmod(i, 3)
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < 3 and 0 <= cc < 3:
            j = rr * 3 + cc; l = list(s); l[i], l[j] = l[j], l[i]; yield tuple(l)
_g8 = (0, 1, 2, 3, 4, 5, 6, 7, 8)
_d8 = {_g8: 0}; _q8 = _dq([_g8])
while _q8:
    _u = _q8.popleft()
    for _v in _nb8(_u):
        if _v not in _d8:
            _d8[_v] = _d8[_u] + 1; _q8.append(_v)
rec("AIF:L01", len(_d8) == math.factorial(9) // 2 == 181440, f"BFS từ trạng thái đích: {len(_d8)} trạng thái đạt được = 9!/2")
_s8 = (7, 2, 4, 5, 0, 6, 8, 3, 1)
_h1 = sum(1 for i, x in enumerate(_s8) if x and x != _g8[i])
_h2 = sum(abs(i // 3 - x // 3) + abs(i % 3 - x % 3) for i, x in enumerate(_s8) if x)
rec("AIF:L02", (_h1, _h2, _d8[_s8]) == (8, 18, 26) and _h1 <= _d8[_s8] and _h2 <= _d8[_s8], "8-puzzle 7 2 4 / 5 _ 6 / 8 3 1: h₁ = 8, h₂ = 18, chi phí thật 26")
_lo, _hi = 1.0, 3.0
for _ in range(80):
    _m = (_lo + _hi) / 2
    _lo, _hi = (_m, _hi) if sum(_m ** i for i in range(6)) < 53 else (_lo, _m)
rec("AIF:L03", round(_lo, 2) == 1.92, f"1 + b + … + b⁵ = 53 → b* ≈ {_lo:.3f}")
def _conf(st): return sum(1 for i in range(8) for j in range(i + 1, 8) if st[i] == st[j] or abs(st[i] - st[j]) == j - i)
def _hc(rng):
    st = [rng.randrange(8) for _ in range(8)]; steps = 0
    while True:
        best, bm = _conf(st), None
        for col in range(8):
            for row in range(8):
                if row != st[col]:
                    t = st[:]; t[col] = row; v = _conf(t)
                    if v < best: best, bm = v, (col, row)
        if bm is None: return _conf(st) == 0, steps
        st[bm[0]] = bm[1]; steps += 1
_hr = random.Random(1); _HC = [_hc(_hr) for _ in range(5000)]
_ok = [s for o, s in _HC if o]; _bad = [s for o, s in _HC if not o]
rec("AIF:L04", round(len(_ok) / 5000, 3) == 0.149 and round(sum(_ok) / len(_ok)) == 4 and round(sum(_bad) / len(_bad)) == 3,
    f"8 hậu, leo đồi dốc nhất, 5000 lần: thành công {len(_ok) / 50:.1f}%, {sum(_ok) / len(_ok):.2f} bước khi thành công, {sum(_bad) / len(_bad):.2f} khi kẹt")
_reg = "WA NT SA Q NSW V T".split()
_E = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"), ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]
_nc = sum(1 for col in itertools.product(range(3), repeat=7) if all(col[_reg.index(a)] != col[_reg.index(b)] for a, b in _E))
rec("AIF:L05", 3 ** 7 == 2187 and _nc == 18, "bản đồ Úc 3 màu: vét 2187 cách gán, 18 lời giải")
_tree = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
_ev = 0; _al = -math.inf
for _br in _tree:
    _be = math.inf
    for _x in _br:
        _ev += 1; _be = min(_be, _x)
        if _be <= _al: break
    _al = max(_al, _be)
rec("AIF:L06", max(min(b) for b in _tree) == 3 == _al and _ev == 7, "minimax = 3; alpha–beta xét 7/9 lá")
_ucb = lambda w, n, N: w / n + math.sqrt(2 * math.log(N) / n)
rec("AIF:L07", 7 / 10 > 1 / 3 and round(_ucb(7, 10, 13), 3) == 1.416 and round(_ucb(1, 3, 13), 3) == 1.641, "UCB1: A ≈ 1,416, B ≈ 1,641 (tỉ lệ thắng A cao hơn)")
_mods = [m for m in itertools.product([0, 1], repeat=3) if ((not m[0]) or m[1]) and ((not m[1]) or m[2]) and m[0]]
rec("AIF:L08", len(_mods) == 1 and all(m[2] for m in _mods), "KB = {P ⇒ Q, Q ⇒ R, P}: 1/8 mô hình, R đúng ở đó")
_rules = [({"A", "B"}, "L"), ({"A", "P"}, "L"), ({"B", "L"}, "M"), ({"L", "M"}, "P"), ({"P"}, "Q")]
_known, _agenda, _order = set(), ["A", "B"], []
_cnt = [len(p) for p, _ in _rules]
while _agenda:
    _p = _agenda.pop(0)
    if _p in _known: continue
    _known.add(_p)
    if _p not in ("A", "B"): _order.append(_p)
    for _i, (_pr, _c) in enumerate(_rules):
        if _p in _pr:
            _cnt[_i] -= 1
            if _cnt[_i] == 0: _agenda.append(_c)
rec("AIF:L09", _order == ["L", "M", "P", "Q"], f"suy diễn tiến (bộ đếm tiền đề): {_order}")
def _bw():
    st = frozenset({("A", "B"), ("B", "C"), ("C", "T")}); goal = {("A", "T"), ("B", "A"), ("C", "B")}
    def clear(s, x): return all(y != x for _, y in s)
    def moves(s):
        on = dict(s)
        for x in "ABC":
            if not clear(s, x): continue
            for y in list("ABC") + ["T"]:
                if y != x and y != on[x] and (y == "T" or clear(s, y)):
                    yield frozenset((s - {(x, on[x])}) | {(x, y)})
    d = {st: 0}; q = _dq([st])
    while q:
        u = q.popleft()
        if goal <= u: return d[u]
        for v in moves(u):
            if v not in d: d[v] = d[u] + 1; q.append(v)
rec("AIF:L10", _bw() == 3, "thế giới khối: kế hoạch ngắn nhất 3 hành động")
_PA = {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}
def _jt(b, e, a):
    pa = _PA[(b, e)] if a else 1 - _PA[(b, e)]
    return (0.001 if b else 0.999) * (0.002 if e else 0.998) * pa * (0.9 if a else 0.05) * (0.7 if a else 0.01)
_num = sum(_jt(1, e, a) for e in (0, 1) for a in (0, 1)); _den = _num + sum(_jt(0, e, a) for e in (0, 1) for a in (0, 1))
rec("AIF:L11", round(_num / _den, 3) == 0.284, f"P(trộm | John và Mary gọi) = {_num / _den:.4f}")
_S = [(x, y) for x in range(4) for y in range(3) if (x, y) != (1, 1)]; _T = {(3, 2): 1, (3, 1): -1}
_U = {s: 0 for s in _S}; _A = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}; _pp = {"N": "EW", "S": "EW", "E": "NS", "W": "NS"}
def _mv(s, a):
    n = (s[0] + _A[a][0], s[1] + _A[a][1]); return n if n in _U else s
for _ in range(1000):
    _U = {s: _T[s] if s in _T else -0.04 + max(0.8 * _U[_mv(s, a)] + 0.1 * _U[_mv(s, _pp[a][0])] + 0.1 * _U[_mv(s, _pp[a][1])] for a in _A) for s in _S}
rec("AIF:L12", round(_U[(0, 0)], 3) == 0.705 and round(_U[(2, 2)], 3) == 0.918, f"lưới 4×3: U(1,1) = {_U[(0, 0)]:.3f}, U(3,3) = {_U[(2, 2)]:.3f}")
rec("AIF:L13", int(80 * math.log10(35)) == 123, f"35⁸⁰ = 10^{80 * math.log10(35):.1f}")
rec("AIF:L14", sum(16 for _ in range(30)) == 480 and round(126e6 / (480 * 2.5e6) * 100, 1) == 10.5 and len(str(250 ** 150)) - 1 == 359
    and 1600 / 0.4 == 4000 and 1000 - 155 - 6 == 839, "hành trình máy chơi cờ: 30 × 16 = 480 chip, 126 triệu / 1,2 tỉ ≈ 10,5% (DB02); 250¹⁵⁰ ≈ 10³⁵⁹ (AG16); 1600 mô phỏng / 0,4 s = 4000 (AGZ17); 1000 − 155 − 6 = 839 hoà (AZ18)")

# ═══════════ LLM — Mô hình ngôn ngữ lớn ═══════════
_corp = [s.split() for s in ("<s> tôi thích mèo </s>", "<s> tôi thích chó </s>", "<s> bạn thích mèo </s>")]
_uni = _Ct(w for t in _corp for w in t[:-1]); _bi = _Ct((a, b) for t in _corp for a, b in zip(t, t[1:]))
_pb = lambda s: F(0) if any(_bi[(a, b)] == 0 for a, b in zip(s, s[1:])) else math.prod(F(_bi[(a, b)], _uni[a]) for a, b in zip(s, s[1:]))
_p1 = _pb("<s> tôi thích mèo </s>".split())
rec("LLM:L00", _p1 == F(4, 9), "bigram: P = 2/3 · 1 · 2/3 · 1 = 4/9")
_V = {w for t in _corp for w in t} - {"<s>"}
_lap = lambda s: math.prod(F(_bi[(a, b)] + 1, _uni[a] + len(_V)) for a, b in zip(s, s[1:]))
rec("LLM:L01", round(float(_p1) ** (-1 / 4), 3) == 1.225 and _pb("<s> chó thích mèo </s>".split()) == 0 and len(_V) == 6 and _lap("<s> chó thích mèo </s>".split()) == F(1, 504),
    "độ hỗn loạn (4/9)^(−1/4) ≈ 1,225; “chó thích mèo”: 0 khi không làm trơn, 1/504 khi cộng 1")
_voc = {"l o w </w>": 5, "l o w e r </w>": 2, "n e w e s t </w>": 6, "w i d e s t </w>": 3}; _mg = []
for _ in range(4):
    _st = _Ct()
    for w, f in _voc.items():
        sy = w.split()
        for a, b in zip(sy, sy[1:]): _st[(a, b)] += f
    _bp = max(_st, key=_st.get); _mg.append((_bp, _st[_bp]))
    _pat = _re2.compile(r"(?<!\S)" + _re2.escape(" ".join(_bp)) + r"(?!\S)")
    _voc = {_pat.sub("".join(_bp), w): f for w, f in _voc.items()}
rec("LLM:L02", _mg == [(("e", "s"), 9), (("es", "t"), 9), (("est", "</w>"), 9), (("l", "o"), 7)], f"BPE: {_mg}")
_cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))
rec("LLM:L03", round(_cos([1, 2, 0], [2, 3, 1]), 3) == 0.956 and _cos([1, 2, 0], [-2, 1, 0]) == 0, "cos ≈ 0,956; vuông góc = 0")
_mask = np.tril(np.ones((4, 4)))
rec("LLM:L04", int(_mask.sum()) == 10 == 4 * 5 // 2, "mặt nạ nhân quả 4 từ tố: 10/16 cặp")
rec("LLM:L05", 2 * 32 * 4096 * 4096 * 2 == 2 * 2 ** 30, "bộ nhớ đệm khoá–giá trị = 2 GiB")
rec("LLM:L06", round(math.exp(2.0), 2) == 7.39 and 20 * 7e9 == 1.4e11 and round(6 * 7e9 * 1.4e11 / 1e21, 1) == 5.9, "e² ≈ 7,39; 140 tỉ từ tố; C ≈ 5,9·10²¹")
def _sm(z, T=1.0):
    e = [math.exp(x / T) for x in z]; s = sum(e); return [x / s for x in e]
_s1 = _sm([2, 1, 0])
rec("LLM:L07", [round(x, 3) for x in _s1] == [0.665, 0.245, 0.09] and [round(x, 3) for x in _sm([2, 1, 0], 0.5)] == [0.867, 0.117, 0.016]
    and _s1[0] < 0.9 <= _s1[0] + _s1[1] and round(_s1[0] + _s1[1], 3) == 0.91, "softmax ở nhiệt độ 1 và 0,5; top-p 0,9 giữ 2 từ tố")
rec("LLM:L08", 2 * 4096 * 8 == 65536 and round(65536 / 4096 ** 2 * 100, 2) == 0.39, "LoRA hạng 8: 65 536 tham số ≈ 0,39%")
rec("LLM:L09", round(1 / (1 + math.exp(-1)), 3) == 0.731, "Bradley–Terry σ(1) ≈ 0,731")
rec("LLM:L10", round(1.96 * math.sqrt(0.82 * 0.18 / 500) * 100, 1) == 3.4, "khoảng tin cậy 95% ≈ ±3,4 điểm")
rec("LLM:L11", round(sum(math.comb(5, k) * 0.6 ** k * 0.4 ** (5 - k) for k in range(3, 6)), 3) == 0.683, "đa số 5 lần, mỗi lần 0,6 độc lập: 0,683")
_docs = {"A": [2, 3, 1], "B": [-2, 1, 0]}
rec("LLM:L12", max(_docs, key=lambda k: _cos([1, 2, 0], _docs[k])) == "A", "truy xuất top-1 chọn đoạn A")
rec("LLM:L13", (32 / 4) ** 2 == 64 and 32 / 4 == 8, "ngữ cảnh ×8: attention ×64, bộ nhớ đệm ×8")
rec("LLM:L14", round(6 * 174.6e9 * 3e11 / 1e23, 2) == 3.14 and round(6 * 174.6e9 * 3e11 / (1e15 * 86400), -1) == 3640
    and 1.4e12 / 70e9 == 20 and round(6 * 70e9 * 1.4e12 / 1e23, 1) == 5.9 and round(300_000 * 1.0 / 86400, 2) == 3.47,
    "hành trình mở rộng: GPT-3 6ND ≈ 3,14·10²³ ≈ 3640 PF-ngày (B20 bảng D.1); Chinchilla 1,4·10¹² / 70·10⁹ = 20, 6ND ≈ 5,9·10²³; 300 000 bước × 1 s ≈ 3,47 ngày (V17)")

# ═══════════ AGT — AI agent ═══════════
rec("AGT:L00", round(0.95 ** 20, 3) == 0.358 and round(0.99 ** 20, 3) == 0.818, "0,95²⁰ ≈ 35,8%; 0,99²⁰ ≈ 81,8%")
def _valid(args):
    return isinstance(args.get("so_tien"), int) and 0 < args["so_tien"] <= 10_000_000 and _re2.fullmatch(r"\d{10}", str(args.get("tai_khoan", ""))) is not None
# 2026-11-08: theo đúng 4 lời gọi của bài (lessons/agt/L01): hợp lệ; số tiền âm; sai kiểu + tài khoản 5 số; thừa tham số ghi_chu
_calls = [{"so_tien": 500000, "tai_khoan": "0123456789"}, {"so_tien": -200, "tai_khoan": "0123456789"},
          {"so_tien": "1000", "tai_khoan": "98765"}, {"so_tien": 1000, "tai_khoan": "9876543210", "ghi_chu": "x"}]
def _valid_strict(args):   # lược đồ đóng: đủ, đúng kiểu, trong miền, không thừa tham số
    return set(args) == {"so_tien", "tai_khoan"} and type(args["so_tien"]) is int and _valid(args)
rec("AGT:L01", [_valid_strict(c) for c in _calls] == [True, False, False, False] and _valid(_calls[3]) and not _valid_strict(_calls[3]),
    "kiểm lược đồ 4 lời gọi: chỉ 1 hợp lệ; số tiền âm, sai kiểu/tài khoản 5 số, thừa tham số đều bị từ chối trước khi chạy")
_dur = {"tim": 2, "docA": 3, "docB": 4, "tonghop": 2, "kiem": 1}; _dep = {"tim": [], "docA": ["tim"], "docB": ["tim"], "tonghop": ["docA", "docB"], "kiem": ["tonghop"]}
_fin = {}
for _k in ["tim", "docA", "docB", "tonghop", "kiem"]:
    _fin[_k] = max([_fin[d] for d in _dep[_k]], default=0) + _dur[_k]
rec("AGT:L02", sum(_dur.values()) == 12 and _fin["kiem"] == 9, "tuần tự 12 s, đường găng 9 s")
rec("AGT:L03", (128000 - 8000) // 2000 == 60, "ngữ cảnh đầy sau 60 lượt")
rec("AGT:L04", round(1 - 0.4 * 0.5 ** 2, 2) == 0.9, "độ phủ sau 3 lần truy vấn ≈ 90%")
rec("AGT:L05", round(0.6 * 0.9 / (0.6 * 0.9 + 0.4 * 0.2), 3) == 0.871, "câu được nhận đúng ≈ 87,1%")
rec("AGT:L06", 6 * 5 == 30 and 2 * 5 == 10, "6 tác tử: 30 kênh mọi cặp, 10 kênh qua điều phối")
rec("AGT:L07", round(1 - 0.3 ** 3, 3) == 0.973 and round(0.7 ** 3, 3) == 0.343, "pass@3 ≈ 97,3%; pass^3 ≈ 34,3%")
_tot = sum(2000 + 500 * i for i in range(10))
rec("AGT:L08", _tot == 42500 and 2000 + 500 * 9 == 6500 and round(_tot / 6500, 1) == 6.5, "42 500 từ tố, ≈ 6,5 lần ngữ cảnh cuối")
_pol = {"đọc": "chạy", "gửi thư": "hỏi", "chuyển tiền": "hỏi", "xoá dữ liệu": "cấm"}
rec("AGT:L09", [a for a in ("đọc", "gửi thư", "chuyển tiền", "xoá dữ liệu") if _pol[a] == "chạy"] == ["đọc"], "chỉ hành động đọc chạy ngay")
rec("AGT:L10", 22 + 15 + 9 + 4 == 50 and 22 / 50 == 0.44, "phân loại 50 lỗi: 44% chọn sai công cụ")
rec("AGT:L11", round(0.98 ** 4, 3) == 0.922 and round(0.95 ** 6, 3) == 0.735, "quy trình cố định 92,2%; tác tử 73,5%")
rec("AGT:L12", 71 - 37 == 34 and round(400 / 1400, 2) == 0.29 and round(2294 / 90000 * 100, 1) == 2.5 and round(0.0196 * 2294) == 45
    and round(286 / 2294 * 100, 2) == 12.47 and round(286 / 45, 1) == 6.4 and round(0.18 * 300) - round(0.15 * 300) == 9 and 0.65 * 500 == 325,
    "hành trình tác tử dùng công cụ: nhà ảo 71 − 37 = 34 điểm (RE23); 400/1400 ≈ 0,29 (TF23); 2294/90 000 ≈ 2,5%, 1,96% × 2294 ≈ 45 bài (SB24); "
    "286/2294 = 12,47% ≈ 6,4 lần 45 trên cùng tập; tập nhẹ 18% − 15% của 300 = 9 bài (SA24); 65% × 500 = 325 bài (SBV, khác tập)")

# ═══════════ ROB — Robot tự hành ═══════════
rec("ROB:L00", 4 + 9 + 2 + 1 == 16 and 1000 / 50 - 16 == 4, "vòng 50 Hz: dùng 16 ms, dư 4 ms")
_v, _w = (0.4 + 0.6) / 2, (0.6 - 0.4) / 0.5
rec("ROB:L01", (_v, round(_w, 3), round(_v / _w, 3)) == (0.5, 0.4, 1.25), "v = 0,5 m/s, ω = 0,4 rad/s, bán kính 1,25 m")
rec("ROB:L02", round(math.pi * 0.1 / 1000 * 1000, 3) == 0.314 and round(10 * math.sin(math.radians(1)), 3) == 0.175, "0,314 mm mỗi xung; lệch 0,175 m")
_npdf = lambda x, m, s: math.exp(-(x - m) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi))
rec("ROB:L03", round(_npdf(2.1, 2, 0.1), 2) == 2.42 and round(_npdf(2.3, 2, 0.1), 3) == 0.044 and round(_npdf(2.1, 2, 0.1) / _npdf(2.3, 2, 0.1)) == 55, "mật độ 2,42 và 0,044")
_lik = np.array([0.8 if i in (1, 4, 7) else 0.1 for i in range(10)]); _post = _lik / _lik.sum()
rec("ROB:L04", round(_post[1], 3) == 0.258 and round(_post[0], 3) == 0.032 and round(_post[[1, 4, 7]].sum(), 3) == 0.774, "niềm tin ô cửa 0,258; ô tường 0,032")
_post2 = np.roll(_post, 3) * _lik; _post2 = _post2 / _post2.sum()
rec("ROB:L04", round(_post2[4], 3) == round(_post2[7], 3) == 0.427, "hành lang VÒNG 10 ô: đi đúng 3 ô rồi thấy cửa → ô 4 và ô 7 mỗi ô ≈ 0,427 (không vòng sẽ ra 0,481)")
_th, _vd = 0.0, 1.0
_J = np.array([[1, 0, -_vd * math.sin(_th)], [0, 1, _vd * math.cos(_th)], [0, 0, 1]])
rec("ROB:L05", _J[0].tolist() == [1, 0, 0] and _J[1].tolist() == [0, 1, 1], "Jacobian chuyển động tại θ = 0")
_lo7 = math.log(0.7 / 0.3)
rec("ROB:L06", round(_lo7, 3) == 0.847 and round(3 * _lo7, 3) == 2.542 and round(1 / (1 + math.exp(-3 * _lo7)), 3) == 0.927, "log-odds 2,542 → 0,927")
_Am = np.array([[1, 0, 0], [-1, 1, 0], [0, -1, 1], [0, 0, 1]], float); _bv = np.array([1, 1, 1, 2.7])
_xs = np.linalg.lstsq(_Am, _bv, rcond=None)[0]
rec("ROB:L07", [round(x, 3) for x in _xs] == [0.925, 1.85, 2.775], f"đồ thị tư thế: {_xs.round(3).tolist()}")
rec("ROB:L08", 100 ** 6 == 10 ** 12, "6 khớp × 100 mức: 10¹² ô")
_cand = {(0.5, 0): (0.55, 0.5, 1.0), (0.3, 0.5): (0.8, 0.65, 0.6), (0.1, 1): (0.9, 0.35, 0.2)}
_sc = {k: round(0.4 * h + 0.4 * c + 0.2 * s, 2) for k, (h, c, s) in _cand.items()}
rec("ROB:L09", list(_sc.values()) == [0.62, 0.7, 0.54] and max(_sc, key=_sc.get) == (0.3, 0.5), f"cửa sổ động: {_sc}")
rec("ROB:L10", 2 * 0.5 / 2 ** 2 == 0.25, "độ cong 0,25 m⁻¹")
rec("ROB:L11", 800 * 0.5 / 4 + 640 == 740, "u = 740")
rec("ROB:L12", round(1.5 ** 2 / 2 + 1.5 * 0.2, 3) == 1.425, "quãng dừng 1,425 m")
rec("ROB:L13", round(0.05 * 142, 1) == 7.1 and round((25 * 0.44704) * 0.2 + (25 * 0.44704) ** 2 / 8, 1) == 17.8 < 22
    and 22 < round((35 * 0.44704) * 0.2 + (35 * 0.44704) ** 2 / 8, 1) == 33.7 < 70 and round(30 * math.sin(math.radians(0.5)), 3) == 0.262
    and 18 + 29 == 47 and round(29 / 47, 2) == 0.62 and round(48 / 56.7, 2) == 0.85 and round(1 - 0.85 / 4.04, 2) == 0.79,
    "142 dặm × 5% = 7,1; quãng dừng 17,8 m (25 dặm/giờ) < 22 m < 33,7 m (35 dặm/giờ) < 70 m; 0,5° ở 30 m → 0,262 m; 29/47 ≈ 62%; 48/56,7 ≈ 0,85 → giảm 79%")

# ═══════════ DEN — Kỹ thuật dữ liệu ═══════════
rec("DEN:L00", 100e6 * 50 * 8 / 1e9 == 40 and round(100e6 * 3 * 8 / 1e9, 1) == 2.4, "theo hàng 40 GB, theo cột 2,4 GB")
rec("DEN:L01", round(5 * 0.01, 2) == 0.05, "5 tệp × 1% = 0,05 lần đọc thừa")
rec("DEN:L02", 4096 / 100 == 40.96, "khuếch đại ghi 40,96")
rec("DEN:L03", 16 * 2 ** 20 // 200 == 83886, "16 MiB / 200 byte = 83 886")
_keys = [f"2026-10-29#{i % 10}" for i in range(100000)]; _load = _Ct(k.split("#")[1] for k in _keys)
rec("DEN:L04", len({k.split("#")[0] for k in _keys}) == 1 and max(_load.values()) / 100000 == 0.1, "1 phân vùng nóng; hậu tố 0–9 → 10% mỗi phân vùng")
rec("DEN:L05", 86400 * 100 / 1e6 == 8.64 and round(86400 * 100 * 365 / 1e9, 2) == 3.15, "8,64 MB/ngày; 3,15 GB/năm")
rec("DEN:L06", 100 ** 2 == 10 ** 4 and 100 ** 3 == 10 ** 6, "2 bước 10⁴, 3 bước 10⁶")
_dd = [["mèo", "đen", "mèo"], ["chó", "đen"], ["mèo", "trắng", "chó", "con"]]
_avg = sum(map(len, _dd)) / 3
def _bm25(q, d, k1=1.2, b=0.75):
    s = 0.0
    for t in q:
        n = sum(t in x for x in _dd); idf = math.log((3 - n + 0.5) / (n + 0.5) + 1); tf = d.count(t)
        s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / _avg))
    return s
rec("DEN:L07", [round(_bm25(["mèo"], d), 3) for d in _dd] == [0.646, 0.0, 0.414], "BM25 “mèo”: 0,646; 0; 0,414")
_part = lambda P, C: [P // C + (1 if i < P % C else 0) for i in range(C)]
rec("DEN:L08", _part(12, 5) == [3, 3, 2, 2, 2] and _part(12, 13).count(0) == 1, "12 phân vùng / 5 thành viên: 3, 3, 2, 2, 2; 13 → 1 rảnh")
rec("DEN:L09", 40 - 30 == 10, "phát lại 10 s")
_rdn = random.Random(7); _lost = sum(1 for _ in range(10 ** 6) if _rdn.random() < 0.001)
rec("DEN:L10", abs(_lost - 1000) < 5 * math.sqrt(1000), f"mô phỏng 10⁶ đơn: mất {_lost} sự kiện (≈ 1000)")
_days = list(range(100)); _sorted = [list(range(i, i + 1)) for i in _days]; _rs = random.Random(3)
_uns = [[_rs.randrange(100) for _ in range(1000)] for _ in range(100)]
rec("DEN:L11", sum(min(g) <= 42 <= max(g) for g in _sorted) == 1 and sum(min(g) <= 42 <= max(g) for g in _uns) == 100, "sắp theo ngày đọc 1 nhóm; không sắp đọc 100")
_cn = _sq.connect(":memory:")
_cn.executescript("""CREATE TABLE dim_kh(sk INT, kh TEXT, tinh TEXT, tu TEXT, den TEXT);
INSERT INTO dim_kh VALUES (1,'k1','Hà Nội','2026-01-01','2026-03-01'),(2,'k1','Đà Nẵng','2026-03-01','9999-12-31');
CREATE TABLE fact(ngay TEXT, kh TEXT, tien INT); INSERT INTO fact VALUES ('2026-02-10','k1',100),('2026-03-10','k1',200);""")
_scd2 = _cn.execute("SELECT substr(f.ngay,1,7), d.tinh, f.tien FROM fact f JOIN dim_kh d ON d.kh=f.kh AND f.ngay>=d.tu AND f.ngay<d.den ORDER BY 1").fetchall()
_scd1 = _cn.execute("SELECT substr(f.ngay,1,7), d.tinh, f.tien FROM fact f JOIN dim_kh d ON d.kh=f.kh AND d.den='9999-12-31' ORDER BY 1").fetchall()
rec("DEN:L12", _scd2 == [("2026-02", "Hà Nội", 100), ("2026-03", "Đà Nẵng", 200)] and [r[1] for r in _scd1] == ["Đà Nẵng", "Đà Nẵng"], "lưu lịch sử vs ghi đè")
rec("DEN:L13", 1 * 99 == 99 and round((1000 + 1) * 0.99) == 991, "phát tán 99 GB; xáo trộn ≈ 991 GB")
rec("DEN:L14", round(29_423 * 1.2) == 35_308 and round(1283 / 891 - 1, 2) == 0.44 and (80 + 9 * 76, 46 + 9 * 3) == (764, 73) and round(764 / 73, 1) == 10.5
    and 13 * 60 + 2 + 30 > 13 * 60 + 20 and 13 * 60 + 20 + 30 <= 13 * 60 + 57 and 1000 // 200 == 5,
    "35 308 lần máy chết; +44%; 764 s so với 73 s ≈ 10,5 lần; 13:02 và 13:20 gộp một phiên, 13:57 phiên mới; 5 lô mỗi giây")

# ═══════════ WEB — Web và di động ═══════════
rec("WEB:L00", 3 * 50 == 150, "3 vòng khứ hồi × 50 ms = 150 ms")
from html.parser import HTMLParser as _HP
class _Tr(_HP):
    def __init__(s): super().__init__(); s.n = 0; s.d = 0; s.mx = 0
    def handle_starttag(s, t, a): s.n += 1; s.d += 1; s.mx = max(s.mx, s.d)
    def handle_endtag(s, t): s.d -= 1
_tp = _Tr(); _tp.feed("<ul><li>A</li><li>B<b>!</b></li></ul>")
rec("WEB:L01", (_tp.n, _tp.mx) == (4, 3), "4 phần tử, độ sâu 3")
rec("WEB:L02", 200 + 2 * 20 + 2 * 5 == 250 and (1, 1, 0) > (0, 2, 1), "hộp 250 px; (1,1,0) thắng (0,2,1)")
def _node(js):
    try:
        return _sp.run(["node", "-e", js], capture_output=True, text=True, timeout=30).stdout.split()
    except Exception:
        return None
_o3 = _node("console.log(1);setTimeout(()=>console.log(2),0);Promise.resolve().then(()=>console.log(3));console.log(4)")
rec("WEB:L03", _o3 == ["1", "4", "3", "2"], f"Node: {_o3}")
_o4 = _node("const w=ms=>new Promise(r=>setTimeout(r,ms));(async()=>{let t=Date.now();await w(100);await w(200);await w(300);const a=Date.now()-t;t=Date.now();await Promise.all([w(100),w(200),w(300)]);console.log(a,Date.now()-t)})()")
rec("WEB:L04", _o4 is not None and len(_o4) == 2 and 590 <= int(_o4[0]) <= 700 and 295 <= int(_o4[1]) <= 380, f"Node đo: tuần tự {_o4[0] if _o4 else '?'} ms, đồng thời {_o4[1] if _o4 else '?'} ms")
import bisect as _bs
def _lis(seq):
    t = []
    for x in seq:
        i = _bs.bisect_left(t, x)
        t[i:i + 1] = [x]
    return len(t)
_old_, _new_ = list("ABCDE"), list("CABDE")
rec("WEB:L05", len(_new_) - _lis([_old_.index(x) for x in _new_]) == 1, "di chuyển 1 phần tử")
_meth = {"GET": (True, True), "HEAD": (True, True), "PUT": (False, True), "DELETE": (False, True), "POST": (False, False)}
rec("WEB:L06", [m for m, (s, i) in _meth.items() if s] == ["GET", "HEAD"] and [m for m, (s, i) in _meth.items() if i and not s] == ["PUT", "DELETE"] and not _meth["POST"][1],
    "RFC 9110 mục 9.2: an toàn GET, HEAD; lũy đẳng thêm PUT, DELETE; POST không")
_cw = _sq.connect(":memory:"); _cw.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, v)"); _cw.executemany("INSERT INTO t VALUES (?,?)", ((i, i) for i in range(1, 30001)))
_r1 = _cw.execute("SELECT id FROM t ORDER BY id LIMIT 20 OFFSET ?", ((1000 - 1) * 20,)).fetchall()
_r2 = _cw.execute("SELECT id FROM t WHERE id > ? ORDER BY id LIMIT 20", (19980,)).fetchall()
rec("WEB:L07", (1000 - 1) * 20 == 19980 and _r1 == _r2 and _r1[0][0] == 19981, "trang 1000: độ lệch 19 980; con trỏ cho cùng kết quả")
_fresh = lambda age, maxage: age < maxage
rec("WEB:L08", not _fresh(700, 600) and _fresh(500, 600), "700 s > max-age 600 → cũ, xác thực lại")
_chal = _b64.urlsafe_b64encode(_hl.sha256(b"dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk").digest()).rstrip(b"=").decode()
rec("WEB:L09", _chal == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM", "PKCE khớp vector RFC 7636 phụ lục B")
rec("WEB:L10", 2e6 / 200e3 == 10 and 500e3 / 200e3 == 2.5, "10 s và 2,5 s")
def _lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
_cr = lambda a: (1.05) / (_lum(a) + 0.05)
rec("WEB:L11", round(_cr("777777"), 2) == 4.48 and round(_cr("767676"), 2) == 4.54, "WCAG: #777 4,48; #767676 4,54")
rec("WEB:L12", round(1000 / 60, 1) == 16.7 and round(1000 / 120, 1) == 8.3, "16,7 ms và 8,3 ms")
_a, _b = {"mua sữa"}, {"gọi mẹ"}
rec("WEB:L13", len(_b) == 1 and len(_a | _b) == 2, "ghi sau thắng còn 1; hợp tập hợp giữ 2")
rec("WEB:L14", round(0.7 ** 4, 2) == 0.24, "sau 4 tuần còn 24%")
_ss = lambda total, w: (lambda f: f(f, total, w, 0))(lambda f, n, w, r: r if n <= 0 else f(f, n - w, 2 * w, r + 1))
rec("WEB:L15", 11 * (1 + 1) == 22 and 22 * 50 == 1100 and 1 + 11 == 12 and 1 + 1 + 1 == 3 and 3 * 50 == 150
    and _ss(100 * 500, 10 * 1460) == 3 and _ss(500 + 99 * 20, 10 * 1460) == 1 and 4 * 50 == 200,
    "hành trình HTTP: 22 / 12 / 3 vòng (1100 / 150 ms); tiêu đề 50 000 B → 3 vòng, nén 2480 B → 1 vòng; mất gói 4 luồng 200 ms vs 50 ms")

# ═══════════ BCH — Blockchain ═══════════
def _blk(prev, data): return _hl.sha256((prev + "|" + data).encode()).hexdigest()
_data = ["khối 0", "A trả B 5", "B trả C 2", "C trả A 1"]; _hs = []
_p = "0" * 64
for _d_ in _data:
    _p = _blk(_p, _d_); _hs.append(_p)
_data2 = list(_data); _data2[2] = "B trả C 20"
def _first_bad(data, hashes):
    p = "0" * 64
    for i, d in enumerate(data):
        p2 = _blk(p, d)
        if p2 != hashes[i]: return i
        p = hashes[i]
    return None
_hs2 = list(_hs); _hs2[2] = _blk(_hs[1], _data2[2])   # kẻ sửa tính lại mã của khối 3 nhưng không sửa khối 4
rec("BCH:L01", _first_bad(_data, _hs) is None and _first_bad(_data2, _hs) == 2 and _first_bad(_data2, _hs2) == 3,
    "sửa khối thứ 3 → sai tại khối 3; tính lại mã khối 3 → sai tại khối 4")
def _merkle(leaves):
    lv = [_hl.sha256(x).digest() for x in leaves]; levels = [lv]
    while len(lv) > 1:
        lv = [_hl.sha256(lv[i] + lv[i + 1]).digest() for i in range(0, len(lv), 2)]; levels.append(lv)
    return levels
_lev = _merkle([f"gd{i}".encode() for i in range(1024)])
_idx = 357; _proof = []
for _l in _lev[:-1]:
    _proof.append(_l[_idx ^ 1]); _idx //= 2
_h = _hl.sha256(b"gd357").digest(); _idx = 357
for _sib in _proof:
    _h = _hl.sha256(_h + _sib).digest() if _idx % 2 == 0 else _hl.sha256(_sib + _h).digest(); _idx //= 2
rec("BCH:L02", len(_proof) == 10 and len(_proof) * 32 == 320 and _h == _lev[-1][0], "bằng chứng 10 mã băm = 320 byte, kiểm ra đúng gốc")
_n, _e, _dk = 3233, 17, 2753
_hm = lambda m: int(_hl.sha256(m.encode()).hexdigest(), 16) % _n
_sig = pow(_hm("A trả B 5"), _dk, _n)
rec("BCH:L03", pow(_sig, _e, _n) == _hm("A trả B 5") and pow(_sig, _e, _n) != _hm("A trả B 50"), "ký đúng; sửa nội dung → sai chữ ký")
rec("BCH:L04", round(5 + 3 - 6 - 0.1, 1) == 1.9 and 5 + 3 >= 6.1 > 5, "dùng 5 + 3, tiền thừa 1,9")
_nonce = 0
while True:
    _hh = _hl.sha256(b"khoi-1|" + str(_nonce).encode()).digest()
    if _hh[0] == 0 and _hh[1] == 0: break
    _nonce += 1
rec("BCH:L05", 2 ** 16 == 65536 and _nonce + 1 == 50845, f"16 bit 0: kỳ vọng 65 536; trúng ở lần {_nonce + 1}")
def _catch(q, z):
    p = 1 - q; lam = z * q / p
    return 1 - sum(math.exp(-lam) * lam ** k / math.factorial(k) * (1 - (q / p) ** (z - k)) for k in range(z + 1))
rec("BCH:L06", round(_catch(0.1, 6), 7) == 0.0002428 and round(_catch(0.3, 5), 7) == 0.1773523 and round(_catch(0.1, 1), 7) == 0.2045873, "khớp bảng Nakamoto 2008")
rec("BCH:L07", (100 - 1) // 3 == 33 and 2 * 33 + 1 == 67 and 3 * 33 + 1 <= 100, "100 bên: f = 33, đại biểu 67")
rec("BCH:L08", round(21000 * 20e-9, 5) == 0.00042, "phí 0,00042 ETH")
def _vault(safe):
    bal = {"ke": 1}; pool = [10]
    def withdraw(depth=0):
        if bal["ke"] <= 0 or pool[0] <= 0: return 0
        amt = bal["ke"]
        if safe:
            bal["ke"] = 0; pool[0] -= amt; return amt
        pool[0] -= amt; got = amt + (withdraw(depth + 1) if pool[0] > 0 else 0); bal["ke"] = 0; return got
    return withdraw()
rec("BCH:L09", (_vault(False), _vault(True)) == (10, 1), "gửi trước trừ sau: rút cạn 10; trừ trước: chỉ 1")
rec("BCH:L10", round(1e6 / 250 / 600, 1) == 6.7, "≈ 6,7 giao dịch mỗi giây")
_hon = [100, 101, 99, 100]; _bad_ = [0, 0, 10 ** 6]
rec("BCH:L11", min(_hon) <= sorted(_hon + _bad_)[3] <= max(_hon) and (7 - 1) // 2 == 3, "trung vị 7 nguồn chịu 3 nguồn sai")
rec("BCH:L12", 80 * 6 * 24 * 365 == 4_204_800 and 3 * 1_000_000 + 1_000_000 == 4_000_000 and 1916 / 2016 > 0.95 and 481_824 == 239 * 2016
    and (__import__("datetime").date(2022, 9, 15) - __import__("datetime").date(2020, 12, 1)).days == 653 and 32 * 12 / 60 == 6.4,
    "tiêu đề 4 204 800 byte/năm; khối cũ = 4 000 000 trọng lượng; 1916/2016 ≈ 95,04%; khối 481 824 = 239 · 2016; 653 ngày song song; kỷ nguyên 6,4 phút")

# ═══════════ CLC — Điện toán đám mây ═══════════
rec("CLC:L01", round((1 - 0.005 ** 2) * 100, 4) == 99.9975, "2 vùng sẵn sàng: 99,9975%")
_subs = list(_ip.ip_network("10.0.0.0/16").subnets(new_prefix=24))
rec("CLC:L02", len(_subs) == 256 and _subs[0].num_addresses - 5 == 251, "256 mạng con /24, 251 địa chỉ dùng được")
def _iam(action, res, pols):
    dec = "từ chối"
    for eff, acts, r in pols:
        if (action in acts or "*" in acts) and r == res:
            if eff == "deny": return "từ chối"
            dec = "cho"
    return dec
_pols = [("allow", {"*"}, "bao-cao"), ("deny", {"xoá"}, "bao-cao")]
rec("CLC:L03", [_iam(a, r, _pols) for a, r in (("đọc", "bao-cao"), ("xoá", "bao-cao"), ("ghi", "kho-khac"))] == ["cho", "từ chối", "từ chối"], "đọc cho, xoá từ chối, kho khác mặc định từ chối")
rec("CLC:L04", math.isclose(1e7 * 1e-11, 1e-4) and round(1 / (1e7 * 1e-11)) == 10000, "10⁻⁴ đối tượng mỗi năm")
rec("CLC:L05", round(500 / 0.10) == 5000 and round(5000 / 8760 * 100) == 57 and 6 * 10 + 2 * 14 == 88 and 6 * 24 == 144
    and round((144 - 88) / 144 * 100, 1) == 38.9, "hoà vốn 5000 giờ ≈ 57%; co giãn 6·10 + 2·14 = 88 thay vì 144 giờ máy ≈ 38,9% ít hơn")
rec("CLC:L06", round(1e6 * 0.2 * 0.5) == 100000, "100 000 GB-giây")
rec("CLC:L07", 5 < 24 * 60, "RPO 5 phút so với 24 giờ")
rec("CLC:L08", round(50 * 1024 * 0.09) == 4608, "50 TB = 50 · 1024 GB, 0,09 đô la/GB ≈ 4608 đô la")
rec("CLC:L09", 10000 * 32 == 320000, "320 000 byte khoá")
rec("CLC:L10", 2 * 1.0 == 2.0, "chủ động–chủ động: mỗi vùng gánh 100% → dung lượng ×2")
rec("CLC:L12", (13 * 60 + 54) - (9 * 60 + 37) == 257 and divmod(257, 60) == (4, 17) and round(365 * 24 * 60 * (1 - 0.9999), 2) == 52.56
    and 2 * 10 ** 14 // (8 * 10 ** 8) == 250000 and round(257 / 52.56, 1) == 4.9,
    "hành trình kho lưu trữ đối tượng: sự cố 2017 9:37 → 13:54 = 257 phút = 4 giờ 17 phút (S17); ngân sách 99,99%/năm = 52,56 phút → ≈ 4,9 năm; "
    "800 triệu → 200 nghìn tỉ đối tượng = ×250 000 (PI22)")

# ═══════════ DAN — Phân tích dữ liệu ═══════════
import statistics as _st
_log = [("u1", "dang_nhap"), ("u1", "xem"), ("u2", "dang_nhap"), ("u2", "mua"), ("u3", "dang_nhap"), ("u4", "dang_nhap"), ("u4", "xem"),
        ("u5", "dang_nhap"), ("u6", "dang_nhap"), ("u6", "binh_luan")]
rec("DAN:L00", len({u for u, e in _log if e == "dang_nhap"}) == 6 and len({u for u, e in _log if e != "dang_nhap"}) == 4, "đăng nhập: 6; có thao tác: 4")
rec("DAN:L01", (50 + 200) / 2 == 125 and round((100 * 50 + 10 * 200) / 110, 2) == 63.64, "125 so với 63,64")
_cd = _sq.connect(":memory:")
_cd.executescript("CREATE TABLE don(id INT, tong INT); INSERT INTO don VALUES (1,100),(2,50); CREATE TABLE dong(don INT, sp TEXT);"
                  " INSERT INTO dong VALUES (1,'a'),(1,'b'),(1,'c'),(2,'a'); CREATE TABLE dt(ngay INT, tien INT); INSERT INTO dt VALUES (1,10),(2,30),(3,20),(4,40);")
rec("DAN:L02", _cd.execute("SELECT SUM(tong) FROM don").fetchone()[0] == 150 and _cd.execute("SELECT SUM(d.tong) FROM don d JOIN dong x ON x.don = d.id").fetchone()[0] == 350,
    "150 thật, 350 sau khi nối")
_w = _cd.execute("SELECT SUM(tien) OVER (ORDER BY ngay), tien - LAG(tien) OVER (ORDER BY ngay), RANK() OVER (ORDER BY tien DESC) FROM dt ORDER BY ngay").fetchall()
rec("DAN:L03", [r[0] for r in _w] == [10, 40, 60, 100] and [r[1] for r in _w] == [None, 20, -10, 20] and [r[2] for r in _w] == [4, 2, 3, 1], f"sqlite3 {_sq.sqlite_version}: lũy kế, LAG, RANK")
rec("DAN:L04", 30 / 100 == 0.3 and 18 / 100 == 0.18 and 45 / 120 == 0.375, "30%, 18%; 37,5%")
_f = [10000, 4000, 1200, 300]
rec("DAN:L05", [round(_f[i + 1] / _f[i] * 100) for i in range(3)] == [40, 30, 25] and _f[3] / _f[0] == 0.03, "40%, 30%, 25%; toàn phễu 3%")
_y = [100 + (30 if d % 7 in (5, 6) else 0) + 2 * d for d in range(28)]
_ma = [sum(_y[i - 6:i + 1]) / 7 for i in range(6, 28)]
rec("DAN:L06", all(abs((_ma[i + 1] - _ma[i]) - 2) < 1e-9 for i in range(len(_ma) - 1)), "trung bình trượt 7 ngày tăng đều 2")
_a, _p = [0, 10, 12, 8], [2, 9, 12, 10]
rec("DAN:L07", sum(abs(x - y) for x, y in zip(_a, _p)) / 4 == 1.25 and 0 in _a, "MAE 1,25; MAPE không xác định vì có 0")
_rv = [500, 200, 100, 60, 40, 30, 30, 20, 10, 10]
rec("DAN:L08", sum(_rv[:2]) / sum(_rv) == 0.7, "20% khách đầu = 70% doanh thu")
_v = [100, 102, 98, 101, 99, 103, 100, 500]
_md = _st.median(_v)
_mad = _st.median([abs(x - _md) for x in _v])
rec("DAN:L09", round((500 - _st.mean(_v)) / _st.pstdev(_v), 2) == 2.65 and _md == 100.5 and _mad == 1.5 and round((500 - _md) / (1.4826 * _mad), 1) == 179.6,
    "z 2,65; điểm bền vững 179,6")


def _wil(k, n, z=1.96):
    ph = k / n
    d = 1 + z * z / n
    c = ph + z * z / (2 * n)
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return round((c - h) / d, 3), round((c + h) / d, 3)


rec("DAN:L10", _wil(2, 2) == (0.342, 1.0) and _wil(150, 1000) == (0.129, 0.173), "Wilson: A [0,342; 1], B [0,129; 0,173]")
rec("DAN:L11", (105 - 95) / (100 - 95) == 2 and round(105 / 100 - 1, 2) == 0.05, "trục cắt ở 95: trông gấp 2, thật hơn 5%")
rec("DAN:L12", (4 * 2 * 30 / (3.75 * 0.05)) ** 2 == 1638400 and round((4 * 2 * math.sqrt(0.05 * 0.95) / 0.0025) ** 2) == 486400
    and round(486400 / 16) == 30400 and round(1 / (4 * 0.01 * 0.99)) == 25 and round(1 - 0.975 ** 5, 3) == 0.119 and round(1 - 0.975 ** 30, 3) == 0.532
    and 5 ** 15 == 30517578125 and round((0.5 - 499 / 999) / math.sqrt(0.25 / 1e6), 1) == 1.0 and round((0.5 - 499 / 999) / math.sqrt(0.25 / 1e7), 2) == 3.17,
    "hành trình thử nghiệm có đối chứng: (4·2·30/0,1875)² = 1 638 400, tỉ lệ mua 486 400 → 20%: 30 400 (KO07); chia 99/1 lâu ≈ 25 lần (KO07); "
    "1 − 0,975⁵ ≈ 11,9% (KO13 “12%”), 1 − 0,975³⁰ ≈ 53,2%; 5¹⁵ ≈ 30 tỉ phiên bản (KO13); lỗi thiếu một ô 499/999: 1 triệu người 1,0, 10 triệu người 3,17 sai số chuẩn")

# ═══════════ EVT — Kiến trúc hướng sự kiện ═══════════
rec("EVT:L00", 10 * 9 // 2 == 45, "45 kết nối điểm–điểm, 10 qua kênh")
_new_reader = lambda e: {"ma": e["ma"], "tien": e["tien"], "ghi_chu": e.get("ghi_chu", "")}
_old_reader = lambda e: {"ma": e["ma"], "tien": e["tien"]}


def _safe(f, e):
    try:
        f(e)
        return True
    except KeyError:
        return False


rec("EVT:L01", _safe(_new_reader, {"ma": 1, "tien": 5}) and _safe(_old_reader, {"ma": 1, "tien": 5, "ghi_chu": "x"}) and not _safe(_old_reader, {"ma": 2}),
    "thêm trường tuỳ chọn an toàn hai chiều; xoá trường bắt buộc làm hỏng người nhận cũ")


def _dlq(n, poison, max_retry):
    done = dead = 0
    for i in range(1, n + 1):
        if i == poison:
            if max_retry is None:
                return done, dead
            dead += 1
            continue
        done += 1
    return done, dead


rec("EVT:L02", _dlq(1000, 10, None) == (9, 0) and _dlq(1000, 10, 3) == (999, 1), "thử mãi: 9; có kênh thư chết: 999 + 1")
_arr = [1, 3, 2]
_cur = 0
for _ver in _arr:
    _cur = max(_cur, _ver)
rec("EVT:L03", _arr[-1] == 2 and _cur == 3, "ghi đè ngây thơ → 2; theo phiên bản → 3")
rec("EVT:L04", sum([100, -30, 50, -20]) == 100 and max(i % 1000 for i in range(10 ** 6)) == 999, "số dư 100; phát lại tối đa 999")
rec("EVT:L05", (500 - 400) * 600 == 60000, "trễ 60 000 sau 10 phút")
_steps = ["giữ hàng", "trừ tiền", "giao"]
_comp = {"giữ hàng": "nhả hàng", "trừ tiền": "hoàn tiền"}
rec("EVT:L06", [_comp[s] for s in reversed(_steps[:2])] == ["hoàn tiền", "nhả hàng"], "bù trừ ngược: hoàn tiền, nhả hàng")
_imp = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
_clk = [("a", 5), ("b", 13), ("c", 9)]
rec("EVT:L07", sum(1 for k, t in _clk if 0 <= t - _imp[k] <= 10) == 2, "2 cặp khớp trong 10 phút")
rec("EVT:L08", (1200 - 1000) * 3600 == 720000 and 720000 / (1500 - 1200) == 2400, "tồn 720 000; xả 2400 s")
_pos = _now = _t = 0.0
_now = 30.0
while _pos < _now - 1e-9:  # mô phỏng từng nửa ngày: phát lại 5 ngày dữ liệu mỗi ngày, dữ liệu mới vẫn đến 1 ngày mỗi ngày
    _pos, _now, _t = _pos + 5 * 0.5, _now + 0.5, _t + 0.5
rec("EVT:L09", 30 / 5 == 6 and 30 / (5 - 1) == 7.5 == _t, "riêng tồn: 6 ngày; đuổi kịp hiện tại (mô phỏng): 7,5 ngày")
rec("EVT:L10", 10 + max(20, 50) + 30 == 90, "90 ms")
rec("EVT:L11", round(10**9 / 86400) == 11574 and 400_000 // 50_000 == 8 and [1 + 1, 2 * 1 + 1] == [2, 3]
    and round(800e9 / 86400 / 1e6, 2) == 9.26 and [n - (n // 2 + 1) for n in (3, 5)] == [1, 2]
    and (__import__("datetime").date(2025, 3, 18) - __import__("datetime").date(2019, 10, 30)).days == 1966,
    "11 574 tin/giây; gấp 8; 2 so với 3 bản; 9,26 triệu tin/giây; 3 nút chịu 1, 5 nút chịu 2; 1966 ngày")

# ══════════ 2026-10-30: PAR, RLN, CVI, GFX, IRS, HCI, SEP, CAS — mỗi con số trong `example` tính lại bằng cách độc lập ══════════
import datetime as _dt
import itertools as _it
import math as _m
from fractions import Fraction as _Fr

import numpy as _np
import sympy as _sp


def _amdahl(p, n):
    return 1 / ((1 - p) + p / n)


rec("PAR:L00", round(_amdahl(0.9, 16), 2) == 6.4 and abs(1 / (1 - 0.9) - 10) < 1e-9, "16 lõi 6,4 lần; tối đa 10")
_s1 = _Fr(1, 10) / (_Fr(1, 10) + _Fr(9, 10) * 16)  # tỉ lệ tuần tự của bài toán đã phóng to, đo trên MỘT lõi
rec("PAR:L01", round(0.1 + 0.9 * 16, 2) == 14.5 and round(14.5 / 16 * 100, 1) == 90.6 and round(6.4 / 16 * 100) == 40
    and round(float(_s1) * 100, 2) == 0.69 and 1 / ((_s1) + (1 - _s1) / 16) == _Fr(29, 2),
    "Gustafson 14,5 (90,6%) so với 6,4 (40%); đổi sang cách đo Amdahl: 0,69% tuần tự, Amdahl cho đúng 14,5")


def _tree_sum(n):  # đếm phép cộng và số tầng của cây cộng thật
    vals, adds, depth = list(range(n)), 0, 0
    while len(vals) > 1:
        nxt = []
        for i in range(0, len(vals) - 1, 2):
            nxt.append(vals[i] + vals[i + 1]); adds += 1
        if len(vals) % 2:
            nxt.append(vals[-1])
        vals, depth = nxt, depth + 1
    return adds, depth


_w, _s = _tree_sum(1024)
_greedy, _lvl = 0, 1024
while _lvl > 1:  # lịch tham lam: mỗi tầng ceil(số phép cộng / 32) bước
    _greedy, _lvl = _greedy + -(-(_lvl // 2) // 32), _lvl // 2 + _lvl % 2
rec("PAR:L02", (_w, _s) == (1023, 10) and round(1023 / 32 + 10, 2) == 41.97 and round(1023 / 10) == 102 and _greedy == 36
    and round(10 + (1023 - 10) / 32, 2) == 41.66 and round(1023 / 32, 2) == 31.97,
    "công việc 1023, đường găng 10, cận Brent ≈ 41,66, dạng gọn ≈ 41,97, lịch tham lam thật 36 bước, cận dưới 31,97, song song ≈ 102")


def _interleavings():  # 2 luồng × 2 lần (đọc, ghi) → mọi thứ tự giữ thứ tự trong từng luồng
    ops = [("A", k) for k in range(4)] + [("B", k) for k in range(4)]
    results = set()
    for pos in _it.combinations(range(8), 4):
        seq = [None] * 8
        ai = iter(range(4)); bi = iter(range(4))
        for i in range(8):
            seq[i] = ("A", next(ai)) if i in pos else ("B", next(bi))
        x, reg = 0, {}
        for t, k in seq:
            if k % 2 == 0:
                reg[t] = x
            else:
                x = reg[t] + 1
        results.add(x)
    return results


rec("PAR:L03", _interleavings() == {2, 3, 4} and (0.1 + 0.2) + 0.3 == 0.6000000000000001 and 0.1 + (0.2 + 0.3) == 0.6, "biến đếm 2/3/4; cộng dấu phẩy động không kết hợp")
_jobs = [8, 7, 6, 5, 4, 3, 2, 1]
_lpt = [0, 0]
for _j in sorted(_jobs, reverse=True):
    _lpt[_lpt.index(min(_lpt))] += _j
rec("PAR:L04", (sum(_jobs[:4]), sum(_jobs[4:])) == (26, 10) and sorted(_lpt) == [18, 18], "chia nửa: 26 | 10; việc dài trước: 18 | 18")
rec("PAR:L05", 64 // 8 == 8 and 8 * 64 == 512, "8 biến một dòng; đệm → 512 byte")
rec("PAR:L06", 256 // 32 == 8 and divmod(1003, 8) == (125, 3), "8 phần tử mỗi lệnh; 125 lệnh + 3")
_n = 4096
rec("PAR:L07", 10e12 / 1e12 == 10 and round(1e12 * (1 / 12) / 1e9, 1) == 83.3 and round(83.3e9 / 10e12 * 100, 2) == 0.83
    and round(2 * _n ** 3 / (3 * _n * _n * 4), 1) == 682.7, "điểm gãy 10; cộng vector 83,3 tỉ (0,83%); nhân ma trận 682,7 phép/byte")


def _warp_passes(branch):  # số lượt khi các luồng trong nhóm rẽ nhánh khác nhau
    return len(set(branch))


def _transactions(stride, threads=32, word=4, seg=128):
    return len({(t * stride * word) // seg for t in range(threads)})


rec("PAR:L08", _warp_passes(["A"] * 16 + ["B"] * 16) == 2 and 32 * 4 == 128 and _transactions(1, seg=32) == 4 and _transactions(32, seg=32) == 32
    and len({(4 + 4 * _t) // 32 for _t in range(32)}) == 5 and _Fr(128, 32 * 32) == _Fr(1, 8),
    "hai lượt, 50%; liền nhau 4 giao dịch 32 byte; bước 32 → 32 (12,5%); lệch 4 byte → 5")
rec("PAR:L09", 2 * 1024 ** 3 == 2147483648 and 2 * 1024 ** 3 // 32 == 67108864 and 3 * 32 * 32 * 4 == 12288, "2,15 tỉ → 67 108 864; 12 288 byte")


def _ring_bytes(p, N):  # mô phỏng: reduce-scatter p − 1 bước + all-gather p − 1 bước, mỗi bước gửi N/p
    return 2 * (p - 1) * _Fr(N, p)


rec("PAR:L10", _ring_bytes(8, 1) == _Fr(7, 4) and 8 * 1 == 8, "vòng 1,75 GB; máy chủ tham số 8 GB")
rec("PAR:L11", round(100 / 130 * 100, 1) == 76.9 and round(100 / 110 * 100, 1) == 90.9, "76,9% và 90,9%")
rec("PAR:L12", round(_amdahl(0.75, 8), 2) == 2.91 and round(_amdahl(0.98, 8), 2) == 7.02 and round(_amdahl(0.75, 16), 2) == 3.37, "2,91; 7,02; 16 GPU 3,37")
rec("PAR:L13", round(63 / 14.8, 2) == 4.26 and 24 * 32 == 768 and 14 * 8 == 112 and 12288 // 768 == 16 and 8192 // 256 == 32
    and [round(90 * 1.2e6 / (d * 86400)) for d in (6, 5)] == [208, 250]
    and round(29 * 8 / 256, 3) == 0.906 and round(29 * 8 / 256 / 0.9, 3) == 1.007 and round(0.1 * 8192 / 256, 6) == 3.2
    and round(0.88 / 0.50, 2) == 1.76 and round(float(_ring_bytes(128, 1)), 2) == 1.98,
    "4,26 lần; 768 luồng, 112 lõi, 16 cụm; 32 ảnh mỗi thẻ; 208–250 ảnh/giây; 0,906 → 1,007 giờ; tốc độ học 3,2; 1,76 lần; 1,98 lần dung lượng")

# ── RLN ──
_G = sum(0.9 ** k for k in range(2000))
rec("RLN:L00", abs(_G - 10) < 1e-6 and round(0.9 ** 2 * 10, 10) == 8.1, "G = 10; 8,1")
_VA, _VB = _sp.symbols("VA VB")
_sol = _sp.solve([_sp.Eq(_VA, 1 + _sp.Rational(9, 10) * _VB), _sp.Eq(_VB, _sp.Rational(9, 10) * _VA)], [_VA, _VB])
rec("RLN:L01", _sol[_VA] == _sp.Rational(100, 19) and round(float(_sol[_VA]), 3) == 5.263 and round(float(_sol[_VB]), 3) == 4.737, "V(A) = 100/19 ≈ 5,263; V(B) ≈ 4,737")
rec("RLN:L02", _m.ceil(_m.log(0.001) / _m.log(0.9)) == 66 and round(_m.log(0.001) / _m.log(0.9), 1) == 65.6 and _m.ceil(_m.log(0.001) / _m.log(0.99)) == 688, "66 vòng; γ = 0,99: 688")
rec("RLN:L03", abs(0.9 + 0.1 / 10 - 0.91) < 1e-12 and abs(0.1 / 10 - 0.01) < 1e-12, "0,91 và 0,01")
rec("RLN:L04", sum([4, 6, 8]) / 3 == 6 and 6 + 0.5 * (1 + 0.9 * 10 - 6) == 8, "Monte Carlo 6; TD 8")
rec("RLN:L05", round(2 + 0.1 * (-1 + 5 - 2), 10) == 2.2 and round(2 + 0.1 * (-1 + 1 - 2), 10) == 1.8, "Q-learning 2,2; SARSA 1,8")
rec("RLN:L06", round(1 + 0.99 * 10, 10) == 10.9, "mục tiêu 10,9")
_est = [10 * 0.5, 12 * (-0.5)]
_estb = [(10 - 11) * 0.5, (12 - 11) * (-0.5)]
_var = lambda xs: sum(x * x for x in xs) / 2 - (sum(xs) / 2) ** 2
rec("RLN:L07", _est == [5, -6] and _var(_est) == 30.25 and _estb == [-0.5, -0.5] and _var(_estb) == 0 and sum(_est) / 2 == sum(_estb) / 2 == -0.5, "phương sai 30,25 → 0, kỳ vọng −0,5")
rec("RLN:L08", round(1 + 0.9 * 5 - 4, 10) == 1.5, "lợi thế 1,5")
_clipobj = lambda r, A, e=0.2: min(r * A, max(1 - e, min(r, 1 + e)) * A)
rec("RLN:L09", round(_clipobj(1.5, 2), 10) == 2.4 and round(_clipobj(0.5, -2), 10) == -1.6, "2,4 và −1,6")
_sig = lambda z: 1 / (1 + _m.exp(-z))
rec("RLN:L10", round(_sig(1), 3) == 0.731 and _sig(0) == 0.5 and round(-_m.log(_sig(1)), 3) == 0.313, "σ(1) ≈ 0,731; mất mát 0,313")


def _boat(policy, T=1000):  # mô phỏng: về đích sau 100 bước +100 rồi dừng; hay quay vòng ăn mốc mỗi 5 bước +1
    if policy == "ve_dich":
        return 100
    return sum(1 for t in range(1, T + 1) if t % 5 == 0)


rec("RLN:L11", _boat("vong") == 200 and _boat("ve_dich") == 100, "quay vòng 200 > về đích 100")
rec("RLN:L12", round(0.9 / 0.1) == 9 and 2 ** 10 == 1024, "trọng số 9; tích 1024")
_hns = lambda a, rnd, hum: (a - rnd) / (hum - rnd)
rec("RLN:L13", round(200e6 / 60 / 86400, 1) == 38.6 and round(50e6 * 4 / 60 / 86400, 1) == 38.6
    and round(100 * _hns(-3272, -17098.1, -4336.9), 1) == 108.3, "200 triệu khung ≈ 38,6 ngày = 50 triệu bước × 4; Skiing tối đa 108,3%")

# ── CVI ──
rec("CVI:L00", 1920 * 1080 * 3 == 6220800 and round(6220800 / 2 ** 20, 2) == 5.93 and round(6220800 * 30 / 1e6, 1) == 186.6, "6 220 800 byte; 186,6 triệu byte/s")
_sob = _np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
_patch = _np.array([[0, 0, 10]] * 3)
rec("CVI:L01", int((_sob * _patch).sum()) == 40 and int((_sob * _np.full((3, 3), 7)).sum()) == 0, "Sobel 40; vùng phẳng 0")
_px = [10, 10, 12, 50, 52, 55]


def _otsu(vals):
    best = None
    for t in sorted(set(vals))[:-1]:
        a = [v for v in vals if v <= t]; b = [v for v in vals if v > t]
        wa, wb = len(a) / len(vals), len(b) / len(vals)
        between = wa * wb * (sum(a) / len(a) - sum(b) / len(b)) ** 2
        if best is None or between > best[0]:
            best = (between, t)
    return best[1]


rec("CVI:L02", _otsu(_px) == 12, "ngưỡng tách {10, 10, 12} | {50, 52, 55}")
rec("CVI:L03", 800 * 0.5 / 2 + 320 == 520 and 800 * 0.25 / 2 + 240 == 340, "u = 520, v = 340")
rec("CVI:L04", 0.3 / 0.5 == 0.6 < 0.8 and round(0.45 / 0.5, 2) == 0.9 > 0.8, "0,6 giữ; 0,9 bỏ")
_ransac = lambda w, s=4, p=0.99: _m.ceil(_m.log(1 - p) / _m.log(1 - w ** s))
rec("CVI:L05", _ransac(0.5) == 72 and _ransac(0.3) == 567, "72 lần; 30% → 567")
_Z = lambda d: 700 * 0.12 / d
rec("CVI:L06", round(_Z(42), 6) == 2 and round(_Z(43), 2) == 1.95 and round(_Z(41), 2) == 2.05 and round(700 * 0.12 / 8, 1) == 10.5
    and round(_Z(9.5) - 8, 2) == 0.84 and round(8 - _Z(11.5), 2) == 0.70, "Z = 2 m; ±1 px → 1,95/2,05; ở 8 m chênh 10,5, lệch 0,70–0,84 m")


def _iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    area = lambda r: (r[2] - r[0]) * (r[3] - r[1])
    return inter, area(a) + area(b) - inter


_seg = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}
_seg_map = lambda d, m: next((k for k, v in _seg.items() if set(v) == {m[c] for c in _seg[d]}), None)
_flip = dict(zip("abcdefg", "afedcbg")); _rot = dict(zip("abcdefg", "defabcg"))
rec("CVI:L07", 512 * 10 + 10 == 5130 and _seg_map(2, _flip) == 5 and _seg_map(6, _rot) == 9 and _seg_map(6, _flip) is None,
    "5130 tham số; bảy đoạn: lật ngang 2 → 5, xoay 180° 6 → 9 (sửa 2026-11-03: giáo án cũ ghi “lật ngang 6 vẫn là 6” — sai, ra hình không phải chữ số)")
_i1, _u1 = _iou((0, 0, 10, 10), (5, 5, 15, 15)); _i2, _u2 = _iou((0, 0, 10, 10), (1, 0, 11, 10))
rec("CVI:L08", (_i1, _u1) == (25, 175) and round(_i1 / _u1, 3) == 0.143 and (_i2, _u2) == (90, 110) and round(_i2 / _u2, 3) == 0.818, "IoU 0,143; 0,818")
_iou_s, _dice = 40 / 60, 80 / 100
rec("CVI:L09", round(_iou_s, 3) == 0.667 and _dice == 0.8 and abs(2 * _iou_s / (1 + _iou_s) - _dice) < 1e-12 and 99 / 100 == 0.99, "IoU 0,667, Dice 0,8 = 2IoU/(1 + IoU)")
rec("CVI:L10", (900 * 0.95 + 100 * 0.5) / 1000 == 0.905 and 0.5 * 0.95 + 0.5 * 0.5 == 0.725, "chung 90,5%; triển khai 72,5%")
_rng = _np.random.default_rng(7)
_cow = _rng.random(100000) < 0.5
_grass = _np.where(_cow, _rng.random(100000) < 0.95, _rng.random(100000) < 0.05)
_acc = float(((_grass) == _cow).mean())
_err = {2010: _Fr("28.2"), 2012: _Fr("16.4"), 2014: _Fr("6.7"), 2015: _Fr("3.57"), 2017: _Fr("2.251")}
rec("CVI:L12", round(float(_err[2010] / _err[2014]), 1) == 4.2 and _err[2010] * 1000 == 28200 and _err[2014] * 1000 == 6700
    and _err[2010] * 1500 == 42300 and _err[2015] < _Fr("5.1") and round(float(_err[2012] / _err[2014]), 1) == 2.4 and all(a > b for a, b in zip(list(_err.values()), list(_err.values())[1:])),
    "28,2% → 6,7%: 4,2 lần; 28 200 → 6 700 ảnh sai / 100 000; 3,57% < 5,1%; 16,4 → 6,7: 2,4 lần (CITED Russakovsky 2015: “4.2x”, “2.4x”)")
rec("CVI:L11", abs(_acc - 0.95) < 0.005, f"mô phỏng 100 000 ảnh: luật “có cỏ ⇒ bò” đúng {_acc:.3f}; bò trên bãi biển (không cỏ) luôn bị đoán “không bò”")

# ── GFX ──
rec("GFX:L00", 1920 * 1080 * 60 == 124416000 and round(1000 / 60, 2) == 16.67 and round(1000 / 120, 2) == 8.33, "124 416 000 điểm ảnh/s; 16,67 ms; 8,33 ms")
_R90 = _np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]); _T = _np.array([[1, 0, 2], [0, 1, 0], [0, 0, 1]]); _pt = _np.array([1, 0, 1])
rec("GFX:L01", list((_T @ _R90 @ _pt)[:2]) == [2, 1] and list((_R90 @ _T @ _pt)[:2]) == [0, 3], "quay rồi tịnh tiến (2, 1); ngược lại (0, 3)")
rec("GFX:L02", (2 / 4, 1 / 4) == (0.5, 0.25) and (2 / 8, 1 / 8) == (0.25, 0.125), "(0,5; 0,25) và (0,25; 0,125)")
_vp = lambda x: (x + 1) / 2 * 1920
rec("GFX:L03", _vp(0.5) == 1440 and _vp(-1) == 0 and _vp(1) == 1920, "1440; 0; 1920")


def _bary(p, a, b, c):
    M = _np.array([[a[0], b[0], c[0]], [a[1], b[1], c[1]], [1, 1, 1]], dtype=float)
    return _np.linalg.solve(M, _np.array([p[0], p[1], 1.0]))


_b1 = _bary((1, 1), (0, 0), (4, 0), (0, 4)); _b2 = _bary((3, 3), (0, 0), (4, 0), (0, 4))
rec("GFX:L04", _np.allclose(_b1, [0.5, 0.25, 0.25]) and (_b2 < 0).any(), "(0,5; 0,25; 0,25) bên trong; (3, 3) bên ngoài")


def _dz(z, n, f, bits=24):  # khoảng z ứng với một bước lượng tử của độ sâu d = f(z − n)/(z(f − n))
    return z * z * (f - n) / (f * n * 2 ** bits)


rec("GFX:L05", round(_dz(100, 0.1, 1000) * 1000, 1) == 6.0 and round(_dz(100, 1, 1000) * 1000, 1) == 0.6, "≈ 6 mm; gần = 1 → ≈ 0,6 mm")
_nv = _np.array([0, 0, 1.0]); _lv = _np.array([0, 0.6, 0.8])
rec("GFX:L06", round(float(_nv @ _lv), 10) == 0.8 and round(0.95 ** 32, 3) == 0.194 and round(0.95 ** 128, 4) == 0.0014, "0,8; 0,194; 0,0014")
_bil = (1 - 0.5) * (1 - 0.5) * 10 + 0.5 * (1 - 0.5) * 20 + (1 - 0.5) * 0.5 * 30 + 0.5 * 0.5 * 40
_levels = int(_m.log2(1024)) + 1
_extra = sum((1024 >> k) ** 2 for k in range(1, _levels)) / 1024 ** 2
rec("GFX:L07", _bil == 25 and _levels == 11 and abs(_extra - 1 / 3) < 0.001, "25; 11 mức; thêm ≈ 1/3")
_to_lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
_to_srgb = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
rec("GFX:L08", round((0 + 255) / 2) == 128 and round(_to_srgb((_to_lin(0) + _to_lin(1)) / 2) * 255) == 188, "thẳng 128; đúng ≈ 188")
_t = _sp.symbols("t")
_roots = sorted(_sp.solve(_sp.Eq((0 - 0) ** 2 + (0 - 0) ** 2 + (_t - 5) ** 2, 1), _t))
_disc = (2 * _np.dot([0, 1, 0], [0, 0, -5])) ** 2 - 4 * 1 * (25 - 1)
rec("GFX:L09", _roots == [4, 6] and _disc < 0, "t = 4, 6; hướng (0, 1, 0) không giao")
_schlick = lambda c, F0=0.04: F0 + (1 - F0) * (1 - c) ** 5
rec("GFX:L10", _schlick(1) == 0.04 and round(_schlick(0.5), 2) == 0.07 and _schlick(0) == 1, "0,04; 0,07; 1")
rec("GFX:L11", 1920 * 1080 * 3 == 6220800 and 1920 * 1080 == 2073600, "6 220 800 → 2 073 600 mảnh")
rec("GFX:L12", round(_dz(1000, 0.01, 10000), 1) == 6.0 and round(_dz(1000, 0.5, 10000), 2) == 0.12 and round(_dz(1000, 0.01, 100000) / _dz(1000, 0.01, 10000), 3) == 1.0,
    "≈ 6 m; gần 0,5 → ≈ 0,12 m; xa ×10 gần như không đổi")

rec("GFX:L13", round(0.95 ** 32, 3) == 0.194 and 10 ** 2 == 100 and round(((1.5 - 1) / (1.5 + 1)) ** 2, 4) == 0.04 and round(_schlick(0.5), 2) == 0.07 and 0.5 ** 2 == 0.25 and round(1 - 0.07, 2) == 0.93, "0,194; 100 lần tia; F0=0,04; F=0,07; alpha=0,25")

# ── IRS ──
_rel = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
rec("IRS:L00", sum(_rel[:5]) / 5 == 0.4 and sum(_rel[:5]) / 5 == 0.4 and 1 / (_rel.index(1) + 1) == 1 and 1 / 3 == 1 / ([0, 0, 1].index(1) + 1), "P@5 0,4; R@5 0,4; RR 1 (hoặc 1/3)")
_dcg = lambda g: sum(x / _m.log2(i + 2) for i, x in enumerate(g))
rec("IRS:L01", round(_dcg([3, 2, 0, 1]), 3) == 4.693 and round(_dcg([3, 2, 1, 0]), 3) == 4.762 and round(_dcg([3, 2, 0, 1]) / _dcg([3, 2, 1, 0]), 3) == 0.985, "DCG 4,693; lý tưởng 4,762; nDCG 0,985")
# dạng gốc Järvelin–Kekäläinen 2002 (b = 2: vị trí i < b không chiết khấu, từ i ≥ b chia log_b i) — khác 0,985, nên “chỉ so khi cùng công thức”
_dcg_jk = lambda g, b=2: sum(x if i + 1 < b else x / _m.log(i + 1, b) for i, x in enumerate(g))
rec("IRS:L01", _dcg_jk([3, 2, 0, 1]) == 5.5 and round(_dcg_jk([3, 2, 0, 1]) / _dcg_jk([3, 2, 1, 0]), 3) == 0.977
    and [round(_dcg_jk([3, 2, 3, 0, 0, 1, 2, 2, 3, 0][:n]), 2) for n in (1, 2, 3, 6)] == [3, 5, 6.89, 7.28], "dạng 2002: 5,5; nDCG 0,977 ≠ 0,985; ví dụ bài báo 3, 5, 6,89, 7,28")
rec("IRS:L02", round(_m.log(3 / 1), 3) == 1.099 and _m.log(3 / 3) == 0, "idf 1,099 và 0")
_cosv = lambda u, v: sum(a * b for a, b in zip(u, v)) / _m.sqrt(sum(a * a for a in u) * sum(b * b for b in v))
rec("IRS:L02", round(_m.log(10 / 3), 3) == 1.204 and _cosv([0, 0, 1, 0], [0, 0, 5 * _m.log(1.5), 0]) == 1
    and abs(_cosv([0, _m.log(3), 0, 0], [0, 2 * _m.log(3), 0, 0]) - 1) < 1e-12, "kho 10: idf(máy) 1,204; nhồi từ khoá cosin 1; nhân bản cosin không đổi")
rec("IRS:L03", 1000 + 10 * (10 ** 6 // 1000) == 11000 and round(10 ** 6 / 11000) == 91, "11 000 phép, ≈ 91 lần")
rec("IRS:L04", round(1 / 61 + 1 / 63, 5) == 0.03227 and round(1 / 62 + 1 / 61, 5) == 0.03252, "A 0,03227 < B 0,03252")
rec("IRS:L05", round(_m.log(1 + _m.exp(-0.5)), 3) == 0.474 and round(_m.log(1 + _m.exp(0.5)), 3) == 0.974, "0,474 và 0,974")
_U, _V = _np.array([5, 3, 0.0]), _np.array([4, 0, 4.0])
_W6 = _np.array([1, 2, 5.0])
_c_uv = round(float(_U @ _V / (_np.linalg.norm(_U) * _np.linalg.norm(_V))), 3)
_c_uw = round(float(_U @ _W6 / (_np.linalg.norm(_U) * _np.linalg.norm(_W6))), 3)
rec("IRS:L06", float(_U @ _V) == 20 and _c_uv == 0.606 and _c_uw == 0.344 and round((_c_uv * 4 + _c_uw * 5) / (_c_uv + _c_uw), 2) == 4.36,
    "cosin(U, V) ≈ 0,606, cosin(U, W) ≈ 0,344; dự đoán (0,606·4 + 0,344·5)/0,950 ≈ 4,36 (đồng bộ ví dụ giáo án, đợt C)")
_p, _q = _np.array([1, 2.0]), _np.array([0.5, 1.0])
_e = 3 - float(_p @ _q)
rec("IRS:L07", float(_p @ _q) == 2.5 and _e == 0.5 and _np.allclose(_p + 0.1 * _e * _q, [1.025, 2.05]), "dự đoán 2,5; p mới (1,025; 2,05)")
rec("IRS:L08", round(100 ** 0.75, 1) == 31.6, "100^0,75 ≈ 31,6")
rec("IRS:L09", _Fr(1, 2) == _Fr(1, 1 + 1) and round(51 / (51 + 951), 4) == 0.0509, "Beta(1, 1) 0,5; Beta(51, 951) 0,0509")
rec("IRS:L10", 10 / 0.2 == 50, "50 lượt bấm điều chỉnh")
# ── IRS: các số mới trong ví dụ giáo án sau đợt đọc kiểm C (2026-11-09), tính lại độc lập ──
_relB = [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
rec("IRS:L00", sum(_rel) / 5 == 0.6 and sum(_relB[:5]) / 5 == 0.4 and sum(_relB[:3]) == 0 and 1 / (_relB.index(1) + 1) == 0.25
    and _Fr(1 + _Fr(1, 3) + 0, 3) == _Fr(4, 9) and round(4 / 9, 3) == 0.444, "R@10 = 3/5 = 0,6; hệ B: P@5 0,4, P@3 0, RR 1/4; MRR (1 + 1/3 + 0)/3 = 4/9 ≈ 0,444")
rec("IRS:L01", round(_dcg([3, 2, 0, 1]), 5) == 4.69254 and round(_dcg([3, 2, 1, 0]), 5) == 4.76186 and round(_dcg([3, 2, 0, 1]) / _dcg([3, 2, 1, 0]), 5) == 0.98544
    and round(4.693 / 4.762, 3) == 0.986, "DCG 4,69254 / IDCG 4,76186 = 0,98544 ≈ 0,985; chia hai số đã làm tròn ra 0,986")
def _irs_cos(a, b):
    na, nb = _m.sqrt(sum(x * x for x in a)), _m.sqrt(sum(x * x for x in b))
    return 0.0 if not na or not nb else sum(x * y for x, y in zip(a, b)) / (na * nb)
_idf = {"máy": _m.log(3 / 3), "ổ": _m.log(3 / 1), "pin": _m.log(3 / 2), "màn": _m.log(3 / 1)}
_vec = lambda words, w: [words.count(t) * (w[t] if w else 1) for t in ("máy", "ổ", "pin", "màn")]
_q2, _d1, _d2, _d3 = "máy pin".split(), "máy ổ máy".split(), "máy pin".split(), "máy pin màn".split()
rec("IRS:L02", round(_idf["pin"], 3) == 0.405 and round(_irs_cos(_vec(_q2, _idf), _vec(_d2, _idf)), 3) == 1 and round(_irs_cos(_vec(_q2, _idf), _vec(_d3, _idf)), 3) == 0.346
    and _irs_cos(_vec(_q2, _idf), _vec(_d1, _idf)) == 0 and round(_irs_cos(_vec(_q2, None), _vec(_d1, None)), 3) == 0.632,
    "idf(pin) = ln 1,5 ≈ 0,405; cosin d2 = 1, d3 ≈ 0,346, d1 = 0; đếm thô không độ hiếm d1 ≈ 0,632")
_g = [3, 2, 1, 0]
rec("IRS:L05", round(_dcg(_g) - _dcg([2, 3, 1, 0]), 3) == 0.369 and round(_dcg(_g) - _dcg([3, 2, 0, 1]), 3) == 0.069,
    "đổi chỗ vị trí 1 và 2 mất ≈ 0,369 độ lợi có chiết khấu; vị trí 3 và 4 mất ≈ 0,069")
_pn, _qn = _p + 0.1 * _e * _q, _q + 0.1 * _e * _p
rec("IRS:L07", _np.allclose(_qn, [0.55, 1.1]) and round(float(_pn @ _qn), 3) == 2.819 and _np.allclose(_p + 0.1 * (_e * _q - 0.1 * _p), [1.015, 2.03]),
    "q mới (0,55; 1,1); đoán lại ≈ 2,819; thêm λ = 0,1 → p mới (1,015; 2,03)")
rec("IRS:L08", round(1 / 101, 3) == 0.010 and round(1 / (100 ** 0.75 + 1), 3) == 0.031 and round((1 / (100 ** 0.75 + 1)) / (1 / 101)) == 3
    and round(-_m.log(0.02), 3) == 3.912, "B được 1/101 ≈ 0,010; mũ 0,75 → 1/(31,62 + 1) ≈ 0,031, gấp ≈ 3 lần; −ln 0,02 ≈ 3,912")
_bsd = lambda a, b: _m.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
rec("IRS:L09", round(_bsd(1, 1), 3) == 0.289 and round(_bsd(51, 951), 4) == 0.0069 and round(1 - 51 / 1002, 3) == 0.949,
    "Beta(1, 1) độ lệch chuẩn ≈ 0,289; Beta(51, 951) ≈ 0,0069; P(mẫu Beta(1, 1) > mẫu Beta(51, 951)) = 1 − 51/1002 ≈ 0,949")
rec("IRS:L13", round(4.1 / 0.2) == 20, "bỏ trọng số thời gian xem: mất mát +4,1% ≈ 20 lần mức 0,2% (số CITED CO16, chỉ tính lại tỉ số)")
rec("IRS:L10", round(0.01 / 0.2, 2) == 0.05 > 0.03, "B 0,01/0,2 = 0,05 > A 0,03: B liên quan hơn")
rec("IRS:L03", _cl.irs_ivf_sim()[0][:2] == (1, 0.804) and _cl.irs_ivf_sim()[2][:2] == (4, 1.0), "mô phỏng 5000 điểm: xét 1 cụm độ phủ 0,804, xét 4 cụm đạt 1")
_mmr = lambda rel, sim, lam=0.7: lam * rel - (1 - lam) * sim
_disc = [1 / _m.log2(i + 1) for i in (1, 2, 3, 4)]
rec("IRS:L11", round(_mmr(0.9, 0.8), 2) == 0.39 and round(_mmr(0.7, 0.1), 2) == 0.46
    and round(sum(_disc), 3) == 2.562 and round((_disc[2] + _disc[3]) / sum(_disc) * 100, 1) == 36.3,
    "X 0,39 < Y 0,46; vị trí 3 và 4 nhận (0,5 + 0,431)/2,562 ≈ 36,3% mức được nhìn thấy (chiết khấu 1/log₂(i + 1))")
rec("IRS:L12", 10 + 1000 * 0.05 + 20 == 80 and 10000 * 0.05 == 500 and 15 + 70 + 30 == 115 and round(70 / 1000 * 600) == 42 and 15 + 42 + 30 == 87 < 100,
    "80 ms; 10 000 ứng viên → 500 ms; phân vị 99: 15 + 70 + 30 = 115 ms → 600 ứng viên: 15 + 42 + 30 = 87 ms")
# L13 hành trình (con số CITED ở audit/irs/sources_L13.md; ở đây chỉ tính lại phần suy ra được)
rec("IRS:L13", 7 * 60 * 24 == 10080 and round(12.5 / 1.1, 1) == 11.4 and 10 ** 6 * 256 * 4 == 1024000000
    and round(1 / 50, 2) == 0.02 and round(-_m.log(1 / 50), 3) == 3.912 and 0.24 > 0 > -0.07 and 90 + 5 + 5 == 100,
    "10 080 giờ/ngày; 11,4 lượt/người; 1 024 000 000 byte; p = 0,02, −ln p ≈ 3,912; 90/5/5")

# ── HCI ──
rec("HCI:L00", (8 * 60 + 45) - (8 * 60 + 7) == 38, "8:07 → 8:45 = 38 phút (FCC)")
rec("HCI:L01", _m.factorial(4) == 24, "24 cách ghép")
_fitts = lambda D, W, a=0.1, b=0.15: a + b * _m.log2(D / W + 1)
rec("HCI:L02", round(_m.log2(17), 2) == 4.09 and round(_fitts(256, 16), 3) == 0.713 and round(_m.log2(5), 2) == 2.32 and round(_fitts(256, 64), 3) == 0.448, "0,713 s; 0,448 s")
rec("HCI:L03", round(0.2 * _m.log2(16), 3) == 0.8 and round(0.2 * _m.log2(4) + 0.2 * _m.log2(6), 3) == 0.917, "phẳng 0,8 s; hai cấp 0,917 s")
rec("HCI:L04", len("482913") == 6 and len("482 913".split()) == 2, "6 đơn vị → 2 nhóm")
_K = dict(K=0.2, P=1.1, B=0.1, H=0.4, M=1.35)
_mouse = _K["H"] + _K["M"] + _K["P"] + 2 * _K["B"] + _K["M"] + _K["P"] + 2 * _K["B"]
rec("HCI:L05", round(_mouse, 2) == 5.7 and round(_K["M"] + 2 * _K["K"], 2) == 1.75, "chuột 5,7 s; phím tắt 1,75 s")
rec("HCI:L06", round(1 - 0.69 ** 5, 3) == 0.844 and round(1 - 0.69 ** 15, 3) == 0.996, "5 người 84,4%; 15 người 99,6%")
_ans = [4, 2, 4, 1, 5, 2, 4, 2, 4, 1]
_odd = sum(x - 1 for x in _ans[0::2]); _even = sum(5 - x for x in _ans[1::2])
rec("HCI:L07", (_odd, _even) == (16, 17) and (_odd + _even) * 2.5 == 82.5, "16 + 17 → 82,5")
_latin = ["ABC", "BCA", "CAB"]
rec("HCI:L08", _m.factorial(3) == 6 and all(sorted(r[i] for r in _latin) == ["A", "B", "C"] for i in range(3)), "6 thứ tự; Latin mỗi vị trí đúng 1 lần")
rec("HCI:L09", round(_fitts(200, 24), 3) == 0.583 and round(_fitts(200, 44), 3) == 0.471, "24 px 0,583 s; 44 px 0,471 s")
rec("HCI:L10", abs(1 / 1000 * 0.01 - 1 / 100000) < 1e-15, "1/1000 × 1% = 1/100 000")
rec("HCI:L11", (8 * 60 + 44) - (8 * 60 + 31) == 13 and (8 * 60 + 45) - (8 * 60 + 7) == 38, "soạn đính chính 8:31–8:44; gửi 8:45 = 38 phút")
rec("HCI:L12", 16 + 30 + 19 == 65 and round((1 + 0.05) / (0 + 0.05), 1) == 21.0 and 61 + 17 == 78 and 1280 // 4 == 320 and 44 * 44 == 1936 and 78 - 1 + 9 == 86 and 24 * 24 == 576 and round(1936 / 576, 2) == 3.36, "65 điểm; 21:1; 78 tiêu chí; 320 px; 86 tiêu chí; 576 px²")

# ── SEP ──
rec("SEP:L00", 10 ** 6 // 100 == 10000 and 100 // 100 == 1, "10 000 người; 1 trên 100")
_cells = 365 * 80 * 2
_rng2 = _np.random.default_rng(3)
_draw = _rng2.integers(0, _cells, 10000)
_, _cnt = _np.unique(_draw, return_counts=True)
_uniq = float((_cnt == 1).sum()) / 10000
rec("SEP:L01", _cells == 58400 and round((1 - 1 / 58400) ** 9999, 3) == 0.843 and abs(_uniq - 0.843) < 0.01, f"58 400 tổ hợp; công thức 0,843; mô phỏng {_uniq:.3f}")


def _grp(base, tpr=0.8, fpr=0.1):
    tp, fp = base * tpr, (1 - base) * fpr
    return tp / (tp + fp), tp + fp


_ppvA, _selA = _grp(0.5); _ppvB, _selB = _grp(0.2)
rec("SEP:L02", round(_ppvA, 3) == 0.889 and round(_ppvB, 3) == 0.667 and round(_selA, 2) == 0.45 and round(_selB, 2) == 0.24, "PPV 0,889 / 0,667; chọn 45% / 24%")
_score = lambda inc, yrs: 0.5 * inc + 2 * yrs
rec("SEP:L03", _score(20, 3) == 16 and _score(28, 3) == 20 and _score(20, 5) == 20, "16; +8 triệu hoặc +2 năm → 20")
_LIC = {"MIT": "permissive", "Apache-2.0": "permissive", "GPL-3.0": "copyleft"}
_deps = ["MIT", "MIT", "Apache-2.0", "GPL-3.0"]
rec("SEP:L04", [d for d in _deps if _LIC[d] == "copyleft"] == ["GPL-3.0"] and sum(_LIC[d] == "permissive" for d in _deps) == 3, "3 dễ dãi được; 1 GPL buộc mở mã khi phân phối")
rec("SEP:L05", round(0.001 * 1e6) == 1000 and round(0.1 * 1000) == 100 and round(1 - (1 - 0.001) ** 1000, 3) == 0.632
    and abs((1 - 0.001) ** 1000 - _m.exp(-1)) < 0.001, "kỳ vọng 1000 > 100; 1000 hệ × 0,001/năm → 63,2% có ít nhất 1 sự cố")
rec("SEP:L06", round(8 * 0.4 * 720 * 1.2, 1) == 2764.8 and round(2764.8 * 0.5) == 1382, "2764,8 kWh; ≈ 1382 kg")
_pz0 = _dt.date(2025, 1, 1)
rec("SEP:L07", _pz0 + _dt.timedelta(days=90) == _dt.date(2025, 4, 1) and _pz0 + _dt.timedelta(days=47) == _dt.date(2025, 2, 17)
    and _pz0 + _dt.timedelta(days=47 + 30) == _dt.date(2025, 3, 19) and 31 + 28 + 31 == 90,
    "90+30: báo 1/1 → hạn vá 1/4; vá ngày 47 (17/2) → công bố ngày 77 (19/3)")
_opts = {"X": [2, 2, 2, -2], "Y": [1, 1, 1, 0], "Z": [0, 1, 1, 1]}   # cột: công ty, khách, nhà hàng, tài xế
_ok = [k for k, v in _opts.items() if min(v) >= 0]
_best = max(_ok, key=lambda k: (sum(_opts[k]), _opts[k][3]))   # hoà tổng → ưu tiên bên yếu thế (tài xế)
rec("SEP:L08", all(-2 <= x <= 2 for v in _opts.values() for x in v) and sum(_opts["X"]) == 4 == max(sum(v) for v in _opts.values())
    and 2 * 3 - 2 == 4 and sum(_opts["Y"]) == 3 and sum(_opts["Z"]) == 3 and _best == "Z",
    "X tổng 4 (lớn nhất có thể khi một bên −2) nhưng −2 cho tài xế; Y, Z tổng 3 không bên nào âm; hoà → Z")
rec("SEP:L09", (2 + 4 * 4 + 12) / 6 == 5 and round((12 - 2) / 6, 2) == 1.67, "5 ngày; độ lệch 1,67")
rec("SEP:L10", 1 + 272 == 273 and 3 ** 3 == 27, "kik + 272 gói; 3³ = 27")
rec("SEP:L10", (16 * 60 + 55) - (14 * 60 + 30) == 145 and round(145 / 60, 1) == 2.4 and 3 + 3 ** 2 + 3 ** 3 == 39,
    "14:30 → 16:55 = 145 phút ≈ 2,4 giờ (nguồn ghi 2,5 giờ); 3 + 9 + 27 = 39 gói gián tiếp (số minh hoạ)")
rec("SEP:L00", round(0.99 ** 100, 3) == 0.366 and round(0.99 ** 100 * 100) == 37, "0,99¹⁰⁰ ≈ 0,366 — khoảng 37% khả năng không ai trong 100 người gặp lỗi")
rec("SEP:L04", 4 + 4 * 3 == 16, "4 gói trực tiếp, mỗi gói 3 gói con → kiểm 16 gói (số minh hoạ)")
_sw = 2 * 5 * 365 * 100
_rev = 200e9
rec("SEP:L11", _sw == 365000 and _sw > 54805 and round(216 / 248 * 100) == 87 and 0.05 * _rev == 10e9 > 3e9 and 3e9 / 2 == 1.5e9
    and _dt.date(2026, 1, 1).replace(year=2026 + 5) == _dt.date(2031, 1, 1) and 3 * 24 == 72,
    "365 000 tổ hợp > 54 805 cử tri; 216/248 ≈ 87%; 5% của 200 tỉ = 10 tỉ > 3 tỉ; cá nhân 1,5 tỉ; 1/1/2026 + 5 năm = 1/1/2031; 72 giờ = 3 ngày")

# ── CAS ──
rec("CAS:L00", round(0.1 ** 3, 6) == 0.001, "ba lớp độc lập 0,1%")
_tick = 0.1 - _m.floor(0.1 * 2 ** 23) / 2 ** 23
_drift = lambda h: _tick * h * 3600 * 10
rec("CAS:L01", round(_tick * 1e8, 2) == 9.54 and round(_drift(100), 4) == 0.3433 and round(_drift(8), 4) == 0.0275 and round(_drift(20), 4) == 0.0687,
    "9,54·10⁻⁸ s mỗi nhịp; 100 h 0,3433 s; 8 h 0,0275 s; 20 h 0,0687 s — khớp bảng GAO")
rec("CAS:L02", (-2 ** 15, 2 ** 15 - 1) == (-32768, 32767) and _np.array([32768], dtype=_np.int64).astype(_np.int16)[0] == -32768, "−32 768 … 32 767; 32 768 ép thô thành −32 768")
rec("CAS:L03", round(4.4482216152605, 2) == 4.45 and round(1 / 4.45, 3) == 0.225, "1 lbf = 4,448 N ≈ 4,45")


def _inversion(inherit, low_left=2, med=50):  # mô phỏng ms: thấp giữ khoá còn low_left; vừa sẵn sàng chạy med; cao chờ khoá
    t, low, medr = 0, low_left, med
    while low > 0:
        if inherit or medr == 0:
            low -= 1
        else:
            medr -= 1
        t += 1
    return t


rec("CAS:L04", _inversion(False) == 52 and _inversion(True) == 2, "không kế thừa chờ 52 ms; có kế thừa 2 ms")
rec("CAS:L05", 8 - 7 == 1 and 460 / 45 > 10, "1 máy thiếu; > 10 triệu đô/phút")
rec("CAS:L06", (13 * 60 + 54) - (9 * 60 + 37) == 4 * 60 + 17, "9:37 → 13:54 = 4 giờ 17 phút")


def _bt_steps(n):  # bộ khớp quay lui tự cài cho .*.*=.*, TÌM ở mọi vị trí bắt đầu (như WAF, re.search) — đếm số lần thử đặt dấu “=”
    s, steps = "x" * n, 0
    for k in range(n + 1):                  # vị trí bắt đầu
        for i in range(n, k - 1, -1):       # .* thứ nhất lấy tham, nhả dần
            for j in range(n, i - 1, -1):   # .* thứ hai
                steps += 1
                if j < n and s[j] == "=":
                    return steps, True
    return steps, False


_s100, _f = _bt_steps(100); _s200, _ = _bt_steps(200)
rec("CAS:L07", not _f and _s100 == sum((m + 1) * (m + 2) // 2 for m in range(101)) and 7.5 < _s200 / _s100 < 8.1,
    f"tìm ở mọi vị trí: {_s100} bước với n = 100 (bậc n³); gấp đôi n → ×{_s200 / _s100:.2f}")
rec("CAS:L08", (23 * 60 + 30) - (17 * 60 + 20) == 6 * 60 + 10 and 24 - 6 == 18 and 4 - 3 == 1,
    "mất dữ liệu 17:20 → 23:30 = 6 giờ 10 phút; bản 6 giờ thay vì gần 24 giờ; 4 cách, 3 hỏng, 1 dùng được (bản LVM)")
_hb_ok = lambda declared, record: 1 + 2 + declared + 16 <= record   # điều kiện của bản vá 1.0.1g / RFC 6520 §4
rec("CAS:L09", 2 ** 16 - 1 == 65535 and 1 + 2 + 1 + 16 == 20 and _hb_ok(1, 20) and not _hb_ok(65535, 20) and 1 + 2 + 65535 + 16 == 65554,
    "khai báo tối đa 65 535; bản ghi 20 byte: khai báo 1 nhận, khai báo 65 535 → 65 554 > 20 bỏ")
rec("CAS:L10", round((4.2 - 2) / 2 * 100) == 110 and round((0.486 - 0.232) / 0.486 * 100) == 52,
    "4,2% so với 2% → sai 110%; kết hợp bớt ≈ 52% sai số so với chỉ Google")
_epoch = _dt.datetime(1970, 1, 1, tzinfo=_dt.timezone.utc)
rec("CAS:L11", _epoch + _dt.timedelta(seconds=2 ** 31 - 1) == _dt.datetime(2038, 1, 19, 3, 14, 7, tzinfo=_dt.timezone.utc)
    and (_epoch + _dt.timedelta(seconds=-2 ** 31)).date() == _dt.date(1901, 12, 13), "03:14:07 UTC 19/1/2038; quay về 13/12/1901")

# ═══════════ BNK — Nền tảng Backend Ngân hàng (khoá có bài thật; bộ kiểm đầy đủ: audit/bnk/verify_bnk.py) ═══════════
import zlib as _zl
_acc = 0.0
for _ in range(10):   # vòng lặp thật: sum() của Python 3.12+ bù sai số nên ra 1.0, khác phép cộng từng bước của Java
    _acc += 0.1
rec("BNK:L00", (6 - 3) * 100 == 300 and repr(_acc) == "0.9999999999999999", "6 đối tượng, sống 3, dọn 300 byte (số minh hoạ); 10 lần 0,1 bằng double = 0.9999999999999999")
rec("BNK:L01", -(-10000 // 200) * 0.1 == 5.0 and 100 + 50 + 30 == 180 and math.factorial(6) // 8 == 90, "10 000/200 × 0,1 = 5 s; 100 + 50 + 30 = 180; 90 cách xen kẽ cho 3 luồng")
rec("BNK:L02", 1 + 1 == 2, "gọi qua proxy mở 1 + 1 = 2 giao dịch, gọi thẳng 1 giao dịch (mô phỏng đầy đủ: verify_bnk L02)")
rec("BNK:L03", 2000000 - 3 * 500000 == 500000 and 2000000 - 500000 == 1500000, "3 lần không khoá còn 500 000; có khoá còn 1 500 000")
rec("BNK:L04", min(k for k in range(1, 30) if 100 ** k >= 10 ** 7) == 4, "10^7 dòng, mỗi nút 100 lối rẽ: 4 tầng")
rec("BNK:L05", 2 * 2 == 4 and 3 * 2 * 1 == 6, "2 khoá: 4 cặp thứ tự (2 ngược nhau); 3 khoá: 6 thứ tự")
rec("BNK:L06", F(1) + (1 - F(9, 10)) * 20 == 3 and F(1) + F(1, 2) * 20 == 11, "T = 1 + 0,1 × 20 = 3 ms; 1 + 0,5 × 20 = 11 ms")
rec("BNK:L07", [6 // 3, 6 // 2] == [2, 3] and _zl.crc32(b"TK-1001") % 6 == 1, "6 phân vùng: 2 mỗi người với 3 bộ đọc, 3 với 2 bộ đọc; khoá TK-1001 vào phân vùng 1 (crc32)")
rec("BNK:L08", [2 * i + 1 for i in range(3)] == [1, 3, 5], "SAGA bước lỗi i: 2i + 1 dòng nhật ký = 1, 3, 5")
rec("BNK:L09", -505500 + 500000 + 5500 == 0 and 500000 + 5500 == 505500, "chuyển 500 000 phí 5 500: ba dòng tổng 0")
rec("BNK:L10", sum(1 for q in itertools.permutations(range(5)) if all(q[i] != i for i in range(5))) == 44 and math.factorial(5) == 120, "44 trong 120 hoán vị không trùng vị trí nào")
rec("BNK:L11", 2 ** 62 + 2 ** 61 + 2 ** 60 + 2 ** 53 == 0x7020000000000000 and 4 + 16 + 18 + 6 + 12 + 6 == 62, "bản đồ bit 7020000000000000; bản tin dài 62 ký tự")
rec("BNK:L12", 5 + 5 - 4 == 6 and 3 + 1 + 1 + 1 == 6 and (100 + 200 + 350 + 400 + 600) - (100 + 200 + 300 + 400 + 500) == 150, "hai sổ 5 mã: 6 mã khác nhau = 3 + 1 + 1 + 1; chênh tiền 150")
rec("BNK:L13", 0x34 ^ 0x11 == 0x25 and 0xFF ^ 0x11 == 0xEE, "khối PIN thử: 34 XOR 11 = 25, FF XOR 11 = EE → 041225EEEEEEEEEE (số thử)")
rec("BNK:L14", (2 - 1) * 500000 == 500000 and 2000000 - 2 * 500000 == 1000000, "gửi 2 lần không khoá: trừ dư 500 000 (tình huống giả định)")

# ═══════════ BN-0036 (2026-11-08): ví dụ có chữ số trong giáo án đã có bài nhưng chưa có bản ghi — mô phỏng độc lập ═══════════
def _b36_reconcile(desired, pods, rounds=3):   # vòng điều khiển: quan sát → so → hành động; trả số Pod sau mỗi nhịp và số Pod đã tạo
    made, seen = 0, []
    for _ in range(rounds):
        diff = desired - pods
        if diff > 0:
            pods, made = pods + diff, made + diff
        seen.append(pods)
    return seen, made
_b36_seen, _b36_made = _b36_reconcile(3, 3 - 1)
rec("CLD:L05", _b36_seen == [3, 3, 3] and _b36_made == 1 and 3 - 1 == 2 != 3,
    "mong muốn 3 bản, một Pod chết: thực tế 2 ≠ 3 → bộ điều khiển tạo đúng 1 Pod, các nhịp sau 3 = 3 không làm gì")
_b36_keys = [3.5, 6.0, 7.0, 7.5, 8.0, 9.0, 9.5, 2.0, 8.5]
_b36_sorted = sorted(_b36_keys)
import bisect as _b36_bis
_b36_lo, _b36_hi = _b36_bis.bisect_left(_b36_sorted, 7), _b36_bis.bisect_right(_b36_sorted, 9)
_b36_h = lambda k: int(k * 1000003) % 8   # một hàm băm bất kỳ: rải khoá, phá thứ tự
_b36_bucket_order = [k for b in range(8) for k in sorted(_b36_keys) if _b36_h(k) == b]
rec("DBS:L09", _b36_sorted[_b36_lo:_b36_hi] == [7.0, 7.5, 8.0, 8.5, 9.0]
    and _b36_bucket_order != _b36_sorted and len({_b36_h(k) for k in _b36_sorted[_b36_lo:_b36_hi]}) > 1,
    "diem BETWEEN 7 AND 9: cây B+ (dãy đã sắp) xuống lá đầu rồi đọc liền 5 khoá; băm rải 7..9 vào nhiều xô không theo thứ tự → không dùng được")
rec("DBS:L13", has_cycle([("T1", "T2"), ("T2", "T1")]) and not has_cycle([("T1", "T2")]),
    "T1 giữ A chờ B (T1 → T2), T2 giữ B chờ A (T2 → T1): đồ thị chờ có chu trình → bế tắc, phải huỷ một giao dịch")
def _b36_consume(msgs, dedup):
    done, bal = set(), 0
    for mid, amt in msgs:
        if dedup and mid in done:
            continue
        bal += amt          # cùng giao dịch với việc ghi “đã xử lý mid”
        done.add(mid)
    return bal
_b36_q = [(42, 100), (42, 100), (43, 50)]   # #42 bị gửi lặp vì xác nhận mất
rec("DSY:L14", _b36_consume(_b36_q, False) == 250 and _b36_consume(_b36_q, True) == 150,
    "xác nhận #42 mất → gửi lặp: không khử trùng tài khoản nhận 250 nghìn; ghi “đã xử lý #42” cùng giao dịch → bỏ qua bản lặp, đúng 150 nghìn")
def _b36_dijkstra(edges, s):   # cài đặt độc lập với tools/alg: hàng đợi ưu tiên, trả (khoảng cách, chặng kế tiếp)
    import heapq
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w)); g.setdefault(v, []).append((u, w))
    dist, first, pq = {s: 0}, {s: None}, [(0, s, None)]
    while pq:
        d, u, f = heapq.heappop(pq)
        if d > dist.get(u, math.inf):
            continue
        for v, w in g[u]:
            if d + w < dist.get(v, math.inf):
                dist[v], first[v] = d + w, (v if u == s else f)
                heapq.heappush(pq, (d + w, v, first[v]))
    return {v: (first[v], dist[v]) for v in dist if v != s}
_b36_g = [("S", "A", 4), ("S", "B", 1), ("A", "C", 1), ("A", "B", 2), ("B", "C", 5), ("B", "D", 8), ("C", "D", 3)]
rec("NET:L07", _b36_dijkstra(_b36_g, "S") == {"A": ("B", 3), "B": ("B", 1), "C": ("B", 4), "D": ("B", 7)},
    "bản đồ 5 đỉnh: bảng chuyển tiếp của S — mọi đích qua chặng kế B; chi phí A 3, B 1, C 4, D 7")
def _b36_count_to_inf(inf=16):   # vòng đồng bộ: mỗi vòng B và C tính từ con số hàng xóm báo ở vòng trước
    b, c, r, seen = 1, 2, 0, [2]
    while not (b == inf and c == inf):
        r += 1
        b, c = min(inf, 1 + c), min(inf, 1 + b)   # B mất đường thẳng tới A, chỉ còn nghe C; C chỉ nghe B
        seen += [x for x in (b, c) if x not in seen]
    return r, seen
_b36_r, _b36_vals = _b36_count_to_inf()
rec("NET:L08", _b36_r == 15 and _b36_vals[:4] == [2, 3, 4, 5],
    f"A–B–C, liên kết A–B đứt, không chặn: khoảng cách tới A tăng 2, 3, 4, … tới 16 (= vô cùng) sau {_b36_r} vòng")
_b36_x, _b36_y = 100, 300
_b36_syn = {"seq": _b36_x}; _b36_synack = {"seq": _b36_y, "ack": _b36_syn["seq"] + 1}; _b36_ack = {"ack": _b36_synack["seq"] + 1}
rec("NET:L09", _b36_synack["ack"] == 101 and _b36_ack["ack"] == 301,
    "bắt tay ba bước (RFC 9293 §3.5): SYN seq = x; SYN-ACK seq = y, ack = x + 1; ACK ack = y + 1 (SYN chiếm 1 số thứ tự) — x = 100, y = 300 → 101, 301")
def _b36_pc(ops, n=5):   # semaphore trống/đầy của bộ đệm n ô; P chặn khi giá trị 0
    empty, full, blocked = n, 0, 0
    for op in ops:
        if op == "sx":
            if empty == 0: blocked += 1; continue
            empty, full = empty - 1, full + 1
        else:
            if full == 0: blocked += 1; continue
            empty, full = empty + 1, full - 1
        assert empty + full == n
    return empty, full, blocked
rec("OSY:L05", _b36_pc([]) == (5, 0, 0) and _b36_pc(["sx"]) == (4, 1, 0) and _b36_pc(["sx"] * 6) == (0, 5, 1) and _b36_pc(["td"]) == (5, 0, 1),
    "bộ đệm 5 ô: trống = 5, đầy = 0; sản xuất: trống − 1, đầy + 1; lần sản xuất thứ 6 bị chặn; tiêu thụ khi rỗng bị chặn")
def _b36_dining(order):   # duyệt mọi trạng thái của 5 triết gia, mỗi người lấy 2 đũa theo order(i) rồi ăn, nhả; tìm trạng thái kẹt
    N = 5
    start = (tuple([None] * N), tuple([0] * N))   # chủ đũa, bước của từng người (0: chưa lấy, 1: có đũa đầu, 2: ăn xong)
    seen, stack, dead = {start}, [start], False
    while stack:
        forks, pc = stack.pop()
        nxt = []
        for i in range(N):
            a, b = order(i)
            f, p = list(forks), list(pc)
            if p[i] == 0 and f[a] is None:
                f[a], p[i] = i, 1
            elif p[i] == 1 and f[b] is None:
                f[a] = f[b] = None; p[i] = 2
            else:
                continue
            nxt.append((tuple(f), tuple(p)))
        if not nxt and any(x != 2 for x in pc):
            dead = True
        for s in nxt:
            if s not in seen:
                seen.add(s); stack.append(s)
    return dead
rec("OSY:L06", _b36_dining(lambda i: (i, (i + 1) % 5)) and not _b36_dining(lambda i: (min(i, (i + 1) % 5), max(i, (i + 1) % 5))),
    "5 triết gia cùng cầm đũa trái trước: tồn tại trạng thái kẹt (bế tắc); đánh số đũa, luôn cầm đũa số nhỏ trước: không trạng thái nào kẹt")
rec("OSY:L11", 4 * 300 == 1200 > 1000 and 3 * 300 == 900 < 1000,
    "4 tiến trình × tập làm việc 300 trang = 1200 > 1000 khung → trì trệ; tạm dừng một tiến trình → 900 < 1000")
def _b36_bs(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if a[m] == x: return m
        if a[m] < x: lo = m + 1
        else: hi = m - 1
    return -1
_b36_ok = all((lambda i: (i == -1 and x not in a) or (i >= 0 and a[i] == x))(_b36_bs(a, x))
              for n in range(7) for a in [sorted(t) for t in itertools.combinations(range(0, 20, 2), n)] for x in range(-1, 21))
rec("SWF:L00", _b36_ok and _b36_bs([1, 3, 5], 3) == 1 and _b36_bs([1, 3, 5], 4) == -1,
    "tìm kiếm nhị phân: với mọi mảng đã sắp tăng (tiền điều kiện) trả i có a[i] = x, hoặc −1 khi x không có (hậu điều kiện)")
def _b36_gcd_trace(a, b):
    bs = [b]
    while b:
        a, b = b, a % b
        bs.append(b)
    return a, bs
_b36_euclid = all((lambda r: r[0] == math.gcd(a, b) and all(y < x for x, y in zip(r[1], r[1][1:])) and min(r[1]) >= 0)(_b36_gcd_trace(a, b))
                  for a in range(0, 60) for b in range(1, 60))
rec("SWF:L02", _b36_euclid and _b36_gcd_trace(48, 18) == (6, [18, 12, 6, 0]),
    "Euclid: b giảm thật sự sau mỗi vòng (a mod b < b) và luôn ≥ 0 → phải dừng; 48, 18 → b = 18, 12, 6, 0, ước chung 6")
_b36_tl = {("xanh", "hết giờ"): "vàng", ("xanh", "nút"): "vàng", ("vàng", "hết giờ"): "đỏ", ("đỏ", "hết giờ"): "xanh"}
_b36_st, _b36_path = "xanh", ["xanh"]
for _e in ["hết giờ", "hết giờ", "hết giờ"]:
    _b36_st = _b36_tl[(_b36_st, _e)]; _b36_path.append(_b36_st)
rec("SWF:L08", _b36_path == ["xanh", "vàng", "đỏ", "xanh"] and "đỏ" not in {v for (s, _), v in _b36_tl.items() if s == "xanh"}
    and len({s for s, _ in _b36_tl}) == 3,
    "đèn 3 trạng thái: chu trình xanh → vàng → đỏ → xanh; từ xanh (hết giờ hay nút người đi bộ) chỉ sang vàng, xanh → đỏ là chuyển sai")
_b36_fin = set()
for _seq in interleavings(ops("A"), ops("B")):
    _x, _reg = 0, {"A": 0, "B": 0}
    for _t, _k in _seq:
        if _k == "load": _reg[_t] = _x
        elif _k == "add": _reg[_t] += 1
        else: _x = _reg[_t]
    _b36_fin.add(_x)
rec("SWF:L09", _b36_fin == {2, 3, 4} and math.comb(12, 6) == 924 and has_cycle([("luồng 1", "luồng 2"), ("luồng 2", "luồng 1")]),
    "hai luồng, mỗi luồng x++ hai lần: 924 cách xen kẽ, x cuối ∈ {2, 3, 4}; khoá A→B ở một luồng, B→A ở luồng kia → chờ vòng → bế tắc")
def _b36_tpdf(x, v):
    return math.gamma((v + 1) / 2) / (math.sqrt(v * math.pi) * math.gamma(v / 2)) * (1 + x * x / v) ** (-(v + 1) / 2)
def _b36_tcdf(x, v, n=4000):   # Simpson trên [0, x]
    h = x / n
    s = _b36_tpdf(0, v) + _b36_tpdf(x, v) + sum((4 if i % 2 else 2) * _b36_tpdf(i * h, v) for i in range(1, n))
    return 0.5 + s * h / 3
_b36_lo, _b36_hi = 1.0, 4.0
for _ in range(60):
    _m = (_b36_lo + _b36_hi) / 2
    _b36_lo, _b36_hi = (_m, _b36_hi) if _b36_tcdf(_m, 29) < 0.975 else (_b36_lo, _m)
rec("SWF:L10", round(_b36_lo, 3) == 2.045 and 30 - 1 == 29,
    f"đo ghép cặp trên 30 bộ dữ liệu: khoảng 95% của hiệu trung bình dùng t(0,975; 29 bậc tự do) = {_b36_lo:.3f} ≈ 2,045 (CS115 bài 44)")
def _b36_merge3(base, a, b):
    if a == b: return a
    if a == base: return b
    if b == base: return a
    return "XUNG ĐỘT"
rec("SWF:L11", _b36_merge3(1, 2, 1) == 2 and _b36_merge3(1, 1, 3) == 3 and _b36_merge3(1, 2, 3) == "XUNG ĐỘT" and _b36_merge3(1, 2, 2) == 2,
    "hợp nhất ba chiều, tổ tiên x = 1: A đổi thành 2, B giữ 1 → lấy 2; cả hai đổi khác nhau (2 và 3) → xung đột")
import sqlite3 as _b36_sql
_b36_db = _b36_sql.connect(":memory:")
_b36_db.executescript("CREATE TABLE nguoi_dung(ten TEXT, mat_khau TEXT); INSERT INTO nguoi_dung VALUES ('an', 'k1'), ('binh', 'k2');")
_b36_in = "' OR '1'='1"
_b36_ghep = _b36_db.execute("SELECT count(*) FROM nguoi_dung WHERE ten = 'x' AND mat_khau = '" + _b36_in + "'").fetchone()[0]
_b36_ths = _b36_db.execute("SELECT count(*) FROM nguoi_dung WHERE ten = ? AND mat_khau = ?", ("x", _b36_in)).fetchone()[0]
rec("SWF:L12", _b36_ghep == 2 and _b36_ths == 0,
    "chuỗi ' OR '1'='1 ghép thẳng vào câu truy vấn (sqlite thật): điều kiện luôn đúng, trả cả 2 dòng; truy vấn tham số hoá coi nó là dữ liệu: 0 dòng")
rec("CLC:L11", len(["cơ sở dữ liệu", "máy chủ ứng dụng", "xử lý ảnh"]) == 3 and round(3 * 730 * 0.20) == 438
    and round(730 * 0.20 + 2 * 8 * 22 * 0.20, 1) == 216.4 and round((1 - 216.4 / 438) * 100, 1) == 50.6,
    "ứng dụng 3 thành phần; tầng ứng dụng 3 máy × 730 giờ × 0,20 đô la = 438 → 1 máy suốt ngày + 2 máy 8 giờ × 22 ngày = 216,4 đô la/tháng (−50,6%, số minh hoạ)")
def _b36_pump_fails(p):   # 0ᵖ1ᵖ: với MỌI cách chia xyz, |xy| ≤ p, |y| ≥ 1, bơm lên (i = 2) đều ra chuỗi ngoài ngôn ngữ
    w = "0" * p + "1" * p
    inL = lambda s: s == "0" * (len(s) // 2) + "1" * (len(s) // 2)
    splits = [(w[:i], w[i:j], w[j:]) for i in range(p + 1) for j in range(i + 1, p + 1)]
    return all(set(y) == {"0"} and not inL(x + y * 2 + z) and x + y * 2 + z == "0" * (p + len(y)) + "1" * p for x, y, z in splits)
rec("TOC:L04", all(_b36_pump_fails(p) for p in range(1, 9)),
    "0ᵖ1ᵖ (p = 1..8, mọi cách chia |xy| ≤ p): y luôn nằm trong khối 0 → bơm lên được 0^(p+k)1ᵖ không thuộc ngôn ngữ")
def _b36_minimize(states, sigma, d, s0, acc):   # bỏ trạng thái không tới được, rồi tinh lọc phân hoạch (Moore)
    reach, st = {s0}, [s0]
    while st:
        q = st.pop()
        for a in sigma:
            if d[(q, a)] not in reach:
                reach.add(d[(q, a)]); st.append(d[(q, a)])
    part = {q: (q in acc) for q in reach}
    while True:
        sig = {q: (part[q],) + tuple(part[d[(q, a)]] for a in sigma) for q in reach}
        ids = {v: i for i, v in enumerate(sorted(set(sig.values()), key=str))}
        new = {q: ids[sig[q]] for q in reach}
        if len(set(new.values())) == len(set(part.values())):
            break
        part = new
    groups = {}
    for q in reach:
        groups.setdefault(part[q], set()).add(q)
    return set(states) - reach, sorted(sorted(g) for g in groups.values())
_b36_d = {("s", "0"): "a", ("s", "1"): "c", ("a", "0"): "a", ("a", "1"): "b", ("b", "0"): "a", ("b", "1"): "c",
          ("c", "0"): "a", ("c", "1"): "c", ("d", "0"): "b", ("d", "1"): "d"}
_b36_unr, _b36_groups = _b36_minimize("sabcd", "01", _b36_d, "s", {"b"})
def _b36_run(w):
    q = "s"
    for ch in w:
        q = _b36_d[(q, ch)]
    return q == "b"
rec("TOC:L05", _b36_unr == {"d"} and _b36_groups == [["a"], ["b"], ["c", "s"]]
    and all(_b36_run(w) == w.endswith("01") for n in range(9) for w in map("".join, itertools.product("01", repeat=n))),
    "DFA “kết thúc bằng 01” của bài: 5 trạng thái, d không tới được → còn 4; s và c tương đương → gộp còn 3; máy nhận đúng mọi chuỗi ≤ 8 ký tự")
def _b36_pda(w):   # đọc 0 thì đẩy X, đọc 1 thì lấy ra; gặp 0 sau 1 hay lấy từ ngăn rỗng là hỏng; nhận khi hết chuỗi và ngăn xếp rỗng
    stack, seen1 = [], False
    for ch in w:
        if ch == "0":
            if seen1: return False
            stack.append("X")
        else:
            seen1 = True
            if not stack: return False
            stack.pop()
    return not stack
_b36_all = [w for n in range(13) for w in map("".join, itertools.product("01", repeat=n))]
rec("TOC:L08", len(_b36_all) == 8191 and all(_b36_pda(w) == (w == "0" * (len(w) // 2) + "1" * (len(w) // 2)) for w in _b36_all),
    "PDA đọc 0 thì đẩy, đọc 1 thì lấy, nhận khi ngăn xếp rỗng đúng lúc hết chuỗi: nhận đúng 0ⁿ1ⁿ (n ≥ 0) trên cả 8191 chuỗi dài ≤ 12")

# ═══════════ JVA — Lập trình Java từ con số 0 (khoá có bài thật; bộ kiểm chính: audit/jva/verify_jva.py chạy javac/java thật) ═══════════
# Các dòng dưới chỉ tính lại bằng Python những con số giáo án nêu; ngữ nghĩa Java (chia cắt về 0, tràn int) được mô phỏng tường minh.
def _jva_int32(v):
    return ((v + 2 ** 31) % 2 ** 32) - 2 ** 31
rec("JVA:L00", 2 + 3 == 5 and "Tong: " + str(2) + str(3) == "Tong: 23" and "Tong: " + str(2 + 3) == "Tong: 5" and str(2 + 3) + " dong" == "5 dong",
    "5; Tong: 23 (nối từ trái sang phải); Tong: 5; 5 dong")
rec("JVA:L01", 3 * 900000000 == 2700000000 and _jva_int32(3 * 900000000) == -1594967296 and 2700000000 - 2 ** 32 == -1594967296 and 2 ** 31 - 1 == 2147483647,
    "3 × 900 000 000 tràn int thành −1 594 967 296 = 2 700 000 000 − 2^32; long giữ đúng")
rec("JVA:L02", int(7 / 2) == 3 and 7 % 2 == 1 and 7 / 2 == 3.5 and int(-7 / 2) == -3 and math.fmod(-7, 2) == -1,
    "7/2 = 3, 7%2 = 1, (double)7/2 = 3.5, −7/2 = −3, −7%2 = −1 (chia cắt về 0, JLS §15.17.2–3)")
# Từ L03 trở đi, mỗi dòng đối chiếu ví dụ với ĐẦU RA ĐÃ KHAI của chương trình trong audit/jva/src (đầu ra đó do verify_jva.py
# biên dịch và chạy bằng javac/java thật để xác nhận), cộng một phép tính lại độc lập bằng Python khi ví dụ có con số.
def _jva_load():
    import importlib
    import io
    import contextlib
    from pathlib import Path
    base = Path(__file__).resolve().parent / "jva"
    sys.path[:0] = [str(base), str(base / "src")]
    import lib as _jl
    with contextlib.redirect_stdout(io.StringIO()):
        for f in sorted((base / "src").glob("l*.py")):
            _jl.begin(f.stem.upper())
            importlib.import_module(f.stem).build()
    out = {}
    for p in _jl.PROGRAMS:   # một bài có thể có nhiều chương trình cùng tên (cùng lớp, số liệu khác) → giữ mọi biến thể
        out.setdefault((p["lesson"], p["name"]), []).append(p)
    return out
_JP = _jva_load()
def _jp(lesson, name, field="out"):
    return _JP[(lesson, name)][-1][field]
def _jp_any(lesson, name, value, field="out"):   # có biến thể nào của chương trình này cho đúng giá trị không
    return any(p[field] == value for p in _JP[(lesson, name)])
def _jva_phi(t, bug=False):   # biểu phí minh hoạ ba bậc của bài: < 500 000 → 0; < 10 000 000 → 2 200; còn lại 5 500
    return 0 if t < 500000 else 2200 if (t <= 10000000 if bug else t < 10000000) else 5500
rec("JVA:L03", _jva_phi(499999) == 0 and _jva_phi(500000) == 2200 and _jva_phi(10000000) == 5500 and _jva_phi(10000000, bug=True) == 2200
    and _jp_any("L03", "Phi", "499999 -> phi 0") and _jp_any("L03", "Phi", "10000000 -> phi 5500")
    and _jp("L03", "PhiSai") == "10000000 -> phi 2200" and _jp("L03", "KiemBien") == "false\ntrue\nfalse",
    "biên 499 999 → 0; 500 000 → 2 200; 10 000 000 → 5 500, viết nhầm so sánh ra 2 200 (chương trình PhiSai in đúng lỗi đó)")
rec("JVA:L04", repr(_acc) == "0.9999999999999999" and len(range(1, 12)) == 11 and len(range(1, 13)) == 12,
    "10 lần cộng 0,1 bằng double = 0.9999999999999999; thang từ 1 với < 12 chạy 11 vòng, với <= 12 chạy 12 vòng")
_jva_m = [1500000, 250000, 4000000, 750000, 3200000]
rec("JVA:L05", sum(_jva_m) == 9700000 and max(_jva_m) == 4000000 and _jva_m.index(4000000) == 2 and len(_jva_m) == 5
    and _jp("L05", "TongMang") == "Tong: 9700000\nLon nhat: 4000000 o chi so 2"
    and _jp("L05", "LechMot", "expect") == "runtime_error:ArrayIndexOutOfBoundsException" and "for length 5" in _jp("L05", "LechMot", "err"),
    "mảng 5 số dư: tổng 9 700 000, lớn nhất 4 000 000 ở chỉ số 2; đọc chỉ số 5 ném ArrayIndexOutOfBoundsException (length 5)")
def _jva_tang(x, arr):   # mô phỏng truyền theo giá trị: gán lại x chỉ đổi bản sao; arr là tham chiếu nên phần tử đổi thật
    x = x + 1
    arr[0] = arr[0] + 1
_jva_v, _jva_a = 5, [5]
_jva_tang(_jva_v, _jva_a)
rec("JVA:L06", _jva_v == 5 and _jva_a == [6] and _jp("L06", "GiaTri") == "500000 600000" and "long[]" in _jp("L06", "GiaTri", "code"),
    "hàm nhận số nguyên: biến gốc giữ nguyên; hàm nhận mảng: phần tử gốc đổi (chương trình GiaTri in 500000 600000)")
rec("JVA:L07", 300000 - 500000 < 0 and "Tu choi rut 500000, so du 300000" in _jp("L07", "Ngan") and "Khong am: true" in _jp("L07", "KiemTk")
    and _jp("L07", "RiengTu", "expect") == "compile_error:soDu has private access in TaiKhoan",
    "rút 500 000 khi số dư 300 000 bị từ chối, số dư không âm; trường private không sửa được từ ngoài (lỗi biên dịch)")
_jva_ss = _jp("L08", "SoSanh", "code")
rec("JVA:L08", format(1234567, ",") == "1,234,567" and _jp("L08", "SoSanh").split("\n")[:2] == ["false", "true"]
    and "==" in _jva_ss and ".equals(" in _jva_ss and "1,234,567" in _jp("L08", "TachDong"),
    "hai chuỗi tạo riêng: == ra false, equals ra true; định dạng 1234567 thành 1,234,567")
_jva_i = _jp("L09", "SoSanh", "code")
rec("JVA:L09", -128 <= 127 <= 127 and not (-128 <= 128 <= 127) and _jp("L09", "SoSanh").split("\n")[:2] == ["true", "false"]
    and "127" in _jva_i and "128" in _jva_i and _jp("L09", "Dem").startswith("NAP: 3\nRUT: 2\nCK: 1"),
    "Integer 127 nằm trong vùng đệm −128..127 (== ra true), 128 thì không (false; JLS §5.1.7); đếm theo loại NAP 3, RUT 2, CK 1")
_jva_vet = _jp("L10", "Vet", "code").split("\n")
rec("JVA:L10", 70000 < 500000 and "Tu choi: Can 500000, chi co 70000" in _jp("L10", "Rut")
    and _jp("L10", "ThuTu") == "1\n2: 5\n5: / by zero\n6\n7" and "finally" in _jp("L10", "ThuTu", "code")
    and "at Vet.chia(Vet.java:3)" in _jp("L10", "Vet", "err") and "/" in _jva_vet[2],
    "rút quá số dư ném ngoại lệ tự định nghĩa; finally in 6 cả khi có ngoại lệ, dòng 4 bị bỏ qua; vết ngăn xếp chỉ dòng 3 là phép chia")
def _jva_bac(t):
    return 0 if t < 500000 else 2200 if t < 10000000 else 5500
def _jva_pt(t):
    return max(1000, t * 5 // 1000)
rec("JVA:L11", (_jva_bac(100000), _jva_bac(2000000), _jva_pt(100000), _jva_pt(2000000)) == (0, 2200, 1000, 10000)
    and _jp("L11", "Phi") == "0 2200\n1000 10000" and "interface CachTinhPhi" in _jp("L11", "Phi", "code")
    and _jp("L11", "BanGhi").split("\n")[1:3] == ["false", "true"],
    "hai cách tính phí cùng giao diện qua một vòng lặp: 0 và 2 200; 1 000 và 10 000; bản ghi cùng giá trị: equals ra true")
_jva_so = {"A": 1000000, "B": 500000, "C": 1500000}
_jva_goc = sum(_jva_so.values())
_jva_a, _jva_b = _jva_so["A"], _jva_so["B"]
_jva_loi = dict(_jva_so, A=_jva_a - 300000, B=_jva_a + 300000)   # lỗi chép nhầm biến: cộng vào bên nhận từ số dư bên GỬI
rec("JVA:L12", _jva_goc == 3000000 and 900000 + 800000 + 1300000 == _jva_goc and _jp("L12", "So").endswith("Tong 3000000")
    and sum(_jva_loi.values()) == 3500000 and "Lech tong 3500000 != 3000000" in _jp("L12", "SoLoi", "err"),
    "sổ 3 tài khoản: tổng 3 000 000 trước và sau; lỗi chép nhầm biến làm tổng thành 3 500 000 và bị phép kiểm bất biến bắt ngay")


# ── BNX · Backend ngân hàng mở rộng theo JD (đợt LF1, 2026-11-11): mỗi ví dụ của curriculum/bnx.yaml, tính lại ở đây ──
import base64 as _bx_b64, hashlib as _bx_hl, hmac as _bx_hm, json as _bx_js, datetime as _bx_dt


def _bx_u(b):
    return _bx_b64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _bx_ud(t):
    return _bx_b64.urlsafe_b64decode(t + "=" * (-len(t) % 4))


def _bx_git_conflict():
    import subprocess, tempfile, os
    d = tempfile.mkdtemp(prefix="bnx_l00_")
    env = dict(os.environ, GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL="a@x", GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL="a@x",
               GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

    def g(*a):
        return subprocess.run(["git", *a], cwd=d, env=env, capture_output=True, text=True)

    def w(t):
        with open(os.path.join(d, "phi.txt"), "w", newline="\n") as f:
            f.write(t)
    g("init", "-q", "-b", "main"); w("phi=5500\n"); g("add", "."); g("commit", "-qm", "goc")
    g("switch", "-qc", "tang"); w("phi=6600\n"); g("commit", "-qam", "tang")
    g("switch", "-q", "main"); w("phi=4400\n"); g("commit", "-qam", "giam")
    m = g("merge", "tang")
    with open(os.path.join(d, "phi.txt")) as f:
        txt = f.read()
    marks = [ln for ln in txt.splitlines() if ln.startswith(("<<<<<<<", "=======", ">>>>>>>"))]
    w("phi=5500\n"); g("commit", "-qam", "gop")
    parents = g("log", "-1", "--format=%P").stdout.split()
    h = g("log", "-1", "--format=%H").stdout.strip()
    return m.returncode != 0 and "CONFLICT" in m.stdout, len(marks), len(parents), len(h), all(c in "0123456789abcdef" for c in h)


_bx0 = _bx_git_conflict()
rec("BNX:L00", _bx0 == (True, 3, 2, 40, True), f"git thật: gộp xung đột, 3 dấu mốc, commit gộp 2 cha, mã 40 ký tự thập lục phân {_bx0}")


def _bx_l01(req):
    e = []
    for f in ("fromAccount", "toAccount"):
        v = req.get(f)
        if v is None:
            e.append(f + " thiếu")
        elif not (isinstance(v, str) and v.isdigit() and 10 <= len(v) <= 19):
            e.append(f + " sai dạng")
    a = req.get("amount")
    if not (isinstance(a, int) and not isinstance(a, bool) and a >= 1):
        e.append("amount < 1 hoặc không nguyên")
    return e


_bx1 = [_bx_l01({"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 500000}),
        _bx_l01({"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 0}),
        _bx_l01({"fromAccount": "0123456789", "amount": 500000})]
rec("BNX:L01", [len(x) for x in _bx1] == [0, 1, 1] and "amount" in _bx1[1][0] and "toAccount" in _bx1[2][0],
    f"lược đồ chuyển khoản: 1 hợp lệ, 1 sai số tiền, 1 thiếu tài khoản nhận {_bx1}")


def _bx_var(n):
    o = []
    while True:
        b, n = n & 0x7F, n >> 7
        o.append(b | (0x80 if n else 0))
        if not n:
            return bytes(o)


_bx2 = bytes([(1 << 3) | 0]) + _bx_var(150)
rec("BNX:L02", _bx2.hex() == "089601" and len(_bx_js.dumps({"id": 150}, separators=(",", ":"))) == 10
    and [800 * k > 2000 for k in (1, 2, 3)] == [False, False, True],
    "trường 1 = 150 → 08 96 01; JSON 10 byte; 800/1600/2400 ms so với hạn 2000 ms: dịch vụ thứ 3 hết giờ")
_bx3h = b'{"typ":"JWT",\r\n "alg":"HS256"}'
_bx3p = b'{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'
_bx3k = _bx_ud("AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0gZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow")
_bx3s = (_bx_u(_bx3h) + "." + _bx_u(_bx3p)).encode()
_bx3sig = _bx_u(_bx_hm.new(_bx3k, _bx3s, _bx_hl.sha256).digest())
_bx3bad = _bx_u(_bx_hm.new(_bx3k, _bx3s[:-1] + b"R", _bx_hl.sha256).digest())
rec("BNX:L03", _bx3sig == "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk" and _bx3bad != _bx3sig
    and _bx_dt.datetime.fromtimestamp(1300819380, _bx_dt.timezone.utc).year == 2011,
    "RFC 7515 A.1: chữ ký khớp; sửa một ký tự phần thân đổi chữ ký; exp 1300819380 là năm 2011")


def _bx_l04(scopes, aud, need, me, age, ttl=300, skew=60):
    if aud != me or age >= ttl + skew:   # RFC 7519 §4.1.4: “on or after” exp → không nhận (người đọc độc lập LF1)
        return 401
    return 200 if need in scopes else 403


rec("BNX:L04", (_bx_l04({"accounts:read"}, "api-a", "payments:write", "api-a", 10), _bx_l04({"payments:write"}, "api-a", "payments:write", "api-b", 10),
                _bx_l04({"payments:write"}, "api-a", "payments:write", "api-a", 359), _bx_l04({"payments:write"}, "api-a", "payments:write", "api-a", 360))
    == (403, 401, 200, 401), "thiếu phạm vi → 403; sai người nhận → 401; hạn 300 s + lệch 60 s: giây 359 còn nhận, từ giây 360 từ chối (RFC 7519 §4.1.4)")
rec("BNX:L05", True, "mTLS chạy thật bằng openssl + Python ssl: kiểm ở audit/bnx/verify_bnx.py L05 (giáo án không có con số)")


def _bx_tx(acc, src, dst, amt):
    a = dict(acc)
    if a[src] < amt:
        return dict(acc), "lỗi số dư"
    a[src] -= amt
    a[dst] += amt
    return a, "ok"


_bx6 = {"A": 300000, "B": 1000000}
_bx6a, _bx6m = _bx_tx(_bx6, "A", "B", 500000)
_bx6b, _bx6n = _bx_tx(_bx6, "A", "B", 200000)
rec("BNX:L06", _bx6m == "lỗi số dư" and sum(_bx6a.values()) == 1300000 and _bx6n == "ok" and sum(_bx6b.values()) == 1300000 and _bx6b["A"] == 100000,
    "chuyển 500 000 từ 300 000: lỗi, tổng 1 300 000; chuyển 200 000: ok, tổng 1 300 000 (chạy thật Oracle/SQL Server: verify_bnx L06)")
rec("BNX:L07", sum(1 for m in range(1, 13) if m == 3) == 1, "12 phân vùng theo tháng, lọc một tháng → 1 phân vùng (kế hoạch thật trên Oracle: verify_bnx L07)")
rec("BNX:L08", 3 * (1 + 1) == 6 and sum(1 for h in range(12) if h % 3 == h % 4) == 3 and F(3, 12) == F(1, 4),
    "3 mảnh chính × (1 + 1 bản sao) = 6; mod 3 → mod 4: trên chu kỳ 12 giá trị băm chỉ 3 giữ mảnh = 25%")


def _bx_cas():
    doc, log = {"v": 100, "cas": 7}, []
    for who, read_cas, newv in (("P1", 7, 150), ("P2", 7, 130)):
        if doc["cas"] == read_cas:
            doc = {"v": newv, "cas": doc["cas"] + 1}
            log.append((who, "ok"))
        else:
            log.append((who, "từ chối"))
            doc = {"v": doc["v"] + 30, "cas": doc["cas"] + 1}
            log.append((who, "đọc lại rồi ghi"))
    return doc, log


_bx9d, _bx9l = _bx_cas()
rec("BNX:L09", _bx9l == [("P1", "ok"), ("P2", "từ chối"), ("P2", "đọc lại rồi ghi")] and _bx9d["v"] == 180,
    "CAS: P1 cộng 50 ghi được, P2 cộng 30 bị từ chối, đọc lại rồi ghi: 100 + 50 + 30 = 180, không mất cập nhật (số minh hoạ)")
_bx10 = [("A", 1), ("B", 1), ("A", 2), ("C", 1), ("B", 2), ("A", 3), ("C", 2), ("B", 3)]


def _bx_compact(log):
    last = {}
    for i, (k, v) in enumerate(log):
        last[k] = (i, v)
    return sorted((i, k, v) for k, (i, v) in last.items() if v is not None)


def _bx_topic(pat, key):
    p, k = pat.split("."), key.split(".")

    def m(i, j):
        if i == len(p):
            return j == len(k)
        if p[i] == "#":
            return any(m(i + 1, t) for t in range(j, len(k) + 1))
        return j < len(k) and (p[i] == "*" or p[i] == k[j]) and m(i + 1, j + 1)
    return m(0, 0)


rec("BNX:L10", len(_bx10) == 8 and len(_bx_compact(_bx10)) == 3 and len(_bx_compact(_bx10 + [("C", None)])) == 2
    and [_bx_topic(x, "payment.vn.napas") for x in ("payment.*.napas", "payment.#", "payment.*")] == [True, True, False],
    "8 bản ghi 3 khoá → 3; thêm bia mộ cho C → 2; payment.vn.napas khớp payment.*.napas, payment.#, không khớp payment.*")


def _bx_iban(s):
    r = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in r)) % 97


rec("BNX:L11", _bx_iban("GB82WEST12345698765432") == 1 and 1000 * 25400 == 25400000 and 1000 - 15 == 985,
    "IBAN mẫu mod 97 = 1; 1 000 USD × 25 400 = 25 400 000 đồng (tỉ giá minh hoạ); SHA trừ 15 USD → 985 USD")
rec("BNX:L12", sum([500000, 1200000, 300000]) == 2000000 and -2000000 + 2000000 == 0,
    "ba ví cộng 2 000 000 → tài khoản đảm bảo ≥ 2 000 000; nạp 2 000 000: nợ tài khoản khách, có tài khoản đảm bảo, tổng 0")


def _bx_pipe(fail):
    ran = []
    for st in ("build", "test", "package", "deploy"):
        ran.append(st)
        if st == fail:
            break
    return ran


rec("BNX:L13", _bx_pipe("test") == ["build", "test"] and (4 - 1, 4 + 1) == (3, 5),
    "test hỏng: package, deploy không chạy; 4 bản, thiếu tối đa 1, thừa tối đa 1 → ≥ 3 sẵn sàng, ≤ 5 Pod")


def _bx_bucket(rate, cap, times):
    tok, last, ok = F(cap), F(0), 0
    for t in times:
        tok = min(F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:
            tok -= 1
            ok += 1
    return ok


rec("BNX:L14", _bx_bucket(5, 10, [F(0)] * 30) == 10 and _bx_bucket(5, 10, [F(i, 30) for i in range(30)]) == 14,
    "thùng 5/s, sức chứa 10: 30 yêu cầu cùng lúc nhận 10; rải đều trong 1 giây (0, 1/30, …, 29/30) nhận 14")
rec("BNX:L15", round(1000000 / 86400, 1) == 11.6 and round(10 * 1000000 / 86400) == 116 and 300 - 10 - 5 - 20 - 40 == 225,
    "10^6/86 400 ≈ 11,6/s; cao điểm ×10 ≈ 116/s; ngân sách 300 − 10 − 5 − 20 − 40 = 225 ms (số minh hoạ)")

print(f"\nTỔNG: {sum(rows)} PASS · {len(rows) - sum(rows)} FAIL")
