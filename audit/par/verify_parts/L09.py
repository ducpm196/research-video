# PAR L09 — nhân ma trận chia khối: chạy THẬT phép nhân chia khối có “bộ nhớ nhanh” mô phỏng (tập các số đang nằm trong đó), đếm
# lần nạp từ bộ nhớ chậm, đối chiếu kết quả với numpy (khác `checks`: alg.par_matmul_reads đếm theo vòng lặp khối, không nhân thật).
import numpy as np


def blocked_matmul(A, B, b):
    n = len(A)
    C = np.zeros((n, n), dtype=np.int64)
    loads = 0
    for bi in range(0, n, b):
        for bj in range(0, n, b):
            for bk in range(0, n, b):
                fastA = A[bi:bi + b, bk:bk + b].copy(); fastB = B[bk:bk + b, bj:bj + b].copy()  # nạp lên bộ nhớ nhanh
                loads += fastA.size + fastB.size
                for i in range(b):
                    for j in range(b):
                        C[bi + i, bj + j] += sum(int(fastA[i, k]) * int(fastB[k, j]) for k in range(b))
    return C, loads


def naive_loads(n):
    return sum(1 + 1 for i in range(n) for j in range(n) for k in range(n))


rng = np.random.default_rng(9)
A = rng.integers(-5, 6, (8, 8)); B = rng.integers(-5, 6, (8, 8))
res = {b: blocked_matmul(A, B, b) for b in (1, 2, 4)}
rec("L09a", all((res[b][0] == A @ B).all() for b in res) and [res[b][1] for b in (1, 2, 4)] == [1024, 512, 256] and naive_loads(8) == 1024,
    "nhân thật n = 8: kết quả trùng numpy; lần nạp 1024 / 512 / 256 = 2n³/b")
two = np.array([[1, 2], [3, 4]]) @ np.array([[5, 6], [7, 8]])
rec("L09b", two.tolist() == [[19, 22], [43, 50]] and blocked_matmul(np.arange(16).reshape(4, 4), np.ones((4, 4), int), 2)[1] == 64 and naive_loads(2) == 16,
    "ôn nền 19, 22, 43, 50; n = 4, b = 2: 64 lần nạp; n = 2 ngây thơ 16")
n = 1024
rec("L09c", 2 * n ** 3 == 2147483648 and (n // 32) ** 3 * 2 * 32 * 32 == 67108864 and 2147483648 * 4 / 1e9 > 8.58 and 67108864 * 4 == 268435456
    and [3 * b * b * 4 for b in (16, 32, 36, 37, 64)] == [3072, 12288, 15552, 16428, 49152] and 15552 <= 16384 < 16428 and 1024 % 36 != 0,
    "n = 1024: 2,15 tỉ và 67 108 864 lần đọc; ba khối 32 = 12 288 byte vừa 16 KB, 36 lớn nhất vừa, 37 và 64 không")
inten = (2 * n ** 3) / (4 * (n // 32) ** 3 * 2 * 32 * 32)
rec("L09d", inten == 8 and min(10e12, 1e12 * inten) / 10e12 == 0.8 and 2 / 8 == 0.25 and round(144.4 / 119.9, 2) == 1.20 and round(195.5 / 144.4, 2) == 1.35 and round(195.5 / 119.9, 2) == 1.63,
    "cường độ b/4 = 8 → 80% đỉnh; số của hãng 1,20 rồi 1,35 lần, tổng 1,63")
rec("L09e", 16384 // 12288 == 1 and 16384 // 3072 == 5 and 2 * 2048 ** 3 == 17179869184 and (2048 // 64) ** 3 * 2 * 64 * 64 == 268435456
    and 3 * 64 * 64 * 4 == 49152 and 3 * 128 * 128 * 4 > 49152 and 3 * 64 * 64 * 8 == 98304 and 3 * 32 * 32 * 8 == 24576,
    "lỗi 3: 1 so với 5 khối luồng mỗi cụm; quiz: b = 64 vừa khít 48 KB, đọc ít hơn 64 lần; số 64 bit → b = 32")
x = np.float32(0.1); y = np.float32(0.2); z = np.float32(0.3)
rec("L09f", (0.1 + 0.2) + 0.3 != 0.1 + (0.2 + 0.3),
    "lỗi 4: cộng số thực không kết hợp — đổi thứ tự cộng khi chia khối có thể đổi chữ số cuối")
