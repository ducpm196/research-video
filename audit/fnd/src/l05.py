from lib import *
from labkit import write_lab, practice_steps, practice_scene

LAB_BAD = """cat > Tong.java <<'EOF'
public class Tong {
    public static void main(String[] args) {
        int a = 100;
        int b = 250
        System.out.println("tong = " + (a + b));
    }
}
EOF
cat > tinh.py <<'EOF'
gia = 40
so_luong = 3
print("thanh tien =", gia * soluong)
EOF
cat > chao.sh <<'EOF'
echo "bat dau"
ech "xin chao"
EOF"""
LAB_FIX = """sed -i 's/int b = 250$/int b = 250;/' Tong.java
sed -i 's/soluong/so_luong/' tinh.py
sed -i 's/^ech /echo /' chao.sh
javac Tong.java && java Tong
python tinh.py
bash chao.sh"""
LAB_OUT = "tong = 350\nthanh tien = 120\nbat dau\nxin chao"

JAVA_LOI = 'public class Chao {\n    public static void main(String[] args) {\n        System.out.println("Chao ban")\n    }\n}\n'
JAVA_EOF = 'public class Dong {\n    public static void main(String[] args) {\n        int x = 5;\n        System.out.println("x = " + x);\n    }\n'
JAVA_QUOTE = 'public class Quote {\n    public static void main(String[] args) {\n        System.out.println(\u201cChao\u201d);\n    }\n}\n'
JAVA_SYM = 'public class Sym {\n    public static void main(String[] args) {\n        int tong = 1;\n        System.out.println(tonng);\n    }\n}\n'
CARET = " " * 38 + "^"


