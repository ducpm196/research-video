import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rgs = [(i * kv['width'], i * kv['width'] + kv['width'] - 1) for i in range(kv['groups'])]
hit = sum(mn <= kv['target'] <= mx for mn, mx in rgs)
print(f'groups_scanned={hit}\nskipped_pct={100 * (len(rgs) - hit) / len(rgs):.1f}%')
