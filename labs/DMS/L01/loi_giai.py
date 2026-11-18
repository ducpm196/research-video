from itertools import product

def keo(a, b):
    return (not a) or b

CAP = [
    (1, 2, lambda p, q: not (p and (not q)), lambda p, q: (not p) or q),
    (2, 2, lambda p, q: keo(p, q), lambda p, q: keo(q, p)),
    (3, 2, lambda p, q: keo(p, q), lambda p, q: keo(not q, not p)),
    (4, 3, lambda p, q, r: keo(p, keo(q, r)), lambda p, q, r: keo(p and q, r)),
    (5, 3, lambda p, q, r: keo(p, q) and keo(q, r), lambda p, q, r: keo(p, r)),
]

for k, n, f, g in CAP:
    lech = None
    for dong in product((True, False), repeat=n):
        if f(*dong) != g(*dong):
            lech = dong
            break
    if lech is None:
        print(str(k) + ': tuong duong')
    else:
        print(str(k) + ': khong tuong duong, dong lech dau tien:', ' '.join(str(int(x)) for x in lech))
