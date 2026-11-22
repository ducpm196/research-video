from collections import Counter
c = Counter(t // 5 for t in (1, 2, 3, 7, 8, 12))
print(f'win0_count={c[0]}')
print(f'win1_count={c[1]}')
print(f'win2_count={c[2]}')
