import sys
s = sys.stdin.read().strip() or "20.0 2.0 2.0"
peak, bw, ai = map(float, s.split())
ridge = peak / bw
att = min(peak, ai * bw)
print(f"ridge_intensity={ridge:.1f} ai={ai:.3f} max_tflops={att:.3f}")
