F = [[1.0, 0.5], [0.0, 1.0]]
P = [[2.0, 0.5], [0.5, 1.0]]
def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
Ft = [[F[j][i] for j in range(2)] for i in range(2)]
P_new = mm(mm(F, P), Ft)
print(f"pred_var_pos={P_new[0][0]:.2f} cross_cov_pos_vel={P_new[0][1]:.2f}")
