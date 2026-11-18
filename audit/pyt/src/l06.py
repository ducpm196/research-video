from lib import *
from labkit import write_lab, practice_steps, practice_scene

CLS = "class TaiKhoan:\n    def __init__(self, ma, so_du=0):\n        self.ma = ma\n        self.so_du = so_du\n    def nap(self, tien):\n        self.so_du = self.so_du + tien\n"
R_SELF = repl("Self", [
    (CLS, ""), ('a = TaiKhoan("A01", 100)', ""), ("a.nap(50)", ""), ("a.so_du", "150"), ("TaiKhoan.nap(a, 50)", ""), ("a.so_du", "200"),
    ("a.__dict__", "{'ma': 'A01', 'so_du': 200}"), ("isinstance(a, TaiKhoan)", "True"),
])
R_ALIAS = repl("BiDanh", [(CLS, ""), ('a = TaiKhoan("A01", 100)', ""), ("b = a", ""), ("b.nap(50)", ""), ("a.so_du", "150")])
R_KIEM = repl("Kiem", [("1000000 + 500000 - 300000", "1200000"), ("1500000 - 300000", "1200000")])
R_QUIZ = repl("Quiz", [(CLS, ""), ('a = TaiKhoan("A01", 100)', ""), ("b = a", ""), ("b.nap(50)", ""), ("a.so_du", "150")])

P_TK = py("tai_khoan", '''class TaiKhoan:
    def __init__(self, ma, so_du=0):
        self.ma = ma
        self.so_du = so_du
    def nap(self, tien):
        self.so_du = self.so_du + tien
    def rut(self, tien):
        if tien > self.so_du:
            return False
        self.so_du = self.so_du - tien
        return True
    def __repr__(self):
        return f"TaiKhoan({self.ma}, {self.so_du})"

a = TaiKhoan("A01", 1000000)
a.nap(500000)
print(a.rut(2000000), a)
print(a.rut(300000), a)''', "False TaiKhoan(A01, 1500000)\nTrue TaiKhoan(A01, 1200000)")
P_DC = py("lop_du_lieu", '''from dataclasses import dataclass

@dataclass
class GiaoDich:
    ma: str
    loai: str
    tien: int

g1 = GiaoDich("G1", "nap", 500000)
g2 = GiaoDich("G1", "nap", 500000)
print(g1)
print(g1 == g2, g1 is g2)''', "GiaoDich(ma='G1', loai='nap', tien=500000)\nTrue False")
P_KT = py("ke_thua", '''class TaiKhoan:
    def __init__(self, ma, so_du=0):
        self.ma = ma
        self.so_du = so_du

    def nap(self, tien):
        self.so_du = self.so_du + tien

class TietKiem(TaiKhoan):
    def __init__(self, ma, so_du, lai_nghin):
        super().__init__(ma, so_du)
        self.lai_nghin = lai_nghin

    def cong_lai(self):
        self.nap(self.so_du * self.lai_nghin // 1000)

class KhachHang:
    def __init__(self, ten, tai_khoan):
        self.ten = ten
        self.tai_khoan = tai_khoan

tk = TietKiem("S01", 2000000, 5)
tk.cong_lai()
kh = KhachHang("Lan", tk)
print(kh.ten, kh.tai_khoan.so_du)
print(isinstance(tk, TaiKhoan))''', "Lan 2010000\nTrue")
P_SELF = py("quen_self", '''class TaiKhoan:
    def nap(tien):
        pass

a = TaiKhoan()
a.nap(5)''', "", expect="error:TypeError", err="TypeError: TaiKhoan.nap() takes 1 positional argument but 2 were given")
P_CHUNG = py("thuoc_tinh_lop", '''class TaiKhoan:
    lich_su = []

    def __init__(self, ma):
        self.ma = ma

    def nap(self, tien):
        self.lich_su.append(tien)

a = TaiKhoan("A01")
b = TaiKhoan("A02")
a.nap(100000)
print(b.lich_su)''', "[100000]")
P_CHUNG2 = py("thuoc_tinh_dung", '''class TaiKhoan:
    def __init__(self, ma):
        self.ma = ma
        self.lich_su = []

    def nap(self, tien):
        self.lich_su.append(tien)

a = TaiKhoan("A01")
b = TaiKhoan("A02")
a.nap(100000)
print(a.lich_su, b.lich_su)''', "[100000] []")
P_EQ = py("so_sanh", '''class TaiKhoan:
    def __init__(self, ma):
        self.ma = ma

a = TaiKhoan("A01")
b = TaiKhoan("A01")
print(a == b)
print(a is a, a is b)''', "False\nTrue False")
P_SIZE = py("kich_thuoc", '''import sys

print(sys.getsizeof(0))
print(sys.getsizeof([]))
print(sys.getsizeof(list(range(1000))))''', "28\n56\n8056")
# Chương trình minh hoạ đo bộ nhớ bằng tracemalloc (hiện nguyên văn trên màn hình): số MB in ra là số đo thật (máy khác, bản khác cho số khác).
DEMO_MEM = '''import tracemalloc

class A:
    def __init__(self, ma, so_du):
        self.ma = ma
        self.so_du = so_du

tracemalloc.start()
xs = [A("A" + str(i), i) for i in range(100000)]
dang_dung, dinh = tracemalloc.get_traced_memory()
print(round(dang_dung / 10**6, 1), "MB")'''
measure("l06_demo", DEMO_MEM + "\nimport json\nprint(json.dumps({'m_demo': dang_dung}))")
measure("l06_mem", '''import json, tracemalloc
res = {}
class A:
    def __init__(self, ma, so_du, han_muc):
        self.ma = ma
        self.so_du = so_du
        self.han_muc = han_muc
class B:
    __slots__ = ("ma", "so_du", "han_muc")
    def __init__(self, ma, so_du, han_muc):
        self.ma = ma
        self.so_du = so_du
        self.han_muc = han_muc
for k, n in (("1e5", 100000), ("1e6", 1000000)):
    for name, make in (("cls", lambda i: A("A%07d" % i, i, 0)), ("slots", lambda i: B("A%07d" % i, i, 0)), ("tuple", lambda i: ("A%07d" % i, i, 0))):
        tracemalloc.start()
        xs = [make(i) for i in range(n)]
        res["m_%s_%s" % (name, k)] = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        del xs
print(json.dumps(res))''')

