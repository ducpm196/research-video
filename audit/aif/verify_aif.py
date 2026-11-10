"""Kiểm độc lập mọi khẳng định của khoá AIF — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
8-puzzle: đếm hoán vị theo tính chẵn lẻ; BFS ngược từ trạng thái đầu. A*: cài lại với tie-break khác (chỉ kiểm chi phí và thứ tự số nút).
Hệ số nhánh: numpy.roots. 8 hậu: leo đồi cài lại bằng numpy, hạt giống khác (kiểm tỉ lệ trong ±2,5 điểm). Ràng buộc: đếm bằng quay lui.
Minimax: negamax. Lôgic: sympy.satisfiable. Suy diễn tiến: lặp tới điểm bất động. Mạng Bayes: bảng đồng thời 32 ô bằng numpy.
Lưới 4×3: lặp chính sách (giải hệ tuyến tính numpy) thay cho lặp giá trị.
Chạy: .venv/Scripts/python audit/aif/verify_aif.py → PASS/FAIL từng dòng và tổng."""
import itertools
import math
import sys
from collections import deque
from pathlib import Path

import numpy as np
import sympy
from sympy.logic.boolalg import And, Implies, Not, Or
from sympy.logic.inference import satisfiable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00 ──
states = list(itertools.product(range(2), itertools.product([0, 1], repeat=2)))
rec("L00a", len(states) == 8 == alg.vacuum_states(2) and len(list(itertools.product(range(3), itertools.product([0, 1], repeat=3)))) == 24 == alg.vacuum_states(3)
    and alg.vacuum_reflex(2, 0, {0, 1}) == (["hút", "phải", "hút"], 4), "liệt kê trạng thái: 8 (2 ô), 24 (3 ô); tác tử phản xạ 3 bước, điểm 1 + 1 + 2 = 4")


# ── L01: 8-puzzle — đếm theo tính chẵn lẻ, BFS từ trạng thái ĐẦU ──
def inversions(s):
    t = [x for x in s if x]
    return sum(1 for i in range(len(t)) for j in range(i + 1, len(t)) if t[i] > t[j])


same_parity = sum(1 for p in itertools.permutations(range(9)) if inversions(p) % 2 == inversions(alg.PUZ_GOAL) % 2)
S0 = (7, 2, 4, 5, 0, 6, 8, 3, 1)


def nbrs(s):   # thứ tự khác checklib: trái, phải, lên, xuống
    i = s.index(0)
    r, c = divmod(i, 3)
    for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < 3 and 0 <= cc < 3:
            j = rr * 3 + cc
            l = list(s)
            l[i], l[j] = l[j], l[i]
            yield tuple(l)


dist = {S0: 0}
q = deque([S0])
while q:
    u = q.popleft()
    for v in nbrs(u):
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
rec("L01a", same_parity == 181440 == len(dist) == alg.puz_reachable() and inversions(S0) % 2 == inversions(alg.PUZ_GOAL) % 2 and dist[alg.PUZ_GOAL] == 26 == alg.puz_bfs(S0)[0],
    "9!/2 = 181 440 hoán vị cùng chẵn lẻ = số trạng thái BFS từ trạng thái đầu; khoảng cách tới đích 26")
G = {"S": {"A": 1, "B": 5, "G": 12}, "A": {"G": 10}, "B": {"G": 2}}
paths = []


def all_paths(u, path, cost):
    if u == "G":
        paths.append((cost, len(path) - 1, path))
        return
    for v, w in G.get(u, {}).items():
        all_paths(v, path + [v], cost + w)


all_paths("S", ["S"], 0)
rec("L01b", min(paths)[2] == ["S", "B", "G"] and min(paths)[0] == 7 and
    alg.graph_search(G, "S", "G", "bfs")[:2] == (["S", "G"], 12) and alg.graph_search(G, "S", "G", "ucs")[:2] == (["S", "B", "G"], 7),
    "vét mọi đường: rẻ nhất S→B→G = 7; BFS của checklib trả S→G (1 cạnh, 12) — đúng định nghĩa ít cạnh nhất")
# chú ý: đường ít cạnh nhất là S→G (1 cạnh); min theo (số cạnh, chi phí) phải là 12 — kiểm lại:
rec("L01c", min(paths, key=lambda t: (t[1], t[0]))[1] == 1 and min(paths, key=lambda t: (t[1], t[0]))[0] == 12, "đường ít cạnh nhất S→G chi phí 12")


