"""DMS L04 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l04.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L04"

C1 = r"""for n in (10, 1000, 1000000):
    tong = 0
    for k in range(1, n + 1):
        tong = tong + 2 * k - 1
    print(n, 'so le: cong', n, 'lan, tong =', tong, ', n * n =', n * n)"""
O1 = run_py(C1)
print(O1)

TAB = read_step([
    ("for n in (10, 1000, 1000000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 10, rồi 1000, rồi 1000000"),
    ("range(1, n + 1)", "các số từ 1 tới n (số sau trong ngoặc không lấy)", "range(1, 5) cho 1, 2, 3, 4"),
    ("tong = tong + 2 * k - 1", "một dấu bằng là <b>gán</b>; <code>*</code> là nhân; dòng này cộng số lẻ thứ k, tức 2k − 1, vào tong", "k = 3: 2 * 3 - 1 = 5"),
    ("print(n, 'so le', n * n)", "in các giá trị ra cửa sổ, cách nhau một dấu cách; <code>n * n</code> là n nhân n", "n = 10 thì n * n là 100"),
], "Chương trình cộng số lẻ dùng bốn ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 10, một nghìn, rồi một triệu, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số với hai số trong ngoặc cho các số từ số đầu tới số sau trừ 1, nên với 1 và n cộng 1 nó cho đúng các số từ 1 tới n.",
    "Dòng này gán: cộng số lẻ thứ k, tức hai nhân k trừ 1, vào tổng, trong đó dấu sao là phép nhân.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách, còn n sao n là n nhân n.",
])

quymo = scene("quymo", "example", "Khi n lớn dần: n phép cộng hay một công thức đã chứng minh", [
    TAB,
    step(
        "<p><b>Chạy thật</b>: cộng tay từng số lẻ đầu tiên với $n = 10$, 1 000, 1 000 000 rồi so với $n \\times n$</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Vòng lặp cộng từng số lẻ, số lẻ thứ k là 2k trừ 1, rồi in tổng cùng n nhân n. Với n bằng 10 phải cộng 10 lần, với n bằng một nghìn phải cộng một nghìn lần, "
        "với n bằng một triệu phải cộng một triệu lần. Ở cả ba cỡ, tổng đúng bằng n nhân n, đúng như điều quy nạp đã chứng minh.",
        focus=[2, ["2.3", "2.4"], "4.1", "4.2", "4.3"][:4], clear=True),
    step(
        '<table class="t"><tr><th>$n$</th><th>cộng từng số lẻ</th><th>dùng $n^2$ đã chứng minh</th></tr>'
        "<tr><td>1 000</td><td>1 000 phép cộng</td><td>1 phép nhân</td></tr>"
        "<tr><td>$10^9$</td><td>$10^9$ phép cộng, khoảng 1 giây (một tỉ phép mỗi giây, số minh hoạ)</td><td>1 phép nhân</td></tr>"
        "<tr><td>$10^{18}$</td><td>$10^{18}$ phép cộng, khoảng 32 năm</td><td>1 phép nhân</td></tr>"
        "<tr><td>mọi $n$</td><td>không bao giờ xong</td><td><b>1 phép nhân, nhờ chứng minh bằng quy nạp</b></td></tr></table>"
        '<div class="box key">Chứng minh quy nạp cho ta một công thức đúng với <b>mọi</b> n. Công thức đổi chi phí từ tỉ lệ với n thành một phép tính.</div>',
        "Bảng này cho thấy giá trị của một chứng minh. Cộng từng số lẻ tốn số phép cộng bằng n, với n bằng mười mũ chín thì khoảng một giây, với mười mũ mười tám thì khoảng ba mươi hai năm. "
        "Còn công thức n bình phương, đã chứng minh bằng quy nạp, chỉ tốn một phép nhân dù n là bao nhiêu. Người làm nghề chọn công thức đã được chứng minh thay cho vòng lặp dài.",
        focus=[1, "1.3", "1.4", 2], clear=True),
], checks=[
    "[sum(2 * k - 1 for k in range(1, n + 1)) for n in (10, 1000)] == [100, 1000000]",
    "sum(2 * k - 1 for k in range(1, 10 ** 6 + 1)) == 10 ** 12",
    "10 ** 9 / 1e9 == 1.0 and round(10 ** 18 / 1e9 / 86400 / 365.25) == 32",
])

DE = """# Lab DMS L04 — Quy nạp: kiểm hai bước cho công thức tổng bình phương

Viết `quynap.py` (Python 3.11 trở lên); chạy: `python quynap.py`.

