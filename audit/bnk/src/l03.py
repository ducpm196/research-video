from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao một lần bấm chuyển tiền lại bị trừ ba lần?", [
        st("""<p>Khách bấm chuyển $500\\,000$ đồng. Mạng chập chờn nên ứng dụng không nhận được phản hồi và <b>tự thử lại</b> hai lần nữa.</p>
<div class="box key">Máy chủ nhận đủ <b>ba</b> yêu cầu. Nếu không phòng bị, tài khoản bị trừ <b>ba lần</b>.</div>""",
           """Chào bạn, khách bấm chuyển năm trăm nghìn đồng. Mạng chập chờn nên ứng dụng không nhận được phản hồi và tự thử lại thêm hai lần.
           Máy chủ nhận đủ ba yêu cầu, và nếu không phòng bị, tài khoản bị trừ ba lần."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["vì sao thử lại là bình thường", "mạng có thể mất phản hồi, người gọi không biết việc đã xong chưa"],
                  ["làm sao thử lại mà không trừ trùng", "khoá lũy đẳng: cùng khoá thì chỉ làm một lần"]]),
           """Hôm nay ta trả lời hai câu. Vì sao thử lại là chuyện bình thường, và làm sao thử lại mà không trừ trùng.
           Đáp án là khoá lũy đẳng: cùng một khoá thì chỉ làm một lần."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① HTTP và REST API", "HTTP là giao thức web: mỗi yêu cầu gồm một phương thức (GET, POST…) và một đường dẫn; REST API là cách một dịch vụ mở chức năng qua các đường dẫn đó", "<code>POST /transfers</code>"],
                  ["② Yêu cầu và phản hồi", "người gọi gửi yêu cầu, máy chủ trả phản hồi", "yêu cầu chuyển tiền, phản hồi thành công"],
                  ["③ Mã trạng thái", "số báo kết quả: 2xx thành công, 4xx lỗi người gọi, 5xx lỗi máy chủ", "200 thành công, 404 không thấy, 503 tạm không phục vụ"],
                  ["④ Hết giờ chờ", "chờ quá lâu thì người gọi bỏ cuộc, dù máy chủ có thể đã làm xong", "chờ 3 giây không thấy gì"]]),
           """Trước hết ta cần hiểu bốn điều. HTTP là giao thức web. Mỗi yêu cầu gồm một phương thức, như lấy hay gửi, và một đường dẫn. REST API là cách một dịch vụ mở chức năng của nó qua các đường dẫn đó.
           Người gọi gửi yêu cầu, máy chủ trả phản hồi. Mã trạng thái báo kết quả. Các mã bắt đầu bằng chữ số hai là thành công, bắt đầu bằng bốn là lỗi người gọi, bắt đầu bằng năm là lỗi máy chủ.
           Còn hết giờ chờ nghĩa là người gọi bỏ cuộc, dù máy chủ có thể đã làm xong."""),
        st("""$$2\\,000\\,000 - 500\\,000 = 1\\,500\\,000$$""",
           """Một ví dụ số. Số dư hai triệu, trừ năm trăm nghìn còn một triệu năm trăm nghìn. Đó là kết quả đúng cho một lần chuyển."""),
    ], checks=["2000000 - 500000 == 1500000"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["GET", "đọc dữ liệu, không làm thay đổi gì: an toàn"],
                  ["POST", "tạo hoặc thực hiện việc mới: mỗi lần gọi có thể làm thêm một việc"],
                  ["PUT", "ghi đè tới trạng thái đã cho: gọi nhiều lần cũng cho một kết quả"],
                  ["lũy đẳng", "gọi một lần hay nhiều lần, kết quả cuối cùng như nhau"],
                  ["khoá lũy đẳng", "mã duy nhất do người gọi sinh ra cho mỗi việc, gửi kèm mọi lần thử"]]),
           """Bảng này giải mã năm từ. G E T là đọc, không thay đổi gì. P O S T là làm một việc mới, mỗi lần gọi có thể làm thêm. P U T là ghi đè tới trạng thái đã cho, gọi nhiều lần cho cùng kết quả.
           Lũy đẳng nghĩa là gọi một lần hay nhiều lần, kết quả cuối như nhau. Khoá lũy đẳng là mã duy nhất người gọi gửi kèm mọi lần thử."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: phản hồi mất, thử lại, và khoá chặn trùng", [
        st(svg(1500, 420,
               box(40, 160, 260, 100, ["Ứng dụng", "người gọi"], C_BLUE, bold=True),
               box(1200, 160, 260, 100, ["Máy chủ", "đã trừ tiền"], C_GREEN, bold=True),
               arrow(300, 190, 1195, 190, "#2a78d6", "1. chuyển 500 000"),
               arrow(1195, 235, 305, 235, "#dc2626", "2. phản hồi bị mất (sai)", dash=True),
               arrow(300, 290, 1195, 290, "#2a78d6", "3. không thấy gì nên thử lại"),
               txt(750, 380, "Người gọi không phân biệt được “chưa làm” và “đã làm nhưng mất phản hồi”", 26, "middle", "#1f2937", True)),
           """Hình cho thấy điều mấu chốt. Ứng dụng gửi lệnh chuyển. Máy chủ đã trừ tiền xong, nhưng phản hồi bị mất trên đường về. Ứng dụng không thấy gì nên thử lại.
           Người gọi không thể phân biệt hai trường hợp, là chưa làm, và đã làm nhưng mất phản hồi."""),
        st(svg(1500, 440,
               box(40, 160, 240, 100, ["Ứng dụng", "khoá k1"], C_BLUE, bold=True),
               box(520, 40, 420, 100, "lần 1: chưa thấy k1 → làm", C_GREEN),
               box(520, 170, 420, 100, "lần 2: đã có k1 → trả kết quả cũ", C_AMBER),
               box(520, 300, 420, 100, "lần 3: đã có k1 → trả kết quả cũ", C_AMBER),
               box(1120, 160, 340, 100, ["bảng khoá", "k1 → kết quả"], C_PURPLE, bold=True),
               arrow(280, 190, 515, 90, "#2a78d6"), arrow(280, 210, 515, 220, "#2a78d6"), arrow(280, 235, 515, 345, "#2a78d6"),
               arrow(945, 90, 1115, 190, "#9333ea", "ghi"), arrow(945, 220, 1115, 220, "#9333ea", "tra")),
           """Có khoá lũy đẳng thì khác. Mỗi lần thử đều mang cùng khoá k một. Lần một, máy chủ chưa thấy khoá nên làm việc và ghi khoá cùng kết quả vào bảng.
           Lần hai và lần ba, máy chủ thấy khoá đã có, nên trả lại kết quả cũ mà không làm lại."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: thử lại an toàn", [
        st("""<p><b>Bước 1.</b> Hết giờ chờ chỉ cho biết <b>chưa nhận phản hồi</b>, không cho biết máy chủ đã làm hay chưa. Muốn biết kết quả, người gọi phải gửi lại hoặc hỏi lại, nên thử lại là chuyện thường xảy ra.</p>
<span class='note'>Làm thử: 3 lần gửi, 0 phản hồi tới nơi, vẫn không biết số lần đã trừ.</span>""",
           """Bước một, vì hết giờ chờ chỉ cho biết chưa nhận được phản hồi, chứ không cho biết máy chủ đã làm hay chưa, nên muốn biết kết quả người gọi phải gửi lại hoặc hỏi lại. Thử lại vì thế là chuyện thường xảy ra.
           Làm thử, ba lần gửi mà không phản hồi nào tới nơi, người gọi vẫn không biết đã trừ mấy lần."""),
        st("""<p><b>Bước 2.</b> Người gọi sinh <b>một khoá duy nhất cho mỗi việc</b> rồi gửi kèm cả ba lần. Khoá đại diện cho <i>việc</i>, không đại diện cho <i>lần gửi</i>.</p>
<span class='note'>Làm thử: ba lần gửi, một khoá k1.</span>""",
           """Bước hai, vì cả ba lần gửi đều là cùng một việc, nên người gọi sinh một khoá duy nhất cho việc đó và gửi kèm mọi lần. Khoá đại diện cho việc, không đại diện cho lần gửi.
           Làm thử, ba lần gửi nhưng chỉ có một khoá."""),
        st("""<p><b>Bước 3.</b> Máy chủ tra khoá. Chưa có thì làm rồi lưu <b>trong cùng một giao dịch</b> với việc trừ tiền. Đã có thì trả kết quả đã lưu.</p>
<span class='note'>Làm thử: số lần trừ tiền = số khoá khác nhau = 1.</span>""",
           """Bước ba, máy chủ tra khoá. Chưa có thì làm việc và lưu khoá trong cùng một giao dịch với việc trừ tiền. Đã có thì trả kết quả đã lưu.
           Vì vậy số lần trừ tiền bằng số khoá khác nhau, tức là một."""),
    ], checks=["len({'k1', 'k1', 'k1'}) == 1", "alg.bnk_unique_key_rows(3) == 1"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Số dư đầu $2\\,000\\,000$, mỗi lần chuyển $500\\,000$, thử tổng cộng $3$ lần.</p>
$$① \\; \\text{không khoá: } 3 \\cdot 500\\,000 = \\hl{1\\,500\\,000}\\ \\text{đã trừ}$$""",
           """Ta tính cả hai trường hợp. Số dư đầu hai triệu, mỗi lần chuyển năm trăm nghìn, thử ba lần. Phép tính thứ nhất, không có khoá, bị trừ ba nhân năm trăm nghìn, là một triệu năm trăm nghìn."""),
        st("""<p>Dùng lại $1\\,500\\,000$ ở phép ①.</p>
$$② \\; 2\\,000\\,000 - 1\\,500\\,000 = \\hl{500\\,000}\\ \\text{còn lại}$$""",
           """Phép tính thứ hai, số dư còn hai triệu trừ một triệu năm trăm nghìn, bằng năm trăm nghìn."""),
        st("""$$③ \\; \\text{có khoá: } 1 \\cdot 500\\,000 = \\hlg{500\\,000}\\ \\text{đã trừ}$$""",
           """Phép tính thứ ba, khi có khoá, chỉ trừ một lần, tức năm trăm nghìn."""),
        st("""$$④ \\; 2\\,000\\,000 - 500\\,000 = \\hlg{1\\,500\\,000}\\ \\text{còn lại}$$""",
           """Phép tính thứ tư, số dư còn hai triệu trừ năm trăm nghìn, bằng một triệu năm trăm nghìn, đúng như một lần chuyển."""),
        st("""$$⑤ \\; 1\\,500\\,000 - 500\\,000 = \\hl{1\\,000\\,000}\\ \\text{bị trừ oan khi không có khoá}$$""",
           """Phép tính thứ năm, chênh lệch giữa hai trường hợp là một triệu năm trăm nghìn trừ năm trăm nghìn, bằng một triệu, chính là số tiền bị trừ oan khi không có khoá."""),
    ], checks=["3 * 500000 == 1500000", "alg.bnk_retry_sim(2000000, 500000, 3, False) == 500000",
               "alg.bnk_retry_sim(2000000, 500000, 3, True) == 1500000",
               "alg.bnk_retry_sim(2000000, 500000, 3, True) - alg.bnk_retry_sim(2000000, 500000, 3, False) == 1000000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: để cơ sở dữ liệu chặn trùng", [
        st("""<p>Đường khác: tạo bảng có ràng buộc <code>UNIQUE</code> trên khoá, rồi chèn cùng khoá ba lần. Ràng buộc cho phép <b>đúng một dòng</b> vào.</p>
$$\\text{số dòng} = \\hl{1}$$""",
           """Kiểm bằng đường khác. Trong cơ sở dữ liệu, bảng là nơi lưu các dòng, và ràng buộc duy nhất là luật cấm hai dòng có cùng giá trị ở một cột. Ta tạo một bảng có ràng buộc duy nhất trên khoá rồi chèn cùng khoá ba lần. Vì cơ sở dữ liệu chỉ cho một dòng vào, số dòng cuối cùng là một.
           Cách này chặn trùng ngay cả khi hai lần thử đến cùng lúc."""),
        st(table(["phương thức", "an toàn (không đổi dữ liệu)", "lũy đẳng"],
                 [["GET", "có", "có"], ["PUT", "không", "có"], ["DELETE", "không", "có"], ["POST", "không", "không (cần khoá)"]]),
           """Bảng này tổng hợp các phương thức. Đọc là an toàn và lũy đẳng. Ghi đè và xoá thay đổi dữ liệu nhưng lũy đẳng. Còn P O S T không lũy đẳng, nên cần khoá nếu muốn thử lại an toàn."""),
    ], checks=["alg.bnk_unique_key_rows(3) == 1", "alg.bnk_unique_key_rows(1) == 1"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Cho rằng gọi lại cho an toàn. Với việc thay đổi tiền, gọi lại <b class="red">không</b> an toàn nếu không có khoá.</div>""",
           """Lỗi thứ nhất, của người mới. Cho rằng cứ gọi lại là an toàn. Với việc thay đổi tiền, gọi lại không an toàn nếu không có khoá."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Kiểm tra rồi mới chèn</b>: đọc xem khoá có chưa, chưa có thì làm. Hai lần thử đến cùng lúc đều thấy “chưa có” rồi đều làm.
<br><span class="note">Cách chữa: ràng buộc UNIQUE, để cơ sở dữ liệu quyết định.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là kiểm tra rồi mới chèn. Đọc xem khoá đã có chưa, chưa có thì làm. Hai lần thử đến cùng lúc đều thấy chưa có, nên đều làm.
           Cách chữa là dùng ràng buộc duy nhất, để cơ sở dữ liệu quyết định."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Dùng lại cùng khoá cho yêu cầu <b>khác nội dung</b>. Máy chủ phải từ chối thay vì trả kết quả cũ. Khoá cũng cần hạn lưu đủ dài hơn thời gian thử lại.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là dùng lại cùng khoá cho một yêu cầu khác nội dung. Máy chủ phải từ chối thay vì trả kết quả cũ.
           Khoá cũng cần được lưu lâu hơn thời gian người gọi còn thử lại."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Số dư 1 000 000, chuyển 200 000, thử 5 lần, không khoá. Còn bao nhiêu?"],
                  ["2", "Cùng đề nhưng có khoá lũy đẳng. Còn bao nhiêu?"],
                  ["3", "Quyết định: lưu khoá ở bộ đệm (vùng lưu tạm trong bộ nhớ, đọc rất nhanh, có thể mất) hay trong cơ sở dữ liệu cùng giao dịch trừ tiền?"]]),
           """Đến lượt bạn. Câu một, số dư một triệu, chuyển hai trăm nghìn, thử năm lần, không khoá, còn bao nhiêu? Câu hai, cùng đề nhưng có khoá lũy đẳng, còn bao nhiêu?
           Câu ba, lưu khoá ở bộ đệm, tức vùng lưu tạm trong bộ nhớ đọc rất nhanh nhưng có thể mất, hay trong cơ sở dữ liệu cùng giao dịch trừ tiền? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: bị trừ $5 \\cdot 200\\,000 = 1\\,000\\,000$.</p>
$$1\\,000\\,000 - 1\\,000\\,000 = \\hl{0}$$""",
           """Đáp án câu một. Bị trừ năm nhân hai trăm nghìn, là một triệu, nên số dư còn lại bằng không."""),
        st("""<p>Câu 2: chỉ trừ một lần.</p>
$$1\\,000\\,000 - 200\\,000 = \\hlg{800\\,000}$$""",
           """Đáp án câu hai. Có khoá thì chỉ trừ một lần, nên còn tám trăm nghìn."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["khoá trong cơ sở dữ liệu, cùng giao dịch", "khoá và việc trừ tiền cùng thành công hoặc cùng huỷ", "tốn thêm một lần ghi"],
                  ["khoá chỉ ở bộ đệm", "nhanh", "không cùng giao dịch với việc trừ: khoá có thể hết hạn, mất khi chuyển dự phòng, hoặc ghi xong mà việc trừ bị huỷ"]]),
           """Đáp án câu ba. Lưu khoá trong cơ sở dữ liệu cùng giao dịch thì khoá và việc trừ tiền cùng thành công hoặc cùng huỷ, đổi lại tốn thêm một lần ghi.
           Chỉ lưu ở bộ đệm thì nhanh, nhưng khoá không cùng giao dịch với việc trừ tiền. Khoá có thể hết hạn, mất khi chuyển sang máy dự phòng,
           hoặc ghi xong mà việc trừ lại bị huỷ."""),
    ], checks=["alg.bnk_retry_sim(1000000, 200000, 5, False) == 0", "alg.bnk_retry_sim(1000000, 200000, 5, True) == 800000"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mất phản hồi", "người gọi thử lại", "cùng một khoá", "máy chủ chỉ làm một lần"),
           """Tổng kết chuỗi logic. Phản hồi có thể mất, nên người gọi thử lại. Mọi lần thử mang cùng một khoá, và máy chủ chỉ làm một lần."""),
        st("""<div class='box key'><b>Tư duy:</b> trong mạng, “không nhận được phản hồi” khác với “việc chưa làm”.
Thiết kế mọi việc thay đổi tiền sao cho <b>thử lại không gây hại</b>.</div>""",
           """Điều cần mang theo. Trong mạng, không nhận được phản hồi khác với việc chưa làm. Hãy thiết kế mọi việc thay đổi tiền sao cho thử lại không gây hại."""),
    ])
    return lesson("L03", "rest_api_khoa_luy_dang", "Bài 3 — REST API và khoá lũy đẳng",
                  "curriculum/bnk.yaml L03; audit/bnk/verify_bnk.py L03; RFC 9110 HTTP Semantics (phương thức an toàn và lũy đẳng)",
                  ["Giải thích vì sao thử lại là bình thường trong mạng", "Tính số tiền bị trừ oan khi không có khoá lũy đẳng",
                   "Thiết kế bảng khoá để chặn xử lý trùng", "Phân biệt phương thức an toàn và lũy đẳng"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
