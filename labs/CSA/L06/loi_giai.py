def add8(a, b):
    s = (a + b) & 0xFF
    cf = int(a + b > 255)
    sa, sb, ss = (a >> 7) & 1, (b >> 7) & 1, (s >> 7) & 1
    ov = int(sa == sb and ss != sa)
    return s, ov, cf
s1, ov1, cf1 = add8(100, 50)
s2, _, _ = add8(40, ((~15) + 1) & 0xFF)
s3, _, cf3 = add8(200, 100)
print(f'add_100_50={s1} ov_signed={ov1} cf_unsigned={cf1}')
print(f'sub_40_15={s2}')
print(f'add_200_100={s3} cf_unsigned={cf3}')
