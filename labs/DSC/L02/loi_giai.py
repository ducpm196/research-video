import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
lv = [int(x) for x in kv['left'].split(',')]; rv = kv['right'].split(',')
j = [(a, b) for a in lv for b in rv]
print(f'joined_rows={len(j)} fake_sum={sum(x[0] for x in j)}')
