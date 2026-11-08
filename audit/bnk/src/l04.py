from lib import *


def build():
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
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Bảng, dòng, cột", "bảng gồm nhiều dòng, mỗi dòng có các cột", "dòng giao dịch có cột tài khoản, số tiền, ngày"],
                  ["② Truy vấn có điều kiện", "SELECT lấy dòng thoả điều kiện WHERE", "WHERE account_id = 7"],
                  ["③ Tìm nhị phân", "trong danh sách đã sắp, mỗi bước loại một nửa", "1024 phần tử cần tối đa 10 bước"]]),
           """Ôn ba điều. Bảng gồm nhiều dòng, mỗi dòng có các cột. Truy vấn lấy các dòng thoả điều kiện đặt sau từ khoá where.
           Còn tìm nhị phân là trong một danh sách đã sắp thứ tự, mỗi bước loại bỏ một nửa, nên một nghìn không trăm hai mươi bốn phần tử cần tối đa mười bước."""),
        st("""$$2^{10} = 1024$$""",
           """Vì sao mười bước? Vì hai mũ mười bằng một nghìn không trăm hai mươi bốn. Mỗi bước chia đôi, nên sau mười bước chỉ còn một phần tử."""),
    ], checks=["2 ** 10 == 1024", "(lambda n: next(k for k in range(64) if 2 ** k >= n))(1024) == 10"])
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
               box(560, 30, 380, 80, "tầng 1 (gốc): 100 lối rẽ", C_BLUE),
               box(160, 160, 380, 80, "tầng 2: 100 lối rẽ", C_BLUE), box(960, 160, 380, 80, "tầng 2: 100 lối rẽ", C_BLUE),
               box(60, 290, 330, 80, "tầng 3 (lá)", C_GREEN), box(430, 290, 330, 80, "tầng 3 (lá)", C_GREEN),
               box(800, 290, 330, 80, "tầng 3 (lá)", C_GREEN), box(1170, 290, 280, 80, "tầng 3 (lá)", C_GREEN),
               arrow(700, 112, 350, 158, "#475569"), arrow(800, 112, 1150, 158, "#475569"),
               arrow(280, 242, 225, 288, "#475569"), arrow(420, 242, 595, 288, "#475569"),
               arrow(1060, 242, 965, 288, "#475569"), arrow(1240, 242, 1310, 288, "#475569")),
           """Hình cho thấy một cây tìm kiếm. Ở mỗi tầng có nhiều lối rẽ, đã sắp thứ tự, nên máy chọn đúng một lối rồi đi xuống tầng dưới.
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
                  ["substr(created, 1, 7) = '2026-01' (bọc hàm)", "SCAN", "SCAN"]]),
           """Bảng này là kết quả hỏi thật. Hai điều kiện đầu dùng được chỉ mục. Điều kiện thứ ba bỏ cột đầu của chỉ mục nên ở đây vẫn phải quét.
           Hai điều kiện cuối bọc cột trong một phép tính hoặc hàm, nên chỉ mục cũng vô dụng."""),
    ], checks=["alg.bnk_sql_plan(False, 'account_id=7').startswith('SCAN')", "alg.bnk_sql_plan(True, 'account_id=7').startswith('SEARCH')",
               "alg.bnk_sql_plan(True, \"created='2026-01-05'\").startswith('SCAN')", "alg.bnk_sql_plan(True, 'account_id+0=7').startswith('SCAN')",
               "alg.bnk_sql_plan(True, \"substr(created,1,7)='2026-01'\").startswith('SCAN')"])
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
    return lesson("L04", "sql_chi_muc_ke_hoach", "Bài 4 — SQL, chỉ mục và kế hoạch thực thi",
                  "curriculum/bnk.yaml L04; audit/bnk/verify_bnk.py L04; SQLite EXPLAIN QUERY PLAN documentation; Oracle EXPLAIN PLAN (khái niệm tương đương, không chạy trên máy này)",
                  ["Tính số tầng của cây chỉ mục theo số dòng và số lối rẽ", "Đọc kế hoạch thực thi để biết truy vấn quét hay tìm qua chỉ mục",
                   "Nhận ra điều kiện làm chỉ mục vô dụng", "Cân nhắc lợi hại khi thêm chỉ mục"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
