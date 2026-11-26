def co_vong(lenh):
    khoa = {}
    cho = {}
    lich = (("A", lenh["A"][0]), ("B", lenh["B"][0]), ("A", lenh["A"][1]), ("B", lenh["B"][1]))
    for ai, tk in lich:
        if ai in cho:
            continue
        giu = khoa.get(tk, ai)
        if giu != ai:
            cho[ai] = giu
        else:
            khoa[tk] = ai
    return cho.get("A") == "B" and cho.get("B") == "A"


goc = {"A": [7, 3], "B": [3, 7]}
sap = {ai: sorted(ds) for ai, ds in goc.items()}
print("A khoa:", sap["A"])
print("B khoa:", sap["B"])
print("vong cho khi khong sap:", "co" if co_vong(goc) else "khong")
print("vong cho khi sap:", "co" if co_vong(sap) else "khong")

so_du = 20
dau = []
for phat_sinh in [4, -6, 3, -2, 5]:
    dau.append(so_du)
    so_du = so_du + phat_sinh
print("dau doan:", dau, "cuoi:", so_du)
print("so khoi:", -(-2500 // 500))
