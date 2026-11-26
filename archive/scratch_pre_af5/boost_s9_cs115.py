from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if new in txt and old not in txt:
        return
    assert old in txt, f"Missing in {rel}: {old[:120]!r}"
    assert txt.count(old) == 1, f"Non-unique in {rel}: {old[:120]!r}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


# 1. Quantitative hook upgrades (L27..L39) matching existing visual focus blocks
rep(
    "lessons/cs115/L27_knn.yaml",
    """    focus:
    - 1
    - 1
    - 2
    say: Chào bạn, phương pháp hôm nay tóm gọn trong câu ngưu tầm ngưu, mã tầm mã. Muốn biết một điểm mới thuộc lớp nào, hãy nhìn các điểm gần nó nhất. Không cần học trọng số, không cần hàm sai số, chỉ cần lưu dữ liệu và một cách đo khoảng cách.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    say: Chào bạn, phương pháp hôm nay tóm gọn trong câu ngưu tầm ngưu, mã tầm mã. Muốn biết một điểm mới thuộc lớp nào, hãy nhìn các điểm gần nó nhất. Không cần học trọng số, không cần hàm sai số, chỉ cần lưu dữ liệu và một cách đo khoảng cách. Nếu có mười nghìn mẫu đã dán nhãn, lúc học không tốn phép tính nào, nhưng mỗi lần hỏi phải đo đủ mười nghìn khoảng cách. Hôm nay bạn sẽ thấy chỉ đổi thước đo hay đơn vị đo cũng làm kết quả bầu chọn đổi hẳn.""",
)

rep(
    "lessons/cs115/L28_cay_quyet_dinh.yaml",
    """    focus:
    - 1
    - 2
    - 3
    say: Chào bạn, hãy lọc thư rác bằng những câu hỏi có hoặc không, như thư có chữ khuyến mãi không, có đường dẫn lạ không. Cách làm này giống trò chơi 20 câu hỏi. Câu hỏi tốt là câu chia dữ liệu thành các nhóm thuần nhất, đo bằng entropy hoặc chỉ số Gini.""",
    """    focus:
    - 1
    - 2
    - 3
    - 3
    say: Chào bạn, hãy lọc thư rác bằng những câu hỏi có hoặc không, như thư có chữ khuyến mãi không, có đường dẫn lạ không. Cách làm này giống trò chơi 20 câu hỏi, và với tám nghìn thư mẫu, ta chỉ cần vài tầng hỏi đúng trọng tâm. Câu hỏi tốt là câu chia dữ liệu thành các nhóm thuần nhất, đo bằng entropy từ không chấm sáu chín về không hoặc chỉ số Gini. Nếu trồng thêm hai mươi lăm cây độc lập thành rừng, tỉ lệ đoán đúng tăng vọt mà không cần chuẩn hoá thang đo.""",
)

rep(
    "lessons/cs115/L30_gmm_em.yaml",
    """    focus:
    - 1
    - 1
    - 2
    say: Chào bạn, K trung bình ở bài 29 bắt mỗi điểm thuộc đúng một cụm. Nhưng một điểm nằm giữa hai cụm thì sao? Mô hình hỗn hợp nhiều phân phối chuẩn cho mỗi điểm thuộc mỗi cụm với một xác suất, và học bằng thuật toán kỳ vọng, cực đại hoá.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    say: Chào bạn, K trung bình ở bài 29 bắt mỗi điểm thuộc đúng một cụm. Nhưng một điểm nằm giữa hai cụm thì sao? Mô hình hỗn hợp nhiều phân phối chuẩn gán xác suất mềm, chẳng hạn sáu mươi lăm phần trăm về cụm một và ba mươi lăm phần trăm về cụm hai. Chỉ sau bốn đến năm vòng kỳ vọng rồi cực đại hoá trên sáu nghìn điểm, các tâm cụm đã tự khớp mượt theo hình elip.""",
)

rep(
    "lessons/cs115/L31_nmf.yaml",
    """    focus:
    - 1
    - 2
    - 3
    say: Chào bạn, một ảnh khuôn mặt có thể ghép từ các phần như mắt, mũi, miệng, chỉ cộng lại, không trừ. Phân rã giá trị kỳ dị của bài 16 cho các thành phần có cả số âm, khó hiểu. Phân rã ma trận không âm buộc mọi số không âm, nên chỉ cộng các phần.""",
    """    focus:
    - 1
    - 2
    - 3
    - 3
    say: Chào bạn, một ảnh khuôn mặt có thể ghép từ các phần như mắt, mũi, miệng, chỉ cộng lại, không trừ. Phân rã giá trị kỳ dị của bài 16 cho các thành phần có cả số âm, khó hiểu. Phân rã ma trận không âm buộc mọi số không âm, nên chỉ cộng các phần. Chẳng hạn bốn nghìn điểm ảnh ghép từ sáu mươi bốn mảnh dương sẽ cho ra từng nét mặt rành mạch hơn hẳn bảng hệ số lẫn dấu âm dương.""",
)

rep(
    "lessons/cs115/L33_tong_on.yaml",
    """    focus:
    - 1
    - 2
    - 0
    say: Chào bạn, từ bài 18 đến bài 32 ta đã gặp hơn mười thuật toán. Có ba câu hỏi vàng giúp hiểu và giảng lại bất kỳ mô hình nào, đó là biểu diễn, mất mát và tối ưu. Bài tổng ôn này dùng ba câu hỏi đó để nhìn lại các bài đã học.""",
    """    focus:
    - 1
    - 2
    - 0
    - 0
    say: Chào bạn, từ bài 18 đến bài 32 ta đã gặp mười lăm mô hình từ năm trăm tới một trăm nghìn mẫu. Có ba câu hỏi vàng giúp hiểu và giảng lại bất kỳ mô hình nào, đó là biểu diễn, mất mát và tối ưu. Khi bạn nắm vững khung ba câu hỏi này, việc chọn mô hình cho bảng dữ liệu nhỏ hay lớn trở thành quy trình rõ ràng thay vì đoán mò. Bài tổng ôn hôm nay nối toàn bộ toán nền từ đại số, giải tích tới xác suất thành một bức tranh thống nhất.""",
)

