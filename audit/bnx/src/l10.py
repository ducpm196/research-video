import re

import lib2
from lib2 import *

lib2.begin("L10")

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

# Đầu ra THẬT: prog() chạy nguyên văn lúc import (Python 3.13); sổ mã sinh bằng lib2.py gen-screen L10.
P_COMPACT = prog("Compact", COMPACT_PY, lang="python",
                 unverified_claims=["Mô hình bỏ hẳn khoá có bia mộ = trạng thái SAU delete.retention.ms; ngay sau lần nén, Kafka thật còn giữ bia mộ (đã thấy thật ở khối BNX L10 check 2 0). Thời điểm Kafka thật dọn bia mộ KHÔNG kiểm (phụ thuộc lần nén sau, không tất định)."])
P_SCHEMA = prog("Schema", SCHEMA_PY, lang="python",
                unverified_claims=["Phép kiểm là GIẢN LƯỢC quy tắc BACKWARD của Confluent Schema Registry (Platform 8.4 'Schema Evolution and Compatibility': bên đọc mới đọc được dữ liệu cũ; thêm trường phải có mặc định, bỏ trường được). Không chạy Schema Registry thật."])
P_TOPIC = prog("Topic", TOPIC_PY, lang="python",
               unverified_claims=["Hàm match tái hiện luật sàn topic; audit/bnx/ver/l10.py đối chiếu đủ 9 ví dụ của RabbitMQ tutorial 5 bằng chính hàm này. Không chạy RabbitMQ thật (máy không có ảnh RabbitMQ)."])
P_CHECK = prog("Check", CHECK_PY, lang="python")
COMPACT_OUT, SCHEMA_OUT, TOPIC_OUT, CHECK_OUT = P_COMPACT.out, P_SCHEMA.out, P_TOPIC.out, P_CHECK.out
# Đầu ra THẬT của Kafka 3.9.0 (ảnh apache/kafka:3.9.0, Docker, 2026-11-11): chủ đề cleanup.policy=compact, segment.ms=1000,
# min.cleanable.dirty.ratio=0.01; ghi 9 bản ghi (8 + bia mộ C), thêm Z:1 để đẩy đoạn cũ ra khỏi đoạn đang ghi, chờ bộ dọn chạy,
# đọc bằng kafka-console-consumer --property print.offset=true --property null.literal=TOMBSTONE. Tái hiện ở audit/bnx/ver/l10.py.
KAFKA_OUT = """
Offset:5	A	120
Offset:7	B	260
Offset:8	C	TOMBSTONE
Offset:9	Z	1
"""

# Lệnh HIỆN TRÊN MÀN HÌNH để người học lặp lại đường Kafka thật (cùng cờ với audit/bnx/ver/l10.py, nơi kiểm từng cờ khớp với lệnh đã chạy).
KAFKA_TOPIC_CMD = r"""docker run -d --name bnx-kafka apache/kafka:3.9.0
docker exec bnx-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --create --topic nen \
  --config cleanup.policy=compact --config segment.ms=1000 \
  --config min.cleanable.dirty.ratio=0.01 \
  --config delete.retention.ms=60000"""
KAFKA_PRODUCE_CMD = r"""printf '%s\n' A:100 B:200 A:150 C:50 B:180 A:120 C:75 \
  B:260 C:NULL | docker exec -i bnx-kafka \
  /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 --topic nen \
  --property parse.key=true --property key.separator=: \
  --property null.marker=NULL
sleep 2   # lâu hơn segment.ms; rồi gửi thêm Z:1 bằng lệnh trên"""
KAFKA_CONSUME_CMD = r"""docker exec bnx-kafka \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic nen \
  --partition 0 --offset earliest --timeout-ms 8000 \
  --property print.key=true --property print.offset=true \
  --property null.literal=TOMBSTONE"""
lib2.other("kafka-topics.sh", kind="other", lang="bash",
           reason="Lệnh dựng Kafka 3.9.0 (ảnh apache/kafka:3.9.0) và tạo chủ đề nén; chạy cần Docker và máy chủ Kafka, không chạy trong cổng screen_code.",
           read_check="audit/bnx/ver/l10.py (kafka_real) lấy các cờ --config và tên ảnh/container TỪ CHÍNH hằng KAFKA_TOPIC_CMD này (bỏ dấu gạch ngược, tách bằng shlex) để dựng container và chủ đề, "
                      "rồi chạy thật và so từng dòng đầu ra với KAFKA_OUT.",
           unverified_claims=["Cổng screen_code không chạy Docker/Kafka; kiểm thật nằm ở audit/bnx/verify_bnx.py L10 (cần Docker)."])
lib2.other("kafka-console-producer.sh", kind="other", lang="bash",
           reason="Lệnh ghi 8 bản ghi và bia mộ vào chủ đề Kafka; chạy cần Kafka.",
           read_check="audit/bnx/ver/l10.py lấy các cờ --property (parse.key, key.separator, null.marker) và dãy bản ghi TỪ hằng KAFKA_PRODUCE_CMD này (shlex) để ghi vào chủ đề thật.",
           unverified_claims=["Cổng screen_code không chạy Docker/Kafka; kiểm thật nằm ở audit/bnx/verify_bnx.py L10."])
lib2.other("kafka-console-consumer.sh", kind="other", lang="bash",
           reason="Lệnh đọc lại chủ đề Kafka từ đầu, in khoá và offset; chạy cần Kafka.",
           read_check="audit/bnx/ver/l10.py lấy các cờ (--partition, --offset, --timeout-ms, --property) TỪ hằng KAFKA_CONSUME_CMD này (shlex) để đọc chủ đề thật; đầu ra đối chiếu với KAFKA_OUT.",
           unverified_claims=["Cổng screen_code không chạy Docker/Kafka; kiểm thật nằm ở audit/bnx/verify_bnx.py L10."])

