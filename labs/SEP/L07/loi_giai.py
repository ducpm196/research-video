import datetime as dt
d0 = dt.date(2024, 2, 1); v = 45
days_pub = min(90, v + 30) if v <= 90 else 90
print(f"d90={d0 + dt.timedelta(days=90)}",
      f"d_patched={d0 + dt.timedelta(days=days_pub)}",
      f"exploit_7d={d0 + dt.timedelta(days=7)}")
