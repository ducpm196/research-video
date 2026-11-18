"""DMS L05 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l05.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L05"

C1 = r"""for n in (100, 10 ** 6):
    dem = 0
    for x in range(1, n + 1):
        if x % 2 == 0 or x % 3 == 0:
            dem = dem + 1
    print(n, 'duyet', n, 'so:', dem, ', cong thuc:', n // 2 + n // 3 - n // 6)
n = 10 ** 12
print(n, 'cong thuc:', n // 2 + n // 3 - n // 6)"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for n in (100, 10 ** 6):", "với mỗi n lần lượt trong ngoặc; <code>**</code> là lũy thừa, nên <code>10 ** 6</code> là 10 mũ 6, một triệu", "hai lượt: n = 100, rồi n = 1000000"),
    ("range(1, n + 1)", "các số từ 1 tới n (số sau trong ngoặc không lấy)", "range(1, 5) cho 1, 2, 3, 4"),
    ("if điều_kiện:", "<b>nếu</b> điều kiện đúng thì chạy các dòng thụt vào bên dưới, sai thì bỏ qua", "if 7 > 5: chạy; if 3 > 5: bỏ qua"),
    ("x % 2 == 0", "<code>%</code> là chia lấy <b>số dư</b>; <code>==</code> là so sánh bằng; dư 0 nghĩa là chia hết", "6 % 2 == 0 là True; 7 % 2 == 0 là False"),
    ("... or ...", "hoặc: đúng khi ít nhất một điều kiện đúng", "x = 9: chia hết cho 3, nên cả câu đúng"),
    ("dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng dem thêm 1", "dem đang là 4 thì thành 5"),
    ("n // 2 + n // 3 - n // 6", "<code>//</code> là chia lấy phần nguyên, bỏ phần lẻ", "n = 12: 6 + 4 - 2 = 8; 7 // 2 là 3"),
    ("print(a, b)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "print(7, 'so') in ra 7 so"),
], "Chương trình đếm hai cách dùng tám ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 100 rồi 10 mũ 6, trong đó hai dấu sao liền nhau là lũy thừa, nên 10 mũ 6 là một triệu.",
    "Hàm tạo dãy số cho các số từ 1 tới n, vì số sau trong ngoặc không được lấy.",
    "Chữ nếu kèm điều kiện nghĩa là: nếu điều kiện đúng thì chạy các dòng thụt vào bên dưới, còn sai thì bỏ qua.",
    "Dấu phần trăm là chia lấy số dư, và hai dấu bằng liền nhau là so sánh bằng, nên x phần trăm 2 bằng 0 nghĩa là x chia hết cho 2.",
    "Chữ giữa hai điều kiện là hoặc, nên dòng này đúng khi x chia hết cho 2 hoặc chia hết cho 3.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, bỏ phần lẻ, nên với n bằng 12, ba số hạng cho 6 cộng 4 trừ 2, được 8.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=4)

quymo = scene("quymo", "example", "Khi n lớn dần: duyệt từng số hay đếm bằng bao hàm–loại trừ", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: đếm các số từ 1 đến $n$ chia hết cho 2 hoặc 3 bằng hai cách</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Cách thứ nhất duyệt từng số từ 1 đến n rồi đếm các số chia hết cho 2 hoặc 3. "
        "Cách thứ hai dùng công thức bao hàm loại trừ, n chia 2 lấy phần nguyên, cộng n chia 3, trừ n chia 6. "
        "Với n bằng 100, cả hai cách cho 67. Với n bằng một triệu, cả hai cho 666 667. Với n bằng mười mũ mười hai, chỉ công thức kịp tính, và cho 666 666 666 667.",
        focus=[2, ["2.2", "2.5"], "2.6", "4.1", "4.2", "4.3"][:6], clear=True),
    step(
        '<table class="t"><tr><th>$n$</th><th>duyệt từng số</th><th>bao hàm–loại trừ (hai điều kiện: chia hết cho 2, cho 3)</th></tr>'
        "<tr><td>100</td><td>100 phép kiểm</td><td>3 phép chia</td></tr>"
        "<tr><td>$10^6$</td><td>$10^6$ phép kiểm</td><td>3 phép chia</td></tr>"
        "<tr><td>$10^{12}$</td><td>$10^{12}$ phép kiểm, khoảng 17 phút (một tỉ phép mỗi giây, số minh hoạ)</td><td>3 phép chia</td></tr>"
        "<tr><td>$10^{15}$</td><td>$10^{15}$ phép kiểm, khoảng 11,6 ngày</td><td>3 phép chia</td></tr></table>"
        '<div class="box key">Duyệt từng số tốn <b>tỉ lệ với n</b>; với hai điều kiện, bao hàm–loại trừ chỉ tốn <b>3 phép chia</b>, vì đếm theo tập chứ không đếm từng phần tử.</div>',
        "Bảng này so hai cách khi n lớn dần. Duyệt từng số tốn số phép kiểm bằng n, với mười mũ mười hai thì khoảng 17 phút, với mười mũ mười lăm thì hơn 11 ngày. "
        "Còn bao hàm loại trừ, với hai điều kiện là chia hết cho 2 và cho 3, chỉ là ba phép chia. Người làm nghề chọn đếm theo tập khi đề cho một khoảng rất lớn, và duyệt từng số chỉ để kiểm lại trên khoảng nhỏ.",
        focus=[1, ["1.4", "1.5"], 1, 2], clear=True),
], checks=[
    "[sum(1 for x in range(1, n + 1) if x % 2 == 0 or x % 3 == 0) for n in (100, 10 ** 6)] == [67, 666667]",
    "10 ** 12 // 2 + 10 ** 12 // 3 - 10 ** 12 // 6 == 666666666667",
    "round(10 ** 12 / 1e9 / 60) == 17 and round(10 ** 15 / 1e9 / 86400, 1) == 11.6",
])

