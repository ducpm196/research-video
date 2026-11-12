from lib import *

# Mã trên màn hình (chạy NGUYÊN VĂN / phân tích thật: audit/bnx/screen/l15.yaml, audit/bnx/ver/l15.py)
CAP_PY = """ngay = 24 * 60 * 60                 # giây trong một ngày
tb = 1_000_000 / ngay               # giao dịch/giây, trung bình
cao = 10 * tb                       # cao điểm gấp 10 (số minh hoạ)
du = 300 - (10 + 5 + 20 + 40)       # ms còn dư (số minh hoạ)
dong_thoi = 116 * 40 / 1000         # lệnh cùng lúc ở Oracle
print("giây mỗi ngày:", ngay)
print("trung bình:", round(tb, 1))
print("cao điểm:", round(cao))
print("còn dư (ms):", du)
print("cùng lúc ở Oracle:", dong_thoi)"""
CAP_OUT = """giây mỗi ngày: 86400
trung bình: 11.6
cao điểm: 116
còn dư (ms): 225
cùng lúc ở Oracle: 4.64"""

OAS_YAML = """openapi: 3.0.3
info: {title: Chuyển khoản mẫu, version: 0.1.0}
paths:
  /transfers:
    post:
      parameters:
        - {name: Idempotency-Key, in: header, required: true,
           schema: {type: string}}
      responses:
        "201": {description: Đã ghi lệnh chuyển}
        "400": {description: Yêu cầu sai lược đồ}
        "429": {description: Quá giới hạn tốc độ}"""

TPS = "alg.bnx_l15_tps(1000000)"
PEAK = "alg.bnx_l15_tps(1000000, 10)"


def _seg(x, w, col):
    return f'<rect x="{x}" y="70" width="{w}" height="80" fill="{col[0]}" stroke="{col[1]}" stroke-width="3"/>'


