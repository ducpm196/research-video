import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene
from spk12 import spoken
from libj import jstep, nowrap

lib2.begin("L15")

# Mã trên màn hình: prog(...) chạy THẬT (đệm ở audit/bnx/progcache/L15.json); đầu ra ASCII. OAS_YAML là YAML (sổ `other` giữ từ bản cũ).
CAP_PY = """ngay = 24 * 60 * 60                 # giây trong một ngày
tb = 1_000_000 / ngay               # giao dịch/giây, trung bình
cao = 10 * tb                       # cao điểm gấp 10 (số minh hoạ)
du = 300 - (10 + 5 + 20 + 40)       # ms còn dư (số minh hoạ)
dong_thoi = cao * 40 / 1000         # lệnh cùng lúc ở Oracle
print("giay moi ngay:", ngay)
print("trung binh:", round(tb, 1))
print("cao diem:", round(cao))
print("con du (ms):", du)
print("cung luc o Oracle:", round(dong_thoi, 2))"""
CAP_OUT = """giay moi ngay: 86400
trung binh: 11.6
cao diem: 116
con du (ms): 225
cung luc o Oracle: 4.63"""
CAP = prog("Cap", CAP_PY, lang="python", out=CAP_OUT,
           claims=["một triệu giao dịch/ngày: trung bình 11,6, cao điểm (gấp 10, số minh hoạ) 116 giao dịch/giây; còn dư 225 ms; 4,63 lệnh cùng lúc ở Oracle (115,74 chưa làm tròn × 0,040; số minh hoạ)"])

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

# Quy mô: đếm số lệnh chạy chồng nhau ở Oracle (mỗi lệnh ở lại 40 ms) khi tải cao điểm tăng ×1, ×100, ×10 000 (số minh hoạ)
CUNG_PY = """def cung_luc(tps, w=40_000):            # w: micro giay
    vao = [i * 1_000_000 // tps for i in range(tps // 5)]
    j = top = 0
    for i, t in enumerate(vao):
        while vao[j] + w <= t:
            j += 1
        top = max(top, i - j + 1)
    return top

for tps in (116, 11_574, 1_157_407):
    print(tps, round(tps * 0.040, 2), cung_luc(tps))"""
CUNG_OUT = """116 4.64 5
11574 462.96 463
1157407 46296.28 46297"""
CUNG = prog("CungLuc", CUNG_PY, lang="python", out=CUNG_OUT, timeout=120,
            claims=["đếm thật số lệnh chồng nhau ở Oracle (mỗi lệnh 40 ms): 5, 463, 46 297 ở cao điểm 116, 11 574, 1 157 407 giao dịch/giây (phép nhân Little: 4,64; 462,96; 46 296,28)"],
            unverified_claims=["tải cao điểm 116 / 11 574 / 1 157 407 giao dịch/giây là ×1, ×100, ×10 000 của số minh hoạ 1 triệu giao dịch/ngày × hệ số 10; bể 50 kết nối và 40 ms mỗi lệnh là số minh hoạ, không đo hệ thống thật"])

# Lab (số liệu khác ví dụ): 5 triệu giao dịch/ngày, cao điểm gấp 6, ngân sách 400 ms, Oracle 120 ms, bể 30 kết nối
LAB_PY = """import math

ngay = 24 * 60 * 60
tb = 5_000_000 / ngay
cao = 6 * tb
chang = [12, 6, 25, 120, 3]
du = 400 - sum(chang)
dong_thoi = cao * 0.120
print("trung binh", round(tb, 1), "giao dich/giay")
print("cao diem", round(cao), "giao dich/giay")
print("con du", du, "ms")
print("cung luc o Oracle", round(dong_thoi, 1))
print("be 30 ket noi:", "khong du" if dong_thoi > 30 else "du", "- can it nhat", math.ceil(dong_thoi))"""
_lp = lib2.Prog("L15", "LabSol", LAB_PY, "python", {}, "lab", {})
_rc, _so, _se = _lp.execute()
assert _rc == 0, _se
LAB_OUT = _so.strip("\n")
EXPECT_LAB = """trung binh 57.9 giao dich/giay
cao diem 347 giao dich/giay
con du 234 ms
cung luc o Oracle 41.7
be 30 ket noi: khong du - can it nhat 42"""
assert LAB_OUT == EXPECT_LAB, LAB_OUT

LAB_DE = """# Lab BNX L15 — Ước lượng tải, ngân sách độ trễ và bể kết nối cho một bộ số liệu mới

Số liệu là số minh hoạ (không phải của ngân hàng nào). Viết `mau.py` (chỉ dùng Python có sẵn):

- **5 000 000** giao dịch mỗi ngày; cao điểm gấp **6** lần trung bình;
- ngân sách độ trễ **400 ms** cho một lệnh; các chặng nối tiếp (ms): cổng 12, xác thực 6, dịch vụ 25, Oracle 120, đọc Redis 3;
- mỗi lệnh ở lại Oracle **120 ms**; bể kết nối tới Oracle có **30** kết nối.

Tính và in đúng năm dòng (dùng `round(x, 1)` cho số có một chữ số thập phân, `round(x)` cho số nguyên, `math.ceil` làm tròn lên):

1. `trung binh <tải trung bình> giao dich/giay` — một chữ số thập phân (một ngày có 24·60·60 giây);
2. `cao diem <tải cao điểm> giao dich/giay` — làm tròn tới số nguyên;
3. `con du <số> ms` — ngân sách trừ tổng các chặng;
4. `cung luc o Oracle <số>` — số lệnh trung bình chạy cùng lúc ở Oracle ở cao điểm (tải cao điểm × thời gian mỗi lệnh, tính bằng giây, định luật Little), một chữ số thập phân; **nhân bằng tải cao điểm chưa làm tròn** (347 × 0,120 = 41,64 cho 41,6, còn số chưa làm tròn cho 41,7: làm tròn chỉ để in);
5. `be 30 ket noi: <du hoặc khong du> - can it nhat <số kết nối>` — bể đủ nếu số lệnh cùng lúc không vượt 30; số kết nối cần ít nhất là số lệnh cùng lúc làm tròn lên.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L15 mau.py`. Đầu ra viết không dấu.
"""

TPS = "alg.bnx_l15_tps(1000000)"
PEAK = "alg.bnx_l15_tps(1000000, 10)"


def _seg(x, w, col):
    return f'<rect x="{x}" y="70" width="{w}" height="80" fill="{col[0]}" stroke="{col[1]}" stroke-width="3"/>'


