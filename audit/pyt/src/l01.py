from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_a import t2

R_SS = repl("SoSanh", [("tien = 7500000", ""), ("tien < 1000000", "False"), ("tien >= 1000000", "True"), ("tien == 7500000", "True"), ("tien != 7500000", "False")])
R_LOGIC = repl("Logic", [
    ("tien = 7500000", ""), ("tien >= 1000000 and tien < 20000000", "True"), ("tien < 1000000 or tien >= 20000000", "False"),
    ("not (tien < 1000000)", "True"), ("1000000 <= tien < 20000000", "True"),
])
R_RANGE = repl("Range", [("list(range(3))", "[0, 1, 2]"), ("list(range(1, 4))", "[1, 2, 3]"), ("list(range(2, 9, 3))", "[2, 5, 8]")])
R_OR = repl("OrSai", [
    ('loai = "nap"', ""), ('loai == "rut" or "chuyen"', "'chuyen'"), ('loai == "rut" or loai == "chuyen"', "False"),
    ('loai in ("rut", "chuyen")', "False"),
])
P_Q1 = py("quiz_lap", '''for i in range(3):
    print(i * 10)''', "0\n10\n20")

P_PL = py("phan_loai", '''tien = 7500000
if tien < 1000000:
    muc = "nho"
elif tien < 20000000:
    muc = "vua"
else:
    muc = "lon"
print("Giao dich", tien, "thuoc muc", muc)''', "Giao dich 7500000 thuoc muc vua")
P_DAO = py("phan_loai_dao", '''tien = 500000
if tien < 20000000:
    muc = "vua"
elif tien < 1000000:
    muc = "nho"
else:
    muc = "lon"
print("Giao dich", tien, "thuoc muc", muc)''', "Giao dich 500000 thuoc muc vua")
P_TONG = py("tong", '''giao_dich = [450000, 12000000, 800000, 30000000, 2500000]
tong = 0
dem_lon = 0
for tien in giao_dich:
    tong = tong + tien
    if tien >= 20000000:
        dem_lon = dem_lon + 1
print("Tong:", tong)
print("So giao dich lon:", dem_lon)''', "Tong: 45750000\nSo giao dich lon: 1")
P_RANGE = py("dem_range", '''for thang in range(1, 4):
    print("Thang", thang)''', "Thang 1\nThang 2\nThang 3")
P_WHILE = py("gap_doi", '''so_du = 10000000
thang = 0
while so_du < 20000000:
    so_du = so_du + so_du * 5 // 1000
    thang = thang + 1
print("So thang de gap doi:", thang)''', "So thang de gap doi: 139")
P_BRK = py("dung_som", '''giao_dich = [450000, 12000000, 800000, 30000000, 2500000]
for tien in giao_dich:
    if tien < 1000000:
        continue
    if tien >= 20000000:
        print("Dung o giao dich", tien)
        break
    print("Xet", tien)''', "Xet 12000000\nDung o giao dich 30000000")
P_THUT = py("loi_thut", '''tien = 500000
if tien > 100000:
print("lon")''', "", expect="error:IndentationError", err='File "…", line 3\nIndentationError: expected an indented block after \'if\' statement on line 2')
P_LECH = py("lech_mot", '''tong = 0
for i in range(1, 5):
    tong = tong + i
print("Tong 1..5 =", tong)''', "Tong 1..5 = 10")
P_VOHAN = py("vo_han", '''so_du = 10000000
buoc = 0
while so_du < 20000000 and buoc < 5:
    buoc = buoc + 1
print("Sau", buoc, "buoc, so_du van la", so_du)''', "Sau 5 buoc, so_du van la 10000000")
P_N = py("tong_n", '''n = 1000000
tong = 0
for i in range(1, n + 1):
    tong = tong + i
print("Tong 1 den", n, "=", tong)''', "Tong 1 den 1000000 = 500000500000")
measure("l01_loop", '''import json, time
res = {}
for k, n in (("1e3", 1000), ("1e6", 1000000), ("1e7", 10000000)):
    t0 = time.perf_counter()
    tong = 0
    for i in range(1, n + 1):
        tong = tong + i
    res["t_loop_" + k] = time.perf_counter() - t0
    assert tong == n * (n + 1) // 2
print(json.dumps(res))''')

LAB_SOL = '''giao_dich = [250000, 3200000, 75000000, 1800000, 64000000, 900000, 5000000, 120000]
tong = 0
dem_nho = 0
dem_vua = 0
dem_lon = 0
for tien in giao_dich:
    tong = tong + tien
    if tien < 2000000:
        muc = "nho"
        dem_nho = dem_nho + 1
    elif tien < 60000000:
        muc = "vua"
        dem_vua = dem_vua + 1
    else:
        muc = "lon"
        dem_lon = dem_lon + 1
    print(tien, muc)
print("Tong:", tong)
print("Nho, vua, lon:", dem_nho, dem_vua, dem_lon)'''
LAB_OUT = """250000 nho
3200000 vua
75000000 lon
1800000 nho
64000000 lon
900000 nho
5000000 vua
120000 nho
Tong: 150270000
Nho, vua, lon: 4 2 2"""
P_LAB = py("lab_l01", LAB_SOL, LAB_OUT)


