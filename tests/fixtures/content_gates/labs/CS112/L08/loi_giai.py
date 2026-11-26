def A(n):
    if n == 1:
        return 1
    return 2 * A(n - 1) + 3


def B(n):
    if n == 1:
        return 1
    return B(n - 1) + 2 * n - 1


for n in range(1, 7):
    print(f"n = {n}: A = {A(n)}, B = {B(n)}")
print("A(10) theo cong thuc dong:", 2 ** 11 - 3)
print("B(50) theo cong thuc dong:", 50 ** 2)
khop = all(A(n) == 2 ** (n + 1) - 3 and B(n) == n * n for n in range(1, 21))
print("khop voi de quy tu n = 1 den 20:", "dung" if khop else "sai")
