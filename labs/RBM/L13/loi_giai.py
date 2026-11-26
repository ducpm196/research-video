import sys
s = sys.stdin.read().strip() or "0.5 2.0 0.5 1.0"
h, p00, p01, p11 = map(float, s.split())
F = [[1.0, h], [0.0, 1.0]]
P = [[p00, p01], [p01, p11]]
mm = lambda A, B: [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
Ft = [[F[j][i] for j in range(2)] for i in range(2)]
Pn = mm(mm(F, P), Ft)
print(f"pred_var_pos={Pn[0][0]:.2f} cross_cov_pos_vel={Pn[0][1]:.2f}")
