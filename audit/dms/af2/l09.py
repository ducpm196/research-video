"""DMS L09 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l09.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L09"

C1 = r"""for do_dai in (4, 6):
    dem = 0
    for ma in range(10 ** do_dai):
        dem = dem + 1
    print(do_dai, 'chu so:', dem, 'ma')
for do_dai in (8, 12):
    so = 62 ** do_dai
    print(do_dai, 'ky tu:', so, 'mat khau,', so // 10 ** 9 // 86400, 'ngay')"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for do_dai in (4, 6):", "với mỗi do_dai (độ dài) lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "hai lượt: độ dài 4, rồi độ dài 6"),
    ("10 ** do_dai", "<code>**</code> là lũy thừa: 10 mũ do_dai, số mã có do_dai chữ số", "10 ** 4 là 10000"),
    ("range(10 ** do_dai)", "các số từ 0 tới 10 ** do_dai − 1: mỗi số là một mã", "range(3) cho 0, 1, 2"),
    ("dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng dem thêm 1", "dem đang là 9 thì thành 10"),
    ("print(do_dai, 'chu so:', dem)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "in ra 4 chu so: 10000"),
    ("so // 10 ** 9 // 86400", "<code>//</code> là chia lấy phần nguyên: chia cho 10<sup>9</sup> (một tỉ lần thử mỗi giây) ra số giây, rồi chia cho 86400 (số giây của một ngày) ra số ngày", "7 // 2 là 3"),
], "Mã PIN là mã số bí mật gồm vài chữ số, như mã mở thẻ; chương trình đếm chúng dùng sáu ký hiệu sau.", [
    "Dòng mở đầu vòng lặp: với mỗi độ dài lần lượt là 4 rồi 6, làm các dòng thụt vào bên dưới.",
    "Hai dấu sao liền nhau là lấy lũy thừa, nên 10 hai sao 4 là 10 mũ 4, tức mười nghìn mã bốn chữ số.",
    "Hàm tạo dãy số cho các số từ 0 tới mười mũ độ dài trừ 1, mỗi số là một mã.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
    "Hai dấu gạch chéo là chia lấy phần nguyên: chia cho 10 mũ 9 ra số giây, rồi chia cho 86400, số giây của một ngày, ra số ngày.",
], split=3, note='<p class="note"><b>PIN</b>: mã số bí mật gồm vài chữ số.</p>')

quymo = scene("quymo", "example", "Khi độ dài tăng: mã PIN đếm xong, mật khẩu dài thì không dò hết nổi", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: PIN 4, 6 chữ số; mật khẩu 8, 12 ký tự từ 62 ký tự (1 tỉ lần thử/giây, minh hoạ)</p>"
        + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Vòng lặp đầu đếm từng mã PIN, 4 chữ số có đúng 10 nghìn mã, 6 chữ số có đúng một triệu mã. "
        "Ở các dòng cuối, ta tính 62 mũ 8 và 62 mũ 12 bằng quy tắc nhân, rồi chia cho một tỉ lần thử mỗi giây để ra số giây. "
        "Chia tiếp cho 86400, số giây của một ngày, để ra số ngày; hai dấu gạch chéo là chia lấy phần nguyên. "
        "Máy bỏ phần lẻ, nên mật khẩu 8 ký tự hiện 2 ngày, thật ra khoảng hai ngày rưỡi, còn mật khẩu 12 ký tự cần hơn 37 triệu ngày.",
        focus=[2, ["2.2", "2.4"], ["2.7", "2.8"], "2.8", ["4.3", "4.4"]], clear=True),
    step(
        '<table class="t"><tr><th>độ dài và bảng ký tự</th><th>số khả năng</th><th>dò hết ở một tỉ lần mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>PIN 4 chữ số ($10^4$)</td><td>10 000</td><td>10 phần triệu giây</td></tr>"
        "<tr><td>PIN 6 chữ số ($10^6$)</td><td>1 000 000</td><td>1 phần nghìn giây</td></tr>"
        "<tr><td>8 ký tự từ 62 ký tự: 26 chữ thường, 26 chữ hoa, 10 chữ số ($62^8$)</td><td>khoảng $2{,}2 \\times 10^{14}$</td><td>hơn 2 ngày (khoảng 2,5 ngày)</td></tr>"
        "<tr><td>12 ký tự từ 62 ký tự ($62^{12}$)</td><td>khoảng $3{,}2 \\times 10^{21}$</td><td>khoảng 102 000 năm</td></tr></table>"
        '<div class="box key">Mỗi ký tự thêm vào <b>nhân</b> số khả năng lên 62 lần. Hệ thật không chỉ dựa vào độ dài: thường còn <b>giới hạn số lần thử</b> mỗi tài khoản, vì máy dò thật không nhanh một tỉ lần mỗi giây vào một dịch vụ trực tuyến (số minh hoạ).</div>',
        "Bảng này cho thấy mỗi ký tự thêm vào nhân số khả năng lên 62 lần. Mã PIN dò hết gần như tức thì, mật khẩu 8 ký tự khoảng hai ngày rưỡi, còn mật khẩu 12 ký tự khoảng một trăm nghìn năm. "
        "Người làm nghề phải chọn, tăng độ dài mật khẩu, và đồng thời giới hạn số lần thử, vì chỉ dựa vào độ dài thì mã PIN ngắn gần như không có sức cản.",
        focus=[1, ["1.2", "1.3", "1.4", "1.5"], 2], clear=True),
], checks=[
    "[10 ** d for d in (4, 6)] == [10000, 1000000]",
    "62 ** 8 == 218340105584896 and 62 ** 8 // 10 ** 9 // 86400 == 2 and round(62 ** 8 / 1e9 / 86400, 1) == 2.5",
    "62 ** 12 == 3226266762397899821056 and 62 ** 12 // 10 ** 9 // 86400 == 37341050",
    "100000 < 62 ** 12 / 1e9 / 31557600 < 105000",
])

