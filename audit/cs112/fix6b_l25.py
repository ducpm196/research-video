"""fix6 CS112 L25: vá MẪU L25_cay_khung_nho_nhat.tpl.yaml (bảng đọc mã giả hợp–tìm + gợi ý Tự làm + chân trang) rồi sinh lại.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l25.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L25")

edit(T, r'''    steps:
      - show: |
          <div class="code"><div>find(x):</div>''', r'''    steps:
      - show: |
          <p>Mã giả của hợp–tìm có bốn cách viết cần đọc trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>cha[x] != x</code></td><td><code>cha[x]</code> là cha của x trong cây của nhóm; <code>!=</code> là “khác”; gốc là nút có cha chính là nó</td><td>cha[5] = 4: 5 chưa phải gốc; cha[1] = 1: 1 là gốc</td></tr>
          <tr><td><code>cha[x] = find(cha[x])</code></td><td>dấu <code>=</code> là <b>gán</b>: hàm <code>find</code> tự gọi lại chính nó (<b>đệ quy</b>) để tìm gốc, rồi ghi thẳng gốc vào <code>cha[x]</code> — đó là nén đường</td><td>chuỗi 5 → 4 → 3 → 2 → 1: sau find(5), cha[5] = 1</td></tr>
          <tr><td><code>ra == rb</code></td><td>hai dấu bằng liền nhau là <b>so sánh</b>, cho đúng hoặc sai; <code>ra</code>, <code>rb</code> là gốc của hai nhóm</td><td>find(3) == find(5) đúng: 3 và 5 đã cùng nhóm</td></tr>
          <tr><td><code>return</code></td><td>trả kết quả ra rồi thoát hàm</td><td>find(5) trả về gốc 1</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4", "2.5"]
        say: "Mã giả của hợp và tìm có bốn cách viết cần đọc trước. Ô cha của x là cha của x trong cây nhóm, và điều kiện khác nghĩa là x chưa phải gốc. Hàm tìm tự gọi lại chính nó, tức đệ quy, để tìm gốc rồi ghi thẳng gốc vào ô cha, đó là nén đường. Hai dấu bằng liền nhau là phép so sánh cho đúng hoặc sai, nên hai gốc trùng nhau nghĩa là hai đỉnh cùng nhóm. Lệnh trả về đưa kết quả ra rồi thoát hàm, ví dụ hàm tìm của đỉnh 5 trả về gốc 1."
      - clear: true
        show: |
          <div class="code"><div>find(x):</div>''')

edit(T, r'''<span class="cm">// lên gốc, nén đường</span>''', r'''<span class="cm">(lên gốc, nén đường)</span>''')

edit(T, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> cạnh chỉ được lấy khi''', r'''      - show: |
          <p>Hai cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>union(a, b)</code> trả <code>False</code></td><td>hợp hai nhóm của a và b; trả <code>True</code> (đúng) khi vừa hợp, <code>False</code> (sai) khi a và b đã cùng nhóm</td><td>union(1, 2) trả True; gọi lại lần nữa trả False</td></tr>
          <tr><td><code>(đầu 1 trong cây) != (đầu 2 trong cây)</code></td><td><code>!=</code> là “khác”: đúng khi một đầu của cạnh ở trong cây còn đầu kia ở ngoài</td><td>đầu 1 trong cây (True), đầu 2 ngoài cây (False): True != False là đúng</td></tr></table>
        focus: [1, "2.2", "2.3"]
        say: "Gợi ý sắp tới dùng hai cách viết, nên ta đọc chúng trước. Hàm hợp trả về đúng khi vừa hợp hai nhóm, và trả về sai nếu hai đỉnh đã cùng nhóm. Dấu khác cho kết quả đúng khi một đầu của cạnh ở trong cây còn đầu kia ở ngoài."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> cạnh chỉ được lấy khi''')

patch_cham(T)
regen("L25")
