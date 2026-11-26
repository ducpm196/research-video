import datetime as dt, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
t0 = dt.datetime(int(kv['epoch_year']), 1, 1, tzinfo=dt.timezone.utc)
ti = (t0 + dt.timedelta(seconds=(1 << 31) - 1)).date()
tu = (t0 + dt.timedelta(seconds=(1 << 32) - 1)).date()
bond = dt.date.fromisoformat(kv['bond_date'])
print(f'i32_date={ti} u32_date={tu} bond_2040_fails={int(bond > ti)}')
