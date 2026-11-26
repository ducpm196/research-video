import itertools, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
nodes = tuple(range(kv['n']))
def dis(r, w):
    return sum(not (set(a) & set(b)) for a in itertools.combinations(nodes, r) for b in itertools.combinations(nodes, w))
print(f'quorum_2_2_all_intersect={int(dis(kv["r_good"], kv["w_good"]) == 0)}')
print(f'pair_1_2_disjoint_cases={dis(kv["r_bad"], kv["w_bad"])}')
print(f'n5_min_r_when_w3={5 - kv["w_bad"] + 1}')
