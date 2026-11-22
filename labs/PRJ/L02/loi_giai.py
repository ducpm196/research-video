import hmac, hashlib, sqlite3
sec, payload = b'bank_secret', b'hdr.body'
sig = hmac.new(sec, payload, hashlib.sha256).hexdigest()
jwt_valid = int(hmac.compare_digest(sig, hmac.new(sec, payload, hashlib.sha256).hexdigest()))
db = sqlite3.connect(':memory:')
db.executescript('CREATE TABLE idem(k TEXT PRIMARY KEY, a INT); CREATE TABLE tx(id INTEGER PRIMARY KEY);')
reqs = [('k1', 400), ('k2', 500), ('k1', 400), ('k3', 300), ('k2', 500)]
for k, a in reqs:
    db.execute('INSERT OR IGNORE INTO idem VALUES(?,?)', (k, a))
cnt, tot = db.execute('SELECT COUNT(*), SUM(a) FROM idem').fetchone()
db.executemany('INSERT INTO tx(id) VALUES(?)', [(i,) for i in range(1, 1001)])
ids = [str(r[0]) for r in db.execute('SELECT id FROM tx WHERE id > 990 ORDER BY id LIMIT 3')]
print(f'jwt_valid={jwt_valid}')
print(f'executed={cnt} total_amount={tot}')
print('cursor_page=' + ','.join(ids))
