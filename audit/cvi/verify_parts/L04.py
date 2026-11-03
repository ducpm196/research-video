# CVI L04 — tính lại bằng numpy (lát cắt mảng, np.roll, np.linalg.norm, sắp xếp ma trận khoảng cách) — khác `checks`
# (alg.cvi_ssd_shift / alg.cvi_match vòng lặp thuần, math.dist).
import numpy as np

I = np.zeros((11, 11))
I[4:, 4:] = 10


def ssd(r, c, dc, dr):
    win = I[r - 1:r + 2, c - 1:c + 2]
    sh = I[r - 1 + dr:r + 2 + dr, c - 1 + dc:c + 2 + dc]
    return int(((sh - win) ** 2).sum())


E = {k: [ssd(r, c, a, b) for a, b in [(1, 0), (0, 1), (1, 1)]] for k, (r, c) in {"phẳng": (8, 1), "cạnh": (4, 8), "góc": (4, 4)}.items()}
rec("L04a", E == {"phẳng": [0, 0, 0], "cạnh": [0, 300, 300], "góc": [200, 200, 500]}
    and E["góc"] == [alg.cvi_ssd_shift(I.astype(int).tolist(), 4, 4, b, a) for a, b in [(1, 0), (0, 1), (1, 1)]],
    "E: phẳng 0,0,0; cạnh 0,300,300; góc 200,200,500")
rec("L04b", [min(v) for v in E.values()] == [0, 0, 200], "min: chỉ góc khác 0 (200)")
A = np.array([[0.2, 0.2], [0.8, 0.8]])
B = np.array([[0.5, 0.2], [0.2, 0.7], [1.07, 1.16], [0.5, 1.2]])
D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
srt = np.sort(D, axis=1)
rec("L04c", np.allclose(D.round(3), [[0.3, 0.5, 1.296, 1.044], [0.671, 0.608, 0.45, 0.5]]) and np.argmin(D, axis=1).tolist() == [0, 2],
    "ma trận khoảng cách 2 × 4; gần nhất của p là b1, của q là b3")
ratio = srt[:, 0] / srt[:, 1]
rec("L04d", np.allclose(ratio, [0.6, 0.9]) and (ratio < 0.8).tolist() == [True, False]
    and [m[5] for m in alg.cvi_match(A.tolist(), B.tolist())] == [True, False], "tỉ số 0,6 giữ; 0,9 bỏ (khớp alg.cvi_match)")
r2 = (srt[:, 0] ** 2) / (srt[:, 1] ** 2)
rec("L04e", np.allclose(r2, [0.36, 0.81]) and ((r2 < 0.64) == (ratio < 0.8)).all(), "so bình phương với 0,64 cho cùng quyết định")
rec("L04f", abs(0.43 / 0.5 - 0.86) < 1e-12 and (0.43 / 0.5) ** 2 < 0.8 < 0.43 / 0.5 and round(0.8 ** 0.5, 3) == 0.894,
    "lỗi 4: 0,86 bỏ đúng; bình phương 0,74 so 0,8 giữ sai; ngưỡng thật √0,8 ≈ 0,894")
kept_true, kept_false = 100 - 100 * 5 // 100, 100 - 100 * 90 // 100
rec("L04g", (kept_true, kept_false) == (95, 10) and round(kept_true / (kept_true + kept_false), 3) == 0.905 and 4 * 4 * 8 == 128,
    "mở đầu: ≥ 95 đúng, ≤ 10 sai → 90,5%; mô tả 4·4·8 = 128 (CITED Lowe 2004)")
rec("L04h", round(0.40 / 0.42, 3) == 0.952 and 0.2 / 0.4 == 0.5, "tự làm: 0,5 giữ; 0,952 bỏ")
