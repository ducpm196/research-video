"""fix10 CS112 L15–L29 (R7_CS112_B): các mục riêng + yếu cùng họ + SHOULD (chữ). Bài sinh từ mẫu: sửa MẪU rồi regen.
Chạy: .venv/Scripts/python -B audit/cs112/fix10b_items.py  (chạy MỘT lần; mọi chỗ thay đã kiểm duy nhất trước khi ghi)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import rd, wr, lesson, tpl, regen, clear_next  # noqa

NL = chr(10)
OPS = []  # (path, old, new)


def E(path, old, new):
    OPS.append((path, old, new))


def APP(path, anchor, html):
    """chèn khối HTML mới ở CUỐI phần show của step chứa anchor (không đổi chỉ số khối cũ)"""
    OPS.append((path, ("APPEND", anchor), html))


L = lambda x: lesson(x)  # noqa
T = lambda x: tpl(x)  # noqa

# ---------- (2) mục riêng ----------
# L15: n!
p = L("L15")
E(p, "<p>5 thành phố: $4! = 24$ thứ tự. 20 thành phố:",
  "<p>$n! = n \\cdot (n - 1) \\cdot \\dots \\cdot 1$ (đọc <b>n giai thừa</b>), ví dụ $4! = 4 \\cdot 3 \\cdot 2 \\cdot 1 = 24$. 5 thành phố: $4! = 24$ thứ tự. 20 thành phố:")
E(p, "Bài toán là chọn thứ tự để tổng chi phí nhỏ nhất. Với 5 thành phố có 24 thứ tự",
  "Bài toán là chọn thứ tự để tổng chi phí nhỏ nhất. Ký hiệu n giai thừa là tích n nhân n trừ 1 và cứ thế tới 1, ví dụ 4 giai thừa bằng 24. Với 5 thành phố có 24 thứ tự")
E(p, "        focus: [1, 1, 2, 2]\n        say: \"Chào bạn, một người du lịch", "        focus: [1, 1, 2, 2, 2]\n        say: \"Chào bạn, một người du lịch")

# L17: [1, 4)
p = T("L17")
E(p, "Hôm nay ta chỉ cần so hai khoảng giờ.", "Hôm nay ta chỉ cần so hai khoảng giờ, viết với ngoặc vuông gồm điểm đầu và ngoặc tròn không gồm điểm cuối.")
APP(p, "<tr><td>[1, 4) và [3, 5)</td>", "<p class=\"note\">[a, b) = từ a tới b: ngoặc vuông <b>gồm</b> điểm đầu a, ngoặc tròn <b>không gồm</b> điểm cuối b.</p>")

# L18: Θ(n)
p = T("L18")
E(p, "nên chỉ tốn Theta của n.", "nên chỉ tốn Theta của n, tức số bước tăng cùng bậc với n: gấp đôi n thì gấp đôi số bước.")
APP(p, "<span class=\"cm\">② Từ dưới lên (lập bảng): điền từ nhỏ đến lớn</span>", "<p class=\"note\">$\\Theta(n)$: số bước tăng cùng bậc với $n$ (gấp đôi $n$ thì gấp đôi số bước).</p>")

# L22: <=  và công thức Klee–Minty
p = L("L22")
E(p, "ràng buộc 6x1 + 4x2 &lt;= 24 là hàng [6, 4] của A và số 24 của b", "ràng buộc 6x1 + 4x2 nhỏ hơn hoặc bằng 24 là hàng [6, 4] của A và số 24 của b")
E(p, "<li>Chạy hàm trên khối Klee–Minty $n = 4$ với hai quy tắc chọn cột.</li></ol>",
  "<li>Chạy hàm trên khối Klee–Minty $n = 4$ với hai quy tắc chọn cột: $c_j = 2^{n-j}$; $A_{ij} = 2^{i-j+1}$ nếu $j < i$, $1$ nếu $j = i$, $0$ nếu $j > i$; $b_i = 5^i$ ($i, j$ từ 1 tới $n$).</li></ol>")

# L26: bit trước sym; bỏ bước bảng bit_length cũ ở gợi ý; chứng chỉ
p = T("L26")
tt, crlf26 = rd(p)
a = tt.index("      - clear: true" + NL + "        show: |" + NL + "          <p>Một cách viết trong gợi ý sắp tới:</p>")
b = tt.index("      - clear: true", a + 10)
tt = tt[:a] + tt[b:]
wr(p, tt, crlf26)
E(p, "    steps:" + NL + "      - show: |" + NL + "          <p><b>Bài toán quyết định</b>: đáp án là có hoặc không.",
  "    steps:" + NL + "      - show: |" + NL +
  "          <table class=\"t\"><tr><th>đọc trước: ký hiệu</th><th>đọc là</th><th>ví dụ</th></tr>" + NL +
  "          <tr><td>bit</td><td>một chữ số 0 hoặc 1 khi viết số ở hệ hai</td><td>14 viết là 1110: 4 bit</td></tr>" + NL +
  "          <tr><td><code>W.bit_length()</code></td><td>số bit cần để ghi số nguyên W, khoảng $\\log_2 W$</td><td>14 → 4 bit; 14000 → 14 bit; $10^9$ → 30 bit</td></tr></table>" + NL +
  "        focus: [\"1.2\", \"1.3\"]" + NL +
  "        say: \"Bit là một chữ số 0 hoặc 1 khi viết số ở hệ hai, ví dụ 14 viết là 1110, cần 4 bit. Một số W cần khoảng lôgarit cơ số 2 của W bit, ví dụ một tỉ chỉ cần 30 bit.\"" + NL +
  "      - clear: true" + NL + "        show: |" + NL + "          <p><b>Bài toán quyết định</b>: đáp án là có hoặc không.")
E(p, "tồn tại một <b>chứng chỉ</b> để <b>kiểm</b> trong thời gian đa thức.</p>",
  "tồn tại một <b>chứng chỉ</b> (bằng chứng ngắn cho đáp án “có”) để <b>kiểm</b> trong thời gian đa thức.</p>")

# L28: ε và tổng Sigma
p = L("L28")
APP(p, "$f(n) = 1 = O(n^{1 - \\varepsilon})$", "<p class=\"note\">$\\varepsilon$ (đọc: ép-xi-lon) là một số dương nhỏ tuỳ ý, ví dụ $0{,}1$: khi đó $n^{1-\\varepsilon} = n^{0{,}9}$.</p>")
E(p, "nên trường hợp một, Theta của n, thử T của 27 bằng 13.", "nên trường hợp một, Theta của n. Ở đây ép-xi-lon là một số dương nhỏ tuỳ ý, ví dụ 0 phẩy 1. Thử T của 27 bằng 13.")
E(p, "đếm số bước, tổng Sigma, O, Ω, Θ, giới hạn tỉ số", "đếm số bước, tổng Sigma (cộng lại nhiều số hạng), O, Ω, Θ, giới hạn tỉ số")

# ---------- (3) yếu cùng họ ----------
# L16: Σ
p = L("L16")
E(p, "để $\\ \\displaystyle\\sum p_i\\,x_i$ lớn nhất,", "để $\\ \\displaystyle\\sum p_i\\,x_i$ (∑ = cộng lại mọi số hạng: $p_1x_1 + p_2x_2 + p_3x_3$) lớn nhất,")
# L19, L20, L24, L25: Θ
E(L("L19"), "tức $\\Theta(n^3)$, và bảng có", "tức $\\Theta(n^3)$ ($\\Theta$ = cùng bậc tăng: $n$ gấp 10 thì $n^3$ gấp 1 000), và bảng có")
E(L("L20"), "mỗi $i$ nhìn mọi $j < i$ → $\\Theta(n^2)$.</p>", "mỗi $i$ nhìn mọi $j < i$ → $\\Theta(n^2)$ ($\\Theta$ = cùng bậc tăng: $n$ gấp đôi thì số bước gấp 4).</p>")
E(T("L24"), "cập nhật trong $\\Theta(\\log_2 n)$", "cập nhật trong $\\Theta(\\log_2 n)$ ($\\Theta$ = cùng bậc tăng, ở đây cỡ $\\log_2 n$)")
E(T("L25"), "lấy phần tử nhỏ nhất trong $\\Theta(\\log_2 n)$.</li>", "lấy phần tử nhỏ nhất trong $\\Theta(\\log_2 n)$ ($\\Theta$ = cùng bậc tăng).</li>")
# L23: log2, lá, ⌈⌉, khoá + SHOULD 2000
p = T("L23")
APP(p, "nhưng cần thêm <b>một mảng phụ</b> $n$ ô để trộn.</p>", "<p class=\"note\">$\\log_2 n$ = số lần chia đôi $n$ để còn 1 (ví dụ $n = 8$: 3 lần).</p>")
APP(p, "mỗi nút là một phép so sánh, mỗi l", "<p class=\"note\">lá = nút ở cuối cây, không có nút con; cây nhị phân: mỗi nút có tối đa 2 con.</p>")
APP(p, "$\\lceil\\log_2 720\\rceil = \\lceil 9{,}49\\rceil = 10$", "<p class=\"note\">$\\lceil x \\rceil$ = làm tròn <b>lên</b> thành số nguyên (ví dụ $\\lceil 9{,}49 \\rceil = 10$).</p>")
E(p, "<p>Khoá là số nguyên từ 0 đến $k = 3$:", "<p>Khoá (giá trị dùng để sắp xếp) là số nguyên từ 0 đến $k = 3$:")
E(p, "báo lỗi tràn <b>ngăn xếp</b> (nơi máy nhớ các lời gọi đang chạy dở) từ $n = 2\\,000$", "báo lỗi tràn <b>ngăn xếp</b> (nơi máy nhớ các lời gọi đang chạy dở) từ khoảng $n = 1\\,000$")
E(p, "nên với 2000 phần tử đã vượt giới hạn mặc định khoảng 1000 tầng và báo lỗi tràn ngăn xếp.", "nên từ khoảng 1000 phần tử đã vượt giới hạn mặc định 1000 tầng và báo lỗi tràn ngăn xếp.")
# L24: chu trình âm, 32 bit, nhãn cột
p = T("L24")
E(p, "<th>nới mọi cạnh, dừng khi không đổi</th>", "<th>nới mọi cạnh, dừng khi không đổi (tối đa $n - 1$ vòng)</th>")
APP(p, "báo có chu trình âm (tới được từ S)", "<p class=\"note\">chu trình âm = đường đi vòng về chỗ cũ mà tổng trọng số nhỏ hơn 0: đi thêm một vòng là ngắn đi.</p>")
APP(p, "$2^{31} - 1$ cộng 1 bị tràn", "<p class=\"note\">số nguyên 32 bit: ghi bằng 32 chữ số 0 hoặc 1, lớn nhất $2^{31} - 1$; cộng thêm 1 thì “tràn”, quay vòng sang số âm nhỏ nhất.</p>")
# L29: CAV, phản ví dụ
p = L("L29")
E(p, "bài báo hội nghị CAV 2015 ghi", "bài báo hội nghị CAV 2015 (hội nghị quốc tế về kiểm chứng bằng máy) ghi")
E(p, "<p>Phản ví dụ nhỏ nhất là một mảng", "<p><b>Phản ví dụ</b> (ví dụ cụ thể làm kết luận sai) nhỏ nhất là một mảng")

# ---------- kiểm duy nhất rồi ghi ----------
by = {}
for path, old, new in OPS:
    by.setdefault(str(path), []).append((old, new))
texts = {}
for path, ops in by.items():
    t, crlf = rd(path)
    for old, new in ops:
        if isinstance(old, tuple):
            n = t.count(old[1])
            assert n == 1, f"{Path(path).name}: anchor {n} lần: {old[1][:60]!r}"
            i = t.index(old[1])
            js = [t.find(NL + "        " + k, i) for k in ("focus:", "say:", "pause:", "introduces:")]
            j = min(x for x in js if x > 0)
            t = t[:j] + NL + "          " + new + t[j:]
        else:
            n = t.count(old)
            assert n == 1, f"{Path(path).name}: cần 1 chỗ, thấy {n}: {old[:70]!r}"
            t = t.replace(old, new)
    texts[path] = (t, crlf)
for path, (t, crlf) in texts.items():
    wr(path, t, crlf)
    print("ghi", Path(path).name)

# bước sau bảng mới cần clear
clear_next(T("L26"), "ví dụ một tỉ chỉ cần 30 bit")
for lid in ("L17", "L18", "L23", "L24", "L25", "L26"):
    regen(lid)
