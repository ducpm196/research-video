"""DMS L12 → AF2 (WP5 phiên 2). Chạy: .venv/Scripts/python -B audit/dms/af2/l12.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L12"

C1 = r"""from itertools import permutations
from math import comb, factorial
for n in (6, 8):
    vet = 0
    for p in permutations(range(n)):
        if all(p[i] != i for i in range(n)):
            vet = vet + 1
    ct = sum((-1) ** k * comb(n, k) * factorial(n - k) for k in range(n + 1))
    print(n, 'nguoi: vet can', vet, ', bao ham loai tru', ct)"""
O1 = run_py(C1)
print(O1)

TAB_A = read_step([
    ("from itertools import permutations", "mượn hàm có sẵn <code>permutations</code>: liệt kê mọi cách xếp các phần tử thành hàng", "permutations(range(3)) cho 6 hàng: (0, 1, 2), (0, 2, 1), …"),
    ("from math import comb, factorial", "mượn hai hàm có sẵn: <code>comb(n, k)</code> là tổ hợp chập k của n, <code>factorial(m)</code> là m giai thừa", "comb(4, 2) = 6; factorial(4) = 24"),
    ("for n in (6, 8):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "hai lượt: n = 6, rồi 8"),
    ("vet = 0, vet = vet + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái; dòng đầu đặt bộ đếm về 0, dòng sau tăng nó thêm 1", "vet đang là 41 thì thành 42"),
], "Chương trình dùng mười ký hiệu, ta đọc bốn cái đầu trước.", [
    "Dòng đầu mượn một hàm có sẵn liệt kê mọi cách xếp các phần tử thành hàng, nên ba phần tử cho sáu hàng.",
    "Dòng này mượn hai hàm có sẵn, một hàm cho tổ hợp chập k của n, một hàm cho giai thừa, nên tổ hợp chập 2 của 4 là 6.",
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 6 rồi 8, làm các dòng thụt vào bên dưới.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên một dòng đặt biến đếm về 0 và dòng kia tăng nó thêm một.",
])

TAB_B = read_steps([
    ("for p in permutations(range(n)):", "<code>range(n)</code> cho 0 tới n − 1; mỗi <code>p</code> là một cách xếp các số đó thành hàng, tức một cách trả mũ: người i nhận mũ <code>p[i]</code>", "n = 3: p lần lượt là (0, 1, 2), (0, 2, 1), (1, 0, 2), …"),
    ("if điều_kiện:", "<code>if</code> là nếu: chỉ khi điều kiện đúng mới chạy các dòng thụt vào bên dưới", "if x > 0: … chỉ chạy khi x lớn hơn 0"),
    ("all(p[i] != i for i in range(n))", "<code>p[i]</code> là phần tử thứ i của p, đếm từ 0; <code>!=</code> là khác; <code>all</code> đúng khi điều kiện đúng với mọi i từ 0 tới n − 1", "p = (1, 2, 0): đúng; p = (0, 2, 1): sai vì p[0] = 0"),
    ("(-1) ** k * comb(n, k) * factorial(n - k)", "<code>**</code> là lũy thừa nên (−1) ** k là +1 khi k chẵn, −1 khi k lẻ; <code>*</code> là nhân: một số hạng của bao hàm–loại trừ", "n = 4, k = 2: (+1) * 6 * 2 = 12"),
    ("sum(... for k in range(n + 1))", "cộng các số hạng khi k chạy lần lượt từ 0 tới n", "n = 3: cộng số hạng của k = 0, 1, 2, 3"),
    ("print(n, 'nguoi: vet can', vet, ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>vet can</code> là vét cạn, tức liệt kê hết, viết không dấu", "in ra 6 nguoi: vet can 265 …"),
], "Sáu ký hiệu còn lại nằm ở vòng lặp trong và dòng tính tổng.", [
    "Hàm tạo dãy số cho 0 tới n trừ 1, và mỗi p là một cách xếp các số đó thành hàng, tức một cách trả mũ.",
    "Chữ nếu ở đầu dòng làm các dòng thụt vào chỉ khi điều kiện đúng.",
    "Dấu ngoặc vuông lấy phần tử thứ i của p đếm từ 0, dấu chấm than kèm bằng là khác, và hàm kiểm tra này đúng khi điều kiện đúng với mọi i.",
    "Hai dấu sao liền nhau là lũy thừa, nên âm một mũ k là một khi k chẵn và âm một khi k lẻ, còn dấu sao đơn là nhân.",
    "Hàm tính tổng cộng các số hạng khi k chạy lần lượt từ 0 tới n, chính là các số hạng của bao hàm loại trừ.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách, và chữ vet can là vét cạn viết không dấu.",
], split=3)

quymo = scene("quymo", "example", "Khi số người tăng: liệt kê mọi cách trả mũ không kịp, bao hàm–loại trừ thì kịp", [
    step(
        "<p><b>Chạy thật</b>: đếm cách trả mũ để không ai nhận đúng mũ của mình, hai cách</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Với mỗi n, vòng lặp liệt kê mọi cách trả mũ rồi đếm các cách mà không ai nhận đúng mũ của mình. "
        "Với 6 người, đếm trực tiếp ra 265, bao hàm loại trừ cũng ra 265. Với 8 người, cả hai cùng ra 14 833.",
        focus=[2, ["2.5", "2.7"], "4.1", "4.2"], clear=True),
    step(
        "<p>Hai dòng có cú pháp mới trong chương trình trên:</p>"
        '<div class="box key"><code>all(p[i] != i for i in range(n))</code>: đúng khi điều kiện <code>p[i] != i</code> đúng với <b>mọi</b> vị trí <code>i</code> từ 0 đến $n - 1$, tức không ai nhận đúng mũ của mình.</div>'
        '<div class="box key"><code>sum(... for k in range(n + 1))</code>: cộng các số hạng khi <code>k</code> chạy lần lượt từ 0 đến $n$.</div>',
        "Hai dòng của chương trình có cú pháp mới. Dòng điều kiện kiểm rằng với mọi vị trí i, người ở vị trí i không nhận đúng mũ số i, và nó đúng khi điều đó thoả ở mọi vị trí. "
        "Dòng tính tổng cộng các số hạng khi k chạy lần lượt từ 0 đến n, đó chính là các số hạng của bao hàm loại trừ.",
        focus=[1, 2, 3], clear=True),
    step(
        '<table class="t"><tr><th>số người $n$</th><th>liệt kê mọi cách trả ($n!$ cách), một tỉ cách mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>10</td><td>3 628 800 cách, khoảng 4 phần nghìn giây</td></tr>"
        "<tr><td>15</td><td>1 307 674 368 000 cách, khoảng 22 phút</td></tr>"
        "<tr><td>20</td><td>2 432 902 008 176 640 000 cách, khoảng 77 năm</td></tr>"
        "<tr><td><b>bao hàm–loại trừ</b></td><td><b>$n + 1$ số hạng</b>: số cách trả cho 20 người là 895 014 631 192 902 121, tính tức thì</td></tr></table>"
        '<div class="box key">Liệt kê tăng <b>giai thừa</b>; bao hàm–loại trừ chỉ cộng trừ <b>$n + 1$ số hạng</b>. Và tỉ lệ “không ai đúng” cho 20 người vẫn khoảng 0,368.</div>',
        "Bảng này cho thấy liệt kê mọi cách trả tăng theo giai thừa. Với 15 người đã mất khoảng 22 phút, với 20 người thì khoảng 77 năm. "
        "Còn bao hàm loại trừ chỉ có n cộng một số hạng, nên số cách trả cho 20 người tính được tức thì. "
        "Người làm nghề chọn công thức, và chỉ liệt kê để kiểm lại trên cỡ nhỏ.",
        focus=[1, ["1.3", "1.4"], "1.5", 2], clear=True),
], checks=[
    "[sum(1 for p in __import__('itertools').permutations(range(n)) if all(p[i] != i for i in range(n))) for n in (6, 8)] == [265, 14833]",
    "[sum((-1) ** k * math.comb(n, k) * math.factorial(n - k) for k in range(n + 1)) for n in (6, 8, 20)] == [265, 14833, 895014631192902121]",
    "[math.factorial(n) for n in (10, 15, 20)] == [3628800, 1307674368000, 2432902008176640000]",
    "round(math.factorial(15) / 1e9 / 60) == 22 and round(math.factorial(20) / 1e9 / 31557600) == 77 and round(895014631192902121 / math.factorial(20), 3) == 0.368",
])
quymo["steps"] = flat(TAB_A, TAB_B, quymo["steps"][0], quymo["steps"][2])   # fix6b: bảng đọc mã thay bước "cú pháp mới" đặt sau mã

DE = """# Lab DMS L12 — Bao hàm–loại trừ: đếm bằng công thức và kiểm bằng cách liệt kê hết

