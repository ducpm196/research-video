import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene
from spk12 import spoken
from libj import jstep, nowrap

lib2.begin("L14")

# Mã trên màn hình: prog(...) chạy THẬT (đệm ở audit/bnx/progcache/L14.json); đầu ra ASCII
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
BUCKET = prog("Bucket", BUCKET_PY, lang="python", out=BUCKET_OUT,
              claims=["thùng token 5/giây, sức chứa 10: 30 yêu cầu cùng lúc nhận 10; rải đều trong 1 giây nhận 14"])

# Quy mô: nhiều bên thứ ba giống nhau cùng gọi; mỗi bên có thùng riêng (giới hạn theo từng bên)
QUYMO_PY = """from fractions import Fraction as F
def nhan(rate, cap, times):
    tok, last, ok = F(cap), F(0), 0
    for t in times:
        tok = min(F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:
            tok, ok = tok - 1, ok + 1
    return ok

dong = [F(0)] * 30
rai = [F(i, 30) for i in range(30)]
for n in (1, 100, 10_000):
    a = sum(nhan(5, 10, dong) for _ in range(n))
    b = sum(nhan(5, 10, rai) for _ in range(n))
    print(n, a, b, 30 * n - a)"""
QUYMO_OUT = """1 10 14 20
100 1000 1400 2000
10000 100000 140000 200000"""
QUYMO = prog("Quymo", QUYMO_PY, lang="python", out=QUYMO_OUT, timeout=240,
             claims=["1, 100 và 10 000 bên thứ ba, mỗi bên gửi 30 yêu cầu: cùng lúc nhận 10, 1 000, 100 000 (từ chối 20, 2 000, 200 000); rải đều nhận 14, 1 400, 140 000"],
             unverified_claims=["hậu phương chịu 2 000 yêu cầu/giây và thời gian 5 ms, 0,5 giây, 50 giây để xử lý hết: số minh hoạ tính từ số yêu cầu đo thật chia cho 2 000; không đo hệ thống thật"])

SPREAD = "alg.bnx_l14_spread(30)"

# Lab (số liệu khác ví dụ): tốc độ 4, sức chứa 6, 20 yêu cầu; 50 bên cùng gọi; hậu phương chịu 120 yêu cầu/giây
LAB_PY = """from fractions import Fraction as F


def nhan(rate, cap, times):
    tok, last, ok = F(cap), F(0), 0
    for t in times:
        tok = min(F(cap), tok + (t - last) * rate)
        last = t
        if tok >= 1:
            tok, ok = tok - 1, ok + 1
    return ok


dong = [F(0)] * 20
rai = [F(i, 10) for i in range(20)]
a = nhan(4, 6, dong)
print("dong 20 yeu cau: nhan", a, "tu choi", 20 - a)
b = nhan(4, 6, rai)
print("rai deu: nhan", b, "can tren", int(6 + 4 * F(19, 10)))
n = 50
print(n, "ben dong:", n * a, "qua cong,", n * (20 - a), "tu choi")
print("hang cho", n * a / 120, "giay neu hau phuong chiu 120 yeu cau/giay")"""
_lp = lib2.Prog("L14", "LabSol", LAB_PY, "python", {}, "lab", {})
_rc, _so, _se = _lp.execute()
assert _rc == 0, _se
LAB_OUT = _so.strip("\n")
EXPECT_LAB = """dong 20 yeu cau: nhan 6 tu choi 14
rai deu: nhan 13 can tren 13
50 ben dong: 300 qua cong, 700 tu choi
hang cho 2.5 giay neu hau phuong chiu 120 yeu cau/giay"""
assert LAB_OUT == EXPECT_LAB, LAB_OUT

LAB_DE = """# Lab BNX L14 — Thùng token của cổng API khi nhiều bên cùng gọi

Số liệu là số minh hoạ. Viết `mau.py` (chỉ dùng Python có sẵn). **Thùng token**: thùng chứa tối đa `cap` thẻ, đầy lúc đầu, mỗi giây thêm `rate` thẻ (không quá `cap`); mỗi yêu cầu cần 1 thẻ, không đủ thì bị từ chối. Dùng `Fraction` (`from fractions import Fraction as F`) để một phần mười giây không bị lệch như số thực.

Cổng cho mỗi bên `rate = 4` thẻ/giây, `cap = 6`. Viết hàm `nhan(rate, cap, times)` nhận danh sách thời điểm (giây) của các yêu cầu theo thứ tự và trả về số yêu cầu được nhận. Rồi:

1. **20 yêu cầu đến cùng lúc** (thời điểm 0): in `dong 20 yeu cau: nhan <a> tu choi <b>`.
2. **20 yêu cầu rải đều**, cách nhau 1/10 giây (thời điểm `0, 1/10, …, 19/10`): in `rai deu: nhan <số> can tren <số>`, trong đó cận trên là phần nguyên của `cap + rate × T` với `T = 19/10` (thời điểm yêu cầu cuối).
3. **50 bên giống hệt nhau** cùng gửi 20 yêu cầu cùng lúc, mỗi bên có thùng riêng: in `50 ben dong: <tổng nhận> qua cong, <tổng từ chối> tu choi`.
4. Nếu hậu phương chỉ xử lý được 120 yêu cầu/giây, số yêu cầu qua cổng ở bước 3 cần bao nhiêu giây để xử lý hết? In `hang cho <giây> giay neu hau phuong chiu 120 yeu cau/giay` (chia số yêu cầu qua cổng cho 120, in thẳng kết quả của phép chia `/`).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L14 mau.py`. Đầu ra viết không dấu.
"""


def note(t):
    return f"<p class='note'>{t}</p>"


