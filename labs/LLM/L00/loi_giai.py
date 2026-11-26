import sys
from fractions import Fraction
from collections import Counter
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(ln.split('=', 1) for ln in lines)
sents = [kv[k].split() for k in ('s1', 's2', 's3')]
uni = Counter(w for s in sents for w in s[:-1]); bi = Counter((a, b) for s in sents for a, b in zip(s, s[1:]))
tgt = kv['target'].split(); p = Fraction(1, 1)
for a, b in zip(tgt, tgt[1:]): p *= Fraction(bi[(a, b)], uni[a])
print(f'prob={p} float={float(p):.4f}')
