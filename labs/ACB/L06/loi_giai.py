import hashlib
import hmac

tong = 0
for tien in [6, 7, 9, 15, 3]:
    quet = tien > 10 or tong + tien > 20
    tong = 0 if quet else tong + tien
    print(tien, "quet mat" if quet else "thuong", "tong:", tong)

KHOA = b"khoa-cua-toi"


def ky(nd):
    return hmac.new(KHOA, nd.encode(), hashlib.sha256).hexdigest()[:8]


ve = {"id": "x7", "tien": 30, "het_han": 240}
ve["ky"] = ky("x7|30|240")
da_dung = set()


def kiem(ve, tien, bay_gio):
    nd = ve["id"] + "|" + str(tien) + "|" + str(ve["het_han"])
    if ve["ky"] != ky(nd):
        return "tu choi: ky sai hoac tien bi sua"
    if bay_gio > ve["het_han"]:
        return "tu choi: het han"
    if ve["id"] in da_dung:
        return "tu choi: da dung"
    da_dung.add(ve["id"])
    return "cho phep"


for tien, giay in [(30, 100), (30, 150), (35, 100), (30, 250)]:
    print(kiem(ve, tien, giay))
