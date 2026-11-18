M = 11


def chen_bang(bang, k):
    o = k % M
    while bang[o] is not None:
        o = (o + 1) % M
    bang[o] = k


def tim_bang(bang, k):
    o, thu = k % M, 1
    while bang[o] is not None:
        if bang[o] == k:
            return thu
        o, thu = (o + 1) % M, thu + 1
    return -thu


bang = [None] * M
for k in (18, 41, 22, 44, 59, 32):
    chen_bang(bang, k)
print("bang:", " ".join("." if x is None else str(x) for x in bang))
print("tim 44: thu", tim_bang(bang, 44), "o")
print("tim 99: khong thay sau", -tim_bang(bang, 99), "o")


def vun_xuong(a, i, n):
    doi = 0
    while 2 * i + 1 < n:
        c = 2 * i + 1
        if c + 1 < n and a[c + 1] > a[c]:
            c += 1
        if a[i] >= a[c]:
            break
        a[i], a[c] = a[c], a[i]
        i, doi = c, doi + 1
    return doi


a = [4, 10, 3, 5, 1, 8, 7]
tong_doi = sum(vun_xuong(a, i, len(a)) for i in range(len(a) // 2 - 1, -1, -1))
print("dong:", " ".join(map(str, a)))
print("so lan doi cho:", tong_doi)
ra = []
for _ in range(3):
    ra.append(a[0])
    a[0] = a[-1]
    a.pop()
    vun_xuong(a, 0, len(a))
print("lay ra 3 lan:", " ".join(map(str, ra)))
print("con lai:", " ".join(map(str, a)))
