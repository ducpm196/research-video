"""DMS L16 → AF2 (WP5 phiên 2). Bài sinh từ MẪU audit/dms/src/L16_*.tpl.yaml. Chạy: .venv/Scripts/python -B audit/dms/af2/l16.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L16"

C1 = r"""for n in (11, 1001):
    bac = [0] * n
    for u in range(n):
        for v in range(u + 1, n):
            bac[u] = bac[u] + 1
            bac[v] = bac[v] + 1
    le = sum(1 for b in bac if b % 2)
    print(n, 'dinh: tong bac', sum(bac), ', canh', n * (n - 1) // 2, ', bac le', le)"""
O1 = run_py(C1)
print(O1)

TAB_A = read_step([
    ("for n in (11, 1001):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "hai lượt: n = 11, rồi 1001"),
    ("bac = [0] * n", "ngoặc vuông tạo một danh sách; nhân danh sách với n là lặp nó n lần, thành n số 0; <code>bac[i]</code> sẽ là bậc của đỉnh i (đếm từ 0)", "n = 3: bac = [0, 0, 0]"),
    ("for u in range(n): for v in range(u + 1, n):", "<code>range(n)</code> cho 0 tới n − 1; <code>range(u + 1, n)</code> cho u + 1 tới n − 1: mỗi cặp đỉnh (u, v) đúng một lần", "n = 4, u = 1: v = 2, 3"),
    ("bac[u] = bac[u] + 1", "<code>bac[u]</code> là phần tử thứ u của danh sách; một dấu bằng là <b>gán</b>: tăng bậc đỉnh u thêm 1", "bac = [0, 0, 0], u = 0: thành [1, 0, 0]"),
], "Chương trình đếm bậc dùng bảy ký hiệu, ta đọc bốn cái đầu trước.", [
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 11 rồi 1001, làm các dòng thụt vào bên dưới.",
    "Ngoặc vuông tạo một danh sách, và nhân danh sách với n là lặp nó n lần, nên đây là n số không, mỗi số là bậc của một đỉnh.",
    "Hai vòng lặp lồng nhau cho mỗi cặp đỉnh đúng một lần, vì đỉnh thứ hai chỉ chạy từ đỉnh sau đỉnh thứ nhất tới hết.",
    "Số trong ngoặc vuông chỉ phần tử thứ u của danh sách, và dấu bằng là gán, nên dòng này tăng bậc của đỉnh u thêm một.",
])

TAB_B = read_step([
    ("sum(1 for b in bac if b % 2)", "<code>b % 2</code> là số dư khi chia b cho 2, bằng 1 khi b lẻ; với mỗi b có số dư khác 0 thì cộng 1, tức đếm các đỉnh bậc lẻ", "bac = [3, 2, 3, 2]: đếm được 2"),
    ("n * (n - 1) // 2", "<code>*</code> là nhân, <code>//</code> là chia lấy phần nguyên: số cạnh của đồ thị đầy đủ", "n = 11: 11 * 10 // 2 = 55"),
    ("print(n, 'dinh: tong bac', sum(bac), ...)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách; <code>sum(bac)</code> là tổng các số trong bac", "in ra 11 dinh: tong bac 110 …"),
], "Ba ký hiệu còn lại nằm ở dòng đếm đỉnh lẻ và dòng in kết quả.", [
    "Dấu phần trăm là chia lấy số dư, nên biểu thức này cộng một cho mỗi bậc có số dư khác không, tức đếm các đỉnh bậc lẻ.",
    "Dấu sao là nhân, hai dấu gạch chéo là chia lấy phần nguyên, nên biểu thức này cho số cạnh của đồ thị đầy đủ.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách, và hàm tính tổng cộng các số trong danh sách.",
])

quymo = scene("quymo", "example", "Khi đồ thị lớn dần: kiểm Euler bằng bậc rất rẻ, đi qua mọi đỉnh thì không kịp", [
    step(
        "<p><b>Chạy thật</b>: đếm bậc trong đồ thị đầy đủ $n$ đỉnh ($n$ lẻ): mọi cặp đỉnh nối nhau bằng một cạnh</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật, trên đồ thị đầy đủ, tức mọi cặp đỉnh nối nhau bằng một cạnh. Với mỗi cặp đỉnh, ta có một cạnh, và mỗi cạnh cộng một vào bậc của cả hai đầu. "
        "Với 11 đỉnh có 55 cạnh, tổng bậc là 110, đúng bằng hai lần số cạnh. Với 1 001 đỉnh có hơn nửa triệu cạnh. "
        "Cả hai lần, không đỉnh nào bậc lẻ, nên đồ thị có chu trình Euler.",
        focus=[2, ["2.3", "2.6"], "4.1", "4.2", 4], clear=True),
    step(
        '<p>$n!$ (đọc “n giai thừa”) là tích $1 \\times 2 \\times \\dots \\times n$, ví dụ $5! = 120$.</p>'
        '<table class="t"><tr><th>số đỉnh $n$ (cạnh lấy ví dụ ở đồ thị đầy đủ)</th><th>kiểm Euler: đọc $m$ cạnh vài lượt (đếm bậc, kiểm liên thông)</th><th>tìm chu trình qua mọi đỉnh bằng cách thử mọi thứ tự đỉnh: trường hợp xấu nhất cỡ $(n-1)!/2$ thứ tự (đồ thị bất kỳ $n$ đỉnh), một tỉ thứ tự mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>11</td><td>55 cạnh</td><td>1 814 400 thứ tự, khoảng 2 phần nghìn giây</td></tr>"
        "<tr><td>21</td><td>210 cạnh</td><td>khoảng $1{,}2 \\times 10^{18}$ thứ tự, khoảng 39 năm</td></tr>"
        "<tr><td>101</td><td>5 050 cạnh</td><td>cỡ $10^{157}$ thứ tự, không bao giờ xong</td></tr></table>"
        '<div class="box key">Kiểm Euler chỉ cần <b>đọc danh sách cạnh vài lượt</b> (đếm bậc, kiểm liên thông). Chu trình qua mọi đỉnh (Hamilton) chưa có cách kiểm nhanh cho mọi đồ thị; thử mọi thứ tự tăng theo <b>giai thừa</b>. Một điều kiện đếm được như tính chẵn lẻ của bậc đáng giá hơn nhiều so với tìm kiếm vét cạn (thử hết mọi khả năng).</div>',
        "Ký hiệu n giai thừa, viết n kèm dấu chấm than, là tích 1 nhân 2 nhân tiếp tới n, ví dụ 5 giai thừa bằng 120. Bảng này so hai bài toán nghe giống nhau. Kiểm có đường đi qua mọi cạnh chỉ cần đọc danh sách cạnh vài lượt, để đếm bậc và kiểm liên thông. "
        "Còn tìm đường qua mọi đỉnh bằng cách thử mọi thứ tự, trong trường hợp xấu nhất, phải thử cỡ n trừ 1 giai thừa chia 2 thứ tự. "
        "Với 21 đỉnh đã mất khoảng 39 năm, với 101 đỉnh thì không bao giờ xong. "
        "Người làm nghề tìm điều kiện đếm được như tính chẵn lẻ của bậc, và dùng tìm kiếm vét cạn, tức thử hết mọi khả năng, chỉ cho đồ thị nhỏ.",
        focus=[1, 2, "2.2", "2.4", "2.4", 3], clear=True, introduces=["factorial"]),
], checks=[
    "[(n, n * (n - 1)) for n in (11, 101, 1001)] == [(11, 110), (101, 10100), (1001, 1001000)] and [n * (n - 1) // 2 for n in (11, 101, 1001)] == [55, 5050, 500500]",
    "[(n - 1) % 2 for n in (11, 101, 1001)] == [0, 0, 0]",
    "math.factorial(10) // 2 == 1814400 and round(math.factorial(20) / 2 / 1e18, 1) == 1.2 and round(math.factorial(20) / 2 / 1e9 / 31557600) == 39",
    "len(str(math.factorial(100) // 2)) == 158",
])
quymo["steps"] = [TAB_A, TAB_B] + quymo["steps"]

DE = """# Lab DMS L16 — Bậc, bổ đề bắt tay và điều kiện Euler bằng chương trình

Viết `dothi.py` (Python 3.11 trở lên); chạy: `python dothi.py`.

Bốn đồ thị, mỗi đồ thị là một danh sách cạnh (chép nguyên vào đầu tệp):

```python
DO_THI = [
    ('G1', [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
    ('G2', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]),
    ('G3', [1, 2, 3, 4, 5, 6], [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]),
    ('G4', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5)]),
]
```

Với mỗi đồ thị in một dòng:
`<tên>: bac=<bậc các đỉnh theo thứ tự đỉnh tăng dần, cách nhau dấu phẩy không có dấu cách> tong=<tổng bậc> canh=<số cạnh> le=<số đỉnh bậc lẻ> lien_thong=<1 nếu liên thông, 0 nếu không> ket_luan=<chu_trinh | duong_di | khong>`

Quy ước `ket_luan` (điều kiện Euler): đồ thị phải liên thông; `chu_trinh` nếu không có đỉnh bậc lẻ; `duong_di` nếu có đúng 2 đỉnh bậc lẻ; còn lại `khong`. Ví dụ định dạng: `G9: bac=2,2,2 tong=6 canh=3 le=0 lien_thong=1 ket_luan=chu_trinh`.

Gợi ý: bậc của đỉnh v = số cạnh có v là một đầu; kiểm liên thông bằng cách đi từ một đỉnh qua các cạnh (duyệt rộng hoặc sâu) rồi xem có tới mọi đỉnh không. Tổng bậc phải bằng hai lần số cạnh.

Cú pháp gợi ý (chưa học ở đâu trước đó): `sum(1 for e in canh if v in e)` nghĩa là: với mỗi cạnh `e` trong danh sách `canh`, nếu `v` là một đầu của `e` thì cộng thêm 1, tức đếm các cạnh chứa `v`. Viết bằng vòng lặp thường cũng được: `bac = 0`, `for e in canh:`, `if v in e:`, `bac = bac + 1`.

Chấm: `bash labs/cham.sh DMS L16 dothi.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""DO_THI = [
    ('G1', [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
    ('G2', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]),
    ('G3', [1, 2, 3, 4, 5, 6], [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]),
    ('G4', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5)]),
]

def lien_thong(dinh, canh):
    thay = {dinh[0]}
    moi = True
    while moi:
        moi = False
        for u, v in canh:
            if (u in thay) != (v in thay):
                thay.add(u)
                thay.add(v)
                moi = True
    return len(thay) == len(dinh)

for ten, dinh, canh in DO_THI:
    bac = [sum(1 for e in canh if v in e) for v in dinh]
    le = sum(1 for b in bac if b % 2 == 1)
    lt = lien_thong(dinh, canh)
    if lt and le == 0:
        kl = 'chu_trinh'
    elif lt and le == 2:
        kl = 'duong_di'
    else:
        kl = 'khong'
    print(ten + ': bac=' + ','.join(str(b) for b in bac), 'tong=' + str(sum(bac)), 'canh=' + str(len(canh)), 'le=' + str(le),
          'lien_thong=' + str(int(lt)), 'ket_luan=' + kl)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> bậc của $v$ = <code>sum(1 for e in canh if v in e)</code> (cộng 1 cho mỗi cạnh chứa $v$; vòng lặp thường cũng được, xem <code>de.md</code>). Liên thông: bắt đầu từ một đỉnh, lặp “cạnh nào có đúng một đầu đã tới thì thêm đầu kia” tới khi không thêm được nữa, rồi so số đỉnh đã tới với tổng số đỉnh. '
    "Euler cần liên thông và số đỉnh bậc lẻ bằng 0 (chu trình) hoặc 2 (đường đi). "
    "Lời giải ở <code>labs/DMS/L16/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, bậc của một đỉnh là số cạnh có đỉnh đó là một đầu, và cách viết gọn cộng một cho mỗi cạnh như vậy được giải thích trong đề. Để kiểm liên thông, bắt đầu từ một đỉnh và lặp việc thêm đầu kia của mọi cạnh có đúng một đầu đã tới, rồi so số đỉnh đã tới với tổng số đỉnh. "
    "Điều kiện Euler cần liên thông, và số đỉnh bậc lẻ bằng không hoặc bằng hai.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_HTML, H_SAY, H_FOC = hint_parts2(HINT_BOX, HINT_SAY, [
    ("sum(1 for e in canh if v in e)", "với mỗi cạnh <code>e</code> trong danh sách <code>canh</code>, nếu <code>v</code> nằm trong <code>e</code> (v là một đầu của cạnh) thì cộng 1; <code>sum</code> cộng tất cả", "canh = [(1, 2), (2, 3)], v = 2: kết quả 2"),
], [
    "Biểu thức này duyệt từng cạnh trong danh sách, với mỗi cạnh có đỉnh v là một đầu thì cộng một, rồi cộng tất cả lại.",
], HINT_TAIL)

prac = practice(
    LID, "Tự làm: máy kiểm điều kiện Euler cho bốn đồ thị",
    "<p><b>Đề</b>: viết <code>dothi.py</code> nhận bốn đồ thị cho sẵn dưới dạng danh sách cạnh, in bậc từng đỉnh, tổng bậc, số cạnh, số đỉnh bậc lẻ, đồ thị có liên thông không, "
    "và kết luận có chu trình Euler, có đường đi Euler hay không (định dạng và bốn đồ thị ở <code>labs/DMS/L16/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Có một đồ thị tất cả đỉnh bậc chẵn mà vẫn không có chu trình: dự đoán trước đồ thị nào.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình nhận bốn đồ thị dưới dạng danh sách cạnh, rồi in bậc từng đỉnh, tổng bậc, số cạnh, số đỉnh bậc lẻ và đồ thị có liên thông không. "
    "Từ đó kết luận có chu trình Euler, có đường đi Euler hay không. Có một đồ thị mà mọi đỉnh bậc chẵn nhưng vẫn không có chu trình, hãy dự đoán trước đó là đồ thị nào. "
    "Bốn đồ thị và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "dothi.py", H_HTML, H_SAY,
    pause=420, focus1=[1, 1, 1, 1, 2, 0][:6], focus3=H_FOC)
patch_cham(prac, LID, "dothi.py")

OBJ = [
    "Tính bậc và dùng bổ đề bắt tay",
    "Nhận biết khi nào có chu trình hoặc đường đi Euler",
    "Phân biệt đi qua mọi cạnh với đi qua mọi đỉnh",
    "Đếm chi phí kiểm điều kiện Euler bằng bậc khi đồ thị lớn dần và so với thử mọi thứ tự đỉnh",
    "Viết chương trình tính bậc, kiểm liên thông và kết luận điều kiện Euler",
]
f, tpl, figs = apply(LID, quiz_pause=30, objectives=OBJ,
                     covers=[(1, "example"), (2, "euler"), (3, "pitfalls"), (4, "quymo"), (5, "practice")],
                     scenes=[(quymo, "pitfalls"), prac],
                     assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop"))
print(figs)
print(fill(LID, {"ENV": "audit/dms/fig/envelope.svg", "ENVP": "audit/dms/fig/envelope_path.svg", "KON": "audit/dms/fig/konigsberg.svg"}))
print(ledger_sync(LID, claims={"quymo": "11 đỉnh có 55 cạnh, tổng bậc 110; 101 đỉnh 5 050 cạnh; 1 001 đỉnh hơn nửa triệu cạnh; không đỉnh nào bậc lẻ"}))
