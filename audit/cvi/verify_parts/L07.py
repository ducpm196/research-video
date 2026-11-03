# CVI L07 — tính lại bằng mô phỏng (chọc từng điểm ảnh qua chồng tích chập numpy, đo trường tiếp nhận thật cả khi có bước nhảy),
# đếm tham số bằng mảng trọng số thật, chữ số bảy đoạn vẽ bằng ma trận điểm rồi lật/xoay bằng numpy — khác `checks`
# (alg.cvi_receptive_field công thức, alg.cvi_seg7_transform bảng ánh xạ đoạn).
import numpy as np


def rf_sim(layers, n=101):
    """Đo trường tiếp nhận của ô ra ở giữa bằng cách bật từng điểm ảnh (1 chiều), tích chập + lấy mẫu theo bước nhảy."""
    def run(x):
        for k, s in layers:
            x = np.convolve(x, np.ones(k), "valid")[::s]
        return x
    out_len = len(run(np.zeros(n)))
    c = out_len // 2
    hit = [i for i in range(n) if run(np.eye(n)[i])[c] != 0]
    return hit[-1] - hit[0] + 1


rec("L07a", [rf_sim([(3, 1)] * m) for m in (1, 2, 3, 5)] == [3, 5, 7, 11] == [alg.cvi_receptive_field([(3, 1)] * m) for m in (1, 2, 3, 5)],
    "mô phỏng: 1, 2, 3, 5 lớp 3 × 3 → 3, 5, 7, 11")
rec("L07b", rf_sim([(7, 2), (3, 2), (3, 1)]) == 19 == alg.cvi_receptive_field([(7, 2), (3, 2), (3, 1)]) and rf_sim([(7, 2), (3, 2)]) == 11,
    "mô phỏng tầng đầu (7 bước 2, gộp 3 bước 2, 3 × 3): 7 → 11 → 19")
head = np.zeros((10, 512)).size + np.zeros(10).size
conv = np.zeros((512, 512, 3, 3)).size + 512
rec("L07c", head == 5130 and conv == 2359808 and round(conv / head) == 460 and np.zeros((3, 512)).size + 3 == 1539 and np.zeros((64, 3, 3, 3)).size + 64 == 1792,
    "tham số: đầu phân loại 5130; lớp 3 × 3 × 512 × 512: 2 359 808 (≈ 460 lần); 3 lớp quả 1539; lớp đầu 1792")
W = np.array([[0.5, -1, 1, 0], [1, 1, -0.5, 0.5]]); b = np.array([0.1, 0]); x = np.array([1, 0, 2, 1])
rec("L07d", np.allclose(W @ x + b, [2.6, 0.5]) and int(np.argmax(W @ x + b)) == 0 and W.size + b.size == 10, "điểm 2,6 / 0,5 → trầy xước; 10 tham số")
# chữ số bảy đoạn trên lưới 5 × 3 điểm: a trên, b phải trên, c phải dưới, d dưới, e trái dưới, f trái trên, g giữa
SEG = {"a": [(0, 0), (0, 1), (0, 2)], "b": [(0, 2), (1, 2), (2, 2)], "c": [(2, 2), (3, 2), (4, 2)], "d": [(4, 0), (4, 1), (4, 2)],
       "e": [(2, 0), (3, 0), (4, 0)], "f": [(0, 0), (1, 0), (2, 0)], "g": [(2, 0), (2, 1), (2, 2)]}
DIG = {0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg", 5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg"}


def draw(segs):
    m = np.zeros((5, 3), int)
    for sg in segs:
        for r, c in SEG[sg]:
            m[r, c] = 1
    return m


def which(m):
    return next((k for k, v in DIG.items() if (draw(v) == m).all()), None)


rec("L07e", which(np.rot90(draw(DIG[6]), 2)) == 9 and which(np.fliplr(draw(DIG[2]))) == 5 and which(np.fliplr(draw(DIG[6]))) is None
    and which(np.fliplr(draw(DIG[8]))) == 8 and alg.cvi_seg7_transform(6, "rot180") == 9 and alg.cvi_seg7_transform(2, "flip") == 5,
    "vẽ điểm rồi xoay/lật: 6 → 9, 2 → 5, 6 lật → không phải chữ số, 8 lật → 8 (khớp bảng đoạn)")
rec("L07f", (224 + 2 * 3 - 7) // 2 + 1 == 112 and (112 + 2 * 1 - 3) // 2 + 1 == 56 and np.allclose([(180 - 120) / 60, (60 - 120) / 60], [1, -1])
    and np.allclose([180 / 255, 60 / 255], [0.70588, 0.23529], atol=1e-4), "224 → 112 → 56; chuẩn hoá 1 / −1 so với 0,706 / 0,235")
