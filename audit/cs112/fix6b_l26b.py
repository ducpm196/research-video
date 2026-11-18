"""fix6 CS112 L26 (đợt 2): tránh cụm 'chữ số nhị phân' (E52), trả câu quiz.3 về dạng ngắn, cắt thêm vài từ.
Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l26b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L26")
edit(T, '''        focus: [1, "2.2"]
        say: "Gợi ý sắp tới dùng một cách viết cần đọc trước. Lệnh đếm bit cho biết cần bao nhiêu chữ số nhị phân để ghi một số nguyên, ví dụ 14 viết là 1110, cần 4 bit."''',
     '''        focus: ["2.2"]
        say: "Gợi ý sắp tới dùng lệnh đếm bit, cho biết cần bao nhiêu chữ số khi viết một số nguyên ở hệ hai, ví dụ 14 viết là 1110, cần 4 bit."''')
edit(T, "nên mọi bài NP quy dẫn được về Y, và hai phép biến đa thức nối tiếp vẫn là đa thức.",
     "nên mọi bài NP quy dẫn được về Y. Hai phép biến đa thức nối tiếp vẫn là đa thức.")
edit(T, "Tự kiểm ba điều, vì sai chiều quy dẫn là kết luận ngược hẳn.", "Tự kiểm ba điều, vì sai chiều quy dẫn thì kết luận ngược.")
edit(T, "đó là một trong bảy bài toán thiên niên kỷ được treo thưởng từ năm 2000.", "đó là một trong bảy bài toán thiên niên kỷ, treo thưởng từ năm 2000.")
regen("L26")
