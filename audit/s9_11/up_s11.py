"""Nâng cấp AF2 Chặng 11: RBM (18) + ESY (16) + ROB (14) + GFX (14) + BCH (13) = 75 bài."""
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
    "RBM:L00": [(1, 'example'), (2, 'props'), (3, 'frames')],
    "RBM:L01": [(1, 'example'), (2, 'check'), (3, 'gimbal')],
    "RBM:L02": [(1, 'sym'), (2, 'example'), (3, 'props')],
    "RBM:L03": [(1, 'example'), (2, 'chain'), (3, 'chain')],
    "RBM:L04": [(1, 'example'), (2, 'check'), (3, 'reach')],
    "RBM:L05": [(1, 'example'), (2, 'reach'), (3, 'pitfalls')],
    "RBM:L06": [(1, 'example'), (2, 'singular'), (3, 'near')],
    "RBM:L07": [(1, 'formula'), (2, 'example'), (3, 'error')],
    "RBM:L08": [(1, 'example'), (2, 'compare'), (3, 'stiff')],
    "RBM:L09": [(1, 'example'), (2, 'complex'), (3, 'discrete')],
    "RBM:L10": [(1, 'ponly'), (1, 'addi'), (2, 'ponly'), (3, 'pitfalls')],
    "RBM:L11": [(1, 'example'), (2, 'system'), (3, 'gd')],
    "RBM:L12": [(1, 'formula'), (2, 'check'), (3, 'cycle')],
    "RBM:L13": [(1, 'formula'), (2, 'example'), (3, 'intuition')],
    "RBM:L14": [(1, 'nyquist'), (2, 'example'), (3, 'dft')],
    "RBM:L15": [(1, 'example'), (2, 'admissible'), (3, 'example')],
    "RBM:L16": [(1, 'example'), (2, 'example'), (3, 'extrapolate')],
    "RBM:L17": [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (2, 'stage1'), (2, 'stage2'), (2, 'check'), (2, 'stage4'), (3, 'stage4')],
    "ESY:L00": [(1, 'sym'), (2, 'realtime'), (3, 'example')],
    "ESY:L01": [(1, 'sym'), (2, 'ops'), (3, 'pitfalls')],
    "ESY:L02": [(1, 'isr'), (2, 'isr'), (3, 'example')],
    "ESY:L03": [(1, 'pwm'), (2, 'pwm'), (3, 'pitfalls')],
    "ESY:L04": [(1, 'sym'), (2, 'snr'), (3, 'example')],
    "ESY:L05": [(1, 'sampling'), (2, 'example'), (3, 'pitfalls')],
    "ESY:L06": [(1, 'sym'), (2, 'example'), (3, 'overflow')],
    "ESY:L07": [(1, 'speed'), (2, 'speed'), (3, 'example')],
    "ESY:L08": [(1, 'i2c'), (2, 'i2c'), (3, 'example')],
    "ESY:L09": [(1, 'example'), (2, 'rta'), (3, 'rta')],
    "ESY:L10": [(1, 'example'), (2, 'overload'), (3, 'inversion')],
    "ESY:L11": [(1, 'sym'), (2, 'queue'), (3, 'pitfalls')],
    "ESY:L12": [(1, 'where'), (2, 'example'), (3, 'heap')],
    "ESY:L13": [(1, 'example'), (2, 'check'), (3, 'example')],
    "ESY:L14": [(1, 'sym'), (2, 'boot'), (3, 'example')],
    "ESY:L15": [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'), (2, 'check'), (3, 'stage5')],
    "ROB:L00": [(1, 'sym'), (2, 'example'), (3, 'sym')],
    "ROB:L01": [(1, 'example'), (2, 'example'), (3, 'pitfalls')],
    "ROB:L02": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
    "ROB:L03": [(1, 'example'), (2, 'intuition'), (3, 'pitfalls')],
    "ROB:L04": [(1, 'example'), (2, 'example'), (3, 'check')],
    "ROB:L05": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "ROB:L06": [(1, 'sym'), (2, 'example'), (3, 'intuition')],
    "ROB:L07": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "ROB:L08": [(1, 'example'), (2, 'sym'), (3, 'check')],
    "ROB:L09": [(1, 'sym'), (2, 'intuition'), (3, 'example')],
    "ROB:L10": [(1, 'example'), (2, 'check'), (3, 'lookahead')],
    "ROB:L11": [(1, 'sym'), (2, 'intuition'), (3, 'example')],
    "ROB:L12": [(1, 'example'), (2, 'example'), (3, 'check')],
    "ROB:L13": [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'), (2, 'check'), (3, 'quiz')],
    "GFX:L00": [(1, 'intuition'), (2, 'example'), (3, 'example')],
    "GFX:L01": [(1, 'formula'), (2, 'example'), (3, 'check')],
    "GFX:L02": [(1, 'formula'), (2, 'formula'), (3, 'check')],
    "GFX:L03": [(1, 'formula'), (2, 'formula'), (3, 'example')],
    "GFX:L04": [(1, 'example'), (2, 'check'), (3, 'example')],
    "GFX:L05": [(1, 'example'), (2, 'formula'), (3, 'example')],
    "GFX:L06": [(1, 'example'), (2, 'check'), (3, 'intuition'), (4, 'pitfalls')],
    "GFX:L07": [(1, 'formula'), (2, 'example'), (3, 'formula'), (4, 'check')],
    "GFX:L08": [(1, 'intuition'), (2, 'formula'), (3, 'example'), (4, 'example')],
    "GFX:L09": [(1, 'example'), (2, 'formula'), (3, 'intuition'), (4, 'pitfalls')],
    "GFX:L10": [(1, 'example'), (2, 'check'), (3, 'pitfalls'), (4, 'formula')],
    "GFX:L11": [(1, 'example'), (2, 'formula'), (3, 'pitfalls'), (4, 'pitfalls')],
    "GFX:L12": [(1, 'formula'), (2, 'example'), (3, 'example'), (4, 'pitfalls')],
    "GFX:L13": [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (2, 'check'), (3, 'stage4')],
    "BCH:L00": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
    "BCH:L01": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "BCH:L02": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "BCH:L03": [(1, 'example'), (2, 'check'), (3, 'check')],
    "BCH:L04": [(1, 'example'), (2, 'check'), (3, 'check')],
    "BCH:L05": [(1, 'sym'), (2, 'example'), (3, 'check')],
    "BCH:L06": [(1, 'example'), (2, 'check'), (3, 'check')],
    "BCH:L07": [(1, 'example'), (2, 'check'), (3, 'check')],
    "BCH:L08": [(1, 'sym'), (2, 'example'), (3, 'pitfalls')],
    "BCH:L09": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "BCH:L10": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "BCH:L11": [(1, 'example'), (2, 'check'), (3, 'pitfalls')],
    "BCH:L12": [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'), (2, 'check'), (3, 'stage5')],
}

DATA = {
    "RBM": [
        ("L00", "Kiểm chứng ma trận quay 2D R(60°): tính R^T R = I và định thức det R",
         "Lập ma trận quay 2D góc `theta = 60°` (`[[c, -s], [s, c]]`), quay vector `(2, 0)`, tính sai số trực giao lớn nhất của `R^T * R - I` và định thức `det = c^2 + s^2`.\nIn đúng 1 dòng theo mẫu `rot=(x, y) ortho_err=e det=d` (3 chữ số thập phân cho toạ độ và det, dạng `:.1e` cho `ortho_err`).",
         """import math
t = math.radians(60.0)
c, s = math.cos(t), math.sin(t)
R = [[c, -s], [s, c]]
x, y = R[0][0] * 2.0 + R[0][1] * 0.0, R[1][0] * 2.0 + R[1][1] * 0.0
RtR = [[R[0][i]*R[0][j] + R[1][i]*R[1][j] for j in range(2)] for i in range(2)]
ortho_err = max(abs(RtR[i][j] - (1.0 if i == j else 0.0)) for i in range(2) for j in range(2))
det = R[0][0] * R[1][1] - R[0][1] * R[1][0]
print(f"rot=({x:.3f}, {y:.3f}) ortho_err={ortho_err:.1e} det={det:.3f}")"""),

        ("L01", "Kiểm định quay 3D quanh X và Z theo hai thứ tự ngược nhau",
         "Với vector `(1, 1, 0)`, hãy quay `90°` quanh `X` trước rồi `Z` sau (`p1 = Rz(Rx(v))`), và ngược lại (`p2 = Rx(Rz(v))`).\nIn đúng 1 dòng theo mẫu `Rz_after_Rx=(...) Rx_after_Rz=(...) equal=0/1`.",
         """rx = lambda p: (p[0], -p[2], p[1])
rz = lambda p: (-p[1], p[0], p[2])
v = (1, 1, 0)
p1 = rz(rx(v))
p2 = rx(rz(v))
print(f"Rz_after_Rx={p1} Rx_after_Rz={p2} equal={int(p1 == p2)}")"""),

        ("L02", "Quay vector bằng quaternion đơn vị và kiểm chuẩn độ dài ||q|| = 1",
         "Dựng quaternion đơn vị `q = (cos 30°, 0, 0, sin 30°)` (quay `60°` quanh trục `z`), kiểm tra độ dài chuẩn `||q||` và quay vector `(1, 2, 0)` bằng `q * (0, x, y, z) * q^-1` (trong đó nghịch đảo `q^-1` giữ phần thực và đổi dấu ba thành phần vector `i, j, k`).\nIn đúng 1 dòng `norm_q=... rotated=(x, y, z)` (`norm_q` lấy 3 chữ số thập phân `:.3f`, từng toạ độ trong `rotated` dùng `round(..., 3)`).",
         """import math
t = math.radians(30.0)
q = (math.cos(t), 0.0, 0.0, math.sin(t))
norm_q = math.sqrt(sum(c * c for c in q))
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
res = qmul(qmul(q, (0.0, 1.0, 2.0, 0.0)), (q[0], -q[1], -q[2], -q[3]))
print(f"norm_q={norm_q:.3f} rotated=({round(res[1],3)}, {round(res[2],3)}, {round(res[3],3)})")"""),

        ("L03", "Toạ độ thuần nhất: so sánh thứ tự quay 90° và tịnh tiến (3, -1)",
         "Áp dụng hai thứ tự biến đổi lên điểm `(2, 1)`: quay `90°` ngược chiều kim đồng hồ quanh gốc rồi tịnh tiến `(3, -1)`, và tịnh tiến `(3, -1)` trước rồi quay `90°`.\nIn đúng 1 dòng `rot_then_tr=(...) tr_then_rot=(...)`.",
         """rot90 = lambda x, y: (-y, x)
tr = lambda x, y: (x + 3, y - 1)
a = tr(*rot90(2, 1))
b = rot90(*tr(2, 1))
print(f"rot_then_tr={a} tr_then_rot={b}")"""),

        ("L04", "Động học thuận tay máy 2 khâu phẳng L1=1.2, L2=0.8",
         "Cho tay máy 2 khâu phẳng dài `L1 = 1.2 m, L2 = 0.8 m` với góc khớp `t1 = 45°, t2 = 45°`. Tính vị trí đầu tay `(x, y)` và khoảng cách từ gốc `r = sqrt(x^2 + y^2)`.\nIn đúng 1 dòng `end=(x, y) dist=r` (3 chữ số thập phân).",
         """import math
L1, L2 = 1.2, 0.8
t1, t2 = math.radians(45.0), math.radians(45.0)
x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)
y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)
dist = math.hypot(x, y)
print(f"end=({x:.3f}, {y:.3f}) dist={dist:.3f}")"""),

        ("L05", "Giải động học ngược tay máy 2 khâu L1=L2=1.0 bằng định lý cos và atan2",
         "Cho `L1 = 1.0, L2 = 1.0` và điểm đích `(x, y) = (1.2, 0.9)`. Hãy tính hai cặp góc khớp `(t1, t2)` (khuỷu dưới `t2 > 0` và khuỷu trên `t2 < 0`) bằng định lý cos + `math.atan2`, rồi kiểm định lại bằng động học thuận xem cả hai có về đúng `(1.2, 0.9)`.\nIn đúng 1 dòng `down=(t1, t2) up=(t1, t2) fk_match=0/1` (góc theo độ, 2 chữ số).",
         """from math import cos, sin, acos, atan2, degrees
L1, L2, x, y = 1.0, 1.0, 1.2, 0.9
c2 = (x*x + y*y - L1*L1 - L2*L2) / (2.0 * L1 * L2)
def solve(s):
    t2 = s * acos(c2)
    return atan2(y, x) - atan2(L2*sin(t2), L1 + L2*cos(t2)), t2
sols = [solve(1), solve(-1)]
ok = all(abs(L1*cos(a)+L2*cos(a+b)-x) < 1e-9
         and abs(L1*sin(a)+L2*sin(a+b)-y) < 1e-9 for a, b in sols)
deg = lambda a, b: (round(degrees(a), 2), round(degrees(b), 2))
print(f"down={deg(*sols[0])} up={deg(*sols[1])} fk_match={int(ok)}")"""),

        ("L06", "Lập ma trận Jacobian 2×2 và phát hiện cấu hình kỳ dị tay máy 2 khâu",
         "Cho `L1 = 1.0, L2 = 0.5, t1 = 30°`. Hãy lập đầy đủ ma trận Jacobian `2x2` `J(t1, t2)` và tính định thức trực tiếp từ các phần tử của `J` tại `t2 = 90°` (xa kỳ dị) và `t2 = 0°` (duỗi thẳng kỳ dị).\nIn đúng 1 dòng `det_90=... det_0=...` (3 chữ số).",
         """import math
def jac_det(t1_deg, t2_deg, L1=1.0, L2=0.5):
    t1, t2 = math.radians(t1_deg), math.radians(t2_deg)
    J = [
        [-L1 * math.sin(t1) - L2 * math.sin(t1 + t2), -L2 * math.sin(t1 + t2)],
        [L1 * math.cos(t1) + L2 * math.cos(t1 + t2), L2 * math.cos(t1 + t2)],
    ]
    return J[0][0] * J[1][1] - J[0][1] * J[1][0]
print(f"det_90={jac_det(30, 90):.3f} det_0={jac_det(30, 0):.3f}")"""),

        ("L07", "Giải gần đúng phương trình vi phân x' = -2x bằng Euler từ x(0)=1",
         "Giải gần đúng `x' = -2x` từ `x(0) = 1.0` tới `t = 1.0` bằng `20` bước Euler cỡ `h = 0.05`, đối chiếu với nghiệm đúng `exp(-2)`.\nIn đúng 1 dòng `euler=... exact=... err=...` (4 chữ số thập phân).",
         """import math
x, h = 1.0, 0.05
for _ in range(20): x += h * (-2.0 * x)
exact = math.exp(-2.0)
print(f"euler={x:.4f} exact={exact:.4f} err={abs(x - exact):.4f}")"""),

        ("L08", "So sánh trực tiếp RK4 với Euler trên cùng bước h=0.2 giải x' = -x",
         "Từ `x(0) = 1.0`, chạy `5` bước tới `t = 1.0` với `h = 0.2` theo cả Euler và RK4, đối chiếu với `exp(-1)` và tính tỉ lệ giảm sai số `err_euler / err_rk4`.\nIn đúng 1 dòng `err_euler=... err_rk4=... gain=...x` (`err_euler` lấy 4 chữ số thập phân `:.4f`, `err_rk4` dạng khoa học `:.2e`, `gain` làm tròn nguyên `:.0f`).",
         """import math
x_e, x_r, h = 1.0, 1.0, 0.2
for _ in range(5):
    x_e += h * (-x_e)
    k1 = -x_r; k2 = -(x_r + 0.5*h*k1); k3 = -(x_r + 0.5*h*k2); k4 = -(x_r + h*k3)
    x_r += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
exact = math.exp(-1.0)
e_e, e_r = abs(x_e - exact), abs(x_r - exact)
print(f"err_euler={e_e:.4f} err_rk4={e_r:.2e} gain={e_e/e_r:.0f}x")"""),

        ("L09", "Tính trị riêng và kiểm định ổn định hệ tuyến tính x' = Ax",
         "Cho ma trận trạng thái `A = [[0, 1], [-6, -5]]`. Tính tổng đường chéo `A[0][0] + A[1][1]`, định thức `det(A)`, giải phương trình đặc trưng tìm hai trị riêng `(l1, l2)` theo thứ tự giảm dần `l1 >= l2` và kiểm tra cả hai đều âm (`stable=0/1`).\nIn đúng 1 dòng `eigs=(l1, l2) stable=0/1` (mỗi trị riêng lấy 1 chữ số thập phân `:.1f`).",
         """import math
A = [[0.0, 1.0], [-6.0, -5.0]]
tr = A[0][0] + A[1][1]
det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
disc = math.sqrt(tr*tr - 4.0*det)
l1, l2 = (tr + disc) / 2.0, (tr - disc) / 2.0
print(f"eigs=({l1:.1f}, {l2:.1f}) stable={int(l1 < 0 and l2 < 0)}")"""),

        ("L10", "So sánh sai số xác lập điều khiển P thuần và PI hội tụ về 0",
         "Cho hệ bậc nhất `y' = -y + u` xuất phát `y(0) = 0`, tích phân đầu `integ(0) = 0`, mục tiêu `r = 1.0`. Tính sai số xác lập lý thuyết của khâu P thuần `u = K*(1 - y)` (`K = 3.0`). Sau đó mô phỏng `150` bước Euler tiến (`y += dt * (-y + u)`, `dt = 0.05`, tích luỹ `integ += err * dt`) cho bộ điều khiển PI (`Kp = 1.2, Ki = 1.5`).\nIn đúng 1 dòng `P_steady_err=... PI_final_err=...` (4 chữ số thập phân `:.4f`).",
         """k = 3.0
ss_err_p = 1.0 / (1.0 + k)
y, integ, dt = 0.0, 0.0, 0.05
for _ in range(150):
    e = 1.0 - y
    integ += e * dt
    u = 1.2 * e + 1.5 * integ
    y += dt * (-y + u)
print(f"P_steady_err={ss_err_p:.4f} PI_final_err={abs(1.0 - y):.4f}")"""),

        ("L11", "Kiểm định điều kiện bước ổn định Euler trên x' = -8x",
         "Với hệ `x' = -8x`, tính hệ số nhân mỗi bước Euler `g(h) = 1 - 8*h` tại `h = 0.30` (`g_030`, 2 chữ số `:.2f`), cùng giá trị sau `10` bước xuất phát từ `x0 = 1.0` ở cỡ bước phân kỳ `h = 0.30` (`x10_div`, 2 chữ số `:.2f`) và cỡ bước hội tụ `h = 0.05` (`x10_conv`, 5 chữ số `:.5f`).\nIn đúng 1 dòng `g_030=... x10_div=... x10_conv=...`.",
         """run = lambda h: (1.0 - 8.0 * h) ** 10
print(f"g_030={1.0 - 8.0*0.30:.2f} x10_div={run(0.30):.2f} x10_conv={run(0.05):.5f}")"""),

        ("L12", "Vòng dự đoán – cập nhật bộ lọc Kalman một chiều",
         "Cho dự đoán `x = 2.0, P = 4.0` và phép đo `z = 5.0, R = 2.0`. Tính hệ số Kalman `K = P / (P + R)`, trạng thái cập nhật `x_new` và phương sai mới `P_new`.\nIn đúng 1 dòng `K=... x_est=... P_est=...` (3 chữ số).",
         """x, P, z, R = 2.0, 4.0, 5.0, 2.0
K = P / (P + R)
x_new = x + K * (z - x)
P_new = (1.0 - K) * P
print(f"K={K:.3f} x_est={x_new:.3f} P_est={P_new:.3f}")"""),

        ("L13", "Lan truyền hiệp phương sai F*P*F^T trong lọc Kalman 2D",
         "Cho ma trận hiệp phương sai ban đầu `P = [[2.0, 0.5], [0.5, 1.0]]` và ma trận chuyển trạng thái bước `h = 0.5`: `F = [[1.0, 0.5], [0.0, 1.0]]`. Hãy nhân đầy đủ `F * P * F^T` để lấy phương sai vị trí `P_00` và hiệp phương sai vị trí–vận tốc `P_01`.\nIn đúng 1 dòng `pred_var_pos=... cross_cov_pos_vel=...` (2 chữ số).",
         """F = [[1.0, 0.5], [0.0, 1.0]]
P = [[2.0, 0.5], [0.5, 1.0]]
def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
Ft = [[F[j][i] for j in range(2)] for i in range(2)]
P_new = mm(mm(F, P), Ft)
print(f"pred_var_pos={P_new[0][0]:.2f} cross_cov_pos_vel={P_new[0][1]:.2f}")"""),

        ("L14", "Định lý lấy mẫu Nyquist và tần số biểu kiến khi chồng phổ",
         "Một tín hiệu dao động ở tần số `f = 9 Hz` được lấy mẫu ở `fs = 12 Hz`. Tính ngưỡng lấy mẫu tối thiểu `2 * f` và tần số biểu kiến `|f - round(f/fs)*fs|`.\nIn đúng 1 dòng `need_fs_gt=...Hz observed_alias=...Hz`.",
         """f_sig, fs = 9.0, 12.0
nyquist_min = 2.0 * f_sig
k = round(f_sig / fs)
alias = abs(f_sig - k * fs)
print(f"need_fs_gt={nyquist_min:.0f}Hz observed_alias={alias:.0f}Hz")"""),

        ("L15", "Tìm đường ngắn nhất A* trên lưới 4×5 có chướng ngại vật",
         "Cho lưới kích thước `4 hàng × 5 cột` (`0 <= r < 4, 0 <= c < 5`), danh sách tường `{(0, 2), (1, 2), (2, 2)}`, điểm xuất phát `(1, 0)` và đích `(1, 4)` (chỉ đi 4 hướng kề). Chạy thuật toán `A*` với hàm ước lượng Manhattan `|r - r_goal| + |c - c_goal|` và in giá trị `h` tại gốc cùng độ dài đường đi ngắn nhất.\nIn đúng 1 dòng `astar_steps=... h_start=...`.",
         """import heapq
walls = {(0, 2), (1, 2), (2, 2)}; start, goal = (1, 0), (1, 4)
h = lambda p: abs(p[0]-goal[0]) + abs(p[1]-goal[1])
pq = [(h(start), 0, start)]; dist = {start: 0}
while pq:
    _, g, u = heapq.heappop(pq)
    if u == goal: print(f"astar_steps={g} h_start={h(start)}"); break
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        v = (u[0]+dr, u[1]+dc)
        if 0 <= v[0] < 4 and 0 <= v[1] < 5 and v not in walls and g+1 < dist.get(v, 99):
            dist[v] = g + 1; heapq.heappush(pq, (g + 1 + h(v), g + 1, v))"""),

        ("L16", "Khớp đường thẳng hiệu chuẩn cảm biến bằng bình phương tối thiểu",
         "Cho 4 điểm đo hiệu chuẩn `[(0, 2.0), (1, 4.9), (2, 8.1), (3, 11.0)]`. Hãy tính hệ số góc `a` và hệ số chặn `b` của mô hình tuyến tính `y = a*x + b` bằng bình phương tối thiểu.\nIn đúng 1 dòng `slope=... intercept=...` (2 chữ số).",
         """pts = [(0, 2.0), (1, 4.9), (2, 8.1), (3, 11.0)]
mx = sum(x for x, _ in pts) / len(pts); my = sum(y for _, y in pts) / len(pts)
a = sum((x - mx)*(y - my) for x, y in pts) / sum((x - mx)**2 for x, _ in pts)
b = my - a * mx
print(f"slope={a:.2f} intercept={b:.2f}")"""),

        ("L17", "Phân tích sự co của P khi thiếu nhiễu quá trình Q=0 so với Q>0",
         "Với `P0 = 1.0, R = 1.0`, chạy `49` bước đo Kalman 1D trong hai trường hợp: `Q = 0.0` (tin tuyệt đối mô hình) và `Q = 0.1` (có thêm nhiễu quá trình).\nIn đúng 1 dòng `P_after_49_Q0=... P_after_49_Q01=...` (3 chữ số).",
         """def sim(Q):
    P, R = 1.0, 1.0
    for _ in range(49):
        P = P + Q
        K = P / (P + R)
        P = (1.0 - K) * P
    return P
print(f"P_after_49_Q0={sim(0.0):.3f} P_after_49_Q01={sim(0.1):.3f}")"""),
    ],

    "ESY": [
        ("L00", "Kiểm định ngân sách thời gian trong chu kỳ thời gian thực cứng",
         "Một vi điều khiển có chu kỳ điều khiển cứng `25 ms`, phải chạy 4 bước với thời gian xấu nhất lần lượt là `6, 9, 4, 2 ms`. Tính tổng thời gian tiêu thụ, kiểm tra có kịp hạn hay không và thời gian dư `slack`.\nIn đúng 1 dòng `used_ms=... deadline_met=0/1 slack=...ms`.",
         """budget = 25
used = 6 + 9 + 4 + 2
print(f"used_ms={used} deadline_met={int(used <= budget)} slack={budget - used}ms")"""),

        ("L01", "Thao tác bit an toàn trên thanh ghi ngoại vi 8 bit",
         "Từ thanh ghi ban đầu `reg = 0x12`, thực hiện tuần tự ba phép biến đổi an toàn: bật bit `3`, xoá bit `1`, rồi đảo bit `0`.\nIn đúng 1 dòng `set=... clr=... tog=...` (dạng `hex(...)`).",
         """reg = 0x12
reg |= (1 << 3); r_set = reg
reg &= ~(1 << 1); r_clr = reg
reg ^= (1 << 0); r_tog = reg
print(f"set={hex(r_set)} clr={hex(r_clr)} tog={hex(r_tog)}")"""),

        ("L02", "Chống dội phím bằng máy trạng thái đếm mẫu liên tiếp",
         "Cho chuỗi lấy mẫu `1 ms/lần`: `[0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]`. Cài máy trạng thái chống dội chỉ đổi trạng thái ngõ ra từ `0 -> 1` khi gặp đúng `5` mẫu giống nhau liên tiếp; đồng thời đếm số lần đổi chiều trên tín hiệu thô vs tín hiệu đã lọc.\nIn đúng 1 dòng `accepted_at_ms=... raw_edges=... clean_edges=...`.",
         """samples = [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]
raw_edges = sum(1 for a, b in zip(samples, samples[1:]) if a != b)
state, streak, prev, clean, accepted_idx = 0, 0, None, [], -1
for i, v in enumerate(samples):
    streak = streak + 1 if v == prev else 1
    prev = v
    if streak >= 5 and v != state:
        state = v
        if state == 1 and accepted_idx == -1: accepted_idx = i
    clean.append(state)
clean_edges = sum(1 for a, b in zip(clean, clean[1:]) if a != b)
print(f"accepted_at_ms={accepted_idx} raw_edges={raw_edges} clean_edges={clean_edges}")"""),

        ("L03", "Tính tần số bộ định thời và độ rộng xung PWM từ f_clk, hệ số chia và TOP",
         "Trên bộ định thời xung nhịp `f_clk = 16_000_000 Hz`, chọn hệ số chia `presc = 8`, giá trị đỉnh `TOP = 999` và ngưỡng so sánh `CMP = 250` (chân ra mức cao khi `counter < CMP`). Tính tần số `f_clk / (presc * (TOP + 1))` và chu kỳ nhiệm vụ `CMP / (TOP + 1) * 100%`.\nIn đúng 1 dòng `pwm_hz=... duty_pct=...%`.",
         """f_clk, presc, top, cmp_v = 16_000_000, 8, 999, 250
freq = f_clk / (presc * (top + 1))
duty = cmp_v / (top + 1) * 100.0
print(f"pwm_hz={freq:.0f} duty_pct={duty:.1f}%")"""),

        ("L04", "Bước lượng tử, điện áp quy đổi và SNR lý tưởng của bộ ADC 10-bit",
         "Cho bộ chuyển đổi tương tự–số `10-bit` (`1024` mức) với điện áp chuẩn `5.0 V`. Tính bước lượng tử (đơn vị `mV`), điện áp ứng với mã `256` và tỉ số tín hiệu trên nhiễu lý tưởng `SNR = 6.02 * 10 + 1.76`.\nIn đúng 1 dòng `lsb_mv=... V256=... V SNR=... dB` (2 chữ số thập phân cho mV và SNR, 3 chữ số cho V).",
         """step_mv = 5.0 / 1024 * 1000
v256 = 256 * 5.0 / 1024
snr_db = 6.02 * 10 + 1.76
print(f"lsb_mv={step_mv:.2f} V256={v256:.3f} V SNR={snr_db:.2f} dB")"""),

        ("L05", "Mô phỏng đáp ứng bậc thang của bộ lọc thông thấp số bậc nhất",
         "Với hệ số lọc `alpha = 0.25` và đầu ra ban đầu `y = 0.0`, chạy `8` mẫu có đầu vào cố định `x = 1.0` theo công thức `y <- y + alpha * (x - y)`, rồi đối chiếu với công thức đóng `1 - (1 - alpha)^8`.\nIn đúng 1 dòng `y8=... closed_form=...` (4 chữ số).",
         """y = 0.0
for _ in range(8): y += 0.25 * (1.0 - y)
print(f"y8={y:.4f} closed_form={1.0 - 0.75**8:.4f}")"""),

        ("L06", "Nhân hai số dấu phẩy tĩnh Q8.8 chỉ bằng phép toán số nguyên",
         "Biểu diễn hai số `2.5` và `1.75` ở định dạng nguyên `Q8.8` (nhân `256`), thực hiện phép nhân nguyên rồi dịch phải `8` bit, và quy đổi ngược ra giá trị thực.\nIn đúng 1 dòng `q88_a=... q88_prod=... val=...` (3 chữ số cho val).",
         """a, b = int(2.5 * 256), int(1.75 * 256)
prod = (a * b) >> 8
print(f"q88_a={a} q88_prod={prod} val={prod / 256:.3f}")"""),

        ("L07", "Tính thông lượng và thời gian truyền khung UART 8N1 ở 9600 baud",
         "Khung UART `8N1` cần `10` bit (`1 start + 8 data + 1 stop`) cho mỗi byte. Ở tốc độ `9600 baud`, tính số byte tối đa mỗi giây và thời gian truyền gói `24` byte (tính bằng `ms`).\nIn đúng 1 dòng `bytes_per_sec=... tx_24B_ms=...` (1 chữ số cho ms).",
         """baud, bits_per_byte = 9600, 10
bps = baud // bits_per_byte
tx_ms = 24 / bps * 1000.0
print(f"bytes_per_sec={bps} tx_24B_ms={tx_ms:.1f}")"""),

        ("L08", "So sánh chi phí bit truyền 8 byte giữa bus SPI và I2C ở 100 kHz",
         "Ở xung nhịp `100 kHz`, một giao dịch gửi `8` byte dữ liệu qua SPI chỉ tốn `64` nhịp (`8 * 8`), còn qua I2C cần `1` byte địa chỉ + `8` byte dữ liệu kèm 1 bit xác nhận `ACK` cho mỗi byte (`9 * 9 = 81` nhịp). Tính thời gian truyền (đơn vị micro giây) của hai bus.\nIn đúng 1 dòng `spi_8B_us=... i2c_8B_us=...` (1 chữ số).",
         """t_spi_us = (8 * 8) / 100_000 * 1e6
t_i2c_us = (9 * 9) / 100_000 * 1e6
print(f"spi_8B_us={t_spi_us:.1f} i2c_8B_us={t_i2c_us:.1f}")"""),

        ("L09", "Phân tích mức dùng bộ xử lý (CPU), cận Liu–Layland và phép lặp thời gian đáp ứng (RTA)",
         "Cho ba tác vụ ưu tiên cố định từ cao xuống thấp `[(C1=1, T1=5), (C2=2, T2=8), (C3=2, T3=16)]` (đơn vị `ms`). Tính tổng độ sử dụng `U` (3 chữ số `:.3f`), cận Liu–Layland `3*(2^(1/3) - 1)` (4 chữ số `:.4f`) và lặp phương trình `R = C3 + sum(ceil(R/Ti)*Ci)` tìm thời gian đáp ứng xấu nhất `R3` của tác vụ 3.\nIn đúng 1 dòng `U=... LL_bound=... exact_R3=...`.",
         """import math
tasks = [(1, 5), (2, 8), (2, 16)]
u = sum(c / p for c, p in tasks)
ll = 3 * (2**(1/3) - 1)
r = 2
for _ in range(10): r = 2 + sum(math.ceil(r / p) * c for c, p in tasks[:2])
print(f"U={u:.3f} LL_bound={ll:.4f} exact_R3={r}")"""),

        ("L10", "Mô phỏng lập lịch ưu tiên cố định so với hạn sớm nhất EDF trên chu kỳ 16 ms",
         "Mô phỏng từng nhịp `1 ms` từ `t = 0..15` cho hai tác vụ `(C=4, T=8)` (chỉ số 0) và `(C=2, T=4)` (chỉ số 1) có tổng độ dùng `U = 1.0` theo hai luật: ưu tiên cố định (luôn chọn tác vụ chỉ số 0 nếu sẵn sàng) và hạn sớm nhất (`EDF`, luôn chọn tác vụ có hạn chót `dl` nhỏ hơn). Đếm số lần trễ hạn của mỗi luật.\nIn đúng 1 dòng `U=... fixed_misses=... edf_misses=...` (1 chữ số thập phân cho `U`).",
         """def sim(edf):
    rem, dl, misses = [0, 0], [0, 0], 0
    for t in range(16):
        for i, (c, p) in enumerate(((4, 8), (2, 4))):
            if t % p == 0:
                if rem[i] > 0: misses += 1
                rem[i] = c; dl[i] = t + p
        ready = [i for i in (0, 1) if rem[i] > 0]
        if ready:
            pick = min(ready, key=lambda i: dl[i]) if edf else ready[0]
            rem[pick] -= 1
    return misses + sum(1 for r in rem if r > 0)
u = 4/8 + 2/4
print(f"U={u:.1f} fixed_misses={sim(False)} edf_misses={sim(True)}")"""),

        ("L11", "Mô phỏng hàng đợi giữa ngắt ISR và tác vụ nền tránh mất byte",
         "Tạo hàng đợi vòng (`collections.deque`) độ dài tối đa `8` nhận từng byte của chuỗi `b'TEMP:42\\n'` từ hàm ngắt, đếm số byte bị tràn không đẩy vào được (`overflows`), rồi tác vụ nền lấy toàn bộ phần tử còn trong hàng đợi giải mã thành chuỗi và in dạng `repr` giữ nguyên dấu nháy (`{msg!r}`).\nIn đúng 1 dòng `queued=... overflows=... decoded=...`.",
         """from collections import deque
isr_q, overflows = deque(), 0
for b in b'TEMP:42\\n':
    if len(isr_q) < 8: isr_q.append(b)
    else: overflows += 1
msg = bytes([isr_q.popleft() for _ in range(len(isr_q))]).decode()
print(f"queued={len(msg)} overflows={overflows} decoded={msg!r}")"""),

        ("L12", "Kiểm định watchdog timer và đo đỉnh ngăn xếp bằng mẫu 0xA5",
         "Cho đồng hồ giám sát hết hạn ở `wdt_ms = 90 ms` chạy qua các chu kỳ `[50, 75, 110, 60]` ms (đếm số lần kích hoạt reset), và mô phỏng mảng ngăn xếp `16` byte tô kín `0xA5` bị ghi đè sâu `11` ô ở đáy.\nIn đúng 1 dòng `wdt_resets=... stack_used_B=...`.",
         """wdt_ms = 90
wdt_resets = sum(1 for ms in (50, 75, 110, 60) if ms > wdt_ms)
stack = [0xA5] * 16
for i in range(11): stack[i] = i
used = 16 - sum(1 for v in stack if v == 0xA5)
print(f"wdt_resets={wdt_resets} stack_used_B={used}")"""),

        ("L13", "Ước lượng dòng trung bình và tuổi thọ pin theo chu kỳ thức–ngủ",
         "Thiết bị thức `2%` thời gian ăn `12 mA` và ngủ `98%` thời gian ăn `0.02 mA`, dùng pin `1200 mAh`. Tính dòng tiêu thụ trung bình và số ngày chạy liên tục.\nIn đúng 1 dòng `avg_ma=... battery_days=...` (`avg_ma` lấy 4 chữ số `:.4f`, `battery_days` làm tròn số nguyên `:.0f`).",
         """i_avg = 0.02 * 12.0 + 0.98 * 0.02
days = 1200.0 / i_avg / 24.0
print(f"avg_ma={i_avg:.4f} battery_days={days:.0f}")"""),

        ("L14", "Kiểm toàn vẹn SHA-256, chữ ký và tự quay lui cập nhật A/B",
         "Cho hai phân vùng phần sụn: bản `A` hợp lệ (`sha_ok=True, sig_ok=True, boot_ok=True`) và bản `B` vừa tải có nội dung `b'fw-v2'` nhưng mã kiểm định mong đợi là SHA-256 của `b'fw-v2-clean'` (`sig_ok=True, boot_ok=True`). Viết bộ chọn khởi động so khớp `hashlib.sha256` thực tế để quyết định chọn `'A'` hay `'B'`.\nIn đúng 1 dòng `b_hash_ok=0/1 boot_slot=...`.",
         """import hashlib
exp_sha = hashlib.sha256(b'fw-v2-clean').hexdigest()
b_sha = hashlib.sha256(b'fw-v2').hexdigest()
b_hash_ok = (b_sha == exp_sha)
slot = 'B' if (b_hash_ok and True and True) else 'A'
print(f"b_hash_ok={int(b_hash_ok)} boot_slot={slot}")"""),

        ("L15", "Mô phỏng vượt ngân sách chu kỳ do đảo ngược ưu tiên",
         "Cho hệ chạy chu kỳ `10 Hz` (`100 ms`). Bình thường 3 tác vụ tốn `[25, 5, 30]` ms; khi bị đảo ngược ưu tiên bởi tác vụ trung bình `45 ms`, tổng trễ thành `[25, 45, 5, 30]`. Kiểm tra tình trạng vượt hạn trước và sau.\nIn đúng 1 dòng `period_ms=... normal_ms=... inverted_ms=... overload=0/1`.",
         """period_ms = 1000 / 10
normal = sum([25, 5, 30])
inverted = sum([25, 45, 5, 30])
ovl = int(inverted > period_ms)
print(f"period_ms={period_ms:.0f} normal_ms={normal}",
      f"inverted_ms={inverted} overload={ovl}")"""),
    ],

    "ROB": [
        ("L00", "Tính ngân sách độ trễ cho vòng điều khiển robot 40 Hz",
         "Một robot chạy vòng điều khiển `40 Hz` (`1000/40 ms`), các khối cảm nhận–định vị–lập kế hoạch–chấp hành lần lượt mất `5, 11, 3, 2 ms`. Tính chu kỳ, tổng thời gian dùng và phần dự phòng còn lại.\nIn đúng 1 dòng `budget_ms=... used_ms=... margin_ms=...`.",
         """budget = 1000 / 40
used = 5 + 11 + 3 + 2
print(f"budget_ms={budget:.0f} used_ms={used} margin_ms={budget - used:.0f}")"""),

        ("L01", "Tính vận tốc thẳng, vận tốc góc và bán kính quay của xe vi sai",
         "Cho tốc độ bánh trái `vl = 0.6 m/s`, bánh phải `vr = 1.0 m/s` và khoảng cách hai bánh `L = 0.8 m`. Tính vận tốc thẳng `v`, vận tốc góc `omega` và bán kính quỹ đạo tròn `R = v / omega`.\nIn đúng 1 dòng `v=...m/s omega=...rad/s R=...m` (1 chữ số cho v/omega, 2 cho R).",
         """vl, vr, L = 0.6, 1.0, 0.8
v = (vr + vl) / 2.0
w = (vr - vl) / L
R = v / w
print(f"v={v:.1f}m/s omega={w:.1f}rad/s R={R:.2f}m")"""),

        ("L02", "Quy đổi độ phân giải encoder và ước lượng sai số trôi ngang",
         "Bánh xe đường kính `D = 0.2 m`, bộ mã hoá vòng quay `2000 xung/vòng`. Tính quãng đường mỗi xung (`mm/xung`) và độ lệch ngang sau `15 m` đi thẳng nếu hướng đầu xe bị lệch `2°`.\nIn đúng 1 dòng `mm_per_tick=... lateral_err_15m=...m` (3 chữ số).",
         """import math
mm_per_tick = math.pi * 0.2 * 1000.0 / 2000.0
lat_err = 15.0 * math.sin(math.radians(2.0))
print(f"mm_per_tick={mm_per_tick:.3f} lateral_err_15m={lat_err:.3f}m")"""),

        ("L03", "Tính mật độ khả năng đo Gauss ở 1 sigma so với 3 sigma",
         "Với mô hình cảm biến phân phối chuẩn (Gauss) `mu = 3.0 m, sigma = 0.2 m`, tính mật độ tại hai phép đo `z1 = 3.2 m` và `z3 = 3.6 m`, cùng tỉ số suy giảm `pdf_32 / pdf_36`.\nIn đúng 1 dòng `pdf_32=... pdf_36=... ratio=...x` (`pdf_32` lấy 3 chữ số `:.3f`, `pdf_36` lấy 4 chữ số `:.4f`, `ratio` lấy 1 chữ số `:.1f`).",
         """import math
pdf = lambda z, mu=3.0, s=0.2: math.exp(-0.5*((z-mu)/s)**2) / (s*math.sqrt(2*math.pi))
d1, d3 = pdf(3.2), pdf(3.6)
print(f"pdf_32={d1:.3f} pdf_36={d3:.4f} ratio={d1/d3:.1f}x")"""),

        ("L04", "Cập nhật hậu nghiệm bộ lọc Bayes rời rạc trên hành lang 8 ô",
         "Một hành lang vòng `8` ô (`0..7`) có cửa tại các ô `{2, 5}` và niềm tin tiên nghiệm đều `1/8`. Khi cảm biến báo thấy cửa (khả năng `0.85` tại ô có cửa, `0.15` tại ô tường), tính vector xác suất chuẩn hoá sau cập nhật.\nIn đúng 1 dòng `p_door2=... p_wall0=... sum=...` (3 chữ số, 1 chữ số cho sum).",
         """doors = {2, 5}
bel = [(1.0 / 8.0) * (0.85 if i in doors else 0.15) for i in range(8)]
tot = sum(bel)
bel = [b / tot for b in bel]
print(f"p_door2={bel[2]:.3f} p_wall0={bel[0]:.3f} sum={sum(bel):.1f}")"""),

        ("L05", "Tính ma trận Jacobian chuyển động cho lọc Kalman mở rộng (EKF)",
         "Với quãng đi `vh = 2.0 m` và góc hướng hiện tại `theta = 30°`, tính cặp đạo hàm riêng vị trí theo hướng `dx/dtheta = -vh*sin(theta)` và `dy/dtheta = vh*cos(theta)`.\nIn đúng 1 dòng `jac_theta=(dx_dth, dy_dth)` (3 chữ số).",
         """import math
vh, th = 2.0, math.radians(30.0)
dx_dth = -vh * math.sin(th)
dy_dth = vh * math.cos(th)
print(f"jac_theta=({dx_dth:.3f}, {dy_dth:.3f})")"""),

        ("L06", "Cập nhật xác suất ô lưới chiếm chỗ trên thang log-odds",
         "Một ô lưới ban đầu chưa biết gì (`l = 0`) nhận liên tiếp `4` phép đo thấy vật cản (`p_hit = 0.75`) rồi `1` phép đo tia đi qua (`p_miss = 0.35`). Cộng các giá trị log-odds tương ứng và chuyển ngược về xác suất.\nIn đúng 1 dòng `log_odds=... prob=...` (3 chữ số).",
         """import math
l = 0.0
for p in [0.75, 0.75, 0.75, 0.75, 0.35]:
    l += math.log(p / (1.0 - p))
prob = 1.0 / (1.0 + math.exp(-l))
print(f"log_odds={l:.3f} prob={prob:.3f}")"""),

        ("L07", "Đóng vòng đồ thị tư thế 1D phân bổ đều sai số trên 5 cạnh (4 đo + 1 đóng vòng)",
         "Robot ghi nhận `5` tư thế thô `[0.0, 1.0, 2.0, 3.0, 4.0]` qua `4` cạnh đo quãng đường, và có thêm `1` cạnh đóng vòng nối từ gốc tới điểm cuối đo được `3.5 m` (tổng cộng `5` cạnh đồng trọng số). Chia đều độ lệch đóng vòng cho cả `5` cạnh để tính hiệu chỉnh mỗi cạnh và cập nhật các tư thế.\nIn đúng 1 dòng `edge_corr=... corrected_poses=[...]` (`edge_corr` lấy 3 chữ số `:.3f`, từng toạ độ làm tròn `round(..., 3)`).",
         """raw = [0.0, 1.0, 2.0, 3.0, 4.0]; loop_meas = 3.5
err = loop_meas - raw[-1]
edge_corr = err / 5.0
corr = [round(raw[i] + i * edge_corr, 3) for i in range(5)]
print(f"edge_corr={edge_corr:.3f} corrected_poses={corr}")"""),

        ("L08", "So sánh độ bùng nổ kích thước lưới đều trên không gian 2D và 5 bậc tự do",
         "Giả sử mỗi trục toạ độ (mỗi chiều bậc tự do) chia `100` mức lưới. Tính số nút lưới trong mặt phẳng `2` chiều (`100^2`) và trên cánh tay `5` bậc tự do (`100^5`), cùng tỉ số phình lớn `grid_5dof // grid_2d`.\nIn đúng 1 dòng `grid_2d=... grid_5dof=... ratio=...` (`grid_5dof` viết dạng khoa học `:.0e`).",
         """g2 = 100 ** 2
g5 = 100 ** 5
print(f"grid_2d={g2} grid_5dof={g5:.0e} ratio={g5 // g2}")"""),

        ("L09", "Mô phỏng lăn mẫu quỹ đạo và chấm điểm cửa sổ động DWA",
         "Cho ba cặp vận tốc `(v, w)` ứng viên: `(0.6, 0.0)`, `(0.4, 0.5)`, `(0.2, -0.6)` lăn `dt = 1.0 s` từ gốc theo quy tắc `x, y, th = v*cos(w), v*sin(w), w`, hướng về đích `(2.0, 0.5)` và né vật cản `(1.2, 0.0)`. Tính điểm từng ứng viên gồm: căn hướng `head = max(0, 1 - |atan2(0.5 - y, 2.0 - x) - th| / pi)`, độ thoáng vật cản `clr = min(1.0, hypot(x - 1.2, y))`, tốc độ chuẩn hoá `v / 0.6`, tổng hợp `tot = round(0.4*head + 0.4*clr + 0.2*(v/0.6), 3)` và chọn cặp `(tot, (v, w))` lớn nhất.\nIn đúng 1 dòng `scores=[...] best=(score, (v, w))`.",
         """import math
cands = [(0.6, 0.0), (0.4, 0.5), (0.2, -0.6)]
scored = []
for v, w in cands:
    x, y, th = v * math.cos(w), v * math.sin(w), w
    head = max(0.0, 1.0 - abs(math.atan2(0.5 - y, 2.0 - x) - th) / math.pi)
    clr = min(1.0, math.hypot(x - 1.2, y - 0.0))
    tot = round(0.4 * head + 0.4 * clr + 0.2 * (v / 0.6), 3)
    scored.append((tot, (v, w)))
print(f"scores={scored} best={max(scored)}")"""),

        ("L10", "Tính độ cong và bán kính lái trong thuật toán Pure Pursuit",
         "Với khoảng nhìn trước `L = 2.5 m` và độ lệch ngang trong hệ xe `e_lat = 0.75 m`, tính độ cong quỹ đạo `kappa = 2 * e_lat / L^2` và bán kính vòng cua `1 / kappa`.\nIn đúng 1 dòng `curvature=... radius=...m` (2 chữ số).",
         """L, e = 2.5, 0.75
curv = 2.0 * e / (L * L)
radius = 1.0 / curv
print(f"curvature={curv:.2f} radius={radius:.2f}m")"""),

        ("L11", "Chiếu điểm 3D lên camera lỗ kim và tính toạ độ điểm ảnh u",
         "Một vật ở vị trí `(X = 0.8 m, Z = 5.0 m)` trước camera có tiêu cự ngang quy đổi điểm ảnh (`px`) là `fx = 600` và tâm ảnh `cx = 320`. Tính hoành độ điểm ảnh `u = fx * (X / Z) + cx` (làm tròn nguyên `:.0f`).\nIn đúng 1 dòng `u_px=...`.",
         """u = 600.0 * (0.8 / 5.0) + 320.0
print(f"u_px={u:.0f}")"""),

        ("L12", "Tính quãng dừng tối thiểu tính cả độ trễ điều khiển",
         "Robot chạy ở `v = 2.0 m/s`, gia tốc phanh tối đa `a = 1.6 m/s^2` và độ trễ hệ thống `td = 0.25 s`. Tính tổng quãng dừng `v^2/(2*a) + v*td`.\nIn đúng 1 dòng `stop_dist_m=...` (3 chữ số).",
         """v, a, td = 2.0, 1.6, 0.25
d_stop = (v * v) / (2.0 * a) + v * td
print(f"stop_dist_m={d_stop:.3f}")"""),

        ("L13", "Đối chiếu cột mốc 2004 -> 2005 và bước nhảy quãng dừng khi tăng tốc 20 -> 30 mph",
         "Tính quãng đường hoàn thành tối đa của chặng mở đầu năm 2004 (`5%` trên `142 dặm`), đối chiếu với quãng đường hoàn thành cuộc thi sa mạc năm 2005 (`132 dặm`), và tính tỉ lệ tăng quãng dừng đầy đủ (gồm phản ứng `v * 0.2` + phanh `v^2 / 8`, với `1 mph = 0.44704 m/s`) khi tăng tốc từ `20 mph` lên `30 mph`.\nIn đúng 1 dòng `mi_2004=... mi_2005=... stop_ratio=...x` (`mi_2004` 1 chữ số, `mi_2005` nguyên, `stop_ratio` 2 chữ số).",
         """stop_d = lambda mph: (v := mph * 0.44704) * 0.2 + (v ** 2) / 8.0
miles_2004 = 0.05 * 142
miles_2005 = 132
ratio_dist = stop_d(30.0) / stop_d(20.0)
print(f"mi_2004={miles_2004:.1f} mi_2005={miles_2005} stop_ratio={ratio_dist:.2f}x")"""),
    ],

    "GFX": [
        ("L00", "Tính thông lượng điểm ảnh và ngân sách khung hình ở 720p",
         "Cho độ phân giải `1280 × 720`, tính tổng số điểm ảnh mỗi giây ở `60 Hz`, cùng thời gian tối đa mỗi khung (đơn vị `ms`) tại `60 Hz` và `144 Hz`.\nIn đúng 1 dòng `px_60hz=... ms60=... ms144=...` (2 chữ số cho ms).",
         """px_frame = 1280 * 720
px_per_sec_60 = px_frame * 60
ms60, ms144 = 1000.0 / 60.0, 1000.0 / 144.0
print(f"px_60hz={px_per_sec_60} ms60={ms60:.2f} ms144={ms144:.2f}")"""),

        ("L01", "Nhân ma trận thuần nhất 3×3 chứng minh biến đổi 2D không giao hoán",
         "Dựng hai ma trận `3×3` đầy đủ: quay `R(90°)` và tịnh tiến `T(3, -1)`. Nhân lần lượt `(T * R) * [1, 2, 1]^T` và `(R * T) * [1, 2, 1]^T` rồi lấy hai toạ độ đầu `(x, y)` làm tròn thành số nguyên.\nIn đúng 1 dòng `T_after_R=(x, y) R_after_T=(x, y)`.",
         """def mv3(M, v):
    return tuple(round(sum(M[i][j]*v[j] for j in range(3)), 2) for i in range(3))
R = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
T = [[1, 0, 3], [0, 1, -1], [0, 0, 1]]
p = (1, 2, 1)
print(f"T_after_R={mv3(T, mv3(R, p))[:2]} R_after_T={mv3(R, mv3(T, p))[:2]}")"""),

        ("L02", "Chiếu phối cảnh và nội suy thuộc tính theo 1/z",
         "Chiếu hai điểm `(4, 2, 5)` và `(4, 2, 10)` với tiêu cự `f = 1.0`. Sau đó tính giá trị thuộc tính `u` đúng phối cảnh tại trung điểm màn hình (`t = 0.5`) nối hai đỉnh có `u0 = 0, z0 = 3` và `u1 = 1, z1 = 9` theo công thức nội suy `1/z`.\nIn đúng 1 dòng `at_z5=(...) at_z10=(...) persp_u=...` (3 chữ số thập phân cho `persp_u`).",
         """proj = lambda x, y, z, f=1.0: (round(f*x/z, 2), round(f*y/z, 2))
z0, z1, u0, u1, t = 3.0, 9.0, 0.0, 1.0, 0.5
num = (1 - t) * (u0 / z0) + t * (u1 / z1)
den = (1 - t) * (1.0 / z0) + t * (1.0 / z1)
print(f"at_z5={proj(4,2,5)} at_z10={proj(4,2,10)} persp_u={num/den:.3f}")"""),

        ("L03", "Ánh xạ toạ độ thiết bị chuẩn hoá NDC [-1, 1] sang pixel màn hình",
         "Cho màn hình rộng `W = 1280 px`, ánh xạ ba giá trị `x_ndc` trong `[-1.0, 0.25, 1.0]` sang chỉ số điểm ảnh `round((x + 1)/2 * W)`.\nIn đúng 1 dòng `ndc_to_px=[...]`.",
         """vp = lambda x, W=1280: round((x + 1.0) / 2.0 * W)
print(f"ndc_to_px={[vp(-1.0), vp(0.25), vp(1.0)]}")"""),

        ("L04", "Tính toạ độ trọng tâm tam giác trực tiếp từ ba hàm cạnh có hướng",
         "Cho tam giác có ba đỉnh `A = (0, 0), B = (6, 0), C = (0, 6)` và điểm thử `P = (1, 2)`. Viết hàm cạnh có hướng `edge(P, U, V) = (P_x - U_x)*(V_y - U_y) - (P_y - U_y)*(V_x - U_x)`, tính diện tích kép toàn tam giác `edge(C, A, B)` và chia để ra bộ ba trọng tâm `(l0, l1, l2)`.\nIn đúng 1 dòng `bary=(l0, l1, l2) inside=0/1` (2 chữ số).",
         """edge = lambda P, U, V: (P[0]-U[0])*(V[1]-U[1]) - (P[1]-U[1])*(V[0]-U[0])
A, B, C, P = (0, 0), (6, 0), (0, 6), (1, 2)
tot = edge(C, A, B)
l0 = edge(P, B, C) / tot
l1 = edge(P, C, A) / tot
l2 = edge(P, A, B) / tot
print(f"bary=({l0:.2f}, {l1:.2f}, {l2:.2f}) inside={int(min(l0, l1, l2) > 0)}")"""),

        ("L05", "Tính bước lượng tử bộ đệm độ sâu 24-bit từ công thức đạo hàm d_n",
         "Cho `far = 2000.0 m`, khoảng cách vật `z = 200.0 m` và độ sâu `24 bit`. Dùng công thức đạo hàm chính xác `dz = (z^2 * (f - n)) / (f * n * 2^24)` để tính bước phân giải nhỏ nhất (đổi ra `mm`) ở hai cấu hình `near = 0.1 m` và `near = 1.0 m`, cùng tỉ số cải thiện `gain`.\nIn đúng 1 dòng `dz_n01_mm=... dz_n10_mm=... gain=...x` (`2` chữ số thập phân cho `dz`, `1` chữ số cho `gain`).",
         """dz_mm = lambda z, n, f=2000.0, bits=24: (z*z*(f - n)) / (f * n * (1 << bits)) * 1000.0
d1, d2 = dz_mm(200.0, 0.1), dz_mm(200.0, 1.0)
print(f"dz_n01_mm={d1:.2f} dz_n10_mm={d2:.2f} gain={d1/d2:.1f}x")"""),

        ("L06", "Tính tích vô hướng Lambert và thành phần bóng sáng Blinn-Phong",
         "Cho vector pháp tuyến `n = (0.0, 0.6, 0.8)` và hướng đèn `l = (0.0, 0.8, 0.6)`. Tính trực tiếp tích vô hướng `max(0, sum(a*b))` cho ánh sáng khuếch tán, cùng độ sáng phản chiếu `(0.95)^64` và `(0.95)^128`.\nIn đúng 1 dòng `diffuse=... spec_s64=... spec_s128=...` (2 chữ số cho diffuse, 4 cho spec).",
         """n = (0.0, 0.6, 0.8); l = (0.0, 0.8, 0.6)
n_dot_l = max(0.0, sum(a * b for a, b in zip(n, l)))
spec64 = 0.95 ** 64
spec128 = 0.95 ** 128
print(f"diffuse={n_dot_l:.2f} spec_s64={spec64:.4f} spec_s128={spec128:.4f}")"""),

        ("L07", "Nội suy song tuyến 4 điểm và dung lượng bộ ảnh thu nhỏ giảm nửa",
         "Nội suy song tuyến tại `(u = 0.25, v = 0.5)` cho ô góc `c00=10, c10=30, c01=50, c11=70`, đồng thời tính số cấp ảnh từ `512 × 512` xuống `1 × 1` và tỉ lệ bộ nhớ tăng thêm.\nIn đúng 1 dòng `bilerp=... levels=... mip_extra_ratio=...` (`1` chữ số cho `bilerp`, `3` chữ số cho `mip_extra_ratio`).",
         """u, v = 0.25, 0.5
top = (1 - u) * 10 + u * 30
bot = (1 - u) * 50 + u * 70
bilerp = (1 - v) * top + v * bot
levels = len([512 >> k for k in range(10)])
ratios = sum(0.25 ** k for k in range(1, 10))
print(f"bilerp={bilerp:.1f} levels={levels} mip_extra_ratio={ratios:.3f}")"""),

        ("L08", "So sánh trộn màu thẳng trên sRGB với trộn tuyến tính đúng vật lý",
         "Tính giá trị ánh sáng tuyến tính thực tế của byte `160` (khi trung bình cộng thẳng hai byte sRGB `80` và `240`) và tính byte sRGB đúng ứng với mức ánh sáng tuyến tính `0.25` theo công thức đổi hai đoạn chuẩn sRGB.\nIn đúng 1 dòng `wrong_lin=... right_srgb=...` (3 chữ số thập phân cho `wrong_lin`).",
         """c = 160.0 / 255.0
lin_wrong = c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
right_lin = 0.25
right_srgb = round((1.055 * (right_lin ** (1.0 / 2.4)) - 0.055) * 255.0)
print(f"wrong_lin={lin_wrong:.3f} right_srgb={right_srgb}")"""),

        ("L09", "Giải phương trình bậc hai tìm giao điểm gần nhất của tia với mặt cầu",
         "Tia xuất phát từ gốc `(0, 0, 0)` hướng `(0, 0, 1)` bắn vào mặt cầu tâm `(0, 0, 7)` bán kính `R = 2`. Thiết lập và giải phương trình bậc hai `t^2 - 14t + 45 = 0` tìm hai nghiệm và chọn điểm chạm gần mắt nhất.\nIn đúng 1 dòng `hits=(t1, t2) nearest=...` (1 chữ số).",
         """import math
# t^2 - 14t + 45 = 0
b, c = -14.0, 45.0
disc = math.sqrt(b*b - 4.0*c)
t1, t2 = (-b - disc) / 2.0, (-b + disc) / 2.0
print(f"hits=({t1:.1f}, {t2:.1f}) nearest={min(t1, t2):.1f}")"""),

        ("L10", "Tính phản xạ Fresnel bằng xấp xỉ Schlick theo góc nhìn",
         "Cho vật liệu điện môi có `F0 = 0.04`, tính tỉ lệ phản xạ tại ba góc `cos_theta in {1.0, 0.5, 0.1}` bằng công thức `F0 + (1 - F0)*(1 - cos_theta)^5`.\nIn đúng 1 dòng `F0=... F60=... F84=...` (3 chữ số).",
         """schlick = lambda cos_t, F0=0.04: F0 + (1.0 - F0) * ((1.0 - cos_t) ** 5)
print(f"F0={schlick(1.0):.3f} F60={schlick(0.5):.3f} F84={schlick(0.1):.3f}")"""),

        ("L11", "Tính số mảnh tiết kiệm nhờ Early-Z trên khung 1280×720",
         "Trên khung `1280 × 720`, tính tổng số mảnh tô ở mức `overdraw = 4` so với sau khi sắp vẽ gần–xa + Early-Z (`1×`) và phần trăm giảm tải.\nIn đúng 1 dòng `overdraw4=... earlyZ=... saved_pct=...%` (1 chữ số).",
         """px = 1280 * 720
print(f"overdraw4={px * 4} earlyZ={px} saved_pct={(1 - 1/4)*100:.1f}%")"""),

        ("L12", "Tính bước lượng tử độ sâu ở z=1000 m theo công thức đạo hàm đầy đủ",
         "Ở khoảng cách `z = 1000.0 m`, `far = 10000.0 m`, `24 bit`, dùng công thức đạo hàm đầy đủ `(z^2*(f-n))/(f*n*2^24)` so sánh cấu hình `near = 0.02 m` với `near = 1.00 m`.\nIn đúng 1 dòng `dz_n002=...m dz_n100=...m` (2 chữ số).",
         """dz = lambda z, n, f=10000.0: (z*z*(f - n)) / (f * n * (1 << 24))
print(f"dz_n002={dz(1000.0, 0.02):.2f}m dz_n100={dz(1000.0, 1.00):.2f}m")"""),

        ("L13", "Đối chiếu bóng sáng Phong và tốc độ giảm nhiễu Monte Carlo",
         "Tính giá trị phản chiếu Phong `0.92^32` và hệ số giảm độ lệch chuẩn nhiễu khi tăng số tia mẫu từ `4` lên `100` (`sqrt(100 / 4)`).\nIn đúng 1 dòng `phong=... mc_noise_reduction=...x` (3 chữ số cho phong, 1 cho ratio).",
         """phong = 0.92 ** 32
mc_err_ratio = (100.0 / 4.0) ** 0.5
print(f"phong={phong:.3f} mc_noise_reduction={mc_err_ratio:.1f}x")"""),
    ],

    "BCH": [
        ("L00", "Áp dụng cây câu hỏi quyết định nhu cầu chuỗi khối cho 5 công ty đối thủ",
         "Cho điều kiện dùng chung sổ cái: `need = shared_state and multi_writers and (not trusted_ttp) and (not mutual_trust)`. So sánh chi phí vận hành giữa `1` máy chủ trung tâm tin cậy với ngưỡng đồng thuận quá bán `n // 2 + 1` cho mạng `n = 5` công ty đối thủ, và kiểm tra hai tình huống (có bên tin cậy vs không có bên tin cậy).\nIn đúng 1 dòng `central_ops=... maj_quorum_5=... school_need=0/1 rivals_need=0/1`.",
         """need = lambda s, w, ttp, trust: s and w and (not ttp) and (not trust)
central_ops = 1
maj_quorum = (5 // 2) + 1
n_sch = int(need(True, True, True, False))
n_riv = int(need(True, True, False, False))
print(f"central_ops={central_ops} maj_quorum_5={maj_quorum}",
      f"school_need={n_sch} rivals_need={n_riv}")"""),

        ("L01", "Dựng chuỗi băm SHA-256 4 khối và phát hiện sửa đổi dữ liệu",
         "Dùng `hashlib.sha256` tạo chuỗi `4` khối nối đuôi từ danh sách `['khối 0', 'A->B 10', 'B->C 4', 'C->A 3']` (bắt đầu bằng `prev = '0'*10`, mỗi khối băm `prev + '|' + data`, lấy 10 ký tự hex đầu). Thử sửa khối chỉ số `2` thành `'B->C 40'` và tính lại phần đuôi để xem có bao nhiêu khối đổi mã.\nIn đúng 1 dòng `orig_b2=... tampered_b2=... broken_blocks=...`.",
         """import hashlib
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:10]
data = ["khối 0", "A->B 10", "B->C 4", "C->A 3"]
chain = []; p = "0" * 10
for d in data: p = h(f"{p}|{d}"); chain.append(p)
tampered = list(chain); p = chain[1]
for i in (2, 3):
    txt = "B->C 40" if i == 2 else data[i]
    p = h(f"{p}|{txt}"); tampered[i] = p
diff = sum(1 for a, b in zip(chain, tampered) if a != b)
print(f"orig_b2={chain[2]} tampered_b2={tampered[2]} broken_blocks={diff}")"""),

        ("L02", "Tính độ dài và dung lượng bằng chứng Merkle cho khối 4096 giao dịch",
         "Cho khối gồm `4096` giao dịch (mỗi mã băm SHA-256 dài `32` byte). Tính số mã băm anh em `log2(4096)` và tổng kích thước bằng chứng theo byte.\nIn đúng 1 dòng `merkle_hashes=... proof_bytes=...`.",
         """import math
proof_hashes = int(math.log2(4096))
proof_bytes = proof_hashes * 32
print(f"merkle_hashes={proof_hashes} proof_bytes={proof_bytes}")"""),

        ("L03", "Ký SHA-256 và kiểm chứng chữ ký số trên mô hình RSA đồ chơi",
         "Với cặp khoá hệ mật mã bất đối xứng RSA (Rivest–Shamir–Adleman) đồ chơi `(n = 3233, e = 17, d = 2753)`, lấy mã băm `m = int(hashlib.sha256('A trả B 15'.encode()).hexdigest(), 16) % n` rồi ký `sig = pow(m, d, n)`. Kiểm định chữ ký cho tin gốc (`m`) và cho tin bị sửa (`'A trả B 150'`).\nIn đúng 1 dòng `sig_valid=0/1 tampered_valid=0/1`.",
         """import hashlib
n, e, d = 3233, 17, 2753
h_mod = lambda s: int(hashlib.sha256(s.encode()).hexdigest(), 16) % n
m = h_mod("A trả B 15")
sig = pow(m, d, n)
ok_orig = (pow(sig, e, n) == m)
ok_tampered = (pow(sig, e, n) == h_mod("A trả B 150"))
print(f"sig_valid={int(ok_orig)} tampered_valid={int(ok_tampered)}")"""),

        ("L04", "Kiểm bất biến tổng đầu vào và tiền thừa trong giao dịch đầu ra chưa tiêu (UTXO)",
         "Một giao dịch gom hai đồng xu chưa tiêu trị giá `7.0` và `4.0` (tính bằng đơn vị xu `[700, 400]` tránh sai số thực) để trả `8.5` (`850` xu) và đóng phí `0.2` (`20` xu). Tính tổng đầu vào và tiền thừa.\nIn đúng 1 dòng `in_sum=... change=...` (1 chữ số).",
         """inputs = [700, 400]; pay = 850; fee = 20
change = sum(inputs) - pay - fee
print(f"in_sum={sum(inputs)/100:.1f} change={change/100:.1f}")"""),

        ("L05", "Đào thử Bằng chứng Công việc PoW tìm SHA-256 mở đầu bằng '00'",
         "Tăng `nonce` từ `0` trên chuỗi byte `f'khoi-99:{nonce}'.encode()` cho tới khi `hashlib.sha256(...).hexdigest()` bắt đầu bằng `'00'` (độ khó `8 bit 0`).\nIn đúng 1 dòng `found_nonce=... hash_prefix=...`.",
         """import hashlib
nonce = 0
while True:
    d = hashlib.sha256(f"khoi-99:{nonce}".encode()).hexdigest()
    if d.startswith("00"): break
    nonce += 1
print(f"found_nonce={nonce} hash_prefix={d[:6]}")"""),

        ("L06", "Tính xác suất kẻ tấn công đuổi kịp sau z khối (Nakamoto)",
         "Cài hàm xác suất đuổi kịp theo mục 11 sách trắng Bitcoin cho hai kịch bản mới: `(q = 0.15, z = 6)` và `(q = 0.25, z = 4)`.\nIn đúng 1 dòng `p_q15_z6=... p_q25_z4=...` (5 chữ số cho p1, 4 cho p2).",
         """import math
def attacker_p(q, z):
    p = 1.0 - q; lam = z * (q / p); s = 1.0
    for k in range(z + 1):
        pois = math.exp(-lam) * (lam ** k) / math.factorial(k)
        s -= pois * (1.0 - (q / p) ** (z - k))
    return s
print(f"p_q15_z6={attacker_p(0.15, 6):.5f} p_q25_z4={attacker_p(0.25, 4):.4f}")"""),

        ("L07", "Tính ngưỡng chịu lỗi Byzantine (BFT) và số phiếu chốt cho cụm 16 bên xác thực (validator)",
         "Cho mạng gồm `N = 16` validator, tính số nút lỗi tối đa chịu được `f = (N - 1) // 3` và ngưỡng phiếu đa số hai phần ba `quorum = N - f`.\nIn đúng 1 dòng `max_byzantine=... quorum_2_3=...`.",
         """n = 16; f = (n - 1) // 3; quorum = n - f
print(f"max_byzantine={f} quorum_2_3={quorum}")"""),

        ("L08", "Tính phí giao dịch hợp đồng từ số lượng gas và giá mỗi gas",
         "Một lời gọi hợp đồng tiêu thụ `75_000` đơn vị gas với mức giá `40 gwei` (`1 gwei = 10^-9 ETH`). Tính tổng phí tính theo `ETH`.\nIn đúng 1 dòng `fee_eth=...` (5 chữ số thập phân).",
         """gas, gwei = 75_000, 40
eth_fee = gas * gwei * 1e-9
print(f"fee_eth={eth_fee:.5f}")"""),

        ("L09", "Mô phỏng lỗi gọi lại (Reentrancy) và bản sửa Checks-Effects-Interactions",
         "Cài lớp `Vault(pool=10, safe=...)` và `Attacker` có phương thức `recv(self, vault)` tự gọi lại `vault.withdraw(self)`. Chạy kịch bản kẻ gửi `2` đồng rút từ kho `10` đồng ở hai chế độ: `safe=False` (gửi tiền trước khi trừ số dư) và `safe=True` (trừ số dư trước khi gọi ra ngoài).\nIn đúng 1 dòng `unsafe_stolen=... safe_withdrawn=...`.",
         """class Vault:
    def __init__(self, pool, safe):
        self.pool, self.safe, self.bal = pool, safe, 2
    def withdraw(self, who):
        if self.bal <= 0 or self.pool < 2: return
        if self.safe: self.bal = 0; self.pool -= 2; who.recv(self)
        else: self.pool -= 2; who.recv(self); self.bal = 0
class Attacker:
    def __init__(self): self.got = 0
    def recv(self, v): self.got += 2; v.withdraw(self)
def run(safe):
    v, a = Vault(10, safe), Attacker(); v.withdraw(a); return a.got
print(f"unsafe_stolen={run(False)} safe_withdrawn={run(True)}")"""),

        ("L10", "Tính thông lượng giao dịch mỗi giây tối đa (TPS) của khối chuỗi gốc 2 MB",
         "Cho chuỗi gốc tạo khối `2_000_000` byte cứ mỗi `600` giây, kích thước trung bình mỗi giao dịch là `400` byte. Tính giới hạn TPS lý thuyết.\nIn đúng 1 dòng `max_tps=...` (2 chữ số).",
         """tps = 2_000_000 / 400 / 600
print(f"max_tps={tps:.2f}")"""),

        ("L11", "Kiểm định độ bền trung vị của Oracle 9 nguồn trước 4 nguồn nhiễu",
         "Cho 9 nguồn giá `[199, 200, 202, 203, 204, 9999, 9999, 9999, 9999]` trong đó có `4` nguồn bị phá hoại báo `9999`. Sắp xếp và lấy phần tử trung vị, kiểm chứng kết quả vẫn nằm trong dải thật `[199..204]`.\nIn đúng 1 dòng `median_price=... safe_in_band=0/1`.",
         """vals = sorted([199, 200, 202, 203, 204, 9999, 9999, 9999, 9999])
med = vals[len(vals) // 2]
print(f"median_price={med} safe_in_band={int(199 <= med <= 204)}")"""),

        ("L12", "So sánh dung lượng tiêu đề 80 byte/khối với dữ liệu đầy khối ở tốc độ 5 khối/giờ",
         "Xét mạng tạo trung bình `5` khối mỗi giờ trong `1` năm (`5 * 24 * 365 = 43_800` khối). Tính tổng dung lượng 1 năm nếu chỉ tải tiêu đề `80 byte` (tính bằng `MB`, 2 chữ số) so với tải đủ cả khối `1_000_000 byte` (tính bằng `GB`, 2 chữ số), cùng tỉ số thu gọn (`:.0f`).\nIn đúng 1 dòng `blocks_yr=... header_MB=... full_GB=... ratio=...x`.",
         """blocks_yr = 5 * 24 * 365
hdr_mb = 80 * blocks_yr / 1e6
full_gb = 1_000_000 * blocks_yr / 1e9
ratio = 1_000_000 / 80
print(f"blocks_yr={blocks_yr} header_MB={hdr_mb:.2f}",
      f"full_GB={full_gb:.2f} ratio={ratio:.0f}x")"""),
    ],
}

want = {a.upper() for a in sys.argv[1:]}
for course, labs in DATA.items():
    if want and course not in want:
        continue
    for lid, hint, de_body, sol in labs:
        key = f"{course}:{lid}"
        de_md = f"# Lab {course} {lid} — {hint}\n\n{de_body}\n\nChấm tự động:\n```bash\nbash labs/cham.sh {course} {lid} duong_dan/bai_cua_ban.py\n```\n"
        common.upgrade_lesson(
            course, lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS[key],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger(course, default_lang="python")
    for lid, _, _, sol in labs:
        common.sync_practice_run_blocks(course, lid, sol)
    print(f"=== {course}: {len(labs)} bài OK, ledger={nblk} blocks ===", flush=True)

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for c in DATA:
    if want and c not in want:
        continue
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
    ):
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"
print("ALL S11 (RBM/ESY/ROB/GFX/BCH = 75 LESSONS) PASSED!", flush=True)
