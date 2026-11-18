def hop_le(s):
    ngan_xep = []
    cap = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{":
            ngan_xep.append(c)
        elif c in cap:
            if not ngan_xep or ngan_xep.pop() != cap[c]:
                return False
    return not ngan_xep


for s in ("{[()]}", "([)]", "((", "())"):
    print(f"{s}: " + ("hop le" if hop_le(s) else "sai"))


class HangDoiVong:
    def __init__(self, max_o):
        self.o = [None] * max_o
        self.dau = 0
        self.cuoi = max_o - 1
        self.dem = 0

    def xep_vao(self, x):
        self.cuoi = (self.cuoi + 1) % len(self.o)
        self.o[self.cuoi] = x
        self.dem += 1

    def lay_ra(self):
        x = self.o[self.dau]
        self.dau = (self.dau + 1) % len(self.o)
        self.dem -= 1
        return x

    def noi_dung(self):
        return [self.o[(self.dau + k) % len(self.o)] for k in range(self.dem)]


h = HangDoiVong(4)
for x in (10, 20, 30, 40):
    h.xep_vao(x)
print("lay ra:", h.lay_ra())
h.xep_vao(50)
print("dau hang:", " ".join(str(x) for x in h.noi_dung()))
print("chi so cuoi:", h.cuoi)
print("so phan tu:", h.dem)


def hau_to(bieu_thuc):
    ngan_xep = []
    for k in bieu_thuc.split():
        if k in "+-*":
            b, a = ngan_xep.pop(), ngan_xep.pop()
            ngan_xep.append(a + b if k == "+" else a - b if k == "-" else a * b)
        else:
            ngan_xep.append(int(k))
    return ngan_xep[0]


print("hau to:", hau_to("6 2 3 + * 4 -"))
