import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene  # noqa: F401
from l03 import _merge_short  # ghép câu < 8 từ vào câu bên cạnh (máy nghe gắn cờ câu ngắn)

# ── Mã trên màn hình (chạy/kiểm NGUYÊN VĂN: audit/review/screen_code.py; audit/bnx/ver/l02.py nạp đúng các hằng này) ──
PROTO_V1 = """syntax = "proto3";

message Transfer {
  int64 id = 1;
  string to_account = 2;
  int64 amount = 3;
  int64 fee = 4;
}

service TransferService {
  rpc Create(Transfer) returns (Transfer);
}
"""

PROTO_BAD = """syntax = "proto3";

message Transfer {      // bản "dọn dẹp": đổi số hiệu
  int64 id = 1;
  string to_account = 2;
  int64 fee = 3;
  int64 amount = 4;
}
"""

PROTO_RESERVED = """syntax = "proto3";

message Transfer {      // xoá to_account đúng cách
  reserved 2;
  reserved "to_account";
  int64 id = 1;
  int64 amount = 3;
  int64 fee = 4;
}
"""

ENCODE_PY = """def varint(n):                   # số nguyên không âm → byte
    out = []
    while True:
        b, n = n & 0x7F, n >> 7        # 0x7F = 127: giữ 7 bit thấp
        out.append(b | 0x80 if n else b)   # 0x80 = 128: bật bit 8
        if n == 0:
            return bytes(out)

def field(num, wire, payload):
    return varint(num << 3 | wire) + payload
m = field(1, 0, varint(150))
print(m.hex(" "), len(m), "byte")

s = "0123456789".encode()
t = field(2, 2, varint(len(s)) + s)    # kiểu 2: độ dài rồi byte
print(t.hex(" "), len(t), "byte")
import json
j = json.dumps({"id": 150}, separators=(",", ":"))
print(j, len(j.encode()), "byte")
"""
ENCODE_PARTS = {"so": (1, 12), "chuoi": (14, 19)}
ENCODE_OUT = """08 96 01 3 byte
12 0a 30 31 32 33 34 35 36 37 38 39 12 byte
{"id":150} 10 byte"""

DECODE_PY = """def read_varint(buf, i):
    n = shift = 0
    while True:
        b = buf[i]
        i += 1
        n |= (b & 0x7F) << shift
        shift += 7
        if b < 0x80:                   # bit 8 tắt: byte cuối
            return n, i

def decode(buf):
    i, out = 0, {}
    while i < len(buf):
        key, i = read_varint(buf, i)
        num, wire = key >> 3, key & 7
        if wire == 0:
            out[num], i = read_varint(buf, i)
        else:                          # wire == 2: độ dài rồi byte
            ln, i = read_varint(buf, i)
            out[num], i = buf[i:i + ln], i + ln
    return out

print(decode(bytes.fromhex("08 96 01")))
print(decode(bytes.fromhex("12 0a 30 31 32 33 34 35 36 37 38 39")))
"""
DECODE_PARTS = {"varint": (1, 9), "decode": (11, 21), "thu": (23, 24)}
DECODE_OUT = """{1: 150}
{2: b'0123456789'}"""

RENUM_PY = """old = bytes.fromhex("08 96 01 18 a0 c2 1e 20 fc 2a")   # bản tin cũ
d = decode(old)
V1 = {1: "id", 3: "amount", 4: "fee"}     # theo .proto cũ
V2 = {1: "id", 3: "fee", 4: "amount"}     # theo .proto đổi số hiệu
print(d)
print({V1[k]: v for k, v in d.items()})
print({V2[k]: v for k, v in d.items()})
"""
RENUM_OUT = """{1: 150, 3: 500000, 4: 5500}
{'id': 150, 'amount': 500000, 'fee': 5500}
{'id': 150, 'fee': 500000, 'amount': 5500}"""

DEADLINE_PY = """HAN = 2000                         # ms người dùng chịu chờ
def goi(ten, can_ms, con_lai):
    if can_ms > con_lai:
        print(ten, "HẾT GIỜ sau", con_lai, "ms")
        return None
    print(ten, "xong, còn", con_lai - can_ms, "ms")
    return con_lai - can_ms
con = HAN
for ten in ["dịch vụ 1", "dịch vụ 2", "dịch vụ 3"]:
    con = goi(ten, 800, con)       # truyền thời gian CÒN LẠI
    if con is None:
        break
"""
DEADLINE_OUT = """dịch vụ 1 xong, còn 1200 ms
dịch vụ 2 xong, còn 400 ms
dịch vụ 3 HẾT GIỜ sau 400 ms"""

# Cảnh quy mô (AF2): đo thật tổng byte của n bản tin chuyển khoản (id, tài khoản 10 chữ số, số tiền, phí) ở hai mức n; ghép sau ENCODE_PY (hàm varint, field).
SCALE_PY = """def msg(i):                 # id = i, số tiền = i × 1000
    s = ("%010d" % i).encode()
    return (field(1, 0, varint(i)) + field(2, 2, varint(len(s)) + s)
            + field(3, 0, varint(i * 1000)) + field(4, 0, varint(5500)))
for n in (1000, 100000):
    pb = sum(len(msg(i)) for i in range(1, n + 1))
    js = sum(len(json.dumps({"id": i, "to_account": "%010d" % i,
                             "amount": i * 1000, "fee": 5500},
                            separators=(",", ":")).encode())
             for i in range(1, n + 1))
    print(n, "ban tin:", pb, "byte nhi phan,", js, "byte JSON")
"""
SCALE_OUT = """1000 ban tin: 21857 byte nhi phan, 62786 byte JSON
100000 ban tin: 2381377 byte nhi phan, 6677790 byte JSON"""

# Lab labs/BNX/L02 (số liệu KHÁC bài: trường 1 = 20, trường 6 = 70000, trường 7 = "ATM01")
LAB_PY = '''
def varint(n):
    out = []
    while True:
        b, n = n & 0x7F, n >> 7
        out.append(b | 0x80 if n else b)
        if n == 0:
            return bytes(out)


def field(num, wire, payload):
    return varint(num << 3 | wire) + payload


m = field(1, 0, varint(20))
m += field(6, 0, varint(70000))
m += field(7, 2, varint(5) + b"ATM01")
print(m.hex(" "))
print(len(m), "byte")
'''
LAB_OUT = """08 14 30 f0 a2 04 3a 05 41 54 4d 30 31
13 byte"""

