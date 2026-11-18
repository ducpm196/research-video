import lib2
from lib2 import *
from libj import jstep, nowrap

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l19.yaml, audit/bnx/ver/l19.py) ──
# Redis thật: ảnh Docker chính thức redis:8.10.3 (audit/bnx/deps/l19/README.md), container bnx-l19-redis tự dựng tự gỡ.
PY_CRC = r'''
def crc16(b):                 # CRC16 XMODEM, đa thức 0x1021
    c = 0
    for x in b:
        c ^= x << 8
        for _ in range(8):
            c = (c << 1) ^ 0x1021 if c & 0x8000 else c << 1
            c &= 0xFFFF
    return c
c = crc16(b"foo")
print(hex(crc16(b"123456789")), c, c % 16384)
print([(a, a + n - 1) for a, n in
       ((0, 5461), (5461, 5462), (10923, 5461))])
'''

SH_START = r'''
docker rm -f bnx-l19-redis > /dev/null 2>&1
docker run -d --name bnx-l19-redis redis:8.10.3 \
  redis-server --port 7000 --cluster-enabled yes > /dev/null
D="docker exec -i bnx-l19-redis"
for p in 7001 7002; do $D redis-server --port $p \
  --cluster-enabled yes --cluster-config-file n$p.conf \
  --daemonize yes > /dev/null; done
$D redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 \
  127.0.0.1:7002 --cluster-yes | grep -E "Slots|covered"
r() { $D redis-cli --no-raw -p 7000 "$@"; }
until r CLUSTER INFO | grep -q state:ok; do sleep 1; done
'''

SH_SLOT = r'''
r CLUSTER KEYSLOT foo
r SET foo bar
r -c SET foo bar
r -c GET foo
'''

SH_LOCK = r'''
r -c <<'EOF'
SET loan:disb:A1001 may-a NX EX 300
SET loan:disb:A1001 may-b NX EX 300
TTL loan:disb:A1001
DELEX loan:disb:A1001 IFEQ may-b
DELEX loan:disb:A1001 IFEQ may-a
SET loan:disb:A1001 may-b NX EX 300
EOF
'''

SH_DEDUP = r'''
r -c <<'EOF'
SET dedup:TX1001 1 NX EX 60
SET dedup:TX1001 1 NX EX 60
TTL dedup:TX1001
SET bl:jti-7f3a 1 EX 240
TTL bl:jti-7f3a
EXISTS bl:jti-7f3a
EXISTS bl:jti-0000
EOF
'''

PY_SIM = r'''
class Kho:                    # MÔ PHỎNG: kho có hạn, đồng hồ giả
    def __init__(self):
        self.het, self.t = {}, 0
    def set_nx_ex(self, khoa, han):
        if self.het.get(khoa, 0) > self.t:
            return None       # khoá còn sống: từ chối, như (nil)
        self.het[khoa] = self.t + han
        return "OK"
kho = Kho()
for kho.t in (0, 30, 61, 62):
    print("giây", kho.t, kho.set_nx_ex("dedup:TX1001", 60))
'''

SH_SHORT = r'''
$D sh -c '
c="redis-cli --no-raw -c -p 7000 SET dedup:TX2002 1 NX EX 2"
$c; sleep 1; $c; sleep 2; $c'
'''

SH_MULTI = r'''
r -c <<'EOF'
MSET acc:1 10 acc:2 20
CLUSTER KEYSLOT acc:1
CLUSTER KEYSLOT acc:2
MSET {acc}:1 10 {acc}:2 20
CLUSTER KEYSLOT {acc}:1
EOF
'''

# Đầu ra thật (chạy 2026-11-11: Python 3.13; Redis 8.10.3 trong Docker, Git Bash)
OUT_CRC = """
0x31c3 44950 12182
[(0, 5460), (5461, 10922), (10923, 16383)]
"""
OUT_START = """
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
[OK] All 16384 slots covered.
"""
OUT_SLOT = """
(integer) 12182
(error) MOVED 12182 127.0.0.1:7002
OK
"bar"
"""
OUT_LOCK = """
OK
(nil)
(integer) 300
(integer) 0
(integer) 1
OK
"""
OUT_DEDUP = """
-> Redirected to slot [9306] located at 127.0.0.1:7001
OK
(nil)
(integer) 60
OK
(integer) 240
(integer) 1
-> Redirected to slot [1074] located at 127.0.0.1:7000
(integer) 0
"""
OUT_SIM = """
giây 0 OK
giây 30 None
giây 61 OK
giây 62 None
"""
OUT_SHORT = """
OK
(nil)
OK
"""
OUT_MULTI = """
(error) CROSSSLOT Keys in request don't hash to the same slot
(integer) 16276
(integer) 4087
-> Redirected to slot [12007] located at 127.0.0.1:7002
OK
(integer) 12007
"""

# Từ ngoại không có luật đọc (CRC, JWT, TTL, NX, EX, MOVED…): lời đọc tiếng Việt, tên gốc chỉ hiện trên màn hình
SPOKEN = {"JWT": "mã Token tự mang thông tin"}

_KEEP_CASE = {"API", "Python", "Redis", "Docker", "Token", "A", "B", "C"}


def _lower_first(t):
    w = t.split(" ", 1)[0].strip(",:")
    if w in _KEEP_CASE or (len(w) > 1 and w.isupper()):
        return t
    return t[:1].lower() + t[1:]


def _fmerge(a, b):
    if a in (0, None):
        return b
    if b in (0, None):
        return a
    la, lb = (a if isinstance(a, list) else [a]), (b if isinstance(b, list) else [b])
    return la + [x for x in lb if x not in la]


def _merge_short(st_, minw=8, maxc=170, maxw=38):
    """Câu ≤ 7 từ ghép vào câu sau (hoặc câu trước) bằng dấu phẩy; focus ghép theo (như bài L03)."""
    ss = lv.sentences(st_["say"])
    foc = st_.get("focus")
    fl = list(foc) if isinstance(foc, list) and len(foc) == len(ss) else None
    j = 0
    while j < len(ss):
        if len(ss[j].split()) < minw and ss[j].endswith("."):
            nxt = ss[j][:-1] + ", " + _lower_first(ss[j + 1]) if j + 1 < len(ss) else None
            if nxt and len(nxt) <= maxc and len(nxt.split()) <= maxw:
                ss[j:j + 2] = [nxt]
                if fl:
                    fl[j:j + 2] = [_fmerge(fl[j], fl[j + 1])]
                continue
            if j > 0 and ss[j - 1].endswith("."):
                prv = ss[j - 1][:-1] + ", " + _lower_first(ss[j])
                if len(prv) <= maxc and len(prv.split()) <= maxw:
                    ss[j - 1:j + 1] = [prv]
                    if fl:
                        fl[j - 1:j + 1] = [_fmerge(fl[j - 1], fl[j])]
                    j -= 1
                    continue
        j += 1
    st_["say"] = " ".join(ss)
    if fl is not None:
        st_["focus"] = fl


def _spoken(scenes):
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            for a_, b_ in SPOKEN.items():
                s_["say"] = s_["say"].replace(a_, b_)
            _merge_short(s_)
    return scenes



# ── AF2 (WP4, 2026-11-14): cảnh quy mô + Tự làm ──
lib2.begin("L19")

PY_QUYMO = r'''
import binascii
dai = [(0, 5460), (5461, 10922), (10923, 16383)]
def nut(khoa):
    a = khoa.find("{")
    b = khoa.find("}", a + 1)
    if a >= 0 and b > a + 1:         # thẻ băm: chỉ băm phần trong {}
        khoa = khoa[a + 1:b]
    k = binascii.crc_hqx(khoa.encode(), 0) % 16384
    return next(i for i, (x, y) in enumerate(dai) if x <= k <= y)
for n in (3000, 300000):
    dem, the = [0, 0, 0], [0, 0, 0]
    for i in range(n):
        dem[nut(f"dedup:TX{i}")] += 1
        the[nut(f"dedup:{{tx}}:{i}")] += 1
    print(n, "khoa, nut 1-2-3:", dem, "| chung the bam:", the)
'''
P_QUYMO = prog("PhanBo", PY_QUYMO, lang="python", timeout=300,
               claims=["3 000 và 300 000 khoá dedup:TX… chia cho ba nút theo dải khe; cùng thẻ băm thì dồn hết về một nút"])

