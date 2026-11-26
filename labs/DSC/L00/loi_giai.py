import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
diff = (kv['seen_c'] / kv['seen_n']) - (kv['un_c'] / kv['un_n'])
print(f'obs_diff={diff:.2f} needs_randomization={int(kv["obs"] == 1)}')