LAB_DE = """# Lab BNX L02 — Mã hoá tay một bản tin ba trường

Một bản tin ghi nhận lần rút tiền ATM (số minh hoạ) có ba trường:

| số hiệu | kiểu dây | giá trị |
|---|---|---|
| 1 | 0 (số nguyên biến độ dài) | 20 |
| 6 | 0 (số nguyên biến độ dài) | 70000 |
| 7 | 2 (độ dài rồi byte) | chuỗi `ATM01` (5 ký tự) |

Viết `mau.py` (Python) gồm hàm `varint(n)` và hàm `field(num, wire, payload)` như trong bài (khoá trường = `num << 3 | wire`), rồi ghép ba trường theo thứ tự trên thành một dãy byte `m` và in đúng hai dòng:

1. `m.hex(" ")` — các byte thập lục phân cách nhau bằng dấu cách;
2. `<số byte> byte` — độ dài của `m`.

Gợi ý tính tay trước: khoá của trường 6 là 6 × 8 + 0 = 48 = `30`; 70000 chia thành các nhóm 7 bit thấp trước. Chuỗi `ATM01` mã hoá là `3a 05` rồi 5 byte chữ.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L02 mau.py`.
"""

# Từ ngoại trong lời đọc: chỉ dùng khi đã dò phát âm (BRIEF mục 6). Chưa dò → nói bằng tiếng Việt, tên gốc chỉ trên màn hình.
SAY_WORDS = {"«gRPC»": "khung gọi hàm từ xa", "«PB»": "định dạng bản tin nhị phân", "«JSON»": "JSON"}   # JSON dò ASR 8/8; gRPC, Protocol Buffers không đạt 7/8 (x1.md)


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


def _bits(x, y, label, top, bot, col):
    return box(x, y, 300, 110, [label, top], col, size=26, bold=True) + txt(x + 150, y + 150, bot, 22, "middle", "#1f2937")


