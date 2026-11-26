import sys, math
s = sys.stdin.read().strip() or "2.0 0.5 1.2 0.0 0.6|0.6,0.0;0.4,0.5;0.2,-0.6"
hdr, cs = s.split("|")
gx, gy, ox, oy, vmax = map(float, hdr.split())
cands = [tuple(map(float, x.split(","))) for x in cs.split(";")]
scored = []
for v, w in cands:
    x, y, th = v * math.cos(w), v * math.sin(w), w
    head = max(0.0, 1.0 - abs(math.atan2(gy - y, gx - x) - th) / math.pi)
    clr = min(1.0, math.hypot(x - ox, y - oy))
    tot = round(0.4 * head + 0.4 * clr + 0.2 * (v / vmax), 3)
    scored.append((tot, (v, w)))
print(f"scores={scored} best={max(scored)}")
