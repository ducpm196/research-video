import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
toks = [kv['base'] + kv['inc'] * k for k in range(kv['steps'])]
print(f'final_ctx={toks[-1]} total_input={sum(toks)} mult={sum(toks) / toks[-1]:.2f}x')
