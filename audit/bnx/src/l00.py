import re as _re

import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene  # noqa: F401
from l03 import _merge_short  # ghép câu < 8 từ vào câu bên cạnh (máy nghe gắn cờ câu ngắn)

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

# ── Cảnh quy mô (AF2, 2026-11-14): N nhánh cùng sửa MỘT dòng, gộp lần lượt vào nhánh chính; đo bằng git thật ở N = 2, 10, 50 ──
# Khối trên màn hình hiện N=10; bộ kiểm ver/l00.py chạy đúng chuỗi này (thay N=10 bằng N=2, N=50) cộng biến thể "mỗi người một tệp".
GIT_SCALE = r"""
N=10
cd `mktemp -d` && git init -q -b main
echo "phi=5500" > phi.txt && git add phi.txt && git commit -q -m goc
for i in `seq 1 $N`; do
  git switch -q -c n$i main
  echo "phi=$i" > phi.txt && git commit -q -am "n$i"
done
git switch -q main; xd=0
for i in `seq 1 $N`; do
  git merge -q n$i >/dev/null || { xd=$((xd+1)); git merge --abort; }
done
echo "$N nhanh cung sua mot dong: $xd xung dot"
"""
GIT_SCALE_ENV = """
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=An GIT_AUTHOR_EMAIL=an@vd.vn
export GIT_COMMITTER_NAME=An GIT_COMMITTER_EMAIL=an@vd.vn
"""
GIT_SCALE_OUT = """
10 nhanh cung sua mot dong: 9 xung dot
"""

# ── Lab (labs/BNX/L00): bash; số liệu KHÁC ví dụ trong bài (lãi suất 7/6/8, nhánh giam có 2 commit → tổng 5 commit) ──
LAB_SH = r"""
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=Binh GIT_AUTHOR_EMAIL=binh@vd.vn
export GIT_COMMITTER_NAME=Binh GIT_COMMITTER_EMAIL=binh@vd.vn
cd `mktemp -d`
git init -q -b main
echo "lai=7" > lai.txt
git add lai.txt
git commit -q -m goc
git switch -q -c giam
echo "lai=6" > lai.txt
git commit -q -am "giam lai"
echo "dot giam thang 3" > ghi_chu.txt
git add ghi_chu.txt
git commit -q -m "ghi chu"
git switch -q main
echo "lai=8" > lai.txt
git commit -q -am "tang lai"
git merge giam > /dev/null
echo "lai=8" > lai.txt
git add lai.txt
git commit -q -m "gop giam"
cat lai.txt
echo "so commit: $(git rev-list --count HEAD)"
echo "so cha: $(git cat-file -p HEAD | grep -c '^parent')"
"""
LAB_OUT = "lai=8\nso commit: 5\nso cha: 2"

LAB_DE = """# Lab BNX L00 — Hai nhánh cùng sửa một dòng lãi suất

Làm trong Git Bash. Viết tệp `lab.sh` (số liệu là số minh hoạ). Bốn dòng đầu cho sẵn, chép nguyên văn: chúng đặt tên người viết rồi chuyển vào một thư mục tạm.

```bash
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=Binh GIT_AUTHOR_EMAIL=binh@vd.vn
export GIT_COMMITTER_NAME=Binh GIT_COMMITTER_EMAIL=binh@vd.vn
cd `mktemp -d`
```

Tiếp theo, bạn viết các lệnh sau:

1. Tạo kho (`git init -q -b main`), tạo tệp `lai.txt` chứa dòng `lai=7`, đưa vào vùng chờ (`git add`) và chốt với lời nhắn `goc` (`git commit -q -m goc`; luôn có `-m`, nếu không Git mở trình soạn thảo và chờ bạn).
2. Tạo nhánh `giam`. Trên nhánh này: sửa `lai.txt` thành `lai=6` rồi chốt; sau đó tạo tệp `ghi_chu.txt` (nội dung tuỳ ý), đưa vào vùng chờ và chốt. Nhánh `giam` có 2 lần chốt riêng.
3. Về nhánh `main`, sửa `lai.txt` thành `lai=8` rồi chốt. Gộp nhánh `giam` vào `main` bằng `git merge giam > /dev/null` (dấu `> /dev/null` giấu thông báo xung đột để đầu ra chỉ còn ba dòng cuối).
4. Giải xung đột: ghi lại `lai.txt` chỉ còn `lai=8` (không còn dấu mốc), đưa vào vùng chờ rồi chốt gộp.
5. Cuối chương trình, in ba dòng bằng ba lệnh sau (cho sẵn, chép nguyên văn):

```bash
cat lai.txt
echo "so commit: $(git rev-list --count HEAD)"
echo "so cha: $(git cat-file -p HEAD | grep -c '^parent')"
```

Chạy: `bash lab.sh`. Chấm: `bash labs/cham.sh BNX L00 lab.sh`.
"""


