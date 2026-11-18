"""fix6 CS112 L23 (đợt 2): rút gọn lời đọc để về ≤ 2300 từ. Chạy: .venv/Scripts/python -B audit/cs112/fix6b_l23b.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, tpl, regen  # noqa

T = tpl("L23")

edit(T, 'say: "Mã giả gồm hai hàm, nhận mảng và một đoạn từ vị trí đầu tới vị trí cuối, nên ta đọc các dòng chính trước. Phần tử ở vị trí cuối của đoạn được gán làm chốt, còn i bằng đầu trừ 1 nghĩa là vùng số nhỏ lúc đầu rỗng. Vòng lặp cho j chạy từ đầu tới cuối trừ 1, tức mọi vị trí đứng trước chốt. Nếu phần tử thứ j không lớn hơn chốt thì tăng i thêm một rồi đổi chỗ hai phần tử. Lệnh trả về đưa vị trí của chốt ra ngoài rồi thoát hàm. Hàm sắp xếp nhanh chỉ làm khi đoạn còn ít nhất hai phần tử, rồi tự gọi lại chính nó cho đoạn trái và đoạn phải, đó là đệ quy."',
     'say: "Mã giả gồm hai hàm, ta đọc các dòng chính trước. Phần tử ở vị trí cuối của đoạn làm chốt, còn i bằng đầu trừ 1 nghĩa là vùng số nhỏ lúc đầu rỗng. Vòng lặp cho j chạy từ đầu tới cuối trừ 1, tức mọi vị trí trước chốt. Nếu phần tử thứ j không lớn hơn chốt thì tăng i thêm một rồi đổi chỗ hai phần tử. Lệnh trả về đưa vị trí của chốt ra ngoài rồi thoát hàm. Hàm sắp xếp nhanh tự gọi lại chính nó cho đoạn trái và đoạn phải của chốt, đó là đệ quy."')

edit(T, "Viết thành mã như sau. Biến p giữ chốt, còn i đánh dấu chỗ cuối của vùng số nhỏ, lúc đầu vùng này rỗng. Biến j duyệt từ đầu đến trước chốt, mỗi bước là một phép so sánh. Gặp số không lớn hơn chốt, ta nới vùng số nhỏ thêm một ô và đổi số đó vào. Cuối cùng đổi chốt vào ngay sau vùng số nhỏ, rồi gọi đệ quy cho hai phần hai bên chốt.",
     "Đây là toàn bộ mã. Biến p giữ chốt, còn i đánh dấu chỗ cuối của vùng số nhỏ. Biến j duyệt từ đầu đến trước chốt, mỗi bước là một phép so sánh. Gặp số không lớn hơn chốt, ta nới vùng số nhỏ và đổi số đó vào. Cuối cùng đổi chốt vào ngay sau vùng số nhỏ, rồi gọi đệ quy cho hai bên.")

edit(T, "Khi đó chốt nằm đúng vị trí cuối cùng của nó trong mảng đã sắp. Rồi ta sắp tiếp hai phần hai bên theo cùng cách, và không cần bước trộn.",
     "Chốt khi đó nằm đúng vị trí cuối cùng của nó. Rồi ta sắp tiếp hai bên theo cùng cách, không cần bước trộn.")

edit(T, "Sắp xếp đếm dùng chính giá trị khoá làm chỉ số mảng, tức là đổi giả thiết, nên không trái với cận dưới. Đổi lại, nó cần khoá là số nguyên trong một khoảng nhỏ, k lớn quá thì mảng đếm quá to.",
     "Sắp xếp đếm dùng giá trị khoá làm chỉ số mảng, tức đổi giả thiết, nên không trái với cận dưới. Đổi lại, nó cần khoá là số nguyên trong khoảng nhỏ, k lớn quá thì mảng đếm quá to.")

edit(T, "Ở bài sau, bài 24, ta học tìm đường đi ngắn nhất trên đồ thị có trọng số, một thuật toán cho trường hợp mọi cạnh không âm, và một thuật toán khác khi có cạnh âm. Hẹn gặp bạn ở bài tiếp theo.",
     "Ở bài sau, bài 24, ta học đường đi ngắn nhất trên đồ thị có trọng số, khi cạnh không âm và cả khi có cạnh âm. Hẹn gặp bạn ở bài tiếp theo.")

regen("L23")
