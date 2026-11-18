tps = 4000
phut = tps * 60
gio = phut * 60
tong = 90 + 40
ttl = 2 * 45
so_du = 3000000
so_du = so_du - 1200000   # core da tru
so_du = so_du + 1200000   # boi hoan khi doi tac bao chua nhan tien
print("moi phut:", phut)
print("moi gio:", gio)
if tong < 200:
    print("toan trinh:", tong, "ms, duoi 200")
else:
    print("toan trinh:", tong, "ms, vuot 200")
print("ttl:", ttl, "giay =", ttl * 1000, "ms")
print("so du sau boi hoan:", so_du)
