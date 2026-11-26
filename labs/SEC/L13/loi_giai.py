import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
n = kv['n_events']; prev = kv['base']
tp = n * prev * kv['tpr']; fp = n * (1 - prev) * kv['fpr']
ppv = tp / (tp + fp)
print(f'tp_per_1m={round(tp)}')
print(f'fp_per_1m={round(fp)}')
print(f'ppv_pct={100 * ppv:.2f}%')