rep(
    "lessons/cs115/L35_rnn_lstm.yaml",
    """    focus:
    - 1
    - 2
    say: Chào bạn, trong câu tôi sinh ra ở Huế nên tôi nói giọng gì, từ cần đoán phụ thuộc vào một từ ở rất xa phía trước. Mạng hồi tiếp đọc từng từ một, giữ một trạng thái như bộ nhớ, và cập nhật nó ở mỗi bước bằng cùng một bộ trọng số.""",
    """    focus:
    - 1
    - 2
    - 2
    say: Chào bạn, trong câu tôi sinh ra ở Huế nên tôi nói giọng gì, từ cần đoán phụ thuộc vào một từ cách hai mươi bước phía trước. Mạng hồi tiếp đọc từng từ một, giữ một trạng thái như bộ nhớ, và cập nhật nó ở mỗi bước bằng cùng một bộ trọng số. Khi nhân liên tiếp hai mươi lần, hệ số không phẩy tám tụt xuống không phẩy không một còn một phẩy hai vọt lên ba mươi tám lần, khiến trí nhớ dễ tắt hoặc nổ.""",
)

rep(
    "lessons/cs115/L36_boosting.yaml",
    """    focus:
    - 1
    - 1
    - 2
    say: Chào bạn, rừng ngẫu nhiên ở bài 28 trồng nhiều cây độc lập rồi bầu chọn. Phương pháp tăng cường thì khác, các mô hình yếu học nối tiếp nhau, mô hình sau tập trung vào chỗ mô hình trước làm sai. Hôm nay ta học hai cách, AdaBoost và tăng cường theo gradient.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    say: Chào bạn, rừng ngẫu nhiên ở bài 28 trồng nhiều cây độc lập rồi bầu chọn. Phương pháp tăng cường thì khác, các mô hình yếu học nối tiếp nhau, mô hình sau tập trung vào chỗ mô hình trước làm sai. Hôm nay ta học hai cách, AdaBoost và tăng cường theo gradient. Với một trăm cây nông học nối tiếp từ dữ liệu ban đầu, mỗi cây sửa phần sai còn sót giúp giảm lỗi đều đặn trên dữ liệu dạng bảng.""",
)

rep(
    "lessons/cs115/L38_ica.yaml",
    """    focus:
    - 1
    - 1
    - 2
    say: Chào bạn, trong một bữa tiệc, hai người nói cùng lúc và hai máy thu âm đặt ở hai chỗ. Mỗi máy thu âm thu một hỗn hợp của cả hai giọng. Phân tích thành phần độc lập tìm lại từng giọng gốc, chỉ từ hai bản ghi, mà không biết cách trộn.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    say: Chào bạn, trong một bữa tiệc, hai người nói cùng lúc và hai máy thu âm đặt ở hai chỗ. Mỗi máy thu âm thu một hỗn hợp của cả hai giọng. Từ hai kênh dài hai nghìn mẫu trộn lẫn không rõ tỉ lệ, phân tích thành phần độc lập chỉ cần hai bản ghi là khôi phục được tín hiệu nguồn. Mẹo cốt lõi là làm trắng dữ liệu trước rồi xoay sao cho phân phối ít giống hình chuông chuẩn nhất.""",
)

rep(
    "lessons/cs115/L39_hoc_tang_cuong.yaml",
    """    focus:
    - 1
    - 2
    say: Chào bạn, khi học chơi một trò chơi, không ai bảo nước đi nào đúng, ta chỉ biết thắng thì được thưởng, mà phần thưởng đến muộn. Học tăng cường mô tả một tác tử, tức chương trình tự chọn hành động, ở một trạng thái, nhận thưởng, rồi sang trạng thái mới, và học cách làm tổng thưởng về sau lớn nhất.""",
    """    focus:
    - 1
    - 2
    - 2
    say: Chào bạn, khi học chơi một trò chơi, không ai bảo nước đi nào đúng, ta chỉ biết thắng thì được thưởng, mà phần thưởng đến muộn. Học tăng cường mô tả một tác tử, tức chương trình tự chọn hành động, ở một trạng thái, nhận thưởng, rồi sang trạng thái mới, và học cách làm tổng thưởng về sau lớn nhất. Chỉ qua một trăm ván thử thắng thua và cập nhật dần bảng giá trị với hệ số chiết khấu, tác tử tự tìm ra nước đi khôn ngoan nhất.""",
)

