import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
kw = kv['kw']; b = kv.get('bias', '')
pred = lambda s: 0 if (b and b in s) else (1 if kw in s else 0)
inv_ok = all(pred(f'{n} is {kw}') == 1 for n in kv['names'].split(','))
sls = [float(p.split(':')[1]) for p in kv['slices'].split(',')]
print(f'inv_pass={int(inv_ok)} min_slice_pass={int(min(sls) >= float(kv["thr"]))}')
