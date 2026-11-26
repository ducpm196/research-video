import itertools, sys
k = int(sys.stdin.read().split('=')[1])
def run(cases):
    br, pa = set(), set()
    for bits in cases:
        for i, v in enumerate(bits):
            br.add((i, bool(v)))
        pa.add(tuple(bits))
    return len(br), len(pa)
b2, p2 = run([tuple([1] * k), tuple([0] * k)])
_, full = run(list(itertools.product([0, 1], repeat=k)))
print(f'two_cases_branches={b2}/{2 * k}')
print(f'two_cases_paths={p2}/{full}')
print(f'full_cases_needed={full}')
