import sys
s = sys.stdin.read().strip() or "1 1 0"
vx, vy, vz = map(int, s.split())
rx = lambda p: (p[0], -p[2], p[1])
rz = lambda p: (-p[1], p[0], p[2])
v = (vx, vy, vz)
p1, p2 = rz(rx(v)), rx(rz(v))
print(f"Rz_after_Rx={p1} Rx_after_Rz={p2} equal={int(p1 == p2)}")
