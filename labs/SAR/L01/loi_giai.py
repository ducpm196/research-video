import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: [float(x) for x in s.split(',')]
w, rb, sk = p(kv['w']), p(kv['rdbms']), p(kv['kv'])
r = sum(a * b for a, b in zip(rb, w)); k = sum(a * b for a, b in zip(sk, w))
print(f'rdbms_score={r:.2f}\nsharded_kv_score={k:.2f}\nchosen={"RDBMS" if r >= k else "ShardedKV"}')
