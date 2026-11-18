MONG_MUON = {"a": 2, "b": 1}
THAT = {"a": 5, "c": 1}


def lech():
    return sorted({t for t in MONG_MUON if THAT.get(t) != MONG_MUON[t]} | (set(THAT) - set(MONG_MUON)))


def dong_bo(prune):
    viec = []
    for ten, ban in MONG_MUON.items():
        if THAT.get(ten) != ban:
            viec.append(("sua " if ten in THAT else "tao ") + ten)
            THAT[ten] = ban
    if prune:
        for ten in sorted(set(THAT) - set(MONG_MUON)):
            viec.append("xoa " + ten)
            del THAT[ten]
    return viec


def hien(ds):
    return ", ".join(ds) or "-"


print("lech:", hien(lech()))
print("dong bo (khong prune):", hien(dong_bo(False)), "| lech:", hien(lech()))
print("dong bo (prune):", hien(dong_bo(True)), "| lech:", hien(lech()))
