"""DMS L02 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l02.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L02"

C1 = r"""for n in (10, 100, 1000):
    dem = 0
    for x in range(n):
        for y in range(n):
            dem = dem + 1
            if y > x:
                break
    print(n, dem)"""
O1 = run_py(C1)
C2 = r"""for n in (10, 100):
    ket_qua = all(any(y > x for y in range(n)) for x in range(n))
    print(n, ket_qua)"""
O2 = run_py(C2)
print(O1, O2, sep="\n")

TAB1 = read_step([
    ("for n in (10, 100, 1000):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "ba lượt: n = 10, rồi 100, rồi 1000"),
    ("range(n)", "các số từ 0 tới n − 1, đúng n giá trị", "range(4) cho 0, 1, 2, 3"),
    ("dem = dem + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng dem thêm 1", "dem đang là 6 thì thành 7"),
    ("if y > x:", "nếu y lớn hơn x thì làm dòng thụt vào bên dưới", "y = 5, x = 3: làm; y = 2, x = 3: bỏ qua"),
    ("break", "dừng ngay vòng lặp đang chạy", "đã tìm được y lớn hơn x thì khỏi thử tiếp"),
    ("print(n, dem)", "in n và dem ra cửa sổ, cách nhau một dấu cách", "print(10, 64) in ra 10 64"),
], "Chương trình đếm này dùng sáu ký hiệu, ta đọc từng cái.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 10, 100, rồi 1000, làm các dòng thụt vào bên dưới.",
    "Hàm tạo dãy số cho các số từ 0 tới n trừ 1, nên có đúng n giá trị.",
    "Một dấu bằng là gán, nên dòng này cộng thêm một vào biến đếm.",
    "Nếu y lớn hơn x thì làm dòng thụt vào bên dưới.",
    "Lệnh thoát vòng dừng ngay vòng lặp đang chạy, vì đã tìm được y lớn hơn x thì khỏi thử tiếp.",
    "Hàm in đưa n và biến đếm ra cửa sổ, cách nhau một dấu cách.",
])
TAB2 = read_step([
    ("any(y > x for y in range(n))", "<b>tồn tại</b>: đúng khi có ít nhất một y trong miền làm <code>y &gt; x</code> đúng", "any(y > 5 for y in range(4)) là False"),
    ("all(... for x in range(n))", "<b>với mọi</b>: đúng khi mọi x trong miền đều làm biểu thức bên trong đúng", "all(x < 4 for x in range(4)) là True"),
], "Chương trình thứ hai dùng hai hàm làm sẵn, tên ghi trên màn hình.", [
    "Hàm đầu đúng khi có ít nhất một y trong miền làm y lớn hơn x đúng, tức là tồn tại.",
    "Hàm sau đúng khi mọi x trong miền đều làm biểu thức bên trong đúng, tức là với mọi.",
])

quymo = scene("quymo", "example", "Khi miền lớn dần: hai lượng từ lồng nhau tốn bình phương số phép thử", [
    TAB1,
    step(
        "<p><b>Chạy thật</b>: câu “với mọi $x$ tồn tại $y$ lớn hơn $x$” — đếm số phép so sánh <code>y &gt; x</code> trên miền $0, 1, \\dots, n-1$</p>"
        + run_html(C1, O1, "Số phép so sánh"),
        "Đây là chương trình chạy thật. Với mỗi x, vòng lặp trong đi tìm một y lớn hơn x. "
        "Miền có 10 số thì tốn 64 phép so sánh. Miền gấp mười lần, 100 số, tốn 5 149 phép. Miền 1 000 số tốn hơn 500 nghìn phép, tức gấp khoảng một trăm lần khi miền gấp mười lần.",
        focus=[2, "2.4", "4.1", "4.2", "4.3"], clear=True),
    TAB2,
    step(
        "<p>Cùng câu đó, hai hàm <code>all</code> (với mọi) và <code>any</code> (tồn tại) trên miền hữu hạn:</p>" + run_html(C2, O2, "Chân trị"),
        "Mỗi hàm thử lần lượt từng phần tử của miền, và câu này cho kết quả sai ở cả hai kích thước. "
        "Vì số lớn nhất của miền, 9 hoặc 99, không có số nào lớn hơn nó trong miền. Trên tập số tự nhiên vô hạn, câu này đúng, vì luôn chọn được x cộng 1.",
        focus=["2.2", 4, 1], clear=True),
    step(
        '<table class="t"><tr><th>miền</th><th>số phép so sánh</th><th>chân trị của câu</th></tr>'
        "<tr><td>10 số</td><td>64</td><td>sai</td></tr><tr><td>100 số</td><td>5 149</td><td>sai</td></tr><tr><td>1 000 số</td><td>501 499</td><td>sai</td></tr>"
        "<tr><td>tập số tự nhiên $\\mathbb{N}$ vô hạn</td><td>không thử hết được</td><td>đúng (chứng minh: chọn $y = x + 1$)</td></tr></table>"
        '<div class="box key">Máy chỉ kiểm được miền <b>hữu hạn</b>, và có hai bài học: chi phí tăng theo <b>bình phương</b> khi lồng hai lượng từ, và đáp số trên miền hữu hạn có thể <b>khác</b> miền vô hạn.</div>',
        "Bảng này gom lại hai bài học. Một, hai lượng từ lồng nhau làm số phép thử tăng theo bình phương, miền gấp mười lần thì tốn gấp khoảng một trăm lần. "
        "Hai, máy chỉ kiểm được miền hữu hạn, và đáp số có thể khác miền vô hạn. Người làm nghề chọn miền thử cho đúng đề bài, và muốn khẳng định cho tập vô hạn thì phải chứng minh.",
        focus=[1, 1, 2, 2], clear=True),
], checks=[
    "sum(min(x + 2, 10) for x in range(10)) == 64",
    "(lambda n: sum(min(x + 2, n) for x in range(n)))(100) == 5149",
    "(lambda n: sum(min(x + 2, n) for x in range(n)))(1000) == 501499",
    "all(not any(y > x for y in range(n)) for n in (10, 100) for x in [n - 1])",
])

DE = """# Lab DMS L02 — Kiểm câu có lượng từ trên một miền hữu hạn

