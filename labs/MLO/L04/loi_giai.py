import random, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rng = random.Random(kv['seed'])
best = max(sum(rng.random() < 0.5 for _ in range(kv['samples'])) / kv['samples'] for _ in range(kv['models']))
print(f'true_skill=0.50 best_lucky_val={best:.2f}')
