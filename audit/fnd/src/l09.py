from lib import *
from labkit import write_lab, practice_steps, practice_scene

LAB_SOL = """git init -q -b main repo
cd repo
git config user.name "Hoc Vien"
git config user.email "hv@example.com"
echo "ao 10" > kho.txt
git add kho.txt
git commit -q -m "tao kho"
echo "non 5" >> kho.txt
git commit -q -am "them non"
sed -i 's/ao 10/ao 12/' kho.txt
git commit -q -am "sua so luong ao"
git log --format=%s
git branch --show-current
git rev-list --count HEAD"""
LAB_OUT = "sua so luong ao\nthem non\ntao kho\nmain\n3"


def build():
    g = cmd("PhienGit", [
        ("mkdir so_tay && cd so_tay", ""), ("git init", "Initialized empty Git repository in C:/Users/ban/so_tay/.git/"),
        ("echo 'so du: 100' > so_du.txt", ""), ("git status -s", "?? so_du.txt"), ("git add so_du.txt", ""), ("git status -s", "A  so_du.txt"),
        ("git commit -q -m 'tao so du ban dau'", ""), ("git status -s", ""), ("git log --format=%s", "tao so du ban dau"),
        ("echo 'so du: 150' > so_du.txt", ""), ("git status -s", " M so_du.txt"),
        ("git diff", "diff --git a/so_du.txt b/so_du.txt\nindex 7de0592..ad79274 100644\n--- a/so_du.txt\n+++ b/so_du.txt\n@@ -1 +1 @@\n-so du: 100\n+so du: 150"),
        ("git commit -q -am 'cap nhat so du'", ""), ("git log --format='%h %s'", "0e66378 cap nhat so du\n32dcaaf tao so du ban dau"),
        ("git branch thu_nghiem", ""), ("git switch thu_nghiem", "Switched to branch 'thu_nghiem'"),
        ("echo 'ghi chu' > ghi_chu.txt", ""), ("git add ghi_chu.txt", ""), ("git commit -q -m 'them ghi chu'", ""),
        ("git switch main", "Switched to branch 'main'"), ("git log --format=%s", "cap nhat so du\ntao so du ban dau"), ("ls", "so_du.txt"),
        ("git merge -q thu_nghiem", ""), ("ls", "ghi_chu.txt  so_du.txt"), ("git log --format=%s", "them ghi chu\ncap nhat so du\ntao so du ban dau"),
        ("git rev-list --count HEAD", "3"), ("git log --format=%s | wc -l", "3"), ("git status -s", ""),
    ])
    loi = cmd("PhienLoi", [
        ("mkdir kho2 && cd kho2", ""), ("git init -q", ""), ("echo a > a.txt", ""), ("git add a.txt", ""), ("git commit -q -m 'a'", ""),
        ("echo x >> a.txt", ""), ("git commit -q -m 'quen add' > /dev/null; echo \"ma thoat: $?\"", "ma thoat: 1"),
        ("echo '*.log' > .gitignore", ""), ("touch a.log", ""), ("git status -s", " M a.txt\n?? .gitignore"),
        ("echo 'mat_khau=abc123' > .env", ""), ("git add .env", ""), ("git commit -q -m 'them cau hinh'", ""), ("git rm -q .env", ""),
        ("git commit -q -m 'xoa env'", ""), ("git show HEAD~1:.env", "mat_khau=abc123"),
    ])
    quiz = cmd("PhienQuiz", [
        ("mkdir q && cd q", ""), ("git init -q", ""), ("echo 1 > a.txt", ""), ("git add a.txt", ""), ("git commit -q -m 'a'", ""),
        ("echo 2 >> a.txt", ""), ("echo 1 > b.txt", ""), ("git add b.txt", ""), ("echo 1 > c.txt", ""),
        ("git status -s", " M a.txt\nA  b.txt\n?? c.txt"),
    ])

    sc_hook = sc("hook", "hook", "Hôm qua chạy đúng, hôm nay hỏng: mình đã sửa gì?", [
        st(term_block(g, 11, 12, title="Công cụ quản lý phiên bản cho thấy đúng dòng đã đổi")
           + "<p>Dòng có <code>-</code> là <b>cũ</b>, dòng có <code>+</code> là <b>mới</b>. Một tệp, một dòng đổi: rõ ràng. Sửa 50 tệp mà không ghi lại thì không ai nhớ nổi.</p>",
           """Chào bạn, hôm qua chương trình chạy đúng, hôm nay hỏng, và bạn không nhớ đã sửa gì. Công cụ quản lý phiên bản giải quyết đúng chuyện đó. Nó cho thấy chính xác dòng nào đã đổi, dòng bắt đầu bằng dấu trừ là cũ, dòng bắt đầu bằng dấu cộng là mới.
           Một tệp một dòng thì rõ ràng, nhưng sửa năm mươi tệp mà không ghi lại thì không ai nhớ nổi."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Vòng làm việc <b>sửa → add → commit</b> gồm những vùng nào, và <code>git status -s</code> đọc ra sao?</li>
<li><b>Nhánh</b> (branch) cho phép thử nghiệm mà không phá bản chính thế nào, rồi <b>gộp</b> lại ra sao?</li>
<li>Vì sao nên <b>chốt nhỏ</b>, và vì sao một bí mật đã chốt thì <b>không xoá khỏi lịch sử</b> bằng cách xoá tệp?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Vòng làm việc sửa, thêm vào vùng chờ, rồi chốt gồm những vùng nào, và lệnh xem trạng thái dạng ngắn đọc ra sao. Nhánh cho phép thử nghiệm mà không phá bản chính thế nào, rồi gộp lại ra sao.
           Và vì sao nên chốt nhỏ, cùng vì sao một bí mật đã chốt thì không xoá khỏi lịch sử bằng cách xoá tệp."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp, thư mục, chuyển hướng, mã thoát", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tạo và sửa tệp", [code("echo 'so du: 100' > so_du.txt")][0] + ": ghi đè; <code>&gt;&gt;</code> nối thêm"],
                  ["② thư mục", "<code>mkdir kho && cd kho</code>: tạo rồi đi vào"],
                  ["③ mã thoát", code("$?") + " bằng 0 là thành công; <code>-q</code> thường nghĩa là “im lặng”"],
                  ["④ tệp ẩn", "tên bắt đầu bằng dấu chấm, xem bằng <code>ls -a</code>"]]),
           """Ta ôn lại bốn điều. Tạo và sửa tệp bằng lệnh in chữ với dấu chuyển hướng, một dấu để ghi đè, hai dấu để nối thêm. Tạo thư mục rồi đi vào. Mã thoát bằng không là thành công, và cờ q thường nghĩa là im lặng.
           Và tệp ẩn có tên bắt đầu bằng dấu chấm, xem bằng cờ a.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã: kho, ba vùng, chốt, nhánh và các lệnh", [
        st(table(["thuật ngữ", "nghĩa"],
                 [["<b>kho</b> (repository)", "thư mục có thêm thư mục ẩn <code>.git</code> chứa <b>toàn bộ lịch sử</b>; <code>git init</code> tạo kho"],
                  ["<b>vùng làm việc</b>", "các tệp bạn đang sửa trong thư mục"],
                  ["<b>vùng chờ</b> (staging)", "danh sách thay đổi bạn <b>chọn</b> đưa vào lần chốt tới: <code>git add</code>"],
                  ["<b>lần chốt</b> (commit)", "một <b>bức ảnh chụp</b> các tệp đã chọn, kèm lời nhắn và <b>mã băm</b> 40 ký tự (thường viết 7 ký tự đầu)"]]),
           """Bảng này giải mã bốn thuật ngữ. Kho là thư mục có thêm một thư mục ẩn chứa toàn bộ lịch sử. Vùng làm việc là các tệp bạn đang sửa. Vùng chờ là danh sách thay đổi bạn chọn đưa vào lần chốt tới.
           Lần chốt là một bức ảnh chụp các tệp đã chọn, kèm lời nhắn và một mã băm, thường viết bảy ký tự đầu.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["lệnh", "nghĩa"],
                 [["<code>git add f</code>", "đưa thay đổi của <code>f</code> vào vùng chờ"],
                  ["<code>git commit -m 'lời nhắn'</code>", "chốt vùng chờ thành một bức ảnh; <code>-a</code> tự add các tệp đã theo dõi; <code>-q</code> im lặng"],
                  ["<code>git status -s</code>", "trạng thái ngắn: <code>??</code> mới chưa theo dõi, <code>A </code> đã add, <code> M</code> sửa chưa add"],
                  ["<code>git diff</code> · <code>git log --format=%s</code>", "xem thay đổi chưa add · liệt kê lời nhắn các lần chốt, mới nhất trước"],
                  ["<code>git branch</code> <code>git switch</code> <code>git merge</code>", "tạo hoặc liệt kê nhánh · chuyển nhánh · gộp nhánh khác vào nhánh hiện tại"]]).replace("·", "và"),
           """Bảng thứ hai là các lệnh. Lệnh thêm đưa thay đổi vào vùng chờ. Lệnh chốt biến vùng chờ thành một bức ảnh kèm lời nhắn. Lệnh xem trạng thái dạng ngắn đánh dấu hai chấm hỏi là tệp mới, chữ A là đã thêm, chữ M là sửa chưa thêm.
           Lệnh xem khác biệt cho thấy thay đổi chưa thêm, và lệnh xem lịch sử liệt kê lời nhắn, mới nhất trước. Cuối cùng là các lệnh về nhánh, tạo, chuyển và gộp.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ba vùng, và lịch sử là một chuỗi ảnh chụp", [
        st(svg(1500, 420,
               box(10, 120, 390, 150, ["vùng làm việc", "tệp đang sửa", " M so_du.txt"], C_AMBER, bold=True),
               arrow(405, 195, 520, 195, "#2a78d6", "git add"),
               box(530, 120, 390, 150, ["vùng chờ", "thay đổi đã chọn", "A  / M "], C_BLUE, bold=True),
               arrow(925, 195, 1040, 195, "#16a34a", "git commit"),
               box(1050, 120, 440, 150, ["kho (lịch sử)", "chuỗi ảnh chụp", "không còn trong status"], C_GREEN, bold=True),
               txt(750, 60, "mỗi lần chốt chỉ lấy những gì bạn đã đưa vào vùng chờ", 28, "middle", "#1f2937", True),
               txt(750, 340, "cái chưa add thì không vào lần chốt này", 26, "middle", "#dc2626", True),
               txt(750, 385, "git status -s cho biết mỗi tệp đang ở vùng nào", 24, "middle", "#1f2937")),
           """Hình này là ba vùng. Bạn sửa tệp ở vùng làm việc. Lệnh thêm đưa thay đổi đã chọn sang vùng chờ. Lệnh chốt lấy vùng chờ làm thành một bức ảnh trong kho, tức lịch sử. Mỗi lần chốt chỉ lấy những gì bạn đã đưa vào vùng chờ,
           nên cái chưa thêm thì không vào lần chốt này. Lệnh xem trạng thái cho biết mỗi tệp đang ở vùng nào."""),
        st(svg(1500, 400,
               box(20, 160, 200, 80, "chốt 1", C_GREEN, bold=True), arrow(225, 200, 300, 200, "#475569"),
               box(305, 160, 200, 80, "chốt 2", C_GREEN, bold=True), arrow(510, 200, 585, 200, "#475569"),
               box(590, 160, 200, 80, "chốt 3", C_GREEN, bold=True), txt(690, 130, "nhánh main", 26, "middle", "#16a34a", True),
               arrow(410, 160, 680, 70, "#d97706"), box(690, 30, 220, 70, "chốt T", C_AMBER, bold=True), txt(800, 20, "nhánh thu_nghiem (thử)", 24, "middle", "#d97706", True),
               arrow(915, 65, 985, 190, "#9333ea"), arrow(795, 200, 985, 215, "#9333ea"),
               box(990, 160, 280, 90, ["chốt gộp", "(hoặc tua nhanh)"], C_PURPLE, bold=True),
               txt(750, 330, "nhánh = một con trỏ rẻ vào lịch sử: tạo trong tích tắc, bỏ đi cũng không mất gì", 26, "middle", "#1f2937", True)),
           """Hình thứ hai là lịch sử và nhánh. Mỗi lần chốt là một ô, nối với ô trước. Nhánh là một con trỏ vào lịch sử, nên tạo nhánh thử nghiệm chỉ mất tích tắc. Ta chốt thử trên nhánh đó mà bản chính vẫn nguyên.
           Khi hài lòng, ta gộp nhánh vào bản chính. Nếu không hài lòng, bỏ nhánh đi cũng không mất gì ở bản chính."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: một tệp đi từ sửa tới lịch sử, qua ba vùng", [
        st(term_block(g, 2, 4, title="Bước 1. Tệp mới: chưa ở vùng nào mà công cụ theo dõi")
           + "<p>Vì mới tạo và chưa add nên mã <code>??</code>: “chưa theo dõi”.</p>",
           """Bước một, tệp mới tạo. Vì chưa thêm vào vùng chờ nên mã trạng thái là hai chấm hỏi, nghĩa là công cụ chưa theo dõi tệp này."""),
        st(term_block(g, 4, 6, title="Bước 2. add: đưa vào vùng chờ")
           + "<p>Nên mã đổi thành <code>A </code>: đã add, chờ chốt.</p>",
           """Bước hai, thêm vào vùng chờ. Nên mã đổi thành chữ A: đã thêm, đang chờ chốt."""),
        st(term_block(g, 6, 9, title="Bước 3. commit: chụp ảnh vào lịch sử")
           + "<p>Vì mọi thay đổi trong vùng chờ đã vào ảnh chụp, <code>status -s</code> hết dòng nào ✓; <code>log</code> có một lần chốt.</p>",
           """Bước ba, chốt. Vì mọi thay đổi trong vùng chờ đã vào ảnh chụp, nên lệnh trạng thái không còn dòng nào. Lệnh xem lịch sử có một lần chốt, mang lời nhắn ta đã viết."""),
        st(term_block(g, 9, 11, title="Bước 4. Sửa tiếp: mã chuyển thành ' M'")
           + "<p>Vì tệp đã được theo dõi nhưng thay đổi mới <b>chưa add</b>: chữ <code>M</code> nằm ở cột <b>thứ hai</b>. Vòng lặp lại từ bước 2.</p>",
           """Bước bốn, sửa tiếp. Tệp đã được theo dõi nhưng thay đổi mới chưa thêm, nên chữ M nằm ở cột thứ hai. Vòng làm việc lặp lại từ bước hai."""),
    ], checks=["len('??') == 2", "' M so_du.txt'.index('M') == 1", "'A  so_du.txt'.index('A') == 0"])
    sc_ex = sc("example", "example", "Ví dụ: một buổi làm việc với kho, năm phép làm", [
        st(term_block(g, 0, 2, title="① Tạo kho")
           + "<p>Thư mục <code>so_tay</code> giờ có thư mục ẩn <code>.git</code>. Câu báo có đường dẫn tuyệt đối; của bạn sẽ khác.</p>",
           """Phép làm thứ nhất, tạo kho. Ta tạo thư mục rồi khởi tạo kho. Công cụ báo đã tạo một kho trống, trong thư mục ẩn chấm g i t. Đường dẫn trong câu báo là của máy bạn nên sẽ khác."""),
        st(term_block(g, 11, 14, title="② Xem khác biệt, chốt lần hai, đọc lịch sử có mã băm")
           + "<p>Mã băm 7 ký tự phụ thuộc <b>tên người, giờ, nội dung</b>; mã trên máy bạn sẽ khác. Lời nhắn mới nhất ở trên cùng.</p>",
           """Phép làm thứ hai, xem khác biệt, chốt lần hai rồi đọc lịch sử có kèm mã băm. Mã băm bảy ký tự phụ thuộc tên người, giờ và nội dung, nên mã trên máy bạn sẽ khác. Lời nhắn mới nhất nằm trên cùng.""", clear=True),
        st(term_block(g, 14, 16, title="③ Tạo nhánh thử nghiệm và chuyển sang")
           + "<p>Chữ <code>Switched</code> báo đã sang nhánh mới. <code>git branch</code> không đối số liệt kê nhánh, dấu <code>*</code> là nhánh hiện tại.</p>",
           """Phép làm thứ ba, tạo nhánh thử nghiệm và chuyển sang đó. Công cụ báo đã chuyển nhánh. Lệnh nhánh không đối số liệt kê các nhánh, và dấu sao đánh dấu nhánh hiện tại."""),
        st(term_block(g, 16, 20, title="④ Chốt trên nhánh thử; về main thì tệp ghi_chu.txt biến mất")
           + "<p>Nhánh thử có $3$ lần chốt; <code>main</code> mới có $2$. <code>ls</code> ở <code>main</code> chưa thấy <code>ghi_chu.txt</code>.</p>",
           """Phép làm thứ tư, chốt trên nhánh thử. Sau khi quay về nhánh chính, lịch sử chỉ có hai lần chốt, và thư mục chưa có tệp ghi chú. Thử nghiệm không làm bẩn bản chính.""", clear=True),
        st(term_block(g, 20, 25, title="⑤ Gộp: tệp xuất hiện, lịch sử có 3 lần chốt")
           + "<p>Gộp nhánh thử vào <code>main</code>: <code>ghi_chu.txt</code> xuất hiện, và $3$ lần chốt đều trên <code>main</code>.</p>",
           """Phép làm thứ năm, gộp. Sau khi gộp nhánh thử vào nhánh chính, tệp ghi chú xuất hiện, và cả ba lần chốt đều nằm trên nhánh chính. Thử nghiệm đã trở thành một phần của bản chính.""", clear=True),
    ], checks=["3 - 1 == 2", "2 + 1 == 3", "len('7de0592') == 7"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm số lần chốt hai cách, và hết thay đổi hai cách", [
        st(term_block(g, 25, 27, title="Hai cách đếm số lần chốt")
           + "<p>Cách 1: lệnh đếm riêng. Cách 2: đếm số dòng của lịch sử. Cả hai ra $3$, khớp với ba lần chốt đã làm ✓</p>",
           """Đường kiểm khác, đếm số lần chốt bằng hai cách. Cách một dùng lệnh đếm riêng. Cách hai đếm số dòng của lịch sử bằng ống. Cả hai ra ba, và khớp với ba lần chốt ta đã làm, vì mỗi lần chốt chỉ ghi một dòng lịch sử."""),
        st(term_block(g, 27, 28, title="Kiểm không còn thay đổi dang dở")
           + "<p>Trạng thái ngắn trống, nghĩa là vùng làm việc và vùng chờ <b>khớp</b> với lần chốt mới nhất. Muốn chắc hơn: <code>git diff</code> cũng trống.</p>",
           """Kiểm thêm là không còn thay đổi dang dở. Lệnh trạng thái ngắn trống nghĩa là vùng làm việc và vùng chờ khớp với lần chốt mới nhất. Lệnh xem khác biệt cũng trống cho cùng kết luận.""", clear=True),
    ], checks=["len(['a', 'b', 'c']) == 3"])
    sc_scale = sc("scale", "example", "Khi lịch sử dài ra: tìm lần chốt gây lỗi bằng chia đôi", [
        st("""<p>Một lỗi mới xuất hiện, biết rằng <b>bản chốt cũ</b> còn tốt và <b>bản chốt mới</b> đã hỏng. Thử bản ở <b>giữa</b>: tốt thì lỗi nằm nửa sau, hỏng thì nằm nửa trước. Mỗi lần thử <b>loại một nửa</b>.</p>
$$2^{t} \\ge n \\;\\Rightarrow\\; t = \\text{số lần thử tối đa}$$
<p class="note">$n$ là số lần chốt giữa bản tốt và bản hỏng; sau $t$ lần chia đôi chỉ còn $1$ ứng viên. Công cụ tự làm việc này (<code>git bisect</code>).</p>""",
           """Giả sử một lỗi mới xuất hiện, biết bản chốt cũ còn tốt và bản chốt mới đã hỏng. Ta thử bản ở giữa. Nếu tốt thì lỗi nằm nửa sau, nếu hỏng thì nằm nửa trước, nên mỗi lần thử loại bỏ một nửa. Gọi t là số lần thử tối đa, thì hai mũ t phải lớn hơn hoặc bằng n, vì sau t lần chia đôi chỉ còn một ứng viên.
           Ở đây n là số lần chốt giữa bản tốt và bản hỏng. Công cụ có sẵn lệnh làm việc này."""),
        st(table(["số lần chốt n", "tính", "thử tối đa"],
                 [["×1: 8", "$2^{3} = 8$", "<b>3</b>"], ["×125: 1 000", "$2^{10} = 1\\,024 \\ge 1\\,000$", "<b>10</b>"], ["×12 500: 100 000", "$2^{17} = 131\\,072 \\ge 100\\,000$", "<b>17</b>"]])
           + "<div class='box key'><b>Đánh đổi:</b> chia đôi chỉ chỉ ra <b>một lần chốt</b>. Nếu lần chốt đó gom 50 thay đổi không liên quan thì ta vẫn phải gỡ từng cái. "
             "Chốt <b>nhỏ, một ý</b> làm cho kết quả tìm kiếm chính là nguyên nhân. Đổi lại, phải kỷ luật viết lời nhắn rõ.</div>",
           """Bảng này cho thấy sức mạnh của chia đôi. Tám lần chốt thì thử tối đa ba lần. Một nghìn lần chốt thì mười lần. Một trăm nghìn lần chốt thì mười bảy lần. Số lần thử tăng rất chậm so với kích thước lịch sử.
           Nhưng chia đôi chỉ chỉ ra một lần chốt. Nếu lần chốt đó gom năm mươi thay đổi không liên quan thì ta vẫn phải gỡ từng cái. Vì vậy chốt nhỏ, mỗi lần một ý, làm cho kết quả tìm kiếm chính là nguyên nhân."""),
    ], checks=["2 ** 3 == 8", "2 ** 10 >= 1000 > 2 ** 9", "2 ** 17 >= 100000 > 2 ** 16", "1000 // 8 == 125", "100000 // 8 == 12500"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Sửa tệp rồi <code>commit</code> mà quên <code>add</code>: lần chốt <b>trống</b>.</div>'
           + term_block(loi, 5, 7) + "<p>Mã thoát $1$: không có gì trong vùng chờ nên không chốt được. Phép thử: chạy <code>git status -s</code> trước mỗi lần chốt; dòng bắt đầu bằng khoảng trắng rồi <code>M</code> là chưa add.</p>",
           """Lỗi thứ nhất, của người mới, là sửa tệp rồi chốt mà quên thêm vào vùng chờ. Lần chốt trống, với mã thoát là một. Phép thử là chạy lệnh trạng thái ngắn trước mỗi lần chốt. Dòng bắt đầu bằng khoảng trắng rồi chữ M nghĩa là chưa thêm."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Tệp rác và tệp nhật ký lẫn vào kho.</div>'
           + term_block(loi, 7, 10) + "<p><code>.gitignore</code> liệt kê mẫu cần bỏ qua: <code>a.log</code> không còn hiện trong trạng thái. Chính <code>.gitignore</code> thì nên được chốt.</p>",
           """Lỗi thứ hai, cũng của người mới, là tệp rác và tệp nhật ký lẫn vào kho. Tệp loại trừ liệt kê các mẫu cần bỏ qua, và tệp nhật ký không còn hiện trong trạng thái. Chính tệp loại trừ thì nên được chốt cùng kho."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Chốt nhầm bí mật (mật khẩu, khoá), rồi nghĩ xoá tệp là xong.</div>'
           + term_block(loi, 10, 16) + "<p>Lịch sử <b>giữ mọi ảnh chụp</b>: dù <code>.env</code> đã bị xoá ở lần chốt sau, lần chốt trước vẫn đọc được mật khẩu. Bí mật đã chốt phải được <b>đổi mới</b> (thu hồi), không chỉ xoá.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là chốt nhầm bí mật như mật khẩu, rồi nghĩ xoá tệp là xong. Lịch sử giữ mọi ảnh chụp. Dù tệp cấu hình đã bị xoá ở lần chốt sau, lần chốt trước vẫn đọc được mật khẩu.
           Bí mật đã chốt phải được thu hồi và đổi mới, không chỉ xoá. Kho đã chia sẻ cho người khác thì càng không thể coi là xoá được."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Trong một kho: <code>a.txt</code> đã chốt rồi bạn sửa tiếp (chưa add); <code>b.txt</code> mới tạo và đã <code>git add</code>; <code>c.txt</code> mới tạo, chưa add.</p>
<ol><li><code>git status -s</code> in ba dòng nào, đúng thứ tự?</li>
<li>Nếu chạy <code>git commit -m 'x'</code> ngay, <b>tệp nào</b> vào lần chốt?</li></ol>
<p><b>Chọn:</b> nhóm sửa 3 việc không liên quan trong một ngày: một lần chốt hay ba lần? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Trong một kho, tệp a đã chốt rồi bạn sửa tiếp, chưa thêm. Tệp b mới tạo và đã thêm. Tệp c mới tạo, chưa thêm. Câu một, lệnh trạng thái ngắn in ba dòng nào, đúng thứ tự. Câu hai, nếu chốt ngay thì tệp nào vào lần chốt.
           Câu ba là một quyết định, sửa ba việc không liên quan trong một ngày, chọn một lần chốt hay ba lần, và vì sao. Hãy dừng video và làm.""", pause=90),
        st(term_block(quiz, 9, 10, title="Máy chạy thật")
           + table(["câu", "đáp án", "lý do"],
                   [["1", "<code> M a.txt</code>, <code>A  b.txt</code>, <code>?? c.txt</code>", "sửa chưa add (M ở cột 2), đã add (A ở cột 1), chưa theo dõi (??)"],
                    ["2", "chỉ <code>b.txt</code>", "lần chốt chỉ lấy vùng chờ; <code>a.txt</code> sửa chưa add, <code>c.txt</code> chưa theo dõi"]]),
           """Đáp án, máy chạy thật cho đúng ba dòng. Câu một, tệp a có chữ M ở cột thứ hai vì sửa chưa thêm, tệp b có chữ A ở cột đầu vì đã thêm, tệp c có hai chấm hỏi vì chưa theo dõi. Câu hai, lần chốt chỉ lấy vùng chờ, nên chỉ có tệp b vào."""),
        st("<div class='box key'><b>Quyết định:</b> <b>ba lần chốt</b>, mỗi lần một việc. Khi một việc gây lỗi, chia đôi chỉ ra đúng lần chốt đó và ta <b>hoàn tác riêng</b> nó mà không mất hai việc kia. "
           "Một lần chốt gom ba việc buộc ta gỡ cả ba.</div>",
           """Về quyết định, chọn ba lần chốt, mỗi lần một việc. Khi một việc gây lỗi, tìm kiếm chia đôi chỉ ra đúng lần chốt đó, và ta hoàn tác riêng nó mà không mất hai việc kia. Một lần chốt gom ba việc buộc ta gỡ cả ba.""", clear=True),
    ], checks=["' M a.txt'.index('M') == 1", "'A  b.txt'.startswith('A')"])
    sc_prac = practice_scene(sc, "Tự làm: dựng kho, chốt ba lần và in lịch sử", pr_steps(
        st, "FND", "L09",
        """<p><b>Đề</b>: tạo <code>kho.sh</code> (làm trong thư mục tạm của lệnh chấm):</p>
<ol><li><code>git init -q -b main repo</code>, vào <code>repo</code>, đặt <code>user.name</code> và <code>user.email</code> (cục bộ);</li>
<li>chốt 3 lần: ① <code>kho.txt</code> có dòng <code>ao 10</code>, lời nhắn <code>tao kho</code>; ② nối dòng <code>non 5</code>, lời nhắn <code>them non</code>; ③ sửa <code>ao 10</code> thành <code>ao 12</code> (dùng <code>sed -i</code>), lời nhắn <code>sua so luong ao</code>;</li>
<li>in: lời nhắn các lần chốt (<code>git log --format=%s</code>), tên nhánh hiện tại (<code>git branch --show-current</code>), số lần chốt (<code>git rev-list --count HEAD</code>).</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh. Khởi tạo kho với nhánh chính, vào kho, đặt tên và thư điện tử cục bộ. Chốt ba lần. Lần một, tệp kho có dòng áo mười, lời nhắn tạo kho. Lần hai, nối dòng nón năm, lời nhắn thêm nón.
        Lần ba, sửa áo mười thành áo mười hai bằng lệnh thay chữ, lời nhắn sửa số lượng áo. Rồi in ba thứ, lời nhắn các lần chốt, tên nhánh hiện tại, và số lần chốt. Hãy dừng video và làm.""",
        LAB_OUT, "kho.sh",
        """<div class="box key"><b>Nếu kẹt:</b> mỗi lần chốt: sửa tệp, <code>git add kho.txt</code> (hoặc <code>commit -a</code> khi tệp đã theo dõi), <code>git commit -q -m '…'</code>. Nhớ đặt <code>user.name</code>/<code>user.email</code> trước lần chốt đầu.
Lời giải ở <code>labs/FND/L09/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, mỗi lần chốt là sửa tệp, thêm vào vùng chờ, rồi chốt kèm lời nhắn. Với tệp đã theo dõi, có thể dùng cờ a để khỏi thêm. Nhớ đặt tên và thư điện tử trước lần chốt đầu. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L09")
    write_lab("FND", "L09", """# Lab FND L09 — Dựng kho Git, chốt ba lần

Tạo `kho.sh` (chạy trong thư mục tạm của lệnh chấm, không ghi ra ngoài):

1. `git init -q -b main repo`, `cd repo`, đặt cục bộ `git config user.name` và `user.email` (giá trị tuỳ ý);
2. chốt **3 lần**, lời nhắn đúng như sau:
   - `tao kho`: `kho.txt` chứa dòng `ao 10`;
   - `them non`: nối dòng `non 5` vào `kho.txt`;
   - `sua so luong ao`: đổi `ao 10` thành `ao 12` bằng `sed -i 's/ao 10/ao 12/' kho.txt`;
3. in lần lượt: `git log --format=%s` (lời nhắn, mới nhất trước), `git branch --show-current`, `git rev-list --count HEAD`.

Chạy `bash kho.sh`; chấm: `bash labs/cham.sh FND L09 kho.sh`. Cần Git 2.28 trở lên. Cảnh báo về xuống dòng (LF/CRLF) nếu có nằm ở luồng lỗi, không ảnh hưởng chấm.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("sửa → add → commit: ba vùng", "status -s: ?? A  M", "log, diff: xem lịch sử và khác biệt", "nhánh: thử không phá bản chính, rồi gộp",
                 "chốt nhỏ một ý: tìm lỗi bằng chia đôi", "bí mật đã chốt: thu hồi, không chỉ xoá"),
           """Tổng kết chuỗi logic. Sửa, thêm vào vùng chờ, rồi chốt, qua ba vùng. Lệnh trạng thái ngắn có các mã hai chấm hỏi, chữ A và chữ M. Lệnh lịch sử và lệnh khác biệt cho xem quá khứ. Nhánh cho thử nghiệm không phá bản chính, rồi gộp lại.
           Chốt nhỏ, mỗi lần một ý, để tìm lỗi bằng chia đôi. Và bí mật đã chốt phải được thu hồi, không chỉ xoá."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi lần chốt là một câu chuyện nhỏ có lời nhắn rõ; trước khi chốt, đọc <code>git status -s</code>; không bao giờ chốt thứ mà bạn không muốn lộ.</div>
<p>Bài cuối: ghép dòng lệnh, SQL và quản lý phiên bản thành một dự án nhỏ, sổ tay giao dịch.</p>""",
           """Điều cần mang theo, mỗi lần chốt là một câu chuyện nhỏ có lời nhắn rõ. Trước khi chốt, hãy đọc trạng thái ngắn. Và không bao giờ chốt thứ mà bạn không muốn lộ.
           Bài cuối, ta ghép dòng lệnh, SQL và quản lý phiên bản thành một dự án nhỏ, là sổ tay giao dịch.""", forward_ref=True),
    ])
    return lesson("L09", "git_toi_thieu", "Bài 9 — Quản lý phiên bản tối thiểu: init, add, commit, log, diff, branch",
                  "curriculum/fnd.yaml L09; audit/fnd/verify_fnd.py L09 (Git 2.x chạy thật trong kho tạm; tên, thư điện tử, nhánh mặc định, ngày giờ cố định nên mã băm tái lập); "
                  "Pro Git (Chacon & Straub, 2nd ed.), chương 2 (Git Basics), chương 3 (Branching), mục Git Tools: Debugging (git bisect); git-scm.com/docs: git-status (--short), git-commit, git-switch; "
                  "số lần thử tối đa ⌈log2 n⌉ là phép tính; kho bí mật: ví dụ cố ý với mật khẩu giả",
                  ["Nêu ba vùng và vòng sửa, add, commit",
                   "Chạy vòng sửa, add, commit và đọc mã git status -s ở từng bước",
                   "Tạo nhánh thử nghiệm, chốt trên đó, chuyển về main rồi gộp",
                   "Kiểm số lần chốt bằng hai cách khác nhau",
                   "Tính số lần thử tối đa khi tìm lần chốt gây lỗi bằng chia đôi",
                   "Chỉ ra ba lỗi hay gặp: quên add, tệp rác, bí mật đã chốt",
                   "Nêu vì sao nên chốt nhỏ, mỗi lần một ý",
                   "Viết tệp lệnh dựng kho, chốt ba lần và in lịch sử"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "intuition"), (2, "example"), (3, "example"), (4, "check"), (5, "scale"), (6, "pitfalls"), (7, "quiz"), (8, "practice")])
