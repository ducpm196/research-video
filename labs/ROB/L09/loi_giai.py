import math
cands = [(0.6, 0.0), (0.4, 0.5), (0.2, -0.6)]
scored = []
for v, w in cands:
    x, y, th = v * math.cos(w), v * math.sin(w), w
    head = max(0.0, 1.0 - abs(math.atan2(0.5 - y, 2.0 - x) - th) / math.pi)
    clr = min(1.0, math.hypot(x - 1.2, y - 0.0))
    tot = round(0.4 * head + 0.4 * clr + 0.2 * (v / 0.6), 3)
    scored.append((tot, (v, w)))
print(f"scores={scored} best={max(scored)}")
