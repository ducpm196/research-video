"""DMS L17 → AF2 (WP5 phiên 2). Bài sinh từ MẪU audit/dms/src/L17_cay.tpl.yaml. Chạy: .venv/Scripts/python -B audit/dms/af2/l17.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L17"

C1 = r"""from itertools import combinations
def la_cay(n, tap):
    nhan = list(range(n))
    for u, v in tap:
        a, b = nhan[u], nhan[v]
        nhan = [a if x == b else x for x in nhan]
    return len(set(nhan)) == 1
for n in (5, 7):
    cay = sum(1 for t in combinations(combinations(range(n), 2), n - 1) if la_cay(n, t))
    print(n, 'dinh:', cay, 'cay co nhan; n^(n-2) =', n ** (n - 2))"""
O1 = run_py(C1)
print(O1)

TAB_A = read_steps([
    ("from itertools import combinations", "mượn hàm có sẵn <code>combinations</code>: liệt kê mọi cách chọn k phần tử từ một danh sách, không kể thứ tự", "combinations(range(3), 2) cho (0, 1), (0, 2), (1, 2)"),
    ("def la_cay(n, tap): … return …", "định nghĩa một hàm tên la_cay nhận n và tap (danh sách cạnh); <code>return</code> ở dòng cuối là kết quả hàm đưa ra", "la_cay(5, tap) đưa ra True hoặc False"),
    ("nhan = list(range(n))", "<code>range(n)</code> cho 0 tới n − 1, <code>list</code> xếp chúng thành danh sách: mỗi đỉnh khởi đầu một nhóm riêng, nhãn là chính nó", "n = 4: nhan = [0, 1, 2, 3]"),
    ("for u, v in tap: a, b = nhan[u], nhan[v]", "với mỗi cạnh (u, v) trong tap; <code>nhan[u]</code> là phần tử thứ u của danh sách (đếm từ 0); gán hai giá trị cùng lúc", "nhan = [0, 1, 2, 3], cạnh (1, 2): a = 1, b = 2"),
    ("nhan = [a if x == b else x for x in nhan]", "lập danh sách mới: với mỗi nhãn x cũ, nếu <code>x == b</code> (hai dấu bằng là so sánh) thì đổi thành a, không thì giữ nguyên; tức gộp nhóm b vào nhóm a", "nhan = [0, 1, 2, 3], a = 1, b = 2: thành [0, 1, 1, 3]"),
], "Chương trình đếm cây dùng mười ký hiệu, ta đọc năm cái đầu trước.", [
    "Dòng đầu mượn một hàm có sẵn liệt kê mọi cách chọn một số phần tử từ danh sách, không kể thứ tự.",
    "Dòng này định nghĩa một hàm nhận n và danh sách cạnh, và chữ trả về ở dòng cuối ghi kết quả hàm đưa ra.",
    "Hàm tạo dãy số cho 0 tới n trừ 1, và dòng này xếp chúng thành danh sách nhãn, mỗi đỉnh khởi đầu một nhóm riêng.",
    "Vòng lặp lấy từng cạnh với hai đầu u và v, rồi gán cùng lúc hai nhãn hiện tại của hai đầu cho a và b.",
    "Dòng này lập danh sách mới, với mỗi nhãn x cũ, nếu x bằng b thì đổi thành a, tức gộp nhóm b vào nhóm a.",
], split=3)

TAB_B = read_steps([
    ("len(set(nhan)) == 1", "<code>set(nhan)</code> giữ các nhãn khác nhau, <code>len</code> đếm chúng; đúng khi chỉ còn một nhóm, tức đồ thị liên thông", "nhan = [1, 1, 1, 1]: một nhãn khác nhau, đúng"),
    ("for n in (5, 7):", "với mỗi n lần lượt trong ngoặc, làm các dòng thụt vào bên dưới", "hai lượt: n = 5, rồi 7"),
    ("combinations(combinations(range(n), 2), n - 1)", "lời gọi trong cho mọi cặp đỉnh, tức mọi cạnh có thể; lời gọi ngoài chọn tiếp n − 1 cạnh trong số đó, được mọi tập n − 1 cạnh", "n = 3: 3 cạnh có thể, chọn 2 cạnh được 3 tập"),
    ("sum(1 for t in ... if la_cay(n, t))", "với mỗi tập cạnh t, nếu la_cay đưa ra True thì cộng 1; tức đếm các tập là cây", "n = 3: cả 3 tập đều là cây, kết quả 3"),
    ("print(n, 'dinh:', cay, ..., n ** (n - 2))", "in chữ trong dấu nháy và các giá trị ra cửa sổ; <code>**</code> là lũy thừa, <code>n ** (n - 2)</code> là công thức Cayley", "n = 5: 5 ** 3 = 125"),
], "Năm ký hiệu còn lại nằm ở dòng kiểm liên thông và các dòng đếm cây.", [
    "Hàm tập hợp giữ các nhãn khác nhau và hàm độ dài đếm chúng, nên điều kiện đúng khi chỉ còn một nhóm, tức đồ thị liên thông.",
    "Dòng mở đầu vòng lặp: với mỗi n lần lượt là 5 rồi 7, làm các dòng thụt vào bên dưới.",
    "Lời gọi trong cho mọi cặp đỉnh, tức mọi cạnh có thể, và lời gọi ngoài chọn tiếp n trừ 1 cạnh trong số đó.",
    "Biểu thức cộng một cho mỗi tập cạnh mà hàm kiểm trả đúng, tức đếm các tập là cây.",
    "Hàm in đưa chữ và các giá trị ra cửa sổ, và hai dấu sao là lũy thừa, nên n mũ n trừ 2 là công thức Cayley.",
], split=3)

quymo = scene("quymo", "example", "Khi số đỉnh tăng: đếm cây có nhãn bằng cách thử từng tập cạnh không kịp", [
    step(
        "<p><b>Chạy thật</b>: thử mọi tập $n - 1$ cạnh, đếm các tập là một cây</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật. Hàm đầu gán cho mỗi đỉnh một nhãn nhóm, mỗi cạnh gộp hai nhóm làm một, và đồ thị là một cây khi chỉ còn đúng một nhóm. "
        "Vòng lặp thử mọi cách chọn n trừ 1 cạnh trong các cạnh có thể. "
        "Với 5 đỉnh, đếm được 125 cây có nhãn. Với 7 đỉnh, 16 807. Cả hai lần khớp công thức Cayley, n mũ n trừ 2.",
        focus=[2, ["2.2", "2.7"], "2.9", "4.1", "4.2", 4], clear=True),
    step(
        "<p>Ba chỗ cú pháp mới trong chương trình trên:</p>"
        '<div class="box key"><code>combinations(range(n), 2)</code> cho mọi cặp đỉnh, tức mọi cạnh có thể; <code>combinations(..., n - 1)</code> chọn tiếp $n - 1$ cạnh trong số đó, được mọi tập $n - 1$ cạnh. Dòng <code>from itertools import combinations</code> mượn hàm có sẵn này.</div>'
        '<div class="box key"><code>[a if x == b else x for x in nhan]</code>: lập danh sách mới, với mỗi nhãn <code>x</code> cũ, nếu <code>x</code> bằng <code>b</code> thì đổi thành <code>a</code>, không thì giữ nguyên. Đó là gộp nhóm <code>b</code> vào nhóm <code>a</code>.</div>'
        '<div class="box key"><code>sum(1 for t in ... if la_cay(n, t))</code>: với mỗi tập cạnh <code>t</code>, nếu hàm trả đúng thì cộng 1, tức đếm các tập là cây. <code>len(set(nhan))</code> đếm số nhãn khác nhau.</div>',
        "Chương trình có ba chỗ cú pháp mới. Hàm mượn ở dòng đầu cho mọi cặp đỉnh, tức mọi cạnh có thể, rồi chọn tiếp n trừ 1 cạnh trong số đó. "
        "Dòng danh sách mới lập lại nhãn, với mỗi nhãn cũ bằng b thì đổi thành a, tức gộp nhóm b vào nhóm a. "
        "Dòng đếm cộng một cho mỗi tập cạnh mà hàm kiểm trả đúng, và đếm số nhãn khác nhau để biết còn mấy nhóm.",
        focus=[1, 1, 2, 3], clear=True),
    step(
        '<table class="t"><tr><th>số đỉnh $n$</th><th>số tập $n - 1$ cạnh phải thử</th><th>thử hết, một tỉ tập mỗi giây (số minh hoạ)</th><th>số cây có nhãn $n^{n-2}$</th></tr>'
        "<tr><td>7</td><td>54 264</td><td>khoảng 50 phần triệu giây</td><td>16 807</td></tr>"
        "<tr><td>10</td><td>886 163 135</td><td>khoảng 0,9 giây</td><td>100 000 000</td></tr>"
        "<tr><td>15</td><td>cỡ $9{,}2 \\times 10^{16}$</td><td>khoảng 3 năm</td><td>cỡ $1{,}9 \\times 10^{15}$</td></tr>"
        "<tr><td>20</td><td>cỡ $6{,}4 \\times 10^{25}$</td><td>khoảng 2 tỉ năm</td><td>cỡ $2{,}6 \\times 10^{23}$</td></tr></table>"
        '<div class="box key">Số tập cạnh phải thử tăng nhanh hơn cả số cây. Công thức Cayley cho đáp số ngay; còn nếu cần <b>liệt kê hay chọn một cây</b> thì dùng thuật toán xây dựng (thêm từng cạnh nối hai nhóm khác nhau), không thử từng tập.</div>',
        "Bảng này cho thấy thử từng tập cạnh không kịp. Với 15 đỉnh mất khoảng 3 năm, với 20 đỉnh khoảng 2 tỉ năm, trong khi số cây có nhãn của 20 đỉnh đã là cỡ mười mũ hai mươi ba. "
        "Công thức Cayley cho đáp số ngay. Còn khi cần dựng một cây, người làm nghề thêm từng cạnh nối hai nhóm khác nhau, chứ không thử từng tập cạnh.",
        focus=[1, "1.4", "1.5", 2][:4], clear=True),
], checks=[
    "[n ** (n - 2) for n in (5, 6, 7)] == [125, 1296, 16807]",
    "[math.comb(math.comb(n, 2), n - 1) for n in (7, 10)] == [54264, 886163135]",
    "9.1e16 < math.comb(105, 14) < 9.2e16 and 6.4e25 < math.comb(190, 19) < 6.5e25 and round(math.comb(105, 14) / 1e9 / 31557600) == 3",
    "1.9e15 < 15 ** 13 < 2e15 and 2.6e23 < 20 ** 18 < 2.7e23 and round(math.comb(190, 19) / 1e9 / 31557600 / 1e9) == 2",
])
quymo["steps"] = flat(TAB_A, TAB_B, quymo["steps"][0], quymo["steps"][2])   # fix6b: bảng đọc mã thay bước "cú pháp mới" đặt sau mã

DE = """# Lab DMS L17 — Cây: kiểm tra, đếm lá và công thức Cayley bằng chương trình