def build():
    hook = sc("hook", "hook", "Tình huống: hai tuần, một tin tuyển dụng, một dự án mẫu", [
        st("""<p><b>Tình huống giả định, số minh hoạ.</b> Tin tuyển dụng kỹ sư phần mềm ghi: <i>“thiết kế API backend xử lý hàng triệu giao dịch mỗi ngày”</i>, đặc tả API bằng Swagger, thủ tục lưu trữ Oracle/MS SQL, Kafka, Redis; điểm cộng Git, Docker.</p>
<div class="box key">Bạn có hai tuần để dựng dự án mẫu. Người phỏng vấn hỏi: “$1\\,000\\,000$ giao dịch mỗi ngày là bao nhiêu mỗi giây? Mỗi lệnh chuyển được bao nhiêu mili giây?”</div>""",
           """Chào bạn, đây là bài tổng hợp của phần nền, một tình huống giả định với số minh hoạ. Một tin tuyển dụng kỹ sư phần mềm ghi rằng ứng viên sẽ thiết kế API phía máy chủ xử lý hàng triệu giao dịch mỗi ngày.
           Tin đó còn đòi đặc tả API bằng Swagger, thủ tục lưu trữ trên Oracle, Kafka và Redis, cộng điểm cho Docker.
           Bạn có hai tuần để dựng một dự án mẫu. Người phỏng vấn hỏi, một triệu giao dịch mỗi ngày là bao nhiêu mỗi giây, và mỗi lệnh chuyển được bao nhiêu mili giây?"""),
        st(table(["bước", "việc", "kết quả của bài"],
                 [["1", "ước lượng tải", "trung bình ≈ 11,6 giao dịch/giây; cao điểm ≈ 116"],
                  ["2", "lập ngân sách độ trễ", "300 ms trừ các chặng còn dư 225 ms"],
                  ["3", "chọn thành phần theo yêu cầu", "mỗi thành phần trả lời một yêu cầu, kèm đánh đổi"],
                  ["4", "trình bày khi phỏng vấn", "số đo thật trên máy của bạn, nói rõ đo ở đâu"]]),
           """Bảng này là lộ trình bốn bước của bài. Một, ước lượng tải, ra trung bình khoảng mười một phẩy sáu giao dịch mỗi giây và cao điểm khoảng một trăm mười sáu.
           Hai, lập ngân sách độ trễ, ba trăm mili giây trừ các chặng còn dư hai trăm hai mươi lăm. Ba, chọn thành phần sao cho mỗi thành phần trả lời một yêu cầu, kèm đánh đổi.
           Bốn, trình bày khi phỏng vấn bằng số đo thật trên máy của bạn, và nói rõ đo ở đâu."""),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + PEAK + ") == 116",
               "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225"])

    pre = sc("prereq", "prereq", "Nhắc lại từ đầu: các mảnh ghép sẽ dùng", [
        st(table(["mảnh ghép", "nghĩa", "ví dụ số"],
                 [["khoá lũy đẳng + <code>UNIQUE</code>", "mỗi lệnh mang một khoá; cơ sở dữ liệu chỉ cho một dòng mang khoá đó", "3 lần gửi cùng khoá → 1 dòng"],
                  ["sổ cái bút toán kép", "mỗi giao dịch có dòng nợ và dòng có, tổng bằng 0", "$-200\\,000 + 200\\,000 = 0$"],
                  ["thủ tục lưu trữ, khoá theo thứ tự", "khoá hai tài khoản theo một thứ tự cố định để tránh bế tắc, lỗi thì hoàn tác", "A 300 000, B 1 000 000; chuyển 200 000: tổng vẫn 1 300 000"]]),
           """Trước hết, ta nhắc lại từ đầu các mảnh ghép sẽ dùng. Khoá lũy đẳng là mã gắn với mỗi lệnh, và ràng buộc duy nhất làm cơ sở dữ liệu chỉ cho một dòng mang khoá đó. Ba lần gửi cùng khoá chỉ còn một dòng.
           Sổ cái bút toán kép ghi mỗi giao dịch thành dòng nợ và dòng có, nên tổng bằng không, ví dụ âm hai trăm nghìn cộng hai trăm nghìn.
           Ở bài 6, thủ tục lưu trữ khoá hai tài khoản theo một thứ tự cố định để tránh bế tắc, và lỗi thì hoàn tác. Chuyển hai trăm nghìn từ A sang B, tổng hai tài khoản vẫn là một triệu ba trăm nghìn."""),
        st(table(["mảnh ghép", "nghĩa", "ví dụ"],
                 [["Outbox → Kafka", "ghi sự kiện vào bảng outbox trong cùng giao dịch ghi tiền; một tiến trình khác gửi sang Kafka", "Kafka hỏng 5 phút: sự kiện chờ trong bảng, không mất"],
                  ["Redis đệm đọc", "đọc nhanh nhưng có thể cũ; không dùng để quyết định trừ tiền", "sao kê đọc từ đệm, trừ tiền đọc từ Oracle"],
                  ["JWT, mTLS", "JWT nói người gọi là ai, được làm gì; mTLS nói máy nào đang gọi", "bài 3, bài 5"],
                  ["Docker + GitLab CI, cổng API", "đóng gói, kiểm rồi mới triển khai; cổng giới hạn tốc độ", "test hỏng thì không deploy; 5/giây, sức chứa 10"]]),
           """Bảng thứ hai là các mảnh đi ra ngoài cơ sở dữ liệu. Với Outbox, sự kiện được ghi vào một bảng trong cùng giao dịch ghi tiền, rồi một tiến trình khác gửi sang Kafka. Kafka hỏng năm phút thì sự kiện chờ trong bảng, không mất.
           Redis đệm đọc cho tốc độ nhưng có thể cũ, nên sao kê đọc từ bộ đệm, còn trừ tiền phải đọc từ Oracle.
           Ở bài 3 và bài 5, mã truy cập tự mang thông tin cho biết người gọi là ai, còn mTLS cho biết máy nào đang gọi.
           Ở bài 13, đường ống kiểm hỏng thì không triển khai. Ở bài 14, cổng API giới hạn năm yêu cầu mỗi giây, sức chứa mười.""", clear=True),
        st("""<p>Một phép tính khởi động: một ngày có bao nhiêu giây?</p>
$$24 \\cdot 60 \\cdot 60 = 86\\,400$$""",
           """Một phép tính khởi động. Một ngày có hai mươi bốn giờ, mỗi giờ sáu mươi phút, mỗi phút sáu mươi giây, nên một ngày có tám mươi sáu nghìn bốn trăm giây.""",
           clear=True),
    ], checks=["alg.bnk_unique_key_rows(3) == 1", "alg.bnk_ledger_unbalanced([(1, 'A', -200000), (1, 'B', 200000)]) == []",
               "300000 + 1000000 == (300000 - 200000) + (1000000 + 200000) == 1300000", "24 * 60 * 60 == 86400 == 1 / alg.bnx_l15_tps(1)"])

    sym = sc("sym", "symbol", "Giải mã ngôn ngữ của nghề", [
        st(table(["từ", "nghĩa", "ví dụ"],
                 [["tải trung bình (giao dịch/giây)", "số giao dịch chia đều cho mọi giây trong ngày", "$86\\,400$ giao dịch/ngày → $1$/giây"],
                  ["hệ số cao điểm", "giờ đông nhất gấp mấy lần trung bình; lấy từ nhật ký thật, ở đây là số minh hoạ", "gấp $10$"],
                  ["ngân sách độ trễ", "tổng thời gian cho phép của một lệnh, chia cho từng chặng nối tiếp", "$300$ ms (số minh hoạ)"],
                  ["phân vị 99 (p99)", "99% yêu cầu nhanh hơn số này; trung bình che mất yêu cầu chậm", "p99 = 120 ms: trong mọi lệnh đã đo, khoảng 1% chậm hơn 120 ms"],
                  ["số minh hoạ / số đo thật", "số đặt ra để dạy / số bạn đo được, có máy, công cụ, ngày đo", "“trên máy của tôi …”"]]),
           """Bảng này giải mã ngôn ngữ của nghề. Tải trung bình là số giao dịch chia đều cho mọi giây trong ngày, ví dụ tám mươi sáu nghìn bốn trăm giao dịch mỗi ngày là một giao dịch mỗi giây.
           Hệ số cao điểm cho biết giờ đông nhất gấp mấy lần trung bình. Số thật lấy từ nhật ký, còn ở đây là số minh hoạ.
           Ngân sách độ trễ là tổng thời gian cho phép của một lệnh, chia cho từng chặng nối tiếp. Phân vị chín mươi chín là mức mà chín mươi chín phần trăm yêu cầu nhanh hơn, vì trung bình che mất các yêu cầu chậm. Ví dụ phân vị chín mươi chín là một trăm hai mươi mili giây, nghĩa là trong mọi lệnh đã đo, khoảng một phần trăm chậm hơn mức đó.
           Cuối cùng, số minh hoạ là số đặt ra để dạy, còn số đo thật phải kèm máy, công cụ và ngày đo."""),
    ], checks=["alg.bnx_l15_tps(86400) == 1", "100 - 99 == 1"])

    intu = sc("intuition", "intuition", "Hình dung: dự án mẫu, ngân sách và hợp đồng API", [
        st(svg(1500, 500,
               box(20, 60, 220, 110, ["Ứng dụng", "khách hàng"], C_BLUE, bold=True),
               box(290, 60, 280, 110, ["Cổng API", "JWT, 5/giây"], C_GRAY, bold=True),
               box(620, 60, 330, 110, ["Dịch vụ chuyển khoản", "Spring Boot, OpenAPI"], C_GREEN, bold=True),
               panel(1000, 20, 480, 310, "Oracle: một giao dịch", C_AMBER, size=24),
               box(1020, 75, 440, 50, "thủ tục: khoá 2 tài khoản theo thứ tự", C_AMBER, size=20),
               box(1020, 135, 440, 50, "bảng khoá lũy đẳng UNIQUE", C_AMBER, size=20),
               box(1020, 195, 440, 50, "sổ cái bút toán kép", C_AMBER, size=20),
               box(1020, 255, 440, 50, "bảng outbox", C_AMBER, size=20),
               box(620, 230, 330, 90, ["Redis", "đệm đọc: sao kê, tra cứu"], C_RED, size=22),
               box(1000, 370, 300, 80, "bộ chuyển outbox", C_PURPLE, size=22),
               box(620, 370, 330, 80, "Kafka", C_PURPLE, bold=True),
               box(290, 370, 280, 80, ["dịch vụ", "thông báo"], C_BLUE, size=22),
               arrow(240, 115, 285, 115), arrow(570, 115, 615, 115), txt(595, 48, "mTLS", 20, "middle", "#475569"), arrow(950, 115, 995, 115),
               arrow(785, 170, 785, 225, "#dc2626", dash=True),
               arrow(1150, 330, 1150, 365, "#9333ea"), arrow(1000, 410, 955, 410, "#9333ea"), arrow(620, 410, 575, 410, "#9333ea"),
               txt(750, 490, "đóng gói bằng Docker; GitLab CI chạy kiểm rồi mới triển khai", 24, "middle", "#1f2937", True)),
           """Hình đầu là kiến trúc của dự án mẫu. Ứng dụng gọi qua cổng API, nơi kiểm mã truy cập và giới hạn năm yêu cầu mỗi giây.
           Cổng chuyển tới dịch vụ chuyển khoản viết bằng Spring Boot, có hợp đồng OpenAPI, và hai bên nói chuyện qua mTLS.
           Dịch vụ gọi một thủ tục lưu trữ trên Oracle. Trong một giao dịch, thủ tục khoá hai tài khoản theo thứ tự, ghi khoá lũy đẳng, ghi sổ cái bút toán kép và ghi bảng Outbox.
           Redis chỉ đệm cho việc đọc như sao kê. Bộ chuyển Outbox đọc bảng rồi gửi sang Kafka, và dịch vụ thông báo nhận từ Kafka.
           Tất cả được đóng gói bằng Docker, và đường ống tích hợp liên tục chạy kiểm rồi mới triển khai."""),
        st(svg(1500, 400,
               txt(50, 45, "ngân sách 300 ms cho một lệnh chuyển (số minh hoạ), vẽ đúng tỉ lệ", 24, "start", "#1f2937", True),
               _seg(50, 47, C_BLUE), _seg(97, 23, C_GREEN), _seg(120, 93, C_AMBER), _seg(213, 187, C_RED), _seg(400, 1050, C_GRAY),
               txt(925, 120, "còn dư 225 ms", 28, "middle", "#1f2937", True),
               box(50, 200, 250, 70, "cổng 10 ms", C_BLUE, size=22), box(320, 200, 250, 70, "xác thực 5 ms", C_GREEN, size=22),
               box(590, 200, 250, 70, "dịch vụ 20 ms", C_AMBER, size=22), box(860, 200, 250, 70, "Oracle 40 ms", C_RED, size=22),
               box(1130, 200, 320, 70, "còn dư 225 ms", C_GRAY, size=22, bold=True),
               txt(750, 340, "đã dùng 10 + 5 + 20 + 40 = 75 ms, tức 25% ngân sách", 26, "middle", "#1f2937", True)),
           """Hình thứ hai vẽ ngân sách ba trăm mili giây cho một lệnh chuyển, đúng tỉ lệ, và đây là số minh hoạ.
           Cổng mười mili giây, xác thực năm, dịch vụ hai mươi, Oracle bốn mươi. Bốn chặng cộng lại là bảy mươi lăm mili giây, tức hai mươi lăm phần trăm.
           Phần xám còn dư hai trăm hai mươi lăm mili giây, rộng hơn hẳn tổng các chặng, nên chưa đo thì chưa có lý do tối ưu chặng nào."""),
        st(code(OAS_YAML, "Hợp đồng API của dự án mẫu (OpenAPI 3), viết trước mã"),
           """Cuối cùng là hợp đồng API của dự án mẫu, viết bằng OpenAPI trước khi viết mã, như bài 1 đã dạy.
           Đường dẫn chuyển tiền dùng phương thức gửi, và bắt buộc có tham số khoá lũy đẳng ở phần đầu yêu cầu.
           Hợp đồng ghi ba phản hồi, gồm hai trăm linh một là đã ghi lệnh, bốn trăm là sai lược đồ, và bốn trăm hai mươi chín là quá giới hạn tốc độ ở cổng.""",
           clear=True, focus=[1, 2, 2]),
    ], checks=["alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225", "10 + 5 + 20 + 40 == 75", "Fraction(75, 300) == Fraction(25, 100)",
               "[round(Fraction(1400, 300) * x) for x in (10, 5, 20, 40, 225)] == [47, 23, 93, 187, 1050]"])

    form = sc("formula", "formula", "Suy ra từng bước: từ số giao dịch mỗi ngày tới ngân sách", [
        st("""<p><b>Bước 1.</b> Vì giao dịch được tính theo ngày còn hệ thống chịu tải theo giây, nên đổi ngày ra giây: $24 \\cdot 60 \\cdot 60 = 86\\,400$.</p>
<p><b>Bước 2.</b> Chia đều thì tải trung bình $= \\frac{\\text{số giao dịch mỗi ngày}}{86\\,400}$.</p>
<span class='note'>Làm thử: $86\\,400$ giao dịch/ngày → $\\frac{86\\,400}{86\\,400} = 1$ giao dịch/giây.</span>""",
           """Bước một, vì giao dịch được tính theo ngày còn hệ thống chịu tải theo từng giây, nên ta đổi ngày ra giây, được tám mươi sáu nghìn bốn trăm.
           Bước hai, nếu chia đều thì tải trung bình bằng số giao dịch mỗi ngày chia cho tám mươi sáu nghìn bốn trăm. Làm thử, tám mươi sáu nghìn bốn trăm giao dịch mỗi ngày chia đều là một giao dịch mỗi giây.""",
           ),
        st("""<p><b>Bước 3.</b> Giao dịch dồn vào giờ đông, nên nhân hệ số cao điểm $k$ <i>(số minh hoạ; số thật lấy từ nhật ký)</i>.</p>
<span class='note'>Làm thử: $1$ giao dịch/giây, $k = 10$ → $10$ giao dịch/giây ở cao điểm.</span>""",
           """Bước ba, vì giao dịch dồn vào giờ đông, nên ta nhân thêm hệ số cao điểm k. Đây là số minh hoạ, còn số thật phải lấy từ nhật ký.
           Làm thử, một giao dịch mỗi giây với k bằng mười thì cao điểm là mười giao dịch mỗi giây."""),
        st("""<p><b>Bước 4.</b> Các chặng chạy <b>nối tiếp</b>, nên thời gian cộng lại: phần dư $=$ ngân sách $-$ tổng các chặng.</p>
<span class='note'>Làm thử:</span>
$$100 - (30 + 50) = 20 \\text{ ms}$$""",
           """Bước bốn, vì các chặng chạy nối tiếp, chặng sau chờ chặng trước, nên thời gian cộng lại. Phần dư bằng ngân sách trừ tổng các chặng.
           Làm thử, ngân sách một trăm mili giây, hai chặng ba mươi và năm mươi, thì còn dư hai mươi.""", focus=[1, 1, 3]),
        st("""<p><b>Bước 5.</b> Khi tải ổn định, số lệnh <b>trung bình</b> đang ở một chặng <b>cùng lúc</b> $=$ số lệnh đến mỗi giây $\\cdot$ thời gian mỗi lệnh ở đó (định luật Little), vì mỗi giây có lệnh mới vào trong khi lệnh cũ chưa ra.</p>
<span class='note'>Làm thử: $10$ lệnh/giây, mỗi lệnh ở lại $0{,}1$ giây → $10 \\cdot 0{,}1 = 1$ lệnh cùng lúc, tính trung bình.</span>""",
           """Bước năm, khi tải ổn định, số lệnh trung bình ở một chặng cùng lúc bằng số lệnh đến mỗi giây nhân thời gian mỗi lệnh ở đó, vì lệnh mới vào trong khi lệnh cũ chưa ra.
           Giống một quầy giao dịch, mỗi giây mười khách vào, mỗi khách ở lại một phần mười giây, thì trung bình trong quầy có một khách.""", clear=True),
    ], checks=["24 * 60 * 60 == 86400", "alg.bnx_l15_tps(86400) == 1", "alg.bnx_l15_tps(86400, 10) == 10", "alg.bnx_l15_left(100, [30, 50]) == 20",
               "alg.bnx_l15_inflight(10, 100) == 1"])

    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Một triệu giao dịch mỗi ngày, dùng lại $86\\,400$ giây ở bước 1.</p>
