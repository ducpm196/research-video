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
def che(so):
    return so[:6] + "*" * 6 + so[-4:]
the = "5500005555555559"
print(luhn(the))
print(luhn(the[:-1] + "8"))
print(che(the))
