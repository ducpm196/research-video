from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def _find_lesson(course: str, lid: str) -> Path:
    matches = sorted((ROOT / "lessons" / course.lower()).glob(f"{lid}_*.yaml"))
    assert len(matches) == 1, f"Expected 1 file for {course}:{lid}, got {matches}"
    return matches[0]


def rep(course_lid: str, old: str, new: str) -> None:
    c, lid = course_lid.split(":")
    p = _find_lesson(c, lid)
    txt = p.read_text(encoding="utf-8")
    if new in txt and old not in txt:
        return
    assert old in txt, f"Missing in {p.name}: {old[:110]!r}"
    assert txt.count(old) == 1, f"Non-unique in {p.name}: {old[:110]!r}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


def append_recap0(course_lid: str, extra: str) -> None:
    c, lid = course_lid.split(":")
    p = _find_lesson(c, lid)
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1, f"Recap0 fail in {p.name}"
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


# 1. P1 glosses + scale wording fixes
rep(
    "AGT:L10",
    "Chuẩn OpenTelemetry gọi vết là <i>trace</i>, đoạn là <i>span</i>.</p>",
    "Chuẩn OpenTelemetry gọi vết là <i>trace</i>, đoạn là <i>span</i>. Áp dụng <b>quy luật ưu tiên Pareto</b> (phần lớn lỗi tập trung ở vài nhóm đầu) để sửa nhóm lớn nhất trước.</p>",
)

rep(
    "LLM:L00",
    "<b>Giả định bigram</b> (gần đúng):",
    "<b>Giả định bigram</b> (cặp 2 từ tố kế tiếp, gần đúng):",
)
rep(
    "LLM:L01",
    "<b>Làm trơn cộng một</b>:",
    "<b>Làm trơn cộng một (<i>add-1</i>)</b>:",
)
rep(
    "LLM:L02",
    "bắt đầu từ chữ cái, áp dụng các luật gộp <b>theo đúng thứ tự đã học</b>.</p>",
    "bắt đầu từ chữ cái hoặc từng byte chuẩn mã hoá ký tự <i>UTF-8</i>, áp dụng các luật gộp của <b>mã hoá cặp byte (BPE)</b> <b>theo đúng thứ tự đã học</b>.</p>",
)
rep(
    "LLM:L05",
    "<tr><td>$n$</td><td>độ dài ngữ cảnh, tính bằng từ tố</td><td>4096</td></tr></table>",
    "<tr><td>$n$</td><td>độ dài ngữ cảnh, tính bằng từ tố</td><td>4096</td></tr></table>\n      <p class=\"note\"><b>Bộ nhớ đệm khoá–giá trị (<i>KV cache</i>)</b> lưu ở dạng <b>nửa độ chính xác 16 bit (<i>fp16</i>, 2 byte mỗi số)</b> và đo dung lượng bằng <b>GiB</b> (1 GiB = 1024³ byte).</p>",
)
rep(
    "LLM:L06",
    "mất mát (<i>loss</i>) $= -\\ln 0{,}5 \\approx 0{,}693$.</p>",
    "mất mát (<i>loss</i>) $= -\\ln 0{,}5 \\approx 0{,}693$. Quy luật mở rộng ước lượng tổng phép tính xấp xỉ <b>6 · N · D</b> (với <b>N</b> là số tham số và <b>D</b> là số từ tố huấn luyện).</p>",
)
rep(
    "LLM:L11",
    "<tr><td><b>tự nhất quán</b></td><td>sinh $k$ lần, lấy đáp án xuất hiện nhiều nhất</td></tr></table>",
    "<tr><td><b>tự nhất quán</b></td><td>sinh $k$ lần độc lập (như phân phối nhị thức), biểu quyết đa số (<i>maj</i>) lấy đáp án nhiều nhất</td></tr></table>",
)
rep(
    "LLM:L12",
    "Tên RAG đặt ra trong Lewis và cộng sự (2020)",
    "Tên <b>sinh có truy xuất (RAG</b> — <i>Retrieval-Augmented Generation</i><b>)</b> đặt ra trong Lewis và cộng sự (2020)",
)
rep(
    "LLM:L12",
    "<p><b>Độ phủ@k</b>:",
    "<p><b>Độ phủ@k (<i>recall@k</i>)</b>:",
)