$$① \\; \\frac{1\\,000\\,000}{86\\,400} \\approx \\hl{11{,}6}\\ \\text{giao dịch/giây}$$""",
           """Ta tính từng bước. Phép tính thứ nhất, một triệu chia tám mươi sáu nghìn bốn trăm, xấp xỉ mười một phẩy sáu giao dịch mỗi giây."""),
        st("""<p>Dùng lại kết quả ① chưa làm tròn ($11{,}574\\ldots$), cao điểm gấp $10$ <i>(số minh hoạ)</i>.</p>
$$② \\; 10 \\cdot 11{,}574 \\approx \\hl{116}\\ \\text{giao dịch/giây}$$""",
           """Phép tính thứ hai dùng lại kết quả trước khi làm tròn, là mười một phẩy năm bảy bốn. Nhân hệ số cao điểm mười, là số minh hoạ, ta được xấp xỉ một trăm mười sáu giao dịch mỗi giây.""",
           introduces=["dots"]),
        st("""$$③ \\; 10 + 5 + 20 + 40 = \\hl{75}\\ \\text{ms}$$""",
           """Phép tính thứ ba, cộng bốn chặng nối tiếp. Cổng mười, xác thực năm, dịch vụ hai mươi, Oracle bốn mươi, tổng bảy mươi lăm mili giây."""),
        st("""$$④ \\; 300 - 75 = \\hlg{225}\\ \\text{ms còn dư (số minh hoạ)}$$""",
           """Phép tính thứ tư, dùng lại số bảy mươi lăm. Ba trăm trừ bảy mươi lăm, còn dư hai trăm hai mươi lăm mili giây, và đây vẫn là số minh hoạ.""", clear=True),
        st("""<p>Dùng lại $116$ ở ② và $40$ ms của Oracle ở ③ (đổi ra $0{,}040$ giây).</p>
