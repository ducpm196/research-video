from lib import *

NEED = "(lambda amt, day: amt > 10000000 or day + amt > 20000000)"


def build():
    hook = sc("hook", "hook", "Vì sao số thẻ phải được che, còn PIN không bao giờ xuất hiện nguyên văn?", [
        st("""<p>Một lập trình viên ghi nhật ký để gỡ lỗi: có cả số thẻ và PIN. Nhật ký được sao lưu, nhiều người đọc được, và <b>rò rỉ</b> chỉ cần một người xấu.</p>
<div class="box key">Bảo mật thanh toán dựa trên bốn ý: <b>che dữ liệu</b>, <b>không lộ khoá</b>, <b>phát hiện sửa bản tin</b>, <b>xác thực người dùng</b>.</div>""",
           """Chào bạn, một lập trình viên ghi nhật ký để gỡ lỗi, trong đó có cả số thẻ lẫn mã PIN. Nhật ký được sao lưu, nhiều người đọc được, và rò rỉ chỉ cần một người xấu.
           Bảo mật thanh toán dựa trên bốn ý. Che dữ liệu, không lộ khoá, phát hiện sửa bản tin, và xác thực người dùng."""),
        st(table(["ý", "công cụ", "bài này làm gì"],
                 [["che dữ liệu", "che số thẻ, không ghi PIN", "tự viết hàm che"],
                  ["không lộ khoá", "HSM giữ khoá, mã hoá khối PIN", "tính khối PIN"],
                  ["phát hiện sửa bản tin", "mã xác thực bản tin (MAC)", "đổi 1 chữ số, MAC đổi"],
                  ["xác thực người dùng", "sinh trắc học theo Quyết định 2345", "tính khi nào bắt buộc"]]),
           """Bảng này là kế hoạch bài học. Che dữ liệu bằng cách che số thẻ và không ghi PIN. Không lộ khoá nhờ thiết bị HSM giữ khoá và mã hoá khối PIN. Phát hiện sửa bản tin bằng mã xác thực bản tin.
           Xác thực người dùng bằng sinh trắc học theo Quyết định hai nghìn ba trăm bốn mươi lăm."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: những điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① PIN", "mã số bí mật vài chữ số khách gõ khi dùng thẻ", "1234 (số thử)"],
                  ["② Bit, hex, byte", "bit là chữ số 0 hoặc 1; một chữ số hex (thập lục phân, 0–9 rồi A–F) gồm 4 bit; một byte là 8 bit, viết bằng 2 chữ số hex", "F = 1111, byte 34 = 0011 0100"],
                  ["③ Mã hoá và khoá mật mã", "mã hoá biến dữ liệu rõ thành dãy không đọc được; chỉ ai có khoá (một chuỗi bí mật) mới giải ra được", "khoá K"]]),
           """Trước hết ta cần hiểu vài điều. PIN là mã số bí mật vài chữ số mà khách gõ khi dùng thẻ.
           Bit là chữ số không hoặc một. Một chữ số thập lục phân, từ không tới chín rồi A tới F, gồm bốn bit, và một byte là tám bit, viết bằng hai chữ số thập lục phân.
           Mã hoá là biến dữ liệu rõ thành một dãy không đọc được, và chỉ ai có khoá, tức một chuỗi bí mật, mới giải ra được. Chữ khoá ở bài này là khoá mật mã."""),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ XOR", "so từng bit: giống nhau cho 0, khác nhau cho 1; làm hai lần thì về ban đầu", "0111 XOR 0101 = 0010"],
                  ["⑤ Hàm băm", "biến dữ liệu thành dãy cố định; đổi một chút dữ liệu, dãy đổi hoàn toàn", "SHA-256"],
                  ["⑥ Khoá bí mật dùng chung", "khoá chỉ hai bên biết, dùng để chứng minh người gửi", "khoá K"]]),
           """Phép XOR so từng bit, giống nhau cho không, khác nhau cho một, và làm hai lần thì trở về ban đầu. Hàm băm biến dữ liệu thành một dãy cố định, đổi một chút dữ liệu thì dãy đổi hoàn toàn.
           Khoá bí mật dùng chung là khoá chỉ hai bên biết, dùng để chứng minh người gửi.""", clear=True),
        st("""$$0111 \\text{ XOR } 0101 = 0010$$""",
           """Một ví dụ XOR. Không một một một XOR không một không một bằng không không một không. Bit nào khác nhau thì thành một."""),
    ], checks=["0b0111 ^ 0b0101 == 0b0010", "(0b0111 ^ 0b0101) ^ 0b0101 == 0b0111"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["PAN", "số thẻ chính; nhạy cảm, phải che khi hiển thị và ghi nhật ký"],
                  ["khối PIN", "PIN được ghép với số thẻ theo một định dạng rồi mới mã hoá"],
                  ["HSM", "thiết bị phần cứng giữ khoá; khoá không bao giờ ra ngoài dạng rõ"],
                  ["MAC", "mã xác thực bản tin: sửa một ký tự thì MAC không còn khớp"],
                  ["Luhn", "phép kiểm số kiểm cuối của số thẻ, bắt lỗi gõ nhầm"]]),
           """Bảng này giải mã năm từ. PAN là số thẻ chính, nhạy cảm, phải che khi hiển thị và ghi nhật ký. Khối PIN là PIN được ghép với số thẻ theo một định dạng rồi mới mã hoá.
           HSM là thiết bị phần cứng giữ khoá, khoá không bao giờ ra ngoài ở dạng rõ. MAC là mã xác thực bản tin. Luhn là phép kiểm số cuối của số thẻ, bắt lỗi gõ nhầm."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: PIN đi từ bàn phím tới ngân hàng mà không lộ", [
        st(svg(1500, 400,
               box(30, 140, 240, 110, ["Người dùng", "gõ PIN"], C_BLUE, bold=True),
               box(330, 140, 300, 110, ["Thiết bị đầu cuối", "mã hoá ngay"], C_AMBER, bold=True),
               box(700, 140, 300, 110, ["HSM chặng giữa", "dịch TPK/ZPK → ZPK"], C_GRAY, size=22),
               box(1070, 140, 380, 110, ["HSM ngân hàng phát hành", "(ngân hàng đã cấp thẻ)", "kiểm PIN trong hộp kín"], C_GREEN, bold=True, size=22),
               arrow(270, 195, 325, 195), arrow(630, 195, 695, 195), arrow(1000, 195, 1065, 195),
               txt(750, 300, "Mỗi chặng chỉ DỊCH khối PIN sang khoá của chặng sau; PIN rõ không ra khỏi HSM", 24, "middle", "#1f2937", True),
               txt(750, 338, "TPK: khoá của thiết bị đầu cuối (máy rút tiền, máy quẹt thẻ); ZPK: khoá PIN dùng chung giữa hai chặng", 22, "middle", "#475569"),
               txt(750, 372, "Khoá làm việc được bọc bằng ZMK (khoá trao đổi) khi gửi, bằng LMK (khoá chủ của HSM) khi lưu", 22, "middle", "#475569")),
           """Hình cho thấy hành trình của mã PIN. Người dùng gõ PIN. Thiết bị đầu cuối, tức máy rút tiền hay máy quẹt thẻ, mã hoá ngay bằng khoá của thiết bị.
           Ngân hàng thanh toán là ngân hàng sở hữu máy quẹt thẻ mà khách vừa dùng.
           Ở mỗi chặng giữa, như ngân hàng thanh toán hay chuyển mạch, thiết bị HSM chỉ dịch khối PIN từ khoá của chặng trước sang khoá của chặng sau.
           PIN rõ không bao giờ ra khỏi HSM.
           Cuối cùng, HSM của ngân hàng phát hành, tức ngân hàng đã cấp thẻ, kiểm PIN trong hộp kín. Các khoá làm việc này được bọc bằng một khoá trao đổi khi gửi đi, và bằng khoá chủ của HSM khi lưu."""),
        st(svg(1500, 420,
               box(40, 40, 500, 70, "PIN 1234 → 04 1234 FFFFFFFFFF", C_BLUE, size=24),
               box(40, 130, 500, 70, "PAN → 0000 + 12 số 111111111111", C_AMBER, size=24),
               box(40, 230, 500, 70, "XOR từng bit hai dòng trên", C_PURPLE, size=24, bold=True),
               arrow(290, 300, 290, 335, "#475569"),
               box(40, 340, 500, 60, "0412 25EE EEEE EEEE", C_GREEN, size=26, bold=True),
               txt(1010, 130, "PIN không đi một mình:", 26, "middle", "#1f2937", True), txt(1010, 170, "luôn ghép với số thẻ trước khi mã hoá", 26, "middle", "#1f2937"),
               txt(1010, 240, "→ cùng PIN, khác thẻ → khối khác", 26, "middle", "#16a34a", True)),
           """Hình thứ hai cho thấy cách tạo khối PIN định dạng không. PIN được đệm thành mười sáu chữ số hex. Số thẻ được lấy mười hai chữ số rồi đệm bốn số không phía trước. Hai dòng XOR với nhau cho khối cuối.
           Nhờ ghép với số thẻ, cùng một PIN trên hai thẻ khác nhau cho hai khối khác nhau. Dữ liệu ở đây là số thử."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: khối PIN, MAC và quy tắc sinh trắc học", [
        st("""<p><b>Bước 1.</b> Khối PIN $= (\\text{PIN đệm}) \\text{ XOR } (\\text{PAN đệm})$. Vì XOR hai lần trả về ban đầu, bên có khoá và số thẻ khôi phục được PIN.</p>
<span class='note'>Làm thử: PIN thử 1234, thẻ thử 4111111111111111 → <code>041225EEEEEEEEEE</code>.</span>""",
           """Bước một, khối PIN bằng PIN đã đệm XOR với số thẻ đã đệm. Vì XOR hai lần trả về ban đầu, nên bên có khoá và số thẻ khôi phục được PIN. Làm thử, PIN thử một hai ba bốn với thẻ thử cho khối không bốn một hai hai năm rồi các chữ E."""),
        st("""<p><b>Bước 2.</b> MAC tính từ <b>khoá bí mật và nội dung</b>. Sửa một ký tự thì MAC mới khác MAC cũ, bên nhận phát hiện ngay.</p>
<span class='note'>Làm thử: tiền $500\\,000$ đổi thành $900\\,000$ → MAC khác.</span>""",
           """Bước hai, vì MAC được tính từ khoá bí mật và nội dung, nên sửa một ký tự thì MAC mới khác MAC cũ, và bên nhận phát hiện ngay. Làm thử, đổi tiền từ năm trăm nghìn thành chín trăm nghìn thì MAC khác hẳn."""),
        st("""<p><b>Bước 3.</b> Theo Quyết định 2345/QĐ-NHNN của Ngân hàng Nhà nước (ký 18/12/2023, hiệu lực 01/07/2024), chuyển tiền trực tuyến <b>trên $10$ triệu đồng</b> một giao dịch, hoặc khi <b>tổng trong ngày vượt $20$ triệu đồng</b>, phải xác thực sinh trắc học.</p>
<span class='note'>Làm thử: $15$ triệu → cần. $5$ triệu, ngày chưa có gì → không.</span>""",
           """Bước ba nói về Quyết định hai nghìn ba trăm bốn mươi lăm của Ngân hàng Nhà nước, ký ngày mười tám tháng mười hai năm hai nghìn không trăm hai mươi ba.
           Quyết định này có hiệu lực từ ngày một tháng bảy năm hai nghìn không trăm hai mươi tư.
           Theo quyết định này, chuyển tiền trực tuyến phải xác thực sinh trắc học khi một giao dịch trên mười triệu đồng.
           Khi tổng trong ngày vượt hai mươi triệu đồng cũng phải xác thực. Làm thử, mười lăm triệu thì cần, năm triệu khi ngày chưa có giao dịch nào thì không."""),
    ], checks=["alg.bnk_pin_block0('1234', '4111111111111111') == '041225EEEEEEEEEE'", "alg.bnk_mac('k', 'amt=500000') != alg.bnk_mac('k', 'amt=900000')",
               NEED + "(15000000, 0) and not " + NEED + "(5000000, 0)"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>PIN thử <code>1234</code> đệm thành <code>041234FFFFFFFFFF</code> (0: mã định dạng 0; 4: PIN dài 4 chữ số; F lấp cho đủ 16 chữ số). Thẻ thử <code>4111111111111111</code>: bỏ số kiểm cuối, lấy $12$ số cuối còn lại rồi đệm.</p>
$$① \\; \\text{PAN đệm} = \\mathtt{0000\\,111111111111}$$""",
           """Ta tính một khối PIN với dữ liệu thử. PIN một hai ba bốn được đệm thành không bốn một hai ba bốn rồi các chữ F. Chữ số không đầu là mã định dạng, chữ số bốn là độ dài của PIN, còn chữ F lấp cho đủ mười sáu chữ số. Thẻ thử, bỏ số kiểm cuối, lấy mười hai số cuối còn lại rồi đệm bốn số không phía trước. Phép tính thứ nhất ra dãy PAN đã đệm."""),
        st("""<p>Hai byte đầu: $\\mathtt{04}\\ \\text{ XOR }\\ \\mathtt{00} = \\mathtt{04}$ và $\\mathtt{12}\\ \\text{ XOR }\\ \\mathtt{00} = \\mathtt{12}$.</p>
$$② \\; \\mathtt{34} \\text{ XOR } \\mathtt{11} = \\hl{\\mathtt{25}}$$""",
           """Phép tính thứ hai, hai byte đầu XOR với không nên giữ nguyên là không bốn và một hai. Byte tiếp theo, ba bốn XOR một một, cho hai năm."""),
        st("""$$③ \\; \\mathtt{FF} \\text{ XOR } \\mathtt{11} = \\hl{\\mathtt{EE}}\\quad \\text{(lặp 5 lần)}$$""",
           """Phép tính thứ ba, F F XOR một một cho E E, và lặp lại năm lần ở các byte còn lại.""", clear=True),
        st("""<p>Ghép lại: $\\mathtt{04}\\ \\mathtt{12}\\ \\mathtt{25}\\ \\mathtt{EE}\\ \\mathtt{EE}\\ \\mathtt{EE}\\ \\mathtt{EE}\\ \\mathtt{EE}$.</p>
$$④ \\; \\text{khối PIN} = \\hlg{\\mathtt{041225EEEEEEEEEE}}$$""",
           """Phép tính thứ tư, ghép lại, khối PIN là không bốn một hai hai năm rồi năm cặp E E."""),
        st("""<p>Quy tắc sinh trắc học (minh hoạ ranh giới). Ba giao dịch trong ngày: $8$, $8$, $8$ triệu.</p>
$$⑤ \\; 8 + 8 = 16 \\le 20\\ \\text{(không)},\\quad 16 + 8 = 24 > 20\\ \\Rightarrow\\ \\hl{\\text{giao dịch thứ 3 cần}}$$""",
           """Phép tính thứ năm, ba giao dịch trong ngày, mỗi giao dịch tám triệu. Giao dịch thứ hai, cộng dồn mười sáu triệu, chưa vượt hai mươi. Giao dịch thứ ba, cộng dồn hai mươi bốn triệu, vượt hai mươi, nên giao dịch thứ ba cần sinh trắc học."""),
    ], checks=["0x34 ^ 0x11 == 0x25", "0xFF ^ 0x11 == 0xEE", "alg.bnk_pin_block0('1234', '4111111111111111') == '0412' + '25' + 'EE' * 5",
               "('0' + str(len('1234')) + '1234').ljust(16, 'F') == '041234FFFFFFFFFF' and len('041234FFFFFFFFFF') == 16",
               "not " + NEED + "(8000000, 8000000) and " + NEED + "(8000000, 16000000)", "8 + 8 == 16 <= 20 < 16 + 8"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: Luhn, che số thẻ và MAC", [
        st("""<p>Đường khác cho ba việc: (a) số thẻ thử qua phép kiểm <b>Luhn</b>; (b) che thẻ giữ $6$ số đầu và $4$ số cuối; (c) đổi một chữ số trong bản tin thì <b>MAC khác</b>.</p>
$$\\text{(b)}\\ \\mathtt{411111}\\,******\\,\\mathtt{1111}$$
<p class="small">(a) Luhn: từ phải sang, nhân đôi mỗi chữ số thứ hai (quá 9 thì trừ 9), cộng tất cả; tổng chia hết cho 10 là hợp lệ. Thẻ thử: tám chữ số 1 giữ nguyên cho $8$, bảy chữ số 1 nhân đôi cho $14$, chữ số 4 nhân đôi cho $8$: $8 + 14 + 8 = 30$ ✓.</p>""",
           """Kiểm bằng đường khác cho ba việc. Một, số thẻ thử qua phép kiểm Luhn. Hai, che thẻ, giữ sáu số đầu và bốn số cuối. Ba, đổi một chữ số trong bản tin thì MAC khác.
           Phép kiểm số kiểm cuối làm thế này. Đi từ phải sang, nhân đôi mỗi chữ số thứ hai, nếu quá chín thì trừ chín, rồi cộng tất cả, và tổng chia hết cho mười là hợp lệ.
           Với thẻ thử, tám chữ số một giữ nguyên cho tám, bảy chữ số một nhân đôi cho mười bốn, chữ số bốn nhân đôi cho tám. Tổng là ba mươi, chia hết cho mười.
           Vì mỗi việc đều tính bằng chương trình, nên kết quả đáng tin hơn tính tay.""", clear=True),
        st(table(["bản tin", "MAC (16 ký tự đầu, khoá thử)", "bên nhận kết luận"],
                 [["amt=500000", "7625fd27947ee367", "nguyên vẹn"], ["amt=900000", "7958d294fb89b6dc", "bị sửa, từ chối"]]),
           """Bảng này cho thấy hai bản tin chỉ khác nhau ở số tiền nhưng MAC hoàn toàn khác. Vì bên nhận tính lại MAC từ khoá và nội dung, nên bản tin bị sửa không khớp và bị từ chối. Lưu ý đây là minh hoạ, chuẩn thẻ dùng thuật toán MAC riêng."""),
    ], checks=["alg.bnk_luhn('4111111111111111') and not alg.bnk_luhn('4111111111111112')",
               "sum((lambda d: d - 9 if d > 9 else d)(int(c) * (2 if i % 2 else 1)) for i, c in enumerate(reversed('4111111111111111'))) == 30 == 8 + 14 + 8", "(lambda p: p[:6] + '*' * (len(p) - 10) + p[-4:])('4111111111111111') == '411111******1111'",
               "alg.bnk_mac('k', 'amt=500000')[:16] == '7625fd27947ee367' and alg.bnk_mac('k', 'amt=900000')[:16] == '7958d294fb89b6dc'"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ “mã hoá” là đủ nên ghi cả PIN mã hoá vào nhật ký. PIN, kể cả đã mã hoá, <b class="red">không được lưu</b> sau khi xử lý xong.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ mã hoá là đủ nên ghi cả PIN đã mã hoá vào nhật ký. PIN, kể cả đã mã hoá, không được lưu sau khi xử lý xong."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Để khoá trong mã nguồn hay tệp cấu hình</b>. Ai đọc được kho mã là có khoá. Khoá phải nằm trong HSM hoặc kho khoá chuyên dụng, và xoay vòng định kỳ.</div>""",
           """Lỗi thứ hai, của người đã đi làm, là để khoá trong mã nguồn hay tệp cấu hình. Ai đọc được kho mã là có khoá. Khoá phải nằm trong HSM hoặc kho khoá chuyên dụng, và được xoay vòng định kỳ."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Chỉ kiểm sinh trắc học ở <b>ứng dụng</b>. Kẻ tấn công gọi thẳng API sẽ bỏ qua. Máy chủ phải kiểm lại điều kiện cho mọi giao dịch, không tin cờ (giá trị báo “đã xác thực”) do ứng dụng gửi lên.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là chỉ kiểm sinh trắc học ở ứng dụng. Kẻ tấn công gọi thẳng giao diện lập trình sẽ bỏ qua. Máy chủ phải kiểm lại điều kiện cho mọi giao dịch, không tin cờ, tức giá trị báo đã xác thực, do ứng dụng gửi lên."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Khách chuyển 12 triệu một lần, ngày chưa có giao dịch nào. Có cần sinh trắc học?"],
                  ["2", "Khách chuyển 6 triệu rồi 7 triệu rồi 9 triệu. Giao dịch nào đầu tiên cần?"],
                  ["3", "Quyết định: ghi số thẻ nguyên vào nhật ký để gỡ lỗi nhanh?"]]),
           """Đến lượt bạn. Câu một, khách chuyển mười hai triệu một lần, ngày chưa có giao dịch nào, có cần sinh trắc học không? Câu hai, khách chuyển sáu triệu, rồi bảy triệu, rồi chín triệu, giao dịch nào đầu tiên cần?
           Câu ba, có nên ghi số thẻ nguyên vào nhật ký để gỡ lỗi nhanh không? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $12 > 10$ triệu một giao dịch.</p>
$$\\hl{\\text{cần}}$$""",
           """Đáp án câu một. Mười hai triệu lớn hơn mười triệu cho một giao dịch, nên cần."""),
        st("""<p>Câu 2: cộng dồn $6 \\to 6 + 7 = 13 \\to 13 + 9 = 22$. Mỗi giao dịch riêng đều dưới $10$ triệu; chỉ cộng dồn $22 > 20$.</p>
$$\\hl{\\text{giao dịch thứ 3}}$$""",
           """Đáp án câu hai. Cộng dồn sáu, rồi mười ba, rồi hai mươi hai. Mỗi giao dịch riêng đều dưới mười triệu, nhưng cộng dồn hai mươi hai vượt hai mươi, nên giao dịch thứ ba cần."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["ghi nguyên số thẻ", "gỡ lỗi nhanh", "rò rỉ dữ liệu thẻ, vi phạm yêu cầu bảo mật"],
                  ["che số thẻ, ghi mã vết", "vẫn tra soát được, an toàn", "thêm một bước tra cứu"]]),
           """Đáp án câu ba. Không ghi nguyên số thẻ. Hãy che số thẻ và ghi mã vết để tra soát, an toàn hơn dù thêm một bước tra cứu."""),
    ], checks=[NEED + "(12000000, 0)", "not " + NEED + "(7000000, 6000000) and not " + NEED + "(6000000, 0) and " + NEED + "(9000000, 13000000)"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("che dữ liệu nhạy cảm", "khoá nằm trong HSM", "MAC phát hiện sửa", "máy chủ tự kiểm điều kiện"),
           """Tổng kết chuỗi logic. Che dữ liệu nhạy cảm. Khoá nằm trong thiết bị HSM. MAC phát hiện bản tin bị sửa. Và máy chủ luôn tự kiểm điều kiện, không tin ứng dụng."""),
        st("""<div class='box key'><b>Tư duy:</b> giả định kẻ xấu đứng ở <b>mọi chỗ ở giữa</b>, kể cả trong nhật ký và trong ứng dụng. Mỗi lớp bảo vệ phải đứng được một mình.</div>""",
           """Điều cần mang theo. Hãy giả định kẻ xấu đứng ở mọi chỗ ở giữa, kể cả trong nhật ký và trong ứng dụng. Mỗi lớp bảo vệ phải đứng được một mình."""),
    ])
    return lesson("L13", "bao_mat_thanh_toan_pin_hsm", "Bài 13 — Bảo mật thanh toán: khối PIN, HSM, MAC và sinh trắc học",
                  "curriculum/bnk.yaml L13; audit/bnk/verify_bnk.py L13; ISO 9564-1 (khối PIN định dạng 0); Quyết định 2345/QĐ-NHNN (CITED qua tìm kiếm web 2026-11-07, luatvietnam.vn và tapchicongthuong.vn, no revision given; ngưỡng 'trên 10 triệu/giao dịch' và 'tổng ngày vượt 20 triệu', ký 18/12/2023, hiệu lực 01/07/2024 — theo rà soát 2026-11-08, chưa đối chiếu bản PDF gốc); PCI DSS v4.0.1 Req. 3.3.1.2 (không lưu PIN / khối PIN sau cấp phép) và 3.4.1 (che PAN khi hiển thị); ISO/IEC 7812-1 (số kiểm Luhn); Thales payShield Host Command Reference (dịch khối PIN TPK/ZPK→ZPK; khoá bọc bằng ZMK/LMK); dữ liệu thẻ và PIN trong bài là dữ liệu thử",
                  ["Tính khối PIN định dạng 0 từ PIN thử và số thẻ thử", "Giải thích vì sao sửa bản tin làm MAC không khớp",
                   "Áp quy tắc sinh trắc học theo giao dịch và cộng dồn trong ngày", "Che số thẻ và không ghi PIN vào nhật ký"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
