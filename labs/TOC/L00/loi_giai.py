import sys
from itertools import product
s = sys.stdin.read().strip() or "01|4"
alp, ms = s.split("|"); maxlen = int(ms)
chains = ["".join(p) for k in range(maxlen + 1) for p in product(alp, repeat=k)]
nonempty = [c for c in chains if len(c) > 0]
print(f"count_le4={len(chains)} nonempty={len(nonempty)}")
