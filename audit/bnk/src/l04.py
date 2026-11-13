from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    tao = prog("TaoBang", """
CREATE TABLE tx (id INTEGER PRIMARY KEY, tk INTEGER);
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5000)
INSERT INTO tx (tk) SELECT i % 500 FROM n;
SELECT COUNT(*) FROM tx;""", out="5000", lang="sqlite")
    ke_hoach = prog("KeHoach", """
CREATE TABLE tx (id INTEGER PRIMARY KEY, tk INTEGER);
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5000)
INSERT INTO tx (tk) SELECT i % 500 FROM n;
EXPLAIN QUERY PLAN SELECT * FROM tx WHERE tk = 7;
CREATE INDEX i_tk ON tx (tk);
EXPLAIN QUERY PLAN SELECT * FROM tx WHERE tk = 7;
EXPLAIN QUERY PLAN SELECT * FROM tx WHERE tk + 0 = 7;""", out="""2|0|216|SCAN tx
2|0|56|SEARCH tx USING COVERING INDEX i_tk (tk=?)
2|0|216|SCAN tx""", lang="sqlite")
    lab_sql = prog("SaoKe", """
CREATE TABLE gd (id INTEGER PRIMARY KEY, tk INTEGER, so_tien INTEGER);
INSERT INTO gd (tk, so_tien) VALUES (11, 900000), (12, -200000), (11, -150000), (13, 400000),
                                   (12, 600000), (11, 250000), (13, -100000);
CREATE INDEX i_gd_tk ON gd (tk);
SELECT id, so_tien FROM gd WHERE tk = 11 ORDER BY id;
SELECT COUNT(*) FROM gd WHERE so_tien < 0;
SELECT tk, SUM(so_tien) FROM gd GROUP BY tk ORDER BY tk;""", out="""1|900000
3|-150000
6|250000
3
11|1000000
12|400000
13|300000""", lang="sqlite")
    hook = sc("hook", "hook", "Vì sao tra cứu sao kê chậm khi bảng đã có hàng triệu dòng?", [
        st("""<p>Bảng giao dịch có $10\\,000\\,000$ dòng <i>(số minh hoạ)</i>. Tra các giao dịch của <b>một</b> tài khoản mà đọc cả mười triệu dòng thì quá lãng phí.</p>
<div class="box key">Có chỉ mục, máy chỉ đi qua khoảng <b>4 tầng</b> của một cây tìm kiếm rồi tới thẳng dòng cần
<i>(mô hình 100 lối rẽ mỗi nút; chỉ mục Oracle thật có hàng trăm lối rẽ nên thường còn ít tầng hơn)</i>.</div>""",
           """Chào bạn, bảng giao dịch có mười triệu dòng, đây là số minh hoạ. Tra các giao dịch của một tài khoản mà phải đọc cả mười triệu dòng thì quá lãng phí.
           Có chỉ mục, máy chỉ đi qua khoảng bốn tầng của một cây tìm kiếm rồi tới thẳng dòng cần. Bốn tầng là theo mô hình một trăm lối rẽ mỗi nút.
           Chỉ mục Oracle thật có hàng trăm lối rẽ, nên thường còn ít tầng hơn."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["chỉ mục là gì, vì sao nhanh", "một cây đã sắp thứ tự, tìm kiếm theo từng tầng"],
                  ["làm sao biết truy vấn có dùng chỉ mục", "đọc kế hoạch thực thi: SCAN hay SEARCH"],
                  ["vì sao có chỉ mục mà vẫn chậm", "viết điều kiện làm chỉ mục vô dụng"]]),
           """Hôm nay ta trả lời ba câu. Chỉ mục là gì và vì sao nhanh. Làm sao biết truy vấn có dùng chỉ mục, bằng cách đọc kế hoạch thực thi.
           Và vì sao có chỉ mục mà vẫn chậm, thường do ta viết điều kiện làm chỉ mục vô dụng."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Cơ sở dữ liệu và SQL", "cơ sở dữ liệu là phần mềm lưu bảng dữ liệu; SQL là ngôn ngữ để hỏi và sửa nó; Oracle là một hệ cơ sở dữ liệu nhiều ngân hàng dùng", "Oracle, sqlite"],
                  ["② Bảng, dòng, cột", "bảng gồm nhiều dòng, mỗi dòng có các cột", "dòng giao dịch có cột tài khoản, số tiền, ngày"],
                  ["③ Truy vấn có điều kiện", "SELECT lấy dòng thoả điều kiện WHERE", "WHERE account_id = 7"],
                  ["④ Tìm nhị phân", "trong danh sách đã sắp, mỗi bước so phần tử giữa rồi loại một nửa", "1024 phần tử: 10 lần chia đôi còn 1"]]),
           """Trước hết ta cần hiểu bốn điều. Cơ sở dữ liệu là phần mềm lưu các bảng dữ liệu, và SQL là ngôn ngữ để hỏi và sửa nó. Oracle là một hệ cơ sở dữ liệu mà nhiều ngân hàng dùng.
           Bảng gồm nhiều dòng, mỗi dòng có các cột. Truy vấn lấy các dòng thoả điều kiện đặt sau từ khoá where.
           Còn tìm nhị phân là trong một danh sách đã sắp thứ tự, mỗi bước so với phần tử ở giữa rồi loại bỏ một nửa. Một nghìn không trăm hai mươi bốn phần tử, sau mười lần chia đôi chỉ còn một."""),
        st("""$$2^{10} = 1024$$
<p>1024 → 512 → 256 → 128 → 64 → 32 → 16 → 8 → 4 → 2 → 1: mười lần chia đôi.</p>
<p class="small">So thêm phần tử cuối cùng đó nữa là xong: tối đa $10 + 1 = 11$ lần so.</p>""",
           """Vì sao mười lần? Vì hai mũ mười bằng một nghìn không trăm hai mươi bốn, nên mỗi lần chia đôi, sau mười lần chỉ còn một phần tử.
           So thêm phần tử cuối cùng đó nữa là xong, nên nhiều nhất là mười một lần so."""),
    ], checks=["2 ** 10 == 1024", "(lambda n: next(k for k in range(64) if 2 ** k >= n))(1024) == 10",
               "(lambda a, x: (lambda f: f(f, 0, len(a) - 1, 0))(lambda f, lo, hi, c: c if lo > hi else (c + 1 if a[(lo + hi) // 2] == x else (f(f, (lo + hi) // 2 + 1, hi, c + 1) if a[(lo + hi) // 2] < x else f(f, lo, (lo + hi) // 2 - 1, c + 1)))))(list(range(1024)), 1023) == 11"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["INDEX (chỉ mục)", "cấu trúc phụ giúp tìm dòng nhanh, như mục lục của sách"],
                  ["PRIMARY KEY", "khoá chính: cột định danh duy nhất mỗi dòng, thường đã có chỉ mục"],
                  ["EXPLAIN", "lệnh xem kế hoạch: máy sẽ tìm dòng bằng cách nào"],
                  ["SCAN (Oracle: TABLE ACCESS FULL)", "quét toàn bảng, đọc từng dòng"],
                  ["SEARCH ... USING INDEX (Oracle: INDEX RANGE SCAN)", "tìm qua chỉ mục, tới thẳng dòng cần"]]),
           """Bảng này giải mã năm từ. Chỉ mục là cấu trúc phụ giúp tìm dòng nhanh, như mục lục của cuốn sách. Khoá chính định danh duy nhất mỗi dòng.
           Lệnh explain cho xem kế hoạch, tức là máy sẽ tìm dòng bằng cách nào. Chữ scan nghĩa là quét toàn bảng. Còn search using index là tìm qua chỉ mục.
           Trong kế hoạch của Oracle, hai cách này mang tên khác, ghi trong ngoặc trên màn hình."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: cây tìm kiếm nhiều tầng", [
        st(svg(1500, 420,
               box(560, 30, 380, 80, "tầng 1 (nút gốc): 100 lối rẽ", C_BLUE),
               box(160, 160, 380, 80, "tầng 2: 100 lối rẽ", C_BLUE), box(960, 160, 380, 80, "tầng 2: 100 lối rẽ", C_BLUE),
               box(60, 290, 330, 80, "tầng 3 (lá)", C_GREEN), box(430, 290, 330, 80, "tầng 3 (lá)", C_GREEN),
               box(800, 290, 330, 80, "tầng 3 (lá)", C_GREEN), box(1170, 290, 280, 80, "tầng 3 (lá)", C_GREEN),
               arrow(700, 112, 350, 158, "#475569"), arrow(800, 112, 1150, 158, "#475569"),
               arrow(280, 242, 225, 288, "#475569"), arrow(420, 242, 595, 288, "#475569"),
               arrow(1060, 242, 965, 288, "#475569"), arrow(1240, 242, 1310, 288, "#475569")),
           """Hình cho thấy một cây tìm kiếm, mỗi ô trong cây gọi là một nút. Ở mỗi tầng có nhiều lối rẽ, đã sắp thứ tự, nên máy chọn đúng một lối rồi đi xuống tầng dưới.
           Đi hết các tầng là tới lá, nơi chỉ tới dòng cần tìm. Số tầng rất ít dù số dòng rất lớn."""),
        st(svg(1500, 380,
               panel(40, 30, 680, 320, "Không có chỉ mục: SCAN", C_RED),
               box(80, 110, 120, 60, "dòng", C_GRAY), box(220, 110, 120, 60, "dòng", C_GRAY), box(360, 110, 120, 60, "dòng", C_GRAY),
               box(500, 110, 120, 60, "dòng", C_GRAY),
               txt(380, 240, "đọc lần lượt cho tới hết", 26, "middle", "#dc2626", True),
               txt(380, 290, "10 000 000 dòng → 10 000 000 lần đọc", 24, "middle", "#1f2937"),
               panel(780, 30, 680, 320, "Có chỉ mục: SEARCH", C_GREEN),
               box(820, 110, 180, 60, "tầng 1", C_BLUE), box(1040, 110, 180, 60, "tầng 2", C_BLUE), box(1260, 110, 160, 60, "…", C_BLUE),
               arrow(1000, 140, 1038, 140), arrow(1220, 140, 1258, 140),
               txt(1120, 240, "đi qua từng tầng rồi tới dòng", 26, "middle", "#16a34a", True),
               txt(1120, 290, "khoảng 4 tầng cho 10 000 000 dòng", 24, "middle", "#1f2937")),
           """Hai cách tìm đặt cạnh nhau. Bên trái, không có chỉ mục, máy quét tuần tự, đọc từng dòng cho tới hết, tức mười triệu lần đọc.
           Bên phải, có chỉ mục, máy đi qua từng tầng rồi tới thẳng dòng, khoảng bốn tầng cho mười triệu dòng."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: bao nhiêu tầng?", [
        st("""<p><b>Bước 1.</b> Mỗi nút có $f$ lối rẽ. Cây $L$ tầng chứa được tối đa $f^L$ dòng.</p>
<span class='note'>Làm thử: $f = 100$, $L = 2$ thì $100^2 = 10\\,000$ dòng.</span>""",
           """Bước một, vì mỗi nút có f lối rẽ, nên cây L tầng chứa được tối đa f mũ L dòng. Làm thử, f bằng một trăm, L bằng hai, thì một trăm mũ hai là mười nghìn dòng."""),
        st("""<p><b>Bước 2.</b> Muốn chứa $n$ dòng, cần $L$ nhỏ nhất sao cho $f^L \\ge n$. Thử tăng $L$ dần.</p>
<span class='note'>Làm thử: $n = 10\\,000\\,000$: $100^3 = 1\\,000\\,000$ chưa đủ, $100^4 = 100\\,000\\,000$ đủ.</span>""",
           """Bước hai, vì cần chứa n dòng, nên ta tìm L nhỏ nhất sao cho f mũ L không nhỏ hơn n. Làm thử với mười triệu dòng, một trăm mũ ba là một triệu chưa đủ, một trăm mũ bốn là một trăm triệu thì đủ."""),
        st("""<p><b>Bước 3.</b> Một lần tra qua chỉ mục đọc khoảng $L$ nút rồi $1$ dòng, nên tổng khoảng $L + 1$ lần đọc.</p>
<span class='note'>Làm thử: $4 + 1 = 5$ lần đọc thay vì $10\\,000\\,000$. Tài khoản có $k$ giao dịch thì đọc thêm khoảng $k$ dòng.</span>""",
           """Bước ba, vì tra qua chỉ mục đi qua L nút rồi đọc một dòng, nên tổng khoảng L cộng một lần đọc. Làm thử, bốn cộng một bằng năm lần đọc, thay vì mười triệu lần.
           Nếu tài khoản có k giao dịch, máy đọc thêm khoảng k dòng nữa."""),
    ], checks=["100 ** 2 == 10000", "alg.bnk_btree_levels(10 ** 7, 100) == 4", "100 ** 3 < 10 ** 7 <= 100 ** 4", "4 + 1 == 5"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Mô hình đơn giản: mỗi nút $100$ lối rẽ, bảng $10\\,000\\,000$ dòng.</p>
$$① \\; 100^1 = 100 < 10\\,000\\,000$$""",
           """Ta thử tăng dần số tầng. Phép tính thứ nhất, một tầng chứa tối đa một trăm dòng, chưa đủ cho mười triệu dòng."""),
        st("""$$② \\; 100^2 = 10\\,000 < 10\\,000\\,000$$""",
           """Phép tính thứ hai, hai tầng chứa tối đa mười nghìn dòng, vẫn chưa đủ."""),
        st("""$$③ \\; 100^3 = 1\\,000\\,000 < 10\\,000\\,000$$""",
           """Phép tính thứ ba, ba tầng chứa tối đa một triệu dòng, vẫn chưa đủ."""),
        st("""$$④ \\; 100^4 = 100\\,000\\,000 \\ge 10\\,000\\,000 \\Rightarrow L = \\hlg{4}$$""",
           """Phép tính thứ tư, bốn tầng chứa tối đa một trăm triệu dòng, đủ cho mười triệu dòng. Vậy cần bốn tầng.""",
           introduces=["implies"]),
        st("""$$⑤ \\; 4 + 1 = \\hlg{5}\\ \\text{lần đọc, so với}\\ \\hl{10\\,000\\,000}\\ \\text{khi quét}$$""",
           """Phép tính thứ năm, một lần tra qua chỉ mục tốn bốn cộng một bằng năm lần đọc, so với mười triệu lần khi quét toàn bảng."""),
    ], checks=["100 ** 1 < 10 ** 7", "100 ** 2 < 10 ** 7", "100 ** 3 < 10 ** 7", "100 ** 4 >= 10 ** 7 and alg.bnk_btree_levels(10 ** 7, 100) == 4",
               "alg.bnk_btree_levels(10 ** 7, 100) + 1 == 5"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: hỏi chính cơ sở dữ liệu", [
        st("""<p>Đường khác: hỏi kế hoạch thực thi thật (sqlite, 5000 dòng). Chưa có chỉ mục thì <b>SCAN</b>; có chỉ mục trên tài khoản thì <b>SEARCH</b>.</p>""",
           """Kiểm bằng đường khác, ta hỏi kế hoạch thực thi thật trên một cơ sở dữ liệu nhỏ, năm nghìn dòng. Chưa có chỉ mục thì kế hoạch là quét toàn bảng.
           Có chỉ mục trên cột tài khoản thì kế hoạch là tìm qua chỉ mục. Máy này không có Oracle, nên ta dùng sqlite để minh hoạ cùng ý tưởng."""),
        st(table(["điều kiện WHERE", "không chỉ mục", "chỉ mục (account_id, created)"],
                 [["account_id = 7", "SCAN", "SEARCH"],
                  ["account_id = 7 AND created = '2026-01-05'", "SCAN", "SEARCH"],
                  ["created = '2026-01-05' (bỏ cột đầu)", "SCAN", "SCAN"],
                  ["account_id + 0 = 7 (bọc phép tính)", "SCAN", "SCAN"],
                  ["abs(account_id) = 7 (bọc hàm)", "SCAN", "SCAN"]]),
           """Bảng này là kết quả hỏi thật. Hai điều kiện đầu dùng được chỉ mục. Điều kiện thứ ba bỏ cột đầu của chỉ mục nên ở đây vẫn phải quét.
           Hai điều kiện cuối bọc cột trong một phép tính hoặc hàm, nên chỉ mục cũng vô dụng."""),
    ], checks=["alg.bnk_sql_plan(False, 'account_id=7').startswith('SCAN')", "alg.bnk_sql_plan(True, 'account_id=7').startswith('SEARCH')",
               "alg.bnk_sql_plan(False, \"account_id=7 AND created='2026-01-05'\").startswith('SCAN')",
               "alg.bnk_sql_plan(True, \"account_id=7 AND created='2026-01-05'\").startswith('SEARCH')",
               "alg.bnk_sql_plan(True, \"created='2026-01-05'\").startswith('SCAN')", "alg.bnk_sql_plan(True, 'account_id+0=7').startswith('SCAN')",
               "alg.bnk_sql_plan(False, 'abs(account_id)=7').startswith('SCAN')",
               "alg.bnk_sql_plan(True, 'abs(account_id)=7').startswith('SCAN')"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ “thêm chỉ mục càng nhiều càng tốt”. Mỗi chỉ mục làm <b class="red">chậm việc ghi</b>, vì mỗi lần thêm dòng phải cập nhật thêm một mục trong mỗi cây chỉ mục; sửa dòng thì chỉ khi cột thuộc chỉ mục thay đổi.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ thêm chỉ mục càng nhiều càng tốt. Mỗi chỉ mục làm chậm việc ghi, vì mỗi lần thêm dòng phải cập nhật thêm một mục trong mỗi cây chỉ mục.
           Còn sửa dòng thì chỉ tốn thêm khi cột thuộc chỉ mục thay đổi."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Bọc cột trong hàm</b> trong điều kiện, ví dụ lấy tháng của ngày. Chỉ mục trên cột bị bỏ qua.
<br><span class="note">Cách chữa: viết khoảng ngày thay vì hàm, hoặc tạo chỉ mục theo đúng biểu thức.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là bọc cột trong một hàm ngay trong điều kiện, ví dụ lấy tháng của ngày. Chỉ mục trên cột bị bỏ qua.
           Cách chữa là viết khoảng ngày thay vì dùng hàm, hoặc tạo chỉ mục theo đúng biểu thức đó."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đặt chỉ mục nhiều cột sai thứ tự. Chỉ mục <code>(account_id, created)</code> dùng được cho điều kiện bắt đầu từ <code>account_id</code>,
thường không dùng tốt cho điều kiện chỉ có <code>created</code>. Oracle có thể dùng INDEX SKIP SCAN khi cột đầu ít giá trị khác nhau, nhưng thường kém hơn chỉ mục đúng thứ tự.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là đặt chỉ mục nhiều cột sai thứ tự. Chỉ mục tài khoản rồi ngày dùng được cho điều kiện bắt đầu từ tài khoản, nhưng thường không dùng tốt cho điều kiện chỉ có ngày.
           Oracle có cách quét nhảy qua cột đầu khi cột đầu ít giá trị khác nhau, nhưng thường kém hơn chỉ mục đúng thứ tự."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bảng 1 000 000 dòng, mỗi nút 100 lối rẽ. Cần mấy tầng?"],
                  ["2", "Tra qua chỉ mục tốn bao nhiêu lần đọc (tầng + 1 dòng)?"],
                  ["3", "Quyết định: bảng ghi liên tục 20 000 giao dịch mỗi giây, có nên thêm 8 chỉ mục?"]]),
           """Đến lượt bạn. Câu một, bảng một triệu dòng, mỗi nút một trăm lối rẽ, cần mấy tầng? Câu hai, tra qua chỉ mục tốn bao nhiêu lần đọc?
           Câu ba, bảng ghi liên tục hai chục nghìn giao dịch mỗi giây, có nên thêm tám chỉ mục không? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $100^3 = 1\\,000\\,000 \\ge 1\\,000\\,000$ và $100^2 = 10\\,000$ chưa đủ.</p>
$$L = \\hl{3}$$""",
           """Đáp án câu một. Một trăm mũ hai chỉ mười nghìn, chưa đủ. Một trăm mũ ba bằng đúng một triệu, đủ. Vậy cần ba tầng."""),
        st("""$$3 + 1 = \\hlg{4}\\ \\text{lần đọc}$$""",
           """Đáp án câu hai. Ba tầng cộng một dòng, bằng bốn lần đọc."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["thêm cả 8 chỉ mục", "mọi truy vấn tra cứu nhanh", "mỗi giao dịch ghi phải cập nhật 8 cây, ghi chậm"],
                  ["chỉ mục cho truy vấn thật sự hay chạy", "cân bằng đọc và ghi", "truy vấn hiếm gặp có thể chậm"]]),
           """Đáp án câu ba là đánh đổi. Thêm cả tám chỉ mục thì tra cứu nhanh nhưng mỗi lần ghi phải cập nhật tám cây, nên ghi chậm. Chỉ nên tạo chỉ mục cho những truy vấn thật sự hay chạy, và đo trước khi thêm."""),
    ], checks=["alg.bnk_btree_levels(10 ** 6, 100) == 3", "alg.bnk_btree_levels(10 ** 6, 100) + 1 == 4"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("bảng lớn", "chỉ mục = cây nhiều tầng", "ít tầng → ít lần đọc", "điều kiện phải khớp chỉ mục"),
           """Tổng kết chuỗi logic. Bảng lớn thì dùng chỉ mục, là cây nhiều tầng. Ít tầng nên ít lần đọc. Nhưng điều kiện phải khớp chỉ mục thì nó mới được dùng."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng đoán, hãy <b>đọc kế hoạch thực thi</b>. Thấy SCAN trên bảng lớn là dấu hiệu cần xem lại điều kiện và chỉ mục.</div>""",
           """Điều cần mang theo. Đừng đoán, hãy đọc kế hoạch thực thi. Thấy quét toàn bảng trên bảng lớn là dấu hiệu cần xem lại điều kiện và chỉ mục."""),
    ])
    # ── AF2: P1 câu lệnh SQL, mã chạy thật (sqlite), quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm ba điều", "nghĩa", "ví dụ"],
                 [["⑤ Câu lệnh SQL", "<code>CREATE TABLE</code> tạo bảng; <code>INSERT INTO … VALUES</code> thêm dòng; <code>SELECT … FROM … WHERE</code> lấy dòng thoả điều kiện; <code>COUNT(*)</code> đếm dòng, <code>SUM(cột)</code> cộng; <code>GROUP BY</code> gom nhóm; <code>ORDER BY</code> sắp xếp", "<code>SELECT COUNT(*) FROM tx;</code>"],
                  ["⑥ Khoá chính", "cột định danh duy nhất mỗi dòng; <code>INTEGER PRIMARY KEY</code> tự đánh số", "cột <code>id</code>"],
                  ["⑦ sqlite", "cơ sở dữ liệu nhỏ chạy ngay trong chương trình, dùng để thực hành; chạy tệp SQL bằng <code>python labs/sqlrun.py tệp.sql</code> hoặc <code>sqlite3</code>", "bảng <code>tx</code> trong bộ nhớ"]]),
           """Thêm ba điều nữa. Các câu lệnh SQL cơ bản: tạo bảng, thêm dòng, lấy dòng thoả điều kiện, đếm dòng, cộng một cột, gom nhóm và sắp xếp. Khoá chính là cột định danh duy nhất mỗi dòng, và cột kiểu số nguyên khoá chính tự đánh số.
           Cuối cùng, ta dùng một cơ sở dữ liệu nhỏ chạy ngay trong chương trình để thực hành, và chạy tệp SQL bằng lệnh có sẵn trong thư mục thực hành.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: bảy điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: đọc kế hoạch quét và tìm qua chỉ mục", [
        st(code_block(tao, title="Dựng bảng tx 5000 dòng (sqlite)"),
           """Ta dựng một bảng thật. Dòng thứ hai là cách sinh năm nghìn số liên tiếp: số sau bằng số trước cộng một, cho tới năm nghìn. Dòng thứ ba chèn năm nghìn dòng,
           cột tài khoản là phần dư của số đó khi chia cho năm trăm, tức là có năm trăm tài khoản, mỗi tài khoản mười dòng. Lệnh cuối đếm số dòng."""),
        st(out_block(tao),
           """Khi chạy thật, lệnh đếm cho ra năm nghìn dòng, đúng như đã chèn.""", clear=True),
        st(code_block(ke_hoach, lines=(4, 7), title="Hỏi kế hoạch: trước chỉ mục, sau chỉ mục, và khi bọc cột vào phép tính"),
           """Bây giờ ta hỏi kế hoạch bằng lệnh xem kế hoạch truy vấn. Lần thứ nhất, chưa có chỉ mục, ta tìm tài khoản số bảy. Rồi ta tạo chỉ mục trên cột tài khoản và hỏi lại.
           Lần cuối, ta viết điều kiện tương đương, là tài khoản cộng không bằng bảy, và hỏi một lần nữa.""", clear=True),
        st(code_block(ke_hoach, lines=(4, 7), title="Hỏi kế hoạch (như trên)") + out_block(ke_hoach, "Kế hoạch máy in ra (cột mô tả)")
           + "<p class=\"note\">Bản sqlite cũ hơn 3.36 ghi <code>SCAN TABLE tx</code>. Máy in thêm ba cột số đứng trước, ta chỉ đọc cột cuối. Chữ <code>COVERING</code>: chỉ mục đã chứa đủ cột cần lấy.</p>",
           """Khi chạy thật, lần đầu máy quét cả bảng. Sau khi có chỉ mục, máy tìm qua chỉ mục theo cột tài khoản, tới thẳng các dòng cần.
           Còn khi cột bị bọc trong phép cộng không, máy quay lại quét cả bảng, vì chỉ mục theo cột tài khoản không dùng được khi ta đổi chính cột đó. Hai điều kiện cùng nghĩa, nhưng chi phí rất khác.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: số dòng tăng ×100 và ×10 000, quét gãy từ đâu?", [
        st("""<p>Giả sử máy quét được $10^6$ dòng mỗi giây, mỗi lối rẽ của cây chỉ mục là $100$, mỗi dòng chỉ mục chiếm $16$ byte <i>(số minh hoạ)</i>.</p>"""
           + table(["tải", "số dòng", "quét toàn bảng", "tầng chỉ mục", "dung lượng chỉ mục"],
                   [["×1", "100 000", "0,1 giây", "3", "1,6 MB"],
                    ["×100", "10 000 000", "<b>10 giây</b>", "4", "160 MB"],
                    ["×10 000", "1 000 000 000", "<b>1000 giây ≈ 16,7 phút</b>", "5", "<b>16 GB</b>"]]),
           """Giả sử máy quét được một triệu dòng mỗi giây, mỗi lối rẽ của cây chỉ mục là một trăm, mỗi dòng chỉ mục chiếm mười sáu byte. Đây là số minh hoạ.
           Với một trăm nghìn dòng, quét toàn bảng mất một phần mười giây, và chỉ mục có ba tầng. Tải tăng một trăm lần, quét mất mười giây, trong khi chỉ mục chỉ thêm một tầng.
           Tải tăng mười nghìn lần, quét mất hơn mười sáu phút, còn chỉ mục mới năm tầng.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Quét toàn bảng tăng <b>tỉ lệ thuận</b> với số dòng (×10 000 dòng thì ×10 000 thời gian); chỉ mục tăng theo <b>số tầng</b>, chỉ 3 → 5.
Nhưng chỉ mục cũng gãy: ở ×10 000 nó nặng cỡ 16 GB, có thể không còn nằm vừa bộ nhớ của máy, nên mỗi tầng thành một lần đọc đĩa.</div>
<div class="box key"><b>Đánh đổi:</b> mỗi chỉ mục làm mỗi lần <b>ghi</b> chậm hơn (phải cập nhật cả cây) và tốn chỗ. Chỉ lập chỉ mục cho cột hay lọc; ở quy mô cực lớn thì chia bảng thành nhiều phần hoặc nhiều máy.</div>""",
           """Câu hỏi là giải pháp cũ sẽ gãy ở chỗ nào khi tải tăng lên. Quét toàn bảng tăng tỉ lệ thuận với số dòng, còn chỉ mục chỉ tăng theo số tầng, từ ba lên năm. Nhưng chỉ mục cũng gãy. Ở tải gấp mười nghìn lần nó nặng cỡ mười sáu nghìn mê ga byte, có thể không vừa bộ nhớ của máy.
           Khi đó mỗi tầng thành một lần đọc đĩa. Đánh đổi là mỗi chỉ mục làm mỗi lần ghi chậm hơn, vì phải cập nhật cả cây, và tốn chỗ. Hãy chỉ lập chỉ mục cho cột hay dùng để lọc.
           Ở quy mô cực lớn thì phải chia bảng thành nhiều phần hoặc nhiều máy.""", clear=True),
    ], checks=["10**5 / 10**6 == 0.1", "10**7 / 10**6 == 10.0", "10**9 / 10**6 == 1000.0", "round(1000 / 60, 1) == 16.7",
               "alg.bnk_btree_levels(10**5, 100) == 3", "alg.bnk_btree_levels(10**7, 100) == 4", "alg.bnk_btree_levels(10**9, 100) == 5",
               "10**5 * 16 == 1_600_000", "10**7 * 16 == 160_000_000", "10**9 * 16 == 16_000_000_000"])
    write_lab("BNK", "L04", """# Lab BNK L04 — Sao kê ba tài khoản

Viết tệp `sao_ke.sql` (chạy bằng `python labs/sqlrun.py sao_ke.sql`, hoặc `sqlite3 :memory: < sao_ke.sql` nếu máy có `sqlite3`), gồm theo thứ tự:

1. `CREATE TABLE gd` với ba cột: `id INTEGER PRIMARY KEY`, `tk INTEGER`, `so_tien INTEGER`.
2. `INSERT INTO gd (tk, so_tien) VALUES` bảy dòng `(tk, so_tien)`: `(11, 900000) (12, -200000) (11, -150000) (13, 400000) (12, 600000) (11, 250000) (13, -100000)`.
3. `CREATE INDEX i_gd_tk ON gd (tk);`
4. Ba câu `SELECT`:
   - `id` và `so_tien` của tài khoản 11, `ORDER BY id`;
   - đếm số dòng có `so_tien < 0`;
   - `tk` và `SUM(so_tien)` theo từng tài khoản, `GROUP BY tk`, `ORDER BY tk`.

Chấm: `bash labs/cham.sh BNK L04 sao_ke.sql`.
""", "sql", lab_sql["code"], lab_sql["out"])
    lab = practice_scene(sc, "Tự làm: sao kê ba tài khoản", practice_steps(
        st, "BNK", "L04",
        """<p><b>Đề</b>: viết <code>sao_ke.sql</code> (đề đầy đủ ở <code>labs/BNK/L04/de.md</code>):</p>
<ol><li>bảng <code>gd(id, tk, so_tien)</code>, 7 dòng <code>(tk, so_tien)</code>: <code>(11,900000) (12,-200000) (11,-150000) (13,400000) (12,600000) (11,250000) (13,-100000)</code></li>
<li>chỉ mục trên <code>tk</code></li>
<li>ba <code>SELECT</code>: dòng của tk 11; số dòng âm; tổng theo tk</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Hãy viết một tệp SQL: tạo bảng giao dịch với ba cột, thêm bảy dòng như trên màn hình, và tạo chỉ mục trên cột tài khoản.
        Rồi viết ba câu lấy dữ liệu: các dòng của tài khoản mười một theo thứ tự mã, số dòng có số tiền âm, và tổng tiền theo từng tài khoản. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_sql["out"], "sao_ke.sql",
        """<div class="box key"><b>Nếu kẹt:</b> câu thứ nhất <code>SELECT id, so_tien FROM gd WHERE tk = 11 ORDER BY id;</code>; câu thứ hai <code>SELECT COUNT(*) FROM gd WHERE so_tien &lt; 0;</code>;
câu thứ ba <code>SELECT tk, SUM(so_tien) FROM gd GROUP BY tk ORDER BY tk;</code>. Lời giải ở <code>labs/BNK/L04/loi_giai.sql</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, câu thứ nhất lọc theo tài khoản mười một rồi sắp theo mã. Câu thứ hai đếm các dòng có số tiền nhỏ hơn không. Câu thứ ba cộng số tiền, gom theo tài khoản và sắp theo tài khoản.
        Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "BNK", "L04")
    return lesson("L04", "sql_chi_muc_ke_hoach", "Bài 4 — SQL, chỉ mục và kế hoạch thực thi",
                  "curriculum/bnk.yaml L04; audit/bnk/verify_bnk.py L04; audit/review/screen_code/BNK.yaml (SQL chạy thật bằng sqlite 3.49); SQLite EXPLAIN QUERY PLAN documentation (SCAN / SEARCH … USING INDEX; bản trước 3.36 ghi SCAN TABLE); SQLite WITH RECURSIVE; Oracle EXPLAIN PLAN (khái niệm tương đương, không chạy trên máy này)",
                  ["Tính số tầng của cây chỉ mục theo số dòng và số lối rẽ", "Đọc kế hoạch thực thi để biết truy vấn quét hay tìm qua chỉ mục",
                   "Nhận ra điều kiện làm chỉ mục vô dụng", "Cân nhắc lợi hại khi thêm chỉ mục",
                   "Tính thời gian quét, số tầng và dung lượng chỉ mục khi số dòng tăng ×100 và ×10 000",
                   "Viết câu SQL tạo bảng, thêm dòng, lọc, đếm, gom nhóm và tạo chỉ mục"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "formula"), (2, "chay_that"), (3, "pitfalls"), (4, "quy_mo"), (5, "quy_mo"), (6, "practice")])
