import sys
from collections import Counter
kv = dict(t.split('=') for t in sys.stdin.read().split())
w = int(kv['win_s'])
c = Counter(int(v) // w for v in kv['ts'].split(','))
print(f'win0_count={c[0]}')
print(f'win1_count={c[1]}')
print(f'win2_count={c[2]}')
