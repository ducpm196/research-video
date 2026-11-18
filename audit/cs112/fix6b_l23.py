"""fix6 CS112 L23: vá MẪU L23_sap_xep_nhanh.tpl.yaml (bảng đọc mã giả partition/quicksort, gợi ý Tự làm, cắt lời để bù) rồi sinh lại.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l23.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L23")

# 1. bảng đọc mã giả trước khối mã; đổi ghi chú // thành ngoặc
edit(T, r'''      - clear: true
        show: |
          <div class="code"><div>partition(a, lo, hi):        <span class="cm">// chốt p = a[hi]; i = cuối vùng số nhỏ</span></div>''', r'''      - clear: true
        show: |
          <p>Mã giả gồm hai hàm, nhận mảng <code>a</code> và một đoạn từ vị trí <code>lo</code> tới <code>hi</code>; đọc các dòng chính trước:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>p = a[hi];  i = lo - 1</code></td><td><code>a[hi]</code> là phần tử ở vị trí hi của mảng (đếm từ 0); gán nó làm chốt p; i = lo − 1 nghĩa là vùng số nhỏ lúc đầu rỗng</td><td>a = [4, 7, 2, 6, 1, 5], hi = 5: p = 5</td></tr>
          <tr><td><code>for j = lo .. hi - 1:</code></td><td><b>vòng lặp</b>: j chạy từ lo tới hi − 1, mọi vị trí đứng trước chốt</td><td>lo = 0, hi = 5: j = 0, 1, 2, 3, 4</td></tr>
          <tr><td><code>if a[j] &lt;= p:  i = i + 1;  đổi chỗ a[i], a[j]</code></td><td>nếu a[j] nhỏ hơn hoặc bằng chốt thì tăng i thêm 1 rồi đổi chỗ hai phần tử</td><td>a[j] = 2, i thành 1: đổi a[1] = 7 với a[2] = 2</td></tr>
          <tr><td><code>return i + 1</code></td><td>trả giá trị i + 1 ra, là vị trí của chốt, rồi thoát hàm</td><td>i = 2: trả về 3</td></tr>
          <tr><td><code>if lo &lt; hi:</code> … <code>quicksort(a, lo, q - 1)</code></td><td>chỉ làm khi đoạn còn ít nhất hai phần tử; hàm tự gọi lại chính nó (<b>đệ quy</b>) cho đoạn trái và đoạn phải của chốt q</td><td>đoạn 6 phần tử, q = 3: gọi cho 3 phần tử bên trái, 2 bên phải</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4", "2.5", "2.6"]
        say: "Mã giả gồm hai hàm, nhận mảng và một đoạn từ vị trí đầu tới vị trí cuối, nên ta đọc các dòng chính trước. Phần tử ở vị trí cuối của đoạn được gán làm chốt, còn i bằng đầu trừ 1 nghĩa là vùng số nhỏ lúc đầu rỗng. Vòng lặp cho j chạy từ đầu tới cuối trừ 1, tức mọi vị trí đứng trước chốt. Nếu phần tử thứ j không lớn hơn chốt thì tăng i thêm một rồi đổi chỗ hai phần tử. Lệnh trả về đưa vị trí của chốt ra ngoài rồi thoát hàm. Hàm sắp xếp nhanh chỉ làm khi đoạn còn ít nhất hai phần tử, rồi tự gọi lại chính nó cho đoạn trái và đoạn phải, đó là đệ quy."
      - clear: true
        show: |
          <div class="code"><div>partition(a, lo, hi):        <span class="cm">(chốt p = a[hi]; i = cuối vùng số nhỏ)</span></div>''')

# 2. gợi ý Tự làm: định nghĩa tại chỗ
edit(T, r'''<b>Nếu kẹt:</b> dùng hai biến toàn cục làm biến đếm và đặt lại về 0 trước mỗi lần chạy. Độ sâu tăng 1 mỗi lần gọi đệ quy.''',
     r'''<b>Nếu kẹt:</b> dùng hai <b>biến toàn cục</b> (biến đặt ngoài mọi hàm, hàm nào cũng đọc và sửa được) làm biến đếm và đặt lại về 0 trước mỗi lần chạy. Độ sâu (số lời gọi đang lồng nhau) tăng 1 mỗi lần gọi đệ quy.''')
edit(T, r'''say: "Nếu kẹt, dùng hai biến toàn cục làm biến đếm và đặt lại về 0 trước mỗi lần chạy. Độ sâu tăng một sau mỗi lần gọi đệ quy. Lời giải''',
     r'''say: "Nếu kẹt, dùng hai biến toàn cục làm biến đếm, tức biến đặt ngoài mọi hàm nên hàm nào cũng sửa được, và đặt lại về 0 trước mỗi lần chạy. Độ sâu, tức số lời gọi đang lồng nhau, tăng một sau mỗi lần gọi đệ quy. Lời giải''')
edit(T, r'''đếm so sánh và độ sâu đệ quy.</li>''', r'''đếm so sánh và độ sâu đệ quy (số lời gọi lồng nhau tại một lúc).</li>''')

# 3. cắt lời để bù (giữ số câu = số mục focus)
edit(T, "Chạy tay với mảng 4, 7, 2, 6, 1, 5, chốt là 5. Với j bằng 0, số 4 không lớn hơn 5, nên i thành 0 và 4 đổi chỗ với chính nó. Với j bằng 1, số 7 lớn hơn 5 nên giữ nguyên. Với j bằng 2, số 2 nhỏ hơn, i thành 1, đổi 2 lên trước 7. Tiếp theo 6 giữ nguyên, còn 1 được đổi vào ô thứ ba, đẩy 7 ra sau. Cuối cùng đổi chốt 5 vào ngay sau vùng số nhỏ.",
     "Chạy tay với mảng 4, 7, 2, 6, 1, 5, chốt là 5. Với j bằng 0, số 4 không lớn hơn 5, nên i thành 0. Với j bằng 1, số 7 lớn hơn 5 nên giữ nguyên. Với j bằng 2, số 2 nhỏ hơn, i thành 1, đổi 2 lên trước 7. Tiếp theo 6 giữ nguyên, còn 1 được đổi vào ô thứ ba. Cuối cùng đổi chốt 5 vào ngay sau vùng số nhỏ.")
edit(T, "Hoán vị là một thứ tự sắp xếp của n số, và ta lấy trung bình số so sánh trên mọi hoán vị. Máy vét cạn mọi hoán vị với n tới 7 và xác nhận công thức C của n bằng 2 nhân tổng n cộng một, nhân H n, trừ 4 n. Ta không suy ra công thức này ở đây, vì nó cần một hệ thức truy hồi riêng. Vì H n xấp xỉ lôgarit tự nhiên của n, phần chính là 2 n lôgarit tự nhiên của n,",
     "Hoán vị là một thứ tự của n số, và ta lấy trung bình số so sánh trên mọi hoán vị. Máy vét cạn mọi hoán vị với n tới 7 và xác nhận công thức C của n bằng 2 nhân tổng n cộng một, nhân H n, trừ 4 n. Ta không suy ra công thức này ở đây, vì nó cần một hệ thức truy hồi riêng. Phần chính của nó là 2 n lôgarit tự nhiên của n,")
edit(T, "Mảng đã sắp với chốt cuối tốn n nhân n trừ 1 chia 2, và mảng toàn số bằng nhau cũng vậy, với n bằng 6 là 15 phép so sánh. Nói đúng là trung bình, hay kỳ vọng khi chọn chốt ngẫu nhiên, với các số khác nhau, mới là Theta của n lôgarit n.",
     "Mảng đã sắp, và mảng toàn số bằng nhau, đều tốn n nhân n trừ 1 chia 2, với n bằng 6 là 15 phép so sánh. Nói đúng là trung bình, hay kỳ vọng khi chọn chốt ngẫu nhiên, với các số khác nhau, mới là Theta của n lôgarit n.")
edit(T, "Vì vậy độ cao h, cũng là số so sánh ở trường hợp tệ nhất, ít nhất bằng lôgarit cơ số 2 của n giai thừa. Vì nửa sau các thừa số của n giai thừa đều không nhỏ hơn n chia 2, nên n giai thừa",
     "Vậy độ cao h, cũng là số so sánh tệ nhất, ít nhất bằng lôgarit cơ số 2 của n giai thừa. Nửa sau các thừa số của n giai thừa đều không nhỏ hơn n chia 2, nên n giai thừa")
edit(T, "Sắp xếp chèn lấy lần lượt từng phần tử và chèn vào đúng chỗ trong phần đầu đã sắp. Mỗi nút",
     "Sắp xếp chèn chèn lần lượt từng phần tử vào đúng chỗ trong phần đầu đã sắp. Mỗi nút")
edit(T, "Năm phần tử có 5 giai thừa, bằng 120 thứ tự, mỗi thứ tự phải là một lá riêng. Cây cao 6",
     "Năm phần tử có 5 giai thừa, bằng 120 thứ tự, nên cần 120 lá. Cây cao 6")
# (không đổi câu ôn Theta/Omega: nó nằm trong asr_reviewed)

patch_cham(T)
regen("L23")