# Lab (số liệu khác ví dụ): cụm 4 nút, mỗi nút 4096 khe; khử trùng hạn 90 giây; danh sách đen
LAB_PY = r'''
import binascii

KHE = 16384
SO_NUT = 4


def khe(khoa):
    a = khoa.find("{")
    b = khoa.find("}", a + 1)
    if a >= 0 and b > a + 1:          # thẻ băm: chỉ băm phần trong {}
        khoa = khoa[a + 1:b]
    return binascii.crc_hqx(khoa.encode(), 0) % KHE


for khoa in ("loan:disb:B7", "dedup:TX9", "{acc}:5", "{acc}:6"):
    k = khe(khoa)
    print(f"{khoa} -> khe {k}, nut {k // (KHE // SO_NUT) + 1}")


class Kho:
    def __init__(self):
        self.het, self.t = {}, 0

    def set_nx_ex(self, khoa, han):
        if self.het.get(khoa, 0) > self.t:
            return None
        self.het[khoa] = self.t + han
        return "OK"


kho = Kho()
for kho.t in (0, 45, 90, 91):
    print("giay", kho.t, kho.set_nx_ex("dedup:TX9", 90))

print("han danh sach den:", 1000 - 640)
'''

LAB_OUT = """loan:disb:B7 -> khe 13590, nut 4
dedup:TX9 -> khe 11819, nut 3
{acc}:5 -> khe 12007, nut 3
{acc}:6 -> khe 12007, nut 3
giay 0 OK
giay 45 None
giay 90 OK
giay 91 None
han danh sach den: 360"""

LAB_DE = """# Lab BNX L19 — Khe băm trong cụm 4 nút, khử trùng hạn 90 giây, danh sách đen (không cần Redis)

Viết `mau.py` (Python, chỉ thư viện chuẩn). Số liệu là số minh hoạ. Mọi thứ chạy ngay trong Python, không cần Docker hay Redis: ta mô phỏng đúng công thức của Redis Cluster.

**Phần 1 — khe và nút.** Cụm có **4 nút**, chia 16384 khe thành 4 dải bằng nhau (nút 1: 0–4095, nút 2: 4096–8191, nút 3: 8192–12287, nút 4: 12288–16383).
Khe của một khoá = `CRC16(khoá) mod 16384`, với CRC16 kiểu XMODEM (đa thức 0x1021, giá trị đầu 0). Trong Python có sẵn hàm này: `binascii.crc_hqx(khoa.encode(), 0)`.
Với 4 khoá theo thứ tự `loan:disb:B7`, `dedup:TX9`, `{acc}:5`, `{acc}:6` in mỗi dòng `<khoá> -> khe <k>, nut <n>`. Lưu ý quy tắc thẻ băm: khoá có `{acc}` thì chỉ chữ `acc` được đem băm — hai khoá cuối phải cùng khe.

**Phần 2 — khử trùng.** Viết lớp `Kho` mô phỏng lệnh `SET khoá 1 NX EX hạn` với đồng hồ giả `t`: nếu khoá còn sống (`thời điểm hết hạn > t`) trả `None`; ngược lại ghi `thời điểm hết hạn = t + hạn` và trả `"OK"`.
Gửi mã giao dịch `dedup:TX9` với hạn **90 giây** ở các giây 0, 45, 90, 91 và in `giay <t> <kết quả>`.

**Phần 3 — danh sách đen.** Mã truy cập có hạn dùng đến giây 1000 bị thu hồi ở giây 640. In `han danh sach den: <hạn của mục danh sách đen>` (bằng thời gian còn lại của mã).

In đúng 9 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L19 mau.py`.
"""


