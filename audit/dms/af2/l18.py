"""DMS L18 → AF2 (WP5 phiên 2). Bài sinh từ MẪU audit/dms/src/L18_do_thi_phang.tpl.yaml. Chạy: .venv/Scripts/python -B audit/dms/af2/l18.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa

LID = "L18"

C1 = r"""def so_mau(n, thu_tu):
    mau = {}
    for v in thu_tu:
        ke = {mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]}
        mau[v] = min(c for c in range(2 * n) if c not in ke)
    return max(mau.values()) + 1
for n in (10, 100):
    xen_ke = [(s, i) for i in range(n) for s in 'ab']
    ab = [(s, i) for s in 'ab' for i in range(n)]
    print(2 * n, 'dinh: xen ke', so_mau(n, xen_ke), 'mau, a truoc b sau', so_mau(n, ab), 'mau')"""
O1 = run_py(C1)
print(O1)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import plain_svg  # noqa: E402  (audit/dms/plain_svg.py: svg() + crown())
CROWN_XEN, _c1 = plain_svg.crown(3, ["a0", "b0", "a1", "b1", "a2", "b2"])
CROWN_AB, _c2 = plain_svg.crown(3, ["a0", "a1", "a2", "b0", "b1", "b2"])
assert max(_c1.values()) + 1 == 3 and max(_c2.values()) + 1 == 2

TAB_A = read_step([
    ("def so_mau(n, thu_tu): … return …", "định nghĩa hàm so_mau nhận n và thu_tu (danh sách đỉnh theo thứ tự tô); <code>return</code> là kết quả hàm đưa ra", "so_mau(10, xen_ke) đưa ra số màu đã dùng"),
    ("mau = {}, mau[v] = …", "<code>{}</code> là từ điển rỗng, một bảng ghi “đỉnh → màu”; <code>mau[v] = …</code> ghi màu cho đỉnh v", "mau[('a', 0)] = 0 ghi đỉnh ('a', 0) màu 0"),
    ("for v in thu_tu: … v[0], v[1]", "với mỗi đỉnh v lần lượt trong thứ tự; đỉnh là một cặp, <code>v[0]</code> là phần tử đầu (chữ a hoặc b: hàng), <code>v[1]</code> là phần tử thứ hai (chỉ số), đếm từ 0", "v = ('a', 3): v[0] = 'a', v[1] = 3"),
    ("{mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]}", "tập các màu <code>mau[u]</code> của mọi đỉnh u đã tô mà <code>!=</code> (khác) hàng <code>and</code> (và) khác chỉ số với v, tức u kề v", "v = ('b', 1): u = ('a', 0) kề; u = ('a', 1) không kề"),
], "Chương trình tô màu dùng chín ký hiệu, ta đọc bốn cái đầu trước.", [
    "Dòng đầu định nghĩa một hàm nhận n và thứ tự tô, và chữ trả về ở dòng cuối ghi kết quả hàm đưa ra.",
    "Dấu ngoặc nhọn rỗng tạo một từ điển, tức bảng ghi mỗi đỉnh với màu của nó, và dòng gán ghi màu cho đỉnh v.",
    "Vòng lặp lấy từng đỉnh theo thứ tự, mỗi đỉnh là một cặp, phần tử đầu là hàng a hoặc b, phần tử thứ hai là chỉ số, đếm từ 0.",
    "Dòng này lập tập màu của mọi đỉnh đã tô mà khác hàng và khác chỉ số với v, tức mọi đỉnh kề v.",
])

TAB_B = read_step([
    ("min(c for c in range(2 * n) if c not in ke)", "với c lần lượt 0, 1, 2, … tới 2n − 1, chỉ lấy c không thuộc tập ke (<code>not in</code> là không có trong); <code>min</code> chọn số nhỏ nhất", "ke = {0, 1}: kết quả 2"),
    ("max(mau.values()) + 1", "<code>mau.values()</code> là các màu đã ghi, <code>max</code> lấy màu lớn nhất; màu đánh số từ 0 nên cộng 1 ra số màu", "màu lớn nhất là 2: đã dùng 3 màu"),
    ("[(s, i) for i in range(n) for s in 'ab']", "lập danh sách các cặp (s, i): vòng ngoài i từ 0 tới n − 1, vòng trong s là 'a' rồi 'b'; đảo hai vòng cho thứ tự a trước, b sau", "n = 2: [('a', 0), ('b', 0), ('a', 1), ('b', 1)]"),
    ("for n in (10, 100): print(2 * n, …)", "với mỗi n lần lượt trong ngoặc; <code>2 * n</code> là số đỉnh; <code>print</code> in chữ trong dấu nháy và các giá trị ra cửa sổ", "n = 10: in ra 20 dinh: xen ke 10 mau, …"),
], "Bốn ký hiệu còn lại nằm ở dòng chọn màu, dòng đếm màu và các dòng tạo thứ tự.", [
    "Dòng này thử các màu từ 0 trở lên, bỏ màu đã nằm trong tập của hàng xóm, rồi chọn màu nhỏ nhất còn lại.",
    "Hàm lấy giá trị lớn nhất cho màu lớn nhất đã ghi trong từ điển, và vì màu đánh số từ 0 nên cộng 1 ra số màu đã dùng.",
    "Dòng này lập danh sách các cặp gồm chữ và chỉ số, và đổi thứ tự hai vòng thì được thứ tự a trước, b sau.",
    "Vòng lặp cho n là 10 rồi 100, số đỉnh là 2 nhân n, và hàm in đưa kết quả ra cửa sổ.",
])

quymo = scene("quymo", "example", "Khi đồ thị lớn dần: tô màu tham lam có thể phí gấp n/2 lần", [
    step(
        '<div class="row"><div class="col"><p><b>Thứ tự xen kẽ</b> a0, b0, a1, b1, a2, b2: <b>3 màu</b></p>' + CROWN_XEN + '</div>'
        '<div class="col"><p><b>Thứ tự a trước, b sau</b> a0, a1, a2, b0, b1, b2: <b>2 màu</b></p>' + CROWN_AB + '</div></div>'
        '<p class="note">Đồ thị “vương miện” 3 cặp: $a_i$ nối $b_j$ <b>khi $i ≠ j$</b> (6 cạnh), không có cạnh nào nối hai đỉnh cùng hàng (đồ thị <b>hai phía</b>). Màu đánh số từ 0.</p>',
        "Trước khi chạy chương trình, ta vẽ đồ thị này với ba cặp đỉnh. "
        "Có hai hàng đỉnh a và b, mỗi hàng ba đỉnh đánh số từ 0 đến 2, và đỉnh a nối với đỉnh b khi chỉ số của chúng khác nhau. "
        "Không có cạnh nào nối hai đỉnh cùng hàng, nên chỉ cần 2 màu, một màu cho mỗi hàng, và đồ thị như vậy gọi là hai phía. "
        "Nhưng tô tham lam xen kẽ cho mỗi cặp a số i và b số i cùng một màu, cặp 0 màu 0, cặp 1 màu 1, cặp 2 màu 2, nên cần 3 màu. "
        "Nếu tô cả hàng a trước rồi mới tới hàng b, chỉ cần 2 màu.",
        focus=[1, 2, 2, "1.1", "1.2"], clear=True),
    step(
        "<p><b>Chạy thật</b>: $2n$ đỉnh $a_i, b_i$; $a_i$ kề $b_j$ khi $i \\ne j$ (hai phía). Tô tham lam theo hai thứ tự</p>" + run_html(C1, O1, "Kết quả chạy thật"),
        "Đây là chương trình chạy thật, trên đồ thị vương miện vừa vẽ nhưng với n bằng 10 và 100 cặp. "
        "Nếu đi xen kẽ a một, b một, a hai, b hai, thì với 20 đỉnh dùng 10 màu, với 200 đỉnh dùng tới 100 màu. "
        "Nếu tô hết các đỉnh a trước rồi mới tới b, chỉ cần 2 màu ở cả hai cỡ.",
        focus=[2, ["4.1", "4.2"], ["4.1", "4.2"]], clear=True),
    step(
        "<p>Cú pháp trong hàm <code>so_mau</code>:</p>"
        '<div class="box key"><code>mau[v] = ...</code>: <code>mau</code> là một từ điển, ghi màu của mỗi đỉnh đã tô. Đỉnh là cặp, ví dụ <code>(&#39;a&#39;, 3)</code>: <code>v[0]</code> là chữ a hoặc b (hàng), <code>v[1]</code> là chỉ số.</div>'
        '<div class="box key"><code>{mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]}</code>: lập tập màu của mọi đỉnh <code>u</code> đã tô mà <b>kề</b> <code>v</code>, tức khác hàng <b>và</b> khác chỉ số.</div>'
        '<div class="box key"><code>min(c for c in range(2 * n) if c not in ke)</code>: số nhỏ nhất trong 0, 1, 2, … mà không thuộc tập màu <code>ke</code>. <code>for s in &#39;ab&#39;</code> cho <code>s</code> lần lượt là a rồi b.</div>',
        "Hàm này có ba chỗ cú pháp mới cần giải thích. Từ điển mau ghi màu của mỗi đỉnh đã tô, và mỗi đỉnh là một cặp gồm chữ a hoặc b, rồi chỉ số. "
        "Dòng thứ ba lập tập màu của mọi đỉnh đã tô mà kề với đỉnh đang xét, tức đỉnh khác hàng và khác chỉ số. "
        "Dòng thứ tư lấy số nhỏ nhất trong 0, 1, 2 và cứ thế, mà chưa thuộc tập màu đó.",
        focus=[1, 2, 3, 4], clear=True),
    step(
        '<table class="t"><tr><th>số đỉnh $2n$</th><th>số màu tối thiểu</th><th>tham lam, thứ tự xen kẽ</th><th>tham lam, a trước b sau</th></tr>'
        "<tr><td>20</td><td>2</td><td>10</td><td>2</td></tr>"
        "<tr><td>200</td><td>2</td><td>100</td><td>2</td></tr>"
        "<tr><td>2 000 000 (suy ra theo quy luật, chưa chạy)</td><td>2</td><td>1 000 000</td><td>2</td></tr></table>"
        '<div class="box key">Bậc lớn nhất là $n - 1$, nên cận “bậc lớn nhất cộng 1” của bài là $n$: thứ tự xấu <b>đạt đúng cận đó</b>, phí gấp $n/2$ lần mức tối thiểu và phí tăng theo cỡ đồ thị. Đánh đổi: thứ tự tốt phải biết trước cấu trúc đồ thị, mà tìm số màu tối thiểu cho mọi đồ thị là bài toán khó.</div>',
        "Bảng này cho thấy thứ tự quyết định. Số màu tối thiểu luôn là 2, nhưng thứ tự xen kẽ phí tăng theo cỡ đồ thị, gấp n chia 2 lần mức cần thiết, tức 5 lần với 20 đỉnh và 50 lần với 200 đỉnh. "
        "Đánh đổi của người làm nghề là, thứ tự tốt cần biết trước cấu trúc đồ thị, trong khi tìm số màu ít nhất cho mọi đồ thị là bài toán khó.",
        focus=[1, "1.3", 2], clear=True),
], checks=[
    "[(lambda n, order: max(__import__('functools').reduce(lambda mau, v: {**mau, v: min(c for c in range(2 * n) if c not in {mau[u] for u in mau if u[0] != v[0] and u[1] != v[1]})}, order, {}).values()) + 1)(n, o) for n, o in ((10, [(s, i) for i in range(10) for s in 'ab']), (10, [(s, i) for s in 'ab' for i in range(10)]), (100, [(s, i) for i in range(100) for s in 'ab']))] == [10, 2, 100]",
    "[(2 * n, n) for n in (10, 100, 1000000)] == [(20, 10), (200, 100), (2000000, 1000000)]",
    "max(sum(1 for u in range(20) if u // 2 != v // 2 and u % 2 != v % 2) for v in range(20)) + 1 == 10",
])
quymo["steps"] = [quymo["steps"][0], TAB_A, TAB_B, quymo["steps"][1], quymo["steps"][3]]   # fix6b: bảng đọc mã đặt TRƯỚC mã, thay bước "cú pháp" đặt sau

DE = """# Lab DMS L18 — Công thức Euler, giới hạn 3V − 6 và tô màu tham lam bằng chương trình

