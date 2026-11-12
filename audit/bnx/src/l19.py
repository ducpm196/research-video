from lib import *

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


def build():
    hook = sc("hook", "hook", "Bấm “Giải ngân” hai lần: tiền có ra hai lần không?", [
        st("""<p>Hồ sơ vay <b>A1001</b>, khoản vay 50 triệu đồng <i>(số minh hoạ)</i>. Mạng chậm, khách bấm nút “Giải ngân” <b>hai lần</b>,
và hai máy chủ ứng dụng cùng nhận yêu cầu.</p>
<div class="box key">Trên CV có bốn dòng về Redis để chặn chuyện này: <b>Redis Cluster</b>, khoá <code>SET … NX EX 300</code>,
khử trùng theo mã giao dịch <b>hạn 60 giây</b>, và <b>danh sách đen</b> mã truy cập. Mỗi dòng làm việc gì, và hở ở đâu?</div>""",
           """Chào bạn, hồ sơ vay A một không không một có khoản vay năm mươi triệu đồng, đây là số minh hoạ. Mạng chậm nên khách bấm nút giải ngân hai lần, và hai máy chủ ứng dụng cùng nhận yêu cầu.
           Có bốn kỹ thuật dùng Redis để chặn chuyện này: cụm nhiều nút, khoá có hạn, khử trùng theo mã giao dịch, và danh sách đen mã truy cập.
           Bài này trả lời từng kỹ thuật làm việc gì, và còn hở ở đâu.""", focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["một khoá nằm ở nút nào của cụm", "khe băm = CRC16(khoá) mod 16384; mỗi nút giữ một dải khe"],
                  ["vì sao khoá cần hạn và cần mã chủ khoá", "hạn để máy chết thì khoá tự nhả; mã chủ khoá để không nhả nhầm khoá của máy khác"],
                  ["gửi lại và thu hồi thì chặn bằng gì", "một mục có hạn sống: mã giao dịch hạn 60 giây; mã truy cập bị thu hồi hạn bằng thời gian còn lại"]]),
           """Hôm nay ta trả lời ba câu. Một khoá nằm ở nút nào của cụm, tính bằng khe băm. Vì sao khoá giữ quyền phải có hạn và phải có mã chủ khoá.
           Và yêu cầu gửi lại hay mã truy cập bị thu hồi thì chặn bằng gì, câu trả lời là một mục có hạn sống.""", clear=True),
    ], checks=["alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_set_nx_ex([0, 30], 300) == ['OK', None]",
               "alg.bnx_l19_set_nx_ex([0, 30], 60)[1] is None"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Redis", "kho “khoá → giá trị” chạy trong bộ nhớ; mỗi lệnh chạy trọn vẹn, không lệnh nào chen vào giữa", "<code>SET foo bar</code> rồi <code>GET foo</code> trả <code>bar</code>"],
                  ["② hạn sống", "mỗi mục có thể kèm số giây; hết số giây đó Redis tự xoá mục", "đặt hạn 60: tới giây 60 mục biến mất"],
                  ["③ chia lấy dư (mod)", "phần còn lại sau khi chia hết số lần nguyên", "$44950 = 2 \\cdot 16384 + 12182$, nên 44950 mod 16384 = 12182"],
                  ["④ băm kiểm lỗi CRC16", "hàm đổi một chuỗi byte thành một số 16 bit, từ 0 tới 65535; cùng chuỗi luôn ra cùng số", "CRC16 của <code>foo</code> = 44950"],
                  ["⑤ mã truy cập và mã giao dịch", "mã truy cập (JWT) ghi sẵn hạn dùng <code>exp</code> và số riêng <code>jti</code>; mã giao dịch là số riêng của một yêu cầu chuyển tiền", "<code>jti-7f3a</code>; <code>TX1001</code>"]]),
           """Trước hết ta cần hiểu năm điều. Thứ nhất, Redis là một kho khoá và giá trị chạy trong bộ nhớ, mỗi lệnh chạy trọn vẹn, không lệnh nào chen vào giữa.
           Thứ hai, mỗi mục có thể kèm một hạn sống tính bằng giây, hết hạn thì Redis tự xoá mục đó.
           Thứ ba, chia lấy dư là lấy phần còn lại sau khi chia hết số lần nguyên, ví dụ ở cột bên phải cho số dư mười hai nghìn một trăm tám mươi hai.
           Thứ tư, phép băm kiểm lỗi mười sáu bit đổi một chuỗi byte thành một số từ không tới sáu mươi lăm nghìn năm trăm ba mươi lăm, cùng chuỗi luôn ra cùng số.
           Thứ năm, mã truy cập ghi sẵn hạn dùng và một số riêng của nó, còn mã giao dịch là số riêng của một yêu cầu chuyển tiền.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st("""<p>Làm thử phép chia lấy dư:</p>
