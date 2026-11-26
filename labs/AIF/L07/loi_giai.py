import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
ucb = lambda w, n, N: (w / n) + math.sqrt(2.0 * math.log(N) / n)
ua, ub = ucb(kv['wa'], kv['na'], kv['N']), ucb(kv['wb'], kv['nb'], kv['N'])
print(f'ucb_A={ua:.4f} ucb_B={ub:.4f}\npick={"B" if ub > ua else "A"}')
