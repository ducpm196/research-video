c1 = [1.0, 2.0, 3.0]
c2 = [5.0, 6.0, 7.0]
m1 = sum(c1) / len(c1)
m2 = sum(c2) / len(c2)
s1 = sum((x - m1) ** 2 for x in c1)
s2 = sum((x - m2) ** 2 for x in c2)
j = (m1 - m2) ** 2 / (s1 + s2)
print(f"m1={m1:.1f} m2={m2:.1f} J={j:.2f}")
print(f"max_dims_3class={3 - 1}")
