"""DMS L13 → AF2 (WP5 phiên 2). Chạy: .venv/Scripts/python -B audit/dms/af2/l13.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L13"

C1 = r"""for a, b in ((252, 198), (10 ** 6 + 3, 10 ** 6), (2880067194370816120, 1779979416004714189)):
    x, y, buoc = a, b, 0
    while y != 0:
        x, y, buoc = y, x % y, buoc + 1
    print(a, b, 'gcd', x, ':', buoc, 'buoc, thu moi uoc can', min(a, b), 'phep')"""
O1 = run_py(C1)
print(O1)

TAB_A = read_step([
    ("for a, b in ((252, 198), …):", "với mỗi cặp trong danh sách, gán số thứ nhất cho a và số thứ hai cho b, rồi làm các dòng thụt vào bên dưới", "lượt đầu: a = 252, b = 198"),
    ("10 ** 6 + 3", "<code>**</code> là lũy thừa: <code>10 ** 6</code> là mười mũ sáu, một triệu", "10 ** 6 + 3 = 1000003"),
    ("x, y, buoc = a, b, 0", "một dấu bằng là <b>gán</b>; gán nhiều giá trị cùng lúc: x nhận a, y nhận b, buoc nhận 0", "a = 252, b = 198: x = 252, y = 198, buoc = 0"),
    ("while y != 0:", "lặp lại các dòng thụt vào bên dưới chừng nào y còn khác 0 (<code>!=</code> là khác)", "y = 54 thì lặp tiếp; y = 0 thì dừng"),
], "Chương trình đếm bước của thuật toán chia lấy dư dùng bảy ký hiệu, ta đọc bốn cái đầu trước.", [
    "Dòng mở đầu vòng lặp: với mỗi cặp trong danh sách, gán số thứ nhất cho a và số thứ hai cho b, rồi làm các dòng thụt vào.",
    "Hai dấu sao liền nhau là lũy thừa, nên mười mũ sáu cộng 3 là một triệu lẻ ba.",
    "Một dấu bằng là gán, và có thể gán nhiều giá trị cùng lúc: x nhận a, y nhận b, còn biến đếm bước nhận 0.",
    "Vòng lặp này lặp lại các dòng thụt vào chừng nào y còn khác 0, vì dấu chấm than kèm bằng là khác.",
])

TAB_B = read_step([
    ("x, y, buoc = y, x % y, buoc + 1", "gán cùng lúc: tính xong cả ba giá trị bên phải rồi mới cất; <code>x % y</code> là số dư khi chia x cho y", "x = 252, y = 198: thành x = 198, y = 54, buoc = 1"),
    ("min(a, b)", "<code>min</code> cho số nhỏ hơn trong hai số", "min(252, 198) = 198"),
    ("print(a, b, 'gcd', x, ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>gcd</code> là ước chung lớn nhất", "in ra 252 198 gcd 18 …"),
], "Ba ký hiệu còn lại nằm trong thân vòng lặp và dòng in kết quả.", [
    "Dòng này gán cùng lúc: tính xong cả ba giá trị bên phải rồi mới cất, trong đó dấu phần trăm là chia lấy số dư.",
    "Hàm này cho số nhỏ hơn trong hai số, nên ở cặp đầu tiên là 198, đúng số phép của cách thử từng ước.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách, và chữ này là viết tắt của ước chung lớn nhất.",
])

quymo = scene("quymo", "example", "Khi số lớn dần: thử từng ước không kịp, thuật toán Euclid chỉ vài chục bước", [
    step(
        "<p><b>Chạy thật</b>: đếm số bước chia lấy dư của thuật toán Euclid ở ba cỡ số, so với thử từng ước</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Ở mỗi cặp số, vòng lặp thay số lớn bằng số bé và số bé bằng số dư, đếm số lần chia cho tới khi số dư bằng 0. "
        "Dòng gán ba giá trị cùng lúc cập nhật cả ba biến trong một lần. "
        "Cặp 252 và 198 mất 4 bước. Cặp quanh một triệu mất 3 bước. Cặp số rất lớn, cỡ mười chín chữ số, thuộc dãy mà thuật toán chạy chậm nhất, mất 88 bước.",
        focus=[2, "2.3", "2.4", "4.1", "4.2", "4.3"][:6], clear=True),
    step(
        '<table class="t"><tr><th>cặp số</th><th>thuật toán Euclid</th><th>thử mọi ước từ 1 đến số bé, một tỉ phép mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>252 và 198</td><td>4 bước</td><td>198 phép, chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>$10^6 + 3$ và $10^6$</td><td>3 bước</td><td>$10^6$ phép, khoảng một phần nghìn giây</td></tr>"
        "<tr><td>hai số cỡ $2 \\times 10^{18}$</td><td>88 bước</td><td>khoảng $1{,}8 \\times 10^{18}$ phép, khoảng 56 năm</td></tr></table>"
        '<div class="box key">Mỗi hai bước chia thì số bé nhất giảm <b>ít nhất một nửa</b>, nên số bước nhiều nhất tỉ lệ với <b>số chữ số</b>, không với giá trị. Thử mọi ước thì tỉ lệ với giá trị.</div>',
        "Bảng này so hai cách tìm ước chung lớn nhất. Thử từng ước tốn số phép bằng giá trị của số bé, nên với số cỡ mười chín chữ số mất khoảng 56 năm. "
        "Thuật toán chia lấy dư chỉ mất 88 bước, vì cứ hai bước chia thì số bé giảm ít nhất một nửa, nên số bước nhiều nhất tỉ lệ với số chữ số. "
        "Người làm nghề dùng thuật toán chia lấy dư, và đó là lý do mật mã khoá công khai làm việc được với số hàng trăm chữ số.",
        focus=[1, "1.4", "1.4", 2][:4], clear=True),
], checks=[
    "[(lambda a, b: (lambda f: f(f, a, b, 0))(lambda f, x, y, n: (x, n) if y == 0 else f(f, y, x % y, n + 1)))(a, b) for a, b in ((252, 198), (10 ** 6 + 3, 10 ** 6), (2880067194370816120, 1779979416004714189))] == [(18, 4), (1, 3), (1, 88)]",
    "round(1779979416004714189 / 1e9 / 31557600) == 56 and 10 ** 6 / 1e9 == 0.001",
])
quymo["steps"] = [TAB_A, TAB_B] + quymo["steps"]

DE = """# Lab DMS L13 — Số học mô-đun và thuật toán Euclid mở rộng bằng chương trình

