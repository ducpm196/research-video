import itertools

ds = [(6, 8), (4, 9), (1, 3), (10, 12), (3, 6), (0, 5), (6, 13), (6, 11), (1, 7)]


def chon(ds, khoa):
    last, ra = -1, []
    for i in sorted(range(len(ds)), key=khoa):
        if ds[i][0] >= last:
            ra.append(i + 1)
            last = ds[i][1]
    return ra


def khong_chong(S):
    return all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(S, 2))


def vet_can(ds):
    for k in range(len(ds), 0, -1):
        if any(khong_chong(S) for S in itertools.combinations(ds, k)):
            return k


ket_thuc = chon(ds, lambda i: ds[i][1])
bat_dau = chon(ds, lambda i: ds[i][0])
ngan = chon(ds, lambda i: ds[i][1] - ds[i][0])
vc = vet_can(ds)
print("Chon theo ket thuc som nhat:", " ".join(map(str, ket_thuc)))
print("So su kien:", len(ket_thuc))
print(f"Bat dau som nhat: {len(bat_dau)}, ngan nhat: {len(ngan)}, vet can: {vc}")
print("Tham lam = vet can:", "CO" if len(ket_thuc) == vc else "KHONG")
