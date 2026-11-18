"""DMS L00 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l00.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa

LID = "L00"

# ── cảnh quy mô: số dòng bảng chân trị gấp đôi mỗi mệnh đề ──
QCODE = r"""for n in (10, 20):
    dong = 0
    for kieu in range(2 ** n):
        dong = dong + 1
    print(n, 'menh de:', dong, 'dong')
for n in (30, 60):
    print(n, 'menh de:', 2 ** n, 'dong,', 2 ** n // 10 ** 9, 'giay')"""
QOUT = run_py(QCODE)
print(QOUT)

TAB = read_step([
    ("for n in (10, 20):", "với mỗi n lần lượt bằng 10 rồi 20, làm các dòng thụt vào bên dưới", "n = 10 chạy một lượt, n = 20 chạy một lượt nữa"),
    ("dong = dong + 1", "một dấu bằng là <b>gán</b>: tính vế phải rồi cất vào tên bên trái, ở đây là tăng dong thêm 1", "dong đang là 4 thì thành 5"),
    ("2 ** n", "hai dấu sao liền nhau là lũy thừa, tức 2 mũ n", "2 ** 3 là 8"),
    ("range(m)", "các số 0, 1, … cho tới m − 1, nên vòng lặp chạy đúng m lượt", "range(3) cho 0, 1, 2"),
    ("print(a, b)", "in các giá trị ra cửa sổ, cách nhau một dấu cách; chữ trong dấu nháy in nguyên", "print(7, 'dong') in ra 7 dong"),
    ("a // b", "chia lấy phần nguyên, bỏ phần lẻ", "7 // 2 là 3"),
], "Trước khi chạy, ta đọc từng ký hiệu trong chương trình sắp hiện ra.", [
    "Dòng mở đầu vòng lặp đọc là: với mỗi n lần lượt bằng 10 rồi 20, làm các dòng thụt vào bên dưới.",
    "Một dấu bằng là gán: tính vế phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hai dấu sao liền nhau là lấy lũy thừa, nên 2 hai sao n đọc là 2 mũ n.",
    "Hàm tạo dãy số nhận m trong ngoặc và cho các số từ 0 tới m trừ 1, nên vòng lặp chạy đúng m lượt.",
    "Hàm in đưa các giá trị trong ngoặc ra cửa sổ, cách nhau một dấu cách, còn chữ trong dấu nháy in nguyên.",
    "Hai dấu gạch chéo là chia lấy phần nguyên, bỏ phần lẻ, nên 7 chia 2 được 3.",
])

quymo = scene("quymo", "example", "Khi số mệnh đề tăng: bảng chân trị gấp đôi mỗi lần thêm một mệnh đề", [
    TAB,
    step(
        "<p><b>Chạy thật</b>: đếm dòng bảng chân trị khi có 10, 20, 30, 60 mệnh đề (một tỉ dòng mỗi giây: số minh hoạ)</p>"
        + run_html(QCODE, QOUT),
        "Đây là chương trình chạy thật. Vòng lặp trong đếm từng kiểu đúng sai của n mệnh đề, và 2 mũ n chính là số dòng của bảng. Với 10 mệnh đề, máy đếm đúng 1 024 dòng. "
        "Với 20 mệnh đề là hơn một triệu dòng, máy vẫn đếm xong. Từ 30 mệnh đề ta không đếm nữa mà tính. "
        "Ba mươi mệnh đề cần khoảng một giây. Sáu mươi mệnh đề cần hơn một tỉ giây, tức khoảng ba mươi sáu năm rưỡi.",
        focus=[2, ["2.2", "2.4"], "4.1", "4.2", "2.7", "4.3", "4.4"],
        clear=True),
    step(
        '<table class="t"><tr><th>số mệnh đề $n$</th><th>số dòng $2^n$</th><th>thời gian ở một tỉ dòng mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>10</td><td>1 024</td><td>chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>20</td><td>1 048 576</td><td>khoảng một phần nghìn giây</td></tr>"
        "<tr><td>30</td><td>1 073 741 824</td><td>khoảng 1 giây</td></tr>"
        "<tr><td>60</td><td>1 152 921 504 606 846 976</td><td>khoảng 36,5 năm</td></tr></table>"
        '<div class="box key">Mỗi mệnh đề thêm vào làm số dòng <b>gấp đôi</b>. Liệt kê hết thì chắc chắn, nhưng chỉ dùng được khi có ít mệnh đề.</div>',
        "Bảng này cho thấy mỗi mệnh đề thêm vào làm số dòng gấp đôi. Cách liệt kê hết rất chắc chắn và chạy tốt khi có ít mệnh đề, nhưng với sáu mươi mệnh đề thì không còn khả thi. "
        "Người làm nghề phải chọn, lập bảng cho điều kiện nhỏ, còn điều kiện lớn thì dùng các luật biến đổi điều kiện, hoặc công cụ chuyên dụng, thay vì thử từng dòng.",
        focus=[2, "1.5", 2],
        clear=True),
], checks=[
    "2 ** 10 == 1024 and 2 ** 20 == 1048576 and 2 ** 30 == 1073741824",
    "2 ** 60 == 1152921504606846976 and 2 ** 60 // 10 ** 9 == 1152921504",
    "round(2 ** 60 / 1e9 / 86400 / 365.25, 1) == 36.5",
    "2 ** 10 / 1e9 < 1e-3 and round(2 ** 20 / 1e9, 3) == 0.001 and round(2 ** 30 / 1e9) == 1",
])

# ── lab ──
DE = """# Lab DMS L00 — Lập bảng chân trị bằng chương trình

Viết `bang.py` (Python 3.11 trở lên) rồi chạy trong Git Bash bằng `python bang.py`.

Biểu thức cần lập bảng: **(p và không q) hoặc r**. Trong Python viết `(p and not q) or r`.

In đúng ba phần, giá trị đúng viết **1**, sai viết **0**, các số cách nhau một dấu cách:
1. Dòng đầu: `p q r kq`
2. Tám dòng, mỗi dòng là giá trị của p, q, r rồi kết quả `kq`. Thứ tự dòng: p đổi chậm nhất, r đổi nhanh nhất; dòng đầu là `1 1 1 ...`, dòng cuối là `0 0 0 ...`.
3. Dòng cuối: `so dong dung: N` với N là số dòng có `kq` bằng 1.

Gợi ý: ba vòng `for` lồng nhau, mỗi vòng chạy trên `(1, 0)`; `int(True)` bằng 1 và `int(False)` bằng 0.

Chấm: `bash labs/cham.sh DMS L00 bang.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""dem = 0
print('p q r kq')
for p in (1, 0):
    for q in (1, 0):
        for r in (1, 0):
            kq = int((p == 1 and q == 0) or r == 1)
            print(p, q, r, kq)
            dem = dem + kq
print('so dong dung:', dem)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ("<div class=\"box key\"><b>Nếu kẹt:</b> ba vòng <code>for</code> lồng nhau, mỗi vòng chạy trên <code>(1, 0)</code> để p, q, r bắt đầu từ 1. "
            "Kết quả là <code>int((p == 1 and q == 0) or r == 1)</code>: vế đầu đúng khi p đúng mà q sai, vế sau đúng khi r đúng. "
            "Một biến <code>dem</code> cộng dồn các kết quả bằng 1. Lời giải ở <code>labs/DMS/L00/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, dùng ba vòng lặp lồng nhau, mỗi vòng chạy trên một và không, để p, q, r bắt đầu từ một. Kết quả là đúng khi p đúng mà q sai, hoặc khi r đúng. "
            "Một biến đếm cộng dồn các kết quả đúng. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("p == 1", "hai dấu bằng liền nhau là <b>so sánh</b>: hỏi “p có bằng 1 không”, kết quả đúng hoặc sai", "p = 1 thì đúng; p = 0 thì sai"),
    ("a and b, a or b", "và, hoặc: <code>and</code> đúng khi cả hai đúng, <code>or</code> đúng khi ít nhất một bên đúng", "đúng and sai là sai; đúng or sai là đúng"),
    ("int(x)", "đổi đúng thành 1, sai thành 0", "int(True) là 1, int(False) là 0"),
], [
    "Hai dấu bằng liền nhau là so sánh, hỏi p có bằng một không, và cho kết quả đúng hoặc sai.",
    "Hai từ khoá nối hai giá trị đúng sai đọc là và, hoặc: và đúng khi cả hai bên đúng, hoặc đúng khi ít nhất một bên đúng.",
    "Hàm này đổi giá trị đúng thành 1 và giá trị sai thành 0.",
], intro="Ba ký hiệu trong lời giải đọc như sau.")

prac = practice(
    LID, "Tự làm: lập bảng chân trị của (p và không q) hoặc r",
    "<p><b>Đề</b>: viết chương trình <code>bang.py</code> in bảng chân trị của <b>(p và không q) hoặc r</b> (số liệu khác ví dụ trong bài).</p>"
    "<p>In dòng <code>p q r kq</code>, rồi 8 dòng, mỗi dòng là p, q, r và kết quả (1 là đúng, 0 là sai; p đổi chậm nhất, bắt đầu từ <code>1 1 1</code>), "
    "cuối cùng dòng <code>so dong dung: N</code>.</p>"
    '<p class="note">Đề đầy đủ ở <code>labs/DMS/L00/de.md</code>.</p>'
    '<p class="note">Cách chạy: mở cửa sổ Git Bash (dòng lệnh đi kèm Git), đi tới thư mục có tệp, gõ <code>python bang.py</code> rồi Enter. '
    'Python đọc tệp <code>.py</code> và chạy từng dòng từ trên xuống; kết quả hiện ngay trong cửa sổ.</p>',
    "Bây giờ tới phần bạn tự làm, với biểu thức mới là p và không q, hoặc r. Hãy viết chương trình in ra tám dòng của bảng chân trị, "
    "mỗi dòng gồm p, q, r và kết quả, một là đúng, không là sai. Cuối cùng in số dòng cho kết quả đúng. Đề đầy đủ nằm trong thư mục thực hành. "
    "Để chạy, mở cửa sổ dòng lệnh, đi tới thư mục có tệp, gõ lệnh chạy kèm tên tệp, rồi máy đọc từng dòng từ trên xuống. "
    "Hãy dừng video và tự làm, đừng chép lại ví dụ.",
    EXP, "bang.py", H_HTML, H_SAY,
    pause=240, focus1=[1, 1, 2, 3, 4, 0], focus3=H_FOC)
patch_cham(prac, LID, "bang.py")

# ── sửa chữ ──
HOOK_OLD = """      - show: |
          <p>Hôm nay: <b>mệnh đề</b> là gì, năm phép toán ghép mệnh đề, và cách dùng <b>bảng chân trị</b> để trả lời chắc chắn.</p>
        say: "Hôm nay ta học mệnh đề là gì, năm phép toán ghép các mệnh đề lại, và cách dùng bảng chân trị để trả lời câu hỏi đó một cách chắc chắn.\""""
HOOK_NEW = """      - show: |
          <p>Hôm nay: <b>mệnh đề</b> (câu khẳng định nói được là đúng hay sai), năm phép toán ghép mệnh đề, và <b>bảng chân trị</b> (bảng liệt kê mọi khả năng đúng sai, kèm kết quả) để trả lời chắc chắn.</p>
        introduces: [dms_menhde, dms_bct]
        say: "Hôm nay ta học ba việc. Mệnh đề, là một câu khẳng định mà ta nói được là đúng hay sai. Năm phép toán ghép các mệnh đề lại với nhau. Và bảng chân trị, là bảng liệt kê mọi khả năng đúng sai rồi ghi kết quả ở từng dòng, để trả lời câu hỏi đầu bài một cách chắc chắn.\""""

OBJ = [
    "Nhận biết một câu có phải mệnh đề không",
    "Lập bảng chân trị cho phủ định, và, hoặc, kéo theo, khi và chỉ khi",
    "Nêu vì sao p → q đúng khi p sai",
    "Đếm số dòng của bảng chân trị là 2 mũ n và nêu vì sao liệt kê hết bảng không còn khả thi khi có hàng chục mệnh đề",
    "Viết chương trình in bảng chân trị của một biểu thức và đếm số dòng cho kết quả đúng",
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "sym_prop"), (2, "example"), (3, "implication"), (4, "quymo"), (5, "practice")],
                scenes=[quymo, prac], repl=[(HOOK_OLD, HOOK_NEW),
                      ("<b>tương đương lôgic và luật De Morgan</b> — biến đổi điều kiện mà không đổi nghĩa.", "<b>biến đổi một điều kiện</b> mà không đổi nghĩa, và khi nào hai biểu thức luôn cùng chân trị."),
                      ("ta học khi nào hai biểu thức là tương đương, và các luật", "ta học khi nào hai biểu thức luôn cùng chân trị, và các luật")])
print(f)
print(ledger_sync(LID, claims={"quymo": "Với 10 mệnh đề, máy đếm đúng 1 024 dòng; 30 mệnh đề cần khoảng một giây; 60 mệnh đề khoảng ba mươi sáu năm rưỡi (số minh hoạ)"}))
