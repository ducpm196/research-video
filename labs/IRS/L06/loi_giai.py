import math
cos = lambda a, b: (
    sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
)
u, v, w = (4.0, 2.0, 0.0), (5.0, 0.0, 3.0), (1.0, 3.0, 5.0)
c_uv, c_uw = cos(u, v), cos(u, w)
pred_u3 = (c_uv * v[2] + c_uw * w[2]) / (c_uv + c_uw)
print(f"cosUV={c_uv:.3f} cosUW={c_uw:.3f} pred_u3={pred_u3:.2f}")
