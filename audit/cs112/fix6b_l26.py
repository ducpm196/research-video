"""fix6 CS112 L26: vá MẪU L26_p_np_quy_dan.tpl.yaml (bảng đọc bit_length trong gợi ý Tự làm, chân trang, cắt lời để bù) rồi sinh lại.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l26.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L26")

edit(T, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> duyệt kích thước tập''', r'''      - show: |
          <p>Một cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>W.bit_length()</code></td><td>số bit cần để ghi số nguyên W (số chữ số khi viết W ở hệ hai)</td><td>14 viết là 1110: 4 bit; 14000 cần 14 bit</td></tr></table>
        focus: [1, "2.2"]
        say: "Gợi ý sắp tới dùng một cách viết cần đọc trước. Lệnh đếm bit cho biết cần bao nhiêu chữ số nhị phân để ghi một số nguyên, ví dụ 14 viết là 1110, cần 4 bit."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> duyệt kích thước tập''')

# cắt lời để bù (không đụng các câu trong asr_reviewed)
edit(T, "Ở bài sau, bài 27, ta làm bài tập lớn, so sánh nhiều thuật toán có đo đạc, và ghi minh bạch phần việc của trí tuệ nhân tạo cùng phần mình tự kiểm chứng.",
     "Ở bài sau, bài 27, ta làm bài tập lớn, so sánh thuật toán có đo đạc, và ghi minh bạch phần việc của trí tuệ nhân tạo.")
edit(T, "nên mọi bài NP quy dẫn được về Y. Hai phép biến đa thức nối tiếp nhau vẫn là đa thức.",
     "nên mọi bài NP quy dẫn được về Y, và hai phép biến đa thức nối tiếp vẫn là đa thức.")
edit(T, "Hệ quả quan trọng là nếu tìm được thuật toán đa thức cho chỉ một bài NP đầy đủ, thì P bằng NP. Hơn 50 năm chưa ai làm được, nên khi gặp một bài NP khó, đừng",
     "Hệ quả là nếu tìm được thuật toán đa thức cho chỉ một bài NP đầy đủ, thì P bằng NP. Hơn 50 năm chưa ai làm được, nên gặp bài NP khó, đừng")
edit(T, "Nó đã giải đúng 5 thành phố với tối ưu 28, nhưng trường hợp tệ nhất vẫn phải thử rất nhiều nhánh.",
     "Nó giải đúng 5 thành phố, tối ưu 28, nhưng tệ nhất vẫn phải thử rất nhiều nhánh.")
edit(T, "cho mỗi món lấy nguyên hoặc bỏ, tổng khối lượng không vượt sức chứa, và tham lam theo đơn giá bị sai,",
     "cho mỗi món lấy nguyên hoặc bỏ, và tham lam theo đơn giá bị sai,")
edit(T, "Con số 5 cũng đếm lại được, năm đỉnh có 5 nhân 4 chia 2, bằng 10 cặp, bỏ 5 cặp nối nhau bằng một cạnh, còn đúng 5 cặp độc lập.",
     "Con số 5 đếm lại được: năm đỉnh có 5 nhân 4 chia 2, bằng 10 cặp, bỏ 5 cặp kề nhau, còn 5 cặp độc lập.")
edit(T, "Ngược lại, quy hoạch tuyến tính ở bài 22 thuộc P từ năm 1979, dù thuật toán đơn hình có thể chạy hàm mũ ở trường hợp tệ nhất.",
     "Ngược lại, quy hoạch tuyến tính ở bài 22 thuộc P từ năm 1979, dù đơn hình tệ nhất chạy hàm mũ.")
edit(T, "Điều đó trái với giả thiết tập độc lập lớn nhất chỉ có 3 đỉnh.", "Điều đó trái với giả thiết lớn nhất chỉ có 3 đỉnh.")

patch_cham(T)
regen("L26")
