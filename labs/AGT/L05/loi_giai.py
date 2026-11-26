import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tp = kv['base'] * kv['tpr']; fp = (1.0 - kv['base']) * kv['fpr']
print(f'accepted_true_pct={tp / (tp + fp) * 100:.1f}%')
