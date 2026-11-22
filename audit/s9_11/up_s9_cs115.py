"""Nâng cấp AF2/AF4 cho 22 bài Chặng 9 của CS115 (L22..L43) — bảo toàn nguyên vẹn L00..L21, L44..L46 đã khoá."""
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
import lv  # noqa: E402

LOCKED_LIDS = {f"L{i:02d}" for i in range(22)} | {"L44", "L45", "L46"}
LOCKED_DIGESTS = {}
for lid in sorted(LOCKED_LIDS):
    fp = up._lesson_path("CS115", lid)
    LOCKED_DIGESTS[lid] = lv.spec_digest(lv.load_spec(fp))

COVERS = {
    "L22": [(1, "example"), (2, "rule"), (2, "example"), (3, "gates"), (4, "neuron"), (5, "verify"), (5, "vector")],
    "L23": [(1, "hook"), (1, "mlp"), (1, "xor_pic"), (2, "why_nonlinear"), (3, "activations"), (4, "init"), (5, "batchnorm"), (5, "hyper")],
    "L24": [(1, "geometry"), (1, "sym_lagrange"), (2, "categorical"), (2, "verify"), (3, "categorical"), (3, "practice"), (4, "kkt"), (5, "when")],
    "L25": [(1, "sym_margin"), (1, "margin_pic"), (2, "optimization"), (3, "hinge"), (4, "kernel"), (5, "valid_kernel")],
    "L26": [(1, "hook"), (1, "shadow_pic"), (2, "hand_J"), (3, "solution"), (4, "vs_pca"), (5, "multi")],
    "L27": [(1, "l1_vs_l2"), (2, "example"), (3, "algorithm"), (4, "choose_k"), (5, "scaling")],
    "L28": [(1, "hook"), (1, "tree"), (2, "gain"), (2, "gain_hand"), (3, "gain_hand"), (3, "verify"), (4, "pitfalls"), (5, "forest")],
    "L29": [(1, "kmeans"), (2, "kmeans"), (3, "local_min"), (4, "hierarchical"), (5, "spectral")],
    "L30": [(1, "model"), (2, "e_step"), (2, "em_hand"), (3, "m_step"), (4, "iterate"), (5, "singular")],
    "L31": [(1, "sym_nmf"), (1, "parts_pic"), (2, "vs_svd"), (3, "updates"), (3, "run"), (4, "pitfalls")],
    "L32": [(1, "hook"), (2, "p_hand"), (3, "perplexity"), (4, "tail_pic"), (4, "kl"), (5, "reading")],
    "L33": [(1, "questions"), (2, "table"), (3, "symbols"), (4, "apply")],
    "L34": [(1, "hand_conv"), (2, "size"), (3, "sharing"), (4, "linear"), (5, "sharing")],
    "L35": [(1, "unroll_pic"), (2, "example"), (3, "bptt"), (4, "lstm")],
    "L36": [(1, "hook"), (2, "reweight"), (3, "gradboost"), (4, "verify")],
    "L37": [(1, "sym_ae"), (1, "bottleneck_pic"), (2, "linear_pca"), (3, "nonlinear"), (4, "tradeoff")],
    "L38": [(1, "hook"), (2, "prereq"), (3, "algorithm"), (3, "example"), (4, "gaussian")],
    "L39": [(1, "hook"), (2, "bellman"), (2, "verify"), (3, "bellman"), (3, "verify"), (4, "qlearning")],
    "L40": [(1, "hook"), (2, "hand_w"), (3, "loss"), (4, "compare")],
    "L41": [(1, "hook"), (2, "example"), (3, "sqrt_d"), (4, "order")],
    "L42": [(1, "hook"), (2, "elbo_hand"), (3, "reparam"), (4, "gan")],
    "L43": [(1, "hook"), (2, "closed"), (3, "schedule"), (4, "reverse")],
}

