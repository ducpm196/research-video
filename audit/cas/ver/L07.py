# CAS L07 — Cloudflare 2/7/2019. Đường KHÁC `checks`: datetime cho mọi khoảng; bộ đếm quay lui viết lại độc lập bằng vòng lặp lồng
# (không gọi alg.bt_match) theo đúng thứ tự thử của bộ máy tham (.* ăn nhiều nhất rồi nhả), đối chiếu với tổng alg.bt_match.
import datetime as dt
from fractions import Fraction as F

T = lambda hm: dt.datetime(2019, 7, 2, *map(int, hm.split(":")))
m = lambda a, b: int((T(b) - T(a)).total_seconds() // 60)
rec("L07a", m("13:42", "14:09") == 27, "13:42 → 14:09 = 27 phút (khớp TOC L14)")
rec("L07b", (m("13:42", "13:45"), m("13:42", "14:00"), m("14:02", "14:07"), m("14:09", "14:52"), m("13:31", "13:37")) == (3, 18, 5, 43, 6),
    "báo động 3, biết thủ phạm 18, tắt được sau 5, thử lại 43, dựng + kiểm thử 6 phút")
rec("L07c", round(60 * 24 / 476, 1) == 3.0, "476 thay đổi / 60 ngày ≈ 3 giờ một lần")


def tries_full(s):
    """Số lần thử của bộ máy tham trên .*.*=.* khớp TRỌN chuỗi s, viết lại không đệ quy.
    Đơn vị như alg.bt_match: mỗi lần .* thử thêm một ký tự (kể cả lần thử hỏng ở cuối), mỗi lần đặt '=' vào một vị trí."""
    n, t = len(s), 0
    t += n + 1                                  # .* thứ nhất: n lần ăn được + 1 lần hỏng
    for i in range(n, -1, -1):                  # nhả dần .* thứ nhất
        t += (n - i) + 1                        # .* thứ hai ăn phần còn lại + 1 lần hỏng
        for j in range(n, i - 1, -1):           # nhả dần .* thứ hai
            t += 1                              # thử đặt '='
            if j < n and s[j] == "=":
                t += (n - j - 1) + 1            # .* cuối ăn hết phần còn lại
                return True, t
    return False, t


def search(n):
    return sum(tries_full("x" * (n - k))[1] for k in range(n + 1))


ok_same = all(tries_full("x" * k) == alg.bt_match(".*.*=.*", "x" * k) for k in range(30))
rec("L07d", ok_same, "bộ đếm viết lại khớp alg.bt_match trên 0…29 chữ x")
rec("L07e", [search(n) for n in (2, 10, 20, 100, 200)] == [26, 638, 3773, 358853, 2767703], "tìm ở mọi vị trí: 26, 638, 3773, 358 853, 2 767 703")
rec("L07f", 7.6 < search(200) / search(100) < 7.8 and abs(F(200, 100) ** 3 - 8) == 0, "gấp đôi n: ×7,7 → bậc n mũ 3 (2 mũ 3 = 8)")
rec("L07g", F(8, 10) * 27 / (F(1, 100) * 8) == 270 and 4 * 15 == 60, "quiz: 21,6 / 0,08 = 270; 4 bậc × 15 phút = 60")
