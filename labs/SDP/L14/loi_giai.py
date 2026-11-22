def bump(v, k):
    M, m, p = v
    return (M, m, p+1) if k=='patch' else ((M, m+1, 0) if k=='minor' else (M+1, 0, 0))
fmt = lambda v: '.'.join(map(str, v))
print(f'patch={fmt(bump((1,4,2),"patch"))} minor={fmt(bump((1,4,2),"minor"))} major={fmt(bump((1,4,2),"major"))}')
print(f'tuple_cmp_1_10_gt_1_9={int((1,10,0) > (1,9,3))}')
print(f'str_cmp_wrong={int("1.10.0" < "1.9.3")}')
