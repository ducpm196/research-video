TTL, SOM, LECH, GIO = 120, 20, 30, 3600


def xin_ma(so_ma):
    dem = 0
    for _ in range(so_ma):
        t = 0
        while t < GIO:
            dem += 1
            t += TTL - SOM
    return dem


print(f"Mot ma chung: {xin_ma(1)} lan xin ma")
print(f"Moi API mot ma: {xin_ma(4)} lan xin ma")
print("Giay cuoi cung ma con duoc nhan:",
      max(g for g in range(1000) if g < TTL + LECH))
