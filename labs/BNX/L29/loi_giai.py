def ap_dung(so_du, sk):
    loai, tien = sk
    return so_du + tien if loai == "NAP" else so_du - tien


def phat_lai(kho, tu=0, so_du=0):
    for sk in kho[tu:]:
        so_du = ap_dung(so_du, sk)
    return so_du


kho = [("NAP", 500), ("RUT", 100), ("NAP", 200), ("RUT", 50), ("NAP", 25), ("RUT", 75)]
print("phat lai het:", phat_lai(kho), "(doc", len(kho), "su kien)")
ban_chup = (4, phat_lai(kho[:4]))
print("ban chup tai su kien", ban_chup[0], ":", ban_chup[1])
print("phat lai tu ban chup:", phat_lai(kho, ban_chup[0], ban_chup[1]), "(doc", len(kho) - ban_chup[0], "su kien)")
kho += [("RUT", 300), ("NAP", 300)]
print("sau khi bu su kien rut nham:", phat_lai(kho))