Khẳng định cần chứng minh bằng quy nạp: tổng các bình phương 1² + 2² + ... + n² bằng n(n+1)(2n+1)/6. Đặt `tong(n)` là tổng cộng trực tiếp bằng vòng lặp, `ct(n) = n*(n+1)*(2*n+1)//6`.

In đúng bảy dòng:
1. `co so: <tong(1)> <ct(1)>`
2. bốn dòng, với n = 1, 2, 3, 4: `quy nap <n>-><n+1>: <tong(n)> + <(n+1)^2> = <tong(n) + (n+1)^2>, cong thuc <ct(n+1)>`
3. `kiem 1..1000: dung` nếu `tong(n) == ct(n)` với mọi n từ 1 đến 1000, ngược lại `kiem 1..1000: sai`
4. Một công thức SAI: `sai(n) = n*(n+1)*(n+2)//6`. Tìm n đầu tiên mà `tong(n) != sai(n)`, rồi in `cong thuc sai: co so dung, sai dau tien o n=<n>` (ở n = 1 công thức sai vẫn đúng: đó là lý do bước cơ sở đơn độc không đủ).

Gợi ý: `str(...)` đổi số thành chữ để ghép bằng dấu `+`; dùng vòng `while` cho phần 4.

Chấm: `bash labs/cham.sh DMS L04 quynap.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""def tong(n):
    t = 0
    for k in range(1, n + 1):
        t = t + k * k
    return t

def ct(n):
    return n * (n + 1) * (2 * n + 1) // 6

def sai(n):
    return n * (n + 1) * (n + 2) // 6

print('co so:', tong(1), ct(1))
for n in range(1, 5):
    print('quy nap ' + str(n) + '->' + str(n + 1) + ': ' + str(tong(n)) + ' + ' + str((n + 1) ** 2)
          + ' = ' + str(tong(n) + (n + 1) ** 2) + ', cong thuc ' + str(ct(n + 1)))
dung = True
for n in range(1, 1001):
    if tong(n) != ct(n):
        dung = False
print('kiem 1..1000:', 'dung' if dung else 'sai')
n = 1
while tong(n) == sai(n):
    n = n + 1
print('cong thuc sai: co so dung, sai dau tien o n=' + str(n))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> viết hàm <code>tong(n)</code> cộng từng $k^2$ bằng vòng lặp và hàm <code>ct(n)</code> theo công thức. '
            "Bước quy nạp từ n sang n+1 là: tong(n) cộng thêm $(n+1)^2$ phải bằng ct(n+1). Phần cuối dùng <code>while tong(n) == sai(n)</code> để tăng n. "
            "Lời giải ở <code>labs/DMS/L04/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, viết một hàm cộng từng bình phương bằng vòng lặp, và một hàm theo công thức. Bước quy nạp từ n sang n cộng một là, tổng cũ cộng thêm bình phương của n cộng một, phải bằng công thức ở n cộng một. "
            "Phần cuối dùng vòng lặp tăng n cho tới khi công thức sai bị lệch. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("def tong(n): ... return ...", "<code>def</code> đặt <b>tên</b> cho một đoạn tính nhận n; <code>return</code> là kết quả đoạn đó đưa ra; gọi <code>tong(3)</code> là chạy đoạn đó với n = 3", "def tong(n): return n * 2 thì tong(3) là 6"),
    ("while tong(n) == sai(n):", "lặp lại các dòng thụt vào <b>chừng nào</b> điều kiện còn đúng; <code>==</code> hỏi hai kết quả có bằng nhau không", "n = 1; while n < 3: n = n + 1 dừng khi n = 3"),
], [
    "Dòng định nghĩa hàm đặt tên cho một đoạn tính nhận n, và chữ trả về cho biết kết quả đoạn đó đưa ra.",
    "Vòng lặp cuối chạy chừng nào hai kết quả còn bằng nhau, và dừng ngay khi chúng lệch nhau.",
])

prac = practice(
    LID, "Tự làm: kiểm hai bước quy nạp cho tổng bình phương bằng chương trình",
    "<p><b>Đề</b>: viết <code>quynap.py</code> kiểm công thức $1^2 + 2^2 + \\dots + n^2 = n(n+1)(2n+1)/6$: in bước cơ sở, bốn lần “đẩy” từ $n$ sang $n+1$, "
    "kiểm mọi $n$ từ 1 đến 1 000, và tìm $n$ đầu tiên làm một công thức SAI bị bác bỏ (bảy dòng, định dạng ở <code>labs/DMS/L04/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Công thức sai vẫn đúng ở n = 1: bước cơ sở đơn độc chưa đủ.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình kiểm công thức tổng các bình phương. In bước cơ sở, rồi bốn lần đẩy từ n sang n cộng một, rồi kiểm mọi n từ một đến một nghìn. "
    "Cuối cùng tìm n đầu tiên làm một công thức sai bị bác bỏ, và để ý công thức sai vẫn đúng khi n có giá trị là một. Định dạng bảy dòng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "quynap.py", H_HTML, H_SAY,
    pause=300, focus1=[1, 1, 1, 1, 2, 0], focus3=H_FOC)
patch_cham(prac, LID, "quynap.py")

OBJ = [
    "Viết đủ bước cơ sở và bước quy nạp",
    "Chỉ ra chỗ dùng giả thiết quy nạp",
    "Dùng quy nạp mạnh khi bước sau cần nhiều giá trị trước",
    "Đếm số phép tính của cách cộng từng số hạng so với công thức đã chứng minh bằng quy nạp khi n lớn dần",
    "Viết chương trình kiểm bước cơ sở, bước quy nạp và tìm n đầu tiên bác bỏ một công thức sai",
]
repl = [
    # fix6 (R4): ASR nghe "bằng một" cuối câu thành "bằng mục" → đổi câu
    ("Bước cơ sở cho Q của 1. Áp bước quy nạp", "Bước cơ sở cho Q của 1, câu đầu tiên của hàng. Áp bước quy nạp"),
    ("Mũi tên xanh là bước cơ sở, đẩy đổ quân Q của 1, tức tổng bằng 1.", "Mũi tên xanh là bước cơ sở, đẩy đổ quân Q của 1, tức tổng có giá trị là 1."),
    ('tổng từ 1 đến n bằng n nhân n cộng 1, chia 2.', 'tổng từ 1 đến n bằng n nhân, trong ngoặc n cộng 1, rồi chia 2.'),
    ('rồi thay phần đầu bằng n nhân n cộng 1 chia 2, theo giả thiết quy nạp.', 'rồi thay phần đầu bằng n nhân, trong ngoặc n cộng 1, rồi chia 2, theo giả thiết quy nạp.'),
    ('được n nhân n cộng 1, cộng 2 nhân n cộng 1, tất cả chia 2.', 'được n nhân, trong ngoặc n cộng 1, cộng 2 nhân, trong ngoặc n cộng 1, rồi tất cả chia 2.'),
    ('đặt n cộng 1 ra ngoài, được n cộng 1 nhân n cộng 2, chia 2,', 'đặt thừa số n cộng 1 ra ngoài, được tích của n cộng 1 và n cộng 2, rồi chia 2,'),
    ("<b>tập hợp</b> — phép hợp, giao, hiệu", "<b>các nhóm phần tử</b> — phép hợp, giao, hiệu"),
    ("ta học tập hợp, các phép hợp, giao, hiệu", "ta học cách nói về một nhóm phần tử, các phép hợp, giao, hiệu"),
    ('        say: "Hãy nghĩ tới một hàng quân cờ', '        introduces: [dms_quynap]\n        say: "Hãy nghĩ tới một hàng quân cờ'),
    ('        say: "Câu giả sử Q của n đúng gọi là giả thiết quy nạp.', '        introduces: [dms_gtqn]\n        say: "Câu giả sử Q của n đúng gọi là giả thiết quy nạp.'),
    # fix4 (R2 SHOULD): lời đọc nói "quân cờ dựng đứng" (tên domino không đọc được: lexicon_vi.DMS.yaml) → màn hình dùng cùng tên, domino chỉ trong ngoặc
    ('title: "Một hàng domino dài vô tận"', 'title: "Một hàng quân cờ dựng đứng (domino) dài vô tận"'),
    ("<div class=\"box key\">Hàng domino: ①", "<div class=\"box key\">Hàng quân cờ dựng đứng (domino): ①"),
    ("<th>phải chứng minh</th><th>domino</th>", "<th>phải chứng minh</th><th>quân cờ dựng đứng</th>"),
    ('title: "Mỗi quân domino là một câu Q(n)"', 'title: "Mỗi quân cờ dựng đứng (domino) là một câu Q(n)"'),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "example"), (2, "example"), (3, "strong"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl,
                assumes_add=("dms_menhde", "dms_bct", "dms_dinhly", "dms_giathiet", "dms_phanvidu"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Ở cả ba cỡ n = 10, 1 000, 1 000 000 tổng bằng n nhân n"}))
