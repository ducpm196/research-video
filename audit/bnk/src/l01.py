from lib import *


def build():
    hook = sc("hook", "hook", "Vì sao hai người cùng nạp tiền lại làm mất một khoản?", [
        st("""<p>Số dư là $100$. Người A nạp $50$, người B nạp $30$ cùng lúc. Đúng ra phải ra $180$.</p>
<div class="box key">Nhưng máy có thể in ra <b>180</b>, <b>150</b> hoặc <b>130</b>, tuỳ luồng nào chen vào trước.</div>""",
           """Chào bạn, số dư là một trăm. Người A nạp năm mươi, người B nạp ba mươi, cùng một lúc, nên kết quả đúng phải là một trăm tám mươi.
           Nhưng máy có thể in ra một trăm tám mươi, một trăm năm mươi, hoặc một trăm ba mươi, tuỳ luồng nào chen vào trước."""),
        st(table(["tình huống", "hậu quả"],
                 [["hai luồng sửa cùng một số dư", "mất một khoản nạp, ngân hàng lệch sổ"],
                  ["10 000 yêu cầu cùng chờ đối tác trả lời", "hết luồng, yêu cầu mới xếp hàng dài"]]),
           """Hôm nay ta học hai chuyện. Một là hai luồng sửa cùng một số dư thì mất khoản nạp. Hai là mười nghìn yêu cầu cùng chờ đối tác thì dịch vụ hết luồng.
           Luồng ảo của Java hai mươi mốt giải quyết chuyện thứ hai."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: ba điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Luồng", "một dòng việc chạy riêng trong chương trình; nhiều luồng chạy cùng lúc và dùng chung dữ liệu", "mỗi yêu cầu chuyển tiền một luồng"],
                  ["② Đọc rồi ghi", "muốn tăng số dư phải đọc số cũ, cộng, rồi ghi lại", "đọc 100, ghi 150"],
                  ["③ Chạy xen kẽ", "CPU (bộ xử lý chạy lệnh) đổi qua lại giữa các luồng ngay giữa chừng", "A đọc, B đọc, rồi mới ghi"]]),
           """Ôn ba điều. Luồng là một dòng việc chạy riêng trong chương trình. Nhiều luồng chạy cùng lúc và dùng chung dữ liệu, ví dụ mỗi yêu cầu chuyển tiền có một luồng.
           Muốn tăng số dư phải đọc số cũ, cộng thêm, rồi ghi lại.
           Còn bộ xử lý chạy lệnh có thể đổi qua lại giữa các luồng ngay giữa chừng, nên A đọc, B đọc rồi mới ghi là chuyện bình thường."""),
        st("""$$100 + 50 + 30 = 180$$""",
           """Nếu hai việc chạy lần lượt, hết việc này rồi mới tới việc kia, thì một trăm cộng năm mươi cộng ba mươi bằng một trăm tám mươi, đúng như mong đợi.""",
           introduces=["plus"] if False else None),
    ], checks=["100 + 50 + 30 == 180"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["race condition", "kết quả phụ thuộc thứ tự chạy may rủi của các luồng"],
                  ["lost update", "một lần ghi đè mất lần ghi trước"],
                  ["vùng găng", "đoạn mã đọc rồi ghi dữ liệu dùng chung, chỉ an toàn khi mỗi lúc một luồng chạy"],
                  ["lock (khoá)", "chỉ một luồng được vào vùng găng tại một thời điểm"],
                  ["blocking I/O", "luồng đứng chờ mạng hoặc đĩa, không làm gì"],
                  ["virtual thread", "luồng ảo, rất nhẹ, do Java quản lý chứ không do hệ điều hành"],
                  ["luồng nền (platform / carrier thread)", "luồng thật của hệ điều hành; luồng ảo chạy nhờ trên nó"]]),
           """Bảng dưới đây giải nghĩa bảy thuật ngữ mà bài sẽ dùng. Điều kiện tranh chấp là khi kết quả phụ thuộc thứ tự chạy may rủi. Mất cập nhật là khi một lần ghi đè mất lần ghi trước.
           Vùng găng là đoạn mã đọc rồi ghi dữ liệu dùng chung, chỉ an toàn khi mỗi lúc một luồng chạy. Khoá cho phép chỉ một luồng vào vùng găng. Chờ vào ra là khi luồng đứng đợi mạng hoặc đĩa. Luồng ảo là luồng rất nhẹ do Java quản lý.
           Còn luồng nền là luồng thật của hệ điều hành, và luồng ảo chạy nhờ trên nó."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: xen kẽ, khoá, và luồng ảo", [
        st(svg(1500, 420,
               txt(60, 60, "Luồng A", 26, "start", "#1f2937", True), txt(60, 200, "Luồng B", 26, "start", "#1f2937", True),
               box(200, 30, 230, 60, "A đọc: 100", C_BLUE), box(700, 30, 230, 60, "A ghi: 150", C_BLUE),
               box(330, 170, 230, 60, "B đọc: 100", C_AMBER), box(960, 170, 230, 60, "B ghi: 130", C_AMBER),
               arrow(315, 95, 700, 60, "#2a78d6"),
               txt(750, 330, "B ghi sau cùng: số dư = 130, khoản nạp 50 của A biến mất", 28, "middle", "#dc2626", True),
               txt(750, 380, "A và B cùng đọc 100 trước khi ai kịp ghi", 24, "middle", "#475569")),
           """Hình cho thấy một cách xen kẽ xấu. A đọc số dư một trăm. Trước khi A kịp ghi, B cũng đọc một trăm. A ghi một trăm năm mươi.
           Rồi B ghi một trăm ba mươi, đè lên kết quả của A. Khoản nạp năm mươi của A biến mất."""),
        st(svg(1500, 420,
               box(60, 130, 260, 120, ["Luồng A", "giữ khoá"], C_GREEN, bold=True),
               box(560, 130, 380, 120, ["vùng găng", "đọc rồi ghi số dư"], C_AMBER, bold=True),
               box(1180, 130, 260, 120, ["Luồng B", "đang chờ"], C_GRAY),
               arrow(320, 190, 555, 190, "#16a34a"), arrow(1180, 190, 945, 190, "#6b7280", None, dash=True),
               txt(750, 330, "Chỉ một luồng vào vùng găng. Luồng kia chờ, rồi mới vào.", 28, "middle", "#1f2937", True)),
           """Khoá giải quyết chuyện đó. Luồng A giữ khoá và vào vùng găng, nơi đọc rồi ghi số dư. Luồng B tới sau, thấy khoá đang bị giữ, nên đứng chờ.
           Khi A xong, B mới vào. Hai việc chạy lần lượt, nên kết quả luôn đúng."""),
        st(svg(1500, 440,
               panel(40, 30, 700, 380, "Luồng nền: 200 luồng", C_AMBER),
               box(80, 110, 160, 60, "chờ", C_GRAY), box(260, 110, 160, 60, "chờ", C_GRAY), box(440, 110, 160, 60, "chờ", C_GRAY),
               box(80, 200, 160, 60, "chờ", C_GRAY), box(260, 200, 160, 60, "chờ", C_GRAY), box(440, 200, 160, 60, "chờ", C_GRAY),
               txt(390, 330, "200 luồng đều đứng chờ → yêu cầu thứ 201 xếp hàng", 24, "middle", "#dc2626", True),
               panel(780, 30, 680, 380, "Luồng ảo: 10 000 luồng", C_GREEN),
               box(820, 110, 600, 70, "luồng ảo chờ → nhả luồng nền", C_BLUE),
               box(820, 210, 600, 70, "luồng nền đi chạy việc khác", C_GREEN),
               arrow(1120, 180, 1120, 205, "#475569"),
               txt(1120, 340, "chờ không giữ chân luồng nền", 24, "middle", "#16a34a", True)),
           """Hình thứ ba so sánh hai cách xử lý việc chờ. Bên trái, mỗi yêu cầu giữ một luồng nền trong lúc chờ. Hai trăm luồng đều đứng chờ, nên yêu cầu thứ hai trăm lẻ một phải xếp hàng.
           Bên phải, luồng ảo khi chờ sẽ nhả luồng nền ra, để luồng nền đi chạy việc khác. Nhờ vậy mười nghìn luồng ảo cùng chờ cũng không cạn."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: bao nhiêu kết quả có thể xảy ra?", [
        st("""<p><b>Bước 1.</b> Mỗi luồng gồm hai việc nhỏ, <b>đọc</b> rồi <b>ghi</b>, và việc ghi luôn sau việc đọc của cùng luồng.</p>
<span class='note'>Làm thử: hai luồng thì có $2 \\cdot 2 = 4$ việc nhỏ.</span>""",
           """Bước một, vì mỗi luồng gồm hai việc nhỏ là đọc rồi ghi, và việc ghi luôn sau việc đọc của cùng luồng, nên hai luồng có bốn việc nhỏ.
           Làm thử, hai nhân hai bằng bốn.""",
           introduces=["cdot"]),
        st("""<p><b>Bước 2.</b> Cách xếp bốn việc vào bốn ô, giữ thứ tự trong từng luồng, bằng số cách chọn hai ô cho luồng A.</p>
<span class='note'>Làm thử: ô đầu của A có $4$ chỗ, ô sau còn $3$, được $4 \\cdot 3$; đổi chỗ hai ô vẫn là một cách chọn nên chia $2 \\cdot 1$: $\\frac{4 \\cdot 3}{2 \\cdot 1} = 6$ cách.</span>""",
           """Bước hai, vì thứ tự trong từng luồng được giữ, nên số cách xếp bằng số cách chọn hai ô trong bốn ô cho luồng A.
           Làm thử, ô thứ nhất của A có bốn chỗ, ô thứ hai còn ba chỗ, nhưng đổi chỗ hai ô vẫn là cùng một cách chọn, nên bốn nhân ba chia hai nhân một bằng sáu cách."""),
        st("""<p><b>Bước 3.</b> Chạy thử cả sáu cách: hai cách cho $180$, hai cách cho $130$, hai cách cho $150$.</p>
<span class='note'>Chỉ đúng khi một luồng xong cả đọc lẫn ghi rồi luồng kia mới đọc.</span>""",
           """Bước ba, ta chạy thử cả sáu cách. Hai cách cho kết quả một trăm tám mươi, hai cách cho một trăm ba mươi, hai cách cho một trăm năm mươi.
           Kết quả chỉ đúng khi một luồng xong cả đọc lẫn ghi rồi luồng kia mới đọc.
           Vì vậy mới có lúc đúng lúc sai, và rất khó thấy khi kiểm thử."""),
    ], checks=["2 * 2 == 4", "math.comb(4, 2) == 6 == len(set(__import__('itertools').permutations([0, 0, 1, 1])))",
               "alg.bnk_lost_update(100, [50, 30]) == [130, 150, 180]"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Chạy A đọc, B đọc, A ghi, B ghi, với số dư đầu $100$.</p>
$$① \\; \\text{A đọc } 100,\\ \\text{B đọc } 100$$""",
           """Ta theo dõi cách xen kẽ xấu. Phép tính thứ nhất, A đọc được một trăm, và B cũng đọc được một trăm, vì chưa ai ghi."""),
        st("""$$② \\; \\text{A ghi } 100 + 50 = \\hl{150}$$""",
           """Phép tính thứ hai, A ghi giá trị đã đọc cộng năm mươi, là một trăm năm mươi."""),
        st("""$$③ \\; \\text{B ghi } 100 + 30 = \\hl{130}$$""",
           """Phép tính thứ ba, B ghi giá trị mà B đã đọc, một trăm, cộng ba mươi, là một trăm ba mươi, và nó đè lên kết quả của A."""),
        st("""$$④ \\; 180 - 130 = \\hl{50}\\ \\text{đã mất}$$""",
           """Phép tính thứ tư, kết quả đúng là một trăm tám mươi, thực tế còn một trăm ba mươi, nên mất đúng năm mươi, chính là khoản nạp của A."""),
        st("""$$⑤ \\; \\text{có khoá: } 100 + 50 + 30 = \\hlg{180}$$""",
           """Phép tính thứ năm, khi có khoá, hai việc chạy lần lượt, nên luôn ra một trăm tám mươi."""),
    ], checks=["100 + 50 == 150", "100 + 30 == 130", "180 - 130 == 50", "alg.bnk_lost_update(100, [50, 30])[-1] == 100 + 50 + 30"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: luồng ảo nhanh hơn bao nhiêu?", [
        st("""<p>Mười nghìn yêu cầu, mỗi yêu cầu chờ $0{,}1$ giây. Với $200$ luồng nền:</p>
<p>Vì mỗi lượt xử lý được $200$ yêu cầu, nên cần $\\frac{10\\,000}{200} = 50$ lượt:</p>
$$50 \\cdot 0{,}1 = \\hl{5}\\ \\text{giây}$$""",
           """Giờ so thời gian xử lý. Mười nghìn yêu cầu, mỗi yêu cầu chờ không phẩy một giây. Vì mỗi lượt xử lý được hai trăm yêu cầu, nên cần năm mươi lượt.
           Năm mươi nhân không phẩy một bằng năm giây."""),
        st(table(["cách tính", "kết quả"],
                 [["theo lô: 50 lô × 0,1 giây", "5 giây"],
                  ["theo thông lượng: 200 ÷ 0,1 = 2000 yêu cầu mỗi giây, 10 000 ÷ 2000", "5 giây"],
                  ["luồng ảo (mô hình lý tưởng): tất cả chờ cùng lúc", "0,1 giây"]]),
           """Kiểm bằng đường khác. Thông lượng là hai trăm chia không phẩy một, bằng hai nghìn yêu cầu mỗi giây, nên mười nghìn yêu cầu mất năm giây, khớp với cách tính theo lô.
           Luồng ảo, trong mô hình lý tưởng bỏ qua chi phí CPU, chờ tất cả cùng lúc nên chỉ mất không phẩy một giây."""),
    ], checks=["alg.bnk_batch_time(10000, 200, 0.1) == 5.0", "abs(10000 / (200 / 0.1) - 5.0) < 1e-9", "alg.bnk_batch_time(10000, 10000, 0.1) == 0.1"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ rằng <code>soDu += 50</code> là một việc không thể chia nhỏ. Thực ra nó là <b>đọc, cộng, ghi</b>: ba việc,
nên luồng khác chen vào được.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ rằng một câu lệnh cộng thêm năm mươi là một việc không chia nhỏ được.
           Thực ra nó gồm đọc, cộng và ghi, nên luồng khác chen vào được."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Giữ khoá khi gọi mạng.</b> Khoá bao cả lời gọi sang đối tác mất $300$ ms
thì mọi luồng khác chờ $300$ ms theo. Khoá chỉ nên bao đoạn đọc rồi ghi ngắn.<br><span class="note">Phép thử: đo thời gian giữ khoá.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là giữ khoá khi gọi mạng. Nếu khoá bao cả lời gọi sang đối tác mất ba trăm mili giây,
           mọi luồng khác phải chờ ba trăm mili giây theo. Khoá chỉ nên bao đoạn đọc rồi ghi ngắn, và hãy đo thời gian giữ khoá."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nghĩ luồng ảo làm CPU chạy nhanh hơn. Nó chỉ giúp việc <b>chờ</b>.
<code>synchronized</code> là từ khoá Java bọc một khối mã bằng khoá, mỗi lúc chỉ một luồng vào.
Ở Java 21, chờ bên trong khối <code>synchronized</code> có thể <b>ghim</b> luồng ảo vào luồng nền (luồng nền bị giữ chân), mất lợi ích.
Từ Java 24 (JEP 491, một bản đề xuất tính năng chính thức của Java), <code>synchronized</code> không còn ghim; gọi mã native (mã máy viết ngoài Java) vẫn ghim.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là nghĩ luồng ảo làm CPU chạy nhanh hơn. Nó chỉ giúp những việc phải chờ.
           Khối đồng bộ là một từ khoá của Java, bọc một đoạn mã bằng khoá để mỗi lúc chỉ một luồng vào.
           Ở Java hai mươi mốt, chờ bên trong khối đồng bộ có thể ghim luồng ảo vào luồng nền, tức là giữ chân luồng nền, nên mất lợi ích.
           Từ Java hai mươi tư, khối đồng bộ không còn ghim, nhưng gọi mã máy gốc viết ngoài Java vẫn ghim."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Ba luồng, mỗi luồng đọc rồi ghi. Có bao nhiêu cách xen kẽ?"],
                  ["2", "2000 yêu cầu, mỗi yêu cầu chờ 0,2 giây, 50 luồng nền. Mất bao lâu?"],
                  ["3", "Quyết định: dịch vụ gọi đối tác chậm 300 ms, hàng nghìn yêu cầu cùng lúc. Chọn gì?"]]),
           """Đến lượt bạn. Câu một, ba luồng, mỗi luồng đọc rồi ghi, có bao nhiêu cách xen kẽ? Câu hai, hai nghìn yêu cầu, mỗi yêu cầu chờ không phẩy hai giây, năm mươi luồng nền, mất bao lâu?
           Câu ba, dịch vụ gọi đối tác chậm ba trăm mili giây, hàng nghìn yêu cầu cùng lúc, bạn chọn gì? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Xếp $6$ việc vào $6$ ô: ô đầu có $6$ cách chọn việc, ô hai $5$ cách, …: $6 \\cdot 5 \\cdot 4 \\cdot 3 \\cdot 2 \\cdot 1 = 720$ thứ tự. Hai việc của mỗi luồng có $2$ cách đứng trước sau mà chỉ $1$ cách hợp lệ (đọc trước ghi sau), nên chia cho $2 \\cdot 2 \\cdot 2 = 8$.</p>
$$\\frac{720}{8} = \\hl{90}$$""",
           """Đáp án câu một. Xếp sáu việc vào sáu ô, ô đầu có sáu cách chọn, ô hai có năm cách, cứ thế được bảy trăm hai mươi thứ tự. Vì hai việc của mỗi luồng có hai cách đứng trước sau mà chỉ một cách hợp lệ, là đọc trước ghi sau, nên ta chia cho hai nhân hai nhân hai, là tám.
           Kết quả là chín mươi cách."""),
        st("""$$\\frac{2000}{50} \\cdot 0{,}2 = 40 \\cdot 0{,}2 = \\hlg{8}\\ \\text{giây}$$""",
           """Đáp án câu hai. Hai nghìn chia năm mươi bằng bốn mươi lượt, nhân không phẩy hai, được tám giây."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tăng số luồng nền lên rất lớn", "không phải sửa mã", "tốn bộ nhớ, hệ điều hành chuyển luồng nặng"],
                  ["luồng ảo (Java 21)", "chờ gần như miễn phí, mã vẫn viết tuần tự", "tránh chỗ gây ghim (Java 21: chờ trong synchronized; mã native); đo trước khi tin"]]),
           """Đáp án câu ba là một đánh đổi. Tăng số luồng nền thì không sửa mã nhưng tốn bộ nhớ. Luồng ảo cho phép chờ gần như miễn phí mà mã vẫn viết tuần tự, nhưng phải tránh ghim và phải đo."""),
    ], checks=["len(set(__import__('itertools').permutations([0, 0, 1, 1, 2, 2]))) == 90 == 720 // 8",
               "6 * 5 * 4 * 3 * 2 * 1 == 720 == math.factorial(6) and 2 * 2 * 2 == 8",
               "alg.bnk_batch_time(2000, 50, 0.2) == 8.0"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đọc – ghi chen nhau", "mất cập nhật", "khoá vùng găng ngắn", "luồng ảo cho việc chờ"),
           """Tổng kết chuỗi logic. Đọc và ghi chen nhau gây mất cập nhật. Khoá một vùng găng ngắn sửa chuyện đó. Còn luồng ảo giải quyết việc chờ mạng quá nhiều."""),
        st("""<div class='box key'><b>Tư duy:</b> lỗi tranh chấp không hiện mỗi lần chạy, nên phải <b>suy luận</b> mọi cách xen kẽ chứ đừng chỉ chạy thử.
Khoá bao ít nhất có thể; luồng ảo là cho chờ, không phải cho tính toán.</div>""",
           """Điều cần mang theo. Lỗi tranh chấp không hiện mỗi lần chạy, nên phải suy luận mọi cách xen kẽ chứ đừng chỉ chạy thử.
           Khoá bao ít nhất có thể, và luồng ảo là để chờ, không phải để tính toán."""),
    ])
    return lesson("L01", "da_luong_khoa_luong_ao", "Bài 1 — Đa luồng, khoá và luồng ảo Java 21",
                  "curriculum/bnk.yaml L01; audit/bnk/verify_bnk.py L01; JEP 444 Virtual Threads (JDK 21: ghim khi chờ trong synchronized hoặc native); JEP 491 Synchronize Virtual Threads without Pinning (JDK 24); Goetz et al., Java Concurrency in Practice",
                  ["Liệt kê mọi cách xen kẽ của hai luồng và nhận ra mất cập nhật", "Giải thích khoá làm các luồng chạy lần lượt",
                   "Tính thời gian xử lý theo lô và so với luồng ảo", "Chọn giữa tăng luồng nền và luồng ảo"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