def build():
    write_lab("BNX", "L15", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Tình huống: hai tuần, một tin tuyển dụng, một dự án mẫu", [
        st("""<p><b>Tình huống giả định, số minh hoạ.</b> Tin tuyển dụng kỹ sư phần mềm ghi: <i>“thiết kế API backend xử lý hàng triệu giao dịch mỗi ngày”</i>, đặc tả API bằng Swagger, thủ tục lưu trữ Oracle/MS SQL, Kafka (nơi dịch vụ để lại tin cho dịch vụ khác lấy), Redis; điểm cộng Git, Docker.</p>
<div class="box key">Bạn có hai tuần để dựng dự án mẫu. Người phỏng vấn hỏi: “$1\\,000\\,000$ giao dịch mỗi ngày là bao nhiêu mỗi giây? Mỗi lệnh chuyển được bao nhiêu mili giây?”</div>""",
           """Chào bạn, đây là bài tổng hợp, một tình huống giả định với số minh hoạ. Một tin tuyển dụng đòi thiết kế API phía máy chủ xử lý hàng triệu giao dịch mỗi ngày, dùng Swagger, Oracle, Kafka và Redis.
           Bạn dựng dự án mẫu trong hai tuần, và người phỏng vấn hỏi một triệu giao dịch mỗi ngày là bao nhiêu mỗi giây, mỗi lệnh chuyển được bao nhiêu mili giây.""",
           focus=[1, 1, 2]),
        st(table(["bước", "việc", "kết quả của bài"],
                 [["1", "ước lượng tải", "trung bình ≈ 11,6 giao dịch/giây; cao điểm ≈ 116"],
                  ["2", "lập ngân sách độ trễ", "300 ms trừ các chặng còn dư 225 ms"],
                  ["3", "chọn thành phần theo yêu cầu", "mỗi thành phần trả lời một yêu cầu, kèm đánh đổi"],
                  ["4", "tải tăng gấp 100 và 10 000 lần", "đếm số lệnh cùng lúc ở Oracle, so với số kết nối mở sẵn"],
                  ["5", "trình bày khi phỏng vấn", "số đo thật trên máy của bạn, nói rõ đo ở đâu"]]),
           """Bảng này là lộ trình năm bước. Một, ước lượng tải, trung bình khoảng mười một phẩy sáu giao dịch mỗi giây, cao điểm khoảng một trăm mười sáu. Hai, ngân sách độ trễ ba trăm mili giây, còn dư hai trăm hai mươi lăm. Ba, chọn thành phần. Bốn, tải tăng gấp trăm và vạn lần. Năm, trình bày bằng số đo thật.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"], clear=True),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + PEAK + ") == 116",
               "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225"])

    pre = sc("prereq", "prereq", "Nhắc lại từ đầu: các mảnh ghép sẽ dùng", [
        st(table(["mảnh ghép", "nghĩa", "ví dụ số"],
                 [["khoá lũy đẳng + <code>UNIQUE</code>", "mỗi lệnh mang một khoá; cơ sở dữ liệu chỉ cho một dòng mang khoá đó", "3 lần gửi cùng khoá → 1 dòng"],
                  ["sổ cái bút toán kép", "mỗi giao dịch có dòng nợ và dòng có, tổng bằng 0", "$-200\\,000 + 200\\,000 = 0$"],
                  ["thủ tục lưu trữ, khoá theo thứ tự", "khoá hai tài khoản theo một thứ tự cố định để tránh bế tắc (hai lệnh chờ nhau mãi, không lệnh nào chạy tiếp), lỗi thì hoàn tác", "A 300 000, B 1 000 000; chuyển 200 000: tổng vẫn 1 300 000"]]),
           """Trước hết, ta nhắc lại các mảnh ghép sẽ dùng. Khoá lũy đẳng là mã gắn với mỗi lệnh, và ràng buộc duy nhất chỉ cho một dòng mang khoá đó.
           Sổ cái bút toán kép ghi mỗi giao dịch thành dòng nợ và dòng có với tổng bằng không. Thủ tục lưu trữ khoá hai tài khoản theo thứ tự cố định để tránh bế tắc, và lỗi thì hoàn tác.""",
           focus=[0, "1.2", "1.3", "1.4"]),
        st(table(["mảnh ghép", "nghĩa", "ví dụ"],
                 [["Outbox → Kafka", "ghi sự kiện vào bảng outbox trong cùng giao dịch ghi tiền; một tiến trình khác gửi sang Kafka", "Kafka hỏng 5 phút: sự kiện chờ trong bảng, không mất"],
                  ["Redis đệm đọc", "đọc nhanh nhưng có thể cũ; không dùng để quyết định trừ tiền", "sao kê đọc từ đệm, trừ tiền đọc từ Oracle"],
                  ["JWT, mTLS", "JWT: mã truy cập có chữ ký, nói người gọi là ai, được làm gì; mTLS: hai bên đều xuất trình chứng chỉ, nói máy nào đang gọi", "hai lớp xác thực khác nhau"],
                  ["Docker + GitLab CI, cổng API", "đóng gói, kiểm rồi mới triển khai; cổng giới hạn tốc độ", "test hỏng thì không deploy; mỗi khách 5/giây, sức chứa 10"],
                  ["OpenAPI (Swagger)", "tệp mô tả hợp đồng của API, viết trước khi viết mã; lược đồ là phần mô tả mỗi trường của yêu cầu có kiểu gì, bắt buộc hay không", "<code>POST /transfers</code> → 201, 400, 429"]]),
           """Bảng thứ hai là các mảnh ngoài cơ sở dữ liệu. Outbox ghi sự kiện vào bảng trong cùng giao dịch ghi tiền, rồi tiến trình khác gửi sang Kafka, nên Kafka hỏng thì sự kiện không mất.
           Redis đệm đọc nhanh nhưng có thể cũ, nên trừ tiền đọc từ Oracle. Mã truy cập cho biết người gọi, mTLS cho biết máy gọi.""",
           focus=[0, "1.2", "1.3", "1.4", ["1.5", "1.6"]], clear=True),
        st("""<p>Một phép tính khởi động: một ngày có bao nhiêu giây?</p>
$$24 \\cdot 60 \\cdot 60 = 86\\,400$$""",
           """Một phép tính khởi động: một ngày có hai mươi bốn giờ, mỗi giờ sáu mươi phút, mỗi phút sáu mươi giây, nên một ngày có tám mươi sáu nghìn bốn trăm giây.""",
           clear=True),
    ], checks=["alg.bnk_unique_key_rows(3) == 1", "alg.bnk_ledger_unbalanced([(1, 'A', -200000), (1, 'B', 200000)]) == []",
               "300000 + 1000000 == (300000 - 200000) + (1000000 + 200000) == 1300000", "24 * 60 * 60 == 86400 == 1 / alg.bnx_l15_tps(1)"])

    sym = sc("sym", "symbol", "Giải mã ngôn ngữ của nghề", [
        st(table(["từ", "nghĩa", "ví dụ"],
                 [["tải trung bình (giao dịch/giây)", "số giao dịch chia đều cho mọi giây trong ngày", "$86\\,400$ giao dịch/ngày → $1$/giây"],
                  ["hệ số cao điểm", "giờ đông nhất gấp mấy lần trung bình; lấy từ nhật ký thật, ở đây là số minh hoạ", "gấp $10$"],
                  ["ngân sách độ trễ", "tổng thời gian cho phép của một lệnh, chia cho từng chặng nối tiếp", "$300$ ms (số minh hoạ)"],
                  ["phân vị 99 (p99)", "99% yêu cầu nhanh hơn số này; trung bình che mất yêu cầu chậm", "p99 = 120 ms: trong mọi lệnh đã đo, khoảng 1% chậm hơn 120 ms"],
                  ["bể kết nối", "số kết nối tới cơ sở dữ liệu mở sẵn, dùng chung, có hạn; hết kết nối thì lệnh phải xếp hàng", "bể 50 kết nối"],
                  ["số minh hoạ / số đo thật", "số đặt ra để dạy / số bạn đo được, có máy, công cụ, ngày đo", "“trên máy của tôi …”"]]),
           """Bảng này giải mã ngôn ngữ của nghề. Tải trung bình là số giao dịch chia đều cho mọi giây trong ngày, hệ số cao điểm cho biết giờ đông nhất gấp mấy lần trung bình. Ngân sách độ trễ là thời gian cho phép của một lệnh, chia cho các chặng.
           Phân vị chín mươi chín là mức mà chín mươi chín phần trăm yêu cầu nhanh hơn. Bể kết nối là số kết nối mở sẵn, dùng chung và có hạn. Số đo thật phải kèm máy và ngày đo.""",
           focus=[0, ["1.2", "1.3"], "1.4", "1.5", "1.6", "1.7"],
           introduces=["bnx_be_ket_noi"]),
    ], checks=["alg.bnx_l15_tps(86400) == 1", "100 - 99 == 1"])

    intu = sc("intuition", "intuition", "Hình dung: dự án mẫu, ngân sách và hợp đồng API", [
        st(svg(1500, 500,
               box(20, 60, 220, 110, ["Ứng dụng", "khách hàng"], C_BLUE, bold=True),
               box(290, 60, 280, 110, ["Cổng API", "JWT, 5/giây", "mỗi khách"], C_GRAY, bold=True),
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
           """Hình đầu là kiến trúc của dự án mẫu. Ứng dụng gọi qua cổng API, nơi kiểm mã truy cập và giới hạn năm yêu cầu mỗi giây cho mỗi khách. Rồi tới dịch vụ chuyển khoản viết bằng Java với khung Spring Boot.
           Dịch vụ gọi một thủ tục lưu trữ trên Oracle, trong một giao dịch khoá hai tài khoản, ghi khoá lũy đẳng, sổ cái và Outbox. Redis chỉ đệm việc đọc, còn bộ chuyển Outbox gửi sang Kafka."""),
        st(table(["thành phần", "trả lời yêu cầu", "đánh đổi"],
                 [["Outbox + Kafka", "Kafka hỏng thì sự kiện không mất", "thêm bảng và cụm phải vận hành"],
                  ["đệm Redis", "đọc nhanh, bớt tải cho Oracle", "dữ liệu có thể cũ"],
                  ["xác thực: JWT, mTLS", "biết ai và máy nào gọi", "thêm một bước kiểm mỗi yêu cầu"],
                  ["cổng API", "một cửa vào, giới hạn tốc độ", "thêm một chặng độ trễ"],
                  ["hợp đồng OpenAPI", "hai bên thống nhất trước khi viết mã", "phải giữ hợp đồng khớp với mã"]]),
           """Mỗi thành phần trả lời một yêu cầu và có giá riêng. Outbox giữ sự kiện khi Kafka hỏng, đổi lại thêm bảng và cụm. Đệm Redis đọc nhanh, đổi lại dữ liệu có thể cũ.
           Xác thực và cổng giới hạn tốc độ, đổi lại thêm bước kiểm và thêm chặng. Hợp đồng thống nhất trước, đổi lại phải giữ khớp mã.""",
           clear=True),
        st(svg(1500, 400,
               txt(50, 45, "ngân sách 300 ms cho một lệnh chuyển (số minh hoạ), vẽ đúng tỉ lệ", 24, "start", "#1f2937", True),
               _seg(50, 47, C_BLUE), _seg(97, 23, C_GREEN), _seg(120, 93, C_AMBER), _seg(213, 187, C_RED), _seg(400, 1050, C_GRAY),
               txt(925, 120, "còn dư 225 ms", 28, "middle", "#1f2937", True),
               box(50, 200, 250, 70, "cổng 10 ms", C_BLUE, size=22), box(320, 200, 250, 70, "xác thực 5 ms", C_GREEN, size=22),
               box(590, 200, 250, 70, "dịch vụ 20 ms", C_AMBER, size=22), box(860, 200, 250, 70, "Oracle 40 ms", C_RED, size=22),
               box(1130, 200, 320, 70, "còn dư 225 ms", C_GRAY, size=22, bold=True),
               txt(750, 340, "đã dùng 10 + 5 + 20 + 40 = 75 ms, tức 25% ngân sách", 26, "middle", "#1f2937", True)),
           """Hình thứ hai vẽ ngân sách ba trăm mili giây cho một lệnh chuyển, là số minh hoạ. Cổng mười, xác thực năm, dịch vụ hai mươi, Oracle bốn mươi, cộng lại bảy mươi lăm mili giây, tức hai mươi lăm phần trăm.
           Phần dư hai trăm hai mươi lăm rộng hơn hẳn tổng các chặng, nên chưa đo thì chưa nên tối ưu chặng nào."""),
        jstep([("yflow", "<code>info: {title: …, version: 0.1.0}</code>: nhóm cặp khoá–giá trị trên một dòng; <code>- {name: Idempotency-Key, …}</code>: một phần tử của danh sách <code>parameters</code>", ""),
               (("<code>\"201\": {description: …}</code>", "khoá <code>\"201\"</code> đặt trong nháy vì là mã số; thụt vào hai dấu cách là khoá con của khoá phía trên", "Mã số đặt trong dấu nháy là tên khoá, và dòng thụt vào hai dấu cách là khoá con của khoá phía trên."), "<code>post:</code> nằm trong <code>/transfers:</code> nằm trong <code>paths:</code>", "")]),
        st(code(OAS_YAML, "Hợp đồng API của dự án mẫu (OpenAPI 3), viết trước mã"),
           """Cuối cùng là hợp đồng API viết bằng OpenAPI trước khi viết mã. Đường dẫn chuyển tiền dùng phương thức gửi và bắt buộc có tham số khoá lũy đẳng ở phần đầu yêu cầu.
           Ba phản hồi là hai trăm linh một đã ghi lệnh, bốn trăm sai lược đồ, và bốn trăm hai mươi chín quá giới hạn tốc độ.""",
           clear=True, focus=[["2.6", "2.7", "2.8"], ["2.10", "2.11", "2.12"]]),
    ], checks=["alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225", "10 + 5 + 20 + 40 == 75", "Fraction(75, 300) == Fraction(25, 100)",
               "[round(Fraction(1400, 300) * x) for x in (10, 5, 20, 40, 225)] == [47, 23, 93, 187, 1050]"])

    form = sc("formula", "formula", "Suy ra từng bước: từ số giao dịch mỗi ngày tới ngân sách", [
        st("""<p><b>Bước 1.</b> Vì giao dịch được tính theo ngày còn hệ thống chịu tải theo giây, nên đổi ngày ra giây: $24 \\cdot 60 \\cdot 60 = 86\\,400$.</p>
<p><b>Bước 2.</b> Chia đều thì tải trung bình $= \\frac{\\text{số giao dịch mỗi ngày}}{86\\,400}$.</p>
<span class='note'>Làm thử: $86\\,400$ giao dịch/ngày → $\\frac{86\\,400}{86\\,400} = 1$ giao dịch/giây.</span>""",
           """Bước một, vì giao dịch tính theo ngày còn hệ thống chịu tải theo giây, nên đổi ngày ra giây, được tám mươi sáu nghìn bốn trăm. Bước hai, chia đều thì tải trung bình bằng số giao dịch mỗi ngày chia cho con số đó, nên chừng ấy giao dịch mỗi ngày là một giao dịch mỗi giây.""",
           focus=[1, [2, 3]]),
        st("""<p><b>Bước 3.</b> Giao dịch dồn vào giờ đông, nên nhân hệ số cao điểm $k$ <i>(số minh hoạ; số thật lấy từ nhật ký)</i>.</p>
<span class='note'>Làm thử: $1$ giao dịch/giây, $k = 10$ → $10$ giao dịch/giây ở cao điểm.</span>""",
           """Bước ba, vì giao dịch dồn vào giờ đông, ta nhân hệ số cao điểm k, là số minh hoạ còn số thật lấy từ nhật ký. Làm thử, một giao dịch mỗi giây với k bằng mười thì cao điểm là mười.""",
           focus=[1, 2], clear=True),
        st("""<p><b>Bước 4.</b> Các chặng chạy <b>nối tiếp</b>, nên thời gian cộng lại: phần dư $=$ ngân sách $-$ tổng các chặng.</p>
<span class='note'>Làm thử:</span>
$$100 - (30 + 50) = 20 \\text{ ms}$$""",
           """Bước bốn, vì các chặng chạy nối tiếp nên thời gian cộng lại, và phần dư bằng ngân sách trừ tổng các chặng. Làm thử, ngân sách một trăm, hai chặng ba mươi và năm mươi thì còn dư hai mươi.""",
           focus=[1, [2, 3]], clear=True),
        st("""<p><b>Bước 5.</b> Khi tải ổn định, số lệnh <b>trung bình</b> đang ở một chặng <b>cùng lúc</b> $=$ số lệnh đến mỗi giây $\\cdot$ thời gian mỗi lệnh ở đó (định luật Little), vì mỗi giây có lệnh mới vào trong khi lệnh cũ chưa ra.</p>
<span class='note'>Làm thử: $10$ lệnh/giây, mỗi lệnh ở lại $0{,}1$ giây → $10 \\cdot 0{,}1 = 1$ lệnh cùng lúc, tính trung bình.</span>""",
           """Bước năm, khi tải ổn định, số lệnh trung bình ở một chặng cùng lúc bằng số lệnh đến mỗi giây nhân thời gian mỗi lệnh ở đó, vì lệnh mới vào trong khi lệnh cũ chưa ra. Giống quầy giao dịch: mỗi giây mười khách vào, mỗi khách ở một phần mười giây, thì trung bình có một khách.""",
           focus=[1, 2], clear=True),
    ], checks=["24 * 60 * 60 == 86400", "alg.bnx_l15_tps(86400) == 1", "alg.bnx_l15_tps(86400, 10) == 10", "alg.bnx_l15_left(100, [30, 50]) == 20",
               "alg.bnx_l15_inflight(10, 100) == 1"])

    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Một triệu giao dịch mỗi ngày, dùng lại $86\\,400$ giây ở bước 1.</p>
$$① \\; \\frac{1\\,000\\,000}{86\\,400} \\approx \\hl{11{,}6}\\ \\text{giao dịch/giây}$$""",
           """Ta tính từng bước. Phép tính thứ nhất: một triệu chia tám mươi sáu nghìn bốn trăm, xấp xỉ mười một phẩy sáu giao dịch mỗi giây."""),
        st("""<p>Dùng lại kết quả ① chưa làm tròn ($11{,}574\\ldots$), cao điểm gấp $10$ <i>(số minh hoạ)</i>.</p>
$$② \\; 10 \\cdot 11{,}574 \\approx 115{,}74 \\approx \\hl{116}\\ \\text{giao dịch/giây}$$""",
           """Phép tính thứ hai dùng lại kết quả chưa làm tròn, mười một phẩy năm bảy bốn. Nhân hệ số cao điểm mười, là số minh hoạ, được một trăm mười lăm phẩy bảy bốn, xấp xỉ một trăm mười sáu.""",
           introduces=["dots"]),
        st("""$$③ \\; 10 + 5 + 20 + 40 = \\hl{75}\\ \\text{ms}$$""",
           """Phép tính thứ ba cộng bốn chặng nối tiếp: cổng mười, xác thực năm, dịch vụ hai mươi, Oracle bốn mươi, tổng bảy mươi lăm mili giây."""),
        st("""$$④ \\; 300 - 75 = \\hlg{225}\\ \\text{ms còn dư (số minh hoạ)}$$""",
           """Phép tính thứ tư dùng lại bảy mươi lăm: ba trăm trừ bảy mươi lăm còn dư hai trăm hai mươi lăm mili giây, vẫn là số minh hoạ.""", clear=True),
        st("""<p>Dùng lại $115{,}74$ ở ② (chưa làm tròn) và $40$ ms của Oracle (đổi ra $0{,}040$ giây).</p>
$$⑤ \\; 115{,}74 \\cdot 0{,}040 \\approx \\hl{4{,}63}\\ \\text{lệnh cùng lúc ở Oracle (trung bình)}$$""",
           """Phép tính thứ năm dùng lại một trăm mười lăm phẩy bảy bốn chưa làm tròn, và bốn mươi mili giây của Oracle, đổi ra không phẩy không bốn mươi giây. Theo bước năm, hai số này nhân với nhau xấp xỉ bốn phẩy sáu ba, nên ở cao điểm trung bình chỉ khoảng năm lệnh chạy cùng lúc.""",
           focus=[1, 2]),
        jstep([(("<code>tb = 1_000_000 / ngay</code>", "gán thương cho <code>tb</code>; dấu gạch dưới chỉ để dễ đọc số; <code>/</code> chia ra số thập phân", "Dấu gạch dưới trong số chỉ để dễ đọc, và dấu gạch chéo chia ra số thập phân."), "<code>1_000_000 / 86400</code> ra 11.574…", ""),
               (("<code>round(tb, 1)</code>", "làm tròn <code>tb</code> còn 1 chữ số sau dấu phẩy; <code>round(x)</code> không có số thứ hai làm tròn thành số nguyên", "Hàm làm tròn giữ số chữ số sau dấu phẩy bằng số thứ hai."), "<code>round(11.574, 1)</code> ra 11.6", ""),
               (("<code>print(\"trung binh:\", round(tb, 1))</code>", "in chữ rồi số, cách nhau một dấu cách; <code># giây trong một ngày</code>: ghi chú, máy bỏ qua", "Lệnh in đưa chữ rồi số ra màn hình, còn dấu thăng mở đầu một ghi chú."), "dòng in: trung binh: 11.6", "")]),
        st(CAP.show(title="Tính lại bằng Python"),
           """Giờ ta cho Python tính lại: năm câu đầu tính các số, năm câu sau in kết quả.""",
           clear=True),
        st("<p>Bằng tay: ① 11,6; ② 116; ④ 225; ⑤ 4,63.</p>" + CAP.out_html(),
           """Kết quả chạy thật in ra đúng các số ta đã tính tay. Python dùng dấu chấm thay dấu phẩy thập phân, nên mười một chấm sáu là mười một phẩy sáu.""",
           clear=True, focus=[1, 3]),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + TPS + ", 3) == Fraction('11.574')",
               "alg.bnx_l15_round(" + PEAK + ") == 116", "10 + 5 + 20 + 40 == 75", "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 300 - 75 == 225",
               "alg.bnx_l15_round(alg.bnx_l15_tps(10**6, 10), 2) == Fraction('115.74')",
               "alg.bnx_l15_round(alg.bnx_l15_inflight(alg.bnx_l15_tps(10**6, 10), 40), 2) == Fraction('4.63')",
               "round(float(alg.bnx_l15_inflight(alg.bnx_l15_tps(10**6, 10), 40))) == 5"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính theo giờ và cộng ngược", [
        st("""<p>Đường khác: chia theo <b>giờ</b> trước, rồi mới chia theo giây.</p>
$$\\frac{1\\,000\\,000}{24} \\approx 41\\,667\\ \\text{giao dịch/giờ}, \\qquad \\frac{41\\,667}{3\\,600} \\approx \\hlg{11{,}6}$$
<p>Cộng ngược ngân sách: $10 + 5 + 20 + 40 + 225 = \\hlg{300}$ ms.</p>""",
           """Kiểm bằng đường khác: chia theo giờ trước, một triệu chia hai mươi bốn là bốn mươi mốt nghìn sáu trăm sáu mươi bảy mỗi giờ. Chia tiếp cho ba nghìn sáu trăm giây được mười một phẩy sáu, khớp phép tính thứ nhất.
           Cộng ngược ngân sách: mười cộng năm cộng hai mươi cộng bốn mươi cộng hai trăm hai mươi lăm bằng ba trăm.""",
           focus=[1, 2, 3]),
        st(table(["con số", "loại", "nói khi phỏng vấn"],
                 [["11,6 và 116 giao dịch/giây", "ước lượng từ đề bài; hệ số 10 là giả định", "“nếu cao điểm gấp 10 thì khoảng 116/giây”"],
                  ["225 ms còn dư", "số minh hoạ", "“chặng chậm nhất phải đo, chưa đo thì chưa sửa”"],
                  ["p99 của dự án mẫu", "số đo thật, chỉ có khi bạn đo", "“trên máy của tôi, dữ liệu giả, công cụ …, ngày …: p99 = …”"]]),
           """Bảng này tách ba loại con số, vì người phỏng vấn sẽ hỏi số đó từ đâu ra. Mười một phẩy sáu và một trăm mười sáu là ước lượng với hệ số mười giả định.
           Hai trăm hai mươi lăm là số minh hoạ, còn phân vị chín mươi chín là số đo thật, kèm máy và ngày đo.""",
           focus=[0, "1.2", ["1.3", "1.4"]], clear=True),
    ], checks=["alg.bnx_l15_round(Fraction(1000000, 24)) == 41667", "alg.bnx_l15_round(Fraction(41667, 3600), 1) == Fraction('11.6') == alg.bnx_l15_round(" + TPS + ", 1)",
               "10 + 5 + 20 + 40 + alg.bnx_l15_left(300, [10, 5, 20, 40]) == 300"])

    quymo = sc("quymo", "example", "Khi tải tăng gấp 100 và 10 000 lần: Oracle chịu ra sao", [
        jstep([(("<code>def cung_luc(tps, w=40_000):</code> … <code>return top</code>", "hàm tên <code>cung_luc</code>; <code>w=40_000</code> là giá trị có sẵn, gọi mà không truyền <code>w</code> thì <code>w</code> là 40 000; <code>return</code> trả <code>top</code> về nơi gọi", "Dòng đầu khai hàm, tham số có dấu bằng là giá trị có sẵn khi không truyền, và lệnh trả về đưa kết quả cho nơi gọi."), "<code>cung_luc(116)</code> dùng w = 40 000", ""),
               (("<code>j = top = 0</code>", "gán 0 cho cả hai biến cùng lúc", "Gán hai tên một lần đặt cả hai bằng không."), "j là 0 và top là 0", ""),
               ("pwhile", "<code>while vao[j] + w &lt;= t:</code> rồi <code>j += 1</code>: còn thoả thì tăng j thêm 1 và xét lại", ""),
               (("<code>for tps in (116, 11_574, 1_157_407):</code> <code>print(tps, round(tps * 0.040, 2), cung_luc(tps))</code>", "chạy ba lần, mỗi lần tps nhận một giá trị; <code>round(x, 2)</code> làm tròn x còn 2 chữ số sau dấu phẩy; <code>print</code> in ba giá trị cách nhau dấu cách", "Vòng lặp chạy ba lần với ba mức tải, hàm làm tròn giữ hai chữ số sau dấu phẩy, và lệnh in cho ra ba giá trị cách nhau dấu cách."), "dòng in: 116 4.64 5", "")]),
        st(table(["dòng mã", "nghĩa", "ví dụ nhỏ: 10 ms một lệnh, mỗi lệnh ở lại 40 ms"],
                 [["<code>vao = [i * 1_000_000 // tps for i in range(tps // 5)]</code>", "danh sách thời điểm lệnh đến, tính bằng micro giây (phần triệu giây), cách đều nhau; <code>//</code> chia lấy phần nguyên; dấu gạch dưới trong <code>1_000_000</code> chỉ để dễ đọc số", "đến lúc 0, 10 000, 20 000, … micro giây"],
                  ["<code>for i, t in enumerate(vao):</code>", "lặp qua từng lệnh, i là số thứ tự, t là thời điểm đến", "i = 4 thì t = 40 000"],
                  ["<code>while vao[j] + w &lt;= t: j += 1</code>", "bỏ qua lệnh đã xong: lệnh j xong khi giờ đến cộng thời gian ở lại không quá t", "lúc t = 40 000: lệnh 0 xong vì 0 + 40 000 ≤ 40 000"],
                  ["<code>top = max(top, i - j + 1)</code>", "số lệnh còn ở lại là i − j + 1; giữ số lớn nhất", "lệnh 1 tới 4 còn ở lại: 4 − 1 + 1 = 4"]]),
           """Dòng đầu tạo thời điểm đến của các lệnh, cách đều nhau, tính bằng phần triệu giây.
           Vòng lặp bỏ qua những lệnh đã xong, rồi đếm số lệnh còn ở lại và giữ số lớn nhất. Cứ mười mili giây một lệnh, mỗi lệnh ở bốn mươi, thì luôn có bốn lệnh chồng nhau.""", clear=True),
        st(CUNG.show(lines=(1, 8), title="Đếm số lệnh chạy chồng nhau: lệnh đến đều đặn, mỗi lệnh ở lại Oracle 40 ms"),
           """Đây là hàm đầy đủ: nó tạo các lệnh đến đều đặn, mỗi lệnh ở lại bốn mươi mili giây, rồi đếm nhiều nhất bao nhiêu lệnh chạy chồng nhau.""",
           focus=[2], clear=True),
        st(CUNG.show(lines=(10, 11)) + CUNG.out_html(title="Kết quả chạy thật: tải cao điểm, phép nhân Little, số lệnh đếm được") + "<p class=\"note\">Mô hình giả định mỗi lệnh luôn ở Oracle đúng 40 ms; thực tế khi lệnh dồn lại, Oracle chậm đi nên số thật còn cao hơn: đây là cận dưới. Tải ở đây đã làm tròn (116, không phải 115,74) nên 116 × 0,040 = 4,64, chênh 4,63 ở ví dụ chỉ do làm tròn.</p>",
           """Ta chạy ở ba mức tải cao điểm, gấp một, một trăm và mười nghìn lần.
           Cột giữa là tải nhân thời gian mỗi lệnh, cột cuối là số đếm thật: năm, bốn trăm sáu mươi ba, và bốn mươi sáu nghìn hai trăm chín mươi bảy.""",
           focus=[1, ["3.1", "3.2", "3.3"]], clear=True),
        st(table(["mức", "giao dịch mỗi ngày", "cao điểm (giao dịch/giây)", "lệnh cùng lúc ở Oracle (đếm thật)", "bể 50 kết nối chịu 50 ÷ 0,04 = 1 250 giao dịch/giây (số minh hoạ)"],
                 [["×1", "1 000 000", "116", "5", "đủ"],
                  ["×100", "100 000 000", "11 574", "463", "thiếu: hàng chờ dài thêm 11 574 − 1 250 = 10 324 lệnh mỗi giây"],
                  ["×10 000", "10 000 000 000", "1 157 407", "46 297", "thiếu: hàng chờ dài thêm 1 156 157 lệnh mỗi giây"]]),
           """Một bể năm mươi kết nối chịu một nghìn hai trăm năm mươi giao dịch mỗi giây.
           Ở gấp trăm lần, cao điểm là mười một nghìn năm trăm bảy mươi bốn nên hàng chờ dài thêm hơn mười nghìn lệnh mỗi giây, gấp vạn lần còn xa hơn.""",
           focus=[0, "1.2", ["1.3", "1.4"]], clear=True),
        st(table(["cách xử lý", "được", "mất"],
                 [["tăng số kết nối của bể", "dễ làm, không đổi mã", "cơ sở dữ liệu phải giữ thêm tiến trình, có trần; quá trần thì chậm hơn"],
                  ["nhân bản dịch vụ và chia dữ liệu theo tài khoản", "tải chia ra, chịu thêm gần tỉ lệ với số mảnh", "chuyển tiền giữa hai mảnh phức tạp hơn (cần chuỗi bước bù trừ: mỗi bước có bước huỷ để bù nếu bước sau hỏng)"],
                  ["xếp hàng bất đồng bộ (nhận lệnh vào hàng, trả lời sau) để làm phẳng cao điểm", "cao điểm thành dòng đều, Oracle không bị dồn", "khách chờ kết quả lâu hơn, thêm chỗ hỏng phải xử lý"]]),
           """Đây là đánh đổi phải chọn. Tăng số kết nối thì dễ nhưng cơ sở dữ liệu có trần. Chia dữ liệu theo tài khoản làm tải chia ra, đổi lại chuyển tiền giữa hai mảnh cần chuỗi bước bù trừ.
           Xếp hàng bất đồng bộ, tức nhận lệnh rồi trả lời sau, làm phẳng cao điểm, đổi lại khách chờ lâu hơn.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l15_inflight(t, 40) for t in (116, 11574, 1157407)] == [Fraction(464, 100), Fraction(46296, 100), Fraction(4629628, 100)]",
               "[alg.bnx_l15_round(alg.bnx_l15_inflight(t, 40), 2) for t in (116, 11574, 1157407)] == [Fraction('4.64'), Fraction('462.96'), Fraction('46296.28')]",
               "[round(alg.bnx_l15_tps(d, 10)) for d in (1_000_000, 100_000_000, 10_000_000_000)] == [116, 11574, 1157407]",
               "[alg.bnx_l15_pool_tps(50, 40)] == [1250] and 11574 - 1250 == 10324 and 1157407 - 1250 == 1156157",
               "100 * 116 == 11600 and 10_000 * 116 == 1_160_000"])

    pit = sc("pitfalls", "pitfall", "Bài học sai hay gặp khi làm dự án mẫu", [
        st("""<div class="box warn"><b>Lỗi 1 (nặng nhất).</b> <b class="red">Khai số đo của dự án mẫu là số của hệ thống ngân hàng thật</b>, kiểu “hệ thống tôi làm chịu 116 giao dịch/giây”. Người phỏng vấn hỏi hai lớp là lộ.
<br><span class="note">Nói đúng: “dự án cá nhân, máy của tôi, dữ liệu giả, đo được …”.</span></div>""",
           """Lỗi nặng nhất là khai số đo của dự án mẫu như số của hệ thống ngân hàng thật, kiểu hệ thống tôi chịu một trăm mười sáu giao dịch mỗi giây. Hỏi thêm hai lớp là lộ, nên hãy nói đúng: dự án cá nhân, dữ liệu giả."""),
        st("""<div class="box warn"><b>Lỗi 2 (mức hệ thống).</b> <b class="red">Thêm công nghệ chỉ vì có trong tin tuyển dụng (JD)</b>: nhét Elasticsearch (cơ sở dữ liệu tìm kiếm), Couchbase (cơ sở dữ liệu lưu dữ liệu dạng JSON), gRPC (cách gọi nhị phân giữa dịch vụ) vào một API chuyển khoản không có yêu cầu nào cần chúng.
<br><span class="note">Phép thử: bỏ thành phần đó đi thì yêu cầu nào hỏng? Không có → bỏ.</span></div>""",
           """Lỗi ở mức hệ thống là thêm công nghệ chỉ vì có trong tin tuyển dụng, như nhét công cụ tìm kiếm vào API chuyển khoản không cần nó. Phép thử là bỏ thành phần đó thì yêu cầu nào hỏng, không có thì bỏ.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Tối ưu trước khi đo</b>: đệm số dư vào Redis cho “nhanh” khi Oracle mới dùng $40$ trong $300$ ms. Vừa không cần, vừa sai: số dư trong bộ đệm có thể cũ, dùng nó để trừ tiền là trừ sai.
<br><span class="note">Phép thử: đo phân vị 99 của từng chặng trước (gửi nhiều lệnh thử, sắp thời gian tăng dần, lấy giá trị ở vị trí 99%), sửa chặng chậm nhất.</span></div>""",
           """Lỗi của người đã đi làm là tối ưu trước khi đo, ví dụ đệm số dư vào Redis trong khi Oracle mới dùng bốn mươi trong ba trăm mili giây. Việc đó vừa không cần vừa sai vì số dư trong đệm có thể cũ.""", clear=True),
    ])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "2 000 000 giao dịch/ngày, cao điểm gấp 8 (số minh hoạ): trung bình và cao điểm bao nhiêu giao dịch/giây?"],
                  ["2", "Ngân sách 250 ms; cổng 10, xác thực 5, dịch vụ 20, Oracle 40, thêm một lần đọc Redis 2 ms. Còn dư bao nhiêu?"],
                  ["3", "Quyết định: ở 116 giao dịch/giây, dùng Outbox + Kafka, hay Outbox + một bảng mà dịch vụ thông báo đọc thẳng?"]]),
           """Đến lượt bạn, ta có ba câu. Câu một: hai triệu giao dịch mỗi ngày, cao điểm gấp tám, thì trung bình và cao điểm bao nhiêu mỗi giây?
           Câu hai: ngân sách hai trăm năm mươi mili giây, các chặng mười, năm, hai mươi, bốn mươi và Redis hai, còn dư bao nhiêu? Câu ba: ở một trăm mười sáu giao dịch mỗi giây, nên dùng Outbox cộng Kafka hay Outbox cộng một bảng?
           Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1:</p>
$$\\frac{2\\,000\\,000}{86\\,400} \\approx \\hl{23{,}1}, \\qquad 8 \\cdot 23{,}148 \\approx \\hl{185}\\ \\text{giao dịch/giây}$$""",
           """Đáp án câu một: hai triệu chia tám mươi sáu nghìn bốn trăm xấp xỉ hai mươi ba phẩy một. Nhân tám, dùng số chưa làm tròn hai mươi ba phẩy một bốn tám, được xấp xỉ một trăm tám mươi lăm giao dịch mỗi giây.""",
           focus=[1, 2]),
        st("""<p>Câu 2: các chặng nối tiếp nên cộng lại, $10 + 5 + 20 + 40 + 2 = 77$.</p>
$$250 - 77 = \\hlg{173}\\ \\text{ms}$$""",
           """Đáp án câu hai: các chặng nối tiếp nên cộng lại bằng bảy mươi bảy, và hai trăm năm mươi trừ bảy mươi bảy còn dư một trăm bảy mươi ba mili giây."""),
        st(table(["lựa chọn", "được", "mất", "đổi khi"],
                 [["Outbox + một bảng", "ít thành phần, một cơ sở dữ liệu; dễ chạy, dễ giải thích; 116/giây là tải nhỏ", "dịch vụ thông báo quét bảng, thêm việc cho Oracle; mỗi người nhận mới lại phải đọc bảng", "chỉ một người nhận, chưa đo thấy quét bảng làm chậm Oracle"],
                  ["Outbox + Kafka", "nhiều dịch vụ cùng nghe, đọc lại được lịch sử, người nhận đi nhịp riêng", "thêm cụm Kafka phải vận hành, thêm chỗ hỏng", "từ hai người nhận trở lên, cần đọc lại, hoặc đo thấy bảng là điểm nghẽn"]])
           + "<p class='note'>Cả hai cách đều gửi <b>ít nhất một lần</b>: bên gửi có thể sập sau khi gửi mà chưa kịp ghi “đã gửi”, rồi gửi lại. Người nhận phải lũy đẳng ở <b>cả hai</b> cách.</p>",
           """Đáp án câu ba là một đánh đổi: Outbox cộng một bảng ít thành phần và dễ chạy, vì tải nhỏ, đổi lại mỗi người nhận mới phải đọc bảng. Outbox cộng Kafka cho nhiều dịch vụ cùng nghe, đổi lại thêm một cụm phải vận hành.
           Cả hai cách đều có thể gửi lại nên người nhận phải lũy đẳng; chọn Kafka khi có từ hai người nhận.""",
           focus=["1.2", "1.3", 2]),
    ], checks=["alg.bnx_l15_round(alg.bnx_l15_tps(2000000), 1) == Fraction('23.1')", "alg.bnx_l15_round(alg.bnx_l15_tps(2000000), 3) == Fraction('23.148')",
               "alg.bnx_l15_round(alg.bnx_l15_tps(2000000, 8)) == 185", "10 + 5 + 20 + 40 + 2 == 77",
               "alg.bnx_l15_left(250, [10, 5, 20, 40, 2]) == 250 - 77 == 173", "alg.bnx_l15_round(" + PEAK + ") == 116"])

    lab_pr = practice_scene(sc, "Tự làm: ước lượng tải, ngân sách và bể kết nối", practice_steps(
        st, "BNX", "L15",
        """<p><b>Đề</b>: viết <code>mau.py</code> cho bộ số liệu trong <code>de.md</code> (5 000 000 giao dịch/ngày, cao điểm gấp 6, ngân sách 400 ms, Oracle 120 ms, bể 30 kết nối) và in năm dòng:</p>
<ol><li>tải trung bình và tải cao điểm (giao dịch/giây)</li><li>phần dư của ngân sách độ trễ</li><li>số lệnh cùng lúc ở Oracle ở cao điểm</li><li>bể 30 kết nối đủ không, và cần ít nhất bao nhiêu kết nối</li></ol>
<p>Các chặng nối tiếp (ms): cổng 12, xác thực 6, dịch vụ 25, Oracle 120, đọc Redis 3.</p>
<p class="note">Số liệu khác ví dụ trong bài; đầu ra viết không dấu.</p>""",
        """Bây giờ tới phần bạn tự làm với bộ số liệu mới: năm triệu giao dịch mỗi ngày, cao điểm gấp sáu, ngân sách bốn trăm mili giây, năm chặng có trong đề, bể ba mươi kết nối.
           Viết chương trình in tải, phần dư, số lệnh cùng lúc và kết luận về bể. Hãy dừng video và tự viết.""",
        EXPECT_LAB, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> trung bình = 5 000 000 ÷ 86 400; cao điểm = 6 × trung bình; dư = 400 − tổng các chặng; cùng lúc = cao điểm CHƯA làm tròn × 0,120 (giây; làm tròn chỉ khi in); số kết nối cần = <code>math.ceil</code> của số cùng lúc.
Lời giải ở <code>labs/BNX/L15/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hãy chia năm triệu cho tám mươi sáu nghìn bốn trăm, nhân sáu, rồi nhân với thời gian mỗi lệnh ở Oracle tính bằng giây. Số kết nối cần là số đó làm tròn lên. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L15")
    lab_pr["checks"] = ["alg.bnx_l15_round(alg.bnx_l15_tps(5_000_000), 1) == Fraction('57.9') and alg.bnx_l15_round(alg.bnx_l15_tps(5_000_000, 6)) == 347",
                        "alg.bnx_l15_left(400, [12, 6, 25, 120, 3]) == 234",
                        "alg.bnx_l15_round(alg.bnx_l15_inflight(alg.bnx_l15_tps(5_000_000, 6), 120), 1) == Fraction('41.7')",
                        "alg.bnx_l15_inflight(alg.bnx_l15_tps(5_000_000, 6), 120).__ceil__() == 42 and 41.7 > 30"]

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("yêu cầu của tin tuyển dụng", "con số: 11,6 và 116 giao dịch/giây, dư 225 ms", "mỗi thành phần trả lời một yêu cầu",
                 "quy mô: đếm lệnh cùng lúc so với bể kết nối", "đo trên dự án của mình", "kể đúng số đo, đúng nơi đo"),
           """Tổng kết: từ tin tuyển dụng ta đổi ra mười một phẩy sáu và một trăm mười sáu giao dịch mỗi giây, dư hai trăm hai mươi lăm mili giây.
           Mỗi thành phần trả lời một yêu cầu, tải tăng thì đếm lại, rồi đo trên dự án của mình.""",
           focus=[["1.1", "1.3"], ["1.5", "1.7", "1.9", "1.11"]]),
        st("""<div class='box key'><b>Tư duy chuyên gia:</b> mỗi thành phần phải trả lời một yêu cầu; mỗi con số phải nói rõ đo ở đâu; <b>đo trước khi tối ưu</b>; và đếm lại khi tải tăng gấp trăm lần.</div>""",
           """Điều cần mang theo: mỗi con số nói rõ đo ở đâu, đo trước khi tối ưu, và đếm lại khi tải tăng."""),
        st("""<p class='note'>Đây là bài tổng hợp của phần nền. Phần còn lại của khoá đi sâu thêm từng công nghệ khác; sau đó là ôn phỏng vấn, kể dự án mẫu này bằng số đo thật của bạn.</p>""",
           """Phần còn lại của khoá đi sâu thêm từng công nghệ, rồi đến chặng ôn phỏng vấn để kể dự án mẫu bằng số đo thật."""),
    ], checks=["alg.bnx_l15_round(" + TPS + ", 1) == Fraction('11.6')", "alg.bnx_l15_round(" + PEAK + ") == 116", "alg.bnx_l15_left(300, [10, 5, 20, 40]) == 225"])
    scenes = spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L15", "tinh_huong_du_an_mau", "Bài 15 — Tình huống chuyên gia: dựng dự án mẫu API chuyển khoản đúng như JD đòi hỏi",
                  "curriculum/bnx.yaml L15; audit/bnx/verify_bnx.py L15; tình huống giả định loại quyết định nghề nghiệp, mọi độ trễ, hệ số cao điểm, tải và bể kết nối là "
                  "số minh hoạ do người soạn đặt ra (không phải số của ngân hàng nào); câu trích tin tuyển dụng từ resources/job/JD.md (tin Software Engineer); "
                  "OpenAPI Specification 3.0.3 [OAS]; dùng lại các hàm kiểm của BNK (khoá lũy đẳng, sổ cái); số lệnh cùng lúc đếm thật bằng Python (prog CungLuc), định luật Little",
                  ["Lập ngân sách độ trễ cho một lệnh chuyển khoản", "Ước lượng tải trung bình và cao điểm từ số giao dịch mỗi ngày",
                   "Nêu mỗi thành phần của dự án mẫu (Outbox, đệm Redis, xác thực, cổng, hợp đồng API) trả lời yêu cầu nào và đánh đổi của nó", "Nêu cách trình bày dự án mẫu trong buổi phỏng vấn: số đo thật kèm máy, dữ liệu và ngày đo",
                   "Đếm số lệnh chạy cùng lúc ở Oracle khi tải tăng gấp 1, 100 và 10 000 lần và so với bể kết nối",
                   "Viết chương trình Python ước lượng tải, ngân sách độ trễ và số kết nối cần cho một bộ số liệu mới"],
                  scenes,
                  covers=[(1, "formula"), (2, "formula"), (3, "intuition"), (4, "check"), (5, "quymo"), (6, "practice")], assumes=["bnx_saga_outbox"])