def build():
    hook = sc("hook", "hook", "Bấm “Giải ngân” hai lần: tiền có ra hai lần không?", [
        st("""<p>Hồ sơ vay <b>A1001</b>, khoản vay 50 triệu đồng <i>(số minh hoạ)</i>. Mạng chậm, khách bấm nút “Giải ngân” <b>hai lần</b>,
và hai máy chủ ứng dụng cùng nhận yêu cầu.</p>
<div class="box key">Trên CV có bốn dòng về Redis: <b>Redis Cluster</b> lo mở rộng bộ nhớ và tải; ba dòng còn lại chặn trùng hoặc thu hồi: khoá <code>SET … NX EX 300</code>,
khử trùng theo mã giao dịch <b>hạn 60 giây</b>, và <b>danh sách đen</b> mã truy cập. Mỗi dòng làm việc gì, và hở ở đâu?</div>""",
           """Chào bạn, hồ sơ vay A một không không một có khoản vay năm mươi triệu đồng, số minh hoạ. Mạng chậm nên khách bấm giải ngân hai lần, và hai máy chủ cùng nhận yêu cầu. Hồ sơ xin việc có bốn dòng về Redis: cụm nhiều nút lo mở rộng, còn khoá có hạn lo chặn trùng hoặc thu hồi.""", focus=[1, 1, 2, 2]),
    ], checks=["alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_set_nx_ex([0, 30], 300) == ['OK', None]",
               "alg.bnx_l19_set_nx_ex([0, 30], 60)[1] is None"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Redis", "kho “khoá → giá trị” chạy trong bộ nhớ; mỗi lệnh chạy trọn vẹn, không lệnh nào chen vào giữa", "<code>SET foo bar</code> rồi <code>GET foo</code> trả <code>bar</code>"],
                  ["② hạn sống", "mỗi mục có thể kèm số giây; hết số giây đó Redis tự xoá mục", "đặt hạn 60: tới giây 60 mục biến mất"],
                  ["③ chia lấy dư (mod)", "phần còn lại sau khi chia hết số lần nguyên", "$44950 = 2 \\cdot 16384 + 12182$, nên 44950 mod 16384 = 12182"],
                  ["④ băm kiểm lỗi CRC16", "hàm đổi một chuỗi byte (byte: khúc dữ liệu gồm 8 bit; bit là chữ số 0 hoặc 1) thành một số 16 bit, từ 0 tới 65535; cùng chuỗi luôn ra cùng số", "CRC16 của <code>foo</code> = 44950"],
                  ["⑤ mã truy cập và mã giao dịch", "mã truy cập ghi sẵn hạn dùng <code>exp</code> và số riêng <code>jti</code>; mã giao dịch là số riêng của một yêu cầu chuyển tiền", "<code>jti-7f3a</code>; <code>TX1001</code>"]]),
           """Trước hết ta cần hiểu năm điều. Redis là kho khoá và giá trị trong bộ nhớ, mỗi lệnh chạy trọn vẹn. Mỗi mục có thể kèm hạn sống, hết hạn thì Redis tự xoá. Chia lấy dư là phần còn lại sau khi chia hết. Phép băm kiểm lỗi mười sáu bit đổi chuỗi byte, mỗi byte là tám chữ số nhị phân, thành một số mười sáu bit. Mã truy cập ghi sẵn hạn dùng, còn mã giao dịch là số riêng của một yêu cầu."""),
        st("""<p>Làm thử phép chia lấy dư:</p>
$$2 \\cdot 16384 = 32768, \\qquad 44950 - 32768 = \\hl{12182}$$""",
           """Làm thử phép chia lấy dư: bốn mươi tư nghìn chín trăm năm mươi trừ hai lần mười sáu nghìn ba trăm tám mươi tư còn mười hai nghìn một trăm tám mươi hai.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950", "44950 == 2 * 16384 + 12182", "alg.bnx_l19_crc16('foo') % 16384 == 12182",
               "2 * 16384 == 32768 and alg.bnx_l19_crc16('foo') - 32768 == 12182", "alg.bnx_l19_crc16(bytes([255]) * 4) <= 65535",
               "alg.bnx_l19_set_nx_ex([0, 59, 60], 60) == ['OK', None, 'OK']"])

    sym = sc("sym", "symbol", "Giải mã các từ trên màn hình", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["Redis Cluster, hash slot", "cụm nhiều nút Redis; không gian khoá chia thành <b>16384 khe băm</b>, đánh số 0 tới 16383"],
                  ["<code>CLUSTER KEYSLOT k</code>", "hỏi Redis: khoá <code>k</code> thuộc khe số mấy"],
                  ["<code>MOVED 12182 127.0.0.1:7002</code>", "lỗi chuyển hướng: “khe 12182 do nút ở cổng 7002 giữ, hãy gửi lại sang đó”"],
                  ["hash tag <code>{…}</code>", "thẻ băm: khoá có <code>{abc}</code> thì chỉ phần <code>abc</code> được đem băm; ngoặc rỗng <code>{}</code> thì băm cả khoá"]]),
           """Bảng này giải mã các từ trên màn hình. Cụm Redis chia khoá thành mười sáu nghìn ba trăm tám mươi tư khe băm. Lỗi chuyển hướng là câu trả lời của nút không giữ khe, kèm địa chỉ nút giữ. Thẻ băm là phần trong ngoặc nhọn, chỉ phần đó được băm.""", clear=True, introduces=['bnx_khe_bam', 'bnx_the_bam']),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["<code>SET k v NX EX 300</code>", "<b>NX</b>: chỉ đặt khi khoá chưa có; <b>EX 300</b>: hạn sống 300 giây; đặt được trả <code>OK</code>, không đặt được trả <code>(nil)</code>"],
                  ["<code>TTL k</code>", "số giây còn lại của khoá; −2 nếu khoá không tồn tại, −1 nếu khoá không có hạn"],
                  ["<code>DELEX k IFEQ v</code>", "xoá khoá <b>chỉ khi</b> giá trị đang lưu đúng bằng <code>v</code> (có từ Redis 8.4)"]]),
           """Lệnh đặt có hai tuỳ chọn: chỉ đặt khi khoá chưa có, và kèm hạn sống, đặt được thì trả chữ ô kê, không thì trả rỗng. Lệnh kế cho biết số giây còn lại, lệnh cuối chỉ xoá khi giá trị đúng bằng giá trị ta đưa vào.""", clear=True),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["nút chính, nút bản sao", "nút chính nhận lệnh ghi; nút bản sao chép lại dữ liệu của nút chính để thay thế khi nút chính hỏng; việc chép có độ trễ"],
                  ["ràng buộc duy nhất", "luật của cơ sở dữ liệu: hai bản ghi cùng mã thì bản ghi thứ hai bị từ chối"],
                  ["thu gom rác", "lúc máy ảo Java dọn bộ nhớ và tạm dừng cả chương trình trong chốc lát"],
                  ["<code>docker run</code>, <code>docker exec</code>, <code>&lt;&lt;'EOF'</code>, <code>r() { … }</code>, <code>0x31c3</code>", "chạy một chương trình đóng gói sẵn / chạy lệnh bên trong nó / đưa nhiều dòng lệnh vào một lệnh / đặt tên ngắn <code>r</code> cho một lệnh dài / số viết hệ 16 (16 chữ số: 0–9, a–f)"]]),
           """Nút chính nhận lệnh ghi, nút bản sao chép lại. Ràng buộc duy nhất từ chối bản ghi trùng mã. Thu gom rác là lúc máy ảo dọn bộ nhớ.""", clear=True, introduces=["bnx_thu_gom_rac"]),
        st(table(["từ", "nghĩa"],
                 [["máy khách", "chương trình gửi lệnh tới Redis, ở đây là ứng dụng của ngân hàng"],
                  ["tiến trình", "một chương trình đang chạy trên máy; mỗi nút Redis là một tiến trình"],
                  ["lõi ngân hàng", "hệ thống sổ cái chính của ngân hàng, nơi tiền thật được ghi"]]),
           """Ba từ nữa: máy khách gửi lệnh tới Redis, tiến trình là chương trình đang chạy, lõi ngân hàng là sổ cái chính ghi tiền thật.""", clear=True),
    ], checks=["alg.bnx_l19_slot('foo') == 12182 and alg.bnx_l19_node(12182) == 3", "alg.bnx_l19_hashed_part('{abc}:1') == 'abc'",
               "alg.bnx_l19_ranges()[-1][1] == 16383 and alg.bnx_l19_ranges()[0][0] == 0"])

    intu = sc("intuition", "intuition", "Hình dung: từ khoá tới nút, và một mục có hạn", [
        st(svg(1500, 480,
               box(30, 40, 200, 90, ["khoá", "foo"], C_BLUE, 26, True),
               box(320, 40, 260, 90, ["CRC16", "= 44950"], C_PURPLE, 26, True),
               box(670, 40, 300, 90, ["mod 16384", "= khe 12182"], C_AMBER, 26, True),
               arrow(235, 85, 315, 85), arrow(585, 85, 665, 85),
               box(60, 260, 400, 110, ["nút 1 (cổng 7000)", "khe 0 – 5460"], C_GRAY, 24, True),
               box(550, 260, 400, 110, ["nút 2 (cổng 7001)", "khe 5461 – 10922"], C_GRAY, 24, True),
               box(1040, 260, 400, 110, ["nút 3 (cổng 7002)", "khe 10923 – 16383"], C_GREEN, 24, True),
               arrow(975, 110, 1235, 255, "#16a34a"), txt(1200, 160, "10923 ≤ 12182 ≤ 16383", 22, "start", "#16a34a"),
               txt(750, 440, "Máy khách tự tính khe; nút nào giữ khe thì hỏi cụm hoặc theo MOVED, không cần máy trung gian", 24, "middle", "#1f2937", True)),
           """Hình cho thấy đường từ khoá tới nút: băm ra bốn mươi tư nghìn chín trăm năm mươi, lấy dư được khe mười hai nghìn một trăm tám mươi hai, thuộc nút thứ ba."""),
        st(svg(1500, 470,
               txt(60, 60, "giây", 24, "start", "#475569"),
               box(120, 90, 900, 80, "mục dedup:TX1001 còn sống (hạn 60 giây)", C_BLUE, 24, True),
               box(1020, 90, 420, 80, "đã tự xoá", C_GRAY, 24, False, True),
               txt(120, 210, "0", 24, "middle"), txt(570, 210, "30", 24, "middle"), txt(1020, 210, "60", 24, "middle"), txt(1035, 250, "61", 24, "start"),
               box(40, 290, 300, 90, ["giây 0: gửi lần đầu", "đặt được → xử lý"], C_GREEN, 22, True),
               box(430, 290, 320, 90, ["giây 30: gửi lại", "khoá còn → từ chối"], C_RED, 22, True),
               box(1000, 290, 380, 90, ["giây 61: gửi lại", "khoá hết → nhận như mới"], C_AMBER, 22, True),
               arrow(120, 285, 120, 225, "#16a34a"), arrow(570, 285, 570, 225, "#dc2626"), arrow(1050, 285, 1050, 262, "#d97706"),
               txt(750, 440, "Một mục có hạn chỉ “nhớ” trong đúng khoảng hạn của nó", 24, "middle", "#1f2937", True)),
           """Hình thứ hai cho thấy một mục có hạn sáu mươi giây. Giây số không mục chưa có nên được xử lý, giây ba mươi mục còn sống nên bị từ chối, giây sáu mươi mốt mục đã xoá nên được nhận."""),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950 and alg.bnx_l19_slot('foo') == 12182",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]", "alg.bnx_l19_node_of_key('foo') == 3",
               "alg.bnx_l19_set_nx_ex([0, 30, 61], 60) == ['OK', None, 'OK']"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một nút tới cụm, từ một lệnh tới ba cách dùng", [
        st("""<p><b>Bước 1.</b> Một nút không đủ bộ nhớ thì thêm nút. Mọi máy khách phải <b>tính giống nhau</b> khoá nào ở đâu, nên dùng một công thức cố định:</p>
$$\\text{khe} = \\text{CRC16}(\\text{khoá}) \\text{ mod } 16384$$
<span class='note'>Làm thử: CRC16(foo) = 44950; 44950 mod 16384 = 12182.</span>""",
           """Bước một, một nút không đủ bộ nhớ thì thêm nút. Mọi máy khách phải tính giống nhau khoá nào ở đâu, nên khe là kết quả băm chia lấy dư cho mười sáu nghìn ba trăm tám mươi tư.""", clear=True),
        st("""<p><b>Bước 2.</b> Nút giữ <b>dải khe</b>, không giữ từng khoá, vì thêm bớt nút chỉ cần chuyển khe. Ba nút: $16384 = 3 \\cdot 5461 + 1$, công cụ tạo cụm chia
<b>0–5460</b>, <b>5461–10922</b>, <b>10923–16383</b> (nút giữa nhận khe dư).</p>
<span class='note'>Làm thử: 12182 ≥ 10923 nên khoá foo ở nút thứ ba; hỏi nhầm nút thì nhận lỗi <code>MOVED</code>.</span>""",
           """Bước hai, mỗi nút giữ một dải khe chứ không giữ từng khoá, vì thêm bớt nút chỉ cần chuyển khe. Khoá mẫu ở nút thứ ba, hỏi nhầm nút thì nhận lỗi chuyển hướng."""),
        st("""<p><b>Bước 3.</b> Một lệnh đụng <b>nhiều khoá</b> chỉ chạy khi các khoá <b>cùng một khe</b>, vì mỗi nút chỉ thấy dữ liệu của mình.
Muốn ép cùng khe thì dùng thẻ băm: chỉ phần trong <code>{…}</code> được băm (ngoặc rỗng thì băm cả khoá).</p>
<span class='note'>Làm thử: <code>acc:1</code> ở khe 16276, <code>acc:2</code> ở khe 4087: khác khe. <code>{acc}:1</code> và <code>{acc}:2</code> cùng băm chữ <code>acc</code>: cùng khe 12007.</span>""",
           """Bước ba, lệnh đụng nhiều khoá chỉ chạy khi các khoá cùng một khe, vì mỗi nút chỉ thấy dữ liệu của mình. Thẻ băm ép chúng cùng khe: hai khoá tài khoản khác khe, còn chung thẻ băm thì cùng khe.""", clear=True),
        st("""<p><b>Bước 4.</b> Khoá giữ quyền: <code>SET loan:disb:A1001 may-a NX EX 300</code>.</p>
<ul><li><b>NX</b> gộp “kiểm rồi đặt” thành một lệnh, vì tách hai lệnh thì hai máy cùng thấy “chưa có”.</li>
<li><b>EX 300</b> vì máy giữ khoá có thể chết: sau 300 giây khoá tự nhả.</li>
<li>Giá trị <code>may-a</code> là <b>mã chủ khoá</b>: khi nhả, chỉ xoá nếu giá trị còn là của mình.</li></ul>
<span class='note'>Làm thử: máy B gửi cùng lệnh trong 300 giây đó thì nhận <code>(nil)</code>.</span>""",
           """Bước bốn là khoá giữ quyền: lệnh đặt chỉ khi chưa có, kèm hạn ba trăm giây. Gộp kiểm rồi đặt thành một lệnh vì tách hai thì hai máy cùng thấy chưa có. Hạn cần vì máy giữ khoá có thể chết."""),
        st("""<p><b>Bước 5.</b> Cùng một lệnh, đổi tên khoá là ra hai cách dùng nữa, vì cả hai đều là “nhớ một điều trong một khoảng thời gian”.</p>
<ul><li><b>Khử trùng</b>: khoá = mã giao dịch, hạn 60 giây. Đặt được thì xử lý; nhận <code>(nil)</code> thì đó là yêu cầu gửi lại.</li>
<li><b>Danh sách đen</b>: khoá = số riêng <code>jti</code> của mã truy cập bị thu hồi; hạn = thời gian còn lại của mã, vì sau đó mã tự hết hạn.</li></ul>
$$\\text{hạn mục danh sách đen} = \\text{exp} - \\text{bây giờ} = 300 - 60 = \\hl{240}\\ \\text{giây (số minh hoạ)}$$""",
           """Bước năm, cùng một lệnh đổi tên khoá là ra hai cách dùng nữa. Khử trùng trả lời rỗng nghĩa là yêu cầu gửi lại, còn danh sách đen có hạn bằng thời gian còn lại của mã, tức hai trăm bốn mươi giây.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950 and alg.bnx_l19_slot('foo') == 12182",
               "16384 == 3 * 5461 + 1 and alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]",
               "alg.bnx_l19_node(12182) == 3 and 12182 >= 10923",
               "alg.bnx_l19_slot('acc:1') == 16276 and alg.bnx_l19_slot('acc:2') == 4087",
               "alg.bnx_l19_slot('{acc}:1') == alg.bnx_l19_slot('{acc}:2') == 12007 and alg.bnx_l19_same_slot('{acc}:1', '{acc}:2')",
               "alg.bnx_l19_set_nx_ex([0, 100], 300) == ['OK', None]", "alg.bnx_l19_set_nx_ex([0, 30], 60) == ['OK', None]",
               "alg.bnx_l19_bl_ttl(300, 60) == 240"])

    ex = sc("example", "example", "Ví dụ chạy thật trên Redis 8.10.3, từng phép tính", [
        st(table(["ký hiệu trong hàm", "nghĩa", "ví dụ nhỏ"],
                 [["<code>c ^= x &lt;&lt; 8</code>", "<code>x &lt;&lt; 8</code> dịch x sang trái 8 bit, tức nhân 256; <code>^</code> cộng từng bit không nhớ (giống nhau cho 0, khác nhau cho 1); <code>^=</code> gán kết quả vào c", "<code>0b1010 ^ 0b0110 = 0b1100</code>; <code>3 &lt;&lt; 1 = 6</code>"],
                  ["<code>c &amp; 0x8000</code>", "chỉ giữ bit mà hai bên cùng là 1; <code>0x8000</code> chỉ có bit cao nhất của số 16 bit, nên kết quả khác 0 là bit cao nhất của c đang là 1", "<code>0b1100 &amp; 0b1000 = 0b1000</code>"],
                  ["<code>(c &lt;&lt; 1) ^ 0x1021</code>", "dịch trái 1 bit rồi cộng bit với <code>0x1021</code>, hằng của biến thể CRC16 XMODEM (số viết hệ 16); không thì chỉ dịch", "lặp 8 lần cho mỗi byte"],
                  ["<code>c &amp;= 0xFFFF</code>", "giữ lại đúng 16 bit thấp, bỏ bit tràn", "<code>0x1FFFF &amp; 0xFFFF = 0xFFFF</code>"]]),
           """Hàm băm dùng vài ký hiệu về bit. Dấu mũ cộng từng bit không nhớ: giống nhau cho không, khác nhau cho một. Dấu dịch trái nhân đôi, còn dấu và chỉ giữ bit mà cả hai cùng bằng một.""", clear=True),
        jstep([(("<code>def crc16(b):</code> … <code>return c</code>", "khai hàm nhận chuỗi byte b; dòng thụt vào là thân hàm; <code>return c</code> trả số c về chỗ gọi", "Khai hàm nhận chuỗi byte, dòng thụt vào là thân hàm, lệnh trả về đưa kết quả ra."), "<code>crc16(b\"foo\")</code> ra 44950", ""),
               (("<code>for x in b:</code>, <code>for _ in range(8):</code>", "vòng lặp: mỗi vòng x là một byte của b, lần lượt; <code>range(8)</code> cho đúng tám lượt, <code>_</code> là tên bỏ đi vì không dùng", "Vòng ngoài duyệt từng byte, vòng trong lặp đúng tám lượt."), "mỗi byte được trộn tám lần", ""),
               (("<code>A if đk else B</code>", "nếu điều kiện đúng thì giá trị là A, ngược lại là B; ở đây A là <code>(c &lt;&lt; 1) ^ 0x1021</code>, B là <code>c &lt;&lt; 1</code>, điều kiện là bit cao của c bằng 1", "Biểu thức điều kiện cho giá trị đầu nếu điều kiện đúng, ngược lại cho giá trị sau."), "<code>5 if 1 &gt; 0 else 9</code> ra 5", "")]),
        jstep([(("<code>b\"foo\"</code>, <code>hex(n)</code>", "chữ <code>b</code> trước dấu nháy: chuỗi <b>byte</b>, không phải chuỗi chữ; <code>hex(n)</code>: viết số n ở hệ 16", "Chữ b trước dấu nháy tạo chuỗi byte, còn hàm hex viết số ở hệ mười sáu."), "<code>hex(255)</code> ra <code>0xff</code>", ""),
               (("<code>print(a, b)</code>", "in các giá trị ra màn hình, cách nhau một dấu cách", "Lệnh in đưa các giá trị ra màn hình, cách nhau một dấu cách."), "<code>print(1, 2)</code> in <code>1 2</code>", ""),
               (("<code>[(a, a + n - 1) for a, n in ((0, 5461), …)]</code>", "danh sách sinh sẵn: lặp từng cặp (a, n), tính cặp (a, a + n − 1), gom hết vào một danh sách; ở đây đổi (điểm đầu, số khe) thành (điểm đầu, điểm cuối)", "Danh sách sinh sẵn lặp từng cặp, tính cặp mới rồi gom vào một danh sách."), "<code>(5461, 5462)</code> thành <code>(5461, 10922)</code>", "")], introduces=["bnx_thap_luc_phan"]),
        st(code(PY_CRC, "Tự tính khe băm bằng Python (không cần Redis)"),
           """Trước hết ta tự tính khe băm bằng Python, chưa cần Redis. Hàm là phép băm kiểm lỗi đi qua từng byte của khoá. Các dòng sau in kết quả băm, số dư và ba dải khe.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_CRC) + """
$$① \\; 44950 \\text{ mod } 16384 = 44950 - 2 \\cdot 16384 = \\hl{12182}$$
$$② \\; 10923 \\le 12182 \\Rightarrow \\hlg{\\text{nút thứ ba}}$$""",
           """Kết quả chạy thật: chuỗi thử chuẩn ra ba một C ba, đúng đặc tả. Phép tính thứ nhất ra mười hai nghìn một trăm tám mươi hai.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>for p in 7001 7002; do … done</code>", "lặp lại lệnh bên trong cho từng giá trị p: 7001 rồi 7002"],
                  ["<code>until … ; do sleep 1; done</code>", "chờ 1 giây rồi thử lại, cho tới khi lệnh điều kiện thành công"],
                  ["<code>grep -q state:ok</code>", "tìm chữ <code>state:ok</code> trong đầu vào, không in gì, chỉ báo thấy hay không"],
                  ["<code>&gt; /dev/null 2&gt;&amp;1</code>", "bỏ hết chữ in ra, cả thông báo lỗi, vào nơi bỏ đi của máy"]]),
           """Các lệnh dựng cụm dùng vài cú pháp của vỏ lệnh: vòng lặp cho từng cổng, vòng chờ thử lại mỗi giây, và dấu chuyển hướng ném chữ in ra vào nơi bỏ đi.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>docker run -d --name … redis:8.10.3 redis-server --port 7000 --cluster-enabled yes</code>", "chạy một hộp chứa: <code>-d</code> chạy nền, <code>--name</code> đặt tên, rồi tên ảnh; phần sau là lệnh chạy trong hộp: máy chủ Redis ở cổng 7000, bật chế độ cụm"],
                  ["<code>--cluster-config-file n7001.conf --daemonize yes</code>", "mỗi nút ghi trạng thái cụm vào một tệp riêng; <code>--daemonize yes</code> chạy nền"],
                  ["<code>redis-cli --cluster create … --cluster-yes | grep -E \"Slots|covered\"</code>", "tạo cụm từ ba nút và chia khe; <code>--cluster-yes</code> trả lời đồng ý mọi câu hỏi; <code>grep -E</code> chỉ giữ dòng có một trong hai chữ"]]),
           """Lệnh dựng cụm có nhiều cờ: chạy hộp có tên ở chế độ nền và bật chế độ cụm, mỗi nút thêm có tệp trạng thái riêng, còn lệnh tạo cụm chia khe.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>D=\"docker exec -i …\"</code>, rồi <code>$D …</code>", "đặt cả một lệnh vào biến <code>D</code>; <code>$D</code> chạy lệnh theo sau bên trong hộp"],
                  ["<code>r() { $D redis-cli --no-raw -p 7000 \"$@\"; }</code>", "hàm <code>r</code> gửi lệnh tới nút 7000; <code>\"$@\"</code> chuyển mọi tham số của <code>r</code> cho <code>redis-cli</code>; <code>--no-raw</code> in kiểu có nhãn <code>(integer)</code>, <code>(nil)</code>"]]),
           """Dòng đầu đặt cả lệnh vào một biến để dùng lại, và hàm ngắn chuyển mọi tham số cho công cụ.""", clear=True),
        st(code(SH_START, "Dựng cụm ba nút thật (thu nhỏ: ba tiến trình Redis trong một container Docker)") + "<p class='note'>Số phiên bản Redis 8.10.3 là ảnh dùng lúc ghi hình; chưa đối chiếu độc lập với trang phát hành (NOT_VERIFIED). <code>DELEX … IFEQ</code> có từ Redis 8.4 (cũng NOT_VERIFIED độc lập).</p>",
           """Bây giờ ta dựng một cụm thật bằng Docker, bản thu nhỏ: ba tiến trình Redis chạy chung một hộp chứa, còn cụm thật đặt mỗi nút trên một máy riêng. Lệnh cuối chia khe cho ba nút.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_START),
           """Kết quả chạy thật: ba nút nhận đúng ba dải khe ta vừa tính, và dòng cuối xác nhận mọi khe đã có chủ.""", clear=True),
        st(code(SH_SLOT, "Hỏi Redis thật: khoá foo ở khe nào, nút nào"),
           """Ta hỏi Redis thật bốn lệnh. Lệnh một hỏi khe của khoá mẫu, lệnh hai đặt giá trị gửi tới nút không giữ khe này, hai lệnh sau thêm chế độ cụm để tự theo lời chuyển hướng.""",
           clear=True),
        st(out(OUT_SLOT, "Kết quả chạy thật (đã lược các dòng “-> Redirected …” mà redis-cli -c in thêm)"),
           """Kết quả chạy thật. Redis trả đúng khe mười hai nghìn một trăm tám mươi hai. Nút thứ nhất từ chối và chỉ sang cổng bảy nghìn không trăm linh hai, tức nút thứ ba, còn chế độ cụm thì tự gửi lại sang đó.""", clear=True),
        st(code(SH_LOCK, "Khoá giải ngân hồ sơ A1001: hai máy tranh nhau"),
           """Tiếp theo là khoá giải ngân của hồ sơ A một không không một. Máy A đặt khoá kèm mã chủ khoá, máy B gửi cùng lệnh, rồi xem hạn. Sau đó B nhả bằng mã của B, A nhả bằng mã của A, rồi B xin lại.""",
           clear=True),
        st(out(OUT_LOCK) + """
$$③ \\; 300 - 120 = \\hlg{180}\\ \\text{giây dư nếu A xong ở giây 120 và nhả ngay (số minh hoạ)}$$""",
           """Kết quả chạy thật: máy A đặt được, máy B nhận trả lời rỗng, hạn còn ba trăm giây. B sai mã nên không xoá được, A xoá được, rồi B lấy được. Phép tính thứ ba: nhả sớm ở giây một trăm hai mươi thì khỏi giữ thêm một trăm tám mươi giây.""", clear=True),
        st(code(SH_DEDUP, "Khử trùng mã giao dịch TX1001 và danh sách đen mã truy cập"),
           """Ba lệnh đầu là khử trùng: đặt mã giao dịch hạn sáu mươi giây, gửi lại, rồi xem hạn. Các lệnh sau là danh sách đen: ghi mã bị thu hồi hạn hai trăm bốn mươi giây, rồi hỏi hai mã.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_DEDUP) + """
$$④ \\; 30 < 60 \\Rightarrow \\hl{\\text{từ chối}}; \\quad 61 \\ge 60 \\Rightarrow \\hlg{\\text{được nhận}}; \\qquad ⑤ \\; 300 - 60 = \\hl{240}\\ \\text{giây}$$""",
           """Kết quả chạy thật: lần đặt đầu thành công, lần gửi lại nhận trả lời rỗng. Phép tính thứ tư và thứ năm khớp: giây ba mươi từ chối, giây sáu mươi mốt nhận, hạn danh sách đen hai trăm bốn mươi giây.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('123456789') == 0x31C3", "alg.bnx_l19_crc16('foo') == 44950 and 44950 - 2 * 16384 == 12182",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)] and alg.bnx_l19_node(12182) == 3",
               "[b - a + 1 for a, b in alg.bnx_l19_ranges()] == [5461, 5462, 5461]",
               "alg.bnx_l19_set_nx_ex([0, 0], 300) == ['OK', None]", "alg.bnx_l19_lock_story(300, 120) == (1, 1) and 300 - 120 == 180",
               "alg.bnx_l19_slot('dedup:TX1001') == 9306 and alg.bnx_l19_node(9306) == 2",
               "alg.bnx_l19_slot('bl:jti-0000') == 1074 and alg.bnx_l19_node(1074) == 1",
               "alg.bnx_l19_set_nx_ex([0, 30, 61, 62], 60) == ['OK', None, 'OK', None]", "alg.bnx_l19_bl_ttl(300, 60) == 240"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: Redis thật với hạn thu nhỏ, và thẻ băm", [
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>$D sh -c '…'</code>, <code>$c</code>", "chạy cả đoạn lệnh bằng vỏ lệnh bên trong hộp; biến <code>c</code> giữ sẵn một lệnh, <code>$c</code> chạy nó"],
                  ["<code>MSET k1 v1 k2 v2</code>", "đặt nhiều khoá bằng một lệnh (khác với <code>SET</code> chỉ đặt một khoá)"]]),
           """Phần kiểm dùng thêm hai chỗ mới nên ta giải trước: đoạn lệnh chạy bằng vỏ lệnh trong hộp, và lệnh đặt nhiều khoá bằng một lệnh.""", clear=True),
        st(code(SH_SHORT, "Đường khác cho phép ④: Redis thật, hạn thu nhỏ còn 2 giây") + out(OUT_SHORT),
           """Phép tính thứ tư mới chỉ tính tay, nên ta kiểm bằng Redis thật với hạn thu nhỏ còn hai giây. Lệnh đặt gửi ba lần: ngay đầu, sau một giây, rồi sau thêm hai giây. Kết quả được nhận, từ chối, được nhận, như phép tính tay.""", clear=True),
        st(code(SH_MULTI, "Đường khác cho bước 3: lệnh nhiều khoá trên cụm thật"),
           """Ta kiểm bước ba trên cụm thật, vì lệnh nhiều khoá dễ sai: đặt hai khoá tài khoản trong một lệnh, hỏi khe từng khoá, rồi đặt hai khoá chung thẻ băm.""",
           clear=True),
        st(out(OUT_MULTI),
           """Kết quả chạy thật: lệnh đầu bị từ chối vì hai khoá ở khe mười sáu nghìn hai trăm bảy mươi sáu và bốn nghìn không trăm tám mươi bảy. Chung thẻ băm thì lệnh chạy được ở khe mười hai nghìn không trăm linh bảy.""", clear=True),
    ], checks=["alg.bnx_l19_set_nx_ex([0, 1, 3], 2) == ['OK', None, 'OK']",
               "alg.bnx_l19_slot('acc:1') == 16276 and alg.bnx_l19_slot('acc:2') == 4087 and not alg.bnx_l19_same_slot('acc:1', 'acc:2')",
               "alg.bnx_l19_slot('{acc}:1') == 12007 and alg.bnx_l19_node(12007) == 3",
               "alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_slot('dedup:TX1001') == 9306 and alg.bnx_l19_node(9306) == 2",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]"])

    quymo = sc("quymo", "example", "Khi số khoá lớn dần: chia đều cho ba nút, và khi thẻ băm dồn về một nút", [
        jstep([(("<code>khoa.find(\"{\")</code>", "vị trí của <code>{</code> đầu tiên trong chuỗi, hoặc −1 nếu không có; <code>khoa.find(\"}\", a + 1)</code> tìm từ vị trí a + 1", "Hàm tìm cho vị trí ngoặc nhọn đầu tiên, hoặc trừ một nếu không có."), "<code>\"x{ab}\".find(\"{\")</code> ra 1", ""),
               (("<code>khoa[a + 1:b]</code>", "cắt lát: lấy phần từ vị trí a + 1 tới trước vị trí b; ở đây là phần nằm giữa hai ngoặc nhọn", "Cắt lát lấy đoạn từ vị trí đầu tới trước vị trí cuối."), "<code>\"x{ab}\"[2:4]</code> ra <code>ab</code>", ""),
               (("<code>next(i for i, (x, y) in enumerate(dai) if x &lt;= k &lt;= y)</code>", "duyệt các dải khe; <code>enumerate</code> cho thêm số thứ tự i; <code>next</code> lấy i đầu tiên thoả <code>x &lt;= k &lt;= y</code>, tức k nằm trong dải", "Duyệt các dải khe kèm số thứ tự, lấy số đầu tiên mà khe nằm trong dải."), "k = 12182 ra 2, tức nút thứ ba", "")]),
        st(P_QUYMO.show(lines=(1, 8), title="PhanBo.py (1/2): nút giữ khe của một khoá, có tính thẻ băm"),
           """Ta đếm thật. Python có sẵn phép băm này, cho cùng kết quả với hàm tự viết. Hàm nút lấy phần trong thẻ băm nếu có, băm rồi tra dải khe để biết nút giữ khoá.""", clear=True),
        jstep([(("<code>for n in (3000, 300000):</code>", "chạy hai lần, n bằng 3000 rồi 300000; <code>range(n)</code>: i đi từ 0 tới n − 1", "Vòng ngoài chạy hai cỡ, vòng trong cho i đi từ không tới n trừ một."), "mỗi cỡ đếm lại từ đầu", ""),
               (("<code>f\"dedup:{{tx}}:{i}\"</code>", "chuỗi f: <code>{i}</code> được thay bằng giá trị của i; ngoặc nhọn gấp đôi in ra một ngoặc nhọn thật", "Chuỗi có chữ f thay phần trong ngoặc nhọn bằng giá trị, ngoặc gấp đôi in ra một ngoặc thật."), "i = 7 ra <code>dedup:{tx}:7</code>", ""),
               (("<code>dem[nut(…)] += 1</code>", "<code>dem</code> là danh sách ba ô đếm; <code>nut(…)</code> cho số nút 0, 1 hoặc 2; <code>+= 1</code> tăng ô của nút đó thêm 1", "Danh sách có ba ô đếm, hàm nút chọn ô để tăng thêm một."), "nút 2 thì <code>dem[2]</code> tăng 1", "")]),
        st(P_QUYMO.show(lines=(9, 15), title="PhanBo.py (2/2): đếm khoá về từng nút, ở hai cỡ"),
           """Với mỗi cỡ, ta đếm khoá mã giao dịch về từng nút, rồi đếm lại khi mọi khoá chung một thẻ băm.""", clear=True),
        st(P_QUYMO.out_html(),
           """Kết quả chạy thật cho thấy khoá chia gần đều ba nút ở cả hai cỡ, còn khi chung thẻ băm thì toàn bộ về một nút.""", clear=True),
        st(table(["số khoá", "chia ba nút (đo thật)", "chung một thẻ băm (đo thật)", "mục khử trùng sống cùng lúc = tốc độ × 60 giây (mô hình)"],
                 [[nowrap("3 000 (×1)"), "994 / 994 / 1 012", "0 / 0 / 3 000", "100 yêu cầu/giây: 6 000 mục"],
                  [nowrap("300 000 (×100)"), "100 008 / 99 949 / 100 043", "0 / 0 / 300 000", "10 000 yêu cầu/giây: 600 000 mục"],
                  [nowrap("30 000 000 (×10 000)"), "(cùng quy luật, chưa đo)", "một nút giữ hết", "1 000 000 yêu cầu/giây: 60 000 000 mục"]])
           + "<p style='margin-top:14px'><span class='note'>Hai cỡ đầu đo thật bằng Python (cỡ 3 000 khoá cũng đã đối chiếu với Redis thật ở bộ kiểm); dòng cuối là mô hình, chưa đo.</span></p>",
           """Khoá chia gần đều ba nút ở cả hai cỡ, lệch chưa tới hai phần trăm. Một thẻ băm chung thì nút thứ ba gánh hết, cụm mất tác dụng. Số mục khử trùng sống cùng lúc bằng tốc độ nhân hạn, nên ở một triệu yêu cầu mỗi giây là sáu mươi triệu.""", clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["một nút, mọi khoá", "lệnh nhiều khoá chạy thoải mái", "bộ nhớ và tải bị chặn bởi một máy", "dữ liệu nhỏ, tải thấp"],
                  ["cụm, thẻ băm theo từng đối tượng", "chia đều tải, lệnh nhiều khoá trong một đối tượng vẫn chạy", "lệnh nhiều khoá khác đối tượng bị từ chối", "dữ liệu lớn dần"],
                  ["cụm, một thẻ băm chung", "lệnh nhiều khoá chạy hết", "một nút gánh toàn bộ, mất lợi ích của cụm", "không nên"]]),
           """Một nút gãy khi dữ liệu vượt một máy. Cụm chia khe, đổi lại lệnh nhiều khoá khác đối tượng bị từ chối, nên đặt thẻ băm theo từng đối tượng.""", clear=True),
    ], checks=["alg.bnx_l19_node_counts(3000) == [994, 994, 1012] and alg.bnx_l19_node_counts(3000, True) == [0, 0, 3000]",
               "sum([100008, 99949, 100043]) == 300000 and sum([994, 994, 1012]) == 3000",
               "[alg.bnx_l19_live_dedup(r, 60) for r in (100, 10000, 1000000)] == [6000, 600000, 60000000]",
               "alg.bnx_l19_live_dedup(10000, 60) // alg.bnx_l19_live_dedup(100, 60) == 100",
               "alg.bnx_l19_live_dedup(1000000, 60) // alg.bnx_l19_live_dedup(100, 60) == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp theo thời gian: lúc mới dựng, lúc tải tăng, lúc vận hành lâu", [
        st("""<div class="box warn"><b>Lỗi 1 (lúc mới dựng).</b> Nhả khoá bằng <code>DEL</code> thẳng, hoặc đặt giá trị khoá là số <code>1</code> cho mọi máy.
