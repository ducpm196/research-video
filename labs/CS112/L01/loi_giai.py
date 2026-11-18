def f(n):
    return 2 * n * n + 10 * n + 30


def nguong(c, gioi_han=2000):
    # n0 nhỏ nhất sao cho f(n) <= c * n * n với MỌI n từ n0 đến gioi_han; None nếu ngay n = gioi_han đã sai
    n0 = None
    for n in range(gioi_han, 0, -1):
        if f(n) <= c * n * n:
            n0 = n
        else:
            break
    return n0


for c in (2, 3, 4, 5):
    n0 = nguong(c)
    print(f"c = {c}: " + ("khong co n0" if n0 is None else f"n0 = {n0}"))
print("ty so f(n)/n^2 voi n = 100000:", round(f(100000) / 100000 ** 2, 4))
