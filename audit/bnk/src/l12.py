from lib import *

BANK = "[('r1', 100), ('r2', 200), ('r3', 300), ('r4', 400), ('r5', 500)]"
SWITCH = "[('r1', 100), ('r2', 200), ('r3', 350), ('r4', 400), ('r6', 600)]"


def build():
    hook = sc("hook", "hook", "Vì sao cuối ngày sổ ngân hàng và sổ chuyển mạch lệch nhau?", [
        st("""<p>Cuối ngày, ngân hàng có $5$ giao dịch, chuyển mạch cũng có $5$. Nhưng hai danh sách <b>không giống nhau</b>: có giao dịch chỉ một bên có, và có giao dịch hai bên ghi <b>số tiền khác nhau</b>.</p>
<div class="box key">Việc <b>đối soát</b> tìm ra chúng, theo từng loại, rồi mỗi loại có cách xử lý riêng.</div>""",
           """Chào bạn, cuối ngày, ngân hàng có năm giao dịch, chuyển mạch cũng có năm. Nhưng hai danh sách không giống nhau. Có giao dịch chỉ một bên có, và có giao dịch hai bên ghi số tiền khác nhau.
           Đối soát tìm ra chúng, theo từng loại, rồi mỗi loại có cách xử lý riêng."""),
        st(table(["loại", "số giao dịch (ví dụ minh hoạ)"],
                 [["khớp hoàn toàn", "3"], ["chỉ có ở ngân hàng", "1"], ["chỉ có ở chuyển mạch", "1"], ["cùng mã nhưng lệch tiền", "1"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài, với số liệu minh hoạ. Ba giao dịch khớp hoàn toàn, một giao dịch chỉ có ở ngân hàng, một chỉ có ở chuyển mạch, và một cùng mã nhưng lệch tiền.
           Lưu ý, bài này dùng mô hình chung của chuyển mạch liên ngân hàng. Ở Việt Nam, chuyển mạch đó là NAPAS, công ty chuyển mạch thẻ và thanh toán liên ngân hàng. Chi tiết của NAPAS nằm trong đặc tả kết nối chính thức của họ."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: ba điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Mã tham chiếu", "mã định danh giao dịch, cả hai bên cùng giữ. Trong bản tin thẻ có RRN (mã tham chiếu 12 ký tự) và STAN (mã vết 6 số do bên gửi đánh); một mã một mình thường chưa đủ duy nhất, nên hệ thống thật hay ghép nhiều trường, ví dụ RRN + STAN + ngày giờ truyền + mã ngân hàng, theo đặc tả của từng mạng", "r1, r2, … (bài gộp thành một mã)"],
                  ["② Hai tập hợp", "tập A và tập B; phần chung gọi là giao", "A = {r1, r2, r3, r4, r5}"],
                  ["③ Đếm bù trừ", "|A| + |B| − |giao| = số mã khác nhau trong cả hai (|A|: số phần tử của A)", "5 + 5 − 4 = 6"]]),
           """Ôn ba điều. Mã tham chiếu là mã định danh giao dịch, cả hai bên cùng giữ. Trong bản tin thẻ có mã tham chiếu mười hai ký tự, và mã vết sáu chữ số do bên gửi đánh.
           Một mã một mình thường chưa đủ duy nhất, nên hệ thống thật hay ghép nhiều trường, ví dụ thêm mã vết, ngày giờ truyền và mã ngân hàng, theo đặc tả của từng mạng. Bài này gộp lại thành một mã cho gọn.
           Hai tập hợp có phần chung gọi là giao. Còn đếm bù trừ nói rằng số mã khác nhau trong cả hai danh sách bằng số phần tử của tập A cộng số phần tử của tập B, trừ đi số phần tử của phần chung.
           Trên màn hình, số phần tử của tập A được viết là A nằm giữa hai gạch đứng."""),
        st("""$$5 + 5 - 4 = 6$$""",
           """Một ví dụ số. Mỗi bên có năm mã, bốn mã chung, nên tổng số mã khác nhau là năm cộng năm trừ bốn, bằng sáu."""),
    ], checks=["5 + 5 - 4 == 6", "len({'r1', 'r2', 'r3', 'r4', 'r5'} | {'r1', 'r2', 'r3', 'r4', 'r6'}) == 6"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["chuyển mạch (switch)", "hệ thống ở giữa, nhận lệnh từ ngân hàng gửi và chuyển tới ngân hàng nhận"],
                  ["ngân hàng gửi / nhận", "bên khởi tạo lệnh chuyển / bên có tài khoản thụ hưởng"],
                  ["đối soát", "so cả hai danh sách giao dịch theo mã để tìm chỗ lệch"],
                  ["tra soát", "hỏi trạng thái hoặc khiếu nại cho từng giao dịch cụ thể"],
                  ["hết giờ chờ (chưa rõ kết quả)", "bên gửi chưa nhận được kết quả; trạng thái thật phải tra cứu"],
                  ["bản tin huỷ (reversal)", "bản tin đảo một giao dịch đã hạch toán khi cần"]]),
           """Bảng dưới đây giải nghĩa sáu thuật ngữ mà bài sẽ dùng. Chuyển mạch là hệ thống ở giữa, nhận lệnh từ ngân hàng gửi rồi chuyển tới ngân hàng nhận. Ngân hàng gửi khởi tạo lệnh, ngân hàng nhận có tài khoản thụ hưởng.
           Đối soát là so cả hai danh sách theo mã để tìm chỗ lệch. Còn tra soát là hỏi trạng thái hoặc khiếu nại cho từng giao dịch cụ thể. Hết giờ chờ là khi chưa nhận được kết quả, trạng thái thật phải tra cứu. Bản tin huỷ là bản tin đảo một giao dịch đã hạch toán."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: đường đi của một lệnh chuyển nhanh và chỗ có thể mất dấu", [
        st(svg(1500, 440,
               box(30, 150, 240, 110, ["Ứng dụng", "khách bấm"], C_BLUE, bold=True),
               box(320, 150, 250, 110, ["Ngân hàng gửi", "lõi + cổng"], C_BLUE, bold=True),
               box(620, 150, 250, 110, ["Chuyển mạch", "liên ngân hàng"], C_AMBER, bold=True),
               box(920, 150, 270, 110, ["Ngân hàng nhận", "ghi có"], C_GREEN, bold=True),
               arrow(270, 195, 315, 195), arrow(570, 195, 615, 195), arrow(870, 195, 915, 195),
               arrow(915, 240, 875, 240, "#16a34a"), arrow(615, 240, 575, 240, "#16a34a"), arrow(315, 240, 275, 240, "#16a34a"),
               txt(1330, 150, "đi: yêu cầu 0200", 26, "middle", "#2a78d6", True), txt(1330, 195, "về: phản hồi 0210", 26, "middle", "#16a34a", True),
               txt(750, 340, "Mỗi mũi tên có thể mất: lệnh mất, hoặc kết quả mất dù bên nhận đã ghi có", 26, "middle", "#dc2626", True),
               txt(750, 390, "→ bên gửi không biết kết quả → cần tra soát và đối soát", 26, "middle", "#1f2937")),
           """Hình cho thấy đường đi của một lệnh chuyển nhanh. Khách bấm trên ứng dụng. Ngân hàng gửi đóng gói lệnh, tức bản tin loại không hai không không là yêu cầu, rồi gửi tới chuyển mạch.
           Chuyển mạch chuyển tiếp tới ngân hàng nhận để ghi có, tức cộng tiền cho người nhận. Kết quả quay ngược lại cùng đường, bằng bản tin loại không hai một không là phản hồi.
           Mỗi mũi tên đều có thể mất. Nếu kết quả mất dù bên nhận đã ghi có, bên gửi không biết kết quả, nên cần tra soát và đối soát."""),
        st(svg(1500, 440,
               panel(40, 30, 600, 380, "Sổ ngân hàng", C_BLUE),
               box(70, 100, 540, 55, "r1: 100", C_GRAY, size=24), box(70, 165, 540, 55, "r2: 200", C_GRAY, size=24), box(70, 230, 540, 55, "r3: 300", C_AMBER, size=24),
               box(70, 295, 540, 55, "r4: 400", C_GRAY, size=24), box(70, 360, 540, 45, "r5: 500  (chỉ bên này)", C_RED, size=22),
               panel(860, 30, 600, 380, "Sổ chuyển mạch", C_AMBER),
               box(890, 100, 540, 55, "r1: 100", C_GRAY, size=24), box(890, 165, 540, 55, "r2: 200", C_GRAY, size=24), box(890, 230, 540, 55, "r3: 350  (lệch tiền)", C_AMBER, size=24),
               box(890, 295, 540, 55, "r4: 400", C_GRAY, size=24), box(890, 360, 540, 45, "r6: 600  (chỉ bên này)", C_RED, size=22),
               arrow(615, 127, 885, 127, "#475569"), arrow(615, 192, 885, 192, "#475569"), arrow(615, 257, 885, 257, "#d97706"), arrow(615, 322, 885, 322, "#475569")),
           """Đối soát là đặt hai sổ cạnh nhau và ghép theo mã. R một, r hai và r bốn khớp cả mã lẫn số tiền. R ba có mặt ở cả hai nhưng ba trăm lệch ba trăm năm mươi.
           R năm chỉ có ở ngân hàng, r sáu chỉ có ở chuyển mạch. Đó là bốn loại ta cần phân biệt.""",
           clear=True),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: phân loại hai danh sách", [
        st("""<p><b>Bước 1.</b> Dùng <b>mã tham chiếu</b> làm khoá ghép, không dùng số tiền (hai giao dịch khác nhau có thể cùng số tiền).</p>
