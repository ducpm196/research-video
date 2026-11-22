import sqlite3
c = sqlite3.connect(':memory:')
for q in ['CREATE TABLE ledger(bal INT)', 'INSERT INTO ledger VALUES(400)']:
    c.execute(q)
c.execute('CREATE TABLE idem(k TEXT PRIMARY KEY)')
app = 0
for att in range(1, 4):
    try:
        with c:
            c.execute("INSERT INTO idem VALUES('req-42')")
            c.execute('UPDATE ledger SET bal = bal - 125')
        app += 1
    except sqlite3.IntegrityError: pass
bal = c.execute('SELECT bal FROM ledger').fetchone()[0]
print(f'tx_attempts={att}\napplied_once={app}\nfinal_balance={bal}')
