p_h, p_v = 0.01, 0.04
p_a = {(1,1):.98, (1,0):.90, (0,1):.25, (0,0):.005}
a1_t, a2_t = 0.85, 0.75; a1_f, a2_f = 0.04, 0.02
num = den = 0.0
for h in (0, 1):
    for v in (0, 1):
        phv = (p_h if h else 1-p_h) * (p_v if v else 1-p_v)
        pa = p_a[(h, v)]
        pa12 = pa*a1_t*a2_t + (1-pa)*a1_f*a2_f
        den += phv * pa12
        if h: num += phv * pa12
print(f"P_heat_given_A12={num / den:.4f}")
