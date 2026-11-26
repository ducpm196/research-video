import sys
s = sys.stdin.read().strip() or "256 22.7 5120.0"
N, one, cl = map(float, s.split())
ideal = N * one; eff = cl / ideal * 100.0
print(f"ideal_img_s={ideal:.1f} scaling_eff={eff:.1f}%")
