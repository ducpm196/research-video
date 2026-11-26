import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
tr = [float(x) for x in kv['tr'].split(',')]; te = [float(x) for x in kv['te'].split(',')]
print(f'train_mean={sum(tr) / len(tr):.1f} leaked_mean={sum(tr + te) / len(tr + te):.1f}')
