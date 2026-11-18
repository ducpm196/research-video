import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene  # noqa: F401
from l03 import _merge_short  # ghép câu < 8 từ vào câu bên cạnh (máy nghe gắn cờ câu ngắn)

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

# Cảnh quy mô (AF2): lô N yêu cầu có tỉ lệ sai cố định (cứ 50 yêu cầu có 1 số tiền 0, cứ 80 yêu cầu có 1 thiếu tài khoản nhận);
# chạy với hàm kiem của khối trên (prelude_keys ở sổ). Số minh hoạ: tỉ lệ sai.
SCALE_PY = """def lo(n):                      # lô n yêu cầu, một phần bị sai
    chan = 0
    for i in range(1, n + 1):
        req = {"fromAccount": A, "toAccount": B, "amount": 500000}
        if i % 50 == 0:
            req["amount"] = 0
        if i % 80 == 0:
            del req["toAccount"]
        chan += bool(kiem(req))
    return chan
for n in (1000, 100000):
    print(n, "yeu cau:", lo(n), "bi chan")
"""
SCALE_OUT = """1000 yeu cau: 30 bi chan
100000 yeu cau: 3000 bi chan"""

# Lab labs/BNX/L01 (số liệu KHÁC bài: lược đồ rút tiền ATM, chuỗi lỗi ASCII quy ước trong de.md)
LAB_PY = '''
import re

THE = re.compile(r"^[0-9]{16}$")


def kiem(req):
    loi = []
    v = req.get("soThe")
    if v is None:
        loi.append("soThe: thieu")
    elif not (type(v) is str and THE.fullmatch(v)):
        loi.append("soThe: sai dang")
    t = req.get("soTien")
    if t is None:
        loi.append("soTien: thieu")
    elif not (type(t) is int and t >= 50000):
        loi.append("soTien: phai la so nguyen >= 50000")
    return loi


thu = [
    {"soThe": "1234567890123456", "soTien": 200000},
    {"soThe": "123456", "soTien": 200000},
    {"soThe": "1234567890123456", "soTien": 20000},
    {"soThe": "1234567890123456", "soTien": "200000"},
    {"soTien": 200000},
]
for i, req in enumerate(thu, 1):
    loi = kiem(req)
    print(i, 400 if loi else 201, "; ".join(loi) or "-")
'''
LAB_OUT = """1 201 -
2 400 soThe: sai dang
3 400 soTien: phai la so nguyen >= 50000
4 400 soTien: phai la so nguyen >= 50000
5 400 soThe: thieu"""

LAB_DE = """# Lab BNX L01 — Kiểm một yêu cầu rút tiền theo lược đồ

Một API rút tiền tại máy ATM có lược đồ yêu cầu (số minh hoạ):

| trường | bắt buộc | luật |
|---|---|---|
| `soThe` | có | chuỗi đúng 16 chữ số |
| `soTien` | có | số nguyên, từ 50000 trở lên |

Viết `mau.py` (Python) gồm hàm `kiem(req)` trả về **danh sách lỗi** (rỗng nếu hợp lệ), dùng đúng các chuỗi lỗi sau (không dấu):

- thiếu số thẻ: `soThe: thieu`; sai dạng (không phải chuỗi 16 chữ số): `soThe: sai dang`
- thiếu số tiền: `soTien: thieu`; không phải số nguyên hoặc nhỏ hơn 50000: `soTien: phai la so nguyen >= 50000`

Với số thẻ dùng `re.fullmatch` trên chuỗi, kiểm `type(v) is str` trước. Với số tiền kiểm `type(t) is int` (chuỗi `"200000"` là sai kiểu).

Sau hàm, chép nguyên văn đoạn chạy năm yêu cầu thử:

```python
thu = [
    {"soThe": "1234567890123456", "soTien": 200000},
    {"soThe": "123456", "soTien": 200000},
    {"soThe": "1234567890123456", "soTien": 20000},
    {"soThe": "1234567890123456", "soTien": "200000"},
    {"soTien": 200000},
]
for i, req in enumerate(thu, 1):
    loi = kiem(req)
    print(i, 400 if loi else 201, "; ".join(loi) or "-")
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L01 mau.py`.
"""

# Từ ngoại trong lời đọc: chỉ dùng khi đã dò phát âm (BRIEF mục 6). Chưa dò → nói bằng tiếng Việt, tên gốc chỉ trên màn hình.
SAY_WORDS = {"«JSON»": "JSON", "«YAML»": "YAML"}   # JSON, YAML: dò ASR 8/8 (audit/bnx/probes/x1.md), luật đọc ở lexicon_vi.BNX.yaml


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


def spec_part(name, title=None):
    return code(SPEC_YAML, title, lines=SPEC_PARTS[name])


