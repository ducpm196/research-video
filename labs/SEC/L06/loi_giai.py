import html, sqlite3
e = html.escape('<script>alert(1)</script>')
c = sqlite3.connect(':memory:'); c.execute('CREATE TABLE u(n TEXT)'); c.execute("INSERT INTO u VALUES('an')")
rows = c.execute('SELECT * FROM u WHERE n=?', ("' OR '1'='1",)).fetchall()
print(f'raw_lt_present={int("<" in e)}')
print(f'escaped_len={len(e)}')
print(f'sqli_rows={len(rows)}')
