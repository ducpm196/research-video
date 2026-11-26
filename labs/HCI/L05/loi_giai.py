import sys
s = sys.stdin.read().strip() or "0.20 1.10 0.40 1.35 0.20"
K, P, H, M, BB = map(float, s.split())
mouse_s = H + M + P + BB + P + BB + 3 * K
key_s = H + 2 * K + M + 3 * K + K
print(f"mouse_s={mouse_s:.2f} keyboard_s={key_s:.2f}")
