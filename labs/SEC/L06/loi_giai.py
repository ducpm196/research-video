import html, sqlite3, sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(ln.split('=', 1) for ln in lines)
e = html.escape(kv['xss'])
c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE u(n TEXT)'); c.execute("INSERT INTO u VALUES('an')")
rows = c.execute('SELECT * FROM u WHERE n=?', (kv['sqli'],)).fetchall()
print(f'raw_lt_present={int("<" in e)}')
print(f'escaped_len={len(e)}')
print(f'sqli_rows={len(rows)}')
