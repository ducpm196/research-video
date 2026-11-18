from lib import *
from labkit import write_lab, practice_steps, practice_scene

V = "venv"



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


def intro(steps, i, ids):
    steps[i]["introduces"] = ids
    return steps


GD = ("ma,ngay,loai,tai_khoan,so_tien\n1,2026-03-01,chuyen,A01,500000\n2,2026-03-01,nap,A02,2000000\n3,2026-03-02,rut,A01,300000\n"
      "4,2026-03-02,chuyen,A03,150000\n5,2026-03-03,nap,A01,1000000\n6,2026-03-03,rut,A03,\n7,2026-03-04,chuyen,A02,800000\n")
TK = "tai_khoan,ten\nA01,Lan\nA02,Minh\nA03,Hoa\n"
F = {"gd.csv": GD, "tk.csv": TK}

P_DOC = py("doc_bang", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd.shape)
print(gd.dtypes)""", '(7, 5)\nma             int64\nngay             str\nloai             str\ntai_khoan        str\nso_tien      float64\ndtype: object', files=F, env=V)
P_HEAD = py("dau_bang", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd.head(3))""", '   ma        ngay    loai tai_khoan    so_tien\n0   1  2026-03-01  chuyen       A01   500000.0\n1   2  2026-03-01     nap       A02  2000000.0\n2   3  2026-03-02     rut       A01   300000.0', files=F, env=V)
P_LOC = py("loc_chon", """import pandas as pd
gd = pd.read_csv("gd.csv")
lon = gd[gd["so_tien"] >= 800000]
print(lon[["ma", "loai", "so_tien"]])
print(gd.loc[gd["loai"] == "nap", "so_tien"].sum())""", '   ma    loai    so_tien\n1   2     nap  2000000.0\n4   5     nap  1000000.0\n6   7  chuyen   800000.0\n3000000.0', files=F, env=V)
P_NHOM1 = py("nhom_loai", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd.groupby("loai")["so_tien"].agg(["count", "sum"]))""", '        count        sum\nloai\nchuyen      3  1450000.0\nnap         2  3000000.0\nrut         1   300000.0', files=F, env=V)
P_NHOM2 = py("nhom_tai_khoan", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd.groupby("tai_khoan")["so_tien"].sum())""", 'tai_khoan\nA01    1800000.0\nA02    2800000.0\nA03     150000.0\nName: so_tien, dtype: float64', files=F, env=V)
P_THIEU1 = py("thieu_tong", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd["so_tien"].isna().sum())
print(gd["so_tien"].sum())
print(gd["so_tien"].count(), gd["so_tien"].mean())""", '1\n4750000.0\n6 791666.6666666666', files=F, env=V)
P_THIEU2 = py("thieu_xu_ly", """import pandas as pd
gd = pd.read_csv("gd.csv")
sach = gd.dropna(subset=["so_tien"])
print(len(sach))
print(gd["so_tien"].fillna(0).mean())""", '6\n678571.4285714285', files=F, env=V)
P_NGAY1 = py("ngay_kieu", """import pandas as pd
gd = pd.read_csv("gd.csv", parse_dates=["ngay"])
print(gd["ngay"].dtype)""", 'datetime64[us]', files=F, env=V)
P_NGAY2 = py("ngay_nhom", """import pandas as pd
gd = pd.read_csv("gd.csv", parse_dates=["ngay"])
print(gd.groupby(gd["ngay"].dt.day)["so_tien"].sum())
print((gd["ngay"].max() - gd["ngay"].min()).days)""", 'ngay\n1    2500000.0\n2     450000.0\n3    1000000.0\n4     800000.0\nName: so_tien, dtype: float64\n3', files=F, env=V)
P_GHEP = py("ghep", """import pandas as pd
gd = pd.read_csv("gd.csv")
tk = pd.read_csv("tk.csv")
g = gd.merge(tk, on="tai_khoan", how="left")
print(g[["ma", "ten", "so_tien"]].head(4))""", '   ma   ten    so_tien\n0   1   Lan   500000.0\n1   2  Minh  2000000.0\n2   3   Lan   300000.0\n3   4   Hoa   150000.0', files=F, env=V)
P_GHEP2 = py("ghep_nhom", """import pandas as pd
gd = pd.read_csv("gd.csv")
tk = pd.read_csv("tk.csv")
g = gd.merge(tk, on="tai_khoan", how="left")
print(g.groupby("ten")["so_tien"].sum())""", 'ten\nHoa      150000.0\nLan     1800000.0\nMinh    2800000.0\nName: so_tien, dtype: float64', files=F, env=V)
P_KIEM = py("kiem_thuan", """import csv

tong = {}
with open("gd.csv", encoding="utf-8", newline="") as f:
    for h in csv.DictReader(f):
        if h["so_tien"]:
            tong[h["loai"]] = tong.get(h["loai"], 0) + int(h["so_tien"])
print(tong)""", "{'chuyen': 1450000, 'nap': 3000000, 'rut': 300000}", files=F)
P_VA = py("va_hay_and", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd[(gd["so_tien"] > 100000) and (gd["loai"] == "nap")])""", "", files=F, env=V, expect="error:ValueError", err="ValueError: The truth value of a Series is ambiguous…")
P_VA2 = py("va_dung", """import pandas as pd
gd = pd.read_csv("gd.csv")
print(gd[(gd["so_tien"] > 100000) & (gd["loai"] == "nap")][["ma", "so_tien"]])""", '   ma    so_tien\n1   2  2000000.0\n4   5  1000000.0', files=F, env=V)
P_NAN = py("nan_khong_bang", """import pandas as pd
gd = pd.read_csv("gd.csv")
print((gd["so_tien"] == float("nan")).sum(), gd["so_tien"].isna().sum())""", '0 1', files=F, env=V)
measure("l10_mem2", """import json, time
import numpy as np
import pandas as pd
res = {}
rng = np.random.default_rng(42)
for k, n in (("1e4", 10 ** 4), ("1e6", 10 ** 6)):
    df = pd.DataFrame({"ma": np.arange(n), "loai": rng.choice(["chuyen", "nap", "rut"], n),
                       "tai_khoan": ["A%04d" % (i % 1000) for i in range(n)], "so_tien": rng.integers(10000, 5000000, n)})
    res["m_obj_" + k] = int(df.memory_usage(deep=True).sum())
    df2 = df.astype({"loai": "category", "tai_khoan": "category"})
    res["m_cat_" + k] = int(df2.memory_usage(deep=True).sum())
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        g = df.groupby("loai")["so_tien"].sum()
        best = min(best, time.perf_counter() - t0)
    res["t_groupby_" + k] = best
    ls, ts = df["loai"].tolist(), df["so_tien"].tolist()
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        d = {}
        for a, b in zip(ls, ts):
            d[a] = d.get(a, 0) + b
        best = min(best, time.perf_counter() - t0)
    res["t_py_" + k] = best
    assert all(int(g[x]) == d[x] for x in d)
print(json.dumps(res))""", env=V)

