import sys
s = sys.stdin.read().strip() or "0.92 32 4 100"
bs, ps, r1s, r2s = s.split()
base, p, r1, r2 = float(bs), int(ps), float(r1s), float(r2s)
phong = base ** p
mc_err_ratio = (r2 / r1) ** 0.5
print(f"phong={phong:.3f} mc_noise_reduction={mc_err_ratio:.1f}x")