# Cảnh quy mô: đo thật (đếm) bằng chính hàm compact của bài, ở ba cỡ nhật ký; mô phỏng cùng quy tắc nén, KHÔNG phải Kafka thật.
SCALE_PY = """
for n in (1000, 100000, 1000000):
    log = [(f"TK{i % 100}", i) for i in range(n)]
    con = compact(log)
    print(n, "ban ghi, 100 tai khoan: doc lai", n,
          "| sau nen", len(con))
"""
P_SCALE = prog("Scale", COMPACT_PY.strip() + chr(10) + SCALE_PY.strip(), lang="python", timeout=300)
LAB_PY = """
log = [("M", 10), ("N", 20), ("M", 15), ("P", 5),
       ("N", None), ("M", 12), ("Q", 7), ("P", 9)]
def nen(log, giu_bia_mo):
    cuoi = {}
    for off, (k, v) in enumerate(log):
        cuoi[k] = (off, v)
    return sorted((off, k, v) for k, (off, v) in cuoi.items()
                  if giu_bia_mo or v is not None)
def hien(ds):
    return " ".join(f"{o}:{k}:{'-' if v is None else v}" for o, k, v in ds)
print("con bia mo:", hien(nen(log, True)))
print("het han bia mo:", hien(nen(log, False)))
def khop(mau, khoa):
    p, k = mau.split("."), khoa.split(".")
    def m(i, j):
        if i == len(p):
            return j == len(k)
        if p[i] == "#":
            return any(m(i + 1, t) for t in range(j, len(k) + 1))
        return j < len(k) and p[i] in ("*", k[j]) and m(i + 1, j + 1)
    return m(0, 0)
for mau in ["payment.*.sepa", "payment.#.eur", "*.eu.#"]:
    ket_qua = "co" if khop(mau, "payment.eu.sepa.eur") else "khong"
    print("payment.eu.sepa.eur voi " + mau + ":", ket_qua)
"""
P_LAB = prog("Lab", LAB_PY, lang="python")
LAB_OUT = P_LAB.out
lib2.other('"type": "record"', kind="other", lang="json",
           reason="Lược đồ Avro phiên bản 2 (dữ liệu JSON, không phải chương trình).",
           read_check="Cổng phân tích thật bằng json.loads. audit/bnx/ver/l10.py kiểm: type = record, 3 trường account (string), amount (long), channel (string, default APP); "
                      "bảng {trường: có mặc định?} suy từ JSON này đúng bằng v2 trong khối kiểm lược đồ. KHÔNG chạy Schema Registry hay thư viện Avro (máy không có) — NOT_VERIFIED phần phân giải lược đồ của Avro thật.")
