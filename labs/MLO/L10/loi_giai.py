import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = [float(x) for x in kv['probs'].split(',')]; y = [float(x) for x in kv['y'].split(',')]
print(f'brier={sum((a - b) ** 2 for a, b in zip(p, y)) / len(y):.4f}')
