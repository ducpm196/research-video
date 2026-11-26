import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def greet(clock): return 'Chuc mung nam moi' if clock() == (1, 1) else 'Ngay binh thuong'
r1 = greet(lambda: (kv['m1'], kv['d1']))
r2 = greet(lambda: (kv['m2'], kv['d2']))
det = int(r1 == greet(lambda: (kv['m1'], kv['d1'])))
print(f'jan1={r1}')
print(f'may10={r2}')
print(f'deterministic={det}')