def build():
    write_lab("BNX", "L02", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Số tiền thành phí, phí thành số tiền, và khách chờ mãi", [
        S("""<p>Một dịch vụ nội bộ “dọn dẹp” tệp mô tả bản tin: đổi chỗ số hiệu của hai trường. Bản tin cũ còn nằm chờ trong <b>hàng đợi</b> (nơi các bản tin xếp hàng chờ được xử lý) được đọc lại (số minh hoạ):</p>"""
          + table(["trường", "bên gửi ghi", "bên nhận đọc ra"],
                  [["số tiền", "500 000", "<b class='red'>5 500</b>"], ["phí", "5 500", "<b class='red'>500 000</b>"]])
          + """<div class="box warn">Không có lỗi nào được báo: bản tin vẫn “hợp lệ”, chỉ có <b>nghĩa</b> bị đảo.</div>""",
          """Chào bạn, một đội nội bộ dọn dẹp tệp mô tả bản tin và đổi chỗ số hiệu của hai trường, số minh hoạ.
          Bản tin cũ còn chờ trong hàng đợi, nơi các bản tin xếp hàng chờ xử lý: bên gửi ghi năm trăm nghìn và năm nghìn năm trăm, bên nhận đọc ra hai số đảo ngược. Không có lỗi nào được báo.""",
          focus=[1, "2.2", 3]),
        S(table(["câu hỏi", "bài này trả lời"],
                [["bản tin nhị phân trông thế nào", "mã hoá bằng tay: khoá trường và số nguyên biến độ dài"],
                 ["vì sao số hiệu trường là bất khả xâm phạm", "giải mã bản tin cũ bằng tệp mô tả mới"],
                 ["nhị phân nhỏ hơn chữ bao nhiêu khi lưu lượng tăng", "đo thật ở 1 000 và 100 000 bản tin"],
                 ["vì sao cả chuỗi lời gọi phải dừng đúng hạn", "hạn chót 2 giây qua ba dịch vụ, mỗi dịch vụ 800 ms"]]),
          """Hôm nay ta trả lời bốn câu hỏi. Bản tin nhị phân trông thế nào, ta tự mã hoá từng byte. Vì sao không được đổi số hiệu trường, ta giải mã bản tin cũ. Nhị phân nhỏ hơn chữ bao nhiêu, ta đo thật, và vì sao chuỗi lời gọi phải dừng đúng hạn.""",
          focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_pb_named(alg.bnx_pb_field(3, 0, 500000) + alg.bnx_pb_field(4, 0, 5500), {3: 'fee', 4: 'amount'}) == {'fee': 500000, 'amount': 5500}",
               "[s for s, _ in alg.bnx_deadline_chain(2000, [800, 800, 800])] == ['xong', 'xong', 'hết giờ']"])

    pre = sc("prereq", "prereq", "Trước hết: bốn phép tính trên byte", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Byte và bit", "1 byte = 8 bit, giá trị từ 0 đến 255", "1001 0110 = 128 + 16 + 4 + 2 = 150"],
                 ["② Thập lục phân", "mỗi byte viết bằng 2 chữ số cơ số 16 (a = 10 … f = 15)", "<code>96</code> = 9 × 16 + 6 = 150"],
                 ["③ Dịch trái, dịch phải", "<code>&lt;&lt; 3</code> nhân 2 ba lần; <code>&gt;&gt; 7</code> chia 128 bỏ phần dư", "1 &lt;&lt; 3 = 8; 150 &gt;&gt; 7 = 1"],
                 ["④ VÀ, HOẶC theo bit", "<code>&amp; 127</code> giữ 7 bit thấp; <code>|</code> bật thêm bit", "150 &amp; 127 = 22; 8 | 0 = 8; 22 | 128 = 150"]]),
          """Trước hết ta cần bốn phép tính trên byte. Một byte gồm tám bit, giá trị từ không đến hai trăm năm mươi lăm.
          Thập lục phân viết mỗi byte bằng hai chữ số cơ số mười sáu, nên chín sáu bằng một trăm năm mươi. Dịch trái ba bit là nhân hai ba lần, dịch phải bảy bit là chia một trăm hai mươi tám bỏ phần dư.
          Phép và giữ bảy bit thấp, còn phép hoặc bật thêm bit.""",
          focus=[0, "1.2", "1.3", "1.4"]),
        S(table(["cách viết", "bản tin <code>{\"id\":150}</code>", "số byte"],
                [["chữ (<b>JSON</b>: cách viết dữ liệu thành chữ, các cặp tên và giá trị trong ngoặc nhọn)", "<code>{</code> <code>\"</code> <code>i</code> <code>d</code> <code>\"</code> <code>:</code> <code>1</code> <code>5</code> <code>0</code> <code>}</code>", "10, mỗi ký tự 1 byte"],
                 ["nhị phân (Protocol Buffers)", "<code>08 96 01</code>", "3, tính ở phần sau"]])
          + """<p class="note">Hạn chót: thời điểm người gọi thôi chờ, thường cho bằng thời gian chờ tối đa tính từ lúc gọi. Ví dụ: chờ tối đa 2 000 ms = 2 giây.</p>""",
          """«JSON» là cách viết dữ liệu thành chữ, bằng các cặp tên và giá trị trong ngoặc nhọn. Mỗi ký tự một byte, nên bản tin mã số một trăm năm mươi dài mười byte, còn nhị phân chỉ ba byte.
          Hạn chót là thời điểm người gọi thôi chờ, ví dụ hai nghìn mi li giây, tức hai giây.""",
          focus=["1.2", "1.3", 2], clear=True),
    ], checks=["128 + 16 + 4 + 2 == 150 == int('10010110', 2) == int('96', 16) == 9 * 16 + 6",
               "(1 << 3, 150 >> 7, 150 & 127, 8 | 0, 22 | 128) == (8, 1, 22, 8, 150)",
               "alg.bnx_json_len({'id': 150}) == 10 and len(alg.bnx_pb_field(1, 0, 150)) == 3"])

    sym = sc("sym", "symbol", "Giải mã các từ của bản tin nhị phân", [
        S(table(["dòng trong tệp mô tả", "nghĩa"],
                [["<code>syntax = \"proto3\";</code>", "chọn phiên bản 3 của cú pháp mô tả bản tin"],
                 ["<code>message Transfer { … }</code>", "khai báo một bản tin tên <code>Transfer</code>, trong ngoặc là các trường"],
                 ["<code>int64 id = 1;</code>", "một trường: kiểu số nguyên 64 bit (<code>int64</code>; <code>string</code> là chuỗi chữ), tên <code>id</code>, số hiệu 1"],
                 ["<code>rpc Create(Transfer) returns (Transfer);</code>", "khai báo một hàm gọi từ xa: nhận một <code>Transfer</code>, trả một <code>Transfer</code>"]]),
          """Trước khi đọc tệp mô tả, ta giải nghĩa vài dòng. Dòng đầu chọn phiên bản cú pháp, và một khối khai báo một bản tin gồm các trường.
          Mỗi trường có kiểu, như số nguyên sáu mươi bốn bit, rồi tên và số hiệu. Dòng hàm từ xa nói hàm nhận gì và trả gì.""",
          focus=[1, "1.2", "1.3", "1.4"]),
        S(code(PROTO_V1, "Tệp mô tả transfer.proto (proto3)"),
          """Đây là tệp mô tả bản tin, đóng vai hợp đồng giữa bên gửi và bên nhận. Khối thứ nhất mô tả bản tin chuyển khoản gồm bốn trường, sau dấu bằng là số hiệu trường.
          Khối cuối mô tả dịch vụ có một hàm tạo lệnh.""",
          focus=[["2.3", "2.4", "2.5", "2.6", "2.7", "2.8"], ["2.10", "2.11", "2.12"]], clear=True),
        S(table(["từ", "nghĩa"],
                [["gRPC", "khung gọi hàm ở máy khác như gọi hàm trong máy (RPC), chạy trên HTTP/2 (bản HTTP mới, nhiều lời gọi chung một kết nối), mặc định dùng Protocol Buffers (nguồn: grpc.io)"],
                 ["số hiệu trường", "số sau dấu <code>=</code>; trên dây chỉ có <b>số</b>, không có tên trường"],
                 ["kiểu dây (wire type)", "cách đọc phần giá trị: 0 = VARINT (số nguyên biến độ dài), 2 = LEN (độ dài rồi byte)"],
                 ["khoá trường", "<code>(số hiệu &lt;&lt; 3) | kiểu dây</code>, đứng trước mỗi giá trị"],
                 ["<code>reserved</code>", "giữ chỗ số hiệu hay tên đã xoá, cấm dùng lại"],
                 ["hạn chót (deadline)", "người gọi chờ tối đa bao lâu; quá hạn thì lời gọi bị huỷ với lỗi DEADLINE_EXCEEDED"]]),
          """Khung gọi hàm từ xa cho dịch vụ gọi hàm ở máy khác như gọi hàm trong máy, mặc định dùng bản tin nhị phân này. Trên đường truyền chỉ có số hiệu trường, không có tên. Kiểu dây cho biết cách đọc giá trị: kiểu không là số nguyên biến độ dài, kiểu hai là độ dài rồi các byte.
          Khoá trường ghép số hiệu và kiểu dây, từ giữ chỗ cấm dùng lại số hiệu đã xoá.""",
          clear=True),
    ], checks=["alg.bnx_pb_key(1, 0) == (1 << 3) | 0 == 8", "alg.bnx_pb_key(2, 2) == (2 << 3) | 2 == 18"])

    intu = sc("intuition", "intuition", "Hình dung: ba byte mang số 150, và đồng hồ chạy qua ba dịch vụ", [
        S(svg(1500, 470,
              _bits(80, 60, "08", "0000 1 | 000", "số hiệu 1, kiểu dây 0", C_BLUE),
              _bits(560, 60, "96", "1 | 001 0110", "bit 8 = 1: còn byte sau; 7 bit = 22", C_AMBER),
              _bits(1040, 60, "01", "0 | 000 0001", "bit 8 = 0: byte cuối; 7 bit = 1", C_GREEN),
              arrow(385, 115, 555, 115), arrow(865, 115, 1035, 115),
              box(380, 300, 740, 100, ["giá trị = 22 + 1 × 128 = 150", "nhóm 7 bit đến trước là phần thấp"], C_PURPLE, size=26),
              arrow(710, 245, 650, 295, "#475569"), arrow(1190, 245, 1000, 295, "#475569")),
          """Hình đầu là ba byte của bản tin. Byte đầu là khoá: ba bit thấp là kiểu dây, phần còn lại là số hiệu.
          Byte thứ hai có bit cao nhất bằng một nên còn byte sau, và bảy bit thấp mang hai mươi hai. Còn byte thứ ba là byte cuối, mang số một, nên giá trị bằng hai mươi hai cộng một trăm hai mươi tám, tức một trăm năm mươi."""),
        S(svg(1500, 470,
              txt(60, 70, "0 ms", 22, "start"), txt(1260, 70, "2 400 ms", 22, "middle"),
              box(60, 100, 400, 80, "dịch vụ 1: 800 ms", C_GREEN),
              box(460, 190, 400, 80, "dịch vụ 2: 800 ms", C_GREEN),
              box(860, 280, 200, 80, "dịch vụ 3", C_AMBER),
              box(1060, 280, 200, 80, "quá hạn", C_RED, dash=True),
              '<line x1="1060" y1="80" x2="1060" y2="390" stroke="#dc2626" stroke-width="4" stroke-dasharray="10 6"/>',
              txt(1075, 110, "hạn chót 2 000 ms", 24, "start", "#dc2626", True),
              txt(470, 140, "còn 2 000 − 800 = 1 200", 22, "start", "#16a34a"),
              txt(850, 330, "còn 1 200 − 800 = 400", 22, "end", "#d97706"),
              txt(750, 440, "Dịch vụ 3 cần 800 ms nhưng chỉ còn 400 ms: hết giờ", 26, "middle", "#1f2937", True)),
          """Hình thứ hai là đồng hồ cả chuỗi: người dùng chờ hai nghìn mi li giây, dịch vụ một dùng tám trăm nên còn một nghìn hai trăm, dịch vụ hai dùng nữa nên còn bốn trăm. Dịch vụ ba cần tám trăm nên hết giờ."""),
    ], checks=["22 + 1 * 128 == 150", "0x96 & 127 == 22 and 0x96 >= 128 and 0x01 < 128",
               "2000 - 800 == 1200 and 1200 - 800 == 400 and 800 > 400"])

    form = sc("formula", "formula", "Suy ra từng bước: mã hoá một trường, rồi chia hạn chót", [
        S("""<p><b>Bước 1. Khoá trường.</b> Bên nhận đọc khoá trước, rồi mới biết đọc phần sau thế nào. Có 6 kiểu dây (0 đến 5), vừa trong <b>3 bit</b>, nên khoá là <code>(số hiệu &lt;&lt; 3) | kiểu dây</code>. Dịch trái 3 bit là nhân 8; kiểu dây nhỏ hơn 8 nên phép HOẶC chính là phép cộng:</p>
$$\\text{khoá} = \\text{số hiệu} \\times 8 + \\text{kiểu dây}$$
<span class='note'>Làm thử: trường 1, kiểu 0 → 1 × 8 + 0 = 8 = <code>08</code>; trường 2, kiểu 2 → 2 × 8 + 2 = 18 = <code>12</code>.</span>""",
          """Bước một là cách ghép khoá. Bên nhận phải đọc khoá trước rồi mới biết đọc phần sau thế nào, và có sáu kiểu dây vừa trong ba bit, nên khoá bằng số hiệu nhân tám cộng kiểu dây.
          Làm thử, trường một kiểu không cho tám, trường hai kiểu hai cho mười tám, tức một hai.""",
          focus=[1, 1, 3]),
        S("""<p><b>Bước 2. Số nguyên biến độ dài (varint).</b> Số nhỏ thì nên tốn ít byte. Mỗi byte chỉ mang <b>7 bit</b> giá trị; bit thứ 8 bằng 1 nghĩa là “còn byte sau”. Nhóm 7 bit thấp đi trước.</p>
<span class='note'>Làm thử: 5 nhỏ hơn 128 → 1 byte <code>05</code>; 150 lớn hơn 127 → phải 2 byte.</span>""",
          """Bước hai là số nguyên biến độ dài. Vì số nhỏ nên tốn ít byte, mỗi byte chỉ mang bảy bit giá trị, bit thứ tám bằng một nghĩa là còn byte sau, và nhóm bảy bit thấp ghi trước.
          Làm thử, năm nhỏ hơn một trăm hai mươi tám nên một byte, còn một trăm năm mươi phải hai byte.""",
          focus=[1, 2], clear=True),
        S("""<p><b>Bước 3. Chuỗi (kiểu dây 2).</b> Chữ không có “dấu kết thúc”, nên trước các byte phải ghi <b>độ dài</b>: khoá, độ dài, rồi các byte.</p>
<span class='note'>Làm thử: <code>"0123456789"</code> → khoá <code>12</code>, độ dài 10 = <code>0a</code>, 10 byte chữ → 1 + 1 + 10 = 12 byte.</span>""",
          """Bước ba là chuỗi, dùng kiểu dây hai. Vì bên nhận không biết chuỗi dừng ở đâu, nên trước các byte phải ghi độ dài: khoá, độ dài, rồi các byte.
          Làm thử, chuỗi mười chữ số có khoá một hai, độ dài không a, rồi mười byte chữ, tổng mười hai byte.""",
          focus=[1, 2], clear=True),
        S("""<p><b>Bước 4. Hạn chót đi theo lời gọi.</b> Người dùng chỉ chờ một lần, nên mỗi dịch vụ phải biết người dùng <b>còn</b> chờ bao lâu:</p>
$$\\text{còn lại} = \\text{hạn chót} - \\text{thời gian đã dùng}$$
<span class='note'>Làm thử: 2 000 − 800 = 1 200 ms cho dịch vụ 2; 1 200 − 800 = 400 ms cho dịch vụ 3, mà nó cần 800 → hết giờ.</span>""",
          """Bước bốn là chia hạn chót qua chuỗi lời gọi. Người dùng chỉ chờ một lần, nên mỗi dịch vụ phải biết người dùng còn chờ bao lâu, bằng hạn chót trừ thời gian đã dùng.
          Làm thử, dịch vụ ba nhận bốn trăm mà cần tám trăm, nên hết giờ.""",
          focus=[1, 3], clear=True),
    ], checks=["alg.bnx_pb_key(1, 0) == 8 and alg.bnx_pb_key(2, 2) == 18 == 0x12", "len(alg.bnx_pb_varint(5)) == 1 and len(alg.bnx_pb_varint(150)) == 2",
               "alg.bnx_pb_field(2, 2, '0123456789')[:2].hex() == '120a' and len(alg.bnx_pb_field(2, 2, '0123456789')) == 12",
               "alg.bnx_deadline_chain(2000, [800, 800, 800]) == [('xong', 2000), ('xong', 1200), ('hết giờ', 400)]"])

    ex = sc("example", "example", "Ví dụ trường số 1 mang 150, từng phép tính", [
        S("""<p>Trường số 1, kiểu dây 0, giá trị 150. Khoá theo bước 1:</p>
$$① \\; \\text{khoá} = 1 \\times 8 + 0 = \\hl{8} = \\texttt{08}$$""",
          """Phép tính thứ nhất, khoá của trường số một, kiểu dây không. Theo bước một, một nhân tám cộng không bằng tám, viết thập lục phân là không tám."""),
        S("""<p>Tách 150 thành nhóm 7 bit (<code>150 &amp; 127</code> và <code>150 &gt;&gt; 7</code>):</p>
$$② \\; 150 = 1 \\times 128 + \\hl{22}$$""",
          """Phép tính thứ hai, tách một trăm năm mươi thành nhóm bảy bit. Vì nó bằng một nhân một trăm hai mươi tám cộng hai mươi hai, nhóm thấp là hai mươi hai."""),
        S("""<p>Còn phần 1 ở sau nên byte đầu bật bit 8 (cộng 128):</p>
$$③ \\; 22 + 128 = 150 = \\texttt{96}, \\quad 1 = \\texttt{01} \\;\\Rightarrow\\; \\hlg{\\texttt{08 96 01}}: 3 \\text{ byte}$$
<p class="note">Khớp ví dụ trong trang “Encoding” của protobuf.dev.</p>""",
          """Phép tính thứ ba, vì còn phần một ở sau, byte đầu bật bit tám, nên hai mươi hai cộng một trăm hai mươi tám bằng một trăm năm mươi, viết là chín sáu. Phần sau là không một, nên bản tin là không tám, chín sáu, không một, ba byte.""",
          focus=[[1, 2], 3]),
        S("""<p>Bản tin chữ <code>{"id":150}</code> có 10 ký tự, tức 10 byte:</p>
$$④ \\; 10 - 3 = \\hl{7} \\text{ byte ít hơn}$$""",
          """Phép tính thứ tư, cùng nội dung ở «JSON» dài mười byte, nên bản tin nhị phân ít hơn bảy byte, vì không ghi tên trường và không ghi số dạng chữ.""",
          clear=True),
        S("""<p>Thêm trường 2 là chuỗi <code>"0123456789"</code>: khoá <code>12</code>, độ dài <code>0a</code>, rồi 10 byte chữ.</p>
$$⑤ \\; 1 + 1 + 10 = 12 \\text{ byte}, \\qquad 3 + 12 = \\hlg{15} \\text{ byte cả bản tin}$$""",
          """Phép tính thứ năm, thêm trường số hai là chuỗi tài khoản. Theo bước ba, nó tốn một byte khoá, một byte độ dài và mười byte chữ, nên cả bản tin mười lăm byte."""),
    ], checks=["alg.bnx_pb_varint(alg.bnx_pb_key(1, 0)).hex() == '08'", "(150 & 127, 150 >> 7) == (22, 1)",
               "alg.bnx_pb_field(1, 0, 150).hex() == '089601' and (22 | 128) == 0x96",
               "alg.bnx_json_len({'id': 150}) - len(alg.bnx_pb_field(1, 0, 150)) == 7",
               "len(alg.bnx_pb_field(1, 0, 150) + alg.bnx_pb_field(2, 2, '0123456789')) == 15"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cho máy mã hoá, giải mã và đếm giờ", [
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>def varint(n):</code> … <code>return x</code>", "định nghĩa hàm <code>varint</code> nhận đầu vào <code>n</code>; <code>return</code> trả kết quả <code>x</code> ra; chữ sau dấu <code>#</code> là chú thích, máy bỏ qua"],
                 ["<code>while True:</code> … <code>return</code>", "lặp mãi cho tới khi gặp <code>return</code>"],
                 ["<code>b, n = n &amp; 0x7F, n &gt;&gt; 7</code>", "gán hai biến cùng lúc; <code>0x7F</code> là 127 viết thập lục phân"],
                 ["<code>b | 0x80 if n else b</code>", "nếu <code>n</code> khác 0 thì bật bit 8 của <code>b</code>, không thì giữ <code>b</code>"],
                 ["<code>out.append(x)</code>, <code>bytes(out)</code>", "thêm <code>x</code> vào cuối danh sách; đổi danh sách số thành dãy byte"],
                 ["<code>m.hex(\" \")</code>", "viết dãy byte thành các chữ số 16, cách nhau dấu cách"]]),
          """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Hàm nhận đầu vào rồi trả kết quả ra, vòng lặp mãi chỉ dừng khi trả kết quả.
          Phép hoặc kèm điều kiện bật bit tám khi còn phần sau, và dãy byte được in ra thập lục phân."""),
        S(code(ENCODE_PY, "Chương trình Python mã hoá", lines=ENCODE_PARTS["so"]),
          """Ta cho máy làm lại vì máy không cộng nhầm. Hàm đầu mã một số nguyên: một dòng cho b bảy bit thấp và n phần còn lại, rồi bật bit tám nếu còn phần sau.
          Hàm thứ hai ghép khoá với giá trị.""",
          focus=[["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7"], ["2.9", "2.10", "2.11", "2.12"]], clear=True),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>\"0123456789\".encode()</code>", "đổi chuỗi chữ thành dãy byte"],
                 ["<code>import json</code>", "nạp thư viện JSON của Python"],
                                  ["<code>{\"id\": 150}</code>", "<b>từ điển</b>: các cặp <code>tên: giá trị</code> trong ngoặc nhọn; ở đây một cặp, tên <code>id</code>, giá trị 150"],
                 ["<code>json.dumps(d, separators=(\",\", \":\"))</code>", "viết từ điển <code>d</code> thành chữ JSON gọn, không dấu cách"]]),
          """Phần tiếp có thêm vài cách viết, nên ta giải nghĩa trước. Lệnh đổi chuỗi chữ thành dãy byte, từ điển là các cặp tên và giá trị trong ngoặc nhọn, và hàm của thư viện JSON viết từ điển thành chữ gọn.""",
          clear=True),
        S(code(ENCODE_PY, "(tiếp) Trường chuỗi và bản tin chữ", lines=ENCODE_PARTS["chuoi"])
          + out(ENCODE_OUT),
          """Phần tiếp mã chuỗi tài khoản thành trường số hai, rồi đếm byte của bản tin chữ. Kết quả là ba, mười hai và mười byte, nên khớp phép tính tay.""",
          focus=[[2, 3], "4.1"], clear=True),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>n |= x</code>", "viết gọn của <code>n = n | x</code>: bật thêm các bit của <code>x</code> vào <code>n</code>"],
                 ["<code>buf[i]</code>, <code>buf[i:i + ln]</code>", "byte thứ <code>i</code> của dãy; đoạn cắt bắt đầu từ <code>i</code>, dài <code>ln</code> byte"],
                                  ["<code>bytes.fromhex(\"08 96 01\")</code>, <code>b'0123'</code>", "đổi chuỗi thập lục phân thành dãy byte; chữ <code>b</code> trước dấu nháy là dãy byte, in ra dạng chữ khi byte đọc được"],
                 ["<code>n = shift = 0</code>, <code>return n, i</code>", "gán 0 cho cả hai biến cùng lúc; trả hai giá trị một lúc"]]),
          """Phần giải mã có thêm vài cách viết nên ta giải nghĩa trước. Phép hoặc gán bật thêm bit, ngoặc vuông lấy một byte hoặc cắt một đoạn, chữ b trước dấu nháy là dãy byte. Rồi gán số không cho hai biến và trả hai giá trị.""",
          clear=True),
        S(code(DECODE_PY, "Giải mã: đọc số nguyên biến độ dài", lines=DECODE_PARTS["varint"]),
          """Đường khác thứ hai là giải mã ngược, vì mã đúng thì giải ra phải được số ban đầu. Hàm này đọc từng byte và dừng khi bit tám bằng không.""",
          focus=[["2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"], ["2.4", "2.5", "2.6", "2.7"]], clear=True),
                S(table(["cách viết trong Python", "nghĩa"],
                [["<code>i, out = 0, {}</code>", "gán hai biến: <code>i</code> bằng 0, <code>out</code> là từ điển rỗng"],
                 ["<code>out[num], i = read_varint(buf, i)</code>", "hàm trả hai giá trị: giá trị đầu cất vào từ điển <code>out</code> dưới tên <code>num</code>, giá trị sau gán cho <code>i</code>"],
                 ["<code>out[num], i = buf[i:i + ln], i + ln</code>", "cất đoạn cắt vào <code>out[num]</code>, và đẩy <code>i</code> lên thêm <code>ln</code>"]]),
          """Hàm giải mã cất kết quả vào từ điển rỗng, vì mỗi trường có một số hiệu riêng. Dòng gán đôi cất giá trị vào từ điển dưới số hiệu, rồi cập nhật vị trí đọc. Với chuỗi, vị trí nhảy qua đúng độ dài.""",
          clear=True),
        S(code(DECODE_PY, "(tiếp) Giải mã cả bản tin", lines=DECODE_PARTS["decode"]),
          """Hàm giải mã đọc khoá, rồi tách số hiệu bằng dịch phải ba và kiểu dây bằng phép và với bảy, vì kiểu dây nằm ở ba bit thấp. Kiểu hai thì đọc độ dài rồi cắt đúng chừng ấy byte.""",
          focus=[["2.4", "2.5"], ["2.6", "2.7", "2.8", "2.9", "2.10"]], clear=True),
        S(code(DECODE_PY, "(tiếp) Chạy thử", lines=DECODE_PARTS["thu"]) + out(DECODE_OUT),
          """Chạy thử trên hai bản tin vừa mã: ba byte giải ra một trăm năm mươi, mười hai byte giải ra chuỗi mười chữ số, nên mã và giải mã khớp nhau.""",
          focus=[[2, "4.1"], "4.2"], clear=True),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>def goi(ten, can_ms, con_lai):</code>", "hàm có ba đầu vào; <code>return None</code> trả giá trị rỗng, <code>None</code> nghĩa là không có gì"],
                 ["<code>for ten in [\"a\", \"b\"]:</code>", "duyệt từng tên trong danh sách, lần lượt gán vào <code>ten</code>"],
                 ["<code>if con is None: break</code>", "nếu <code>con</code> rỗng thì <code>break</code>: thoát khỏi vòng lặp ngay"]]),
          """Đoạn đếm giờ có vòng lặp duyệt ba dịch vụ, nên ta giải nghĩa trước. Giá trị rỗng báo hết giờ, và lệnh thoát vòng lặp dừng ngay khi đó.""",
          clear=True),
        S(code(DEADLINE_PY, "Đếm giờ: truyền thời gian còn lại"),
          """Ta mô phỏng hạn chót qua ba dịch vụ. Mỗi dịch vụ nhận thời gian còn lại, báo hết giờ nếu cần nhiều hơn vì người dùng không chờ thêm, rồi chuyển phần còn lại cho dịch vụ sau.""",
          focus=[["2.2", "2.3", "2.4", "2.5"], ["2.8", "2.9", "2.10"]], clear=True),
        S(out(DEADLINE_OUT),
          """Kết quả chạy thật: dịch vụ một còn một nghìn hai trăm, dịch vụ hai còn bốn trăm, và dịch vụ ba hết giờ, nên khớp bước bốn.""",
          focus=[["2.1", "2.2", "2.3"]], clear=True),
    ], checks=["alg.bnx_pb_field(1, 0, 150).hex() == '089601'", "alg.bnx_pb_field(2, 2, '0123456789').hex() == '120a30313233343536373839'",
               "alg.bnx_json_len({'id': 150}) == 10", "alg.bnx_pb_decode(bytes.fromhex('089601')) == {1: 150}",
               "alg.bnx_pb_decode(bytes.fromhex('120a30313233343536373839')) == {2: b'0123456789'}",
               "alg.bnx_deadline_chain(2000, [800, 800, 800]) == [('xong', 2000), ('xong', 1200), ('hết giờ', 400)]"])

    quymo = sc("quymo", "example", "Khi lưu lượng tăng: nhị phân nhỏ hơn chữ bao nhiêu byte", [
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>\"%010d\" % i</code>", "viết số <code>i</code> thành đúng 10 chữ số, thêm số 0 đứng đầu cho đủ"],
                 ["<code>sum(len(…) for i in range(1, n + 1))</code>", "cộng độ dài của từng bản tin, <code>i</code> chạy từ 1 đến n"],
                 ["<code>json.dumps(d, separators=(\",\", \":\"))</code>", "viết từ điển <code>d</code> thành chữ JSON gọn, không dấu cách"]]),
                    """Khối đo dùng ba cách viết nên ta giải nghĩa trước: định dạng viết số thành mười chữ số, hàm cộng tổng độ dài từng bản tin, và cách viết từ điển thành chữ gọn.""",
          clear=True),
        S(code(SCALE_PY, "Đo thật: tổng byte của n bản tin, dùng lại hàm varint và field ở trên"),
          """Ta đo khi lưu lượng tăng, dùng lại hai hàm mã hoá lúc nãy. Mã và số tiền tăng dần nên số nguyên biến độ dài tốn thêm byte. Ta cộng tổng byte của một nghìn và một trăm nghìn bản tin, mã nhị phân rồi mã chữ.""",
          clear=True),
        S(out(SCALE_OUT) + table(["n bản tin", "nhị phân", "chữ (JSON)", "trung bình mỗi bản tin"],
                                 [["1 000", "21 857 byte", "62 786 byte", "21,9 so với 62,8 byte"],
                                  ["100 000 (gấp 100 lần)", "2 381 377 byte", "6 677 790 byte", "23,8 so với 66,8 byte"]])
          + """<p class="note">Ước theo trung bình ở 100 000 (số minh hoạ): 1 000 000 bản tin mỗi ngày ≈ 24 MB nhị phân so với 67 MB chữ, chênh khoảng 43 MB mỗi ngày (MB là mê-ga-byte, một triệu byte).</p>""",
          """Ở một nghìn bản tin, nhị phân tốn hơn hai mươi mốt nghìn byte còn chữ hơn sáu mươi hai nghìn.
          Ở một trăm nghìn bản tin, nhị phân hơn hai triệu ba trăm tám mươi nghìn byte còn chữ hơn sáu triệu sáu trăm bảy mươi nghìn.
          Chữ vẫn gấp gần ba lần, nên một triệu bản tin mỗi ngày, số minh hoạ, chênh bốn mươi ba triệu byte.""",
          clear=True),
        S(table(["cách", "được", "mất", "khi nào chọn"],
                [["chữ (JSON)", "đọc bằng mắt, gỡ lỗi dễ, đối tác nào cũng gọi được", "gấp ≈ 2,8 lần byte, và mỗi lần phải đọc lại chữ", "API cho đối tác, lưu lượng vừa"],
                 ["nhị phân (Protocol Buffers)", "nhỏ hơn ≈ 2,8 lần; hợp đồng .proto chặt", "cần công cụ để đọc; giữ kỷ luật số hiệu", "gọi nội bộ, lưu lượng lớn, hàng đợi"]]),
          """Chữ dễ đọc nhưng gấp gần ba lần byte, nên với lưu lượng lớn và gọi nội bộ thì nhị phân hợp hơn, đổi lại cần công cụ đọc.""",
          clear=True),
    ], checks=["alg.bnx_l02_sizes(1000) == (21857, 62786) and alg.bnx_l02_sizes(100000) == (2381377, 6677790)",
               "round(2381377 / 100000, 1) == 23.8 and round(6677790 / 100000, 1) == 66.8 and round(21857 / 1000, 1) == 21.9 and round(62786 / 1000, 1) == 62.8",
               "6677790 - 2381377 == 4296413 and 100000 // 1000 == 100"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người mới).</b> “gRPC luôn nhanh hơn REST.” (<b>REST</b>: kiểu API thường gặp, gọi qua HTTP với bản tin chữ JSON.) Lợi thật nằm ở bản tin nhỏ, gọi theo luồng (gửi nhiều bản tin liên tiếp trong một lời gọi), và hợp đồng chặt.
