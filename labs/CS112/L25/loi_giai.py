import itertools

CANH = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 9), ("C", "D", 5), ("C", "E", 8), ("D", "E", 3), ("D", "F", 6), ("E", "F", 10), ("A", "F", 11)]
DINH = "ABCDEF"


class HopTim:
    def __init__(self):
        self.cha = {v: v for v in DINH}
        self.co = {v: 1 for v in DINH}

    def tim(self, x):
        if self.cha[x] != x:
            self.cha[x] = self.tim(self.cha[x])
        return self.cha[x]

    def hop(self, a, b):
        ra, rb = self.tim(a), self.tim(b)
        if ra == rb:
            return False
        if self.co[ra] < self.co[rb]:
            ra, rb = rb, ra
        self.cha[rb] = ra
        self.co[ra] += self.co[rb]
        return True


def ten(e):
    return f"{e[0]}-{e[1]}({e[2]})"


ht = HopTim()
kr = [e for e in sorted(CANH, key=lambda e: e[2]) if ht.hop(e[0], e[1])]
print("Kruskal:", " ".join(map(ten, kr)) + f", tong {sum(e[2] for e in kr)}")

trong = {"A"}
pr = []
while len(trong) < len(DINH):
    e = min((e for e in CANH if (e[0] in trong) != (e[1] in trong)), key=lambda e: e[2])
    pr.append(e)
    trong |= {e[0], e[1]}
print("Prim tu A:", " ".join(map(ten, pr)) + f", tong {sum(e[2] for e in pr)}")

so_cay, nho = 0, None
for bo in itertools.combinations(CANH, len(DINH) - 1):
    h = HopTim()
    if all(h.hop(e[0], e[1]) for e in bo):
        so_cay += 1
        t = sum(e[2] for e in bo)
        nho = t if nho is None or t < nho else nho
print(f"Vet can: {so_cay} cay khung, nho nhat {nho}")
print("Cung tong:", "CO" if sum(e[2] for e in kr) == sum(e[2] for e in pr) == nho else "KHONG")
