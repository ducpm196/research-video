import re
nhat_ky = [
    "10:15:02 GD#A0731 chuyen 1.250.000 VND tu A01 den A02",
    "10:15:09 GD#A0732 rut 500.000 VND tu A03",
    "10:16:40 GD#A0733 nap 12.000.000 VND vao A01",
    "10:17:01 LOI GD#A0734 timeout",
    "10:17:30 GD#A0735 chuyen 75.000 VND tu A02 den A03",
]
tong = 0
for dong in nhat_ky:
    ma = re.search(r"GD#(\w+)", dong)
    so = re.search(r"([\d.]+) VND", dong)
    if so is None:
        continue
    tien = int(so.group(1).replace(".", ""))
    tong = tong + tien
    print(ma.group(1), tien)
print("Tong:", tong)
