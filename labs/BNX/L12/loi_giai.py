bao_dam = 250_000
vi = {"X": 0, "Y": 250_000, "Z": 0}
nhat_ky = [("nap", "X", 3_000_000), ("chuyen", "X", "Z", 1_200_000),
           ("rut", "Z", 400_000), ("nap", "Y", 500_000),
           ("rut", "Y", 2_000_000), ("chuyen", "Z", "Y", 300_000)]
for g in nhat_ky:
    if g[0] == "chuyen":
        vi[g[1]] -= g[3]
        vi[g[2]] += g[3]
    elif g[0] == "rut" and vi[g[1]] < g[2]:
        print("tu choi rut", g[1], g[2])
    else:
        dau = 1 if g[0] == "nap" else -1
        vi[g[1]] += dau * g[2]
        bao_dam += dau * g[2]
tong = sum(vi.values())
print("vi", *vi.values())
print("tong vi", tong, "dam bao", bao_dam, "dat", bao_dam >= tong)
HAN_MUC = 50_000_000
da_dung = 0
for so_tien in [20_000_000, 25_000_000, 10_000_000, 5_000_000]:
    if da_dung + so_tien > HAN_MUC:
        print("tu choi", so_tien, "da dung", da_dung)
    else:
        da_dung += so_tien
        print("chap nhan", so_tien, "da dung", da_dung)
