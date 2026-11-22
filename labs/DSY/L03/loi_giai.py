import itertools
nodes = (0, 1, 2)
def dis(r, w): return sum(not (set(a) & set(b)) for a in itertools.combinations(nodes, r) for b in itertools.combinations(nodes, w))
print(f'quorum_2_2_all_intersect={int(dis(2,2) == 0)}')
print(f'pair_1_2_disjoint_cases={dis(1,2)}')
print(f'n5_min_r_when_w3={5 - 3 + 1}')