Viết `phang.py` (Python 3.11 trở lên); chạy: `python phang.py`.

In đúng tám dòng (không dấu):
1–3. Với đồ thị phẳng liên thông có `(V, E)` = `(10, 15)`, `(7, 6)`, `(12, 30)`: in `V=<V> E=<E>: F=<số mặt>` với `F = 2 - V + E` (công thức Euler `V - E + F = 2`).
4–6. Với đồ thị đơn mà ta chỉ biết số đỉnh `V` và số cạnh `E` (không có danh sách cạnh) với `(V, E)` = `(7, 19)`, `(8, 18)`, `(6, 9)`: in `V=<V> E=<E>: khong phang` nếu `E > 3*V - 6`, ngược lại `V=<V> E=<E>: chua ket luan` (bất đẳng thức đúng thì chưa đủ để kết luận phẳng; ví dụ `(6, 9)` là bài toán ba nhà ba nguồn, không phẳng).
7. Đồ thị "vương miện" 4 cặp (8 đỉnh): đỉnh `('a', i)` và `('b', i)` với `i` từ 0 đến 3; `('a', i)` kề `('b', j)` khi `i != j`. Tô màu tham lam (đi lần lượt từng đỉnh, tô màu nhỏ nhất, bắt đầu từ 0, chưa bị đỉnh kề đã tô dùng), theo hai thứ tự: xen kẽ `a0, b0, a1, b1, ...` và `a0, a1, a2, a3, b0, b1, b2, b3`. In `do thi 4 cap (8 dinh): xen ke <số màu> mau, a truoc b sau <số màu> mau` (số màu = màu lớn nhất đã dùng cộng 1).
8. Chu trình 5 đỉnh (đỉnh i kề đỉnh (i+1) mod 5), tô tham lam theo thứ tự 0, 1, 2, 3, 4: in `chu trinh 5 dinh: tham lam <số màu> mau, can tren <bậc lớn nhất + 1>`.

