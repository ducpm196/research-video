import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
k = kv['k']; rrf = lambda r1, r2: 1.0 / (k + r1) + 1.0 / (k + r2)
sa, sb = rrf(kv['a1'], kv['a2']), rrf(kv['b1'], kv['b2'])
print(f'score_A={sa:.5f} score_B={sb:.5f} win={"B" if sb > sa else "A"}')
