import sys
s = sys.stdin.read().strip() or "100 512 32"
n, rbits, ebits = map(int, s.split())
lanes = rbits // ebits
print(f"simd_lanes={lanes} vec_ops={n // lanes} scalar_tail={n % lanes}")
