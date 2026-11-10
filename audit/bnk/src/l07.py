from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao một thông điệp khi thì bị xử lý hai lần, khi thì mất hẳn?", [
        st("""<p>Một bộ đọc Kafka xử lý thông điệp số $2$ rồi <b>sập trước khi ghi nhớ</b> rằng đã đọc. Khi chạy lại, nó đọc thông điệp số $2$ <b>lần nữa</b>.</p>
<div class="box key">Đổi thứ tự “ghi nhớ trước, xử lý sau” thì thông điệp số $2$ lại <b>mất hẳn</b>.</div>""",
           """Chào bạn, một bộ đọc Kafka xử lý thông điệp số hai rồi sập, trước khi kịp ghi nhớ rằng đã đọc. Khi chạy lại, nó đọc thông điệp số hai lần nữa.
           Nếu đổi thứ tự, ghi nhớ trước rồi xử lý sau, thì thông điệp số hai lại mất hẳn."""),
        st(table(["thứ tự", "thông điệp số 2 được xử lý", "tên gọi"],
                 [["xử lý rồi ghi nhớ", "2 lần", "ít nhất một lần"],
                  ["ghi nhớ rồi xử lý", "0 lần", "nhiều nhất một lần"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài. Xử lý rồi mới ghi nhớ thì thông điệp số hai được xử lý hai lần, gọi là ít nhất một lần.
           Ghi nhớ rồi mới xử lý thì có thể mất, gọi là nhiều nhất một lần. Hôm nay ta học cách sống chung với chuyện này."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Kafka và thông điệp", "Kafka là hệ thống chuyển thông điệp: bên gửi ghi thông điệp (một gói dữ liệu báo việc gì đó) vào nhật ký, bên đọc lấy ra xử lý", "“TK-1001 vừa nạp 50 000”"],
                  ["② Nhật ký chỉ thêm", "chỉ ghi nối vào cuối, không sửa dòng cũ", "thông điệp 0, 1, 2, 3, …"],
                  ["③ Số thứ tự (offset)", "vị trí của mỗi thông điệp trong nhật ký", "thông điệp thứ 2 có offset 2"],
                  ["④ Khoá thông điệp và băm chia dư", "khoá (key) là nhãn đi kèm thông điệp, ví dụ số tài khoản; hàm băm biến khoá thành một số (cùng khoá luôn ra cùng số), rồi chia dư để chọn nhóm", "mã băm 13 chia 6 dư 1 → nhóm 1"]]),
           """Trước hết ta cần hiểu bốn điều. Kafka là hệ thống chuyển thông điệp. Bên gửi ghi thông điệp, tức một gói dữ liệu báo việc gì đó, vào nhật ký, còn bên đọc lấy ra xử lý.
           Nhật ký chỉ thêm là chỉ ghi nối vào cuối, không sửa dòng cũ. Số thứ tự cho biết vị trí của mỗi thông điệp trong nhật ký.
           Khoá thông điệp là nhãn đi kèm, ví dụ số tài khoản. Hàm băm biến khoá thành một số, và cùng khoá luôn ra cùng số. Rồi ta chia dư để chọn một nhóm, ví dụ mười ba chia sáu dư một thì vào nhóm một."""),
        st("""$$13 = 2 \\cdot 6 + 1$$""",
           """Kiểm phép chia dư. Mười ba bằng hai nhân sáu cộng một, nên mười ba chia sáu dư một."""),
    ], checks=["13 == 2 * 6 + 1 and 13 % 6 == 1"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["topic", "một luồng thông điệp có tên, ví dụ giao dịch chuyển tiền"],
                  ["partition (phân vùng)", "một nhật ký thật của topic; topic gồm nhiều phân vùng chạy song song"],
                  ["consumer group", "nhóm bộ đọc cùng chia nhau các phân vùng của topic"],
                  ["rebalance", "chia lại phân vùng khi có bộ đọc vào hoặc ra khỏi nhóm"],
                  ["commit offset", "ghi nhớ đã đọc tới đâu để lần sau đọc tiếp"]]),
           """Bảng này giải mã năm từ. Topic là một luồng thông điệp có tên. Phân vùng là một nhật ký thật của topic, và topic gồm nhiều phân vùng chạy song song.
           Nhóm bộ đọc là các bộ đọc cùng chia nhau phân vùng. Chia lại là khi có bộ đọc vào hay ra khỏi nhóm. Còn ghi nhớ vị trí là lưu lại đã đọc tới đâu."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: phân vùng, nhóm bộ đọc và chia lại", [
        st(svg(1500, 420,
               panel(40, 30, 760, 360, "Topic có 6 phân vùng", C_AMBER),
               box(70, 100, 320, 50, "P0: 0 1 2 3 …", C_GRAY, size=22), box(410, 100, 360, 50, "P1: 0 1 2 …", C_GRAY, size=22),
               box(70, 170, 320, 50, "P2: 0 1 2 3 …", C_GRAY, size=22), box(410, 170, 360, 50, "P3: 0 1 …", C_GRAY, size=22),
               box(70, 240, 320, 50, "P4: 0 1 2 …", C_GRAY, size=22), box(410, 240, 360, 50, "P5: 0 1 2 3 …", C_GRAY, size=22),
               panel(900, 30, 560, 360, "Nhóm bộ đọc: 3 người", C_GREEN),
               box(940, 100, 480, 70, "Đọc 1: P0, P1", C_BLUE), box(940, 190, 480, 70, "Đọc 2: P2, P3", C_BLUE), box(940, 280, 480, 70, "Đọc 3: P4, P5", C_BLUE)),
           """Hình cho thấy topic có sáu phân vùng, mỗi phân vùng là một nhật ký riêng. Nhóm có ba bộ đọc, mỗi bộ đọc nhận hai phân vùng.
           Quy tắc quan trọng là mỗi phân vùng chỉ có một bộ đọc trong nhóm, nên thứ tự trong phân vùng được giữ."""),
        st(svg(1500, 420,
               panel(40, 30, 700, 360, "Trước: 3 người", C_GREEN),
               box(70, 100, 640, 60, "Đọc 1: P0, P1", C_BLUE), box(70, 180, 640, 60, "Đọc 2: P2, P3", C_BLUE, dash=True), box(70, 260, 640, 60, "Đọc 3: P4, P5", C_BLUE),
               arrow(750, 210, 810, 210, "#dc2626"),
               panel(820, 30, 640, 360, "Sau khi Đọc 2 rời nhóm", C_AMBER),
               box(850, 100, 580, 60, "Đọc 1: P0, P1, P2", C_BLUE), box(850, 200, 580, 60, "Đọc 3: P3, P4, P5", C_BLUE),
               txt(1140, 320, "chia lại (rebalance): mỗi người 3 phân vùng", 24, "middle", "#1f2937", True)),
           """Khi một bộ đọc rời nhóm, hệ thống chia lại. Còn hai bộ đọc, nên sáu phân vùng chia thành ba cho mỗi người.
           Trong lúc chia lại, việc đọc có thể tạm dừng, và các thông điệp chưa ghi nhớ vị trí có thể bị đọc lại."""),
        st(svg(1500, 400,
               box(60, 70, 320, 80, "đọc thông điệp", C_BLUE), box(480, 70, 320, 80, "xử lý", C_GREEN), box(900, 70, 320, 80, "ghi nhớ vị trí", C_AMBER),
               arrow(380, 110, 475, 110), arrow(800, 110, 895, 110),
               txt(750, 210, "Sập giữa “xử lý” và “ghi nhớ” → khởi động lại đọc lại → xử lý hai lần", 26, "middle", "#dc2626", True),
               box(60, 260, 320, 80, "đọc thông điệp", C_BLUE), box(480, 260, 320, 80, "ghi nhớ vị trí", C_AMBER), box(900, 260, 320, 80, "xử lý", C_GREEN),
               arrow(380, 300, 475, 300), arrow(800, 300, 895, 300),
               txt(750, 385, "Sập giữa “ghi nhớ” và “xử lý” → khởi động lại bỏ qua → mất thông điệp", 26, "middle", "#dc2626", True)),
           """Hình thứ ba cho thấy hai thứ tự. Hàng trên, xử lý rồi mới ghi nhớ. Sập ở giữa thì khi chạy lại sẽ đọc lại, nên xử lý hai lần.
           Hàng dưới, ghi nhớ rồi mới xử lý. Sập ở giữa thì khi chạy lại sẽ bỏ qua, nên mất thông điệp."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: chia việc và số lần xử lý", [
        st("""<p><b>Bước 1.</b> Cùng khoá băm ra cùng phân vùng, <b>miễn là số phân vùng không đổi</b>, nên thông điệp cùng một tài khoản nằm cùng một phân vùng và <b>giữ đúng thứ tự</b>.</p>
<span class='note'>Làm thử: khoá TK-1001 hai lần đều vào phân vùng 1. Thêm phân vùng thì khoá có thể chuyển sang phân vùng khác.</span>""",
           """Bước một, vì cùng khoá băm ra cùng phân vùng, miễn là số phân vùng không đổi, nên thông điệp của cùng một tài khoản nằm cùng một phân vùng và giữ đúng thứ tự. Làm thử, khoá T K một không không một hai lần đều vào phân vùng một.
           Nếu thêm phân vùng, phép chia dư đổi, và khoá có thể chuyển sang phân vùng khác."""),
        st("""<p><b>Bước 2.</b> Mỗi phân vùng chỉ một bộ đọc trong nhóm, nên số bộ đọc làm việc thật sự tối đa bằng <b>số phân vùng</b>.</p>
<span class='note'>Làm thử: $6$ phân vùng, $8$ bộ đọc → $6$ làm việc, $2$ ngồi không.</span>""",
           """Bước hai, vì mỗi phân vùng chỉ có một bộ đọc trong nhóm, nên số bộ đọc làm việc tối đa bằng số phân vùng. Làm thử, sáu phân vùng mà tám bộ đọc thì sáu người làm việc, hai người ngồi không."""),
        st("""<p><b>Bước 3.</b> Số lần xử lý một thông điệp phụ thuộc <b>thứ tự</b> giữa xử lý và ghi nhớ khi sập: xử lý trước thì $\\ge 1$ lần, ghi nhớ trước thì $\\le 1$ lần.</p>
<span class='note'>Muốn đúng một lần về hiệu quả: xử lý trước, ghi nhớ sau, và để việc xử lý lũy đẳng.</span>""",
           """Bước ba, vì khi sập, thứ tự giữa xử lý và ghi nhớ quyết định kết quả, nên xử lý trước thì ít nhất một lần, ghi nhớ trước thì nhiều nhất một lần. Muốn hiệu quả đúng một lần, ta xử lý trước, ghi nhớ sau, và làm việc xử lý lũy đẳng."""),
    ], checks=["[alg.bnk_key_partition(k, 6) for k in ('TK-1001', 'TK-1001')] == [1, 1]", "len(alg.bnk_assign(6, 8)[6]) + len(alg.bnk_assign(6, 8)[7]) == 0 and sum(1 for g in alg.bnk_assign(6, 8) if g) == 6",
               "alg.bnk_commit_sim(5, 2, False)[2] >= 1 and alg.bnk_commit_sim(5, 2, True)[2] <= 1"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Topic $6$ phân vùng, nhóm $3$ bộ đọc: chia đều.</p>
$$① \\; \\frac{6}{3} = \\hl{2}\\ \\text{phân vùng mỗi người}$$""",
           """Ta tính bốn tình huống. Tình huống một, topic sáu phân vùng, nhóm ba bộ đọc, chia đều thì mỗi người nhận sáu chia ba, là hai phân vùng."""),
        st("""<p>Một người rời nhóm, còn $2$ người.</p>
$$② \\; \\frac{6}{2} = \\hl{3}\\ \\text{phân vùng mỗi người}$$""",
           """Tình huống hai, một người rời nhóm, còn hai người. Mỗi người nhận sáu chia hai, là ba phân vùng."""),
        st("""<p>Thêm người cho đủ $8$ bộ đọc.</p>
$$③ \\; 8 - 6 = \\hl{2}\\ \\text{người ngồi không}$$""",
           """Tình huống ba, thêm người cho đủ tám bộ đọc. Chỉ có sáu phân vùng nên hai người ngồi không, tám trừ sáu bằng hai."""),
        st("""<p>Năm thông điệp $0..4$, ghi nhớ vị trí sau từng thông điệp. Sập ở thông điệp $2$, thứ tự <b>xử lý rồi ghi nhớ</b>.</p>
$$④ \\; \\text{số lần xử lý} = [1, 1, \\hl{2}, 1, 1]\\quad \\text{tổng } 6$$
<p class="small">Ghi nhớ theo lô nhiều thông điệp một lần thì còn nhiều thông điệp bị xử lý lại hơn.</p>""",
           """Tình huống bốn, năm thông điệp từ không tới bốn, và bộ đọc ghi nhớ vị trí sau từng thông điệp. Sập ở thông điệp hai, thứ tự xử lý rồi ghi nhớ. Số lần xử lý là một, một, hai, một, một, tổng cộng sáu lần cho năm thông điệp.
           Nếu ghi nhớ theo lô nhiều thông điệp một lần, số thông điệp bị xử lý lại còn nhiều hơn.""", clear=True),
        st("""<p>Cùng tình huống nhưng <b>ghi nhớ rồi xử lý</b>.</p>
$$⑤ \\; \\text{số lần xử lý} = [1, 1, \\hl{0}, 1, 1]\\quad \\text{tổng } 4$$""",
           """Tình huống năm, cùng tình huống nhưng ghi nhớ rồi mới xử lý. Số lần xử lý là một, một, không, một, một, tổng bốn lần, tức là mất thông điệp số hai."""),
    ], checks=["6 // 3 == 2 and alg.bnk_assign(6, 3) == [[0, 1], [2, 3], [4, 5]]", "6 // 2 == 3 and alg.bnk_assign(6, 2) == [[0, 1, 2], [3, 4, 5]]",
               "8 - 6 == 2", "alg.bnk_commit_sim(5, 2, False) == [1, 1, 2, 1, 1] and sum(alg.bnk_commit_sim(5, 2, False)) == 6",
               "alg.bnk_commit_sim(5, 2, True) == [1, 1, 0, 1, 1] and sum(alg.bnk_commit_sim(5, 2, True)) == 4"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: khử trùng ở phía xử lý", [
        st("""<p>Đường khác: giữ <b>tập các mã đã xử lý</b>. Thông điệp số $2$ đến hai lần, nhưng lần hai gặp mã đã có nên bỏ qua.</p>
$$\\text{số thông điệp xử lý thật} = \\hlg{5}$$""",
           """Kiểm bằng đường khác. Vì thông điệp đến ít nhất một lần, nên ta giữ tập các mã đã xử lý. Thông điệp số hai đến hai lần, nhưng lần hai gặp mã đã có nên bị bỏ qua. Kết quả là năm thông điệp được xử lý thật, đúng mỗi thông điệp một lần."""),
        st(table(["cách", "xử lý thật mỗi thông điệp", "điều kiện"],
                 [["ít nhất một lần + khử trùng", "đúng 1 lần (về hiệu quả)", "mã thông điệp duy nhất, kho mã bền; ghi mã đã xử lý và tác dụng nghiệp vụ trong cùng một giao dịch cơ sở dữ liệu"],
                  ["nhiều nhất một lần", "0 hoặc 1 lần", "chấp nhận mất"]]),
           """Bảng này so hai cách. Vì thông điệp đã đến ít nhất một lần, nên khử trùng cho hiệu quả đúng một lần, với điều kiện mã thông điệp duy nhất và kho mã bền.
           Mã đã xử lý và tác dụng nghiệp vụ phải được ghi trong cùng một giao dịch cơ sở dữ liệu, nếu không thì sập ở giữa vẫn trùng hoặc mất.
           Nhiều nhất một lần thì có thể mất, chỉ dùng khi chấp nhận mất."""),
    ], checks=["len(set(i for i, c in enumerate(alg.bnk_commit_sim(5, 2, False)) for _ in range(c))) == 5"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ thêm bộ đọc là nhanh hơn mãi. Quá số phân vùng, các bộ đọc thừa <b class="red">ngồi không</b>.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ thêm bộ đọc là nhanh hơn mãi. Quá số phân vùng thì các bộ đọc thừa ngồi không."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Xử lý quá lâu</b> trong một lần đọc. Bộ đọc bị coi là chết, nhóm chia lại, thông điệp đang xử lý bị giao cho người khác và <b>xử lý hai lần</b>.
<br><span class="note">Cách chữa: gọi <code>poll()</code> lại trong hạn <code>max.poll.interval.ms</code> (giảm <code>max.poll.records</code> hoặc tăng hạn), và làm việc xử lý lũy đẳng.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là xử lý quá lâu trong một lần đọc. Bộ đọc bị coi là chết, nhóm chia lại, thông điệp đang xử lý bị giao cho người khác và xử lý hai lần.
           Nhịp báo còn sống chạy ở một luồng riêng, nên lỗi này là do quá hạn giữa hai lần đọc. Cách chữa là đọc lại trong hạn cho phép, bằng cách lấy ít thông điệp hơn mỗi lần hoặc tăng hạn, và làm việc xử lý lũy đẳng."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nghe “đúng một lần” của Kafka rồi tin mọi tác dụng phụ chỉ xảy ra một lần. Giao dịch của Kafka chỉ bao trùm đọc, xử lý, ghi <b>trong Kafka</b>.
Ghi vào cơ sở dữ liệu hay gọi hệ ngoài vẫn cần khoá lũy đẳng.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nghe đúng một lần của Kafka rồi tin mọi tác dụng phụ chỉ xảy ra một lần. Giao dịch của Kafka chỉ bao trùm việc đọc, xử lý và ghi bên trong Kafka.
           Ghi vào cơ sở dữ liệu hay gọi hệ ngoài vẫn cần khoá lũy đẳng."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "10 phân vùng, 4 bộ đọc. Mỗi người nhận mấy phân vùng (chia khoảng liền nhau)?"],
                  ["2", "10 phân vùng, 12 bộ đọc. Mấy người ngồi không?"],
                  ["3", "Quyết định: lệnh trừ tiền nên ghi nhớ vị trí trước hay sau khi xử lý?"]]),
           """Đến lượt bạn. Câu một, mười phân vùng, bốn bộ đọc, mỗi người nhận mấy phân vùng? Câu hai, mười phân vùng, mười hai bộ đọc, mấy người ngồi không?
           Câu ba, lệnh trừ tiền nên ghi nhớ vị trí trước hay sau khi xử lý? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $10 = 4 \\cdot 2 + 2$, nên hai người đầu nhận $3$, hai người sau nhận $2$.</p>
$$[3, 3, 2, 2]\\quad 3 + 3 + 2 + 2 = \\hl{10}$$""",
           """Đáp án câu một. Mười bằng bốn nhân hai cộng hai, nên hai người đầu nhận ba phân vùng, hai người sau nhận hai. Ba cộng ba cộng hai cộng hai bằng mười."""),
        st("""$$12 - 10 = \\hlg{2}\\ \\text{người ngồi không}$$""",
           """Đáp án câu hai. Mười hai bộ đọc trừ mười phân vùng, nên hai người ngồi không."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["xử lý rồi ghi nhớ + khoá lũy đẳng", "không mất lệnh, trùng thì bị chặn", "phải làm khoá lũy đẳng"],
                  ["ghi nhớ rồi xử lý", "không bao giờ xử lý hai lần", "có thể mất lệnh trừ tiền"]]),
           """Đáp án câu ba. Với lệnh trừ tiền, mất lệnh nguy hiểm hơn trùng lệnh, vì trùng ta chặn được bằng khoá lũy đẳng. Nên chọn xử lý rồi mới ghi nhớ, kèm khoá lũy đẳng."""),
    ], checks=["[len(g) for g in alg.bnk_assign(10, 4)] == [3, 3, 2, 2]", "12 - 10 == 2 and sum(1 for g in alg.bnk_assign(10, 12) if not g) == 2"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("khoá → phân vùng", "mỗi phân vùng một bộ đọc", "sập → đọc lại", "xử lý lũy đẳng"),
           """Tổng kết chuỗi logic. Khoá quyết định phân vùng. Mỗi phân vùng chỉ một bộ đọc. Sập thì đọc lại, nên việc xử lý phải lũy đẳng."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng hỏi “Kafka có đúng một lần không”. Hãy hỏi <b>“khi sập giữa chừng, việc của tôi chạy mấy lần, và có hại không?”</b></div>""",
           """Điều cần mang theo. Đừng hỏi Kafka có đúng một lần không. Hãy hỏi, khi sập giữa chừng, việc của tôi chạy mấy lần, và có hại không."""),
    ])
    return lesson("L07", "kafka_partition_offset", "Bài 7 — Kafka: phân vùng, offset, chia lại và số lần xử lý",
                  "curriculum/bnk.yaml L07; audit/bnk/verify_bnk.py L07; Apache Kafka documentation (consumer groups, delivery semantics); băm crc32 chỉ để tất định, Kafka dùng murmur2",
                  ["Chia phân vùng cho nhóm bộ đọc và tính số người ngồi không", "Giải thích vì sao cùng khoá giữ đúng thứ tự",
                   "Dự đoán số lần xử lý theo thứ tự ghi nhớ và xử lý khi sập", "Khử trùng ở phía xử lý để được hiệu quả đúng một lần"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
