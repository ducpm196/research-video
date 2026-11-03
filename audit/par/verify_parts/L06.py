# PAR L06 — tính lại bằng cách KHÁC checks của bài: đếm khúc bằng range bước w (không vòng while như checklib), cộng mảng thật bằng
# numpy theo khúc 8 phần tử và so với cộng từng phần tử, chạy lại phép truy hồi bằng numpy.cumsum (cách đúng) và bằng “8 làn đọc giá trị
# cũ” (cách sai), cộng tổng theo làn bằng numpy reshape, và số thực 32/64 bit bằng numpy dtype.
import numpy as np


def count_chunks(n, w):
    full = [s for s in range(0, n, w) if s + w <= n]
    return len(full), n - w * len(full)


rec("L06a", count_chunks(1003, 8) == (125, 3) == alg.par_vector_split(1003, 8) and count_chunks(1003, 4) == (250, 3)
    and count_chunks(20, 8) == (2, 4) and count_chunks(1000, 8) == (125, 0) and count_chunks(1000, 16) == (62, 8),
    "khúc: 1003/8 → 125 + 3; 1003/4 → 250 + 3; 20/8 → 2 + 4; quiz 1000/8 → 125 + 0, 1000/16 → 62 + 8")
rec("L06b", np.dtype(np.float32).itemsize * 8 == 32 and 256 // (np.dtype(np.float32).itemsize * 8) == 8
    and 256 // (np.dtype(np.float64).itemsize * 8) == 4 and 512 // 64 == 8 and 512 // 32 == 16,
    "số làn: 256/32 = 8, 256/64 = 4, 512/64 = 8, 512/32 = 16 (cỡ phần tử lấy từ numpy)")
a = np.arange(1003, dtype=np.float32)
b = np.arange(1003, dtype=np.float32) * 2
c = np.empty_like(a)
vec = 0
for s in range(0, 1000, 8):
    c[s:s + 8] = a[s:s + 8] + b[s:s + 8]; vec += 1
for i in range(1000, 1003):
    c[i] = a[i] + b[i]
ref = np.array([x + y for x, y in zip(a.tolist(), b.tolist())], dtype=np.float32)
cl, v2, s2 = alg.par_vector_add(a.tolist(), b.tolist(), 8)
rec("L06c", vec == 125 and np.array_equal(c, ref) and v2 == 125 and s2 == 3 and np.allclose(cl, ref)
    and round(1003 / (125 + 3), 2) == 7.84 and round(1003 / (250 + 3), 2) == 3.96 and round(1000 / 70, 2) == 14.29,
    "cộng theo khúc 8 bằng numpy = cộng từng phần tử; 7,84 / 3,96 / 14,29 lần ít lệnh")
bb = np.ones(8, dtype=np.int64)
right = np.concatenate([[0], np.cumsum(bb)])
old = np.zeros(9, dtype=np.int64)
wrong = old.copy(); wrong[1:] = old[:-1] + bb      # 8 làn cùng đọc a[i − 1] cũ
rec("L06d", right.tolist() == alg.par_recurrence([1] * 8) and wrong.tolist() == alg.par_recurrence([1] * 8, width=8)
    and int(right.sum()) == 36 and int(wrong.sum()) == 8,
    "truy hồi: đúng 1, 2, …, 8 (tổng 36); ép 8 làn: 1, 1, …, 1 (tổng 8)")
x = np.full(16, 0.1)
seq = 0.0
for t in x.tolist():
    seq = seq + t
lanes = x.reshape(2, 8).sum(axis=0)   # làn k = phần tử k + phần tử k + 8
lane_total = 0.0
for t in lanes.tolist():
    lane_total = lane_total + t
rec("L06e", repr(seq) == "1.6000000000000003" and repr(lane_total) == "1.5999999999999999"
    and lane_total == alg.par_lane_sum([0.1] * 16, 8) and abs(seq - lane_total) < 1e-15,
    "16 × 0,1: cộng dồn 1,6000000000000003; theo 8 làn 1,5999999999999999 (numpy reshape); lệch < 10⁻¹⁵")
rec("L06f", round(20e9 / 12 / 1e9, 2) == 1.67 and min(2e9, 20e9 / 12) == min(16e9, 20e9 / 12),
    "lỗi 3: 20 GB/s ÷ 12 byte = 1,67 tỉ phần tử/giây chặn cả bản vô hướng lẫn bản vector")
