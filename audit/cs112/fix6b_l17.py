"""fix6 CS112 L17: vá MẪU L17_lap_lich.tpl.yaml (bảng đọc mã giả + đọc lệnh trong đề) rồi sinh lại bài.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l17.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham, lesson  # noqa

T = tpl("L17")

edit(T, r'''    steps:
      - show: |
          <div class="code"><div>sắp xếp theo f tăng dần;  last = -1   <span class="cm">// nhỏ hơn mọi giờ</span></div>''', r'''    steps:
      - show: |
          <p>Quy tắc viết bằng <b>mã giả</b> (các bước viết gần như mã thật, chưa chạy được), đọc từng dòng trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>last = -1</code></td><td>dấu <code>=</code> là <b>gán</b>: <code>last</code> là giờ kết thúc của sự kiện vừa chọn, lúc đầu là −1, nhỏ hơn mọi giờ</td><td>sự kiện đầu bắt đầu lúc 0 thì 0 &gt;= −1</td></tr>
          <tr><td><code>for mỗi sự kiện k theo thứ tự đó:</code></td><td><b>vòng lặp</b>: làm các dòng thụt vào bên dưới lần lượt cho từng sự kiện</td><td>sự kiện 1, rồi 2, rồi 3…</td></tr>
          <tr><td><code>if s[k] &gt;= last:</code></td><td>nếu giờ bắt đầu của sự kiện k (viết <code>s[k]</code>) lớn hơn hoặc bằng <code>last</code> thì làm dòng bên phải</td><td>s[k] = 5, last = 4: đúng</td></tr>
          <tr><td><code>chọn k;  last = f[k]</code></td><td>thêm k vào kết quả, rồi đặt <code>last</code> là giờ kết thúc của k (viết <code>f[k]</code>)</td><td>f[k] = 7 thì last thành 7</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4", "2.5"]
        say: "Quy tắc viết bằng mã giả, tức các bước viết gần như mã thật, nên ta đọc từng dòng trước. Dòng đầu gán cho giờ kết thúc vừa chọn giá trị trừ một, nhỏ hơn mọi giờ. Dòng lặp làm các dòng thụt vào bên dưới lần lượt cho từng sự kiện. Dòng điều kiện hỏi giờ bắt đầu của sự kiện có lớn hơn hoặc bằng giờ kết thúc vừa chọn không. Dòng chọn thêm sự kiện vào kết quả rồi đặt lại giờ kết thúc vừa chọn."
      - show: |
          <div class="code"><div>sắp xếp theo f tăng dần;  last = -1   <span class="cm">(−1 nhỏ hơn mọi giờ)</span></div>''')

edit(T, r'''    steps:
      - show: |
          <p><b>Đề</b>: tạo <code>lich.py</code>.''', r'''    steps:
      - show: |
          <p>Đề dùng ba mẩu mã, đọc trước khi làm:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>chon(ds, khoa)</code></td><td>hàm tên <code>chon</code> nhận danh sách sự kiện <code>ds</code> và <code>khoa</code>: cách tính số dùng để sắp xếp</td><td>khoá là giờ kết thúc f: sắp theo f</td></tr>
          <tr><td><code>s &gt;= last</code></td><td>s lớn hơn hoặc bằng last</td><td>4 &gt;= 4 là đúng; 3 &gt;= 4 là sai</td></tr>
          <tr><td><code>itertools.combinations(...)</code></td><td>liệt kê mọi cách chọn một số phần tử từ danh sách, không xét thứ tự, không lặp</td><td>chọn 2 từ [1, 2, 3] cho (1, 2), (1, 3), (2, 3)</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4"]
        say: "Đề dùng ba mẩu mã, nên ta đọc chúng trước. Hàm chọn nhận danh sách sự kiện và một khoá, tức cách tính con số dùng để sắp xếp, ví dụ khoá giờ kết thúc nghĩa là sắp theo giờ kết thúc. Dấu lớn hơn hoặc bằng cho kết quả đúng cả khi hai số bằng nhau, nên bốn lớn hơn hoặc bằng bốn là đúng. Lệnh chọn tổ hợp liệt kê mọi cách chọn một số phần tử, không xét thứ tự và không lặp, ví dụ chọn hai từ ba số cho ba cặp."
      - show: |
          <p><b>Đề</b>: tạo <code>lich.py</code>.''')

patch_cham(T)
regen("L17")
