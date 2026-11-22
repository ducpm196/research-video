seq = [0x00, 0x80, 0x00, 0x80]
dm = None; dh = dm_m = 0
for a in seq:
    tg = a >> 7
    if dm == tg: dh += 1
    else: dm_m += 1; dm = tg
lru = []; lh = lm = 0
for a in seq:
    tg = a >> 7
    if tg in lru: lh += 1; lru.remove(tg); lru.append(tg)
    else:
        lm += 1
        if len(lru) == 2: lru.pop(0)
        lru.append(tg)
print(f'direct_mapped_hits={dh} misses={dm_m}')
print(f'two_way_lru_hits={lh} misses={lm}')
print('final_set0_order=' + ','.join(f'0x{t<<7:02X}' for t in lru))
