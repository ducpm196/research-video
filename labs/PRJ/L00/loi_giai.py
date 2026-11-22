import sqlite3
rows = [('IN', '1000'), ('OUT', '300'), ('IN', '500'), ('BAD', 'xyz'), ('OUT', '200')]
ok, bad, in_tot, out_tot = [], 0, 0, 0
for tp, amt in rows:
    if tp in ('IN', 'OUT') and amt.isdigit() and int(amt) > 0:
        v = int(amt)
        ok.append((tp, v))
        if tp == 'IN': in_tot += v
        else: out_tot += v
    else:
        bad += 1
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE l(tp TEXT, v INT)')
db.executemany('INSERT INTO l VALUES(?,?)', ok)
sql_net = db.execute("SELECT SUM(CASE WHEN tp='IN' THEN v ELSE -v END) FROM l").fetchone()[0]
tot = len(rows)
print(f'valid={len(ok)} bad={bad} valid_pct={100*len(ok)/tot:.1f}%')
print(f'py_net={in_tot - out_tot} sql_net={sql_net}')
print(f'in_total={in_tot} out_total={out_tot}')
