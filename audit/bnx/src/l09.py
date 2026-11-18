import re

import lib2
from lib2 import *

lib2.begin("L09")

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

# Đầu ra THẬT: prog() chạy nguyên văn lúc import (Python 3.13); khối USE chạy cùng STORE (cùng một chương trình).
NL = chr(10)
P_KEY = prog("Key", KEY_PY, lang="python")
P_USE = prog("StoreUse", STORE_PY.strip() + NL + USE_PY.strip(), lang="python")
P_INTER = prog("Inter", INTER_PY, lang="python")
KEY_OUT, USE_OUT, INTER_OUT = P_KEY.out, P_USE.out, P_INTER.out

# Cảnh quy mô: n tiến trình cùng đọc rồi cùng ghi (tranh chấp hoàn toàn) trên chính lớp Store của bài; đếm số lần ghi.
SCALE_PY = """
for n in (2, 20, 200):
    s, chua, lan = Store(), n, 0
    s.doc["diem_thuong"] = 0
    while chua:
        bo = [s.get() for _ in range(chua)]    # cùng đọc
        chua = 0
        for d, cas in bo:
            d["diem_thuong"] += 1
            lan += 1
            if s.replace(d, cas).startswith("từ"):
                chua += 1
    print(n, "tien trinh:", lan, "lan ghi, diem", s.doc["diem_thuong"])
"""
P_SCALE = prog("Scale", STORE_PY.strip() + NL + SCALE_PY.strip(), lang="python")
LAB_PY = """
import zlib
khoa = "session::s77"
r = (zlib.crc32(khoa.encode()) >> 16) & 0x7FFF
print("thung ao (1024):", r % 1024, "| (128):", r % 128)
doc, cas = 300, 4
def ghi(moi, cas_kem):
    global doc, cas
    if cas_kem != cas:
        return "tu choi"
    doc, cas = moi, cas + 1
    return "ghi duoc, CAS moi = %d" % cas
d1, c1 = doc, cas
d2, c2 = doc, cas
print("P1:", ghi(d1 + 20, c1))
print("P2:", ghi(d2 - 50, c2))
d2, c2 = doc, cas
print("P2 lan 2:", ghi(d2 - 50, c2))
print("cuoi:", doc, cas)
"""
P_LAB = prog("Lab", LAB_PY, lang="python")
LAB_OUT = P_LAB.out
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
            """[1] Chào bạn, hồ sơ khách hàng C một nghìn không trăm linh một có một trăm điểm thưởng. Cùng một lúc, dịch vụ khuyến mãi cộng năm mươi điểm, dịch vụ hoàn tiền cộng ba mươi điểm, đây là số minh hoạ.
            [2] Ta mong đợi một trăm tám mươi, nhưng hồ sơ chỉ ghi một trăm ba mươi.
            [3] Cả hai cùng đọc một trăm, mỗi bên tự cộng rồi ghi đè, nên lần ghi sau xoá mất năm mươi điểm của lần ghi trước, gọi là mất cập nhật."""),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["lưu hồ sơ khách hàng thế nào để lấy ra nhanh", "khoá bản ghi <code>customer::C1001</code>"],
                   ["khoá nằm ở máy nào trong cụm (nhóm máy)", "thùng ảo (vBucket) = băm khoá, rồi tra bản đồ cụm"],
                   ["làm sao không mất 50 điểm", "dấu phiên bản CAS: ghi kèm dấu đã đọc, lệch thì bị từ chối"],
                   ["phiên đăng nhập tự hết hạn thế nào", "hạn sống (TTL) tính bằng giây"]]),
            """Hôm nay ta trả lời bốn câu hỏi. [1.2] Lưu hồ sơ để lấy ra nhanh thì thiết kế khoá bản ghi. [1.3] Khoá nằm ở máy nào trong cụm, tức nhóm máy chạy chung kho, thì băm vào một thùng ảo rồi tra bản đồ cụm.
            [1.4] Để không mất năm mươi điểm thì ghi kèm dấu phiên bản. [1.5] Phiên đăng nhập tự hết hạn nhờ hạn sống tính bằng giây.""", introduces=["bnx_cas", "bnx_vbucket"]),
    ], checks=["alg.bnx_cas_story(use_cas=False)[0] == 130", "alg.bnx_cas_story()[0] == 100 + 50 + 30 == 180"])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Kho khoá → giá trị", "đưa khoá, nhận lại đúng một giá trị, không phải quét", "khoá <code>so_du:TK-1001</code>"],
                   ["② Băm rồi chia dư", "cùng khoá luôn ra cùng số; số dư khi chia chọn ngăn", "17 chia 3 dư 2"],
                   ["③ Mất cập nhật", "hai bên (hai <b>tiến trình</b>: hai chương trình đang chạy cùng lúc) đọc cùng giá trị cũ, cùng ghi; lần ghi sau xoá lần ghi trước", "100 → 150 rồi bị ghi đè thành 130"],
                   ["④ Hạn sống của khoá", "mục tự biến mất sau một số giây", "hạn 60 giây"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Kho khoá và giá trị nhận một khoá và trả lại đúng một giá trị, không phải quét cả kho.
            [1.3] Băm rồi chia dư là cách chọn ngăn: cùng khoá luôn ra cùng số, và số dư chọn ra ngăn.
            [1.4] Mất cập nhật là khi hai tiến trình, tức hai chương trình chạy cùng lúc, đọc cùng một giá trị cũ rồi cùng ghi, nên lần ghi sau xoá lần ghi trước.
            [1.5] Hạn sống là số giây sau đó một mục tự biến mất."""),
        st("""$$100 + 50 = 150, \\qquad 100 + 30 = 130 \\neq 180$$""",
           """Một bên tính một trăm cộng năm mươi, bằng một trăm năm mươi. Bên kia tính từ cùng giá trị cũ, một trăm cộng ba mươi, bằng một trăm ba mươi, khác một trăm tám mươi.""",
           focus=[0, 1, 1]),
    ], checks=["100 + 50 == 150 and alg.bnx_cas_story(use_cas=False)[0] == 130", "alg.bnx_cas_story(use_cas=False)[0] != alg.bnx_cas_story()[0]"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["document key (khoá bản ghi)", "tên duy nhất của một bản ghi dạng JSON (các cặp <code>tên: giá trị</code> trong ngoặc nhọn) trong kho, ví dụ <code>customer::C1001</code>"],
                   ["bucket (thùng dữ liệu)", "nơi chứa bản ghi, giống một cơ sở dữ liệu"],
                   ["vBucket (thùng ảo)", "một phần của thùng dữ liệu; khoá → thùng ảo qua băm CRC32. <b>Bộ lưu</b> là cách kho ghi dữ liệu xuống đĩa: Couchstore (kiểu cũ) có 1024 thùng ảo; Magma (kiểu mới) 128 hoặc 1024; từ bản 8.0, ở bản Enterprise (bản thương mại), thùng mới mặc định Magma 128. Bài lấy 1024 làm ví dụ"]]),
            """Bảng này giải mã sáu từ, ba từ đầu trước. [1.2] Khoá bản ghi là tên duy nhất của một bản ghi trong kho. Bản ghi dạng JSON là các cặp tên và giá trị trong ngoặc nhọn.
            [1.4] Thùng ảo là một phần của thùng dữ liệu, và khoá được băm để chọn thùng ảo. Bộ lưu là cách kho ghi dữ liệu xuống đĩa: kiểu cũ có một nghìn không trăm hai mươi tư thùng ảo, kiểu mới ở bản thương mại mặc định một trăm hai mươi tám."""),
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["cluster map (bản đồ cụm)", "bảng thùng ảo → máy đang giữ bản chính; thư viện khách (mã của hãng, nằm trong ứng dụng, nói chuyện với kho) tải về và gọi thẳng máy đó"],
                   ["CAS (dấu phiên bản)", "giá trị đổi mỗi lần bản ghi bị sửa; ghi kèm CAS đã đọc, lệch thì bị từ chối"],
                   ["TTL (hạn sống)", "số giây bản ghi được tồn tại trước khi kho tự xoá"]]),
            """Ba từ còn lại. [1.2] Bản đồ cụm cho biết thùng ảo nào ở máy nào.
            [1.3] Dấu phiên bản là giá trị đổi mỗi lần bản ghi bị sửa. [1.4] Hạn sống là số giây bản ghi tồn tại trước khi kho tự xoá.""", clear=True),
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
           """Khoá hồ sơ được băm ra hơn hai tỉ. Thư viện chia nguyên cho sáu mươi lăm nghìn năm trăm ba mươi sáu rồi lấy dư cho ba mươi hai nghìn bảy trăm sáu mươi tám, được ba trăm năm mươi mốt.
           Lấy dư tiếp cho một nghìn không trăm hai mươi tư, bản ghi thuộc thùng ảo ba trăm năm mươi mốt. Tra bản đồ cụm, thùng này nằm ở máy hai.
"""),
        st(svg(1500, 450,
               txt(90, 70, "P1", 28, "middle", "#2a78d6", True), txt(90, 270, "P2", 28, "middle", "#9333ea", True),
               box(150, 30, 260, 80, ["đọc 100", "CAS 7"], C_BLUE, size=22),
               box(470, 30, 300, 80, ["ghi 150, CAS 7", "khớp → CAS 8"], C_GREEN, size=22),
               box(150, 230, 260, 80, ["đọc 100", "CAS 7"], C_BLUE, size=22),
               box(830, 230, 300, 80, ["ghi 130, CAS 7", "lệch → từ chối"], C_RED, size=22),
               box(1170, 130, 300, 80, ["đọc lại 150, CAS 8", "ghi 180 → CAS 9"], C_GREEN, size=22),
               arrow(410, 70, 465, 70), arrow(410, 270, 825, 270), arrow(1130, 250, 1240, 215),
               txt(750, 400, "Không ai bị chặn đọc; chỉ lần ghi tính từ dữ liệu cũ bị từ chối", 26, "middle", "#1f2937", True)),
           """Hai tiến trình cùng đọc một trăm điểm với dấu phiên bản bảy. Tiến trình một ghi một trăm năm mươi kèm dấu bảy.
           Tiến trình hai ghi một trăm ba mươi kèm dấu bảy, nhưng dấu đã là tám nên kho từ chối. Tiến trình hai đọc lại một trăm năm mươi với dấu tám, cộng ba mươi thành một trăm tám mươi rồi ghi, dấu thành chín."""),
    ], checks=[f"alg.bnx_crc32('{KEY}') == 2170508415", f"alg.bnx_vbucket('{KEY}') == 351",
               "alg.bnx_cas_story()[2][0] == ('P1', 'ghi', 150, 8)", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[:2] == (180, 9)", "1024 // 4 == 256 and 256 <= alg.bnx_vbucket('customer::C1001') <= 511"])
    form = sc("formula", "formula", "Suy ra từng bước: khoá, thùng ảo, dấu phiên bản, hạn sống", [
        stf("""<p><b>Bước 1.</b> Kho này tìm nhanh nhất <b>theo khoá</b>, nên khoá phải chứa thứ mà ứng dụng luôn có trong tay: loại bản ghi và mã nghiệp vụ.</p>
$$\\texttt{customer::C1001}, \\quad \\texttt{session::s9f2}$$
<span class='note'>Làm thử: mở hồ sơ C1001 = 1 lần lấy theo khoá, không quét bản ghi nào khác.</span>""",
            """[1] Bước một, vì kho này tìm nhanh nhất theo khoá, nên khoá phải chứa thứ ứng dụng luôn có trong tay, là loại bản ghi và mã nghiệp vụ.
            [2] [3] Làm thử, mở hồ sơ C một nghìn không trăm linh một chỉ cần một lần lấy theo khoá."""),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>zlib.crc32(key.encode())</code>", "<code>.encode()</code> đổi chữ thành byte; <code>zlib.crc32</code> băm chúng thành một số nguyên 32 bit"],
                  ["<code>h // 65536</code>, <code>h % 1024</code>", "<code>//</code> chia lấy phần nguyên; <code>%</code> lấy số dư"]]),
           """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Hàm băm biến byte thành một số nguyên, hai dấu gạch chéo là chia lấy phần nguyên, còn dấu phần trăm lấy số dư.""", clear=True),
        stf(code(KEY_PY, "Bước 2. Khoá → thùng ảo, đúng cách thư viện Java của hãng tính") + out(KEY_OUT)
            + "<p class='note'>Ở <code>r = …</code>: dịch phải 16 = chia nguyên cho 65 536; phép &amp; với 0x7FFF = lấy dư cho 32 768.</p>",
            """[2.3] Bước hai, vì cụm cần biết khoá thuộc thùng ảo nào, nên thư viện băm khoá bằng hàm băm kiểm tra dư vòng, rồi chia nguyên và lấy dư. [5] Chạy thật, thương là ba mươi ba nghìn một trăm mười chín, lấy dư còn ba trăm năm mươi mốt.
            [4.1]
            [4.2]""",
            clear=True),
        stf("""<p><b>Bước 3.</b> Mỗi lần ghi mang theo CAS đã đọc. Kho so: <b>bằng</b> thì ghi và đổi CAS; <b>khác</b> thì từ chối.</p>
$$\\text{ghi được} \\iff \\text{CAS gửi kèm} = \\text{CAS hiện tại}$$
<span class='note'>Làm thử: P1 gửi 7, kho đang 7 → ghi, CAS đổi. P2 gửi 7, kho đang 8 → từ chối. Mô phỏng tăng CAS thêm 1; CAS thật là một số không đoán được, chỉ dùng để so bằng.</span>""",
            """[1] Bước ba, vì lỗi mất cập nhật đến từ việc ghi dựa trên dữ liệu cũ, nên mỗi lần ghi phải mang theo dấu phiên bản đã đọc. [2] Kho chỉ nhận khi dấu gửi kèm bằng dấu hiện tại.
            [3] Làm thử, tiến trình một gửi bảy, kho đang bảy, nên ghi được. Tiến trình hai cũng gửi bảy nhưng kho đã là tám, nên bị từ chối.
""",
            introduces=["iff"], clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>class Store:</code>", "<b>lớp</b>: khuôn tạo ra một đối tượng có dữ liệu và hàm riêng, ở đây là một kho"],
                  ["<code>def __init__(self):</code>", "hàm chạy khi tạo kho; <code>self</code> là chính cái kho đó"],
                  ["<code>self.doc, self.cas = {…}, 7</code>", "gán hai thuộc tính cùng lúc: nội dung (một từ điển) và dấu phiên bản"],
                  ["<code>return dict(self.doc), self.cas</code>", "trả về <b>hai giá trị</b> cùng lúc: bản sao nội dung và dấu phiên bản; nơi gọi nhận bằng <code>d, c = s.get()</code>"],
                  ["<code>dict(self.doc)</code>, <code>\"…%d\" % x</code>", "sao chép từ điển để sửa không đụng dữ liệu đang giữ; chèn số <code>x</code> vào chỗ <code>%d</code>"]]),
           """Kho mô phỏng dùng thêm vài cách viết nữa, nên ta giải nghĩa trước. Lớp là khuôn tạo ra một kho có dữ liệu và hàm riêng, và tham số đầu của hàm là chính cái kho đó. Dòng gán đặt nội dung và dấu phiên bản cùng lúc, còn lệnh trả về có thể trả hai giá trị một lúc.""", clear=True),
        stf(code(STORE_PY, "Bước 4. Kho mô phỏng có CAS"),
            """[2.3] Bước bốn, vì muốn thấy quy tắc chạy thật, ta dựng một kho mô phỏng bằng Python. Hồ sơ có một trăm điểm, dấu phiên bản bảy.
            [2.4] Hàm đọc trả về bản sao của hồ sơ cùng dấu hiện tại. [2.6] Hàm ghi đè so dấu gửi kèm với dấu hiện tại, lệch thì từ chối.""",
            clear=True),
        stf(code(USE_PY, "Bước 5. Hai tiến trình cùng cộng điểm"),
            """[2.2] Bước năm, hai tiến trình cùng đọc, nên cùng thấy dấu bảy. [2.5] Tiến trình một cộng năm mươi rồi ghi. [2.7] Tiến trình hai cộng ba mươi rồi ghi với dấu cũ. [2.8] Bị từ chối thì nó đọc lại, cộng ba mươi vào giá trị mới, rồi ghi lần hai.""",
            clear=True),
        stf(out(USE_OUT, "Bước 5. Kết quả chạy thật"),
            """[2.1] Tiến trình một ghi được, dấu mới là tám. [2.2] Tiến trình hai bị từ chối vì dấu lệch.
            [2.3] Lần hai, sau khi đọc lại, tiến trình hai ghi được, dấu là chín. [2.4] Hồ sơ cuối cùng có một trăm tám mươi điểm, không mất cập nhật nào.""",
            clear=True),
        stf("""<p><b>Bước 6.</b> Bản ghi phiên đăng nhập cần tự hết hạn, nên đặt hạn sống tính bằng giây khi ghi:</p>
$$\\text{tạo lúc 9:00:00} + 1\\,800 \\text{ giây} = \\text{9:30:00}$$
<span class='note'>Số minh hoạ. Mỗi lần ghi lại bản ghi phải đặt lại hạn sống: ghi mà không đặt thì hạn sống về 0 (không bao giờ hết hạn), trừ khi dùng <code>preserve_expiry</code> hoặc thùng dữ liệu có hạn sống tối đa (<code>maxTTL</code>).</span>""",
            """[1] Bước sáu, vì phiên đăng nhập phải tự hết hiệu lực, nên khi ghi bản ghi phiên ta đặt hạn sống tính bằng giây.
            [2] Tạo lúc chín giờ đúng, cộng một nghìn tám trăm giây, tức ba mươi phút, thì hết hạn lúc chín giờ ba mươi. Đây là số minh hoạ.
            [3] Ghi mà không đặt thì hạn sống về không, tức không bao giờ hết hạn.""",
            clear=True),
    ], checks=[f"alg.bnx_crc32('{KEY}') // 65536 == 33119 and 33119 % 32768 == 351", f"alg.bnx_vbucket('{KEY}') == 351 and alg.bnx_vbucket('{KEY}', 128) == 95",
               "2 ** 16 == 65536 and 0x7FFF + 1 == 32768", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[:2] == (180, 9)", "alg.bnx_clock_add(9, 0, 0, 1800) == (9, 30, 0)",
               "alg.bnx_ttl_after_mutation(1800, False) == 0 and alg.bnx_ttl_after_mutation(1800, False, True) == 1800"])
    ex = sc("example", "example", "Ví dụ hai tiến trình cùng cộng điểm, từng phép tính", [
        st("""<p>Hồ sơ C1001: 100 điểm, CAS = 7. P1 cộng 50, P2 cộng 30, cả hai đọc trước khi ai ghi (số minh hoạ).</p>
$$① \\; \\text{P1: } 100 + 50 = \\hl{150}$$""",
           """Hồ sơ có một trăm điểm, dấu phiên bản bảy. Tiến trình một cộng năm mươi, tiến trình hai cộng ba mươi, và cả hai đọc trước khi ai ghi.
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
           Có dấu phiên bản thì không mất cập nhật nào.""",
           focus=[1, 2, 3]),
    ], checks=["alg.bnx_cas_story()[2][0] == ('P1', 'ghi', 150, 8)", "alg.bnx_cas_story()[2][1] == ('P2', 'từ chối')",
               "alg.bnx_cas_story()[2][3] == ('P2', 'ghi', 180, 9)",
               "alg.bnx_cas_story()[0] - alg.bnx_cas_story(use_cas=False)[0] == 50"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: thử mọi thứ tự đọc và ghi", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>def f(order, cas_on): … return v</code>", "định nghĩa hàm nhận hai đầu vào; <code>return</code> trả kết quả <code>v</code> ra"],
                  ["<code>from itertools import permutations</code>", "nạp hàm <code>permutations</code>, liệt kê mọi cách xếp thứ tự"],
                  ["<code>a; continue</code>", "dấu <code>;</code> đặt hai lệnh trên một dòng; <code>continue</code> bỏ qua phần còn lại của vòng lặp này, sang vòng kế tiếp"],
                  ["<code>x = a if điều_kiện else b</code>", "<code>x</code> lấy <code>a</code> nếu điều kiện đúng, không thì lấy <code>b</code>"],
                  ["<code>p not in rd</code>", "<code>p</code> chưa có trong từ điển <code>rd</code>"]]),
           """Hàm kiểm dùng thêm vài cách viết, nên ta giải nghĩa trước. Một dòng nạp hàm liệt kê mọi thứ tự. Hàm nhận đầu vào rồi trả kết quả ra. Dấu chấm phẩy đặt hai lệnh một dòng, lệnh bỏ qua chuyển sang vòng lặp kế tiếp, và cách viết chọn một trong hai giá trị tuỳ điều kiện.""",
           clear=True),
        stf(code(INTER_PY, "Đường khác: liệt kê mọi thứ tự của 4 sự kiện")
            + """<p class="note"><code>permutations([…])</code>: mọi cách xếp thứ tự các phần tử; <code>{f(o, c) for o in od}</code>: tập các kết quả, mỗi kết quả chỉ ghi một lần.</p>""",
            """[2] Vì một kịch bản chưa đủ, ta liệt kê mọi thứ tự của bốn sự kiện, mỗi tiến trình đọc một lần rồi ghi một lần.
            [2.7]""", clear=True),
        stf(out(INTER_OUT),
            """[2.1] Chạy thật, có sáu thứ tự, và khi bật dấu phiên bản, mọi thứ tự đều cho một trăm tám mươi, vì không lần ghi nào dựa trên giá trị cũ.
            [2.2]""", clear=True),
        stf(table(["kiểu", "chặn đọc?", "khi tranh chấp"],
                  [["CAS (khoá lạc quan)", "không", "người ghi sau bị từ chối, tự đọc lại rồi thử lại"],
                   ["khoá bi quan (get-and-lock)", "vẫn đọc được, nhưng không ai sửa được nếu không có đúng CAS của khoá", "người khác phải chờ hết khoá"]]),
            """[1.2] Dấu phiên bản còn gọi là khoá lạc quan, không chặn ai đọc, người ghi sau bị từ chối và tự thử lại.
            [1.3]  Khoá bi quan thì người khác vẫn đọc được, nhưng không ai sửa được nếu không có đúng dấu của khoá, nên phải chờ.""",
            clear=True),
    ], checks=["alg.bnx_interleavings(True) == (6, [180])", "alg.bnx_interleavings(False) == (6, [130, 150, 180])"])
    quymo = sc("quymo", "example", "Khi số tiến trình tăng: CAS tốn bao nhiêu lần ghi, khoá bi quan chờ bao lâu", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>while chua:</code>", "lặp khi <code>chua</code> khác 0, tức còn tiến trình chưa ghi xong"],
                  ["<code>[s.get() for _ in range(chua)]</code>", "viết gọn: gọi <code>s.get()</code> đúng <code>chua</code> lần, gom kết quả vào danh sách; <code>_</code> là tên biến bỏ đi, không dùng giá trị"],
                  ["<code>for d, cas in bo:</code>", "duyệt từng cặp (nội dung, dấu) trong danh sách <code>bo</code>"],
                  ["<code>….startswith(\"từ\")</code>", "chuỗi bắt đầu bằng chữ <code>từ</code>, tức bị từ chối"]]),
           """Khối đếm dùng thêm vài cách viết, nên ta giải nghĩa trước. Vòng lặp chạy khi còn tiến trình chưa ghi xong, cách viết gọn gọi hàm đọc nhiều lần, và dấu gạch dưới là tên biến bỏ đi.""",
           clear=True),
        stf(P_SCALE.show_from("for n in", 12, title="Đếm trên chính lớp Store của bài (kho mô phỏng, không phải Couchbase thật): trường hợp xấu nhất, n tiến trình cùng đọc rồi cùng ghi, thử lại ngay, không lùi"),
            """[2] Ta đếm bằng chính lớp kho mô phỏng, không phải kho thật. Đó là trường hợp xấu nhất: n tiến trình cùng đọc rồi cùng ghi, bị từ chối thì thử lại ngay. [2.9] Mỗi vòng chỉ một tiến trình ghi khớp, những tiến trình còn lại sang vòng sau.""",
            clear=True),
        stf(P_SCALE.out_html()
            + """<p class="note">Trường hợp xấu nhất (đồng bộ, thử lại ngay, không lùi): cộng đúng n lần, không mất cập nhật nào, nhưng số lần ghi tăng nhanh hơn nhiều so với n. Thử lại có lùi ngẫu nhiên thì ít hơn.</p>""",
            """[2] Hai, hai mươi và hai trăm tiến trình tốn ba, hai trăm mười và hai mươi nghìn một trăm lần ghi. [3] Điểm cuối luôn đúng bằng n, nhưng phần lớn lần ghi bị từ chối.""",
            clear=True),
        stf(table(["số tiến trình n", "CAS: tổng lần ghi (đếm trong mô phỏng, trường hợp xấu nhất)", "CAS: số vòng", "khoá bi quan: số lần ghi", "khoá bi quan: người cuối chờ (giữ khoá 1 ms, số minh hoạ)"],
                  [["2 (×1)", "3", "2", "2", "2 ms"],
                   ["20 (×10)", "210", "20", "20", "20 ms"],
                   ["200 (×100)", "20 100", "200", "200", "200 ms"]]),
            """[1.3] Với dấu phiên bản, trường hợp xấu nhất có tổng lần ghi là n nhân n cộng một, chia hai, nên tăng theo bình phương. [1.4] Khoá bi quan chỉ cần n lần ghi, nhưng người cuối chờ n lần thời gian giữ khoá, hai trăm tiến trình chờ hai trăm mili giây.""",
            clear=True),
        stf(table(["cách", "được", "mất", "khi nào chọn"],
                  [["CAS, thử lại", "không chặn đọc; ít tranh chấp thì gần như không tốn thêm", "tranh chấp nặng thì tải ghi lên kho tăng theo bình phương", "ít tiến trình cùng sửa một bản ghi"],
                   ["khoá bi quan ngắn có thời hạn", "tải ghi tăng thẳng theo n, không ghi thừa", "người sau phải chờ; giữ lâu thì nghẽn, quên nhả thì phải đợi hết hạn", "nhiều yêu cầu cùng sửa một bản ghi nóng"],
                   ["chia nhỏ bản ghi để bớt tranh chấp", "mỗi bên ghi một bản ghi riêng, không tranh nhau", "đọc phải gom nhiều bản ghi lại", "bản ghi nóng như bộ đếm, điểm thưởng"],
                   ["phép tăng liền một bước (counter) của kho", "kho tự cộng trong một bước, không cần CAS hay khoá", "chỉ cho phép cộng trừ một số, không cho kiểm điều kiện nhiều bước", "bộ đếm thuần cộng dồn"]]),
            """[1.1] [1.2] Dấu phiên bản hợp khi ít tiến trình cùng sửa một bản ghi, vì gần như không tốn thêm. [1.3] Khoá bi quan ngắn có thời hạn hợp khi nhiều yêu cầu cùng sửa một bản ghi nóng, đổi lại người sau phải chờ. [1.4] Cách thứ ba là chia nhỏ bản ghi để bớt tranh chấp. [1.5] Nếu chỉ cộng dồn một số, kho có phép tăng liền một bước, không cần dấu phiên bản hay khoá.""",
            clear=True),
    ], checks=["[alg.bnx_l09_cas_writes(n) for n in (2, 20, 200)] == [3, 210, 20100]",
               "[alg.bnx_l09_cas_writes(n) == n * (n + 1) // 2 for n in (2, 20, 200)] == [True, True, True]",
               "[alg.bnx_l09_lock_wait_ms(n, 1) for n in (2, 20, 200)] == [2, 20, 200]"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng CAS là <b class="red">khoá</b>: đọc kèm CAS thì người khác không đọc được. Sai: CAS không chặn ai đọc, chỉ chặn ghi đè bản cũ.
<br><span class="note">Kèm theo: bắt lỗi “CAS lệch” rồi bỏ qua là mất cập nhật y như không có CAS. Phải đọc lại và thử lại, có giới hạn số lần.</span></div>""",
           """Lỗi thứ nhất, của người mới, là tưởng dấu phiên bản là một cái khoá. Sai, dấu không chặn ai đọc, chỉ chặn ghi đè bản cũ.
           Bắt lỗi dấu lệch rồi bỏ qua thì vẫn mất cập nhật y như không có dấu, nên phải đọc lại và thử lại, có giới hạn số lần."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Cập nhật bản ghi phiên (gia hạn, ghi lần truy cập) mà <b class="red">không đặt lại hạn sống</b> → hạn sống về 0, phiên <b>không bao giờ hết hạn</b>.
<br><span class="note">Cách chữa: mỗi lần ghi đặt lại hạn sống, hoặc dùng <code>preserve_expiry</code> để giữ hạn cũ. Kiểm bằng cách đọc hạn sống sau khi cập nhật.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm. Cập nhật bản ghi phiên mà không đặt lại hạn sống thì hạn sống bị đưa về không, và phiên không bao giờ hết hạn.
           Cách chữa là mỗi lần ghi đặt lại hạn sống, hoặc dùng tuỳ chọn giữ hạn cũ, rồi kiểm bằng cách đọc hạn sống sau khi cập nhật.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Để khoá ngẫu nhiên rồi mới nghĩ cách truy cập: muốn mở hồ sơ theo mã khách hàng lại phải tìm theo trường bên trong, chậm hơn nhiều so với lấy thẳng theo khoá.
<br><span class="note">Cách chữa: thiết kế khoá trước (<code>customer::&lt;mã&gt;</code>). Và kho bản ghi giữ hồ sơ, phiên; <b>sổ cái số dư</b> vẫn ở lõi ngân hàng.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, là để khoá ngẫu nhiên rồi mới nghĩ cách truy cập. Khi đó mở hồ sơ theo mã khách hàng phải tìm theo trường bên trong, chậm hơn nhiều so với lấy thẳng theo khoá.
           Cách chữa là thiết kế khoá trước. Kho bản ghi giữ hồ sơ và phiên, còn sổ cái số dư vẫn ở lõi ngân hàng.""",
           clear=True),
    ], checks=["alg.bnx_ttl_after_mutation(1800, False) == 0"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "CRC32 của một khoá ra 1 000 000 000 (số minh hoạ). Có 1024 thùng ảo, khoá vào thùng nào (cách của thư viện Java)?"],
                   ["2", "Hồ sơ 200 điểm, CAS 12. P1 trừ 40, P2 cộng 25, cùng đọc trước; P1 ghi trước. Kết quả có CAS? Không có CAS?"],
                   ["3", "Quyết định: cập nhật “hạn mức đã dùng trong ngày” của một khách, nếu 200 yêu cầu của khách đó đến cùng lúc (số minh hoạ). Dùng CAS hay khoá bi quan?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.4] Câu ba chọn dấu phiên bản hay khoá bi quan cho hạn mức, nếu hai trăm yêu cầu đến cùng lúc. [0] Hãy dừng video và làm ra giấy.""",
            pause=25),
        st("""<p>Câu 1: chia nguyên cho 65 536 được 15 258; số này nhỏ hơn 32 768 nên lấy dư vẫn là 15 258.</p>
$$15\\,258 - 14 \\cdot 1\\,024 = 15\\,258 - 14\\,336 = \\hlg{922}$$""",
           """Đáp án câu một. Một tỉ chia nguyên cho sáu mươi lăm nghìn năm trăm ba mươi sáu được mười lăm nghìn hai trăm năm mươi tám, nhỏ hơn ba mươi hai nghìn bảy trăm sáu mươi tám.
           Lấy dư cho một nghìn không trăm hai mươi tư thì còn chín trăm hai mươi hai. Khoá vào thùng ảo chín trăm hai mươi hai.""",
           focus=[1, 1, 2, 2]),
        stf("""<p>Câu 2: P1 ghi $200 - 40 = 160$, CAS thành 13; P2 gửi CAS 12 → từ chối, đọc lại 160.</p>
$$\\text{có CAS: } 160 + 25 = \\hlg{185}, \\qquad \\text{không CAS: } 200 + 25 = \\hl{225}$$""",
            """[1] Đáp án câu hai. Tiến trình một ghi hai trăm trừ bốn mươi, bằng một trăm sáu mươi, dấu thành mười ba.
            [2] Có dấu thì một trăm sáu mươi cộng hai mươi lăm bằng một trăm tám mươi lăm. Không có dấu thì hai trăm hai mươi lăm, mất phần trừ bốn mươi."""),
        stf(table(["lựa chọn", "được", "mất"],
                  [["CAS (lạc quan)", "không chặn đọc; ít tranh chấp thì gần như không tốn thêm", "tranh chấp nặng thì bị từ chối nhiều lần, phải thử lại có giới hạn"],
                   ["khoá bi quan", "người giữ khoá chắc chắn ghi được", "người khác phải chờ; khoá phải có thời hạn, giữ lâu thì nghẽn"]])
            + """<div class="box key">Hạn mức có nhiều yêu cầu cùng lúc và phải kiểm điều kiện rồi mới ghi: chọn <b>khoá bi quan ngắn, có thời hạn</b>, vì nếu 200 yêu cầu đến cùng lúc, CAS bị từ chối nhiều lần (bảng ở cảnh quy mô). Nếu chỉ cộng dồn một số, ưu tiên <b>phép tăng liền một bước</b> của kho.</div>""",
            """[1.2] Đáp án câu ba. Dấu phiên bản không chặn đọc nhưng bị từ chối nhiều lần khi tranh chấp nặng. [1.3] Khoá bi quan cho người giữ khoá chắc chắn ghi được, đổi lại người khác phải chờ.
            [2] Vậy với hạn mức phải kiểm điều kiện rồi mới ghi, nếu hai trăm yêu cầu đến cùng lúc, nên chọn khoá bi quan ngắn có thời hạn. """),
    ], checks=["10**9 // 65536 == 15258 < 32768 and 15258 - 14 * 1024 == 922 == alg.bnx_vbucket_of_crc(10**9)",
               "alg.bnx_cas_story(200, 12, (('P1', -40), ('P2', 25)))[:2] == (185, 14)",
               "alg.bnx_cas_story(200, 12, (('P1', -40), ('P2', 25)), use_cas=False)[0] == 225"])
    lab_pr = practice_scene(sc, "Tự làm: tính thùng ảo và chạy lại hai tiến trình có CAS", practice_steps2(
        st, "BNX", "L09",
        """<p><b>Đề</b>: viết <code>mau.py</code> (Python, chỉ thư viện chuẩn):</p>
<ol><li>khoá <code>session::s77</code>: tính <code>r = (crc32 &gt;&gt; 16) &amp; 0x7FFF</code> rồi in thùng ảo <code>r % 1024</code> và <code>r % 128</code></li>
<li>hồ sơ <b>300</b> điểm, CAS <b>4</b>; P1 cộng 20, P2 trừ 50, cả hai đọc trước khi ai ghi. Viết hàm <code>ghi(moi, cas_kem)</code> (đặt tên không dấu): lệch CAS thì trả <code>tu choi</code>, khớp thì lưu và tăng CAS thêm 1</li>
<li>P1 ghi; P2 ghi (bị từ chối); P2 đọc lại, trừ 50 lần nữa rồi ghi lần hai; in giá trị và CAS cuối</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; chữ in ra phải đúng từng ký tự như kết quả mong đợi.</p>""",
        """Bây giờ tới phần bạn tự làm. Tính thùng ảo của khoá phiên với một nghìn không trăm hai mươi tư thùng và một trăm hai mươi tám thùng. Rồi dựng hàm ghi có dấu phiên bản, cho hồ sơ ba trăm điểm, hai tiến trình cùng đọc trước. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> hàm <code>ghi</code> so <code>cas_kem != cas</code> trước; khớp thì gán giá trị mới và <code>cas + 1</code>. Tiến trình hai bị từ chối thì phải đọc lại giá trị và CAS hiện tại.
Lời giải đầy đủ ở <code>labs/BNX/L09/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hàm ghi so dấu gửi kèm với dấu hiện tại trước, khớp thì lưu giá trị mới và tăng dấu thêm một. Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L09")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("khoá customer::C1001", "CRC32 → thùng ảo 351", "bản đồ cụm → máy", "ghi kèm CAS: lệch thì đọc lại", "180, không mất điểm"),
           """ Khoá bản ghi được băm ra thùng ảo ba trăm năm mươi mốt, bản đồ cụm chỉ ra máy giữ thùng đó.
           Mỗi lần ghi mang theo dấu phiên bản, lệch thì đọc lại rồi ghi, nên kết quả là một trăm tám mươi điểm, không mất cập nhật."""),
        st("""<div class='box key'><b>Tư duy:</b> thiết kế <b>khoá trước</b>, vì đó là cách truy cập chính. Mỗi lần “đọc, sửa, ghi” phải mang CAS. Bản ghi phiên luôn có hạn sống, và hạn sống phải được đặt lại mỗi lần ghi.</div>""",
           """Điều cần mang theo. Thiết kế khoá trước, vì đó là cách truy cập chính. Mỗi lần đọc, sửa, ghi phải mang dấu phiên bản. Bản ghi phiên luôn có hạn sống, và phải đặt lại mỗi lần ghi."""),
        st("""<p>Bài sau: Kafka giữ bản cuối của mỗi khoá trong nhật ký, kiểm lược đồ trước khi bên gửi đổi, và một hàng đợi khác định tuyến theo mẫu chủ đề.</p>""",
           """Bài sau học Kafka nâng cao: nén nhật ký theo khoá, kiểm lược đồ và định tuyến theo mẫu.""",
           forward_ref=True),
    ])
    return lesson("L09", "couchbase_vbucket_cas", "Bài 9 — Couchbase: bản ghi theo khoá, vBucket và giá trị CAS chống ghi đè",
                  "curriculum/bnx.yaml L09; audit/bnx/verify_bnx.py L09; Couchbase Server docs 8.0 (đọc 2026-11-11): vBuckets, Expiration, "
                  "Manage Expiration (Mutation's Effect on Expiration); Couchbase Java SDK 3.13 docs: Concurrent Document Mutations",
                  ["Thiết kế khoá bản ghi cho hồ sơ khách hàng", "Tính vBucket của một khoá", "Dùng giá trị CAS để chặn mất cập nhật",
                   "Đặt hạn sống cho bản ghi phiên", "So sánh tổng số lần ghi của CAS với khoá bi quan khi số tiến trình tranh chấp tăng 2, 20, 200"],
                  [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec],
                  covers=[(1, "formula"), (2, "formula"), (3, "example"), (4, "formula"), (5, "quymo")])


LAB_DE = """# Lab BNX L09 — Thùng ảo của một khoá và ghi có dấu phiên bản CAS (kho mô phỏng bằng Python, không cần Couchbase)

Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`:

1. Khoá `session::s77`: `r = (zlib.crc32(khoa.encode()) >> 16) & 0x7FFF`. In `thung ao (1024): <r % 1024> | (128): <r % 128>`.
2. Hồ sơ 300 điểm, CAS 4. Hàm `ghi(moi, cas_kem)`: nếu `cas_kem` khác CAS hiện tại thì trả `tu choi`; khớp thì lưu giá trị mới, tăng CAS thêm 1 và trả `ghi duoc, CAS moi = <số>`.
3. P1 (cộng 20) và P2 (trừ 50) cùng đọc (300, CAS 4) trước khi ai ghi. In `P1: <kết quả ghi>`, `P2: <kết quả ghi>`. Rồi P2 đọc lại giá trị và CAS hiện tại, trừ 50 lần nữa và ghi lần hai: in `P2 lan 2: <kết quả ghi>`.
4. In `cuoi: <giá trị> <CAS>`.

Đặt tên biến và hàm không dấu. Gợi ý cú pháp: `import zlib` nạp thư viện băm; `s.encode()` đổi chữ thành byte; `"... %d" % x` chèn số `x` vào chỗ `%d`; từ khoá `global` cho hàm sửa biến ngoài hàm. Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L09 mau.py`.
"""

# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L09", LAB_DE, "py", LAB_PY, LAB_OUT)
