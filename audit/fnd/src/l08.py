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
    ], files=F)
    quymo = cmd("PhienQuyMo", [
        ("(echo id,v; seq 1 70000 | sed 's/.*/&,&/') > big.csv", ""), ("sqlite3 big.db '.import --csv big.csv g'", ""),
        ("sqlite3 big.db 'SELECT COUNT(*) FROM g;'", "70000"), ("sqlite3 big.db 'SELECT v FROM g WHERE id = 54321;'", "54321"),
    ])
    quiz = cmd("PhienQuiz", [
        ("DB=nh.db", ""), ("sqlite3 $DB < dung.sql", ""),
        ("sqlite3 $DB 'SELECT SUM(so_tien) FROM giao_dich WHERE tk = 2 AND so_tien > 0;'", "700000"),
        ("sqlite3 $DB 'SELECT tk, COUNT(*) AS n FROM giao_dich GROUP BY tk ORDER BY n DESC LIMIT 1;'", "1|3"),
    ], files=F)

    sc_hook = sc("hook", "hook", "Chuyển tiền cần hai lệnh ghi, và máy sập giữa chừng thì sao?", [
        st(term_block(gd, 2, 3, title="Chuyển 100 000 đồng: mới trừ ở An, chưa cộng ở Bình")
           + "<p>Tổng tiền của cả ngân hàng nhỏ này phải luôn là $2\\,000\\,000$. Ngay giữa hai lệnh, nó là $1\\,900\\,000$: <b>mất $100\\,000$ đồng</b>.</p>",
           """Chào bạn, chuyển tiền cần hai lệnh ghi, trừ ở tài khoản này và cộng ở tài khoản kia. Ở đây ta mới trừ một trăm nghìn ở tài khoản An, chưa cộng cho Bình, và tổng tiền cả ngân hàng nhỏ chỉ còn một triệu chín trăm nghìn, tức mất một trăm nghìn đồng.
           Nếu máy sập đúng lúc này mà không có cơ chế bảo vệ thì tiền mất thật. Hôm nay ta học bảng, câu lệnh hỏi bảng, và cơ chế bảo vệ đó."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li><b>Bảng</b> là gì: hàng, cột, khoá chính? Hỏi một bảng bằng <b>SELECT … WHERE … GROUP BY …</b> thế nào?</li>
<li>Sửa và xoá bằng <b>UPDATE, DELETE</b>: vì sao quên <b>WHERE</b> là tai nạn?</li>
<li><b>Giao dịch</b> (BEGIN … COMMIT/ROLLBACK) bảo vệ việc “hai lệnh hoặc không lệnh nào” ra sao?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Bảng là gì, gồm hàng, cột và khoá chính, và hỏi một bảng bằng ngôn ngữ SQL thế nào. Sửa và xoá ra sao, và vì sao quên mệnh đề điều kiện là tai nạn.
           Và giao dịch bảo vệ việc hai lệnh hoặc không lệnh nào ra sao."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp CSV, lọc, đếm, tổng", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① bảng bằng chữ", "tệp CSV: mỗi dòng một hàng, các cột cách nhau bằng dấu phẩy, dòng đầu là tên cột"],
                  ["② lọc", "<code>grep -v</code>, <code>cut</code>: giữ hàng hay cột cần dùng"],
                  ["③ nhóm và đếm", "<code>sort | uniq -c</code>: gom các dòng giống nhau và đếm"],
                  ["④ tổng không đổi", "tiền chuyển đi bằng tiền nhận về: kiểm bằng cách cộng toàn bộ"]]),
           """Ta ôn lại bốn điều. Bảng bằng chữ là tệp bảng, mỗi dòng một hàng, các cột cách nhau bằng dấu phẩy. Ta đã lọc hàng và cột bằng các lệnh lọc. Ta đã gom các dòng giống nhau rồi đếm.
           Và ta biết tiền chuyển đi bằng tiền nhận về, nên kiểm bằng cách cộng toàn bộ. Hôm nay chính cơ sở dữ liệu làm các việc đó giúp ta.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 1]),
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
                 [["<code>CREATE TABLE</code>", "tạo bảng", "khai tên bảng, tên và kiểu từng cột"],
                  ["<code>INSERT INTO … VALUES</code>", "chèn", "thêm hàng"],
                  ["<code>SELECT cột FROM bảng WHERE điều_kiện</code>", "chọn", "đọc các hàng thoả điều kiện"],
                  ["<code>ORDER BY</code> và <code>LIMIT</code>", "sắp xếp và giới hạn", "sắp theo cột (<code>DESC</code> giảm dần); lấy vài hàng đầu"],
                  ["<code>GROUP BY</code> + <code>SUM, COUNT</code>", "nhóm theo + hàm gộp", "gom hàng cùng giá trị cột nhóm; <code>SUM</code> tổng, <code>COUNT</code> đếm"],
                  ["<code>UPDATE … SET … WHERE</code> và <code>DELETE FROM … WHERE</code>", "sửa và xoá", "đổi hoặc bỏ <b>các hàng thoả WHERE</b>"]]),
           """Bảng thứ hai là các câu lệnh. Lệnh tạo bảng khai tên và kiểu từng cột. Lệnh chèn thêm hàng. Lệnh chọn đọc các hàng thoả điều kiện. Sắp xếp theo một cột, giảm dần nếu thêm một chữ, và giới hạn lấy vài hàng đầu.
           Nhóm theo cùng hàm gộp gom các hàng cùng giá trị rồi cộng hoặc đếm. Lệnh sửa và lệnh xoá tác động lên các hàng thoả mệnh đề điều kiện, và nếu không có mệnh đề đó thì tác động lên mọi hàng.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"], clear=True),
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
           Nhóm theo cột tài khoản gom các hàng cùng giá trị thành một nhóm. Ví dụ ba hàng của tài khoản một gom thành một nhóm, và hàm tổng cho hai trăm nghìn trừ năm mươi nghìn cộng một trăm năm mươi nghìn, bằng ba trăm nghìn."""),
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
           + term_block(nh, 0, 2, title="Nạp tệp vào cơ sở dữ liệu"),
           """Ta dựng dữ liệu trước. Tệp lệnh khai bảng tài khoản và chèn ba hàng, rồi lệnh đọc tệp đưa vào cơ sở dữ liệu, tạo ra tệp ngân hàng chấm d b. Lệnh này im lặng khi thành công, vì không có lỗi nào để báo."""),
        st(term_block(nh, 4, 5, title="Câu hỏi: tài khoản nào có số dư trên 400 000, sắp từ lớn xuống nhỏ?")
           + "<p><b>Bước 1.</b> Chọn <b>cột</b> cần xem: <code>SELECT ten, so_du</code>. <b>Bước 2.</b> Chỉ ra <b>bảng</b>: <code>FROM tai_khoan</code>. "
             "<b>Bước 3.</b> Lọc <b>hàng</b>: <code>WHERE so_du &gt; 400000</code>. <b>Bước 4.</b> Sắp xếp: <code>ORDER BY so_du DESC</code>.</p>",
           """Câu hỏi là tài khoản nào có số dư trên bốn trăm nghìn, sắp từ lớn xuống nhỏ. Bước một, chọn cột cần xem, là tên và số dư. Bước hai, chỉ ra bảng. Bước ba, lọc hàng, vì chỉ lấy số dư lớn hơn bốn trăm nghìn.
           Bước bốn, sắp xếp giảm dần theo số dư. Kết quả có hai hàng, Bình một triệu hai trăm nghìn và An năm trăm nghìn, còn Chi bị loại vì chỉ ba trăm nghìn."""),
        st(term_block(nh, 5, 7, title="Câu hỏi: số dư của từng tài khoản theo sổ giao dịch?")
           + "<p>Vì mỗi hàng giao dịch thuộc một <code>tk</code>, <b>nhóm</b> theo <code>tk</code> rồi <b>cộng</b> <code>so_tien</code>. Kiểm: $300\\,000 + 400\\,000 + 300\\,000 = \\hl{1\\,000\\,000}$ = tổng toàn bảng ✓</p>",
           """Câu hỏi thứ hai là số dư của từng tài khoản theo sổ giao dịch. Vì mỗi hàng giao dịch thuộc về một tài khoản, ta nhóm theo cột tài khoản rồi cộng số tiền. Làm thử, ba trăm nghìn cộng bốn trăm nghìn cộng ba trăm nghìn bằng một triệu, đúng bằng tổng toàn bảng, nên phép nhóm không bỏ sót hàng nào."""),
    ], checks=["200000 - 50000 + 150000 == 300000", "700000 - 300000 == 400000", "-100000 + 400000 == 300000",
               "300000 + 400000 + 300000 == 1000000", "sum([200000, -50000, 700000, -100000, -300000, 150000, 400000]) == 1000000"])
    sc_ex = sc("example", "example", "Ví dụ: sửa, xoá và giao dịch trên cùng cơ sở dữ liệu, năm phép làm", [
        st(term_block(nh, 2, 4, title="① Đọc cả bảng, rồi đọc kèm tên cột (-header)")
           + "<p>Ba hàng, ba cột. Cột <code>ma</code> là khoá chính nên không hàng nào trùng mã.</p>",
           """Phép làm thứ nhất, đọc cả bảng. Có ba hàng, ba cột. Cờ tiêu đề cho in thêm dòng tên cột, tiện cho người đọc. Cột mã là khoá chính nên không có hai hàng trùng mã."""),
        st(term_block(nh, 7, 9, title="② Sửa MỘT hàng bằng WHERE, rồi xoá MỘT giao dịch")
           + "<p><code>WHERE ma = 1</code> chỉ chạm hàng của An. Xoá <code>id = 2</code> làm số giao dịch từ $7$ xuống $6$.</p>",
           """Phép làm thứ hai, sửa và xoá đúng một hàng. Mệnh đề điều kiện mã bằng một chỉ chạm vào hàng của An, đổi tên thành An Lê. Xoá giao dịch số hai làm số giao dịch từ bảy xuống sáu."""),
        st(term_block(qwhere, 2, 3, title="③ Quên WHERE: sửa MỌI hàng (chạy trong giao dịch để huỷ được)")
           + "<p>Cả ba tài khoản về $0$; <code>ROLLBACK</code> huỷ, tổng trở lại $2\\,000\\,000$ ✓</p>",
           """Phép làm thứ ba, quên mệnh đề điều kiện. Lệnh sửa đưa số dư của cả ba tài khoản về không. Ta chạy trong một giao dịch nên lệnh huỷ đưa mọi thứ về như cũ, và tổng lại là hai triệu. Ngoài giao dịch thì không còn đường quay lại."""),
        st(term_block(gd, 2, 3, title="④ Giao dịch dở dang: mất tiền trong nháp, ROLLBACK trả lại"),
           """Phép làm thứ tư, giao dịch dở dang. Sau lệnh trừ, tổng tiền trong nháp là một triệu chín trăm nghìn, nhưng giao dịch chưa chốt. Lệnh huỷ đưa tổng trở lại hai triệu, như chưa có gì xảy ra."""),
        st(term_block(gd, 3, 5, title="⑤ Hai lệnh trong một giao dịch rồi COMMIT")
           + "<p>An $500\\,000 - 100\\,000 = \\hl{400\\,000}$; Bình $1\\,200\\,000 + 100\\,000 = \\hl{1\\,300\\,000}$; tổng vẫn $2\\,000\\,000$ ✓</p>",
           """Phép làm thứ năm, hai lệnh trong một giao dịch rồi chốt. An còn bốn trăm nghìn, Bình có một triệu ba trăm nghìn, Chi giữ nguyên, và tổng vẫn là hai triệu. Hai lệnh có hiệu lực cùng lúc, hoặc cả hai không có hiệu lực.""", clear=True),
    ], checks=["500000 - 100000 == 400000", "1200000 + 100000 == 1300000", "400000 + 1300000 + 300000 == 2000000", "7 - 1 == 6", "500000 + 1200000 + 300000 == 2000000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tổng hai cách và đếm hai cách", [
        st(term_block(nh, 5, 7, title="Cách 1: tổng theo nhóm") + "<p>Cộng ba nhóm: $300\\,000 + 400\\,000 + 300\\,000 = 1\\,000\\,000$.</p>"
           + "<p>Cách 2: một câu lệnh cộng cả bảng cho $1\\,000\\,000$ (đã in ở trên). Hai đường độc lập cùng ra một số ✓</p>",
           """Đường kiểm khác, tính tổng bằng hai cách. Cách một cộng ba nhóm, ra một triệu. Cách hai dùng một câu lệnh cộng cả bảng, cũng ra một triệu. Hai đường độc lập cùng ra một số, nên ta tin kết quả nhóm."""),
        st(term_block(nul, 3, 6, title="Kiểm NULL: so sánh bằng không bao giờ đúng với NULL")
           + "<p>$7 / 2 = 3$ (chia số nguyên), $7 / 2.0 = 3{,}5$: kiểu của số quyết định kết quả; tiền nên lưu <b>số nguyên theo đồng</b>.</p>",
           """Kiểm thêm giá trị rỗng. Dấu bằng với giá trị rỗng không bao giờ đúng, nên đếm ra không. Phải dùng cụm là giá trị rỗng, thì đếm ra một. Và bảy chia hai ra ba vì chia số nguyên, còn bảy chia hai chấm không ra ba rưỡi. Vì vậy tiền nên lưu bằng số nguyên theo đồng.""", clear=True),
    ], checks=["300000 + 400000 + 300000 == 1000000", "7 // 2 == 3", "7 / 2.0 == 3.5"])
    sc_scale = sc("scale", "example", "Khi bảng nhân lên: quét cả bảng hay tra theo chỉ mục", [
        st(term_block(quymo, 0, 4, title="Một bảng 70 000 hàng, tra một hàng theo id")
           + "<p>Lệnh tạo bảng 70 000 hàng từ tệp CSV rồi tra <code>id = 54321</code>. Không có chỉ mục thì cơ sở dữ liệu phải <b>xem lần lượt từng hàng</b>.</p>",
           """Ta nạp một tệp bảng bảy mươi nghìn hàng vào cơ sở dữ liệu rồi tra một hàng theo mã. Nếu bảng không có chỉ mục, tức một cái mục lục, thì cơ sở dữ liệu phải xem lần lượt từng hàng cho tới khi gặp hàng cần tìm."""),
        st(table(["số hàng", "không chỉ mục: xem tối đa", "có chỉ mục (tìm nhị phân): xem tối đa"],
                 [["×1: 7", "7 hàng", "3 bước"], ["×100: 700", "700 hàng", "10 bước"], ["×10 000: 70 000", "70 000 hàng", "17 bước"]])
           + "<div class='box key'><b>Đánh đổi:</b> chỉ mục làm <b>đọc nhanh</b> nhưng làm <b>ghi chậm hơn</b> và tốn thêm chỗ, vì mỗi lần ghi phải cập nhật cả mục lục. "
             "Khoá chính tự có chỉ mục. Số liệu là ước tính theo công thức (không đo thời gian).</div>",
           """Bảng này là số hàng phải xem trong trường hợp xấu nhất. Bảy hàng thì xem bảy hàng hoặc ba bước. Bảy trăm hàng, bảy trăm hàng hoặc mười bước. Bảy mươi nghìn hàng, bảy mươi nghìn hàng hoặc mười bảy bước. Chênh lệch tăng nhanh theo kích thước bảng.
           Chỉ mục làm đọc nhanh nhưng làm ghi chậm hơn và tốn thêm chỗ, vì mỗi lần ghi phải cập nhật cả mục lục. Khoá chính tự có chỉ mục. Các số này là ước tính theo công thức, không đo thời gian."""),
    ], checks=["10000 * 7 == 70000", "100 * 7 == 700", "__import__('math').ceil(__import__('math').log2(7)) == 3",
               "__import__('math').ceil(__import__('math').log2(700)) == 10", "__import__('math').ceil(__import__('math').log2(70000)) == 17"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên <code>WHERE</code> trong <code>UPDATE</code> hoặc <code>DELETE</code>: tác động lên <b>mọi</b> hàng.</div>'
           + term_block(qwhere, 2, 3) + "<p>Phép thử: viết <b>SELECT</b> với cùng <code>WHERE</code> trước để đếm số hàng; chạy trong giao dịch và xem kết quả rồi mới chốt.</p>",
           """Lỗi thứ nhất, của người mới, là quên mệnh đề điều kiện trong lệnh sửa hoặc lệnh xoá, nên tác động lên mọi hàng. Phép thử là viết lệnh chọn với cùng mệnh đề đó trước để đếm số hàng.
           Rồi chạy trong giao dịch, xem kết quả, và chỉ chốt khi đúng."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> So sánh với NULL bằng dấu <code>=</code>.</div>'
           + term_block(nul, 3, 5) + "<p>NULL nghĩa là “không biết”; “không biết = không biết” cũng không biết, nên cho kết quả <b>không đúng</b>. Dùng <code>IS NULL</code>. Hàm <code>SUM</code> bỏ qua NULL.</p>",
           """Lỗi thứ hai, cũng của người mới, là so sánh với giá trị rỗng bằng dấu bằng. Giá trị rỗng nghĩa là không biết, và không biết bằng không biết cũng là không biết, nên kết quả không đúng. Hãy dùng cụm là giá trị rỗng.
           Hàm cộng bỏ qua các giá trị rỗng, nên một cột có chỗ rỗng cho tổng thấp hơn bạn nghĩ."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Chuyển tiền bằng hai lệnh rời nhau, không giao dịch.</div>'
           + term_block(gd, 2, 3) + "<p>Giữa hai lệnh, lỗi mạng hay máy sập làm tiền biến mất. <b>Bất biến</b> “tổng không đổi” chỉ giữ được khi hai lệnh nằm <b>trong một giao dịch</b>.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là chuyển tiền bằng hai lệnh rời nhau, không có giao dịch. Giữa hai lệnh, lỗi mạng hay máy sập làm tiền biến mất, và tổng tiền sai mà không ai báo lỗi.
           Quy tắc tổng không đổi chỉ giữ được khi hai lệnh nằm trong một giao dịch. Người làm nghề luôn kiểm tổng sau mỗi thao tác chuyển tiền."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(file_block(cmd("Mau2", [("true", "")], files=F), "dung.sql", title="Dùng lại dữ liệu của bài (tệp dung.sql): bảng giao_dich", lines=(7, 10))
           + "<p><b>Đề.</b> (1) Viết SELECT cho <b>tổng tiền nạp</b> (số dương) của tài khoản $2$. (2) Viết SELECT cho tài khoản có <b>nhiều giao dịch nhất</b> kèm số giao dịch. "
             "(3) <b>Chọn</b>: chuyển $100\\,000$ từ An sang Bình bằng hai UPDATE: có cần giao dịch không, vì sao?</p>",
           """Bây giờ tới phần bạn tự làm, trên bảng giao dịch của bài. Câu một, viết lệnh chọn tổng tiền nạp, tức số dương, của tài khoản hai. Câu hai, viết lệnh chọn tài khoản có nhiều giao dịch nhất, kèm số giao dịch.
           Câu ba là một quyết định, chuyển một trăm nghìn từ An sang Bình bằng hai lệnh sửa thì có cần giao dịch không, và vì sao. Hãy dừng video và làm.""", pause=90),
        st(term_block(quiz, 2, 4, title="Máy chạy thật")
           + table(["câu", "câu lệnh", "kết quả và lý do"],
                   [["1", "<code>SELECT SUM(so_tien) FROM giao_dich WHERE tk = 2 AND so_tien &gt; 0;</code>", "$700\\,000$: chỉ giao dịch nạp của tk 2 (id 3); id 5 âm bị loại"],
                    ["2", "<code>SELECT tk, COUNT(*) AS n FROM giao_dich GROUP BY tk ORDER BY n DESC LIMIT 1;</code>", "<code>1|3</code>: tk 1 có $3$ giao dịch, nhiều nhất"]]),
           """Đáp án, máy chạy thật cho đúng hai kết quả. Câu một, chỉ giao dịch nạp của tài khoản hai là số ba, bảy trăm nghìn, còn giao dịch âm bị loại bởi điều kiện số dương. Câu hai, nhóm theo tài khoản, đếm, sắp giảm dần và lấy một hàng, ra tài khoản một có ba giao dịch."""),
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
Dòng âm: thêm <code>WHERE so_tien &lt; 0</code> và <code>COUNT(*)</code>. Chấm bằng máy: <code>sqlite3</code> chạy tệp, hoặc Python (<code>labs/sqlrun.py</code>). Lời giải ở <code>labs/FND/L08/loi_giai.sql</code>.</div>""",
        """Nếu kẹt, số dư từng tài khoản là lệnh chọn tài khoản và tổng, nhóm theo tài khoản, sắp theo tài khoản. Dòng tổng chọn một chữ cố định kèm tổng toàn bảng. Dòng âm thêm điều kiện số tiền nhỏ hơn không và đếm. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L08")
    write_lab("FND", "L08", """# Lab FND L08 — Bảng và SQL đầu tiên

Viết `so_du.sql` (tệp SQL, chạy được bằng `sqlite3 :memory: < so_du.sql` hoặc `python labs/sqlrun.py so_du.sql`), gồm theo thứ tự:

1. `CREATE TABLE giao_dich` với ba cột `INTEGER`: `id` (khoá chính `PRIMARY KEY`), `tk`, `so_tien`.
2. `INSERT INTO giao_dich VALUES` tám hàng `(id, tk, so_tien)`: `(1,1,800000) (2,2,-120000) (3,3,450000) (4,1,300000) (5,2,500000) (6,3,-50000) (7,1,-100000) (8,2,70000)`.
3. Ba câu `SELECT`:
   - số dư từng tài khoản: `tk` và `SUM(so_tien)`, `GROUP BY tk`, `ORDER BY tk`;
   - `SELECT 'tong', SUM(so_tien) FROM giao_dich;`
   - `SELECT 'am', COUNT(*) FROM giao_dich WHERE so_tien < 0;`

Chấm: `bash labs/cham.sh FND L08 so_du.sql` (dùng `sqlite3` nếu có, không thì `labs/sqlrun.py`). Khác bài giảng: số liệu, số hàng.
""", "sql", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("bảng: cột có kiểu, hàng, khoá chính", "SELECT cột FROM bảng WHERE hàng ORDER BY", "GROUP BY + SUM, COUNT",
                 "UPDATE, DELETE luôn kèm WHERE", "NULL: dùng IS NULL", "giao dịch: BEGIN … COMMIT hoặc ROLLBACK"),
           """Tổng kết chuỗi logic. Bảng có cột có kiểu, hàng và khoá chính. Lệnh chọn gồm cột, bảng, điều kiện và sắp xếp. Nhóm theo cùng tổng hoặc đếm. Sửa và xoá luôn kèm mệnh đề điều kiện. Giá trị rỗng phải dùng cụm là giá trị rỗng.
           Và giao dịch bắt đầu, rồi chốt hoặc huỷ, để hai lệnh cùng có hiệu lực hoặc cùng không."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi sửa dữ liệu, hỏi “bao nhiêu hàng?” bằng một SELECT cùng WHERE; sau khi sửa, kiểm một <b>bất biến</b> (tổng tiền) bằng một câu lệnh thứ hai.</div>
<p>Bài sau: ghi lại lịch sử thay đổi của chính các tệp mã bằng quản lý phiên bản, để mọi thao tác đều quay lại được.</p>""",
           """Điều cần mang theo, trước khi sửa dữ liệu, hãy hỏi bao nhiêu hàng bằng một lệnh chọn cùng điều kiện. Sau khi sửa, kiểm một quy tắc bất biến, như tổng tiền, bằng một câu lệnh thứ hai.
           Bài sau, ta học ghi lại lịch sử thay đổi của chính các tệp mã bằng quản lý phiên bản, để mọi thao tác đều quay lại được.""", forward_ref=True),
    ])
    return lesson("L08", "bang_va_sql", "Bài 8 — Bảng và SQL đầu tiên bằng sqlite",
                  "curriculum/fnd.yaml L08; audit/fnd/verify_fnd.py L08 (chương trình dòng lệnh sqlite3, thay bằng audit/fnd/shim/sqlite3 trên máy kiểm chưa cài sqlite3: mô-đun sqlite3 của Python, cùng định dạng mặc định, "
                  "cùng lõi SQLite); lab chạy qua labs/sqlrun.py; SQLite docs: Datatypes In SQLite, NULL Handling in SQLite, Transaction (BEGIN/COMMIT/ROLLBACK), "
                  "The SQLite Query Optimizer Overview (chỉ mục, quét bảng); ISO/IEC 9075 (SQL); Codd 1970 (mô hình quan hệ); số bước tìm nhị phân là ⌈log2 n⌉, ước tính theo công thức",
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