Viết `cay.py` (Python 3.11 trở lên); chạy: `python cay.py`.

Bốn đồ thị trên 6 đỉnh 1..6 (chép nguyên vào đầu tệp):

```python
DO_THI = [
    ('H1', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]),
    ('H2', [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6)]),
    ('H3', [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]),
    ('H4', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]),
]
```

Với mỗi đồ thị in một dòng `<tên>: n=6 m=<số cạnh> lien_thong=<0|1> chu_trinh=<0|1> la_cay=<0|1>`.
- `lien_thong`: có đường đi giữa hai đỉnh bất kỳ không.
- `chu_trinh`: có chu trình không (gợi ý: thêm lần lượt từng cạnh vào nhóm đỉnh; nếu một cạnh nối hai đỉnh ĐÃ cùng nhóm thì có chu trình).
- `la_cay`: bằng 1 khi liên thông và không có chu trình.

Sau bốn dòng, in tiếp ba dòng:
5. `H1: so la = <số>` — lá là đỉnh bậc 1
6. `H3: so la = <số>`
7. `cay co nhan 8 dinh (cong thuc Cayley): <số>` — `8 ** 6`

Để ý H2: có 5 cạnh = n − 1 nhưng KHÔNG phải cây.

Gợi ý khung (vòng lặp thường, không cần cú pháp nâng cao): cho mỗi đỉnh một nhãn nhóm `nhom = {v: v for v in range(1, 7)}` (từ điển: đỉnh → nhãn, lúc đầu mỗi đỉnh một nhóm); với mỗi cạnh `(u, v)`: nếu `nhom[u] == nhom[v]` thì có chu trình; nếu khác thì đổi mọi đỉnh mang nhãn `nhom[v]` sang nhãn `nhom[u]`. Cuối cùng còn một nhãn duy nhất nghĩa là liên thông.

