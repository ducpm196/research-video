giao_dich = [250000, 3200000, 75000000, 1800000, 64000000, 900000, 5000000, 120000]
tong = 0
dem_nho = 0
dem_vua = 0
dem_lon = 0
for tien in giao_dich:
    tong = tong + tien
    if tien < 2000000:
        muc = "nho"
        dem_nho = dem_nho + 1
    elif tien < 60000000:
        muc = "vua"
        dem_vua = dem_vua + 1
    else:
        muc = "lon"
        dem_lon = dem_lon + 1
    print(tien, muc)
print("Tong:", tong)
print("Nho, vua, lon:", dem_nho, dem_vua, dem_lon)
