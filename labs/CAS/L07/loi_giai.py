import sys
n = int(sys.stdin.read().split('=')[1])
cubic = sum((n - s) * (n - s + 1) // 2 for s in range(n))
print(f'n={n} cubic_steps={cubic} ratio={cubic // n}x')
