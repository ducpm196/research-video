from lib import *
from labkit import write_lab, practice_steps, practice_scene

FILES = {"anh/meo.png": "x", "anh/cho.png": "x", "hoc/ghichu.txt": "x", "hoc/nen/bai1.txt": "x", "hoc/nen/bai2.txt": "x",
         "hoc/toan/loi.txt": "x", "tai_ve/phim.mp4": "x", ".bashrc": ""}

SETUP = """mkdir -p vp/kho/a vp/kho/b vp/ho_so
touch vp/kho/a/x.txt vp/kho/b/y.txt vp/kho/b/z.txt vp/ho_so/hd.txt
cd vp/kho/b"""
LAB_BODY = """ls
cd ../../ho_so
ls
cd ../kho/a
ls
ls .."""
LAB_OUT = "y.txt\nz.txt\nhd.txt\nx.txt\na\nb"

CAY = [(0, "ban", "d"), (1, "anh", "d"), (2, "meo.png", "f"), (2, "cho.png", "f"), (1, "hoc", "d"), (2, "ghichu.txt", "f"),
       (2, "nen", "d"), (3, "bai1.txt", "f"), (3, "bai2.txt", "f"), (2, "toan", "d"), (3, "loi.txt", "f"), (1, "tai_ve", "d"), (2, "phim.mp4", "f")]


def cay(hi, note=None, w=1500):
    parts = []
    nodes = CAY
    pos = []
    stack = {}
    for i, (dep, name, kind) in enumerate(nodes):
        x, y = 30 + dep * 300, 8 + i * 50
        pos.append((x, y))
        stack[dep] = i
        if dep > 0:
            px, py = pos[stack[dep - 1]]
            parts.append(f'<path d="M{px + 16},{py + 38} L{px + 16},{y + 18} L{x - 6},{y + 18}" fill="none" stroke="#6b7280" stroke-width="3"/>')
    for i, (dep, name, kind) in enumerate(nodes):
        x, y = pos[i]
        col = C_AMBER if hi == i else (C_BLUE if kind == "d" else C_GRAY)
        label = ("▸ " if kind == "d" else "") + name
        width = max(120, int(len(label) * 15) + 26)
        parts.append(box(x, y, width, 38, label, col, 22, bold=(hi == i)))
    if note:
        parts.append(note)
    return svg(w, 668, *parts)