def build():
    write_lab("BNX", "L01", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Hai đội làm mười ngày, ghép lại thì mọi yêu cầu bị từ chối", [
        S("""<p>Đội ứng dụng và đội máy chủ cùng làm tính năng chuyển tiền trong <b>10 ngày</b> (số minh hoạ). Không ai viết ra yêu cầu trông thế nào.</p>"""
          + table(["chỗ", "ứng dụng gửi", "máy chủ chờ"],
                  [["tên trường tài khoản nhận", "<code>to</code>", "<code>toAccount</code>"],
                   ["số tiền", "<code>\"500000\"</code> (chuỗi)", "<code>500000</code> (số nguyên)"]])
          + """<div class="box warn">Ngày ghép nối: máy chủ trả <b class="red">400</b> cho mọi yêu cầu.</div>""",
          """Chào bạn, hai đội cùng làm tính năng chuyển tiền trong mười ngày, số minh hoạ, và không ai viết ra yêu cầu trông thế nào.
          Ứng dụng đặt tên trường một kiểu, máy chủ chờ kiểu khác, và ứng dụng gửi số tiền dưới dạng chuỗi chữ còn máy chủ chờ số nguyên.
          Ngày ghép nối, máy chủ trả mã bốn trăm cho mọi yêu cầu.""",
          focus=[1, ["2.2", "2.3"], 3]),
        S(table(["câu hỏi", "bài này trả lời"],
                [["viết hợp đồng API thế nào", "đặc tả OpenAPI: đường dẫn, phương thức, thân yêu cầu, phản hồi, lược đồ"],
                 ["kiểm một yêu cầu ra sao", "so từng trường với lược đồ, chỉ ra trường sai"],
                 ["lưu lượng tăng thì sao", "đo thật: số yêu cầu sai bị chặn ở cửa khi lô lớn dần"],
                 ["sửa hợp đồng mà không làm gãy ai", "phân biệt thay đổi tương thích và thay đổi phá vỡ"]]),
          """Hôm nay ta trả lời bốn câu hỏi. Viết hợp đồng cho API thế nào, bằng chuẩn OpenAPI. Kiểm một yêu cầu ra sao, khi lưu lượng tăng thì chuyện gì xảy ra, và sửa hợp đồng thế nào để không làm gãy ai.""",
          focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_oas_status({'fromAccount': '0123456789', 'to': '9876543210', 'amount': '500000'}) == 400",
               "sorted(alg.bnx_oas_errors({'fromAccount': '0123456789', 'to': '9876543210', 'amount': '500000'})) == ['amount: sai kiểu', 'toAccount: thiếu']"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① API, yêu cầu HTTP", "<b>API</b>: danh sách việc một dịch vụ cho chương trình khác (máy khách) nhờ làm. Một yêu cầu HTTP gồm phương thức và đường dẫn, phần đầu (các cặp tên: giá trị), rồi thân", "<code>POST /transfers</code>"],
                 ["② Mã trạng thái", "2xx là thành công, 4xx là lỗi của người gọi", "201 đã tạo, 400 yêu cầu sai, 409 xung đột, 422 không xử lý được"],
                 ["③ Khoá lũy đẳng", "mã người gọi gửi kèm mọi lần thử; cùng khoá thì máy chủ chỉ làm một lần", "thử 3 lần, chỉ trừ tiền 1 lần"]]),
          """Trước hết ta cần hiểu năm điều. API là danh sách việc một dịch vụ cho chương trình khác nhờ làm, và yêu cầu HTTP gồm phương thức, đường dẫn, phần đầu rồi thân.
          Mã trạng thái bắt đầu bằng hai là thành công, bắt đầu bằng bốn là lỗi của người gọi, như bốn trăm là yêu cầu sai.
          Khoá lũy đẳng là mã người gọi gửi kèm mọi lần thử, nên thử ba lần thì máy chủ vẫn chỉ trừ tiền một lần.""",
          focus=[0, "1.2", "1.3", "1.4"]),
        S("""<div class="row"><div class="col">"""
          + code(BODY_JSON, "④ Thân yêu cầu dạng JSON") + """</div><div class="col">"""
          + code(BODY_YAML, "⑤ Cùng dữ liệu, viết dạng YAML") + """</div></div>
<p class="note">Cả hai đều là 3 cặp tên: giá trị. YAML bỏ ngoặc, dùng <b>thụt lề</b> để chỉ cái gì nằm trong cái gì.</p>""",
          """Điều thứ tư, thân yêu cầu thường viết ở «JSON», gồm các cặp tên và giá trị trong ngoặc nhọn. Ở đây có ba cặp, số tiền là năm trăm nghìn.
          Điều thứ năm, đặc tả hôm nay viết ở «YAML». Cùng ba cặp đó, bỏ ngoặc, và thụt lề chỉ cái nằm trong cái.""",
          focus=["1.1", "1.1", "1.2", ["1.2", 2]], clear=True),
    ], checks=["alg.bnk_retry_sim(2000000, 500000, 3, True) == 1500000",
               "len(__import__('json').loads('{\"fromAccount\": \"0123456789\", \"toAccount\": \"9876543210\", \"amount\": 500000}')) == 3"])

    sym = sc("sym", "symbol", "Giải mã các từ của một đặc tả", [
        S(table(["từ", "nghĩa"],
                [["OpenAPI", "<b>chuẩn</b> viết đặc tả API qua HTTP: có đường dẫn nào, nhận gì, trả gì (tên cũ: Swagger Specification)"],
                 ["Swagger", "<b>bộ công cụ</b> làm việc với chuẩn đó: soạn đặc tả, trang thử API, sinh mã"],
                 ["<code>paths</code>, <code>post</code>", "đường dẫn và phương thức"],
                 ["<code>requestBody</code>, <code>responses</code>", "thân yêu cầu; phản hồi theo từng mã trạng thái"],
                 ["<code>schema</code> (lược đồ)", "kiểu và ràng buộc của từng trường"]]),
          """Năm từ hay gặp trong một đặc tả. OpenAPI là chuẩn viết đặc tả API qua HTTP, nói có đường dẫn nào, nhận gì và trả gì, còn Swagger là bộ công cụ làm việc với chuẩn đó.
          Rồi đến đường dẫn và phương thức, thân yêu cầu và phản hồi theo từng mã trạng thái. Cuối cùng, lược đồ là kiểu và ràng buộc của từng trường.""",
          focus=[["1.1", "1.2"], "1.3", "1.4", "1.5", "1.6"]),
        S(table(["mảnh", "đọc là", "nghĩa"],
                [["<code>^</code>", "dấu mũ", "bắt đầu chuỗi"],
                 ["<code>[0-9]</code>", "một chữ số từ 0 đến 9", "đúng một ký tự là chữ số"],
                 ["<code>{10,19}</code>", "lặp từ 10 đến 19 lần", "dài 10 đến 19 chữ số"],
                 ["<code>$</code>", "dấu đô la", "kết thúc chuỗi: không thêm gì sau"]])
          + """<p class="note">Làm thử: <code>0123456789</code> (10 chữ số) khớp; <code>12345</code> (5) không khớp; <code>0123-456789</code> (có gạch) không khớp.</p>""",
          """Số tài khoản được tả bằng một mẫu chữ. Dấu mũ nghĩa là bắt đầu chuỗi, ngoặc vuông là đúng một chữ số, ngoặc nhọn là lặp từ mười đến mười chín lần, và dấu đô la là kết thúc chuỗi.
          Làm thử, chuỗi mười chữ số thì khớp. Chuỗi năm chữ số, hay chuỗi có dấu gạch, thì không khớp.""",
          focus=[0, "1.2", "1.3", "1.4", "1.5", 2, 2], clear=True),
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
          """Hình đầu cho thấy vì sao viết hợp đồng trước. Bản đặc tả ở giữa làm điểm chung, đội ứng dụng dựng máy chủ giả từ nó, tức chương trình đóng vai máy chủ để thử, nên khỏi chờ máy chủ thật.
          Các bên còn lại cũng dùng chung bản đặc tả, nên bốn bên làm song song."""),
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
          """Hình thứ hai là đường đi của một yêu cầu. Trước hết kiểm lược đồ, sai thì trả bốn trăm ngay.
          Nếu đúng thì tra khoá lũy đẳng. Cùng khoá mà còn xử lý dở thì trả bốn trăm linh chín, cùng khoá mà khác nội dung thì bốn trăm hai mươi hai, còn khoá mới thì trừ tiền và trả hai trăm linh một."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: đọc đặc tả thành luật kiểm", [
        S(spec_part("head", "Bước 1. Có đường dẫn nào, phương thức nào")
          + """<span class='note'>Làm thử: <code>POST /transfers</code> có trong hợp đồng; <code>DELETE /transfers</code> không có, nên máy chủ không hứa gì về nó.</span>""",
          """Bước một, đặc tả mở đầu bằng phiên bản chuẩn và tên API. Dưới mục đường dẫn có đường chuyển tiền, dưới đó là phương thức P O S T.
          Hợp đồng chỉ hứa điều được viết ra, nên phương thức xoá không có thì người gọi đừng trông vào.""",
          focus=[["2.1", "2.2", "2.3", "2.4"], ["2.5", "2.6", "2.7"], 3]),
        S(spec_part("input", "Bước 2. Người gọi phải gửi gì")
          + """<span class='note'>Làm thử: yêu cầu thiếu phần đầu <code>Idempotency-Key</code> → 400, chưa cần xem thân. <code>application/json</code> là tên <b>kiểu nội dung</b>: thân yêu cầu viết bằng JSON.</span>""",
          """Bước hai, mục tham số nói phần đầu phải có khoá lũy đẳng, và bắt buộc nghĩa là thiếu thì sai. Thân yêu cầu cũng bắt buộc, kiểu nội dung ghi trên màn hình nghĩa là viết ở «JSON», và lược đồ của nó trỏ sang lược đồ có tên ở cuối đặc tả.
          Làm thử, yêu cầu thiếu khoá lũy đẳng bị trả bốn trăm, chưa cần đọc thân.""",
          focus=[["2.1", "2.2", "2.3", "2.4"], ["2.7", "2.8", "2.9", "2.10", "2.11", "2.12"], ["2.4", "2.8"]], clear=True),
        S(spec_part("schema1", "Bước 3. Lược đồ: trường nào bắt buộc, dạng gì")
          + """<span class='note'>Làm thử: <code>"0123456789"</code> là chuỗi, 10 chữ số → khớp.</span>""",
          """Bước ba, lược đồ chuyển khoản là một đối tượng với ba trường bắt buộc: tài khoản chuyển, tài khoản nhận và số tiền. Tài khoản chuyển phải là chuỗi mười đến mười chín chữ số, và vì là chuỗi nên số không ở đầu vẫn được giữ.""",
          focus=[["2.3", "2.4"], ["2.7", "2.8", "2.9"]], clear=True),
        S(spec_part("schema2", "Bước 4. Tài khoản nhận và số tiền")
          + """<span class='note'>Làm thử: số tiền 0 nhỏ hơn 1 → sai; số tiền <code>"500000"</code> là chuỗi, không phải số nguyên → sai.</span>""",
          """Bước bốn, tài khoản nhận có cùng luật, còn số tiền phải là số nguyên nhỏ nhất là một, vì chuyển không đồng là vô nghĩa.
          Làm thử, số tiền bằng không thì sai, và số tiền viết trong dấu nháy là chuỗi nên cũng sai, đúng lỗi của hai đội lúc đầu bài.""",
          focus=[["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"], 3], clear=True),
        S(spec_part("resp", "Bước 5. Người gọi phải xử lý những phản hồi nào")
          + """<p class='note'>Làm thử: 4 mã → ứng dụng viết đúng 4 nhánh. 409, 422 theo bản nháp IETF về Idempotency-Key (bản 08). IETF là tổ chức soạn các chuẩn Internet; <b>bản nháp</b> là văn bản đang soạn, chưa thành chuẩn chính thức và còn có thể đổi.</p>""",
          """Bước năm, mục phản hồi liệt kê bốn mã. Hai trăm linh một là đã tạo lệnh, bốn trăm là sai lược đồ. Bốn trăm linh chín và bốn trăm hai mươi hai theo một bản nháp, tức văn bản chuẩn đang soạn, chưa chính thức.
          Vì các mã viết sẵn, người gọi biết trước phải xử lý trường hợp nào, nên ứng dụng viết đúng bốn nhánh.""",
          focus=[["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"], 3], clear=True),
        S("""<p><b>Bước 6. Luật đổi hợp đồng.</b> Hợp đồng đã có người dùng. Một thay đổi là <b class="green">tương thích</b> khi:</p>
<div class="box key">mọi yêu cầu cũ hợp lệ vẫn hợp lệ, <b>và</b> mọi máy khách cũ vẫn đọc được phản hồi mới.</div>
<span class='note'>Làm thử: thêm trường bắt buộc <code>purpose</code> vào yêu cầu → yêu cầu 1 hợp lệ ở hợp đồng cũ thành 400 → <b class="red">phá vỡ</b>.</span>""",
          """Bước sáu là luật khi đổi một hợp đồng đã có người dùng. Thay đổi chỉ là tương thích khi mọi yêu cầu cũ hợp lệ vẫn hợp lệ, và mọi máy khách cũ vẫn đọc được phản hồi mới.
          Làm thử, thêm trường bắt buộc mới thì yêu cầu cũ không có trường đó, từ hợp lệ thành bốn trăm, nên đó là thay đổi phá vỡ.""",
          focus=[1, 2, 3], clear=True),
    ], checks=["alg.bnx_oas_match('0123456789')", "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': 0}) == ['amount: nhỏ hơn 1']",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': '500000'}) == ['amount: sai kiểu']",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0 and alg.bnx_oas_old_valid_after([]) == 1"])

    ex = sc("example", "example", "Ví dụ ba yêu cầu thử, từng phép tính", [
        S(table(["yêu cầu", "fromAccount", "toAccount", "amount"],
                [["1", "0123456789", "9876543210", "500000"], ["2", "0123456789", "9876543210", "0"], ["3", "0123456789", "(không có)", "500000"]])
          + """<p><b>①</b> Yêu cầu 1, hai tài khoản: <code>len("0123456789") = 10</code>, <code>len("9876543210") = 10</code>; 10 nằm trong 10–19 → <b class="green">khớp cả hai</b>.</p>""",
          """Ta kiểm ba yêu cầu thử bằng tay. Yêu cầu một và hai chỉ khác số tiền, còn yêu cầu ba không có tài khoản nhận.
          Phép tính thứ nhất, yêu cầu một có hai số tài khoản đều dài mười chữ số, trong khoảng mười đến mười chín, nên khớp.""",
          focus=[0, 1, 2, 2]),
        S("""<p><b>②</b> Yêu cầu 1, số tiền: <code>500000</code> là số nguyên và lớn hơn 1. Có đủ 3/3 trường bắt buộc → <b class="green">0 lỗi → 201</b>.</p>""",
          """Phép tính thứ hai, số tiền năm trăm nghìn là số nguyên và lớn hơn một. Đủ ba trên ba trường bắt buộc, nên không có lỗi nào, máy chủ trả hai trăm linh một."""),
        S("""<p><b>③</b> Yêu cầu 2: hai tài khoản giống yêu cầu 1, dùng lại kết quả ① → khớp. Số tiền <code>0</code> nhỏ hơn 1 → <b class="red">1 lỗi, trường amount → 400</b>.</p>""",
          """Phép tính thứ ba, yêu cầu hai có hai tài khoản như yêu cầu một nên khớp. Số tiền bằng không, nhỏ hơn một, nên một lỗi, trả bốn trăm."""),
        S("""<p><b>④</b> Yêu cầu 3: có 2 trong 3 trường bắt buộc, thiếu 3 − 2 = 1 trường là <code>toAccount</code> → <b class="red">1 lỗi → 400</b>.</p>""",
          """Phép tính thứ tư, yêu cầu ba có hai trong ba trường bắt buộc. Ba trừ hai bằng một, nên thiếu tài khoản nhận, và máy chủ trả bốn trăm."""),
        S("""<p><b>⑤</b> Tổng hợp: 1 yêu cầu được 201, 2 yêu cầu bị 400. Chỉ 1 trong 3 yêu cầu đi tới bước trừ tiền.</p>"""
          + table(["yêu cầu", "số lỗi", "trường sai", "mã"], [["1", "0", "—", "201"], ["2", "1", "amount", "400"], ["3", "1", "toAccount", "400"]]),
          """Phép tính thứ năm, ta tổng hợp cả ba yêu cầu. Một yêu cầu được hai trăm linh một, hai yêu cầu bị bốn trăm, nên chỉ một trong ba yêu cầu đi tới bước trừ tiền.""",
          focus=[1, 2], clear=True),
    ], checks=["len('0123456789') == 10 and len('9876543210') == 10 and alg.bnx_oas_match('0123456789') and alg.bnx_oas_match('9876543210')",
               "[s for s, _ in alg.bnx_oas_batch()] == [201, 400, 400]",
               "[len(e) for _, e in alg.bnx_oas_batch()] == [0, 1, 1]",
               "alg.bnx_oas_batch()[1][1][0].startswith('amount') and alg.bnx_oas_batch()[2][1][0].startswith('toAccount')",
               "3 - len({'fromAccount', 'amount'}) == 1"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cho máy kiểm lại", [
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>import re</code>", "nạp thư viện mẫu chữ của Python"],
                 ["<code>re.compile(r\"^[0-9]{10,19}&#36;\")</code>", "biên mẫu thành một vật dùng lại được; chữ <code>r</code> trước dấu nháy: viết nguyên mọi dấu gạch ngược"],
                 ["<code>def kiem(req):</code> … <code>return loi + …</code>", "định nghĩa hàm <code>kiem</code> nhận một yêu cầu <code>req</code>, là một <b>từ điển</b>: bảng tên trường và giá trị; <code>return</code> trả kết quả về nơi gọi; dấu <code>+</code> nối hai danh sách thành một"],
                 ["<code>req.get(f)</code>", "lấy giá trị của trường <code>f</code>; không có thì cho <code>None</code>, nghĩa là rỗng"],
                 ["<code>type(v) is str</code>, <code>TK.fullmatch(v)</code>, <code>loi.append(x)</code>", "<code>v</code> đúng là chuỗi chữ; cả chuỗi <code>v</code> khớp mẫu <code>TK</code>, không chỉ một đoạn; thêm <code>x</code> vào cuối danh sách <code>loi</code>"]]),
          """Mã Python sắp tới dùng vài cách viết mới, nên ta giải nghĩa trước. Ta nạp thư viện mẫu chữ rồi biên mẫu số tài khoản thành một vật dùng lại được. Hàm nhận một yêu cầu là từ điển, tức bảng tên trường và giá trị, rồi trả về một danh sách lỗi.
          Lệnh lấy giá trị cho rỗng khi thiếu trường. Các phép kiểm hỏi giá trị có là chuỗi khớp trọn mẫu không."""),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>[f + \": thiếu\" for f in CAN if req.get(f) is None]</code>", "viết gọn một vòng lặp: duyệt từng tên <code>f</code> trong <code>CAN</code>, giữ tên nào có giá trị rỗng, ghép thành danh sách lỗi"],
                 ["<code>CAN = (\"a\", \"b\", \"c\")  # chú thích</code>", "bộ giá trị (tuple): vài giá trị cố định trong ngoặc tròn; chữ sau dấu <code>#</code> là chú thích, máy bỏ qua"],
                 ["<code>for f in (\"fromAccount\", \"toAccount\"):</code>", "duyệt từng phần tử của bộ: <code>f</code> lần lượt là hai tên; dấu hai chấm cuối dòng mở khối lệnh thụt vào"],
                 ["<code>if v is not None and not (…):</code>", "chỉ khi <code>v</code> có giá trị <b>và</b> KHÔNG đúng điều trong ngoặc (v là chuỗi khớp mẫu) thì ghi lỗi"]]),
          """Bốn cách viết nữa của hàm kiểm. Dòng liệt kê lỗi là cách viết gọn một vòng lặp. Bộ giá trị là vài giá trị cố định trong ngoặc tròn, chữ sau dấu thăng là chú thích. Vòng lặp duyệt từng phần tử của bộ.
          Điều kiện cuối chỉ ghi lỗi khi có giá trị mà giá trị không phải chuỗi khớp mẫu, vì thiếu trường đã báo ở dòng trên.""",
          clear=True),
        S(code(VALIDATE_PY, "Chương trình Python kiểm theo lược đồ", lines=VALIDATE_PARTS["ham"]),
          """Ta kiểm lại bằng một chương trình Python nhỏ làm đúng các luật của lược đồ. Hàm kiểm trước hết liệt kê trường bắt buộc nào thiếu.
          Với hai tài khoản, giá trị phải là chuỗi và khớp trọn mẫu, vì dấu đô la của Python vẫn cho lọt một ký tự xuống dòng ở cuối.""",
          focus=[0, 2, ["2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>a is None or (…)</code>", "<code>or</code> đúng nếu một trong hai vế đúng; <code>a</code> rỗng thì khỏi kiểm vế sau"],
                 ["<code>[] if ok else [\"…\"]</code>, <code>400 if loi else 201</code>", "chọn một trong hai giá trị: <code>ok</code> đúng thì cho danh sách rỗng, không thì danh sách có một lỗi; danh sách lỗi không rỗng thì 400, rỗng thì 201"],
                 ["<code>A, B = \"…\", \"…\"</code>", "gán hai biến trên một dòng: <code>A</code> nhận chuỗi đầu, <code>B</code> nhận chuỗi sau"],
                 ["<code>enumerate(thu, 1)</code>", "duyệt danh sách <code>thu</code> kèm số thứ tự bắt đầu từ 1"]]),
          """Đoạn sau còn vài cách viết nữa, nên ta giải nghĩa trước. Phép hoặc đúng nếu một trong hai vế đúng. Cách viết chọn một trong hai giá trị tuỳ điều kiện cho danh sách rỗng hoặc mã bốn trăm. Dòng gán hai biến nhận hai chuỗi, và lệnh cuối duyệt danh sách kèm số thứ tự từ một.""",
          clear=True),
        S(code(VALIDATE_PY, "(tiếp) Kiểm số tiền, rồi chạy ba yêu cầu thử", lines=VALIDATE_PARTS["thu"]),
          """Hàm kiểm số tiền đòi một số nguyên lớn hơn hoặc bằng một, và bỏ qua nếu không có số tiền vì phần trên đã báo thiếu.
          Rồi ta chạy ba yêu cầu thử y như bảng lúc nãy và in mã trạng thái cùng danh sách lỗi.""",
          focus=[["2.1", "2.2", "2.3"], ["2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11"]], clear=True),
        S(out(VALIDATE_OUT),
          """Kết quả chạy thật: yêu cầu một được hai trăm linh một, yêu cầu hai bị bốn trăm ở số tiền, và yêu cầu ba bị bốn trăm vì thiếu tài khoản nhận, khớp phép tính tay.""",
          focus=[["2.1", "2.2", "2.3"]], clear=True),
        S(table(["thay đổi", "ở đâu", "luật ở bước 6", "loại"],
                [["thêm trường tuỳ chọn <code>fee</code>", "phản hồi", "nếu máy khách cũ được cấu hình bỏ qua trường lạ (<b>Jackson</b>, thư viện đọc JSON phổ biến của Java, mặc định báo lỗi; <b>Spring</b>, bộ khung dựng máy chủ Java, tắt lỗi này)", "<b class='green'>tương thích</b>"],
                 ["thêm trường bắt buộc <code>purpose</code>", "yêu cầu", "yêu cầu cũ thiếu nó → 400", "<b class='red'>phá vỡ</b>"],
                 ["đổi <code>amount</code> từ số nguyên sang chuỗi", "yêu cầu", "yêu cầu cũ gửi số → sai kiểu", "<b class='red'>phá vỡ</b>"],
                 ["xoá trường <code>toAccount</code> khỏi phản hồi", "phản hồi", "máy khách cũ đang đọc nó", "<b class='red'>phá vỡ</b>"]]),
          """Bảng này áp luật đổi hợp đồng cho bốn thay đổi. Thêm trường tuỳ chọn vào phản hồi là tương thích, nếu máy khách cũ bỏ qua trường lạ, như Spring, bộ khung dựng máy chủ Java. Ba thay đổi còn lại đều là phá vỡ.""",
          focus=[["1.1", "1.2"], ["1.3", "1.4", "1.5"]], clear=True, introduces=["bnx_jackson"]),
    ], checks=["[s for s, _ in alg.bnx_oas_batch()] == [201, 400, 400]",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': None, 'amount': None}) == ['toAccount: sai kiểu', 'amount: sai kiểu'] and not alg.bnx_oas_match('0123456789\\n')",
               "alg.bnx_oas_change({'required': ['id'], 'properties': {'id': {'type': 'string'}}}, {'required': ['id'], 'properties': {'id': {'type': 'string'}, 'fee': {'type': 'integer'}}}, 'response') == 'tương thích'",
               "alg.bnx_oas_change({'required': ['amount'], 'properties': {'amount': {'type': 'integer'}}}, {'required': ['amount', 'purpose'], 'properties': {'amount': {'type': 'integer'}, 'purpose': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_change({'properties': {'amount': {'type': 'integer'}}}, {'properties': {'amount': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_change({'properties': {'id': {'type': 'string'}, 'toAccount': {'type': 'string'}}}, {'properties': {'id': {'type': 'string'}}}, 'response') == 'phá vỡ'"])

    quymo = sc("quymo", "example", "Khi lưu lượng tăng: bao nhiêu yêu cầu sai bị chặn ở cửa", [
        S(table(["cách viết", "nghĩa", "ví dụ"],
                [["<code>i % 50 == 0</code>", "phần dư khi chia <code>i</code> cho 50 bằng 0, tức <code>i</code> là bội của 50", "50, 100, 150…"],
                 ["<code>req[\"amount\"] = 0</code>, <code>del req[\"toAccount\"]</code>", "gán giá trị cho một trường của từ điển <code>req</code>; xoá hẳn trường khỏi <code>req</code>", "số tiền bằng 0; yêu cầu thiếu tài khoản nhận"],
                 ["<code>range(1, n + 1)</code>", "dãy số từ 1 đến n", "n = 3 cho 1, 2, 3"],
                 ["<code>chan += bool(kiem(req))</code>", "<code>+=</code> cộng thêm vào biến; <code>bool(danh sách)</code> là True nếu danh sách có lỗi, và True tính là 1", "có lỗi thì <code>chan</code> tăng 1"]]),
          """Khối đo dùng thêm bốn cách viết. Dấu phần trăm cho phần dư của phép chia, nên phần dư bằng không nghĩa là số đó là bội. Lệnh gán đặt một trường bằng không, lệnh xoá bỏ hẳn một trường, và lệnh dãy số cho các số từ một đến n.
          Dòng cuối cộng thêm một vào biến đếm mỗi khi danh sách lỗi không rỗng.""",
          clear=True),
        S(code(SCALE_PY, "Đo thật: lô yêu cầu có tỉ lệ sai cố định, chạy hàm kiem ở trên"),
          """Ta đo khi lưu lượng tăng, dùng lại hàm kiểm lúc nãy. Mỗi lô có tỉ lệ sai cố định, số minh hoạ: cứ năm mươi yêu cầu có một số tiền bằng không, cứ tám mươi yêu cầu có một yêu cầu thiếu tài khoản nhận.
          Hàm đếm số yêu cầu bị chặn, rồi ta chạy với một nghìn và một trăm nghìn yêu cầu.""",
          focus=[["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"], ["2.10", "2.11", "2.12"]], clear=True),
        S(out(SCALE_OUT) + table(["lô", "bị chặn ở cửa", "nếu không bật kiểm lược đồ"],
                                 [["1 000", "30", "30 yêu cầu sai chạm vào tiền"], ["100 000 (gấp 100 lần)", "3 000", "3 000 yêu cầu sai chạm vào tiền"]])
          + """$$n = 100\\,000: \\quad 2\\,000 + 1\\,250 - 250 = \\hl{3\\,000} \\text{ yêu cầu bị chặn}$$
<p class="note">2 000 yêu cầu số tiền 0, 1 250 yêu cầu thiếu tài khoản nhận, trừ 250 yêu cầu bị đếm hai lần (cả hai lỗi).</p>""",
          """Máy cho ba mươi yêu cầu sai ở lô một nghìn, và ba nghìn ở lô một trăm nghìn. Vì tỉ lệ sai giữ nguyên, gấp một trăm lần lưu lượng thì gấp một trăm lần yêu cầu sai. Không bật kiểm lược đồ thì cả ba nghìn yêu cầu đó đi tới bước trừ tiền.""",
          clear=True),
        S(table(["số đối tác gọi API", "đổi hợp đồng kiểu phá vỡ làm gãy", "cách làm"],
                [["5", "5 đối tác cùng lúc", "báo từng nơi, vài ngày là xong"],
                 ["50 (gấp 10 lần)", "50 đối tác", "không thể bắt cùng đổi một ngày"],
                 ["500 (gấp 100 lần)", "500 đối tác", "bắt buộc chạy song song hai phiên bản, tắt bản cũ theo hạn đã báo"]])
          + """<p class="note">Số đối tác là số minh hoạ; bộ kiểm chạy hàm kiểm với hợp đồng mới đòi thêm trường <code>purpose</code>: mỗi đối tác cũ nhận 400.</p>""",
          """Đổi hợp đồng kiểu phá vỡ làm gãy mọi đối tác cùng lúc. Với năm đối tác ta báo từng nơi, với năm mươi thì không thể bắt cùng đổi một ngày. Với năm trăm thì bắt buộc chạy song song hai phiên bản.""",
          clear=True),
    ], checks=["[alg.bnx_l01_blocked(n) for n in (1000, 100000)] == [30, 3000]",
               "alg.bnx_l01_blocked(100000) == 100000 // 50 + 100000 // 80 - 100000 // 400 == 2000 + 1250 - 250",
               "100000 // 1000 == 100 and 500 // 5 == 100"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nói “viết API bằng Swagger 3”. <b>OpenAPI là chuẩn đặc tả</b>; <b>Swagger là bộ công cụ</b> làm việc với chuẩn đó.
<br><span class="note">Lịch sử: chuẩn tên cũ là Swagger Specification; cuối năm 2015 bản Swagger 2.0 được trao cho tổ chức OpenAPI Initiative, rồi đặc tả mang tên OpenAPI. Bài này dùng OpenAPI 3.0.3.</span></div>""",
          """Lỗi thứ nhất, của người mới, là gọi đặc tả là Swagger ba. OpenAPI mới là chuẩn đặc tả, còn Swagger là bộ công cụ. Chuẩn này trước kia mang tên Swagger, cuối năm hai nghìn không trăm mười lăm được trao cho một tổ chức mở và đổi tên."""),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Đặc tả viết đẹp, trang mô tả API chạy tốt, nhưng máy chủ <b class="red">không bật kiểm lược đồ</b>. Yêu cầu số tiền 0 vẫn lọt vào bước trừ tiền.
