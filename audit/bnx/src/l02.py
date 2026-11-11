from lib import *

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

# Từ ngoại trong lời đọc: chỉ dùng khi đã dò phát âm (BRIEF mục 6). Chưa dò → nói bằng tiếng Việt, tên gốc chỉ trên màn hình.
SAY_WORDS = {"«gRPC»": "khung gọi hàm từ xa", "«PB»": "định dạng bản tin nhị phân", "«JSON»": "JSON"}   # JSON dò ASR 8/8; gRPC, Protocol Buffers không đạt 7/8 (x1.md)


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


def _bits(x, y, label, top, bot, col):
    return box(x, y, 300, 110, [label, top], col, size=26, bold=True) + txt(x + 150, y + 150, bot, 22, "middle", "#1f2937")


def build():
    hook = sc("hook", "hook", "Số tiền thành phí, phí thành số tiền, và khách chờ mãi", [
        S("""<p>Một dịch vụ nội bộ “dọn dẹp” tệp mô tả bản tin: đổi chỗ số hiệu của hai trường. Bản tin cũ còn trong hàng đợi được đọc lại (số minh hoạ):</p>"""
          + table(["trường", "bên gửi ghi", "bên nhận đọc ra"],
                  [["số tiền", "500 000", "<b class='red'>5 500</b>"], ["phí", "5 500", "<b class='red'>500 000</b>"]])
          + """<div class="box warn">Không có lỗi nào được báo: bản tin vẫn “hợp lệ”, chỉ có <b>nghĩa</b> bị đảo.</div>""",
          """Chào bạn, một đội nội bộ dọn dẹp tệp mô tả bản tin và đổi chỗ số hiệu của hai trường. Bản tin cũ còn trong hàng đợi được đọc lại, đây là số minh hoạ.
          Bên gửi ghi số tiền năm trăm nghìn, phí năm nghìn năm trăm. Bên nhận đọc ra số tiền năm nghìn năm trăm, và phí năm trăm nghìn.
          Không có lỗi nào được báo, vì bản tin vẫn hợp lệ, chỉ có nghĩa bị đảo.""",
          focus=[1, 1, "2.2", "2.3", 3]),
        S(table(["câu hỏi", "bài này trả lời"],
                [["bản tin nhị phân trông thế nào", "mã hoá bằng tay: khoá trường và số nguyên biến độ dài"],
                 ["vì sao số hiệu trường là bất khả xâm phạm", "giải mã bản tin cũ bằng tệp mô tả mới"],
                 ["vì sao cả chuỗi lời gọi phải dừng đúng hạn", "hạn chót 2 giây qua ba dịch vụ, mỗi dịch vụ 800 ms"]]),
          """Hôm nay ta trả lời ba câu hỏi. Bản tin nhị phân trông thế nào, ta sẽ tự mã hoá bằng tay từng byte.
          Vì sao không được đổi số hiệu trường, ta sẽ giải mã bản tin cũ để thấy.
          Và vì sao cả chuỗi lời gọi phải dừng đúng hạn, với hạn chót hai giây qua ba dịch vụ, mỗi dịch vụ cần tám trăm mi li giây.""",
          focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_pb_named(alg.bnx_pb_field(3, 0, 500000) + alg.bnx_pb_field(4, 0, 5500), {3: 'fee', 4: 'amount'}) == {'fee': 500000, 'amount': 5500}",
               "[s for s, _ in alg.bnx_deadline_chain(2000, [800, 800, 800])] == ['xong', 'xong', 'hết giờ']"])

    pre = sc("prereq", "prereq", "Trước hết: bốn phép tính trên byte", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Byte và bit", "1 byte = 8 bit, giá trị từ 0 đến 255", "1001 0110 = 128 + 16 + 4 + 2 = 150"],
                 ["② Thập lục phân", "mỗi byte viết bằng 2 chữ số cơ số 16 (a = 10 … f = 15)", "<code>96</code> = 9 × 16 + 6 = 150"],
                 ["③ Dịch trái, dịch phải", "<code>&lt;&lt; 3</code> nhân 2 ba lần; <code>&gt;&gt; 7</code> chia 128 bỏ phần dư", "1 &lt;&lt; 3 = 8; 150 &gt;&gt; 7 = 1"],
                 ["④ VÀ, HOẶC theo bit", "<code>&amp; 127</code> giữ 7 bit thấp; <code>|</code> bật thêm bit", "150 &amp; 127 = 22; 8 | 0 = 8; 22 | 128 = 150"]]),
          """Trước hết ta cần bốn phép tính trên byte. Một byte gồm tám bit, giá trị từ không đến hai trăm năm mươi lăm. Dãy một không không một, không một một không là một trăm hai mươi tám cộng mười sáu cộng bốn cộng hai, bằng một trăm năm mươi.
          Thập lục phân viết mỗi byte bằng hai chữ số cơ số mười sáu. Chín sáu thập lục phân là chín nhân mười sáu cộng sáu, bằng một trăm năm mươi.
          Dịch trái ba bit là nhân hai ba lần, nên một dịch trái ba bằng tám. Dịch phải bảy bit là chia một trăm hai mươi tám bỏ phần dư, nên một trăm năm mươi dịch phải bảy bằng một.
          Phép và với một trăm hai mươi bảy giữ lại bảy bit thấp, nên một trăm năm mươi và một trăm hai mươi bảy bằng hai mươi hai. Phép hoặc bật thêm bit, nên hai mươi hai hoặc một trăm hai mươi tám bằng một trăm năm mươi.""",
          focus=[0, "1.2", "1.2", "1.3", "1.3", "1.4", "1.4", "1.5", "1.5"]),
        S(table(["cách viết", "bản tin <code>{\"id\":150}</code>", "số byte"],
                [["chữ (JSON)", "<code>{</code> <code>\"</code> <code>i</code> <code>d</code> <code>\"</code> <code>:</code> <code>1</code> <code>5</code> <code>0</code> <code>}</code>", "10, mỗi ký tự 1 byte"],
                 ["nhị phân (Protocol Buffers)", "<code>08 96 01</code>", "3, tính ở phần sau"]])
          + """<p class="note">Hạn chót: thời điểm người gọi thôi chờ, thường cho bằng thời gian chờ tối đa tính từ lúc gọi. Ví dụ: chờ tối đa 2 000 ms = 2 giây.</p>""",
          """Bản tin chữ ghi từng ký tự, mỗi ký tự một byte. Bản tin mã số một trăm năm mươi ở «JSON» có mười ký tự, nên dài mười byte.
          Bản tin nhị phân chỉ cần ba byte, phần sau ta sẽ tự tính ra ba byte đó. Cuối cùng, hạn chót là thời điểm người gọi thôi chờ, thường cho bằng thời gian chờ tối đa tính từ lúc gọi, ví dụ hai nghìn mi li giây, tức hai giây.""",
          focus=["1.2", "1.2", "1.3", 2], clear=True),
    ], checks=["128 + 16 + 4 + 2 == 150 == int('10010110', 2) == int('96', 16) == 9 * 16 + 6",
               "(1 << 3, 150 >> 7, 150 & 127, 8 | 0, 22 | 128) == (8, 1, 22, 8, 150)",
               "alg.bnx_json_len({'id': 150}) == 10 and len(alg.bnx_pb_field(1, 0, 150)) == 3"])

    sym = sc("sym", "symbol", "Giải mã các từ của bản tin nhị phân", [
        S(code(PROTO_V1, "Tệp mô tả transfer.proto (proto3)"),
          """Đây là tệp mô tả bản tin, đóng vai hợp đồng như đặc tả ở bài trước. Dòng đầu nói tệp viết theo phiên bản ba của cú pháp tệp mô tả.
          Khối thứ nhất mô tả bản tin chuyển khoản gồm bốn trường. Mỗi trường có kiểu, tên, và sau dấu bằng là số hiệu trường: mã, tài khoản nhận, số tiền, phí mang số một, hai, ba, bốn.
          Khối cuối mô tả dịch vụ có một hàm tạo lệnh, nhận một bản tin chuyển khoản và trả lại một bản tin chuyển khoản.""",
          focus=[0, "2.1", ["2.3", "2.4", "2.5", "2.6", "2.7", "2.8"], ["2.4", "2.5", "2.6", "2.7"], ["2.10", "2.11", "2.12"]]),
        S(table(["từ", "nghĩa"],
                [["số hiệu trường", "số sau dấu <code>=</code>; trên dây chỉ có <b>số</b>, không có tên trường"],
                 ["kiểu dây (wire type)", "cách đọc phần giá trị: 0 = VARINT (số nguyên biến độ dài), 2 = LEN (độ dài rồi byte)"],
                 ["khoá trường", "<code>(số hiệu &lt;&lt; 3) | kiểu dây</code>, đứng trước mỗi giá trị"],
                 ["<code>reserved</code>", "giữ chỗ số hiệu hay tên đã xoá, cấm dùng lại"],
                 ["hạn chót (deadline)", "người gọi chờ tối đa bao lâu; quá hạn thì lời gọi bị huỷ với lỗi DEADLINE_EXCEEDED"]]),
          """Bảng này giải mã năm từ hay gặp với bản tin nhị phân. Số hiệu trường là số sau dấu bằng, và trên đường truyền chỉ có số này, không có tên trường.
          Kiểu dây cho biết cách đọc phần giá trị. Kiểu không là số nguyên biến độ dài, kiểu hai là độ dài rồi đến các byte.
          Khoá trường ghép số hiệu và kiểu dây, đứng trước mỗi giá trị. Từ giữ chỗ dùng để cấm dùng lại số hiệu hay tên đã xoá.
          Còn hạn chót là người gọi chờ tối đa bao lâu, quá hạn thì lời gọi bị huỷ với lỗi hết hạn.""",
          focus=[0, "1.2", "1.3", "1.3", "1.4", "1.5", "1.6"], clear=True),
        S(table(["kiểu gọi", "nghĩa", "ví dụ ngân hàng (minh hoạ)"],
                [["một-một (unary)", "gửi một yêu cầu, nhận một phản hồi", "tạo một lệnh chuyển"],
                 ["luồng từ máy chủ", "gửi một yêu cầu, đọc về một chuỗi bản tin", "tải sao kê nhiều dòng"],
                 ["luồng từ máy khách", "gửi một chuỗi bản tin, nhận một phản hồi", "gửi một lô lệnh chi lương"],
                 ["hai chiều", "hai bên cùng gửi chuỗi bản tin, độc lập nhau", "đẩy tỉ giá và nhận lệnh đặt"]])
          + """<p class="note">gRPC là một khung RPC (gọi hàm ở máy khác như gọi hàm trong máy), chạy trên HTTP/2 và mặc định dùng Protocol Buffers (nguồn: grpc.io).</p>""",
          """Khung gọi hàm từ xa giúp một dịch vụ gọi hàm nằm ở máy khác như gọi hàm trong cùng chương trình. Nó chạy trên HTTP phiên bản hai, mặc định dùng định dạng bản tin nhị phân ta vừa xem, và có bốn kiểu gọi.
          Một-một là gửi một yêu cầu, nhận một phản hồi, như tạo một lệnh chuyển. Luồng từ máy chủ là gửi một yêu cầu rồi đọc về cả chuỗi bản tin, như tải sao kê.
          Luồng từ máy khách là gửi một chuỗi bản tin rồi nhận một phản hồi, như gửi lô lệnh chi lương. Hai chiều là hai bên cùng gửi chuỗi bản tin, độc lập với nhau.""",
          focus=[2, 0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["alg.bnx_pb_key(1, 0) == (1 << 3) | 0 == 8", "alg.bnx_pb_key(2, 2) == (2 << 3) | 2 == 18"])

    intu = sc("intuition", "intuition", "Hình dung: ba byte mang số 150, và đồng hồ chạy qua ba dịch vụ", [
        S(svg(1500, 470,
              _bits(80, 60, "08", "0000 1 | 000", "số hiệu 1, kiểu dây 0", C_BLUE),
              _bits(560, 60, "96", "1 | 001 0110", "bit 8 = 1: còn byte sau; 7 bit = 22", C_AMBER),
              _bits(1040, 60, "01", "0 | 000 0001", "bit 8 = 0: byte cuối; 7 bit = 1", C_GREEN),
              arrow(385, 115, 555, 115), arrow(865, 115, 1035, 115),
              box(380, 300, 740, 100, ["giá trị = 22 + 1 × 128 = 150", "nhóm 7 bit đến trước là phần thấp"], C_PURPLE, size=26),
              arrow(710, 245, 650, 295, "#475569"), arrow(1190, 245, 1000, 295, "#475569")),
          """Hình đầu là ba byte của bản tin. Ở byte đầu tiên, ta có khoá của trường. Ba bit thấp bằng không là kiểu dây, phần còn lại bằng một là số hiệu trường.
          Sang byte thứ hai, bit cao nhất bằng một, nghĩa là còn byte sau, và bảy bit thấp mang hai mươi hai. Ở byte thứ ba, bit cao nhất bằng không, nên đó là byte cuối, mang số một.
          Nhóm bảy bit đến trước là phần thấp, nên giá trị bằng hai mươi hai cộng một nhân một trăm hai mươi tám, bằng một trăm năm mươi."""),
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
          """Hình thứ hai là đồng hồ của cả chuỗi. Người dùng chịu chờ hai nghìn mi li giây. Dịch vụ một dùng tám trăm, còn một nghìn hai trăm.
          Dịch vụ hai dùng tám trăm nữa, còn bốn trăm. Dịch vụ ba cần tám trăm nhưng chỉ còn bốn trăm, nên nó hết giờ đúng ở vạch hạn chót."""),
    ], checks=["22 + 1 * 128 == 150", "0x96 & 127 == 22 and 0x96 >= 128 and 0x01 < 128",
               "2000 - 800 == 1200 and 1200 - 800 == 400 and 800 > 400"])

    form = sc("formula", "formula", "Suy ra từng bước: mã hoá một trường, rồi chia hạn chót", [
        S("""<p><b>Bước 1. Khoá trường.</b> Bên nhận đọc khoá trước, rồi mới biết đọc phần sau thế nào. Có 6 kiểu dây (0 đến 5), vừa trong <b>3 bit</b>, nên khoá là <code>(số hiệu &lt;&lt; 3) | kiểu dây</code>. Dịch trái 3 bit là nhân 8; kiểu dây nhỏ hơn 8 nên phép HOẶC chính là phép cộng:</p>
$$\\text{khoá} = \\text{số hiệu} \\times 8 + \\text{kiểu dây}$$
<span class='note'>Làm thử: trường 1, kiểu 0 → 1 × 8 + 0 = 8 = <code>08</code>; trường 2, kiểu 2 → 2 × 8 + 2 = 18 = <code>12</code>.</span>""",
          """Bước một là cách ghép khoá cho mỗi trường. Bên nhận phải đọc khoá trước, rồi mới biết đọc phần sau thế nào. Có sáu kiểu dây, từ không đến năm, vừa trong ba bit.
          Vì vậy khoá bằng số hiệu dịch trái ba bit, rồi hoặc với kiểu dây. Dịch trái ba bit là nhân tám, và vì kiểu dây nhỏ hơn tám nên phép hoặc chính là phép cộng.
          Làm thử, trường một kiểu không cho tám. Trường hai kiểu hai cho mười tám, viết thập lục phân là một hai.""",
          focus=[1, 1, 1, 1, 2, 3, 3]),
        S("""<p><b>Bước 2. Số nguyên biến độ dài (varint).</b> Số nhỏ thì nên tốn ít byte. Mỗi byte chỉ mang <b>7 bit</b> giá trị; bit thứ 8 bằng 1 nghĩa là “còn byte sau”. Nhóm 7 bit thấp đi trước.</p>
<span class='note'>Làm thử: 5 nhỏ hơn 128 → 1 byte <code>05</code>; 150 lớn hơn 127 → phải 2 byte.</span>""",
          """Bước hai là số nguyên biến độ dài. Vì số nhỏ thì nên tốn ít byte, mỗi byte chỉ mang bảy bit giá trị, còn bit thứ tám bằng một nghĩa là còn byte sau. Nhóm bảy bit thấp luôn được ghi ra trước tiên.
          Làm thử, năm nhỏ hơn một trăm hai mươi tám nên chỉ cần một byte. Một trăm năm mươi lớn hơn một trăm hai mươi bảy nên phải dùng hai byte.""",
          focus=[1, 1, 1, 2, 2], clear=True),
        S("""<p><b>Bước 3. Chuỗi (kiểu dây 2).</b> Chữ không có “dấu kết thúc”, nên trước các byte phải ghi <b>độ dài</b>: khoá, độ dài, rồi các byte.</p>
<span class='note'>Làm thử: <code>"0123456789"</code> → khoá <code>12</code>, độ dài 10 = <code>0a</code>, 10 byte chữ → 1 + 1 + 10 = 12 byte.</span>""",
          """Bước ba là chuỗi, dùng kiểu dây hai. Vì bên nhận không biết chuỗi dừng ở đâu, trước các byte phải ghi độ dài. Thứ tự là khoá, độ dài, rồi các byte.
          Làm thử, chuỗi mười chữ số có khoá một hai, độ dài mười viết là không a, rồi mười byte chữ, tổng cộng mười hai byte.""",
          focus=[1, 1, 1, 2], clear=True),
        S("""<p><b>Bước 4. Hạn chót đi theo lời gọi.</b> Người dùng chỉ chờ một lần, nên mỗi dịch vụ phải biết người dùng <b>còn</b> chờ bao lâu:</p>
$$\\text{còn lại} = \\text{hạn chót} - \\text{thời gian đã dùng}$$
<span class='note'>Làm thử: 2 000 − 800 = 1 200 ms cho dịch vụ 2; 1 200 − 800 = 400 ms cho dịch vụ 3, mà nó cần 800 → hết giờ.</span>""",
          """Bước bốn là cách chia hạn chót qua chuỗi lời gọi. Người dùng chỉ chờ một lần, nên mỗi dịch vụ phải biết người dùng còn chờ bao lâu. Thời gian còn lại bằng hạn chót trừ thời gian đã dùng.
          Làm thử, dịch vụ hai nhận hai nghìn trừ tám trăm, bằng một nghìn hai trăm. Dịch vụ ba nhận một nghìn hai trăm trừ tám trăm, bằng bốn trăm, mà nó cần tám trăm, nên hết giờ.""",
          focus=[1, 1, 2, 3, 3], clear=True),
    ], checks=["alg.bnx_pb_key(1, 0) == 8 and alg.bnx_pb_key(2, 2) == 18 == 0x12", "len(alg.bnx_pb_varint(5)) == 1 and len(alg.bnx_pb_varint(150)) == 2",
               "alg.bnx_pb_field(2, 2, '0123456789')[:2].hex() == '120a' and len(alg.bnx_pb_field(2, 2, '0123456789')) == 12",
               "alg.bnx_deadline_chain(2000, [800, 800, 800]) == [('xong', 2000), ('xong', 1200), ('hết giờ', 400)]"])

    ex = sc("example", "example", "Ví dụ trường số 1 mang 150, từng phép tính", [
        S("""<p>Trường số 1, kiểu dây 0, giá trị 150. Khoá theo bước 1:</p>
$$① \\; \\text{khoá} = 1 \\times 8 + 0 = \\hl{8} = \\texttt{08}$$""",
          """Phép tính thứ nhất, khoá của trường số một, kiểu dây không. Theo bước một, một nhân tám cộng không bằng tám, viết thập lục phân là không tám."""),
        S("""<p>Tách 150 thành nhóm 7 bit (<code>150 &amp; 127</code> và <code>150 &gt;&gt; 7</code>):</p>
$$② \\; 150 = 1 \\times 128 + \\hl{22}$$""",
          """Phép tính thứ hai, tách một trăm năm mươi thành các nhóm bảy bit. Vì một trăm năm mươi bằng một nhân một trăm hai mươi tám cộng hai mươi hai, nhóm thấp là hai mươi hai và phần còn lại là một."""),
        S("""<p>Còn phần 1 ở sau nên byte đầu bật bit 8 (cộng 128):</p>
$$③ \\; 22 + 128 = 150 = \\texttt{96}, \\quad 1 = \\texttt{01} \\;\\Rightarrow\\; \\hlg{\\texttt{08 96 01}}: 3 \\text{ byte}$$
<p class="note">Khớp ví dụ trong trang “Encoding” của protobuf.dev.</p>""",
          """Phép tính thứ ba, vì còn phần một ở sau, byte đầu bật bit tám, hai mươi hai cộng một trăm hai mươi tám bằng một trăm năm mươi, là chín sáu. Còn byte sau mang phần còn lại, là không một.
          Ghép với khoá ở phép thứ nhất, bản tin là không tám, chín sáu, không một, dài ba byte, đúng như ví dụ trên trang hướng dẫn mã hoá chính thức.""",
          focus=[[1, 2], [2, 3], 3]),
        S("""<p>Bản tin chữ <code>{"id":150}</code> có 10 ký tự, tức 10 byte:</p>
$$④ \\; 10 - 3 = \\hl{7} \\text{ byte ít hơn}$$""",
          """Phép tính thứ tư, cùng nội dung ở «JSON» dài mười byte. Mười trừ ba bằng bảy, nên bản tin nhị phân ít hơn bảy byte, vì nó không ghi tên trường và không ghi số dưới dạng chữ.""",
          clear=True),
        S("""<p>Thêm trường 2 là chuỗi <code>"0123456789"</code>: khoá <code>12</code>, độ dài <code>0a</code>, rồi 10 byte chữ.</p>
$$⑤ \\; 1 + 1 + 10 = 12 \\text{ byte}, \\qquad 3 + 12 = \\hlg{15} \\text{ byte cả bản tin}$$""",
          """Phép tính thứ năm, thêm trường số hai là chuỗi tài khoản mười chữ số. Theo bước ba, nó tốn một byte khoá, một byte độ dài và mười byte chữ, tức mười hai byte.
          Cộng với ba byte ở phép thứ ba, cả bản tin dài mười lăm byte."""),
    ], checks=["alg.bnx_pb_varint(alg.bnx_pb_key(1, 0)).hex() == '08'", "(150 & 127, 150 >> 7) == (22, 1)",
               "alg.bnx_pb_field(1, 0, 150).hex() == '089601' and (22 | 128) == 0x96",
               "alg.bnx_json_len({'id': 150}) - len(alg.bnx_pb_field(1, 0, 150)) == 7",
               "len(alg.bnx_pb_field(1, 0, 150) + alg.bnx_pb_field(2, 2, '0123456789')) == 15"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cho máy mã hoá, giải mã và đếm giờ", [
        S(code(ENCODE_PY, "Chương trình Python mã hoá", lines=ENCODE_PARTS["so"]),
          """Kiểm bằng đường khác, ta cho máy làm lại, vì máy không mắc lỗi cộng nhầm như tính tay. Hàm thứ nhất mã một số nguyên, lặp tới khi không còn phần nào.
          Dòng gán hai biến cùng lúc: b nhận bảy bit thấp, tức phép và với một trăm hai mươi bảy, còn n nhận phần còn lại sau khi dịch phải bảy bit.
          Dòng sau chọn một trong hai giá trị ngay trên một dòng: nếu còn phần sau thì bật bit tám, tức hoặc với một trăm hai mươi tám, còn hết thì giữ nguyên.
          Hàm thứ hai ghép khoá trường với phần giá trị. Rồi ta mã trường số một mang một trăm năm mươi và in ra.""",
          focus=[0, ["2.1", "2.2", "2.3", "2.6", "2.7"], "2.4", "2.5", ["2.9", "2.10"], ["2.11", "2.12"]]),
        S(code(ENCODE_PY, "(tiếp) Trường chuỗi và bản tin chữ", lines=ENCODE_PARTS["chuoi"])
          + out(ENCODE_OUT),
          """Phần tiếp đổi chuỗi tài khoản thành các byte, mã thành trường số hai, rồi đếm byte của bản tin chữ để so kích thước. Đây là kết quả chạy thật của chương trình trên máy.
          Dòng đầu là không tám, chín sáu, không một, ba byte. Dòng hai là mười hai byte của trường chuỗi. Dòng ba là mười byte của bản tin chữ, nên cả ba số khớp năm phép tính tay.""",
          focus=[2, 3, "4.1", "4.2", "4.3"], clear=True),
        S(code(DECODE_PY, "Giải mã: đọc số nguyên biến độ dài", lines=DECODE_PARTS["varint"]),
          """Đường khác thứ hai là giải mã ngược lại, vì mã đúng thì giải ra phải được đúng số ban đầu. Dòng thứ hai cho cả giá trị và độ dịch cùng bằng không trong một lệnh. Hàm này đọc từng byte, lấy bảy bit thấp đặt vào đúng chỗ, và dừng khi gặp byte có bit tám bằng không.""",
          focus=[0, "2.2", ["2.4", "2.5", "2.6", "2.7", "2.8", "2.9"]], clear=True),
        S(code(DECODE_PY, "(tiếp) Giải mã cả bản tin", lines=DECODE_PARTS["decode"]),
          """Hàm giải mã đọc khoá, rồi tách số hiệu bằng dịch phải ba, tách kiểu dây bằng phép và với bảy, vì kiểu dây nằm ở ba bit thấp. Kiểu không thì đọc một số, kiểu hai thì đọc độ dài rồi cắt đúng chừng ấy byte. Các dòng có dấu phẩy bên trái dấu bằng là gán nhiều biến cùng lúc, ví dụ vị trí bằng không và kết quả là một từ điển rỗng.""",
          focus=[["2.4", "2.5"], ["2.6", "2.7", "2.8", "2.9", "2.10"], ["2.2", "2.5"]], clear=True),
        S(code(DECODE_PY, "(tiếp) Chạy thử", lines=DECODE_PARTS["thu"]) + out(DECODE_OUT),
          """Chạy thử trên hai bản tin vừa mã. Ba byte không tám, chín sáu, không một giải ra trường một bằng một trăm năm mươi. Mười hai byte giải ra trường hai là chuỗi mười chữ số, nên mã và giải mã khớp nhau.""",
          focus=[2, "4.1", "4.2"], clear=True),
        S(code(DEADLINE_PY, "Đếm giờ: truyền thời gian còn lại"),
          """Cuối cùng, ta mô phỏng hạn chót qua ba dịch vụ. Mỗi dịch vụ nhận thời gian còn lại, nếu cần nhiều hơn thì báo hết giờ, vì người dùng sẽ không chờ thêm.
          Vòng lặp gọi lần lượt ba dịch vụ, mỗi dịch vụ cần tám trăm mi li giây, và chuyển phần còn lại cho dịch vụ sau.""",
          focus=[0, ["2.2", "2.3", "2.4", "2.5"], ["2.8", "2.9", "2.10"]], clear=True),
        S(out(DEADLINE_OUT),
          """Kết quả chạy thật: dịch vụ một còn một nghìn hai trăm, dịch vụ hai còn bốn trăm.
          Dịch vụ ba hết giờ vì chỉ còn bốn trăm mi li giây, khớp bước bốn.""",
          focus=[["2.1", "2.2"], "2.3"], clear=True),
    ], checks=["alg.bnx_pb_field(1, 0, 150).hex() == '089601'", "alg.bnx_pb_field(2, 2, '0123456789').hex() == '120a30313233343536373839'",
               "alg.bnx_json_len({'id': 150}) == 10", "alg.bnx_pb_decode(bytes.fromhex('089601')) == {1: 150}",
               "alg.bnx_pb_decode(bytes.fromhex('120a30313233343536373839')) == {2: b'0123456789'}",
               "alg.bnx_deadline_chain(2000, [800, 800, 800]) == [('xong', 2000), ('xong', 1200), ('hết giờ', 400)]"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người mới).</b> “gRPC luôn nhanh hơn REST.” Lợi thật nằm ở bản tin nhỏ, gọi theo luồng, và hợp đồng chặt.
<br><span class="note">Một lời gọi 100 ms mà 95 ms là truy vấn cơ sở dữ liệu (số minh hoạ): đổi cách mã bản tin chỉ có thể bớt trong 100 − 95 = 5 ms còn lại.</span></div>""",
          """Lỗi thứ nhất, của người mới, là tin rằng «gRPC» luôn nhanh hơn REST. Lợi thật của nó nằm ở bản tin nhỏ, gọi theo luồng, và hợp đồng chặt.
          Ví dụ minh hoạ, một lời gọi mất một trăm mi li giây mà chín mươi lăm là truy vấn cơ sở dữ liệu. Đổi cách mã bản tin chỉ có thể bớt trong năm mi li giây còn lại."""),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> “Dọn dẹp” tệp mô tả bằng cách đổi số hiệu, hoặc xoá trường rồi dùng lại số của nó.</div>"""
          + code(PROTO_BAD),
          """Lỗi thứ hai, của người đã đi làm, là dọn dẹp tệp mô tả bằng cách đổi số hiệu. Ở đây phí được đổi sang số ba, số tiền sang số bốn, trông gọn hơn.
          Nhưng bản tin cũ trên đường truyền chỉ mang số, không mang tên, nên bên đọc theo tệp mới sẽ hiểu sai.""",
          focus=[1, ["2.6", "2.7"], 2], clear=True),
        S(code(RENUM_PY, "Giải mã bản tin cũ bằng hai tệp mô tả") + out(RENUM_OUT),
          """Ta chứng minh bằng giải mã, dùng lại hàm giải mã lúc nãy, rồi tra từng số hiệu sang tên theo bảng của tệp cũ và tệp mới. Bản tin cũ có mã một trăm năm mươi, số tiền năm trăm nghìn ở trường ba, phí năm nghìn năm trăm ở trường bốn.
          Đọc theo tệp mô tả cũ thì mọi trường đều đúng. Đọc theo tệp đã đổi số hiệu thì phí thành năm trăm nghìn, số tiền thành năm nghìn năm trăm, mà không có lỗi nào được báo.""",
          focus=[2, ["2.1", "4.1"], "4.2", "4.3"], clear=True),
        S(code(PROTO_RESERVED, "Xoá trường đúng cách: giữ chỗ bằng reserved")
          + """<p class="note">Số hiệu 2 và tên <code>to_account</code> bị khoá lại: ai thêm trường mới dùng số 2 sẽ bị trình biên dịch .proto từ chối.</p>""",
          """Cách chữa là không bao giờ đổi hay dùng lại số hiệu. Muốn xoá trường tài khoản nhận, ta khai giữ chỗ cho số hai và cho tên của nó.
          Vì vậy nếu sau này ai thêm trường mới dùng số hai, trình biên dịch tệp mô tả sẽ từ chối ngay.""",
          focus=[2, ["2.4", "2.5"], 3], clear=True),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Mỗi dịch vụ tự đặt lại hạn 2 giây, hoặc không đặt hạn nào (mặc định gRPC <b>không</b> có hạn chót).
<br><span class="note">Đặt lại 2 giây: chuỗi chạy 3 × 800 = 2 400 ms; người dùng đã bỏ cuộc ở 2 000 ms, dịch vụ 3 vẫn làm thêm 400 ms vô ích. Không đặt hạn: một dịch vụ treo kéo cả chuỗi treo theo.</span></div>""",
          """Lỗi thứ ba, cũng của người đã đi làm, là mỗi dịch vụ tự đặt lại hạn hai giây, hoặc không đặt hạn nào, vì mặc định «gRPC» không có hạn chót.
          Đặt lại hai giây thì chuỗi chạy ba nhân tám trăm, bằng hai nghìn bốn trăm mi li giây. Người dùng đã bỏ cuộc ở hai nghìn, nên dịch vụ ba làm thêm bốn trăm vô ích.
          Còn không đặt hạn thì một dịch vụ treo sẽ kéo cả chuỗi treo theo.""",
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
          """Bây giờ tới phần bạn tự làm bài. Câu một, mã hoá bằng tay trường số ba mang số ba trăm, kiểu dây không.
          Câu hai, hạn chót ba giây, chuỗi bốn dịch vụ, mỗi dịch vụ cần tám trăm mi li giây và có truyền thời gian còn lại. Dịch vụ nào hết giờ, khi còn bao nhiêu?
          Câu ba là một quyết định có đánh đổi rõ ràng. Một chỗ là API cho ví điện tử của đối tác gọi vào, chỗ kia là lời gọi nội bộ giữa hai dịch vụ. Hãy dừng video lại và tự làm ra giấy trước.""",
          pause=25, focus=[0, "1.2", "1.3", "1.3", "1.4", "1.4", 0]),
        S("""$$\\text{khoá} = 3 \\times 8 + 0 = 24 = \\texttt{18}; \\quad 300 = 2 \\times 128 + 44; \\quad 44 + 128 = 172 = \\texttt{ac}, \\; 2 = \\texttt{02}$$
<div class="box key">Câu 1: <code>18 ac 02</code>, 3 byte.</div>""",
          """Bây giờ ta xem đáp án của câu một. Khoá bằng ba nhân tám cộng không, bằng hai mươi tư, viết thập lục phân là một tám. Ba trăm bằng hai nhân một trăm hai mươi tám cộng bốn mươi bốn.
          Nhóm thấp bốn mươi bốn bật bit tám thành một trăm bảy mươi hai, là a c, còn phần hai là không hai. Vậy bản tin là một tám, a c, không hai, dài ba byte.""",
          focus=[0, 1, 1, 1, 2]),
        S(table(["dịch vụ", "còn lại khi bắt đầu", "cần", "kết quả"],
                [["1", "3 000", "800", "xong"], ["2", "3 000 − 800 = 2 200", "800", "xong"], ["3", "2 200 − 800 = 1 400", "800", "xong"],
                 ["4", "1 400 − 800 = 600", "800", "<b class='red'>hết giờ</b>"]]),
          """Bây giờ ta xem đáp án của câu hai. Dịch vụ một nhận ba nghìn, dịch vụ hai nhận hai nghìn hai trăm, dịch vụ ba nhận một nghìn bốn trăm, cả ba đều xong.
          Dịch vụ bốn chỉ còn sáu trăm mà cần tám trăm, nên dịch vụ bốn hết giờ khi còn sáu trăm mi li giây.""",
          focus=[0, ["1.2", "1.3", "1.4"], "1.5"]),
        S(table(["chỗ", "chọn", "được", "mất"],
                [["API cho ví đối tác", "REST + JSON + OpenAPI", "đối tác nào cũng gọi được, đọc bản tin bằng mắt, trang mô tả sẵn", "bản tin to hơn, kiểm lược đồ phải tự bật"],
                 ["chuyển tiền → chống gian lận (nội bộ)", "gRPC", "bản tin nhỏ, hợp đồng .proto chặt, có luồng, hạn chót đi theo lời gọi", "cần công cụ để đọc bản tin; phải giữ kỷ luật số hiệu"]]),
          """Bây giờ ta xem đáp án của câu ba. Với API cho đối tác, chọn REST, «JSON» và đặc tả OpenAPI, vì đối tác nào cũng gọi được và đọc được bản tin. Đổi lại bản tin to hơn, và kiểm lược đồ phải tự bật.
          Với lời gọi nội bộ, «gRPC» hợp hơn vì bản tin nhỏ, hợp đồng chặt, có luồng và có hạn chót đi theo lời gọi. Đổi lại phải có công cụ để đọc bản tin, và giữ kỷ luật số hiệu.""",
          focus=[0, "1.2", "1.2", "1.3", "1.3"]),
    ], checks=["alg.bnx_pb_field(3, 0, 300).hex() == '18ac02' and alg.bnx_pb_key(3, 0) == 24 and (300 & 127, 44 | 128, 300 >> 7) == (44, 172, 2)",
               "alg.bnx_deadline_chain(3000, [800] * 4) == [('xong', 3000), ('xong', 2200), ('xong', 1400), ('hết giờ', 600)]"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("tệp .proto là hợp đồng", "trên dây chỉ có số hiệu", "khoá = số hiệu và kiểu dây", "không đổi, không dùng lại số hiệu", "hạn chót đi theo cả chuỗi"),
          """Ta tổng kết lại chuỗi logic của cả bài. Tệp mô tả là hợp đồng, nhưng trên đường truyền chỉ có số hiệu, ghép với kiểu dây thành khoá trường.
          Vì vậy không bao giờ đổi hay dùng lại số hiệu. Và mỗi lời gọi mang theo thời gian còn lại, để cả chuỗi dừng đúng hạn."""),
        S("""<div class='box key'><b>Tư duy:</b> bản tin nhị phân nhỏ vì bỏ hết những gì hai bên đã thoả thuận trước. Cái giá là <b>kỷ luật</b>: số hiệu là vĩnh viễn, và thời gian chờ của người dùng là của chung cả chuỗi.</div>
<p class="note">Bài sau: dịch vụ gọi nhau thì phải chứng minh mình là ai, bằng một mã truy cập có chữ ký.</p>""",
          """Đây là điều cần mang theo sau bài này. Bản tin nhị phân nhỏ vì nó bỏ hết những gì hai bên đã thoả thuận trước. Cái giá là kỷ luật: số hiệu là vĩnh viễn, và thời gian chờ của người dùng là của chung cả chuỗi.
          Ở bài sau, khi các dịch vụ gọi nhau, mỗi bên phải chứng minh mình là ai bằng một mã truy cập có chữ ký.""",
          focus=[1, 1, 1, 2], forward_ref=True),
    ])
    return lesson("L02", "grpc_protobuf", "Bài 2 — gRPC và Protocol Buffers: bản tin nhị phân, số hiệu trường và hạn chót",
                  "curriculum/bnx.yaml L02; audit/bnx/verify_bnx.py L02; protobuf.dev Encoding và Language Guide (proto3) (đọc 2026-11-11); "
                  "grpc.io Core concepts, Deadlines, FAQ (đọc 2026-11-11)",
                  ["Mã hoá một bản tin Protocol Buffers bằng tay: khoá trường và số nguyên biến độ dài", "So kích thước với JSON",
                   "Giải thích vì sao không được đổi số hiệu trường", "Truyền hạn chót qua chuỗi lời gọi"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
