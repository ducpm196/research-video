# IRS L05 — học để xếp hạng: tính lại bằng chuỗi Taylor của e^x và ln (không dùng math.exp/log), bằng phân số, bằng liệt kê mọi
# cặp, và bằng mô phỏng vài bước xuống dốc trên mất mát theo cặp (khác `checks`: hàm alg.irs_*).
from fractions import Fraction as F
import itertools


def exp_t(x, n=120):  # e^x theo chuỗi Taylor (x âm: lấy nghịch đảo để tránh triệt tiêu)
    if x < 0:
        return 1 / exp_t(-x, n)
    s, t = 0.0, 1.0
    for k in range(1, n):
        s += t
        t *= x / k
    return s


def ln_t(y):  # ln y bằng chia đôi trên exp_t
    lo, hi = -20.0, 20.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if exp_t(mid) < y else (lo, mid)
    return lo


pl = lambda o: ln_t(1 + exp_t(-o))
rec("L05a", round(pl(0.5), 3) == 0.474 == round(alg.irs_pair_loss(2, 1.5), 3) and round(pl(-0.5), 3) == 0.974
    and abs(pl(-0.5) - pl(0.5) - 0.5) < 1e-9 and round(exp_t(-0.5), 3) == 0.607 and round(exp_t(0.5), 3) == 1.649,
    "mất mát 0,474 / 0,974, hiệu đúng 0,5 (Taylor + chia đôi)")
rec("L05b", round(1 / (1 + exp_t(-0.5)), 4) == 0.6225 and round(-ln_t(1 / (1 + exp_t(-0.5))), 3) == 0.474
    and round(1 / (1 + exp_t(0.5)), 4) == 0.3775 and round(ln_t(2), 3) == 0.693,
    "đường xác suất: 0,6225 → 0,474; 0,3775 → 0,974; ln 2 = 0,693")
mse = lambda p, t: sum((F(str(a)) - b) ** 2 for a, b in zip(p, t)) / len(t)
rec("L05c", mse([2.4, 2.6], [3, 2]) == F(36, 100) and mse([10, 1], [3, 2]) == 25 and round(25 / 0.36) == 69
    and round(pl(-0.2), 3) == 0.798 and round(pl(9), 4) == 0.0001,
    "hook: sai số 0,36 / 25 (≈ 69 lần); theo cặp 0,798 / 0,0001")


def dcg_list(g):  # cộng từng vị trí, lôgarit cơ số 2 bằng ln_t
    return sum(x / (ln_t(i + 1) / ln_t(2)) for i, x in enumerate(g, 1))


def wrong(g):  # liệt kê mọi cặp
    return sum(1 for i, j in itertools.combinations(range(len(g)), 2) if g[i] < g[j])


I = [3, 2, 1, 0]
d12, d34 = dcg_list(I) - dcg_list([2, 3, 1, 0]), dcg_list(I) - dcg_list([3, 2, 0, 1])
rec("L05d", round(dcg_list(I), 3) == 4.762 and round(d12, 3) == 0.369 and round(d34, 3) == 0.069 and round(d12 / d34, 1) == 5.3
    and wrong([2, 3, 1, 0]) == wrong([3, 2, 0, 1]) == 1 and round(dcg_list([2, 3, 1, 0]), 3) == 4.393 and round(dcg_list([3, 2, 0, 1]), 3) == 4.693,
    "theo danh sách: mất 0,369 ở đầu so với 0,069 ở cuối (≈ 5,3 lần), mỗi bên 1 cặp sai")
X = [2, 3, 1, 1, 1, 1, 1, 1, 1, 0]
Y = [3, 2, 1, 1, 1, 1, 1, 0, 1, 1]
rec("L05e", wrong(X) == 1 == alg.irs_wrong_pairs(X) and wrong(Y) == 2 == alg.irs_wrong_pairs(Y)
    and round(dcg_list(X[:3]), 3) == 4.393 and round(dcg_list(Y[:3]), 3) == 4.762 and len(list(itertools.combinations(range(1000), 2))) == 499500,
    "lỗi 3 / quiz: X 1 cặp sai nhưng 3 dòng đầu 4,393; Y 2 cặp sai, 4,762; 1000 văn bản → 499 500 cặp")
rec("L05f", round(pl(0), 3) == 0.693 and round(pl(2), 3) == 0.127 and round(exp_t(-2), 3) == 0.135 and round(ln_t(3) / ln_t(2), 3) == 1.585
    and pl(10) < 1e-4 and abs(pl(-10) - 10) < 1e-4, "quiz 0,693 → 0,127; giới hạn o = ±10")
# mô phỏng: xuống dốc trên mất mát theo cặp làm hiệu điểm tăng dần (thứ tự được học, không cần đúng điểm)
sa, sb = 1.0, 1.0
for _ in range(50):
    g = -1 / (1 + exp_t(sa - sb))  # đạo hàm theo sa của ln(1 + e^−(sa − sb))
    sa, sb = sa - 0.5 * g, sb + 0.5 * g
rec("L05g", sa > sb and pl(sa - sb) < pl(0), "mô phỏng: 50 bước kéo a lên trên b, mất mát giảm dưới ln 2")
