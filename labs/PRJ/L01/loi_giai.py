import sqlite3
db = sqlite3.connect(':memory:')
db.executescript('CREATE TABLE acc(id TEXT PRIMARY KEY, bal INT); CREATE TABLE ent(tx INT, id TEXT, d INT);')
db.executemany('INSERT INTO acc VALUES(?,?)', [('A', 500), ('B', 400), ('C', 150), ('FEE', 0)])
def xfer(tx, s, d, amt, fee=0):
    _order = sorted([s, d])
    bal = db.execute('SELECT bal FROM acc WHERE id=?', (s,)).fetchone()[0]
    if amt <= 0 or bal < amt + fee:
        return False
    db.execute('UPDATE acc SET bal=bal-? WHERE id=?', (amt + fee, s))
    db.execute('UPDATE acc SET bal=bal+? WHERE id=?', (amt, d))
    rows = [(tx, s, -(amt + fee)), (tx, d, amt)]
    if fee:
        db.execute("UPDATE acc SET bal=bal+? WHERE id='FEE'", (fee,))
        rows.append((tx, 'FEE', fee))
    db.executemany('INSERT INTO ent VALUES(?,?,?)', rows)
    return True
r1 = xfer(1, 'A', 'B', 300)
r2 = xfer(2, 'C', 'B', 900)
r3 = xfer(3, 'B', 'C', 150, 5)
lsum = db.execute('SELECT SUM(d) FROM ent').fetchone()[0]
bals = dict(db.execute('SELECT id, bal FROM acc').fetchall())
print(f'tx_results={r1},{r2},{r3}')
print(f'ledger_sum={lsum}')
print(f"balances=A:{bals['A']},B:{bals['B']},C:{bals['C']},FEE:{bals['FEE']}")
