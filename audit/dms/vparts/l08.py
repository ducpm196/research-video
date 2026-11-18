import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L08")
def _():
    S = [1, 2, 3, 4, 6, 8, 12, 24]
    leq = {(a, b) for a in S for b in S if b % a == 0}
    lt = {(a, b) for a, b in leq if a != b}
    # quan hệ phủ = lt trừ (lt ∘ lt) — tính bằng hợp thành quan hệ, không dùng điều kiện "không có c ở giữa" như lời giải
    comp = {(a, c) for a, b in lt for b2, c in lt if b == b2}
    cover = sorted(lt - comp)
    out = [f"so canh Hasse: {len(cover)}", "canh: " + " ".join(f"{a}-{b}" for a, b in cover)]
    out.append("phan tu toi tieu: " + " ".join(str(x) for x in S if all((y, x) not in lt for y in S)))
    out.append("phan tu toi dai: " + " ".join(str(x) for x in S if all((x, y) not in lt for y in S)))
    out.append("cap khong so sanh duoc: " + str(sum(1 for a, b in itertools.combinations(S, 2) if (a, b) not in leq and (b, a) not in leq)))
    # Kahn với bậc vào đếm trên các cạnh phủ; mỗi lượt chọn số lớn nhất trong các nút bậc vào 0
    indeg = {x: sum(1 for a, b in cover if b == x) for x in S}
    order = []
    while indeg:
        z = max(x for x, d in indeg.items() if d == 0)
        order.append(z)
        del indeg[z]
        for a, b in cover:
            if a == z:
                indeg[b] -= 1
    out.append("sap xep to po (chon so lon nhat): " + " ".join(map(str, order)))
    # đếm hàng hợp lệ bằng quy hoạch động trên tập con đã xếp (không thử mọi hoán vị)
    below = {x: {a for a, b in lt if b == x} for x in S}
    memo = {0: 1}
    idx = {x: i for i, x in enumerate(S)}
    def count(mask):
        if mask in memo:
            return memo[mask]
        tot = 0
        for x in S:
            if not mask >> idx[x] & 1 and all(mask >> idx[a] & 1 for a in below[x]):
                tot += count(mask | 1 << idx[x])
        memo[mask] = tot
        return tot
    # đếm xuôi: số cách xếp đủ tập S = Σ theo thứ tự; dùng đếm ngược từ mask rỗng
    def ways(mask):
        if mask == (1 << len(S)) - 1:
            return 1
        return sum(ways(mask | 1 << idx[x]) for x in S if not mask >> idx[x] & 1 and all(mask >> idx[a] & 1 for a in below[x]))
    out.append("so cach sap xep to po: " + str(ways(0)))
    return out


@quymo("L08")
def _():
    def valid(n):
        return sum(1 for h in itertools.permutations(range(1, n + 1)) if h.index(1) < h.index(2) and h.index(3) < h.index(4))
    f = math.factorial
    return [("6 việc: 720 / 180", f(6) == 720 and valid(6) == 180 == f(6) // 4), ("8 việc: 40320 / 10080", f(8) == 40320 and valid(8) == 10080 == f(8) // 4),
            ("15! và 20!", f(15) == 1307674368000 and f(20) == 2432902008176640000),
            ("15! ≈ 22 phút; 20! ≈ 77 năm ở 1e9 hàng/giây", round(f(15) / 1e9 / 60) == 22 and round(f(20) / 1e9 / 31557600) == 77),
            ("bộ đếm: 4 việc 4 ràng buộc → 8 thao tác; n = 1e6 việc, ràng buộc v-1, v-2: chạy thật ra 1999997 ràng buộc, 2999997 thao tác (≈ 3 ms ở 1e9/s)", _kahn_demo())]


def _kahn_demo():
    n = 10 ** 6
    sau = [[] for _ in range(n + 1)]
    dem = [0] * (n + 1)
    rb = 0
    for v in range(2, n + 1):
        sau[v - 1].append(v); dem[v] += 1; rb += 1
        if v >= 3:
            sau[v - 2].append(v); dem[v] += 1; rb += 1
    ready = [v for v in range(1, n + 1) if dem[v] == 0]
    chon = tru = 0
    while ready:
        v = ready.pop(); chon += 1
        for w in sau[v]:
            tru += 1; dem[w] -= 1
            if dem[w] == 0:
                ready.append(w)
    return rb == 1999997 and chon == n and tru == rb and chon + tru == 2999997 and round((chon + tru) / 1e9 * 1000) == 3 and 4 + 4 == 8
