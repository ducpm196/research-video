import sqlite3, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
c = sqlite3.connect(':memory:'); c.executescript('CREATE TABLE o(id INT, amt INT); CREATE TABLE it(oid INT);')
c.executemany('INSERT INTO o VALUES(?,?)', [tuple(int(x) for x in p.split(':')) for p in kv['orders'].split(',')])
c.executemany('INSERT INTO it VALUES(?)', [(int(x),) for x in kv['items'].split(',')])
bad = c.execute('SELECT SUM(o.amt) FROM o JOIN it ON o.id=it.oid').fetchone()[0]
good = c.execute('SELECT SUM(amt) FROM o').fetchone()[0]
print(f'joined_wrong={bad} true_sum={good}')
