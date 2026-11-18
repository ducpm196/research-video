from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_a import t2, val2

R_HOOK = repl("Hook", [
    ("import re", ""), ('dong = "09:01 GD#A0001 chuyen 500.000 VND"', ""), (r're.findall(r"\d+", dong)', "['09', '01', '0001', '500', '000']"),
    (r're.search(r"GD#(\w+) \w+ ([\d.]+) VND", dong).groups()', "('A0001', '500.000')"),
])
R_PRE = repl("Pre", [('ma = "GD#A0731"', ""), ("ma[3:]", "'A0731'"), ("len(ma)", "8"), ("ma[0] + ma[1]", "'GD'")])
R_FIX = repl("BatBien", [
    ('s = "chuyen"', ""), ("s.upper()", "'CHUYEN'"), ("s", "'chuyen'"),
    ('s[0] = "C"', 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nTypeError: \'str\' object does not support item assignment'),
    ('"C" + s[1:]', "'Cluyen'".replace("Cluyen", "Chuyen")),
])
R_FIX3 = repl("SuaChuoi", [
    ('s = "chuyen"', ""),
    ('s[0] = "C"', 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nTypeError: \'str\' object does not support item assignment'),
    ('"C" + s[1:]', "'Chuyen'"),
])
R_SPLIT = repl("TachGhep", [
    ('dong = "A01,chuyen,500000"', ""), ('phan = dong.split(",")', ""), ("phan", "['A01', 'chuyen', '500000']"),
    ('"|".join(phan)', "'A01|chuyen|500000'"), ('",".join(phan) == dong', "True"),
])
R_METH = repl("PhuongThuc", [
    ('ma = "GD#A0731"', ""), ('ma.find("#")', "2"), ('ma.startswith("GD")', "True"), ('ma.replace("GD", "TX")', "'TX#A0731'"),
    ('"  A01 ".strip()', "'A01'"),
])
R_UTF = repl("UTF8", [
    ('s = "tiền"', ""), ("len(s)", "4"), ('s.encode("utf-8")', r"b'ti\xe1\xbb\x81n'"), ('len(s.encode("utf-8"))', "6"),
    ('s.encode("utf-8").decode("utf-8") == s', "True"),
])
R_RE = repl("Regex", [
    ("import re", ""), ('dong = "10:15 GD#A0731 chuyen 1250000 VND"', ""), (r're.findall(r"\d+", dong)', "['10', '15', '0731', '1250000']"),
    (r're.search(r"\d+ VND", dong).group()', "'1250000 VND'"), (r'm = re.search(r"GD#(\w+) (\w+) (\d+)", dong)', ""),
    ("m.groups()", "('A0731', 'chuyen', '1250000')"), ("m.group(3)", "'1250000'"), (r'print(re.search(r"xyz", dong))', "None"),
])
R_GREEDY = repl("Tham", [("import re", ""), ('re.search(r"<(.*)>", "<a><b>").group(1)', "'a><b'"), ('re.search(r"<(.*?)>", "<a><b>").group(1)', "'a'")])
R_NUM = repl("SoVN", [('float("1.250")', "1.25"), ('int("1.250".replace(".", ""))', "1250"), ('int("1.250.000".replace(".", ""))', "1250000")])
R_KIEM = repl("Kiem", [('int("500.000".replace(".", "")) + int("2.000.000".replace(".", ""))', "2500000"), ("500000 + 2000000", "2500000")])
R_QUIZ = repl("Quiz", [('"A01,chuyen".split(",")[1].upper()', "'CHUYEN'"), ('len("đồng")', "4"), ('len("đồng".encode("utf-8"))', "7")])

P_LOG = py("nhat_ky", r'''import re
nhat_ky = [
    "09:01 GD#A0001 chuyen 500.000 VND",
    "09:02 GD#A0002 rut 2.000.000 VND",
    "09:03 LOI GD#A0003 timeout",
]
tong = 0
for dong in nhat_ky:
    m = re.search(r"GD#(\w+) (\w+) ([\d.]+) VND", dong)
    if m is None:
        print("Bo qua:", dong)
        continue
    ma, loai, so = m.groups()
    tien = int(so.replace(".", ""))
    tong = tong + tien
    print(ma, loai, tien)
print("Tong:", tong)''', "A0001 chuyen 500000\nA0002 rut 2000000\nBo qua: 09:03 LOI GD#A0003 timeout\nTong: 2500000")
P_FSTR = py("dinh_dang", '''tien = 1250000
ty_le = 0.0725
print(f"{tien:,}")
print(f"{tien * ty_le:,.2f}")
print(f"[{'A01':>6}] [{'A01':<6}]")
print(f"{ty_le:.2%}")''', "1,250,000\n90,625.00\n[   A01] [A01   ]\n7.25%")
measure("l04_redos", '''import json, re, time
res = {}
for n in (16, 20, 24):
    s = "a" * n + "c"
    t0 = time.perf_counter()
    re.match(r"(a+)+b", s)
    res["t_bad_%d" % n] = time.perf_counter() - t0
t0 = time.perf_counter()
for _ in range(2000):
    re.match(r"a+b", "a" * 24 + "c")
res["t_good_24"] = (time.perf_counter() - t0) / 2000
for n in (4000, 8000):
    s = "a" * n + "c"
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        re.search(r"a+b", s)
        best = min(best, time.perf_counter() - t0)
    res["t_lin_%d" % n] = best
print(json.dumps(res))''')

