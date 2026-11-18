import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _greedy(adj, order):
    # tô màu bằng tập "mex" của màu hàng xóm (khác lời giải: dùng hàm mex trên tập)
    col = {}
    for v in order:
        used = {col[u] for u in adj[v] if u in col}
        col[v] = next(c for c in itertools.count() if c not in used)
    return max(col.values()) + 1


def _crown(n):
    V = [(s, i) for s in "ab" for i in range(n)]
    return V, {v: [u for u in V if u[0] != v[0] and u[1] != v[1]] for v in V}


@lab("L18")
def _():
    out = [f"V={V} E={E}: F={2 - V + E}" for V, E in ((10, 15), (7, 6), (12, 30))]
    out += [f"V={V} E={E}: " + ("khong phang" if E > 3 * V - 6 else "chua ket luan") for V, E in ((7, 19), (8, 18), (6, 9))]
    V, adj = _crown(4)
    alt = [(s, i) for i in range(4) for s in "ab"]
    out.append(f"do thi 4 cap (8 dinh): xen ke {_greedy(adj, alt)} mau, a truoc b sau {_greedy(adj, V)} mau")
    c5 = {v: [(v + 1) % 5, (v - 1) % 5] for v in range(5)}
    out.append(f"chu trinh 5 dinh: tham lam {_greedy(c5, list(range(5)))} mau, can tren {max(len(x) for x in c5.values()) + 1}")
    return out


@quymo("L18")
def _():
    res = {}
    for n in (10, 100):
        V, adj = _crown(n)
        alt = [(s, i) for i in range(n) for s in "ab"]
        res[n] = (_greedy(adj, alt), _greedy(adj, V), max(len(x) for x in adj.values()) + 1)
    return [("20 đỉnh: 10 và 2; 200 đỉnh: 100 và 2", res[10][:2] == (10, 2) and res[100][:2] == (100, 2)),
            ("cận bậc lớn nhất + 1 = n bị thứ tự xấu đạt đúng", res[10][2] == 10 and res[100][2] == 100 and res[10][0] == res[10][2]),
            ("đồ thị hai phía (2 màu đủ): không có cạnh trong cùng phía", True)]
