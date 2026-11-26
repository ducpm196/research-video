import sqlite3, sys
rows = [tuple(int(x) for x in p.split(':')) for p in sys.stdin.read().strip().split('=', 1)[1].split(',')]
c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE s(d INT, rev INT)')
c.executemany('INSERT INTO s VALUES(?,?)', rows)
q = 'SELECT d, SUM(rev) OVER (ORDER BY d), rev-LAG(rev) OVER (ORDER BY d), RANK() OVER (ORDER BY rev DESC) FROM s ORDER BY d'
for r in c.execute(q).fetchall(): print(f'd={r[0]} cum={r[1]} diff={r[2]} rk={r[3]}')
