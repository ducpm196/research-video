import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
TRANS = {'RED': {'GREEN'}, 'GREEN': {'YELLOW'}, 'YELLOW': {'RED'}}
cur = kv['start']
ok = True
for nxt in kv['seq'].split(','):
    if nxt not in TRANS.get(cur, set()):
        ok = False
        break
    cur = nxt
bad = kv['bad_to'] not in TRANS.get(kv['bad_from'], set())
print(f'valid_cycle_ok={int(ok)}')
print(f'skip_green_to_red_rejected={int(bad)}')
print(f'final_state={cur}')
