from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_a import t2, val2

R_LIST = repl("List", [
    ("gd = [450000, 12000000, 800000]", ""), ("gd[0]", "450000"), ("gd[-1]", "800000"), ("len(gd)", "3"),
    ("gd.append(30000000)", ""), ("gd", "[450000, 12000000, 800000, 30000000]"),
])
R_CAT = repl("CatLat", [("x = [10, 20, 30, 40, 50]", ""), ("x[1:3]", "[20, 30]"), ("x[:2]", "[10, 20]"), ("x[2:]", "[30, 40, 50]"), ("x[::2]", "[10, 30, 50]")])
R_EDIT = repl("SuaChiSo", [
    ("gd = [450000, 12000000, 800000]", ""), ("gd[0] = 500000", ""), ("gd", "[500000, 12000000, 800000]"),
    ("tk = (450000, 12000000, 800000)", ""),
    ("tk[0] = 500000", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nTypeError: \'tuple\' object does not support item assignment'),
])
R_TAPHOP = repl("TapHopTuDien", [
    ('s = {"nap", "rut"}', ""), ('"nap" in s', "True"), ('s.add("nap")', ""), ("len(s)", "2"),
    ('d = {"A01": 5}', ""), ('d["A02"] = 3', ""), ('d.get("A09", 0)', "0"),
])
R_DICT = repl("Dict", [
    ('d = {"A01": 5, "A02": 3}', ""), ('d["A01"]', "5"), ('d["A03"] = 1', ""), ("d", "{'A01': 5, 'A02': 3, 'A03': 1}"),
    ('"A02" in d', "True"), ('d.get("A09", 0)', "0"),
])
R_SET = repl("Set", [('s = {"nap", "rut"}', ""), ('"nap" in s', "True"), ('s.add("nap")', ""), ("len(s)", "2"), ("type({})", "<class 'dict'>")])
R_SORT = repl("Sort", [
    ('gd = [("A01", 500000), ("A02", 150000), ("A03", 900000)]', ""),
    ("sorted(gd, key=lambda g: g[1])", "[('A02', 150000), ('A01', 500000), ('A03', 900000)]"),
    ("sorted(gd, key=lambda g: g[1], reverse=True)[0]", "('A03', 900000)"),
])
R_COMP = repl("Comp", [
    ("xs = [450000, 12000000, 800000, 30000000]", ""), ("[x // 1000 for x in xs]", "[450, 12000, 800, 30000]"),
    ("[x for x in xs if x >= 1000000]", "[12000000, 30000000]"), ("{x: x * 2 for x in range(3)}", "{0: 0, 1: 2, 2: 4}"),
])
R_CHECK = repl("Kiem", [
    ('loai = ["chuyen", "nap", "rut", "chuyen", "chuyen", "nap"]', ""), ('loai.count("chuyen")', "3"),
    ("len(loai)", "6"), ("3 + 2 + 1", "6"),
])
R_QUIZ = repl("Quiz", [("x = [10, 20, 30, 40, 50]", ""), ("x[-2:]", "[40, 50]"), ("x[1:4]", "[20, 30, 40]"), ("len(x[1:4])", "3")])

P_DEM = py("dem_tan_suat", '''loai = ["chuyen", "nap", "rut", "chuyen", "chuyen", "nap"]
dem = {}
for l in loai:
    dem[l] = dem.get(l, 0) + 1
print(dem)''', "{'chuyen': 3, 'nap': 2, 'rut': 1}")
P_GOP = py("gop_theo_khoa", '''ten = {"A01": "Lan", "A02": "Minh"}
giao_dich = [("A02", 300000), ("A01", 500000), ("A02", 250000)]
tong = {}
for ma, tien in giao_dich:
    tong[ma] = tong.get(ma, 0) + tien
for ma in sorted(tong):
    print(ten[ma], tong[ma])''', "Lan 500000\nMinh 550000")
P_XEP = py("xep_theo_tong", '''tong = {"A01": 500000, "A02": 550000, "A03": 120000}
xep = sorted(tong, key=lambda m: tong[m], reverse=True)
print(xep)
print(xep[:2])''', "['A02', 'A01', 'A03']\n['A02', 'A01']")
P_ALIAS = py("bi_danh", '''goc = [100000, 200000]
ban_sao = goc
ban_sao.append(300000)
print(goc)
doc_lap = goc[:]
doc_lap.append(400000)
print(goc)
print(doc_lap)''', "[100000, 200000, 300000]\n[100000, 200000, 300000]\n[100000, 200000, 300000, 400000]")
P_ALIAS_IS = py("bi_danh_is", '''goc = [100000, 200000]
ban_sao = goc
ban_sao.append(300000)
print(goc)
print(goc is ban_sao)''', "[100000, 200000, 300000]\nTrue")
P_NONG = py("sao_chep_nong", '''bang = [[1, 2], [3, 4]]
nong = bang[:]
nong[0].append(9)
print(bang)''', "[[1, 2, 9], [3, 4]]")
P_LAPXOA = py("sua_khi_lap", '''gd = [5, 0, 0, 7, 0]
for x in gd:
    if x == 0:
        gd.remove(x)
print(gd)
gd = [5, 0, 0, 7, 0]
gd = [x for x in gd if x != 0]
print(gd)''', "[5, 7, 0]\n[5, 7]")
P_KEYERR = py("thieu_khoa", '''so_gd = {"A01": 5, "A02": 3}
print(so_gd["A01"])
print(so_gd["A09"])''', "5", expect="error:KeyError", err="KeyError: 'A09'")
measure("l03_lookup", '''import json, time, tracemalloc
res = {}
for k, n in (("1e3", 1000), ("1e6", 1000000)):
    data = list(range(n))
    t0 = time.perf_counter()
    for q in range(200):
        _ = (-1 - q) in data
    res["t_list_" + k] = (time.perf_counter() - t0) / 200
    s = set(data)
    t0 = time.perf_counter()
    for q in range(200000):
        _ = (-1 - q) in s
    res["t_set_" + k] = (time.perf_counter() - t0) / 200000
tracemalloc.start()
data = list(range(1000000))
res["m_list_1e6"] = tracemalloc.get_traced_memory()[0]
tracemalloc.stop()
tracemalloc.start()
s = set(range(1000000))
res["m_set_1e6"] = tracemalloc.get_traced_memory()[0]
tracemalloc.stop()
print(json.dumps(res))''')

