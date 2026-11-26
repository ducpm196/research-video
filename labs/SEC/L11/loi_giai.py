import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
s1, s2 = 2 ** kv['b_low'], 2 ** kv['b_high']
print(f'slots_16bit={s1}')
print(f'expected_guesses_16={s1 // 2}')
print(f'slots_28bit={s2}')
