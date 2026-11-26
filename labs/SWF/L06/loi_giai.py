import itertools, sys
from collections import Counter
kv = dict(t.split('=') for t in sys.stdin.read().split())
vals = [int(v) for v in kv['vals'].split(',')]
length = int(kv['length'])
tot = idemp = mult = 0
for xs in itertools.product(vals, repeat=length):
    tot += 1
    s = sorted(xs)
    if sorted(s) == s:
        idemp += 1
    if Counter(s) == Counter(xs):
        mult += 1
print(f'tested_sequences={tot}')
print(f'idempotent_pass={idemp}')
print(f'multiset_preserved={mult}')
