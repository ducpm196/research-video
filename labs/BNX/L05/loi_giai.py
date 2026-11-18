from datetime import date, timedelta

HOM_NAY = date(2026, 6, 15)
CHUNG_CHI = [("so_cai", "2026-04-20", 60),
             ("bao_cao", "2026-01-10", 365),
             ("doi_soat", "2026-05-01", 30)]

can_xu_ly = 0
for ten, cap, han in CHUNG_CHI:
    ngay_cap = date.fromisoformat(cap)
    xoay = ngay_cap + timedelta(days=han * 2 // 3)
    het = ngay_cap + timedelta(days=han)
    if HOM_NAY > het:
        tt = "da het han"
    elif HOM_NAY >= xoay:
        tt = f"can xoay, con {(het - HOM_NAY).days} ngay"
    else:
        tt = "chua den han xoay"
    if tt != "chua den han xoay":
        can_xu_ly += 1
    print(f"{ten}: xoay {xoay}, het han {het}: {tt}")
print("So chung chi can xu ly:", can_xu_ly)
