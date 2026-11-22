p1 = 1 - (1 - 5/100)**40; p2 = 1 - (1 - 5/100)**5
print(f'p_conflict_40={100*p1:.1f}%')
print(f'p_conflict_5={100*p2:.1f}%')
print(f'shorter_branch_safer={int(p2 < p1)}')
