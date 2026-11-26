import sqlite3, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
c = sqlite3.connect(':memory:')
c.executescript('CREATE TABLE orders(id TEXT); CREATE TABLE outbox(id TEXT);')
c.execute('INSERT INTO orders VALUES(?)', (kv['bad_id'],)); c.rollback()
c.execute('INSERT INTO orders VALUES(?)', (kv['good_id'],))
c.execute('INSERT INTO outbox VALUES(?)', (kv['good_id'],)); c.commit()
o = [r[0] for r in c.execute('SELECT id FROM orders').fetchall()]
ob = [r[0] for r in c.execute('SELECT id FROM outbox').fetchall()]
print(f'orders_after_tx={o}\noutbox_after_tx={ob}')
