X_col = [4.0, 3.0]
A = [[2.0, 1.0], [1.0, 2.0]]
B = [1.0, 1.0]
for step in range(1, 3):
    pred = [A[r][0] * B[0] + A[r][1] * B[1] for r in range(2)]
    num = [A[0][c] * X_col[0] + A[1][c] * X_col[1] for c in range(2)]
    den = [A[0][c] * pred[0] + A[1][c] * pred[1] for c in range(2)]
    B = [B[c] * num[c] / den[c] for c in range(2)]
    rec = [A[r][0] * B[0] + A[r][1] * B[1] for r in range(2)]
    err = sum((X_col[r] - rec[r]) ** 2 for r in range(2))
    print(f"step{step} B={[round(x, 4) for x in B]} err={err:.4f}")
