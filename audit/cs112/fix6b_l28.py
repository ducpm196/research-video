"""fix6 CS112 L28: bảng đọc mã giả của ví dụ (if/==/return, for, đệ quy) + math.log2 trong gợi ý + chân trang; cắt lời để bù.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l28.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, patch_cham  # noqa

P = lesson("L28")

edit(P, r'''    steps:
      - show: |
          <div class="code"><div>f(A, n):</div>''', r'''    steps:
      - show: |
          <p>Mã giả của ví dụ có ba cách viết cần đọc trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>if n == 1: return</code></td><td>hai dấu bằng liền nhau là <b>so sánh</b>, cho đúng hoặc sai; <code>return</code> thoát khỏi hàm ngay, nên đoạn một phần tử không làm gì</td><td>n = 1: thoát; n = 8: đi tiếp</td></tr>
          <tr><td><code>for i = 1..n: làm 1 bước</code></td><td><b>vòng lặp</b>: i chạy từ 1 tới n, mỗi lượt một bước, tổng n bước</td><td>n = 8: 8 bước</td></tr>
          <tr><td><code>f(nửa trái, n/2)</code></td><td>hàm f tự gọi lại chính nó (<b>đệ quy</b>) trên nửa mảng, cỡ n/2</td><td>n = 8: hai lời gọi cỡ 4</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4"]
        say: "Mã giả của ví dụ có ba cách viết cần đọc trước. Hai dấu bằng liền nhau là phép so sánh cho đúng hoặc sai, còn lệnh trả về thoát khỏi hàm ngay. Vòng lặp cho i chạy từ 1 tới n, mỗi lượt làm một bước, nên tổng cộng n bước. Hàm tự gọi lại chính nó cho mỗi nửa, cỡ n chia 2, đó là đệ quy."
      - clear: true
        show: |
          <div class="code"><div>f(A, n):</div>''')
edit(P, '<span class="cm">// n bước</span>', '<span class="cm">(n bước)</span>')
edit(P, '<span class="cm">// cả hai đều chạy</span>', '<span class="cm">(cả hai đều chạy)</span>')
edit(P, "<b>Nếu kẹt:</b> hệ thức $A$ có", "<b>Nếu kẹt:</b> hệ thức $A$ có")
edit(P, "Hãy dùng <code>math.log2</code>. Lời giải", "Hãy dùng <code>math.log2</code> (<code>math.log2(8)</code> là 3, lôgarit cơ số 2). Lời giải")

# cắt lời để bù (không đụng câu nằm trong asr_reviewed)
edit(P, "Hàm này làm n bước, rồi gọi đệ quy cả hai nửa, cả hai lời gọi đều chạy. Bước một,", "Hàm này làm n bước, rồi gọi đệ quy cả hai nửa. Bước một,")
edit(P, "Lôgarit trả lời câu hỏi mũ mấy, 2 mũ 3 bằng 8 nên lôgarit cơ số 2 của 8 bằng 3, và 3 mũ 1 bằng 3 nên lôgarit cơ số 3 của 3 bằng 1.",
     "Lôgarit trả lời câu hỏi mũ mấy, 2 mũ 3 bằng 8 nên lôgarit cơ số 2 của 8 bằng 3.")
edit(P, "Chào bạn, đây là bài tổng ôn của khoá, nơi ta xếp hai mươi tám bài vào sáu nhóm.", "Chào bạn, đây là bài tổng ôn, nơi ta xếp hai mươi tám bài vào sáu nhóm.")
edit(P, "Nhóm hai là hệ thức truy hồi, với thế ngược, hàm sinh, đổi biến, định lý thợ và quy nạp.", "Nhóm hai là các hệ thức truy hồi và cách giải chúng.")
edit(P, "Nhóm ba là các chiến lược thiết kế, từ chia để trị tới quay lui, nhánh cận và tham lam.", "Nhóm ba là các chiến lược thiết kế, từ chia để trị tới tham lam.")
edit(P, "Nhóm sáu là sắp xếp, đồ thị và độ khó của bài toán, với cây quyết định, phép nới cạnh, tính chất lát cắt và phép quy dẫn.",
     "Nhóm sáu là sắp xếp, đồ thị và độ khó của bài toán, với cây quyết định và phép quy dẫn.")
edit(P, "Bẫy ba, viết định nghĩa tiệm cận thiếu phần tồn tại hay phần với mọi, hãy đọc to đủ cả hai vế của lời hứa.",
     "Bẫy ba, định nghĩa tiệm cận thiếu phần tồn tại hay phần với mọi, hãy đọc to đủ hai vế của lời hứa.")
edit(P, "Ở bài sau, bài 29, cũng là bài cuối của khoá, ta đi theo dòng thời gian của một thuật toán sắp xếp thật. Hành trình đi từ năm 2002 tới khi",
     "Ở bài sau, bài 29, bài cuối của khoá, ta đi theo dòng thời gian của một thuật toán sắp xếp thật, từ năm 2002 tới khi")
patch_cham(P)
