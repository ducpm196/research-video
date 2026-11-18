dem = 0
print('p q r kq')
for p in (1, 0):
    for q in (1, 0):
        for r in (1, 0):
            kq = int((p == 1 and q == 0) or r == 1)
            print(p, q, r, kq)
            dem = dem + kq
print('so dong dung:', dem)
