def luhn(so):
    tong = 0
    for i, c in enumerate(reversed(so)):
        d = int(c)
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d = d - 9
        tong = tong + d
    return tong % 10 == 0
the = "5500005555555559"
print(luhn(the))
print(luhn(the[:-1] + "8"))
print(the[:6] + "*" * 6 + the[-4:])
