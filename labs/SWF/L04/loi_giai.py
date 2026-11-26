import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def tri(nums):
    x, y, z = sorted(int(v) for v in nums.split(','))
    if x <= 0 or x + y <= z:
        return 'none'
    if x == z:
        return 'equilateral'
    return 'isosceles' if (x == y or y == z) else 'scalene'
print(f't333={tri(kv["c1"])} t334={tri(kv["c2"])}')
print(f't345={tri(kv["c3"])}')
print(f'boundary_123={tri(kv["c4"])}')
