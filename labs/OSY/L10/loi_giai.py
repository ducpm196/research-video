import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
seq = [int(x) for x in kv['seq'].split(',')]; c1, c2 = int(kv['c1']), int(kv['c2'])
def run(cap, alg):
    f = []; pf = 0
    for i, p in enumerate(seq):
        if p in f:
            if alg == 'lru': f.remove(p); f.append(p)
            continue
        pf += 1
        if len(f) == cap:
            if alg in ('fifo', 'lru'): f.pop(0)
            else: f.remove(max(f, key=lambda x: seq.index(x, i+1) if x in seq[i+1:] else 999999))
        f.append(p)
    return pf
f1, f2 = run(c1, 'fifo'), run(c2, 'fifo')
print(f'fifo_3={f1} fifo_4={f2} belady={int(f2 > f1)}')
print(f'lru_3={run(c1, "lru")}')
print(f'opt_3={run(c1, "opt")}')