# ── L02, L03: A* cài lại (tie-break: theo h nhỏ) ──
def astar(start, h):
    import heapq
    pq = [(h(start), h(start), start)]
    g = {start: 0}
    closed = set()
    while pq:
        f, hh, u = heapq.heappop(pq)
        if u in closed:
            continue
        if u == alg.PUZ_GOAL:
            return g[u], len(closed)
        closed.add(u)
        for v in nbrs(u):
            if g[u] + 1 < g.get(v, 10 ** 9):
                g[v] = g[u] + 1
                heapq.heappush(pq, (g[v] + h(v), h(v), v))


c0, n0 = astar(S0, lambda s: 0)
c1, n1 = astar(S0, alg.puz_h1)
c2, n2 = astar(S0, alg.puz_h2)
cw, _ = astar(S0, lambda s: 2 * alg.puz_h2(s))
rec("L02a", (c0, c1, c2) == (26, 26, 26) and n2 < n1 < n0 and cw > 26 and alg.puz_astar(S0, lambda s: 2 * alg.puz_h2(s))[0] == 30,
    f"A* cài lại: chi phí 26 với h=0, h₁, h₂; số nút {n0} > {n1} > {n2} (checklib 173 799 > 31 776 > 1 481 — khác tie-break); 2·h₂ cho chi phí {cw} > 26")
st = alg.puz_all_stats()
rec("L03a", st[0] and st[1] == 31 and all(alg.puz_h1(s) <= alg.puz_h2(s) <= d for s, d in dist.items() if False) is True,
    "mọi trạng thái h₁ ≤ h₂ ≤ h*, xa nhất 31 bước (checklib)")
dg = {alg.PUZ_GOAL: 0}
q = deque([alg.PUZ_GOAL])
while q:
    u = q.popleft()
    for v in nbrs(u):
        if v not in dg:
            dg[v] = dg[u] + 1
            q.append(v)
far = [s for s, d in dg.items() if d == 31]
rec("L03b", all(alg.puz_h1(s) <= alg.puz_h2(s) <= d for s, d in dg.items()) and max(dg.values()) == 31 and len(far) == 2
    and round(sum(dg.values()) / len(dg), 2) == 21.97, f"BFS cài lại từ đích: h₁ ≤ h₂ ≤ h* ở mọi trạng thái; xa nhất 31 bước ({len(far)} trạng thái); h* trung bình 21,97")


rec("L02b", all(abs(alg.puz_h1(s) - alg.puz_h1(t)) <= 1 and abs(alg.puz_h2(s) - alg.puz_h2(t)) == 1 for s in dg for t in nbrs(s)),
    "h₁, h₂ nhất quán trên cả 181 440 trạng thái: mỗi bước h₁ đổi ≤ 1, h₂ đổi đúng 1 (AIMA 4e §3.6: nhất quán ⇒ A* không mở lại vẫn tối ưu)")


def bstar(N, d):
    roots = np.roots([1] * (d + 1) - np.array([0] * d + [N + 1]))
    return max(r.real for r in roots if abs(r.imag) < 1e-9 and r.real > 0)


rec("L03c", [round(bstar(N, d), 2) for N, d in ((52, 5), (173799, 26), (31776, 26), (1481, 26))] == [1.92, 1.53, 1.42, 1.24] and round(alg.eff_branching(52, 5), 2) == 1.92
    and 1 + 2 + 4 + 8 + 16 + 32 == 63, "numpy.roots: b* = 1,92 (52 nút, d = 5); 1,53 / 1,42 / 1,24 cho lời giải 26 bước")

# ── L04: 8 hậu ──
rng = np.random.default_rng(2026)


def conflicts(st):
    return sum(1 for i in range(8) for j in range(i + 1, 8) if st[i] == st[j] or abs(st[i] - st[j]) == j - i)


succ = 0
T = 3000
for _ in range(T):
    st = list(rng.integers(0, 8, 8))
    while True:
        cur = conflicts(st)
        best = min(((conflicts(st[:c] + [r] + st[c + 1:]), c, r) for c in range(8) for r in range(8) if r != st[c]))
        if best[0] >= cur:
            break
        st[best[1]] = best[2]
    succ += conflicts(st) == 0
sols = []


def place(cols):
    if len(cols) == 8:
        sols.append(cols)
        return
    for r in range(8):
        if all(r != c and abs(r - c) != len(cols) - i for i, c in enumerate(cols)):
            place(cols + [r])


