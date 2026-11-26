import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
cur = [int(x) for x in kv['board'].split(',')]; hs = int(kv['hstar'])
h1 = sum(1 for i, v in enumerate(cur) if v != 0 and v != i)
h2 = sum(abs(i // 3 - v // 3) + abs(i % 3 - v % 3) for i, v in enumerate(cur) if v != 0)
print(f'h1={h1} h2={h2} admissible={int(h1 <= h2 <= hs)}')
