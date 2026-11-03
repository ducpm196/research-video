"""Hình cho khoá RBM — mọi toạ độ, đường cong tính từ checklib (alg.*), không vẽ tay.
Theo skill dataviz: một trục y; chuỗi màu theo thứ tự cố định của bảng mặc định (xanh #2a78d6, cam #eb6834 — đã kiểm
validate_palette.js ở NET: ALL PASS, CVD ΔE 24,7); chuỗi thứ hai thêm nét đứt (mã hoá phụ); đường tham chiếu màu xám mờ;
nhãn đặt trực tiếp, chữ màu mực (không dùng màu chuỗi); nền bảng #fffbeb. Video là khung tĩnh nên không có lớp hover.
Chạy: .venv/Scripts/python audit/rbm/figs.py → audit/rbm/fig/*.svg (mỗi hình một dòng)."""
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "rbm" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Plane:
    """Mặt phẳng toạ độ: (x, y) toán học → pixel, cùng tỉ lệ hai trục (geom=True) hoặc tỉ lệ riêng (biểu đồ)."""

    def __init__(self, W, H, xr, yr, pad=(70, 30, 40, 60), geom=True):
        self.W, self.H, (self.x0, self.x1), (self.y0, self.y1) = W, H, xr, yr
        L, R, T, B = pad
        sx, sy = (W - L - R) / (xr[1] - xr[0]), (H - T - B) / (yr[1] - yr[0])
        if geom:
            sx = sy = min(sx, sy)
        self.sx, self.sy, self.L, self.T, self.B = sx, sy, L, T, B
        self.out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
                    '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" '
                    f'orient="auto"><path d="M0,0 L18,9 L0,18 z" fill="{INK}"/></marker>'
                    '<marker id="ab" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" '
                    f'orient="auto"><path d="M0,0 L18,9 L0,18 z" fill="{S1}"/></marker>'
                    '<marker id="ao" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" '
                    f'orient="auto"><path d="M0,0 L18,9 L0,18 z" fill="{S2}"/></marker></defs>']

    def X(self, x):
        return self.L + (x - self.x0) * self.sx

    def Y(self, y):
        return self.T + (self.y1 - y) * self.sy

    def add(self, s):
        self.out.append(s)

    def line(self, a, b, col=INK, w=3, dash=None, arrow=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{arrow})"' if arrow else ""
        self.add(f'<line x1="{self.X(a[0]):.1f}" y1="{self.Y(a[1]):.1f}" x2="{self.X(b[0]):.1f}" y2="{self.Y(b[1]):.1f}" '
                 f'stroke="{col}" stroke-width="{w}"{d}{m}/>')

    def poly(self, pts, col, w=3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self.add(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="{w}"{d} stroke-linejoin="round"/>')

    def dot(self, p, col, r=7):
        self.add(f'<circle cx="{self.X(p[0]):.1f}" cy="{self.Y(p[1]):.1f}" r="{r}" fill="{col}" stroke="{BG}" stroke-width="2"/>')

    def text(self, p, t, dx=0, dy=0, size=22, col=INK, anchor="middle", halo=True):
        h = f' stroke="{BG}" stroke-width="6" paint-order="stroke"' if halo else ""
        self.add(f'<text x="{self.X(p[0]) + dx:.1f}" y="{self.Y(p[1]) + dy:.1f}" font-size="{size}" fill="{col}" '
                 f'text-anchor="{anchor}"{h}>{esc(t)}</text>')

    def arc(self, r, a0, a1, col=MUTED, w=2.5, arrow=None, center=(0, 0)):
        """Cung tròn bán kính r (đơn vị toán) từ góc a0 tới a1 (độ, ngược chiều kim đồng hồ)."""
        n = max(8, int(abs(a1 - a0) / 4))
        pts = [(center[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                center[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        p = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        m = f' marker-end="url(#{arrow})"' if arrow else ""
        self.add(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="{w}"{m}/>')

    def axes(self, ticks=True, labels=("x", "y"), step=1):
        self.line((self.x0, 0), (self.x1, 0), MUTED, 2, arrow="ar")
        self.line((0, self.y0), (0, self.y1), MUTED, 2, arrow="ar")
        self.text((self.x1, 0), labels[0], dx=-6, dy=30, col=MUTED)
        self.text((0, self.y1), labels[1], dx=-22, dy=14, col=MUTED)
        if ticks:
            k = math.ceil(self.x0)
            while k < self.x1:
                if k != 0 and k % step == 0:
                    self.line((k, -0.06 / self.sy * 100), (k, 0.06 / self.sy * 100), MUTED, 2)
                    self.text((k, 0), str(k), dy=30, size=19, col=MUTED)
                k += 1
            k = math.ceil(self.y0)
            while k < self.y1:
                if k != 0 and k % step == 0:
                    self.line((-0.06 / self.sx * 100, k), (0.06 / self.sx * 100, k), MUTED, 2)
                    self.text((0, k), str(k), dx=-18, dy=7, size=19, col=MUTED, anchor="end")
                k += 1

    def svg(self):
        return "".join(self.out) + "</svg>"


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def vn(x, d=2):
    """Số thập phân kiểu Việt (dấu phẩy)."""
    s = f"{x:.{d}f}".rstrip("0").rstrip(".") if d else f"{x:.0f}"
    return s.replace(".", ",").replace("-", "−")


# ───────── L00: quay điểm (1, 0) đi 90° ─────────
def l00_rot():
    P = Plane(620, 420, (-1.6, 1.8), (-0.6, 1.6))
    P.axes(ticks=False)
    P.arc(1, 0, 360, GRID, 2)
    P.line((0, 0), (1, 0), S1, 4, arrow="ab")
    q = alg.rot2(90) @ [1, 0]
    P.line((0, 0), tuple(q), S2, 4, dash="12 7", arrow="ao")
    P.arc(0.45, 4, 86, MUTED, 2.5, arrow="ar")
    P.text((0.42, 0.42), "90°", dx=24, dy=0, size=22)
    P.text((1, 0), "(1, 0)", dx=8, dy=-16, anchor="start")
    P.text(tuple(q), "(0, 1)", dx=16, dy=-8, anchor="start")
    P.dot((1, 0), S1)
    P.dot(tuple(q), S2)
    return P.svg()


def l00_rot30():
    """Điểm (2, 1) quay 30° — số trên hình lấy từ alg.rot2."""
    P = Plane(620, 420, (-0.8, 2.8), (-0.6, 2.6))
    P.axes()
    p = (2, 1)
    q = alg.rot2(30) @ p
    P.line((0, 0), p, S1, 4, arrow="ab")
    P.line((0, 0), tuple(q), S2, 4, dash="12 7", arrow="ao")
    a0 = math.degrees(math.atan2(1, 2))
    P.arc(0.9, a0 + 2, a0 + 28, MUTED, 2.5, arrow="ar")
    P.text((0.95, 0.9), "30°", dx=10, dy=8, size=22, anchor="start")
    P.text(p, "(2, 1)", dx=10, dy=8, anchor="start")
    P.text(tuple(q), f"({vn(q[0], 3)}; {vn(q[1], 3)})", dx=12, dy=-10, anchor="start")
    P.dot(p, S1)
    P.dot(tuple(q), S2)
    return P.svg()


# ───────── L03: hai thứ tự ghép quay và tịnh tiến ─────────
def l03_order():
    P = Plane(760, 430, (-0.8, 3.6), (-0.6, 3.5))
    P.axes(ticks=False)
    a = (1, 0)
    r = tuple(alg.rot2(90) @ a)                         # quay trước: (0, 1)
    rt = tuple(alg.homog2(90, 2, 0) @ [1, 0, 1])[:2]     # rồi tịnh tiến (2, 0): (2, 1)
    t = (a[0] + 2, a[1])                                 # tịnh tiến trước: (3, 0)
    tr = tuple(alg.rot2(90) @ t)                         # rồi quay: (0, 3)
    P.line(a, r, S1, 3, dash="2 7", arrow="ab")
    P.line(r, rt, S1, 3.5, arrow="ab")
    P.line(a, t, S2, 3, dash="12 7", arrow="ao")
    P.arc(3, 2, 88, S2, 3, arrow="ao")
    for p, lab, dx, dy, an in ((a, "(1, 0)", 0, 34, "middle"), (r, "(0, 1)", -14, -10, "end"), (rt, "(2, 1)", 12, -10, "start"),
                               (t, "(3, 0)", 0, 34, "middle"), (tr, "(0, 3)", -14, 6, "end")):
        P.dot(p, INK, 6)
        P.text(p, lab, dx=dx, dy=dy, anchor=an)
    P.text((1.0, 1.0), "① quay rồi tịnh tiến", dy=-16, size=20)
    P.text((2.3, 2.3), "② tịnh tiến rồi quay", dx=10, size=20, anchor="start")
    return P.svg()


# ───────── L04–L06: tay máy hai khâu ─────────
def arm(P, t1, t2, col, dash=None, lab=True, elbow_lab=None):
    e, tip = alg.fk2(1, 1, t1, t2)
    P.line((0, 0), e, col, 7, dash)
    P.line(e, tip, col, 7, dash)
    P.dot((0, 0), INK, 9)
    P.dot(e, col, 8)
    P.dot(tip, col, 8)
    return e, tip


def l04_fk():
    P = Plane(660, 470, (-0.5, 2.0), (-0.4, 1.9))
    P.axes(step=1)
    e, tip = arm(P, 30, 60, S1)
    P.arc(0.35, 2, 28, MUTED, 2.5, arrow="ar")
    P.text((0.4, 0.1), "θ₁ = 30°", dx=10, dy=4, size=21, anchor="start")
    # θ2 đo từ phần kéo dài của khâu 1
    ext = (e[0] + 0.45 * math.cos(math.radians(30)), e[1] + 0.45 * math.sin(math.radians(30)))
    P.line(e, ext, MUTED, 2, dash="6 6")
    P.arc(0.3, 32, 88, MUTED, 2.5, arrow="ar", center=e)
    P.text(e, "θ₂ = 60°", dx=58, dy=-4, size=21, anchor="start")
    P.text(tip, f"({vn(tip[0], 3)}; {vn(tip[1], 3)})", dx=14, dy=-6, anchor="start")
    P.text(e, "khuỷu", dx=14, dy=24, size=20, col=MUTED, anchor="start")
    P.text((0.43, 0.25), "L₁ = 1", dx=-4, dy=-14, size=20, col=MUTED, anchor="end")
    P.text(((e[0] + tip[0]) / 2, (e[1] + tip[1]) / 2), "L₂ = 1", dx=-14, dy=0, size=20, col=MUTED, anchor="end")
    return P.svg()


def l05_ik():
    P = Plane(660, 470, (-0.7, 2.0), (-0.4, 1.9))
    P.axes(ticks=False)
    sols = alg.ik2(1, 1, *alg.fk2(1, 1, 30, 60)[1])
    (a1, b1), (a2, b2) = sols
    e1, tip = arm(P, a1, b1, S1)
    e2, _ = arm(P, a2, b2, S2, dash="12 8")
    P.text(e1, f"({vn(a1, 0)}°, {vn(b1, 0)}°)", dx=16, dy=22, size=21, anchor="start")
    P.text(e2, f"({vn(a2, 0)}°, {vn(b2, 0)}°)", dx=-14, dy=-8, size=21, anchor="end")
    P.text(tip, "đích", dx=14, dy=-8, anchor="start")
    return P.svg()


def l05_reach():
    """Vùng với tới của L1 = 2, L2 = 1: vành khuyên 1 ≤ r ≤ 3; điểm (4, 0) ngoài tầm, (0,5; 0) trong lỗ."""
    P = Plane(660, 470, (-3.4, 4.6), (-3.3, 3.4))
    P.add(f'<path d="M{P.X(3):.1f},{P.Y(0):.1f} A{3 * P.sx:.1f},{3 * P.sy:.1f} 0 1,0 {P.X(-3):.1f},{P.Y(0):.1f} '
          f'A{3 * P.sx:.1f},{3 * P.sy:.1f} 0 1,0 {P.X(3):.1f},{P.Y(0):.1f} Z M{P.X(1):.1f},{P.Y(0):.1f} '
          f'A{P.sx:.1f},{P.sy:.1f} 0 1,1 {P.X(-1):.1f},{P.Y(0):.1f} A{P.sx:.1f},{P.sy:.1f} 0 1,1 {P.X(1):.1f},{P.Y(0):.1f} Z" '
          f'fill="{S1}" fill-opacity="0.16" fill-rule="evenodd" stroke="{S1}" stroke-width="2.5"/>')
    P.axes(ticks=False)
    for k in (1, 3):
        P.text((k, 0), str(k), dx=10, dy=26, size=19, col=MUTED, anchor="start")
    P.dot((4, 0), S2, 8)
    P.text((4, 0), "(4, 0)", dy=-16)
    P.dot((0.5, 0), S2, 8)
    P.text((0.5, 0), "(0,5; 0)", dy=-16, size=20)
    P.text((0, 2.2), "với tới được", size=21)
    return P.svg()


def l06_sing():
    P = Plane(760, 420, (-0.4, 2.9), (-0.4, 1.6))
    P.axes(ticks=False)
    e, tip = arm(P, 20, 0, S1)
    c, s_ = math.cos(math.radians(20)), math.sin(math.radians(20))
    P.text(e, "θ₂ = 0: duỗi thẳng", dx=10, dy=34, size=21, anchor="start")
    up = (tip[0] - 0.5 * s_, tip[1] + 0.5 * c)
    P.line(tip, up, S2, 3.5, arrow="ao")
    P.text(up, "đi được (vuông góc với tay)", dx=-10, dy=-12, size=20, anchor="end")
    out = (tip[0] + 0.5 * c, tip[1] + 0.5 * s_)
    P.line(tip, out, MUTED, 3, dash="5 7", arrow="ar")
    P.text(out, "không đi được (dọc tay)", dx=-30, dy=36, size=20, col=MUTED, anchor="start")
    return P.svg()


# ───────── biểu đồ thời gian ─────────
class Chart(Plane):
    def __init__(self, W, H, xr, yr, xstep, ystep, xlab, ylab, fmt=vn, pad=(80, 40, 50, 66), xstart=None):
        super().__init__(W, H, xr, yr, pad=pad, geom=False)
        x = xr[0] if xstart is None else xstart
        while x <= xr[1] + 1e-9:
            self.add(f'<text x="{self.X(x):.1f}" y="{self.Y(yr[0]) + 30:.1f}" font-size="19" fill="{MUTED}" text-anchor="middle">{fmt(x)}</text>')
            x += xstep
        y = yr[0]
        while y <= yr[1] + 1e-9:
            self.add(f'<line x1="{self.X(xr[0]):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(xr[1]):.1f}" y2="{self.Y(y):.1f}" stroke="{GRID}" stroke-width="1.5"/>')
            self.add(f'<text x="{self.X(xr[0]) - 12:.1f}" y="{self.Y(y) + 7:.1f}" font-size="19" fill="{MUTED}" text-anchor="end">{fmt(y)}</text>')
            y += ystep
        self.line((xr[0], yr[0]), (xr[1], yr[0]), MUTED, 2)
        self.add(f'<text x="{self.X(xr[1]):.1f}" y="{H - 6}" font-size="19" fill="{MUTED}" text-anchor="end">{esc(xlab)}</text>')
        self.add(f'<text x="{self.X(xr[0]) - 60:.1f}" y="{self.T - 14:.1f}" font-size="19" fill="{MUTED}" text-anchor="start">{esc(ylab)}</text>')


def l07_euler():
    C = Chart(900, 430, (0, 1), (0.3, 1.0), 0.2, 0.1, "thời gian t", "x(t)")
    ex = [(k / 100, math.exp(-k / 100)) for k in range(101)]
    C.poly(ex, MUTED, 3)
    xs = alg.euler_ode(lambda t, x: -x, 1.0, 0.1, 10)
    pts = [(k * 0.1, v) for k, v in enumerate(xs)]
    C.poly(pts, S1, 3)
    for p in pts:
        C.dot(p, S1, 6)
    C.text((0.55, 0.62), f"đúng: e mũ −t, tại t = 1 là {vn(math.exp(-1), 4)}", size=20, anchor="start")
    C.text((0.45, 0.47), f"Euler h = 0,1: {vn(xs[-1], 4)}", size=20, anchor="end")
    return C.svg()


def l10_pid():
    C = Chart(900, 430, (0, 5), (0, 1.2), 1, 0.2, "thời gian t (giây)", "x(t)")
    C.line((0, 1), (5, 1), MUTED, 2, dash="6 6")
    C.text((0.1, 1), "đích r = 1", dx=0, dy=-10, size=19, col=MUTED, anchor="start")
    for kp, ki, col, dash, lab, dy in ((4, 0, S1, None, "chỉ P, K = 4: dừng ở 0,8", 30), (4, 4, S2, "12 7", "P + I: về 1", -14)):
        pts, x, integ = [], 0.0, 0.0
        h = 0.001
        for k in range(5001):
            if k % 50 == 0:
                pts.append((k * h, x))
            e = 1 - x
            integ += e * h
            x += h * (-x + kp * e + ki * integ)
        C.poly(pts, col, 3, dash)
        C.text((5, pts[-1][1]), lab, dx=-6, dy=dy, size=20, anchor="end")
    return C.svg()


def l11_steps():
    C = Chart(900, 430, (0, 6), (-3, 3), 1, 1, "bước k", "giá trị x ở bước k", fmt=lambda v: vn(v, 0))
    for h, col, dash, lab, dy in ((0.25, S2, "12 7", "h = 0,25: nhân −1,5 mỗi bước", 0), (0.05, S1, None, "h = 0,05: nhân 0,5", 0)):
        xs = alg.euler_ode(lambda t, x: -10 * x, 1.0, h, 6)
        pts = [(k, max(-3, min(3, v))) for k, v in enumerate(xs)]
        C.poly(pts, col, 3, dash)
        for p in pts:
            C.dot(p, col, 6)
    C.text((0.2, -2.5), "h = 0,25: nhân −1,5 mỗi bước", size=20, anchor="start")
    C.text((3.2, 0.3), "h = 0,05: nhân 0,5", dy=-12, size=20, anchor="start")
    return C.svg()


def l12_fuse():
    C = Chart(900, 430, (-3, 4), (0, 0.6), 1, 0.1, "vị trí", "mật độ", fmt=lambda v: vn(v, 1))
    g = lambda m, v: [(x / 50, math.exp(-(x / 50 - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)) for x in range(-150, 201)]
    K, m, v = alg.kalman1d_update(0, 1, 1, 1)
    C.poly(g(0, 1), S1, 3)
    C.poly(g(1, 1), S2, 3, "12 7")
    C.poly(g(m, v), INK, 3.5)
    C.text((-2.9, 0.47), "dự đoán 0, phương sai 1", size=19, anchor="start")
    C.text((3.95, 0.47), "phép đo 1, phương sai 1", size=19, anchor="end")
    C.text((m, max(y for _, y in g(m, v))), f"kết hợp {vn(m)}, phương sai {vn(v)}", dy=-12, size=20)
    return C.svg()


def l14_alias():
    C = Chart(900, 420, (0, 1), (-1.0, 1.0), 0.1, 0.5, "thời gian t (giây)", "tín hiệu", fmt=lambda v: vn(v, 1), pad=(80, 40, 96, 66))
    C.poly([(k / 1000, math.cos(2 * math.pi * 7 * k / 1000)) for k in range(1001)], "#9ca3af", 2)
    C.poly([(k / 1000, math.cos(2 * math.pi * 3 * k / 1000)) for k in range(1001)], S2, 3, "12 7")
    for n in range(11):
        C.dot((n / 10, math.cos(2 * math.pi * 7 * n / 10)), S1, 8)
    C.text((0.0, 1.0), "xám: tín hiệu thật 7 Hz;  chấm xanh: mẫu 10 lần mỗi giây;  cam: 3 Hz đi qua đúng các mẫu", dy=-58, size=19, anchor="start")
    return C.svg()


def l16_fit():
    xs, ys = [0, 1, 2, 3], [1, 3, 5.1, 6.9]
    a, b, *_ = alg.lsq_line(xs, ys)
    C = Chart(760, 430, (0, 3.5), (0, 8), 0.5, 2, "giá trị chuẩn x", "số đọc y", fmt=lambda v: vn(v, 1))
    C.poly([(0, b), (3.5, a * 3.5 + b)], S1, 3)
    for x, y in zip(xs, ys):
        C.line((x, y), (x, a * x + b), S2, 2.5)
        C.dot((x, y), S2, 8)
    C.text((3.45, a * 3.45 + b), f"y = {vn(a)}x + {vn(b)}", dx=-8, dy=34, size=20, anchor="end")
    return C.svg()


# ───────── L15: lưới A* ─────────
def l15_grid(show_order=True, show_path=True):
    grid = ["....", ".##.", "...."]
    cost, path, order = alg.astar_grid(grid, (1, 0), (1, 3))
    cs, L, T = 110, 40, 30
    W, H = L * 2 + cs * 4, T * 2 + cs * 3
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            fill = "#4b5563" if ch == "#" else ("#dbeafe" if show_path and (r, c) in path else "#ffffff")
            out.append(f'<rect x="{L + c * cs}" y="{T + r * cs}" width="{cs}" height="{cs}" fill="{fill}" stroke="#9ca3af" stroke-width="2"/>')
            if ch == ".":
                h = abs(r - 1) + abs(c - 3)
                out.append(f'<text x="{L + c * cs + cs - 10}" y="{T + r * cs + 28}" font-size="20" fill="{MUTED}" text-anchor="end">h={h}</text>')
    for k, (r, c) in enumerate(order):
        if show_order:
            out.append(f'<circle cx="{L + c * cs + 30}" cy="{T + r * cs + 30}" r="17" fill="{S1}"/>'
                       f'<text x="{L + c * cs + 30}" y="{T + r * cs + 37}" font-size="20" fill="#ffffff" text-anchor="middle">{k + 1}</text>')
    for (r, c), lab in (((1, 0), "S"), ((1, 3), "Đ")):
        out.append(f'<text x="{L + c * cs + cs / 2}" y="{T + r * cs + cs / 2 + 22}" font-size="34" font-weight="bold" fill="{INK}" text-anchor="middle">{lab}</text>')
    if show_path:
        pts = " ".join(f"{L + c * cs + cs / 2},{T + r * cs + cs / 2 + 4}" for r, c in path)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{S2}" stroke-width="5" stroke-dasharray="12 7"/>')
    return "".join(out) + "</svg>"


# ───────── L01: hai thứ tự quay trong 3D (hình chiếu xiên) ─────────
def np_close(u, v):
    return all(abs(a - b) < 1e-9 for a, b in zip(u, v))


def iso(x, y, z):
    """Chiếu xiên: trục x hướng chéo xuống trái, y sang phải, z lên trên."""
    return (0.95 * y - 0.62 * x, 0.95 * z - 0.42 * x)


def l01_panel(P, ox, steps, title):
    """steps: [(vectơ 3D, màu, nét đứt, nhãn)] — vectơ đầu, vectơ giữa, vectơ cuối; ox: dịch ngang panel."""
    o = (ox, 0)
    q = iso(-1.3, 0, 0)
    P.line(o, (ox + q[0], q[1]), MUTED, 2, dash="5 7")
    P.text((ox + q[0], q[1]), "−x", dx=12, dy=-4, size=19, col=MUTED, anchor="start")
    for v, lab in (((1.3, 0, 0), "x"), ((0, 1.3, 0), "y"), ((0, 0, 1.3), "z")):
        q = iso(*v)
        P.line(o, (ox + q[0], q[1]), MUTED, 2, arrow="ar")
        P.text((ox + q[0], q[1]), lab, dx=-14 if lab == "x" else 14, dy=8 if lab != "z" else -6, size=21, col=MUTED)
    for v, col, dash, lab, dx, dy in steps:
        q = iso(*v)
        P.line(o, (ox + q[0], q[1]), col, 4.5, dash=dash, arrow="ab" if col == S1 else ("ao" if col == S2 else "ar"))
        P.text((ox + q[0], q[1]), lab, dx=dx, dy=dy, size=20, anchor="start" if dx >= 0 else "end")
    P.text((ox, -1.15), title, size=21)


def l01_order3d():
    P = Plane(980, 430, (-1.3, 4.9), (-1.35, 1.45), pad=(20, 20, 30, 20))
    a = alg.rotx(90) @ [0, 1, 0]
    b = alg.rotz(90) @ a
    c = alg.rotz(90) @ [0, 1, 0]
    d = alg.rotx(90) @ c
    f = lambda v: "(" + ", ".join(vn(round(c) + 0, 0) for c in v) + ")"
    assert np_close(b, (0, 0, 1)) and np_close(d, (-1, 0, 0))
    l01_panel(P, 0, [((0, 1, 0), S1, None, "(0, 1, 0)", 10, 26), (tuple(b), S2, "12 7", f(b), 14, 4)],
              "quay quanh x trước, rồi quanh z")
    l01_panel(P, 3.3, [((0, 1, 0), S1, None, "(0, 1, 0)", 10, 26), (tuple(d), S2, "12 7", f(d), -14, -14)],
              "quay quanh z trước, rồi quanh x")
    return P.svg()


def l09_resp():
    """x_1(t) của x' = Ax từ (1, 0): A có trị riêng −1, −2 (thực) và A có trị riêng −1 ± 2i (phức) — RK4 bước 0,01."""
    import numpy as np
    C = Chart(900, 430, (0, 5), (-0.4, 1.0), 1, 0.2, "thời gian t", "x₁(t): vị trí", fmt=lambda v: vn(v, 1))
    C.line((0, 0), (5, 0), MUTED, 2)
    for M, col, dash, lab, at in (([[0, 1], [-2, -3]], S1, None, "trị riêng −1, −2: tắt dần", (1.6, 0.55)),
                                  ([[0, 1], [-5, -2]], S2, "12 7", "trị riêng −1 ± 2i: dao động tắt dần", (2.0, -0.3))):
        A = np.array(M, float)
        xs = alg.rk4_ode(lambda t, x: A @ x, np.array([1.0, 0.0]), 0.01, 500)
        C.poly([(k * 0.01, float(v[0])) for k, v in enumerate(xs) if k % 5 == 0], col, 3, dash)
        C.text(at, lab, size=20, anchor="start")
    return C.svg()


def l13_ellipse():
    """Elip 1 độ lệch chuẩn của (vị trí, vận tốc): ban đầu P = I; sau dự đoán F P Fᵀ (nghiêng); sau cập nhật — từ alg.kalman_cv."""
    import numpy as np
    xp, Pp, K, xn, Pn = alg.kalman_cv((0, 1), np.eye(2), 1.5, 1, np.zeros((2, 2)), 1)
    P = Plane(760, 470, (-1.3, 3.0), (-0.6, 2.7), pad=(70, 30, 30, 60))
    P.line((-1.3, 0), (3.0, 0), MUTED, 2, arrow="ar")
    P.line((0, -0.6), (0, 2.7), MUTED, 2, arrow="ar")
    P.text((3.0, 0), "vị trí", dx=-6, dy=30, col=MUTED, anchor="end")
    P.text((0, 2.7), "vận tốc", dx=12, dy=8, col=MUTED, anchor="start")

    def ell(c, M, col, dash=None):
        w, V = np.linalg.eigh(np.asarray(M, float))
        pts = []
        for k in range(73):
            a = 2 * math.pi * k / 72
            v = V @ (np.sqrt(w) * np.array([math.cos(a), math.sin(a)]))
            pts.append((c[0] + v[0], c[1] + v[1]))
        P.poly(pts, col, 3, dash)
        P.dot(tuple(c), col, 6)

    ell((0, 1), np.eye(2), MUTED)
    ell(xp, Pp, S1)
    ell(xn, Pn, S2, "12 7")
    P.text((-0.95, 2.15), "ban đầu", size=20, anchor="start")
    P.text((1.6, 2.15), "sau dự đoán (nghiêng)", size=20, anchor="start")
    P.text((xn[0], xn[1] - 0.95), "sau khi đo vị trí", size=20, anchor="start")
    return P.svg()


def l14_dft():
    """|X_k| của 10 mẫu (lấy 10 lần mỗi giây) của cos 2 Hz + 0,5·cos 4 Hz — alg.dft_mag. Nửa sau (k > 5) là ảnh gương: tô xám."""
    x = [math.cos(2 * math.pi * 2 * n / 10) + 0.5 * math.cos(2 * math.pi * 4 * n / 10) for n in range(10)]
    mags = alg.dft_mag(x)
    C = Chart(900, 400, (-0.5, 9.5), (0, 6), 1, 1, "chỉ số k (tần số k Hz khi lấy 10 mẫu trong 1 giây)", "độ lớn |Xₖ|",
              fmt=lambda v: vn(v, 0), pad=(80, 40, 50, 66), xstart=0)
    for k, m in enumerate(mags):
        col = S1 if k <= 5 else "#9ca3af"
        x0, x1 = C.X(k - 0.32), C.X(k + 0.32)
        y0, y1 = C.Y(0), C.Y(m)
        if m > 1e-9:
            C.add(f'<path d="M{x0:.1f},{y0:.1f} L{x0:.1f},{y1 + 4:.1f} Q{x0:.1f},{y1:.1f} {x0 + 4:.1f},{y1:.1f} '
                  f'L{x1 - 4:.1f},{y1:.1f} Q{x1:.1f},{y1:.1f} {x1:.1f},{y1 + 4:.1f} L{x1:.1f},{y0:.1f} Z" fill="{col}"/>')
            C.text((k, m), vn(m, 1), dy=-10, size=19)
    C.text((7.0, 5.6), "k > 5: ảnh gương, không thêm thông tin", size=19, anchor="middle", col=MUTED)
    return C.svg()


if __name__ == "__main__":
    for name, fn in (("rot90", l00_rot), ("rot30", l00_rot30), ("order", l03_order), ("fk", l04_fk), ("ik", l05_ik),
                     ("reach", l05_reach), ("sing", l06_sing), ("euler", l07_euler), ("pid", l10_pid), ("steps", l11_steps),
                     ("fuse", l12_fuse), ("alias", l14_alias), ("fit", l16_fit), ("order3d", l01_order3d), ("resp", l09_resp), ("ellipse", l13_ellipse), ("dft", l14_dft)):
        save(name, fn())
    save("grid0", l15_grid(False, False))
    save("grid", l15_grid())
