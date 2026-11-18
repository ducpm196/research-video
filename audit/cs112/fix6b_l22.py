"""fix6 CS112 L22: bảng đọc cho đề + gợi ý Tự làm, chân trang chấm bài, bỏ số bổ đề CLRS chưa kiểm được ở header source.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l22.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L22")

edit(P, "Cormen và cộng sự, Introduction to Algorithms, bản 3, Bổ đề 29.7)",
     "Cormen và cộng sự, Introduction to Algorithms, bản 3, chương Quy hoạch tuyến tính; SỐ bổ đề chưa kiểm được với sách nên không ghi)")

edit(P, r'''    steps:
      - show: |
          <p><b>Đề</b>: tạo <code>donhinh.py</code>''', r'''    steps:
      - show: |
          <p>Đề dùng hai mẩu mã, đọc trước khi làm:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>don_hinh(c, A, b, quy_tac)</code></td><td>hàm đơn hình nhận bốn đầu vào: <code>c</code> là các hệ số của hàm mục tiêu, <code>A</code> là bảng hệ số vế trái (mỗi hàng một ràng buộc), <code>b</code> là các vế phải, <code>quy_tac</code> là cách chọn cột vào</td><td>z = 5x1 + 4x2 thì c = [5, 4]; ràng buộc 6x1 + 4x2 &lt;= 24 là hàng [6, 4] của A và số 24 của b</td></tr>
          <tr><td><code>Fraction(a, b)</code></td><td><b>phân số chính xác</b> a trên b, không làm tròn; in ra viết <code>3/2</code>, hoặc <code>3</code> nếu chia hết</td><td><code>Fraction(3, 2)</code> in ra 3/2; phép xoay trên các phân số không mất độ chính xác</td></tr></table>
        focus: [1, "2.2", "2.2", "2.3"]
        say: "Đề dùng hai mẩu mã, nên ta đọc chúng trước. Hàm đơn hình nhận bốn đầu vào: hệ số hàm mục tiêu, bảng hệ số vế trái của các ràng buộc, các vế phải, và cách chọn cột vào. Ví dụ, hàm mục tiêu năm x một cộng bốn x hai cho danh sách năm, bốn, còn ràng buộc đầu cho hàng sáu, bốn và số 24. Phân số chính xác giữ nguyên a trên b, không làm tròn, nên phép xoay không mất độ chính xác."
      - show: |
          <p><b>Đề</b>: tạo <code>donhinh.py</code>''')

edit(P, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> bảng có <code>m</code> hàng ràng buộc''', r'''      - show: |
          <p>Hai cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>-c</code></td><td>đổi dấu từng hệ số của <code>c</code>: hàng <code>z</code> của bảng bắt đầu bằng các số đối</td><td>c = [5, 4] thì hàng z bắt đầu −5, −4</td></tr>
          <tr><td><code>(hệ số ở cột vào) * hàng ra</code></td><td>dấu <code>*</code> là nhân: nhân mọi ô của hàng ra với hệ số của hàng đang sửa ở cột vào, rồi trừ</td><td>hệ số −3 thì trừ (−3) lần hàng ra, tức cộng 3 lần hàng ra</td></tr></table>
        focus: [1, "2.2", "2.3"]
        say: "Gợi ý sắp tới dùng hai cách viết, nên ta đọc chúng trước. Dấu trừ trước danh sách hệ số nghĩa là đổi dấu từng số, nên hàng z bắt đầu bằng các số đối của hệ số hàm mục tiêu. Dấu sao là phép nhân, trừ hệ số ở cột vào nhân hàng ra nghĩa là nếu hệ số là âm ba thì thực chất cộng ba lần hàng ra."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> bảng có <code>m</code> hàng ràng buộc''')

patch_cham(P)
