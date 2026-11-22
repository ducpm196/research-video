"""Nâng cấp AF2 Chặng 9 đợt 1: AIF (15) + DAN (13) + DSC (16) + MLO (15) = 59 bài."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
sys.stdout.reconfigure(encoding="utf-8")

import af2_upgrader as up  # noqa: E402
import common  # noqa: E402

COVERS = {
    "AIF": {
        "L00": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L01": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L02": [(1, 'sym'), (2, 'check'), (3, 'example')],
        "L03": [(1, 'example'), (2, 'pitfalls'), (3, 'check')],
        "L04": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L05": [(1, 'example'), (2, 'example'), (3, 'check')],
        "L06": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L07": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L08": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L09": [(1, 'example'), (2, 'example'), (3, 'check')],
        "L10": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L11": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L12": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L13": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L14": [
            (1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'),
            (2, 'check'),
            (3, 'stage5'), (3, 'practice'),
        ],
    },
    "DAN": {
        "L00": [(1, 'example'), (2, 'sym'), (3, 'hook')],
        "L01": [(1, 'example'), (2, 'intuition'), (3, 'sym')],
        "L02": [(1, 'sym'), (2, 'pitfalls'), (3, 'check')],
        "L03": [(1, 'example'), (2, 'sym'), (3, 'check')],
        "L04": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L05": [(1, 'example'), (2, 'pitfalls'), (3, 'quiz')],
        "L06": [(1, 'sym'), (2, 'check'), (3, 'pitfalls')],
        "L07": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L08": [(1, 'example'), (2, 'sym'), (3, 'pitfalls')],
        "L09": [(1, 'sym'), (2, 'pitfalls'), (3, 'pitfalls')],
        "L10": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L11": [(1, 'example'), (2, 'check'), (3, 'practice')],
        "L12": [(1, 'intuition'), (2, 'check'), (3, 'stage5')],
    },
    "DSC": {
        "L00": [(1, 'sym'), (2, 'hook'), (3, 'example')],
        "L01": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L02": [(1, 'sym'), (2, 'example'), (3, 'check')],
        "L03": [(1, 'sym'), (2, 'example'), (3, 'check')],
        "L04": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L05": [(1, 'example'), (2, 'sym'), (3, 'pitfalls')],
        "L06": [(1, 'example'), (2, 'pitfalls'), (3, 'example')],
        "L07": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L08": [(1, 'sym'), (2, 'example'), (3, 'peeking')],
        "L09": [(1, 'example'), (2, 'sym'), (3, 'pitfalls')],
        "L10": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L11": [(1, 'example'), (2, 'pitfalls'), (3, 'check')],
        "L12": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L13": [(1, 'pitfalls'), (2, 'example'), (3, 'check')],
        "L14": [(1, 'check'), (2, 'sym'), (3, 'example')],
        "L15": [(1, 'intuition'), (2, 'check'), (3, 'stage5')],
    },
    "MLO": {
        "L00": [(1, 'sym'), (2, 'sym'), (3, 'example')],
        "L01": [(1, 'sym'), (2, 'example'), (3, 'check')],
        "L02": [(1, 'example'), (2, 'sym'), (3, 'pitfalls')],
        "L03": [(1, 'example'), (2, 'example'), (3, 'check')],
        "L04": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L05": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L06": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L07": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L08": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
        "L09": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L10": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
        "L11": [(1, 'example'), (2, 'check'), (3, 'practice')],
        "L12": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
        "L13": [(1, 'sym'), (2, 'example'), (3, 'check')],
        "L14": [(1, 'intuition'), (2, 'check'), (3, 'stage4')],
    },
}

DATA = {
    "AIF": [
        ("L00", "Tác tử phản xạ ba ô và đếm không gian trạng thái",
         "Liệt kê mọi trạng thái của phòng 3 ô (vị trí `pos` là `0`, `1` hoặc `2`; độ bẩn 3 ô `dirty_0`, `dirty_1`, `dirty_2` mỗi ô là `0` hoặc `1`). Khởi đầu máy ở ô `0` với trạng thái bụi `[1, 0, 1]`, chạy mô phỏng tác tử phản xạ: hút nếu ô hiện tại bẩn, ngược lại đi sang ô kế tiếp bên phải tới khi cả 3 ô sạch.\n\nĐịnh dạng đầu ra cần in đúng 1 dòng:\n`total_states=<số nguyên> clean=<danh sách> steps=<số bước>`",
         """states = [
    (p, a, b, c)
    for p in (0, 1, 2) for a in (0, 1) for b in (0, 1) for c in (0, 1)
]
pos, clean, steps = 0, [1, 0, 1], 0
while any(clean):
    if clean[pos]:
        clean[pos] = 0
    else:
        pos = (pos + 1) % 3
    steps += 1
print(f"total_states={len(states)} clean={clean} steps={steps}")"""),

        ("L01", "Tìm đường ngắn nhất theo chiều rộng và kiểm đích khi sinh nút",
         "Chạy tìm theo chiều rộng từ đỉnh `S` tới đích `G` trên đồ thị có hướng `{'S':['A','B'], 'A':['C','D'], 'B':['G'], 'C':['G'], 'D':[], 'G':[]}`. Theo đúng quy ước kiểm đích ngay khi sinh nút kề: đếm độ dài đường ngắn nhất (`shortest`), số nút đã lấy ra mở rộng (`expanded`, gồm `S, A, B`), và số nút đã thăm (`visited`).\n\nĐịnh dạng đầu ra:\n`shortest=<số> expanded=<số> visited=<số>`",
         """from collections import deque
g = {
    'S': ['A', 'B'], 'A': ['C', 'D'],
    'B': ['G'], 'C': ['G'], 'D': [], 'G': [],
}
q, seen, expanded, found_d = deque([('S', 0)]), {'S'}, 0, -1
while q and found_d < 0:
    u, d = q.popleft()
    expanded += 1
    for v in g[u]:
        if v not in seen:
            seen.add(v)
            if v == 'G': found_d = d + 1; break
            q.append((v, d + 1))
print(f"shortest={found_d} expanded={expanded} visited={len(seen)}")"""),

        ("L02", "Hàm đánh giá cho A*: đếm ô sai chỗ h1 và khoảng cách Manhattan h2",
         "Với trạng thái trò xếp 8 ô số `[0,6,2,1,3,5,7,4,8]` (đích `[0,1,2,3,4,5,6,7,8]`, chi phí thật tối ưu `h* = 10`), tính `h1` (số ô khác 0 sai vị trí), `h2` (tổng khoảng cách Manhattan), và kiểm tra tính chấp nhận được (`h1 <= h2 <= 10`).\n\nĐịnh dạng đầu ra:\n`h1=<số> h2=<số> admissible=<1 hoặc 0>`",
         """cur = [0, 6, 2, 1, 3, 5, 7, 4, 8]
