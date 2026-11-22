from lib import *
from labkit import write_lab, practice_steps, practice_scene

KIEM = r"""dat() {
  v=$("$1" --version 2>/dev/null | grep -oE '[0-9.]+' | head -1)
  nho=$(printf '%s\n%s\n' "$2" "$v" | sort -V | head -1)
  if [ "$nho" = "$2" ]; then echo "✔ $1"; else echo "THIEU $1"; fi
}
dat bash 4.0
dat git 2.28
dat javac 21
dat java 21
dat python 3.11
dat sqlite3 3.32"""
KIEM_OUT = "✔ bash\n✔ git\n✔ javac\n✔ java\n✔ python\n✔ sqlite3"


def build():
    kiem = cmd("KiemMay", [("bash kiem.sh", KIEM_OUT)], files={"kiem.sh": KIEM + "\n"})
    loi = cmd("GoSai", [("pyton --version", "bash: pyton: command not found")])
    # kiểm tệp kiem.sh KHÔNG bị lừa: lối tắt cửa hàng ứng dụng của Python (có tên trong PATH nhưng không chạy) và bản Git quá cũ đều phải ra THIEU
    cmd("KiemStub", [("PATH=\"$HOME/stub:$PATH\" bash kiem.sh | grep -E 'git|python'", "THIEU git\nTHIEU python"),
                     ("PATH=\"$HOME/stub:$PATH\" python --version 2>&1 | head -c 20", "Python was not found")],
        files={"kiem.sh": KIEM + "\n",
               "stub/python": "#!/bin/sh\necho 'Python was not found; run without arguments to install from the Microsoft Store.' >&2\nexit 49\n",
               "stub/git": "#!/bin/sh\necho 'git version 2.25.1.windows.1'\n"})

    sc_hook = sc("hook", "hook", "Cùng một chương trình: chờ mười giây hay gần hai mươi tám giờ?", [
        st(table(["số lần đọc", "mỗi lần chờ", "tổng chờ"],
                 [["1 000", "10 mili giây", "<b>10 giây</b>"], ["10 000 000", "10 mili giây", "<b>100 000 giây</b>, gần 28 giờ"]])
           + "<p>Chương trình đọc các <b>bản ghi</b> (mỗi bản ghi là một mẩu dữ liệu nhỏ, như một dòng của sổ) nằm rải rác trên <b>ổ đĩa cơ</b> "
             "(HDD: đĩa kim loại quay, đầu đọc phải di chuyển nên chậm). Số minh hoạ. Cùng cách viết; chỉ khác "
             "<b>dữ liệu nằm ở đâu</b> và <b>có bao nhiêu</b>.</p>",
           """Chào bạn, hãy nhìn một chương trình đọc các bản ghi nhỏ nằm rải rác trên ổ đĩa cơ, mỗi lần chờ chừng mười phần nghìn giây, đây là số minh hoạ.
           Bản ghi là một mẩu dữ liệu nhỏ, như một dòng của sổ, còn ổ đĩa cơ có đĩa kim loại quay và đầu đọc phải di chuyển nên chậm.
           Một nghìn lần là mười giây. Nhưng mười triệu lần là một trăm nghìn giây, gần hai mươi tám giờ.
           Cùng chương trình, cùng cách viết, chỉ khác dữ liệu nằm ở đâu và có bao nhiêu.""", focus=[1, 2, "1.2", "1.3", 2]),
        st("""<div class="box key">Hôm nay, bài mở đầu của cả lộ trình, ta trả lời ba câu hỏi:
<ol><li>Máy tính <b>chạy</b> một chương trình thế nào, và vì sao chỗ để dữ liệu quyết định tốc độ?</li>
<li>Bạn nên <b>học</b> cả bộ khoá này theo cách nào để nhớ lâu?</li>
<li>Máy của bạn cần <b>cài</b> những gì, và kiểm bằng cách nào?</li></ol></div>""",
           """Hôm nay là bài mở đầu, ta trả lời ba câu hỏi. Máy tính chạy một chương trình thế nào, và vì sao chỗ để dữ liệu quyết định tốc độ.
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
                  ["<b>ổ đĩa</b>", "lưu tệp lâu dài; chậm hơn bộ nhớ nhiều; có hai loại: <b>ổ cơ</b> (HDD, đĩa quay, chậm hơn) và <b>ổ thể rắn</b> (SSD, chip nhớ, nhanh hơn)", "tủ hồ sơ ở phòng bên"],
                  ["<b>hệ điều hành</b>", "chương trình điều phối: nạp tệp vào bộ nhớ, chia việc", "quản lý toà nhà"],
                  ["<b>cửa sổ lệnh</b>", "khung chữ: bạn gõ lệnh, máy trả lời bằng chữ", "quầy giao dịch bằng lời"],
                  ["<b>✔</b>", "dấu tích: đạt; dùng khi kiểm máy", "dấu tích của giáo viên"]]),
           """Bảng này giải mã năm bộ phận và một dấu hiệu. Bộ xử lý làm từng lệnh nhỏ rất nhanh, giống người thu ngân bấm máy tính.
           Bộ nhớ giữ dữ liệu đang dùng, tắt máy là mất, giống tờ giấy nháp. Ổ đĩa lưu tệp lâu dài nhưng chậm hơn nhiều, giống tủ hồ sơ ở phòng bên; loại có đĩa quay gọi là ổ cơ, loại dùng chip nhớ gọi là ổ thể rắn và nhanh hơn.
           Hệ điều hành là chương trình điều phối, nạp tệp vào bộ nhớ và chia việc. Cửa sổ lệnh là khung chữ để bạn gõ lệnh. Dấu tích nghĩa là đạt.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: đường đi của một chương trình", [
        st(svg(1500, 440,
               box(20, 140, 300, 135, ["ổ đĩa", "tệp chương trình", "chậm, rất nhiều chỗ"], C_GRAY, bold=True),
               arrow(325, 207, 470, 207, "#2a78d6", "① nạp"),
               box(480, 140, 310, 135, ["bộ nhớ (RAM)", "dữ liệu đang chạy", "nhanh, ít chỗ hơn"], C_AMBER, bold=True),
               arrow(795, 207, 940, 207, "#16a34a", "② đọc lệnh"),
               box(950, 140, 260, 135, ["bộ xử lý (CPU)", "xử lý cực nhanh", "chỉ giữ vài ô đang làm"], C_GREEN, bold=True),
               arrow(1215, 207, 1345, 207, "#16a34a", "③ xuất"),
               box(1355, 140, 130, 135, ["màn", "hình"], C_BLUE),
               box(480, 20, 730, 70, "hệ điều hành điều phối cả ba bước", C_PURPLE, bold=True),
               arrow(845, 95, 635, 135, "#9333ea"),
               '<line x1="20" y1="302" x2="1210" y2="302" stroke="#475569" stroke-width="2.5" stroke-dasharray="10 6"/>',
               txt(615, 346, "3 tầng đầu (ổ đĩa → bộ nhớ → trong CPU): nhanh và đắt hơn theo dung lượng, nhưng sức chứa nhỏ dần", 21, "middle", "#1f2937", True),
               txt(750, 396, "màn hình chỉ hiển thị kết quả — bộ nhớ nhỏ hơn ổ đĩa, nên số lần quay về ổ đĩa quyết định tốc độ", 22, "middle", "#dc2626")),
           """Hình này là đường đi của một chương trình. Bước một, hệ điều hành nạp tệp chương trình từ ổ đĩa vào bộ nhớ, vì bộ xử lý không đọc thẳng được từ ổ đĩa.
           Bước hai, bộ xử lý đọc từng lệnh từ bộ nhớ và làm việc cực nhanh với vài ô nhớ đang xử lý ngay bên trong nó. Bước ba, kết quả hiện ra màn hình hoặc được ghi lại vào tệp.
           Xét riêng ba tầng từ ổ đĩa sang bộ nhớ rồi tới các ô bên trong bộ xử lý. Đi tới đâu thì nhanh hơn và đắt hơn trên mỗi đơn vị dung lượng tới đó, nhưng sức chứa lại nhỏ dần.
           Màn hình ở cuối chỉ dùng để hiển thị kết quả. Bộ nhớ không rộng như ổ đĩa nên không thể ôm hết mọi tệp, vì vậy số lần phải quay về đọc ổ đĩa sẽ quyết định chương trình nhanh hay chậm."""),
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
           """Bảng này cho thấy bộ nhớ sau từng lệnh. Sau lệnh ba, ô hai giữ năm, vì hai cộng ba bằng năm.
           Mọi chương trình, dù lớn đến đâu, đều là hàng triệu việc nhỏ như vậy.""",
           clear=True, focus=[1, "1.4", 2]),
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
           """Bước hai, muốn so hai thiết bị, ta phải đổi về cùng một đơn vị. Mỗi bậc đơn vị gấp một nghìn lần bậc dưới, nên một phần nghìn giây bằng một nghìn phần triệu giây, và bằng một triệu phần tỉ giây."""),
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
           """Phép tính thứ hai. Ổ đĩa thể rắn mất một trăm nghìn phần tỉ giây, phóng to thành một trăm nghìn giây. Chia cho ba nghìn sáu trăm giây mỗi giờ được hai mươi bảy giờ, dư hai nghìn tám trăm giây, tức bốn mươi sáu phút bốn mươi giây."""),
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
    ], checks=["10_000_000 // 100 == 100_000 == 1000 * 100"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu nhân lên: chỗ để dữ liệu quyết định", [
        st(table(["số lần đọc", "bộ nhớ", "ổ thể rắn", "ổ cơ"],
                 [["×1: 1 000", "0,1 ms", "0,1 giây", "10 giây"],
                  ["×100: 100 000", "10 ms", "10 giây", "16,7 phút"],
                  ["×10 000: 10 000 000", "1 giây", "16,7 phút", "27,8 giờ"]])
           + "<span class='note'>Số minh hoạ: 100 ns, 100 micro giây, 10 mili giây mỗi lần đọc. ms = mili giây.</span>",
           """Bảng này cho thấy điều gì xảy ra khi số lần đọc nhân lên. Ở một nghìn lần, ổ cơ mất mười giây, vẫn chịu được. Nhân một trăm lần, ổ cơ mất mười sáu phẩy bảy phút.
           Nhân mười nghìn lần, ổ cơ mất hai mươi tám giờ, còn bộ nhớ vẫn chỉ một giây.""",
           focus=[1, "1.2", "1.3", "1.4"]),
        st("""<div class="box key"><b>Đánh đổi người làm nghề phải chọn:</b>
<ul><li>giữ dữ liệu nóng trong <b>bộ nhớ</b>: nhanh, nhưng giá theo dung lượng đắt hơn, chứa được ít hơn ổ đĩa và <b>mất khi tắt máy</b>;</li>
<li>đọc theo <b>khối liền nhau</b> thay vì rải rác: ít lần chờ hơn;</li>
<li>lập <b>chỉ mục</b> (mục lục) để khỏi đọc cả kho: bài về cơ sở dữ liệu quay lại ý này.</li></ul></div>""",
           """Người làm nghề phải chọn một đánh đổi. Giữ dữ liệu nóng trong bộ nhớ thì nhanh, nhưng đắt theo dung lượng, sức chứa nhỏ hơn ổ đĩa và mất khi tắt máy. Đọc theo khối liền nhau thì ít lần chờ hơn.
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
        st("""<div class="box key"><b>Vì sao tự làm TRƯỚC khi xem đáp án?</b> Tự kiểm tra và tự làm, kể cả làm sai, giúp nhớ <b>lâu</b> hơn là chỉ đọc lại hay xem lại.
<span class='note'>(Roediger &amp; Karpicke, 2006: kiểm tra sau <b>5 phút</b> thì học lại còn nhỉnh hơn; kiểm tra sau <b>2 ngày và 1 tuần</b> thì người tự kiểm tra giữ được nhiều hơn.)</span></div>
<p>Xem video thụ động tạo <b>ảo giác “mình biết rồi”</b>; chỉ khi tay gõ ra kết quả bạn mới biết mình hiểu thật chưa.</p>""",
           """Vì sao phải tự làm trước khi xem đáp án? Một nghiên cứu năm hai nghìn không trăm linh sáu cho thấy kiểm tra sau năm phút thì học lại còn nhỉnh hơn. Nhưng sau hai ngày và một tuần thì người tự kiểm tra giữ được nhiều hơn.
           Xem video thụ động dễ tạo ảo giác là mình biết rồi. Chỉ khi tay bạn gõ ra kết quả, bạn mới biết mình hiểu thật chưa.""", clear=True),
    ])
    demo = cmd("DemoEcho", [("echo xin chao", "xin chao")])
    sc_may2 = sc("chuanbi", "concept", "Chuẩn bị máy: cửa sổ lệnh và bốn công cụ", [
        st(table(["tên", "nghĩa"],
                 [["<b>vỏ lệnh</b> (shell)", "chương trình nhận chữ bạn gõ rồi bảo máy làm: bạn gõ một dòng, nhấn phím <b>Enter</b>, máy làm và trả lời"],
                  ["<b>bash</b>", "tên một loại vỏ lệnh, phổ biến nhất trên máy chủ"],
                  ["<b>Git Bash</b>", "cửa sổ gõ lệnh trên Windows, đi kèm khi cài Git for Windows; bên trong nó chạy bash"],
                  ["<b>.sh</b>", "đuôi tên <b>tệp lệnh</b> viết cho bash; <code>bash kiem.sh</code> nghĩa là nhờ bash chạy các lệnh ghi trong tệp <code>kiem.sh</code>"]]),
           """Vỏ lệnh là chương trình nhận chữ bạn gõ rồi bảo máy làm: bạn gõ một dòng, nhấn phím xuống dòng, và máy trả lời.
           Một loại vỏ lệnh phổ biến có tên là b a s h. Cửa sổ gõ lệnh đi kèm công cụ ghi phiên bản chạy vỏ lệnh đó bên trong.
           Tệp lệnh viết cho nó thường có đuôi chấm s h, và gõ tên vỏ lệnh rồi tên tệp là nhờ nó chạy các lệnh trong tệp ấy.""", introduces=["fnd_bash"]),
        st(term_block(demo, title="Ví dụ nhỏ: gõ lệnh, nhấn Enter, máy trả lời")
           + "<p class='note'>Dòng có dấu " + code("$") + " ở đầu là dòng <b>bạn gõ</b>; <code>echo</code> in lại đúng chữ đứng sau nó; dòng bên dưới là máy trả lời.</p>",
           """Ví dụ nhỏ. Lệnh in chữ có tên là e c h o, và nó in lại đúng chữ đứng sau nó. Dòng có dấu đô la ở đầu là dòng bạn gõ, còn dòng bên dưới là máy trả lời.""", clear=True),
        st(svg(1500, 440,
               box(20, 60, 340, 150, ["① Git for Windows", "kèm cửa sổ lệnh Git Bash", "git-scm.com"], C_BLUE, bold=True),
               box(390, 60, 340, 150, ["② JDK 21 (Temurin)", "để viết và chạy Java", "adoptium.net"], C_GREEN, bold=True),
               box(760, 60, 340, 150, ["③ Python 3.11 trở lên", "đánh dấu “Add to PATH”", "python.org"], C_AMBER, bold=True),
               box(1130, 60, 350, 150, ["④ sqlite3", "bắt buộc: phần SQL dùng", "sqlite.org"], C_PURPLE, bold=True),
               arrow(750, 215, 750, 285, "#475569"),
               box(250, 290, 1000, 90, "đóng rồi mở LẠI Git Bash  →  gõ  bash kiem.sh  →  sáu dòng ✔", C_GRAY, bold=True),
               txt(750, 420, "địa chỉ chính thức; không tải từ nguồn lạ", 24, "middle", "#dc2626"))
           + "<p class='note'><b>Git</b> ghi lại các phiên bản của một dự án; <b>Java</b>, <b>Python</b> là ngôn ngữ lập trình (cách viết chỉ dẫn cho máy); <b>SQL</b> là ngôn ngữ hỏi dữ liệu trong bảng. "
             "<b>PATH</b> là danh sách thư mục mà cửa sổ lệnh tìm công cụ khi bạn gõ tên; ô “Add to PATH” khi cài là đưa công cụ vào danh sách đó. "
             "Mức thấp nhất: Git 2.28, Java 21, Python 3.11, sqlite3 3.32.</p>",
           """Máy của bạn cần bốn công cụ. Một, công cụ ghi lại các phiên bản của một dự án, kèm cửa sổ lệnh vừa nói. Hai, bộ phát triển Java phiên bản hai mươi mốt; Java là một ngôn ngữ lập trình, tức một cách viết chỉ dẫn cho máy.
           Ba, Python, ngôn ngữ lập trình thứ hai của khoá. Bốn, chương trình cơ sở dữ liệu nhỏ, bắt buộc, vì phần ngôn ngữ SQL, tức ngôn ngữ hỏi dữ liệu trong bảng, dùng đến nó.
           Danh sách đường dẫn là danh sách thư mục mà cửa sổ lệnh tìm công cụ khi bạn gõ tên.""", clear=True),
    ])
    sc_caidat = sc("caidat", "concept", "Cài đặt từng bước: Git, JDK, Python, sqlite3", [
        st(table(["màn hình của trình cài", "việc làm"],
                 [["trang <code>git-scm.com</code>", "bấm tải Git for Windows bản 64-bit (tệp <code>Git-….-64-bit.exe</code>), rồi chạy tệp vừa tải"],
                  ["<b>Select Components</b>", "giữ ô <b>Windows Explorer integration</b>, trong đó có <b>Open Git Bash here</b>"],
                  ["<b>Adjusting your PATH environment</b>", "giữ mục có ghi <b>Recommended</b>; mục <b>Use Git from Git Bash only</b> cũng đủ cho khoá này"],
                  ["các màn hình còn lại", "giữ mặc định, bấm <b>Next</b>; cuối cùng <b>Install</b>, đợi xong, bấm <b>Finish</b>"]])
           + "<p class='note'><b>① Cài Git for Windows</b> (giao diện có thể khác nhẹ theo phiên bản)</p>",
           """Bước một là cài công cụ ghi phiên bản. Tải ở địa chỉ chính thức, chạy tệp vừa tải, và giữ lựa chọn mặc định ở hầu hết màn hình.
           Hai màn hình đáng liếc là danh sách thành phần, nơi nên giữ mục mở cửa sổ lệnh tại một thư mục, và màn hình chỉnh đường dẫn, nơi nên giữ mục được ghi là nên chọn."""),
        st("""<div class="box key"><b>Mở Git Bash và thử:</b> <span class='note'>(giao diện có thể khác nhẹ theo phiên bản)</span>
<ol><li>Bấm <b>Start</b>, gõ <code>Git Bash</code>, nhấn <b>Enter</b>: một cửa sổ chữ hiện ra, chờ bạn gõ.</li>
<li>Gõ <code>git --version</code>, nhấn <b>Enter</b>: máy in một dòng <code>git version 2.…</code>; từ bản 2.28 trở lên là đạt.</li></ol></div>""",
           """Bây giờ mở cửa sổ lệnh: bấm vào nút mở danh sách chương trình ở góc dưới màn hình, gõ tên cửa sổ đó, rồi nhấn phím xuống dòng.
           Gõ lệnh hỏi phiên bản của công cụ ghi phiên bản; máy in tên và số phiên bản, từ hai chấm hai mươi tám trở lên là đạt.""", clear=True),
        st("""<div class="box key"><b>Máy bạn là x64 hay ARM?</b> <b>x64</b> là loại chip 64-bit của Intel và AMD, có ở hầu hết máy Windows; <b>ARM</b> là loại chip khác, hiếm hơn.
<ol><li>Bấm <b>Start</b>, gõ <code>System Information</code>, nhấn <b>Enter</b>.</li>
<li>Đọc dòng <b>System Type</b>: <code>x64-based PC</code> là x64; ghi <code>ARM64-based PC</code> thì ở trang tải chọn bản <b>aarch64</b> thay cho x64.</li></ol></div>""",
           """Trước khi tải bộ phát triển Java, hãy biết máy mình dùng loại chip nào. Kiến trúc x sáu mươi bốn là loại chip sáu mươi bốn bit của hầu hết máy tính cá nhân, loại khác tên là a r m. Mở thông tin hệ thống, đọc dòng loại hệ thống; nếu ghi a r m sáu mươi bốn thì ở trang tải chọn bản dành cho nó.""", clear=True),
        st(table(["bước", "việc làm"],
                 [["trang <code>adoptium.net</code>", "chọn <b>Temurin 21 (LTS)</b> (<b>LTS</b> = bản hỗ trợ dài hạn, được vá lỗi nhiều năm), hệ điều hành <b>Windows</b>, kiến trúc <b>x64</b>, loại <b>JDK</b> (không phải JRE); tải tệp <code>.msi</code>"],
                  ["màn hình <b>Custom Setup</b>", "bảo đảm ô <b>Add to PATH</b> được chọn (thường đã chọn sẵn); bấm <b>Next</b>, <b>Install</b>, <b>Finish</b>"],
                  ["kiểm", "mở một Git Bash <b>mới</b>, gõ <code>java -version</code> (chương trình chạy Java) rồi <code>javac -version</code> (<b>trình biên dịch</b>: chương trình dịch mã Java sang dạng máy chạy được): cả hai in số bắt đầu bằng <code>21</code>"]])
           + "<p class='note'><b>② Cài JDK 21 (Temurin)</b> (giao diện có thể khác nhẹ theo phiên bản)</p>",
           """Bước hai là bộ phát triển Java hai mươi mốt. Chọn bản có chữ L T S, nghĩa là hỗ trợ dài hạn. Chọn hệ điều hành của bạn, kiến trúc vừa biết, loại bộ phát triển đầy đủ chứ không phải loại chỉ để chạy, rồi tải tệp đuôi m s i.
           Khi cài, giữ ô thêm vào danh sách đường dẫn. Sau đó mở cửa sổ lệnh mới và hỏi phiên bản của chương trình chạy Java và của trình biên dịch. Trình biên dịch là chương trình dịch mã Java sang dạng máy chạy được. Cả hai phải in số hai mươi mốt.""", clear=True),
        st("""<div class="box key"><b>③ Cài Python 3.11 trở lên</b> <span class='note'>(giao diện có thể khác nhẹ theo phiên bản)</span>
<ol><li>Vào <code>python.org/downloads/windows</code>, chọn một bản Python 3.13 (hoặc từ 3.11 trở lên), tệp <b>Windows installer (64-bit)</b>.</li>
<li>Chạy tệp tải về. Ở màn hình <b>đầu tiên</b>, <b>tích ô <code>Add python.exe to PATH</code></b> (nằm dưới cùng), rồi bấm <b>Install Now</b>.</li>
<li>Mở một Git Bash <b>mới</b>, gõ <code>python --version</code>: in <code>Python 3.…</code>, từ 3.11 trở lên là đạt.</li></ol></div>
<p class="note">Nếu trang chỉ đưa <b>Python install manager</b> (trình cài kiểu mới), cài nó theo hướng dẫn trên trang; đích vẫn là <code>python --version</code> trong Git Bash in từ 3.11. Nếu gõ <code>python</code> mà Windows mở cửa hàng ứng dụng, hoặc báo “Python was not found”, là Python chưa cài đúng: xem cảnh lỗi hay gặp.</p>""",
           """Bước ba là Python, ngôn ngữ lập trình thứ hai, từ phiên bản ba chấm mười một trở lên. Tải tệp cài đặt sáu mươi bốn bit, ở màn hình đầu tiên tích ô thêm vào danh sách đường dẫn, rồi bấm cài ngay.
           Mở cửa sổ lệnh mới và hỏi phiên bản, cần thấy ba chấm mười một trở lên. Nếu trang chỉ đưa trình cài kiểu mới, cài nó theo trang hướng dẫn.""", clear=True),
        st("""<div class="box key"><b>④ Cài sqlite3 trên Windows (không cần quyền quản trị):</b>
<ol><li>Vào <code>sqlite.org/download.html</code>, mục <b>Precompiled Binaries for Windows</b>, tải tệp <code>sqlite-tools-win-x64-….zip</code>.</li>
<li>Giải nén (chuột phải, <b>Extract All</b>): có tệp <code>sqlite3.exe</code>.</li>
<li>Trong thư mục cá nhân của bạn (<code>C:/Users/tên_bạn</code>) tạo thư mục tên <code>bin</code>, chép <code>sqlite3.exe</code> vào đó.</li>
<li>Mở <b>LẠI</b> Git Bash, gõ <code>sqlite3 --version</code>: thấy số phiên bản bắt đầu bằng <code>3</code> là xong.</li></ol></div>
<p class="note">Git Bash tự đưa thư mục <code>bin</code> trong thư mục cá nhân vào danh sách tìm lệnh mỗi khi mở.</p>""",
           """Bước bốn, chương trình cơ sở dữ liệu, cài theo bốn việc và không cần quyền quản trị. Một, vào trang chính thức, tải tệp nén dựng sẵn cho hệ điều hành này. Hai, giải nén, bạn có một tệp chạy đuôi e x e.
           Ba, trong thư mục cá nhân của bạn, tạo một thư mục tên bin và chép tệp đó vào. Bốn, mở lại cửa sổ lệnh, gõ lệnh hỏi phiên bản, và thấy số bắt đầu bằng ba là xong.""", clear=True),
    ])
    sc_kiem = sc("kiemsh", "concept", "Tệp kiểm kiem.sh: tạo, chép và chạy", [
        st("""<div class="box key"><b>Tạo tệp kiem.sh và chạy nó:</b>
<ol><li>Mở một <b>trình soạn mã</b> (chương trình sửa chữ thuần): Visual Studio Code, tải ở <code>code.visualstudio.com</code>. Không dùng Word.</li>
<li>Dán nội dung tệp kiểm, chép từ <code>labs/FND/L00/de.md</code>. Dấu ✔ chép dán, không gõ bằng bàn phím.</li>
<li>Lưu (<b>Save As</b>) với tên <code>kiem.sh</code> vào thư mục gốc của bộ khoá: thư mục chứa thư mục <code>labs</code>.</li>
<li>Trong cửa sổ quản lý tệp, mở thư mục đó, chuột phải vào chỗ trống, chọn <b>Open Git Bash here</b> (Windows 11: bấm <b>Show more options</b> trước).</li>
<li>Gõ <code>bash kiem.sh</code>, nhấn Enter.</li></ol></div>
<p class="note">Cửa sổ lệnh mở đúng thư mục chứa tệp nên chưa cần lệnh đổi thư mục; ta sẽ học lệnh đó sau.</p>""",
           """Bây giờ tạo tệp kiểm. Mở một trình soạn mã, tức chương trình sửa chữ thuần, không dùng chương trình soạn văn bản có định dạng. Dán nội dung tệp kiểm chép từ tệp đề bài; dấu tích phải chép và dán, vì bàn phím thường không gõ được.
           Lưu với tên kiem chấm s h vào thư mục gốc của bộ khoá, rồi chuột phải vào chỗ trống trong thư mục đó và chọn mở cửa sổ lệnh tại đây."""),
        st(file_block(kiem, "kiem.sh", title="Tệp kiem.sh: chép nguyên vào tệp"),
           """Đây là tệp kiểm, bạn chép nguyên vào tệp tên kiem chấm s h. Nó chạy thật từng công cụ để hỏi phiên bản, rồi in dấu tích hoặc chữ báo thiếu.
           Bạn có thể dừng video để chép, chưa hiểu hết cũng đừng lo. Ta đọc từng phần của nó ngay sau đây.""", pause=40),
        st(table(["phần của tệp", "nghĩa"],
                 [[code('dat() { … }'), "đặt tên <code>dat</code> cho một nhóm lệnh để gọi lại nhiều lần; khi gọi, " + code("$1") + " là chữ thứ nhất sau tên (tên công cụ), " + code("$2") + " là chữ thứ hai (mức phiên bản thấp nhất)"],
                  [code('v=$( … )'), "<b>biến</b> là một cái tên mang một giá trị: <code>v</code> nhận phần chữ mà lệnh trong ngoặc in ra; " + code("$v") + " lấy giá trị đó ra"],
                  [code('"$1" --version 2>/dev/null'), "hỏi chính công cụ: bạn là phiên bản nào? Nháy kép quanh <code>\"$1\"</code> giữ giá trị là một chữ nguyên vẹn. Công cụ chưa cài, hay chỉ là lối tắt mở cửa hàng ứng dụng, không trả được số; <code>2>/dev/null</code> ném thông báo lỗi đi"]]),
           """Dòng đầu đặt tên dat cho một nhóm lệnh để gọi lại sáu lần; trong đó đô la một là tên công cụ, đô la hai là mức phiên bản thấp nhất.
           Biến là một cái tên mang một giá trị: chữ v nhận phần chữ mà lệnh trong ngoặc in ra, và đô la v lấy giá trị đó ra. Lệnh hỏi chính công cụ xem nó là phiên bản nào, dấu nháy kép giữ tên công cụ là một chữ nguyên vẹn. Công cụ chưa cài thì không trả ra số, và đoạn chuyển hướng ở cuối ném thông báo lỗi đi.""",
           focus=["1.2", "1.3", "1.4", "1.4"]),
        st(table(["phần của tệp", "nghĩa"],
                 [[code("… | grep -oE '[0-9.]+' | head -1"), "dấu <code>|</code> đưa chữ in ra của lệnh bên trái cho lệnh bên phải; <code>grep -o</code> chỉ in phần khớp <b>mẫu</b>; trong mẫu, <code>[0-9.]</code> là <b>một</b> ký tự thuộc nhóm chữ số <code>0</code>–<code>9</code> hoặc dấu chấm, và <code>+</code> (cần cờ <code>-E</code>) là một hay nhiều lần liền nhau, nên mẫu bắt trọn số phiên bản, ví dụ <code>2.53.0</code> trong dòng <code>git version 2.53.0</code>; <code>head -1</code> giữ dòng đầu"],
                  [code("printf '%s\\n%s\\n' \"$2\" \"$v\""), "<code>printf</code> in chữ theo một khuôn: mỗi <code>%s</code> là một chỗ điền một chữ, <code>\\n</code> là xuống dòng. Ví dụ <code>printf '%s\\n%s\\n' 2.28 2.53</code> in hai dòng: <code>2.28</code> rồi <code>2.53</code>. Ở đây: mức thấp nhất và số phiên bản thật, mỗi số một dòng"]]),
           """Phần hai lọc ra số phiên bản rồi so với mức thấp nhất. Dấu gạch đứng đưa chữ in ra của lệnh bên trái cho lệnh bên phải. Lệnh lọc kèm cờ o chỉ in phần khớp mẫu. Trong mẫu, ngoặc vuông là một ký tự thuộc nhóm chữ số hoặc dấu chấm. Dấu cộng, cần cờ E, là một hay nhiều lần liền nhau, nên bắt trọn số phiên bản như hai chấm năm mươi ba chấm không. Lệnh lấy dòng đầu giữ dòng đầu tiên.
           Lệnh in theo khuôn nhận một khuôn chữ. Trong khuôn, ký hiệu phần trăm s là một chỗ điền một chữ, gạch chéo n là xuống dòng; điền hai chấm hai mươi tám và hai chấm năm mươi ba thì in hai dòng.
""",
           focus=[1, "1.2", "1.2", "1.2", "1.2", "1.2", "1.3", "1.3"], clear=True),
        st(table(["phần của tệp", "nghĩa"],
                 [[code("sort -V"), "xếp các số phiên bản từ nhỏ tới lớn: nếu số đứng đầu đúng là mức thấp nhất thì máy đạt"],
                  [code('if [ "$nho" = "$2" ]; then A; else B; fi'), "<b>lệnh điều kiện</b>: " + code('[ "$nho" = "$2" ]') + " hỏi hai chữ có bằng nhau không; đúng thì làm A (in ✔), không thì làm B (in THIEU). Dấu <code>;</code> nối các phần trên cùng một dòng, như một lần xuống dòng"],
                  [code("dat git 2.28"), "một lần gọi: công cụ <code>git</code>, từ bản 2.28 trở lên mới đạt; sáu dòng cuối là sáu lần gọi"]]),
           """Lệnh xếp theo phiên bản sắp hai số từ nhỏ tới lớn, nên nếu số đứng đầu đúng là mức thấp nhất thì máy đạt yêu cầu.
           Lệnh điều kiện hỏi hai chữ có bằng nhau không, đúng thì in dấu tích, không thì in chữ báo thiếu; dấu chấm phẩy nối các phần trên cùng một dòng, như một lần xuống dòng.
           Sáu dòng cuối là sáu lần gọi, mỗi lần ghi tên công cụ và mức thấp nhất, ví dụ công cụ ghi phiên bản từ bản hai chấm hai mươi tám.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
        st(term_block(kiem, title="Chạy trong cửa sổ lệnh"),
           """Chạy tệp này, máy in sáu dòng. Mỗi dòng bắt đầu bằng dấu tích nghĩa là công cụ đó đã có và đủ phiên bản. Dòng nào báo thiếu, bạn cài hoặc nâng cấp công cụ đó rồi mở lại cửa sổ lệnh và chạy lại.""", clear=True),
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
           Hoặc cài nhầm bản chỉ để chạy Java, thiếu trình biên dịch nên không viết được chương trình."""),
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
           Câu ba, nếu chỉ cần hai mươi bản ghi thì chọn cách nào, vì sao.""", pause=30),
        st("""<p><b>Câu 1.</b> Cách A:</p>
$$200\\,000 \\times 100\\ \\text{micro giây} = 20\\,000\\,000\\ \\text{micro giây} = \\hl{20\\ \\text{giây}}$$
<p><b>Câu 2.</b> Cách B: nạp $2$ giây, rồi đọc ở bộ nhớ:</p>
$$200\\,000 \\times 100\\ \\text{ns} = 0{,}02\\ \\text{giây} \\;\\Rightarrow\\; 2 + 0{,}02 = \\hl{2{,}02\\ \\text{giây}}$$""",
           """Đáp án câu một, cách A, hai trăm nghìn nhân một trăm phần triệu giây là hai mươi triệu phần triệu giây, tức hai mươi giây.
           Câu hai, cách B, nạp mất hai giây, rồi đọc ở bộ nhớ hai trăm nghìn nhân một trăm phần tỉ giây là hai mươi triệu phần tỉ giây, tức không phẩy không hai giây. Tổng là hai phẩy không hai giây, nhanh hơn gần mười lần."""),
        st("""<p><b>Câu 3.</b> Cách A với 20 bản ghi: $20 \\times 100$ micro giây $= 2$ mili giây. Cách B vẫn mất ít nhất $2$ giây để nạp.</p>
<div class="box key">Chỉ cần ít bản ghi thì <b>cách A thắng</b> ($2$ mili giây so với hơn $2$ giây). Nạp trước chỉ có lợi khi số lần đọc đủ lớn để bù chi phí nạp.</div>""",
           """Câu ba, với hai mươi bản ghi, cách A mất hai phần nghìn giây, còn cách B vẫn mất ít nhất hai giây chỉ để nạp. Vậy khi chỉ cần ít bản ghi, cách A thắng.
           Nạp trước chỉ có lợi khi số lần đọc đủ lớn để bù chi phí nạp.""", clear=True),
    ], checks=["200_000 * 100 // 1_000_000 == 20", "200_000 * 100 / 1e9 == 0.02", "round(2 + 200_000 * 100 / 1e9, 2) == 2.02",
               "20 * 100 / 1000 == 2.0", "round(20 / 2.02, 1) == 9.9"])
    sc_prac = practice_scene(sc, "Tự làm: cài đủ công cụ, chấm bằng tệp kiểm", pr_steps(
        st, "FND", "L00",
        """<p><b>Đề</b>: máy của bạn phải có đủ công cụ của khoá.</p>
<ol><li>Cài Git for Windows (2.28+), JDK 21, Python 3.11+ và <code>sqlite3</code> 3.32+ (đặt <code>sqlite3.exe</code> vào thư mục <code>bin</code> cá nhân), rồi <b>mở lại</b> Git Bash.</li>
<li>Tạo tệp <code>kiem.sh</code> với đúng nội dung ở cảnh trước (chép nguyên), lưu ở thư mục gốc của bộ khoá.</li>
<li>Mở Git Bash tại thư mục đó và chạy <code>bash kiem.sh</code>: cần <b>sáu dòng ✔</b>.</li></ol>
<p class="note">Dòng nào báo THIEU: cài công cụ đó, mở lại Git Bash, chạy lại.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy. Cài bốn công cụ của khoá rồi mở lại cửa sổ lệnh.
        Tạo tệp kiểm với đúng nội dung ở cảnh trước, mở cửa sổ lệnh tại thư mục chứa tệp, chạy nó, và cần thấy sáu dấu tích. Hãy dừng video và làm.""",
        KIEM_OUT, "kiem.sh",
        """<div class="box key"><b>Nếu kẹt:</b> dòng THIEU python: chưa cài Python 3.11 trở lên, hoặc chưa đánh dấu “Add to PATH”, hoặc máy chỉ có lối tắt mở cửa hàng ứng dụng thay cho Python (gõ <code>python --version</code> mà báo “Python was not found” là ca này); cài từ python.org.
Dòng THIEU javac: bạn cài bản JRE hoặc bản Java cũ hơn 21; hãy cài JDK 21. Dòng THIEU git hoặc sqlite3: bản cũ hơn mức thấp nhất (Git 2.28, sqlite3 3.32). Dòng THIEU sqlite3: <code>sqlite3.exe</code> chưa nằm trong thư mục <code>bin</code> cá nhân, hoặc chưa mở lại Git Bash. Lời giải ở <code>labs/FND/L00/loi_giai.sh</code>; chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, dòng báo thiếu ngôn ngữ thứ hai nghĩa là bạn chưa cài, hoặc chưa đánh dấu ô thêm vào đường dẫn. Cũng có thể máy chỉ có lối tắt mở cửa hàng ứng dụng, hãy cài từ địa chỉ chính thức.
        Dòng báo thiếu trình biên dịch Java nghĩa là bạn cài nhầm bản chỉ để chạy, hoặc bản cũ hơn hai mươi mốt. Dòng báo thiếu cơ sở dữ liệu nghĩa là tệp chạy chưa nằm trong thư mục bin cá nhân, hoặc bạn chưa mở lại cửa sổ lệnh. Lời giải chỉ mở sau khi đã thử.""", pause=120), "FND", "L00")
    write_lab("FND", "L00", """# Lab FND L00 — Kiểm máy bằng một tệp lệnh

Cài đủ công cụ theo bài (từng bước cài nằm ở cảnh “Cài đặt từng bước” của video; giao diện trình cài có thể khác nhẹ theo phiên bản), đúng phiên bản thấp nhất (Git for Windows 2.28 trở lên kèm Git Bash, JDK 21 trở lên, Python 3.11+, và `sqlite3` 3.32 trở lên: tải `sqlite-tools-win-x64` từ sqlite.org, giải nén, chép `sqlite3.exe` vào thư mục `bin` trong thư mục cá nhân), rồi **mở lại** Git Bash. `sqlite3` là bắt buộc: bài 8 và 10 dùng. Kiểm: `sqlite3 --version` in số phiên bản bắt đầu bằng 3.

1. Tạo tệp `kiem.sh` (bằng Visual Studio Code hoặc Notepad++, không dùng Word) với nội dung dưới đây. Chép nguyên, kể cả dấu ✔ (chép dán, không gõ bằng bàn phím); phần giải thích từng dòng ở cảnh "Chuẩn bị máy" của video. Tệp chạy thật lệnh hỏi phiên bản của từng công cụ (`--version`) rồi so với mức thấp nhất; công cụ chưa cài, bản quá cũ, hoặc Python chỉ là lối tắt mở cửa hàng ứng dụng của Windows đều in THIEU. Lưu ở **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó: chuột phải vào chỗ trống của thư mục, chọn *Open Git Bash here*.

```bash
""" + KIEM + """
```

2. Chạy `bash kiem.sh` ở thư mục đó. Máy đạt khi in **đúng sáu dòng**, mỗi dòng bắt đầu bằng ✔ (xem `mong_doi.txt`).
3. Chấm: `bash labs/cham.sh FND L00 kiem.sh` (chạy từ chính thư mục gốc có `labs`). Dòng báo THIEU nghĩa là thiếu công cụ đó: cài, mở lại Git Bash, chạy lại.

Muốn xem số phiên bản từng công cụ: `bash labs/check_env.sh` (cùng mức thấp nhất, in rõ số và lý do thiếu).
""", "sh", KIEM, KIEM_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic, tư duy và bản đồ khoá", [
        st(chain("tệp trên ổ đĩa", "nạp vào bộ nhớ", "bộ xử lý làm từng lệnh", "tổng chờ = số lần × thời gian một lần",
                 "học: xem → tự làm → chấm → đánh dấu → ôn", "máy: kiểm bằng tệp kiem.sh"),
           """Tổng kết chuỗi logic. Chương trình nằm ở ổ đĩa, được nạp vào bộ nhớ, và bộ xử lý làm từng lệnh.
           Tổng chờ bằng số lần nhân thời gian một lần, nên chỗ để dữ liệu quyết định tốc độ. Cách học là xem, tự làm, chấm, đánh dấu, ôn. Và máy sẵn sàng khi tệp kiểm in sáu dấu tích."""),
        st(table(["bài", "nội dung", "bạn làm được"],
                 [["L01–L02", "cửa sổ lệnh, thư mục, tệp", "đi quanh máy và dựng cây thư mục bằng chữ"],
                  ["L03–L04", "lọc văn bản, chương trình và PATH", "ghép lệnh bằng ống, chạy tệp lệnh"],
                  ["L05–L06", "trình soạn mã, đọc lỗi, CSV/JSON/YAML", "sửa lỗi theo thông báo, đọc dữ liệu có cấu trúc"],
                  ["L07–L08", "HTTP và SQL", "hỏi một máy chủ bằng chữ, hỏi một bảng bằng chữ"],
                  ["L09–L10", "phiên bản và dự án nhỏ", "nối mọi thứ thành sổ tay giao dịch"]])
           + "<div class='box key'><b>Tư duy:</b> trước khi viết gì, hỏi dữ liệu nằm ở đâu và sẽ bị đọc mấy lần.</div>",
           """Đây là bản đồ mười bài tiếp theo của khoá. Hai bài đầu dạy cửa sổ lệnh, thư mục và tệp; hai bài sau dạy lọc văn bản và chương trình.
           Hai bài nữa dạy đọc lỗi và dữ liệu có cấu trúc, rồi giao thức HTTP và SQL. Hai bài sau cùng dạy quản lý phiên bản và một dự án nhỏ.
           Điều cần mang theo, trước khi viết gì, hãy hỏi dữ liệu nằm ở đâu và sẽ bị đọc mấy lần.""", forward_ref=True,
           focus=[1, ["1.2", "1.3"], ["1.4", "1.5"], "1.6", 2]),
    ])
    return lesson("L00", "may_tinh_va_cach_hoc", "Bài 0 — Máy tính chạy chương trình thế nào, cách học và chuẩn bị máy",
                  "curriculum/fnd.yaml L00; audit/fnd/verify_fnd.py L00 (Git Bash chạy thật tệp kiem.sh); labs/ENV.md; "
                  "Hennessy & Patterson, Computer Architecture: A Quantitative Approach (phân cấp bộ nhớ: bộ nhớ, ổ đĩa; số trong bài là số minh hoạ bậc độ lớn); "
                  "Roediger & Karpicke 2006, Test-enhanced learning: taking memory tests improves long-term retention, Psychological Science 17(3), 249-255, doi 10.1111/j.1467-9280.2006.01693.x (CITED: tiêu đề, số tập và kết luận sau 5 phút / 2 ngày / 1 tuần đối chiếu qua API Crossref ngày 2026-11-15; chỉ đọc phần tóm tắt, chưa mở bài đầy đủ); "
                  "địa chỉ cài đặt: git-scm.com, adoptium.net, python.org, sqlite.org, code.visualstudio.com; hướng dẫn cài từng bước (truy cập 2026-11-15, CITED): Git for Windows: git-scm.com/install/windows (bản 64-bit, Git-x.y.z-64-bit.exe) và tệp cài đặt install.iss của dự án git-for-windows/build-extra (thành phần Windows Explorer integration > Open Git Bash here; màn hình Adjusting your PATH environment, ba lựa chọn, mục giữa Recommended là mặc định; lối tắt Start > Git > Git Bash; terminal mặc định MinTTY); JDK: adoptium.net/installation/windows (tệp .msi chỉ cho Windows x64; màn hình Custom Setup có Add to PATH chọn sẵn, Set JAVA_HOME không chọn sẵn) và API api.adoptium.net (có OpenJDK21U-jdk_x64_windows_hotspot_21.0.x.msi); Python: docs.python.org/3.13/using/windows.html (Install Now / Customize installation; ô thêm vào PATH) và python.org/downloads/windows (có Python install manager; bản 3.13 vẫn có Windows installer 64-bit). NOT_VERIFIED: dòng System Type (x64-based PC / ARM64-based PC) của ứng dụng System Information của Windows và việc trang adoptium.net có sẵn bản aarch64 cho Windows; LTS = bản hỗ trợ dài hạn (Temurin 21 là bản LTS); chữ chính xác của ô tích trong trình cài Python 3.13 (Add python.exe to PATH) và mục Show more options của Windows 11, vì không chạy trình cài ở máy kiểm (không có ảnh chụp màn hình trình cài); giao diện có thể khác nhẹ theo phiên bản; sqlite3 để ở ~/bin (Git for Windows: /etc/profile.d/env.sh đặt $HOME/bin vào PATH khi mở cửa sổ lệnh đăng nhập)",
                  ["Mô tả đường đi của chương trình từ ổ đĩa vào bộ nhớ tới bộ xử lý làm từng lệnh",
                   "Chạy tay chương trình ba lệnh và ghi bộ nhớ sau mỗi lệnh",
                   "Tính tổng thời gian chờ bằng số lần nhân thời gian một lần, ở ba quy mô dữ liệu",
                   "Kể năm bước của vòng học (xem, tự làm, chấm, đánh dấu, ôn) và giải thích vì sao tự làm trước khi xem đáp án",
                   "Cài các công cụ của khoá, kể cả sqlite3, và kiểm máy bằng tệp lệnh in dấu tích cho từng công cụ",
                   "Tạo, lưu và chạy một tệp lệnh bằng trình soạn mã và Git Bash mở ngay tại thư mục chứa tệp"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_may, sc_form, sc_ex, sc_chk, sc_scale, sc_hoc, sc_may2, sc_caidat, sc_kiem, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "intuition"), (2, "ex_may"), (3, "example"), (4, "hoc"), (5, "practice"), (6, "practice")])
