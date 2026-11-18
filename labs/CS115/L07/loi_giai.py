def f(x, y):
    return [x * y, x**2 - y, x + y**2]


def jacobian(x, y):
    return [[y, x], [2 * x, -1], [1, 2 * y]]


x0, y0 = 2, 3
J = jacobian(x0, y0)
print("J =", J)
buoc = [0.1, -0.1]
du_doan = [round(J[i][0] * buoc[0] + J[i][1] * buoc[1], 4) for i in range(3)]
f0, f1 = f(x0, y0), f(x0 + 0.1, y0 - 0.1)
thuc_te = [round(f1[i] - f0[i], 4) for i in range(3)]
print("du doan:", du_doan)
print("thuc te:", thuc_te)

a, b, c = f(x0, y0)
J_ngoai = [2 * a, c, b]
print("Jacobian ngoai:", J_ngoai)
hop = [sum(J_ngoai[i] * J[i][j] for i in range(3)) for j in range(2)]
print("gradient hop (J ngoai nhan J):", hop)


def H(x, y):
    a, b, c = f(x, y)
    return a**2 + b * c


e = 0.00001
gx = (H(x0 + e, y0) - H(x0 - e, y0)) / (2 * e)
gy = (H(x0, y0 + e) - H(x0, y0 - e)) / (2 * e)
print("gradient truc tiep (buoc nho):", [round(gx, 2), round(gy, 2)])
