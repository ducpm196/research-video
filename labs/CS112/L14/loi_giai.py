def liet_ke(n, cat_tia):
    # đếm các hoán vị x của 1..n với x[i] != i + 1 (không phần tử nào đứng yên); trả (số nghiệm, số nút của cây)
    x, da_dung = [], [False] * (n + 1)
    ket_qua = [0, 0]

    def thu(i):
        ket_qua[1] += 1
        if i == n:
            if all(x[k] != k + 1 for k in range(n)):
                ket_qua[0] += 1
            return
        for j in range(1, n + 1):
            if da_dung[j]:
                continue
            if cat_tia and j == i + 1:
                continue
            da_dung[j] = True
            x.append(j)
            thu(i + 1)
            x.pop()
            da_dung[j] = False

    thu(0)
    return ket_qua[0], ket_qua[1]


for n in (4, 5, 6):
    nghiem, nut_cat = liet_ke(n, True)
    nghiem2, nut_khong = liet_ke(n, False)
    print(f"n = {n}: {nghiem} nghiem, {nut_cat} nut khi cat tia, {nut_khong} nut khi khong cat, cung so nghiem: {'dung' if nghiem == nghiem2 else 'sai'}")
