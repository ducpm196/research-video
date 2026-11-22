import re
pat = re.compile(r'^(0|1)*10$')
ok = True; cnt = 0
for L in range(8):
    for m in range(1 << L):
        s = format(m, f'0{L}b') if L else ''
        hit = bool(pat.fullmatch(s))
        if hit != s.endswith('10'):
            ok = False
        cnt += int(hit)
print(f"matches={cnt} exact={int(ok)}")
