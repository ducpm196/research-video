import math


def W(n):
    if n == 2:
        return 6
    return math.isqrt(n) * W(math.isqrt(n)) + 3 * n


def cong_thuc(n):
    m = int(math.log2(n))
    k = int(math.log2(m))
    return n * (3 * k + 3)


khop = True
for n in (4, 16, 256, 65536):
    a, b = W(n), cong_thuc(n)
    khop = khop and a == b
    print(f"n = {n}: he thuc {a}, cong thuc {b}")
print("n = 2^32: he thuc", W(2 ** 32), "- cong thuc", cong_thuc(2 ** 32))
print("khop: " + ("dung" if khop and W(2 ** 32) == cong_thuc(2 ** 32) else "sai"))