def build():
    write_lab("BNX", "L00", LAB_DE, "sh", LAB_SH, LAB_OUT)
    hook = sc("hook", "hook", "Hai người cùng sửa một dòng phí: ai thắng?", [
        st("""<p>Tệp cấu hình ghi phí chuyển khoản <code>phi=5500</code> đồng <span class='note'>(số minh hoạ)</span>.</p>
<div class="box key">Cùng một sáng: <b>An</b> sửa thành <b>6 600</b>, <b>Bình</b> sửa thành <b>4 400</b>. Cùng tệp, cùng dòng.</div>
<div class="box warn">Gửi tệp cho nhau rồi chép đè: một thay đổi <b class="red">biến mất</b> mà không ai hay.</div>""",
           """Chào bạn, tệp cấu hình ghi phí chuyển khoản là năm nghìn năm trăm đồng, số minh hoạ.
           Một buổi sáng, An sửa thành sáu nghìn sáu trăm, còn Bình sửa thành bốn nghìn bốn trăm, cùng một dòng.
           Nếu hai người chép đè tệp cho nhau, một thay đổi sẽ biến mất mà không ai hay."""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["Git ghi lịch sử thế nào?", "mỗi commit là một ảnh chụp cả cây tệp, có mã riêng dài 40 ký tự"],
                  ["hai nhánh sửa cùng dòng thì sao?", "Git dừng lại, đánh ba dấu mốc, người quyết rồi commit gộp có 2 cha"],
                  ["cả nhóm cùng sửa một dòng thì sao?", "đo thật: càng nhiều nhánh, càng nhiều xung đột phải giải"],
                  ["lỡ commit mật khẩu rồi xoá thì hết chưa?", "chưa: lịch sử vẫn giữ, phải đổi mật khẩu"]]),
           """Hôm nay ta trả lời bốn câu hỏi. Git ghi lịch sử thế nào, hai nhánh cùng sửa một dòng thì sao, cả nhóm cùng sửa thì bao nhiêu xung đột, và chốt mật khẩu rồi xoá đã an toàn chưa?""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Dòng lệnh", "gõ lệnh và đối số, máy in kết quả; <code>&gt;</code> ghi kết quả vào tệp",
                   "<code>echo \"phi=5500\" &gt; phi.txt</code> ghi một dòng vào tệp"],
                  ["② Thập lục phân", "hệ đếm 16 chữ số: 0–9 rồi a–f; a = 10, f = 15; mỗi ký tự mang 4 bit vì 4 bit có 16 giá trị", "$\\text{ff} = 15 \\cdot 16 + 15 = 255$"],
                  ["③ Hàm băm, mã băm", "biến nội dung bất kỳ thành một chuỗi độ dài cố định, gọi là <b>mã băm</b>; đổi một ký tự thì kết quả khác hẳn",
                   "Git dùng thuật toán băm tên SHA-1: 160 bit, viết thành 40 ký tự thập lục phân"],
                  ["④ Kho chung", "một kho trên <b>máy chủ</b> (máy luôn bật, nhiều người cùng nối vào) cho cả nhóm; <b>bản sao kho</b> (clone): chép cả lịch sử về máy; <b>đẩy</b> (push): gửi lên; <b>lấy về</b> (fetch): tải xuống",
                   "An đẩy, Bình lấy về"]]),
           """Trước hết ta cần hiểu bốn điều. Dòng lệnh là nơi gõ lệnh cho máy chạy và in kết quả, dấu lớn hơn ghi kết quả vào tệp.
           Thập lục phân là hệ đếm mười sáu chữ số, từ không đến chín rồi a đến f, với f là mười lăm.
           Hàm băm biến nội dung bất kỳ thành chuỗi dài cố định gọi là mã băm, đổi một ký tự thì khác hẳn. Git dùng thuật toán ra mã một trăm sáu mươi bít.
           Kho chung nằm trên máy chủ luôn bật: bản sao kho chép lịch sử về máy, đẩy là gửi lên, lấy về là tải xuống.""",
           introduces=["bnx_thap_luc_phan", "bnx_ma_bam"]),
        st("""$$\\text{ff} = 15 \\cdot 16 + 15 = \\hl{255}$$
$$40 \\text{ ký tự} \\cdot 4 \\text{ bit} = \\hlg{160} \\text{ bit}$$""",
           """Làm thử hai phép tính. Hai chữ f cạnh nhau bằng mười lăm nhân mười sáu cộng mười lăm, tức hai trăm năm mươi lăm.
           Mỗi ký tự mang bốn bít, nên bốn mươi ký tự mang một trăm sáu mươi bít, đúng độ dài mã băm này.""", clear=True),
    ], checks=["int('ff', 16) == 15 * 16 + 15 == 255", "alg.bnx_hex_bits(40) == 160", "alg.bnx_hex_bits(1) == 4 and 2 ** 4 == 16"])
    sym = sc("sym", "symbol", "Giải mã các từ của Git", [
        st(table(["từ", "nghĩa"],
                 [["Git", "trình quản lý phiên bản: chương trình ghi lại mọi lần sửa tệp của dự án"],
                  ["kho (repository)", "thư mục có thư mục con <code>.git</code> giữ toàn bộ lịch sử"],
                  ["vùng chờ (<code>git add</code>)", "nơi đặt các tệp sẽ vào lần lưu tới; <code>git add</code> đưa tệp vào đó"],
                  ["commit (lời giảng gọi là “lần chốt”)", "một ảnh chụp cả cây tệp trong vùng chờ, kèm người viết, giờ, lời nhắn và mã của commit cha"],
                  ["mã commit", "40 ký tự thập lục phân, là mã băm của chính commit đó; vài ký tự đầu (thường 7) là mã ngắn"]]),
           """Từ đầu bảng là tên một chương trình, gọi là trình quản lý phiên bản, vì nó ghi lại mọi lần sửa tệp. Kho là thư mục giữ toàn bộ lịch sử.
           Vùng chờ là nơi đặt các tệp sẽ vào lần chốt tới. Từ thứ tư, ta đọc là lần chốt, là ảnh chụp cả cây tệp, kèm người viết, giờ, lời nhắn và mã của lần chốt cha.
           Mã chốt dài bốn mươi ký tự thập lục phân, là mã băm của chính nó.""",
           introduces=["bnx_vung_cho"]),
        st(table(["từ", "nghĩa"],
                 [["nhánh (branch)", "một nhãn trỏ vào commit mới nhất của một hướng làm việc; <code>main</code> là nhánh chính"],
                  ["<code>HEAD</code>", "con trỏ “đang đứng ở đâu”: trỏ vào nhánh đang đứng, tức commit mới nhất của nhánh đó"],
                  ["gộp (merge)", "ghép một nhánh vào nhánh đang đứng, tạo commit gộp có 2 cha"]]),
           """Ba từ về nhánh. Nhánh chỉ là một cái nhãn trỏ vào lần chốt mới nhất của một hướng làm việc, và nhánh chính tên là main.
           Chữ in hoa là con trỏ cho biết ta đang đứng ở đâu, còn gộp là ghép một nhánh vào nhánh đang đứng, tạo một lần chốt gộp có hai cha.""", clear=True),
        st(table(["dấu mốc", "đọc là", "nghĩa"],
                 [[f"<code>{LT} HEAD</code>", "bảy dấu nhỏ hơn", "mở phần của nhánh đang đứng (ở đây: <code>main</code>)"],
                  ["<code>=======</code>", "bảy dấu bằng", "ranh giới giữa hai phần"],
                  [f"<code>{GT} tang</code>", "bảy dấu lớn hơn", "đóng phần của nhánh được gộp vào (nhánh <code>tang</code>)"]]),
           """Khi gộp không tự xong, máy chèn ba dấu mốc vào tệp. Bảy dấu nhỏ hơn mở phần của nhánh đang đứng, bảy dấu bằng là ranh giới giữa hai phần,
           và bảy dấu lớn hơn đóng phần của nhánh được gộp vào, ở đây là nhánh tang.""", clear=True),
        st(table(["lệnh", "nghĩa"],
                 [["<code>export TEN=giatri</code>", "đặt một biến môi trường: chương trình chạy sau đó đọc được; <code>GIT_AUTHOR_NAME=An</code> đặt tên người viết là An; <code>GIT_CONFIG_GLOBAL=/dev/null</code> bỏ cấu hình riêng của máy để ai chạy cũng ra cùng mã"],
                  ["<code>cd `mktemp -d`</code>", "<code>mktemp -d</code> tạo một thư mục tạm trống và in đường dẫn; dấu huyền chạy lệnh bên trong rồi thay bằng kết quả, nên <code>cd</code> đi vào đúng thư mục đó"],
                  ["<code>git init -q -b main</code>", "tạo kho trống trong thư mục hiện tại; <code>-q</code> là chạy im lặng, <code>-b main</code> đặt tên nhánh đầu là <code>main</code>"],
                  ["<code>git switch -c tang</code>", "tạo nhánh <code>tang</code> rồi đứng sang đó; <code>git switch main</code> chỉ đứng sang nhánh có sẵn"],
                  ["<code>git commit -am \"lời nhắn\"</code>", "đưa mọi tệp đã theo dõi vào vùng chờ rồi chốt luôn"]]),
           """Năm lệnh đầu của ví dụ. Lệnh đặt biến cho chương trình chạy sau đọc được, như tên người viết, và biến cấu hình riêng đặt rỗng để ai chạy cũng ra cùng mã.
           Lệnh tạo thư mục tạm in đường dẫn, dấu huyền thay lệnh bên trong bằng kết quả của nó, nên lệnh chuyển thư mục đi vào đúng chỗ đó.
           Lệnh tạo kho có tuỳ chọn im lặng và tên nhánh đầu. Lệnh chuyển nhánh có tuỳ chọn tạo nhánh mới, còn lệnh chốt có tuỳ chọn chốt luôn mọi tệp đã theo dõi.""",
           clear=True),
        st(table(["lệnh", "nghĩa"],
                 [["<code>cat phi.txt</code>", "in nội dung tệp <code>phi.txt</code> ra màn hình"],
                  ["<code>git log --format=\"%H %s\"</code>", "in lịch sử, mỗi commit một dòng theo mẫu: <code>%H</code> là mã băm đầy đủ 40 ký tự, <code>%s</code> là tiêu đề (lời nhắn)"],
                  ["<code>git cat-file -p HEAD</code>", "in nội dung của một đối tượng Git, ở đây là commit mới nhất"],
                  ["<code>git rev-parse HEAD:phi.txt</code>", "in mã nội dung của tệp <code>phi.txt</code> trong commit mới nhất"],
                  ["<code>git log --graph --oneline</code>", "in lịch sử, mỗi commit một dòng, kèm đồ thị nhánh"]]),
           """Còn năm lệnh để xem lại. Lệnh đầu in nội dung một tệp. Lệnh thứ hai in lịch sử theo mẫu, mã băm đầy đủ rồi tiêu đề.
           Lệnh thứ ba in lần chốt mới nhất, lệnh thứ tư in mã nội dung của một tệp, lệnh thứ năm in lịch sử kèm đồ thị nhánh.""",
           clear=True),
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
           """Đây là đồ thị lịch sử của ví dụ. Bên trái là lần chốt gốc, phí năm nghìn năm trăm. Nhánh tang ở trên đổi thành sáu nghìn sáu trăm, nhánh chính ở dưới đổi thành bốn nghìn bốn trăm.
           Mỗi mũi tên trỏ về cha, và lần chốt gộp bên phải có hai mũi tên, tức là hai cha."""),
        st(svg(1500, 430,
               box(30, 110, 420, 210, ["commit 0eac7e6", "tree 4ed712d", "parent a8af580", "parent 577eea4", "An, lời nhắn"], C_GREEN, size=24, bold=True),
               box(560, 165, 380, 100, ["tree 4ed712d", "phi.txt → a9b66cb"], C_PURPLE, size=24, bold=True),
               box(1050, 165, 400, 100, ["blob a9b66cb", "phi=6600"], C_AMBER, size=24, bold=True),
               arrow(450, 215, 555, 215), arrow(940, 215, 1045, 215),
               txt(750, 305, "tree = danh sách tên tệp và mã nội dung", 22), txt(1250, 305, "blob = nội dung một tệp", 22),
               txt(750, 400, "Đổi một chữ trong tệp → mã blob đổi → mã tree đổi → mã commit đổi", 26, "middle", "#1f2937", True)),
           """Bên trong, một lần chốt không lưu phần thay đổi, mà lưu ảnh chụp cả cây tệp. Lần chốt trỏ tới một cây, cây ghi tên tệp phí và mã của nội dung. Phần nội dung một tệp mà Git lưu, ta gọi là khối nội dung.
           Mỗi tầng được đặt tên bằng mã băm của chính nó, nên đổi một chữ trong tệp thì mã của cả ba tầng đều đổi."""),
    ], checks=["alg.bnx_git_demo()['merge'].startswith('0eac7e6') and alg.bnx_git_demo()['tree6600'].startswith('4ed712d')",
               "alg.bnx_git_demo()['blob6600'].startswith('a9b66cb') and alg.bnx_git_demo()['root'].startswith('18bdd9f')",
               "alg.bnx_git_demo()['tang'].startswith('577eea4') and alg.bnx_git_demo()['giam'].startswith('a8af580')"])
    form = sc("formula", "formula", "Suy ra từng bước: khi nào gộp tự xong, khi nào xung đột", [
        st("""<p><b>Bước 1.</b> Git tìm <b>commit chung gần nhất</b> của hai nhánh, vì chỉ so với điểm xuất phát chung mới biết <i>ai đã đổi gì</i>.</p>
<span class='note'>Làm thử: <code>main</code> = gốc → 4400; <code>tang</code> = gốc → 6600; chung = gốc <code>18bdd9f</code> (5500).</span>""",
           """Bước một, máy tìm lần chốt chung gần nhất của hai nhánh, vì chỉ khi so với điểm chung mới biết ai đã đổi gì.
           Làm thử, cả hai nhánh đi ra từ lần chốt gốc, nên điểm chung là phí năm nghìn năm trăm."""),
        st("""<p><b>Bước 2.</b> So <b>từng bên với gốc</b>, không so hai bên với nhau.</p>
$$\\text{main: } 4\\,400 - 5\\,500 = \\hl{-1\\,100} \\qquad \\text{tang: } 6\\,600 - 5\\,500 = \\hl{1\\,100}$$
<span class='note'>Phép trừ chỉ để ta dễ thấy. Máy không tính số: nó so <b>chữ</b> từng dòng, dòng <code>phi=4400</code> khác dòng <code>phi=5500</code> là đủ.</span>""",
           """Bước hai, máy so từng bên với gốc chứ không so hai bên với nhau.
           Nhánh chính giảm một nghìn một trăm, nhánh tang tăng một nghìn một trăm, nên cả hai đều đổi cùng một dòng. Máy không tính số mà so chữ từng dòng.""", focus=[1, 2, 3]),
        st(table(["gốc", "main", "tang", "kết quả gộp"],
                 [["5500", "5500", "6600", "6600 — chỉ tang đổi, lấy tang"],
                  ["5500", "4400", "5500", "4400 — chỉ main đổi, lấy main"],
                  ["5500", "6600", "6600", "6600 — hai bên đổi giống nhau"],
                  ["5500", "4400", "6600", "<b class='red'>xung đột</b> — hai bên đổi khác nhau: người quyết"]]),
           """Bước ba là luật gộp ba chiều mà máy áp dụng. Nếu chỉ một bên đổi hoặc hai bên đổi giống nhau, máy lấy luôn bản đã đổi.
           Còn khi hai bên đổi cùng một dòng thành hai giá trị khác nhau, máy không có cơ sở chọn, nên dừng lại để người quyết.""",
           introduces=["bnx_gop_ba_chieu"]),
    ], checks=["4400 - 5500 == -1100 and 6600 - 5500 == 1100",
               "alg.bnx_merge3('5500', '5500', '6600') == ('ok', '6600') and alg.bnx_merge3('5500', '4400', '5500') == ('ok', '4400')",
               "alg.bnx_merge3('5500', '6600', '6600') == ('ok', '6600') and alg.bnx_merge3('5500', '4400', '6600')[0] == 'conflict'"])
    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(code(GIT_INIT),
           """Giờ ta chạy thật từng lệnh. Năm dòng đầu cố định người viết và giờ chốt, để ai chạy lại cũng ra đúng các mã này.
           Sau đó ta tạo kho trong thư mục tạm, ghi phí năm nghìn năm trăm, chốt và in lịch sử theo mẫu.""",
           ),
        st(out(GIT_INIT_OUT) + """$$① \\; 40 \\text{ ký tự} \\cdot 4 \\text{ bit} = \\hl{160} \\text{ bit}$$""",
           """Máy in ra mã của lần chốt gốc, đếm được bốn mươi ký tự. Phép tính thứ nhất, bốn mươi ký tự nhân bốn bít bằng một trăm sáu mươi bít."""),
        st(code(GIT_BRANCH),
           """Tiếp theo ta tạo nhánh tang, sửa phí thành sáu nghìn sáu trăm rồi chốt, về nhánh chính sửa thành bốn nghìn bốn trăm rồi chốt, và gộp nhánh tang vào.
           Cuối cùng lệnh in tệp cho ta thấy nội dung.""", clear=True),
        st(out(GIT_BRANCH_OUT) + """<p>② 3 dấu mốc chia tệp thành <b>2</b> phiên bản: <code>main</code> 4400, <code>tang</code> 6600.</p>""",
           """Máy báo xung đột ở tệp phí và dừng lại, đúng như luật gộp ba chiều. Phép tính thứ hai, ba dấu mốc chia tệp thành hai phiên bản, bốn nghìn bốn trăm và sáu nghìn sáu trăm.""",
           clear=True, focus=[2, 3]),
        st(code(GIT_RESOLVE) + """<p>③ Người quyết giữ 6600 <span class='note'>(số minh hoạ)</span>: so với <code>main</code> tăng $6\\,600 - 4\\,400 = \\hl{2\\,200}$.</p>""",
           """Xung đột không phải do hỏng hóc, mà là hai người sửa cùng chỗ và người phải quyết. Giả sử người phụ trách sản phẩm chọn sáu nghìn sáu trăm.
           Ta ghi lại dòng phí rồi chốt. Phép tính thứ ba, so với nhánh chính phí tăng hai nghìn hai trăm.""",
           clear=True, focus=[0, 2, 1, 2]),
        st(out(GIT_RESOLVE_OUT1, "Kết quả chạy thật: nội dung commit gộp") + """<p>④ Có <b>2</b> dòng <code>parent</code> → commit gộp có <b>2 cha</b>.</p>""",
           """Lệnh xem nội dung in ra lần chốt gộp, đúng như hình ảnh chụp lúc nãy. Phép tính thứ tư, có hai dòng cha, một của nhánh chính và một của nhánh tang.""",
           clear=True, focus=[2, 3]),
        st(out(GIT_RESOLVE_OUT2, "Kết quả chạy thật: đồ thị commit") + """$$⑤ \\; 3 + 1 = \\hlg{4} \\text{ commit}$$""",
           """Đồ thị vẽ bằng ký tự cho thấy hai nhánh tách ra từ gốc rồi nhập lại. Phép tính thứ năm, ba lần chốt trước khi gộp cộng một lần chốt gộp, bằng bốn lần chốt.""",
           clear=True, focus=[2, 2, 3]),
    ], checks=["alg.bnx_is_hex40(alg.bnx_git_demo()['root']) and alg.bnx_hex_bits(40) == 160",
               "len(alg.bnx_markers(alg.bnx_conflict_file('phi=4400', 'phi=6600'))) == 3 and alg.bnx_merge3('5500', '4400', '6600')[0] == 'conflict'",
               "6600 - 4400 == 2200",
               "alg.bnx_git_demo()['merge'] != alg.bnx_git_demo()['tang'] and len([alg.bnx_git_demo()['giam'], alg.bnx_git_demo()['tang']]) == 2",
               "(lambda r: alg.bnx_reachable({r['merge']: [r['giam'], r['tang']], r['giam']: [r['root']], r['tang']: [r['root']]}, r['merge']))(alg.bnx_git_demo()) == 3 + 1"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: tự tính mã băm", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>import hashlib</code>", "nạp thư viện băm có sẵn của Python"],
                  ["<code>\"phi=6600\\n\".encode()</code>", "đổi chuỗi chữ thành dãy byte để băm; <code>\\n</code> là ký tự xuống dòng"],
                  ["<code>f\"blob {len(noi_dung)}\\0\"</code>", "chuỗi có <code>f</code> đầu: phần trong ngoặc nhọn được thay bằng giá trị, <code>len</code> đếm độ dài; <code>\\0</code> là ký tự rỗng; <code>blob</code> là loại đối tượng chứa nội dung tệp, Git viết chữ này đầu chuỗi trước khi băm"],
                  ["<code>hashlib.sha1(…)</code>", "băm bằng SHA-1, cùng thuật toán Git dùng, ra 160 bit"],
                  ["<code>.hexdigest()</code>", "viết mã băm thành chuỗi thập lục phân"]]),
           """Mã Python sắp tới có vài cách viết mới. Dòng đầu nạp thư viện băm. Hàm đổi chữ thành dãy byte để băm, gạch ngược n là xuống dòng.
           Chuỗi có chữ f đứng đầu thì phần trong ngoặc nhọn được thay bằng giá trị, còn chữ đầu chuỗi là loại đối tượng, ở đây là khối nội dung tệp. Hàm băm cùng thuật toán đó, hàm cuối viết mã băm thành chuỗi thập lục phân."""),
        st(code(PY_BLOB) + out(PY_BLOB_OUT),
           """Ta kiểm bằng đường khác: tự tính mã băm bằng Python.
           Nội dung tệp có tám ký tự và một ký tự xuống dòng, nên dài chín ký tự. Cách ghép là loại nội dung, độ dài, một ký tự rỗng rồi nội dung, và băm cả chuỗi.
           Kết quả trùng từng ký tự với mã nội dung đã in ở ví dụ.""",
           focus=[0, 1, 3], clear=True),
        st(table(["đối tượng", "git in ra", "Python thuần tự tính"],
                 [["nội dung phi=6600", "a9b66cb…", "a9b66cb…"],
                  ["commit gốc", "18bdd9f…", "18bdd9f…"],
                  ["commit gộp (2 cha)", "0eac7e6…", "0eac7e6…"]]),
           """Dựng lại cả các lần chốt bằng Python thuần cũng ra mã khớp, nên mã chốt chỉ phụ thuộc nội dung, cha, người viết, giờ và lời nhắn.""",
           clear=True),
    ], checks=["alg.bnx_git_blob('phi=6600\\n') == alg.bnx_git_demo()['blob6600'] and len('phi=6600\\n') == 9",
               "alg.bnx_git_demo()['root'].startswith('18bdd9f') and alg.bnx_git_demo()['merge'].startswith('0eac7e6')",
               "alg.bnx_git_commit(alg.bnx_git_demo()['tree6600'], [alg.bnx_git_demo()['giam'], alg.bnx_git_demo()['tang']], 'Gộp nhánh tang: chốt 6600') == alg.bnx_git_demo()['merge']"])
    quymo = sc("quymo", "example", "Khi cả nhóm cùng sửa một dòng: xung đột tăng theo số nhánh", [
        st(table(["cách viết", "nghĩa", "ví dụ"],
                 [["<code>for i in `seq 1 3`; do … done</code>", "<code>seq 1 3</code> in dãy 1, 2, 3; vòng lặp chạy phần giữa ba lần, <code>i</code> lần lượt là 1, 2, 3", "<code>&#36;i</code> là giá trị hiện tại"],
                  ["<code>lệnh_a &amp;&amp; lệnh_b</code>", "<code>lệnh_b</code> chỉ chạy khi <code>lệnh_a</code> thành công", "vào thư mục tạm xong mới <code>git init</code>"],
                  ["<code>lệnh_a ; lệnh_b</code>", "dấu chấm phẩy ngăn hai lệnh trên một dòng, chạy lần lượt dù lệnh trước ra sao", "<code>git switch -q main; xd=0</code>"],
                  ["<code>git switch -q -c n&#36;i main</code>", "tạo nhánh <code>n1</code>, <code>n2</code>… mỗi nhánh xuất phát từ <code>main</code>; <code>-q</code> là im lặng", "i = 2 thì nhánh <code>n2</code>"]]),
           """Khối đo dùng thêm vài cách viết. Vòng lặp chạy phần giữa ba lần, biến đếm nhận lần lượt từng số. Hai dấu và liền nhau nghĩa là lệnh sau chỉ chạy khi lệnh trước thành công.
           Dấu chấm phẩy ngăn hai lệnh cùng dòng, chạy lần lượt. Lệnh tạo nhánh có số thứ tự, nhánh nào cũng xuất phát từ nhánh chính.""",
           clear=True),
        st(table(["cách viết", "nghĩa", "ví dụ"],
                 [["<code>lệnh_a || { lệnh_b; lệnh_c; }</code>", "phần trong ngoặc nhọn gom nhiều lệnh, chỉ chạy khi <code>lệnh_a</code> thất bại", "gộp xung đột thì thất bại"],
                  ["<code>git merge --abort</code>", "huỷ lần gộp đang dở, trả tệp về như trước khi gộp", "để gộp nhánh kế tiếp"],
                  ["<code>xd=&#36;((xd+1))</code>", "tính số nguyên rồi gán lại", "xd = 2 thì thành 3"],
                  ["<code>&gt;/dev/null</code>", "vứt đầu ra thường vào tệp rỗng", "giấu thông báo gộp"]]),
           """Hai gạch đứng nghĩa là phần trong ngoặc nhọn chỉ chạy khi lệnh trước thất bại, như gộp bị xung đột, rồi lệnh huỷ gộp trả tệp về như cũ.
           Hai cặp ngoặc tròn tính số nguyên, đường dẫn rỗng là nơi vứt đầu ra.""",
           clear=True),
        st(code(GIT_SCALE, "Đo thật: N nhánh cùng sửa dòng phí, gộp lần lượt vào main"),
           """Bây giờ ta đo khi nhóm lớn dần. Biến N là số người, mỗi người một nhánh cùng sửa dòng phí.
           Rồi ta gộp lần lượt từng nhánh vào nhánh chính, lần gộp nào thất bại là một xung đột, ta huỷ gộp và đếm.""",
           focus=[0, "2.2", "2.7", "2.10"], clear=True),
        st(out(GIT_SCALE_OUT) + table(["số nhánh N", "xung đột phải giải", "nếu mỗi người sửa tệp riêng", "mỗi lần 3 phút (số minh hoạ)"],
                                      [["2", "1", "0", "3 phút"], ["10 (gấp 5 lần cỡ 2)", "9", "0", "27 phút"], ["50 (gấp 25 lần cỡ 2)", "49", "0", "147 phút, gần 2,5 giờ"]])
           + """$$\\text{xung đột} = N - 1 \\qquad (N = 2, 10, 50 \\Rightarrow 1,\\; 9,\\; \\hl{49})$$""",
           """Máy báo mười nhánh thì chín xung đột, còn hai và năm mươi nhánh cho một và bốn mươi chín.
           Vì nhánh đầu gộp được, còn mỗi nhánh sau đụng vào dòng đã đổi, nên xung đột bằng N trừ một. Với ba phút mỗi lần, số minh hoạ, năm mươi người tốn gần hai giờ rưỡi. Mỗi người một tệp riêng thì cả ba cỡ đều không xung đột.""",
           focus=[0, 1, 2, 2], clear=True),
        st(table(["cách làm", "đo được", "được", "mất"],
                 [["mỗi người một nhánh sống lâu, gộp một lần cuối kỳ", "N − 1 xung đột dồn một ngày, mỗi cái đã cũ và khó nhớ lý do", "không ai phải theo ai", "ngày gộp là ngày rủi ro"],
                  ["nhánh ngắn, gộp vào main hằng ngày", "mỗi lần chỉ vài dòng lệch, người sửa còn nhớ", "xung đột nhỏ và sớm", "phải kỷ luật lấy về trước khi gộp"],
                  ["tách tệp: mỗi người một tệp hoặc mô-đun", "đo cùng chương trình khi mỗi người sửa tệp riêng: 0 xung đột", "gần như hết xung đột", "chỉ tách được khi công việc tách được"]]),
           """Người làm nghề chọn giữa ba cách. Nhánh sống lâu dồn xung đột vào ngày gộp, nhánh ngắn gộp hằng ngày chia nhỏ chúng, tách tệp thì không xung đột nếu công việc tách được.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l00_conflicts(n) for n in (2, 10, 50)] == [1, 9, 49]",
               "[alg.bnx_l00_minutes(alg.bnx_l00_conflicts(n), 3) for n in (2, 10, 50)] == [3, 27, 147]",
               "[alg.bnx_l00_conflicts_split(n) for n in (2, 10, 50)] == [0, 0, 0]",
               "50 // 2 == 25 and 10 // 2 == 5 and 147 / 60 == 2.45"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st(f"""<div class="box warn"><b>Lỗi 1 (người mới).</b> Thấy xung đột tưởng Git hỏng, xoá kho tải lại; hoặc sửa vội mà <b class="red">để sót</b> dòng <code>{LT} HEAD</code> trong tệp cấu hình rồi commit.
<br><span class="note">Phép thử: sau <code>git add</code>, chạy <code>git diff --cached --check</code>. <code>git diff --cached</code> so vùng chờ với lần chốt gần nhất; <code>--check</code> không in khác biệt mà chỉ tìm lỗi, như dấu mốc còn sót, và báo “leftover conflict marker”.</span></div>""",
           """Lỗi thứ nhất của người mới là thấy xung đột lại tưởng công cụ hỏng, rồi xoá kho tải lại, hoặc sửa vội mà để sót dấu mốc trong tệp.
           Phép thử là lệnh so vùng chờ với lần chốt gần nhất, có tuỳ chọn kiểm lỗi để chỉ báo còn sót dấu mốc."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Commit tệp <code>.env</code> chứa mật khẩu, rồi xoá ở commit sau. <code>.env</code> là tệp cấu hình ẩn (tên bắt đầu bằng dấu chấm), nơi hay để mật khẩu.</div>"""
           + table(["lệnh", "nghĩa"],
                   [["<code>git switch -c thu 18bdd9f</code>", "tạo nhánh <code>thu</code> xuất phát từ commit có mã <code>18bdd9f</code>, thay vì từ chỗ đang đứng"],
                    ["<code>git rm .env</code>", "xoá tệp khỏi cây; <code>git ls-files</code> liệt kê các tệp đang được theo dõi"],
                    ["<code>git log --format=\"%h %s\"</code>", "như lệnh log ban nãy, nhưng <code>%h</code> là mã ngắn 7 ký tự, <code>%s</code> là lời nhắn"],
                    ["<code>git show 57d5547:.env</code>", "in tệp <code>.env</code> đúng như ở commit có mã <code>57d5547</code>"]]),
           """Lỗi thứ hai, của người đã đi làm. Lỡ chốt tệp cấu hình ẩn chứa mật khẩu, rồi xoá nó ở lần chốt sau và yên tâm là đã hết.
           Lệnh đầu tạo nhánh mới từ một lần chốt cũ, lệnh xoá tệp, lệnh xem lịch sử với mã ngắn bảy ký tự, và lệnh in tệp đúng như ở một lần chốt cũ.""",
           clear=True),
        st(code(GIT_SECRET), """Ta chạy cả chuỗi: chốt tệp mật khẩu, xoá tệp rồi chốt lần nữa, rồi xem ba kết quả cuối.""",
           clear=True),
        st(out(GIT_SECRET_OUT) + """<div class="box key">Tệp đã biến khỏi cây hiện tại, nhưng commit cũ <code>57d5547</code> vẫn trả lại mật khẩu. <b>Cách chữa: đổi mật khẩu ngay</b>, rồi mới tính chuyện dọn lịch sử.</div>""",
           """Danh sách tệp hiện tại chỉ còn tệp phí, nhưng lệnh xem tệp ở lần chốt cũ vẫn trả lại nguyên mật khẩu.
           Nên cách chữa là đổi mật khẩu ngay, vì xoá ở lần chốt sau không xoá được nó khỏi lịch sử.""",
           clear=True, focus=[2, 3]),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <code>git push --force</code> (đẩy và ép ghi đè) lên nhánh chung: máy chủ bị ghi đè bằng lịch sử trên máy mình, commit đồng nghiệp vừa đẩy lên <b class="red">mất khỏi nhánh</b>.