lib2.other("Offset:5", kind="output",
           reason="Đầu ra THẬT của kafka-console-consumer.sh (Kafka 3.9.0, ảnh apache/kafka:3.9.0, Docker, 2026-11-11) trên chủ đề cleanup.policy=compact, segment.ms=1000, min.cleanable.dirty.ratio=0.01, delete.retention.ms=60000: "
                  "ghi A:100 B:200 A:150 C:50 B:180 A:120 C:75 B:260 rồi bia mộ C (null.marker), thêm Z:1 để cuộn đoạn, chờ bộ dọn; đọc với print.offset=true, null.literal=TOMBSTONE (tách bằng dấu tab). "
                  "audit/bnx/ver/l10.py chạy lại toàn bộ trong container bnx-kafka và so từng dòng.",
           claims=["còn A ở vị trí năm", "B ở vị trí bảy", "bia mộ của C ở vị trí tám", "Bản ghi Z ở vị trí chín ... còn nguyên"])


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
        stf("""<p>Dịch vụ tra số dư nhanh khởi động lại, phải đọc lại chủ đề Kafka <code>balances</code> (<b>chủ đề</b>: một nhật ký có tên, nơi các bản ghi cùng loại được ghi nối vào) từ đầu để biết số dư mới nhất.</p>
<p>Trong ví dụ: <b>8</b> bản ghi cho <b>3</b> tài khoản. Ngoài đời là hàng triệu bản ghi, mà chỉ cần <b>bản cuối</b> của mỗi tài khoản.</p>
<div class="box key">Cùng lúc: bên nhận lên <b>lược đồ</b> mới (bản mô tả thông điệp có những trường nào, kiểu gì) có thêm một trường bắt buộc, đọc lại thông điệp cũ thiếu trường đó thì vỡ; và thông báo NAPAS (hệ thống chuyển mạch thanh toán liên ngân hàng) phải tới đúng hàng đợi.</div>""",
            """[1] Chào bạn, dịch vụ tra số dư nhanh vừa khởi động lại, và phải đọc lại chủ đề số dư trong Kafka từ đầu.
            [2] Ví dụ có tám bản ghi cho ba tài khoản, ngoài đời là hàng triệu, mà chỉ cần bản cuối của mỗi tài khoản.
            [3] Cùng lúc đó, bên nhận lên lược đồ mới có thêm một trường bắt buộc, nên đọc lại thông điệp cũ thì vỡ."""),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["giữ nhật ký gọn mà không mất số dư mới nhất", "nén nhật ký theo khoá; <b>bia mộ</b> (bản ghi rỗng đánh dấu khoá đã xoá) để xoá khoá"],
                   ["đổi lược đồ thông điệp mà không làm vỡ bên nhận", "kho lược đồ kiểm tương thích ngược trước khi cho dùng"],
                   ["một thông điệp tới đúng các hàng đợi cần nó", "<b>sàn chủ đề</b> của RabbitMQ (nơi nhận thông điệp rồi chia cho các hàng đợi theo mẫu), mẫu * và #"],
                   ["luồng nào dùng Kafka, luồng nào dùng RabbitMQ", "giữ để đọc lại hay xoá khi đã xác nhận"]]),
            """[1.2] Giữ nhật ký gọn thì nén theo khoá. [1.3] Đổi lược đồ mà không làm vỡ bên nhận thì kiểm tương thích trước.
            [1.4] Đưa thông điệp tới đúng hàng đợi thì dùng sàn chủ đề. [1.5] Chọn Kafka hay hàng đợi có sàn thì tuỳ có cần đọc lại không.""", clear=True,
            introduces=["bnx_bia_mo", "bnx_san_chu_de"]),
    ], checks=[f"len({LOG}) == 8 and len({{k for k, _ in {LOG}}}) == 3"])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Nhật ký chỉ thêm và offset", "Kafka ghi nối vào cuối, mỗi bản ghi có số thứ tự (offset) không đổi", "offset 0, 1, …, 7"],
                   ["② Khoá thông điệp", "nhãn đi kèm, ví dụ số tài khoản; khi số phân vùng không đổi, cùng khoá luôn vào cùng một <b>phân vùng</b> (một phần song song của chủ đề) nên giữ thứ tự", "khoá A, B, C"],
                   ["③ Tương thích ngược / xuôi", "ngược: bên đọc dùng lược đồ mới đọc được dữ liệu cũ; xuôi: bên đọc cũ đọc được dữ liệu mới", "thêm trường có mặc định"],
                   ["④ Hàng đợi và xác nhận", "bên nhận lấy thông điệp, xử lý xong thì báo đã xong (ack)", "xác nhận rồi mới lấy tiếp"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Kafka là nhật ký chỉ thêm, ghi nối vào cuối, mỗi bản ghi có một số thứ tự không đổi.
            [1.3] Khoá thông điệp là nhãn đi kèm, ví dụ số tài khoản. Khi số phân vùng không đổi, cùng khoá luôn vào cùng một phân vùng, tức một phần song song của chủ đề.
            [1.4] Tương thích ngược là bên đọc dùng lược đồ mới vẫn đọc được dữ liệu cũ, xuôi là bên đọc cũ đọc được dữ liệu mới. [1.5] Hàng đợi là nơi bên nhận lấy thông điệp, xử lý xong thì báo xác nhận."""),
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
            """Bảng này giải mã bảy từ. [1.2] Nén nhật ký là giữ ít nhất bản cuối của mỗi khoá. [1.3] Bia mộ là bản ghi có khoá nhưng giá trị rỗng, nghĩa là lệnh xoá khoá đó.
            [1.5] Kho lược đồ lưu các phiên bản lược đồ và kiểm tương thích trước khi nhận phiên bản mới.
            [1.6] Sàn loại chủ đề chép thông điệp tới mọi hàng đợi có mẫu khớp với khoá định tuyến. [1.8] Dấu sao thay đúng một từ, còn dấu thăng thay không hoặc nhiều từ."""),
    ], checks=["alg.bnx_ms_to_hours(86400000) == 24"])
    intu = sc("intuition", "intuition", "Hình dung: nén nhật ký, bia mộ và sàn chủ đề", [
        st(svg(1500, 475,
               txt(40, 30, "trước khi nén: 8 bản ghi", 24, "start", "#1f2937", True),
               log_row(50, full, x0=30, w=180),
               arrow(750, 150, 750, 230, "#475569", None),
               txt(780, 200, "giữ bản cuối của mỗi khoá, offset không đổi", 24, "start", "#475569"),
               txt(40, 265, "sau khi nén: 3 bản ghi", 24, "start", "#16a34a", True),
               log_row(285, [(5, "A", 120), (6, "C", 75), (7, "B", 260)], x0=930, w=180),
               txt(750, 420, "Nhật ký cắt thành nhiều tệp nối tiếp gọi là đoạn; đoạn cuối, nơi đang ghi thêm, không bao giờ bị nén", 24, "middle", "#1f2937", True),
               txt(750, 458, "Bộ dọn: tiến trình nền của Kafka làm việc nén, chạy theo từng đoạn đã đóng", 22, "middle", "#475569")),
           """Hàng trên là tám bản ghi của ba tài khoản theo thứ tự ghi. Bộ dọn, tiến trình nền của Kafka, chỉ giữ bản cuối của mỗi khoá, là A ở vị trí năm, C ở vị trí sáu, và B ở vị trí bảy, vị trí không đổi.
           Nhật ký cắt thành các tệp gọi là đoạn, và đoạn cuối đang ghi không bao giờ bị nén."""),
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
           """Thêm một bia mộ cho tài khoản C ở vị trí tám. Lần nén kế tiếp bỏ bản cũ của C, chỉ còn A, B và bia mộ của C. Sau thời gian giữ, bia mộ bị dọn, nhật ký còn hai bản ghi."""),
        st(svg(1500, 450,
               box(30, 170, 300, 90, ["khoá định tuyến", "payment.vn.napas"], C_BLUE, size=22),
               arrow(330, 215, 470, 215),
               box(480, 160, 260, 110, ["sàn chủ đề", "payments"], C_PURPLE, size=24, bold=True),
               arrow(740, 190, 960, 70, "#16a34a"), arrow(740, 215, 960, 215, "#16a34a"), arrow(740, 240, 960, 360, "#dc2626", dash=True),
               box(970, 25, 500, 90, ["hàng đợi napas", "payment.*.napas  → khớp"], C_GREEN, size=22),
               box(970, 170, 500, 90, ["hàng đợi audit", "payment.#  → khớp"], C_GREEN, size=22),
               box(970, 315, 500, 90, ["hàng đợi cu", "payment.*  → không khớp"], C_RED, size=22),
               txt(530, 420, "* = đúng một từ;  # = không hoặc nhiều từ", 26, "middle", "#1f2937", True)),
           """Thông điệp mang khoá định tuyến gồm ba từ, thanh toán, chấm v n, chấm NAPAS. Mẫu thứ nhất có dấu sao thay đúng một từ, nên khớp. Mẫu thứ hai có dấu thăng thay hai từ còn lại, cũng khớp.
           Mẫu thứ ba chỉ có hai từ nên không khớp, và sàn chép thông điệp tới hai hàng đợi."""),
    ], checks=[f"alg.bnx_compact({LOG}) == [(5, 'A', 120), (6, 'C', 75), (7, 'B', 260)]",
               f"alg.bnx_compact({TOMB}, drop_tombstones=False) == [(5, 'A', 120), (7, 'B', 260), (8, 'C', None)]",
               f"len(alg.bnx_compact({TOMB})) == 2",
               f"alg.bnx_route({BIND}, 'payment.vn.napas') == ['napas', 'audit']"])
    form = sc("formula", "formula", "Suy ra từng bước: nén, bia mộ, kiểm lược đồ, định tuyến", [
        stf("""<p><b>Bước 1.</b> Bên đọc chủ đề số dư chỉ cần <b>trạng thái cuối</b> của mỗi khoá, nên nén nhật ký giữ bản cuối mỗi khoá và giữ nguyên offset:</p>
$$\\text{số bản ghi sau nén} = \\text{số khoá khác nhau}$$
<span class='note'>Làm thử: 8 bản ghi, khoá A, B, C, đều đã nằm trong đoạn đã đóng và bộ dọn đã chạy → còn 3.</span>""",
            """[1] Bước một, vì bên đọc chủ đề số dư chỉ cần trạng thái cuối của mỗi khoá, nên nén nhật ký giữ bản cuối mỗi khoá và giữ nguyên vị trí.
            [2] Suy ra số bản ghi sau nén bằng số khoá khác nhau. [3] Làm thử, tám bản ghi của ba khoá, khi bộ dọn đã chạy, thì còn ba."""),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>for off, (key, val) in enumerate(log):</code>", "duyệt kèm số thứ tự <code>off</code>; mỗi phần tử là cặp (khoá, giá trị), tách luôn thành hai biến"],
                  ["<code>last[key] = (off, val)</code>", "từ điển <code>last</code> ghi cặp sau cùng của mỗi khoá; bản sau đè bản trước"],
                  ["<code>sorted((…) for … if v is not None)</code>", "viết gọn: xếp các bộ ba, bỏ bộ có giá trị <code>None</code> (rỗng)"],
                  ["<code>log.append((\"C\", None))</code>", "thêm một phần tử vào cuối danh sách"]]),
           """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Vòng lặp duyệt kèm số thứ tự, từ điển ghi đè bản trước bằng bản sau, và giá trị rỗng bị bỏ.""", clear=True),
        stf(code(COMPACT_PY, "Bước 2. Mô hình nén nhật ký bằng Python (trạng thái sau thời gian giữ bia mộ)"),
            """[2.3] Bước hai, ta viết lại phép nén bằng Python. [2.6] Đi qua nhật ký từ đầu, bản sau của một khoá đè lên bản trước, nên mỗi khoá chỉ còn bản mới nhất.
            [2.8] Giá trị rỗng là bia mộ, mô hình này bỏ hẳn khoá đó, như lúc hết thời gian giữ bia mộ. [2.10] Rồi thêm bia mộ cho C.""",
            clear=True),
        stf(out(COMPACT_OUT, "Bước 2. Kết quả chạy thật của mô hình"),
            """[2.1] Tám bản ghi còn ba, là A, C, B. [2.2] Thêm bia mộ thì chín bản ghi còn hai, vì mô hình bỏ khoá C. Kafka thật còn giữ bia mộ ngay sau lần nén.""",
            clear=True),
        stf("""<p><b>Bước 3.</b> Bia mộ không biến mất ngay: nó được giữ thêm <code>delete.retention.ms</code> (mặc định 1 ngày), vì bên đọc đang chậm phải kịp thấy lệnh xoá.</p>
$$86\\,400\\,000 \\text{ ms} = \\frac{86\\,400\\,000}{3\\,600\\,000} \\text{ giờ} = 24 \\text{ giờ}$$
<span class='note'>Và đoạn nhật ký đang ghi không bao giờ được nén; nén chạy nền theo từng đoạn, nên lúc nào xong không đoán trước.</span>""",
            """[1] Bước ba, bia mộ không biến mất ngay mà được giữ thêm một thời gian, vì bên đọc chậm phải kịp thấy lệnh xoá. [2] Mặc định là hai mươi bốn giờ.
            [3] Nén chạy nền theo từng đoạn, nên không đoán trước lúc nào xong.""",
            clear=True),
        stf("""<p><b>Bước 4.</b> Mức BACKWARD: bên đọc dùng lược đồ <b>mới</b> phải đọc được dữ liệu ghi bằng lược đồ <b>cũ</b>, nên trường mới phải có giá trị mặc định. Lược đồ Avro (định dạng ghi thông điệp theo lược đồ viết bằng JSON), phiên bản 2:</p>"""
            + code(SCHEMA_JSON)
            + """<p class="note"><code>"record"</code>: một thông điệp gồm nhiều trường (<code>fields</code>); <code>"string"</code>: chuỗi chữ; <code>"long"</code>: số nguyên 64 bit; <code>"default"</code>: giá trị dùng khi dữ liệu cũ thiếu trường.</p>""",
            """[1] Bước bốn, mức tương thích ngược đòi bên đọc dùng lược đồ mới phải đọc được dữ liệu cũ. Vì dữ liệu cũ không có trường mới, nên trường mới phải có giá trị mặc định.
            [2.4] Avro là định dạng ghi thông điệp theo một lược đồ viết bằng JSON. [3] Kiểu bản ghi gồm nhiều trường, và kiểu dài là số nguyên sáu mươi bốn bit.""",
            clear=True, introduces=["bnx_avro"]),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>{**v1, &quot;channel&quot;: True}</code>", "sao chép từ điển <code>v1</code> rồi thêm một khoá"],
                  ["<code>[f for f, has_default in new.items() if f not in old and not has_default]</code>", "viết gọn: giữ những trường <code>f</code> có trong lược đồ mới, không có trong lược đồ cũ và không có mặc định"],
                  ["<code>return len(bad) == 0, bad</code>", "trả về hai giá trị cùng lúc: đúng hay sai, và danh sách trường vi phạm"]]),
           """Hàm kiểm sao chép từ điển rồi thêm khoá, gom các trường mới không có mặc định, nên ta giải nghĩa trước.""", clear=True),
        stf(code(SCHEMA_PY, "Bước 4. Hàm đồ chơi kiểm tương thích ngược (không phải Schema Registry)") + out(SCHEMA_OUT, "Kết quả của hàm đồ chơi (kho thật còn kiểm đổi kiểu)"),
            """[2.2] Phiên bản hai thêm trường có mặc định. [2.3] Phiên bản ba thêm trường phí không có mặc định.
            [4.1] Phiên bản hai được chấp nhận. [4.2] Phiên bản ba bị từ chối, vì dữ liệu cũ không có trường phí và bên đọc không biết điền gì.""",
            clear=True),
        st("""<div class="box key"><b>Xoá trường:</b> ở mức tương thích ngược không bị chặn; ở mức tương thích xuôi chỉ bị chặn <b>nếu trường bị xoá không có giá trị mặc định</b>. Đây là hàm đồ chơi, kho lược đồ thật kiểm cả đổi kiểu.</div>""",
           """Đây là hàm đồ chơi. Xoá trường thì ở mức ngược không bị chặn vì bên đọc mới bỏ qua trường thừa, còn ở mức xuôi chỉ bị chặn nếu trường bị xoá không có giá trị mặc định.""", clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>pattern.split(&quot;.&quot;)</code>", "cắt chuỗi ở mỗi dấu chấm thành danh sách các từ"],
                  ["<code>def m(i, j):</code> … <code>m(i + 1, j + 1)</code>", "hàm nằm trong hàm, và tự gọi lại chính nó với vị trí kế tiếp (đệ quy)"],
                  ["<code>any(m(i + 1, t) for t in range(j, len(k) + 1))</code>", "thử từng <code>t</code>; đúng nếu có ít nhất một <code>t</code> cho kết quả đúng"],
                  ["<code>p[i] in (&quot;*&quot;, k[j])</code>", "từ mẫu là <code>*</code> hoặc đúng bằng từ của khoá"]]),
           """Hàm khớp mẫu cắt chuỗi ở dấu chấm, có một hàm con tự gọi lại chính nó, nên ta giải nghĩa trước.""", clear=True),
        stf(code(TOPIC_PY, "Bước 5. Sàn chủ đề: khớp mẫu * và #"),
            """[2.6] Bước năm, vì sàn phải biết hàng đợi nào cần thông điệp, nên nó so khoá định tuyến với từng mẫu, từng từ một.
            [2.7] Gặp dấu thăng thì thử cho nó nuốt không, một, hay nhiều từ. [2.8] Gặp dấu sao thì thay đúng một từ. [2.12] Dòng cuối thử ba mẫu.""",
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
           """Tài khoản A có ba bản ghi, B có ba, C có hai.
           Phép tính thứ nhất, tám bản ghi của ba khoá nén còn ba, là A một trăm hai mươi, C bảy mươi lăm, B hai trăm sáu mươi.""",
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
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>range(len(log) - 1, -1, -1)</code>", "dãy số đi ngược: bắt đầu ở vị trí cuối <code>len(log) - 1</code>, dừng trước <code>-1</code>, mỗi lần giảm 1"],
                  ["<code>seen = set()</code>, <code>seen.add(key)</code>, <code>key not in seen</code>", "<code>seen</code> là tập các khoá đã gặp; thêm khoá vào tập; kiểm khoá chưa gặp"]]),
           """Hàm đi ngược dùng thêm hai cách viết, nên ta giải nghĩa trước. Dãy số đi từ vị trí cuối về đầu, và một tập ghi nhớ những khoá đã gặp.""", clear=True),
        stf(code(CHECK_PY, "Đường khác 1: đi ngược từ cuối nhật ký"),
            """[2.3] Vì bản sau đè bản trước, ta đi ngược từ cuối nhật ký, gặp khoá lần đầu thì giữ, gặp lại thì bỏ.
            [2.7] [2.12] Dòng cuối in số bản ghi còn lại, trước và sau khi thêm bia mộ.""", clear=True),
        stf(out(CHECK_OUT, "Đường khác 1: kết quả chạy thật"),
            """[2] Chạy thật ra ba và hai, khớp với cách đi xuôi, nên hai cách độc lập cho cùng kết quả.""", clear=True),
        st(table(["lệnh", "nghĩa"],
                 [["<code>docker run -d --name bnx-kafka apache/kafka:3.9.0</code>", "chạy một “thùng” Kafka ở nền (<code>-d</code>), đặt tên <code>bnx-kafka</code>"],
                  ["<code>docker exec bnx-kafka /opt/kafka/bin/…</code>", "chạy một lệnh bên trong thùng đó; chương trình nằm ở thư mục <code>/opt/kafka/bin/</code>: <code>kafka-topics.sh</code> quản lý chủ đề, <code>kafka-console-producer.sh</code> gửi bản ghi, <code>kafka-console-consumer.sh</code> đọc bản ghi ra màn hình"],
                  ["<code>--bootstrap-server localhost:9092</code>", "địa chỉ máy Kafka để nối vào (máy này, cổng 9092)"],
                  ["<code>--create --topic nen</code>, <code>--config tên=giá trị</code>", "tạo chủ đề tên <code>nen</code>; đặt từng cấu hình cho nó; dấu <code>\\</code> cuối dòng nối lệnh dài"]]),
           """Các lệnh Kafka sắp tới có nhiều cờ, nên ta giải nghĩa trước. Lệnh đầu chạy một thùng Kafka ở nền, lệnh sau chạy trong thùng đó một chương trình của Kafka: quản lý chủ đề, gửi bản ghi, đọc bản ghi. Mỗi cờ cấu hình đặt một thiết lập cho chủ đề.""", clear=True),
        stf(code(KAFKA_TOPIC_CMD, "Đường khác 2, bước 1: dựng Kafka 3.9.0 bằng Docker, tạo chủ đề nén")
            + """<p class="note"><b>Docker</b>: công cụ chạy phần mềm trong một “thùng” đóng gói sẵn. Sau <code>docker run</code>, chờ vài giây cho máy Kafka khởi động (xem <code>docker logs bnx-kafka</code>) rồi mới tạo chủ đề.</p>""",
            """[2] Đường khác thứ hai là chạy Kafka thật trong Docker, công cụ chạy phần mềm trong một thùng đóng gói sẵn. Ta dựng một máy Kafka, chờ vài giây cho nó khởi động, rồi tạo chủ đề bật nén. Vì muốn thấy kết quả sớm, ta đặt đoạn dài một giây và ngưỡng dọn thấp.""", clear=True),
        st(table(["lệnh", "nghĩa"],
                 [["<code>printf '%s\\n' A:100 B:200 …</code>", "in mỗi đối số một dòng: <code>A:100</code>, <code>B:200</code>…"],
                  ["<code>… | docker exec -i …</code>", "dấu <code>|</code> (ống): đầu ra của lệnh trước thành đầu vào của lệnh sau; <code>-i</code> giữ đầu vào mở"],
                  ["<code>--property parse.key=true --property key.separator=:</code>", "mỗi dòng là <code>khoá:giá trị</code>, tách ở dấu hai chấm"],
                  ["<code>--property null.marker=NULL</code>", "chữ <code>NULL</code> nghĩa là giá trị rỗng (bia mộ)"],
                  ["<code>sleep 2</code>", "chờ 2 giây"]]),
           """Lệnh ghi dùng thêm vài cách viết, nên ta giải nghĩa trước. Lệnh in mỗi đối số một dòng, dấu gạch đứng chuyển đầu ra sang lệnh sau. Hai cờ báo mỗi dòng là khoá và giá trị cách nhau dấu hai chấm, và chữ viết hoa kia là giá trị rỗng.""", clear=True),
        stf(code(KAFKA_PRODUCE_CMD, "Đường khác 2, bước 2: ghi 8 bản ghi và bia mộ của C (NULL)")
            + """<p class="note">Sau <code>sleep 2</code>, gửi thêm bản ghi <code>Z:1</code> bằng đúng lệnh <code>printf … | docker exec -i …</code> ở trên, chỉ đổi dãy bản ghi thành <code>Z:1</code> (bỏ <code>C:NULL</code>).</p>""",
            """[2] Rồi ta ghi tám bản ghi và một bia mộ cho C. Hai giây sau ta ghi thêm bản ghi Z bằng chính lệnh đó, chỉ đổi dãy bản ghi, vì đoạn đang ghi không bao giờ bị nén, nên cần đoạn mới để đoạn cũ được dọn.""", clear=True),
        st(table(["cờ", "nghĩa"],
                 [["<code>--partition 0 --offset earliest --timeout-ms 8000</code>", "đọc phân vùng 0 từ đầu; thôi chờ sau 8 giây không có gì mới"],
                  ["<code>--property print.key=true --property print.offset=true</code>", "in kèm khoá và vị trí (offset) của mỗi bản ghi"],
                  ["<code>--property null.literal=TOMBSTONE</code>", "giá trị rỗng in thành chữ <code>TOMBSTONE</code>"]]),
           """Lệnh đọc có ba nhóm cờ: đọc phân vùng không từ đầu, in kèm khoá và vị trí, và in giá trị rỗng thành chữ bia mộ, vì bia mộ không có giá trị.""", clear=True),
        stf(code(KAFKA_CONSUME_CMD, "Đường khác 2, bước 3: chờ bộ dọn chạy rồi đọc lại từ đầu")
            + out(KAFKA_OUT, "Đường khác 2: kết quả Kafka 3.9.0 thật (Docker)"),
            """[2] Chờ bộ dọn chạy, từ vài chục giây tới vài phút, rồi đọc lại từ đầu. [4.2] Còn A ở vị trí năm, B ở vị trí bảy, và bia mộ của C ở vị trí tám. [4.4] Bản ghi Z ở vị trí chín nằm trong đoạn đang ghi nên còn nguyên.""",
            clear=True),
    ], checks=[f"[len(alg.bnx_compact({LOG})), len(alg.bnx_compact({TOMB}))] == [3, 2]",
               f"alg.bnx_compact({TOMB} + [('Z', 1)], drop_tombstones=False) == [(5, 'A', 120), (7, 'B', 260), (8, 'C', None), (9, 'Z', 1)]"])
    quymo = sc("quymo", "example", "Khi nhật ký lớn dần: khởi động lại phải đọc bao nhiêu bản ghi", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>f\"TK{i % 100}\"</code>", "chuỗi có <code>f</code> đứng đầu: <code>{…}</code> được thay bằng giá trị; <code>i % 100</code> là số dư khi chia <code>i</code> cho 100, nên chỉ có 100 tên TK0 … TK99"],
                  ["<code>[(…) for i in range(n)]</code>", "viết gọn: tạo danh sách <code>n</code> cặp, <code>i</code> chạy từ 0 tới n − 1"]]),
           """Khối đo dùng thêm hai cách viết, nên ta giải nghĩa trước. Chuỗi có chữ f đứng đầu thay phần trong ngoặc nhọn bằng giá trị, và phép lấy dư làm tên tài khoản quay vòng trong một trăm tên.""", clear=True),
        stf(P_SCALE.show_from("for n in", 5, title="Mô phỏng cùng quy tắc nén (không phải Kafka thật): gõ nối tiếp sau hàm compact của bước 2"),
            """[2] Ta đo bằng chính hàm nén của bước hai, nên đây là mô phỏng chứ không phải Kafka thật, ở ba cỡ nhật ký. [2.3] Mỗi cỡ có một trăm tài khoản, ta nén rồi đếm bản ghi còn lại.""",
            clear=True),
        stf(P_SCALE.out_html("\n".join(P_SCALE.out.splitlines()[2:]))
            + """<p class="note">Không nén: khởi động lại phải đọc mọi bản ghi. Có nén: chỉ còn bản cuối của mỗi tài khoản. Con số 100 là cận dưới của mô phỏng nén hoàn toàn: Kafka thật nén theo ngưỡng (<code>min.cleanable.dirty.ratio</code>) và đoạn đang ghi chưa nén, nên số còn lại thật có thể lớn hơn.</p>""",
            """[2.1] Nhật ký một nghìn bản ghi còn một trăm sau nén. [2.2] Một trăm nghìn bản ghi, gấp một trăm lần, cũng chỉ còn một trăm. [2.3] Một triệu bản ghi vẫn còn đúng một trăm, vì chỉ có một trăm tài khoản. [3] Một trăm là cận dưới, vì Kafka thật nén theo ngưỡng và đoạn đang ghi chưa nén.""",
            clear=True),
        stf(table(["số bản ghi trong nhật ký", "không nén: số bản ghi phải đọc lại", "có nén (100 tài khoản, cận dưới)", "đọc lại mất nếu 1 micro giây mỗi bản ghi (số minh hoạ)"],
                  [["1 000", "1 000", "100", "1 ms so với 0,1 ms"],
                   ["100 000 (gấp 100 lần)", "100 000", "100", "100 ms so với 0,1 ms"],
                   ["1 000 000 (gấp 1 000 lần)", "1 000 000", "100", "1 giây so với 0,1 ms"]]),
            """[1.2] Không nén thì thời gian khởi động tăng thẳng theo độ dài nhật ký, từ một mili giây lên một giây, với số minh hoạ một phần triệu giây mỗi bản ghi. [1.3] Có nén thì khối lượng đọc chỉ phụ thuộc số tài khoản, nên gần như không đổi.""",
            clear=True),
        stf(table(["cách", "được", "mất", "khi nào chọn"],
                  [["không nén, giữ theo thời hạn", "đủ lịch sử trong thời hạn; đọc lại sự kiện cũ được", "khởi động lại phải đọc cả nhật ký; dung lượng tăng theo thời gian", "luồng cần lịch sử, như đối soát cuối ngày"],
                   ["nén theo khoá", "chỉ cần bản cuối mỗi khoá; khởi động nhanh, dung lượng theo số khoá", "mất các bản cũ của khoá; nén chạy nền nên không đoán được lúc nào xong; đoạn đang ghi chưa nén", "chủ đề trạng thái như số dư, hồ sơ"],
                   ["nén và dựng bộ nhớ đệm ở bên đọc", "bên đọc dựng lại trạng thái nhanh rồi phục vụ tra cứu", "bên đọc phải xử lý bia mộ và các bản trùng", "dịch vụ tra số dư cần khởi động lại nhanh"]]),
            """[1.2] Không nén thì giữ đủ lịch sử, đổi lại khởi động lại phải đọc cả nhật ký. [1.3] Nén theo khoá thì khởi động nhanh, đổi lại mất các bản cũ. [1.4]""",
            clear=True),
    ], checks=["[alg.bnx_l10_compacted(n, 100) for n in (1000, 100000, 1000000)] == [100, 100, 100]",
               "[alg.bnx_l10_read_ms(n, 0.001) for n in (1000, 100000, 1000000)] == [1.0, 100.0, 1000.0]",
               "100000 // 1000 == 100 and 1000000 // 1000 == 1000",
               "alg.bnx_l10_read_ms(100, 0.001) == 0.1"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng nén nhật ký là <b class="red">xoá theo thời gian</b>. Sai: nén giữ bản cuối của mỗi khoá dù cũ bao lâu; xoá theo thời gian là chính sách <code>delete</code> (mặc định, <code>retention.ms</code> = 7 ngày).
<br><span class="note">Kèm theo: đọc ngay sau khi ghi vẫn thấy đủ bản cũ, vì đoạn đang ghi chưa nén; đừng viết bên đọc giả định mỗi khoá chỉ có một bản.</span></div>""",
           """Lỗi thứ nhất, của người mới, là tưởng nén nhật ký là xoá theo thời gian. Sai, nén giữ bản cuối của mỗi khoá dù cũ bao lâu.
"""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Coi RabbitMQ như Kafka: định “đọc lại hôm qua” từ hàng đợi. Hàng đợi thường (không phải loại stream) xoá thông điệp <b class="red">khi đã xác nhận</b>; Kafka giữ theo thời hạn hoặc theo khoá, đọc lại được bằng offset.
<br><span class="note">Ngược lại, dùng Kafka cho việc cần định tuyến linh hoạt theo mẫu là tự viết lại thứ sàn đã có.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là coi hàng đợi có sàn như Kafka, định đọc lại thông điệp hôm qua. Hàng đợi thường xoá thông điệp khi đã xác nhận, còn Kafka giữ lại.
""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đổi lược đồ <b class="red">trước</b>, kiểm sau: bên nhận lên lược đồ có trường <code>fee</code> không mặc định, đọc lại bản ghi cũ (ví dụ chủ đề nén đọc từ đầu) thiếu <code>fee</code> → vỡ lúc nửa đêm.
<br><span class="note">Cách chữa: đưa phép kiểm tương thích vào quy trình dựng, chạy trước khi phát hành; với BACKWARD, trường mới phải có mặc định, nâng cấp bên đọc trước rồi mới cho bên gửi ghi dữ liệu mới.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, là đổi lược đồ trước rồi mới kiểm. Bên nhận lên lược đồ có trường phí không mặc định thì đọc bản ghi cũ bị vỡ lúc nửa đêm.
           Cách chữa là đưa phép kiểm tương thích vào quy trình dựng, và nâng cấp bên đọc trước rồi mới cho bên gửi ghi dữ liệu mới.""",
           clear=True),
    ], checks=["alg.bnx_ms_to_hours(604800000) == 7 * 24"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "Nhật ký: X:1, Y:5, X:2, Z:7, Y:6, X:3, rồi bia mộ Y. Sau nén (chưa hết hạn bia mộ) còn mấy bản ghi? Sau 1 ngày?"],
                   ["2", "Khoá <code>payment.intl.swift.usd</code>. Khớp mẫu nào: <code>payment.*.swift</code>, <code>payment.#.usd</code>, <code>*.intl.#</code>?"],
                   ["3", "Quyết định: luồng “sự kiện giao dịch để đối soát cuối ngày” và luồng “gửi tin nhắn báo số dư”. Kafka hay RabbitMQ?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.4] Câu ba chọn Kafka hay hàng đợi có sàn. [0] Hãy dừng video và làm ra giấy.""",
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
            [1.3] Mẫu thứ hai khớp, vì dấu thăng thay hai từ ở giữa. [1.4] Mẫu thứ ba cũng khớp."""),
        stf(table(["luồng", "chọn", "được", "mất"],
                  [["sự kiện giao dịch để đối soát", "Kafka", "giữ lại, đọc lại từ offset bất kỳ, nhiều nhóm cùng đọc", "không định tuyến theo mẫu; phải quản lý thời hạn giữ"],
                   ["tin nhắn báo số dư", "RabbitMQ (hàng đợi thường)", "định tuyến theo mẫu, xoá khi đã xác nhận", "không đọc lại được tin đã xác nhận"]]),
            """[1.2] Đáp án câu ba. Sự kiện đối soát nên đi Kafka, vì được giữ lại và đọc lại được, cái giá là không định tuyến theo mẫu.
            [1.3] Tin nhắn báo số dư hợp với hàng đợi có sàn, vì định tuyến theo mẫu và xoá khi đã xác nhận."""),
    ], checks=["alg.bnx_compact([('X', 1), ('Y', 5), ('X', 2), ('Z', 7), ('Y', 6), ('X', 3), ('Y', None)], drop_tombstones=False) == [(3, 'Z', 7), (5, 'X', 3), (6, 'Y', None)]",
               "len(alg.bnx_compact([('X', 1), ('Y', 5), ('X', 2), ('Z', 7), ('Y', 6), ('X', 3), ('Y', None)])) == 2",
               "[alg.bnx_topic_match(p, 'payment.intl.swift.usd') for p in ('payment.*.swift', 'payment.#.usd', '*.intl.#')] == [False, True, True]"])
    lab_pr = practice_scene(sc, "Tự làm: nén nhật ký có bia mộ và khớp mẫu sàn chủ đề", practice_steps2(
        st, "BNX", "L10",
        """<p><b>Đề</b>: nhật ký 8 bản ghi (khoá, giá trị): M10, N20, M15, P5, <b>N rỗng</b> (bia mộ), M12, Q7, P9 (offset từ 0). Viết <code>mau.py</code> (Python, viết không dấu):</p>
<ol><li>nén giữ bản cuối của mỗi khoá, <b>còn bia mộ</b>: in <code>con bia mo:</code> rồi các mục <code>offset:khoá:giá trị</code> theo thứ tự offset (bia mộ in <code>-</code>)</li>
<li>sau thời gian giữ bia mộ: in <code>het han bia mo:</code> và danh sách đã bỏ bia mộ</li>
<li>khoá <code>payment.eu.sepa.eur</code> với ba mẫu <code>payment.*.sepa</code>, <code>payment.#.eur</code>, <code>*.eu.#</code>: in <code>co</code> hoặc <code>khong</code></li></ol>
<p class="note">Số liệu khác ví dụ trong bài; chữ in ra phải đúng từng ký tự như kết quả mong đợi.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết chương trình nén nhật ký giữ bản cuối của mỗi khoá, in kết quả còn bia mộ và sau khi bia mộ hết hạn, rồi kiểm khoá bốn từ với ba mẫu. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> duyệt nhật ký, với mỗi khoá chỉ nhớ <code>(offset, giá trị)</code> sau cùng; bia mộ có giá trị <code>None</code>. Khớp mẫu: dấu <code>*</code> thay đúng một từ, dấu <code>#</code> thay không hoặc nhiều từ (thử mọi cách nuốt).
Lời giải đầy đủ ở <code>labs/BNX/L10/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hãy duyệt nhật ký và với mỗi khoá chỉ nhớ vị trí và giá trị sau cùng. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L10")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("8 bản ghi, 3 khoá", "nén: còn 3", "bia mộ C: còn 2", "kiểm lược đồ trước khi gửi", "sàn: * một từ, # nhiều từ"),
           """Tám bản ghi của ba khoá nén còn ba. Thêm bia mộ cho C, sau thời gian giữ bia mộ còn hai. Lược đồ được kiểm trước khi bên gửi đổi."""),
        st("""<div class='box key'><b>Tư duy:</b> hỏi “có cần <b>đọc lại</b> không?”. Cần lịch sử hoặc trạng thái cuối theo khoá: Kafka (nén nhật ký). Cần chia việc theo mẫu rồi xoá: RabbitMQ. Và mọi thay đổi lược đồ đi qua phép kiểm <b>trước</b>.</div>""",
           """Hãy hỏi có cần đọc lại không. Cần lịch sử hay trạng thái cuối theo khoá thì dùng Kafka, cần chia việc theo mẫu rồi xoá thì dùng hàng đợi có sàn."""),
        st("""<p>Bài sau: chuyển tiền ra nước ngoài, mã ngân hàng quốc tế, kiểm số tài khoản quốc tế và phí khi đổi ngoại tệ.</p>""",
           """Bài sau học thanh toán quốc tế và ngoại tệ, gồm mã ngân hàng và phí chuyển tiền.""",
           forward_ref=True),
    ])
    return lesson("L10", "kafka_nang_cao_rabbitmq", "Bài 10 — Kafka nâng cao và RabbitMQ: nén nhật ký theo khoá, kiểm lược đồ, định tuyến theo sàn",
                  "curriculum/bnx.yaml L10; audit/bnx/verify_bnx.py L10; Apache Kafka 4.4 docs (đọc 2026-11-11): Design — Log Compaction, "
                  "Topic configs (cleanup.policy, retention.ms, delete.retention.ms); chạy thật apache/kafka:3.9.0 (Docker); Confluent Platform 8.4 "
                  "Schema Evolution and Compatibility; RabbitMQ tutorial 5 (Topics), RabbitMQ 4.4 Consumer Acknowledgements",
                  ["Tính kết quả nén nhật ký theo khoá, kể cả bản ghi bia mộ", "Kiểm một thay đổi lược đồ trước khi cho người gửi dùng",
                   "Định tuyến thông điệp qua sàn chủ đề của RabbitMQ", "Nêu khi nào chọn Kafka, khi nào chọn RabbitMQ cho một luồng ngân hàng",
                   "So sánh số bản ghi phải đọc lại khi khởi động, có và không nén nhật ký, ở 1 000, 100 000 và 1 000 000 bản ghi"],
                  [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec],
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "quiz"), (5, "quymo")])


