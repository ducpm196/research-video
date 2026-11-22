r1_m1, r1_m2 = 50 / 200 * 100, 24 / 200 * 100
r2_m1 = 56 / 160 * 100
print(f"c1_m1={r1_m1:.1f}% c1_m2={r1_m2:.1f}%")
print(f"c2_m1={r2_m1:.1f}% improved={int(r2_m1 > r1_m1)}")
