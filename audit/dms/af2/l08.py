"""DMS L08 → AF2 (WP5). Bài sinh từ mẫu: vá MẪU audit/dms/src/L08_*.tpl.yaml rồi ghép hình. Chạy: .venv/Scripts/python -B audit/dms/af2/l08.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6lib import *  # noqa
from fix6b import patch_cham  # noqa  (câu giải nghĩa Git Bash; fix13)

LID = "L08"

C1 = r"""from itertools import permutations
for n in (6, 8):
    tong = 0
    hop_le = 0
    for hang in permutations(range(1, n + 1)):
        tong = tong + 1
        if hang.index(1) < hang.index(2) and hang.index(3) < hang.index(4):
            hop_le = hop_le + 1
    print(n, 'viec: thu', tong, 'hang, hop le', hop_le)"""
O1 = run_py(C1)
print(O1)

C2 = r"""sau = {1: [2, 3], 2: [4], 3: [4], 4: []}
dem = {1: 0, 2: 1, 3: 1, 4: 2}
san_sang = [1]
while san_sang:
    v = san_sang.pop()
    for w in sau[v]:
        dem[w] = dem[w] - 1
        if dem[w] == 0:
            san_sang.append(w)
    print('chon', v, ', bo dem:', dem)"""
O2 = run_py(C2)
print(O2)

# vết chạy thật của C2: dựng lại bằng chính thuật toán, đối chiếu từng dòng với đầu ra của C2
def _vet():
    sau = {1: [2, 3], 2: [4], 3: [4], 4: []}
    dem = {1: 0, 2: 1, 3: 1, 4: 2}
    san_sang = [1]
    rows, out = [], []
    while san_sang:
        v = san_sang.pop()
        for w in sau[v]:
            dem[w] = dem[w] - 1
            if dem[w] == 0:
                san_sang.append(w)
        out.append("chon " + str(v) + " , bo dem: " + str(dem))
        rows.append((len(rows) + 1, v, ", ".join(map(str, sau[v])) or "không có", " ".join(str(dem[k]) for k in (1, 2, 3, 4)), ", ".join(map(str, san_sang)) or "trống"))
    return rows, out
VET, VET_OUT = _vet()
assert VET_OUT == O2.splitlines(), (VET_OUT, O2)
VET_HTML = ("<p>Bốn việc: 1 trước 2 và 3; 2 và 3 trước 4. Bộ đếm ban đầu của việc 1, 2, 3, 4 là 0, 1, 1, 2 (số việc phải xong trước nó).</p>"
            '<table class="t"><tr><th>lượt</th><th>việc được chọn</th><th>trừ 1 ở bộ đếm của</th><th>bộ đếm việc 1 2 3 4</th><th>danh sách sẵn sàng</th></tr>'
            + "".join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>" for r in VET) + "</table>"
            '<p class="note">Bảng này là kết quả chạy thật của thuật toán chọn từng việc bằng bộ đếm, chạy trên bốn việc ở trên.</p>')

TABA = read_steps([
    ("from itertools import permutations", "mượn một hàm làm sẵn tên <code>permutations</code>: liệt kê mọi cách xếp thứ tự", "permutations([1, 2, 3]) cho 6 hàng: (1, 2, 3), (1, 3, 2), …"),
    ("for n in (6, 8):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "hai lượt: n = 6, rồi n = 8"),
    ("for hang in permutations(range(1, n + 1)):", "<code>range(1, n + 1)</code> cho các số 1 tới n; <code>hang</code> chạy qua mọi cách xếp các số đó thành một hàng", "n = 3: hang lần lượt là (1, 2, 3), (1, 3, 2), … đủ 6 hàng"),
    ("tong = tong + 1", "một dấu bằng là <b>gán</b>: tính bên phải rồi cất vào tên bên trái, ở đây là tăng tong thêm 1", "tong đang là 4 thì thành 5"),
    ("print(n, 'viec: thu', tong)", "in chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách", "n = 6: in ra 6 viec: thu 720"),
], "Chương trình thử mọi hàng dùng hai đợt ký hiệu, đợt một là phần dựng và đếm các hàng.", [
    "Dòng đầu mượn một hàm làm sẵn để liệt kê mọi cách xếp thứ tự, tên hàm ghi trên màn hình.",
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 6 rồi 8, làm các dòng thụt vào bên dưới.",
    "Vòng lặp trong cho hàng chạy qua mọi cách xếp các số từ 1 tới n thành một hàng, trong đó hàm tạo dãy số cho các số từ 1 tới n.",
    "Một dấu bằng là gán: tính bên phải rồi cất vào tên bên trái, nên dòng này tăng biến đếm thêm một.",
    "Hàm in đưa chữ trong dấu nháy và các giá trị ra cửa sổ, cách nhau một dấu cách.",
], split=3)
TABB = read_step([
    ("if điều_kiện:", "<b>nếu</b> điều kiện đúng thì chạy các dòng thụt vào bên dưới, sai thì bỏ qua", "if 7 > 5: chạy; if 3 > 5: bỏ qua"),
    ("hang.index(1)", "vị trí của số 1 trong hàng, đếm từ 0", "(3, 1, 2).index(1) là 1"),
    ("hang.index(1) < hang.index(2)", "<code>&lt;</code> là nhỏ hơn: vị trí của 1 nhỏ hơn vị trí của 2, tức việc 1 đứng trước việc 2", "(3, 1, 2): 1 ở vị trí 1, 2 ở vị trí 2, nên đúng"),
    ("... and ...", "và: đúng khi cả hai điều kiện đúng", "đúng and sai là sai"),
], "Đợt hai là dòng kiểm hai ràng buộc của mỗi hàng.", [
    "Chữ nếu kèm điều kiện nghĩa là: nếu điều kiện đúng thì chạy các dòng thụt vào bên dưới, còn sai thì bỏ qua.",
    "Phép lấy vị trí cho biết số 1 đứng ở chỗ nào trong hàng, đếm từ 0.",
    "Dấu nhỏ hơn so hai vị trí: vị trí của việc 1 nhỏ hơn vị trí của việc 2 nghĩa là việc 1 đứng trước việc 2.",
    "Chữ giữa hai điều kiện là và, nên hàng hợp lệ khi cả hai ràng buộc cùng đúng.",
])

quymo = scene("quymo", "example", "Khi số việc tăng: thử mọi hàng không kịp, chọn từng phần tử thì kịp", [
    *TABA,
    TABB,
    step(
        "<p><b>Chạy thật</b>: $n$ việc, chỉ có hai ràng buộc “việc 1 trước việc 2” và “việc 3 trước việc 4”; thử mọi cách xếp thành hàng</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Hàm làm sẵn liệt kê mọi cách xếp thứ tự n việc thành một hàng, và ta đếm các hàng thoả cả hai ràng buộc. "
        "Với 6 việc có 720 cách xếp, trong đó 180 hàng hợp lệ. Với 8 việc có 40 320 cách xếp, trong đó 10 080 hàng hợp lệ. "
        "Thêm hai việc thì số cách xếp phải thử tăng hơn năm mươi lần.",
        focus=[2, ["2.1", "2.2"], "4.1", "4.2", 4], clear=True),
    step(
        VET_HTML,
        "Đây là cách chọn từng việc bằng bộ đếm, kết quả chạy thật trên bốn việc. "
        "Mỗi việc có một bộ đếm, ghi số việc phải xong trước nó, và việc một có bộ đếm không nên làm được ngay. "
        "Mỗi lượt ta lấy một việc sẵn sàng ra làm, rồi trừ một ở bộ đếm của các việc đứng ngay sau nó. "
        "Việc nào có bộ đếm về không thì được thêm vào danh sách sẵn sàng, và bảng cho thấy bộ đếm sau từng lượt. "
        "Bốn lượt chọn, cộng bốn lần trừ bộ đếm, đúng bằng số ràng buộc, tức tám thao tác cho bốn việc.",
        focus=[1, 1, "2.2", "2.3", 2], clear=True),
    step(
        '<p>$n!$ (đọc “n giai thừa”) là tích $1 \\times 2 \\times \\dots \\times n$, ví dụ $3! = 1 \\times 2 \\times 3 = 6$.</p>'
        '<table class="t"><tr><th>số việc $n$</th><th>số cách xếp $n!$</th><th>thử hết ở một tỉ hàng mỗi giây (số minh hoạ)</th></tr>'
        "<tr><td>8</td><td>40 320</td><td>chưa tới một phần nghìn giây</td></tr>"
        "<tr><td>15</td><td>1 307 674 368 000</td><td>khoảng 22 phút</td></tr>"
        "<tr><td>20</td><td>2 432 902 008 176 640 000</td><td>khoảng 77 năm</td></tr>"
        "<tr><td><b>chọn từng việc không còn ai đứng dưới</b></td><td><b>$n$ lượt chọn</b>, cộng một lần trừ bộ đếm cho mỗi ràng buộc (ví dụ trên: $4 + 4 = 8$ thao tác)</td><td>một triệu việc, gần hai triệu ràng buộc: khoảng 3 triệu thao tác, cỡ 3 phần nghìn giây</td></tr></table>"
        '<div class="box key">Thử mọi hàng tăng <b>giai thừa</b>; chọn từng phần tử còn trống chỉ tốn khoảng <b>$n$ lượt</b>.</div>',
        "Ký hiệu n giai thừa, viết n kèm dấu chấm than, là tích 1 nhân 2 nhân tiếp tới n, ví dụ 3 giai thừa bằng 6. Bảng này cho thấy thử mọi hàng tăng theo giai thừa. Với 15 việc đã mất khoảng 22 phút, với 20 việc thì khoảng 77 năm. "
        "Còn thuật toán của bài chọn một phần tử còn trống ở mỗi lượt, nên cần n lượt chọn. Tổng công sức chỉ cỡ n cộng số ràng buộc, như ví dụ bốn việc ở trên, bốn cộng bốn bằng tám. "
        "Với một triệu việc và gần hai triệu ràng buộc, đó là khoảng ba triệu thao tác, cỡ ba phần nghìn giây theo số minh hoạ. Nhờ vậy kịp với cả triệu việc. "
        "Người làm nghề dùng thuật toán chọn từng phần tử, và chỉ dùng cách thử mọi hàng để kiểm lại trên cỡ nhỏ.",
        focus=[1, 2, ["2.3", "2.4"], "2.5", "2.5", "2.5", "2.5", 3], clear=True, introduces=["factorial"]),
], checks=[
    "[math.factorial(n) for n in (6, 8)] == [720, 40320] and [math.factorial(n) // 4 for n in (6, 8)] == [180, 10080]",
    "[math.factorial(n) for n in (10, 15, 20)] == [3628800, 1307674368000, 2432902008176640000]",
    "round(math.factorial(15) / 1e9 / 60) == 22 and round(math.factorial(20) / 1e9 / 86400 / 365.25) == 77",
    "round(math.factorial(8) / math.factorial(6)) == 56",
    "(10 ** 6) + (2 * 10 ** 6 - 3) == 2999997 and round((3 * 10 ** 6 - 3) / 1e9 * 1000) == 3",
])

DE = """# Lab DMS L08 — Biểu đồ thứ tự và sắp xếp tô pô cho quan hệ "là ước của" trên các ước của 24

