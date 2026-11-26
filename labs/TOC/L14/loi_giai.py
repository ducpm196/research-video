import sys
s = sys.stdin.read().strip() or "25"
n = int(s)
bt = 2 ** n; sp = n + 1; lc = n * sp
print(f"backtrack={bt} subset_pos={sp} linear_checks={lc}")
