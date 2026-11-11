import re

from lib import *

# ── Mã hiện trên màn hình (chạy nguyên văn: audit/bnx/screen/l09.yaml, audit/bnx/ver/l09.py) ──
KEY_PY = """
import zlib
key = "customer::C1001"
h = zlib.crc32(key.encode())
r = (h >> 16) & 0x7FFF          # như thư viện Java của hãng
print(h, "// 65536 =", h // 65536, "; mod 32768 =", r)
print("1024 thùng:", r % 1024, "| 128 thùng:", r % 128)
"""

STORE_PY = """
class Store:                      # kho một bản ghi, có CAS
    def __init__(self):
        self.doc, self.cas = {"diem_thuong": 100}, 7
    def get(self):
        return dict(self.doc), self.cas
    def replace(self, doc, cas):
        if cas != self.cas:
            return "từ chối: CAS lệch"
        self.doc, self.cas = doc, self.cas + 1
        return "ghi được, CAS mới = %d" % self.cas
"""

USE_PY = """
s = Store()
d1, c1 = s.get()                  # P1 đọc: CAS 7
d2, c2 = s.get()                  # P2 đọc: CAS 7
d1["diem_thuong"] += 50
print("P1:", s.replace(d1, c1))
d2["diem_thuong"] += 30
print("P2:", s.replace(d2, c2))
d2, c2 = s.get()                  # P2 đọc lại
d2["diem_thuong"] += 30
print("P2 lần 2:", s.replace(d2, c2))
print(s.get())
"""

INTER_PY = """
from itertools import permutations
def f(order, cas_on):
    v, ver, rd, add = 100, 7, {}, {"P1": 50, "P2": 30}
    for p in order:
        if p not in rd:                    # lần đầu: đọc
            rd[p] = (v, ver); continue
        old = rd[p][0] if not cas_on or rd[p][1] == ver else v
        v, ver = old + add[p], ver + 1     # ghi (lệch CAS: đọc lại)
    return v
od = set(permutations(["P1", "P1", "P2", "P2"]))
for c in (True, False):
    print(len(od), "thứ tự, CAS", c, sorted({f(o, c) for o in od}))
"""

# Đầu ra THẬT (.venv Python 3.13.5, 2026-11-11)
KEY_OUT = """
2170508415 // 65536 = 33119 ; mod 32768 = 351
1024 thùng: 351 | 128 thùng: 95
"""
USE_OUT = """
P1: ghi được, CAS mới = 8
P2: từ chối: CAS lệch
P2 lần 2: ghi được, CAS mới = 9
({'diem_thuong': 180}, 9)
"""
INTER_OUT = """
6 thứ tự, CAS True [180]
6 thứ tự, CAS False [130, 150, 180]
"""
KEY = "customer::C1001"


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