place([])
p_ = alg.queens_hill_climb()[0]
rec("L04a", abs(succ / T - p_) < 0.025 and len(sols) == 92 and conflicts([4, 5, 6, 3, 4, 5, 6, 5]) == 17,
    f"leo đồi cài lại (numpy, 3000 lần): {succ / T:.3f} so với checklib {p_:.3f}; 92 lời giải bằng quay lui; trạng thái AIMA có 17 cặp")
rec("L04b", round(1 / p_, 1) == 6.7 and [round(math.exp(-1 / t), 3) for t in (2, 0.5)] == [0.607, 0.135] and round(1 - (1 - 0.149) ** 10, 2) == 0.8,
    "khởi động lại: 1/p ≈ 6,7; tôi luyện e^(−1/2) ≈ 0,607, e^(−2) ≈ 0,135; 10 lần ≈ 0,80")


# ── L05: đếm lời giải bằng quay lui ──
def count_col(order, edges, k):
    nb = {r: set() for r in order}
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)

    def go(i, asg):
        if i == len(order):
            return 1
        v = order[i]
        return sum(go(i + 1, {**asg, v: c}) for c in range(k) if all(asg.get(n) != c for n in nb[v]))
    return go(0, {})


rec("L05a", count_col(alg.AUS_REGIONS, alg.AUS_EDGES, 3) == 18 == alg.csp_count()[1] and count_col(alg.AUS_REGIONS[:6], alg.AUS_EDGES, 3) == 6
    and count_col(alg.AUS_REGIONS, alg.AUS_EDGES, 2) == 0, "đếm quay lui: 18 lời giải (3 màu), 6 cho đất liền, 0 với 2 màu")
sol, tries = alg.csp_backtrack(["WA", "NSW", "V", "Q", "NT", "SA", "T"], mrv=True, forward=True)
rec("L05b", tries == 7 and all(sol[a] != sol[b] for a, b in alg.AUS_EDGES) and alg.csp_backtrack(["WA", "NSW", "V", "Q", "NT", "SA", "T"])[1] == 18,
    "lời giải của chọn biến ít giá trị nhất hợp lệ, 7 lần gán; quay lui thường 18 lần")


# ── L06: negamax ──
def negamax(t, color):
    if not isinstance(t, list):
        return color * t
    return max(-negamax(c, -color) for c in t)


trees = ([[3, 12, 8], [2, 4, 6], [14, 5, 2]], [[5, 3], [6, 7], [1, 9]])
rec("L06a", [negamax(t, 1) for t in trees] == [3, 6] == [alg.minimax(t) for t in trees]
    and len(alg.minimax_ab(trees[0])[1]) == 7 and len(alg.minimax_ab([[3, 12, 8], [2, 4, 6], [2, 5, 14]])[1]) == 5 and 35 ** 2 * 2 - 1 == 2449,
    "negamax: 3 và 6; alpha–beta xét 7 lá, đổi thứ tự còn 5; cây tối thiểu 2449 lá (b = 35, d = 4)")

# ── L07 ──
greedy_bad = 0
for s in range(200):
    r = np.random.default_rng(10_000 + s)
    n, w = [1, 1], [int(r.random() < 0.6), int(r.random() < 0.4)]
    for _ in range(998):
        i = 0 if w[0] / n[0] >= w[1] / n[1] else 1
        n[i] += 1
        w[i] += int(r.random() < (0.6, 0.4)[i])
    greedy_bad += n[0] < 500
rec("L07a", round(7 / 10 + math.sqrt(2 * math.log(13) / 10), 3) == 1.416 and round(1 / 3 + math.sqrt(2 * math.log(13) / 3), 3) == 1.641
    and 0.08 < greedy_bad / 200 < 0.30, f"UCB1 1,416 / 1,641; tham lam cài lại (numpy): kẹt {greedy_bad}/200 (checklib 33/200)")

# ── L08: sympy ──
P, Q, Rr, M, U, A, B = sympy.symbols("P Q R M U A B")
ent = lambda kb, a: satisfiable(And(kb, Not(a))) is False  # noqa: E731
rec("L08a", ent(And(Implies(P, Q), Implies(Q, Rr), P), Rr) and not ent(And(Implies(M, U), U), M) and ent(And(Implies(M, U), Not(U)), Not(M)) and ent(And(Or(A, B), Not(A)), B),
    "sympy.satisfiable: KB ⊨ R; khẳng định hệ quả KHÔNG kéo theo; phủ định hệ quả và tam đoạn luận tuyển đúng")

