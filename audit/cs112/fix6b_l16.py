"""fix6 CS112 L16 (bảng đọc mã giả + đọc lệnh trong đề Tự làm). Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l16.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L16")

edit(P, r'''    title: "Quy tắc tham lam: đơn giá cao lấy trước"
    steps:
      - show: |
          <div class="code">''', r'''    title: "Quy tắc tham lam: đơn giá cao lấy trước"
    steps:
      - show: |
          <p>Quy tắc viết bằng <b>mã giả</b> (các bước viết gần như mã thật, chưa chạy được), đọc từng dòng trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>for mỗi món i theo thứ tự đó:</code></td><td><b>vòng lặp</b>: làm các dòng thụt vào bên dưới lần lượt cho từng món</td><td>món 2, rồi món 3, rồi món 1</td></tr>
          <tr><td><code>if w[i] &lt;= Rem:</code> … <code>else:</code></td><td>nếu khối lượng món i (viết <code>w[i]</code>) nhỏ hơn hoặc bằng chỗ còn trống <code>Rem</code> thì làm dòng này, ngược lại làm dòng <code>else</code></td><td>w[i] = 10, Rem = 15: vừa</td></tr>
          <tr><td><code>x[i] = 1;  Rem = Rem - w[i]</code></td><td>dấu <code>=</code> là <b>gán</b>: phần lấy của món i là 1 (cả món), chỗ trống giảm đúng khối lượng món</td><td>Rem = 20, w[i] = 15: Rem thành 5</td></tr>
          <tr><td><code>break</code></td><td>thoát vòng lặp ngay, không xét món còn lại</td><td>túi đầy thì dừng</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4", "2.5"]
        say: "Quy tắc viết bằng mã giả, tức các bước viết gần như mã thật, nên ta đọc từng dòng của nó trước. Dòng mở đầu là vòng lặp, làm các dòng thụt vào bên dưới lần lượt cho từng món. Dòng điều kiện hỏi khối lượng món có nhỏ hơn hoặc bằng chỗ còn trống không, nếu có thì làm dòng này, nếu không thì làm dòng kia. Dòng gán đặt phần lấy của món là 1, nghĩa là lấy cả món, và giảm chỗ trống đúng bằng khối lượng món. Dòng thoát cho vòng lặp dừng ngay, không xét món còn lại."
      - show: |
          <div class="code">''')

edit(P, r'''    steps:
      - show: |
          <p><b>Đề</b>: tạo <code>tui.py</code>''', r'''    steps:
      - show: |
          <p>Đề dùng hai mẩu mã, đọc trước khi làm:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>Fraction(p, w)</code></td><td><b>phân số chính xác</b> p trên w, không làm tròn; in ra viết <code>5/9</code>, hoặc <code>2</code> nếu chia hết</td><td><code>Fraction(25, 18)</code> in ra 25/18</td></tr>
          <tr><td><code>itertools.combinations(...)</code></td><td>liệt kê mọi cách chọn một số phần tử từ danh sách, không xét thứ tự, không lặp</td><td>chọn 2 từ [1, 2, 3] cho (1, 2), (1, 3), (2, 3)</td></tr></table>
        focus: [1, "2.2", "2.3"]
        say: "Đề dùng hai mẩu mã, nên ta đọc chúng trước. Phân số chính xác giữ nguyên p trên w, không làm tròn, in ra dạng năm phần chín, hoặc số nguyên nếu chia hết. Lệnh chọn tổ hợp liệt kê mọi cách chọn một số phần tử từ danh sách, không xét thứ tự và không lặp, ví dụ chọn hai từ ba số cho ba cặp."
      - show: |
          <p><b>Đề</b>: tạo <code>tui.py</code>''')

patch_cham(P)
