import math


def f(x, y):
    return 3 * x**2 + x * y - 2 * y**2


x0, y0 = 2, 1
gx, gy = 6 * x0 + y0, x0 - 4 * y0
print(f"gradient bang cong thuc: [{gx}, {gy}]")
h = 0.0001
ax = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
ay = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)
print(f"gradient bang buoc nho: [{round(ax, 4)}, {round(ay, 4)}]")
print(f"do dai gradient: {round(math.sqrt(gx**2 + gy**2), 4)}")
x1, y1 = x0 - 0.01 * gx, y0 - 0.01 * gy
print(f"f(2,1) = {f(x0, y0)}; sau buoc nguoc gradient 0.01: {round(f(x1, y1), 4)}")
print("f giam:", f(x1, y1) < f(x0, y0))
