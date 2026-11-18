def euclid(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mo_rong(A, B):
    # trả (g, x, y) với A*x + B*y = g
    a, b = A, B
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

print('gcd(462, 1071) =', euclid(462, 1071))
g, x, y = mo_rong(462, 1071)
print('he so Bezout (x, y) thoa 462x + 1071y = 21:', 'dung' if 462 * x + 1071 * y == 21 else 'sai')
print('-17 mod 5 =', (-17) % 5)
print('(123456789 * 987654321) mod 1000:', (123456789 * 987654321) % 1000, ((123456789 % 1000) * (987654321 % 1000)) % 1000)
TEN = ['Hai', 'Ba', 'Tu', 'Nam', 'Sau', 'Bay', 'CN']
print('1000 ngay nua tu thu Ba la thu', TEN[(1 + 1000) % 7])
a, b, buoc = 832040, 514229, 0
while b != 0:
    a, b = b, a % b
    buoc = buoc + 1
print('so buoc Euclid cua (832040, 514229):', buoc)
for x in range(30):
    if (7 * x) % 30 == 3:
        print('7x = 3 (mod 30): x =', x)
