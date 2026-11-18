import math

ngay = 24 * 60 * 60
tb = 5_000_000 / ngay
cao = 6 * tb
chang = [12, 6, 25, 120, 3]
du = 400 - sum(chang)
dong_thoi = cao * 0.120
print("trung binh", round(tb, 1), "giao dich/giay")
print("cao diem", round(cao), "giao dich/giay")
print("con du", du, "ms")
print("cung luc o Oracle", round(dong_thoi, 1))
print("be 30 ket noi:", "khong du" if dong_thoi > 30 else "du", "- can it nhat", math.ceil(dong_thoi))
