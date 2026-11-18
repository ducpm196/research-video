"""DMS L07 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l07.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L07"

C1 = r"""for n in (9, 30, 100):
    dem = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if a % 3 == b % 3 and b % 3 == c % 3 and a % 3 != c % 3:
                    dem = dem + 1
    print(n, 'so:', n * n * n, 'bo ba da kiem, vi pham bac cau:', dem)"""
O1 = run_py(C1)
C2 = r"""for n in (9, 30, 100):
    lop = [0, 0, 0]
    for x in range(n):
        lop[x % 3] = lop[x % 3] + 1
    print(n, 'so: chia', n, 'lan thanh', len(lop), 'lop, moi lop co', sorted(lop))"""
O2 = run_py(C2)
print(O1, O2, sep="\n")

TAB1 = read_steps([
    ("for n in (9, 30, 100):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 9, rồi 30, rồi 100"),
    ("range(n)", "các số từ 0 tới n − 1, đúng n giá trị", "range(4) cho 0, 1, 2, 3"),
    ("if điều_kiện:", "<b>nếu</b> điều kiện đúng thì chạy các dòng thụt vào bên dưới, sai thì bỏ qua", "if 7 > 5: chạy; if 3 > 5: bỏ qua"),
    ("a % 3 == b % 3", "<code>%</code> là chia lấy <b>số dư</b>; <code>==</code> là so sánh bằng: a và b có cùng số dư khi chia cho 3", "7 % 3 == 4 % 3 là 1 == 1, đúng"),
    ("... and ...  a % 3 != c % 3", "<code>and</code> là và: đúng khi cả hai đúng; <code>!=</code> là khác", "đúng and sai là sai; 1 != 2 là đúng"),
    ("dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng dem thêm 1", "dem đang là 0 thì thành 1"),
    ("print(n, n * n * n)", "in các giá trị ra cửa sổ, cách nhau một dấu cách; <code>*</code> là nhân, nên <code>n * n * n</code> là n lập phương", "n = 9: 9 * 9 * 9 = 729"),
], "Ta kiểm bắc cầu bằng cách thử hết mọi bộ ba, gọi là vét cạn, với chương trình dùng bảy ký hiệu sau.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 9, 30, rồi 100, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số cho các số từ 0 tới n trừ 1, nên có đúng n giá trị.",
    "Chữ nếu kèm điều kiện nghĩa là: nếu điều kiện đúng thì chạy các dòng thụt vào bên dưới, còn sai thì bỏ qua.",
    "Dấu phần trăm là chia lấy số dư, hai dấu bằng liền nhau là so sánh bằng, nên dòng này hỏi a và b có cùng số dư khi chia cho 3 không.",
    "Chữ giữa các điều kiện là và, nên cả ba điều kiện phải cùng đúng, còn dấu chấm than kèm bằng là khác.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hàm in đưa các giá trị ra cửa sổ, còn n sao n sao n là n nhân n nhân n, tức n lập phương.",
], split=4, note='<p class="note"><b>Vét cạn</b> = thử hết mọi trường hợp.</p>')
TAB2 = read_step([
    ("lop = [0, 0, 0]", "danh sách ba ô đếm, mỗi ô là một lớp: dư 0, dư 1, dư 2", "[0, 0, 0] nghĩa là chưa có số nào"),
    ("lop[x % 3] = lop[x % 3] + 1", "<code>lop[i]</code> là ô thứ i của danh sách (đếm từ 0); dòng này tăng ô của lớp chứa x thêm 1", "x = 4: 4 % 3 = 1, ô số 1 tăng thêm 1"),
    ("len(lop)", "đếm số phần tử của danh sách, tức số lớp", "len([3, 3, 3]) là 3"),
    ("sorted(lop)", "xếp các phần tử theo thứ tự tăng dần", "sorted([34, 33, 33]) là [33, 33, 34]"),
], "Cách gom lớp dùng danh sách ba ô đếm, với bốn ký hiệu sau.", [
    "Danh sách ba số 0 là ba ô đếm, mỗi ô ứng với một lớp, dư 0, dư 1 và dư 2.",
    "Dấu ngoặc vuông chỉ ô thứ i của danh sách, đếm từ 0, nên dòng này tăng thêm một ở ô của lớp chứa x.",
    "Hàm đếm cho số phần tử của danh sách, tức số lớp.",
    "Hàm xếp cho các phần tử theo thứ tự tăng dần, để dễ so sánh.",
])

quymo = scene("quymo", "example", "Khi tập lớn dần: kiểm bắc cầu vét cạn tốn n³, gom lớp chỉ tốn n", [
    *TAB1,
    step(
        "<p><b>Chạy thật</b>: kiểm tính bắc cầu của “cùng số dư khi chia cho 3” bằng cách thử mọi bộ ba $(a, b, c)$ trong $0, \\dots, n-1$</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Ba vòng lặp thử mọi bộ ba a, b, c, và đếm các bộ ba có a quan hệ b, b quan hệ c, mà a không quan hệ c. "
        "Với 9 số, máy kiểm 729 bộ ba. Với 30 số là 27 nghìn bộ ba. Với 100 số là một triệu bộ ba. Cả ba lần đều không có bộ ba vi phạm, nên tính bắc cầu đúng.",
        focus=[2, ["2.4", "2.6"], "4.1", "4.2", "4.3", 4][:6], clear=True),
    TAB2,
    step(
        "<p>Cách gom lớp: mỗi số chỉ cần chia lấy dư một lần rồi bỏ vào đúng nhóm</p>" + run_html(C2, O2, "Kết quả chạy thật"),
        "Cách khác, vì đây là quan hệ tương đương, ta không cần kiểm bắc cầu từng bộ ba mà chỉ gom lớp. Mỗi số chia lấy dư một lần rồi bỏ vào đúng nhóm. "
        "Với 100 số chỉ cần 100 lần chia, và ra ngay ba lớp có 33, 33 và 34 số.",
        focus=[2, 2, 4], clear=True),
    step(
        '<table class="t"><tr><th>$n$ số</th><th>kiểm mọi bộ ba</th><th>gom lớp theo số dư</th></tr>'
        "<tr><td>9</td><td>729 bộ ba</td><td>9 lần chia</td></tr>"
        "<tr><td>100</td><td>1 000 000 bộ ba</td><td>100 lần chia</td></tr>"
        "<tr><td>1 000</td><td>$10^9$ bộ ba, khoảng 1 giây ở một tỉ phép mỗi giây (số minh hoạ)</td><td>1 000 lần chia</td></tr>"
        "<tr><td>$10^5$</td><td>$10^{15}$ bộ ba, khoảng 11,6 ngày</td><td>$10^5$ lần chia</td></tr></table>"
        '<div class="box key">Số bộ ba tăng <b>lập phương</b> theo n. Biết quan hệ là tương đương (kiểm chứng một lần bằng chứng minh) thì gom lớp chỉ tốn <b>tỉ lệ với n</b>.</div>',
        "Bảng này cho thấy số bộ ba tăng theo lập phương của n. Với một nghìn số thì khoảng một giây, còn với một trăm nghìn số thì hơn 11 ngày, trong khi gom lớp chỉ cần một trăm nghìn lần chia. "
        "Người làm nghề chứng minh một lần rằng quan hệ là tương đương, rồi dùng cách gom lớp thay cho việc vét cạn mọi bộ ba.",
        focus=[1, "1.4", 2], clear=True),
], checks=[
    "[n ** 3 for n in (9, 30, 100)] == [729, 27000, 1000000]",
    "sum(1 for a in range(30) for b in range(30) for c in range(30) if a % 3 == b % 3 == c % 3 and a % 3 != c % 3) == 0",
    "sorted([x % 3 for x in range(100)].count(r) for r in range(3)) == [33, 33, 34]",
    "round((10 ** 5) ** 3 / 1e9 / 86400, 1) == 11.6 and 1000 ** 3 / 1e9 == 1.0",
])

DE = """# Lab DMS L07 — Kiểm ba tính chất của quan hệ và tìm lớp tương đương bằng chương trình

