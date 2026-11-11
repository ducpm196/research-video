import re

from lib import *

# ── Mã hiện trên màn hình (chạy nguyên văn: audit/bnx/screen/l10.yaml, audit/bnx/ver/l10.py) ──
COMPACT_PY = """
log = [("A", 100), ("B", 200), ("A", 150), ("C", 50),
       ("B", 180), ("A", 120), ("C", 75), ("B", 260)]
def compact(log):
    last = {}
    for off, (key, val) in enumerate(log):
        last[key] = (off, val)        # bản sau đè bản trước
    return sorted((off, k, v) for k, (off, v) in last.items()
                  if v is not None)   # bia mộ: khoá biến mất
print(len(log), "->", compact(log))
log.append(("C", None))               # bia mộ cho C
print(len(log), "->", compact(log))
"""

SCHEMA_JSON = """
{"type": "record", "name": "Transfer", "fields": [
  {"name": "account", "type": "string"},
  {"name": "amount", "type": "long"},
  {"name": "channel", "type": "string", "default": "APP"}
]}
"""

SCHEMA_PY = """
v1 = {"account": False, "amount": False}  # trường: có mặc định?
v2 = {**v1, "channel": True}              # thêm trường có mặc định
v3 = {**v1, "fee": False}                 # thêm trường không mặc định
def backward_ok(new, old):
    # bên đọc dùng lược đồ mới có đọc được dữ liệu cũ không?
    bad = [f for f, has_default in new.items()
           if f not in old and not has_default]
    return len(bad) == 0, bad
print("v2:", backward_ok(v2, v1))
print("v3:", backward_ok(v3, v1))
"""

TOPIC_PY = """
def match(pattern, key):
    p, k = pattern.split("."), key.split(".")
    def m(i, j):
        if i == len(p):
            return j == len(k)
        if p[i] == "#":                       # không hoặc nhiều từ
            return any(m(i + 1, t) for t in range(j, len(k) + 1))
        ok = j < len(k) and p[i] in ("*", k[j])   # * đúng một từ
        return ok and m(i + 1, j + 1)
    return m(0, 0)
for pat in ["payment.*.napas", "payment.#", "payment.*"]:
    print(pat, match(pat, "payment.vn.napas"))
"""

CHECK_PY = """
def compact_back(log):
    seen, kept = set(), []
    for off in range(len(log) - 1, -1, -1):   # đi ngược từ cuối
        key, val = log[off]
        if key not in seen:
            seen.add(key)
            if val is not None:
                kept.append((off, key, val))
    return sorted(kept)
log = [("A", 100), ("B", 200), ("A", 150), ("C", 50),
       ("B", 180), ("A", 120), ("C", 75), ("B", 260)]
print(len(compact_back(log)), len(compact_back(log + [("C", None)])))
"""

# Đầu ra THẬT (.venv Python 3.13.5, 2026-11-11)
COMPACT_OUT = """
8 -> [(5, 'A', 120), (6, 'C', 75), (7, 'B', 260)]
9 -> [(5, 'A', 120), (7, 'B', 260)]
"""
SCHEMA_OUT = """
v2: (True, [])
v3: (False, ['fee'])
"""
TOPIC_OUT = """
payment.*.napas True
payment.# True
payment.* False
"""
CHECK_OUT = """
3 2
"""
# Đầu ra THẬT của Kafka 3.9.0 (ảnh apache/kafka:3.9.0, Docker, 2026-11-11): chủ đề cleanup.policy=compact, segment.ms=1000,
# min.cleanable.dirty.ratio=0.01; ghi 9 bản ghi (8 + bia mộ C), thêm Z:1 để đẩy đoạn cũ ra khỏi đoạn đang ghi, chờ bộ dọn chạy,
# đọc bằng kafka-console-consumer --property print.offset=true --property null.literal=TOMBSTONE. Tái hiện ở audit/bnx/ver/l10.py.
KAFKA_OUT = """
Offset:5	A	120
Offset:7	B	260
Offset:8	C	TOMBSTONE
Offset:9	Z	1
"""