Máy A quá hạn, máy B đã lấy khoá, rồi A chạy tới dòng nhả và <b class="red">xoá mất khoá của B</b>.
<br><span class="note">Cách chữa: giá trị là mã chủ khoá ngẫu nhiên; nhả bằng lệnh “chỉ xoá nếu giá trị còn là của tôi” (<code>DELEX … IFEQ</code>; bản Redis cũ hơn 8.4 dùng một đoạn kịch bản nhỏ so rồi xoá).</span></div>""",
           """Lỗi thứ nhất lúc mới dựng là nhả khoá bằng lệnh xoá thẳng, nên máy A quá hạn có thể xoá mất khoá của B. Hãy dùng mã chủ khoá ngẫu nhiên và lệnh chỉ xoá khi giá trị là của mình.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (lúc tải tăng, chuyển từ một nút sang cụm).</b> Mã đang chạy tốt trên một nút bỗng báo
<code class="red">CROSSSLOT</code>, vì lệnh nhiều khoá chỉ chạy trong cụm khi các khoá <b>cùng một khe băm</b>.
Chữa vội bằng cách gắn <b>cùng một thẻ băm cho mọi khoá</b> thì mọi khoá dồn về một nút, cụm mất tác dụng (bảng quy mô vừa đo).
<br><span class="note">Cách chữa: thẻ băm theo từng đối tượng, ví dụ theo mã hồ sơ. Chú ý: viết nguyên <code>loan:disb:{A1001}</code> thì Redis chỉ băm chữ <code>A1001</code> (khe 1830, khác khe 5075 của <code>loan:disb:A1001</code>).</span></div>""",
           """Lỗi thứ hai khi chuyển sang cụm: bỗng báo lỗi các khoá không cùng khe. Chữa vội bằng một thẻ băm chung thì mọi khoá dồn về một nút, nên hãy đặt thẻ băm theo từng đối tượng.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Tin rằng khoá Redis có hạn là <b>loại trừ tuyệt đối</b>.