$$⑤ \\; 116 \\cdot 0{,}040 = \\hl{4{,}64}\\ \\text{lệnh cùng lúc ở Oracle (trung bình)}$$""",
           """Phép tính thứ năm dùng lại một trăm mười sáu và bốn mươi mili giây của Oracle, đổi ra không phẩy không bốn mươi giây.
           Theo bước năm, một trăm mười sáu nhân không phẩy không bốn mươi bằng bốn phẩy sáu bốn. Vậy ở cao điểm, trung bình chỉ khoảng năm lệnh đang chạy cùng lúc trên Oracle.""", focus=[1, 2, 2]),
        st(code(CAP_PY, "Tính lại bằng Python"),
           """Giờ ta cho máy tính lại cả năm số bằng Python. Năm câu lệnh đầu tính số giây trong ngày, tải trung bình, tải cao điểm, phần còn dư và số lệnh cùng lúc.
           Năm câu lệnh sau in từng kết quả, có làm tròn tải trung bình một chữ số thập phân và tải cao điểm tới hàng đơn vị.""", clear=True, focus=[1, 2, 2]),
        st("<p>Bằng tay: ① 11,6; ② 116; ④ 225; ⑤ 4,64.</p>" + out(CAP_OUT),
           """Kết quả chạy thật in ra đúng các số ta đã tính bằng tay. Python dùng dấu chấm thay cho dấu phẩy thập phân, nên mười một chấm sáu chính là mười một phẩy sáu.""",
           clear=True, focus=[1, 3]),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + TPS + ", 3) == Fraction('11.574')",
               "alg.bnx_l15_round(" + PEAK + ") == 116", "10 + 5 + 20 + 40 == 75", "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 300 - 75 == 225",
               "alg.bnx_l15_inflight(116, 40) == Fraction(464, 100)", "round(float(alg.bnx_l15_inflight(116, 40))) == 5"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính theo giờ và cộng ngược", [
        st("""<p>Đường khác: chia theo <b>giờ</b> trước, rồi mới chia theo giây.</p>