def stf(show, say, **kw):
    """Lời đọc có nhãn [n] / [n.m] trước câu: mọi câu sau nhãn trỏ tới phần đó (focus); câu trước nhãn đầu tiên trỏ 0 (cả khối)."""
    parts = re.split(r"\[(\d+(?:\.\d+)?)\]", say)
    chunks = [("0", parts[0])] + [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
    focus, text = [], []
    for tag, ch in chunks:
        ch = " ".join(ch.split())
        if not ch:
            continue
        n = len(lv.sentences(fix_say(ch)))
        focus += [tag if "." in tag else int(tag)] * n
        text.append(ch)
    return st(show, " ".join(text), focus=focus, **kw)


LOG = "alg.bnx_l10_log()"
TOMB = "(alg.bnx_l10_log() + [('C', None)])"
BIND = "[('napas', 'payment.*.napas'), ('audit', 'payment.#'), ('cu', 'payment.*')]"


def log_row(y, items, x0=40, w=165):
    out = []
    for i, (off, k, v) in enumerate(items):
        col = C_GRAY if v is None else {"A": C_BLUE, "B": C_GREEN, "C": C_AMBER, "Z": C_PURPLE}[k]
        out.append(box(x0 + i * w, y, 150, 86, [f"offset {off}", f"{k}: {'bia mộ' if v is None else v}"], col, size=21))
    return "".join(out)


def build():
    full = [(i, k, v) for i, (k, v) in enumerate([("A", 100), ("B", 200), ("A", 150), ("C", 50), ("B", 180), ("A", 120), ("C", 75), ("B", 260)])]
    hook = sc("hook", "hook", "Vì sao khởi động lại mà phải đọc hàng triệu bản ghi chỉ để biết vài số dư?", [
        stf("""<p>Dịch vụ tra số dư nhanh khởi động lại, phải đọc lại chủ đề Kafka <code>balances</code> từ đầu để biết số dư mới nhất.</p>
<p>Trong ví dụ: <b>8</b> bản ghi cho <b>3</b> tài khoản. Ngoài đời là hàng triệu bản ghi, mà chỉ cần <b>bản cuối</b> của mỗi tài khoản.</p>
<div class="box key">Cùng lúc: bên nhận lên lược đồ mới có thêm một trường bắt buộc, đọc lại thông điệp cũ thiếu trường đó thì vỡ; và thông báo NAPAS phải tới đúng hàng đợi.</div>""",
            """[1] Chào bạn, dịch vụ tra số dư nhanh vừa khởi động lại, và phải đọc lại chủ đề số dư trong Kafka từ đầu để biết số dư mới nhất.
            [2] Trong ví dụ có tám bản ghi cho ba tài khoản. Ngoài đời là hàng triệu bản ghi, trong khi chỉ cần bản cuối của mỗi tài khoản.
            [3] Cùng lúc đó, bên nhận lên lược đồ mới có thêm một trường bắt buộc, đọc lại thông điệp cũ thiếu trường đó thì vỡ. Còn thông báo NAPAS phải tới đúng hàng đợi."""),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["giữ nhật ký gọn mà không mất số dư mới nhất", "nén nhật ký theo khoá; bia mộ để xoá khoá"],
                   ["đổi lược đồ thông điệp mà không làm vỡ bên nhận", "kho lược đồ kiểm tương thích ngược trước khi cho dùng"],
                   ["một thông điệp tới đúng các hàng đợi cần nó", "sàn chủ đề của RabbitMQ, mẫu * và #"],
                   ["luồng nào dùng Kafka, luồng nào dùng RabbitMQ", "giữ để đọc lại hay xoá khi đã xác nhận"]]),
            """Hôm nay ta trả lời bốn câu hỏi. [1.2] Thứ nhất, giữ nhật ký gọn mà không mất số dư mới nhất, câu trả lời là nén nhật ký theo khoá.
            [1.3] Thứ hai, đổi lược đồ thông điệp mà không làm vỡ bên nhận, câu trả lời là kho lược đồ kiểm tương thích trước khi cho dùng.
            [1.4] Thứ ba, đưa một thông điệp tới đúng các hàng đợi cần nó, câu trả lời là sàn chủ đề với hai ký hiệu sao và thăng.
            [1.5] Thứ tư, khi nào chọn Kafka, khi nào chọn hàng đợi có sàn, tuỳ ta cần giữ thông điệp để đọc lại hay xoá khi đã xác nhận.""", clear=True),
    ], checks=[f"len({LOG}) == 8 and len({{k for k, _ in {LOG}}}) == 3"])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Nhật ký chỉ thêm và offset", "Kafka ghi nối vào cuối, mỗi bản ghi có số thứ tự (offset) không đổi", "offset 0, 1, …, 7"],
                   ["② Khoá thông điệp", "nhãn đi kèm, ví dụ số tài khoản; cùng khoá vào cùng phân vùng nên giữ thứ tự", "khoá A, B, C"],
                   ["③ Tương thích ngược / xuôi", "ngược: bên đọc dùng lược đồ mới đọc được dữ liệu cũ; xuôi: bên đọc cũ đọc được dữ liệu mới", "thêm trường có mặc định"],
                   ["④ Hàng đợi và xác nhận", "bên nhận lấy thông điệp, xử lý xong thì báo đã xong (ack)", "xác nhận rồi mới lấy tiếp"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Kafka là nhật ký chỉ thêm, ghi nối vào cuối, và mỗi bản ghi có một số thứ tự không bao giờ đổi.
            [1.3] Khoá thông điệp là nhãn đi kèm, ví dụ số tài khoản. Cùng khoá thì vào cùng phân vùng, nên thứ tự theo khoá được giữ trong từng phân vùng.
            [1.4] Tương thích ngược nghĩa là bên đọc dùng lược đồ mới vẫn đọc được dữ liệu cũ. Tương thích xuôi là bên đọc cũ đọc được dữ liệu mới. Phần này chỉ nhắc lại.
            [1.5] Hàng đợi là nơi bên nhận lấy thông điệp ra, xử lý xong thì báo đã xong, gọi là xác nhận."""),
        st(svg(1000, 92, log_row(2, full[:6], x0=2, w=165))
           + """$$\\text{tài khoản A: offset } 0, 2, 5 \\Rightarrow \\text{bản cuối ở offset } 5$$""",
           """Một ví dụ về khoá. Tài khoản A có ba bản ghi ở các vị trí không, hai và năm, suy ra bản mới nhất của A nằm ở vị trí năm. Mũi tên kép đọc là suy ra.""",
           focus=[0, 2, 2]),
    ], checks=[f"[i for i, (k, _) in enumerate({LOG}) if k == 'A'] == [0, 2, 5]"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["log compaction (nén nhật ký)", "giữ ít nhất bản cuối của mỗi khoá; bật bằng <code>cleanup.policy=compact</code>"],
                   ["tombstone (bia mộ)", "bản ghi có khoá và giá trị rỗng (null): lệnh xoá khoá đó"],
                   ["<code>delete.retention.ms</code>", "thời gian giữ bia mộ trước khi dọn; mặc định 86 400 000 ms = 1 ngày"],
                   ["Schema Registry (kho lược đồ)", "nơi lưu các phiên bản lược đồ, kiểm tương thích trước khi nhận phiên bản mới; mức mặc định BACKWARD"],
                   ["exchange (sàn) loại topic", "nhận thông điệp kèm khoá định tuyến, chép tới mọi hàng đợi có mẫu khớp"],
                   ["routing key (khoá định tuyến)", "các từ nối bằng dấu chấm, tối đa 255 byte: <code>payment.vn.napas</code>"],
                   ["<code>*</code> và <code>#</code>", "<code>*</code> thay đúng một từ; <code>#</code> thay không hoặc nhiều từ"]]),
            """Bảng này giải mã bảy từ. [1.2] Nén nhật ký là giữ ít nhất bản cuối của mỗi khoá, bật bằng chính sách dọn kiểu nén.
            [1.3] Bia mộ là bản ghi có khoá nhưng giá trị rỗng, nghĩa là lệnh xoá khoá đó.
            [1.4] Thời gian giữ bia mộ mặc định là tám mươi sáu triệu bốn trăm nghìn mili giây, tức một ngày.
            [1.5] Kho lược đồ lưu các phiên bản lược đồ, và kiểm tương thích trước khi nhận phiên bản mới. Mức mặc định là tương thích ngược.
            [1.6] Sàn loại chủ đề nhận thông điệp kèm khoá định tuyến, rồi chép tới mọi hàng đợi có mẫu khớp.
            [1.7] Khoá định tuyến là các từ nối bằng dấu chấm, dài tối đa hai trăm năm mươi lăm byte.
            [1.8] Dấu sao thay đúng một từ, còn dấu thăng thay không hoặc nhiều từ."""),
    ], checks=["alg.bnx_ms_to_hours(86400000) == 24"])
    intu = sc("intuition", "intuition", "Hình dung: nén nhật ký, bia mộ và sàn chủ đề", [
        st(svg(1500, 440,
               txt(40, 30, "trước khi nén: 8 bản ghi", 24, "start", "#1f2937", True),
               log_row(50, full, x0=30, w=180),
               arrow(750, 150, 750, 230, "#475569", None),
               txt(780, 200, "giữ bản cuối của mỗi khoá, offset không đổi", 24, "start", "#475569"),
               txt(40, 265, "sau khi nén: 3 bản ghi", 24, "start", "#16a34a", True),
               log_row(285, [(5, "A", 120), (6, "C", 75), (7, "B", 260)], x0=930, w=180),
               txt(750, 425, "Nhật ký cắt thành nhiều tệp nối tiếp gọi là đoạn; đoạn cuối, nơi đang ghi thêm, không bao giờ bị nén", 24, "middle", "#1f2937", True)),
           """Hình đầu cho thấy nén nhật ký. Hàng trên là tám bản ghi của ba tài khoản theo thứ tự ghi.
           Bộ dọn chỉ giữ bản cuối của mỗi khoá, là A ở vị trí năm, C ở vị trí sáu, và B ở vị trí bảy. Vị trí không đổi, thứ tự cũng không đổi.
           Lưu ý, Kafka cắt nhật ký thành nhiều tệp nối tiếp gọi là đoạn, và đoạn cuối, nơi đang ghi thêm, không bao giờ bị nén, nên bên đọc luôn thấy đủ các bản mới ghi."""),
        st(svg(1500, 450,
               txt(40, 30, "thêm bia mộ cho C (offset 8)", 24, "start", "#1f2937", True),
               log_row(45, [(5, "A", 120), (6, "C", 75), (7, "B", 260), (8, "C", None)], x0=30, w=180),
               arrow(780, 90, 880, 90, "#475569", "nén"),
               log_row(45, [(5, "A", 120), (7, "B", 260), (8, "C", None)], x0=900, w=180),
               arrow(1170, 145, 1170, 245, "#475569"),
               txt(1190, 205, "sau delete.retention.ms", 22, "start", "#475569"),
               log_row(260, [(5, "A", 120), (7, "B", 260)], x0=990, w=180),
               txt(40, 330, "Bia mộ giữ thêm một thời gian để bên đọc", 24, "start", "#1f2937"),
               txt(40, 365, "đang chậm vẫn kịp thấy lệnh xoá, rồi mới bị dọn.", 24, "start", "#1f2937"),
               txt(750, 435, "Kết quả cuối: còn 2 bản ghi (A, B)", 26, "middle", "#16a34a", True)),
           """Hình thứ hai thêm một bia mộ cho tài khoản C ở vị trí tám. Lần nén kế tiếp bỏ bản cũ của C, chỉ còn A, B và bia mộ của C.
           Bia mộ được giữ thêm một thời gian, để bên đọc đang chậm vẫn kịp thấy lệnh xoá. Sau thời gian đó nó mới bị dọn, và nhật ký còn hai bản ghi."""),
        st(svg(1500, 450,
               box(30, 170, 300, 90, ["khoá định tuyến", "payment.vn.napas"], C_BLUE, size=22),
               arrow(330, 215, 470, 215),
               box(480, 160, 260, 110, ["sàn chủ đề", "payments"], C_PURPLE, size=24, bold=True),
               arrow(740, 190, 960, 70, "#16a34a"), arrow(740, 215, 960, 215, "#16a34a"), arrow(740, 240, 960, 360, "#dc2626", dash=True),
               box(970, 25, 500, 90, ["hàng đợi napas", "payment.*.napas  → khớp"], C_GREEN, size=22),
               box(970, 170, 500, 90, ["hàng đợi audit", "payment.#  → khớp"], C_GREEN, size=22),
               box(970, 315, 500, 90, ["hàng đợi cu", "payment.*  → không khớp"], C_RED, size=22),
               txt(530, 420, "* = đúng một từ;  # = không hoặc nhiều từ", 26, "middle", "#1f2937", True)),
           """Hình thứ ba là sàn chủ đề. Thông điệp mang khoá định tuyến gồm ba từ, thanh toán, chấm v n, chấm NAPAS.
           Mẫu thứ nhất có dấu sao ở giữa thay đúng một từ, nên khớp. Mẫu thứ hai có dấu thăng thay hai từ còn lại, cũng khớp.
           Mẫu thứ ba chỉ có hai từ, dấu sao chỉ thay một từ, nên không khớp. Sàn chép thông điệp tới hai hàng đợi."""),
    ], checks=[f"alg.bnx_compact({LOG}) == [(5, 'A', 120), (6, 'C', 75), (7, 'B', 260)]",
               f"alg.bnx_compact({TOMB}, drop_tombstones=False) == [(5, 'A', 120), (7, 'B', 260), (8, 'C', None)]",
               f"len(alg.bnx_compact({TOMB})) == 2",
               f"alg.bnx_route({BIND}, 'payment.vn.napas') == ['napas', 'audit']"])
    form = sc("formula", "formula", "Suy ra từng bước: nén, bia mộ, kiểm lược đồ, định tuyến", [
        stf("""<p><b>Bước 1.</b> Bên đọc chủ đề số dư chỉ cần <b>trạng thái cuối</b> của mỗi khoá, nên nén nhật ký giữ bản cuối mỗi khoá và giữ nguyên offset:</p>
$$\\text{số bản ghi sau nén} = \\text{số khoá khác nhau}$$
<span class='note'>Làm thử: 8 bản ghi, khoá A, B, C, đều đã nằm trong đoạn đã đóng và bộ dọn đã chạy → còn 3.</span>""",
            """[1] Bước một, vì bên đọc chủ đề số dư chỉ cần trạng thái cuối của mỗi khoá, nên nén nhật ký giữ bản cuối mỗi khoá và giữ nguyên vị trí.
            [2] Suy ra số bản ghi sau nén bằng số khoá khác nhau. [3] Làm thử, tám bản ghi của ba khoá A, B, C, khi cả tám đã nằm trong đoạn đã đóng và bộ dọn đã chạy, thì còn ba."""),
        stf(code(COMPACT_PY, "Bước 2. Nén nhật ký bằng Python"),
            """[2.3] Bước hai, ta viết lại phép nén bằng Python. [2.6] Đi qua nhật ký từ đầu, bản sau của một khoá đè lên bản trước, nên cuối cùng mỗi khoá chỉ còn bản mới nhất.
            [2.8] Bản ghi có giá trị rỗng là bia mộ, nên khoá đó bị bỏ hẳn. [2.10] Dòng gần cuối thêm một bia mộ cho tài khoản C rồi nén lại.""",
            clear=True),
        stf(out(COMPACT_OUT, "Bước 2. Kết quả chạy thật"),
            """[2.1] Chạy thật, tám bản ghi còn ba, là A ở vị trí năm, C ở vị trí sáu, B ở vị trí bảy. [2.2] Thêm bia mộ thì chín bản ghi còn hai, vì khoá C biến mất.""",
            clear=True),
        stf("""<p><b>Bước 3.</b> Bia mộ không biến mất ngay: nó được giữ thêm <code>delete.retention.ms</code> (mặc định 1 ngày), vì bên đọc đang chậm phải kịp thấy lệnh xoá.</p>
$$86\\,400\\,000 \\text{ ms} = \\frac{86\\,400\\,000}{3\\,600\\,000} \\text{ giờ} = 24 \\text{ giờ}$$
<span class='note'>Và đoạn nhật ký đang ghi không bao giờ được nén; nén chạy nền theo từng đoạn, nên lúc nào xong không đoán trước.</span>""",
            """[1] Bước ba, bia mộ không biến mất ngay, mà được giữ thêm một thời gian, vì bên đọc đang chậm phải kịp thấy lệnh xoá.
            [2] Mặc định là tám mươi sáu triệu bốn trăm nghìn mili giây, chia ba triệu sáu trăm nghìn mili giây mỗi giờ, được hai mươi bốn giờ.
            [3] Ngoài ra, đoạn nhật ký đang ghi không bao giờ được nén. Nén chạy nền theo từng đoạn, nên không đoán trước lúc nào xong.""",
            clear=True),
        stf("""<p><b>Bước 4.</b> Mức BACKWARD: bên đọc dùng lược đồ <b>mới</b> phải đọc được dữ liệu ghi bằng lược đồ <b>cũ</b>, nên trường mới phải có giá trị mặc định. Lược đồ Avro (định dạng ghi thông điệp theo lược đồ viết bằng JSON), phiên bản 2:</p>"""
            + code(SCHEMA_JSON),
            """[1] Bước bốn, mức tương thích ngược đòi bên đọc dùng lược đồ mới phải đọc được dữ liệu ghi bằng lược đồ cũ. Vì dữ liệu cũ không có trường mới, nên trường mới phải có giá trị mặc định.
            [2.4] Avro là định dạng ghi thông điệp theo một lược đồ viết bằng JSON. Đây là lược đồ phiên bản hai, thêm trường kênh giao dịch với giá trị mặc định là ứng dụng.""",
            clear=True),
        stf(code(SCHEMA_PY, "Bước 4. Kiểm trước khi cho bên gửi dùng") + out(SCHEMA_OUT),
            """[2.2] Ta kiểm hai thay đổi. Phiên bản hai thêm trường có mặc định. [2.3] Phiên bản ba thêm trường phí không có mặc định.
            [4.1] Chạy thật, phiên bản hai được chấp nhận. [4.2] Phiên bản ba bị từ chối, vì bên đọc mới gặp dữ liệu cũ không có trường phí và không biết điền gì.
            [0] Kho lược đồ làm phép kiểm này khi đăng ký phiên bản mới, nên phải đăng ký và nâng cấp bên đọc trước khi bên gửi đổi.""",
            clear=True),
        stf(code(TOPIC_PY, "Bước 5. Sàn chủ đề: khớp mẫu * và #"),
            """[2.6] Bước năm, vì sàn phải biết hàng đợi nào cần thông điệp, nên nó so khoá định tuyến với mẫu của từng hàng đợi, từng từ một.
            [2.7] Gặp dấu thăng thì thử cho nó nuốt không, một, hay nhiều từ. [2.8] Gặp dấu sao thì nó thay đúng một từ.
            [2.12] Dòng cuối thử ba mẫu với khoá thanh toán chấm v n chấm NAPAS.""",
            clear=True),
        stf(out(TOPIC_OUT, "Bước 5. Kết quả chạy thật"),
            """[2.1] Chạy thật, mẫu có dấu sao ở giữa khớp. [2.2] Mẫu có dấu thăng cũng khớp. [2.3] Còn mẫu chỉ có hai từ thì không khớp, vì khoá có ba từ.""",
            clear=True),
    ], checks=[f"len(alg.bnx_compact({LOG})) == len({{k for k, _ in {LOG}}}) == 3",
               f"len(alg.bnx_compact({TOMB})) == 2", "alg.bnx_ms_to_hours(86400000) == 86400000 / 3600000 == 24",
               "alg.bnx_backward_ok({'account': False, 'amount': False, 'channel': True}, {'account': False, 'amount': False}) == (True, [])",
               "alg.bnx_backward_ok({'account': False, 'amount': False, 'fee': False}, {'account': False, 'amount': False}) == (False, ['fee'])",
               "[alg.bnx_topic_match(p, 'payment.vn.napas') for p in ('payment.*.napas', 'payment.#', 'payment.*')] == [True, True, False]"])
    ex = sc("example", "example", "Ví dụ chủ đề số dư và sàn thanh toán, từng phép tính", [
        st("""<p>Chủ đề số dư (số minh hoạ, nghìn đồng): A: 100, 150, 120; B: 200, 180, 260; C: 50, 75.</p>
$$① \\; 8 \\text{ bản ghi}, 3 \\text{ khoá} \\Rightarrow \\hl{3} \\text{ bản ghi sau nén: A = 120, C = 75, B = 260}$$""",
           """Ta tính từng bước với số minh hoạ. Tài khoản A có ba bản ghi, B có ba, C có hai.
           Phép tính thứ nhất, tám bản ghi của ba khoá, nén còn ba, là A bằng một trăm hai mươi, C bằng bảy mươi lăm, B bằng hai trăm sáu mươi.""",
           focus=[1, 1, 2]),
        st("""$$② \\; 8 + 1 \\text{ bia mộ} = 9 \\text{ bản ghi} \\Rightarrow \\hl{3} \\text{ sau nén: A, B, bia mộ C}$$""",
           """Phép tính thứ hai, thêm một bia mộ cho C thành chín bản ghi. Ngay sau lần nén kế tiếp còn ba, là A, B và bia mộ của C."""),
        st("""$$③ \\; \\text{sau } 24 \\text{ giờ (delete.retention.ms)}: 3 - 1 = \\hlg{2} \\text{ bản ghi: A, B}$$""",
           """Phép tính thứ ba, sau hai mươi bốn giờ, bia mộ cũng bị dọn ở lần nén sau đó, nên ba trừ một còn hai bản ghi, là A và B."""),
        st("""<p>Khoá định tuyến <code>payment.vn.napas</code> có 3 từ.</p>
$$④ \\; \\texttt{payment.*.napas}: 3 \\text{ từ}, \\texttt{*} = \\text{vn} \\Rightarrow \\hlg{\\text{khớp}}; \\quad \\texttt{payment.\\#}: \\texttt{\\#} = \\text{vn.napas} \\Rightarrow \\hlg{\\text{khớp}}$$""",
           """Phép tính thứ tư, khoá định tuyến có ba từ. Mẫu có dấu sao ở giữa cũng có ba từ, dấu sao thay chữ v n, nên khớp. Mẫu có dấu thăng thì dấu thăng thay hai từ còn lại, nên cũng khớp.""",
           focus=[1, 2, 2], clear=True),
        st("""$$⑤ \\; \\texttt{payment.*}: 2 \\text{ từ} \\neq 3 \\text{ từ} \\Rightarrow \\hl{\\text{không khớp}}$$
<div class="box key">Sàn chép thông điệp tới <b>2</b> hàng đợi: napas và audit.</div>""",
           """Phép tính thứ năm, mẫu thanh toán chấm sao chỉ có hai từ, khác ba từ, nên không khớp. Vậy sàn chép thông điệp tới hai hàng đợi, là hàng đợi NAPAS và hàng đợi kiểm toán.""",
           focus=[1, 2]),
    ], checks=[f"len({LOG}) == 8 and alg.bnx_compact({LOG}) == [(5, 'A', 120), (6, 'C', 75), (7, 'B', 260)]",
               f"len({TOMB}) == 9 and len(alg.bnx_compact({TOMB}, drop_tombstones=False)) == 3",
               f"len(alg.bnx_compact({TOMB}, drop_tombstones=False)) - 1 == len(alg.bnx_compact({TOMB})) == 2",
               "alg.bnx_topic_match('payment.*.napas', 'payment.vn.napas') and alg.bnx_topic_match('payment.#', 'payment.vn.napas')",
               f"not alg.bnx_topic_match('payment.*', 'payment.vn.napas') and len(alg.bnx_route({BIND}, 'payment.vn.napas')) == 2"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đi ngược nhật ký, và chạy Kafka thật", [
        stf(code(CHECK_PY, "Đường khác 1: đi ngược từ cuối nhật ký"),
            """[2.3] Đường khác thứ nhất. Thay vì để bản sau đè bản trước, ta đi ngược từ cuối nhật ký, gặp khoá lần đầu thì giữ, gặp lại thì bỏ.
            [2.7] Nếu bản gặp đầu tiên là bia mộ, khoá đó bị bỏ hẳn. [2.12] Dòng cuối in số bản ghi còn lại, trước và sau khi thêm bia mộ.""", clear=True),
        stf(out(CHECK_OUT, "Đường khác 1: kết quả chạy thật"),
            """[2] Chạy thật ra ba và hai, khớp với cách đi xuôi ở bước hai, nên hai cách tính độc lập cho cùng một kết quả.""", clear=True),
        stf(out(KAFKA_OUT, "Đường khác 2: Kafka 3.9.0 thật (Docker), chủ đề cleanup.policy=compact")
            + """<p class='note'>Ghi 8 bản ghi + bia mộ C (giá trị rỗng, in ra là TOMBSTONE), thêm Z:1 để đoạn cũ thôi là đoạn đang ghi, chờ bộ dọn chạy (cấu hình thử: đoạn 1 giây).</p>""",
            """[1] Đường khác thứ hai là chạy Kafka thật trong Docker, chủ đề bật nén. Ta ghi tám bản ghi và một bia mộ, rồi thêm một bản ghi Z để đoạn cũ thôi là đoạn đang ghi.
            [2.1] Sau khi bộ dọn chạy, còn A ở vị trí năm. [2.2] Còn B ở vị trí bảy. [2.3] Và bia mộ của C ở vị trí tám, đúng như phép tính thứ hai.
            [2.4] Bản ghi Z ở vị trí chín nằm trong đoạn đang ghi nên còn nguyên. Vị trí của mọi bản ghi giữ nguyên.""",
            clear=True),
    ], checks=[f"[len(alg.bnx_compact({LOG})), len(alg.bnx_compact({TOMB}))] == [3, 2]",
               f"alg.bnx_compact({TOMB} + [('Z', 1)], drop_tombstones=False) == [(5, 'A', 120), (7, 'B', 260), (8, 'C', None), (9, 'Z', 1)]"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng nén nhật ký là <b class="red">xoá theo thời gian</b>. Sai: nén giữ bản cuối của mỗi khoá dù cũ bao lâu; xoá theo thời gian là chính sách <code>delete</code> (mặc định, <code>retention.ms</code> = 7 ngày).
<br><span class="note">Kèm theo: đọc ngay sau khi ghi vẫn thấy đủ bản cũ, vì đoạn đang ghi chưa nén; đừng viết bên đọc giả định mỗi khoá chỉ có một bản.</span></div>""",
           """Lỗi thứ nhất, của người mới, là tưởng nén nhật ký là xoá theo thời gian. Sai, nén giữ bản cuối của mỗi khoá dù cũ bao lâu. Xoá theo thời gian là chính sách xoá mặc định, giữ bảy ngày.
           Kèm theo đó, đọc ngay sau khi ghi vẫn thấy đủ các bản cũ, vì đoạn đang ghi chưa nén. Đừng viết bên đọc giả định mỗi khoá chỉ có một bản."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Coi RabbitMQ như Kafka: định “đọc lại hôm qua” từ hàng đợi. Hàng đợi thường (không phải loại stream) xoá thông điệp <b class="red">khi đã xác nhận</b>; Kafka giữ theo thời hạn hoặc theo khoá, đọc lại được bằng offset.
<br><span class="note">Ngược lại, dùng Kafka cho việc cần định tuyến linh hoạt theo mẫu là tự viết lại thứ sàn đã có.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là coi hàng đợi có sàn như Kafka, định đọc lại thông điệp hôm qua từ hàng đợi. Hàng đợi thường, không phải loại luồng, xoá thông điệp khi đã xác nhận, còn Kafka giữ theo thời hạn hoặc theo khoá, đọc lại được bằng vị trí.
           Ngược lại, dùng Kafka cho việc cần định tuyến linh hoạt theo mẫu là tự viết lại thứ mà sàn đã có sẵn.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đổi lược đồ <b class="red">trước</b>, kiểm sau: bên nhận lên lược đồ có trường <code>fee</code> không mặc định, đọc lại bản ghi cũ (ví dụ chủ đề nén đọc từ đầu) thiếu <code>fee</code> → vỡ lúc nửa đêm.
<br><span class="note">Cách chữa: đưa phép kiểm tương thích vào quy trình dựng, chạy trước khi phát hành; với BACKWARD, trường mới phải có mặc định, nâng cấp bên đọc trước rồi mới cho bên gửi ghi dữ liệu mới.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là đổi lược đồ trước rồi mới kiểm. Bên nhận lên lược đồ có trường phí không mặc định, rồi đọc lại bản ghi cũ thiếu trường phí, ví dụ khi đọc chủ đề nén từ đầu, và vỡ lúc nửa đêm.
           Cách chữa là đưa phép kiểm tương thích vào quy trình dựng, chạy trước khi phát hành. Với tương thích ngược, trường mới phải có mặc định, và nâng cấp bên đọc trước rồi mới cho bên gửi ghi dữ liệu mới.""",
           clear=True),
    ], checks=["alg.bnx_ms_to_hours(604800000) == 7 * 24"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "Nhật ký: X:1, Y:5, X:2, Z:7, Y:6, X:3, rồi bia mộ Y. Sau nén (chưa hết hạn bia mộ) còn mấy bản ghi? Sau 1 ngày?"],
                   ["2", "Khoá <code>payment.intl.swift.usd</code>. Khớp mẫu nào: <code>payment.*.swift</code>, <code>payment.#.usd</code>, <code>*.intl.#</code>?"],
                   ["3", "Quyết định: luồng “sự kiện giao dịch để đối soát cuối ngày” và luồng “gửi tin nhắn báo số dư”. Kafka hay RabbitMQ?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.2] Câu một, nhật ký có sáu bản ghi của ba khoá X, Y, Z, rồi một bia mộ cho Y. Sau nén còn mấy bản ghi, và sau một ngày còn mấy?
            [1.3] Câu hai, khoá định tuyến trên màn hình có bốn từ, bắt đầu bằng chữ thanh toán. Nó khớp mẫu nào trong ba mẫu?
            [1.4] Câu ba, luồng sự kiện giao dịch để đối soát cuối ngày, và luồng gửi tin nhắn báo số dư, chọn Kafka hay hàng đợi có sàn? [0] Hãy dừng video và làm ra giấy.""",
            pause=25),
        stf("""<p>Câu 1: bản cuối mỗi khoá: X:3 (offset 5), Z:7 (offset 3), bia mộ Y (offset 6).</p>
$$\\text{ngay sau nén: } \\hlg{3}, \\qquad \\text{sau ít nhất 1 ngày, ở lần nén kế tiếp: } 3 - 1 = \\hlg{2}$$""",
            """[1] Đáp án câu một. Bản cuối của mỗi khoá là X bằng ba, Z bằng bảy, và bia mộ của Y.
            [2] Ngay sau nén còn ba bản ghi. Sau ít nhất một ngày, ở lần nén kế tiếp, bia mộ bị dọn, còn hai."""),
        stf(table(["mẫu", "khớp?", "vì sao"],
                  [["<code>payment.*.swift</code>", "không", "mẫu 3 từ, khoá 4 từ: * chỉ thay một từ"],
                   ["<code>payment.#.usd</code>", "có", "# thay hai từ intl.swift"],
                   ["<code>*.intl.#</code>", "có", "* = payment, # = swift.usd"]]),
            """[1.2] Đáp án câu hai. Mẫu thứ nhất có ba từ, khoá có bốn từ, dấu sao chỉ thay một từ, nên không khớp.
            [1.3] Mẫu thứ hai khớp, vì dấu thăng thay hai từ ở giữa. [1.4] Mẫu thứ ba cũng khớp, dấu sao thay chữ thanh toán, dấu thăng thay hai từ cuối."""),
        stf(table(["luồng", "chọn", "được", "mất"],
                  [["sự kiện giao dịch để đối soát", "Kafka", "giữ lại, đọc lại từ offset bất kỳ, nhiều nhóm cùng đọc", "không định tuyến theo mẫu; phải quản lý thời hạn giữ"],
                   ["tin nhắn báo số dư", "RabbitMQ (hàng đợi thường)", "định tuyến theo mẫu, xoá khi đã xác nhận", "không đọc lại được tin đã xác nhận"]]),
            """[1.2] Đáp án câu ba. Sự kiện giao dịch để đối soát nên đi Kafka, vì được giữ lại và đọc lại từ vị trí bất kỳ, nhiều nhóm cùng đọc. Cái giá là không định tuyến theo mẫu.
            [1.3] Tin nhắn báo số dư hợp với hàng đợi thường có sàn, vì định tuyến theo mẫu và xoá khi đã xác nhận. Cái giá là không đọc lại được tin đã xác nhận."""),
    ], checks=["alg.bnx_compact([('X', 1), ('Y', 5), ('X', 2), ('Z', 7), ('Y', 6), ('X', 3), ('Y', None)], drop_tombstones=False) == [(3, 'Z', 7), (5, 'X', 3), (6, 'Y', None)]",
               "len(alg.bnx_compact([('X', 1), ('Y', 5), ('X', 2), ('Z', 7), ('Y', 6), ('X', 3), ('Y', None)])) == 2",
               "[alg.bnx_topic_match(p, 'payment.intl.swift.usd') for p in ('payment.*.swift', 'payment.#.usd', '*.intl.#')] == [False, True, True]"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("8 bản ghi, 3 khoá", "nén: còn 3", "bia mộ C: còn 2", "kiểm lược đồ trước khi gửi", "sàn: * một từ, # nhiều từ"),
           """Tổng kết chuỗi logic. Tám bản ghi của ba khoá nén còn ba. Thêm bia mộ cho C, sau thời gian giữ bia mộ còn hai.
           Lược đồ được kiểm trước khi bên gửi đổi. Và sàn chủ đề định tuyến bằng dấu sao cho một từ, dấu thăng cho nhiều từ."""),
        st("""<div class='box key'><b>Tư duy:</b> hỏi “có cần <b>đọc lại</b> không?”. Cần lịch sử hoặc trạng thái cuối theo khoá: Kafka (nén nhật ký). Cần chia việc theo mẫu rồi xoá: RabbitMQ. Và mọi thay đổi lược đồ đi qua phép kiểm <b>trước</b>.</div>""",
           """Điều cần mang theo là câu hỏi, có cần đọc lại không. Cần lịch sử hay trạng thái cuối theo khoá thì dùng Kafka với nén nhật ký. Cần chia việc theo mẫu rồi xoá thì dùng hàng đợi có sàn. Và mọi thay đổi lược đồ phải qua phép kiểm trước."""),
        st("""<p>Bài sau: chuyển tiền ra nước ngoài, mã ngân hàng quốc tế, kiểm số tài khoản quốc tế và phí khi đổi ngoại tệ.</p>""",
           """Ở bài sau, ta học thanh toán quốc tế và ngoại tệ, gồm mã ngân hàng quốc tế, cách kiểm số tài khoản quốc tế, và phí khi chuyển tiền qua ngân hàng trung gian.""",
           forward_ref=True),
    ])
    return lesson("L10", "kafka_nang_cao_rabbitmq", "Bài 10 — Kafka nâng cao và RabbitMQ: nén nhật ký theo khoá, kiểm lược đồ, định tuyến theo sàn",
                  "curriculum/bnx.yaml L10; audit/bnx/verify_bnx.py L10; Apache Kafka 4.4 docs (đọc 2026-11-11): Design — Log Compaction, "
                  "Topic configs (cleanup.policy, retention.ms, delete.retention.ms); chạy thật apache/kafka:3.9.0 (Docker); Confluent Platform 8.4 "
                  "Schema Evolution and Compatibility; RabbitMQ tutorial 5 (Topics), RabbitMQ 4.4 Consumer Acknowledgements",
                  ["Tính kết quả nén nhật ký theo khoá, kể cả bản ghi bia mộ", "Kiểm một thay đổi lược đồ trước khi cho người gửi dùng",
                   "Định tuyến thông điệp qua sàn chủ đề của RabbitMQ", "Chọn Kafka hay RabbitMQ cho một luồng ngân hàng"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