LAB_SOL = '''from pathlib import Path
import pandas as pd

Path("gd.csv").write_text("ma,ngay,loai,kenh,so_tien\\n1,2026-04-01,rut,atm,500000\\n2,2026-04-01,chuyen,app,1200000\\n3,2026-04-02,nap,quay,5000000\\n4,2026-04-02,chuyen,app,250000\\n5,2026-04-03,rut,atm,700000\\n6,2026-04-03,thanh_toan,pos,\\n7,2026-04-04,chuyen,web,90000\\n8,2026-04-04,nap,app,3000000\\n", encoding="utf-8")
gd = pd.read_csv("gd.csv", parse_dates=["ngay"])
print("Thieu so_tien:", gd["so_tien"].isna().sum())
sach = gd.dropna(subset=["so_tien"])
theo_loai = sach.groupby("loai")["so_tien"].agg(["count", "sum"])
print(theo_loai)
theo_ngay = sach.groupby(sach["ngay"].dt.day)["so_tien"].sum()
print(theo_ngay)
print("Ngay nhieu nhat:", theo_ngay.idxmax(), int(theo_ngay.max()))'''
P_LAB = py("lab_l10", LAB_SOL, 'Thieu so_tien: 1\n        count        sum\nloai\nchuyen      3  1540000.0\nnap         2  8000000.0\nrut         2  1200000.0\nngay\n1    1700000.0\n2    5250000.0\n3     700000.0\n4    3090000.0\nName: so_tien, dtype: float64\nNgay nhieu nhat: 2 5250000', env=V)
LAB_OUT = P_LAB["out"]


def shown_sec(txt):
    """Giây ứng với chữ t_show đã hiện trên màn hình ('≈ 2 s' -> 2)."""
    v, u = txt[2:].split()
    return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1, "phút": 60, "giờ": 3600, "ngày": 86400}[u]


def x_k(x, k):
    """Ngoại suy từ số ĐÃ LÀM TRÒN hiện trên màn hình (bảng khớp phép nhân: 2 s x 100 = 3 phút, không phải 4 phút)."""
    return t_show(shown_sec(t_show(x)[0]) * k)