<br><span class="note">Cách chữa: khoá nhánh <code>main</code> trên máy chủ không cho ép đẩy. <code>git push --force-with-lease</code> từ chối khi máy chủ có commit mình chưa thấy, nhưng nếu máy mình vừa lấy về (kể cả công cụ lấy ngầm) thì nó coi là đã thấy và vẫn ghi đè.</span></div>""",
           """Lỗi thứ ba là ép đẩy lên nhánh chung: máy chủ bị ghi đè, nên lần chốt đồng nghiệp vừa đẩy biến khỏi nhánh.
           Cách chữa chắc chắn là khoá nhánh chính không cho ép đẩy, vì ép đẩy kèm điều kiện vẫn ghi đè.""", clear=True),
    ], checks=["alg.bnx_git_demo()['secret_add'].startswith('57d5547') and alg.bnx_git_demo()['secret_rm'].startswith('96f907b')",
               "len(alg.bnx_markers(alg.bnx_conflict_file('phi=4400', 'phi=6600'))) == 3"])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Gốc <code>phi=5500</code>. Nhánh A sửa thành 7700, nhánh B không chạm tệp phí. Gộp B vào A có xung đột không? Tệp còn giá trị nào?"],
                  ["2", "Lịch sử đang có 4 commit như ví dụ. Nhánh X rẽ ra từ commit gốc và có 2 commit riêng chưa nằm trong 4 commit đó; <code>main</code> cũng đã có commit mà X chưa có. Bạn gộp X vào <code>main</code> (không xung đột). Sau khi gộp có bao nhiêu commit? Commit mới có mấy cha?"],
                  ["3", "Quyết định: mật khẩu đã lên máy chủ chung được 10 phút. Đổi mật khẩu ngay, hay viết lại lịch sử để xoá rồi ép đẩy?"]]),
           """Bây giờ tới phần bạn tự làm bài, ba câu trên màn hình. Câu hai gộp nhánh X có hai lần chốt riêng, trong khi nhánh chính cũng đã có lần chốt mà X chưa có. Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: chỉ nhánh A đổi so với gốc.</p>
