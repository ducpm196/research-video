import sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE u(n TEXT, r TEXT)'); c.executemany('INSERT INTO u VALUES(?,?)', [('an','user'),('root','admin')])
pay = "' OR '1'='1"; bad = c.execute(f"SELECT * FROM u WHERE n='{pay}'").fetchall()
safe = c.execute('SELECT * FROM u WHERE n=?', (pay,)).fetchall()
print(f'unsafe_rows_leaked={len(bad)}')
print(f'param_rows_returned={len(safe)}')
print(f'sqli_blocked={int(len(safe)==0)}')
