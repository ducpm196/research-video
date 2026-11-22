import math
p1, p2 = 0.08, 0.09
pb = (p1 + p2) / 2.0
za, zb = 1.959963984540054, 0.8416212335729143
s1 = za * math.sqrt(2 * pb * (1 - pb))
s2 = zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
n = math.ceil(((s1 + s2) / (p2 - p1)) ** 2)
print(f"n_per_group={n}")
