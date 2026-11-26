import sys, math
s = sys.stdin.read().strip() or "60.0 2.0 0.0"
ang, vx, vy = map(float, s.split())
t = math.radians(ang)
c, si = math.cos(t), math.sin(t)
R = [[c, -si], [si, c]]
x, y = R[0][0] * vx + R[0][1] * vy, R[1][0] * vx + R[1][1] * vy
RtR = [[R[0][i]*R[0][j] + R[1][i]*R[1][j] for j in range(2)] for i in range(2)]
ortho_err = max(abs(RtR[i][j] - (1.0 if i == j else 0.0)) for i in range(2) for j in range(2))
det = R[0][0] * R[1][1] - R[0][1] * R[1][0]
print(f"rot=({x:.3f}, {y:.3f}) ortho_err={ortho_err:.1e} det={det:.3f}")
