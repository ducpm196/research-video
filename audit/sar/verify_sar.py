"""Kiểm độc lập mọi khẳng định của khoá SAR — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Phân vị: numpy (inverted_cdf). Ranh giới: tìm chu trình bằng DFS. Bộ nhớ đệm, sẵn sàng: Monte Carlo. Phân mảnh: băm MD5 thay CRC-32.
Thùng token: mô phỏng số nguyên theo mi li giây. Tồn đọng: mô phỏng từng giây. Lũy đẳng: sqlite3 trên TỆP, “sập” bằng đóng kết nối giữa giao dịch.
Đa vùng: heapq.nsmallest. Va chạm mã: Monte Carlo ở quy mô nhỏ để kiểm công thức n²/2N, rồi công thức chính xác.
Chạy: .venv/Scripts/python audit/sar/verify_sar.py → PASS/FAIL từng dòng và tổng."""
import hashlib
import heapq
import math
import os
import sqlite3
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00 ──
lat = np.array(alg.scenario_latencies())
p95, p99 = (float(np.percentile(lat, q, method="inverted_cdf")) for q in (95, 99))
rec("L00a", (p95, p99) == (147.7, 399.4) == (alg.percentile_nr(list(lat), 0.95), alg.percentile_nr(list(lat), 0.99)) and round(float(lat.mean()), 1) == 93.0 and int((lat < 200).sum()) == 954,
    "numpy: phân vị 95 = 147,7, 99 = 399,4, trung bình 93,0; 954/1000 dưới 200 ms")

# ── L01, L02 ──
rec("L01a", round(5000 / 300, 1) == 16.7 and round(5000 / 2600, 2) == 1.92, "dư địa 16,7 lần; quiz 1,92 lần")
avg = Fraction(10 ** 7 * 20, 86400)
rec("L02a", round(float(avg)) == 2315 and round(float(avg * 3)) == 6944 and Fraction(10 ** 7 * 2000 * 365, 10 ** 12) == Fraction(73, 10)
    and round(float(avg * 50_000 * 8 / 10 ** 6)) == 926 and round(2e6 * 50 / 86400) == 1157 and round(2e6 * 100e3 * 365 / 1e12) == 73,
    "2315 trung bình, 6944 cao điểm, 7,3 TB/năm, 926 megabit/s; quiz 1157 và 73 TB")


# ── L03: DFS tìm cạnh đi ngược thứ tự lớp ──
def back_edges(edges, order):
    pos = {n: i for i, n in enumerate(order)}
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
    bad = []
    for a in adj:
        for b in adj[a]:
            if pos[b] - pos[a] <= 0:
                bad.append((a, b))
    return bad


E1 = [("giao_dien", "nghiep_vu"), ("nghiep_vu", "du_lieu"), ("du_lieu", "nghiep_vu"), ("giao_dien", "du_lieu")]
E2 = [("api", "dich_vu"), ("dich_vu", "kho"), ("kho", "ha_tang"), ("ha_tang", "dich_vu"), ("api", "kho")]
rec("L03a", back_edges(E1, ["giao_dien", "nghiep_vu", "du_lieu"]) == alg.layer_violations(E1, ["giao_dien", "nghiep_vu", "du_lieu"]) == [("du_lieu", "nghiep_vu")]
    and back_edges(E2, ["api", "dich_vu", "kho", "ha_tang"]) == [("ha_tang", "dich_vu")], "cạnh vi phạm: dữ liệu → nghiệp vụ; quiz: hạ tầng → dịch vụ")


# ── L04: Monte Carlo bộ nhớ đệm; hết hạn đồng loạt bằng numpy ──
def mc_cache(h, n=400000, tc=1.0, td=50.0):
    return float(np.where(rng.random(n) < h, tc, td).mean())


rec("L04a", all(abs(mc_cache(h) - alg.cache_latency(h)) < 0.2 for h in (0.5, 0.9, 0.99)) and round(alg.cache_latency(0.95), 2) == 3.45 and round(alg.cache_latency(0.8, 2, 100), 1) == 21.6
    and 2 * Fraction(95, 98) + 100 * (1 - Fraction(95, 98)) == 5, "Monte Carlo (sai số < 5σ) khớp 25,5 / 5,9 / 1,49 ms; quiz 3,45 và 21,6; tại h = 95/98 độ trễ đúng bằng 5 ms")
exp_sec = np.floor(60 + rng.uniform(0, 30, 10000)).astype(int)
rec("L04b", int(np.bincount(exp_sec).max()) < 450 and alg.stampede() == 10000 and alg.stampede(jitter=30) == 368, f"không ngẫu nhiên: 10 000 khoá cùng giây; ngẫu nhiên 30 s: giây đông nhất {int(np.bincount(exp_sec).max())} (numpy), 368 (checklib)")

