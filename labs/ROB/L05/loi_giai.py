import sys, math
s = sys.stdin.read().strip() or "2.0 30.0"
vh, th_deg = map(float, s.split())
th = math.radians(th_deg)
dx = -vh * math.sin(th)
dy = vh * math.cos(th)
print(f"jac_theta=({dx:.3f}, {dy:.3f})")