$$\\frac{1\\,000\\,000}{24} \\approx 41\\,667\\ \\text{giao dịch/giờ}, \\qquad \\frac{41\\,667}{3\\,600} \\approx \\hlg{11{,}6}$$
<p>Cộng ngược ngân sách: $10 + 5 + 20 + 40 + 225 = \\hlg{300}$ ms.</p>""",
           """Kiểm bằng đường khác, ta chia theo giờ trước. Một triệu chia hai mươi bốn, xấp xỉ bốn mươi mốt nghìn sáu trăm sáu mươi bảy giao dịch mỗi giờ.
           Chia tiếp cho ba nghìn sáu trăm giây, được xấp xỉ mười một phẩy sáu, khớp phép tính thứ nhất.
           Cộng ngược ngân sách, mười cộng năm cộng hai mươi cộng bốn mươi cộng hai trăm hai mươi lăm bằng ba trăm, nên phép trừ đúng.""", focus=[1, 2, 2, 3]),
        st(table(["con số", "loại", "nói khi phỏng vấn"],
                 [["11,6 và 116 giao dịch/giây", "ước lượng từ đề bài; hệ số 10 là giả định", "“nếu cao điểm gấp 10 thì khoảng 116/giây”"],
                  ["225 ms còn dư", "số minh hoạ", "“chặng chậm nhất phải đo, chưa đo thì chưa sửa”"],
                  ["p99 của dự án mẫu", "số đo thật, chỉ có khi bạn đo", "“trên máy của tôi, dữ liệu giả, công cụ …, ngày …: p99 = …”"]]),
           """Bảng này tách ba loại con số, vì người phỏng vấn sẽ hỏi số đó từ đâu ra. Mười một phẩy sáu và một trăm mười sáu là ước lượng từ đề bài, và hệ số mười là giả định.
           Hai trăm hai mươi lăm mili giây là số minh hoạ. Còn phân vị chín mươi chín của dự án mẫu là số đo thật, chỉ có khi bạn tự đo, và phải kèm máy, dữ liệu, công cụ, ngày đo.""",
           clear=True),
    ], checks=["alg.bnx_l15_round(Fraction(1000000, 24)) == 41667", "alg.bnx_l15_round(Fraction(41667, 3600), 1) == Fraction('11.6') == alg.bnx_l15_round(" + TPS + ", 1)",
               "10 + 5 + 20 + 40 + alg.bnx_l15_left(300, [10, 5, 20, 40]) == 300"])

    pit = sc("pitfalls", "pitfall", "Bài học sai hay gặp khi làm dự án mẫu", [
        st("""<div class="box warn"><b>Lỗi 1 (nặng nhất).</b> <b class="red">Khai số đo của dự án mẫu là số của hệ thống ngân hàng thật</b>, kiểu “hệ thống tôi làm chịu 116 giao dịch/giây”. Người phỏng vấn hỏi hai lớp là lộ.