Viết `luongtu.py` (Python 3.11 trở lên); chạy: `python luongtu.py`.

Miền: `D = range(20)`, tức các số tự nhiên 0, 1, ..., 19. Với mỗi câu dưới đây, in đúng một dòng:

| số | câu | in ra |
|---|---|---|
| 1 | với mọi x trong D: x·x > x | `1: dung` nếu đúng; nếu sai: `1: sai, phan vi du x=<giá trị nhỏ nhất làm câu sai>` |
| 2 | tồn tại x trong D: x·x = 2x + 3 | nếu đúng: `2: dung, vi du x=<giá trị nhỏ nhất>`; nếu sai: `2: sai` |
| 3 | với mọi x trong D tồn tại y trong D: x + y = 19 | `3: dung` hoặc `3: sai` |
| 4 | tồn tại y trong D với mọi x trong D: x + y = 19 | `4: dung` hoặc `4: sai` |
| 5 | với mọi x trong D tồn tại y trong D: y > x | `5: dung` nếu đúng; nếu sai: `5: sai, phan vi du x=<giá trị nhỏ nhất của x không có y>` |

Gợi ý: `all(...)` là "với mọi", `any(...)` là "tồn tại"; câu 3 và 4 chỉ khác thứ tự lượng từ. Phản ví dụ: danh sách `[x for x in D if not (...)]`, lấy phần tử đầu.

