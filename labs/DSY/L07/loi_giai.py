import sys
from collections import defaultdict
words = sys.stdin.read().split()
mp = [(w, 1) for w in words]
shuf = defaultdict(list)
for k, v in mp: shuf[k].append(v)
red = {k: sum(vs) for k, vs in sorted(shuf.items())}
print(f'mapped_pairs={len(mp)}')
print(f'unique_keys={len(red)}')
print('reduced=' + ','.join(f'{k}:{v}' for k, v in red.items()))
