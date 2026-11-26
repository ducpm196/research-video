import sys
kv = dict(t.split('=', 1) for t in sys.stdin.read().split())
names = kv['names'].split(','); bf = int(kv.get('backfill', '1'))
steps = ['expand_col', 'dual_write_backfill', 'switch_reads', 'drop_old_col']
rows = [{'ten': nm, 'ho_ten': None} for nm in names]
if bf:
    for r in rows: r['ho_ten'] = r['ten']
ok = all(r['ten'] == r['ho_ten'] for r in rows)
dt = sum(1 for r in rows if r['ho_ten'] is None)
for r in rows: del r['ten']
print(f'steps_count={len(steps)}')
print(f'dual_write_synced={int(ok)}')
print(f'downtime_s={dt}')