Chấm: `bash labs/cham.sh DMS L17 cay.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""DO_THI = [
    ('H1', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]),
    ('H2', [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6)]),
    ('H3', [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]),
    ('H4', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]),
]

def phan_tich(canh):
    nhom = {v: v for v in range(1, 7)}
    chu_trinh = False
    for u, v in canh:
        a, b = nhom[u], nhom[v]
        if a == b:
            chu_trinh = True
        else:
            for x in nhom:
                if nhom[x] == b:
                    nhom[x] = a
    lien_thong = len(set(nhom.values())) == 1
    return lien_thong, chu_trinh

for ten, canh in DO_THI:
    lt, ct = phan_tich(canh)
    print(ten + ': n=6 m=' + str(len(canh)), 'lien_thong=' + str(int(lt)), 'chu_trinh=' + str(int(ct)), 'la_cay=' + str(int(lt and not ct)))

def so_la(canh):
    return sum(1 for v in range(1, 7) if sum(1 for e in canh if v in e) == 1)

print('H1: so la =', so_la(DO_THI[0][1]))
print('H3: so la =', so_la(DO_THI[2][1]))
print('cay co nhan 8 dinh (cong thuc Cayley):', 8 ** 6)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: kiểm bốn đồ thị có phải cây không, đếm lá và áp công thức Cayley",
    "<p><b>Đề</b>: viết <code>cay.py</code> nhận bốn đồ thị 6 đỉnh dưới dạng danh sách cạnh, in số cạnh, đồ thị có liên thông không, có chu trình không, có phải cây không; "
    "đếm lá của hai cây; và tính số cây có nhãn trên 8 đỉnh bằng công thức Cayley (bảy dòng, định dạng ở <code>labs/DMS/L17/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Một đồ thị có đúng n − 1 cạnh mà không phải cây: dự đoán trước đó là đồ thị nào.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình nhận bốn đồ thị sáu đỉnh dưới dạng danh sách cạnh, và in số cạnh, đồ thị có liên thông không, có chu trình không, và có phải cây không. "
    "Sau đó đếm lá của hai cây, và tính số cây có nhãn trên tám đỉnh bằng công thức Cayley. "
    "Có một đồ thị đúng năm cạnh mà vẫn không phải cây, hãy dự đoán trước đó là đồ thị nào. Định dạng bảy dòng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "cay.py",
    '<div class="box key"><b>Nếu kẹt:</b> gán cho mỗi đỉnh một nhãn nhóm; với mỗi cạnh $(u, v)$: nếu hai đầu đã cùng nhóm thì có chu trình, nếu khác thì gộp hai nhóm. Cuối cùng còn một nhóm là liên thông. '
    "Lá: đỉnh có đúng một cạnh chạm vào. Cayley: $n^{n-2}$, với $n = 8$ là $8^6$. "
    "Lời giải ở <code>labs/DMS/L17/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, gán cho mỗi đỉnh một nhãn nhóm. Với mỗi cạnh, nếu hai đầu đã cùng nhóm thì có chu trình, nếu khác nhóm thì gộp hai nhóm làm một. Cuối cùng chỉ còn một nhóm nghĩa là liên thông. "
    "Lá là đỉnh có đúng một cạnh. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=420, focus1=[1, 1, 1, 1, 2, 0])
patch_cham(prac, LID, "cay.py")

OBJ = [
    "Nhận ra cây qua các tính chất tương đương",
    "Nêu cách chứng minh cây n đỉnh có n − 1 cạnh bằng quy nạp (bỏ một lá)",
    "Dùng công thức Cayley đếm cây có nhãn",
    "Đếm số tập cạnh phải thử khi đếm cây có nhãn bằng cách liệt kê và so với công thức Cayley khi số đỉnh tăng",
    "Viết chương trình kiểm một đồ thị có phải cây không, đếm lá và áp công thức Cayley",
]
repl = [
    # fix12 (R8 SHOULD): "mạng rẻ nhất" cần độ dài từng dây, chưa nêu ở đầu bài
    ("Vì vậy tìm mạng rẻ nhất bằng cách thử hết từng cây là rất chậm, người ta dùng", "Nếu mỗi dây có độ dài riêng, tìm mạng ngắn nhất bằng cách thử hết từng cây là rất chậm, nên người ta dùng"),
    # fix6b (SHOULD): đỉnh cuối của đường dài nhất có thể kề đỉnh liền trước; bỏ lá không phá liên thông
    ("hay trên đường (sẽ có chu trình)", "hay trên đường ngoài đỉnh liền trước nó (sẽ có chu trình)"),
    ("còn một cây $n$ đỉnh, theo giả thiết quy nạp", "còn một cây $n$ đỉnh (vẫn liên thông vì lá chỉ có một cạnh nên không đường đi nào giữa hai đỉnh khác đi qua nó), theo giả thiết quy nạp"),
    ("Nó cũng không thể có hàng xóm khác trên đường, vì sẽ tạo chu trình", "Nó cũng không thể có hàng xóm trên đường ngoài đỉnh liền trước nó, vì sẽ tạo chu trình"),
    ("Bước quy nạp, cây n cộng 1 đỉnh có một lá, bỏ lá đó đi thì còn một cây n đỉnh có n trừ 1 cạnh theo giả thiết, thêm lại lá thì có n cạnh.",
     "Bước quy nạp, cây n cộng 1 đỉnh có một lá, bỏ lá đó thì còn cây n đỉnh, vì không đường đi nào giữa hai đỉnh khác đi qua lá. Cây đó có n trừ 1 cạnh theo giả thiết, thêm lại lá thì có n cạnh."),
    ('focus: [1, 1, 1, 1, 2, 2, 2]\n        say: "Bổ đề trước', 'focus: [1, 1, 1, 1, 2, 2, 2, 2]\n        say: "Bổ đề trước'),
]
f, tpl, figs = apply(LID, quiz_pause=30, objectives=OBJ, repl=asr_keep(LID) + repl,
                     covers=[(1, "equiv_props"), (2, "proof"), (3, "example"), (4, "quymo"), (5, "practice")],
                     scenes=[(quymo, "pitfalls"), prac],
                     assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop", "dms_quynap", "dms_tuongduong", "dms_giathiet", "dms_gtqn"))
print(figs)
print(fill(LID, {"T3": "audit/dms/fig/trees3.svg", "S4": "audit/dms/fig/shapes4.svg"}))
print(ledger_sync(LID, claims={"quymo": "5 đỉnh có 125 cây có nhãn, 6 đỉnh 1 296, 7 đỉnh 16 807, khớp công thức Cayley"}))