<span class='note'>Làm thử: hai sổ có $5 + 5 - 4 = 6$ mã khác nhau.</span>""",
           """Bước một, vì hai giao dịch khác nhau có thể cùng số tiền, nên ta dùng mã tham chiếu làm khoá ghép, không dùng số tiền. Làm thử, hai sổ có năm cộng năm trừ bốn, bằng sáu mã khác nhau."""),
        st("""<p><b>Bước 2.</b> Với mỗi mã, đúng một trong bốn loại: <b>khớp</b> (cả hai có, tiền bằng), <b>lệch tiền</b> (cả hai có, tiền khác), <b>chỉ ngân hàng</b>, <b>chỉ chuyển mạch</b>.</p>
<span class='note'>Làm thử: $3 + 1 + 1 + 1 = 6$, đủ cả sáu mã, không mã nào thuộc hai loại.</span>""",
           """Bước hai, vì mỗi mã chỉ rơi vào đúng một loại, nên ta chia bốn loại. Khớp là cả hai có và tiền bằng nhau. Lệch tiền là cả hai có nhưng tiền khác. Còn hai loại là chỉ ngân hàng có, hoặc chỉ chuyển mạch có.
           Làm thử, ba cộng một cộng một cộng một bằng sáu, đủ cả sáu mã."""),
        st("""<p><b>Bước 3.</b> Mỗi loại có <b>hành động riêng</b> (quy trình điển hình): khớp thì xong; chỉ một bên thì tra soát trạng thái thật; lệch tiền thì điều tra nguyên nhân. Việc sửa sổ luôn qua bước duyệt.</p>