def build():
    write_lab("BNX", "L14", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Cửa vào của ngân hàng: 30 yêu cầu cùng một lúc", [
        st("""<p>Từ $01/3/2025$, ngân hàng bắt đầu mở API (cửa để chương trình khác gọi vào) cho <b>bên thứ ba</b> (tổ chức khác ngoài ngân hàng và khách) theo Thông tư 64/2024/TT-NHNN, với lộ trình chuyển tiếp. Một ứng dụng bên thứ ba gửi $30$ yêu cầu <b>cùng một lúc</b>.</p>
<div class="box key">Cổng API cho mỗi bên $5$ yêu cầu/giây, sức chứa $10$ <i>(số minh hoạ)</i>: nhận $10$, từ chối $20$. Nếu $30$ yêu cầu <b>rải đều trong 1 giây</b> thì nhận $14$.</div>""",
           """Chào bạn, từ một tháng ba năm hai nghìn không trăm hai mươi lăm, ngân hàng mở API, cửa cho chương trình khác, cho bên thứ ba theo Thông tư sáu mươi tư.
           Một ứng dụng bên thứ ba gửi ba mươi yêu cầu cùng lúc, mà cổng cho mỗi bên năm yêu cầu mỗi giây với sức chứa mười, là số minh hoạ. Cổng nhận mười và từ chối hai mươi, còn rải đều trong một giây thì nhận mười bốn.""",
           focus=[1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời bằng"],
                 [["chia hệ thống ngân hàng ở đâu", "<b>ngữ cảnh giới hạn</b>: mỗi nghĩa của một chữ có chỗ riêng"],
                  ["ai đứng ở cửa vào", "cổng API: kiểm ai gọi, giới hạn tốc độ, chuyển đúng dịch vụ, nhật ký"],
                  ["bên thứ ba được lấy dữ liệu gì", "Open API theo Thông tư 64: hợp đồng và sự đồng ý của khách"],
                  ["cả vạn bên cùng gọi thì phía sau cổng chịu thế nào", "đếm yêu cầu qua cổng ở 1, 100 và 10 000 bên"]]),
           """Hôm nay ta trả lời bốn câu. Chia hệ thống ở đâu thì dùng ngữ cảnh giới hạn, mỗi nghĩa của một chữ có chỗ riêng. Ai đứng ở cửa vào thì là cổng API, kiểm người gọi và chuyển đúng dịch vụ.
           Bên thứ ba được lấy dữ liệu gì thì theo Thông tư sáu mươi tư. Cả vạn bên cùng gọi thì hậu phương chịu ra sao, ta sẽ đếm.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], introduces=["bnx_ngu_canh_gioi_han"], clear=True),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 30) == 10", "30 - alg.bnx_l14_bucket(5, 10, [0] * 30) == 20",
               "alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 14"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① dịch vụ và REST API", "mỗi dịch vụ là một chương trình riêng, mở chức năng qua <b>REST API</b>: mỗi chức năng là một đường dẫn <b>HTTP</b> (cách chương trình hỏi và đáp qua mạng) kèm một động từ (GET: lấy dữ liệu; POST: gửi dữ liệu để tạo hoặc làm một việc)", "<code>POST /transfers</code>: gửi yêu cầu tạo một lệnh chuyển ở dịch vụ Thanh toán"],
                  ["② mã truy cập và phạm vi quyền", "mã ghi người gọi được làm gì; sai phạm vi thì bị từ chối", "mã <code>accounts:read</code> gọi API cần <code>payments:write</code> → 403"],
                  ["③ mã trạng thái 429", "“quá nhiều yêu cầu”: người gọi phải chậm lại rồi thử sau", "yêu cầu thứ 11 gửi cùng lúc → 429"]]),
           """Trước hết ta cần hiểu bốn điều. Một, mỗi dịch vụ là một chương trình riêng, mở chức năng qua các đường dẫn HTTP, tức cách chương trình hỏi và đáp qua mạng, mỗi đường dẫn đi với một động từ. Động từ gửi nghĩa là gửi dữ liệu để tạo một việc.
           Hai, mã truy cập ghi rõ người gọi được làm gì, nên mã chỉ có quyền đọc mà gọi API ghi thanh toán thì bị từ chối với mã bốn trăm linh ba. Ba, mã trạng thái bốn trăm hai mươi chín nghĩa là quá nhiều yêu cầu, người gọi phải chậm lại.""",
           focus=[0, "1.2", "1.3", "1.4"]),
        st("""<p>④ Phân số giữ đúng thời gian: $\\frac{1}{30}$ giây không viết gọn được thành số thập phân hữu hạn; trong Python, <code>Fraction(1, 30)</code> giữ đúng phân số.</p>
$$5 \\cdot \\frac{1}{30} = \\frac{5}{30} = \\frac{1}{6}$$""",
           """Bốn, ta giữ thời gian bằng phân số, vì một phần ba mươi giây không viết gọn được thành số thập phân hữu hạn. Năm nhân một phần ba mươi bằng năm phần ba mươi, rút gọn còn một phần sáu.""",
           focus=[1, 2], clear=True),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 11) == 10", "5 * Fraction(1, 30) == Fraction(5, 30) == Fraction(1, 6)"])

    sym = sc("sym", "symbol", "Giải mã các từ của bài", [
        st(table(["từ", "nghĩa"],
                 [["ngữ cảnh giới hạn <i>(bounded context)</i>", "vùng mà mỗi từ có đúng một nghĩa; DDD (thiết kế hướng miền) chia mô hình lớn thành nhiều vùng như vậy (Evans, <i>Domain-Driven Design</i>, 2003)"],
                  ["ngôn ngữ chung <i>(ubiquitous language)</i>", "người nghiệp vụ và lập trình viên dùng cùng một bộ từ, và chính các từ đó có trong mã"],
                  ["cụm đối tượng <i>(aggregate)</i>, gốc <i>(root)</i>", "nhóm đối tượng (đối tượng: một thứ trong mã gồm dữ liệu và việc nó làm được, như Tài khoản có số dư và việc ghi nợ) được coi là một khối; bên ngoài chỉ chạm vào gốc; một <b>giao dịch</b> (nhiều thao tác cùng thành hoặc cùng huỷ) không vượt ranh giới cụm"],
                  ["bất biến", "điều luôn đúng sau mọi thao tác, ví dụ số dư không âm"]]),
           """Bảng này giải mã bốn từ của thiết kế hướng miền. Ngữ cảnh giới hạn là vùng mà mỗi từ có đúng một nghĩa, và ngôn ngữ chung là bộ từ cả nghiệp vụ lẫn lập trình viên cùng dùng. Cụm đối tượng là nhóm các thứ trong mã coi như một khối, bên ngoài chỉ chạm vào gốc, còn bất biến là điều luôn đúng sau mọi thao tác.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], introduces=["bnx_ngon_ngu_chung"]),
        st(table(["từ", "nghĩa"],
                 [["cổng API <i>(API gateway)</i>", "cửa vào duy nhất cho mọi người gọi từ bên ngoài, đứng trước các dịch vụ; <b>xác thực</b> là kiểm người gọi là ai, <b>định tuyến</b> là chuyển yêu cầu tới đúng dịch vụ theo đường dẫn"],
                  ["thùng token <i>(token bucket)</i>", "thùng chứa tối đa $b$ thẻ, mỗi giây thêm $r$ thẻ; mỗi yêu cầu lấy 1 thẻ, hết thẻ thì từ chối"],
                  ["mã tương quan <i>(correlation ID)</i>", "một mã gắn vào yêu cầu ở cổng và chuyển qua mọi dịch vụ, để lần theo một yêu cầu trong nhật ký"],
                  ["Open API, bên thứ ba", "API ngân hàng cung cấp cho tổ chức khác có hợp đồng với ngân hàng"]]),
           """Bảng thứ hai là từ của cửa vào. Cổng API kiểm người gọi là ai rồi chuyển yêu cầu tới đúng dịch vụ. Thùng chứa tối đa b thẻ, mỗi giây thêm r thẻ, mỗi yêu cầu lấy một thẻ và hết thẻ thì bị từ chối. Mã tương quan giúp lần theo một yêu cầu trong nhật ký.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True, introduces=["bnx_thung_token"]),
    ])

    intu = sc("intuition", "intuition", "Hình dung: ranh giới, cửa vào và luồng đồng ý", [
        st(svg(1500, 460,
               panel(20, 20, 470, 340, "Tài khoản", C_BLUE),
               box(45, 90, 420, 110, ["khách hàng =", "chủ tài khoản"], C_GRAY, size=24),
               box(45, 225, 420, 110, ["cụm đối tượng Tài khoản:", "số dư không âm"], C_GREEN, size=24),
               panel(515, 20, 470, 340, "Thanh toán", C_AMBER),
               box(540, 90, 420, 110, ["khách hàng =", "người ra lệnh chuyển"], C_GRAY, size=24),
               box(540, 225, 420, 110, ["hạn mức =", "100 triệu đồng/ngày"], C_AMBER, size=24),
               panel(1010, 20, 470, 340, "Tín dụng", C_PURPLE),
               box(1035, 90, 420, 110, ["khách hàng =", "người vay được chấm điểm"], C_GRAY, size=24),
               box(1035, 225, 420, 110, ["hạn mức =", "50 triệu đồng được duyệt"], C_PURPLE, size=24),
               txt(750, 405, "cùng chữ, khác nghĩa: mỗi ngữ cảnh một mô hình, gọi nhau qua API", 26, "middle", "#1f2937", True),
               txt(750, 445, "(hạn mức là số minh hoạ)", 22, "middle", "#6b7280")),
           """Hình đầu chia ngân hàng thành ba ngữ cảnh. Ở Tài khoản, khách hàng là chủ tài khoản và số dư không âm.
           Ở Thanh toán, khách hàng là người ra lệnh chuyển và hạn mức là một trăm triệu mỗi ngày. Còn ở Tín dụng, khách hàng là người vay, hạn mức năm mươi triệu, đều là số minh hoạ. Cùng chữ mà khác nghĩa, nên mỗi ngữ cảnh giữ mô hình riêng."""),
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
           """Hình thứ hai là cửa vào: mọi yêu cầu đi qua cổng API trước. Cổng xác thực mã truy cập, giới hạn năm yêu cầu mỗi giây, định tuyến và ghi nhật ký.
           Yêu cầu quá giới hạn bị trả mã bốn trăm hai mươi chín ngay ở cổng, nhưng mỗi dịch vụ vẫn tự kiểm phạm vi quyền, vì cổng không biết luật nghiệp vụ."""),
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
           """Hình thứ ba là luồng API mở theo Thông tư sáu mươi tư, có hiệu lực từ một tháng ba năm hai nghìn không trăm hai mươi lăm.
           Khách đồng ý rõ ràng, bên thứ ba có hợp đồng mới được gọi, ngân hàng chỉ trả đúng phạm vi đã đồng ý, và khách có thể rút lại."""),
        st(table(["điều thông tư ghi", "nội dung"],
                 [["Open API", "tập hợp các API ngân hàng cung cấp cho bên thứ ba trực tiếp kết nối, xử lý dữ liệu"],
                  ["Điều 8", "ngân hàng phải ký hợp đồng với bên thứ ba về triển khai Open API; cam kết dùng dữ liệu đúng phạm vi, mục đích"],
                  ["Điều 11", "khách tra cứu được dữ liệu đã đồng ý cho bên thứ ba xử lý, rút lại được sự đồng ý; thời hạn truy vấn sau khi khách đồng ý không quá 180 ngày; <i>vế “trừ khi khách và ngân hàng thoả thuận khác” theo bản dịch tiếng Anh, cần kiểm lại</i>"],
                  ["Điều 5, Điều 15 <i>(theo bản dịch tiếng Anh, cần kiểm lại)</i>", "API khởi tạo thanh toán, nạp, rút ví chỉ cấp cho bên thứ ba là ngân hàng hoặc tổ chức trung gian thanh toán; ngân hàng đã kết nối trực tiếp từ trước có lộ trình chuyển tiếp tới 01/3/2027"],
                  ["nguồn", "Tạp chí Ngân hàng 24/02/2025; trang NHNN 14/11/2025 (trích Thông tư 64/2024/TT-NHNN)"]]),
           """Bảng này ghi điều thông tư nói, theo hai bài báo dẫn lại, nên khi làm việc thật hãy đọc nguyên văn. Điều tám buộc ngân hàng ký hợp đồng với bên thứ ba cam kết dùng dữ liệu đúng phạm vi. Điều mười một cho khách tra cứu và rút lại sự đồng ý, thời hạn truy vấn không quá một trăm tám mươi ngày, vế thoả thuận khác cần kiểm lại. Điều năm và mười lăm cũng cần kiểm lại.""",
           focus=[["1.2", "1.6"], "1.3", "1.4", "1.5"], clear=True),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: ranh giới, bất biến, rồi thùng token", [
        st("""<p><b>Bước 1.</b> Vì “hạn mức” ở Thanh toán và ở Tín dụng theo hai luật khác nhau, nên mỗi nghĩa nằm trong ngữ cảnh của nó, không dùng chung một cột.</p>
<span class='note'>Làm thử (số minh hoạ, đơn vị triệu đồng): hôm nay đã chuyển 80, chuyển thêm 30; hạn mức vay 50 không liên quan.</span>
$$80 + 30 = 110 > 100 \\;\\to\\; \\text{Thanh toán từ chối}$$""",
           """Bước một, vì chữ hạn mức ở Thanh toán và Tín dụng theo hai luật khác nhau, nên mỗi nghĩa nằm trong ngữ cảnh của nó.
           Làm thử: đã chuyển tám mươi triệu, chuyển thêm ba mươi triệu thì một trăm mười vượt một trăm nên Thanh toán từ chối, còn hạn mức vay không liên quan.""",
           focus=[1, [2, 3]]),
        st("""<p><b>Bước 2.</b> Mọi thay đổi số dư đi qua <b>gốc</b> cụm đối tượng Tài khoản, nên bất biến “số dư không âm” chỉ phải kiểm ở <b>một</b> chỗ.</p>
<span class='note'>Làm thử: số dư $300\\,000$, ghi nợ $500\\,000$ → từ chối, giữ $300\\,000$; ghi nợ $200\\,000$ → $300\\,000 - 200\\,000 = 100\\,000$.</span>""",
           """Bước hai, mọi thay đổi số dư đi qua gốc của cụm Tài khoản, nên bất biến số dư không âm chỉ phải kiểm ở một chỗ.
           Làm thử: số dư ba trăm nghìn, ghi nợ năm trăm nghìn thì bị từ chối và giữ ba trăm nghìn. Ghi nợ hai trăm nghìn thì được, còn một trăm nghìn.""",
           focus=[1, 2, 2], clear=True),
        st("""<p><b>Bước 3.</b> Ở cổng, mỗi yêu cầu cần $1$ thẻ. Thùng thêm $r = 5$ thẻ mỗi giây và chứa tối đa $b = 10$: sức chứa cho dồn ngắn, tốc độ giữ trung bình.</p>
<span class='note'>Làm thử: sau $\\frac{1}{30}$ giây thùng thêm $5 \\cdot \\frac{1}{30} = \\frac{1}{6}$ thẻ.</span>""",
           """Bước ba, mỗi yêu cầu ở cổng cần một thẻ. Thùng thêm năm thẻ mỗi giây và chứa tối đa mười, vì sức chứa cho phép dồn ngắn hạn còn tốc độ giữ mức trung bình.
           Làm thử: sau một phần ba mươi giây thùng thêm một phần sáu thẻ.""",
           focus=[1, 1, 2], clear=True),
        st("""<p><b>Bước 4.</b> Trước mỗi yêu cầu: số thẻ $=$ thẻ còn $+ \\, r \\cdot$ thời gian đã trôi, nhưng không quá $b$. Có ít nhất $1$ thẻ thì nhận và trừ $1$.</p>
<span class='note'>Làm thử: còn $9$ thẻ, sau $\\frac{1}{30}$ giây: $9 + \\frac{1}{6} = \\frac{55}{6}$, vẫn dưới $10$ nên giữ nguyên.</span>""",
           """Bước bốn, trước mỗi yêu cầu số thẻ bằng thẻ còn cộng tốc độ nhân thời gian trôi, nhưng không quá sức chứa vì thùng đầy thì thẻ bị tràn. Có ít nhất một thẻ thì nhận và trừ một thẻ.
           Làm thử: còn chín thẻ, sau một phần ba mươi giây được năm mươi lăm phần sáu, vẫn dưới mười nên giữ nguyên.""",
           focus=[1, 1, 2], clear=True),
    ], checks=["80 + 30 == 110 > 100", "alg.bnx_l14_debit(300000, 500000) == (300000, False)", "alg.bnx_l14_debit(300000, 200000) == (100000, True)",
               "5 * Fraction(1, 30) == Fraction(1, 6)", "alg.bnx_l14_bucket_trace(5, 10, " + SPREAD + ")[1][1] == 9 + Fraction(1, 6) == Fraction(55, 6)"])

    ex = sc("example", "example", "Ví dụ: 30 yêu cầu qua cổng, từng phép tính", [
        st("""<p>Cổng $r = 5$ thẻ/giây, $b = 10$. Thùng bắt đầu <b>đầy</b> $10$ thẻ. Trường hợp A: $30$ yêu cầu đến <b>cùng lúc</b>, thời gian trôi bằng $0$ nên không thêm thẻ.</p>
$$① \\; \\text{nhận} = \\hl{10}$$""",
           """Cổng có năm thẻ mỗi giây và sức chứa mười, thùng bắt đầu đầy. Ba mươi yêu cầu đến cùng lúc nên không thêm thẻ nào, mười thẻ đầu cho mười yêu cầu, vậy nhận mười.""",
           focus=[1, 2], clear=True),
        st("""$$② \\; 30 - 10 = \\hl{20}\\ \\text{bị từ chối (429)}$$""",
           """Phép tính thứ hai, dùng lại số mười: ba mươi trừ mười bằng hai mươi yêu cầu bị từ chối với mã bốn trăm hai mươi chín.""", clear=True),
        st("""<p>Trường hợp B: $30$ yêu cầu <b>rải đều</b> trong $1$ giây, ở thời điểm $0, \\frac{1}{30}, \\frac{2}{30}, \\dots, \\frac{29}{30}$.</p>
$$③ \\; 1 - \\frac{1}{6} = \\hl{\\frac{5}{6}}\\ \\text{thẻ mất đi sau mỗi yêu cầu được nhận}$$""",
           """Trường hợp rải đều: ba mươi yêu cầu ở các thời điểm không, một phần ba mươi, cứ thế tới hai mươi chín phần ba mươi giây. Giữa hai yêu cầu chỉ thêm một phần sáu thẻ, nên mỗi lần nhận thùng mất năm phần sáu thẻ.""",
           introduces=["dots"], focus=[1, 2], clear=True),
        st("""<p>Dùng lại $\\frac{5}{6}$: trước yêu cầu thứ $11$ (thời điểm $\\frac{10}{30}$) đã nhận $10$ yêu cầu.</p>
$$④ \\; 10 - 10 \\cdot \\frac{5}{6} = \\hl{\\frac{5}{3}} \\geq 1 \\ \\text{nên nhận đủ } 11 \\text{ yêu cầu đầu}$$""",
           """Dùng lại năm phần sáu: trước yêu cầu thứ mười một, thùng còn mười trừ mười nhân năm phần sáu, bằng năm phần ba, lớn hơn hoặc bằng một, nên nhận.""",
           introduces=["geq"], clear=True),
        st("""<p>Sau yêu cầu thứ 11, thùng còn 2/3 thẻ. Mỗi khoảng thêm 1/6 thẻ, nên thêm 2 khoảng là đủ 1 thẻ: nhận ở 12/30 giây.</p>
<p>Sau đó thùng về 0, cứ 6 khoảng (1/5 giây) mới đủ 1 thẻ: nhận ở 18/30 và 24/30 giây.</p>
$$⑤ \\; 11 + 3 = \\hlg{14}\\ \\text{nhận}, \\quad 30 - 14 = 16\\ \\text{từ chối}$$""",
           """Sau yêu cầu thứ mười một, thùng còn hai phần ba thẻ, thêm hai khoảng là đủ một thẻ nên nhận ở mười hai phần ba mươi giây. Sau đó thùng về không, cứ sáu khoảng mới đủ một thẻ, nên nhận thêm ở mười tám và hai mươi tư phần ba mươi: mười bốn nhận, mười sáu từ chối.""",
           focus=[[1, 2], 3], clear=True),
        jstep([("pimp", "<code>from fractions import Fraction as F</code>: lấy loại phân số về dùng với tên ngắn <code>F</code>; <code>F(1, 30)</code> là phân số 1/30, giữ đúng không làm tròn", ""),
               ("pdef", "<code>def cong(rate, cap, times):</code> … <code>return ok</code>: hàm tên cong nhận ba tham số, rồi trả kết quả ok về", ""),
               ("pfor", "<code>for t in times:</code>: lần lượt qua từng thời điểm t của danh sách times", "")]),
        jstep([(("<code>[F(0)] * 30</code>, <code>[F(i, 30) for i in range(30)]</code>", "danh sách 30 phần tử đều là 0; danh sách dựng bằng vòng lặp: với i từ 0 tới 29, lấy <code>F(i, 30)</code>", "Nhân danh sách với một số lặp phần tử chừng ấy lần, và danh sách dựng bằng vòng lặp lấy một giá trị cho mỗi i từ không tới hai mươi chín."), "30 yêu cầu cùng lúc; 30 yêu cầu rải đều", ""),
               (("<code>min(a, b)</code>; <code>a, b = x, y</code>; <code>if tok &gt;= 1:</code>", "số nhỏ hơn; gán hai biến cùng lúc; làm tiếp khi còn ít nhất 1 thẻ", "Hàm nhỏ hơn chọn số bé hơn, câu gán hai biến cùng lúc gán theo thứ tự, và điều kiện hỏi còn ít nhất một thẻ không."), "<code>min(F(cap), tok + …)</code>: không vượt sức chứa", ""),
               ("pprint", "<code>print(cong(5, 10, […]))</code>: in số yêu cầu nhận; <code># cùng lúc</code>: ghi chú cho người đọc", "")], clear=True),
        st(BUCKET.show(title="Mô phỏng cổng bằng Python, dùng phân số"),
           """Giờ ta cho Python tính lại. Hàm cổng bắt đầu với thùng đầy, mỗi lần cộng thẻ theo thời gian trôi nhưng không quá sức chứa, và còn ít nhất một thẻ thì nhận một yêu cầu.""",
           focus=[["2.1", "2.3", "2.5"], ["2.7", "2.8"]], clear=True),
        st("<p>Bằng tay: cùng lúc nhận $10$ (phép ①), rải đều nhận $14$ (phép ⑤).</p>" + BUCKET.out_html(),
           """Bằng tay ta tính cùng lúc nhận mười và rải đều nhận mười bốn, và kết quả chạy thật in ra mười rồi mười bốn, khớp cả hai.""", clear=True),
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
           """Kiểm bằng đường khác: trong thời gian T cổng phát ra nhiều nhất sức chứa cộng tốc độ nhân T thẻ, nên số yêu cầu nhận không vượt quá số đó.
           Cùng lúc thì T bằng không, cận trên là mười. Rải đều thì T là hai mươi chín phần ba mươi giây, cận trên xấp xỉ mười bốn phẩy tám, nên nhiều nhất mười bốn, khớp cả hai.""",
           focus=[1, 2, 2]),
        st(table(["kiểm", "cách tính khác", "kết quả"],
                 [["số yêu cầu nhận ở B", "đếm thời điểm: 0 tới 10/30 là 11, thêm 12/30, 18/30, 24/30", "11 + 3 = 14"],
                  ["ngày ban hành tới ngày hiệu lực", "1 ngày cuối tháng 12, 31 ngày tháng 1, 28 ngày tháng 2", "1 + 31 + 28 = 60 ngày"]]),
           """Bảng này kiểm thêm bằng cách đếm. Ở trường hợp rải đều, từ không tới mười phần ba mươi là mười một lần nhận, thêm ba lần sau, tổng mười bốn, nên khớp.
           Từ ngày ban hành tới ngày hiệu lực là một cộng ba mươi mốt cộng hai mươi tám, tổng sáu mươi ngày.""",
           focus=[0, "1.2", "1.3"], clear=True),
    ], checks=["alg.bnx_l14_bound(5, 10, 0) == alg.bnx_l14_bucket(5, 10, [0] * 30) == 10",
               "10 + 5 * Fraction(29, 30) == Fraction(89, 6)", "round(float(Fraction(89, 6)), 1) == 14.8",
               "alg.bnx_l14_bound(5, 10, Fraction(29, 30)) == alg.bnx_l14_bucket(5, 10, " + SPREAD + ") == 14",
               "len(alg.bnx_l14_accepted_idx(5, 10, " + SPREAD + ")) == 11 + 3",
               "alg.bnx_l14_days('31/12/2024', '01/03/2025') == 1 + 31 + 28 == 60"])

    quymo = sc("quymo", "example", "Khi nhiều bên cùng gọi: giới hạn theo từng bên có đủ không", [
        st(QUYMO.show(lines=(1, 9), title="Hàm cổng dùng lại, viết đủ để gõ được: thùng riêng cho mỗi bên"),
           """Bài toán thật có nhiều bên thứ ba cùng gọi, nên ta xem tải đổi thế nào khi số bên tăng. Ta viết lại đủ hàm cổng để gõ được, vì mỗi bên có một thùng riêng.""",
           focus=[2, ["2.3", "2.5"]], clear=True),
        st(QUYMO.show(lines=(11, 16)) + note("<code>sum(… for _ in range(n))</code> cộng kết quả của n lần gọi, mỗi lần ứng với một bên; <code>10_000</code> là mười nghìn; <code>print(a, b)</code> in các giá trị cách nhau dấu cách.") + QUYMO.out_html(title="Kết quả chạy thật: số bên, nhận khi cùng lúc, nhận khi rải đều, từ chối khi cùng lúc"),
           """Mỗi bên gửi ba mươi yêu cầu, một lần cùng lúc và một lần rải đều. Với một, một trăm và mười nghìn bên, lệnh cộng gọn cộng số yêu cầu nhận của từng bên. Lệnh in cho ra các giá trị cách nhau dấu cách, thêm số bị từ chối.""",
           focus=[1, ["4.1", "4.2", "4.3"]], clear=True),
        st(table(["số bên N", "nhận khi cùng lúc", "từ chối", "nhận khi rải đều", "xử lý hết nếu phía sau chịu 2 000 yêu cầu/giây (số minh hoạ)", "tải duy trì N × 5 mỗi giây"],
                 [[nowrap("1 (×1)"), "10", "20", "14", "5 ms (phần nghìn giây)", "5"],
                  [nowrap("100 (×100)"), "1 000", "2 000", "1 400", "0,5 giây", "500"],
                  [nowrap("10 000 (×10 000)"), "100 000", "200 000", "140 000", "50 giây", "50 000, vượt 2 000"]]),
           """Bảng này cho thấy giải pháp cũ gãy ở đâu. Giới hạn theo từng bên giữ mỗi bên ở mười yêu cầu dồn, nhưng với mười nghìn bên cổng vẫn cho một trăm nghìn yêu cầu qua cùng lúc.
           Nếu phía sau chỉ chịu hai nghìn yêu cầu mỗi giây thì xử lý hết mất năm mươi giây, và tải duy trì năm mươi nghìn mỗi giây vượt xa.""",
           focus=[0, "1.4", "1.4"], clear=True),
        st(table(["cách", "được", "mất"],
                 [["giới hạn riêng từng bên", "công bằng; một bên gửi dồn không làm nghẽn bên khác", "tổng tải tăng theo số bên (N × 5/giây), không bảo vệ phía sau khi có 10 000 bên"],
                  ["thêm giới hạn toàn cục", "chặn trần tổng tải vào phía sau", "một bên ồn ào làm các bên khác bị từ chối; phải chia phần"],
                  ["co giãn phía sau (thêm máy)", "chịu được tải cao hơn", "tốn tiền, thêm độ phức tạp; vẫn cần giới hạn để chống bị dồn bất ngờ"]]),
           """Bảng thứ hai là đánh đổi phải chọn. Giới hạn riêng từng bên công bằng, nhưng tổng tải tăng theo số bên.
           Thêm giới hạn toàn cục chặn trần tổng, đổi lại một bên ồn ào làm bên khác bị từ chối. Co giãn phía sau chịu tải cao hơn, đổi lại tốn tiền hơn.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l14_bucket(5, 10, [0] * 30) * n for n in (1, 100, 10_000)] == [10, 1000, 100_000]",
               "[30 * n - alg.bnx_l14_bucket(5, 10, [0] * 30) * n for n in (1, 100, 10_000)] == [20, 2000, 200_000]",
               "[alg.bnx_l14_bucket(5, 10, " + SPREAD + ") * n for n in (1, 100, 10_000)] == [14, 1400, 140_000]",
               "[alg.bnx_l14_drain_s(alg.bnx_l14_bucket(5, 10, [0] * 30) * n, 2000) for n in (1, 100, 10_000)] == [0.005, 0.5, 50.0]",
               "[alg.bnx_l14_sustained(n, 5) for n in (1, 100, 10_000)] == [5, 500, 50_000] and 50_000 > 2000 > 500",
               "100 // 1 == 10_000 // 100 == 100"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng DDD <b class="red">bắt buộc</b> tách thành nhiều microservice (dịch vụ nhỏ chạy riêng, gọi nhau qua mạng). DDD vẽ ranh giới trước; ranh giới đó có thể là <b>mô-đun</b> (khối mã có ranh giới rõ) <b>trong một ứng dụng</b>, cách triển khai tính sau.</div>""",
           """Lỗi của người mới là tưởng thiết kế hướng miền bắt buộc tách thành nhiều dịch vụ nhỏ chạy riêng. Thiết kế hướng miền vẽ ranh giới trước, ranh giới đó có thể chỉ là các mô-đun, tức khối mã tách bạch, trong một ứng dụng."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Cổng đã kiểm mã nên dịch vụ <b class="red">bỏ kiểm quyền</b>. Nếu cổng không được cấu hình kiểm phạm vi, mã <code>accounts:read</code> hợp lệ vẫn qua cổng; khi đó nếu dịch vụ Thanh toán không tự kiểm phạm vi <code>payments:write</code>, lệnh chuyển tiền sẽ chạy.
