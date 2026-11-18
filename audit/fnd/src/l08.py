from lib import *
from labkit import write_lab, practice_steps, practice_scene

DUNG = """CREATE TABLE tai_khoan (
  ma INTEGER PRIMARY KEY, ten TEXT, so_du INTEGER);
INSERT INTO tai_khoan VALUES
  (1, 'An', 500000),
  (2, 'Binh', 1200000),
  (3, 'Chi', 300000);
CREATE TABLE giao_dich (
  id INTEGER PRIMARY KEY, tk INTEGER, so_tien INTEGER);
INSERT INTO giao_dich VALUES
  (1, 1, 200000), (2, 1, -50000), (3, 2, 700000), (4, 3, -100000),
  (5, 2, -300000), (6, 1, 150000), (7, 3, 400000);
"""
LAB_SOL = """CREATE TABLE giao_dich (
  id INTEGER PRIMARY KEY, tk INTEGER, so_tien INTEGER);
INSERT INTO giao_dich VALUES
  (1, 1, 800000), (2, 2, -120000), (3, 3, 450000),
  (4, 1, 300000), (5, 2, 500000), (6, 3, -50000),
  (7, 1, -100000), (8, 2, 70000);
SELECT tk, SUM(so_tien) FROM giao_dich GROUP BY tk ORDER BY tk;
SELECT 'tong', SUM(so_tien) FROM giao_dich;
SELECT 'am', COUNT(*) FROM giao_dich WHERE so_tien < 0;"""
LAB_OUT = "1|1000000\n2|450000\n3|400000\ntong|1850000\nam|3"