def build():
    ma = cmd("PhienMa", [
        ("echo A | od -An -tx1", " 41 0a"), ("echo ă | od -An -tx1", " c4 83 0a"), ("echo ể | od -An -tx1", " e1 bb 83 0a"),
        ("echo € | od -An -tx1", " e2 82 ac 0a"), ("wc -c vi.txt", "3 vi.txt"), ("echo ă | iconv -f cp1252 -t utf-8", "Äƒ"),
    ], files={"vi.txt": "ă\n"})
    cr = cmd("PhienCR", [
        ("printf 'echo a\\r\\n\\r\\necho b\\r\\n' > crlf.sh", ""), ("cat -A crlf.sh", "echo a^M$\n^M$\necho b^M$"),
        ("tr -d '\\r' < crlf.sh > lf.sh", ""), ("cat -A lf.sh", "echo a$\n$\necho b$"),
    ])
    jv = cmd("PhienJava", [
        ("javac Chao.java", "Chao.java:3: error: ';' expected\n" + '        System.out.println("Chao ban")\n' + CARET + "\n1 error"),
        ('grep -n println Chao.java', '3:        System.out.println("Chao ban")'),
        ("javac Dong.java", "Dong.java:5: error: reached end of file while parsing\n    }\n     ^\n1 error"),
    ], files={"Chao.java": JAVA_LOI, "Dong.java": JAVA_EOF})
    py = cmd("PhienPy", [
        ("python loi.py 2>&1 | tail -n 1", "NameError: name 'sodu_moi' is not defined"),
        ("python loi.py 2>&1 | grep -o 'line [0-9]*'", "line 2"),
    ], files={"loi.py": "sodu = 100\nprint(sodu_moi)\n"})
    sh = cmd("PhienSh", [("bash loi.sh", "bat dau\nloi.sh: line 2: ech: command not found\nhet")],
             files={"loi.sh": 'echo bat dau\nech "xin chao"\necho het\n'})
    quote = cmd("PhienQuote", [
        ("javac Quote.java 2>&1 | grep 'error:'", "Quote.java:3: error: illegal character: '\\u201c'\nQuote.java:3: error: illegal character: '\\u201d'\nQuote.java:3: error: not a statement"),
        ("javac Quote.java 2>&1 | tail -n 1", "3 errors"),
    ], files={"Quote.java": JAVA_QUOTE})
    sym = cmd("PhienSym", [
        ("javac Sym.java", "Sym.java:4: error: cannot find symbol\n        System.out.println(tonng);\n                           ^\n  symbol:   variable tonng\n  location: class Sym\n1 error"),
    ], files={"Sym.java": JAVA_SYM})
    log = cmd("PhienLog", [
        ("seq 1 1200 | sed 's/^/INFO dong /' > app.log", ""), ("echo 'ERROR mat ket noi' >> app.log", ""), ("grep -n ERROR app.log", "1201:ERROR mat ket noi"),
        ("seq 1 120000 | sed 's/^/INFO dong /' > big.log", ""), ("echo 'ERROR mat ket noi' >> big.log", ""), ("grep -n ERROR big.log", "120001:ERROR mat ket noi"),
        ("tail -n 2 big.log", "INFO dong 120000\nERROR mat ket noi"),
    ])

    sc_hook = sc("hook", "hook", "Cùng một tệp, hai chương trình đọc ra hai thứ khác nhau", [
        st(term_block(ma, 1, 2, title="Chữ ă lưu trên đĩa là hai byte c4 83 (hệ thập lục phân)")
           + term_block(ma, 5, 6, title="Cùng hai byte ấy, đọc nhầm bảng mã khác thì thành")
           + "<p>Một người gõ “ă” trong tệp, người khác mở ra thấy <b>Äƒ</b>: tệp không đổi, chỉ khác <b>bảng mã dùng để đọc</b>.</p>",
           """Chào bạn, hãy nhìn một tệp chỉ chứa chữ a có dấu mũ. Trên đĩa nó là hai byte, viết bằng hệ thập lục phân là c bốn và tám ba. Nếu một chương trình đọc hai byte ấy bằng một bảng mã khác, bạn thấy hai ký tự lạ.
           Tệp không đổi, chỉ khác bảng mã dùng để đọc. Đây là nguồn gốc của rất nhiều lỗi chữ tiếng Việt vỡ, và cũng của những thông báo lỗi khó hiểu."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Trình soạn mã khác trình soạn văn bản thế nào, và máy <b>lưu chữ</b> (UTF-8, xuống dòng) ra sao?</li>
<li>Một thông báo lỗi nói gì: <b>tệp, dòng, loại lỗi</b> nằm ở đâu?</li>
<li>Vì sao <b>lỗi đầu tiên</b> mới đáng sửa, còn những lỗi sau thường là hệ quả?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Trình soạn mã khác trình soạn văn bản thế nào, và máy lưu chữ ra sao, gồm bảng mã và cách xuống dòng. Một thông báo lỗi nói gì, tệp, dòng và loại lỗi nằm ở đâu.
           Và vì sao lỗi đầu tiên mới đáng sửa, còn những lỗi sau thường là hệ quả."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp là dãy byte, và lệnh đếm byte", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① byte", "tám bit, một số từ $0$ tới $255$; tệp là một dãy byte"],
                  ["② tệp văn bản", "dãy byte mà một <b>bảng mã</b> đổi thành chữ"],
                  ["③ đếm byte", "<code>wc -c f</code> cho số byte của tệp <code>f</code>"],
                  ["④ ống và lọc", "<code>A | B</code>, <code>grep</code>, <code>tail</code>, <code>head</code> để chọn phần cần đọc"]]),
           """Ta ôn lại bốn điều. Một byte là tám bit, một số từ không tới hai trăm năm mươi lăm, và tệp là một dãy byte. Tệp văn bản là dãy byte mà một bảng mã đổi thành chữ.
           Lệnh đếm có cờ c cho số byte của tệp. Và ống cùng các lệnh lọc giúp chọn phần cần đọc.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ], checks=["2 ** 8 - 1 == 255"])
    sc_sym = sc("sym", "symbol", "Giải mã: bảng mã, UTF-8, xuống dòng và đọc một thông báo lỗi", [
        st(table(["thuật ngữ", "nghĩa"],
                 [["<b>bảng mã</b>", "bảng ghép mỗi ký tự với một số, và cách ghi số đó thành byte"],
                  ["<b>UTF-8</b>", "bảng mã phổ biến nhất: ký tự dùng <b>1 đến 4 byte</b>; chữ không dấu 1 byte, chữ tiếng Việt có dấu 2 hoặc 3 byte"],
                  ["<b>xuống dòng</b>", "Linux, macOS: một ký tự <b>LF</b> (<code>\\n</code>); Windows: hai ký tự <b>CR LF</b> (<code>\\r\\n</code>)"],
                  ["<b>trình soạn mã</b>", "chương trình sửa <b>chữ thuần</b> không thêm định dạng: Visual Studio Code, Notepad++; <b>không</b> dùng Word"]]),
           """Bảng này giải mã bốn thuật ngữ. Bảng mã là bảng ghép mỗi ký tự với một số, và cách ghi số đó thành byte. Bảng mã phổ biến nhất ghi mỗi ký tự bằng một tới bốn byte. Chữ không dấu một byte, chữ tiếng Việt có dấu hai hoặc ba byte.
           Xuống dòng ở một số hệ điều hành là một ký tự, ở hệ điều hành bạn đang dùng thường là hai ký tự. Và trình soạn mã sửa chữ thuần, không thêm định dạng, khác hẳn trình soạn văn bản.""",
           focus=[1, "1.2", "1.3", "1.3", "1.4", "1.5"]),
        st(table(["viết", "nghĩa"],
                 [["<code>od -c f</code>", "in từng byte của <code>f</code> dạng ký tự (thấy <code>\\r</code>, <code>\\n</code>); <code>od -An -tx1</code>: dạng số thập lục phân"],
                  ["<code>cat -A f</code>", "in tệp, hiện <b>CR</b> là <code>^M</code> và <b>hết dòng</b> là <code>$</code>"],
                  ["<code>Tep.java:3: error: …</code>", "<b>tệp : dòng : loại lỗi : mô tả</b>; dòng sau in lại dòng mã, dấu <code>^</code> chỉ chỗ máy bắt đầu thấy lỗi"]]),
           """Bảng thứ hai là ba cách nhìn. Lệnh in từng byte cho thấy ký tự xuống dòng, hoặc cho số thập lục phân nếu thêm cờ. Lệnh in tệp có cờ chữ a hoa hiện ký tự về đầu dòng là mũ M và hết dòng là dấu đô la.
           Còn thông báo lỗi có dạng tệp, dòng, loại lỗi, mô tả. Dòng kế in lại dòng mã, và dấu mũ chỉ chỗ máy bắt đầu thấy lỗi.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: chữ → số → byte, và giải phẫu một thông báo lỗi", [
        st(svg(1500, 420,
               box(20, 40, 300, 100, ["chữ", "ă"], C_BLUE, bold=True),
               arrow(325, 90, 440, 90, "#2a78d6", "Unicode"),
               box(450, 40, 330, 100, ["số thứ tự 259", "(U+0103)"], C_AMBER, bold=True),
               arrow(785, 90, 900, 90, "#2a78d6", "UTF-8"),
               box(910, 40, 360, 100, ["byte  c4  83", "(2 byte)"], C_GREEN, bold=True),
               arrow(1275, 90, 1340, 90, "#16a34a"),
               box(1345, 40, 150, 100, ["tệp"], C_GRAY),
               txt(280, 230, "A  →  41  (1 byte)", 30, "middle", "#1f2937", True),
               txt(750, 230, "ă  →  c4 83  (2 byte)", 30, "middle", "#16a34a", True),
               txt(1220, 230, "ể  →  e1 bb 83  (3 byte)", 30, "middle", "#d97706", True),
               txt(750, 330, "chữ càng ít gặp trong tiếng Anh thì càng cần nhiều byte", 26, "middle", "#1f2937"),
               txt(750, 385, "đọc sai bảng mã = đổi byte thành sai chữ", 26, "middle", "#dc2626", True)),
           """Hình này là đường đi của một chữ vào tệp. Chữ a có mũ có số thứ tự hai trăm năm mươi chín trong bảng ký tự quốc tế. Bảng mã ghi số đó thành hai byte, c bốn và tám ba, rồi các byte nằm vào tệp.
           Chữ không dấu chỉ cần một byte, chữ tiếng Việt có dấu cần hai hoặc ba byte. Đọc ngược lại là làm đúng các bước trên theo chiều ngược, nên đọc sai bảng mã sẽ ra ký tự lạ."""),
        st(svg(1500, 380,
               box(20, 20, 1460, 80, "Chao.java:3: error: ';' expected", C_AMBER, 34, bold=True),
               box(20, 130, 1460, 60, '        System.out.println("Chao ban")', C_GRAY, 28),
               box(20, 215, 1460, 60, "                                      ^   máy dừng ở đây mới biết thiếu dấu", C_GRAY, 28),
               box(20, 300, 330, 60, "tệp: Chao.java", C_BLUE, 26, bold=True),
               box(370, 300, 250, 60, "dòng: 3", C_BLUE, 26, bold=True),
               box(640, 300, 330, 60, "loại: error", C_RED, 26, bold=True),
               box(990, 300, 490, 60, "mô tả: cần dấu ;", C_GREEN, 26, bold=True)),
           """Hình thứ hai là giải phẫu một thông báo lỗi. Phần đầu gồm bốn mảnh, tên tệp, số dòng, loại lỗi và mô tả. Dòng thứ hai in lại dòng mã. Dòng thứ ba có dấu mũ chỉ chỗ máy dừng lại mới biết thiếu dấu chấm phẩy.
           Chú ý dấu mũ chỉ chỗ máy phát hiện, không hẳn là chỗ gây ra lỗi."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: một chữ cần mấy byte trong UTF-8", [
        st("""<p><b>Bước 1.</b> Mỗi ký tự có một <b>số thứ tự</b> $N$. UTF-8 chọn số byte theo độ lớn của $N$:</p>
<table class='t'><tr><th>khoảng của $N$</th><th>số byte</th><th>khuôn bit</th></tr>
<tr><td>$0 .. 127$</td><td>1</td><td><code>0xxxxxxx</code></td></tr>
<tr><td>$128 .. 2\\,047$</td><td>2</td><td><code>110xxxxx 10xxxxxx</code></td></tr>
<tr><td>$2\\,048 .. 65\\,535$</td><td>3</td><td><code>1110xxxx 10xxxxxx 10xxxxxx</code></td></tr></table>""",
           """Bước một, mỗi ký tự có một số thứ tự. Bảng mã chọn số byte theo độ lớn của số đó. Từ không tới một trăm hai mươi bảy thì một byte. Từ một trăm hai mươi tám tới hai nghìn không trăm bốn mươi bảy thì hai byte.
           Từ hai nghìn không trăm bốn mươi tám tới sáu mươi lăm nghìn năm trăm ba mươi lăm thì ba byte. Mỗi byte có một khuôn bit riêng, các chữ x là chỗ điền bit của số."""),
        st("""<p><b>Bước 2. Làm thử với chữ ă</b> ($N = 259$). Vì $128 \\le 259 \\le 2\\,047$, nên dùng <b>2 byte</b>. Đổi ra nhị phân và điền khuôn:</p>
$$259 \\;\\to\\; 100000011 \\;\\to\\; 00100\\ 000011 \\;\\Rightarrow\\; 110\\mathbf{00100}\\ 10\\mathbf{000011} = \\hl{c4\\ 83}$$
<p class="note">Nhị phân của 259 là <code>100000011</code>; byte đầu <code>11000100</code> = 196 = <code>c4</code>, byte hai <code>10000011</code> = 131 = <code>83</code> (hệ thập lục phân): khớp với lệnh <code>od</code> ở đầu bài ✓</p>""",
           """Bước hai, làm thử với chữ a có mũ, số thứ tự hai trăm năm mươi chín. Vì hai trăm năm mươi chín nằm giữa một trăm hai mươi tám và hai nghìn không trăm bốn mươi bảy, nên dùng hai byte. Đổi ra nhị phân được chín bit.
           Ta chia thành năm bit và sáu bit, điền vào khuôn hai byte. Kết quả là một trăm chín mươi sáu và một trăm ba mươi mốt, tức c bốn và tám ba, khớp với lệnh in byte ở đầu bài.""", introduces=["implies"]),
        st("""<p><b>Bước 3. Chữ có hai dấu</b> như ể ($N = 7\\,875$) lớn hơn $2\\,047$, nên dùng <b>3 byte</b>: <code>e1 bb 83</code>. Chữ tiếng Việt có dấu vì thế nặng hơn chữ không dấu.</p>
$$\\text{“Nguyen”} = 6\\ \\text{byte} \\qquad \\text{“Nguyễn”} = 5 + 3 = 8\\ \\text{byte}$$""",
           """Bước ba, chữ có hai dấu như chữ ê hỏi có số thứ tự bảy nghìn tám trăm bảy mươi lăm, lớn hơn hai nghìn không trăm bốn mươi bảy, nên dùng ba byte. Vì vậy chữ tiếng Việt có dấu nặng hơn chữ không dấu.
           Tên không dấu có sáu byte, còn tên có dấu có tám byte, vì năm chữ một byte cộng một chữ ba byte."""),
    ], checks=["len(chr(259).encode('utf-8')) == 2", "chr(259).encode('utf-8').hex() == 'c483'", "128 <= 259 <= 2047",
               "0b11000100 == 196 and 0b10000011 == 131 and 196 == 0xc4 and 131 == 0x83", "bin(259)[2:] == '100000011'",
               "len('Nguyen'.encode('utf-8')) == 6", "len('Nguyễn'.encode('utf-8')) == 8", "len(chr(0x1ec3).encode('utf-8')) == 3 and 0x1ec3 == 7875"])
    sc_ex = sc("example", "example", "Ví dụ: đọc bốn thông báo lỗi thật và sửa một lỗi", [
        st(file_block(jv, "Chao.java", title="Tệp Chao.java") + term_block(jv, 0, 1, title="① Biên dịch: thông báo của Java"),
           """Phép thứ nhất, đọc thông báo của trình biên dịch Java. Tệp là Chao chấm Java, dòng ba, loại là lỗi, mô tả là cần dấu chấm phẩy. Dấu mũ nằm ngay sau dấu ngoặc đóng, nơi máy dừng lại mới biết thiếu."""),
        st(term_block(jv, 1, 2, title="② Kiểm: dòng thứ ba có đúng là dòng println?")
           + term_block(py, title="③ Python: lỗi nằm ở dòng CUỐI của thông báo"),
           """Phép thứ hai, kiểm lại bằng lệnh tìm có đánh số dòng. Dòng ba đúng là dòng in chữ, khớp với thông báo. Phép thứ ba, thông báo của ngôn ngữ thứ hai khác kiểu. Dòng cuối nói tên lỗi và mô tả, còn số dòng nằm ở dòng đầu của khối.
           Ở đây một tên biến chưa được định nghĩa, ở dòng hai."""),
        st(file_block(sh, "loi.sh", title="Tệp loi.sh") + term_block(sh, title="④ Bash: tên tệp, số dòng, tên lệnh sai"),
           """Phép thứ tư, thông báo của cửa sổ lệnh. Nó nói tên tệp, số dòng hai, và tên lệnh sai là e c h. Điểm đặc biệt là các dòng trước và sau vẫn chạy, nên màn hình có cả dòng bắt đầu và dòng hết, và lỗi chỉ là một dòng giữa."""),
        st(file_block(jv, "Dong.java", title="Tệp Dong.java (thiếu một dấu ngoặc nhọn đóng)") + term_block(jv, 2, 3, title="Java báo ở CUỐI tệp"),
           """Phép thứ năm, một lỗi có chỗ gây ra khác chỗ báo. Tệp thiếu một dấu ngoặc nhọn đóng cho lớp. Java đọc hết tệp mới biết thiếu, nên báo ở dòng cuối. Dấu mũ chỉ chỗ máy phát hiện, không phải chỗ bạn quên.
           Cách sửa là đếm các cặp ngoặc từ trên xuống, và thêm dấu đóng cuối tệp."""),
    ], checks=["len('Chao.java:3: error:'.split(':')) == 4"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đoán số byte rồi đếm", [
        st(term_block(ma, 4, 5, title="Tệp vi.txt chỉ có một chữ ă và dấu xuống dòng")
           + "<p>Đoán: $2$ byte cho chữ $+$ $1$ byte xuống dòng $= \\hl{3}$ byte. Máy đếm: $3$ ✓. Hai đường (tính theo khuôn, đếm bằng máy) cho cùng số.</p>",
           """Đường kiểm khác là đoán số byte rồi để máy đếm. Tệp chỉ có chữ a có mũ và dấu xuống dòng. Theo khuôn, chữ này hai byte, cộng một byte xuống dòng là ba byte. Máy đếm cũng ra ba, vì vậy phép tính của ta khớp."""),
        st(term_block(cr, 1, 2, title="Nhìn thấy ký tự vô hình bằng cat -A")
           + "<p>Mỗi dòng của tệp kiểu Windows kết thúc bằng <code>^M$</code> (CR rồi hết dòng); sau khi bỏ CR bằng <code>tr -d</code> chỉ còn <code>$</code> ✓</p>"
           + term_block(cr, 3, 4),
           """Kiểm thêm bằng cách nhìn ký tự vô hình. Tệp viết theo kiểu của hệ điều hành bạn đang dùng có mỗi dòng kết thúc bằng mũ M và đô la, nghĩa là có thêm ký tự về đầu dòng. Sau khi bỏ ký tự đó bằng lệnh xoá ký tự, chỉ còn dấu đô la hết dòng. Nhiều chương trình trên máy chủ sẽ coi ký tự về đầu dòng là một phần của dòng, nên lỗi hiện ra khó hiểu."""),
    ], checks=["2 + 1 == 3"])
    sc_scale = sc("scale", "example", "Khi nhật ký dài ra: một dòng lỗi nằm giữa hàng trăm nghìn dòng", [
        st(term_block(log, 0, 3, title="×1: nhật ký 1 201 dòng") + term_block(log, 3, 6, title="×100: nhật ký 120 001 dòng"),
           """Ta tạo hai nhật ký giả, một nhật ký một nghìn hai trăm lẻ một dòng, một nhật ký hơn một trăm hai mươi nghìn dòng, mỗi nhật ký có đúng một dòng lỗi ở cuối. Lệnh tìm có đánh số dòng chỉ ra ngay, một nghìn hai trăm lẻ một và một trăm hai mươi nghìn lẻ một.
           Hai kết quả cùng nhanh, dù nhật ký thứ hai lớn gấp một trăm lần."""),
        st(table(["số dòng", "đọc bằng mắt", "lọc bằng lệnh tìm"],
                 [["×1: 1 201", "cuộn nhiều trang", "ra ngay: vị trí 1 201"], ["×100: 120 001", "không thể", "ra ngay: vị trí 120 001"]])
           + "<div class='box key'><b>Đánh đổi:</b> với nhật ký lớn, đừng mở và cuộn: <b>lọc</b> theo từ khoá (<code>grep -n</code>), xem cuối (<code>tail</code>), rồi mở đúng quanh dòng đó. "
             "Lỗi cuối cùng thường gần cuối nhật ký, nhưng <b>nguyên nhân</b> có thể nằm ở dòng trước nó rất xa.</div>",
           """Bảng này so hai cách. Đọc bằng mắt thì không thể với nhật ký lớn. Lọc bằng lệnh tìm thì luôn ra ngay. Vì vậy với nhật ký lớn, đừng mở và cuộn, hãy lọc theo từ khoá, xem phần cuối, rồi mở đúng quanh dòng đó.
           Lỗi cuối cùng thường gần cuối nhật ký, nhưng nguyên nhân có thể nằm ở một dòng trước nó rất xa."""),
    ], checks=["1200 + 1 == 1201", "120000 + 1 == 120001", "120001 // 1201 == 99"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Soạn mã bằng Word, hoặc dán từ trang web: dấu nháy <b>cong</b> thay cho dấu nháy thẳng.</div>'
           + term_block(quote, 0, 1) + "<p>Dấu nháy cong <code>\\u201c</code> không phải dấu nháy của ngôn ngữ; cả một dòng thành <b>3 lỗi</b>. Phép thử: dùng trình soạn mã, tắt tự thay thế dấu nháy.</p>",
           """Lỗi thứ nhất, của người mới, là soạn mã bằng trình soạn văn bản, hoặc dán từ trang mạng. Dấu nháy cong thay cho dấu nháy thẳng, và Java báo ký tự không hợp lệ, mang mã u hai không không c.
           Chỉ một dòng nhưng ra ba lỗi. Phép thử là dùng trình soạn mã và tắt tính năng tự thay dấu nháy."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Sửa lỗi ở dòng <b>cuối</b> của danh sách, thay vì dòng đầu.</div>'
           + term_block(quote, 1, 2) + "<p>Ba lỗi nhưng chỉ <b>một nguyên nhân</b> (dấu nháy cong). Sửa lỗi đầu rồi <b>biên dịch lại</b>; các lỗi sau thường tự hết.</p>",
           """Lỗi thứ hai, cũng của người mới, là sửa lỗi ở cuối danh sách. Ba lỗi nhưng chỉ một nguyên nhân. Một lỗi đầu có thể làm máy hiểu sai cả những dòng sau, nên các lỗi sau thường là hệ quả.
           Hãy sửa lỗi đầu tiên rồi biên dịch lại, và đếm lại số lỗi."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Cho rằng thông báo luôn chỉ đúng chỗ sai.</div>'
           + term_block(jv, 2, 3) + "<p>Thông báo cho biết nơi máy <b>phát hiện</b>, không phải nơi bạn <b>gây ra</b>. Dòng cuối tệp ở đây chỉ là chỗ Java đọc hết mà vẫn thiếu một ngoặc.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là tin rằng thông báo luôn chỉ đúng chỗ sai. Thông báo cho biết nơi máy phát hiện, không phải nơi bạn gây ra. Ở đây dòng cuối tệp chỉ là chỗ Java đọc hết mà vẫn thấy thiếu một ngoặc.
           Người làm nghề đọc cả vùng quanh dòng báo, rồi đếm cặp ngoặc, dấu nháy, thụt lề ở phía trên."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(term_block(sym, title="Thông báo của Java khi biên dịch Sym.java"),
           """Bây giờ tới phần bạn tự làm. Tệp Sym chấm Java có một thông báo lỗi, như màn hình đang hiện."""),
        st(file_block(sym, "Sym.java", title="Tệp Sym.java") + "<p><b>Đề.</b> Trả lời: (1) tệp nào, dòng mấy, loại lỗi gì? (2) Tên nào sai và nên sửa thành gì? (3) <b>Chọn</b>: nếu trình biên dịch báo 3 lỗi, bạn sửa lỗi nào trước và vì sao?</p>",
           """Câu một, tệp nào, dòng mấy, loại lỗi gì. Câu hai, tên nào sai và nên sửa thành gì. Câu ba là một quyết định, nếu trình biên dịch báo ba lỗi thì sửa lỗi nào trước và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án", "lý do"],
                 [["1", "<code>Sym.java</code>, dòng thứ <b>4</b>, <code>error</code>: cannot find symbol", "ba mảnh đầu của dòng đầu thông báo"],
                  ["2", "<code>tonng</code> → <code>tong</code>", "dòng <code>symbol: variable tonng</code> nêu tên lạ; tệp có biến <code>tong</code> ở dòng thứ ba"],
                  ["3", "lỗi <b>đầu tiên</b>", "các lỗi sau thường là hệ quả; sửa xong biên dịch lại và đếm lại"]]),
           """Đáp án câu một, tệp Sym, dòng bốn, loại lỗi là không tìm thấy ký hiệu, đọc từ dòng đầu của thông báo. Câu hai, tên sai có hai chữ n, sửa thành tên có một chữ n, vì dòng ký hiệu nêu tên lạ, và tệp có biến tong ở dòng ba.
           Câu ba, sửa lỗi đầu tiên rồi biên dịch lại, vì các lỗi sau thường là hệ quả.""",
           focus=["1.2", "1.3", "1.4"]),
        st(term_block(quote, 0, 1) + "<div class='box key'><b>Quyết định:</b> ba lỗi từ <b>một</b> nguyên nhân ở dòng thứ ba. Sửa lỗi đầu (dấu nháy cong thành thẳng), biên dịch lại: cả ba cùng hết.</div>",
           """Về quyết định, ví dụ ba lỗi ở bài trên đều do một nguyên nhân ở dòng ba. Sửa lỗi đầu, đổi dấu nháy cong thành dấu nháy thẳng, biên dịch lại, và cả ba lỗi cùng hết."""),
    ], checks=["'tonng'.replace('nn', 'n') == 'tong'"])
    sc_prac = practice_scene(sc, "Tự làm: sửa ba tệp hỏng bằng cách đọc lỗi", pr_steps(
        st, "FND", "L05",
        """<p><b>Đề</b>: tạo <code>sua.sh</code>. Chép nguyên đoạn dựng ba tệp hỏng (xem <code>de.md</code>: <code>Tong.java</code>, <code>tinh.py</code>, <code>chao.sh</code>). Rồi:</p>
<ol><li>chạy từng tệp một lần, <b>đọc</b> thông báo lỗi (tệp, dòng, loại);</li>
<li>sửa mỗi tệp đúng chỗ (gợi ý: <code>sed -i 's/cũ/mới/' tệp</code> thay chữ trong tệp);</li>
<li>chạy lại cả ba: biên dịch và chạy <code>Tong</code>, <code>python tinh.py</code>, <code>bash chao.sh</code>.</li></ol>
<p class="note">Thông báo lỗi nằm ở luồng lỗi, không tính vào kết quả chấm.</p>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh, chép nguyên đoạn dựng ba tệp hỏng. Chạy từng tệp một lần và đọc thông báo lỗi, tìm tệp, dòng và loại. Sửa mỗi tệp đúng chỗ, bạn có thể dùng lệnh thay chữ trong tệp.
        Cuối cùng chạy lại cả ba, và kết quả cần là bốn dòng. Thông báo lỗi nằm ở luồng lỗi nên không tính vào kết quả chấm. Hãy dừng video và làm.""",
        LAB_OUT, "sua.sh",
        """<div class="box key"><b>Nếu kẹt:</b> <code>Tong.java</code>: thiếu <code>;</code> cuối dòng <code>int b = 250</code>. <code>tinh.py</code>: <code>soluong</code> phải là <code>so_luong</code> (NameError, dòng thứ ba).
<code>chao.sh</code>: <code>ech</code> phải là <code>echo</code> (dòng thứ hai). Lời giải ở <code>labs/FND/L05/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, tệp Java thiếu dấu chấm phẩy cuối dòng khai báo biến b. Tệp ngôn ngữ thứ hai gõ sai tên biến số lượng ở dòng ba. Tệp cửa sổ lệnh gõ sai tên lệnh in chữ ở dòng hai. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L05")
    write_lab("FND", "L05", """# Lab FND L05 — Đọc thông báo lỗi và sửa ba tệp hỏng

Tạo `sua.sh`. **Chép nguyên** đoạn dưới để dựng ba tệp hỏng (`<<'EOF'` nhập nhiều dòng, học dần ở các bài sau):

```bash
""" + LAB_BAD + """
```

Rồi:
1. chạy từng tệp một lần để **đọc** thông báo lỗi: `javac Tong.java`, `python tinh.py`, `bash chao.sh` (thông báo ở luồng lỗi, không tính vào kết quả);
2. **sửa** mỗi tệp đúng chỗ (có thể dùng `sed -i 's/cũ/mới/' tệp`);
3. chạy lại: `javac Tong.java && java Tong`, `python tinh.py`, `bash chao.sh`.

Kết quả cần đúng bốn dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh FND L05 sua.sh`. Cần JDK 21 và Python theo bài đầu tiên.
""", "sh", LAB_BAD + "\n" + LAB_FIX, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("chữ → số thứ tự → byte UTF-8 (1, 2, 3 byte)", "đọc sai bảng mã → ký tự lạ", "xuống dòng: LF hay CR LF",
                 "lỗi = tệp : dòng : loại : mô tả", "dấu ^ = chỗ máy phát hiện", "sửa lỗi ĐẦU rồi biên dịch lại"),
           """Tổng kết chuỗi logic. Chữ có số thứ tự, bảng mã ghi số đó thành một, hai hoặc ba byte. Đọc sai bảng mã thì ra ký tự lạ. Xuống dòng có thể là một hoặc hai ký tự. Thông báo lỗi gồm tệp, dòng, loại, mô tả.
           Dấu mũ là chỗ máy phát hiện. Và hãy sửa lỗi đầu tiên rồi biên dịch lại."""),
        st("""<div class='box key'><b>Tư duy:</b> đọc <b>từ trên xuống</b> chữ đầu tiên máy than phiền, mở đúng tệp ở đúng dòng, nhìn cả vùng quanh nó, sửa <b>một</b> lỗi, chạy lại.</div>
<p>Bài sau: dữ liệu có cấu trúc, CSV, JSON và YAML, để máy và người cùng đọc được.</p>""",
           """Điều cần mang theo, đọc từ trên xuống chữ đầu tiên máy than phiền, mở đúng tệp ở đúng dòng, nhìn cả vùng quanh nó, sửa một lỗi, rồi chạy lại.
           Bài sau, ta học dữ liệu có cấu trúc, gồm các dạng bảng, JSON và YAML, để máy và người cùng đọc được.""", forward_ref=True),
    ])
    return lesson("L05", "soan_ma_utf8_doc_loi", "Bài 5 — Trình soạn mã, UTF-8, xuống dòng và đọc thông báo lỗi",
                  "curriculum/fnd.yaml L05; audit/fnd/verify_fnd.py L05 (javac, python, bash, od, iconv chạy thật); "
                  "The Unicode Standard / RFC 3629 (UTF-8: khuôn 1–4 byte); GNU Coreutils manual (od, cat -A, tr, wc); "
                  "JLS (Java SE 21) §3.10.5, javac báo lỗi (thông báo thật chạy bằng JDK 21); Python Tutorial, Errors and Exceptions; "
                  "số dòng nhật ký 1 201 và 120 001 là số minh hoạ chạy thật",
                  ["Nêu cách UTF-8 ghi một chữ thành 1, 2 hoặc 3 byte và vì sao đọc sai bảng mã ra ký tự lạ",
                   "Tính số byte của một chữ theo khuôn UTF-8 và kiểm bằng lệnh in byte",
                   "Đọc một thông báo lỗi của Java, Python, bash: tệp, dòng, loại và mô tả",
                   "Phân biệt chỗ máy phát hiện lỗi với chỗ gây lỗi",
                   "Kiểm một phép đoán bằng hai đường khác nhau: tính theo khuôn và đếm bằng máy",
                   "Chỉ ra ba lỗi hay gặp và nêu vì sao sửa lỗi đầu tiên trước",
                   "Sửa ba tệp hỏng từ thông báo lỗi và chạy lại cho đúng"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "intuition"), (2, "formula"), (3, "example"), (4, "example"), (5, "check"), (6, "pitfalls"), (7, "practice")])
