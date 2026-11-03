# PAR L07 — mái nhà: tính lại bằng phân số chính xác, đếm byte/phép của vòng lặp chạy thật (cỡ nhỏ rồi ngoại suy theo công thức đã
# kiểm), và mô phỏng thời gian “tính chồng chuyển” từng khối (khác `checks`: số thực + alg.par_roofline).
from fractions import Fraction as F


def count_vec_add(n):  # chạy vòng cộng vector thật, đếm phép và byte (số 32 bit)
    a, b, c = list(range(n)), list(range(n)), [0] * n
    ops = rd = wr = 0
    for i in range(n):
        x, y = a[i], b[i]; rd += 8
        c[i] = x + y; ops += 1; wr += 4
    return ops, rd + wr


def roof(peak, bw, inten):
    t_comp, t_move = F(1, 1) / peak, F(1, 1) / (bw * inten)  # thời gian cho 1 phép
    return 1 / max(t_comp, t_move)


ops, byt = count_vec_add(1000)
I_vec = F(ops, byt)
Fpk, Bw = F(10 ** 13), F(10 ** 12)
rec("L07a", I_vec == F(1, 12) and round(float(roof(Fpk, Bw, I_vec)) / 1e9, 1) == 83.3
    and round(float(roof(Fpk, Bw, I_vec) / Fpk) * 100, 2) == 0.83 and Fpk / Bw == 10,
    "cộng vector đếm thật: I = 1/12; trần 83,3 tỉ = 0,83% đỉnh; điểm gãy 10")


def count_matmul(n, reuse):  # đếm phép và byte bộ nhớ chính của nhân ma trận n × n chạy thật
    import random
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    ops = byt = 0
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]; ops += 2
                if not reuse:
                    byt += 8
    byt = byt + 4 * n * n if not reuse else 12 * n * n  # ngây thơ: + ghi C; lý tưởng: đọc A, B, ghi C một lần
    return ops, byt


o16, b16 = count_matmul(16, True)
o16n, b16n = count_matmul(16, False)
rec("L07b", F(o16, b16) == F(2 * 16, 12) and F(2 * 4096, 12) > 682 and round(float(F(2 * 4096, 12)), 1) == 682.7
    and 2 * 4096 ** 3 == 137438953472 and 12 * 4096 ** 2 == 201326592 and roof(Fpk, Bw, F(2 * 4096, 12)) == Fpk,
    "nhân ma trận lý tưởng: I = 2n/12 (đếm thật n = 16) → 682,7 với n = 4096, chạm mái phẳng")
rec("L07c", abs(F(o16n, b16n) - F(1, 4)) < F(1, 100) and roof(Fpk, Bw, F(1, 4)) == 250 * 10 ** 9,
    "nhân ngây thơ đếm thật: I ≈ 0,25 → 250 tỉ (2,5%)")
# kiểm thời gian bằng mô phỏng từng khối 1 triệu phần tử: tính và chuyển chạy chồng (đường ống hai tầng)
blocks, t_c, t_m = 1000, F(10 ** 6, 10 ** 13), F(12 * 10 ** 6, 10 ** 12)
done_m = done_c = F(0)
for _ in range(blocks):
    done_m += t_m
    done_c = max(done_c, done_m) + t_c
rec("L07d", round(float(done_c) * 1e3, 1) == 12.0 and round(10 ** 9 / float(done_c) / 1e9, 1) == 83.3
    and round(2 * 4096 ** 3 / 1e13 * 1e3, 1) == 13.7 and round(12 * 4096 ** 2 / 1e12 * 1e3, 1) == 0.2,
    "mô phỏng 1000 khối chồng tính–chuyển: xong ≈ 12 ms, 83,3 tỉ; nhân ma trận 13,7 ms tính, 0,2 ms chuyển")
rec("L07e", float(min(F(176, 10), F(15) * F(8, 24))) == 5.0 and round(8 / 24, 2) == 0.33,
    "Opteron X2 [WWP08]: 17,6 tỉ phép/s, 15 tỉ byte/s, mẫu lưới 8/24 → 5 tỉ")
X, Y = (F(20 * 10 ** 12), F(10 ** 12)), (F(10 ** 13), F(2 * 10 ** 12))
rec("L07f", X[0] / X[1] == 20 and Y[0] / Y[1] == 5 and roof(*X, 4) == 4 * 10 ** 12 and roof(*Y, 4) == 8 * 10 ** 12
    and roof(*X, 40) == 20 * 10 ** 12 and roof(*Y, 40) == 10 ** 13
    and roof(F(2 * 10 ** 13), Bw, F(1, 12)) == roof(Fpk, Bw, F(1, 12)) and round(float(roof(Fpk, 2 * Bw, F(1, 12))) / 1e9, 1) == 166.7,
    "quiz: điểm gãy 20 và 5; I = 4 chọn Y (8 > 4); I = 40 chọn X (20 > 10); lỗi 2: đỉnh gấp đôi không đổi, băng thông gấp đôi 166,7 tỉ")