# 2. Clean recap0 / in_ai boosts on all 20 tight CS115 lessons (>= 1645w)
# Note: in_ai focus=None ONLY when inspected as None; recap0 focus=None on all 20.
IN_AI_BOOSTS = {
    "lessons/cs115/L22_lan_truyen_nguoc.yaml": (
        "Ở bài 23, mạng nhiều lớp chạy lượt lùi qua từng lớp, mỗi lớp nhân với ma trận chuyển vị của nó. Các thư viện học sâu tự xây đồ thị tính toán và tự chạy lượt lùi. Ở bài mở rộng 35, lượt lùi còn đi ngược theo thời gian.",
        "Ở bài 23, mạng nhiều lớp chạy lượt lùi qua từng lớp, mỗi lớp nhân với ma trận chuyển vị của nó. Các thư viện học sâu tự xây đồ thị tính toán và tự chạy lượt lùi. Ở bài mở rộng 35, lượt lùi còn đi ngược theo thời gian. Toàn bộ công việc tự động tính đạo hàm này gọi là vi phân tự động theo chiều ngược. Nó lưu kết quả trung gian ở lượt tiến làm bản đồ sẵn, để khi có tín hiệu lỗi đổ về chỉ việc nhân đúng một lần qua từng nút. Không có quy tắc chuỗi phân rã qua từng cổng đơn giản như vậy, mô hình ngôn ngữ hàng tỉ tham số ngày nay hoàn toàn không thể huấn luyện nổi trên máy thật.",
    ),
    "lessons/cs115/L26_lda_fisher.yaml": (
        "Phân tích phân biệt tuyến tính được dùng để giảm chiều có giám sát trước khi phân loại, ví dụ trong nhận dạng khuôn mặt. Ở bài 27, ta học một bộ phân loại dựa vào khoảng cách tới các điểm gần nhất, và chiếu trước giúp khoảng cách có ý nghĩa hơn.",
        "Phân tích phân biệt tuyến tính được dùng để giảm chiều có giám sát trước khi phân loại, ví dụ trong nhận dạng khuôn mặt. Ở bài 27, ta học một bộ phân loại dựa vào khoảng cách tới các điểm gần nhất, và chiếu trước giúp khoảng cách có ý nghĩa hơn. Trên tập ảnh chân dung ít mẫu nhưng hàng nghìn chiều điểm ảnh, việc giảm xuống tối đa C trừ 1 trục đặc trưng vừa giảm nhiễu nền vừa giữ trọn sự khác biệt giữa từng người. Nhờ dùng cả nhãn khi tìm trục chiếu, phương pháp này thường cho ranh giới tách lớp sắc nét hơn nhiều so với cách chiếu không nhãn ở bài 16.",
    ),
    "lessons/cs115/L27_knn.yaml": (
        "Ý tưởng láng giềng gần nhất được dùng để tìm sản phẩm, ảnh, văn bản giống nhất. Ở bài 29, phân cụm cũng dựa vào khoảng cách tới các tâm. Ở bài 32, ta vẽ dữ liệu nhiều chiều sao cho láng giềng gần vẫn gần nhau.",
        "Ý tưởng láng giềng gần nhất được dùng để tìm sản phẩm, ảnh, văn bản giống nhất trong các hệ thống tìm kiếm thực tế. Ngày nay nhiều cơ sở dữ liệu véc-tơ lưu hàng triệu bản ghi đã mã hoá thành véc-tơ, rồi tìm nhanh vài láng giềng gần nhất chỉ trong vài mi-li-giây. Phương pháp này không cần huấn luyện lại từ đầu khi thêm mẫu mới vào kho, chỉ cần chèn thêm điểm và nhãn vào tập lưu trữ. Ở bài 29, phân cụm cũng dựa vào khoảng cách tới các tâm thay vì tới từng điểm lẻ. Ở bài 32, ta vẽ dữ liệu nhiều chiều lên mặt phẳng sao cho ai là láng giềng gần vẫn đứng sát nhau trên hình.",
    ),
    "lessons/cs115/L37_autoencoder.yaml": (
        "Mạng tự mã hoá được dùng để nén và khử nhiễu ảnh, và phát hiện bất thường, vì mẫu lạ sẽ khôi phục kém. Ở bài mở rộng 42, một biến thể dùng xác suất để sinh dữ liệu mới từ mã.",
        "Mạng tự mã hoá được dùng để nén và khử nhiễu ảnh, và phát hiện bất thường, vì mẫu lạ sẽ khôi phục kém với sai số cao bất thường. Trong sản xuất công nghiệp, người ta thường chỉ huấn luyện mạng trên ảnh sản phẩm bình thường rồi dùng ngưỡng sai số tái tạo để báo lỗi dây chuyền. Một biến thể khử nhiễu còn cố tình làm mờ hoặc xoá bớt một góc ảnh đầu vào để ép khe hẹp phải học đúng cấu trúc thật thay vì sao chép thô. Ở bài mở rộng 42, biến thể dùng xác suất sẽ biến khe hẹp thành không gian liên tục để sinh dữ liệu hoàn toàn mới từ mã.",
    ),
}

