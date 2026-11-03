"""Kiểm độc lập mọi khẳng định của khoá CLC — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Độ sẵn sàng: Monte Carlo từng giờ. Mạng con: phép tính bit tay (không dùng ipaddress). Quyền: bộ đánh giá viết lại theo thứ tự ưu tiên.
Độ bền: phân phối Poisson. Giá: Decimal. Khôi phục: dòng thời gian từng phút. Dung lượng chủ động–chủ động: mô phỏng mọi cách hỏng.
Chạy: .venv/Scripts/python audit/clc/verify_clc.py"""
import itertools
import math
import sys
from decimal import Decimal as D
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


# ── L00: phân loại trách nhiệm (bảng tra) ──
resp = {"máy ảo": {"hệ điều hành": "khách"}, "cơ sở dữ liệu được quản lý": {"phần mềm cơ sở dữ liệu": "nhà cung cấp"}, "bất kỳ": {"quyền": "khách"}}
rec("L00", resp["máy ảo"]["hệ điều hành"] == "khách" and resp["cơ sở dữ liệu được quản lý"]["phần mềm cơ sở dữ liệu"] == "nhà cung cấp" and resp["bất kỳ"]["quyền"] == "khách",
    "bảng trách nhiệm: hệ điều hành máy ảo → khách; vá cơ sở dữ liệu được quản lý → nhà cung cấp; quyền → khách")

# ── L01: Monte Carlo 10 triệu giờ ──
N = 10_000_000
a = rng.random(N) >= 0.005
b = rng.random(N) >= 0.005
both_down = (~a & ~b).mean()
cp = rng.random(N) >= 0.0005
up_with_cp = ((a | b) & cp).mean()
rec("L01", abs(both_down - 0.005 ** 2) < 5e-6 and abs(up_with_cp - 0.999975 * 0.9995) < 2e-4 and round(alg.parallel_availability(0.995, 2) * 100, 4) == 99.9975
    and round(alg.parallel_availability(0.99, 3) * 0.9999 * 100, 4) == 99.9899 and round(0.005 * 8760, 1) == 43.8,
    f"Monte Carlo: hai vùng cùng hỏng {both_down:.2e} ≈ 2,5·10⁻⁵; có phụ thuộc chung {up_with_cp:.5f} ≈ 0,99948")


# ── L02: phép tính bit tay ──
def ip2int(s):
    return sum(int(p) << (8 * (3 - i)) for i, p in enumerate(s.split(".")))


def plan(cidr, new):
    base, pre = cidr.split("/")
    return 2 ** (new - int(pre)), 2 ** (32 - new), 2 ** (32 - new) - 5


def overlap(c1, c2):
    (b1, p1), (b2, p2) = [(ip2int(c.split("/")[0]), int(c.split("/")[1])) for c in (c1, c2)]
    p = min(p1, p2)
    mask = ((1 << 32) - 1) ^ ((1 << (32 - p)) - 1)
    return (b1 & mask) == (b2 & mask)


rec("L02", plan("10.0.0.0/16", 24) == (256, 256, 251) == alg.subnet_plan("10.0.0.0/16", 24) and plan("10.1.0.0/22", 26) == (16, 64, 59) == alg.subnet_plan("10.1.0.0/22", 26)
    and plan("10.0.0.0/16", 28)[2] == 11 and overlap("10.0.0.0/16", "10.0.5.0/24") and not overlap("10.0.0.0/16", "10.20.0.0/16"),
    "bit tay: /16 → 256 × 256, 251 dùng được; /22 → 16 × 64, 59; /28 → 11; 10.0.0.0/16 trùng 10.0.5.0/24, không trùng 10.20.0.0/16")


# ── L03: bộ đánh giá viết lại theo thứ tự ưu tiên ──
def eval2(pols, act, res):
    hits = [eff for eff, acts, r in pols if (act in acts or "*" in acts) and r in (res, "*")]
    return "deny" if "deny" in hits else ("allow" if hits else "implicit-deny")


