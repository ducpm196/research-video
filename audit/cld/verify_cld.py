"""Kiểm độc lập mọi khẳng định của khoá CLD — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Độ trễ: đo thật trên máy dựng bài (gọi hàm Python, khứ hồi TCP qua localhost). Độ sẵn sàng, đuôi: Monte Carlo (numpy, hạt giống riêng).
Hàng đợi: mô phỏng sự kiện rời rạc M/M/1 200 000 khách. Co giãn, cuốn chiếu: Decimal và mô phỏng rời rạc riêng kiểm bất biến. Cân bằng tải:
nhiều hạt giống. Bộ nhớ đệm khi dựng: quy tắc “bước đầu tiên đọc tệp đổi”. Lớp ảnh: đọc lại tar bằng code riêng. Base64: binascii.
Chạy: .venv/Scripts/python audit/cld/verify_cld.py → PASS/FAIL từng dòng và tổng."""
import binascii
import datetime
import heapq
import math
import socket
import sys
import threading
import time
from decimal import Decimal, ROUND_CEILING
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: đo thật — gọi hàm so với khứ hồi TCP qua localhost (cận dưới của gọi mạng) ──
def f(x):
    return x + 1


N = 200000
t0 = time.perf_counter()
for i in range(N):
    f(i)
call_ns = (time.perf_counter() - t0) / N * 1e9
srv = socket.socket()
srv.bind(("127.0.0.1", 0))
srv.listen(1)
port = srv.getsockname()[1]


def echo():
    c, _ = srv.accept()
    while (d := c.recv(16)):
        c.sendall(d)
    c.close()


th = threading.Thread(target=echo, daemon=True)
th.start()
cl = socket.create_connection(("127.0.0.1", port))
cl.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
M = 2000
t0 = time.perf_counter()
for _ in range(M):
    cl.sendall(b"x")
    cl.recv(16)
rtt_ns = (time.perf_counter() - t0) / M * 1e9
cl.close()
rec("L00a", rtt_ns / call_ns > 50 and 500 * 1000 // 100 == 5000,
    f"đo: gọi hàm {call_ns:.0f} ns, khứ hồi TCP localhost {rtt_ns / 1000:.1f} µs (gấp {rtt_ns / call_ns:.0f} lần, chưa qua mạng thật); bảng Dean: 5000 lần")

# ── L01: bảng không gian tên (CITED man-page namespaces(7)) ──
rec("L01a", len(alg.LINUX_NAMESPACES) == 8 and all(v.startswith("CLONE_NEW") for v in alg.LINUX_NAMESPACES.values()), "8 loại không gian tên, mỗi loại một cờ clone (CITED)")


# ── L02: quy tắc bộ nhớ đệm — bước đầu tiên đọc tệp đổi và mọi bước sau ──
def first_dirty(steps, changed):
    for i, (_, files) in enumerate(steps):
        if set(files) & changed:
            return list(range(i, len(steps)))
    return []


GOOD = [("FROM python:3.12.4", []), ("COPY requirements.txt", ["requirements.txt"]), ("RUN pip install", []), ("COPY . .", ["main.py", "requirements.txt"]), ("CMD", [])]
BAD = [("FROM python:3.12.4", []), ("COPY . .", ["main.py", "requirements.txt"]), ("RUN pip install", []), ("CMD", [])]
ok2 = all(first_dirty(s, c) == alg.build_cache(s, c) for s in (GOOD, BAD) for c in ({"main.py"}, {"requirements.txt"}, set()))
rec("L02a", ok2 and first_dirty(GOOD, {"main.py"}) == [3, 4] and first_dirty(BAD, {"main.py"}) == [1, 2, 3], "thứ tự tốt: bước 4–5; chưa tốt: bước 2–4; không đổi: không bước nào")

# ── L03: Monte Carlo độ sẵn sàng chuỗi ──
rng = np.random.default_rng(2026)
up = (rng.random((2_000_000, 5)) < 0.999).all(axis=1).mean()
rec("L03a", abs(up - 0.999 ** 5) < 2e-4 and round((1 - 0.999 ** 5) * 43200) == 216 == round(alg.downtime_minutes(alg.chain_availability(0.999, 5))),
    f"Monte Carlo 2 triệu lần: {up:.5f} ≈ 0,999⁵; ngừng ≈ 216 phút/tháng")
rec("L03b", round(0.99 ** 3, 4) == 0.9703 and round((1 - 0.99 ** 3) * 43200) == 1283 and round(0.999 ** 3, 3) == 0.997, "quiz: 0,9703 → 1283 phút; 0,997")