$$2 \\cdot 16384 = 32768, \\qquad 44950 - 32768 = \\hl{12182}$$""",
           """Làm thử ngay phép chia lấy dư. Hai lần mười sáu nghìn ba trăm tám mươi tư là ba mươi hai nghìn bảy trăm sáu mươi tám.
           Vì bốn mươi tư nghìn chín trăm năm mươi trừ đi số đó còn mười hai nghìn một trăm tám mươi hai, nên đó chính là số dư.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950", "44950 == 2 * 16384 + 12182", "alg.bnx_l19_crc16('foo') % 16384 == 12182",
               "2 * 16384 == 32768 and alg.bnx_l19_crc16('foo') - 32768 == 12182", "alg.bnx_l19_crc16(bytes([255]) * 4) <= 65535",
               "alg.bnx_l19_set_nx_ex([0, 59, 60], 60) == ['OK', None, 'OK']"])

    sym = sc("sym", "symbol", "Giải mã các từ trên màn hình", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["Redis Cluster, hash slot", "cụm nhiều nút Redis; không gian khoá chia thành <b>16384 khe băm</b>, đánh số 0 tới 16383"],
                  ["<code>CLUSTER KEYSLOT k</code>", "hỏi Redis: khoá <code>k</code> thuộc khe số mấy"],
                  ["<code>MOVED 12182 127.0.0.1:7002</code>", "lỗi chuyển hướng: “khe 12182 do nút ở cổng 7002 giữ, hãy gửi lại sang đó”"],
                  ["hash tag <code>{…}</code>", "thẻ băm: khoá có <code>{abc}</code> thì chỉ phần <code>abc</code> được đem băm; ngoặc rỗng <code>{}</code> thì băm cả khoá"],
                  ["<code>SET k v NX EX 300</code>", "<b>NX</b>: chỉ đặt khi khoá chưa có; <b>EX 300</b>: hạn sống 300 giây; đặt được trả <code>OK</code>, không đặt được trả <code>(nil)</code>"],
                  ["<code>TTL k</code>", "số giây còn lại của khoá; −2 nếu khoá không tồn tại, −1 nếu khoá không có hạn"],
                  ["<code>DELEX k IFEQ v</code>", "xoá khoá <b>chỉ khi</b> giá trị đang lưu đúng bằng <code>v</code> (có từ Redis 8.4)"]]),
           """Bảng này giải mã các từ sẽ hiện trên màn hình. Cụm Redis chia không gian khoá thành mười sáu nghìn ba trăm tám mươi tư khe băm.
           Lệnh thứ hai hỏi Redis xem một khoá thuộc khe số mấy.
           Lỗi chuyển hướng là câu trả lời của một nút không giữ khe đó, kèm địa chỉ nút đang giữ để máy khách gửi lại.
           Thẻ băm là phần nằm trong ngoặc nhọn của khoá, khi có thẻ băm thì chỉ phần đó được đem băm, còn ngoặc rỗng thì băm cả khoá.
           Lệnh đặt có hai tuỳ chọn: chỉ đặt khi khoá chưa có, và kèm hạn sống tính bằng giây, đặt được thì trả chữ ô kê, không được thì trả rỗng.
           Lệnh kế tiếp cho biết số giây còn lại, trả âm 2 nếu khoá không tồn tại và âm 1 nếu khoá không có hạn.
           Lệnh cuối chỉ xoá khoá khi giá trị đang lưu đúng bằng giá trị ta đưa vào.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
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
           """Hình cho thấy đường đi từ một khoá tới một nút. Khoá mẫu đi qua phép băm kiểm lỗi, ra số bốn mươi tư nghìn chín trăm năm mươi.
           Lấy dư cho mười sáu nghìn ba trăm tám mươi tư thì được khe mười hai nghìn một trăm tám mươi hai.
           Ba nút chia nhau ba dải khe liền nhau, và khe này rơi vào dải của nút thứ ba.
           Máy khách tự tính khe, còn nút nào giữ khe thì hỏi cụm hoặc theo lỗi chuyển hướng, nên cụm không cần máy trung gian chỉ đường."""),
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
           """Hình thứ hai cho thấy một mục có hạn sáu mươi giây. Ở giây không, yêu cầu tới lần đầu, đặt được mục nên được xử lý.
           Ở giây ba mươi, yêu cầu gửi lại gặp mục còn sống nên bị từ chối.
           Tới giây sáu mươi mốt mục đã tự xoá, nên yêu cầu gửi lại được nhận như một yêu cầu mới.
           Vậy một mục có hạn chỉ nhớ trong đúng khoảng hạn của nó, và đây vừa là điểm mạnh vừa là chỗ hở."""),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950 and alg.bnx_l19_slot('foo') == 12182",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]", "alg.bnx_l19_node_of_key('foo') == 3",
               "alg.bnx_l19_set_nx_ex([0, 30, 61], 60) == ['OK', None, 'OK']"])

    form = sc("formula", "formula", "Suy ra từng bước: từ một nút tới cụm, từ một lệnh tới ba cách dùng", [
        st("""<p><b>Bước 1.</b> Một nút không đủ bộ nhớ thì thêm nút. Mọi máy khách phải <b>tính giống nhau</b> khoá nào ở đâu, nên dùng một công thức cố định:</p>
$$\\text{khe} = \\text{CRC16}(\\text{khoá}) \\text{ mod } 16384$$
<span class='note'>Làm thử: CRC16(foo) = 44950; 44950 mod 16384 = 12182.</span>""",
           """Bước một, khi một nút không đủ bộ nhớ thì ta thêm nút. Vì mọi máy khách phải tính giống nhau khoá nào nằm ở đâu, nên cụm dùng một công thức cố định.
           Khe bằng kết quả băm kiểm lỗi của khoá, chia lấy dư cho mười sáu nghìn ba trăm tám mươi tư.
           Làm thử với khoá mẫu, ta được khe mười hai nghìn một trăm tám mươi hai.""", clear=True),
        st("""<p><b>Bước 2.</b> Nút giữ <b>dải khe</b>, không giữ từng khoá, vì thêm bớt nút chỉ cần chuyển khe. Ba nút: $16384 = 3 \\cdot 5461 + 1$, công cụ tạo cụm chia
<b>0–5460</b>, <b>5461–10922</b>, <b>10923–16383</b> (nút giữa nhận khe dư).</p>
<span class='note'>Làm thử: 12182 ≥ 10923 nên khoá foo ở nút thứ ba; hỏi nhầm nút thì nhận lỗi <code>MOVED</code>.</span>""",
           """Bước hai, mỗi nút giữ một dải khe chứ không giữ từng khoá, vì khi thêm bớt nút ta chỉ cần chuyển khe.
           Mười sáu nghìn ba trăm tám mươi tư chia ba được năm nghìn bốn trăm sáu mươi mốt, dư một, nên ba dải gần bằng nhau, nút giữa nhận khe dư.
           Làm thử, khe của khoá mẫu lớn hơn mười nghìn chín trăm hai mươi ba nên nằm ở nút thứ ba, hỏi nhầm nút thì nhận lỗi chuyển hướng."""),
        st("""<p><b>Bước 3.</b> Một lệnh đụng <b>nhiều khoá</b> chỉ chạy khi các khoá <b>cùng một khe</b>, vì mỗi nút chỉ thấy dữ liệu của mình.
