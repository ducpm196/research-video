import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p_h, p_v = float(kv['p_h']), float(kv['p_v'])
a1_on, a2_on = int(kv['a1']), int(kv['a2'])
p_a = {(1,1):.98, (1,0):.90, (0,1):.25, (0,0):.005}
pa1 = lambda alarm: (0.85 if alarm else 0.04) if a1_on else (0.15 if alarm else 0.96)
pa2 = lambda alarm: (0.75 if alarm else 0.02) if a2_on else (0.25 if alarm else 0.98)
num = den = 0.0
for h in (0, 1):
    for v in (0, 1):
        phv = (p_h if h else 1 - p_h) * (p_v if v else 1 - p_v); pa = p_a[(h, v)]
        pa12 = pa * pa1(1) * pa2(1) + (1 - pa) * pa1(0) * pa2(0)
        den += phv * pa12
        if h: num += phv * pa12
print(f'P_heat_given_A12={num / den:.4f}')