h1 = sum(1 for i, v in enumerate(cur) if v != 0 and v != i)
h2 = sum(abs(i // 3 - v // 3) + abs(i % 3 - v % 3)
         for i, v in enumerate(cur) if v != 0)
print(f"h1={h1} h2={h2} admissible={int(h1 <= h2 <= 10)}")"""),

        ("L03", "Giải hệ số nhánh hiệu dụng b* với N=100 nút ở độ sâu d=4",
         "Dùng phương pháp chia đôi trên đoạn `[1.0, 5.0]` tìm hệ số nhánh hiệu dụng `b*` thoả `1 + b + b^2 + b^3 + b^4 = 101`.\n\nĐịnh dạng đầu ra:\n`b_star=<4 chữ số thập phân> sum_val=<2 chữ số thập phân>`",
         """lo, hi = 1.0, 5.0
for _ in range(50):
    mid = (lo + hi) / 2.0
    val = sum(mid**k for k in range(5))
    if val < 101.0: lo = mid
    else: hi = mid
print(f"b_star={mid:.4f} sum_val={sum(mid**k for k in range(5)):.2f}")"""),

        ("L04", "Leo đồi dốc nhất trên bàn cờ 4-Hậu (mỗi cột một hậu)",
         "Theo quy ước bài học (`b[c]` là hàng của quân hậu ở cột `c`), cho bàn cờ xuất phát `b0 = [2, 2, 1, 3]` (đếm cặp ăn nhau cùng hàng hoặc cùng đường chéo). Chạy thuật toán leo đồi dốc nhất: ở mỗi vòng, duyệt hết cả `4 × 4` láng giềng dời 1 hậu trong cùng cột để chọn láng giềng có ít xung đột nhất, dừng khi không còn láng giềng nào tốt hơn trạng thái hiện tại.\n\nĐịnh dạng đầu ra:\n`init_conflicts=<số> final_conflicts=<số> final_board=<danh sách>`",
         """def conf(b):
    return sum(
        b[i] == b[j] or abs(b[i] - b[j]) == j - i
        for i in range(4) for j in range(i + 1, 4)
    )
cur = [2, 2, 1, 3]; c0 = conf(cur)
while True:
    best_b, best_c = cur, conf(cur)
    for col in range(4):
        for row in range(4):
            cand = list(cur); cand[col] = row
            if conf(cand) < best_c: best_b, best_c = cand, conf(cand)
    if best_c == conf(cur): break
    cur = best_b
print(f"init_conflicts={c0} final_conflicts={conf(cur)} final_board={cur}")"""),

        ("L05", "Bài toán thoả ràng buộc: tô 3 màu bản đồ 6 vùng liên kết",
         "Cho bản đồ gồm `6` vùng đánh số `0..5` nối theo `8` cạnh kề `[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(4,5),(2,5)]` và dùng `3` màu `{0, 1, 2}`. Đếm tổng số cách tô màu có thể và số lời giải hợp lệ không có hai vùng kề nào trùng màu.\n\nĐịnh dạng đầu ra:\n`total_assign=<số> valid_solutions=<số>`",
         """edges = [(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(4,5),(2,5)]
ok = 0
for mask in range(3**6):
    c = [(mask // (3**i)) % 3 for i in range(6)]
    if all(c[u] != c[v] for u, v in edges): ok += 1
print(f"total_assign={3**6} valid_solutions={ok}")"""),

        ("L06", "Cực đại–cực tiểu và cắt tỉa Alpha–Beta trên cây 3 nhánh",
         "Cho cây 3 nhánh `[[4, 10, 7], [1, 5, 9], [12, 6, 3]]` (gốc bên cực đại `MAX`, tầng lá bên cực tiểu `MIN`). Tính giá trị tối ưu ở gốc và tổng số lá phải xét khi cắt tỉa từ trái sang phải.\n\nĐịnh dạng đầu ra:\n`minimax=<số> leaves_visited=<số>`",
         """tree = [[4, 10, 7], [1, 5, 9], [12, 6, 3]]
visited, best = 0, -999
for ch in tree:
    mn = 999
    for v in ch:
        visited += 1; mn = min(mn, v)
        if mn <= best: break
    best = max(best, mn)
print(f"minimax={best} leaves_visited={visited}")"""),

        ("L07", "Công thức cận trên tin cậy UCB1 cân bằng khai thác và khám phá",
         "Ở bước thứ `N = 16` trong tìm kiếm cây mô phỏng ngẫu nhiên, nước A thắng `9/12` lần còn nước B thắng `2/4` lần. Tính điểm `UCB1 = w/n + căn(2 * ln(N) / n)` cho cả hai nước và chọn nước tiếp theo.\n\nĐịnh dạng đầu ra (2 dòng):\n`ucb_A=<4 chữ số> ucb_B=<4 chữ số>`\n`pick=<A hoặc B>`",
         """import math
ucb = lambda w, n, N: (w / n) + math.sqrt(2.0 * math.log(N) / n)
ua, ub = ucb(9, 12, 16), ucb(2, 4, 16)
print(f"ucb_A={ua:.4f} ucb_B={ub:.4f}")
print(f"pick={'B' if ub > ua else 'A'}")"""),

        ("L08", "Kiểm mô hình lôgic mệnh đề bằng liệt kê chân trị trên ba biến A, B, C",
         "Duyệt đủ 8 cách gán đúng/sai `(1/0)` cho `(A, B, C)`. Đếm số mô hình thoả tri thức `KB = {A kéo theo B, B hoặc C, không C}` và kiểm tra `KB` có kéo theo lôgic `B` không.\n\nĐịnh dạng đầu ra:\n`kb_models=<số> entails_B=<1 hoặc 0>`",
         """models = [
    (a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)
    if ((not a or b) and (b or c) and (not c))
]
entails_b = all(b == 1 for _, b, _ in models)
print(f"kb_models={len(models)} entails_B={int(entails_b)}")"""),

        ("L09", "Suy diễn tiến trên tập luật một kết luận (luật Horn)",
         "Từ sự kiện đầu `{X, Y}` và 5 luật `[({X,Y}->Z), ({X,W}->Z), ({Y,Z}->U), ({Z,U}->W), ({W}->V)]`, chạy suy diễn tiến tới khi không suy thêm được và in thứ tự các mệnh đề mới suy ra.\n\nĐịnh dạng đầu ra:\n`derived=...`",
         """facts, order = {'X', 'Y'}, []
rules = [
    ({'X', 'Y'}, 'Z'), ({'X', 'W'}, 'Z'),
    ({'Y', 'Z'}, 'U'), ({'Z', 'U'}, 'W'), ({'W'}, 'V'),
]
while True:
    added = [c for pre, c in rules if pre <= facts and c not in facts]
    if not added: break
    facts.add(added[0]); order.append(added[0])
print("derived=" + ",".join(order))"""),

        ("L10", "Tìm kế hoạch đảo chồng 3 khối M/P/N về N/M/P trên bàn T",
         "Dùng tìm theo chiều rộng trên không gian trạng thái (ký hiệu `T` là mặt bàn) để tìm kế hoạch ít hành động nhất đảo chồng `M trên P trên N (trên T)` thành `N trên M trên P (trên T)`.\n\nĐịnh dạng đầu ra:\n`init_bottom=<khối đáy đầu> goal_bottom=<khối đáy đích> min_actions=<số bước>`",
         """from collections import deque
s = {'M': 'P', 'P': 'N', 'N': 'T'}; g = {'N': 'M', 'M': 'P', 'P': 'T'}
st0 = tuple(sorted(s.items()))
q, seen, ans = deque([(st0, 0)]), {st0}, 0
while q:
    c, d = dict(q[0][0]), q.popleft()[1]
    if c == g: ans = d; break
    clr = (set(c) - set(c.values())) | {'T'}
    for b in clr - {'T'}:
        for dst in clr - {b}:
            ks = tuple(sorted({**c, b: dst}.items()))
            if ks not in seen: seen.add(ks); q.append((ks, d + 1))
ib = [b for b, u in s.items() if u == 'T'][0]
gb = [b for b, u in g.items() if u == 'T'][0]
print(f"init_bottom={ib} goal_bottom={gb} min_actions={ans}")"""),

        ("L11", "Mạng Bayes cảm biến nhiệt: suy diễn hậu nghiệm P(Nóng | A1, A2)",
         "Cho bảng xác suất gốc mạng cảm biến: `P(Quá_nhiệt=1)=0.01`, `P(Sụt_áp=1)=0.04`; bảng chuông `Báo_động`: `(1,1)->0.98`, `(1,0)->0.90`, `(0,1)->0.25`, `(0,0)->0.005`; hai cảm biến báo tín hiệu `A1` (khi kêu: `0.85` / yên: `0.04`) và `A2` (khi kêu: `0.75` / yên: `0.02`). Tính `P(Quá_nhiệt=1 | A1=1, A2=1)` bằng liệt kê qua biến ẩn.\n\nĐịnh dạng đầu ra:\n`P_heat_given_A12=<4 chữ số thập phân>`",
         """p_h, p_v = 0.01, 0.04
p_a = {(1,1):.98, (1,0):.90, (0,1):.25, (0,0):.005}
a1_t, a2_t = 0.85, 0.75; a1_f, a2_f = 0.04, 0.02
num = den = 0.0
for h in (0, 1):
    for v in (0, 1):
        phv = (p_h if h else 1-p_h) * (p_v if v else 1-p_v)
        pa = p_a[(h, v)]
        pa12 = pa*a1_t*a2_t + (1-pa)*a1_f*a2_f
        den += phv * pa12
        if h: num += phv * pa12
print(f"P_heat_given_A12={num / den:.4f}")"""),

        ("L12", "Lặp giá trị bài toán bất định 3 ô thẳng hàng tới ô đích +1.0",
         "Cho 3 ô `[0, 1, 2]` với ô đích `2` giá trị cố định `+1.0`. Mỗi bước nhận thưởng `r = -0.05`, hệ số chiết khấu `gamma = 0.9`; chọn đi tiến/lùi có xác suất tiến đúng hướng `0.7` và trượt đứng yên `0.3` (lấy `max` theo hai hành động). Chạy `30` vòng lặp giá trị cập nhật `u[0], u[1]`.\n\nĐịnh dạng đầu ra:\n`U0=<3 chữ số> U1=<3 chữ số>`",
         """u = [0.0, 0.0, 1.0]
for _ in range(30):
    act1 = -0.05 + 0.9 * (0.7 * u[2] + 0.3 * u[1])
    act2 = -0.05 + 0.9 * (0.7 * u[0] + 0.3 * u[1])
    u1_new = max(act1, act2)
    u0_new = max(-0.05 + 0.9 * (0.7 * u[1] + 0.3 * u[0]), -0.05 + 0.9 * u[0])
    u[0], u[1] = u0_new, u1_new
print(f"U0={u[0]:.3f} U1={u[1]:.3f}")"""),

        ("L13", "Ước lượng kích thước cây trò chơi b=20 ở độ sâu 60 và độ sâu 3",
         "Trong một trò chơi có trung bình `20` nước đi mỗi lượt, so sánh kích thước cây đầy đủ tới độ sâu `60` với khi chỉ duyệt tối đa tới độ sâu `3`. Tính lôgarit cơ số 10 (`log10`) của tổng số nút lá ở độ sâu 60, số nút lá ở độ sâu 3, và số bậc 10 giảm đi giữa hai trường hợp.\n\nĐịnh dạng đầu ra:\n`log10_tree=<1 chữ số> depth3_nodes=<số nguyên> log10_reduction=<1 chữ số>`",
         """import math
log10_full = 60 * math.log10(20)
d3 = 20 ** 3
log10_red = log10_full - 3 * math.log10(20)
print(
    f"log10_tree={log10_full:.1f} depth3_nodes={d3} "
    f"log10_reduction={log10_red:.1f}"
)"""),

        ("L14", "Hành trình máy chơi cờ 1997–2018: hiệu suất song song và tỉ lệ hoà",
         "Tính lại: (1) hiệu suất song song (%) của máy cờ năm 1997 (`126 000 000` so với lý thuyết `480 * 2 500 000` thế/giây), (2) số mô phỏng mỗi giây trên cờ vây (`1600 / 0.4s`), (3) số ván hoà trong trận `1000` ván (`155` thắng, `6` thua).\n\nĐịnh dạng đầu ra:\n`deepblue_eff=<1 chữ số>% sim_rate=<số nguyên>/s az_draws=<số nguyên>`",
         """theo = 480 * 2_500_000
eff = 126_000_000 / theo * 100.0
sim_s = 1600 / 0.4
draws = 1000 - 155 - 6
print(f"deepblue_eff={eff:.1f}% sim_rate={sim_s:.0f}/s az_draws={draws}")"""),
    ],

    "DAN": [
        ("L00", "Định nghĩa chỉ số chặt: người dùng hoạt động theo đăng nhập và thao tác",
         "Từ nhật ký 8 người dùng `(login, actions)` là `[(1,3), (1,0), (1,2), (1,0), (1,0), (1,5), (1,1), (1,0)]`, đếm số người dùng hoạt động (`active user`) theo hai định nghĩa: `login > 0` và `actions > 0`.\n\nĐịnh dạng đầu ra:\n`active_login=<số> active_action=<số>`",
         """logs = [(1,3), (1,0), (1,2), (1,0), (1,0), (1,5), (1,1), (1,0)]
by_login = sum(1 for l, _ in logs if l > 0)
by_action = sum(1 for _, a in logs if a > 0)
print(f"active_login={by_login} active_action={by_action}")"""),

        ("L01", "Trung bình có trọng số và bẫy trung bình của hai trung bình",
         "Cửa hàng A có `80` đơn trung bình `40` nghìn, cửa hàng B có `20` đơn trung bình `190` nghìn. Tính trung bình gộp sai `(mA + mB)/2` và trung bình gộp đúng có trọng số.\n\nĐịnh dạng đầu ra:\n`naive=<2 chữ số> weighted=<2 chữ số>`",
         """nA, mA, nB, mB = 80, 40.0, 20, 190.0
naive = (mA + mB) / 2.0
weighted = (nA * mA + nB * mB) / (nA + nB)
print(f"naive={naive:.2f} weighted={weighted:.2f}")"""),

        ("L02", "Nối bảng quan hệ một–nhiều (1–N) làm nhân dòng tổng đơn hàng",
         "Dùng thư viện `sqlite3` trong bộ nhớ tạm (RAM), tạo bảng đơn hàng `(1, 120), (2, 80)` và bảng chi tiết dòng hàng `(1),(1),(1),(1),(2)` (quan hệ 1–N). So sánh tổng sai khi nối thẳng với tổng đúng trước khi nối.\n\nĐịnh dạng đầu ra:\n`joined_wrong=<số> true_sum=<số>`",
         """import sqlite3
c = sqlite3.connect(':memory:')
c.executescript('CREATE TABLE o(id INT, amt INT); CREATE TABLE it(oid INT);'
                'INSERT INTO o VALUES(1,120),(2,80);'
                'INSERT INTO it VALUES(1),(1),(1),(1),(2);')
bad = c.execute('SELECT SUM(o.amt) FROM o JOIN it ON o.id=it.oid').fetchone()[0]
good = c.execute('SELECT SUM(amt) FROM o').fetchone()[0]
print(f"joined_wrong={bad} true_sum={good}")"""),

        ("L03", "Hàm cửa sổ trong bảng dữ liệu: tổng lũy kế, chênh lệch và xếp hạng 4 ngày",
         "Dùng thư viện `sqlite3` chạy hàm cửa sổ tính tổng lũy kế (`SUM`), hiệu so với dòng trước (`LAG`) và xếp hạng giảm dần (`RANK`) trên doanh thu 4 ngày `[(1,20), (2,50), (3,30), (4,60)]`.\n\nĐịnh dạng đầu ra (4 dòng, theo ngày d=1..4):\n`d=<ngày> cum=<tổng lũy kế> diff=<chênh hôm trước hoặc None> rk=<hạng>`",
         """import sqlite3
c = sqlite3.connect(':memory:')
c.execute('CREATE TABLE s(d INT, rev INT)')
c.executemany('INSERT INTO s VALUES(?,?)', [(1,20),(2,50),(3,30),(4,60)])
q = ('SELECT d, SUM(rev) OVER (ORDER BY d), '
     'rev-LAG(rev) OVER (ORDER BY d), RANK() OVER (ORDER BY rev DESC) '
     'FROM s ORDER BY d')
for r in c.execute(q).fetchall():
    print(f"d={r[0]} cum={r[1]} diff={r[2]} rk={r[3]}")"""),

        ("L04", "Phân tích giữ chân theo nhóm tháng đăng ký (cohort retention)",
         "Với nhóm tháng 1 cỡ ban đầu `200` người (tháng 1 còn `50`, tháng 2 còn `24`) và nhóm tháng 2 cỡ `160` người (tháng 1 còn `56`), tính các tỉ lệ giữ chân (%) và kiểm tra nhóm T2 có cải thiện so với T1 ở tháng 1 không.\n\nĐịnh dạng đầu ra (2 dòng):\n`c1_m1=<1 chữ số>% c1_m2=<1 chữ số>%`\n`c2_m1=<1 chữ số>% improved=<1 hoặc 0>`",
         """r1_m1, r1_m2 = 50 / 200 * 100, 24 / 200 * 100
r2_m1 = 56 / 160 * 100
print(f"c1_m1={r1_m1:.1f}% c1_m2={r1_m2:.1f}%")
print(f"c2_m1={r2_m1:.1f}% improved={int(r2_m1 > r1_m1)}")"""),

        ("L05", "Phễu chuyển đổi từng bước, toàn phễu và ước lượng cải thiện bước 2",
         "Cho số người qua 4 bước từ `8 000` (`(8000, 3600, 1080, 270)`). Tính tỉ lệ (%) từng bước, toàn phễu, và toàn phễu ước lượng mới nếu bước 2 tăng từ `30%` lên `38%` (giữ nguyên tỉ lệ bước 1 và bước 3).\n\nĐịnh dạng đầu ra:\n`step_pct=<danh sách 3 số> overall=<1 chữ số>% overall_step2_38=<1 chữ số>%`",
         """s = [8000, 3600, 1080, 270]
rates = [round(s[i+1]/s[i]*100, 1) for i in range(3)]
overall = s[-1] / s[0] * 100
proj = (rates[0] / 100) * 0.38 * (rates[2] / 100) * 100
print(f"step_pct={rates} overall={overall:.1f}% overall_step2_38={proj:.1f}%")"""),

        ("L06", "Trung bình trượt 7 ngày khử mùa vụ cuối tuần (+35)",
         "Cho chuỗi 14 ngày `y[d] = 20 + 3*d + (35 nếu d chia 7 dư 5 hoặc 6)`. Tính trung bình trượt 7 ngày và kiểm tra độ dốc sai phân liên tiếp có đều bằng `3.0` không.\n\nĐịnh dạng đầu ra:\n`ma7_diffs=<3 giá trị đầu> constant_slope=<1 hoặc 0>`",
         """y = [20 + 3*d + (35 if d % 7 in (5, 6) else 0) for d in range(14)]
ma7 = [sum(y[i-6:i+1]) / 7.0 for i in range(6, 14)]
diffs = [round(ma7[i+1] - ma7[i], 2) for i in range(len(ma7)-1)]
ok = int(all(x == 3.0 for x in diffs))
print(f"ma7_diffs={diffs[:3]} constant_slope={ok}")"""),

        ("L07", "Dự báo đường cơ sở: sai số tuyệt đối trung bình (MAE) và bẫy chia 0",
         "Cho thực tế `[0, 15, 20, 9]` và dự báo `[3, 14, 18, 12]`. Tính sai số tuyệt đối trung bình (`MAE`) và kiểm tra sai số phần trăm trung bình (`MAPE`) có bị chia cho 0 không.\n\nĐịnh dạng đầu ra:\n`mae=<2 chữ số> mape_undefined=<1 hoặc 0>`",
         """act, pred = [0, 15, 20, 9], [3, 14, 18, 12]
mae = sum(abs(a - p) for a, p in zip(act, pred)) / len(act)
has_zero = any(a == 0 for a in act)
print(f"mae={mae:.2f} mape_undefined={int(has_zero)}")"""),

        ("L08", "Phân bố lệch và quy luật nhóm 20% khách hàng đầu",
         "Từ 10 doanh thu `[800, 300, 150, 90, 80, 70, 50, 30, 20, 10]`, tính trung bình, trung vị và tỉ trọng (%) của 2 khách hàng đứng đầu (nhóm 20% đầu).\n\nĐịnh dạng đầu ra:\n`mean=<1 chữ số> median=<1 chữ số> top20=<1 chữ số>%`",
         """rev = [800, 300, 150, 90, 80, 70, 50, 30, 20, 10]
mean_v = sum(rev) / len(rev)
med_v = (rev[4] + rev[5]) / 2.0
top20_share = sum(rev[:2]) / sum(rev) * 100
print(f"mean={mean_v:.1f} median={med_v:.1f} top20={top20_share:.1f}%")"""),

        ("L09", "Phát hiện bất thường bền vững theo độ lệch tuyệt đối trung vị (MAD)",
         "Trên `[200, 204, 196, 202, 198, 206, 200, 900]` (`n = 8`), tính điểm chuẩn `z` theo độ lệch chuẩn tổng thể (chia `n`) và điểm bền vững theo trung vị cùng `1.4826 * MAD` (độ lệch tuyệt đối trung vị chuẩn hoá).\n\nĐịnh dạng đầu ra:\n`z_classical=<2 chữ số> z_robust=<1 chữ số>`",
         """import math
xs = sorted([200, 204, 196, 202, 198, 206, 200, 900])
mean = sum(xs) / len(xs)
sd_pop = math.sqrt(sum((x - mean)**2 for x in xs) / len(xs))
med = (xs[3] + xs[4]) / 2.0
mad_list = sorted(abs(x - med) for x in xs)
norm_mad = 1.4826 * (mad_list[3] + mad_list[4]) / 2.0
print(f"z_classical={(900-mean)/sd_pop:.2f} z_robust={(900-med)/norm_mad:.1f}")"""),

        ("L10", "Khoảng tin cậy Wilson 95% trên mẫu nhỏ 3/3 và mẫu lớn 120/800",
         "Tính cận dưới và cận trên khoảng tin cậy Wilson 95% (`z = 1.96`, làm tròn 3 chữ số) cho hai sản phẩm `3/3` và `120/800`.\n\nĐịnh dạng đầu ra:\n`A_3_3= (<cận dưới>, <cận trên>) B_120_800= (<cận dưới>, <cận trên>)`",
         """import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    m = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return round(c - m, 3), round(c + m, 3)
print("A_3_3=", wilson(3, 3), "B_120_800=", wilson(120, 800))"""),

        ("L11", "Méo tỉ lệ trục tung cắt ngọn trên biểu đồ cột",
         "So sánh chênh lệch thực (%) giữa `200` và `212` với độ phóng đại trực quan khi vẽ biểu đồ cột bắt đầu đáy trục từ `190` thay vì `0`.\n\nĐịnh dạng đầu ra:\n`real_diff_pct=<1 chữ số>% visual_ratio=<1 chữ số>x`",
         """a, b, base = 200.0, 212.0, 190.0
real_ratio = (b - a) / a * 100
visual_ratio = (b - base) / (a - base)
print(f"real_diff_pct={real_ratio:.1f}% visual_ratio={visual_ratio:.1f}x")"""),

        ("L12", "Toán học thử nghiệm có đối chứng quy mô lớn: chia lệch 98/2 và lặp nhiều phiên bản",
         "Tính hệ số chậm thời gian chạy khi chia nhóm `98/2` so với `50/50`, và xác suất báo nhầm (mỗi phía `alpha = 0.025`) khi thử `4` phiên bản đồng thời và lặp `5` vòng (`20` so sánh).\n\nĐịnh dạng đầu ra:\n`split98_2_slow=<2 chữ số>x fp4=<1 chữ số>% fp20=<1 chữ số>%`",
         """slow = 0.25 / (0.02 * 0.98)
fp4 = (1.0 - (1.0 - 0.025)**4) * 100
fp20 = (1.0 - (1.0 - 0.025)**20) * 100
print(f"split98_2_slow={slow:.2f}x fp4={fp4:.1f}% fp20={fp20:.1f}%")"""),
    ],

    "DSC": [
        ("L00", "Biến gây nhiễu trong dữ liệu quan sát vs phân chia ngẫu nhiên",
         "Trong dữ liệu quan sát ở cửa hàng, nhóm đã xem quảng cáo có `75/120` khách mua hàng, nhóm chưa xem có `30/150` khách mua. Tính hiệu chênh lệch quan sát và gắn cờ cần phân chia ngẫu nhiên (`needs_randomization=1`).\n\nĐịnh dạng đầu ra:\n`obs_diff=<2 chữ số> needs_randomization=1`",
         """seen_n, seen_cnt = 120, 75
unseen_n, unseen_cnt = 150, 30
obs_diff = (seen_cnt / seen_n) - (unseen_cnt / unseen_n)
print(f"obs_diff={obs_diff:.2f} needs_randomization=1")"""),

        ("L01", "Thang đo khoảng vs tỉ lệ: phép chia sai ở độ C so với độ Kelvin",
         "Kiểm chứng phép chia sai `30°C / 15°C = 2.0x` trên thang khoảng so với tỉ lệ đúng khi đổi sang thang Kelvin có số 0 tuyệt đối (`+273.15`).\n\nĐịnh dạng đầu ra:\n`celsius_fake=<1 chữ số>x kelvin_real=<3 chữ số>x`",
         """ratio_c = 30.0 / 15.0
ratio_k = (30.0 + 273.15) / (15.0 + 273.15)
print(f"celsius_fake={ratio_c:.1f}x kelvin_real={ratio_k:.3f}x")"""),

        ("L02", "Khoá trùng hai phía (nhiều–nhiều N–M) làm phình số dòng khi nối bảng",
         "Bảng trái có 3 dòng khoá `'M'` với tiền `(15, 25, 30)`, bảng phải có 2 dòng khoá `'M'` (`'x','y'`). Thực hiện phép nối ghép cặp (tích Đề-các) trên khoá `'M'` rồi đếm số dòng và tổng tiền phình lên.\n\nĐịnh dạng đầu ra:\n`joined_rows=<số> fake_sum=<số>`",
         """left = [('M', 15), ('M', 25), ('M', 30)]
right = [('M', 'x'), ('M', 'y')]
joined = [(l, r) for kl, l in left for kr, r in right if kl == kr]
print(f"joined_rows={len(joined)} fake_sum={sum(x[0] for x in joined)}")"""),

        ("L03", "Điền trung bình làm co giả phương sai mẫu",
         "So sánh phương sai mẫu (chia `n - 1`) của dãy gốc `[10.0, 20.0, 30.0, 40.0]` với dãy khi điền `25.0` vào 2 ô thiếu.\n\nĐịnh dạng đầu ra:\n`orig_var=<3 chữ số> mean_imputed_var=<3 chữ số>`",
         """var = lambda xs: sum((x - sum(xs)/len(xs))**2 for x in xs) / (len(xs) - 1)
orig = [10.0, 20.0, 30.0, 40.0]
imp = orig + [25.0, 25.0]
print(f"orig_var={var(orig):.3f} mean_imputed_var={var(imp):.3f}")"""),

        ("L04", "Trung vị, khoảng tứ phân vị (IQR) và hàng rào Tukey trước ngoại lai",
         "Từ dãy `[2.0, 4.0, 6.0, 8.0, 9.0, 10.0, 12.0, 80.0]` (`n = 8`), sắp xếp rồi tính trung bình, trung vị, hai điểm tứ phân vị `Q1, Q3` (trung vị nửa dưới & nửa trên) và ngưỡng rào trên `Q3 + 1.5 * IQR` (với `IQR = Q3 - Q1`), kiểm `max > rào trên`.\n\nĐịnh dạng đầu ra:\n`mean=<1 chữ số> median=<1 chữ số> fence=<1 chữ số> outlier=<1 hoặc 0>`",
         """xs = sorted([2.0, 4.0, 6.0, 8.0, 9.0, 10.0, 12.0, 80.0])
n = len(xs)
mean_x = sum(xs) / n
med_x = (xs[n // 2 - 1] + xs[n // 2]) / 2.0
lo, hi = xs[:n // 2], xs[n // 2:]
q1 = (lo[len(lo) // 2 - 1] + lo[len(lo) // 2]) / 2.0
q3 = (hi[len(hi) // 2 - 1] + hi[len(hi) // 2]) / 2.0
fence = q3 + 1.5 * (q3 - q1)
print(f"mean={mean_x:.1f} median={med_x:.1f} fence={fence:.1f} outlier={int(max(xs) > fence)}")"""),

        ("L05", "Trung thực trực quan: trục tung cắt ở 80 phóng đại khác biệt",
         "So sánh mức tăng thật (%) giữa `82` và `84` với tỉ lệ chiều cao nhìn thấy trên biểu đồ cột khi cắt đáy trục ở `80`.\n\nĐịnh dạng đầu ra:\n`real_gain=<2 chữ số>% truncated_visual=<1 chữ số>x`",
         """v0, v1, cut = 82.0, 84.0, 80.0
real_pct = (v1 - v0) / v0 * 100
fake_ratio = (v1 - cut) / (v0 - cut)
print(f"real_gain={real_pct:.2f}% truncated_visual={fake_ratio:.1f}x")"""),

        ("L06", "Hệ số tương quan tuyến tính Pearson r đảo dấu chỉ vì một ngoại lai",
         "Tính hệ số tương quan tuyến tính Pearson `r` của 4 điểm thuận chiều `[(1,2), (2,3), (3,5), (4,7)]`, sau đó thêm 1 ngoại lai `(25, -12)` và đo `r` mới.\n\nĐịnh dạng đầu ra:\n`r_clean=<3 chữ số> r_outlier=<3 chữ số>`",
         """import math
def corr(pts):
    mx = sum(x for x, _ in pts)/len(pts); my = sum(y for _, y in pts)/len(pts)
    num = sum((x-mx)*(y-my) for x, y in pts)
    dx = sum((x-mx)**2 for x, _ in pts)
    dy = sum((y-my)**2 for _, y in pts)
    return num / math.sqrt(dx * dy)
base = [(1,2),(2,3),(3,5),(4,7)]
print(f"r_clean={corr(base):.3f} r_outlier={corr(base+[(25,-12)]):.3f}")"""),

        ("L07", "Nghịch lý Simpson: tốt hơn ở từng nhóm nhưng thua khi gộp",
         "Kiểm tỉ lệ thành công phương án A (ca nhẹ `46/50`, ca nặng `140/200`) và B (ca nhẹ `176/200`, ca nặng `32/50`) riêng lẻ rồi so sánh tỉ lệ sau khi gộp tổng.\n\nĐịnh dạng đầu ra:\n`sub_A_wins=<1 hoặc 0> pooled_A=<3 chữ số> pooled_B=<3 chữ số>`",
         """a_sm, b_sm = 46/50, 176/200
a_lg, b_lg = 140/200, 32/50
a_all, b_all = (46+140)/(50+200), (176+32)/(200+50)
won = int(a_sm > b_sm and a_lg > b_lg)
print(f"sub_A_wins={won} pooled_A={a_all:.3f} pooled_B={b_all:.3f}")"""),

        ("L08", "Ước lượng cỡ mẫu thử nghiệm có đối chứng cho mức tăng 8% lên 9%",
         "Tính cỡ mẫu tối thiểu mỗi nhóm theo công thức phân phối chuẩn với trung bình gộp `pb = (p1 + p2)/2`: `(za*căn(2*pb*(1-pb)) + zb*căn(p1*(1-p1)+p2*(1-p2)))^2 / (p2 - p1)^2` làm tròn lên (với `p1=0.08, p2=0.09, za=1.959964, zb=0.841621`).\n\nĐịnh dạng đầu ra:\n`n_per_group=<số nguyên>`",
         """import math
p1, p2 = 0.08, 0.09
pb = (p1 + p2) / 2.0
za, zb = 1.959963984540054, 0.8416212335729143
s1 = za * math.sqrt(2 * pb * (1 - pb))
s2 = zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
n = math.ceil(((s1 + s2) / (p2 - p1)) ** 2)
print(f"n_per_group={n}")"""),

        ("L09", "Câu cá dữ liệu: xác suất báo giả toàn họ (FWER) và hiệu chỉnh Bonferroni",
         "Với `15` lần kiểm định ở mức `0.05` khi không có hiệu ứng thật, tính xác suất ít nhất 1 báo động giả toàn họ (`FWER = 1 - (1 - 0.05)^15`) và kết quả sau khi chia đều ngưỡng theo hiệu chỉnh Bonferroni (`0.05/15`).\n\nĐịnh dạng đầu ra:\n`raw_fwer=<3 chữ số> bonf_alpha=<4 chữ số> fwer_bonf=<3 chữ số>`",
         """fwer = 1.0 - (1.0 - 0.05)**15
alpha_bonf = 0.05 / 15
fwer_bonf = 1.0 - (1.0 - alpha_bonf)**15
print(f"raw_fwer={fwer:.3f} bonf_alpha={alpha_bonf:.4f} fwer_bonf={fwer_bonf:.3f}")"""),

        ("L10", "Rò rỉ dữ liệu: trung bình chuẩn hoá trên tập huấn luyện vs trộn tập kiểm tra",
         "Cho tập huấn luyện `[2.0, 4.0, 6.0]` và tập kiểm tra `[12.0, 12.0]`. Tính trung bình đúng chỉ trên tập huấn luyện và trung bình bị rò rỉ khi trộn cả hai tập.\n\nĐịnh dạng đầu ra:\n`train_mean=<1 chữ số> leaked_mean=<1 chữ số>`",
         """tr, te = [2.0, 4.0, 6.0], [12.0, 12.0]
m_tr = sum(tr) / len(tr)
m_all = sum(tr + te) / len(tr + te)
print(f"train_mean={m_tr:.1f} leaked_mean={m_all:.1f}")"""),

        ("L11", "Tỉ lệ nền 2%: xét nghiệm nhạy 95%, đặc hiệu 90% và giá trị dự đoán dương (PPV)",
         "Trên `10 000` người có tỉ lệ nền bệnh `2%`, xét nghiệm độ nhạy `95%`, độ đặc hiệu `90%`. Đếm số dương thật (`tp`), dương giả (`fp`) và tính giá trị dự đoán dương (`PPV = tp / (tp + fp)`).\n\nĐịnh dạng đầu ra:\n`tp=<1 chữ số> fp=<1 chữ số> ppv=<3 chữ số>`",
         """n, prev, sens, spec = 10000, 0.02, 0.95, 0.90
tp = n * prev * sens
fp = n * (1.0 - prev) * (1.0 - spec)
ppv = tp / (tp + fp)
print(f"tp={tp:.1f} fp={fp:.1f} ppv={ppv:.3f}")"""),

        ("L12", "Đa cộng tuyến: tương quan 0.8 làm phình hệ số phóng đại phương sai (VIF) và sai số chuẩn",
         "Tại tương quan `r = 0.8`, tính hệ số phóng đại phương sai `VIF = 1 / (1 - r^2)` và hệ số phình sai số chuẩn `căn(VIF)`.\n\nĐịnh dạng đầu ra:\n`r=<1 chữ số> VIF=<2 chữ số> se_inflation=<2 chữ số>x`",
         """import math
r = 0.8
vif = 1.0 / (1.0 - r * r)
se_mult = math.sqrt(vif)
print(f"r={r:.1f} VIF={vif:.2f} se_inflation={se_mult:.2f}x")"""),

        ("L13", "Kiểm định k-ẩn danh sau khái quát hoá mã bưu chính & nhóm tuổi",
         "Cho 6 dòng đã khái quát gồm cặp `(3 chữ số đầu mã bưu chính, nhóm tuổi)`: `[('12*','25-34'), ('12*','25-34'), ('12*','25-34'), ('45*','35-44'), ('45*','35-44'), ('90*','55+')]`. Đếm cỡ nhóm nhỏ nhất `min_k` và kiểm tra có đạt `k = 2` ẩn danh không.\n\nĐịnh dạng đầu ra:\n`min_k=<số> is_2_anon=<1 hoặc 0>`",
         """from collections import Counter
rows = [('12*', '25-34'), ('12*', '25-34'), ('12*', '25-34'),
        ('45*', '35-44'), ('45*', '35-44'), ('90*', '55+')]
min_k = min(Counter(rows).values())
print(f"min_k={min_k} is_2_anon={int(min_k >= 2)}")"""),

        ("L14", "Truyền đạt trung thực kết quả: ước lượng điểm kèm khoảng tin cậy 95%",
         "Tính chênh lệch điểm phần trăm (`8.0% -> 9.5%`) và khoảng tin cậy 95% (`+- 1.96 * sai số chuẩn`) với cỡ mẫu `n = 10 000` mỗi nhóm.\n\nĐịnh dạng đầu ra:\n`lift_pp=<1 chữ số> ci95=[<1 chữ số>, <1 chữ số>]`",
         """import math
p1, p2, n = 0.080, 0.095, 10000
d = (p2 - p1) * 100
se = math.sqrt(p1*(1-p1)/n + p2*(1-p2)/n) * 100
print(f"lift_pp={d:.1f} ci95=[{d-1.96*se:.1f}, {d+1.96*se:.1f}]")"""),

        ("L15", "Hành trình cuộc thi dự đoán điểm phim: mốc 10%, cải thiện và độ lạc quan trộn",
         "Tính: (1) mốc cần vượt giảm `10%` từ `0.9525` cắt đúng 4 chữ số thập phân, (2) phần trăm cải thiện khi đạt `0.8567`, (3) độ lạc quan làm tròn 5 chữ số trên thước sai số căn quân phương `căn(0.8558^2 + round(2*800/(2817131/2), 5)) - 0.8558`.\n\nĐịnh dạng đầu ra:\n`goal=<4 chữ số> win_imp=<2 chữ số>% blend_opt=<5 chữ số>`",
         """import math
goal = math.floor(0.9525 * 0.9 * 10000) / 10000
imp = (0.9525 - 0.8567) / 0.9525 * 100
mse_gap = round(2 * 800 / (2_817_131 / 2), 5)
opt = math.sqrt(0.8558**2 + mse_gap) - 0.8558
print(f"goal={goal:.4f} win_imp={imp:.2f}% blend_opt={opt:.5f}")"""),
    ],

    "MLO": [
        ("L00", "Vòng đời học máy sản xuất: tỉ lệ mã mô hình và mã keo bao quanh",
         "Trên một hệ thống học máy gồm `80 000` dòng mã có `4 800` dòng mã huấn luyện mô hình, tính phần trăm mã mô hình so với phần trăm mã keo hạ tầng bao quanh.\n\nĐịnh dạng đầu ra:\n`ml_pct=<1 chữ số>% glue_lines=<số> glue_pct=<1 chữ số>%`",
         """tot, ml = 80_000, 4_800
glue = tot - ml
print(f"ml_pct={ml/tot*100:.1f}% glue_lines={glue} glue_pct={glue/tot*100:.1f}%")"""),

        ("L01", "Tái lập thí nghiệm: cố định hạt giống ngẫu nhiên giữ nguyên tập chia",
         "Dùng hạt giống `7` và `9` trong `random.Random(seed).sample(range(12), 5)` để chứng minh cùng hạt giống luôn chia ra đúng cùng danh sách 5 phần tử còn khác hạt giống thì khác.\n\nĐịnh dạng đầu ra:\n`same_seed=<1 hoặc 0> diff_seed=<1 hoặc 0> s7=<danh sách>`",
         """import random
ids = list(range(12))
s7a = random.Random(7).sample(ids, 5)
s7b = random.Random(7).sample(ids, 5)
s9 = random.Random(9).sample(ids, 5)
print(f"same_seed={int(s7a==s7b)} diff_seed={int(s7a!=s9)} s7={s7a}")"""),

        ("L02", "Phiên bản hoá dữ liệu bằng mã băm nội dung SHA-256 thay vì đặt tên tệp",
         "Đổi đúng 1 nhãn trong chuỗi bản ghi `\"u101,1\\nu102,0\"` thành `\"u101,1\\nu102,1\"` rồi lấy 12 ký tự đầu mã băm SHA-256 để kiểm tra hai phiên bản khác nhau hoàn toàn.\n\nĐịnh dạng đầu ra:\n`h1=<12 ký tự> h2=<12 ký tự> changed=<1 hoặc 0>`",
         """import hashlib
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
v1 = h("u101,1\\nu102,0")
v2 = h("u101,1\\nu102,1")
print(f"h1={v1} h2={v2} changed={int(v1 != v2)}")"""),

        ("L03", "Kiểm thử bất biến hành vi và theo từng lát nhóm thay vì điểm tổng",
         "Viết hàm chấm điểm `pred(s)` trả `1` nếu có `'tot'` ngược lại `0`, kiểm thử bất biến khi thử đủ 3 câu `'Binh is tot'`, `'Chi is tot'`, `'Dung is tot'`, và kiểm ngưỡng `>= 0.80` cho từng nhóm `{'maj': 0.94, 'min': 0.71}`.\n\nĐịnh dạng đầu ra:\n`inv_pass=<1 hoặc 0> min_slice_pass=<1 hoặc 0>`",
         """pred = lambda s: 1 if 'tot' in s else 0
inv_ok = all(pred(f"{n} is tot") == 1 for n in ('Binh', 'Chi', 'Dung'))
slice_acc = {'maj': 0.94, 'min': 0.71}
ok_min = int(min(slice_acc.values()) >= 0.80)
print(f"inv_pass={int(inv_ok)} min_slice_pass={ok_min}")"""),

        ("L04", "Quá khớp tập kiểm định khi thử 150 cấu hình ngẫu nhiên trên 80 mẫu",
         "Mô phỏng tất định bằng `random.Random(7)` cho `150` bộ đoán bừa (đúng `50%` trên `80` mẫu kiểm định) rồi lấy điểm cao nhất trong 150 bộ để thấy sự thổi phồng.\n\nĐịnh dạng đầu ra:\n`true_skill=0.50 best_lucky_val=<2 chữ số>`",
         """import random
rng = random.Random(7)
n_m, n_s = 150, 80
best_val = max(sum(rng.random() < 0.5 for _ in range(n_s)) / n_s
               for _ in range(n_m))
print(f"true_skill=0.50 best_lucky_val={best_val:.2f}")"""),

        ("L05", "Lệch huấn luyện–phục vụ khi không dùng chung công thức chuẩn hoá",
         "Với giá trị đầu vào `x = 80.0` và độ lệch chuẩn `std = 10.0`, tính giá trị chuẩn hoá đúng khi dùng trung bình lúc huấn luyện (`mean_train = 55.0`) so với khi mã phục vụ viết lại nhầm sang trung bình (`mean_serve = 65.0`).\n\nĐịnh dạng đầu ra:\n`z_train=<1 chữ số> z_serve_skew=<1 chữ số>`",
         """x, std = 80.0, 10.0
z_train = (x - 55.0) / std
z_serve = (x - 65.0) / std
print(f"z_train={z_train:.1f} z_serve_skew={z_serve:.1f}")"""),

        ("L06", "Gộp lô phục vụ: đánh đổi độ trễ chờ đợi và thông lượng yêu cầu",
         "Với tốc độ đến `200` yêu cầu mỗi giây (cách nhau `5` mi-li-giây), gộp lô `16` yêu cầu; một yêu cầu đơn xử lý mất `4` mi-li-giây còn cả lô 16 mất `15` mi-li-giây. Tính thời gian chờ tối đa của yêu cầu đầu (`first_wait_ms`), thông lượng chạy đơn và chạy lô.\n\nĐịnh dạng đầu ra:\n`first_wait_ms=<số nguyên> single_rps=<số nguyên> batch_rps=<số nguyên>`",
         """wait_ms = 15 * (1000 / 200)
tp_single = 1000 / 4
tp_batch = 16 * 1000 / 15
print(f"first_wait_ms={wait_ms:.0f} single_rps={tp_single:.0f} batch_rps={tp_batch:.0f}")"""),

        ("L07", "Phát hành chạy bóng: ghi nhật ký độ lệch mà không ảnh hưởng người dùng",
         "Trong chế độ chạy bóng song song, cho dự đoán mô hình cũ `old_p = [0.2, 0.8, 0.6, 0.3, 0.9]` và mới `new_p = [0.3, 0.7, 0.4, 0.3, 0.8]` (ngưỡng `0.5`). Trả kết quả cho người dùng từ bản cũ và ghi nhật ký số yêu cầu lệch nhãn.\n\nĐịnh dạng đầu ra:\n`served=old disagree=<số>/5`",
         """old_p = [0.2, 0.8, 0.6, 0.3, 0.9]
new_p = [0.3, 0.7, 0.4, 0.3, 0.8]
disagree = sum(int((a >= 0.5) != (b >= 0.5)) for a, b in zip(old_p, new_p))
print(f"served=old disagree={disagree}/5")"""),

        ("L08", "Giám sát trôi dữ liệu bằng chỉ số ổn định quần thể (PSI)",
         "Tính chỉ số ổn định quần thể (`PSI = tổng (a_i - e_i) * ln(a_i / e_i)`) khi phân bố 4 nhóm thu nhập từ huấn luyện `exp = [0.20, 0.30, 0.30, 0.20]` dịch sang hiện tại `cur = [0.10, 0.20, 0.35, 0.35]`, và kiểm mức cảnh báo theo dõi (`0.1 <= psi < 0.25`).\n\nĐịnh dạng đầu ra:\n`psi=<3 chữ số> alert_moderate=<1 hoặc 0>`",
         """import math
exp = [0.20, 0.30, 0.30, 0.20]
cur = [0.10, 0.20, 0.35, 0.35]
psi = sum((c - e) * math.log(c / e) for e, c in zip(exp, cur))
print(f"psi={psi:.3f} alert_moderate={int(0.1 <= psi < 0.25)}")"""),

        ("L09", "Vòng phản hồi tự củng cố: hai mục dẫn đầu chiếm dần lượt chọn",
         "Cho 5 mục ban đầu `[2, 2, 2, 2, 2]`. Mô phỏng 8 vòng luôn chỉ hiển thị 2 mục dẫn đầu (`top-2`) và mỗi vòng hai mục này được cộng thêm `+3` lượt bấm. Tính tỉ lệ (%) lượt bấm dồn vào 2 mục đầu.\n\nĐịnh dạng đầu ra:\n`clicks=<danh sách 5 số> top2_share=<1 chữ số>%`",
         """clicks = [2, 2, 2, 2, 2]
for _ in range(8):
    top2 = sorted(range(5), key=lambda i: (-clicks[i], i))[:2]
    for i in top2: clicks[i] += 3
share = sum(sorted(clicks, reverse=True)[:2]) / sum(clicks) * 100
print(f"clicks={clicks} top2_share={share:.1f}%")"""),

        ("L10", "Đo hiệu chuẩn xác suất bằng điểm Brier (trung bình bình phương sai số)",
         "Tính điểm Brier bằng công thức trung bình bình phương hiệu `(p - y)^2` cho 4 dự đoán `probs = [0.85, 0.70, 0.20, 0.40]` và nhãn thật `y = [1, 1, 0, 1]`.\n\nĐịnh dạng đầu ra:\n`brier=<4 chữ số>`",
         """probs = [0.85, 0.70, 0.20, 0.40]
y = [1, 1, 0, 1]
brier = sum((p - t)**2 for p, t in zip(probs, y)) / len(y)
print(f"brier={brier:.4f}")"""),

        ("L11", "Lượng tử hoá đối xứng số nguyên 8 bit và nén bộ nhớ trong (RAM)",
         "Lượng tử hoá giá trị `-0.9` về số nguyên 8 bit đối xứng trên khoảng `[-2, 2]` (giá trị nguyên lớn nhất `q_max = 127`), tính sai số khôi phục và so bộ nhớ trong (RAM) cho mô hình `13 tỉ` tham số giữa `4 byte` và `1 byte`.\n\nĐịnh dạng đầu ra (2 dòng):\n`q=<số nguyên> deq=<4 chữ số> err=<4 chữ số>`\n`fp32_gb=<số nguyên> int8_gb=<số nguyên>`",
         """scale = 2.0 / 127.0
q = round(-0.9 / scale)
deq = q * scale
print(f"q={q} deq={deq:.4f} err={abs(deq - (-0.9)):.4f}")
print(f"fp32_gb={13*4} int8_gb={13*1}")"""),

        ("L12", "Thẻ mô hình và công bằng: điểm chung đẹp che khuất nhóm thiểu số",
         "Khi nhóm đa số có `760/800` dự đoán đúng và nhóm thiểu số có `140/200` dự đoán đúng, tính tỉ lệ chính xác chung (`900/1000`) và độ chính xác từng nhóm.\n\nĐịnh dạng đầu ra:\n`overall=<1 chữ số>% maj=<1 chữ số>% min=<1 chữ số>%`",
         """acc_maj = 760 / 800 * 100
acc_min = 140 / 200 * 100
acc_all = (760 + 140) / 1000 * 100
print(f"overall={acc_all:.1f}% maj={acc_maj:.1f}% min={acc_min:.1f}%")"""),

        ("L13", "Tấn công đầu độc cửa sau: điểm tập sạch che khuất mẫu gắn dấu hiệu lệch",
         "Khi mô hình đạt `388/400` đúng trên tập sạch nhưng bị kích hoạt đổi nhãn `17/20` mẫu có gắn dấu hiệu kích hoạt cửa sau, tính tỉ lệ chính xác sạch và tỉ lệ cướp nhãn (%).\n\nĐịnh dạng đầu ra:\n`clean_acc=<1 chữ số>% trigger_hijack=<1 chữ số>%`",
         """clean_acc = 388 / 400 * 100
backdoor_flip = 17 / 20 * 100
print(f"clean_acc={clean_acc:.1f}% trigger_hijack={backdoor_flip:.1f}%")"""),

        ("L14", "Hành trình hạ tầng học máy: độ trễ ở phân vị 99,9% và tổ hợp cấu hình triển khai",
         "Với số minh hoạ cho đội học máy: độ trễ ở phân vị `99,9%` giảm từ `2000` mi-li-giây xuống `200` mi-li-giây; có `4 * 3 * 2` tổ hợp cấu hình triển khai; và `6 000` trên `120 000` dòng mã dành cho thuật toán học máy. Tính hệ số tăng tốc, số cấu hình và tỉ lệ mã học máy (%).\n\nĐịnh dạng đầu ra:\n`p999_speedup=<số nguyên>x configs=<số nguyên> ml_code=<1 chữ số>%`",
         """speedup = 2000 / 200
configs = 4 * 3 * 2
ml_share = 6000 / 120000 * 100
print(f"p999_speedup={speedup:.0f}x configs={configs} ml_code={ml_share:.1f}%")"""),
    ],
}

def main():
    only = {x.strip().upper() for x in sys.argv[1:] if x.strip()}
    for course, labs in DATA.items():
        if only and course not in only:
            print(f"=== {course}: SKIPPED (argv filter) ===", flush=True)
            continue
        for lid, hint, de_body, sol in labs:
            de_md = f"# Lab {course} {lid} — {hint}\n\n{de_body}\n\nChấm tự động:\n```bash\nbash labs/cham.sh {course} {lid} duong_dan/bai_cua_ban.py\n```\n"
            common.upgrade_lesson(
                course, lid, hint, de_md, sol,
                add_code_if_missing=True,
                covers=COVERS[course][lid],
                force_code=True,
            )
        led_p, nblk = up.sync_course_ledger(course, default_lang="python")
        for lid, _, _, sol in labs:
            common.sync_practice_run_blocks(course, lid, sol)
        print(f"=== {course}: {len(labs)} bài OK, ledger={nblk} blocks ===", flush=True)

    PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
    for c in DATA:
        if only and c not in only:
            continue
        for cmd in (
            [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
            [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
            [PY, "-B", "audit/review/lab_gate.py", c],
        ):
            r = subprocess.run(cmd, cwd=ROOT)
            assert r.returncode == 0, f"failed: {cmd}"
    print("ALL S9 BATCH-1 (AIF/DAN/DSC/MLO = 59 LESSONS) PASSED!", flush=True)


if __name__ == "__main__":
    main()
