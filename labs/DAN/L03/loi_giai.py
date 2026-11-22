import sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE s(d INT, rev INT)')
c.executemany('INSERT INTO s VALUES(?,?)', [(1,20),(2,50),(3,30),(4,60)])
q = ('SELECT d, SUM(rev) OVER (ORDER BY d), '
     'rev-LAG(rev) OVER (ORDER BY d), RANK() OVER (ORDER BY rev DESC) '
     'FROM s ORDER BY d')
for r in c.execute(q).fetchall():
    print(f"d={r[0]} cum={r[1]} diff={r[2]} rk={r[3]}")
