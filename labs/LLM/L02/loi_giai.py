import sys
from collections import Counter
vocab = {}
for ln in sys.stdin.read().splitlines():
    if ':' in ln: k, f = ln.rsplit(':', 1); vocab[k.strip()] = int(f)
for step in (1, 2):
    pairs = Counter()
    for w, f in vocab.items():
        syms = w.split()
        for a, b in zip(syms, syms[1:]): pairs[(a, b)] += f
    best = max(pairs, key=pairs.__getitem__)
    print(f'merge{step}={best[0]}+{best[1]} freq={pairs[best]}')
    ps, ms = f'{best[0]} {best[1]}', ''.join(best)
    vocab = {w.replace(ps, ms): f for w, f in vocab.items()}
