n, b = 512, 16
naive = 2 * (n ** 3)
tiled = naive // b
print(f"naive_reads={naive} tiled_reads={tiled} reduction={b}x")
