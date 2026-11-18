"""DMS L06 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l06.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L06"

C1 = r"""m = 1000
for n in (1000, 10000, 100000):
    dem = [0] * m
    for k in range(n):
        o = (k * 2654435761) % 2 ** 32 % m
        dem[o] = dem[o] + 1
    print(n, 'khoa: toi thieu', (n + m - 1) // m, ', thuc te', max(dem), ', o trong', dem.count(0))"""
O1 = run_py(C1)
print(O1)

TABA = read_step([
    ("m = 1000", "một dấu bằng là <b>gán</b>: đặt số ô của bảng là 1000", "m là 1000 thì bảng có 1000 ô"),
    ("for n in (1000, 10000, 100000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 1000, rồi 10000, rồi 100000"),
    ("dem = [0] * m", "danh sách m số 0 (dấu <code>*</code> sau danh sách là lặp lại): ô nào cũng đang chứa 0 khoá", "[0] * 3 là [0, 0, 0]"),
    ("for k in range(n):", "k chạy qua các số từ 0 tới n − 1: mỗi k là một khoá, đúng n khoá", "range(3) cho 0, 1, 2"),
], "Ta đọc chương trình này hai đợt, đợt một là bốn dòng đầu.", [
    "Dòng đầu gán m bằng 1000, tức bảng có một nghìn ô.",
    "Vòng lặp ngoài cho n lần lượt là một nghìn, mười nghìn, rồi một trăm nghìn khoá.",
    "Dấu sao đặt sau một danh sách là lặp lại nó: danh sách một số 0 lặp m lần là m số 0, nên ô nào cũng đang chứa không khoá.",
    "Vòng lặp trong cho k chạy từ 0 tới n trừ 1, mỗi k là một khoá, nên có đúng n khoá.",
])
TABB = read_steps([
    ("k * 2654435761", "nhân khoá k với một hằng số lớn chọn sẵn, để rải các khoá đều trên các ô", "k = 2 thì 2 * 2654435761 = 5308871522"),
    ("% 2 ** 32", "lấy dư cho 2<sup>32</sup> (<code>**</code> là lũy thừa, nên <code>2 ** 32</code> là 2 mũ 32): kết quả nằm trong khoảng 0 đến 2<sup>32</sup> − 1, vừa một số nguyên <b>32 bit</b> (<b>nhị phân</b> = viết bằng hai chữ số 0 và 1; 32 chữ số nhị phân cho 2<sup>32</sup>, hơn 4 tỉ giá trị)", "5308871522 % 2 ** 32 = 1013904226"),
    ("% m", "lấy dư cho số ô: ra số thứ tự ô <code>o</code>, từ 0 tới m − 1", "1013904226 % 1000 = 226"),
    ("dem[o] = dem[o] + 1", "<code>dem[o]</code> là ô số o của danh sách (đếm từ 0); dòng này tăng số khoá trong ô o thêm 1", "dem = [0, 4], o = 1 thì dem thành [0, 5]"),
    ("(n + m - 1) // m", "<code>//</code> là chia lấy phần nguyên; cộng thêm m − 1 trước thì thành chia <b>làm tròn lên</b>", "(10 + 3 - 1) // 3 là 4"),
    ("max(dem), dem.count(0)", "<code>max</code> là số lớn nhất của danh sách (ô đông nhất); <code>.count(0)</code> đếm các phần tử bằng 0 (ô trống)", "max([2, 0, 1]) là 2; [2, 0, 1, 0].count(0) là 2"),
], "Đợt hai là các dòng tính ô rồi in kết quả.", [
    "Phép nhân khoá k với một hằng số lớn giúp rải các khoá đều trên các ô.",
    "Lấy dư cho hai mũ 32 giữ kết quả trong số nguyên 32 bit, tức số viết bằng 32 chữ số nhị phân 0 hoặc 1, nên có hơn bốn tỉ giá trị.",
    "Lấy dư tiếp cho số ô, ta được số thứ tự ô, từ 0 tới m trừ 1.",
    "Dấu ngoặc vuông chỉ ô số o của danh sách, đếm từ 0, nên dòng này tăng số khoá trong ô đó thêm một.",
    "Phép chia lấy phần nguyên, sau khi cộng thêm m trừ 1, thành phép chia làm tròn lên.",
    "Hàm lớn nhất cho số khoá của ô đông nhất, còn phép đếm bằng 0 cho số ô trống.",
], split=3)
# fix13: thêm hàng print vào bảng đợt hai (chỉ đổi show; không có câu lời đọc mới)
TABB[1]["show"] = TABB[1]["show"].replace("</table>", "<tr><td>" + C("print(n, 'khoa: toi thieu', …)") + "</td><td>in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách</td><td>print(7, 'khoa') in ra 7 khoa</td></tr></table>", 1)

quymo = scene("quymo", "example", "Khi khoá nhiều lên: va chạm trong bảng băm là tất yếu", [
    TABA,
    *TABB,
    step(
        "<p><b>Chạy thật</b>: bỏ $n$ khoá vào bảng 1 000 ô bằng một hàm băm cố định</p>" + run_html(C1, O1, "Kết quả chạy thật")
,
        "Đây là chương trình chạy thật. Bảng có 1 000 ô, mỗi khoá, tức mã định danh của dữ liệu, được một công thức cố định đưa vào một ô, và danh sách đếm số khoá mỗi ô. "
        "Phép chia làm tròn lên số khoá cho số ô chính là cận dưới mà nguyên lý chuồng bồ câu bảo đảm. "
        "Với 1 000 khoá, nguyên lý chưa bảo đảm gì, và thực tế vẫn có ô chứa 2 khoá, cùng 271 ô trống. Ô chứa hai khoá trở lên là có va chạm, tức hai khoá khác nhau rơi vào cùng một ô. "
        "Với 10 000 khoá, nguyên lý bảo đảm có ô chứa ít nhất 10 khoá, thực tế là 11. Với 100 000 khoá, bảo đảm 100, thực tế 102.",
        focus=[2, ["2.2", "2.6"], "2.7", "4.1", "4.1", "4.2", "4.3"], clear=True),
    step(
        '<table class="t"><tr><th>số khoá $n$ (bảng 1 000 ô)</th><th>chuồng bồ câu bảo đảm</th><th>thực tế</th><th>ý nghĩa khi tìm một khoá</th></tr>'
        "<tr><td>1 000</td><td>chưa bảo đảm gì</td><td>ô đông nhất: 2 khoá</td><td>tìm gần như tức thì</td></tr>"
        "<tr><td>10 000</td><td>có ô từ 10 khoá</td><td>11 khoá</td><td>phải so khoảng chục khoá</td></tr>"
        "<tr><td>100 000</td><td>có ô từ 100 khoá</td><td>102 khoá</td><td>phải so khoảng một trăm khoá</td></tr></table>"
        '<div class="box key">Khoá gấp 100 lần thì ô đông nhất đông gấp khoảng 50 lần: <b>va chạm không thể tránh</b>, chỉ có thể <b>chia đều</b>. Người làm nghề phải chọn: tăng số ô khi bảng đầy (tốn bộ nhớ) hay chấp nhận tìm chậm hơn.</div>',
        "Bảng này gom lại. Khi khoá nhiều gấp một trăm lần, ô đông nhất đông gấp khoảng năm mươi lần, và đúng như nguyên lý nói, va chạm không thể tránh, chỉ có thể chia đều. "
        ""
        "Người làm nghề phải chọn, tăng số ô khi bảng đầy, tốn thêm bộ nhớ, hay chấp nhận tìm chậm hơn.",
        focus=[1, "1.4", 2], clear=True),
], checks=[
    "[max(__import__('collections').Counter((k * 2654435761) % 2 ** 32 % 1000 for k in range(n)).values()) for n in (1000, 10000, 100000)] == [2, 11, 102]",
    "1000 - len({(k * 2654435761) % 2 ** 32 % 1000 for k in range(1000)}) == 271",
    "[(n + 1000 - 1) // 1000 for n in (1000, 10000, 100000)] == [1, 10, 100]",
    "round(102 / 2) == 51",
])

DE = """# Lab DMS L06 — Phân loại hàm trên tập hữu hạn và kiểm chuồng bồ câu bằng máy

Viết `ham.py` (Python 3.11 trở lên); chạy: `python ham.py`.

Phần 1. Năm hàm, mỗi hàm là một từ điển `{phần tử của A: ảnh}` (chép nguyên vào đầu tệp), cùng tập đích B:

```python
HAM = [
    ('f1', {1: 'a', 2: 'b', 3: 'a', 4: 'c'}, {'a', 'b', 'c'}),
    ('f2', {1: 'a', 2: 'c', 3: 'd'}, {'a', 'b', 'c', 'd'}),
    ('f3', {1: 'x', 2: 'z', 3: 'y'}, {'x', 'y', 'z'}),
    ('f4', {1: 'p', 2: 'q', 3: 'p', 4: 'p', 5: 'q'}, {'p', 'q'}),
    ('f5', {1: 'a', 2: 'a', 3: 'b'}, {'a', 'b', 'c'}),
]
```

Với mỗi hàm in một dòng:
- `<tên>: song anh` nếu vừa đơn ánh vừa toàn ánh;
- nếu không: `<tên>: <đơn ánh hay không>, <toàn ánh hay không>` viết đúng `don anh` hoặc `khong don anh`, rồi `toan anh` hoặc `khong toan anh` (theo thứ tự đó: đơn ánh trước, toàn ánh sau). Ví dụ: `f9: khong don anh, toan anh`.

(Đơn ánh: hai phần tử khác nhau luôn có ảnh khác nhau. Toàn ánh: mọi phần tử của B đều là ảnh của ít nhất một phần tử của A.)

Phần 2. Chọn k số khác nhau từ 1 đến 12. Có hai số tổng bằng 13 không? Với k = 7 rồi k = 6, liệt kê MỌI cách chọn và in:
`chon <k> so tu 1 den 12: <tổng số cách chọn> cach, <số cách có hai số tổng 13> cach co cap tong 13`

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import combinations` ở đầu tệp: mượn một hàm có sẵn của Python. `combinations(range(1, 13), 3)` lần lượt cho mọi cách chọn 3 số khác nhau từ 1 đến 12, không kể thứ tự; mỗi cách là một bộ số như `(1, 2, 3)`, `(1, 2, 4)`, ... Vòng lặp: `for chon in combinations(range(1, 13), k):`.
- `f.values()` là các ảnh của hàm `f` (các giá trị của từ điển); `set(...)` bỏ các giá trị trùng; `len(...)` đếm. Số ảnh khác nhau bằng số phần tử của A nghĩa là hai phần tử khác nhau luôn có ảnh khác nhau.

Chấm: `bash labs/cham.sh DMS L06 ham.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import combinations

HAM = [
    ('f1', {1: 'a', 2: 'b', 3: 'a', 4: 'c'}, {'a', 'b', 'c'}),
    ('f2', {1: 'a', 2: 'c', 3: 'd'}, {'a', 'b', 'c', 'd'}),
    ('f3', {1: 'x', 2: 'z', 3: 'y'}, {'x', 'y', 'z'}),
    ('f4', {1: 'p', 2: 'q', 3: 'p', 4: 'p', 5: 'q'}, {'p', 'q'}),
    ('f5', {1: 'a', 2: 'a', 3: 'b'}, {'a', 'b', 'c'}),
]

for ten, f, B in HAM:
    don = len(set(f.values())) == len(f)
    toan = set(f.values()) == B
    if don and toan:
        print(ten + ': song anh')
    else:
        print(ten + ': ' + ('don anh' if don else 'khong don anh') + ', ' + ('toan anh' if toan else 'khong toan anh'))

for k in (7, 6):
    tong = 0
    co_cap = 0
    for chon in combinations(range(1, 13), k):
        tong = tong + 1
        if any(a + b == 13 for a in chon for b in chon):
            co_cap = co_cap + 1
    print('chon', k, 'so tu 1 den 12:', tong, 'cach,', co_cap, 'cach co cap tong 13')"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> đơn ánh khi số ảnh khác nhau bằng số phần tử của A: <code>len(set(f.values())) == len(f)</code>. Toàn ánh khi tập ảnh bằng B: <code>set(f.values()) == B</code>. '
    "Các cặp bù của 13 là 1–12, 2–11, …, 6–7: 6 chuồng, nên 7 số chắc có cặp, còn 6 số thì chọn mỗi cặp một số là né được. "
    "Liệt kê mọi cách chọn bằng <code>combinations</code> mượn từ <code>itertools</code> (đọc ở bảng ngay sau). "
    "Lời giải ở <code>labs/DMS/L06/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, hàm là đơn ánh khi số giá trị khác nhau bằng số phần tử của tập nguồn, và là toàn ánh khi tập giá trị bằng đúng tập đích. "
    "Các cặp có tổng mười ba là sáu chuồng, nên bảy số chắc chắn có cặp, còn sáu số thì chọn mỗi cặp một số là né được. "
    "Để liệt kê mọi cách chọn, hãy mượn một hàm có sẵn ở đầu tệp, cách dùng đọc ở bảng ngay sau. "
    "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("f.values()", "các giá trị (ảnh) của từ điển f; từ điển viết <code>{khoá: giá_trị}</code>, đọc ở bảng ngay sau", "{1: 'a', 2: 'b'}.values() cho 'a', 'b'"),
    ("set(...)", "bỏ các giá trị trùng nhau", "set(['a', 'a', 'b']) là {'a', 'b'}"),
    ("len(...)", "đếm số phần tử", "len({'a', 'b'}) là 2"),
], [
    "Hàm giá trị của từ điển cho mọi ảnh của hàm f, tên ghi trên màn hình.",
    "Hàm tập hợp bỏ các giá trị trùng nhau, nên chỉ còn các ảnh khác nhau.",
    "Hàm đếm cho số phần tử, nên đem so với số phần tử của tập nguồn là biết đơn ánh hay không.",
])

prac = practice(
    LID, "Tự làm: phân loại năm hàm và kiểm chuồng bồ câu trên mọi cách chọn",
    "<p><b>Đề</b>: viết <code>ham.py</code> phân loại năm hàm cho sẵn là đơn ánh, toàn ánh hay song ánh, "
    "rồi liệt kê MỌI cách chọn 7 số, và 6 số, từ 1 đến 12 để đếm bao nhiêu cách có hai số tổng 13 (năm hàm và định dạng ở <code>labs/DMS/L06/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dự đoán trước: chọn 7 số thì cách nào cũng có cặp tổng 13 không? Chọn 6 số thì sao?</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình phân loại năm hàm cho sẵn là đơn ánh, toàn ánh hay song ánh. "
    "Sau đó liệt kê mọi cách chọn bảy số, rồi sáu số, từ một đến mười hai, và đếm bao nhiêu cách có hai số tổng bằng mười ba. "
    "Hãy dự đoán trước kết quả bằng nguyên lý chuồng bồ câu, rồi để máy kiểm. Năm hàm và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "ham.py",
    H_HTML, H_SAY,
    pause=300, focus1=[1, 1, 1, 2, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "ham.py")
add_read_step(prac, [
    ("{1: 'a', 2: 'b'}", "<b>từ điển</b>: mỗi khoá đi với một giá trị; ở đây hàm f gửi 1 tới 'a' và 2 tới 'b'", "f = {1: 'a', 2: 'b'} thì f[1] là 'a'"),
    ("from itertools import combinations", "mượn hàm làm sẵn <code>combinations</code> ở đầu tệp: liệt kê mọi cách chọn k phần tử, không kể thứ tự", "combinations([1, 2, 3], 2) cho (1, 2), (1, 3), (2, 3)"),
    ("for chon in combinations(range(1, 13), k):", "<code>chon</code> chạy qua mọi cách chọn k số khác nhau từ 1 tới 12", "k = 7 có 792 cách chọn"),
], "Ba chỗ cú pháp còn lại của lời giải đọc như sau.", [
    "Các cặp khoá và giá trị trong ngoặc nhọn là một từ điển, tức một hàm: mỗi phần tử nguồn đi với đúng một ảnh.",
    "Dòng đầu mượn một hàm làm sẵn để liệt kê mọi cách chọn k phần tử, không kể thứ tự, tên hàm ghi trên màn hình.",
    "Vòng lặp cho chọn chạy qua mọi cách chọn k số khác nhau từ 1 tới 12, mỗi cách là một bộ số.",
])

OBJ = [
    "Phân loại một hàm là đơn ánh, toàn ánh, song ánh",
    "Phát biểu và chứng minh nguyên lý chuồng bồ câu",
    "Dùng chuồng bồ câu để chứng minh va chạm tất yếu",
    "Đếm khoá trong từng ô của bảng băm khi số khoá lớn dần, và so với cận dưới mà chuồng bồ câu bảo đảm",
    "Viết chương trình phân loại hàm trên tập hữu hạn và kiểm chuồng bồ câu bằng cách liệt kê mọi cách chọn",
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "kinds"), (2, "pigeonhole"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                repl=[(" Hẹn gặp bạn ở bài tiếp theo.", ""),
                      ("không bỏ sót phần tử nào của B, hai điều kiện này độc lập nhau", "không bỏ sót phần tử nào của B, hai điều kiện độc lập"),
                      ('Một bảng băm, tức một dãy ô mà máy tính dùng quy tắc gọi là hàm băm để chỉ mỗi khoá tới một ô, có 10 ô', 'Một bảng băm, tức một dãy ô, dùng hàm băm để chỉ mỗi khoá, tức mã định danh của dữ liệu cần cất, tới một ô, có 10 ô')],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop", "dms_tuongduong"))
print(f)
print(ledger_sync(LID, claims={"quymo": "1 000 khoá: ô đông nhất 2 khoá, 271 ô trống; 10 000 khoá: bảo đảm 10, thực tế 11; 100 000 khoá: bảo đảm 100, thực tế 102"}))
