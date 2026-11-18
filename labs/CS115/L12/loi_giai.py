import math

for n in (50, 500, 5000):
    t = 1.0
    for _ in range(n):
        t = t * 0.2
    s = n * math.log(0.2)
    ts = f"{t:.3e}" if t > 0 else "0.0"
    print(f"N={n} tich={ts} tong ln={round(s, 2)}")
s50 = 50 * math.log(0.2)
print(f"e mu tong ln (N=50): {math.exp(s50):.3e}")
print(f"ln2 + ln3 = {round(math.log(2) + math.log(3), 4)}, ln6 = {round(math.log(6), 4)}")


def f(x):
    return math.log(x**2 + 1)


h = 0.0001
print("dao ham ln(x^2+1) tai 1:", round((f(1 + h) - f(1 - h)) / (2 * h), 4))
