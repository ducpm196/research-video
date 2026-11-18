log = [("M", 10), ("N", 20), ("M", 15), ("P", 5),
       ("N", None), ("M", 12), ("Q", 7), ("P", 9)]
def nen(log, giu_bia_mo):
    cuoi = {}
    for off, (k, v) in enumerate(log):
        cuoi[k] = (off, v)
    return sorted((off, k, v) for k, (off, v) in cuoi.items()
                  if giu_bia_mo or v is not None)
def hien(ds):
    return " ".join(f"{o}:{k}:{'-' if v is None else v}" for o, k, v in ds)
print("con bia mo:", hien(nen(log, True)))
print("het han bia mo:", hien(nen(log, False)))
def khop(mau, khoa):
    p, k = mau.split("."), khoa.split(".")
    def m(i, j):
        if i == len(p):
            return j == len(k)
        if p[i] == "#":
            return any(m(i + 1, t) for t in range(j, len(k) + 1))
        return j < len(k) and p[i] in ("*", k[j]) and m(i + 1, j + 1)
    return m(0, 0)
for mau in ["payment.*.sepa", "payment.#.eur", "*.eu.#"]:
    ket_qua = "co" if khop(mau, "payment.eu.sepa.eur") else "khong"
    print("payment.eu.sepa.eur voi " + mau + ":", ket_qua)
