from math import comb

print('2^80 =', 2 ** 80)
print('2^64 lan thu o 1e9 lan moi giay:', round(2 ** 64 / 10 ** 9 / 31536000), 'nam')
print('nhanh hon vet can (2^80 / 2^61):', 2 ** 80 // 2 ** 61, 'lan')
print('1000000 tep, ma 32 bit: ky vong cap trung gia', round(comb(1000000, 2) / 2 ** 32, 1))
print('1000000 tep, ma 64 bit: ky vong cap trung gia', '%.1e' % (comb(1000000, 2) / 2 ** 64))
n = 1
while n / 2 < 100:
    n = n + 1
print('ma bang bit can de vet can ngay sinh >= 2^100:', n)
