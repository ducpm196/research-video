from lib import *
from labkit import write_lab, practice_steps, practice_scene

NEED = "(lambda amt, day: amt > 10000000 or day + amt > 20000000)"


def build():
    pin_block = prog("KhoiPin", """
pin, pan = "1234", "4111111111111111"
a = "041234FFFFFFFFFF"                        # PIN đã đệm: 0, độ dài 4, PIN, rồi chữ F
b = "0000" + pan[-13:-1]                      # 12 số cuối của thẻ (bỏ số kiểm cuối), đệm 4 số 0
khoi = "".join("%X" % (int(x, 16) ^ int(y, 16)) for x, y in zip(a, b))   # XOR từng cặp chữ số hex
print(khoi)""", out="041225EEEEEEEEEE", lang="python")
    che_mac = prog("CheVaMac", """
import hmac, hashlib
pan = "4111111111111111"
print(pan[:6] + "*" * 6 + pan[-4:])           # che số thẻ: giữ 6 số đầu và 4 số cuối
def mac(nd):
    return hmac.new(b"k", nd.encode(), hashlib.sha256).hexdigest()[:16]
print(mac("amt=500000"))
print(mac("amt=900000"))
print(mac("amt=500000") == mac("amt=900000"))""", out="""411111******1111
7625fd27947ee367
7958d294fb89b6dc
False""", lang="python")
    lab_lu = prog("LuhnLab", """
def luhn(so):
    tong = 0
    for i, c in enumerate(reversed(so)):
        d = int(c)
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d = d - 9
        tong = tong + d
    return tong % 10 == 0
the = "5500005555555559"
print(luhn(the))
print(luhn(the[:-1] + "8"))
print(the[:6] + "*" * 6 + the[-4:])""", out="""True
False
550000******5559""", lang="python")
    hook = sc("hook", "hook", "Vì sao số thẻ phải được che, còn PIN không bao giờ xuất hiện nguyên văn?", [
        st("""<p>Một lập trình viên ghi nhật ký để gỡ lỗi: có cả số thẻ và PIN. Nhật ký được sao lưu, nhiều người đọc được, và <b>rò rỉ</b> chỉ cần một người xấu.</p>
<div class="box key">Bảo mật thanh toán dựa trên bốn ý: <b>che dữ liệu</b>, <b>không lộ khoá</b>, <b>phát hiện sửa bản tin</b>, <b>xác thực người dùng</b>.</div>""",
           """Chào bạn, một lập trình viên ghi nhật ký để gỡ lỗi, trong đó có cả số thẻ lẫn mã PIN. Nhật ký được sao lưu, nhiều người đọc được, và rò rỉ chỉ cần một người xấu.
           Bảo mật thanh toán dựa trên bốn ý. Che dữ liệu, không lộ khoá, phát hiện sửa bản tin, và xác thực người dùng."""),
        st(table(["ý", "công cụ", "bài này làm gì"],
                 [["che dữ liệu", "che số thẻ, không ghi PIN", "tự viết hàm che"],
                  ["không lộ khoá", "HSM giữ khoá, mã hoá khối PIN", "tính khối PIN"],
                  ["phát hiện sửa bản tin", "mã xác thực bản tin (MAC)", "đổi 1 chữ số, MAC đổi"],
                  ["xác thực người dùng", "sinh trắc học theo Thông tư 50/2024 (sửa đổi bởi Thông tư 77/2025)", "tính khi nào bắt buộc"]]),
           """Bảng này là kế hoạch bài học. Che dữ liệu bằng cách che số thẻ và không ghi PIN. Không lộ khoá nhờ thiết bị HSM giữ khoá và mã hoá khối PIN. Phát hiện sửa bản tin bằng mã xác thực bản tin.
           Xác thực người dùng bằng sinh trắc học theo Thông tư năm mươi năm hai nghìn không trăm hai mươi tư. Thông tư này đã được sửa đổi bởi Thông tư bảy mươi bảy năm hai nghìn không trăm hai mươi lăm."""),
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
        st("""<p><b>Bước 3.</b> Theo Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN, hiệu lực 01/03/2026), chuyển tiền trực tuyến của cá nhân <b>trên $10$ triệu đồng</b> một giao dịch, hoặc khi <b>tổng trong ngày vượt $20$ triệu đồng</b>, phải xác thực sinh trắc học (Phụ lục 01). Tổng cộng dồn tính lại từ $0$ sau mỗi lần xác thực.</p>
<span class='note'>Làm thử: $15$ triệu → cần. $5$ triệu, ngày chưa có gì → không.</span>""",
           """Bước ba nói về quy tắc xác thực sinh trắc học. Theo Thông tư năm mươi năm hai nghìn không trăm hai mươi tư, chuyển tiền trực tuyến của cá nhân phải xác thực sinh trắc học khi một giao dịch trên mười triệu đồng. Thông tư ấy được sửa đổi bởi Thông tư bảy mươi bảy năm hai nghìn không trăm hai mươi lăm. Bản sửa đổi có hiệu lực từ ngày một tháng ba năm hai nghìn không trăm hai mươi sáu.
           Khi tổng trong ngày vượt hai mươi triệu đồng cũng phải xác thực. Theo thông tư ấy, tổng cộng dồn được tính lại từ không sau mỗi lần đã xác thực sinh trắc học. Làm thử, mười lăm triệu thì cần, năm triệu khi ngày chưa có giao dịch nào thì không."""),
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
    # ── AF2: P1 Python tối thiểu, mã chạy thật (khối PIN, che số thẻ, MAC), quy mô HSM, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm ba điều để đọc mã", "nghĩa", "ví dụ"],
                 [["⑦ Cắt chuỗi từ cuối", "<code>s[-4:]</code> là 4 ký tự cuối; <code>s[:6]</code> là 6 ký tự đầu; <code>s[-13:-1]</code> là 12 ký tự trước ký tự cuối", "<code>\"41111\"[-2:]</code> = <code>\"11\"</code>"],
                  ["⑧ XOR từng cặp", "<code>int(x, 16)</code> đọc chữ số hex; <code>^</code> là XOR; <code>\"%X\" % n</code> viết lại bằng chữ số hex; <code>zip(a, b)</code> ghép cặp từng vị trí", "<code>\"%X\" % (0x4 ^ 0x1)</code> = <code>\"5\"</code>"],
                  ["⑨ MAC bằng thư viện chuẩn", "<code>hmac.new(khoá, nội_dung, hashlib.sha256).hexdigest()</code> cho dãy chữ số hex; ta lấy 16 ký tự đầu", "khoá thử <code>b\"k\"</code>"]]),
           """Thêm ba điều để đọc mã bằng một ngôn ngữ lập trình khác. Cắt chuỗi từ cuối cho phép lấy mấy ký tự cuối, hoặc mấy ký tự đầu. Phép XOR từng cặp đọc từng chữ số thập lục phân, XOR chúng, rồi viết lại, ghép cặp theo từng vị trí.
           Cuối cùng, mã xác thực bản tin có sẵn trong thư viện chuẩn, cho ra một dãy chữ số thập lục phân, và ta lấy mười sáu ký tự đầu.""", clear=True),
    ], at=1)
    pre["title"] = "Trước hết: chín điều cần hiểu"
    run = sc("chay_that", "example", "Chạy thật: khối PIN, che số thẻ và MAC bằng chương trình ngắn", [
        st(code_block(pin_block, title="Tính khối PIN định dạng 0 từ PIN thử và số thẻ thử"),
           """Ta tính khối PIN bằng chương trình ngắn, với dữ liệu thử. Biến thứ nhất là PIN đã đệm thành không bốn một hai ba bốn rồi các chữ F. Biến thứ hai là mười hai số cuối của thẻ, bỏ số kiểm cuối, đệm bốn số không phía trước.
           Dòng bốn đọc từng cặp chữ số hex của hai dãy, XOR chúng, và viết lại."""),
        st(out_block(pin_block),
           """Khi chạy thật, khối PIN là không bốn một hai hai năm rồi các chữ E, đúng như phép tính tay. Bên nào có khoá và số thẻ thì XOR lại để lấy PIN. Người không có thì chỉ thấy dãy này.""", clear=True),
        st(code_block(che_mac, title="Che số thẻ và tính MAC của hai bản tin chỉ khác số tiền") + out_block(che_mac),
           """Đoạn này che số thẻ, giữ sáu số đầu và bốn số cuối. Rồi nó tính mã xác thực bản tin của hai nội dung chỉ khác số tiền, và so sánh.
           Khi chạy thật, số thẻ hiện bốn một một một một một, sáu dấu sao, một một một một. Hai mã xác thực khác hẳn nhau, nên so sánh cho kết quả sai, và bên nhận phát hiện ra bản tin bị sửa.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: mỗi giao dịch cần phép tính khoá, thiết bị HSM phải nhân lên", [
        st("""<p>Mỗi giao dịch cần $2$ thao tác với khoá bí mật (dịch khối PIN và tính MAC). Giả sử một thiết bị HSM làm $1\\,000$ thao tác mỗi giây <i>(số minh hoạ)</i>:</p>"""
           + table(["tải", "giao dịch mỗi giây", "thao tác khoá mỗi giây", "HSM tối thiểu"],
                   [["×1", "100", "200", "1"],
                    ["×100", "10 000", "20 000", "<b>20</b>"],
                    ["×10 000", "1 000 000", "2 000 000", "<b>2 000</b>"]]),
           """Mỗi giao dịch cần hai thao tác với khoá bí mật, là dịch khối PIN và tính mã xác thực bản tin. Giả sử một thiết bị giữ khoá làm một nghìn thao tác mỗi giây. Đây là số minh hoạ.
           Với một trăm giao dịch mỗi giây cần hai trăm thao tác, một thiết bị là đủ. Tải tăng một trăm lần cần hai mươi thiết bị. Tải tăng mười nghìn lần cần hai nghìn thiết bị.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Mọi thao tác khoá đều đi qua HSM: ở ×1 một thiết bị là đủ; ở ×10 000 phải mua và vận hành 2 000 thiết bị, và mỗi thiết bị là một điểm cần bảo vệ, sao lưu, đổi khoá.</div>
<div class="box key"><b>Đánh đổi:</b> chỉ để khoá gốc và khâu dịch khối PIN trong HSM; MAC bản tin có thể dùng khoá phiên ngắn hạn sinh từ khoá gốc rồi tính ở máy thường (đúng cách làm tuỳ chuẩn của từng mạng); gom lô để giảm vòng đi về. Mỗi cách giảm tải cho HSM cũng mở thêm một chỗ phải bảo vệ khoá.</div>""",
           """Câu hỏi là giải pháp cũ sẽ gãy ở chỗ nào khi tải tăng lên. Mọi thao tác khoá đều đi qua thiết bị giữ khoá. Ở tải gốc một thiết bị là đủ, nhưng ở tải gấp mười nghìn lần phải mua và vận hành hai nghìn thiết bị, và mỗi thiết bị là một điểm cần bảo vệ, sao lưu, đổi khoá.
           Đánh đổi là chỉ để khoá gốc và khâu dịch khối PIN trong thiết bị. Còn mã xác thực bản tin có thể dùng khoá phiên ngắn hạn, sinh từ khoá gốc, rồi tính ở máy thường, tuỳ chuẩn của từng mạng. Gom lô để giảm vòng đi về. Mỗi cách giảm tải cho thiết bị cũng mở thêm một chỗ phải bảo vệ khoá.""", clear=True),
    ], checks=["100 * 2 == 200", "10_000 * 2 == 20_000", "1_000_000 * 2 == 2_000_000", "-(-200 // 1000) == 1", "-(-20_000 // 1000) == 20",
               "-(-2_000_000 // 1000) == 2000"])
    write_lab("BNK", "L13", """# Lab BNK L13 — Phép kiểm Luhn cho số thẻ thử

Phép kiểm Luhn: đi từ **phải sang trái**, chữ số ở vị trí 0 (cuối) giữ nguyên, chữ số ở vị trí 1, 3, 5, … **nhân đôi** (kết quả quá 9 thì trừ 9); cộng tất cả; **tổng chia hết cho 10** thì hợp lệ.

Viết chương trình `luhn_lab.py` (Python):
1. Hàm `luhn(so)` trả `True` hoặc `False` theo phép kiểm trên.
2. Với thẻ thử `the = "5500005555555559"`: in `luhn(the)`, rồi in `luhn` của số đó khi đổi chữ số cuối thành `8`, rồi in số thẻ đã che (giữ 6 số đầu, 4 số cuối, 6 dấu `*` ở giữa).

Kết quả đúng ba dòng: `True`, `False`, `550000******5559`. Chạy: `python luhn_lab.py`. Chấm: `bash labs/cham.sh BNK L13 luhn_lab.py`.
""", "py", lab_lu["code"], lab_lu["out"])
    lab = practice_scene(sc, "Tự làm: phép kiểm Luhn và che số thẻ", practice_steps(
        st, "BNK", "L13",
        """<p><b>Đề</b>: Luhn: từ phải sang, nhân đôi chữ số ở vị trí 1, 3, 5, … (quá 9 thì trừ 9), cộng hết, chia hết cho 10 là hợp lệ. Viết <code>luhn_lab.py</code>:</p>
<ol><li>hàm <code>luhn(so)</code> trả <code>True</code>/<code>False</code></li>
<li>thẻ thử <code>5500005555555559</code>: in <code>luhn</code> của nó; in <code>luhn</code> khi đổi chữ số cuối thành 8; in số thẻ đã che</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Phép kiểm số kiểm cuối đi từ phải sang trái, nhân đôi chữ số ở vị trí một, ba, năm, và cứ thế, quá chín thì trừ chín, rồi cộng tất cả. Tổng chia hết cho mười thì số thẻ hợp lệ.
        Hãy viết hàm kiểm này, thử với số thẻ thử, thử lại khi đổi chữ số cuối thành tám, và in số thẻ đã che. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_lu["out"], "luhn_lab.py",
        """<div class="box key"><b>Nếu kẹt:</b> duyệt <code>for i, c in enumerate(reversed(so))</code> (<code>enumerate</code> đánh số vị trí từ 0); nếu <code>i % 2 == 1</code> thì nhân đôi, quá 9 thì trừ 9; cộng dồn; trả <code>tong % 10 == 0</code>.
Lời giải ở <code>labs/BNK/L13/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, duyệt các chữ số từ phải sang kèm vị trí. Vị trí lẻ thì nhân đôi, nếu quá chín thì trừ chín. Cộng dồn, rồi trả về việc tổng có chia hết cho mười không. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=180), "BNK", "L13")
    return lesson("L13", "bao_mat_thanh_toan_pin_hsm", "Bài 13 — Bảo mật thanh toán: khối PIN, HSM, MAC và sinh trắc học",
                  "curriculum/bnk.yaml L13; audit/bnk/verify_bnk.py L13; audit/review/screen_code/BNK.yaml (mã chạy thật bằng Python 3.13: khối PIN, che số thẻ, HMAC-SHA256, Luhn); ISO 9564-1 (khối PIN định dạng 0); Thông tư 50/2024/TT-NHNN về an toàn hệ thống thanh toán, sinh trắc học (Phụ lục 01; audit/legal/registry.yaml: đã đọc bản gốc Công báo 1279+1280, 30-11-2024), SỬA ĐỔI bởi Thông tư 77/2025/TT-NHNN hiệu lực 01/3/2026 (bản hợp nhất 25/VBHN-NHNN); ngưỡng cá nhân 'trên 10 triệu/giao dịch' và 'tổng ngày vượt 20 triệu'; PCI DSS v4.0.1 Req. 3.3.1.2 (không lưu PIN / khối PIN sau cấp phép) và 3.4.1 (che PAN khi hiển thị); ISO/IEC 7812-1 (số kiểm Luhn); Thales payShield Host Command Reference (dịch khối PIN TPK/ZPK→ZPK; khoá bọc bằng ZMK/LMK); dữ liệu thẻ, PIN và khoá trong bài là dữ liệu thử; thông lượng HSM trong bảng quy mô là số minh hoạ",
                  ["Tính khối PIN định dạng 0 từ PIN thử và số thẻ thử", "Giải thích vì sao sửa bản tin làm MAC không khớp",
                   "Áp quy tắc sinh trắc học theo giao dịch và cộng dồn trong ngày", "Che số thẻ và không ghi PIN vào nhật ký",
                   "Chạy chương trình tính khối PIN, che số thẻ và MAC để thấy kết quả thật",
                   "Tính số thiết bị HSM tối thiểu khi tải tăng ×100, ×10 000",
                   "Viết hàm kiểm Luhn và hàm che số thẻ"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "check"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
