"""Kiểm độc lập mọi khẳng định số của khoá ESY — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Bit: thao tác trên chuỗi nhị phân thay cho toán tử bit. Chống dội, PWM, lập lịch: mô phỏng lại từ đầu bằng vòng lặp riêng (theo sự kiện).
Phân tích thời gian đáp ứng: vét cạn mô phỏng tới siêu chu kỳ (bội chung nhỏ nhất). Dấu phẩy tĩnh: Fraction. Thời gian lên RC: giải
phương trình 1 − e^{−t/RC} bằng sympy. Lấy trung bình nhiễu: Monte Carlo với hạt giống khác.
Chạy: .venv/Scripts/python audit/esy/verify_esy.py → PASS/FAIL từng dòng và tổng."""
import math
import sys
import zlib
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: bộ nhớ, tần số ──
rec("L00a", (16 * 1024 ** 3) / (2 * 1024) == 8388608, "16 GB / 2 KB = 8 388 608 lần")
rec("L00b", abs(16e6 / 3e9 - 0.00533) < 1e-4, "16 MHz / 3 GHz ≈ 0,0053")
rec("L00c", (sum([1] * 99 + [30]) / 100, max([1] * 99 + [30])) == (1.29, 30), "trung bình 1,29 ms nhưng xấu nhất 30 ms")


# ── L01: bit bằng chuỗi ──
def set_bit_str(v, k, b):
    s = list(format(v, "08b"))
    s[7 - k] = str(b)
    return int("".join(s), 2)


def flip_str(v, k):
    s = format(v, "08b")
    return set_bit_str(v, k, 1 - int(s[7 - k]))


r = 0b10010001
rec("L01a", (set_bit_str(r, 5, 1), set_bit_str(177, 5, 0), flip_str(r, 3)) == (177, 145, 153), "145 → 177 → 145; đảo bit 3 → 153")
rec("L01b", alg.bit_ops(145)[:1] == (177,) and alg.bit_ops(177)[1] == 145 and alg.bit_ops(145)[2] == 153, "khớp alg.bit_ops")
q = 0b01010101
rec("L01c", (set_bit_str(q, 1, 1), set_bit_str(q, 6, 0), format(q, "08b")[7 - 4], format(q, "08b")[7 - 3]) == (87, 21, "1", "0"), "quiz: 87, 21, bit4=1, bit3=0")
rec("L01d", [i for i, c in enumerate(reversed(format(145, "08b"))) if c == "1"] == [0, 4, 7], "145 = đèn 0, 4, 7")


# ── L02: chống dội (mô phỏng riêng), đọc rách ──
def deb(samples, n):
    out, state, cnt, prev = [], samples[0], 0, None
    for x in samples:
        cnt = cnt + 1 if x == prev else 1
        prev = x
        if cnt >= n and x != state:
            state = x
        out.append(state)
    return out


