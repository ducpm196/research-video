import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
items = [int(v) for v in kv['items'].split(',')]
sub = sum(items)
thr, pct, flat = int(kv['thr']), float(kv['pct']), int(kv['flat'])
p10 = round(sub * (1.0 - pct)) if sub > thr else sub
f50 = max(0, sub - flat)
print(f'subtotal={sub}')
print(f'pct10_total={p10}')
print(f'flat50_total={f50}')
