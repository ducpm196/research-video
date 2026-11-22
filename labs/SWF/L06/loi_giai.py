import itertools
from collections import Counter
tot = idemp = mult = 0
for xs in itertools.product((0, 1, 2), repeat=4):
    tot += 1; s = sorted(xs)
    if sorted(s) == s: idemp += 1
    if Counter(s) == Counter(xs): mult += 1
print(f'tested_sequences={tot}')
print(f'idempotent_pass={idemp}')
print(f'multiset_preserved={mult}')
