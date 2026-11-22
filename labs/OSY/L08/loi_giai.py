holes0 = [100, 500, 200, 300, 600]; reqs = [212, 417, 112, 426]
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
