import sys
s = sys.stdin.read().strip() or "0,0,12;0,0,12;0,0,12|5,5,5;5,5,5;5,5,5"
e_s, f_s = s.split("|")
parse_m = lambda txt: [[int(x) for x in row.split(",")] for row in txt.split(";")]
conv = lambda k, m: sum(k[2 - r][2 - c] * m[r][c] for r in range(3) for c in range(3))
kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
print(f"sobel_edge_x={conv(kx, parse_m(e_s))} flat_region={conv(kx, parse_m(f_s))}")
