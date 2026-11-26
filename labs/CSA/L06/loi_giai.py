import sys
def add8(a, b):
    s = (a + b) & 0xFF
    cf = int(a + b > 255)
    sa, sb, ss = (a >> 7) & 1, (b >> 7) & 1, (s >> 7) & 1
    ov = int(sa == sb and ss != sa)
    return s, ov, cf
kv = dict(t.split('=') for t in sys.stdin.read().split())
a1, b1 = map(int, kv['p1'].split(','))
c, d = map(int, kv['sub'].split(','))
a2, b2 = map(int, kv['p2'].split(','))
s1, ov1, cf1 = add8(a1, b1)
s2, _, _ = add8(c, ((~d) + 1) & 0xFF)
s3, _, cf3 = add8(a2, b2)
print(f'add_100_50={s1} ov_signed={ov1} cf_unsigned={cf1}')
print(f'sub_40_15={s2}')
print(f'add_200_100={s3} cf_unsigned={cf3}')
