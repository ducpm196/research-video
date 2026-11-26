import sys, datetime as dt
s = sys.stdin.read().strip() or "2024-02-01 45"
ds, vs = s.split()
y, m, d = map(int, ds.split("-"))
d0 = dt.date(y, m, d)
v = int(vs)
days_pub = (v + 30) if v <= 90 else 90
print(f"d90={d0 + dt.timedelta(days=90)} d_patched={d0 + dt.timedelta(days=days_pub)} exploit_7d={d0 + dt.timedelta(days=7)}")
