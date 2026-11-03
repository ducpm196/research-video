# CVI L08 — tính lại bằng mặt nạ điểm ảnh numpy (đếm ô cho IoU), ghép vét cạn mọi hoán vị nhỏ, và tích phân thẳng đường
# độ chuẩn xác bằng numpy — khác `checks` (alg.cvi_box_iou công thức góc, alg.cvi_match_dets tham lam, alg.cvi_ap).
import itertools
from fractions import Fraction as F

import numpy as np


def mask(b, W=120, H=20):
    m = np.zeros((H, W), bool)
    m[b[1]:b[3], b[0]:b[2]] = True
    return m


def iou_px(a, b):
    A, B = mask(a), mask(b)
    return (A & B).sum() / (A | B).sum()


rec("L08a", (mask((0, 0, 10, 10)) & mask((5, 5, 15, 15))).sum() == 25 and (mask((0, 0, 10, 10)) | mask((5, 5, 15, 15))).sum() == 175
    and round(iou_px((0, 0, 10, 10), (1, 0, 11, 10)), 3) == 0.818 and iou_px((0, 0, 10, 10), (20, 0, 30, 10)) == 0,
    "đếm điểm ảnh: giao 25, hợp 175 (0,143); lệch 1 điểm ảnh 0,818; rời nhau 0")
G = [(0, 0, 10, 10), (20, 0, 30, 10), (40, 0, 50, 10)]
D = [(0.95, (1, 0, 11, 10)), (0.9, (23, 0, 33, 10)), (0.8, (60, 0, 70, 10)), (0.6, (41, 1, 50, 10)), (0.4, (80, 0, 90, 10))]
rec("L08b", [round(max(iou_px(b, g) for g in G), 3) for _, b in D] == [0.818, 0.538, 0.0, 0.81, 0.0], "IoU lớn nhất của 5 phát hiện")


def match(D, G, t):
    # mỗi phát hiện (theo điểm) lấy hộp thật chưa ghép có IoU ≥ t lớn nhất — đếm bằng mặt nạ
    used, out = set(), []
    for _, b in sorted(D, key=lambda d: -d[0]):
        c = [(iou_px(b, g), k) for k, g in enumerate(G) if k not in used and iou_px(b, g) >= t]
        out.append(bool(c))
        if c:
            used.add(max(c)[1])
    return out


def ap_area(tp, n):
    tp = np.array(tp, bool)
    ctp = np.cumsum(tp); cfp = np.cumsum(~tp)
    prec, recl = ctp / (ctp + cfp), ctp / n
    env = np.maximum.accumulate(prec[::-1])[::-1]
    r = np.concatenate([[0], recl])
    return float(np.sum((r[1:] - r[:-1]) * env))


m5 = match(D, G, 0.5)
rec("L08c", m5 == [True, True, False, True, False] == alg.cvi_match_dets(D, G, 0.5) and round(ap_area(m5, 3), 3) == 0.917
    and F(1, 3) * 1 + F(1, 3) * 1 + F(1, 3) * F(3, 4) == F(11, 12), "ngưỡng 0,5: đ đ s đ s → AP = 11/12 ≈ 0,917")
m75 = match(D, G, 0.75)
rec("L08d", m75 == [True, False, False, True, False] and ap_area(m75, 3) == 0.5, "ngưỡng 0,75: AP 0,5")
aps = [ap_area(match(D, G, t), 3) for t in np.round(np.linspace(0.5, 0.95, 10), 2)]
rec("L08e", [round(a, 3) for a in aps] == [0.917] + [0.5] * 6 + [0.0] * 3 and round(np.mean(aps), 3) == 0.392
    and round(alg.cvi_ap101(m5, 3), 3) == 0.916, "10 ngưỡng 0,5…0,95: trung bình 0,392; đọc 101 mức độ phủ ở ngưỡng 0,5: 0,916")
# loại bỏ không cực đại — làm lại bằng vét: giữ hộp i nếu không hộp nào điểm cao hơn ĐÃ GIỮ chồng với nó quá 0,5
B = [(0, 0, 10, 10), (1, 0, 11, 10), (5, 5, 15, 15)]
keep = []
for i in sorted(range(3), key=lambda i: -[0.9, 0.8, 0.7][i]):
    if all(iou_px(B[i], B[k]) <= 0.5 for k in keep):
        keep.append(i)
rec("L08f", keep == [0, 2] == alg.cvi_nms(B, [0.9, 0.8, 0.7]), "loại bỏ không cực đại: giữ A và B, bỏ D")
D2 = D + [(0.93, (0, 1, 10, 11))]
m2 = match(D2, G, 0.5)
rec("L08g", m2 == [True, False, True, False, True, False] and round(ap_area(m2, 3), 3) == 0.756 and round(iou_px((0, 1, 10, 11), (1, 0, 11, 10)), 3) == 0.681,
    "hộp trùng không loại bỏ: AP 0,756; hai hộp chồng 0,681")
rec("L08h", iou_px((0, 0, 4, 4), (1, 0, 5, 4)) == 0.6 and round((99 * 100) / (100 * 100 * 2 - 99 * 100), 2) == 0.98
    and round(min(0.5, 16 / 196), 3) == 0.082, "vật nhỏ: 0,6 so với 0,98; ngưỡng nới 0,082")
rec("L08i", iou_px((5, 5, 15, 15), (5, 5, 10, 10)) == 0.25 and abs(iou_px((0, 0, 4, 4), (2, 0, 6, 4)) - 1 / 3) < 1e-12, "đọc nhầm [x, y, rộng, cao]: 0,25; tự làm câu 1: 1/3")
qb = [(0, 0, 4, 4), (2, 0, 6, 4), (1, 0, 5, 4)]
qk = []
for i in range(3):
    if all(iou_px(qb[i], qb[k]) <= 0.5 for k in qk):
        qk.append(i)
rec("L08j", qk == [0, 1] and round((0.917 + 0.60) / 2, 3) == 0.758 and F(9, 108) == F(1, 12), "tự làm câu 2: giữ hộp 1, 2; mAP 0,758; ôn nền 1/12")
# ghép tham lam trùng ghép tối ưu (vét mọi phép gán) ở ví dụ — không có xung đột
best = max(sum(iou_px(D[i][1], G[k]) >= 0.5 for i, k in zip(p, range(3))) for p in itertools.permutations(range(5), 3))
rec("L08k", best == 3 == sum(m5), "vét mọi phép gán: tối đa 3 cặp đúng, khớp ghép tham lam")
