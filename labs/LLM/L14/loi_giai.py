import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
pf = (6.0 * kv['params'] * kv['train_toks']) / (1e15 * 86400.0); rat = kv['opt_toks'] / kv['opt_params']
print(f'model_pf_days={pf:.0f} tokens_per_param={rat:.0f}')