LAB_DE = """# Lab BNX L10 — Nén nhật ký có bia mộ và khớp mẫu sàn chủ đề (mô phỏng bằng Python, không cần Kafka hay RabbitMQ)

Nhật ký 8 bản ghi (khoá, giá trị), offset từ 0: `("M", 10), ("N", 20), ("M", 15), ("P", 5), ("N", None), ("M", 12), ("Q", 7), ("P", 9)`.
`None` là bia mộ (xoá khoá N). Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`:

1. Nén giữ bản cuối của mỗi khoá, còn bia mộ. In `con bia mo:` rồi các mục `offset:khoá:giá trị` theo thứ tự offset, cách nhau một dấu cách; bia mộ in `-` thay cho giá trị.
2. Hết thời gian giữ bia mộ: in `het han bia mo:` và danh sách đã bỏ bia mộ, cùng dạng.
3. Với khoá `payment.eu.sepa.eur` và mỗi mẫu `payment.*.sepa`, `payment.#.eur`, `*.eu.#` (`*` thay đúng một từ, `#` thay không hoặc nhiều từ; từ cách nhau dấu chấm), in `payment.eu.sepa.eur voi <mẫu>: co` hoặc `: khong`.

Gợi ý cú pháp Python: `for off, (k, v) in enumerate(log):` duyệt kèm số thứ tự và tách luôn cặp (khoá, giá trị); `d[k] = (off, v)` ghi đè bản trước của khoá `k` trong từ điển `d`; `None` là giá trị rỗng (bia mộ). Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L10 mau.py`.
"""

# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L10", LAB_DE, "py", LAB_PY, LAB_OUT)
