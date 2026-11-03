# PAR L10 — gộp toàn phần theo vòng: mô phỏng lại bằng hộp thư (mỗi bước mọi máy gửi vào hộp thư của máy phải rồi mới nhận), chỉ số
# mảnh tính theo cách khác (máy i ở bước s gửi mảnh có tổng dở dang “đi được s + 1 máy”), đối chiếu tổng numpy; thời gian bằng mô phỏng
# sự kiện từng đường (khác `checks`: alg.par_ring_allreduce / par_ring_time / par_ps_time).
from fractions import Fraction as F
import numpy as np


def ring_mailbox(vecs):
    n = len(vecs); c = len(vecs[0]) // n
    buf = [np.array(v, dtype=np.int64).reshape(n, c) for v in vecs]
    sent = [0] * n
    for phase in ("rs", "ag"):
        for s in range(n - 1):
            box = {}
            for i in range(n):
                k = (i - s) % n if phase == "rs" else (i + 1 - s) % n
                box[(i + 1) % n] = (k, buf[i][k].copy()); sent[i] += c
            for j, (k, data) in box.items():
                buf[j][k] = buf[j][k] + data if phase == "rs" else data
    return [b.reshape(-1) for b in buf], sent


rng = np.random.default_rng(10)
ok = True
for n in (2, 3, 4, 8):
    V = rng.integers(-50, 50, (n, 4 * n))
    out, sent = ring_mailbox(V)
    ok &= all((o == V.sum(axis=0)).all() for o in out) and sent == [2 * (n - 1) * 4] * n
rec("L10a", ok and ring_mailbox([[1, 2, 3], [10, 20, 30], [100, 200, 300]])[1] == [4, 4, 4]
    and [list(map(int, o)) for o in ring_mailbox([[1, 2, 3], [10, 20, 30], [100, 200, 300]])[0]] == [[111, 222, 333]] * 3
    and ring_mailbox([[1] * 8] * 4)[1] == [12] * 4,
    "hộp thư n = 2, 3, 4, 8: mọi máy có đúng tổng numpy, mỗi máy gửi 2(n − 1) mảnh; 3 máy: 111, 222, 333, 4 số mỗi máy; 4 máy × 8 số: 12")
rec("L10b", [2 * F(n - 1, n) for n in (2, 8, 64, 1024)] == [1, F(7, 4), F(63, 32), F(1023, 512)] and all(2 * F(n - 1, n) < 2 for n in range(2, 5000)),
    "hệ số 1; 1,75; 1,96875; 1,998; luôn nhỏ hơn 2")


def sim_ring(n, size, bws, lat=0.0):  # mỗi bước: mọi đường chạy song song, bước xong khi đường chậm nhất xong
    t = 0.0
    for _ in range(2 * (n - 1)):
        t += max(lat + (size / n) / b for b in bws)
    return t


def sim_ps(n, size, bw, lat=0.0):  # máy chủ nhận lần lượt n gói rồi gửi lần lượt n gói qua một đường
    t = lat
    for _ in range(n):
        t += size / bw
    t += lat
    for _ in range(n):
        t += size / bw
    return t


rec("L10c", abs(sim_ring(8, 1, [10] * 8) - 0.175) < 1e-12 and abs(sim_ps(8, 1, 10) - 1.6) < 1e-12 and round(1.6 / 0.175, 1) == 9.1
    and abs(sim_ring(64, 1, [10] * 64) - 0.196875) < 1e-12 and abs(sim_ps(64, 1, 10) - 12.8) < 1e-9 and round(0.8 / 0.175, 2) == 4.57,
    "mô phỏng từng đường: vòng 8 máy 0,175 s, máy chủ 1,6 s (≈ 9,1 lần; hai chiều 0,8 s ≈ 4,57 lần); 64 máy 0,197 s và 12,8 s")
rec("L10d", abs(sim_ring(8, 1, [10] * 7 + [1]) - 1.75) < 1e-12 and abs(sim_ring(64, 1e-3, [10] * 64, 50e-6) * 1e3 - 6.496875) < 1e-9
    and abs(126 * 50e-6 - 6.3e-3) < 1e-15,
    "một đường 1 GB/s: 1,75 s (gấp 10); 64 máy gói 1 MB trễ 0,05 ms: 6,5 ms, trong đó 6,3 ms là trễ")
rec("L10e", abs(sim_ring(16, 2, [25] * 16) - 0.15) < 1e-12 and abs(sim_ps(16, 2, 25) - 2.56) < 1e-12 and abs(sim_ps(16, 1, 25) - 1.28) < 1e-12
    and abs(sim_ring(16, 2e-3, [25] * 16, 5e-3) - 0.15015) < 1e-12 and abs(sim_ps(16, 2e-3, 25, 5e-3) - 0.01256) < 1e-12,
    "quiz: gói 2 GB vòng 0,15 s, máy chủ 2,56 s, hai máy chủ 1,28 s; gói 2 MB: vòng 150,15 ms, máy chủ 12,56 ms")
rec("L10f", 1 / 10 + 0.001 == 0.101 and (1 + 3 + 5 + 7) / 4 == 4 and F(1, 8) * 1000 == 125,
    "ôn nền 0,101 s; trung bình 4; mảnh 125 MB")
