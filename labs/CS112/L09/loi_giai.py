def T(n):
    if n == 1:
        return 1
    return 4 * T(n - 1) + 1


# G(x) = x / ((1 - x)(1 - 4x)) = x / (1 - 5x + 4x^2)  =>  G * (1 - 5x + 4x^2) = x
# so sánh hệ số của x^n hai vế: c[n] - 5*c[n-1] + 4*c[n-2] = (1 nếu n == 1, ngược lại 0)
c = {-1: 0, 0: 0}
for n in range(1, 11):
    c[n] = 5 * c[n - 1] - 4 * c[n - 2] + (1 if n == 1 else 0)
print("mau so: (1 - x)(1 - 4x) = 1 - 5x + 4x^2")
print("he so 1..6 tu G:", " ".join(str(c[n]) for n in range(1, 7)))
print("he so 1..6 tu T:", " ".join(str(T(n)) for n in range(1, 7)))
print("cong thuc dong voi n = 10:", (4 ** 10 - 1) // 3)
khop = all(c[n] == T(n) == (4 ** n - 1) // 3 for n in range(1, 11))
print("khop tu n = 1 den 10:", "dung" if khop else "sai")
