import sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE invoices(amt INT)')
c.execute('INSERT INTO invoices VALUES(950)')
c.execute('PRAGMA query_only = ON')
val = c.execute('SELECT amt FROM invoices').fetchone()[0]
blk = 0
try:
    c.execute('DELETE FROM invoices')
except sqlite3.OperationalError:
    blk = 1
print(f'read_allowed={int(val == 950)}')
print(f'write_blocked={blk}')
print(f'blast_contained={int(blk == 1 and val == 950)}')
