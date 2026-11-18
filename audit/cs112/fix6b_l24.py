"""fix6 CS112 L24: vá MẪU L24_duong_di_ngan_nhat.tpl.yaml (bảng đọc hai vòng lặp của mã giả Dijkstra, cắt lời để bù) rồi sinh lại.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l24.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L24")

edit(T, r'''    steps:
      - show: |
          <div class="code"><div>d[S] = 0; mọi đỉnh khác d = $\infty$; tập đã chốt rỗng</div>''', r'''    steps:
      - show: |
          <p>Mã giả dùng hai vòng lặp, đọc trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>while còn đỉnh chưa chốt có d &lt; ∞:</code></td><td>vòng lặp <code>while</code>: lặp lại các dòng thụt vào chừng nào điều kiện còn đúng</td><td>còn đỉnh chưa chốt có d hữu hạn thì còn lặp</td></tr>
          <tr><td><code>for mỗi cạnh u → v với v chưa chốt:</code></td><td>vòng lặp <code>for</code>: làm dòng bên phải lần lượt cho từng cạnh đi ra từ u</td><td>u = A: chỉ có cạnh A → C</td></tr></table>
        focus: [1, "2.2", "2.3"]
        say: "Mã giả dùng hai vòng lặp, nên ta đọc chúng trước. Vòng lặp thứ nhất lặp lại các dòng thụt vào chừng nào điều kiện còn đúng, ở đây là còn đỉnh chưa chốt. Vòng lặp thứ hai làm dòng bên phải lần lượt cho từng cạnh đi ra từ đỉnh u."
      - show: |
          <div class="code"><div>d[S] = 0; mọi đỉnh khác d = $\infty$; tập đã chốt rỗng</div>''')

# cắt lời để bù (không đụng các câu trong asr_reviewed)
edit(T, "Một đồ thị gồm các đỉnh như S, A, B, nối với nhau bằng cạnh, và ở đây mỗi cạnh là một mũi tên một chiều mang một trọng số, chính là số phút.",
     "Một đồ thị gồm các đỉnh như S, A, B nối nhau bằng cạnh, ở đây mỗi cạnh là một mũi tên một chiều mang trọng số, chính là số phút.")
edit(T, "Trước hết, ta ôn lại vài điều sẽ dùng trong bài.", "Trước hết, ta ôn lại vài điều sẽ dùng.")
edit(T, "Đường đó phải ra khỏi vùng đã chốt tại một đỉnh chưa chốt x nào đó, và đoạn đầu tới x dài",
     "Đường đó phải ra khỏi vùng đã chốt tại một đỉnh chưa chốt x, và đoạn đầu tới x dài")
edit(T, "Nên độ dài của nó ít nhất bằng d của x cộng phần còn lại, mà phần còn lại không âm, và d của x không nhỏ hơn d của u.",
     "Nên độ dài của nó ít nhất d của x cộng phần còn lại không âm, mà d của x không nhỏ hơn d của u.")
edit(T, "Nếu mỗi lần chốt ta quét cả mảng, thì vì có n lần chốt, mỗi lần quét n đỉnh, nên tốn",
     "Nếu mỗi lần chốt ta quét cả mảng, có n lần chốt, mỗi lần quét n đỉnh, nên tốn")
edit(T, "Sau vòng thứ k, mọi đỉnh mà đường ngắn nhất tới nó dùng không quá k cạnh đã có d đúng, vì vòng k nới đúng cạnh thứ k của đường đó. Đây giống quy hoạch động ở bài 18, dùng kết quả của bài toán nhỏ hơn.",
     "Sau vòng thứ k, mọi đỉnh mà đường ngắn nhất tới nó dùng không quá k cạnh đã có d đúng. Cách làm này giống quy hoạch động ở bài 18.")
edit(T, "Nếu có chu trình tổng âm, như A tới B dài 1, B quay về A dài âm 3, tổng là âm 2. Khi đó cứ đi thêm một vòng là ngắn đi 2, nên không tồn tại đường ngắn nhất. Dấu hiệu nhận ra là sau n trừ 1 vòng mà vẫn còn cạnh nới được, nghĩa là có chu trình âm mà từ S đi tới được.",
     "Nếu có chu trình tổng âm, như A tới B dài 1, B quay về A dài âm 3, tổng là âm 2, thì cứ đi thêm một vòng là ngắn đi 2, nên không có đường ngắn nhất. Dấu hiệu là sau n trừ 1 vòng mà vẫn còn cạnh nới được, tức có chu trình âm mà từ S đi tới được.")
edit(T, "Kết quả trùng khớp, và vì đây là một thuật toán khác hẳn, sự trùng khớp là một bằng chứng độc lập.",
     "Kết quả trùng khớp, và vì đây là thuật toán khác hẳn, đó là bằng chứng độc lập.")
edit(T, "Chào bạn, đây là bản đồ đường một chiều, số trên mỗi mũi tên là số phút đi hết đoạn đó.",
     "Chào bạn, đây là bản đồ đường một chiều, số trên mỗi mũi tên là số phút đi đoạn đó.")

patch_cham(T)
regen("L24")
