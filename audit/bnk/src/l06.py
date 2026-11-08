from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao bộ đệm làm nhanh gấp nhiều lần, và vì sao khoá phân tán vẫn có thể sai?", [
        st("""<p>Mỗi lần tra số dư mất $20$ ms ở cơ sở dữ liệu <i>(số minh hoạ)</i>. Có bộ đệm với tỉ lệ trúng $90\\%$, trung bình chỉ còn khoảng <b>3 ms</b>.</p>
<div class="box key">Nhưng một khoá phân tán có hạn <b>10 giây</b> vẫn có thể bị <b>hai người cùng giữ</b> nếu một người bị tạm dừng.</div>""",
           """Chào bạn, giả sử mỗi lần tra số dư mất hai mươi mili giây ở cơ sở dữ liệu, đây là số minh hoạ. Có bộ đệm với tỉ lệ trúng chín mươi phần trăm, trung bình chỉ còn khoảng ba mili giây.
           Nhưng một khoá phân tán có hạn mười giây vẫn có thể bị hai người cùng giữ, nếu một người bị tạm dừng."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["bộ đệm nhanh hơn bao nhiêu", "độ trễ trung bình = tđệm + (1 − tỉ lệ trúng) × tcsdl"],
                  ["khoá có hạn sai ở đâu", "người giữ khoá bị tạm dừng quá hạn rồi vẫn ghi"],
                  ["chữa thế nào", "mã chặn tăng dần, nơi lưu từ chối mã cũ"]]),
           """Hôm nay ta trả lời ba câu. Bộ đệm nhanh hơn bao nhiêu, nhờ một công thức đơn giản. Khoá có hạn sai ở đâu, khi người giữ khoá bị tạm dừng quá hạn rồi vẫn ghi.
           Và cách chữa, là mã chặn tăng dần để nơi lưu từ chối mã cũ."""),
    ])
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Khoá và giá trị", "kho dữ liệu trong bộ nhớ, tra theo khoá", "khoá so_du:42 → giá trị 1500000"],
                  ["② Hết hạn (TTL)", "mỗi mục tự biến mất sau một thời gian", "hạn 60 giây"],
                  ["③ Độ trễ", "thời gian từ lúc hỏi tới lúc có đáp", "bộ đệm 1 ms, cơ sở dữ liệu 20 ms (số minh hoạ)"]]),
           """Ôn ba điều. Kho dữ liệu trong bộ nhớ tra theo khoá, ví dụ khoá số dư của tài khoản bốn mươi hai trả về một triệu năm trăm nghìn. Mỗi mục có thể tự hết hạn sau một thời gian.
           Độ trễ là thời gian từ lúc hỏi tới lúc có đáp, ví dụ minh hoạ là bộ đệm một mili giây, cơ sở dữ liệu hai mươi mili giây."""),
        st("""$$0{,}9 + 0{,}1 = 1$$""",
           """Một phép kiểm nhỏ. Tỉ lệ trúng cộng tỉ lệ trượt luôn bằng một. Không phẩy chín cộng không phẩy một bằng một."""),
    ], checks=["abs(0.9 + 0.1 - 1) < 1e-12"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["cache-aside", "hỏi bộ đệm trước; trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm"],
                  ["hit / miss", "trúng bộ đệm / trượt bộ đệm"],
                  ["TTL", "thời gian sống của một mục trước khi tự xoá"],
                  ["SET key value NX PX 10000", "lệnh Redis đặt khoá chỉ khi chưa có (NX), hết hạn sau 10 000 mili giây (PX)"],
                  ["fencing token (mã chặn)", "số tăng dần cấp kèm mỗi lần giữ khoá, nơi lưu dùng để từ chối người cũ; SET NX PX và Redlock không tự cấp, phải lấy từ bộ đếm (INCR hoặc sequence)"],
                  ["nhả khoá", "so giá trị mình đã đặt rồi mới xoá, trong một script Lua; không DEL thẳng"]]),
           """Bảng dưới đây giải nghĩa sáu thuật ngữ mà bài sẽ dùng. Kiểu hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm. Trúng là có trong bộ đệm, trượt là không có.
           Thời gian sống là hạn tự xoá của mỗi mục. Lệnh đặt khoá có hai tuỳ chọn, chỉ đặt khi chưa có, và tự hết hạn. Mã chặn là số tăng dần để nơi lưu từ chối người giữ khoá cũ.
           Lệnh đặt khoá không tự cấp mã chặn, nên phải lấy từ một bộ đếm tăng dần. Cuối cùng, khi nhả khoá, phải so giá trị mình đã đặt rồi mới xoá, để không xoá nhầm khoá của người khác."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: bộ đệm và khoá hết hạn", [
        st(svg(1500, 400,
               box(40, 150, 220, 100, ["Dịch vụ", "tra số dư"], C_BLUE, bold=True),
               box(560, 40, 380, 100, ["Redis (bộ đệm)", "1 ms"], C_AMBER, bold=True),
               box(560, 260, 380, 100, ["Cơ sở dữ liệu", "20 ms"], C_GREEN, bold=True),
               arrow(260, 180, 555, 100, "#2a78d6", "1. hỏi"),
               arrow(1000, 90, 1100, 90, "#16a34a", "trúng → trả"),
               arrow(260, 220, 555, 300, "#2a78d6", "2. trượt → hỏi tiếp"),
               arrow(560, 330, 1000, 330, "#475569", None), txt(1250, 100, "90 trong 100 lần", 26, "middle", "#16a34a", True),
               txt(1250, 340, "10 trong 100 lần", 26, "middle", "#d97706", True)),
           """Hình cho thấy kiểu hỏi bộ đệm trước. Dịch vụ hỏi Redis trước. Nếu trúng thì trả luôn, chỉ mất một mili giây, và đó là chín mươi trong một trăm lần.
           Nếu trượt thì hỏi tiếp cơ sở dữ liệu, mất thêm hai mươi mili giây, và đó là mười trong một trăm lần."""),
        st(svg(1500, 460,
               txt(60, 50, "Giây", 24, "start", "#475569"),
               box(120, 80, 520, 70, "A giữ khoá (mã chặn 1), hạn 10 giây", C_BLUE),
               box(640, 80, 280, 70, "A tạm dừng…", C_GRAY, dash=True),
               box(740, 190, 420, 70, "giây 11: B giữ khoá (mã chặn 2)", C_AMBER),
               box(740, 290, 360, 70, "giây 11,5: B ghi", C_AMBER),
               box(1000, 80, 440, 70, "giây 12: A tỉnh dậy, vẫn ghi!", C_RED),
               txt(750, 420, "Khoá của A đã hết hạn từ giây 10, nhưng A không biết", 26, "middle", "#dc2626", True)),
           """Hình thứ hai cho thấy lỗi của khoá có hạn. A giữ khoá với hạn mười giây, rồi bị tạm dừng, ví dụ do thu gom rác. Khoá hết hạn, B lấy khoá ở giây mười một và ghi lúc mười một phẩy năm.
           Đến giây mười hai A tỉnh dậy, không biết khoá đã hết, và vẫn ghi đè lên B."""),
        st(svg(1500, 400,
               box(60, 150, 260, 100, ["B ghi", "mã chặn 2"], C_AMBER, bold=True),
               box(60, 280, 260, 80, ["A ghi muộn", "mã chặn 1"], C_RED),
               box(620, 130, 420, 140, ["Nơi lưu", "nhớ mã chặn lớn nhất = 2"], C_GREEN, bold=True),
               arrow(320, 190, 615, 190, "#16a34a", "nhận"), arrow(320, 320, 615, 240, "#dc2626", "1 < 2 → từ chối"),
               txt(1260, 180, "Nơi lưu chặn người cũ", 26, "middle", "#1f2937", True),
               txt(1260, 220, "dù khoá đã hết hạn", 26, "middle", "#1f2937", True)),
           """Mã chặn chữa lỗi này. Nơi lưu nhớ mã chặn lớn nhất đã thấy, ở đây là hai. Khi A ghi muộn với mã chặn một, nơi lưu thấy một nhỏ hơn hai và từ chối.
           Nhờ vậy, người cũ không thể ghi đè dù khoá đã hết hạn."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: độ trễ trung bình và an toàn của khoá", [
        st("""<p><b>Bước 1.</b> Luôn hỏi bộ đệm: mọi lần tốn $c$. Trượt (xác suất $1 - h$) thì tốn thêm $d$ của cơ sở dữ liệu.</p>
<span class='note'>Làm thử: $h = 0{,}9$, $c = 1$, $d = 20$: trượt $0{,}1$ lần, mỗi lần thêm $20$ ms.</span>""",
           """Bước một, vì ta luôn hỏi bộ đệm trước, nên mọi lần đều tốn thời gian của bộ đệm. Lần nào trượt, với xác suất một trừ h, thì tốn thêm thời gian của cơ sở dữ liệu.
           Làm thử với h bằng không phẩy chín, mỗi lần trượt thêm hai mươi mili giây."""),
        st("""<p><b>Bước 2.</b> Vì mọi lần tốn $c$ và chỉ phần trượt tốn thêm $d$, nên gộp lại: $T = c + (1 - h) \\cdot d$.</p>
<span class='note'>Làm thử: $T = 1 + 0{,}1 \\cdot 20 = 3$ ms.</span>""",
           """Bước hai, vì mọi lần tốn thời gian bộ đệm và chỉ phần trượt tốn thêm, nên gộp lại, trung bình T bằng thời gian bộ đệm cộng, một trừ h, nhân thời gian cơ sở dữ liệu. Làm thử, một cộng không phẩy một nhân hai mươi bằng ba mili giây."""),
        st("""<p><b>Bước 3.</b> Khoá có hạn không bảo đảm “một người giữ”, vì người giữ có thể bị tạm dừng lâu hơn hạn. Nơi lưu phải kiểm <b>mã chặn</b> mới an toàn.</p>
<span class='note'>Làm thử: ghi mã 2 rồi mã 1 → nơi lưu nhận mã 2, từ chối mã 1.</span>""",
           """Bước ba, vì người giữ khoá có thể bị tạm dừng lâu hơn hạn, nên khoá có hạn không bảo đảm chỉ một người giữ. Nơi lưu phải kiểm mã chặn mới an toàn.
           Làm thử, ghi mã hai rồi mã một, nơi lưu nhận mã hai và từ chối mã một."""),
    ], checks=["abs(1 + (1 - 0.9) * 20 - 3) < 1e-9", "abs(alg.bnk_cache_avg(0.9, 1, 20) - 3) < 1e-9", "alg.bnk_fencing_sim(True) == ['B']"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Dùng $c = 1$ ms, $d = 20$ ms <i>(số minh hoạ)</i>.</p>
$$① \\; h = 0{,}9:\\quad T = 1 + 0{,}1 \\cdot 20 = \\hlg{3}\\ \\text{ms}$$""",
           """Ta tính cho ba mức trúng. Dùng thời gian bộ đệm một mili giây và cơ sở dữ liệu hai mươi mili giây, đây là số minh hoạ. Phép tính thứ nhất, với h bằng không phẩy chín, T bằng một cộng không phẩy một nhân hai mươi, là ba mili giây."""),
        st("""$$② \\; h = 0{,}5:\\quad T = 1 + 0{,}5 \\cdot 20 = \\hl{11}\\ \\text{ms}$$""",
           """Phép tính thứ hai, với h bằng không phẩy năm, T bằng một cộng không phẩy năm nhân hai mươi, là mười một mili giây."""),
        st("""$$③ \\; \\text{không có bộ đệm: } T = \\hl{20}\\ \\text{ms}$$""",
           """Phép tính thứ ba, không có bộ đệm, mọi lần đều hỏi cơ sở dữ liệu, nên T bằng hai mươi mili giây."""),
        st("""<p>Dùng lại $T = 3$ ở ① và $20$ ở ③.</p>
$$④ \\; \\text{nhanh gấp} \\; \\frac{20}{3} \\approx \\hlg{6{,}7}\\ \\text{lần}$$""",
           """Phép tính thứ tư, nhanh gấp hai mươi chia ba, xấp xỉ sáu phẩy bảy lần."""),
        st("""<p>Khoá hạn $10$ giây, A tạm dừng tới giây $12$: quá hạn $12 - 10 = \\hl{2}$ giây.</p>
$$⑤ \\; \\text{không mã chặn: ghi cuối là A (đè B)};\\quad \\text{có mã chặn: ghi cuối là B}$$""",
           """Phép tính thứ năm, khoá hạn mười giây mà A tạm dừng tới giây mười hai, nên quá hạn hai giây. Không có mã chặn thì người ghi cuối là A, đè lên B. Có mã chặn thì người ghi cuối là B."""),
    ], checks=["abs(alg.bnk_cache_avg(0.9, 1, 20) - 3) < 1e-9", "abs(alg.bnk_cache_avg(0.5, 1, 20) - 11) < 1e-9", "abs(20 / 3 - 6.7) < 0.05",
               "12 - 10 == 2 and alg.bnk_fencing_sim(False)[-1] == 'A' and alg.bnk_fencing_sim(True)[-1] == 'B'"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính theo từng trường hợp", [
        st("""<p>Đường khác: vì mỗi trường hợp có độ trễ riêng, ta tính theo từng trường hợp thay vì công thức. Trong $100$ lần, $90$ lần trúng tốn $1$ ms, $10$ lần trượt tốn $1 + 20$ ms.</p>
$$\\frac{90 \\cdot 1 + 10 \\cdot 21}{100} = \\frac{300}{100} = \\hl{3}\\ \\text{ms}$$""",
           """Kiểm bằng đường khác. Thay vì dùng công thức, ta tính theo từng trường hợp. Trong một trăm lần, chín mươi lần trúng tốn một mili giây, mười lần trượt tốn hai mươi mốt mili giây.
           Cộng lại được ba trăm, nên chia một trăm bằng ba mili giây, khớp công thức."""),
        st(table(["tỉ lệ trúng", "độ trễ trung bình", "so với 20 ms"],
                 [["0,5", "11 ms", "nhanh 1,8 lần"], ["0,9", "3 ms", "nhanh 6,7 lần"], ["0,99", "1,2 ms", "nhanh 16,7 lần"]]),
           """Bảng này cho thấy tỉ lệ trúng quan trọng thế nào. Vì phần trượt tốn nhiều nhất, nên từ không phẩy năm lên không phẩy chín chín, độ trễ giảm từ mười một xuống một phẩy hai mili giây."""),
    ], checks=["(90 * 1 + 10 * 21) / 100 == 3.0", "abs(alg.bnk_cache_avg(0.99, 1, 20) - 1.2) < 1e-9", "abs(20 / 1.2 - 16.7) < 0.05", "abs(20 / 11 - 1.8) < 0.05"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Lưu <b>số dư</b> trong bộ đệm rồi dùng nó để quyết định trừ tiền. Bộ đệm có thể cũ. Số dư thật để quyết định luôn đọc từ cơ sở dữ liệu nguồn.</div>""",
           """Lỗi thứ nhất, của người mới. Lưu số dư trong bộ đệm rồi dùng nó để quyết định trừ tiền. Bộ đệm có thể cũ. Số dư dùng để quyết định phải luôn đọc từ cơ sở dữ liệu nguồn."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Bộ đệm hết hạn cùng lúc</b>: nghìn khoá cùng hạn $60$ giây, đến giờ tất cả trượt, nghìn truy vấn đổ về cơ sở dữ liệu cùng lúc.
<br><span class="note">Cách chữa: cộng thêm một số ngẫu nhiên nhỏ vào hạn, và chỉ cho một luồng nạp lại mỗi khoá.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là bộ đệm hết hạn cùng lúc. Hàng nghìn khoá cùng hạn sáu mươi giây, đến giờ tất cả trượt, nghìn truy vấn đổ về cơ sở dữ liệu cùng lúc.
           Cách chữa là cộng thêm một số ngẫu nhiên nhỏ vào hạn, và chỉ cho một luồng nạp lại mỗi khoá."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tin khoá phân tán là đủ để bảo vệ việc ghi tiền. Khoá có hạn có thể bị hai người cùng giữ. Hãy để <b>cơ sở dữ liệu</b> chặn: ràng buộc duy nhất hoặc cột phiên bản.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là tin khoá phân tán là đủ để bảo vệ việc ghi tiền. Khoá có hạn có thể bị hai người cùng giữ. Hãy để cơ sở dữ liệu chặn, bằng ràng buộc duy nhất hoặc cột phiên bản."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "tđệm = 2 ms, tcsdl = 30 ms, tỉ lệ trúng 0,8. Độ trễ trung bình?"],
                  ["2", "Nhanh hơn không có bộ đệm bao nhiêu lần?"],
                  ["3", "Quyết định: dùng khoá Redis để bảo vệ việc trừ tiền?"]]),
           """Đến lượt bạn. Câu một, thời gian bộ đệm hai mili giây, cơ sở dữ liệu ba mươi mili giây, tỉ lệ trúng không phẩy tám, độ trễ trung bình là bao nhiêu?
           Câu hai, nhanh hơn không có bộ đệm bao nhiêu lần? Câu ba, có nên dùng khoá Redis để bảo vệ việc trừ tiền không? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$T = 2 + 0{,}2 \\cdot 30 = 2 + 6 = \\hl{8}\\ \\text{ms}$$""",
           """Đáp án câu một. T bằng hai cộng không phẩy hai nhân ba mươi, bằng hai cộng sáu, là tám mili giây."""),
        st("""$$\\frac{30}{8} = \\hlg{3{,}75}\\ \\text{lần}$$""",
           """Đáp án câu hai. Ba mươi chia tám bằng ba phẩy bảy mươi lăm lần."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chỉ khoá Redis", "nhanh, dễ viết", "khoá hết hạn có thể bị hai người cùng giữ, có thể trừ trùng"],
                  ["khoá Redis + ràng buộc / cột phiên bản ở cơ sở dữ liệu", "khoá giảm tranh chấp, cơ sở dữ liệu bảo đảm đúng", "thêm mã"]]),
           """Đáp án câu ba. Chỉ dùng khoá Redis thì nhanh nhưng có thể trừ trùng. Nên dùng khoá để giảm tranh chấp, và để cơ sở dữ liệu bảo đảm tính đúng bằng ràng buộc hoặc cột phiên bản."""),
    ], checks=["abs(alg.bnk_cache_avg(0.8, 2, 30) - 8) < 1e-9", "abs(30 / 8 - 3.75) < 1e-9"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("hỏi bộ đệm trước", "T = tđệm + (1 − h) × tcsdl", "khoá có hạn có thể quá hạn", "mã chặn + ràng buộc cơ sở dữ liệu"),
           """Tổng kết chuỗi logic. Hỏi bộ đệm trước, độ trễ trung bình là thời gian bộ đệm cộng tỉ lệ trượt nhân thời gian cơ sở dữ liệu. Khoá có hạn có thể quá hạn, nên cần mã chặn và ràng buộc ở cơ sở dữ liệu."""),
        st("""<div class='box key'><b>Tư duy:</b> bộ đệm là để <b>đọc nhanh</b>, không phải nguồn sự thật cho tiền.
Khoá phân tán là <b>tối ưu</b>; tính đúng đắn phải do cơ sở dữ liệu bảo đảm.</div>""",
           """Điều cần mang theo. Bộ đệm là để đọc nhanh, không phải nguồn sự thật cho tiền. Khoá phân tán là một tối ưu, còn tính đúng đắn phải do cơ sở dữ liệu bảo đảm."""),
    ])
    return lesson("L06", "redis_cache_khoa_phan_tan", "Bài 6 — Redis, bộ đệm và khoá phân tán",
                  "curriculum/bnk.yaml L06; audit/bnk/verify_bnk.py L06; Redis documentation (SET NX PX); Kleppmann, How to do distributed locking (fencing token)",
                  ["Tính độ trễ trung bình của bộ đệm theo tỉ lệ trúng", "Giải thích vì sao khoá có hạn có thể bị hai người giữ",
                   "Áp mã chặn để nơi lưu từ chối người giữ khoá cũ", "Quyết định đúng khi dùng khoá phân tán cho tiền"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
