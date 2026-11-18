"""DMS L03 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l03.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L03"

C1 = r"""for n in (10, 100, 1000):
    tong = 0
    dem = 0
    for a in range(1, n + 1, 2):
        for b in range(1, n + 1, 2):
            tong = tong + 1
            if (a + b) % 2 == 0:
                dem = dem + 1
    print(n, 'so: da thu', tong, 'cap, co', dem, 'cap tong chan')"""
O1 = run_py(C1)
print(O1)

TAB = read_steps([
    ("for n in (10, 100, 1000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 10, rồi 100, rồi 1000"),
    ("range(1, n + 1, 2)", "các số bắt đầu từ 1, mỗi lần tăng 2, dừng trước n + 1: đúng các số lẻ từ 1 tới n", "range(1, 8, 2) cho 1, 3, 5, 7"),
    ("if điều_kiện:", "<b>nếu</b> điều kiện đúng thì chạy các dòng thụt vào bên dưới, sai thì bỏ qua", "if 7 > 5: chạy; if 3 > 5: bỏ qua"),
    ("(a + b) % 2 == 0", "<code>%</code> là chia lấy <b>số dư</b>; <code>==</code> là <b>so sánh bằng</b>, cho đúng hoặc sai", "(3 + 5) % 2 == 0 là True"),
    ("tong = tong + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái; dòng này tăng tong thêm 1, dòng <code>dem = dem + 1</code> tăng dem thêm 1", "tong đang là 24 thì thành 25"),
    ("print(a, b)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "print(10, 'so') in ra 10 so"),
], "Chương trình đếm cặp số lẻ dùng sáu ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 10, 100, rồi 1000, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số với ba số trong ngoặc: bắt đầu từ 1, mỗi lần tăng 2, dừng trước n cộng 1, nên cho đúng các số lẻ từ 1 tới n.",
    "Chữ nếu kèm điều kiện nghĩa là: nếu điều kiện đúng thì chạy các dòng thụt vào bên dưới, còn sai thì bỏ qua.",
    "Dấu phần trăm là chia lấy số dư, hai dấu bằng liền nhau là so sánh bằng, nên tổng chia 2 dư 0 nghĩa là tổng chẵn.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên hai dòng này tăng hai biến đếm thêm một.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)

quymo = scene("quymo", "example", "Khi miền lớn dần: thử từng cặp không bao giờ xong, chứng minh thì có hạn", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: thử “tổng hai số lẻ là số chẵn” trên mọi cặp số lẻ trong khoảng từ 1 đến $n$</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Hai vòng lặp chạy qua mọi cặp số lẻ từ 1 đến n, và đếm các cặp có tổng chẵn. Với n bằng 10, máy thử 25 cặp. "
        "Với n bằng 100, máy thử 2 500 cặp. Với n bằng 1 000, máy thử 250 nghìn cặp. Mỗi lần n gấp mười, số cặp phải thử gấp một trăm lần, và lần nào cũng đều chẵn.",
        focus=[2, ["2.3", "2.5"], "4.1", "4.2", "4.3", 4], clear=True),
    step(
        '<table class="t"><tr><th>$n$</th><th>số cặp số lẻ cần thử</th><th>thời gian ở một tỉ cặp mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>1 000</td><td>250 000</td><td>chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>$10^6$</td><td>250 000 000 000</td><td>khoảng 4 phút</td></tr>"
        "<tr><td>$10^9$</td><td>250 000 000 000 000 000</td><td>khoảng 8 năm</td></tr>"
        "<tr><td>mọi số nguyên</td><td>vô hạn</td><td>không bao giờ xong</td></tr>"
        "<tr><td><b>chứng minh trực tiếp</b></td><td><b>3 bước</b></td><td><b>phủ mọi cặp</b></td></tr></table>"
        '<div class="box key">Thử càng nhiều càng tốn, mà vẫn chưa phủ hết. Biểu thức đầu bài đúng 40 lần rồi sai. Chứng minh thì chỉ vài dòng, và phủ <b>mọi</b> trường hợp.</div>',
        "Bảng này cho thấy cái giá của việc thử. Với n bằng một triệu, thử hết cần khoảng 4 phút, còn với n bằng một tỉ thì khoảng 8 năm, và với mọi số nguyên thì không bao giờ xong. "
        "Trong khi đó chứng minh trực tiếp chỉ có ba bước mà phủ mọi cặp. Người làm nghề dùng thử để tìm phản ví dụ nhanh, nhưng muốn khẳng định cho mọi trường hợp thì phải chứng minh.",
        focus=[1, "1.4", "1.6", 2], clear=True),
], checks=[
    "[sum(1 for a in range(1, n + 1, 2) for b in range(1, n + 1, 2) if (a + b) % 2 == 0) for n in (10, 100, 1000)] == [25, 2500, 250000]",
    "(10 ** 6 // 2) ** 2 == 250000000000 and (10 ** 9 // 2) ** 2 == 250000000000000000",
    "round((10 ** 6 // 2) ** 2 / 1e9 / 60, 1) == 4.2 and round((10 ** 9 // 2) ** 2 / 1e9 / 86400 / 365.25, 1) == 7.9",
    "(1000 // 2) ** 2 / 1e9 < 1e-3",
])

DE = """# Lab DMS L03 — Ví dụ không phải chứng minh: tìm phản ví dụ nhỏ nhất bằng chương trình

