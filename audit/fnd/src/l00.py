from lib import *
from labkit import write_lab, practice_steps, practice_scene

KIEM = """for ten in bash git javac java python; do
  if command -v "$ten" >/dev/null; then echo "✔ $ten"
  else echo "THIEU $ten"; fi
done
if python -c "import sqlite3" 2>/dev/null; then echo "✔ sql"
else echo "THIEU sql"; fi"""
KIEM_OUT = "✔ bash\n✔ git\n✔ javac\n✔ java\n✔ python\n✔ sql"


def build():
    kiem = cmd("KiemMay", [("bash kiem.sh", KIEM_OUT)], files={"kiem.sh": KIEM + "\n"})
    loi = cmd("GoSai", [("pyton --version", "bash: pyton: command not found")])

    sc_hook = sc("hook", "hook", "Cùng một chương trình: chờ mười giây hay gần hai mươi tám giờ?", [
        st(table(["số lần đọc", "mỗi lần chờ", "tổng chờ"],
                 [["1 000", "10 mili giây", "<b>10 giây</b>"], ["10 000 000", "10 mili giây", "<b>100 000 giây</b>, gần 28 giờ"]])
           + "<p>Chương trình đọc các bản ghi nhỏ nằm rải rác trên ổ đĩa cơ (số minh hoạ). Cùng cách viết; chỉ khác "
             "<b>dữ liệu nằm ở đâu</b> và <b>có bao nhiêu</b>.</p>",
           """Chào bạn, hãy nhìn một chương trình đọc các bản ghi nhỏ nằm rải rác trên ổ đĩa cơ, mỗi lần chờ chừng mười phần nghìn giây, đây là số minh hoạ.
           Một nghìn lần là mười giây, nghe chấp nhận được. Nhưng mười triệu lần thì là một trăm nghìn giây, gần hai mươi tám giờ.
           Cùng chương trình, cùng cách viết, chỉ khác dữ liệu nằm ở đâu và có bao nhiêu.""", focus=[1, "1.2", "1.3", 2]),
        st("""<div class="box key">Hôm nay, bài mở đầu của cả lộ trình, ta trả lời ba câu hỏi:
<ol><li>Máy tính <b>chạy</b> một chương trình thế nào, và vì sao chỗ để dữ liệu quyết định tốc độ?</li>
<li>Bạn nên <b>học</b> cả bộ khoá này theo cách nào để nhớ lâu?</li>
<li>Máy của bạn cần <b>cài</b> những gì, và kiểm bằng cách nào?</li></ol></div>""",
           """Hôm nay là bài mở đầu của cả lộ trình, ta trả lời ba câu hỏi. Máy tính chạy một chương trình thế nào, và vì sao chỗ để dữ liệu quyết định tốc độ.
           Bạn nên học cả bộ khoá này theo cách nào để nhớ lâu. Và máy của bạn cần cài những gì, kiểm bằng cách nào."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp, chương trình, bit và byte", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tệp", "dữ liệu có tên, lưu lâu dài trên ổ đĩa; ví dụ ảnh <code>meo.png</code>"],
                  ["② chương trình", "một tệp chứa danh sách lệnh để máy làm lần lượt"],
                  ["③ bit", "một ô nhỏ nhất, chỉ chứa $0$ hoặc $1$"],
                  ["④ byte", "tám bit ghép lại: có $2^8 = 256$ giá trị, từ $0$ tới $255$"]]),
           """Ta ôn lại bốn điều. Tệp là dữ liệu có tên, được lưu lâu dài trên ổ đĩa. Chương trình là một tệp chứa danh sách lệnh để máy làm lần lượt.
           Bit là một ô nhỏ nhất, chỉ chứa không hoặc một. Hai mũ tám bằng hai trăm năm mươi sáu, nên một byte, tức tám bit ghép lại, có hai trăm năm mươi sáu giá trị, từ không tới hai trăm năm mươi lăm.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ], checks=["2 ** 8 == 256", "256 - 1 == 255"])
    sc_sym = sc("sym", "symbol", "Giải mã năm bộ phận và một dấu hiệu", [
        st(table(["tên gọi", "làm gì", "ví dụ đời thường"],
                 [["<b>bộ xử lý</b> (CPU)", "làm từng lệnh nhỏ, rất nhanh", "người thu ngân bấm máy tính"],
                  ["<b>bộ nhớ</b> (RAM)", "giữ dữ liệu đang dùng; tắt máy là mất", "tờ giấy nháp trên bàn"],
                  ["<b>ổ đĩa</b> (SSD, HDD)", "lưu tệp lâu dài; chậm hơn bộ nhớ nhiều", "tủ hồ sơ ở phòng bên"],
                  ["<b>hệ điều hành</b>", "chương trình điều phối: nạp tệp vào bộ nhớ, chia việc", "quản lý toà nhà"],
                  ["<b>cửa sổ lệnh</b>", "khung chữ: bạn gõ lệnh, máy trả lời bằng chữ", "quầy giao dịch bằng lời"],
                  ["<b>✔</b>", "dấu tích: đạt; dùng khi kiểm máy", "dấu tích của giáo viên"]]),
           """Bảng này giải mã năm bộ phận và một dấu hiệu. Bộ xử lý làm từng lệnh nhỏ rất nhanh, giống người thu ngân bấm máy tính.
           Bộ nhớ giữ dữ liệu đang dùng, tắt máy là mất, giống tờ giấy nháp. Ổ đĩa lưu tệp lâu dài nhưng chậm hơn nhiều, giống tủ hồ sơ ở phòng bên.
           Hệ điều hành là chương trình điều phối, nạp tệp vào bộ nhớ và chia việc. Cửa sổ lệnh là khung chữ để bạn gõ lệnh. Dấu tích nghĩa là đạt.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: đường đi của một chương trình", [
        st(svg(1500, 420,
               box(20, 140, 300, 130, ["ổ đĩa", "tệp chương trình", "chậm, lưu lâu"], C_GRAY, bold=True),
               arrow(325, 205, 470, 205, "#2a78d6", "① nạp"),
               box(480, 140, 300, 130, ["bộ nhớ", "chương trình + dữ liệu", "nhanh, mất khi tắt"], C_AMBER, bold=True),
               arrow(785, 205, 930, 205, "#16a34a", "② đọc lệnh"),
               box(940, 140, 260, 130, ["bộ xử lý", "làm từng lệnh", "rất nhanh"], C_GREEN, bold=True),
               arrow(1205, 205, 1340, 205, "#16a34a", "③ kết quả"),
               box(1350, 140, 140, 130, ["màn", "hình"], C_BLUE),
               box(480, 20, 720, 70, "hệ điều hành điều phối cả ba bước", C_PURPLE, bold=True),
               arrow(840, 95, 630, 135, "#9333ea"),
               txt(750, 350, "càng sang phải càng nhanh, càng đắt, càng ít chỗ", 26, "middle", "#1f2937", True),
               txt(750, 395, "số lần phải quay về ổ đĩa quyết định chương trình nhanh hay chậm", 24, "middle", "#dc2626")),
           """Hình này là đường đi của một chương trình. Bước một, hệ điều hành nạp tệp chương trình từ ổ đĩa vào bộ nhớ, vì bộ xử lý không đọc thẳng được từ ổ đĩa.
           Bước hai, bộ xử lý đọc lệnh từ bộ nhớ và làm từng lệnh một. Bước ba, kết quả hiện ra màn hình hoặc được ghi lại.
           Càng sang phải càng nhanh, càng đắt và càng ít chỗ. Vì thế số lần phải quay về ổ đĩa quyết định chương trình nhanh hay chậm."""),
    ])
    sc_may = sc("ex_may", "example", "Ví dụ: chạy tay một chương trình ba lệnh", [
        st(table(["lệnh", "việc bộ xử lý làm"],
                 [["① nạp ô 0 ← 2", "ghi số 2 vào ô nhớ số 0"],
                  ["② nạp ô 1 ← 3", "ghi số 3 vào ô nhớ số 1"],
                  ["③ cộng ô 2 ← ô 0 + ô 1", "lấy hai số, cộng, ghi vào ô 2"]])
           + "<span class='note'>Các ô nhớ được đánh số 0, 1, 2…; mũi tên ← nghĩa là “ghi giá trị bên phải vào ô bên trái”.</span>",
           """Ta chạy tay một chương trình ba lệnh, như bộ xử lý làm. Lệnh một ghi số hai vào ô nhớ số không. Lệnh hai ghi số ba vào ô nhớ số một.
           Lệnh ba lấy hai số đó, cộng lại, và ghi vào ô số hai. Các ô nhớ được đánh số từ không, và mũi tên nghĩa là ghi giá trị bên phải vào ô bên trái.""",
           introduces=["assign"], focus=[1, "1.2", "1.3", "1.4", 2]),
        st(table(["sau lệnh", "ô 0", "ô 1", "ô 2"],
                 [["①", "<b>2</b>", "chưa ghi", "chưa ghi"], ["②", "2", "<b>3</b>", "chưa ghi"], ["③", "2", "3", "<b>5</b>"]])
           + "<p>Sau lệnh ③, ô 2 giữ $2 + 3 = \\hl{5}$.</p>",
           """Bảng này cho thấy bộ nhớ sau từng lệnh. Sau lệnh một, ô không giữ hai. Sau lệnh hai, ô một giữ ba.
           Sau lệnh ba, ô hai giữ năm, vì hai cộng ba bằng năm. Mỗi lệnh chỉ làm một việc nhỏ, và mọi chương trình, dù lớn đến đâu, đều là hàng triệu việc nhỏ như vậy.""",
           clear=True, focus=[1, "1.2", "1.3", "1.4", 2]),
    ], checks=["2 + 3 == 5"])
    sc_form = sc("formula", "formula", "Suy ra từng bước: thời gian chờ = số lần × thời gian mỗi lần", [
        st("""<p><b>Bước 1.</b> Mỗi lần đọc phải chờ xong rồi mới tới lần sau, nên các thời gian chờ <b>cộng nối tiếp</b>:</p>
$$\\text{tổng chờ} = \\text{số lần} \\times \\text{thời gian một lần}$$
<span class='note'>Làm thử: 1 000 lần × 10 mili giây = 10 000 mili giây = 10 giây ✓</span>""",
           """Bước một, mỗi lần đọc phải chờ xong rồi mới tới lần sau, nên các thời gian chờ cộng nối tiếp. Vì vậy tổng thời gian chờ bằng số lần nhân thời gian một lần.
           Làm thử, một nghìn lần nhân mười phần nghìn giây là mười nghìn phần nghìn giây, tức mười giây."""),
        st("""<p><b>Bước 2.</b> Muốn so hai thiết bị phải đổi về <b>cùng một đơn vị</b>. Mỗi bậc đơn vị gấp $1\\,000$ lần bậc dưới:</p>
$$1\\ \\text{mili giây} = 1\\,000\\ \\text{micro giây} = 1\\,000\\,000\\ \\text{nano giây}$$
<span class='note'>Làm thử: 10 mili giây = 10 000 micro giây = 10 000 000 nano giây ✓</span>""",
           """Bước hai, muốn so hai thiết bị, ta phải đổi về cùng một đơn vị. Mỗi bậc đơn vị gấp một nghìn lần bậc dưới, nên một phần nghìn giây bằng một nghìn phần triệu giây, và bằng một triệu phần tỉ giây.
           Làm thử, mười phần nghìn giây là mười nghìn phần triệu giây, và là mười triệu phần tỉ giây."""),
        st("""<p><b>Bước 3.</b> Con số nano giây khó cảm nhận, nên <b>phóng to</b>: coi $1$ nano giây như $1$ giây của đời người.</p>
$$100\\ \\text{nano giây} \\;\\to\\; 100\\ \\text{giây} = 1\\ \\text{phút}\\ 40\\ \\text{giây}$$""",
           """Bước ba, phần tỉ giây khó cảm nhận, nên ta phóng to. Coi một phần tỉ giây như một giây của đời người. Khi đó một trăm phần tỉ giây thành một trăm giây, tức một phút bốn mươi giây."""),
    ], checks=["1000 * 10 == 10000", "10 * 1000 * 1000 == 10_000_000", "100 // 60 == 1 and 100 % 60 == 40"])
    sc_ex = sc("example", "example", "Ví dụ: thang thời gian của người, năm phép tính", [
        st("""<p>Số minh hoạ (bậc độ lớn): bộ nhớ $100$ ns, ổ đĩa thể rắn $100\\,000$ ns, ổ đĩa cơ $10\\,000\\,000$ ns cho một lần đọc (ns = nano giây).</p>
$$① \\; \\text{bộ nhớ: } 100\\ \\text{ns} \\to 100\\ \\text{giây} = \\hl{1\\ \\text{phút}\\ 40\\ \\text{giây}}$$""",
           """Phép tính thứ nhất. Theo số minh hoạ, một lần đọc bộ nhớ mất chừng một trăm phần tỉ giây. Phóng to thành thang người, đó là một trăm giây, tức một phút bốn mươi giây."""),
        st("""$$② \\; \\text{ổ thể rắn: } 100\\,000\\ \\text{ns} \\to 100\\,000\\ \\text{giây} = 27\\ \\text{giờ}\\ 46\\ \\text{phút}\\ 40\\ \\text{giây}$$
<span class='note'>$100\\,000 / 3\\,600 = 27$ dư $2\\,800$ giây; $2\\,800 / 60 = 46$ dư $40$.</span>""",
           """Phép tính thứ hai. Ổ đĩa thể rắn mất một trăm nghìn phần tỉ giây, phóng to thành một trăm nghìn giây. Chia cho ba nghìn sáu trăm giây mỗi giờ được hai mươi bảy giờ, dư hai nghìn tám trăm giây, tức bốn mươi sáu phút bốn mươi giây.
           Vậy một lần đọc ở ổ đĩa thể rắn dài hơn một ngày theo thang người."""),
        st("""$$③ \\; \\text{ổ cơ: } 10\\,000\\,000\\ \\text{ns} \\to 10\\,000\\,000\\ \\text{giây} \\approx \\hl{115{,}7\\ \\text{ngày}}$$
<span class='note'>$10\\,000\\,000 / 86\\,400 \\approx 115{,}7$ (một ngày có $86\\,400$ giây).</span>""",
           """Phép tính thứ ba. Ổ đĩa cơ mất mười triệu phần tỉ giây, phóng to thành mười triệu giây. Chia cho tám mươi sáu nghìn bốn trăm giây mỗi ngày, được khoảng một trăm mười lăm phẩy bảy ngày, gần bốn tháng."""),
        st("""$$④ \\; \\frac{100\\,000}{100} = \\hl{1\\,000} \\qquad \\frac{10\\,000\\,000}{100\\,000} = \\hl{100}$$
<p>Ổ thể rắn chậm hơn bộ nhớ $1\\,000$ lần; ổ cơ chậm hơn ổ thể rắn $100$ lần.</p>""",
           """Phép tính thứ tư, so các tỉ lệ. Một trăm nghìn chia một trăm được một nghìn, nên ổ thể rắn chậm hơn bộ nhớ một nghìn lần. Mười triệu chia một trăm nghìn được một trăm, nên ổ cơ chậm hơn ổ thể rắn một trăm lần.""", clear=True),
        st(table(["đọc 1 000 lần", "tính", "tổng chờ"],
                 [["bộ nhớ", "$1\\,000 \\times 100$ ns", "<b>0,1 mili giây</b>"],
                  ["ổ thể rắn", "$1\\,000 \\times 100$ micro giây", "<b>100 mili giây</b>"],
                  ["ổ cơ", "$1\\,000 \\times 10$ mili giây", "<b>10 giây</b>"]])
           + "<span class='note'>Phép tính ⑤: lấy số lần nhân thời gian một lần, theo công thức ở bước trước.</span>",
           """Phép tính thứ năm, áp công thức tổng chờ cho một nghìn lần đọc. Bộ nhớ mất không phẩy một phần nghìn giây. Ổ đĩa thể rắn mất một trăm phần nghìn giây.
           Ổ đĩa cơ mất mười giây. Ba thiết bị cho cùng việc nhưng khác nhau tới một trăm nghìn lần.""", clear=True, focus=[1, "1.2", "1.3", "1.4", 2]),
    ], checks=["100 * 1_000 == 100_000", "100_000 // 3600 == 27 and (100_000 % 3600) // 60 == 46 and (100_000 % 3600) % 60 == 40",
               "round(10_000_000 / 86400, 1) == 115.7", "100_000 // 100 == 1000", "10_000_000 // 100_000 == 100",
               "1000 * 100 == 100_000 and 1000 * 100_000 == 100_000_000 and 1000 * 10_000_000 == 10_000_000_000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: so thẳng ổ cơ với bộ nhớ", [
        st("""<p>Đường khác: bỏ qua thang người, so thẳng ổ cơ với bộ nhớ bằng nano giây.</p>
$$\\frac{10\\,000\\,000}{100} = \\hl{100\\,000} \\text{ lần}$$
<p>Mà $1\\,000 \\times 100 = 100\\,000$ ✓ khớp với tích hai tỉ lệ ở trên.</p>""",
           """Đường kiểm khác, ta bỏ qua thang người và so thẳng ổ đĩa cơ với bộ nhớ bằng phần tỉ giây. Mười triệu chia một trăm được một trăm nghìn lần.
           Vì một nghìn nhân một trăm cũng bằng một trăm nghìn, kết quả khớp với tích hai tỉ lệ ở ví dụ trên."""),
        st("""<p>Kiểm đơn vị: $100\\,000$ giây chia $3\\,600$ ra khoảng $27{,}8$ giờ; ở đầu bài $10\\,000\\,000$ lần $\\times 10$ mili giây $= 100\\,000$ giây ✓</p>""",
           """Kiểm thêm đơn vị. Một trăm nghìn giây chia ba nghìn sáu trăm là khoảng hai mươi bảy phẩy tám giờ. Theo đầu bài, mười triệu lần nhân mười phần nghìn giây cũng ra một trăm nghìn giây, nên hai con số trùng nhau.""", clear=True),
    ], checks=["10_000_000 // 100 == 100_000 == 1000 * 100", "round(100_000 / 3600, 1) == 27.8", "10_000_000 * 10 // 1000 == 100_000"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu nhân lên: chỗ để dữ liệu quyết định", [
        st(table(["số lần đọc", "bộ nhớ", "ổ thể rắn", "ổ cơ"],
                 [["×1: 1 000", "0,1 ms", "0,1 giây", "10 giây"],
                  ["×100: 100 000", "10 ms", "10 giây", "16,7 phút"],
                  ["×10 000: 10 000 000", "1 giây", "16,7 phút", "27,8 giờ"]])
           + "<span class='note'>Số minh hoạ: 100 ns, 100 micro giây, 10 mili giây mỗi lần đọc. ms = mili giây.</span>",
           """Bảng này cho thấy điều gì xảy ra khi số lần đọc nhân lên. Ở một nghìn lần, ổ cơ mất mười giây, vẫn chịu được. Nhân một trăm lần, ổ cơ mất mười sáu phẩy bảy phút.
           Nhân mười nghìn lần, ổ cơ mất hai mươi tám giờ, còn bộ nhớ vẫn chỉ một giây. Cách cũ là cứ đọc từ ổ đĩa khi cần, và nó gãy ở quy mô lớn.""",
           focus=[1, "1.2", "1.3", "1.4", 2]),
        st("""<div class="box key"><b>Đánh đổi người làm nghề phải chọn:</b>
<ul><li>giữ dữ liệu nóng trong <b>bộ nhớ</b>: nhanh, nhưng đắt, ít chỗ, <b>mất khi tắt máy</b>;</li>
<li>đọc theo <b>khối liền nhau</b> thay vì rải rác: ít lần chờ hơn;</li>
<li>lập <b>chỉ mục</b> (mục lục) để khỏi đọc cả kho: bài về cơ sở dữ liệu quay lại ý này.</li></ul></div>""",
           """Người làm nghề phải chọn một đánh đổi. Giữ dữ liệu nóng trong bộ nhớ thì nhanh, nhưng đắt, ít chỗ và mất khi tắt máy. Đọc theo khối liền nhau thì ít lần chờ hơn.
           Lập chỉ mục, tức một cái mục lục, để khỏi đọc cả kho. Ý này sẽ quay lại ở bài về cơ sở dữ liệu.""", forward_ref=True),
    ], checks=["1000 * 10 // 1000 == 10", "100_000 * 10 // 1000 == 1000 and round(1000 / 60, 1) == 16.7",
               "round(10_000_000 * 10 / 1000 / 3600, 1) == 27.8", "10_000_000 * 100 // 1_000_000_000 == 1"])
    sc_hoc = sc("hoc", "concept", "Cách học cả bộ khoá: xem, tự làm, chấm, ôn", [
        st(svg(1500, 400,
               box(20, 120, 260, 120, ["① Xem", "một bài video"], C_BLUE, bold=True),
               arrow(285, 180, 380, 180, "#2a78d6"),
               box(390, 120, 300, 120, ["② Dừng, tự làm", "cảnh Tự làm + đề"], C_AMBER, bold=True),
               arrow(695, 180, 790, 180, "#2a78d6"),
               box(800, 120, 280, 120, ["③ Chấm", "cham.sh: ĐÚNG?"], C_GREEN, bold=True),
               arrow(1085, 180, 1180, 180, "#2a78d6"),
               box(1190, 120, 290, 120, ["④ Đánh dấu", "ở trang HOC_TAP"], C_GRAY, bold=True),
               '<path d="M1335,245 L1335,330 L150,330 L150,245" fill="none" stroke="#d97706" stroke-width="3.5" marker-end="url(#ah)"/>',
               txt(740, 318, "⑤ ôn lại sau 1 ngày, 1 tuần, 1 tháng (lịch gợi ý, số minh hoạ)", 24, "middle", "#d97706", True),
               txt(740, 385, "đáp án chỉ mở sau khi bạn đã thử ít nhất một lần", 24, "middle", "#dc2626")),
           """Đây là vòng học của cả bộ khoá. Bước một, xem một bài video. Bước hai, dừng video và tự làm cảnh Tự làm, đề nằm trong thư mục thực hành của bài.
           Bước ba, chấm bằng một lệnh, nó in đúng hoặc chỉ ra dòng khác. Bước bốn, đánh dấu bài đó ở trang học tập. Bước năm, ôn lại sau một ngày, một tuần, một tháng, đây là lịch gợi ý."""),
        st("""<div class="box key"><b>Vì sao tự làm TRƯỚC khi xem đáp án?</b> Cố nhớ lại và tự làm, kể cả làm sai, giúp nhớ lâu hơn
đọc lại hay xem lại. <span class='note'>(Roediger &amp; Karpicke, 2006: kiểm tra trí nhớ sau khi học giữ được nhiều hơn học lại.)</span></div>
<p>Xem video thụ động tạo <b>ảo giác “mình biết rồi”</b>; chỉ khi tay gõ ra kết quả bạn mới biết mình hiểu thật chưa.</p>""",
           """Vì sao phải tự làm trước khi xem đáp án? Một nghiên cứu năm hai nghìn không trăm linh sáu cho thấy người tự kiểm tra trí nhớ sau khi học giữ được nhiều hơn người chỉ học lại.
           Xem video thụ động dễ tạo ảo giác là mình biết rồi. Chỉ khi tay bạn gõ ra kết quả, bạn mới biết mình hiểu thật chưa.""", clear=True),
    ])
    sc_may2 = sc("chuanbi", "concept", "Chuẩn bị máy: bốn công cụ, một tệp kiểm", [
        st(svg(1500, 440,
               box(20, 60, 340, 150, ["① Git for Windows", "kèm cửa sổ lệnh Git Bash", "git-scm.com"], C_BLUE, bold=True),
               box(390, 60, 340, 150, ["② JDK 21 (Temurin)", "để viết và chạy Java", "adoptium.net"], C_GREEN, bold=True),
               box(760, 60, 340, 150, ["③ Python 3.11 trở lên", "đánh dấu “Add to PATH”", "python.org"], C_AMBER, bold=True),
               box(1130, 60, 350, 150, ["④ sqlite (tuỳ chọn)", "hoặc dùng labs/sqlrun.py", "sqlite.org"], C_PURPLE, bold=True),
               arrow(750, 215, 750, 285, "#475569"),
               box(250, 290, 1000, 90, "đóng rồi mở LẠI Git Bash  →  gõ  bash kiem.sh  →  sáu dòng ✔", C_GRAY, bold=True),
               txt(750, 420, "địa chỉ chính thức; không tải từ nguồn lạ", 24, "middle", "#dc2626")),
           """Máy của bạn cần bốn công cụ. Một, công cụ quản lý phiên bản, có kèm cửa sổ lệnh, tải ở địa chỉ chính thức hiện trên màn hình.
           Hai, bộ phát triển Java phiên bản hai mươi mốt. Ba, ngôn ngữ lập trình thứ hai của khoá, nhớ đánh dấu ô thêm vào đường dẫn khi cài. Bốn, bộ máy cơ sở dữ liệu nhỏ, tuỳ chọn.
           Cài xong, đóng rồi mở lại cửa sổ lệnh, gõ lệnh chạy tệp kiểm, và phải thấy sáu dấu tích."""),
        st(file_block(kiem, "kiem.sh", title="Tệp kiem.sh: chép nguyên, chưa cần hiểu từng dòng"),
           """Đây là tệp kiểm. Bạn chép nguyên vào một tệp tên kiem chấm s h, chưa cần hiểu từng dòng, vì ta sẽ học dần dần trong khoá.
           Nó hỏi máy từng công cụ có tồn tại không, rồi in dấu tích hoặc chữ báo thiếu."""),
        st(term_block(kiem, title="Chạy trong cửa sổ lệnh"),
           """Chạy tệp này, máy in sáu dòng. Mỗi dòng bắt đầu bằng dấu tích nghĩa là công cụ đó đã sẵn sàng. Dòng nào báo thiếu, bạn cài công cụ đó rồi mở lại cửa sổ lệnh và chạy lại."""),
    ])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Cài xong nhưng vẫn dùng cửa sổ lệnh <b>cũ</b> đang mở.</div>'
           + table(["cửa sổ lệnh", "mở lúc nào", "thấy công cụ vừa cài?"],
                   [["A", "trước khi cài", "<b>không</b>"], ["B", "sau khi cài", "<b>có</b>"]]),
           """Lỗi thứ nhất, của người mới, là cài xong nhưng vẫn dùng cửa sổ lệnh cũ. Cửa sổ lệnh chỉ đọc danh sách thư mục công cụ lúc nó mở.
           Công cụ cài sau sẽ không được thấy cho tới khi bạn đóng và mở lại cửa sổ."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Gõ sai tên lệnh, hoặc quên “Add to PATH” khi cài, hoặc cài nhầm bản <b>JRE</b> thay vì <b>JDK</b>.</div>'
           + term_block(loi) + "<p>JRE chỉ chạy được Java; thiếu trình biên dịch <code>javac</code>, nên không viết được chương trình.</p>",
           """Lỗi thứ hai, cũng của người mới, là gõ sai tên lệnh, hoặc quên đánh dấu ô thêm vào đường dẫn khi cài, nên máy báo không tìm thấy lệnh.
           Hoặc cài nhầm bản chỉ để chạy Java, thiếu trình biên dịch, nên không viết được chương trình. Tệp kiểm sẽ báo thiếu đúng ở dòng đó."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đo thời gian chạy hai lần rồi tin lần nhanh hơn.</div>'
           + table(["lần đo", "dữ liệu lấy từ đâu", "thời gian"],
                   [["đầu (nguội)", "ổ đĩa", "chậm"], ["sau (nóng)", "bộ nhớ, hệ điều hành đã giữ sẵn", "nhanh hơn nhiều"]]),
           """Lỗi thứ ba, của cả người đã đi làm, là đo thời gian chạy hai lần rồi tin lần nhanh hơn. Lần đầu, dữ liệu phải đọc từ ổ đĩa.
           Lần sau, hệ điều hành đã giữ sẵn trong bộ nhớ, nên nhanh hơn nhiều dù mã không đổi. Một số đo đáng tin phải nói rõ là lần nguội hay lần nóng."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Một chương trình cần đọc <b>200 000</b> bản ghi nhỏ, mỗi bản ghi chỉ đọc <b>một lần</b>, từ ổ thể rắn ($100$ micro giây mỗi lần).</p>
<ol><li>Cách A: đọc từng bản ghi từ ổ. Tổng chờ?</li>
<li>Cách B: nạp cả kho vào bộ nhớ trước (mất $2$ giây), rồi đọc $200\\,000$ lần ở bộ nhớ ($100$ ns mỗi lần). Tổng?</li>
<li>Nếu chỉ cần <b>20</b> bản ghi thì chọn cách nào, vì sao?</li></ol>""",
           """Bây giờ tới phần bạn tự làm. Một chương trình đọc hai trăm nghìn bản ghi nhỏ, mỗi bản ghi chỉ đọc một lần, từ ổ đĩa thể rắn, một trăm phần triệu giây mỗi lần.
           Câu một, cách A đọc từng bản ghi từ ổ, tổng chờ bao nhiêu. Câu hai, cách B nạp cả kho vào bộ nhớ trước, mất hai giây, rồi đọc ở bộ nhớ, tổng bao nhiêu.
           Câu ba, nếu chỉ cần hai mươi bản ghi thì chọn cách nào, vì sao. Hãy dừng video và tính.""", pause=30),
        st("""<p><b>Câu 1.</b> Cách A:</p>
$$200\\,000 \\times 100\\ \\text{micro giây} = 20\\,000\\,000\\ \\text{micro giây} = \\hl{20\\ \\text{giây}}$$
<p><b>Câu 2.</b> Cách B: nạp $2$ giây, rồi đọc ở bộ nhớ:</p>
$$200\\,000 \\times 100\\ \\text{ns} = 0{,}02\\ \\text{giây} \\;\\Rightarrow\\; 2 + 0{,}02 = \\hl{2{,}02\\ \\text{giây}}$$""",
           """Đáp án câu một, cách A, hai trăm nghìn nhân một trăm phần triệu giây là hai mươi triệu phần triệu giây, tức hai mươi giây.
           Câu hai, cách B, nạp mất hai giây, rồi đọc ở bộ nhớ hai trăm nghìn nhân một trăm phần tỉ giây là hai mươi triệu phần tỉ giây, tức không phẩy không hai giây. Tổng là hai phẩy không hai giây, nhanh hơn gần mười lần."""),
        st("""<p><b>Câu 3.</b> Cách A với 20 bản ghi: $20 \\times 100$ micro giây $= 2$ mili giây. Cách B vẫn mất ít nhất $2$ giây để nạp.</p>
<div class="box key">Chỉ cần ít bản ghi thì <b>cách A thắng</b> ($2$ mili giây so với hơn $2$ giây). Nạp trước chỉ có lợi khi số lần đọc đủ lớn để bù chi phí nạp.</div>""",
           """Câu ba, với hai mươi bản ghi, cách A mất hai phần nghìn giây, còn cách B vẫn mất ít nhất hai giây chỉ để nạp. Vậy khi chỉ cần ít bản ghi, cách A thắng.
           Nạp trước chỉ có lợi khi số lần đọc đủ lớn để bù chi phí nạp, và đó là một quyết định người làm nghề phải tính trước.""", clear=True),
    ], checks=["200_000 * 100 // 1_000_000 == 20", "200_000 * 100 / 1e9 == 0.02", "round(2 + 200_000 * 100 / 1e9, 2) == 2.02",
               "20 * 100 / 1000 == 2.0", "round(20 / 2.02, 1) == 9.9"])
    sc_prac = practice_scene(sc, "Tự làm: cài đủ công cụ, chấm bằng tệp kiểm", pr_steps(
        st, "FND", "L00",
        """<p><b>Đề</b>: máy của bạn phải có đủ công cụ của khoá.</p>
<ol><li>Cài Git for Windows, JDK 21, Python 3.11+, rồi <b>mở lại</b> Git Bash.</li>
<li>Tạo tệp <code>kiem.sh</code> với đúng nội dung ở cảnh trước (chép nguyên).</li>
<li>Chạy <code>bash kiem.sh</code> trong thư mục chứa tệp: cần <b>sáu dòng ✔</b>.</li></ol>
<p class="note">Dòng nào báo THIEU: cài công cụ đó, mở lại Git Bash, chạy lại.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Cài công cụ quản lý phiên bản kèm cửa sổ lệnh, bộ phát triển Java hai mươi mốt, ngôn ngữ thứ hai của khoá, rồi mở lại cửa sổ lệnh.
        Tạo tệp kiểm với đúng nội dung ở cảnh trước, chạy nó trong thư mục chứa tệp, và cần thấy sáu dấu tích. Hãy dừng video và làm.""",
        KIEM_OUT, "kiem.sh",
        """<div class="box key"><b>Nếu kẹt:</b> dòng THIEU python: có thể bạn chưa đánh dấu “Add to PATH”, hoặc máy mở cửa hàng ứng dụng thay cho Python; cài lại từ python.org.
Dòng THIEU javac: bạn cài bản JRE; hãy cài JDK. Lời giải ở <code>labs/FND/L00/loi_giai.sh</code>; chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, dòng báo thiếu ngôn ngữ thứ hai thường nghĩa là bạn chưa đánh dấu ô thêm vào đường dẫn. Cũng có thể máy mở cửa hàng ứng dụng thay cho nó, nên hãy cài lại từ địa chỉ chính thức.
        Dòng báo thiếu trình biên dịch Java nghĩa là bạn cài nhầm bản chỉ để chạy, hãy cài bộ phát triển đầy đủ. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=120), "FND", "L00")
    write_lab("FND", "L00", """# Lab FND L00 — Kiểm máy bằng một tệp lệnh

Cài đủ công cụ theo bài (Git for Windows kèm Git Bash, JDK 21, Python 3.11+, sqlite hoặc dùng `labs/sqlrun.py`), **mở lại** Git Bash.

1. Tạo tệp `kiem.sh` với nội dung dưới đây (chép nguyên; bài L04 sẽ giải thích từng dòng):

```bash
""" + KIEM + """
```

2. Chạy `bash kiem.sh`. Máy đạt khi in **đúng sáu dòng**, mỗi dòng bắt đầu bằng ✔ (xem `mong_doi.txt`).
3. Chấm: `bash labs/cham.sh FND L00 kiem.sh`. Dòng báo THIEU nghĩa là thiếu công cụ đó: cài, mở lại Git Bash, chạy lại.

Muốn xem phiên bản từng công cụ: `bash labs/check_env.sh`.
""", "sh", KIEM, KIEM_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic, tư duy và bản đồ khoá", [
        st(chain("tệp trên ổ đĩa", "nạp vào bộ nhớ", "bộ xử lý làm từng lệnh", "tổng chờ = số lần × thời gian một lần",
                 "học: xem → tự làm → chấm → ôn", "máy: kiểm bằng tệp kiem.sh"),
           """Tổng kết chuỗi logic. Chương trình nằm ở ổ đĩa, được nạp vào bộ nhớ, và bộ xử lý làm từng lệnh.
           Tổng chờ bằng số lần nhân thời gian một lần, nên chỗ để dữ liệu quyết định tốc độ. Cách học là xem, tự làm, chấm, ôn. Và máy sẵn sàng khi tệp kiểm in sáu dấu tích."""),
        st(table(["bài", "nội dung", "bạn làm được"],
                 [["L01–L02", "cửa sổ lệnh, thư mục, tệp", "đi quanh máy và dựng cây thư mục bằng chữ"],
                  ["L03–L04", "lọc văn bản, chương trình và PATH", "ghép lệnh bằng ống, chạy tệp lệnh"],
                  ["L05–L06", "trình soạn mã, đọc lỗi, CSV/JSON/YAML", "sửa lỗi theo thông báo, đọc dữ liệu có cấu trúc"],
                  ["L07–L08", "HTTP và SQL", "hỏi một máy chủ bằng chữ, hỏi một bảng bằng chữ"],
                  ["L09–L10", "phiên bản và dự án nhỏ", "nối mọi thứ thành sổ tay giao dịch"]])
           + "<div class='box key'><b>Tư duy:</b> trước khi viết gì, hỏi dữ liệu nằm ở đâu và sẽ bị đọc mấy lần.</div>",
           """Đây là bản đồ mười bài tiếp theo của khoá. Hai bài đầu dạy cửa sổ lệnh, thư mục và tệp. Hai bài tiếp theo dạy lọc văn bản, chương trình và đường dẫn.
           Hai bài nữa dạy trình soạn mã, đọc thông báo lỗi và các dạng dữ liệu có cấu trúc. Rồi tới giao thức HTTP và ngôn ngữ SQL. Hai bài ở cuối khoá dạy quản lý phiên bản và một dự án nhỏ nối mọi thứ.
           Điều cần mang theo, trước khi viết gì, hãy hỏi dữ liệu nằm ở đâu và sẽ bị đọc mấy lần.""", forward_ref=True,
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", 2]),
    ])
    return lesson("L00", "may_tinh_va_cach_hoc", "Bài 0 — Máy tính chạy chương trình thế nào, cách học và chuẩn bị máy",
                  "curriculum/fnd.yaml L00; audit/fnd/verify_fnd.py L00 (Git Bash chạy thật tệp kiem.sh); labs/ENV.md; "
                  "Hennessy & Patterson, Computer Architecture: A Quantitative Approach (phân cấp bộ nhớ: bộ nhớ, ổ đĩa; số trong bài là số minh hoạ bậc độ lớn); "
                  "Roediger & Karpicke 2006, Test-enhanced learning, Psychological Science 17(3) (NOT_VERIFIED: trích theo trí nhớ, chưa mở lại nguyên văn); "
                  "địa chỉ cài đặt: git-scm.com, adoptium.net, python.org, sqlite.org",
                  ["Mô tả đường đi của chương trình từ ổ đĩa vào bộ nhớ tới bộ xử lý làm từng lệnh",
                   "Chạy tay chương trình ba lệnh và ghi bộ nhớ sau mỗi lệnh",
                   "Tính tổng thời gian chờ bằng số lần nhân thời gian một lần, ở ba quy mô dữ liệu",
                   "Kể bốn bước của vòng học và giải thích vì sao tự làm trước khi xem đáp án",
                   "Cài các công cụ của khoá và kiểm máy bằng tệp lệnh in dấu tích cho từng công cụ"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_may, sc_form, sc_ex, sc_chk, sc_scale, sc_hoc, sc_may2, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "intuition"), (2, "ex_may"), (3, "example"), (4, "hoc"), (5, "practice")])
