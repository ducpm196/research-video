from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_a import t2, val2

R_PRE = repl("Pre", [("gia = 2000000", ""), ("gia * 10 // 100", "200000"), ("gia + gia * 10 // 100", "2200000")])
R_DEFAULT = repl("MacDinh", [
    ("def tong_tien(gia, ty_le=10):\n    return gia + gia * ty_le // 100\n", ""),
    ("tong_tien(2000000)", "2200000"), ("tong_tien(2000000, 8)", "2160000"), ("tong_tien(ty_le=8, gia=2000000)", "2160000"),
])
R_FUNCVAL = repl("HamLaGiaTri", [
    ("def tang(x):\n    return x + 1\n", ""), ("tang(5)", "6"), ("f = tang", ""), ("f(5)", "6"), ("type(tang)", "<class 'function'>"),
    ("(lambda x: x + 1)(5)", "6"),
])
R_MIN = repl("Min", [("min(0.31, 0.29, 0.30)", "0.29")])
R_QUIZ = repl("Quiz", [("def gap(x):\n    return x * 2\n", ""), ("gap(gap(3))", "12"), ("gap(3) + gap(4)", "14")])

P_HAM = py("ham", '''def tinh_vat(gia, ty_le=10):
    return gia * ty_le // 100

def tong_tien(gia, ty_le=10):
    return gia + tinh_vat(gia, ty_le)

print("VAT:", tinh_vat(2000000))
print("Tong:", tong_tien(2000000))
print("Tong (8%):", tong_tien(2000000, ty_le=8))''', "VAT: 200000\nTong: 2200000\nTong (8%): 2160000")
P_SCOPE = py("pham_vi", '''TY_LE = 10

def tong_tien(gia):
    phi_them = gia * TY_LE // 100
    return gia + phi_them

print(tong_tien(2000000))
print(phi_them)''', "2200000", expect="error:NameError", err="NameError: name 'phi_them' is not defined")
P_LAMBDA = py("ap_dung", '''def ap_dung(ham, x):
    return ham(x)

def them_vat(g):
    return g * 110 // 100

print(ap_dung(them_vat, 2000000))
print(ap_dung(lambda g: g * 108 // 100, 2000000))''', "2200000\n2160000")
P_NORET = py("quen_return", '''def tinh_vat(gia):
    vat = gia * 10 // 100
    print(vat)

ket_qua = tinh_vat(2000000)
print("Ket qua:", ket_qua)''', "200000\nKet qua: None")
P_UNB = py("gan_trong_ham", '''tong = 0

def cong(x):
    tong = tong + x

cong(5)''', "", expect="error:UnboundLocalError",
           err="UnboundLocalError: cannot access local variable 'tong' where it is not associated with a value")
P_SWAP = py("doi_cho", '''def chia_deu(tong, so_nguoi):
    return tong // so_nguoi

print(chia_deu(2000000, 4))
print(chia_deu(4, 2000000))
print(chia_deu(so_nguoi=4, tong=2000000))''', "500000\n0\n500000")
# Phép đo so sánh gọi hàm với viết thẳng: mỗi cách chạy TRONG MỘT HÀM (biến cục bộ), lấy lần nhanh nhất của 3 lần; hàm chỉ có MỘT phép cộng nên tỉ lệ là cận trên.
CODE_HAI = '''def tang(x):
    return x + 1
def goi(n):
    y = 0
    for i in range(n):
        y = tang(y)
    return y
def thang(n):
    y = 0
    for i in range(n):
        y = y + 1
    return y'''
P_HAI = py("hai_cach", CODE_HAI + "\nprint(goi(10), thang(10))", "10 10")
measure("l02_call", '''import json, time
''' + CODE_HAI + '''
def do(ham, n):
    tot = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        assert ham(n) == n
        tot = min(tot, time.perf_counter() - t0)
    return tot
res = {}
for k, n in (("1e6", 10 ** 6), ("1e7", 10 ** 7)):
    res["t_call_" + k] = do(goi, n)
    res["t_inline_" + k] = do(thang, n)
print(json.dumps(res))''')
# Chương trình minh hoạ cách đo (hiện nguyên văn trên màn hình): số giây in ra là số đo thật (máy khác cho số khác).
DEMO_DO = '''import time
def tang(x):
    return x + 1
def chay(n):
    y = 0
    for i in range(n):
        y = tang(y)

t0 = time.perf_counter()
chay(1000000)
print(round(time.perf_counter() - t0, 2), "giay")'''
measure("l02_demo", DEMO_DO + "\nimport json\nprint(json.dumps({'t_demo': time.perf_counter() - t0}))")

LAB_SOL = '''def phi_rut(tien):
    if tien < 2000000:
        return 1100
    return tien * 5 // 10000

def vat(phi, ty_le=10):
    return phi * ty_le // 100

def tong_chi(tien, ham_phi):
    phi = ham_phi(tien)
    return phi + vat(phi)

for tien in [500000, 3000000, 80000000]:
    print(tien, phi_rut(tien), tong_chi(tien, phi_rut))
print(tong_chi(3000000, lambda t: t // 1000))

import time


def do(ham):
    tot = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        ham()
        tot = min(tot, time.perf_counter() - t0)
    return tot


def goi():
    for _ in range(1000000):
        vat(1100)


def thang():
    phi = 1100
    for _ in range(1000000):
        phi * 10 // 100


print("Goi ham cham hon viet thang:", "CO" if do(goi) > do(thang) else "KHONG")'''
LAB_OUT = "500000 1100 1210\n3000000 1500 1650\n80000000 40000 44000\n3300\nGoi ham cham hon viet thang: CO"
P_LAB = py("lab_l02", LAB_SOL, LAB_OUT)

