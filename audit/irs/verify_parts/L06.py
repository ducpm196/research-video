# IRS L06 — lọc cộng tác: tính lại bằng numpy (ma trận đầy đủ, chuẩn hoá hàng rồi nhân ma trận), bằng phân số + căn sympy, và bằng
# đếm tập (khác `checks`: alg.cosine dạng vòng lặp, alg.irs_knn_predict).
import numpy as np
import sympy as sp

R = np.array([[5, 3, 0], [4, 0, 4], [1, 2, 5]], float)          # U, V, W
N = R / np.linalg.norm(R, axis=1, keepdims=True)
S = N @ N.T                                                       # mọi cosin một lần
cUV = sp.Rational(20) / (sp.sqrt(34) * sp.sqrt(32))
rec("L06a", round(S[0, 1], 3) == 0.606 == round(float(cUV), 3) and round(S[0, 2], 3) == 0.344 and R[0] @ R[1] == 20 and R[0] @ R[2] == 11
    and abs(S[0, 1] - alg.cosine([5, 3, 0], [4, 0, 4])) < 1e-12 and round(float(sp.sqrt(34) * sp.sqrt(32)), 3) == 32.985,
    "cosin U–V 0,606 (= 20/√34·√32), U–W 0,344, ma trận chuẩn hoá")
w = S[0, 1:]
pred = float(w @ R[1:, 2] / w.sum())
rec("L06b", round(pred, 2) == 4.36 and 4 <= pred <= 5 and round(w[0] / w.sum(), 2) == 0.64 and round(float(w @ R[1:, 2]), 3) == 4.147
    and abs(pred - alg.irs_knn_predict(list(w), [4, 5])) < 1e-12, "dự đoán 4,36, nằm giữa 4 và 5, phần của V 0,64")
rec("L06c", [round(x, 3) for x in N[0]] == [0.857, 0.514, 0.0] and [round(x, 3) for x in N[1]] == [0.707, 0.0, 0.707],
    "vector đã chuẩn hoá (0,857; 0,514; 0) và (0,707; 0; 0,707)")
mask = R > 0
mu = np.array([R[i][mask[i]].mean() for i in range(3)])
pred_c = mu[0] + float(w @ (R[1:, 2] - mu[1:]) / w.sum())
rec("L06d", mu.tolist()[:2] == [4.0, 4.0] and round(mu[2], 3) == 2.667 and round(R[0].mean(), 2) == 2.67 and round(pred_c, 2) == 4.85,
    "trung bình đã chấm 4 / 4 / 2,667 (coi 0 là điểm: 2,67); trừ thang chấm → 4,85")
common = lambda a, b: [(x, y) for x, y in zip(a, b) if x and y]
c = common([5, 3, 0], [4, 0, 4])
rec("L06e", len(c) == 1 and c[0][0] * c[0][1] / (c[0][0] * c[0][1]) == 1 and alg.irs_cos_common([5, 3, 0], [4, 0, 4]) == 1,
    "một món chung → cosin 1")
X = np.array([0, 4, 2.])
cUX = float(R[0] @ X / np.linalg.norm(R[0]) / np.linalg.norm(X))
pq = (S[0, 1] * 4 + cUX * 2) / (S[0, 1] + cUX)
rec("L06f", R[0] @ X == 12 and round(np.linalg.norm(X), 3) == 4.472 and round(cUX, 3) == 0.46 and round(pq, 2) == 3.14
    and len(common([5, 3, 0], [0, 4, 2])) == 1 and round(np.mean([4, 5, 2]), 3) == 3.667, "quiz: 0,460; 3,14; mỗi láng giềng 1 món chung; trung bình món 3,667")
rec("L06g", sorted({"L", "M", "N"} | {"N", "O", "P", "Q"}) == list("LMNOPQ") and sum(v == "N" for v in "LMN" + "NOPQ") == 2
    and sp.binomial(10 ** 6, 2) == 499999500000, "cùng xem: hợp L…Q, N hai lần; C(10^6, 2) = 499 999 500 000")
rec("L06h", np.dot([1, 2], [3, 4]) == 11 and np.linalg.norm([3, 4]) == 5 and round(11 / (np.sqrt(5) * 5), 3) == 0.984 and (2 * 4 + 1) / 3 == 3,
    "ôn: 11, 5, 0,984, trung bình có trọng số 3")
