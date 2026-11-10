# SEP L10 — tính lại bằng datetime, liệt kê cây phụ thuộc, so phiên bản bằng bộ so khớp tự viết (khác `checks` của bài).
import datetime as dt
import itertools

t0, t1, t2 = (dt.datetime(2016, 3, 22, h, m) for h, m in ((14, 30), (16, 5), (16, 55)))
rec("L10a", (t2 - t0) == dt.timedelta(minutes=145) and round((t2 - t0).total_seconds() / 3600, 1) == 2.4
    and (t2 - t1) == dt.timedelta(minutes=50) and dt.date(2016, 3, 22).strftime("%A") == "Tuesday",
    "14:30 → 16:55 = 145 phút ≈ 2,4 giờ (nguồn: 2,5 giờ); 16:05 → 16:55 = 50 phút; 22/3/2016 là thứ Ba")


def leaves(depth, fan=3):
    """liệt kê mọi đường đi tới gói ở tầng 1..depth của một cây đều nhánh"""
    return [p for d in range(1, depth + 1) for p in itertools.product(range(fan), repeat=d)]


rec("L10b", len(leaves(3)) == 39 and sum(1 for p in leaves(3) if len(p) == 3) == 27 and (3 ** 4 - 3) // 2 == 39,
    "liệt kê cây 3 nhánh sâu 3 tầng: 39 gói, 27 ở tầng 3")


def exact_match(req, have):
    return tuple(int(x) for x in req.split(".")) == tuple(int(x) for x in have.split("."))


rec("L10c", exact_match("0.0.3", "0.0.3") and not exact_match("0.0.3", "1.0.0") and 1 + 272 == 273,
    "yêu cầu đúng 0.0.3: 1.0.0 không khớp; 273 gói bị gỡ")


def can_unpublish(age_h, dependents, weekly_dl, owners):
    """chính sách hiện hành [N26]: < 72 giờ và không ai phụ thuộc; hoặc đủ cả ba điều kiện"""
    return (age_h < 72 and dependents == 0) or (dependents == 0 and weekly_dl < 300 and owners == 1)


rec("L10d", not can_unpublish(2 * 365 * 24, 12, 4000, 1) and can_unpublish(10, 0, 5000, 3) and can_unpublish(10000, 0, 299, 1)
    and not can_unpublish(10000, 0, 300, 1) and 52 * 2 == 104,
    "quiz: gói 2 năm, 12 phụ thuộc, 4000 lượt/tuần → không tự gỡ được; ca biên 299/300 lượt; 104 lần dựng/năm")
# Thêm 2026-11-09 (đợt C): đường kiểm 39 gói nay giải thích phép dịch tầng: 3S − S = 81 − 3.
_S = 3 + 9 + 27
rec("L10e", 3 * _S - _S == 81 - 3 and (81 - 3) // 2 == _S == 39, "tổng 3 + 9 + 27: 3S − S = 78 → S = 39")
