import math


def minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


for n in (1000, 4097, 5000):
    m = minrun(n)
    k = math.ceil(n / m)
    print(f"n = {n}: minrun {m}, {k} doan, luy thua cua 2: {'CO' if k & (k - 1) == 0 else 'KHONG'}")


def gop(s, ban_sua):
    while len(s) > 1:
        n = len(s) - 2
        if (n > 0 and s[n - 1] <= s[n] + s[n + 1]) or (ban_sua and n > 1 and s[n - 2] <= s[n - 1] + s[n]):
            if s[n - 1] < s[n + 1]:
                n -= 1
            s[n:n + 2] = [s[n] + s[n + 1]]
        elif s[n] <= s[n + 1]:
            s[n:n + 2] = [s[n] + s[n + 1]]
        else:
            break


def bat_bien(s):
    return all(s[i] > s[i + 1] + s[i + 2] for i in range(len(s) - 2)) and all(s[i] > s[i + 1] for i in range(len(s) - 1))


def chay(day, ban_sua):
    s = []
    for r in day:
        s.append(r)
        gop(s, ban_sua)
    return s


DAY = [62, 109, 119, 37, 22, 55]
for ten, sua in (("Ban cu", False), ("Ban sua", True)):
    s = chay(DAY, sua)
    print(f"{ten}: ngan xep cuoi {s}, bat bien {'DUNG' if bat_bien(s) else 'HONG'}")
