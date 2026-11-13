from pathlib import Path
from lib import *
from labkit import write_lab, practice_steps, practice_scene

CSV = """ngay,tk,loai,so_tien
2026-01-02,A01,nap,2000000
2026-01-02,A02,nap,1500000
2026-01-03,A01,rut,300000
2026-01-03,A03,nap,800000
2026-01-04,A02,rut,500000
2026-01-04,A01,chuyen,400000
2026-01-05,A03,rut,100000
2026-01-05,A02,chuyen,250000
2026-01-06,A01,nap,600000
2026-01-06,A03,chuyen,200000
"""
SH = """set -e
rm -f so_tay.db
sqlite3 so_tay.db <<'EOF'
CREATE TABLE gd (ngay TEXT, tk TEXT, loai TEXT, so_tien INTEGER);
.import --csv --skip 1 giaodich.csv gd
CREATE VIEW sd AS SELECT tk,
  CASE WHEN loai = 'nap' THEN so_tien ELSE -so_tien END AS dong
  FROM gd;
EOF
sqlite3 so_tay.db <<'EOF' > bao_cao.txt
.print == so du theo tai khoan ==
SELECT tk, SUM(dong) FROM sd GROUP BY tk ORDER BY tk;
.print == so giao dich theo loai ==
SELECT loai, COUNT(*) FROM gd GROUP BY loai ORDER BY loai;
.print == giao dich lon nhat moi ngay ==
SELECT ngay, MAX(so_tien) FROM gd GROUP BY ngay ORDER BY ngay;
EOF
a=$(sqlite3 so_tay.db "SELECT SUM(dong) FROM sd;")
b=$(awk -F, 'NR > 1 { if ($3 == "nap") s += $4; else s -= $4 }
  END { print s }' giaodich.csv)
[ "$a" = "$b" ] && echo "tong khop: $a" || echo "LECH: $a $b"
"""
SH_LOI = SH.replace("rm -f so_tay.db\n", "").replace("CREATE TABLE gd", "CREATE TABLE IF NOT EXISTS gd").replace("CREATE VIEW sd", "CREATE VIEW IF NOT EXISTS sd")
SINH_AWK = (Path(__file__).resolve().parents[1] / "assets" / "sinh.awk").read_text(encoding="utf-8")

LAB_CSV = """ngay,loai,so_tien
01,luong,12000000
02,an,150000
03,di_lai,60000
05,an,220000
08,mua_sam,900000
10,an,95000
12,di_lai,45000
15,luong,3000000
"""
LAB_SOL = "cat > gd.csv <<'EOF'\n" + LAB_CSV + """EOF
# may kiem chua cai sqlite3: dung ban thay the cua kho (hoc vien da cai sqlite3 thi bo qua hai dong nay)
command -v sqlite3 > /dev/null 2>&1 || sqlite3() { cat > q.sql; python "$(dirname "$0")/../../sqlrun.py" q.sql; }
{
  echo "CREATE TABLE gd (ngay TEXT, loai TEXT, so_tien INTEGER);"
  tail -n +2 gd.csv | sed "s/\\(.*\\),\\(.*\\),\\(.*\\)/INSERT INTO gd VALUES ('\\1', '\\2', \\3);/"
  echo "SELECT loai, SUM(so_tien) FROM gd WHERE loai <> 'luong' GROUP BY loai ORDER BY loai;"
  echo "SELECT 'so du', SUM(CASE WHEN loai = 'luong' THEN so_tien ELSE -so_tien END) FROM gd;"
} | sqlite3 :memory: > bao_cao.txt
cat bao_cao.txt
a=$(tail -n 1 bao_cao.txt | cut -d'|' -f2)
b=$(awk -F, 'NR > 1 { if ($2 == "luong") s += $3; else s -= $3 } END { print s }' gd.csv)
[ "$a" = "$b" ] && echo "tong khop: $a" || echo "LECH: $a $b"
git init -q -b main repo
cp bao_cao.txt gd.csv repo/
cd repo
git config user.name "Hoc Vien"
git config user.email "hv@example.com"
git add bao_cao.txt gd.csv
git commit -q -m "bao cao thang 1"
git log --format=%s"""
LAB_OUT = "an|465000\ndi_lai|105000\nmua_sam|900000\nso du|13530000\ntong khop: 13530000\nbao cao thang 1"