Viết `thutu.py` (Python 3.11 trở lên); chạy: `python thutu.py`.

Tập `S = [1, 2, 3, 4, 6, 8, 12, 24]` (các ước của 24); quan hệ `a ≼ b` khi `a` là ước của `b` (`b % a == 0`). Quan hệ "phủ" (cạnh của biểu đồ thứ tự): cặp `(a, b)` với `a` khác `b`, `a ≼ b`, và KHÔNG có phần tử `c` khác `a`, `b` nào mà `a ≼ c` và `c ≼ b`.

In đúng bảy dòng:
1. `so canh Hasse: <số cạnh phủ>`
2. `canh: a-b a-b ...` — các cạnh phủ `a-b` xếp tăng dần theo `a` rồi theo `b`, cách nhau một dấu cách
3. `phan tu toi tieu: <các phần tử không có ai đứng dưới, cách nhau dấu cách>`
4. `phan tu toi dai: <các phần tử không có ai đứng trên>`
5. `cap khong so sanh duoc: <số cặp {a, b} với a < b mà không số nào là ước của số kia>`
6. `sap xep to po (chon so lon nhat): ...` — thuật toán: mỗi lượt, trong các phần tử CHƯA xếp mà mọi phần tử đứng dưới nó đã xếp, chọn phần tử LỚN NHẤT, xếp vào hàng; lặp tới khi hết. In hàng, các số cách nhau một dấu cách.
7. `so cach sap xep to po: <số>` — đếm bằng cách thử mọi hoán vị của S, tức mọi cách xếp thứ tự (`from itertools import permutations` liệt kê chúng): hàng hợp lệ khi mọi cặp `a ≼ b` (a khác b) có `a` đứng trước `b`.

