import math

dem_ss = 0
sau_max = 0


def phan_hoach(a, lo, hi):
    global dem_ss
    p, i = a[hi], lo - 1
    for j in range(lo, hi):
        dem_ss += 1
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def sap_nhanh(a, lo, hi, sau=1):
    global sau_max
    if lo < hi:
        sau_max = max(sau_max, sau)
        q = phan_hoach(a, lo, hi)
        sap_nhanh(a, lo, q - 1, sau + 1)
        sap_nhanh(a, q + 1, hi, sau + 1)


a = [7, 3, 9, 1, 8, 2, 6, 4]
x = a[:]
q = phan_hoach(x, 0, len(x) - 1)
print(f"Phan hoach: {x}, chot o vi tri {q}, {dem_ss} so sanh")

dem_ss, sau_max = 0, 0
y = a[:]
sap_nhanh(y, 0, len(y) - 1)
print(f"Sap nhanh: tong {dem_ss} so sanh, do sau {sau_max}")

dem_ss, sau_max = 0, 0
z = [1, 2, 3, 4, 5, 6, 7, 8]
sap_nhanh(z, 0, len(z) - 1)
print(f"Da sap: tong {dem_ss} so sanh, do sau {sau_max}")

print("Can duoi n = 8:", math.ceil(math.log2(math.factorial(8))))

b = [2, 0, 3, 2, 1, 0, 2, 3, 1]
dem = [0] * 4
for v in b:
    dem[v] += 1
ra = []
for gia_tri, so_lan in enumerate(dem):
    ra += [gia_tri] * so_lan
print("Sap xep dem:", ra)
