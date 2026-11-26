import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
v1 = {'order_id': int(kv['v1_id'])}; v2 = {'order_id': int(kv['v2_id']), 'tier': kv['v2_tier']}
print(f'old_reads_v2={v2["order_id"]}')
print(f'new_reads_v1={v1.get("tier", kv["def_tier"])}')