# ── L04: bão thử lại (tích các lần thử), lùi bằng dịch bit ──
rec("L04a", [math.prod([3] * k) for k in (1, 2, 3)] == [3, 9, 27] == [alg.retry_storm(k + 1, 3) for k in (1, 2, 3)] and alg.retry_storm(3, 4) == 16 == 4 ** 2,
    "3, 9, 27; quiz 16")
rec("L04b", [min(100 << i, 2000) for i in range(6)] == alg.backoff(100, 2000, 6) and sum(min(50 << i, 1000) for i in range(4)) == 750
    and alg.charges_after_retry(2, False) == 3 and alg.charges_after_retry(2, True) == 1, "lịch lùi; tổng 750 ms; khoá lũy đẳng: 3 → 1 lần trừ")


# ── L05: vòng điều khiển, mô phỏng riêng ──
def ctrl(desired, kills):
    pods, h = list(range(desired)), []
    nxt = desired
    for k in kills:
        pods = pods[k:]
        h.append(len(pods))
        while len(pods) < desired:
            pods.append(nxt)
            nxt += 1
        h.append(len(pods))
    return h


rec("L05a", ctrl(3, [1, 0, 2]) == alg.reconcile(3, [1, 0, 2]) == [2, 3, 3, 3, 1, 3] and ctrl(5, [2, 0, 1]) == alg.reconcile(5, [2, 0, 1]), "3 nhịp; quiz 5 Pod")

