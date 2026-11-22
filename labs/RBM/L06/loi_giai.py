import math
def jac_det(t1_deg, t2_deg, L1=1.0, L2=0.5):
    t1, t2 = math.radians(t1_deg), math.radians(t2_deg)
    J = [
        [-L1 * math.sin(t1) - L2 * math.sin(t1 + t2), -L2 * math.sin(t1 + t2)],
        [L1 * math.cos(t1) + L2 * math.cos(t1 + t2), L2 * math.cos(t1 + t2)],
    ]
    return J[0][0] * J[1][1] - J[0][1] * J[1][0]
print(f"det_90={jac_det(30, 90):.3f} det_0={jac_det(30, 0):.3f}")