Khoá hạn 300 giây, tiến trình A bị dừng tới giây 320 (thu gom rác, máy ảo bị treo, gọi lõi ngân hàng chậm): quá hạn 320 − 300 = <b class="red">20 giây</b>,
B đã lấy khoá, và <b>cả hai cùng giải ngân</b>. Nút chính hỏng trước khi nút bản sao nhận khoá cũng gây hiệu ứng tương tự.
<br><span class="note">Cách chữa: khoá chỉ để giảm tranh chấp; lớp chặn cuối nằm ở cơ sở dữ liệu (ràng buộc duy nhất theo mã hồ sơ, hoặc đổi trạng thái có điều kiện).</span></div>""",
           """Lỗi thứ ba, của người đã đi làm: tin rằng khoá Redis có hạn là loại trừ tuyệt đối. Tiến trình A bị dừng quá hạn hai mươi giây nên máy B lấy được khoá và cả hai cùng giải ngân, nên lớp chặn cuối là ràng buộc duy nhất.""", clear=True),
        st("<p><b>Lỗi 4 (người đã đi làm, lúc đối tác đổi cách thử lại).</b> Hạn khử trùng ngắn hơn thời gian thử lại của bên gửi <i>(số minh hoạ)</i>.</p>"
           + table(["bên gửi thử lại ở giây", "hạn khử trùng 60 giây", "hạn khử trùng 120 giây"],
                   [["30", "30 &lt; 60: từ chối", "30 &lt; 120: từ chối"],
                    ["90", "90 ≥ 60: mục đã hết, <b class='red'>xử lý lần hai</b>", "90 &lt; 120: từ chối"]])
           + "<p class='note'>Cách chữa: hạn dài hơn khoảng thử lại dài nhất của bên gửi; và vẫn giữ ràng buộc duy nhất theo mã giao dịch ở cơ sở dữ liệu.</p>",
           """Lỗi thứ tư: hạn khử trùng ngắn hơn thời gian thử lại của bên gửi. Hạn sáu mươi giây mà bên gửi thử lại ở giây chín mươi thì xử lý hai lần, nên hạn phải dài hơn.""",
           focus=[1, 2, 3], clear=True),
    ], checks=["alg.bnx_l19_lock_story(300, 320, owner_check=False) == (2, 1)", "alg.bnx_l19_lock_story(300, 320) == (2, 0)",
               "alg.bnx_l19_overrun(300, 320) == 20", "alg.bnx_l19_slot('loan:disb:{A1001}') == 1830 and alg.bnx_l19_slot('loan:disb:A1001') == 5075",
               "alg.bnx_l19_hashed_part('loan:disb:{A1001}') == 'A1001'", "alg.bnx_l19_processed([0, 90], 60) == 2",
               "alg.bnx_l19_processed([0, 90], 120) == 1", "alg.bnx_l19_set_nx_ex([0, 30], 60)[1] is None and alg.bnx_l19_set_nx_ex([0, 30], 120)[1] is None", "not alg.bnx_l19_same_slot('acc:1', 'acc:2')"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "CRC16 của khoá <code>hello</code> là 50018. Khoá này ở khe nào, và nút nào trong cụm ba nút 0–5460, 5461–10922, 10923–16383?"],
                  ["2", "Mã giao dịch đặt hạn 60 giây ở giây 0. Bên gửi gửi lại ở giây 45 và giây 75: mỗi lần được nhận hay bị từ chối? Mã truy cập hạn 900 giây bị thu hồi ở giây 250: mục danh sách đen đặt hạn bao nhiêu?"],
                  ["3", "Quyết định: chống giải ngân hai lần cho một hồ sơ bằng (a) chỉ khoá Redis hạn 300 giây, (b) chỉ ràng buộc duy nhất ở cơ sở dữ liệu, hay (c) cả hai?"]]),
           """Đến lượt bạn. Câu một, kết quả băm của một khoá là năm mươi nghìn không trăm mười tám, khoá ở khe và nút nào? Câu hai, mã giao dịch hạn sáu mươi giây gửi lại ở giây bốn mươi lăm và bảy mươi lăm thì sao? Còn mã truy cập hạn chín trăm giây thu hồi ở giây hai trăm năm mươi thì hạn danh sách đen là bao nhiêu? Câu ba, chống giải ngân hai lần nên chọn cách nào? Hãy dừng video.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""<p>Câu 1: $3 \\cdot 16384 = 49152$.</p>
