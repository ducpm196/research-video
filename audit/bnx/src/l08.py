import re

from lib import *

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

# Đầu ra THẬT (chạy bằng .venv Python 3.13.5, 2026-11-11; sổ: kind output, of: khối mã tương ứng)
INV_OUT = """
tiền ['d1', 'd2', 'd3', 'd4']
chuyển ['d1', 'd3']
napas ['d1']
chuyển và napas: ['d1']
"""
ROUTE_OUT = """
h = 17: 2 -> 1
giữ mảnh: [0, 1, 2] 3 / 12
"""
CRC_OUT = """
315 / 1200 = 0.263
tách 3 -> 6, mảnh mới nằm trong mảnh cũ: True
"""
REFRESH_OUT = """
ngay sau khi ghi: []
sau lần làm tươi: ['chuyển tiền napas']
"""

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
        stf("""<p>9 giờ đúng, khách chuyển $500\\,000$ đồng qua NAPAS. Giao dịch được ghi ngay vào cụm tìm kiếm Elasticsearch.</p>
<p>Nửa giây sau, khách mở <b>lịch sử giao dịch</b>, gõ “napas”: <b class="red">không thấy</b>.</p>
<div class="box key">Một giây sau gõ lại thì thấy. Tiền không mất: bản ghi chỉ <b>chưa tìm được</b>, vì chưa tới lần làm tươi.</div>""",
            """[1] Chào bạn, chín giờ đúng, khách chuyển năm trăm nghìn đồng qua NAPAS, và giao dịch được ghi ngay vào cụm máy tìm kiếm.
            [2] Nửa giây sau, khách mở lịch sử giao dịch và tìm chữ NAPAS, nhưng không thấy gì.
            [3] Một giây sau tìm lại thì thấy. Tiền không mất, bản ghi chỉ chưa tìm được, vì chưa tới lần làm tươi."""),
        stf(table(["câu hỏi", "bài này trả lời bằng"],
                  [["tìm “chuyển tiền napas” trong hàng triệu mô tả thế nào cho nhanh", "chỉ mục ngược: từ → danh sách bản ghi"],
                   ["bản ghi nằm ở mảnh nào, vì sao không đổi được số mảnh", "băm rồi chia dư cho số mảnh chính"],
                   ["vì sao ghi xong chưa tìm thấy ngay", "làm tươi định kỳ, mặc định 1 giây"],
                   ["có giữ số dư ở đây được không", "không: không có giao dịch nhiều bản ghi"]]),
            """Hôm nay ta trả lời bốn câu hỏi. [1.2] Thứ nhất, tìm một cụm từ trong hàng triệu mô tả giao dịch thế nào cho nhanh, câu trả lời là chỉ mục ngược.
            [1.3] Thứ hai, bản ghi nằm ở mảnh nào, và vì sao không đổi được số mảnh, câu trả lời là băm rồi chia dư.
            [1.4] Thứ ba, vì sao ghi xong chưa thấy ngay, đó là do làm tươi định kỳ, mặc định mỗi giây một lần.
            [1.5] Thứ tư, có giữ số dư ở đây được không, câu trả lời là không, vì máy tìm kiếm không có giao dịch gồm nhiều bản ghi."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        stf(table(["khái niệm", "nghĩa", "ví dụ"],
                  [["① Mục lục cuối sách", "mỗi từ khoá trỏ tới các trang có từ đó, nên không phải lật từng trang", "“lãi suất” → trang 12, 40"],
                   ["② Băm rồi chia dư", "hàm băm biến khoá thành một số, cùng khoá luôn ra cùng số; lấy số dư khi chia để chọn ngăn", "17 chia 3 dư 2 → ngăn 2"],
                   ["③ Giao dịch cơ sở dữ liệu", "nhiều thay đổi cùng thành công hoặc cùng huỷ", "trừ A 500 000 và cộng B 500 000 cùng chốt"],
                   ["④ Điểm liên quan", "xếp kết quả: bản ghi chứa từ hiếm, chứa từ nhiều lần thì đứng trên", "bài này chỉ nhắc, không đi sâu"]]),
            """Trước hết ta cần hiểu bốn điều. [1.2] Mục lục cuối sách cho mỗi từ khoá trỏ tới các trang có từ đó, nên ta không phải lật từng trang.
            [1.3] Băm rồi chia dư là cách chọn ngăn cho một khoá. Hàm băm biến khoá thành một số, cùng khoá luôn ra cùng số, rồi lấy số dư để chọn ngăn.
            [1.4] Giao dịch cơ sở dữ liệu là nhiều thay đổi cùng thành công hoặc cùng huỷ, ví dụ trừ tài khoản A và cộng tài khoản B cùng được chốt.
            [1.5] Còn điểm liên quan dùng để xếp kết quả, bản ghi chứa từ hiếm hoặc chứa nhiều lần thì đứng trên. Phần chấm điểm này bài hôm nay chỉ nhắc qua."""),
        st("""$$17 = 5 \\cdot 3 + 2$$""",
           """Một ví dụ số cho phép chia dư. Mười bảy bằng năm nhân ba cộng hai, nên mười bảy chia ba dư hai, và khoá đó vào ngăn số hai."""),
    ], checks=["17 == 5 * 3 + 2 and alg.bnx_shard(17, 3) == 2"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        stf(table(["từ trên màn hình", "nghĩa"],
                  [["document (bản ghi)", "một bản ghi JSON, ví dụ <code>{\"_id\": \"tx1001\", \"mo_ta\": \"chuyển tiền napas\"}</code>"],
                   ["index (chỉ mục)", "tập bản ghi cùng loại, giống một bảng"],
                   ["inverted index (chỉ mục ngược)", "từ → danh sách bản ghi chứa từ đó"],
                   ["primary shard (mảnh chính)", "một phần của chỉ mục; mỗi bản ghi thuộc đúng một mảnh chính"],
                   ["replica (bản sao)", "bản chép của mảnh chính: phục vụ đọc, thay mảnh chính khi hỏng; không đặt cùng máy với mảnh chính"],
                   ["<code>_routing</code> (khoá định tuyến)", "giá trị đem băm để chọn mảnh; mặc định là <code>_id</code>"],
                   ["refresh (làm tươi)", "mở phần vừa ghi cho việc tìm; mặc định mỗi 1 giây"]]),
            """Bảng này giải mã bảy từ. [1.2] Bản ghi là một gói dữ liệu JSON có các trường, ví dụ mã giao dịch và mô tả. [1.3] Chỉ mục là tập bản ghi cùng loại, giống một bảng.
            [1.4] Chỉ mục ngược đi từ từ sang danh sách bản ghi chứa từ đó. [1.5] Mảnh chính là một phần của chỉ mục, và mỗi bản ghi thuộc đúng một mảnh chính.
            [1.6] Bản sao là bản chép của mảnh chính, phục vụ đọc và thay mảnh chính khi hỏng, nên không đặt cùng máy với mảnh chính của nó.
            [1.7] Khoá định tuyến là giá trị đem băm để chọn mảnh, mặc định chính là mã bản ghi. [1.8] Làm tươi là mở phần vừa ghi cho việc tìm, mặc định mỗi giây."""),
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
           """Hình đầu cho thấy chỉ mục ngược. Bên trái là bốn mô tả giao dịch. Máy tách mỗi mô tả thành từng từ, rồi ghi ngược lại, mỗi từ trỏ tới các bản ghi chứa nó.
           Chữ tiền có trong cả bốn, chữ chuyển có trong d một và d ba, chữ NAPAS chỉ có trong d một.
           Muốn tìm cả hai chữ chuyển và NAPAS, máy lấy phần chung của hai danh sách, ra d một, mà không phải đọc lại mô tả nào."""),
        stf(code(INV_PY, "Dựng chỉ mục ngược bằng Python"),
            """[2] Đây là chương trình Python dựng đúng chỉ mục đó. [2.4] Vòng lặp ngoài đi qua từng bản ghi trong bốn mô tả. [2.6] Vòng lặp trong đi qua từng từ, và thêm mã bản ghi vào tập của từ ấy.
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
           Mười bảy chia ba dư hai, nên bản ghi vào mảnh chính số hai, nằm ở máy ba.
           Mỗi mảnh chính có một bản sao đặt ở máy khác, nên khi máy ba hỏng, bản sao của mảnh hai ở máy một được nâng lên thay.
           Cộng lại có ba mảnh chính và ba bản sao, tức sáu mảnh."""),
        st(svg(1500, 420,
               arrow(60, 200, 1440, 200, "#475569"),
               txt(1440, 245, "thời gian", 22, "end"),
               txt(160, 245, "0 s", 22), txt(570, 245, "0,5 s", 22), txt(870, 170, "1 s", 22), txt(1150, 245, "1,2 s", 22),
               box(30, 60, 260, 80, "ghi bản ghi", C_BLUE, size=24),
               box(420, 60, 300, 80, ["tìm “napas”", "không thấy"], C_RED, size=22),
               box(740, 280, 260, 80, "làm tươi", C_AMBER, size=24, bold=True),
               box(1000, 60, 300, 80, ["tìm “napas”", "thấy d1"], C_GREEN, size=22),
               arrow(160, 140, 160, 190), arrow(570, 140, 570, 190), arrow(870, 275, 870, 210), arrow(1150, 140, 1150, 190),
               txt(750, 405, "Ghi xong nằm ở vùng đệm; chỉ sau lần làm tươi (mặc định 1 giây) mới tìm được", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là trục thời gian. Ở giây không, bản ghi được ghi, nhưng nó mới nằm trong vùng đệm. Ở giây không phẩy năm, lượt tìm chưa thấy nó.
           Tới giây thứ một, lần làm tươi mở phần vừa ghi cho việc tìm. Nên ở giây một phẩy hai, lượt tìm đã thấy d một."""),
    ], checks=[f"alg.bnx_inverted_index({_D})['tiền'] == ['d1', 'd2', 'd3', 'd4']",
               f"alg.bnx_inverted_index({_D})['chuyển'] == ['d1', 'd3']",
               f"alg.bnx_search_and({_D}, 'chuyển', 'napas') == ['d1']",
               "alg.bnx_shard(17, 3) == 2", "alg.bnx_total_shards(3, 1) == 6",
               "alg.bnx_refresh_sim([(0, 'd1')], [0.5, 1.2]) == [0, 1]"])
    form = sc("formula", "formula", "Suy ra từng bước: bản ghi nằm ở đâu, và vì sao chưa thấy ngay", [
        stf("""<p><b>Bước 1.</b> Mọi máy phải tự tính ra mảnh của một bản ghi mà không tra bảng lớn, nên dùng một công thức cố định:</p>
$$\\text{mảnh} = \\text{băm}(\\text{khoá định tuyến}) \\text{ mod } \\text{số mảnh chính}$$
<span class='note'>Làm thử: băm = 17, có 3 mảnh chính → 17 mod 3 = 2. Bài dùng băm minh hoạ; hàm băm thật của Elasticsearch khác. Công thức này cho chỉ mục tạo từ bản 9.4; chỉ mục cũ hơn thêm một bước chia, nhưng vẫn phụ thuộc số mảnh chính.</span>""",
            """[1] Bước một, vì mọi máy phải tự tính ra mảnh của một bản ghi mà không phải tra một bảng lớn, nên ta dùng công thức cố định.
            [2] Mảnh bằng giá trị băm của khoá định tuyến, chia lấy dư cho số mảnh chính. Ba chữ m o d trên màn hình là viết tắt của phép lấy số dư.
            [3] Làm thử, băm ra mười bảy, có ba mảnh chính, thì mười bảy chia ba dư hai. Bài này dùng một hàm băm minh hoạ, còn hàm băm thật của hệ thống thì khác, và công thức này áp dụng cho chỉ mục tạo từ bản chín phẩy bốn."""),
        stf("""<p><b>Bước 2.</b> Mỗi mảnh chính có thêm một số bản sao, nên</p>
$$\\text{tổng số mảnh} = \\text{số mảnh chính} \\cdot (1 + \\text{số bản sao})$$
<p class='note'>Làm thử: $3 \\cdot (1 + 1) = 6$.</p>""",
            """[2] Bước hai, vì mỗi mảnh chính còn có thêm các bản sao của nó, nên tổng số mảnh bằng số mảnh chính nhân với một cộng số bản sao.
            Dấu chấm ở giữa là phép nhân. [3] Làm thử, ba nhân với một cộng một, bằng sáu."""),
        stf("""<p><b>Bước 3.</b> Công thức chia cho số mảnh chính, nên đổi số này thì số dư đổi theo:</p>
$$17 \\text{ mod } 4 = 1 \\neq 2$$
<span class='note'>Bản ghi đang nằm ở mảnh 2, nhưng lấy, sửa, xoá theo mã thì máy tới thẳng mảnh 1, nên không thấy. Vì vậy số mảnh chính chỉ đặt được lúc tạo chỉ mục.</span>""",
            """[1] Bước ba, vì công thức chia cho số mảnh chính, nên đổi số này thì số dư cũng đổi. [2] Mười bảy chia bốn dư một, khác hai.
            [3] Bản ghi đang nằm ở mảnh hai, nhưng khi lấy theo mã, máy tới thẳng mảnh một, nên không thấy. Vì vậy số mảnh chính chỉ đặt được lúc tạo chỉ mục.""",
            clear=True),
        stf(code(ROUTE_PY, "Bước 4. Đếm bao nhiêu giá trị băm giữ nguyên mảnh") + out(ROUTE_OUT),
            """[1] Bước bốn, số dư khi chia ba và khi chia bốn lặp lại sau mỗi mười hai giá trị, vì mười hai là bội chung nhỏ nhất của ba và bốn.
            [2.4] Nên chỉ cần đếm mười hai giá trị băm. [4.2] Chạy thật, chỉ có không, một và hai là giữ nguyên mảnh, tức ba trên mười hai.""",
            clear=True),
        stf(code(REFRESH_PY, "Bước 5. Mô phỏng làm tươi"),
            """[2.3] Bước năm, vì bản ghi mới chỉ vào vùng đệm, còn lượt tìm chỉ đọc phần đã mở, nên phải có bước làm tươi chuyển vùng đệm sang phần tìm được.
            [2.4] Hàm làm tươi chuyển hết vùng đệm sang phần tìm được rồi xoá vùng đệm. [2.9] Ta ghi một bản ghi, tìm ngay, làm tươi, rồi tìm lại.""",
            clear=True),
        stf(out(REFRESH_OUT, "Bước 5. Kết quả chạy thật"),
            """[2.1] Chạy thật, ngay sau khi ghi thì kết quả rỗng, vì bản ghi còn nằm trong vùng đệm. [2.2] Sau một lần làm tươi thì tìm thấy bản ghi chuyển tiền NAPAS.""",
            clear=True),
    ], checks=["alg.bnx_shard(17, 3) == 2", "alg.bnx_total_shards(3, 1) == 6", "alg.bnx_shard(17, 4) == 1",
               "alg.bnx_keep_cycle(3, 4)[:2] == (3, 12)", "alg.bnx_refresh_sim([(0, 'd1')], [0.0, 1.0]) == [0, 1]"])
    ex = sc("example", "example", "Ví dụ chỉ mục giao dịch, từng phép tính", [
        st("""<p>Chỉ mục giao dịch có 3 mảnh chính, mỗi mảnh 1 bản sao; chứa $1\\,200\\,000$ bản ghi (số minh hoạ).</p>
$$① \\; 3 \\cdot (1 + 1) = \\hl{6}\\ \\text{mảnh}$$""",
           """Ta làm một ví dụ. Chỉ mục giao dịch có ba mảnh chính, mỗi mảnh một bản sao, và chứa một triệu hai trăm nghìn bản ghi, đây là số minh hoạ.
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
           Vì gần như mọi bản ghi phải dời chỗ, hệ thống không đổi tại chỗ, mà phải tạo chỉ mục mới có bốn mảnh chính rồi chép lại toàn bộ.""",
           focus=[1, 2, 3]),
    ], checks=["alg.bnx_total_shards(3, 1) == 6", "alg.bnx_shard(17, 3) == 2", "alg.bnx_shard(17, 4) == 1",
               f"alg.bnx_keep_cycle(3, 4) == (3, 12, {FR}(1, 4))",
               "(1 - alg.bnx_keep_cycle(3, 4)[2]) * 1200000 == 900000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: băm thật trên 1 200 mã", [
        stf(code(CRC_PY, "Đường khác: băm CRC32 cho 1 200 mã giao dịch") + out(CRC_OUT),
            """[2] Kiểm bằng đường khác. Thay vì đếm trên vòng mười hai giá trị, ta băm thật một nghìn hai trăm mã giao dịch bằng hàm băm có sẵn trong Python, rồi so mảnh khi chia ba và chia bốn.
            [4.1] Kết quả là ba trăm mười lăm trên một nghìn hai trăm, khoảng hai mươi sáu phần trăm, rất gần hai mươi lăm phần trăm.
            [4.2] Dòng cuối kiểm một điều khác. Khi tách ba mảnh thành sáu, mọi bản ghi ở mảnh mới vẫn nằm trong đúng mảnh cũ của nó."""),
        stf(table(["số mảnh chính mới", "cách làm", "vì sao"],
                  [["6 (bội của 3)", "tách mảnh (split) sang chỉ mục mới: mỗi mảnh cũ tách đôi; chỉ mục cũ phải tạm chỉ đọc", "h mod 6 rồi mod 3 = h mod 3: bản ghi không rời mảnh cha"],
                   ["4 (không phải bội của 3)", "tạo chỉ mục mới, chép lại (reindex)", "75% bản ghi đổi mảnh"]]),
            """[1.2] Bảng này rút ra quy tắc. Nếu số mảnh mới là bội của số cũ, như ba lên sáu, thì tách được sang một chỉ mục mới, vì mỗi mảnh cũ chỉ chia đôi, và chỉ mục cũ phải tạm chỉ đọc.
            [1.3] Nếu không phải bội, như ba lên bốn, thì bảy mươi lăm phần trăm bản ghi đổi mảnh, nên phải tạo chỉ mục mới rồi chép lại.""",
            clear=True),
    ], checks=["alg.bnx_crc_keep(1200, 3, 4) == 315", "round(alg.bnx_crc_keep(1200, 3, 4) / 1200, 3) == 0.263",
               "alg.bnx_split_ok(3, 2)", f"1 - alg.bnx_keep_cycle(3, 4)[2] == {FR}(3, 4)"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Ghi xong tìm ngay, không thấy, tưởng ghi hỏng nên <b class="red">ghi lại lần nữa</b> → lịch sử có hai dòng trùng.
<br><span class="note">Cách chữa: chờ lần làm tươi; cần thấy ngay thì cho lệnh ghi chờ lần làm tươi kế tiếp (<code>refresh=wait_for</code>). Nếu không tự đặt <code>refresh_interval</code>, mảnh nào 30 giây không có lượt tìm thì tạm ngừng làm tươi nền; lượt tìm kế tiếp tự làm tươi mảnh đó trước khi tìm.</span></div>""",
           """Lỗi thứ nhất, của người mới. Ghi xong tìm ngay mà không thấy, tưởng ghi hỏng nên ghi lại lần nữa, thế là lịch sử có hai dòng trùng.
           Cách chữa là chờ lần làm tươi. Nếu thật sự cần thấy ngay, cho lệnh ghi chờ tới lần làm tươi kế tiếp rồi mới trả lời.
           Thêm một chi tiết, nếu không tự đặt chu kỳ làm tươi, mảnh nào ba mươi giây không có lượt tìm sẽ tạm ngừng làm tươi nền. Lượt tìm kế tiếp tự làm tươi mảnh đó trước khi tìm."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Gọi lệnh làm tươi sau <b class="red">mỗi</b> lần ghi “cho chắc”. Làm tươi tốn tài nguyên; khuyến nghị của hãng là để làm tươi định kỳ chạy, hoặc dùng <code>wait_for</code>.
<br><span class="note">Cùng nhóm lỗi: tạo chỉ mục 1 mảnh chính (mặc định) rồi khi dữ liệu lớn muốn đổi sang 4 tại chỗ — không được, phải tạo chỉ mục mới.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm. Gọi lệnh làm tươi sau mỗi lần ghi cho chắc. Làm tươi tốn tài nguyên, nên khuyến nghị của hãng là để làm tươi định kỳ tự chạy, hoặc cho lệnh ghi chờ.
           Cùng nhóm lỗi là tạo chỉ mục với một mảnh chính mặc định, rồi khi dữ liệu lớn muốn đổi sang bốn tại chỗ. Việc đó không làm được, phải tạo chỉ mục mới.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Giữ <b class="red">số dư</b> trong Elasticsearch. Chuyển tiền cần trừ A và cộng B cùng thành công; ở đây mỗi thao tác trong một lô có kết quả riêng, nên có thể trừ A xong mà cộng B hỏng.
<br><span class="note">Cách chữa: sổ chính ở cơ sở dữ liệu giao dịch (Oracle); Elasticsearch chỉ là bản chép để tìm, cập nhật qua Kafka.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là giữ số dư trong máy tìm kiếm. Chuyển tiền cần trừ A và cộng B cùng thành công hoặc cùng huỷ.
           Ở đây, mỗi thao tác trong một lô có kết quả riêng, nên có thể trừ A xong mà cộng B lại hỏng.
           Cách chữa là giữ sổ chính ở cơ sở dữ liệu giao dịch như Oracle. Máy tìm kiếm chỉ là bản chép để tìm, được cập nhật qua Kafka.""", clear=True),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        stf(table(["câu", "đề"],
                  [["1", "Chỉ mục 5 mảnh chính, mỗi mảnh 2 bản sao. Tổng cộng bao nhiêu mảnh?"],
                   ["2", "Băm minh hoạ = 23. Có 5 mảnh chính thì vào mảnh nào? Đổi thành 6 thì sao?"],
                   ["3", "Quyết định: trang “lịch sử giao dịch” có ô tìm theo mô tả và dòng số dư. Lấy mỗi thứ từ đâu?"]]),
            """Bây giờ tới phần bạn tự làm bài. [1.2] Câu một, chỉ mục năm mảnh chính, mỗi mảnh hai bản sao, tổng cộng bao nhiêu mảnh?
            [1.3] Câu hai, giá trị băm minh hoạ là hai mươi ba. Có năm mảnh chính thì vào mảnh nào, và đổi thành sáu thì sao?
            [1.4] Câu ba, trang lịch sử giao dịch có ô tìm theo mô tả và một dòng số dư. Bạn lấy mỗi thứ từ đâu? [0] Hãy dừng video và làm ra giấy.""",
            pause=25),
        st("""<p>Câu 1: mỗi mảnh chính kèm 2 bản sao.</p>
$$5 \\cdot (1 + 2) = \\hlg{15}$$""",
           """Đáp án câu một. Mỗi mảnh chính kèm hai bản sao, nên tổng là năm nhân với một cộng hai, bằng mười lăm mảnh.""", focus=[0, 2]),
        stf("""<p>Câu 2:</p>
$$23 \\text{ mod } 5 = \\hlg{3}, \\qquad 23 \\text{ mod } 6 = \\hl{5}$$
<p>Mảnh đổi từ 3 sang 5. Trên vòng 30 giá trị chỉ 0…4 giữ mảnh, vì cùng số dư r thì h − r chia hết cho cả 5 và 6, tức cho 30, nên h = r &lt; 5: $\\frac{5}{30}$, khoảng 17%. Phải tạo chỉ mục mới.</p>""",
            """[2] Đáp án câu hai. Hai mươi ba chia năm dư ba, còn chia sáu dư năm, nên bản ghi đổi từ mảnh ba sang mảnh năm.
            [3] Trên vòng ba mươi giá trị, chỉ năm giá trị từ không tới bốn giữ mảnh, vì cùng số dư thì hiệu chia hết cho cả năm và sáu, tức cho ba mươi. Tỉ lệ khoảng mười bảy phần trăm, nên phải tạo chỉ mục mới."""),
        stf(table(["lấy từ", "được", "mất"],
                  [["số dư: cơ sở dữ liệu giao dịch (Oracle)", "đúng ngay sau khi chốt, có giao dịch nhiều dòng", "tìm theo chữ trong mô tả chậm và kém linh hoạt"],
                   ["ô tìm mô tả: Elasticsearch", "tìm theo từ nhanh, xếp theo điểm liên quan", "trễ ít nhất một lần làm tươi cộng thời gian đường ống Kafka; phải ghi rõ “đang cập nhật”"]]),
            """[1.2] Đáp án câu ba. Số dư lấy từ cơ sở dữ liệu giao dịch, vì nó đúng ngay sau khi chốt và có giao dịch nhiều dòng, đổi lại tìm theo chữ trong mô tả thì chậm.
            [1.3] Ô tìm mô tả lấy từ máy tìm kiếm, nhanh và xếp được theo điểm liên quan. Cái giá là trễ ít nhất một lần làm tươi, cộng thời gian đi qua Kafka, nên giao diện nên báo đang cập nhật."""),
    ], checks=["alg.bnx_total_shards(5, 2) == 15", "alg.bnx_shard(23, 5) == 3 and alg.bnx_shard(23, 6) == 5",
               f"alg.bnx_keep_cycle(5, 6) == (5, 30, {FR}(1, 6))",
               "round(100 * alg.bnx_keep_cycle(5, 6)[2]) == 17"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mô tả giao dịch", "chỉ mục ngược: từ → bản ghi", "băm mod số mảnh chính", "3 chính + 3 bản sao = 6", "làm tươi 1 giây → tìm thấy"),
           """Tổng kết chuỗi logic. Mô tả giao dịch được tách từ và ghi vào chỉ mục ngược. Mỗi bản ghi về một mảnh chính bằng băm rồi chia dư.
           Ba mảnh chính và ba bản sao thành sáu mảnh trên nhiều máy. Sau lần làm tươi, thường là một giây, bản ghi mới tìm thấy được."""),
        st("""<div class='box key'><b>Tư duy:</b> máy tìm kiếm là <b>bản chép để tìm</b>, không phải sổ. Số mảnh chính là quyết định lúc tạo chỉ mục; độ trễ làm tươi là điều phải nói trước với người dùng.</div>""",
           """Điều cần mang theo. Máy tìm kiếm là bản chép để tìm, không phải sổ cái. Số mảnh chính là quyết định lúc tạo chỉ mục, còn độ trễ làm tươi phải nói trước với người dùng."""),
        st("""<p>Bài sau: một kho lấy dữ liệu theo khoá, nơi mỗi lần ghi phải mang theo dấu phiên bản đã đọc, để không ghi đè cập nhật của người khác.</p>""",
           """Ở bài sau, ta học một kho lấy dữ liệu theo khoá, nơi mỗi lần ghi phải mang theo dấu phiên bản vừa đọc, để không ghi đè cập nhật của người khác.""",
           forward_ref=True),
    ])
    return lesson("L08", "elasticsearch_manh_ban_sao", "Bài 8 — Elasticsearch: chỉ mục ngược phân tán, mảnh, bản sao và độ tươi",
                  "curriculum/bnx.yaml L08; audit/bnx/verify_bnx.py L08; Elasticsearch docs (bản hiện hành, đọc 2026-11-11): "
                  "_routing field, Index settings (number_of_shards, number_of_replicas, refresh_interval), Near real-time search, "
                  "Split index API, Refresh API, Bulk API",
                  ["Dựng chỉ mục ngược cho vài mô tả giao dịch", "Tính mảnh chứa một bản ghi từ khoá định tuyến",
                   "Giải thích vì sao bản ghi vừa ghi chưa tìm thấy ngay", "Biết vì sao không dùng Elasticsearch làm nơi lưu số dư"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
