import sys
raw = sys.stdin.read().strip().split('=', 1)[1]
evs = [(p.split(':')[0], int(p.split(':')[1])) for p in raw.split(',')]
seen = set(); bal = 0
for eid, amt in evs:
    if eid not in seen:
        seen.add(eid)
        bal += amt
print(f'raw_events={len(evs)}')
print(f'unique_applied={len(seen)}')
print(f'final_balance={bal}')
