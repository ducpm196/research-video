"""fix6 CS112 L21: vá MẪU L21_qhtt.tpl.yaml (bảng đọc Fraction, công thức trong gợi ý) + chân trang, rồi sinh lại bài.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l21.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen, patch_cham  # noqa

T = tpl("L21")

edit(T, r'''    steps:
      - show: |
          <p><b>Đề</b>: tạo <code>qhtt.py</code>.''', r'''    steps:
      - show: |
          <p>Đề dùng một mẩu mã, đọc trước khi làm:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>Fraction(a, b)</code></td><td><b>phân số chính xác</b> a trên b, không làm tròn; in ra viết <code>9/2</code>, hoặc <code>3</code> nếu chia hết</td><td><code>Fraction(9, 2)</code> in ra 9/2; cộng, trừ, nhân, chia các phân số vẫn ra phân số</td></tr></table>
        focus: [1, "2.2"]
        say: "Đề dùng một mẩu mã, nên ta đọc nó trước. Phân số chính xác giữ nguyên a trên b, không làm tròn, in ra dạng chín phần hai, hoặc số nguyên nếu chia hết, và các phép tính giữa chúng vẫn ra phân số."
      - show: |
          <p><b>Đề</b>: tạo <code>qhtt.py</code>.''')

edit(T, r'''      - show: |
          <div class="box key"><b>Nếu kẹt:</b> hai đường <code>a1*x + b1*y = c1</code>''', r'''      - show: |
          <p>Ba cách viết trong gợi ý sắp tới:</p>
          <table class="t"><tr><th>viết trong mã</th><th>đọc là</th><th>ví dụ</th></tr>
          <tr><td><code>a1*x + b1*y = c1</code></td><td>dấu <code>*</code> là nhân: đường thẳng thứ nhất có hệ số a1 (của x), b1 (của y), vế phải c1</td><td>x + y = 9: a1 = 1, b1 = 1, c1 = 9</td></tr>
          <tr><td><code>det = a1*b2 - a2*b1</code></td><td><b>định thức</b>: bằng 0 thì hai đường song song, không có giao điểm</td><td>với x + y = 9 và 3x + y = 18: 1*1 - 3*1 = -2</td></tr>
          <tr><td><code>x = (c1*b2 - c2*b1) / det</code></td><td>dấu <code>/</code> là chia: công thức cho số x của giao điểm; <code>y</code> có công thức tương tự</td><td>(9*1 - 18*1) / (-2) = 9/2: x của giao điểm là 9/2</td></tr></table>
        focus: [1, "2.2", "2.3", "2.4"]
        say: "Gợi ý sắp tới dùng ba cách viết, nên ta đọc chúng trước. Mỗi đường thẳng được viết bằng ba hệ số, a nhân x cộng b nhân y bằng c, ví dụ x cộng y bằng 9 có a bằng 1, b bằng 1, c bằng 9. Định thức tính từ các hệ số, bằng 0 thì hai đường song song, còn hai đường ví dụ cho trừ 2. Lấy tử số chia cho định thức ra số x của giao điểm, ví dụ chín phần hai."
      - show: |
          <div class="box key"><b>Nếu kẹt:</b> hai đường <code>a1*x + b1*y = c1</code>''')

patch_cham(T)
regen("L21")
