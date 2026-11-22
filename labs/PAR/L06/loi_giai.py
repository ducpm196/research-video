n, lanes = 100, 512 // 32
print(f"simd_lanes={lanes} vec_ops={n // lanes} scalar_tail={n % lanes}")
