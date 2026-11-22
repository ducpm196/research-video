def mv3(M, v):
    return tuple(round(sum(M[i][j]*v[j] for j in range(3)), 2) for i in range(3))
R = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
T = [[1, 0, 3], [0, 1, -1], [0, 0, 1]]
p = (1, 2, 1)
print(f"T_after_R={mv3(T, mv3(R, p))[:2]} R_after_T={mv3(R, mv3(T, p))[:2]}")
