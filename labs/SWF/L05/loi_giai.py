import itertools
def run(cases):
    br, pa = set(), set()
    for a, b, c in cases:
        for i, v in enumerate((a, b, c)): br.add((i, bool(v)))
        pa.add((a, b, c))
    return len(br), len(pa)
b2, p2 = run([(1,1,1), (0,0,0)]); _, p8 = run(list(itertools.product([0,1], repeat=3)))
print(f'two_cases_branches={b2}/6')
print(f'two_cases_paths={p2}/8')
print(f'full_cases_needed={p8}')
