import sqlite3, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE invoices(amt INT)')
c.execute('INSERT INTO invoices VALUES(?)', (kv['amt'],))
if kv['read_only']: c.execute('PRAGMA query_only = ON')
val = c.execute('SELECT amt FROM invoices').fetchone()[0]; blk = 0
try: c.execute('DELETE FROM invoices')
except sqlite3.OperationalError: blk = 1
ok_r = int(val == kv.get('expect', kv['amt']))
print(f'read_allowed={ok_r}\nwrite_blocked={blk}\nblast_contained={int(blk == 1 and ok_r == 1)}')
