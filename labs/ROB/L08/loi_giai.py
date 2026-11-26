import sys
s = sys.stdin.read().strip() or "100 2 5"
lv, d1, d2 = map(int, s.split())
g2 = lv ** d1; g5 = lv ** d2
print(f"grid_2d={g2} grid_5dof={g5:.0e} ratio={g5 // g2}")