<br><span class="note">Một lời gọi 100 ms mà 95 ms là truy vấn cơ sở dữ liệu (số minh hoạ): đổi cách mã bản tin chỉ có thể bớt trong 100 − 95 = 5 ms còn lại.</span></div>""",
          """Lỗi thứ nhất, của người mới, là tin rằng «gRPC» luôn nhanh hơn REST, kiểu API thường gặp với bản tin chữ. Lợi thật nằm ở bản tin nhỏ, gọi theo luồng tức gửi nhiều bản tin liền nhau, và hợp đồng chặt.
          Lời gọi một trăm mi li giây mà chín mươi lăm là truy vấn thì đổi cách mã chỉ bớt năm."""),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> “Dọn dẹp” tệp mô tả bằng cách đổi số hiệu, hoặc xoá trường rồi dùng lại số của nó.</div>"""
          + code(PROTO_BAD) + """<p class="note">Chữ sau <code>//</code> là chú thích trong tệp mô tả, máy bỏ qua.</p>""",
          """Lỗi thứ hai, của người đã đi làm, là dọn dẹp tệp mô tả bằng cách đổi số hiệu: phí sang số ba, số tiền sang số bốn, còn chữ sau hai gạch chéo là chú thích.
          Bản tin cũ chỉ mang số, không mang tên, nên bên đọc theo tệp mới hiểu sai.""",
          focus=[["2.6", "2.7"], ["2.3", "2.4", "2.5", "2.6", "2.7", "2.8"]], clear=True),
        S(table(["cách viết trong Python", "nghĩa"],
                [["<code>V1 = {1: \"id\", 3: \"amount\"}</code>", "từ điển: bảng tra từ số hiệu sang tên"],
                 ["<code>d.items()</code>", "liệt kê từng cặp (khoá, giá trị) của từ điển <code>d</code>"],
                 ["<code>{V1[k]: v for k, v in d.items()}</code>", "viết gọn vòng lặp tạo từ điển mới: với mỗi cặp <code>k, v</code> của <code>d</code>, đổi số hiệu <code>k</code> thành tên <code>V1[k]</code>, giữ giá trị <code>v</code>"]]),
          """Ta đọc lại bản tin cũ bằng hai bảng tra, nên cần giải nghĩa trước. Bảng tra là từ điển từ số hiệu sang tên, và dòng gọn tạo từ điển mới đổi số hiệu thành tên.""",
          clear=True),
        S(code(RENUM_PY, "Giải mã bản tin cũ bằng hai tệp mô tả") + out(RENUM_OUT),
          """Ta chứng minh bằng giải mã, rồi tra tên theo tệp cũ và tệp mới. Đọc theo tệp cũ thì đúng, còn theo tệp đã đổi thì phí thành năm trăm nghìn mà không có lỗi nào được báo.""",
          focus=[["2.1", "2.2", "2.3", "2.4"], "4.2", "4.3"], clear=True),
        S(code(PROTO_RESERVED, "Xoá trường đúng cách: giữ chỗ bằng reserved")
          + """<p class="note">Số hiệu 2 và tên <code>to_account</code> bị khoá lại: ai thêm trường mới dùng số 2 sẽ bị trình biên dịch .proto từ chối.</p>""",
          """Cách chữa là không bao giờ đổi hay dùng lại số hiệu. Muốn xoá trường tài khoản nhận, ta giữ chỗ số hai và tên của nó, nên trình biên dịch, chương trình đọc tệp mô tả, từ chối ai dùng lại.""",
          focus=[["2.4", "2.5"], 3], clear=True),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Mỗi dịch vụ tự đặt lại hạn 2 giây, hoặc không đặt hạn nào (mặc định gRPC <b>không</b> có hạn chót).