raw = [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
rec("L02a", deb(raw, 5) == alg.debounce(raw, 5) and deb(raw, 5).index(1) == 10, "trạng thái sạch đổi ở mẫu 10, một lần")
rec("L02b", sum(1 for a, b in zip(deb(raw, 5), deb(raw, 5)[1:]) if a != b) == 1, "chỉ đổi một lần")
rec("L02c", int("01" + "FF", 16) == 511 and int("02" + "FF", 16) == 767, "đọc rách: 0x01FF = 511, 0x02FF = 767")
rec("L02d", math.ceil(5 / 1) == 5 and math.ceil(8 / 2) == 4, "số mẫu 5 và 4")

# ── L03: bộ định thời, PWM ──
f = Fraction(16_000_000, 64 * 250)
rec("L03a", f == 1000 and alg.timer_freq(16e6, 64, 249) == 1000, "16 MHz/64/250 = 1000 Hz")
cnt = [k % 250 for k in range(2500)]
rec("L03b", Fraction(sum(1 for c in cnt if c < 63), len(cnt)) == Fraction(63, 250), "độ rộng xung 63/250 = 25,2% (mô phỏng 10 chu kỳ)")
rec("L03c", round(0.252 * 5, 2) == 1.26 and round(16e6 / (64 * 249), 1) == 1004.0, "1,26 V; lỗi lệch một 1004 Hz")
rec("L03d", abs(1004.016 - 1000) / 1000 * 86400 / 60 > 5.7 and abs(1004.016 - 1000) / 1000 * 86400 / 60 < 5.8, "lệch 0,4% ≈ 5,8 phút/ngày (“gần 6 phút”)")
rec("L03e", Fraction(8_000_000, 8 * 1000) - 1 == 999 and Fraction(500, 1000) == Fraction(1, 2), "quiz: TOP 999, CMP 500")

# ── L04: ADC ──
rec("L04a", abs(3.3 / 1024 - 0.00322) < 1e-5 and alg.adc_volts(512, 10, 3.3) == 1.65, "bậc 3,22 mV; 512 → 1,65 V")
rec("L04b", int(1.0 * 1024 // 3.3) == 310 and abs(310 * 3.3 / 1024 - 0.999) < 1e-3, "1 V → 310 → 0,999 V")
v = np.linspace(0, 3.3, 200001, endpoint=False)
codes = np.floor(v * 1024 / 3.3)
err = v - codes * 3.3 / 1024
sig = 1.65 * np.sin(np.linspace(0, 2 * np.pi * 50, 400000, endpoint=False)) + 1.65
qs = np.floor(sig * 1024 / 3.3).clip(0, 1023) * 3.3 / 1024 + 3.3 / 2048
snr = 10 * np.log10(np.var(sig) / np.var(sig - qs))
rec("L04c", err.min() >= 0 and err.max() < 3.3 / 1024, "sai số lượng tử nằm trong [0, 1 bậc)")
rec("L04d", abs(snr - (6.02 * 10 + 1.76)) < 0.3, f"SNR mô phỏng sin toàn thang 10 bit = {snr:.2f} dB ≈ 61,96")
rec("L04e", round(10 / (3.3 / 1024 * 1000)) == 3 and round(10 / (3.3 / 4096 * 1000)) == 12, "nhiễu 10 mV ≈ 3 bậc / 12 bậc")
rec("L04f", int(2.0 * 4096 // 3.3) == 2482 and round(512 * 3.3 / 1023, 4) == 1.6516, "quiz 2482; quy ước 1023 → 1,6516 V")

# ── L05: lọc ──
x = [0, 0, 0, 1, 1, 1, 1]
ma = [float(np.mean(x[max(0, k - 3):k + 1] + [0] * max(0, 3 - k))) for k in range(len(x))]
rec("L05a", ma == [0, 0, 0, 0.25, 0.5, 0.75, 1.0], "trung bình trượt 4 mẫu: 0, 0,25, 0,5, 0,75, 1")
rng = np.random.default_rng(12345)
rec("L05b", abs(rng.normal(0, 1, (300000, 4)).mean(axis=1).std() - 0.5) < 0.01, "nhiễu độc lập: độ lệch chuẩn giảm √4 = 2 lần")
y, ys = Fraction(0), []
for _ in range(10):
    y = y + Fraction(1, 5) * (1 - y)
    ys.append(y)
yalg = 0.0
for _ in range(10):
    yalg = alg.ema_step(yalg, 1, 0.2)
rec("L05c", ys[0] == Fraction(1, 5) and ys[1] == Fraction(9, 25) and abs(float(ys[-1]) - 0.8926) < 1e-4 and abs(yalg - float(ys[-1])) < 1e-12, "đáp ứng bước a=0,2: 0,2; 0,36; …; 0,8926")
yi = 25
for _ in range(50):
    yi = yi + (26 - yi) // 4
rec("L05d", yi == 25, "lọc số nguyên chia trước: chênh lệch 1 không bao giờ bắt kịp")
rec("L05e", 1 - Fraction(1, 2) ** 3 == Fraction(7, 8) and abs(1 / math.sqrt(8) - 0.354) < 1e-3, "quiz 0,875; 0,354")
drift = np.cumsum(np.full(4000, 0.001))
rec("L05f", abs(np.mean(drift[-4:]) - drift[-1]) < 0.002, "nhiễu trôi chậm: trung bình 4 mẫu gần như không giảm")

# ── L06: dấu phẩy tĩnh bằng Fraction ──
qv = lambda z: Fraction(z) / 256
rec("L06a", qv(384) == Fraction(3, 2) and qv(576) == Fraction(9, 4) and qv(864) == Fraction(27, 8), "384·576 → 864 = 3,375")
rec("L06b", 384 * 576 > 2 ** 16 - 1 and alg.q_mul(384, 576)[0] == 864, "tích trung gian vượt 16 bit")


def wrap16(z):
    return (z + 2 ** 15) % 2 ** 16 - 2 ** 15


raw6 = (25600 * 512) // 256
rec("L06c", wrap16(raw6) == -14336 and qv(-14336) == -56 and alg.q_mul(25600, 512) == (32767, -14336), "100·2: quay vòng −56, bão hoà 32767")
rec("L06d", wrap16((16384 * 1024) // 256) == 0 and alg.q_mul(16384, 1024) == (32767, 0), "64·4: quay vòng 0")
rec("L06e", qv(96) == Fraction(3, 8) and alg.q_mul(192, 128)[0] == 96, "0,75·0,5 = 0,375")
rec("L06f", (-3) >> 1 == -2 and (256 * 128 + 128) >> 8 == 128 and float(qv(32767)) - 127.996 < 1e-3, "dịch phải làm tròn xuống; cộng 128; biên 127,996")

# ── L07: UART ──
frame = [0] + [int(c) for c in reversed(format(0x41, "08b"))] + [1]
rec("L07a", frame == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1] and len(frame) == 10, "khung 8N1 của 'A' = 10 bit")
rec("L07b", 9600 // 10 == 960 and abs(1 / 9600 - 0.000104) < 1e-6, "960 byte/s; 0,104 ms mỗi bit")
best = {B: min(range(256), key=lambda u: abs(16e6 / (16 * (u + 1)) - B)) for B in (9600, 115200)}
rec("L07c", best == {9600: 103, 115200: 8}, "UBRR tốt nhất 103 và 8")
rec("L07d", round((16e6 / 1664 - 9600) / 96, 2) == 0.16 and round((16e6 / 144 - 115200) / 1152, 2) == -3.55, "lệch +0,16% và −3,55%")
rec("L07e", abs(0.5 / 9.5 - 0.0526) < 1e-3, "ngưỡng tổng 0,5/9,5 ≈ 5,3%")
rec("L07f", [int(c) for c in reversed(format(0x4B, "08b"))] == [1, 1, 0, 1, 0, 0, 1, 0] and 115200 // 10 == 11520, "quiz 0x4B; 11 520 byte/s")

# ── L08: I²C ──
t, Rr, C = sp.symbols("t R C", positive=True)
t30 = sp.solve(sp.Eq(1 - sp.exp(-t / (Rr * C)), sp.Rational(3, 10)), t)[0]
t70 = sp.solve(sp.Eq(1 - sp.exp(-t / (Rr * C)), sp.Rational(7, 10)), t)[0]
k = sp.N(sp.simplify((t70 - t30) / (Rr * C)))
rec("L08a", abs(float(k) - 0.8473) < 1e-4, f"thời gian lên 30%→70% = {float(k):.4f} RC")
rec("L08b", round(300e-9 / (float(k) * 200e-12)) == 1770 and round(1000e-9 / (float(k) * 200e-12)) == 5901, "R_max 1770 Ω (400 kHz), 5901 Ω (100 kHz)")
rec("L08c", round(2.9 / 0.003) == 967 and round(300e-9 / (float(k) * 100e-12)) == 3541, "R_min 967 Ω; quiz 3541 Ω")
rec("L08d", int(format(0x48, "07b") + "0", 2) == 0x90 and int(format(0x3C, "07b") + "1", 2) == 0x79, "byte địa chỉ 0x90; 0x78/0x79")


# ── L09, L10: mô phỏng theo sự kiện, khác alg.schedule_sim ──
def sim(tasks, horizon, edf):
    rem = [0] * len(tasks)
    dl = [0] * len(tasks)
    tl, miss = [], []
    for now in range(horizon):
        for i, (c, p) in enumerate(tasks):
            if now % p == 0:
                if rem[i] > 0:
                    miss.append((i, now))
                rem[i], dl[i] = c, now + p
        ready = [i for i in range(len(tasks)) if rem[i] > 0]
        if not ready:
            tl.append(None)
            continue
        i = min(ready, key=(lambda i: (dl[i], i)) if edf else (lambda i: (tasks[i][1], i)))
        rem[i] -= 1
        tl.append(i)
    return tl, miss


def resp(tasks, i):
    """Thời gian đáp ứng xấu nhất bằng mô phỏng RM tới siêu chu kỳ (mọi tác vụ thả ở 0)."""
    H = math.lcm(*[p for _, p in tasks])
    tl, miss = sim(tasks, H, False)
    if any(j == i for j, _ in miss):
        return None
    worst, p = 0, tasks[i][1]
    for s in range(0, H, p):
        last = max(k for k in range(s, s + p) if tl[k] == i)
        worst = max(worst, last + 1 - s)
    return worst


rec("L09a", round(3 * (2 ** (1 / 3) - 1), 4) == round(alg.rm_bound(3), 4) == 0.7798 and round(alg.rm_bound(2), 4) == 0.8284, "cận 0,7798 và 0,8284")
T1 = [(1, 4), (2, 6), (3, 12)]
rec("L09b", [resp(T1, i) for i in range(3)] == [1, 3, 10] == [r for r, _ in alg.rta(T1)], "R = 1, 3, 10 (mô phỏng = phép lặp)")
rec("L09c", Fraction(1, 4) + Fraction(2, 6) + Fraction(3, 12) == Fraction(5, 6), "U = 5/6 ≈ 0,833 > 0,780")
rec("L09d", sim(T1, 12, False)[0] == alg.schedule_sim(T1, 12, "RM")[0], "biểu đồ Gantt khớp")
T2 = [(2, 5), (2, 7), (2, 10)]
rec("L09e", resp(T2, 2) == 10 == alg.rta(T2)[2][0] and abs(sum(Fraction(c, p) for c, p in T2) - Fraction(31, 35)) == 0, "quiz: R = 10, U = 31/35 ≈ 0,886")
T3 = [(2, 4), (3, 6)]
rec("L09f", resp(T3, 1) is None and alg.rta(T3)[1][0] is None, "U = 1 mà RM trễ")
rec("L10a", sim(T3, 12, True)[1] == [] and sim(T3, 12, False)[1] == [(1, 6)], "EDF kịp, RM trễ ở 6")
rec("L10b", sim(T3, 12, True)[0] == alg.schedule_sim(T3, 12, "EDF")[0] and sim(T3, 12, False)[0][:11] == alg.schedule_sim(T3, 12, "RM")[0][:11], "Gantt EDF/RM khớp")
T4 = [(2, 4), (3, 6), (1, 5)]
m_rm = {i for i, _ in alg.schedule_sim(T4, 60, "RM")[1]}
m_edf = {i for i, _ in alg.schedule_sim(T4, 60, "EDF")[1]}
rec("L10c", m_rm == {1} and m_edf == {0, 1, 2}, "quá tải U = 1,2: RM chỉ trễ (3,6); EDF trễ cả ba")
T5 = [(1, 3), (2, 5), (1, 4)]
rec("L10d", sum(Fraction(c, p) for c, p in T5) == Fraction(59, 60) and sim(T5, 60, True)[1] == [], "quiz EDF: U = 59/60, kịp")


def inversion(m_len, inherit):
    """Thấp giữ khoá cần thêm 3; Cao tới ở 1 (cần khoá, 1 đơn vị); Trung bình tới ở 2, chạy m_len. Trả thời điểm Cao xong."""
    low, high, mid, now, lock = 3, 1, m_len, 0, True
    while high > 0:
        h_ready = now >= 1 and not lock
        m_ready = now >= 2 and mid > 0
        low_prio = 3 if (inherit and now >= 1 and lock) else 1
        if h_ready:
            high -= 1
        elif m_ready and 2 > low_prio:
            mid -= 1
        elif low > 0:
            low -= 1
            if low == 0:
                lock = False
        now += 1
    return now


rec("L10e", inversion(4, False) == 8 and inversion(4, True) == 4, "không kế thừa: Cao xong ở 8 (đáp ứng 7); kế thừa: 4 (đáp ứng 3)")
rec("L10f", inversion(5, False) == 9, "quiz: Trung bình 5 đơn vị → Cao xong ở 9")

# ── L11: hàng đợi ──
rec("L11a", math.ceil(Fraction(11520, 100)) == 116 and math.ceil(Fraction(960 * 2, 100)) == 20, "116 chỗ; quiz 20 chỗ")
rec("L11b", abs(1e6 / 11520 - 86.8) < 0.1, "một byte mỗi 86,8 µs")

# ── L12 ──
rec("L12a", Fraction(248 * 5, 4) == 310 and Fraction(320 * 5, 4) == 400, "ngăn xếp 310 và 400 byte")
heap = ["A", None, "C", None, "E"]
runs, cur = [], 0
for b in heap + ["X"]:
    if b is None:
        cur += 200
    else:
        runs.append(cur)
        cur = 0
rec("L12b", sum(200 for b in heap if b is None) == 400 and max(runs) == 200 < 300, "trống 400, khối liền lớn nhất 200")

# ── L13 ──
rec("L13a", Fraction(1, 100) * 10 + Fraction(99, 100) * Fraction(1, 100) == Fraction(1099, 10000) and abs(alg.avg_current(0.01, 10, 0.01) - 0.1099) < 1e-12, "dòng TB 0,1099 mA")
rec("L13b", round(1000 / 0.1099 / 24) == 379 and round(1000 / 0.0599 / 24) == 696 and round(1000 / 0.199 / 24) == 209, "379, 696, 209 ngày")
part_sleep = Fraction(9999, 10000) * Fraction(1, 100) / (Fraction(1, 10000) * 10 + Fraction(9999, 10000) * Fraction(1, 100))
rec("L13c", round(float(part_sleep), 2) == 0.91 and round(0.1 / 0.1099, 2) == 0.91, "phần ngủ 91% khi thức 0,01%; phần thức 91% khi thức 1%")
rec("L13d", round(1000 / (0.001 * 20 + 0.999 * 0.005)) == 40008 and round(1000 / (0.001 * 20 + 0.999 * 0.005) / 24) == 1667, "quiz 40 008 giờ, 1667 ngày")

# ── L14 ──
rec("L14a", zlib.crc32(b"dat toc do 50") != zlib.crc32(b"dat toc do 99"), "CRC đổi khi sửa — nhưng kẻ xấu tính lại được")
rec("L14b", 2 * 400 + 32 <= 1024 < 2 * 600 + 64 and abs(2 ** -32 - 2.33e-10) < 1e-12, "832 ≤ 1024 < 1264; 2^−32 ≈ 2,33·10^−10")

# ── L15 (bài hành trình; nguồn audit/esy/sources_L15.md) ──
def _deliver(t_wake, medium, hold, work, inherit):
    """Mô phỏng từng mi li giây: tác vụ phân phát (cao) chờ khoá của tác vụ khí tượng (thấp), tác vụ trung bình chen vào."""
    t, med, low, w = t_wake, medium, hold, work
    while w:
        if low:                      # khoá còn bị giữ: ai chạy?
            if inherit or not med:   # kế thừa: tác vụ thấp mang ưu tiên cao → chạy trước tác vụ trung bình
                low -= 1
            else:
                med -= 1
        else:
            w -= 1
        t += 1
    return t


rec("L15a", 1 / 8 == 0.125 and _deliver(40, 60, 2, 15, False) == 117 > 110 and _deliver(40, 30, 2, 15, False) == 87 <= 110
    and _deliver(40, 60, 2, 15, True) == 57 and max(m for m in range(200) if _deliver(40, m, 2, 15, False) <= 110) == 53,
    "8 Hz → 125 ms; không kế thừa: 117 (tải 60) / 87 (tải 30); kế thừa: 57; tải tối đa còn kịp hạn 53 ms")
rec("L15b", 18 * 3600 * 8 == 518400, "18 giờ ở 8 Hz = 518 400 chu kỳ")
rec("L15c", 3000 + 2000 + 1000 == 6000 and 6000 // 100 == 60 and 4096 // 256 == 16 and 2 ** 13 == 8192, "mục nhiều nhất từng có 6000 = 60 × 100; 16 lần nới 256 KB; 8192 = 2^13")
_resets = [m for m in range(1, 1477) if m % 90 in (15, 30, 0)]
rec("L15d", round(1477 / 90 * 3, 1) == 49.2 and len(_resets) == 50 and _resets[:6] == [15, 30, 90, 105, 120, 180]
    and round(15 * 1477 / 1440, 1) == 15.4, "mẫu 15–15–60: 49,2 lần/sol trung bình, liệt kê từ phút 0 được 50; 15 sol ≈ 15,4 ngày")
rec("L15e", 800 // 256 == 3 and 300 * 48 // 24 == 600 and round(600 / 8192 * 100, 1) == 7.3 and round(300 / 8192 * 100, 1) == 3.7,
    "ngưỡng 800 KB = 3 lần nới; 300 sản phẩm/ngày: 600 tệp (48 h) → 300 (24 h)")
import datetime as _dt
rec("L15f", round((_dt.date(2014, 8, 29) - _dt.date(2004, 1, 25)).days / 365.25, 1) == 10.6 and round(10.6 / 0.25) == 42
    and round(6 / 7 * 100, 1) == 85.7 and round((_dt.date(2018, 11, 18) - _dt.date(2014, 9, 21)).days / 365.25, 1) == 4.2
    and (600 - 100) // 20 == 25 and 90 * 20 == 1800,
    "Opportunity ≈ 10,6 năm ≈ 42 × 3 tháng; 6/7 ≈ 85,7%; RapidScat ≈ 4,2 năm; câu đố 25 ngày, 1800 KB")

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