<br><span class="note">Phép thử bắt lỗi: gọi thẳng dịch vụ bằng mã sai phạm vi, phải nhận 403.</span></div>""",
           """Lỗi của người đã đi làm là nghĩ cổng đã kiểm mã nên dịch vụ bỏ kiểm quyền. Nếu cổng không kiểm phạm vi, mã chỉ có quyền đọc vẫn qua cổng, và dịch vụ Thanh toán không tự kiểm thì lệnh chuyển tiền sẽ chạy.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bên thứ ba đã có thông tin kết nối là <b class="red">trả mọi dữ liệu</b>. Theo Thông tư 64, cần hợp đồng với bên thứ ba <b>và</b> sự đồng ý của khách, chỉ trả đúng phạm vi đã đồng ý; khách rút lại thì dừng.
<br><span class="note">Phép thử bắt lỗi: khách rút lại sự đồng ý, lần gọi kế tiếp phải bị từ chối.</span></div>""",
           """Lỗi thứ ba cũng của người đã đi làm là thấy bên thứ ba có thông tin kết nối thì trả mọi dữ liệu. Theo Thông tư sáu mươi tư cần hợp đồng và sự đồng ý của khách, chỉ trả đúng phạm vi, và khách rút lại thì phải dừng.""", clear=True),
    ])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Cổng 5 thẻ/giây, sức chứa 10. 40 yêu cầu đến cùng lúc: nhận bao nhiêu, từ chối bao nhiêu?"],
                  ["2", "Cổng 2 thẻ/giây, sức chứa 3. 6 yêu cầu cách nhau 1/4 giây (0, 1/4, …, 5/4): nhận bao nhiêu?"],
                  ["3", "Quyết định: đội 5 người, một cơ sở dữ liệu Oracle (phần mềm cơ sở dữ liệu của hãng Oracle). Tách Tài khoản và Thanh toán thành hai dịch vụ ngay, hay một ứng dụng có hai mô-đun ranh giới rõ?"]]),
           """Đến lượt bạn, ta có ba câu. Câu một: cổng năm thẻ mỗi giây, sức chứa mười, bốn mươi yêu cầu cùng lúc thì nhận bao nhiêu?
           Câu hai: cổng hai thẻ mỗi giây, sức chứa ba, sáu yêu cầu cách nhau một phần tư giây thì nhận bao nhiêu? Câu ba: đội năm người dùng một cơ sở dữ liệu Oracle, nên tách thành hai dịch vụ ngay hay giữ một ứng dụng hai mô-đun? Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: cùng lúc nên không thêm thẻ, chỉ có $10$ thẻ ban đầu.</p>
