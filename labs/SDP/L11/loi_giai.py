NEXT = {'NEW': {'PAID','CANCELLED'}, 'PAID': {'SHIPPED','CANCELLED'}, 'SHIPPED': set(), 'CANCELLED': set()}
states = ('NEW', 'PAID', 'SHIPPED')
vp = sum(b in NEXT[a] for a in states for b in states) + sum(s in ('NEW','PAID') for s in states)
cur = 'NEW'
for s in ('PAID', 'SHIPPED'): cur = s if s in NEXT[cur] else cur
print(f'valid_pairs={vp}')
print(f'shipped_cancel_blocked={int("CANCELLED" not in NEXT["SHIPPED"])}')
print(f'flow_end={cur}')
