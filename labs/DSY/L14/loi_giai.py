evs = [('#41', 100), ('#42', 50), ('#42', 50), ('#43', 25)]; seen = set(); bal = 0
for eid, amt in evs:
    if eid not in seen: seen.add(eid); bal += amt
print(f'raw_events={len(evs)}')
print(f'unique_applied={len(seen)}')
print(f'final_balance={bal}')