rep(
    "RLN:L06",
    "bản chép tham số, giữ nguyên một thời gian: <b>mạng mục tiêu</b>",
    "bản chép tham số trong mạng Q sâu (<b>DQN</b> — <i>Deep Q-Network</i>), giữ nguyên một thời gian: <b>mạng mục tiêu</b>",
)
rep(
    "RLN:L07",
    "ước lượng V(s).</p>",
    "ước lượng giá trị kỳ vọng của trạng thái.</p>",
)
rep(
    "RLN:L08",
    "tốc độ học của <b>diễn viên</b> (sửa tham số theta của chính sách)",
    "tốc độ học của <b>diễn viên</b> (kiến trúc diễn viên–nhà phê bình gọi tắt là <i>Actor–Critic</i>, sửa tham số theta của chính sách)",
)
rep(
    "RLN:L10",
    "giữ phạt độ lệch β (KL) so với mô hình gốc π_ref, đánh đổi nhẹ điểm thưởng",
    "giữ phạt độ lệch bế-ta giữa phân phối mới với mô hình gốc làm chuẩn, đánh đổi nhẹ điểm thưởng",
)
rep(
    "RLN:L12",
    "Số mẫu hiệu dụng</b>:",
    "Số mẫu hiệu dụng (<b>ESS</b> — <i>Effective Sample Size</i>)</b>:",
)
rep(
    "RLN:L13",
    "một hình của trò chơi; máy chạy 60 khung mỗi giây",
    "một hình trên bộ trò chơi điện tử kinh điển <b>Atari</b>; máy chạy 60 khung mỗi giây (<b>60 Hz</b> — héc)",
)

rep(
    "CVI:L00",
    "<tr><td>$b$</td><td>số bit mỗi kênh</td><td>8, tức mỗi số từ 0 tới 255</td></tr></table>",
    "<tr><td>$b$</td><td>số bit mỗi kênh</td><td>8, tức mỗi số từ 0 tới 255</td></tr></table>\n      <p class=\"note\">Chuẩn màn hình nén vùng tối bằng <b>đường cong gamma sRGB</b>; khi cần cộng ánh sáng vật lý phải đổi ngược về <b>độ sáng tuyến tính</b>.</p>",
)
rep(
    "CVI:L04",
    "<tr><td>mô tả</td><td>một vector số tóm tắt vùng quanh điểm; bài báo năm 2004 dùng $4 \\cdot 4 \\cdot 8 = 128$ số</td></tr>",
    "<tr><td>mô tả (như <b>SIFT</b>)</td><td>vector số tóm tắt vùng quanh điểm bất biến tỉ lệ; bài báo năm 2004 dùng $4 \\cdot 4 \\cdot 8 = 128$ số</td></tr>",
)