<br><span class="note">Nói đúng: “dự án cá nhân, máy của tôi, dữ liệu giả, đo được …”.</span></div>""",
           """Lỗi thứ nhất, và nặng nhất, là khai số đo của dự án mẫu như số của hệ thống ngân hàng thật, kiểu hệ thống tôi làm chịu một trăm mười sáu giao dịch mỗi giây. Người phỏng vấn hỏi thêm hai lớp là lộ.
           Hãy nói đúng, đây là dự án cá nhân, chạy trên máy của tôi với dữ liệu giả, và đo được bao nhiêu."""),
        st("""<div class="box warn"><b>Lỗi 2 (mức hệ thống).</b> <b class="red">Thêm công nghệ chỉ vì có trong tin tuyển dụng (JD)</b>: nhét Elasticsearch, Couchbase, gRPC vào một API chuyển khoản không có yêu cầu nào cần chúng.
<br><span class="note">Phép thử: bỏ thành phần đó đi thì yêu cầu nào hỏng? Không có → bỏ.</span></div>""",
           """Lỗi thứ hai ở mức hệ thống, là thêm công nghệ chỉ vì có trong tin tuyển dụng. Ví dụ nhét công cụ tìm kiếm, kho lưu theo khoá và lời gọi nhị phân vào một API chuyển khoản không có yêu cầu nào cần chúng.
           Phép thử là hỏi, bỏ thành phần đó đi thì yêu cầu nào hỏng. Nếu không có yêu cầu nào hỏng, hãy bỏ nó."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Tối ưu trước khi đo</b>: đệm số dư vào Redis cho “nhanh” khi Oracle mới dùng $40$ trong $300$ ms. Vừa không cần, vừa sai: số dư trong bộ đệm có thể cũ, dùng nó để trừ tiền là trừ sai.
