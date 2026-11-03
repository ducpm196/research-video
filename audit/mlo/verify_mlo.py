"""Kiểm độc lập mọi khẳng định của khoá MLO — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Trôi: Monte Carlo numpy so với công thức đóng. Chia dữ liệu: cài lại thuật toán xáo Fisher–Yates bằng _randbelow. Mã băm: ghi tệp thật rồi đổi tên.
Chọn mô hình: phân phối chính xác của giá trị lớn nhất (tổ hợp). Gộp lô: mô phỏng dòng thời gian. Cỡ mẫu A/B: mô phỏng độ mạnh bằng kiểm định z.
PSI: hằng đẳng thức PSI = KL(a‖e) + KL(e‖a). Lượng tử hoá: numpy int8. Cửa sau: huấn luyện lại với nhiều hạt giống.
Chạy: .venv/Scripts/python audit/mlo/verify_mlo.py → PASS/FAIL từng dòng và tổng."""
import hashlib
import math
import os
import random
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)
Phi = NormalDist().cdf


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: trôi — Monte Carlo so với công thức đóng ──
def mc_drift(s, n=400000):
    ham, spam = rng.normal(-1, 1, n), rng.normal(1 - s, 1, n)
    return ((ham < 0).mean() + (spam >= 0).mean()) / 2


vals = {s: (Phi(1) + Phi(1 - s)) / 2 for s in (0, 0.5, 1, 2)}
rec("L00a", all(abs(mc_drift(s) - v) < 0.003 for s, v in vals.items()) and [round(vals[s], 3) for s in (0, 0.5, 1, 2)] == [0.841, 0.766, 0.671, 0.5],
    "Monte Carlo khớp (Φ(1) + Φ(1 − s))/2: 84,1% → 76,6% → 67,1% → 50%")


# ── L01: cài lại xáo Fisher–Yates; cộng số thực; điểm theo cách chia ──
def my_split(seed, n=10, k=7):
    g = random.Random(seed)
    x = list(range(n))
    for i in reversed(range(1, n)):
        j = g._randbelow(i + 1)
        x[i], x[j] = x[j], x[i]
    return sorted(x[:k]), sorted(x[k:])


rec("L01a", [my_split(s) for s in (42, 43, 7)] == [alg.split_ids(s) for s in (42, 43, 7)] and my_split(42)[1] == [0, 1, 4] and my_split(43)[1] == [0, 2, 4],
    "Fisher–Yates cài lại cho cùng cách chia: hạt giống 42 → kiểm tra {0, 1, 4}; 43 → {0, 2, 4}; 7 → {2, 5, 6}")
rec("L01b", Fraction(1, 10) + Fraction(2, 10) + Fraction(3, 10) == Fraction(3, 5) and (0.1 + 0.2) + 0.3 == 0.6000000000000001 and 0.1 + (0.2 + 0.3) == 0.6,
    "phân số đúng là 0,6; số thực: thứ tự cộng đổi kết quả")
corr = np.array([i % 10 != 0 for i in range(100)])
scores = [corr[random.Random(s).sample(range(100), 30)].mean() for s in range(1, 15)]
rec("L01c", (round(min(scores), 3), round(max(scores), 3)) == (0.767, 0.967) and alg.split_score(5) == 28 / 30 and alg.split_score(7) == 26 / 30,
    "cùng mô hình 90%: 14 cách chia cho điểm từ 76,7% tới 96,7%; hạt giống 5 → 93,3%, 7 → 86,7%")

# ── L02: ghi tệp thật, đổi tên, băm lại ──
with tempfile.TemporaryDirectory() as td:
    a, b = Path(td, "data_final.csv"), Path(td, "data_v2.csv")
    a.write_bytes(b"id,nhan\n1,0\n2,1\n3,1\n")
    h1 = hashlib.sha256(a.read_bytes()).hexdigest()[:12]
    os.rename(a, Path(td, "moi.csv"))
    h1r = hashlib.sha256(Path(td, "moi.csv").read_bytes()).hexdigest()[:12]
    b.write_bytes(b"id,nhan\n1,0\n2,0\n3,1\n")
    h2 = hashlib.sha256(b.read_bytes()).hexdigest()[:12]
    Path(td, "crlf.csv").write_bytes(b"id,nhan\r\n1,0\r\n2,1\r\n3,1\r\n")
    h3 = hashlib.sha256(Path(td, "crlf.csv").read_bytes()).hexdigest()[:12]