Viết `modun.py` (Python 3.11 trở lên); chạy: `python modun.py`.

In đúng bảy dòng (không dấu):
1. `gcd(462, 1071) = <số>` — ước chung lớn nhất bằng thuật toán Euclid (vòng `while`, thay `(a, b)` bằng `(b, a % b)` tới khi `b` bằng 0)
2. `he so Bezout (x, y) thoa 462x + 1071y = 21: <dung|sai>` — tìm `x`, `y` nguyên bằng Euclid mở rộng (đi ngược các dòng chia), rồi KIỂM `462*x + 1071*y == 21` và in `dung` nếu thoả (không in giá trị x, y vì có nhiều cặp đúng)
3. `-17 mod 5 = <số>` — số dư không âm của −17 khi chia cho 5 (toán học cho kết quả trong 0..4)
4. `(123456789 * 987654321) mod 1000: <a> <b>` — `a` là số dư của TÍCH đầy đủ, `b` là số dư của (tích hai số dư của từng thừa số) — hai số phải bằng nhau
5. `1000 ngay nua tu thu Ba la thu <tên>` — tên ngày đánh số thứ Hai = 0, ..., Chủ nhật = 6 (viết `Hai`, `Ba`, `Tu`, `Nam`, `Sau`, `Bay`, `CN`), tính bằng số dư khi chia cho 7
6. `so buoc Euclid cua (832040, 514229): <số>` — số lần chia lấy dư cho tới khi số dư bằng 0
7. `7x = 3 (mod 30): x = <số>` — số x trong 0..29 thoả `(7*x) % 30 == 3` (duyệt từng x)

Gợi ý cho dòng 2 (Euclid mở rộng bằng vòng lặp, không cần đệ quy). Mỗi lần chia ta giữ hai số `a`, `b` kèm cách viết chúng dưới dạng `A*x + B*y` (A, B là hai số đề cho): `a = A*x0 + B*y0` và `b = A*x1 + B*y1`. Lúc đầu `a = A` nên `(x0, y0) = (1, 0)`, và `b = B` nên `(x1, y1) = (0, 1)`. Mỗi vòng, với thương `q = a // b`, cặp số mới là `(b, a % b)`, và hệ số cập nhật cùng quy tắc với số: số mới thứ hai là `a - q*b`, nên hệ số mới thứ hai là `x0 - q*x1` và `y0 - q*y1`:

