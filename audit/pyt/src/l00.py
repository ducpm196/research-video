from lib import *
from labkit import write_lab, practice_steps, practice_scene

# ── dữ liệu chạy thật ───────────────────────────────────────────────────────────────────────────────────────────────────
R_HOOK = repl("Hook", [("0.1 + 0.2", "0.30000000000000004"), ("0.1 + 0.2 == 0.3", "False")])
R_LAI_BUG = repl("LaiLech", [("12000000 * 0.072", "863999.9999999999")])
R_TYPE = repl("Kieu", [
    ("1250000", "1250000"), ("0.072", "0.072"), ('"A01"', "'A01'"), ("True", "True"),
    ("type(1250000)", "<class 'int'>"), ("type(0.072)", "<class 'float'>"), ('type("A01")', "<class 'str'>"), ("type(True)", "<class 'bool'>"),
    ("type(1250000).__name__", "'int'"), ("type(0.072).__name__", "'float'"),
])
R_BIEN = repl("Bien", [
    ("so_du = 2000000", ""), ("so_du", "2000000"), ("so_du = so_du + 500000", ""), ("so_du", "2500000"),
    ("a = 5", ""), ("b = a", ""), ("a = 7", ""), ("b", "5"),
])
R_LAI = repl("Lai", [
    ("so_du = 2000000", ""), ("lai_suat = 0.06", ""), ("thang = 3", ""), ("so_du * lai_suat", "120000.0"),
    ("so_du * lai_suat * thang / 12", "30000.0"), ("so_du + 30000", "2030000"),
])
R_CHIA = repl("Chia", [
    ("2000000 / 3", "666666.6666666666"), ("2000000 // 3", "666666"), ("2000000 % 3", "2"),
    ("666666 * 3 + 2", "2000000"),
])
R_UT = repl("UuTien", [("2 + 3 * 4", "14"), ("(2 + 3) * 4", "20"), ("2 ** 3 * 2", "16"), ("-7 // 2", "-4")])
R_NHIPHAN = repl("NhiPhan", [
    ("0.5 + 0.25 == 0.75", "True"), ("0.1 + 0.2 == 0.3", "False"), ("round(0.1 + 0.2, 2) == 0.3", "True"),
])
R_CHECK = repl("Kiem", [
    ("2000000 * 6 * 3 // 1200", "30000"), ("round(2000000 * 0.06 * 3 / 12)", "30000"),
    ("(2000000 // 7) * 7 + 2000000 % 7 == 2000000", "True"),
])
R_QM = repl("QuyMo", [
    ("1 + 0.1 - 1", "0.10000000000000009"),
    ("1000000 + 0.1 - 1000000", "0.09999999997671694"),
    ("1000000000000000 + 0.1 - 1000000000000000", "0.125"),
])
R_QM2 = repl("QuyMo2", [("2 ** 53", "9007199254740992"), ("2 ** 53 + 1", "9007199254740993"), ("float(2 ** 53) + 1", "9007199254740992.0")])
R_FSTR = repl("FString", [
    ("tong = 2030000", ""), ('f"Tong: {tong}"', "'Tong: 2030000'"), ('f"Tong: {tong:,}"', "'Tong: 2,030,000'"),
    ('f"Tong: {2000000 + 30000:,}"', "'Tong: 2,030,000'"),
])
R_PIT = repl("LoiTien", [
    ("12000000 * 0.072", "863999.9999999999"), ("int(12000000 * 0.072)", "863999"),
    ("round(12000000 * 0.072)", "864000"), ("12000000 * 72 // 1000", "864000"),
])
R_ROUND = repl("RoundChan", [("round(0.5)", "0"), ("round(1.5)", "2"), ("round(2.5)", "2"), ("(2 * 5 + 2) // (2 * 2)", "3")])
R_DIV = repl("ChiaFloat", [("10 / 5", "2.0"), ("10 // 5", "2"), ("type(10 / 5)", "<class 'float'>")])
R_QUIZ = repl("Quiz", [("17 // 5", "3"), ("17 % 5", "2"), ("17 / 5", "3.4"), ("type(7 / 7)", "<class 'float'>"), ("5 * 3 + 2", "17")])

P_LAI = py("lai", '''so_du = 2000000
lai_suat = 0.06
thang = 3
lai = so_du * lai_suat * thang / 12
print("So du goc:", so_du)
print("Lai", thang, "thang:", round(lai))
print(f"Tong: {so_du + round(lai):,}")''', "So du goc: 2000000\nLai 3 thang: 30000\nTong: 2,030,000")
SH_RUN = sh("ChayTep", [("python lai.py", P_LAI["out"]), ("echo $?", "0")], files={"lai.py": P_LAI["code"] + "\n"})
P_NHAP = py("nhap", '''print("Nhap so tien:")
tien = int(input())
print("Gap doi:", tien * 2)''', "Nhap so tien:\nGap doi: 300000", stdin="150000\n")
P_SAI1 = py("nhap_sai", '''print("Nhap so tien:")
tien = input()
print("Gap doi:", tien * 2)''', "Nhap so tien:\nGap doi: 150000150000", stdin="150000\n")
SH_PRE = sh("Pre", [
    ("python -c \"print('xin chao')\"", "xin chao"), ("echo $?", "0"),
    ('python -c "1/0"', 'Traceback (most recent call last):\n  File "<string>", line 1, in <module>\nZeroDivisionError: division by zero'), ("echo $?", "1"),
], only311=True)
SH_CD = sh("ThuMuc", [("pwd", "/c/Users/ban"), ("cd khoa_hoc", ""), ("pwd", "/c/Users/ban/khoa_hoc"), ("ls", "labs/"), ("cd ..", ""), ("pwd", "/c/Users/ban")],
           files={"khoa_hoc/labs/README.txt": "x\n"})