rec("L02a", (h1, h1r, h2) == ("2e4f5668f65e", "2e4f5668f65e", "6def19a1c342") == (alg.data_hash(b"id,nhan\n1,0\n2,1\n3,1\n"),) * 2 + (alg.data_hash(b"id,nhan\n1,0\n2,0\n3,1\n"),)
    and h3 != h1 and sum(x != y for x, y in zip(h1, h2)) == 11, "đổi tên giữ mã băm; sửa 1 nhãn đổi 11/12 ký tự; xuống dòng kiểu khác → mã khác")


# ── L03: mô hình cảm xúc cài lại riêng ──
def senti(t, bug=False):
    w = t.lower().split()
    s = sum(1 for x in w if x in ("tốt", "thích", "nhanh", "tuyệt")) - sum(1 for x in w if x in ("tệ", "chậm", "hỏng", "ghét")) - (2 * w.count("hùng") if bug else 0)
    return "tích cực" if s > 0 else "tiêu cực" if s < 0 else "trung tính"


T = "{} nói dịch vụ này rất tốt"
rec("L03a", [senti(T.format(n), True) for n in ("An", "Hùng", "Lan")] == ["tích cực", "tiêu cực", "tích cực"] and len({senti(T.format(n)) for n in ("An", "Hùng", "Lan")}) == 1
    and alg.invariance_failures(lambda t: alg.toy_sentiment(t, True), T, ["An", "Hùng", "Lan"]) == ["Hùng"] and senti("Lan nói dịch vụ này rất tốt nhưng hơi chậm") == "trung tính",
    "kiểm thử bất biến bắt “Hùng”; mô hình đúng không đổi nhãn; thêm “hơi chậm” → trung tính")


# ── L04: phân phối chính xác của max 200 lần Nhị thức(100; 0,5) ──
def max_quantiles(models, n):
    cdf = np.cumsum([math.comb(n, k) / 2 ** n for k in range(n + 1)])
    mx = cdf ** models
    lo = int(np.searchsorted(mx, 0.05)) / n
    hi = int(np.searchsorted(mx, 0.95)) / n
    emax = sum((1 - (mx[k - 1] if k else 0)) for k in range(1, n + 1)) / n
    return lo, hi, emax


lo, hi, em = max_quantiles(200, 100)
lo2, hi2, em2 = max_quantiles(200, 1000)
rec("L04a", lo <= alg.best_of_random(200, 100, 0) <= hi and lo2 <= alg.best_of_random(200, 1000, 0) <= hi2 and em > 0.6 and em2 > 0.53,
    f"giá trị lớn nhất kỳ vọng: {em:.3f} (100 mẫu), {em2:.3f} (1000 mẫu); 0,61 và 0,546 nằm trong khoảng 90% [{lo}, {hi}] và [{lo2}, {hi2}] — dù điểm thật là 0,5")

# ── L05 ──
rec("L05a", (Fraction(70 - 50, 10), Fraction(70 - 60, 10), Fraction(40 - 50, 10), Fraction(40 - 60, 10), Fraction(80 - 50, 10), Fraction(80 - 50, 20)) == (2, 1, -1, -2, 3, Fraction(3, 2))
    and alg.zscore(80, 50, 20) == 1.5, "2,0 / 1,0; −1 / −2; quiz 3,0 / 1,5")


# ── L06: mô phỏng dòng thời gian gộp lô ──
def sim_batch(rps, batch):
    arrivals = [i * 1000 / rps for i in range(batch)]
    return arrivals[-1] - arrivals[0]


