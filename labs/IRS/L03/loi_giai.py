exact = 2_000_000
ivf = 1000 + 8 * (exact // 1000)
print(f"ivf_ops={ivf} speedup={exact / ivf:.1f}x")
