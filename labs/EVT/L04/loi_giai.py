import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
deltas = [int(v) for v in kv['deltas'].split(',')]
st, ev = int(kv['store']), int(kv['every'])
print(f'balance={sum(deltas)}\nsnapshots={st // ev}\nmax_replay={ev - 1}')
