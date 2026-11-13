from lib import *
from labkit import write_lab, practice_steps, practice_scene

LAB_SOL = """mkdir -p cua_hang/kho cua_hang/bao_cao
touch cua_hang/kho/ao.txt cua_hang/kho/quan.txt cua_hang/kho/non.txt
echo "ao 5" > cua_hang/bao_cao/tong.txt
echo "quan 3" >> cua_hang/bao_cao/tong.txt
cp cua_hang/kho/ao.txt cua_hang/kho/ao_sao.txt
mv cua_hang/kho/non.txt cua_hang/kho/mu.txt
rm cua_hang/kho/quan.txt
find cua_hang | sort
cat cua_hang/bao_cao/tong.txt"""
LAB_OUT = """cua_hang
cua_hang/bao_cao
cua_hang/bao_cao/tong.txt
cua_hang/kho
cua_hang/kho/ao.txt
cua_hang/kho/ao_sao.txt
cua_hang/kho/mu.txt
ao 5
quan 3"""


def build():
    hook = cmd("PhienHook", [
        ("mkdir bc && cd bc", ""), ("touch a.txt b.txt c.png", ""), ("ls", "a.txt  b.txt  c.png"),
        ("rm *.txt", ""), ("ls", "c.png"),
        ("touch a.txt b.txt", ""), ("rm * .txt", "rm: cannot remove '.txt': No such file or directory"), ("ls", ""),
    ])
    tep = cmd("PhienTep", [
        ("mkdir -p du_an/nguon du_an/sao_luu", ""), ("cd du_an", ""), ("touch nguon/main.txt", ""),
        ("ls -R", ".:\nnguon/  sao_luu/\n\n./nguon:\nmain.txt\n\n./sao_luu:"),
        ('echo "dong 1" > nguon/main.txt', ""), ('echo "dong 2" >> nguon/main.txt', ""), ("cat nguon/main.txt", "dong 1\ndong 2"),
        ('echo "ghi de" > nguon/main.txt', ""), ("cat nguon/main.txt", "ghi de"),
        ("cp nguon/main.txt sao_luu/ban_sao.txt", ""), ("mv sao_luu/ban_sao.txt sao_luu/ghi_chu.txt", ""),
        ("ls nguon sao_luu", "nguon:\nmain.txt\n\nsao_luu:\nghi_chu.txt"),
        ("rm sao_luu/ghi_chu.txt", ""), ("ls sao_luu", ""), ("ls nguon", "main.txt"),
        ("rm nguon", "rm: cannot remove 'nguon': Is a directory"), ("rm -r nguon", ""), ("ls", "sao_luu/"),
    ])
    sao = cmd("PhienSao", [
        ("touch a.txt b.txt c.png", ""), ("echo *.txt", "a.txt b.txt"), ("echo *", "a.txt b.txt c.png"),
        ("echo * .txt", "a.txt b.txt c.png .txt"), ("echo ?.png", "c.png"), ("echo ??.png", "??.png"),
    ])
    kiem = cmd("PhienKiem", [
        ("mkdir p && cd p", ""), ("touch a b c d e", ""), ("ls | wc -l", "5"), ("rm a b", ""),
        ("ls | wc -l", "3"), ("find . -type f | wc -l", "3"),
    ])
    quymo = cmd("PhienQuyMo", [
        ("mkdir q && cd q", ""),
        ("touch t{1..3}.txt", ""), ("ls *.txt | wc -l", "3"),
        ("touch t{1..300}.txt", ""), ("ls *.txt | wc -l", "300"),
        ("touch t{1..3000}.txt", ""), ("ls *.txt | wc -l", "3000"),
    ])
    dir_rong = cmd("PhienDirRong", [("DIR=", ""), ('echo "$DIR/"', "/")])
    quiz = cmd("PhienQuiz", [
        ("touch bao_cao_1.txt bao_cao_2.txt bao_cao_10.txt anh_1.png ghi_chu.txt", ""),
        ("echo bao_cao_?.txt", "bao_cao_1.txt bao_cao_2.txt"),
        ("echo bao_cao_*.txt", "bao_cao_1.txt bao_cao_10.txt bao_cao_2.txt"),
        ("echo *.txt", "bao_cao_1.txt bao_cao_10.txt bao_cao_2.txt ghi_chu.txt"),
        ("echo *_1.*", "anh_1.png bao_cao_1.txt"),
    ])

    sc_hook = sc("hook", "hook", "Một dấu cách thừa xoá sạch cả thư mục, và không có thùng rác", [
        st(term_block(hook, 0, 5, title="Xoá đúng: chỉ các tệp .txt")
           + "<p>Lệnh xoá <code>rm *.txt</code> bỏ hai tệp <code>.txt</code>; ảnh còn nguyên.</p>",
           """Chào bạn, hãy xem một thao tác xoá an toàn trước. Thư mục có ba tệp. Lệnh xoá mẫu sao chấm t x t chỉ bỏ hai tệp văn bản, còn lại tệp ảnh.
           Chú ý là không có hộp hỏi lại, và cũng không có thùng rác."""),
        st(term_block(hook, 5, 8, title="Xoá sai: thêm MỘT dấu cách")
           + "<div class='box warn'>Dấu cách làm <code>* .txt</code> thành <b>hai</b> mẫu: <code>*</code> khớp <b>mọi</b> tệp. Thư mục trống rỗng.</div>",
           """Bây giờ ta tạo lại hai tệp và gõ sai một dấu cách, sao cách chấm t x t. Máy hiểu đó là hai mẫu riêng. Mẫu sao khớp mọi tệp, nên cả thư mục bị xoá sạch.
           Dòng báo lỗi chỉ nói về mẫu thứ hai, còn việc xoá đã xảy ra. Thư mục sau đó trống rỗng, và không thể lấy lại."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Tạo, ghi, đọc, chép, đổi tên, xoá tệp bằng lệnh: mỗi lệnh làm gì?</li>
<li>Dấu <code>&gt;</code> và <code>&gt;&gt;</code> khác nhau thế nào?</li>
<li>Ký tự đại diện <code>*</code> thật sự làm gì, và <b>xem trước</b> nó bằng cách nào?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Tạo, ghi, đọc, chép, đổi tên và xoá tệp bằng lệnh, mỗi lệnh làm gì. Dấu lớn hơn và hai dấu lớn hơn khác nhau thế nào.
           Và ký tự đại diện dấu sao thật sự làm gì, cùng cách xem trước nó."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: chỗ đứng, đường dẫn và tên tệp", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① chỗ đứng", "lệnh in vị trí cho biết bạn đứng ở đâu; mọi tên tệp tính từ đó"],
                  ["② đường dẫn tương đối", "<code>nguon/main.txt</code> = tệp <code>main.txt</code> trong thư mục <code>nguon</code> ngay dưới chỗ đứng"],
                  ["③ hai dấu chấm", "<code>..</code> là thư mục cha; <code>cd ..</code> lùi một cấp"],
                  ["④ tên tệp", "không dấu, không khoảng trắng, ví dụ <code>ghi_chu.txt</code>"]]),
           """Ta ôn lại bốn điều từ bài trước. Chỗ đứng là nơi lệnh in vị trí cho biết, và mọi tên tệp được tính từ đó. Đường dẫn tương đối nguồn gạch chéo main chấm t x t là tệp main trong thư mục nguồn ngay dưới chỗ đứng.
           Hai dấu chấm là thư mục cha. Và tên tệp nên không dấu, không khoảng trắng, nối bằng dấu gạch dưới.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tám lệnh và ba dấu", [
        st(table(["lệnh", "đọc là", "nghĩa"],
                 [["<code>mkdir -p a/b</code>", "lệnh tạo thư mục", "tạo thư mục; cờ <code>-p</code> tạo luôn các thư mục cha còn thiếu"],
                  ["<code>touch f.txt</code>", "lệnh tạo tệp rỗng", "tạo tệp không có nội dung (nếu đã có thì chỉ đổi giờ sửa)"],
                  ["<code>echo \"xin chao\"</code>", "lệnh in chữ", "in các tham số ra <b>đầu ra</b> (màn hình)"],
                  ["<code>cat f.txt</code>", "lệnh in nội dung tệp", "in nội dung tệp ra đầu ra"]]),
           """Bảng này giải mã bốn lệnh đầu. Lệnh tạo thư mục tạo thư mục, và cờ p tạo luôn các thư mục cha còn thiếu. Lệnh tạo tệp rỗng tạo tệp không có nội dung.
           Lệnh in chữ in các tham số ra đầu ra, tức màn hình. Lệnh in nội dung tệp cho thấy nội dung tệp ra đầu ra.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["lệnh", "đọc là", "nghĩa"],
                 [["<code>cp a b</code>", "lệnh chép", "chép tệp <code>a</code> thành <code>b</code>; <code>a</code> vẫn còn"],
                  ["<code>mv a b</code>", "lệnh di chuyển", "đổi tên hoặc chuyển <code>a</code> sang <code>b</code>; <code>a</code> không còn"],
                  ["<code>rm a</code>", "lệnh xoá", "xoá <b>ngay</b>, không thùng rác; thư mục cần cờ <code>-r</code>"]]),
           """Ba lệnh tiếp theo. Lệnh chép làm ra tệp thứ hai, tệp đầu vẫn còn. Lệnh di chuyển đổi tên hoặc chuyển chỗ, tệp cũ không còn.
           Lệnh xoá bỏ ngay, không qua thùng rác, và muốn xoá thư mục thì cần cờ r.""",
           focus=[1, "1.2", "1.3", "1.4"], clear=True),
        st(table(["viết", "nghĩa"],
                 [["<code>&gt;</code>", "<b>chuyển hướng</b>: đưa đầu ra vào tệp, <b>ghi đè</b> cả tệp"],
                  ["<code>&gt;&gt;</code>", "đưa đầu ra vào cuối tệp, <b>nối thêm</b>"],
                  ["<code>*</code>", "<b>ký tự đại diện</b>: khớp mọi chuỗi (kể cả rỗng), ví dụ <code>*.txt</code>"],
                  ["<code>?</code>", "khớp <b>đúng một</b> ký tự bất kỳ, ví dụ <code>?.png</code>"]]),
           """Ba dấu cuối. Một dấu lớn hơn chuyển hướng đầu ra vào tệp và ghi đè cả tệp. Hai dấu lớn hơn nối thêm vào cuối tệp.
           Dấu sao là ký tự đại diện, khớp mọi chuỗi. Dấu hỏi khớp đúng một ký tự bất kỳ.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: chép, di chuyển, xoá làm cây thay đổi thế nào", [
        st(svg(1500, 470,
               panel(10, 10, 470, 440, "cp a.txt b.txt", C_BLUE),
               box(40, 90, 150, 60, "a.txt", C_GRAY), txt(115, 190, "trước", 22, "middle", "#6b7280"),
               arrow(200, 120, 270, 120, "#2a78d6"),
               box(280, 80, 160, 60, "a.txt", C_GRAY), box(280, 160, 160, 60, "b.txt", C_GREEN),
               txt(360, 270, "sau: HAI tệp", 24, "middle", "#16a34a", True),
               txt(245, 340, "nội dung giống nhau", 22, "middle", "#1f2937"),
               panel(510, 10, 470, 440, "mv a.txt b.txt", C_AMBER),
               box(540, 90, 150, 60, "a.txt", C_GRAY),
               arrow(700, 120, 770, 120, "#d97706"),
               box(780, 100, 160, 60, "b.txt", C_AMBER),
               txt(860, 210, "sau: MỘT tệp, đổi tên", 24, "middle", "#d97706", True),
               txt(745, 340, "a.txt không còn", 22, "middle", "#1f2937"),
               panel(1010, 10, 480, 440, "rm a.txt", C_RED),
               box(1040, 90, 150, 60, "a.txt", C_GRAY),
               arrow(1200, 120, 1270, 120, "#dc2626"),
               box(1280, 100, 180, 60, "(không còn)", C_RED, dash=True),
               txt(1250, 220, "KHÔNG qua thùng rác", 24, "middle", "#dc2626", True),
               txt(1250, 340, "không có nút hoàn tác", 22, "middle", "#1f2937")),
           """Hình này so ba lệnh. Lệnh chép làm ra thêm một tệp, nên sau đó có hai tệp nội dung giống nhau. Lệnh di chuyển chỉ đổi tên, nên sau đó vẫn một tệp, và tên cũ không còn.
           Lệnh xoá thì tệp biến mất ngay, không qua thùng rác, và không có nút hoàn tác. Vì vậy với lệnh xoá, hãy kiểm tra kỹ trước khi bấm phím xuống dòng."""),
        st(svg(1500, 330,
               box(20, 40, 380, 110, ["tệp ghi.txt", "dong 1", "dong 2"], C_GRAY, bold=True),
               txt(210, 190, "đang có 2 dòng", 22, "middle", "#6b7280"),
               arrow(410, 70, 560, 70, "#d97706", "echo &gt; (ghi đè)"),
               box(570, 40, 380, 110, ["tệp ghi.txt", "dòng mới", "(cũ mất)"], C_AMBER, bold=True),
               arrow(410, 130, 560, 250, "#16a34a", "echo &gt;&gt; (nối)"),
               box(570, 200, 380, 110, ["tệp ghi.txt", "dong 1", "dong 2", "dòng mới"], C_GREEN, bold=True),
               txt(1200, 100, "một dấu &gt;: bắt đầu lại từ trống", 24, "middle", "#d97706", True),
               txt(1200, 260, "hai dấu &gt;&gt;: viết tiếp phía dưới", 24, "middle", "#16a34a", True)),
           """Hình thứ hai so một dấu lớn hơn với hai dấu lớn hơn. Tệp đang có hai dòng. Một dấu bắt đầu lại từ trống, nên hai dòng cũ mất và chỉ còn dòng mới.
           Hai dấu viết tiếp phía dưới, nên hai dòng cũ vẫn còn và thêm dòng mới ở cuối."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: dấu sao do chương trình cửa sổ lệnh mở ra, không phải lệnh", [
        st(term_block(sao, 0, 2, title="Bước 1. Thử với tệp có thật")
           + "<p>Vì <code>echo</code> chỉ in lại các tham số, nó cho ta thấy <b>máy đã đổi mẫu thành gì</b> trước khi lệnh chạy.</p>",
           """Bước một, thử với tệp có thật. Vì lệnh in chữ chỉ in lại các tham số, nó cho ta thấy máy đã đổi mẫu thành những gì, trước khi lệnh chạy.
           Mẫu sao chấm t x t được đổi thành hai tên tệp là a chấm t x t và b chấm t x t."""),
        st(term_block(sao, 2, 4, title="Bước 2. Dấu sao một mình khớp mọi tệp")
           + "<p>Nên <code>rm *</code> thành <code>rm a.txt b.txt c.png</code>: lệnh xoá <b>không hề thấy dấu sao</b>, chỉ thấy danh sách tên.</p>",
           """Bước hai, dấu sao đứng một mình khớp mọi tệp. Vì vậy lệnh xoá với dấu sao thành lệnh xoá với cả ba tên tệp. Lệnh xoá không hề thấy dấu sao, nó chỉ thấy danh sách tên đã được mở ra."""),
        st(term_block(sao, 3, 4, title="Bước 3. Dấu cách chia mẫu thành hai")
           + "<p>Vì dấu cách ngăn tham số, <code>* .txt</code> là hai tham số: <code>*</code> mở thành <b>mọi tên</b>, cộng thêm chữ <code>.txt</code>.</p>",
           """Bước ba, dấu cách chia mẫu thành hai tham số. Vì dấu cách ngăn các tham số, sao cách chấm t x t là hai mẫu. Mẫu sao mở thành mọi tên, và còn thêm chữ chấm t x t đứng riêng.
           Đó chính là nguyên nhân của tai nạn đầu bài.""", clear=True),
        st(term_block(sao, 4, 6, title="Bước 4. Dấu hỏi: đúng một ký tự")
           + "<p>Vì <code>?</code> khớp <b>đúng một</b> ký tự, <code>?.png</code> khớp <code>c.png</code>. Mẫu <b>không khớp</b> gì thì máy giữ nguyên chữ, như <code>??.png</code>.</p>",
           """Bước bốn, dấu hỏi. Vì dấu hỏi khớp đúng một ký tự, nên mẫu hỏi chấm p n g khớp c chấm p n g. Hai dấu hỏi thì cần hai ký tự, không có tệp nào khớp.
           Khi mẫu không khớp tệp nào, máy giữ nguyên chữ của mẫu, và đó cũng là một dấu hiệu bạn gõ sai.""", clear=True),
    ], checks=["len('a.txt b.txt'.split()) == 2", "len('a.txt b.txt c.png .txt'.split()) == 4", "len('c.png') - len('.png') == 1"])
    sc_ex = sc("example", "example", "Ví dụ: dựng, ghi, chép, đổi tên, xoá: năm phép làm", [
        st(term_block(tep, 0, 4, title="① Dựng cây du_an")
           + "<p><code>mkdir -p</code> tạo hai thư mục cùng lúc; <code>touch</code> tạo tệp rỗng <code>main.txt</code>; <code>ls -R</code> liệt kê cả thư mục con.</p>",
           """Phép thứ nhất, dựng cây. Lệnh tạo thư mục tạo hai thư mục một lúc, nguồn và sao lưu. Ta đi vào du án, tạo tệp rỗng main trong nguồn, rồi liệt kê cả các thư mục con bằng cờ chữ r hoa.
           Thư mục nguồn có một tệp, thư mục sao lưu còn trống."""),
        st(term_block(tep, 4, 7, title="② Ghi bằng > rồi nối bằng >>")
           + "<p>Lệnh đầu ghi vào tệp trống; lệnh sau <b>nối</b> dòng thứ hai xuống dưới; <code>cat</code> cho thấy cả hai.</p>",
           """Phép thứ hai, ghi vào tệp. Dấu lớn hơn đưa dòng một vào tệp. Hai dấu lớn hơn nối dòng hai xuống dưới. Lệnh in nội dung tệp cho thấy cả hai dòng, theo đúng thứ tự ghi.""", clear=True),
        st(term_block(tep, 7, 9, title="③ Ghi đè: một dấu > xoá sạch nội dung cũ")
           + "<p>Một dấu <code>&gt;</code> đã <b>mất hai dòng cũ</b>; không ai hỏi lại.</p>",
           """Phép thứ ba, ghi đè. Lần này ta dùng một dấu lớn hơn. Nội dung cũ có hai dòng mất hết, chỉ còn đúng dòng mới. Không có lời hỏi lại, nên một dấu thiếu có thể xoá dữ liệu quan trọng.""", clear=True),
        st(term_block(tep, 9, 12, title="④ Chép rồi đổi tên")
           + "<p><code>cp</code> làm bản sao ở <code>sao_luu</code>; <code>mv</code> đổi tên bản sao; <code>main.txt</code> gốc vẫn ở <code>nguon</code>.</p>",
           """Phép thứ tư, chép rồi đổi tên. Lệnh chép làm bản sao sang thư mục sao lưu. Lệnh di chuyển đổi tên bản sao thành ghi chú. Tệp gốc vẫn nằm ở nguồn, nên cả hai thư mục đều có một tệp."""),
        st(term_block(tep, 12, 17, title="⑤ Xoá: tệp bằng rm, thư mục bằng rm -r")
           + "<p>Thư mục cần cờ <code>-r</code> (xoá cả nội dung bên trong). Xoá tệp rồi, <code>ls</code> thấy thư mục trống.</p>",
           """Phép thứ năm, xoá. Xoá tệp ghi chú thì thư mục sao lưu trống. Lệnh xoá không có cờ từ chối xoá thư mục, và báo đó là một thư mục.
           Thêm cờ r thì xoá cả thư mục cùng mọi thứ bên trong, và thư mục nguồn biến mất. Chỉ còn lại sao lưu.""", clear=True),
    ], checks=["len(['dong 1', 'dong 2']) == 2", "len(['ghi de']) == 1"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm bằng hai cách", [
        st(term_block(kiem, 1, 5, title="Cách 1: đếm bằng ls, ống | và wc -l")
           + "<p>Dấu <code>|</code> (ống) chuyển đầu ra của lệnh bên trái làm đầu vào cho lệnh bên phải; <code>wc -l</code> <b>đếm dòng</b>.</p>",
           """Đường kiểm khác là đếm. Ta tạo năm tệp, rồi dùng dấu ống để chuyển danh sách của lệnh liệt kê cho lệnh đếm dòng. Dấu ống chuyển đầu ra của lệnh bên trái làm đầu vào cho lệnh bên phải.
           Ta được năm. Sau khi xoá hai tệp thì còn ba, vì năm trừ hai bằng ba.""", forward_ref=True),
        st(term_block(kiem, 5, 6, title="Cách 2: đếm bằng một lệnh khác (find)")
           + "<p>$5 - 2 = \\hl{3}$ và hai cách đếm cùng ra $3$ ✓</p>",
           """Cách thứ hai, dùng một lệnh khác để tìm các tệp rồi đếm. Kết quả vẫn là ba. Hai cách đếm khác nhau cùng ra ba, và khớp với phép trừ năm trừ hai, nên ta tin việc xoá đã làm đúng hai tệp.""", clear=True),
    ], checks=["5 - 2 == 3"])
    sc_scale = sc("scale", "concept", "Khi số tệp nhân lên: một lệnh xoá hay chép chạm tới bao nhiêu tệp?", [
        st(term_block(quymo, 1, 7, title="Cùng mẫu *.txt, ba quy mô")
           + "<p>Chữ <code>t{1..300}</code> là <b>dải số</b>: máy mở thành <code>t1 t2 … t300</code>. <code>ls *.txt | wc -l</code> đếm mẫu khớp bao nhiêu tệp.</p>",
           """Ta tạo ba, rồi ba trăm, rồi ba nghìn tệp, cùng mẫu sao chấm t x t. Chữ trong ngoặc nhọn có hai dấu chấm là một dải số, máy mở thành các số liên tiếp.
           Lệnh đếm cho biết mẫu khớp bao nhiêu tệp, đó chính là số tệp một lệnh xoá cùng mẫu sẽ chạm tới."""),
        st(table(["số tệp khớp", "xem bằng mắt", "một lệnh xoá sai chạm tới"],
                 [["×1: 3", "đọc được", "3 tệp"], ["×100: 300", "cuộn mãi", "300 tệp"], ["×1 000: 3 000", "không đọc nổi", "3 000 tệp, gần như tức thì"]])
           + "<div class='box key'><b>Đánh đổi:</b> mẫu rộng thì tiện, nhưng sai một dấu là chạm tới cả nghìn tệp. "
             "Người làm nghề <b>xem trước</b> bằng <code>echo</code> hoặc đếm, và giữ bản sao lưu ở nơi khác, vì <code>rm</code> không hoàn tác.</div>",
           """Bảng này cho thấy sức nặng của một mẫu. Ba tệp thì cứ mở ra và đọc bằng mắt, không cần nhờ lệnh nào. Ba trăm tệp thì phải cuộn. Ba nghìn tệp thì không đọc nổi, mà một lệnh xoá sai vẫn chạm tới cả ba nghìn gần như tức thì.
           Mẫu rộng thì tiện nhưng nguy hiểm. Người làm nghề xem trước bằng lệnh in chữ hoặc đếm, và giữ bản sao lưu ở nơi khác, vì lệnh xoá không hoàn tác.""", clear=True),
    ], checks=["3 * 100 == 300", "3 * 1000 == 3000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Dấu cách thừa trong mẫu xoá: <code>rm * .txt</code>.</div>'
           + term_block(sao, 2, 4)
           + "<p>Phép thử bắt được lỗi: chạy <code>echo</code> với <b>đúng mẫu đó</b> trước. Thấy thừa <code>.txt</code> và mọi tên tệp thì dừng.</p>",
           """Lỗi thứ nhất, của người mới, là dấu cách thừa trong mẫu xoá. Phép thử bắt được lỗi này là chạy lệnh in chữ với đúng mẫu đó trước.
           Nếu thấy mọi tên tệp cùng chữ chấm t x t thừa, hãy dừng lại và sửa."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Dùng một dấu <code>&gt;</code> khi muốn nối: ghi đè tệp quan trọng.</div>'
           + term_block(tep, 7, 9)
           + "<p>Phép thử: đọc lại lệnh trước khi chạy, hỏi “mình muốn <b>thay</b> hay <b>thêm</b>?”. Thêm thì hai dấu.</p>",
           """Lỗi thứ hai, cũng của người mới, là dùng một dấu lớn hơn khi muốn nối. Nội dung cũ bị ghi đè mà không hỏi.
           Trước khi chạy, hãy tự hỏi mình muốn thay hay muốn thêm. Muốn thêm thì phải hai dấu."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Biến rỗng trong lệnh xoá: <code>rm -rf "<span>&#36;</span>DIR"/*</code>.</div>'
           + term_block(dir_rong)
           + "<p>Biến <code>DIR</code> chưa đặt, nên <code>\"<span>&#36;</span>DIR/\"</code> thành <code>/</code>, tức <b>gốc</b> của cả hệ thống. Lệnh xoá sẽ nhắm vào gốc.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là dùng biến trong lệnh xoá mà biến đó rỗng. Ở đây biến chưa có giá trị, nên đường dẫn có biến cộng dấu gạch chéo chỉ còn lại đúng dấu gạch chéo, tức gốc của cả hệ thống.
           Một lệnh xoá đệ quy nhắm vào đó sẽ phá cả máy. Hãy luôn kiểm tra biến không rỗng, và in thử đường dẫn trước khi xoá."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Thư mục có năm tệp: <code>bao_cao_1.txt</code>, <code>bao_cao_2.txt</code>, <code>bao_cao_10.txt</code>, <code>anh_1.png</code>, <code>ghi_chu.txt</code>. Máy xếp tên theo chữ cái.</p>
<ol><li><code>echo bao_cao_?.txt</code> in ra gì?</li><li><code>echo *_1.*</code> in ra gì?</li></ol>
<p><b>Quyết định:</b> muốn xoá ba bản báo cáo, bạn gõ <code>rm *.txt</code> hay <code>rm bao_cao_*.txt</code>? Vì sao, và bạn làm gì trước khi xoá?</p>""",
           """Bây giờ tới phần bạn tự làm. Thư mục có năm tệp, ba báo cáo mang số một, hai và mười, một ảnh, và một ghi chú. Câu một, lệnh in chữ với mẫu báo cáo gạch dưới hỏi chấm t x t in ra gì.
           Câu hai, mẫu sao gạch dưới một chấm sao in ra gì. Sau đó là một quyết định. Muốn xoá ba bản báo cáo thì nên gõ mẫu nào, vì sao, và làm gì trước khi xoá. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "kết quả", "lý do"],
                 [["1", "<code>bao_cao_1.txt bao_cao_2.txt</code>", "<code>?</code> là đúng một ký tự: <code>1</code>, <code>2</code> được; <code>10</code> có hai ký tự nên loại"],
                  ["2", "<code>anh_1.png bao_cao_1.txt</code>", "tên kết thúc bằng <code>_1.</code> rồi bất cứ gì: ảnh và báo cáo số 1"]]),
           """Đáp án câu một, dấu hỏi chỉ khớp đúng một ký tự, nên báo cáo số một và số hai được, còn số mười có hai ký tự bị loại.
           Câu hai, mẫu khớp mọi tên có gạch dưới một chấm, nên cả ảnh số một và báo cáo số một cùng được chọn.""",
           focus=["1.2", "1.3"]),
        st(term_block(quiz, 1, 5, title="Máy chạy thật")
           + "<div class='box key'><b>Quyết định:</b> chọn <code>rm bao_cao_*.txt</code> (3 tệp), vì <code>rm *.txt</code> xoá thêm <code>ghi_chu.txt</code> (4 tệp). "
             "Trước khi xoá, chạy <code>echo bao_cao_*.txt</code> để thấy đúng 3 tên.</div>",
           """Máy chạy thật cho cùng kết quả. Về quyết định, nên chọn mẫu báo cáo sao chấm t x t, vì mẫu sao chấm t x t sẽ xoá thêm cả ghi chú, tức bốn tệp thay vì ba.
           Và trước khi xoá, hãy chạy lệnh in chữ với đúng mẫu đó để thấy đúng ba tên.""", clear=True),
    ], checks=["len('bao_cao_1.txt bao_cao_2.txt'.split()) == 2", "len('bao_cao_1.txt bao_cao_10.txt bao_cao_2.txt'.split()) == 3",
               "len('bao_cao_1.txt bao_cao_10.txt bao_cao_2.txt ghi_chu.txt'.split()) == 4"])
    sc_prac = practice_scene(sc, "Tự làm: dựng cây cửa hàng, in bằng find", pr_steps(
        st, "FND", "L02",
        """<p><b>Đề</b>: tạo <code>dung.sh</code>, làm tuần tự, ở thư mục hiện tại:</p>
<ol><li><code>mkdir -p</code> tạo <code>cua_hang/kho</code> và <code>cua_hang/bao_cao</code>.</li>
<li>Trong <code>kho</code>: tạo <code>ao.txt</code>, <code>quan.txt</code>, <code>non.txt</code>.</li>
<li><code>bao_cao/tong.txt</code>: dòng <code>ao 5</code> (dùng <code>&gt;</code>) rồi <code>quan 3</code> (dùng <code>&gt;&gt;</code>).</li>
<li>Chép <code>ao.txt</code> thành <code>ao_sao.txt</code>; đổi tên <code>non.txt</code> thành <code>mu.txt</code>; xoá <code>quan.txt</code>.</li>
<li>In <code>find cua_hang | sort</code>, rồi <code>cat</code> tệp tổng.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Viết một tệp lệnh làm tuần tự. Tạo thư mục cửa hàng với hai thư mục con là kho và báo cáo. Trong kho tạo ba tệp áo, quần, nón.
        Ghi hai dòng vào tệp tổng, dòng đầu bằng một dấu, dòng sau bằng hai dấu. Chép tệp áo, đổi tên tệp nón, xoá tệp quần. Cuối cùng in cây bằng lệnh tìm, nối với lệnh xếp, rồi in nội dung tệp tổng.
        Lệnh xếp chỉ để các dòng theo thứ tự chữ cái. Hãy dừng video và làm.""",
        LAB_OUT, "dung.sh",
        """<div class="box key"><b>Nếu kẹt:</b> đọc đề từng dòng một, mỗi dòng là một lệnh. Tạo tệp dùng <code>touch</code> với đường dẫn đầy đủ, ví dụ <code>cua_hang/kho/ao.txt</code>.
Dòng đầu của tổng dùng một <code>&gt;</code>, dòng sau hai <code>&gt;&gt;</code>. Lời giải ở <code>labs/FND/L02/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, hãy đọc đề từng dòng, mỗi dòng là một lệnh. Tạo tệp thì dùng đường dẫn đầy đủ. Dòng đầu của tệp tổng dùng một dấu lớn hơn, dòng sau dùng hai dấu. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=180), "FND", "L02")
    write_lab("FND", "L02", """# Lab FND L02 — Dựng cây cửa hàng bằng tệp lệnh

Tạo `dung.sh` (làm trong thư mục hiện tại, tuần tự):
1. `mkdir -p`: tạo `cua_hang/kho` và `cua_hang/bao_cao`.
2. Trong `kho`: tạo ba tệp rỗng `ao.txt`, `quan.txt`, `non.txt`.
3. `cua_hang/bao_cao/tong.txt`: dòng `ao 5` bằng `>`, rồi dòng `quan 3` bằng `>>`.
4. Chép `ao.txt` thành `ao_sao.txt`; đổi tên `non.txt` thành `mu.txt`; xoá `quan.txt`.
5. In `find cua_hang | sort` (sort xếp các dòng theo chữ cái, để kết quả cố định), rồi `cat cua_hang/bao_cao/tong.txt`.

Chạy `bash dung.sh`; chấm: `bash labs/cham.sh FND L02 dung.sh`. Khác bài giảng: tên thư mục, tên tệp, số liệu.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("tạo: mkdir, touch", "ghi: &gt; ghi đè, &gt;&gt; nối", "đọc: cat", "chép cp, đổi tên mv, xoá rm (không hoàn tác)",
                 "* ? do cửa sổ lệnh mở ra", "xem trước bằng echo"),
           """Tổng kết chuỗi logic. Tạo bằng hai lệnh tạo thư mục và tạo tệp. Ghi bằng một dấu để ghi đè, hai dấu để nối. Đọc bằng lệnh in nội dung. Chép, đổi tên, xoá, và xoá thì không hoàn tác.
           Dấu sao và dấu hỏi do chương trình cửa sổ lệnh mở ra trước khi lệnh chạy, nên xem trước bằng lệnh in chữ."""),
        st("""<div class='box key'><b>Tư duy:</b> với mọi lệnh phá huỷ, làm ba việc: <b>xem trước</b> mẫu, <b>đếm</b> số tệp chạm tới, và hỏi “có bản sao ở nơi khác không?”.</div>
<p>Bài sau: đọc và lọc văn bản bằng ống, để trả lời “có bao nhiêu” và “dòng nào” trong tệp lớn.</p>""",
           """Điều cần mang theo, với mọi lệnh phá huỷ, hãy làm ba việc. Xem trước mẫu, đếm số tệp chạm tới, và hỏi có bản sao ở nơi khác không.
           Bài sau, ta học đọc và lọc văn bản bằng ống, để trả lời có bao nhiêu và dòng nào trong tệp lớn.""", forward_ref=True),
    ])
    return lesson("L02", "tep_va_thu_muc", "Bài 2 — Làm việc với tệp: tạo, ghi, chép, đổi tên, xoá",
                  "curriculum/fnd.yaml L02; audit/fnd/verify_fnd.py L02 (Git Bash chạy thật mkdir/touch/echo/cat/cp/mv/rm trong thư mục tạm); "
                  "GNU Coreutils manual (mkdir, touch, cp, mv, rm), GNU Bash Reference Manual (Redirections, Filename Expansion, Brace Expansion); "
                  "số tệp ×1 / ×100 / ×1 000 là số minh hoạ chạy thật bằng verify_fnd",
                  ["Nêu chức năng của các lệnh tạo thư mục, tạo tệp, in chữ, in nội dung, chép, di chuyển, xoá",
                   "Phân biệt một dấu lớn hơn (ghi đè) với hai dấu lớn hơn (nối thêm)",
                   "Giải thích dấu sao và dấu hỏi do chương trình cửa sổ lệnh mở ra và xem trước chúng bằng lệnh in chữ",
                   "Dựng, ghi, chép, đổi tên và xoá trong một cây thư mục bằng đúng lệnh",
                   "Đếm số tệp bị chạm tới bằng hai cách khác nhau",
                   "Chỉ ra ba lỗi hay gặp: dấu cách thừa, ghi đè nhầm, biến rỗng trong lệnh xoá",
                   "Viết tệp lệnh dựng một cây cửa hàng và in cây bằng lệnh tìm"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "sym"), (2, "intuition"), (3, "formula"), (4, "example"), (5, "check"), (6, "pitfalls"), (7, "practice")])