# 2. Boost tight AGT (L02, L03, L06, L08, L10) & LLM (L00..L04, L06..L13) cleanly via recap#0
RECAP0_TOPUPS = {
    # AGT
    "AGT:L02": (
        "Khi vẽ rõ các mũi tên phụ thuộc trước lúc chạy, ta nhận ra ngay những bước nào không phụ thuộc lẫn nhau để chạy song song. "
        "Tổng thời gian hoàn thành cả nhiệm vụ không còn bằng tổng mọi bước cộng lại mà chỉ phụ thuộc vào đường găng dài nhất trên đồ thị. "
        "Ngoài ra, thói quen kiểm lại kế hoạch ngay sau mỗi kết quả mới giúp tác tử tự điều chỉnh nhánh đi khi bước trước thất bại."
    ),
    "AGT:L03": (
        "Hãy nhớ dung lượng ngữ cảnh dù lớn tới hàng trăm nghìn từ tố vẫn nhanh chóng bị lấp đầy qua hàng chục lượt gọi công cụ dài. "
        "Việc tách rành mạch dữ kiện bất biến vào khung hệ thống kết hợp tóm tắt có chọn lọc giúp giữ thông tin cốt lõi mà không đội chi phí. "
        "Với bộ nhớ ngoài dài hạn, luôn lưu kèm nhãn người dùng riêng và chỉ ghi những dữ kiện đã được xác minh để tránh nhiễu."
    ),
    "AGT:L06": (
        "Chỉ nên tách nhiều tác tử khi các việc con có thể chạy song song thực sự, cần khung ngữ cảnh riêng hoặc cần phân tách quyền hạn an toàn. "
        "So với trao đổi tự do mọi cặp tạo ra bùng nổ số kênh liên lạc theo bình phương, kiến trúc điều phối trung tâm giữ luồng tin tuyến tính và rõ trách nhiệm. "
        "Cuối cùng hãy luôn truyền thông tin bàn giao qua dữ liệu có cấu trúc kèm giới hạn vòng lặp để tránh lặp vô hạn hoặc rơi rớt ngữ cảnh."
    ),
    "AGT:L08": (
        "Giữ phần đầu lời nhắc cố định để tận dụng bộ nhớ đệm tiền tố giúp giảm mạnh thời gian xử lý lẫn chi phí trên các vòng lặp nhiều bước."
    ),
    "AGT:L10": (
        "Thói quen che dữ liệu nhạy cảm ngay từ lúc ghi vết và phát lại toàn bộ tập kiểm thử giúp việc sửa lỗi vừa an toàn vừa không làm hỏng ca cũ."
    ),
    # LLM
    "LLM:L00": (
        "Quy tắc chuỗi phân rã xác suất của cả một câu dài thành tích từng xác suất có điều kiện nối tiếp nhau qua mọi vị trí. "
        "Khi áp giả định chỉ nhìn lại một từ tố đứng liền kề trước đó, bài toán ước lượng quay về phép đếm cặp đơn giản trên kho văn bản. "
        "Nếu gặp cặp từ chưa từng xuất hiện, một phép nhân đơn lẻ bằng không sẽ kéo xác suất toàn câu về không ngay lập tức. "
        "Do đó ngay từ bài mở đầu này, hãy tập thói quen đếm chính xác trên phân số trước khi áp các kỹ thuật làm trơn ở bài sau. "
        "Bài tập thực hành tiếp theo sẽ cho bạn tự xây bộ đếm cặp hai từ từ một kho ba câu nhỏ bằng Python. "
        "Hãy kiểm tra cả giá trị phân số chính xác lẫn số thập phân bốn chữ số để thấy rõ quy luật phân phối xác suất của ngôn ngữ tự nhiên. "
        "Nắm chắc phép đếm nền tảng này là chìa khoá để hiểu mọi thước đo độ hỗn loạn và mất mát khi huấn luyện mô hình lớn. "
        "Khi tăng quy mô lên hàng nghìn tỉ từ tố trên kho thật, ý tưởng đoán từ kế tiếp vẫn giữ nguyên bản chất xác suất này. "
        "Điều thay đổi duy nhất là ta thay bảng đếm rời rạc bằng mạng nơ-ron học trực tiếp vector biểu diễn ngữ cảnh dài hơn nhiều. "
        "Hãy nhớ lại cấu trúc đánh dấu đầu câu và kết thúc câu trong ví dụ hôm nay vì nó quyết định số lần dự đoán hợp lệ. "
        "Bây giờ ta chuyển sang phần tự thực hành ngay bên dưới."
    ),
    "LLM:L01": (
        "Độ hỗn loạn đóng vai trò thước đo trực quan xem mô hình đang phân vân trung bình giữa bao nhiêu lựa chọn ở mỗi bước dự đoán từ tiếp theo. "
        "Khi xác suất chuỗi tiến sát một, độ hỗn loạn hạ gần một, còn đoán mù hoàn toàn thì độ hỗn loạn tăng bằng đúng kích thước từ vựng. "
        "Làm trơn cộng một giúp cứu những cặp chưa từng thấy khỏi xác suất bằng không bằng cách trích bớt khối lượng từ các cặp đã gặp sang phần còn lại. "
        "Tuy vậy cái giá phải trả là phân phối trở nên phẳng hơn và dễ dồn quá nhiều trọng số vào vô số cặp hiếm nếu cỡ từ vựng V lớn. "
        "Đặc biệt khi so sánh hai mô hình ngôn ngữ bằng độ hỗn loạn, hai bên bắt buộc dùng chung tập thử chưa từng thấy và cùng đúng một bộ tách từ tố. "
        "Đừng bao giờ so sánh hai con số đo trên hai bộ tách mảnh khác nhau vì chia nhỏ từ sẽ làm giảm nhân tạo độ hỗn loạn mỗi bước. "
        "Hãy chạy bài thực hành ngay sau đây để tự tính đồng thời độ hỗn loạn chính xác và xác suất làm trơn cộng một."
    ),
    "LLM:L02": (
        "Thuật toán mã hoá cặp byte bắt đầu từ danh sách ký tự hay từng byte nhỏ rồi liên tiếp gộp cặp liền nhau hay gặp nhất thành ký hiệu mới. "
        "Khi từ điển hợp nhất đủ nhỏ gọn, các từ thông dụng thành một mảnh duy nhất trong khi từ hiếm hoặc từ mới vẫn được tách mượt thành phần gốc quen thuộc. "
        "Điểm bắt buộc không được quên là khi tách một từ mới lúc chạy thật, ta phải áp dụng các luật gộp đúng theo thứ tự ưu tiên đã học lúc huấn luyện. "
        "Nếu đảo ngược thứ tự hai bước gộp, cùng một từ đầu vào có thể bị chia ra thành chuỗi mảnh hoàn toàn khác biệt. "
        "Trong tình huống hai cặp bất kỳ hoà nhau về tổng tần suất trong một bước, ta chọn cặp xuất hiện trước theo quy ước nhất quán. "
        "Trên thực tế triển khai mô hình đa ngôn ngữ, bộ từ tố học nhiều trên tiếng Anh thường khiến tiếng Việt tốn gấp hai tới ba lần số từ tố cho cùng một ý. "
        "Hệ quả trực tiếp là chi phí gọi hàm tính toán lẫn độ trễ trả lời của câu tiếng Việt đều tăng theo số mảnh bị cắt vụn. "
        "Nắm vững quy tắc đếm có trọng số theo tần suất từ điển giúp bạn hiểu sâu cách bộ tách hiện đại tối ưu băng thông ngữ cảnh. "
        "Hãy tự tay chạy vòng lặp hai bước gộp cặp ngay ở bài thực hành bên dưới để đối chiếu kết quả."
    ),
    "LLM:L03": (
        "Ý tưởng cốt lõi của vector nhúng là đưa mọi từ tố rời rạc vào một không gian số liên tục sao cho các từ xuất hiện cùng ngữ cảnh đứng gần nhau. "
        "Khi đo mức độ tương đồng bằng cô-sin giữa hai vector, ta chỉ xét góc hướng giữa chúng mà bỏ qua hoàn toàn chênh lệch độ dài véc-tơ. "
        "Hai vector cùng hướng cho cô-sin bằng một, còn hai vector vuông góc trực giao cho cô-sin đúng bằng không dù thành phần chứa các con số lớn. "
        "Tuy nhiên cần luôn tỉnh táo rằng hai từ trái nghĩa như nóng và lạnh hay tốt và xấu vẫn thường có cô-sin rất cao vì hay xuất hiện trong cùng mẫu câu. "
        "Do đó độ tương tự vector nhúng phản ánh mức độ liên quan về ngữ cảnh phân bố chứ chưa phải chứng minh cho quan hệ đồng nghĩa hay suy luận logic. "
        "Ở quy mô mô hình ngôn ngữ lớn với vài nghìn chiều nhúng, chuẩn hoá độ dài từng vector trước khi nhân ma trận giúp hệ tìm kiếm chạy cực nhanh. "
        "Khám phá ngay góc vuông và tích vô hướng qua bài tập tính cô-sin đơn giản trên ba chiều ngay sau đây."
    ),
    "LLM:L04": (
        "Kiến trúc giải mã tự hồi quy sinh từng từ tố từ trái sang phải nhờ mặt nạ nhân quả chặn đứng mọi đường nhìn trộm về các vị trí tương lai. "
        "Trong bảng ma trận vuông kích thước n nhân n, chỉ nửa tam giác dưới tính cả đường chéo chính gồm n nhân n cộng một chia hai ô là được phép truy cập. "
        "Bởi bản chất phép chú ý xử lý các cột song song không phân biệt thứ tự tự nhiên, việc cộng thêm mã hoá vị trí vào đầu vào là yêu cầu bắt buộc. "
        "Nếu thiếu thông tin vị trí, mô hình sẽ nhìn thấy hai câu đảo vị trí từ như hoàn toàn giống nhau và đánh mất cấu trúc ngữ pháp của câu. "
        "Khi chuyển từ huấn luyện song song cả chuỗi sang sinh chữ thật từng bước một, mỗi bước dự đoán mới được nối vào đuôi chuỗi để tiếp tục làm đầu vào kế tiếp. "
        "Hiểu trọn vẹn cấu trúc tam giác dưới và cơ chế vị trí này đặt nền tảng vững chắc cho bài tính bộ nhớ đệm khoá giá trị tiếp theo."
    ),
    "LLM:L06": (
        "Nhớ phân biệt rành mạch mục tiêu tối thiểu hoá mất mát entropy chéo trung bình theo từng vị trí dự đoán thay vì tối ưu sai lầm từng câu đơn lẻ."
    ),
    "LLM:L07": (
        "Trước một phân phối xác suất đầu ra tại mỗi bước, chiến lược chọn từ quyết định trực tiếp tính ổn định hay độ sáng tạo của văn bản sinh ra. "
        "Chia điểm thô cho nhiệt độ nhỏ hơn một làm phân phối dốc nhọn tập trung hẳn vào phương án đầu bảng, trong khi nhiệt độ lớn hơn một trải phẳng cơ hội cho nhánh hiếm. "
        "Cắt đuôi theo ngưỡng k cố định đơn giản nhưng dễ quá hẹp khi phân phối phẳng hoặc thừa quá nhiều lựa chọn vô nghĩa khi phân phối vốn đã dốc. "
        "Ngược lại lọc hạt nhân dựa trên tổng xác suất tích lũy tự động thu hẹp danh sách lúc mô hình tự tin và mở rộng lúc mô hình còn phân vân. "
        "Khi làm bài toán trích xuất ngắn hay viết mã đòi hỏi tính xác định cao, giảm nhiệt độ gần không hoặc chọn tham lam thường cho kết quả sạch nhất. "
        "Khi viết sáng tạo hay hội thoại dài, kết hợp nhiệt độ vừa phải với lọc tổng xác suất tránh được vòng lặp câu chữ nhàm chán. "
        "Lưu ý quy ước lọc tổng xác suất dừng ngay khi chạm hoặc vượt ngưỡng đã chọn trên danh sách đã sắp xếp giảm dần."
    ),
    "LLM:L08": (
        "Trong tinh chỉnh toàn bộ trọng số, ngoài lưu tham số mô hình còn phải giữ trạng thái bộ tối ưu và độ dốc làm bộ nhớ tăng vọt tới khoảng mười sáu byte mỗi số. "
        "Phân tích hạng thấp đóng băng ma trận trọng số gốc và chỉ huấn luyện cặp ma trận kẹp có hạng r nhỏ giúp giảm hàng trăm lần lượng tham số cập nhật. "
        "Đừng quên vai trò thực sự của tinh chỉnh là dạy mô hình định dạng đầu ra, giọng điệu hay kỹ năng chuyên biệt chứ không phải nạp kiến thức sự kiện mới. "
        "Để bổ sung dữ kiện biến động nhanh như văn bản nội bộ doanh nghiệp, đường ống truy xuất tài liệu luôn tiết kiệm và cập nhật linh hoạt hơn nhiều. "
        "Thứ tự tối ưu chi phí cho dự án thực tế luôn bắt đầu từ thử lời nhắc tốt, ghép thêm truy xuất ngữ cảnh rồi mới cân nhắc tinh chỉnh trọng số."
    ),
    "LLM:L09": (
        "Một mô hình ngôn ngữ đi qua ba nấc rõ ràng từ học đoán tiếp trên kho văn bản khổng lồ, tới học theo cặp chỉ dẫn mẫu và cuối cùng là căn chỉnh theo lựa chọn con người. "
        "Tại bước học mô hình phần thưởng theo cặp so sánh, xác suất câu thắng được đẩy lên bằng hàm xích-ma trên hiệu điểm thưởng giữa hai đáp án. "
        "Tuy nhiên nếu chỉ tối đa hoá thô điểm phần thưởng mà thả phanh trọng số, mô hình chính sách sẽ học cách khai thác kẽ hở bằng câu chữ dài dòng sáo rỗng. "
        "Thêm thành phần phạt độ lệch giữ mô hình mới không trôi quá xa bản trước đó giúp bảo toàn năng lực ngôn ngữ tự nhiên đã học. "
        "Chú ý luôn kiểm định chất lượng thực tế độc lập bằng bộ đánh giá riêng thay vì tin tuyệt đối vào chính mô hình chấm phần thưởng."
    ),
    "LLM:L10": (
        "Bất kỳ tỷ lệ phần trăm chính xác nào đo được trên tập kiểm tra hữu hạn đều là một biến ngẫu nhiên có sai số lấy mẫu đi kèm. "
        "Luôn báo cáo kèm biên độ khoảng tin cậy thay vì chỉ ghi điểm đơn lẻ giúp bạn tránh vội kết luận hệ mới thắng khi hai khoảng tin cậy còn chồng lấn lớn. "
        "Khi muốn so trực diện hai mô hình làm trên cùng một bộ câu hỏi, kiểm định theo cặp tập trung vào đúng tập câu hai bên cho kết quả bất đồng sẽ nhạy hơn nhiều. "
        "Rủi ro nghiêm trọng nhất ở các bảng xếp hạng công khai là nhiễm dữ liệu kiểm tra lọt vào tập huấn luyện trước làm điểm tăng ảo hoàn toàn. "
        "Thực hành tính biên độ khoảng tin cậy chín mươi lăm phần trăm trên tám trăm câu hỏi ngay sau đây giúp bạn thấy rõ tác động của cỡ mẫu."
    ),
    "LLM:L11": (
        "Ảo giác xuất hiện tự nhiên vì mô hình học tối đa hoá độ trôi chảy xác suất chuỗi câu chứ không mặc định kiểm chứng sự thật ngoài đời. "
        "Thước đo sai số hiệu chuẩn kỳ vọng đối chiếu độ tự tin mô hình tự gán ở từng khoảng với tỷ lệ trả lời đúng thực tế trong chính nhóm đó. "
        "Một mô hình được hiệu chuẩn tốt sẽ đúng xấp xỉ chín mươi phần trăm khi nó nói mức tự tin chín mươi phần trăm, tránh tình trạng tự tin mù quáng lúc sai. "
        "Để nâng độ chính xác bài toán suy luận, biểu quyết đa số trên nhiều lần lấy mẫu độc lập tỏ ra rất hiệu quả miễn xác suất đúng mỗi lượt vượt quá một nửa. "
        "Tuy nhiên nếu các lần lấy mẫu lặp lại cùng một lối suy nghĩ sai tương quan nhau, biểu quyết nhiều lần chỉ làm khuếch đại đáp án sai đồng loạt."
    ),
    "LLM:L12": (
        "Đường ống sinh có truy xuất biến tri thức tĩnh cồng kềnh bên trong trọng số thành kho văn bản ngoài có thể cập nhật tức thì bất cứ lúc nào. "
        "Văn bản gốc được chia thành các đoạn nhỏ vừa ngữ cảnh, nhúng thành véc-tơ số rồi lập chỉ mục tìm nhanh k đoạn liên quan nhất cho mỗi câu hỏi. "
        "Một lỗi bảo mật hay gặp ở sản phẩm doanh nghiệp là quên lọc quyền truy cập theo từng người dùng trước khi đưa đoạn vào lời nhắc khiến rò rỉ dữ liệu mật. "
        "Ngoài ra hãy luôn đo riêng độ phủ của bước truy xuất xem đoạn đúng có thật sự nằm trong nhóm đầu hay không trước khi đổ lỗi cho bước sinh chữ. "
        "Kết hợp tìm kiếm từ khoá chính xác với tìm theo ngữ nghĩa véc-tơ cho hiệu quả vượt trội trên các truy vấn hỗn hợp."
    ),
    "LLM:L13": (
        "Khi kéo dài ngữ cảnh từ vài nghìn lên hàng chục nghìn từ tố, bộ nhớ đệm tăng tuyến tính nhưng khối lượng phép tính tự chú ý tăng vọt theo bình phương độ dài. "
        "Ngay cả khi phần cứng chứa vừa ngữ cảnh dài, hiện tượng hụt thông tin ở giữa chuỗi vẫn dễ xảy ra khiến mô hình hay bỏ sót chi tiết chôn giữa tài liệu dài. "
        "Các kỹ thuật tăng tốc như lượng tử hoá trọng số xuống bốn hoặc tám bit, gom lô liên tục và giải mã suy đoán giúp cắt mạnh chi phí phục vụ mỗi yêu cầu. "
        "Luôn nhớ kiểm thử lại chất lượng đầu ra và tốc độ thực tế sau từng thay đổi nén hay tối ưu phần cứng."
    ),
}

