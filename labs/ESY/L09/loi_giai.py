import sys, math
s = sys.stdin.read().strip() or "1,5;2,8;2,16"
tasks = [tuple(map(int, x.split(","))) for x in s.split(";") if x]
n = len(tasks)
u = sum(c / p for c, p in tasks)
ll = n * (2**(1/n) - 1)
c_last = tasks[-1][0]
r = c_last
for _ in range(20):
    r = c_last + sum(math.ceil(r / p) * c for c, p in tasks[:-1])
print(f"U={u:.3f} LL_bound={ll:.4f} exact_R3={r}")
