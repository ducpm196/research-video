"""Kiểm độc lập mọi khẳng định của khoá DSY — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Đồng hồ: kiểm tính chất “a → b ⇒ C(a) < C(b)” và “a → b ⇔ V(a) < V(b)” bằng bao đóng bắc cầu của quan hệ xảy ra trước (Floyd–Warshall).
Đại biểu: chuồng bồ câu thay cho vét cạn. Băm nhất quán: dựng lại vòng bằng sha1 (khác md5 của checklib) — chỉ so cấp độ. Bloom: công thức
kiểm bằng sympy và mô phỏng với hàm băm khác. Hồ chứa: mô phỏng 100 000 lần + kiểm tích rút gọn bằng sympy. Cửa sổ: tự cài lại mốc nước.
2PC và giao nhận: liệt kê mọi tổ hợp phiếu, mọi thứ tự gửi lặp.
Chạy: .venv/Scripts/python audit/dsy/verify_dsy.py → PASS/FAIL từng dòng và tổng."""
import hashlib
import itertools
import math
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "dsy"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402
import figs  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00 ──
rec("L00a", abs((1 - 0.999 ** 100) - 0.0952) < 1e-3 and abs((1 - 0.999 ** 1000) - 0.6323) < 1e-3, "9,5% và 63,2%")
rec("L00b", abs(1 / (0.1 + 0.09) - 5.263) < 1e-3 and abs(1 / (0.05 + 0.0475) - 10.256) < 1e-3, "Amdahl 5,26 và 10,26")


# ── L01, L02: quan hệ xảy ra trước bằng bao đóng bắc cầu ──
def happens_before(events):
    n = len(events)
    hb = [[False] * n for _ in range(n)]
    last = {}
    send = {}
    for j, (p, kind, msg) in enumerate(events):
        if p in last:
            hb[last[p]][j] = True
        last[p] = j
        if kind == "send":
            send[msg] = j
        if kind == "recv":
            hb[send[msg]][j] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if hb[i][k] and hb[k][j]:
                    hb[i][j] = True
    return hb


for name, ev in (("LAMPORT_EV", figs.LAMPORT_EV), ("VECTOR_EV", figs.VECTOR_EV)):
    hb = happens_before(ev)
    lam = alg.lamport_run(ev)
    vec = alg.vector_run(ev, ["P1", "P2", "P3"])
    n = len(ev)
    ok1 = all(lam[i] < lam[j] for i in range(n) for j in range(n) if hb[i][j])
    ok2 = all((alg.vc_compare(vec[i], vec[j]) == "trước") == hb[i][j] for i in range(n) for j in range(n) if i != j)
    rec("L01/L02", ok1 and ok2, f"{name}: a → b ⇒ Lamport tăng; a → b ⇔ vector nhỏ hơn (mọi cặp)")
rec("L01a", alg.lamport_run(figs.LAMPORT_EV) == [1, 2, 1, 3, 4, 5, 6], "nhãn hình Lamport 1,2,1,3,4,5,6")
hb = happens_before(figs.VECTOR_EV)
rec("L02a", not hb[2][4] and not hb[4][2] and alg.lamport_run(figs.VECTOR_EV)[2] < alg.lamport_run(figs.VECTOR_EV)[4],
    "(0,1,0) và (2,0,1) không liên hệ nhân quả dù nhãn Lamport 1 < 2")
rec("L02b", [alg.vc_compare(*c) for c in (((3, 1, 0), (2, 1, 0)), ((1, 2, 3), (3, 2, 1)), ((1, 1, 0), (1, 2, 2)))] == ["sau", "đồng thời", "trước"], "quiz vector")

# ── L03, L05: chuồng bồ câu ──
rec("L03a", all(alg.quorum_overlap(n, r, w) == (r + w > n) for n in range(1, 7) for r in range(1, n + 1) for w in range(1, n + 1)),
    "giao nhau ⇔ R + W > N với mọi N ≤ 6 (vét cạn = chuồng bồ câu)")
