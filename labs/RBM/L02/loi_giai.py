import math
t = math.radians(30.0)
q = (math.cos(t), 0.0, 0.0, math.sin(t))
norm_q = math.sqrt(sum(c * c for c in q))
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
res = qmul(qmul(q, (0.0, 1.0, 2.0, 0.0)), (q[0], -q[1], -q[2], -q[3]))
print(f"norm_q={norm_q:.3f} rotated=({round(res[1],3)}, {round(res[2],3)}, {round(res[3],3)})")