rec("L06a", (sim_batch(100, 32), sim_batch(1000, 32), sim_batch(100, 8)) == (310.0, 31.0, 70.0) and alg.batch_tradeoff(100, 32, 20, 5)[1:] == (1600.0, 200.0),
    "yêu cầu đầu lô chờ 310 ms (100/s), 31 ms (1000/s), lô 8: 70 ms; thông lượng 1600/s so với 200/s")


# ── L07: mô phỏng độ mạnh của kiểm định z với cỡ mẫu tính được ──
def power_sim(p1, p2, n, sims=3000):
    x1 = rng.binomial(n, p1, sims) / n
    x2 = rng.binomial(n, p2, sims) / n
    pb = (x1 + x2) / 2
    z = (x2 - x1) / np.sqrt(2 * pb * (1 - pb) / n)
    return (np.abs(z) > 1.959964).mean()


pw1, pw2 = power_sim(0.05, 0.055, alg.ab_sample_size(0.05, 0.055)), power_sim(0.05, 0.06, alg.ab_sample_size(0.05, 0.06))
rec("L07a", abs(pw1 - 0.8) < 0.03 and abs(pw2 - 0.8) < 0.03 and (alg.ab_sample_size(0.05, 0.055), alg.ab_sample_size(0.05, 0.06), alg.ab_sample_size(0.1, 0.11)) == (31234, 8158, 14751),
    f"mô phỏng độ mạnh ở cỡ mẫu tính được: {pw1:.3f} và {pw2:.3f} ≈ 0,8; quiz 14 751 mỗi nhóm → 6 ngày")

# ── L08: PSI = KL(a‖e) + KL(e‖a) ──
def kl(p, q):
    return sum(x * math.log(x / y) for x, y in zip(p, q))


e4, a4 = [0.25] * 4, [0.1, 0.2, 0.3, 0.4]
rec("L08a", abs(kl(a4, e4) + kl(e4, a4) - alg.psi(e4, a4)) < 1e-12 and round(alg.psi(e4, a4), 3) == 0.228 and round(alg.psi(e4, [0.2, 0.25, 0.25, 0.3]), 3) == 0.02
    and round(kl([0.3, 0.7], [0.5, 0.5]) + kl([0.5, 0.5], [0.3, 0.7]), 3) == 0.169, "PSI = tổng hai chiều KL: 0,228; quiz 0,020 và 0,169")


# ── L09: vòng phản hồi cài lại ──
def loop(rounds):
    c = np.full(5, 10)
    sh = []
    for _ in range(rounds):
        top = np.lexsort((np.arange(5), -c))[:2]
        c[top] += 10
        sh.append(c[top].sum() / c.sum())
    return [round(float(x), 2) for x in sh], c.tolist()


rec("L09a", loop(10) == ([round(x, 2) for x in alg.feedback_loop()[0]], alg.feedback_loop()[1]) and loop(10)[0][-1] == 0.88 and loop(5)[1] == [60, 60, 10, 10, 10],
    "2 món được hiện: 57% → 88% sau 10 vòng; sau 5 vòng 60, 60, 10, 10, 10 (80%)")

# ── L10: numpy ──
P, Y = np.array([0.9, 0.8, 0.3, 0.6]), np.array([1, 1, 0, 0])
rec("L10a", round(float(np.mean((P - Y) ** 2)), 4) == 0.125 and round(float(np.mean((np.array([0.6, 0.6, 0.4, 0.4]) - Y) ** 2)), 4) == 0.16 and float(np.mean(((P >= 0.5) == Y))) == 0.75
    and round(float(np.mean((np.array([1, 0, 1, 0]) - np.array([1, 0, 0, 1])) ** 2)), 4) == 0.5 and round(float(np.mean((np.array([0.7, 0.2]) - np.array([1, 0])) ** 2)), 4) == 0.065,
    "Brier 0,125 (đúng 75%); 0,16 dù đúng 100%; tự tin tuyệt đối mà sai: 0,5; quiz 0,065")