LABS = [
    ("L22", "Lan truyền ngược đồ thị f=(x+y)*z & kiểm tra đạo hàm bước nhỏ",
     "Tính `f = (x + y) * z` tại `(x=-3, y=7, z=-5)`, tính các đạo hàm riêng giải tích `dx, dy, dz` (với nút trung gian `q = x + y`) rồi đối chiếu `dx` với sai phân trung tâm bước `h = 1e-5`.\n\nĐịnh dạng đầu ra (3 dòng):\n`f=<1 chữ số> dx=<1 chữ số> dy=<1 chữ số> dz=<1 chữ số>`\n`dx=<1 chữ số> num_x=<6 chữ số>`\n`diff=<dạng e, ví dụ 0.00e+00>`",
     """x, y, z = -3.0, 7.0, -5.0
q = x + y
f = q * z
dx, dy, dz = z, z, q
h = 1e-5
num_x = (((x + h) + y) * z - ((x - h) + y) * z) / (2 * h)
print(f"f={f:.1f} dx={dx:.1f} dy={dy:.1f} dz={dz:.1f}")
print(f"dx={dx:.1f} num_x={num_x:.6f}")
print(f"diff={abs(dx - num_x):.2e}")"""),

    ("L23", "MLP: hàm ReLU chuẩn, bão hoà Sigmoid và chuẩn khởi tạo Xavier",
     "Tính đạo hàm `sigmoid(10)*(1-sigmoid(10))`, áp dụng **hàm ReLU chuẩn** `max(0.0, v)` lên dãy `(-3, 0, 4)`, và tính độ lệch chuẩn khởi tạo Xavier `sqrt(2/(n_vao + n_ra))` với `n_vao = 64` (số đầu vào) và `n_ra = 16` (số đầu ra).\n\nĐịnh dạng đầu ra (3 dòng):\n`dsigmoid_10=<6 chữ số dạng e>`\n`relu=<danh sách 3 số>`\n`xavier_std=<4 chữ số>`",
     """import math
sig = lambda t: 1.0 / (1.0 + math.exp(-t))
ds = sig(10.0) * (1.0 - sig(10.0))
relus = [max(0.0, v) for v in (-3.0, 0.0, 4.0)]
xav = math.sqrt(2.0 / (64 + 16))
print(f"dsigmoid_10={ds:.6e}")
print(f"relu={relus}")
print(f"xavier_std={xav:.4f}")"""),

    ("L24", "Lagrange cho ước lượng hợp lý cực đại (MLE) phân phối phân loại tổng = 1",
     "Với số đếm `[6, 3, 1]`, thiết lập hàm Lagrange dưới ràng buộc đẳng thức tổng xác suất `sum(p) == 1` để tìm phân phối cực đại hàm hợp lý, rồi kiểm hệ số Lagrange `c_k / p_k = lambda` tại mọi lớp (danh sách `lambda` làm tròn 1 chữ số bằng `round(x, 1)`).\n\nĐịnh dạng đầu ra (3 dòng):\n`p=<danh sách 3 số> sum=<1 chữ số>`\n`lambda=<danh sách 3 số làm tròn 1 chữ số>`\n`lagrange_equal=<0 hoặc 1>`",
     """counts = [6, 3, 1]
tot = sum(counts)
p = [c / tot for c in counts]
lam = [c / pk for c, pk in zip(counts, p)]
print(f"p={p} sum={sum(p):.1f}")
print(f"lambda={[round(x, 1) for x in lam]}")
print(f"lagrange_equal={int(len(set(round(x, 6) for x in lam)) == 1)}")"""),

    ("L25", "SVM lề lớn nhất 2/||w|| và hàm mất mát bản lề (hinge loss)",
     "Với `w = (6, 8), b = -1` và điểm `(1, 1)` mang nhãn `y = -1`, tính độ dài vector trọng số `||w||`, lề hình học `2/||w||`, tích `y*(w·x + b)` và `hinge = max(0, 1 - y*(w·x + b))`.\n\nĐịnh dạng đầu ra (2 dòng):\n`norm_w=<1 chữ số> margin=<2 chữ số>`\n`y_pred_margin=<1 chữ số> hinge=<1 chữ số>`",
     """import math
w = (6.0, 8.0)
b = -1.0
nw = math.hypot(*w)
margin = 2.0 / nw
score = w[0] * 1 + w[1] * 1 + b
hinge = max(0.0, 1.0 - (-1.0) * score)
print(f"norm_w={nw:.1f} margin={margin:.2f}")
print(f"y_pred_margin={-score:.1f} hinge={hinge:.1f}")"""),

    ("L26", "LDA tiêu chí Fisher: tỉ số độ lệch giữa lớp / tổng bình phương trong lớp",
     "Cho hai lớp `c1 = [1, 2, 3]` và `c2 = [5, 6, 7]`. Tính tiêu chí Fisher `J = (m1 - m2)^2 / (s1^2 + s2^2)` trong đó `s_k^2 = sum((x - m_k)^2)` (tổng bình phương độ lệch chưa chia `n`), cùng số chiều tối đa `C - 1` cho bài toán 3 lớp.\n\nĐịnh dạng đầu ra (2 dòng):\n`m1=<1 chữ số> m2=<1 chữ số> J=<2 chữ số>`\n`max_dims_3class=<số nguyên>`",
     """c1 = [1.0, 2.0, 3.0]
c2 = [5.0, 6.0, 7.0]
m1 = sum(c1) / len(c1)
m2 = sum(c2) / len(c2)
s1 = sum((x - m1) ** 2 for x in c1)
s2 = sum((x - m2) ** 2 for x in c2)
j = (m1 - m2) ** 2 / (s1 + s2)
print(f"m1={m1:.1f} m2={m2:.1f} J={j:.2f}")
print(f"max_dims_3class={3 - 1}")"""),

    ("L27", "KNN: chuẩn hoá thang đo tránh biến lớn lấn át khoảng cách L2",
     "Cho `A = (20, 2000)`, `B = (50, 2000)` và điểm hỏi `Q = (20, 3000)`: tính khoảng cách Euclid `L2` giữa `Q` tới `A`, `B` trước và sau khi chia mỗi chiều cho thang `(40, 1000)`.\n\nĐịnh dạng đầu ra (2 dòng):\n`raw_dQA=<1 chữ số> raw_dQB=<2 chữ số>`\n`norm_dQA=<3 chữ số> norm_dQB=<3 chữ số>`",
     """import math
dist = lambda u, v: math.hypot(u[0] - v[0], u[1] - v[1])
A, B, Q = (20, 2000), (50, 2000), (20, 3000)
scale = lambda p: (p[0] / 40.0, p[1] / 1000.0)
print(f"raw_dQA={dist(Q, A):.1f} raw_dQB={dist(Q, B):.2f}")
print(f"norm_dQA={dist(scale(Q), scale(A)):.3f} norm_dQB={dist(scale(Q), scale(B)):.3f}")"""),

    ("L28", "Cây quyết định: Entropy (dùng lôgarit tự nhiên ln), Gini và Độ lợi thông tin",
     "Nút gốc gồm `(5 dương, 5 âm)` được chia 1 nút thành nhánh trái `(4, 1)` và phải `(1, 4)`. Dùng công thức **lôgarit tự nhiên `ln`** (`math.log`, khớp với bài giảng) để tính `H_root`, `H_split`, độ lợi thông tin `info_gain = H_root - H_split` và chỉ số `Gini` tại gốc.\n\nĐịnh dạng đầu ra (2 dòng):\n`H_root=<3 chữ số> H_split=<4 chữ số>`\n`info_gain=<4 chữ số> gini_root=<2 chữ số>`",
     """import math
ent = lambda a, b: -sum((x / (a + b)) * math.log(x / (a + b)) for x in (a, b) if x > 0)
gini = lambda a, b: 1.0 - (a / (a + b)) ** 2 - (b / (a + b)) ** 2
h0 = ent(5, 5)
h_after = 0.5 * ent(4, 1) + 0.5 * ent(1, 4)
ig = h0 - h_after
print(f"H_root={h0:.3f} H_split={h_after:.4f}")
print(f"info_gain={ig:.4f} gini_root={gini(5, 5):.2f}")"""),

    ("L29", "K-Means: cập nhật tâm bằng trung bình và đo độ tản inertia",
     "Với dãy `X = [1, 2, 8, 10]` và hai tâm khởi tạo `(1, 8)`, chạy 2 bước gán cụm (gần tâm đầu hơn nếu bằng nhau) -> cập nhật tâm, rồi tính `centers` và `inertia` cuối.\n\nĐịnh dạng đầu ra (1 dòng):\n`centers=<danh sách 2 số> inertia=<2 chữ số>`",
     """pts = [1.0, 2.0, 8.0, 10.0]
c = [1.0, 8.0]
for _ in range(2):
    g = [[], []]
    for x in pts:
        g[0 if abs(x - c[0]) <= abs(x - c[1]) else 1].append(x)
    c = [sum(k) / len(k) for k in g]
inertia = sum(min((x - ci) ** 2 for ci in c) for x in pts)
print(f"centers={c} inertia={inertia:.2f}")"""),

    ("L30", "GMM & EM: tính độ thuộc về r_ik (bước E) và cập nhật trung bình (bước M)",
     "Cho hai thành phần chuẩn `N(0, 1)` và `N(4, 1)` có trọng số bằng nhau `0.5`: (1) thực hiện **bước E** tính **độ thuộc về** `r1`, `r2` tại điểm `x = 1.0`; (2) trên bộ 2 điểm `x_list = [1.0, 3.0]` (giả sử tại `3.0` đối xứng có `r1_b = 1 - r1`), thực hiện **bước M** cập nhật trung bình mới `mu1_new = (r1*1.0 + r1_b*3.0) / (r1 + r1_b)`.\n\nĐịnh dạng đầu ra (2 dòng):\n`r1=<6 chữ số> r2=<6 chữ số>`\n`sum=<1 chữ số> mu1_new=<4 chữ số>`",
     """import math
phi = lambda x, m: math.exp(-0.5 * (x - m) ** 2) / math.sqrt(2 * math.pi)
w1, w2 = 0.5 * phi(1.0, 0.0), 0.5 * phi(1.0, 4.0)
r1 = w1 / (w1 + w2)
r2 = 1.0 - r1
r1_b = 1.0 - r1
mu1_new = (r1 * 1.0 + r1_b * 3.0) / (r1 + r1_b)
print(f"r1={r1:.6f} r2={r2:.6f}")
print(f"sum={r1 + r2:.1f} mu1_new={mu1_new:.4f}")"""),

    ("L31", "NMF X ≈ A nhân B: quy tắc nhân giữ mọi phần tử không âm A >= 0, B >= 0",
     "Theo đúng ký hiệu `X ≈ A·B` trong bài: cho vector cột `X_col = [4.0, 3.0]`, ma trận `A = [[2.0, 1.0], [1.0, 2.0]]` và vector hệ số khởi tạo `B = [1.0, 1.0]`. Thực hiện 2 bước cập nhật nhân `B <- B * (A^T X_col) / (A^T A B)` để thấy tổng bình phương sai lệch tái tạo `err = sum((X_col[r] - rec[r])^2)` trên 2 phần tử giảm dần qua từng bước mà mọi hệ số vẫn không âm.\n\nĐịnh dạng đầu ra (2 dòng):\n`step1 B=<danh sách 2 số làm tròn 4 chữ số> err=<4 chữ số>`\n`step2 B=<danh sách 2 số làm tròn 4 chữ số> err=<4 chữ số>`",
     """X_col = [4.0, 3.0]
A = [[2.0, 1.0], [1.0, 2.0]]
B = [1.0, 1.0]
for step in range(1, 3):
    pred = [A[r][0] * B[0] + A[r][1] * B[1] for r in range(2)]
    num = [A[0][c] * X_col[0] + A[1][c] * X_col[1] for c in range(2)]
    den = [A[0][c] * pred[0] + A[1][c] * pred[1] for c in range(2)]
    B = [B[c] * num[c] / den[c] for c in range(2)]
    rec = [A[r][0] * B[0] + A[r][1] * B[1] for r in range(2)]
    err = sum((X_col[r] - rec[r]) ** 2 for r in range(2))
    print(f"step{step} B={[round(x, 4) for x in B]} err={err:.4f}")"""),

    ("L32", "t-SNE: đo độ bất đối xứng của độ lệch KL(P || Q)",
     "Dùng lôgarit tự nhiên `ln` (`math.log`) tính độ lệch `KL(P || Q) = sum(p * ln(p / q))` và `KL(Q || P)` cho hai phân phối `P = [0.7, 0.3]`, `Q = [0.4, 0.6]`, kiểm chứng bất đối xứng và `KL >= 0`.\n\nĐịnh dạng đầu ra (2 dòng):\n`KL_PQ=<6 chữ số> KL_QP=<6 chữ số>`\n`asymmetric=<0 hoặc 1> nonneg=<0 hoặc 1>`",
     """import math
kl = lambda P, Q: sum(p * math.log(p / q) for p, q in zip(P, Q))
P, Q = [0.7, 0.3], [0.4, 0.6]
d1, d2 = kl(P, Q), kl(Q, P)
print(f"KL_PQ={d1:.6f} KL_QP={d2:.6f}")
print(f"asymmetric={int(abs(d1 - d2) > 1e-3)} nonneg={int(d1 >= 0)}")"""),

    ("L33", "Tổng ôn: quy tắc chọn mô hình theo cỡ mẫu và loại tác vụ",
     "Cài hàm chọn mô hình `pick(n, kind)` theo quy tắc ba tầng: nếu tác vụ là giảm chiều vẽ hình (`kind == 'viz'`) thì chọn `'PCA/t-SNE'`; nếu là dữ liệu dạng bảng (`kind == 'tab'`): với cỡ mẫu `n < 1000` chọn `'Linear/Ridge'`, ngược lại (`n >= 1000`) chọn `'Tree/Boosting'`. Kiểm hàm với 3 kịch bản: `(500, 'tab')`, `(100000, 'tab')`, `(5000, 'viz')`.\n\nĐịnh dạng đầu ra (3 dòng):\n`s1= <tên>`\n`s2= <tên>`\n`s3= <tên>`",
     """def pick(n, kind):
    if kind == 'viz':
        return 'PCA/t-SNE'
    return 'Linear/Ridge' if n < 1000 else 'Tree/Boosting'
print("s1=", pick(500, 'tab'))
print("s2=", pick(100000, 'tab'))
print("s3=", pick(5000, 'viz'))"""),

    ("L34", "CNN: kích thước bản đồ đặc trưng đầu ra và tổng số tham số tích chập",
     "Cho ảnh vuông `28 × 28`, bộ lọc vuông cạnh `K = 5` (thay vì `3` trong bài), đệm `P = 2`, bước nhảy `S = 2`, số kênh vào `C_vao = 3`, số kênh ra `C_ra = 8`, mỗi bộ lọc có cộng 1 hệ số tự do (bias). Tính kích thước phẳng trải của bản đồ đặc trưng đầu ra (`w × w × C_ra`) và tổng số tham số (trọng số và hệ số tự do) của lớp tích chập.\n\nĐịnh dạng đầu ra (2 dòng):\n`out_dim=<w>x<w>x8=<tổng số chiều>`\n`conv_params=<số nguyên>`",
     """n, k, p, s = 28, 5, 2, 2
out_sz = (n - k + 2 * p) // s + 1
params = (k * k * 3 + 1) * 8
dense = out_sz * out_sz * 8
print(f"out_dim={out_sz}x{out_sz}x8={dense}")
print(f"conv_params={params}")"""),

    ("L35", "RNN: suy giảm / bùng nổ gradient qua 20 bước và cắt ngưỡng clip = 5.0",
     "Tính `0.8^20` (tắt dần), `1.2^20` (bùng nổ) và độ lớn chuẩn gradient sau khi áp dụng phép cắt trần `clip = 5.0` (nếu vượt ngưỡng `5.0` thì giữ ở `5.0`).\n\nĐịnh dạng đầu ra (2 dòng):\n`vanish_20=<5 chữ số> explode_20=<2 chữ số>`\n`clipped_norm=<2 chữ số>`",
     """t = 20
vanish = 0.8 ** t
explode = 1.2 ** t
clipped = min(explode, 5.0)
print(f"vanish_20={vanish:.5f} explode_20={explode:.2f}")
print(f"clipped_norm={clipped:.2f}")"""),

    ("L36", "AdaBoost trọng số alpha và Gradient Boosting (GBDT) sửa phần dư",
     "Tính trọng số mô hình yếu trong AdaBoost `alpha = 0.5 * ln((1 - eps)/eps)` tại `eps = 0.2`. Sau đó với mô hình cây tăng cường theo gradient (**GBDT** — *Gradient Boosted Decision Trees*), xuất phát từ giá trị đích `y = 10.0`, dự đoán ban đầu `f = 0.0` và tốc độ học `lr = 0.5`: chạy 2 vòng cập nhật `f += lr * (y - f)` để lấy dự đoán và phần dư còn lại `y - f`.\n\nĐịnh dạng đầu ra (2 dòng):\n`adaboost_alpha=<4 chữ số>`\n`gbdt_f2=<2 chữ số> rem=<2 chữ số>`",
     """import math
eps = 0.2
alpha = 0.5 * math.log((1.0 - eps) / eps)
y, f, lr = 10.0, 0.0, 0.5
for _ in range(2):
    f += lr * (y - f)
print(f"adaboost_alpha={alpha:.4f}")
print(f"gbdt_f2={f:.2f} rem={y - f:.2f}")"""),

    ("L37", "Autoencoder tuyến tính: chiếu lên trục đơn vị (0.6, 0.8) và đo MSE tái tạo",
     "Chiếu 4 điểm `[(3, 4), (5, 0), (-3, -4), (0, 5)]` lên vector đơn vị `u = (0.6, 0.8)` (`z = x*u[0] + y*u[1]`), rồi khôi phục `(z*u[0], z*u[1])` và đo trung bình theo 4 điểm của tổng bình phương sai lệch hai toạ độ `(dx^2 + dy^2)` (`MSE` chuẩn vectơ hai chiều trên 4 mẫu).\n\nĐịnh dạng đầu ra (2 dòng):\n`latent=<danh sách 4 số làm tròn 3 chữ số>`\n`recon_mse=<4 chữ số>`",
     """pts = [(3.0, 4.0), (5.0, 0.0), (-3.0, -4.0), (0.0, 5.0)]
u = (0.6, 0.8)
z = [x * u[0] + y * u[1] for x, y in pts]
mse = sum((x - zi * u[0]) ** 2 + (y - zi * u[1]) ** 2 for (x, y), zi in zip(pts, z)) / len(pts)
print(f"latent={[round(v, 3) for v in z]}")
print(f"recon_mse={mse:.4f}")"""),

    ("L38", "ICA: kiểm tra tính bất biến tỉ lệ và dấu của độ nhọn dư",
     "Cho dãy đối xứng quanh 0 là `xs = [-1.5, -0.5, 0.5, 1.5]` (trung bình `m = 0`, phương sai `sd^2 = sum(x^2)/n`). Tính **độ nhọn dư** (`excess kurtosis = (1/n) * sum((x / sd)^4) - 3`) trên `xs` và trên dãy đổi dấu phóng đại `[-2.0 * x for x in xs]` để chứng minh bất biến theo dấu và tỉ lệ.\n\nĐịnh dạng đầu ra (2 dòng):\n`kurt=<4 chữ số> scaled_neg_kurt=<4 chữ số>`\n`sign_scale_invariant=<0 hoặc 1>`",
     """xs = [-1.5, -0.5, 0.5, 1.5]
kurt = lambda v: sum((x ** 4) for x in v) / len(v) / ((sum(x * x for x in v) / len(v)) ** 2) - 3.0
k1 = kurt(xs)
k2 = kurt([-2.0 * x for x in xs])
print(f"kurt={k1:.4f} scaled_neg_kurt={k2:.4f}")
print(f"sign_scale_invariant={int(abs(k1 - k2) < 1e-9)}")"""),

    ("L39", "Thực hành 1 bước cập nhật Q-learning với alpha = 0.25, gamma = 0.8",
     "Thực hiện một bước cập nhật công thức `Q(s, a) <- Q + alpha * (r + gamma * maxQ' - Q)` với các tham số mới `Q = 1.0`, tốc độ học `alpha = 0.25`, phần thưởng ngay `r = 2.0`, hệ số chiết khấu `gamma = 0.8`, và giá trị tốt nhất tại trạng thái kế tiếp `maxQ' = 8.0`.\n\nĐịnh dạng đầu ra (2 dòng):\n`target=<1 chữ số> td_err=<1 chữ số>`\n`q_new=<2 chữ số>`",
     """q, alpha, r, gamma, max_qn = 1.0, 0.25, 2.0, 0.8, 8.0
td_target = r + gamma * max_qn
q_new = q + alpha * (td_target - q)
print(f"target={td_target:.1f} td_err={td_target - q:.1f}")
print(f"q_new={q_new:.2f}")"""),

    ("L40", "UMAP: trọng số đối xứng hoá đồ thị 1 láng giềng gần nhất (1-NN)",
     "Cho đồ thị 1 láng giềng gần nhất (**1-NN**, *1-Nearest Neighbor*) có các trọng số có hướng trong cụm `w01 = 1.0, w10 = 1.0` và giữa hai cụm `w12 = 0.02, w21 = 0.0`. Tính trọng số đối xứng `w_sym = w_ij + w_ji - w_ij * w_ji` cho cặp gần (`0-1`), cặp nối hai cụm (`1-2`) và kiểm điều kiện giữ cụm `w_near > 10 * w_cross`.\n\nĐịnh dạng đầu ra (2 dòng):\n`w_near_01=<2 chữ số> w_cross_12=<4 chữ số>`\n`keeps_cluster=<0 hoặc 1>`",
     """sym = lambda a, b: a + b - a * b
w_near = sym(1.0, 1.0)
w_cross = sym(0.02, 0.0)
print(f"w_near_01={w_near:.2f} w_cross_12={w_cross:.4f}")
print(f"keeps_cluster={int(w_near > 10 * w_cross)}")"""),

    ("L41", "Attention: softmax(QK^T / sqrt(d)) * V và kiểm tổng trọng số = 1",
     "Tính cơ chế chú ý (`attention`) với số chiều `d = 4`, dãy điểm `QK^T = [2.0, 0.0]`, chia `sqrt(4) = 2`, chuẩn hoá mũ (softmax) theo hàng rồi lấy trung bình có trọng số với vector giá trị `V = [10.0, 2.0]`.\n\nĐịnh dạng đầu ra (2 dòng):\n`weights=<danh sách 2 số làm tròn 4 chữ số> sum=<1 chữ số>`\n`attn_out=<4 chữ số>`",
     """import math
scores = [2.0 / math.sqrt(4.0), 0.0 / math.sqrt(4.0)]
exps = [math.exp(s) for s in scores]
w = [e / sum(exps) for e in exps]
out = w[0] * 10.0 + w[1] * 2.0
print(f"weights={[round(x, 4) for x in w]} sum={sum(w):.1f}")
print(f"attn_out={out:.4f}")"""),

    ("L42", "VAE KL(N(mu, sigma^2) || N(0, 1)) và điểm tối ưu trò chơi GAN",
     "Tính độ lệch `KL = 0.5 * (sigma^2 + mu^2 - 1 - ln(sigma^2))` tại `(mu = 1.0, sigma = 2.0)` và xác định bộ phân biệt tối ưu `D*` cùng giá trị trò chơi tại **cân bằng Nash** của GAN khi mật độ thật `p_real = 0.25` và mật độ giả `p_fake = 0.25`.\n\nĐịnh dạng đầu ra (2 dòng):\n`vae_kl=<4 chữ số>`\n`gan_nash_d=<2 chữ số> val=<4 chữ số>`",
     """import math
mu, sig = 1.0, 2.0
kl = 0.5 * (sig ** 2 + mu ** 2 - 1.0 - math.log(sig ** 2))
p_real, p_fake = 0.25, 0.25
d_star = p_real / (p_real + p_fake)
gan_val = math.log(d_star) + math.log(1.0 - d_star)
print(f"vae_kl={kl:.4f}")
print(f"gan_nash_d={d_star:.2f} val={gan_val:.4f}")"""),

    ("L43", "Diffusion: suy giảm tín hiệu alpha_bar = prod(1 - beta_t) qua 500 bước",
     "Với lịch tuyến tính mới `T = 500` bước từ `beta_0 = 0.0002` tới `beta_{T-1} = 0.015`, chạy vòng lặp tính `alpha_bar = prod(1 - beta_t)` và tính hệ số tỉ lệ độ lệch nhiễu `sqrt(1 - alpha_bar)`.\n\nĐịnh dạng đầu ra (2 dòng):\n`alpha_bar_500=<2 chữ số dạng e>`\n`noise_scale=<6 chữ số>`",
     """T = 500
b0, b1 = 0.0002, 0.015
ab = 1.0
for t in range(T):
    beta = b0 + (b1 - b0) * t / (T - 1)
    ab *= (1.0 - beta)
print(f"alpha_bar_500={ab:.2e}")
print(f"noise_scale={(1.0 - ab) ** 0.5:.6f}")"""),
]

