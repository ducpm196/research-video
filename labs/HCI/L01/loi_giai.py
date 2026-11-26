import sys, math
s = sys.stdin.read().strip() or "6"
n = int(s)
print(f"linear_guesses={math.factorial(n)} matched_2d={int(len(set(range(n))) == n)}")
