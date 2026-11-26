import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
lines, ib, ob = int(kv['lines']), int(kv['idx_bits']), int(kv['off_bits'])
imask, omask = (1 << ib) - 1, (1 << ob) - 1
split_a = lambda a: (a >> (ib + ob), (a >> ob) & imask, a & omask)
t1, i1, o1 = split_a(int(kv['probe'], 16))
tags = [None] * lines; hits = misses = conf = 0
for s in kv['seq'].split(','):
    tg, idx, _ = split_a(int(s, 16))
    if tags[idx] == tg: hits += 1
    else:
        if tags[idx] is not None: conf += 1
        misses += 1; tags[idx] = tg
print(f'split_0x84=tag:{t1},idx:{i1},off:{o1}')
print(f'hits={hits} misses={misses}')
print(f'conflict_at_0x80={conf}')