def gl(t):
    """Chú đơn vị ngay trong ô: '≈ 93 µs' -> '≈ 93 µs (phần triệu giây)'."""
    for u, g in (("µs", "phần triệu giây"), ("ms", "phần nghìn giây")):
        if t.endswith(" " + u):
            return t + f" ({g})"
    return t


def build():
    t3, t6, t7 = M("l01_loop", "t_loop_1e3"), M("l01_loop", "t_loop_1e6"), M("l01_loop", "t_loop_1e7")
    s3, s6, s7 = t2(t3), t2(t6), t2(t7)
    t9 = t7 * 100          # ngoại suy tuyến tính: mười mũ chín lần lặp = 100 × mười mũ bảy
    s9 = t2(t9)
    sc_hook = sc("hook", "hook", "Một triệu giao dịch, mỗi giao dịch phải được phân loại", [
        st(code_block(P_PL, title="Một giao dịch: chương trình tự chọn nhánh (print(a, b, …) in các giá trị cách nhau một dấu cách)") + out_block(P_PL),
           """Một hệ thống thanh toán nhận hàng triệu giao dịch mỗi ngày, và với mỗi giao dịch nó phải quyết định xử lý thế nào. Giao dịch nhỏ thì cho qua, giao dịch lớn thì cần kiểm tra thêm.
           Không ai ngồi quyết định từng cái. Chương trình ở đây tự chọn một trong ba nhánh theo số tiền, và giao dịch bảy triệu rưỡi rơi vào mức vừa. Lệnh in nhận nhiều giá trị cách nhau dấu phẩy và in chúng cách nhau một dấu cách."""),
        st(code_block(P_TONG, title="Và tự lặp lại việc đó cho cả danh sách") + out_block(P_TONG),
           """Chuyện thứ hai là lặp lại. Viết một lần, máy làm một triệu lần. Chương trình này đi qua năm giao dịch, cộng dồn tổng tiền và đếm số giao dịch lớn. Máy in ra tổng bốn mươi lăm triệu bảy trăm năm mươi nghìn đồng, và có một giao dịch lớn."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Chương trình <b>chọn nhánh</b> theo điều kiện bằng cách nào?</li>
<li>Cách <b>lặp lại</b> một việc, và khi nào chọn vòng lặp đếm hay vòng lặp điều kiện?</li>
<li>Vì sao <b>thụt lề</b> quan trọng, và số lần lặp thay đổi thế nào khi dữ liệu lớn lên?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, chương trình chọn nhánh theo điều kiện bằng cách nào. Hai, cách lặp lại một việc, và khi nào chọn vòng lặp đếm hay vòng lặp điều kiện.
           Ba, vì sao thụt lề quan trọng, và số lần lặp thay đổi thế nào khi dữ liệu lớn lên."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: biến, kiểu, và phép so sánh cho ra đúng hoặc sai", [
        st(repl_block(R_SS, title="Phép so sánh cho ra giá trị đúng hoặc sai")
           + "<p>Biến <code>tien</code> là nhãn dán lên số nguyên <code>7500000</code>. Một phép so sánh luôn trả về <b>đúng</b> (<code>True</code>) hoặc <b>sai</b> (<code>False</code>), kiểu đúng–sai của bài trước.</p>",
           """Ta ôn lại hai điều từ bài trước. Biến là một cái nhãn dán lên giá trị, ở đây nhãn tiền dán lên bảy triệu rưỡi. Và một phép so sánh luôn cho ra giá trị đúng hoặc sai, chính là kiểu đúng sai ta đã học.
           Hỏi bảy triệu rưỡi có nhỏ hơn một triệu không, máy trả lời sai. Có lớn hơn hoặc bằng không, máy trả lời đúng."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã sáu phép so sánh, ba từ nối, hai chấm và thụt lề", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>a == b</code>, <code>a != b</code>", "bằng, khác", "hai dấu <code>=</code> hỏi “bằng nhau?”; <code>!=</code> hỏi “khác nhau?”"],
                  ["<code>a &lt; b</code>, <code>a &lt;= b</code>", "nhỏ hơn, nhỏ hơn hoặc bằng", "<code>&lt;=</code> gồm cả trường hợp bằng"],
                  ["<code>a &gt; b</code>, <code>a &gt;= b</code>", "lớn hơn, lớn hơn hoặc bằng", "<code>&gt;=</code> gồm cả trường hợp bằng"]]),
           """Bảng đầu là sáu phép so sánh. Hai dấu bằng hỏi hai bên có bằng nhau không, còn dấu chấm than và một dấu bằng hỏi có khác nhau không. Nhỏ hơn và nhỏ hơn hoặc bằng khác nhau ở chỗ trường hợp bằng nhau.
           Lớn hơn và lớn hơn hoặc bằng cũng vậy. Mọi phép so sánh đều cho ra đúng hoặc sai."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>A and B</code>", "và", "đúng khi <b>cả hai</b> cùng đúng"],
                  ["<code>A or B</code>", "hoặc", "đúng khi <b>ít nhất một</b> bên đúng"],
                  ["<code>not A</code>", "không phải", "đảo đúng thành sai và ngược lại"]]),
           """Bảng thứ hai là ba từ nối điều kiện. Từ và cho kết quả đúng khi cả hai vế cùng đúng. Từ hoặc cho kết quả đúng khi ít nhất một vế đúng. Từ phủ định đảo đúng thành sai và sai thành đúng.""", clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>if điều_kiện:</code>", "câu lệnh rẽ nhánh", "chạy khối bên dưới <b>chỉ khi</b> điều kiện đúng; <code>elif</code> = “nếu không thì, nếu”; <code>else</code> = “còn lại”"],
                  ["<code>:</code> và <b>thụt lề</b>", "dấu hai chấm, bốn dấu cách", "dòng kết thúc bằng <code>:</code> mở một <b>khối lệnh</b>; các dòng <b>thụt vào</b> cùng độ sâu là một khối"],
                  ["<code>for x in …:</code>", "vòng lặp đếm", "lặp khối bên dưới, mỗi lượt <code>x</code> nhận <b>một giá trị kế tiếp</b>; <code>in</code> = “nằm trong”"],
                  ["<code>while điều_kiện:</code>", "vòng lặp điều kiện", "lặp khối bên dưới <b>chừng nào</b> điều kiện còn đúng"]]),
           """Bảng thứ ba là bộ khung của chương trình. Câu lệnh rẽ nhánh chạy khối bên dưới chỉ khi điều kiện đúng, từ khoá nếu-không-thì-nếu là nhánh kiểm tra thêm, còn từ khoá còn-lại là nhánh cuối. Dòng kết thúc bằng dấu hai chấm mở ra một khối lệnh.
           Các dòng thụt vào cùng độ sâu, thường bốn dấu cách, thuộc cùng một khối. Vòng lặp đếm lặp khối bên dưới, mỗi lượt biến nhận một giá trị kế tiếp, và chữ in nghĩa là nằm trong. Vòng lặp điều kiện lặp chừng nào điều kiện còn đúng.""",
           focus=[1, "1.2", "1.3", "1.3", "1.4", "1.5"], clear=True),
        st(repl_block(R_RANGE, title="range(...) sinh dãy số, bắt đầu từ 0, dừng TRƯỚC số cuối; list(...) xếp dãy đó thành danh sách để nhìn thấy")
           + "<p><code>[ … ]</code> là một <b>danh sách</b>: các giá trị xếp thành hàng. <code>range(3)</code> sinh <code>0, 1, 2</code>; <code>range(1, 4)</code> sinh <code>1, 2, 3</code>; số thứ ba là bước nhảy; <code>list(…)</code> xếp các số do <code>range</code> sinh ra thành một danh sách để ta nhìn thấy.</p>",
           """Cuối cùng là lệnh sinh dãy số, bọc trong lệnh danh sách để ta nhìn thấy các số. Nó cho ra các số bắt đầu từ không và dừng trước số cuối cùng. Dãy ba số bắt đầu từ không là không, một, hai. Dãy từ một đến bốn dừng trước bốn là một, hai, ba. Số thứ ba là bước nhảy.
           Cặp ngoặc vuông là một danh sách, tức các giá trị xếp thành hàng, và vòng lặp đếm có thể đi qua từng phần tử của nó.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: rẽ nhánh là ngã ba, vòng lặp là con đường vòng lại", [
        st(svg(1500, 470,
               box(30, 170, 190, 90, ["tien = 7 500 000"], C_GRAY, 24, True),
               arrow(225, 215, 290, 215, "#2a78d6"),
               box(295, 150, 270, 130, ["tien &lt; 1 000 000 ?"], C_AMBER, 26, True),
               arrow(565, 215, 650, 215, "#dc2626", "sai"),
               box(655, 150, 290, 130, ["tien &lt; 20 000 000 ?"], C_AMBER, 26, True),
               arrow(945, 215, 1030, 215, "#dc2626", "sai"),
               box(1035, 170, 220, 90, ["muc = lon"], C_RED, 26, True),
               arrow(430, 150, 430, 70, "#16a34a", "đúng"),
               box(310, 10, 240, 60, ["muc = nho"], C_GREEN, 26, True),
               arrow(800, 150, 800, 70, "#16a34a", "đúng"),
               box(680, 10, 240, 60, ["muc = vua"], C_GREEN, 26, True),
               txt(750, 350, "máy hỏi TỪ TRÊN XUỐNG; điều kiện đầu tiên đúng thì chạy nhánh đó rồi BỎ QUA phần còn lại", 26, "middle", "#1f2937", True),
               txt(750, 395, "7 500 000 không nhỏ hơn 1 000 000 (sai) nhưng nhỏ hơn 20 000 000 (đúng): nhánh vừa", 24, "middle", "#16a34a"),
               txt(750, 440, "else không có điều kiện: nhận mọi trường hợp còn lại", 24, "middle", "#6b7280")),
           """Hình này là câu lệnh rẽ nhánh như một chuỗi ngã ba. Máy hỏi từ trên xuống. Số tiền bảy triệu rưỡi không nhỏ hơn một triệu, nên câu hỏi đầu trả lời sai, máy đi tiếp. Câu hỏi thứ hai, có nhỏ hơn hai mươi triệu, trả lời đúng.
           Máy chạy nhánh mức vừa rồi bỏ qua phần còn lại. Nhánh cuối cùng không có điều kiện, nó nhận mọi trường hợp còn lại."""),
        st(svg(1500, 400,
               box(30, 140, 300, 120, ["còn phần tử nào", "chưa xử lý?"], C_AMBER, 26, True),
               arrow(335, 200, 470, 200, "#16a34a", "còn"),
               box(475, 140, 340, 120, ["làm khối lệnh", "tong = tong + tien"], C_BLUE, 26, True),
               arrow(820, 200, 940, 200, "#2a78d6"),
               box(945, 140, 260, 120, ["lấy phần tử", "kế tiếp"], C_GRAY, 26, True),
               arrow(1075, 135, 1075, 70, "#2a78d6"),
               arrow(1075, 70, 180, 70, "#2a78d6"),
               arrow(180, 70, 180, 135, "#2a78d6"),
               arrow(180, 265, 180, 335, "#dc2626", "hết"),
               box(60, 340, 240, 55, ["thoát vòng lặp"], C_RED, 24, True),
               txt(850, 340, "vòng đếm: biết trước số lượt (mỗi phần tử một lượt)", 26, "middle", "#1f2937", True),
               txt(850, 380, "vòng điều kiện: chừng nào câu hỏi còn đúng thì vòng lại", 26, "middle", "#1f2937", True)),
           """Hình thứ hai là vòng lặp, một con đường vòng lại. Máy hỏi còn phần tử nào chưa xử lý không. Nếu còn, máy chạy khối lệnh, lấy phần tử kế tiếp, rồi quay lại câu hỏi. Khi hết, máy thoát.
           Vòng lặp đếm biết trước số lượt. Vòng lặp điều kiện cứ vòng lại chừng nào câu hỏi còn đúng."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: so sánh, thứ tự các nhánh, biến cộng dồn, vòng điều kiện", [
        st(repl_block(R_LOGIC, 0, 3, title="Bước 1. Ghép điều kiện bằng và / hoặc / không phải")
           + "<p>Mức vừa là $1\\,000\\,000 \\le tien < 20\\,000\\,000$: cần <b>cả hai</b> vế đúng nên dùng <code>and</code>. Mức nhỏ <b>hoặc</b> lớn: chỉ cần một vế, dùng <code>or</code>.</p>",
           """Bước một, ghép điều kiện. Mức vừa đòi cả hai vế cùng đúng, tiền không nhỏ hơn một triệu và nhỏ hơn hai mươi triệu, nên dùng từ và. Bảy triệu rưỡi thoả cả hai, máy trả lời đúng. Còn mức nhỏ hoặc lớn chỉ cần một vế đúng, nên dùng từ hoặc.
           Với bảy triệu rưỡi cả hai vế đều sai, máy trả lời sai. Và từ phủ định đảo kết quả."""),
        st(code_block(P_PL) + out_block(P_PL) + "<p>Vì máy hỏi từ trên xuống và <b>dừng ở nhánh đúng đầu tiên</b>, nhánh sau không cần ghi lại cận dưới: tới <code>elif</code> là đã chắc <code>tien &gt;= 1000000</code>.</p>",
           """Bước hai, thứ tự các nhánh. Vì máy hỏi từ trên xuống và dừng ở nhánh đúng đầu tiên, nhánh sau không cần ghi lại cận dưới. Tới nhánh thứ hai là đã chắc số tiền không nhỏ hơn một triệu, vì nhánh một đã sai. Làm thử với bảy triệu rưỡi: nhánh một sai, nhánh hai đúng, in mức vừa.""",
           clear=True),
        st(table(["lượt", "tien", "tong sau lượt"],
                 [["bắt đầu", "—", "0"], ["1", "450 000", "450 000"], ["2", "12 000 000", "12 450 000"], ["3", "800 000", "13 250 000"],
                  ["4", "30 000 000", "43 250 000"], ["5", "2 500 000", "45 750 000"]])
           + "<p>Vì mỗi lượt <code>tong = tong + tien</code> lấy <b>giá trị tong cũ</b> cộng thêm <code>tien</code> rồi dán nhãn mới, <code>tong</code> là biến <b>cộng dồn</b>: bắt đầu từ $0$ để không cộng thừa.</p>",
           """Bước ba, biến cộng dồn. Ta chạy tay chương trình tổng. Bắt đầu tổng bằng không. Lượt một, cộng bốn trăm năm mươi nghìn. Lượt hai, cộng mười hai triệu, được mười hai triệu bốn trăm năm mươi nghìn. Cứ thế đến lượt năm, tổng là bốn mươi lăm triệu bảy trăm năm mươi nghìn.
           Vì mỗi lượt lấy giá trị tổng cũ cộng thêm số tiền rồi dán nhãn mới, nên phải bắt đầu từ không, nếu không ta cộng thừa một số.""", clear=True),
        st(code_block(P_WHILE) + out_block(P_WHILE) + "<p>Vì không biết trước bao nhiêu lượt, ta dùng vòng điều kiện: mỗi lượt <b>phải làm điều kiện tiến dần tới sai</b> (số dư tăng, tháng tăng). Lãi $0{,}5\\%$ một tháng là <code>so_du * 5 // 1000</code>; <code>//</code> chia lấy <b>phần nguyên</b> (<code>7 // 2</code> ra <code>3</code>), nên lãi là số nguyên đồng.</p>",
           """Bước bốn, vòng điều kiện. Ta muốn biết gửi mười triệu, lãi không phẩy năm phần trăm mỗi tháng nhập vào gốc, sau bao nhiêu tháng thì gấp đôi. Vì không biết trước số lượt, ta dùng vòng điều kiện. Mỗi lượt số dư tăng và số tháng tăng, nên điều kiện tiến dần tới sai.
           Hai dấu gạch chéo chia lấy phần nguyên, nên lãi mỗi tháng là số nguyên đồng. Máy trả lời một trăm ba mươi chín tháng, hơn mười một năm rưỡi.""", clear=True),
        st(code_block(P_BRK) + out_block(P_BRK) + "<p><code>continue</code>: <b>bỏ qua phần còn lại của lượt này</b>, sang lượt sau. <code>break</code>: <b>thoát hẳn</b> vòng lặp.</p>",
           """Bước năm, hai lệnh điều khiển. Lệnh bỏ lượt này, ở đây bỏ qua các giao dịch dưới một triệu. Lệnh thoát hẳn, ở đây dừng ngay khi gặp giao dịch từ hai mươi triệu trở lên. Vì vậy chỉ giao dịch mười hai triệu được xét, rồi chương trình dừng ở ba mươi triệu.""", clear=True),
    ], checks=["1000000 <= 7500000 < 20000000", "not (7500000 < 1000000 or 7500000 >= 20000000)",
               "[sum([450000, 12000000, 800000, 30000000, 2500000][:i + 1]) for i in range(5)] == [450000, 12450000, 13250000, 43250000, 45750000]",
               "1.005 ** 139 >= 2 > 1.005 ** 138"])
    sc_ex = sc("example", "example", "Ví dụ: phân loại cả danh sách, và đọc một lỗi thụt lề", [
        st(code_block(P_TONG, title="Tệp tong.py") + out_block(P_TONG) + "<p>Danh sách có năm giao dịch, tổng $45\\,750\\,000$, đúng bảng chạy tay.</p>",
           """Ta chạy lại chương trình tổng và đối chiếu với bảng chạy tay. Danh sách có năm giao dịch. Mỗi lượt cộng dồn vào tổng, và nếu giao dịch từ hai mươi triệu trở lên thì tăng biến đếm lên một. Kết quả khớp bảng, bốn mươi lăm triệu bảy trăm năm mươi nghìn, và chỉ một giao dịch lớn."""),
        st(code_block(P_RANGE, title="Vòng đếm với dãy số: số tháng") + out_block(P_RANGE),
           """Khi không có sẵn danh sách mà chỉ cần lặp một số lần, ta dùng lệnh sinh dãy số. Dãy từ một đến bốn dừng trước bốn, nên ba lượt, in ba tháng.""", clear=True),
        st(code_block(P_THUT, title="Quên thụt lề dòng in") + out_block(P_THUT)
           + "<p>Đọc <b>dòng cuối</b>: máy <b>mong một khối thụt vào</b> sau dòng rẽ nhánh ở dòng $2$. Sửa: thụt dòng $3$ bốn dấu cách.</p>",
           """Giờ ta đọc một lỗi thụt lề. Dòng ba nằm sát lề trái, trong khi dòng hai kết thúc bằng dấu hai chấm, nên máy báo lỗi thụt lề. Đọc dòng cuối: máy mong một khối thụt vào sau câu lệnh rẽ nhánh ở dòng hai. Cách sửa là thụt dòng ba bốn dấu cách.""",
           clear=True),
    ], checks=["sum([450000, 12000000, 800000, 30000000, 2500000]) == 45750000", "len(range(1, 4)) == 3", "3 + 1 == 4"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cộng tay theo nhóm, và đếm theo hai cách", [
        st(repl_block(repl("KiemTong", [("450000 + 800000 + 2500000", "3750000"), ("12000000 + 30000000", "42000000"), ("3750000 + 42000000", "45750000")]), title="Cộng tay theo nhóm: nhóm nhỏ rồi nhóm lớn")
           + "<p>Chia nhóm khác với chương trình: ba giao dịch nhỏ trước, hai giao dịch lớn sau. Cộng hai nhóm: $3\\,750\\,000 + 42\\,000\\,000 = 45\\,750\\,000$ ✓</p>",
           """Đường kiểm khác, cộng tay theo nhóm thay vì từng giao dịch. Ba giao dịch nhỏ cộng lại ba triệu bảy trăm năm mươi nghìn. Hai giao dịch lớn cộng lại bốn mươi hai triệu. Cộng hai nhóm được bốn mươi lăm triệu bảy trăm năm mươi nghìn, trùng với chương trình. Hai cách chia nhóm khác nhau cùng ra một con số."""),
    ], checks=["450000 + 800000 + 2500000 == 3750000 and 12000000 + 30000000 == 42000000 and 3750000 + 42000000 == 45750000"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn dần: số lần lặp tăng theo, thời gian cũng tăng theo", [
        st(code_block(P_N, title="Cộng 1 + 2 + … + n bằng vòng lặp") + out_block(P_N),
           """Ta thử vòng lặp ở quy mô lớn hơn. Chương trình này cộng các số từ một đến một triệu bằng vòng lặp, và cho ra năm trăm nghìn năm trăm nghìn lẻ năm trăm nghìn. Một triệu lượt lặp, mỗi lượt một phép cộng."""),
        st(table(["n (số lượt lặp)", "số phép cộng", "thời gian vòng lặp (đo trên máy kiểm, số minh hoạ)"],
                 [["×1: 1 000", "1 000", gl(s3[0])], ["×1 000: 1 000 000", "1 000 000", gl(s6[0])], ["×10 000: 10 000 000", "10 000 000", gl(s7[0])],
                  ["×1 000 000: 1 000 000 000 (ngoại suy)", "1 000 000 000", s9[0] + " (ngoại suy tuyến tính)"]])
           + "<p class='note'><b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo để đoán quy mô lớn hơn: ước lượng, chưa đo.</p>"
           + "<div class='box key'><b>Đánh đổi:</b> số lượt lặp tăng bao nhiêu lần thì thời gian tăng cùng bậc chừng đó (mỗi lần nhân $10$ số lượt, thời gian tăng khoảng $10$ lần, lệch vài chục phần trăm). "
             "Với tổng các số từ $1$ đến $n$ còn có công thức $\\frac{n(n+1)}{2}$ chỉ cần <b>một phép tính</b>; nhưng khi phải xem từng giao dịch thì không có lối tắt, ta phải lặp.</div>",
           f"""Bảng này cho thấy quy mô. Một nghìn lượt gần như tức thì. Một triệu lượt mất {s6[1]}. Mười triệu lượt mất {s7[1]}. Một tỉ lượt thì ta chưa đo, mà ngoại suy, nghĩa là nhân theo tỉ lệ từ số đã đo để đoán quy mô lớn hơn. Ngoại suy tuyến tính cho {s9[1]}, chỉ là ước lượng.
           Mỗi lần nhân mười số lượt, thời gian tăng khoảng mười lần, lệch vài chục phần trăm. Thời gian đo trên máy kiểm, số minh hoạ, máy của bạn sẽ khác.
           Riêng tổng các số liên tiếp có công thức một phép tính, nhưng việc xem từng giao dịch thì không có lối tắt.""",
           clear=True, introduces=["pyt_ngoai_suy"]),
    ], checks=["1000000 * (1000000 + 1) // 2 == 500000500000", "10000000 // 1000 == 10000 and 1000000000 // 1000000 == 1000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Lệch một: <code>range(1, 5)</code> dừng <b>trước</b> $5$.</div>'
           + code_block(P_LECH) + out_block(P_LECH)
           + "<p>Muốn tổng $1 + 2 + 3 + 4 + 5 = 15$ phải viết <code>range(1, 6)</code>. Phép thử bắt được lỗi: so với công thức $\\frac{5 \\cdot 6}{2} = 15$ hoặc in vài giá trị của biến đếm.</p>",
           """Lỗi thứ nhất, của người mới, là lệch một. Dãy từ một đến năm dừng trước năm, nên chương trình cộng một đến bốn, ra mười thay vì mười lăm. Phép thử bắt được lỗi này là so với công thức năm nhân sáu chia hai, hoặc in vài giá trị của biến đếm."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Viết điều kiện như viết câu tiếng Việt.</div>'
           + repl_block(R_OR) + "<p><code>loai == \"rut\" or \"chuyen\"</code> hiểu thành <code>(loai == \"rut\") or \"chuyen\"</code>; chuỗi không rỗng được coi là <b>đúng</b>, nên điều kiện luôn đúng. Viết đủ từng vế, hoặc dùng <code>in</code>: <code>loai in (\"rut\", \"chuyen\")</code> hỏi “<code>loai</code> có nằm trong nhóm này không?”; nhóm giá trị trong ngoặc tròn là một <b>bộ</b>, như danh sách nhưng không sửa được.</p>",
           """Lỗi thứ hai, của cả người đã đi làm, là viết điều kiện như viết câu tiếng Việt. Loại bằng rút hoặc chuyển, viết gọn như vậy, máy hiểu là loại bằng rút, hoặc chữ chuyển. Chuỗi không rỗng được coi là đúng, nên điều kiện luôn đúng, kể cả khi loại là nạp.
           Phải viết đủ từng vế, hoặc dùng từ in để hỏi một giá trị có nằm trong một nhóm không, nhóm đó là một bộ, tức các giá trị trong cặp ngoặc tròn. Máy đưa kết quả chữ chuyển thay vì sai, nên không ai thấy lỗi.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Vòng lặp điều kiện quên làm điều kiện tiến dần tới sai: chạy mãi.</div>'
           + code_block(P_VOHAN, title="Khi thử, luôn thêm một giới hạn số bước") + out_block(P_VOHAN)
           + "<p>Biến <code>so_du</code> không đổi nên điều kiện đúng mãi. Phép thử: <b>thêm bộ đếm bước</b> như trên; sau $5$ bước số dư vẫn là $10\\,000\\,000$. Khi chạy mãi ngoài thật, ta ngắt bằng <code>Ctrl+C</code>.</p>",
           """Lỗi thứ ba, của người đã đi làm, là vòng lặp điều kiện chạy mãi. Quên cộng lãi vào số dư, điều kiện không bao giờ sai. Phép thử là thêm một bộ đếm bước vào điều kiện, như ở đây. Sau năm bước số dư vẫn là mười triệu, nghĩa là vòng lặp không tiến triển.
           Khi chương trình chạy mãi ngoài thật, bạn ngắt bằng tổ hợp phím điều khiển và chữ C.""", clear=True),
    ], checks=["sum(range(1, 5)) == 10 and sum(range(1, 6)) == 15 and 5 * 6 // 2 == 15", "bool('chuyen') is True"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b></p>
<ol><li>Vòng <code>for i in range(3): print(i * 10)</code> in những gì?</li>
<li>Đổi chỗ hai nhánh đầu như mã dưới đây: với <code>tien = 500000</code> nhánh nào chạy?</li></ol>"""
           + code_block(P_DAO) + """
<p><b>Quyết định:</b> đọc hết $1\\,000\\,000$ giao dịch trong tệp, hay lặp tới khi số dư đủ gấp ba? Chọn vòng đếm hay vòng điều kiện? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Câu một, vòng lặp đếm ba lượt, mỗi lượt in số đếm nhân mười, in những gì. Câu hai, hai nhánh đầu đã đổi chỗ như mã trên màn hình, với giao dịch năm trăm nghìn thì nhánh nào chạy.
           Sau đó là một quyết định, đọc hết một triệu giao dịch, hay lặp tới khi số dư đủ gấp ba, chọn vòng đếm hay vòng điều kiện, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(code_block(P_Q1, title="Câu 1: lượt 0, 1, 2") + out_block(P_Q1) + "<p>Lượt $0$: in $0$; lượt $1$: in $10$; lượt $2$: in $20$. Ba dòng: <code>0</code>, <code>10</code>, <code>20</code>.</p>",
           """Đáp án câu một. Biến đếm chạy không, một, hai, nên in không, mười, hai mươi, ba dòng."""),
        st(code_block(P_DAO) + out_block(P_DAO) + "<p>$500\\,000 < 20\\,000\\,000$ <b>đã</b> thoả ở nhánh đầu nên nhánh <code>nho</code> không bao giờ tới (mọi số dưới $1\\,000\\,000$ cũng dưới $20\\,000\\,000$): sai thứ tự gây ra mức <code>vua</code> thay vì <code>nho</code>.</p>",
           """Đáp án câu hai. Vì năm trăm nghìn đã nhỏ hơn hai mươi triệu ở nhánh đầu, máy dừng ở đó và in mức vừa, trong khi đúng ra là mức nhỏ. Nhánh nhỏ không bao giờ được tới, vì mọi số dưới một triệu cũng dưới hai mươi triệu.
           Đổi thứ tự nhánh có thể làm sai kết quả mà không báo lỗi.""", clear=True),
        st("<div class='box key'><b>Quyết định:</b> đọc hết tệp: <b>vòng đếm</b>, vì biết trước phải đi qua từng giao dịch, mỗi giao dịch một lượt. "
           "Lặp tới khi số dư đủ gấp ba: <b>vòng điều kiện</b>, vì không biết trước số lượt, chỉ biết điều kiện dừng. Với vòng điều kiện luôn nghĩ: điều gì làm điều kiện tiến tới sai?</div>",
           """Còn quyết định cuối thì thế này. Đọc hết tệp thì dùng vòng đếm, vì biết trước phải đi qua từng giao dịch. Lặp tới khi số dư đủ gấp ba thì dùng vòng điều kiện, vì không biết trước số lượt, chỉ biết khi nào dừng. Với vòng điều kiện luôn tự hỏi, điều gì làm điều kiện tiến dần tới sai.""", clear=True),
    ], checks=["[i * 10 for i in range(3)] == [0, 10, 20]", "('vua' if 500000 < 20000000 else ('nho' if 500000 < 1000000 else 'lon')) == 'vua'"])
    sc_prac = practice_scene(sc, "Tự làm: phân loại giao dịch theo mức tiền, tính tổng và đếm", pr_steps(
        st, "PYT", "L01",
        """<p><b>Đề</b>: tạo <code>phan_loai.py</code>. Danh sách giao dịch (chép nguyên): <code>[250000, 3200000, 75000000, 1800000, 64000000, 900000, 5000000, 120000]</code>.</p>
<ol><li>Với mỗi giao dịch in một dòng <code>số_tiền mức</code>: <code>nho</code> nếu dưới $2\\,000\\,000$; <code>vua</code> nếu dưới $60\\,000\\,000$; còn lại <code>lon</code>.</li>
<li>Rồi in <code>Tong: …</code> và <code>Nho, vua, lon: a b c</code> (số giao dịch mỗi mức).</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp chấm py với danh sách tám giao dịch cho sẵn. Với mỗi giao dịch, in một dòng gồm số tiền và mức, nhỏ nếu dưới hai triệu, vừa nếu dưới sáu mươi triệu, còn lại là lớn.
        Sau vòng lặp, in tổng tiền và số giao dịch của từng mức. Hãy dừng video và làm.""",
        LAB_OUT, "phan_loai.py",
        """<div class="box key"><b>Nếu kẹt:</b> đặt <code>tong = 0</code> và ba biến đếm bằng <code>0</code> trước vòng lặp. Trong vòng <code>for tien in giao_dich:</code> dùng một khối <code>if / elif / else</code>; mỗi nhánh tăng biến đếm của nó thêm $1$. In <code>muc</code> cuối mỗi lượt.
Lời giải ở <code>labs/PYT/L01/loi_giai.py</code>.</div>""",
        """Nếu kẹt, đặt tổng và ba biến đếm bằng không trước vòng lặp. Trong vòng lặp dùng một khối rẽ nhánh với ba nhánh, mỗi nhánh tăng biến đếm của nó thêm một. In mức ở cuối mỗi lượt.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L01")
    write_lab("PYT", "L01", """# Lab PYT L01 — Phân loại giao dịch theo mức tiền

Cần: Python 3.11 trở lên. Tạo `phan_loai.py`. Danh sách giao dịch (chép nguyên, số minh hoạ — khác ví dụ trong bài):

```python
giao_dich = [250000, 3200000, 75000000, 1800000, 64000000, 900000, 5000000, 120000]
```

1. Với **mỗi** giao dịch (vòng `for`) in một dòng `<số tiền> <mức>`:
   `nho` nếu dưới 2 000 000; `vua` nếu dưới 60 000 000; còn lại `lon`.
2. Sau vòng lặp in `Tong: <tổng tiền>` và `Nho, vua, lon: <a> <b> <c>` (số giao dịch của từng mức, cách nhau một dấu cách).

Chạy: `python phan_loai.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L01 phan_loai.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("so sánh cho ra đúng hoặc sai; and / or / not ghép điều kiện", "if – elif – else: dừng ở nhánh đúng đầu tiên",
                 "khối lệnh = dòng thụt vào sau dấu hai chấm", "for: biết trước số lượt; while: biết điều kiện dừng", "biến cộng dồn bắt đầu từ 0; break / continue",
                 "số lượt lặp tăng bao nhiêu thì thời gian tăng chừng đó"),
           """Tổng kết chuỗi logic. So sánh cho ra đúng hoặc sai, và các từ nối ghép điều kiện. Câu lệnh rẽ nhánh dừng ở nhánh đúng đầu tiên. Khối lệnh là các dòng thụt vào sau dấu hai chấm.
           Vòng đếm dùng khi biết trước số lượt, vòng điều kiện dùng khi biết khi nào dừng. Biến cộng dồn bắt đầu từ không. Và số lượt lặp tăng bao nhiêu lần thì thời gian tăng chừng đó."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi nhánh và mỗi vòng lặp hỏi hai câu: <b>điều kiện này đúng khi nào?</b> và <b>điều gì làm vòng lặp kết thúc?</b> Thử với đúng một giá trị nhỏ, bằng tay, trước khi chạy cả triệu.</div>
<p>Bài sau: hàm, để gói một việc lại, đặt tên và dùng lại ở nhiều nơi.</p>""",
           """Điều cần mang theo, với mỗi nhánh và mỗi vòng lặp hãy hỏi hai câu. Điều kiện này đúng khi nào, và điều gì làm vòng lặp kết thúc. Hãy thử bằng tay với một giá trị nhỏ trước khi chạy cả triệu.
           Bài sau, ta học hàm, để gói một việc lại, đặt tên và dùng lại ở nhiều nơi.""", forward_ref=True),
    ])
    return lesson("L01", "re_nhanh_vong_lap", "Bài 1 — Rẽ nhánh và vòng lặp: để chương trình tự chọn việc và lặp lại một việc",
                  "curriculum/pyt.yaml L01; audit/pyt/verify_pyt.py L01 (chạy thật trên Python 3.11 và 3.13); Python Tutorial §4 (More Control Flow Tools: if, for, range, break/continue, while), "
                  "Language Reference §8 (Compound statements), §2.1.8 (Indentation); thời gian vòng lặp đo bằng verify_pyt (máy kiểm, số minh hoạ; ngoại suy 10^9 lượt tuyến tính); số tiền là số minh hoạ",
                  ["Viết câu lệnh rẽ nhánh nhiều nhánh bằng so sánh và các từ nối and, or, not",
                   "Đọc một lỗi thụt lề và sửa nó",
                   "Viết vòng lặp đếm và vòng lặp điều kiện, dùng break và continue",
                   "Tính tổng và đếm bằng biến cộng dồn, chạy tay từng lượt",
                   "Giải thích vì sao thứ tự các nhánh quyết định kết quả",
                   "Nêu khi nào dùng vòng đếm, khi nào dùng vòng điều kiện",
                   "Nêu thời gian của vòng lặp thay đổi thế nào ở ba quy mô dữ liệu",
                   "Chỉ ra ba lỗi hay gặp: lệch một, điều kiện viết như câu văn, vòng lặp chạy mãi",
                   "Viết chương trình phân loại giao dịch theo mức tiền, tính tổng và đếm"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "formula"), (5, "formula"), (6, "quiz"), (7, "scale"),
                          (8, "pitfalls"), (9, "practice")])