DE = """# Lab DMS L09 — Đếm bằng quy tắc nhân và kiểm lại bằng cách liệt kê hết

Viết `dem.py` (Python 3.11 trở lên); chạy: `python dem.py`.

Với mỗi bài đếm dưới đây, in một dòng `<mô tả>: <công thức> <vét cạn>`, trong đó `<công thức>` là kết quả tính bằng quy tắc nhân / chỉnh hợp / hoán vị (một biểu thức số học, KHÔNG liệt kê), và `<vét cạn>` là kết quả đếm bằng cách liệt kê mọi trường hợp (`itertools.product`, `itertools.permutations`, hoặc vòng lặp). Hai số phải bằng nhau.

Dòng cần in, đúng chữ (không dấu):
1. `ma PIN 4 chu so (duoc lap)` — chuỗi 4 chữ số từ 0 đến 9
2. `ma PIN 4 chu so khac nhau` — 4 chữ số từ 0 đến 9, đôi một khác nhau
3. `xep 5 nguoi thanh hang` — hoán vị của 5 người
4. `chuoi 3 ky tu tu abcd, duoc lap`
5. `chuoi 3 ky tu tu abcd, khong lap`
6. `so chan 3 chu so khac nhau tu 1..5` — số có 3 chữ số đôi một khác nhau lập từ các chữ số 1, 2, 3, 4, 5 và chia hết cho 2

Ví dụ định dạng: `chuoi 2 ky tu tu ab, duoc lap: 4 4`.

Gợi ý: ví dụ ở dòng 6, chọn chữ số hàng đơn vị trước (chẵn), rồi các hàng còn lại là chỉnh hợp.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import product, permutations` ở đầu tệp: mượn hai hàm có sẵn của Python. `product('ab', repeat=2)` lần lượt cho `('a', 'a')`, `('a', 'b')`, `('b', 'a')`, `('b', 'b')`: mọi chuỗi có lặp (n mũ k chuỗi). `permutations('abc', 2)` cho `('a', 'b')`, `('a', 'c')`, `('b', 'a')`, ...: mọi chuỗi không lặp (n × (n−1) × ... chuỗi).
- `len(list(...))` đếm số phần tử mà các hàm đó sinh ra. `p[2]` là phần tử thứ ba của bộ `p` (đếm từ 0); `int(p[2]) % 2 == 0` kiểm số đó chẵn.

Chấm: `bash labs/cham.sh DMS L09 dem.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import product, permutations

def in_ra(mo_ta, cong_thuc, vet_can):
    print(mo_ta + ':', cong_thuc, vet_can)

in_ra('ma PIN 4 chu so (duoc lap)', 10 ** 4, len(list(product(range(10), repeat=4))))
in_ra('ma PIN 4 chu so khac nhau', 10 * 9 * 8 * 7, len(list(permutations(range(10), 4))))
in_ra('xep 5 nguoi thanh hang', 5 * 4 * 3 * 2 * 1, len(list(permutations('ABCDE'))))
in_ra('chuoi 3 ky tu tu abcd, duoc lap', 4 ** 3, len(list(product('abcd', repeat=3))))
in_ra('chuoi 3 ky tu tu abcd, khong lap', 4 * 3 * 2, len(list(permutations('abcd', 3))))
chan = 0
for p in permutations('12345', 3):
    if int(p[2]) % 2 == 0:
        chan = chan + 1
in_ra('so chan 3 chu so khac nhau tu 1..5', 2 * 4 * 3, chan)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> có lặp: mỗi vị trí $n$ lựa chọn, $n^k$ cách (<code>product(..., repeat=k)</code>). Không lặp: $n \\times (n-1) \\times \\dots$ (<code>permutations(..., k)</code>); cả hai mượn từ <code>itertools</code>, cú pháp và ví dụ nhỏ ở <code>de.md</code>. '
    "Số chẵn: hàng đơn vị là 2 hoặc 4 (2 cách), hai hàng còn lại chọn từ 4 chữ số còn lại, có thứ tự: $2 \\times 4 \\times 3 = 24$. "
    "Lời giải ở <code>labs/DMS/L09/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, khi được lặp thì mỗi vị trí có n lựa chọn, nhân lại là n mũ k. Khi không lặp thì mỗi vị trí sau ít hơn vị trí trước một lựa chọn. "
    "Với số chẵn, hàng đơn vị là 2 hoặc 4, rồi hai hàng còn lại chọn có thứ tự từ bốn chữ số còn lại. "
    "Hai hàm liệt kê có sẵn được mượn ở đầu tệp, cách dùng kèm ví dụ nằm trong đề. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("product(X, repeat=k)", "mọi chuỗi độ dài k, mỗi vị trí chọn <b>có lặp</b> từ X", "product('ab', repeat=2) cho aa, ab, ba, bb: 4 chuỗi, bằng 2 mũ 2"),
    ("permutations(X, k)", "mọi chuỗi độ dài k, <b>không lặp</b> phần tử", "permutations('abc', 2) cho ab, ac, ba, bc, ca, cb: 6 chuỗi, bằng 3 nhân 2"),
], [
    "Hàm đầu liệt kê mọi chuỗi độ dài k mà mỗi vị trí được chọn lặp lại từ tập X, nên có n mũ k chuỗi.",
    "Hàm sau liệt kê mọi chuỗi độ dài k không lặp phần tử, nên có n nhân n trừ 1 nhân tiếp, đủ k thừa số.",
])

prac = practice(
    LID, "Tự làm: đếm bằng quy tắc nhân rồi kiểm bằng cách liệt kê hết",
    "<p><b>Đề</b>: viết <code>dem.py</code> giải sáu bài đếm (mã PIN có lặp và không lặp, xếp 5 người thành hàng, chuỗi 3 ký tự từ abcd có và không lặp, "
    "số chẵn 3 chữ số khác nhau từ 1 đến 5). Mỗi dòng in công thức và kết quả liệt kê hết: hai số phải bằng nhau (định dạng ở <code>labs/DMS/L09/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dòng cuối cần hai quy tắc: chọn hàng đơn vị chẵn trước, rồi chỉnh hợp.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình giải sáu bài đếm, và với mỗi bài, in kết quả của công thức nhân cạnh kết quả liệt kê hết mọi trường hợp. "
    "Hai số phải bằng nhau. Dòng cuối cần hai quy tắc, chọn hàng đơn vị chẵn trước, rồi mới chọn các hàng còn lại. Sáu bài và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "dem.py", H_HTML, H_SAY,
    pause=300, focus1=[1, 1, 1, 2, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "dem.py")

OBJ = [
    "Chọn đúng quy tắc cộng hay quy tắc nhân",
    "Đếm hoán vị và chỉnh hợp",
    "Ước lượng độ khó dò mật khẩu bằng phép đếm",
    "Đếm số mã và ước thời gian dò hết khi độ dài mật khẩu tăng, và nêu vì sao chỉ dựa vào độ dài thì chưa đủ",
    "Viết chương trình đếm bằng quy tắc nhân, hoán vị, chỉnh hợp và kiểm lại bằng cách liệt kê hết",
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "example"), (2, "example"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                repl=[("làm <b>lần lượt</b> nhiều bước, số cách mỗi bước không đổi", "làm <b>lần lượt</b> nhiều bước, số cách ở mỗi bước không phụ thuộc bước trước chọn gì"),
                      # fix6 (R4 SHOULD): tiêu đề Lỗi 2 mơ hồ so với bài hoán vị
                      ('<b>thay đổi</b> theo bước trước <b class="red">(sai)</b>', '<b>thay đổi</b> tuỳ bước trước chọn cái nào <b class="red">(sai)</b>'),
                      # fix6 (R4): ASR nghe "bằng một" thành "bằng mục" → đổi câu
                      ("Người ta quy ước 0 giai thừa bằng 1.", "Người ta quy ước 0 giai thừa có giá trị là 1."),
                      ("Thật ra 0 giai thừa bằng 1, vì có đúng một cách xếp 0 vật", "Thật ra 0 giai thừa có giá trị là 1, vì có đúng một cách xếp 0 vật")],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"))
print(f)
print(ledger_sync(LID, claims={"quymo": "PIN 4 chữ số có đúng 10 nghìn mã, 6 chữ số một triệu mã; mật khẩu 8 ký tự từ 62 ký tự dò hết hơn 2 ngày (khoảng 2,5 ngày), 12 ký tự hơn 37 triệu ngày"}))
