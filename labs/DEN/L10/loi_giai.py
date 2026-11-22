import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('CREATE TABLE orders(id TEXT); CREATE TABLE outbox(id TEXT);')
c.execute("INSERT INTO orders VALUES('O100')")
c.rollback()
c.execute("INSERT INTO orders VALUES('O200')")
c.execute("INSERT INTO outbox VALUES('O200')")
c.commit()
o = [r[0] for r in c.execute('SELECT id FROM orders').fetchall()]
ob = [r[0] for r in c.execute('SELECT id FROM outbox').fetchall()]
print(f'orders_after_tx={o}')
print(f'outbox_after_tx={ob}')