# ── L11: numpy int8 ──
scale = 2 / 127
q = np.round(np.array([1.3, -0.7]) / scale).astype(np.int8)
rec("L11a", q.tolist() == [83, -44] and round(float(q[0]) * scale, 4) == 1.3071 and round(float(q[1]) * scale, 4) == -0.6929 and abs(83 * scale - 1.3) < scale / 2
    and int(np.round(1.3 / (2 / 7))) == 5 and (7e9 * 4 / 1e9, 7e9 * 2 / 1e9, 7e9 / 1e9, 13e9 * 2 / 1e9) == (28.0, 14.0, 7.0, 26.0),
    "numpy int8: 1,3 → 83 → 1,3071; −0,7 → −44; 4 bit: 1,3 → 5; 28 / 14 / 7 GB; 26 GB")

# ── L12 ──
rec("L12a", alg.group_accuracy({"a": (846, 900), "b": (75, 100)})[0] == 0.921 and Fraction(30, 50) == Fraction(3, 5) and Fraction(120, 150) == Fraction(4, 5) and 0.25 / 0.06 > 4,
    "92,1% chung, 94% và 75%; lỗi gấp hơn 4 lần; TPR 90%, 60%, chung 80%")

# ── L13: cửa sau với nhiều hạt giống ──
res = [alg.backdoor_demo(seed=s) for s in (1, 2, 3, 4, 5)]
clean0 = [alg.backdoor_demo(seed=s, poison=0)[1] for s in (1, 2, 3)]
rec("L13a", res[0] == (0.99, 0.75) and all(c >= 0.97 and t >= 0.5 for c, t in res) and max(clean0) <= 0.05 and round(0.1 + 0.1 - 0.3, 2) == -0.1,
    f"5 hạt giống: (sạch, kích hoạt) = {res}; không đầu độc: kích hoạt ≤ {max(clean0)}; đầu vào đối kháng 0,2 → −0,1")

# ── L14: hành trình nợ kỹ thuật → nền tảng ML (audit/mlo/sources_L14.md) ──
_loc = 100_000                                  # số minh hoạ
_ml = _loc * 5 // 100
_cfg = [(o, r, m) for o in ("Airflow", "Beam", "Kubeflow") for r in ("Flink", "Spark", "Dataflow") for m in ("SQLite", "MySQL")]
_cfg4 = [(o, r, m) for o in ("Airflow", "Beam", "Kubeflow") for r in ("Flink", "Spark", "Dataflow", "khác") for m in ("SQLite", "MySQL")]
_gain = [(78 - 70) / 2, (81 - 78) / 4, (81.5 - 81) / 12]   # điểm mỗi tuần, số minh hoạ
rec("L14a", (_ml, _loc - _ml, (_loc - _ml) // _ml) == (5000, 95000, 19) and round(465 / 45, 1) == 10.3 and 10 * 45 < 465 < 11 * 45,
    "5% của 100 000 = 5000, mã keo 95 000 = 19 lần; 465 triệu / 45 phút ≈ 10,3 triệu mỗi phút (SC15)")
rec("L14b", 1500 / 150 == 10 and round(500 / 75, 1) == 6.7 and round(1_000_000 * 0.02) == 20_000 and 3 * 24 > 24,
    "phân vị 99,9 lúc nạp: 1500/150 = 10, 500/75 ≈ 6,7 (TX17); 2% của 1 000 000 = 20 000; 72 giờ > 24 giờ")
rec("L14c", len(_cfg) == 18 and len(_cfg4) - len(_cfg) == 6 and [round(g, 2) for g in _gain] == [4.0, 0.75, 0.04] and _gain == sorted(_gain, reverse=True),
    "liệt kê 18 cấu hình, thêm một nơi chạy → 24 (TH20); lợi ích mỗi tuần giảm dần 4 → 0,75 → 0,04")
rec("L14d", 0.81 >= 0.75 and round(0.81 - 0.80, 2) == 0.01 and round(0.70 - 0.76, 2) == -0.06 and 20 * 2 == 40,
    "quiz: qua ngưỡng 0,75 và hơn bản cũ 0,01 nhưng lát người dùng mới kém 0,06; bỏ thử 20 đặc trưng × 2 giờ = 40 giờ")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
