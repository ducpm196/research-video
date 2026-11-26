import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p, k = float(kv['p']), int(kv['k'])
print(f'pass_at_4={(1.0 - (1.0 - p)**k)*100:.1f}% pass_pow_4={(p**k)*100:.1f}%')