<br><span class="note">Đặc tả không tự kiểm dữ liệu. Phải bật bộ kiểm ở máy chủ, và có ca thử gửi yêu cầu sai để chắc nó trả 400.</span></div>""",
          """Lỗi thứ hai, của người đã đi làm. Đặc tả viết đẹp nhưng máy chủ không bật kiểm lược đồ, nên yêu cầu số tiền bằng không vẫn lọt vào bước trừ tiền.
          Đặc tả chỉ là văn bản, nên phải bật bộ kiểm và có ca thử yêu cầu sai để chắc máy chủ trả bốn trăm."""),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Thêm trường bắt buộc <code>purpose</code> vào yêu cầu rồi nghĩ “chỉ là thêm, không sao”. Mọi đối tác chưa cập nhật nhận <b class="red">400</b>.
<br><span class="note">Cách chữa: thêm trường <b>tuỳ chọn</b> có giá trị mặc định; muốn bắt buộc thì ra phiên bản mới và báo trước cho đối tác.</span></div>""",
          """Lỗi thứ ba, cũng của người đã đi làm, là thêm một trường bắt buộc rồi nghĩ chỉ là thêm, không sao, nên mọi đối tác chưa cập nhật lập tức nhận bốn trăm.
          Cách chữa là thêm trường tuỳ chọn có giá trị mặc định, còn muốn bắt buộc thì ra bản mới và báo trước."""),
    ], checks=["alg.bnx_oas_status({'fromAccount': '0123456789', 'toAccount': '9876543210', 'amount': 0}) == 400",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "Yêu cầu: fromAccount <code>\"0123456789\"</code>, toAccount <code>\"12345678901234567890\"</code> (20 chữ số), amount <code>100000</code>. Mã trạng thái nào? Trường nào sai?"],
                 ["2", "Phân loại: (a) thêm trường tuỳ chọn <code>createdAt</code> vào phản hồi 201; (b) đổi amount từ số nguyên sang chuỗi."],
                 ["3", "Quyết định: cần thêm trường bắt buộc <code>purpose</code> (nội dung chuyển khoản), đã có 5 đối tác đang gọi (số minh hoạ). Sửa ngay đường cũ, hay làm cách khác?"]]),
          """Bây giờ tới phần bạn tự làm, ba câu trên màn hình. Câu ba hỏi cách thêm trường bắt buộc khi đã có năm đối tác. Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""<p>Câu 1: <code>len("12345678901234567890") = 20</code>, lớn hơn 19 → không khớp mẫu.</p>
<div class="box key">Trường sai: <b>toAccount</b> → máy chủ trả <b class="red">400</b>. Tài khoản chuyển và số tiền đều đúng.</div>""",
          """Đáp án câu một. Chuỗi tài khoản nhận dài hai mươi chữ số, lớn hơn mười chín, nên không khớp mẫu. Trường sai là tài khoản nhận, máy chủ trả bốn trăm.""",
          focus=[0, 1, 2]),
        S(table(["thay đổi", "lý do", "loại"],
                [["(a) thêm <code>createdAt</code> tuỳ chọn ở phản hồi", "máy khách cũ bỏ qua trường lạ (khi được cấu hình như vậy)", "<b class='green'>tương thích</b>"],
                 ["(b) amount: số nguyên → chuỗi", "yêu cầu cũ gửi số nguyên bị báo sai kiểu", "<b class='red'>phá vỡ</b>"]]),
          """Đáp án câu hai. Thêm trường tuỳ chọn vào phản hồi là tương thích, nếu máy khách cũ được cấu hình bỏ qua trường lạ. Đổi kiểu số tiền là phá vỡ, vì yêu cầu cũ gửi số nguyên sẽ bị báo sai kiểu.""",
          focus=[0, "1.2", "1.3"]),
        S(table(["lựa chọn", "được", "mất"],
                [["sửa ngay đường cũ, <code>purpose</code> bắt buộc", "một phiên bản, mã gọn", "5 đối tác nhận 400 tới khi họ sửa xong"],
                 ["đường cũ: <code>purpose</code> tuỳ chọn, có mặc định; bắt buộc ở <code>/v2/transfers</code>, báo trước thời hạn", "không ai gãy; đối tác chuyển dần", "phải chạy và kiểm hai phiên bản trong một thời gian"]]),
          """Đáp án câu ba. Sửa ngay đường cũ thì chỉ có một phiên bản và mã gọn, nhưng năm đối tác nhận bốn trăm cho tới khi họ sửa xong.
          Cách thứ hai giữ trường tuỳ chọn ở đường cũ và chỉ bắt buộc ở phiên bản hai, có báo trước. Nhờ vậy không ai bị gãy, đổi lại phải chạy hai phiên bản một thời gian.""",
          focus=[0, "1.2", "1.3"]),
    ], checks=["len('12345678901234567890') == 20 and not alg.bnx_oas_match('12345678901234567890')",
               "alg.bnx_oas_errors({'fromAccount': '0123456789', 'toAccount': '12345678901234567890', 'amount': 100000}) == ['toAccount: sai dạng']",
               "alg.bnx_oas_change({'properties': {'id': {'type': 'string'}}}, {'properties': {'id': {'type': 'string'}, 'createdAt': {'type': 'string'}}}, 'response') == 'tương thích'",
               "alg.bnx_oas_change({'properties': {'amount': {'type': 'integer'}}}, {'properties': {'amount': {'type': 'string'}}}, 'request') == 'phá vỡ'",
               "alg.bnx_oas_old_valid_after(['purpose']) == 0"])

    lab_pr = practice_scene(sc, "Tự làm: kiểm yêu cầu rút tiền theo lược đồ", practice_steps2(
        st, "BNX", "L01",
        """<p><b>Đề</b> (số minh hoạ): lược đồ yêu cầu rút tiền ATM có hai trường bắt buộc.</p>
<ul><li><code>soThe</code>: chuỗi đúng <b>16</b> chữ số</li><li><code>soTien</code>: số nguyên, từ <b>50000</b> trở lên</li></ul>
<p>Viết <code>mau.py</code> có hàm <code>kiem(req)</code> trả danh sách lỗi (chuỗi lỗi quy ước trong <code>de.md</code>), rồi chạy năm yêu cầu thử và in một dòng <code>i mã lỗi</code> mỗi yêu cầu (lỗi cách nhau bằng <code>; </code>, không lỗi thì in <code>-</code>).</p>""",
        """Bây giờ tới phần bạn tự làm. Một yêu cầu rút tiền có hai trường bắt buộc, số thẻ là chuỗi đúng mười sáu chữ số và số tiền là số nguyên từ năm mươi nghìn trở lên.
        Hãy viết hàm kiểm trả danh sách lỗi theo quy ước trong thư mục thực hành, chạy năm yêu cầu thử và in kết quả, rồi dừng video để tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> làm đúng như hàm <code>kiem</code> trong bài: thiếu thì <code>req.get(f) is None</code>; số thẻ kiểm <code>type(v) is str</code> rồi <code>fullmatch</code>; số tiền kiểm <code>type(t) is int</code> và <code>t &gt;= 50000</code>.
Lời giải ở <code>labs/BNX/L01/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, làm đúng như hàm kiểm trong bài. Lấy giá trị bằng hàm get rồi so với rỗng, số thẻ phải là chuỗi khớp trọn mẫu, số tiền phải là số nguyên không nhỏ hơn năm mươi nghìn.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L01")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("viết đặc tả trước", "các đội làm song song", "máy chủ kiểm lược đồ", "yêu cầu sai trả 400", "đổi hợp đồng theo luật tương thích"),
          """Viết đặc tả trước nên các đội làm song song, và máy chủ bật kiểm lược đồ nên yêu cầu sai bị chặn trước khi chạm tiền. Mỗi lần đổi hợp đồng, ta hỏi yêu cầu cũ và máy khách cũ còn chạy không."""),
        S("""<div class='box key'><b>Tư duy:</b> đặc tả API là <b>lời hứa</b> với người gọi. Thêm điều hứa thường thì được; rút lại hay siết chặt điều đã hứa là làm gãy người khác.
<br><span class="note">Trường hợp đặc biệt: thêm giá trị mới vào một trường liệt kê (<code>enum</code>) của phản hồi làm gãy máy khách đọc chặt danh sách giá trị.</span></div>
<p class="note">Bài sau: cùng ý tưởng hợp đồng trước, nhưng bản tin là dãy byte nhị phân thay cho chữ.</p>""",
          """Điều cần mang theo: đặc tả API là lời hứa với người gọi, thêm điều hứa thường thì được, còn rút lại hay siết chặt điều đã hứa là làm gãy người khác. Có một trường hợp đặc biệt: thêm giá trị mới vào trường liệt kê, tức trường chỉ nhận vài giá trị cho trước, cũng làm gãy máy khách đọc chặt.
          Ở bài sau, bản tin là một dãy byte nhị phân thay cho chữ.""",
          focus=[1, 1, 2], forward_ref=True),
    ])
    scenes = [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec]
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            _merge_short(s_)
    return lesson("L01", "openapi_hop_dong_api", "Bài 1 — OpenAPI (Swagger): đặc tả API là hợp đồng, viết trước khi viết mã",
                  "curriculum/bnx.yaml L01; audit/bnx/verify_bnx.py L01; OpenAPI Specification 3.0.3 (spec.openapis.org, đọc 2026-11-11); "
                  "swagger.io/docs/specification/v3_0/about (đọc 2026-11-11)",
                  ["Đọc một đặc tả OpenAPI 3: đường dẫn, phương thức, thân yêu cầu, phản hồi, lược đồ", "Kiểm một yêu cầu theo lược đồ và chỉ ra trường sai",
                   "Phân biệt thay đổi tương thích và thay đổi phá vỡ hợp đồng", "Nêu lợi ích của cách làm hợp đồng trước",
                   "Đếm số yêu cầu sai bị chặn ở cửa kiểm lược đồ khi lưu lượng tăng từ 1 000 lên 100 000 yêu cầu",
                   "Tự viết hàm kiểm một yêu cầu theo lược đồ và chạy năm yêu cầu thử"],
                  scenes,
                  covers=[(1, "formula"), (2, "example"), (3, "check"), (4, "intuition"), (5, "quymo"), (6, "practice")])
