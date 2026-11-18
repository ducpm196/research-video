import hashlib


def kiem(noi_dung):
    dong = noi_dung.rstrip("\n").split("\n")
    _, so, ma = dong[-1].split("|")
    du_lieu = "\n".join(dong[:-1]) + "\n"
    if len(dong) - 1 != int(so):
        return "THIEU DONG"
    if hashlib.sha256(du_lieu.encode()).hexdigest() != ma:
        return "SAI MA BAM"
    return "OK"


def lo(dong):
    nd = "\n".join(dong) + "\n"
    return nd + f"TRAILER|{len(dong)}|{hashlib.sha256(nd.encode()).hexdigest()}\n"


dong = ["A01|100", "A02|200", "A03|300", "A04|400", "A05|500"]
tot = lo(dong)
thieu = tot.replace("A05|500\n", "")
sai = tot.replace("A03|300", "A03|301")
rong = tot.split("TRAILER")[0] + "TRAILER|5|" + "0" * 64 + "\n"
print("lo tot:", kiem(tot))
print("lo thieu mot dong:", kiem(thieu))
print("lo sai mot chu so:", kiem(sai))
print("lo co trailer gia:", kiem(rong))