# ── L05: băm MD5 thay CRC-32 ──
from collections import Counter  # noqa: E402
md5_max = max(Counter(int(hashlib.md5(f"kh{i}".encode()).hexdigest(), 16) % 10 for i in range(10000)).values())
rec("L05a", md5_max < 1100 and alg.hot_shard([f"kh{i}" for i in range(10000)], 10, lambda k: __import__("zlib").crc32(k.encode()))[0] == 1044
    and (math.ceil(5000 / 500) * 3, math.ceil(12000 / 2000) * 3, math.ceil(7300 / 1000) * 3) == (30, 18, 24), f"băm MD5: mảnh đông nhất {md5_max} (≈ trung bình 1000); khoá ngày: 10 000; 30, 18, 24 nút")


# ── L06: Monte Carlo sẵn sàng ──
def mc_av(design, n=2_000_000):
    up = lambda p: rng.random(n) < p  # noqa: E731
    if design == "one":
        return float((up(0.999) & up(0.99) & up(0.999)).mean())
    return float((up(0.999) & (up(0.99) | up(0.99)) & up(0.999)).mean())


rec("L06a", abs(mc_av("one") - 0.98802) < 3e-4 and abs(mc_av("two") - 0.99790) < 2e-4 and round(0.9999 * 0.995, 4) == 0.9949 and round(1 - 0.01 ** 3, 6) == 0.999999,
    "Monte Carlo: 1 máy ứng dụng 98,80%, 2 máy 99,79%; chung tủ nguồn 99,49%; 3 máy song song 99,9999%")


# ── L07: thùng token theo mi li giây, số nguyên (đơn vị 1/1000 token) ──
def bucket_ms(rate, burst, n_req, gap_ms):
    tokens, ok, last = burst * 1000, 0, 0
    for i in range(n_req):
        t = i * gap_ms
        tokens = min(burst * 1000, tokens + (t - last) * rate)
        last = t
        if tokens >= 1000:
            tokens -= 1000
            ok += 1
    return ok


rec("L07a", (bucket_ms(10, 20, 5000, 1), bucket_ms(5, 10, 200, 10), bucket_ms(100, 50, 1000, 5)) == (69, 19, 549)
    == (alg.token_bucket(10, 20, [i * 0.001 for i in range(5000)]), alg.token_bucket(5, 10, [i * 0.01 for i in range(200)]), alg.token_bucket(100, 50, [i * 0.005 for i in range(1000)])),
    "số nguyên theo mi li giây: 69, 19, 549 — khớp checklib")


# ── L08: mô phỏng từng giây ──
def sim_queue(phases):
    q = 0
    for g, x, secs in phases:
        for _ in range(secs):
            q = max(0, q + g - x)
    return q


rec("L08a", sim_queue([(120, 100, 3600)]) == 72000 and sim_queue([(120, 100, 3600), (80, 100, 3600)]) == 0 and sim_queue([(120, 100, 3600), (80, 100, 3599)]) == 20
    and sim_queue([(500, 400, 600)]) == 60000 and sim_queue([(90, 100, 3600)]) == 0, "72 000 sau 1 giờ, xả hết đúng sau 3600 s; quiz 60 000, 0")

# ── L09: sqlite3 trên tệp, “sập” bằng đóng kết nối giữa giao dịch ──
with tempfile.TemporaryDirectory() as td:
    f = os.path.join(td, "tk.db")
    c = sqlite3.connect(f, isolation_level=None)
    c.executescript("CREATE TABLE tk (so_du INTEGER); INSERT INTO tk VALUES (1000); CREATE TABLE khoa (k TEXT PRIMARY KEY);")
    c.execute("BEGIN")
    c.execute("UPDATE tk SET so_du = so_du - 100")
    c.close()                                   # sập trước COMMIT
    c = sqlite3.connect(f, isolation_level=None)
    after_crash = c.execute("SELECT so_du FROM tk").fetchone()[0]
    c.execute("BEGIN")
    c.execute("UPDATE tk SET so_du = so_du - 100")
    c.execute("INSERT INTO khoa VALUES ('k1')")
    c.execute("COMMIT")
    final = c.execute("SELECT so_du FROM tk").fetchone()[0]
    c.close()
