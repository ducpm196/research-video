imps = {'x1': 50, 'x2': 180, 'x3': 310}
clicks = [('x1', 200), ('x2', 900), ('x3', 500)]
hit = [k for k, t in clicks if k in imps and 0 <= t - imps[k] <= 600]
print(f'matched={hit}')
print(f'match_count={len(hit)}')