Muốn ép cùng khe thì dùng thẻ băm: chỉ phần trong <code>{…}</code> được băm (ngoặc rỗng thì băm cả khoá).</p>
<span class='note'>Làm thử: <code>acc:1</code> ở khe 16276, <code>acc:2</code> ở khe 4087: khác khe. <code>{acc}:1</code> và <code>{acc}:2</code> cùng băm chữ <code>acc</code>: cùng khe 12007.</span>""",
           """Bước ba, một lệnh đụng nhiều khoá chỉ chạy được khi các khoá cùng một khe, vì mỗi nút chỉ thấy dữ liệu của riêng nó.
           Muốn ép cùng khe thì dùng thẻ băm, khi đó chỉ phần trong ngoặc nhọn được đem băm, còn ngoặc rỗng thì băm cả khoá.
           Làm thử, hai khoá tài khoản một và hai rơi vào hai khe khác nhau, còn khi bọc chung một thẻ băm thì cả hai cùng về khe mười hai nghìn không trăm linh bảy.""", clear=True),
        st("""<p><b>Bước 4.</b> Khoá giữ quyền: <code>SET loan:disb:A1001 may-a NX EX 300</code>.</p>
<ul><li><b>NX</b> gộp “kiểm rồi đặt” thành một lệnh, vì tách hai lệnh thì hai máy cùng thấy “chưa có”.</li>
<li><b>EX 300</b> vì máy giữ khoá có thể chết: sau 300 giây khoá tự nhả.</li>
<li>Giá trị <code>may-a</code> là <b>mã chủ khoá</b>: khi nhả, chỉ xoá nếu giá trị còn là của mình.</li></ul>
<span class='note'>Làm thử: máy B gửi cùng lệnh trong 300 giây đó thì nhận <code>(nil)</code>.</span>""",
           """Bước bốn là khoá giữ quyền, dùng lệnh đặt chỉ khi chưa có, kèm hạn ba trăm giây.
           Tuỳ chọn thứ nhất gộp việc kiểm rồi đặt thành một lệnh, vì nếu tách làm hai thì hai máy cùng thấy chưa có và cùng đặt.
           Tuỳ chọn thứ hai cần có vì máy giữ khoá có thể chết, khi đó sau ba trăm giây khoá tự nhả.
           Giá trị của khoá là mã chủ khoá, vì khi nhả ta chỉ được xoá nếu khoá vẫn còn là của mình.
           Làm thử, máy B gửi cùng lệnh trong ba trăm giây đó thì nhận câu trả lời rỗng."""),
        st("""<p><b>Bước 5.</b> Cùng một lệnh, đổi tên khoá là ra hai cách dùng nữa, vì cả hai đều là “nhớ một điều trong một khoảng thời gian”.</p>