Chấm: `bash labs/cham.sh DMS L02 luongtu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""D = range(20)

x1 = [x for x in D if not x * x > x]
print('1: sai, phan vi du x=' + str(x1[0]) if x1 else '1: dung')
x2 = [x for x in D if x * x == 2 * x + 3]
print('2: dung, vi du x=' + str(x2[0]) if x2 else '2: sai')
print('3:', 'dung' if all(any(x + y == 19 for y in D) for x in D) else 'sai')
print('4:', 'dung' if any(all(x + y == 19 for x in D) for y in D) else 'sai')
x5 = [x for x in D if not any(y > x for y in D)]
print('5: sai, phan vi du x=' + str(x5[0]) if x5 else '5: dung')"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> “với mọi” là <code>all(... for x in D)</code>, “tồn tại” là <code>any(... for x in D)</code>; phần <code>for x in D</code> nghĩa là thử lần lượt từng <code>x</code> của <code>D</code>. '
            "Câu 3 là <code>all(any(...))</code>, câu 4 là <code>any(all(...))</code>. Phản ví dụ nhỏ nhất: <code>[x for x in D if not (điều kiện)][0]</code>. "
            "Lời giải ở <code>labs/DMS/L02/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, với mọi và tồn tại đều có hàm làm sẵn, nhận một biểu thức thử lần lượt từng phần tử của miền. "
            "Phản ví dụ nhỏ nhất lấy từ danh sách các x làm điều kiện sai. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("all(... for x in D)", "<b>với mọi</b>: đúng khi mọi x của D đều làm biểu thức đúng", "all(x < 3 for x in range(3)) là True"),
    ("any(... for x in D)", "<b>tồn tại</b>: đúng khi ít nhất một x của D làm biểu thức đúng", "any(x == 2 for x in range(3)) là True"),
    ("[x for x in D if not (cond)][0]", "danh sách các x của D làm điều kiện cond <b>sai</b>; <code>[0]</code> lấy phần tử đầu, tức phản ví dụ nhỏ nhất", "[x for x in range(5) if not (x < 3)][0] là 3"),
], [
    "Hàm đầu đúng khi mọi x của miền làm biểu thức đúng, tức là với mọi.",
    "Hàm sau đúng khi ít nhất một x của miền làm biểu thức đúng, tức là tồn tại.",
    "Dòng cuối dựng danh sách các x làm điều kiện sai, rồi lấy phần tử đầu bằng số 0 trong ngoặc vuông, tức phản ví dụ nhỏ nhất.",
])

prac = practice(
    LID, "Tự làm: máy kiểm năm câu có lượng từ trên miền 0 đến 19",
    "<p><b>Đề</b>: viết <code>luongtu.py</code> kiểm năm câu có “với mọi”, “tồn tại” trên miền <code>D = range(20)</code> (bảng năm câu và định dạng ở <code>labs/DMS/L02/de.md</code>).</p>"
    "<p>Câu 3 và câu 4 chỉ khác thứ tự lượng từ: dự đoán trước xem chúng có cùng chân trị không, rồi để máy trả lời.</p>"
    '<p class="note">Số liệu khác ví dụ trong bài.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình kiểm năm câu có với mọi và tồn tại trên miền các số từ 0 đến 19. Bảng năm câu và định dạng in nằm trong thư mục thực hành. "
    "Câu ba và câu bốn chỉ khác thứ tự lượng từ, hãy dự đoán trước chúng có cùng chân trị không, rồi để máy trả lời. Hãy dừng video và tự làm.",
    EXP, "luongtu.py", H_HTML, H_SAY,
    pause=240, focus1=[1, 1, 2, 2, 0], focus3=H_FOC)
patch_cham(prac, LID, "luongtu.py")

OBJ = [
    "Đọc và viết câu có “với mọi”, “tồn tại”",
    "Phủ định một câu có lượng từ",
    "Nhận ra miền xác định và thứ tự lượng từ làm đổi chân trị",
    "Đếm số phép thử khi kiểm câu có hai lượng từ lồng nhau trên miền lớn dần, và nêu vì sao đáp số trên miền hữu hạn có thể khác miền vô hạn",
    "Viết chương trình kiểm câu có lượng từ trên một miền hữu hạn và tìm phản ví dụ",
]
repl = [
    ('say: "Trong một số ngôn ngữ lập trình có sẵn hai hàm, trên một danh sách hữu hạn, hàm đầu tiên trên màn hình chính là với mọi, hàm thứ hai chính là tồn tại. Kiểm mọi số từ 0 đến 9999, x bình phương lớn hơn hoặc bằng x luôn đúng.',
     'say: "Trong một số ngôn ngữ lập trình có sẵn hai hàm, trên một danh sách hữu hạn, hàm đầu tiên trên màn hình chính là với mọi, hàm thứ hai chính là tồn tại. Phần lặp theo x trong khoảng từ 0 đến 9999 thử lần lượt từng x, và x bình phương lớn hơn hoặc bằng x luôn đúng.'),
    ('        say: "Câu có chứa biến gọi là vị từ,', '        introduces: [dms_vitu]\n        say: "Câu có chứa biến gọi là vị từ,'),
    ("introduces: [forall, exists]", "introduces: [forall, exists, dms_luongtu]"),
    # fix4 (R2 SHOULD): "miền" giảng thẳng
    ("(vì $x = \\frac{1}{2}$).</div>\n", "(vì $x = \\frac{1}{2}$).</div>\n          <p class=\"note\"><b>Miền</b> là tập các giá trị mà $x$ được phép nhận (ở đây $\\mathbb{N}$ hoặc $\\mathbb{Q}$).</p>\n"),
    ('        say: "Quay lại câu đầu bài.', '        focus: [1, 1, 1, 2, 1]\n        say: "Quay lại câu đầu bài.'),
    # fix6 (R4): "phản ví dụ" định nghĩa tại chỗ ở verify.0
    ("Muốn chứng tỏ với mọi là sai, cũng chỉ cần một phản ví dụ. Nhưng", "Muốn chứng tỏ với mọi là sai, cũng chỉ cần một phản ví dụ, tức một giá trị cụ thể làm câu sai. Nhưng"),
    ("<td>chỉ ra <b>một</b> phản ví dụ</td>", "<td>chỉ ra <b>một</b> phản ví dụ (một giá trị làm câu sai)</td>"),
    ("vì x bằng một phần hai làm Q sai. Cùng một vị từ, đổi miền là đổi chân trị.",
     "vì x bằng một phần hai làm Q sai. Ở đây miền là tập các giá trị mà x được phép nhận, tức N hoặc Q. Cùng một vị từ, đổi miền là đổi chân trị."),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "example"), (2, "negation"), (3, "order"), (4, "quymo"), (5, "practice")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl,
                assumes_add=("dms_menhde", "dms_bct", "dms_tuongduong", "dms_demorgan", "dms_phanvidu", "dms_phandao"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Miền 10 số tốn 64 phép so sánh, 100 số tốn 5 149, 1 000 số hơn 500 nghìn; câu cho kết quả sai trên miền hữu hạn"}))
