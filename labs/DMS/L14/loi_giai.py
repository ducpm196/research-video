def nghich_dao(a, n):
    for b in range(1, n):
        if (a * b) % n == 1:
            return b
    return None

def luy_thua_nhanh(a, e, n):
    kq, phep = 1, 0
    while e > 0:
        if e % 2 == 1:
            kq = (kq * a) % n
            phep = phep + 1
        a = (a * a) % n
        e = e // 2
        phep = phep + 1
    return kq, phep

print('nghich dao cua 7 theo mo-dun 40:', nghich_dao(7, 40))
b = nghich_dao(12, 18)
print('nghich dao cua 12 theo mo-dun 18:', 'khong co' if b is None else b)
a1, _ = luy_thua_nhanh(6, 100, 19)
a2, _ = luy_thua_nhanh(6, 100 % 18, 19)
print('6^100 mod 19:', a1, a2)
print('so phep nhan cua luy thua nhanh voi mu 1000:', luy_thua_nhanh(2, 1000, 10 ** 9 + 7)[1])
d = 2
while 561 % d != 0:
    d = d + 1
print('2^560 mod 561: ' + str(luy_thua_nhanh(2, 560, 561)[0]) + ', uoc nho nhat cua 561: ' + str(d))