LAB_SOL = '''class TaiKhoan:
    def __init__(self, ma, so_du=0, thau_chi=0):
        self.ma = ma
        self.so_du = so_du
        self.thau_chi = thau_chi

    def nap(self, tien):
        if tien <= 0:
            return False
        self.so_du = self.so_du + tien
        return True

    def rut(self, tien):
        if tien <= 0 or self.so_du - tien < -self.thau_chi:
            return False
        self.so_du = self.so_du - tien
        return True

    def __repr__(self):
        return f"TaiKhoan({self.ma}, {self.so_du})"

a = TaiKhoan("B07", 2000000, thau_chi=500000)
print(a.rut(2400000), a)
print(a.rut(200000), a)
print(a.nap(600000), a)
print(a.nap(-5), a)
b = TaiKhoan("B08")
print(b)

import sys
import tracemalloc

so = [i for i in range(1000)]
chuoi = ["x" * 100 + str(i) for i in range(1000)]
print("getsizeof hai danh sach:", "bang nhau" if sys.getsizeof(so) == sys.getsizeof(chuoi) else "khac nhau")


def dung(tao):
    tracemalloc.start()
    xs = tao()
    dang_dung = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    return dang_dung


m_so = dung(lambda: [i for i in range(1000)])
m_chuoi = dung(lambda: ["x" * 100 + str(i) for i in range(1000)])
print("tracemalloc hai danh sach:", "chuoi lon hon" if m_chuoi > m_so else "so lon hon")'''
LAB_OUT = "True TaiKhoan(B07, -400000)\nFalse TaiKhoan(B07, -400000)\nTrue TaiKhoan(B07, 200000)\nFalse TaiKhoan(B07, 200000)\nTaiKhoan(B08, 0)\ngetsizeof hai danh sach: bang nhau\ntracemalloc hai danh sach: chuoi lon hon"
P_LAB = py("lab_l06", LAB_SOL, LAB_OUT)

