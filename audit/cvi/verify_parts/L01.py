# CVI L01 — tính lại bằng numpy vector hoá (np.correlate, lát cắt, np.outer, np.pad) — khác `checks` (alg.cvi_xcorr2d vòng lặp thuần).
import numpy as np

Sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
Sy = Sx.T


def corr(P, K):
    P, K = np.asarray(P), np.asarray(K)
    k = K.shape[0]
    return np.array([[(P[i:i + k, j:j + k] * K).sum() for j in range(P.shape[1] - k + 1)] for i in range(P.shape[0] - k + 1)])


E = np.array([[0, 0, 10]] * 3)
D = np.array([[0, 0, 10], [0, 10, 10], [10, 10, 10]])
rec("L01a", corr(E, Sx)[0, 0] == 40 == alg.cvi_xcorr2d(E.tolist(), Sx.tolist())[0][0] and corr(np.full((3, 3), 7), Sx)[0, 0] == 0
    and corr(E, Sy)[0, 0] == 0, "cạnh dọc 40; vùng phẳng 0; cùng vùng đo dọc 0")
rec("L01b", corr(D, Sx)[0, 0] == 30 and corr(D, Sy)[0, 0] == 30 and round(float(np.hypot(30, 30)), 1) == 42.4, "cạnh chéo 30, 30 → 42,4")
rec("L01c", (np.outer([1, 2, 1], [-1, 0, 1]) == Sx).all() and (np.outer([1, 2, 1], [-1, 0, 1]).T == Sy).all(), "S_x = cột 1, 2, 1 nhân hàng −1, 0, 1")
# hai lượt một chiều
col = (E * np.array([[1], [2], [1]])).sum(0)
colD = (D * np.array([[1], [2], [1]])).sum(0)
rec("L01d", col.tolist() == [0, 0, 40] and colD.tolist() == [10, 30, 40] and col[2] - col[0] == 40 and colD[2] - colD[0] == 30, "lượt 1: 0, 0, 40 / 10, 30, 40; lượt 2: 40 / 30")
rec("L01e", corr(E, Sx[::-1, ::-1])[0, 0] == -40 == alg.cvi_conv2d(E.tolist(), Sx.tolist())[0][0], "lật bộ lọc: −40")
x = np.array([0, 0, 0, 9, 0, 0, 0, 0, 12, 12, 12, 12], float)
b = np.convolve(x, np.ones(3) / 3, mode="valid")
d_raw = np.correlate(x, [-1, 0, 1], mode="valid")
d_blur = np.correlate(b, [-1, 0, 1], mode="valid")
rec("L01f", np.allclose(b, [0, 3, 3, 3, 0, 0, 4, 8, 12, 12]) and d_raw.tolist() == [0, 9, 0, -9, 0, 0, 12, 12, 0, 0]
    and np.allclose(d_blur, [3, 0, -3, -3, 4, 8, 8, 4]), "làm mờ 0,3,3,3,0,0,4,8,12,12; hiệu thô 9 / 12; sau làm mờ 3 / 8")
rec("L01g", (np.abs(d_raw) > 6).sum() == 4 and (np.abs(d_blur) > 6).sum() == 2 and abs(d_blur[:4]).max() == 3, "ngưỡng 6: thô 4 cột vượt (2 giả); sau làm mờ chỉ 2 cột cạnh thật")
rec("L01h", int(np.int16(-40).astype(np.uint8)) == 216 and corr(np.pad(np.full((3, 5), 100), ((0, 0), (1, 0))), Sx)[0, 0] == 400
    and corr(E // 2, Sx)[0, 0] == 20, "−40 → 216; đệm 0 ở mép ảnh 100 → 400; ảnh tối nửa → 20")
rec("L01i", corr(np.array([[9, 0, 0], [0, 0, 0], [0, 0, 0]]), np.full((3, 3), 1 / 9))[0, 0] == 1 and corr(np.array([[10] * 3, [0] * 3, [0] * 3]), Sy)[0, 0] == -40
    and corr(np.array([[10] * 3, [0] * 3, [0] * 3]), Sx)[0, 0] == 0 and corr(np.array([[1, 2], [3, 4]]), np.array([[1, 0], [0, -1]]))[0, 0] == -3,
    "tự làm: 1; G_x 0, G_y −40, độ lớn 40; ôn nền −3")
rec("L01j", 9 == 3 * 3 and 3 + 3 == 6 and np.allclose(np.convolve(np.convolve(E[:, 2], [1, 2, 1], "valid"), [1], "valid"), [40]), "9 phép nhân so với 6")