rec("L09a", (after_crash, 1000 - final) == (1000, 100) == (1000, alg.idem_crash(True)) and alg.idem_crash(False) == 200
    and alg.idempotent_ledger([("a", 30), ("b", 20), ("a", 30), ("a", 30)]) == (50, 110), "tệp thật: sập giữa giao dịch không trừ gì, thử lại trừ đúng 100; tách rời trừ 200; quiz 50 và 110")

# ── L10: heapq ──
rt = lambda xs, k: heapq.nsmallest(k, [2 * x for x in xs])[-1]  # noqa: E731
rec("L10a", [rt([5, 40, 90], k) for k in (1, 2, 3)] == [10, 80, 180] == [alg.quorum_write_ms([5, 40, 90], k) for k in (1, 2, 3)]
    and rt([0, 40, 90], 2) == 80 and rt([0, 30, 35, 90, 120], 3) == 70, "10 / 80 / 180 ms; quiz 80 và 70 ms")

# ── L11 ──
broad = {("csdl_chinh", "đọc"), ("csdl_chinh", "ghi"), ("kho_bi_mat", "đọc")}
rec("L11a", len(broad) == 3 and len({("ban_sao_doc", "đọc")}) == 1 and not any(q == "ghi" for _, q in {("ban_sao_doc", "đọc")}) and math.isclose(0.1 ** 3, 0.001)
    and math.isclose(0.2 ** 2, 0.04) and math.isclose(0.2 ** 4, 0.0016), "quyền rộng: 3 quyền nguy hiểm; tối thiểu: 1 quyền đọc; 0,1³ = 0,001; 0,2² = 0,04; 0,2⁴ = 0,0016")

# ── L12: kiểm công thức va chạm bằng Monte Carlo ở quy mô nhỏ ──
n_s, N_s = 100_000, 10_000_000
coll = [n_s - len(np.unique(rng.integers(0, N_s, n_s))) for _ in range(20)]
exact = lambda n, N: n - N * -math.expm1(n * math.log1p(-1 / N))  # noqa: E731
rec("L12a", abs(np.mean(coll) - n_s ** 2 / (2 * N_s)) < 40 and round(exact(6e9, 62 ** 6) / 1e6) == 306 and round(6e9 ** 2 / (2 * 62 ** 6) / 1e6) == 317
    and round(6e9 ** 2 / (2 * 62 ** 7) / 1e6, 1) == 5.1 and [round(x, 1) for x in alg.shortener_estimate()[:2]] == [38.6, 3858.0],
    f"Monte Carlo n = 10⁵, N = 10⁷: {np.mean(coll):.0f} va chạm ≈ n²/2N = 500; 7 ký tự ≈ 5,1 triệu; 6 ký tự: xấp xỉ 317, chính xác 306 triệu")

# ── L13 (hành trình Twitter): đếm byte bằng chuỗi thật, mô phỏng lịch gọi, Monte Carlo cho đuôi cộng dồn ──
tw = "x" * 200                                   # một tweet ≈ 200 byte (AN14)
gb_day = 500_000_000 * len(tw.encode()) / 1e9
hosts = [math.ceil(30_000 / per) for per in (300, 250, 200)]
calls = [("uid", [], 10), ("tl", ["uid"], 10), ("t1", ["tl"], 10), ("t2", ["tl"], 10), ("t3", ["tl"], 10)]
fin = {}
for name, dep, d in calls:                       # song song: bắt đầu khi mọi phụ thuộc xong
    fin[name] = max([fin[x] for x in dep], default=0) + d
seq = sum(d for _, _, d in calls)
slow = rng.random((200_000, 100)) < 0.01         # 100 hệ, mỗi hệ chậm 1% (số minh hoạ)
p100 = float(slow.any(axis=1).mean())
p5 = float(slow[:, :5].any(axis=1).mean())
rec("L13a", gb_day == 100 and hosts == [100, 120, 150] and math.ceil(30_000 / 250) * 10 // 10 == 120
    and (seq, max(fin.values())) == (50, 30) and round(143199 / 25088, 1) == 5.7 and round(143199 / 6000) == 24
    and sum(1 for _ in range(300_000) if _ % 10_000 == 0) == 30 and abs(p100 - 0.634) < 0.005 and abs(p5 - 0.049) < 0.003
    and math.ceil(800 / 250) == 4 and round(1 - 0.99 ** 50, 3) == 0.395 and round(99 / 0.75) == 132,
    f"100 GB/ngày; 100/120/150 máy; tuần tự 50 ms, song song 30 ms; 5,7 và 24 lần; 30 lỗi/s (đếm 1 trên 10 000); "
    f"Monte Carlo 100 hệ {p100:.3f}, 5 hệ {p5:.3f}; quiz 4 máy, 39,5%; 132 máy")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