Hai đỉnh gọi là kề nhau khi có một cạnh nối chúng.

Gợi ý cú pháp cho dòng 7–8 (có thể viết bằng vòng lặp thường nếu quen hơn):
- Tập màu của các đỉnh kề đã tô: `{mau[u] for u in ke[v] if u in mau}` nghĩa là: với mỗi đỉnh `u` kề `v` mà đã có trong từ điển `mau`, lấy màu `mau[u]`, gom thành một tập. Tương đương: `da_dung = set()`, `for u in ke[v]:`, `if u in mau:`, `da_dung.add(mau[u])`.
- Màu nhỏ nhất chưa dùng: `c = 0`, rồi `while c in da_dung: c = c + 1`.
- Danh sách đỉnh `[('a', i) for i in range(n)]` lập các cặp `('a', 0)`, `('a', 1)`, ... ; từ điển kề `{v: [u for u in dinh if u[0] != v[0] and u[1] != v[1]] for v in dinh}` ghi, với mỗi đỉnh `v`, danh sách các đỉnh khác hàng và khác chỉ số.

Chấm: `bash labs/cham.sh DMS L18 phang.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""def tham_lam(dinh, ke, thu_tu):
    mau = {}
    for v in thu_tu:
        da_dung = {mau[u] for u in ke[v] if u in mau}
        c = 0
        while c in da_dung:
            c = c + 1
        mau[v] = c
    return max(mau.values()) + 1

for V, E in ((10, 15), (7, 6), (12, 30)):
    print('V=' + str(V), 'E=' + str(E) + ': F=' + str(2 - V + E))
for V, E in ((7, 19), (8, 18), (6, 9)):
    print('V=' + str(V), 'E=' + str(E) + ':', 'khong phang' if E > 3 * V - 6 else 'chua ket luan')

n = 4
dinh = [('a', i) for i in range(n)] + [('b', i) for i in range(n)]
ke = {v: [u for u in dinh if u[0] != v[0] and u[1] != v[1]] for v in dinh}
xen_ke = [(s, i) for i in range(n) for s in 'ab']
a_truoc = [('a', i) for i in range(n)] + [('b', i) for i in range(n)]
print('do thi 4 cap (8 dinh): xen ke', tham_lam(dinh, ke, xen_ke), 'mau, a truoc b sau', tham_lam(dinh, ke, a_truoc), 'mau')

chu = list(range(5))
ke5 = {v: [(v + 1) % 5, (v - 1) % 5] for v in chu}
print('chu trinh 5 dinh: tham lam', tham_lam(chu, ke5, chu), 'mau, can tren', max(len(x) for x in ke5.values()) + 1)"""
EXP = make_lab(LID, DE, SOL)
print(EXP)

prac = practice(
    LID, "Tự làm: số mặt theo công thức Euler, giới hạn 3V − 6 và tô màu tham lam",
    "<p><b>Đề</b>: viết <code>phang.py</code> tính số mặt từ công thức Euler cho ba đồ thị phẳng, dùng $E \\le 3V - 6$ để loại ba đồ thị, và tô màu tham lam hai thứ tự cho một đồ thị vương miện 4 cặp, 8 đỉnh, "
    "cùng một chu trình 5 đỉnh (tám dòng, định dạng ở <code>labs/DMS/L18/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Đồ thị (6, 9) thoả bất đẳng thức mà vẫn không phẳng: máy chỉ nói “chưa kết luận”.</p>',
    "Bây giờ tới phần bạn tự làm. Hãy viết chương trình tính số mặt từ công thức Euler cho ba đồ thị phẳng. Sau đó dùng giới hạn số cạnh để loại ba đồ thị khác, và chú ý có một đồ thị thoả bất đẳng thức mà vẫn không phẳng. "
    "Cuối cùng tô màu tham lam một đồ thị vương miện bốn cặp, tám đỉnh, theo hai thứ tự, và một chu trình năm đỉnh. Tám dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "phang.py",
    '<div class="box key"><b>Nếu kẹt:</b> $V - E + F = 2$ nên $F = 2 - V + E$. Giới hạn: $E > 3V - 6$ thì chắc chắn không phẳng; ngược lại chưa kết luận được. '
    "Tham lam: với mỗi đỉnh, lấy tập màu của các đỉnh kề đã tô, rồi chọn số nguyên không âm nhỏ nhất không thuộc tập đó. "
    "Lời giải ở <code>labs/DMS/L18/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>",
    "Nếu kẹt, số mặt bằng hai trừ số đỉnh cộng số cạnh. Nếu số cạnh vượt ba lần số đỉnh trừ sáu thì đồ thị chắc chắn không phẳng, còn ngược lại thì chưa kết luận được. "
    "Với tô màu tham lam, mỗi đỉnh lấy tập màu của các đỉnh kề đã tô, rồi chọn số nhỏ nhất không thuộc tập đó. Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử.",
    pause=420, focus1=[1, 1, 1, 1, 2, 0])
patch_cham(prac, LID, "phang.py")

OBJ = [
    "Kiểm công thức V − E + F = 2 trên đồ thị phẳng liên thông",
    "Dùng E ≤ 3V − 6 để chứng minh một đồ thị không phẳng",
    "Tô màu tham lam và hiểu giới hạn của nó",
    "Đếm số màu của tô màu tham lam ở hai thứ tự khi đồ thị lớn dần và so với số màu tối thiểu",
    "Viết chương trình tính số mặt, kiểm giới hạn 3V − 6 và tô màu tham lam",
]
f, tpl, figs = apply(LID, quiz_pause=30, objectives=OBJ,
                     covers=[(1, "verify"), (2, "example"), (3, "coloring"), (4, "quymo"), (5, "practice")],
                     scenes=[(quymo, "pitfalls"), prac],
                     repl=asr_keep(LID) + [
                         # fix6b (P1): "phản chứng" định nghĩa tại chỗ
                         ("giả sử phản chứng $K_5$ phẳng rồi tính thẳng số mặt:", "giả sử ngược lại $K_5$ phẳng (phản chứng, tức đi tới mâu thuẫn) rồi tính thẳng số mặt:"),
                         ("Giả sử phản chứng K năm phẳng, theo công thức Euler", "Giả sử ngược lại K năm phẳng, cách này gọi là phản chứng, theo công thức Euler"),
                         # fix4 (R2 SHOULD B): tiền đề "mỗi mặt có ít nhất 3 cạnh" sai với đường 3 đỉnh (V=3, E=2) → thêm điều kiện E ≥ 3
                         ("không có cạnh nối một đỉnh với chính nó), $V \\ge 3$: $E \\le 3V - 6$.</p>",
                          "không có cạnh nối một đỉnh với chính nó), <b>liên thông</b>, $V \\ge 3$: $E \\le 3V - 6$. (Chứng minh dưới đây cần $E \\ge 3$; trường hợp $E < 3$ kiểm tay.)</p>"),
                         ("Ta dùng một bất đẳng thức, với đồ thị phẳng đơn có từ 3 đỉnh, số cạnh không vượt quá 3 lần số đỉnh trừ 6.",
                          "Ta dùng một bất đẳng thức, với đồ thị phẳng đơn liên thông có từ 3 đỉnh và ít nhất 3 cạnh, số cạnh không vượt quá 3 lần số đỉnh trừ 6."),
                         # fix6b (giới hạn từ 2 300 từ): lý do suy ra từng bước ở các step sau, bỏ hai câu lặp ở đây (có điều kiện ít nhất 3 cạnh)
                         ("Lý do, mỗi mặt có ít nhất 3 cạnh bao quanh, mỗi cạnh giáp nhiều nhất 2 mặt, nên 3 lần số mặt không vượt quá 2 lần số cạnh. Thay số mặt từ công thức Euler rồi rút gọn, ta được bất đẳng thức đó.",
                          "Lý do, khi có ít nhất 3 cạnh, sẽ được suy ra từng bước ngay sau đây."),
                         ('focus: ["1.2", "1.2", "1.2", "1.2", "1.2", "1.1"]', 'focus: ["1.2", "1.2", "1.2", "1.2", "1.1"]'),
                     ],
                     assumes_add=("dms_menhde", "dms_dinhly", "dms_taphop", "dms_phanvidu"))
print(figs)
print(fill(LID, {"K4": "audit/dms/fig/k4.svg", "K5": "audit/dms/fig/k5.svg", "GG": "audit/dms/fig/greedy_good.svg", "GB": "audit/dms/fig/greedy_bad.svg"}))
print(ledger_sync(LID, claims={"quymo": "20 đỉnh: thứ tự xen kẽ dùng 10 màu, a trước b sau 2 màu; 200 đỉnh: 100 màu và 2 màu"}))