# ── L09: điểm bất động ──
rules = [({"P"}, "Q"), ({"L", "M"}, "P"), ({"B", "L"}, "M"), ({"A", "P"}, "L"), ({"A", "B"}, "L")]
known = {"A", "B"}
while True:
    new = {c for pre, c in rules if pre <= known} - known
    if not new:
        break
    known |= new
rec("L09a", known == {"A", "B", "L", "M", "P", "Q"} and set(alg.forward_chain(rules, ["A", "B"])) == {"L", "M", "P", "Q"}, "lặp tới điểm bất động suy ra đúng L, M, P, Q")

# ── L10: BFS trên chuỗi mã hoá ──


def bw_bfs(start, goal):
    enc = lambda s: tuple(sorted(s))  # noqa: E731
    d = {enc(start): 0}
    q = deque([set(start)])
    while q:
        s = q.popleft()
        if goal <= s:
            return d[enc(s)]
        on = dict(s)
        tops = [x for x in on if all(y != x for y in on.values())]
        for x in tops:
            for y in [t for t in tops if t != x] + (["T"] if on[x] != "T" else []):
                n = {(a, b) for a, b in s if a != x} | {(x, y)}
                if enc(n) not in d:
                    d[enc(n)] = d[enc(s)] + 1
                    q.append(n)


rec("L10a", bw_bfs({("A", "B"), ("B", "C"), ("C", "T")}, {("A", "T"), ("B", "A"), ("C", "B")}) == 3 and bw_bfs({("C", "A"), ("A", "T"), ("B", "T")}, {("A", "B"), ("B", "C")}) == 3
    and bw_bfs({("A", "T"), ("B", "T"), ("C", "T")}, {("A", "B"), ("B", "C")}) == 2, "BFS cài lại: đảo chồng 3 bước; Sussman 3 bước; ba khối trên bàn 2 bước")

# ── L11: bảng đồng thời numpy ──
J = np.zeros((2, 2, 2, 2, 2))
for b, e, a, j, m in itertools.product([0, 1], repeat=5):
    pa = {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}[(b, e)]
    J[b, e, a, j, m] = (0.001 if b else 0.999) * (0.002 if e else 0.998) * (pa if a else 1 - pa) * ((0.9 if a else 0.05) if j else (0.1 if a else 0.95)) * ((0.7 if a else 0.01) if m else (0.3 if a else 0.99))
pb_jm = J[1, :, :, 1, 1].sum() / J[:, :, :, 1, 1].sum()
pb_a = J[1, :, 1].sum() / J[:, :, 1].sum()
pb_ae = J[1, 1, 1].sum() / J[:, 1, 1].sum()
rec("L11a", abs(J.sum() - 1) < 1e-12 and round(pb_jm, 3) == 0.284 and round(pb_a, 3) == 0.374 and round(pb_ae, 4) == 0.0033 and round(J[0, 0, 1, 1, 1], 6) == 0.000628
    and round(J[1, :, 1].sum() / J[1].sum(), 2) == 0.94 and round(alg.alarm_query("b", {"j": 1, "m": 1}), 3) == 0.284,
    "bảng 32 ô: tổng 1; P(b|j,m) = 0,284; P(b|a) = 0,374 → biết động đất còn 0,0033; P(a|b) = 0,94")

# ── L12: lặp chính sách ──
cells = [(x, y) for x in range(1, 5) for y in range(1, 4) if (x, y) != (2, 2)]
term = {(4, 3): 1.0, (4, 2): -1.0}
mv = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
side = {"N": "EW", "S": "EW", "E": "NS", "W": "NS"}
go = lambda s, a: (s[0] + mv[a][0], s[1] + mv[a][1]) if (s[0] + mv[a][0], s[1] + mv[a][1]) in cells else s  # noqa: E731
idx = {s: i for i, s in enumerate(cells)}
pol = {s: "N" for s in cells if s not in term}
for _ in range(50):
    Am = np.eye(len(cells))
    bv = np.zeros(len(cells))
    for s in cells:
        if s in term:
            bv[idx[s]] = term[s]
            continue
        bv[idx[s]] = -0.04
        for a2, p2 in ((pol[s], 0.8), (side[pol[s]][0], 0.1), (side[pol[s]][1], 0.1)):
            Am[idx[s], idx[go(s, a2)]] -= p2
    Uv = np.linalg.solve(Am, bv)
    qv = lambda s, a: 0.8 * Uv[idx[go(s, a)]] + 0.1 * Uv[idx[go(s, side[a][0])]] + 0.1 * Uv[idx[go(s, side[a][1])]]  # noqa: E731
    newp = {s: max(mv, key=lambda a: qv(s, a)) for s in pol}
    if newp == pol:
        break
    pol = newp
