A = {2, 3, 5, 7, 11, 13}
B = {1, 3, 5, 7, 9, 11}

def in_ra(ten, s):
    print(ten + ':', ' '.join(str(x) for x in sorted(s)))

in_ra('hop', A | B)
in_ra('giao', A & B)
in_ra('A bo B', A - B)
in_ra('B bo A', B - A)
print('so tap con cua A:', 2 ** len(A))
dem = 0
for x in range(1, 1001):
    if x % 4 == 0 or x % 6 == 0:
        dem = dem + 1
n = 1000
print('chia het cho 4 hoac 6, tu 1 den 1000: dem=' + str(dem), 'congthuc=' + str(n // 4 + n // 6 - n // 12))
