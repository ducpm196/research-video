import math
vh, th = 2.0, math.radians(30.0)
dx_dth = -vh * math.sin(th)
dy_dth = vh * math.cos(th)
print(f"jac_theta=({dx_dth:.3f}, {dy_dth:.3f})")
