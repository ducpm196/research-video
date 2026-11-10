from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao phản hồi về không đúng thứ tự, và hết giờ chờ thì làm gì?", [
        st("""<p>Kênh số gửi $5$ lệnh sang lõi ngân hàng qua hàng đợi. Phản hồi quay về <b>lộn xộn</b>: lệnh $2$ trả lời trước lệnh $0$.</p>
<div class="box key">Nếu ghép phản hồi theo <b>thứ tự đến</b>, cả $5$ lệnh nhận nhầm kết quả. Phải ghép theo <b>mã tương quan</b>.</div>""",
           """Chào bạn, kênh số gửi năm lệnh sang lõi ngân hàng qua hàng đợi. Phản hồi quay về lộn xộn, lệnh hai được trả lời trước lệnh không.
           Nếu ghép phản hồi theo thứ tự đến, cả năm lệnh nhận nhầm kết quả. Phải ghép theo mã tương quan."""),
        st(table(["cách ghép", "số phản hồi đúng (thứ tự về: 2, 0, 1, 4, 3)"],
                 [["theo thứ tự đến", "0 trên 5"], ["theo mã tương quan", "5 trên 5"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài. Ghép theo thứ tự đến thì không phản hồi nào đúng. Ghép theo mã tương quan thì đúng cả năm.
           Hôm nay ta học thêm một việc khó hơn, là khi hết giờ chờ mà không biết lõi ngân hàng đã hạch toán hay chưa."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: những điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Kênh số", "ứng dụng ngân hàng trên điện thoại hay trang web mà khách dùng", "ứng dụng chuyển tiền"],
                  ["② Lõi ngân hàng (core banking)", "hệ thống trung tâm giữ tài khoản và sổ cái (sổ ghi mọi khoản tiền vào ra)", "T24"],
                  ["③ Hạch toán", "ghi khoản tiền vào sổ cái, tức là trừ hay cộng tiền thật sự", "ghi nợ 500 000 vào tài khoản A"]]),
           """Trước hết ta cần hiểu vài điều. Kênh số là ứng dụng ngân hàng trên điện thoại hay trang web mà khách dùng. Lõi ngân hàng là hệ thống trung tâm giữ tài khoản và sổ cái, tức sổ ghi mọi khoản tiền vào ra.
           Hạch toán là ghi khoản tiền vào sổ cái, tức là trừ hay cộng tiền thật sự, ví dụ ghi nợ năm trăm nghìn vào tài khoản A."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ Hàng đợi", "nơi xếp thông điệp (gói dữ liệu gửi giữa hai hệ thống), lấy theo thứ tự vào", "lệnh 0, 1, 2 xếp hàng"],
                  ["⑤ Thông điệp có tiêu đề", "ngoài nội dung còn có các nhãn như mã thông điệp", "mã thông điệp M7"],
                  ["⑥ Yêu cầu – phản hồi", "bên gửi hỏi, bên nhận làm rồi trả lời", "hỏi chuyển tiền, trả kết quả"]]),
           """Hàng đợi là nơi xếp thông điệp, tức gói dữ liệu gửi giữa hai hệ thống, và lấy ra theo thứ tự vào. Thông điệp ngoài nội dung còn có các nhãn như mã thông điệp.
           Còn yêu cầu và phản hồi là bên gửi hỏi, bên nhận làm rồi trả lời.""", clear=True),
        st("""$$5! = 5 \\cdot 4 \\cdot 3 \\cdot 2 \\cdot 1 = 120$$""",
           """Một phép đếm cần dùng. Năm phản hồi có thể về theo một trăm hai mươi thứ tự khác nhau, vì năm nhân bốn nhân ba nhân hai nhân một bằng một trăm hai mươi."""),
    ], checks=["5 * 4 * 3 * 2 * 1 == 120 == math.factorial(5)"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["Temenos T24", "phần mềm lõi ngân hàng (nơi giữ tài khoản và sổ cái)"],
                  ["OFS", "Open Financial Service: bản tin dạng chữ để gọi chức năng của lõi từ bên ngoài"],
                  ["IBM MQ", "phần mềm hàng đợi thông điệp, chuyển bản tin giữa hệ thống"],
                  ["MessageID / CorrelationID", "mã của thông điệp / mã của thông điệp mà phản hồi này trả lời"],
                  ["hết giờ chờ (timeout)", "không nhận phản hồi trong thời hạn, chưa biết kết quả"]]),
           """Bảng này giải mã năm từ. Temenos T24 là phần mềm lõi ngân hàng. OFS là bản tin dạng chữ để gọi chức năng của lõi từ bên ngoài. IBM MQ là phần mềm hàng đợi, chuyển bản tin giữa các hệ thống.
           Mã thông điệp là mã của chính thông điệp, còn mã tương quan là mã của thông điệp mà phản hồi này trả lời. Hết giờ chờ là khi không nhận được phản hồi trong thời hạn."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: hai hàng đợi và mã tương quan", [
        st(svg(1500, 440,
               box(40, 160, 260, 110, ["Kênh số", "gửi lệnh"], C_BLUE, bold=True),
               box(420, 40, 380, 90, "hàng đợi yêu cầu", C_AMBER), box(420, 300, 380, 90, "hàng đợi phản hồi", C_AMBER),
               box(960, 160, 300, 110, ["Lõi ngân hàng", "xử lý song song"], C_GREEN, bold=True),
               arrow(300, 190, 415, 100, "#2a78d6", "M7"), arrow(800, 95, 955, 190, "#475569"),
               arrow(955, 245, 805, 340, "#16a34a", "tương quan = M7"), arrow(415, 345, 300, 250, "#16a34a"),
               txt(750, 425, "mẫu minh hoạ, không phải cú pháp T24 thật", 22, "middle", "#6b7280")),
           """Hình cho thấy luồng chung. Kênh số đặt lệnh vào hàng đợi yêu cầu, mang mã thông điệp, ví dụ M bảy. Lõi ngân hàng lấy ra xử lý, có thể song song nhiều lệnh.
           Phản hồi được đặt vào hàng đợi phản hồi, mang mã tương quan bằng đúng M bảy. Nhờ đó kênh số biết phản hồi nào trả lời lệnh nào. Hình này là mẫu minh hoạ, không phải cú pháp thật của T hai mươi tư."""),
        st(svg(1500, 420,
               txt(60, 50, "Lệnh gửi theo thứ tự:", 26, "start", "#1f2937", True),
               box(60, 80, 160, 60, "0", C_BLUE), box(240, 80, 160, 60, "1", C_BLUE), box(420, 80, 160, 60, "2", C_BLUE), box(600, 80, 160, 60, "3", C_BLUE), box(780, 80, 160, 60, "4", C_BLUE),
               txt(560, 232, "Phản hồi về theo thứ tự:", 26, "start", "#1f2937", True),
               box(60, 250, 160, 60, "2", C_AMBER), box(240, 250, 160, 60, "0", C_AMBER), box(420, 250, 160, 60, "1", C_AMBER), box(600, 250, 160, 60, "4", C_AMBER), box(780, 250, 160, 60, "3", C_AMBER),
               arrow(500, 142, 140, 246, "#dc2626", None, dash=True),
               txt(1200, 150, "Ghép theo thứ tự đến:", 26, "middle", "#dc2626", True), txt(1200, 190, "phản hồi 2 bị gán cho lệnh 0 (sai)", 24, "middle", "#dc2626"),
               txt(1200, 300, "Ghép theo mã tương quan:", 26, "middle", "#16a34a", True), txt(1200, 340, "phản hồi 2 → lệnh 2 (đúng)", 24, "middle", "#16a34a")),
           """Hình thứ hai cho thấy vì sao thứ tự đến không dùng được. Lệnh gửi theo thứ tự không, một, hai, ba, bốn. Phản hồi về theo thứ tự hai, không, một, bốn, ba.
           Ghép theo thứ tự đến thì phản hồi của lệnh hai bị gán cho lệnh không, sai. Ghép theo mã tương quan thì phản hồi hai về đúng lệnh hai."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: ghép đúng và xử lý khi hết giờ chờ", [
        st("""<p><b>Bước 1.</b> Lõi xử lý song song, nên thứ tự phản hồi <b>có thể không</b> theo thứ tự gửi. $5$ phản hồi có thể về theo $120$ thứ tự.</p>
<span class='note'>Làm thử: chỉ $1$ thứ tự trong $120$ là đúng thứ tự gửi.</span>""",
           """Bước một, vì lõi xử lý song song, nên thứ tự phản hồi có thể không theo thứ tự gửi. Năm phản hồi có thể về theo một trăm hai mươi thứ tự. Làm thử, chỉ một thứ tự trong số đó trùng đúng thứ tự gửi."""),
        st("""<p><b>Bước 2.</b> Mỗi phản hồi mang <b>mã tương quan</b> bằng mã thông điệp của lệnh. Bên gửi giữ bảng “mã → lệnh đang chờ” rồi tra theo mã.</p>
<span class='note'>Làm thử: mọi phản hồi đều tìm ra lệnh của mình → $5$ trên $5$.</span>""",
           """Bước hai, vì mỗi phản hồi mang mã tương quan bằng mã thông điệp của lệnh, nên bên gửi giữ một bảng mã và lệnh đang chờ, rồi tra theo mã. Làm thử, mọi phản hồi đều tìm ra lệnh của mình, năm trên năm."""),
        st("""<p><b>Bước 3.</b> Hết giờ chờ chỉ cho biết chưa có phản hồi, không cho biết lõi đã hạch toán chưa. <b>Truy vấn trạng thái trước</b>, rồi mới quyết định thử lại.</p>
<span class='note'>Làm thử: đã hạch toán mà gửi lại ngay → ghi nợ $2$ lần.</span>
<p>Lưu ý: “chưa thấy” chưa chắc chắn, vì lệnh gốc có thể còn trong hàng đợi. Gửi lại phải dùng <b>cùng mã tham chiếu</b> (mã riêng của lệnh chuyển tiền, giữ nguyên qua mọi lần gửi) để lõi từ chối trùng, hoặc đặt hạn sống (Expiry) cho bản tin.</p>""",
           """Bước ba, vì hết giờ chờ chỉ cho biết chưa có phản hồi, chứ không cho biết lõi đã hạch toán chưa, nên ta truy vấn trạng thái trước, rồi mới quyết định thử lại. Làm thử, nếu đã hạch toán mà gửi lại ngay, khách bị ghi nợ hai lần.
           Lưu ý, kết quả chưa thấy cũng chưa chắc chắn, vì lệnh gốc có thể còn nằm trong hàng đợi. Vì vậy gửi lại phải dùng cùng mã tham chiếu, tức mã riêng của lệnh chuyển tiền được giữ nguyên qua mọi lần gửi, để lõi từ chối trùng, hoặc đặt hạn sống cho bản tin.""", clear=True),
    ], checks=["math.factorial(5) == 120", "alg.bnk_reply_match([2, 0, 1, 4, 3]) == (0, 5)", "alg.bnk_unknown_outcome(True, False) == 2"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Năm lệnh mã $0..4$. Phản hồi về theo thứ tự $2, 0, 1, 4, 3$.</p>
$$① \\; \\text{ghép theo thứ tự đến: } 0 \\text{ trên } 5\\ \\text{đúng}$$""",
           """Ta tính hai trường hợp. Năm lệnh có mã từ không tới bốn. Phản hồi về theo thứ tự hai, không, một, bốn, ba. Phép tính thứ nhất, ghép theo thứ tự đến thì không phản hồi nào đúng."""),
        st("""<p>Vì sao $0$? Vị trí về thứ $k$ chứa mã $2, 0, 1, 4, 3$, và <b>không vị trí nào trùng mã của nó</b> ($2 \\ne 0$, $0 \\ne 1$, $1 \\ne 2$, $4 \\ne 3$, $3 \\ne 4$).</p>
$$② \\; \\text{số vị trí trùng} = \\hl{0}$$""",
           """Phép tính thứ hai, vì sao là không. Vị trí thứ nhất chứa hai, khác không. Vị trí thứ hai chứa không, khác một. Cứ thế, không vị trí nào trùng mã của nó. Số vị trí trùng là không."""),
        st("""$$③ \\; \\text{ghép theo mã tương quan: } \\hlg{5} \\text{ trên } 5\\ \\text{đúng}$$""",
           """Phép tính thứ ba, ghép theo mã tương quan thì cả năm đều đúng, vì mỗi phản hồi tự mang mã của lệnh."""),
        st("""<p>Hết giờ chờ, lõi <b>đã</b> hạch toán, gửi lại không truy vấn.</p>
$$④ \\; 1 + 1 = \\hl{2}\\ \\text{lần ghi nợ}$$""",
           """Phép tính thứ tư, hết giờ chờ, nhưng lõi đã hạch toán, và ta gửi lại mà không truy vấn. Số lần ghi nợ là một cộng một, bằng hai."""),
        st("""<p>Cùng tình huống nhưng <b>truy vấn trạng thái trước</b>: thấy đã hạch toán nên không gửi lại.</p>
$$⑤ \\; \\text{số lần ghi nợ} = \\hlg{1}$$""",
           """Phép tính thứ năm, cùng tình huống nhưng truy vấn trạng thái trước. Thấy đã hạch toán nên không gửi lại, số lần ghi nợ là một."""),
    ], checks=["alg.bnk_reply_match([2, 0, 1, 4, 3])[0] == 0 and all(r != k for k, r in enumerate([2, 0, 1, 4, 3]))",
               "alg.bnk_reply_match([2, 0, 1, 4, 3])[1] == 5", "1 + 1 == alg.bnk_unknown_outcome(True, False)", "alg.bnk_unknown_outcome(True, True) == 1"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm các thứ tự không trùng", [
        st("""<p>Đường khác: vét cạn $120$ thứ tự, đếm những thứ tự mà <b>không</b> phản hồi nào về đúng vị trí. Đáp số là $44$, và thứ tự $2, 0, 1, 4, 3$ nằm trong $44$ đó.</p>
$$\\text{44 trên 120} \\approx \\hl{37\\%}$$
<p class="small">Đây là xác suất nếu mọi thứ tự về đều có khả năng như nhau (mô hình minh hoạ).</p>""",
           """Kiểm bằng đường khác. Ta vét cạn một trăm hai mươi thứ tự, đếm những thứ tự mà không phản hồi nào về đúng vị trí. Có bốn mươi bốn thứ tự như vậy, và thứ tự của ta nằm trong đó.
           Bốn mươi bốn trên một trăm hai mươi là khoảng ba mươi bảy phần trăm.
           Ta gọi đó là xác suất trong mô hình minh hoạ, vì ta giả sử mọi thứ tự về đều có khả năng như nhau."""),
        st(table(["tình huống", "đã hạch toán?", "truy vấn trước?", "số lần ghi nợ"],
                 [["A", "có", "không", "2 (sai)"], ["B", "có", "có", "1"], ["C", "chưa", "có", "1 (gửi lại cùng mã tham chiếu)"], ["D", "chưa", "không", "1 nếu lệnh gốc đã mất hẳn; 2 nếu lệnh gốc tới muộn mà lần gửi lại khác mã"]]),
           """Bảng này tổng hợp bốn tình huống. Tình huống A chắc chắn ghi nợ hai lần. Vì truy vấn trước cho ta biết đã hạch toán chưa, nên tình huống B và C đều đúng một lần. Ở tình huống C, lần gửi lại mang cùng mã tham chiếu, để lõi từ chối nếu lệnh gốc tới muộn.
           Tình huống D chỉ đúng một lần khi lệnh gốc đã mất hẳn. Nếu lệnh gốc còn trong hàng đợi và tới muộn, mà lần gửi lại mang mã khác, khách vẫn bị ghi nợ hai lần.""", clear=True),
    ], checks=["sum(1 for p in __import__('itertools').permutations(range(5)) if all(p[i] != i for i in range(5))) == 44",
               "round(44 / 120 * 100) == 37", "[alg.bnk_unknown_outcome(a, b) for a, b in ((True, False), (True, True), (False, True), (False, False))] == [2, 1, 1, 1]"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Giả định phản hồi về <b>đúng thứ tự gửi</b>. Khi tải nhẹ có thể đúng, khi tải cao thì sai, nên lỗi chỉ hiện lúc cao điểm.</div>""",
           """Lỗi thứ nhất, của người mới. Giả định phản hồi về đúng thứ tự gửi. Khi tải nhẹ có thể đúng, khi tải cao thì sai, nên lỗi chỉ hiện lúc cao điểm."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Hết giờ chờ rồi gửi lại ngay</b>. Lõi có thể đã hạch toán, nên khách bị ghi nợ hai lần.
<br><span class="note">Cách chữa: truy vấn trạng thái bằng mã tham chiếu của lệnh trước khi gửi lại, và gắn khoá lũy đẳng vào lệnh.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là hết giờ chờ rồi gửi lại ngay. Lõi có thể đã hạch toán, nên khách bị ghi nợ hai lần.
           Cách chữa là truy vấn trạng thái bằng mã tham chiếu của lệnh trước khi gửi lại, và gắn khoá lũy đẳng vào lệnh."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nhiều bản của dịch vụ cùng đọc <b>một hàng đợi phản hồi</b>, nên bản này lấy nhầm phản hồi của bản kia.
Mỗi bản cần hàng đợi phản hồi riêng, hoặc chỉ nhận thông điệp có mã tương quan của mình.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nhiều bản của dịch vụ cùng đọc một hàng đợi phản hồi, nên bản này lấy nhầm phản hồi của bản kia.
           Mỗi bản cần hàng đợi phản hồi riêng, hoặc chỉ nhận thông điệp có mã tương quan của mình."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Phản hồi về theo thứ tự 0, 2, 1, 3, 4. Ghép theo thứ tự đến đúng mấy lệnh?"],
                  ["2", "Lõi chưa hạch toán, bạn truy vấn rồi gửi lại. Ghi nợ mấy lần?"],
                  ["3", "Quyết định: khi hết giờ chờ với lệnh chuyển tiền, làm gì đầu tiên?"]]),
           """Đến lượt bạn. Câu một, phản hồi về theo thứ tự không, hai, một, ba, bốn, ghép theo thứ tự đến đúng mấy lệnh? Câu hai, lõi chưa hạch toán, bạn truy vấn rồi gửi lại, ghi nợ mấy lần?
           Câu ba, khi hết giờ chờ với lệnh chuyển tiền, việc đầu tiên là gì? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: vị trí $0$ chứa $0$ ✓, vị trí $3$ chứa $3$ ✓, vị trí $4$ chứa $4$ ✓; vị trí $1$ chứa $2$, vị trí $2$ chứa $1$.</p>
$$\\hl{3}\\ \\text{trên } 5$$""",
           """Đáp án câu một. Vị trí không chứa không, đúng. Vị trí ba chứa ba, vị trí bốn chứa bốn, đúng. Vị trí một và hai chứa nhầm. Vậy đúng ba trên năm."""),
        st("""$$\\text{ghi nợ} = \\hlg{1}\\ \\text{lần (chỉ lần gửi lại)}$$""",
           """Đáp án câu hai. Lõi chưa hạch toán nên lần đầu chưa trừ gì, và lần gửi lại trừ đúng một lần."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["truy vấn trạng thái trước, rồi mới thử lại", "không ghi nợ trùng", "chậm hơn một vòng hỏi"],
                  ["gửi lại ngay", "nhanh", "có thể ghi nợ hai lần"]]),
           """Đáp án câu ba. Việc đầu tiên là truy vấn trạng thái bằng mã tham chiếu của lệnh, rồi mới quyết định thử lại. Chậm hơn một vòng hỏi, nhưng không ghi nợ trùng. Gửi lại ngay thì nhanh nhưng có thể ghi nợ hai lần."""),
    ], checks=["alg.bnk_reply_match([0, 2, 1, 3, 4])[0] == 3", "alg.bnk_unknown_outcome(False, True) == 1"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("lõi xử lý song song", "phản hồi lộn xộn", "ghép theo mã tương quan", "hết giờ chờ → truy vấn trước"),
           """Tổng kết chuỗi logic. Lõi xử lý song song nên phản hồi lộn xộn. Ghép theo mã tương quan. Hết giờ chờ thì truy vấn trạng thái trước khi thử lại."""),
        st("""<div class='box key'><b>Tư duy:</b> “không có phản hồi” là <b>trạng thái chưa biết</b>, không phải “thất bại”. Chưa biết thì đi hỏi, đừng đoán.</div>""",
           """Điều cần mang theo. Không có phản hồi là trạng thái chưa biết, không phải thất bại. Chưa biết thì đi hỏi, đừng đoán."""),
    ])
    return lesson("L10", "t24_ofs_ibm_mq_tuong_quan", "Bài 10 — Lõi ngân hàng T24: OFS, IBM MQ và mã tương quan",
                  "curriculum/bnk.yaml L10; audit/bnk/verify_bnk.py L10; IBM MQ / JMS: MessageID và CorrelationID (khái niệm chung); OFS: tên gọi theo Temenos, bản tin trong bài là mẫu minh hoạ",
                  ["Ghép phản hồi theo mã tương quan thay vì thứ tự đến", "Tính xác suất phản hồi không trùng thứ tự gửi bằng vét cạn",
                   "Xử lý đúng khi hết giờ chờ: truy vấn trạng thái trước", "Tránh nhiều bản dịch vụ lấy nhầm phản hồi của nhau"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
