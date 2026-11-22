conv = lambda k, m: (
    sum(k[2 - r][2 - c] * m[r][c] for r in range(3) for c in range(3))
)
kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
e_img = [[0, 0, 12], [0, 0, 12], [0, 0, 12]]
f_img = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
print(f"sobel_edge_x={conv(kx, e_img)} flat_region={conv(kx, f_img)}")
