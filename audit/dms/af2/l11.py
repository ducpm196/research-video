"""DMS L11 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l11.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L11"

C1 = r"""for n in (10, 100, 1000):
    dem = 0
    for a in range(n + 1):
        for b in range(n + 1 - a):
            dem = dem + 1
    print(n, 'vien, 3 ban:', dem, 'cach, cong thuc C(n+2, 2) =', (n + 2) * (n + 1) // 2)"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for n in (10, 100, 1000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 10, rồi 100, rồi 1000"),
    ("range(n + 1), range(n + 1 - a)", "<code>range(m)</code> cho các số từ 0 tới m − 1: <code>range(n + 1)</code> cho 0 tới n, <code>range(n + 1 - a)</code> cho 0 tới n − a", "n = 10, a = 4: b chạy 0, 1, …, 6"),
    ("dem = 0, dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái; dòng đầu đặt bộ đếm về 0, dòng sau tăng nó thêm 1", "dem đang là 27 thì thành 28"),
    ("(n + 2) * (n + 1) // 2", "<code>*</code> là nhân, <code>//</code> là chia lấy phần nguyên: công thức số cách viết bằng mã", "n = 10: 12 * 11 // 2 = 66"),
    ("print(n, 'vien, 3 ban:', dem, ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>C(n+2, 2)</code> trong dấu nháy chỉ là chữ được in ra", "print(10, 'vien', 66) in ra 10 vien 66"),
], "Chương trình đếm cách chia dùng năm ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 10, 100, rồi 1000, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số đếm từ 0 và dừng trước số trong ngoặc, nên n cộng 1 cho 0 tới n, còn n cộng 1 trừ a cho 0 tới n trừ a.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên một dòng đặt biến đếm về 0 và dòng kia tăng nó thêm một.",
    "Dấu sao là nhân, hai dấu gạch chéo là chia lấy phần nguyên, nên tích của n cộng 2 và n cộng 1, chia 2, cho đúng số cách theo công thức.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)

quymo = scene("quymo", "example", "Khi số bạn tăng: liệt kê từng cách chia không kịp, sao và vạch thì kịp", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: chia $n$ viên kẹo giống nhau cho 3 bạn, liệt kê từng cách (phần của An là $a$, của Bình là $b$, phần còn lại của Chi)</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Vòng lặp ngoài chọn phần của An, vòng lặp trong chọn phần của Bình, và phần của Chi là số kẹo còn lại, nên mỗi cách chia được đếm đúng một lần. "
        "Với 10 viên có 66 cách. Với 100 viên có 5 151 cách. Với 1 000 viên có hơn 500 nghìn cách. Cả ba lần khớp công thức sao và vạch, tổ hợp chập 2 của n cộng 2.",
        focus=[2, ["2.3", "2.4"], "4.1", "4.2", "4.3", 4], clear=True),
    step(
        '<table class="t"><tr><th>chia 100 viên kẹo cho $k$ bạn</th><th>số cách $\\binom{99+k}{k-1}$</th><th>liệt kê từng cách, một tỉ cách mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>$k = 3$</td><td>5 151</td><td>vài phần triệu giây</td></tr>"
        "<tr><td>$k = 5$</td><td>4 598 126</td><td>khoảng 5 phần nghìn giây</td></tr>"
        "<tr><td>$k = 10$</td><td>4 263 421 511 271</td><td>khoảng 71 phút</td></tr>"
        "<tr><td>$k = 20$</td><td>khoảng $4{,}9 \\times 10^{21}$</td><td>khoảng 156 000 năm</td></tr></table>"
        '<div class="box key">Thêm hộp làm số cách <b>bùng nổ</b>, nên liệt kê từng cách chỉ dùng được với cỡ nhỏ. Công thức sao và vạch cho đáp số trong <b>một phép tính</b>, kể cả khi liệt kê là không thể.</div>',
        "Bảng này giữ 100 viên kẹo và tăng số bạn. Với 10 bạn, liệt kê từng cách mất khoảng 71 phút, với 20 bạn thì khoảng một trăm năm mươi sáu nghìn năm. "
        "Còn công thức sao và vạch cho đáp số trong một phép tính. Người làm nghề dùng công thức để biết trước kích cỡ, và chỉ liệt kê khi số cách đủ nhỏ.",
        focus=[1, "1.4", "1.5", 2], clear=True),
], checks=[
    "[sum(1 for a in range(n + 1) for b in range(n + 1 - a)) for n in (10, 100, 1000)] == [66, 5151, 501501]",
    "[(n + 2) * (n + 1) // 2 for n in (10, 100, 1000)] == [66, 5151, 501501]",
    "[math.comb(99 + k, k - 1) for k in (3, 5, 10)] == [5151, 4598126, 4263421511271]",
    "4.9e21 < math.comb(119, 19) < 4.92e21 and round(math.comb(119, 19) / 1e9 / 31557600 / 1000) == 156",
    "round(math.comb(109, 9) / 1e9 / 60) == 71 and round(math.comb(104, 4) / 1e9, 3) == 0.005",
])