$$\\text{gốc } 5\\,500,\\ \\text{A } 7\\,700,\\ \\text{B } 5\\,500 \\;\\Rightarrow\\; \\hlg{7\\,700},\\ \\text{không xung đột}$$""",
           """Đáp án câu một. So từng bên với gốc, chỉ nhánh A đổi, nên Git lấy bên đã đổi theo luật gộp ba chiều. Tệp còn bảy nghìn bảy trăm và không có xung đột."""),
        st("""<p>Câu 2: dùng lại 4 commit của ví dụ.</p>
$$4 + 2 + 1 = \\hlg{7} \\text{ commit}, \\qquad \\text{commit gộp có } \\hl{2} \\text{ cha}$$
<span class='note'>Cả hai bên đều có commit riêng nên phải tạo commit gộp. Nếu <code>main</code> không có commit mới, Git chỉ tua nhanh: 4 + 2 = 6 commit, không có commit gộp.</span>""",
           """Đáp án câu hai. Bốn lần chốt của ví dụ, cộng hai lần chốt riêng của nhánh kia, cộng một lần chốt gộp, bằng bảy lần chốt, và lần chốt gộp có hai cha. Nếu nhánh chính không có gì mới thì chỉ tua nhanh, ra sáu lần chốt, không có lần chốt gộp."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["đổi mật khẩu ngay (bắt buộc)", "mật khẩu cũ vô dụng, kể cả trên mọi bản sao đã tải về", "phải cập nhật cấu hình mọi nơi dùng mật khẩu đó"],
                  ["viết lại lịch sử rồi ép đẩy (làm thêm)", "kho sạch cho người tải sau", "mọi người phải lấy lại kho; bản sao cũ vẫn còn mật khẩu; ép đẩy nhánh chung"]]),
           """Đáp án câu ba. Đổi mật khẩu ngay là bắt buộc, vì trong mười phút đó bản sao kho có thể đã nằm trên máy khác. Viết lại lịch sử chỉ làm thêm, bản sao cũ vẫn giữ mật khẩu."""),
    ], checks=["alg.bnx_merge3('5500', '7700', '5500') == ('ok', '7700')", "4 + 2 + 1 == 7"])
    lab_pr = practice_scene(sc, "Tự làm: hai nhánh cùng sửa một dòng lãi suất", practice_steps2(
        st, "BNX", "L00",
        """<p><b>Đề</b> (số minh hoạ): viết <code>lab.sh</code>, bốn dòng đầu chép từ <code>de.md</code> (đặt tên người viết, chuyển vào thư mục tạm).</p>
<ol><li>Tạo kho; tệp <code>lai.txt</code> ghi <code>lai=7</code>; chốt <code>goc</code></li>
<li>Nhánh <code>giam</code>: <code>lai=6</code> chốt, rồi thêm tệp <code>ghi_chu.txt</code> và chốt</li>
<li>Về <code>main</code>: <code>lai=8</code>, chốt, rồi gộp <code>giam</code> (có xung đột)</li>
<li>Giải xung đột giữ <code>lai=8</code> và chốt gộp; in ba dòng cho sẵn</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Viết một tệp lệnh tạo kho, tạo nhánh giảm với hai lần chốt riêng, rồi về nhánh chính sửa lãi suất thành tám và chốt.
        Gộp nhánh giảm vào, giữ lãi suất tám, chốt gộp rồi in ba dòng cho sẵn. Hãy dừng video và tự viết.""",
        LAB_OUT, "lab.sh",
        """<div class="box key"><b>Nếu kẹt:</b> xung đột nghĩa là tệp đang chứa dấu mốc; ghi đè <code>lai.txt</code> bằng <code>echo "lai=8" &gt; lai.txt</code>, rồi <code>git add</code> và <code>git commit</code>.
Nhánh <code>giam</code> có 2 lần chốt, <code>main</code> có 2 (gốc và tăng), cộng 1 lần chốt gộp. Lời giải ở <code>labs/BNX/L00/loi_giai.sh</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, nhớ rằng xung đột nghĩa là tệp đang chứa dấu mốc, nên ghi đè nó bằng dòng lãi suất tám, đưa vào vùng chờ rồi chốt. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=180), "BNX", "L00")
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("commit = ảnh chụp có mã băm", "nhánh = nhãn trỏ commit", "gộp ba chiều so với gốc", "cùng dòng khác nhau: người quyết", "lịch sử không quên"),
           """Mỗi lần chốt là ảnh chụp có mã băm, nhánh chỉ là nhãn trỏ vào lần chốt, và khi gộp máy so từng bên với gốc.
           Hai bên đổi cùng dòng thì người quyết, nhiều nhánh sống lâu thì xung đột tăng, lịch sử không quên."""),
        st("""<div class='box key'><b>Tư duy:</b> mã commit là <b>tên duy nhất của một trạng thái mã nguồn</b>. Cái gì đã commit thì coi như đã công bố cho mọi người có bản sao kho.</div>""",
           """Và đây là điều cần mang theo sau bài. Mã chốt là tên duy nhất của một trạng thái mã nguồn, và cái gì đã chốt thì coi như đã công bố cho mọi người có bản sao kho."""),
        st(table(["bài", "nội dung của khoá (phần 1)"],
                 [["Bài 0", "bài này: công cụ Git"],
                  ["Bài 1–2", "hợp đồng giữa các dịch vụ: OpenAPI, gRPC"],
                  ["Bài 3–5", "xác thực: JWT, OAuth 2.0, mTLS"],
                  ["Bài 6–7 và 37–38", "cơ sở dữ liệu lớn: Oracle và SQL Server"],
                  ["Bài 8–10", "kho dữ liệu và hàng đợi khác: Elasticsearch, Couchbase, Kafka"],
                  ["Bài 11–12", "nghiệp vụ: thanh toán quốc tế, ví điện tử, thuế điện tử"],
                  ["Bài 13–15", "đóng gói và triển khai, mã chốt gắn lên bản chạy; kiến trúc cổng API; dự án mẫu"]]),
           """Đây là bản đồ cả khoá. Bài một và hai là hợp đồng giữa các dịch vụ, bài ba đến năm là xác thực, bài sáu và bảy là cơ sở dữ liệu lớn, rồi kho dữ liệu khác, nghiệp vụ và triển khai.""",
           forward_ref=True, clear=True),
        st(table(["bài", "nội dung của khoá (phần 2)"],
                 [["Bài 16–20", "đa luồng Java, bảo mật Spring, kiểm thử, Redis nâng cao, Go"],
                  ["Bài 21–23", "cho vay số, Adobe Experience Manager, phát hiện bất thường bằng học máy"],
                  ["Bài 24–26", "JPA/Hibernate, giao dịch Spring, Maven và Jenkins"],
                  ["Bài 27–29", "tích hợp hệ cũ và tệp lô, so sánh cơ sở dữ liệu, tách ghi và đọc"],
                  ["Bài 30–32", "chịu lỗi, quan sát hệ thống, GitOps"],
                  ["Bài 33–36", "hệ cũ, phê duyệt tín dụng, vận hành, phỏng vấn thiết kế hệ thống"]]),
           """Phần hai đi từ bài mười sáu đến bài ba mươi sáu, nơi phỏng vấn thiết kế hệ thống ráp lại mọi thứ.""",
           forward_ref=True, clear=True),
    ])
    scenes = [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec]
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            _merge_short(s_)
    if not GIT_SPOKEN:
        for sc_ in scenes:
            for s_ in sc_["steps"]:
                s_["say"] = _say_no_git(s_["say"])
    return lesson("L00", "git_nhanh_gop_xung_dot", "Bài 0 — Git: lưu lịch sử, tạo nhánh, gộp và giải xung đột",
                  "curriculum/bnx.yaml L00; audit/bnx/verify_bnx.py L00; git 2.53 chạy thật (OBSERVED 2026-11-11); git-scm.com tài liệu git-merge, git-show, git-push (--force-with-lease)",
                  ["Tạo kho, ghi một commit và đọc lịch sử", "Tạo nhánh, gộp nhánh và đọc đồ thị commit",
                   "Đọc dấu xung đột và giải xung đột bằng tay", "Nêu vì sao bí mật đã commit vẫn còn trong lịch sử",
                   "Đếm số xung đột khi nhiều nhánh cùng sửa một dòng, đo thật ở 2, 10 và 50 nhánh",
                   "Tự viết chuỗi lệnh tạo kho, hai nhánh cùng sửa một dòng, giải xung đột và đếm lịch sử"],
                  scenes,
                  covers=[(1, "example"), (2, "example"), (3, "example"), (4, "pitfalls"), (5, "quymo"), (6, "practice")])


LT, GT = "&lt;" * 7, "&gt;" * 7
