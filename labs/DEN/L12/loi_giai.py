import sqlite3, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE scd(city TEXT, f TEXT, t TEXT)')
rows = [tuple(r.split(':')) for r in kv['rows'].split(',')]
c.executemany('INSERT INTO scd VALUES(?,?,?)', rows)
q = lambda d: c.execute('SELECT city FROM scd WHERE ? BETWEEN f AND t', (d,)).fetchone()[0]
n_r = c.execute('SELECT COUNT(*) FROM scd').fetchone()[0]
print(f'scd_rows={n_r}\ncity_mar20={q(kv["d1"])}\ncity_may01={q(kv["d2"])}')