$$\\text{nhận } \\hl{10}, \\quad 40 - 10 = \\hl{30}\\ \\text{từ chối}$$""",
           """Đáp án câu một: các yêu cầu đến cùng lúc nên chỉ có mười thẻ ban đầu, nhận mười và từ chối ba mươi."""),
        st("""<p>Câu 2: mỗi khoảng thêm $2 \\cdot \\frac{1}{4} = \\frac{1}{2}$ thẻ, mỗi lần nhận mất $1 - \\frac{1}{2} = \\frac{1}{2}$. Trước yêu cầu thứ $5$: $3 - 4 \\cdot \\frac{1}{2} = 1$ nên nhận; yêu cầu thứ $6$ chỉ có $\\frac{1}{2}$ thẻ.</p>
$$\\text{nhận } \\hlg{5}, \\quad \\text{cận trên } 3 + 2 \\cdot \\frac{5}{4} = 5{,}5$$""",
           """Đáp án câu hai: mỗi lần nhận thùng mất nửa thẻ. Trước yêu cầu thứ năm còn ba trừ bốn nhân một nửa bằng một thẻ nên nhận, yêu cầu thứ sáu chỉ có nửa thẻ nên từ chối.
           Vậy nhận năm, khớp với cận trên năm phẩy năm.""",
           focus=[1, 1, 2], clear=True),
        st(table(["lựa chọn", "được", "mất", "đổi khi"],
                 [["một ứng dụng, hai mô-đun", "chuyển tiền và ghi sổ trong một giao dịch, một lần chốt; triển khai một lần", "phải giữ kỷ luật: mô-đun này không đọc bảng của mô-đun kia", "hai phần cần nhịp phát hành hoặc mức tải khác hẳn nhau (đo được)"],
                  ["hai dịch vụ riêng", "triển khai, co giãn độc lập", "giao dịch vượt hai dịch vụ phải dùng SAGA (chuỗi bước, mỗi bước có bước huỷ bù lại nếu bước sau hỏng) và Outbox (ghi tin cần gửi ngay trong giao dịch rồi mới gửi đi, nên không mất tin); thêm lời gọi mạng, thêm chỗ hỏng", "đội nhỏ, chưa đo thấy nghẽn: chưa cần"]]),
           """Đáp án câu ba là một đánh đổi: hai mô-đun giữ chuyển tiền và ghi sổ trong một giao dịch, đổi lại phải giữ kỷ luật. Hai dịch vụ riêng triển khai độc lập, nhưng giao dịch vượt cả hai cần chuỗi bước bù trừ. Với đội năm người chưa đo thấy nghẽn, hai mô-đun là đủ.""",
           focus=["1.2", "1.3", "1.2"], clear=True, introduces=["bnx_saga_outbox"]),
    ], checks=["alg.bnx_l14_bucket(5, 10, [0] * 40) == 10", "40 - alg.bnx_l14_bucket(5, 10, [0] * 40) == 30",
               "2 * Fraction(1, 4) == Fraction(1, 2) == 1 - Fraction(1, 2)",
               "alg.bnx_l14_bucket_trace(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2)))[4][1] == 3 - 4 * Fraction(1, 2) == 1",
               "alg.bnx_l14_bucket_trace(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2)))[5][1] == Fraction(1, 2)",
               "alg.bnx_l14_bucket(2, 3, alg.bnx_l14_spread(6, Fraction(3, 2))) == 5 == alg.bnx_l14_bound(2, 3, Fraction(5, 4))",
               "3 + 2 * Fraction(5, 4) == Fraction(11, 2)"])

    lab_pr = practice_scene(sc, "Tự làm: thùng token và nhiều bên cùng gọi", practice_steps(
        st, "BNX", "L14",
        """<p><b>Đề</b>: cổng cho mỗi bên <code>rate = 4</code>, <code>cap = 6</code>. Viết <code>mau.py</code> với hàm <code>nhan(rate, cap, times)</code> dùng <code>Fraction</code>, rồi in:</p>
