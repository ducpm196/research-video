import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
q = lambda n: n // 2 + 1
mf = lambda n: n - q(n)
n1, n2 = kv['n1'], kv['n2']
print(f'quorum_4={q(n1)} max_fail_4={mf(n1)}')
print(f'quorum_5={q(n2)} max_fail_5={mf(n2)}')
print(f'odd_beats_even={int(mf(n2) > mf(n1))}')
