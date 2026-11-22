from fractions import Fraction
from collections import Counter
raw = ('<s> em hoc toan </s>', '<s> em hoc ly </s>', '<s> anh hoc toan </s>')
sents = [s.split() for s in raw]
uni = Counter(w for s in sents for w in s[:-1])
bi = Counter((a, b) for s in sents for a, b in zip(s, s[1:]))
target = '<s> em hoc toan </s>'.split()
p = Fraction(1, 1)
for a, b in zip(target, target[1:]):
    p *= Fraction(bi[(a, b)], uni[a])
print(f"prob={p} float={float(p):.4f}")