assert len(LABS) == 22, len(LABS)
assert set(COVERS) == {x[0] for x in LABS}

for lid, hint, de_body, sol in LABS:
    de_md = f"# Lab CS115 {lid} — {hint}\n\n{de_body}\n\nChấm tự động:\n```bash\nbash labs/cham.sh CS115 {lid} duong_dan/bai_cua_ban.py\n```\n"
    common.upgrade_lesson(
        "CS115", lid, hint, de_md, sol,
        add_code_if_missing=True,
        covers=COVERS[lid],
        force_code=True,
    )
    print(f"OK CS115:{lid}", flush=True)

# Verify locked L00..L21 + L44..L46 digests untouched!
for lid, old_d in LOCKED_DIGESTS.items():
    fp = up._lesson_path("CS115", lid)
    new_d = lv.spec_digest(lv.load_spec(fp))
    assert old_d == new_d, f"LOCKED CS115:{lid} digest changed! {old_d} != {new_d}"
print("LOCKED CHECK OK: all 25 L00..L21+L44..L46 digests preserved verbatim!", flush=True)

led_p, nblk = up.sync_course_ledger("CS115", default_lang="python")
for lid, _, _, sol in LABS:
    common.sync_practice_run_blocks("CS115", lid, sol)
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks", flush=True)

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for cmd in (
    [PY, "-B", "audit/review/sync_tpl_from_lesson.py", "CS115", "--write"],
    [PY, "-B", "audit/review/screen_code.py", "check", "--course", "CS115"],
    [PY, "-B", "audit/review/lab_gate.py", "CS115"],
):
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"failed: {cmd}"
print("ALL CS115 L22..L43 PASSED!", flush=True)
