import sys
s = sys.stdin.read().strip() or "3"
k = int(s); c = 0
for _ in range(k):
    r1 = c; r2 = c
    c = r1 + 1; c = r2 + 1
print(f"racy_final={c} expected_atomic={2 * k}")
