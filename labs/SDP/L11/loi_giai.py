import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
NEXT = {'NEW': {'PAID', 'CANCELLED'}, 'PAID': {'SHIPPED', 'CANCELLED'}, 'SHIPPED': set(), 'CANCELLED': set()}
vp = sum(len(vs) for vs in NEXT.values())
cur = 'NEW'
for s in kv['flow'].split(','):
    if s in NEXT.get(cur, set()):
        cur = s
blocked = kv['check_to'] not in NEXT.get(kv['check_from'], set())
print(f'valid_pairs={vp}')
print(f'shipped_cancel_blocked={int(blocked)}')
print(f'flow_end={cur}')
