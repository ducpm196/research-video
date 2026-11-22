import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('CREATE TABLE o(id INT, amt INT); CREATE TABLE it(oid INT);'
                'INSERT INTO o VALUES(1,120),(2,80);'
                'INSERT INTO it VALUES(1),(1),(1),(1),(2);')
bad = c.execute('SELECT SUM(o.amt) FROM o JOIN it ON o.id=it.oid').fetchone()[0]
good = c.execute('SELECT SUM(amt) FROM o').fetchone()[0]
print(f"joined_wrong={bad} true_sum={good}")
