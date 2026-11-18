def rut_co_dieu_kien(tk, so):
    if tk["so_du"] >= so:
        tk["so_du"] -= so
        return 1
    return 0


tk = {"so_du": 700}
kq = [rut_co_dieu_kien(tk, r) for r in (500, 500, 200)]
print("co dieu kien:", *kq, "con", tk["so_du"])

so_du = 700
doc_a = doc_b = so_du                 # hai bên cùng đọc trước khi ai ghi
so_du = doc_a - 500                   # A ghi
so_du = doc_b - 500                   # B ghi đè
mat = 500 + 500 - (700 - so_du)
print(f"doc roi ghi: A doc {doc_a}, B doc {doc_b}, ghi 200 va 200, con {so_du} (mat {mat})")
