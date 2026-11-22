w = (0.5, 0.2, 0.3)
sc = lambda v: sum(a * b for a, b in zip(v, w))
r, k = sc((5, 5, 1)), sc((3, 2, 5))
chosen = 'RDBMS' if r >= k else 'ShardedKV'
print(f'rdbms_score={r:.2f}')
print(f'sharded_kv_score={k:.2f}')
print(f'chosen={chosen}')
