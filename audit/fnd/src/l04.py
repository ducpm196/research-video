from lib import *
from labkit import write_lab, practice_steps, practice_scene

LAB_SOL = """git --version | cut -d' ' -f1-2
javac -version 2>&1 | cut -d. -f1
python --version | cut -d. -f1
ls . > /dev/null; echo "ls: $?"
ls khong_co 2> /dev/null; echo "ls loi: $?"
echo "so du" > tep.txt
grep -q tien tep.txt; echo "grep: $?"
mkdir tien_ich
echo 'echo xin chao tu tien_ich' > tien_ich/chao_ban
chmod +x tien_ich/chao_ban
PATH="$PWD/tien_ich:$PATH"
chao_ban"""
LAB_OUT = """git version
javac 21
Python 3
ls: 0
ls loi: 2
grep: 1
xin chao tu tien_ich"""
HOME_ = "/c/Users/ban"


def build():
    hook = cmd("PhienHook", [("chao.sh", "bash: chao.sh: command not found"), ("./chao.sh", "xin chao"), ("bash chao.sh", "xin chao")],
               files={"chao.sh": "echo xin chao\n"})
    bien = cmd("PhienBien", [
        ("TEN=ban", ""), ("echo $TEN", "ban"), ('echo "xin chao $TEN"', "xin chao ban"), ("echo 'xin chao $TEN'", "xin chao $TEN"),
        ("bash -c 'echo [$TEN]'", "[]"), ("export TEN", ""), ("bash -c 'echo [$TEN]'", "[ban]"),
    ])
    path = cmd("PhienPath", [
        ("PATH=/usr/bin:/bin", ""), ("echo $PATH | tr ':' '\\n'", "/usr/bin\n/bin"), ("chao", "bash: chao: command not found"),
        (f'PATH="{HOME_}/tien_ich:$PATH"', ""), ("echo $PATH | tr ':' '\\n'", f"{HOME_}/tien_ich\n/usr/bin\n/bin"), ("chao", "ban tien ich"),
        (f'PATH="{HOME_}/hai:$PATH"', ""), ("chao", "ban hai"), ("command -v chao", f"{HOME_}/hai/chao"),
    ], files={"tien_ich/chao": "echo ban tien ich\n", "hai/chao": "echo ban hai\n"})
    ma = cmd("PhienMa", [
        ("grep -q xin a.txt; echo $?", "0"), ("grep -q xyz a.txt; echo $?", "1"), ("ls khong_co 2> /dev/null; echo $?", "2"),
        ("khong_co_lenh 2> /dev/null; echo $?", "127"),
        ("grep -q xin a.txt && echo co || echo khong", "co"), ("grep -q xyz a.txt && echo co || echo khong", "khong"),
    ], files={"a.txt": "xin chao\n"})
    buoc = cmd("PhienE", [
        ("bash buoc.sh", "ls: cannot access 'khong_co': No such file or directory\nda xong"),
        ("bash buoc_e.sh; echo $?", "ls: cannot access 'khong_co': No such file or directory\n2"),
    ], files={"buoc.sh": "ls khong_co\necho da xong\n", "buoc_e.sh": "set -e\nls khong_co\necho da xong\n"})
    ong = cmd("PhienOng", [
        ("false | true; echo $?", "0"), ("set -o pipefail; false | true; echo $?", "1"),
    ])
    quiz = cmd("PhienQuiz", [
        ("chmod +x tien_ich/cat", ""),
        (f'PATH="{HOME_}/tien_ich:/usr/bin:/bin"', ""), ("cat a.txt", "gia cat"),
        (f'PATH="/usr/bin:/bin:{HOME_}/tien_ich"', ""), ("hash -r; cat a.txt", "xin chao"),
    ], files={"a.txt": "xin chao\n", "tien_ich/cat": "#!/bin/bash\necho gia cat\n"})
    ver = cmd("PhienVer", [("git --version | cut -d' ' -f1-2", "git version"), ("javac -version 2>&1 | cut -d. -f1", "javac 21"),
                           ("python --version | cut -d. -f1", "Python 3")])

    sc_hook = sc("hook", "hook", "Một tệp, ba cách gõ, hai kết quả: máy tìm lệnh ở đâu?", [
        st(term_block(hook, title="Tệp chao.sh có thật trong thư mục hiện tại")
           + "<p>Cùng một tệp, mà gõ <code>chao.sh</code> thì <b>“không tìm thấy lệnh”</b>, còn gõ <code>./chao.sh</code> hay <code>bash chao.sh</code> thì chạy.</p>",
           """Chào bạn, hãy nhìn một tệp lệnh nhỏ nằm ngay trong thư mục hiện tại. Gõ tên tệp trần trụi thì máy báo không tìm thấy lệnh. Gõ thêm dấu chấm gạch chéo phía trước, hoặc gọi qua chương trình cửa sổ lệnh, thì tệp chạy bình thường.
           Cùng một tệp mà ba cách gõ cho hai kết quả, và nguyên nhân nằm ở cách máy đi tìm lệnh."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Máy <b>tìm</b> một lệnh ở đâu, và <code>PATH</code> là gì?</li>
<li><b>Biến</b> là gì, <code>export</code> khác gì không có <code>export</code>?</li>
<li>Làm sao biết một lệnh <b>thành công hay thất bại</b> (mã thoát), và vì sao tự động hoá bắt buộc phải kiểm?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Máy tìm một lệnh ở đâu, và đường dẫn tìm lệnh là gì. Biến là gì, và thêm chữ xuất ra thì khác gì không thêm.
           Và làm sao biết một lệnh thành công hay thất bại, tức mã thoát, cùng lý do tự động hoá bắt buộc phải kiểm."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: lệnh, tệp lệnh, chuyển hướng, chỗ đứng", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① lệnh", "tên lệnh + các tham số, ví dụ <code>ls hoc</code>"],
                  ["② chỗ đứng", "lệnh in vị trí cho biết đang ở đâu; <code>./x</code> nghĩa là tệp <code>x</code> <b>ngay tại chỗ đứng</b>"],
                  ["③ tệp văn bản", "dựng bằng <code>echo \"…\" &gt; tep</code>, đọc bằng <code>cat</code>"],
                  ["④ ống và lỗi", "<code>A | B</code> nối lệnh; <code>2&gt; /dev/null</code> vứt thông báo lỗi"]]),
           """Ta ôn lại bốn điều. Lệnh gồm tên lệnh và các tham số. Chấm gạch chéo rồi tên nghĩa là tệp đó nằm ngay tại chỗ đứng. Tệp văn bản dựng bằng lệnh in chữ kèm dấu chuyển hướng.
           Và ống nối lệnh, còn chữ hai kèm dấu lớn hơn vứt thông báo lỗi vào thùng không đáy.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã: biến, PATH, mã thoát và hai dấu nối lệnh", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>TEN=ban</code>", "gán biến", "tạo <b>biến</b> (ô nhớ có tên) <code>TEN</code> chứa <code>ban</code>; <b>không</b> có khoảng trắng quanh dấu <code>=</code>"],
                  [code("$TEN"), "đọc biến", "dấu <b>đô la</b> lấy giá trị của biến; trong dấu nháy kép vẫn thay, trong dấu nháy đơn thì <b>giữ nguyên chữ</b>"],
                  ["<code>export TEN</code>", "xuất biến", "biến thành <b>biến môi trường</b>: các chương trình con sinh ra từ cửa sổ này cũng thấy"],
                  [code("echo $PATH"), "đường dẫn tìm lệnh", "<code>PATH</code> là một biến môi trường: danh sách thư mục, ngăn bằng dấu <code>:</code>, để máy tìm lệnh"]]),
           """Bảng này giải mã biến và đường dẫn tìm lệnh. Gán biến là tạo một ô nhớ có tên, và không có khoảng trắng quanh dấu bằng. Dấu đô la đọc giá trị của biến, trong dấu nháy kép vẫn thay, trong dấu nháy đơn thì giữ nguyên chữ.
           Lệnh xuất biến biến nó thành biến môi trường, để các chương trình con cũng thấy. Và đường dẫn tìm lệnh là một biến môi trường, chứa danh sách thư mục ngăn bằng dấu hai chấm.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["viết", "đọc là", "nghĩa"],
                 [[code("$?"), "mã thoát", "số của lệnh <b>vừa chạy xong</b>: <code>0</code> = thành công, <b>khác 0</b> = thất bại"],
                  ["<code>A &amp;&amp; B</code>", "và rồi", "chạy <code>B</code> <b>chỉ khi</b> <code>A</code> thành công (mã 0)"],
                  ["<code>A || B</code>", "hoặc không thì", "chạy <code>B</code> <b>chỉ khi</b> <code>A</code> thất bại (mã khác 0)"],
                  ["<code>set -e</code>", "dừng khi lỗi", "tệp lệnh <b>dừng ngay</b> khi một lệnh trả mã khác 0"]]),
           """Bảng thứ hai là mã thoát. Mỗi lệnh chạy xong để lại một con số, gọi là mã thoát, số không là thành công, khác không là thất bại, và dấu đô la hỏi chấm đọc nó. Hai dấu và nối hai lệnh, lệnh sau chỉ chạy khi lệnh trước thành công.
           Hai gạch đứng thì ngược lại, lệnh sau chỉ chạy khi lệnh trước thất bại. Còn lệnh đặt chế độ dừng khi lỗi làm tệp lệnh dừng ngay khi có một lệnh thất bại.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: máy dò thư mục theo thứ tự, và mã thoát điều khiển lệnh sau", [
        st(svg(1500, 400,
               box(20, 150, 250, 100, ["gõ:  chao", "(không có /)"], C_BLUE, bold=True),
               arrow(275, 200, 380, 200, "#2a78d6"),
               box(390, 40, 560, 80, "① …/hai → có tệp chao: DỪNG, chạy", C_GREEN, bold=True),
               box(390, 160, 560, 80, "② …/tien_ich → cũng có chao, không dò tới", C_GRAY, dash=True),
               box(390, 280, 560, 80, "③ /usr/bin   → không dò tới", C_GRAY, dash=True),
               arrow(280, 190, 385, 85, "#16a34a"),
               txt(145, 290, "dò lần lượt từ trên xuống", 22, "middle", "#2a78d6", True),
               box(1000, 40, 480, 100, ["thư mục ĐẦU danh sách thắng", "đặt thư mục của mình ở đầu: đè lệnh cũ"], C_AMBER),
               box(1000, 190, 480, 100, ["không thư mục nào có tên đó", "→ “command not found”, mã thoát 127"], C_RED),
               txt(1240, 340, "gõ ./chao: có dấu / nên KHÔNG dò, đi thẳng", 24, "middle", "#1f2937", True)),
           """Hình này là cách máy tìm lệnh. Bạn gõ một tên không có dấu gạch chéo. Máy dò lần lượt từng thư mục trong danh sách, và dừng ở thư mục đầu tiên có tệp tên đó. Các thư mục phía sau không được dò tới.
           Vì vậy thư mục đứng đầu thắng. Nếu không thư mục nào có, máy báo không tìm thấy lệnh và mã thoát là một trăm hai mươi bảy. Còn nếu tên có dấu gạch chéo thì máy không dò, mà đi thẳng tới đường dẫn đó."""),
        st(svg(1500, 340,
               box(20, 110, 230, 100, ["lệnh A"], C_BLUE, bold=True),
               arrow(255, 160, 380, 160, "#2a78d6"),
               box(390, 110, 280, 100, ["mã thoát", "của A"], C_AMBER, bold=True),
               arrow(675, 130, 800, 70, "#16a34a", "= 0"),
               box(810, 20, 330, 90, "A &amp;&amp; B: chạy B", C_GREEN, bold=True),
               arrow(675, 190, 800, 260, "#dc2626", "khác 0"),
               box(810, 220, 330, 90, "A || B: chạy B", C_RED, bold=True),
               txt(1320, 70, "thành công", 26, "middle", "#16a34a", True), txt(1320, 270, "thất bại", 26, "middle", "#dc2626", True)),
           """Hình thứ hai là mã thoát điều khiển lệnh sau. Lệnh A chạy xong để lại mã thoát. Nếu bằng không, thành công, thì hai dấu và cho chạy lệnh B. Nếu khác không, thất bại, thì hai gạch đứng mới cho chạy lệnh B.
           Nhờ vậy ta viết được cả nhánh làm tiếp lẫn nhánh xử lý lỗi ngay trên một dòng."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: máy chọn tệp nào để chạy", [
        st(term_block(path, 0, 3, title="Bước 1. Danh sách chỉ có hai thư mục hệ thống: không thấy chao")
           + "<p>Vì tên <code>chao</code> không có <code>/</code>, máy dò <b>từng thư mục trong <code>PATH</code></b>; hết danh sách mà không có nên báo lỗi.</p>",
           """Bước một, đặt đường dẫn tìm lệnh chỉ còn hai thư mục hệ thống. Vì tên chao không có dấu gạch chéo, nên máy dò từng thư mục trong danh sách. Hết danh sách mà không thấy, nên máy báo không tìm thấy lệnh."""),
        st(term_block(path, 3, 6, title="Bước 2. Thêm thư mục của mình vào ĐẦU danh sách")
           + "<p>Nên máy dò <code>tien_ich</code> trước, thấy <code>chao</code> và chạy nó: in <code>ban tien ich</code>.</p>",
           """Bước hai, thêm thư mục của mình vào đầu danh sách. Nên máy dò thư mục của ta trước, thấy tệp chao và chạy nó. Màn hình in ra dòng bạn tiện ích, đúng nội dung tệp."""),
        st(term_block(path, 6, 9, title="Bước 3. Hai thư mục cùng có chao: thư mục ĐỨNG TRƯỚC thắng")
           + "<p>Vì máy dừng ở thư mục đầu tiên có tệp, thêm <code>hai</code> lên đầu thì <code>chao</code> của <code>hai</code> chạy; <code>command -v</code> cho biết tệp nào sẽ chạy.</p>",
           """Bước ba, hai thư mục cùng có tệp chao. Vì máy dừng ở thư mục đầu tiên có tệp, nên khi thêm thư mục hai lên đầu, tệp chao của thư mục hai chạy. Lệnh hỏi đường dẫn cho biết đúng tệp nào sẽ được chạy, và đó là thư mục hai."""),
    ])
    sc_ex = sc("example", "example", "Ví dụ: biến, mã thoát, và tệp lệnh dừng khi lỗi, năm phép làm", [
        st(term_block(bien, 0, 4, title="① Đặt và đọc biến")
           + "<p>Dấu nháy <b>kép</b> thay <code>$TEN</code> bằng <code>ban</code>; dấu nháy <b>đơn</b> giữ nguyên chữ.</p>".replace("$", "<span>&#36;</span>"),
           """Phép làm thứ nhất, đặt và đọc biến. Gán biến ten bằng ban, rồi đọc bằng dấu đô la. Trong dấu nháy kép, biến được thay bằng giá trị. Trong dấu nháy đơn, chữ được giữ nguyên, không thay gì."""),
        st(term_block(bien, 4, 7, title="② Biến thường chỉ sống trong cửa sổ này; export cho con cháu")
           + "<p><code>bash -c '…'</code> chạy một cửa sổ lệnh <b>con</b>. Chưa <code>export</code>: con không thấy. Sau <code>export</code>: con thấy.</p>",
           """Phép làm thứ hai, biến và các chương trình con. Lệnh gọi chương trình cửa sổ lệnh kèm cờ c chạy một cửa sổ lệnh con. Khi chưa xuất, cửa sổ con không thấy biến, nên in ra rỗng. Sau khi xuất, nó thấy và in ra ban."""),
        st(term_block(ma, 0, 4, title="③ Mã thoát: 0 thành công, khác 0 thất bại")
           + "<p>Tìm thấy chữ: <code>0</code>. Không thấy: <code>1</code>. Thư mục không có: <code>2</code>. Lệnh không tồn tại: <code>127</code>.</p>",
           """Phép làm thứ ba, đọc mã thoát. Lệnh tìm thấy chữ thì trả không, không thấy thì trả một. Liệt kê một thư mục không có trả hai, và gõ một lệnh không tồn tại trả một trăm hai mươi bảy. Thông báo lỗi chỉ để người đọc, còn chương trình đọc con số."""),
        st(term_block(ma, 4, 6, title="④ Nối lệnh theo mã thoát: && và ||")
           + "<p>Lệnh tìm thấy chữ nên in <code>co</code>; lệnh không thấy nên rơi sang nhánh <code>||</code>, in <code>khong</code>.</p>",
           """Phép làm thứ tư, nối lệnh theo mã thoát. Khi tìm thấy chữ, mã là không, nên lệnh sau hai dấu và chạy, in có. Khi không thấy, mã khác không, nên rơi sang nhánh hai gạch đứng, in không."""),
        st(file_block(buoc, "buoc.sh", title="Tệp buoc.sh") + file_block(buoc, "buoc_e.sh", title="Tệp buoc_e.sh (thêm set -e)"),
           """Phép làm thứ năm, tệp lệnh dừng khi lỗi. Cả hai tệp đều có một lệnh sẽ thất bại, rồi in đã xong. Tệp thứ hai có thêm dòng đầu, chế độ dừng khi lỗi."""),
        st(term_block(buoc, title="Chạy cả hai"),
           """Tệp thứ nhất vẫn in đã xong, dù lệnh liệt kê đã lỗi, nên người đọc tưởng mọi việc ổn.
           Tệp thứ hai dừng ngay, không in đã xong, và mã thoát là hai, báo cho bên ngoài biết thất bại."""),
    ], checks=["'xin chao ' + 'ban' == 'xin chao ban'", "127 == 128 - 1", "[0, 1, 2, 127][-1] == 127"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: hỏi thẳng máy tệp nào sẽ chạy", [
        st(term_block(path, 8, 9, title="Hỏi bằng command -v (và type -t, which cho cùng ý)")
           + "<p>Kết quả trùng bước 3: là tệp trong <code>hai</code>, không phải <code>tien_ich</code>. Đây là cách kiểm <b>không cần chạy</b> lệnh.</p>",
           """Đường kiểm khác là hỏi thẳng máy tệp nào sẽ chạy, mà không cần chạy lệnh. Lệnh hỏi đường dẫn trả về tệp trong thư mục hai, trùng với kết quả ở bước ba, vì thư mục hai đứng trước."""),
        st(term_block(path, 1, 2, title="Đối chiếu danh sách đang có")
           + "<p>Đếm: danh sách có $2$ thư mục, thêm $2$ lần ở đầu thì có $4$; thư mục thêm sau cùng đứng đầu, nên thắng ✓</p>",
           """Kiểm thêm bằng cách đếm. Danh sách ban đầu có hai thư mục, ta thêm hai lần ở đầu nên có bốn. Thư mục thêm sau cùng đứng đầu danh sách, nên nó thắng, đúng như kết quả.""", clear=True),
    ], checks=["2 + 2 == 4"])
    sc_scale = sc("scale", "example", "Khi tệp lệnh dài ra: một lỗi bị bỏ qua lọt vào gần như chắc chắn", [
        st("""<p>Giả sử mỗi bước của một tệp lệnh tự động có xác suất thất bại chỉ $0{,}1\\%$ (số minh hoạ), các bước độc lập. Xác suất <b>có ít nhất một bước lỗi</b> trong $n$ bước:</p>
$$P = 1 - (1 - 0{,}001)^{n}$$
<p>Vì xác suất mọi bước đều tốt là $0{,}999^{n}$, nên phần còn lại là có ít nhất một lỗi.</p>""",
           """Giả sử mỗi bước của một tệp lệnh tự động có xác suất thất bại chỉ không phẩy một phần trăm, đây là số minh hoạ, và các bước độc lập. Vì xác suất mọi bước đều tốt là không phẩy chín chín chín mũ n, nên xác suất có ít nhất một bước lỗi là một trừ số đó."""),
        st(table(["số bước n", "tính", "xác suất có lỗi"],
                 [["×1: 10", "$1 - 0{,}999^{10}$", "<b>1,0%</b>"], ["×10: 100", "$1 - 0{,}999^{100}$", "<b>9,5%</b>"], ["×100: 1 000", "$1 - 0{,}999^{1000}$", "<b>63,2%</b>"]])
           + "<div class='box key'><b>Đánh đổi:</b> mười bước thì bỏ qua lỗi còn tạm chấp nhận; một nghìn bước thì lỗi gần như chắc chắn xảy ra, mà không ai biết bước nào. "
             "Tự động hoá càng lớn càng phải <b>dừng khi lỗi</b> (<code>set -e</code>), ghi mã thoát, và kiểm kết quả cuối.</div>",
           """Bảng này cho thấy tác động của quy mô. Mười bước thì xác suất có lỗi chỉ khoảng một phần trăm. Một trăm bước là chín phẩy năm phần trăm. Một nghìn bước là sáu mươi ba phẩy hai phần trăm, nghĩa là gần như chắc chắn có lỗi.
           Vì vậy tự động hoá càng lớn càng phải dừng khi lỗi, ghi lại mã thoát, và kiểm kết quả cuối, thay vì tin rằng không thấy báo lỗi nghĩa là đúng."""),
    ], checks=["round((1 - 0.999 ** 10) * 100, 1) == 1.0", "round((1 - 0.999 ** 100) * 100, 1) == 9.5", "round((1 - 0.999 ** 1000) * 100, 1) == 63.2"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên <code>./</code> khi chạy tệp ngay tại chỗ.</div>'
           + term_block(hook, 0, 2) + "<p>Tên trần trụi chỉ được dò trong <code>PATH</code>; thư mục hiện tại <b>không</b> nằm trong đó. Phép thử: <code>command -v</code> hoặc gõ <code>./</code>.</p>",
           """Lỗi thứ nhất, của người mới, là quên chấm gạch chéo khi chạy tệp ngay tại chỗ. Tên trần trụi chỉ được dò trong danh sách đường dẫn, mà thư mục hiện tại không nằm trong đó.
           Phép thử là hỏi lệnh hỏi đường dẫn, hoặc gõ thêm chấm gạch chéo."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Sửa <code>PATH</code> trong cửa sổ này rồi tưởng đã cài vĩnh viễn.</div>'
           + table(["việc làm", "sống tới khi nào"],
                   [[code('PATH="$HOME/tien_ich:$PATH"') + " gõ trong cửa sổ", "<b>đóng cửa sổ là mất</b>"],
                    ["ghi dòng đó vào tệp <code>~/.bashrc</code>", "<b>mỗi cửa sổ mới tự chạy</b> tệp này lúc mở"]]),
           """Lỗi thứ hai, cũng của người mới, là sửa đường dẫn trong cửa sổ này rồi tưởng đã cài vĩnh viễn. Cách gõ trực tiếp chỉ sống tới khi đóng cửa sổ.
           Muốn giữ lại, hãy ghi dòng đó vào tệp khởi động của cửa sổ lệnh, nằm trong thư mục nhà, vì mỗi cửa sổ mới tự chạy tệp này lúc mở."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Ống che mất lỗi: mã thoát của <code>A | B</code> là mã của <b>B</b>.</div>'
           + term_block(ong) + "<p>Lệnh <code>false</code> luôn thất bại, vậy mà cả ống báo $0$. Chế độ <code>set -o pipefail</code>: ống thất bại nếu <b>bất kỳ</b> lệnh nào trong đó thất bại.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là tin mã thoát của cả một ống. Mã thoát của ống chỉ là mã của lệnh cuối. Ở đây lệnh luôn thất bại đứng đầu, vậy mà cả ống báo không, tức thành công.
           Bật chế độ ống thất bại thì chỉ cần một lệnh trong ống lỗi là cả ống lỗi, và đó là thói quen của người viết tệp lệnh cẩn thận."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(file_block(quiz, "tien_ich/cat", title="Tệp tien_ich/cat: lệnh giả (dòng đầu #!/bin/bash: chạy bằng bash)")
           + "<p><b>Đề.</b> Thư mục <code>tien_ich</code> có tệp <code>cat</code> (lệnh giả, chỉ in <code>gia cat</code>). Hai cách đặt <code>PATH</code> (cùng thư mục hệ thống <code>/usr/bin:/bin</code>):</p>"
           + "<ol><li>A: <code>tien_ich</code> đứng <b>đầu</b> danh sách.</li><li>B: <code>tien_ich</code> đứng <b>cuối</b>.</li></ol>"
           + "<p>Gõ <code>cat a.txt</code> (tệp có chữ <code>xin chao</code>). In ra gì ở A, ở B? <b>Chọn</b> cách nào cho thư mục tiện ích của nhóm, vì sao?</p>",
           """Bây giờ tới phần bạn tự làm. Thư mục tiện ích có một tệp tên cát, là lệnh giả, chỉ in giả cát. Dòng đầu của nó, dấu thăng chấm than, cho biết tệp chạy bằng chương trình nào. Có hai cách đặt đường dẫn tìm lệnh, cùng hai thư mục hệ thống. Cách A đặt thư mục tiện ích ở đầu, cách B đặt ở cuối.
           Gõ lệnh in nội dung tệp a. Ở A và ở B máy in ra gì. Rồi chọn cách nào cho thư mục tiện ích của cả nhóm, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(term_block(quiz, 1, 5, title="Máy chạy thật")
           + "<p>A: thư mục tiện ích đứng trước nên <code>cat</code> giả thắng, in <code>gia cat</code>. B: đứng sau nên <code>cat</code> thật thắng, in <code>xin chao</code>.</p>",
           """Đáp án, ở cách A, thư mục tiện ích đứng trước nên lệnh giả thắng, màn hình in giả cát. Ở cách B, thư mục tiện ích đứng sau nên lệnh thật của hệ thống thắng, màn hình in xin chào."""),
        st("<div class='box key'><b>Quyết định:</b> chọn <b>B</b> (đặt cuối) cho thư mục dùng chung. Đặt đầu cho phép một tệp trùng tên "
           "<b>che lệnh hệ thống</b> mà không ai hay, và lỗi kiểu đó rất khó tìm. Chỉ đặt đầu khi bạn <b>cố ý</b> thay lệnh, và ghi rõ lý do.</div>",
           """Về quyết định, nên chọn cách B, đặt thư mục dùng chung ở cuối. Đặt ở đầu cho phép một tệp trùng tên che mất lệnh hệ thống mà không ai hay, và lỗi kiểu đó rất khó tìm.
           Chỉ đặt ở đầu khi bạn cố ý thay lệnh, và hãy ghi rõ lý do.""", clear=True),
    ], checks=["'gia cat' != 'xin chao'"])
    sc_prac = practice_scene(sc, "Tự làm: in phiên bản công cụ, mã thoát và một lệnh trong PATH", pr_steps(
        st, "FND", "L04",
        """<p><b>Đề</b>: tạo <code>kiem_tra.sh</code>, in lần lượt (bảy dòng):</p>
<ol><li>ba dòng tên và số phiên bản chính của <code>git</code>, <code>javac</code>, <code>python</code> (dùng <code>--version</code> / <code>-version</code>, <code>cut</code>);</li>
<li>mã thoát của <code>ls .</code> và của <code>ls khong_co</code> (giấu thông báo lỗi), dạng <code>ls: 0</code>, <code>ls loi: 2</code>;</li>
<li>mã thoát của <code>grep -q tien tep.txt</code> (tệp chỉ có chữ <code>so du</code>), dạng <code>grep: 1</code>;</li>
<li>tạo thư mục <code>tien_ich</code> với lệnh <code>chao_ban</code> (in <code>xin chao tu tien_ich</code>), thêm vào <code>PATH</code>, gọi <code>chao_ban</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh in bảy dòng. Ba dòng đầu là tên và số phiên bản chính của ba công cụ, dùng lệnh cắt để bỏ phần sau. Hai dòng nữa là mã thoát của lệnh liệt kê một thư mục có và một thư mục không có, giấu thông báo lỗi.
        Một dòng là mã thoát của lệnh tìm chữ không có trong tệp. Cuối cùng tạo thư mục tiện ích với một lệnh của riêng bạn, thêm vào đường dẫn tìm lệnh rồi gọi nó. Hãy dừng video và làm.""",
        LAB_OUT, "kiem_tra.sh",
        """<div class="box key"><b>Nếu kẹt:</b> <code>git --version | cut -d' ' -f1-2</code> lấy hai chữ đầu; <code>javac -version 2&gt;&amp;1 | cut -d. -f1</code> (lệnh in ra luồng lỗi, nên <code>2&gt;&amp;1</code>).
Mã thoát: <code>echo "ls: """ + "<span>&#36;</span>" + """?"</code> ngay sau lệnh. PATH: thêm <code>"<span>&#36;</span>PWD/tien_ich"</code> vào đầu. Lời giải ở <code>labs/FND/L04/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, cắt phiên bản bằng lệnh cắt, và nhớ lệnh biên dịch Java in phiên bản ra luồng lỗi nên cần nối luồng lỗi vào đầu ra. Mã thoát thì in ngay sau lệnh cần đo. Đường dẫn thì thêm thư mục tiện ích vào đầu danh sách.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L04")
    write_lab("FND", "L04", """# Lab FND L04 — Phiên bản công cụ, mã thoát và PATH

Tạo `kiem_tra.sh` in **bảy dòng**, đúng như `mong_doi.txt`:
1. ba dòng: tên và số phiên bản chính của `git` (`git version`), `javac` (`javac 21`), `python` (`Python 3`). Gợi ý: `git --version | cut -d' ' -f1-2`; `javac -version 2>&1 | cut -d. -f1`; `python --version | cut -d. -f1`.
2. `ls .` rồi in mã thoát dạng `ls: 0`; `ls khong_co` (giấu thông báo lỗi bằng `2> /dev/null`) rồi in `ls loi: 2`.
3. tạo `tep.txt` chỉ có chữ `so du`; `grep -q tien tep.txt` rồi in mã thoát dạng `grep: 1`.
4. tạo thư mục `tien_ich`, trong đó tệp `chao_ban` chứa lệnh `echo 'xin chao tu tien_ich'`; `chmod +x`; thêm `"$PWD/tien_ich"` vào **đầu** `PATH`; gọi `chao_ban`.

Chạy `bash kiem_tra.sh`; chấm: `bash labs/cham.sh FND L04 kiem_tra.sh`. Cần Git, JDK 21 và Python theo bài đầu tiên của khoá.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("tên không có /: dò từng thư mục trong PATH", "thư mục đứng trước thắng", "./tên: đi thẳng, không dò",
                 "biến: TEN=… rồi dùng đô la; export cho tiến trình con", "mã thoát: 0 tốt, khác 0 lỗi; &amp;&amp; và ||", "set -e, set -o pipefail: dừng khi lỗi"),
           """Tổng kết chuỗi logic. Tên không có dấu gạch chéo thì máy dò từng thư mục trong danh sách đường dẫn, thư mục đứng trước thắng. Có dấu gạch chéo thì đi thẳng.
           Biến đặt bằng dấu bằng, đọc bằng dấu đô la, và xuất để chương trình con thấy. Mã thoát không là tốt, khác không là lỗi, nối lệnh bằng hai dấu và hoặc hai gạch đứng. Tệp lệnh nên dừng khi lỗi."""),
        st("""<div class='box key'><b>Tư duy:</b> khi “lệnh không chạy” hay “chạy sai bản”, hỏi <code>command -v</code>; khi tự động hoá, đừng tin “không thấy báo lỗi”, hãy đọc mã thoát.</div>
<p>Bài sau: trình soạn mã, cách máy lưu chữ tiếng Việt, và cách đọc một thông báo lỗi thật.</p>""",
           """Điều cần mang theo, khi lệnh không chạy hoặc chạy sai bản, hãy hỏi lệnh hỏi đường dẫn. Khi tự động hoá, đừng tin là không thấy báo lỗi, hãy đọc mã thoát.
           Bài sau, ta học trình soạn mã, cách máy lưu chữ tiếng Việt, và cách đọc một thông báo lỗi thật.""", forward_ref=True),
    ])
    return lesson("L04", "chuong_trinh_path_ma_thoat", "Bài 4 — Chương trình, PATH, biến môi trường và mã thoát",
                  "curriculum/fnd.yaml L04; audit/fnd/verify_fnd.py L04 (Git Bash chạy thật PATH, biến, mã thoát, tệp lệnh); "
                  "GNU Bash Reference Manual (Shell Variables, Command Search and Execution, Exit Status, Lists of Commands, The Set Builtin: -e, pipefail); "
                  "xác suất 1 − (1 − p)^n là phép tính, p = 0,1% là số minh hoạ",
                  ["Giải thích máy tìm lệnh theo thứ tự các thư mục trong PATH và khác biệt của ./ khi chạy tệp",
                   "Đặt biến, đọc biến và phân biệt biến thường với biến môi trường",
                   "Đọc mã thoát của một lệnh và nối lệnh bằng hai dấu và, hai gạch đứng",
                   "Chạy tệp lệnh dừng khi lỗi và so với tệp không dừng",
                   "Kiểm tệp nào sẽ chạy bằng lệnh hỏi đường dẫn",
                   "Tính xác suất có ít nhất một bước lỗi khi tệp lệnh dài ra",
                   "Nêu cách chọn thứ tự thư mục trong PATH và chỉ ra ba lỗi hay gặp",
                   "Viết tệp lệnh in phiên bản công cụ, mã thoát và gọi một lệnh đặt trong PATH"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "formula"), (2, "example"), (3, "example"), (4, "example"), (5, "check"), (6, "scale"), (7, "quiz"), (8, "practice")])