Viết `phanvidu.py` (Python 3.11 trở lên); chạy: `python phanvidu.py`.

Ba biểu thức sau cho ra số nguyên tố ở nhiều giá trị n đầu tiên (n = 0, 1, 2, ...), nhưng khẳng định "với mọi n tự nhiên, biểu thức là số nguyên tố" là SAI:

1. `n*n + n + 17`
2. `2*n*n + 29`
3. `n*n - 79*n + 1601`

Với mỗi biểu thức, tìm n nhỏ nhất làm giá trị KHÔNG phải số nguyên tố (giá trị lớn hơn 1 chỉ chia hết cho 1 và chính nó mới là nguyên tố), rồi in một dòng:

`<số thứ tự>: n=<n>, <giá trị> = <ước nhỏ nhất lớn hơn 1> x <thương>`

Ví dụ định dạng: `9: n=3, 45 = 3 x 15`.

Gợi ý: thử chia cho d = 2, 3, 4, ... cho tới khi `giá trị % d == 0`; vòng `for n in range(...)` bên ngoài, `break` khi gặp phản ví dụ đầu tiên.

Chấm: `bash labs/cham.sh DMS L03 phanvidu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""def uoc_nho_nhat(v):
    d = 2
    while d < v:
        if v % d == 0:
            return d
        d = d + 1
    return v

BIEU_THUC = [
    lambda n: n * n + n + 17,
    lambda n: 2 * n * n + 29,
    lambda n: n * n - 79 * n + 1601,
]

for k, f in enumerate(BIEU_THUC, start=1):
    n = 0
    while uoc_nho_nhat(f(n)) == f(n):
        n = n + 1
    v = f(n)
    d = uoc_nho_nhat(v)
    print(str(k) + ': n=' + str(n) + ', ' + str(v) + ' = ' + str(d) + ' x ' + str(v // d))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: tìm phản ví dụ nhỏ nhất cho ba biểu thức “luôn ra số nguyên tố”",
    "<p><b>Đề</b>: viết <code>phanvidu.py</code> tìm <b>n nhỏ nhất</b> làm mỗi biểu thức sau không còn là số nguyên tố: "
    "(1) $n^2 + n + 17$, (2) $2n^2 + 29$, (3) $n^2 - 79n + 1601$.</p>"
    "<p>In mỗi dòng <code>&lt;số&gt;: n=&lt;n&gt;, &lt;giá trị&gt; = &lt;ước nhỏ nhất&gt; x &lt;thương&gt;</code> (đề đầy đủ ở <code>labs/DMS/L03/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Mỗi dòng in ra là một phản ví dụ, nên khẳng định “với mọi n” bị bác bỏ.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình tìm n nhỏ nhất làm mỗi biểu thức trong đề không còn là số nguyên tố. "
    "Mỗi dòng in ra gồm n, giá trị của biểu thức, và một cách phân tích thành hai thừa số. Mỗi dòng như vậy là một phản ví dụ bác bỏ khẳng định với mọi n. Định dạng đầy đủ nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "phanvidu.py",
    '<div class="box key"><b>Nếu kẹt:</b> viết một hàm trả ước nhỏ nhất lớn hơn 1 của một số, thử chia cho 2, 3, 4, … Số là nguyên tố khi ước nhỏ nhất của nó chính là nó. '
    "Rồi cho n chạy từ 0 lên, dừng ở n đầu tiên mà giá trị không phải nguyên tố. Lời giải ở <code>labs/DMS/L03/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, hãy viết một hàm tìm ước nhỏ nhất lớn hơn một của một số, bằng cách thử chia cho 2, 3, 4 và cứ thế. Số là nguyên tố khi ước nhỏ nhất của nó chính là nó. "
    "Rồi cho n chạy từ 0 lên và dừng ở n đầu tiên làm giá trị không phải nguyên tố. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=240, focus1=[1, 2, 2, 3, 1, 0])
patch_cham(prac, LID, "phanvidu.py")

OBJ = [
    "Phân biệt ví dụ và chứng minh",
    "Viết chứng minh trực tiếp, chứng minh qua phản đảo, chứng minh phản chứng",
    "Nêu các bước chứng minh căn 2 là số vô tỉ bằng phản chứng",
    "Đếm số phép thử khi kiểm một khẳng định “với mọi” bằng cách thử từng trường hợp, và nêu vì sao chứng minh phủ mọi trường hợp mà thử thì không",
    "Viết chương trình tìm phản ví dụ nhỏ nhất cho một khẳng định “với mọi n”",
]
repl = [
    ('được 2 nhân a cộng b cộng 1. Bước ba', 'được 2 nhân tổng a cộng b cộng 1, tổng này đặt trong ngoặc. Bước ba'),
    ('        forward_ref: true\n        say: "Ở bài sau, bài 4, ta học quy nạp toán học', '        forward_ref: true\n        introduces: [dms_quynap]\n        say: "Ở bài sau, bài 4, ta học quy nạp toán học'),
    ('        focus: [1, "2.2", "2.2", "2.3", "2.4"]\n        say: "Định lý, tổng hai số lẻ là số chẵn. Bước một,',
     '        focus: [1, 1, "2.2", "2.2", "2.3", "2.4"]\n        introduces: [dms_dinhly, dms_giathiet]\n        say: "Định lý, tức một khẳng định đã được chứng minh, tổng hai số lẻ là số chẵn. Giả thiết là điều đã cho, kết luận là điều cần chứng minh. Bước một,'),
    # fix6 (R4 SHOULD): tối giản = không có ước chung lớn hơn 1
    ("phân số <b>tối giản</b> ($a$, $b$ không cùng chia hết cho 2 — rút gọn trước là được).", "phân số <b>tối giản</b> ($a$, $b$ không có ước chung lớn hơn 1, nên đặc biệt không cùng chẵn)."),
    ('{sentence: "Bước một, giả sử căn 2 bằng a chia b, với phân số đã rút gọn tối giản."', '{sentence: "Bước một, giả sử căn 2 bằng a chia b, với phân số tối giản, tức a và b không có ước chung nào lớn hơn 1, nên đặc biệt không cùng chẵn."'),
    ("Bước một, giả sử căn 2 bằng a chia b, với phân số đã rút gọn tối giản. Bước hai", "Bước một, giả sử căn 2 bằng a chia b, với phân số tối giản, tức a và b không có ước chung nào lớn hơn 1, nên đặc biệt không cùng chẵn. Bước hai"),
    (" Hẹn gặp bạn ở bài tiếp theo.", ""),
    # fix12 (R8 SHOULD): "số thực không thuộc Q"
    ("số không thuộc $\\mathbb{Q}$ gọi là số <b>vô tỉ</b>", "số thực không thuộc $\\mathbb{Q}$ gọi là số <b>vô tỉ</b>"),
    ("không thuộc tập Q, và ta gọi nó là số vô tỉ.", "không thuộc tập Q, và số thực như thế gọi là số vô tỉ."),
    # fix13 (item-verifier): ℚ gọi tên tại chỗ (chỉ đổi show, không đổi say)
    # fix13b: gộp vào đoạn sẵn có (không thêm khối) để không tràn khung
    ("(đọc “không thuộc”); số thực không thuộc", "(đọc “không thuộc”; $\\mathbb{Q}$ = các phân số $a/b$, $b \\ne 0$); số thực không thuộc"),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "verify"), (2, "example"), (3, "contradiction"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl, drop_asr=("Định lý, tổng hai số lẻ là số chẵn.",),
                assumes_add=("dms_menhde", "dms_bct", "dms_tuongduong", "dms_phandao", "dms_phanvidu", "dms_vitu", "dms_luongtu"))
print(f)
print(ledger_sync(LID, claims={"quymo": "n = 10 thử 25 cặp, n = 100 thử 2 500 cặp, n = 1 000 thử 250 nghìn cặp, lần nào cũng đều chẵn"}))
