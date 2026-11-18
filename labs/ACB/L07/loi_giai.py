import hashlib
import hmac

KHOA = b"khoa-lab-07"


def ky(noi_dung):
    return hmac.new(KHOA, noi_dung.encode(), hashlib.sha256).hexdigest()[:12]


goi = '{"va": "770000009999", "tien": 2500000}'
kem_theo = ky(goi)
print("hmac nguyen ven:", kem_theo == ky(goi))
print("hmac bi sua:", kem_theo == ky(goi.replace("2500000", "9500000")))

da_xu_ly = set()
for ma in ["e1", "e2", "e1", "e3", "e2"]:
    if ma in da_xu_ly:
        print(ma + ": bo qua")
    else:
        da_xu_ly.add(ma)
        print(ma + ": gach no")

core, napas, erp = [10, 11, 13, 15], [10, 11, 12, 13, 15, 16], [10, 13, 16]
for ma in sorted(set(core) | set(napas) | set(erp)):
    c, n, e = ma in core, ma in napas, ma in erp
    if c and n and e:
        kq = "MATCHED"
    elif c and n:
        kq = "rot webhook, goi gach no bo sung"
    elif n and not c and not e:
        kq = "treo ghi co, hach toan bu"
    elif c and not n:
        kq = "loi chuyen tien NAPAS, tra soat"
    else:
        kq = "bat thuong"
    print(str(ma) + ": " + kq)
