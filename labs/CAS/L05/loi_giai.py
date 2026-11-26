import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
rate = float(kv['loss_m']) / float(kv['mins'])
prob = 1.0 - (1.0 - float(kv['p'])) ** int(kv['nodes'])
print(f'loss_per_min_M={rate:.1f} prob_any_miss={prob:.4f}')