<br><span class="note">Đặt lại 2 giây: chuỗi chạy 3 × 800 = 2 400 ms; người dùng đã bỏ cuộc ở 2 000 ms, dịch vụ 3 vẫn làm thêm 400 ms vô ích. Không đặt hạn: một dịch vụ treo kéo cả chuỗi treo theo.</span></div>""",
          """Lỗi thứ ba, của người đã đi làm, là mỗi dịch vụ tự đặt lại hạn hai giây, hoặc không đặt hạn vì mặc định «gRPC» không có hạn chót.
          Đặt lại thì chuỗi chạy hai nghìn bốn trăm mi li giây, nên dịch vụ ba làm thêm bốn trăm vô ích. Không đặt hạn thì một dịch vụ treo kéo cả chuỗi treo theo.""",
          clear=True),
    ], checks=["100 - 95 == 5",
               "alg.bnx_pb_named(bytes.fromhex('08960118a0c21e20fc2a'), {1: 'id', 3: 'fee', 4: 'amount'}) == {'id': 150, 'fee': 500000, 'amount': 5500}",
               "alg.bnx_pb_named(bytes.fromhex('08960118a0c21e20fc2a'), {1: 'id', 3: 'amount', 4: 'fee'}) == {'id': 150, 'amount': 500000, 'fee': 5500}",
               "3 * 800 == 2400 and alg.bnx_deadline_wasted(2000, [800, 800, 800]) == 400",
               "[s for s, _ in alg.bnx_deadline_chain(2000, [800, 800, 800], propagate=False)] == ['xong', 'xong', 'xong']"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "Mã hoá bằng tay trường số 3 mang số nguyên 300 (kiểu dây 0). Viết các byte thập lục phân."],
                 ["2", "Hạn chót 3 giây, chuỗi 4 dịch vụ, mỗi dịch vụ cần 800 ms, có truyền thời gian còn lại. Dịch vụ nào hết giờ, khi còn bao nhiêu ms?"],
                 ["3", "Quyết định: API cho ví điện tử của đối tác gọi vào, và lời gọi nội bộ từ dịch vụ chuyển tiền sang dịch vụ chống gian lận. Mỗi chỗ chọn REST + JSON + OpenAPI hay gRPC?"]]),
          """Bây giờ tới phần bạn tự làm bài, ba câu trên màn hình. Câu ba chọn cách gọi cho đối tác và nội bộ. Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""$$\\text{khoá} = 3 \\times 8 + 0 = 24 = \\texttt{18}; \\quad 300 = 2 \\times 128 + 44; \\quad 44 + 128 = 172 = \\texttt{ac}, \\; 2 = \\texttt{02}$$