```python
def mo_rong(A, B):
    a, b = A, B
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0   # a là ước chung lớn nhất, và A*x0 + B*y0 = a
```

`return a, x0, y0` trả về ba giá trị cùng lúc; nhận bằng `g, x, y = mo_rong(462, 1071)`. Hãy tự chạy tay hai vòng đầu với A = 462, B = 1071 để thấy hệ số đổi.

Chấm: `bash labs/cham.sh DMS L13 modun.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""def euclid(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mo_rong(A, B):
    # trả (g, x, y) với A*x + B*y = g
    a, b = A, B
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

print('gcd(462, 1071) =', euclid(462, 1071))
g, x, y = mo_rong(462, 1071)
print('he so Bezout (x, y) thoa 462x + 1071y = 21:', 'dung' if 462 * x + 1071 * y == 21 else 'sai')
print('-17 mod 5 =', (-17) % 5)
print('(123456789 * 987654321) mod 1000:', (123456789 * 987654321) % 1000, ((123456789 % 1000) * (987654321 % 1000)) % 1000)
TEN = ['Hai', 'Ba', 'Tu', 'Nam', 'Sau', 'Bay', 'CN']
print('1000 ngay nua tu thu Ba la thu', TEN[(1 + 1000) % 7])
a, b, buoc = 832040, 514229, 0
while b != 0:
    a, b = b, a % b
    buoc = buoc + 1
print('so buoc Euclid cua (832040, 514229):', buoc)
for x in range(30):
    if (7 * x) % 30 == 3:
        print('7x = 3 (mod 30): x =', x)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> Euclid: <code>a, b = b, a % b</code> lặp tới khi b bằng 0. Euclid mở rộng bằng vòng lặp: cùng với <code>(a, b)</code> giữ hai cặp hệ số <code>(x0, y0)</code> và <code>(x1, y1)</code>, mỗi vòng cập nhật <code>x0, x1 = x1, x0 - q * x1</code> (và tương tự cho <code>y</code>) với <code>q = a // b</code>; khung mã đầy đủ ở <code>de.md</code>. '
    "Số dư của tích: <code>((a % n) * (b % n)) % n</code>. Ngày: chỉ số <code>(1 + 1000) % 7</code> trong danh sách tên. "
    "Lời giải ở <code>labs/DMS/L13/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, thuật toán chia lấy dư lặp việc thay cặp số bằng số bé và số dư, cho tới khi số dư bằng không. Bản mở rộng của thuật toán dùng vòng lặp. Cùng với cặp số, giữ cho mỗi số một cặp hệ số, và mỗi vòng cập nhật hệ số theo đúng quy tắc của số, hệ số mới bằng hệ số cũ trừ thương nhân hệ số kia. Khung mã đầy đủ của hàm này nằm trong đề. "
    "Số dư của một tích bằng số dư của tích hai số dư.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_STEPS = hint_steps2(HINT_BOX, HINT_SAY, [
    ("a, b = b, a % b", "gán cùng lúc: tính xong cả hai giá trị bên phải rồi mới cất; <code>a % b</code> là số dư khi chia a cho b", "a = 252, b = 198: thành a = 198, b = 54"),
    ("x0, x1 = x1, x0 - q * x1", "cùng kiểu gán cùng lúc: x0 nhận giá trị cũ của x1, x1 nhận x0 trừ q lần x1 (<code>*</code> là nhân)", "x0 = 1, x1 = 0, q = 2: thành x0 = 0, x1 = 1"),
    ("q = a // b", "<code>//</code> là chia lấy phần nguyên: q là thương của phép chia", "252 // 198 = 1"),
    ("((a % n) * (b % n)) % n", "lấy dư từng thừa số cho n, nhân hai số dư, rồi lấy dư lần nữa cho n", "a = 123, b = 456, n = 10: (3 * 6) % 10 = 8"),
    ("(1 + 1000) % 7", "chia 1001 cho 7 lấy số dư; kết quả là vị trí trong danh sách tên ngày, đánh số từ 0", "1001 % 7 = 0, vị trí đầu danh sách"),
], [
    "Dòng đầu gán cùng lúc: tính xong cả hai giá trị bên phải rồi mới cất, trong đó dấu phần trăm là chia lấy số dư.",
    "Dòng này cùng kiểu: giá trị mới của x0 là giá trị cũ của x1, còn x1 nhận x0 trừ thương nhân x1.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, nên dòng này tính thương của phép chia.",
    "Dòng này lấy dư từng thừa số, nhân hai số dư, rồi lấy dư lần nữa cho mô-đun.",
    "Dòng cuối chia một nghìn lẻ một cho 7 lấy số dư, và kết quả là vị trí trong danh sách tên ngày, đếm từ 0.",
], HINT_TAIL, '<p class="note">Lời giải ở <code>labs/DMS/L13/loi_giai.py</code> — chỉ mở sau khi đã thử.</p>', split=3)

prac = practice(
    LID, "Tự làm: Euclid, hệ số Bézout, số dư và phương trình đồng dư",
    "<p><b>Đề</b>: viết <code>modun.py</code> in: ước chung lớn nhất của 462 và 1071 và kiểm hệ số Bézout; số dư của −17 chia 5; số dư của một tích lớn tính hai cách; "
    "ngày trong tuần sau 1 000 ngày; số bước Euclid của một cặp số; nghiệm của $7x \\equiv 3 \\pmod{30}$ (bảy dòng, định dạng ở <code>labs/DMS/L13/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Bài thứ tư: số dư của tích bằng số dư của tích hai số dư.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình tìm ước chung lớn nhất của 462 và 1071 và kiểm hệ số biểu diễn, tính số dư của số âm, và tính số dư của một tích lớn bằng hai cách. "
    "Sau đó tính ngày trong tuần sau một nghìn ngày, đếm số bước của thuật toán, và giải một phương trình đồng dư bằng cách duyệt. Bảy dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "modun.py", H_STEPS[0]["show"], H_STEPS[0]["say"],
    pause=420, focus1=[1, 1, 1, 2, 0][:5], focus3=H_STEPS[0]["focus"])
prac["steps"].append(H_STEPS[1])
patch_cham(prac, LID, "modun.py")

OBJ = [
    "Nêu cách tính số dư và kiểm hai số đồng dư theo mô-đun",
    "Cộng, nhân theo mô-đun",
    "Tìm ước chung lớn nhất và hệ số Bézout bằng thuật toán Euclid mở rộng",
    "Đếm số bước của thuật toán Euclid ở các cỡ số khác nhau và so với việc thử từng ước",
    "Viết chương trình tính ước chung lớn nhất, hệ số Bézout, số dư và nghiệm đồng dư",
]
repl = [
    # fix12 (R8): "quan hệ tương đương" giảng lại tại câu
    ("là một quan hệ tương đương (bài 7): các lớp chính là", "là một quan hệ tương đương (bài 7: chia các số thành các lớp, hai số cùng lớp khi cùng số dư): các lớp chính là"),
    ("là một quan hệ tương đương như bài 7, mỗi lớp ứng với một số dư từ 0 đến n trừ 1.", "là một quan hệ tương đương, tức chia các số thành các lớp, hai số cùng lớp khi cùng số dư, ứng với các số dư từ 0 đến n trừ 1."),
    # fix6b (SHOULD/P1): giảng % và bỏ == trong lỗi 1; thêm điều kiện chia hai vế đồng dư
    ("Toán tử <code>%</code> của C, Java cho <code>-7 % 3 == -1</code>; của Python cho 2.", "Toán tử <code>%</code> (chia lấy dư) của C, Java cho <code>-7 % 3</code> ra −1; của Python ra 2."),
    ("nhưng toán tử phần trăm của một số ngôn ngữ lập trình lại trả về âm 1.", "nhưng toán tử phần trăm, tức dấu chia lấy dư của một số ngôn ngữ lập trình, lại trả về âm 1."),
    ("<td>3 − 1 = 2</td><td>không</td></tr></table>\n        focus: [1, 2]", "<td>3 − 1 = 2</td><td>không</td></tr></table>\n          <p class=\"note\">Chỉ chia được khi số chia và mô-đun không có ước chung nào lớn hơn 1.</p>\n        focus: [1, 2, 3]"),
    ("3 trừ 1 bằng 2 không chia hết cho 4.\"", "3 trừ 1 bằng 2 không chia hết cho 4. Chỉ chia được khi số chia và mô-đun không có ước chung nào lớn hơn 1.\""),
]
f, _, _ = apply(LID, quiz_pause=30, objectives=OBJ, repl=repl + asr_keep(LID),
                covers=[(1, "sym_mod"), (2, "arith"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_tuongduong"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Cặp 252 và 198 mất 4 bước, cặp quanh một triệu mất 3 bước, cặp mười tám chữ số mất 88 bước"}))
