import sys
s = sys.stdin.read().strip() or "16 0.20 0.04"
N, sb, sf = map(float, s.split())
a1 = 1.0 / (sb + (1.0 - sb) / N)
a2 = 1.0 / (sf + (1.0 - sf) / N)
print(f"amdahl_before={a1:.2f}x amdahl_after={a2:.2f}x")
