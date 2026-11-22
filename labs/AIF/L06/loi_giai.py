tree = [[4, 10, 7], [1, 5, 9], [12, 6, 3]]
visited, best = 0, -999
for ch in tree:
    mn = 999
    for v in ch:
        visited += 1; mn = min(mn, v)
        if mn <= best: break
    best = max(best, mn)
print(f"minimax={best} leaves_visited={visited}")
