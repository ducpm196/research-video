import sys, math
s = sys.stdin.read().strip() or "A,B,C,D,E"
items = s.split(",")
n = len(items)
latin = [items[r:] + items[:r] for r in range(n)]
r_ok = all(len(set(row)) == n for row in latin)
c_ok = all(len({latin[r][c] for r in range(n)}) == n for c in range(n))
print(f"size={n} balanced={int(r_ok and c_ok)} perms_total={math.factorial(n)}")
