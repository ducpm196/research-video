import sys, math
s = sys.stdin.read().strip() or "0.1 0.15 300 28 48"
a, b, D, W1, W2 = map(float, s.split())
fitts = lambda W: a + b * math.log2(D / W + 1.0)
ratio = (W2 * W2) / (W1 * W1)
print(f"area_ratio={ratio:.2f}x t_28px={fitts(W1):.3f}s t_48px={fitts(W2):.3f}s")
