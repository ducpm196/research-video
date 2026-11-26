import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
act = [float(x) for x in kv['act'].split(',')]; pred = [float(x) for x in kv['pred'].split(',')]
mae = sum(abs(a - p) for a, p in zip(act, pred)) / len(act)
print(f'mae={mae:.2f} mape_undefined={int(any(a == 0 for a in act))}')