Viết `baohamloaitru.py` (Python 3.11 trở lên); chạy: `python baohamloaitru.py`.

Với mỗi bài, in một dòng `<mô tả>: <bao hàm–loại trừ> <vét cạn>`; `<bao hàm–loại trừ>` tính bằng công thức (cộng, trừ xen kẽ theo số tập trong giao), `<vét cạn>` đếm bằng cách liệt kê hết. Hai số phải bằng nhau.

Năm dòng, đúng chữ (không dấu):
1. `khong chia het cho 3, 5, 7 tu 1 den 1000` — số nguyên từ 1 đến 1000 không chia hết cho cả ba số 3, 5, 7 (bao hàm–loại trừ cho ba tập; số chia hết cho a là `1000 // a`)
2. `D7` — số hoán vị của 7 vật mà không vật nào ở đúng vị trí cũ
3. `D9` — như trên cho 9 vật (vét cạn 362 880 hoán vị)
4. `toan anh 5 phan tu len 3 phan tu` — số hàm từ tập 5 phần tử lên tập 3 phần tử sao cho mọi phần tử của tập đích đều được dùng (bao hàm–loại trừ: lấy tất cả các hàm rồi trừ những hàm bỏ sót ít nhất một giá trị của tập đích, tự lập biểu thức; vét cạn: `product(range(3), repeat=5)` giữ lại dãy dùng đủ 3 giá trị)
5. `so nguyen to cung nhau voi 360 trong 1..360` — đếm các số k từ 1 đến 360 nguyên tố cùng nhau với 360. (Hai số nguyên tố cùng nhau khi ước chung lớn nhất của chúng bằng 1, tức không có số nào lớn hơn 1 chia hết cho cả hai; ví dụ 8 và 15 là nguyên tố cùng nhau, 8 và 12 thì không vì 4 chia hết cho cả hai. `math.gcd(a, b)` cho ước chung lớn nhất của a và b.) Cho 360 = 2³ · 3² · 5, nên chỉ cần các số nguyên tố 2, 3, 5; vét cạn: `math.gcd`.

