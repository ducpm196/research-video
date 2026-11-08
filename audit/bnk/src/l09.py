from lib import *


def build():
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
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Số nguyên đồng", "tiền Việt Nam không có phần lẻ, lưu bằng số nguyên", "500 000 đồng = 500000"],
                  ["② Số có dấu", "dương là tiền vào, âm là tiền ra khỏi tài khoản", "−505 500 và +500 000"],
                  ["③ Tổng một nhóm", "cộng mọi số trong nhóm", "−100 + 60 + 40 = 0"]]),
           """Ôn ba điều. Tiền Việt Nam không có phần lẻ nên ta lưu bằng số nguyên. Số có dấu cho biết hướng, dương là tiền vào, âm là tiền ra khỏi tài khoản. Tổng một nhóm là cộng mọi số trong nhóm.
           Lưu ý, kế toán dùng cách gọi nợ và có theo quy ước riêng, còn bài này dùng số có dấu cho dễ thấy."""),
        st("""$$-100 + 60 + 40 = 0$$""",
           """Một ví dụ số. Âm một trăm cộng sáu mươi cộng bốn mươi bằng không. Đó là một giao dịch cân đối."""),
    ], checks=["-100 + 60 + 40 == 0"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["bút toán", "một dòng trong sổ cái: tài khoản nào, bao nhiêu tiền, hướng nào"],
                  ["sổ cái (ledger)", "tập mọi bút toán, chỉ thêm, không sửa, không xoá"],
                  ["cân đối", "tổng mọi bút toán của một giao dịch bằng 0"],
                  ["bút toán đảo", "dòng mới làm ngược một dòng cũ để sửa sai, không xoá dòng cũ"],
                  ["số dư", "về nguyên tắc bằng tổng các bút toán của tài khoản; số dư lưu sẵn phải khớp tổng đó"]]),
           """Bảng này giải mã năm từ. Bút toán là một dòng cho biết tài khoản nào, bao nhiêu tiền, hướng nào. Sổ cái là tập mọi bút toán, chỉ thêm, không sửa, không xoá.
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
$$\\text{giao dịch lệch} = \\hl{[1]}$$""",
           """Kiểm bằng đường khác. Vì mọi dòng nằm trong một bảng, ta hỏi cơ sở dữ liệu giao dịch nào có tổng khác không. Ta cố ý sửa một dòng của giao dịch một, và cơ sở dữ liệu chỉ đúng giao dịch một là lệch."""),
        st(table(["giao dịch", "các dòng", "tổng", "kết luận"],
                 [["1 (đã sửa lén)", "−100, +90", "−10", "lệch, phải điều tra"], ["2", "−5, +5", "0", "cân đối"]]),
           """Bảng này cho thấy kết quả. Vì giao dịch một có tổng âm mười, nên nó lệch và cần điều tra. Giao dịch hai tổng bằng không, nên cân đối. Chỉ cần một câu truy vấn tổng nhóm là thấy."""),
    ], checks=["alg.bnk_ledger_unbalanced([(1, 'a', -100), (1, 'b', 90), (2, 'a', -5), (2, 'b', 5)]) == [1]", "-100 + 90 == -10"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu số dư là một cột rồi <b class="red">cộng trừ trực tiếp</b>. Hai giao dịch cùng lúc có thể ghi đè nhau, và không còn dấu vết để tìm lỗi.</div>""",
           """Lỗi thứ nhất, của người mới. Lưu số dư là một cột rồi cộng trừ trực tiếp. Hai giao dịch cùng lúc có thể ghi đè nhau, và không còn dấu vết để tìm lỗi."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Xoá hay sửa dòng cũ</b> khi phát hiện sai, cho “gọn”. Từ đó sổ không còn bằng chứng, kiểm toán không dựng lại được. Chỉ thêm bút toán đảo.</div>""",
           """Lỗi thứ hai, của người đã đi làm, là xoá hay sửa dòng cũ khi phát hiện sai, cho gọn. Từ đó sổ không còn bằng chứng, kiểm toán không dựng lại được. Hãy chỉ thêm bút toán đảo."""),
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
    return lesson("L09", "so_cai_but_toan_kep", "Bài 9 — Sổ cái bút toán kép và kiểm cân đối",
                  "curriculum/bnk.yaml L09; audit/bnk/verify_bnk.py L09; nguyên lý kế toán bút toán kép (Pacioli, 1494); mô hình số có dấu để minh hoạ, không thay quy ước nợ–có của kế toán",
                  ["Ghi sổ một giao dịch có phí bằng các dòng cân đối", "Tính số dư từ tổng các bút toán", "Sửa sai bằng bút toán đảo mà không xoá dòng cũ",
                   "Dùng một câu truy vấn tổng nhóm để tìm giao dịch lệch"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