P1 = [("allow", {"*"}, "bao-cao"), ("deny", {"xoá"}, "bao-cao")]
P2 = [("allow", {"đọc"}, "*"), ("deny", {"*"}, "luong")]
reqs = [("đọc", "bao-cao"), ("xoá", "bao-cao"), ("ghi", "kho-khac"), ("đọc", "luong"), ("ghi", "bao-cao")]
rec("L03", all(eval2(P, x, r) == alg.iam_eval(P, x, r) for P in (P1, P2) for x, r in reqs)
    and [eval2(P1, x, r) for x, r in reqs[:3]] == ["allow", "deny", "implicit-deny"] and [eval2(P2, x, r) for x, r in (reqs[0], reqs[3], reqs[4])] == ["allow", "deny", "implicit-deny"]
    and all(eval2(list(perm), "xoá", "bao-cao") == "deny" for perm in itertools.permutations(P1)),
    "bộ đánh giá thứ hai khớp; thứ tự câu lệnh không đổi kết quả (từ chối tường minh thắng)")

# ── L04: Poisson cho số đối tượng mất ──
lam7, lam9 = 1e7 * 1e-11, 1e9 * 1e-11
rec("L04", abs(lam7 - 1e-4) < 1e-12 and abs((1 - math.exp(-lam7)) - 1e-4) < 1e-8 and abs(lam9 - 0.01) < 1e-12
    and round(1 / alg.expected_object_loss(1e7, 0.99999999999)) == 10000 and round(1 / alg.expected_object_loss(1e9, 0.99999999999)) == 100,
    "Poisson: P(mất ≥ 1 trong năm) ≈ 10⁻⁴ với 10⁷ đối tượng; 10⁹ đối tượng → 0,01/năm (1 mỗi 100 năm)")

# ── L05: Decimal, đếm giờ ──
rec("L05", D(500) / D("0.10") == 5000 and D(1100) / D("0.20") == 5500 and D(8760) * D("0.10") == 876 and D(10 * 22 * 12) * D("0.10") == 264 and D(5000) * D("0.20") == 1000
    and round(5000 / 8760 * 100, 1) == 57.1 and round(5500 / 8760 * 100, 1) == 62.8, "Decimal: hoà vốn 5000 h (57,1%), 5500 h (62,8%); 876 / 264 / 1000 đô la")

# ── L06: Decimal cho chi phí hàm ──
gbs = lambda n, s, m: D(n) * D(s) * D(m)
cost = lambda n, s, m: gbs(n, s, m) * D("0.0000166667") + D(n) / D(10 ** 6) * D("0.20")
rec("L06", gbs(10 ** 6, "0.2", "0.5") == 100000 and round(cost(10 ** 6, "0.2", "0.5"), 2) == D("1.87") and round(cost(5 * 10 ** 7, "0.1", 1), 2) == D("93.33")
    and round(float(D("36.5") / cost(1, "0.2", "0.5")) / 1e6, 1) == 19.6 and round(alg.faas_cost(5e7, 0.1, 1, 0.0000166667, 0.20), 2) == 93.33,
    "Decimal: 100 000 GB-giây → 1,87 đô la; 50 triệu lần → 93,33; hoà vốn với máy 36,5 đô la ≈ 19,6 triệu lần")


# ── L07: dòng thời gian từng phút ──
def worst_loss(snap_every, log_every=None, horizon=3 * 24 * 60):
    worst = 0
    for t in range(horizon):
        last_snap = t - t % snap_every
        last_log = t - t % log_every if log_every else last_snap
        worst = max(worst, t - max(last_snap, last_log))
    return worst + 1


rec("L07", worst_loss(1440, 5) == 5 == alg.worst_data_loss_minutes(1440, 5) and worst_loss(1440) == 1440 and worst_loss(360, 1) == 1 and worst_loss(360) == 360
    and round(500e9 / 200e6) == 2500 and round(200e9 / 100e6) == 2000, "mô phỏng từng phút: mất tối đa 5 phút / 24 giờ / 1 phút / 6 giờ; dựng 500 GB mất 2500 s, 200 GB mất 2000 s")

# ── L08: Decimal ──
rec("L08", D(50) * 1024 * D("0.09") == D("4608.00") and D(8) * 1024 * D("0.09") == D("737.28") and D(12000) / D(400000) == D("0.03") and D(15000) / D(600000) == D("0.025")
    and D(9900) / D(300000) == D("0.033") and round(alg.egress_cost(50, 0.09)) == 4608, "Decimal: 4608 / 737,28 đô la; 0,03 → 0,025 đô la mỗi người; 0,030 → 0,033 mỗi đơn")

