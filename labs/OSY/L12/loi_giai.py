blk, ptr = 4096, 4; fan = blk // ptr
d_kib = (12 * blk) // 1024
s_blk = fan
d_mib = (fan * fan * blk) // (1024 * 1024)
print(f'direct_kib={d_kib}')
print(f'single_ind_blocks={s_blk}')
print(f'double_ind_mib={d_mib}')