Viết `quanhe.py` (Python 3.11 trở lên); chạy: `python quanhe.py`.

Tập `A = {1, 2, 3, 4, 5, 6}`. Bốn quan hệ, mỗi quan hệ là một hàm `R(a, b)` trả đúng khi `a` có quan hệ với `b` (chép nguyên vào đầu tệp):

```python
A = [1, 2, 3, 4, 5, 6]
QH = [
    ('R1', lambda a, b: (a - b) % 4 == 0),
    ('R2', lambda a, b: b % a == 0),
    ('R3', lambda a, b: abs(a - b) <= 1),
    ('R4', lambda a, b: (a + b) % 2 == 0),
]
```

Với mỗi quan hệ, kiểm bốn tính chất trên MỌI phần tử, mọi cặp, mọi bộ ba của A (viết 1 nếu đúng, 0 nếu sai):
- `PX`: phản xạ (mọi a: a R a);
- `DX`: đối xứng (mọi a, b: a R b thì b R a);
- `PDX`: phản đối xứng (mọi a, b: a R b và b R a thì a bằng b);
- `BC`: bắc cầu (mọi a, b, c: a R b và b R c thì a R c).

In một dòng `<tên>: PX=<0|1> DX=<0|1> PDX=<0|1> BC=<0|1>`. Nếu quan hệ là tương đương (PX, DX, BC cùng bằng 1), in thêm vào cuối dòng `, tuong duong, cac lop: ` rồi các lớp tương đương, mỗi lớp là một danh sách tăng dần in bằng `print(sorted(lop))`, các lớp xếp theo phần tử nhỏ nhất, cách nhau một dấu cách.

