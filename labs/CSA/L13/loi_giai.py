def amdahl(p, n): return 1.0 / ((1.0 - p) + p / n)
print(f'speedup_4={amdahl(0.80, 4):.2f}')
print(f'speedup_16={amdahl(0.80, 16):.2f}')
print(f'max_limit={1.0 / (1.0 - 0.80):.2f}')
