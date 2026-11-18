docs = {"a1": "rut tien atm", "a2": "chuyen tien the",
        "a3": "chuyen khoan napas", "a4": "nap tien the"}
chi_muc = {}
for ma, mo_ta in docs.items():
    for tu in mo_ta.split():
        chi_muc.setdefault(tu, set()).add(ma)
for tu in ["tien", "the", "chuyen"]:
    print(tu + ":", *sorted(chi_muc[tu]))
print("chuyen va the:", *sorted(chi_muc["chuyen"] & chi_muc["the"]))
print("manh cua 29, 41, 50 voi 5 manh chinh:", *[h % 5 for h in (29, 41, 50)])
giu = sum(h % 4 == h % 6 for h in range(12))
print("doi 4 -> 6 manh chinh: giu manh", giu, "/ 12")
