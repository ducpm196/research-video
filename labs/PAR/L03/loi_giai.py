c = 0
for _ in range(3):
    r1 = c; r2 = c
    c = r1 + 1; c = r2 + 1
print(f"racy_final={c} expected_atomic=6")
