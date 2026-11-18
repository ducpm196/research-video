import re

import lib2
from lib2 import *

lib2.begin("L08")

# ── Mã hiện trên màn hình (chạy nguyên văn: audit/bnx/screen/l08.yaml, audit/bnx/ver/l08.py) ──
INV_PY = """
docs = {"d1": "chuyển tiền napas", "d2": "nạp tiền ví",
        "d3": "chuyển tiền quốc tế", "d4": "rút tiền atm"}
index = {}
for doc_id, text in docs.items():
    for word in text.split():
        index.setdefault(word, set()).add(doc_id)
for word in ["tiền", "chuyển", "napas"]:
    print(word, sorted(index[word]))
both = index["chuyển"] & index["napas"]
print("chuyển và napas:", sorted(both))
"""

ROUTE_PY = """
def shard(h, n_primary):
    return h % n_primary      # mảnh = băm mod số mảnh chính
print("h = 17:", shard(17, 3), "->", shard(17, 4))
same = [h for h in range(12) if shard(h, 3) == shard(h, 4)]
print("giữ mảnh:", same, len(same), "/ 12")
"""

CRC_PY = """
import zlib
def shard(doc_id, n):         # băm minh hoạ: CRC32
    return zlib.crc32(doc_id.encode()) % n
ids = [f"tx{i}" for i in range(1, 1201)]
stay = sum(shard(d, 3) == shard(d, 4) for d in ids)
print(stay, "/", len(ids), "=", round(stay / len(ids), 3))
split = all(shard(d, 6) % 3 == shard(d, 3) for d in ids)
print("tách 3 -> 6, mảnh mới nằm trong mảnh cũ:", split)
"""

REFRESH_PY = """
buffer, searchable = [], []
def write(doc):
    buffer.append(doc)
def refresh():                # mặc định mỗi 1 giây
    searchable.extend(buffer)
    buffer.clear()
def search(word):
    return [d for d in searchable if word in d.split()]
write("chuyển tiền napas")
print("ngay sau khi ghi:", search("napas"))
refresh()
print("sau lần làm tươi:", search("napas"))
"""

# Đầu ra THẬT: prog() chạy nguyên văn (Python 3.13, thư mục tạm) lúc import; sổ mã sinh bằng lib2.py gen-screen L08.
P_INV = prog("Inv", INV_PY, lang="python")
P_ROUTE = prog("Route", ROUTE_PY, lang="python")
P_CRC = prog("Crc", CRC_PY, lang="python")
P_REFRESH = prog("Refresh", REFRESH_PY, lang="python")
INV_OUT, ROUTE_OUT, CRC_OUT, REFRESH_OUT = P_INV.out, P_ROUTE.out, P_CRC.out, P_REFRESH.out

# Cảnh quy mô: số đo thật (đếm, tất định) ở ba mức ×1, ×100, ×1000 — mô phỏng cơ chế bằng Python, KHÔNG phải Elasticsearch thật.
QM_SEARCH_PY = """
for n in (1200, 120000, 1200000):
    mo_ta = [("chuyen tien napas" if i % 1000 == 0
              else "chuyen tien the") for i in range(n)]
    chi_muc = {}
    for i, m in enumerate(mo_ta):
        for tu in m.split():
            chi_muc.setdefault(tu, []).append(i)
    print(n, "mo ta: quet doc", n, "mo ta, chi muc doc",
          len(chi_muc["napas"]), "dong")
"""
QM_ROUTE_PY = """
import zlib
def manh(i, n):
    return zlib.crc32(f"tx{i}".encode()) % n
for n in (1200, 120000, 1200000):
    doi = sum(manh(i, 3) != manh(i, 4) for i in range(n))
    print(n, "ban ghi: doi 3 -> 4 manh", doi, "=", round(100 * doi / n), "%")
"""
P_QM_SEARCH = prog("QmSearch", QM_SEARCH_PY, lang="python", timeout=300)
P_QM_ROUTE = prog("QmRoute", QM_ROUTE_PY, lang="python", timeout=300)
LAB_PY = """
docs = {"a1": "rut tien atm", "a2": "chuyen tien the",
        "a3": "chuyen khoan napas", "a4": "nap tien the"}
chi_muc = {}
for ma, mo_ta in docs.items():
    for tu in mo_ta.split():
        chi_muc.setdefault(tu, set()).add(ma)
for tu in ["tien", "the", "chuyen"]:
    print(tu + ":", *sorted(chi_muc[tu]))
print("chuyen va the:", *sorted(chi_muc["chuyen"] & chi_muc["the"]))
print("manh cua 29, 41, 50 voi 5 manh chinh:", *[h % 5 for h in (29, 41, 50)])
giu = sum(h % 4 == h % 6 for h in range(12))
print("doi 4 -> 6 manh chinh: giu manh", giu, "/ 12")
"""
LAB_OUT = """tien: a1 a2 a4
the: a2 a4
chuyen: a2 a3
chuyen va the: a2
manh cua 29, 41, 50 voi 5 manh chinh: 4 1 0
doi 4 -> 6 manh chinh: giu manh 4 / 12"""

