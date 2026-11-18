so_du = 25000000
lai_suat = 0.084
thang = 6
lai = so_du * lai_suat * thang / 12
lai_tron = round(lai)
print(f"So du goc: {so_du:,}")
print(f"Lai {thang} thang: {lai_tron:,}")
print(f"Tong nhan duoc: {so_du + lai_tron:,}")
print("Kieu cua lai:", type(lai).__name__)