def build():
    hook = sc("hook", "hook", "Vì sao cộng điểm thưởng hai lần mà chỉ thấy một lần?", [
        stf("""<p>Hồ sơ khách hàng C1001 có $100$ điểm thưởng. Cùng một lúc, dịch vụ khuyến mãi cộng $50$ điểm, dịch vụ hoàn tiền cộng $30$ điểm (số minh hoạ).</p>
<p>Mong đợi: $100 + 50 + 30 = 180$. Hồ sơ ghi: <b class="red">130</b>.</p>
<div class="box key">Cả hai cùng đọc 100, mỗi bên tự cộng rồi ghi đè. Lần ghi sau xoá mất 50 điểm của lần ghi trước: <b>mất cập nhật</b>.</div>""",
            """[1] Chào bạn, hồ sơ khách hàng C một nghìn không trăm linh một có một trăm điểm thưởng. Cùng một lúc, dịch vụ khuyến mãi cộng năm mươi điểm, còn dịch vụ hoàn tiền cộng ba mươi điểm, đây là số minh hoạ.
            [2] Ta mong đợi một trăm cộng năm mươi cộng ba mươi, bằng một trăm tám mươi. Nhưng hồ sơ chỉ ghi một trăm ba mươi.
            [3] Lý do là cả hai cùng đọc một trăm, mỗi bên tự cộng rồi ghi đè. Lần ghi sau xoá mất năm mươi điểm của lần ghi trước, gọi là mất cập nhật."""),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["lưu hồ sơ khách hàng thế nào để lấy ra nhanh", "khoá bản ghi <code>customer::C1001</code>"],
                   ["khoá nằm ở máy nào trong cụm", "thùng ảo (vBucket) = băm khoá, rồi tra bản đồ cụm"],
                   ["làm sao không mất 50 điểm", "dấu phiên bản CAS: ghi kèm dấu đã đọc, lệch thì bị từ chối"],
                   ["phiên đăng nhập tự hết hạn thế nào", "hạn sống (TTL) tính bằng giây"]]),
            """Hôm nay ta trả lời bốn câu hỏi. [1.2] Thứ nhất, lưu hồ sơ khách hàng thế nào để lấy ra nhanh, câu trả lời là thiết kế khoá bản ghi.
            [1.3] Thứ hai, khoá nằm ở máy nào trong cụm, câu trả lời là băm khoá vào một thùng ảo, rồi tra bản đồ cụm.
            [1.4] Thứ ba, làm sao không mất năm mươi điểm, câu trả lời là dấu phiên bản, ghi kèm dấu đã đọc, lệch thì bị từ chối.
            [1.5] Thứ tư, phiên đăng nhập tự hết hạn thế nào, câu trả lời là hạn sống tính bằng giây."""),
    ], checks=["alg.bnx_cas_story(use_cas=False)[0] == 130", "alg.bnx_cas_story()[0] == 100 + 50 + 30 == 180"])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Kho khoá → giá trị", "đưa khoá, nhận lại đúng một giá trị, không phải quét", "khoá <code>so_du:TK-1001</code>"],
                   ["② Băm rồi chia dư", "cùng khoá luôn ra cùng số; số dư khi chia chọn ngăn (như chọn mảnh ở bài 8)", "17 chia 3 dư 2"],
                   ["③ Mất cập nhật", "hai bên đọc cùng giá trị cũ, cùng ghi; lần ghi sau xoá lần ghi trước", "100 → 150 rồi bị ghi đè thành 130"],
                   ["④ Hạn sống của khoá", "mục tự biến mất sau một số giây (Redis cũng có)", "hạn 60 giây"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Kho khoá và giá trị nhận một khoá và trả lại đúng một giá trị, không phải quét cả kho.
            [1.3] Băm rồi chia dư, như ở bài tám khi chọn mảnh cho bản ghi tìm kiếm. Cùng khoá luôn ra cùng số, và số dư khi chia chọn ra ngăn.
            [1.4] Mất cập nhật là khi hai bên đọc cùng một giá trị cũ rồi cùng ghi, nên lần ghi sau xoá lần ghi trước.
            [1.5] Còn hạn sống là số giây mà sau đó mục tự biến mất, Redis cũng có tính năng này."""),
        st("""$$100 + 50 = 150, \\qquad 100 + 30 = 130 \\neq 180$$""",
           """Một ví dụ số cho mất cập nhật. Một bên tính một trăm cộng năm mươi, bằng một trăm năm mươi. Bên kia tính từ cùng giá trị cũ, một trăm cộng ba mươi, bằng một trăm ba mươi, khác một trăm tám mươi.""",
           focus=[0, 1, 1]),
    ], checks=["100 + 50 == 150 and alg.bnx_cas_story(use_cas=False)[0] == 130", "alg.bnx_cas_story(use_cas=False)[0] != alg.bnx_cas_story()[0]"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["document key (khoá bản ghi)", "tên duy nhất của một bản ghi JSON trong kho, ví dụ <code>customer::C1001</code>"],
                   ["bucket (thùng dữ liệu)", "nơi chứa bản ghi, giống một cơ sở dữ liệu"],
                   ["vBucket (thùng ảo)", "một phần của thùng dữ liệu; khoá → thùng ảo qua băm CRC32. Bộ lưu Couchstore: 1024; Magma: 128 hoặc 1024; từ bản 8.0 (Enterprise) thùng mới mặc định Magma 128. Bài lấy 1024 làm ví dụ"],
                   ["cluster map (bản đồ cụm)", "bảng thùng ảo → máy đang giữ bản chính; thư viện khách tải về và gọi thẳng máy đó"],
                   ["CAS (dấu phiên bản)", "giá trị đổi mỗi lần bản ghi bị sửa; ghi kèm CAS đã đọc, lệch thì bị từ chối"],
                   ["TTL (hạn sống)", "số giây bản ghi được tồn tại trước khi kho tự xoá"]]),
            """Bảng này giải mã sáu từ. [1.2] Khoá bản ghi là tên duy nhất của một bản ghi JSON trong kho, ví dụ chữ khách hàng bằng tiếng Anh, hai dấu hai chấm, rồi mã khách hàng.
            [1.3] Thùng dữ liệu là nơi chứa bản ghi, giống một cơ sở dữ liệu.
            [1.4] Thùng ảo là một phần của thùng dữ liệu, và khoá được băm để chọn thùng ảo. Bộ lưu kiểu cũ có một nghìn không trăm hai mươi tư thùng ảo, còn từ bản tám, thùng dữ liệu mới mặc định có một trăm hai mươi tám. Bài này lấy một nghìn không trăm hai mươi tư làm ví dụ.
            [1.5] Bản đồ cụm cho biết thùng ảo nào đang ở máy nào, nên thư viện phía ứng dụng gọi thẳng máy đó.
            [1.6] Dấu phiên bản là giá trị đổi mỗi lần bản ghi bị sửa. Ta ghi kèm dấu đã đọc, nếu lệch thì bị từ chối.
            [1.7] Hạn sống là số giây bản ghi được tồn tại trước khi kho tự xoá."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: từ khoá tới máy, và hai bên cùng ghi", [
        st(svg(1500, 430,
               box(30, 60, 330, 90, ["khoá", "customer::C1001"], C_BLUE, size=24),
               arrow(360, 105, 470, 105, "#475569", "CRC32"),
               box(480, 45, 450, 120, ["2 170 508 415", "chia nguyên 65 536 → 33 119", "dư 32 768 → 351; dư 1024 → 351"], C_PURPLE, size=22),
               arrow(930, 105, 1000, 105),
               box(1010, 60, 160, 90, ["thùng ảo", "351"], C_AMBER, size=24, bold=True),
               arrow(1090, 155, 1090, 240, "#475569"),
               txt(1110, 205, "tra bản đồ cụm", 22, "start"),
               box(110, 250, 360, 80, "Máy 1: thùng 0–255", C_GRAY, size=24),
               box(490, 250, 380, 80, "Máy 2: thùng 256–511", C_GRAY, size=24),
               box(940, 250, 300, 80, "Máy 2 giữ 351", C_GREEN, size=24, bold=True),
               txt(750, 370, "(4 máy, mỗi máy 256 thùng ảo: số minh hoạ)", 22, "middle", "#6b7280"),
               txt(750, 415, "Khoá → thùng ảo không bao giờ đổi; thêm máy chỉ chuyển cả thùng ảo sang máy mới", 24, "middle", "#1f2937", True)),
           """Hình đầu đi từ khoá tới máy. Khoá hồ sơ được băm bằng hàm băm kiểm tra dư vòng, ra hơn hai tỉ.
           Thư viện chia nguyên số đó cho sáu mươi lăm nghìn năm trăm ba mươi sáu, rồi lấy dư cho ba mươi hai nghìn bảy trăm sáu mươi tám, được ba trăm năm mươi mốt.
           Lấy dư tiếp cho một nghìn không trăm hai mươi tư vẫn là ba trăm năm mươi mốt, nên bản ghi thuộc thùng ảo số ba trăm năm mươi mốt.
           Thư viện tra bản đồ cụm, ví dụ bốn máy mỗi máy giữ hai trăm năm mươi sáu thùng, thấy thùng này ở máy hai, nên gọi thẳng máy hai.
           Vì số thùng ảo cố định, khoá không bao giờ đổi thùng. Khi thêm máy, cụm chỉ chuyển nguyên cả thùng ảo sang máy mới và sửa bản đồ."""),
        st(svg(1500, 450,
               txt(90, 70, "P1", 28, "middle", "#2a78d6", True), txt(90, 270, "P2", 28, "middle", "#9333ea", True),
               box(150, 30, 260, 80, ["đọc 100", "CAS 7"], C_BLUE, size=22),
               box(470, 30, 300, 80, ["ghi 150, CAS 7", "khớp → CAS 8"], C_GREEN, size=22),
               box(150, 230, 260, 80, ["đọc 100", "CAS 7"], C_BLUE, size=22),
               box(830, 230, 300, 80, ["ghi 130, CAS 7", "lệch → từ chối"], C_RED, size=22),
               box(1170, 130, 300, 80, ["đọc lại 150, CAS 8", "ghi 180 → CAS 9"], C_GREEN, size=22),
               arrow(410, 70, 465, 70), arrow(410, 270, 825, 270), arrow(1130, 250, 1240, 215),
               txt(750, 400, "Không ai bị chặn đọc; chỉ lần ghi tính từ dữ liệu cũ bị từ chối", 26, "middle", "#1f2937", True)),
           """Hình thứ hai là hai tiến trình cùng ghi. Cả hai cùng đọc một trăm điểm với dấu phiên bản bảy.
           Tiến trình một ghi một trăm năm mươi kèm dấu bảy. Dấu khớp nên kho nhận, và dấu đổi thành tám.
           Tiến trình hai ghi một trăm ba mươi kèm dấu bảy. Dấu đã là tám nên kho từ chối.
           Tiến trình hai đọc lại một trăm năm mươi với dấu tám, cộng ba mươi thành một trăm tám mươi rồi ghi, dấu thành chín. Không ai bị chặn đọc cả."""),
    ], checks=[f"alg.bnx_crc32('{KEY}') == 2170508415", f"alg.bnx_vbucket('{KEY}') == 351",
               "alg.bnx_cas_story()[2][0] == ('P1', 'ghi', 150, 8)", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[:2] == (180, 9)", "1024 // 4 == 256 and 256 <= alg.bnx_vbucket('customer::C1001') <= 511"])
    form = sc("formula", "formula", "Suy ra từng bước: khoá, thùng ảo, dấu phiên bản, hạn sống", [
        stf("""<p><b>Bước 1.</b> Kho này tìm nhanh nhất <b>theo khoá</b>, nên khoá phải chứa thứ mà ứng dụng luôn có trong tay: loại bản ghi và mã nghiệp vụ.</p>
$$\\texttt{customer::C1001}, \\quad \\texttt{session::s9f2}$$
<span class='note'>Làm thử: mở hồ sơ C1001 = 1 lần lấy theo khoá, không quét bản ghi nào khác.</span>""",
            """[1] Bước một, vì kho này tìm nhanh nhất theo khoá, nên khoá phải chứa thứ ứng dụng luôn có trong tay, là loại bản ghi và mã nghiệp vụ.
            [2] Ví dụ khoá hồ sơ khách hàng, và khoá phiên đăng nhập. [3] Làm thử, mở hồ sơ C một nghìn không trăm linh một chỉ cần một lần lấy theo khoá, không quét bản ghi nào khác."""),
        stf(code(KEY_PY, "Bước 2. Khoá → thùng ảo, đúng cách thư viện Java của hãng tính") + out(KEY_OUT)
            + "<p class='note'>Ở <code>r = …</code>: dịch phải 16 = chia nguyên cho 65 536; phép &amp; với 0x7FFF = lấy dư cho 32 768.</p>",
            """[2.3] Bước hai, vì cụm cần biết khoá thuộc thùng ảo nào, nên thư viện băm khoá bằng hàm băm kiểm tra dư vòng có sẵn trong Python.
            [5] Dòng thứ tư làm đúng như thư viện Java chính thức của hãng. Nó chia nguyên cho sáu mươi lăm nghìn năm trăm ba mươi sáu, rồi lấy dư cho ba mươi hai nghìn bảy trăm sáu mươi tám.
            [4.1] Chạy thật, thương là ba mươi ba nghìn một trăm mười chín, lấy dư còn ba trăm năm mươi mốt.
            [4.2] Với một nghìn không trăm hai mươi tư thùng, thùng ảo là ba trăm năm mươi mốt. Với một trăm hai mươi tám thùng, mặc định của thùng dữ liệu mới, thì là chín mươi lăm.""",
            clear=True),
        stf("""<p><b>Bước 3.</b> Mỗi lần ghi mang theo CAS đã đọc. Kho so: <b>bằng</b> thì ghi và đổi CAS; <b>khác</b> thì từ chối.</p>
$$\\text{ghi được} \\iff \\text{CAS gửi kèm} = \\text{CAS hiện tại}$$
<span class='note'>Làm thử: P1 gửi 7, kho đang 7 → ghi, CAS đổi. P2 gửi 7, kho đang 8 → từ chối. Mô phỏng tăng CAS thêm 1; CAS thật là một số không đoán được, chỉ dùng để so bằng.</span>""",
            """[1] Bước ba, vì lỗi mất cập nhật đến từ việc ghi dựa trên dữ liệu cũ, nên mỗi lần ghi phải mang theo dấu phiên bản đã đọc.
            [2] Kho chỉ nhận khi dấu gửi kèm bằng dấu hiện tại. Mũi tên hai chiều đọc là khi và chỉ khi.
            [3] Làm thử, tiến trình một gửi bảy, kho đang bảy, nên ghi được và dấu đổi. Tiến trình hai cũng gửi bảy nhưng kho đã là tám, nên bị từ chối.
            Trong mô phỏng, dấu tăng thêm một. Dấu thật là một số không đoán trước được, chỉ dùng để so bằng.""",
            introduces=["iff"], clear=True),
        stf(code(STORE_PY, "Bước 4. Kho mô phỏng có CAS"),
            """[2.4] Bước bốn, vì muốn thấy quy tắc chạy thật, ta dựng một kho mô phỏng bằng Python. Hồ sơ có một trăm điểm, dấu phiên bản bảy.
            [2.6] Hàm đọc trả về bản sao của hồ sơ cùng dấu hiện tại. [2.8] Hàm ghi đè so dấu gửi kèm với dấu hiện tại, lệch thì từ chối.
            [2.10] Khớp thì lưu hồ sơ mới, nên dấu tăng thêm một.""",
            clear=True),
        stf(code(USE_PY, "Bước 5. Hai tiến trình cùng cộng điểm"),
            """[2.2] Bước năm, hai tiến trình cùng đọc, nên cùng thấy dấu bảy. [2.5] Tiến trình một cộng năm mươi rồi ghi.
            [2.7] Tiến trình hai cộng ba mươi rồi ghi với dấu cũ. [2.8] Bị từ chối thì nó đọc lại, cộng ba mươi vào giá trị mới, rồi ghi lần hai.""",
            clear=True),
        stf(out(USE_OUT, "Bước 5. Kết quả chạy thật"),
            """[2.1] Chạy thật, tiến trình một ghi được, dấu mới là tám. [2.2] Tiến trình hai bị từ chối vì dấu lệch.
            [2.3] Lần hai, sau khi đọc lại, tiến trình hai ghi được, dấu là chín. [2.4] Hồ sơ cuối cùng có một trăm tám mươi điểm, không mất cập nhật nào.""",
            clear=True),
        stf("""<p><b>Bước 6.</b> Bản ghi phiên đăng nhập cần tự hết hạn, nên đặt hạn sống tính bằng giây khi ghi:</p>
$$\\text{tạo lúc 9:00:00} + 1\\,800 \\text{ giây} = \\text{9:30:00}$$
<span class='note'>Số minh hoạ. Mỗi lần ghi lại bản ghi phải đặt lại hạn sống: ghi mà không đặt thì hạn sống về 0 (không bao giờ hết hạn), trừ khi dùng <code>preserve_expiry</code> hoặc thùng dữ liệu có hạn sống tối đa (<code>maxTTL</code>).</span>""",
            """[1] Bước sáu, vì phiên đăng nhập phải tự hết hiệu lực, nên khi ghi bản ghi phiên ta đặt hạn sống tính bằng giây.
            [2] Tạo lúc chín giờ đúng, cộng một nghìn tám trăm giây, tức ba mươi phút, thì hết hạn lúc chín giờ ba mươi. Đây là số minh hoạ.
            [3] Lưu ý, mỗi lần ghi lại bản ghi phải đặt lại hạn sống. Ghi mà không đặt thì hạn sống về không, nghĩa là không bao giờ hết hạn, trừ khi dùng tuỳ chọn giữ hạn cũ hoặc thùng dữ liệu có hạn sống tối đa.""",
            clear=True),
    ], checks=[f"alg.bnx_crc32('{KEY}') // 65536 == 33119 and 33119 % 32768 == 351", f"alg.bnx_vbucket('{KEY}') == 351 and alg.bnx_vbucket('{KEY}', 128) == 95",
               "2 ** 16 == 65536 and 0x7FFF + 1 == 32768", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[:2] == (180, 9)", "alg.bnx_clock_add(9, 0, 0, 1800) == (9, 30, 0)",
               "alg.bnx_ttl_after_mutation(1800, False) == 0 and alg.bnx_ttl_after_mutation(1800, False, True) == 1800"])
    ex = sc("example", "example", "Ví dụ hai tiến trình cùng cộng điểm, từng phép tính", [
        st("""<p>Hồ sơ C1001: 100 điểm, CAS = 7. P1 cộng 50, P2 cộng 30, cả hai đọc trước khi ai ghi (số minh hoạ).</p>
$$① \\; \\text{P1: } 100 + 50 = \\hl{150}$$""",
           """Ta tính từng bước. Hồ sơ có một trăm điểm, dấu phiên bản bảy. Tiến trình một cộng năm mươi, tiến trình hai cộng ba mươi, và cả hai đọc trước khi ai ghi.
           Phép tính thứ nhất, tiến trình một tính một trăm cộng năm mươi, bằng một trăm năm mươi.""", focus=[1, 1, 1, 2]),
        st("""$$② \\; \\text{P1 ghi kèm CAS 7; kho đang 7} \\Rightarrow \\text{nhận } \\hlg{150},\\ \\text{CAS} = 8$$""",
           """Phép tính thứ hai, tiến trình một ghi kèm dấu bảy, kho đang bảy, suy ra kho nhận một trăm năm mươi và dấu thành tám. Mũi tên kép đọc là suy ra."""),
        st("""$$③ \\; \\text{P2 ghi } 100 + 30 = 130 \\text{ kèm CAS 7; kho đang 8} \\Rightarrow \\hl{\\text{từ chối}}$$""",
           """Phép tính thứ ba, tiến trình hai ghi một trăm cộng ba mươi, bằng một trăm ba mươi, kèm dấu bảy. Kho đang tám, nên từ chối."""),
        st("""<p>Dùng lại $150$ và CAS $8$ ở phép ②.</p>
$$④ \\; \\text{P2 đọc lại: } 150 + 30 = \\hlg{180},\\ \\text{CAS} = 9$$""",
           """Phép tính thứ tư, dùng lại một trăm năm mươi và dấu tám ở phép thứ hai. Tiến trình hai đọc lại, tính một trăm năm mươi cộng ba mươi, bằng một trăm tám mươi, và dấu thành chín.""",
           focus=[1, 2], clear=True),
        st("""<p>Nếu không có CAS, P2 ghi đè 130 ở phép ③:</p>
$$⑤ \\; 180 - 130 = \\hl{50}\\ \\text{điểm bị mất}$$
<div class="box key">Có CAS: $100 + 50 + 30 = 180$, không mất cập nhật nào.</div>""",
           """Phép tính thứ năm, nếu không có dấu phiên bản, tiến trình hai ghi đè một trăm ba mươi. Một trăm tám mươi trừ một trăm ba mươi bằng năm mươi điểm bị mất, đúng bằng phần của tiến trình một.
           Có dấu phiên bản thì một trăm cộng năm mươi cộng ba mươi bằng một trăm tám mươi, không mất cập nhật nào.""",
           focus=[1, 2, 3]),
    ], checks=["alg.bnx_cas_story()[2][0] == ('P1', 'ghi', 150, 8)", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[2][3] == ('P2', 'ghi', 180, 9)",
               "alg.bnx_cas_story()[0] - alg.bnx_cas_story(use_cas=False)[0] == 50"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: thử mọi thứ tự đọc và ghi", [
        stf(code(INTER_PY, "Đường khác: liệt kê mọi thứ tự của 4 sự kiện"),
            """[2] Kiểm bằng đường khác. Thay vì chỉ một kịch bản, ta liệt kê mọi thứ tự của bốn sự kiện, mỗi tiến trình đọc một lần rồi ghi một lần.
            [2.7] Có dấu phiên bản thì khi dấu lệch, tiến trình đọc lại giá trị mới rồi mới cộng."""),
        stf(out(INTER_OUT),
            """[2.1] Chạy thật, có sáu thứ tự, và khi bật dấu phiên bản, mọi thứ tự đều cho một trăm tám mươi, vì không lần ghi nào dựa trên giá trị cũ.
            [2.2] Khi tắt, kết quả có thể là một trăm ba mươi, một trăm năm mươi hoặc một trăm tám mươi, tuỳ ai ghi sau.""", clear=True),
        stf(table(["kiểu", "chặn đọc?", "khi tranh chấp"],
                  [["CAS (khoá lạc quan)", "không", "người ghi sau bị từ chối, tự đọc lại rồi thử lại"],
                   ["khoá bi quan (get-and-lock)", "vẫn đọc được, nhưng không ai sửa được nếu không có đúng CAS của khoá", "người khác phải chờ hết khoá"]]),
            """[1.2] Bảng này so hai cách. Dấu phiên bản còn gọi là khoá lạc quan, không chặn ai đọc, người ghi sau bị từ chối và tự thử lại.
            [1.3] Khoá bi quan thì giữ bản ghi lại. Người khác vẫn đọc được, nhưng không ai sửa được nếu không có đúng dấu của khoá, nên phải chờ.""",
            clear=True),
    ], checks=["alg.bnx_interleavings(True) == (6, [180])", "alg.bnx_interleavings(False) == (6, [130, 150, 180])"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng CAS là <b class="red">khoá</b>: đọc kèm CAS thì người khác không đọc được. Sai: CAS không chặn ai đọc, chỉ chặn ghi đè bản cũ.
<br><span class="note">Kèm theo: bắt lỗi “CAS lệch” rồi bỏ qua là mất cập nhật y như không có CAS. Phải đọc lại và thử lại, có giới hạn số lần.</span></div>""",
           """Lỗi thứ nhất, của người mới, là tưởng dấu phiên bản là một cái khoá, đọc kèm dấu thì người khác không đọc được. Sai, dấu không chặn ai đọc, chỉ chặn ghi đè bản cũ.
           Kèm theo đó, bắt lỗi dấu lệch rồi bỏ qua thì vẫn mất cập nhật y như không có dấu. Phải đọc lại và thử lại, có giới hạn số lần."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Cập nhật bản ghi phiên (gia hạn, ghi lần truy cập) mà <b class="red">không đặt lại hạn sống</b> → hạn sống về 0, phiên <b>không bao giờ hết hạn</b>.
<br><span class="note">Cách chữa: mỗi lần ghi đặt lại hạn sống, hoặc dùng <code>preserve_expiry</code> để giữ hạn cũ. Kiểm bằng cách đọc hạn sống sau khi cập nhật.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm. Cập nhật bản ghi phiên, ví dụ ghi lần truy cập cuối, mà không đặt lại hạn sống. Hạn sống bị đưa về không, và phiên không bao giờ hết hạn.
           Cách chữa là mỗi lần ghi đặt lại hạn sống, hoặc dùng tuỳ chọn giữ hạn cũ. Hãy kiểm bằng cách đọc lại hạn sống sau khi cập nhật.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Để khoá ngẫu nhiên rồi mới nghĩ cách truy cập: muốn mở hồ sơ theo mã khách hàng lại phải tìm theo trường bên trong, chậm hơn nhiều so với lấy thẳng theo khoá.
<br><span class="note">Cách chữa: thiết kế khoá trước (<code>customer::&lt;mã&gt;</code>). Và kho bản ghi giữ hồ sơ, phiên; <b>sổ cái số dư</b> vẫn ở lõi ngân hàng.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là để khoá ngẫu nhiên rồi mới nghĩ cách truy cập. Muốn mở hồ sơ theo mã khách hàng lại phải tìm theo trường bên trong, chậm hơn nhiều so với lấy thẳng theo khoá.
           Cách chữa là thiết kế khoá trước. Và nhớ rằng kho này giữ hồ sơ và phiên, còn sổ cái số dư vẫn ở lõi ngân hàng.""",
           clear=True),
    ], checks=["alg.bnx_ttl_after_mutation(1800, False) == 0"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "CRC32 của một khoá ra 1 000 000 000 (số minh hoạ). Có 1024 thùng ảo, khoá vào thùng nào (cách của thư viện Java)?"],
                   ["2", "Hồ sơ 200 điểm, CAS 12. P1 trừ 40, P2 cộng 25, cùng đọc trước; P1 ghi trước. Kết quả có CAS? Không có CAS?"],
                   ["3", "Quyết định: cập nhật “hạn mức đã dùng trong ngày” của khách, nhiều yêu cầu cùng lúc. Dùng CAS hay khoá bi quan?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.2] Câu một, băm một khoá ra một tỉ, có một nghìn không trăm hai mươi tư thùng ảo, khoá vào thùng nào?
            [1.3] Câu hai, hồ sơ hai trăm điểm, dấu mười hai. Tiến trình một trừ bốn mươi, tiến trình hai cộng hai mươi lăm, cùng đọc trước, tiến trình một ghi trước. Kết quả khi có và không có dấu?
            [1.4] Câu ba, cập nhật hạn mức đã dùng trong ngày của khách, nhiều yêu cầu cùng lúc. Dùng dấu phiên bản hay khoá bi quan? [0] Hãy dừng video và làm ra giấy.""",
            pause=25),
        st("""<p>Câu 1: chia nguyên cho 65 536 được 15 258; số này nhỏ hơn 32 768 nên lấy dư vẫn là 15 258.</p>
$$15\\,258 - 14 \\cdot 1\\,024 = 15\\,258 - 14\\,336 = \\hlg{922}$$""",
           """Đáp án câu một. Một tỉ chia nguyên cho sáu mươi lăm nghìn năm trăm ba mươi sáu được mười lăm nghìn hai trăm năm mươi tám, nhỏ hơn ba mươi hai nghìn bảy trăm sáu mươi tám nên giữ nguyên.
           Lấy dư cho một nghìn không trăm hai mươi tư, tức trừ mười bốn nhân một nghìn không trăm hai mươi tư, còn chín trăm hai mươi hai. Khoá vào thùng ảo chín trăm hai mươi hai.""",
           focus=[1, 1, 2, 2]),
        stf("""<p>Câu 2: P1 ghi $200 - 40 = 160$, CAS thành 13; P2 gửi CAS 12 → từ chối, đọc lại 160.</p>
$$\\text{có CAS: } 160 + 25 = \\hlg{185}, \\qquad \\text{không CAS: } 200 + 25 = \\hl{225}$$""",
            """[1] Đáp án câu hai. Tiến trình một ghi hai trăm trừ bốn mươi, bằng một trăm sáu mươi, dấu thành mười ba. Tiến trình hai gửi dấu mười hai nên bị từ chối và đọc lại.
            [2] Có dấu thì một trăm sáu mươi cộng hai mươi lăm bằng một trăm tám mươi lăm. Không có dấu thì hai trăm cộng hai mươi lăm bằng hai trăm hai mươi lăm, mất phần trừ bốn mươi."""),
        stf(table(["lựa chọn", "được", "mất"],
                  [["CAS (lạc quan)", "không chặn đọc; ít tranh chấp thì gần như không tốn thêm", "nhiều yêu cầu cùng lúc thì bị từ chối liên tục, phải thử lại có giới hạn"],
                   ["khoá bi quan", "người giữ khoá chắc chắn ghi được", "người khác phải chờ; khoá phải có thời hạn, giữ lâu thì nghẽn"]])
            + """<div class="box key">Hạn mức có nhiều yêu cầu cùng lúc: chọn <b>khoá bi quan ngắn, có thời hạn</b>, vì CAS sẽ bị từ chối liên tục.</div>""",
            """[1.2] Đáp án câu ba. Dấu phiên bản không chặn đọc, ít tranh chấp thì gần như không tốn thêm, nhưng nhiều yêu cầu cùng lúc thì bị từ chối liên tục và phải thử lại có giới hạn.
            [1.3] Khoá bi quan cho người giữ khoá chắc chắn ghi được, đổi lại người khác phải chờ, và khoá phải có thời hạn.
            [2] Vậy với hạn mức có nhiều yêu cầu cùng lúc, nên chọn khoá bi quan ngắn có thời hạn, vì dấu phiên bản sẽ bị từ chối liên tục."""),
    ], checks=["10**9 // 65536 == 15258 < 32768 and 15258 - 14 * 1024 == 922 == alg.bnx_vbucket_of_crc(10**9)",
               "alg.bnx_cas_story(200, 12, (('P1', -40), ('P2', 25)))[:2] == (185, 14)",
               "alg.bnx_cas_story(200, 12, (('P1', -40), ('P2', 25)), use_cas=False)[0] == 225"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("khoá customer::C1001", "CRC32 → thùng ảo 351", "bản đồ cụm → máy", "ghi kèm CAS: lệch thì đọc lại", "180, không mất điểm"),
           """Tổng kết chuỗi logic. Khoá bản ghi được băm ra thùng ảo ba trăm năm mươi mốt, bản đồ cụm chỉ ra máy giữ thùng đó.
           Mỗi lần ghi mang theo dấu phiên bản, lệch thì đọc lại rồi ghi, nên kết quả là một trăm tám mươi điểm, không mất cập nhật."""),
        st("""<div class='box key'><b>Tư duy:</b> thiết kế <b>khoá trước</b>, vì đó là cách truy cập chính. Mỗi lần “đọc, sửa, ghi” phải mang CAS. Bản ghi phiên luôn có hạn sống, và hạn sống phải được đặt lại mỗi lần ghi.</div>""",
           """Điều cần mang theo. Thiết kế khoá trước, vì đó là cách truy cập chính. Mỗi lần đọc, sửa, ghi phải mang dấu phiên bản. Bản ghi phiên luôn có hạn sống, và phải đặt lại mỗi lần ghi."""),
        st("""<p>Bài sau: Kafka giữ bản cuối của mỗi khoá trong nhật ký, kiểm lược đồ trước khi bên gửi đổi, và một hàng đợi khác định tuyến theo mẫu chủ đề.</p>""",
           """Ở bài sau, ta học Kafka nâng cao, gồm nén nhật ký chỉ giữ bản cuối của mỗi khoá, kiểm lược đồ trước khi bên gửi đổi, và một hàng đợi khác định tuyến theo mẫu.""",
           forward_ref=True),
    ])
    return lesson("L09", "couchbase_vbucket_cas", "Bài 9 — Couchbase: bản ghi theo khoá, vBucket và giá trị CAS chống ghi đè",
                  "curriculum/bnx.yaml L09; audit/bnx/verify_bnx.py L09; Couchbase Server docs 8.0 (đọc 2026-11-11): vBuckets, Expiration, "
                  "Manage Expiration (Mutation's Effect on Expiration); Couchbase Java SDK 3.13 docs: Concurrent Document Mutations",
                  ["Thiết kế khoá bản ghi cho hồ sơ khách hàng", "Tính vBucket của một khoá", "Dùng giá trị CAS để chặn mất cập nhật",
                   "Đặt hạn sống cho bản ghi phiên"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
