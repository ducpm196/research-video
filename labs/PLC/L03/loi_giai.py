import sys
s = sys.stdin.read().strip() or "15 6 2"
a, b, c = map(int, s.split())
print(f"left_assoc={(a - b) - c} right_assoc={a - (b - c)}")
