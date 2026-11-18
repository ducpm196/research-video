p, q, e = 7, 13, 5
n = p * q
L = (p - 1) * (q - 1)
print('n = ' + str(n) + ', L = ' + str(L))
d = 1
while (e * d) % L != 1:
    d = d + 1
print('khoa bi mat d =', d)
ban_ma = pow(10, e, n)
print('ma hoa 10:', ban_ma)
print('giai ma ' + str(ban_ma) + ':', pow(ban_ma, d, n))
dung = 0
for x in range(n):
    if pow(pow(x, e, n), d, n) == x:
        dung = dung + 1
print('ma hoa roi giai ma moi ban tin 0..90:', dung, '/ 91 dung')
u = 2
while n % u != 0:
    u = u + 1
print('phan tich n: ' + str(n) + ' = ' + str(u) + ' x ' + str(n // u))
