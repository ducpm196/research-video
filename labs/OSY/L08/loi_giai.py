import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
holes0 = [int(x) for x in kv['holes'].split(',')]
reqs = [int(x) for x in kv['reqs'].split(',')]
def sim(best=False):
    h = holes0[:]; fail = []
    for r in reqs:
        cands = [i for i, v in enumerate(h) if v >= r]
        if not cands: fail.append(r); continue
        idx = min(cands, key=lambda i: h[i]) if best else cands[0]
        h[idx] -= r
    return len(reqs) - len(fail), fail, sum(h)
fp, ff, _ = sim(False); bp, bf, bf_sum = sim(True)
print(f'first_fit_placed={fp} failed=' + (','.join(map(str, ff)) or 'none'))
print(f'best_fit_placed={bp} failed=' + (','.join(map(str, bf)) or 'none'))
print(f'best_fit_free_total={bf_sum}')
