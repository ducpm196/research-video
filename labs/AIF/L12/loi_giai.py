import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
r, g, it = float(kv['r']), float(kv['gamma']), int(kv['iters']); u = [0.0, 0.0, 1.0]
for _ in range(it):
    u1 = max(r + g * (0.7 * u[2] + 0.3 * u[1]), r + g * (0.7 * u[0] + 0.3 * u[1]))
    u0 = max(r + g * (0.7 * u[1] + 0.3 * u[0]), r + g * u[0])
    u[0], u[1] = u0, u1
print(f'U0={u[0]:.3f} U1={u[1]:.3f}')
