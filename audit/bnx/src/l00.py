import re as _re

from lib import *

# "Git" chỉ được vào lời đọc khi BRIEF §6 (audit/bnx/probes/x1.md) xác nhận đã dò phát âm đạt. Chưa xác nhận → lời đọc nói
# "trình quản lý phiên bản", tên Git vẫn hiện trên màn hình. Bật True (một dòng) khi §6 có "Git" rồi chạy lại gen/lint.
GIT_SPOKEN = False


def _say_no_git(t):
    t = _re.sub(r"(?<!\w)Git(?!\w)", "trình quản lý phiên bản", t)
    return _re.sub(r"(^|[.!?]\s+)trình", lambda m: m.group(1) + "Trình", t)


# ── Mã trên màn hình (chạy NGUYÊN VĂN bằng bash của Git for Windows; audit/bnx/ver/l00.py chạy lại đúng các chuỗi này) ──
GIT_INIT = r"""
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=An GIT_AUTHOR_EMAIL=an@vd.vn
export GIT_COMMITTER_NAME=An GIT_COMMITTER_EMAIL=an@vd.vn
export GIT_AUTHOR_DATE=2026-01-05T09:00:00+07:00
export GIT_COMMITTER_DATE=2026-01-05T09:00:00+07:00
cd `mktemp -d`
git init -q -b main
echo "phi=5500" > phi.txt
git add phi.txt
git commit -q -m "Phí chuyển khoản 5500"
git log --format="%H %s"
"""
GIT_INIT_OUT = """
18bdd9f83171c5e0cd7c8f61b3976e87f436643d Phí chuyển khoản 5500
"""
GIT_BRANCH = r"""
git switch -q -c tang
echo "phi=6600" > phi.txt
git commit -q -am "Tăng phí lên 6600"
git switch -q main
echo "phi=4400" > phi.txt
git commit -q -am "Giảm phí còn 4400"
git merge tang
cat phi.txt
"""
GIT_BRANCH_OUT = """
Auto-merging phi.txt
CONFLICT (content): Merge conflict in phi.txt
Automatic merge failed; fix conflicts and then commit the result.
<<<<<<< HEAD
phi=4400
=======
phi=6600
>>>>>>> tang
"""
GIT_RESOLVE = r"""
echo "phi=6600" > phi.txt
git add phi.txt
git commit -q -m "Gộp nhánh tang: chốt 6600"
git cat-file -p HEAD
git log --graph --oneline
git rev-parse HEAD:phi.txt
"""
GIT_RESOLVE_OUT1 = """
tree 4ed712d4f4f629cec4feef460dab40a18aa4d67c
parent a8af580122c034d23f48f1a2b5352f76e21f1606
parent 577eea45be69df57323a445daa576fabd322f6d0
author An <an@vd.vn> 1767578400 +0700
committer An <an@vd.vn> 1767578400 +0700

Gộp nhánh tang: chốt 6600
"""
GIT_RESOLVE_OUT2 = """
*   0eac7e6 Gộp nhánh tang: chốt 6600
|\\
| * 577eea4 Tăng phí lên 6600
* | a8af580 Giảm phí còn 4400
|/
* 18bdd9f Phí chuyển khoản 5500
a9b66cbffa3ddbb8bd633e5dc03afc3fb5575166
"""
PY_BLOB = r"""
import hashlib
noi_dung = "phi=6600\n".encode()
dau = f"blob {len(noi_dung)}\0".encode()
print(len(noi_dung))
print(hashlib.sha1(dau + noi_dung).hexdigest())
"""
PY_BLOB_OUT = """
9
a9b66cbffa3ddbb8bd633e5dc03afc3fb5575166
"""
GIT_SECRET = r"""
git switch -q -c thu 18bdd9f
echo "DB_PASS=MatKhau123" > .env
git add .env
git commit -q -m "Thêm cấu hình kết nối"
git rm -q .env
git commit -q -m "Xoá mật khẩu"
git ls-files
git log --format="%h %s"
git show 57d5547:.env
"""
GIT_SECRET_OUT = """
phi.txt
96f907b Xoá mật khẩu
57d5547 Thêm cấu hình kết nối
18bdd9f Phí chuyển khoản 5500
DB_PASS=MatKhau123
"""

LT, GT = "&lt;" * 7, "&gt;" * 7