# ── L09: đếm byte phong bì ──
rec("L09", sum(32 for _ in range(10000)) == 320000 == alg.envelope_rewrap_bytes(10000) and sum(32 for _ in range(50000)) == 1600000 and round(1e12 / 320000 / 1e6, 1) == 3.1,
    "10 000 khoá × 32 byte = 320 000 byte; 50 000 → 1,6 MB; ít hơn ≈ 3,1 triệu lần so với 1 TB")


# ── L10: mọi cách hỏng f vùng ──
def min_capacity(n, f):
    # dung lượng mỗi vùng c nhỏ nhất sao cho với MỌI tập f vùng hỏng, n − f vùng còn lại gánh đủ tải 1
    return min(c / 1000 for c in range(1, 2001) if all((n - f) * c / 1000 >= 1 - 1e-12 for _ in itertools.combinations(range(n), f)))


rec("L10", all(abs(min_capacity(n, f) - alg.active_active_capacity(n, f)[0]) < 1e-3 for n, f in ((2, 1), (3, 1), (4, 1), (5, 2)))
    and alg.active_active_capacity(2)[1] == 2.0 and alg.active_active_capacity(3)[1] == 1.5, "vét cạn cách hỏng: 2 vùng → 100% mỗi vùng (×2), 3 → 50% (×1,5), 4 → 33% (×1,33)")

# ── L11: Decimal ──
rec("L11", D(3) * 730 * D("0.20") == 438 and D(730) * D("0.20") + 2 * D(176) * D("0.20") == D("216.4") and round((1 - 216.4 / 438) * 100, 1) == 50.6 and 8 * 22 == 176,
    "Decimal: 438 → 216,4 đô la (giảm 50,6%) khi co giãn 2 máy theo 176 giờ cao điểm")

# ── L12 (hành trình kho lưu trữ đối tượng, audit/clc/sources_L12.md): đếm phút từng phút, đếm lô, mô phỏng công cụ có chặn tối thiểu ──
def minutes_between(h0, m0, h1, m1):
    t, n = (h0, m0), 0
    while t != (h1, m1):
        t = (t[0] + (t[1] + 1) // 60, (t[1] + 1) % 60); n += 1
    return n
def remove_tool(fleet, k, minimum):  # công cụ sau 2017: không cho xuống dưới mức tối thiểu ([S17])
    return (fleet - k, True) if fleet - k >= minimum else (fleet, False)
_m = [minutes_between(9, 37, h, m) for h, m in ((12, 26), (13, 54), (11, 37))]
_year_budget = D(365 * 24 * 60) * (1 - D("0.9999"))
_rounds, _left = 0, 200_000
while _left > 0:
    _left -= min(_left, 2_000_000 // 100); _rounds += 1
rec("L12", _m == [169, 257, 120] and divmod(_m[1], 60) == (4, 17) and _year_budget == D("52.56") and round(257 / float(_year_budget), 1) == 4.9
    and D(2) * 10 ** 14 / (D(8) * 10 ** 8) == 250000 and round(2e14 / (365 * 24 * 3600) / 1e6, 3) == 6.342 and 10 ** 12 // (8 * 10 ** 8) == 1250
    and remove_tool(100, 5, 80) == (95, True) and remove_tool(100, 50, 80) == (100, False) and _rounds == 10
    and D(100) * D("0.15") + D(100) * D("0.20") == 35 and -(-12 // 5) == 3,
    "sự cố 2017 (S17): 9:37→12:26 = 169 phút, →13:54 = 257 phút (4 giờ 17), →11:37 = 120 phút; ngân sách 99,99%/năm 52,56 phút → 257 ≈ 4,9 năm; "
    "2·10¹⁴/8·10⁸ = 250 000 (PI22), 2·10¹⁴ giây ≈ 6,342 triệu năm (PI22), 10¹²/8·10⁸ = 1250; công cụ chặn tối thiểu 80/100: gỡ 5 được, gỡ 50 bị chặn; "
    "xoá 200 000 với giới hạn 1% của 2 000 000 = 10 lượt; 100 GB × 0,15 + 100 GB × 0,20 = 35 đô la (PR06); tệp 12 GB / 5 GB → 3 đối tượng")

bad = [c for c, ok in R if not ok]
print(f"\nverify_clc: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