def build():
    mo4, mo6 = M("l10_mem2", "m_obj_1e4"), M("l10_mem2", "m_obj_1e6")
    mc4, mc6 = M("l10_mem2", "m_cat_1e4"), M("l10_mem2", "m_cat_1e6")
    tg4, tg6 = M("l10_mem2", "t_groupby_1e4"), M("l10_mem2", "t_groupby_1e6")
    tp4, tp6 = M("l10_mem2", "t_py_1e4"), M("l10_mem2", "t_py_1e6")
    bo4, bo6, bo8 = b_show(mo4), b_show(mo6), b_show(mo6 * 100)
    bc4, bc6, bc8 = b_show(mc4), b_show(mc6), b_show(mc6 * 100)
    sg4, sg6, sp4, sp6 = t_show(tg4), t_show(tg6), t_show(tp4), t_show(tp6)
    per = sig(mo6 / 1e6, 2)

    def rat(x):
        return str(sig(x, 2)).replace(".", ",")

    def sec_of(txt):  # giây ứng với chữ t_show đã hiện trên màn hình
        v, u = txt[2:].split()
        return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1}[u]

    sc_hook = sc("hook", "hook", "Bảng một triệu dòng: nhóm một lệnh, bộ nhớ nhân theo số dòng", [
        st(table(["bảng giao dịch bốn cột, cột chữ kiểu thường", "bộ nhớ (đo, số minh hoạ)", "nhóm theo loại: vòng lặp Python trên danh sách", "nhóm theo loại: một lệnh trên bảng"],
                 [["10 000 dòng", bo4[0], sp4[0], sg4[0]], ["1 000 000 dòng", bo6[0], sp6[0], sg6[0]], ["100 000 000 dòng (ngoại suy)", bo8[0], x_k(tp6, 100)[0], x_k(tg6, 100)[0]]])
           + "<p class='note'>Bốn cột: <code>ma</code>, <code>loai</code>, <code>tai_khoan</code>, <code>so_tien</code> (chưa tính cột ngày). Vòng lặp duyệt các danh sách đã có sẵn trong bộ nhớ. <b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo (ước lượng, chưa đo).</p>",
           f"""Chào bạn, một bảng giao dịch có một triệu dòng, bốn cột là mã, loại, tài khoản và số tiền. Trên máy kiểm nó chiếm {bo6[1]} bộ nhớ, tức cỡ {vi_num(per)} byte mỗi dòng. Nhóm theo loại giao dịch bằng vòng lặp thuần trên danh sách mất {sp6[1]}, còn bằng một lệnh trên bảng mất {sg6[1]}.
           Ngoại suy, tức nhân theo tỉ lệ từ số đã đo, một trăm triệu dòng: bảng chiếm {bo8[1]}, nhiều hơn bộ nhớ của nhiều máy cá nhân. Số đo trên máy kiểm, số minh hoạ. Hôm nay ta học công cụ này và học nhìn ra giới hạn của nó."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Đọc một tệp CSV thành <b>bảng</b>, <b>chọn</b> và <b>nhóm</b> các dòng ra sao?</li>
<li><b>Ghép</b> hai bảng, và xử lý <b>giá trị thiếu</b> và <b>ngày</b> thế nào cho đúng?</li>
<li>Vì sao bộ nhớ tăng theo số dòng, và có cách nào giảm?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, đọc một tệp bảng thành bảng trong chương trình, chọn và nhóm các dòng ra sao. Hai, ghép hai bảng, và xử lý giá trị thiếu và ngày thế nào cho đúng. Ba, vì sao bộ nhớ tăng theo số dòng, và có cách nào giảm."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: mảng và trục, mặt nạ, đọc CSV, nhóm bằng từ điển", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① mảng, trục, mặt nạ", "<code>a.sum(axis=0)</code> gộp theo cột; <code>a[a &gt; 1000]</code> chọn bằng mặt nạ đúng/sai"],
                  ["② đọc tệp CSV", "<code>csv.DictReader</code>: mỗi dòng một từ điển, mọi giá trị là <b>chuỗi</b>"],
                  ["③ nhóm bằng từ điển", "<code>d[k] = d.get(k, 0) + tien</code> cộng dồn theo khoá"]]),
           """Ta ôn lại ba điều. Mảng cho phép tính theo trục và chọn bằng mặt nạ đúng sai. Bộ đọc bảng của thư viện chuẩn cho mỗi dòng một từ điển, với mọi giá trị là chuỗi. Và từ điển cộng dồn theo khoá để nhóm. Thư viện bảng dữ liệu gộp cả ba ý đó lại, và thêm nhãn cho hàng và cột.""",
           focus=[1, "1.2", "1.3", "1.4", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã bảng, cột, mặt nạ, nhóm, ghép và giá trị thiếu", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>pd.read_csv(\"gd.csv\")</code>", "đọc CSV thành bảng", "<code>pd</code> là tên ngắn của thư viện; kết quả là <b>bảng</b> (<code>DataFrame</code>): hàng có <b>số thứ tự</b>, cột có <b>tên</b>"],
                  ["<code>gd.shape</code>, <code>gd.dtypes</code>, <code>gd.head(3)</code>", "hình dạng, kiểu từng cột, 3 dòng đầu", "<code>(7, 5)</code> = 7 hàng, 5 cột; mỗi cột <b>một kiểu</b>"],
                  ["<code>gd[\"so_tien\"]</code>, <code>gd[[\"ma\", \"loai\"]]</code>", "lấy một cột, nhiều cột", "một cột là <b>chuỗi giá trị có nhãn</b> (<code>Series</code>); nhiều cột là bảng con"]]),
           """Bảng đầu là bảng dữ liệu. Lệnh đọc biến tệp thành bảng, hàng có số thứ tự, cột có tên. Ba lệnh xem nhanh cho hình dạng, kiểu từng cột và vài dòng đầu. Mỗi cột có đúng một kiểu. Lấy một cột cho một chuỗi giá trị có nhãn, lấy nhiều cột cho một bảng con."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>gd[gd[\"so_tien\"] &gt;= 800000]</code>", "chọn dòng bằng mặt nạ", "mặt nạ đúng/sai theo từng dòng; nhiều điều kiện nối bằng <code>&amp;</code> (và), <code>|</code> (hoặc), mỗi điều kiện đặt trong <b>ngoặc tròn</b>"],
                  ["<code>gd.groupby(\"loai\")[\"so_tien\"].sum()</code>", "nhóm rồi tính", "tách các dòng thành nhóm theo <code>loai</code>, tính tổng <code>so_tien</code> mỗi nhóm; <code>.agg([\"count\", \"sum\"])</code> tính nhiều thứ"],
                  ["<code>gd.merge(tk, on=\"tai_khoan\", how=\"left\")</code>", "ghép hai bảng", "nối theo cột chung; <code>left</code> giữ <b>mọi dòng</b> của bảng bên trái"]]),
           """Bảng thứ hai là chọn, nhóm, ghép. Chọn dòng bằng mặt nạ, và nhiều điều kiện nối bằng dấu và hay dấu gạch đứng, mỗi điều kiện đặt trong ngoặc tròn. Nhóm là tách các dòng theo một cột rồi tính trên mỗi nhóm. Ghép nối hai bảng theo cột chung, và kiểu trái giữ mọi dòng của bảng bên trái.""", clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>s.isna()</code>, <code>s.dropna()</code>, <code>s.fillna(0)</code>", "hỏi thiếu, bỏ dòng thiếu, điền", "giá trị thiếu hiện là <code>NaN</code> (không phải số); <code>sum</code>, <code>mean</code> <b>bỏ qua</b> nó"],
                  ["<code>parse_dates=[\"ngay\"]</code>, <code>s.dt.day</code>", "đọc cột ngày, lấy ngày trong tháng", "không khai thì cột ngày chỉ là chữ"],
                  ["<code>astype(\"category\")</code>", "kiểu danh mục", "lưu mỗi giá trị chữ lặp lại <b>một lần</b>, các dòng chỉ giữ mã số: tiết kiệm bộ nhớ"]]),
           """Bảng cuối là giá trị thiếu, ngày và kiểu danh mục. Giá trị thiếu hiện là một ký hiệu không phải số, và các phép tổng, trung bình bỏ qua nó. Khai cột ngày khi đọc thì mới có kiểu ngày, không thì chỉ là chữ. Kiểu danh mục lưu mỗi giá trị chữ lặp lại một lần, các dòng chỉ giữ mã số, nên tiết kiệm bộ nhớ.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: bảng là mảng có nhãn; nhóm là tách – tính – gộp", [
        st(svg(1500, 430,
               box(300, 40, 130, 56, ["ma"], C_GRAY, 22, True), box(440, 40, 150, 56, ["loai"], C_GRAY, 22, True), box(600, 40, 190, 56, ["tai_khoan"], C_GRAY, 22, True), box(800, 40, 200, 56, ["so_tien"], C_GRAY, 22, True),
               txt(150, 75, "tên cột →", 24, "middle", "#6b7280", True),
               *[txt(255, 135 + i * 56, str(i), 24, "middle", "#6b7280") for i in range(3)],
               *[box(300, 105 + i * 56, 130, 50, [str(i + 1)], C_BLUE, 22) for i in range(3)],
               *[box(440, 105 + i * 56, 150, 50, [v], C_BLUE, 22) for i, v in enumerate(["chuyen", "nap", "rut"])],
               *[box(600, 105 + i * 56, 190, 50, [v], C_BLUE, 22) for i, v in enumerate(["A01", "A02", "A01"])],
               *[box(800, 105 + i * 56, 200, 50, [v], C_AMBER, 22, True) for i, v in enumerate(["500000.0", "2000000.0", "300000.0"])],
               txt(140, 135, "số thứ tự", 22, "middle", "#6b7280", True), txt(140, 165, "hàng ↓", 22, "middle", "#6b7280"),
               txt(1130, 100, "mỗi cột: MỘT kiểu", 26, "middle", "#1f2937", True),
               txt(1130, 145, "ma: số nguyên", 24, "middle", "#2a78d6"), txt(1130, 180, "loai, tai_khoan: chữ", 24, "middle", "#2a78d6"), txt(1130, 215, "so_tien: số thực", 24, "middle", "#d97706"),
               txt(750, 335, "bảng = nhiều mảng cùng độ dài ghép lại, thêm nhãn cho hàng và cột", 28, "middle", "#1f2937", True),
               txt(750, 380, "nên mọi điều ở bài trước (mặt nạ, trục, lan truyền) vẫn đúng", 26, "middle", "#16a34a")),
           """Hình này cho thấy bảng là gì. Bảng là nhiều mảng cùng độ dài ghép lại, thêm nhãn cho hàng và cột. Mỗi cột có đúng một kiểu, mã là số nguyên, loại và tài khoản là chữ, số tiền là số thực. Vì bảng là mảng có nhãn, mọi điều ở bài trước, mặt nạ, trục, lan truyền, vẫn đúng."""),
        st(svg(1500, 430,
               txt(250, 35, "bảng gốc (6 dòng có số tiền)", 26, "middle", "#1f2937", True),
               *[box(40, 60 + i * 52, 400, 46, [t], c, 22) for i, (t, c) in enumerate([("chuyen  500 000", C_GREEN), ("nap  2 000 000", C_BLUE), ("rut  300 000", C_AMBER), ("chuyen  150 000", C_GREEN), ("nap  1 000 000", C_BLUE), ("chuyen  800 000", C_GREEN)])],
               arrow(450, 220, 560, 160, "#475569"), arrow(450, 220, 560, 230, "#475569"), arrow(450, 220, 560, 300, "#475569"),
               txt(740, 35, "1. TÁCH theo loai", 26, "middle", "#1f2937", True),
               box(570, 60, 340, 110, ["chuyen", "500 000, 150 000, 800 000"], C_GREEN, 22, True),
               box(570, 185, 340, 90, ["nap", "2 000 000, 1 000 000"], C_BLUE, 22, True),
               box(570, 290, 340, 90, ["rut", "300 000"], C_AMBER, 22, True),
               arrow(915, 115, 1010, 115, "#475569"), arrow(915, 230, 1010, 230, "#475569"), arrow(915, 335, 1010, 335, "#475569"),
               txt(1190, 35, "2. TÍNH mỗi nhóm → 3. GỘP", 26, "middle", "#1f2937", True),
               box(1015, 85, 340, 60, ["chuyen: 1 450 000"], C_GREEN, 24, True), box(1015, 200, 340, 60, ["nap: 3 000 000"], C_BLUE, 24, True), box(1015, 305, 340, 60, ["rut: 300 000"], C_AMBER, 24, True),
               txt(750, 415, "tổng ba nhóm = tổng bảng gốc: 1 450 000 + 3 000 000 + 300 000 = 4 750 000", 24, "middle", "#16a34a", True)),
           """Hình thứ hai là nhóm, gồm ba việc. Một, tách các dòng thành nhóm theo loại. Hai, tính trên mỗi nhóm, ở đây là tổng. Ba, gộp các kết quả thành một bảng mới. Điều kiểm luôn đúng, tổng các nhóm bằng tổng của bảng gốc, một triệu bốn trăm năm mươi nghìn cộng ba triệu cộng ba trăm nghìn bằng bốn triệu bảy trăm năm mươi nghìn.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đọc, chọn bằng mặt nạ, nhóm, giá trị thiếu", intro(nofill(splitall([
        st(raw_block(GD.strip().split("\n"), title="Tệp gd.csv dùng suốt bài: bảy giao dịch, năm cột")
           + "<p>Ô <code>so_tien</code> của giao dịch $6$ để <b>trống</b>: đó là <b>giá trị thiếu</b>. Tệp <code>gd.csv</code> nằm cùng thư mục với chương trình.</p>",
           """Vì mọi ví dụ sau đều đọc tệp này, ta xem nó trước. Đây là tệp giao dịch dùng suốt bài, bảy giao dịch và năm cột. Giao dịch thứ sáu có ô số tiền để trống, và ta sẽ thấy ô thiếu đó làm đổi kết quả thế nào."""),
        st(run_block(P_DOC, title="Bước 1. Đọc: hình dạng và kiểu từng cột")
           + "<p>Vì CSV chỉ là chữ, thư viện <b>đoán kiểu</b> từng cột: <code>so_tien</code> thành số <b>thực</b> (<code>float64</code>) vì có ô trống. <code>str</code> là kiểu chữ (đo bằng <b>pandas 3.1.1</b>; bản 2.x hiện <code>object</code>).</p>",
           """Bước một, đọc tệp. Bảng có bảy dòng, năm cột. Vì tệp chỉ là chữ, thư viện đoán kiểu từng cột, và kiểu chữ hiện viết tắt là chuỗi. Tên kiểu này là của bản thư viện ghim trong khoá, bản cũ hơn ghi tên khác. Cột số tiền thành số thực, dù các số đều nguyên, vì có một ô trống, tức giá trị thiếu, mà số nguyên không chứa được.""", clear=True),
        st(run_block(P_HEAD, title="Xem nhanh ba dòng đầu"),
           """Vì vậy ba dòng đầu cho ta xem nhanh dữ liệu mà không cần mở cả tệp. Số tiền hiện dưới dạng số thực, có một chữ số không sau dấu phẩy.""", clear=True),
        st("<p><code>gd.loc[điều_kiện, \"cột\"]</code>: trong ngoặc vuông, <b>điều kiện</b> chọn dòng, dấu phẩy, rồi <b>tên cột</b> cần lấy.</p>"
           + run_block(P_LOC, title="Bước 2. Chọn dòng bằng mặt nạ, tính trên một cột")
           + "<p>Vì <code>so_tien &gt;= 800000</code> cho một cột đúng/sai theo từng dòng, đưa nó vào <code>gd[…]</code> giữ các dòng đúng: $3$ dòng. Dòng thứ hai (<code>.loc</code>) chọn các dòng thoả điều kiện rồi lấy đúng cột đó. Tổng tiền loại <code>nap</code>: $2\\,000\\,000 + 1\\,000\\,000 = 3\\,000\\,000$ ✓</p>",
           """Bước hai, chọn bằng mặt nạ. Vì so sánh cột số tiền với tám trăm nghìn cho một cột đúng sai theo từng dòng, đưa nó vào trong ngoặc vuông giữ các dòng đúng, được ba dòng. Dòng lệnh thứ hai dùng cách chọn có nhãn: trong ngoặc vuông ghi điều kiện, dấu phẩy, rồi tên cột, để chọn các dòng thoả điều kiện và lấy đúng cột đó. Vì vậy nó cộng tiền các giao dịch nạp, hai triệu cộng một triệu bằng ba triệu.""", clear=True, introduces=["pyt_loc"]),
        st(run_block(P_NHOM1, title="Bước 3. Nhóm: tách – tính – gộp")
           + "<p>Vì mỗi nhóm cộng riêng: <code>chuyen</code> $500\\,000 + 150\\,000 + 800\\,000 = 1\\,450\\,000$; <code>nap</code> $2\\,000\\,000 + 1\\,000\\,000 = 3\\,000\\,000$; <code>rut</code> chỉ $300\\,000$ (rút thứ hai có ô tiền trống nên không đếm).</p>",
           """Bước ba, nhóm. Nhóm theo loại, đếm và cộng tiền mỗi nhóm. Vì mỗi nhóm cộng riêng, ba giao dịch chuyển cộng được một triệu bốn trăm năm mươi nghìn, hai giao dịch nạp cộng ba triệu. Chỉ một giao dịch rút có tiền cộng ba trăm nghìn, vì giao dịch rút thứ hai có ô tiền trống nên không được đếm.""", clear=True),
        st(run_block(P_NHOM2, title="Nhóm theo tài khoản")
           + "<p><code>A01</code>: $500\\,000 + 300\\,000 + 1\\,000\\,000 = 1\\,800\\,000$; <code>A02</code>: $2\\,000\\,000 + 800\\,000 = 2\\,800\\,000$; <code>A03</code>: $150\\,000$. Kiểm: ba nhóm cộng lại $= 4\\,750\\,000$.</p>",
           """Nhóm theo tài khoản cho tổng theo từng tài khoản. Tài khoản A không một gồm ba giao dịch, năm trăm nghìn, ba trăm nghìn và một triệu, cộng được một triệu tám trăm nghìn. Tài khoản A không hai có hai triệu tám trăm nghìn. Tài khoản A không ba chỉ có một trăm năm mươi nghìn.""", clear=True),
        st(run_block(P_THIEU1, title="Bước 4. Giá trị thiếu: tổng và trung bình bỏ qua nó")
           + "<p><code>isna()</code> cho một cột đúng/sai (<code>True</code> ở ô thiếu); <code>True</code> tính là $1$, <code>False</code> là $0$, nên <code>.sum()</code> đếm số ô thiếu.</p>",
           """Bước bốn, giá trị thiếu. Vì tệp có một ô trống, ta đếm ô thiếu, cộng, và lấy trung bình. Hỏi thiếu cho cột đúng sai, đúng tính là một, nên tổng đếm số ô thiếu. Có một ô thiếu. Tổng là bốn triệu bảy trăm năm mươi nghìn, và trung bình chia cho sáu ô có số.""", clear=True),
        st(run_block(P_THIEU2, title="Bỏ dòng thiếu, hoặc điền không")
           + "<p>Vì <code>sum</code> và <code>mean</code> bỏ qua ô thiếu: tổng $4\\,750\\,000$ của $6$ ô; trung bình chia cho $6$. Điền $0$ vào ô thiếu thì chia cho $7$, trung bình thấp hơn: $\\frac{4\\,750\\,000}{7} \\approx 678\\,571$. <code>gd.dropna(subset=[\"so_tien\"])</code> bỏ các dòng mà cột <code>so_tien</code> thiếu (<code>subset</code> = chỉ xét các cột được nêu).</p>",
           """Lệnh bỏ dòng thiếu, kèm tên cột cần xét, còn sáu dòng. Nếu điền không vào ô thiếu thì phải chia cho bảy, và trung bình thấp hơn. Vì thế quyết định bỏ, điền hay giữ ô thiếu đổi kết quả, và phải được nêu rõ.""", clear=True),
    ], k=3, only=[3])), 3, ["pyt_loc"]), checks=["800000 + 1000000 + 2000000 > 0 and 2000000 + 1000000 == 3000000", "500000 + 150000 + 800000 == 1450000 and 1450000 + 3000000 + 300000 == 4750000",
               "500000 + 300000 + 1000000 == 1800000 and 2000000 + 800000 == 2800000",
               "round(4750000 / 6, 4) == 791666.6667 and round(4750000 / 7, 2) == 678571.43"])
    sc_ex = sc("example", "example", "Ví dụ: ngày, ghép bảng tên khách, điều kiện nối bằng &", [
        st(run_block(P_NGAY1, title="Cột ngày: khai khi đọc thì có kiểu ngày giờ")
           + "<p><code>datetime64[us]</code> là kiểu <b>ngày giờ</b> của bảng (<code>us</code> = phần triệu giây, độ chính xác lưu trữ). Đo bằng pandas 3.1.1; pandas 2.x hiện <code>datetime64[ns]</code> (phần tỉ giây): nội dung giống, chỉ tên kiểu khác.</p>",
           """Ví dụ một, ngày. Khai cột ngày khi đọc, cột có kiểu ngày giờ thay vì chữ. Tên kiểu ghi thêm độ chính xác là phần triệu giây.""", introduces=["pyt_datetime64"]),
        st(run_block(P_NGAY2, title="Tổng tiền theo ngày trong tháng")
           + "<p>Hai ngày trừ nhau cho một khoảng thời gian; <code>.days</code> là số ngày của khoảng đó.</p>",
           """Nhóm theo ngày trong tháng cho tổng tiền mỗi ngày, ví dụ ngày một có năm trăm nghìn cộng hai triệu bằng hai triệu rưỡi. Hai ngày trừ nhau cho một khoảng thời gian, và thuộc tính số ngày của nó là ba.""", clear=True),
        st(raw_block(TK.strip().split("\n"), title="Tệp tk.csv: tên khách của từng tài khoản"),
           """Ví dụ hai, ghép bảng. Bảng giao dịch chỉ có mã tài khoản, còn tệp thứ hai cho tên khách của từng mã.""", clear=True),
        st(run_block(P_GHEP, title="Ghép bảng giao dịch với bảng tên khách"),
           """Ghép theo mã tài khoản, giữ mọi dòng của bảng giao dịch. Bốn dòng đầu giờ có tên khách.""", clear=True),
        st(run_block(P_GHEP2, title="Nhóm theo tên khách"),
           """Nhóm theo tên cho tổng một triệu tám trăm nghìn của Lan, hai triệu tám trăm nghìn của Minh, và một trăm năm mươi nghìn của Hoa.""", clear=True),
        st(run_block(P_VA2, title="Nhiều điều kiện: nối bằng & và đặt từng điều kiện trong ngoặc")
           + "<p>Giao dịch <code>nap</code> <b>và</b> trên $100\\,000$: các dòng $2$ và $5$.</p>",
           """Ví dụ ba, nhiều điều kiện. Ta muốn các giao dịch nạp và trên một trăm nghìn. Nối hai điều kiện bằng dấu và, mỗi điều kiện đặt trong ngoặc tròn. Kết quả là hai dòng, mã hai và mã năm.""", clear=True),
    ], checks=["500000 + 2000000 == 2500000", "500000 + 300000 + 1000000 == 1800000 and 2000000 + 800000 == 2800000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cộng bằng thư viện chuẩn", [
        st(run_block(P_KIEM, title="Không dùng thư viện bảng: bộ đọc CSV và từ điển")
           + "<p>Dòng điều kiện <code>if h[\"so_tien\"]:</code> coi chuỗi rỗng <code>\"\"</code> (ô trống) là <b>sai</b>, nên dòng thiếu bị bỏ; <code>csv.DictReader(f)</code> cho mỗi dòng một từ điển, khoá là tên cột; <code>newline=\"\"</code> để bộ đọc tự xử lý xuống dòng trong ô.</p>",
           """Đường kiểm khác, không dùng thư viện bảng. Bộ đọc bảng của thư viện chuẩn cho mỗi dòng một từ điển. Câu điều kiện coi chuỗi rỗng là sai, nên dòng thiếu bị bỏ qua, và từ điển cộng theo loại."""),
        st("<div class='box key'>Hai đường độc lập cùng cho chuyển $1\\,450\\,000$, nạp $3\\,000\\,000$, rút $300\\,000$. Tổng $= 4\\,750\\,000$, trùng bước $4$ ✓</div>",
           """Hai đường cho đúng ba con số, một triệu bốn trăm năm mươi nghìn, ba triệu, ba trăm nghìn, trùng với kết quả nhóm. Tổng bốn triệu bảy trăm năm mươi nghìn nên trùng tổng chung.""", clear=True),
    ], checks=["1450000 + 3000000 + 300000 == 4750000"])
    sc_scale = sc("scale", "concept", "Khi bảng lớn dần: bộ nhớ tăng theo số dòng, kiểu danh mục tiết kiệm", [
        st(table(["số dòng", "cột chữ kiểu thường", "cột chữ kiểu danh mục", "tiết kiệm"],
                 [["×1: 10 000", bo4[0], bc4[0], f"≈ {rat(mo4 / mc4)} lần"], ["×100: 1 000 000", bo6[0], bc6[0], f"≈ {rat(mo6 / mc6)} lần"],
                  ["×10 000 (ngoại suy): 100 000 000", bo8[0], bc8[0], "—"]])
           + "<p class='note'>Hai cột chữ (<code>loai</code>, <code>tai_khoan</code>) đổi sang kiểu danh mục. Hệ số tiết kiệm gần như <b>không đổi theo số dòng</b>: nó phụ thuộc số giá trị khác nhau trong cột (ở đây $3$ loại, $1\\,000$ tài khoản). Bộ nhớ đo bằng lệnh đo bộ nhớ của bảng (kể cả nội dung chuỗi); đo trên máy kiểm, số minh hoạ; ngoại suy = nhân theo tỉ lệ từ số đã đo.</p>",
           f"""Bảng này đo bộ nhớ của một bảng bốn cột. Mười nghìn dòng chiếm {bo4[1]} với cột chữ kiểu thường, và {bc4[1]} khi đổi sang kiểu danh mục. Một triệu dòng chiếm {bo6[1]} và {bc6[1]}. Hệ số tiết kiệm xấp xỉ nhau ở hai quy mô, cỡ {vi_num(sig(mo6 / mc6, 2))} lần, vì nó phụ thuộc số giá trị khác nhau trong cột chứ không phụ thuộc số dòng. Ngoại suy một trăm triệu dòng, kiểu thường cần {bo8[1]}, kiểu danh mục cần {bc8[1]}.
           Số đo trên máy kiểm, số minh hoạ."""),
        st(table(["nhóm theo loại (dữ liệu đã nằm sẵn)", "vòng lặp Python trên danh sách", "một lệnh trên bảng", "nhanh gấp"],
                 [["10 000 dòng", sp4[0], sg4[0], "cùng cỡ; chưa chắc nhanh hơn"], ["1 000 000 dòng", sp6[0], sg6[0], f"≈ {rat(sec_of(sp6[0]) / sec_of(sg6[0]))}"]])
           + "<div class='box key'><b>Đánh đổi:</b> bảng nhanh vì tính theo cột bằng mã đã biên dịch, nhưng <b>mọi dòng nằm trong bộ nhớ</b>. Khi bảng lớn: chọn <b>kiểu hẹp</b> (danh mục cho chữ lặp, số nguyên nhỏ cho số), "
             "<b>chỉ đọc cột cần</b>, hoặc <b>đọc theo khối</b> (mỗi lần chỉ đọc một phần tệp, cỡ vài trăm nghìn dòng) rồi cộng dồn. Với hàng trăm triệu dòng và hơn, người làm nghề chuyển sang cơ sở dữ liệu.</div>",
           f"""Về thời gian, nhóm theo loại ở một triệu dòng mất {sp6[1]} bằng vòng lặp trên danh sách. Một lệnh trên bảng mất {sg6[1]}, nhanh hơn cỡ {vi_num(sig(sec_of(sp6[0]) / sec_of(sg6[0]), 2))} lần. Ở mười nghìn dòng hai cách cùng cỡ thời gian, và có máy lệnh trên bảng còn chậm hơn, vì nó có chi phí cố định. Đánh đổi là bảng nhanh vì tính theo cột bằng mã đã biên dịch, nhưng mọi dòng nằm trong bộ nhớ. Khi bảng lớn, ta chọn kiểu hẹp, chỉ đọc cột cần, hoặc đọc theo khối, nghĩa là mỗi lần chỉ đọc một phần tệp, rồi cộng dồn. Với hàng trăm triệu dòng trở lên, người làm nghề chuyển sang cơ sở dữ liệu.""", clear=True),
    ], checks=["10 ** 6 * 100 == 10 ** 8", "10 ** 4 * 100 == 10 ** 6"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Nối hai điều kiện trên bảng bằng <code>and</code> thay cho <code>&amp;</code>.</div>' + run_block(P_VA)
           + "<p>Đọc dòng cuối: “giá trị đúng/sai của cả một cột là mập mờ”. <code>and</code> đòi <b>một</b> đúng/sai; cột có <b>nhiều</b>. Dùng <code>&amp;</code>, <code>|</code>, và ngoặc.</p>",
           """Lỗi thứ nhất, của người mới, là nối hai điều kiện trên bảng bằng từ và thay cho dấu và. Dòng cuối nói giá trị đúng sai của cả một cột là mập mờ. Từ và đòi một giá trị đúng sai, trong khi cột có nhiều. Phải dùng dấu và, dấu gạch đứng, và đặt mỗi điều kiện trong ngoặc."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Tổng bỏ qua ô thiếu và <b>không báo</b>: số trông hợp lý nhưng thiếu một giao dịch.</div>' + run_slice(P_THIEU1, code=(1, 4), out=(0, 2))
           + "<p>Tổng $4\\,750\\,000$ chỉ của $6$ trong $7$ giao dịch. Phép thử: <b>luôn in <code>isna().sum()</code></b> trước khi tin một tổng, và ghi lại cách xử lý thiếu.</p>",
           """Lỗi thứ hai, của người đã đi làm, là tổng bỏ qua ô thiếu mà không báo. Bốn triệu bảy trăm năm mươi nghìn trông hợp lý, nhưng chỉ là của sáu trong bảy giao dịch. Phép thử là luôn in số ô thiếu trước khi tin một tổng, và ghi lại cách xử lý.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> So giá trị thiếu bằng <code>==</code>.</div>' + run_block(P_NAN)
           + "<p><code>NaN == NaN</code> là <b>sai</b> (nó “không phải số”, không bằng cả chính nó): đếm bằng <code>==</code> ra $0$, đúng phải là <code>isna()</code> $= 1$. <code>float(\"nan\")</code> tự dựng giá trị thiếu <code>NaN</code> bằng tay để thử so sánh.</p>",
           """Lỗi thứ ba, của người đã đi làm, là so giá trị thiếu bằng dấu hai bằng. Ở đây lệnh đổi chữ sang số, với chữ nan, tự dựng một giá trị thiếu. Giá trị thiếu không bằng cả chính nó, nên đếm bằng phép so ra không, trong khi đúng phải là một. Luôn dùng lệnh hỏi thiếu.""", clear=True),
    ], checks=["float('nan') != float('nan')"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Bảng nhỏ <code>kk</code> gồm $4$ dòng (một ô số tiền thiếu).</p>
<table class='t'><tr><th>kenh</th><th>so_tien</th></tr><tr><td>quay</td><td>300</td></tr><tr><td>mang</td><td>200</td></tr><tr><td>quay</td><td>500</td></tr><tr><td>mang</td><td>(thiếu)</td></tr></table>
<ol><li><code>kk.groupby("kenh")["so_tien"].sum()</code> cho mỗi kênh bao nhiêu?</li>
<li><code>kk["so_tien"].mean()</code> bằng bao nhiêu? Điền $0$ vào ô thiếu rồi lấy trung bình thì sao?</li></ol>
<p><b>Quyết định:</b> tệp $10^8$ dòng, $4$ cột: <b>đọc cả một lần</b> hay <b>đọc theo khối</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Bảng nhỏ có bốn dòng, kênh và số tiền, một ô số tiền thiếu. Câu một, tổng theo từng kênh là bao nhiêu. Câu hai, trung bình của cột số tiền bằng bao nhiêu, và nếu điền không vào ô thiếu thì sao.
           Sau đó là một quyết định, tệp một trăm triệu dòng bốn cột, đọc cả một lần hay đọc theo khối, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "<code>quay</code>: $300 + 500 = 800$; <code>mang</code>: $200$ (ô thiếu không được cộng). Tổng hai nhóm $= 1000$"], ["2", "ô thiếu bị bỏ qua: $\\frac{300 + 200 + 500}{3} \\approx 333{,}33$ (chia cho $3$, không phải $4$); điền $0$ thì chia cho $4$ được $250$"]]),
           """Đáp án như sau. Câu một, kênh quầy cộng được tám trăm, kênh mạng chỉ có hai trăm, vì ô thiếu không được cộng. Câu hai, ô thiếu bị bỏ qua nên trung bình chia cho ba, được ba trăm ba mươi ba phẩy ba ba. Nếu điền không thì chia cho bốn, được hai trăm năm mươi."""),
        st("<div class='box key'><b>Quyết định:</b> <b>theo khối</b>. Một trăm triệu dòng bốn cột dù kiểu hẹp cũng cỡ hàng gi-ga-bai đến hàng chục gi-ga-bai trong bộ nhớ. "
           "Đọc từng khối vài trăm nghìn dòng, tính nhóm cho khối đó, <b>cộng dồn</b> vào bảng kết quả: bộ nhớ không đổi. Đây là cách ta làm ở bài tình huống cuối khoá.</div>".replace("gi-ga-bai", "GB"),
           """Quyết định, đọc theo khối. Một trăm triệu dòng bốn cột, dù dùng kiểu hẹp, vẫn cỡ hàng tỉ byte đến hàng chục tỉ byte trong bộ nhớ. Đọc từng khối vài trăm nghìn dòng, tính nhóm cho khối đó, rồi cộng dồn vào bảng kết quả, nên bộ nhớ không đổi. Ta sẽ làm điều này ở bài tình huống cuối khoá.""", clear=True, forward_ref=True),
    ], checks=["300 + 500 == 800", "round((300 + 200 + 500) / 3, 2) == 333.33 and (300 + 200 + 500) / 4 == 250"])
    sc_prac = practice_scene(sc, "Tự làm: thống kê giao dịch theo loại và theo ngày", intro(pr_steps(
        st, "PYT", "L10",
        """<p><b>Đề</b> (cần môi trường ảo đã cài thư viện): tạo <code>thong_ke.py</code>. Dòng đầu <b>ghi sẵn</b> <code>gd.csv</code> (8 giao dịch, cột <code>ma, ngay, loai, kenh, so_tien</code>; chép từ <code>de.md</code>; một ô <code>so_tien</code> trống). Rồi:</p>
<ol><li>đọc với <code>parse_dates=["ngay"]</code>; in <code>Thieu so_tien: …</code>;</li>
<li>bỏ dòng thiếu; in bảng <code>count</code> và <code>sum</code> theo <code>loai</code>;</li>
<li>in tổng theo ngày (<code>.dt.day</code>); in <code>Ngay nhieu nhat: &lt;ngày&gt; &lt;tổng&gt;</code>: <code>idxmax()</code> cho <b>nhãn</b> (ở đây là ngày) của giá trị lớn nhất; tổng in dạng <b>số nguyên</b> (dùng <code>int(…)</code>, vì tổng là số thực).</li></ol>""",
        """Bây giờ tới phần bạn tự làm, trong môi trường ảo đã cài thư viện. Ghi sẵn tệp tám giao dịch từ đề bài, có một ô số tiền trống. Đọc với cột ngày được khai. In số ô thiếu. Bỏ dòng thiếu, rồi in bảng đếm và tổng tiền theo loại. In tổng theo ngày trong tháng, và in ngày có tổng lớn nhất cùng tổng đó, viết thành số nguyên. Hãy dừng video và làm.""",
        LAB_OUT, "thong_ke.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>gd["so_tien"].isna().sum()</code>; <code>sach = gd.dropna(subset=["so_tien"])</code>; <code>sach.groupby("loai")["so_tien"].agg(["count", "sum"])</code>; <code>theo_ngay = sach.groupby(sach["ngay"].dt.day)["so_tien"].sum()</code>; <code>theo_ngay.idxmax()</code>; <code>int(theo_ngay.max())</code>.
Lời giải ở <code>labs/PYT/L10/loi_giai.py</code>.</div>""",
        """Nếu kẹt, đếm ô thiếu bằng lệnh hỏi thiếu, rồi bỏ dòng thiếu bằng lệnh bỏ. Nhóm theo loại với hai phép tính, nhóm theo ngày trong tháng. Tìm nhãn của giá trị lớn nhất, và đổi tổng sang số nguyên.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=360), 0, ["pyt_idxmax"]), "PYT", "L10")
    write_lab("PYT", "L10", """# Lab PYT L10 — Thống kê giao dịch theo loại và theo ngày

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `thong_ke.py`. Dòng đầu chương trình **ghi sẵn** `gd.csv` bằng `Path("gd.csv").write_text(..., encoding="utf-8")` (số minh hoạ; khác ví dụ trong bài):

```
ma,ngay,loai,kenh,so_tien
1,2026-04-01,rut,atm,500000
2,2026-04-01,chuyen,app,1200000
3,2026-04-02,nap,quay,5000000
4,2026-04-02,chuyen,app,250000
5,2026-04-03,rut,atm,700000
6,2026-04-03,thanh_toan,pos,
7,2026-04-04,chuyen,web,90000
8,2026-04-04,nap,app,3000000
```

1. Đọc bằng `pd.read_csv("gd.csv", parse_dates=["ngay"])`. In `Thieu so_tien: <số ô thiếu>`.
2. Bỏ dòng thiếu `so_tien`; in bảng `count` và `sum` của `so_tien` **theo `loai`**.
3. In tổng `so_tien` **theo ngày trong tháng** (`sach["ngay"].dt.day`), rồi `Ngay nhieu nhat: <ngày> <tổng nguyên>`. `idxmax()` cho nhãn (ngày) của giá trị lớn nhất; tổng là số thực nên in bằng `int(...)` (ví dụ `5250000`, không phải `5250000.0`).

Chạy: `python thong_ke.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L10 thong_ke.py` (trên máy chấm của khoá dùng `labs/.venv-pyt`).
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("bảng = mảng có nhãn; mỗi cột một kiểu", "chọn bằng mặt nạ; & | và ngoặc", "nhóm: tách – tính – gộp; tổng nhóm = tổng gốc",
                 "ô thiếu: tổng bỏ qua, phải đếm và nêu cách xử lý", "kiểu danh mục giảm bộ nhớ", "mọi dòng nằm trong bộ nhớ: lớn thì đọc theo khối"),
           """Tổng kết chuỗi logic. Bảng là mảng có nhãn, mỗi cột một kiểu. Chọn bằng mặt nạ, nối điều kiện bằng dấu và và ngoặc. Nhóm là tách, tính, gộp, và tổng các nhóm bằng tổng gốc. Ô thiếu bị tổng bỏ qua, nên phải đếm và nêu cách xử lý.
           Kiểu danh mục giảm bộ nhớ. Và mọi dòng nằm trong bộ nhớ, nên khi bảng lớn thì đọc theo khối."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi tin một con số từ bảng, hỏi ba câu: <b>có ô thiếu không?</b>, <b>tổng các nhóm có bằng tổng gốc không?</b>, và <b>bảng này nằm vừa bộ nhớ không?</b></div>
<p>Bài sau: vẽ biểu đồ từ dữ liệu, và đọc biểu đồ cho đúng, kể cả khi biểu đồ cố ý đánh lừa.</p>""",
           """Điều cần mang theo, trước khi tin một con số từ bảng hãy hỏi ba câu. Có ô thiếu không. Tổng các nhóm có bằng tổng gốc không. Và bảng này nằm vừa bộ nhớ không.
           Bài sau, ta học vẽ biểu đồ từ dữ liệu, và đọc biểu đồ cho đúng, kể cả khi biểu đồ cố ý đánh lừa.""", forward_ref=True),
    ])
    return lesson("L10", "bang_du_lieu", "Bài 10 — Thư viện bảng dữ liệu: đọc, lọc, nhóm, ghép",
                  "curriculum/pyt.yaml L10; audit/pyt/verify_pyt.py L10 (chạy thật trên Python 3.11, labs/.venv-pyt: pandas 3.1.1 theo labs/requirements-py.txt; bộ nhớ và thời gian đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính); "
                  "pandas documentation: 10 minutes to pandas, Working with missing data, Group by: split-apply-combine, Merge, join, concatenate, Categorical data, Scaling to large datasets; dữ liệu giao dịch là số minh hoạ",
                  ["Đọc CSV thành bảng, xem hình dạng và kiểu từng cột",
                   "Chọn dòng bằng mặt nạ và nối điều kiện bằng & và |",
                   "Nhóm theo cột rồi tính, và kiểm tổng các nhóm bằng tổng gốc",
                   "Xử lý giá trị thiếu và nêu vì sao cách xử lý đổi kết quả",
                   "Đọc cột ngày và ghép hai bảng theo cột chung",
                   "Nêu bộ nhớ của bảng thay đổi thế nào theo số dòng và kiểu cột",
                   "Chỉ ra ba lỗi hay gặp: and thay cho &, tổng bỏ qua ô thiếu, so giá trị thiếu bằng ==",
                   "Viết chương trình thống kê giao dịch theo loại và theo ngày"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy", "pyt_bien_dich"],
                  covers=[(1, "formula"), (2, "formula"), (3, "formula"), (4, "formula"), (5, "example"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
