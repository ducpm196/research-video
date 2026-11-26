import sys
s = sys.stdin.read().strip() or "2.0 6.0 16.0 3"
O, M, B, k = map(float, s.split())
E = (O + 4.0 * M + B) / 6.0
SD = (B - O) / 6.0
print(f"E={E:.2f} SD={SD:.2f} sum_3E={int(k) * E:.2f}")
