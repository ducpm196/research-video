def phi_rut(tien):
    if tien < 2000000:
        return 1100
    return tien * 5 // 10000

def vat(phi, ty_le=10):
    return phi * ty_le // 100

def tong_chi(tien, ham_phi):
    phi = ham_phi(tien)
    return phi + vat(phi)

for tien in [500000, 3000000, 80000000]:
    print(tien, phi_rut(tien), tong_chi(tien, phi_rut))
print(tong_chi(3000000, lambda t: t // 1000))

import time


def do(ham):
    tot = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        ham()
        tot = min(tot, time.perf_counter() - t0)
    return tot


def goi():
    for _ in range(1000000):
        vat(1100)


def thang():
    phi = 1100
    for _ in range(1000000):
        phi * 10 // 100


print("Goi ham cham hon viet thang:", "CO" if do(goi) > do(thang) else "KHONG")
