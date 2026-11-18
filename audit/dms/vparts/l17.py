import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _is_tree(n, edges):
    # n−1 cạnh và không chu trình (kiểm bằng DFS có cha) ⇒ cây; khác lời giải (nhãn nhóm)
    adj = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, stack = {0}, [(0, -1)]
    while stack:
        v, par = stack.pop()
        for w in adj[v]:
            if w == par:
                continue
            if w in seen:
                return False
            seen.add(w)
            stack.append((w, v))
    return len(seen) == n


@lab("L17")
def _():
    G = [("H1", [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]), ("H2", [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6)]),
         ("H3", [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]), ("H4", [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])]
    out = []
    for name, E in G:
        E0 = [(u - 1, v - 1) for u, v in E]
        tree = _is_tree(6, E0)
        # liên thông: đếm thành phần bằng ma trận kề lũy thừa (bao đóng bắc cầu Warshall)
        R = [[i == j or (i, j) in E0 or (j, i) in E0 for j in range(6)] for i in range(6)]
        for k in range(6):
            for i in range(6):
                for j in range(6):
                    R[i][j] = R[i][j] or (R[i][k] and R[k][j])
        conn = all(R[0])
        # chu trình: đồ thị liên thông m ≥ n, hoặc không liên thông mà vẫn có chu trình ⇔ m > n − số thành phần
        comps = len({tuple(r) for r in R})
        cyc = len(E) > 6 - comps
        out.append(f"{name}: n=6 m={len(E)} lien_thong={int(conn)} chu_trinh={int(cyc)} la_cay={int(tree)}")
    out.append("H1: so la = " + str(sum(1 for v in range(6) if sum(v in e for e in [(u - 1, w - 1) for u, w in G[0][1]]) == 1)))
    out.append("H3: so la = " + str(sum(1 for v in range(6) if sum(v in e for e in [(u - 1, w - 1) for u, w in G[2][1]]) == 1)))
    out.append(f"cay co nhan 8 dinh (cong thuc Cayley): {8 ** 6}")
    return out


@quymo("L17")
def _():
    cnt = lambda n: sum(1 for t in itertools.combinations(itertools.combinations(range(n), 2), n - 1) if _is_tree(n, t))
    return [("125 và 16807 cây có nhãn (thử từng tập, kiểm bằng DFS)", [cnt(5), cnt(7)] == [125, 16807]),
            ("số tập cạnh phải thử", [math.comb(math.comb(n, 2), n - 1) for n in (7, 10)] == [54264, 886163135] and 9.1e16 < math.comb(105, 14) < 9.2e16 and 6.4e25 < math.comb(190, 19) < 6.5e25),
            ("thời gian ≈ 3 năm; ≈ 2 tỉ năm; số cây 1,9e15 và 2,6e23", round(math.comb(105, 14) / 1e9 / 31557600) == 3 and round(math.comb(190, 19) / 1e9 / 31557600 / 1e9) == 2 and 1.9e15 < 15 ** 13 < 2e15 and 2.6e23 < 20 ** 18 < 2.7e23)]