LAB_SOL = r'''import re
nhat_ky = [
    "10:15:02 GD#A0731 chuyen 1.250.000 VND tu A01 den A02",
    "10:15:09 GD#A0732 rut 500.000 VND tu A03",
    "10:16:40 GD#A0733 nap 12.000.000 VND vao A01",
    "10:17:01 LOI GD#A0734 timeout",
    "10:17:30 GD#A0735 chuyen 75.000 VND tu A02 den A03",
]
tong = 0
for dong in nhat_ky:
    ma = re.search(r"GD#(\w+)", dong)
    so = re.search(r"([\d.]+) VND", dong)
    if so is None:
        continue
    tien = int(so.group(1).replace(".", ""))
    tong = tong + tien
    print(ma.group(1), tien)
print("Tong:", tong)'''
LAB_OUT = "A0731 1250000\nA0732 500000\nA0733 12000000\nA0735 75000\nTong: 13825000"
P_LAB = py("lab_l04", LAB_SOL, LAB_OUT)


def build():
    b16, b20, b24 = M("l04_redos", "t_bad_16"), M("l04_redos", "t_bad_20"), M("l04_redos", "t_bad_24")
    g24 = M("l04_redos", "t_good_24")
    s16, s20, s24, sg = t_show(b16), t_show(b20), t_show(b24), t_show(g24)
    l4, l8 = M("l04_redos", "t_lin_4000"), M("l04_redos", "t_lin_8000")
    t4s, t8s = t2(l4), t2(l8)
    r48 = round(val2(l8) / val2(l4), 1)   # tỉ số thời gian khi chuỗi dài gấp đôi, từ chính hai số hiện trên màn hình
    s30 = t2(b24 * 2 ** 6)
    s40 = t2(b24 * 2 ** 16)
    sc_hook = sc("hook", "hook", "Một dòng nhật ký, hai cách bóc số tiền: một cách ra rác", [
        st(repl_block(R_HOOK, title="Dòng nhật ký: 09:01 GD#A0001 chuyen 500.000 VND")
           + "<p>Cách thứ nhất nhặt <b>mọi dãy chữ số</b>: giờ, phút, mã, số tiền bị cắt đôi. Cách thứ hai mô tả <b>hình dạng</b> mong muốn.</p>",
           """Chào bạn, ngân hàng ghi hàng triệu dòng nhật ký, mỗi dòng là một câu chữ, có giờ, mã giao dịch, loại và số tiền. Muốn cộng tổng tiền, ta phải bóc số tiền ra khỏi chữ. Cách ngây thơ là nhặt mọi dãy chữ số, và ta nhận một đống rác, giờ phút lẫn vào, số tiền bị cắt đôi ở dấu chấm.
           Cách tốt hơn là mô tả hình dạng của thứ ta cần, và máy trả đúng mã và số tiền."""),
        st(table(["cùng một kiểu viết mẫu, cố ý viết kém", "chuỗi dài", "thời gian một lần thử (đo trên máy kiểm, số minh hoạ)"],
                 [["chữ a lặp 16 lần rồi chữ c", "17 ký tự", s16[0]], ["chữ a lặp 24 lần rồi chữ c", "25 ký tự", s24[0]]])
           + "<p class='note'>ms = phần nghìn giây; µs = phần triệu giây; ns = phần tỉ giây (đơn vị dùng trong cả bài).</p>",
           f"""Nhưng công cụ này có một cái bẫy. Một mẫu viết kém có thể khiến máy bị treo. Với chuỗi mười bảy ký tự, một lần thử mất {s16[1]}. Chỉ thêm tám ký tự nữa, tức hai mươi lăm ký tự, mất {s24[1]}. Thời gian gấp đôi theo mỗi ký tự thêm vào.
           Hôm nay ta học cả cách bóc dữ liệu từ chữ, lẫn cách tránh cái bẫy này."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Cắt, tìm, thay, tách, ghép <b>chuỗi</b> và <b>định dạng số</b> ra sao?</li>
<li>Vì sao số ký tự khác số <b>byte</b>?</li>
<li>Mô tả hình dạng chuỗi bằng <b>biểu thức chính quy</b> thế nào, và khi nào mẫu viết kém làm máy treo?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, cắt, tìm, thay, tách, ghép chuỗi và định dạng số ra sao. Hai, vì sao số ký tự khác số byte. Ba, mô tả hình dạng chuỗi bằng biểu thức chính quy thế nào, và khi nào mẫu viết kém làm máy treo."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: chuỗi là dãy ký tự, chỉ số và cắt lát giống danh sách", [
        st(repl_block(R_PRE, title="Chuỗi dùng chỉ số và cắt lát như danh sách")
           + "<p>Chuỗi <code>\"GD#A0731\"</code> có $8$ ký tự; chỉ số bắt đầu từ $0$; lát <code>[3:]</code> lấy từ chỉ số $3$ tới hết.</p>",
           """Ta ôn lại hai điều. Chuỗi là một dãy ký tự, và dùng chỉ số, cắt lát giống danh sách. Mã giao dịch có tám ký tự, chỉ số bắt đầu từ không, và lát từ chỉ số ba đến hết cho phần mã tài khoản. Cộng hai chuỗi là nối chúng lại."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã các lệnh trên chuỗi, định dạng trong chuỗi và các ký tự của mẫu", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>s.split(\",\")</code>", "tách", "cắt <code>s</code> tại mỗi dấu <code>,</code> thành <b>danh sách</b> các mảnh"],
                  ["<code>\",\".join(ds)</code>", "ghép", "nối các chuỗi trong <code>ds</code>, đặt <code>,</code> ở giữa; ngược lại của tách"],
                  ["<code>s.find(x)</code>, <code>s.replace(a, b)</code>", "tìm vị trí, thay", "vị trí đầu của <code>x</code> (không có thì <code>-1</code>); chuỗi <b>mới</b> với <code>a</code> đổi thành <code>b</code>"],
                  ["<code>s.startswith(x)</code>, <code>s.strip()</code>", "bắt đầu bằng, cắt khoảng trắng", "đúng/sai; chuỗi mới bỏ khoảng trắng hai đầu"]]),
           """Bảng đầu là các lệnh gắn vào chuỗi. Lệnh tách cắt chuỗi tại mỗi dấu cho trước thành một danh sách các mảnh. Lệnh ghép làm ngược lại, nối các chuỗi với một dấu ở giữa. Lệnh tìm cho vị trí đầu tiên, hoặc âm một nếu không có. Lệnh thay cho ra chuỗi mới.
           Hai lệnh nữa kiểm xem chuỗi có bắt đầu bằng gì không, và bỏ khoảng trắng hai đầu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4", "1.5"]),
        st(table(["viết trong f\"…{…}…\"", "đọc là", "ví dụ với 1250000 và 0,0725"],
                 [["<code>{x:,}</code>", "ngăn hàng nghìn", "<code>1,250,000</code>"],
                  ["<code>{x:,.2f}</code>", "hai chữ số thập phân", "<code>90,625.00</code> với <code>1250000 * 0.0725</code>"],
                  ["<code>{s:&gt;6}</code>, <code>{s:&lt;6}</code>", "canh phải, canh trái, rộng 6", "<code>[   A01]</code>, <code>[A01   ]</code>"],
                  ["<code>{r:.2%}</code>", "phần trăm", "<code>7.25%</code> với <code>0.0725</code>"]]),
           """Bảng thứ hai là định dạng trong chuỗi có chỗ điền. Sau dấu hai chấm ta ghi cách hiển thị. Dấu phẩy ngăn hàng nghìn, giúp số tiền lớn dễ đọc hơn nhiều. Chữ f kèm số chữ số sau dấu thập phân cố định số chữ số lẻ. Dấu lớn hơn hay nhỏ hơn với một độ rộng canh phải hay canh trái. Và dấu phần trăm đổi tỉ lệ thành phần trăm.""",
           focus=[1, 1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>\\d</code>, <code>\\w</code>, <code>.</code>", "chữ số; chữ-hoặc-số-hoặc-gạch-dưới; ký tự bất kỳ (trừ xuống dòng)", "mỗi cái khớp <b>đúng một</b> ký tự thuộc loại đó"],
                  ["<code>+</code>, <code>*</code>, <code>?</code>", "một hoặc nhiều; không hoặc nhiều; không hoặc một", "đặt sau một mục để cho phép <b>lặp lại</b>: <code>\\d+</code> là một dãy chữ số"],
                  ["<code>[\\d.]</code>, <code>(…)</code>", "một ký tự trong tập; nhóm", "<code>[\\d.]+</code> khớp chữ số hoặc dấu chấm; <b>nhóm</b> trong ngoặc tròn là phần ta muốn lấy ra"],
                  ["<code>r\"…\"</code>", "chuỗi thô", "dấu gạch ngược <code>\\</code> được giữ nguyên, không bị hiểu là ký tự đặc biệt"]]),
           """Bảng thứ ba là các ký tự của mẫu mô tả hình dạng. Gạch ngược d khớp đúng một chữ số, gạch ngược w khớp một chữ cái, chữ số hoặc dấu gạch dưới, và dấu chấm khớp một ký tự bất kỳ, trừ xuống dòng. Dấu cộng, dấu sao, dấu hỏi đặt sau một mục cho phép lặp lại, một hoặc nhiều, không hoặc nhiều, không hoặc một.
           Cặp ngoặc vuông là một tập ký tự, cặp ngoặc tròn là nhóm, phần ta muốn lấy ra. Và chuỗi thô giữ nguyên dấu gạch ngược.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>import re</code>", "nạp bộ công cụ", "mang bộ công cụ biểu thức chính quy có sẵn của ngôn ngữ vào chương trình"],
                  ["<code>re.search(mẫu, s)</code>", "tìm lần khớp đầu", "trả về đối tượng khớp, hoặc <code>None</code> nếu không khớp"],
                  ["<code>re.findall(mẫu, s)</code>", "tìm mọi lần khớp", "trả về danh sách các mảnh khớp"],
                  ["<code>m.group()</code>, <code>m.group(1)</code>, <code>m.groups()</code>", "lấy phần khớp, lấy nhóm", "cả phần khớp; nhóm thứ 1; bộ mọi nhóm"]]),
           """Bảng cuối là bốn lệnh của bộ công cụ biểu thức chính quy. Lệnh nạp mang bộ công cụ vào chương trình. Lệnh tìm lần khớp đầu trả về một đối tượng khớp, hoặc giá trị rỗng nếu không khớp. Lệnh tìm mọi lần khớp trả về danh sách. Và các lệnh lấy kết quả cho cả phần khớp, một nhóm, hoặc mọi nhóm.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một ký tự có thể là nhiều byte; mẫu trượt trên dòng chữ", [
        st(svg(1500, 420,
               txt(750, 40, "chuỗi \"tiền\": 4 ký tự", 30, "middle", "#1f2937", True),
               box(230, 70, 160, 80, ["t"], C_BLUE, 34, True), box(400, 70, 160, 80, ["i"], C_BLUE, 34, True),
               box(570, 70, 360, 80, ["ề"], C_AMBER, 34, True), box(940, 70, 160, 80, ["n"], C_BLUE, 34, True),
               box(230, 190, 160, 70, ["74"], C_GRAY, 28, True), box(400, 190, 160, 70, ["69"], C_GRAY, 28, True),
               box(570, 190, 110, 70, ["e1"], C_GRAY, 28, True), box(690, 190, 110, 70, ["bb"], C_GRAY, 28, True), box(810, 190, 120, 70, ["81"], C_GRAY, 28, True),
               box(940, 190, 160, 70, ["6e"], C_GRAY, 28, True),
               txt(160, 235, "byte:", 26, "end", "#6b7280", True),
               txt(750, 310, "1 byte + 1 byte + 3 byte + 1 byte = 6 byte, trong khi chỉ có 4 ký tự", 28, "middle", "#dc2626", True),
               txt(750, 355, "UTF-8: chữ không dấu 1 byte; chữ có dấu tiếng Việt 2 hoặc 3 byte", 26, "middle", "#1f2937"),
               txt(750, 398, "mỗi byte viết ở hệ 16: hai ký tự gồm chữ số 0–9 và chữ cái a–f (74 là chữ t)", 24, "middle", "#6b7280")),
           """Hình này giải thích vì sao số ký tự khác số byte, chuỗi tiền có bốn ký tự. Nhưng bộ nhớ lưu byte, và quy ước mã hoá phổ biến nhất dùng một byte cho chữ không dấu, còn chữ có dấu tiếng Việt cần hai hoặc ba byte. Chữ e có dấu mũ và dấu huyền ở đây cần ba byte.
           Mỗi byte là một số, viết ở hệ mười sáu bằng hai ký tự gồm chữ số và chữ cái a đến f. Cộng lại, bốn ký tự thành sáu byte. Vì thế khi đo độ dài trong bộ nhớ hay trên đường truyền, phải nói rõ đếm ký tự hay đếm byte."""),
        st(svg(1500, 400,
               txt(750, 40, "dòng nhật ký, đặt mẫu trượt từ trái sang phải", 28, "middle", "#1f2937", True),
               box(30, 70, 150, 70, ["10:15"], C_GRAY, 26), box(190, 70, 360, 70, ["GD#", "A0731"], C_BLUE, 26, True),
               box(560, 70, 190, 70, ["chuyen"], C_GREEN, 26, True), box(760, 70, 230, 70, ["1250000"], C_AMBER, 26, True), box(1000, 70, 130, 70, ["VND"], C_GRAY, 26),
               txt(370, 185, "nhóm 1: \\w+", 26, "middle", "#2a78d6", True),
               txt(655, 185, "nhóm 2: \\w+", 26, "middle", "#16a34a", True),
               txt(875, 185, "nhóm 3: \\d+", 26, "middle", "#d97706", True),
               txt(750, 270, "mẫu:  GD#(\\w+) (\\w+) (\\d+)", 34, "middle", "#1f2937", True),
               txt(750, 330, "chữ GD# và các dấu cách phải khớp NGUYÊN VĂN; ngoặc tròn đánh dấu phần ta lấy ra", 26, "middle", "#1f2937"),
               txt(750, 375, "không khớp ở chỗ nào thì máy thử lại từ ký tự kế tiếp, cho tới hết dòng", 24, "middle", "#6b7280")),
           """Hình thứ hai là mẫu trượt trên dòng chữ. Mẫu gồm phần chữ phải khớp nguyên văn, như chữ G D và dấu thăng, cùng các nhóm đặt trong ngoặc tròn. Máy trượt mẫu từ trái sang phải. Chỗ nào khớp đủ thì dừng, và các nhóm là các mảnh ta lấy ra, ở đây mã, loại và số tiền.
           Không khớp ở chỗ nào thì máy thử lại từ ký tự kế tiếp, cho tới hết dòng.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: chuỗi không sửa được, tách và ghép, đếm byte, dựng mẫu", [
        st(repl_block(R_FIX, 0, 5, title="Bước 1. Chuỗi KHÔNG sửa tại chỗ: mọi lệnh cho chuỗi mới")
           + "<p>Vì chuỗi <b>bất biến</b>, <code>s.upper()</code> trả chuỗi mới và <code>s</code> vẫn nguyên; gán vào <code>s[0]</code> bị chặn. Muốn đổi, dựng chuỗi mới: <code>\"C\" + s[1:]</code>.</p>",
           """Bước một, chuỗi không sửa tại chỗ. Vì chuỗi là bất biến, lệnh viết hoa trả về một chuỗi mới, còn chuỗi cũ vẫn nguyên. Gán thẳng vào một vị trí của chuỗi bị máy chặn bằng một lỗi kiểu. Muốn đổi, ta dựng chuỗi mới, ví dụ ghép chữ C hoa với phần còn lại từ chỉ số một."""),
        st("<div class='box key'><b>Lưu ý về phiên bản.</b> Cách <b>hiển thị</b> lỗi khác nhau giữa Python 3.11 và 3.13, ở cả hai nơi chạy: cửa sổ <code>&gt;&gt;&gt;</code> của 3.13 in <code>&lt;python-input-N&gt;</code> kèm dòng mã và dấu <code>~^</code>; chạy tệp <code>.py</code> (cả 3.11 và 3.13) in đường dẫn tệp, dòng mã và dấu <code>~^</code> ở mỗi tầng. <b>Dòng cuối</b> (tên lỗi và nội dung) <b>giống nhau</b> ở mọi bản.</div>",
           """Lưu ý về phiên bản. Cách hiển thị lỗi khác nhau giữa các bản, ở cả cửa sổ gõ lệnh lẫn khi chạy tệp, nên hình trên máy bạn có thể có thêm dòng mã và dấu mũ so với video. Dòng cuối, nói tên lỗi và nội dung, thì giống nhau ở mọi bản.""", clear=True),
        st(repl_block(R_SPLIT, 0, 5, title="Bước 2. Tách rồi ghép lại với cùng dấu thì được chuỗi cũ")
           + "<p>Vì tách cắt tại mỗi dấu <code>,</code> và ghép đặt lại đúng dấu <code>,</code> ở giữa, <code>\",\".join(dong.split(\",\")) == dong</code> luôn đúng.</p>",
           """Bước hai, tách và ghép. Tách chuỗi tại mỗi dấu phẩy được danh sách ba mảnh. Ghép lại bằng dấu gạch đứng cho chuỗi khác. Vì tách cắt tại dấu phẩy và ghép đặt đúng dấu phẩy đó vào giữa, ghép bằng dấu phẩy trả lại đúng chuỗi ban đầu. Đây là một phép thử hữu ích.""", clear=True),
        st(repl_block(R_UTF, 0, 5, title="Bước 3. Số ký tự khác số byte")
           + "<p><code>.encode(\"utf-8\")</code> đổi chuỗi thành <b>các byte</b> (<code>b'…'</code>; <code>\\xe1</code> là một byte viết ở hệ $16$); <code>.decode(\"utf-8\")</code> đổi ngược. Vì chữ <code>ề</code> chiếm $3$ byte: $1 + 1 + 3 + 1 = 6$ byte.</p>",
           """Bước ba, đếm byte. Lệnh mã hoá đổi chuỗi thành các byte, và lệnh giải mã đổi ngược lại. Chuỗi tiền có bốn ký tự, nhưng chữ có dấu chiếm ba byte, nên tổng là một cộng một cộng ba cộng một, bằng sáu byte.
           Mã hoá rồi giải mã cùng một quy ước thì trả lại chuỗi cũ. Nếu giải mã bằng quy ước khác, ta nhận các ký tự hỏng.""", clear=True),
        st(repl_block(R_RE, 0, 4, title="Bước 4a. Dựng mẫu từ thô đến tinh")
           + "<p>Vì <code>\\d+</code> nhặt <b>mọi</b> dãy số nên có rác; thêm <code> VND</code> ép dãy số phải đứng <b>ngay trước</b> chữ VND; <code>.group()</code> không đối số trả <b>cả phần khớp</b>.</p>",
           """Bước bốn, dựng mẫu từ thô đến tinh. Ta nạp bộ công cụ và gán một dòng nhật ký. Vì gạch ngược d cộng nhặt mọi dãy số nên lẫn giờ và phút. Thêm chữ đơn vị tiền phía sau ép dãy số phải đứng ngay trước chữ đó, và lấy phần khớp không đối số cho cả cụm số tiền.""", clear=True),
        st(repl_block(R_RE, 4, 8, title="Bước 4b. Nhóm: lấy riêng từng mảnh (tiếp phiên trên)")
           + "<p>Bọc <code>(\\d+)</code> trong ngoặc để lấy riêng; thêm <code>GD#(\\w+) (\\w+) </code> ở đầu để lấy cả mã và loại: <code>m.groups()</code> là bộ ba nhóm, <code>m.group(3)</code> là nhóm thứ ba.</p>",
           """Rồi ta thêm mẫu cho mã và loại ở đầu, và bọc từng phần trong ngoặc tròn. Vì ngoặc tròn đánh dấu phần cần lấy, ta lấy được cả ba nhóm cùng lúc, mã A không bảy ba một, loại chuyển và số tiền, hoặc riêng nhóm thứ ba. Nếu dòng không khớp, kết quả là rỗng.""", clear=True),
    ], checks=["',' .join('A01,chuyen,500000'.split(',')) == 'A01,chuyen,500000'" .replace("' .join", "'.join"),
               "len('tiền') == 4 and len('tiền'.encode('utf-8')) == 6 and 1 + 1 + 3 + 1 == 6",
               "'tiền'.encode('utf-8') == b'ti\\xe1\\xbb\\x81n'"])
    sc_ex = sc("example", "example", "Ví dụ: đọc nhật ký, bóc mã và số tiền, bỏ dòng lỗi, cộng tổng", [
        st(code_block(P_LOG, lines=(1, 6), title="Tệp nhat_ky.py, phần dữ liệu"),
           """Ta ráp lại thành một chương trình. Nạp bộ công cụ biểu thức chính quy. Có ba dòng nhật ký, dòng cuối là dòng lỗi không có số tiền."""),
        st(code_block(P_LOG, lines=(7, 17), title="Phần xử lý")
           + "<p><code>m is None</code>: <code>is</code> hỏi “đúng là cùng một thứ không”, <code>None</code> là “không có gì”, nên dòng này hỏi “không khớp phải không?”. <code>continue</code>: bỏ phần còn lại của lượt này, sang dòng nhật ký kế.</p>",
           """Với mỗi dòng, tìm mẫu gồm mã, loại và số tiền có thể chứa dấu chấm. Từ hỏi đúng là cùng một thứ, đứng cạnh giá trị rỗng, nghĩa là hỏi mẫu có không khớp không. Nếu không khớp thì in một thông báo, rồi lệnh bỏ lượt này nhảy sang dòng kế. Nếu khớp thì mở gói ba nhóm, bỏ dấu chấm ngăn hàng nghìn, đổi sang số nguyên, rồi cộng vào tổng.""", clear=True),
        st(out_block(P_LOG) + "<p>Dòng $1$: $500.000 \\to 500\\,000$. Dòng $2$: $2.000.000 \\to 2\\,000\\,000$. Dòng $3$ không có <code>VND</code> nên <code>re.search</code> trả <code>None</code> và bị bỏ qua: tổng $2\\,500\\,000$.</p>",
           """Kết quả khớp cách ta nghĩ. Hai dòng đầu cho năm trăm nghìn và hai triệu. Dòng thứ ba bị bỏ qua vì không khớp mẫu. Tổng là hai triệu rưỡi. Chú ý ta kiểm kết quả không khớp trước khi dùng nhóm, vì lấy nhóm từ giá trị rỗng sẽ gây lỗi.""", clear=True),
        st(run_block(P_FSTR, title="In kết quả cho người đọc: định dạng số"),
           """Cuối cùng là in số cho người đọc. Số một triệu hai trăm năm mươi nghìn ngăn hàng nghìn bằng dấu phẩy. Số tiền nhân tỉ lệ in với hai chữ số thập phân. Hai chuỗi canh phải và canh trái trong độ rộng sáu. Và tỉ lệ không phẩy không bảy hai lăm hiện thành bảy phẩy hai lăm phần trăm.""", clear=True),
    ], checks=["500000 + 2000000 == 2500000", "int('500.000'.replace('.', '')) == 500000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: bóc bằng thay-và-ép-kiểu, và cộng tay", [
        st(repl_block(R_KIEM, title="Không dùng mẫu: bỏ dấu chấm rồi đổi sang số nguyên, cộng tay")
           + "<p>Vì dấu chấm chỉ ngăn hàng nghìn, bỏ nó rồi đổi kiểu cho đúng giá trị. Hai số $500\\,000 + 2\\,000\\,000 = 2\\,500\\,000$ trùng tổng của chương trình ✓</p>",
           """Đường kiểm khác, không dùng mẫu. Vì dấu chấm chỉ ngăn hàng nghìn, ta bỏ nó rồi đổi sang số nguyên cho từng số tiền, và cộng tay. Hai số năm trăm nghìn và hai triệu cộng lại đúng hai triệu rưỡi, trùng tổng của chương trình. Hai đường độc lập cùng ra một con số."""),
    ], checks=["500000 + 2000000 == 2500000"])
    sc_scale = sc("scale", "concept", "Khi chuỗi dài ra: mẫu viết kém tốn thời gian gấp đôi theo mỗi ký tự", [
        st(table(["độ dài chuỗi thử", "mẫu viết kém: (a+)+b", "mẫu viết tốt: a+b"],
                 [["17 ký tự", s16[0], "—"], ["21 ký tự", s20[0], "—"], ["25 ký tự", s24[0], sg[0] + " (với 25 ký tự)"],
                  ["31 ký tự (ngoại suy)", s30[0] + " (gấp đôi mỗi ký tự)", "vẫn gần như tức thì"], ["41 ký tự (ngoại suy)", s40[0], "vẫn gần như tức thì"]])
           + "<p class='note'><b>Ngoại suy</b> = nhân theo quy luật đã đo để đoán quy mô lớn hơn (ước lượng, chưa đo).</p>",
           f"""Bảng này cho thấy cái bẫy rất rõ qua thời gian chạy của từng độ dài. Với mẫu viết kém, mười bảy ký tự mất {s16[1]}. Hai mươi mốt ký tự mất {s20[1]}, hai mươi lăm ký tự mất {s24[1]}. Mẫu viết tốt cùng làm một việc chỉ mất {sg[1]}.
           Ngoại suy, tức nhân theo quy luật gấp đôi mỗi ký tự đã đo, cho ba mươi mốt ký tự mất {s30[1]}, bốn mươi mốt ký tự mất {s40[1]}. Các số này đo trên máy kiểm, số minh hoạ."""),
        st("<div class='box key'><b>Đánh đổi:</b> mẫu có <b>lặp lồng lặp</b> như <code>(a+)+</code> buộc máy thử mọi cách chia chuỗi, nên thời gian tăng <b>theo hàm mũ</b>: gấp đôi mỗi ký tự thêm vào.</div>"
           + f"<div class='box key'>Mẫu tương đương không lồng lặp, <code>a+b</code>, không bùng nổ gấp đôi mỗi ký tự: ở chuỗi ngắn gần như tức thì. Ở chuỗi dài hàng nghìn ký tự không khớp, nó vẫn chậm dần nhanh hơn tỉ lệ vì thử từng vị trí đầu (đo: 4 000 ký tự {t4s[0]}, 8 000 ký tự {t8s[0]}: chuỗi dài gấp đôi, thời gian gấp cỡ {str(r48).replace('.', ',')} lần, tức tăng theo bình phương độ dài; số minh hoạ theo máy), nhưng vẫn nhanh hơn rất xa mẫu viết kém ở cùng chuỗi dài.</div>"
           + "<p>Với dữ liệu lấy từ bên ngoài, mẫu viết kém là lỗ hổng làm treo hệ thống.</p>",
           f"""Nguyên nhân là mẫu có lặp lồng trong lặp buộc máy thử mọi cách chia chuỗi, nên thời gian tăng theo hàm mũ, gấp đôi mỗi ký tự. Mẫu viết tốt thì không bùng nổ như vậy. Nhưng trên chuỗi dài hàng nghìn ký tự nó vẫn chậm dần nhanh hơn tỉ lệ, vì phải thử từng vị trí đầu. Trên máy kiểm, chuỗi dài gấp đôi thì thời gian gấp cỡ {vi_num(r48)} lần.
           Với dữ liệu lấy từ bên ngoài, một mẫu viết kém là lỗ hổng làm treo hệ thống.""", clear=True),
    ], checks=["2 ** 6 == 64 and 2 ** 16 == 65536", "len('a' * 16 + 'c') == 17 and len('a' * 24 + 'c') == 25"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Dấu <code>.*</code> tham lam: lấy nhiều nhất có thể.</div>'
           + repl_block(R_GREEDY, 0, 3) + "<p>Mẫu <code>&lt;(.*)&gt;</code> chạy tới dấu <code>&gt;</code> <b>cuối cùng</b>. Thêm <code>?</code> sau <code>*</code> để lấy <b>ít nhất</b>: dừng ở dấu <code>&gt;</code> đầu tiên. Phép thử: in nhóm lấy được và so với điều mong đợi.</p>",
           """Lỗi thứ nhất, của người mới, là mẫu tham lam. Dấu chấm sao lấy nhiều nhất có thể, nên mẫu trong cặp dấu nhỏ hơn lớn hơn chạy tới dấu lớn hơn cuối cùng. Thêm dấu hỏi sau dấu sao thì nó lấy ít nhất, dừng ở dấu lớn hơn đầu tiên. Phép thử là in nhóm lấy được và so với điều mong đợi."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Đọc số kiểu Việt bằng kiểu số của máy.</div>'
           + repl_block(R_NUM) + "<p>Trong tiếng Việt <code>1.250</code> thường là <b>một nghìn hai trăm năm mươi</b>; máy hiểu là $1{,}25$. Không báo lỗi. Phép thử: <b>so với số liệu mẫu đã biết đáp án</b>; quy ước dấu chấm/phẩy phải ghi rõ trong định dạng dữ liệu.</p>",
           """Lỗi thứ hai, của người đã đi làm, là đọc số kiểu Việt bằng kiểu số của máy. Trong tiếng Việt, một chấm hai năm không thường là một nghìn hai trăm năm mươi. Máy hiểu đó là một phẩy hai lăm, và không báo lỗi gì. Cách phòng là bỏ dấu ngăn hàng nghìn trước khi đổi kiểu, và so với một số liệu mẫu đã biết đáp án.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người mới).</b> Tưởng sửa được một ký tự của chuỗi.</div>'
           + repl_block(R_FIX3) + "<p>Đọc dòng cuối: chuỗi không cho gán vào một vị trí. Dựng chuỗi mới, như bước $1$ ở trên.</p>",
           """Lỗi thứ ba, của người mới, là tưởng sửa được một ký tự của chuỗi. Máy báo lỗi và dòng cuối nói rõ chuỗi không cho gán vào một vị trí. Cách đúng là dựng chuỗi mới, như ta đã làm ở bước một.""", clear=True),
    ], checks=["'a><b' != 'a'", "float('1.250') == 1.25 and int('1.250'.replace('.', '')) == 1250"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b></p>
<ol><li><code>"A01,chuyen".split(",")[1].upper()</code> cho gì?</li>
<li><code>"đồng"</code> có mấy ký tự, mấy byte (UTF-8)? (chữ <code>đ</code>: 2 byte; <code>ồ</code>: 3 byte)</li></ol>
<p><b>Quyết định:</b> dòng nhật ký luôn dạng <code>mã,loại,tiền</code> ngăn bằng dấu phẩy: dùng <b>tách</b> hay <b>biểu thức chính quy</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Câu một, tách chuỗi tại dấu phẩy, lấy phần tử có chỉ số một rồi viết hoa, cho gì. Câu hai, chữ đồng có mấy ký tự và mấy byte, biết chữ đ hai byte, chữ ồ ba byte.
           Sau đó là một quyết định, dòng nhật ký luôn dạng mã, loại, tiền ngăn bằng dấu phẩy, dùng lệnh tách hay biểu thức chính quy, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_QUIZ, 0, 3, title="Câu 1 và câu 2")
           + "<p>Tách được <code>['A01', 'chuyen']</code>, chỉ số $1$ là <code>chuyen</code>, viết hoa: <code>CHUYEN</code>. Ký tự: $4$. Byte: $2 + 3 + 1 + 1 = 7$ (<code>đ</code>, <code>ồ</code>, <code>n</code>, <code>g</code>).</p>",
           """Đáp án như sau. Tách được hai mảnh, chỉ số một là chữ chuyển khoản, viết hoa thành chữ hoa. Chữ đồng có bốn ký tự. Số byte là hai cộng ba cộng một cộng một, bằng bảy."""),
        st("<div class='box key'><b>Quyết định:</b> dùng <b>tách</b>. Khi định dạng cố định và đơn giản, tách ngắn hơn, dễ đọc hơn và không có nguy cơ mẫu viết kém. "
           "Dùng biểu thức chính quy khi hình dạng <b>thay đổi</b> (số cột không cố định, dấu cách thừa, dòng lỗi lẫn vào) và luôn tránh lặp lồng lặp.</div>",
           """Quyết định, nên dùng lệnh tách. Khi định dạng cố định và đơn giản, tách ngắn hơn, dễ đọc hơn và không có nguy cơ mẫu viết kém. Dùng biểu thức chính quy khi hình dạng thay đổi, như số cột không cố định hay dòng lỗi lẫn vào, và luôn tránh lặp lồng trong lặp.""", clear=True),
    ], checks=["'A01,chuyen'.split(',')[1].upper() == 'CHUYEN'", "len('đồng') == 4 and len('đồng'.encode('utf-8')) == 7 and 2 + 3 + 1 + 1 == 7"])
    sc_prac = practice_scene(sc, "Tự làm: trích mã và số tiền từ dòng nhật ký", pr_steps(
        st, "PYT", "L04",
        """<p><b>Đề</b>: tạo <code>trich_log.py</code>. Chép dòng đầu <code>nhat_ky = [ … ]</code> (5 dòng, xem <code>de.md</code>), ví dụ <code>"10:15:09 GD#A0732 rut 500.000 VND tu A03"</code>.</p>
<ol><li>Mỗi dòng <b>có</b> số tiền: in <code>mã số_tiền</code> (số nguyên, bỏ dấu chấm); dòng lỗi (không có <code>VND</code>) thì bỏ qua;</li>
<li>Cuối cùng in <code>Tong: …</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Chép danh sách năm dòng nhật ký từ tệp đề bài. Mỗi dòng có số tiền, in mã giao dịch và số tiền đã bỏ dấu chấm, đổi sang số nguyên. Dòng lỗi không có số tiền thì bỏ qua. Cuối cùng in tổng.
        Dùng hai mẫu, một cho mã và một cho số tiền. Hãy dừng video và làm.""",
        LAB_OUT, "trich_log.py",
        """<div class="box key"><b>Nếu kẹt:</b> mã: <code>re.search(r"GD#(\\w+)", dong)</code>; số tiền: <code>re.search(r"([\\d.]+) VND", dong)</code>. Nếu <code>None</code> thì <code>continue</code>. Rồi <code>so.group(1).replace(".", "")</code> và <code>int(...)</code>.
Lời giải ở <code>labs/PYT/L04/loi_giai.py</code>.</div>""",
        """Nếu kẹt, dùng một mẫu cho mã, với nhóm là chữ và số sau dấu thăng, và một mẫu cho số tiền, với nhóm là chữ số và dấu chấm đứng trước chữ đơn vị tiền. Nếu mẫu số tiền không khớp thì bỏ qua dòng. Rồi bỏ dấu chấm và đổi sang số nguyên.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L04")
    write_lab("PYT", "L04", """# Lab PYT L04 — Trích mã và số tiền từ nhật ký

Cần: Python 3.11 trở lên. Tạo `trich_log.py`. Dữ liệu (chép nguyên; minh hoạ, khác ví dụ trong bài):

```python
nhat_ky = [
    "10:15:02 GD#A0731 chuyen 1.250.000 VND tu A01 den A02",
    "10:15:09 GD#A0732 rut 500.000 VND tu A03",
    "10:16:40 GD#A0733 nap 12.000.000 VND vao A01",
    "10:17:01 LOI GD#A0734 timeout",
    "10:17:30 GD#A0735 chuyen 75.000 VND tu A02 den A03",
]
```

1. Với mỗi dòng **có** số tiền (mẫu `[\\d.]+ VND`): in `<mã> <số tiền>` — mã là phần sau `GD#`, số tiền là **số nguyên** (bỏ dấu chấm ngăn hàng nghìn). Dòng lỗi (không có `VND`) thì bỏ qua.
2. Cuối cùng in `Tong: <tổng>`.

Dùng `import re`. Chạy: `python trich_log.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L04 trich_log.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("chuỗi bất biến: lệnh nào cũng cho chuỗi mới", "tách và ghép là hai phép ngược nhau", "ký tự ≠ byte: UTF-8 dùng 1–3 byte cho chữ Việt",
                 "mẫu: nhóm trong ngoặc, lặp bằng + * ?", "tham lam lấy nhiều nhất; thêm ? để lấy ít nhất", "lặp lồng lặp làm thời gian tăng gấp đôi mỗi ký tự"),
           """Tổng kết chuỗi logic. Chuỗi bất biến, lệnh nào cũng cho chuỗi mới. Tách và ghép là hai phép ngược nhau. Ký tự khác byte, vì mã hoá dùng một đến ba byte cho chữ Việt. Mẫu dùng nhóm trong ngoặc và các dấu lặp.
           Dấu chấm sao tham lam, thêm dấu hỏi để lấy ít nhất. Và lặp lồng trong lặp làm thời gian tăng gấp đôi theo mỗi ký tự."""),
        st("""<div class='box key'><b>Tư duy:</b> dữ liệu dạng chữ thì <b>mô tả hình dạng</b> thứ cần lấy, <b>kiểm</b> kết quả không khớp trước khi dùng, và thử với dòng lỗi. Mẫu nhận dữ liệu từ bên ngoài phải được thử với đầu vào xấu nhất.</div>
<p>Bài sau: đọc và ghi tệp, CSV và JSON, để dữ liệu vào ra khỏi chương trình.</p>""",
           """Điều cần mang theo, với dữ liệu dạng chữ hãy mô tả hình dạng thứ cần lấy, kiểm kết quả không khớp trước khi dùng, và thử với dòng lỗi. Mẫu nhận dữ liệu từ bên ngoài phải được thử với đầu vào xấu nhất.
           Bài sau, ta học đọc và ghi tệp, các định dạng bảng và dữ liệu có cấu trúc, để dữ liệu vào ra khỏi chương trình.""", forward_ref=True),
    ])
    return lesson("L04", "chuoi_va_bieu_thuc_chinh_quy", "Bài 4 — Chuỗi và biểu thức chính quy: đọc dữ liệu dạng chữ",
                  "curriculum/pyt.yaml L04; audit/pyt/verify_pyt.py L04 (chạy thật trên Python 3.11 và 3.13; thời gian mẫu viết kém đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy gấp đôi mỗi ký tự); "
                  "Python Tutorial §3.1.2 (Text), Library Reference §4.7 (Text Sequence Type, str methods), Format Specification Mini-Language, Regular Expression HOWTO, RFC 3629 (UTF-8); "
                  "OWASP về ReDoS (Regular expression Denial of Service) — chỉ nêu khái niệm; dữ liệu nhật ký là minh hoạ",
                  ["Cắt, tìm, thay, tách và ghép chuỗi bằng các lệnh trên chuỗi",
                   "Định dạng số trong chuỗi có chỗ điền: ngăn hàng nghìn, số chữ số thập phân, canh lề, phần trăm",
                   "Giải thích vì sao số ký tự khác số byte trong UTF-8 và đếm cả hai",
                   "Viết biểu thức chính quy bằng search, findall và nhóm để bóc dữ liệu",
                   "Nêu thời gian của mẫu viết kém tăng thế nào theo độ dài chuỗi",
                   "Chỉ ra ba lỗi hay gặp: mẫu tham lam, đọc số kiểu Việt sai, sửa chuỗi tại chỗ",
                   "Viết chương trình trích mã và số tiền từ dòng nhật ký"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy"],
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "example"), (5, "scale"), (6, "pitfalls"), (7, "practice")])
