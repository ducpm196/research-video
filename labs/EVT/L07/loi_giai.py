import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
imps = {p.split(':')[0]: int(p.split(':')[1]) for p in kv['imps'].split(',')}
clks = [(p.split(':')[0], int(p.split(':')[1])) for p in kv['clicks'].split(',')]
w = int(kv['win']); hit = [k for k, t in clks if k in imps and 0 <= t - imps[k] <= w]
print(f'matched={hit}\nmatch_count={len(hit)}')
