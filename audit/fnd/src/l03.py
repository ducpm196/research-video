from lib import *
from labkit import write_lab, practice_steps, practice_scene

CSV = """ma,loai,tai_khoan,so_tien
1,chuyen,A01,500000
2,nap,A02,2000000
3,rut,A01,300000
4,chuyen,A03,150000
5,chuyen,A02,800000
6,nap,A01,1000000
7,rut,A03,200000
8,chuyen,A01,50000
9,nap,A03,750000
10,chuyen,A02,120000
11,rut,A02,400000
12,chuyen,A03,900000
"""
LAB_CSV = """ma,loai,kenh,so_tien
1,rut,atm,500000
2,chuyen,app,1200000
3,thanh_toan,pos,85000
4,chuyen,app,300000
5,nap,quay,5000000
6,rut,atm,2000000
7,chuyen,web,450000
8,thanh_toan,pos,120000
9,chuyen,app,75000
10,rut,atm,1000000
11,nap,app,3000000
12,thanh_toan,web,260000
13,chuyen,app,640000
14,thanh_toan,pos,45000
15,rut,quay,700000
"""
LAB_SOL = "cat > gd.csv <<'EOF'\n" + LAB_CSV + """EOF
tail -n +2 gd.csv | wc -l
cut -d, -f2 gd.csv | tail -n +2 | sort | uniq -c
cut -d, -f2 gd.csv | tail -n +2 | sort | uniq -c | sort -rn | head -n 1
cut -d, -f4 gd.csv | tail -n +2 | sort -rn | head -n 3"""
LAB_OUT = """15
      5 chuyen
      2 nap
      4 rut
      4 thanh_toan
      5 chuyen
5000000
3000000
2000000"""