LAB_SOL = '''giao_dich = [("A02", 500000), ("A01", 200000), ("A03", 950000), ("A02", 150000), ("A01", 700000), ("A02", 50000)]
ten = {"A01": "Hoa", "A02": "Nam", "A03": "Linh"}
dem = {}
tong = {}
for ma, tien in giao_dich:
    dem[ma] = dem.get(ma, 0) + 1
    tong[ma] = tong.get(ma, 0) + tien
for ma in sorted(dem):
    print(ma, dem[ma], tong[ma])
for ma in sorted(tong, key=lambda m: tong[m], reverse=True):
    print(ten[ma], tong[ma])'''
LAB_OUT = "A01 2 900000\nA02 3 700000\nA03 1 950000\nLinh 950000\nHoa 900000\nNam 700000"
P_LAB = py("lab_l03", LAB_SOL, LAB_OUT)


def build():
    L3, L6 = M("l03_lookup", "t_list_1e3"), M("l03_lookup", "t_list_1e6")
    S3, S6 = M("l03_lookup", "t_set_1e3"), M("l03_lookup", "t_set_1e6")
    ml, ms = M("l03_lookup", "m_list_1e6"), M("l03_lookup", "m_set_1e6")
    tL3, tL6, tS3, tS6 = t2(L3), t2(L6), t2(S3), t2(S6)
    tot_l6 = t2(L6 * 1000)        # 1000 lần tra
    tot_s6 = t2(S6 * 1000)
    tot_l8 = t2(L6 * 100 * 1000)  # ngoại suy: danh sách 100 lần dài hơn, 1000 lần tra
    bl, bs = b_show(ml), b_show(ms)
    ratio = round(val2(L6) / val2(S6))
    sc_hook = sc("hook", "hook", "Một nghìn lần hỏi “mã này đã xử lý chưa?” trên một triệu mã", [
        st(table(["cách lưu một triệu mã đã xử lý", "một lần hỏi “có trong đó không?”", "1 000 lần hỏi (số đo trên máy kiểm, số minh hoạ)"],
                 [["danh sách", tL6[0], tot_l6[0]], ["tập hợp", tS6[0], tot_s6[0]]]),
           f"""Chào bạn, hãy tưởng tượng một hệ thống đã xử lý một triệu mã giao dịch, và với mỗi giao dịch mới phải hỏi mã này đã xử lý chưa. Nếu lưu các mã trong một danh sách, mỗi lần hỏi máy phải duyệt từ đầu, mất {tL6[1]}. Một nghìn lần hỏi mất {tot_l6[1]}.
           Nếu lưu trong một tập hợp thì mỗi lần hỏi chỉ mất {tS6[1]}, và một nghìn lần hỏi chỉ mất {tot_s6[1]}. Số đo trên máy kiểm, máy của bạn sẽ khác, nhưng chênh lệch thì có thật."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Bốn cách xếp nhiều giá trị: <b>danh sách</b>, <b>bộ</b>, <b>từ điển</b>, <b>tập hợp</b> khác nhau ở đâu?</li>
<li>Vì sao <b>gán</b> một danh sách cho biến khác không tạo ra bản sao?</li>
<li>Khi dữ liệu lớn lên, vì sao <b>cách xếp</b> quyết định tốc độ?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, bốn cách xếp nhiều giá trị, là danh sách, bộ, từ điển và tập hợp, khác nhau ở đâu. Hai, vì sao gán một danh sách cho biến khác không tạo ra bản sao. Ba, khi dữ liệu lớn lên, vì sao cách xếp quyết định tốc độ."""),
    ], )
    sc_pre = sc("prereq", "prereq", "Ôn lại: vòng lặp đi qua danh sách, và hàm một dòng làm khoá", [
        st(code_block(P_DEM, lines=(1, 1), title="Hai bài trước ta đã gặp danh sách trong vòng lặp") + "<p>Vòng lặp đếm lấy từng phần tử một; hàm một dòng không tên <code>lambda</code> là cách viết gọn một quy tắc. Bài này đi sâu vào <b>danh sách</b> và các anh em của nó.</p>",
           """Ta ôn lại hai điều. Ta đã thấy một danh sách các giá trị trong cặp ngoặc vuông, và vòng lặp đếm lấy từng phần tử một. Ta cũng đã biết hàm một dòng không tên, cách viết gọn một quy tắc. Hôm nay ta đi sâu vào danh sách và các cấu trúc họ hàng của nó."""),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ngoặc vuông, ngoặc tròn, ngoặc nhọn, chỉ số và cắt lát", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>[a, b, c]</code>", "danh sách", "các giá trị xếp thành hàng, <b>sửa được</b>; <code>x[0]</code> là phần tử đầu (chỉ số bắt đầu từ <code>0</code>), <code>x[-1]</code> là phần tử cuối"],
                  ["<code>x[1:3]</code>", "cắt lát", "lấy từ chỉ số <code>1</code> đến <b>trước</b> chỉ số <code>3</code> (giống <code>range</code>); <code>x[:2]</code> hai phần tử đầu"],
                  ["<code>len(x)</code>, <code>x.append(v)</code>", "độ dài, thêm cuối", "<code>len</code> đếm số phần tử; dấu chấm gọi một việc (<b>phương thức</b>) gắn với giá trị đứng trước nó: <code>append</code> thêm <code>v</code> vào cuối"]]),
           """Bảng đầu là danh sách. Các giá trị xếp thành hàng trong cặp ngoặc vuông, và sửa được. Chỉ số bắt đầu từ không, nên chỉ số không là phần tử đầu, và chỉ số âm một là phần tử cuối. Cắt lát lấy từ chỉ số này đến trước chỉ số kia, giống lệnh sinh dãy số.
           Lệnh đếm độ dài cho biết số phần tử. Dấu chấm sau tên một danh sách gọi một việc gắn với danh sách đó, gọi là phương thức, ở đây là thêm một giá trị vào cuối."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>(a, b)</code>", "bộ", "như danh sách nhưng <b>không sửa được</b>"],
                  ["<code>{\"A01\": 5}</code>", "từ điển", "bảng tra <b>khoá → giá trị</b>; <code>d[\"A01\"]</code> lấy giá trị; <code>d.get(k, 0)</code> lấy hoặc trả <code>0</code> nếu thiếu"],
                  ["<code>{\"nap\", \"rut\"}</code>", "tập hợp", "các giá trị <b>không trùng</b>, hỏi “có trong đó không” rất nhanh; <code>{}</code> rỗng là từ điển, không phải tập hợp"]]),
           """Bảng thứ hai là ba họ hàng. Bộ giống danh sách nhưng không sửa được. Từ điển là bảng tra, đưa khoá vào thì lấy ra giá trị, và có cách lấy an toàn trả về một giá trị mặc định nếu khoá thiếu. Tập hợp chứa các giá trị không trùng nhau, và hỏi có trong đó không rất nhanh.
           Chú ý cặp ngoặc nhọn rỗng là từ điển rỗng, không phải tập hợp.""", clear=True),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>sorted(x, key=f)</code>", "sắp xếp theo khoá", "trả danh sách mới xếp theo <code>f(phần_tử)</code>; <code>reverse=True</code> xếp giảm dần"],
                  ["<code>[f(x) for x in xs if đk]</code>", "danh sách suy ra", "viết gọn vòng lặp: với mỗi <code>x</code> thoả <code>đk</code>, thêm <code>f(x)</code> vào danh sách mới"],
                  ["<code>for ma, tien in cac_cap:</code>", "mở gói", "mỗi phần tử là bộ hai giá trị, gán luôn cho hai biến"]]),
           """Bảng cuối là ba cách viết gọn. Lệnh sắp xếp theo khoá cho một danh sách mới xếp theo kết quả của hàm khoá, và đảo ngược nếu cần giảm dần. Danh sách suy ra viết gọn một vòng lặp: với mỗi phần tử thoả điều kiện, thêm kết quả vào danh sách mới.
           Và mở gói cho phép vòng lặp gán luôn hai giá trị của một bộ cho hai biến.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: dãy ô, tủ có nhãn, hai nhãn một danh sách", [
        st(svg(1500, 430,
               txt(260, 45, "danh sách: dãy ô đánh số", 28, "middle", "#1f2937", True),
               *[box(20 + i * 170, 70, 160, 80, [str(v)], C_BLUE, 24, True) for i, v in enumerate(["450 000", "12 000 000", "800 000", "30 000 000"][:3])],
               *[txt(100 + i * 170, 185, f"[{i}]", 24, "middle", "#6b7280") for i in range(3)],
               txt(260, 245, "tìm một giá trị: xem lần lượt từng ô", 26, "middle", "#dc2626", True),
               txt(260, 285, "n ô thì tới n lần so sánh", 26, "middle", "#dc2626"),
               txt(1010, 45, "từ điển / tập hợp: tủ có nhãn", 28, "middle", "#1f2937", True),
               box(760, 70, 150, 80, ["A01", "→ 5"], C_GREEN, 24, True),
               box(930, 70, 150, 80, ["A02", "→ 3"], C_GREEN, 24, True),
               box(1100, 70, 150, 80, ["A03", "→ 1"], C_GREEN, 24, True),
               txt(1010, 245, "máy tính ra vị trí từ chính khoá,", 26, "middle", "#16a34a", True),
               txt(1010, 285, "nhảy thẳng tới ngăn: số bước gần như không đổi", 26, "middle", "#16a34a"),
               txt(750, 375, "đổi lại: tủ nhãn tốn thêm bộ nhớ và các khoá phải là giá trị không sửa được", 26, "middle", "#1f2937"),
               txt(750, 415, "(chuỗi, số, bộ chứa toàn giá trị không sửa được; danh sách thì không)", 24, "middle", "#6b7280")),
           """Hình này giải thích vì sao tìm kiếm nhanh hay chậm. Danh sách là dãy ô đánh số. Muốn tìm một giá trị, máy phải xem lần lượt từng ô, nên n ô thì tới n lần so sánh. Từ điển và tập hợp là tủ có nhãn. Máy tính ra vị trí từ chính khoá rồi nhảy thẳng tới ngăn, nên số bước gần như không đổi.
           Đổi lại, tủ có nhãn tốn thêm bộ nhớ, và các khoá phải là giá trị không sửa được."""),
        st(svg(1500, 380,
               box(30, 60, 150, 70, ["goc"], C_AMBER, 28, True),
               box(30, 160, 170, 70, ["ban_sao"], C_AMBER, 28, True),
               arrow(185, 95, 360, 150, "#d97706"),
               arrow(205, 195, 360, 175, "#d97706"),
               box(365, 110, 430, 90, ["[100000, 200000]", "MỘT danh sách"], C_BLUE, 26, True),
               txt(580, 240, "ban_sao = goc: dán thêm nhãn,", 24, "middle", "#dc2626", True),
               txt(580, 272, "KHÔNG tạo danh sách mới", 24, "middle", "#dc2626", True),
               box(900, 60, 150, 70, ["goc"], C_AMBER, 28, True),
               box(900, 200, 190, 70, ["doc_lap"], C_AMBER, 28, True),
               arrow(1055, 95, 1180, 60, "#d97706"),
               arrow(1095, 235, 1180, 235, "#d97706"),
               box(1185, 20, 290, 70, ["[100000, 200000]"], C_BLUE, 24, True),
               box(1185, 200, 290, 70, ["[100000, 200000]", "bản sao mới"], C_GREEN, 24, True),
               txt(1180, 330, "goc[:] tạo danh sách MỚI", 24, "middle", "#16a34a", True)),
           """Hình thứ hai là điều hay gây lỗi. Khi viết biến mới bằng biến cũ, máy chỉ dán thêm một nhãn lên cùng danh sách, không tạo danh sách mới. Sửa qua nhãn nào, nhãn kia cũng thấy. Muốn có bản sao độc lập, ta cắt lát toàn bộ, và máy tạo ra một danh sách mới.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: chỉ số, cắt lát, bản sao, khoá sắp xếp, đếm bằng từ điển", [
        st(repl_block(R_LIST, 0, 4, title="Bước 1. Chỉ số bắt đầu từ 0, âm đếm từ cuối")
           + "<p>Vì chỉ số là <b>khoảng cách tính từ đầu</b>, phần tử đầu cách đầu $0$ ô nên <code>gd[0]</code>. Chỉ số $-1$ là một ô tính từ cuối: <code>450000</code>, <code>12000000</code>, <code>800000</code> có $3$ phần tử, cuối là <code>gd[2]</code> = <code>gd[-1]</code>.</p>",
           """Bước một, chỉ số. Vì chỉ số là khoảng cách tính từ đầu, phần tử đầu cách đầu không ô nên có chỉ số không. Với ba phần tử, phần tử cuối có chỉ số hai, và chỉ số âm một cũng trỏ đúng ô đó, vì âm một đếm một ô từ cuối. Máy xác nhận, phần tử đầu là bốn trăm năm mươi nghìn, phần tử cuối là tám trăm nghìn."""),
        st(repl_block(R_EDIT, title="Bước 1b. Sửa tại chỗ bằng chỉ số: danh sách được, bộ không")
           + "<p>Vì danh sách <b>sửa được</b>, <code>gd[0] = 500000</code> thay phần tử có chỉ số $0$ ngay trong danh sách. Bộ <b>không sửa được</b>: máy báo lỗi, <b>dòng cuối</b> nói không gán được vào phần tử của bộ. (Python 3.13 in thêm dòng mã và dấu <code>^</code> ở giữa; dòng cuối giống nhau.)</p>",
           """Thêm một điều về chỉ số, đó là sửa. Vì danh sách sửa được, gán một giá trị vào chỗ chỉ số không thay phần tử đầu ngay trong danh sách, số bốn trăm năm mươi nghìn thành năm trăm nghìn.
           Còn bộ không sửa được, nên gán vào chỉ số không của một bộ làm máy báo lỗi, và dòng cuối nói rõ điều đó.""", clear=True),
        st(repl_block(R_TAPHOP, title="Bước 1c. Tập hợp: hỏi “có không”; từ điển: thêm khoá, lấy có mặc định")
           + "<p><code>in</code> hỏi một giá trị có <b>nằm trong</b> tập hợp không: đúng hoặc sai. Thêm giá trị đã có thì tập hợp <b>không đổi</b> ($2$ phần tử). <code>d.get(khoá, 0)</code> trả <code>0</code> nếu khoá thiếu.</p>",
           """Thêm tập hợp và từ điển là hai kiểu chứa dữ liệu cuối cùng của bài này. Chữ in hỏi một giá trị có nằm trong tập hợp không, và máy trả về đúng hoặc sai. Vì tập hợp không chứa giá trị trùng, thêm một giá trị đã có thì tập hợp không đổi, vẫn hai phần tử. Với từ điển, gán vào một khoá mới là thêm cặp mới, còn cách lấy có giá trị mặc định trả về không nếu khoá thiếu.""", clear=True),
        st(repl_block(R_CAT, 0, 3, title="Bước 2. Cắt lát: từ chỉ số đầu đến TRƯỚC chỉ số cuối")
           + "<p>Vì lát <code>[1:3]</code> lấy các chỉ số $1$ và $2$, số phần tử là $3 - 1 = 2$: <code>[20, 30]</code>. Bỏ chỉ số đầu thì bắt đầu từ $0$, bỏ chỉ số cuối thì đi tới hết.</p>",
           """Bước hai, cắt lát. Lát từ một đến ba lấy các chỉ số một và hai, dừng trước ba, nên có ba trừ một bằng hai phần tử, là hai mươi và ba mươi. Vì thế số phần tử của một lát bằng chỉ số cuối trừ chỉ số đầu, khi chỉ số cuối không vượt quá độ dài. Bỏ chỉ số đầu thì bắt đầu từ không, bỏ chỉ số cuối thì đi tới hết.""", clear=True),
        st(run_block(P_ALIAS, title="Bước 3. Gán không sao chép; cắt lát toàn bộ thì sao chép")
           + "<p>Dòng $2$ chỉ <b>dán thêm nhãn</b>; <code>goc[:]</code> là lát từ đầu đến cuối nên là danh sách <b>mới</b>. Nhưng bản sao này <b>nông</b>: các phần tử bên trong (nếu là danh sách) vẫn dùng chung.</p>",
           """Bước ba, sao chép. Vì dòng hai chỉ dán thêm một nhãn, thêm phần tử qua nhãn bản sao làm cả hai nhãn thấy ba phần tử. Còn cắt lát toàn bộ tạo một danh sách mới, nên thêm phần tử vào bản độc lập không đổi danh sách ban đầu. Nhưng bản sao này là sao chép nông, các phần tử bên trong nếu cũng là danh sách thì vẫn dùng chung.""",
           clear=True),
        st(repl_block(R_SORT, 0, 3, title="Bước 4. Sắp xếp theo một khoá")
           + "<p>Vì mỗi phần tử là bộ <code>(mã, tiền)</code>, khoá <code>g[1]</code> lấy tiền; máy xếp theo tiền tăng dần: $150\\,000 < 500\\,000 < 900\\,000$. <code>reverse=True</code> đảo lại, lấy phần tử đầu là lớn nhất.</p>",
           """Bước bốn, sắp xếp theo khoá. Mỗi phần tử là một bộ gồm mã và tiền, nên hàm khoá lấy phần tử có chỉ số một, tức là tiền. Máy xếp theo tiền tăng dần, từ một trăm năm mươi nghìn đến chín trăm nghìn. Thêm tham số đảo ngược thì xếp giảm dần, và phần tử đầu là giao dịch lớn nhất.""", clear=True),
        st(repl_block(R_COMP, 0, 3, title="Bước 5. Danh sách suy ra = vòng lặp viết gọn")
           + "<p>Vì <code>[x // 1000 for x in xs]</code> nghĩa là: với mỗi <code>x</code> trong <code>xs</code>, thêm <code>x // 1000</code>. Thêm <code>if x &gt;= 1000000</code> thì chỉ giữ các <code>x</code> thoả điều kiện.</p>",
           """Bước năm, danh sách suy ra. Vì dòng đầu nghĩa là với mỗi phần tử, thêm phần tử chia nghìn vào danh sách mới, nên bốn số thành bốn số đã chia nghìn. Thêm điều kiện ở cuối thì chỉ giữ các phần tử thoả điều kiện, ở đây hai giao dịch từ một triệu trở lên. Mỗi cách viết gọn đều thay được bằng một vòng lặp.""", clear=True),
    ], checks=["[450000, 12000000, 800000][-1] == [450000, 12000000, 800000][2]", "len([10, 20, 30, 40, 50][1:3]) == 3 - 1 and [10, 20, 30, 40, 50][1:3] == [20, 30]",
               "sorted([('A01', 500000), ('A02', 150000), ('A03', 900000)], key=lambda g: g[1])[0][1] == 150000",
               "[x // 1000 for x in [450000, 12000000, 800000, 30000000]] == [450, 12000, 800, 30000]"])
    sc_ex = sc("example", "example", "Ví dụ: đếm tần suất bằng từ điển, rồi gộp hai nguồn theo khoá", [
        st(run_block(P_DEM, title="Đếm số giao dịch theo loại"),
           """Ví dụ một, đếm tần suất. Từ điển rỗng ban đầu. Mỗi lượt lấy số đếm hiện tại của loại đó, trả về không nếu chưa có, cộng một rồi ghi lại. Máy in sáu giao dịch gồm ba chuyển khoản, hai nạp và một rút. Cách này đếm được dù không biết trước có những loại nào."""),
        st(run_block(P_GOP, title="Gộp hai nguồn: danh sách giao dịch và bảng tra tên")
           + "<p>Vòng đầu cộng tiền theo mã tài khoản: $300\\,000 + 250\\,000 = 550\\,000$ cho <code>A02</code>. Vòng sau duyệt <code>sorted(tong)</code>: danh sách các <b>khoá</b> của từ điển <code>tong</code>, xếp tăng dần; mỗi khoá dùng để tra tên.</p>",
           """Ví dụ hai. Ta có danh sách giao dịch và một bảng tra tên theo mã tài khoản. Vòng đầu cộng tiền theo mã, ở đây tài khoản A không hai có ba trăm nghìn cộng hai trăm năm mươi nghìn bằng năm trăm năm mươi nghìn. Vòng sau duyệt danh sách các khoá của từ điển, đã xếp tăng dần, và tra tên bằng khoá, rồi máy in tên kèm tổng tiền.""", clear=True),
        st(run_block(P_XEP, title="Xếp các mã theo tổng giảm dần, lấy hai mã đầu")
           + "<p>Hàm khoá <code>lambda m: tong[m]</code> tra tổng của từng mã; <code>reverse=True</code> xếp giảm dần; cắt lát <code>[:2]</code> lấy hai mã đầu.</p>",
           """Ví dụ ba, xếp theo khoá. Ta xếp các mã tài khoản theo tổng tiền giảm dần, với hàm khoá tra tổng trong từ điển. Mã A không hai có tổng lớn nhất, rồi đến A không một, rồi A không ba. Cắt lát lấy hai phần tử đầu cho ra hai tài khoản có tổng lớn nhất.""", clear=True),
    ], checks=["sorted({'A01': 500000, 'A02': 550000, 'A03': 120000}, key=lambda m: {'A01': 500000, 'A02': 550000, 'A03': 120000}[m], reverse=True)[:2] == ['A02', 'A01']", "300000 + 250000 == 550000", "dict((k, ['chuyen', 'nap', 'rut', 'chuyen', 'chuyen', 'nap'].count(k)) for k in ['chuyen', 'nap', 'rut']) == {'chuyen': 3, 'nap': 2, 'rut': 1}"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm lại, và cộng các nhóm", [
        st(repl_block(R_CHECK, 0, 4, title="Cách khác: đếm thẳng, rồi cộng các nhóm")
           + "<p>Tổng các nhóm phải bằng số phần tử: $3 + 2 + 1 = 6 = $ <code>len(loai)</code>. Nếu lệch, ta đã đếm thiếu hoặc đếm trùng.</p>",
           """Đường kiểm khác, đếm thẳng bằng một lệnh khác. Vì mỗi cách đếm độc lập, nếu trùng nhau thì đáng tin. Đếm chữ chuyển khoản trong danh sách cho ba, trùng với từ điển. Rồi kiểm tổng các nhóm. Ba cộng hai cộng một bằng sáu, đúng bằng độ dài danh sách. Nếu lệch, ta đã đếm thiếu hoặc đếm trùng."""),
    ], checks=["3 + 2 + 1 == len(['chuyen', 'nap', 'rut', 'chuyen', 'chuyen', 'nap'])"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn dần: số bước tìm kiếm tăng theo n, hoặc gần như không đổi", [
        st(table(["số phần tử", "danh sách: 1 lần hỏi", "tập hợp: 1 lần hỏi", "chênh (lần)"],
                 [["×1: 1 000", tL3[0], tS3[0], f"≈ {vnum(sig(val2(L3) / val2(S3), 2))}"], ["×1 000: 1 000 000", tL6[0], tS6[0], f"≈ {vnum(sig(val2(L6) / val2(S6), 2))}"],
                  ["ngoại suy ×100 000: 100 000 000", t2(L6 * 100)[0] + " (tuyến tính)", tS6[0] + " (gần như không đổi)", f"≈ {vnum(sig(val2(L6 * 100) / val2(S6), 2))}"]])
           + "<p class='note'>Đo trên máy kiểm, số minh hoạ (ns = phần tỉ giây, µs = phần triệu giây); hỏi giá trị <b>không có</b> trong dữ liệu (trường hợp tệ nhất của danh sách). <b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo để đoán quy mô lớn hơn (ước lượng, chưa đo).</p>",
           f"""Bảng này đo một lần hỏi giá trị không có trong dữ liệu, là trường hợp tệ nhất của danh sách. Với một nghìn phần tử, danh sách mất {tL3[1]}, tập hợp mất {tS3[1]}. Với một triệu phần tử, danh sách mất {tL6[1]}, còn tập hợp vẫn chỉ {tS6[1]}.
           Ngoại suy, tức nhân theo tỉ lệ từ số đã đo, cho thấy một trăm triệu phần tử khiến danh sách mất {t2(L6 * 100)[1]} mỗi lần hỏi. Nhân một nghìn lần hỏi, đó là {tot_l8[1]}, còn tập hợp gần như không đổi."""),
        st(table(["cấu trúc, một triệu số nguyên", "bộ nhớ (đo bằng công cụ theo dõi bộ nhớ, máy kiểm, số minh hoạ)"],
                 [["danh sách", bl[0]], ["tập hợp", bs[0]]])
           + "<p class='note'><b>byte</b> là đơn vị đo bộ nhớ (một byte đủ chứa một chữ cái); <b>KB</b> ≈ một nghìn byte, <b>MB</b> ≈ một triệu byte.</p>"
           + "<div class='box key'><b>Đánh đổi:</b> tập hợp và từ điển tìm nhanh nhưng tốn bộ nhớ hơn và phải dựng một lần (lần dựng cũng tốn thời gian). "
             "Nếu chỉ hỏi vài lần, danh sách đủ; nếu hỏi nhiều lần trên dữ liệu lớn, đáng dựng tập hợp. Người làm nghề <b>đo</b> chứ không đoán.</div>",
           f"""Cái giá của tốc độ là bộ nhớ, đo bằng byte: một byte đủ chứa một chữ cái, màn hình ghi tắt một triệu byte bằng hai chữ cái. Một triệu số nguyên trong danh sách chiếm {bl[1]}, trong tập hợp chiếm {bs[1]}. Đánh đổi là tập hợp và từ điển tìm nhanh nhưng tốn bộ nhớ hơn, và phải dựng một lần. Nếu chỉ hỏi vài lần thì danh sách đủ dùng. Nếu hỏi nhiều lần trên dữ liệu lớn thì đáng dựng tập hợp.
          """, clear=True),
    ], checks=["100 * 10 ** 6 == 10 ** 8", "1000 * 1000 == 10 ** 6"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng gán danh sách là sao chép.</div>' + run_block(P_ALIAS_IS)
           + "<p>Sửa <code>ban_sao</code> làm <code>goc</code> đổi theo. Phép thử: in cả hai biến sau khi sửa, hoặc hỏi <code>goc is ban_sao</code>: <code>is</code> hỏi hai nhãn có dán vào <b>cùng một đối tượng</b> (một giá trị nằm trong bộ nhớ) không.</p>",
           """Lỗi thứ nhất, của người mới, là tưởng gán danh sách là sao chép. Thêm phần tử vào bản sao làm danh sách gốc đổi theo, vì chỉ có một danh sách với hai nhãn. Phép thử là in cả hai biến, hoặc dùng phép so sánh danh tính để hỏi hai nhãn có dán vào cùng một giá trị trong bộ nhớ không, và máy trả lời đúng."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Xoá khi đang lặp: <code>gd.remove(x)</code> xoá <code>x</code> đầu tiên khỏi danh sách.</div>' + run_block(P_LAPXOA)
           + "<p>Vòng đầu bỏ sót một số $0$ vì danh sách co lại: còn <code>[5, 7, 0]</code>. Cách đúng: dựng danh sách <b>mới</b> bằng danh sách suy ra.</p>",
           """Lỗi thứ hai, của người đã đi làm, là xoá phần tử khi đang lặp qua chính danh sách đó, bằng lệnh xoá phần tử đầu tiên có giá trị cho trước. Mỗi lần xoá, danh sách co lại và các phần tử dịch chỗ, nên vòng lặp bỏ sót một số không. Kết quả còn năm, bảy, không, không báo lỗi. Cách đúng là dựng một danh sách mới bằng danh sách suy ra, như dòng cuối.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người mới).</b> Hỏi từ điển một khoá chưa có.</div>' + run_block(P_KEYERR)
           + "<p>Đọc dòng cuối: khoá <code>'A09'</code> không có. Nếu thiếu là chuyện bình thường, dùng <code>d.get(khoá, mặc_định)</code>; nếu thiếu là <b>lỗi dữ liệu</b>, để máy báo to còn hơn che đi.</p>",
           """Lỗi thứ ba, của người mới, là hỏi từ điển một khoá chưa có. Máy báo lỗi khoá, và dòng cuối nêu khoá thiếu. Nếu thiếu là chuyện bình thường, hãy dùng cách lấy có giá trị mặc định. Nhưng nếu thiếu là lỗi dữ liệu thì để máy báo to còn hơn che đi, vì che đi làm con số sai lọt vào báo cáo.""", clear=True),
    ], checks=["[x for x in [5, 0, 0, 7, 0] if x != 0] == [5, 7]"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Cho <code>x = [10, 20, 30, 40, 50]</code>.</p>
<ol><li><code>x[-2:]</code> là gì?</li>
<li><code>x[1:4]</code> có mấy phần tử, là những gì?</li></ol>
<p><b>Quyết định:</b> lưu $50\\,000$ mã tài khoản để hỏi “mã này có trong hệ thống không?” hàng triệu lần: dùng <b>danh sách</b> hay <b>tập hợp</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Cho một danh sách năm số. Câu một, lát từ âm hai đến hết là gì. Câu hai, lát từ một đến bốn có mấy phần tử và là những số nào.
           Sau đó là một quyết định, lưu năm mươi nghìn mã tài khoản để hỏi một mã có trong hệ thống không hàng triệu lần, dùng danh sách hay tập hợp, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(repl_block(R_QUIZ, 0, 4, title="Câu 1 và câu 2")
           + "<p>$-2$ là hai ô tính từ cuối: <code>[40, 50]</code>. Lát <code>[1:4]</code> lấy các chỉ số $1, 2, 3$: ba phần tử $= 4 - 1$.</p>",
           """Đáp án như sau. Chỉ số âm hai là hai ô tính từ cuối, nên lát từ đó đến hết là bốn mươi và năm mươi. Lát từ một đến bốn lấy các chỉ số một, hai, ba, nên có ba phần tử, hai mươi, ba mươi và bốn mươi."""),
        st("<div class='box key'><b>Quyết định:</b> <b>tập hợp</b>. Hỏi hàng triệu lần thì mỗi lần phải rẻ: tập hợp nhảy thẳng tới ngăn, danh sách phải duyệt tới $50\\,000$ ô. "
           "Dựng tập hợp một lần là chi phí nhỏ so với hàng triệu lần hỏi. Nếu cần giữ thứ tự hoặc cho phép trùng thì danh sách.</div>",
           """Còn quyết định cuối thì thế này, ta chọn tập hợp. Hỏi hàng triệu lần thì mỗi lần phải rẻ, tập hợp nhảy thẳng tới ngăn, còn danh sách phải duyệt tới năm mươi nghìn ô. Dựng tập hợp một lần là chi phí nhỏ so với hàng triệu lần hỏi. Nếu cần giữ thứ tự hoặc cho phép trùng thì mới dùng danh sách.""", clear=True),
    ], checks=["[10, 20, 30, 40, 50][-2:] == [40, 50] and len([10, 20, 30, 40, 50][1:4]) == 4 - 1"])
    sc_prac = practice_scene(sc, "Tự làm: đếm tần suất và gộp hai danh sách theo khoá", pr_steps(
        st, "PYT", "L03",
        """<p><b>Đề</b>: tạo <code>gop_khoa.py</code>. Chép dữ liệu từ <code>de.md</code>:</p>
<div class="code"><div>giao_dich = [("A02", 500000), ("A01", 200000), …]  # 6 giao dịch</div><div>ten = {"A01": "Hoa", "A02": "Nam", "A03": "Linh"}</div></div>
<ol><li>Với mỗi mã (xếp theo mã) in <code>mã số_giao_dịch tổng_tiền</code>;</li>
<li>Rồi in <code>tên tổng_tiền</code> theo <b>tổng giảm dần</b>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp với danh sách sáu giao dịch gồm mã tài khoản và số tiền, cùng một bảng tra tên. Với mỗi mã, theo thứ tự mã, in số giao dịch và tổng tiền. Rồi in tên kèm tổng tiền theo thứ tự tổng giảm dần.
        Dùng hai từ điển để đếm và cộng. Hãy dừng video và làm.""",
        LAB_OUT, "gop_khoa.py",
        """<div class="box key"><b>Nếu kẹt:</b> hai từ điển <code>dem</code> và <code>tong</code>, cùng mẫu <code>d[k] = d.get(k, 0) + giá_trị</code>. Vòng <code>for ma, tien in giao_dich:</code>. In theo mã: <code>sorted(dem)</code>. Theo tổng giảm dần: <code>sorted(tong, key=lambda m: tong[m], reverse=True)</code>.
Lời giải ở <code>labs/PYT/L03/loi_giai.py</code>.</div>""",
        """Nếu kẹt, dùng hai từ điển, một để đếm và một để cộng tiền, cùng mẫu lấy giá trị cũ hoặc không rồi cộng thêm. In theo mã thì sắp xếp các khoá. In theo tổng giảm dần thì sắp xếp các mã với khoá là tổng của mã đó, và đảo ngược.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L03")
    write_lab("PYT", "L03", """# Lab PYT L03 — Đếm tần suất và gộp theo khoá

Cần: Python 3.11 trở lên. Tạo `gop_khoa.py`. Dữ liệu (chép nguyên; số minh hoạ, khác ví dụ trong bài):

```python
giao_dich = [("A02", 500000), ("A01", 200000), ("A03", 950000), ("A02", 150000), ("A01", 700000), ("A02", 50000)]
ten = {"A01": "Hoa", "A02": "Nam", "A03": "Linh"}
```

1. Dùng hai từ điển đếm số giao dịch và cộng tiền theo mã. Với mỗi mã **theo thứ tự mã** in `<mã> <số giao dịch> <tổng tiền>`.
2. Rồi in `<tên> <tổng tiền>` cho mỗi mã, **theo tổng giảm dần**.

Chạy: `python gop_khoa.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L03 gop_khoa.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("danh sách: dãy ô, chỉ số từ 0, cắt lát trước chỉ số cuối", "bộ không sửa; từ điển: khoá → giá trị; tập hợp: không trùng",
                 "gán chỉ dán nhãn; muốn bản sao thì cắt lát hoặc sao chép", "sắp xếp theo khoá; danh sách suy ra", "tìm trong danh sách: n bước; tập hợp: gần như một bước"),
           """Tổng kết chuỗi logic. Danh sách là dãy ô, chỉ số từ không, và cắt lát dừng trước chỉ số cuối. Bộ không sửa được, từ điển ghép khoá với giá trị, tập hợp không chứa trùng. Gán chỉ dán nhãn, muốn bản sao phải làm riêng.
           Sắp xếp theo khoá và danh sách suy ra viết gọn việc hay gặp. Tìm trong danh sách mất n bước, còn trong tập hợp gần như một bước."""),
        st("""<div class='box key'><b>Tư duy:</b> chọn cấu trúc theo <b>câu hỏi sẽ hỏi nhiều nhất</b>: duyệt theo thứ tự (danh sách), tra theo khoá (từ điển), hỏi “có không” (tập hợp). Rồi <b>đo</b> ở quy mô thật.</div>
<p>Bài sau: chuỗi chữ và biểu thức chính quy, để đọc dữ liệu dạng chữ như dòng nhật ký.</p>""",
           """Điều cần mang theo, chọn cấu trúc theo câu hỏi sẽ hỏi nhiều nhất, duyệt theo thứ tự, tra theo khoá, hay hỏi có hay không. Rồi đo ở quy mô thật.
           Bài sau, ta học chuỗi chữ và biểu thức chính quy, để đọc dữ liệu dạng chữ như các dòng nhật ký.""", forward_ref=True),
    ])
    return lesson("L03", "danh_sach_tu_dien_tap_hop", "Bài 3 — Danh sách, từ điển, tập hợp: chọn cấu trúc cho dữ liệu",
                  "curriculum/pyt.yaml L03; audit/pyt/verify_pyt.py L03 (chạy thật trên Python 3.11 và 3.13; thời gian và bộ nhớ tra cứu đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính cho danh sách); "
                  "Python Tutorial §5 (Data Structures: lists, tuples, sets, dictionaries, comprehensions), Python Wiki TimeComplexity (tra cứu danh sách O(n), tập hợp O(1) trung bình), "
                  "Library Reference §4.6 (Sequence types: sao chép nông); số tiền là số minh hoạ",
                  ["Tạo, đọc và sửa danh sách bằng chỉ số, chỉ số âm, cắt lát và thêm phần tử",
                   "Phân biệt danh sách, bộ, từ điển và tập hợp, và nêu khi nào dùng từng loại",
                   "Giải thích vì sao gán một danh sách không tạo bản sao, và tạo bản sao độc lập",
                   "Sắp xếp theo một khoá và viết danh sách suy ra",
                   "Đếm tần suất và gộp hai nguồn theo khoá bằng từ điển",
                   "Nêu số bước tìm kiếm của danh sách và tập hợp thay đổi thế nào ở ba quy mô",
                   "Chỉ ra ba lỗi hay gặp: gán thay cho sao chép, xoá khi đang lặp, hỏi khoá thiếu",
                   "Viết chương trình đếm tần suất và gộp hai danh sách theo khoá"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy"],
                  covers=[(1, "formula"), (2, "quiz"), (3, "formula"), (4, "formula"), (5, "example"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