for rel, (old, new) in []:
    rep(rel, old, new)
for rel, ext in RECAP0_TOPUPS.items():
    append_recap0(rel, ext)

# Fix any remaining 'càng ' in IRS/AGT/LLM/RLN/CVI lessons automatically reported if any, and lint all 69 lessons
bad = []
for c in ("irs", "agt", "llm", "rln", "cvi"):
    for fp in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        lid = sp["id"]
        w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        if res.errors or res.warnings:
            bad.append(f"{c.upper()}:{lid} E={res.errors} W={res.warnings}")
        if w < 1645:
            bad.append(f"{c.upper()}:{lid} w={w} (need +{1655-w})")
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                say = st.get("say") or ""
                foc = st.get("focus")
                sents = lv.sentences(say)
                if foc is not None and len(foc) != len(sents):
                    bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
                for s in sents:
                    if len(s) > 170: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >170 ({len(s)}): {s}")
                    if len(s.split()) > 38: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >38w ({len(s.split())}): {s}")
                    if "càng " in s.lower(): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} 'càng ': {s}")
                    if re.search(r"[$_^]", s): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} TeX: {s}")
        print(f"CHECK {c.upper()}:{lid} w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)

for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} issues across 5 Stage 9 courses"

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
r = subprocess.run([PY, "-B", "-u", "audit/s9_11/up_s9_llm_rl_cv.py"], cwd=ROOT)
assert r.returncode == 0, "FAILED: up_s9_llm_rl_cv.py"
for c in ("IRS", "AGT", "LLM", "RLN", "CVI"):
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
    ):
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"FAILED: {cmd}"
print("ALL 5 STAGE 9 COURSES (IRS/AGT/LLM/RLN/CVI = 69 LESSONS) PASSED!", flush=True)
