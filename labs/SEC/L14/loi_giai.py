import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def chk(s):
    c, m, o = (int(v) for v in s.split(','))
    return (c >= 3, m >= 2, o >= 1)
r1, r2 = chk(kv['c1']), chk(kv['c2'])
print(f'same_disk_210_ok={int(all(r1))}')
print(f'full_321_ok={int(all(r2))}')
print(f'missing_in_210={sum(not x for x in r1)}')
