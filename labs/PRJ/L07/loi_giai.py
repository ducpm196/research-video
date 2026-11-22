import bisect, hashlib, sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE ord(id INT)'); c.execute('CREATE TABLE outb(id INT)')
with c: c.execute('INSERT INTO ord VALUES(1)'); c.execute('INSERT INTO outb VALUES(1)')
c.execute('BEGIN'); c.execute('INSERT INTO ord VALUES(2)'); c.execute('INSERT INTO outb VALUES(2)'); c.rollback()
eq = c.execute('SELECT COUNT(*) FROM ord').fetchone()[0] == c.execute('SELECT COUNT(*) FROM outb').fetchone()[0]
h = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)
def own(n, k):
    r = sorted((h(f'n{i}#0'), i) for i in range(n))
    return r[bisect.bisect(r, (h(f'k{k}'), 99)) % n][1]
mv = sum(own(4, k) != own(5, k) for k in range(500))
state, fails = 'CLOSED', 0
for ok in (False, False, False):
    fails = 0 if ok else fails + 1
    if fails >= 3:
        state = 'OPEN'
print(f'outbox_atomic_match={int(eq)}')
print(f'ch_moved_lt_150={int(mv < 150)}')
print(f'cb_after_3fails={state}')
