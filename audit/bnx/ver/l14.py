"""Kiểm độc lập BNX L14 — tính lại bằng đường KHÁC checklib (số nguyên thuần thay cho phân số, đếm ngày theo độ dài tháng,
chạy thật đúng chuỗi mã Python đang hiện trên màn hình), rồi đối chiếu với alg.bnx_l14_*."""
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l14  # noqa: E402


def bucket_int(rate, cap, n, ticks_per_sec, simultaneous=False):
    """Mô phỏng bằng SỐ NGUYÊN: yêu cầu thứ i đến ở nhịp i (mỗi nhịp 1/ticks_per_sec giây); đếm thẻ theo đơn vị 1/ticks_per_sec thẻ.
    Mỗi nhịp thùng thêm `rate` đơn vị (= rate/ticks_per_sec thẻ); một yêu cầu cần `ticks_per_sec` đơn vị; thùng đầy = cap·ticks_per_sec."""
    unit, full = ticks_per_sec, cap * ticks_per_sec
    tok, got, idx = full, 0, []
    for i in range(n):
        if i and not simultaneous:
            tok = min(full, tok + rate)
        if tok >= unit:
            tok -= unit
            got += 1
            idx.append(i)
    return got, idx


def run(rec):
    # 1) 30 yêu cầu cùng lúc
    g0, _ = bucket_int(5, 10, 30, 30, simultaneous=True)
    rec("L14", g0 == 10 == alg.bnx_l14_bucket(5, 10, [0] * 30), f"cùng lúc: số nguyên {g0}, checklib {alg.bnx_l14_bucket(5, 10, [0] * 30)} → nhận 10")
    rec("L14", 30 - g0 == 20, "cùng lúc: từ chối 30 − 10 = 20")
    # 2) rải đều 0, 1/30, …, 29/30 (nhịp 1/30 s; mỗi nhịp thêm 5 đơn vị = 5/30 = 1/6 thẻ; một thẻ = 30 đơn vị)
    g1, idx = bucket_int(5, 10, 30, 30)
    rec("L14", g1 == 14 == alg.bnx_l14_bucket(5, 10, alg.bnx_l14_spread(30)), f"rải đều: số nguyên {g1} → nhận 14")
    rec("L14", idx == list(range(11)) + [12, 18, 24] == alg.bnx_l14_accepted_idx(5, 10, alg.bnx_l14_spread(30)),
        f"thời điểm được nhận (theo phần ba mươi giây): {idx}")
    rec("L14", 30 - g1 == 16, "rải đều: từ chối 30 − 14 = 16")
    # sau yêu cầu thứ 11 còn 300 + 50 − 330 = 20 đơn vị (= 2/3 thẻ): thêm 2 nhịp (10 đơn vị) là đủ 30 → nhận ở nhịp 12; rồi 6 nhịp/thẻ
    rec("L14", 300 + 10 * 5 - 11 * 30 == 20 and (30 - 20) // 5 == 2 and 30 // 5 == 6 and [10 + 2, 12 + 6, 18 + 6] == idx[11:],
        "từ 2/3 thẻ: thêm 2 khoảng (nhận ở 12/30), rồi cứ 6 khoảng = 1/5 giây (18/30, 24/30)")
    # số thẻ trước yêu cầu thứ 11 (chỉ số 10): 300 + 10·5 − 10·30 = 50 đơn vị = 50/30 = 5/3 thẻ
    rec("L14", Fraction(300 + 10 * 5 - 10 * 30, 30) == Fraction(5, 3) == alg.bnx_l14_bucket_trace(5, 10, alg.bnx_l14_spread(30))[10][1],
        "trước yêu cầu thứ 11 còn 5/3 thẻ")
    rec("L14", Fraction(270 + 5, 30) == Fraction(55, 6) == alg.bnx_l14_bucket_trace(5, 10, alg.bnx_l14_spread(30))[1][1],
        "còn 9 thẻ, sau 1/30 giây: 55/6")
    # 3) cận trên b + r·T: tính bằng số nguyên (300 + 5·29)//30
    rec("L14", (300 + 5 * 29) // 30 == 14 == alg.bnx_l14_bound(5, 10, Fraction(29, 30)) and Fraction(300 + 145, 30) == Fraction(89, 6),
        "cận trên rải đều 89/6 ≈ 14,8 → 14; cùng lúc 10")
    rec("L14", f"{445 / 30:.1f}" == "14.8", "89/6 làm tròn một chữ số thập phân = 14,8")
    # 4) chạy thật đúng chuỗi mã trên màn hình
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", l14.BUCKET_PY], capture_output=True, text=True, encoding="utf-8")
    rec("L14", r.returncode == 0 and r.stdout.split() == ["10", "14"] and r.stdout.strip() == l14.BUCKET_OUT,
        f"chạy thật mã trên màn hình: stdout {r.stdout.split()} (khối 'Kết quả chạy thật' ghi {l14.BUCKET_OUT.split()})")
    # 5) quiz
    q1, _ = bucket_int(5, 10, 40, 30, simultaneous=True)
    rec("L14", (q1, 40 - q1) == (10, 30) and q1 == alg.bnx_l14_bucket(5, 10, [0] * 40), "quiz 1: 40 cùng lúc → nhận 10, từ chối 30")
    # cổng 2 thẻ/giây, sức chứa 3, nhịp 1/4 giây: đơn vị = 1/4 thẻ … mỗi nhịp thêm 2 đơn vị; một thẻ = 4 đơn vị
    q2, idx2 = bucket_int(2, 3, 6, 4)
    rec("L14", q2 == 5 == alg.bnx_l14_bucket(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2))) and idx2 == [0, 1, 2, 3, 4],
        f"quiz 2: nhận {q2} (yêu cầu thứ 6 bị từ chối)")
    rec("L14", (12 + 2 * 5) // 4 == 5 == alg.bnx_l14_bound(2, 3, Fraction(5, 4)) and Fraction(12 + 10, 4) == Fraction(11, 2),
        "quiz 2: cận trên 3 + 2·5/4 = 5,5 → 5")
    # 6) aggregate Tài khoản (số dư không âm)
    rec("L14", alg.bnx_l14_debit(300000, 500000) == (300000, False) and alg.bnx_l14_debit(300000, 200000) == (100000, True)
        and 300000 - 200000 == 100000 and not (300000 - 500000 >= 0), "ghi nợ 500 000 từ 300 000 bị từ chối; ghi nợ 200 000 còn 100 000")
    rec("L14", 80 + 30 == 110 and 110 > 100, "hạn mức chuyển (số minh hoạ): 80 + 30 = 110 > 100 triệu → từ chối")
    # 7) ngày của Thông tư 64: đếm theo độ dài tháng (năm 2025 không nhuận)
    leap = (2025 % 4 == 0 and 2025 % 100 != 0) or 2025 % 400 == 0
    days = 1 + 31 + (29 if leap else 28)          # 31/12 → 01/01, cả tháng 1, cả tháng 2
    rec("L14", days == 60 == alg.bnx_l14_days("31/12/2024", "01/03/2025"), f"31/12/2024 → 01/3/2025: {days} ngày")
