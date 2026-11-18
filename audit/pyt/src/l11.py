from lib import *
from labkit import write_lab, practice_steps, practice_scene

V = "venv"
HEAD = "import matplotlib\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\n"


def nofill(steps):
    """Bỏ hai câu đệm tự động của lib.split_note (lời bài đã nêu lý do ở cả hai nửa)."""
    for s_ in steps:
        t_ = s_["say"].replace("Nghĩa là mỗi kết luận ở đây đều kiểm được bằng con số trên màn hình. ", "").replace(" Vì vậy ta đọc kết quả thật của máy ngay bên dưới.", "")
        if t_ != s_["say"]:  # tính lại `focus` cho khớp số câu mới
            s_["say"] = t_
            sents_, units_ = lv.sentences(t_), lv.html_units(s_["show"])
            if len(units_) >= 2 and len(sents_) >= 2:
                s_["focus"] = [1 + (j * len(units_)) // len(sents_) for j in range(len(sents_))]
            else:
                s_.pop("focus", None)
    return steps


P_COT = py("bieu_do_cot", HEAD + '''loai = ["chuyen", "nap", "rut"]
tong = [1450, 3000, 300]
fig, ax = plt.subplots()
ax.bar(loai, tong)
ax.set_title("Tong tien theo loai (nghin dong)")
fig.savefig("cot.png")
print([int(p.get_height()) for p in ax.patches])
print([round(float(v), 1) for v in ax.get_ylim()])''', '[1450, 3000, 300]\n[0.0, 3150.0]', env=V)
P_DUONG = py("bieu_do_duong", HEAD + '''ngay = [1, 2, 3, 4, 5, 6, 7]
so_gd = [120, 135, 128, 150, 162, 158, 171]
fig, ax = plt.subplots()
ax.plot(ngay, so_gd, marker="o")
ax.set_xlabel("ngay trong tuan")
print([int(y) for y in ax.lines[0].get_ydata()])
print([round(float(v), 2) for v in ax.get_ylim()])''', '[120, 135, 128, 150, 162, 158, 171]\n[117.45, 173.55]', env=V)
P_HIST = py("bieu_do_cot_nhom", HEAD + '''so_tien = [50, 80, 120, 150, 160, 200, 220, 250, 300, 310, 900]
fig, ax = plt.subplots()
dem, bien, _ = ax.hist(so_tien, bins=[0, 200, 400, 600, 800, 1000])
print([int(x) for x in dem])
print([int(b) for b in bien])''', '[5, 5, 0, 0, 1]\n[0, 200, 400, 600, 800, 1000]', env=V)
P_TAN = py("bieu_do_phan_tan", HEAD + '''so_gd = [120, 135, 128, 150, 162, 158, 171]
doanh_thu = [60, 70, 64, 80, 86, 83, 92]
fig, ax = plt.subplots()
ax.scatter(so_gd, doanh_thu)
print(len(ax.collections[0].get_offsets()))''', '7', env=V)
P_GOP = py("gop_danh_lua", '''kenh_a = {"nho": (9, 10), "lon": (30, 90)}
kenh_b = {"nho": (80, 90), "lon": (2, 10)}
for ten, kenh in (("A", kenh_a), ("B", kenh_b)):
    dat_chung = 0
    tong_chung = 0
    for loai in ["nho", "lon"]:
        dat, tong = kenh[loai]
        print(ten, loai, round(100 * dat / tong, 1))
        dat_chung = dat_chung + dat
        tong_chung = tong_chung + tong
    print(ten, "chung", round(100 * dat_chung / tong_chung, 1))''', 'A nho 90.0\nA lon 33.3\nA chung 39.0\nB nho 88.9\nB lon 20.0\nB chung 82.0')
P_LOG = py("thang_log", HEAD + '''du_lieu = [1, 10, 100, 1000]
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(du_lieu)
ax2.plot(du_lieu)
ax2.set_yscale("log")
print(ax1.get_yscale(), ax2.get_yscale())''', 'linear log', env=V)
P_CAT2 = py("truc_cat_don", HEAD + '''fig, ax = plt.subplots()
ax.bar(["thang 1", "thang 2"], [100, 103])
ax.set_ylim(99, 104)
print([float(v) for v in ax.get_ylim()])
thay = round((103 - 99) / (100 - 99), 1)
print("ti le nhin thay:", thay, "- ti le that:", round(103 / 100, 2))''', '[99.0, 104.0]\nti le nhin thay: 4.0 - ti le that: 1.03', env=V)
P_HEX = py("gop_luc_giac", HEAD + '''import numpy as np
rng = np.random.default_rng(1)
x = rng.normal(size=100000)
y = rng.normal(size=100000)
fig, ax = plt.subplots()
ax.hexbin(x, y, gridsize=30)
fig.savefig("luc_giac.png")
print(int(ax.collections[0].get_array().sum()))''', '100000', env=V)
measure("l11_plot", '''import json, os, tempfile, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
res = {}
rng = np.random.default_rng(1)
d = tempfile.mkdtemp()
for k, n in (("1e3", 10 ** 3), ("1e5", 10 ** 5), ("1e6", 10 ** 6)):
    x = rng.normal(size=n)
    y = rng.normal(size=n)
    fig, ax = plt.subplots()
    t0 = time.perf_counter()
    ax.scatter(x, y, s=2)
    p = os.path.join(d, "a.png")
    fig.savefig(p)
    res["t_png_" + k] = time.perf_counter() - t0
    res["m_png_" + k] = os.path.getsize(p)
    if n <= 10 ** 5:
        q = os.path.join(d, "a.svg")
        fig.savefig(q, metadata={"Date": None})
        res["m_svg_" + k] = os.path.getsize(q)
    plt.close(fig)
    fig, ax = plt.subplots()
    t0 = time.perf_counter()
    ax.hexbin(x, y, gridsize=30)
    fig.savefig(p)
    res["t_hex_" + k] = time.perf_counter() - t0
    plt.close(fig)
print(json.dumps(res))''', env=V)

LAB_SOL = HEAD + '''from pathlib import Path

kenh = ["atm", "app", "quay"]
tong = [4200, 6100, 1500]
fig, ax = plt.subplots()
ax.bar(kenh, tong)
ax.set_title("Tong tien theo kenh (nghin dong)")
ax.set_ylabel("nghin dong")
fig.savefig("bieu_do.png")
print("Ve xong:", Path("bieu_do.png").exists())
print("Do cao cot:", [int(p.get_height()) for p in ax.patches])
print("Truc y bat dau tu 0:", ax.get_ylim()[0] == 0)
print("Tieu de:", ax.get_title())
lon = tong.index(max(tong))
nho = tong.index(min(tong))
print("Lon nhat:", kenh[lon], "- gap", round(tong[lon] / tong[nho], 1), "lan nho nhat")'''
P_LAB = py("lab_l11", LAB_SOL, 'Ve xong: True\nDo cao cot: [4200, 6100, 1500]\nTruc y bat dau tu 0: True\nTieu de: Tong tien theo kenh (nghin dong)\nLon nhat: app - gap 4.1 lan nho nhat', env=V)
LAB_OUT = P_LAB["out"]


def chart_bar(x, y, w, h, vals, labels, lo, hi, col, size=22, fmt=str):
    """Khung biểu đồ cột vẽ bằng SVG: trục y chạy từ lo đến hi (lo > 0 là trục bị cắt)."""
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#9ca3af" stroke-width="2"/>']
    n = len(vals)
    slot = w / n
    bw = slot * 0.55
    for i, v in enumerate(vals):
        bh = max(2, (v - lo) / (hi - lo) * h)
        bx = x + i * slot + (slot - bw) / 2
        parts.append(f'<rect x="{bx:.0f}" y="{y + h - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{col[1]}" opacity="0.85"/>')
        ty = round(y + h - bh - 8)
        if ty - size < y:  # nhãn sẽ chạm viền trên của khung: đặt vào trong cột, chữ trắng
            parts.append(txt(round(bx + bw / 2), round(y + h - bh + size + 6), fmt(v), size, "middle", "#ffffff", True))
        else:
            parts.append(txt(round(bx + bw / 2), ty, fmt(v), size, "middle", "#1f2937", True))
        parts.append(txt(round(bx + bw / 2), y + h + 28, labels[i], size, "middle", "#1f2937"))
    if x > 90:
        parts.append(txt(x - 8, y + h, str(lo), size, "end", "#6b7280"))
        parts.append(txt(x - 8, y + 20, str(hi), size, "end", "#6b7280"))
    return "".join(parts)


def chart_line(x, y, w, h, vals, lo, hi, col, labels=None, size=20):
    pts = []
    n = len(vals)
    for i, v in enumerate(vals):
        px = x + 30 + i * (w - 60) / (n - 1)
        py_ = y + h - (v - lo) / (hi - lo) * h
        pts.append((px, py_))
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#9ca3af" stroke-width="2"/>',
             '<polyline fill="none" stroke="' + col[1] + '" stroke-width="4" points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + '"/>']
    for i, (a, b) in enumerate(pts):
        parts.append(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="7" fill="{col[1]}"/>')
        if labels:
            parts.append(txt(round(a), y + h + 26, labels[i], size, "middle", "#1f2937"))
    return "".join(parts)


def shown_sec(txt):
    """Giây ứng với chữ t_show đã hiện trên màn hình ('≈ 2 s' -> 2)."""
    v, u = txt[2:].split()
    return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1, "phút": 60, "giờ": 3600, "ngày": 86400}[u]


def x_k(x, k):
    """Ngoại suy từ số ĐÃ LÀM TRÒN hiện trên màn hình (bảng khớp phép nhân: 2 s x 100 = 3 phút, không phải 4 phút)."""
    return t_show(shown_sec(t_show(x)[0]) * k)


FIG11 = json.loads((ROOT / "audit" / "pyt" / "fig_l11.json").read_text(encoding="utf-8"))  # dữ liệu thật của hexbin (make_fig_l11.py)
HX_NZ = sum(1 for _, _, c in FIG11["cells"] if c > 0)


def fig_hex(x0, y0, side):
    """Vẽ các ô lục giác thật của lệnh hexbin (toạ độ ô và số đếm từ fig_l11.json); ô đậm = nhiều điểm."""
    (xa, xb), (ya, yb) = FIG11["xlim"], FIG11["ylim"]
    sx, sy = side / (xb - xa), side / (yb - ya)
    hexv = FIG11["hex"][:6]
    parts = [f'<rect x="{x0}" y="{y0}" width="{side}" height="{side}" fill="#fff" stroke="#9ca3af" stroke-width="2"/>']
    for cx, cy, c in FIG11["cells"]:
        if c == 0:
            continue
        t = c / FIG11["max"]
        col = f"rgb({round(219 + (30 - 219) * t)},{round(234 + (58 - 234) * t)},{round(254 + (138 - 254) * t)})"
        pts = " ".join(f"{x0 + (cx + vx - xa) * sx:.1f},{y0 + side - (cy + vy - ya) * sy:.1f}" for vx, vy in hexv)
        parts.append(f'<polygon points="{pts}" fill="{col}"/>')
    return "".join(parts)


def hex_legend(x0, y0, mx):
    """Thanh màu: từ 1 điểm (nhạt) đến mx điểm (đậm), cùng bảng màu với fig_hex."""
    parts = []
    for i in range(10):
        t = i / 9
        col = f"rgb({round(219 + (30 - 219) * t)},{round(234 + (58 - 234) * t)},{round(254 + (138 - 254) * t)})"
        parts.append(f'<rect x="{x0}" y="{y0 + 240 - i * 24}" width="40" height="24" fill="{col}"/>')
    parts.append(txt(x0 + 50, y0 + 244, "1 điểm", 22, "start", "#1f2937"))
    parts.append(txt(x0 + 50, y0 + 22, f"{vnum(mx)} điểm", 22, "start", "#1f2937"))
    return "".join(parts)


def ticks(x0, y0, w, h, xs, ys, size=20):
    """Vạch và nhãn trục: xs = [(vị trí px, nhãn)] dưới khung, ys = [(vị trí px, nhãn)] bên trái khung."""
    parts = []
    for px_, lb in xs:
        parts.append(f'<line x1="{px_:.0f}" y1="{y0 + h}" x2="{px_:.0f}" y2="{y0 + h + 8}" stroke="#6b7280" stroke-width="2"/>')
        parts.append(txt(round(px_), y0 + h + 30, lb, size, "middle", "#374151"))
    for py_, lb in ys:
        parts.append(f'<line x1="{x0 - 8}" y1="{py_:.0f}" x2="{x0}" y2="{py_:.0f}" stroke="#6b7280" stroke-width="2"/>')
        parts.append(txt(x0 - 12, round(py_ + 7), lb, size, "end", "#374151"))
    return "".join(parts)


def fig_pts(x0, y0, w, h, dark):
    """Đám điểm trên hệ trục từ −4,5 đến 4,5: bên trái 1 000 điểm THẬT (đầu mẫu của lệnh hexbin, fig_l11.json); bên phải hình bầu dục minh hoạ vùng −3..3."""
    lo, hi = -4.5, 4.5
    sx, sy = w / (hi - lo), h / (hi - lo)

    def px_(v):
        return x0 + (v - lo) * sx

    def py_(v):
        return y0 + h - (v - lo) * sy

    parts = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{"#1f2937" if dark else "#fff"}" stroke="#9ca3af" stroke-width="2"/>']
    if dark:
        parts.append(f'<ellipse cx="{px_(0):.0f}" cy="{py_(0):.0f}" rx="{3 * sx:.0f}" ry="{3 * sy:.0f}" fill="#2a78d6"/>')
    else:
        d = " ".join(f"M{px_(a):.1f} {py_(b):.1f}h0" for a, b in FIG11["pts1k"])
        parts.append(f'<path d="{d}" stroke="#2a78d6" stroke-width="6" stroke-linecap="round" opacity="0.55" fill="none"/>')
    tk = (-4, -2, 0, 2, 4)
    parts.append(ticks(x0, y0, w, h, [(px_(v), str(v).replace("-", "−")) for v in tk], [(py_(v), str(v).replace("-", "−")) for v in tk]))
    return "".join(parts)


def fig_log(x0, y0, w, h, log):
    """Biểu đồ đường của đúng bốn số 1, 10, 100, 1000 (như mã P_LOG), thang thường hoặc thang lôgarit."""
    import math
    vals = [1, 10, 100, 1000]
    pts = []
    for i, v in enumerate(vals):
        t = math.log10(v) / 3 if log else v / 1000
        pts.append((x0 + 60 + i * (w - 120) / 3, y0 + h - 20 - t * (h - 40)))
    parts = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#fff" stroke="#9ca3af" stroke-width="2"/>',
             '<polyline fill="none" stroke="' + ("#16a34a" if log else "#2a78d6") + '" stroke-width="4" points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + '"/>']
    for (a, b), v in zip(pts, vals):
        parts.append(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="7" fill="#1f2937"/>')
        parts.append(txt(round(a - 12), round(b - 12), str(v), 22, "end", "#1f2937", True))
    return "".join(parts)


def build():
    t3, t5, t6 = M("l11_plot", "t_png_1e3"), M("l11_plot", "t_png_1e5"), M("l11_plot", "t_png_1e6")
    h3, h5, h6 = M("l11_plot", "t_hex_1e3"), M("l11_plot", "t_hex_1e5"), M("l11_plot", "t_hex_1e6")
    sv3, sv5 = M("l11_plot", "m_svg_1e3"), M("l11_plot", "m_svg_1e5")
    pn3, pn5, pn6 = M("l11_plot", "m_png_1e3"), M("l11_plot", "m_png_1e5"), M("l11_plot", "m_png_1e6")
    st3, st5, st6, sh6 = t_show(t3), t_show(t5), t_show(t6), t_show(h6)
    st8 = x_k(t6, 100)
    bs3, bs5, bs6, bs8 = b_show(sv3), b_show(sv5), b_show(sv5 * 10), b_show(sv5 * 1000)
    bp6 = b_show(pn6)
    sc_hook = sc("hook", "hook", "Cùng dữ liệu, hai biểu đồ: tăng 3% hay tăng gấp bốn?", [
        st(svg(1500, 400,
               txt(375, 30, "biểu đồ A: trục y từ 0 đến 110", 26, "middle", "#1f2937", True),
               chart_bar(120, 50, 500, 250, [100, 103], ["tháng 1", "tháng 2"], 0, 110, C_BLUE, 26),
               txt(1125, 30, "biểu đồ B: trục y từ 99 đến 104", 26, "middle", "#dc2626", True),
               chart_bar(870, 50, 500, 250, [100, 103], ["tháng 1", "tháng 2"], 99, 104, C_RED, 26),
               txt(750, 370, "dữ liệu giống hệt nhau: 100 và 103 (triệu đồng)", 28, "middle", "#1f2937", True)),
           """Chào bạn, đây là hai biểu đồ vẽ từ cùng một dữ liệu, doanh thu tháng một là một trăm và tháng hai là một trăm lẻ ba triệu đồng. Biểu đồ bên trái có trục dọc bắt đầu từ không, cột hai chỉ cao hơn chút. Biểu đồ bên phải cắt trục từ chín mươi chín, cột hai trông cao gấp bốn lần.
           """),
        st(f'<div class="box key">Tỉ lệ <b>nhìn thấy</b> = (cột hai − gốc trục) ÷ (cột một − gốc trục). Gốc trục $0$: $\\frac{{103}}{{100}} = 1{{,}}03$. Gốc trục $99$: $\\frac{{103 - 99}}{{100 - 99}} = 4$.</div>'
           '<div class="box key">Hôm nay ta trả lời ba câu hỏi:<ol><li>Chọn loại biểu đồ nào cho câu hỏi nào, và vẽ ra <b>tệp ảnh</b> thế nào?</li>'
           '<li><b>Đọc</b> một biểu đồ cho đúng: nhìn vào đâu trước?</li>'
           '<li>Ba cách biểu đồ <b>đánh lừa</b>, và khi dữ liệu lớn thì biểu đồ gặp vấn đề gì?</li></ol></div>',
           """Tỉ lệ nhìn thấy bằng chiều cao phần cột nhô lên trên gốc trục. Gốc trục bằng không thì tỉ lệ là một phẩy không ba. Gốc trục chín mươi chín thì tỉ lệ là bốn. Hôm nay ta học chọn loại biểu đồ và vẽ ra tệp ảnh, đọc một biểu đồ cho đúng, và nhận ra ba cách biểu đồ đánh lừa cùng vấn đề khi dữ liệu lớn."""),
    ], )
    sc_pre = sc("prereq", "prereq", "Ôn lại: danh sách, mảng, bảng và nạp thư viện bằng tên ngắn", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① danh sách, mảng, bảng", "dữ liệu cần vẽ nằm trong danh sách <code>[1450, 3000, 300]</code>, mảng hoặc cột của bảng"],
                  ["② nạp bằng tên ngắn", "<code>import matplotlib.pyplot as plt</code>: <code>as</code> đặt tên ngắn; thư viện vẽ đã có trong tệp ghim của khoá"],
                  ["③ đối tượng và phương thức", "<code>ax.bar(…)</code> là gọi một <b>phương thức</b> của đối tượng <code>ax</code>"]]),
           """Dữ liệu cần vẽ nằm trong danh sách, mảng hoặc cột của bảng. Lệnh nạp với tên ngắn mang thư viện vẽ vào chương trình. Và gọi một lệnh trên đối tượng là gọi một phương thức của nó.""",
           focus=["1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã khung ảnh, trục, bốn loại biểu đồ và tệp ảnh", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>fig, ax = plt.subplots()</code>", "dựng khung ảnh và một biểu đồ", "<code>fig</code> là <b>khung ảnh</b>; <code>ax</code> là <b>một biểu đồ</b> nằm trong khung (có hai trục)"],
                  ["<code>matplotlib.use(\"Agg\")</code>", "vẽ ra tệp, không mở cửa sổ", "dùng trên máy chủ hoặc khi chạy tự động; sau đó <code>fig.savefig(\"cot.png\")</code> ghi ảnh"],
                  ["<code>ax.set_title(…)</code>, <code>ax.set_xlabel(…)</code>, <code>ax.set_ylabel(…)</code>", "đặt tiêu đề, nhãn trục ngang, nhãn trục đứng", "luôn ghi <b>đơn vị</b> ở nhãn trục"]]),
           """Bảng đầu là khung và tệp ảnh. Lệnh dựng khung cho ta khung ảnh và một biểu đồ nằm trong đó, với hai trục. Chọn chế độ vẽ ra tệp khi chạy trên máy chủ hoặc chạy tự động, rồi lệnh lưu ghi ảnh ra tệp. Tiêu đề và nhãn trục phải có, và luôn ghi đơn vị ở nhãn trục."""),
        st(table(["câu hỏi", "loại biểu đồ", "viết"],
                 [["so sánh <b>giữa các nhóm</b>", "cột", "<code>ax.bar(nhãn, giá_trị)</code>"],
                  ["xu hướng <b>theo thời gian</b>", "đường", "<code>ax.plot(x, y)</code>"],
                  ["quan hệ <b>giữa hai số</b>", "phân tán", "<code>ax.scatter(x, y)</code>"],
                  ["<b>phân bố</b> của một số", "biểu đồ tần suất (histogram)", "<code>ax.hist(dữ_liệu, bins=…)</code>: các cột đếm số giá trị rơi vào mỗi <b>khoảng</b>"]]),
           """So sánh giữa các nhóm thì dùng cột. Xu hướng theo thời gian thì dùng đường. Quan hệ giữa hai số thì dùng phân tán, mỗi điểm là một cặp. Phân bố của một số thì dùng biểu đồ tần suất, các cột đếm số giá trị rơi vào mỗi khoảng.""",
           focus=["1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>ax.set_ylim(99, 104)</code>", "đặt khoảng của trục y", "chọn <b>gốc trục</b> và đầu trên: quyết định hình dáng cột; <code>ax.get_ylim()</code> hỏi khoảng đang dùng"],
                  ["<code>ax.set_yscale(\"log\")</code>", "thang lôgarit", "mỗi vạch cách nhau <b>một hệ số nhân</b> (×10), không phải một số cộng; <code>ax.get_yscale()</code> hỏi thang đang dùng"],
                  ["<code>ax.patches</code>, <code>ax.lines[0].get_ydata()</code>", "các hình đã vẽ", "đọc lại <b>số liệu thật</b> để kiểm: <code>ax.lines[0]</code> là đường đầu, <code>get_ydata()</code> là các giá trị trục đứng của nó"],
                  ["<code>ax.collections[0].get_offsets()</code>, <code>.get_array()</code>", "đọc lại điểm, ô gộp", "<code>ax.collections</code>: các nhóm điểm (hoặc ô gộp) đã vẽ, <code>[0]</code> lấy nhóm đầu; <code>get_offsets()</code> = toạ độ từng điểm; <code>get_array()</code> = số điểm rơi vào từng ô gộp"]]),
           """Đặt khoảng của trục chọn gốc trục, và gốc trục quyết định hình dáng cột. Thang lôgarit làm mỗi vạch cách nhau một hệ số nhân. Các lệnh hỏi lại cho biết khoảng và thang đang dùng. Ta đọc lại các hình đã vẽ và giá trị của đường để lấy số liệu thật. Với điểm và ô gộp, ta lấy nhóm đã vẽ đầu tiên, rồi hỏi toạ độ từng điểm hoặc số điểm trong từng ô gộp.""", clear=True, introduces=["pyt_get_offsets"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: bốn câu hỏi, bốn biểu đồ; đọc biểu đồ là đọc trục trước, hình sau", [
        st(svg(1500, 430,
               txt(190, 30, "cột: so sánh nhóm", 24, "middle", "#1f2937", True),
               chart_bar(30, 50, 320, 240, [1450, 3000, 300], ["chuyển", "nạp", "rút"], 0, 3150, C_BLUE, 20),
               txt(560, 30, "đường: theo thời gian", 24, "middle", "#1f2937", True),
               chart_line(390, 50, 340, 240, [120, 135, 128, 150, 162, 158, 171], 110, 180, C_GREEN, ["1", "2", "3", "4", "5", "6", "7"]),
               txt(930, 30, "phân tán: hai số", 24, "middle", "#1f2937", True),
               '<rect x="770" y="50" width="330" height="240" fill="#fff" stroke="#9ca3af" stroke-width="2"/>'
               + "".join(f'<circle cx="{800 + (a - 118) * 5}" cy="{280 - (b - 58) * 6}" r="7" fill="#d97706"/>' for a, b in zip([120, 135, 128, 150, 162, 158, 171], [60, 70, 64, 80, 86, 83, 92])),
               txt(1290, 30, "tần suất: phân bố", 24, "middle", "#1f2937", True),
               chart_bar(1140, 50, 330, 240, [5, 5, 0, 0, 1], ["200", "400", "600", "800", "1000"], 0, 6, C_PURPLE, 18),
               txt(750, 372, "bước đầu tiên khi đọc: tiêu đề, đơn vị, trục bắt đầu từ đâu, thang gì", 28, "middle", "#1f2937", True),
               txt(750, 412, "rồi mới nhìn hình và so các giá trị", 26, "middle", "#16a34a", True)),
           """Hình này là bốn câu hỏi và bốn biểu đồ: cột, đường, phân tán, tần suất. Khi đọc biểu đồ, bước đầu tiên là đọc tiêu đề, đơn vị, trục bắt đầu từ đâu và dùng thang gì. Rồi mới nhìn hình."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: vẽ cột đọc lại số liệu, cắt trục, khoảng chia, gộp, thang lôgarit", nofill(splitall([
        st(run_block(P_COT, title="Bước 1. Cột bắt đầu từ 0: chiều cao tỉ lệ giá trị")
           + "<p>Ba dòng đầu nạp thư viện và chọn chế độ vẽ ra tệp (<code>Agg</code>: vẽ ra tệp, không mở cửa sổ); ba dòng này có mặt ở mọi chương trình vẽ bên dưới. Vì trục <code>y</code> tự chọn từ $0$ tới $3150$ ($3000$ cộng $5\\%$ đệm), chiều cao cột tỉ lệ với giá trị: cột nạp cao gấp $\\frac{3000}{300} = 10$ lần cột rút. <code>ax.patches</code> là danh sách các cột (hình chữ nhật) đã vẽ; <code>p.get_height()</code> hỏi chiều cao cột <code>p</code>; <code>[… for p in ax.patches]</code> là danh sách suy ra: một phần tử cho mỗi cột.</p>",
           """Bước một, vẽ cột. Vì ta cần vẽ ra tệp chứ không mở cửa sổ, ba dòng đầu nạp thư viện và chọn chế độ vẽ ra tệp. Ta vẽ tổng tiền ba loại, rồi đọc lại số liệu từ các hình đã vẽ: lấy danh sách các cột, hỏi chiều cao từng cột, gom thành một danh sách suy ra, đúng ba số. Trục dọc tự chọn từ không đến ba nghìn một trăm năm mươi, tức giá trị lớn nhất cộng năm phần trăm đệm. Vì gốc trục là không, chiều cao cột tỉ lệ với giá trị, cột nạp cao gấp mười lần cột rút."""),
        st(run_block(P_CAT2, title="Bước 2. Cắt trục làm tỉ lệ nhìn thấy khác tỉ lệ thật"),
           """Bước hai, cắt trục. Ta vẽ cột cho dữ liệu một trăm và một trăm lẻ ba, nhưng đặt trục bắt đầu từ chín mươi chín. Máy in khoảng của trục, và tỉ lệ cột nhìn thấy là bốn, trong khi tỉ lệ dữ liệu thật là một phẩy không ba. Vì phần cột nhô lên trên gốc trục mới là phần mắt so sánh.""", clear=True),
        st(code_block(P_HIST, title="Bước 3. Khoảng chia quyết định hình dáng phân bố")
           + "<p><code>dem, bien, _ = ax.hist(…)</code>: hàm trả về <b>ba thứ</b> (số đếm, các mốc khoảng, các hình cột); gán cùng lúc cho ba tên, và <code>_</code> là tên cho thứ không dùng.</p>"
           + out_block(P_HIST, title=None)
           + "<p>$11$ giao dịch chia vào $5$ khoảng rộng $200$: $[5, 5, 0, 0, 1]$; tổng $5 + 5 + 0 + 0 + 1 = 11$ ✓. Khoảng khác thì hình khác; giao dịch $900$ nằm lẻ loi xa nhóm chính.</p>",
           """Bước ba, khoảng chia của biểu đồ tần suất. Hàm vẽ cột trả về ba thứ, ta gán cả ba cùng lúc cho ba tên, và dấu gạch dưới là tên cho thứ ta bỏ qua. Vì mười một giao dịch chia vào năm khoảng rộng hai trăm nghìn, số đếm là năm, năm, không, không, một. Tổng đúng mười một. Giao dịch chín trăm nghìn nằm lẻ loi, xa nhóm chính, nên khoảng chia khác thì hình khác.""", clear=True),
        st(table(["viết trong mã", "đọc là", "nghĩa"],
                 [["<code>kenh_a = {\"nho\": (9, 10), …}</code>", "từ điển của các bộ", "mỗi loại giao dịch ứng với một bộ <code>(đạt, tổng)</code>: $9$ đạt trong $10$"],
                  ["<code>for ten, kenh in ((\"A\", kenh_a), (\"B\", kenh_b)):</code>", "mở gói bộ", "mỗi lượt lấy một bộ <code>(tên, kênh)</code> và gán luôn cho hai tên <code>ten</code>, <code>kenh</code>"],
                  ["<code>dat, tong = kenh[loai]</code>", "mở gói bộ", "lấy bộ <code>(đạt, tổng)</code> của loại đó, gán cho hai tên <code>dat</code>, <code>tong</code>"]]),
           """Trước khi chạy gộp, đọc ba dòng chính, vì chúng mở gói bộ. Mỗi loại giao dịch ứng với một bộ hai số, đạt và tổng. Vòng lặp ngoài lấy từng bộ tên và kênh, gán luôn cho hai tên. Dòng trong mở gói bộ đạt và tổng của loại đó, gán cho hai tên.""", clear=True),
        st(code_block(P_GOP, title="Bước 4. Gộp che mất cấu trúc: A tốt hơn ở MỌI loại, nhưng B tốt hơn khi gộp")
           + "<div class='box key'>Mỗi tỉ lệ là <code>round(100 * dat / tong, 1)</code>: phần trăm đạt, làm tròn một chữ số; <code>dat_chung</code> và <code>tong_chung</code> cộng dồn đạt và tổng của từng kênh.</div>",
           """Bước bốn là gộp, với hai kênh và tỉ lệ thành công theo giao dịch nhỏ và lớn. Vì mỗi tỉ lệ là phần trăm đạt làm tròn một chữ số, còn hai biến cộng dồn đạt và tổng của từng kênh, ta chạy và đọc kết quả thật ở bước kế.""", clear=True),
        st("<p>$A$: nhỏ $\\frac{9}{10}$, lớn $\\frac{30}{90}$, chung $\\frac{39}{100}$. $B$: nhỏ $\\frac{80}{90}$, lớn $\\frac{2}{10}$, chung $\\frac{82}{100}$. $A$ nhận <b>nhiều giao dịch lớn khó</b>, $B$ nhận nhiều giao dịch nhỏ dễ.</p>" + out_block(P_GOP, title="Kết quả chạy"),
           """Kênh A tốt hơn ở cả hai loại, chín mươi phần trăm so với tám mươi tám phẩy chín, và ba mươi ba phẩy ba so với hai mươi. Nhưng khi gộp lại, kênh B hơn hẳn, tám mươi hai phần trăm so với ba mươi chín, vì kênh A nhận nhiều giao dịch lớn khó.""", clear=True),
        st(code_block(P_LOG, title="Bước 5. Thang lôgarit: mỗi vạch là nhân mười")
           + "<p><code>plt.subplots(1, 2)</code> dựng <b>một hàng, hai biểu đồ</b> cạnh nhau và trả về khung ảnh cùng <b>một cặp</b> biểu đồ; <code>fig, (ax1, ax2) = …</code> tách cặp đó thành hai tên. <code>ax1.plot(du_lieu)</code> chỉ có một đối số: trục ngang tự lấy 0, 1, 2, … (số thứ tự).</p>"
           + out_block(P_LOG, title=None)
           + "<p>Dữ liệu $1, 10, 100, 1000$ tăng <b>gấp mười</b> mỗi bước: trên thang thường là đường cong dốc dần, trên thang lôgarit là <b>đường thẳng</b>. Người đọc quen thang thường dễ hiểu sai thành “tăng đều”.</p>",
           """Bước năm, thang lôgarit. Vì cần so hai thang, ta dựng một hàng hai biểu đồ cạnh nhau, và tách cặp biểu đồ ấy thành hai tên. Vì dữ liệu tăng gấp mười mỗi bước, trên thang thường nó là đường cong dốc dần. Trên thang lôgarit nó là đường thẳng, vì mỗi vạch là một lần nhân mười.""", clear=True),
        st(svg(1500, 400,
               txt(375, 30, "thang thường (linear)", 26, "middle", "#1f2937", True),
               fig_log(60, 50, 630, 290, False),
               txt(1125, 30, "thang lôgarit (log)", 26, "middle", "#16a34a", True),
               fig_log(810, 50, 630, 290, True),
               txt(750, 385, "cùng bốn số 1, 10, 100, 1000: đường cong dốc dần ↔ đường thẳng", 26, "middle", "#1f2937", True)),
           """Đây là hai biểu đồ vẽ từ chính bốn số một, mười, một trăm, một nghìn. Bên trái là thang thường, một đường cong dốc dần. Bên phải là thang lôgarit, bốn điểm nằm trên một đường thẳng, vì mỗi vạch là một lần nhân mười. Người đọc quen thang thường dễ hiểu sai đường thẳng đó thành tăng đều.""", clear=True),
    ])), checks=["round(103 / 100, 2) == 1.03 and round((103 - 99) / (100 - 99), 1) == 4.0", "5 + 5 + 0 + 0 + 1 == 11", "3000 // 300 == 10 and round(3000 * 1.05) == 3150",
               "round(100 * 9 / 10, 1) == 90.0 and round(100 * 80 / 90, 1) == 88.9 and round(100 * 30 / 90, 1) == 33.3 and round(100 * 2 / 10, 1) == 20.0",
               "round(100 * 39 / 100) == 39 and round(100 * 82 / 100) == 82 and 9 + 30 == 39 and 80 + 2 == 82"])
    sc_ex = sc("example", "example", "Ví dụ: đường, phân tán, và đọc số liệu thật từ hình đã vẽ", nofill(splitall([
        st(run_block(P_DUONG, title="Đường: số giao dịch theo ngày trong tuần")
           + "<p>Số giao dịch tăng từ $120$ lên $171$: $\\frac{171 - 120}{120} = 42{,}5\\%$ trong $7$ ngày. Trục $y$ tự chọn từ $117{,}45$ tới $173{,}55$: <b>không bắt đầu từ $0$</b>, chấp nhận được với đường vì ta xem <b>xu hướng</b>, nhưng phải ghi rõ. <code>marker=\"o\"</code> vẽ thêm một chấm tròn tại mỗi điểm dữ liệu.</p>",
           """Ví dụ một, đường. Vì số giao dịch trong bảy ngày tăng từ một trăm hai mươi lên một trăm bảy mươi mốt, nên mức tăng là bốn mươi hai phẩy năm phần trăm. Tham số kiểu dấu vẽ thêm một chấm tròn tại mỗi điểm dữ liệu. Trục dọc tự chọn không bắt đầu từ không. Với biểu đồ đường, điều đó chấp nhận được vì ta xem xu hướng, nhưng người vẽ phải ghi rõ."""),
        st(svg(1500, 420,
               txt(380, 30, "đường: số giao dịch (trục đứng) theo ngày (trục ngang)", 24, "middle", "#1f2937", True),
               chart_line(60, 50, 640, 250, [120, 135, 128, 150, 162, 158, 171], 117.45, 173.55, C_GREEN, ["1", "2", "3", "4", "5", "6", "7"])
               + ticks(60, 50, 640, 250, [], [(300 - (v - 117.45) / 56.1 * 250, str(v)) for v in (120, 140, 160)]),
               txt(1100, 30, "phân tán: doanh thu (trục đứng) theo số giao dịch (trục ngang)", 24, "middle", "#1f2937", True),
               '<rect x="800" y="50" width="600" height="250" fill="#fff" stroke="#9ca3af" stroke-width="2"/>'
               + "".join(f'<circle cx="{830 + (a - 118) * 10.6}" cy="{285 - (b - 58) * 6.6}" r="8" fill="#d97706"/>' for a, b in zip([120, 135, 128, 150, 162, 158, 171], [60, 70, 64, 80, 86, 83, 92]))
               + ticks(800, 50, 600, 250, [(830 + (v - 118) * 10.6, str(v)) for v in (120, 140, 160)], [(285 - (v - 58) * 6.6, str(v)) for v in (60, 70, 80, 90)]),
               txt(750, 392, "doanh thu tăng cùng số giao dịch: các điểm xếp gần một đường dốc lên", 26, "middle", "#1f2937", True)),
           """Bên trái là đường, bên phải là phân tán, mỗi điểm là một ngày. Các điểm xếp gần một đường dốc lên, nghĩa là ngày nhiều giao dịch thì doanh thu cũng cao, nhưng chưa nói cái nào gây ra cái nào.""", clear=True),
        st(run_block(P_TAN, title="Phân tán: bảy điểm, mỗi ngày một điểm")
           + "<p>Đọc lại từ hình đã vẽ: <code>get_offsets()</code> (lấy lại toạ độ các điểm đã vẽ) có $7$ điểm, đúng $7$ ngày. Luôn đối chiếu <b>số điểm vẽ</b> với <b>số dòng dữ liệu</b>.</p>",
           """Cuối cùng, ta lấy lại toạ độ các điểm đã vẽ từ chính hình. Hình phân tán có bảy điểm, đúng bằng bảy ngày. Luôn đối chiếu số điểm vẽ với số dòng dữ liệu, để biết không dòng nào bị mất hay vẽ thừa.""", clear=True),
        st(table(["bước đọc", "biểu đồ B ở đầu bài (trục từ 99 đến 104)"],
                 [["1. tiêu đề", "doanh thu của hai tháng"], ["2. đơn vị", "triệu đồng"], ["3. trục bắt đầu từ đâu", "<b>từ $99$, không phải $0$</b>: cột bị cắt, đáng ngờ"], ["4. thang", "tuyến tính, các vạch cách đều"]])
           + "<p>Kết luận: hình phóng đại; giá trị thật là $100 \\to 103$, chỉ tăng $3\\%$.</p>",
           """Ta đọc mẫu biểu đồ bên phải ở đầu bài theo thứ tự. Tiêu đề và đơn vị cho biết đây là doanh thu hai tháng, tính bằng triệu đồng. Trục bắt đầu ở chín mươi chín chứ không phải không, nên cột bị cắt. Kết luận, hình phóng đại một mức tăng chỉ ba phần trăm.""", clear=True),
    ], only=[0])), checks=["round(100 * (171 - 120) / 120, 1) == 42.5", "len([120, 135, 128, 150, 162, 158, 171]) == 7"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: số liệu vẽ khớp dữ liệu", [
        st("<p>Cách 1: so <code>[int(p.get_height()) for p in ax.patches]</code> với danh sách đã đưa vào: $[1450, 3000, 300]$ ✓. "
           "Cách 2: tổng các cột $1450 + 3000 + 300 = 4750$ phải bằng tổng bảng gốc (đã tính ở bài trước). "
           "Cách 3: tỉ lệ nhìn thấy của hai cột <b>bằng</b> tỉ lệ dữ liệu khi gốc trục là $0$: $\\frac{3000}{300} = 10$.</p>",
           """Ba cách kiểm, độc lập nhau nên khớp cả ba là đáng tin. Cách một, đọc lại chiều cao các cột từ hình đã vẽ và so với danh sách đã đưa vào. Cách hai, cộng các cột, được bốn nghìn bảy trăm năm mươi, phải bằng tổng của bảng gốc ở bài trước. Cách ba, khi gốc trục bằng không, tỉ lệ nhìn thấy giữa hai cột bằng tỉ lệ dữ liệu."""),
    ], checks=["1450 + 3000 + 300 == 4750", "3000 // 300 == 10"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn dần: đám điểm thành mực đen, tệp vector phình theo, nên phải gộp", nofill(splitall([
        st(table(["số điểm", "vẽ phân tán rồi lưu PNG (đo, số minh hoạ)", "kích thước SVG (đo)", "vẽ gộp thành ô lục giác"],
                 [["×1: 1 000", st3[0], bs3[0], t_show(h3)[0]], ["×100: 100 000", st5[0], bs5[0], t_show(h5)[0]],
                  ["×1 000: 1 000 000", st6[0], bs6[0] + " (ngoại suy tuyến tính)", sh6[0]], ["×100 000 (ngoại suy): 100 000 000", st8[0], bs8[0], "—"]])
           + "<p class='note'>Đo trên máy kiểm, số minh hoạ; tệp SVG ghi mỗi điểm một dòng nên lớn tỉ lệ với số điểm. <b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo (ước lượng, chưa đo).</p>",
           f"""Một nghìn điểm mất {st3[1]}. Một trăm nghìn điểm mất {st5[1]}. Một triệu điểm mất {st6[1]}, và tệp ảnh vector, loại ảnh ghi từng hình, ngoại suy, tức nhân theo tỉ lệ từ số đã đo, lên cỡ {bs6[1]}. Cột cuối là vẽ gộp thành ô lục giác, nghĩa là chia mặt phẳng thành các ô sáu cạnh rồi tô màu theo số điểm rơi vào mỗi ô.""", introduces=["pyt_luc_giac"]),
        st(code_block(P_HEX, lines=(1, 7), title="Vẽ gộp (1/2): dựng một trăm nghìn điểm ngẫu nhiên")
           + "<p><code>default_rng(1)</code>: bộ sinh số ngẫu nhiên, hạt giống $1$ (cùng hạt giống thì cùng dãy số); <code>rng.normal(size=…)</code>: số hình chuông, phần lớn gần $0$.</p>",
           """Đây là cách vẽ gộp một trăm nghìn điểm. Dòng đầu dựng bộ sinh số ngẫu nhiên với hạt giống một, cùng hạt giống thì cùng dãy số. Mỗi lần gọi, bộ sinh lấy một trăm nghìn số hình chuông, phần lớn gần không.""", clear=True),
        st(run_slice(P_HEX, code=(8, 11), title="Vẽ gộp (2/2): chia mặt phẳng thành ô lục giác")
           + "<p><code>gridsize=30</code>: khoảng $30$ ô lục giác theo bề ngang. Mỗi ô đếm số điểm rơi vào nó; tổng các ô vẫn là $100\\,000$, không điểm nào mất.</p>",
           """Đối số cuối chia mặt phẳng thành các ô lục giác, khoảng ba mươi ô theo bề ngang. Tổng số điểm đếm trong mọi ô vẫn đúng một trăm nghìn, nên không điểm nào bị mất. Vì ô chỉ đếm điểm, thời gian vẽ gộp gần như không đổi khi số điểm tăng.""", clear=True),
        st(svg(1500, 400,
               txt(375, 30, "1 000 điểm thật (đầu mẫu): còn đọc được", 24, "middle", "#16a34a", True),
               fig_pts(60, 50, 630, 250, False),
               txt(1125, 30, "càng nhiều điểm càng kín (bầu dục minh hoạ −3..3)", 22, "middle", "#dc2626", True),
               fig_pts(810, 50, 630, 250, True),
               txt(750, 382, "điểm chồng lên nhau: không thấy chỗ nào dày hơn chỗ nào", 28, "middle", "#1f2937", True)),
           """Hình này cho thấy vấn đề khác ngoài thời gian. Một nghìn điểm còn đọc được từng cụm. Một triệu điểm chồng lên nhau thành một đám kín, và mắt không còn thấy chỗ nào dày hơn chỗ nào. Tệp ảnh điểm ảnh, tức ảnh lưu từng chấm nhỏ của màn hình, chỉ nặng cỡ vài chục nghìn byte, nhưng thông tin đã mất.""", clear=True, introduces=["pyt_diem_anh"]),
        st(svg(1500, 400,
               txt(390, 30, f"kết quả thật của lệnh vẽ gộp: {vnum(FIG11['n'])} điểm vào {HX_NZ} ô lục giác", 26, "middle", "#1f2937", True),
               fig_hex(60, 50, 330),
               hex_legend(470, 90, FIG11["max"]),
               txt(1100, 120, "ô càng đậm càng nhiều điểm rơi vào", 26, "middle", "#1f2937", True),
               txt(1100, 165, "lõi dày ở giữa, thưa dần ra rìa:", 26, "middle", "#1f2937"),
               txt(1100, 205, "ảnh phân tán một triệu điểm không cho thấy điều này", 26, "middle", "#16a34a", True),
               txt(1100, 270, f"tổng số đếm của mọi ô = {vnum(FIG11['total'])}: không điểm nào mất", 24, "middle", "#6b7280")),
           f"""Đây là kết quả thật của lệnh vẽ gộp: mỗi ô lục giác tô đậm theo số điểm rơi vào. Ô đậm nhất, ở giữa, đếm được {words(FIG11['max'])} điểm, và các ô thưa dần ra rìa, nên ta thấy chỗ dày chỗ thưa.""", clear=True),
        st("<div class='box key'><b>Đánh đổi:</b> khi dữ liệu lớn, <b>đừng vẽ từng điểm</b>: gộp trước (đếm số điểm trong mỗi ô lục giác hoặc mỗi khoảng, lấy mẫu ngẫu nhiên, tính thống kê theo nhóm) rồi vẽ kết quả gộp. "
           "Cái giá: mất chi tiết từng điểm, và phải <b>chọn cách gộp</b> mà đừng để nó đánh lừa (xem bước $4$). Ảnh vector nhỏ khi ít hình, phình tỉ lệ khi nhiều hình; ảnh điểm ảnh thì kích thước gần cố định.</div>",
           f"""Đánh đổi là khi dữ liệu lớn thì đừng vẽ từng điểm. Hãy gộp trước, đếm số điểm trong mỗi ô lục giác hoặc mỗi khoảng, hoặc lấy mẫu ngẫu nhiên, rồi vẽ kết quả gộp. Cái giá là mất chi tiết từng điểm, và phải chọn cách gộp sao cho không đánh lừa.""", clear=True),
    ], only=[])), checks=["10 ** 6 // 10 ** 3 == 1000", "10 ** 8 // 10 ** 6 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", nofill(splitall([
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Cắt trục ở biểu đồ cột: hiệu ứng thị giác không còn tỉ lệ với giá trị.</div>' + run_block(P_CAT2)
           + "<p>Cột <b>luôn</b> bắt đầu từ $0$ (chiều cao là thông tin). Phép thử: <b>đọc <code>get_ylim()</code></b> và tính tỉ lệ nhìn thấy so với tỉ lệ dữ liệu: ở đây $4{,}0$ so với $1{,}03$.</p>",
           """Lỗi thứ nhất, của người mới, là cắt trục ở biểu đồ cột. Chiều cao cột là thông tin, nên cột luôn phải bắt đầu từ không. Phép thử là đọc khoảng của trục và tính tỉ lệ nhìn thấy, vì chỉ so với tỉ lệ dữ liệu mới biết có bị đánh lừa không. Ở đây bốn so với một phẩy không ba."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Gộp mọi nhóm vào một con số: kết luận đảo ngược khi tách nhóm.</div>'
           + "<p>Trong ví dụ: A tốt hơn ở <b>mọi</b> loại giao dịch, nhưng B có tỉ lệ chung cao hơn nhiều vì nhận nhiều giao dịch dễ. Phép thử: <b>luôn vẽ thêm theo nhóm quan trọng nhất</b> (loại giao dịch, vùng, thời gian) và hỏi “tỉ trọng các nhóm có như nhau không?”.</p>",
           """Lỗi thứ hai, của người đã đi làm, là gộp mọi nhóm vào một con số. Kênh A tốt hơn ở mọi loại giao dịch, nhưng kênh B có tỉ lệ chung cao hơn nhiều vì nhận nhiều giao dịch dễ. Phép thử là luôn vẽ thêm theo nhóm quan trọng nhất và hỏi tỉ trọng các nhóm có như nhau không.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng thang lôgarit mà không ghi, hoặc đọc thang lôgarit như thang thường.</div>' + run_block(P_LOG)
           + "<p>Đường thẳng trên thang lôgarit nghĩa là <b>tăng theo hệ số nhân</b>, không phải tăng đều. Phép thử: nhìn <b>nhãn trục</b>: các vạch $1, 10, 100, 1000$ cách đều nhau là thang lôgarit.</p>",
           """Lỗi thứ ba, của người đã đi làm, là dùng thang lôgarit mà không ghi, hoặc đọc thang lôgarit như thang thường. Đường thẳng trên thang lôgarit nghĩa là tăng theo hệ số nhân, không phải tăng đều. Phép thử là nhìn nhãn trục, vì nếu các vạch một, mười, một trăm, một nghìn cách đều nhau thì đó là thang lôgarit.""", clear=True),
    ], only=[0, 2])), checks=["round((103 - 99) / (100 - 99), 1) == 4.0"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b></p>
<ol><li>Chọn loại biểu đồ: (a) tổng tiền của $3$ kênh; (b) số giao dịch mỗi ngày trong $30$ ngày; (c) quan hệ giữa số giao dịch và doanh thu.</li>
<li>Biểu đồ cột có trục từ $99$, hai cột $100$ và $103$: cột hai <b>trông</b> cao gấp mấy lần cột một?</li>
<li>Nhìn lại biểu đồ B ở đầu bài và đọc theo thứ tự: tiêu đề, đơn vị, trục, thang. Chỗ nào cho thấy nó đánh lừa?</li></ol>
<p><b>Quyết định:</b> $10^6$ cặp (số giao dịch, doanh thu) cần xem quan hệ: vẽ <b>từng điểm</b> hay <b>gộp</b> trước? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Câu một, chọn loại biểu đồ cho ba trường hợp trên màn hình. Câu hai, trục bắt đầu từ chín mươi chín, hai cột một trăm và một trăm lẻ ba, cột hai trông cao gấp mấy lần cột một. Câu ba, đọc lại biểu đồ bên phải ở đầu bài theo thứ tự và chỉ ra chỗ đánh lừa.
           Sau đó là một quyết định, một triệu cặp số cần xem quan hệ, vẽ từng điểm hay gộp trước, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "(a) cột, so sánh nhóm; (b) đường, theo thời gian; (c) phân tán, hai số"], ["2", "$\\frac{103 - 99}{100 - 99} = 4$ lần (tỉ lệ thật chỉ $1{,}03$)"], ["3", "tiêu đề và đơn vị đều đúng, thang đều; <b>trục bắt đầu ở $99$ chứ không phải $0$</b>: phần cột nhô lên bị phóng đại"]]),
           """Đáp án như sau. Câu một, tổng tiền của ba kênh là cột, số giao dịch theo ngày là đường, quan hệ hai số là phân tán. Câu hai, bốn lần, vì phần cột nhô lên trên gốc trục là bốn so với một, trong khi tỉ lệ thật chỉ một phẩy không ba. Câu ba, tiêu đề, đơn vị và thang đều ổn, nhưng trục bắt đầu ở chín mươi chín chứ không phải không, nên phần cột nhô lên bị phóng đại."""),
        st("<div class='box key'><b>Quyết định:</b> <b>gộp trước</b>. Một triệu điểm chồng thành đám kín (không thấy chỗ dày chỗ thưa), vẽ chậm, và tệp vector phình tỉ lệ với số điểm. "
           "Gộp thành ô lục giác hoặc lấy mẫu giữ lại cấu trúc; nhưng ghi rõ cách gộp và thử gộp theo nhóm quan trọng để không bị đánh lừa.</div>",
           """Quyết định, gộp trước. Một triệu điểm chồng thành đám kín, vẽ chậm, và tệp vector phình tỉ lệ với số điểm. Gộp thành ô lục giác hoặc lấy mẫu giữ lại cấu trúc. Nhưng phải ghi rõ cách gộp và thử gộp theo nhóm quan trọng để không bị đánh lừa.""", clear=True),
    ], checks=["round((103 - 99) / (100 - 99)) == 4"])
    sc_prac = practice_scene(sc, "Tự làm: vẽ một biểu đồ cột và mô tả đúng bằng số liệu vẽ", pr_steps(
        st, "PYT", "L11",
        """<p><b>Đề</b> (cần môi trường ảo đã cài thư viện): tạo <code>ve_bieu_do.py</code>. Ba dòng đầu nạp thư viện và chọn chế độ vẽ ra tệp (như ví dụ). Dữ liệu: <code>kenh = ["atm", "app", "quay"]</code>, <code>tong = [4200, 6100, 1500]</code> (nghìn đồng). Vẽ biểu đồ cột có <b>tiêu đề</b> <code>Tong tien theo kenh (nghin dong)</code> và nhãn trục y, lưu <code>bieu_do.png</code>. Rồi in <b>năm dòng</b> (xem <code>de.md</code>): vẽ xong chưa; chiều cao các cột; trục y có bắt đầu từ $0$ không; tiêu đề; kênh lớn nhất gấp mấy lần kênh nhỏ nhất.</p>""",
        """Bây giờ tới phần bạn tự làm, trong môi trường ảo đã cài thư viện. Vẽ biểu đồ cột tổng tiền của ba kênh, có tiêu đề và nhãn trục, lưu ra một tệp ảnh. Rồi in năm dòng đọc lại từ chính biểu đồ. Đã vẽ xong chưa, chiều cao các cột, trục dọc có bắt đầu từ không không, tiêu đề, và kênh lớn nhất gấp mấy lần kênh nhỏ nhất.
        Hãy dừng video và làm.""",
        LAB_OUT, "ve_bieu_do.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>fig, ax = plt.subplots()</code>, <code>ax.bar(kenh, tong)</code>, <code>ax.set_title(...)</code>, <code>ax.set_ylabel(...)</code>, <code>fig.savefig("bieu_do.png")</code>. Đọc lại: <code>[int(p.get_height()) for p in ax.patches]</code>, <code>ax.get_ylim()[0] == 0</code>, <code>ax.get_title()</code>. Lời giải ở <code>labs/PYT/L11/loi_giai.py</code>.</div>""",
        """Nếu kẹt, dựng khung, vẽ cột, đặt tiêu đề và nhãn trục đứng, lưu ảnh. Rồi đọc lại chiều cao các cột từ các hình đã vẽ, khoảng của trục dọc và tiêu đề. Kênh lớn nhất và nhỏ nhất tìm bằng vị trí của giá trị lớn nhất và nhỏ nhất.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=360), "PYT", "L11")
    write_lab("PYT", "L11", """# Lab PYT L11 — Vẽ một biểu đồ cột và mô tả đúng bằng số liệu vẽ

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `ve_bieu_do.py`. Ba dòng đầu:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

Dữ liệu (số minh hoạ; khác ví dụ trong bài): `kenh = ["atm", "app", "quay"]`, `tong = [4200, 6100, 1500]` (nghìn đồng).

1. Vẽ biểu đồ cột (`ax.bar`), tiêu đề **`Tong tien theo kenh (nghin dong)`**, nhãn trục y; lưu `bieu_do.png`.
2. In năm dòng, **đọc lại từ chính biểu đồ** (`ax.patches`, `ax.get_ylim()`, `ax.get_title()`):
   `Ve xong: <True/False>` (tệp tồn tại) · `Do cao cot: [..]` (số nguyên) · `Truc y bat dau tu 0: <True/False>` · `Tieu de: …` · `Lon nhat: <kênh> - gap <x> lan nho nhat` (làm tròn 1 chữ số).

Lab kiểm **số liệu vẽ**, không so ảnh. Chạy: `python ve_bieu_do.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L11 ve_bieu_do.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("câu hỏi quyết định loại biểu đồ: cột, đường, phân tán, tần suất", "đọc trục trước: gốc, thang, đơn vị", "cột phải bắt đầu từ 0",
                 "gộp có thể đảo ngược kết luận: vẽ thêm theo nhóm", "thang lôgarit: đường thẳng là tăng theo hệ số nhân", "dữ liệu lớn: gộp trước, rồi vẽ"),
           """Tổng kết chuỗi logic. Câu hỏi quyết định loại biểu đồ, cột, đường, phân tán, tần suất. Đọc trục trước, gốc, thang và đơn vị. Cột phải bắt đầu từ không. Gộp có thể đảo ngược kết luận, nên vẽ thêm theo nhóm. Trên thang lôgarit, đường thẳng là tăng theo hệ số nhân.
           Và khi dữ liệu lớn, gộp trước rồi mới vẽ."""),
        st("""<div class='box key'><b>Tư duy:</b> một biểu đồ là một <b>lập luận</b>. Trước khi tin hay đưa ra một biểu đồ, hỏi: <b>trục bắt đầu từ đâu?</b>, <b>đã gộp những gì?</b>, <b>thang gì?</b>, và <b>số liệu vẽ có khớp dữ liệu không?</b></div>
<p>Bài sau: kiểm thử tự động, để mỗi lần sửa mã, máy tự kiểm lại các số mà ta đã tin.</p>""",
           """Một biểu đồ là một lập luận. Trước khi tin hay đưa ra một biểu đồ, hãy hỏi trục bắt đầu từ đâu, đã gộp những gì, thang gì, và số liệu vẽ có khớp dữ liệu không.
           Bài sau, ta học kiểm thử tự động.""", forward_ref=True),
    ])
    return lesson("L11", "ve_bieu_do_va_doc_bieu_do", "Bài 11 — Vẽ biểu đồ và đọc biểu đồ cho đúng",
                  "curriculum/pyt.yaml L11; audit/pyt/verify_pyt.py L11 (chạy thật trên Python 3.11, labs/.venv-pyt: matplotlib 3.11.2 theo labs/requirements-py.txt, chế độ Agg; biểu đồ trên màn hình vẽ lại bằng SVG từ đúng số liệu mà verify_pyt đọc từ đối tượng biểu đồ; thời gian và kích thước đo bằng verify_pyt, máy kiểm, số minh hoạ); "
                  "Matplotlib documentation: Quick start guide, Backends, Scales; Tufte, The Visual Display of Quantitative Information (1983, nguyên tắc cột bắt đầu từ 0 — NOT_VERIFIED trang); "
                  "hiện tượng đảo kết luận khi gộp (nghịch lý Simpson, Simpson 1951 — NOT_VERIFIED trang); số liệu hai kênh là số minh hoạ",
                  ["Nêu loại biểu đồ hợp với từng câu hỏi: cột, đường, phân tán, tần suất",
                   "Vẽ biểu đồ ra tệp ảnh và đọc lại số liệu đã vẽ từ đối tượng biểu đồ",
                   "Đọc một biểu đồ theo thứ tự tiêu đề, đơn vị, trục, thang, rồi mới đến hình",
                   "Tính tỉ lệ nhìn thấy khi trục bị cắt và so với tỉ lệ dữ liệu",
                   "Giải thích vì sao gộp có thể đảo ngược kết luận và cách phát hiện",
                   "Nêu thời gian vẽ và kích thước tệp thay đổi thế nào ở ba quy mô, và vì sao phải gộp",
                   "Chỉ ra ba lỗi hay gặp: cắt trục ở biểu đồ cột, gộp che nhóm, nhầm thang lôgarit",
                   "Vẽ và mô tả đúng một biểu đồ cột bằng số liệu vẽ"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy"],
                  covers=[(1, "intuition"), (2, "formula"), (3, "example"), (4, "formula"), (5, "formula"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
