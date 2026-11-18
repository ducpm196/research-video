import base64, hmac, hashlib, json

KHOA = b"khoa-lab-l03"


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def ky(dau, than):
    vao = b64u(dau) + "." + b64u(than)
    mac = hmac.new(KHOA, vao.encode(), hashlib.sha256).digest()
    return vao + "." + b64u(mac)


def kiem(ma, aud, bay_gio):
    d, t, s = ma.split(".")
    mac = hmac.new(KHOA, (d + "." + t).encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(b64u(mac), s):
        return "chu ky sai"
    c = json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))
    if bay_gio >= c["exp"]:
        return "het han"
    if c["aud"] != aud:
        return "sai nguoi nhan"
    return "nhan"


dau = b'{"alg":"HS256","typ":"JWT"}'
than = b'{"sub":"u42","aud":"app-b","exp":2000}'
ma = ky(dau, than)
print(ma.split(".")[2])
print(kiem(ma, "app-b", 1999))
print(kiem(ma, "app-b", 2000))
d, t, s = ma.split(".")
sua = b64u(than.replace(b"u42", b"u43"))
print(kiem(d + "." + sua + "." + s, "app-b", 1000))
print(kiem(ma, "app-c", 1000))
