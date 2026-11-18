DU_AN = [("A", "1.0"), ("B", "1.0")]
CAY = {("A", "1.0"): [("X", "1.0"), ("Y", "2.0")],
       ("B", "1.0"): [("Y", "3.0"), ("Z", "1.0")],
       ("Z", "1.0"): [("X", "2.0")]}


def so(v):
    return tuple(int(p) for p in v.split("."))


def maven():
    chon, hang = {}, [(t, v) for t, v in DU_AN]
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon:
            continue
        chon[ten] = ban
        hang += CAY.get((ten, ban), [])
    return chon


def gradle():
    chon, hang = {}, [(t, v) for t, v in DU_AN]
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon and so(chon[ten]) >= so(ban):
            continue
        chon[ten] = ban
        hang += CAY.get((ten, ban), [])
    return chon


for ten, ban in sorted(maven().items()):
    print("maven", ten, ban)
for ten, ban in sorted(gradle().items()):
    if ten not in ("A", "B"):
        print("gradle", ten, ban)
