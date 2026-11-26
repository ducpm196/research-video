import sys
s = sys.stdin.read().strip() or "512 16"
n, b = map(int, s.split())
naive = 2 * (n ** 3); tiled = naive // b
print(f"naive_reads={naive} tiled_reads={tiled} reduction={b}x")