DOCS = {"d1": "chuyển tiền napas", "d2": "nạp tiền ví", "d3": "chuyển tiền quốc tế", "d4": "rút tiền atm"}
_D = repr(DOCS)
FR = "__import__('fractions').Fraction"


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
    hook = sc("hook", "hook", "Vì sao vừa chuyển tiền xong mà tìm trong lịch sử chưa thấy?", [
        stf("""<p>9 giờ đúng, khách chuyển $500\\,000$ đồng qua NAPAS (hệ thống chuyển tiền giữa các ngân hàng ở Việt Nam). Giao dịch được ghi ngay vào cụm tìm kiếm Elasticsearch (phần mềm máy tìm kiếm chạy trên nhiều máy).</p>
<p>Chưa tới một giây sau, khách mở <b>lịch sử giao dịch</b>, gõ “napas”: <b class="red">có thể chưa thấy</b>.</p>
<div class="box key">Nhiều nhất một giây sau gõ lại thì thấy (độ trễ từ 0 đến 1 giây, tuỳ lần làm tươi tới lúc nào). Tiền không mất: bản ghi chỉ <b>chưa tìm được</b>, vì chưa tới <b>lần làm tươi</b> (lần máy mở phần vừa ghi cho việc tìm).</div>""",
            """[1] Chào bạn, chín giờ đúng, khách chuyển năm trăm nghìn đồng qua NAPAS, tức hệ thống chuyển tiền giữa các ngân hàng trong nước. Giao dịch được ghi ngay vào cụm máy tìm kiếm.
            [2] Chưa tới một giây sau, khách mở lịch sử giao dịch và tìm chữ NAPAS, và có thể chưa thấy gì.
            [3] Một giây sau tìm lại thì thấy, độ trễ từ không đến một giây. Tiền không mất, bản ghi chỉ chưa tìm được, vì chưa tới lần làm tươi, tức lần máy mở phần vừa ghi cho việc tìm.""", introduces=["bnx_lam_tuoi"]),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["tìm “chuyển tiền napas” trong hàng triệu mô tả thế nào cho nhanh", "<b>chỉ mục ngược</b>: từ → danh sách bản ghi chứa từ đó"],
                   ["bản ghi nằm ở mảnh nào, vì sao không đổi được số mảnh", "băm rồi chia dư cho số <b>mảnh chính</b> (số phần chia của chỉ mục)"],
                   ["vì sao ghi xong chưa tìm thấy ngay", "làm tươi định kỳ, mặc định 1 giây"],
                   ["có giữ số dư ở đây được không", "không: không có giao dịch nhiều bản ghi"]]),
            """[1.2] Tìm cụm từ trong hàng triệu mô tả cho nhanh thì dùng chỉ mục ngược, tức bảng ghi từ nào nằm ở bản ghi nào.
            [1.3] Bản ghi nằm ở mảnh nào thì tính bằng băm rồi chia dư cho số mảnh chính. [1.4] Ghi xong chưa thấy ngay là do làm tươi định kỳ, mặc định mỗi giây.
            [1.5] Giữ số dư ở đây thì không được, vì không có giao dịch gồm nhiều bản ghi.""", introduces=["bnx_chi_muc_nguoc", "bnx_manh_chinh"], clear=True),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Mục lục cuối sách", "mỗi từ khoá trỏ tới các trang có từ đó, nên không phải lật từng trang", "“lãi suất” → trang 12, 40"],
                   ["② Băm rồi chia dư", "hàm băm biến khoá thành một số, cùng khoá luôn ra cùng số; lấy số dư khi chia để chọn ngăn", "17 chia 3 dư 2 → ngăn 2"],
                   ["③ Giao dịch cơ sở dữ liệu", "nhiều thay đổi cùng thành công hoặc cùng huỷ", "trừ A 500 000 và cộng B 500 000 cùng chốt"],
                   ["④ Điểm liên quan", "xếp kết quả: bản ghi chứa từ hiếm, chứa từ nhiều lần thì đứng trên", "bài này chỉ nhắc, không đi sâu"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Mục lục cuối sách cho mỗi từ khoá trỏ tới các trang có từ đó, nên ta không phải lật từng trang.
            [1.3] Băm rồi chia dư là cách chọn ngăn cho một khoá. Hàm băm biến khoá thành một số, cùng khoá luôn ra cùng số, rồi lấy số dư để chọn ngăn.
            [1.4] Giao dịch cơ sở dữ liệu là nhiều thay đổi cùng thành công hoặc cùng huỷ. [1.5] Điểm liên quan dùng để xếp kết quả, bản ghi chứa từ hiếm hoặc nhiều lần thì đứng trên.""", introduces=["bnx_giao_dich_csdl"]),
        st("""$$17 = 5 \\cdot 3 + 2$$""",
           """Một ví dụ số cho phép chia dư. Mười bảy bằng năm nhân ba cộng hai, nên mười bảy chia ba dư hai, và khoá đó vào ngăn số hai."""),
    ], checks=["17 == 5 * 3 + 2 and alg.bnx_shard(17, 3) == 2"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["document (bản ghi)", "một bản ghi dạng JSON (các cặp <code>tên: giá trị</code> trong ngoặc nhọn), ví dụ <code>{\"_id\": \"tx1001\", \"mo_ta\": \"chuyển tiền napas\"}</code>"],
                   ["index (chỉ mục)", "tập bản ghi cùng loại, giống một bảng"],
                   ["inverted index (chỉ mục ngược)", "từ → danh sách bản ghi chứa từ đó"],
                   ["primary shard (mảnh chính)", "một phần của chỉ mục; mỗi bản ghi thuộc đúng một mảnh chính"],
                   ["replica (bản sao)", "bản chép của mảnh chính: phục vụ đọc, thay khi hỏng; khác máy với mảnh chính"],
                   ["<code>_routing</code> (khoá định tuyến)", "giá trị đem băm để chọn mảnh; mặc định là <code>_id</code>"],
                   ["refresh (làm tươi)", "mở phần vừa ghi cho việc tìm; mặc định mỗi 1 giây"]]),
            """Bảng này giải mã bảy từ. [1.2] Bản ghi là một chuỗi chữ dạng JSON, ghi các cặp tên trường và giá trị trong ngoặc nhọn. [1.3] Chỉ mục là tập các bản ghi cùng loại, giống một bảng.
            [1.4] Chỉ mục ngược đi từ từ sang danh sách bản ghi chứa từ đó. [1.5] Mảnh chính là một phần của chỉ mục, mỗi bản ghi thuộc đúng một mảnh chính.
            [1.6] Bản sao là bản chép của mảnh chính, phục vụ đọc và thay khi hỏng, nên không đặt cùng máy với mảnh chính của nó.
            [1.7] Khoá định tuyến là giá trị đem băm để chọn mảnh. [1.8] Làm tươi là mở phần vừa ghi cho việc tìm, mặc định mỗi giây."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: chỉ mục ngược, mảnh trên các máy và lần làm tươi", [
        st(svg(1500, 470,
               txt(250, 40, "4 mô tả giao dịch", 26, bold=True),
               box(40, 70, 420, 70, "d1: chuyển tiền napas", C_BLUE, size=24),
               box(40, 160, 420, 70, "d2: nạp tiền ví", C_BLUE, size=24),
               box(40, 250, 420, 70, "d3: chuyển tiền quốc tế", C_BLUE, size=24),
               box(40, 340, 420, 70, "d4: rút tiền atm", C_BLUE, size=24),
               arrow(470, 240, 640, 240, "#475569", "tách từ"),
               txt(1030, 40, "chỉ mục ngược: từ → bản ghi", 26, bold=True),
               box(660, 70, 740, 70, "tiền → d1, d2, d3, d4", C_AMBER, size=24),
               box(660, 160, 740, 70, "chuyển → d1, d3", C_AMBER, size=24),
               box(660, 250, 740, 70, "napas → d1", C_AMBER, size=24),
               box(660, 340, 740, 70, "nạp → d2   …", C_AMBER, size=24),
               txt(750, 455, "Tìm “chuyển” và “napas”: lấy phần chung của hai danh sách → d1", 26, "middle", "#16a34a", True)),
           """Máy tách mỗi mô tả thành từng từ, rồi ghi ngược lại, mỗi từ trỏ tới các bản ghi chứa nó.

           Muốn tìm cả hai chữ chuyển và NAPAS, máy lấy phần chung của hai danh sách, ra d một, mà không đọc lại mô tả nào."""),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>docs = {&quot;d1&quot;: &quot;…&quot;, …}</code>", "<b>từ điển</b>: bảng ghi mỗi khoá một giá trị, ở đây mã bản ghi → mô tả"],
                  ["<code>for doc_id, text in docs.items():</code>", "duyệt từng cặp khoá và giá trị"],
                  ["<code>index.setdefault(word, set()).add(doc_id)</code>", "lấy <b>tập</b> của <code>word</code> (tập: nhóm giá trị không trùng), chưa có thì tạo tập rỗng, rồi thêm <code>doc_id</code> vào"],
                  ["<code>text.split()</code>", "tách chuỗi <code>text</code> thành danh sách từ, cắt ở khoảng trắng: <code>\"nạp tiền ví\".split()</code> là <code>[\"nạp\", \"tiền\", \"ví\"]</code>"],
                  ["<code>a &amp; b</code>, <code>sorted(…)</code>", "giao hai tập, tức phần chung; xếp theo thứ tự"]]),
           """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Từ điển là bảng ghi mỗi khoá một giá trị, vòng lặp duyệt từng cặp, và hàm tách cắt chuỗi thành các từ.
           Tập là nhóm giá trị không trùng, và dấu và lấy phần chung của hai tập.""", clear=True),
        stf(code(INV_PY, "Dựng chỉ mục ngược bằng Python"),
            """[2] Chương trình Python dựng đúng chỉ mục đó. [2.4] Vòng lặp ngoài đi qua từng bản ghi. [2.6] Vòng lặp trong đi qua từng từ, và thêm mã bản ghi vào tập của từ ấy.
            [2.9] Dòng gần cuối lấy phần chung của hai tập, bằng dấu và trong Python.""",
            clear=True),
        stf(out(INV_OUT),
            """[2.1] Chạy thật thì chữ tiền ra bốn bản ghi. [2.2] Chữ chuyển ra hai bản ghi, là d một và d ba. [2.3] Còn chữ NAPAS chỉ ra một bản ghi. [2.4] Phép giao của hai tập cho đúng một bản ghi, là d một.""",
            clear=True),
        st(svg(1500, 470,
               box(40, 30, 520, 80, ["bản ghi tx1001", "băm minh hoạ = 17"], C_PURPLE, size=24),
               arrow(560, 70, 760, 70, "#9333ea", "17 chia 3 dư 2"),
               box(780, 30, 300, 80, "mảnh chính P2", C_GREEN, size=24, bold=True),
               panel(40, 160, 460, 270, "Máy 1", C_GRAY),
               box(80, 230, 380, 70, "P0 (chính)", C_GREEN, size=24), box(80, 320, 380, 70, "R2 (bản sao của P2)", C_BLUE, size=24),
               panel(520, 160, 460, 270, "Máy 2", C_GRAY),
               box(560, 230, 380, 70, "P1 (chính)", C_GREEN, size=24), box(560, 320, 380, 70, "R0 (bản sao của P0)", C_BLUE, size=24),
               panel(1000, 160, 460, 270, "Máy 3", C_GRAY),
               box(1040, 230, 380, 70, "P2 (chính)", C_GREEN, size=24), box(1040, 320, 380, 70, "R1 (bản sao của P1)", C_BLUE, size=24),
               arrow(1080, 112, 1180, 225, "#16a34a"),
               txt(750, 462, "3 mảnh chính + 3 bản sao = 6 mảnh; bản sao không nằm cùng máy với mảnh chính của nó", 24, "middle", "#1f2937", True)),
           """Hình thứ hai cho thấy chỉ mục chia thành ba mảnh chính, đặt trên ba máy. Bản ghi mã một nghìn không trăm linh một có giá trị băm minh hoạ là mười bảy.
           Mười bảy chia ba dư hai, nên bản ghi vào mảnh chính số hai, nằm ở máy ba. Mỗi mảnh chính có một bản sao ở máy khác, nên khi máy ba hỏng, bản sao ở máy một được nâng lên thay.
"""),
        st(svg(1500, 420,
               arrow(60, 200, 1440, 200, "#475569"),
               txt(1440, 245, "thời gian", 22, "end"),
               txt(160, 245, "0 s", 22), txt(570, 245, "0,5 s", 22), txt(870, 170, "1 s", 22), txt(1150, 245, "1,2 s", 22),
               box(30, 60, 260, 80, "ghi bản ghi", C_BLUE, size=24),
               box(420, 60, 300, 80, ["tìm “napas”", "không thấy"], C_RED, size=22),
               box(740, 280, 260, 80, "làm tươi", C_AMBER, size=24, bold=True),
               box(1000, 60, 300, 80, ["tìm “napas”", "thấy d1"], C_GREEN, size=22),
               arrow(160, 140, 160, 190), arrow(570, 140, 570, 190), arrow(870, 275, 870, 210), arrow(1150, 140, 1150, 190),
               txt(750, 405, "Ghi xong nằm ở vùng đệm; chỉ sau lần làm tươi (mặc định 1 giây) mới tìm được, độ trễ từ 0 tới 1 giây", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là trục thời gian. Ở giây không, bản ghi mới nằm trong vùng đệm, và ở giây không phẩy năm lượt tìm chưa thấy nó.
           Tới giây thứ một, lần làm tươi mở phần vừa ghi cho việc tìm, nên ở giây một phẩy hai, lượt tìm đã thấy d một. Độ trễ nằm từ không tới một giây."""),
    ], checks=[f"alg.bnx_inverted_index({_D})['tiền'] == ['d1', 'd2', 'd3', 'd4']",
               f"alg.bnx_inverted_index({_D})['chuyển'] == ['d1', 'd3']",
               f"alg.bnx_search_and({_D}, 'chuyển', 'napas') == ['d1']",
               "alg.bnx_shard(17, 3) == 2", "alg.bnx_total_shards(3, 1) == 6",
               "alg.bnx_refresh_sim([(0, 'd1')], [0.5, 1.2]) == [0, 1]"])
    form = sc("formula", "formula", "Suy ra từng bước: bản ghi nằm ở đâu, và vì sao chưa thấy ngay", [
        stf("""<p><b>Bước 1.</b> Mọi máy phải tự tính ra mảnh của một bản ghi mà không tra bảng lớn, nên dùng một công thức cố định:</p>
$$\\text{mảnh} = \\text{băm}(\\text{khoá định tuyến}) \\text{ mod } \\text{số mảnh chính}$$
<span class='note'>Làm thử: băm = 17, có 3 mảnh chính → 17 mod 3 = 2. Bài dùng băm minh hoạ; hàm băm thật của Elasticsearch là murmur3, không phải hàm này. Công thức này cho chỉ mục tạo từ bản 9.4; chỉ mục cũ hơn thêm một bước chia, nhưng vẫn phụ thuộc số mảnh chính.</span>""",
            """[1] Bước một, vì mọi máy phải tự tính ra mảnh mà không tra bảng lớn, nên ta dùng công thức cố định.
            [2] Mảnh bằng giá trị băm của khoá định tuyến, chia lấy dư cho số mảnh chính. Ba chữ m o d là viết tắt của phép lấy số dư.
            [3] Làm thử, băm ra mười bảy, có ba mảnh chính, thì mười bảy chia ba dư hai. """),
        stf("""<p><b>Bước 2.</b> Mỗi mảnh chính có thêm một số bản sao, nên</p>
$$\\text{tổng số mảnh} = \\text{số mảnh chính} \\cdot (1 + \\text{số bản sao})$$
<p class='note'>Làm thử: $3 \\cdot (1 + 1) = 6$.</p>""",
            """[2] Bước hai, vì mỗi mảnh chính còn có thêm các bản sao của nó, nên tổng số mảnh bằng số mảnh chính nhân với một cộng số bản sao.
            Dấu chấm ở giữa là phép nhân. [3] Làm thử, ba nhân với một cộng một, bằng sáu."""),
        stf("""<p><b>Bước 3.</b> Công thức chia cho số mảnh chính, nên đổi số này thì số dư đổi theo:</p>
$$17 \\text{ mod } 4 = 1 \\neq 2$$
<span class='note'>Bản ghi đang nằm ở mảnh 2, nhưng lấy, sửa, xoá theo mã thì máy tới thẳng mảnh 1, nên không thấy. Vì vậy số mảnh chính chỉ đặt được lúc tạo chỉ mục.</span>""",
            """[1] Bước ba, vì công thức chia cho số mảnh chính, nên đổi số này thì số dư cũng đổi. [2] Mười bảy chia bốn dư một, khác hai.
            [3] Bản ghi đang ở mảnh hai, nhưng khi lấy theo mã, máy tới thẳng mảnh một, nên không thấy. Vì vậy số mảnh chính chỉ đặt được lúc tạo chỉ mục.""",
            clear=True),
        stf(code(ROUTE_PY, "Bước 4. Đếm bao nhiêu giá trị băm giữ nguyên mảnh") + out(ROUTE_OUT)
            + """<p class="note"><code>def shard(h, n): return h % n</code>: định nghĩa hàm nhận <code>h</code>, <code>n</code>; <code>return</code> trả kết quả ra. <code>h % n</code>: số dư khi chia <code>h</code> cho <code>n</code>. <code>[h for h in range(12) if …]</code>: cách viết gọn, giữ những <code>h</code> từ 0 tới 11 thoả điều kiện.</p>""",
            """[1] Bước bốn, hàm nhận giá trị băm và số mảnh rồi trả số dư. Số dư khi chia ba và khi chia bốn lặp lại sau mỗi mười hai giá trị, vì mười hai là số nhỏ nhất chia hết cho cả ba và bốn.
            [2.4] Nên chỉ cần đếm mười hai giá trị. [4.2] Chạy thật, chỉ có không, một và hai là giữ nguyên mảnh, tức ba trên mười hai.""",
            clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>buffer, searchable = [], []</code>", "gán hai danh sách rỗng một lúc: vùng đệm và phần đã mở cho việc tìm"],
                  ["<code>append(x)</code>, <code>extend(l)</code>, <code>clear()</code>", "thêm <code>x</code> vào cuối danh sách; thêm cả danh sách <code>l</code>; làm rỗng"],
                  ["<code>word in d.split()</code>", "<code>d.split()</code> là danh sách từ của <code>d</code>; đúng khi <code>d</code> có đúng từ <code>word</code>"]]),
           """Mô phỏng sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Hai danh sách rỗng là vùng đệm và phần đã mở. Ba hàm thêm vào cuối, thêm cả danh sách và làm rỗng. Bản ghi khớp khi có đúng từ cần tìm.""", clear=True),
        stf(code(REFRESH_PY, "Bước 5. Mô phỏng làm tươi"),
            """[2.3] Bước năm, vì bản ghi mới chỉ vào vùng đệm, còn lượt tìm chỉ đọc phần đã mở, nên phải có bước làm tươi.
            [2.4] [2.9] Ta ghi một bản ghi, tìm ngay, làm tươi, rồi tìm lại. """,
            clear=True),
        stf(out(REFRESH_OUT, "Bước 5. Kết quả chạy thật"),
            """[2.1] Chạy thật, ngay sau khi ghi thì kết quả rỗng, vì bản ghi còn nằm trong vùng đệm. [2.2] Sau một lần làm tươi thì tìm thấy bản ghi chuyển tiền NAPAS.""",
            clear=True),
    ], checks=["alg.bnx_shard(17, 3) == 2", "alg.bnx_total_shards(3, 1) == 6", "alg.bnx_shard(17, 4) == 1",
               "alg.bnx_keep_cycle(3, 4)[:2] == (3, 12)", "alg.bnx_refresh_sim([(0, 'd1')], [0.0, 1.0]) == [0, 1]"])
    ex = sc("example", "example", "Ví dụ chỉ mục giao dịch, từng phép tính", [
        st("""<p>Chỉ mục giao dịch có 3 mảnh chính, mỗi mảnh 1 bản sao; chứa $1\\,200\\,000$ bản ghi (số minh hoạ).</p>
$$① \\; 3 \\cdot (1 + 1) = \\hl{6}\\ \\text{mảnh}$$""",
           """Chỉ mục giao dịch có ba mảnh chính, mỗi mảnh một bản sao, và chứa một triệu hai trăm nghìn bản ghi, đây là số minh hoạ.
           Phép tính thứ nhất, tổng số mảnh bằng ba nhân với một cộng một, tức sáu mảnh.""", focus=[1, 1, 2]),
        st("""<p>Bản ghi tx1001 có băm minh hoạ 17.</p>
$$② \\; 17 \\text{ mod } 3 = \\hlg{2}\\ \\text{(mảnh chính P2)}$$""",
           """Phép tính thứ hai, bản ghi mã một nghìn không trăm linh một có giá trị băm minh hoạ mười bảy. Mười bảy chia ba dư hai, nên nó nằm ở mảnh chính số hai.""",
           focus=[1, 2]),
        st("""<p>Nếu đổi thành 4 mảnh chính:</p>
$$③ \\; 17 \\text{ mod } 4 = \\hl{1} \\neq 2$$""",
           """Phép tính thứ ba, nếu đổi thành bốn mảnh chính, thì mười bảy chia bốn dư một, khác với hai ở phép thứ hai. Vậy máy sẽ tìm nhầm mảnh.""",
           focus=[2, 2]),
        st("""<p>Trên một vòng 12 giá trị băm, giá trị giữ mảnh là 0, 1, 2:</p>
$$④ \\; \\frac{3}{12} = \\hlg{25\\%}\\ \\text{giữ mảnh cũ}$$""",
           """Phép tính thứ tư, trên một vòng mười hai giá trị băm, chỉ ba giá trị giữ mảnh cũ. Ba trên mười hai bằng hai mươi lăm phần trăm.""",
           focus=[1, 2], clear=True),
        st("""<p>Dùng lại $25\\%$ ở phép ④ và $1\\,200\\,000$ bản ghi.</p>
$$⑤ \\; (100\\% - 25\\%) \\cdot 1\\,200\\,000 = \\hl{900\\,000}\\ \\text{bản ghi phải chuyển mảnh}$$
<div class="box key">Không sửa tại chỗ được: phải <b>tạo chỉ mục mới</b> 4 mảnh chính rồi <b>chép lại</b> (reindex).</div>""",
           """Phép tính thứ năm, dùng lại hai mươi lăm phần trăm của phép thứ tư. Còn bảy mươi lăm phần trăm phải chuyển, nhân một triệu hai trăm nghìn, là chín trăm nghìn bản ghi.
           Vì gần như mọi bản ghi phải dời chỗ, nên phải tạo chỉ mục mới rồi chép lại toàn bộ.""",
           focus=[1, 2, 3]),
    ], checks=["alg.bnx_total_shards(3, 1) == 6", "alg.bnx_shard(17, 3) == 2", "alg.bnx_shard(17, 4) == 1",
               f"alg.bnx_keep_cycle(3, 4) == (3, 12, {FR}(1, 4))",
               "(1 - alg.bnx_keep_cycle(3, 4)[2]) * 1200000 == 900000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: băm CRC32 (minh hoạ) trên 1 200 mã", [
        stf(code(CRC_PY, "Đường khác: băm CRC32 cho 1 200 mã giao dịch") + out(CRC_OUT)
            + """<p class="note"><code>f"tx{i}"</code>: <code>{i}</code> thay bằng giá trị của <code>i</code>. <code>zlib.crc32(x.encode())</code>: băm chuỗi thành một số. <code>sum(a == b for …)</code>: đếm số lần đúng. <code>all(…)</code>: đúng với mọi phần tử. <code>round(x, 3)</code>: làm tròn tới 3 chữ số sau dấu phẩy.</p>""",
            """[2] Kiểm bằng đường khác. Vì muốn dùng số thật, ta băm một nghìn hai trăm mã giao dịch bằng hàm băm có sẵn, rồi so mảnh khi chia ba và chia bốn.
            [4.1] Kết quả là ba trăm mười lăm trên một nghìn hai trăm, khoảng hai mươi sáu phần trăm, gần hai mươi lăm phần trăm.
            [4.2] Khi tách ba mảnh thành sáu, mọi bản ghi ở mảnh mới vẫn nằm trong đúng mảnh cũ của nó."""),
        stf(table(["số mảnh chính mới", "cách làm", "vì sao"],
                  [["6 (bội của 3)", "tách mảnh (split) sang chỉ mục mới: mỗi mảnh cũ tách đôi; chỉ mục cũ phải tạm chỉ đọc", "h mod 6 rồi mod 3 = h mod 3: bản ghi không rời mảnh cha"],
                   ["4 (không phải bội của 3)", "tạo chỉ mục mới, chép lại (reindex)", "75% bản ghi đổi mảnh"]]),
            """[1.2] Nếu số mảnh mới là bội của số cũ, như ba lên sáu, thì tách được vì bản ghi không rời mảnh cha, và chỉ mục cũ phải tạm chỉ đọc.
            [1.3] Nếu không phải bội thì phải tạo chỉ mục mới rồi chép lại toàn bộ.""",
            clear=True),
    ], checks=["alg.bnx_crc_keep(1200, 3, 4) == 315", "round(alg.bnx_crc_keep(1200, 3, 4) / 1200, 3) == 0.263",
               "alg.bnx_split_ok(3, 2)", f"1 - alg.bnx_keep_cycle(3, 4)[2] == {FR}(3, 4)"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Ghi xong tìm ngay, không thấy, tưởng ghi hỏng nên <b class="red">ghi lại lần nữa</b> → lịch sử có hai dòng trùng.
<br><span class="note">Cách chữa: chờ lần làm tươi; cần thấy ngay thì cho lệnh ghi chờ lần làm tươi kế tiếp (<code>refresh=wait_for</code>). Nếu không tự đặt <code>refresh_interval</code>, mảnh nào 30 giây không có lượt tìm thì tạm ngừng làm tươi nền; lượt tìm kế tiếp tự làm tươi mảnh đó trước khi tìm.</span></div>""",
           """Lỗi thứ nhất, của người mới. Ghi xong tìm ngay mà không thấy, tưởng ghi hỏng nên ghi lại lần nữa, thế là lịch sử có hai dòng trùng.
           Cách chữa là chờ lần làm tươi, hoặc cho lệnh ghi chờ tới lần làm tươi kế tiếp.
"""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Gọi lệnh làm tươi sau <b class="red">mỗi</b> lần ghi “cho chắc”. Làm tươi tốn tài nguyên; khuyến nghị của hãng là để làm tươi định kỳ chạy, hoặc dùng <code>wait_for</code>.
<br><span class="note">Cùng nhóm lỗi: tạo chỉ mục 1 mảnh chính (mặc định) rồi khi dữ liệu lớn muốn đổi sang 4 tại chỗ — không được, phải tạo chỉ mục mới.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm. Gọi lệnh làm tươi sau mỗi lần ghi cho chắc. Làm tươi tốn tài nguyên, nên khuyến nghị của hãng là để làm tươi định kỳ tự chạy, hoặc cho lệnh ghi chờ.
""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Giữ <b class="red">số dư</b> trong Elasticsearch. Chuyển tiền cần trừ A và cộng B cùng thành công; ở đây mỗi thao tác trong một lô (nhiều thao tác gửi chung một yêu cầu) có kết quả riêng, nên có thể trừ A xong mà cộng B hỏng.
<br><span class="note">Cách chữa: sổ chính ở cơ sở dữ liệu giao dịch (Oracle); Elasticsearch chỉ là bản chép để tìm, cập nhật qua Kafka (hệ truyền bản tin giữa các dịch vụ).</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là giữ số dư trong máy tìm kiếm. Mỗi thao tác trong một lô, tức nhiều thao tác gửi chung một yêu cầu, có kết quả riêng, nên có thể trừ A xong mà cộng B lại hỏng.
           Cách chữa là giữ sổ chính ở cơ sở dữ liệu giao dịch như Oracle. Máy tìm kiếm chỉ là bản chép để tìm.""", clear=True),
    ])
    quymo = sc("quymo", "example", "Khi dữ liệu lớn dần: tìm và đổi số mảnh, số đếm theo mô hình ở ba mức", [
        stf(table(["cách viết trong Python", "nghĩa"],
                  [["<code>\"chuyen tien napas\" if i % 1000 == 0 else \"chuyen tien the\"</code>", "chọn một trong hai chuỗi: nếu <code>i</code> chia hết cho 1000 thì lấy chuỗi đầu, không thì lấy chuỗi sau"],
                   ["<code>for i, m in enumerate(mo_ta):</code>", "duyệt danh sách <code>mo_ta</code> kèm số thứ tự <code>i</code> bắt đầu từ 0"],
                   ["<code>f\"tx{i}\"</code>", "chuỗi có <code>f</code> đứng đầu: <code>{i}</code> được thay bằng giá trị của <code>i</code>, ra tx0, tx1…"]]),
            """Khối mô phỏng dùng thêm vài cách viết, nên ta giải nghĩa trước. Cách viết chọn một trong hai chuỗi tuỳ điều kiện, và lệnh duyệt danh sách kèm số thứ tự. Chuỗi có chữ f đứng đầu thì phần trong ngoặc nhọn được thay bằng giá trị.""",
            clear=True),
        stf(P_QM_SEARCH.show(title="Mô phỏng bằng Python (không phải Elasticsearch thật): đếm theo mô hình số dòng phải đọc khi tìm chữ napas"),
            """[2] Ta đo bằng chương trình mô phỏng, không phải máy tìm kiếm thật, ở ba cỡ: một nghìn hai trăm, một trăm hai mươi nghìn và một triệu hai trăm nghìn mô tả.
            [2.4] [2.6] Mỗi vòng dựng chỉ mục ngược rồi hỏi chữ NAPAS có bao nhiêu dòng.""",
            clear=True),
        stf(P_QM_SEARCH.out_html("\n".join(P_QM_SEARCH.out.split("\n")), "Kết quả đếm của chương trình mô phỏng")
            + """<p class="note">Quét thô phải đọc <b>mọi</b> mô tả; chỉ mục ngược chỉ đọc danh sách của chữ cần tìm. Đây là <b>đếm theo mô hình</b> (độ dài danh sách trong mô phỏng), không đo thời gian hay đọc ghi đĩa, và chưa tính công dựng chỉ mục.</p>""",
            """[2] Dữ liệu lớn gấp một trăm lần thì quét thô phải đọc nhiều gấp một trăm lần. [3] Còn chỉ mục chỉ đọc danh sách của chữ NAPAS. Đây là số đếm theo mô hình, không đo thời gian thật.""",
            clear=True),
        stf(P_QM_ROUTE.show(title="Đếm theo mô hình (băm CRC32 minh hoạ, không phải hàm băm thật của Elasticsearch): đổi từ 3 sang 4 mảnh chính thì bao nhiêu bản ghi đổi mảnh?")
            + P_QM_ROUTE.out_html(),
            """[2] Giờ đo chuyện đổi số mảnh chính từ ba sang bốn, bằng cách băm thật từng mã giao dịch. [4.3] Ở một triệu hai trăm nghìn bản ghi, có tám trăm chín mươi chín nghìn bốn trăm tám mươi bản ghi đổi mảnh, khoảng bảy mươi lăm phần trăm. Lệch chút so với lý thuyết vì hàm băm không chia đều tuyệt đối.""",
            clear=True),
        stf(table(["số bản ghi", "quét thô: số mô tả phải đọc", "chỉ mục: số dòng phải đọc", "đổi 3 → 4 mảnh: số bản ghi phải chép lại", "chép lại mất (10 000 bản ghi/giây, số minh hoạ)"],
                  [["1 200 (×1)", "1 200", "2", "885", "≈ 0,09 giây"],
                   ["120 000 (×100)", "120 000", "120", "89 991", "≈ 9 giây"],
                   ["1 200 000 (×1000)", "1 200 000", "1 200", "899 480", "≈ 90 giây"]]),
            """[1.2] Quét thô tăng thẳng theo số bản ghi, còn chỉ mục chỉ tăng theo số dòng của chữ cần tìm. [1.3] [1.4] Nhưng ở một triệu hai trăm nghìn bản ghi, chép lại tốn chừng chín mươi giây, với tốc độ minh hoạ mười nghìn bản ghi mỗi giây, nên cách đổi số mảnh gãy.""",
            clear=True),
        stf(table(["cách xử lý", "được", "mất", "khi nào chọn"],
                  [["đoán đúng số mảnh chính ngay từ đầu, hơi dư", "khỏi phải chép lại về sau", "mỗi mảnh là một chỉ mục nhỏ riêng, nhiều mảnh nhỏ tốn tài nguyên", "dữ liệu chắc chắn sẽ lớn nhiều lần"],
                   ["tách mảnh sang bội số (3 → 6)", "mỗi mảnh cũ chỉ chia đôi, bản ghi không rời mảnh cha", "chỉ mục cũ phải tạm chỉ đọc, và vẫn tạo ra chỉ mục mới", "cần tăng mảnh mà không muốn băm lại từng bản ghi"],
                   ["tạo chỉ mục mới rồi chép lại", "đặt được số mảnh bất kỳ", "tốn thời gian chép như bảng trên, phải lo bản ghi mới ghi trong lúc chép", "số mảnh mới không phải bội số mảnh cũ"]]),
            """[1.1] Người làm nghề phải chọn. [1.2] Đoán số mảnh hơi dư ngay từ đầu thì khỏi chép lại, đổi lại nhiều mảnh nhỏ tốn tài nguyên. [1.3] Tách sang bội số thì bản ghi không rời mảnh cha, nhưng chỉ mục cũ phải tạm chỉ đọc. [1.4] Tạo chỉ mục mới thì đặt được số mảnh bất kỳ, đổi lại tốn thời gian chép.""",
            clear=True),
    ], checks=["[alg.bnx_l08_postings(n) for n in (1200, 120000, 1200000)] == [2, 120, 1200]",
               "[alg.bnx_l08_moved(n) for n in (1200, 120000, 1200000)] == [885, 89991, 899480]",
               "[round(100 * alg.bnx_l08_moved(n) / n) for n in (1200, 120000, 1200000)] == [74, 75, 75]",
               "[round(alg.bnx_l08_moved(n) / 10000, 2) for n in (1200, 120000, 1200000)] == [0.09, 9.0, 89.95]",
               "120000 // 1200 == 100 and 1200000 // 1200 == 1000"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "Chỉ mục 5 mảnh chính, mỗi mảnh 2 bản sao. Tổng cộng bao nhiêu mảnh?"],
                   ["2", "Băm minh hoạ = 23. Có 5 mảnh chính thì vào mảnh nào? Đổi thành 6 thì sao?"],
                   ["3", "Quyết định: trang “lịch sử giao dịch” có ô tìm theo mô tả và dòng số dư. Lấy mỗi thứ từ đâu?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.2] Câu một hỏi tổng số mảnh. [1.3] Câu hai hỏi băm hai mươi ba vào mảnh nào. [1.4] Câu ba hỏi trang lịch sử lấy ô tìm và dòng số dư từ đâu. [0] Hãy dừng video và làm ra giấy.""",
            pause=25),
        st("""<p>Câu 1: mỗi mảnh chính kèm 2 bản sao.</p>
$$5 \\cdot (1 + 2) = \\hlg{15}$$""",
           """Đáp án câu một. Mỗi mảnh chính kèm hai bản sao, nên tổng là năm nhân với một cộng hai, bằng mười lăm mảnh.""", focus=[0, 2]),
        stf("""<p>Câu 2:</p>
$$23 \\text{ mod } 5 = \\hlg{3}, \\qquad 23 \\text{ mod } 6 = \\hl{5}$$
<p>Mảnh đổi từ 3 sang 5. Trên vòng 30 giá trị chỉ 0…4 giữ mảnh, vì cùng số dư r thì h − r chia hết cho cả 5 và 6, tức cho 30, nên h = r &lt; 5: $\\frac{5}{30}$, khoảng 17%. Phải tạo chỉ mục mới.</p>""",
            """[2] Đáp án câu hai. Hai mươi ba chia năm dư ba, còn chia sáu dư năm, nên bản ghi đổi từ mảnh ba sang mảnh năm.
            [3] Trên vòng ba mươi giá trị, chỉ năm giá trị giữ mảnh, khoảng mười bảy phần trăm, nên phải tạo chỉ mục mới."""),
        stf(table(["lấy từ", "được", "mất"],
                  [["số dư: cơ sở dữ liệu giao dịch (Oracle)", "đúng ngay sau khi chốt, có giao dịch nhiều dòng", "tìm theo chữ trong mô tả chậm và kém linh hoạt"],
                   ["ô tìm mô tả: Elasticsearch", "tìm theo từ nhanh, xếp theo điểm liên quan", "trễ ít nhất một lần làm tươi cộng thời gian đường ống Kafka; phải ghi rõ “đang cập nhật”"]]),
            """[1.2] Đáp án câu ba. Số dư lấy từ cơ sở dữ liệu giao dịch, vì nó đúng ngay sau khi chốt, đổi lại tìm theo chữ thì chậm.
            [1.3] Ô tìm mô tả lấy từ máy tìm kiếm, nhanh nhưng trễ ít nhất một lần làm tươi cộng thời gian đi qua Kafka, nên giao diện phải báo đang cập nhật."""),
    ], checks=["alg.bnx_total_shards(5, 2) == 15", "alg.bnx_shard(23, 5) == 3 and alg.bnx_shard(23, 6) == 5",
               f"alg.bnx_keep_cycle(5, 6) == (5, 30, {FR}(1, 6))",
               "round(100 * alg.bnx_keep_cycle(5, 6)[2]) == 17"])
    lab_pr = practice_scene(sc, "Tự làm: chỉ mục ngược và định tuyến mảnh cho dữ liệu của bạn", practice_steps2(
        st, "BNX", "L08",
        """<p><b>Đề</b>: có bốn mô tả giao dịch (viết không dấu). Viết <code>mau.py</code> bằng Python:</p>
<table class='t'><tr><th>mã</th><th>mô tả</th></tr><tr><td>a1</td><td>rut tien atm</td></tr><tr><td>a2</td><td>chuyen tien the</td></tr><tr><td>a3</td><td>chuyen khoan napas</td></tr><tr><td>a4</td><td>nap tien the</td></tr></table>
<ol><li>dựng chỉ mục ngược, in danh sách bản ghi của ba từ <code>tien</code>, <code>the</code>, <code>chuyen</code></li><li>in các bản ghi chứa <b>cả</b> <code>chuyen</code> và <code>the</code></li><li>in mảnh của các giá trị băm 29, 41, 50 khi có 5 mảnh chính</li><li>đổi từ 4 sang 6 mảnh chính: đếm bao nhiêu trong 12 giá trị băm đầu (0 tới 11) giữ nguyên mảnh</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; chữ in ra phải đúng từng ký tự như kết quả mong đợi.</p>""",
        """Bây giờ tới phần bạn tự làm. Bạn viết chương trình Python dựng chỉ mục ngược và in danh sách bản ghi của ba từ. Rồi in các bản ghi chứa cả hai từ chuyển và thẻ. Cuối cùng tính mảnh của ba giá trị băm, và đếm giá trị giữ mảnh khi đổi từ bốn sang sáu. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> mỗi từ ứng với một tập mã bản ghi, dùng <code>setdefault(từ, set()).add(mã)</code>. Phần chung của hai tập là dấu <code>&amp;</code>. Mảnh là <code>h % số_mảnh</code>. Lưu <code>mau.py</code>, chạy <code>python mau.py</code>.
Lời giải đầy đủ ở <code>labs/BNX/L08/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, mỗi từ ứng với một tập mã bản ghi, và phần chung của hai tập tính bằng dấu và. Lời giải nằm trong thư mục thực hành của bài, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L08")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mô tả giao dịch", "chỉ mục ngược: từ → bản ghi", "băm mod số mảnh chính", "3 chính + 3 bản sao = 6", "làm tươi 1 giây → tìm thấy"),
           """Mô tả giao dịch được tách từ và ghi vào chỉ mục ngược. Mỗi bản ghi về một mảnh chính bằng băm rồi chia dư.
 Sau lần làm tươi, thường là một giây, bản ghi mới tìm thấy được."""),
        st("""<div class='box key'><b>Tư duy:</b> máy tìm kiếm là <b>bản chép để tìm</b>, không phải sổ. Số mảnh chính là quyết định lúc tạo chỉ mục; độ trễ làm tươi là điều phải nói trước với người dùng.</div>""",
           """Máy tìm kiếm là bản chép để tìm, không phải sổ cái. Số mảnh chính là quyết định lúc tạo chỉ mục, còn độ trễ làm tươi phải nói trước với người dùng."""),
        st("""<p>Bài sau: một kho lấy dữ liệu theo khoá, nơi mỗi lần ghi phải mang theo dấu phiên bản đã đọc, để không ghi đè cập nhật của người khác.</p>""",
           """Bài sau học một kho lấy dữ liệu theo khoá, nơi mỗi lần ghi mang theo dấu phiên bản vừa đọc, để không ghi đè cập nhật của người khác.""",
           forward_ref=True),
    ])
    return lesson("L08", "elasticsearch_manh_ban_sao", "Bài 8 — Elasticsearch: chỉ mục ngược phân tán, mảnh, bản sao và độ tươi",
                  "curriculum/bnx.yaml L08; audit/bnx/verify_bnx.py L08; Elasticsearch docs (bản hiện hành, đọc 2026-11-11): "
                  "_routing field, Index settings (number_of_shards, number_of_replicas, refresh_interval), Near real-time search, "
                  "Split index API, Refresh API, Bulk API",
                  ["Dựng chỉ mục ngược cho vài mô tả giao dịch", "Tính mảnh chứa một bản ghi từ khoá định tuyến",
                   "Giải thích vì sao bản ghi vừa ghi chưa tìm thấy ngay", "Biết vì sao không dùng Elasticsearch làm nơi lưu số dư",
                   "So sánh số bản ghi phải đọc và phải chép lại ở 1 200, 120 000 và 1 200 000 bản ghi"],
                  [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec],
                  covers=[(1, "practice"), (2, "example"), (3, "formula"), (4, "pitfalls"), (5, "quymo")])


LAB_DE = """# Lab BNX L08 — Chỉ mục ngược và định tuyến mảnh (mô phỏng bằng Python, không cần Elasticsearch)

Có bốn mô tả giao dịch (viết không dấu): `a1` rut tien atm; `a2` chuyen tien the; `a3` chuyen khoan napas; `a4` nap tien the.
Viết `mau.py` (Python 3, chỉ thư viện chuẩn) làm bốn việc, in đúng sáu dòng như `mong_doi.txt`:

1. Dựng chỉ mục ngược (từ → tập mã bản ghi) rồi in danh sách đã sắp của ba từ `tien`, `the`, `chuyen`, dạng `tien: a1 a2 a4` (từ, dấu hai chấm, các mã cách nhau một dấu cách).
2. In `chuyen va the:` và các mã bản ghi chứa cả hai từ (phần chung của hai tập), cùng dạng.
3. In `manh cua 29, 41, 50 voi 5 manh chinh:` và ba mảnh `h % 5`, cách nhau một dấu cách.
4. Đổi từ 4 sang 6 mảnh chính: đếm trong 12 giá trị băm đầu (0 đến 11) bao nhiêu giá trị có `h % 4 == h % 6`. In `doi 4 -> 6 manh chinh: giu manh <số> / 12`.

Gợi ý cú pháp Python: `d = {}` là từ điển rỗng; `d.setdefault(k, set()).add(x)` lấy tập của `k` (tạo tập rỗng nếu chưa có) rồi thêm `x`; `a & b` là phần chung của hai tập; `sorted(t)` xếp một tập; `h % n` là số dư; `print(a, *l)` in `a` rồi từng phần tử của `l` cách nhau dấu cách.

Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L08 mau.py`.
"""

# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L08", LAB_DE, "py", LAB_PY, LAB_OUT)
