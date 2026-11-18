"""fix10 CS112 (đợt cắt lời): rút ngắn lời đọc về ≤ 2300 từ sau khi thêm bước Git Bash và định nghĩa thuật ngữ. Chạy một lần."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import edit, lesson, tpl, regen  # noqa

TPL = {"L17", "L18", "L21", "L23", "L24", "L25", "L26"}
G_OLD = "Git Bash là cửa sổ gõ lệnh trên Windows, mở bằng cách vào thư mục bài làm, bấm chuột phải rồi chọn mở Git Bash tại đây. Gõ lệnh đầu để chạy chương trình, gõ lệnh sau để chấm, lệnh chấm in chữ ĐÚNG khi mọi dòng khớp."
G_NEW = "Git Bash là cửa sổ gõ lệnh trên Windows, mở bằng chuột phải trong thư mục bài làm. Gõ lệnh đầu để chạy chương trình, lệnh sau để chấm, lệnh chấm in chữ ĐÚNG khi mọi dòng khớp."
P = lambda lid: tpl(lid) if lid in TPL else lesson(lid)  # noqa
for n in range(15, 30):
    edit(P(f"L{n}"), G_OLD, G_NEW)

# L22
p = P("L22")
edit(p, "Ở bài sau, bài 23, ta học sắp xếp nhanh, và giới hạn của sắp xếp bằng so sánh, tức vì sao mọi thuật toán so sánh đều có một giới hạn tốc độ.",
     "Ở bài sau, bài 23, ta học sắp xếp nhanh và giới hạn tốc độ của mọi thuật toán sắp xếp bằng so sánh.")
edit(p, "Quy tắc đó chọn cột vào là biến có chỉ số nhỏ nhất trong các cột có hệ số âm, thay cho cột âm nhất. Khi các tỉ số hoà, nó chọn hàng của biến có chỉ số nhỏ nhất. Trường hợp tệ nhất, đơn hình vẫn có thể đi qua số đỉnh tăng theo hàm mũ, dù ở các bài ngẫu nhiên đo trong bài này nó rất nhanh.",
     "Quy tắc đó chọn cột vào là biến có chỉ số nhỏ nhất trong các cột có hệ số âm, và khi tỉ số hoà thì chọn hàng của biến có chỉ số nhỏ nhất. Tệ nhất, đơn hình vẫn có thể đi qua số đỉnh tăng theo hàm mũ, dù ở các bài ngẫu nhiên nó rất nhanh.")
# L23
p = P("L23")
edit(p, "Ở bài sau, bài 24, ta học đường đi ngắn nhất trên đồ thị có trọng số, khi cạnh không âm và cả khi có cạnh âm.", "Ở bài sau, bài 24, ta học đường đi ngắn nhất trên đồ thị có trọng số.")
edit(p, "Điều cần mang theo, một cận dưới luôn đi kèm mô hình tính toán của nó. Trước khi nói không thể nhanh hơn, hãy hỏi thuật toán được phép làm những thao tác gì.",
     "Điều cần mang theo, một cận dưới luôn đi kèm mô hình tính toán của nó, nên trước khi nói không thể nhanh hơn, hãy hỏi thuật toán được làm những thao tác gì.")
edit(p, "Tổng kết chuỗi logic. Phân hoạch quanh chốt tốn n trừ 1 phép so sánh. Sắp xếp nhanh tệ nhất", "Tổng kết chuỗi logic. Sắp xếp nhanh tệ nhất")
edit(p, "đều tốn n nhân n trừ 1 chia 2, với n bằng 6 là 15 phép so sánh.", "đều tốn n nhân n trừ 1 chia 2, với n bằng 6 là 15.")
# L24
p = P("L24")
edit(p, "Điều cần mang theo, một chiến lược tham lam thường đúng nhờ một giả thiết, ở đây là không có cạnh âm. Khi dùng, luôn hỏi giả thiết đó có còn đúng với dữ liệu của mình không.",
     "Điều cần mang theo, tham lam thường đúng nhờ một giả thiết, ở đây là không có cạnh âm, nên hãy hỏi giả thiết đó có còn đúng với dữ liệu của mình không.")
edit(p, "Ở bài sau, bài 25, ta học cây khung nhỏ nhất, cách nối mọi đỉnh với tổng chi phí nhỏ nhất, cùng một cấu trúc dữ liệu gọi là hợp và tìm.", "Ở bài sau, bài 25, ta học cây khung nhỏ nhất và cấu trúc hợp và tìm.")
edit(p, "Với số nguyên 32 bit, số lớn nhất cộng 1 bị tràn, trong Java nó thành một số âm cực nhỏ, và cả bảng d sai.", "Số nguyên 32 bit lớn nhất cộng 1 bị tràn thành số âm cực nhỏ, làm cả bảng d sai.")
# L26
p = P("L26")
edit(p, "Điều cần mang theo, chứng minh được một bài toán là khó cũng là một kết quả có giá trị. Nó cho biết nên đổi hướng tiếp cận, thay vì tìm mãi một thuật toán chưa ai tìm ra.",
     "Điều cần mang theo, chứng minh một bài toán là khó cũng là kết quả có giá trị. Nó cho biết nên đổi hướng, thay vì tìm mãi một thuật toán chưa ai tìm ra.")
edit(p, " Các bài NP đầy đủ là khó nhất trong NP. Gặp bài NP khó,", " Gặp bài NP khó,")
edit(p, "Đa số nhà nghiên cứu tin như vậy, nhưng đến nay chưa có chứng minh, câu đúng là chưa biết.", "Đa số tin như vậy, nhưng chưa có chứng minh, câu đúng là chưa biết.")
edit(p, ", trong khi bảng sẽ cần tới khoảng 5 nhân 10 mũ 13 ô.", ".")
# L28
p = P("L28")
edit(p, "Ta bắt đầu từ đếm số bước, nói gọn bằng các ký hiệu tiệm cận, rồi biến đệ quy thành hệ thức và giải. Sau đó chọn chiến lược thiết kế phù hợp, và luôn kết thúc bằng một chứng minh hoặc một phép kiểm bằng máy.",
     "Ta bắt đầu từ đếm số bước, nói gọn bằng các ký hiệu tiệm cận, rồi biến đệ quy thành hệ thức và giải. Sau đó chọn chiến lược thiết kế, và luôn kết thúc bằng một chứng minh hoặc một phép kiểm.")
edit(p, "ta đi theo dòng thời gian của một thuật toán sắp xếp thật. Hành trình đi từ năm 2002 tới khi", "ta đi theo một thuật toán sắp xếp thật. Hành trình đi từ năm 2002 tới khi")
edit(p, '        focus: [1, "2.2", "2.3"]\n        say: "Câu hai, phần lá là n, lớn hơn f bằng 1 một lũy thừa', '        focus: [1, 3, 1, "2.2", "2.3"]\n        say: "Câu hai, phần lá là n, lớn hơn f bằng 1 một lũy thừa')
# L29
p = P("L29")
edit(p, "Tổng kết lại hành trình. Năm 2002,", "Năm 2002,")
edit(p, "đều không thấy suốt nhiều năm, và kiểm thử rộng rãi cũng bỏ sót.", "đều không thấy suốt nhiều năm, kiểm thử cũng bỏ sót.")
for lid in sorted(TPL):
    regen(lid)