Gợi ý: phần tử "đứng dưới x" là các a khác x mà x % a == 0; dùng `list.index` để biết vị trí trong hàng.

Chấm: `bash labs/cham.sh DMS L08 thutu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from itertools import permutations

S = [1, 2, 3, 4, 6, 8, 12, 24]

def duoi(x):
    return [a for a in S if a != x and x % a == 0]

canh = []
for a in S:
    for b in S:
        if a != b and b % a == 0 and not any(c != a and c != b and c % a == 0 and b % c == 0 for c in S):
            canh.append((a, b))

print('so canh Hasse:', len(canh))
print('canh:', ' '.join(str(a) + '-' + str(b) for a, b in canh))
print('phan tu toi tieu:', ' '.join(str(x) for x in S if not duoi(x)))
print('phan tu toi dai:', ' '.join(str(x) for x in S if not any(y != x and y % x == 0 for y in S)))
khong_sanh = 0
for a in S:
    for b in S:
        if a < b and b % a != 0:
            khong_sanh = khong_sanh + 1
print('cap khong so sanh duoc:', khong_sanh)

hang = []
while len(hang) < len(S):
    san_sang = [x for x in S if x not in hang and all(a in hang for a in duoi(x))]
    hang.append(max(san_sang))
print('sap xep to po (chon so lon nhat):', ' '.join(str(x) for x in hang))

dem = 0
for h in permutations(S):
    if all(h.index(a) < h.index(b) for a in S for b in S if a != b and b % a == 0):
        dem = dem + 1
print('so cach sap xep to po:', dem)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> cạnh phủ là cặp ước–bội không có phần tử nào ở giữa: <code>not any(c != a and c != b and c % a == 0 and b % c == 0 for c in S)</code>. '
    "Mỗi lượt sắp xếp: lọc các số chưa xếp mà mọi số đứng dưới nó đã nằm trong hàng, rồi lấy <code>max</code>. "
    "Lời giải ở <code>labs/DMS/L08/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, cạnh của biểu đồ là cặp ước và bội mà không có phần tử nào ở giữa. Mỗi lượt sắp xếp, lọc các số chưa xếp mà mọi số đứng dưới nó đã nằm trong hàng, rồi lấy số lớn nhất. "
    "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.")
H_HTML, H_SAY, H_FOC = hint_parts(HINT_BOX, HINT_SAY, [
    ("not any(điều_kiện for c in S)", "<code>any</code> là <b>tồn tại</b>: có ít nhất một c trong S làm điều kiện đúng; thêm <code>not</code> là <b>không có</b> c nào như vậy", "not any(c > 9 for c in [1, 2, 3]) là True"),
    ("c != a and c != b", "c khác a <b>và</b> khác b: c không trùng hai đầu", "a = 2, b = 8, c = 4: đúng"),
    ("c % a == 0", "<code>%</code> là chia lấy số dư, <code>==</code> là so sánh bằng: c chia hết cho a, tức a là ước của c", "12 % 4 == 0 là True"),
    ("max(san_sang)", "số lớn nhất trong danh sách", "max([2, 8, 3]) là 8"),
], [
    "Hàm tồn tại đúng khi có ít nhất một phần tử làm điều kiện đúng, và chữ không đứng trước nó nghĩa là không có phần tử nào như vậy.",
    "Điều kiện đầu nói c khác cả a lẫn b, tức c không trùng hai đầu của cặp.",
    "Dấu phần trăm là chia lấy số dư, hai dấu bằng liền nhau là so sánh bằng, nên dòng này nói c chia hết cho a.",
    "Hàm lớn nhất lấy số lớn nhất trong danh sách các việc sẵn sàng.",
])

prac = practice(
    LID, "Tự làm: biểu đồ thứ tự và sắp xếp tô pô cho các ước của 24",
    "<p><b>Đề</b>: với quan hệ “là ước của” trên $\\{1, 2, 3, 4, 6, 8, 12, 24\\}$, viết <code>thutu.py</code> in số cạnh và các cạnh của biểu đồ thứ tự, phần tử tối tiểu (không ai đứng dưới), tối đại (không ai đứng trên), "
    "số cặp không so sánh được, một hàng sắp xếp tô pô theo luật “chọn số lớn nhất còn trống”, và số hàng hợp lệ đếm bằng cách thử mọi hoán vị, tức mọi cách xếp thứ tự (bảy dòng, định dạng ở <code>labs/DMS/L08/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài (24 thay cho 12, có thêm số 8).</p>',
    "Bây giờ tới phần bạn tự làm. Với quan hệ là ước của trên các ước của 24, hãy viết chương trình in các cạnh của biểu đồ thứ tự và số cặp không so sánh được. Rồi in phần tử tối tiểu, tức không ai đứng dưới, và phần tử tối đại, tức không ai đứng trên. "
    "Sau đó xếp tô pô bằng luật chọn số lớn nhất còn trống, và đếm số hàng hợp lệ bằng cách thử mọi cách xếp thứ tự. Bảy dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "thutu.py", H_HTML, H_SAY,
    pause=360, focus1=[1, 1, 1, 1, 2, 0], focus3=H_FOC)
patch_cham(prac, LID, "thutu.py")

OBJ = [
    "Nhận ra thứ tự bộ phận và cặp không so sánh được",
    "Nêu cách vẽ biểu đồ Hasse (biểu đồ thứ tự): chỉ nối hai phần tử liền kề",
    "Liệt kê một thứ tự tuyến tính tương thích (sắp xếp tô pô)",
    "Đếm số cách xếp phải thử khi số việc tăng, và so với thuật toán chọn từng phần tử còn trống",
    "Viết chương trình tìm cạnh của biểu đồ thứ tự, sắp xếp tô pô và đếm số hàng hợp lệ",
]
f, tpl, figs = apply(LID, objectives=OBJ,
                     covers=[(1, "sym_poset"), (2, "hasse"), (3, "example"), (4, "quymo"), (5, "practice")],
                     scenes=[(quymo, "pitfalls"), prac],
                     repl=[("Biểu đồ thứ tự trên màn hình, mang tên một nhà toán học ghi trên màn hình, vẽ quan hệ này rất gọn.",
                            "Biểu đồ thứ tự trên màn hình, tên riêng của nó ghi ở trên đó, vẽ quan hệ này rất gọn.")],
                     assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop", "dms_tuongduong"))
print(figs)
print(fill(LID, {"HASSE": "audit/dms/fig/hasse12.svg", "HASSE_BAD": "audit/dms/fig/hasse12_bad.svg"}))
print(ledger_sync(LID, claims={"quymo": "6 việc: 720 cách xếp, 180 hàng hợp lệ; 8 việc: 40 320 cách xếp, 10 080 hàng hợp lệ"}))
