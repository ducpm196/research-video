import math


def so_sanh(ten, a, b, gioi_han=300):
    # lan_dau: n nhỏ nhất có a(n) > b(n); mai_mai: n nhỏ nhất để a(n) > b(n) với MỌI n từ đó đến gioi_han
    lan_dau = next(n for n in range(1, gioi_han + 1) if a(n) > b(n))
    mai_mai = None
    for n in range(gioi_han, 0, -1):
        if a(n) > b(n):
            mai_mai = n
        else:
            break
    print(f"{ten}: lan dau {lan_dau}, mai mai tu {mai_mai}")


so_sanh("2^n va n^5", lambda n: 2 ** n, lambda n: n ** 5)
so_sanh("2^n va n^10", lambda n: 2 ** n, lambda n: n ** 10)
so_sanh("n! va 3^n", lambda n: math.factorial(n), lambda n: 3 ** n)
so_sanh("4^n va 1000*2^n", lambda n: 4 ** n, lambda n: 1000 * 2 ** n)
