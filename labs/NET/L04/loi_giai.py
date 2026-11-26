import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
tbl = {}
for ev in kv['events'].split(','):
    src, pt = ev.rsplit(':', 1); tbl[src] = int(pt)
print(f'pure_aloha_pct={100 / (2 * math.e):.1f}%')
print(f'slotted_aloha_pct={100 / math.e:.1f}%')
print(f'switch_mac_entries={len(tbl)}')
