import sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE scd(city TEXT, f TEXT, t TEXT)')
rows = [('HCM','2026-01-01','2026-04-14'),('HN','2026-04-15','9999-12-31')]
c.executemany('INSERT INTO scd VALUES(?,?,?)', rows)
sql = 'SELECT city FROM scd WHERE ? BETWEEN f AND t'
q = lambda d: c.execute(sql, (d,)).fetchone()[0]
n_r = c.execute('SELECT COUNT(*) FROM scd').fetchone()[0]
print(f'scd_rows={n_r}')
print(f'city_mar20={q("2026-03-20")}')
print(f'city_may01={q("2026-05-01")}')
