from lib import *
from labkit import write_lab, practice_steps, practice_scene

TB = "so_tien = np.array([[500, 1200, 300, 800], [200, 900, 450, 100], [1500, 700, 600, 2000]])"
V = "venv"
R_TAO = repl("Tao", [
    ("import numpy as np", ""), (TB, ""), ("so_tien.shape", "(3, 4)"), ("so_tien.dtype", "dtype('int64')"), ("so_tien.ndim", "2"),
    ("print(so_tien[1, 2])", "450"), ("print(so_tien[:, 0])", "[ 500  200 1500]"),
], env=V)
R_OP = repl("PhanTu", [
    ("import numpy as np", ""), (TB, ""), ("print(so_tien * 2)", "[[1000 2400  600 1600]\n [ 400 1800  900  200]\n [3000 1400 1200 4000]]"),
    ("print(np.array([1, 2, 3]) * np.array([10, 20, 30]))", "[10 40 90]"),
    ("print(so_tien + np.array([10, 20, 30, 40]))", "[[ 510 1220  330  840]\n [ 210  920  480  140]\n [1510  720  630 2040]]"),
], env=V)
R_AXIS = repl("Truc", [
    ("import numpy as np", ""), (TB, ""), ("print(so_tien.sum(axis=0))", "[2200 2800 1350 2900]"), ("print(so_tien.sum(axis=1))", "[2800 1650 4800]"),
    ("print(so_tien.sum())", "9250"), ("print(so_tien.sum(axis=0).shape)", "(4,)"),
], env=V)
R_EX2 = repl("VeTaiKhoan", [
    ("import numpy as np", ""), (TB, ""), ("print(so_tien.mean(axis=1))", "[ 700.   412.5 1200. ]"),
    ("print(so_tien[so_tien > 1000])", "[1200 1500 2000]"), ("print((so_tien > 1000).sum())", "3"),
], env=V)
R_ROW = repl("CongMotHang", [
    ("import numpy as np", ""), (TB, ""), ("print(so_tien + np.array([10, 20, 30, 40]))", "[[ 510 1220  330  840]\n [ 210  920  480  140]\n [1510  720  630 2040]]"),
], env=V)
R_BC = repl("LanTruyen", [
    ("import numpy as np", ""), (TB, ""),
    ("so_tien + np.array([1, 2, 3])", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nValueError: operands could not be broadcast together with shapes (3,4) (3,) '),
    ("print(so_tien + np.array([[1], [2], [3]]))", "[[ 501 1201  301  801]\n [ 202  902  452  102]\n [1503  703  603 2003]]"),
], env=V)
R_STD = repl("DoLech", [
    ("import numpy as np", ""), ("x = np.array([2, 4, 4, 4, 5, 5, 7, 9])", ""), ("print(x.mean())", "5.0"), ("print((x - x.mean()) ** 2)", "[ 9.  1.  1.  1.  0.  0.  4. 16.]"),
    ("print(((x - x.mean()) ** 2).mean())", "4.0"), ("print(np.sqrt(4.0))", "2.0"), ("print(x.std())", "2.0"),
], env=V)
R_NORM = repl("ChuanHoa", [
    ("import numpy as np", ""), ("a = np.array([[1., 10.], [2., 20.], [3., 30.]])", ""),
    ("print((a - a.mean(axis=0)) / a.std(axis=0))", "[[-1.22474487 -1.22474487]\n [ 0.          0.        ]\n [ 1.22474487  1.22474487]]"),
], env=V)
R_Q = repl("Quiz", [
    ("import numpy as np", ""), ("a = np.array([[1, 2, 3], [4, 5, 6]])", ""), ("print(a.sum(axis=0))", "[5 7 9]"), ("print(a.sum(axis=1))", "[ 6 15]"),
    ("print(a + np.array([10, 20, 30]))", "[[11 22 33]\n [14 25 36]]"),
], env=V)

P_INT = py("tran_so", '''import numpy as np

a = np.array([2000000000], dtype=np.int32)
print(a + a)
b = a.astype(np.int64)
print(b + b)''', "[-294967296]\n[4000000000]", env=V)
P_VIEW = py("lat_cat_view", '''import numpy as np

a = np.array([10, 20, 30, 40])
b = a[1:3]
b[0] = 999
print(a)
c = a[1:3].copy()
c[0] = 0
print(a)''', "[ 10 999  30  40]\n[ 10 999  30  40]", env=V)
P_PY = py("tong_cot", '''bang = [[500, 1200, 300, 800], [200, 900, 450, 100], [1500, 700, 600, 2000]]
tong_cot = [0, 0, 0, 0]
for hang in bang:
    for j in range(4):
        tong_cot[j] = tong_cot[j] + hang[j]
print(tong_cot)''', "[2200, 2800, 1350, 2900]")
measure("l09_sum", '''import json, time, tracemalloc
import numpy as np
res = {}
for k, n in (("1e4", 10 ** 4), ("1e6", 10 ** 6), ("1e7", 10 ** 7)):
    xs = list(range(n))
    reps = max(1, 10 ** 6 // n)
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        for _ in range(reps):
            s = 0
            for x in xs:
                s += x
        best = min(best, (time.perf_counter() - t0) / reps)
    res["t_loop_" + k] = best
    del xs
    a = np.arange(n, dtype=np.int64)
    reps2 = max(1, 10 ** 7 // n)
    best2 = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        for _ in range(reps2):
            s2 = int(a.sum())
        best2 = min(best2, (time.perf_counter() - t0) / reps2)
    res["t_np_" + k] = best2
    assert s == s2
    res["bytes_np_" + k] = a.nbytes
tracemalloc.start()
xs = list(range(10 ** 6))
res["m_list_1e6"] = tracemalloc.get_traced_memory()[0]
tracemalloc.stop()
print(json.dumps(res))''', env=V)

LAB_SOL = '''import numpy as np

so_lieu = np.array([[120, 4000], [150, 5200], [90, 3100], [200, 6100], [140, 4600]], dtype=float)
tb = so_lieu.mean(axis=0)
do_lech = so_lieu.std(axis=0)
chuan = (so_lieu - tb) / do_lech
print("Trung binh:", np.round(tb, 2))
print("Do lech chuan:", np.round(do_lech, 2))
print(np.round(chuan, 3))
print("Trung binh cot sau chuan hoa ~ 0:", np.allclose(chuan.mean(axis=0), 0))
print("Do lech chuan cot sau chuan hoa:", np.round(chuan.std(axis=0), 6))'''
LAB_OUT = """Trung binh: [ 140. 4600.]
Do lech chuan: [  36.33 1021.76]
[[-0.55  -0.587]
 [ 0.275  0.587]
 [-1.376 -1.468]
 [ 1.651  1.468]
 [ 0.     0.   ]]
Trung binh cot sau chuan hoa ~ 0: True
Do lech chuan cot sau chuan hoa: [1. 1.]"""
P_LAB = py("lab_l09", LAB_SOL, LAB_OUT, env=V)


def build():
    tl = {k: M("l09_sum", "t_loop_" + k) for k in ("1e4", "1e6", "1e7")}
    tn = {k: M("l09_sum", "t_np_" + k) for k in ("1e4", "1e6", "1e7")}
    stl = {k: t_show(v) for k, v in tl.items()}
    stn = {k: t_show(v) for k, v in tn.items()}
    # tỉ số tính từ chính các số ĐÃ LÀM TRÒN hiện trên màn hình, để bảng, lời đọc và tiêu đề không mâu thuẫn nhau
    def shown_sec(txt):
        v, u = txt[2:].split()
        return float(v.replace(",", ".")) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1}[u]
    gap = {k: vnum(sig(shown_sec(stl[k][0]) / shown_sec(stn[k][0]))) for k in tl}
    stl8, stn8 = t_show(shown_sec(stl["1e7"][0]) * 10), t_show(shown_sec(stn["1e7"][0]) * 10)
    nb6, nb7 = M("l09_sum", "bytes_np_1e6"), M("l09_sum", "bytes_np_1e7")
    ml = M("l09_sum", "m_list_1e6")
    bn6, bn8, bl6, bl8 = b_show(nb6), b_show(nb7 * 10), b_show(ml), b_show(ml * 100)
    HT = "hàng chục đến hàng trăm"  # hệ số đo được khác nhau giữa các quy mô và giữa các máy: không nêu một số tròn chung
    sc_hook = sc("hook", "hook", f"Một triệu số: mảng nhanh hơn vòng lặp {HT} lần", [
        st(table(["một triệu số nguyên", "thời gian (đo trên máy kiểm, số minh hoạ)", "bộ nhớ"],
                 [["vòng lặp trên danh sách", stl["1e6"][0], bl6[0]], ["một lệnh trên mảng", stn["1e6"][0], bn6[0]], ["nhanh gấp", f"≈ {gap['1e6']} lần", "ít hơn ≈ " + vnum(sig(ml / nb6)) + " lần"]])
           + "<p class='note'>ms = phần nghìn giây; µs = phần triệu giây; MB = triệu byte.</p>",
           f"""Chào bạn, hãy cộng một triệu số. Bằng vòng lặp trên danh sách, trên máy kiểm mất {stl['1e6'][1]} và chiếm {bl6[1]} bộ nhớ. Bằng một lệnh trên mảng, mất {stn['1e6'][1]} và chỉ chiếm {bn6[1]}. Nhanh hơn khoảng {words(int(gap['1e6'].replace(' ', '')))} lần, và nhẹ hơn nhiều lần.
           Số đo trên máy kiểm, số minh hoạ. Với dữ liệu phân tích, đây là khác biệt giữa chờ một giây và chờ một phút."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li><b>Mảng</b> khác danh sách ở đâu, và <b>hình dạng</b> của nó nói gì?</li>
<li>Tính <b>theo từng phần tử</b>, <b>lan truyền</b> và tính theo <b>trục</b> hoạt động ra sao?</li>
<li>Vì sao mảng nhanh hơn vòng lặp, và <b>giới hạn</b> của nó là gì?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, mảng khác danh sách ở đâu, và hình dạng của nó nói gì. Hai, tính theo từng phần tử, lan truyền và tính theo trục hoạt động ra sao. Ba, vì sao mảng nhanh hơn vòng lặp, và giới hạn của nó là gì."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: danh sách, vòng lặp, môi trường ảo và thư viện đã cài", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① danh sách và vòng lặp", "<code>for x in ds: tong = tong + x</code>: mỗi lượt một phần tử, Python làm từng lệnh một"],
                  ["② cắt lát danh sách", "<code>ds[1:3]</code> tạo danh sách <b>mới</b> (bản sao)"],
                  ["③ thư viện ngoài", "cài vào môi trường ảo từ tệp ghim; nạp bằng <code>import numpy as np</code> (<code>as</code> đặt tên ngắn)"]]),
           """Ta ôn lại ba điều. Vòng lặp lấy từng phần tử một và làm từng lệnh một. Cắt lát danh sách tạo danh sách mới. Và thư viện ngoài được cài vào môi trường ảo từ tệp ghim, rồi nạp bằng lệnh nạp với tên ngắn. Bài này dùng thư viện tính trên mảng, đã có trong tệp ghim của khoá, nên hãy chạy trong môi trường ảo đã cài.""",
           focus=[1, "1.2", "1.3", "1.4", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã mảng, hình dạng, trục, lan truyền và mặt nạ", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>np.array([[1, 2], [3, 4]])</code>", "tạo mảng", "mảng 2 chiều: hàng nhìn từ trên xuống, cột từ trái sang; mọi phần tử <b>cùng một kiểu</b>"],
                  ["<code>a.shape</code>, <code>a.dtype</code>, <code>a.ndim</code>", "hình dạng, kiểu, số chiều", "<code>(3, 4)</code> = 3 hàng 4 cột; <code>int64</code> = số nguyên 8 byte; <code>ndim</code> = 2"],
                  ["<code>a[1, 2]</code>, <code>a[:, 0]</code>", "chỉ số, cắt cột", "hàng <code>1</code> cột <code>2</code> (đếm từ $0$); <code>:</code> = mọi hàng, cột <code>0</code>"]]),
           """Bảng đầu là mảng. Mảng hai chiều có hàng và cột, mọi phần tử cùng một kiểu. Hình dạng cho biết số hàng và số cột, kiểu cho biết loại số và cỡ, số chiều là hai. Chỉ số đặt hàng trước cột, đếm từ không. Dấu hai chấm nghĩa là mọi hàng, nên lấy cột không của mọi hàng."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>a * 2</code>, <code>a + b</code>", "tính theo phần tử", "mỗi ô một phép tính, không cần vòng lặp"],
                  ["<code>a.sum(axis=0)</code>, <code>a.sum(axis=1)</code>", "tính theo trục", "trục <code>0</code> chạy dọc hàng → <b>một kết quả cho mỗi cột</b>; trục <code>1</code> → một kết quả cho mỗi hàng"],
                  ["<code>a.mean()</code>, <code>a.std()</code>", "trung bình, độ lệch chuẩn", "độ lệch chuẩn = căn của trung bình các <b>bình phương độ lệch so với trung bình</b>"],
                  ["<code>a[a &gt; 1000]</code>", "mặt nạ", "<code>a &gt; 1000</code> cho mảng đúng/sai cùng hình dạng; dùng nó làm chỉ số để lấy phần tử thoả. Cộng mặt nạ, <code>(a &gt; 1000).sum()</code>: <code>True</code> tính là $1$, <code>False</code> là $0$, nên tổng là <b>số phần tử đúng</b>"]]),
           """Bảng thứ hai là phép tính. Phép tính theo phần tử làm mỗi ô một phép tính mà không cần vòng lặp. Tính theo trục không chạy dọc hàng cho mỗi cột một kết quả, còn trục một cho mỗi hàng một kết quả. Trung bình và độ lệch chuẩn, trong đó độ lệch chuẩn là căn của trung bình các bình phương độ lệch so với trung bình.
           Cuối cùng là mặt nạ, một mảng đúng sai dùng làm chỉ số để lấy các phần tử thoả điều kiện. Cộng một mặt nạ thì đúng tính là một, sai tính là không, nên tổng là số phần tử đúng.""".replace("Tính theo trục không chạy dọc hàng", "Tính theo trục không là chạy dọc hàng"),
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: trục là hướng gộp; lan truyền là kéo dài hàng cho khớp", [
        st(svg(1500, 450,
               *[box(40 + j * 150, 60 + i * 80, 140, 70, [str(v)], C_BLUE, 26, True) for i, row in enumerate([[500, 1200, 300, 800], [200, 900, 450, 100], [1500, 700, 600, 2000]]) for j, v in enumerate(row)],
               txt(340, 40, "so_tien: hình dạng (3, 4)", 26, "middle", "#1f2937", True),
               *[arrow(110 + j * 150, 310, 110 + j * 150, 345, "#16a34a") for j in range(4)],
               *[box(40 + j * 150, 350, 140, 60, [str(v)], C_GREEN, 24, True) for j, v in enumerate([2200, 2800, 1350, 2900])],
               txt(340, 438, "sum(axis=0): gộp theo hàng, còn 4 số", 22, "middle", "#16a34a", True),
               *[arrow(650, 95 + i * 80, 700, 95 + i * 80, "#d97706") for i in range(3)],
               *[box(705, 60 + i * 80, 150, 70, [str(v)], C_AMBER, 26, True) for i, v in enumerate([2800, 1650, 4800])],
               txt(780, 40, "sum(axis=1): còn 3 số", 22, "middle", "#d97706", True),
               txt(1190, 120, "trục = hướng bị GỘP lại", 28, "middle", "#1f2937", True),
               txt(1190, 170, "axis=0: gộp dọc, mất chiều hàng", 24, "middle", "#16a34a"),
               txt(1190, 210, "axis=1: gộp ngang, mất chiều cột", 24, "middle", "#d97706"),
               txt(1190, 280, "kết quả còn lại là chiều KHÔNG gộp", 24, "middle", "#1f2937")),
           """Hình này giải thích trục. Mảng có ba hàng và bốn cột. Tính tổng theo trục không là gộp dọc theo các hàng, mất chiều hàng, nên còn bốn số, mỗi cột một số. Tính tổng theo trục một là gộp ngang theo các cột, nên còn ba số, mỗi hàng một số. Quy tắc nhớ là trục chỉ hướng bị gộp lại, kết quả là chiều còn lại."""),
        st(svg(1500, 400,
               *[box(40 + j * 130, 50 + i * 70, 120, 60, [str(v)], C_BLUE, 24, True) for i, row in enumerate([[500, 1200, 300, 800], [200, 900, 450, 100], [1500, 700, 600, 2000]]) for j, v in enumerate(row)],
               txt(300, 35, "so_tien: mảng (3, 4)", 24, "middle", "#1f2937", True),
               txt(595, 130, "+", 44, "middle", "#1f2937", True),
               *[box(640 + j * 130, 120, 120, 60, [str(v)], C_AMBER, 24, True) for j, v in enumerate([10, 20, 30, 40])],
               txt(900, 105, "hàng (4,)", 24, "middle", "#d97706", True),
               *[box(640 + j * 130, 220, 120, 45, ["10 20 30 40"[j * 3:j * 3 + 2]], C_GRAY, 20) for j in range(4)],
               txt(900, 290, "máy kéo dài hàng này xuống 3 lần cho khớp", 24, "middle", "#6b7280"),
               txt(750, 345, "khớp từ bên PHẢI sang: (3, 4) với (4,) → 4 = 4: được", 26, "middle", "#16a34a", True),
               txt(750, 385, "(3, 4) với (3,) → 4 ≠ 3: lỗi, vì hàng 3 số không kéo dài thành 4 cột", 26, "middle", "#dc2626", True)),
           """Hình thứ hai là lan truyền. Khi cộng một mảng ba hàng bốn cột với một hàng bốn số, máy kéo dài hàng đó xuống ba lần cho khớp rồi cộng từng ô. Quy tắc là so các kích thước từ bên phải sang. Ba hàng bốn cột với một hàng bốn số khớp ở bốn. Nhưng với một hàng ba số thì bốn khác ba, nên có lỗi.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: theo phần tử, theo trục, lan truyền, độ lệch chuẩn", [
        st(repl_block(R_OP, 0, 4, title="Bước 1. Phép tính theo phần tử: mỗi ô một phép")
           + "<p>Hai dòng đầu nạp thư viện và dựng bảng <code>so_tien</code> dùng suốt bài (ba tài khoản, bốn tuần). Vì <code>so_tien * 2</code> áp dụng cho <b>từng ô</b>, ô đầu $500 \\to 1000$. Hai mảng cùng hình dạng thì nhân từng cặp ô: $1 \\cdot 10,\\ 2 \\cdot 20,\\ 3 \\cdot 30$ cho <code>[10 40 90]</code>.</p>",
           """Bước một, tính theo phần tử. Hai dòng đầu nạp thư viện và dựng bảng ba tài khoản, bốn tuần, dùng suốt bài. Vì phép nhân với hai áp dụng cho từng ô, ô đầu năm trăm thành một nghìn. Hai mảng cùng hình dạng thì nhân từng cặp ô, một nhân mười, hai nhân hai mươi, ba nhân ba mươi, cho ra mười, bốn mươi, chín mươi. Không có vòng lặp nào ở phía người viết."""),
        st(repl_block(R_AXIS, 0, 6, title="Bước 2. Theo trục: hình dạng kết quả là chiều không gộp")
           + "<p>Vì <code>axis=0</code> gộp các hàng, còn $4$ số: $500 + 200 + 1500 = 2200$. <code>axis=1</code> gộp các cột: $500 + 1200 + 300 + 800 = 2800$. Cả hai phải cho tổng chung $9250$: $2200 + 2800 + 1350 + 2900 = 9250$ ✓</p>",
           """Bước hai, tính theo trục. Vì trục không gộp các hàng, còn bốn số, mỗi cột một tổng, ví dụ cột đầu là năm trăm cộng hai trăm cộng một nghìn năm trăm, bằng hai nghìn hai trăm. Trục một gộp các cột, còn ba số, mỗi hàng một tổng. Cả hai cách cho cùng tổng chung chín nghìn hai trăm năm mươi, và hình dạng kết quả là chiều không bị gộp.""", clear=True),
        st(repl_block(R_ROW, title="Bước 3. Lan truyền: một hàng bốn số được kéo dài xuống cho khớp")
           + "<p>Hình dạng <code>(3, 4)</code> và <code>(4,)</code>: so từ phải, $4 = 4$, nên máy kéo hàng $[10, 20, 30, 40]$ xuống cả ba hàng rồi cộng từng ô. <code>(4,)</code> là hình dạng của mảng <b>một chiều</b> có $4$ số (dấu phẩy sau $4$ để phân biệt với chính số $4$).</p>",
           """Bước ba, lan truyền. Cộng bảng ba hàng bốn cột với một hàng bốn số. So kích thước từ bên phải, bốn bằng bốn, nên máy kéo hàng đó xuống cả ba hàng rồi cộng từng ô, và mỗi hàng của bảng được cộng cùng một hàng bốn số.""", clear=True),
        st(repl_block(R_BC, title="Khi không khớp: lỗi, và cách sửa bằng một cột")
           + "<p>Vì <code>(3, 4)</code> và <code>(3,)</code>: so từ phải, $4$ với $3$ khác nhau và không bên nào bằng $1$ nên lỗi. Đổi hàng thành <b>cột</b> <code>(3, 1)</code>: $1$ được kéo dài thành $4$, mỗi hàng cộng một số riêng.</p>",
           """Còn với mảng ba số thì bị lỗi, vì so từ bên phải thì bốn khác ba, và không bên nào bằng một. Muốn cộng mỗi hàng một số riêng, ta đổi thành một cột ba hàng một cột. Kích thước một được kéo dài thành bốn, và hàng thứ nhất cộng một, hàng thứ hai cộng hai, hàng thứ ba cộng ba.""", clear=True),
        st(repl_block(R_STD, 0, 7, title="Bước 4. Độ lệch chuẩn tính từ định nghĩa")
           + "<p>Tám số $2, 4, 4, 4, 5, 5, 7, 9$ có trung bình $5$; bình phương độ lệch: $(2-5)^2 = 9$, … , $(9-5)^2 = 16$; trung bình của chúng $= 4$; căn $= 2$ (<code>np.sqrt</code> lấy căn bậc hai). Khớp với <code>x.std()</code> ✓</p>",
           """Bước bốn, độ lệch chuẩn từ định nghĩa. Ta lập mảng tám số hai, bốn, bốn, bốn, năm, năm, bảy, chín, có trung bình năm. Bình phương độ lệch của từng số so với trung bình là chín, một, một, một, không, không, bốn, mười sáu. Trung bình các bình phương đó bằng bốn, lấy căn được hai. Lệnh có sẵn cho cùng kết quả hai, nên ta tin nó.""", clear=True),
    ], checks=["500 + 200 + 1500 == 2200 and 500 + 1200 + 300 + 800 == 2800", "2200 + 2800 + 1350 + 2900 == 9250 and 2800 + 1650 + 4800 == 9250",
               "(2 + 4 + 4 + 4 + 5 + 5 + 7 + 9) / 8 == 5 and ((2 - 5) ** 2 + 0 + 0 + 0 + 0 + 0 + 0 + (9 - 5) ** 2) >= 0", "(9 + 1 + 1 + 1 + 0 + 0 + 4 + 16) / 8 == 4"])
    sc_ex = sc("example", "example", "Ví dụ: thống kê theo tuần và theo tài khoản, mặt nạ, chuẩn hoá cột", [
        st(repl_block(R_TAO, 0, 7, title="Dựng bảng giao dịch: 3 tài khoản × 4 tuần (nghìn đồng)"),
           """Ví dụ một, dựng bảng. Ba tài khoản, bốn tuần, đơn vị nghìn đồng. Hình dạng ba hàng bốn cột, kiểu số nguyên tám byte, hai chiều. Chỉ số một hai lấy tài khoản thứ hai ở tuần thứ ba, bốn trăm năm mươi. Cắt cột không cho giao dịch của cả ba tài khoản ở tuần đầu."""),
        st(repl_block(R_EX2, title="Trung bình mỗi tài khoản, rồi giao dịch trên một triệu đồng (1 000 nghìn)")
           + "<p>Mặt nạ đúng/sai: <code>True</code> tính là $1$, <code>False</code> là $0$, nên <code>(so_tien &gt; 1000).sum()</code> đếm số phần tử đúng.</p>",
           """Ví dụ hai, trung bình theo từng tài khoản, trục một. Tài khoản đầu trung bình bảy trăm, tài khoản thứ hai bốn trăm mười hai phẩy năm, tài khoản thứ ba một nghìn hai trăm. Rồi dùng mặt nạ lấy các giao dịch trên một nghìn, tức trên một triệu đồng. Có ba giao dịch, một nghìn hai trăm, một nghìn năm trăm và hai nghìn. Cộng mặt nạ cho số phần tử đúng, vì đúng tính là một và sai là không.""", clear=True),
        st(repl_block(R_NORM, title="Chuẩn hoá từng cột: trừ trung bình cột, chia độ lệch chuẩn cột")
           + "<p>Vì <code>a.mean(axis=0)</code> có hình dạng <code>(2,)</code> nên lan truyền lên từng hàng; cột nào cũng quy về trung bình $0$, độ lệch chuẩn $1$: <code>[-1.22, 0, 1.22]</code>. Viết <code>1.</code> (có dấu chấm) là số thực $1{,}0$, nên <code>[1., 10.]</code> là <code>[1.0, 10.0]</code> và cả mảng là số thực.</p>",
           """Ví dụ ba, chuẩn hoá cột. Số một viết kèm dấu chấm là số thực, nên mảng này toàn số thực. Ta trừ trung bình của từng cột rồi chia cho độ lệch chuẩn của cột đó. Vì trung bình theo cột có hình dạng hai số nên được lan truyền lên từng hàng. Kết quả là hai cột có thang đo giống nhau, mỗi cột trung bình không, độ lệch chuẩn một. Cột một và cột hai có số rất khác nhau về độ lớn, nay đã so sánh được.""", clear=True),
    ], checks=["(500 + 1200 + 300 + 800) / 4 == 700 and (200 + 900 + 450 + 100) / 4 == 412.5 and (1500 + 700 + 600 + 2000) / 4 == 1200",
               "len([x for x in [500, 1200, 300, 800, 200, 900, 450, 100, 1500, 700, 600, 2000] if x > 1000]) == 3"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cộng cột bằng hai vòng lặp, và tổng chung hai cách", [
        st(run_block(P_PY, title="Cộng từng cột bằng hai vòng lặp thuần Python"),
           """Đường kiểm khác, không dùng mảng. Hai vòng lặp lồng nhau cộng từng cột. Chúng cho đúng bốn số, hai nghìn hai trăm, hai nghìn tám trăm, một nghìn ba trăm năm mươi, hai nghìn chín trăm. Bốn số này trùng với kết quả tính theo trục không của mảng. Tổng bốn số vẫn là chín nghìn hai trăm năm mươi, trùng tổng chung.""")
        , st("<p>Hai đường độc lập cùng cho $[2200, 2800, 1350, 2900]$ và tổng $9250$; trung bình tổng thể $\\frac{9250}{12} \\approx 770{,}83$, trùng <code>so_tien.mean()</code> $= 770{,}8333$ ✓</p>",
             """Thêm một phép thử nữa. Vì tổng chia cho số ô chính là trung bình, chín nghìn hai trăm năm mươi chia mười hai ô bằng bảy trăm bảy mươi phẩy tám ba, trùng với trung bình của cả mảng. Ba cách đều khớp.""", clear=True),
    ], checks=["[500 + 200 + 1500, 1200 + 900 + 700, 300 + 450 + 600, 800 + 100 + 2000] == [2200, 2800, 1350, 2900]", "round(9250 / 12, 2) == 770.83"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn dần: mảng nhanh hơn nhiều lần, nhưng vẫn phải nằm vừa bộ nhớ", [
        st(table(["số phần tử", "vòng lặp Python", "một lệnh trên mảng", "nhanh gấp"],
                 [["×1: 10 000", stl["1e4"][0], stn["1e4"][0], f"≈ {gap['1e4']}"], ["×100: 1 000 000", stl["1e6"][0], stn["1e6"][0], f"≈ {gap['1e6']}"],
                  ["×1 000: 10 000 000", stl["1e7"][0], stn["1e7"][0], f"≈ {gap['1e7']}"], ["×10 000 (ngoại suy): 100 000 000", stl8[0], stn8[0], "—"]])
           + "<p class='note'>Đo trên máy kiểm, số minh hoạ. <b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo để đoán số ở quy mô chưa đo (ở đây từ mức mười triệu, nhân $10$). Hệ số “nhanh gấp” khác nhau giữa các quy mô và giữa các máy: chỉ nên nhớ cỡ hàng chục đến hàng trăm lần.</p>",
           f"""Bảng này là kết quả đo. Một vạn số, vòng lặp mất {stl['1e4'][1]}, mảng mất {stn['1e4'][1]}. Một triệu số, vòng lặp mất {stl['1e6'][1]}, mảng mất {stn['1e6'][1]}. Mười triệu số, vòng lặp mất {stl['1e7'][1]}, mảng mất {stn['1e7'][1]}. Hàng cuối là ngoại suy, nghĩa là nhân theo tỉ lệ từ số đã đo để đoán số ở quy mô chưa đo. Một trăm triệu số, vòng lặp cỡ {stl8[1]}, mảng cỡ {stn8[1]}. Hệ số nhanh gấp khác nhau giữa các quy mô và giữa các máy, nên chỉ nhớ cỡ hàng chục đến hàng trăm lần.""", introduces=["pyt_ngoai_suy"]),
        st(table(["số phần tử", "bộ nhớ mảng (8 byte mỗi số)", "bộ nhớ danh sách các số nguyên"],
                 [["1 000 000", bn6[0], bl6[0]], ["10 000 000", b_show(nb7)[0], b_show(ml * 10)[0] + " (ngoại suy)"], ["100 000 000", bn8[0], bl8[0] + " (ngoại suy)"]])
           + "<div class='box key'><b>Đánh đổi:</b> mảng nhanh vì dữ liệu nằm <b>liền nhau</b>, <b>cùng một kiểu</b>, và phép tính chạy bằng mã <b>đã biên dịch</b> (viết sẵn bằng ngôn ngữ gần máy hơn, đã dịch ra lệnh máy), không qua từng lệnh của Python. "
             "Nhưng mảng vẫn phải nằm <b>trọn trong bộ nhớ</b>: một trăm triệu số nguyên tám byte là 800 MB. Và nó nhanh nhất khi tính cả mảng một lệnh; quay lại vòng lặp từng phần tử thì mất lợi thế.</div>",
           f"""Cái giá nằm ở bộ nhớ. Một triệu số trong mảng chiếm {bn6[1]}, trong danh sách chiếm {bl6[1]}. Một trăm triệu số trong mảng chiếm {bn8[1]}, và trong danh sách cần cỡ {bl8[1]}. Mảng nhanh vì dữ liệu nằm liền nhau, cùng một kiểu, và phép tính chạy bằng mã đã biên dịch, nghĩa là mã viết sẵn bằng một ngôn ngữ gần máy hơn và đã dịch ra lệnh máy. Nhưng mảng vẫn phải nằm trọn trong bộ nhớ.
           Và nó nhanh nhất khi tính cả mảng bằng một lệnh. Số đo trên máy kiểm, số minh hoạ.""", clear=True, introduces=["pyt_bien_dich"]),
    ], checks=["10 ** 7 * 10 == 10 ** 8", "8 * 10 ** 8 == 800000000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Cộng hai mảng khác hình dạng, không khớp từ bên phải.</div>' + repl_block(R_BC, 0, 3)
           + "<p>Đọc dòng cuối: hình dạng <code>(3,4)</code> và <code>(3,)</code> không lan truyền được. Phép thử: <b>in <code>.shape</code></b> của từng mảng trước khi tính.</p>",
           """Lỗi thứ nhất, của người mới, là cộng hai mảng khác hình dạng, không khớp từ bên phải. Dòng cuối nói hai hình dạng không lan truyền được. Phép thử là in hình dạng của từng mảng trước khi tính."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Kiểu số nguyên nhỏ bị tràn mà không báo lỗi.</div>' + run_block(P_INT)
           + "<p>Hai tỉ cộng hai tỉ vượt $2^{31} - 1 = 2\\,147\\,483\\,647$ của số nguyên $4$ byte ($32$ bit: <b>bit</b> là một chữ số $0$ hoặc $1$, một byte có $8$ bit; một bit dành cho dấu): kết quả <b>quay vòng</b> thành số âm: $4\\,000\\,000\\,000 - 2^{32} = -294\\,967\\,296$. Không cảnh báo. Phép thử: so tổng với tính tay; đổi sang kiểu $8$ byte khi tổng có thể lớn.</p>",
           """Lỗi thứ hai, của người đã đi làm, là kiểu số nguyên nhỏ bị tràn mà không báo lỗi. Số nguyên bốn byte có ba mươi hai bit, mỗi bit là một chữ số không hoặc một, và một bit dành cho dấu, nên số lớn nhất chỉ hơn hai tỉ một trăm bốn mươi bảy triệu. Hai tỉ cộng hai tỉ vượt giới hạn đó, nên kết quả quay vòng. Bốn tỉ trừ hai mũ ba mươi hai ra âm hai trăm chín mươi bốn triệu chín trăm sáu mươi bảy nghìn hai trăm chín mươi sáu. Không có cảnh báo nào. Phép thử là so tổng với tính tay, và đổi sang kiểu tám byte khi tổng có thể lớn.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Cắt lát mảng là một <b>cái nhìn</b>, không phải bản sao: khác với danh sách.</div>' + run_block(P_VIEW)
           + "<p>Sửa <code>b</code> làm <code>a</code> đổi theo, vì chung bộ nhớ. Muốn độc lập: <code>.copy()</code> (dòng $7$ không ảnh hưởng $a$).</p>",
           """Lỗi thứ ba, của người đã đi làm, là cắt lát mảng chỉ là một cái nhìn vào cùng bộ nhớ, không phải bản sao. Khác với danh sách. Sửa một phần tử của lát làm mảng gốc đổi theo. Muốn bản độc lập phải gọi lệnh sao chép, và khi đó sửa bản sao không ảnh hưởng mảng gốc.""", clear=True),
    ], checks=["2000000000 + 2000000000 > 2 ** 31 - 1", "2 ** 31 - 1 == 2147483647", "(2000000000 * 2) - 2 ** 32 == -294967296"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> <code>a = np.array([[1, 2, 3], [4, 5, 6]])</code> (hình dạng <code>(2, 3)</code>).</p>
<ol><li><code>a.sum(axis=0)</code> và <code>a.sum(axis=1)</code> là gì?</li>
<li><code>a + np.array([10, 20, 30])</code> có chạy không? Kết quả?</li></ol>
<p><b>Quyết định:</b> tính tổng $10^7$ số: <b>vòng lặp</b> hay <b>một lệnh trên mảng</b>? Còn $10^9$ số?</p>""",
           """Bây giờ tới phần bạn tự làm. Cho mảng hai hàng ba cột. Câu một, tổng theo trục không và theo trục một là gì. Câu hai, cộng với một hàng ba số có chạy không, kết quả là gì.
           Sau đó là một quyết định, tính tổng mười triệu số, dùng vòng lặp hay một lệnh trên mảng, còn một tỉ số thì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_Q, 0, 5, title="Câu 1 và câu 2")
           + "<p>Trục $0$ gộp hai hàng: $[1+4, 2+5, 3+6] = [5, 7, 9]$. Trục $1$ gộp ba cột: $[6, 15]$. <code>(2, 3) + (3,)</code> khớp từ phải ($3 = 3$): hàng $(10, 20, 30)$ cộng vào cả hai hàng.</p>",
           """Đáp án như sau. Trục không gộp hai hàng, cho năm, bảy, chín. Trục một gộp ba cột, cho sáu và mười lăm. Cộng với hàng ba số chạy được, vì so từ bên phải ba bằng ba, hàng mười, hai mươi, ba mươi được cộng vào cả hai hàng."""),
        st("<div class='box key'><b>Quyết định:</b> mười triệu số: <b>mảng</b>, nhanh hơn " + HT + " lần và nhẹ hơn nhiều lần. "
           "Một tỉ số nguyên tám byte là $8$ GB: nhiều máy không chứa vừa. Khi đó <b>không nạp hết</b>: đọc và tính <b>theo từng khối</b>, cộng dồn kết quả của mỗi khối (bài tình huống ở cuối khoá).</div>",
           """Còn quyết định cuối thì thế này. Mười triệu số thì dùng mảng, nhanh hơn <HT> lần và nhẹ hơn nhiều lần. Một tỉ số nguyên tám byte là tám gi-ga-bai, nhiều máy không chứa vừa. Khi đó không nạp hết, mà đọc và tính theo từng khối, cộng dồn kết quả của mỗi khối. Ta sẽ làm điều này ở bài tình huống cuối khoá.""".replace("tám gi-ga-bai", "tám tỉ byte").replace("<HT>", HT), forward_ref=True, clear=True),
    ], checks=["[1 + 4, 2 + 5, 3 + 6] == [5, 7, 9] and [1 + 2 + 3, 4 + 5 + 6] == [6, 15]", "8 * 10 ** 9 == 8000000000"])
    sc_prac = practice_scene(sc, "Tự làm: trung bình, độ lệch chuẩn và chuẩn hoá cột", pr_steps(
        st, "PYT", "L09",
        """<p><b>Đề</b> (cần môi trường ảo đã cài thư viện): tạo <code>chuan_hoa.py</code>. Dữ liệu <code>so_lieu</code> (5 hàng × 2 cột, <code>dtype=float</code>; xem <code>de.md</code>: số giao dịch/ngày và doanh thu). In <b>năm khối</b>:</p>
<ol><li>trung bình từng cột (làm tròn $2$ chữ số);</li>
<li>độ lệch chuẩn từng cột (làm tròn $2$ chữ số);</li>
<li>mảng đã chuẩn hoá (tròn $3$ chữ số);</li>
<li>kiểm trung bình cột mới $\\approx 0$ (<code>np.allclose(a, b)</code>: hai mảng gần bằng nhau, sai lệch cực nhỏ);</li>
<li>độ lệch chuẩn cột mới (tròn $6$).</li></ol>""",
        """Bây giờ tới phần bạn tự làm, trong môi trường ảo đã cài thư viện. Cho một mảng năm hàng hai cột là số giao dịch mỗi ngày và doanh thu. Tính trung bình và độ lệch chuẩn của từng cột, làm tròn hai chữ số. Chuẩn hoá từng cột rồi in mảng, làm tròn ba chữ số. Kiểm trung bình các cột mới xấp xỉ không và in độ lệch chuẩn của chúng.
        Hãy dừng video và làm.""",
        LAB_OUT, "chuan_hoa.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>tb = so_lieu.mean(axis=0)</code>, <code>do_lech = so_lieu.std(axis=0)</code>, <code>chuan = (so_lieu - tb) / do_lech</code> (lan truyền). Làm tròn khi in: <code>np.round(x, 2)</code>. Lời giải ở <code>labs/PYT/L09/loi_giai.py</code>.</div>""",
        """Nếu kẹt, tính trung bình và độ lệch chuẩn theo trục không, rồi chuẩn hoá bằng phép trừ và chia, nhờ lan truyền. Làm tròn khi in bằng lệnh làm tròn của thư viện.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L09")
    write_lab("PYT", "L09", """# Lab PYT L09 — Trung bình, độ lệch chuẩn, chuẩn hoá cột

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `chuan_hoa.py` (số minh hoạ; khác ví dụ trong bài):

```python
import numpy as np
so_lieu = np.array([[120, 4000], [150, 5200], [90, 3100], [200, 6100], [140, 4600]], dtype=float)
# cột 0: số giao dịch/ngày; cột 1: doanh thu (nghìn đồng)
```

In lần lượt (dùng `np.round`):
1. `Trung binh:` rồi trung bình từng cột, làm tròn 2 chữ số;
2. `Do lech chuan:` rồi độ lệch chuẩn từng cột (`std`, mặc định chia $n$), tròn 2 chữ số;
3. mảng đã chuẩn hoá `(x - trung bình) / độ lệch chuẩn` từng cột, tròn 3 chữ số;
4. `Trung binh cot sau chuan hoa ~ 0:` rồi `np.allclose(chuan.mean(axis=0), 0)`;
5. `Do lech chuan cot sau chuan hoa:` rồi độ lệch chuẩn từng cột mới, tròn 6 chữ số.

Chạy: `python chuan_hoa.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L09 chuan_hoa.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("mảng: cùng một kiểu, nằm liền nhau; hình dạng (hàng, cột)", "phép tính chạy theo từng phần tử, không cần vòng lặp", "trục = hướng bị gộp; kết quả là chiều còn lại",
                 "lan truyền: so kích thước từ bên phải", "mặt nạ đúng/sai làm chỉ số", "nhanh " + HT + " lần, nhưng phải nằm trọn trong bộ nhớ"),
           """Tổng kết chuỗi logic. Mảng cùng một kiểu, nằm liền nhau, có hình dạng hàng cột. Phép tính chạy theo từng phần tử, không cần vòng lặp. Trục là hướng bị gộp, kết quả là chiều còn lại. Lan truyền so kích thước từ bên phải. Mặt nạ đúng sai làm chỉ số.
           Và mảng nhanh <HT> lần, nhưng phải nằm trọn trong bộ nhớ.""".replace("<HT>", HT)),
        st("""<div class='box key'><b>Tư duy:</b> nghĩ <b>cả mảng</b> thay vì từng phần tử; trước mỗi phép tính, hỏi “hình dạng hai bên là gì?”; và hỏi “cả mảng có nằm vừa bộ nhớ không?”.</div>
<p>Bài sau: thư viện bảng dữ liệu, mảng có nhãn cột và nhãn hàng, để đọc, lọc, nhóm và ghép bảng giao dịch.</p>""",
           """Điều cần mang theo, hãy nghĩ cả mảng thay vì từng phần tử. Trước mỗi phép tính hỏi hình dạng hai bên là gì, và hỏi cả mảng có nằm vừa bộ nhớ không.
           Bài sau, ta học thư viện bảng dữ liệu, mảng có nhãn cột và nhãn hàng, để đọc, lọc, nhóm và ghép bảng giao dịch.""", forward_ref=True),
    ])
    return lesson("L09", "mang_so_tinh_theo_mang", "Bài 9 — Thư viện mảng: tính trên cả mảng, không vòng lặp",
                  "curriculum/pyt.yaml L09; audit/pyt/verify_pyt.py L09 (chạy thật trên Python 3.11, labs/.venv-pyt: numpy 2.4.6 theo labs/requirements-py.txt; thời gian và bộ nhớ đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính); "
                  "NumPy documentation: Absolute basics for beginners, Broadcasting, Array creation, Data types (kiểu và tràn số nguyên), Copies and views; Harris et al., Array programming with NumPy, Nature 585, 357–362 (2020)",
                  ["Tạo mảng, đọc hình dạng và kiểu, chọn phần tử bằng chỉ số và cắt",
                   "Tính theo từng phần tử bằng phép tính trên cả mảng",
                   "Tính tổng và trung bình theo trục và nêu hình dạng kết quả",
                   "Giải thích lan truyền và vì sao hình dạng không khớp gây lỗi",
                   "Chọn phần tử bằng mặt nạ đúng sai",
                   "Tính độ lệch chuẩn từ định nghĩa và chuẩn hoá cột",
                   "Nêu tốc độ và bộ nhớ của mảng so với vòng lặp ở ba quy mô",
                   "Chỉ ra ba lỗi hay gặp: hình dạng không khớp, tràn số nguyên nhỏ, nhầm cắt lát với bản sao",
                   "Viết chương trình tính trung bình, độ lệch chuẩn và chuẩn hoá cột"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "formula"), (5, "example"), (6, "formula"), (7, "scale"), (8, "pitfalls"), (9, "practice")])
