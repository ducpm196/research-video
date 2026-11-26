import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
clicks = [int(x) for x in kv['init'].split(',')]; rds, add = int(kv['rounds']), int(kv['add'])
for _ in range(rds):
    for i in sorted(range(len(clicks)), key=lambda i: (-clicks[i], i))[:2]: clicks[i] += add
sh = sum(sorted(clicks, reverse=True)[:2]) / sum(clicks) * 100
print(f'clicks={clicks} top2_share={sh:.1f}%')
