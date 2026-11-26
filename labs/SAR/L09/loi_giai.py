import sqlite3, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE ledger(bal INT)'); c.execute('INSERT INTO ledger VALUES(?)', (int(kv['init_bal']),))
c.execute('CREATE TABLE idem(k TEXT PRIMARY KEY)'); app = 0; tr = int(kv['tries']); amt = int(kv['amt'])
for _ in range(tr):
    try:
        with c:
            c.execute('INSERT INTO idem VALUES(?)', (kv['key'],))
            c.execute('UPDATE ledger SET bal = bal - ?', (amt,))
        app += 1
    except sqlite3.IntegrityError: pass
bal = c.execute('SELECT bal FROM ledger').fetchone()[0]
print(f'tx_attempts={tr}\napplied_once={app}\nfinal_balance={bal}')
