from lib import *

# ── Mã trên màn hình (chạy/kiểm NGUYÊN VĂN: audit/review/screen_code.py; audit/bnx/ver/l01.py nạp đúng các hằng này) ──
SPEC_YAML = """openapi: 3.0.3
info:
  title: Transfer API
  version: 1.0.0
paths:
  /transfers:
    post:
      summary: Tạo lệnh chuyển khoản
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TransferRequest'
      responses:
        '201':
          description: Đã tạo lệnh chuyển
        '400':
          description: Yêu cầu sai lược đồ
        '409':
          description: Yêu cầu cùng khoá đang xử lý dở
        '422':
          description: Cùng khoá lũy đẳng nhưng khác nội dung
components:
  schemas:
    TransferRequest:
      type: object
      required: [fromAccount, toAccount, amount]
      properties:
        fromAccount:
          type: string
          pattern: '^[0-9]{10,19}$'
        toAccount:
          type: string
          pattern: '^[0-9]{10,19}$'
        amount:
          type: integer
          minimum: 1
"""
# năm đoạn hiện trên màn hình (dòng đầu, dòng cuối — tính từ 1); mỗi đoạn tự là một YAML hợp lệ
SPEC_PARTS = {"head": (1, 8), "input": (9, 20), "resp": (21, 29), "schema1": (30, 38), "schema2": (39, 44)}

BODY_JSON = """{
  "fromAccount": "0123456789",
  "toAccount": "9876543210",
  "amount": 500000
}"""

BODY_YAML = """fromAccount: '0123456789'
toAccount: '9876543210'
amount: 500000"""

VALIDATE_PY = """import re
TK = re.compile(r"^[0-9]{10,19}$")          # 10–19 chữ số
CAN = ("fromAccount", "toAccount", "amount")   # required

def kiem(req):
    loi = [f + ": thiếu" for f in CAN if req.get(f) is None]
    for f in ("fromAccount", "toAccount"):
        v = req.get(f)
        if v is not None and not (type(v) is str and TK.fullmatch(v)):
            loi.append(f + ": sai dạng")
    return loi + kiem_tien(req.get("amount"))

def kiem_tien(a):                 # a là None: đã báo "thiếu" ở trên
    ok = a is None or (type(a) is int and a >= 1)
    return [] if ok else ["amount: phải là số nguyên ≥ 1"]

A, B = "0123456789", "9876543210"
thu = [{"fromAccount": A, "toAccount": B, "amount": 500000},
       {"fromAccount": A, "toAccount": B, "amount": 0},
       {"fromAccount": A, "amount": 500000}]
for i, req in enumerate(thu, 1):
    loi = kiem(req)
    print(i, 400 if loi else 201, loi)
"""
VALIDATE_PARTS = {"ham": (1, 11), "thu": (13, 23)}

VALIDATE_OUT = """1 201 []
2 400 ['amount: phải là số nguyên ≥ 1']
3 400 ['toAccount: thiếu']"""

# Từ ngoại trong lời đọc: chỉ dùng khi đã dò phát âm (BRIEF mục 6). Chưa dò → nói bằng tiếng Việt, tên gốc chỉ trên màn hình.
SAY_WORDS = {"«JSON»": "JSON", "«YAML»": "YAML"}   # JSON, YAML: dò ASR 8/8 (audit/bnx/probes/x1.md), luật đọc ở lexicon_vi.BNX.yaml


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


def spec_part(name, title=None):
    return code(SPEC_YAML, title, lines=SPEC_PARTS[name])


