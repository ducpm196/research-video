"""fix6 CS112 L18: vá MẪU L18_qhd.tpl.yaml (bảng đọc mã giả hai cách + gợi ý Tự làm) rồi sinh lại bài.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l18.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L18")

edit(T, r'''    steps:
      - show: |
          <div class="code"><div><span class="cm">// ① Từ trên xuống (ghi nhớ): memo[k] = -1 nghĩa là chưa tính</span></div>''', r'''    steps:
      - show: |
          <p>Hai cách viết bằng <b>mã giả</b> (các bước viết gần như mã thật, chưa chạy được), đọc từng dòng trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>memo[n] != -1</code></td><td><code>memo[n]</code> là ô số n của bảng ghi nhớ; <code>!=</code> nghĩa là khác; −1 là dấu “chưa tính”</td><td>memo[3] = 2: đã có, F(3) trả về 2 ngay</td></tr>
          <tr><td><code>return memo[n]</code></td><td>trả giá trị ra rồi thoát khỏi hàm</td><td>return 5: F(5) cho kết quả 5</td></tr>
          <tr><td><code>memo[n] = n nếu n &lt; 2, không thì F(n - 1) + F(n - 2)</code></td><td>dấu <code>=</code> là <b>gán</b>: ghi vào ô n chính n khi n nhỏ hơn 2, còn lại ghi tổng hai lời gọi nhỏ hơn</td><td>n = 4: ghi F(3) + F(2)</td></tr>
          <tr><td><code>dp[0] = 0;  dp[1] = 1</code></td><td>điền sẵn hai ô đầu của bảng <code>dp</code>; dấu chấm phẩy ngăn hai lệnh</td><td>bảng bắt đầu 0, 1</td></tr>
          <tr><td><code>for i = 2..n:  dp[i] = dp[i - 1] + dp[i - 2]</code></td><td><b>vòng lặp</b>: i lần lượt là 2, 3, … tới n; mỗi ô bằng tổng hai ô liền trước</td><td>dp[5] = dp[4] + dp[3] = 3 + 2 = 5</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4", "2.5", "2.6"]
        say: "Hai cách viết bằng mã giả, tức các bước viết gần như mã thật, nên ta đọc từng dòng trước. Dòng đầu kiểm ô số n của bảng ghi nhớ có khác trừ một không, khác nghĩa là đã tính rồi, nên dùng ngay. Lệnh trả về đưa giá trị ra và thoát khỏi hàm. Dòng gán ghi vào ô n chính n khi n nhỏ hơn 2, còn lại ghi tổng hai lời gọi nhỏ hơn. Ở cách hai, hai ô đầu của bảng được điền sẵn. Vòng lặp cho i chạy từ 2 tới n, mỗi ô bằng tổng hai ô liền trước."
      - show: |
          <div class="code"><div><span class="cm">① Từ trên xuống (ghi nhớ): memo[k] = -1 nghĩa là chưa tính</span></div>''')

edit(T, r'''<span class="cm">// ② Từ dưới lên (lập bảng): điền từ nhỏ đến lớn</span>''',
     r'''<span class="cm">② Từ dưới lên (lập bảng): điền từ nhỏ đến lớn</span>''')

edit(T, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> ô <code>dp[a]</code> bằng''', r'''      - show: |
          <p>Ba cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>dp[a - c]</code></td><td>ô của bảng ở vị trí a trừ c</td><td>a = 8, c = 4: ô dp[4]</td></tr>
          <tr><td><code>1 + min(dp[a - c])</code></td><td>1 cộng số nhỏ nhất trong các ô <code>dp[a - c]</code>, mỗi mệnh giá c cho một ô</td><td>a = 8, c là 1, 4, 6: 1 + min(dp[7], dp[4], dp[2]) = 1 + min(2, 1, 2) = 2</td></tr>
          <tr><td><code>1 + dp[a - c] == dp[a]</code></td><td>hai dấu bằng liền nhau là <b>so sánh</b>, cho đúng hoặc sai; một dấu bằng là gán</td><td>1 + 1 == 2 là đúng</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4"]
        say: "Gợi ý sắp tới dùng ba cách viết, nên ta đọc chúng trước. Dấu ngoặc vuông chỉ ô của bảng ở vị trí a trừ c, ví dụ a bằng 8 và c bằng 4 là ô số 4. Một cộng số nhỏ nhất trong các ô như vậy, mỗi mệnh giá cho một ô, ví dụ với 8 ra 2. Hai dấu bằng liền nhau là phép so sánh cho đúng hoặc sai, còn một dấu bằng là gán."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> ô <code>dp[a]</code> bằng''')

patch_cham(T)
regen("L18")
