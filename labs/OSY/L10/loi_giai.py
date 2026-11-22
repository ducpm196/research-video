seq = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
def run(cap, alg):
    f = []; pf = 0
    for i, p in enumerate(seq):
        if p in f:
            if alg == 'lru': f.remove(p); f.append(p)
            continue
        pf += 1
        if len(f) == cap:
            if alg in ('fifo', 'lru'): f.pop(0)
            else: f.remove(max(f, key=lambda x: seq.index(x, i+1) if x in seq[i+1:] else 999))
        f.append(p)
    return pf
f3, f4 = run(3, 'fifo'), run(4, 'fifo')
print(f'fifo_3={f3} fifo_4={f4} belady={int(f4 > f3)}')
print(f'lru_3={run(3, "lru")}')
print(f'opt_3={run(3, "opt")}')