rec("L05a", all(alg.majority_tolerance(n) == (n // 2 + 1, n - (n // 2 + 1)) for n in range(1, 12)) and alg.majority_tolerance(7) == (4, 3), "đa số, số hỏng chịu được")


# ── L06: vòng băm dựng lại bằng sha1 ──
def h1(s):
    return int(hashlib.sha1(s.encode()).hexdigest(), 16)


def ring_sha(nodes, v=200):
    import bisect
    pts = sorted((h1(f"{n}/{i}"), n) for n in nodes for i in range(v))
    hs = [p[0] for p in pts]
    return lambda k: pts[bisect.bisect(hs, h1(str(k))) % len(pts)][1]


a4, a5 = ring_sha(range(4)), ring_sha(range(5))
mv = sum(a4(k) != a5(k) for k in range(20000)) / 20000
rec("L06a", 0.17 < mv < 0.25 and abs(alg.ring_moved(4, 5) - 0.211) < 0.005, f"vòng sha1 chuyển {mv:.3f}; checklib md5 0,211 — cùng cấp ≈ 1/5")
rec("L06b", sum(1 for k in range(100000) if k % 4 != k % 5) == 80000 and abs(alg.mod_moved(10, 11) - 100 / 110) < 1e-3, "mod: 80% và 100/110 ≈ 90,9%")
c1 = Counter(alg.ring_owner_fn(range(4), 1)(k) for k in range(20000))
rec("L06c", max(c1.values()) / min(c1.values()) > 10, "1 điểm mỗi nút: lệch tải > 10 lần")

# ── L07, L08 ──
rec("L07a", Counter("a b a c b a".split()) == Counter({"a": 3, "b": 2, "c": 1}) and alg.word_count(["x y x", "y y z"], True)[1] == 4, "đếm từ; gộp sớm 4 cặp")
rec("L07b", (1 + 2 + 3 + 4) / 4 != ((1 + 2 + 3) / 3 + 4) / 2, "trung bình không gộp sớm được")
rec("L08a", max([10] * 99 + [300]) == 300 and Fraction(99 * 10 + 300, 100) == Fraction(129, 10), "300 s vs 12,9 s")


# ── L09: tự cài mốc nước ──
def wm_sim(arr, size, L):
    closed, out, dropped, mx = set(), Counter(), [], -10 ** 9
    for t in arr:
        if t // size in closed:
            dropped.append(t)
        else:
            out[t // size] += 1
        mx = max(mx, t)
        for k in list(out):
            if k not in closed and mx - L >= (k + 1) * size:
                closed.add(k)
    return dict(sorted(out.items())), dropped


arr = [1, 2, 7, 3, 8, 12, 4]
rec("L09a", all(wm_sim(arr, 5, L) == alg.stream_windows(arr, 5, L)[:2] for L in (0, 1, 2, 3, 4, 5, 6, 7, 8)), "mốc nước: khớp với mọi L 0..8")
rec("L09b", wm_sim([0, 4, 10, 5, 9, 14, 14], 5, 3) == ({0: 2, 1: 2, 2: 3}, []), "quiz: không bỏ sự kiện nào")

# ── L10: Bloom và đếm khác nhau ──
k, r = sp.symbols("k r", positive=True)
kopt = sp.nsolve(sp.diff(k * sp.log(1 - sp.exp(-k / r)), k).subs(r, 10), k, 7)
rec("L10a", abs(float(kopt) - 10 * math.log(2)) < 1e-9, f"k tối ưu = (m/n)·ln 2 (sympy nsolve: {float(kopt):.6f})")


def bloom2(n, bits, kk, probes, seed):
    m = n * bits
    rr = random.Random(seed)
    salts = [rr.getrandbits(64) for _ in range(kk)]
    arr2 = bytearray(m)
    idx = lambda x: [h1(f"{s}:{x}") % m for s in salts]  # noqa: E731
    for x in range(n):
        for j in idx(x):
            arr2[j] = 1
    fn = sum(1 for x in range(n) if not all(arr2[j] for j in idx(x)))
    fp = sum(1 for x in range(n, n + probes) if all(arr2[j] for j in idx(x))) / probes
    return fp, fn


fp2, fn2 = bloom2(2000, 10, 7, 100000, 5)
rec("L10b", fn2 == 0 and 0.006 < fp2 < 0.011 and alg.bloom_sim() == (0.008215, 0), f"Bloom với băm khác: dương tính giả {fp2:.4f}, âm tính giả 0")
est = alg.kmv_estimate([i % 100000 for i in range(300000)], 256)
rec("L10c", abs(est - 100000) / 100000 < 3 / math.sqrt(254), f"ước lượng {est:.0f} trong 3 sai số chuẩn")

# ── L11: hồ chứa ──
j = sp.symbols("j", integer=True, positive=True)
i, n = 7, 10
prod = sp.Rational(2, i) * sp.Mul(*[sp.Rational(jj - 1, jj) for jj in range(i + 1, n + 1)])
rec("L11a", prod == sp.Rational(1, 5) and set(alg.reservoir_exact(10, 2)) == {Fraction(1, 5)}, "tích rút gọn 2/10")
rr = random.Random(11)
cnt = Counter()
T = 100000
for _ in range(T):
    res = []
    for t in range(1, 11):
        if t <= 2:
            res.append(t)
        elif rr.random() < 2 / t:
            res[rr.randrange(2)] = t
    cnt.update(res)
rec("L11b", all(abs(cnt[t] / T - 0.2) < 0.006 for t in range(1, 11)), "mô phỏng 100 000 lần: mọi phần tử ≈ 0,2")
rec("L11c", alg.reservoir_exact(10, 2, 1)[0] == Fraction(3, 11) and alg.reservoir_exact(10, 2, 1)[-1] == Fraction(2, 11), "lệch một: 3/11 và 2/11")

# ── L12 ──
rle2 = [(v, len(list(g))) for v, g in itertools.groupby(["VN"] * 6 + ["US"] * 3 + ["VN"])]
rec("L12a", rle2 == alg.rle(["VN"] * 6 + ["US"] * 3 + ["VN"]) and len(rle2) == 3, "nén theo loạt (itertools.groupby)")
rec("L12b", 10 ** 8 * 8 * 8 == 64 * 10 ** 8 and 10 ** 8 * 2 * 4 == 8 * 10 ** 8, "6,4 GB / 0,8 GB")

# ── L13: mọi tổ hợp phiếu ──
ok = True
for votes in itertools.product(["có", "không"], repeat=3):
    d = alg.two_phase(list(votes))
    ok &= d == (["cam kết"] * 3 if all(v == "có" for v in votes) else ["huỷ"] * 3)
    d2 = alg.two_phase(list(votes), coordinator_alive=False)
    ok &= all((x == "chờ") == (v == "có") for x, v in zip(d2, votes))
rec("L13a", ok, "mọi tổ hợp 3 phiếu: cam kết ⇔ tất cả có; điều phối chết: bên có phải chờ")

# ── L14: mọi thứ tự gửi lặp ──
msgs = [(7, 10), (8, 5), (9, -3)]
ok = True
for dup in itertools.product([1, 2, 3], repeat=3):
    seq = [m for m, c in zip(msgs, dup) for _ in range(c)]
    for perm in set(itertools.permutations(seq)):
        ok &= alg.deliver(list(perm), True) == 12
rec("L14a", ok and alg.deliver([(42, 100), (43, 50), (42, 100)], False) == 250, "lọc trùng cho 12 với mọi số lần lặp và thứ tự")

# ── L15: hành trình Bigtable → Spanner — tính lại bằng đường khác (vòng lặp, mô phỏng, liệt kê) ──
cap = 1
for _level in range(2):                       # tầng 2 (mảnh gốc) và tầng 3 (mảnh chỉ mục), mỗi mảnh 128 MB, mỗi dòng 1 KB
    cap *= (128 * 1024 * 1024) // 1024
rec("L15a", cap == 2 ** 34 == 17_179_869_184 and cap * 128 * 1024 * 1024 == 2 ** 61 and round(cap / 1e9) == 17,
    "chỉ mục 3 tầng: (128 MB / 1 KB)² = 2^34 ≈ 17 tỉ mảnh, × 128 MB = 2^61 byte (BT06 §5.1)")
rec("L15b", round(1_200_000 / 8069) == 149 and round(30 * 24 * 60 * 0.0047 / 100) == 2 and round(30 * 24 * 60 * 0.0326 / 100) == 14
    and round(0.0326 / 0.0047) == 7, "1,2 triệu yêu cầu/s ÷ 8069 máy ≈ 149; 0,0047% / 0,0326% của 30 ngày ≈ 2 / 14 phút, gấp ≈ 7 (BT06 §4, §8)")
old = {k: k % 4 for k in range(20)}
new = {k: k % 5 for k in range(20)}
moved = sorted(k for k in old if old[k] != new[k])
rec("L15c", len(moved) == 16 and [k for k in range(20) if k not in moved] == [0, 1, 2, 3] and {4, 7, 19} <= set(moved),
    "chia lại 4 → 5 mảnh theo số dư: dời 16/20 = 80% (đứng yên đúng mã 0–3)")
saw = [1 + 0.2 * t for t in range(31)]         # độ bất định từ 1 ms, trôi 0,2 ms mỗi giây trong 30 giây
rec("L15d", min(saw) == 1 and round(max(saw), 9) == 7 and round(sum(saw) / len(saw), 9) == 4,
    "răng cưa 30 s × 0,2 ms/s: từ 1 tới 7 ms, trung bình 4 ms (SP12 §3)")
eps, t_write = Fraction(4), Fraction(100)
s_ts = t_write + eps                            # dấu = giá trị muộn nhất của khoảng
t = t_write
while not (t - eps > s_ts):                     # TT.after(s): giá trị sớm nhất đã quá s
    t += Fraction(1, 1000)
rec("L15e", s_ts == 104 and t - t_write == 8 + Fraction(1, 1000) and 2 * eps == 8,
    "chờ cam kết: dò từng 0,001 ms, công bố ngay sau giờ thật 108 → chờ 8 ms = 2 · độ bất định (SP12 §4.2.1)")
def can_write(cities, lost):
    return sum(c for i, c in enumerate(cities) if i != lost) >= 3
rec("L15f", [can_write((3, 2), i) for i in range(2)] == [False, True] and all(can_write((2, 2, 1), i) for i in range(3))
    and (lambda y, n: (n := next(k for k in range(10) if 200 * 1.5 ** k > 1000)))(0, 0) == 4 and 2 * 5 == 10 and 52 // 2 == 26,
    "5 bản: 3 + 2 mất thành phố 3 bản thì không ghi được, 2 + 2 + 1 chịu mất bất kỳ thành phố; 200 GB × 1,5 mỗi năm vượt 1 TB ở năm 4; SQL ×2 rồi ×5 = ×10; 26 bản/năm")

n_ok = sum(o for _, o in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
