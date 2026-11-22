import math
A = [[0.0, 1.0], [-6.0, -5.0]]
tr = A[0][0] + A[1][1]
det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
disc = math.sqrt(tr*tr - 4.0*det)
l1, l2 = (tr + disc) / 2.0, (tr - disc) / 2.0
print(f"eigs=({l1:.1f}, {l2:.1f}) stable={int(l1 < 0 and l2 < 0)}")
