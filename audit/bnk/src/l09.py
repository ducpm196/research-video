from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    so_cai = prog("SoCai", """
CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);
INSERT INTO but_toan VALUES (1, 'khach_A', -505500), (1, 'khach_B', 500000), (1, 'thu_phi', 5500);
SELECT gd, SUM(tien) FROM but_toan GROUP BY gd;
SELECT tk, SUM(tien) FROM but_toan GROUP BY tk ORDER BY tk;""", out="""1|0
khach_A|-505500
khach_B|500000
thu_phi|5500""", lang="sqlite")
    so_cai_dao = prog("SoCaiDao", """
CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);
INSERT INTO but_toan VALUES (1, 'khach_A', -505500), (1, 'khach_B', 500000), (1, 'thu_phi', 5500);
INSERT INTO but_toan SELECT 2, tk, -tien FROM but_toan WHERE gd = 1;
SELECT tk, SUM(tien) FROM but_toan GROUP BY tk ORDER BY tk;
SELECT COUNT(*) FROM but_toan;""", out="""khach_A|0
khach_B|0
thu_phi|0
6""", lang="sqlite")
    lab_sc = prog("SoCaiLab", """
CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);
INSERT INTO but_toan VALUES (1, 'C', -1206600), (1, 'D', 1200000), (1, 'phi', 6600);
INSERT INTO but_toan VALUES (2, 'C', -50000), (2, 'D', 40000);
SELECT gd FROM but_toan GROUP BY gd HAVING SUM(tien) <> 0;
SELECT tk, SUM(tien) FROM but_toan GROUP BY tk ORDER BY tk;""", out="""2
C|-1256600
D|1240000
phi|6600""", lang="sqlite")
    hook = sc("hook", "hook", "Vì sao ngân hàng không chỉ lưu một con số số dư?", [
        st("""<p>Nếu chỉ lưu <b>một cột số dư</b> và sửa thẳng, khi số dư sai ta <b>không biết sai từ đâu</b>, vì mọi dấu vết đã bị ghi đè.</p>
<div class="box key">Sổ cái ghi <b>từng bút toán</b>, mỗi giao dịch có tổng bằng <b>0</b>. Số dư chỉ là <b>tổng các bút toán</b>.</div>""",
           """Chào bạn, nếu chỉ lưu một cột số dư và sửa thẳng vào đó, khi số dư sai ta không biết sai từ đâu, vì mọi dấu vết đã bị ghi đè.
           Sổ cái làm khác. Nó ghi từng bút toán, mỗi giao dịch có tổng bằng không, và số dư chỉ là tổng các bút toán."""),
        st(table(["cách lưu", "tìm lỗi", "kiểm cân đối"],
                 [["một cột số dư, sửa trực tiếp", "không thể, dấu vết bị ghi đè", "không có gì để cộng lại"],
                  ["sổ cái bút toán, chỉ thêm", "xem từng dòng", "tổng mỗi giao dịch phải bằng 0"]]),
           """Bảng này so hai cách lưu. Một cột số dư sửa trực tiếp thì không tìm được lỗi và không có gì để cộng lại kiểm tra. Sổ cái chỉ thêm thì xem được từng dòng, và kiểm cân đối bằng cách cộng tổng mỗi giao dịch."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: ba điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Số nguyên đồng", "trong thanh toán, đồng Việt Nam không dùng phần lẻ (ISO 4217 ghi VND có 0 chữ số thập phân), nên lưu bằng số nguyên", "500 000 đồng = 500000"],
                  ["② Số có dấu", "dương là tiền vào, âm là tiền ra khỏi tài khoản", "−505 500 và +500 000"],
                  ["③ Tổng một nhóm", "cộng mọi số trong nhóm", "−100 + 60 + 40 = 0"]]),
           """Ôn ba điều. Trong thanh toán, đồng Việt Nam không dùng phần lẻ, nên ta lưu bằng số nguyên. Số có dấu cho biết hướng, dương là tiền vào, âm là tiền ra khỏi tài khoản. Tổng một nhóm là cộng mọi số trong nhóm.
           Lưu ý, kế toán dùng cách gọi nợ và có theo quy ước riêng, còn bài này dùng số có dấu cho dễ thấy."""),
        st("""$$-100 + 60 + 40 = 0$$""",
           """Một ví dụ số. Âm một trăm cộng sáu mươi cộng bốn mươi bằng không. Đó là một giao dịch cân đối."""),
    ], checks=["-100 + 60 + 40 == 0"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["bút toán", "một dòng trong sổ cái: tài khoản nào, bao nhiêu tiền, hướng nào"],
                  ["bút toán kép", "mỗi giao dịch ghi ít nhất hai dòng ở hai tài khoản: tiền rời chỗ này thì phải tới chỗ khác"],
                  ["sổ cái (ledger)", "tập mọi bút toán, chỉ thêm, không sửa, không xoá"],
                  ["cân đối", "tổng mọi bút toán của một giao dịch bằng 0"],
                  ["bút toán đảo", "dòng mới làm ngược một dòng cũ để sửa sai, không xoá dòng cũ"],
                  ["số dư", "về nguyên tắc bằng tổng các bút toán của tài khoản; số dư lưu sẵn phải khớp tổng đó"]]),
           """Bảng dưới đây giải thích nghĩa của sáu thuật ngữ sẽ gặp trong bài. Bút toán là một dòng cho biết tài khoản nào, bao nhiêu tiền, hướng nào. Bút toán kép nghĩa là mỗi giao dịch ghi ít nhất hai dòng ở hai tài khoản, vì tiền rời chỗ này thì phải tới chỗ khác.
           Sổ cái là tập mọi bút toán, chỉ thêm, không sửa, không xoá.
           Cân đối là tổng bút toán của một giao dịch bằng không. Bút toán đảo là dòng mới làm ngược dòng cũ để sửa sai. Số dư bằng tổng các bút toán của tài khoản."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: tiền đi từ đâu tới đâu, tổng luôn bằng không", [
        st(svg(1500, 420,
               box(40, 150, 360, 110, ["Khách A", "−505 500"], C_RED, bold=True),
               box(560, 40, 360, 110, ["Khách B", "+500 000"], C_GREEN, bold=True),
               box(560, 270, 360, 110, ["Thu phí", "+5 500"], C_GREEN, bold=True),
               arrow(400, 185, 555, 105, "#475569"), arrow(400, 225, 555, 320, "#475569"),
               box(1040, 150, 420, 110, ["Tổng giao dịch", "−505 500 + 500 000 + 5 500 = 0"], C_BLUE, bold=True, size=22)),
           """Hình cho thấy một giao dịch chuyển năm trăm nghìn kèm phí năm nghìn năm trăm. Khách A bị trừ năm trăm lẻ năm nghìn năm trăm. Khách B nhận năm trăm nghìn. Quỹ thu phí nhận năm nghìn năm trăm.
           Cộng ba dòng lại, tổng đúng bằng không. Tiền không tự sinh ra hay mất đi, chỉ đổi chỗ."""),
        st(svg(1500, 400,
               box(40, 40, 700, 70, "bút toán A: −505 500   (giao dịch 1)", C_GRAY, size=22),
               box(40, 120, 700, 70, "bút toán B: +500 000   (giao dịch 1)", C_GRAY, size=22),
               box(40, 200, 700, 70, "bút toán phí: +5 500   (giao dịch 1)", C_GRAY, size=22),
               box(40, 290, 700, 70, "chỉ thêm dòng mới ở cuối — không sửa, không xoá", C_AMBER, size=22, bold=True),
               box(840, 120, 620, 150, ["số dư của A", "= tổng các dòng của A", "= −505 500 (sổ bắt đầu trống)"], C_BLUE, bold=True, size=24),
               txt(1150, 330, "hệ thống thật lưu thêm số dư tính sẵn,", 22, "middle", "#475569"),
               txt(1150, 362, "cập nhật cùng giao dịch, đối soát với tổng", 22, "middle", "#475569")),
           """Sổ cái là một danh sách chỉ thêm ở cuối. Không dòng nào bị sửa hay xoá. Về nguyên tắc, số dư của một tài khoản là tổng các dòng của tài khoản đó.
           Ở đây sổ bắt đầu trống, nên số dư của A là âm năm trăm lẻ năm nghìn năm trăm.
           Hệ thống thật thường lưu thêm số dư tính sẵn để đọc nhanh, nhưng phải cập nhật cùng giao dịch với bút toán, và đối soát được với tổng bút toán."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: cân đối và sửa sai", [
        st("""<p><b>Bước 1.</b> Mỗi giao dịch có ít nhất hai dòng, và tổng các dòng bằng $0$. Vì vậy số tiền ra khỏi nơi này luôn bằng số tiền vào nơi khác.</p>
<span class='note'>Làm thử: $-505\\,500 + 500\\,000 + 5\\,500 = 0$.</span>""",
           """Bước một, vì mỗi giao dịch có ít nhất hai dòng và tổng bằng không, nên số tiền ra khỏi nơi này luôn bằng số tiền vào nơi khác. Làm thử, âm năm trăm lẻ năm nghìn năm trăm, cộng năm trăm nghìn, cộng năm nghìn năm trăm, bằng không."""),
        st("""<p><b>Bước 2.</b> Số dư bằng tổng các dòng của tài khoản. Vì sổ chỉ thêm, ta cộng lại bất cứ lúc nào để <b>kiểm</b>.</p>
<span class='note'>Làm thử: tài khoản B chỉ có một dòng $+500\\,000$ nên số dư $500\\,000$.</span>""",
           """Bước hai, vì số dư bằng tổng các dòng của tài khoản, và sổ chỉ thêm, nên ta cộng lại bất cứ lúc nào để kiểm. Làm thử, tài khoản B chỉ có một dòng cộng năm trăm nghìn, nên số dư là năm trăm nghìn."""),
        st("""<p><b>Bước 3.</b> Muốn sửa một giao dịch sai, thêm giao dịch mới có các dòng <b>ngược dấu</b>, không xoá dòng cũ. Tổng vẫn bằng $0$.</p>
<span class='note'>Làm thử: sau khi đảo, số dư mỗi tài khoản về số dư trước giao dịch; sổ ví dụ bắt đầu trống nên về $0$.</span>""",
           """Bước ba, vì sổ không được xoá, nên muốn sửa giao dịch sai ta thêm giao dịch mới có các dòng ngược dấu. Tổng vẫn bằng không.
           Làm thử, sau khi đảo, số dư mỗi tài khoản về đúng số dư trước giao dịch. Sổ ví dụ bắt đầu trống, nên về không."""),
    ], checks=["-505500 + 500000 + 5500 == 0", "alg.bnk_ledger_demo(500000, 5500)[0] == 0", "alg.bnk_ledger_demo(500000, 5500)[1]['khach_B'] == 500000",
               "all(v == 0 for v in alg.bnk_ledger_after_reversal(500000, 5500)[2].values())"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Chuyển $500\\,000$ đồng, phí $5\\,500$ đồng <i>(số minh hoạ)</i>.</p>
$$① \\; \\text{A bị trừ: } 500\\,000 + 5\\,500 = \\hl{505\\,500}$$""",
           """Ta ghi sổ một giao dịch. Chuyển năm trăm nghìn đồng, phí năm nghìn năm trăm đồng, đây là số minh hoạ. Phép tính thứ nhất, A bị trừ năm trăm nghìn cộng năm nghìn năm trăm, là năm trăm lẻ năm nghìn năm trăm đồng."""),
        st("""$$② \\; \\text{B nhận } +500\\,000,\\quad \\text{thu phí } +5\\,500$$""",
           """Phép tính thứ hai, B nhận cộng năm trăm nghìn, quỹ thu phí nhận cộng năm nghìn năm trăm."""),
        st("""<p>Dùng lại ba dòng ở ① và ②.</p>
$$③ \\; -505\\,500 + 500\\,000 + 5\\,500 = \\hlg{0}$$""",
           """Phép tính thứ ba, cộng ba dòng, âm năm trăm lẻ năm nghìn năm trăm, cộng năm trăm nghìn, cộng năm nghìn năm trăm, bằng không. Giao dịch cân đối."""),
        st("""<p>Phát hiện chuyển nhầm, thêm giao dịch đảo: ba dòng ngược dấu.</p>
$$④ \\; +505\\,500 - 500\\,000 - 5\\,500 = \\hlg{0}$$""",
           """Phép tính thứ tư, phát hiện chuyển nhầm, ta thêm giao dịch đảo với ba dòng ngược dấu. Tổng của giao dịch đảo cũng bằng không."""),
        st("""<p>Sổ lúc này có $3 + 3 = 6$ dòng.</p>
$$⑤ \\; \\text{số dư A} = -505\\,500 + 505\\,500 = \\hl{0}$$""",
           """Phép tính thứ năm, sổ lúc này có sáu dòng. Số dư của A bằng âm năm trăm lẻ năm nghìn năm trăm cộng năm trăm lẻ năm nghìn năm trăm, bằng không. Mọi dấu vết vẫn còn nguyên."""),
    ], checks=["500000 + 5500 == 505500", "alg.bnk_ledger_demo(500000, 5500)[1] == {'khach_A': -505500, 'khach_B': 500000, 'thu_phi': 5500}",
               "-505500 + 500000 + 5500 == 0", "+505500 - 500000 - 5500 == 0",
               "alg.bnk_ledger_after_reversal(500000, 5500)[0] == 3 + 3 and alg.bnk_ledger_after_reversal(500000, 5500)[2]['khach_A'] == 0"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: để cơ sở dữ liệu tìm giao dịch lệch", [
        st("""<p>Đường khác: vì mọi dòng nằm trong một bảng, ta hỏi cơ sở dữ liệu: giao dịch nào có tổng khác $0$? Ta cố ý sửa một dòng của giao dịch 1.</p>
<div class="box code"><code>SELECT txn FROM entry GROUP BY txn HAVING SUM(amt) &lt;&gt; 0;</code></div>
<p class="small">Bảng <code>entry</code> (bút toán) có cột <code>txn</code> (mã giao dịch) và <code>amt</code> (số tiền có dấu). <code>GROUP BY txn</code>: gom các dòng cùng mã giao dịch thành một nhóm. <code>HAVING SUM(amt) &lt;&gt; 0</code>: chỉ giữ nhóm có tổng khác 0.</p>
$$\\text{giao dịch lệch} = \\hl{[1]}$$""",
           """Kiểm bằng đường khác. Vì mọi dòng nằm trong một bảng, ta hỏi cơ sở dữ liệu giao dịch nào có tổng khác không. Bảng bút toán có cột mã giao dịch và cột số tiền có dấu. Câu truy vấn gom các dòng cùng mã giao dịch thành một nhóm, rồi chỉ giữ những nhóm có tổng khác không. Ta cố ý sửa một dòng của giao dịch một, và cơ sở dữ liệu chỉ đúng giao dịch một là lệch."""),
        st(table(["giao dịch", "các dòng", "tổng", "kết luận"],
                 [["1 (đã sửa lén)", "−100, +90", "−10", "lệch, phải điều tra"], ["2", "−5, +5", "0", "cân đối"]]),
           """Bảng này cho thấy kết quả. Vì giao dịch một có tổng âm mười, nên nó lệch và cần điều tra. Giao dịch hai tổng bằng không, nên cân đối. Chỉ cần một câu truy vấn tổng nhóm là thấy."""),
    ], checks=["alg.bnk_ledger_unbalanced([(1, 'a', -100), (1, 'b', 90), (2, 'a', -5), (2, 'b', 5)]) == [1]", "-100 + 90 == -10"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu số dư là một cột rồi <b class="red">cộng trừ trực tiếp</b>. Hai giao dịch cùng lúc có thể ghi đè nhau, và không còn dấu vết để tìm lỗi.</div>""",
           """Lỗi thứ nhất, của người mới. Lưu số dư là một cột rồi cộng trừ trực tiếp. Hai giao dịch cùng lúc có thể ghi đè nhau, và không còn dấu vết để tìm lỗi."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Xoá hay sửa dòng cũ</b> khi phát hiện sai, cho “gọn”. Từ đó sổ không còn bằng chứng, kiểm toán (người kiểm tra sổ sách độc lập) không dựng lại được. Chỉ thêm bút toán đảo.</div>""",
           """Lỗi thứ hai, của người đã đi làm, là xoá hay sửa dòng cũ khi phát hiện sai, cho gọn. Từ đó sổ không còn bằng chứng, và kiểm toán, tức người kiểm tra sổ sách độc lập, không dựng lại được. Hãy chỉ thêm bút toán đảo."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tính phí theo phần trăm bằng số thực rồi làm tròn tuỳ ý. Lệch một đồng mỗi giao dịch, nhân với hàng triệu giao dịch. Cần <b>quy tắc làm tròn viết rõ</b>, tính bằng số nguyên.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là tính phí theo phần trăm bằng số thực rồi làm tròn tuỳ ý. Lệch một đồng mỗi giao dịch, nhân với hàng triệu giao dịch thì thành số lớn.
           Cần quy tắc làm tròn viết rõ, và tính bằng số nguyên."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Chuyển 2 000 000 đồng, phí 11 000 đồng. Khách A bị trừ bao nhiêu?"],
                  ["2", "Ba dòng của giao dịch đó có tổng bằng bao nhiêu?"],
                  ["3", "Quyết định: sửa dòng sai trực tiếp hay thêm bút toán đảo?"]]),
           """Đến lượt bạn. Câu một, chuyển hai triệu đồng, phí mười một nghìn đồng, khách A bị trừ bao nhiêu? Câu hai, ba dòng của giao dịch đó có tổng bằng bao nhiêu?
           Câu ba, sửa dòng sai trực tiếp hay thêm bút toán đảo? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$2\\,000\\,000 + 11\\,000 = \\hl{2\\,011\\,000}$$""",
           """Đáp án câu một. Hai triệu cộng mười một nghìn bằng hai triệu không trăm mười một nghìn đồng."""),
        st("""$$-2\\,011\\,000 + 2\\,000\\,000 + 11\\,000 = \\hlg{0}$$""",
           """Đáp án câu hai. Âm hai triệu không trăm mười một nghìn, cộng hai triệu, cộng mười một nghìn, bằng không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["thêm bút toán đảo", "giữ nguyên dấu vết, kiểm toán dựng lại được", "sổ dài hơn"],
                  ["sửa trực tiếp dòng sai", "sổ gọn", "mất bằng chứng, không kiểm toán được"]]),
           """Đáp án câu ba. Thêm bút toán đảo giữ nguyên dấu vết và kiểm toán dựng lại được, đổi lại sổ dài hơn. Sửa trực tiếp thì sổ gọn nhưng mất bằng chứng. Với tiền, luôn chọn thêm bút toán đảo."""),
    ], checks=["2000000 + 11000 == 2011000", "alg.bnk_ledger_demo(2000000, 11000)[0] == 0 and alg.bnk_ledger_demo(2000000, 11000)[1]['khach_A'] == -2011000"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mỗi giao dịch ≥ 2 dòng", "tổng = 0", "sổ chỉ thêm", "số dư = tổng dòng", "sai → bút toán đảo"),
           """Tổng kết chuỗi logic. Mỗi giao dịch có ít nhất hai dòng và tổng bằng không. Sổ chỉ thêm. Số dư bằng tổng các dòng. Có sai thì thêm bút toán đảo."""),
        st("""<div class='box key'><b>Tư duy:</b> số dư là một <b>kết quả suy ra</b>, không phải dữ liệu gốc. Dữ liệu gốc là các bút toán không thể sửa.</div>""",
           """Điều cần mang theo. Số dư là một kết quả suy ra, không phải dữ liệu gốc. Dữ liệu gốc là các bút toán không thể sửa."""),
    ])
    # ── AF2: P1 SQL tối thiểu, SQL chạy thật trên sqlite (sổ cái, cân đối, đảo), quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm một điều", "nghĩa", "ví dụ"],
                 [["④ SQL tối thiểu", "<code>CREATE TABLE</code> tạo bảng; <code>INSERT INTO … VALUES</code> thêm dòng; <code>SELECT cột FROM bảng</code> lấy dữ liệu; <code>SUM(cột)</code> cộng; <code>GROUP BY cột</code> gom các dòng cùng giá trị cột đó thành nhóm; <code>HAVING</code> lọc nhóm; <code>ORDER BY</code> sắp xếp",
                   "<code>SELECT gd, SUM(tien) FROM but_toan GROUP BY gd;</code> cộng tiền theo từng giao dịch"]]),
           """Thêm một điều nữa. Ngôn ngữ SQL tối thiểu để đọc bài này. Một lệnh tạo bảng, một lệnh thêm dòng, một lệnh lấy dữ liệu từ bảng. Hàm cộng là hàm tính tổng, nó cộng mọi giá trị của một cột lại với nhau. Mệnh đề gom nhóm gom các dòng có cùng giá trị của một cột thành nhóm, mệnh đề lọc nhóm giữ nhóm thoả điều kiện, và mệnh đề sắp xếp xếp kết quả.
           Ví dụ, một câu lấy mã giao dịch và tổng tiền, gom theo mã giao dịch, cho tổng tiền của từng giao dịch.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: bốn điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: dựng sổ cái, kiểm cân đối, đảo bút toán (sqlite)", [
        st(code_block(so_cai, title="Sổ cái: một giao dịch có phí, hai câu tổng nhóm"),
           """Ta dựng sổ cái thật trên cơ sở dữ liệu nhỏ. Bảng bút toán có ba cột là mã giao dịch, tài khoản và số tiền có dấu. Giao dịch một có ba dòng: khách A ra năm trăm linh năm nghìn năm trăm, khách B vào năm trăm nghìn, và tài khoản thu phí vào năm nghìn năm trăm.
           Câu thứ nhất cộng số tiền theo mã giao dịch, câu thứ hai cộng theo tài khoản."""),
        st(out_block(so_cai),
           """Khi chạy thật, giao dịch một có tổng bằng không, tức là cân đối. Số dư theo tài khoản đúng là âm năm trăm linh năm nghìn năm trăm, năm trăm nghìn, và năm nghìn năm trăm.
           Phí năm nghìn năm trăm không biến mất, nó nằm ở tài khoản thu phí.""", clear=True),
        st(code_block(so_cai_dao, lines=(3, 5), title="Sửa sai bằng bút toán đảo: thêm dòng ngược dấu, không xoá dòng cũ"),
           """Bây giờ sửa sai bằng bút toán đảo. Lệnh chèn thứ nhất lấy mọi dòng của giao dịch một, đổi dấu số tiền, rồi ghi thành giao dịch hai. Không dòng cũ nào bị xoá hay sửa.
           Hai câu sau cộng số dư theo tài khoản và đếm số dòng của sổ cái.""", clear=True),
        st(out_block(so_cai_dao),
           """Khi chạy thật, ba tài khoản đều về không, và sổ cái có sáu dòng, ba dòng gốc cộng ba dòng đảo. Số dư về không mà lịch sử vẫn còn nguyên, nên người kiểm toán thấy cả việc làm sai lẫn việc sửa.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: cộng lại cả lịch sử cho tài khoản thu phí", [
        st("""<p>Mỗi giao dịch có $3$ dòng, và <b>mỗi</b> giao dịch đều có một dòng ở tài khoản thu phí. Cộng lại số dư bằng cách cộng mọi dòng của tài khoản đó trong một năm, với tốc độ quét $10^6$ dòng mỗi giây <i>(số minh hoạ)</i>:</p>"""
           + table(["tải", "giao dịch mỗi ngày", "dòng sổ cái mỗi ngày", "dòng thu phí mỗi năm", "cộng lại số dư thu phí"],
                   [["×1", "100 000", "300 000", "36 500 000", "36,5 giây"],
                    ["×100", "10 000 000", "30 000 000", "3 650 000 000", "<b>≈ 1 giờ</b>"],
                    ["×10 000", "1 000 000 000", "3 000 000 000", "365 000 000 000", "<b>≈ 4,2 ngày</b>"]]),
           """Mỗi giao dịch có ba dòng, và mỗi giao dịch đều có một dòng ở tài khoản thu phí. Giả sử cộng lại số dư bằng cách cộng mọi dòng của tài khoản đó trong một năm, quét một triệu dòng mỗi giây. Đây là số minh hoạ.
           Với một trăm nghìn giao dịch mỗi ngày, một năm có ba mươi sáu triệu rưỡi dòng, cộng lại mất ba mươi sáu rưỡi giây. Tải tăng một trăm lần, mất khoảng một giờ. Tải tăng mười nghìn lần, mất khoảng bốn ngày rưỡi.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> “Số dư luôn bằng tổng các bút toán” vẫn đúng, nhưng <b>tính lại từ đầu mỗi lần hỏi</b> thì gãy với tài khoản nóng như tài khoản thu phí: 36,5 giây, 1 giờ, 4,2 ngày.</div>
<div class="box key"><b>Đánh đổi:</b> lưu <b>số dư sẵn</b> và cập nhật cùng giao dịch, cộng đối chiếu với tổng bút toán định kỳ (hoặc chỉ cộng các dòng mới từ mốc chốt). Nhưng một dòng số dư mà mọi giao dịch cùng sửa sẽ thành <b>điểm nghẽn khoá</b> (như bài trước); có thể chia nhỏ thành nhiều dòng phí rồi cộng gộp.</div>""",
           """Câu hỏi là giải pháp cũ sẽ gãy ở chỗ nào khi tải tăng lên. Số dư luôn bằng tổng các bút toán vẫn đúng. Nhưng tính lại từ đầu mỗi lần hỏi thì gãy với tài khoản nóng như tài khoản thu phí, từ ba mươi sáu giây tới một giờ rồi bốn ngày.
           Đánh đổi là lưu số dư sẵn và cập nhật cùng giao dịch, cộng đối chiếu với tổng bút toán định kỳ, hoặc chỉ cộng các dòng mới kể từ mốc chốt. Nhưng một dòng số dư mà mọi giao dịch cùng sửa sẽ thành điểm nghẽn khoá, như bài trước.
           Cách giảm là chia nhỏ thành nhiều dòng phí rồi cộng gộp.""", clear=True),
    ], checks=["100000 * 3 == 300_000", "10_000_000 * 3 == 30_000_000", "1_000_000_000 * 3 == 3_000_000_000",
               "100000 * 365 == 36_500_000", "10_000_000 * 365 == 3_650_000_000", "1_000_000_000 * 365 == 365_000_000_000",
               "36_500_000 / 10**6 == 36.5", "round(3_650_000_000 / 10**6 / 3600, 1) == 1.0", "round(365_000_000_000 / 10**6 / 86400, 1) == 4.2"])
    write_lab("BNK", "L09", """# Lab BNK L09 — Hai giao dịch, một giao dịch lệch

Viết tệp `so_cai.sql` (chạy bằng `python labs/sqlrun.py so_cai.sql`, hoặc `sqlite3 :memory: < so_cai.sql`):

1. `CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);`
2. Giao dịch 1 (có phí): `('C', -1206600)`, `('D', 1200000)`, `('phi', 6600)`.
3. Giao dịch 2: `('C', -50000)`, `('D', 40000)` — **cố ý lệch**.
4. Câu `SELECT` tìm mã giao dịch có tổng khác 0 (`GROUP BY gd HAVING SUM(tien) <> 0`).
5. Câu `SELECT` số dư mỗi tài khoản: `tk`, `SUM(tien)`, `GROUP BY tk`, `ORDER BY tk`.

Chấm: `bash labs/cham.sh BNK L09 so_cai.sql`.
""", "sql", lab_sc["code"], lab_sc["out"])
    lab = practice_scene(sc, "Tự làm: hai giao dịch, tìm giao dịch lệch", practice_steps(
        st, "BNK", "L09",
        """<p><b>Đề</b>: viết <code>so_cai.sql</code>:</p>
<ol><li>bảng <code>but_toan(gd, tk, tien)</code>; giao dịch 1: <code>C −1206600</code>, <code>D +1200000</code>, <code>phi +6600</code></li>
<li>giao dịch 2 (cố ý lệch): <code>C −50000</code>, <code>D +40000</code></li>
<li><code>SELECT</code> mã giao dịch có tổng khác 0; <code>SELECT</code> số dư theo tài khoản</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Hãy viết một tệp SQL với bảng bút toán. Giao dịch một có phí, gồm ba dòng, C ra một triệu hai trăm linh sáu nghìn sáu trăm, D vào một triệu hai trăm nghìn, và phí sáu nghìn sáu trăm.
        Giao dịch hai cố ý lệch, C ra năm mươi nghìn và D vào bốn mươi nghìn. Rồi viết câu tìm giao dịch có tổng khác không, và câu tính số dư theo tài khoản. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_sc["out"], "so_cai.sql",
        """<div class="box key"><b>Nếu kẹt:</b> câu tìm lệch: <code>SELECT gd FROM but_toan GROUP BY gd HAVING SUM(tien) &lt;&gt; 0;</code>; câu số dư: <code>SELECT tk, SUM(tien) FROM but_toan GROUP BY tk ORDER BY tk;</code>.
Lời giải ở <code>labs/BNK/L09/loi_giai.sql</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, để tìm giao dịch lệch thì gom theo mã giao dịch rồi chỉ giữ nhóm có tổng khác không. Còn số dư thì gom theo tài khoản và cộng số tiền. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=150), "BNK", "L09")
    return lesson("L09", "so_cai_but_toan_kep", "Bài 9 — Sổ cái bút toán kép và kiểm cân đối",
                  "curriculum/bnk.yaml L09; audit/bnk/verify_bnk.py L09; audit/review/screen_code/BNK.yaml (SQL chạy thật trên sqlite 3.49); nguyên lý kế toán bút toán kép (Pacioli, 1494); mô hình số có dấu để minh hoạ, không thay quy ước nợ–có của kế toán",
                  ["Ghi sổ một giao dịch có phí bằng các dòng cân đối", "Tính số dư từ tổng các bút toán", "Sửa sai bằng bút toán đảo mà không xoá dòng cũ",
                   "Dùng một câu truy vấn tổng nhóm để tìm giao dịch lệch",
                   "Chạy SQL dựng sổ cái, kiểm cân đối và đảo bút toán để thấy kết quả",
                   "Tính số dòng sổ cái và thời gian cộng lại số dư của tài khoản thu phí khi tải tăng ×100, ×10 000",
                   "Viết SQL ghi hai giao dịch, tìm giao dịch lệch và tính số dư"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "example"), (2, "example"), (3, "formula"), (4, "check"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
