import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b = kv['base']; goal = math.floor(b * 0.9 * 10000) / 10000
imp = (b - kv['ach']) / b * 100
mgap = round(2 * kv['k_params'] / (kv['n_rows'] / 2), 5)
opt = math.sqrt(kv['ref'] ** 2 + mgap) - kv['ref']
print(f'goal={goal:.4f} win_imp={imp:.2f}% blend_opt={opt:.5f}')