<div class="box key">Câu 1: <code>18 ac 02</code>, 3 byte.</div>""",
          """Đáp án câu một. Khoá bằng ba nhân tám, tức hai mươi tư, viết là một tám. Ba trăm bằng hai nhân một trăm hai mươi tám cộng bốn mươi bốn, nên nhóm thấp bật bit tám thành a c, phần hai là không hai, vậy dài ba byte.""",
          focus=[0, 1, 2]),
        S(table(["dịch vụ", "còn lại khi bắt đầu", "cần", "kết quả"],
                [["1", "3 000", "800", "xong"], ["2", "3 000 − 800 = 2 200", "800", "xong"], ["3", "2 200 − 800 = 1 400", "800", "xong"],
                 ["4", "1 400 − 800 = 600", "800", "<b class='red'>hết giờ</b>"]]),
          """Đáp án câu hai. Ba dịch vụ đầu đều xong, còn dịch vụ bốn chỉ còn sáu trăm mà cần tám trăm, nên hết giờ.""",
          focus=[["1.2", "1.3", "1.4"], "1.5"]),
        S(table(["chỗ", "chọn", "được", "mất"],
                [["API cho ví đối tác", "REST + JSON + OpenAPI", "đối tác nào cũng gọi được, đọc bản tin bằng mắt, trang mô tả sẵn", "bản tin to hơn, kiểm lược đồ phải tự bật"],
                 ["chuyển tiền → chống gian lận (nội bộ)", "gRPC", "bản tin nhỏ, hợp đồng .proto chặt, có luồng, hạn chót đi theo lời gọi", "cần công cụ để đọc bản tin; phải giữ kỷ luật số hiệu"]]),
          """Đáp án câu ba. API cho đối tác chọn REST, «JSON» và OpenAPI vì đối tác nào cũng gọi được, đổi lại bản tin to hơn. Lời gọi nội bộ hợp với «gRPC» vì bản tin nhỏ, đổi lại phải giữ kỷ luật số hiệu.""",
          focus=["1.2", "1.3"]),
    ], checks=["alg.bnx_pb_field(3, 0, 300).hex() == '18ac02' and alg.bnx_pb_key(3, 0) == 24 and (300 & 127, 44 | 128, 300 >> 7) == (44, 172, 2)",
               "alg.bnx_deadline_chain(3000, [800] * 4) == [('xong', 3000), ('xong', 2200), ('xong', 1400), ('hết giờ', 600)]"])

    lab_pr = practice_scene(sc, "Tự làm: mã hoá tay một bản tin ba trường", practice_steps2(
        st, "BNX", "L02",
        """<p><b>Đề</b> (số minh hoạ): bản tin lần rút ATM có ba trường.</p>
