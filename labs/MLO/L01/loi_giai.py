import random, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
ids = list(range(kv['n']))
a = random.Random(kv['s1']).sample(ids, kv['k'])
b = random.Random(kv['s1']).sample(ids, kv['k'])
c = random.Random(kv['s2']).sample(ids, kv['k'])
print(f'same_seed={int(a==b)} diff_seed={int(a!=c)} s7={a}')