<ol><li>20 yêu cầu <b>cùng lúc</b>: nhận / từ chối</li><li>20 yêu cầu <b>rải đều</b> cách nhau 1/10 giây: nhận, và cận trên <code>cap + rate × T</code></li>
<li><b>50 bên</b> giống nhau, mỗi bên gửi dồn <b>20 yêu cầu</b> cùng lúc: tổng nhận / từ chối</li><li>hậu phương (các dịch vụ phía sau cổng) chịu 120 yêu cầu/giây: <b>bao nhiêu giây</b> để xử lý hết số đã qua cổng</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; đầu ra viết không dấu.</p>""",
        """Bây giờ tới phần bạn tự làm: cổng cho mỗi bên bốn thẻ mỗi giây, sức chứa sáu. Viết hàm tính số yêu cầu nhận được cho hai mươi yêu cầu cùng lúc và rải đều, kèm cận trên. Rồi cho năm mươi bên gửi dồn, tính phía sau cổng chịu một trăm hai mươi yêu cầu mỗi giây cần bao nhiêu giây.""",
        EXPECT_LAB, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> dùng lại ý của hàm trong bài: thùng đầy lúc đầu, mỗi lần cộng <code>(t − last) × rate</code> nhưng không quá <code>cap</code>, còn ít nhất 1 thẻ thì nhận. Cận trên là <code>int(cap + rate × T)</code>. Tải của 50 bên là 50 lần số của một bên.
Lời giải ở <code>labs/BNX/L14/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hãy dùng lại ý của hàm trong bài: thùng đầy lúc đầu, mỗi lần cộng thẻ theo thời gian trôi nhưng không quá sức chứa. Lời giải chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L14")
    lab_pr["checks"] = ["alg.bnx_l14_bucket(4, 6, [0] * 20) == 6 and 20 - alg.bnx_l14_bucket(4, 6, [0] * 20) == 14",
                        "alg.bnx_l14_bucket(4, 6, alg.bnx_l14_spread(20, 2)) == 13 == alg.bnx_l14_bound(4, 6, Fraction(19, 10))",
                        "50 * alg.bnx_l14_bucket(4, 6, [0] * 20) == 300 and 50 * 20 - 300 == 700",
                        "alg.bnx_l14_drain_s(300, 120) == 2.5"]

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("một chữ, nhiều nghĩa", "ngữ cảnh giới hạn", "gốc cụm đối tượng giữ bất biến", "cổng: xác thực, giới hạn, định tuyến, nhật ký",
                 "dịch vụ vẫn kiểm quyền", "Open API: hợp đồng + đồng ý", "quy mô: cần giới hạn tổng"),
           """Tổng kết: một chữ nhiều nghĩa nên ta chia ngữ cảnh giới hạn, và gốc của cụm đối tượng giữ bất biến. Cổng lo xác thực, giới hạn, định tuyến, nhật ký nhưng dịch vụ vẫn tự kiểm quyền, và nhiều bên cùng gọi cần giới hạn tổng.""",
           focus=[["1.1", "1.3", "1.5"], ["1.7", "1.9", "1.11", "1.13"]]),
        st("""<div class='box key'><b>Tư duy:</b> vẽ ranh giới theo <b>nghĩa của từ</b> trước khi chọn công nghệ; mỗi lớp bảo vệ (cổng, dịch vụ, cơ sở dữ liệu) tự kiểm phần của nó, không lớp nào tin lớp trước đã kiểm hộ; và đo tải ở nhiều bên chứ đừng suy từ một bên.</div>""",
           """Điều cần mang theo: hãy vẽ ranh giới theo nghĩa của từ trước khi chọn công nghệ, mỗi lớp bảo vệ tự kiểm phần của nó, và đo tải ở nhiều bên chứ đừng suy từ một bên."""),
        st("""<p class='note'>Bài sau (bài tổng hợp): ghép mọi mảnh đã học thành một dự án mẫu API chuyển khoản đúng như tin tuyển dụng đòi hỏi.</p>""",
           """Ở bài sau, bài tổng hợp, ta ghép mọi mảnh đã học thành một dự án mẫu API chuyển khoản.""",
           forward_ref=True),
    ])
    scenes = spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L14", "ddd_cong_api_open_api", "Bài 14 — DDD, cổng API và Open API ngân hàng: ranh giới, cửa vào và chia sẻ dữ liệu có đồng ý",
                  "curriculum/bnx.yaml L14; audit/bnx/verify_bnx.py L14; Evans, Domain-Driven Design (2003), qua M. Fowler, bliki BoundedContext (15/01/2014), "
                  "DDD_Aggregate (23/04/2013), DomainDrivenDesign (22/04/2020); C. Richardson, microservices.io Pattern: API Gateway; AWS API Gateway Developer Guide "
                  "“Throttle requests” (thùng token, 429); Thông tư 64/2024/TT-NHNN (31/12/2024, hiệu lực 01/3/2025; audit/legal/registry.yaml: HIEU_LUC) qua Tạp chí Ngân hàng (24/02/2025) và sbv.gov.vn (14/11/2025) "
                  "[TT64] [TT64b] [DDD] [AGW] — đọc 2026-11-11; Điều 5, Điều 11 khoản 6 (180 ngày, trừ khi thoả thuận), Điều 15 (lộ trình chuyển tiếp tới 01/3/2027): theo bản dịch tiếng Anh luatvietnam (người đọc độc lập 2026-11-14), cần đối chiếu lại bản gốc tiếng Việt; giới hạn 5/giây, sức chứa 10, hạn mức 100/50 triệu, hậu phương 2 000 yêu cầu/giây là số minh hoạ; số yêu cầu qua cổng đo thật bằng Python (prog Quymo)",
                  ["Nêu cách chia hệ thống ngân hàng thành ngữ cảnh giới hạn", "Nhận ra một khái niệm mang nghĩa khác nhau ở hai ngữ cảnh",
                   "Nêu việc cổng API làm: xác thực, giới hạn tốc độ, định tuyến, nhật ký", "Nêu nội dung Open API ngân hàng theo Thông tư 64/2024/TT-NHNN: hợp đồng, sự đồng ý của khách, thời hạn tra cứu",
                   "Tính số yêu cầu một cổng thùng token nhận và từ chối khi 30 yêu cầu đến cùng lúc và khi rải đều",
                   "Đếm số yêu cầu qua cổng khi 1, 100 và 10 000 bên thứ ba cùng gọi và so với sức chịu của phía sau",
                   "Viết chương trình Python mô phỏng thùng token và tính tải khi nhiều bên cùng gọi"],
                  scenes,
                  covers=[(1, "intuition"), (2, "formula"), (3, "intuition"), (4, "intuition"), (5, "example"), (6, "quymo"), (7, "practice")])
