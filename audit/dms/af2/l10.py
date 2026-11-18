"""DMS L10 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l10.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L10"

C1 = r"""for n in (8, 100, 1000):
    dem = 0
    for i in range(n):
        for j in range(i + 1, n):
            dem = dem + 1
    print(n, 'nguoi:', dem, 'cap, cong thuc n(n-1)/2 =', n * (n - 1) // 2)
print('1000 nguoi chia 10 nhom, chi so trong nhom:', 10 * (100 * 99 // 2), 'cap')"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for n in (8, 100, 1000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 8, rồi 100, rồi 1000"),
    ("range(n), range(i + 1, n)", "<code>range(n)</code> cho 0 tới n − 1; <code>range(i + 1, n)</code> cho các số từ i + 1 tới n − 1, tức chỉ các người đứng sau i", "i = 2, n = 5: range(3, 5) cho 3, 4"),
    ("dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng dem thêm 1", "dem đang là 27 thì thành 28"),
    ("n * (n - 1) // 2", "<code>*</code> là nhân, <code>//</code> là chia lấy phần nguyên: công thức số cặp", "n = 8: 8 * 7 // 2 = 28"),
    ("print(n, 'nguoi:', dem)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "n = 8: in ra 8 nguoi: 28"),
], "Chương trình đếm cặp dùng năm ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 8, 100, rồi 1000, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số cho các số từ 0 tới n trừ 1, còn với hai số trong ngoặc, từ i cộng 1 tới n trừ 1, tức chỉ các người đứng sau i.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Dấu sao là nhân, hai dấu gạch chéo là chia lấy phần nguyên, nên n nhân n trừ 1, chia 2, cho đúng số cặp.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)

quymo = scene("quymo", "example", "Khi số người tăng: so sánh mọi cặp tốn bình phương", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: liệt kê từng cặp (bắt tay) trong $n$ người rồi so với công thức $\\binom{n}{2} = n(n-1)/2$</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Vòng lặp ngoài chọn người thứ i, vòng lặp trong chỉ chọn người đứng sau i, nên mỗi cặp được đếm đúng một lần, không có thứ tự. "
        "Với 8 người có 28 cặp, với 100 người có 4 950 cặp, với 1 000 người có 499 500 cặp. "
        "Dòng cuối thử chia một nghìn người vào mười nhóm, mỗi nhóm một trăm người, rồi chỉ đếm cặp trong từng nhóm, và chỉ còn 49500 cặp thay vì 499500.",
        focus=[2, ["2.3", "2.5"], ["4.1", "4.3"], "4.4"], clear=True),
    step(
        '<table class="t"><tr><th>số người $n$</th><th>số cặp $\\binom{n}{2}$</th><th>so mọi cặp, một tỉ cặp mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>1 000</td><td>499 500</td><td>chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>$10^4$</td><td>49 995 000</td><td>khoảng 0,05 giây</td></tr>"
        "<tr><td>$10^6$</td><td>499 999 500 000</td><td>khoảng 8 phút</td></tr>"
        "<tr><td>$10^8$</td><td>4 999 999 950 000 000</td><td>khoảng 58 ngày</td></tr></table>"
        '<div class="box key">Số cặp tăng <b>bình phương</b> theo n: gấp 100 lần người thì gấp khoảng <b>10 000</b> lần số cặp. Cách làm nghề: gom các phần tử cùng nhóm trước (sắp xếp, hoặc dùng khoá băm), rồi chỉ so trong nhóm. Ví dụ 1 000 người chia 10 nhóm đều nhau, khi chỉ cần so các cặp cùng khoá: chỉ còn <b>49 500</b> cặp thay vì 499 500, ít hơn hơn 10 lần. <b>Khoá băm</b> = giá trị tính từ mỗi phần tử để xếp nó vào một nhóm.</div>',
        "Bảng này cho thấy số cặp tăng theo bình phương. Với một triệu người, so mọi cặp mất khoảng 8 phút, với một trăm triệu người thì khoảng 58 ngày. "
        "Người làm nghề không so mọi cặp, mà gom các phần tử cùng nhóm trước, bằng cách sắp xếp hoặc dùng khoá băm, tức một giá trị tính từ mỗi phần tử để xếp nó vào một nhóm. Rồi họ chỉ so trong từng nhóm. Như ở ví dụ chạy thật, một nghìn người chia mười nhóm đều nhau, khi chỉ cần so các cặp cùng nhóm, còn 49500 cặp, ít hơn hơn mười lần. Đánh đổi là phải tốn thêm bộ nhớ hoặc thời gian sắp xếp.",
        focus=[1, ["1.4", "1.5"], 2, 2, 2, 2], clear=True),
], checks=[
    "[n * (n - 1) // 2 for n in (8, 100, 1000)] == [28, 4950, 499500]",
    "[n * (n - 1) // 2 for n in (10 ** 4, 10 ** 6, 10 ** 8)] == [49995000, 499999500000, 4999999950000000]",
    "round(499999500000 / 1e9 / 60) == 8 and round(4999999950000000 / 1e9 / 86400) == 58 and round(49995000 / 1e9, 2) == 0.05",
    "(10 ** 8 // 10 ** 6) ** 2 == 10 ** 4",
    "10 * (100 * 99 // 2) == 49500 and 1000 * 999 // 2 == 499500 and 499500 / 49500 > 10",
])

DE = """# Lab DMS L10 — Tam giác Pascal, tổ hợp và đường đi trên lưới bằng chương trình

Viết `tohop.py` (Python 3.11 trở lên); chạy: `python tohop.py`.

Viết hàm `pascal(n)` trả hàng thứ n của tam giác Pascal (hàng 0 là `[1]`, hàng 1 là `[1, 1]`, ...) bằng QUY TẮC CỘNG (mỗi số bằng tổng hai số phía trên, hai đầu là 1), KHÔNG dùng công thức giai thừa. In đúng năm dòng:

1. `C(12,5): <a> <b>` (`C(n,k)` là tổ hợp chập k của n) — `a` tính bằng công thức giai thừa `12! / (5! 7!)`, `b` lấy từ `pascal(12)[5]`
2. `hang 8 cua tam giac Pascal: ...` — các số của hàng 8, cách nhau một dấu cách
3. `tong hang 6: <số>` — tổng các số của hàng 6
4. `uy ban 3 nguoi, 7 nam 5 nu, it nhat 1 nu: <a> <b>` — `a = C(12,3) − C(7,3)` (lấy từ `pascal`), `b` đếm vét cạn (thử hết mọi trường hợp): liệt kê mọi nhóm 3 người từ 12 người (7 nam, 5 nữ) và đếm nhóm có ít nhất một nữ
5. `duong di luoi 4 phai 3 len: <a> <b>` — `a = C(7,3)` (từ `pascal`), `b` điền số trên lưới: ô (hàng r, cột c) có `d[r][c] = d[r-1][c] + d[r][c-1]`, hàng đầu và cột đầu bằng 1, đáp số là `d[3][4]`

Gợi ý: `from math import factorial`; `from itertools import combinations`; nhóm 3 người: `combinations(nguoi, 3)`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from math import factorial` ở đầu tệp: mượn hàm có sẵn `factorial(n)`, cho n giai thừa (`factorial(4)` là 24).
- `from itertools import combinations` mượn hàm có sẵn khác: `combinations(['a', 'b', 'c'], 2)` lần lượt cho `('a', 'b')`, `('a', 'c')`, `('b', 'c')`, mọi cách chọn 2 phần tử, không kể thứ tự. Vòng lặp: `for nhom in combinations(nguoi, 3):`.
- Danh sách lồng nhau: `d = [[1] * 5 for _ in range(4)]` là danh sách 4 hàng, mỗi hàng 5 số 1; `d[r][c]` là ô ở hàng `r`, cột `c` (đếm từ 0).

Chấm: `bash labs/cham.sh DMS L10 tohop.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from math import factorial
from itertools import combinations

def pascal(n):
    hang = [1]
    for _ in range(n):
        moi = [1]
        for i in range(len(hang) - 1):
            moi.append(hang[i] + hang[i + 1])
        moi.append(1)
        hang = moi
    return hang

print('C(12,5):', factorial(12) // (factorial(5) * factorial(7)), pascal(12)[5])
print('hang 8 cua tam giac Pascal:', ' '.join(str(x) for x in pascal(8)))
print('tong hang 6:', sum(pascal(6)))

nguoi = [('nam', i) for i in range(7)] + [('nu', i) for i in range(5)]
co_nu = 0
for nhom in combinations(nguoi, 3):
    if any(p[0] == 'nu' for p in nhom):
        co_nu = co_nu + 1
print('uy ban 3 nguoi, 7 nam 5 nu, it nhat 1 nu:', pascal(12)[3] - pascal(7)[3], co_nu)

d = [[1] * 5 for _ in range(4)]
for r in range(1, 4):
    for c in range(1, 5):
        d[r][c] = d[r - 1][c] + d[r][c - 1]
print('duong di luoi 4 phai 3 len:', pascal(7)[3], d[3][4])"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> hàng mới = <code>[1]</code>, rồi <code>hang[i] + hang[i + 1]</code> với mọi i, rồi <code>1</code>. Hàng n, phần tử k chính là $\\binom{n}{k}$. '
    "Ủy ban có ít nhất một nữ = tất cả nhóm 3 người − nhóm toàn nam = $C(12,3) - C(7,3)$. "
    "Lời giải ở <code>labs/DMS/L10/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, hàng mới của tam giác bắt đầu bằng 1, rồi mỗi số là tổng hai số đứng cạnh nhau ở hàng trước, rồi kết thúc bằng 1. Phần tử thứ k của hàng n chính là tổ hợp chập k của n. "
    "Hàm tự viết, giai thừa, liệt kê nhóm và lưới số được đọc ở bảng ngay sau. "
    "Ủy ban có ít nhất một nữ bằng tất cả các nhóm ba người trừ nhóm toàn nam. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("hang[i] + hang[i + 1]", "<code>hang[i]</code> là phần tử thứ i của danh sách (đếm từ 0), <code>hang[i + 1]</code> là phần tử kế tiếp; cộng lại là tổng hai số liền nhau của hàng trên", "hang = [1, 3, 3, 1], i = 1: 3 + 3 = 6"),
], [
    "Dấu ngoặc vuông chỉ phần tử thứ i của hàng trên, đếm từ 0, nên dòng này cộng hai số liền nhau của hàng trên để ra một số của hàng mới.",
])

prac = practice(
    LID, "Tự làm: dựng tam giác Pascal bằng quy tắc cộng và kiểm tổ hợp hai cách",
    "<p><b>Đề</b>: viết <code>tohop.py</code> với hàm <code>pascal(n)</code> dựng hàng thứ $n$ chỉ bằng quy tắc cộng, rồi in: $C(12,5)$ (tổ hợp chập 5 của 12) hai cách, hàng 8, tổng hàng 6, "
    "số ủy ban có ít nhất một nữ (công thức và vét cạn, tức thử hết mọi trường hợp), số đường đi trên lưới 4 phải 3 lên (công thức và điền số). Năm dòng, định dạng ở <code>labs/DMS/L10/de.md</code>.</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Ủy ban “ít nhất một nữ” = tất cả trừ nhóm toàn nam.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết hàm dựng một hàng của tam giác Pascal chỉ bằng quy tắc cộng, rồi dùng nó để tính tổ hợp. "
    "In tổ hợp chập 5 của 12 bằng hai cách, hàng 8 và tổng hàng 6. Sau đó in số ủy ban có ít nhất một nữ và số đường đi trên lưới, mỗi bài tính bằng công thức và kiểm lại bằng cách khác. "
    "Năm dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "tohop.py", H_HTML, H_SAY,
    pause=360, focus1=[1, 1, 1, 1, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "tohop.py")
add_read_step(prac, [
    ("def pascal(n): ... return hang", "<code>def</code> đặt <b>tên</b> cho một đoạn tính nhận n; <code>return</code> là kết quả đoạn đó đưa ra", "def gap_doi(n): return n * 2 thì gap_doi(4) là 8"),
    ("from math import factorial", "mượn hàm làm sẵn <code>factorial(n)</code> cho n giai thừa", "factorial(4) là 24"),
    ("for nhom in combinations(nguoi, 3):", "sau <code>from itertools import combinations</code>: nhom chạy qua mọi cách chọn 3 người, không kể thứ tự", "combinations(['a', 'b', 'c'], 2) cho ('a', 'b'), ('a', 'c'), ('b', 'c')"),
    ("d = [[1] * 5 for _ in range(4)]", "lưới 4 hàng, mỗi hàng 5 số 1; <code>d[r][c]</code> là ô ở hàng r, cột c (đếm từ 0)", "d[0][0] là ô đầu, d[3][4] là ô cuối"),
], "Bốn chỗ cú pháp trong lời giải, ở đầu tệp và trong thân chương trình, đọc như sau.", [
    "Dòng định nghĩa hàm đặt tên cho một đoạn tính nhận n, và chữ trả về cho biết kết quả đoạn đó đưa ra.",
    "Dòng mượn hàm làm sẵn cho n giai thừa, tên hàm ghi trên màn hình.",
    "Vòng lặp này cho nhóm chạy qua mọi cách chọn ba người, không kể thứ tự, nhờ hàm liệt kê mượn ở đầu tệp.",
    "Danh sách trong danh sách là lưới số, ở đây bốn hàng mỗi hàng năm số 1, và hai ngoặc vuông liền nhau chỉ ô ở hàng r, cột c, đếm từ 0.",
])

OBJ = [
    "Tính tổ hợp và giải thích vì sao chia k!",
    "Nêu cách dựng tam giác Pascal và vì sao mỗi số bằng tổng hai số phía trên",
    "Khai triển nhị thức và chứng minh tổng một hàng bằng 2 mũ n",
    "Đếm số cặp khi số người tăng và nêu vì sao so mọi cặp không dùng được khi số người rất lớn",
    "Viết chương trình dựng tam giác Pascal bằng quy tắc cộng và kiểm tổ hợp bằng hai cách",
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "example"), (2, "pascal"), (3, "binomial"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                repl=[("Thay x và y cùng bằng 1, vế trái", "Thay x và y cùng có giá trị là 1, vế trái"),
                      ("Ta được x mũ n trừ k nhân y mũ k khi chọn y", "Ta được x mũ, n trừ k trên đầu, nhân y mũ k khi chọn y"),
                      ('Chia $k!$ cả khi các vật đã giống nhau <b class="red">(sai)</b>', 'Chia thêm $k!$ khi đã đếm theo nhóm <b class="red">(sai)</b>')],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"))
print(f)
print(ledger_sync(LID, claims={"quymo": "8 người có 28 cặp, 100 người 4 950 cặp, 1 000 người 499 500 cặp, khớp công thức n(n-1)/2"}))
