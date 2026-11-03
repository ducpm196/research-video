# PAR L04 — tính lại bằng cách KHÁC checks của bài: mô phỏng theo đồng hồ (từng giây, lõi rảnh nhận việc), chia khối/vòng bằng cắt
# lát danh sách, tối ưu bằng quy hoạch động trên tập con (không thử từng cách gán như checklib), và kiểm cận trên của chia động trên mọi
# hoán vị của các danh sách nhỏ.
import itertools


def clock_sim(jobs, cores):
    """Mô phỏng từng đơn vị thời gian: mỗi lúc t, lõi nào rảnh lấy việc đầu hàng (lõi chỉ số nhỏ trước). Trả về (thời gian bận mỗi lõi, C)."""
    queue, busy_until, load, t = list(jobs), [0] * cores, [0] * cores, 0
    while queue:
        for c in range(cores):
            if busy_until[c] <= t and queue:
                j = queue.pop(0); busy_until[c] = t + j; load[c] += j
        t += 1
    return load, max(busy_until)


J = [8, 7, 6, 5, 4, 3, 2, 1]
blocks = [sum(J[:4]), sum(J[4:])]
cyclic = [sum(J[0::2]), sum(J[1::2])]
rec("L04a", blocks == [26, 10] == alg.par_static_blocks(J, 2) and cyclic == [20, 16] == alg.par_static_cyclic(J, 2),
    "chia khối 26 | 10; chia vòng 20 | 16 (cắt lát danh sách)")
la, ca = clock_sim(sorted(J), 2)
lb, cb = clock_sim(sorted(J, reverse=True), 2)
rec("L04b", (la, ca) == ([16, 20], 20) and (lb, cb) == ([18, 18], 18) and alg.par_lpt(J, 2) == lb,
    "mô phỏng đồng hồ: ngắn trước 16 | 20 → 20; dài trước 18 | 18 → 18")


def opt_two(jobs):
    """Tối ưu 2 lõi bằng quy hoạch động tổng con: tổng một lõi có thể đạt."""
    reach = {0}
    for j in jobs:
        reach |= {r + j for r in reach}
    tot = sum(jobs)
    return min(max(r, tot - r) for r in reach)


rec("L04c", opt_two(J) == 18 == alg.par_best_makespan(J, 2) and max(sum(J) / 2, max(J)) == 18,
    "tối ưu 2 lõi (quy hoạch động tổng con) = 18 = cận dưới")
ok = True
for L in ([3, 3, 2, 2, 2], [5, 4, 3, 3, 1], [7, 6, 5, 4, 3]):
    for perm in set(itertools.permutations(L)):
        for n in (2, 3):
            _, c = clock_sim(list(perm), n)
            lo = max(sum(L) / n, max(L))
            ok &= lo <= c <= sum(L) / n + max(L)
rec("L04d", ok, "mọi hoán vị của 3 danh sách nhỏ, 2 và 3 lõi: cận dưới ≤ C ≤ T₁/n + việc dài nhất")
rec("L04e", round(36 / 26, 2) == 1.38 and 36 / 18 == 2 and 18 + 8 == 26 and la[1] - 8 == 12,
    "tăng tốc 1,38 và 2; cận trên 26; ảnh 8 bắt đầu ở giây 12")
B = [30] + [1] * 100
_, cB = clock_sim(sorted(B, reverse=True), 8)
B2 = [10, 10, 10] + [1] * 100
_, cB2 = clock_sim(sorted(B2, reverse=True), 8)
rec("L04f", cB == 30 and cB2 == 17 and round(130 / 30, 2) == 4.33 and round(130 / 17, 2) == 7.65 and round(130 / 8, 2) == 16.25,
    "lỗi 3: việc 30 giây → C = 30 (4,33 lần); tách 3 × 10 → C = 17 (7,65 lần)")
rec("L04g", round(1000 * 0.1 / 1000 * 100) == 10 and round(100 * 0.1 / 1000 * 100) == 1,
    "lỗi 2: 1000 lần lấy việc × 0,1 ms trên 1000 ms = 10%; khúc 10 việc → 100 lần = 1%")
Q = [7, 6, 5, 4, 3, 3, 2, 2]
lq, cq = clock_sim(sorted(Q, reverse=True), 4)
best = min(max(sum(Q[i] for i in range(8) if a[i] == c) for c in range(4)) for a in itertools.product(range(4), repeat=8))
rec("L04h", [sum(Q[0:2]), sum(Q[2:4]), sum(Q[4:6]), sum(Q[6:8])] == [13, 9, 6, 4] and [sum(Q[c::4]) for c in range(4)] == [10, 9, 7, 6]
    and sorted(lq) == [7, 8, 8, 9] and cq == 9 == best and max(32 / 4, 7) == 8 and 25 > 24,
    "quiz: khối 13, vòng 10, dài trước 9 = tối ưu (thử 4⁸ cách); cận dưới 8 không đạt")
rec("L04i", round(32 / 9, 2) == 3.56 and round(32 / 7, 2) == 4.57 and round((9 / 7 - 1) * 100) == 29,
    "quiz: 3,56 lần; 8 lõi 4,57 lần; thêm ≈ 29%")
