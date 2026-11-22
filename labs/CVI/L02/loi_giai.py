px = [8, 8, 10, 44, 46, 50]
cands = []
for t in range(9, 50):
    g0, g1 = [x for x in px if x <= t], [x for x in px if x > t]
    if g0 and g1:
        w = (len(g0) / len(px)) * (len(g1) / len(px))
        v = w * (sum(g0) / len(g0) - sum(g1) / len(g1)) ** 2
        cands.append((round(v, 9), t))
best_v, best_t = min(cands, key=lambda item: (-item[0], item[1]))
print(f"best_thr={best_t} between_var={best_v:.1f}")