Ví dụ định dạng: `D3: 2 2`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import permutations, product, combinations` mượn các hàm liệt kê có sẵn: `permutations(range(3))` cho mọi cách xếp 3 số 0, 1, 2 thành hàng (6 hàng); `product(range(3), repeat=2)` cho mọi bộ hai số từ 0 đến 2 (9 bộ); `combinations([2, 3, 5], 2)` cho `(2, 3)`, `(2, 5)`, `(3, 5)`, mọi cách chọn 2 phần tử không kể thứ tự. `from math import comb, factorial, gcd` mượn tổ hợp, giai thừa và ước chung lớn nhất.
- `sum(1 for p in permutations(range(n)) if điều kiện)`: với mỗi `p`, nếu điều kiện đúng thì cộng thêm 1, tức đếm các `p` thoả điều kiện. Dùng vòng lặp thường với `dem = dem + 1` cũng được.
- `all(p[i] != i for i in range(n))`: đúng khi `p[i] != i` đúng với mọi `i` từ 0 đến n − 1. `len(set(f))` đếm số giá trị khác nhau trong `f`.

Chấm: `bash labs/cham.sh DMS L12 baohamloaitru.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import permutations, product, combinations
from math import comb, factorial, gcd

def in_ra(mo_ta, ct, vet):
    print(mo_ta + ':', ct, vet)

def ihl(tong, uoc):
    # tong: số phần tử; uoc: các số nguyên tố; mỗi giao là bội chung -> tong // tích
    kq = tong
    for k in range(1, len(uoc) + 1):
        for nhom in combinations(uoc, k):
            tich = 1
            for u in nhom:
                tich = tich * u
            kq = kq + (-1) ** k * (tong // tich)
    return kq

def D(n):
    return sum((-1) ** k * comb(n, k) * factorial(n - k) for k in range(n + 1))

in_ra('khong chia het cho 3, 5, 7 tu 1 den 1000', ihl(1000, [3, 5, 7]), sum(1 for x in range(1, 1001) if x % 3 and x % 5 and x % 7))
for n in (7, 9):
    in_ra('D' + str(n), D(n), sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n))))
