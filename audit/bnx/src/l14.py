from lib import *

# Mã trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l14.yaml, audit/bnx/ver/l14.py)
BUCKET_PY = """from fractions import Fraction as F
def cong(rate, cap, times):          # cổng: tốc độ, sức chứa
    tok, last, ok = F(cap), F(0), 0  # thùng đầy lúc đầu
    for t in times:
        tok = min(F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:                 # còn ít nhất 1 thẻ
            tok, ok = tok - 1, ok + 1
    return ok
print(cong(5, 10, [F(0)] * 30))                    # cùng lúc
print(cong(5, 10, [F(i, 30) for i in range(30)]))  # rải đều"""
BUCKET_OUT = """10
14"""

SPREAD = "alg.bnx_l14_spread(30)"


def build():
    hook = sc("hook", "hook", "Cửa vào của ngân hàng: 30 yêu cầu cùng một lúc", [
        st("""<p>Từ $01/3/2025$, ngân hàng mở API cho <b>bên thứ ba</b> theo Thông tư 64/2024/TT-NHNN. Một ứng dụng bên thứ ba gửi $30$ yêu cầu <b>cùng một lúc</b>.</p>
<div class="box key">Cổng API cho mỗi bên $5$ yêu cầu/giây, sức chứa $10$ <i>(số minh hoạ)</i>: nhận $10$, từ chối $20$. Nếu $30$ yêu cầu <b>rải đều trong 1 giây</b> thì nhận $14$.</div>""",
           """Chào bạn, từ ngày một tháng ba năm hai nghìn không trăm hai mươi lăm, ngân hàng mở API cho bên thứ ba theo Thông tư sáu mươi tư của Ngân hàng Nhà nước.
           Một ứng dụng bên thứ ba gửi ba mươi yêu cầu cùng một lúc. Giả sử cổng API cho mỗi bên năm yêu cầu mỗi giây, sức chứa mười, là số minh hoạ. Khi đó cổng nhận mười và từ chối hai mươi.
           Nếu ba mươi yêu cầu đó rải đều trong một giây thì cổng nhận mười bốn. Cuối bài, bạn sẽ tự tính ra hai con số này.""", focus=[1, 1, 2, 2, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời bằng"],
                 [["chia hệ thống ngân hàng ở đâu", "ngữ cảnh giới hạn: mỗi nghĩa của một chữ có chỗ riêng"],
                  ["ai đứng ở cửa vào", "cổng API: xác thực, giới hạn tốc độ, định tuyến, nhật ký"],
                  ["bên thứ ba được lấy dữ liệu gì", "Open API theo Thông tư 64: hợp đồng và sự đồng ý của khách"]]),
           """Hôm nay ta trả lời ba câu. Hệ thống ngân hàng nên chia ở đâu, thì dùng ngữ cảnh giới hạn, mỗi nghĩa của một chữ có chỗ riêng.
           Ai đứng ở cửa vào, thì là cổng API, lo xác thực, giới hạn tốc độ, định tuyến và nhật ký.
           Bên thứ ba được lấy dữ liệu gì, thì theo Thông tư sáu mươi tư, cần hợp đồng với ngân hàng và sự đồng ý của khách."""),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 30) == 10", "30 - alg.bnx_l14_bucket(5, 10, [0] * 30) == 20",
               "alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 14"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① dịch vụ và REST API", "mỗi dịch vụ là một chương trình riêng, mở chức năng qua đường dẫn HTTP", "<code>POST /transfers</code> ở dịch vụ Thanh toán"],
                  ["② mã truy cập và phạm vi quyền", "mã ghi người gọi được làm gì; sai phạm vi thì bị từ chối", "mã <code>accounts:read</code> gọi API cần <code>payments:write</code> → 403"],
                  ["③ mã trạng thái 429", "“quá nhiều yêu cầu”: người gọi phải chậm lại rồi thử sau", "yêu cầu thứ 11 gửi cùng lúc → 429"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, mỗi dịch vụ là một chương trình riêng, mở chức năng của nó qua các đường dẫn HTTP, ví dụ đường dẫn chuyển tiền ở dịch vụ Thanh toán.
           Thứ hai, ở bài 4 ta đã thấy mã truy cập ghi rõ người gọi được làm gì. Mã chỉ có quyền đọc tài khoản mà gọi API ghi thanh toán thì bị từ chối với mã bốn trăm linh ba.
           Thứ ba, mã trạng thái bốn trăm hai mươi chín nghĩa là quá nhiều yêu cầu, người gọi phải chậm lại rồi thử sau."""),
        st("""<p>④ Phân số giữ đúng thời gian: $\\frac{1}{30}$ giây không viết gọn được thành số thập phân hữu hạn.</p>
$$5 \\cdot \\frac{1}{30} = \\frac{5}{30} = \\frac{1}{6}$$""",
           """Thứ tư là phân số. Một phần ba mươi giây không viết gọn được thành số thập phân hữu hạn, nên ta giữ dạng phân số để không lệch.
           Ví dụ, năm nhân một phần ba mươi bằng năm phần ba mươi, rút gọn còn một phần sáu."""),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 11) == 10", "5 * Fraction(1, 30) == Fraction(5, 30) == Fraction(1, 6)"])

    sym = sc("sym", "symbol", "Giải mã các từ của bài", [
        st(table(["từ", "nghĩa"],
                 [["ngữ cảnh giới hạn <i>(bounded context)</i>", "vùng mà mỗi từ có đúng một nghĩa; DDD chia mô hình lớn thành nhiều vùng như vậy (Evans, <i>Domain-Driven Design</i>, 2003)"],
                  ["ngôn ngữ chung <i>(ubiquitous language)</i>", "người nghiệp vụ và lập trình viên dùng cùng một bộ từ, và chính các từ đó có trong mã"],
                  ["aggregate, gốc <i>(root)</i>", "cụm đối tượng được coi là một khối; bên ngoài chỉ chạm vào gốc; một giao dịch không vượt ranh giới cụm"],
                  ["bất biến", "điều luôn đúng sau mọi thao tác, ví dụ số dư không âm"]]),
           """Bảng này giải mã bốn từ của thiết kế hướng miền, theo cuốn sách năm hai nghìn không trăm linh ba cùng tên. Ngữ cảnh giới hạn là vùng mà mỗi từ có đúng một nghĩa, và mô hình lớn được chia thành nhiều vùng như vậy.
           Ngôn ngữ chung là người nghiệp vụ và lập trình viên dùng cùng một bộ từ, và chính các từ đó có trong mã.
           Cụm thực thể là nhóm đối tượng coi như một khối, bên ngoài chỉ chạm vào gốc, và một giao dịch không vượt ranh giới cụm. Bất biến là điều luôn đúng sau mọi thao tác, ví dụ số dư không âm."""),
        st(table(["từ", "nghĩa"],
                 [["cổng API <i>(API gateway)</i>", "cửa vào duy nhất cho mọi người gọi từ bên ngoài, đứng trước các dịch vụ"],
                  ["thùng token <i>(token bucket)</i>", "thùng chứa tối đa $b$ thẻ, mỗi giây thêm $r$ thẻ; mỗi yêu cầu lấy 1 thẻ, hết thẻ thì từ chối"],
                  ["mã tương quan <i>(correlation ID)</i>", "một mã gắn vào yêu cầu ở cổng và chuyển qua mọi dịch vụ, để lần theo một yêu cầu trong nhật ký"],
                  ["Open API, bên thứ ba", "API ngân hàng cung cấp cho tổ chức khác có hợp đồng với ngân hàng"]]),
           """Bảng thứ hai là từ của cửa vào. Cổng API là cửa vào duy nhất cho mọi người gọi từ bên ngoài, đứng trước các dịch vụ.
           Thùng Token chứa tối đa b thẻ và mỗi giây thêm r thẻ, mỗi yêu cầu lấy một thẻ, hết thẻ thì bị từ chối.
           Mã tương quan được gắn vào yêu cầu ở cổng rồi chuyển qua mọi dịch vụ, để lần theo đúng một yêu cầu trong nhật ký.
           Còn API mở là các API ngân hàng cung cấp cho bên thứ ba, tức tổ chức khác có hợp đồng với ngân hàng.""", clear=True),
    ])

    intu = sc("intuition", "intuition", "Hình dung: ranh giới, cửa vào và luồng đồng ý", [
        st(svg(1500, 460,
               panel(20, 20, 470, 340, "Tài khoản", C_BLUE),
               box(45, 90, 420, 110, ["khách hàng =", "chủ tài khoản"], C_GRAY, size=24),
               box(45, 225, 420, 110, ["aggregate Tài khoản:", "số dư không âm"], C_GREEN, size=24),
               panel(515, 20, 470, 340, "Thanh toán", C_AMBER),
               box(540, 90, 420, 110, ["khách hàng =", "người ra lệnh chuyển"], C_GRAY, size=24),
               box(540, 225, 420, 110, ["hạn mức =", "100 triệu đồng/ngày"], C_AMBER, size=24),
               panel(1010, 20, 470, 340, "Tín dụng", C_PURPLE),
               box(1035, 90, 420, 110, ["khách hàng =", "người vay được chấm điểm"], C_GRAY, size=24),
               box(1035, 225, 420, 110, ["hạn mức =", "50 triệu đồng được duyệt"], C_PURPLE, size=24),
               txt(750, 405, "cùng chữ, khác nghĩa: mỗi ngữ cảnh một mô hình, gọi nhau qua API", 26, "middle", "#1f2937", True),
               txt(750, 445, "(hạn mức là số minh hoạ)", 22, "middle", "#6b7280")),
           """Hình đầu chia hệ thống ngân hàng thành ba ngữ cảnh. Ở Tài khoản, khách hàng là chủ tài khoản, và cụm thực thể Tài khoản giữ bất biến số dư không âm.
           Ở Thanh toán, khách hàng là người ra lệnh chuyển, còn hạn mức là số tiền được chuyển mỗi ngày, ví dụ một trăm triệu đồng.
           Ở Tín dụng, khách hàng là người vay được chấm điểm, và hạn mức là khoản vay được duyệt, ví dụ năm mươi triệu đồng. Hai hạn mức này là số minh hoạ.
           Cùng một chữ mà khác nghĩa, nên mỗi ngữ cảnh giữ mô hình riêng và gọi nhau qua API."""),
        st(svg(1500, 490,
               box(20, 170, 250, 110, ["ứng dụng,", "bên thứ ba"], C_BLUE, bold=True),
               panel(340, 20, 620, 400, "Cổng API", C_GRAY),
               box(365, 80, 570, 70, "1. xác thực mã truy cập", C_GREEN, size=24),
               box(365, 165, 570, 70, "2. giới hạn tốc độ: 5/giây, sức chứa 10", C_AMBER, size=24),
               box(365, 250, 570, 70, "3. định tuyến theo đường dẫn", C_BLUE, size=24),
               box(365, 335, 570, 70, "4. nhật ký; mã tương quan gắn trước khi chuyển", C_PURPLE, size=24),
               box(1060, 40, 420, 100, ["Tài khoản", "vẫn kiểm quyền"], C_BLUE, size=24),
               box(1060, 180, 420, 100, ["Thanh toán", "vẫn kiểm quyền"], C_AMBER, size=24),
               box(1060, 320, 420, 100, ["Tín dụng", "vẫn kiểm quyền"], C_PURPLE, size=24),
               arrow(270, 205, 335, 205, "#2a78d6"),
               arrow(335, 255, 275, 255, "#dc2626", dash=True),
               txt(170, 330, "quá giới hạn", 22, "middle", "#dc2626"), txt(170, 358, "→ 429", 22, "middle", "#dc2626"),
               arrow(960, 285, 1055, 90, "#475569"), arrow(960, 285, 1055, 230, "#475569"), arrow(960, 285, 1055, 370, "#475569"),
               txt(750, 470, "cổng làm việc chung một lần; dịch vụ vẫn tự kiểm phạm vi quyền", 26, "middle", "#1f2937", True)),
           """Hình thứ hai là cửa vào. Mọi yêu cầu từ ứng dụng hay bên thứ ba đi qua cổng API trước.
           Cổng làm bốn việc, thứ tự cụ thể tuỳ cấu hình. Đó là xác thực mã truy cập, giới hạn tốc độ năm yêu cầu mỗi giây với sức chứa mười, định tuyến theo đường dẫn, và ghi nhật ký. Mã tương quan được gắn trước khi chuyển yêu cầu đi, để dịch vụ phía sau nhận được nó.
           Yêu cầu quá giới hạn bị trả về mã bốn trăm hai mươi chín ngay ở cổng, nên không làm tốn sức các dịch vụ phía sau.
           Nhưng mỗi dịch vụ vẫn tự kiểm phạm vi quyền. Cổng thường chỉ kiểm mã hợp lệ và phạm vi thô theo đường dẫn, không biết luật nghiệp vụ của từng dịch vụ."""),
        st(svg(1500, 470,
               box(20, 60, 260, 110, ["Khách hàng", "chủ dữ liệu"], C_BLUE, bold=True),
               box(680, 60, 330, 110, ["Bên thứ ba", "có hợp đồng (Điều 8)"], C_AMBER, bold=True),
               box(1180, 40, 300, 300, ["Ngân hàng", "cổng Open API", "chỉ trả dữ liệu", "khách đã đồng ý,", "đúng phạm vi"], C_GREEN, bold=True),
               arrow(280, 115, 675, 115, "#2a78d6", "1. đồng ý rõ ràng, tự nguyện"),
               arrow(1010, 115, 1175, 115, "#d97706", "2. gọi Open API", size=20),
               arrow(150, 170, 150, 290, "#475569", dash=True),
               arrow(150, 300, 1175, 300, "#9333ea", "3. tra cứu, rút lại sự đồng ý (Điều 11)", dash=True),
               txt(750, 400, "Thông tư 64/2024/TT-NHNN: ban hành 31/12/2024, hiệu lực 01/3/2025", 26, "middle", "#1f2937", True),
               txt(750, 440, "danh mục Open API cơ bản ở Phụ lục 01", 24, "middle", "#1f2937")),
           """Hình thứ ba là luồng của API mở theo Thông tư sáu mươi tư, ban hành ngày ba mươi mốt tháng mười hai năm hai nghìn không trăm hai mươi tư.
           Bước một, khách hàng là chủ dữ liệu, đồng ý một cách rõ ràng, tự nguyện. Bước hai, bên thứ ba đã ký hợp đồng với ngân hàng mới được gọi API mở.
           Ngân hàng chỉ trả dữ liệu khách đã đồng ý, đúng phạm vi đã thoả thuận. Bước ba, khách có thể tra cứu dữ liệu đã đồng ý chia sẻ và rút lại sự đồng ý.
           Danh mục API mở cơ bản nằm ở Phụ lục một của thông tư, và thông tư có hiệu lực từ ngày một tháng ba năm hai nghìn không trăm hai mươi lăm."""),
        st(table(["điều thông tư ghi", "nội dung"],
                 [["Open API", "tập hợp các API ngân hàng cung cấp cho bên thứ ba trực tiếp kết nối, xử lý dữ liệu"],
                  ["Điều 8", "ngân hàng phải ký hợp đồng với bên thứ ba về triển khai Open API; cam kết dùng dữ liệu đúng phạm vi, mục đích"],
                  ["Điều 11", "khách tra cứu được dữ liệu đã đồng ý cho bên thứ ba xử lý, rút lại được sự đồng ý; thời hạn truy vấn sau khi khách đồng ý không quá 180 ngày"],
                  ["nguồn", "Tạp chí Ngân hàng 24/02/2025; trang NHNN 14/11/2025 (trích Thông tư 64/2024/TT-NHNN)"]]),
           """Bảng này ghi những điều thông tư nói, theo bài của Tạp chí Ngân hàng và trang tin của Ngân hàng Nhà nước. API mở là tập hợp các API ngân hàng cung cấp cho bên thứ ba trực tiếp kết nối và xử lý dữ liệu.
           Điều tám buộc ngân hàng ký hợp đồng với bên thứ ba, trong đó bên thứ ba cam kết dùng dữ liệu đúng phạm vi và mục đích.
           Điều mười một cho khách tra cứu và rút lại sự đồng ý, và thời hạn được truy vấn thông tin sau khi khách đồng ý không quá một trăm tám mươi ngày.
           Hai bài báo đó dẫn lại văn bản, nên khi làm việc thật bạn hãy đọc nguyên văn thông tư.""", clear=True),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: ranh giới, bất biến, rồi thùng token", [
        st("""<p><b>Bước 1.</b> Vì “hạn mức” ở Thanh toán và ở Tín dụng theo hai luật khác nhau, nên mỗi nghĩa nằm trong ngữ cảnh của nó, không dùng chung một cột.</p>
<span class='note'>Làm thử (số minh hoạ, đơn vị triệu đồng): hôm nay đã chuyển 80, chuyển thêm 30; hạn mức vay 50 không liên quan.</span>
$$80 + 30 = 110 > 100 \\;\\to\\; \\text{Thanh toán từ chối}$$""",
           """Bước một, vì chữ hạn mức ở Thanh toán và ở Tín dụng theo hai luật khác nhau, nên mỗi nghĩa nằm trong ngữ cảnh của nó, không dùng chung một cột.
           Làm thử với số minh hoạ, hôm nay khách đã chuyển tám mươi triệu, muốn chuyển thêm ba mươi triệu. Tám mươi cộng ba mươi là một trăm mười, vượt một trăm, nên Thanh toán từ chối, còn hạn mức vay năm mươi triệu không liên quan."""),
        st("""<p><b>Bước 2.</b> Mọi thay đổi số dư đi qua <b>gốc</b> aggregate Tài khoản, nên bất biến “số dư không âm” chỉ phải kiểm ở <b>một</b> chỗ.</p>
<span class='note'>Làm thử: số dư $300\\,000$, ghi nợ $500\\,000$ → từ chối, giữ $300\\,000$; ghi nợ $200\\,000$ → $300\\,000 - 200\\,000 = 100\\,000$.</span>""",
           """Bước hai, mọi thay đổi số dư đi qua gốc của cụm Tài khoản, nên bất biến số dư không âm chỉ phải kiểm ở một chỗ.
           Làm thử, số dư ba trăm nghìn, ghi nợ năm trăm nghìn thì bị từ chối và số dư giữ ba trăm nghìn. Ghi nợ hai trăm nghìn thì được, còn một trăm nghìn.""", focus=[1, 2, 2]),
        st("""<p><b>Bước 3.</b> Ở cổng, mỗi yêu cầu cần $1$ thẻ. Thùng thêm $r = 5$ thẻ mỗi giây và chứa tối đa $b = 10$: sức chứa cho dồn ngắn, tốc độ giữ trung bình.</p>
<span class='note'>Làm thử: sau $\\frac{1}{30}$ giây thùng thêm $5 \\cdot \\frac{1}{30} = \\frac{1}{6}$ thẻ.</span>""",
           """Bước ba, ở cổng mỗi yêu cầu cần một thẻ. Thùng thêm r bằng năm thẻ mỗi giây và chứa tối đa b bằng mười, vì sức chứa cho phép dồn ngắn hạn, còn tốc độ giữ mức trung bình.
           Làm thử, sau một phần ba mươi giây thùng thêm năm nhân một phần ba mươi, tức một phần sáu thẻ.""", clear=True),
        st("""<p><b>Bước 4.</b> Trước mỗi yêu cầu: số thẻ $=$ thẻ còn $+ \\, r \\cdot$ thời gian đã trôi, nhưng không quá $b$. Có ít nhất $1$ thẻ thì nhận và trừ $1$.</p>
<span class='note'>Làm thử: còn $9$ thẻ, sau $\\frac{1}{30}$ giây: $9 + \\frac{1}{6} = \\frac{55}{6}$, vẫn dưới $10$ nên giữ nguyên.</span>""",
           """Bước bốn, trước mỗi yêu cầu, số thẻ bằng thẻ còn lại cộng r nhân thời gian đã trôi, nhưng không quá b, vì thùng đầy thì thẻ thêm bị tràn ra ngoài. Có ít nhất một thẻ thì nhận yêu cầu và trừ một thẻ.
           Làm thử, còn chín thẻ, sau một phần ba mươi giây được chín cộng một phần sáu, là năm mươi lăm phần sáu, vẫn dưới mười nên giữ nguyên."""),
    ], checks=["80 + 30 == 110 > 100", "alg.bnx_l14_debit(300000, 500000) == (300000, False)", "alg.bnx_l14_debit(300000, 200000) == (100000, True)",
               "5 * Fraction(1, 30) == Fraction(1, 6)", "alg.bnx_l14_bucket_trace(5, 10, " + SPREAD + ")[1][1] == 9 + Fraction(1, 6) == Fraction(55, 6)"])

    ex = sc("example", "example", "Ví dụ: 30 yêu cầu qua cổng, từng phép tính", [
        st("""<p>Cổng $r = 5$ thẻ/giây, $b = 10$. Thùng bắt đầu <b>đầy</b> $10$ thẻ. Trường hợp A: $30$ yêu cầu đến <b>cùng lúc</b>, thời gian trôi bằng $0$ nên không thêm thẻ.</p>
$$① \\; \\text{nhận} = \\hl{10}$$""",
           """Ta tính từng bước. Cổng có r bằng năm thẻ mỗi giây và b bằng mười, và thùng bắt đầu đầy mười thẻ. Trường hợp thứ nhất, ba mươi yêu cầu đến cùng lúc, thời gian trôi bằng không nên không thêm thẻ nào.
           Phép tính thứ nhất, mười thẻ đầu tiên cho mười yêu cầu, nên nhận mười.""", focus=[1, 1, 1, 2]),
        st("""$$② \\; 30 - 10 = \\hl{20}\\ \\text{bị từ chối (429)}$$""",
           """Phép tính thứ hai, dùng lại số mười ở trên. Ba mươi trừ mười bằng hai mươi yêu cầu bị từ chối với mã bốn trăm hai mươi chín."""),
        st("""<p>Trường hợp B: $30$ yêu cầu <b>rải đều</b> trong $1$ giây, ở thời điểm $0, \\frac{1}{30}, \\frac{2}{30}, \\dots, \\frac{29}{30}$.</p>
$$③ \\; 1 - \\frac{1}{6} = \\hl{\\frac{5}{6}}\\ \\text{thẻ mất đi sau mỗi yêu cầu được nhận}$$""",
           """Trường hợp thứ hai, ba mươi yêu cầu rải đều trong một giây, ở thời điểm không, một phần ba mươi, hai phần ba mươi, và cứ thế tới hai mươi chín phần ba mươi giây. Dấu ba chấm nghĩa là cứ thế tiếp tục.
           Phép tính thứ ba, mỗi yêu cầu lấy một thẻ mà giữa hai yêu cầu chỉ thêm một phần sáu thẻ, nên mỗi lần nhận, thùng mất đi năm phần sáu thẻ.""", introduces=["dots"]),
        st("""<p>Dùng lại $\\frac{5}{6}$: trước yêu cầu thứ $11$ (thời điểm $\\frac{10}{30}$) đã nhận $10$ yêu cầu.</p>
$$④ \\; 10 - 10 \\cdot \\frac{5}{6} = \\hl{\\frac{5}{3}} \\geq 1 \\ \\text{nên nhận đủ } 11 \\text{ yêu cầu đầu}$$""",
           """Phép tính thứ tư dùng lại năm phần sáu. Trước yêu cầu thứ mười một, ở thời điểm mười phần ba mươi giây, cổng đã nhận mười yêu cầu.
           Số thẻ còn mười trừ mười nhân năm phần sáu, bằng năm phần ba, vẫn lớn hơn hoặc bằng một, nên mười một yêu cầu đầu đều được nhận.""",
           introduces=["geq"], clear=True),
        st("""<p>Sau yêu cầu thứ 11, thùng còn 2/3 thẻ. Mỗi khoảng thêm 1/6 thẻ, nên thêm 2 khoảng là đủ 1 thẻ: nhận ở 12/30 giây.</p>
<p>Sau đó thùng về 0, cứ 6 khoảng (1/5 giây) mới đủ 1 thẻ: nhận ở 18/30 và 24/30 giây.</p>
$$⑤ \\; 11 + 3 = \\hlg{14}\\ \\text{nhận}, \\quad 30 - 14 = 16\\ \\text{từ chối}$$""",
           """Phép tính thứ năm. Sau yêu cầu thứ mười một, thùng còn hai phần ba thẻ. Mỗi khoảng thêm một phần sáu thẻ, nên chỉ cần thêm hai khoảng là đủ một thẻ, và cổng nhận yêu cầu ở mười hai phần ba mươi giây.
           Sau đó thùng về không, nên cứ sáu khoảng, tức một phần năm giây, mới đủ một thẻ, và cổng nhận ở mười tám và hai mươi tư phần ba mươi giây.
           Tổng là mười một cộng ba bằng mười bốn được nhận, còn mười sáu bị từ chối.""", focus=[3, 1, 1, 2, 3], clear=True),
        st(code(BUCKET_PY, "Mô phỏng cổng bằng Python, dùng phân số"),
           """Giờ ta cho máy tính lại bằng Python. Câu lệnh đầu nạp kiểu phân số, để một phần ba mươi giây được giữ đúng, không lệch như số thực.
           Hàm cong, tức là cổng, nhận tốc độ, sức chứa và danh sách thời điểm, rồi bắt đầu với thùng đầy.
           Với mỗi thời điểm, thùng được cộng tốc độ nhân thời gian đã trôi, nhưng không quá sức chứa. Còn ít nhất một thẻ thì trừ một thẻ và đếm thêm một yêu cầu được nhận.
           Hai câu lệnh cuối chạy hai trường hợp, cùng lúc và rải đều.""", clear=True, focus=[1, 2, 2, 2, 2, 2]),
        st("<p>Bằng tay: cùng lúc nhận $10$ (phép ①), rải đều nhận $14$ (phép ⑤).</p>" + out(BUCKET_OUT),
           """Bằng tay, ta đã tính cùng lúc nhận mười ở phép tính thứ nhất, và rải đều nhận mười bốn ở phép tính thứ năm. Kết quả chạy thật in ra mười rồi mười bốn, khớp cả hai.""", clear=True, focus=[1, 3]),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 30) == 10", "30 - alg.bnx_l14_bucket(5, 10, [0] * 30) == 20",
               "1 - Fraction(1, 6) == Fraction(5, 6)",
               "alg.bnx_l14_bucket_trace(5, 10, " + SPREAD + ")[10][1] == 10 - 10 * Fraction(5, 6) == Fraction(5, 3)",
               "alg.bnx_l14_accepted_idx(5, 10, " + SPREAD + ")[:11] == list(range(11))",
               "alg.bnx_l14_accepted_idx(5, 10, " + SPREAD + ")[11:] == [12, 18, 24]",
               "alg.bnx_l14_bucket_trace(5, 10, " + SPREAD + ")[10][1] - 1 == Fraction(2, 3)",
               "Fraction(2, 3) + 2 * Fraction(1, 6) == 1 == 6 * Fraction(1, 6) == 6 * Fraction(1, 30) * 5", "Fraction(6, 30) == Fraction(1, 5)",
               "alg.bnx_l14_bucket_trace(5, 10, " + SPREAD + ")[11][1] == Fraction(5, 6) < 1",
               "alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 11 + 3 == 14", "30 - alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 16"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cận trên của cổng", [
        st("""<p>Đường khác: trong khoảng thời gian $T$, cổng phát ra nhiều nhất $b + r \\cdot T$ thẻ, nên số yêu cầu nhận được không vượt quá số đó.</p>
$$\\text{A: } 10 + 5 \\cdot 0 = \\hl{10} \\qquad \\text{B: } 10 + 5 \\cdot \\frac{29}{30} = \\frac{89}{6} \\approx 14{,}8 \\;\\to\\; \\text{nhiều nhất } \\hlg{14}$$""",
           """Kiểm bằng đường khác, không cần mô phỏng. Trong khoảng thời gian T, cổng phát ra nhiều nhất b cộng r nhân T thẻ, nên số yêu cầu được nhận không vượt quá số đó.
           Trường hợp cùng lúc, T bằng không, cận trên là mười, đúng bằng kết quả mô phỏng.
           Trường hợp rải đều, T là hai mươi chín phần ba mươi giây, cận trên là tám mươi chín phần sáu, xấp xỉ mười bốn phẩy tám. Không nhận được nửa yêu cầu, nên nhiều nhất mười bốn, cũng khớp.""", focus=[1, 1, 2, 2, 2]),
        st(table(["kiểm", "cách tính khác", "kết quả"],
                 [["số yêu cầu nhận ở B", "đếm thời điểm: 0 tới 10/30 là 11, thêm 12/30, 18/30, 24/30", "11 + 3 = 14"],
                  ["ngày ban hành tới ngày hiệu lực", "1 ngày cuối tháng 12, 31 ngày tháng 1, 28 ngày tháng 2", "1 + 31 + 28 = 60 ngày"]]),
           """Bảng này kiểm thêm hai điều bằng cách đếm, vì đếm thẳng là một đường độc lập với công thức. Đếm thời điểm được nhận, từ không tới mười phần ba mươi là mười một, thêm ba thời điểm sau, tổng mười bốn.
           Từ ngày ban hành tới ngày hiệu lực của thông tư, ta đếm một ngày cuối tháng mười hai, ba mươi mốt ngày tháng một và hai mươi tám ngày tháng hai, tổng sáu mươi ngày.""", clear=True),
    ], checks=["alg.bnx_l14_bound(5, 10, 0) == alg.bnx_l14_bucket(5, 10, [0] * 30) == 10",
               "10 + 5 * Fraction(29, 30) == Fraction(89, 6)", "round(float(Fraction(89, 6)), 1) == 14.8",
               "alg.bnx_l14_bound(5, 10, Fraction(29, 30)) == alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 14",
               "len(alg.bnx_l14_accepted_idx(5, 10, " + SPREAD + ")) == 11 + 3",
               "alg.bnx_l14_days('31/12/2024', '01/03/2025') == 1 + 31 + 28 == 60"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng DDD <b class="red">bắt buộc</b> tách thành nhiều microservice. DDD vẽ ranh giới trước; ranh giới đó có thể là <b>mô-đun trong một ứng dụng</b>, cách triển khai tính sau.</div>""",
           """Lỗi thứ nhất, của người mới, là tưởng thiết kế hướng miền bắt buộc tách thành nhiều Microservice. Thiết kế hướng miền vẽ ranh giới trước.
           Ranh giới đó có thể chỉ là các mô-đun trong một ứng dụng, còn cách triển khai thì tính sau, khi đã có lý do."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Cổng đã kiểm mã nên dịch vụ <b class="red">bỏ kiểm quyền</b>. Nếu cổng không được cấu hình kiểm phạm vi, mã <code>accounts:read</code> hợp lệ vẫn qua cổng; khi đó nếu dịch vụ Thanh toán không tự kiểm phạm vi <code>payments:write</code>, lệnh chuyển tiền sẽ chạy.
<br><span class="note">Phép thử bắt lỗi: gọi thẳng dịch vụ bằng mã sai phạm vi, phải nhận 403.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là nghĩ cổng đã kiểm mã nên dịch vụ bỏ kiểm quyền. Nếu cổng không được cấu hình kiểm phạm vi, mã chỉ có quyền đọc tài khoản vẫn hợp lệ nên vẫn qua cổng.
           Nếu dịch vụ Thanh toán không tự kiểm phạm vi ghi thanh toán, lệnh chuyển tiền sẽ chạy. Phép thử bắt lỗi là gọi thẳng dịch vụ bằng mã sai phạm vi, và phải nhận mã bốn trăm linh ba."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bên thứ ba đã có thông tin kết nối là <b class="red">trả mọi dữ liệu</b>. Theo Thông tư 64, cần hợp đồng với bên thứ ba <b>và</b> sự đồng ý của khách, chỉ trả đúng phạm vi đã đồng ý; khách rút lại thì dừng.
<br><span class="note">Phép thử bắt lỗi: khách rút lại sự đồng ý, lần gọi kế tiếp phải bị từ chối.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là thấy bên thứ ba có thông tin kết nối thì trả mọi dữ liệu. Theo Thông tư sáu mươi tư, cần hợp đồng với bên thứ ba và sự đồng ý của khách.
           Ngân hàng chỉ trả đúng phạm vi khách đã đồng ý, và khách rút lại thì phải dừng. Phép thử bắt lỗi là cho khách rút lại sự đồng ý, rồi lần gọi kế tiếp phải bị từ chối."""),
    ])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Cổng 5 thẻ/giây, sức chứa 10. 40 yêu cầu đến cùng lúc: nhận bao nhiêu, từ chối bao nhiêu?"],
                  ["2", "Cổng 2 thẻ/giây, sức chứa 3. 6 yêu cầu cách nhau 1/4 giây (0, 1/4, …, 5/4): nhận bao nhiêu?"],
                  ["3", "Quyết định: đội 5 người, một cơ sở dữ liệu Oracle. Tách Tài khoản và Thanh toán thành hai dịch vụ ngay, hay một ứng dụng có hai mô-đun ranh giới rõ?"]]),
           """Đến lượt bạn. Câu một, cổng năm thẻ mỗi giây, sức chứa mười, bốn mươi yêu cầu đến cùng lúc, nhận bao nhiêu và từ chối bao nhiêu?
           Câu hai, cổng hai thẻ mỗi giây, sức chứa ba, sáu yêu cầu cách nhau một phần tư giây, nhận bao nhiêu?
           Câu ba là một quyết định. Đội năm người dùng một cơ sở dữ liệu Oracle, nên tách Tài khoản và Thanh toán thành hai dịch vụ ngay, hay giữ một ứng dụng có hai mô-đun ranh giới rõ? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: cùng lúc nên không thêm thẻ, chỉ có $10$ thẻ ban đầu.</p>
$$\\text{nhận } \\hl{10}, \\quad 40 - 10 = \\hl{30}\\ \\text{từ chối}$$""",
           """Đáp án câu một. Các yêu cầu đến cùng lúc nên không thêm thẻ, chỉ có mười thẻ ban đầu. Vậy nhận mười, và bốn mươi trừ mười bằng ba mươi yêu cầu bị từ chối."""),
        st("""<p>Câu 2: mỗi khoảng thêm $2 \\cdot \\frac{1}{4} = \\frac{1}{2}$ thẻ, mỗi lần nhận mất $1 - \\frac{1}{2} = \\frac{1}{2}$. Trước yêu cầu thứ $5$: $3 - 4 \\cdot \\frac{1}{2} = 1$ nên nhận; yêu cầu thứ $6$ chỉ có $\\frac{1}{2}$ thẻ.</p>
$$\\text{nhận } \\hlg{5}, \\quad \\text{cận trên } 3 + 2 \\cdot \\frac{5}{4} = 5{,}5$$""",
           """Đáp án câu hai. Mỗi khoảng một phần tư giây thêm hai nhân một phần tư, bằng nửa thẻ, nên mỗi lần nhận thùng mất nửa thẻ.
           Trước yêu cầu thứ năm còn ba trừ bốn nhân một nửa, bằng một thẻ, nên vẫn nhận. Yêu cầu thứ sáu chỉ có nửa thẻ nên bị từ chối.
           Vậy nhận năm. Kiểm bằng cận trên, ba cộng hai nhân năm phần tư bằng năm phẩy năm, nên nhiều nhất là năm, khớp.""", focus=[1, 1, 1, 1, 2, 2]),
        st(table(["lựa chọn", "được", "mất", "đổi khi"],
                 [["một ứng dụng, hai mô-đun", "chuyển tiền và ghi sổ trong một giao dịch, một lần chốt; triển khai một lần", "phải giữ kỷ luật: mô-đun này không đọc bảng của mô-đun kia", "hai phần cần nhịp phát hành hoặc mức tải khác hẳn nhau (đo được)"],
                  ["hai dịch vụ riêng", "triển khai, co giãn độc lập", "giao dịch vượt hai dịch vụ phải dùng SAGA, Outbox; thêm lời gọi mạng, thêm chỗ hỏng", "đội nhỏ, chưa đo thấy nghẽn: chưa cần"]]),
           """Đáp án câu ba là một đánh đổi. Một ứng dụng hai mô-đun thì chuyển tiền và ghi sổ nằm trong một giao dịch, một lần chốt, triển khai một lần. Đổi lại phải giữ kỷ luật, mô-đun này không đọc bảng của mô-đun kia.
           Hai dịch vụ riêng thì triển khai và co giãn độc lập, nhưng giao dịch vượt hai dịch vụ phải dùng SAGA hay Outbox, thêm lời gọi mạng và thêm chỗ hỏng.
           Với đội năm người chưa đo thấy nghẽn, hai mô-đun là đủ. Nên đổi sang hai dịch vụ khi đo được hai phần cần nhịp phát hành hoặc mức tải khác hẳn nhau."""),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 40) == 10", "40 - alg.bnx_l14_bucket(5, 10, [0] * 40) == 30",
               "2 * Fraction(1, 4) == Fraction(1, 2) == 1 - Fraction(1, 2)",
               "alg.bnx_l14_bucket_trace(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2)))[4][1] == 3 - 4 * Fraction(1, 2) == 1",
               "alg.bnx_l14_bucket_trace(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2)))[5][1] == Fraction(1, 2)",
               "alg.bnx_l14_bucket(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2))) == 5 == alg.bnx_l14_bound(2, 3, Fraction(5, 4))",
               "3 + 2 * Fraction(5, 4) == Fraction(11, 2)"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("một chữ, nhiều nghĩa", "ngữ cảnh giới hạn", "gốc aggregate giữ bất biến", "cổng: xác thực, giới hạn, định tuyến, nhật ký",
                 "dịch vụ vẫn kiểm quyền", "Open API: hợp đồng + đồng ý"),
           """Tổng kết chuỗi logic. Một chữ có nhiều nghĩa, nên ta chia thành ngữ cảnh giới hạn, và trong mỗi ngữ cảnh, gốc của cụm thực thể giữ bất biến.
           Ở cửa vào, cổng xác thực, giới hạn tốc độ, định tuyến và ghi nhật ký, nhưng dịch vụ vẫn tự kiểm quyền. Với bên thứ ba, API mở cần hợp đồng và sự đồng ý của khách."""),
        st("""<div class='box key'><b>Tư duy:</b> vẽ ranh giới theo <b>nghĩa của từ</b> trước khi chọn công nghệ; mỗi lớp bảo vệ (cổng, dịch vụ, cơ sở dữ liệu) tự kiểm phần của nó, không lớp nào tin lớp trước đã kiểm hộ.</div>""",
           """Điều cần mang theo. Hãy vẽ ranh giới theo nghĩa của từ trước khi chọn công nghệ. Mỗi lớp bảo vệ, gồm cổng, dịch vụ và cơ sở dữ liệu, tự kiểm phần của nó, không lớp nào tin lớp trước đã kiểm hộ."""),
        st("""<p class='note'>Bài sau (bài tổng hợp): ghép mọi mảnh đã học thành một dự án mẫu API chuyển khoản đúng như tin tuyển dụng đòi hỏi.</p>""",
           """Ở bài sau, bài tổng hợp, ta ghép mọi mảnh đã học thành một dự án mẫu API chuyển khoản. Bài đó có ước lượng tải và ngân sách thời gian cho từng phần, đúng như tin tuyển dụng đòi hỏi.""",
           forward_ref=True),
    ])
    return lesson("L14", "ddd_cong_api_open_api", "Bài 14 — DDD, cổng API và Open API ngân hàng: ranh giới, cửa vào và chia sẻ dữ liệu có đồng ý",
                  "curriculum/bnx.yaml L14; audit/bnx/verify_bnx.py L14; Evans, Domain-Driven Design (2003), qua M. Fowler, bliki BoundedContext (15/01/2014), "
                  "DDD_Aggregate (23/04/2013), DomainDrivenDesign (22/04/2020); C. Richardson, microservices.io Pattern: API Gateway; AWS API Gateway Developer Guide "
                  "“Throttle requests” (thùng token, 429); Thông tư 64/2024/TT-NHNN (31/12/2024, hiệu lực 01/3/2025) qua Tạp chí Ngân hàng (24/02/2025) và sbv.gov.vn (14/11/2025) "
                  "[TT64] [TT64b] [DDD] [AGW] — đọc 2026-11-11; giới hạn 5/giây, sức chứa 10 và hạn mức 100/50 triệu là số minh hoạ",
                  ["Chia hệ thống ngân hàng thành ngữ cảnh giới hạn", "Nhận ra một khái niệm mang nghĩa khác nhau ở hai ngữ cảnh",
                   "Liệt kê việc cổng API làm: xác thực, giới hạn tốc độ, định tuyến, nhật ký", "Mô tả Open API ngân hàng theo Thông tư 64/2024/TT-NHNN"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