def build():
    P = {"giaodich.csv": CSV, "so_tay.sh": SH}
    h = cmd("PhienDuAn", [
        ("bash so_tay.sh", "tong khop: 3150000"),
        ("head -n 7 bao_cao.txt", "== so du theo tai khoan ==\nA01|1900000\nA02|750000\nA03|500000\n== so giao dich theo loai ==\nchuyen|3\nnap|4"),
        ("tail -n 7 bao_cao.txt", "rut|3\n== giao dich lon nhat moi ngay ==\n2026-01-02|2000000\n2026-01-03|800000\n2026-01-04|500000\n2026-01-05|250000\n2026-01-06|600000"),
        ("git init -q", ""), ("git status -s", "?? bao_cao.txt\n?? giaodich.csv\n?? so_tay.db\n?? so_tay.sh"),
        ("echo so_tay.db > .gitignore", ""), ("git add .gitignore giaodich.csv so_tay.sh bao_cao.txt", ""),
        ("git commit -q -m 'bao cao dau tien'", ""), ("git log --format=%s", "bao cao dau tien"), ("git status -s", ""),
        ("bash so_tay.sh", "tong khop: 3150000"), ("git status -s", ""),
    ], files=P)
    lap = cmd("PhienLap", [
        ("bash so_tay_loi.sh", "tong khop: 3150000"), ("bash so_tay_loi.sh", "LECH: 6300000 3150000"),
        ("sqlite3 so_tay.db 'SELECT COUNT(*) FROM gd;'", "20"),
    ], files={"giaodich.csv": CSV, "so_tay_loi.sh": SH_LOI})
    tieude = cmd("PhienTieuDe", [
        ("sqlite3 t.db 'CREATE TABLE gd (ngay TEXT, tk TEXT, loai TEXT, so_tien INTEGER);'", ""),
        ("sqlite3 t.db '.import --csv giaodich.csv gd'", ""), ("sqlite3 t.db 'SELECT COUNT(*) FROM gd;'", "11"),
        ("tail -n +2 giaodich.csv | wc -l", "10"),
    ], files={"giaodich.csv": CSV})
    quymo = cmd("PhienQuyMo", [
        ("wc -c giaodich.csv", "292 giaodich.csv"), ("mkdir big && cd big", ""),
        ("seq 1 10000 | awk -f ../sinh.awk > giaodich.csv", ""), ("wc -l giaodich.csv", "10001 giaodich.csv"), ("wc -c giaodich.csv", "248221 giaodich.csv"),
        ("cp ../so_tay.sh .", ""), ("bash so_tay.sh", "tong khop: 130000000"),
        ("head -n 4 bao_cao.txt", "== so du theo tai khoan ==\nA01|43286000\nA02|43397000\nA03|43317000"),
    ], files={"giaodich.csv": CSV, "so_tay.sh": SH, "sinh.awk": SINH_AWK})
    quiz = cmd("PhienQuiz", [
        ("bash so_tay.sh", "tong khop: 3150000"),
        ("sqlite3 so_tay.db \"SELECT SUM(so_tien) FROM gd WHERE tk = 'A02' AND loai <> 'nap';\"", "750000"),
        ("sqlite3 so_tay.db \"SELECT ngay, SUM(so_tien) AS t FROM gd WHERE loai = 'nap'\nGROUP BY ngay ORDER BY t DESC LIMIT 1;\"", "2026-01-02|3500000"),
    ], files=P)

    sc_hook = sc("hook", "hook", "Báo cáo cuối tháng lệch gấp đôi vì ai đó chạy script hai lần", [
        st(term_block(lap, 0, 2, title="Cùng một tệp lệnh, chạy lần thứ hai")
           + "<p>Lần đầu khớp: $3\\,150\\,000$. Chạy <b>lại</b>: cơ sở dữ liệu có <b>gấp đôi</b> giao dịch, tổng thành $6\\,300\\,000$ và dòng kiểm tra báo <b>LECH</b>.</p>",
           """Chào bạn, bài cuối của chặng nền là một tình huống làm nghề. Một tệp lệnh lập báo cáo, chạy lần đầu cho tổng ba triệu một trăm năm mươi nghìn, khớp với phép kiểm. Ai đó chạy lại lần nữa, cơ sở dữ liệu có gấp đôi giao dịch, tổng thành sáu triệu ba trăm nghìn.
           May là dòng kiểm tra báo lệch. Không có dòng kiểm tra đó, con số sai sẽ đi vào báo cáo mà không ai biết."""),
        st("""<div class="box key">Hôm nay ta ghép <b>mọi thứ của chặng</b> thành một dự án nhỏ, “sổ tay giao dịch”, và trả lời:
<ol><li>Làm sao nối <b>dòng lệnh + SQL + quản lý phiên bản</b> thành một quy trình chạy lại được?</li>
<li>Làm sao <b>kiểm</b> kết quả bằng một đường độc lập, để lỗi không lặng lẽ lọt qua?</li>
<li>Khi dữ liệu lớn gấp <b>1 000 lần</b>, cái gì vẫn đúng và cái gì phải đổi?</li></ol></div>""",
           """Hôm nay ta ghép mọi thứ của cả chặng thành một dự án nhỏ, là sổ tay giao dịch, và trả lời ba câu hỏi. Làm sao nối dòng lệnh, ngôn ngữ SQL và quản lý phiên bản thành một quy trình chạy lại được. Làm sao kiểm kết quả bằng một đường độc lập, để lỗi không lặng lẽ lọt qua.
           Và khi dữ liệu lớn gấp một nghìn lần thì cái gì vẫn đúng, cái gì phải đổi."""),
    ])
    pre_rows = [["① đường dẫn, tệp (bài 1, 2)", "chỗ đứng, <code>mkdir</code>, <code>&gt;</code>, <code>rm</code> không có thùng rác"],
                ["② ống và lọc (bài 3)", "<code>tail -n +2</code>, <code>cut</code>, <code>sort</code>, <code>wc</code>"],
                ["③ mã thoát, tệp lệnh, đọc thông báo lỗi (bài 4, 5)", "<code>set -e</code>, <code>&amp;&amp;</code>, <code>||</code>; dòng lỗi cho biết tệp, dòng, nguyên nhân"],
                ["④ dữ liệu có cấu trúc, máy khách và máy chủ (bài 6, 7)", "tệp CSV: dòng đầu là tên cột; yêu cầu và phản hồi, mã trạng thái"],
                ["⑤ bảng và SQL (bài 8)", "<code>CREATE</code>, <code>SELECT … GROUP BY</code>, giao dịch"],
                ["⑥ phiên bản (bài 9)", "<code>add</code>, <code>commit</code>, <code>.gitignore</code>"]]
    sc_pre = sc("prereq", "prereq", "Ôn lại: sáu mảnh của chặng, mỗi mảnh một dòng", [
        st(table(["mảnh đã học", "nhắc lại"], pre_rows),
           """Ta ôn lại sáu mảnh của chặng. Đường dẫn và tệp, nhớ rằng lệnh xoá không có thùng rác. Ống và lọc để đọc tệp bảng. Mã thoát và tệp lệnh, gồm chế độ dừng khi lỗi và cách đọc thông báo lỗi. Dữ liệu có cấu trúc, ở đây là tệp bảng với dòng đầu là tên cột, cùng cách hỏi một máy chủ.
           Bảng và ngôn ngữ SQL, với nhóm và tổng. Và quản lý phiên bản, với thêm, chốt và tệp loại trừ.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã năm mảnh mới của dự án", [
        st(table(["viết", "nghĩa"],
                 [["<code>lệnh &lt;&lt;'EOF' … EOF</code>", "<b>khối chữ nhúng</b>: gửi nhiều dòng liền cho lệnh làm đầu vào; nháy quanh <code>EOF</code> để máy <b>không</b> thay biến bên trong"],
                  [code("a=$(lệnh)"), "lấy <b>kết quả in ra</b> của lệnh làm giá trị của biến <code>a</code>"],
                  [code('[ "$a" = "$b" ]'), "phép <b>so sánh</b> hai chuỗi: mã thoát 0 nếu bằng nhau, nên ghép được với <code>&amp;&amp;</code> và <code>||</code>"],
                  ["<code>awk -F, '…'</code>", "lệnh xử lý từng dòng theo cột; <code>-F,</code>: cột cách nhau bằng dấu phẩy; <code>$3</code> là cột 3; <code>NR</code> là số thứ tự dòng"]]),
           """Bảng này giải mã bốn mảnh mới. Khối chữ nhúng gửi nhiều dòng liền cho một lệnh làm đầu vào, và nháy quanh chữ kết thúc để máy không thay biến bên trong. Dấu đô la mở ngoặc lấy kết quả in ra của một lệnh làm giá trị của biến.
           Ngoặc vuông so sánh hai chuỗi và cho mã thoát không nếu bằng nhau, nên ghép được với hai dấu và và hai gạch đứng. Và lệnh xử lý cột đọc từng dòng, cho ta cộng hoặc trừ theo cột, như một đường tính độc lập.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["viết", "nghĩa"],
                 [["<code>CREATE VIEW sd AS SELECT …</code>", "<b>khung nhìn</b>: một câu <code>SELECT</code> được đặt tên, dùng như một bảng; ở đây <code>dong</code> là tiền <b>có dấu</b> (nạp dương, còn lại âm)"],
                  ["<code>.import --csv --skip 1 f.csv bang</code>", "nạp tệp CSV vào bảng, <b>bỏ dòng tiêu đề</b>"],
                  ["<code>.print văn bản</code>", "in một dòng chữ (để đề mục báo cáo)"]]),
           """Bảng thứ hai giải mã các từ của phần ngôn ngữ SQL trong dự án. Khung nhìn là một câu chọn được đặt tên, dùng như một bảng, ở đây nó cho tiền có dấu, nạp dương và còn lại âm. Lệnh nạp tệp bảng vào bảng, kèm cờ bỏ dòng tiêu đề. Và lệnh in chữ để viết đề mục cho báo cáo.""",
           focus=[1, "1.2", "1.3", "1.4"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: quy trình năm bước, mỗi bước có đầu vào và đầu ra", [
        st(svg(1500, 430,
               box(10, 150, 250, 120, ["giaodich.csv", "đầu vào, nhỏ"], C_GRAY, bold=True), arrow(265, 210, 320, 210, "#2a78d6"),
               box(325, 150, 270, 120, ["sqlite", "nạp + truy vấn"], C_BLUE, bold=True), arrow(600, 210, 655, 210, "#2a78d6"),
               box(660, 150, 250, 120, ["bao_cao.txt", "3 báo cáo"], C_GREEN, bold=True), arrow(915, 210, 970, 210, "#2a78d6"),
               box(975, 150, 240, 120, ["kiểm", "SQL = awk ?"], C_AMBER, bold=True), arrow(1220, 210, 1270, 210, "#16a34a"),
               box(1275, 150, 220, 120, ["git", "chốt kết quả"], C_PURPLE, bold=True),
               txt(750, 70, "mọi bước đều là chữ: đọc được, chạy lại được, kiểm được", 30, "middle", "#1f2937", True),
               txt(750, 340, "so_tay.db không vào git: sinh lại được từ csv + tệp lệnh", 26, "middle", "#dc2626", True),
               txt(750, 390, "chạy lại từ trạng thái sạch (rm -f so_tay.db) nên lần nào cũng cùng kết quả", 24, "middle", "#1f2937")),
           """Hình này là quy trình năm bước. Tệp giao dịch nhỏ là đầu vào. Cơ sở dữ liệu nạp và truy vấn, ra ba báo cáo. Bước kiểm tính lại tổng bằng một đường khác. Rồi quản lý phiên bản chốt kết quả. Mọi bước đều là chữ, nên đọc được, chạy lại được, kiểm được.
           Tệp cơ sở dữ liệu không vào kho, vì sinh lại được từ tệp bảng và tệp lệnh. Và ta luôn chạy lại từ trạng thái sạch, nên lần nào cũng cùng kết quả."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: ba nguyên tắc của một quy trình đáng tin", [
        st(file_block(cmd("Mau", [("true", "")], files=P), "so_tay.sh", title="Bước 1. Tệp so_tay.sh, phần nạp dữ liệu", lines=(1, 8))
           + "<p>Vì mỗi lần chạy <b>xoá cơ sở dữ liệu cũ</b> rồi nạp lại từ tệp bảng, trạng thái đầu luôn giống nhau.</p>",
           """Bước một, nguyên tắc chạy lại được. Tệp lệnh bắt đầu bằng dừng khi lỗi, rồi xoá cơ sở dữ liệu cũ, tạo bảng và nạp lại từ tệp bảng. Vì mỗi lần chạy đều xuất phát từ trạng thái sạch, nên lần nào cũng cùng kết quả."""),
        st(file_block(cmd("Mau2", [("true", "")], files=P), "so_tay.sh", title="Bước 2. Phần báo cáo: mỗi câu hỏi một câu SELECT", lines=(9, 16)),
           """Bước hai, nguyên tắc mỗi câu hỏi một câu chọn. Ba báo cáo là số dư theo tài khoản, số giao dịch theo loại, và giao dịch lớn nhất mỗi ngày. Mỗi báo cáo có một dòng đề mục, và toàn bộ được ghi vào một tệp bằng dấu chuyển hướng."""),
        st(file_block(cmd("Mau3", [("true", "")], files=P), "so_tay.sh", title="Bước 3. Kiểm bằng đường độc lập", lines=(17, 21))
           + "<p>Vì <code>a</code> tính bằng <b>SQL</b> và <code>b</code> tính bằng <b>awk</b> từ chính tệp csv, hai đường không dùng chung mã. Bằng nhau thì tin; lệch thì <b>dừng và tìm</b>.</p>",
           """Bước ba, nguyên tắc kiểm bằng đường độc lập. Tổng thứ nhất tính bằng SQL, tổng thứ hai tính bằng lệnh xử lý cột từ chính tệp bảng, nên hai đường không dùng chung mã. Nếu bằng nhau thì ta tin, nếu lệch thì dừng lại và đi tìm nguyên nhân."""),
    ])
    sc_ex = sc("example", "example", "Ví dụ: chạy cả dự án, năm phép làm", [
        st(term_block(h, 0, 1, title="① Chạy tệp lệnh")
           + "<p>Tổng khớp: nạp $4\\,900\\,000$ trừ chi $1\\,750\\,000$ bằng $\\hl{3\\,150\\,000}$ ✓</p>",
           """Phép làm thứ nhất, chạy tệp lệnh rồi đọc báo cáo. Dòng kiểm tra khớp, tổng là ba triệu một trăm năm mươi nghìn. Làm thử bằng tay, tổng nạp là bốn triệu chín trăm nghìn, tổng chi là một triệu bảy trăm năm mươi nghìn, hiệu đúng như vậy."""),
        st(term_block(h, 1, 2, title="② Báo cáo, nửa đầu: số dư theo tài khoản, bắt đầu số giao dịch theo loại")
           + "<p>Kiểm tay số dư A01: $2\\,000\\,000 - 300\\,000 - 400\\,000 + 600\\,000 = \\hl{1\\,900\\,000}$ ✓</p>",
           """Phép làm thứ hai, đọc báo cáo, nửa đầu. Kiểm tay số dư của tài khoản đầu tiên. Hai triệu trừ ba trăm nghìn trừ bốn trăm nghìn cộng sáu trăm nghìn, bằng một triệu chín trăm nghìn, khớp với dòng đầu của báo cáo.""", clear=True),
        st(term_block(h, 2, 3, title="② Báo cáo, nửa sau: loại còn lại và giao dịch lớn nhất mỗi ngày")
           + "<p>Mỗi ngày một dòng: ngày 2 lớn nhất là khoản nạp $2\\,000\\,000$ ✓</p>",
           """Nửa sau của báo cáo là giao dịch lớn nhất mỗi ngày. Ngày hai tháng một, khoản lớn nhất là hai triệu, đúng là khoản nạp đầu tiên trong tệp bảng.""", clear=True),
        st(term_block(h, 3, 5, title="③ Tạo kho: tệp cơ sở dữ liệu cũng hiện ra!")
           + "<p>Công cụ thấy cả <code>so_tay.db</code>. Đó là tệp <b>sinh lại được</b> nên không nên chốt.</p>",
           """Phép làm thứ ba, tạo kho. Trạng thái cho thấy cả tệp cơ sở dữ liệu. Đó là tệp sinh lại được, nên không nên chốt vào kho.""", clear=True),
        st(term_block(h, 5, 10, title="④ .gitignore, add có chọn lọc, chốt, kiểm sạch")
           + "<p>Chốt 4 tệp: tệp loại trừ, dữ liệu vào, tệp lệnh, báo cáo. Trạng thái trống ✓</p>",
           """Phép làm thứ tư, ghi tên tệp cơ sở dữ liệu vào tệp loại trừ, thêm đúng bốn tệp cần giữ, chốt, rồi kiểm. Lịch sử có một lần chốt, và trạng thái trống, nghĩa là mọi thứ khớp.""", clear=True),
        st(term_block(h, 10, 12, title="⑤ Chạy lại: cùng kết quả, kho vẫn sạch")
           + "<p>Chạy lại từ trạng thái sạch, tổng vẫn $3\\,150\\,000$, và <code>so_tay.db</code> bị bỏ qua nên kho không bẩn thêm ✓</p>",
           """Phép làm thứ năm, chạy lại. Vì xuất phát từ trạng thái sạch nên tổng vẫn như cũ. Tệp cơ sở dữ liệu bị bỏ qua nên kho không bẩn thêm. Đó là một quy trình chạy lại được.""", clear=True),
    ], checks=["2000000 + 1500000 + 800000 + 600000 == 4900000", "300000 + 500000 + 400000 + 100000 + 250000 + 200000 == 1750000", "4900000 - 1750000 == 3150000",
               "2000000 - 300000 - 400000 + 600000 == 1900000", "1500000 - 500000 - 250000 == 750000", "800000 - 100000 - 200000 == 500000", "1900000 + 750000 + 500000 == 3150000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: ba đường cho cùng một tổng", [
        st("""<p>Ba đường, không dùng chung mã, cùng ra $3\\,150\\,000$:</p>
<ol><li><b>SQL</b>: <code>SUM(dong)</code> trên khung nhìn (trong tệp lệnh);</li>
<li><b>awk</b>: cộng trừ cột 4 của tệp csv (trong tệp lệnh);</li>
<li><b>tay</b>: tổng ba số dư $1\\,900\\,000 + 750\\,000 + 500\\,000 = \\hl{3\\,150\\,000}$ ✓</li></ol>""",
           """Đường kiểm khác, ba đường không dùng chung mã cùng ra ba triệu một trăm năm mươi nghìn. Đường một là SQL cộng trên khung nhìn. Đường hai là lệnh xử lý cột cộng trừ cột bốn của tệp bảng. Đường ba là tay, cộng ba số dư của ba tài khoản, nên ba đường độc lập với nhau."""),
        st(term_block(tieude, 1, 4, title="Kiểm cả số dòng: nạp thiếu --skip làm thừa một hàng")
           + "<p>$10$ giao dịch nhưng bảng có $11$ hàng: dòng tiêu đề bị nạp như một giao dịch. Đếm bằng hai đường ($11 \\neq 10$) bắt được lỗi.</p>",
           """Kiểm thêm số dòng. Nếu nạp mà quên cờ bỏ dòng tiêu đề thì bảng có mười một hàng, trong khi tệp chỉ có mười giao dịch. Đếm bằng hai đường cho hai số khác nhau, nên bắt được lỗi.""", clear=True),
    ], checks=["1900000 + 750000 + 500000 == 3150000", "10 + 1 == 11"])
    sc_scale = sc("scale", "example", "Khi dữ liệu lớn gấp 1 000 lần: cái gì vẫn đúng, cái gì phải đổi", [
        st(term_block(quymo, 1, 7, title="×1 000: tạo 10 000 giao dịch giả bằng một tệp awk, chạy nguyên tệp lệnh cũ")
           + "<p>Cùng tệp <code>so_tay.sh</code>, <b>không sửa một chữ</b>: tổng vẫn khớp ($130\\,000\\,000$).</p>",
           """Ta tạo mười nghìn giao dịch giả bằng một tệp lệnh xử lý cột, rồi chạy nguyên tệp lệnh cũ, không sửa một chữ. Dòng kiểm tra vẫn khớp, tổng là một trăm ba mươi triệu. Cách nghĩ của quy trình vẫn đúng ở quy mô lớn hơn một nghìn lần."""),
        st(term_block(quymo, 0, 1, title="Dung lượng bản nhỏ (10 giao dịch)") + table(["số giao dịch", "dung lượng tệp CSV", "ghi chú"],
                 [["×1: 10", "292 byte", "đọc bằng mắt"], ["×1 000: 10 000", "248 221 byte (≈ 0,25 MB)", "máy đọc nhẹ nhàng"],
                  ["×1 000 000: 10 000 000", "≈ 248 triệu byte (≈ 0,25 GB), ngoại suy", "không còn nằm gọn trong kho mã"]])
           + "<div class='box key'><b>Đổi gì khi lớn:</b> (1) <b>không</b> chốt CSV khổng lồ vào kho; chốt tệp lệnh, mẫu nhỏ, báo cáo; (2) đặt <b>chỉ mục</b> cho cột hay lọc; "
             "(3) đọc <b>từng dòng</b>/theo khối thay vì nạp cả tệp vào biến; (4) dữ liệu thật rất lớn thì dùng máy chủ cơ sở dữ liệu. Cái vẫn đúng: chạy lại được, kiểm độc lập.</div>",
           """Bảng này cho thấy quy mô. Mười giao dịch chỉ hai trăm chín mươi hai byte. Mười nghìn giao dịch là khoảng hai trăm bốn mươi tám nghìn byte. Mười triệu giao dịch, ngoại suy, là khoảng hai trăm bốn mươi tám triệu byte, không còn nằm gọn trong kho mã.
           Khi lớn lên, có bốn thứ phải đổi. Không chốt tệp bảng khổng lồ vào kho, chỉ chốt tệp lệnh, mẫu nhỏ và báo cáo. Đặt chỉ mục cho cột hay lọc. Đọc từng dòng thay vì nạp cả tệp vào một biến. Và dữ liệu thật rất lớn thì dùng máy chủ cơ sở dữ liệu.
           Còn hai thứ vẫn đúng là chạy lại được và kiểm độc lập.""", clear=True),
    ], checks=["10 * 1000 == 10000", "round(248221 / 1e6, 2) == 0.25", "248221 * 1000 == 248_221_000", "round(292 * 1000 * 1000 / 1e6) == 292"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Chốt cả tệp cơ sở dữ liệu vào kho.</div>'
           + term_block(h, 4, 5) + "<p>Tệp nhị phân, to, <b>đổi toàn bộ</b> mỗi lần chạy: lịch sử phình ra mà không đọc được khác biệt. Đưa vào <code>.gitignore</code> ngay từ lần đầu.</p>",
           """Lỗi thứ nhất, của người mới, là chốt cả tệp cơ sở dữ liệu vào kho. Đó là tệp nhị phân, to, đổi toàn bộ mỗi lần chạy, nên lịch sử phình ra mà không đọc được khác biệt. Hãy đưa nó vào tệp loại trừ ngay từ lần đầu."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Nạp CSV mà quên bỏ dòng tiêu đề.</div>'
           + term_block(tieude, 2, 4) + "<p>Phép thử: đếm số hàng của bảng và số dòng dữ liệu của tệp; hai số phải bằng nhau.</p>",
           """Lỗi thứ hai, cũng của người mới, là nạp tệp bảng mà quên bỏ dòng tiêu đề. Dòng tiêu đề thành một giao dịch giả. Phép thử là đếm số hàng của bảng và số dòng dữ liệu của tệp, hai số phải bằng nhau."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Tệp lệnh không chạy lại được: lần hai nhân đôi dữ liệu.</div>'
           + term_block(lap) + "<p>Thiếu “xoá rồi nạp lại”, mỗi lần chạy <b>cộng thêm</b>. Con số sai nhưng <b>không báo lỗi</b>; chính phép kiểm độc lập mới bắt được. Quy trình tốt: <b>chạy bao nhiêu lần cũng một kết quả</b>.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là tệp lệnh không chạy lại được. Thiếu bước xoá rồi nạp lại, nên mỗi lần chạy cộng thêm dữ liệu, bảng có hai mươi hàng thay vì mười. Con số sai mà không báo lỗi, và chính phép kiểm độc lập mới bắt được.
           Một quy trình tốt cho cùng một kết quả dù chạy bao nhiêu lần."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Dùng dữ liệu và <code>so_tay.db</code> của bài. (1) Tổng tiền <b>đã chi ra</b> (loại khác <code>nap</code>) của tài khoản A02? (2) Ngày có <b>tổng nạp lớn nhất</b>, kèm tổng?</p>
<p><b>Chọn:</b> bạn tiếp quản dự án này khi tệp CSV đã lên $10\\,000\\,000$ dòng ($\\approx 0{,}25$ GB). Bạn <b>chốt CSV vào kho</b> hay chỉ chốt tệp lệnh + mẫu nhỏ + báo cáo? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm, trên dữ liệu và cơ sở dữ liệu của bài. Câu một, tổng tiền đã chi ra, tức loại khác nạp, của tài khoản A không hai. Câu hai, ngày có tổng nạp lớn nhất, kèm tổng.
           Câu ba là một quyết định. Bạn tiếp quản dự án khi tệp bảng đã lên mười triệu dòng, khoảng hai trăm bốn mươi tám triệu byte. Bạn chốt tệp bảng vào kho, hay chỉ chốt tệp lệnh, mẫu nhỏ và báo cáo, và vì sao. Hãy dừng video và làm.""", pause=90),
        st(term_block(quiz, 1, 3, title="Máy chạy thật")
           + table(["câu", "kết quả", "lý do"],
                   [["1", "<b>750 000</b>", "A02 chi: rút $500\\,000$ + chuyển $250\\,000$"],
                    ["2", "<b>2026-01-02|3 500 000</b>", "ngày 2: hai khoản nạp $2\\,000\\,000$ và $1\\,500\\,000$"]]),
           """Đáp án, máy chạy thật cho hai kết quả. Câu một, tài khoản A không hai chi bảy trăm năm mươi nghìn, gồm rút năm trăm nghìn và chuyển hai trăm năm mươi nghìn. Câu hai, ngày hai tháng một nạp tổng cộng ba triệu năm trăm nghìn, từ hai tài khoản."""),
        st("<div class='box key'><b>Quyết định:</b> chỉ chốt <b>tệp lệnh + mẫu nhỏ + báo cáo</b> và ghi rõ cách lấy CSV gốc. $0{,}25$ GB mỗi lần đổi nhân với số lần chốt làm kho phình ra, "
           "và CSV gốc có thể chứa <b>dữ liệu nhạy cảm</b>. Điều bắt buộc giữ: quy trình chạy lại được và phép kiểm độc lập, trên mẫu nhỏ và trên dữ liệu thật.</div>",
           """Về quyết định, chỉ chốt tệp lệnh, mẫu nhỏ và báo cáo, kèm ghi chú cách lấy tệp bảng gốc. Hai trăm bốn mươi tám triệu byte mỗi lần đổi, nhân với số lần chốt, làm kho phình ra, và tệp gốc có thể chứa dữ liệu nhạy cảm.
           Điều bắt buộc giữ là quy trình chạy lại được và phép kiểm độc lập, trên cả mẫu nhỏ lẫn dữ liệu thật.""", clear=True),
    ], checks=["500000 + 250000 == 750000", "2000000 + 1500000 == 3500000"])
    sc_prac = practice_scene(sc, "Tự làm: sổ tay chi tiêu bằng bash, SQL và git", pr_steps(
        st, "FND", "L10",
        """<p><b>Đề</b>: tạo <code>so_tay.sh</code>. Chép nguyên đoạn dữ liệu <code>gd.csv</code> (8 dòng chi tiêu, xem <code>de.md</code>). Rồi viết:</p>
<ol><li>tạo bảng <code>gd (ngay, loai, so_tien)</code>, nạp dữ liệu, in <b>tổng chi theo loại</b> (loại khác <code>luong</code>) và dòng <code>so du</code> (lương <b>trừ</b> chi);</li>
<li>kiểm độc lập: tính số dư bằng <code>awk</code> từ chính tệp csv, in <code>tong khop: …</code> hoặc <code>LECH: …</code>;</li>
<li>tạo kho <code>repo</code>, chốt <code>bao_cao.txt</code> và <code>gd.csv</code> với lời nhắn <code>bao cao thang 1</code>, in <code>git log --format=%s</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm, là cả dự án thu nhỏ. Tạo một tệp lệnh, chép nguyên đoạn dữ liệu tám dòng chi tiêu. Rồi viết ba việc. Một, tạo bảng, nạp dữ liệu, in tổng chi theo loại và dòng số dư, lương trừ chi.
        Hai, kiểm độc lập, tính số dư bằng lệnh xử lý cột từ chính tệp bảng, rồi in khớp hoặc lệch. Ba, tạo kho, chốt báo cáo và dữ liệu với lời nhắn cho trước, rồi in lời nhắn của lịch sử. Hãy dừng video và làm.""",
        LAB_OUT, "so_tay.sh",
        """<div class="box key"><b>Nếu kẹt:</b> nạp CSV vào bảng: có thể dùng <code>.import --csv --skip 1</code>, hoặc đổi từng dòng thành <code>INSERT</code> bằng <code>sed</code> (cách ở <code>loi_giai.sh</code>). Số dư = lương − chi = $15\\,000\\,000 - 1\\,470\\,000 = 13\\,530\\,000$.
Nhớ <code>git config user.name</code> và <code>user.email</code> trước khi chốt. Lời giải ở <code>labs/FND/L10/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, nạp tệp bảng vào bảng bằng lệnh nạp có cờ bỏ dòng tiêu đề, hoặc đổi từng dòng thành lệnh chèn bằng lệnh thay chữ. Số dư bằng lương trừ chi, mười lăm triệu trừ một triệu bốn trăm bảy mươi nghìn, bằng mười ba triệu năm trăm ba mươi nghìn.
        Nhớ đặt tên và thư điện tử cục bộ trước khi chốt. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=420), "FND", "L10")
    write_lab("FND", "L10", """# Lab FND L10 — Sổ tay chi tiêu: bash + SQL + git

Tạo `so_tay.sh`. **Chép nguyên** đoạn tạo dữ liệu `gd.csv` (số minh hoạ):

```bash
cat > gd.csv <<'EOF'
""" + LAB_CSV + """EOF
```

Rồi viết:
1. **SQL** (sqlite3): bảng `gd (ngay TEXT, loai TEXT, so_tien INTEGER)`, nạp dữ liệu (bỏ dòng tiêu đề; `.import --csv --skip 1 gd.csv gd` hoặc `sed` đổi mỗi dòng thành `INSERT`), rồi in **tổng chi theo loại** (loại khác `luong`, sắp theo tên loại) và dòng `so du` = tổng `luong` trừ tổng chi. Ghi cả hai kết quả vào `bao_cao.txt` và in ra.
2. **Kiểm độc lập**: tính số dư bằng `awk -F,` từ `gd.csv`, so với số dư của SQL, in `tong khop: <số>` hoặc `LECH: <a> <b>`.
3. **git**: `git init -q -b main repo`, chép `bao_cao.txt` và `gd.csv` vào `repo`, đặt `user.name`/`user.email` cục bộ, chốt với lời nhắn `bao cao thang 1`, in `git log --format=%s`.

Kết quả đúng sáu dòng như `mong_doi.txt`. Chạy `bash so_tay.sh`; chấm: `bash labs/cham.sh FND L10 so_tay.sh`. Cần sqlite3, awk, git (Git Bash có awk và git; sqlite3 theo bài đầu tiên). Máy kiểm của kho chưa cài sqlite3 nên `loi_giai.sh` có hai dòng thay thế bằng `labs/sqlrun.py`; bạn đã cài sqlite3 thì không cần chúng.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic, tư duy và nhìn lại cả chặng", [
        st(chain("nối bash + SQL + git bằng tệp lệnh", "chạy từ trạng thái sạch: chạy lại được", "kiểm bằng đường độc lập: SQL = awk = tay",
                 "dữ liệu lớn: không chốt CSV, đặt chỉ mục, đọc từng dòng", "chốt tệp lệnh, mẫu, báo cáo"),
           """Tổng kết chuỗi logic. Nối dòng lệnh, SQL và quản lý phiên bản bằng một tệp lệnh. Chạy từ trạng thái sạch để chạy lại được. Kiểm bằng đường độc lập, SQL bằng lệnh xử lý cột bằng tay. Khi dữ liệu lớn, không chốt tệp bảng khổng lồ, đặt chỉ mục, đọc từng dòng.
           Và chốt tệp lệnh, mẫu nhỏ và báo cáo."""),
        st(table(["bạn đã có", "dùng ở đâu tiếp"],
                 [["dòng lệnh, tệp, đường dẫn, ống, mã thoát", "mọi thao tác biên dịch, chạy, kiểm"],
                  ["CSV, JSON, YAML", "đọc và viết dữ liệu, tệp cấu hình"],
                  ["HTTP và curl", "gọi và kiểm một dịch vụ"],
                  ["SQL cơ bản và giao dịch", "lưu và hỏi dữ liệu có bảo đảm"],
                  ["quản lý phiên bản", "ghi lại và quay lại mọi thay đổi"]])
           + "<div class='box key'><b>Tư duy:</b> một quy trình tốt là <b>chạy lại được</b>, <b>kiểm được bằng đường độc lập</b>, và <b>nhỏ gọn để chốt</b>. Bạn đã có đủ nền để bắt đầu viết chương trình thật.</div>",
           """Đây là những gì bạn đã có, và dùng ở đâu tiếp. Dòng lệnh, tệp, ống và mã thoát dùng cho mọi thao tác biên dịch, chạy và kiểm. Dữ liệu có cấu trúc để đọc và viết dữ liệu, tệp cấu hình. Giao thức HTTP để gọi và kiểm một dịch vụ. SQL và giao dịch để lưu và hỏi dữ liệu có bảo đảm.
           Quản lý phiên bản để ghi lại và quay lại mọi thay đổi. Điều cần mang theo, một quy trình tốt chạy lại được, kiểm được bằng đường độc lập, và nhỏ gọn để chốt. Bạn đã có đủ nền để bắt đầu viết chương trình thật.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6", 2, 2]),
    ])
    return lesson("L10", "so_tay_giao_dich", "Bài 10 — Dự án nhỏ: sổ tay giao dịch bằng bash, SQL và git",
                  "curriculum/fnd.yaml L10; audit/fnd/verify_fnd.py L10 (Git Bash + sqlite3 [shim trên máy kiểm] + awk + git chạy thật toàn bộ quy trình); "
                  "GNU Bash Reference Manual (Here-Documents, Command Substitution, Conditional Constructs [ ]); The AWK Programming Language (Aho, Kernighan, Weinberger); "
                  "SQLite docs: CREATE VIEW, Command-Line Shell (.import, .print); tính idempotent của một tác vụ (chạy n lần = chạy 1 lần); "
                  "số dòng và byte 10 / 10 001 / 292 / 248 221 đo bằng verify_fnd; 0,25 GB cho 10 triệu dòng là ngoại suy tuyến tính",
                  ["Nối tệp lệnh, SQL và quản lý phiên bản thành một quy trình chạy lại được",
                   "Chạy quy trình sổ tay giao dịch và đọc ba báo cáo",
                   "Kiểm tổng bằng ba đường độc lập: SQL, awk và tính tay",
                   "So sánh dung lượng và cách xử lý khi dữ liệu nhân lên 1 000 lần",
                   "Chỉ ra ba lỗi hay gặp: chốt tệp cơ sở dữ liệu, nạp cả dòng tiêu đề, tệp lệnh không chạy lại được",
                   "Nêu nên chốt gì vào kho khi tệp dữ liệu rất lớn",
                   "Viết tệp lệnh tổng hợp: nạp dữ liệu, truy vấn, kiểm độc lập và chốt vào kho"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "formula"), (2, "example"), (3, "check"), (4, "scale"), (5, "pitfalls"), (6, "quiz"), (7, "practice")])
