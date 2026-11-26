import sys
tree = [[int(x) for x in grp.split(',')] for grp in sys.stdin.read().strip().split('=')[1].split(';')]
vis, best = 0, -10**9
for ch in tree:
    mn = 10**9
    for v in ch:
        vis += 1; mn = min(mn, v)
        if mn <= best: break
    best = max(best, mn)
print(f'minimax={best} leaves_visited={vis}')