RECAP0_BOOSTS = {
    "lessons/cs115/L22_lan_truyen_nguoc.yaml": (
        "Tổng kết chuỗi logic. Vẽ hàm thành đồ thị gồm các phép tính đơn giản. Lượt tiến tính giá trị. Lượt lùi gửi xuống bằng đổ về nhân cục bộ. Bốn cổng chia đều, tráo đổi, định tuyến và cộng dồn. Kiểm tra lại bằng bước nhỏ.",
        "Tổng kết chuỗi logic. Vẽ hàm thành đồ thị gồm các phép tính đơn giản. Lượt tiến tính giá trị và giữ lại các số trung gian cần thiết. Lượt lùi gửi xuống bằng độ dốc đổ về nhân với đạo hàm cục bộ tại mỗi nút. Ta đã làm chủ bốn cổng chuẩn là cổng cộng chia đều, cổng nhân tráo đổi, cổng cực đại định tuyến đúng nhánh lớn nhất, và cổng rẽ nhánh cộng dồn mọi dòng chảy. Luôn nhớ quy tắc vàng là kích thước đạo hàm theo một biến phải khớp y hệt kích thước chính biến đó. Cuối cùng hãy kiểm tra lại kết quả giải tích bằng sai phân bước nhỏ để phát hiện sớm lỗi dấu hay quên nhân cục bộ trước khi huấn luyện thật.",
    ),
    "lessons/cs115/L24_lagrange_kkt.yaml": (
        "Tổng kết chuỗi logic. Tại điểm tốt nhất, đường mức tiếp xúc ràng buộc, nên hai gradient cùng phương. Gói lại thành hàm Lagrange và cho đạo hàm bằng 0. Với bất đẳng thức, dùng bốn điều kiện KKT, an-pha không âm và điều kiện bù. Với bài toán lồi, chúng là đủ.",
        "Tổng kết chuỗi logic. Tại điểm tốt nhất, đường mức tiếp xúc ràng buộc, nên hai gradient cùng phương và ngược hướng tuỳ dấu. Gói lại thành hàm Lagrange và cho đạo hàm riêng bằng không để đưa bài toán có ràng buộc về hệ phương trình quen thuộc. Với ràng buộc bất đẳng thức, ta mở rộng sang bốn điều kiện KKT gồm dừng, khả thi gốc, nhân tử không âm và điều kiện bù chặt chẽ. Nhờ điều kiện bù, mọi ràng buộc không chạm biên đều tự động có nhân tử bằng không và biến mất khỏi đáp số. Với các bài toán lồi, bộ điều kiện này không chỉ là cần mà còn là điều kiện đủ để khẳng định điểm cực trị toàn cục.",
    ),
    "lessons/cs115/L25_svm.yaml": (
        "Tổng kết chuỗi logic. Lề bằng 2 chia độ dài w, nên lề lớn nhất là w ngắn nhất. Điều kiện KKT cho thấy chỉ các vector hỗ trợ có an-pha dương. Lề mềm dùng hàm mất mát bản lề cộng phạt L2. Hàm nhân hợp lệ khi ma trận Gram nửa xác định dương.",
        "Tổng kết chuỗi logic. Bề rộng dải an toàn bằng hai chia độ dài véc-tơ trọng số, nên muốn mở rộng lề tối đa thì ta thu ngắn chuẩn của véc-tơ đó. Điều kiện KKT và điều kiện bù chứng minh chỉ các điểm sát biên gọi là véc-tơ hỗ trợ mới có trọng số an-pha dương, còn mọi điểm nằm xa hoàn toàn không ảnh hưởng đường biên. Khi dữ liệu không tách thẳng hoàn toàn hoặc dính nhiễu, mô hình lề mềm kết hợp hàm mất mát bản lề với phạt bình phương L2 cho phép đánh đổi độ rộng lề lấy số lần vi phạm nhỏ nhất. Cuối cùng mẹo hàm nhân giúp tính tích vô hướng trong không gian chiều cao mà không cần tính rõ toạ độ mới, miễn là ma trận Gram tương ứng nửa xác định dương.",
    ),
    "lessons/cs115/L26_lda_fisher.yaml": (
        "Tổng kết chuỗi logic. Chiếu dữ liệu lên một hướng. Tỉ số Fisher bằng bình phương khoảng cách hai tâm chia độ trải trong lớp. Hướng tốt nhất tỉ lệ với nghịch đảo của S w nhân hiệu hai tâm. Có tối đa C trừ 1 hướng, và khác phân tích thành phần chính vì có dùng nhãn.",
        "Tổng kết chuỗi logic. Chiếu dữ liệu lên một hướng để vừa tách hai tâm ra xa vừa ép từng lớp gom chặt lại. Tỉ số Fisher đo chính xác sự đánh đổi này bằng bình phương khoảng cách hai tâm chia tổng độ phân tán trong lớp. Hướng chiếu tối ưu được giải đóng ngay từ nghịch đảo ma trận phân tán trong lớp nhân với hiệu hai véc-tơ trung bình. Do hạng của ma trận phân tán giữa các lớp bị chặn bởi số lớp, phương pháp chỉ tìm được tối đa C trừ 1 hướng có nghĩa. Khác với phân tích thành phần chính vốn chạy mù không nhãn, phân tích phân biệt tuyến tính dùng nhãn lớp để giữ đúng các trục giúp phân loại tốt nhất.",
    ),
    "lessons/cs115/L27_knn.yaml": (
        "Tổng kết chuỗi logic. Lưu dữ liệu, đo khoảng cách L một hoặc L hai, để K láng giềng gần nhất bầu chọn. Chọn K và cách đo bằng kiểm định, và nhớ chuẩn hoá thang đo trước.",
        "Tổng kết chuỗi logic. Thuật toán lười không tạo công thức hay ranh giới cố định lúc học mà chỉ cất toàn bộ dữ liệu đã dán nhãn vào bộ nhớ. Khi có điểm mới, nó đo khoảng cách L một hoặc L hai tới từng mẫu, lấy đúng K láng giềng gần nhất rồi cho bầu chọn theo đa số hoặc lấy trung bình. L một đi theo ô vuông góc và hay ít bị một vài trục lớn kéo lệch hơn, còn L hai là đường chim bay quen thuộc dễ bị biến có thang đo lớn nuốt chửng. Hãy luôn chọn K lẻ khi có hai lớp, dùng kiểm định chéo thay vì kiểm trên chính tập lưu để tránh chọn nhầm K bằng một, và chuẩn hoá mọi cột về cùng thang đo trước khi đo bất kỳ khoảng cách nào.",
    ),
    "lessons/cs115/L28_cay_quyet_dinh.yaml": (
        "Tổng kết chuỗi logic. Cây chia dữ liệu bằng các câu hỏi có hoặc không. Đo độ lẫn bằng entropy hoặc chỉ số Gini, chọn câu có độ lợi lớn nhất, giới hạn độ sâu để tránh quá khớp, và gộp nhiều cây khác nhau thành rừng để bầu chọn.",
        "Tổng kết chuỗi logic. Cây quyết định phân vùng không gian bằng chuỗi câu hỏi nhị phân theo từng đặc trưng mà không cần chuẩn hoá đơn vị. Tại mỗi nút, ta đo độ hỗn tạp bằng entropy hoặc chỉ số Gini rồi chọn ngưỡng chia làm độ lợi thông tin đạt cực đại. Nếu để cây mọc sâu không phanh, nó sẽ tách vừa khít từng điểm nhiễu và rơi vào bẫy quá khớp ngay lập tức, nên ta phải cắt tỉa bằng độ sâu tối đa hay số mẫu tối thiểu ở lá. Để giảm phương sai do chọn nhánh tham lam, rừng ngẫu nhiên cho hàng loạt cây học trên mẫu bốc lại có hoàn lại kèm tập con đặc trưng ngẫu nhiên rồi lấy đa số phiếu. Đây là mô hình nền cực mạnh cho dữ liệu dạng bảng thực tế.",
    ),
    "lessons/cs115/L30_gmm_em.yaml": (
        "Tổng kết chuỗi logic. Mật độ hỗn hợp là tổng có trọng số các hình chuông. Bước E tính độ thuộc về bằng định lý Bayes. Bước M cập nhật bằng trung bình có trọng số. Tổng lôgarit khả năng không giảm nhưng chỉ tới cực trị địa phương, và phải chặn phương sai.",
        "Tổng kết chuỗi logic. Mô hình hỗn hợp biểu diễn phân phối phức tạp thành tổng có trọng số của các hình chuông chuẩn, giải quyết hạn chế gán cứng của phân cụm K trung bình. Trong thuật toán lặp EM, bước kỳ vọng E dùng định lý Bayes để gán xác suất thuộc từng cụm cho mọi điểm dữ liệu dựa trên tâm và độ rộng hiện tại. Sau đó bước cực đại hoá M cập nhật lại trọng số trộn, trung bình cụm và phương sai theo trung bình có trọng số của các xác suất vừa tính. Giá trị log hợp lý chắc chắn không giảm sau mỗi vòng, nhưng vì hàm không lồi nên dễ dừng ở cực trị địa phương tuỳ điểm khởi tạo. Luôn nhớ cộng hằng số nhỏ vào đường chéo ma trận hiệp phương sai để cụm không co sụp vào một điểm đơn độc.",
    ),
    "lessons/cs115/L31_nmf.yaml": (
        "Tổng kết chuỗi logic. Dữ liệu không âm xấp xỉ bằng A nhân B với mọi số không âm. Chỉ cộng các phần nên dễ đọc. Quy tắc nhân giữ không âm và sai số không tăng. Kết quả không duy nhất và phụ thuộc khởi tạo.",
        "Tổng kết chuỗi logic. Khi ma trận đầu vào chỉ chứa số không âm như tần suất từ, lượng mua sắm hay cường độ sáng ảnh, ta xấp xỉ nó thành tích A nhân B với mọi phần tử đều lớn hơn hoặc bằng không. Ràng buộc không âm loại bỏ hoàn toàn phép trừ triệt tiêu lẫn nhau, biến mỗi cột thành công thức cộng ghép trực quan từ các bộ phận rời rạc. Thuật toán cập nhật bằng phép nhân bảo toàn dấu không âm tự động qua từng bước và đảm bảo hàm mất mát tái tạo không bao giờ tăng. Hãy lưu ý nghiệm phân rã không duy nhất do luôn có thể nhân hai chiều bởi hai hệ số nghịch đảo nhau, và lời giải có thể dừng ở cực tiểu địa phương tuỳ ma trận khởi tạo ban đầu.",
    ),
    "lessons/cs115/L32_tsne.yaml": (
        "Tổng kết chuỗi logic. Ở không gian gốc, xác suất láng giềng là hình chuông chia cho tổng. Độ bối rối là số láng giềng hiệu dụng. Ở mặt phẳng, dùng phân phối đuôi dày. Dời các điểm bằng gradient descent để giảm độ lệch giữa hai phân phối, và khi đọc hình, chỉ tin láng giềng gần.",
        "Tổng kết chuỗi logic. Để vẽ dữ liệu nhiều chiều lên mặt phẳng hai chiều mà không bị nén chụm ở tâm, phương pháp chuyển khoảng cách ở không gian gốc thành xác suất hàng xóm bằng hàm chuông rồi hiệu chỉnh bề rộng theo độ bối rối. Dưới mặt phẳng đích, ta lại dùng phân phối đuôi dày kiểu t nhằm dành chỗ cho các điểm nằm xa nhau không đè lên nhóm gần. Thuật toán hạ gradient theo độ lệch KL bất đối xứng ưu tiên rất mạnh việc giữ gần những điểm vốn thân cận, trong khi chấp nhận buông lỏng vị trí tương đối giữa các cụm xa. Vì vậy khi đọc bản đồ trực quan, bạn tuyệt đối không đo kích thước cụm hay khoảng cách giữa hai đám mây xa nhau mà kết luận vội.",
    ),
    "lessons/cs115/L33_tong_on.yaml": (
        "Tổng kết cả khoá học. Biểu diễn dữ liệu bằng vector và ma trận. Chọn hàm mất mát từ mô hình xác suất. Tối ưu bằng giải đóng, gradient hoặc thuật toán lặp. Và luôn kiểm định trên dữ liệu chưa thấy.",
        "Tổng kết cả khoá học nền tảng đến đây. Dù gặp thuật toán nào từ hồi quy tuyến tính đến phân cụm, mạng nơ-ron hay SVM, ta luôn mở khoá nó qua đúng ba câu hỏi vàng là biểu diễn, mất mát và tối ưu. Biểu diễn giúp chuyển thực tế thành không gian véc-tơ và ma trận có thể tính đạo hàm hay đo khoảng cách được. Hàm mất mát thường bắt nguồn trực tiếp từ ước lượng hợp lý cực đại của bài 17 kèm thêm thành phần điều chuẩn để kiềm chế quá khớp. Bước tối ưu nối công thức giải đóng, hạ gradient hay vòng lặp E và M tuỳ độ phức tạp bề mặt. Và nguyên tắc tối hậu là mọi quyết định chỉnh mô hình đều phải đứng trước tập kiểm định độc lập chưa từng lộ trong lúc huấn luyện.",
    ),
    "lessons/cs115/L34_cnn.yaml": (
        "Tổng kết chuỗi logic. Tích chập trượt bộ lọc trên ảnh, nhân từng ô với nhau, rồi cộng tất cả lại. Kích thước đầu ra theo công thức đệm và bước nhảy. Dùng chung bộ lọc nên rất ít tham số. Nó là phép tuyến tính, nhân với ma trận thưa. Lớp gộp thu nhỏ ảnh và không có tham số.",
        "Tổng kết chuỗi logic. Mạng tích chập khai thác cấu trúc không gian của ảnh bằng cách trượt cùng một bộ lọc nhỏ qua mọi toạ độ, nhân từng ô rồi cộng tổng. Nhờ kết nối cục bộ và dùng chung trọng số, số tham số giảm từ hàng chục triệu xuống chỉ còn vài trăm mà vẫn bắt được đặc trưng bất biến theo vị trí dịch chuyển. Kích thước bản đồ đầu ra quyết định chuẩn xác bởi cạnh ảnh, cỡ bộ lọc, phần đệm biên và bước nhảy trượt. Về bản chất đại số, phép tích chập vẫn là phép nhân với một ma trận thưa dạng Toeplitz rất có cấu trúc, ghép xen kẽ lớp gộp cực đại hay gộp trung bình không chứa tham số để nén dần chiều rộng và mở rộng vùng nhìn.",
    ),
    "lessons/cs115/L35_rnn_lstm.yaml": (
        "Tổng kết chuỗi logic. Mạng hồi tiếp mang theo trạng thái, dùng cùng trọng số ở mọi bước. Ta duỗi mạng ra theo thời gian để làm lan truyền ngược. Tích nhiều ma trận gây triệt tiêu hoặc bùng nổ. Giảm nhẹ bằng cắt gradient và ô nhớ có cổng.",
        "Tổng kết chuỗi logic. Mạng hồi tiếp xử lý chuỗi độ dài bất kỳ bằng cách duy trì một véc-tơ trạng thái ẩn làm bộ nhớ và dùng đi dùng lại đúng một bộ trọng số tại mọi bước thời gian. Khi huấn luyện, ta duỗi mạng dọc theo chiều dài chuỗi để chạy lan truyền ngược qua thời gian rồi cộng dồn gradient về chung một ma trận. Cũng chính vì nhân lặp cùng một ma trận qua k bước, độ lớn gradient tăng vọt hoặc tắt lịm theo cấp số nhân, dễ gây nổ số hoặc mất hẳn khả năng nhớ từ xa. Cắt chuẩn gradient chận được tình trạng bùng nổ tức thời, còn kiến trúc ô nhớ có cổng bổ sung đường cộng song song được điều tiết bằng cổng quên và cổng vào để giữ tín hiệu qua nhiều trăm bước.",
    ),
    "lessons/cs115/L36_boosting.yaml": (
        "Tổng kết chuỗi logic. Tăng cường ghép nối tiếp nhiều mô hình yếu lại với nhau. AdaBoost tính trọng số mô hình từ sai số và tăng trọng số các mẫu bị sai. Tăng cường theo gradient khớp mỗi cây mới vào phần dư. Và dừng theo tập kiểm định.",
        "Tổng kết chuỗi logic. Trái với rừng ngẫu nhiên trồng nhiều cây song song nhằm giảm dao động phương sai, nhóm thuật toán tăng cường ghép nhiều cây nông nối tiếp nhau nhằm giảm dần thiên lệch còn sót. Với AdaBoost, mô hình có sai số thấp được cấp trọng số biểu quyết cao hơn, đồng thời hệ thống tăng cân nặng cho các mẫu vừa bị đoán nhầm để mô hình kế tiếp tập trung sửa đúng chỗ đó. Tăng cường theo gradient nhìn vấn đề tổng quát hơn bằng cách coi mỗi cây mới như một bước hạ gradient trong không gian hàm số, trực tiếp khớp phần dư sai lệch mà tổng các cây trước còn để lại. Luôn hạ tốc độ học kết hợp dừng sớm dựa trên tập kiểm định chéo để cây nối tiếp không học thuộc luôn nhiễu.",
    ),
    "lessons/cs115/L37_autoencoder.yaml": (
        "Tổng kết chuỗi logic. Mạng tự mã hoá đi qua mã hoá, cổ chai và giải mã, học bằng sai số tái tạo mà không cần nhãn. Bản tuyến tính chỉ bằng phân tích thành phần chính, còn bản phi tuyến nén được dữ liệu nằm trên đường cong.",
        "Tổng kết chuỗi logic. Mạng tự mã hoá giải bài toán học biểu diễn không nhãn bằng cách ép dữ liệu gốc phải đi qua một cổ chai ít chiều ở giữa rồi cố gắng khôi phục nguyên bản ở đầu ra. Khi cổ chai đủ hẹp, mạng buộc phải gạt bỏ nhiễu vụn và chắt lọc những đặc trưng mang nhiều thông tin nhất để tối thiểu hoá sai số tái tạo bình phương. Nếu bỏ toàn bộ hàm kích hoạt phi tuyến và dùng bình phương sai số, không gian con học được trùng khớp đúng không gian trải bởi các thành phần chính của bài 16. Thêm hàm kích hoạt phi tuyến như ReLU hay GELU mở ra khả năng uốn lượn để trải phẳng những dữ liệu nằm trên đa tạp cong mà phép chiếu thẳng truyền thống đành chịu thua.",
    ),
    "lessons/cs115/L38_ica.yaml": (
        "Tổng kết chuỗi logic. Tín hiệu đo là hỗn hợp tuyến tính của các nguồn độc lập. Làm trắng bằng phân tích thành phần chính, rồi xoay để các thành phần ít chuẩn nhất. Cần nguồn không chuẩn, và không biết được thứ tự, tỉ lệ, dấu.",
        "Tổng kết chuỗi logic. Phân tích thành phần độc lập tách các nguồn phát gốc từ những tín hiệu thu trộn lẫn hoàn toàn mù thông tin ma trận trộn. Vì bản chất trộn nhiều biến làm tín hiệu tổng ngày càng tiến sát phân phối chuẩn theo định lý giới hạn trung tâm, ta đảo ngược quá trình bằng cách tìm phép xoay sau bước làm trắng để các thành phần đầu ra có độ bất chuẩn lớn nhất đo bằng độ nhọn dư hay entropy. Nhớ phân biệt rõ hai khái niệm nền là không tương quan mới triệt tiêu hiệp phương sai bậc hai, còn độc lập thống kê mạnh hơn nhiều và luôn khớp trục nhờ tính phi chuẩn. Thuật toán chỉ khôi phục được hình dạng sóng gốc, không thể tự biết trước thứ tự kênh, hệ số phóng đại hay dấu âm dương của từng nguồn.",
    ),
    "lessons/cs115/L39_hoc_tang_cuong.yaml": (
        "Tổng kết chuỗi logic. Tác tử có trạng thái, hành động và phần thưởng. Mục tiêu của tác tử là làm cho tổng phần thưởng đã chiết khấu lớn nhất. Giá trị thoả phương trình tự nhất quán. Học bằng cập nhật trung bình trượt về đích, và phải thăm dò.",
        "Tổng kết chuỗi logic. Trong bài toán học tăng cường, tác tử không được cho sẵn nhãn đúng từng bước mà tương tác liên tục với môi trường qua trạng thái, hành động và phần thưởng tức thời. Mục tiêu là chọn chính sách hành động làm cực đại tổng phần thưởng tương lai có nhân hệ số chiết khấu nhỏ hơn một để đảm bảo hội tụ và ưu tiên lợi ích gần. Phương trình Bellman tạo cầu nối tự nhất quán giữa giá trị hiện tại với phần thưởng ngay cộng giá trị tối ưu tại trạng thái kế tiếp. Thuật toán Q-learning học không cần mô hình môi trường bằng cách nhích nhẹ bảng ước lượng về phía mục tiêu tạm thời, đồng thời luôn giữ tỉ lệ thăm dò hợp lý thay vì chỉ khai thác tham lam quá sớm.",
    ),
    "lessons/cs115/L40_umap.yaml": (
        "Tổng kết chuỗi logic. Đầu tiên dựng đồ thị nối mỗi điểm với các láng giềng gần nhất, gán trọng số cho từng cạnh, rồi gộp hai chiều theo kiểu hoặc. Tìm toạ độ bằng entropy chéo nhị phân, vừa kéo vừa đẩy. Và nhớ các nhận định so sánh là thực nghiệm, không phải định lý.",
        "Tổng kết chuỗi logic. Để vẽ dữ liệu hàng trăm nghìn hay hàng triệu điểm lên mặt phẳng mà không mất thời gian tính toàn bộ mọi cặp khoảng cách, thuật toán mở đầu bằng đồ thị k láng giềng gần nhất có chuẩn hoá khoảng cách theo từng vùng mật độ cục bộ. Hai trọng số có hướng trên mỗi cạnh được hợp nhất bằng phép hội xác suất mềm đối xứng để đảm bảo cả hai phía đều công nhận quan hệ hàng xóm. Ở chiều thấp, hàm entropy chéo nhị phân kết hợp lấy mẫu ngẫu nhiên cặp xa tạo ra hai lực kéo điểm cùng cạnh lại gần và đẩy cụm rời ra xa một cách tiết kiệm. Cuối cùng hãy luôn giữ thái độ khoa học khi đọc biểu đồ thực nghiệm, kiểm tra độ ổn định qua nhiều hạt giống ngẫu nhiên và hiểu rõ tốc độ vượt trội quan sát được không tự động thành bất biến toán học cho khoảng cách giữa các cụm xa.",
    ),
    "lessons/cs115/L41_attention.yaml": (
        "Tổng kết chuỗi logic. Truy vấn nhân khoá cho điểm số, chia căn d để phương sai về 1, chuẩn hoá mũ theo hàng thành trọng số, rồi lấy trung bình có trọng số của giá trị. Nhớ thêm mã hoá vị trí, và chi phí tăng theo bình phương độ dài.",
        "Tổng kết chuỗi logic. Cơ chế tự chú ý loại bỏ nút thắt đọc tuần tự của mạng hồi tiếp bằng cách cho mọi token trong chuỗi nhìn trực tiếp lẫn nhau qua chỉ một bước ma trận. Mỗi vị trí phát ra ba véc-tơ gồm truy vấn, khoá và giá trị để tính độ tương đồng bằng tích vô hướng rồi chia căn bậc hai số chiều khoá nhằm giữ phương sai ổn định bằng một trước khi chuẩn hoá mũ. Trọng số thu được dùng để pha trộn có chọn lọc thông tin từ các giá trị phù hợp nhất tạo ra biểu diễn ngữ cảnh mới cực kỳ sắc nét. Đừng quên hai mảnh ghép bắt buộc đi kèm là mã hoá vị trí vì bản chất phép chú ý đối xứng thứ tự, và chi phí bộ nhớ tăng bậc hai theo độ dài chuỗi khiến chuỗi siêu dài cần cửa sổ thưa hoặc bộ nhớ đệm khoá giá trị.",
    ),
    "lessons/cs115/L42_vae_gan.yaml": (
        "Tổng kết chuỗi logic. Mạng tự mã hoá biến phân làm lớn cận dưới, gồm giải mã tốt trừ độ lệch giữa hai phân phối. Nó dùng mẹo tham số hoá lại, và sinh ảnh bằng cách rút mã từ phân phối chuẩn tắc. Mạng đối kháng là trò chơi hai bên, với bộ phân biệt tốt nhất có công thức gọn.",
        "Tổng kết chuỗi logic. Muốn chuyển từ nén dữ liệu sang sinh mẫu hoàn toàn mới, mạng tự mã hoá biến phân biến mã ẩn thành một phân phối chuẩn có trung bình và độ lệch chuẩn riêng rồi tối đa hoá cận dưới biến phân gồm độ chính xác tái tạo trừ độ lệch KL giữ không gian ẩn gần phân phối chuẩn tắc. Mẹo tham số hoá lại tách phần ngẫu nhiên ra ngoài thành nhiễu chuẩn độc lập giúp gradient đi thẳng xuyên qua nút lấy mẫu để cập nhật mạng mã hoá bình thường. Sang nửa kia, mạng đối kháng đặt hai mạng sinh và phân biệt vào một trò chơi tổng bằng không mà cân bằng Nash đạt tại xác suất phân biệt một phần hai cho cả dữ liệu thật lẫn dữ liệu giả. Nhờ hai triết lý bù trừ nhau đó, một bên vững xác suất dễ hội tụ còn một bên sinh ảnh sắc nét nhờ hàm mục tiêu cạnh tranh.",
    ),
    "lessons/cs115/L43_diffusion.yaml": (
        "Tổng kết chuỗi logic. Thêm nhiễu từng bước mà giữ phương sai bằng 1. Gộp lại để nhảy thẳng tới bước bất kỳ. Mạng học đoán nhiễu bằng sai số bình phương. Khi sinh, đi từ nhiễu và khử dần qua nhiều bước.",
        "Tổng kết chuỗi logic. Mô hình khuếch tán giải bài toán sinh ảnh chất lượng cao bằng hai chiều thuận và nghịch đều đặn qua hàng trăm bước nhỏ. Ở chiều thuận, ta trộn dần nhiễu chuẩn theo một lịch phương sai sao cho tổng bình phương hai hệ số luôn bằng một để phân phối cuối tiến hẳn về nhiễu chuẩn tắc thuần khiết. Điểm kỳ diệu về giải tích của phân phối chuẩn là cho phép gộp toàn bộ T bước thành một công thức đóng tính thẳng mẫu nhiễu ở bước t bất kỳ chỉ từ ảnh gốc và một véc-tơ nhiễu đơn. Lúc huấn luyện mạng chỉ cần dự đoán đúng lượng nhiễu đã pha theo sai số bình phương trung bình rồi tới lúc sinh ảnh mới lặp ngược từng bước bóc nhiễu dần cho tới khi đường nét ảnh sắc sảo hiện hình trở lại.",
    ),
}

