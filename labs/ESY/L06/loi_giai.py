import sys
s = sys.stdin.read().strip() or "2.5 1.75"
fa, fb = map(float, s.split())
a, b = int(fa * 256), int(fb * 256)
prod = (a * b) >> 8
print(f"q88_a={a} q88_prod={prod} val={prod / 256:.3f}")
