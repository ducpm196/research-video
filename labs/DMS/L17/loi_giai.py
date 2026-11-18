DO_THI = [
    ('H1', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]),
    ('H2', [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6)]),
    ('H3', [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]),
    ('H4', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]),
]

def phan_tich(canh):
    nhom = {v: v for v in range(1, 7)}
    chu_trinh = False
    for u, v in canh:
        a, b = nhom[u], nhom[v]
        if a == b:
            chu_trinh = True
        else:
            for x in nhom:
                if nhom[x] == b:
                    nhom[x] = a
    lien_thong = len(set(nhom.values())) == 1
    return lien_thong, chu_trinh

for ten, canh in DO_THI:
    lt, ct = phan_tich(canh)
    print(ten + ': n=6 m=' + str(len(canh)), 'lien_thong=' + str(int(lt)), 'chu_trinh=' + str(int(ct)), 'la_cay=' + str(int(lt and not ct)))

def so_la(canh):
    return sum(1 for v in range(1, 7) if sum(1 for e in canh if v in e) == 1)

print('H1: so la =', so_la(DO_THI[0][1]))
print('H3: so la =', so_la(DO_THI[2][1]))
print('cay co nhan 8 dinh (cong thuc Cayley):', 8 ** 6)