Ví dụ định dạng: `R9: PX=1 DX=1 PDX=0 BC=1, tuong duong, cac lop: [1, 2] [3]`.

Chấm: `bash labs/cham.sh DMS L07 quanhe.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""A = [1, 2, 3, 4, 5, 6]
QH = [
    ('R1', lambda a, b: (a - b) % 4 == 0),
    ('R2', lambda a, b: b % a == 0),
    ('R3', lambda a, b: abs(a - b) <= 1),
    ('R4', lambda a, b: (a + b) % 2 == 0),
]

for ten, R in QH:
    px = all(R(a, a) for a in A)
    dx = all(R(b, a) for a in A for b in A if R(a, b))
    pdx = all(a == b for a in A for b in A if R(a, b) and R(b, a))
    bc = all(R(a, c) for a in A for b in A for c in A if R(a, b) and R(b, c))
    dong = ten + ': PX=' + str(int(px)) + ' DX=' + str(int(dx)) + ' PDX=' + str(int(pdx)) + ' BC=' + str(int(bc))
    if px and dx and bc:
        lop = []
        for a in A:
            nhom = [b for b in A if R(a, b)]
            if nhom not in lop:
                lop.append(nhom)
        dong = dong + ', tuong duong, cac lop: ' + ' '.join(str(sorted(l)) for l in lop)
    print(dong)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> mỗi tính chất là một câu “với mọi”, nên viết bằng <code>all(...)</code> trên mọi a, b, c của A. '
    "Ví dụ bắc cầu: <code>all(R(a, c) for a in A for b in A for c in A if R(a, b) and R(b, c))</code>. "
    "Lớp của a là <code>[b for b in A if R(a, b)]</code>; hai phần tử cùng lớp cho cùng danh sách, nên chỉ thêm danh sách chưa có. "
    "Lời giải ở <code>labs/DMS/L07/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, mỗi tính chất là một câu với mọi, nên viết bằng hàm kiểm mọi trường hợp, trên mọi phần tử, mọi cặp, mọi bộ ba của tập. "
    "Lớp của một phần tử là danh sách các phần tử có quan hệ với nó, và hai phần tử cùng lớp cho cùng danh sách, nên chỉ thêm danh sách chưa có. "
    "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("all(biểu_thức for a in A for b in A ...)", "<b>với mọi</b>: đúng khi biểu thức đúng với mọi a, b trong A (mỗi <code>for</code> là một biến chạy qua A)", "all(a < 4 for a in [1, 2, 3]) là True"),
    ("... if R(a, b) and R(b, c)", "chỉ xét các bộ mà điều kiện sau chữ <code>if</code> đúng: a R b <b>và</b> b R c", "bộ nào không có a R b thì bỏ qua"),
    ("[b for b in A if R(a, b)]", "danh sách các b của A thoả a R b: chính là <b>lớp</b> của a", "A = [1, 2, 3, 4], R là cùng chẵn lẻ, a = 1: cho [1, 3]"),
], [
    "Hàm kiểm mọi đúng khi biểu thức đúng với mọi a, b, c chạy qua tập, mỗi chữ lặp là một biến chạy qua tập đó.",
    "Chữ điều kiện ở cuối chỉ giữ lại những bộ mà a có quan hệ với b, và b có quan hệ với c.",
    "Dòng cuối dựng danh sách các b có quan hệ với a, đó chính là lớp của a.",
])

prac = practice(
    LID, "Tự làm: máy kiểm bốn tính chất của bốn quan hệ trên {1, …, 6}",
    "<p><b>Đề</b>: viết <code>quanhe.py</code> kiểm phản xạ, đối xứng, phản đối xứng, bắc cầu của bốn quan hệ cho sẵn trên $A = \\{1, \\dots, 6\\}$, "
    "và in các lớp tương đương của quan hệ nào là tương đương (bốn quan hệ và định dạng ở <code>labs/DMS/L07/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dự đoán trước quan hệ nào là tương đương, rồi để máy kiểm.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình kiểm bốn tính chất, phản xạ, đối xứng, phản đối xứng và bắc cầu, cho bốn quan hệ cho sẵn trên các số từ một đến sáu. "
    "Với quan hệ nào là tương đương, in thêm các lớp tương đương. Bốn quan hệ và định dạng nằm trong thư mục thực hành. Hãy dự đoán trước, rồi dừng video và tự làm.",
    EXP, "quanhe.py", H_HTML, H_SAY,
    pause=300, focus1=[1, 1, 1, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "quanhe.py")

OBJ = [
    "Kiểm ba tính chất phản xạ, đối xứng, bắc cầu của một quan hệ",
    "Nhận ra quan hệ tương đương",
    "Chia một tập thành các lớp tương đương",
    "Đếm số bộ ba phải kiểm khi vét cạn tính bắc cầu khi tập lớn dần, và so với cách gom lớp theo số dư",
    "Viết chương trình kiểm các tính chất của quan hệ trên tập hữu hạn và in các lớp tương đương",
]
repl = [
    # fix6 (R4 SHOULD): equivalence.1 thêm ý "phủ kín" (a thuộc lớp của a nhờ phản xạ); quiz.1 dấu "." lẻ
    ('<p class="note">Ý chính: nếu hai lớp có chung một phần tử $c$ thì nhờ đối xứng và bắc cầu, mọi phần tử của lớp này liên hệ được với lớp kia — hai lớp trùng nhau.</p>\n        focus: [1, 2, 2]\n',
     '<p class="note">Rời nhau: nếu hai lớp có chung một phần tử $c$ thì nhờ đối xứng và bắc cầu, mọi phần tử của lớp này liên hệ được với lớp kia — hai lớp trùng nhau.</p>\n          <p class="note">Phủ kín: mỗi $a$ thuộc lớp của chính nó, vì phản xạ cho $a\\,R\\,a$.</p>\n        focus: [1, 2, 2, 3]\n'),
    ("Vì vậy hai lớp phải trùng nhau.", "Vì vậy hai lớp phải trùng nhau. Còn phủ kín, vì mỗi a thuộc lớp của chính nó, nhờ phản xạ."),
    ("Hai lớp: $\\{1, 3, 5\\}$ và $\\{2, 4, 6\\}$.</p>", "Hai lớp: $\\{1, 3, 5\\}$ (các số lẻ) và $\\{2, 4, 6\\}$ (các số chẵn).</p>"),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "example"), (2, "equivalence"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl,
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop", "dms_tuongduong", "dms_phanvidu"))
print(f)
print(ledger_sync(LID, claims={"quymo": "9, 30, 100 số cần 729, 27 nghìn, một triệu bộ ba, không bộ ba vi phạm; với 100 số gom lớp chia 100 lần ra ba lớp 33, 33, 34"}))
