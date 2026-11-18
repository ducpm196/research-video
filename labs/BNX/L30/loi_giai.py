class CauDao:
    def __init__(self, nguong, cho):
        self.nguong, self.cho = nguong, cho
        self.t, self.hong, self.mo_luc = "DONG", 0, 0

    def cho_phep(self, ms):
        if self.t == "MO":
            if ms - self.mo_luc < self.cho:
                return False
            self.t = "NUA_MO"
        return True

    def ghi(self, tot, ms):
        if self.t == "NUA_MO":
            if tot:
                self.t, self.hong = "DONG", 0
            else:
                self.t, self.mo_luc = "MO", ms
        elif tot:
            self.hong = 0
        else:
            self.hong += 1
            if self.hong >= self.nguong:
                self.t, self.mo_luc = "MO", ms


c = CauDao(2, 600)
that = chan = 0
for ms in range(0, 3001, 300):
    tot = ms >= 1500
    if not c.cho_phep(ms):
        chan += 1
        print(f"t={ms} chan")
        continue
    c.ghi(tot, ms)
    that += 1
    print(f"t={ms} {'tot' if tot else 'hong'} -> {c.t}")
print(f"goi that {that}, bi chan {chan}")