<ul><li>trường <b>1</b>, kiểu dây 0: <b>20</b></li><li>trường <b>6</b>, kiểu dây 0: <b>70000</b></li><li>trường <b>7</b>, kiểu dây 2: chuỗi <code>ATM01</code></li></ul>
<p>Viết <code>mau.py</code> có <code>varint</code>, <code>field</code> như trong bài, ghép ba trường thành <code>m</code>, rồi in <code>m.hex(" ")</code> và <code>số byte</code>.</p>""",
        """Bây giờ tới phần bạn tự làm. Bản tin lần rút tiền có ba trường: trường một mang hai mươi, trường sáu mang bảy mươi nghìn, trường bảy là chuỗi năm ký tự.
        Hãy viết hai hàm mã hoá như trong bài, ghép ba trường rồi in các byte thập lục phân và số byte, rồi dừng video để tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> khoá trường 6 là 6 × 8 + 0 = 48 = <code>30</code>; 70000 tách nhóm 7 bit thấp trước, byte đầu và byte giữa bật bit 8.
Chuỗi 5 ký tự mã là <code>3a 05</code> rồi 5 byte chữ. Lời giải ở <code>labs/BNX/L02/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, khoá trường sáu bằng sáu nhân tám, là ba mươi thập lục phân, và số bảy mươi nghìn tách nhóm bảy bit thấp trước.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L02")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("tệp .proto là hợp đồng", "trên dây chỉ có số hiệu", "khoá = số hiệu và kiểu dây", "không đổi, không dùng lại số hiệu", "hạn chót đi theo cả chuỗi"),
          """Trên đường truyền chỉ có số hiệu ghép với kiểu dây thành khoá, nên không bao giờ đổi hay dùng lại số hiệu. Mỗi lời gọi mang theo thời gian còn lại để cả chuỗi dừng đúng hạn."""),
        S("""<div class='box key'><b>Tư duy:</b> bản tin nhị phân nhỏ vì bỏ hết những gì hai bên đã thoả thuận trước. Cái giá là <b>kỷ luật</b>: số hiệu là vĩnh viễn, và thời gian chờ của người dùng là của chung cả chuỗi.</div>
<p class="note">Bài sau: dịch vụ gọi nhau thì phải chứng minh mình là ai, bằng một mã truy cập có chữ ký.</p>""",
          """Điều cần mang theo: bản tin nhị phân nhỏ vì bỏ hết những gì hai bên đã thoả thuận trước. Cái giá là kỷ luật, vì số hiệu là vĩnh viễn.
          Bài sau là mã truy cập có chữ ký.""",
          focus=[1, 1, 2], forward_ref=True),
    ])
    scenes = [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec]
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            _merge_short(s_)
    return lesson("L02", "grpc_protobuf", "Bài 2 — gRPC và Protocol Buffers: bản tin nhị phân, số hiệu trường và hạn chót",
                  "curriculum/bnx.yaml L02; audit/bnx/verify_bnx.py L02; protobuf.dev Encoding và Language Guide (proto3) (đọc 2026-11-11); "
                  "grpc.io Core concepts, Deadlines, FAQ (đọc 2026-11-11)",
                  ["Mã hoá một bản tin Protocol Buffers bằng tay: khoá trường và số nguyên biến độ dài", "So kích thước với JSON",
                   "Nêu vì sao không được đổi số hiệu trường", "Truyền hạn chót qua chuỗi lời gọi",
                   "Đo tổng byte của bản tin nhị phân so với JSON khi số bản tin tăng từ 1 000 lên 100 000",
                   "Tự mã hoá một bản tin ba trường bằng Python và so với kết quả mong đợi"],
                  scenes,
                  assumes=["bnx_thap_luc_phan"],
                  covers=[(1, "example"), (2, "example"), (3, "pitfalls"), (4, "check"), (5, "quymo"), (6, "practice")])