def build():
    c6, c7 = M("l02_call", "t_call_1e6"), M("l02_call", "t_call_1e7")
    i6, i7 = M("l02_call", "t_inline_1e6"), M("l02_call", "t_inline_1e7")
    sc6, sc7, si6, si7 = t2(c6), t2(c7), t2(i6), t2(i7)
    sc9 = t2(c7 * 100)
    ratio = round(val2(c7) / val2(i7), 1)   # tỉ lệ tính từ chính hai số hiện trên màn hình
    ratio6 = round(val2(c6) / val2(i6), 1)
    lo_r, hi_r = min(ratio, ratio6), max(ratio, ratio6)
    giay_demo = c6   # chương trình minh hoạ đo đúng việc này (10^6 lần gọi hàm); hiện số của lần đo nhanh nhất để khớp bảng bên dưới
    sc_hook = sc("hook", "hook", "Công thức thuế chép ở 40 chỗ, sửa quên 3 chỗ", [
        st(code_block(P_HAM, title="Công thức thuế viết MỘT lần, đặt tên") + out_block(P_HAM),
           """Chào bạn, giả sử công thức tính thuế giá trị gia tăng được chép vào bốn mươi chỗ trong một hệ thống. Khi thuế suất đổi, ai đó sửa ba mươi bảy chỗ và quên ba chỗ. Sổ sách của khách hàng ở ba chỗ đó sai, và không có thông báo lỗi nào. Đây là số minh hoạ, nhưng lỗi kiểu này rất thật.
           Cách tránh là viết công thức một lần, đặt cho nó một cái tên, rồi gọi tên đó ở mọi nơi. Đó chính là hàm.
           Chữ viết tắt ở đầu dòng kết quả đầu tiên là tên tiếng Anh của thuế giá trị gia tăng."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Cách <b>khai báo hàm</b>: tham số vào, giá trị <b>trả về</b> ra?</li>
<li>Biến nằm ở đâu thì ai nhìn thấy: <b>phạm vi</b> của biến?</li>
<li>Vì sao hàm cũng là một <b>giá trị</b>, và khi nào dùng hàm một dòng không tên?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, cách khai báo hàm, tham số đi vào, giá trị trả về đi ra. Hai, biến nằm ở đâu thì ai nhìn thấy, tức là phạm vi của biến. Ba, vì sao hàm cũng là một giá trị, và khi nào dùng hàm một dòng không tên."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: biến, phép tính và khối lệnh thụt lề", [
        st(repl_block(R_PRE, title="Tính thuế bằng tay, bằng biến")
           + "<p>Ta đã biết: biến là nhãn dán lên giá trị; <code>//</code> chia lấy phần nguyên; một khối lệnh là các dòng <b>thụt vào</b> sau dấu hai chấm. Công thức thuế $10\\%$ là <code>gia * 10 // 100</code>.</p>",
           """Biến là nhãn dán lên giá trị. Phép chia lấy phần nguyên cho ra số nguyên, hợp với tiền đồng. Và một khối lệnh là các dòng thụt vào sau dấu hai chấm. Với giá hai triệu, thuế mười phần trăm là hai trăm nghìn, cộng vào được hai triệu hai trăm nghìn."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã khai báo hàm, trả về, tham số mặc định, gọi có tên, hàm một dòng", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>def tên(a, b):</code>", "khai báo hàm", "đặt tên <code>tên</code> cho một khối lệnh; <code>a, b</code> là <b>tham số</b>: chỗ trống chờ giá trị"],
                  ["<code>return giá_trị</code>", "trả về", "kết thúc hàm và <b>đưa giá trị ra</b> cho nơi gọi; không có <code>return</code> thì hàm trả <code>None</code> (không có gì)"],
                  ["<code>tên(2000000, 8)</code>", "gọi hàm", "các giá trị trong ngoặc là <b>đối số</b>: điền vào tham số theo thứ tự"]]),
           """Bảng đầu là ba thứ cơ bản. Từ khoá khai báo hàm đặt tên cho một khối lệnh. Các tên trong ngoặc là tham số, tức chỗ trống chờ giá trị. Từ khoá trả về kết thúc hàm và đưa một giá trị ra cho nơi gọi. Không có nó thì hàm trả về một giá trị rỗng.
           Khi gọi hàm, các giá trị trong ngoặc gọi là đối số, và chúng điền vào tham số theo đúng thứ tự."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>def f(gia, ty_le=10):</code>", "tham số mặc định", "<code>ty_le=10</code>: nếu người gọi <b>không đưa</b> giá trị thì dùng <code>10</code>"],
                  ["<code>f(ty_le=8, gia=1000)</code>", "gọi có tên", "ghi <b>tên tham số</b> trước giá trị: thứ tự không còn quan trọng"],
                  ["<code>lambda g: g * 2</code>", "hàm một dòng không tên", "tương đương hàm có một lệnh trả về <code>g * 2</code>, nhưng <b>không đặt tên</b>"]]),
           """Bảng thứ hai là ba cách gọi và viết gọn. Tham số mặc định là giá trị dùng khi người gọi không đưa. Gọi có tên là ghi tên tham số trước giá trị, nên thứ tự không còn quan trọng. Và hàm một dòng không tên là cách viết gọn một hàm chỉ có đúng một lệnh trả về, mà không đặt tên.""",
           clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: hàm là cái máy; mỗi lần gọi có một hộp biến riêng", [
        st(svg(1500, 400,
               box(20, 60, 330, 120, ["gia = 2 000 000", "ty_le = 10"], C_BLUE, 26, True),
               txt(185, 40, "đối số đi vào", 24, "middle", "#2a78d6", True),
               arrow(355, 120, 480, 120, "#2a78d6"),
               box(485, 40, 480, 160, ["tong_tien(gia, ty_le)", "gọi tinh_vat → 200 000", "gia + 200 000"], C_AMBER, 26, True),
               arrow(970, 120, 1095, 120, "#16a34a"),
               box(1100, 60, 330, 120, ["return 2 200 000", "giá trị đi ra"], C_GREEN, 26, True),
               txt(750, 250, "hàm = tên + chỗ trống (tham số) + khối lệnh + giá trị trả về", 28, "middle", "#1f2937", True),
               txt(750, 300, "gọi một hàm từ trong hàm khác được: tong_tien gọi tinh_vat", 26, "middle", "#1f2937"),
               txt(750, 350, "giá trị đi ra là KẾT QUẢ để dùng tiếp; còn in ra màn hình chỉ là hiển thị", 26, "middle", "#dc2626")),
           """Hình này là cái máy. Các đối số đi vào, ở đây giá hai triệu và thuế suất mười. Khối lệnh bên trong làm việc, có thể gọi một hàm khác, ở đây gọi hàm tính thuế được hai trăm nghìn, rồi cộng với giá. Giá trị trả về đi ra, là hai triệu hai trăm nghìn.
           Hãy nhớ khác biệt này: giá trị trả về là kết quả để dùng tiếp, còn in ra màn hình chỉ là hiển thị."""),
        st(svg(1500, 400,
               panel(20, 20, 1040, 360, "bộ nhớ khi chương trình chạy", C_GRAY),
               box(60, 80, 440, 80, ["toàn cục: TY_LE = 10"], C_BLUE, 26, True),
               box(650, 80, 380, 250, ["", "", "", ""], C_AMBER),
               txt(840, 120, "hộp CỤC BỘ của lần gọi", 26, "middle", "#1f2937", True),
               txt(840, 175, "tong_tien(2 000 000)", 24, "middle", "#1f2937"),
               txt(840, 225, "gia = 2 000 000", 26, "middle", "#1f2937"),
               txt(840, 275, "phi_them = 200 000", 26, "middle", "#1f2937"),
               arrow(650, 120, 505, 120, "#2a78d6", "nhìn thấy"),
               txt(1290, 120, "trong hàm nhìn được hộp toàn cục", 24, "middle", "#16a34a", True),
               txt(1290, 170, "nhưng hộp cục bộ chỉ sống", 24, "middle", "#1f2937"),
               txt(1290, 205, "trong lúc hàm chạy", 24, "middle", "#1f2937"),
               txt(1290, 270, "hàm xong: hộp biến mất,", 26, "middle", "#dc2626", True),
               txt(1290, 310, "phi_them không còn", 26, "middle", "#dc2626", True)),
           """Hình thứ hai là phạm vi của biến. Biến đặt ngoài mọi hàm là toàn cục, hàm nào cũng nhìn thấy. Mỗi lần gọi hàm, máy dựng một hộp cục bộ chứa tham số và các biến gán bên trong. Hộp này nhìn được hộp toàn cục, nhưng chỉ sống trong lúc hàm chạy.
           Hàm xong, hộp biến mất, nên bên ngoài không còn nhìn thấy biến phí thêm nữa."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: gọi hàm, tham số mặc định, phạm vi, hàm là giá trị", [
        st(table(["bước", "việc máy làm", "giá trị"],
                 [["1", "gọi <code>tong_tien(2000000)</code>: dựng hộp, điền <code>gia</code>", "gia = 2 000 000, ty_le = 10 (mặc định)"],
                  ["2", "tính <code>tinh_vat(gia, ty_le)</code>: dựng hộp con", "2 000 000 * 10 // 100 = 200 000"],
                  ["3", "hộp con trả về, bị xoá; <code>tong_tien</code> tính <code>gia + 200000</code>", "2 200 000"],
                  ["4", "<code>return</code>: đưa ra, xoá hộp", "kết quả 2 200 000"]])
           + "<p>Vì <code>tong_tien</code> cần kết quả của <code>tinh_vat</code> nên máy làm xong hàm con trước, rồi mới quay lại cộng.</p>",
           """Bước một, chạy tay một lần gọi. Gọi hàm tổng tiền với giá hai triệu. Máy dựng một hộp, điền giá bằng hai triệu và thuế suất bằng mười theo mặc định. Vì hàm tổng tiền cần kết quả của hàm tính thuế, máy dựng thêm một hộp con, tính hai trăm nghìn, trả về và xoá hộp con.
           Rồi hàm tổng tiền cộng giá với hai trăm nghìn được hai triệu hai trăm nghìn, trả về và xoá hộp của nó."""),
        st(repl_block(R_DEFAULT, 0, 4, title="Bước 2. Tham số mặc định và gọi có tên (gõ hàm vào cửa sổ trước)")
           + "<p>Vì <code>ty_le</code> có mặc định nên bỏ qua được. Gọi theo vị trí <code>(2000000, 8)</code> và gọi có tên <code>(ty_le=8, gia=2000000)</code> cho cùng kết quả: $2\\,000\\,000 + 160\\,000 = 2\\,160\\,000$.</p>"
           + "<p class='note'>Dòng bắt đầu bằng <code>...</code> là <b>dấu nhắc nối</b>: máy chờ thêm các dòng thụt vào của hàm. Bấm Enter thêm một lần (dòng trống) để báo hàm đã xong.</p>",
           """Bước hai, tham số mặc định và gọi có tên. Ta gõ hàm vào cửa sổ gõ từng câu trước, rồi mới gọi. Dòng bắt đầu bằng ba dấu chấm là dấu nhắc nối, máy đang chờ các dòng thụt vào của hàm. Ta bấm xuống dòng thêm một lần trống để báo hàm đã xong. Vì thuế suất có giá trị mặc định mười, ta gọi chỉ với giá và được hai triệu hai trăm nghìn. Đưa thêm số tám thì thuế suất là tám phần trăm, được hai triệu một trăm sáu mươi nghìn. Gọi có tên với thứ tự đảo cho đúng kết quả đó.
           Làm thử bằng tay: tám phần trăm của hai triệu là một trăm sáu mươi nghìn.""", clear=True),
        st(run_block(P_SCOPE, title="Bước 3. Phạm vi: biến cục bộ không nhìn thấy từ ngoài")
           + "<p>Trong hàm <code>TY_LE</code> (toàn cục) <b>đọc</b> được; ngoài hàm, <code>phi_them</code> (cục bộ) không còn: <b>dòng cuối</b> báo tên chưa được định nghĩa.</p>",
           """Bước ba, phạm vi. Hàm đọc được biến toàn cục thuế suất, nên in ra hai triệu hai trăm nghìn. Nhưng biến phí thêm chỉ có trong hộp cục bộ của hàm. Hàm xong thì hộp biến mất, nên dòng in cuối báo lỗi, tên chưa được định nghĩa. Đọc dòng cuối là biết ngay lỗi gì.""",
           clear=True),
        st(repl_block(R_FUNCVAL, title="Bước 4. Hàm cũng là một giá trị")
           + "<p>Vì tên hàm cũng chỉ là <b>nhãn dán</b> lên một giá trị kiểu hàm, ta dán thêm nhãn <code>f</code> lên nó và gọi qua nhãn mới; <code>lambda</code> tạo hàm mà chưa dán nhãn nào.</p>",
           """Bước bốn, hàm cũng là một giá trị. Ta khai báo hàm tăng thêm một, gọi nó được sáu, rồi hỏi kiểu của nó là kiểu hàm, vì tên hàm chỉ là nhãn dán lên một giá trị, giống mọi biến khác. Ta dán thêm nhãn f lên hàm tăng, và gọi qua nhãn mới vẫn cho sáu. Hàm một dòng không tên tạo ra một hàm mà chưa dán nhãn nào, và ta có thể gọi nó ngay.""",
           clear=True),
    ], checks=["2000000 * 10 // 100 == 200000 and 2000000 + 200000 == 2200000", "2000000 * 8 // 100 == 160000 and 2000000 + 160000 == 2160000"])
    sc_ex = sc("example", "example", "Ví dụ: hai hàm thuế, rồi truyền hàm cho hàm khác", [
        st(run_block(P_HAM, title="Tệp ham.py"),
           """Ta ráp lại thành một tệp, trong đó hàm tính thuế nhận giá và thuế suất mặc định mười. Hàm tổng tiền gọi hàm tính thuế. Ba dòng cuối gọi hàm với các đối số khác nhau. Máy in thuế hai trăm nghìn, tổng hai triệu hai trăm nghìn, và tổng với thuế tám phần trăm là hai triệu một trăm sáu mươi nghìn."""),
        st(run_block(P_LAMBDA, title="Hàm nhận hàm: ap_dung(ham, x)")
           + "<p>Hàm <code>ap_dung</code> nhận <b>một hàm</b> làm tham số và gọi nó. Đưa <code>them_vat</code> (có tên) hay <code>lambda</code> (không tên) đều được.</p>",
           """Vì hàm là giá trị, ta truyền nó cho hàm khác. Hàm áp dụng nhận một hàm và một giá trị, rồi gọi hàm đó với giá trị. Ta đưa vào hàm thêm thuế có tên, được hai triệu hai trăm nghìn. Rồi đưa vào một hàm một dòng không tên với thuế tám phần trăm, được hai triệu một trăm sáu mươi nghìn.
           Cách này cho phép đổi quy tắc tính mà không sửa hàm áp dụng.""", clear=True),
        st(table(["viết trong mã", "đọc là", "nghĩa"],
                 [["<code>import time</code>", "nạp thư viện thời gian", "mang thư viện <code>time</code> vào chương trình"],
                  ["<code>time.perf_counter()</code>", "đọc đồng hồ", "dấu chấm đọc là “của”: hàm <code>perf_counter</code> <b>của</b> thư viện <code>time</code>; hiệu hai lần đọc là số giây"],
                  ["<code>for i in range(n): …</code>", "lặp n lượt", "<code>i</code> đếm từ $0$ tới $n - 1$"]]),
           """Ta còn cần đo một việc mất bao lâu. Dòng nạp mang thư viện thời gian vào chương trình. Dấu chấm giữa hai tên đọc là của: hàm đồng hồ chính xác cao nằm trong thư viện đó, và hiệu hai lần đọc là số giây đã trôi. Vòng lặp nhiều lượt có biến đếm từ không.""", clear=True, introduces=["pyt_perf_counter"]),
        st(raw_block(DEMO_DO.split("\n"), title="Đo một việc mất bao lâu: đọc đồng hồ trước và sau", py_hl=True)
           + f'<div class="code"><div>{round(giay_demo, 2)} giay</div></div>',
           """Ta hỏi đồng hồ ngay trước và ngay sau việc cần đo, rồi làm tròn hiệu hai lần đọc tới hai chữ số sau dấu phẩy. Việc đo là vòng lặp một triệu lượt, mỗi lượt gọi hàm tăng thêm một.""", clear=True),
        st("<div class='box key'><code>time.perf_counter()</code> trả số giây của một đồng hồ chính xác cao; <b>hiệu hai lần đọc</b> là thời gian chạy. Số in ra mỗi máy, mỗi lần một khác (số minh hoạ); đo nhiều lần và lấy lần <b>nhanh nhất</b>.</div>"
           + repl_block(R_MIN, title="Lần nhanh nhất = số nhỏ nhất: <code>min</code>")
           + "<p><code>min(a, b, c)</code> trả về số <b>nhỏ nhất</b> trong các số đưa vào; thời gian ngắn nhất là lần nhanh nhất.</p>",
           """Số giây in ra mỗi máy một khác, và mỗi lần chạy cũng lệch một chút vì máy còn việc khác chen vào. Vì vậy người làm nghề chạy nhiều lần rồi lấy lần nhanh nhất.
           Lần nhanh nhất là lần có thời gian ngắn nhất, và lệnh tìm số nhỏ nhất nhận vài số rồi trả về số nhỏ nhất trong chúng.""", clear=True),
    ], checks=["2000000 * 110 // 100 == 2200000 and 2000000 * 108 // 100 == 2160000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: gọi hàm khớp với tính tay, và với công thức gộp", [
        st(repl_block(R_QUIZ, 0, 2, title="Hàm lồng nhau cho kết quả như tính tay")
           + "<p>Hàm $gap(x) = 2x$. Gọi hai lần: $gap(gap(3)) = gap(6) = 12$, trùng $3 \\cdot 2 \\cdot 2 = 12$ ✓</p>",
           """Đường kiểm khác, so hàm với tính tay. Một hàm nhân đôi, gọi hai lần lồng nhau với số ba. Gọi trong trước được sáu, gọi ngoài được mười hai. Tính tay, ba nhân hai nhân hai cũng bằng mười hai. Hai cách khớp nhau, nên ta tin hàm hơn, dù một lần thử chưa phải là chứng minh."""),
        st(repl_block(R_QUIZ, 2, 3, title="Và hai lần gọi độc lập") + "<p>$gap(3) + gap(4) = 6 + 8 = 14 = gap(3 + 4)$: hàm này <b>giữ phép cộng</b>, nên hai cách tính khớp.</p>",
           """Phép thử thứ hai, hai lần gọi độc lập. Nhân đôi ba cộng nhân đôi bốn là sáu cộng tám, bằng mười bốn, cũng bằng nhân đôi của bảy. Với hàm nhân đôi thì hai cách tính khớp, vì phép nhân đôi giữ nguyên phép cộng.""", clear=True),
    ], checks=["2 * (2 * 3) == 12 and 3 * 2 * 2 == 12", "2 * 3 + 2 * 4 == 14 == 2 * (3 + 4)"])
    sc_scale = sc("scale", "concept", "Khi hệ thống lớn dần: sửa một chỗ thay vì N chỗ, và cái giá của một lần gọi", [
        st(table(["số nơi dùng công thức", "chép tay: số chỗ phải sửa", "hàm: số chỗ phải sửa", "khả năng bỏ sót ≥ 1 chỗ nếu mỗi chỗ quên 2% (số minh hoạ)"],
                 [["×1: 1", "1", "1", f"{round(100 * (1 - 0.98 ** 1), 1)}%".replace(".", ",")],
                  ["×10: 10", "10", "1", f"{round(100 * (1 - 0.98 ** 10), 1)}%".replace(".", ",")],
                  ["×100: 100", "100", "1", f"{round(100 * (1 - 0.98 ** 100), 1)}%".replace(".", ",")]]),
           """Bảng này nói về quy mô bảo trì. Công thức dùng ở một nơi thì sửa một chỗ. Dùng ở mười nơi, nếu chép tay thì phải sửa mười chỗ, và nếu mỗi chỗ có hai phần trăm khả năng quên, khả năng bỏ sót ít nhất một chỗ là mười tám phẩy ba phần trăm. Dùng ở một trăm nơi, khả năng đó lên tới tám mươi sáu phẩy bảy phần trăm.
           Với hàm, mọi quy mô đều chỉ sửa một chỗ."""),
        st(code_block(P_HAI, lines=(1, 12), title="Hai cách viết đem so: gọi hàm ở mỗi vòng, và viết thẳng phép cộng"),
           """Để so hai cách viết, ta dùng hai hàm có cùng một việc. Hàm thứ nhất ở mỗi vòng gọi hàm tăng thêm một. Hàm thứ hai ở mỗi vòng viết thẳng phép cộng một, không gọi hàm nào.""", clear=True),
        st(table(["số lần chạy", "gọi qua hàm (ms = phần nghìn giây, s = giây)", "viết thẳng, không hàm"],
                 [["×1 000 000: 10<sup>6</sup>", sc6[0], si6[0]], ["×10 000 000: 10<sup>7</sup>", sc7[0], si7[0]],
                  ["ngoại suy: 10<sup>9</sup>", sc9[0] + " (tuyến tính)", "—"]])
           + "<p class='note'><b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo để đoán quy mô lớn hơn (ước lượng, chưa đo).</p>"
           + f"<div class='box key'><b>Đánh đổi:</b> mỗi lần gọi hàm tốn thêm một khoản nhỏ: đo trên máy kiểm (Python 3.11, vòng lặp nằm trong một hàm, hàm chỉ có một phép cộng, lấy lần nhanh nhất của 3 lần), gọi hàm chậm hơn cỡ {str(lo_r).replace('.', ',')} đến {str(hi_r).replace('.', ',')} lần (ở $10^6$ và $10^7$ lần gọi). "
             "Hàm này chỉ có một phép cộng nên khoản gọi chiếm phần lớn; hàm làm việc thật thì khoản gọi chỉ là phần nhỏ trong việc nó làm. Hầu hết chương trình đáng đổi khoản đó lấy sự rõ ràng; chỉ ở vòng lặp nóng chạy hàng trăm triệu lần mới đo rồi mới tối ưu (số minh hoạ, máy bạn khác).</div>",
           f"""Còn cái giá của một lần gọi hàm. Trên máy kiểm, với vòng lặp nằm trong một hàm, mười triệu lần gọi hàm mất {sc7[1]}, còn viết thẳng phép cộng mất {si7[1]}. Hàm chậm hơn cỡ {vi_num(lo_r)} đến {vi_num(hi_r)} lần. Hàm này chỉ có một phép cộng nên khoản gọi chiếm phần lớn, còn hàm làm việc thật thì khoản gọi chỉ là phần nhỏ. Ngoại suy, tức nhân theo tỉ lệ từ số đã đo, một tỉ lần gọi mất {sc9[1]}.
           Đánh đổi là gọi hàm tốn thêm một khoản nhỏ, nhưng hầu hết chương trình nên đổi khoản đó lấy sự rõ ràng. Chỉ ở vòng lặp nóng, chạy hàng trăm triệu lần, mới cần đo rồi mới tối ưu. Số minh hoạ, máy bạn sẽ khác.""", clear=True),
    ], checks=["round(100 * (1 - 0.98 ** 10), 1) == 18.3 and round(100 * (1 - 0.98 ** 100), 1) == 86.7", "10 ** 9 // 10 ** 7 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> In ra màn hình nhưng quên <code>return</code>.</div>'
           + run_block(P_NORET)
           + "<p>Màn hình hiện $200\\,000$ nên tưởng đúng, nhưng giá trị trả về là <code>None</code>: không dùng tiếp được. Phép thử: in <b>kết quả đã gán</b>, như dòng cuối.</p>",
           """Lỗi thứ nhất, của người mới, là chỉ in mà quên trả về. Màn hình hiện hai trăm nghìn nên tưởng đúng. Nhưng giá trị trả về của hàm là rỗng, và biến kết quả nhận giá trị rỗng. Mọi phép tính sau đó sẽ hỏng. Phép thử bắt được lỗi là in chính biến kết quả."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Gán vào biến trùng tên với biến toàn cục: máy coi là biến cục bộ mới.</div>'
           + run_block(P_UNB)
           + "<p>Trong hàm có <code>tong = …</code> nên <code>tong</code> là <b>cục bộ</b>; vế phải đọc nó trước khi nó có giá trị. Sửa: nhận và trả về giá trị, <b>không</b> sửa biến ngoài.</p>",
           """Lỗi thứ hai, của người mới, là gán vào biến trùng tên với biến toàn cục. Khi trong hàm có phép gán, máy coi biến đó là cục bộ. Vế phải lại đọc biến này trước khi nó có giá trị, nên máy báo lỗi. Cách sửa tốt là cho hàm nhận giá trị và trả về giá trị, thay vì sửa biến bên ngoài.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đổi chỗ hai đối số cùng kiểu: máy không báo lỗi.</div>'
           + run_block(P_SWAP)
           + "<p>Cả hai đều là số nguyên nên hợp lệ; kết quả $0$ nghe có vẻ hợp lý. Phép thử: <b>gọi có tên</b> cho các tham số cùng kiểu, như dòng cuối.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là đổi chỗ hai đối số cùng kiểu. Chia đều hai triệu cho bốn người cho năm trăm nghìn. Đổi chỗ hai số vẫn là hai số nguyên hợp lệ, máy không báo lỗi và trả về không. Con số không dễ lọt vào báo cáo.
           Cách phòng là gọi có tên với các tham số cùng kiểu, vì tên nói rõ số nào là gì.""", clear=True),
    ], checks=["2000000 // 4 == 500000 and 4 // 2000000 == 0"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Cho <code>def gap(x): return x * 2</code>.</p>
<ol><li><code>gap(gap(3))</code> bằng bao nhiêu?</li>
<li>Hàm <code>def hai(x): print(x * 2)</code> khác hàm trên ở điểm nào khi viết <code>y = hai(3) + 1</code>?</li></ol>
<p><b>Quyết định:</b> thuế suất đổi theo từng tháng: truyền thuế suất làm <b>tham số</b> hay đặt làm <b>biến toàn cục</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Cho một hàm nhân đôi. Câu một, gọi hàm hai lần lồng nhau với số ba bằng bao nhiêu. Câu hai, một hàm khác chỉ in mà không trả về, thì khác gì khi ta cộng thêm một vào kết quả của nó.
           Sau đó là một quyết định, thuế suất đổi theo từng tháng, nên truyền làm tham số hay đặt làm biến toàn cục, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_QUIZ, 0, 2, title="Câu 1") + "<p>Gọi trong: $gap(3) = 6$; gọi ngoài: $gap(6) = 12$.</p>",
           """Đáp án câu một. Gọi trong cho sáu, gọi ngoài với sáu cho mười hai."""),
        st("<p><b>Câu 2.</b> Hàm chỉ in trả về <code>None</code>; <code>None + 1</code> không cộng được, máy báo lỗi kiểu. Hàm có <code>return</code> trả về số, cộng được.</p>",
           """Đáp án câu hai. Hàm chỉ in trả về giá trị rỗng, và cộng một vào giá trị rỗng không được, máy báo lỗi. Hàm có trả về thì cho ra một số, cộng được.""", clear=True),
        st("<div class='box key'><b>Quyết định:</b> truyền làm <b>tham số</b>. Hàm chỉ phụ thuộc vào thứ nó nhận, nên thử được với mọi thuế suất và ai đọc cũng thấy "
           "dữ liệu vào từ đâu. Biến toàn cục là đầu vào <b>ẩn</b>: đổi nó ở một nơi làm kết quả hàm đổi ở mọi nơi, rất khó lần ra.</div>",
           """Còn quyết định cuối thì thế này. Nên truyền thuế suất làm tham số. Khi đó hàm chỉ phụ thuộc vào thứ nó nhận, thử được với mọi thuế suất, và người đọc thấy dữ liệu vào từ đâu. Biến toàn cục là đầu vào ẩn, đổi nó ở một nơi làm kết quả của hàm đổi ở mọi nơi, rất khó lần ra.""", clear=True),
    ], checks=["(lambda g: g(g(3)))(lambda x: x * 2) == 12"])
    sc_prac = practice_scene(sc, "Tự làm: ba hàm phí và thuế, và hàm nhận hàm", pr_steps(
        st, "PYT", "L02",
        """<p><b>Đề</b>: tạo <code>phi_thue.py</code> gồm ba hàm (số nguyên đồng, chia lấy phần nguyên):</p>
<ol><li><code>phi_rut(tien)</code>: trả <code>1100</code> nếu <code>tien &lt; 2000000</code>, ngược lại <code>tien * 5 // 10000</code>;</li>
<li><code>vat(phi, ty_le=10)</code>: <code>phi * ty_le // 100</code>;</li>
<li><code>tong_chi(tien, ham_phi)</code>: gọi <code>ham_phi(tien)</code> được phí, trả <code>phi + vat(phi)</code>.</li></ol>
<p>Rồi in (xem <code>de.md</code>) ba dòng cho <code>[500000, 3000000, 80000000]</code> dạng <code>tien phi tong</code>, và một dòng <code>tong_chi(3000000, lambda t: t // 1000)</code>.</p>
<p><b>Đo</b>: với <code>time.perf_counter</code>, chạy <code>vat(1100)</code> một triệu lần, rồi chạy <code>phi * 10 // 100</code> một triệu lần (<code>phi = 1100</code>); mỗi cách lấy lần nhanh nhất trong ba lần. Dòng cuối: <code>Goi ham cham hon viet thang: CO</code> nếu gọi hàm chậm hơn.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết ba hàm. Hàm phí rút trả một nghìn một trăm nếu tiền dưới hai triệu, còn lại là năm phần mười nghìn của số tiền. Hàm thuế giá trị gia tăng nhận phí và thuế suất mặc định mười. Hàm tổng chi nhận số tiền và một hàm tính phí, trả về phí cộng thuế.
        Rồi in ba dòng cho ba số tiền cho sẵn, và một dòng truyền vào hàm một dòng không tên. Cuối cùng, tự đo hai cách. Gọi hàm thuế một triệu lần, rồi viết thẳng công thức thuế một triệu lần, mỗi cách lấy lần nhanh nhất trong ba lần, và in có phải gọi hàm chậm hơn không. Hãy dừng video và làm.""",
        LAB_OUT, "phi_thue.py",
        """<div class="box key"><b>Nếu kẹt:</b> mỗi hàm một khối <code>def</code> có <code>return</code>. <code>tong_chi</code> không biết <code>phi_rut</code>: nó chỉ gọi <code>ham_phi(tien)</code>. Khi truyền hàm, viết <b>tên không có ngoặc</b>: <code>tong_chi(tien, phi_rut)</code>.
Đo ba lần lấy nhanh nhất: <code>min(mot_lan(f), mot_lan(f), mot_lan(f))</code>, với <code>mot_lan(f)</code> trả hiệu hai lần đọc đồng hồ quanh <code>f()</code>.
Lời giải ở <code>labs/PYT/L02/loi_giai.py</code>.</div>""",
        """Nếu kẹt, mỗi hàm là một khối khai báo có trả về. Hàm tổng chi không biết hàm phí rút, nó chỉ gọi hàm được truyền vào. Khi truyền hàm, viết tên mà không có ngoặc, vì có ngoặc là gọi nó ngay. Để lấy lần nhanh nhất trong ba lần, gọi một hàm đo ba lần rồi đưa ba kết quả cho lệnh tìm số nhỏ nhất.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L02")
    write_lab("PYT", "L02", """# Lab PYT L02 — Phí rút, thuế và hàm nhận hàm

Cần: Python 3.11 trở lên. Tạo `phi_thue.py` với ba hàm (số nguyên đồng; số liệu minh hoạ, khác ví dụ trong bài):

1. `phi_rut(tien)`: trả `1100` nếu `tien < 2000000`; ngược lại trả `tien * 5 // 10000`.
2. `vat(phi, ty_le=10)`: trả `phi * ty_le // 100`.
3. `tong_chi(tien, ham_phi)`: tính `phi = ham_phi(tien)`, trả `phi + vat(phi)`.

Rồi in:
- với mỗi `tien` trong `[500000, 3000000, 80000000]` một dòng `tien phi tong` (`phi` = `phi_rut(tien)`, `tong` = `tong_chi(tien, phi_rut)`);
- một dòng: `tong_chi(3000000, lambda t: t // 1000)`.
- **đo** (lab chấm *hình dạng* kết quả, không chấm số giây tuyệt đối vì mỗi máy một khác): với `import time`, viết hai hàm không đối số, một hàm gọi `vat(1100)` một triệu lần trong vòng lặp, một hàm tính `phi * 10 // 100` (`phi = 1100`) một triệu lần trong vòng lặp. Mỗi hàm chạy ba lần, lấy thời gian ngắn nhất (hiệu hai lần đọc `time.perf_counter()` quanh lần chạy; lấy số nhỏ nhất của ba số bằng `min(a, b, c)`, hoặc vòng `for` ba lần cập nhật `nhanh = min(nhanh, lan_nay)`). In dòng cuối `Goi ham cham hon viet thang: CO` nếu thời gian của hàm gọi `vat` lớn hơn, ngược lại `KHONG`.

Chạy: `python phi_thue.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L02 phi_thue.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("hàm = tên + tham số + khối lệnh + trả về", "không trả về thì được None", "mặc định và gọi có tên chống nhầm thứ tự",
                 "biến cục bộ sống trong một lần gọi", "hàm cũng là giá trị: truyền được, lambda", "viết một lần, sửa một chỗ"),
           """Tổng kết chuỗi logic. Hàm gồm tên, tham số, khối lệnh và giá trị trả về. Không trả về thì hàm cho giá trị rỗng. Tham số mặc định và gọi có tên giúp tránh nhầm thứ tự. Biến cục bộ chỉ sống trong một lần gọi.
           Hàm cũng là giá trị, nên truyền được và có thể viết gọn không tên. Và viết một lần thì sửa một chỗ."""),
        st("""<div class='box key'><b>Tư duy:</b> một hàm tốt làm <b>một việc</b>, nhận mọi thứ qua tham số và đưa kết quả qua <code>return</code>; không đọc hay sửa biến ẩn bên ngoài.</div>
<p>Bài sau: danh sách, từ điển và tập hợp, những cách xếp nhiều giá trị lại để tìm và đếm nhanh.</p>""",
           """Điều cần mang theo, một hàm tốt làm một việc, nhận mọi thứ qua tham số và đưa kết quả qua giá trị trả về, không đọc hay sửa biến ẩn bên ngoài.
           Bài sau, ta học danh sách, từ điển và tập hợp, những cách xếp nhiều giá trị lại để tìm và đếm nhanh.""", forward_ref=True),
    ])
    return lesson("L02", "ham", "Bài 2 — Hàm: gói một việc, đặt tên, dùng lại",
                  "curriculum/pyt.yaml L02; audit/pyt/verify_pyt.py L02 (chạy thật trên Python 3.11 và 3.13); Python Tutorial §4.8–4.9 (Defining Functions: default values, keyword arguments, lambda), "
                  "Language Reference §4.2 (Naming and binding: scopes), FAQ 'Why am I getting an UnboundLocalError'; chi phí một lần gọi hàm đo bằng verify_pyt (máy kiểm, đo trong một hàm, lấy lần nhanh nhất của 3 lần; số minh hoạ; ngoại suy 10^9 tuyến tính); Library Reference time.perf_counter; "
                  "xác suất bỏ sót 2% mỗi chỗ là giả định minh hoạ",
                  ["Viết hàm có tham số, giá trị trả về và hàm gọi hàm khác",
                   "Dùng tham số mặc định và gọi có tên",
                   "Xác định phạm vi của biến: toàn cục đọc được trong hàm, cục bộ chỉ sống trong một lần gọi",
                   "Truyền một hàm cho hàm khác và viết hàm một dòng không tên",
                   "Kiểm một hàm bằng tính tay và bằng cách gọi lồng nhau",
                   "Nêu vì sao hàm giảm số chỗ phải sửa và cái giá của một lần gọi ở ba quy mô",
                   "Chỉ ra ba lỗi hay gặp: quên trả về, gán trùng tên biến toàn cục, đổi chỗ đối số cùng kiểu",
                   "Viết ba hàm phí và thuế cùng hàm nhận hàm",
                   "Đo thời gian chạy của một đoạn mã bằng đồng hồ time.perf_counter và so hai cách viết"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy"],
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "example"), (5, "check"), (6, "scale"), (7, "pitfalls"), (8, "practice"), (9, "example")])
