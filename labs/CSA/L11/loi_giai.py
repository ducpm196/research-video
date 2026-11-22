def split_a(a): return (a >> 7), ((a >> 4) & 0x7), (a & 0xF)
t1, i1, o1 = split_a(0x84)
tags = [None] * 8; hits = misses = conf = 0
for a in [0x00, 0x04, 0x80, 0x08]:
    tg, idx, _ = split_a(a)
    if tags[idx] == tg: hits += 1
    else:
        if tags[idx] is not None: conf += 1
        misses += 1; tags[idx] = tg
print(f'split_0x84=tag:{t1},idx:{i1},off:{o1}')
print(f'hits={hits} misses={misses}')
print(f'conflict_at_0x80={conf}')