def build():
    hook = sc("hook", "hook", "Hai đội làm mười ngày, ghép lại thì mọi yêu cầu bị từ chối", [
        S("""<p>Đội ứng dụng và đội máy chủ cùng làm tính năng chuyển tiền trong <b>10 ngày</b> (số minh hoạ). Không ai viết ra yêu cầu trông thế nào.</p>"""
          + table(["chỗ", "ứng dụng gửi", "máy chủ chờ"],
                  [["tên trường tài khoản nhận", "<code>to</code>", "<code>toAccount</code>"],
                   ["số tiền", "<code>\"500000\"</code> (chuỗi)", "<code>500000</code> (số nguyên)"]])
          + """<div class="box warn">Ngày ghép nối: máy chủ trả <b class="red">400</b> cho mọi yêu cầu.</div>""",
          """Chào bạn, đội ứng dụng và đội máy chủ cùng làm tính năng chuyển tiền trong mười ngày, đây là số minh hoạ. Không ai viết ra yêu cầu trông thế nào.
          Ứng dụng đặt tên trường tài khoản nhận một kiểu, máy chủ chờ một kiểu khác. Ứng dụng gửi số tiền năm trăm nghìn dưới dạng chuỗi chữ, còn máy chủ chờ một số nguyên.
          Ngày ghép nối, máy chủ trả mã bốn trăm cho mọi yêu cầu, và hai đội mất thêm nhiều ngày để cãi nhau xem ai sai.""",
          focus=[1, 1, "2.2", "2.3", 3]),
        S(table(["câu hỏi", "bài này trả lời"],
                [["viết hợp đồng API thế nào", "đặc tả OpenAPI: đường dẫn, phương thức, thân yêu cầu, phản hồi, lược đồ"],
                 ["kiểm một yêu cầu ra sao", "so từng trường với lược đồ, chỉ ra trường sai"],
                 ["sửa hợp đồng mà không làm gãy ai", "phân biệt thay đổi tương thích và thay đổi phá vỡ"]]),
          """Hôm nay ta trả lời ba câu hỏi. Viết hợp đồng cho một API thế nào, bằng chuẩn đặc tả OpenAPI.
          Kiểm một yêu cầu ra sao, bằng cách so từng trường với lược đồ. Và sửa hợp đồng thế nào để không làm gãy người đang dùng nó.""",
          focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_oas_status({'fromAccount': '0123456789', 'to': '9876543210', 'amount': '500000'}) == 400",
               "sorted(alg.bnx_oas_errors({'fromAccount': '0123456789', 'to': '9876543210', 'amount': '500000'})) == ['amount: sai kiểu', 'toAccount: thiếu']"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Yêu cầu HTTP", "phương thức và đường dẫn, phần đầu (các cặp tên: giá trị), rồi thân", "<code>POST /transfers</code>"],
                 ["② Mã trạng thái", "2xx là thành công, 4xx là lỗi của người gọi", "201 đã tạo, 400 yêu cầu sai, 409 xung đột, 422 không xử lý được"],
                 ["③ Khoá lũy đẳng", "mã người gọi gửi kèm mọi lần thử; cùng khoá thì máy chủ chỉ làm một lần", "thử 3 lần, chỉ trừ tiền 1 lần"]]),
          """Trước hết ta cần hiểu năm điều, và ba điều đầu sẽ được nhắc lại ngắn gọn ngay đây. Một yêu cầu HTTP gồm phương thức và đường dẫn, phần đầu là các cặp tên và giá trị, rồi đến thân.
          Mã trạng thái bắt đầu bằng chữ số hai là thành công, bắt đầu bằng bốn là lỗi của người gọi. Ví dụ hai trăm linh một là đã tạo, bốn trăm là yêu cầu sai, bốn trăm linh chín là xung đột, bốn trăm hai mươi hai là nội dung không xử lý được.
          Khoá lũy đẳng là mã người gọi gửi kèm mọi lần thử, nên thử ba lần thì máy chủ vẫn chỉ trừ tiền một lần.""",
          focus=[0, "1.2", "1.3", "1.3", "1.4"]),
        S("""<div class="row"><div class="col">"""
          + code(BODY_JSON, "④ Thân yêu cầu dạng JSON") + """</div><div class="col">"""
          + code(BODY_YAML, "⑤ Cùng dữ liệu, viết dạng YAML") + """</div></div>
<p class="note">Cả hai đều là 3 cặp tên: giá trị. YAML bỏ ngoặc, dùng <b>thụt lề</b> để chỉ cái gì nằm trong cái gì.</p>""",
          """Điều thứ tư, thân yêu cầu thường viết ở «JSON», gồm các cặp tên và giá trị trong ngoặc nhọn. Ở đây có ba cặp, số tiền là năm trăm nghìn.
          Điều thứ năm, đặc tả hôm nay viết ở «YAML». Cùng ba cặp đó, nhưng bỏ ngoặc và dùng thụt lề để chỉ cái gì nằm trong cái gì.""",
          focus=["1.1", "1.1", "1.2", ["1.2", 2]], clear=True),
    ], checks=["alg.bnk_retry_sim(2000000, 500000, 3, True) == 1500000",
               "len(__import__('json').loads('{\"fromAccount\": \"0123456789\", \"toAccount\": \"9876543210\", \"amount\": 500000}')) == 3"])

    sym = sc("sym", "symbol", "Giải mã các từ của một đặc tả", [
        S(table(["từ", "nghĩa"],
                [["OpenAPI", "<b>chuẩn</b> viết đặc tả API qua HTTP: có đường dẫn nào, nhận gì, trả gì (tên cũ: Swagger Specification)"],
                 ["Swagger", "<b>bộ công cụ</b> làm việc với chuẩn đó: Swagger Editor (soạn), Swagger UI (trang thử API), Swagger Codegen (sinh mã)"],
                 ["<code>paths</code>, <code>post</code>", "đường dẫn và phương thức"],
                 ["<code>requestBody</code>, <code>responses</code>", "thân yêu cầu; phản hồi theo từng mã trạng thái"],
                 ["<code>schema</code> (lược đồ)", "kiểu và ràng buộc của từng trường"]]),
          """Bảng này giải mã năm từ hay gặp trong một đặc tả. OpenAPI là một chuẩn, dùng để viết đặc tả cho API qua HTTP, nói có đường dẫn nào, nhận gì và trả gì. Tên cũ của chuẩn này có chữ Swagger.
          Còn Swagger ngày nay là bộ công cụ làm việc với chuẩn đó: trình soạn, trang thử API, và bộ sinh mã.
          Hai từ tiếp theo là đường dẫn và phương thức. Rồi thân yêu cầu, và phản hồi theo từng mã trạng thái. Cuối cùng, lược đồ là kiểu và ràng buộc của từng trường.""",
          focus=[0, "1.2", "1.2", "1.3", "1.4", "1.5", "1.6"]),
        S(table(["mảnh", "đọc là", "nghĩa"],
                [["<code>^</code>", "dấu mũ", "bắt đầu chuỗi"],
                 ["<code>[0-9]</code>", "một chữ số từ 0 đến 9", "đúng một ký tự là chữ số"],
                 ["<code>{10,19}</code>", "lặp từ 10 đến 19 lần", "dài 10 đến 19 chữ số"],
                 ["<code>$</code>", "dấu đô la", "kết thúc chuỗi: không thêm gì sau"]])
          + """<p class="note">Làm thử: <code>0123456789</code> (10 chữ số) khớp; <code>12345</code> (5) không khớp; <code>0123-456789</code> (có gạch) không khớp.</p>""",
          """Số tài khoản trong bài được tả bằng một mẫu chữ. Dấu mũ ở đầu mẫu nghĩa là bắt đầu chuỗi. Cặp ngoặc vuông không đến chín là đúng một chữ số.
          Cặp ngoặc nhọn mười, mười chín nghĩa là lặp từ mười đến mười chín lần. Dấu đô la ở cuối nghĩa là kết thúc chuỗi, không được thêm gì sau.
          Làm thử, chuỗi mười chữ số thì khớp. Chuỗi năm chữ số thì không khớp, vì ngắn hơn mười. Chuỗi có dấu gạch cũng không khớp, vì gạch không phải chữ số.""",
          focus=[0, "1.2", "1.3", "1.4", "1.5", 2, 2, 2], clear=True),
    ], checks=["alg.bnx_oas_match('0123456789') and not alg.bnx_oas_match('12345') and not alg.bnx_oas_match('0123-456789')",
               "len('0123456789') == 10 and len('12345') == 5"])

    intu = sc("intuition", "intuition", "Hình dung: hợp đồng ở giữa, mọi đội làm theo nó", [
        S(svg(1500, 470,
              box(560, 170, 380, 120, ["Đặc tả OpenAPI", "= hợp đồng"], C_PURPLE, size=28, bold=True),
              box(40, 50, 380, 110, ["Đội ứng dụng", "sinh mã gọi, máy chủ giả"], C_BLUE),
              box(1080, 50, 380, 110, ["Đội máy chủ", "sinh khung, bật kiểm lược đồ"], C_GREEN),
              box(40, 300, 380, 110, ["Kiểm thử", "sinh ca thử từ lược đồ"], C_AMBER),
              box(1080, 300, 380, 110, ["Đối tác", "đọc trang mô tả API"], C_GRAY),
              arrow(555, 200, 425, 130, "#9333ea"), arrow(945, 200, 1075, 130, "#9333ea"),
              arrow(555, 260, 425, 340, "#9333ea"), arrow(945, 260, 1075, 340, "#9333ea"),
              txt(750, 450, "Viết hợp đồng trước: bốn bên làm song song, không ai chờ ai", 26, "middle", "#1f2937", True)),
          """Hình đầu cho thấy vì sao viết hợp đồng trước. Bản đặc tả nằm ở giữa, làm điểm chung cho mọi bên. Đội ứng dụng sinh mã gọi và dựng máy chủ giả từ đặc tả, nên không phải chờ máy chủ thật.
          Đội máy chủ sinh khung mã và bật kiểm lược đồ. Người kiểm thử sinh ca thử từ lược đồ, còn đối tác đọc trang mô tả API.
          Bốn bên làm song song, vì ai cũng làm theo cùng một bản hợp đồng."""),
        S(svg(1500, 480,
              box(30, 180, 220, 100, ["Yêu cầu", "chuyển tiền"], C_BLUE, bold=True),
              box(330, 180, 260, 100, ["Kiểm", "lược đồ"], C_PURPLE, bold=True),
              box(330, 350, 260, 90, "400: trả ngay", C_RED),
              box(680, 180, 280, 100, ["Tra khoá", "lũy đẳng"], C_AMBER, bold=True),
              box(500, 30, 360, 90, "409: cùng khoá, đang xử lý dở", C_RED, size=22),
              box(900, 30, 380, 90, "422: cùng khoá, khác nội dung", C_RED, size=22),
              box(1050, 180, 220, 100, ["Trừ tiền", "ghi sổ"], C_GREEN, bold=True),
              box(1300, 190, 170, 80, "201", C_GREEN, size=30, bold=True),
              arrow(250, 230, 325, 230), arrow(590, 230, 675, 230, "#475569", "đúng"),
              arrow(460, 280, 460, 345, "#dc2626"), txt(520, 322, "sai", 22, "start", "#dc2626"),
              arrow(760, 180, 700, 125, "#dc2626"), arrow(880, 180, 1000, 125, "#dc2626"), arrow(960, 230, 1045, 230, "#475569", "mới"), arrow(1270, 230, 1295, 230),
              txt(750, 470, "Yêu cầu sai lược đồ bị chặn trước khi chạm vào tiền", 26, "middle", "#1f2937", True)),
          """Hình thứ hai là đường đi của một yêu cầu ở máy chủ. Bước đầu tiên ở máy chủ là kiểm yêu cầu theo lược đồ. Sai thì trả bốn trăm ngay, yêu cầu không chạm vào tiền.
          Nếu đúng lược đồ thì máy chủ tra khoá lũy đẳng. Cùng khoá mà yêu cầu trước còn đang xử lý dở thì trả bốn trăm linh chín. Cùng khoá mà khác nội dung thì trả bốn trăm hai mươi hai. Khoá mới thì trừ tiền, ghi sổ và trả hai trăm linh một."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: đọc đặc tả thành luật kiểm", [
        S(spec_part("head", "Bước 1. Có đường dẫn nào, phương thức nào")
          + """<span class='note'>Làm thử: <code>POST /transfers</code> có trong hợp đồng; <code>DELETE /transfers</code> không có, nên máy chủ không hứa gì về nó.</span>""",
          """Bước một, đặc tả mở đầu bằng phiên bản chuẩn và tên API. Dưới mục đường dẫn có đường chuyển tiền, dưới đó là phương thức P O S T.
          Vì hợp đồng chỉ hứa những gì được viết ra, nên đường dẫn hay phương thức không có ở đây thì người gọi không được trông vào. Làm thử, phương thức xoá trên cùng đường dẫn không có trong hợp đồng này.""",
          focus=[["2.1", "2.2", "2.3", "2.4"], ["2.5", "2.6", "2.7"], 2, 3]),
        S(spec_part("input", "Bước 2. Người gọi phải gửi gì")
          + """<span class='note'>Làm thử: yêu cầu thiếu phần đầu <code>Idempotency-Key</code> → 400, chưa cần xem thân.</span>""",
          """Bước hai, mục tham số nói phần đầu phải có khoá lũy đẳng, và chữ bắt buộc bằng đúng nghĩa là thiếu thì sai.
          Thân yêu cầu cũng bắt buộc, viết ở «JSON», và lược đồ của nó trỏ sang một lược đồ có tên ở cuối đặc tả. Vì cả hai đều bắt buộc, nên thiếu phần đầu là sai ngay.
          Làm thử, yêu cầu thiếu khoá lũy đẳng bị trả bốn trăm, máy chủ chưa cần đọc thân.""",
          focus=[["2.1", "2.2", "2.3", "2.4"], ["2.7", "2.8", "2.9", "2.10", "2.11", "2.12"], ["2.4", "2.8"], 3], clear=True),
        S(spec_part("schema1", "Bước 3. Lược đồ: trường nào bắt buộc, dạng gì")
          + """<span class='note'>Làm thử: <code>"0123456789"</code> là chuỗi, 10 chữ số → khớp.</span>""",
          """Bước ba, lược đồ chuyển khoản là một đối tượng. Danh sách bắt buộc gồm ba trường: tài khoản chuyển, tài khoản nhận và số tiền.
          Tài khoản chuyển phải là chuỗi khớp mẫu mười đến mười chín chữ số. Vì là chuỗi, nên số không ở đầu vẫn được giữ.
          Làm thử, chuỗi không một hai ba đến chín dài mười chữ số, nên khớp.""",
          focus=[["2.3", "2.4"], "2.5", ["2.7", "2.8", "2.9"], ["2.8", "2.9"], 3], clear=True),
        S(spec_part("schema2", "Bước 4. Tài khoản nhận và số tiền")
          + """<span class='note'>Làm thử: số tiền 0 nhỏ hơn 1 → sai; số tiền <code>"500000"</code> là chuỗi, không phải số nguyên → sai.</span>""",
          """Bước bốn, tài khoản nhận có cùng luật với tài khoản chuyển. Số tiền phải là số nguyên, và giá trị nhỏ nhất là một, vì chuyển không đồng là vô nghĩa.
          Làm thử, số tiền bằng không thì sai. Số tiền năm trăm nghìn viết trong dấu nháy là chuỗi, cũng sai, đúng lỗi của hai đội lúc đầu bài.""",
          focus=[["2.1", "2.2", "2.3"], ["2.4", "2.5", "2.6"], 3, 3], clear=True),
        S(spec_part("resp", "Bước 5. Người gọi phải xử lý những phản hồi nào")
          + """<p class='note'>Làm thử: 4 mã → ứng dụng viết đúng 4 nhánh. 409, 422 theo bản nháp IETF về Idempotency-Key (bản 08).</p>""",
          """Bước năm, mục phản hồi liệt kê bốn mã. Hai trăm linh một là đã tạo lệnh, bốn trăm là sai lược đồ.
          Hai mã cuối theo bản nháp chuẩn về khoá lũy đẳng của tổ chức chuẩn hoá giao thức mạng. Bốn trăm linh chín là yêu cầu cùng khoá còn đang xử lý dở, bốn trăm hai mươi hai là cùng khoá mà khác nội dung.
          Vì các mã được viết sẵn, người gọi biết trước phải xử lý những trường hợp nào. Làm thử, bốn mã thì ứng dụng viết đúng bốn nhánh.""",
          focus=["2.1", ["2.2", "2.3", "2.4", "2.5"], 3, ["2.6", "2.7", "2.8", "2.9"], 2, 3], clear=True),
        S("""<p><b>Bước 6. Luật đổi hợp đồng.</b> Hợp đồng đã có người dùng. Một thay đổi là <b class="green">tương thích</b> khi:</p>
<div class="box key">mọi yêu cầu cũ hợp lệ vẫn hợp lệ, <b>và</b> mọi máy khách cũ vẫn đọc được phản hồi mới.</div>
<span class='note'>Làm thử: thêm trường bắt buộc <code>purpose</code> vào yêu cầu → yêu cầu 1 hợp lệ ở hợp đồng cũ thành 400 → <b class="red">phá vỡ</b>.</span>""",
          """Bước sáu là luật khi cần đổi một hợp đồng đã có. Hợp đồng đã có người dùng, nên một thay đổi chỉ là tương thích khi mọi yêu cầu cũ hợp lệ vẫn hợp lệ, và mọi máy khách cũ vẫn đọc được phản hồi mới.
          Làm thử, thêm một trường bắt buộc mới vào yêu cầu. Yêu cầu cũ không có trường đó, nên từ hợp lệ thành bốn trăm. Vậy thêm trường bắt buộc vào yêu cầu là thay đổi phá vỡ.""",
          focus=[1, 2, 3, 3, 3], clear=True),
    ], checks=["alg.bnx_oas_match('0123456789')", "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': 0}) == ['amount: nhỏ hơn 1']",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': '500000'}) == ['amount: sai kiểu']",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0 and alg.bnx_oas_old_valid_after([]) == 1"])

    ex = sc("example", "example", "Ví dụ ba yêu cầu thử, từng phép tính", [
        S(table(["yêu cầu", "fromAccount", "toAccount", "amount"],
                [["1", "0123456789", "9876543210", "500000"], ["2", "0123456789", "9876543210", "0"], ["3", "0123456789", "(không có)", "500000"]])
          + """<p><b>①</b> Yêu cầu 1, hai tài khoản: <code>len("0123456789") = 10</code>, <code>len("9876543210") = 10</code>; 10 nằm trong 10–19 → <b class="green">khớp cả hai</b>.</p>""",
          """Ta kiểm ba yêu cầu thử bằng tay. Bảng dưới đây ghi lại đủ ba yêu cầu thử. Yêu cầu một và hai giống nhau, chỉ khác số tiền. Yêu cầu ba không có tài khoản nhận.
          Phép tính thứ nhất, ta xét yêu cầu thử số một. Hai số tài khoản đều là chuỗi dài mười chữ số. Mười nằm trong khoảng mười đến mười chín, nên cả hai đều khớp.""",
          focus=[0, 1, ["1.2", "1.3"], "1.4", 2, 2, 2]),
        S("""<p><b>②</b> Yêu cầu 1, số tiền: <code>500000</code> là số nguyên và lớn hơn 1. Có đủ 3/3 trường bắt buộc → <b class="green">0 lỗi → 201</b>.</p>""",
          """Phép tính thứ hai, số tiền năm trăm nghìn là số nguyên và lớn hơn một. Đủ ba trên ba trường bắt buộc, nên không có lỗi nào, máy chủ trả hai trăm linh một."""),
        S("""<p><b>③</b> Yêu cầu 2: hai tài khoản giống yêu cầu 1, dùng lại kết quả ① → khớp. Số tiền <code>0</code> nhỏ hơn 1 → <b class="red">1 lỗi, trường amount → 400</b>.</p>""",
          """Phép tính thứ ba, ta xét yêu cầu thử số hai. Hai tài khoản giống yêu cầu một, nên dùng lại kết quả phép thứ nhất là khớp. Số tiền bằng không, nhỏ hơn một, nên có một lỗi ở trường số tiền, trả bốn trăm."""),
        S("""<p><b>④</b> Yêu cầu 3: có 2 trong 3 trường bắt buộc, thiếu 3 − 2 = 1 trường là <code>toAccount</code> → <b class="red">1 lỗi → 400</b>.</p>""",
          """Phép tính thứ tư, yêu cầu ba có hai trong ba trường bắt buộc. Ba trừ hai bằng một, nên thiếu đúng một trường, là tài khoản nhận. Máy chủ trả bốn trăm và nêu tên trường đó."""),
        S("""<p><b>⑤</b> Tổng hợp: 1 yêu cầu được 201, 2 yêu cầu bị 400. Chỉ 1 trong 3 yêu cầu đi tới bước trừ tiền.</p>"""
          + table(["yêu cầu", "số lỗi", "trường sai", "mã"], [["1", "0", "—", "201"], ["2", "1", "amount", "400"], ["3", "1", "toAccount", "400"]]),
          """Phép tính thứ năm, ta tổng hợp lại cả ba yêu cầu. Một yêu cầu được hai trăm linh một, hai yêu cầu bị bốn trăm. Vậy chỉ một trong ba yêu cầu đi tới bước trừ tiền, hai yêu cầu sai bị chặn ở cửa.""",
          focus=[1, 2, 1], clear=True),
    ], checks=["len('0123456789') == 10 and len('9876543210') == 10 and alg.bnx_oas_match('0123456789') and alg.bnx_oas_match('9876543210')",
               "[s for s, _ in alg.bnx_oas_batch()] == [201, 400, 400]",
               "[len(e) for _, e in alg.bnx_oas_batch()] == [0, 1, 1]",
               "alg.bnx_oas_batch()[1][1][0].startswith('amount') and alg.bnx_oas_batch()[2][1][0].startswith('toAccount')",
               "3 - len({'fromAccount', 'amount'}) == 1"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cho máy kiểm lại", [
        S(code(VALIDATE_PY, "Chương trình Python kiểm theo lược đồ", lines=VALIDATE_PARTS["ham"]),
          """Bây giờ ta tự kiểm lại bằng một đường khác. Ta viết một chương trình Python nhỏ làm đúng các luật của lược đồ. Mẫu số tài khoản được chép nguyên văn từ đặc tả, vì máy phải kiểm đúng luật đã hứa.
          Hàm kiểm trước hết liệt kê trường bắt buộc nào thiếu, kể cả trường có tên mà giá trị rỗng. Dòng này là cách viết gọn của Python: duyệt từng tên bắt buộc và giữ lại tên nào thiếu.
          Sau đó với hai tài khoản, giá trị phải là chuỗi và khớp trọn mẫu, vì dấu đô la của Python vẫn cho lọt một ký tự xuống dòng ở cuối. Cuối cùng nó gọi hàm kiểm số tiền.""",
          focus=[0, 2, "2.2", ["2.5", "2.6"], "2.6", ["2.7", "2.8", "2.9", "2.10"], "2.11"]),
        S(code(VALIDATE_PY, "(tiếp) Kiểm số tiền, rồi chạy ba yêu cầu thử", lines=VALIDATE_PARTS["thu"]),
          """Hàm kiểm số tiền đòi một số nguyên lớn hơn hoặc bằng một. Nếu không có số tiền thì hàm bỏ qua, vì phần trên đã báo thiếu.
          Rồi ta gán hai số tài khoản cho hai biến trong cùng một dòng, chạy ba yêu cầu thử y như bảng lúc nãy, đánh số từ một, và in mã trạng thái cùng danh sách lỗi.""",
          focus=[["2.1", "2.2", "2.3"], "2.2", ["2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        S(out(VALIDATE_OUT),
          """Đây là kết quả chạy thật của chương trình trên máy. Yêu cầu một được hai trăm linh một, không lỗi. Yêu cầu hai bị bốn trăm ở trường số tiền. Yêu cầu ba bị bốn trăm vì thiếu tài khoản nhận.
          Kết quả khớp đúng năm phép tính tay ở trên.""",
          focus=[0, "2.1", "2.2", "2.3", 0], clear=True),
        S(table(["thay đổi", "ở đâu", "luật ở bước 6", "loại"],
                [["thêm trường tuỳ chọn <code>fee</code>", "phản hồi", "nếu máy khách cũ được cấu hình bỏ qua trường lạ (Jackson thuần mặc định báo lỗi; Spring tắt lỗi này)", "<b class='green'>tương thích</b>"],
                 ["thêm trường bắt buộc <code>purpose</code>", "yêu cầu", "yêu cầu cũ thiếu nó → 400", "<b class='red'>phá vỡ</b>"],
                 ["đổi <code>amount</code> từ số nguyên sang chuỗi", "yêu cầu", "yêu cầu cũ gửi số → sai kiểu", "<b class='red'>phá vỡ</b>"],
                 ["xoá trường <code>toAccount</code> khỏi phản hồi", "phản hồi", "máy khách cũ đang đọc nó", "<b class='red'>phá vỡ</b>"]]),
          """Bảng này áp luật đổi hợp đồng cho bốn thay đổi. Thêm một trường tuỳ chọn vào phản hồi là tương thích, với điều kiện máy khách cũ được cấu hình bỏ qua trường lạ. Thư viện đọc JSON phổ biến của Java mặc định báo lỗi khi gặp trường lạ, còn Spring tắt lỗi đó đi.
          Thêm trường bắt buộc vào yêu cầu là phá vỡ, vì yêu cầu cũ thiếu nó. Đổi số tiền từ số nguyên sang chuỗi là phá vỡ, vì yêu cầu cũ gửi số.
          Xoá một trường khỏi phản hồi cũng là phá vỡ, vì máy khách cũ đang đọc trường đó.""",
          focus=[0, "1.2", "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["[s for s, _ in alg.bnx_oas_batch()] == [201, 400, 400]",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': None, 'amount': None}) == ['toAccount: sai kiểu', 'amount: sai kiểu'] and not alg.bnx_oas_match('0123456789\\n')",
               "alg.bnx_oas_change({'required': ['id'], 'properties': {'id': {'type': 'string'}}}, {'required': ['id'], 'properties': {'id': {'type': 'string'}, 'fee': {'type': 'integer'}}}, 'response') == 'tương thích'",
               "alg.bnx_oas_change({'required': ['amount'], 'properties': {'amount': {'type': 'integer'}}}, {'required': ['amount', 'purpose'], 'properties': {'amount': {'type': 'integer'}, 'purpose': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_change({'properties': {'amount': {'type': 'integer'}}}, {'properties': {'amount': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_change({'properties': {'id': {'type': 'string'}, 'toAccount': {'type': 'string'}}}, {'properties': {'id': {'type': 'string'}}}, 'response') == 'phá vỡ'"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nói “viết API bằng Swagger 3”. <b>OpenAPI là chuẩn đặc tả</b>; <b>Swagger là bộ công cụ</b> làm việc với chuẩn đó.
<br><span class="note">Lịch sử: chuẩn tên cũ là Swagger Specification; năm 2015 bản Swagger 2.0 được trao cho tổ chức OpenAPI Initiative. Bài này dùng OpenAPI 3.0.3.</span></div>""",
          """Lỗi thứ nhất, của người mới, là gọi đặc tả là Swagger ba. OpenAPI mới là chuẩn đặc tả, còn Swagger là bộ công cụ làm việc với chuẩn đó.
          Sự nhầm lẫn có lý do lịch sử. Chuẩn này trước kia mang tên Swagger, đến năm hai nghìn không trăm mười lăm thì được trao cho một tổ chức mới và đổi tên thành OpenAPI."""),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Đặc tả viết đẹp, trang mô tả API chạy tốt, nhưng máy chủ <b class="red">không bật kiểm lược đồ</b>. Yêu cầu số tiền 0 vẫn lọt vào bước trừ tiền.
<br><span class="note">Đặc tả không tự kiểm dữ liệu. Phải bật bộ kiểm ở máy chủ, và có ca thử gửi yêu cầu sai để chắc nó trả 400.</span></div>""",
          """Lỗi thứ hai, của người đã đi làm. Đặc tả viết đẹp, trang mô tả API chạy tốt, nhưng máy chủ không bật kiểm lược đồ. Yêu cầu số tiền bằng không vẫn lọt vào bước trừ tiền.
          Đặc tả chỉ là văn bản, nó không tự kiểm dữ liệu. Phải bật bộ kiểm ở máy chủ, và viết ca thử gửi yêu cầu sai để chắc máy chủ trả bốn trăm."""),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Thêm trường bắt buộc <code>purpose</code> vào yêu cầu rồi nghĩ “chỉ là thêm, không sao”. Mọi đối tác chưa cập nhật nhận <b class="red">400</b>.
<br><span class="note">Cách chữa: thêm trường <b>tuỳ chọn</b> có giá trị mặc định; muốn bắt buộc thì ra phiên bản mới và báo trước cho đối tác.</span></div>""",
          """Lỗi thứ ba, cũng của người đã đi làm. Thêm một trường bắt buộc vào yêu cầu rồi nghĩ chỉ là thêm, không sao. Mọi đối tác chưa cập nhật lập tức nhận bốn trăm.
          Cách chữa là thêm trường đó ở dạng tuỳ chọn có giá trị mặc định. Muốn bắt buộc thì ra một phiên bản mới và báo trước cho đối tác."""),
    ], checks=["alg.bnx_oas_status({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': 0}) == 400",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "Yêu cầu: fromAccount <code>\"0123456789\"</code>, toAccount <code>\"12345678901234567890\"</code> (20 chữ số), amount <code>100000</code>. Mã trạng thái nào? Trường nào sai?"],
                 ["2", "Phân loại: (a) thêm trường tuỳ chọn <code>createdAt</code> vào phản hồi 201; (b) đổi amount từ số nguyên sang chuỗi."],
                 ["3", "Quyết định: cần thêm trường bắt buộc <code>purpose</code> (nội dung chuyển khoản), đã có 5 đối tác đang gọi (số minh hoạ). Sửa ngay đường cũ, hay làm cách khác?"]]),
          """Bây giờ tới phần bạn tự làm bài. Câu một, tài khoản nhận dài hai mươi chữ số, số tiền một trăm nghìn. Máy chủ trả mã nào, và trường nào sai?
          Câu hai, bạn hãy phân loại hai thay đổi sau đây. Một là thêm trường tuỳ chọn vào phản hồi. Hai là đổi số tiền từ số nguyên sang chuỗi.
          Câu ba là một quyết định có đánh đổi rõ ràng. Cần thêm trường nội dung chuyển khoản là bắt buộc, trong khi đã có năm đối tác đang gọi. Hãy dừng video lại và tự làm ra giấy trước.""",
          pause=25, focus=[0, "1.2", "1.2", "1.3", "1.3", "1.3", "1.4", "1.4", 0]),
        S("""<p>Câu 1: <code>len("12345678901234567890") = 20</code>, lớn hơn 19 → không khớp mẫu.</p>
<div class="box key">Trường sai: <b>toAccount</b> → máy chủ trả <b class="red">400</b>. Tài khoản chuyển và số tiền đều đúng.</div>""",
          """Bây giờ ta xem đáp án của câu một. Chuỗi tài khoản nhận dài hai mươi chữ số, lớn hơn mười chín, nên không khớp mẫu. Trường sai là tài khoản nhận, máy chủ trả bốn trăm. Hai trường còn lại của yêu cầu này đều đúng.""",
          focus=[0, 1, 2, 2]),
        S(table(["thay đổi", "lý do", "loại"],
                [["(a) thêm <code>createdAt</code> tuỳ chọn ở phản hồi", "máy khách cũ bỏ qua trường lạ (khi được cấu hình như vậy)", "<b class='green'>tương thích</b>"],
                 ["(b) amount: số nguyên → chuỗi", "yêu cầu cũ gửi số nguyên bị báo sai kiểu", "<b class='red'>phá vỡ</b>"]]),
          """Bây giờ ta xem đáp án của câu hai. Thêm trường tuỳ chọn vào phản hồi là tương thích, nếu máy khách cũ được cấu hình bỏ qua trường lạ. Đổi kiểu số tiền là phá vỡ, vì yêu cầu cũ gửi số nguyên sẽ bị báo sai kiểu.""",
          focus=[0, "1.2", "1.3"]),
        S(table(["lựa chọn", "được", "mất"],
                [["sửa ngay đường cũ, <code>purpose</code> bắt buộc", "một phiên bản, mã gọn", "5 đối tác nhận 400 tới khi họ sửa xong"],
                 ["đường cũ: <code>purpose</code> tuỳ chọn, có mặc định; bắt buộc ở <code>/v2/transfers</code>, báo trước thời hạn", "không ai gãy; đối tác chuyển dần", "phải chạy và kiểm hai phiên bản trong một thời gian"]]),
          """Bây giờ ta xem đáp án của câu ba. Sửa ngay đường cũ thì chỉ có một phiên bản và mã gọn, nhưng năm đối tác nhận bốn trăm cho tới khi họ sửa xong.
          Cách thứ hai giữ trường đó tuỳ chọn ở đường cũ, có giá trị mặc định, và chỉ bắt buộc ở phiên bản hai, có báo trước thời hạn.
          Không ai bị gãy và đối tác chuyển dần. Đổi lại, đội phải chạy và kiểm hai phiên bản trong một thời gian.""",
          focus=[0, "1.2", "1.3", "1.3", "1.3"]),
    ], checks=["len('12345678901234567890') == 20 and not alg.bnx_oas_match('12345678901234567890')",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '12345678901234567890', 'amount': 100000}) == ['toAccount: sai dạng']",
               "alg.bnx_oas_change({'properties': {'id': {'type': 'string'}}}, {'properties': {'id': {'type': 'string'}, 'createdAt': {'type': 'string'}}}, 'response') == 'tương thích'",
               "alg.bnx_oas_change({'properties': {'amount': {'type': 'integer'}}}, {'properties': {'amount': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("viết đặc tả trước", "các đội làm song song", "máy chủ kiểm lược đồ", "yêu cầu sai trả 400", "đổi hợp đồng theo luật tương thích"),
          """Ta tổng kết lại chuỗi logic của cả bài. Viết đặc tả trước, nên các đội làm song song. Máy chủ bật kiểm lược đồ, nên yêu cầu sai bị trả bốn trăm trước khi chạm tiền.
          Và mỗi lần đổi hợp đồng, ta hỏi xem yêu cầu cũ và máy khách cũ có còn chạy không."""),
        S("""<div class='box key'><b>Tư duy:</b> đặc tả API là <b>lời hứa</b> với người gọi. Thêm điều hứa thường thì được; rút lại hay siết chặt điều đã hứa là làm gãy người khác.
<br><span class="note">Ngoại lệ: thêm giá trị mới vào một trường liệt kê (<code>enum</code>) của phản hồi làm gãy máy khách đọc chặt danh sách giá trị.</span></div>
<p class="note">Bài sau: cùng ý tưởng hợp đồng trước, nhưng bản tin là dãy byte nhị phân thay cho chữ.</p>""",
          """Đây là điều cần mang theo sau bài này. Đặc tả API là lời hứa với người gọi. Thêm điều hứa thường thì được, còn rút lại hay siết chặt điều đã hứa là làm gãy người khác. Có một ngoại lệ hay gặp: thêm giá trị mới vào một trường liệt kê của phản hồi sẽ làm gãy máy khách đọc chặt danh sách giá trị.
          Ở bài sau, ta giữ ý tưởng viết hợp đồng trước, nhưng bản tin là một dãy byte nhị phân thay cho chữ.""",
          focus=[1, 1, 1, 1, 2], forward_ref=True),
    ])
    return lesson("L01", "openapi_hop_dong_api", "Bài 1 — OpenAPI (Swagger): đặc tả API là hợp đồng, viết trước khi viết mã",
                  "curriculum/bnx.yaml L01; audit/bnx/verify_bnx.py L01; OpenAPI Specification 3.0.3 (spec.openapis.org, đọc 2026-11-11); "
                  "swagger.io/docs/specification/v3_0/about (đọc 2026-11-11)",
                  ["Đọc một đặc tả OpenAPI 3: đường dẫn, phương thức, thân yêu cầu, phản hồi, lược đồ", "Kiểm một yêu cầu theo lược đồ và chỉ ra trường sai",
                   "Phân biệt thay đổi tương thích và thay đổi phá vỡ hợp đồng", "Giải thích lợi ích của cách làm hợp đồng trước"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
