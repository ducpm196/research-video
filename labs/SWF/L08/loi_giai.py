TRANS = {'RED': {'GREEN'}, 'GREEN': {'YELLOW'}, 'YELLOW': {'RED'}}
cur = 'RED'; ok = True
for nxt in ('GREEN', 'YELLOW', 'RED'):
    if nxt not in TRANS[cur]: ok = False; break
    cur = nxt
bad = 'RED' not in TRANS['GREEN']
print(f'valid_cycle_ok={int(ok)}')
print(f'skip_green_to_red_rejected={int(bad)}')
print(f'final_state={cur}')
