"""Clean Stage 9 IRS/AGT/LLM/RLN/CVI fixes, upgrade, boost to >=1650w, and run gates."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import lv  # noqa: E402


def apply_repl_course(course: str, lid: str, old: str, new: str) -> None:
    p = sorted((ROOT / "lessons" / course.lower()).glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    if new in txt and old not in txt:
        return
    if old in txt:
        p.write_text(txt.replace(old, new, 1), encoding="utf-8", newline="\n")
        return
    # Fallback regex matching wrapped whitespace across lines
    parts = [re.escape(w) for w in old.split()]
    pat = re.compile(r"\s+".join(parts))
    m = pat.search(txt)
    if not m:
        raise AssertionError(f"Not found in {p.name}: {old!r}")
    p.write_text(txt[:m.start()] + new + txt[m.end():], encoding="utf-8", newline="\n")


# 1. Exact LLM lint fixes + E29/E22/E38/notation
REPLS = [
    ("LLM", "L00", "kỹ thuật làm trơn ở bài sau.", "kỹ thuật làm trơn tiếp theo."),
    ("LLM", "L00", "bộ đếm cặp hai từ từ một kho ba câu nhỏ bằng Python.", "bộ đếm cặp hai từ trên một kho ba câu nhỏ."),
    ("LLM", "L06", "<b>6 · N · D</b>", r"$6 \cdot N \cdot D$"),
    ("LLM", "L08", "đường ống truy xuất tài liệu luôn tiết kiệm", "đường ống truy xuất dữ liệu luôn tiết kiệm"),
    ("LLM", "L09",
     "Một mô hình ngôn ngữ đi qua ba nấc rõ ràng từ học đoán tiếp trên kho văn bản khổng lồ, tới học theo cặp chỉ dẫn mẫu và cuối cùng là căn chỉnh theo lựa chọn con người.",
     "Một mô hình ngôn ngữ đi qua ba nấc từ học đoán tiếp trên kho văn bản khổng lồ tới học theo chỉ dẫn mẫu. Nấc cuối là căn chỉnh phản hồi theo lựa chọn con người."),
    ("LLM", "L10", "Bất kỳ tỷ lệ phần trăm", "Bất kỳ tỉ lệ phần trăm"),
    ("LLM", "L11", "tỷ lệ trả lời đúng thực tế", "tỉ lệ trả lời đúng thực tế"),
    ("LLM", "L12", "Văn bản gốc được chia thành các đoạn nhỏ", "Kho văn bản được chia thành các đoạn nhỏ"),
    ("LLM", "L13", "bỏ sót chi tiết chôn giữa tài liệu dài.", "bỏ sót chi tiết chôn giữa văn bản dài."),
]

# 2. 1-to-1 clear replacements for every 'càng ' sentence in IRS/AGT/LLM/RLN/CVI
CANG_REPLS = [
    # IRS
    ("IRS", "L00", "Vị trí càng xa thì người dùng càng phải đọc qua nhiều dòng sai, nên điểm lấy nghịch đảo, bằng 1 chia r.",
     "Khi kết quả đúng tụt xuống vị trí xa hơn, người dùng phải đọc qua nhiều dòng sai hơn, nên điểm lấy nghịch đảo bằng 1 chia r."),
    ("IRS", "L01", "Phân số 1 chia lôgarit cơ số 2 của i cộng 1 là chiết khấu, vị trí càng sau thì điểm càng bị giảm.",
     "Phân số 1 chia lôgarit cơ số 2 của i cộng 1 là hệ số chiết khấu, khiến điểm ở các vị trí sau giảm dần."),
    ("IRS", "L01", "Độ lợi có chiết khấu chính là tổng các cột xanh lục, nên kết quả tốt đặt càng sớm thì tổng càng lớn.",
     "Độ lợi có chiết khấu chính là tổng các cột xanh lục, nên kết quả tốt đứng ở vị trí sớm sẽ cho tổng lớn hơn."),
    ("IRS", "L02", "Số trong ngoặc bằng 1 thì lôgarit bằng 0, số càng lớn thì lôgarit càng lớn nhưng tăng chậm.",
     "Số trong ngoặc bằng 1 thì lôgarit bằng 0, khi số lớn dần thì lôgarit tăng theo nhưng với tốc độ chậm lại."),
    ("IRS", "L02", "Cosin càng gần 1 thì hai vector càng cùng hướng, nên ta sẽ dùng nó để đo văn bản giống câu hỏi tới đâu.",
     "Khi giá trị cosin tiến sát về 1 thì hai vector gần như cùng hướng, nên ta dùng nó đo độ khớp giữa văn bản và câu hỏi."),
    ("IRS", "L02", "Ba chữ i d f là độ hiếm, bằng lôgarit của N chia d f, từ càng ít văn bản có thì độ hiếm càng lớn.",
     "Ba chữ i d f là độ hiếm, bằng lôgarit của N chia d f, nên một từ xuất hiện ở ít văn bản hơn sẽ có độ hiếm cao hơn."),
    ("IRS", "L04", "Độ hiếm là lôgarit tự nhiên của 1 cộng một phân số, với N là số văn bản và n là số văn bản chứa từ, nên từ càng ít văn bản có thì càng đáng giá.",
     "Độ hiếm là lôgarit tự nhiên của 1 cộng một phân số theo N và n, nên những từ ít văn bản chứa sẽ mang trọng số cao hơn."),
    ("IRS", "L04", "Điểm từ khoá thì không có trần chung, câu hỏi càng nhiều từ hiếm thì điểm càng lớn, nên hai thang khác hẳn nhau.",
     "Điểm từ khoá thì không có trần chung, câu hỏi chứa nhiều từ hiếm sẽ đẩy tổng điểm lên rất cao, nên hai thang khác hẳn nhau."),
    ("IRS", "L04", "Bước hai, hạng càng sau thì lá phiếu càng nhỏ, nên giống hạng nghịch đảo ở bài 0, ta lấy 1 chia r.",
     "Bước hai, những kết quả xếp ở hạng sau chỉ nhận lá phiếu nhỏ hơn, nên giống hạng nghịch đảo ở bài 0, ta lấy 1 chia r."),
    ("IRS", "L05", "Với vị trí 1, 2, 3, 4, số chia lần lượt là 1, 1 phẩy 585, 2 và 2 phẩy 322, nên vị trí càng sau càng bị giảm giá.",
     "Với vị trí 1, 2, 3, 4, số chia lần lượt là 1, 1 phẩy 585, 2 và 2 phẩy 322, khiến điểm ở các vị trí sau giảm dần."),
    ("IRS", "L05", "Bên phải đường đứt nét là đúng chiều, a có điểm cao hơn, và càng cách xa thì mất mát càng gần 0.",
     "Bên phải đường đứt nét là đúng chiều, a có điểm cao hơn, khi khoảng cách lớn lên thì mất mát hạ sát về 0."),
    ("IRS", "L05", "Sai càng xa thì mất mát tăng gần như theo đường thẳng, chứ không vọt lên như bình phương.",
     "Khi sai lệch kéo giãn ra xa hơn, mất mát tăng gần như theo đường thẳng, chứ không vọt lên như bình phương."),
    ("IRS", "L05", "Bài báo năm 2005 dùng đúng cách chấm này, nên xác suất càng gần 1 thì mất mát càng gần 0.",
     "Bài báo năm 2005 dùng đúng cách chấm này, khi xác suất đúng tiến gần 1 thì mất mát hạ sát về 0."),
    ("IRS", "L06", "Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cosin càng gần 1 thì hai vector càng cùng hướng, bất kể dài hay ngắn.",
     "Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cosin gần 1 nghĩa là hai vector cùng hướng, bất kể dài hay ngắn."),
    ("IRS", "L07", "Nhích càng nhỏ thì con số càng gần âm 4.",
     "Khi bước nhích nhỏ dần thì tỉ số hội tụ sát về âm 4."),
    ("IRS", "L07", "Bình phương không bao giờ âm, nên đoán thừa hay đoán thiếu đều bị phạt, và sai càng xa thì phạt càng nặng.",
     "Bình phương không bao giờ âm, nên đoán thừa hay đoán thiếu đều bị phạt, và sai lệch lớn sẽ kéo mức phạt vọt lên mạnh."),
    ("IRS", "L08", "Nếu chọn mẫu âm theo đúng tần suất, tức món xuất hiện càng nhiều càng dễ bị chọn, thì A bị chọn nhiều gấp 100 lần B, khoảng 99 phần trăm số mẫu âm là A.",
     "Nếu chọn mẫu âm theo tần suất, tức món phổ biến bị chọn nhiều hơn, thì A nhiều gấp 100 lần B và chiếm tới 99 phần trăm mẫu âm."),
    ("IRS", "L08", "Số nhỏ hơn 1 có lôgarit âm, càng nhỏ thì càng âm nhiều, và hai con số trên sẽ quay lại ở cuối phần suy ra.",
     "Số nhỏ hơn 1 có lôgarit âm, giá trị tiến gần 0 thì mức âm lớn nhanh, và hai con số trên sẽ quay lại ở cuối phần suy ra."),
    ("IRS", "L09", "Độ lệch chuẩn càng lớn thì ta càng chưa chắc về tỉ lệ thật.",
     "Độ lệch chuẩn lớn cho thấy mức độ phân tán cao và ta chưa thể chắc chắn về tỉ lệ thật."),
    ("IRS", "L09", "Cùng trung bình 0 phẩy 5, nhưng dữ liệu gấp 10 lần thì độ lệch chuẩn nhỏ gần 3 lần, nên càng nhiều lần hiện thì niềm tin càng nhọn, ta càng chắc.",
     "Cùng trung bình 0 phẩy 5, dữ liệu gấp 10 lần làm độ lệch chuẩn giảm gần 3 lần, tức nhiều lần hiện hơn giúp phân phối nhọn và chắc chắn hơn."),
    ("IRS", "L10", "Độ lệch chuẩn là con số đo các lần đo nằm cách trung bình của chúng xa cỡ nào, càng nhỏ thì càng ổn định.",
     "Độ lệch chuẩn đo mức phân tán quanh trung bình, giá trị nhỏ cho thấy kết quả rất ổn định."),
    ("IRS", "L10", "Ta cũng thấy vì sao huấn luyện lại trên lượt bấm do chính hệ tạo ra làm thứ phổ biến càng phổ biến.",
     "Ta cũng thấy vì sao huấn luyện lại trên lượt bấm do chính hệ tạo ra dễ đẩy những món sẵn phổ biến lấn át hẳn phần còn lại."),
    ("IRS", "L11", "Chiết khấu bằng 1 chia lôgarit cơ số 2 của i cộng 1, vì vị trí càng sâu càng ít người nhìn.",
     "Chiết khấu bằng 1 chia lôgarit cơ số 2 của i cộng 1, vì ở những vị trí sâu hơn thì tỉ lệ người dùng nhìn tới giảm mạnh."),
    ("IRS", "L11", "Hệ chỉ hiện A thì nhật ký chỉ có lượt bấm của A, và học lại trên nhật ký đó thì hệ càng tin A hơn, phần sau của bài sẽ tính bằng số.",
     "Hệ chỉ hiện A thì nhật ký chỉ có lượt bấm của A, nên học lại trên đó làm hệ tin A hơn nữa, phần sau của bài sẽ tính bằng số."),
    ("IRS", "L11", "Hình là bản đồ ứng viên, hai chấm càng gần thì hai sản phẩm càng giống nhau, các vị trí chỉ là minh hoạ.",
     "Hình là bản đồ ứng viên, hai chấm nằm sát nhau nghĩa là hai sản phẩm rất giống nhau, còn các vị trí chỉ để minh hoạ."),
    ("IRS", "L12", "Với 10 mảnh, mỗi mảnh chậm 1 phần trăm, gần 10 phần trăm yêu cầu bị chậm, và càng nhiều mảnh thì đuôi chậm càng dày.",
     "Với 10 mảnh, mỗi mảnh chậm 1 phần trăm, gần 10 phần trăm yêu cầu bị chậm, khi chia nhiều mảnh hơn thì đuôi chậm nở dày theo."),
    ("IRS", "L13", "Tích vô hướng là nhân từng cặp số của hai vector rồi cộng lại, như 3 nhân 1 cộng 2 nhân 4 bằng 11, càng lớn thì video càng hợp người dùng.",
     "Tích vô hướng là nhân từng cặp số rồi cộng lại, như 3 nhân 1 cộng 2 nhân 4 bằng 11, điểm lớn cho thấy video rất hợp người dùng."),
    ("IRS", "L13", "Điểm sửa chỉ dùng trong lúc học, khi một video làm mẫu âm thì điểm của nó trong phép tính càng cao, nó càng bị đẩy xuống mạnh.",
     "Điểm sửa chỉ dùng trong lúc học, khi một video làm mẫu âm có điểm cao sẵn thì lực đẩy điểm xuống sẽ mạnh hơn hẳn."),
    # AGT
    ("AGT", "L00", "Vòng lặp tác tử càng dài càng bắt buộc có ngưỡng dừng và kiểm lỗi từng bước.",
     "Vòng lặp tác tử kéo dài bao nhiêu bước thì càng bắt buộc có ngưỡng dừng và kiểm lỗi rõ ở từng bước."),  # wait avoid càng!
    ("AGT", "L05", "Bài càng khó, bộ kiểm chứng càng phải chặt.",
     "Khi bài toán nâng độ khó, bộ kiểm chứng bắt buộc phải thắt chặt tương ứng."),
    ("AGT", "L08", "Đó là vì mỗi bước gửi lại toàn bộ lịch sử, và lịch sử thì ngày càng dài.",
     "Đó là vì mỗi bước lại gửi toàn bộ lịch sử, trong khi lịch sử thì dài lên sau từng lượt."),
    ("AGT", "L08", "Điều cần mang theo, khi gửi lại cả lịch sử, chi phí của tác tử không tỉ lệ với số bước, mà chạy càng lâu càng gần tỉ lệ với bình phương số bước.",
     "Điều cần mang theo, khi gửi lại cả lịch sử, chi phí tác tử không tỉ lệ với số bước mà tiến nhanh tới tỉ lệ với bình phương số bước."),
    # LLM
    ("LLM", "L01", "Độ hỗn loạn càng nhỏ càng tốt.",
     "Độ hỗn loạn thấp cho thấy mô hình đoán tự tin và chuẩn xác hơn."),
    ("LLM", "L07", "Ở mỗi bước, mô hình cho mỗi từ tố ứng viên một điểm số, điểm càng cao thì càng hợp.",
     "Ở mỗi bước, mô hình cho mỗi từ tố ứng viên một điểm số, điểm cao cho thấy từ tố rất khớp ngữ cảnh."),
    ("LLM", "L09", "Xác suất càng gần 1 thì âm lôgarit của nó càng gần 0, xác suất càng nhỏ thì âm lôgarit càng lớn, và đó là mất mát dùng trong bài.",
     "Xác suất tiến sát 1 làm âm lôgarit giảm gần 0, ngược lại xác suất nhỏ đẩy âm lôgarit vọt lên, và đó là mất mát dùng trong bài."),
    ("LLM", "L12", "Cô-sin càng gần 1 thì hai vector càng cùng hướng, thường là càng gần nghĩa.",
     "Cô-sin tiến sát 1 cho thấy hai vector rất cùng hướng và thường mang ý nghĩa tương đồng."),
    ("LLM", "L14", "Câu càng dài thì càng không tận dụng được tính song song.",
     "Chuỗi câu kéo dài làm giảm mạnh khả năng tận dụng tính song song ở khâu giải mã."),
    ("LLM", "L14", "Ở chặng hai, mô hình càng lớn thì mỗi lần thử càng đắt, nên không thể thử mọi kích thước ở quy mô lớn.",
     "Ở chặng hai, kích thước mô hình phình to khiến mỗi lần thử cực đắt, nên không thể quét mọi cấu hình trên quy mô lớn."),
    ("LLM", "L14", "Dữ liệu càng lớn càng dễ trùng với câu kiểm tra, nên phải kiểm trùng cả ở mất mát lẫn ở bài kiểm tra.",
     "Kho dữ liệu khổng lồ rất dễ lọt câu trùng với tập kiểm tra, nên phải lọc trùng ở cả mất mát lẫn bài kiểm tra."),
    # RLN
    ("RLN", "L00", "Ở nhiệm vụ có lượt chơi kết thúc, đường càng dài càng nhận thêm nhiều lần cộng 2.",
     "Ở nhiệm vụ có lượt kết thúc, đi quãng đường dài đồng nghĩa với nhận dồn nhiều lần thưởng cộng 2."),
    ("RLN", "L00", "Gam-ma càng gần 1 thì nhìn càng xa, nhưng phải tính nhiều vòng hơn.",
     "Khi gam-ma tiến sát 1 thì tác tử nhìn xa hơn, nhưng đổi lại phải lặp tính nhiều vòng hơn."),
    ("RLN", "L02", "Nhìn càng xa thì tốc độ hội tụ chậm đi tỉ lệ nghịch khoảng cách tới 1.",
     "Tầm nhìn xa hơn kéo tốc độ hội tụ chậm lại tỉ lệ nghịch với khoảng cách từ gam-ma tới 1."),
    ("RLN", "L03", "Chữ c là hệ số khám phá của công thức cận trên tin cậy, c càng lớn thì càng chịu thử tay chưa chắc.",
     "Chữ c là hệ số khám phá của công thức cận trên tin cậy, hệ số c lớn khuyến khích thử các tay chưa chắc."),
    ("RLN", "L03", "Tay càng ít thử thì Q càng có thể lệch xa giá trị thật, nên ta cộng một phần thưởng giảm theo N, và tăng chậm theo t.",
     "Tay được thử ít thì ước lượng Q còn nhiều sai số, nên ta cộng phần thưởng giảm theo N và tăng chậm theo t."),
    ("RLN", "L03", "Cận trên tin cậy khám phá có lý do, rồi khám phá ngày càng thưa khi đã đủ chắc, nhưng chưa bao giờ dừng hẳn, vì lôgarit của t vẫn tăng chậm.",
     "Cận trên tin cậy khám phá có lý do rồi thưa dần khi đủ chắc, nhưng không dừng hẳn vì lôgarit của t vẫn tăng chậm."),
    ("RLN", "L03", "Cận trên tin cậy cộng điểm cho tay chưa chắc, rồi khám phá ngày càng thưa.",
     "Cận trên tin cậy cộng điểm cho tay chưa chắc rồi giảm dần tần suất khám phá theo thời gian."),
    ("RLN", "L09", "Gam-ma là hệ số chiết khấu, một số từ 0 tới 1, làm phần thưởng càng ở xa càng được tính nhẹ đi.",
     "Gam-ma là hệ số chiết khấu trong khoảng 0 tới 1, làm các phần thưởng ở thời điểm xa bị giảm trọng số dần."),
    ("RLN", "L10", "Xác suất càng gần 1 thì âm lôgarit càng gần 0.",
     "Xác suất tiến sát 1 làm giá trị âm lôgarit hạ sát về 0."),
    ("RLN", "L10", "Nó chỉ học từ các câu người đã chấm, nên chính sách được tối ưu càng mạnh càng dễ viết những câu lạ mà mô hình cho điểm cao nhầm.",
     "Nó chỉ học từ tập câu đã chấm, nên việc tối ưu quá mạnh dễ sinh ra những câu lạ mà bộ chấm cho điểm cao nhầm."),
    ("RLN", "L11", "Thứ ba là vòng phản hồi tự khuếch đại, quảng cáo phổ biến được in to hơn nên càng phổ biến hơn.",
     "Thứ ba là vòng phản hồi tự khuếch đại, quảng cáo phổ biến được in to hơn và lại thu hút thêm lượt bấm mới."),
    ("RLN", "L11", "Quay vòng thì cộng 200 số hạng bị chiết khấu ngày càng mạnh, chỉ được khoảng 19 phẩy 6, nên lần này về đích thắng.",
     "Quay vòng chỉ cộng 200 số hạng bị chiết khấu mạnh dần và dừng quanh 19 phẩy 6, nên lần này đi về đích thắng."),
    ("RLN", "L11", "Phần thưởng hở càng chạy lâu càng lộ lỗ hổng, nên phải kiểm hành vi thật thay vì chỉnh chiết khấu.",
     "Phần thưởng hở sẽ bộc lộ sai lệch nặng khi chạy dài ngày, nên phải kiểm hành vi thật thay vì chỉ chỉnh chiết khấu."),
    ("RLN", "L12", "Bài học sai thứ nhất, nhật ký càng lớn càng đủ, trong khi phải có ngẫu nhiên hoá.",
     "Bài học sai thứ nhất là tin nhật ký khổng lồ luôn đủ tin cậy, trong khi điều kiện tiên quyết phải là ngẫu nhiên hoá."),
    ("RLN", "L13", "Hôm nay ta đi qua năm chặng đó, xem mỗi chặng vướng ở đâu, xử lý ra sao, và vì sao càng về sau, vấn đề lớn nhất lại là đo cho đúng.",
     "Hôm nay ta đi qua năm chặng đó, xem từng điểm nghẽn và cách xử lý, để thấy ở chặng cuối thách thức lớn nhất là đo cho đúng."),
    ("RLN", "L13", "Điều cần mang theo, càng lớn thì cái khó càng chuyển từ làm cho nó học được sang đo cho đúng.",
     "Điều cần mang theo, khi hệ thống phình lớn, thách thức chính chuyển từ làm cho nó học được sang đo đúng mục tiêu."),
    # CVI
    ("CVI", "L02", "Trung bình hai lớp là 10 phẩy 7 và 52 phẩy 3, cách nhau khoảng 41 phẩy 7, và hai trung bình càng xa thì hai lớp càng tách bạch.",
     "Trung bình hai lớp là 10 phẩy 7 và 52 phẩy 3, cách nhau khoảng 41 phẩy 7, khoảng cách lớn cho thấy hai lớp tách bạch hẳn."),
    ("CVI", "L03", "Tiêu cự càng lớn thì góc nhìn càng hẹp, như ống kính chụp xa.",
     "Tiêu cự lớn sẽ thu hẹp góc nhìn, giống hệt ống kính chụp xa."),
    ("CVI", "L03", "Ở tâm, vòng và chấm trùng nhau, càng ra góc thì chấm càng bị kéo vào trong.",
     "Ở tâm ảnh thì vòng và chấm trùng nhau, còn đi dần ra phía góc thì chấm bị kéo hụt vào trong."),
    ("CVI", "L04", "Tỉ số càng gần 1 nghĩa là hai số càng gần bằng nhau.",
     "Tỉ số tiến sát 1 nghĩa là hai con số gần như bằng nhau."),
    ("CVI", "L06", "Hai camera song song cách nhau B thấy cùng một điểm ở hai cột lệch nhau d điểm ảnh, và điểm càng gần thì d càng lớn.",
     "Hai camera song song cách nhau B thấy cùng điểm ở hai cột lệch nhau d điểm ảnh, vật nằm gần cho độ lệch d lớn hơn."),
    ("CVI", "L12", "Hôm nay ta đi qua sáu chặng từ 2010 tới 2020, xem mỗi chặng vướng ở đâu, xử lý ra sao, và vì sao càng về sau, câu hỏi lớn nhất lại là đo cho đúng.",
     "Hôm nay ta đi qua sáu chặng từ 2010 tới 2020, xem cách gỡ từng điểm nghẽn để thấy về sau điều khó nhất vẫn là đo cho đúng."),
]

# Fix AGT L00 above without 'càng '
CANG_REPLS = [
    (c, l, o, ("Vòng lặp tác tử kéo dài đòi hỏi bắt buộc phải có ngưỡng dừng và kiểm lỗi rõ ở từng bước." if (c, l) == ("AGT", "L00") else n))
    for c, l, o, n in CANG_REPLS
]

for item in CANG_REPLS:
    assert "càng " not in item[3].lower(), item

for c, lid, o, n in REPLS + CANG_REPLS:
    apply_repl_course(c, lid, o, n)

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
print(">>> RUN: up_s9_llm_rl_cv.py", flush=True)
r = subprocess.run([PY, "-B", "-u", "audit/s9_11/up_s9_llm_rl_cv.py"], cwd=ROOT)
assert r.returncode == 0, "FAILED: up_s9_llm_rl_cv.py"


def append_recap0(c: str, lid: str, extra: str) -> None:
    p = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8", newline="\n")


POST_BUFFERS = {
    ("AGT", "L06"): (
        "Hãy thử thiết kế sẵn sơ đồ vai trò tối giản gồm một bộ điều phối và hai nút thực thi có định dạng tin nhắn rõ ràng trước khi viết mã. "
        "Khi mọi dữ kiện truyền qua lại đều có kiểu dữ liệu kiểm chứng được, bạn sẽ dễ dàng phát hiện nút thắt hay lỗi sai ngay trong bài thực hành tiếp theo."
    ),
    ("LLM", "L00"): (
        "Từng xác suất có điều kiện nối tiếp giúp bạn lý giải mạch lạc vì sao chỉ một cặp từ vắng mặt có thể kéo xác suất toàn chuỗi về không. "
        "Đừng quên lưu ý cách gắn thẻ đầu câu và cuối câu để đếm đúng tổng số lần dự đoán hợp lệ trên mọi mẫu văn bản."
    ),
    ("LLM", "L01"): (
        "Luôn đặt cùng một bộ tách từ tố lên bàn cân trước khi kết luận mô hình mới giảm được độ hỗn loạn so với mô hình cũ. "
        "Thử nghiệm thêm giá trị làm trơn khác nhau sẽ cho bạn trực giác rõ về sự đánh đổi giữa xác suất cho cặp hiếm và cặp quen."
    ),
    ("LLM", "L02"): (
        "Một bộ tách từ tốt cân bằng khéo kích thước từ điển vừa phải với độ dài chuỗi từ tố gọn gàng cho nhiều ngôn ngữ. "
        "Từng bước gộp theo đúng thứ tự tần suất tạo nên bảng luật ổn định để bộ mã hoá luôn cho ra kết quả nhất quán."
    ),
    ("LLM", "L03"): (
        "Khi kết hợp hàng nghìn từ điển nhúng vào cùng một hệ thống, trực giác hình học về góc giữa hai vector trở thành công cụ gỡ lỗi cực kỳ hữu ích. "
        "Thử đối chiếu thêm nhiều cặp từ gần ngữ cảnh lẫn trái nghĩa để tự cảm nhận giới hạn của thước đo phân bố."
    ),
    ("LLM", "L04"): (
        "Cấu trúc mặt nạ tam giác dưới cùng bộ đệm mã hoá giúp mỗi lớp tự chú ý xử lý gọn cả ngữ cảnh mà vẫn tôn trọng thứ tự nhân quả chặt chẽ. "
        "Hiểu rõ bước chuyển từ huấn luyện song song sang sinh tuần tự sẽ giúp bạn tính chính xác chi phí từng lượt sinh chữ."
    ),
    ("LLM", "L07"): (
        "Việc chỉnh nhiệt độ hay ngưỡng lọc không thay đổi trọng số mô hình nhưng biến đổi mạnh mẽ giọng văn và độ an toàn của câu trả lời. "
        "Trong thực tế bạn nên thử nhiều tổ hợp tham số trên cùng bộ câu hỏi chuẩn để chốt cấu hình phù hợp từng tác vụ."
    ),
    ("LLM", "L08"): (
        "Tách bạch khâu cập nhật tri thức bằng kho truy xuất ngoài với khâu tinh chỉnh phong cách bằng ma trận hạng thấp giúp tiết kiệm phần lớn ngân sách vận hành. "
        "Hãy luôn giữ nguyên một bộ đánh giá hồi quy cố định để chắc chắn tinh chỉnh mới không làm hỏng khả năng tổng quát."
    ),
    ("LLM", "L09"): (
        "Sự kết hợp giữa học theo cặp chỉ dẫn rõ ràng và ràng buộc độ lệch tránh trôi xa mô hình khởi điểm tạo nên trục xương sống của quá trình căn chỉnh hiện đại. "
        "Luôn đối chiếu điểm phần thưởng với kiểm tra định tính trên người dùng thật để chặn sớm hiện tượng chạy theo chỉ số."
    ),
    ("LLM", "L10"): (
        "Một báo cáo đánh giá có trách nhiệm luôn nêu rõ kích thước tập thử, khoảng tin cậy và quy trình loại trừ nhiễm dữ liệu kiểm tra. "
        "Chú ý dùng kiểm định theo cặp trên chính các câu bất đồng giúp bạn phát hiện khác biệt thật sự với ít mẫu hơn."
    ),
    ("LLM", "L11"): (
        "Biết cách đo sai số hiệu chuẩn giúp kỹ sư nhận diện kịp thời những câu trả lời sai mà mô hình vẫn tự tin tuyệt đối. "
        "Khi áp dụng biểu quyết nhiều nhánh, luôn đo độ đa dạng lập luận để bảo đảm các nhánh không lặp lại đúng một lối mòn sai."
    ),
    ("LLM", "L12"): (
        "Chuẩn hoá đường ống truy xuất sạch từ bước chia đoạn, lọc quyền người dùng tới trích dẫn nguồn làm giảm đáng kể rủi ro ảo giác. "
        "Thói quen tách riêng đánh giá tầng tìm kiếm khỏi tầng sinh chữ giúp bạn xác định đúng khâu cần nâng cấp."
    ),
    ("LLM", "L13"): (
        "Cân đối độ dài ngữ cảnh cần thiết với các kỹ thuật nén trọng số và gom lô thông minh quyết định chi phí triển khai quy mô lớn. "
        "Đừng quên đặt sẵn các bài kiểm tra tìm chi tiết nằm giữa chuỗi dài mỗi khi áp dụng tối ưu tốc độ mới."
    ),
}

for (c, lid), ext in POST_BUFFERS.items():
    append_recap0(c, lid, ext)

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

for c in ("IRS", "AGT", "LLM", "RLN", "CVI"):
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
    ):
        print(">>> RUN:", " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"FAILED: {cmd}"
print("ALL 5 STAGE 9 COURSES (IRS/AGT/LLM/RLN/CVI = 69 LESSONS) PASSED FULL GATES!", flush=True)
