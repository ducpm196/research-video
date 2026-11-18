import math
n = 128
c = 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n
offset = -0.6
print("c(128) =", round(c, 4))
for ten, h in (("A", 2), ("B", 9)):
    diem = -2 ** (-h / c)
    qd = diem - offset
    print(ten, "diem", round(diem, 4), "quyet dinh", round(qd, 4), "nhan", -1 if qd < 0 else 1)
so = math.ceil(0.03 * (3000 - 1))
print("bi gan -1:", so, "| gan oan:", so - 25)
