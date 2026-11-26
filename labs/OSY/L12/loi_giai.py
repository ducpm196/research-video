import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
blk, ptr, dn = kv['blk'], kv['ptr'], kv['direct_n']
fan = blk // ptr
print(f'direct_kib={(dn * blk) // 1024}')
print(f'single_ind_blocks={fan}')
print(f'double_ind_mib={(fan * fan * blk) // (1024 * 1024)}')
