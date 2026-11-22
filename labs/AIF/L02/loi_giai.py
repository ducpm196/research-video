cur = [0, 6, 2, 1, 3, 5, 7, 4, 8]
h1 = sum(1 for i, v in enumerate(cur) if v != 0 and v != i)
h2 = sum(abs(i // 3 - v // 3) + abs(i % 3 - v % 3)
         for i, v in enumerate(cur) if v != 0)
print(f"h1={h1} h2={h2} admissible={int(h1 <= h2 <= 10)}")
