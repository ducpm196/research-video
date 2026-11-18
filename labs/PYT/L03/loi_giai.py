giao_dich = [("A02", 500000), ("A01", 200000), ("A03", 950000), ("A02", 150000), ("A01", 700000), ("A02", 50000)]
ten = {"A01": "Hoa", "A02": "Nam", "A03": "Linh"}
dem = {}
tong = {}
for ma, tien in giao_dich:
    dem[ma] = dem.get(ma, 0) + 1
    tong[ma] = tong.get(ma, 0) + tien
for ma in sorted(dem):
    print(ma, dem[ma], tong[ma])
for ma in sorted(tong, key=lambda m: tong[m], reverse=True):
    print(ten[ma], tong[ma])
