def euclid(a, b):
    buoc = 0
    while b != 0:
        a, b = b, a % b
        buoc += 1
    return a, buoc


def chen(a):
    a = list(a)
    dem = 0
    for i in range(1, len(a)):
        j = i
        while j > 0:
            dem += 1
            if a[j - 1] <= a[j]:
                break
            a[j - 1], a[j] = a[j], a[j - 1]
            j -= 1
    return a, dem


def co_trung(a):
    b, _ = chen(a)
    so_sanh = 0
    for i in range(len(b) - 1):
        so_sanh += 1
        if b[i] == b[i + 1]:
            return True, so_sanh
    return False, so_sanh


u, buoc = euclid(1071, 462)
print(f"gcd(1071, 462) = {u} sau {buoc} buoc chia")
for ten, mang in (("giam dan, n = 8", list(range(8, 0, -1))), ("da sap, n = 8", list(range(8))), ("lan xon", [7, 3, 9, 1, 5])):
    kq, dem = chen(mang)
    print(f"chen {ten}: {dem} lan so sanh, ket qua {kq}")
for mang in ([9, 4, 7, 1, 4, 8], [9, 4, 7, 1, 5, 8]):
    print("co trung" if co_trung(mang)[0] else "khong trung", mang)
