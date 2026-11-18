"""fix6 CS112 L19: bảng đọc cho gợi ý Tự làm + chân trang chấm bài. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l19.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L19")

edit(P, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> ba vòng lặp lồng nhau''', r'''      - show: |
          <p>Ba cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td>ba vòng <code>for</code> lồng nhau</td><td>vòng trong chạy lại từ đầu mỗi khi vòng ngoài sang một giá trị mới</td><td>hai vòng, mỗi vòng chạy 1, 2: cho các cặp (1, 1), (1, 2), (2, 1), (2, 2)</td></tr>
          <tr><td><code>j = i + độ dài - 1</code></td><td>gán: cuối đoạn j bằng đầu đoạn i cộng độ dài trừ 1</td><td>i = 1, độ dài 2: j = 2</td></tr>
          <tr><td><code>p[i-1] * p[k] * p[j]</code></td><td>ba số của danh sách p ở các vị trí i − 1, k, j (vị trí đếm từ 0), nhân với nhau</td><td>p = [10, 30, 5, 60], i = 1, k = 1, j = 2: 10 * 30 * 5 = 1500</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4"]
        say: "Gợi ý sắp tới dùng ba cách viết, nên ta đọc chúng trước. Ba vòng lặp lồng nhau nghĩa là vòng trong chạy lại từ đầu mỗi khi vòng ngoài sang một giá trị mới, như hai vòng cho bốn cặp. Cuối đoạn bằng đầu đoạn cộng độ dài trừ 1, ví dụ đầu là 1 và độ dài là 2 thì cuối là 2. Chi phí ghép nhân ba số của danh sách p ở các vị trí i trừ 1, k và j, đếm từ 0, ví dụ ba số đầu là 10, 30, 5 cho 1500."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> ba vòng lặp lồng nhau''')

patch_cham(P)