def build():
    F = {"giaodich.csv": CSV}
    doc = cmd("PhienDoc", [
        ("head -n 3 giaodich.csv", "ma,loai,tai_khoan,so_tien\n1,chuyen,A01,500000\n2,nap,A02,2000000"),
        ("tail -n 2 giaodich.csv", "11,rut,A02,400000\n12,chuyen,A03,900000"),
        ("wc -l giaodich.csv", "13 giaodich.csv"),
        ("tail -n +2 giaodich.csv | wc -l", "12"),
    ], files=F)
    loc = cmd("PhienLoc", [
        ("grep chuyen giaodich.csv", "1,chuyen,A01,500000\n4,chuyen,A03,150000\n5,chuyen,A02,800000\n8,chuyen,A01,50000\n10,chuyen,A02,120000\n12,chuyen,A03,900000"),
        ("grep -c chuyen giaodich.csv", "6"),
        ("grep -v chuyen giaodich.csv | wc -l", "7"),
        ("grep A01 giaodich.csv | grep rut", "3,rut,A01,300000"),
    ], files=F)
    ong = cmd("PhienOng", [
        ("cut -d, -f2 giaodich.csv | tail -n +2 | sort | uniq -c", "      6 chuyen\n      3 nap\n      3 rut"),
        ("cut -d, -f2 giaodich.csv | tail -n +2 | uniq -c | head -n 4", "      1 chuyen\n      1 nap\n      1 rut\n      2 chuyen"),
        ("cut -d, -f2 giaodich.csv | tail -n +2 | sort | uniq -c | sort -rn | head -n 1", "      6 chuyen"),
        ("cut -d, -f2 giaodich.csv | tail -n +2 | sort | uniq -c > thong_ke.txt", ""),
        ("cat thong_ke.txt", "      6 chuyen\n      3 nap\n      3 rut"),
    ], files=F)
    so = cmd("PhienSo", [
        ("cut -d, -f4 giaodich.csv | tail -n +2 | sort | head -n 3", "1000000\n120000\n150000"),
        ("cut -d, -f4 giaodich.csv | tail -n +2 | sort -n | head -n 3", "50000\n120000\n150000"),
        ("cut -d, -f4 giaodich.csv | tail -n +2 | sort -rn | head -n 3", "2000000\n1000000\n900000"),
    ], files=F)
    loi = cmd("PhienLoi", [
        ("ls khong_co 2> loi.txt", ""), ("cat loi.txt", "ls: cannot access 'khong_co': No such file or directory"),
        ("ls khong_co 2> /dev/null", ""),
    ])
    cham = cmd("PhienCham", [
        ("echo 125 > so.txt", ""), ("echo 1.5 >> so.txt", ""), ("grep 1.5 so.txt", "125\n1.5"), ("grep -F 1.5 so.txt", "1.5"),
    ])
    quymo = cmd("PhienQuyMo", [
        ("seq 1 12 > t12.txt", ""), ("wc -l t12.txt", "12 t12.txt"), ("wc -c t12.txt", "27 t12.txt"),
        ("seq 1 1200 > t1200.txt", ""), ("wc -l t1200.txt", "1200 t1200.txt"), ("wc -c t1200.txt", "4893 t1200.txt"),
        ("seq 1 120000 > t120k.txt", ""), ("wc -l t120k.txt", "120000 t120k.txt"), ("wc -c t120k.txt", "728895 t120k.txt"),
        ("tail -n 1 t120k.txt", "120000"),
    ])
    quiz = cmd("PhienQuiz", [
        ("grep -c rut giaodich.csv", "3"),
        ("grep A02 giaodich.csv | cut -d, -f4 | sort -n | tail -n 1", "2000000"),
        ("grep chuyen giaodich.csv | wc -l", "6"),
    ], files=F)

    sc_hook = sc("hook", "hook", "Tệp giao dịch cả trăm nghìn dòng: hỏi một câu, trả lời bằng một dòng lệnh", [
        st(file_block(cmd("Mau", [("true", "")], files=F), "giaodich.csv", title="Tệp giaodich.csv, bản rút gọn 12 dòng giao dịch (số minh hoạ)", lines=(1, 4))
           + term_block(ong, 0, 1, title="Hỏi: mỗi loại giao dịch có bao nhiêu lệnh?"),
           """Chào bạn, một tệp giao dịch có thể dài hàng trăm nghìn dòng, mở bằng trình soạn thảo thì không đọc nổi. Giả sử ai đó hỏi mỗi loại giao dịch có bao nhiêu lệnh.
           Ở đây ta dùng bản rút gọn mười hai dòng, và bốn lệnh nối nhau bằng dấu ống trả lời ngay trong một dòng, gồm sáu lệnh chuyển, ba lệnh nạp và ba lệnh rút."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Xem <b>đầu</b>, <b>cuối</b> và <b>đếm dòng</b> của một tệp lớn bằng lệnh nào?</li>
<li><b>Lọc</b> dòng theo mẫu và <b>cắt cột</b> của tệp bảng ra sao?</li>
<li>Dấu <b>ống</b> <code>|</code> nối các lệnh nhỏ thành một lệnh lớn thế nào, và vì sao thứ tự quan trọng?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Xem đầu, xem cuối và đếm dòng của một tệp lớn bằng lệnh nào. Lọc dòng theo mẫu và cắt cột của tệp bảng ra sao.
           Và dấu ống nối các lệnh nhỏ thành một lệnh lớn thế nào, vì sao thứ tự quan trọng."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp văn bản, lệnh in nội dung, chuyển hướng", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tệp văn bản", "tệp chứa chữ, mỗi dòng kết thúc bằng một ký tự xuống dòng"],
                  ["② tệp CSV", "bảng viết bằng chữ: mỗi dòng là một hàng, các cột cách nhau bằng dấu phẩy, ví dụ <code>1,chuyen,A01,500000</code>"],
                  ["③ lệnh in nội dung", "<code>cat f.txt</code> in cả tệp ra đầu ra (màn hình)"],
                  ["④ chuyển hướng", "<code>&gt;</code> ghi đè, <code>&gt;&gt;</code> nối thêm: đưa đầu ra vào tệp"]]),
           """Ta ôn lại bốn điều. Tệp văn bản chứa chữ, mỗi dòng kết thúc bằng một ký tự xuống dòng. Tệp bảng là bảng viết bằng chữ, mỗi dòng là một hàng, các cột cách nhau bằng dấu phẩy.
           Lệnh in nội dung in cả tệp ra đầu ra. Và chuyển hướng đưa đầu ra vào tệp, một dấu để ghi đè, hai dấu để nối thêm.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã chín lệnh, cờ và dấu ống", [
        st(table(["lệnh", "đọc là", "nghĩa"],
                 [["<code>head -n 3 f</code>", "xem đầu tệp", "in <b>3 dòng đầu</b>; cờ <code>-n</code> cho số dòng"],
                  ["<code>tail -n 2 f</code>", "xem cuối tệp", "in <b>2 dòng cuối</b>; <code>tail -n +2 f</code>: từ dòng thứ 2 trở đi (bỏ dòng tiêu đề)"],
                  ["<code>wc -l f</code>", "đếm dòng", "in <b>số dòng</b> của tệp; cờ <code>-l</code> = lines"]]),
           """Bảng này là ba lệnh đọc. Lệnh xem đầu tệp in vài dòng đầu, cờ n cho biết số dòng. Lệnh xem cuối tệp in vài dòng cuối, và nếu viết dấu cộng trước số thì in từ dòng đó trở đi, nên dùng để bỏ dòng tiêu đề.
           Lệnh đếm dòng in số dòng của tệp, cờ chữ l là viết tắt của dòng.""",
           focus=[1, "1.2", "1.3", "1.4"]),
        st(table(["lệnh", "đọc là", "nghĩa"],
                 [["<code>grep chuyen f</code>", "tìm dòng chứa mẫu", "in các dòng <b>chứa</b> chữ <code>chuyen</code>; <code>-c</code> đếm; <code>-v</code> lấy dòng <b>không</b> chứa"],
                  ["<code>cut -d, -f2 f</code>", "cắt cột", "lấy <b>cột thứ 2</b>; <code>-d,</code> cho biết các cột cách nhau bằng dấu phẩy"],
                  ["<code>sort</code>", "xếp dòng", "xếp các dòng theo chữ cái; <code>-n</code> theo <b>giá trị số</b>; <code>-r</code> đảo ngược"],
                  ["<code>uniq -c</code>", "gộp dòng trùng", "gộp các dòng <b>giống nhau và liền kề</b>, kèm số lần (<code>-c</code> = count)"]]),
           """Bảng thứ hai là bốn lệnh lọc. Lệnh tìm dòng chứa mẫu in các dòng có mẫu, cờ c đếm, cờ v lấy các dòng không có mẫu. Lệnh cắt cột lấy một cột, cờ d cho biết dấu ngăn cột, cờ f cho biết số cột.
           Lệnh xếp dòng xếp theo chữ cái, cờ n xếp theo giá trị số, cờ r đảo ngược. Lệnh gộp dòng trùng chỉ gộp các dòng giống nhau và liền kề, và cờ c cho biết số lần.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "nghĩa"],
                 [["<code>A | B</code>", "<b>ống</b>: đầu ra của lệnh <code>A</code> trở thành đầu vào của lệnh <code>B</code>, không qua tệp trung gian"],
                  ["<code>2&gt; f</code>", "đưa <b>thông báo lỗi</b> (luồng lỗi) vào tệp <code>f</code>, thay vì ra màn hình"],
                  ["<code>/dev/null</code>", "“thùng không đáy”: ghi vào đó là <b>vứt đi</b>, ví dụ <code>2&gt; /dev/null</code>"]]),
           """Bảng cuối là ba dấu. Dấu ống nối đầu ra của lệnh bên trái thành đầu vào của lệnh bên phải, không qua tệp trung gian. Chữ hai và dấu lớn hơn đưa thông báo lỗi vào một tệp, thay vì ra màn hình.
           Và một nơi đặc biệt của máy là thùng không đáy, ghi vào đó là vứt đi.""",
           focus=[1, "1.2", "1.3", "1.4"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: dữ liệu chảy qua đường ống", [
        st(svg(1500, 400,
               box(10, 140, 230, 120, ["giaodich.csv", "13 dòng"], C_GRAY, bold=True),
               arrow(245, 200, 300, 200, "#2a78d6"),
               box(305, 140, 230, 120, ["cut -d, -f2", "lấy cột loại"], C_BLUE, bold=True),
               arrow(540, 200, 595, 200, "#2a78d6"),
               box(600, 140, 190, 120, ["tail -n +2", "bỏ tiêu đề"], C_BLUE, bold=True),
               arrow(795, 200, 850, 200, "#2a78d6"),
               box(855, 140, 170, 120, ["sort", "xếp loại"], C_AMBER, bold=True),
               arrow(1030, 200, 1085, 200, "#2a78d6"),
               box(1090, 140, 190, 120, ["uniq -c", "đếm nhóm"], C_GREEN, bold=True),
               arrow(1285, 200, 1340, 200, "#16a34a"),
               box(1345, 140, 150, 120, ["màn hình"], C_GRAY),
               txt(750, 60, "mỗi hộp làm MỘT việc nhỏ; dấu | nối đầu ra hộp trước vào đầu vào hộp sau", 26, "middle", "#1f2937", True),
               txt(750, 330, "dữ liệu chảy từng dòng, không cần chờ cả tệp xong", 26, "middle", "#16a34a", True),
               txt(750, 375, "riêng sort phải thấy mọi dòng mới xếp được", 24, "middle", "#d97706")),
           """Hình này là đường ống. Tệp giao dịch đi vào hộp cắt cột, lấy ra cột loại. Hộp thứ hai bỏ dòng tiêu đề. Hộp thứ ba xếp các loại theo chữ cái. Hộp cuối gộp các dòng liền nhau và đếm.
           Mỗi hộp làm một việc nhỏ, và dấu ống nối đầu ra của hộp trước vào đầu vào của hộp sau. Dữ liệu chảy từng dòng, riêng hộp xếp phải thấy mọi dòng mới xếp được."""),
        st(svg(1500, 340,
               box(20, 40, 360, 100, ["đầu vào", "(bàn phím, tệp, ống)"], C_BLUE, bold=True),
               arrow(385, 90, 510, 90, "#2a78d6", "đọc"),
               box(520, 40, 420, 100, ["một lệnh", "ví dụ grep, sort, cut"], C_AMBER, bold=True),
               arrow(945, 70, 1060, 70, "#16a34a", "kết quả"),
               box(1070, 30, 400, 80, ["đầu ra thường (màn hình, tệp, ống)"], C_GREEN),
               arrow(945, 120, 1060, 200, "#dc2626", "thông báo lỗi"),
               box(1070, 170, 400, 80, ["luồng lỗi: 2&gt; chuyển riêng"], C_RED),
               txt(750, 310, "hai đường ra: kết quả đi qua ống, lỗi mặc định vẫn hiện trên màn hình", 24, "middle", "#1f2937", True)),
           """Hình thứ hai cho thấy mỗi lệnh có một đầu vào và hai đường ra. Đường thứ nhất là kết quả, đi qua ống hoặc vào tệp. Đường thứ hai là thông báo lỗi, mặc định vẫn hiện trên màn hình.
           Vì vậy chuyển hướng hay ống chỉ bắt được kết quả, còn lỗi muốn bắt phải dùng chữ hai và dấu lớn hơn."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: vì sao phải xếp trước khi gộp, và xếp theo số khác xếp theo chữ", [
        st(term_block(ong, 1, 2, title="Bước 1. Gộp mà chưa xếp: chỉ gộp được dòng LIỀN KỀ")
           + "<p>Vì <code>uniq</code> chỉ so mỗi dòng với dòng <b>ngay trước</b> nó, các lệnh <code>chuyen</code> nằm rải rác nên không được gộp: ra số $1$, $1$, $1$, $2$.</p>",
           """Bước một, thử gộp mà chưa xếp. Vì lệnh gộp chỉ so mỗi dòng với dòng ngay trước nó, nên các dòng chuyển nằm rải rác không được gộp. Kết quả là một, một, một, rồi hai, và ta chưa có thống kê nào."""),
        st(term_block(ong, 0, 1, title="Bước 2. Xếp trước để các dòng giống nhau nằm liền nhau")
           + "<p>Nên <code>sort | uniq -c</code>: xếp xong, sáu dòng <code>chuyen</code> liền nhau, gộp thành $6$. Kiểm: $6 + 3 + 3 = \\hl{12}$ dòng dữ liệu ✓</p>",
           """Bước hai, xếp trước. Sau khi xếp, các dòng giống nhau nằm liền nhau, nên lệnh gộp đếm đúng, sáu lệnh chuyển, ba lệnh nạp và ba lệnh rút. Làm thử, sáu cộng ba cộng ba bằng mười hai, đúng bằng số dòng dữ liệu.""", clear=True),
        st(term_block(so, 0, 2, title="Bước 3. Xếp theo chữ khác xếp theo số")
           + "<p>Vì mặc định <code>sort</code> so <b>từng ký tự</b> từ trái sang, <code>1000000</code> đứng trước <code>120000</code> (ký tự thứ hai: chữ số 0 đứng trước chữ số 2). Thêm <code>-n</code> để so theo <b>giá trị</b>.</p>",
           """Bước ba, xếp theo chữ khác xếp theo số. Vì mặc định lệnh xếp so từng ký tự từ trái sang, nên một triệu đứng trước một trăm hai mươi nghìn, vì ký tự thứ hai là không nhỏ hơn hai.
           Thêm cờ n thì so theo giá trị, và số nhỏ nhất, năm mươi nghìn, hiện đầu tiên.""", clear=True),
    ], checks=["6 + 3 + 3 == 12", "'1000000' < '120000'", "1000000 > 120000", "sorted([500000, 2000000, 300000, 150000, 800000, 1000000, 200000, 50000, 750000, 120000, 400000, 900000])[:3] == [50000, 120000, 150000]"])
    sc_ex = sc("example", "example", "Ví dụ: hỏi tệp giao dịch năm câu", [
        st(term_block(doc, 0, 3, title="① Xem đầu, xem cuối, đếm dòng")
           + "<p>Tệp có $13$ dòng: $1$ dòng tiêu đề và $12$ giao dịch.</p>",
           """Câu hỏi thứ nhất, tệp trông thế nào. Xem ba dòng đầu thấy dòng tiêu đề và hai giao dịch. Xem hai dòng cuối thấy giao dịch mười một và mười hai. Đếm dòng ra mười ba, gồm một dòng tiêu đề và mười hai giao dịch."""),
        st(term_block(doc, 3, 4, title="② Đếm giao dịch, bỏ tiêu đề") + term_block(loc, 0, 2, title="③ Lọc theo loại"),
           """Câu hỏi thứ hai, có bao nhiêu giao dịch. Bỏ dòng tiêu đề rồi đếm, ra mười hai. Câu hỏi thứ ba, những dòng nào là lệnh chuyển. Lệnh tìm in sáu dòng chứa chữ chuyển, và cờ c cho đếm thẳng, cũng ra sáu.""", clear=True),
        st(term_block(loc, 2, 4, title="④ Dòng KHÔNG chứa mẫu; hai lần lọc nối nhau")
           + "<p>Bảy dòng không chứa <code>chuyen</code> (kể cả dòng tiêu đề). Rồi lọc tiếp: tài khoản A01 <b>và</b> loại rút.</p>",
           """Câu hỏi thứ tư, những dòng nào không phải lệnh chuyển. Cờ v lấy các dòng không chứa mẫu, có bảy dòng, kể cả dòng tiêu đề. Rồi lọc hai lần nối nhau, chỉ lấy tài khoản A không một và loại rút, ra đúng một giao dịch.""", clear=True),
        st(term_block(ong, 2, 5, title="⑤ Loại nhiều nhất, rồi lưu kết quả vào tệp")
           + "<p>Xếp ngược theo số lần, lấy dòng đầu: <code>chuyen</code> nhiều nhất ($6$ lần). Ghi bằng <code>&gt;</code> để giữ lại.</p>",
           """Câu hỏi thứ năm, loại nào nhiều nhất. Ta xếp bảng thống kê theo số lần, từ lớn xuống nhỏ, rồi lấy dòng đầu. Đó là loại chuyển với sáu lần. Cuối cùng ta ghi bảng thống kê vào một tệp bằng dấu lớn hơn, để giữ lại và đọc sau.""", clear=True),
    ], checks=["1 + 12 == 13", "13 - 1 == 12", "len([1, 4, 5, 8, 10, 12]) == 6", "13 - 6 == 7", "max([('chuyen', 6), ('nap', 3), ('rut', 3)], key=lambda t: t[1])[0] == 'chuyen'"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: ba cách đếm cùng một con số", [
        st(term_block(loc, 1, 2, title="Cách 1: đếm bằng cờ -c") + term_block(quiz, 2, 3, title="Cách 2: lọc rồi đếm dòng bằng ống"),
           """Đường kiểm khác, đếm số lệnh chuyển bằng hai cách. Cách một dùng cờ c của lệnh tìm. Cách hai lọc ra các dòng rồi chuyển qua ống cho lệnh đếm dòng. Cả hai cùng ra sáu, vì cùng đếm các dòng chứa chữ chuyển."""),
        st("<p>Cách 3: từ bảng thống kê, $6$ lệnh chuyển. Tổng ba nhóm $6 + 3 + 3 = 12$ trùng số dòng dữ liệu ở bước ②, nên không có dòng nào bị bỏ sót hay đếm hai lần ✓</p>",
           """Cách ba, đối chiếu với bảng thống kê. Sáu lệnh chuyển, và tổng ba nhóm là mười hai, trùng với số dòng dữ liệu đã đếm. Vì vậy không có dòng nào bị bỏ sót hay đếm hai lần.""", clear=True),
    ], checks=["6 + 3 + 3 == 12", "13 - 1 == 12"])
    sc_scale = sc("scale", "concept", "Khi tệp nhân lên: ống xử lý từng dòng, mở cả tệp thì không", [
        st(term_block(quymo, 1, 3, title="×1: 12 dòng") + term_block(quymo, 4, 6, title="×100: 1 200 dòng"),
           """Ta tạo hai tệp số bằng lệnh in dãy số, một tệp mười hai dòng, một tệp một nghìn hai trăm dòng. Số byte tăng theo, hai mươi bảy rồi bốn nghìn tám trăm chín mươi ba."""),
        st(term_block(quymo, 7, 10, title="×10 000: 120 000 dòng"),
           """Tệp thứ ba có một trăm hai mươi nghìn dòng, hơn bảy trăm nghìn byte. Dòng cuối của nó, một trăm hai mươi nghìn, hiện ra tức thì, vì lệnh xem cuối không cần mở cả tệp vào bộ nhớ.""", clear=True),
        st(table(["số dòng", "dung lượng đo được", "ngoại suy: 100 triệu dòng giao dịch × 35 byte/dòng (số minh hoạ)"],
                 [["×1: 12", "27 byte", "—"], ["×100: 1 200", "4 893 byte", "—"], ["×10 000: 120 000", "728 895 byte (≈ 0,7 MB)", "≈ 3,5 tỉ byte, tức ≈ 3,5 GB"]])
           + "<div class='box key'><b>Đánh đổi:</b> ống đọc và xử lý <b>từng dòng</b>, nên tệp lớn hơn bộ nhớ vẫn xử lý được; "
             "mở cả tệp để xem hay sửa thì phải nạp hết vào bộ nhớ. Riêng <code>sort</code> phải thấy mọi dòng, nên với dữ liệu rất lớn nó dùng tệp tạm trên đĩa và chậm hơn.</div>",
           """Bảng này ghi dung lượng đo được. Một trăm hai mươi nghìn dòng chỉ hơn bảy trăm nghìn byte. Nhưng một sổ cái một trăm triệu dòng, mỗi dòng ba mươi lăm byte, số minh hoạ, đã khoảng ba phẩy năm tỉ byte, lớn hơn bộ nhớ của nhiều máy.
           Ống xử lý từng dòng nên vẫn chạy được, còn mở cả tệp bằng trình soạn thảo thì không. Riêng lệnh xếp phải thấy mọi dòng, nên với dữ liệu quá lớn nó dùng tệp tạm trên đĩa và chậm hơn.""", clear=True),
    ], checks=["10000 // 100 == 100 and 12 * 100 == 1200 and 12 * 10000 == 120000", "100_000_000 * 35 == 3_500_000_000", "round(728895 / 1e6, 1) == 0.7"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Gộp bằng <code>uniq -c</code> mà quên <code>sort</code> trước.</div>'
           + term_block(ong, 1, 2) + "<p>Phép thử bắt được lỗi: tổng các số phải bằng số dòng dữ liệu, và mỗi loại chỉ được xuất hiện <b>một</b> lần. Ở đây <code>chuyen</code> xuất hiện nhiều lần.</p>",
           """Lỗi thứ nhất, của người mới, là gộp mà quên xếp trước. Phép thử bắt được lỗi này là mỗi loại chỉ được xuất hiện một lần trong bảng thống kê. Ở đây loại chuyển xuất hiện nhiều lần, nên bảng sai."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Dấu chấm trong mẫu của <code>grep</code> khớp <b>mọi</b> ký tự.</div>'
           + term_block(cham) + "<p>Mẫu <code>1.5</code> khớp cả <code>125</code>. Muốn tìm đúng chữ <code>1.5</code>, thêm cờ <code>-F</code> (tìm chuỗi nguyên văn).</p>",
           """Lỗi thứ hai, cũng của người mới, là dấu chấm trong mẫu của lệnh tìm khớp mọi ký tự. Mẫu một chấm năm khớp cả một trăm hai mươi lăm, nên ta nhận cả hai dòng.
           Muốn tìm đúng chuỗi, hãy thêm cờ F, tìm chuỗi nguyên văn."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Báo cáo “ba giao dịch nhỏ nhất” sai vì xếp theo chữ.</div>'
           + term_block(so, 0, 2) + "<p>Không có <code>-n</code>, <code>1000000</code> bị xếp vào nhóm “nhỏ nhất”. Số liệu sai mà <b>không báo lỗi</b>, nên thường lọt vào báo cáo.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là lập báo cáo ba giao dịch nhỏ nhất mà xếp theo chữ. Không có cờ n, một triệu bị xếp vào nhóm nhỏ nhất.
           Kết quả sai mà máy không báo lỗi, nên con số sai dễ lọt vào báo cáo. Hãy luôn dùng cờ n cho cột số, và đối chiếu một vài giá trị bằng mắt."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Dùng tệp <code>giaodich.csv</code> mười hai dòng ở trên (cột: <code>ma, loai, tai_khoan, so_tien</code>).</p>
<ol><li>Có bao nhiêu giao dịch <b>rút</b>?</li>
<li>Giao dịch <b>lớn nhất</b> của tài khoản A02 là bao nhiêu?</li></ol>
<p><b>Quyết định:</b> để đếm lệnh chuyển, bạn chọn <code>grep -c chuyen f</code> hay <code>grep chuyen f | wc -l</code>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Dùng tệp giao dịch mười hai dòng ở trên. Câu một, có bao nhiêu giao dịch rút. Câu hai, giao dịch lớn nhất của tài khoản A không hai là bao nhiêu.
           Sau đó là một quyết định, để đếm lệnh chuyển thì chọn cờ c hay chọn ống nối với lệnh đếm dòng, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(term_block(quiz, 0, 2, title="Câu 1 và câu 2")
           + "<p>Câu 1: ba giao dịch rút (các mã $3$, $7$, $11$). Câu 2: lọc A02, cắt cột số tiền, <code>sort -n</code>, lấy dòng cuối: $2\\,000\\,000$.</p>",
           """Đáp án câu một, có ba giao dịch rút, mang mã ba, bảy và mười một. Câu hai, lọc tài khoản A không hai, cắt cột số tiền, xếp theo số, lấy dòng cuối, ra hai triệu."""),
        st("<div class='box key'><b>Quyết định:</b> cả hai cùng ra $6$. Chọn <code>grep -c</code>: một lệnh, ngắn, ít chỗ sai. "
           "Dùng ống khi cần <b>xử lý tiếp</b> các dòng đã lọc (cắt cột, xếp, ...), vì chỉ khi đó đầu ra trung gian mới có ích.</div>",
           """Về quyết định, cả hai cùng ra sáu. Nên chọn cờ c, vì chỉ một lệnh, ngắn, ít chỗ sai. Dùng ống khi cần xử lý tiếp các dòng đã lọc, như cắt cột hay xếp, vì chỉ khi đó đầu ra trung gian mới có ích.""", clear=True),
    ], checks=["len([3, 7, 11]) == 3", "max([2000000, 800000, 120000, 400000]) == 2000000"])
    sc_prac = practice_scene(sc, "Tự làm: thống kê loại giao dịch và ba khoản lớn nhất", pr_steps(
        st, "FND", "L03",
        """<p><b>Đề</b>: tạo <code>thong_ke.sh</code>. Dòng đầu chép nguyên để có dữ liệu <code>gd.csv</code> (cột <code>ma, loai, kenh, so_tien</code>, 15 dòng; xem <code>de.md</code>). Rồi in lần lượt, bỏ dòng tiêu đề:</p>
<ol><li>tổng số giao dịch;</li>
<li>số giao dịch của <b>từng loại</b> (<code>cut | tail | sort | uniq -c</code>);</li>
<li>loại có <b>nhiều nhất</b> (kèm số lần);</li>
<li><b>ba</b> số tiền lớn nhất (<code>sort -rn | head</code>).</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh. Dòng đầu chép nguyên để có dữ liệu mười lăm giao dịch, bạn chưa cần hiểu dòng đó. Rồi in lần lượt bốn thứ, luôn bỏ dòng tiêu đề.
        Một, tổng số giao dịch. Hai, số giao dịch của từng loại. Ba, loại nhiều nhất kèm số lần. Bốn, ba số tiền lớn nhất, nhớ xếp theo giá trị số. Hãy dừng video và làm.""",
        LAB_OUT, "thong_ke.sh",
        """<div class="box key"><b>Nếu kẹt:</b> cột loại là cột <b>2</b>, cột số tiền là cột <b>4</b>. Mẫu chung: <code>cut -d, -f2 gd.csv | tail -n +2 | sort | uniq -c</code>.
Loại nhiều nhất: thêm <code>| sort -rn | head -n 1</code>. Ba khoản lớn nhất: cột 4, <code>sort -rn | head -n 3</code>. Lời giải ở <code>labs/FND/L03/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, cột loại là cột hai, cột số tiền là cột bốn. Mẫu chung là cắt cột, bỏ tiêu đề, xếp, rồi đếm nhóm. Loại nhiều nhất thì xếp ngược theo số lần rồi lấy dòng đầu. Ba khoản lớn nhất thì cắt cột bốn, xếp ngược theo số, lấy ba dòng.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=240), "FND", "L03")
    write_lab("FND", "L03", """# Lab FND L03 — Thống kê giao dịch bằng ống

Tạo `thong_ke.sh`. **Dòng đầu chép nguyên** (tạo dữ liệu giả `gd.csv`; `<<'EOF'` nhập nhiều dòng, bài sau giải thích):

```bash
cat > gd.csv <<'EOF'
""" + LAB_CSV + """EOF
```

Rồi viết bốn lệnh, **luôn bỏ dòng tiêu đề** (`tail -n +2`), in lần lượt:
1. tổng số giao dịch;
2. số giao dịch **từng loại** (cột 2): `cut`, `sort`, `uniq -c`;
3. loại có **nhiều nhất** (kèm số lần);
4. **ba** số tiền lớn nhất (cột 4): xếp theo số, giảm dần.

Chạy `bash thong_ke.sh`; chấm: `bash labs/cham.sh FND L03 thong_ke.sh`. Khác bài giảng: dữ liệu (15 dòng, cột kênh thay cho tài khoản), câu hỏi.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("head, tail, wc -l: nhìn và đếm", "grep: lọc dòng; cut: lấy cột", "sort rồi uniq -c: nhóm và đếm",
                 "| nối đầu ra vào đầu vào", "sort -n cho số", "&gt; lưu kết quả; 2&gt; bắt lỗi"),
           """Tổng kết chuỗi logic. Xem đầu, xem cuối và đếm dòng để nhìn tệp. Lọc dòng, cắt cột. Xếp rồi gộp để nhóm và đếm. Dấu ống nối đầu ra vào đầu vào. Cột số phải xếp theo số.
           Và dấu lớn hơn lưu kết quả, chữ hai dấu lớn hơn bắt thông báo lỗi."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng mở cả tệp lớn; hỏi nó bằng chuỗi lệnh nhỏ, mỗi lệnh một việc, rồi <b>kiểm</b> bằng một đường đếm thứ hai.</div>
<p>Bài sau: chương trình là gì, biến PATH cho máy biết tìm nó ở đâu, và mã thoát cho biết lệnh thành công hay thất bại.</p>""",
           """Điều cần mang theo, đừng mở cả tệp lớn. Hãy hỏi nó bằng chuỗi lệnh nhỏ, mỗi lệnh một việc, rồi kiểm bằng một đường đếm thứ hai.
           Bài sau, ta học chương trình là gì, biến môi trường nào cho máy biết tìm nó ở đâu, và mã thoát cho biết lệnh thành công hay thất bại.""", forward_ref=True),
    ])
    return lesson("L03", "doc_va_loc_van_ban", "Bài 3 — Đọc và lọc văn bản: ống và chuyển hướng",
                  "curriculum/fnd.yaml L03; audit/fnd/verify_fnd.py L03 (Git Bash chạy thật head/tail/wc/grep/cut/sort/uniq/seq); "
                  "GNU Coreutils manual (head, tail, wc, cut, sort, uniq, seq), GNU grep manual, GNU Bash Reference Manual (Pipelines, Redirections); "
                  "dữ liệu giao dịch là số minh hoạ; số dòng và số byte đo bằng verify_fnd",
                  ["Dùng các lệnh xem đầu, xem cuối và đếm dòng để nhìn một tệp lớn",
                   "Lọc dòng bằng mẫu và cắt cột của tệp bảng",
                   "Nối các lệnh nhỏ bằng dấu ống và giải thích vì sao phải xếp trước khi gộp",
                   "Xếp theo giá trị số thay vì theo chữ",
                   "Đếm một con số bằng ba cách khác nhau để kiểm",
                   "Chỉ ra ba lỗi hay gặp: quên xếp trước khi gộp, dấu chấm trong mẫu, xếp số theo chữ",
                   "Viết chuỗi lệnh thống kê loại giao dịch và ba khoản lớn nhất từ tệp bảng"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "ex"+"ample"), (2, "sym"), (3, "formula"), (4, "formula"), (5, "check"), (6, "pitfalls"), (7, "practice")])
