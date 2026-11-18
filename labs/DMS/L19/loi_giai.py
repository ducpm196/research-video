from itertools import permutations, product
from math import comb

khong_trung = 1.0
for i in range(30):
    khong_trung = khong_trung * (365 - i) / 365
print('P(trung ngay sinh) voi 30 nguoi:', round(1 - khong_trung, 4))

khong_trung, n = 1.0, 0
while khong_trung > 0.5:
    khong_trung = khong_trung * (1000 - n) / 1000
    n = n + 1
print('so nguoi nho nhat de P >= 0.5 voi 1000 ngay:', n)

print('ky vong so cap va cham 200 khoa vao 10000 o:', comb(200, 2) / 10000)

tong = 0
for p in permutations(range(7)):
    tong = tong + sum(1 for i in range(7) if p[i] == i)
print('so diem co dinh trung binh cua 7 vat:', tong / 5040)

khac = sum(1 for b in product(range(10), repeat=5) if len(set(b)) == 5)
print('P(khong trung) 5 nguoi, 10 ngay (liet ke het):', khac / 100000)
