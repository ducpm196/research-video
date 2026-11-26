import random, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def sim(p2c):
    r = random.Random(kv['seed']); c = [0] * kv['hosts']
    for _ in range(kv['reqs']):
        a = r.randrange(kv['hosts'])
        if p2c:
            b = r.randrange(kv['hosts'])
            if c[b] < c[a]: a = b
        c[a] += 1
    return max(c)
r1, r2 = sim(False), sim(True)
print(f'max_rand1={r1}\nmax_p2c={r2}\np2c_better={int(r2 < r1)}')
