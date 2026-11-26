import sys
s = sys.stdin.read().strip() or "16"
n = int(s); f = (n - 1) // 3; quorum = n - f
print(f"max_byzantine={f} quorum_2_3={quorum}")
