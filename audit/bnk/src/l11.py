from lib import *

MSG = "02007020000000000000164111111111111111000000000000500000123456"


def build():
    hook = sc("hook", "hook", "Vì sao một chuỗi ký tự vô nghĩa lại là một lệnh chuyển tiền?", [
        st("""<p>Một bản tin ISO 8583 trông như dãy số dài:</p>
<p><code>0200 7020000000000000 16 4111111111111111 000000 000000500000 123456</code></p>
<div class="box key">Bên nhận biết trường nào ở đâu nhờ <b>bản đồ bit</b> nằm ngay sau mã loại bản tin.</div>""",
           """Chào bạn, một bản tin ISO tám nghìn năm trăm tám mươi ba trông như một dãy số dài vô nghĩa. Nhưng bên nhận đọc ra được số thẻ, số tiền, mã vết, nhờ bản đồ bit nằm ngay sau mã loại bản tin.
           Hôm nay ta dựng một bản tin từ đầu, rồi đọc ngược lại."""),
        st(table(["ý hỏi", "bài này trả lời"],
                 [["làm sao biết bản tin có những trường nào", "bản đồ 64 bit, bit nào bật thì trường đó có mặt"],
                  ["làm sao biết mỗi trường dài bao nhiêu", "trường cố định thì biết trước, trường đổi độ dài thì có số báo độ dài đứng trước"]]),
           """Hôm nay ta trả lời hai câu. Làm sao biết bản tin có những trường nào, nhờ bản đồ sáu mươi bốn bit. Làm sao biết mỗi trường dài bao nhiêu, nhờ độ dài cố định hoặc số báo độ dài đứng trước.
           Lưu ý, mỗi mạng thanh toán có đặc tả riêng, kể cả NAPAS. Bài này dạy nguyên lý chung, không phải đặc tả kết nối của riêng mạng nào."""),
    ])
    pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Nhị phân", "chỉ có hai chữ số 0 và 1, mỗi chữ số là một bit", "0111 = 7"],
                  ["② Thập lục phân", "16 chữ số: 0–9 rồi A–F; một chữ số hex = 4 bit", "7 = 0111, 2 = 0010, A = 1010"],
                  ["③ Lũy thừa của hai", "bit thứ k từ phải sang trái (đếm từ 0) có giá trị 2 mũ k", "2 mũ 3 = 8"]]),
           """Ôn ba điều. Nhị phân chỉ có hai chữ số không và một, mỗi chữ số là một bit. Thập lục phân có mười sáu chữ số, từ không tới chín rồi A tới F, và mỗi chữ số tương ứng bốn bit.
           Còn bit thứ k từ phải sang, đếm từ không, có giá trị hai mũ k."""),
        st("""$$0111_2 = 0 \\cdot 8 + 1 \\cdot 4 + 1 \\cdot 2 + 1 \\cdot 1 = 7$$""",
           """Một ví dụ số. Chuỗi bit không một một một bằng không nhân tám, cộng một nhân bốn, cộng một nhân hai, cộng một nhân một, bằng bảy. Đó cũng là chữ số hex bảy."""),
    ], checks=["0 * 8 + 1 * 4 + 1 * 2 + 1 * 1 == 7 == int('0111', 2)", "format(7, '04b') == '0111' and format(2, '04b') == '0010'"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["MTI", "Message Type Identifier, 4 chữ số: 0200 là yêu cầu tài chính, 0210 là phản hồi"],
                  ["bản đồ bit (bitmap)", "64 bit; bit thứ i bật (bằng 1) thì trường i có; bit 1 bật nghĩa là có bản đồ thứ hai (trường 65–128). Nhiều mạng gửi dạng nhị phân 8 byte, không phải 16 ký tự hex"],
                  ["DE (data element)", "một trường dữ liệu, đánh số 2, 3, 4, …"],
                  ["LLVAR", "trường có độ dài thay đổi: 2 chữ số báo độ dài rồi tới nội dung"],
                  ["STAN / RRN", "DE 11 mã vết 6 số / DE 37 mã tham chiếu 12 ký tự"]]),
           """Bảng này giải mã năm từ. MTI là mã loại bản tin gồm bốn chữ số, không hai không không là yêu cầu tài chính, không hai một không là phản hồi. Bản đồ bit có sáu mươi bốn bit, bit thứ i bật thì trường i có mặt.
           Riêng bit một bật nghĩa là còn bản đồ thứ hai, cho các trường sáu mươi lăm tới một trăm hai mươi tám. Nhiều mạng gửi bản đồ ở dạng nhị phân tám byte, chứ không phải mười sáu ký tự.
           D E là một trường dữ liệu, đánh số hai, ba, bốn. Còn trường độ dài thay đổi có hai chữ số báo độ dài rồi tới nội dung. Cuối cùng, STAN là trường mười một, RRN là trường ba mươi bảy."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: bản tin gồm những khúc nào", [
        st(svg(1500, 380,
               box(30, 130, 150, 110, ["MTI", "0200"], C_PURPLE, bold=True, size=22),
               box(190, 130, 330, 110, ["bản đồ bit", "7020000000000000"], C_AMBER, bold=True, size=22),
               box(530, 130, 270, 110, ["DE 2 (PAN)", "16 + 4111…1111"], C_BLUE, bold=True, size=20),
               box(810, 130, 190, 110, ["DE 3", "000000"], C_BLUE, bold=True, size=20),
               box(1010, 130, 250, 110, ["DE 4 (tiền)", "000000500000"], C_BLUE, bold=True, size=18),
               box(1270, 130, 200, 110, ["DE 11", "123456"], C_BLUE, bold=True, size=20),
               txt(750, 60, "mỗi khúc nối liền nhau, không có dấu phân cách", 28, "middle", "#1f2937", True),
               txt(750, 320, "đọc theo thứ tự: MTI → bản đồ bit → các trường theo số tăng dần", 26, "middle", "#475569")),
           """Hình cho thấy một bản tin gồm các khúc nối liền nhau, không có dấu phân cách. Đầu tiên là mã loại bản tin. Rồi tới bản đồ bit.
           Sau đó là các trường theo số tăng dần, ở đây là trường hai số thẻ, trường ba mã xử lý, trường bốn số tiền, và trường mười một mã vết."""),
        st(svg(1500, 420,
               txt(60, 50, "Vị trí bit:", 24, "start", "#475569"),
               *[box(40 + i * 90, 70, 80, 60, str(b), C_GREEN if b else C_GRAY, size=26) for i, b in enumerate([0, 1, 1, 1, 0, 0, 0, 0])],
               *[txt(80 + i * 90, 160, str(i + 1), 22, "middle", "#475569") for i in range(8)],
               box(800, 70, 320, 60, "0111 0000 = 0x70", C_AMBER, size=26),
               *[box(40 + i * 90, 220, 80, 60, str(b), C_GREEN if b else C_GRAY, size=26) for i, b in enumerate([0, 0, 1, 0, 0, 0, 0, 0])],
               *[txt(80 + i * 90, 310, str(i + 9), 22, "middle", "#475569") for i in range(8)],
               box(800, 220, 320, 60, "0010 0000 = 0x20", C_AMBER, size=26),
               txt(750, 380, "bit 2, 3, 4 và 11 bật → trường 2, 3, 4 và 11 có mặt", 26, "middle", "#1f2937", True)),
           """Hình này giải mã bản đồ bit. Hàng trên là tám bit đầu, vị trí một tới tám. Các bit hai, ba và bốn bật, nên tám bit đó là không một một một, không không không không, tức hex bảy không.
           Hàng dưới là tám bit tiếp theo, vị trí chín tới mười sáu. Chỉ bit mười một bật, nên là không không một không, không không không không, tức hex hai không."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: dựng và đọc bản đồ bit", [
        st("""<p><b>Bước 1.</b> Bản đồ có $64$ bit. Bit của trường $i$ nằm ở vị trí $i$ tính từ trái, nên có giá trị $2^{64 - i}$.</p>
<span class='note'>Làm thử: trường $2$ cho $2^{62}$, trường $3$ cho $2^{61}$, trường $4$ cho $2^{60}$, trường $11$ cho $2^{53}$.</span>""",
           """Bước một, vì bản đồ có sáu mươi bốn bit và bit của trường i nằm ở vị trí i tính từ trái, nên nó có giá trị hai mũ sáu mươi bốn trừ i. Làm thử, trường hai cho hai mũ sáu mươi hai, trường ba cho hai mũ sáu mươi mốt, trường bốn cho hai mũ sáu mươi, trường mười một cho hai mũ năm mươi ba."""),
        st("""<p><b>Bước 2.</b> Cộng các giá trị rồi đổi sang hex: byte đầu <b>0x70</b> (bit 2, 3, 4), byte tiếp <b>0x20</b> (bit 11), các byte còn lại bằng $0$.</p>
<span class='note'>Làm thử: bản đồ = <code>7020000000000000</code>, đủ 16 chữ số hex.</span>""",
           """Bước hai, vì mỗi chữ số hex tương ứng bốn bit, nên ta đổi từng nhóm. Byte đầu là bảy không từ các bit hai, ba, bốn. Byte thứ hai là hai không từ bit mười một. Các byte còn lại bằng không. Làm thử, bản đồ là bảy không hai không rồi mười hai chữ số không, đủ mười sáu chữ số hex."""),
        st("""<p><b>Bước 3.</b> Đọc ngược: duyệt trường $2..64$, bit nào bật thì đọc trường đó. Trường cố định đọc đúng số ký tự; <b>LLVAR</b> đọc $2$ chữ số độ dài rồi đọc đúng ngần ấy ký tự.</p>
<span class='note'>Làm thử: sau bản đồ đọc “16” rồi lấy tiếp 16 ký tự làm số thẻ. Bắt đầu từ trường 2 vì bit 1 chỉ báo bản đồ thứ hai.</span>""",
           """Bước ba, vì ta biết trường nào có mặt, nên đọc ngược bằng cách duyệt các trường từ trường hai, bit nào bật thì đọc trường đó. Bit một không phải trường dữ liệu, nó chỉ báo có bản đồ thứ hai hay không. Trường cố định đọc đúng số ký tự đã biết. Trường đổi độ dài thì đọc hai chữ số báo độ dài, rồi đọc đúng ngần ấy ký tự.
           Làm thử, sau bản đồ đọc mười sáu, rồi lấy tiếp mười sáu ký tự làm số thẻ."""),
    ], checks=["2 ** 62 + 2 ** 61 + 2 ** 60 + 2 ** 53 == 0x7020000000000000", "format(2 ** 62 + 2 ** 61 + 2 ** 60 + 2 ** 53, '016X') == '7020000000000000'",
               "alg.bnk_iso_unpack(alg.bnk_iso_pack('0200', {2: '4111111111111111', 3: '000000', 4: '000000500000', 11: '123456'}))[1][2] == '4111111111111111'"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Dựng bản tin <code>0200</code> với trường $2$ (số thẻ thử), $3$, $4$ ($500\\,000$ đồng), $11$. Số thẻ <code>4111111111111111</code> là số thử, không phải thẻ thật.</p>
$$① \\; \\text{bản đồ} = 2^{62} + 2^{61} + 2^{60} + 2^{53} = \\hl{\\mathtt{7020000000000000}}$$""",
           """Ta dựng một bản tin. Mã không hai không không, trường hai là số thẻ thử, trường ba, trường bốn là năm trăm nghìn đồng, và trường mười một. Số thẻ này là số thử, không phải thẻ thật.
           Phép tính thứ nhất, bản đồ bằng tổng bốn lũy thừa của hai, là hai mũ sáu mươi hai, sáu mươi mốt, sáu mươi và năm mươi ba. Kết quả là bảy không hai không, rồi các chữ số không."""),
        st("""<p>Trường $2$ là LLVAR: $16$ ký tự nên báo <code>16</code>.</p>
$$② \\; \\text{độ dài trường 2} = 2 + 16 = \\hl{18}\\ \\text{ký tự}$$""",
           """Phép tính thứ hai, trường hai là loại độ dài thay đổi. Số thẻ có mười sáu ký tự nên số báo độ dài là mười sáu. Cả trường chiếm hai cộng mười sáu, bằng mười tám ký tự."""),
        st("""<p>Trường $4$ có $12$ chữ số, số tiền $500\\,000$ đồng viết thành <code>000000500000</code>. Với tiền đồng, đơn vị nhỏ nhất là $1$ đồng.</p>
$$③ \\; \\text{độ dài trường 4} = \\hl{12}\\ \\text{ký tự}$$""",
           """Phép tính thứ ba, trường bốn có mười hai chữ số, năm trăm nghìn đồng viết thành sáu chữ số không rồi năm trăm nghìn. Với đồng Việt Nam, đơn vị nhỏ nhất là một đồng. Độ dài trường bốn là mười hai ký tự.""", clear=True),
        st("""<p>Cộng độ dài các khúc: MTI $4$, bản đồ $16$, trường $2$: $18$, trường $3$: $6$, trường $4$: $12$, trường $11$: $6$.</p>
$$④ \\; 4 + 16 + 18 + 6 + 12 + 6 = \\hlg{62}\\ \\text{ký tự}$$""",
           """Phép tính thứ tư, cộng độ dài các khúc. Mã loại bản tin bốn, bản đồ mười sáu, trường hai mười tám, trường ba sáu, trường bốn mười hai, trường mười một sáu. Tổng là sáu mươi hai ký tự."""),
        st("""<p>Đọc ngược bản tin $62$ ký tự: bản đồ cho biết có trường $2, 3, 4, 11$; đọc theo thứ tự ra lại đúng số thẻ, mã xử lý, số tiền và mã vết.</p>
$$⑤ \\; \\text{số tiền đọc lại} = \\hlg{500\\,000}\\ \\text{đồng}$$""",
           """Phép tính thứ năm, đọc ngược bản tin sáu mươi hai ký tự. Bản đồ cho biết có bốn trường. Đọc theo thứ tự thì ra lại đúng số thẻ, mã xử lý, số tiền và mã vết. Số tiền đọc lại là năm trăm nghìn đồng."""),
    ], checks=["alg.bnk_iso_pack('0200', {2: '4111111111111111', 3: '000000', 4: '000000500000', 11: '123456'}) == '" + MSG + "'",
               "2 + 16 == 18", "len('000000500000') == 12", "4 + 16 + 18 + 6 + 12 + 6 == 62 == len('" + MSG + "')",
               "int(alg.bnk_iso_unpack('" + MSG + "')[1][4]) == 500000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: vòng đi vòng về", [
        st("""<p>Đường khác: không tin phép tính tay. Đóng gói rồi <b>đọc ngược</b> bằng chương trình, và so với dữ liệu ban đầu.</p>
$$\\text{đóng gói} \\to \\text{đọc ngược} = \\text{dữ liệu ban đầu}\\quad \\hlg{\\text{khớp}}$$""",
           """Kiểm bằng đường khác. Vì không nên chỉ tin phép tính tay, ta đóng gói rồi đọc ngược bằng chương trình, và so với dữ liệu ban đầu. Kết quả khớp từng trường."""),
        st(table(["trường", "tên", "kiểu", "ví dụ"],
                 [["2", "số thẻ (PAN)", "LLVAR, tối đa 19", "4111111111111111"], ["3", "mã xử lý", "6 chữ số", "000000"], ["4", "số tiền", "12 chữ số", "000000500000"],
                  ["11", "mã vết (STAN)", "6 chữ số", "123456"], ["39", "mã trả lời", "2 ký tự", "00 = chấp nhận"]]),
           """Bảng này liệt kê vài trường hay gặp. Trường hai là số thẻ, độ dài thay đổi. Trường ba là mã xử lý, trường bốn là số tiền, trường mười một là mã vết. Trường ba mươi chín là mã trả lời, không không nghĩa là chấp nhận."""),
    ], checks=["alg.bnk_iso_unpack(alg.bnk_iso_pack('0210', {3: '000000', 4: '000000500000', 11: '123456', 39: '00'})) == ('0210', {3: '000000', 4: '000000500000', 11: '123456', 39: '00'})",
               "alg.bnk_iso_pack('0210', {3: '000000', 4: '000000500000', 11: '123456', 39: '00'})[4:20] == '3020000002000000'"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Đọc <code>000000500000</code> thành “500 nghìn” mà quên <b>đơn vị nhỏ nhất theo loại tiền</b>. Với đồng là một đồng, nhưng loại tiền có số lẻ thì cùng dãy số có nghĩa khác.</div>""",
           """Lỗi thứ nhất, của người mới. Đọc dãy sáu chữ số không rồi năm trăm nghìn thành năm trăm nghìn mà quên đơn vị nhỏ nhất theo loại tiền. Với đồng là một đồng, nhưng loại tiền có số lẻ thì cùng dãy số có nghĩa khác."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Ghi nguyên số thẻ vào nhật ký</b> khi gỡ lỗi. Số thẻ là dữ liệu nhạy cảm; nhật ký phải che, ví dụ 6 số đầu và 4 số cuối.</div>""",
           """Lỗi thứ hai, của người đã đi làm, là ghi nguyên số thẻ vào nhật ký khi gỡ lỗi. Số thẻ là dữ liệu nhạy cảm, nên nhật ký phải che, ví dụ chỉ giữ sáu số đầu và bốn số cuối."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Coi mọi đối tác dùng cùng một bảng trường. Cùng ISO 8583 nhưng <b class="red">mỗi mạng có đặc tả riêng</b>: trường nào dùng, độ dài, bảng mã ký tự. Luôn đọc đặc tả kết nối chính thức.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là coi mọi đối tác dùng cùng một bảng trường. Cùng chuẩn nhưng mỗi mạng có đặc tả riêng, gồm trường nào dùng, độ dài, bảng mã ký tự. Luôn đọc đặc tả kết nối chính thức."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bản tin chỉ có trường 3, 4, 11. Bản đồ bit là gì?"],
                  ["2", "Tổng độ dài bản tin MTI 0200 đó (trường 3: 6, trường 4: 12, trường 11: 6)?"],
                  ["3", "Quyết định: gỡ lỗi cần xem số thẻ, có ghi nguyên vào nhật ký không?"]]),
           """Đến lượt bạn. Câu một, bản tin chỉ có trường ba, bốn và mười một, bản đồ bit là gì? Câu hai, tổng độ dài bản tin đó là bao nhiêu, biết trường ba dài sáu, trường bốn mười hai, trường mười một sáu?
           Câu ba, khi gỡ lỗi cần xem số thẻ, có ghi nguyên vào nhật ký không? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $2^{61} + 2^{60} + 2^{53}$. Byte đầu: bit $3, 4$ → $0011\\,0000 = 0x30$. Byte hai: bit $11$ → $0x20$.</p>
$$\\hl{\\mathtt{3020000000000000}}$$""",
           """Đáp án câu một. Hai mũ sáu mươi mốt, cộng hai mũ sáu mươi, cộng hai mũ năm mươi ba. Byte đầu có bit ba và bốn bật, nên là không không một một, không không không không, tức ba không. Byte hai có bit mười một bật, tức hai không."""),
        st("""$$4 + 16 + 6 + 12 + 6 = \\hlg{44}\\ \\text{ký tự}$$""",
           """Đáp án câu hai. Mã loại bản tin bốn, bản đồ mười sáu, rồi sáu, mười hai, sáu. Tổng là bốn mươi bốn ký tự."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["ghi nguyên số thẻ", "gỡ lỗi nhanh", "rò rỉ dữ liệu thẻ, vi phạm yêu cầu bảo mật"],
                  ["che số thẻ (6 đầu + 4 cuối), giữ mã vết", "vẫn tra soát được qua mã vết", "khó tìm hơn một chút"]]),
           """Đáp án câu ba. Không ghi nguyên số thẻ. Hãy che, chỉ giữ sáu số đầu và bốn số cuối, và dùng mã vết để tra soát. Ghi nguyên thì gỡ lỗi nhanh nhưng rò rỉ dữ liệu thẻ."""),
    ], checks=["format(2 ** 61 + 2 ** 60 + 2 ** 53, '016X') == '3020000000000000'",
               "alg.bnk_iso_pack('0200', {3: '000000', 4: '000000500000', 11: '123456'})[4:20] == '3020000000000000'",
               "4 + 16 + 6 + 12 + 6 == 44 == len(alg.bnk_iso_pack('0200', {3: '000000', 4: '000000500000', 11: '123456'}))"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("MTI", "bản đồ 64 bit", "bit i bật → trường i có", "cố định hoặc LLVAR", "đọc ngược khớp"),
           """Tổng kết chuỗi logic. Mã loại bản tin, rồi bản đồ sáu mươi bốn bit. Bit i bật nghĩa là trường i có mặt. Trường cố định hoặc có độ dài báo trước, và đọc ngược phải khớp."""),
        st("""<div class='box key'><b>Tư duy:</b> bản tin nhị phân hay chữ đều là <b>hợp đồng giữa hai bên</b>. Luôn dựng rồi đọc ngược để kiểm, và đọc kỹ đặc tả của đối tác.</div>""",
           """Điều cần mang theo. Bản tin là hợp đồng giữa hai bên. Luôn dựng rồi đọc ngược để kiểm, và đọc kỹ đặc tả của đối tác."""),
    ])
    return lesson("L11", "iso_8583_ban_do_bit", "Bài 11 — ISO 8583: bản đồ bit và cấu trúc bản tin",
                  "curriculum/bnk.yaml L11; audit/bnk/verify_bnk.py L11; ISO 8583:1987 (định nghĩa trường 2, 3, 4, 7, 11, 12, 13, 37, 39, 41, 49), ISO 4217 (đơn vị nhỏ nhất của VND là 0); đặc tả của từng mạng, kể cả NAPAS, có thể khác",
                  ["Dựng bản đồ bit từ danh sách trường có mặt", "Tính độ dài một bản tin gồm trường cố định và trường LLVAR",
                   "Đọc ngược một bản tin thành các trường", "Che số thẻ khi ghi nhật ký"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