def build():
    c5, c6 = M("l06_mem", "m_cls_1e5"), M("l06_mem", "m_cls_1e6")
    s5, s6 = M("l06_mem", "m_slots_1e5"), M("l06_mem", "m_slots_1e6")
    t5, t6 = M("l06_mem", "m_tuple_1e5"), M("l06_mem", "m_tuple_1e6")
    bc5, bc6, bc8 = b_show(c5), b_show(c6), b_show(c6 * 100)
    bs5, bs6, bs8 = b_show(s5), b_show(s6), b_show(s6 * 100)
    bt5, bt6 = b_show(t5), b_show(t6)
    per = sig(c6 / 1e6, 2)
    mdemo = M("l06_demo", "m_demo")
    sc_hook = sc("hook", "hook", "Một triệu tài khoản trong bộ nhớ: mỗi cái tốn bao nhiêu?", [
        st(table(["số tài khoản nằm trong bộ nhớ", "lớp thường", "lớp có khai báo trước chỗ chứa", "bộ ba giá trị"],
                 [["100 000", bc5[0], bs5[0], bt5[0]], ["1 000 000", bc6[0], bs6[0], bt6[0]], ["100 000 000 (ngoại suy)", bc8[0], bs8[0], "—"]])
           + "<p class='note'>“Lớp có khai báo trước chỗ chứa” là cách khai báo lớp tiết kiệm bộ nhớ (học ở phần quy mô); “bộ ba giá trị” là ba giá trị xếp thành một bộ, như ở bài 3. Mỗi số đã gồm cả chuỗi và số bên trong. <b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo (ước lượng, chưa đo).</p>",
           f"""Chào bạn, một ngân hàng có một triệu tài khoản, mỗi tài khoản là một đối tượng có số hiệu, số dư, hạn mức. Trên máy kiểm, một triệu đối tượng như vậy chiếm {bc6[1]}, tức khoảng {vi_num(per)} byte mỗi đối tượng, đã tính cả chuỗi và số bên trong. Ngoại suy, tức nhân theo tỉ lệ từ số đã đo, một trăm triệu tài khoản cần {bc8[1]}."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li><b>Lớp</b> và <b>đối tượng</b> là gì, và <b>self</b> nghĩa là gì?</li>
<li>Khi nào dùng <b>kế thừa</b>, khi nào dùng <b>hợp thành</b> (một đối tượng chứa đối tượng khác)?</li>
<li>Hai đối tượng “bằng nhau” nghĩa là gì, và đối tượng tốn bao nhiêu bộ nhớ?</li></ol></div>""",
           """Hôm nay ta học ba điều. Lớp, đối tượng và tham số đầu tiên của phương thức. Kế thừa và hợp thành, tức một đối tượng chứa đối tượng khác. Hai đối tượng bằng nhau nghĩa là gì, và đối tượng tốn bao nhiêu bộ nhớ."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm, từ điển và biến là nhãn dán", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① hàm", "<code>def tong_tien(gia, ty_le=10)</code>: tên + tham số + trả về; mỗi lần gọi có hộp biến riêng"],
                  ["② từ điển", "<code>{\"ma\": \"A01\", \"so_du\": 100}</code>: các cặp khoá → giá trị"],
                  ["③ biến là nhãn", "<code>b = a</code> chỉ dán thêm nhãn, không sao chép (như với danh sách)"]]),
           """Hàm có tên, tham số và giá trị trả về, và mỗi lần gọi có hộp biến riêng. Từ điển là các cặp khoá và giá trị. Và biến chỉ là nhãn dán lên giá trị, nên gán biến này cho biến kia chỉ dán thêm nhãn, không sao chép.""",
           focus=["1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã khai báo lớp, hàm tạo, self, dấu chấm và hai dấu gạch dưới", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>class TaiKhoan:</code>", "khai báo lớp", "<b>bản vẽ</b>: mô tả mọi tài khoản có những gì và làm được gì"],
                  ["<code>TaiKhoan(\"A01\", 100)</code>", "tạo đối tượng", "dựng <b>một tài khoản cụ thể</b> từ bản vẽ; mỗi lần gọi ra một đối tượng mới"],
                  ["<code>def __init__(self, ma, so_du=0):</code>", "hàm tạo", "chạy <b>ngay khi tạo</b> đối tượng; <code>self</code> là <b>chính đối tượng đang được dựng</b>"]]),
           """Bảng đầu là ba thứ cơ bản. Khai báo lớp là một bản vẽ, mô tả mọi tài khoản có những gì và làm được những gì. Gọi tên lớp kèm các giá trị là dựng một tài khoản cụ thể từ bản vẽ, mỗi lần gọi ra một đối tượng mới. Hàm tạo chạy ngay khi dựng.
           Tham số đầu tiên trong nó là chính đối tượng đang được dựng."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>self.so_du = so_du</code>", "thuộc tính", "gắn <b>một dữ kiện</b> vào đối tượng: nhãn <code>so_du</code> dán vào chính nó"],
                  ["<code>a.nap(500000)</code>", "gọi phương thức", "hàm nằm trong lớp; <code>a</code> tự được đưa vào làm <code>self</code>"],
                  ["<code>__repr__</code>", "cách hiển thị", "hàm đặc biệt, tên có <b>hai dấu gạch dưới</b> hai đầu; quyết định đối tượng <b>in ra</b> thế nào"],
                  ["<code>class B(A):</code>", "kế thừa", "<code>B</code> có sẵn mọi thứ của <code>A</code> và thêm của riêng nó; <code>super()</code> gọi lớp cha"]]),
           """Bảng thứ hai là bốn điều nữa. Thuộc tính là một dữ kiện gắn vào đối tượng. Phương thức là hàm nằm trong lớp, và khi gọi qua đối tượng thì đối tượng tự được đưa vào làm tham số đầu. Hàm có hai dấu gạch dưới hai đầu là hàm đặc biệt, hàm hiển thị quyết định đối tượng in ra thế nào.
           Cuối cùng, kế thừa là lớp con có sẵn mọi thứ của lớp cha và thêm phần riêng, và có cách gọi lớp cha.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>a == b</code>, <code>a is b</code>", "bằng nhau, cùng một đối tượng", "<code>==</code> hỏi “nội dung bằng nhau?”; <code>is</code> hỏi “cùng <b>một</b> đối tượng trong bộ nhớ?”"],
                  ["<code>from dataclasses import dataclass</code>, <code>@dataclass</code>", "nạp công cụ, rồi lớp dữ liệu", "<code>from X import Y</code>: lấy riêng công cụ <code>Y</code> từ thư viện <code>X</code>, viết một lần ở đầu tệp; <code>@dataclass</code> đặt <b>ngay trước</b> lớp, nhờ máy viết giúp hàm tạo, cách hiển thị và so sánh; <code>ma: str</code> là ghi chú kiểu"]]),
           """Bảng cuối là hai điều về so sánh và viết gọn. Dấu hai bằng hỏi nội dung có bằng nhau không, còn phép so sánh danh tính hỏi có cùng một đối tượng trong bộ nhớ không. Dòng nạp lấy riêng một công cụ từ thư viện của nó, viết một lần ở đầu tệp. Dòng đánh dấu lớp dữ liệu đặt ngay trước lớp, nhờ máy viết giúp hàm tạo, cách hiển thị và so sánh.
           Phần tên kèm kiểu là một ghi chú kiểu.""",
           focus=[1, "1.2", "1.3", "1.3", "1.3"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: lớp là bản vẽ, đối tượng là ngôi nhà", [
        st(svg(1500, 420,
               box(40, 60, 380, 130, ["lớp TaiKhoan", "bản vẽ: ma, so_du", "nap, rut"], C_AMBER, 26, True),
               arrow(425, 100, 560, 80, "#d97706", "dựng"),
               arrow(425, 150, 560, 230, "#d97706"),
               txt(470, 232, "dựng", 22, "middle", "#d97706"),
               box(565, 30, 380, 120, ["a", "ma = A01", "so_du = 1 200 000"], C_BLUE, 26, True),
               box(565, 190, 380, 120, ["b", "ma = A02", "so_du = 50 000"], C_BLUE, 26, True),
               txt(1180, 100, "mỗi đối tượng có", 26, "middle", "#1f2937", True),
               txt(1180, 140, "dữ liệu RIÊNG", 26, "middle", "#1f2937", True),
               txt(1180, 230, "nhưng cùng dùng", 26, "middle", "#16a34a", True),
               txt(1180, 270, "hành vi của lớp", 26, "middle", "#16a34a", True),
               txt(750, 380, "a.nap(100) nghĩa là TaiKhoan.nap(a, 100): self chính là a", 28, "middle", "#dc2626", True)),
           """Hình này là ý chính. Lớp là bản vẽ, mô tả mọi tài khoản có số hiệu, số dư, và biết nạp, rút. Mỗi lần dựng ta được một đối tượng, như một ngôi nhà xây từ bản vẽ. Mỗi đối tượng có dữ liệu riêng, nhưng cùng dùng hành vi của lớp.
           Gọi nạp qua đối tượng a chính là gọi hàm nạp của lớp, với tham số đầu tiên là a."""),
        st(svg(1500, 400,
               box(60, 40, 300, 70, ["TaiKhoan"], C_AMBER, 26, True),
               arrow(210, 215, 210, 115, "#475569"),
               box(60, 220, 300, 70, ["TietKiem"], C_BLUE, 26, True),
               txt(230, 330, "kế thừa: LÀ MỘT", 26, "middle", "#1f2937", True),
               txt(230, 370, "khi hai thứ thật sự cùng loại", 24, "middle", "#6b7280"),
               box(560, 40, 320, 70, ["KhachHang"], C_AMBER, 26, True),
               box(600, 160, 240, 70, ["TaiKhoan"], C_BLUE, 26, True),
               arrow(720, 115, 720, 155, "#475569"),
               txt(720, 330, "hợp thành: CÓ MỘT", 26, "middle", "#1f2937", True),
               txt(720, 370, "khách hàng không phải là một tài khoản", 24, "middle", "#6b7280"),
               box(1030, 60, 420, 150, ["quy tắc chọn:", "câu “A là một B” đúng? → kế thừa", "câu “A có một B” đúng? → hợp thành", "không chắc → hợp thành"], C_GREEN, 24, True)),
           """Hình thứ hai là hai cách dùng lại. Kế thừa nghĩa là lớp con là một loại của lớp cha, như tài khoản tiết kiệm là một tài khoản. Hợp thành nghĩa là một đối tượng chứa đối tượng khác, như khách hàng có một tài khoản, chứ không phải là một tài khoản.
           Quy tắc chọn là đặt câu là một hay có một, câu nào đúng thì chọn cách đó, và khi không chắc thì chọn hợp thành.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: self, thuộc tính, hiển thị, so sánh", [
        st(repl_block(R_SELF, 0, 4, title="Bước 1. Gõ lớp, dựng đối tượng, gọi qua đối tượng")
           + "<p>Vì <code>a.nap(50)</code> tự đưa <code>a</code> vào làm <code>self</code>: $100 + 50 = 150$.</p>",
           """Bước một, tham số đầu tiên là gì. Ta gõ lớp có hàm tạo và phương thức nạp, dựng tài khoản có một trăm đồng, rồi gọi nạp năm mươi qua đối tượng. Vì nạp năm mươi vào một trăm, số dư thành một trăm năm mươi."""),
        st(repl_block(R_SELF, 4, 6, title="Bước 1 (tiếp phiên trên). Gọi qua lớp, đối tượng là tham số đầu")
           + "<p>Vì <code>a.nap(50)</code> tự đưa <code>a</code> vào làm <code>self</code>, nó <b>cùng nghĩa</b> với <code>TaiKhoan.nap(a, 50)</code>: nạp thêm $50$ lên $200$ ✓</p>",
           """Gọi qua lớp, đưa đối tượng vào làm tham số đầu, cũng nạp năm mươi, số dư thành hai trăm. Vì gọi qua đối tượng tự đưa đối tượng vào làm tham số đầu tiên, hai cách gọi cùng nghĩa.""", clear=True),
        st(repl_block(R_SELF, 6, 8, title="Bước 2. Về khái niệm, đối tượng là một từ điển thuộc tính")
           + "<p>Vì mỗi dòng <code>self.x = …</code> thêm một cặp vào từ điển của đối tượng, <code>a.__dict__</code> cho thấy đúng hai cặp <code>ma</code> và <code>so_du</code> (lớp khai báo trước chỗ chứa, ở phần quy mô, thì không có từ điển này; từ Python 3.11 máy dựng từ điển đó muộn, chỉ khi cần). "
             "<code>isinstance(a, TaiKhoan)</code> hỏi <code>a</code> có phải đối tượng của lớp <code>TaiKhoan</code> (hoặc lớp con của nó) không: đúng hoặc sai.</p>",
           """Bước hai, đối tượng bên trong là gì. Vì mỗi dòng gán qua đối tượng thêm một cặp vào từ điển riêng của nó, ta nhìn thẳng vào từ điển đó và thấy hai cặp, mã và số dư. Về mặt khái niệm, đối tượng thường là một từ điển thuộc tính kèm liên kết tới lớp, và từ phiên bản ba chấm mười một máy dựng từ điển đó muộn, chỉ khi cần.
           Câu hỏi cuối hỏi a có phải đối tượng của lớp tài khoản không, và máy trả lời đúng.""", clear=True, introduces=["pyt_isinstance"]),
        st(code_block(P_TK, lines=(7, 11), title="Bước 3. Phương thức rút kiểm tra điều kiện trước khi đổi số dư")
           + "<p>Python <b>không cấm</b> gán thẳng: <code>a.so_du = -999</code> vẫn chạy. Giữ dữ liệu hợp lệ là <b>quy ước</b>: chỉ đổi qua phương thức.</p>",
           """Bước ba, phương thức kiểm tra điều kiện. Phương thức rút trả về sai nếu số tiền lớn hơn số dư, và không đổi gì cả. Chỉ khi đủ tiền, nó trừ số dư rồi trả về đúng.
           Ngôn ngữ không ngăn ai gán thẳng một giá trị khác, nên giữ dữ liệu hợp lệ chỉ là quy ước.""", clear=True),
        st(run_block(P_EQ, title="Bước 4. Hai đối tượng cùng nội dung chưa chắc “bằng nhau”")
           + "<p>Vì mặc định <code>==</code> chỉ hỏi <b>cùng một đối tượng</b> hay không, hai tài khoản <code>A01</code> riêng biệt cho <code>False</code>. Muốn so nội dung phải viết thêm hàm so sánh, hoặc dùng lớp dữ liệu.</p>",
           """Bước bốn, so sánh. Vì mặc định phép so bằng chỉ hỏi có cùng một đối tượng không, hai tài khoản riêng biệt dù cùng mã vẫn cho sai. Muốn so nội dung, phải viết thêm hàm so sánh, hoặc dùng lớp dữ liệu.""", clear=True),
    ], checks=["100 + 50 + 50 == 200", "1500000 - 300000 == 1200000"])
    sc_ex = sc("example", "example", "Ví dụ: tài khoản nạp và rút, lớp dữ liệu, kế thừa và hợp thành", [
        st(code_block(P_TK, lines=(1, 13), title="Tệp tai_khoan.py: lớp đầy đủ (f\"…{x}…\" điền giá trị của x vào chuỗi)"),
           """Ví dụ một, lớp tài khoản đầy đủ. Ngoài hàm tạo và nạp, nó có phương thức rút kiểm tra điều kiện, và hàm hiển thị, dùng chuỗi có chỗ điền, quyết định dòng in đối tượng ra sao."""),
        st(run_block(P_TK, lines=(15, 18), title="Dùng lớp: nạp, rút quá số dư, rút hợp lệ"),
           """Giờ ta dùng lớp. Dựng tài khoản A không một với một triệu. Nạp năm trăm nghìn được một triệu rưỡi. Rút hai triệu bị từ chối, trả về sai và số dư không đổi. Rút ba trăm nghìn thì được, trả về đúng, số dư còn một triệu hai trăm nghìn."""),
        st(code_block(P_DC, lines=(1, 7), title="Lớp dữ liệu: chỉ cần dòng đánh dấu và ba trường"),
           """Ví dụ hai, lớp dữ liệu. Chỉ cần dòng đánh dấu và khai báo ba trường, máy viết giúp hàm tạo, cách hiển thị và so sánh.""", clear=True),
        st(run_block(P_DC, lines=(9, 12), title="Dùng thử: in đọc được, so sánh theo nội dung"),
           """In ra đọc được ngay, và hai giao dịch cùng nội dung bằng nhau, nhưng vẫn là hai đối tượng khác nhau.""", clear=True),
        st(code_block(P_KT, lines=(1, 7), title="Kế thừa (1/2): lớp cha TaiKhoan"),
           """Ví dụ ba, kế thừa. Ta bắt đầu từ lớp cha tài khoản.""", clear=True),
        st(code_block(P_KT, lines=(9, 15), title="Kế thừa (2/2): tiết kiệm là một tài khoản, thêm cộng lãi"),
           """Lớp tiết kiệm đặt lớp tài khoản trong ngoặc, nên có sẵn mã, số dư và nạp. Nó gọi lớp cha để khởi tạo phần chung, rồi thêm lãi suất theo phần nghìn và hàm cộng lãi, tự nạp tiền lãi vào số dư.""", clear=True),
        st(code_block(P_KT, lines=(17, 20), title="Hợp thành: khách hàng CÓ một tài khoản"),
           """Ví dụ bốn, hợp thành. Khách hàng chứa một tài khoản làm thuộc tính, không kế thừa.""", clear=True),
        st(run_block(P_KT, lines=(22, 26), title="Dùng: tiết kiệm cộng lãi, rồi đưa cho khách hàng")
           + "<p>$\\frac{2\\,000\\,000 \\cdot 5}{1000} = 10\\,000$ lãi, nên số dư $2\\,010\\,000$ ✓</p>",
           """Ta dựng tài khoản tiết kiệm hai triệu với lãi năm phần nghìn, cộng lãi được mười nghìn, rồi đưa nó cho khách hàng. In ra tên khách hàng và số dư hai triệu không trăm mười nghìn.""", clear=True),
        st(run_block(P_SIZE, title="Đo bộ nhớ, cách 1: hỏi kích thước một giá trị")
           + "<p><code>sys.getsizeof(x)</code> trả số <b>byte</b> của riêng <code>x</code>: danh sách $1000$ ô chiếm $56 + 1000 \\cdot 8 = 8056$ byte vì mỗi ô chỉ là một <b>con trỏ</b>: số $8$ byte ghi chỗ chứa giá trị thật; những gì các ô trỏ tới <b>không được tính</b>.</p>",
           """Cách đo thứ nhất là lệnh hỏi kích thước một giá trị. Số nguyên nhỏ chiếm hai mươi tám byte, danh sách rỗng năm mươi sáu byte.
           Danh sách một nghìn phần tử chiếm tám nghìn không trăm năm mươi sáu byte, bằng năm mươi sáu cộng một nghìn lần tám. Mỗi ô chỉ là một con trỏ, tức một số tám byte ghi chỗ chứa giá trị thật. Lệnh này không tính những gì các ô trỏ tới.""", clear=True, introduces=["pyt_getsizeof"]),
        st(table(["viết trong mã", "đọc là", "nghĩa"],
                 [["<code>str(i)</code>", "đổi sang chuỗi", "đổi số <code>i</code> thành chữ, để ghép với chữ khác: <code>\"A\" + str(5)</code> ra <code>\"A5\"</code>"],
                  ["<code>[A(…) for i in range(n)]</code>", "danh sách suy ra", "dựng một đối tượng cho mỗi <code>i</code> từ $0$ tới $n - 1$, rồi xếp tất cả vào một danh sách"],
                  ["<code>dang_dung, dinh = tracemalloc.get_traced_memory()</code>", "gán hai tên cùng lúc", "hàm trả <b>hai số</b>: số byte <b>đang dùng</b> và số byte <b>đỉnh</b>; gán theo thứ tự cho hai tên (ở đây chỉ dùng <code>dang_dung</code>)"]]),
           """Ba điều trong khối đo. Lệnh đổi sang chuỗi biến số thành chữ. Danh sách suy ra dựng một đối tượng cho mỗi số. Lệnh theo dõi bộ nhớ trả hai số, byte đang dùng và byte đỉnh, gán cho hai tên.""", clear=True, introduces=["pyt_tracemalloc"]),
        st(raw_block(DEMO_MEM.split("\n"), title="Đo bộ nhớ, cách 2: theo dõi mọi byte chương trình đã xin thêm", py_hl=True)
           + f'<div class="code"><div>{round(mdemo / 1e6, 1)} MB</div></div>',
           """Cách thứ hai tính cả những thứ mà đối tượng trỏ tới. Ta bật công cụ theo dõi bộ nhớ, dựng một trăm nghìn đối tượng, rồi hỏi số byte đang dùng và chia cho một triệu.""",
           clear=True),
        st("<div class='box key'><code>tracemalloc</code> đếm <b>mọi</b> byte chương trình đã xin thêm từ lúc bật, kể cả chuỗi và số bên trong đối tượng; chia cho $10^6$ ra MB (số minh hoạ, máy khác cho số khác).</div>",
           """Các bảng ở phần quy mô đo bằng cách này.""", clear=True),
    ], checks=["1000000 + 500000 - 300000 == 1200000", "2000000 * 5 // 1000 == 10000 and 2000000 + 10000 == 2010000", "56 + 1000 * 8 == 8056"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: bảo toàn số dư, rút bị từ chối không đổi gì", [
        st(repl_block(R_KIEM, title="Cộng trừ tay, không qua lớp")
           + "<p>Số dư cuối phải bằng số dư đầu cộng tổng nạp, trừ tổng rút <b>đã được chấp nhận</b>: $1\\,000\\,000 + 500\\,000 - 300\\,000 = 1\\,200\\,000$. Lần rút $2\\,000\\,000$ bị từ chối nên không tính ✓</p>",
           """Đường kiểm khác, cộng trừ tay. Vì số dư cuối phải bằng số dư đầu cộng tổng nạp, trừ tổng rút đã được chấp nhận, ta có một triệu cộng năm trăm nghìn trừ ba trăm nghìn bằng một triệu hai trăm nghìn."""),
    ], checks=["1000000 + 500000 - 300000 == 1200000"])
    sc_scale = sc("scale", "concept", "Khi số đối tượng lớn dần: mỗi đối tượng tốn bộ nhớ, và có cách giảm", [
        st(table(["số đối tượng", "lớp thường", "lớp khai báo trước chỗ chứa (__slots__)", "bộ ba giá trị"],
                 [["×1: 100 000", bc5[0], bs5[0], bt5[0]], ["×10: 1 000 000", bc6[0], bs6[0], bt6[0]], ["×1 000 (ngoại suy): 100 000 000", bc8[0], bs8[0], "—"]])
           + "<p class='note'>Đo bằng công cụ theo dõi bộ nhớ trên máy kiểm (kể cả chuỗi và số bên trong); số minh hoạ; ngoại suy = nhân theo tỉ lệ từ số đã đo. Khai báo trước chỗ chứa: viết một dòng <code>__slots__ = (\"ma\", \"so_du\", \"han_muc\")</code> ngay dưới dòng <code>class</code>, lớp chỉ giữ đúng các thuộc tính đó.</p>",
           f"""Một trăm nghìn đối tượng lớp thường chiếm {bc5[1]}, một triệu chiếm {bc6[1]}. Khai báo trước chỗ chứa là viết ngay dưới dòng khai báo lớp một dòng liệt kê đúng các thuộc tính, và nó giảm xuống còn {bs6[1]} cho một triệu. Bộ ba giá trị đơn giản chiếm {bt6[1]}.
           Ngoại suy, một trăm triệu đối tượng lớp thường cần {bc8[1]}."""),
        st("<div class='box key'><b>Đánh đổi:</b> lớp thường lưu thuộc tính theo kiểu từ điển linh hoạt (từ 3.11 máy dựng từ điển muộn, chỉ khi cần) nên vẫn tốn thêm, đổi lại linh hoạt (thêm thuộc tính lúc chạy). "
           "Khai báo trước chỗ chứa tiết kiệm bộ nhớ nhưng cứng hơn. Với hàng trăm triệu bản ghi, người làm nghề <b>không giữ hết trong bộ nhớ dạng đối tượng</b>: họ xử lý theo dòng, theo khối, hoặc để dữ liệu ở cơ sở dữ liệu.</div>",
           """Đánh đổi là lớp thường lưu thuộc tính linh hoạt hơn, nên tốn thêm bộ nhớ. Khai báo trước chỗ chứa tiết kiệm bộ nhớ nhưng cứng hơn. Với hàng trăm triệu bản ghi, người làm nghề xử lý theo dòng, theo khối, hoặc để dữ liệu ở cơ sở dữ liệu.""", clear=True),
    ], checks=["100 * 10 ** 6 == 10 ** 8", "1000 * 10 ** 5 == 10 ** 8"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên <code>self</code> ở tham số đầu của phương thức.</div>' + run_block(P_SELF)
           + "<p><code>pass</code> nghĩa là <b>không làm gì</b>: chỗ giữ để khối lệnh không bị rỗng.</p>",
           """Lỗi thứ nhất, của người mới, là quên chỗ dành cho đối tượng ở tham số đầu của phương thức. Dòng không làm gì chỉ giữ chỗ cho khối lệnh. Chương trình chạy tới lệnh gọi thì dừng.""", introduces=["pyt_pass"]),
        st("<div class='box key'>Máy tự đưa đối tượng vào làm tham số đầu, nên <code>nap(tien)</code> nhận <b>2</b> giá trị mà chỉ khai <b>1</b> chỗ. Đọc dòng cuối là thấy.</div>",
           """Máy tự đưa đối tượng vào làm tham số đầu, nên phương thức nhận hai giá trị mà chỉ khai một chỗ. Đọc dòng cuối là thấy ngay.""", clear=True),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Đặt danh sách ở cấp lớp: mọi đối tượng dùng chung (<code>.append(x)</code> thêm <code>x</code> vào cuối).</div>' + code_block(P_CHUNG, lines=(1, 8)),
           """Lỗi thứ hai, của người đã đi làm, là đặt danh sách ở cấp lớp, rồi thêm phần tử vào cuối bằng lệnh nối thêm. Mọi đối tượng dùng chung một danh sách."""),
        st(run_block(P_CHUNG, lines=(10, 13), title="Dùng: nạp vào A01, hỏi lịch sử của A02")
           + "<p>Phép thử: nạp vào <code>A01</code> mà <code>A02</code> cũng thấy lịch sử. Sửa: tạo danh sách <b>trong hàm tạo</b> bằng <code>self.lich_su = []</code>.</p>",
           """Nạp tiền vào tài khoản A không một mà tài khoản A không hai cũng thấy lịch sử. Lỗi này không báo gì.""", clear=True),
        st(run_block(P_CHUNG2, lines=(1, 12), title="Cách sửa: mỗi đối tượng một danh sách riêng"),
           """Cách sửa là tạo danh sách trong hàm tạo, gắn vào đối tượng. Khi đó mỗi đối tượng có danh sách riêng, nạp vào A không một thì A không hai vẫn rỗng. Quy tắc nhớ: dữ liệu riêng của đối tượng đặt trong hàm tạo.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người mới).</b> Tưởng gán đối tượng là sao chép nó.</div>' + repl_block(R_ALIAS, 0, 5)
           + "<p>Như danh sách: <code>b = a</code> chỉ dán thêm nhãn. Nạp qua <code>b</code>, số dư của <code>a</code> đổi. Phép thử: <code>a is b</code>.</p>",
           """Lỗi thứ ba, của người mới, là tưởng gán đối tượng là sao chép nó. Giống danh sách, gán chỉ dán thêm nhãn. Nạp qua nhãn b, số dư của đối tượng mà a trỏ tới cũng đổi, vì chỉ có một đối tượng.""", clear=True),
    ], checks=["100 + 50 == 150"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> <code>a = TaiKhoan("A01", 100)</code>, rồi <code>b = a</code>, rồi <code>b.nap(50)</code>.</p>
<ol><li><code>a.so_du</code> bằng bao nhiêu? Vì sao?</li>
<li>Muốn <code>b</code> là bản <b>độc lập</b> của <code>a</code>, làm thế nào?</li></ol>
<p><b>Quyết định:</b> <code>TheNganHang</code> và <code>TaiKhoan</code>: dùng <b>kế thừa</b> hay <b>hợp thành</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Dựng tài khoản a có một trăm đồng, gán b bằng a, rồi nạp năm mươi qua b. Câu một, số dư của a bằng bao nhiêu và vì sao. Câu hai, muốn b là bản độc lập của a thì làm thế nào.
           Rồi một quyết định, thẻ ngân hàng và tài khoản, dùng kế thừa hay hợp thành, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_QUIZ, 0, 5, title="Câu 1")
           + "<p>$a$ và $b$ là <b>hai nhãn của cùng một đối tượng</b>, nên nạp qua $b$ thì $a$ thấy: $100 + 50 = 150$. Muốn bản độc lập: dựng đối tượng mới, ví dụ <code>TaiKhoan(a.ma, a.so_du)</code>.</p>",
           """Đáp án như sau. Vì a và b là hai nhãn của cùng một đối tượng, nạp qua b thì a thấy, một trăm cộng năm mươi bằng một trăm năm mươi. Muốn bản độc lập, ta dựng đối tượng mới, truyền mã và số dư của a vào."""),
        st("<div class='box key'><b>Quyết định:</b> <b>hợp thành</b>. Một thẻ <b>có một</b> tài khoản đứng sau, nhưng thẻ <b>không phải là</b> một tài khoản. "
           "Kế thừa buộc chặt hai lớp (đổi lớp cha có thể làm vỡ lớp con); hợp thành lỏng hơn và dễ thay tài khoản khác.</div>",
           """Quyết định, chọn hợp thành. Thẻ có một tài khoản đứng sau, nhưng thẻ không phải là một tài khoản. Kế thừa buộc chặt hai lớp, đổi lớp cha có thể làm vỡ lớp con. Hợp thành lỏng hơn và dễ thay bằng tài khoản khác.""", clear=True),
    ], checks=["100 + 50 == 150"])
    sc_prac = practice_scene(sc, "Tự làm: lớp TaiKhoan có nạp, rút và kiểm số dư", [st(
        raw_block(['a = TaiKhoan("B07", 2000000, thau_chi=500000)', "print(a.rut(2400000), a)", "print(a.rut(200000), a)", "print(a.nap(600000), a)",
                   "print(a.nap(-5), a)", 'b = TaiKhoan("B08")', "print(b)"], title="Đoạn thử cho sẵn: thêm ĐÚNG như vậy vào cuối tệp tai_khoan.py", py_hl=True)
        + "<p class='note'>Cũng có trong <code>de.md</code>. Dựng tài khoản có <b>thấu chi</b> $500\\,000$ (thấu chi = mức số dư được phép âm), thử rút, nạp, rồi in kết quả cùng tài khoản.</p>",
        """Xem đoạn thử cho sẵn và thêm đúng đoạn này vào cuối tệp. Nó dựng tài khoản có thấu chi, tức mức số dư được phép âm, năm trăm nghìn, thử rút và nạp, mỗi dòng in kết quả kèm tài khoản.""")] + pr_steps(
        st, "PYT", "L06",
        """<p><b>Đề</b>: tạo <code>tai_khoan.py</code> với lớp <code>TaiKhoan(ma, so_du=0, thau_chi=0)</code> (<b>thấu chi</b> = mức số dư được phép âm):</p>
<ol><li><code>nap(tien)</code>: <code>tien &lt;= 0</code> thì trả <code>False</code>; ngược lại cộng và trả <code>True</code>;</li>
<li><code>rut(tien)</code>: trả <code>False</code> (không đổi gì) nếu <code>tien &lt;= 0</code> hoặc số dư sau khi rút sẽ nhỏ hơn <code>-thau_chi</code>; ngược lại trừ và trả <code>True</code>;</li>
<li><code>__repr__</code> trả <code>TaiKhoan(mã, số_dư)</code>; rồi chạy đoạn thử ở màn hình trước (5 dòng in).</li></ol>
<p><b>Đo</b> hai danh sách $1000$ phần tử (số; chuỗi dài $100$ ký tự), in <code>getsizeof hai danh sach: bang nhau</code> và <code>tracemalloc hai danh sach: chuoi lon hon</code>.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết lớp tài khoản có mã, số dư và hạn mức thấu chi, tức mức số dư được phép âm. Phương thức nạp từ chối số tiền không dương. Phương thức rút từ chối khi số tiền không dương hoặc khi số dư sau rút thấp hơn âm hạn mức, và khi từ chối thì không đổi gì. Viết thêm hàm hiển thị.
        Rồi chạy đoạn thử vừa thấy. Cuối cùng, tự đo hai danh sách một nghìn phần tử, một danh sách số, một danh sách chuỗi dài, bằng cả hai cách đo, và in hai dòng so sánh. Hãy dừng video và làm.""",
        LAB_OUT, "tai_khoan.py",
        """<div class="box key"><b>Nếu kẹt:</b> điều kiện từ chối của <code>rut</code>: <code>tien &lt;= 0 or self.so_du - tien &lt; -self.thau_chi</code>. Mọi nhánh từ chối phải <code>return False</code> <b>trước</b> khi đổi <code>self.so_du</code>. Hàm hiển thị dùng <code>f"TaiKhoan({self.ma}, {self.so_du})"</code>. Phần đo: <code>sys.getsizeof(ds)</code> chỉ tính chính danh sách; với công cụ theo dõi, gọi <code>tracemalloc.start()</code>, tạo danh sách, đọc <code>tracemalloc.get_traced_memory()[0]</code>, rồi <code>tracemalloc.stop()</code>.
Lời giải ở <code>labs/PYT/L06/loi_giai.py</code>.</div>""",
        """Nếu kẹt, điều kiện từ chối của phương thức rút ghép hai vế bằng từ hoặc. Mọi nhánh từ chối phải trả về sai trước khi đổi số dư. Hàm hiển thị dùng chuỗi có chỗ điền với mã và số dư. Phần đo, lệnh hỏi kích thước chỉ tính chính danh sách, còn công cụ theo dõi cho số byte đang dùng sau khi tạo.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L06")
    write_lab("PYT", "L06", """# Lab PYT L06 — Lớp TaiKhoan có nạp, rút, thấu chi

Cần: Python 3.11 trở lên. Tạo `tai_khoan.py` với lớp `TaiKhoan(ma, so_du=0, thau_chi=0)` (`thau_chi` = thấu chi: mức số dư được phép âm; số minh hoạ, khác ví dụ trong bài):

- `nap(tien)`: nếu `tien <= 0` trả `False`, không đổi gì; ngược lại cộng vào số dư và trả `True`.
- `rut(tien)`: trả `False` (không đổi gì) nếu `tien <= 0` **hoặc** số dư sau khi rút sẽ nhỏ hơn `-thau_chi`; ngược lại trừ và trả `True`.
- `__repr__`: trả chuỗi `TaiKhoan(<ma>, <so_du>)`.

Rồi thêm **đúng đoạn thử này** vào cuối tệp:

```python
a = TaiKhoan("B07", 2000000, thau_chi=500000)
print(a.rut(2400000), a)
print(a.rut(200000), a)
print(a.nap(600000), a)
print(a.nap(-5), a)
b = TaiKhoan("B08")
print(b)
```

**Phần đo** (lab chấm *hình dạng* kết quả, không chấm số byte tuyệt đối vì mỗi máy một khác): thêm tiếp, sau đoạn thử, `import sys` và `import tracemalloc`; tạo `so = [i for i in range(1000)]` và `chuoi = ["x" * 100 + str(i) for i in range(1000)]`.

- In `getsizeof hai danh sach: bang nhau` nếu `sys.getsizeof(so) == sys.getsizeof(chuoi)`, ngược lại `getsizeof hai danh sach: khac nhau`.
- Với mỗi danh sách, `tracemalloc.start()`, tạo danh sách (viết lại câu tạo trong một hàm), lấy `tracemalloc.get_traced_memory()[0]` rồi `tracemalloc.stop()`. In `tracemalloc hai danh sach: chuoi lon hon` nếu số byte của danh sách chuỗi lớn hơn, ngược lại `tracemalloc hai danh sach: so lon hon`.

Chạy: `python tai_khoan.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L06 tai_khoan.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("lớp = bản vẽ; đối tượng = một cái dựng từ bản vẽ", "self = chính đối tượng; dữ liệu riêng đặt trong hàm tạo", "theo quy ước, đổi dữ liệu qua phương thức có kiểm tra (Python không ép)",
                 "== so nội dung (khi có), is so cùng đối tượng", "kế thừa = là một; hợp thành = có một", "mỗi đối tượng tốn bộ nhớ: đo trước khi nhân lên"),
           """Tổng kết chuỗi logic. Lớp là bản vẽ, đối tượng là một cái dựng từ bản vẽ. Tham số đầu tiên là chính đối tượng, và dữ liệu riêng đặt trong hàm tạo. Theo quy ước, mọi thay đổi đi qua phương thức có kiểm tra điều kiện. Phép so bằng hỏi nội dung nếu có viết, còn phép so sánh danh tính hỏi cùng một đối tượng.
           Kế thừa là câu là một, hợp thành là câu có một. Và mỗi đối tượng tốn bộ nhớ, nên đo trước khi nhân lên."""),
        st("""<div class='box key'><b>Tư duy:</b> đối tượng tốt <b>giữ dữ liệu của mình hợp lệ</b>: ta thoả thuận không ai sửa số dư từ bên ngoài mà bỏ qua kiểm tra (Python không ép, ta tự giữ kỷ luật). Khi phân vân kế thừa hay hợp thành, chọn <b>hợp thành</b>.</div>
<p>Bài sau: bắt lỗi và gỡ lỗi, để chương trình xử lý lỗi một cách có chủ đích thay vì chết giữa chừng.</p>""",
           """Điều cần mang theo, một đối tượng tốt giữ dữ liệu của mình hợp lệ, và ta thoả thuận không ai sửa số dư từ bên ngoài mà bỏ qua kiểm tra, vì ngôn ngữ không ép. Khi phân vân giữa kế thừa và hợp thành, hãy chọn hợp thành.
           Bài sau, ta học cách bắt lỗi và gỡ lỗi, để chương trình xử lý lỗi một cách có chủ đích thay vì chết giữa chừng.""", forward_ref=True),
    ])
    return lesson("L06", "lop_va_doi_tuong", "Bài 6 — Lớp và đối tượng: gói dữ liệu cùng hành vi",
                  "curriculum/pyt.yaml L06; audit/pyt/verify_pyt.py L06 (chạy thật trên Python 3.11 và 3.13; bộ nhớ của 10^5 và 10^6 đối tượng đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính); "
                  "Python Tutorial §9 (Classes), Library Reference: dataclasses, sys.getsizeof, tracemalloc; Data Model (object.__repr__, __eq__, __slots__); nguyên tắc ưu tiên hợp thành hơn kế thừa (Gamma, Helm, Johnson, Vlissides, Design Patterns, 1994 — chỉ nêu nguyên tắc; NOT_VERIFIED trang)",
                  ["Khai báo lớp có hàm tạo và phương thức, và dựng đối tượng",
                   "Nêu self là chính đối tượng và đối tượng gồm các thuộc tính riêng",
                   "Viết cách hiển thị và dùng lớp dữ liệu để máy viết giúp",
                   "Viết phương thức rút kiểm tra điều kiện trước khi đổi số dư",
                   "Nêu khi nào dùng kế thừa và khi nào dùng hợp thành",
                   "Giải thích khác biệt giữa so bằng và cùng một đối tượng",
                   "Nêu bộ nhớ của đối tượng thay đổi thế nào ở ba quy mô",
                   "Chỉ ra ba lỗi hay gặp: quên self, danh sách dùng chung ở cấp lớp, gán thay cho sao chép",
                   "Viết lớp TaiKhoan có nạp, rút và kiểm số dư",
                   "Đo bộ nhớ của dữ liệu bằng sys.getsizeof và tracemalloc, và nêu hai cách khác nhau ở đâu"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy", "pyt_repr"],
                  covers=[(1, "example"), (2, "formula"), (3, "example"), (4, "example"), (5, "quiz"), (6, "formula"), (7, "scale"), (8, "pitfalls"), (9, "practice"), (10, "example")])