DE = """# Lab DMS L05 — Phép toán tập hợp và bao hàm–loại trừ bằng chương trình

Viết `taphop.py` (Python 3.11 trở lên); chạy: `python taphop.py`.

Cho `A = {2, 3, 5, 7, 11, 13}` và `B = {1, 3, 5, 7, 9, 11}` (kiểu `set` của Python). In đúng sáu dòng, các phần tử của một tập in theo thứ tự tăng dần, cách nhau một dấu cách:
1. `hop: ...` (hợp A và B)
2. `giao: ...`
3. `A bo B: ...` (phần tử thuộc A mà không thuộc B)
4. `B bo A: ...`
5. `so tap con cua A: <số>` (số phần tử của tập lũy thừa của A)
6. `chia het cho 4 hoac 6, tu 1 den 1000: dem=<a> congthuc=<b>` với `a` là số đếm bằng cách duyệt từng số từ 1 đến 1000, `b` là kết quả của công thức bao hàm–loại trừ (số chia hết cho 4, cộng số chia hết cho 6, trừ số chia hết cho bội chung nhỏ nhất của 4 và 6, tức số nhỏ nhất chia hết cho cả hai, là 12).

Gợi ý: `A | B`, `A & B`, `A - B`; `sorted(...)`; `' '.join(str(x) for x in ...)`; `2 ** len(A)`; `n // 4` là phần nguyên của n chia 4.

Chấm: `bash labs/cham.sh DMS L05 taphop.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""A = {2, 3, 5, 7, 11, 13}
B = {1, 3, 5, 7, 9, 11}

def in_ra(ten, s):
    print(ten + ':', ' '.join(str(x) for x in sorted(s)))

in_ra('hop', A | B)
in_ra('giao', A & B)
in_ra('A bo B', A - B)
in_ra('B bo A', B - A)
print('so tap con cua A:', 2 ** len(A))
dem = 0
for x in range(1, 1001):
    if x % 4 == 0 or x % 6 == 0:
        dem = dem + 1
n = 1000
print('chia het cho 4 hoac 6, tu 1 den 1000: dem=' + str(dem), 'congthuc=' + str(n // 4 + n // 6 - n // 12))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> Python có sẵn <code>A | B</code> (hợp), <code>A &amp; B</code> (giao), <code>A - B</code> (hiệu). Số tập con là $2^{|A|}$. '
            "Số chia hết cho 4 và 6 cùng lúc là số chia hết cho bội chung nhỏ nhất của chúng, tức 12 (chứ không phải 24), nên công thức là <code>n // 4 + n // 6 - n // 12</code>. "
            "Lời giải ở <code>labs/DMS/L05/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, ngôn ngữ lập trình có sẵn các phép hợp, giao và hiệu cho tập. Số tập con là hai mũ số phần tử. "
            "Số chia hết cho cả 4 và 6 là số chia hết cho bội chung nhỏ nhất của chúng, là 12 chứ không phải 24. Nên công thức là n chia 4, cộng n chia 6, trừ n chia 12, mỗi phép lấy phần nguyên. "
            "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("A | B, A & B, A - B", "hợp, giao, hiệu của hai tập", "{1, 2} | {2, 3} là {1, 2, 3}; {1, 2} & {2, 3} là {2}; {1, 2} - {2, 3} là {1}"),
    ("n // 4 + n // 6 - n // 12", "<code>//</code> là chia lấy phần nguyên, bỏ phần lẻ", "n = 24: 6 + 4 - 2 = 8 số chia hết cho 4 hoặc 6"),
], [
    "Dấu gạch đứng, dấu và, dấu trừ nối hai tập lần lượt cho hợp, giao và hiệu.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, nên cả công thức cho số bội của 4 hoặc 6 mà không cần duyệt.",
])

prac = practice(
    LID, "Tự làm: hợp, giao, hiệu và đếm bằng bao hàm–loại trừ",
    "<p><b>Đề</b>: với $A = \\{2, 3, 5, 7, 11, 13\\}$ và $B = \\{1, 3, 5, 7, 9, 11\\}$, viết <code>taphop.py</code> in hợp, giao, hai hiệu, số tập con của $A$, "
    "và số từ 1 đến 1 000 chia hết cho 4 hoặc 6 (đếm bằng vòng lặp và bằng bao hàm–loại trừ). Sáu dòng, định dạng ở <code>labs/DMS/L05/de.md</code>.</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Để ý: bội chung nhỏ nhất của 4 và 6, tức số nhỏ nhất chia hết cho cả hai, là 12, không phải 24.</p>',
    "Bây giờ tới phần bạn tự làm. Với hai tập cho sẵn, hãy viết chương trình in hợp, giao và hai hiệu của chúng, rồi số tập con của tập đầu. "
    "Sau đó đếm các số từ một đến một nghìn chia hết cho 4 hoặc 6, bằng vòng lặp và bằng bao hàm loại trừ. Định dạng sáu dòng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "taphop.py", H_HTML, H_SAY,
    pause=240, focus1=[1, 1, 1, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "taphop.py")

OBJ = [
    "Thực hiện hợp, giao, hiệu hai tập",
    "Liệt kê và đếm tập lũy thừa",
    "Đếm bằng bao hàm–loại trừ hai tập",
    "Đếm số phép tính của cách duyệt từng phần tử so với bao hàm–loại trừ khi khoảng cần đếm lớn dần",
    "Viết chương trình in hợp, giao, hiệu của hai tập và đếm bằng bao hàm–loại trừ",
]
repl = [
    ('vì 2 và 3 không có ước chung lớn hơn 1', 'vì hai số 2 và 3 không có ước chung nào lớn hơn 1'),
    ("Hôm nay ta học ngôn ngữ tập hợp để đếm như vậy cho chắc.", "Hôm nay ta học ngôn ngữ tập hợp, tức cách nói về một nhóm phần tử, để đếm như vậy cho chắc."),
    ('        say: "Không, 7 bạn có tên', '        introduces: [dms_taphop]\n        say: "Không, 7 bạn có tên'),
    ("Từ 1 đến 100 có bao nhiêu bội của 2? Chia 100 cho 2", "Từ 1 đến 100 có bao nhiêu bội của 2, tức số chia hết cho 2? Chia 100 cho 2"),
    # fix4 (R2 SHOULD, khung 00033): lời và chữ nói "vùng đỏ" nhưng phần giao không tô đỏ → tô đỏ nhạt đúng phần giao của hai vòng tròn
    ('<circle cx="580" cy="180" r="150" fill="#15803d" fill-opacity="0.15" stroke="#15803d" stroke-width="4"/>',
     '<circle cx="580" cy="180" r="150" fill="#15803d" fill-opacity="0.15" stroke="#15803d" stroke-width="4"/>'
     '<path d="M480,68.2 A150,150 0 0 0 480,291.8 A150,150 0 0 0 480,68.2 Z" fill="#b91c1c" fill-opacity="0.35" stroke="none"/>'),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "ops"), (2, "powerset"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl,
                assumes_add=("dms_menhde", "dms_bct", "dms_dinhly"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Với n = 100 cả hai cách cho 67; n = một triệu cho 666 667; n = mười mũ mười hai chỉ công thức, cho 666 666 666 667"}))
