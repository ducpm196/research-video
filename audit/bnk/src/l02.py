from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao dòng ghi vết vẫn mất dù đã gắn nhãn giao dịch?", [
        st("""<p>Một lệnh chuyển tiền thất bại giữa chừng. Lập trình viên gắn <code>@Transactional</code> lên hàm chuyển tiền, và nhãn giao dịch <b>luôn mở giao dịch mới</b> lên hàm ghi vết, vậy mà dòng ghi vết <b>không còn</b> trong bảng.</p>
<div class="box key">Hôm nay ta trả lời: Spring <b>tạo và nối</b> các đối tượng thế nào, <b>proxy</b> là gì, và vì sao nhãn giao dịch đôi khi <b>không có tác dụng</b>.</div>""",
           """Chào bạn, một lệnh chuyển tiền thất bại giữa chừng. Lập trình viên đã gắn nhãn giao dịch lên hàm chuyển tiền, và nhãn luôn mở giao dịch mới lên hàm ghi vết,
           vậy mà dòng ghi vết không còn trong bảng.
           Hôm nay ta trả lời ba câu. Spring tạo và nối các đối tượng thế nào, proxy là gì, và vì sao nhãn giao dịch đôi khi không có tác dụng."""),
        st(table(["cách gọi hàm ghi vết (nhãn luôn mở giao dịch mới)", "giao dịch đã mở", "dòng ghi vết sau khi chuyển tiền hỏng"],
                 [["gọi thẳng trong cùng lớp", "1", "mất"],
                  ["gọi qua một bean khác (qua proxy)", "2", "còn"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài, khi hàm ghi vết mang nhãn luôn mở giao dịch mới. Nếu hàm ghi vết được gọi thẳng trong cùng lớp, chỉ có một giao dịch được mở và dòng ghi vết mất theo.
           Nếu gọi qua một bean khác, tức là qua proxy, có hai giao dịch và dòng ghi vết còn lại."""),
    ])
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Lớp và đối tượng", "lớp là khuôn, đối tượng là bản làm ra từ khuôn", "lớp TaiKhoan, đối tượng tài khoản số 1"],
                  ["② Một hàm gọi hàm khác", "hàm A có thể gọi hàm B của đối tượng khác", "chuyenTien gọi ghiVet"],
                  ["③ Giao dịch", "một nhóm thao tác: hoặc cùng thành công, hoặc cùng huỷ", "trừ tiền và cộng tiền cùng lúc"]]),
           """Ôn ba điều. Lớp là cái khuôn, đối tượng là bản làm ra từ khuôn. Một hàm có thể gọi hàm của đối tượng khác, ví dụ chuyển tiền gọi ghi vết.
           Giao dịch là nhóm thao tác mà hoặc cùng thành công, hoặc cùng bị huỷ, ví dụ trừ tiền và cộng tiền."""),
        st("""$$-500\\,000 + 500\\,000 = 0$$""",
           """Một ví dụ số cho giao dịch. Trừ năm trăm nghìn ở một tài khoản và cộng năm trăm nghìn ở tài khoản kia, tổng bằng không. Nếu chỉ làm một nửa, sổ sách lệch."""),
    ], checks=["-500000 + 500000 == 0"])
    sym = sc("sym", "symbol", "Giải mã vài từ trong Spring", [
        st(table(["từ", "nghĩa"],
                 [["bean", "đối tượng do Spring tạo và quản lý"],
                  ["IoC (đảo điều khiển)", "bạn không tự tạo đối tượng bằng new, Spring tạo rồi trao cho bạn"],
                  ["tiêm phụ thuộc", "Spring nối các bean với nhau qua hàm khởi tạo"],
                  ["proxy", "một lớp vỏ bọc bean, chạy thêm việc trước và sau khi gọi hàm"],
                  ["REQUIRED / REQUIRES_NEW", "tham gia giao dịch đang có / luôn mở giao dịch mới"]]),
           """Bảng này giải mã năm từ. Bean là đối tượng do Spring tạo và quản lý. Đảo điều khiển nghĩa là bạn không tự tạo đối tượng, Spring tạo rồi trao cho bạn.
           Tiêm phụ thuộc là Spring nối các bean với nhau. Proxy là lớp vỏ bọc bean, chạy thêm việc trước và sau lời gọi.
           Cuối cùng, chế độ tham gia nghĩa là dùng giao dịch đang có, còn chế độ mới nghĩa là luôn mở giao dịch mới."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: vỏ bọc proxy đứng giữa", [
        st(svg(1500, 380,
               panel(40, 30, 1420, 320, "Spring container (hộp chứa các bean)", C_AMBER),
               box(100, 130, 300, 100, ["Controller", "bean"], C_BLUE),
               box(560, 130, 300, 100, ["Proxy", "vỏ bọc"], C_PURPLE),
               box(1020, 130, 360, 100, ["TransferService", "bean thật"], C_GREEN),
               arrow(400, 180, 555, 180, "#2a78d6", "gọi"), arrow(860, 180, 1015, 180, "#9333ea", "chuyển tiếp"),
               txt(700, 300, "Controller không giữ bean thật mà giữ proxy", 26, "middle", "#1f2937", True)),
           """Hình cho thấy cách Spring nối các bean. Controller muốn gọi dịch vụ chuyển tiền. Nhưng thứ nó nhận được không phải bean thật, mà là một proxy vỏ bọc.
           Proxy đứng giữa, rồi mới chuyển lời gọi tới bean thật."""),
        st(svg(1500, 400,
               box(60, 150, 240, 90, "Proxy", C_PURPLE, bold=True),
               box(380, 40, 300, 70, "1. mở giao dịch", C_GREEN), box(380, 150, 300, 90, ["2. chạy hàm", "chuyenTien()"], C_BLUE),
               box(380, 280, 300, 70, "3. commit / rollback", C_GREEN),
               arrow(300, 170, 375, 90, "#16a34a"), arrow(530, 115, 530, 145, "#475569"), arrow(530, 245, 530, 275, "#475569"),
               txt(1080, 160, "Nhãn @Transactional thật ra", 26, "middle", "#1f2937", True),
               txt(1080, 200, "chỉ là lời dặn cho proxy:", 26, "middle", "#1f2937", True),
               txt(1080, 240, "mở trước, đóng sau", 26, "middle", "#1f2937", True)),
           """Proxy làm ba việc. Trước tiên mở một giao dịch. Rồi chạy hàm chuyển tiền thật. Cuối cùng, commit nếu thành công, hoặc rollback nếu có lỗi.
           Nhãn giao dịch thật ra chỉ là lời dặn cho proxy, rằng hãy mở trước và đóng sau."""),
        st(svg(1500, 420,
               box(60, 40, 280, 90, "Proxy", C_PURPLE, bold=True),
               box(480, 40, 460, 90, ["chuyenTien() (bean thật)", "đã trong giao dịch 1"], C_GREEN),
               box(480, 230, 460, 90, ["this.ghiVet()", "gọi thẳng, không qua proxy"], C_RED),
               arrow(340, 85, 475, 85, "#9333ea"), arrow(710, 135, 710, 225, "#dc2626"),
               txt(1230, 150, "Không qua proxy", 26, "middle", "#dc2626", True),
               txt(1230, 190, "nên không có", 26, "middle", "#dc2626", True),
               txt(1230, 230, "giao dịch mới", 26, "middle", "#dc2626", True)),
           """Nhưng khi hàm chuyển tiền bên trong tự gọi ghi vết bằng từ khoá this, lời gọi đó đi thẳng, không qua proxy. Không có proxy thì không ai đọc nhãn, nên không có giao dịch mới.
           Đây chính là lỗi mở đầu bài."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: khi nào có giao dịch mới?", [
        st("""<p><b>Bước 1.</b> Người gọi từ bên ngoài luôn nhận <b>proxy</b>, nên lời gọi đầu tiên vào <code>chuyenTien()</code> đi qua proxy và mở giao dịch 1.</p>
<span class='note'>Làm thử: số giao dịch đã mở = $1$.</span>""",
           """Bước một, vì người gọi từ bên ngoài luôn nhận proxy, nên lời gọi đầu tiên vào hàm chuyển tiền đi qua proxy và mở giao dịch thứ nhất.
           Làm thử, số giao dịch đã mở bằng một."""),
        st("""<p><b>Bước 2.</b> Hàm ghi vết với chế độ <code>REQUIRES_NEW</code> chỉ mở giao dịch mới khi lời gọi <b>đi qua proxy</b>.</p>
<span class='note'>Qua proxy: $1 + 1 = 2$ giao dịch. Gọi thẳng: vẫn $1$ giao dịch.</span>""",
           """Bước hai, vì proxy mới là nơi đọc nhãn, nên hàm ghi vết chỉ mở giao dịch mới khi lời gọi đi qua proxy.
           Làm thử, qua proxy thì một cộng một bằng hai giao dịch, còn gọi thẳng vẫn chỉ một giao dịch."""),
        st("""<p><b>Bước 3.</b> Giao dịch mới commit riêng, nên khi giao dịch ngoài hỏng, dòng ghi vết vẫn còn. Giao dịch dùng chung thì mất theo.</p>
<span class='note'>Mặc định, Spring chỉ rollback khi gặp lỗi không bắt buộc xử lý (RuntimeException) hoặc Error.</span>""",
           """Bước ba, vì giao dịch mới commit riêng, nên khi giao dịch ngoài hỏng, dòng ghi vết vẫn còn. Còn giao dịch dùng chung thì mất theo.
           Mặc định Spring chỉ rollback khi gặp lỗi thời gian chạy hoặc lỗi hệ thống."""),
    ], checks=["alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[0] == 1 + 1", "alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[0] == 1",
               "alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1] == ['audit']"])
    ex = sc("example", "example", "Ví dụ bằng số, từng trường hợp", [
        st("""<p>Chuyển $500\\,000$ đồng, giao dịch ngoài hỏng. <b>Trường hợp A:</b> ghi vết gọi thẳng bằng <code>this</code>.</p>
$$① \\; \\text{giao dịch đã mở} = \\hl{1}$$""",
           """Ta chạy ba trường hợp. Trường hợp A, chuyển năm trăm nghìn đồng, giao dịch ngoài hỏng, ghi vết gọi thẳng bằng this. Phép tính thứ nhất, số giao dịch đã mở là một."""),
        st("""<p>Giao dịch ngoài hỏng nên rollback cả hai dòng.</p>
$$② \\; \\text{dòng còn lại} = \\hl{0}$$""",
           """Phép tính thứ hai, giao dịch ngoài hỏng nên rollback cả dòng chuyển tiền lẫn dòng ghi vết. Số dòng còn lại là không."""),
        st("""<p><b>Trường hợp B:</b> ghi vết gọi qua bean khác, chế độ mới.</p>
$$③ \\; \\text{giao dịch đã mở} = 1 + 1 = \\hlg{2}$$""",
           """Trường hợp B, ghi vết gọi qua một bean khác với chế độ mới. Phép tính thứ ba, số giao dịch đã mở là một cộng một bằng hai."""),
        st("""<p>Dòng ghi vết commit riêng, dòng chuyển tiền bị huỷ.</p>
$$④ \\; \\text{dòng còn lại} = \\hlg{1}\\ \\text{(dòng ghi vết)}$$""",
           """Phép tính thứ tư, dòng ghi vết đã commit riêng, còn dòng chuyển tiền bị huỷ, nên còn lại đúng một dòng, là dòng ghi vết."""),
        st("""<p><b>Trường hợp C:</b> mọi thứ thành công, lời gọi qua proxy.</p>
$$⑤ \\; \\text{dòng còn lại} = \\hlg{2}$$""",
           """Trường hợp C, mọi việc thành công. Phép tính thứ năm, cả hai dòng đều commit, nên còn hai dòng."""),
    ], checks=["alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[0] == 1", "len(alg.bnk_spring_sim(False, 'REQUIRES_NEW', True)[1]) == 0",
               "alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[0] == 1 + 1", "len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1]) == 1",
               "len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', False)[1]) == 2"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm lần đi qua proxy", [
        st("""<p>Đường khác: vì chỉ proxy mới mở giao dịch, nên số giao dịch bằng giao dịch đầu cộng <b>số lần lời gọi đi qua proxy có chế độ mở mới</b>.</p>
$$\\text{giao dịch} = 1 + \\text{số lần qua proxy với chế độ mới}$$""",
           """Kiểm bằng đường khác. Vì chỉ proxy mới mở giao dịch, nên số giao dịch bằng một, là giao dịch đầu, cộng số lần lời gọi đi qua proxy với chế độ mở mới."""),
        st(table(["trường hợp", "lần qua proxy với chế độ mới", "giao dịch = 1 + lần", "khớp mô phỏng"],
                 [["A: gọi thẳng", "0", "1", "có"], ["B: qua bean khác", "1", "2", "có"], ["REQUIRED qua proxy", "0", "1", "có"]]),
           """Bảng này so sánh. Gọi thẳng thì không có lần nào qua proxy, nên một giao dịch. Qua bean khác với chế độ mới là một lần, nên hai giao dịch.
           Chế độ dùng chung qua proxy cũng không mở thêm, nên một giao dịch. Cả ba khớp mô phỏng."""),
    ], checks=["alg.bnk_spring_sim(True, 'REQUIRED', True)[0] == 1 + 0",
               "all(alg.bnk_spring_sim(v, m, False)[0] == 1 + (1 if (v and m == 'REQUIRES_NEW') else 0) for v in (True, False) for m in ('REQUIRED', 'REQUIRES_NEW'))"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tự viết <code>new TransferService()</code>. Đối tượng đó không do Spring tạo, nên không được nối phụ thuộc và không có proxy.</div>""",
           """Lỗi thứ nhất, của người mới. Tự tạo đối tượng dịch vụ bằng từ khoá tạo mới. Đối tượng đó không do Spring tạo, nên không được nối phụ thuộc và không có proxy."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Gọi hàm có nhãn giao dịch từ trong cùng lớp</b> bằng <code>this</code>. Nhãn bị bỏ qua.
<br><span class="note">Cách chữa: tách hàm sang bean khác, rồi gọi qua bean đó.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là gọi hàm có nhãn giao dịch từ trong cùng lớp bằng this. Nhãn bị bỏ qua vì không có proxy.
           Cách chữa là tách hàm sang bean khác rồi gọi qua bean đó."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Bắt lỗi trong hàm có nhãn rồi chỉ ghi log. Proxy không thấy lỗi nào, nên <b class="red">commit nửa chừng</b>.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là bắt lỗi ngay trong hàm có nhãn rồi chỉ ghi nhật ký. Proxy không thấy lỗi nào nên cứ commit, và dữ liệu bị lưu nửa chừng."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Gọi ghi vết qua proxy, chế độ mới, giao dịch ngoài hỏng. Còn dòng nào?"],
                  ["2", "Như câu 1 nhưng chế độ dùng chung (REQUIRED). Còn dòng nào?"],
                  ["3", "Quyết định: đặt hàm ghi vết ở đâu để luôn lưu được vết?"]]),
           """Đến lượt bạn. Câu một, gọi ghi vết qua proxy, chế độ mới, giao dịch ngoài hỏng, còn dòng nào? Câu hai, như câu một nhưng chế độ dùng chung, còn dòng nào?
           Câu ba, đặt hàm ghi vết ở đâu để luôn lưu được vết? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: giao dịch mới commit riêng, nên còn dòng ghi vết.</p>
$$\\text{số dòng} = \\hl{1}$$""",
           """Đáp án câu một. Giao dịch mới commit riêng, nên còn đúng dòng ghi vết, một dòng."""),
        st("""<p>Câu 2: dùng chung thì ghi vết nằm trong giao dịch ngoài, nên bị rollback cùng.</p>
$$\\text{số dòng} = \\hl{0}$$""",
           """Đáp án câu hai. Chế độ dùng chung đưa ghi vết vào giao dịch ngoài, nên bị rollback cùng, số dòng là không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hàm ghi vết ở bean riêng, chế độ mới", "vết lưu kể cả khi giao dịch chính hỏng", "tốn thêm một giao dịch"],
                  ["cùng lớp, gọi bằng this", "ít mã", "nhãn bị bỏ qua, vết mất"]]),
           """Đáp án câu ba. Đặt hàm ghi vết ở một bean riêng với chế độ mới, thì vết luôn được lưu dù giao dịch chính hỏng, đổi lại tốn thêm một giao dịch.
           Để cùng lớp thì ít mã nhưng nhãn bị bỏ qua."""),
    ], checks=["len(alg.bnk_spring_sim(True, 'REQUIRES_NEW', True)[1]) == 1", "len(alg.bnk_spring_sim(True, 'REQUIRED', True)[1]) == 0"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("Spring tạo bean", "trao proxy cho người gọi", "proxy đọc nhãn", "mở / đóng giao dịch"),
           """Tổng kết chuỗi logic. Spring tạo bean, trao proxy cho người gọi. Proxy đọc nhãn rồi mở và đóng giao dịch."""),
        st("""<div class='box key'><b>Tư duy:</b> nhãn chỉ có tác dụng khi lời gọi <b>đi qua proxy</b>.
Khi giao dịch “không chạy”, hãy hỏi trước tiên: lời gọi này có đi qua proxy không?</div>""",
           """Điều cần mang theo. Nhãn chỉ có tác dụng khi lời gọi đi qua proxy. Khi giao dịch không chạy, hãy hỏi trước tiên, lời gọi này có đi qua proxy không."""),
    ])
    return lesson("L02", "spring_boot_proxy_giao_dich", "Bài 2 — Spring Boot: bean, proxy và giao dịch",
                  "curriculum/bnk.yaml L02; audit/bnk/verify_bnk.py L02; Spring Framework Reference (Transaction Management, AOP proxies)",
                  ["Giải thích Spring tạo bean và trao proxy cho người gọi", "Dự đoán số giao dịch được mở khi gọi qua proxy hoặc gọi thẳng",
                   "Nhận ra lỗi gọi hàm cùng lớp làm mất nhãn giao dịch", "Chọn nơi đặt hàm ghi vết để luôn lưu được"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