# ── L06: số Pod vừa, tính theo phần mười CPU (số nguyên) ──
rec("L06a", (40 // 15, (40 - 40 // 15 * 15) / 10) == alg.pods_fit(4, 1.5) == (2, 1.0) and (80 // 25, (80 - 80 // 25 * 25) / 10) == alg.pods_fit(8, 2.5),
    "4 : 1,5 → 2 Pod thừa 1; 8 : 2,5 → 3 Pod thừa 0,5")
free = [40, 40]
place = []
for p in (15, 15, 15, 15, 10):
    i = next(j for j, x in enumerate(free) if x >= p)
    free[i] -= p
    place.append(i)
rec("L06b", (place, [x / 10 for x in free]) == alg.first_fit([4, 4], [1.5, 1.5, 1.5, 1.5, 1]), "xếp tham lam: Pod 1 CPU vào nút 1; thừa 0 và 1")


# ── L07: công thức co giãn bằng Decimal ──
def hpa_dec(cur, m, t, tol=Decimal("0.1")):
    r = Decimal(m) / Decimal(t)
    if abs(r - 1) <= tol:
        return cur
    return int((Decimal(cur) * r).to_integral_value(rounding=ROUND_CEILING))


cases = [(4, 90, 60, 6), (4, 63, 60, 4), (10, 20, 60, 4), (3, 80, 50, 5), (6, 66, 60, 6), (6, 67, 60, 7)]
rec("L07a", all(hpa_dec(c, m, t) == alg.hpa(c, m, t) == want for c, m, t, want in cases), "6; giữ 4; 4; quiz 5, 6 (biên dung sai), 7")


# ── L08: cuốn chiếu — mô phỏng rời rạc riêng, kiểm bất biến và đạt biên ──
def roll(n, frac=0.25):
    u, s = math.floor(n * frac), math.ceil(n * frac)
    old, new = n, 0
    lo, hi = n, n
    while old:
        add = min(n + s - (old + new), n - new)
        hi = max(hi, old + new + add)
        new += add
        rm = min(old, old + new - (n - u) - add) if False else min(old, (old + new - add) - (n - u))
        old -= max(0, rm)
        lo = min(lo, old + new - add)
    return u, s, lo, hi


rec("L08a", all(roll(n)[:2] == alg.rolling_update(n)[:2] and alg.rolling_update(n)[2] >= n - roll(n)[0] and alg.rolling_update(n)[3] <= n + roll(n)[1] for n in (4, 8, 10, 20, 7))
    and alg.rolling_update(10)[:4] == (2, 3, 8, 13) and alg.rolling_update(4)[:4] == (1, 1, 3, 5) and alg.rolling_update(8)[:4] == (2, 2, 6, 10),
    "u = ⌊n·25%⌋, s = ⌈n·25%⌉; bất biến giữ cho n = 4, 7, 8, 10, 20; 10 bản: ≥ 8, ≤ 13")


# ── L09: cân bằng tải, nhiều hạt giống ──
def lb(k, seed):
    g = np.random.default_rng(seed)
    load = np.zeros(100, int)
    for _ in range(20000):
        c = g.choice(100, k, replace=False)
        load[c[np.argmin(load[c])]] += 1
    return load.max()


m1 = [lb(1, s) for s in range(5)]
m2 = [lb(2, s) for s in range(5)]
rec("L09a", min(m1) > 225 and max(m2) <= 206 and (alg.lb_max_load(1), alg.lb_max_load(2)) == (243, 202),
    f"5 hạt giống numpy: chọn 1 → {m1}; chọn ít tải hơn trong 2 → {m2}; checklib hạt giống 1: 243 và 202")


# ── L10: mô phỏng sự kiện rời rạc M/M/1 ──
def sim_mm1(lam, mu, n=200000, seed=7):
    g = np.random.default_rng(seed)
    arr = np.cumsum(g.exponential(1 / lam, n))
    svc = g.exponential(1 / mu, n)
    free_at, tot = 0.0, 0.0
    for a, s in zip(arr, svc):
        start = max(a, free_at)
        free_at = start + s
        tot += free_at - a
    return tot / n


w80, w95 = sim_mm1(80, 100), sim_mm1(95, 100, n=400000)
rec("L10a", abs(w80 - 0.05) / 0.05 < 0.05 and abs(w95 - 0.2) / 0.2 < 0.15 and alg.mm1(80, 100)[:2] == (0.05, 4.0),
    f"mô phỏng: λ = 80 → {w80 * 1000:.1f} ms (lý thuyết 50); λ = 95 → {w95 * 1000:.0f} ms (lý thuyết 200)")
rec("L10b", round(1000 / (200 - 180)) == 50 and round(1000 / (200 - 190)) == 100 and Fraction(30, 600) == Fraction(1, 20) and alg.mm1(60, 100)[1] == 1.5,
    "quiz: 50 và 100 ms; Little 30/600 s = 50 ms")

# ── L11: phân vị (numpy inverted_cdf), Monte Carlo đuôi ──
lat = np.array([20] * 95 + [30, 40, 500, 800, 2000])
A, B = [10] * 98 + [1000] * 2, [10] * 900
p99 = lambda x: float(np.percentile(x, 99, method="inverted_cdf"))  # noqa: E731
rec("L11a", (lat.mean(), np.percentile(lat, 50, method="inverted_cdf"), p99(lat)) == (52.7, 20, 800) and (p99(A), p99(B), p99(A + B)) == (1000, 10, 10),
    "trung bình 52,7; p50 20; p99 800; gộp hai máy: p99 thật 10 (trung bình p99 là 505)")
slow = (rng.random((200000, 100)) < 0.01).any(axis=1).mean()
rec("L11b", abs(slow - 0.634) < 0.005 and round(alg.fanout_slow(0.01, 100), 3) == 0.634 and round(1 - 0.99 ** 10, 3) == 0.096 and round(1 - 0.999 ** 100, 3) == 0.095,
    f"Monte Carlo: {slow:.3f} ≈ 0,634; quiz 0,096 và 0,095")

# ── L12: ngân sách lỗi bằng timedelta ──
mins = lambda slo, d=30: datetime.timedelta(days=d).total_seconds() / 60 * (1 - slo)  # noqa: E731
rec("L12a", [round(mins(s), 2) for s in (0.99, 0.999, 0.9999, 0.995)] == [432.0, 43.2, 4.32, 216.0] and round(mins(0.999, 7), 2) == 10.08
    and round(alg.error_budget_min(0.999), 1) == 43.2, "432; 43,2; 4,32; 216 phút; 7 ngày: 10,08")

# ── L13: đọc lại lớp tar bằng code riêng; base64 bằng binascii ──
leaked_view, leaked = alg.layered_secret()
rec("L13a", leaked_view is False and leaked == b"MAT_KHAU=hunter2" and binascii.a2b_base64(b"aHVudGVyMg==") == b"hunter2" and binascii.b2a_base64(b"admin").strip() == b"YWRtaW4=",
    "hệ tệp ghép không thấy tệp, lớp 2 vẫn đọc được; base64 giải ngược được")


# ── L14: saga cài lại bằng ngoại lệ ──
def saga2(fail_at):
    steps = [("giữ ghế", "nhả ghế"), ("trừ tiền", "hoàn tiền"), ("xuất vé", "huỷ vé")]
    log, undo = [], []
    try:
        for i, (d, u) in enumerate(steps):
            if i == fail_at:
                raise RuntimeError(d)
            log.append(d)
            undo.append(u)
    except RuntimeError as e:
        log.append(f"{e}: LỖI")
        while undo:
            log.append(undo.pop())
    return log


rec("L14a", all(saga2(k) == alg.saga([("giữ ghế", "nhả ghế"), ("trừ tiền", "hoàn tiền"), ("xuất vé", "huỷ vé")], k) for k in (None, 0, 1, 2))
    and saga2(2)[-2:] == ["hoàn tiền", "nhả ghế"], "lỗi ở bước 2: nhả ghế; lỗi ở bước 3: hoàn tiền rồi nhả ghế")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
