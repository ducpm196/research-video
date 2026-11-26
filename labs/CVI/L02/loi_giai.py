import sys
s = sys.stdin.read().strip() or "9 49|8,8,10,44,46,50"
r_s, p_s = s.split("|")
lo, hi = map(int, r_s.split())
px = [int(x) for x in p_s.split(",")]
cands = []
for t in range(lo, hi + 1):
    g0, g1 = [x for x in px if x <= t], [x for x in px if x > t]
    if g0 and g1:
        w = (len(g0) / len(px)) * (len(g1) / len(px))
        v = w * (sum(g0) / len(g0) - sum(g1) / len(g1)) ** 2
        cands.append((round(v, 9), t))
best_v, best_t = min(cands, key=lambda item: (-item[0], item[1]))
print(f"best_thr={best_t} between_var={best_v:.1f}")
