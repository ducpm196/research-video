from lib import *


# Ba bước bù được (mô hình bài): giữ hạn mức ngày, ghi nợ, ghi có. "Thông báo" đứng sau ghi có (điểm không quay lại)
# nên chỉ thử lại, không bù (Richardson, Microservices Patterns: compensatable / pivot / retriable transactions).
STEPS = ("giữ hạn mức", "ghi nợ", "ghi có")
_S = repr(STEPS)


def build():
    hook = sc("hook", "hook", "Vì sao tiền bị trừ mà bên kia chưa nhận?", [
        st("""<p>Chuyển tiền gồm nhiều việc ở nhiều dịch vụ: <b>giữ hạn mức</b>, <b>ghi nợ</b>, <b>ghi có</b>, rồi <b>thông báo</b>. Mỗi dịch vụ có cơ sở dữ liệu riêng, không có giao dịch chung bao tất cả.</p>
<div class="box key">Nếu ghi có lỗi sau khi ghi nợ đã xong, tiền của khách <b>đã bị trừ</b> mà chưa ai nhận.</div>""",
           """Chào bạn, chuyển tiền gồm nhiều việc ở nhiều dịch vụ khác nhau, là giữ hạn mức, ghi nợ, ghi có, rồi thông báo. Mỗi dịch vụ có cơ sở dữ liệu riêng, nên không có giao dịch chung bao tất cả.
           Nếu ghi có lỗi sau khi ghi nợ đã xong, tiền của khách đã bị trừ mà chưa ai nhận."""),
        st(table(["tình huống", "kết quả mô phỏng"],
                 [["ghi có lỗi, không bù", "tiền mất dấu"], ["ghi có lỗi, chạy bước bù", "ghi nợ được hoàn lại"],
                  ["lưu xong rồi sập trước khi báo, không Outbox", "0 sự kiện được phát"], ["có Outbox", "1 sự kiện được phát"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài. Ghi có lỗi mà không bù thì tiền mất dấu. Có bước bù thì ghi nợ được hoàn lại.
           Lưu xong rồi sập trước khi báo thì không có sự kiện nào được phát, còn có Outbox thì sự kiện vẫn được phát."""),
    ])
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Giao dịch cục bộ", "tất cả hoặc không gì cả, nhưng chỉ trong một cơ sở dữ liệu", "trừ và cộng trong cùng một bảng"],
                  ["② Dịch vụ độc lập", "mỗi dịch vụ sở hữu dữ liệu riêng và có thể lỗi riêng", "dịch vụ ghi nợ, dịch vụ ghi có"],
                  ["③ Hành động bù", "việc làm ngược lại để huỷ tác dụng của một việc đã xong", "hoàn lại tiền đã trừ"]]),
           """Ôn ba điều. Giao dịch cục bộ bảo đảm tất cả hoặc không gì cả, nhưng chỉ trong một cơ sở dữ liệu. Dịch vụ độc lập sở hữu dữ liệu riêng và có thể lỗi riêng.
           Hành động bù là việc làm ngược lại để huỷ tác dụng của một việc đã xong, ví dụ hoàn lại tiền đã trừ."""),
        st("""$$+500\\,000 - 500\\,000 = 0$$""",
           """Một ví dụ cho hành động bù. Trừ năm trăm nghìn rồi hoàn lại năm trăm nghìn, tổng bằng không, như chưa từng trừ."""),
    ], checks=["500000 - 500000 == 0"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["SAGA", "chuỗi giao dịch cục bộ; mỗi bước có bước bù để quay lui"],
                  ["compensation (bù)", "bước làm ngược lại cho một bước đã xong"],
                  ["orchestration / choreography", "một người điều phối gọi từng bước / các dịch vụ tự phản ứng với sự kiện"],
                  ["Transactional Outbox", "ghi dữ liệu và sự kiện vào cùng một giao dịch, rồi một bộ chuyển tiếp phát sự kiện"],
                  ["relay (bộ chuyển tiếp)", "tiến trình đọc bảng Outbox rồi gửi sang Kafka"]]),
           """Bảng này giải mã năm từ. SAGA là chuỗi giao dịch cục bộ, mỗi bước có bước bù để quay lui. Bù là việc làm ngược lại cho một bước đã xong.
           Điều phối là một người gọi từng bước, còn phối hợp theo sự kiện là các dịch vụ tự phản ứng. Outbox là ghi dữ liệu và sự kiện vào cùng một giao dịch, rồi bộ chuyển tiếp phát sự kiện."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: chuỗi bước và bước bù ngược chiều", [
        st(svg(1500, 420,
               box(40, 60, 360, 90, ["0. giữ hạn mức", "xong"], C_GREEN, bold=True), box(500, 60, 360, 90, ["1. ghi nợ", "xong"], C_GREEN, bold=True),
               box(960, 60, 360, 90, ["2. ghi có", "LỖI"], C_RED, bold=True),
               arrow(400, 105, 495, 105), arrow(860, 105, 955, 105),
               box(500, 250, 360, 90, ["bù: hoàn lại ghi nợ", "chạy trước"], C_AMBER, bold=True),
               box(40, 250, 360, 90, ["bù: trả lại hạn mức", "chạy sau"], C_AMBER, bold=True),
               arrow(960, 160, 865, 245, "#d97706", "lỗi → quay lui"), arrow(500, 295, 405, 295, "#d97706"),
               txt(1180, 300, "Bước đã xong thì bù,", 26, "middle", "#1f2937", True),
               txt(1180, 340, "theo thứ tự ngược lại", 26, "middle", "#1f2937", True)),
           """Hình cho thấy chuỗi ba bước. Bước không giữ hạn mức đã xong. Bước một ghi nợ đã xong. Bước hai ghi có bị lỗi.
           Khi có lỗi, hệ thống quay lui, chạy bước bù cho những bước đã xong, theo thứ tự ngược lại. Ở đây là hoàn lại ghi nợ trước, rồi trả lại hạn mức."""),
        st(svg(1500, 440,
               box(40, 160, 300, 110, ["Dịch vụ", "chuyển tiền"], C_BLUE, bold=True),
               panel(460, 40, 540, 360, "Một giao dịch cơ sở dữ liệu", C_GREEN),
               box(500, 110, 460, 80, "bảng nghiệp vụ: lệnh chuyển", C_GRAY), box(500, 230, 460, 80, "bảng Outbox: sự kiện", C_AMBER),
               arrow(340, 215, 455, 215, "#2a78d6", "ghi cả hai"),
               box(1120, 160, 340, 110, ["Bộ chuyển tiếp", "đọc Outbox → Kafka"], C_PURPLE, bold=True),
               arrow(1000, 270, 1115, 230, "#9333ea", "đọc sau")),
           """Mẫu Outbox giải quyết việc vừa lưu vừa báo. Dịch vụ ghi lệnh chuyển và ghi sự kiện vào hai bảng, nhưng trong cùng một giao dịch, nên cả hai cùng thành công hoặc cùng huỷ.
           Rồi một bộ chuyển tiếp đọc bảng Outbox và gửi sang Kafka, kể cả khi dịch vụ đã sập và chạy lại."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: đếm bước bù và chặn mất sự kiện", [
        st("""<p><b>Bước 1.</b> Không có giao dịch bao nhiều dịch vụ, nên mỗi bước là giao dịch cục bộ riêng và <b>mỗi bước cần một bước bù</b>.</p>
<span class='note'>Làm thử: 3 bước bù được → 3 bước bù. Thông báo đứng sau ghi có, là điểm không quay lại, nên lỗi thì <b>thử lại</b>, không bù.</span>""",
           """Bước một, vì không có giao dịch nào bao được nhiều dịch vụ, nên mỗi bước là một giao dịch cục bộ riêng và mỗi bước cần một bước bù. Làm thử, ba bước giữ hạn mức, ghi nợ, ghi có thì cần ba bước bù.
           Còn thông báo đứng sau ghi có, là điểm không quay lại, nên nếu lỗi thì thử lại, chứ không hoàn tiền."""),
        st("""<p><b>Bước 2.</b> Nếu bước thứ $i$ lỗi (đếm từ $0$), có $i$ bước đã xong cần bù. Nhật ký gồm $i$ bước xong, $1$ lỗi, $i$ bước bù: $2i + 1$ dòng.</p>
<span class='note'>Làm thử: $i = 2$ cho $2 \\cdot 2 + 1 = 5$ dòng.</span>""",
           """Bước hai, vì nếu bước thứ i bị lỗi, đếm từ không, thì có i bước đã xong cần bù. Nên nhật ký gồm i bước xong, một dòng lỗi, và i bước bù, tức hai i cộng một dòng.
           Làm thử, i bằng hai cho hai nhân hai cộng một, bằng năm dòng."""),
        st("""<p><b>Bước 3.</b> Hai việc “lưu” và “báo” ở hai nơi khác nhau có thể sập ở giữa. Outbox gộp hai việc thành <b>một giao dịch</b> nên không có “giữa”.</p>
<span class='note'>Bộ chuyển tiếp có thể phát trùng, nên người nhận phải khử trùng (khoá lũy đẳng).</span>""",
           """Bước ba, vì hai việc lưu và báo ở hai nơi khác nhau có thể sập ở giữa, nên Outbox gộp hai việc thành một giao dịch, và không còn khoảng giữa. Bộ chuyển tiếp có thể phát trùng, nên người nhận phải khử trùng."""),
    ], checks=["2 * 2 + 1 == 5", f"all(len(alg.bnk_saga(i, {_S})) == 2 * i + 1 for i in range(3))", "alg.bnk_outbox_sim('between', True) == (True, 1)"])
    ex = sc("example", "example", "Ví dụ bằng số, từng trường hợp", [
        st("""<p>Ba bước bù được, đánh số $0, 1, 2$: giữ hạn mức, ghi nợ, ghi có.</p>
$$① \\; \\text{bước 0 lỗi: nhật ký} = 2 \\cdot 0 + 1 = \\hl{1}\\ \\text{dòng}$$""",
           """Ta xét ba trường hợp lỗi. Ba bước đánh số từ không, là giữ hạn mức, ghi nợ, ghi có. Trường hợp một, bước không lỗi, chưa có gì để bù, nhật ký có hai nhân không cộng một, bằng một dòng."""),
        st("""$$② \\; \\text{bước 1 lỗi: } 2 \\cdot 1 + 1 = \\hl{3}\\ \\text{dòng: giữ hạn mức, lỗi ghi nợ, bù giữ hạn mức}$$""",
           """Trường hợp hai, bước một lỗi. Có một bước đã xong cần bù, nhật ký có ba dòng, là giữ hạn mức, lỗi ghi nợ, và bù giữ hạn mức, tức trả lại hạn mức."""),
        st("""$$③ \\; \\text{bước 2 lỗi: } 2 \\cdot 2 + 1 = \\hl{5}\\ \\text{dòng}$$""",
           """Trường hợp ba, bước hai là ghi có bị lỗi. Có hai bước đã xong cần bù, nhật ký có năm dòng."""),
        st("""<p>Thứ tự bù ở trường hợp ③:</p>
$$④ \\; \\text{giữ hạn mức},\\ \\text{ghi nợ},\\ \\text{lỗi ghi có},\\ \\hl{\\text{bù ghi nợ}},\\ \\hl{\\text{bù giữ hạn mức}}$$""",
           """Bây giờ xem thứ tự bù ở trường hợp ba. Nhật ký là giữ hạn mức, ghi nợ, lỗi ghi có, rồi bù ghi nợ, rồi bù giữ hạn mức. Bước nào xong sau thì được bù trước."""),
        st("""<p>Outbox: lưu xong rồi sập giữa “lưu” và “báo”.</p>
$$⑤ \\; \\text{không Outbox: } \\hl{0}\\ \\text{sự kiện};\\quad \\text{có Outbox: } \\hlg{1}\\ \\text{sự kiện}$$""",
           """Cuối cùng, trường hợp sập giữa lưu và báo. Không có Outbox thì không sự kiện nào được phát. Có Outbox thì sự kiện vẫn nằm trong bảng và được phát, tức một sự kiện."""),
    ], checks=[f"len(alg.bnk_saga(0, {_S})) == 2 * 0 + 1", f"alg.bnk_saga(1, {_S}) == ['giữ hạn mức', 'lỗi ghi nợ', 'bù giữ hạn mức']",
               f"len(alg.bnk_saga(2, {_S})) == 2 * 2 + 1",
               f"alg.bnk_saga(2, {_S}) == ['giữ hạn mức', 'ghi nợ', 'lỗi ghi có', 'bù ghi nợ', 'bù giữ hạn mức']",
               "alg.bnk_outbox_sim('between', False)[1] == 0 and alg.bnk_outbox_sim('between', True)[1] == 1"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm tay theo dòng", [
        st("""<p>Đường khác: đếm tay từng dòng thay vì công thức. Với bước 2 lỗi: $2$ dòng “xong”, $1$ dòng “lỗi”, $2$ dòng “bù”.</p>
$$2 + 1 + 2 = \\hl{5}$$""",
           """Kiểm bằng đường khác. Ta đếm tay từng dòng thay vì dùng công thức. Với bước hai lỗi, có hai dòng xong, một dòng lỗi và hai dòng bù, tổng là năm, khớp công thức."""),
        st(table(["bước lỗi", "đã xong", "dòng bù", "tổng dòng nhật ký"],
                 [["0", "0", "0", "1"], ["1", "1", "1", "3"], ["2", "2", "2", "5"]]),
           """Bảng này tổng hợp. Vì số dòng bù bằng số bước đã xong, nên bước lỗi càng muộn thì càng nhiều bước phải bù, và nhật ký càng dài."""),
    ], checks=[f"2 + 1 + 2 == 5 == len(alg.bnk_saga(2, {_S}))", f"[len(alg.bnk_saga(i, {_S})) for i in range(3)] == [1, 3, 5]"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tưởng SAGA cho tính <b>cô lập</b> như giao dịch thường. Giữa các bước, người khác vẫn <b class="red">thấy trạng thái dở dang</b>, ví dụ tiền đã trừ mà chưa cộng.</div>""",
           """Lỗi thứ nhất, của người mới. Tưởng SAGA cho tính cô lập như giao dịch thường. Giữa các bước, người khác vẫn thấy trạng thái dở dang, ví dụ tiền đã trừ mà chưa cộng."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Bước bù không lũy đẳng</b>. Bước bù lỗi mạng nên được chạy lại, và hoàn tiền hai lần. Bước bù phải thử lại được, và ghi dấu “đã bù”.</div>""",
           """Lỗi thứ hai, của người đã đi làm, là bước bù không lũy đẳng. Bước bù gặp lỗi mạng sẽ được chạy lại, và hoàn tiền hai lần. Bước bù phải thử lại được, và ghi dấu đã bù."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Ghi kép</b>: lưu cơ sở dữ liệu rồi gửi Kafka thành hai lệnh riêng. Sập giữa hai lệnh thì mất sự kiện. Gửi trước lưu sau thì có sự kiện mà không có dữ liệu.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là ghi kép. Lưu cơ sở dữ liệu rồi gửi Kafka thành hai lệnh riêng. Sập giữa hai lệnh thì mất sự kiện. Gửi trước lưu sau thì có sự kiện mà không có dữ liệu."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Chuỗi có 4 bước (0..3), bước 3 lỗi. Nhật ký có mấy dòng?"],
                  ["2", "Thứ tự chạy bước bù?"],
                  ["3", "Quyết định: điều phối tập trung hay các dịch vụ tự phản ứng sự kiện?"]]),
           """Đến lượt bạn. Câu một, chuỗi có bốn bước đánh số từ không tới ba, bước ba lỗi, nhật ký có mấy dòng? Câu hai, bước bù chạy theo thứ tự nào?
           Câu ba, nên điều phối tập trung hay để các dịch vụ tự phản ứng theo sự kiện? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $i = 3$ bước đã xong.</p>
$$2 \\cdot 3 + 1 = \\hl{7}\\ \\text{dòng}$$""",
           """Đáp án câu một. Bước ba lỗi nghĩa là ba bước đã xong. Hai nhân ba cộng một bằng bảy dòng."""),
        st("""<p>Câu 2: bước nào xong sau thì được bù trước.</p>
$$\\text{bù bước 2} \\to \\text{bù bước 1} \\to \\text{bù bước 0}$$""",
           """Đáp án câu hai. Bước nào xong sau thì được bù trước, nên thứ tự bù là bước hai, bước một, rồi bước không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["điều phối tập trung", "luồng rõ ràng, dễ theo dõi và gỡ lỗi", "người điều phối thành điểm phụ thuộc"],
                  ["tự phản ứng theo sự kiện", "các dịch vụ lỏng lẻo, dễ mở rộng", "luồng khó thấy, khó gỡ lỗi khi nhiều bước"]]),
           """Đáp án câu ba là đánh đổi. Điều phối tập trung cho luồng rõ ràng, dễ theo dõi, nhưng người điều phối thành điểm phụ thuộc. Tự phản ứng theo sự kiện thì các dịch vụ lỏng lẻo hơn, nhưng luồng khó thấy khi có nhiều bước."""),
    ], checks=["2 * 3 + 1 == 7 == len(alg.bnk_saga(3, ['b0', 'b1', 'b2', 'b3']))", "alg.bnk_saga(2, ['b0', 'b1', 'b2'])[-3:] == ['lỗi b2', 'bù b1', 'bù b0']"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("không có giao dịch chung", "chuỗi bước cục bộ", "mỗi bước có bước bù", "Outbox gộp lưu và báo"),
           """Tổng kết chuỗi logic. Không có giao dịch chung, nên ta dùng chuỗi bước cục bộ. Mỗi bước có bước bù. Và Outbox gộp việc lưu với việc báo vào một giao dịch."""),
        st("""<div class='box key'><b>Tư duy:</b> trong hệ phân tán, đừng hỏi “làm sao để không lỗi”. Hãy hỏi <b>“khi lỗi giữa chừng, làm sao quay về trạng thái nhất quán?”</b></div>""",
           """Điều cần mang theo. Trong hệ phân tán, đừng hỏi làm sao để không lỗi. Hãy hỏi, khi lỗi giữa chừng, làm sao quay về trạng thái nhất quán."""),
    ])
    return lesson("L08", "saga_transactional_outbox", "Bài 8 — SAGA và Transactional Outbox",
                  "curriculum/bnk.yaml L08; audit/bnk/verify_bnk.py L08; Garcia-Molina & Salem, Sagas (1987); Richardson, Microservices Patterns (Transactional Outbox)",
                  ["Đếm số dòng nhật ký và thứ tự bước bù khi một bước lỗi", "Giải thích vì sao ghi kép làm mất sự kiện",
                   "Mô tả cách Outbox gộp lưu và báo thành một giao dịch", "Chọn điều phối hay phối hợp theo sự kiện"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
