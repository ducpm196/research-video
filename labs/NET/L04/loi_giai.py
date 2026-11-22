import math
tbl = {}
for src, port in (('AA:01', 1), ('BB:02', 3), ('AA:01', 1)): tbl[src] = port
print(f'pure_aloha_pct={100 / (2 * math.e):.1f}%')
print(f'slotted_aloha_pct={100 / math.e:.1f}%')
print(f'switch_mac_entries={len(tbl)}')
