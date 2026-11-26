import sys
s = sys.stdin.read().strip() or "0.20 12"
qs, ns = s.split(); q, N = float(qs), int(ns)
print(f"gustafson_12={q + (1.0 - q) * N:.2f}x")