for rel, (old, new) in IN_AI_BOOSTS.items():
    rep(rel, old, new)
for rel, (old, new) in RECAP0_BOOSTS.items():
    rep(rel, old, new)

# Programmatic verification across all 47 CS115 lessons
errs = warns = 0
for p in sorted((ROOT / "lessons" / "cs115").glob("L*.yaml")):
    sp = lv.load_spec(p)
    lid = sp["id"]
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    errs += len(res.errors)
    warns += len(res.warnings)
    # Check sentence lengths, banned tokens, and focus alignment for L22..L43
    if 22 <= int(lid[1:]) <= 43:
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                say = st.get("say") or ""
                foc = st.get("focus")
                sents = lv.sentences(say)
                if foc is not None:
                    assert len(foc) == len(sents), f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}"
                for s in sents:
                    assert len(s) <= 170, f"{lid}:{sc['id']}#{idx} sent >170 chars ({len(s)}): {s}"
                    assert len(s.split()) <= 38, f"{lid}:{sc['id']}#{idx} sent >38 words ({len(s.split())}): {s}"
                    assert "càng " not in s.lower(), f"{lid}:{sc['id']}#{idx} 'càng ': {s}"
                    assert not re.search(r"[$_^]", s), f"{lid}:{sc['id']}#{idx} TeX char in say: {s}"
        assert w >= 1645, f"CS115:{lid} words={w} < 1645"
        print(f"OK CS115:{lid} words={w} PASS", flush=True)
print(f"CS115 BOOST ALL 47 LESSONS LINT: FAIL={errs}, WARN={warns}", flush=True)
assert errs == 0 and warns == 0