in_ra('toan anh 5 phan tu len 3 phan tu', 3 ** 5 - 3 * 2 ** 5 + 3 * 1 ** 5, sum(1 for f in product(range(3), repeat=5) if len(set(f)) == 3))
in_ra('so nguyen to cung nhau voi 360 trong 1..360', ihl(360, [2, 3, 5]), sum(1 for k in range(1, 361) if gcd(k, 360) == 1))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> đếm phần bù: tổng − (các tập đơn) + (giao hai tập) − (giao ba tập)… Số chia hết cho cả $a$ và $b$ (nguyên tố cùng nhau) là số chia hết cho $a \\times b$: <code>1000 // (3 * 5)</code>. '
    "$D_n$ cộng trừ xen kẽ các số hạng $\\binom{n}{k} (n-k)!$ (k từ 0 đến n). Hàm toàn ánh: tất cả hàm trừ các hàm bỏ sót ít nhất một giá trị. "
    "Lời giải ở <code>labs/DMS/L12/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, hãy đếm phần bù, lấy tổng trừ các tập đơn, cộng giao hai tập, trừ giao ba tập, và cứ thế. Số chia hết cho cả hai số nguyên tố cùng nhau là số chia hết cho tích của chúng. "
    "Hàm toàn ánh là tất cả các hàm trừ những hàm bỏ sót ít nhất một giá trị. "
    "Cú pháp liệt kê và đếm bộ thoả điều kiện được giải thích kèm ví dụ nhỏ trong đề.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_HTML, H_SAY, H_FOC = hint_parts2(HINT_BOX, HINT_SAY, [
    ("1000 // (3 * 5)", "<code>*</code> là nhân, <code>//</code> là chia lấy phần nguyên: đếm các số từ 1 đến 1000 chia hết cho 3 × 5 = 15", "1000 // 15 = 66"),
], [
    "Dấu sao là nhân, hai dấu gạch chéo là chia lấy phần nguyên, nên một nghìn chia lấy phần nguyên cho 15 đếm các số chia hết cho 15.",
], HINT_TAIL)

