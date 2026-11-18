def chu_so(s):
    return "".join(str(int(c, 36)) for c in s)
def du97(iban):
    return int(chu_so(iban[4:] + iban[:4])) % 97
bic = "ABCDDEFFXXX"
print(f"BIC {bic}: to chuc {bic[:4]}, quoc gia {bic[4:6]}, dia diem {bic[6:8]}, chi nhanh {bic[8:] or '-'}")
iban = "GB90BANK98765432101234"
sai = iban[:-2] + iban[-1] + iban[-2]
for x in (iban, sai):
    r = du97(x)
    print(x + ": du", r, "->", "hop le" if r == 1 else "khong hop le")
tien, phi_gui, phi_tg = 2000, 8, 12
print("nguoi nhan: OUR", tien, "SHA", tien - phi_tg, "BEN", tien - phi_gui - phi_tg)
print("nguoi gui tra: OUR", tien + phi_gui + phi_tg)