<span class='note'>Sửa sổ bằng bút toán đảo: thêm dòng mới ngược dấu với dòng sai, không xoá dòng cũ.</span>""",
           """Bước ba, vì nguyên nhân mỗi loại khác nhau, nên mỗi loại có hành động riêng theo quy trình điển hình. Khớp thì xong. Chỉ một bên có thì tra soát trạng thái thật. Lệch tiền thì điều tra nguyên nhân.
           Việc sửa sổ luôn qua bước duyệt, và sửa bằng bút toán đảo, tức là thêm một dòng mới ngược dấu với dòng sai, chứ không xoá dòng cũ."""),
    ], checks=["3 + 1 + 1 + 1 == 6", "alg.bnk_reconcile(" + BANK + ", " + SWITCH + ") == (3, 1, 1, 1)"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Sổ ngân hàng: r1 $100$, r2 $200$, r3 $300$, r4 $400$, r5 $500$. Sổ chuyển mạch: r1 $100$, r2 $200$, r3 $350$, r4 $400$, r6 $600$ <i>(số minh hoạ)</i>.</p>
$$① \\; \\text{mã chung: r1, r2, r3, r4}\\ \\Rightarrow\\ 4\\ \\text{mã}$$""",
           """Ta đối soát hai sổ. Sổ ngân hàng có r một đến r năm, sổ chuyển mạch có r một, r hai, r ba, r bốn và r sáu, số tiền như trên màn hình, đây là số minh hoạ. Phép tính thứ nhất, mã chung là r một, r hai, r ba, r bốn, tức bốn mã."""),
        st("""<p>Trong $4$ mã chung, r3 có tiền khác ($300 \\ne 350$).</p>
$$② \\; \\text{khớp} = 4 - 1 = \\hlg{3},\\quad \\text{lệch tiền} = \\hl{1}$$""",
           """Phép tính thứ hai, trong bốn mã chung, r ba có tiền khác nhau, ba trăm khác ba trăm năm mươi. Vậy khớp là bốn trừ một bằng ba, và lệch tiền là một."""),
        st("""$$③ \\; \\text{chỉ ngân hàng} = 5 - 4 = \\hl{1}\\ (r5)$$""",
           """Phép tính thứ ba, sổ ngân hàng có năm mã, trừ bốn mã chung, còn một mã chỉ có ở ngân hàng, là r năm."""),
        st("""$$④ \\; \\text{chỉ chuyển mạch} = 5 - 4 = \\hl{1}\\ (r6)$$""",
           """Phép tính thứ tư, sổ chuyển mạch có năm mã, trừ bốn mã chung, còn một mã chỉ có ở chuyển mạch, là r sáu."""),
        st("""<p>Dùng lại bốn con số ở ②, ③, ④.</p>
$$⑤ \\; 3 + 1 + 1 + 1 = \\hlg{6}\\ \\text{mã} = 5 + 5 - 4$$""",
           """Phép tính thứ năm, cộng bốn loại, ba cộng một cộng một cộng một, bằng sáu mã, đúng bằng năm cộng năm trừ bốn. Không bỏ sót mã nào."""),
    ], checks=["len({k for k, _ in " + BANK + "} & {k for k, _ in " + SWITCH + "}) == 4", "alg.bnk_reconcile(" + BANK + ", " + SWITCH + ")[0] == 4 - 1 and alg.bnk_reconcile(" + BANK + ", " + SWITCH + ")[3] == 1",
               "alg.bnk_reconcile(" + BANK + ", " + SWITCH + ")[1] == 5 - 4", "alg.bnk_reconcile(" + BANK + ", " + SWITCH + ")[2] == 5 - 4",
               "sum(alg.bnk_reconcile(" + BANK + ", " + SWITCH + ")) == 6 == 5 + 5 - 4"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: tổng tiền hai sổ", [
        st("""<p>Đường khác: cộng tổng tiền mỗi sổ. Ngân hàng $100 + 200 + 300 + 400 + 500 = 1500$. Chuyển mạch $100 + 200 + 350 + 400 + 600 = 1650$.</p>
$$1650 - 1500 = \\hl{150}\\ \\text{chênh lệch}$$""",
           """Kiểm bằng đường khác. Vì mỗi giao dịch đều có tiền, ta cộng tổng tiền của mỗi sổ. Ngân hàng là một nghìn năm trăm. Chuyển mạch là một nghìn sáu trăm năm mươi. Chênh lệch là một trăm năm mươi."""),
        st(table(["nguồn chênh lệch", "số tiền", "giải thích"],
                 [["r3 lệch tiền", "+50", "350 − 300"], ["r6 chỉ chuyển mạch", "+600", "ngân hàng thiếu"], ["r5 chỉ ngân hàng", "−500", "chuyển mạch thiếu"], ["tổng", "+150", "50 + 600 − 500"]]),
           """Bảng này giải thích chênh lệch. Vì mỗi mã góp một phần, nên r ba lệch cộng năm mươi. R sáu chỉ có ở chuyển mạch, cộng sáu trăm. R năm chỉ có ở ngân hàng, trừ năm trăm. Cộng lại được một trăm năm mươi, khớp với hiệu hai tổng."""),
    ], checks=["sum(v for _, v in " + SWITCH + ") - sum(v for _, v in " + BANK + ") == 150", "50 + 600 - 500 == 150"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Ghép hai sổ theo <b>số tiền</b>. Hai giao dịch khác nhau cùng số tiền sẽ ghép nhầm. Phải ghép theo mã tham chiếu.</div>""",
           """Lỗi thứ nhất, của người mới. Ghép hai sổ theo số tiền. Hai giao dịch khác nhau cùng số tiền sẽ ghép nhầm. Phải ghép theo mã tham chiếu."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Lệch ranh giới ngày</b>: giao dịch lúc gần nửa đêm được hai bên tính vào hai ngày khác nhau, nên cuối ngày xuất hiện lệch giả.
<br><span class="note">Cách chữa: thống nhất múi giờ và giờ chốt; đối soát theo cùng thời điểm cắt.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là lệch ranh giới ngày. Giao dịch lúc gần nửa đêm được hai bên tính vào hai ngày khác nhau, nên cuối ngày xuất hiện lệch giả.
           Cách chữa là thống nhất múi giờ và giờ chốt, rồi đối soát theo cùng thời điểm cắt."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Tự động “sửa” sổ</b> cho khớp mà không qua duyệt. Một người vừa tạo vừa duyệt bút toán điều chỉnh là rủi ro gian lận. Cần hai người: người lập và người duyệt.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là tự động sửa sổ cho khớp mà không qua duyệt. Một người vừa tạo vừa duyệt bút toán điều chỉnh là rủi ro gian lận. Cần hai người, một người lập và một người duyệt."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Sổ A: a1 10, a2 20, a3 30. Sổ B: a1 10, a2 25, a4 40. Phân loại bao nhiêu mã mỗi loại?"],
                  ["2", "Tổng số mã khác nhau trong hai sổ?"],
                  ["3", "Quyết định: loại “chỉ ngân hàng có” thì làm gì đầu tiên?"]]),
           """Đến lượt bạn. Câu một, sổ A có a một mười, a hai hai mươi, a ba ba mươi. Sổ B có a một mười, a hai hai mươi lăm, a bốn bốn mươi. Phân loại bao nhiêu mã mỗi loại? Câu hai, tổng số mã khác nhau trong hai sổ?
           Câu ba, loại chỉ ngân hàng có thì làm gì đầu tiên? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: chung là a1 và a2. a1 khớp, a2 lệch tiền ($20 \\ne 25$). a3 chỉ A, a4 chỉ B.</p>
$$\\text{khớp } 1,\\ \\text{lệch } 1,\\ \\text{chỉ A } 1,\\ \\text{chỉ B } 1$$""",
           """Đáp án câu một. Mã chung là a một và a hai. A một khớp. A hai lệch tiền, hai mươi khác hai mươi lăm. A ba chỉ có ở sổ A, a bốn chỉ có ở sổ B. Mỗi loại một mã."""),
        st("""$$3 + 3 - 2 = \\hlg{4}\\ \\text{mã}$$""",
           """Đáp án câu hai. Mỗi sổ ba mã, hai mã chung, nên ba cộng ba trừ hai bằng bốn mã khác nhau, khớp với bốn loại mỗi loại một."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tra soát trạng thái thật của giao dịch trước", "biết đã hạch toán hay chưa rồi mới xử lý", "mất một bước"],
                  ["ghi nợ hoặc hoàn tiền ngay theo phỏng đoán", "nhanh", "có thể trừ hoặc hoàn trùng"]]),
           """Đáp án câu ba. Việc đầu tiên là tra soát trạng thái thật của giao dịch, để biết đã hạch toán hay chưa, rồi mới xử lý. Đoán rồi ghi nợ hoặc hoàn tiền ngay có thể gây trừ hoặc hoàn trùng."""),
    ], checks=["alg.bnk_reconcile([('a1', 10), ('a2', 20), ('a3', 30)], [('a1', 10), ('a2', 25), ('a4', 40)]) == (1, 1, 1, 1)", "3 + 3 - 2 == 4"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("kết quả có thể mất", "hai bên giữ hai sổ", "ghép theo mã tham chiếu", "bốn loại", "mỗi loại một hành động"),
           """Tổng kết chuỗi logic. Kết quả có thể mất, nên hai bên giữ hai sổ. Ghép theo mã tham chiếu, chia bốn loại, mỗi loại một hành động."""),
        st("""<div class='box key'><b>Tư duy:</b> đối soát không phải việc cuối ngày cho xong, mà là <b>lưới an toàn</b> bắt mọi trường hợp “chưa biết” mà hệ thống thời gian thực để lọt.</div>""",
           """Điều cần mang theo. Đối soát không phải việc cuối ngày cho xong, mà là lưới an toàn, bắt mọi trường hợp chưa biết mà hệ thống thời gian thực để lọt."""),
    ])
    return lesson("L12", "napas_247_doi_soat", "Bài 12 — Chuyển mạch liên ngân hàng và đối soát hai bên",
                  "curriculum/bnk.yaml L12; audit/bnk/verify_bnk.py L12; mô hình chung của chuyển mạch liên ngân hàng; chi tiết NAPAS theo đặc tả kết nối chính thức của NAPAS (không có trong kho)",
                  ["Vẽ đường đi của một lệnh chuyển nhanh và chỉ ra chỗ có thể mất dấu", "Phân loại hai danh sách giao dịch thành bốn loại theo mã tham chiếu",
                   "Kiểm lại bằng đếm bù trừ và tổng tiền", "Nêu hành động đầu tiên cho từng loại lệch"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
