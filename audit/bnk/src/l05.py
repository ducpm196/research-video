from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao hai lệnh chuyển tiền ngược chiều lại làm nhau treo?", [
        st("""<p>Lệnh 1 chuyển từ tài khoản A sang B. Lệnh 2 chuyển từ B sang A, cùng lúc. Mỗi lệnh <b>khoá hàng của mình trước</b> rồi chờ hàng của lệnh kia.</p>
<div class="box key">Cả hai chờ nhau mãi. Oracle phát hiện và trả lỗi <b>ORA-00060</b> cho một trong hai.</div>""",
           """Chào bạn, lệnh một chuyển từ tài khoản A sang B. Lệnh hai chuyển từ B sang A, cùng lúc. Mỗi lệnh khoá hàng của mình trước, rồi chờ hàng của lệnh kia.
           Cả hai chờ nhau mãi. Oracle phát hiện chuyện này và trả lỗi O R A không không không sáu không cho một trong hai lệnh."""),
        st(table(["thứ tự khoá của hai phiên", "kết quả mô phỏng"],
                 [["A rồi B  và  B rồi A (ngược nhau)", "bế tắc khoá"],
                  ["A rồi B  và  A rồi B (cùng thứ tự)", "chạy bình thường"]]),
           """Bảng này là kết quả mô phỏng ở cuối bài. Hai phiên khoá ngược thứ tự thì bế tắc. Hai phiên khoá cùng thứ tự thì chạy bình thường.
           Cách chữa nằm gọn trong một quy tắc, ta sẽ học hôm nay."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Phiên", "một kết nối đang làm việc với cơ sở dữ liệu (cơ sở dữ liệu: phần mềm lưu bảng, hỏi bằng ngôn ngữ SQL), thường của một luồng chương trình", "phiên 1, phiên 2"],
                  ["② Giao dịch", "nhiều thao tác cùng thành công hoặc cùng huỷ; kết thúc bằng commit (chốt lưu) hoặc rollback (huỷ hết)", "trừ A rồi cộng B"],
                  ["③ Khoá hàng", "khi một phiên sửa một hàng, hàng đó bị khoá tới khi giao dịch kết thúc", "UPDATE (lệnh SQL sửa hàng) tài khoản A"],
                  ["④ Chờ", "phiên khác muốn sửa hàng đang khoá thì phải đứng chờ", "phiên 2 chờ hàng A"]]),
           """Trước hết ta cần hiểu bốn điều. Phiên là một kết nối đang làm việc với cơ sở dữ liệu, tức phần mềm lưu bảng dữ liệu mà ta hỏi bằng ngôn ngữ SQL.
           Giao dịch là nhiều thao tác cùng thành công hoặc cùng huỷ, và kết thúc bằng chốt để lưu, hoặc hoàn tác để huỷ hết.
           Khi một phiên sửa một hàng, hàng đó bị khoá cho tới khi giao dịch kết thúc. Phiên khác muốn sửa hàng đang khoá thì phải đứng chờ.
           Vì khoá chỉ được nhả khi giao dịch kết thúc, nên một giao dịch dài giữ khoá lâu."""),
        st("""$$2 \\cdot 2 = 4$$""",
           """Một phép đếm cần dùng. Hai phiên, mỗi phiên có hai cách chọn thứ tự khoá hai hàng, nên có hai nhân hai bằng bốn cặp thứ tự. Ta sẽ xem cặp nào gây bế tắc."""),
    ], checks=["2 * 2 == 4"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["id", "mã số định danh mỗi hàng, ví dụ mã tài khoản 2, 5"],
                  ["deadlock (bế tắc)", "hai hay nhiều phiên chờ nhau theo vòng tròn, không ai đi tiếp được"],
                  ["SELECT ... FOR UPDATE", "đọc và khoá luôn các hàng đọc được để sửa an toàn"],
                  ["ORA-00060", "mã lỗi Oracle: phát hiện bế tắc khi chờ tài nguyên"],
                  ["đồ thị chờ", "mũi tên từ phiên đang chờ tới phiên đang giữ khoá; có vòng tròn là bế tắc"],
                  ["PL/SQL", "ngôn ngữ lập trình thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu"]]),
           """Bảng dưới đây giải thích nghĩa của sáu thuật ngữ sẽ gặp trong bài. Mã số định danh là con số riêng của mỗi hàng, ví dụ mã tài khoản hai và năm. Bế tắc là khi hai hay nhiều phiên chờ nhau theo vòng tròn, không ai đi tiếp được. Câu lệnh đọc kèm khoá cho phép đọc rồi khoá luôn các hàng để sửa an toàn.
           Mã lỗi sáu mươi là cách Oracle báo đã phát hiện bế tắc. Đồ thị chờ có mũi tên từ phiên chờ tới phiên giữ khoá, có vòng tròn là bế tắc.
           Cuối cùng, P L S Q L là ngôn ngữ thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: vòng tròn chờ", [
        st(svg(1500, 450,
               box(100, 40, 300, 90, ["Phiên 1", "giữ hàng A"], C_BLUE, bold=True),
               box(1100, 40, 300, 90, ["Phiên 2", "giữ hàng B"], C_AMBER, bold=True),
               box(100, 290, 300, 90, "hàng B (đang bị khoá)", C_GRAY), box(1100, 290, 300, 90, "hàng A (đang bị khoá)", C_GRAY),
               arrow(250, 135, 250, 285, "#dc2626", "muốn B", dash=True), arrow(1250, 135, 1250, 285, "#dc2626", "muốn A", dash=True),
               arrow(405, 85, 1095, 85, "#6b7280", "A đang do phiên 1 giữ"),
               txt(750, 425, "Phiên 1 chờ phiên 2, phiên 2 chờ phiên 1 → vòng tròn → bế tắc", 26, "middle", "#dc2626", True)),
           """Hình cho thấy vòng tròn chờ. Phiên một đang giữ hàng A và muốn hàng B. Phiên hai đang giữ hàng B và muốn hàng A.
           Phiên một chờ phiên hai, phiên hai lại chờ phiên một. Không phiên nào chịu nhả khoá đang giữ, nên đó là bế tắc."""),
        st(svg(1500, 420,
               txt(750, 40, "Quy tắc: luôn khoá theo thứ tự id tăng dần", 28, "middle", "#1f2937", True),
               box(60, 90, 300, 80, ["Phiên 1: chuyển", "id 2 → id 5"], C_BLUE, size=22), box(60, 220, 300, 80, ["Phiên 2: chuyển", "id 5 → id 2"], C_AMBER, size=22),
               arrow(365, 130, 560, 130, "#475569"), arrow(365, 260, 560, 260, "#475569"),
               box(570, 90, 360, 80, "sắp lại: khoá 2 rồi 5", C_GREEN), box(570, 220, 360, 80, "sắp lại: khoá 2 rồi 5", C_GREEN),
               box(1020, 150, 420, 100, ["cả hai cùng thứ tự", "→ không có vòng tròn"], C_GREEN, bold=True),
               arrow(935, 130, 1015, 190, "#475569"), arrow(935, 260, 1015, 220, "#475569")),
           """Cách phá vòng tròn là một quy tắc. Phiên một chuyển từ tài khoản mã hai sang mã năm, phiên hai chuyển ngược lại. Dù lệnh chuyển theo chiều nào, ta luôn khoá hàng có id nhỏ trước, rồi mới khoá hàng có id lớn.
           Khi mọi phiên cùng một thứ tự, không thể có vòng tròn chờ."""),
        st(svg(1500, 400,
               box(60, 40, 1380, 60, "DECLARE  — khai báo biến (không bắt buộc)", C_GRAY),
               box(60, 120, 1380, 100, ["BEGIN  — các lệnh chạy theo thứ tự", "khoá hàng nhỏ trước, rồi hàng lớn; trừ; cộng"], C_BLUE),
               box(60, 240, 1380, 70, "EXCEPTION  — xử lý lỗi, ví dụ ORA-00060", C_RED),
               box(60, 330, 1380, 50, "END;", C_GRAY, size=24)),
           """Một khối P L S Q L gồm bốn phần. Khai báo biến không bắt buộc. Phần chính chạy các lệnh theo thứ tự, ở đây là khoá hàng nhỏ trước, rồi hàng lớn, rồi trừ và cộng.
           Phần xử lý lỗi bắt những lỗi như bế tắc. Cuối cùng là từ khoá kết thúc. Ta chỉ cần hiểu khung này, không cần học thuộc cú pháp."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: vì sao thứ tự khoá chặn được bế tắc?", [
        st("""<p><b>Bước 1.</b> Bế tắc cần một <b>vòng tròn chờ</b>: phiên 1 chờ phiên 2, phiên 2 chờ phiên 1.</p>
<span class='note'>Làm thử: 2 phiên, 2 mũi tên chờ khép kín.</span>""",
           """Bước một, vì bế tắc cần một vòng tròn chờ, nên ta chỉ cần ngăn vòng tròn xuất hiện. Làm thử, hai phiên chờ nhau tạo ra hai mũi tên khép kín."""),
        st("""<p><b>Bước 2.</b> Vòng tròn <b>chỉ có thể</b> xuất hiện khi hai phiên lấy hai khoá theo <b>thứ tự ngược nhau</b>, và xảy ra thật khi cả hai kịp giữ khoá đầu. Với 2 khoá có $2 \\cdot 2 = 4$ cặp thứ tự, trong đó $2$ cặp ngược nhau.</p>
<span class='note'>Làm thử: (A,B)+(B,A) và (B,A)+(A,B) là hai cặp ngược.</span>""",
           """Bước hai, vì phiên giữ một khoá rồi xin khoá thứ hai, nên trong mô hình hai hàng này, vòng tròn chỉ có thể xuất hiện khi hai phiên lấy hai khoá theo thứ tự ngược nhau. Nó xảy ra thật khi cả hai phiên kịp giữ khoá đầu trước khi xin khoá thứ hai.
           Với hai khoá có bốn cặp thứ tự, trong đó hai cặp ngược nhau.
           Làm thử, A rồi B kèm B rồi A là một cặp ngược, và cặp đảo lại là cặp ngược thứ hai."""),
        st("""<p><b>Bước 3.</b> Nếu mọi phiên đều khoá theo thứ tự tăng của id, mọi cặp thứ tự đều <b>giống nhau</b>, nên số cặp ngược là $0$.</p>
<span class='note'>Làm thử: sắp lại cả hai phiên thành (2,5) và (2,5) → chạy bình thường.</span>""",
           """Bước ba, vì nếu mọi phiên đều khoá theo thứ tự tăng của id, thì mọi cặp thứ tự đều giống nhau, nên số cặp ngược là không. Làm thử, sắp lại cả hai phiên thành hai rồi năm, thì chạy bình thường."""),
    ], checks=["2 * 2 == 4", "[alg.bnk_lock_sim([p, q]) for p in (['A', 'B'], ['B', 'A']) for q in (['A', 'B'], ['B', 'A'])] == ['ok', 'deadlock', 'deadlock', 'ok']",
               "alg.bnk_lock_sim([sorted([5, 2]), sorted([2, 5])]) == 'ok'"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Hai tài khoản có id $2$ và $5$. Lệnh 1 chuyển $2 \\to 5$, lệnh 2 chuyển $5 \\to 2$. Mỗi lệnh khoá <b>nguồn trước</b>.</p>
$$① \\; \\text{Phiên 1 khoá } 2,\\ \\text{Phiên 2 khoá } 5$$""",
           """Ta theo dõi từng bước. Hai tài khoản có id hai và năm. Lệnh một chuyển từ hai sang năm, lệnh hai chuyển từ năm sang hai, mỗi lệnh khoá nguồn trước.
           Bước thứ nhất, phiên một khoá hàng hai, phiên hai khoá hàng năm."""),
        st("""<p>Vòng chờ kế tiếp: Phiên 1 xin hàng $5$ nhưng $5$ đang bị Phiên 2 giữ; Phiên 2 xin hàng $2$ nhưng $2$ đang bị Phiên 1 giữ.</p>
$$② \\; \\text{không ai tiến thêm được} \\Rightarrow \\hl{\\text{bế tắc}}$$""",
           """Bước thứ hai, phiên một xin hàng năm nhưng hàng năm đang do phiên hai giữ. Phiên hai xin hàng hai nhưng hàng hai đang do phiên một giữ. Không ai tiến thêm được, nên là bế tắc."""),
        st("""<p>Áp quy tắc: mỗi lệnh sắp hai id tăng dần, ra $(2, 5)$.</p>
$$③ \\; \\text{Phiên 1: } 2 \\to 5,\\quad \\text{Phiên 2: } 2 \\to 5$$""",
           """Bước thứ ba, áp quy tắc. Mỗi lệnh sắp hai id tăng dần, nên cả hai cùng khoá hai rồi mới tới năm.""", clear=True),
        st("""<p>Phiên 1 khoá $2$ trước. Phiên 2 cũng xin $2$ nên <b>chờ ngay từ đầu</b> và chưa giữ gì cả.</p>
$$④ \\; \\text{số khoá Phiên 2 đang giữ} = \\hlg{0} \\Rightarrow \\text{không ai bị chờ vòng}$$""",
           """Bước thứ tư, phiên một khoá hai trước. Phiên hai cũng cần hai nên chờ ngay từ đầu và chưa giữ khoá nào. Vì phiên hai không giữ gì, nên không ai bị chờ vòng."""),
        st("""<p>Phiên 1 khoá $5$, trừ, cộng, commit, nhả cả hai khoá. Phiên 2 vào.</p>
$$⑤ \\; \\text{kết quả} = \\hlg{\\text{cả hai lệnh xong lần lượt}}$$""",
           """Bước thứ năm, phiên một khoá hàng năm, trừ và cộng, rồi commit và nhả cả hai khoá. Phiên hai mới vào, nên cả hai lệnh xong lần lượt."""),
    ], checks=["alg.bnk_lock_sim([[2, 5], [5, 2]]) == 'deadlock'", "alg.bnk_lock_sim([sorted([2, 5]), sorted([5, 2])]) == 'ok'"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: thử hết cặp thứ tự", [
        st("""<p>Đường khác: vì chỉ có hai khoá, ta vét cạn mọi cặp thứ tự, rồi chạy mô phỏng cho từng cặp.</p>""",
           """Kiểm bằng đường khác. Ta vét cạn mọi cặp thứ tự của hai khoá, rồi chạy mô phỏng cho từng cặp. Mô phỏng chỉ kiểm logic thứ tự khoá, còn cú pháp riêng của Oracle thì máy này không chạy được."""),
        st(table(["phiên 1", "phiên 2", "kết quả (khi cả hai kịp giữ khoá đầu)"],
                 [["A, B", "A, B", "bình thường"], ["A, B", "B, A", "bế tắc"], ["B, A", "A, B", "bế tắc"], ["B, A", "B, A", "bình thường"]]),
           """Bốn cặp thứ tự cho kết quả này, trong trường hợp cả hai phiên kịp giữ khoá đầu. Vì chỉ hai cặp ngược nhau mới bế tắc, nên kết quả khớp với bước hai. Hai cặp cùng thứ tự đều chạy bình thường."""),
        st(table(["nguyên nhân ORA-00060 ngoài đời", "sắp thứ tự hàng có chữa được?", "cách chữa"],
                 [["hai phiên khoá hàng ngược thứ tự", "có", "khoá theo id tăng dần"],
                  ["khoá ngoại (cột ở bảng con trỏ tới bảng cha) không có chỉ mục: xoá hay sửa khoá chính ở bảng cha thì Oracle khoá cả bảng con", "không", "tạo chỉ mục (cấu trúc tra nhanh) cho cột khoá ngoại"],
                  ["thiếu chỗ ITL (danh sách giao dịch đang sửa khối) trong khối dữ liệu (đơn vị nhỏ nhất Oracle đọc ghi trên đĩa, chứa nhiều hàng), INITRANS thấp", "không", "tăng INITRANS cho bảng hay chỉ mục nóng"]]),
           """Bảng này nhắc rằng ngoài đời, lỗi bế tắc còn có nguyên nhân khác. Một là khoá ngoại không có chỉ mục. Khoá ngoại là cột ở bảng con trỏ tới một hàng của bảng cha, còn chỉ mục là cấu trúc giúp tra nhanh.
           Khi thiếu chỉ mục đó, xoá hay sửa khoá chính ở bảng cha làm Oracle khoá cả bảng con, nên nhiều phiên dễ chờ nhau.
           Hai là khối dữ liệu, tức đơn vị nhỏ nhất Oracle đọc ghi trên đĩa và chứa nhiều hàng, thiếu chỗ ghi các giao dịch đang sửa nó. Sắp thứ tự hàng không chữa được hai loại này, mà phải tạo chỉ mục hoặc tăng chỗ trong khối.""",
           clear=True),
    ], checks=["sum(1 for p in (['A', 'B'], ['B', 'A']) for q in (['A', 'B'], ['B', 'A']) if alg.bnk_lock_sim([p, q]) == 'deadlock') == 2"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ đọc dữ liệu cũng làm người khác chờ. Với Oracle, <b>câu SELECT thường không khoá hàng</b> và người đọc không chặn người ghi.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ đọc dữ liệu cũng làm người khác chờ. Với Oracle, câu đọc thông thường không khoá hàng, và người đọc không chặn người ghi."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Khoá theo thứ tự người gọi đưa vào</b>, tức nguồn rồi đích. Hai lệnh ngược chiều sẽ gặp bế tắc đúng lúc cao điểm.
<br><span class="note">Cách chữa: sắp các id tăng dần rồi khoá từng hàng bằng câu riêng; đừng tin <code>ORDER BY … FOR UPDATE</code> khoá theo thứ tự ORDER BY.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là khoá theo thứ tự người gọi đưa vào, tức nguồn rồi đích. Hai lệnh ngược chiều sẽ gặp bế tắc đúng lúc cao điểm.
           Cách chữa là sắp các id tăng dần, rồi khoá từng hàng bằng một câu lệnh riêng. Đừng tin rằng một câu đọc kèm khoá có sắp thứ tự sẽ khoá đúng theo thứ tự đã sắp."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Gặp ORA-00060 rồi <b>thử lại ngay</b>. Theo mô tả của Oracle, chỉ <b>câu lệnh</b> bị huỷ, không phải cả giao dịch, nên các khoá cũ vẫn còn.
<br><span class="note">Cách chữa: rollback cả giao dịch rồi mới thử lại, kèm giới hạn số lần thử.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là gặp lỗi bế tắc rồi thử lại ngay. Theo mô tả của Oracle, chỉ câu lệnh bị huỷ, không phải cả giao dịch, nên các khoá cũ vẫn còn.
           Cách chữa là rollback cả giao dịch rồi mới thử lại, kèm giới hạn số lần thử."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Với 3 khoá, mỗi phiên khoá cả 3 theo một thứ tự. Mỗi phiên có bao nhiêu thứ tự?"],
                  ["2", "Chuyển tiền từ tài khoản 9 sang tài khoản 4. Thứ tự khoá đúng?"],
                  ["3", "Quyết định: tránh bế tắc bằng sắp thứ tự, hay đặt giới hạn chờ rồi thử lại?"]]),
           """Đến lượt bạn. Câu một, với ba khoá, mỗi phiên khoá cả ba theo một thứ tự, mỗi phiên có bao nhiêu thứ tự? Câu hai, chuyển tiền từ tài khoản chín sang tài khoản bốn, thứ tự khoá đúng là gì?
           Câu ba, nên tránh bế tắc bằng sắp thứ tự, hay đặt giới hạn chờ rồi thử lại? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: chọn khoá đầu có $3$ cách, khoá hai có $2$ cách, khoá ba có $1$ cách.</p>
$$3 \\cdot 2 \\cdot 1 = \\hl{6}$$""",
           """Đáp án câu một. Khoá đầu có ba cách chọn, khoá thứ hai có hai cách, khoá thứ ba còn một cách. Ba nhân hai nhân một bằng sáu thứ tự."""),
        st("""<p>Câu 2: id nhỏ trước, id lớn sau.</p>
$$\\text{khoá } 4 \\text{ trước, rồi khoá } 9$$""",
           """Đáp án câu hai. Luôn khoá id nhỏ trước, nên khoá tài khoản bốn trước, rồi mới khoá tài khoản chín, dù tiền đi từ chín sang bốn."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["sắp thứ tự khoá", "ngăn bế tắc từ gốc", "phải biết trước mọi khoá cần lấy"],
                  ["giới hạn chờ rồi thử lại", "đơn giản, bắt được mọi trường hợp", "bế tắc vẫn xảy ra, tốn thời gian chờ và thử lại"]]),
           """Đáp án câu ba. Sắp thứ tự khoá ngăn bế tắc từ gốc, nhưng phải biết trước mọi khoá cần lấy. Giới hạn chờ rồi thử lại đơn giản và bắt được mọi trường hợp, nhưng bế tắc vẫn xảy ra.
           Hệ thống thật thường dùng cả hai."""),
    ], checks=["3 * 2 * 1 == 6 == len(list(__import__('itertools').permutations('ABC')))", "sorted([9, 4]) == [4, 9]"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("giữ khoá, xin khoá khác", "hai phiên ngược thứ tự", "vòng tròn chờ = bế tắc", "luôn khoá theo thứ tự id tăng"),
           """Tổng kết chuỗi logic. Phiên giữ một khoá và xin khoá khác. Hai phiên ngược thứ tự thì tạo vòng tròn chờ, tức bế tắc. Luôn khoá theo thứ tự id tăng dần để chặn vòng tròn."""),
        st("""<div class='box key'><b>Tư duy:</b> bế tắc là lỗi <b>thiết kế thứ tự</b>, không phải lỗi may rủi.
Gặp bế tắc: rollback cả giao dịch, thử lại có giới hạn, và sửa thứ tự khoá.</div>""",
           """Điều cần mang theo. Bế tắc là lỗi thiết kế thứ tự, không phải lỗi may rủi. Gặp bế tắc thì rollback cả giao dịch, thử lại có giới hạn, và sửa thứ tự khoá."""),
    ])
    return lesson("L05", "plsql_khoa_hang_deadlock", "Bài 5 — PL/SQL, khoá hàng và bế tắc ORA-00060",
                  "curriculum/bnk.yaml L05; audit/bnk/verify_bnk.py L05; Oracle Database Concepts (Data Concurrency and Consistency: phát hiện bế tắc, rollback một câu lệnh; khoá bảng con khi khoá ngoại không có chỉ mục); Oracle Database Error Messages (ORA-00060); thứ tự khoá của ORDER BY … FOR UPDATE không được bảo đảm — Oracle không chạy trên máy này, chỉ mô phỏng logic thứ tự khoá",
                  ["Vẽ đồ thị chờ và nhận ra vòng tròn gây bế tắc", "Đếm số cặp thứ tự khoá gây bế tắc",
                   "Áp quy tắc khoá theo thứ tự id tăng dần", "Xử lý đúng khi gặp ORA-00060"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
