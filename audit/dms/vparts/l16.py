import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L16")
def _():
    G = [("G1", [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
         ("G2", [1, 2, 3, 4, 5], list(itertools.combinations(range(1, 6), 2))),
         ("G3", [1, 2, 3, 4, 5, 6], [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]),
         ("G4", [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5)])]
    out = []
    for name, V, E in G:
        deg = {v: 0 for v in V}
        for u, w in E:
            deg[u] += 1
            deg[w] += 1
        odd = sum(1 for d in deg.values() if d % 2)
        # liên thông bằng hợp nhất tập (union-find rút gọn)
        comp = {v: {v} for v in V}
        for u, w in E:
            if comp[u] is not comp[w]:
                m = comp[u] | comp[w]
                for x in m:
                    comp[x] = m
        connected = len({id(c) for c in comp.values()}) == 1
        kl = "chu_trinh" if connected and odd == 0 else "duong_di" if connected and odd == 2 else "khong"
        out.append(f"{name}: bac={','.join(str(deg[v]) for v in V)} tong={sum(deg.values())} canh={len(E)} le={odd} lien_thong={int(connected)} ket_luan={kl}")
    return out


@quymo("L16")
def _():
    f = math.factorial
    return [("tổng bậc K_n = n(n−1), n lẻ → bậc n−1 chẵn", all(n * (n - 1) == 2 * math.comb(n, 2) and (n - 1) % 2 == 0 for n in (11, 101, 1001))),
            ("(n−1)!/2: 1814400; ≈1,2e18 (≈39 năm); 100!/2 có 158 chữ số", f(10) // 2 == 1814400 and round(f(20) / 2 / 1e9 / 31557600) == 39 and len(str(f(100) // 2)) == 158)]