LAB_SOL = '''so_du = 25000000
lai_suat = 0.084
thang = 6
lai = so_du * lai_suat * thang / 12
lai_tron = round(lai)
print(f"So du goc: {so_du:,}")
print(f"Lai {thang} thang: {lai_tron:,}")
print(f"Tong nhan duoc: {so_du + lai_tron:,}")
print("Kieu cua lai:", type(lai).__name__)'''
LAB_OUT = "So du goc: 25,000,000\nLai 6 thang: 1,050,000\nTong nhan duoc: 26,050,000\nKieu cua lai: float"
P_LAB = py("lab_l00", LAB_SOL, LAB_OUT)


def bash_note(steps):
    """Bài đầu của khoá: nói rõ lệnh chấm làm gì (bước 1 = khung kết quả mong đợi)."""
    steps[1]["show"] = steps[1]["show"].replace("— in <b>ĐÚNG</b> khi trùng.", "— chạy tệp chấm của bài (<code>bash</code> chạy một tệp lệnh); in <b>ĐÚNG</b> khi trùng.")
    steps[1]["say"] = steps[1]["say"].replace("dùng lệnh ở dưới màn hình;", "dùng lệnh ở dưới màn hình, lệnh này chạy tệp chấm của bài;")
    return steps


def build():
    sc_hook = sc("hook", "hook", "Sổ tiết kiệm lệch một đồng: vì sao máy tính cộng sai?", [
        st(repl_block(R_HOOK, title="Hỏi máy một phép cộng đơn giản"),
           """Chào bạn, hôm nay ta bắt đầu học viết chương trình bằng Python, và trước hết hãy xem một chuyện lạ. Ta bảo máy lấy không phẩy một cộng không phẩy hai.
           Máy trả lời không phẩy ba, nhưng kèm một dãy số lẻ ở cuối, và khi ta hỏi kết quả có bằng không phẩy ba hay không, máy trả lời là không bằng."""),
        st(repl_block(R_LAI_BUG, title="Lãi của sổ tiết kiệm 12 triệu đồng, lãi 7,2% một năm")
           + "<p>Đúng ra phải là <b>864 000</b> đồng.</p>",
           """Một sổ tiết kiệm mười hai triệu đồng, lãi bảy phẩy hai phần trăm một năm, đúng ra sinh lãi tám trăm sáu mươi tư nghìn đồng. Nhưng máy trả lời tám trăm sáu mươi ba nghìn chín trăm chín mươi chín phẩy chín chín chín.
           Cắt phần lẻ là mất đúng một đồng."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Chạy một chương trình bằng <b>hai cách</b> nào?</li>
<li><b>Giá trị</b>, <b>kiểu</b>, <b>biến</b> và các <b>phép toán</b> hoạt động ra sao?</li>
<li>Vì sao <b>số thực</b> lệch một chút, và <b>tiền</b> nên lưu bằng gì?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, chạy một chương trình bằng hai cách nào. Hai, giá trị, kiểu, biến và các phép toán hoạt động ra sao.
           Ba, vì sao số thực lệch một chút, và tiền nên lưu bằng gì."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: cửa sổ lệnh, chương trình tìm được qua PATH, mã thoát", [
        st(term_block(SH_PRE, 0, 2, title="Gọi chương trình từ cửa sổ lệnh")
           + "<p>Máy tìm được <code>python</code> vì thư mục chứa nó nằm trong biến <code>PATH</code>. Mã thoát <code>0</code> nghĩa là thành công.</p>"
           + "<p>Cờ <code>-c</code> bảo máy chạy ngay câu nằm trong cặp nháy, không cần tệp; <code>print(…)</code> in giá trị trong ngoặc ra màn hình. Máy báo không tìm thấy <code>python</code> thì cài từ <b>python.org</b>, tích ô thêm vào <code>PATH</code> khi cài; kiểm bằng <code>python --version</code>.</p>"
           + "<p><b>Git Bash</b> là cửa sổ lệnh của khoá: tải <b>Git for Windows</b> ở git-scm.com, cài, rồi mở <b>Git Bash</b> trong menu Start. Dấu <code>&#36;</code> ở đầu dòng là dấu nhắc của máy, không gõ nó. <code>echo</code> in chữ đứng sau nó ra màn hình; <code>&#36;?</code> là mã thoát của lệnh vừa chạy, nên <code>echo &#36;?</code> in mã thoát đó.</p>",
           """Cửa sổ lệnh của khoá cài từ trang chủ bộ công cụ quản lý phiên bản, tên nó hiện trên màn hình. Máy tìm được chương trình vì thư mục chứa nó nằm trong biến môi trường tìm đường. Lệnh in chữ in một dòng ra màn hình, và dấu hỏi sau dấu đô la là mã thoát của lệnh vừa chạy, bằng không nghĩa là thành công. Cờ chữ c cho chạy ngay câu nằm trong cặp nháy, và lệnh in của ngôn ngữ in giá trị trong ngoặc ra màn hình."""),
        st(term_block(SH_CD, 0, 4, title="Cửa sổ lệnh luôn đứng trong một thư mục")
           + "<p><code>pwd</code> in thư mục đang đứng; <code>cd khoa_hoc</code> đi vào thư mục con tên đó (<code>cd ..</code> lùi ra một cấp); <code>ls</code> liệt kê tên trong thư mục.</p>",
           """Mọi tệp của khoá lưu ở thư mục gốc của bộ khoá, nơi có thư mục thực hành. Cửa sổ lệnh luôn đứng trong một thư mục, và lệnh hỏi vị trí cho biết đó là đâu.
           Lệnh đổi thư mục kèm tên thì đi vào thư mục con, kèm hai dấu chấm thì lùi ra.""",
           introduces=["pyt_cd"], clear=True),
        st("<div class='box key'>Mọi tệp của khoá lưu ở <b>thư mục gốc của bộ khoá</b> (gõ <code>ls</code> thấy thư mục <code>labs</code>). Nhanh nhất: mở thư mục đó trong File Explorer, chuột phải vào chỗ trống, chọn <i>Open Git Bash here</i> "
           "(Windows 11: chọn <i>Show more options</i> trước), rồi gõ <code>pwd</code> và <code>ls</code> để kiểm.</div>",
           """Cách nhanh nhất là mở thư mục gốc trong trình quản lý tệp, bấm chuột phải vào chỗ trống, chọn mở cửa sổ lệnh tại đây, rồi kiểm lại bằng lệnh hỏi vị trí.""", clear=True),
        st(term_block(SH_PRE, 2, 4, title="Khi có lỗi: đọc từ dưới lên")
           + "<p>Mã thoát khác <code>0</code> là thất bại; <b>dòng cuối</b> của thông báo nói lỗi gì: <code>ZeroDivisionError</code> = chia cho không; dòng bắt đầu bằng <code>File</code> cho biết dòng thứ mấy.</p>"
           + "<p class='note'>Hình này là Python 3.11. Python 3.13 in thêm dòng mã và dấu <code>^</code> giữa các dòng; cách đọc vẫn vậy: dòng cuối trước, rồi tìm dòng bắt đầu bằng <code>File</code>.</p>",
           """Khi có lỗi, mã thoát khác không và máy in thông báo nhiều dòng. Hãy đọc từ dòng cuối lên, vì dòng cuối nói thẳng lỗi gì, ở đây là chia cho không.""",
           clear=True),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã dấu nhắc, dấu bằng, dấu thăng và bảy phép toán", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>python</code>", "mở cửa sổ gõ từng câu", "máy hiện dấu nhắc <code>&gt;&gt;&gt;</code>: <b>chờ bạn gõ một câu</b>, chạy ngay, in kết quả"],
                  ["<code>exit()</code>", "thoát cửa sổ", "quay về cửa sổ lệnh thường"],
                  ["<code>python lai.py</code>", "chạy cả tệp", "máy đọc <b>cả tệp</b> <code>lai.py</code> từ trên xuống dưới, mỗi dòng một câu lệnh"]]),
           """Bảng đầu là cách mở chương trình. Gõ tên ngôn ngữ, máy mở cửa sổ gõ từng câu với dấu nhắc ba dấu lớn hơn, bạn gõ một câu thì máy chạy ngay và in kết quả.
           Cách thứ hai là viết nhiều dòng vào một tệp có đuôi chấm py rồi gõ tên ngôn ngữ cùng tên tệp, máy đọc cả tệp từ trên xuống."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>so_du = 2000000</code>", "gán", "dấu <code>=</code> <b>không</b> là “bằng” của toán: nó <b>dán nhãn</b> <code>so_du</code> lên giá trị bên phải"],
                  ["<code>a == b</code>", "so sánh bằng", "hai dấu <code>==</code> <b>hỏi</b> “a có bằng b không?”, trả lời đúng hoặc sai"],
                  ["<code># ghi chú</code>", "chú thích", "từ dấu <code>#</code> đến hết dòng, máy <b>bỏ qua</b>; chỉ để người đọc"],
                  ["<code>\"A01\"</code>", "chuỗi", "chữ đặt trong cặp nháy kép (hay đơn); <code>\"A01\"</code> là chữ, không phải số"]]),
           """Bảng thứ hai là bốn dấu hay gặp. Một dấu bằng là phép gán, nó dán nhãn bên trái lên giá trị bên phải. Hai dấu bằng mới là câu hỏi hai bên có bằng nhau không.
           Dấu thăng mở đầu chú thích, máy bỏ qua đến hết dòng. Chữ đặt trong cặp nháy gọi là chuỗi, chuỗi A không một là chữ chứ không phải số.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "đọc là", "ví dụ"],
                 [["<code>+  -  *</code>", "cộng, trừ, nhân", "<code>7 * 2</code> ra <code>14</code>"],
                  ["<code>/</code>", "chia, <b>luôn ra số thực</b>", "<code>7 / 2</code> ra <code>3.5</code>"],
                  ["<code>//</code>", "chia lấy <b>phần nguyên</b>", "<code>7 // 2</code> ra <code>3</code>"],
                  ["<code>%</code>", "chia lấy <b>phần dư</b>", "<code>7 % 2</code> ra <code>1</code>"],
                  ["<code>**</code>", "lũy thừa", "<code>2 ** 10</code> ra <code>1024</code>"]]),
           """Bảng cuối là bảy phép toán số học. Cộng, trừ, nhân như thường. Một dấu gạch chéo là phép chia, luôn ra số thực, như bảy chia hai ra ba phẩy năm. Hai dấu gạch chéo lấy phần nguyên, bảy chia hai được ba.
           Dấu phần trăm lấy phần dư, bảy chia hai dư một. Hai dấu sao là lũy thừa, hai mũ mười bằng một nghìn không trăm hai mươi tư.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: chương trình chạy từng dòng, biến là cái nhãn dán lên giá trị", [
        st(svg(1500, 430,
               box(20, 40, 520, 340, ["", "", "", ""], C_GRAY),
               txt(280, 80, "chương trình (đọc từ trên xuống)", 26, "middle", "#1f2937", True),
               txt(60, 150, "(1)   a = 5", 30, "start", "#1f2937"),
               txt(60, 220, "(2)   b = a", 30, "start", "#1f2937"),
               txt(60, 290, "(3)   a = 7", 30, "start", "#1f2937"),
               txt(60, 350, "máy làm xong dòng này mới sang dòng sau", 22, "start", "#6b7280"),
               box(900, 60, 160, 90, ["5"], C_BLUE, 34, True),
               box(900, 230, 160, 90, ["7"], C_GREEN, 34, True),
               box(680, 80, 130, 50, ["b"], C_AMBER, 28, True),
               box(680, 250, 130, 50, ["a"], C_AMBER, 28, True),
               arrow(815, 105, 895, 105, "#d97706"),
               arrow(815, 275, 895, 275, "#d97706"),
               txt(1290, 100, "sau câu (3): a dán vào 7,", 26, "middle", "#1f2937", True),
               txt(1290, 140, "b vẫn dán vào 5", 26, "middle", "#1f2937", True),
               txt(1290, 230, "đổi a không kéo b theo:", 24, "middle", "#dc2626"),
               txt(1290, 266, "b chỉ nhớ giá trị lúc dán", 24, "middle", "#dc2626")),
           """Bên trái, máy đọc chương trình từ trên xuống, xong dòng này mới sang dòng sau. Dòng một dán nhãn a lên số năm, dòng hai dán thêm nhãn b lên cùng giá trị.
           Dòng ba dán lại nhãn a sang số bảy, còn nhãn b không bị kéo theo, nó vẫn nằm trên số năm."""),
        st(repl_block(R_BIEN, 4, 8, title="Thử đúng như hình") + repl_block(R_BIEN, 0, 4, title="Và một biến dùng lại chính nó"),
           """Ta thử đúng như hình. Gán a bằng năm, gán b bằng a, rồi gán lại a bằng bảy. Hỏi b, máy trả lời năm. Còn khi viết số dư bằng số dư cộng năm trăm nghìn, máy lấy giá trị hiện tại bên phải, cộng rồi dán nhãn mới.""", clear=True),
        st(svg(1500, 330,
               box(30, 70, 300, 140, ["1250000", "số nguyên", "tiền đồng, số lượng"], C_BLUE, 26, True),
               box(390, 70, 300, 140, ["0.072", "số thực", "lãi suất, tỉ lệ"], C_AMBER, 26, True),
               box(750, 70, 300, 140, ["\"A01\"", "chuỗi", "tên, mã tài khoản"], C_GREEN, 26, True),
               box(1110, 70, 340, 140, ["True / False", "đúng–sai", "câu trả lời có/không"], C_PURPLE, 26, True),
               txt(750, 270, "mỗi giá trị có MỘT kiểu; kiểu quyết định phép toán nào làm được", 28, "middle", "#1f2937", True),
               txt(750, 310, "tên kiểu trong ngôn ngữ: int, float, str, bool", 24, "middle", "#6b7280")),
           """Mỗi giá trị còn có một kiểu. Số nguyên dùng cho tiền đồng và số lượng, số thực có phần lẻ dùng cho lãi suất. Chuỗi là chữ dùng cho tên và mã, còn giá trị đúng sai trả lời câu hỏi có hay không.
           Kiểu quyết định phép toán nào làm được, và bạn hỏi máy kiểu bằng lệnh hỏi kiểu."""),
        st(repl_block(R_TYPE, 4, 10, title="Hỏi kiểu bằng type(...)")
           + "<p>Dấu chấm lấy một <b>thuộc tính</b> của giá trị; <code>__name__</code> là tên kiểu viết thành chữ (trong cặp nháy).</p>",
           """Ta hỏi thử bốn lần. Một triệu hai trăm năm mươi nghìn là số nguyên. Không phẩy không bảy hai là số thực. Chữ A không một là chuỗi. Và đúng là giá trị đúng sai. Muốn tên kiểu viết thành chữ, thêm dấu chấm và tên thuộc tính ghi trên màn hình sau lệnh hỏi kiểu."""),
    ], checks=["type(1250000) is int and type(0.072) is float and type('A01') is str and type(True) is bool"])
    sc_form = sc("formula", "formula", "Suy ra từng bước: tính lãi, chia dư, thứ tự ưu tiên, và vì sao số thực lệch", [
        st(repl_block(R_LAI, 0, 4, title="Bước 1. Đặt tên cho từng số, rồi tính một năm")
           + "<p>Vì lãi suất là <b>6%</b> một năm, một năm sinh $2\\,000\\,000 \\cdot 0{,}06 = 120\\,000$ đồng.</p>",
           """Bước một, đặt tên cho từng số rồi mới tính. Vì lãi suất sáu phần trăm là một năm, nên một năm sinh hai triệu nhân không phẩy không sáu, bằng một trăm hai mươi nghìn.
           Máy trả lời một trăm hai mươi nghìn chấm không, có chấm vì kết quả là số thực."""),
        st(repl_block(R_LAI, 4, 6, title="Bước 2. Chỉ lấy ba tháng, rồi cộng vào gốc")
           + "<p>Vì ba tháng là $\\frac{3}{12}$ năm, nhân thêm ba rồi chia mười hai: $\\frac{120\\,000 \\cdot 3}{12} = 30\\,000$. Tổng nhận: $2\\,000\\,000 + 30\\,000 = 2\\,030\\,000$ ✓</p>",
           """Bước hai, ta chỉ lấy ba tháng. Vì ba tháng là ba phần mười hai của một năm, ta nhân thêm ba rồi chia mười hai, được ba mươi nghìn. Cộng vào gốc, người gửi nhận hai triệu không trăm ba mươi nghìn.""", clear=True),
        st(repl_block(R_CHIA, title="Bước 3. Chia tiền cho người: /, //, %")
           + "<p>Chia $2\\,000\\,000$ đồng cho $3$ người: mỗi người $666\\,666$ (phần nguyên), <b>dư $2$</b>. Kiểm: $666\\,666 \\cdot 3 + 2 = 2\\,000\\,000$ ✓</p>",
           """Bước ba, chia tiền cho người. Vì chia hai triệu đồng cho ba người không hết, dấu chia thường cho ra số thực lẻ, vô nghĩa với đồng tiền. Phần nguyên là sáu trăm sáu mươi sáu nghìn sáu trăm sáu mươi sáu đồng mỗi người, và còn dư hai đồng, nhân lại ba rồi cộng hai thì đúng hai triệu.""", clear=True),
        st(repl_block(R_UT, 0, 3, title="Bước 4. Thứ tự ưu tiên, như trong toán")
           + "<p>Vì nhân làm <b>trước</b> cộng, $2 + 3 \\cdot 4 = 2 + 12 = 14$. Muốn cộng trước thì dùng ngoặc: $(2 + 3) \\cdot 4 = 20$.</p>",
           """Bước bốn, thứ tự ưu tiên. Giống toán học, lũy thừa làm trước, rồi nhân chia, rồi cộng trừ. Vì nhân làm trước cộng, hai cộng ba nhân bốn bằng hai cộng mười hai, là mười bốn. Muốn cộng trước, ta dùng ngoặc, được hai mươi.""", clear=True),
        st(repl_block(R_NHIPHAN, title="Bước 5. Vì sao 0.1 + 0.2 lệch: máy đếm bằng hệ hai")
           + "<p>Máy lưu số bằng <b>hệ nhị phân</b> (hệ hai): chỉ có hai chữ số <code>0</code> và <code>1</code>, các vị trí đếm gấp đôi nhau (1, 2, 4, 8… như hệ mười có 1, 10, 100…), và số chữ số cố định. Một phần mười ở hệ hai là số lặp vô hạn, như một phần ba ở hệ mười ($0{,}333$ và cứ thế mãi), nên bị <b>cắt</b>. Nửa và một phần tư thì vừa khít.</p>",
           """Bước năm, vì sao số thực lệch. Máy lưu số bằng hệ hai, chỉ có hai chữ số không và một, các vị trí gấp đôi nhau, với một số chữ số cố định. Một phần mười ở hệ hai là số lặp vô hạn, giống một phần ba ở hệ mười là không phẩy ba ba ba mãi mãi, nên phải bị cắt.
           Nửa cộng một phần tư thì vừa khít nên đúng, còn làm tròn hai chữ số thì cho lại không phẩy ba.""", clear=True),
    ], checks=["2000000 * 0.06 == 120000.0", "120000 * 3 // 12 == 30000", "2000000 + 30000 == 2030000", "2000000 // 3 == 666666 and 2000000 % 3 == 2",
               "666666 * 3 + 2 == 2000000", "2 + 3 * 4 == 14 and (2 + 3) * 4 == 20", "0.5 + 0.25 == 0.75 and 0.1 + 0.2 != 0.3 and round(0.1 + 0.2, 2) == 0.3"])
    sc_ex = sc("example", "example", "Ví dụ: chạy một tệp tính lãi, rồi một tệp đọc bàn phím", [
        st(repl_block(R_FSTR, title="Trước hết, chuỗi có chỗ điền: f\"…{…}…\"")
           + "<p>Chữ <code>f</code> ngay trước cặp nháy cho phép điền vào chỗ <code>{…}</code> một tên biến hoặc cả một phép tính; <code>:,</code> thêm dấu phẩy ngăn cách hàng nghìn.</p>",
           """Trước khi viết tệp, ta học một dạng chuỗi có chỗ điền. Đặt chữ f ngay trước cặp nháy, rồi viết tên biến hoặc cả một phép tính trong cặp ngoặc nhọn, máy điền kết quả vào đó. Thêm dấu hai chấm và dấu phẩy, máy ngăn cách hàng nghìn cho dễ đọc."""),
        st(file_block(P_LAI, title="Tệp lai.py (gõ bằng trình soạn thảo, lưu cùng thư mục)")
           + "<p><b>Trình soạn thảo</b> là chương trình gõ chữ thuần (Notepad, VS Code; không dùng Word). Lưu tên <code>lai.py</code> (đuôi <code>.py</code>) vào thư mục gốc của bộ khoá, đúng thư mục cửa sổ lệnh đang đứng (kiểm bằng <code>pwd</code>).</p>",
           """Bây giờ ta viết tệp đầu tiên. Hãy mở một trình soạn thảo chữ thuần, không phải phần mềm soạn văn bản, rồi gõ bảy dòng này. Lưu thành tệp lai chấm py ở thư mục gốc của bộ khoá, đúng chỗ cửa sổ lệnh đang đứng. Ba dòng đầu đặt tên cho số dư, lãi suất và số tháng. Dòng thứ tư tính lãi bằng công thức vừa suy ra. Ba dòng cuối in kết quả, lệnh in nhận các giá trị cách nhau dấu phẩy và in chúng cách nhau một dấu cách; dòng cuối dùng chuỗi có chỗ điền."""),
        st(term_block(SH_RUN, title="Chạy tệp từ cửa sổ lệnh") + "<p>Lệnh làm tròn đổi <code>30000.0</code> thành số nguyên <code>30000</code>.</p>",
           """Ta chạy tệp từ cửa sổ lệnh. Gõ tên ngôn ngữ, dấu cách, rồi tên tệp. Máy in ba dòng, đúng như ba lệnh in. Chú ý lệnh làm tròn đã đổi ba mươi nghìn chấm không thành số nguyên ba mươi nghìn."""),
        st(file_block(P_NHAP, title="Tệp nhap.py: đọc một số từ bàn phím") + io_block(P_NHAP, [0], title="Chạy và gõ 150000 rồi bấm xuống dòng"),
           """Tệp thứ hai đọc từ bàn phím. Lệnh nhập đợi bạn gõ một dòng rồi trả về dòng đó dưới dạng chuỗi, nên ta bọc nó bằng lệnh đổi sang số nguyên. Bạn gõ một trăm năm mươi nghìn, máy in gấp đôi là ba trăm nghìn.""", clear=True),
    ], checks=["round(2000000 * 0.06 * 3 / 12) == 30000", "2000000 + 30000 == 2030000", "150000 * 2 == 300000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: số nguyên, ngoặc, và phép thử chia dư", [
        st(repl_block(R_CHECK, 0, 2, title="Cách 1: làm toàn số nguyên, không dùng số thực")
           + "<p>Lãi suất $6\\%$ là $6$ phần $100$; ba tháng là $3$ phần $12$ nên mẫu chung $100 \\cdot 12 = 1200$.</p>",
           """Đường kiểm khác, làm toàn bằng số nguyên. Lãi suất sáu phần trăm là sáu phần một trăm, ba tháng là ba phần mười hai, nên mẫu chung là một nghìn hai trăm. Nhân tử số trước rồi chia nguyên một lần cho ra ba mươi nghìn, trùng kết quả bằng số thực.
          """),
    ], checks=["2000000 * 6 * 3 // 1200 == 30000", "(2000000 // 7) * 7 + 2000000 % 7 == 2000000"])
    sc_scale = sc("scale", "concept", "Khi số lớn dần: số thực mất độ chính xác, số nguyên thì không", [
        st(repl_block(R_QM, title="Cộng 0.1 đồng vào một tổng, rồi trừ tổng đó đi")
           + "<p>Đúng ra phải ra $0{,}1$ ở cả ba lần. Cách đọc: $10^{6}$ là một và sáu số không (một triệu); $10^{-16}$ là một chia cho $10^{16}$, rất nhỏ ($0{,}0000000000000001$).</p>",
           """Ta lấy một số, cộng thêm không phẩy một, rồi trừ lại chính số đó, đúng ra luôn ra không phẩy một. Mười mũ sáu là một và sáu số không, mười mũ âm mười sáu là một chia cho mười mũ mười sáu, rất nhỏ. Với số một, sai số cỡ mười mũ âm mười sáu, với một triệu cỡ mười mũ âm mười một.
           Với mười mũ mười lăm, máy trả lời không phẩy một hai lăm, vì số lẻ không phẩy một đã bị làm tròn thành một phần tám."""),
        st(repl_block(R_QM2, title="Số nguyên không có giới hạn đó")
           + "<p>Số thực chỉ giữ chắc được tới $2^{53} = 9\\,007\\,199\\,254\\,740\\,992$ (khoảng $9 \\cdot 10^{15}$): ở đó cộng thêm $1$ <b>không thay đổi</b> gì. <code>float(x)</code> đổi số nguyên <code>x</code> thành số thực.</p>",
           """Số thực còn có giới hạn cứng. Lệnh đổi sang số thực biến số nguyên thành số thực. Hai mũ năm mươi ba là chín nghìn không trăm linh bảy nghìn tỉ và hơn nữa. Từ đó trở lên, cộng thêm một vào số thực không thay đổi gì cả. Số nguyên thì khác: cộng một vẫn đúng chính xác.""",
           clear=True),
        st(table(["quy mô tổng tiền", "số thực (float)", "số nguyên (int)"],
                 [["×1 (1 đồng)", "sai số cỡ 10<sup>−16</sup>", "chính xác"],
                  ["×10<sup>6</sup> (1 triệu đồng)", "sai số cỡ 10<sup>−11</sup>", "chính xác"],
                  ["×10<sup>15</sup> (1 nghìn nghìn tỉ đồng)", "0,1 bị làm tròn thành 0,125: sai 0,025", "chính xác"]])
           + "<div class='box key'><b>Đánh đổi:</b> số thực cho phép phần lẻ nhưng sai số tăng theo độ lớn; số nguyên chính xác nhưng không có phần lẻ. "
             "Vì vậy tiền đồng lưu bằng <b>số nguyên đồng</b>, còn quy tắc làm tròn viết rõ bằng một lệnh (số minh hoạ cho quy mô; kết quả lấy từ máy kiểm).</div>",
           """Đánh đổi là số thực cho phép phần lẻ nhưng sai số tăng theo độ lớn, số nguyên chính xác nhưng không có phần lẻ.
           Vì vậy tiền đồng nên lưu bằng số nguyên đồng, còn quy tắc làm tròn viết rõ bằng một lệnh.""", clear=True),
    ], checks=["2 ** 53 == 9007199254740992 and 2 ** 53 + 1 == 9007199254740993 and float(2 ** 53) + 1 == float(2 ** 53)",
               "1 + 0.1 - 1 != 0.1 and 1000000 + 0.1 - 1000000 != 0.1 and 10 ** 15 + 0.1 - 10 ** 15 == 0.125",
               "10 ** 15 == 1000000000000000", "abs((1 + 0.1 - 1) - 0.1) < 1e-15 and 1e-12 < abs((1000000 + 0.1 - 1000000) - 0.1) < 1e-10 and abs((10 ** 15 + 0.1 - 10 ** 15) - 0.1) > 0.02"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên đổi kiểu: lệnh nhập luôn trả về <b>chuỗi</b>.</div>'
           + file_block(P_SAI1, title="Tệp nhap_sai.py (quên bọc bằng số nguyên)") + io_block(P_SAI1, [0], title="Gõ 150000")
           + "<p>Không báo lỗi, nhưng <code>\"150000\" * 2</code> là <b>lặp chuỗi hai lần</b>: <code>150000150000</code>. Phép thử bắt được: hỏi <code>type(tien)</code>, hoặc so với kết quả tính tay $300\\,000$.</p>",
           """Lỗi thứ nhất, của người mới, là quên đổi kiểu. Lệnh nhập luôn trả về chuỗi. Nhân một chuỗi với hai là lặp chuỗi hai lần, nên ra một trăm năm mươi nghìn một trăm năm mươi nghìn. Chương trình không báo lỗi gì cả.
           Phép thử bắt được là so với kết quả tính tay ba trăm nghìn, hoặc hỏi kiểu của biến."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Phép chia một dấu luôn ra số thực, kể cả khi chia hết.</div>'
           + repl_block(R_DIV) + "<p>Cần số nguyên (số giao dịch, số người) thì dùng <code>//</code>. Phép thử: <code>type(...)</code>.</p>",
           """Lỗi thứ hai, của người mới, là tưởng phép chia một dấu cho ra số nguyên khi chia hết. Mười chia năm ra hai chấm không, một số thực. Khi cần số nguyên, hãy dùng phép chia lấy phần nguyên, và hỏi kiểu để kiểm.""",
           clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tính tiền bằng số thực rồi cắt bỏ phần lẻ.</div>'
           + repl_block(R_PIT) + "<p>Cắt bằng <code>int</code> mất $1$ đồng; làm tròn rõ ràng, hoặc tính toàn số nguyên, đều ra $864\\,000$. Số tiền sai mà <b>không báo lỗi</b>, nên dễ lọt vào sổ cái.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là tính tiền bằng số thực rồi cắt phần lẻ. Mười hai triệu nhân không phẩy không bảy hai ra tám trăm sáu mươi ba nghìn chín trăm chín mươi chín chấm chín, cắt bằng lệnh đổi sang số nguyên mất đúng một đồng.
           Làm tròn có quy tắc, hoặc tính toàn số nguyên, đều cho tám trăm sáu mươi tư nghìn.""", clear=True),
        st("<div class='box warn'><b>Lưu ý về chính lệnh làm tròn.</b> Đúng giữa hai số nguyên, <code>round</code> chọn số <b>chẵn</b>.</div>"
           + repl_block(R_ROUND)
           + "<p>$0{,}5 \\to 0$, $1{,}5 \\to 2$, $2{,}5 \\to 2$. Nếu nghiệp vụ cần “làm tròn lên từ nửa”, tự viết bằng số nguyên: $\\frac{5}{2}$ làm tròn nửa lên là $\\frac{2 \\cdot 5 + 2}{2 \\cdot 2} = 3$ (chia nguyên).</p>",
           """Còn một điều về chính lệnh làm tròn. Đúng giữa hai số nguyên, nó chọn số chẵn, nên không phẩy năm thành không, còn hai phẩy năm thành hai.
           Muốn làm tròn lên từ nửa, hãy tự viết bằng số nguyên, như công thức hiện trên màn hình.""", clear=True),
    ], checks=["'150000' * 2 == '150000150000'", "int(12000000 * 0.072) == 863999 and round(12000000 * 0.072) == 864000 and 12000000 * 72 // 1000 == 864000",
               "type(10 / 5) is float and type(10 // 5) is int", "round(0.5) == 0 and round(1.5) == 2 and round(2.5) == 2 and (2 * 5 + 2) // (2 * 2) == 3"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b></p>
<ol><li>Máy in gì với <code>17 // 5</code>, <code>17 % 5</code>, <code>17 / 5</code>?</li>
<li><code>type(7 / 7)</code> là kiểu gì?</li></ol>
<p><b>Quyết định:</b> lưu số tiền <code>1250000</code> đồng bằng số nguyên hay số thực? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Câu một, máy in gì với mười bảy chia lấy phần nguyên cho năm, chia dư cho năm, và chia thường cho năm. Câu hai, bảy chia bảy có kiểu gì.
           Rồi một quyết định, lưu một triệu hai trăm năm mươi nghìn đồng bằng số nguyên hay số thực, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_QUIZ, 0, 3, title="Câu 1") + "<p>$17 = 3 \\cdot 5 + 2$: thương $3$, dư $2$; chia thường ra $3{,}4$.</p>",
           """Đáp án câu một. Mười bảy bằng ba nhân năm cộng hai, nên phần nguyên là ba, phần dư là hai. Phép chia thường ra ba phẩy bốn."""),
        st(repl_block(R_QUIZ, 3, 4, title="Câu 2") + "<p>Bảy chia bảy bằng $1$, nhưng dấu <code>/</code> <b>luôn</b> ra số thực, nên kiểu là số thực: $1.0$.</p>",
           """Đáp án câu hai. Bảy chia bảy bằng một, nhưng phép chia một dấu luôn cho số thực, nên kiểu vẫn là số thực.""", clear=True),
        st("<div class='box key'><b>Quyết định:</b> chọn <b>số nguyên</b>. Tiền đồng không có phần lẻ; số nguyên chính xác ở mọi quy mô, "
           "còn số thực lệch như ta đã thấy ở $0{,}1 + 0{,}2$. Khi buộc phải nhân với tỉ lệ, tính rồi <b>làm tròn một lần, có quy tắc rõ ràng</b>.</div>",
           """Quyết định: chọn số nguyên. Tiền đồng không có phần lẻ, số nguyên chính xác ở mọi quy mô, còn số thực lệch như ta đã thấy. Khi buộc phải nhân với một tỉ lệ, hãy tính rồi làm tròn một lần, với quy tắc rõ ràng.""", clear=True),
    ], checks=["17 // 5 == 3 and 17 % 5 == 2 and 17 / 5 == 3.4", "type(7 / 7) is float", "3 * 5 + 2 == 17"])
    sc_prac = practice_scene(sc, "Tự làm: tính lãi tiết kiệm từ ba biến, in có định dạng", bash_note(pr_steps(
        st, "PYT", "L00",
        """<p><b>Đề</b>: tạo <code>lai_tk.py</code>. Đặt ba biến: <code>so_du = 25000000</code>, <code>lai_suat = 0.084</code> (8,4% một năm), <code>thang = 6</code>. Rồi in <b>bốn dòng</b> (xem <code>de.md</code>):</p>
<ol><li><code>So du goc: …</code> (có dấu phẩy ngăn hàng nghìn);</li>
<li><code>Lai 6 thang: …</code> — lãi đã <b>làm tròn</b> thành số nguyên;</li>
<li><code>Tong nhan duoc: …</code> = gốc + lãi đã làm tròn;</li>
<li><code>Kieu cua lai: …</code> — kiểu của lãi <b>trước</b> khi làm tròn (gợi ý: <code>type(lai).__name__</code>).</li></ol>""",
        """Bây giờ tới phần bạn tự làm, tạo một tệp chấm py. Đặt ba biến, số dư hai mươi lăm triệu, lãi suất tám phẩy bốn phần trăm một năm, và sáu tháng. Rồi in bốn dòng. Dòng một là số dư gốc có dấu ngăn hàng nghìn.
        Dòng hai là lãi sáu tháng đã làm tròn thành số nguyên. Dòng ba là tổng nhận được. Dòng bốn là kiểu của lãi trước khi làm tròn. Hãy dừng video và làm.""",
        LAB_OUT, "lai_tk.py",
        """<div class="box key"><b>Nếu kẹt:</b> lãi một năm = <code>so_du * lai_suat</code>; sáu tháng thì nhân <code>thang</code> rồi chia <code>12</code>. Làm tròn: <code>round(lai)</code>.
In có ngăn hàng nghìn: <code>f"…{so_du:,}"</code>. <code>type(lai).__name__</code>: dấu chấm lấy một <b>thuộc tính</b> của giá trị; <code>__name__</code> là tên kiểu viết bằng chữ (<code>type(5).__name__</code> là <code>int</code>). Lời giải ở <code>labs/PYT/L00/loi_giai.py</code>.</div>""",
        """Nếu kẹt, lãi một năm là số dư nhân lãi suất, sáu tháng thì nhân số tháng rồi chia mười hai. Làm tròn bằng lệnh làm tròn, in có ngăn hàng nghìn bằng chuỗi có chỗ điền. Với dòng bốn, dấu chấm sau lệnh hỏi kiểu lấy tên của kiểu viết thành chữ.
       """, pause=240)), "PYT", "L00")
    write_lab("PYT", "L00", """# Lab PYT L00 — Lãi tiết kiệm sáu tháng

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Nếu máy báo không tìm thấy `python`: tải bản cài từ python.org, **tích ô thêm Python vào PATH** khi cài, rồi mở lại Git Bash và kiểm lại. Không cần cài thêm thư viện nào.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `lai_tk.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó (mở thư mục đó trong File Explorer, chuột phải vào chỗ trống, chọn *Open Git Bash here*; Windows 11: chọn *Show more options* trước). Kiểm: gõ `pwd` (in thư mục đang đứng) và `ls` (phải thấy `labs/`). Đang đứng sai chỗ thì dùng `cd tên_thư_mục` để đi vào, `cd ..` để lùi ra. Các bài sau chỉ nhắc "mở Git Bash ở thư mục gốc của bộ khoá": làm đúng như vậy.

Tạo `lai_tk.py`. Đặt ba biến (số minh hoạ, **khác ví dụ trong bài**):

```python
so_du = 25000000      # đồng
lai_suat = 0.084      # 8,4% một năm
thang = 6
```

Rồi in **đúng bốn dòng**, theo thứ tự (dùng chuỗi có chỗ điền `f"…{biến}…"`; `:,` ngăn hàng nghìn):
1. `So du goc: <số dư, có dấu phẩy ngăn hàng nghìn>`
2. `Lai 6 thang: <lãi làm tròn thành số nguyên, có dấu phẩy ngăn hàng nghìn>` — lãi = `so_du * lai_suat * thang / 12`, rồi `round(...)`
3. `Tong nhan duoc: <gốc + lãi đã làm tròn, có dấu phẩy ngăn hàng nghìn>`
4. `Kieu cua lai: <tên kiểu của lãi TRƯỚC khi làm tròn>` (gợi ý: `type(lai).__name__` — dấu chấm lấy thuộc tính của giá trị, `__name__` là tên kiểu bằng chữ, ví dụ `type(5).__name__` là `int`)

Chạy: `python lai_tk.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L00 lai_tk.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("hai cách chạy: gõ từng câu hoặc chạy cả tệp", "giá trị có kiểu; biến là nhãn dán", "/ ra số thực; // phần nguyên; % phần dư",
                 "nhập luôn là chuỗi: đổi kiểu", "số thực lệch; tiền dùng số nguyên"),
           """Tổng kết chuỗi logic. Có hai cách chạy, gõ từng câu hoặc chạy cả tệp. Mỗi giá trị có một kiểu, và biến chỉ là nhãn dán lên giá trị.
           Phép chia một dấu ra số thực, hai dấu lấy phần nguyên, dấu phần trăm lấy phần dư. Lệnh nhập luôn trả về chuỗi nên cần đổi kiểu. Số thực lệch, nên tiền lưu bằng số nguyên."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng tin kết quả chỉ vì máy tính ra nó. Luôn <b>kiểm bằng một đường thứ hai</b> (tính tay, làm toàn số nguyên) và hỏi “kiểu của giá trị này là gì?”.</div>
<p>Bài sau: rẽ nhánh theo điều kiện và vòng lặp, để chương trình tự chọn việc và lặp lại một việc nhiều lần.</p>""",
           """Điều cần mang theo, đừng tin một kết quả chỉ vì máy tính ra nó. Hãy kiểm bằng một đường thứ hai, và luôn hỏi kiểu của giá trị là gì.
           Bài sau, ta học rẽ nhánh theo điều kiện và vòng lặp, để chương trình tự chọn việc và lặp lại một việc.""", forward_ref=True),
    ])
    return lesson("L00", "chay_python_gia_tri_bien", "Bài 0 — Chạy Python: giá trị, biến, kiểu và phép toán",
                  "curriculum/pyt.yaml L00; audit/pyt/verify_pyt.py L00 (chạy thật trên Python 3.11 và 3.13: cửa sổ gõ từng câu bằng code.InteractiveConsole, tệp .py, Git Bash); "
                  "Python Tutorial §3 (An Informal Introduction to Python), Language Reference §3.2 và §6 (Expressions), Tutorial §15 (Floating-Point Arithmetic: Issues and Limitations), "
                  "IEEE 754-2019 (nhị phân 64 bit, 53 bit định trị); số tiền là số minh hoạ; mọi kết quả máy in là đầu ra thật",
                  ["Chạy chương trình bằng hai cách: cửa sổ gõ từng câu và tệp chạy từ cửa sổ lệnh",
                   "Phân biệt bốn kiểu giá trị (số nguyên, số thực, chuỗi, đúng–sai) và hỏi kiểu bằng lệnh hỏi kiểu",
                   "Nêu biến là cái nhãn dán lên giá trị, đổi nhãn không kéo nhãn khác theo",
                   "Tính bằng bảy phép toán số học theo đúng thứ tự ưu tiên",
                   "Viết chương trình dùng lệnh in, lệnh nhập và chuỗi có chỗ điền",
                   "Giải thích vì sao 0.1 + 0.2 khác 0.3",
                   "Nêu vì sao tiền đồng nên lưu bằng số nguyên khi quy mô tổng tiền tăng",
                   "Chỉ ra ba lỗi hay gặp: nhập trả về chuỗi, phép chia ra số thực, cắt phần lẻ của tiền",
                   "Viết chương trình tính lãi tiết kiệm từ ba biến và in có định dạng"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "example"), (2, "intuition"), (3, "intuition"), (4, "formula"), (5, "example"), (6, "formula"), (7, "scale"),
                          (8, "pitfalls"), (9, "practice")])