DE = """# Lab DMS L11 — Sao và vạch: đếm nghiệm và kiểm lại bằng cách liệt kê hết

Viết `saovach.py` (Python 3.11 trở lên); chạy: `python saovach.py`.

Với mỗi bài, in một dòng `<mô tả>: <công thức> <vét cạn>`: `<công thức>` là kết quả tính bằng sao và vạch (có thể dùng `from math import comb`; bài 4 dùng công thức "tổng trừ các trường hợp vi phạm"), `<vét cạn>` là kết quả đếm bằng cách liệt kê hết (dùng `itertools.product` hoặc `itertools.combinations_with_replacement`). Hai số phải bằng nhau.

Bốn dòng, đúng chữ (không dấu):
1. `x1+x2+x3+x4 = 7` — số nghiệm nguyên không âm
2. `x1+x2+x3 = 12, moi xi >= 2` — mỗi biến ít nhất 2 (đổi biến yi = xi − 2)
3. `chon 4 vien kem tu 6 vi` — chọn 4 viên kem từ 6 vị, được trùng vị, không kể thứ tự
4. `x1+x2+x3 = 10, moi xi <= 5` — số nghiệm nguyên không âm mà mọi biến không quá 5. Công thức: tổng số nghiệm không giới hạn, trừ đi số nghiệm có một biến từ 6 trở lên (có 3 cách chọn biến đó; không thể có hai biến cùng từ 6 trở lên vì khi đó tổng đã quá 10).

Ví dụ định dạng: `x1+x2 = 3: 4 4`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from math import comb` mượn hàm có sẵn: `comb(5, 2)` là tổ hợp chập 2 của 5, bằng 10.
- `from itertools import product, combinations_with_replacement` mượn hai hàm liệt kê. `product(range(3), repeat=2)` lần lượt cho mọi bộ hai số từ 0 đến 2: `(0, 0)`, `(0, 1)`, `(0, 2)`, `(1, 0)`, ... (9 bộ). `combinations_with_replacement('ab', 2)` cho `('a', 'a')`, `('a', 'b')`, `('b', 'b')`: chọn 2 phần tử, được lặp, không kể thứ tự.
- Đếm bộ thoả điều kiện: `sum(1 for x in product(range(8), repeat=4) if sum(x) == 7)` nghĩa là: với mỗi bộ `x`, nếu tổng các số trong `x` bằng 7 thì cộng thêm 1. Cách viết tương đương dài hơn: đặt `dem = 0`, vòng `for x in product(...)`, `if sum(x) == 7:`, `dem = dem + 1`. Dùng vòng lặp thường cũng được.

Chấm: `bash labs/cham.sh DMS L11 saovach.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from math import comb
from itertools import product, combinations_with_replacement

def in_ra(mo_ta, cong_thuc, vet_can):
    print(mo_ta + ':', cong_thuc, vet_can)

in_ra('x1+x2+x3+x4 = 7', comb(7 + 3, 3), sum(1 for x in product(range(8), repeat=4) if sum(x) == 7))
in_ra('x1+x2+x3 = 12, moi xi >= 2', comb(6 + 2, 2), sum(1 for x in product(range(13), repeat=3) if sum(x) == 12 and min(x) >= 2))
in_ra('chon 4 vien kem tu 6 vi', comb(4 + 5, 5), len(list(combinations_with_replacement(range(6), 4))))
in_ra('x1+x2+x3 = 10, moi xi <= 5', comb(12, 2) - 3 * comb(4 + 2, 2), sum(1 for x in product(range(11), repeat=3) if sum(x) == 10 and max(x) <= 5))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: đếm nghiệm bằng sao và vạch rồi kiểm bằng cách liệt kê hết",
    "<p><b>Đề</b>: viết <code>saovach.py</code> giải bốn bài đếm (nghiệm không âm, mỗi biến ít nhất 2, chọn kem có lặp, mỗi biến không quá 5). "
    "Mỗi dòng in kết quả công thức và kết quả liệt kê hết: hai số phải bằng nhau (định dạng ở <code>labs/DMS/L11/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Bài 4 có giới hạn trên: dùng tổng trừ các trường hợp vi phạm.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình giải bốn bài đếm, nghiệm không âm, mỗi biến ít nhất hai, chọn kem có lặp, và mỗi biến không quá năm. "
    "Mỗi dòng in kết quả của công thức sao và vạch cạnh kết quả liệt kê hết mọi trường hợp, và hai số phải bằng nhau. "
    "Bài bốn có giới hạn trên, nên dùng tổng số nghiệm trừ các trường hợp vi phạm. Định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "saovach.py",
    '<div class="box key"><b>Nếu kẹt:</b> $k$ ẩn tổng $n$: $\\binom{n+k-1}{k-1}$. Mỗi ẩn ít nhất $m$: trừ trước $m$ ở mỗi ẩn, còn $n - km$. '
    "Chọn có lặp $r$ vật từ $k$ loại là $\\binom{r+k-1}{k-1}$. Bài 4: $\\binom{12}{2}$ trừ $3 \\times$ số nghiệm có một biến từ 6 trở lên (đặt $y = x - 6$, tổng còn 4). "
    "Lời giải ở <code>labs/DMS/L11/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, k ẩn có tổng n thì số nghiệm là tổ hợp chập k trừ một của n cộng k trừ một. Mỗi ẩn ít nhất m thì trừ trước m ở mỗi ẩn. "
    "Với bài bốn, lấy tổng số nghiệm trừ ba lần số nghiệm có một biến từ sáu trở lên. "
    "Các hàm liệt kê có sẵn và cách đếm bộ thoả điều kiện được giải thích kèm ví dụ nhỏ trong đề, và bạn có thể dùng vòng lặp thường thay cho chúng. "
    "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=360, focus1=[1, 1, 1, 2, 1, 0])
patch_cham(prac, LID, "saovach.py")

OBJ = [
    "Đếm số cách chia vật giống nhau vào các hộp khác nhau",
    "Đếm nghiệm nguyên không âm của x₁ + … + x_k = n",
    "Đổi biến khi mỗi hộp phải có ít nhất một vật",
    "Đếm số cách chia khi số hộp tăng và nêu vì sao liệt kê từng cách chỉ dùng được với cỡ nhỏ",
    "Viết chương trình đếm bằng sao và vạch và kiểm lại bằng cách liệt kê hết",
]
f, _, _ = apply(LID, quiz_pause=30, objectives=OBJ, repl=asr_keep(LID),
                covers=[(1, "example"), (2, "example"), (3, "atleast"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac],
                assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"))
print(f)
print(ledger_sync(LID, claims={"quymo": "10 viên có 66 cách, 100 viên 5 151 cách, 1 000 viên 501 501 cách, khớp công thức sao và vạch"}))