<br><span class="note">Phép thử: đo phân vị 99 của từng chặng trước, sửa chặng chậm nhất.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, là tối ưu trước khi đo. Ví dụ đệm số dư vào Redis cho nhanh, trong khi Oracle mới dùng bốn mươi trong ba trăm mili giây.
           Việc đó vừa không cần, vừa sai, vì số dư trong bộ đệm có thể cũ, dùng nó để trừ tiền là trừ sai. Phép thử là đo phân vị chín mươi chín của từng chặng trước, rồi sửa chặng chậm nhất."""),
    ])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "2 000 000 giao dịch/ngày, cao điểm gấp 8 (số minh hoạ): trung bình và cao điểm bao nhiêu giao dịch/giây?"],
                  ["2", "Ngân sách 250 ms; cổng 10, xác thực 5, dịch vụ 20, Oracle 40, thêm một lần đọc Redis 2 ms. Còn dư bao nhiêu?"],
                  ["3", "Quyết định: ở 116 giao dịch/giây, dùng Outbox + Kafka, hay Outbox + một bảng mà dịch vụ thông báo đọc thẳng?"]]),
           """Đến lượt bạn. Câu một, hai triệu giao dịch mỗi ngày, cao điểm gấp tám, là số minh hoạ, thì trung bình và cao điểm bao nhiêu giao dịch mỗi giây?
           Câu hai, ngân sách hai trăm năm mươi mili giây, gồm cổng mười, xác thực năm, dịch vụ hai mươi, Oracle bốn mươi, và thêm một lần đọc Redis hai mili giây. Còn dư bao nhiêu?
           Câu ba là một quyết định. Ở một trăm mười sáu giao dịch mỗi giây, nên dùng Outbox cộng Kafka, hay Outbox cộng một bảng mà dịch vụ thông báo đọc thẳng? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1:</p>
$$\\frac{2\\,000\\,000}{86\\,400} \\approx \\hl{23{,}1}, \\qquad 8 \\cdot 23{,}148 \\approx \\hl{185}\\ \\text{giao dịch/giây}$$""",
           """Đáp án câu một. Hai triệu chia tám mươi sáu nghìn bốn trăm, xấp xỉ hai mươi ba phẩy một giao dịch mỗi giây.
           Nhân tám, dùng số chưa làm tròn hai mươi ba phẩy một bốn tám, được xấp xỉ một trăm tám mươi lăm giao dịch mỗi giây.""", focus=[1, 2, 2]),
        st("""<p>Câu 2: các chặng nối tiếp nên cộng lại, $10 + 5 + 20 + 40 + 2 = 77$.</p>