$$50018 - 49152 = \\hlg{866}; \\qquad 0 \\le 866 \\le 5460 \\Rightarrow \\hlg{\\text{nút thứ nhất}}$$""",
           """Đáp án câu một. Ba lần mười sáu nghìn ba trăm tám mươi tư là bốn mươi chín nghìn một trăm năm mươi hai, nên khe là tám trăm sáu mươi sáu, thuộc nút thứ nhất."""),
        st("""<p>Câu 2:</p>
$$45 < 60 \\Rightarrow \\hl{\\text{từ chối}}; \\qquad 75 \\ge 60 \\Rightarrow \\hlg{\\text{được nhận}}; \\qquad 900 - 250 = \\hlg{650}\\ \\text{giây}$$""",
           """Đáp án câu hai. Giây bốn mươi lăm còn trong hạn nên bị từ chối, giây bảy mươi lăm quá hạn nên được nhận. Hạn danh sách đen là chín trăm trừ hai trăm năm mươi, tức sáu trăm năm mươi giây."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["(a) chỉ khoá Redis hạn 300 giây", "nhanh; chặn sớm phần lớn lần bấm trùng", "tiến trình dừng quá 300 giây, hoặc nút chính hỏng trước khi nút bản sao kịp nhận khoá, thì vẫn giải ngân hai lần"],
                  ["(b) chỉ ràng buộc duy nhất ở cơ sở dữ liệu", "đúng tuyệt đối: lần ghi thứ hai bị từ chối", "cả hai máy cùng gọi lõi ngân hàng rồi mới biết trùng; tốn tải, phải hoàn tác"],
                  ["(c) khoá Redis + ràng buộc duy nhất", "khoá chặn sớm, cơ sở dữ liệu bảo đảm đúng", "thêm một hệ phải vận hành; phải quyết định làm gì khi Redis hỏng"]]),
           """Đáp án câu ba. Chỉ khoá Redis thì nhanh nhưng tiến trình dừng quá hạn vẫn giải ngân hai lần. Chỉ ràng buộc ở cơ sở dữ liệu thì đúng nhưng hai máy cùng gọi lõi ngân hàng rồi mới biết trùng. Dùng cả hai thì khoá chặn sớm, còn cơ sở dữ liệu bảo đảm.""",
           focus=["1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l19_crc16('hello') == 50018", "3 * 16384 == 49152 and 50018 - 49152 == 866 == alg.bnx_l19_slot('hello')",
               "alg.bnx_l19_node(866) == 1", "alg.bnx_l19_set_nx_ex([0, 45], 60) == ['OK', None]",
               "alg.bnx_l19_set_nx_ex([0, 75], 60) == ['OK', 'OK']", "alg.bnx_l19_bl_ttl(900, 250) == 650",
               "alg.bnx_l19_lock_story(300, 301)[0] == 2"])

    lab_pr = practice_scene(sc, "Tự làm: khe và nút trong cụm 4 nút, khử trùng hạn 90 giây, danh sách đen", practice_steps2(
        st, "BNX", "L19",
        """<p><b>Đề</b>: viết <code>mau.py</code> (Python, không cần Redis):</p>
<ol><li>cụm <b>4 nút</b>, mỗi nút 4096 khe: in <code>khoá -&gt; khe k, nut n</code> cho <code>loan:disb:B7</code>, <code>dedup:TX9</code>, <code>{acc}:5</code>, <code>{acc}:6</code> (khe = CRC16 mod 16384; gợi ý <code>binascii.crc_hqx(b, 0)</code>)</li>
<li>lớp <code>Kho</code> mô phỏng <code>SET … NX EX 90</code> với đồng hồ giả; gửi <code>dedup:TX9</code> ở giây 0, 45, 90, 91</li>
<li>mã truy cập hạn đến giây 1000 bị thu hồi ở giây 640: in hạn mục danh sách đen</li></ol>
<p class="note">Chi tiết từng dòng in nằm trong <code>de.md</code>. Số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết chương trình Python tính khe và nút của bốn khoá trong cụm bốn nút. Rồi viết kho mô phỏng khử trùng, và tính hạn danh sách đen.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> khe = <code>binascii.crc_hqx(khoa.encode(), 0) % 16384</code>; nút = <code>khe // 4096 + 1</code>. Thẻ băm <code>{acc}</code> khiến hai khoá cuối cùng khe. Kho: khoá còn sống khi <code>het[khoa] &gt; t</code>.
Lời giải đầy đủ ở <code>labs/BNX/L19/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, nút là khe chia cho bốn nghìn không trăm chín mươi sáu cộng một, và kho coi khoá còn sống khi thời điểm hết hạn lớn hơn đồng hồ giả. Lời giải chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L19")

    rec = sc("recap", "recap", "Chuỗi logic, tư duy, và góc phỏng vấn theo CV", [
        st(chain("khe = CRC16(khoá) mod 16384", "nút giữ dải khe, sai nút thì MOVED", "SET NX EX + mã chủ khoá", "cùng lệnh: khử trùng, danh sách đen",
                 "lớp chặn cuối ở cơ sở dữ liệu"),
           """Tổng kết: khe của khoá là kết quả băm chia lấy dư, mỗi nút giữ một dải khe. Khoá giữ quyền là lệnh đặt chỉ khi chưa có, kèm hạn và mã chủ khoá, và cũng dùng để khử trùng."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["“Redis Cluster: một khoá nằm ở nút nào, và lệnh nhiều khoá thì sao?”", "khe = CRC16(khoá) mod 16384, nút giữ dải khe, sai nút trả MOVED; lệnh nhiều khoá cần cùng khe, ép bằng thẻ băm"],
                  ["“<code>SET loan:disb:{app_id} 1 NX EX 300</code> có bảo đảm chỉ giải ngân một lần không?”", "không tuyệt đối: tiến trình dừng quá 300 giây hoặc nút chính hỏng thì hai máy cùng làm; cần mã chủ khoá khi nhả và ràng buộc duy nhất ở cơ sở dữ liệu"],
                  ["“Vì sao hạn khử trùng 60 giây, và danh sách đen đặt hạn bao nhiêu?”", "hạn phải dài hơn khoảng thử lại của bên gửi; mục danh sách đen sống đúng bằng thời gian còn lại của mã truy cập"]]),
           """Người phỏng vấn hay hỏi ba câu. Về cụm, nói công thức khe, lỗi chuyển hướng và thẻ băm. Về khoá giải ngân, nêu mã chủ khoá và ràng buộc duy nhất, còn hạn khử trùng phải dài hơn khoảng thử lại.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> mọi thứ có hạn trong Redis chỉ “nhớ” trong khoảng hạn đó. Trước khi tin nó, hãy hỏi:
<b>điều gì xảy ra ở giây ngay sau khi hết hạn</b>, và khi tải tăng mười nghìn lần thì có bao nhiêu mục sống cùng lúc?</div>""",
           """Điều cần mang theo là mọi thứ có hạn trong Redis chỉ nhớ trong khoảng hạn đó. Hãy hỏi điều gì xảy ra ngay sau khi hết hạn, và khi tải tăng mười nghìn lần thì có bao nhiêu mục sống."""),
    ], checks=["alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_lock_story(300, 320)[0] == 2", "alg.bnx_l19_processed([0, 90], 60) == 2",
               "alg.bnx_l19_bl_ttl(300, 60) == 240"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L19", "redis_cum_khoa_khu_trung",
                  "Bài 19 — Redis nâng cao: cụm 16384 khe băm, khoá có hạn, khử trùng và danh sách đen",
                  "curriculum/bnx.yaml L19; audit/bnx/verify_bnx.py L19; Redis cluster specification, Scale with Redis Cluster, lệnh SET, TTL, EXPIRE, "
                  "Distributed Locks with Redis (redis.io, đọc 2026-11-11, audit/bnx/sources_l19.md); chạy thật Redis 8.10.3 trong Docker",
                  ["Tính khe băm của một khoá và chỉ ra nút giữ khe đó trong cụm ba nút",
                   "Giải thích lệnh đặt khoá chỉ khi chưa có, kèm hạn sống, và vì sao phải có mã chủ khoá",
                   "Khử trùng yêu cầu gửi lại bằng mã giao dịch có hạn 60 giây",
                   "Thu hồi một mã truy cập trước hạn bằng danh sách đen có hạn sống"],
                  scenes,
                  covers=[(1, "example"), (2, "formula"), (3, "practice"), (4, "example")])


# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L19", LAB_DE, "py", LAB_PY, LAB_OUT)