def build():
    phien = cmd("PhienDi", [
        ("pwd", "/c/Users/ban"),
        ("ls", "anh/  hoc/  tai_ve/"),
        ("ls -a", "./  ../  .bashrc  anh/  hoc/  tai_ve/"),
        ("ls hoc", "ghichu.txt  nen/  toan/"),
        ("cd hoc", ""),
        ("pwd", "/c/Users/ban/hoc"),
        ("cd nen", ""),
        ("pwd", "/c/Users/ban/hoc/nen"),
        ("cd ../../anh", ""),
        ("pwd", "/c/Users/ban/anh"),
        ("ls", "cho.png  meo.png"),
        ("cd", ""),
        ("pwd", "/c/Users/ban"),
    ], files=FILES)
    hook = cmd("PhienHook", [("ls /c/Users/anhA/du_lieu.csv", "ls: cannot access '/c/Users/anhA/du_lieu.csv': No such file or directory")], files=FILES)
    kiem = cmd("PhienKiem", [("cd /c/Users/ban/anh", ""), ("pwd", "/c/Users/ban/anh"),
                             ("cd /c/Users/ban/hoc/nen", ""), ("cd ../../anh", ""), ("pwd", "/c/Users/ban/anh")], files=FILES)
    loi = cmd("PhienLoi", [
        ("mkdir 'Tai lieu'", ""),
        ("cd Tai lieu", "bash: cd: too many arguments"),
        ("cd 'Tai lieu'", ""),
        ("pwd", "/c/Users/ban/Tai lieu"),
        ("cd ~", ""),
        ("cd C:\\Users\\ban", "bash: cd: C:Usersban: No such file or directory"),
        ("cd HOC", ""),
        ("pwd", "/c/Users/ban/HOC"),
    ], files=FILES)
    quiz = cmd("PhienQuiz", [
        ("cd hoc/toan", ""), ("cd ..", ""), ("pwd", "/c/Users/ban/hoc"), ("cd nen", ""), ("pwd", "/c/Users/ban/hoc/nen"),
        ("cd ../../anh", ""), ("pwd", "/c/Users/ban/anh"), ("cd", ""), ("pwd", "/c/Users/ban"),
        ("cd hoc/toan", ""), ("pwd", "/c/Users/ban/hoc/toan"),
    ], files=FILES)

    sc_hook = sc("hook", "hook", "Lệnh chạy được trên máy bạn, báo lỗi trên máy người khác: vì sao?", [
        st(term_block(hook, title="Máy của bạn Lan, chép lệnh của anh A")
           + "<p>Tệp <code>du_lieu.csv</code> có thật, nhưng nằm ở máy anh A. Dòng báo lỗi nghĩa là: "
             "<b>“không có tệp hay thư mục như vậy”</b>.</p>",
           """Chào bạn, hãy nhìn tình huống này. Anh A viết một lệnh đọc tệp dữ liệu, chạy tốt trên máy anh. Bạn Lan chép nguyên lệnh sang máy mình và nhận về một dòng báo lỗi bằng tiếng Anh.
           Dòng đó nghĩa là không có tệp hay thư mục như vậy. Tệp vẫn có thật, nhưng nằm ở máy anh A, vì đường dẫn đã ghi cứng tên thư mục của anh ấy."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Cửa sổ lệnh cho bạn thấy <b>đang đứng ở đâu</b> trong máy bằng cách nào?</li>
<li>Làm sao <b>đi</b> tới thư mục khác, và <b>nhìn</b> xem trong đó có gì?</li>
<li>Vì sao đường dẫn <b>tuyệt đối</b> hay hỏng khi chép sang máy khác, còn <b>tương đối</b> thì sao?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Cửa sổ lệnh cho bạn thấy đang đứng ở đâu trong máy bằng cách nào. Làm sao đi tới thư mục khác và nhìn xem trong đó có gì.
           Và vì sao đường dẫn tuyệt đối hay hỏng khi chép sang máy khác, còn đường dẫn tương đối thì sao."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp, thư mục và cây", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tệp", "dữ liệu có tên, ví dụ <code>meo.png</code> (đuôi <code>.png</code> cho biết loại)"],
                  ["② thư mục", "ngăn chứa tệp <b>và cả thư mục khác</b>, ví dụ <code>anh</code> chứa hai ảnh"],
                  ["③ cây thư mục", "thư mục nằm trong thư mục, vẽ thành cây lộn ngược; gốc ở trên, lá là tệp"],
                  ["④ Explorer", "chương trình duyệt thư mục của Windows, địa chỉ viết <code>C:\\Users\\ban\\anh</code>"]]),
           """Ta ôn lại bốn điều. Tệp là dữ liệu có tên, phần đuôi sau dấu chấm cho biết loại tệp. Thư mục là ngăn chứa tệp và cả thư mục khác.
           Thư mục nằm trong thư mục tạo thành cây lộn ngược, gốc ở trên, lá là tệp. Và trình duyệt thư mục của hệ điều hành là chương trình bạn đã dùng hằng ngày.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã dấu nhắc, ba lệnh đầu tiên và các dấu của đường dẫn", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>$</code>", "dấu nhắc", "máy đang chờ bạn gõ; <b>không gõ</b> dấu này"],
                  ["<code>pwd</code>", "lệnh in vị trí", "cho biết <b>đang đứng ở đâu</b>"],
                  ["<code>ls</code>", "lệnh liệt kê", "cho biết <b>trong đây có gì</b>"],
                  ["<code>cd hoc</code>", "lệnh đổi thư mục", "<b>đi vào</b> thư mục tên hoc; <code>hoc</code> là một <b>tham số</b>"]])
           + "<span class='note'>Lệnh = tên lệnh + các tham số, cách nhau bằng khoảng trắng; bấm phím xuống dòng để chạy.</span>",
           """Bảng này giải mã dấu nhắc và ba lệnh đầu tiên. Dấu nhắc là chỗ máy đang chờ bạn gõ, và bạn không gõ dấu này. Lệnh in vị trí cho biết bạn đang đứng ở đâu.
           Lệnh liệt kê cho biết trong đây có gì. Lệnh đổi thư mục đi vào thư mục có tên đứng sau, và tên đó gọi là tham số.
           Một lệnh gồm tên lệnh và các tham số, cách nhau bằng khoảng trắng, rồi bấm phím xuống dòng để chạy.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", 2]),
        st(table(["viết", "nghĩa", "ví dụ"],
                 [["<code>/</code>", "<b>gốc</b> của cây, và dấu ngăn các cấp", "<code>/c/Users/ban</code>"],
                  ["<code>~</code>", "thư mục <b>nhà</b> của bạn", "<code>/c/Users/ban</code>"],
                  ["<code>.</code>", "thư mục <b>hiện tại</b>", "<code>ls .</code> = <code>ls</code>"],
                  ["<code>..</code>", "thư mục <b>cha</b>, lên một cấp", "<code>cd ..</code>"]]),
           """Bảng thứ hai là các dấu của đường dẫn. Dấu gạch chéo là gốc của cả cây, và cũng là dấu ngăn các cấp. Dấu ngã là thư mục nhà của bạn.
           Một dấu chấm là thư mục hiện tại. Hai dấu chấm là thư mục cha, lên một cấp.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
        st(table(["viết", "nghĩa"],
                 [["<code>-a</code>", "<b>cờ</b> = tuỳ chọn của lệnh; <code>ls -a</code> hiện cả <b>tệp ẩn</b> (tên bắt đầu bằng dấu chấm)"],
                  ["<code>C:\\Users\\ban</code> ↔ <code>/c/Users/ban</code>", "Windows viết <code>\\</code> và chữ ổ đĩa; Git Bash viết <code>/</code>: ổ C là <code>/c</code>, ổ D là <code>/d</code>"]]),
           """Bảng cuối có hai điều nữa. Dấu gạch ngang kèm chữ là cờ, một tuỳ chọn của lệnh, ví dụ cờ a hiện cả tệp ẩn, tên bắt đầu bằng dấu chấm.
           Và hệ điều hành của máy dùng gạch chéo ngược cùng chữ ổ đĩa, còn cửa sổ lệnh dùng gạch chéo xuôi, ổ C viết là gạch chéo c.""",
           focus=[1, "1.2", "1.3"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: cây thư mục và chỗ bạn đang đứng", [
        st(cay(0, txt(1100, 120, "đang đứng: thư mục nhà", 30, "middle", "#d97706", True)
               + txt(1100, 165, "pwd → /c/Users/ban", 28, "middle", "#1f2937")
               + txt(1100, 230, "ls hiện: anh/  hoc/  tai_ve/", 28, "middle", "#1f2937")),
           """Hình này là cây thư mục của một thư mục nhà tên là ban. Ô màu cam là chỗ bạn đang đứng, lúc mở cửa sổ lệnh thì đó là thư mục nhà.
           Lệnh in vị trí cho ra đường dẫn từ gốc xuống chỗ đứng. Lệnh liệt kê chỉ cho thấy những gì nằm ngay dưới chỗ đứng, tức ba thư mục con, chưa thấy các tệp ở sâu hơn."""),
        st(cay(6, txt(1100, 120, "sau: cd hoc  rồi  cd nen", 28, "middle", "#d97706", True)
               + txt(1100, 170, "đường dẫn = đi từ gốc xuống,", 26, "middle", "#1f2937")
               + txt(1100, 205, "mỗi cấp cách nhau một dấu /", 26, "middle", "#1f2937")
               + txt(1100, 260, "/c/Users/ban/hoc/nen", 28, "middle", "#d97706", True)),
           """Sau khi đi vào hoc rồi vào nen, chỗ đứng chuyển xuống ô cam mới. Đường dẫn của nó là chuỗi các thư mục đi từ gốc xuống, mỗi cấp cách nhau một dấu gạch chéo.
           Đọc đường dẫn từ trái sang phải giống như đi theo cây từ trên xuống dưới."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: hai cách viết đường dẫn", [
        st("""<p><b>Bước 1. Tuyệt đối.</b> Bắt đầu bằng <code>/</code> (hoặc <code>~</code>): luôn đếm từ <b>gốc</b>, nên cùng một đường dẫn trỏ cùng một chỗ dù bạn đang đứng đâu.</p>
<p class="note">Làm thử: <code>cd /c/Users/ban/anh</code> luôn tới <code>anh</code>, đứng ở đâu cũng vậy ✓</p>""",
           """Bước một, đường dẫn tuyệt đối. Nó bắt đầu bằng dấu gạch chéo hoặc dấu ngã, nên luôn đếm từ gốc. Vì vậy cùng một đường dẫn trỏ cùng một chỗ, dù bạn đang đứng đâu.
           Làm thử, đi tới thư mục anh bằng đường dẫn tuyệt đối thì lúc nào cũng tới đúng chỗ đó."""),
        st("""<p><b>Bước 2. Tương đối.</b> Không bắt đầu bằng <code>/</code>: đếm từ <b>chỗ đang đứng</b>, nên cùng một chữ ở hai chỗ đứng khác nhau trỏ hai nơi khác nhau.</p>
<p class="note">Làm thử: đứng ở <code>ban</code>, <code>cd hoc</code> tới <code>ban/hoc</code>; đứng ở <code>anh</code> thì <code>cd hoc</code> báo lỗi vì không có <code>hoc</code> ở đó ✓</p>""",
           """Bước hai, đường dẫn tương đối. Nó không bắt đầu bằng dấu gạch chéo, nên đếm từ chỗ đang đứng. Vì vậy cùng một chữ, ở hai chỗ đứng khác nhau, trỏ hai nơi khác nhau.
           Làm thử, đứng ở thư mục nhà thì đi vào hoc được, nhưng đứng ở thư mục anh thì báo lỗi, vì ở đó không có hoc."""),
        st("""<p><b>Bước 3. Lùi bằng <code>..</code>.</b> Mỗi <code>..</code> lùi một cấp, nên số lần lùi bằng hiệu độ sâu:</p>
$$\\text{số lần lùi} = \\text{độ sâu chỗ đứng} - \\text{độ sâu của thư mục chung}$$
<p class="note">Làm thử: từ <code>/c/Users/ban/hoc/nen</code> (độ sâu 5) tới <code>anh</code> cần lùi tới <code>ban</code> (độ sâu 3): lùi $5 - 3 = 2$ lần, nên <code>../../anh</code> ✓</p>""",
           """Bước ba, lùi bằng hai dấu chấm. Mỗi lần lùi một cấp, nên số lần lùi bằng độ sâu của chỗ đứng trừ độ sâu của thư mục chung.
           Làm thử, từ nen có độ sâu năm, muốn tới anh thì phải lùi tới ban có độ sâu ba, tức năm trừ ba bằng hai lần. Vậy đường đi là lùi hai lần rồi xuống anh.""",
           ),
    ], checks=["5 - 3 == 2", "len('c/Users/ban/hoc/nen'.split('/')) == 5", "len('c/Users/ban'.split('/')) == 3"])
    sc_ex = sc("example", "example", "Ví dụ: đi một vòng trong thư mục nhà, năm phép đi", [
        st(term_block(phien, 0, 4, title="① Đứng ở nhà, nhìn quanh")
           + "<p class='note'>Dấu <code>/</code> sau tên là của Git Bash: đánh dấu đây là <b>thư mục</b>. Máy bạn có thể có thêm tệp ẩn.</p>",
           """Phép thứ nhất, nhìn quanh. Lệnh in vị trí cho ra đường dẫn đi từ ổ C, qua thư mục người dùng, tới ban, tức bạn đang ở thư mục nhà. Lệnh liệt kê cho ba thư mục.
           Cờ a hiện thêm tệp ẩn bắt đầu bằng dấu chấm, và cả hai mục đặc biệt là một dấu chấm và hai dấu chấm. Cửa sổ lệnh thêm dấu gạch chéo sau tên để đánh dấu đó là thư mục.""",
           ),
        st(term_block(phien, 4, 8, title="② Đi xuống hai cấp: hoc rồi nen")
           + "<p>Mỗi lệnh đổi thư mục <b>im lặng</b> khi thành công; muốn thấy chỗ đứng, hỏi vị trí.</p>",
           """Phép thứ hai, đi xuống hai cấp. Lệnh đổi thư mục vào hoc không in gì, vì khi thành công nó im lặng. Muốn thấy chỗ đứng, ta hỏi lại vị trí, và đường dẫn dài thêm một cấp.
           Rồi đi tiếp vào nen, đường dẫn lại dài thêm một cấp nữa."""),
        st(term_block(phien, 8, 11, title="③ Lùi hai cấp rồi xuống anh")
           + "<p>Từ <code>nen</code>, <code>../../anh</code> = lùi 2 cấp tới <code>ban</code>, rồi vào <code>anh</code>.</p>",
           """Phép thứ ba, lùi hai cấp rồi xuống anh. Từ nen, hai dấu chấm lùi tới hoc, hai dấu chấm nữa lùi tới ban, rồi đi vào anh. Vị trí in ra đúng là gạch chéo ban gạch chéo anh, khớp với phép tính ở bước ba.""",
           focus=[1, 2, 3]),
        st(term_block(phien, 10, 11, title="④ Nhìn trong anh") + "<p>Trong <code>anh</code> chỉ có hai tệp ảnh.</p>",
           """Phép thứ tư, nhìn xem trong anh có gì. Lệnh liệt kê cho thấy hai tệp ảnh, không có dấu gạch chéo vì chúng là tệp, không phải thư mục.""", clear=True),
        st(term_block(phien, 11, 13, title="⑤ Về nhà bằng một lệnh")
           + "<p>Lệnh đổi thư mục <b>không có tham số</b> đưa bạn về thư mục nhà, từ bất cứ đâu.</p>",
           """Phép thứ năm, về nhà. Lệnh đổi thư mục không kèm tham số nào đưa bạn về thư mục nhà, từ bất cứ đâu. Vị trí in ra lại là thư mục ban, và vòng đi của ta khép kín."""),
    ], checks=["'/c/Users/ban/hoc/nen'.count('/') == 5", "5 - 3 == 2", "'/c/Users/ban/anh'.split('/')[-1] == 'anh'"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: cùng đích, hai cách đi", [
        st(term_block(kiem, 0, 2, title="Cách 1: đường tuyệt đối") + term_block(kiem, 2, 5, title="Cách 2: tương đối từ nen"),
           """Đường kiểm khác, đi tới cùng một đích bằng hai cách. Cách một, dùng đường dẫn tuyệt đối tới anh, vị trí in ra là gạch chéo ban gạch chéo anh.
           Cách hai, đứng ở nen rồi dùng đường dẫn tương đối lùi hai cấp. Vị trí in ra giống hệt, nên hai cách trỏ cùng một chỗ."""),
        st("""<p>Kiểm bằng đếm: độ sâu <code>nen</code> là $5$, độ sâu <code>ban</code> là $3$, nên lùi $5 - 3 = \\hl{2}$ lần, đúng hai dấu <code>..</code> trong <code>../../anh</code> ✓</p>""",
           """Kiểm thêm bằng cách đếm. Độ sâu của nen là năm, độ sâu của ban là ba, nên phải lùi năm trừ ba bằng hai lần. Trong đường dẫn có đúng hai dấu chấm, nên số lần lùi khớp.""", clear=True),
    ], checks=["5 - 3 == 2", "'../../anh'.count('..') == 2"])
    sc_scale = sc("scale", "concept", "Khi cây lớn dần: đường dẫn dài ra, thư mục đầy lên", [
        st(table(["số cấp", "độ dài đường dẫn", "so với giới hạn 260"],
                 [["×1: 4 cấp", "3 + 9 × 4 − 1 = 38 ký tự", "còn dư nhiều"],
                  ["×7: 28 cấp", "3 + 9 × 28 − 1 = 254 ký tự", "sát giới hạn"],
                  ["×7,25: 29 cấp", "3 + 9 × 29 − 1 = 263 ký tự", "<b>vượt</b>"]])
           + "<span class='note'>Số minh hoạ: mỗi cấp 8 ký tự tên + 1 dấu ngăn; 3 ký tự đầu là <code>C:\\</code>. Giới hạn 260 (MAX_PATH) là mặc định của Windows.</span>",
           """Bảng này cho thấy điều gì xảy ra khi cây lớn dần. Mỗi cấp thêm chín ký tự, tám cho tên và một cho dấu ngăn. Bốn cấp chỉ dài ba mươi tám ký tự, rất dư.
           Hai mươi tám cấp dài hai trăm năm mươi bốn, sát giới hạn mặc định của hệ điều hành. Hai mươi chín cấp dài hai trăm sáu mươi ba, vượt giới hạn, và nhiều chương trình sẽ báo lỗi.""",
           focus=[1, 1, "1.2", "1.3", "1.4"]),
        st(table(["tệp trong một thư mục", "dòng do lệnh liệt kê in ra", "cách xử lý"],
                 [["×1: 10", "10 dòng, đọc được", "nhìn là đủ"],
                  ["×100: 1 000", "1 000 dòng, cuộn mãi", "lọc theo tên"],
                  ["×10 000: 100 000", "100 000 dòng, chỉ đọc nổi vài chục", "lọc, đếm, tìm"]]),
           """Bảng thứ hai là số tệp trong một thư mục. Mười tệp thì đọc bằng mắt được. Một nghìn tệp thì cuộn mãi. Một trăm nghìn tệp thì màn hình chỉ đọc nổi vài chục dòng.""",
           focus=[1, "1.2", "1.3", "1.4"]),
        st("<div class='box key'><b>Đánh đổi:</b> tên ngắn và cây nông thì dễ gõ; chia nhỏ thư mục theo chủ đề thì dễ tìm. "
           "Cách cũ “nhìn bằng mắt” gãy ở quy mô lớn, nên người ta cần các lệnh lọc.</div>",
           """Cách nhìn bằng mắt gãy ở quy mô lớn, nên người ta cần các lệnh lọc. Người làm nghề phải cân giữa tên ngắn, cây nông dễ gõ, và chia thư mục theo chủ đề dễ tìm.""", clear=True),
    ], checks=["3 + 9 * 4 - 1 == 38", "3 + 9 * 28 - 1 == 254", "3 + 9 * 29 - 1 == 263", "263 > 260 > 254"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Tên thư mục có <b>khoảng trắng</b>: máy hiểu là hai tham số.</div>'
           + term_block(loi, 0, 4)
           + "<p>Bọc tên trong dấu nháy: <code>'Tai lieu'</code>. Tốt hơn: đặt tên không dấu, không khoảng trắng, ví dụ <code>tai_lieu</code>.</p>",
           """Lỗi thứ nhất, của người mới, là tên thư mục có khoảng trắng. Máy hiểu Tai và lieu là hai tham số, nên báo có quá nhiều tham số.
           Cách chữa là bọc tên trong dấu nháy. Cách tốt hơn là đặt tên không dấu, không khoảng trắng, ví dụ nối bằng dấu gạch dưới."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Chép đường dẫn Windows có <code>\\</code> vào Git Bash.</div>'
           + term_block(loi, 4, 6)
           + "<p>Trong Git Bash, <code>\\</code> là ký tự thoát: nó <b>nuốt</b> chữ đứng sau, nên <code>C:\\Users\\ban</code> thành <code>C:Usersban</code>. Dùng <code>/c/Users/ban</code>.</p>",
           """Lỗi thứ hai, của người mới, là chép đường dẫn kiểu hệ điều hành của máy, có gạch chéo ngược, vào cửa sổ lệnh. Ở đây gạch chéo ngược có nghĩa khác, nó nuốt chữ đứng sau.
           Vì vậy các chữ bị dính lại thành một tên lạ, và máy báo không có. Hãy đổi sang gạch chéo xuôi, ổ C viết là gạch chéo c."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Máy Windows chấp nhận <code>HOC</code> thay <code>hoc</code>; máy chủ Linux thì không.</div>'
           + term_block(loi, 6, 8)
           + "<p>Hệ tệp Windows thường <b>không phân biệt</b> hoa thường; Linux <b>có phân biệt</b>. Lệnh chạy tốt ở máy bạn có thể hỏng khi đưa lên máy chủ.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là gõ hoa thường tuỳ tiện. Trên máy của bạn, gõ chữ hoa thay cho chữ thường vẫn vào được, nên bạn không nhận ra sai.
           Nhiều máy chủ phân biệt chữ hoa và chữ thường, và sẽ báo không có thư mục đó. Vì vậy hãy luôn gõ đúng hoa thường như tên thật, ngay từ trên máy bạn."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Cây ở sơ đồ trên; bạn đang đứng ở <code>/c/Users/ban/hoc/toan</code>. Gõ lần lượt các lệnh dưới đây, ghi lại vị trí sau mỗi lệnh.</p>
<ol><li><code>cd ..</code></li><li><code>cd nen</code></li><li><code>cd ../../anh</code></li><li><code>cd</code></li><li><code>cd hoc/toan</code></li></ol>
<p><b>Quyết định:</b> bạn gửi tệp lệnh cho bạn cùng lớp tên khác. Trong đó nên viết <code>cd /c/Users/ban/anh</code> hay <code>cd ../../anh</code>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Bạn đang đứng ở thư mục toan, nằm trong hoc, nằm trong ban. Gõ lần lượt năm lệnh đổi thư mục trên màn hình, và ghi lại vị trí sau mỗi lệnh.
           Sau đó là một quyết định. Bạn gửi tệp lệnh cho bạn cùng lớp có tên khác, nên viết đường dẫn tuyệt đối tới anh hay đường dẫn tương đối, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["lệnh", "vị trí sau lệnh", "lý do"],
                 [["① <code>cd ..</code>", "<code>/c/Users/ban/hoc</code>", "lùi một cấp từ toan"],
                  ["② <code>cd nen</code>", "<code>/c/Users/ban/hoc/nen</code>", "xuống nen, nằm trong hoc"],
                  ["③ <code>cd ../../anh</code>", "<code>/c/Users/ban/anh</code>", "lùi hai cấp tới ban, rồi xuống anh"],
                  ["④ <code>cd</code>", "<code>/c/Users/ban</code>", "không tham số: về nhà"],
                  ["⑤ <code>cd hoc/toan</code>", "<code>/c/Users/ban/hoc/toan</code>", "xuống hai cấp một lần"]]),
           """Đáp án từng bước. Lệnh một lùi một cấp từ toan, vào hoc. Lệnh hai xuống nen. Lệnh ba lùi hai cấp tới ban, rồi xuống anh.
           Lệnh bốn không có tham số nên về nhà. Lệnh năm xuống hai cấp liền, về lại toan, đúng chỗ bắt đầu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st(term_block(quiz, 2, 11, title="Máy chạy lại đúng các lệnh đó (kèm vị trí)"),
           """Máy chạy lại đúng các lệnh đó, và vị trí in ra khớp từng dòng với đáp án của bạn.""", clear=True),
        st("<div class='box key'><b>Quyết định:</b> đường dẫn <b>tuyệt đối</b> chứa tên <code>ban</code> nên hỏng trên máy khác. "
           "Đường tương đối <code>../../anh</code> chạy được trên mọi máy, miễn là chạy từ đúng thư mục <code>nen</code>; "
           "vì thế tệp lệnh tốt tự đổi về thư mục của chính nó trước.</div>",
           """Về quyết định, đường dẫn tuyệt đối chứa tên ban nên hỏng trên máy khác. Đường dẫn tương đối chạy được trên mọi máy, miễn là chạy từ đúng thư mục nen.
           Vì vậy tệp lệnh tốt tự đổi về thư mục của chính nó trước. Cách làm có khi ta học chạy tệp lệnh.""", clear=True),
    ], checks=["'/c/Users/ban/hoc/toan'.count('/') == 5"])
    sc_prac = practice_scene(sc, "Tự làm: đi theo cây, nhìn bằng ls", pr_steps(
        st, "FND", "L01",
        """<p><b>Đề</b>: tạo tệp <code>di.sh</code> gồm đoạn dựng cây (chép nguyên) rồi các lệnh của bạn.</p>
<div class="code">""" + "".join(f"<div>{esc(l)}</div>" for l in SETUP.split("\n")) + """</div>
<ol><li>Đang đứng ở <code>b</code>: in nội dung <code>b</code>.</li>
<li>Chỉ dùng <b>đường tương đối</b> tới <code>ho_so</code>, in nội dung.</li>
<li>Từ <code>ho_so</code> tới <code>a</code>, in nội dung.</li>
<li>In nội dung thư mục <b>cha</b> của <code>a</code> (không cần đi tới đó).</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh, bắt đầu bằng đoạn dựng cây trên màn hình, chép nguyên, bạn chưa cần hiểu các lệnh đó. Rồi viết các lệnh của bạn.
        Đang đứng ở thư mục b, hãy liệt kê nội dung của nó. Chỉ dùng đường dẫn tương đối để tới thư mục ho sơ và liệt kê. Từ đó tới thư mục a và liệt kê.
        Cuối cùng liệt kê thư mục cha của a mà không cần đi tới đó. Hãy dừng video và làm.""",
        LAB_OUT, "di.sh",
        """<div class="box key"><b>Nếu kẹt:</b> từ <code>b</code> tới <code>ho_so</code> phải lùi hai cấp: <code>cd ../../ho_so</code>. Từ <code>ho_so</code> tới <code>a</code>: lùi một cấp, xuống <code>kho/a</code>.
Cha của <code>a</code> là <code>..</code> nên <code>ls ..</code>. Lời giải ở <code>labs/FND/L01/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, từ thư mục b tới ho sơ phải lùi hai cấp, rồi xuống ho sơ. Từ ho sơ tới a thì lùi một cấp rồi xuống kho và a. Thư mục cha của a chính là hai dấu chấm.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=150), "FND", "L01")
    write_lab("FND", "L01", f"""# Lab FND L01 — Đi theo cây thư mục

Tạo `di.sh`. Bắt đầu bằng đoạn dựng cây này (chép nguyên; `mkdir` và `touch` học ở bài sau):

```bash
{SETUP}
```

Rồi viết các lệnh, **chỉ dùng `cd` với đường dẫn tương đối** (không gõ `/` ở đầu) và `ls`:
1. đang đứng ở `b`: in nội dung `b`;
2. tới `ho_so`, in nội dung;
3. từ `ho_so` tới `a`, in nội dung;
4. in nội dung thư mục **cha** của `a` (một lệnh `ls`, không `cd`).

Chạy `bash di.sh`; chấm: `bash labs/cham.sh FND L01 di.sh`. Khác bài giảng: số tệp, tên thư mục.
""", "sh", SETUP + "\n" + LAB_BODY, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("dấu nhắc: máy chờ lệnh", "pwd: đang đứng ở đâu", "ls: trong đây có gì", "cd: đi sang chỗ khác",
                 "tuyệt đối: đếm từ gốc /", "tương đối: đếm từ chỗ đứng, .. lùi một cấp"),
           """Tổng kết chuỗi logic. Dấu nhắc cho biết máy chờ lệnh. Lệnh in vị trí cho biết đang đứng ở đâu. Lệnh liệt kê cho biết trong đây có gì. Lệnh đổi thư mục đi sang chỗ khác.
           Đường dẫn tuyệt đối đếm từ gốc, đường dẫn tương đối đếm từ chỗ đứng và hai dấu chấm lùi một cấp."""),
        st("""<div class='box key'><b>Tư duy:</b> trước mỗi lệnh, tự hỏi “mình đang đứng ở đâu?”. Lệnh chạy tốt hay hỏng thường chỉ vì chỗ đứng.</div>
<p>Bài sau: tạo thư mục và tệp, chép, đổi tên, và xoá, tức làm cho cây thay đổi.</p>""",
           """Điều cần mang theo, trước mỗi lệnh, hãy tự hỏi mình đang đứng ở đâu. Lệnh chạy tốt hay hỏng thường chỉ vì chỗ đứng.
           Bài sau, ta học tạo thư mục và tệp, chép, đổi tên và xoá, tức là làm cho cây thay đổi.""", forward_ref=True),
    ])
    return lesson("L01", "git_bash_duong_dan", "Bài 1 — Cửa sổ lệnh: đang đứng ở đâu, đi đâu, nhìn gì",
                  "curriculum/fnd.yaml L01; audit/fnd/verify_fnd.py L01 (Git Bash chạy thật pwd/ls/cd trong thư mục tạm); Git for Windows /etc/profile.d/aliases.sh "
                  "(alias ls có -F: đã mở tệp trên máy kiểm); GNU Coreutils manual (ls, pwd), GNU Bash Reference Manual (cd, Tilde Expansion, Quoting); "
                  "Microsoft Learn, Maximum Path Length Limitation (MAX_PATH = 260; NOT_VERIFIED: trích theo trí nhớ, chưa mở lại nguyên văn)",
                  ["Nêu ý nghĩa của dấu nhắc và ba lệnh in vị trí, liệt kê, đổi thư mục",
                   "Phân biệt đường dẫn tuyệt đối với tương đối và tính số lần lùi bằng hai dấu chấm",
                   "Đi một vòng trong cây thư mục bằng các lệnh cd và kiểm vị trí bằng pwd",
                   "Kiểm một đích đến bằng hai cách đi khác nhau",
                   "Chỉ ra ba lỗi hay gặp: khoảng trắng, gạch chéo ngược, chữ hoa chữ thường",
                   "Đi theo cây cho trước chỉ bằng đường tương đối và in nội dung từng thư mục"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "sym"), (2, "formula"), (3, "example"), (4, "check"), (5, "pitfalls"), (6, "practice")])