<ul><li><b>Khử trùng</b>: khoá = mã giao dịch, hạn 60 giây. Đặt được thì xử lý; nhận <code>(nil)</code> thì đó là yêu cầu gửi lại.</li>
<li><b>Danh sách đen</b>: khoá = số riêng <code>jti</code> của mã truy cập bị thu hồi; hạn = thời gian còn lại của mã, vì sau đó mã tự hết hạn.</li></ul>
$$\\text{hạn mục danh sách đen} = \\text{exp} - \\text{bây giờ} = 300 - 60 = \\hl{240}\\ \\text{giây (số minh hoạ)}$$""",
           """Bước năm, cùng một lệnh mà đổi tên khoá là ra hai cách dùng nữa, vì cả hai đều là nhớ một điều trong một khoảng thời gian.
           Với khử trùng, khoá là mã giao dịch, hạn sáu mươi giây, đặt được thì xử lý, còn nhận trả lời rỗng thì đó là yêu cầu gửi lại.
           Với danh sách đen, khoá là số riêng của mã truy cập bị thu hồi, và hạn bằng thời gian còn lại của mã, vì sau đó mã tự hết hạn.
           Làm thử bằng số minh hoạ, mã có hạn dùng ba trăm giây, bị thu hồi ở giây sáu mươi, nên mục danh sách đen đặt hạn hai trăm bốn mươi giây.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('foo') == 44950 and alg.bnx_l19_slot('foo') == 12182",
               "16384 == 3 * 5461 + 1 and alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]",
               "alg.bnx_l19_node(12182) == 3 and 12182 >= 10923",
               "alg.bnx_l19_slot('acc:1') == 16276 and alg.bnx_l19_slot('acc:2') == 4087",
               "alg.bnx_l19_slot('{acc}:1') == alg.bnx_l19_slot('{acc}:2') == 12007 and alg.bnx_l19_same_slot('{acc}:1', '{acc}:2')",
               "alg.bnx_l19_set_nx_ex([0, 100], 300) == ['OK', None]", "alg.bnx_l19_set_nx_ex([0, 30], 60) == ['OK', None]",
               "alg.bnx_l19_bl_ttl(300, 60) == 240"])

    ex = sc("example", "example", "Ví dụ chạy thật trên Redis 8.10.3, từng phép tính", [
        st(code(PY_CRC, "Tự tính khe băm bằng Python (không cần Redis)"),
           """Trước hết ta tự tính khe băm bằng Python, chưa cần tới Redis. Hàm ở trên là phép băm kiểm lỗi mười sáu bit, đi qua từng byte và từng bit của khoá.
           Hai dòng kế tiếp in kết quả băm của một chuỗi thử chuẩn, rồi kết quả băm của khoá mẫu và số dư khi chia cho mười sáu nghìn ba trăm tám mươi tư.
           Hai dòng cuối in ba dải khe, mỗi dải bắt đầu ở một khe và dài năm nghìn bốn trăm sáu mươi mốt hoặc sáu mươi hai khe.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_CRC),
           """Kết quả chạy thật. Chuỗi thử chuẩn ra ba một C ba ở hệ mười sáu, đúng con số ghi trong đặc tả cụm Redis, nên hàm băm của ta đúng.
           Khoá mẫu ra bốn mươi tư nghìn chín trăm năm mươi, và khe là mười hai nghìn một trăm tám mươi hai.""", clear=True),
        st("""$$① \\; 44950 \\text{ mod } 16384 = 44950 - 2 \\cdot 16384 = \\hl{12182}$$
$$② \\; 16384 = 3 \\cdot 5461 + 1: \\; \\text{0–5460},\\ \\text{5461–10922},\\ \\text{10923–16383}; \\quad 10923 \\le 12182 \\Rightarrow \\hlg{\\text{nút thứ ba}}$$""",
           """Phép tính thứ nhất, bốn mươi tư nghìn chín trăm năm mươi trừ hai lần mười sáu nghìn ba trăm tám mươi tư còn mười hai nghìn một trăm tám mươi hai.
           Phép tính thứ hai dùng lại khe đó. Vì nó nằm trong dải từ mười nghìn chín trăm hai mươi ba tới mười sáu nghìn ba trăm tám mươi ba, nên khoá mẫu thuộc nút thứ ba.""", clear=True),
        st(code(SH_START, "Dựng cụm ba nút thật (thu nhỏ: ba tiến trình Redis trong một container Docker)"),
           """Bây giờ ta dựng một cụm thật bằng Docker. Đây là bản thu nhỏ để học: ba tiến trình Redis chạy chung một hộp chứa, ở ba cổng, còn cụm vận hành thật đặt mỗi nút trên một máy riêng.
           Hai lệnh đầu xoá hộp chứa cũ rồi chạy nút thứ nhất ở cổng bảy nghìn, có bật chế độ cụm.
           Vòng lặp chạy thêm hai nút ở cổng bảy nghìn không trăm linh một và linh hai.
           Lệnh tạo cụm chia khe cho ba nút, ta chỉ giữ lại các dòng nói về khe.
           Hai dòng cuối định nghĩa lệnh tắt r để gửi lệnh tới nút thứ nhất, rồi chờ cụm sẵn sàng.""",
           focus=[1, 1, 2, 2, 2, 2], clear=True),
        st(out(OUT_START),
           """Kết quả chạy thật của công cụ tạo cụm. Ba nút nhận đúng ba dải khe ta vừa tính bằng tay, và dòng cuối xác nhận cả mười sáu nghìn ba trăm tám mươi tư khe đã có chủ.""", clear=True),
        st(code(SH_SLOT, "Hỏi Redis thật: khoá foo ở khe nào, nút nào"),
           """Ta hỏi Redis thật bốn lệnh. Lệnh một hỏi khe của khoá mẫu. Lệnh hai đặt giá trị cho khoá đó, nhưng gửi tới nút thứ nhất, là nút không giữ khe này.
           Lệnh ba và lệnh bốn thêm tuỳ chọn chế độ cụm, để công cụ tự đi theo lời chuyển hướng.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_SLOT),
           """Kết quả chạy thật. Redis trả đúng khe mười hai nghìn một trăm tám mươi hai, khớp con số ta tự tính.
           Nút thứ nhất từ chối và báo lỗi chuyển hướng, chỉ sang cổng bảy nghìn không trăm linh hai, tức nút thứ ba.
           Khi bật chế độ cụm, công cụ tự gửi lại sang đó, nên lệnh đặt thành công và lệnh đọc trả về giá trị đã đặt."""),
        st(code(SH_LOCK, "Khoá giải ngân hồ sơ A1001: hai máy tranh nhau"),
           """Tiếp theo là khoá giải ngân của hồ sơ A một không không một, gửi liền sáu lệnh trong một phiên.
           Máy A đặt khoá với mã chủ khoá của mình, hạn ba trăm giây. Máy B gửi cùng lệnh với mã của B. Lệnh ba xem hạn còn lại.
           Lệnh bốn là máy B thử nhả khoá bằng mã của B, lệnh năm là máy A nhả bằng mã của A. Lệnh cuối, máy B xin khoá lần nữa.""",
           clear=True),
        st(out(OUT_LOCK),
           """Kết quả chạy thật, đúng thứ tự. Máy A đặt được khoá. Máy B nhận trả lời rỗng, tức không được làm. Hạn còn lại là ba trăm giây.
           Máy B không xoá được khoá vì sai mã chủ khoá, kết quả là không. Máy A xoá được, kết quả là một. Sau đó máy B mới lấy được khoá.""", clear=True),
        st("""$$③ \\; \\text{khoá hạn } 300 \\text{ giây, máy A làm xong ở giây } 120: \\; 300 - 120 = \\hlg{180}\\ \\text{giây dư, A tự nhả sớm (số minh hoạ)}$$""",
           """Phép tính thứ ba, bằng số minh hoạ. Khoá có hạn ba trăm giây, máy A giải ngân xong ở giây một trăm hai mươi, nên còn dư một trăm tám mươi giây.
           Vì A nhả khoá ngay khi xong, hồ sơ không bị giữ thêm một trăm tám mươi giây vô ích.""", clear=True),
        st(code(SH_DEDUP, "Khử trùng mã giao dịch TX1001 và danh sách đen mã truy cập"),
           """Phiên tiếp theo gồm hai việc. Ba lệnh đầu là khử trùng: đặt mục cho mã giao dịch với hạn sáu mươi giây, gửi lại đúng lệnh đó, rồi xem hạn còn lại.
           Bốn lệnh sau là danh sách đen: ghi số riêng của mã truy cập bị thu hồi với hạn hai trăm bốn mươi giây, xem hạn.
           Sau đó hỏi xem mã bị thu hồi và một mã khác có nằm trong danh sách không.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_DEDUP),
           """Kết quả chạy thật. Dòng có mũi tên là công cụ tự chuyển sang nút giữ khe của khoá. Lần đặt đầu thành công, lần gửi lại nhận trả lời rỗng, và hạn còn sáu mươi giây.
           Mục danh sách đen đặt được, hạn hai trăm bốn mươi giây. Mã bị thu hồi có trong danh sách, kết quả là một, còn mã khác thì không có, kết quả là không.""", clear=True),
        st("""$$④ \\; \\text{hạn } 60: \\quad 30 < 60 \\Rightarrow \\hl{\\text{từ chối}}; \\qquad 61 \\ge 60 \\Rightarrow \\hlg{\\text{được nhận}}$$
$$⑤ \\; \\text{mã truy cập còn } 300 - 60 = \\hl{240}\\ \\text{giây} \\Rightarrow \\text{mục danh sách đen đặt hạn } 240 \\text{ giây}$$""",
           """Phép tính thứ tư, với hạn sáu mươi giây. Gửi lại ở giây ba mươi thì mục còn sống nên bị từ chối. Gửi lại ở giây sáu mươi mốt thì mục đã hết nên được nhận.
           Phép tính thứ năm dùng lại ý hạn sống. Mã truy cập còn hai trăm bốn mươi giây, nên mục danh sách đen cũng đặt hạn hai trăm bốn mươi giây, hết lúc đó thì cả hai cùng biến mất.""",
           clear=True),
        st(code(PY_SIM, "Giây 30 và giây 61: mô phỏng bằng đồng hồ giả (không phải Redis thật)"),
           """Để thấy giây ba mươi và giây sáu mươi mốt mà không phải ngồi chờ, ta dùng một mô phỏng nhỏ bằng Python với đồng hồ giả, đây không phải Redis thật.
           Kho nhớ thời điểm hết hạn của từng khoá. Hàm đặt từ chối khi khoá còn sống, ngược lại thì ghi hạn mới và trả chữ ô kê.
           Vòng lặp cuối vặn đồng hồ tới bốn thời điểm và gửi cùng một mã giao dịch.""",
           focus=[1, 2, 2, 2], clear=True),
        st(out(OUT_SIM),
           """Kết quả chạy thật của mô phỏng. Giây không được nhận. Giây ba mươi bị từ chối. Giây sáu mươi mốt được nhận như yêu cầu mới.
           Giây sáu mươi hai lại bị từ chối, vì lần nhận ở giây sáu mươi mốt đã mở một khoảng sáu mươi giây mới.""", clear=True),
    ], checks=["alg.bnx_l19_crc16('123456789') == 0x31C3", "alg.bnx_l19_crc16('foo') == 44950 and 44950 - 2 * 16384 == 12182",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)] and alg.bnx_l19_node(12182) == 3",
               "[b - a + 1 for a, b in alg.bnx_l19_ranges()] == [5461, 5462, 5461]",
               "alg.bnx_l19_set_nx_ex([0, 0], 300) == ['OK', None]", "alg.bnx_l19_lock_story(300, 120) == (1, 1) and 300 - 120 == 180",
               "alg.bnx_l19_slot('dedup:TX1001') == 9306 and alg.bnx_l19_node(9306) == 2",
               "alg.bnx_l19_slot('bl:jti-0000') == 1074 and alg.bnx_l19_node(1074) == 1",
               "alg.bnx_l19_set_nx_ex([0, 30, 61, 62], 60) == ['OK', None, 'OK', None]", "alg.bnx_l19_bl_ttl(300, 60) == 240"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: Redis thật với hạn thu nhỏ, và thẻ băm", [
        st(code(SH_SHORT, "Đường khác cho phép ④: Redis thật, hạn thu nhỏ còn 2 giây"),
           """Mô phỏng có thể sai, nên ta kiểm phép tính thứ tư bằng Redis thật, với hạn thu nhỏ từ sáu mươi giây xuống hai giây.
           Cùng một lệnh đặt được gửi ba lần: ngay lúc đầu, sau một giây, rồi sau thêm hai giây nữa, tức ở giây thứ ba.""",
           focus=[1, 2], clear=True),
        st(out(OUT_SHORT),
           """Kết quả chạy thật. Lần đầu được nhận. Lần gửi lại ở giây một nhận trả lời rỗng, vì mục còn trong hạn. Lần gửi ở giây ba lại được nhận, vì đã quá hạn hai giây.
           Redis thật cư xử đúng như mô phỏng, chỉ khác tỉ lệ thời gian."""),
        st(code(SH_MULTI, "Đường khác cho bước 3: lệnh nhiều khoá trên cụm thật"),
           """Ta kiểm tiếp bước ba trên cụm thật. Lệnh đầu đặt hai khoá tài khoản trong một lệnh, nên Redis phải xét khe của cả hai. Hai lệnh sau hỏi khe của từng khoá.
           Lệnh bốn đặt hai khoá có chung thẻ băm, và lệnh cuối hỏi khe của khoá có thẻ băm.""",
           clear=True),
        st(out(OUT_MULTI),
           """Kết quả chạy thật. Lệnh đầu bị từ chối với lỗi các khoá không cùng khe, vì hai khoá nằm ở khe mười sáu nghìn hai trăm bảy mươi sáu và bốn nghìn không trăm tám mươi bảy.
           Khi có chung thẻ băm, lệnh chạy được ở nút thứ ba, và khe là mười hai nghìn không trăm linh bảy.""", clear=True),
        st(table(["đại lượng", "tự tính bằng Python", "Redis 8.10.3 thật"],
                 [["khe của <code>foo</code>", "12182", "12182"],
                  ["ba dải khe", "0–5460, 5461–10922, 10923–16383", "0–5460, 5461–10922, 10923–16383"],
                  ["khe của <code>dedup:TX1001</code>", "9306 (nút 2)", "9306, cổng 7001"],
                  ["khe của <code>{acc}:1</code>", "12007", "12007"],
                  ["gửi lại trong hạn / sau hạn", "từ chối / nhận (đồng hồ giả, hạn 60)", "(nil) / OK (hạn 2 giây)"]]),
           """Bảng này đặt hai đường cạnh nhau. Cột giữa là số ta tự tính bằng Python, cột phải là số Redis thật trả về.
           Khe của khoá mẫu, ba dải khe, khe của mã giao dịch và khe của khoá có thẻ băm đều khớp từng số.
           Hành vi gửi lại trong hạn và sau hạn cũng khớp, nên ta tin các phép tính ở trên.""", clear=True),
    ], checks=["alg.bnx_l19_set_nx_ex([0, 1, 3], 2) == ['OK', None, 'OK']",
               "alg.bnx_l19_slot('acc:1') == 16276 and alg.bnx_l19_slot('acc:2') == 4087 and not alg.bnx_l19_same_slot('acc:1', 'acc:2')",
               "alg.bnx_l19_slot('{acc}:1') == 12007 and alg.bnx_l19_node(12007) == 3",
               "alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_slot('dedup:TX1001') == 9306 and alg.bnx_l19_node(9306) == 2",
               "alg.bnx_l19_ranges() == [(0, 5460), (5461, 10922), (10923, 16383)]"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp theo thời gian: lúc mới dựng, lúc tải tăng, lúc vận hành lâu", [
        st("""<div class="box warn"><b>Lỗi 1 (lúc mới dựng).</b> Nhả khoá bằng <code>DEL</code> thẳng, hoặc đặt giá trị khoá là số <code>1</code> cho mọi máy.
Máy A quá hạn, máy B đã lấy khoá, rồi A chạy tới dòng nhả và <b class="red">xoá mất khoá của B</b>.
<br><span class="note">Cách chữa: giá trị là mã chủ khoá ngẫu nhiên; nhả bằng lệnh “chỉ xoá nếu giá trị còn là của tôi” (<code>DELEX … IFEQ</code>; bản Redis cũ hơn 8.4 dùng một đoạn kịch bản nhỏ so rồi xoá).</span></div>""",
           """Lỗi thứ nhất gặp ngay lúc mới dựng, là nhả khoá bằng lệnh xoá thẳng, hoặc đặt giá trị khoá giống nhau cho mọi máy.
           Khi đó máy A quá hạn, máy B đã lấy khoá, rồi A chạy tới dòng nhả và xoá mất khoá của B.
           Cách chữa là dùng mã chủ khoá ngẫu nhiên, và nhả bằng lệnh chỉ xoá khi giá trị còn là của mình.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (lúc tải tăng, chuyển từ một nút sang cụm).</b> Mã đang chạy tốt trên một nút bỗng báo
<code class="red">CROSSSLOT</code>, vì lệnh nhiều khoá chỉ chạy trong cụm khi các khoá <b>cùng một khe băm</b>.
Chữa vội bằng cách gắn <b>cùng một thẻ băm cho mọi khoá</b> thì mọi khoá dồn về một nút, cụm mất tác dụng.
<br><span class="note">Cách chữa: thẻ băm theo từng đối tượng, ví dụ theo mã hồ sơ. Chú ý: viết nguyên <code>loan:disb:{A1001}</code> thì Redis chỉ băm chữ <code>A1001</code> (khe 1830, khác khe 5075 của <code>loan:disb:A1001</code>).</span></div>""",
           """Lỗi thứ hai xuất hiện lúc tải tăng, khi chuyển từ một nút sang cụm. Mã đang chạy tốt bỗng báo lỗi các khoá không cùng khe, vì lệnh nhiều khoá chỉ chạy trong cụm khi các khoá cùng một khe băm.
           Nếu chữa vội bằng cách gắn cùng một thẻ băm cho mọi khoá, thì mọi khoá dồn về một nút, và cụm mất tác dụng.
           Cách chữa là đặt thẻ băm theo từng đối tượng, ví dụ theo mã hồ sơ.
           Cũng cần nhớ rằng cặp ngoặc nhọn viết trong tên khoá sẽ được hiểu là thẻ băm, nên khe của khoá đổi theo.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Tin rằng khoá Redis có hạn là <b>loại trừ tuyệt đối</b>.
Khoá hạn 300 giây, tiến trình A bị dừng tới giây 320 (thu gom rác, máy ảo bị treo, gọi lõi ngân hàng chậm): quá hạn 320 − 300 = <b class="red">20 giây</b>,
B đã lấy khoá, và <b>cả hai cùng giải ngân</b>.
<br><span class="note">Cách chữa: khoá chỉ để giảm tranh chấp; lớp chặn cuối nằm ở cơ sở dữ liệu (ràng buộc duy nhất theo mã hồ sơ, hoặc đổi trạng thái có điều kiện).</span></div>""",
           """Lỗi thứ ba là của người đã đi làm, lộ ra khi vận hành lâu dài: tin rằng khoá Redis có hạn là loại trừ tuyệt đối.
           Khoá có hạn ba trăm giây, nhưng tiến trình A bị dừng tới giây ba trăm hai mươi, do thu gom rác, máy ảo bị treo, hay lõi ngân hàng trả lời chậm.
           Vì đã quá hạn hai mươi giây, máy B lấy được khoá, và cả hai cùng giải ngân.
           Cách chữa là coi khoá chỉ để giảm tranh chấp, còn lớp chặn cuối nằm ở cơ sở dữ liệu, bằng ràng buộc duy nhất theo mã hồ sơ.""", clear=True),
        st("<p><b>Lỗi 3 (phần tiếp, lúc vận hành lâu dài).</b> Hai nguy cơ nữa của khoá Redis có hạn:</p>"
           + table(["nguy cơ", "điều xảy ra", "cách chữa"],
                   [["nút chính hỏng", "mỗi nút chính thường có <b>nút bản sao</b>, chép dữ liệu theo kiểu không chờ bản sao xác nhận; nút chính hỏng trước khi bản sao nhận khoá, bản sao lên thay: B lấy được khoá khi A vẫn tin mình giữ",
                     "khoá chỉ để giảm tranh chấp; lớp chặn cuối ở cơ sở dữ liệu"],
                    ["bộ nhớ đầy", "đã đặt giới hạn bộ nhớ thì chính sách đẩy khoá có thể xoá khoá giữ quyền và mục danh sách đen còn hạn; nhóm chỉ đẩy khoá có hạn (volatile) vẫn đẩy được vì khoá của bài đều có hạn; chính sách không đẩy thì lệnh ghi mới báo lỗi",
                     "chừa chỗ, theo dõi số khoá bị đẩy; quyết định trước khi Redis lỗi hay đầy thì từ chối hay cho qua"],
                    ["khoá chưa đủ an toàn", "bài hướng dẫn khoá phân tán của nhóm làm Redis nêu <b>mã hàng rào</b> (fencing token) tăng dần, kiểm ở nơi ghi",
                     "bài chọn ràng buộc duy nhất ở cơ sở dữ liệu làm lớp cuối"]]),
           """Lỗi thứ ba còn hai nguy cơ nữa. Thứ nhất là nút chính hỏng: mỗi nút chính thường có nút bản sao, chép dữ liệu theo kiểu không chờ bản sao xác nhận.
           Nếu nút chính hỏng trước khi bản sao nhận khoá, rồi bản sao lên thay, thì máy B lấy được khoá trong lúc máy A vẫn tin mình giữ.
           Thứ hai là bộ nhớ đầy: khi đã đặt giới hạn, chính sách đẩy khoá có thể xoá cả khoá giữ quyền lẫn mục danh sách đen còn hạn.
           Nhóm chính sách chỉ đẩy khoá có hạn cũng không cứu được, vì khoá của bài đều có hạn. Chính sách không đẩy khoá thì lệnh ghi mới báo lỗi.
           Cách chữa là chừa chỗ, theo dõi số khoá bị đẩy, và quyết định trước khi Redis lỗi hay đầy thì từ chối hay cho qua.
           Bài hướng dẫn khoá phân tán của nhóm làm Redis còn nêu mã hàng rào tăng dần, kiểm ở nơi ghi, còn bài chọn ràng buộc ở cơ sở dữ liệu.""",
           focus=[1, "2.2", "2.2", "2.3", "2.3", "2.3", "2.3", "2.4"], clear=True),
        st("<p><b>Lỗi 4 (người đã đi làm, lúc đối tác đổi cách thử lại).</b> Hạn khử trùng ngắn hơn thời gian thử lại của bên gửi <i>(số minh hoạ)</i>.</p>"
           + table(["bên gửi thử lại ở giây", "hạn khử trùng 60 giây", "hạn khử trùng 120 giây"],
                   [["30", "30 &lt; 60: từ chối", "30 &lt; 120: từ chối"],
                    ["90", "90 ≥ 60: mục đã hết, <b class='red'>xử lý lần hai</b>", "90 &lt; 120: từ chối"]])
           + "<p class='note'>Cách chữa: hạn dài hơn khoảng thử lại dài nhất của bên gửi; và vẫn giữ ràng buộc duy nhất theo mã giao dịch ở cơ sở dữ liệu.</p>",
           """Lỗi thứ tư cũng của người đã đi làm, lộ ra khi đối tác đổi cách thử lại: hạn khử trùng ngắn hơn thời gian thử lại của bên gửi.
           Với số minh hoạ trong bảng, hạn sáu mươi giây mà bên gửi thử lại ở giây chín mươi, lúc đó mục đã hết nên yêu cầu được xử lý hai lần.
           Cách chữa là đặt hạn dài hơn khoảng thử lại dài nhất của bên gửi, và vẫn giữ ràng buộc duy nhất theo mã giao dịch ở cơ sở dữ liệu.""",
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
           """Đến lượt bạn. Câu một, kết quả băm của một khoá là năm mươi nghìn không trăm mười tám, hỏi khoá ở khe nào và nút nào trong cụm ba nút?
           Câu hai, mã giao dịch đặt hạn sáu mươi giây ở giây không, bên gửi gửi lại ở giây bốn mươi lăm và giây bảy mươi lăm, mỗi lần được nhận hay bị từ chối?
           Cũng trong câu hai, mã truy cập hạn chín trăm giây bị thu hồi ở giây hai trăm năm mươi, mục danh sách đen đặt hạn bao nhiêu?
           Câu ba, để chống giải ngân hai lần, bạn chọn chỉ khoá Redis, chỉ ràng buộc ở cơ sở dữ liệu, hay cả hai? Hãy dừng video lại và làm từng câu ra giấy trước khi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.3", "1.4", "1.4"], pause=25),
        st("""<p>Câu 1: $3 \\cdot 16384 = 49152$.</p>
$$50018 - 49152 = \\hlg{866}; \\qquad 0 \\le 866 \\le 5460 \\Rightarrow \\hlg{\\text{nút thứ nhất}}$$""",
           """Đáp án câu một. Ba lần mười sáu nghìn ba trăm tám mươi tư là bốn mươi chín nghìn một trăm năm mươi hai.
           Vì năm mươi nghìn không trăm mười tám trừ đi số đó còn tám trăm sáu mươi sáu, nên khoá ở khe tám trăm sáu mươi sáu, thuộc dải của nút thứ nhất."""),
        st("""<p>Câu 2:</p>
$$45 < 60 \\Rightarrow \\hl{\\text{từ chối}}; \\qquad 75 \\ge 60 \\Rightarrow \\hlg{\\text{được nhận}}; \\qquad 900 - 250 = \\hlg{650}\\ \\text{giây}$$""",
           """Đáp án câu hai. Giây bốn mươi lăm còn trong hạn sáu mươi giây nên bị từ chối. Giây bảy mươi lăm đã quá hạn nên được nhận như yêu cầu mới.
           Mã truy cập còn chín trăm trừ hai trăm năm mươi, bằng sáu trăm năm mươi giây, nên mục danh sách đen đặt hạn sáu trăm năm mươi giây."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["(a) chỉ khoá Redis hạn 300 giây", "nhanh; chặn sớm phần lớn lần bấm trùng", "tiến trình dừng quá 300 giây, hoặc nút chính hỏng trước khi nút bản sao kịp nhận khoá (xem lỗi 3, phần tiếp), thì vẫn giải ngân hai lần"],
                  ["(b) chỉ ràng buộc duy nhất ở cơ sở dữ liệu", "đúng tuyệt đối: lần ghi thứ hai bị từ chối", "cả hai máy cùng gọi lõi ngân hàng rồi mới biết trùng; tốn tải, phải hoàn tác"],
                  ["(c) khoá Redis + ràng buộc duy nhất", "khoá chặn sớm, cơ sở dữ liệu bảo đảm đúng", "thêm một hệ phải vận hành; phải quyết định làm gì khi Redis hỏng"]]),
           """Đáp án câu ba. Chỉ khoá Redis thì nhanh và chặn sớm, nhưng tiến trình dừng quá hạn, hoặc nút chính hỏng trước khi bản sao kịp nhận khoá, thì vẫn giải ngân hai lần.
           Chỉ ràng buộc ở cơ sở dữ liệu thì đúng tuyệt đối, nhưng cả hai máy cùng gọi lõi ngân hàng rồi mới biết trùng, tốn tải và phải hoàn tác.
           Dùng cả hai thì khoá chặn sớm, cơ sở dữ liệu bảo đảm đúng, đổi lại thêm một hệ phải vận hành, và phải quyết định làm gì khi Redis hỏng.""",
           focus=["1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l19_crc16('hello') == 50018", "3 * 16384 == 49152 and 50018 - 49152 == 866 == alg.bnx_l19_slot('hello')",
               "alg.bnx_l19_node(866) == 1", "alg.bnx_l19_set_nx_ex([0, 45], 60) == ['OK', None]",
               "alg.bnx_l19_set_nx_ex([0, 75], 60) == ['OK', 'OK']", "alg.bnx_l19_bl_ttl(900, 250) == 650",
               "alg.bnx_l19_lock_story(300, 301)[0] == 2"])

    rec = sc("recap", "recap", "Chuỗi logic, tư duy, và góc phỏng vấn theo CV", [
        st(chain("khe = CRC16(khoá) mod 16384", "nút giữ dải khe, sai nút thì MOVED", "SET NX EX + mã chủ khoá", "cùng lệnh: khử trùng, danh sách đen",
                 "lớp chặn cuối ở cơ sở dữ liệu"),
           """Tổng kết chuỗi logic. Khe của một khoá là kết quả băm kiểm lỗi chia lấy dư cho mười sáu nghìn ba trăm tám mươi tư. Mỗi nút giữ một dải khe, hỏi sai nút thì được chuyển hướng.
           Khoá giữ quyền là lệnh đặt chỉ khi chưa có, kèm hạn và mã chủ khoá. Cũng lệnh đó dùng để khử trùng và làm danh sách đen, còn lớp chặn cuối luôn nằm ở cơ sở dữ liệu."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["“Redis Cluster: một khoá nằm ở nút nào, và lệnh nhiều khoá thì sao?”", "khe = CRC16(khoá) mod 16384, nút giữ dải khe, sai nút trả MOVED; lệnh nhiều khoá cần cùng khe, ép bằng thẻ băm"],
                  ["“<code>SET loan:disb:{app_id} 1 NX EX 300</code> có bảo đảm chỉ giải ngân một lần không?”", "không tuyệt đối: tiến trình dừng quá 300 giây hoặc nút chính hỏng thì hai máy cùng làm; cần mã chủ khoá khi nhả và ràng buộc duy nhất ở cơ sở dữ liệu"],
                  ["“Vì sao hạn khử trùng 60 giây, và danh sách đen đặt hạn bao nhiêu?”", "hạn phải dài hơn khoảng thử lại của bên gửi; mục danh sách đen sống đúng bằng thời gian còn lại của mã truy cập"]]),
           """Đây là góc phỏng vấn theo hồ sơ xin việc, với ba câu hay gặp. Hỏi về cụm, hãy nói công thức khe, dải khe của nút, lỗi chuyển hướng, và thẻ băm cho lệnh nhiều khoá.
           Hỏi khoá giải ngân có bảo đảm một lần không, hãy nói không tuyệt đối, rồi nêu mã chủ khoá và ràng buộc duy nhất ở cơ sở dữ liệu, vì nút chính hỏng cũng mất khoá.
           Hỏi về các con số hạn, hãy nói hạn khử trùng phải dài hơn khoảng thử lại của bên gửi, còn mục danh sách đen sống đúng bằng thời gian còn lại của mã truy cập.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> mọi thứ có hạn trong Redis chỉ “nhớ” trong khoảng hạn đó. Trước khi tin nó, hãy hỏi:
<b>điều gì xảy ra ở giây ngay sau khi hết hạn?</b></div>""",
           """Điều cần mang theo. Mọi thứ có hạn trong Redis chỉ nhớ trong đúng khoảng hạn đó. Trước khi tin nó, hãy tự hỏi điều gì xảy ra ở giây ngay sau khi hết hạn."""),
    ], checks=["alg.bnx_l19_slot('foo') == 12182", "alg.bnx_l19_lock_story(300, 320)[0] == 2", "alg.bnx_l19_processed([0, 90], 60) == 2",
               "alg.bnx_l19_bl_ttl(300, 60) == 240"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L19", "redis_cum_khoa_khu_trung",
                  "Bài 19 — Redis nâng cao: cụm 16384 khe băm, khoá có hạn, khử trùng và danh sách đen",
                  "curriculum/bnx.yaml L19; audit/bnx/verify_bnx.py L19; Redis cluster specification, Scale with Redis Cluster, lệnh SET, TTL, EXPIRE, "
                  "Distributed Locks with Redis (redis.io, đọc 2026-11-11, audit/bnx/sources_l19.md); chạy thật Redis 8.10.3 trong Docker",
                  ["Tính khe băm của một khoá và chỉ ra nút giữ khe đó trong cụm ba nút",
                   "Giải thích lệnh đặt khoá chỉ khi chưa có, kèm hạn sống, và vì sao phải có mã chủ khoá",
                   "Khử trùng yêu cầu gửi lại bằng mã giao dịch có hạn 60 giây",
                   "Thu hồi một mã truy cập trước hạn bằng danh sách đen có hạn sống"],
                  scenes)
