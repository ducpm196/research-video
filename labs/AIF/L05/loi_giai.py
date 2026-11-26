import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, k = int(kv['n']), int(kv['colors'])
edges = [tuple(int(x) for x in p.split(':')) for p in kv['edges'].split(',') if p]
ok = 0; tot = k ** n
for m in range(tot):
    c = [(m // (k ** i)) % k for i in range(n)]
    if all(c[u] != c[v] for u, v in edges): ok += 1
print(f'total_assign={tot} valid_solutions={ok}')