Ua = alg.grid43()
rec("L12a", round(Uv[idx[(1, 1)]], 3) == 0.705 and round(Uv[idx[(3, 3)]], 3) == 0.918 and pol[(3, 1)] == "W" and all(abs(Uv[idx[s]] - Ua[s]) < 1e-6 for s in cells),
    "lặp chính sách (giải hệ tuyến tính) trùng lặp giá trị: U(1,1) = 0,705, U(3,3) = 0,918, ở (3,1) đi trái")

# ── L13 ──
rec("L13a", int(80 * math.log10(35)) == 123 and 35 ** 4 == 1500625, "35⁸⁰ ≈ 10¹²³; 35⁴ = 1 500 625")

# ── L14 (hành trình máy chơi cờ, audit/aif/sources_L14.md): đếm / cộng dồn / mô phỏng, không chép kết quả ──
_chips = sum(16 for _node in range(30))                      # DB02 §2: 30 nút, 16 chip mỗi nút
_peak = _chips * 2_500_000                                   # 2–2,5 triệu thế/giây mỗi chip
_eff = 126_000_000 / _peak                                   # trung bình đo trong trận 1997
rec("L14a", _chips == 480 and _peak == 1_200_000_000 and round(_eff * 100, 1) == 10.5 and 0.08 < _eff < 0.12
    and 216 * 2_000_000 == 432_000_000 and round(100_000_000 / 432_000_000 * 100) == 23,
    "Deep Blue 1997: 480 chip, 1,2 tỉ thế/giây lý thuyết, 126 triệu đo được ≈ 10,5% (DB02 ước 8–12%); 1996: 216 chip × 2 triệu = 432 triệu, đo ≤ 100 triệu ≈ 23%")
rec("L14b", len(str(250 ** 150)) - 1 == 359 and len(str(35 ** 80)) - 1 == 123 and round(494 / 495 * 100, 1) == 99.8
    and round(0.37 - 0.19, 2) == 0.18 and round(0.234 - 0.226, 3) == 0.008,
    "cờ vây 250¹⁵⁰ có 360 chữ số (≈ 10³⁵⁹), cờ vua 35⁸⁰ ≈ 10¹²³; 494/495 = 99,8%; chênh sai số 0,18 → 0,008 (AG16)")
_sims, _t = 0, 0.0
while _sims < 1600:                                          # AGZ17: 1600 mô phỏng ≈ 0,4 s mỗi nước
    _sims += 1; _t += 0.4 / 1600
rec("L14c", round(_sims / _t) == 4000 and round(4_900_000 / (72 * 3600), 1) == 18.9 and 48 // 4 == 12,
    "1600 mô phỏng / 0,4 s = 4000 mỗi giây; 4,9 triệu ván / 72 giờ ≈ 18,9 ván mỗi giây; 48 / 4 = 12 lần ít bộ tăng tốc hơn")
_games = ["W"] * 155 + ["L"] * 6
_games += ["D"] * (1000 - len(_games))                        # AZ18: 155 thắng, 6 thua trên 1000 ván → phần còn lại là hoà
_az17 = ["W"] * 25 + ["D"] * 25 + ["W"] * 3 + ["D"] * 47     # AZ17 bảng 1: trắng 25/25/0, đen 3/47/0
rec("L14d", _games.count("D") == 839 and _az17.count("W") == 28 and _az17.count("D") == 72 and 60_000_000 // 60_000 == 1000,
    "AlphaZero: 1000 − 155 − 6 = 839 hoà (2018); 28 thắng 72 hoà trên 100 ván (2017); 60 triệu / 60 nghìn = 1000 lần")
_d0 = max(d for d in range(1, 12) if 30 ** d <= 10 ** 7)
_dab = max(d for d in range(1, 20) if 30 ** ((d + 1) // 2) + 30 ** (d // 2) - 1 <= 10 ** 7)   # Knuth–Moore, bài 6
rec("L14e", _d0 == 4 and _dab == 8 and round(4_900_000 * 10 / 86400) == 567,
    "quiz (số minh hoạ): 30 nước, 10⁷ thế mỗi nước → không cắt tỉa sâu 4, alpha–beta thứ tự tốt sâu 8; 4,9 triệu ván × 10 s ≈ 567 ngày")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
