import sys
s = sys.stdin.read().strip() or "16 0.35 500 1.15 0.45"
gpus, kw, hrs, pue, grid = map(float, s.split())
kwh = gpus * kw * hrs * pue
co2_kg = kwh * grid
print(f"kwh={kwh:.1f} co2_kg={co2_kg:.1f}")
