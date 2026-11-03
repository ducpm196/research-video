# CAS L06 — Amazon S3 2017. Tính lại bằng đường KHÁC `checks`: datetime (giờ 12 tiếng đổi bằng strptime) thay phép trừ phút; mô phỏng
# từng máy bị gỡ thay phép trừ; mô phỏng từng lượt gỡ chậm thay phép chia trần; Fraction cho phần trăm ô.
import datetime as dt
from fractions import Fraction as F

P = lambda s: dt.datetime.strptime("2017-02-28 " + s, "%Y-%m-%d %I:%M%p")
m = lambda a, b: int((P(b) - P(a)).total_seconds() // 60)
rec("L06a", m("9:37AM", "1:54PM") == 257 and divmod(257, 60) == (4, 17), "9:37 sáng → 1:54 chiều = 257 phút = 4 giờ 17 phút")
rec("L06b", (m("9:37AM", "12:26PM"), m("9:37AM", "1:18PM"), m("1:18PM", "1:54PM"), m("9:37AM", "11:37AM")) == (169, 221, 36, 120),
    "đọc lại sau 169; chỉ mục đầy đủ 221; ghi chờ thêm 36; trang tình trạng 120 phút")
rec("L06c", (divmod(169, 60), divmod(221, 60)) == ((2, 49), (3, 41)), "169 = 2 giờ 49; 221 = 3 giờ 41")
rec("L06d", P("1:54PM").strftime("%H:%M") == "13:54" and P("12:26PM").strftime("%H:%M") == "12:26", "đổi 12 giờ → 24 giờ")


def guard(total, minimum, k):          # công cụ mới: từ chối nếu gỡ k máy làm còn dưới mức tối thiểu
    left = total
    for _ in range(k):
        left -= 1
    return left >= minimum


rec("L06e", 100 - 40 == 60 < 70 and not guard(100, 70, 40) and guard(100, 70, 30) and not guard(100, 70, 31), "100 máy, tối thiểu 70: gỡ 40 bị chặn, tối đa 30")
rec("L06f", [k for k in range(101) if guard(100, 70, k)] == list(range(31)), "đúng 31 lệnh được chấp nhận (0…30)")


def slow(k, per=5, every=10):          # mô phỏng gỡ chậm: mỗi lượt tối đa `per` máy, mỗi lượt `every` phút
    t = 0
    while k > 0:
        k -= min(per, k)
        t += every
    return t


rec("L06g", (slow(4), slow(30)) == (10, 60), "gỡ chậm: 4 máy 10 phút; 30 máy 60 phút")
rec("L06h", not guard(200, 150, 60) and max(k for k in range(201) if guard(200, 150, k)) == 50, "quiz: 200 máy, tối thiểu 150 → tối đa 50")
rec("L06i", round(float(F(1, 12)) * 100, 1) == 8.3, "quiz: 1 ô trong 12 ≈ 8,3%")
