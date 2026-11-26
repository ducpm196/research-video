import sys
vers = sys.stdin.read().strip().split('=', 1)[1].split(',')
key = lambda s: tuple(map(int, s.split('.')))
vs = sorted(vers, key=key, reverse=True)
va, vb = vers[0], vers[-1]
print(f'semver_1_10_gt_1_9={int(key(va) > key(vb))}')
print(f'str_cmp_bug={int((va < vb) and (key(va) > key(vb)))}')
print('sorted_desc=' + ','.join(vs))
