A = [1, 2, 3, 4, 5, 6]
QH = [
    ('R1', lambda a, b: (a - b) % 4 == 0),
    ('R2', lambda a, b: b % a == 0),
    ('R3', lambda a, b: abs(a - b) <= 1),
    ('R4', lambda a, b: (a + b) % 2 == 0),
]

for ten, R in QH:
    px = all(R(a, a) for a in A)
    dx = all(R(b, a) for a in A for b in A if R(a, b))
    pdx = all(a == b for a in A for b in A if R(a, b) and R(b, a))
    bc = all(R(a, c) for a in A for b in A for c in A if R(a, b) and R(b, c))
    dong = ten + ': PX=' + str(int(px)) + ' DX=' + str(int(dx)) + ' PDX=' + str(int(pdx)) + ' BC=' + str(int(bc))
    if px and dx and bc:
        lop = []
        for a in A:
            nhom = [b for b in A if R(a, b)]
            if nhom not in lop:
                lop.append(nhom)
        dong = dong + ', tuong duong, cac lop: ' + ' '.join(str(sorted(l)) for l in lop)
    print(dong)