def build():
    F = {"dung.sql": DUNG}
    nh = cmd("PhienNH", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'SELECT * FROM tai_khoan;'", "1|An|500000\n2|Binh|1200000\n3|Chi|300000"),
        ("sqlite3 -header $DB 'SELECT * FROM tai_khoan;'", "ma|ten|so_du\n1|An|500000\n2|Binh|1200000\n3|Chi|300000"),
        ("sqlite3 $DB 'SELECT ten, so_du FROM tai_khoan\nWHERE so_du > 400000 ORDER BY so_du DESC;'", "Binh|1200000\nAn|500000"),
        ("sqlite3 $DB 'SELECT tk, SUM(so_tien) AS so_du FROM giao_dich\nGROUP BY tk ORDER BY tk;'", "1|300000\n2|400000\n3|300000"),
        ("sqlite3 $DB 'SELECT SUM(so_tien) FROM giao_dich;'", "1000000"),
        ("sqlite3 $DB \"UPDATE tai_khoan SET ten = 'An Le' WHERE ma = 1;\nSELECT * FROM tai_khoan WHERE ma = 1;\"", "1|An Le|500000"),
        ("sqlite3 $DB 'DELETE FROM giao_dich WHERE id = 2;\nSELECT COUNT(*) FROM giao_dich;'", "6"),
        # từ đây: dựng lại cơ sở dữ liệu sạch (② đã đổi tên và xoá giao dịch), rồi ③ ④ ⑤ chạy tiếp CÙNG phiên
        ("rm -f $DB; sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = 0;\nSELECT * FROM tai_khoan;\nROLLBACK;\nSELECT SUM(so_du) FROM tai_khoan;'", "1|An|0\n2|Binh|0\n3|Chi|0\n2000000"),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = so_du - 100000 WHERE ma = 1;\nSELECT SUM(so_du) FROM tai_khoan;\nROLLBACK;\nSELECT SUM(so_du) FROM tai_khoan;'", "1900000\n2000000"),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = so_du - 100000 WHERE ma = 1;\nUPDATE tai_khoan SET so_du = so_du + 100000 WHERE ma = 2;\nCOMMIT;'", ""),
        ("sqlite3 $DB 'SELECT * FROM tai_khoan;\nSELECT SUM(so_du) FROM tai_khoan;'", "1|An|400000\n2|Binh|1300000\n3|Chi|300000\n2000000"),
        ("sqlite3 $DB 'SELECT tk, SUM(so_tien) AS so_du FROM giao_dich\nGROUP BY tk ORDER BY tk;'", "1|300000\n2|400000\n3|300000"),
        ("sqlite3 $DB 'SELECT SUM(so_tien) FROM giao_dich;'", "1000000"),
    ], files=F)
    asx = cmd("PhienAS", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 -header $DB 'SELECT SUM(so_tien) FROM giao_dich;'", "SUM(so_tien)\n1000000"),
        ("sqlite3 -header $DB 'SELECT SUM(so_tien) AS tong FROM giao_dich;'", "tong\n1000000"),
    ], files=F)
    qwhere = cmd("PhienQuenWhere", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = 0;\nSELECT * FROM tai_khoan;\nROLLBACK;\nSELECT SUM(so_du) FROM tai_khoan;'", "1|An|0\n2|Binh|0\n3|Chi|0\n2000000"),
    ], files=F)
    gd = cmd("PhienGiaoDich", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = so_du - 100000 WHERE ma = 1;\nSELECT SUM(so_du) FROM tai_khoan;\nROLLBACK;\nSELECT SUM(so_du) FROM tai_khoan;'", "1900000\n2000000"),
        ("sqlite3 $DB 'BEGIN;\nUPDATE tai_khoan SET so_du = so_du - 100000 WHERE ma = 1;\nUPDATE tai_khoan SET so_du = so_du + 100000 WHERE ma = 2;\nCOMMIT;'", ""),
        ("sqlite3 $DB 'SELECT * FROM tai_khoan;\nSELECT SUM(so_du) FROM tai_khoan;'", "1|An|400000\n2|Binh|1300000\n3|Chi|300000\n2000000"),
    ], files=F)
    nul = cmd("PhienNull", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB \"INSERT INTO tai_khoan VALUES (4, 'Dung', NULL);\"", ""),
        ("sqlite3 $DB 'SELECT COUNT(*) FROM tai_khoan WHERE so_du = NULL;'", "0"),
        ("sqlite3 $DB 'SELECT COUNT(*) FROM tai_khoan WHERE so_du IS NULL;'", "1"),
        ("sqlite3 $DB 'SELECT 7 / 2, 7 / 2.0;'", "3|3.5"),
        ("sqlite3 $DB \"INSERT INTO tai_khoan VALUES (4, 'Dung', NULL);\" 2>&1 | grep -o 'UNIQUE constraint failed: tai_khoan.ma'", "UNIQUE constraint failed: tai_khoan.ma"),
    ], files=F)
    kgd = cmd("PhienKhongGD", [
        ("DB=ngan_hang.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'UPDATE tai_khoan SET so_du = so_du - 100000 WHERE ma = 1;'", ""),
        ("# may sap o day: lenh cong cho Binh khong bao gio chay", ""),
        ("sqlite3 $DB 'SELECT SUM(so_du) FROM tai_khoan;'", "1900000"),
    ], files=F)
    quymo = cmd("PhienQuyMo", [
        ("(echo id,v; seq 1 70000 | sed 's/.*/&,&/') > big.csv", ""), ("sqlite3 big.db '.import --csv big.csv g'", ""),
        ("sqlite3 big.db 'SELECT COUNT(*) FROM g;'", "70000"), ("sqlite3 big.db 'SELECT v FROM g WHERE id = 54321;'", "54321"),
        ("sqlite3 big.db 'CREATE INDEX idx_id ON g(id);'", ""), ("sqlite3 big.db 'SELECT v FROM g WHERE id = 54321;'", "54321"),
    ])
    quiz = cmd("PhienQuiz", [
        ("DB=nh.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'SELECT SUM(so_tien) FROM giao_dich WHERE tk = 2 AND so_tien > 0;'", "700000"),
        ("sqlite3 $DB 'SELECT tk, COUNT(*) AS n FROM giao_dich GROUP BY tk ORDER BY n DESC LIMIT 1;'", "1|3"),
    ], files=F)

    sc_hook = sc("hook", "hook", "Chuyển tiền cần hai lệnh ghi, và máy sập giữa chừng thì sao?", [
        st(term_block(gd, 2, 3, title="Chuyển 100 000 đồng: mới trừ ở An, chưa cộng ở Bình")
           + "<p>Tổng tiền của cả ngân hàng nhỏ này phải luôn là $2\\,000\\,000$. Ngay giữa hai lệnh, nó là $1\\,900\\,000$: <b>mất $100\\,000$ đồng</b>.</p>",
           """Chào bạn, chuyển tiền cần hai lệnh ghi, trừ ở tài khoản này và cộng ở tài khoản kia. Ta mới trừ một trăm nghìn ở tài khoản An, chưa cộng cho Bình, nên tổng tiền cả ngân hàng nhỏ chỉ còn một triệu chín trăm nghìn.
           Nếu máy sập đúng lúc này thì tiền mất thật. Hôm nay ta học bảng, câu lệnh hỏi bảng, và cơ chế bảo vệ."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li><b>Bảng</b> là gì: hàng, cột, khoá chính? Hỏi một bảng bằng <b>SELECT … WHERE … GROUP BY …</b> thế nào?</li>
<li>Sửa và xoá bằng <b>UPDATE, DELETE</b>: vì sao quên <b>WHERE</b> (<b>mệnh đề</b> điều kiện: phần câu lệnh chọn hàng nào) là tai nạn?</li>
<li><b>Giao dịch</b> (BEGIN … COMMIT/ROLLBACK) bảo vệ việc “hai lệnh hoặc không lệnh nào” ra sao?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Bảng là gì, gồm hàng, cột và khoá chính, và hỏi một bảng bằng ngôn ngữ SQL thế nào. Sửa và xoá ra sao, và vì sao quên mệnh đề điều kiện, tức phần câu lệnh chọn ra những hàng cần làm, là tai nạn.
           Và giao dịch bảo vệ việc hai lệnh hoặc không lệnh nào ra sao."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp CSV, lọc, đếm, tổng", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① bảng bằng chữ", "tệp CSV: mỗi dòng một hàng, các cột cách nhau bằng dấu phẩy, dòng đầu là tên cột"],
                  ["② lọc", "<code>grep -v</code>, <code>cut</code>: giữ hàng hay cột cần dùng"],
                  ["③ nhóm và đếm", "<code>sort | uniq -c</code>: gom các dòng giống nhau và đếm"],
                  ["④ tổng không đổi", "tiền chuyển đi bằng tiền nhận về: kiểm bằng cách cộng toàn bộ"]]),
           """Ta ôn lại bốn điều. Bảng bằng chữ là tệp bảng, mỗi dòng một hàng, các cột cách nhau bằng dấu phẩy. Ta đã lọc hàng và cột, rồi gom các dòng giống nhau và đếm.
           Và ta biết tiền chuyển đi bằng tiền nhận về, nên kiểm bằng cách cộng toàn bộ.""",
           focus=[1, "1.2", ["1.3", "1.4"], "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã: bảng, hàng, cột, khoá chính và các câu lệnh", [
        st(table(["thuật ngữ", "nghĩa"],
                 [["<b>cơ sở dữ liệu</b>", "nơi lưu dữ liệu có tổ chức; ở đây là tệp <code>ngan_hang.db</code> do chương trình <b>sqlite</b> quản lý"],
                  ["<b>bảng</b>", "như một tờ bảng tính: <b>cột</b> có tên và kiểu (<code>INTEGER</code> số nguyên, <code>TEXT</code> chữ), <b>hàng</b> là một bản ghi"],
                  ["<b>khoá chính</b>", "<code>PRIMARY KEY</code>: cột <b>không trùng giữa hai hàng</b>, dùng để chỉ đúng một hàng (ví dụ mã tài khoản)"],
                  ["<b>NULL</b>", "“chưa có giá trị” (không phải số $0$, không phải chữ rỗng)"]]),
           """Bảng này giải mã bốn thuật ngữ. Cơ sở dữ liệu là nơi lưu dữ liệu có tổ chức, ở đây là một tệp do một chương trình nhỏ quản lý. Bảng giống tờ bảng tính, cột có tên và kiểu, hàng là một bản ghi.
           Khoá chính là cột không trùng giữa hai hàng, dùng để chỉ đúng một hàng. Và giá trị rỗng nghĩa là chưa có giá trị, không phải số không.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["câu lệnh", "đọc là", "nghĩa"],
                 [["<code>sqlite3 $DB 'câu SQL;'</code>".replace("$", "<span>&#36;</span>"), "chạy một câu SQL", "chạy câu trong nháy đơn trên tệp cơ sở dữ liệu có tên ở biến <code>DB</code>; dấu <code>;</code> <b>kết thúc một câu SQL</b>, như dấu chấm hết câu"],
                  ["<code>CREATE TABLE</code>", "tạo bảng", "khai tên bảng, tên và kiểu từng cột"],
                  ["<code>INSERT INTO … VALUES</code>", "chèn", "thêm hàng"]]),
           """Bảng thứ hai là các câu lệnh. Lệnh chạy chương trình nhỏ kèm câu SQL trong nháy đơn chạy câu đó trên tệp cơ sở dữ liệu, và dấu chấm phẩy kết thúc một câu SQL, như dấu chấm hết câu. Lệnh tạo bảng khai tên và kiểu từng cột. Lệnh chèn thêm hàng.""",
           focus=[1, "1.2", "1.3", "1.4"], clear=True),
        st(table(["câu lệnh", "đọc là", "nghĩa"],
                 [["<code>SELECT cột FROM bảng WHERE điều_kiện</code>", "chọn", "đọc các hàng thoả điều kiện; <code>SELECT *</code>: dấu <code>*</code> = <b>mọi cột</b>; <code>COUNT(*)</code> đếm số hàng"],
                  ["<code>ORDER BY</code> và <code>LIMIT</code>", "sắp xếp và giới hạn", "sắp theo cột (<code>DESC</code> giảm dần); lấy vài hàng đầu"],
                  ["<code>GROUP BY</code> + <code>SUM, COUNT</code>", "nhóm theo + hàm gộp", "gom hàng cùng giá trị cột nhóm; <code>SUM</code> tổng, <code>COUNT</code> đếm"],
                  ["<code>UPDATE … SET … WHERE</code><br>và <code>DELETE FROM … WHERE</code>", "sửa và xoá", "đổi hoặc bỏ <b>các hàng thoả WHERE</b>"]]),
           """Lệnh chọn đọc các hàng thoả điều kiện; dấu sao là mọi cột, và hàm đếm với dấu sao đếm số hàng. Sắp xếp theo một cột, giảm dần nếu thêm một chữ, và giới hạn lấy vài hàng đầu.
           Nhóm theo cùng hàm gộp gom các hàng cùng giá trị rồi cộng hoặc đếm. Lệnh sửa và lệnh xoá tác động lên các hàng thoả mệnh đề điều kiện.""",
           focus=["1.2", "1.3", "1.4", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: hai bảng, và phép nhóm gom hàng lại", [
        st(svg(1500, 520,
               box(10, 10, 640, 70, "bảng tai_khoan (3 hàng)", C_BLUE, 28, bold=True),
               box(10, 90, 190, 50, "ma", C_GRAY, 24, bold=True), box(205, 90, 220, 50, "ten", C_GRAY, 24, bold=True), box(430, 90, 220, 50, "so_du", C_GRAY, 24, bold=True),
               box(10, 145, 190, 50, "1", C_BLUE, 24), box(205, 145, 220, 50, "An", C_BLUE, 24), box(430, 145, 220, 50, "500000", C_BLUE, 24),
               box(10, 200, 190, 50, "2", C_BLUE, 24), box(205, 200, 220, 50, "Binh", C_BLUE, 24), box(430, 200, 220, 50, "1200000", C_BLUE, 24),
               box(10, 255, 190, 50, "3", C_BLUE, 24), box(205, 255, 220, 50, "Chi", C_BLUE, 24), box(430, 255, 220, 50, "300000", C_BLUE, 24),
               box(700, 10, 790, 70, "bảng giao_dich (7 hàng), cột tk trỏ tới tai_khoan.ma", C_GREEN, 28, bold=True),
               box(700, 90, 190, 50, "id", C_GRAY, 24, bold=True), box(895, 90, 190, 50, "tk", C_GRAY, 24, bold=True), box(1090, 90, 400, 50, "so_tien", C_GRAY, 24, bold=True),
               box(700, 145, 190, 50, "1", C_GREEN, 24), box(895, 145, 190, 50, "1", C_AMBER, 24), box(1090, 145, 400, 50, "200000", C_GREEN, 24),
               box(700, 200, 190, 50, "2", C_GREEN, 24), box(895, 200, 190, 50, "1", C_AMBER, 24), box(1090, 200, 400, 50, "-50000", C_GREEN, 24),
               box(700, 255, 190, 50, "6", C_GREEN, 24), box(895, 255, 190, 50, "1", C_AMBER, 24), box(1090, 255, 400, 50, "150000", C_GREEN, 24),
               txt(1090, 345, "… (còn 4 hàng của tk 2 và 3)", 24, "start", "#6b7280"),
               box(10, 400, 1480, 100, ["GROUP BY tk: ba hàng của tk 1 gom thành một nhóm", "SUM(so_tien) = 200000 - 50000 + 150000 = 300000"], C_AMBER, 28, bold=True)),
           """Hình này là hai bảng. Bảng tài khoản có ba hàng, mỗi hàng một tài khoản. Bảng giao dịch có bảy hàng, và một cột cho biết giao dịch thuộc tài khoản nào, tức trỏ tới mã ở bảng kia.
           Nhóm theo cột tài khoản gom các hàng cùng giá trị thành một nhóm. Ví dụ ba hàng của tài khoản một gom thành một nhóm có tổng ba trăm nghìn."""),
        st(svg(1500, 380,
               box(20, 130, 280, 110, ["BEGIN", "bắt đầu"], C_BLUE, bold=True),
               arrow(305, 185, 400, 185, "#2a78d6"),
               box(410, 60, 320, 100, ["lệnh 1: trừ An", "(mới trong nháp)"], C_AMBER, bold=True),
               box(410, 210, 320, 100, ["lệnh 2: cộng Bình", "(mới trong nháp)"], C_AMBER, bold=True),
               arrow(735, 110, 880, 110, "#16a34a"), arrow(735, 260, 880, 260, "#dc2626"),
               box(890, 50, 580, 110, ["COMMIT: cả hai lệnh có hiệu lực cùng lúc", "(tổng tiền luôn 2 000 000)"], C_GREEN, bold=True),
               box(890, 200, 580, 110, ["ROLLBACK / máy sập: cả hai bị huỷ", "(như chưa từng chạy)"], C_RED, bold=True),
               txt(750, 350, "giao dịch = “tất cả hoặc không gì cả”", 28, "middle", "#1f2937", True)),
           """Hình thứ hai là giao dịch. Ta bắt đầu giao dịch, rồi chạy hai lệnh, và chúng mới chỉ nằm trong bản nháp. Nếu kết thúc bằng lệnh chốt thì cả hai lệnh có hiệu lực cùng lúc, tổng tiền luôn là hai triệu.
           Nếu kết thúc bằng lệnh huỷ, hoặc máy sập giữa chừng, thì cả hai bị huỷ như chưa từng chạy. Giao dịch nghĩa là tất cả hoặc không gì cả."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: từ câu hỏi bằng lời tới câu lệnh chọn", [
        st(file_block(cmd("Mau", [("true", "")], files=F), "dung.sql", title="Dựng dữ liệu: tệp dung.sql (bảng tai_khoan)", lines=(1, 6))
           + term_block(nh, 0, 2, title="Nạp tệp vào cơ sở dữ liệu")
           + "<p><code>DB=ngan_hang.db</code> đặt biến <code>DB</code> giữ tên tệp cơ sở dữ liệu. Dấu <code>&lt;</code> trong <code>sqlite3 $DB &lt; dung.sql</code> đưa nội dung tệp <code>dung.sql</code> vào làm chữ vào của <code>sqlite3</code>, như thể bạn gõ từng dòng đó.</p>".replace("$", "<span>&#36;</span>"),
           """Vì các câu hỏi sau cần có bảng, ta dựng dữ liệu trước. Tệp lệnh khai bảng tài khoản và chèn ba hàng. Dòng đầu đặt một biến giữ tên tệp cơ sở dữ liệu. Dấu nhỏ hơn ở dòng sau đưa nội dung tệp vào làm chữ vào của chương trình, như thể bạn gõ từng dòng đó, và tạo ra tệp ngân hàng chấm d b."""),
        st(term_block(nh, 4, 5, title="Câu hỏi: tài khoản nào có số dư trên 400 000, sắp từ lớn xuống nhỏ?")
           + "<p><b>Bước 1.</b> Chọn <b>cột</b> cần xem: <code>SELECT ten, so_du</code>. <b>Bước 2.</b> Chỉ ra <b>bảng</b>: <code>FROM tai_khoan</code>. "
             "<b>Bước 3.</b> Lọc <b>hàng</b>: <code>WHERE so_du &gt; 400000</code>. <b>Bước 4.</b> Sắp xếp: <code>ORDER BY so_du DESC</code>.</p>"
           + "<p class='note'>Lệnh viết trên hai dòng: sau dấu nháy mở, dòng kế bắt đầu bằng <code>&gt;</code> do cửa sổ lệnh in ra, nghĩa là nó còn <b>chờ nháy đóng</b>; đừng gõ dấu đó. Dấu <code>&gt;</code> trong <code>so_du &gt; 400000</code> mới là phép so sánh.</p>",
           """Câu hỏi là tài khoản nào có số dư trên bốn trăm nghìn, sắp từ lớn xuống nhỏ. Lệnh viết trên hai dòng, dấu lớn hơn ở đầu dòng thứ hai do cửa sổ lệnh tự in vì còn chờ dấu nháy đóng, bạn không gõ. Bước một, chọn cột tên và số dư. Bước hai, chỉ ra bảng. Bước ba, lọc hàng có số dư lớn hơn bốn trăm nghìn.
           Bước bốn, sắp giảm dần theo số dư. Kết quả có Bình và An, còn Chi bị loại."""),
        st(file_block(cmd("Mau3", [("true", "")], files=F), "dung.sql", title="Bảng giao_dich: bảy giao dịch (cột tk là mã tài khoản)", lines=(7, 11))
           + "<p>Vì mỗi hàng ghi một lần tiền vào hoặc ra của một tài khoản, cột <code>tk</code> cho biết tài khoản nào. Cột <code>so_tien</code> dương là tiền vào, âm là tiền ra. Đoạn trên nằm trong tệp <code>dung.sql</code>.</p>",
           """Bảng giao dịch có bảy hàng, đây là toàn bộ. Mỗi hàng có mã giao dịch, mã tài khoản mà nó thuộc về, và số tiền, vì mỗi hàng ghi một lần tiền vào hoặc ra. Số tiền dương là tiền vào, số tiền âm là tiền ra.
           Bạn có thể chép đoạn này vào tệp dựng dữ liệu để chạy lại các câu lệnh sau.""", clear=True),
        st(term_block(asx, 2, 4, title="Bí danh cột bằng AS")
           + "<p class='note'><code>AS</code> đặt <b>bí danh</b>: một cái tên mới cho cột kết quả. Không có <code>AS</code>, đầu cột là chính biểu thức <code>SUM(so_tien)</code>; có <code>AS tong</code>, đầu cột là <code>tong</code>. "
             "Cờ <code>-header</code> của <code>sqlite3</code> bảo in thêm một dòng tên cột; dữ liệu không đổi.</p>",
           """Trước câu hỏi tiếp, một từ mới là A S, nghĩa là đặt bí danh, tức một cái tên mới cho cột kết quả. Không có nó, đầu cột là cả biểu thức cộng; có nó, đầu cột là chữ tong.""", introduces=["fnd_as"], clear=True),
        st(term_block(nh, 5, 7, title="Câu hỏi: số dư của từng tài khoản theo sổ giao dịch?")
           + "<p>Vì mỗi hàng giao dịch thuộc một <code>tk</code>, <b>nhóm</b> theo <code>tk</code> rồi <b>cộng</b> <code>so_tien</code>. Kiểm: $300\\,000 + 400\\,000 + 300\\,000 = \\hl{1\\,000\\,000}$ = tổng toàn bảng ✓</p>"
           + "<p class='note'>Số này khác số dư lưu ở bảng <code>tai_khoan</code> (An $500\\,000$, Bình $1\\,200\\,000$): hai bảng ở đây được dựng <b>riêng</b>, chỉ để minh hoạ <code>GROUP BY</code>, nên không cần khớp nhau.</p>",
           """Câu hỏi thứ hai là số dư của từng tài khoản theo sổ giao dịch. Vì mỗi hàng giao dịch thuộc về một tài khoản, ta nhóm theo cột tài khoản rồi cộng số tiền. Làm thử, ba trăm nghìn cộng bốn trăm nghìn cộng ba trăm nghìn bằng một triệu, đúng bằng tổng toàn bảng, nên không bỏ sót hàng nào. Số này khác số dư ở bảng tài khoản vì hai bảng dựng riêng."""),
    ], checks=["200000 - 50000 + 150000 == 300000", "700000 - 300000 == 400000", "-100000 + 400000 == 300000",
               "300000 + 400000 + 300000 == 1000000", "sum([200000, -50000, 700000, -100000, -300000, 150000, 400000]) == 1000000"])
    sc_ex = sc("example", "example", "Ví dụ: sửa, xoá và giao dịch trên cùng cơ sở dữ liệu, năm phép làm", [
        st(term_block(nh, 2, 4, title="① Đọc cả bảng, rồi đọc kèm tên cột (-header)")
           + "<p>Ba hàng, ba cột. Cột <code>ma</code> là khoá chính nên không hàng nào trùng mã.</p>",
           """Phép làm thứ nhất, đọc cả bảng. Có ba hàng, ba cột. Cờ tiêu đề cho in thêm dòng tên cột, tiện cho người đọc. Cột mã là khoá chính nên không có hai hàng trùng mã."""),
        st(term_block(nh, 7, 9, title="② Sửa MỘT hàng bằng WHERE, rồi xoá MỘT giao dịch")
           + "<p><code>WHERE ma = 1</code> chỉ chạm hàng của An. Nháy <b>kép</b> ngoài bao cả câu SQL vì bên trong đã có nháy <b>đơn</b> quanh chữ <code>An Le</code>. Xoá <code>id = 2</code> làm số giao dịch từ $7$ xuống $6$.</p>",
           """Phép làm thứ hai, sửa và xoá đúng một hàng. Mệnh đề điều kiện mã bằng một chỉ chạm vào hàng của An, đổi tên thành An Le. Câu nằm trong nháy kép vì bên trong đã có nháy đơn quanh tên. Xoá giao dịch số hai làm số giao dịch từ bảy xuống sáu."""),
        st(term_block(nh, 9, 11, title="③ Dựng lại cơ sở dữ liệu sạch, rồi quên WHERE: sửa MỌI hàng (trong giao dịch để huỷ được)")
           + "<p>Dòng đầu " + code("rm -f $DB; sqlite3 $DB < dung.sql") + " <b>dựng lại</b> từ tệp dựng dữ liệu: xoá tệp cũ rồi nạp lại, nên An lại tên <code>An</code> và đủ $7$ giao dịch, không còn dấu vết của ②. <code>rm -f</code> xoá tệp mà không hỏi; dấu <code>;</code> đặt hai lệnh trên một dòng, chạy lần lượt. "
             "Rồi cả ba tài khoản về $0$; <code>ROLLBACK</code> huỷ, tổng trở lại $2\\,000\\,000$ ✓</p>",
           """Phép làm thứ ba, quên mệnh đề điều kiện. Trước hết ta dựng lại cơ sở dữ liệu sạch, xoá tệp cũ rồi nạp lại; dấu chấm phẩy đặt hai lệnh đó trên một dòng. Lệnh sửa đưa số dư cả ba tài khoản về không. Ta chạy trong một giao dịch nên lệnh huỷ đưa mọi thứ về như cũ, tổng lại là hai triệu. Ngoài giao dịch thì không còn đường quay lại."""),
        st(term_block(nh, 11, 12, title="④ Giao dịch dở dang: mất tiền trong nháp, ROLLBACK trả lại"),
           """Phép làm thứ tư, giao dịch dở dang. Sau lệnh trừ, tổng tiền trong nháp là một triệu chín trăm nghìn, nhưng giao dịch chưa chốt. Lệnh huỷ đưa tổng trở lại hai triệu, như chưa có gì xảy ra."""),
        st(term_block(nh, 12, 14, title="⑤ Hai lệnh trong một giao dịch rồi COMMIT")
           + "<p>An $500\\,000 - 100\\,000 = \\hl{400\\,000}$; Bình $1\\,200\\,000 + 100\\,000 = \\hl{1\\,300\\,000}$; tổng vẫn $2\\,000\\,000$ ✓</p>",
           """Phép làm thứ năm, hai lệnh trong một giao dịch rồi chốt. An còn bốn trăm nghìn, Bình có một triệu ba trăm nghìn, Chi giữ nguyên, và tổng vẫn là hai triệu. Hai lệnh có hiệu lực cùng lúc, hoặc cả hai không có hiệu lực.""", clear=True),
    ], checks=["500000 - 100000 == 400000", "1200000 + 100000 == 1300000", "400000 + 1300000 + 300000 == 2000000", "7 - 1 == 6", "500000 + 1200000 + 300000 == 2000000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tổng hai cách và đếm hai cách", [
        st(term_block(nh, 14, 16, title="Cách 1: tổng theo nhóm (trên cơ sở dữ liệu đã dựng lại ở ③; giao dịch ⑤ không đụng bảng giao_dich)") + "<p>Cộng ba nhóm: $300\\,000 + 400\\,000 + 300\\,000 = 1\\,000\\,000$.</p>"
           + "<p>Cách 2: một câu lệnh cộng cả bảng cho $1\\,000\\,000$ (đã in ở trên). Hai đường độc lập cùng ra một số ✓</p>",
           """Đường kiểm khác, tính tổng bằng hai cách, trên cơ sở dữ liệu đã dựng lại ở phép thứ ba. Cách một cộng ba nhóm, ra một triệu. Cách hai dùng một câu lệnh cộng cả bảng, cũng ra một triệu, nên ta tin kết quả nhóm."""),
        st(term_block(nul, 2, 6, title="Kiểm NULL: so sánh bằng không bao giờ đúng với NULL")
           + "<p>Ta chèn thêm tài khoản Dung với số dư NULL (bảng thành $4$ hàng, đúng một hàng NULL). <code>= NULL</code> đếm ra $0$, <code>IS NULL</code> đếm ra $1$. "
             "Và $7 / 2 = 3$ (chia số nguyên), $7 / 2.0 = 3{,}5$: kiểu của số quyết định kết quả; tiền nên lưu <b>số nguyên theo đồng</b>. "
             "Mã $4$ là khoá chính: chạy lại lệnh chèn trên <b>cùng</b> cơ sở dữ liệu sẽ báo <code>UNIQUE constraint failed</code>; muốn làm lại thì dựng lại cơ sở dữ liệu.</p>",
           """Kiểm thêm giá trị rỗng. Ta chèn thêm một tài khoản tên Dung với số dư rỗng, nên bảng có bốn hàng và đúng một hàng rỗng. Dấu bằng với giá trị rỗng không bao giờ đúng, nên đếm ra không. Phải dùng cụm là giá trị rỗng, thì đếm ra một.
           Bảy chia hai ra ba vì chia số nguyên, còn bảy chia hai chấm không ra ba rưỡi, nên tiền lưu bằng số nguyên theo đồng.""", clear=True),
    ], checks=["300000 + 400000 + 300000 == 1000000", "7 // 2 == 3", "7 / 2.0 == 3.5"])
    sc_scale = sc("scale", "example", "Khi bảng nhân lên: quét cả bảng hay tra theo chỉ mục", [
        st(term_block(quymo, 0, 2, title="Dựng tệp CSV 70 000 hàng, nạp thành bảng g")
           + "<p><code>seq 1 70000</code> in các số 1 tới 70000, mỗi số một dòng; <code>sed 's/.*/&amp;,&amp;/'</code> thay <b>cả dòng</b> (<code>.*</code> khớp cả dòng) bằng chữ mới, mà <code>&amp;</code> là <b>chính phần vừa khớp</b>: dòng <code>5</code> thành <code>5,5</code>. "
             "Ngoặc tròn gộp phần tạo dòng tiêu đề <code>id,v</code> và 70 000 dòng số vào cùng một tệp <code>big.csv</code>; dấu <code>;</code> trong ngoặc xếp hai phần chạy lần lượt: <code>echo</code> in dòng tiêu đề trước, rồi mới tới các dòng số.</p>"
           + "<p><code>.import</code> là <b>lệnh riêng</b> của sqlite3 (bắt đầu bằng dấu chấm, không phải câu SQL): đọc tệp CSV thành bảng <code>g</code>; "
             "vì chưa có bảng, dòng đầu <code>id,v</code> thành <b>tên hai cột</b>.</p>",
           """Ta dựng tệp bảy mươi nghìn hàng rồi nạp vào cơ sở dữ liệu. Lệnh in dãy số in các số từ một tới bảy mươi nghìn; lệnh thay chữ biến mỗi dòng thành chính nó, dấu phẩy, rồi chính nó nữa, nên dòng năm thành năm phẩy năm.
           Ngoặc tròn gộp dòng tiêu đề, chạy trước nhờ dấu chấm phẩy, với các dòng số vào một tệp. Lệnh nạp bắt đầu bằng dấu chấm là lệnh riêng của chương trình, không phải câu SQL, và dòng đầu thành tên cột."""),
        st(term_block(quymo, 2, 4, title="Đếm hàng, rồi tra một hàng theo id")
           + "<p>Đếm ra đúng $70\\,000$ hàng dữ liệu (dòng tiêu đề đã thành tên cột). Không có chỉ mục thì cơ sở dữ liệu phải <b>xem lần lượt từng hàng</b> để tìm <code>id = 54321</code>.</p>",
           """Đếm ra đúng bảy mươi nghìn hàng dữ liệu, vì dòng tiêu đề đã thành tên cột. Rồi ta tra một hàng theo mã.
           Nếu không có chỉ mục, tức mục lục, thì cơ sở dữ liệu phải xem lần lượt từng hàng cho tới khi gặp hàng cần tìm.""", clear=True),
        st(term_block(quymo, 4, 6, title="Tạo chỉ mục cho cột id, rồi tra lại: kết quả giống hệt")
           + "<p><code>CREATE INDEX idx_id ON g(id)</code> dựng <b>mục lục</b> cho cột <code>id</code>: tên mục lục, bảng, cột. Câu tra <b>không đổi</b>, chỉ cách tìm đổi: tra qua mục lục thay vì xem từng hàng.</p>",
           """Làm chỉ mục chỉ cần một lệnh, nêu tên mục lục, tên bảng và cột. Sau đó câu tra giữ nguyên và kết quả vẫn y hệt. Khác biệt chỉ nằm ở cách tìm, là tra qua mục lục thay vì xem từng hàng."""),
        st("<div class='box key'><b>Tìm nhị phân</b> (cách dễ hình dung nhất của việc tra qua mục lục): với danh sách <b>đã xếp thứ tự</b>, xem hàng ở <b>giữa</b>, bỏ nửa không chứa kết quả, rồi lặp lại trên nửa còn lại. "
           "Mỗi lần xem là bỏ được một nửa, nên $70\\,000$ hàng cần tối đa khoảng $17$ lần chia đôi.</div>"
           + "<p>Chỉ mục thật của SQLite là <b>cây B</b> (mỗi nút có rất nhiều nhánh, nên đọc ít trang hơn nữa); số bước ở bảng sau là <b>cận trên</b> theo tìm nhị phân, để so cỡ, không đo thời gian.</p>",
           """Tìm nhị phân là cách dễ hình dung nhất của việc tra qua mục lục. Với danh sách đã xếp thứ tự, ta xem hàng ở giữa, bỏ nửa không chứa kết quả, rồi lặp lại trên nửa còn lại. Vì vậy bảy mươi nghìn hàng cần tối đa khoảng mười bảy lần chia đôi.
           Số bước ở bảng sau chỉ là cận trên, không đo thời gian."""),
        st(table(["số hàng", "không chỉ mục: xem tối đa", "có chỉ mục: cận trên theo tìm nhị phân"],
                 [["×1: 7", "7 hàng", "3 bước"], ["×100: 700", "700 hàng", "10 bước"], ["×10 000: 70 000", "70 000 hàng", "17 bước"]])
           + "<div class='box key'><b>Đánh đổi:</b> chỉ mục làm <b>đọc nhanh</b> nhưng làm <b>ghi chậm hơn</b> và tốn thêm chỗ, vì mỗi lần ghi phải cập nhật cả mục lục. "
             "Khoá chính tự có chỉ mục. Số liệu là ước tính theo công thức (không đo thời gian).</div>",
           """Bảng này là số hàng phải xem trong trường hợp xấu nhất. Bảy, bảy trăm, bảy mươi nghìn hàng, so với ba, mười, mười bảy bước. Chênh lệch tăng nhanh theo kích thước bảng.
           Chỉ mục làm đọc nhanh nhưng làm ghi chậm hơn và tốn thêm chỗ, vì mỗi lần ghi phải cập nhật cả mục lục. Khoá chính tự có chỉ mục."""),
    ], checks=["10000 * 7 == 70000", "100 * 7 == 700", "__import__('math').ceil(__import__('math').log2(7)) == 3",
               "__import__('math').ceil(__import__('math').log2(700)) == 10", "__import__('math').ceil(__import__('math').log2(70000)) == 17"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên <code>WHERE</code> trong <code>UPDATE</code> hoặc <code>DELETE</code>: tác động lên <b>mọi</b> hàng.</div>'
           + term_block(qwhere, 2, 3),
           """Lỗi thứ nhất, của người mới, là quên mệnh đề điều kiện trong lệnh sửa hoặc lệnh xoá, nên tác động lên mọi hàng."""),
        st("<p>Phép thử: viết <b>SELECT</b> với cùng <code>WHERE</code> trước để đếm số hàng; chạy trong giao dịch và xem kết quả rồi mới chốt.</p>"
           + "<p class='note'>Chạy trên cơ sở dữ liệu <b>vừa dựng lại sạch</b> từ <code>dung.sql</code> (ba hàng). Nếu bạn đã chèn Dung ở phép kiểm trước và chạy liền, sẽ thấy thêm hàng <code>4|Dung|0</code> (NULL cũng bị đặt thành $0$); tổng vẫn $2\\,000\\,000$.</p>",
           """Phép thử là viết lệnh chọn với cùng mệnh đề đó trước để đếm số hàng.
           Rồi chạy trong giao dịch, xem kết quả, và chỉ chốt khi đúng. Ví dụ trên dùng cơ sở dữ liệu dựng lại sạch; nếu còn hàng Dung từ phép kiểm trước, bạn thấy thêm hàng thứ tư."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> So sánh với NULL bằng dấu <code>=</code>.</div>'
           + term_block(nul, 3, 5) + "<p>Bảng có một hàng NULL (Dung, mã $4$, chèn ở phép kiểm trước; chèn lại cùng mã sẽ báo <code>UNIQUE constraint failed</code>, vì mã là khoá chính). NULL nghĩa là “không biết”; “không biết = không biết” cũng không biết, nên cho kết quả <b>không đúng</b>. Dùng <code>IS NULL</code>. Hàm <code>SUM</code> bỏ qua NULL.</p>",
           """Lỗi thứ hai, cũng của người mới, là so sánh với giá trị rỗng bằng dấu bằng. Giả sử bảng có một hàng rỗng, như tài khoản Dung ở phép kiểm trước. Giá trị rỗng nghĩa là không biết, và không biết bằng không biết cũng là không biết, nên kết quả không đúng. Hãy dùng cụm là giá trị rỗng."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Chuyển tiền bằng hai lệnh rời nhau, không giao dịch.</div>'
           + term_block(kgd, 2, 5) + "<p>Dòng bắt đầu bằng <code>#</code> là <b>chú thích</b>: máy bỏ qua, chỉ để người đọc. Lệnh trừ ở An đã chốt ngay; máy sập trước lệnh cộng cho Bình: tổng còn $1\\,900\\,000$ và <b>không còn đường quay lại</b>. "
             "<b>Bất biến</b> là điều luôn phải đúng, ở đây là “tổng không đổi”; nó chỉ giữ được khi hai lệnh nằm <b>trong một giao dịch</b>.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là chuyển tiền bằng hai lệnh rời nhau, không có giao dịch. Mỗi lệnh chạy riêng thì có hiệu lực ngay. Lệnh trừ ở An đã chốt, dòng chú thích nói máy sập, nên lệnh cộng cho Bình không chạy, tổng còn một triệu chín trăm nghìn.
           Bất biến là điều luôn phải đúng, ở đây là tổng không đổi, và chỉ giữ được khi hai lệnh nằm trong một giao dịch."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(file_block(cmd("Mau2", [("true", "")], files=F), "dung.sql", title="Dùng lại dữ liệu của bài (tệp dung.sql): bảng giao_dich, đủ 7 hàng", lines=(7, 11))
           + "<p><b>Đề.</b> (1) Viết SELECT cho <b>tổng tiền nạp</b> (số dương) của tài khoản $2$. (2) Viết SELECT cho tài khoản có <b>nhiều giao dịch nhất</b> kèm số giao dịch. "
             "(3) <b>Chọn</b>: chuyển $100\\,000$ từ An sang Bình bằng hai UPDATE: có cần giao dịch không, vì sao?</p>",
           """Bây giờ tới phần bạn tự làm, trên bảng giao dịch của bài. Câu một, viết lệnh chọn tổng tiền nạp, tức số dương, của tài khoản hai. Câu hai, viết lệnh chọn tài khoản có nhiều giao dịch nhất, kèm số giao dịch.
           Câu ba là một quyết định, chuyển một trăm nghìn từ An sang Bình bằng hai lệnh sửa thì có cần giao dịch không, và vì sao. Hãy dừng video và làm.""", pause=90),
        st(term_block(quiz, 2, 4, title="Máy chạy thật")
           + table(["câu", "câu lệnh", "kết quả và lý do"],
                   [["1", "<code>SELECT SUM(so_tien) FROM giao_dich WHERE tk = 2 AND so_tien &gt; 0;</code>", "<code>AND</code> = cả hai điều kiện cùng đúng. Ra $700\\,000$: chỉ giao dịch nạp của tk 2 (id 3); id 5 âm bị loại"],
                    ["2", "<code>SELECT tk, COUNT(*) AS n FROM giao_dich GROUP BY tk ORDER BY n DESC LIMIT 1;</code>", "<code>1|3</code>: tk 1 có $3$ giao dịch, nhiều nhất"]]),
           """Đáp án, máy chạy thật cho đúng hai kết quả. Câu một, chữ A N D đòi cả hai điều kiện cùng đúng, nên chỉ giao dịch nạp của tài khoản hai là số ba, bảy trăm nghìn, còn giao dịch âm bị loại. Câu hai, nhóm theo tài khoản, đếm, sắp giảm dần và lấy một hàng, ra tài khoản một có ba giao dịch."""),
        st("<div class='box key'><b>Quyết định:</b> <b>có</b>, bắt buộc dùng giao dịch: hai UPDATE phải <b>cùng có hiệu lực hoặc cùng không</b>. "
           "Sau <code>COMMIT</code> kiểm bất biến: tổng số dư vẫn $2\\,000\\,000$. Không giao dịch thì lỗi giữa chừng làm mất $100\\,000$ (bước ④ của ví dụ).</div>",
           """Về quyết định, có, bắt buộc dùng giao dịch, vì hai lệnh sửa phải cùng có hiệu lực hoặc cùng không. Sau khi chốt, hãy kiểm quy tắc tổng số dư vẫn là hai triệu. Không có giao dịch thì lỗi giữa chừng làm mất một trăm nghìn, như ở phép làm thứ tư.""", clear=True),
    ], checks=["[700000, -300000][0] == 700000", "[1, 1, 1, 2, 2, 3, 3].count(1) == 3"])
    sc_prac = practice_scene(sc, "Tự làm: tạo bảng, chèn dữ liệu và in số dư theo tài khoản", pr_steps(
        st, "FND", "L08",
        """<p><b>Đề</b>: viết <code>so_du.sql</code> (một tệp SQL), gồm theo thứ tự:</p>
<ol><li><code>CREATE TABLE giao_dich</code> với ba cột <code>id</code> (khoá chính), <code>tk</code>, <code>so_tien</code> (cả ba <code>INTEGER</code>);</li>
<li><code>INSERT</code> 8 hàng: <code>(1,1,800000) (2,2,-120000) (3,3,450000) (4,1,300000) (5,2,500000) (6,3,-50000) (7,1,-100000) (8,2,70000)</code>;</li>
<li><code>SELECT</code> số dư từng tài khoản, sắp theo <code>tk</code>; rồi <code>SELECT 'tong', SUM(so_tien)</code>; rồi <code>SELECT 'am', COUNT(*)</code> số giao dịch âm.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Việc đầu tiên là viết một tệp chứa các câu lệnh SQL. Một, tạo bảng giao dịch với ba cột số nguyên, trong đó cột mã là khoá chính. Hai, chèn tám hàng theo danh sách trong đề. Ba, in số dư từng tài khoản sắp theo tài khoản, rồi in một dòng có chữ tổng kèm tổng toàn bảng, rồi một dòng có chữ âm kèm số giao dịch âm.
        Hãy dừng video và làm.""",
        LAB_OUT, "so_du.sql",
        """<div class="box key"><b>Nếu kẹt:</b> <code>SELECT tk, SUM(so_tien) FROM giao_dich GROUP BY tk ORDER BY tk;</code>. Dòng tổng: <code>SELECT 'tong', SUM(so_tien) FROM giao_dich;</code>.
Dòng âm: thêm <code>WHERE so_tien &lt; 0</code> và <code>COUNT(*)</code>. Chấm bằng máy: <code>bash labs/cham.sh FND L08 so_du.sql</code> (cần chương trình <code>sqlite3</code> đã cài ở bài đầu). Lời giải ở <code>labs/FND/L08/loi_giai.sql</code>.</div>""",
        """Nếu kẹt, số dư từng tài khoản là lệnh chọn tài khoản và tổng, nhóm theo tài khoản, sắp theo tài khoản. Dòng tổng chọn một chữ cố định kèm tổng toàn bảng. Dòng âm thêm điều kiện số tiền nhỏ hơn không và đếm. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L08")
    write_lab("FND", "L08", """# Lab FND L08 — Bảng và SQL đầu tiên

Viết `so_du.sql` (tệp SQL, chạy được bằng `sqlite3 :memory: < so_du.sql`; cần chương trình `sqlite3` đã cài ở bài đầu, kiểm bằng `sqlite3 --version`), gồm theo thứ tự:

1. `CREATE TABLE giao_dich` với ba cột `INTEGER`: `id` (khoá chính `PRIMARY KEY`), `tk`, `so_tien`.
2. `INSERT INTO giao_dich VALUES` tám hàng `(id, tk, so_tien)`: `(1,1,800000) (2,2,-120000) (3,3,450000) (4,1,300000) (5,2,500000) (6,3,-50000) (7,1,-100000) (8,2,70000)`.
3. Ba câu `SELECT`:
   - số dư từng tài khoản: `tk` và `SUM(so_tien)`, `GROUP BY tk`, `ORDER BY tk`;
   - `SELECT 'tong', SUM(so_tien) FROM giao_dich;`
   - `SELECT 'am', COUNT(*) FROM giao_dich WHERE so_tien < 0;`

Chấm: `bash labs/cham.sh FND L08 so_du.sql` (chạy tệp bằng `sqlite3`). Khác bài giảng: số liệu, số hàng.
""", "sql", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("bảng: cột có kiểu, hàng, khoá chính", "SELECT cột FROM bảng WHERE hàng ORDER BY", "GROUP BY + SUM, COUNT",
                 "UPDATE, DELETE luôn kèm WHERE", "NULL: dùng IS NULL", "giao dịch: BEGIN … COMMIT hoặc ROLLBACK"),
           """Tổng kết chuỗi logic. Bảng có cột có kiểu, hàng và khoá chính. Lệnh chọn gồm cột, bảng, điều kiện và sắp xếp. Nhóm theo cùng tổng hoặc đếm. Sửa và xoá luôn kèm mệnh đề điều kiện. Giá trị rỗng phải dùng cụm là giá trị rỗng.
           Và giao dịch bắt đầu, rồi chốt hoặc huỷ, để hai lệnh cùng có hiệu lực hoặc cùng không."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi sửa dữ liệu, hỏi “bao nhiêu hàng?” bằng một SELECT cùng WHERE; sau khi sửa, kiểm một <b>bất biến</b> (tổng tiền) bằng một câu lệnh thứ hai.</div>
<p>Bài sau: ghi lại lịch sử thay đổi của chính các tệp mã bằng quản lý phiên bản, để mọi thao tác đều quay lại được.</p>""",
           """Điều cần mang theo, trước khi sửa dữ liệu, hãy hỏi bao nhiêu hàng bằng một lệnh chọn cùng điều kiện. Sau khi sửa, kiểm một quy tắc bất biến, như tổng tiền, bằng một câu lệnh thứ hai.
           Bài sau, ta học quản lý phiên bản để ghi lại lịch sử thay đổi của các tệp mã.""", forward_ref=True),
    ])
    return lesson("L08", "bang_va_sql", "Bài 8 — Bảng và SQL đầu tiên bằng sqlite",
                  "curriculum/fnd.yaml L08; audit/fnd/verify_fnd.py L08 (chương trình dòng lệnh sqlite3 bản 3.46 chạy thật; NULL: cột so_du có một hàng NULL khi đếm IS NULL); SQLite docs: Datatypes In SQLite, NULL Handling in SQLite, Transaction (BEGIN/COMMIT/ROLLBACK), "
                  "The SQLite Query Optimizer Overview (chỉ mục, quét bảng); SQLite Database File Format (chỉ mục là cây B); CLI docs (.import: dòng đầu thành tên cột khi chưa có bảng); ISO/IEC 9075 (SQL); Codd 1970 (mô hình quan hệ); số bước tìm nhị phân là ⌈log2 n⌉, ước tính theo công thức",
                  ["Nêu bảng, hàng, cột, khoá chính và NULL là gì",
                   "Viết lệnh SELECT với WHERE, ORDER BY, GROUP BY để trả lời một câu hỏi về dữ liệu",
                   "Dùng UPDATE, DELETE đúng một hàng bằng WHERE và nêu hậu quả khi quên WHERE",
                   "Dùng giao dịch BEGIN, COMMIT, ROLLBACK để hai lệnh cùng có hiệu lực hoặc cùng không",
                   "Kiểm một kết quả nhóm bằng tổng toàn bảng",
                   "So sánh số hàng phải xem khi có và không có chỉ mục khi bảng nhân lên",
                   "Chỉ ra ba lỗi hay gặp: quên WHERE, so sánh bằng với NULL, chuyển tiền không giao dịch",
                   "Viết tệp SQL tạo bảng, chèn dữ liệu và in số dư theo tài khoản"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "sym"), (2, "formula"), (3, "example"), (4, "example"), (5, "check"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
