def dao_ham(w):
    return 6 * (w - 2)


def chay(eta, so_buoc):
    w = 10.0
    ds = [w]
    for _ in range(so_buoc):
        w = w - eta * dao_ham(w)
        ds.append(round(w, 4))
    return ds


a = chay(0.1, 4)
print("eta=0.1:", [round(x, 4) for x in a])
b = chay(0.4, 3)
print("eta=0.4:", [round(x, 4) for x in b])
print("phan ky:", abs(b[3] - 2) > abs(b[0] - 2))
N, D, B = 1000000, 100, 100
print(f"GD 1 buoc: {N * D} phep; SGD 1 buoc: {B * D} phep; buoc SGD moi epoch: {N // B}")
