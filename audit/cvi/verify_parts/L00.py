# CVI L00 — tính lại bằng numpy (mảng thật, nbytes), đếm bit, phân số chính xác — khác `checks` (alg.cvi_frame_bytes, nhân thẳng).
from fractions import Fraction as F

import numpy as np

fr = np.zeros((1080, 1920, 3), dtype=np.uint8)
rec("L00a", fr.nbytes == 6220800 == alg.cvi_frame_bytes(1920, 1080) and fr.shape[:2] == (1080, 1920),
    "khung 1920 × 1080 × 3 kênh 8 bit = 6 220 800 byte; hình dạng (1080, 1920, 3): hàng trước")
rec("L00b", round(float(F(6220800, 2 ** 20)), 2) == 5.93 and fr.nbytes * 30 == 186624000 and round(fr.nbytes * 30 / 1e6, 1) == 186.6,
    "5,93 MiB; 30 khung = 186 624 000 byte ≈ 186,6 triệu byte/s")
rec("L00c", fr.nbytes * 30 * 3600 == 671846400000 and round(10 ** 12 / (fr.nbytes * 30) / 60) == 89,
    "một giờ ≈ 672 tỉ byte; ổ 10¹² byte đầy sau ≈ 89 phút")
bits = np.unpackbits(np.zeros((4, 6, 3), dtype=np.uint8)).size
rec("L00d", bits == 576 and bits // 8 == 72 == alg.cvi_frame_bytes(6, 4) and 2073600 * 24 // 8 == 6220800,
    "ảnh 6 × 4: 576 bit = 72 byte (đếm bit bằng unpackbits); khung lớn đếm bit ra cùng 6 220 800")
lv = [np.linspace(0, 255, 2 ** b).round().astype(int).tolist() for b in (1, 2, 3)]
rec("L00e", lv[1] == [0, 85, 170, 255] and lv[2] == [0, 36, 73, 109, 146, 182, 219, 255] and len(set(np.arange(256, dtype=np.uint8))) == 256,
    "1/2/3 bit: 2/4/8 mức (màu xám trong hình); 8 bit: 256 mức")
a = np.array([200], dtype=np.uint8) + np.array([100], dtype=np.uint8)
rec("L00f", int(a[0]) == 44 and int(np.clip(np.int16(200) + np.int16(100), 0, 255)) == 255, "tràn 8 bit: 200 + 100 → 44; đổi kiểu rồi kẹp → 255")
rec("L00g", np.array([[255, 128, 0]])[:, ::-1].tolist() == [[0, 128, 255]], "đảo thứ tự kênh: cam (255, 128, 0) → (0, 128, 255)")


def lin(c):  # W3C CSS Color 4 lin_sRGB
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


best = min(range(256), key=lambda v: abs(lin(v / 255) - 0.5))
rec("L00h", round(lin(128 / 255), 3) == 0.216 and best == 188, "sRGB 128 → 0,216 ánh sáng; nửa ánh sáng ứng với giá trị lưu 188 (dò hết 256 giá trị)")
q = [np.zeros((480, 640), np.uint8).nbytes, np.zeros((224, 224, 3), np.uint8).nbytes, np.zeros((2160, 3840, 3), np.uint8).nbytes]
rec("L00i", q == [307200, 150528, 24883200] and round(6220800 / q[1], 1) == 41.3 and q[2] * 30 * 3600 == 2687385600000
    and round(10 ** 12 / (q[2] * 30) / 60, 1) == 22.3, "tự làm: 307 200; 150 528 (nhỏ hơn 41,3 lần); 4K một giờ 2,69·10¹² byte, ổ 1 TB đầy sau 22,3 phút")
