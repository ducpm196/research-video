import datetime as dt
t0 = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
t_i32 = (t0 + dt.timedelta(seconds=(1 << 31) - 1)).date()
t_u32 = (t0 + dt.timedelta(seconds=(1 << 32) - 1)).date()
bond = dt.date(2040, 6, 1)
print(f"i32_date={t_i32} u32_date={t_u32} bond_2040_fails={int(bond > t_i32)}")