prac = practice(
    LID, "Tự làm: bao hàm–loại trừ cho ba tập, hoán vị không điểm cố định, hàm toàn ánh",
    "<p><b>Đề</b>: viết <code>baohamloaitru.py</code> giải năm bài đếm (số từ 1 đến 1 000 không chia hết cho 3, 5, 7; $D_7$; $D_9$; số hàm toàn ánh từ 5 phần tử lên 3 phần tử, tức hàm dùng mọi phần tử của tập đích ít nhất một lần; số k nguyên tố cùng nhau với 360). "
    "Mỗi dòng in kết quả bao hàm–loại trừ cạnh kết quả liệt kê hết; hai số phải bằng nhau (định dạng ở <code>labs/DMS/L12/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Dấu theo số tập trong giao: giao một tập trừ, hai tập cộng, ba tập trừ (khi đếm phần bù).</p>'
    '<p class="note"><b>Nguyên tố cùng nhau</b>: hai số có ước chung lớn nhất bằng 1, tức không số nào lớn hơn 1 chia hết cho cả hai. Ví dụ 8 và 15 thì có, 8 và 12 thì không (4 chia hết cho cả hai).</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình giải năm bài đếm bằng bao hàm loại trừ, rồi kiểm lại bằng cách liệt kê hết. "
    "Các bài gồm đếm số không chia hết cho ba số, và hoán vị không điểm cố định với 7 và 9 vật. "
    "Còn lại là đếm hàm toàn ánh, tức hàm dùng mọi phần tử của tập đích, và đếm số nguyên tố cùng nhau với 360. "
    "Hai số gọi là nguyên tố cùng nhau khi ước chung lớn nhất của chúng bằng một, nghĩa là không số nào lớn hơn một chia hết cho cả hai. "
    "Hai số ở mỗi dòng phải bằng nhau. Năm bài và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "baohamloaitru.py", H_HTML, H_SAY,
    pause=420, focus1=[1, 1, 1, 1, 3, 1, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "baohamloaitru.py")
prac["steps"][0]["introduces"] = ["dms_ntcn"]

OBJ = [
    "Áp dụng bao hàm–loại trừ cho ba tập và nhiều tập",
    "Nêu quy tắc dấu xen kẽ của bao hàm–loại trừ",
    "Đếm hoán vị không điểm cố định",
    "Đếm số cách trả mũ khi số người tăng và so liệt kê mọi cách với bao hàm–loại trừ",
    "Viết chương trình đếm bằng bao hàm–loại trừ và kiểm lại bằng cách liệt kê hết",
]
repl = [
    # fix6b (SHOULD): tổng xen kẽ bằng 1 với điều kiện m ≥ 1 và có lý do; bước chứng minh "không còn kiểu nào khác"
    ("Tổng đó luôn bằng 1, máy đã kiểm với m từ 1 đến 14.", "Tổng đó bằng 1 với mọi m từ 1 trở lên, vì khai triển một trừ một mũ m ra 0, và máy đã kiểm với m từ 1 đến 14."),
    ("= 1$ lần — máy kiểm $m$ từ 1 đến 14.", "= 1$ lần với mọi $m ≥ 1$ (vì khai triển $(1 - 1)^m = 0$) — máy kiểm $m$ từ 1 đến 14."),
    ("Không còn kiểu nào khác, vì nếu một người đứng riêng thì người đó nhận đúng mũ, nên tổng là 3 cộng 6, bằng 9, khớp với công thức.",
     "Không còn kiểu khác, vì mỗi nhóm đổi mũ có ít nhất 2 người, mà 4 chỉ tách thành 2 cộng 2 hoặc một nhóm 4, nên tổng là 3 cộng 6, bằng 9."),
    ('</td></tr></table>\n        focus: [1, "2.2", "2.3", "2.4"]',
     '</td></tr></table>\n          <p class="note">Không còn kiểu khác: mỗi nhóm đổi mũ vòng tròn có ít nhất 2 người, mà 4 = 2 + 2 hoặc 4.</p>\n        focus: [1, "2.2", "2.3", "2.4"]'),
    # fix12 (R8): ký hiệu ∪ đọc ra tại chỗ; "có … số chia hết" thay cho "là số chia hết" (nghĩa đen sai)
    ("+ |A \\cap B \\cap C|$</div>\n          <p>Từ 1 đến 100,",
     "+ |A \\cap B \\cap C|$<br><span class=\"note\">Dấu $\\cup$ đọc là “hợp”: $|A \\cup B \\cup C|$ là số phần tử thuộc <b>ít nhất một</b> trong ba tập.</span></div>\n          <p>Từ 1 đến 100,"),
    ("<p class=\"note\">16, 10, 6 là số chia hết cho 6, 10, 15; số 3 là số chia hết cho 30 (30, 60, 90).",
     "<p class=\"note\">Có 16, 10, 6 số chia hết cho 6, 10, 15; có 3 số chia hết cho 30 (30, 60, 90)."),
    ('focus: [1, 2, 3, 3]\n        say: "Với ba tập, ta cộng ba tập,', 'focus: [1, 1, 2, 3, 3]\n        say: "Dấu hợp cho số phần tử thuộc ít nhất một trong ba tập. Với ba tập, ta cộng ba tập,'),
    # fix12 (giữ ≤ 2 300 từ): rút gọn lời ở ba chỗ (số liệu vẫn trên màn hình)
    ("Ba vòng cắt nhau thành 7 vùng, và số trong mỗi vùng là đếm thẳng bằng máy, không qua công thức.", "Ba vòng cắt nhau thành 7 vùng, số trong mỗi vùng do máy đếm thẳng."),
    ("Vùng giữa chỉ có 3 số là 30, 60, 90, và nó nằm trong cả ba vòng, nên bị cộng ba lần, trừ ba lần, rồi phải cộng lại một lần.", "Vùng giữa có 3 số là 30, 60, 90, nằm trong cả ba vòng, nên bị cộng ba lần, trừ ba lần, rồi cộng lại một lần."),
    ("vì khai triển một trừ một mũ m ra 0, và máy đã kiểm với m từ 1 đến 14.", "vì khai triển một trừ một mũ m ra 0."),
    ("Bây giờ kiểm D bốn bằng đường khác, liệt kê thẳng, không dùng công thức.", "Bây giờ kiểm D bốn bằng cách liệt kê thẳng."),
    ("Các số 16, 10, 6 là số chia hết cho 6, 10 và 15. Số 3 là số chia hết cho cả ba, tức chia hết cho 30,", "Có 16, 10 và 6 số chia hết cho 6, 10 và 15. Có 3 số chia hết cho cả ba, tức chia hết cho 30,"),
]
f, _, _ = apply(LID, quiz_pause=30, objectives=OBJ,
                covers=[(1, "example"), (2, "general"), (3, "example"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                repl=repl + asr_keep(LID),
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"))
print(f)
print(ledger_sync(LID, claims={"quymo": "6 người: 265 cách, 8 người: 14 833 cách, đếm trực tiếp và bao hàm loại trừ đều khớp"}))