def build():
    hook = sc("hook", "hook", "Hai người cùng sửa một dòng phí: ai thắng?", [
        st("""<p>Tệp cấu hình ghi phí chuyển khoản <code>phi=5500</code> đồng <span class='note'>(số minh hoạ)</span>.</p>
<div class="box key">Cùng một sáng: <b>An</b> sửa thành <b>6 600</b>, <b>Bình</b> sửa thành <b>4 400</b>. Cùng tệp, cùng dòng.</div>
<div class="box warn">Gửi tệp cho nhau rồi chép đè: một thay đổi <b class="red">biến mất</b> mà không ai hay.</div>""",
           """Chào bạn, tệp cấu hình của dịch vụ chuyển khoản ghi phí là năm nghìn năm trăm đồng, đây là số minh hoạ.
           Cùng một buổi sáng, An sửa thành sáu nghìn sáu trăm, còn Bình sửa thành bốn nghìn bốn trăm, cùng một dòng.
           Nếu hai người gửi tệp cho nhau rồi chép đè, một thay đổi sẽ biến mất mà không ai hay."""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["Git ghi lịch sử thế nào?", "mỗi commit là một ảnh chụp cả cây tệp, có mã băm 40 ký tự"],
                  ["hai nhánh sửa cùng dòng thì sao?", "Git dừng lại, đánh ba dấu mốc, người quyết rồi commit gộp có 2 cha"],
                  ["lỡ commit mật khẩu rồi xoá thì hết chưa?", "chưa: lịch sử vẫn giữ, phải đổi mật khẩu"]]),
           """Hôm nay ta trả lời ba câu hỏi. Git ghi lịch sử thế nào, hai nhánh cùng sửa một dòng thì chuyện gì xảy ra,
           và lỡ chốt mật khẩu rồi xoá đi thì đã an toàn chưa. Tin tuyển dụng ngân hàng ghi Git là điểm cộng, nhưng đi làm thì ngày nào cũng dùng."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Dòng lệnh", "gõ lệnh và đối số, máy in kết quả; <code>&gt;</code> ghi kết quả vào tệp",
                   "<code>echo \"phi=5500\" &gt; phi.txt</code> ghi một dòng vào tệp"],
                  ["② Thập lục phân", "hệ đếm 16 chữ số: 0–9 rồi a–f; a = 10, f = 15; mỗi ký tự mang 4 bit vì 4 bit có 16 giá trị", "$\\text{ff} = 15 \\cdot 16 + 15 = 255$"],
                  ["③ Hàm băm", "biến nội dung bất kỳ thành một chuỗi độ dài cố định; đổi một ký tự thì kết quả khác hẳn",
                   "Git dùng SHA-1: 160 bit, viết thành 40 ký tự thập lục phân"],
                  ["④ Kho chung", "một kho trên máy chủ cho cả nhóm; <b>bản sao kho</b> (clone): chép cả lịch sử về máy; <b>đẩy</b> (push): gửi lên; <b>lấy về</b> (fetch): tải xuống",
                   "An đẩy, Bình lấy về"]]),
           """Trước hết ta cần hiểu bốn điều sẽ dùng trong bài. Dòng lệnh là nơi gõ tên lệnh cùng đối số, máy chạy rồi in kết quả, còn dấu lớn hơn nghĩa là ghi kết quả vào tệp.
           Thập lục phân là hệ đếm có mười sáu chữ số, từ không đến chín rồi từ a đến f, trong đó a là mười và f là mười lăm.
           Hàm băm biến nội dung bất kỳ thành một chuỗi độ dài cố định, và chỉ đổi một ký tự thì kết quả khác hẳn.
           Cuối cùng, cả nhóm dùng chung một kho đặt trên máy chủ. Bản sao kho là chép cả lịch sử về máy mình.
           Đẩy là gửi phần mới của mình lên máy chủ, còn lấy về là tải phần mới của người khác xuống máy mình."""),
        st("""$$\\text{ff} = 15 \\cdot 16 + 15 = \\hl{255}$$
$$40 \\text{ ký tự} \\cdot 4 \\text{ bit} = \\hlg{160} \\text{ bit}$$""",
           """Bây giờ ta làm thử hai phép tính nhỏ. Hai chữ f đứng cạnh nhau bằng mười lăm nhân mười sáu cộng mười lăm, tức hai trăm năm mươi lăm.
           Mỗi ký tự thập lục phân mang bốn bít, nên bốn mươi ký tự mang một trăm sáu mươi bít, đúng độ dài mã băm của Git.""", clear=True),
    ], checks=["int('ff', 16) == 15 * 16 + 15 == 255", "alg.bnx_hex_bits(40) == 160", "alg.bnx_hex_bits(1) == 4 and 2 ** 4 == 16"])
    sym = sc("sym", "symbol", "Giải mã các từ của Git", [
        st(table(["từ", "nghĩa"],
                 [["Git", "trình quản lý phiên bản: chương trình ghi lại mọi lần sửa tệp của dự án"],
                  ["kho (repository)", "thư mục có thư mục con <code>.git</code> giữ toàn bộ lịch sử"],
                  ["vùng chờ (<code>git add</code>)", "nơi đặt các tệp sẽ vào lần lưu tới; <code>git add</code> đưa tệp vào đó"],
                  ["commit (lời giảng gọi là “lần chốt”)", "một ảnh chụp cả cây tệp trong vùng chờ, kèm người viết, giờ, lời nhắn và mã của commit cha"],
                  ["mã commit", "40 ký tự thập lục phân, là mã băm của chính commit đó; vài ký tự đầu (thường 7, có công cụ dùng 8) là mã ngắn"]]),
           """Bảng này giải mã năm từ đầu tiên của bài. Hàng đầu là tên của trình quản lý phiên bản ta dùng, một chương trình ghi lại mọi lần sửa tệp của dự án.
           Kho là thư mục có một thư mục con ẩn giữ toàn bộ lịch sử.
           Vùng chờ là nơi đặt các tệp sẽ vào lần lưu tới, và lệnh thêm đưa tệp vào đó.
           Từ tiếng Anh ở hàng thứ tư, trong lời giảng gọi là lần chốt, là một ảnh chụp cả cây tệp trong vùng chờ, kèm người viết, giờ, lời nhắn và mã của lần chốt cha.
           Mã chốt dài bốn mươi ký tự thập lục phân, là mã băm của chính lần chốt đó.
           Vài ký tự đầu, thường là bảy, có công cụ dùng tám, gọi là mã ngắn."""),
        st(table(["từ", "nghĩa"],
                 [["nhánh (branch)", "một nhãn trỏ vào commit mới nhất của một hướng làm việc; <code>main</code> là nhánh chính"],
                  ["<code>HEAD</code>", "con trỏ “đang đứng ở đâu”: trỏ vào nhánh đang đứng, tức commit mới nhất của nhánh đó"],
                  ["gộp (merge)", "ghép một nhánh vào nhánh đang đứng, tạo commit gộp có 2 cha"]]),
           """Bảng thứ hai giải mã thêm ba từ về nhánh. Nhánh chỉ là một cái nhãn trỏ vào lần chốt mới nhất của một hướng làm việc, và nhánh chính tên là main.
           Chữ in hoa ở hàng giữa là con trỏ cho biết ta đang đứng ở đâu, nó trỏ vào nhánh đang đứng, tức lần chốt mới nhất của nhánh đó.
           Gộp là ghép một nhánh vào nhánh đang đứng, tạo ra một lần chốt gộp có hai cha.""", clear=True),
        st(table(["dấu mốc", "đọc là", "nghĩa"],
                 [[f"<code>{LT} HEAD</code>", "bảy dấu nhỏ hơn", "mở phần của nhánh đang đứng (ở đây: <code>main</code>)"],
                  ["<code>=======</code>", "bảy dấu bằng", "ranh giới giữa hai phần"],
                  [f"<code>{GT} tang</code>", "bảy dấu lớn hơn", "đóng phần của nhánh được gộp vào (nhánh <code>tang</code>)"]]),
           """Khi gộp không tự xong, Git chèn ba dấu mốc vào tệp. Bảy dấu nhỏ hơn mở phần của nhánh đang đứng, ở đây là nhánh chính.
           Bảy dấu bằng là ranh giới giữa hai phần. Bảy dấu lớn hơn đóng phần của nhánh được gộp vào, ở đây là nhánh tang.""", clear=True),
    ])
    intu = sc("intuition", "intuition", "Hình dung: đồ thị commit và ảnh chụp có mã băm", [
        st(svg(1500, 470,
               box(40, 190, 250, 100, ["18bdd9f", "phi=5500"], C_GRAY, bold=True),
               box(560, 40, 270, 100, ["577eea4", "phi=6600"], C_AMBER, bold=True),
               box(560, 330, 270, 100, ["a8af580", "phi=4400"], C_BLUE, bold=True),
               box(1110, 190, 280, 100, ["0eac7e6", "gộp: phi=6600"], C_GREEN, bold=True),
               arrow(555, 95, 295, 215, "#475569"), arrow(555, 375, 295, 265, "#475569"),
               arrow(1105, 215, 835, 95, "#475569"), arrow(1105, 265, 835, 375, "#475569"),
               txt(695, 30, "nhánh tang", 24, "middle", "#d97706", True),
               txt(695, 460, "nhánh main", 24, "middle", "#2a78d6", True),
               txt(165, 320, "commit gốc", 22),
               txt(1250, 320, "2 cha", 24, "middle", "#16a34a", True),
               txt(980, 245, "mũi tên: trỏ về cha", 22, "middle", "#475569")),
           """Hình là đồ thị lịch sử của ví dụ hôm nay. Bên trái là lần chốt gốc, phí năm nghìn năm trăm.
           Nhánh tang ở trên đổi thành sáu nghìn sáu trăm, nhánh chính ở dưới đổi thành bốn nghìn bốn trăm.
           Mỗi mũi tên trỏ về cha, vì mỗi lần chốt ghi mã của lần chốt trước nó.
           Lần chốt gộp bên phải có hai mũi tên, tức là có hai cha."""),
        st(svg(1500, 430,
               box(30, 110, 420, 210, ["commit 0eac7e6", "tree 4ed712d", "parent a8af580", "parent 577eea4", "An, lời nhắn"], C_GREEN, size=24, bold=True),
               box(560, 165, 380, 100, ["tree 4ed712d", "phi.txt → a9b66cb"], C_PURPLE, size=24, bold=True),
               box(1050, 165, 400, 100, ["blob a9b66cb", "phi=6600"], C_AMBER, size=24, bold=True),
               arrow(450, 215, 555, 215), arrow(940, 215, 1045, 215),
               txt(750, 400, "Đổi một chữ trong tệp → mã blob đổi → mã tree đổi → mã commit đổi", 26, "middle", "#1f2937", True)),
           """Bên trong, một lần chốt không lưu phần thay đổi, mà lưu ảnh chụp cả cây tệp.
           Lần chốt trỏ tới một cây, cây ghi tên tệp phí và mã của nội dung, còn nội dung là dòng phí sáu nghìn sáu trăm.
           Mỗi tầng được đặt tên bằng mã băm của chính nó, nên đổi một chữ trong tệp thì mã của cả ba tầng đều đổi."""),
    ], checks=["alg.bnx_git_demo()['merge'].startswith('0eac7e6') and alg.bnx_git_demo()['tree6600'].startswith('4ed712d')",
               "alg.bnx_git_demo()['blob6600'].startswith('a9b66cb') and alg.bnx_git_demo()['root'].startswith('18bdd9f')",
               "alg.bnx_git_demo()['tang'].startswith('577eea4') and alg.bnx_git_demo()['giam'].startswith('a8af580')"])
    form = sc("formula", "formula", "Suy ra từng bước: khi nào gộp tự xong, khi nào xung đột", [
        st("""<p><b>Bước 1.</b> Git tìm <b>commit chung gần nhất</b> của hai nhánh, vì chỉ so với điểm xuất phát chung mới biết <i>ai đã đổi gì</i>.</p>
<span class='note'>Làm thử: <code>main</code> = gốc → 4400; <code>tang</code> = gốc → 6600; chung = gốc <code>18bdd9f</code> (5500).</span>""",
           """Bước một, Git tìm lần chốt chung gần nhất của hai nhánh, vì chỉ khi so với điểm xuất phát chung mới biết ai đã đổi gì.
           Làm thử, cả hai nhánh đều đi ra từ lần chốt gốc, nên điểm chung là phí năm nghìn năm trăm."""),
        st("""<p><b>Bước 2.</b> So <b>từng bên với gốc</b>, không so hai bên với nhau.</p>
$$\\text{main: } 4\\,400 - 5\\,500 = \\hl{-1\\,100} \\qquad \\text{tang: } 6\\,600 - 5\\,500 = \\hl{1\\,100}$$
<span class='note'>Phép trừ chỉ để ta dễ thấy. Máy không tính số: nó so <b>chữ</b> từng dòng, dòng <code>phi=4400</code> khác dòng <code>phi=5500</code> là đủ.</span>""",
           """Bước hai, Git so từng bên với gốc chứ không so hai bên với nhau, vì cần biết mỗi bên đã đổi gì so với lúc tách ra.
           Nhánh chính lấy bốn nghìn bốn trăm trừ năm nghìn năm trăm, được âm một nghìn một trăm.
           Nhánh tang lấy sáu nghìn sáu trăm trừ năm nghìn năm trăm, được một nghìn một trăm. Như vậy cả hai bên đều đổi cùng một dòng.
           Phép trừ chỉ để ta dễ thấy, vì máy không tính số mà so chữ từng dòng, thấy dòng khác gốc là đủ.""", focus=[1, 1, 2, 2, 3]),
        st(table(["gốc", "main", "tang", "kết quả gộp"],
                 [["5500", "5500", "6600", "6600 — chỉ tang đổi, lấy tang"],
                  ["5500", "4400", "5500", "4400 — chỉ main đổi, lấy main"],
                  ["5500", "6600", "6600", "6600 — hai bên đổi giống nhau"],
                  ["5500", "4400", "6600", "<b class='red'>xung đột</b> — hai bên đổi khác nhau: người quyết"]]),
           """Bước ba là luật gộp ba chiều mà máy áp dụng. Nếu chỉ nhánh tang đổi, Git lấy bản của tang.
           Nếu chỉ nhánh chính đổi, Git lấy bản của nhánh chính. Nếu hai bên đổi giống nhau, Git lấy luôn bản đó.
           Còn khi hai bên đổi cùng một dòng thành hai giá trị khác nhau, máy không có cơ sở chọn, nên dừng lại để người quyết."""),
    ], checks=["4400 - 5500 == -1100 and 6600 - 5500 == 1100",
               "alg.bnx_merge3('5500', '5500', '6600') == ('ok', '6600') and alg.bnx_merge3('5500', '4400', '5500') == ('ok', '4400')",
               "alg.bnx_merge3('5500', '6600', '6600') == ('ok', '6600') and alg.bnx_merge3('5500', '4400', '6600')[0] == 'conflict'"])
    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(code(GIT_INIT),
           """Giờ ta chạy thật từng lệnh trên máy. Năm dòng đầu cố định tên người viết và giờ chốt, để ai chạy lại cũng ra đúng các mã băm như trên màn hình.
           Sau đó ta tạo kho trong một thư mục tạm, ghi dòng phí năm nghìn năm trăm, dùng lệnh thêm đưa tệp vào vùng chờ, rồi chốt và in lịch sử.""",
           ),
        st(out(GIT_INIT_OUT) + """$$① \\; 40 \\text{ ký tự} \\cdot 4 \\text{ bit} = \\hl{160} \\text{ bit}$$""",
           """Máy in ra mã của lần chốt gốc, đếm được bốn mươi ký tự. Phép tính thứ nhất, bốn mươi ký tự nhân bốn bít bằng một trăm sáu mươi bít."""),
        st(code(GIT_BRANCH),
           """Tiếp theo ta tạo nhánh tang, sửa phí thành sáu nghìn sáu trăm rồi chốt.
           Quay về nhánh chính, sửa phí thành bốn nghìn bốn trăm rồi chốt. Cuối cùng gộp nhánh tang vào và in tệp phí.
           Tuỳ chọn a của lệnh chốt tự đưa mọi tệp đã theo dõi vào vùng chờ, nên ở đây khỏi gõ lệnh thêm.""", clear=True),
        st(out(GIT_BRANCH_OUT) + """<p>② 3 dấu mốc chia tệp thành <b>2</b> phiên bản: <code>main</code> 4400, <code>tang</code> 6600.</p>""",
           """Git báo xung đột ở tệp phí và dừng lại, đúng như luật gộp ba chiều. Phép tính thứ hai, ba dấu mốc chia tệp thành hai phiên bản,
           bốn nghìn bốn trăm của nhánh chính ở trên và sáu nghìn sáu trăm của nhánh tang ở dưới.""",
           clear=True, focus=[2, 3]),
        st(code(GIT_RESOLVE) + """<p>③ Người quyết giữ 6600 <span class='note'>(số minh hoạ)</span>: so với <code>main</code> tăng $6\\,600 - 4\\,400 = \\hl{2\\,200}$.</p>""",
           """Xung đột không phải Git hỏng, mà là hai người sửa cùng chỗ và người phải quyết. Giả sử người phụ trách sản phẩm chọn sáu nghìn sáu trăm.
           Ta ghi lại dòng phí không còn dấu mốc, rồi chốt. Phép tính thứ ba, so với nhánh chính phí tăng sáu nghìn sáu trăm trừ bốn nghìn bốn trăm, bằng hai nghìn hai trăm.""",
           clear=True, focus=[0, 2, 1, 2]),
        st(out(GIT_RESOLVE_OUT1, "Kết quả chạy thật: nội dung commit gộp") + """<p>④ Có <b>2</b> dòng <code>parent</code> → commit gộp có <b>2 cha</b>.</p>""",
           """Lệnh xem nội dung in ra lần chốt gộp, đúng như hình ảnh chụp lúc nãy. Phép tính thứ tư, có hai dòng cha,
           một là lần chốt bốn nghìn bốn trăm của nhánh chính, một là lần chốt sáu nghìn sáu trăm của nhánh tang.""",
           clear=True, focus=[2, 3]),
        st(out(GIT_RESOLVE_OUT2, "Kết quả chạy thật: đồ thị commit") + """$$⑤ \\; 3 + 1 = \\hlg{4} \\text{ commit}$$""",
           """Đồ thị vẽ bằng ký tự cho thấy hai nhánh tách ra từ gốc rồi nhập lại. Dòng cuối là mã nội dung của tệp phí.
           Phép tính thứ năm, ba lần chốt trước khi gộp cộng một lần chốt gộp, bằng bốn lần chốt.""",
           clear=True, focus=[2, 2, 3]),
    ], checks=["alg.bnx_is_hex40(alg.bnx_git_demo()['root']) and alg.bnx_hex_bits(40) == 160",
               "len(alg.bnx_markers(alg.bnx_conflict_file('phi=4400', 'phi=6600'))) == 3 and alg.bnx_merge3('5500', '4400', '6600')[0] == 'conflict'",
               "6600 - 4400 == 2200",
               "alg.bnx_git_demo()['merge'] != alg.bnx_git_demo()['tang'] and len([alg.bnx_git_demo()['giam'], alg.bnx_git_demo()['tang']]) == 2",
               "(lambda r: alg.bnx_reachable({r['merge']: [r['giam'], r['tang']], r['giam']: [r['root']], r['tang']: [r['root']]}, r['merge']))(alg.bnx_git_demo()) == 3 + 1"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: tự tính mã băm", [
        st(code(PY_BLOB) + out(PY_BLOB_OUT),
           """Bây giờ ta kiểm lại bằng một đường khác. Python là một ngôn ngữ lập trình ngắn gọn, ở đây chỉ dùng thư viện băm có sẵn của nó.
           Ta không dùng Git mà tự tính mã băm bằng Python, theo đúng cách Git làm.
           Nội dung tệp là tám ký tự của dòng phí cộng một ký tự xuống dòng mà lệnh ghi tệp tự thêm, nên dài chín ký tự.
           Git ghép chữ chỉ loại nội dung, độ dài chín, một ký tự rỗng, rồi tới nội dung, sau đó băm cả chuỗi.
           Kết quả trùng từng ký tự với mã nội dung mà Git vừa in ra ở dòng cuối của ví dụ.
           Vì hai cách tính độc lập cho cùng một mã, ta biết Git thật sự đặt tên nội dung theo chính nội dung.""",
           focus=[0, 1, 1, 3, 1, 3, 0]),
        st(table(["đối tượng", "git in ra", "Python thuần tự tính"],
                 [["nội dung phi=6600", "a9b66cb…", "a9b66cb…"],
                  ["commit gốc", "18bdd9f…", "18bdd9f…"],
                  ["commit gộp (2 cha)", "0eac7e6…", "0eac7e6…"]]),
           """Bộ kiểm của bài còn đi xa hơn một bước. Nó dựng lại cả cây và các lần chốt bằng Python thuần, với cùng tên người viết, giờ và lời nhắn.
           Mã của lần chốt gốc và lần chốt gộp đều khớp, nên mã chốt chỉ phụ thuộc nội dung, cha, người viết, giờ và lời nhắn.""",
           clear=True),
    ], checks=["alg.bnx_git_blob('phi=6600\\n') == alg.bnx_git_demo()['blob6600'] and len('phi=6600\\n') == 9",
               "alg.bnx_git_demo()['root'].startswith('18bdd9f') and alg.bnx_git_demo()['merge'].startswith('0eac7e6')",
               "alg.bnx_git_commit(alg.bnx_git_demo()['tree6600'], [alg.bnx_git_demo()['giam'], alg.bnx_git_demo()['tang']], 'Gộp nhánh tang: chốt 6600') == alg.bnx_git_demo()['merge']"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st(f"""<div class="box warn"><b>Lỗi 1 (người mới).</b> Thấy xung đột tưởng Git hỏng, xoá kho tải lại; hoặc sửa vội mà <b class="red">để sót</b> dòng <code>{LT} HEAD</code> trong tệp cấu hình rồi commit.
<br><span class="note">Phép thử: sau <code>git add</code>, chạy <code>git diff --cached --check</code>; nó báo “leftover conflict marker” trước khi commit.</span></div>""",
           """Lỗi thứ nhất là lỗi hay gặp của người mới. Thấy xung đột lại tưởng Git hỏng, rồi xoá kho tải lại, hoặc sửa vội mà để sót dấu mốc trong tệp cấu hình.
           Phép thử là lệnh kiểm phần đã đưa vào vùng chờ, chạy ngay trước khi chốt, nó báo còn sót dấu mốc xung đột."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Commit mật khẩu, rồi xoá ở commit sau.</div>""" + code(GIT_SECRET),
           """Lỗi thứ hai, của người đã đi làm. Lỡ chốt tệp chứa mật khẩu cơ sở dữ liệu, rồi xoá tệp đó ở lần chốt sau và yên tâm là đã hết.
           Ta làm thử trên một nhánh mới tách ra từ lần chốt gốc, để lịch sử ngắn và dễ đọc.""",
           clear=True),
        st(out(GIT_SECRET_OUT) + """<div class="box key">Tệp đã biến khỏi cây hiện tại, nhưng commit cũ <code>57d5547</code> vẫn trả lại mật khẩu. <b>Cách chữa: đổi mật khẩu ngay</b>, rồi mới tính chuyện dọn lịch sử.</div>""",
           """Danh sách tệp hiện tại chỉ còn tệp phí, nhưng lịch sử vẫn còn lần chốt cũ.
           Lệnh xem tệp ở lần chốt cũ trả lại nguyên mật khẩu, nên ai có bản sao kho, tức đã chép cả lịch sử về máy, đều đọc được.
           Cách chữa là đổi mật khẩu ngay, vì xoá ở lần chốt sau không xoá được nó khỏi lịch sử.""",
           clear=True, focus=[2, 2, 3]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <code>git push --force</code> lên nhánh chung: máy chủ bị ghi đè bằng lịch sử trên máy mình, commit đồng nghiệp vừa đẩy lên <b class="red">mất khỏi nhánh</b>.
<br><span class="note">Cách chữa: khoá nhánh <code>main</code> trên máy chủ không cho ép đẩy. <code>git push --force-with-lease</code> từ chối khi máy chủ có commit mình chưa thấy, nhưng nếu máy mình vừa lấy về (kể cả công cụ lấy ngầm) thì nó coi là đã thấy và vẫn ghi đè.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là ép đẩy lên nhánh chung. Máy chủ bị ghi đè bằng lịch sử trên máy mình,
           nên lần chốt đồng nghiệp vừa đẩy lên biến khỏi nhánh. Cách chữa chắc chắn là khoá nhánh chính trên máy chủ không cho ép đẩy.
           Ép đẩy kèm điều kiện sẽ từ chối khi máy chủ có thứ mình chưa thấy, nhưng nếu máy mình vừa lấy về thì nó vẫn cho ghi đè.""", clear=True),
    ], checks=["alg.bnx_git_demo()['secret_add'].startswith('57d5547') and alg.bnx_git_demo()['secret_rm'].startswith('96f907b')",
               "len(alg.bnx_markers(alg.bnx_conflict_file('phi=4400', 'phi=6600'))) == 3"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Gốc <code>phi=5500</code>. Nhánh A sửa thành 7700, nhánh B không chạm tệp phí. Gộp B vào A có xung đột không? Tệp còn giá trị nào?"],
                  ["2", "Lịch sử đang có 4 commit như ví dụ. Bạn gộp vào một nhánh có 2 commit riêng. Sau khi gộp có bao nhiêu commit? Commit mới có mấy cha?"],
                  ["3", "Quyết định: mật khẩu đã lên máy chủ chung được 10 phút. Đổi mật khẩu ngay, hay viết lại lịch sử để xoá rồi ép đẩy?"]]),
           """Bây giờ tới phần bạn tự làm bài. Câu một, gốc là năm nghìn năm trăm, nhánh A sửa thành bảy nghìn bảy trăm, nhánh B không chạm tệp phí. Gộp có xung đột không, và tệp còn giá trị nào?
           Câu hai, lịch sử đang có bốn lần chốt như ví dụ, bạn gộp vào một nhánh có hai lần chốt riêng. Sau gộp có bao nhiêu lần chốt, và lần chốt mới có mấy cha?
           Câu ba là một quyết định có đánh đổi. Mật khẩu đã lên máy chủ chung được mười phút. Đổi mật khẩu ngay, hay viết lại lịch sử để xoá rồi ép đẩy? Hãy dừng video lại và làm ra giấy trước.""",
           pause=25),
        st("""<p>Câu 1: chỉ nhánh A đổi so với gốc.</p>
$$\\text{gốc } 5\\,500,\\ \\text{A } 7\\,700,\\ \\text{B } 5\\,500 \\;\\Rightarrow\\; \\hlg{7\\,700},\\ \\text{không xung đột}$$""",
           """Bây giờ ta xem đáp án câu một. So từng bên với gốc, chỉ nhánh A đổi, còn nhánh B giữ nguyên năm nghìn năm trăm.
           Theo luật gộp ba chiều, Git lấy bên đã đổi, nên tệp còn bảy nghìn bảy trăm và không có xung đột."""),
        st("""<p>Câu 2: dùng lại 4 commit của ví dụ.</p>
$$4 + 2 + 1 = \\hlg{7} \\text{ commit}, \\qquad \\text{commit gộp có } \\hl{2} \\text{ cha}$$""",
           """Tiếp theo là đáp án của câu hai. Dùng lại bốn lần chốt của ví dụ, cộng hai lần chốt của nhánh kia, cộng một lần chốt gộp, bằng bảy.
           Lần chốt gộp có hai cha, một ở mỗi nhánh."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["đổi mật khẩu ngay (bắt buộc)", "mật khẩu cũ vô dụng, kể cả trên mọi bản sao đã tải về", "phải cập nhật cấu hình mọi nơi dùng mật khẩu đó"],
                  ["viết lại lịch sử rồi ép đẩy (làm thêm)", "kho sạch cho người tải sau", "mọi người phải lấy lại kho; bản sao cũ vẫn còn mật khẩu; ép đẩy nhánh chung"]]),
           """Cuối cùng là đáp án của câu ba. Đổi mật khẩu ngay là bắt buộc, vì trong mười phút đó bản sao kho có thể đã nằm trên máy khác, đổi rồi thì mật khẩu cũ vô dụng.
           Viết lại lịch sử chỉ là việc làm thêm. Nó cho kho sạch với người tải sau, nhưng mọi người phải lấy lại kho, còn bản sao cũ vẫn giữ mật khẩu."""),
    ], checks=["alg.bnx_merge3('5500', '7700', '5500') == ('ok', '7700')", "4 + 2 + 1 == 7"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("commit = ảnh chụp có mã băm", "nhánh = nhãn trỏ commit", "gộp ba chiều so với gốc", "cùng dòng khác nhau: người quyết", "lịch sử không quên"),
           """Bây giờ ta tổng kết lại chuỗi logic. Mỗi lần chốt là một ảnh chụp có mã băm, còn nhánh chỉ là nhãn trỏ vào lần chốt.
           Khi gộp, máy so từng bên với gốc. Hai bên đổi cùng dòng khác nhau thì người quyết. Và lịch sử không quên thứ gì đã chốt."""),
        st("""<div class='box key'><b>Tư duy:</b> mã commit là <b>tên duy nhất của một trạng thái mã nguồn</b>. Cái gì đã commit thì coi như đã công bố cho mọi người có bản sao kho.</div>""",
           """Và đây là điều cần mang theo sau bài. Mã chốt là tên duy nhất của một trạng thái mã nguồn, và cái gì đã chốt thì coi như đã công bố cho mọi người có bản sao kho."""),
        st("""<p class='note'>Bài 13: mã commit được gắn lên ảnh chạy trên máy chủ, để từ một lỗi lúc vận hành truy ngược đúng dòng mã.</p>""",
           """Ở bài mười ba, mã chốt này được gắn lên bản đóng gói chạy trên máy chủ, để khi có lỗi lúc vận hành ta truy ngược được đúng dòng mã.""",
           forward_ref=True),
    ])
    if not GIT_SPOKEN:
        for sc_ in (hook, pre, sym, intu, form, ex, chk, pit, quiz, rec):
            for s_ in sc_["steps"]:
                s_["say"] = _say_no_git(s_["say"])
    return lesson("L00", "git_nhanh_gop_xung_dot", "Bài 0 — Git: lưu lịch sử, tạo nhánh, gộp và giải xung đột",
                  "curriculum/bnx.yaml L00; audit/bnx/verify_bnx.py L00; git 2.53 chạy thật (OBSERVED 2026-11-11); git-scm.com tài liệu git-merge, git-show, git-push (--force-with-lease)",
                  ["Tạo kho, ghi một commit và đọc lịch sử", "Tạo nhánh, gộp nhánh và đọc đồ thị commit",
                   "Đọc dấu xung đột và giải xung đột bằng tay", "Giải thích vì sao bí mật đã commit vẫn còn trong lịch sử"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
