import heapq


def kenh(co_app, tien):
    if co_app:
        return "OTT_PUSH"
    if tien >= 50000:
        return "SMS_BRANDNAME"
    return "EMAIL"


ds = [(True, 15000), (None, 120000), (False, 49999), (False, 50000)]
print("kenh:", " ".join(kenh(a, t) for a, t in ds))

hang = []
for it in [(3, "khuyen mai"), (1, "otp 9911"), (2, "bien dong so du"), (1, "otp 7788")]:
    heapq.heappush(hang, it)
ra = []
while hang:
    ra.append(heapq.heappop(hang)[1])
print("uu tien:", " | ".join(ra))

the, cuoi, kq = 3, 0, []
for t in [0, 0, 0, 0, 1, 1, 2]:
    the = min(3, the + (t - cuoi))
    cuoi = t
    if the >= 1:
        the = the - 1
        kq.append("gui")
    else:
        kq.append("tu_choi")
print("xo the:", " ".join(kq))

tong = 90000
mien = tong * 65 // 100
print("mien cuoc:", mien, "tin/phut, tinh cuoc toi da:", tong - mien)
