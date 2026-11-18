"""DMS L01 → AF2 (WP5). Chạy: .venv/Scripts/python -B audit/dms/af2/l01.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L01"

QCODE = r"""def dung(x):
    return x <= 0 or x >= 10
def nham(x):
    return x < 0 or x > 10
lech = 0
for x in range(-50, 51):
    if dung(x) != nham(x):
        lech = lech + 1
print('thu 101 so, so lech:', lech)
print('thu ngau nhien so 32 bit can trung binh', 2 ** 32 // 2, 'lan')"""
QOUT = run_py(QCODE)
print(QOUT)

TAB = read_steps([
    ("def dung(x):", "định nghĩa một hàm tên dung nhận x; <code>return</code> ở dòng dưới là kết quả hàm đưa ra", "dung(10) đưa ra True (đúng)"),
    ("x <= 0 or x >= 10", "<code>&lt;=</code> nhỏ hơn hoặc bằng, <code>&gt;=</code> lớn hơn hoặc bằng, <code>or</code> là hoặc", "x = 10: so sánh sau đúng nên cả biểu thức đúng"),
    ("for x in range(-50, 51):", "với mỗi x trong các số nguyên từ −50 tới 50 (số sau không lấy), làm các dòng thụt vào bên dưới", "101 số, từ −50 đến 50"),
    ("if dung(x) != nham(x):", "<code>!=</code> là khác: nếu hai hàm cho kết quả khác nhau thì làm dòng thụt vào", "dung(0) là True, nham(0) là False: khác"),
    ("lech = lech + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng lech thêm 1", "lech đang là 1 thì thành 2"),
    ("2 ** 32 // 2", "<code>**</code> là lũy thừa, <code>//</code> là chia lấy phần nguyên", "2 ** 32 = 4294967296; chia 2 được 2147483648"),
    ("print(a, b)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "print('so lech:', 2) in ra so lech: 2"),
], "Chương trình sắp chạy dùng vài ký hiệu của ngôn ngữ lập trình, nên ta đọc trước.", [
    "Dòng đầu định nghĩa một hàm tên dung nhận x, và chữ trả về ở dòng dưới ghi kết quả hàm đưa ra.",
    "Dấu nhỏ hơn kèm bằng là nhỏ hơn hoặc bằng, dấu lớn hơn kèm bằng là lớn hơn hoặc bằng, và chữ giữa hai so sánh là hoặc.",
    "Dòng này là vòng lặp cho x chạy qua các số nguyên từ âm 50 tới 50, vì số sau trong ngoặc không được lấy, nên có đúng 101 giá trị.",
    "Dấu chấm than kèm bằng là khác, nên dòng này nghĩa là nếu hai hàm cho kết quả khác nhau thì làm dòng thụt vào.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hai dấu sao liền nhau là lũy thừa, hai dấu gạch chéo là chia lấy phần nguyên, nên 2 mũ 32 chia 2 được hơn hai tỉ.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=4, intro2="Tiếp theo là các ký hiệu còn lại của chương trình này.")

quymo = scene("quymo", "example", "Khi miền giá trị rất rộng: thử ngẫu nhiên bỏ sót lỗi ở biên", [
    *TAB,
    step(
        "<p><b>Chạy thật</b>: bản đúng (viết lại bằng De Morgan) so với bản nhầm (<code>x &lt; 0</code>, <code>x &gt; 10</code>)</p>"
        + run_html(QCODE, QOUT),
        "Đây là chương trình chạy thật. Hàm đầu là bản viết đúng bằng luật De Morgan, hàm sau là bản nhầm, thiếu dấu bằng. "
        "Vòng lặp thử 101 số nguyên từ âm 50 đến 50 và đếm số lần hai hàm cho kết quả khác nhau. Chỉ có hai số lệch, là 0 và 10. "
        "Còn mỗi lần thử ngẫu nhiên một số nguyên 32 bit, tức một trong hai mũ 32 giá trị, thì trung bình phải thử hơn hai tỉ lần mới gặp một trong hai số đó.",
        focus=[2, ["2.1", "2.4"], ["2.5", "2.8"], "4.1", "4.2"], clear=True),
    step(
        '<table class="t"><tr><th>cách kiểm</th><th>số trường hợp thử</th><th>bắt được lỗi ở 0 và 10?</th></tr>'
        "<tr><td>thử mọi số trong miền nhỏ</td><td>101</td><td>có, vì đã thử cả 0 và 10</td></tr>"
        "<tr><td>thử mọi số nguyên 32 bit</td><td>4 294 967 296</td><td>có, nhưng quá nhiều khi có hai biến (2<sup>64</sup> cặp)</td></tr>"
        "<tr><td>thử ngẫu nhiên vài nghìn số</td><td>vài nghìn</td><td>gần như không: mỗi lần thử chỉ trúng với xác suất 2 phần 2<sup>32</sup></td></tr>"
        "<tr><td>thử các giá trị ở biên: <b>0 và 10</b></td><td>2 đến 4</td><td>có, chỉ cần vài số</td></tr></table>"
        '<div class="box key">Điều kiện càng nhiều biến thì không gian thử càng nổ. Cách làm nghề: <b>biến đổi bằng luật</b> (chắc chắn) rồi <b>thử đúng các giá trị ở biên</b>.</div>',
        "Bảng này so sánh bốn cách kiểm. Thử hết thì chắc chắn, nhưng với hai biến số nguyên 32 bit đã là hai mũ 64 cặp, không thể thử. "
        "Thử ngẫu nhiên vài nghìn số gần như không bắt được lỗi ở biên. Người làm nghề chọn cách rẻ nhất mà chắc chắn, là biến đổi bằng luật rồi thử đúng các giá trị ở biên, chỉ cần vài số.",
        focus=[1, "1.3", "1.4", 2], clear=True),
], checks=[
    "[x for x in range(-50, 51) if (x <= 0 or x >= 10) != (x < 0 or x > 10)] == [0, 10]",
    "2 ** 32 == 4294967296 and 2 ** 32 // 2 == 2147483648 and 2 ** 64 == 18446744073709551616",
    "len(range(-50, 51)) == 101",
])

DE = """# Lab DMS L01 — Kiểm hai biểu thức có tương đương không bằng bảng chân trị

Viết `tuongduong.py` (Python 3.11 trở lên); chạy: `python tuongduong.py`.

Cho sẵn năm cặp biểu thức (chép nguyên đoạn này vào đầu tệp; `lambda` chỉ là cách viết một hàm ngắn trên một dòng, số đầu mỗi cặp là số thứ tự, số thứ hai là số mệnh đề):

```python
def keo(a, b):
    return (not a) or b

CAP = [
    (1, 2, lambda p, q: not (p and (not q)), lambda p, q: (not p) or q),
    (2, 2, lambda p, q: keo(p, q), lambda p, q: keo(q, p)),
    (3, 2, lambda p, q: keo(p, q), lambda p, q: keo(not q, not p)),
    (4, 3, lambda p, q, r: keo(p, keo(q, r)), lambda p, q, r: keo(p and q, r)),
    (5, 3, lambda p, q, r: keo(p, q) and keo(q, r), lambda p, q, r: keo(p, r)),
]
```

Với mỗi cặp, thử MỌI dòng của bảng chân trị (2 mũ n dòng; p đổi chậm nhất, bắt đầu từ đúng đúng...), rồi in một dòng:
- `<số thứ tự>: tuong duong` nếu hai biểu thức cùng chân trị ở mọi dòng;
- `<số thứ tự>: khong tuong duong, dong lech dau tien: <giá trị các mệnh đề, 1 là đúng 0 là sai, cách nhau một dấu cách>` nếu có dòng khác nhau (chỉ in dòng lệch ĐẦU TIÊN theo thứ tự trên).

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import product` ở đầu tệp: mượn một hàm có sẵn của Python tên `product`. Nó sinh mọi bộ giá trị: `product((True, False), repeat=2)` lần lượt cho `(True, True)`, `(True, False)`, `(False, True)`, `(False, False)` (đúng bốn dòng của bảng chân trị hai mệnh đề); `repeat=3` cho tám dòng.
- `for dong in product((True, False), repeat=n):` chạy vòng lặp qua từng dòng đó; mỗi `dong` là một bộ giá trị.
- `f(*dong)`: dấu `*` trước `dong` mở bộ giá trị thành từng đối số riêng. Nếu `dong` là `(True, False)` thì `f(*dong)` giống hệt `f(True, False)`.

Chấm: `bash labs/cham.sh DMS L01 tuongduong.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import product

def keo(a, b):
    return (not a) or b

CAP = [
    (1, 2, lambda p, q: not (p and (not q)), lambda p, q: (not p) or q),
    (2, 2, lambda p, q: keo(p, q), lambda p, q: keo(q, p)),
    (3, 2, lambda p, q: keo(p, q), lambda p, q: keo(not q, not p)),
    (4, 3, lambda p, q, r: keo(p, keo(q, r)), lambda p, q, r: keo(p and q, r)),
    (5, 3, lambda p, q, r: keo(p, q) and keo(q, r), lambda p, q, r: keo(p, r)),
]

for k, n, f, g in CAP:
    lech = None
    for dong in product((True, False), repeat=n):
        if f(*dong) != g(*dong):
            lech = dong
            break
    if lech is None:
        print(str(k) + ': tuong duong')
    else:
        print(str(k) + ': khong tuong duong, dong lech dau tien:', ' '.join(str(int(x)) for x in lech))"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: máy kiểm hai biểu thức có tương đương không",
    "<p><b>Đề</b>: viết <code>tuongduong.py</code> thử <b>mọi dòng</b> của bảng chân trị cho năm cặp biểu thức cho sẵn (đề đầy đủ và năm cặp ở <code>labs/DMS/L01/de.md</code>).</p>"
    "<p>Với mỗi cặp, in <code>tuong duong</code> hoặc in dòng lệch <b>đầu tiên</b> (1 là đúng, 0 là sai, mệnh đề đầu đổi chậm nhất).</p>"
    '<p class="note">Trong năm cặp có cả luật đúng và mệnh đề đảo. Số liệu khác ví dụ trong bài.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình thử mọi dòng của bảng chân trị cho năm cặp biểu thức cho sẵn trong đề. "
    "Với mỗi cặp, chương trình in là tương đương, hoặc in dòng lệch đầu tiên cùng giá trị các mệnh đề. "
    "Năm cặp và định dạng đầy đủ nằm trong thư mục thực hành. Hãy dừng video và tự làm, đừng chép lại ví dụ.",
    EXP, "tuongduong.py",
    '<div class="box key"><b>Nếu kẹt:</b> với mỗi cặp, <code>for dong in product((True, False), repeat=n)</code> cho mọi dòng. '
    "Nếu <code>f(*dong) != g(*dong)</code> thì ghi nhớ dòng đó rồi <code>break</code> (thoát ngay khỏi vòng lặp). Cuối vòng, chưa ghi nhớ dòng nào nghĩa là tương đương. "
    "Ba chỗ cú pháp mới (<code>import</code>, <code>repeat=n</code>, dấu <code>*</code>) được đọc ở bảng ngay sau. "
    "Lời giải ở <code>labs/DMS/L01/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, với mỗi cặp hãy duyệt mọi dòng của bảng bằng một vòng lặp. Gặp dòng mà hai biểu thức cho kết quả khác nhau thì ghi nhớ dòng đó và dừng. "
    "Cuối vòng, chưa ghi nhớ dòng nào nghĩa là hai biểu thức tương đương. "
    "Có ba chỗ cú pháp mới, được đọc ở bảng ngay sau. "
    "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=240, focus1=[1, 1, 2, 1, 0])
patch_cham(prac, LID, "tuongduong.py")
add_read_step(prac, [
    ("from itertools import product", "mượn một hàm làm sẵn tên <code>product</code>, đặt ở đầu tệp", "sau dòng này mới gọi được product(...)"),
    ("product((True, False), repeat=n)", "mọi bộ n giá trị, mỗi giá trị đúng hoặc sai (<code>repeat=n</code> là lặp n lần): đủ $2^n$ dòng của bảng chân trị", "repeat=2 cho 4 bộ: (True, True), (True, False), (False, True), (False, False)"),
    ("f(*dong)", "dấu <code>*</code> mở bộ giá trị thành từng đối số riêng", "dong = (True, False) thì f(*dong) giống f(True, False)"),
], "Ba chỗ cú pháp mới của lời giải đọc như sau.", [
    "Dòng đầu tệp mượn một hàm làm sẵn, tên ghi trên màn hình, và sau dòng đó ta mới gọi được hàm.",
    "Hàm này nhận hai giá trị đúng sai và số lần lặp n, rồi cho mọi bộ n giá trị, nên đủ 2 mũ n dòng của bảng chân trị.",
    "Dấu sao đứng trước tên biến mở một bộ giá trị thành từng đối số riêng của hàm.",
])

OBJ = [
    "Lập bảng chân trị để chứng minh hai biểu thức tương đương, hoặc tìm dòng cho thấy chúng không tương đương",
    "Dùng luật De Morgan để phủ định một điều kiện phức",
    "Phân biệt mệnh đề đảo và mệnh đề phản đảo",
    "Nêu vì sao thử ngẫu nhiên có thể bỏ sót lỗi ở biên của điều kiện, và vì sao phải thử đúng các giá trị ở biên",
]
repl = [
    ('say: "Chào bạn, đoạn mã này chặn người không đủ điều kiện vào cửa, tức là không đúng khi vừa đủ tuổi vừa có vé.',
     'say: "Chào bạn, đoạn mã này chặn người không đủ điều kiện vào cửa, trong đó dấu chấm than là không, hai dấu và là và, tức là không đúng khi vừa đủ tuổi vừa có vé.'),
    ("<b>lượng từ “với mọi”, “tồn tại”</b> — nói về cả một tập giá trị cùng lúc, và cách phủ định chúng.", "<b>“với mọi” và “tồn tại”</b> — nói về cả một tập giá trị cùng lúc, và cách phủ định chúng."),
    ("introduces: [equiv]", "introduces: [equiv, dms_tuongduong]"),
    ('        say: "Luật De Morgan có hai vế.', '        introduces: [dms_demorgan]\n        say: "Luật De Morgan gồm hai luật nhỏ.'),
    # fix6: mục asr_reviewed thêm tay sau AF2 (không có trong bản gốc) — giữ lại khi sinh lại
    ("asr_reviewed:\n", "asr_reviewed:\n" + '''  - {sentence: "Hàm đầu là bản viết đúng bằng luật De Morgan, hàm sau là bản nhầm, thiếu dấu bằng.", reason: "ASR chép “Hàm đầu là bản viết đúng bằng lược đơ mor gần, hàm sau là bản nhầm, thiếu dấu bằng.” (0.895): “de morgan” đọc theo luật lexicon (lexicon_vi.DMS.yaml: “Đơ Mo-gần”), ASR viết “mor”; lệch âm/thanh thuần Việt: luật/lược — NOT_VERIFIED bằng tai người"}''' + "\n"),
    # fix6 (R4 SHOULD): "vế" hai nghĩa trong cùng cảnh → "luật nhỏ" / "không p lẫn không q"
    ('{sentence: "Luật De Morgan có hai vế."', '{sentence: "Luật De Morgan gồm hai luật nhỏ."'),
    ("Ta kiểm vế thứ nhất của luật bằng bảng chân trị.", "Ta kiểm luật nhỏ thứ nhất bằng bảng chân trị."),
    ("cũng sai vì cả hai vế đều sai.", "cũng sai vì cả không p lẫn không q đều sai."),
    ('<p class="note">Vế thứ hai kiểm y hệt; máy đã kiểm đủ 4 dòng cho cả hai vế.</p>', '<p class="note">Luật nhỏ thứ hai kiểm y hệt; máy đã kiểm đủ 4 dòng cho cả hai luật.</p>'),
    ("Vế thứ hai kiểm y hệt, máy đã kiểm đủ bốn dòng cho cả hai vế.", "Luật nhỏ thứ hai kiểm y hệt, máy đã kiểm đủ bốn dòng cho cả hai luật."),
    ('        say: "Từ p kéo theo q, ta có thể đảo hai vế', '        introduces: [dms_phandao]\n        say: "Từ p kéo theo q, ta có thể đảo hai vế'),
    ('        say: "Câu hai, phản đảo là nếu n lẻ thì n không chia hết cho 4, đúng như câu gốc, vì phản đảo luôn tương đương với gốc. Còn đảo là nếu n chẵn thì chia hết cho 4, sai. Một phản ví dụ là 6,',
     '        introduces: [dms_phanvidu]\n        say: "Câu hai, phản đảo là nếu n lẻ thì n không chia hết cho 4, đúng như câu gốc, vì phản đảo luôn tương đương với gốc. Còn đảo là nếu n chẵn thì chia hết cho 4, sai. Ta cần một phản ví dụ, tức một trường hợp cụ thể làm câu sai, và 6 là một phản ví dụ,'),
]
f, _, _ = apply(LID, objectives=OBJ,
                covers=[(1, "practice"), (2, "example"), (3, "contrapositive"), (4, "quymo")],
                scenes=[(quymo, "pitfalls"), prac], repl=repl, assumes_add=("dms_menhde", "dms_bct"))
print(f)
print(ledger_sync(LID, claims={"quymo": "Chỉ có hai số lệch, là 0 và 10; thử ngẫu nhiên số nguyên 32 bit trung bình hơn hai tỉ lần mới gặp một trong hai số đó"}))
