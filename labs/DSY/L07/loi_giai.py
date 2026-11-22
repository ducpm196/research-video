from collections import defaultdict
mp = [(w, 1) for w in 'a b a c b a'.split()]
shuf = defaultdict(list)
for k, v in mp: shuf[k].append(v)
red = {k: sum(vs) for k, vs in sorted(shuf.items())}
print(f'mapped_pairs={len(mp)}')
print(f'unique_keys={len(red)}')
print('reduced=' + ','.join(f'{k}:{v}' for k, v in red.items()))
