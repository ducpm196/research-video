# PAR L02 — tính lại bằng cách KHÁC checks của bài: dựng đồ thị phép tính thật (mỗi nút một phép cộng, cạnh = phải chờ), đếm nút và
# đường dài nhất bằng duyệt đồ thị; xếp lịch bằng mô phỏng hàng đợi “phép đã sẵn sàng” (tham lam thật, không theo công thức từng tầng);
# vét hết mọi cách xếp cho cây nhỏ để thấy lịch tham lam đạt cận dưới.
import itertools
from fractions import Fraction as F


def tree_dag(n):
    """Đồ thị cộng theo cặp: trả về {nút: (con trái, con phải)}; lá là ('x', i)."""
    level, dag, k = [("x", i) for i in range(n)], {}, 0
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            node = ("+", k); k += 1
            dag[node] = (level[i], level[i + 1]); nxt.append(node)
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return dag


def chain_dag(n):
    dag, prev = {}, ("x", 0)
    for i in range(1, n):
        node = ("+", i); dag[node] = (prev, ("x", i)); prev = node
    return dag


def depth(dag):
    memo = {}

    def d(v):
        if v not in dag:
            return 0
        if v not in memo:
            memo[v] = 1 + max(d(c) for c in dag[v])
        return memo[v]
    return max(d(v) for v in dag)


def greedy_ready(dag, procs):
    """Mô phỏng: mỗi bước lấy tối đa `procs` phép mà hai đầu vào đã có (ưu tiên phép sẵn sàng sớm nhất)."""
    done, steps = set(), 0
    while len(done) < len(dag):
        ready = [v for v in dag if v not in done and all(c not in dag or c in done for c in dag[v])]
        done |= set(ready[:procs]); steps += 1
    return steps


d1024 = tree_dag(1024)
rec("L02a", len(d1024) == 1023 and depth(d1024) == 10 and alg.par_tree_sum(1024)[:2] == (1023, 10),
    "đồ thị cộng theo cặp 1024 số: 1023 nút, đường dài nhất 10 (khớp checklib)")
rec("L02b", greedy_ready(d1024, 32) == 36 == alg.par_greedy_tree_steps(1024, 32),
    "tham lam theo hàng đợi phép sẵn sàng, 32 lõi: 36 bước (khớp lịch theo tầng)")
c1024 = chain_dag(1024)
rec("L02c", len(c1024) == 1023 and depth(c1024) == 1023 and greedy_ready(c1024, 32) == 1023,
    "cộng dồn: 1023 phép, đường găng 1023, 32 lõi vẫn 1023 bước (lỗi 1)")
T1, Ti, n = F(1023), F(10), 32
rec("L02d", max(T1 / n, Ti) <= 36 <= Ti + (T1 - Ti) / n <= T1 / n + Ti and round(float(Ti + (T1 - Ti) / n), 2) == 41.66
    and round(float(T1 / n + Ti), 2) == 41.97 and round(float(T1 / n), 2) == 31.97 and round(float(T1 / Ti), 1) == 102.3,
    "cận dưới 31,97 ≤ 36 ≤ 41,66 (Brent) ≤ 41,97 (dạng gọn); độ song song 102,3 (phân số chính xác)")
# cây 8 số, 2 lõi: vét mọi cách gán phép vào bước (mỗi bước ≤ 2 phép, đúng thứ tự phụ thuộc) → ít nhất 4 bước
d8 = tree_dag(8)
nodes = list(d8)
best = None
for assign in itertools.product(range(1, 6), repeat=len(nodes)):
    a = dict(zip(nodes, assign))
    if any(sum(1 for v in nodes if a[v] == s) > 2 for s in range(1, 6)):
        continue
    if all(a[v] > a[c] for v in nodes for c in d8[v] if c in d8):
        best = max(assign) if best is None else min(best, max(assign))
rec("L02e", best == 4 == greedy_ready(d8, 2) and depth(d8) == 3 and len(d8) == 7,
    "cây 8 số, 2 lõi: vét hết mọi lịch, tốt nhất 4 bước = tham lam; T₁ = 7, T∞ = 3")
rec("L02f", greedy_ready(d1024, 1024) == 10 and round(1023 / (10 * 1024) * 100) == 10 and round(36 / 10, 1) == 3.6,
    "1024 lõi: 10 bước, nhanh hơn 32 lõi 3,6 lần, mỗi lõi bận ≈ 10%")
d4096 = tree_dag(4096)
g16, g64 = greedy_ready(d4096, 16), greedy_ready(d4096, 64)
rec("L02g", (len(d4096), depth(d4096), g16, g64) == (4095, 12, 259, 69) and round(4095 / g16, 1) == 15.8
    and round(4095 / g64, 1) == 59.3 and round(g16 / g64, 2) == 3.75 and round(12 + 4083 / 16, 1) == 267.2
    and round(12 + 4083 / 64, 1) == 75.8 and round(4095 / 12, 1) == 341.2 and round(4095 / g64 / 64 * 100) == 93,
    "quiz 4096 số: 259 và 69 bước, 15,8 và 59,3 lần, tỉ 3,75; cận 267,2 và 75,8; độ song song 341,2")
total = 0
vals = list(range(1, 1025))
while len(vals) > 1:
    vals = [vals[i] + vals[i + 1] for i in range(0, len(vals), 2)]
rec("L02h", vals[0] == 524800 == sum(range(1, 1025)) and round(1023 / 46, 1) == 22.2 and round(1023 / 36 / 32 * 100) == 89,
    "tổng theo cây 524 800; lỗi 4: 46 bước ≈ 22,2 lần; lõi bận 89%")
