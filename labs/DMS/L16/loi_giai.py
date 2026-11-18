DO_THI = [
    ('G1', [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
    ('G2', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]),
    ('G3', [1, 2, 3, 4, 5, 6], [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]),
    ('G4', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5)]),
]

def lien_thong(dinh, canh):
    thay = {dinh[0]}
    moi = True
    while moi:
        moi = False
        for u, v in canh:
            if (u in thay) != (v in thay):
                thay.add(u)
                thay.add(v)
                moi = True
    return len(thay) == len(dinh)

for ten, dinh, canh in DO_THI:
    bac = [sum(1 for e in canh if v in e) for v in dinh]
    le = sum(1 for b in bac if b % 2 == 1)
    lt = lien_thong(dinh, canh)
    if lt and le == 0:
        kl = 'chu_trinh'
    elif lt and le == 2:
        kl = 'duong_di'
    else:
        kl = 'khong'
    print(ten + ': bac=' + ','.join(str(b) for b in bac), 'tong=' + str(sum(bac)), 'canh=' + str(len(canh)), 'le=' + str(le),
          'lien_thong=' + str(int(lt)), 'ket_luan=' + kl)