$$250 - 77 = \\hlg{173}\\ \\text{ms}$$""",
           """Đáp án câu hai. Các chặng nối tiếp nên cộng lại, mười cộng năm cộng hai mươi cộng bốn mươi cộng hai, bằng bảy mươi bảy. Hai trăm năm mươi trừ bảy mươi bảy còn dư một trăm bảy mươi ba mili giây."""),
        st(table(["lựa chọn", "được", "mất", "đổi khi"],
                 [["Outbox + một bảng", "ít thành phần, một cơ sở dữ liệu; dễ chạy, dễ giải thích; 116/giây là tải nhỏ", "dịch vụ thông báo quét bảng, thêm việc cho Oracle; mỗi người nhận mới lại phải đọc bảng", "chỉ một người nhận, chưa đo thấy quét bảng làm chậm Oracle"],
                  ["Outbox + Kafka", "nhiều dịch vụ cùng nghe, đọc lại được lịch sử, người nhận đi nhịp riêng", "thêm cụm Kafka phải vận hành, thêm chỗ hỏng", "từ hai người nhận trở lên, cần đọc lại, hoặc đo thấy bảng là điểm nghẽn"]])
           + "<p class='note'>Cả hai cách đều gửi <b>ít nhất một lần</b>: bên gửi có thể sập sau khi gửi mà chưa kịp ghi “đã gửi”, rồi gửi lại. Người nhận phải lũy đẳng ở <b>cả hai</b> cách.</p>",
           """Đáp án câu ba là một đánh đổi. Outbox cộng một bảng có ít thành phần, một cơ sở dữ liệu, dễ chạy và dễ giải thích, vì một trăm mười sáu giao dịch mỗi giây là tải nhỏ. Đổi lại, quét bảng thêm việc cho Oracle, và mỗi người nhận mới lại phải đọc bảng.
           Outbox cộng Kafka cho nhiều dịch vụ cùng nghe, đọc lại được lịch sử, nhưng thêm một cụm phải vận hành.
           Ở cả hai cách, bên gửi có thể sập sau khi gửi mà chưa kịp ghi là đã gửi, rồi gửi lại, nên người nhận phải lũy đẳng ở cả hai cách.
           Ở tải này, Kafka không cần vì thông lượng. Nên chọn Kafka khi có từ hai người nhận trở lên, cần đọc lại, hoặc đo thấy bảng là điểm nghẽn, và khi phỏng vấn hãy nói đúng lý do đó.""", focus=[1, 1, 1, 1, 2, 1, 1]),
    ], checks=["alg.bnx_l15_round(alg.bnx_l15_tps(2000000), 1) == Fraction('23.1')", "alg.bnx_l15_round(alg.bnx_l15_tps(2000000), 3) == Fraction('23.148')",
               "alg.bnx_l15_round(alg.bnx_l15_tps(2000000, 8)) == 185", "10 + 5 + 20 + 40 + 2 == 77",
               "alg.bnx_l15_left(250, [10, 5, 20, 40, 2]) == 250 - 77 == 173", "alg.bnx_l15_round(" + PEAK + ") == 116"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("yêu cầu của tin tuyển dụng", "con số: 11,6 và 116 giao dịch/giây, dư 225 ms", "mỗi thành phần trả lời một yêu cầu",
                 "đo trên dự án của mình", "kể đúng số đo, đúng nơi đo"),
           """Tổng kết chuỗi logic. Bắt đầu từ yêu cầu của tin tuyển dụng, đổi thành con số, là mười một phẩy sáu và một trăm mười sáu giao dịch mỗi giây, còn dư hai trăm hai mươi lăm mili giây.
           Mỗi thành phần phải trả lời một yêu cầu. Sau đó đo trên dự án của chính mình, và kể đúng số đo, đúng nơi đo."""),
        st("""<div class='box key'><b>Tư duy chuyên gia:</b> mỗi thành phần phải trả lời một yêu cầu; mỗi con số phải nói rõ đo ở đâu; <b>đo trước khi tối ưu</b>.</div>""",
           """Điều cần mang theo là tư duy của chuyên gia. Mỗi thành phần phải trả lời một yêu cầu, mỗi con số phải nói rõ đo ở đâu, và luôn đo trước khi tối ưu."""),
        st("""<p class='note'>Đây là bài tổng hợp của phần nền. Phần còn lại của khoá đi sâu thêm từng công nghệ khác; sau đó là ôn phỏng vấn, kể dự án mẫu này bằng số đo thật của bạn.</p>""",
           """Đây là bài tổng hợp của phần nền. Phần còn lại của khoá đi sâu thêm từng công nghệ khác, rồi đến chặng ôn phỏng vấn, nơi bạn kể dự án mẫu này bằng số đo thật của mình."""),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + PEAK + ") == 116", "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225"])
    return lesson("L15", "tinh_huong_du_an_mau", "Bài 15 — Tình huống chuyên gia: dựng dự án mẫu API chuyển khoản đúng như JD đòi hỏi",
                  "curriculum/bnx.yaml L15; audit/bnx/verify_bnx.py L15; tình huống giả định loại quyết định nghề nghiệp, mọi độ trễ, hệ số cao điểm và tải là "
                  "số minh hoạ do người soạn đặt ra (không phải số của ngân hàng nào); câu trích tin tuyển dụng từ resources/job/JD.md (tin Software Engineer); "
                  "OpenAPI Specification 3.0.3 [OAS]; dùng lại các hàm kiểm của BNK (khoá lũy đẳng, sổ cái)",
                  ["Lập ngân sách độ trễ cho một lệnh chuyển khoản", "Ước lượng tải trung bình và cao điểm từ số giao dịch mỗi ngày",
                   "Chọn thành phần cho từng yêu cầu của JD và nêu đánh đổi", "Trình bày dự án mẫu trong buổi phỏng vấn bằng số đo thật của mình"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
