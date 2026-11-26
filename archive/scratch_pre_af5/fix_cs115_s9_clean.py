from pathlib import Path
import re
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    assert old in txt, f"Missing in {rel}: {old[:110]!r}"
    assert txt.count(old) == 1, f"Non-unique in {rel}: {old[:110]!r}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


# Split/shorten every >170 chars / >38 words sentence + remove 'càng ' cleanly
PATCHES = [
    ("lessons/cs115/L25_svm.yaml",
     "Khi dữ liệu không tách thẳng hoàn toàn hoặc dính nhiễu, mô hình lề mềm kết hợp hàm mất mát bản lề với phạt bình phương L2 cho phép đánh đổi độ rộng lề lấy số lần vi phạm nhỏ nhất.",
     "Khi dữ liệu dính nhiễu và không tách thẳng được, mô hình lề mềm dùng hàm mất mát bản lề cộng phạt bình phương L2. Nhờ vậy ta đánh đổi khéo độ rộng lề lấy số lần vi phạm ít nhất."),
    ("lessons/cs115/L27_knn.yaml",
     "Hãy luôn chọn K lẻ khi có hai lớp, dùng kiểm định chéo thay vì kiểm trên chính tập lưu để tránh chọn nhầm K bằng một, và chuẩn hoá mọi cột về cùng thang đo trước khi đo bất kỳ khoảng cách nào.",
     "Hãy chọn K lẻ khi có hai lớp và dùng kiểm định chéo để tránh chọn nhầm K bằng một. Nhớ chuẩn hoá mọi cột về cùng thang đo trước khi tính bất kỳ khoảng cách nào. Trên thực tế, nếu dữ liệu mất cân bằng nặng, bạn có thể thử trọng số nghịch đảo theo khoảng cách để điểm gần được ưu tiên phiếu bầu hơn. Đồng thời chuẩn bị một bản lưu riêng trên đĩa hoặc chỉ mục tìm nhanh sẽ giúp hệ thống trả lời truy vấn thời gian thực mà không cần quét thô toàn bảng."),
    ("lessons/cs115/L28_cay_quyet_dinh.yaml",
     "Nếu để cây mọc sâu không phanh, nó sẽ tách vừa khít từng điểm nhiễu và rơi vào bẫy quá khớp ngay lập tức, nên ta phải cắt tỉa bằng độ sâu tối đa hay số mẫu tối thiểu ở lá.",
     "Nếu để cây mọc sâu không phanh, nó sẽ tách vừa khít từng điểm nhiễu và rơi vào bẫy quá khớp. Ta tránh bẫy này bằng độ sâu tối đa hay số mẫu tối thiểu ở lá."),
    ("lessons/cs115/L28_cay_quyet_dinh.yaml",
     "Một mẹo thực chiến quan trọng là dùng độ sâu nông từ ba đến năm tầng cho dữ liệu nhiễu hoặc ít mẫu, đồng thời theo dõi sai số ngoài túi trên phần mẫu không được bốc để tinh chỉnh rừng nhanh mà không cần tách thêm tập kiểm định riêng.",
     "Mẹo thực chiến hay là giữ cây nông từ ba đến năm tầng khi dữ liệu ít hoặc nhiều nhiễu. Hãy theo dõi thêm sai số ngoài túi trên phần mẫu không được bốc để tinh chỉnh rừng nhanh gọn."),
    ("lessons/cs115/L29_phan_cum.yaml",
     "Trị riêng thứ hai càng nhỏ, đồ thị càng gần đứt thành hai mảnh.",
     "Khi trị riêng thứ hai tiến về không, đồ thị gần như tách đứt thành hai mảnh riêng."),
    ("lessons/cs115/L30_gmm_em.yaml",
     "Các cột phía dưới cho thấy điểm càng nằm về bên trái thì phần cam càng lớn, còn ba điểm bên phải gần như toàn màu xanh.",
     "Các cột phía dưới cho thấy điểm nằm lệch hẳn về bên trái mang phần cam rất lớn, còn ba điểm bên phải gần như toàn màu xanh."),
    ("lessons/cs115/L31_nmf.yaml",
     "Khi ma trận đầu vào chỉ chứa số không âm như tần suất từ, lượng mua sắm hay cường độ sáng ảnh, ta xấp xỉ nó thành tích A nhân B với mọi phần tử đều lớn hơn hoặc bằng không.",
     "Với dữ liệu không âm như tần suất từ hay cường độ sáng ảnh, ta xấp xỉ ma trận gốc thành tích A nhân B. Mọi phần tử của cả hai ma trận thừa số đều giữ lớn hơn hoặc bằng không."),
    ("lessons/cs115/L31_nmf.yaml",
     "Hãy lưu ý nghiệm phân rã không duy nhất do luôn có thể nhân hai chiều bởi hai hệ số nghịch đảo nhau, và lời giải có thể dừng ở cực tiểu địa phương tuỳ ma trận khởi tạo ban đầu.",
     "Hãy lưu ý nghiệm phân rã không duy nhất vì luôn nhân hai ma trận bằng hai hệ số nghịch đảo nhau được. Lời giải còn phụ thuộc mạnh vào điểm khởi tạo ban đầu."),
    ("lessons/cs115/L31_nmf.yaml",
     "Trên thực tế khi phân tích hàng vạn tài liệu hoặc ma trận đánh giá thưa thớt, chọn hạng phân rã nhỏ vừa đủ giúp ép mô hình gom các từ đồng nghĩa thành từng chủ đề cô đọng dễ đặt tên.",
     "Khi phân tích hàng vạn tài liệu hoặc bảng đánh giá thưa, chọn hạng phân rã nhỏ giúp ép mô hình gom từ đồng nghĩa thành chủ đề cô đọng. Khi đó ta rất dễ đặt tên từng nhóm nội dung. Bạn cũng có thể chấm điểm mức đóng góp của từng từ khoá trên mỗi hàng để lọc ra năm tới mười từ đại diện rõ nhất cho từng chủ đề. Điều này biến kết quả toán học thành báo cáo phân tích rất dễ giải thích với người làm kinh doanh."),
    ("lessons/cs115/L32_tsne.yaml",
     "Để vẽ dữ liệu nhiều chiều lên mặt phẳng hai chiều mà không bị nén chụm ở tâm, phương pháp chuyển khoảng cách ở không gian gốc thành xác suất hàng xóm bằng hàm chuông rồi hiệu chỉnh bề rộng theo độ bối rối.",
     "Để vẽ dữ liệu nhiều chiều mà không bị nén ở tâm, phương pháp chuyển khoảng cách không gian gốc thành xác suất hàng xóm. Bề rộng hình chuông tại mỗi điểm được tự chỉnh theo độ bối rối đã chọn."),
    ("lessons/cs115/L32_tsne.yaml",
     "Thuật toán hạ gradient theo độ lệch KL bất đối xứng ưu tiên rất mạnh việc giữ gần những điểm vốn thân cận, trong khi chấp nhận buông lỏng vị trí tương đối giữa các cụm xa.",
     "Hạ gradient theo độ lệch KL bất đối xứng ưu tiên giữ rất sát những điểm vốn gần nhau. Đổi lại thuật toán buông lỏng vị trí tương đối giữa các cụm xa nhau."),
    ("lessons/cs115/L32_tsne.yaml",
     "Hãy luôn thử ít nhất hai hoặc ba giá trị độ bối rối cùng vài hạt giống khởi tạo khác nhau để chắc chắn nhóm cụm bạn thấy là cấu trúc thật chứ không phải ảo ảnh ngẫu nhiên của một lần tối ưu.",
     "Hãy luôn thử vài giá trị độ bối rối cùng nhiều hạt giống ngẫu nhiên khác nhau. Việc lặp như vậy giúp bạn phân biệt cấu trúc cụm thật với ảo ảnh ngẫu nhiên của một lần chạy. Khi thấy các nhóm chính xuất hiện ổn định qua nhiều cấu hình, bạn mới tự tin dùng bản vẽ hai chiều này để trình bày hay phát hiện điểm ngoại lai."),
    ("lessons/cs115/L34_cnn.yaml",
     "Về bản chất đại số, phép tích chập vẫn là phép nhân với một ma trận thưa dạng Toeplitz rất có cấu trúc, ghép xen kẽ lớp gộp cực đại hay gộp trung bình không chứa tham số để nén dần chiều rộng và mở rộng vùng nhìn.",
     "Về đại số, phép tích chập chính là phép nhân với ma trận thưa có cấu trúc lặp đều. Ta thường ghép xen kẽ lớp gộp không tham số để thu nhỏ ảnh dần và mở rộng vùng nhìn."),
    ("lessons/cs115/L34_cnn.yaml",
     "Khi ghép nhiều lớp liên tiếp trên ảnh màu ba kênh, chiều sâu bản đồ đặc trưng tăng dần trong khi kích thước không gian co nhỏ lại để gom toàn bộ nét cục bộ thành khái niệm toàn cảnh ở tầng phân loại cuối.",
     "Khi chồng nhiều lớp tích chập trên ảnh màu, số kênh đặc trưng tăng dần còn kích thước không gian co lại. Nhờ đó mạng gom dần nét cục bộ thành khái niệm toàn cảnh ở tầng phân loại cuối. Cách thiết kế theo tầng này vừa tiết kiệm tham số mạnh mẽ vừa giúp mô hình nhận ra vật thể ngay cả khi nó dịch vị trí vài điểm ảnh."),
    ("lessons/cs115/L35_rnn_lstm.yaml",
     "Cắt chuẩn gradient chận được tình trạng bùng nổ tức thời, còn kiến trúc ô nhớ có cổng bổ sung đường cộng song song được điều tiết bằng cổng quên và cổng vào để giữ tín hiệu qua nhiều trăm bước.",
     "Cắt chuẩn gradient chận được tình trạng bùng nổ độ dốc tức thời. Còn kiến trúc ô nhớ có cổng bổ sung đường cộng song song với cổng quên để giữ ký ức qua nhiều trăm bước."),
    ("lessons/cs115/L35_rnn_lstm.yaml",
     "Việc hiểu rõ cơ chế duỗi theo thời gian và nút thắt truyền tin tuần tự cũng lý giải vì sao kiến trúc chú ý song song ở bài 41 ra đời sau này lại nhanh chóng vượt qua mạng hồi tiếp trên các chuỗi văn bản dài hàng nghìn từ.",
     "Hiểu rõ nút thắt truyền tin tuần tự của mạng hồi tiếp giúp ta thấy giá trị của bước ngoặt tiếp theo. Kiến trúc chú ý song song ở bài 41 nhờ kết nối thẳng mọi vị trí đã vượt xa mạng hồi tiếp trên chuỗi văn bản hàng nghìn từ."),
    ("lessons/cs115/L36_boosting.yaml",
     "Khác rừng ngẫu nhiên trồng cây sâu song song, tăng cường nối từng cây nông và ở dữ liệu lớn càng cần kiểm định để tránh quá khớp.",
     "Khác rừng ngẫu nhiên trồng cây sâu song song, tăng cường nối từng cây nông và rất cần tập kiểm định riêng để tránh quá khớp."),
    ("lessons/cs115/L36_boosting.yaml",
     "Trái với rừng ngẫu nhiên trồng nhiều cây song song nhằm giảm dao động phương sai, nhóm thuật toán tăng cường ghép nhiều cây nông nối tiếp nhau nhằm giảm dần thiên lệch còn sót.",
     "Trái với rừng ngẫu nhiên trồng cây song song để giảm phương sai, tăng cường ghép nhiều cây nông nối tiếp để giảm thiên lệch."),
    ("lessons/cs115/L36_boosting.yaml",
     "Với AdaBoost, mô hình có sai số thấp được cấp trọng số biểu quyết cao hơn, đồng thời hệ thống tăng cân nặng cho các mẫu vừa bị đoán nhầm để mô hình kế tiếp tập trung sửa đúng chỗ đó.",
     "Với AdaBoost, mô hình ít lỗi được cấp trọng số biểu quyết cao hơn. Hệ thống cũng tăng cân nặng cho các mẫu vừa bị đoán nhầm để cây sau tập trung sửa đúng chỗ đó."),
    ("lessons/cs115/L36_boosting.yaml",
     "Tăng cường theo gradient nhìn vấn đề tổng quát hơn bằng cách coi mỗi cây mới như một bước hạ gradient trong không gian hàm số, trực tiếp khớp phần dư sai lệch mà tổng các cây trước còn để lại.",
     "Tăng cường theo gradient tổng quát hoá bài toán bằng cách xem mỗi cây mới như một bước hạ gradient theo hàm số. Cây mới khớp trực tiếp phần dư sai lệch còn sót lại."),
    ("lessons/cs115/L36_boosting.yaml",
     "Trên dữ liệu dạng bảng có kích thước vừa phải, các biến thể tăng cường gradient hiện đại thường cho độ chính xác vượt trội so với mạng nơ-ron nhiều lớp, miễn là bạn kiểm soát chặt chiều sâu từng cây con và số vòng lặp nối tiếp.",
     "Trên dữ liệu dạng bảng cỡ vừa, các biến thể tăng cường gradient hiện đại thường thắng mạng nơ-ron nhiều lớp. Bí quyết nằm ở việc giới hạn chiều sâu cây con và điều chỉnh tốc độ học kèm số vòng lặp. Nhờ từng bước sửa nhỏ có kiểm soát trên tập kiểm định, mô hình tổng hợp giữ được ranh giới phân loại sắc nét mà không học thuộc nhiễu ngẫu nhiên."),
    ("lessons/cs115/L37_autoencoder.yaml",
     "Cổ chai càng hẹp thì nén càng mạnh nhưng khôi phục càng mất mát.",
     "Khe cổ chai hẹp ép nén dữ liệu mạnh hơn nhưng cũng làm sai số khôi phục tăng theo."),
    ("lessons/cs115/L38_ica.yaml",
     "Vì bản chất trộn nhiều biến làm tín hiệu tổng ngày càng tiến sát phân phối chuẩn theo định lý giới hạn trung tâm, ta đảo ngược quá trình bằng cách tìm phép xoay sau bước làm trắng để các thành phần đầu ra có độ bất chuẩn lớn nhất đo bằng độ nhọn dư hay entropy.",
     "Bản chất trộn nhiều biến kéo tín hiệu tổng tiến gần phân phối chuẩn theo định lý giới hạn trung tâm. Do đó sau bước làm trắng, ta tìm phép xoay làm tăng độ bất chuẩn đo bằng độ nhọn dư hay entropy."),
    ("lessons/cs115/L39_hoc_tang_cuong.yaml",
     "Thuật toán Q-learning học không cần mô hình môi trường bằng cách nhích nhẹ bảng ước lượng về phía mục tiêu tạm thời, đồng thời luôn giữ tỉ lệ thăm dò hợp lý thay vì chỉ khai thác tham lam quá sớm.",
     "Thuật toán Q-learning học trực tiếp qua tương tác mà không cần biết trước xác suất chuyển trạng thái. Nó nhích dần bảng ước lượng về phía mục tiêu tạm thời và vẫn giữ tỉ lệ thăm dò hợp lý."),
    ("lessons/cs115/L40_umap.yaml",
     "Để vẽ dữ liệu hàng trăm nghìn hay hàng triệu điểm lên mặt phẳng mà không mất thời gian tính toàn bộ mọi cặp khoảng cách, thuật toán mở đầu bằng đồ thị k láng giềng gần nhất có chuẩn hoá khoảng cách theo từng vùng mật độ cục bộ.",
     "Để vẽ hàng triệu điểm mà không tính toàn bộ mọi cặp khoảng cách, thuật toán mở đầu bằng đồ thị k láng giềng gần nhất. Khoảng cách cạnh được chuẩn hoá riêng theo mật độ cục bộ quanh từng điểm."),
    ("lessons/cs115/L40_umap.yaml",
     "Cuối cùng hãy luôn giữ thái độ khoa học khi đọc biểu đồ thực nghiệm, kiểm tra độ ổn định qua nhiều hạt giống ngẫu nhiên và hiểu rõ tốc độ vượt trội quan sát được không tự động thành bất biến toán học cho khoảng cách giữa các cụm xa.",
     "Cuối cùng hãy luôn giữ thái độ khoa học khi đọc biểu đồ thực nghiệm. Hãy thử nhiều hạt giống ngẫu nhiên khác nhau và nhớ rằng tốc độ nhanh không đảm bảo tính đúng cho khoảng cách giữa các cụm xa."),
    ("lessons/cs115/L40_umap.yaml",
     "Từ mặt phẳng trực quan thu được, hãy luôn quay lại kiểm tra chỉ số lân cận trên chính dữ liệu gốc nhiều chiều trước khi ra quyết định phân nhóm khách hàng hay phân tích dữ liệu sinh học.",
     "Từ bản vẽ hai chiều thu được, hãy luôn đối chiếu lại cấu trúc lân cận trên dữ liệu gốc nhiều chiều trước khi ra kết luận. Kết hợp trực quan hoá nhanh cùng chỉ số định lượng sẽ giúp phân tích khách quan và chính xác hơn. Đặc biệt hãy thử đổi số láng giềng k từ mười lăm lên năm mươi để quan sát sự dịch chuyển giữa cấu trúc chi tiết nhỏ và toàn cảnh rộng. Nếu hai vùng giữ nguyên ranh giới phân tách qua nhiều mức k khác nhau, bạn mới có cơ sở vững chắc để báo cáo kết quả."),
    ("lessons/cs115/L41_attention.yaml",
     "Mỗi vị trí phát ra ba véc-tơ gồm truy vấn, khoá và giá trị để tính độ tương đồng bằng tích vô hướng rồi chia căn bậc hai số chiều khoá nhằm giữ phương sai ổn định bằng một trước khi chuẩn hoá mũ.",
     "Mỗi vị trí phát ra ba véc-tơ gồm truy vấn, khoá và giá trị để tính điểm tương đồng. Phép chia căn bậc hai số chiều khoá giữ phương sai ổn định bằng một trước khi chuẩn hoá mũ."),
    ("lessons/cs115/L41_attention.yaml",
     "Đừng quên hai mảnh ghép bắt buộc đi kèm là mã hoá vị trí vì bản chất phép chú ý đối xứng thứ tự, và chi phí bộ nhớ tăng bậc hai theo độ dài chuỗi khiến chuỗi siêu dài cần cửa sổ thưa hoặc bộ nhớ đệm khoá giá trị.",
     "Đừng quên hai mảnh ghép bắt buộc đi kèm là mã hoá vị trí và kiểm soát chi phí bộ nhớ bậc hai. Chuỗi siêu dài thường cần thêm cửa sổ thưa hoặc bộ nhớ đệm khoá giá trị để chạy vừa trên phần cứng thật."),
    ("lessons/cs115/L42_vae_gan.yaml",
     "Muốn chuyển từ nén dữ liệu sang sinh mẫu hoàn toàn mới, mạng tự mã hoá biến phân biến mã ẩn thành một phân phối chuẩn có trung bình và độ lệch chuẩn riêng rồi tối đa hoá cận dưới biến phân gồm độ chính xác tái tạo trừ độ lệch KL giữ không gian ẩn gần phân phối chuẩn tắc.",
     "Mạng tự mã hoá biến phân không nén thành một điểm cứng mà biến mã ẩn thành một phân phối chuẩn. Nó tối đa hoá cận dưới biến phân gồm độ chính xác tái tạo trừ độ lệch KL giữ mã ẩn gần phân phối chuẩn tắc."),
    ("lessons/cs115/L42_vae_gan.yaml",
     "Sang nửa kia, mạng đối kháng đặt hai mạng sinh và phân biệt vào một trò chơi tổng bằng không mà cân bằng Nash đạt tại xác suất phân biệt một phần hai cho cả dữ liệu thật lẫn dữ liệu giả.",
     "Sang nửa kia, mạng đối kháng đặt mạng sinh và bộ phân biệt vào một trò chơi đối kháng hai bên. Điểm cân bằng Nash đạt tại xác suất phân biệt một phần hai cho cả dữ liệu thật lẫn dữ liệu giả."),
    ("lessons/cs115/L43_diffusion.yaml",
     "Ở chiều thuận, ta trộn dần nhiễu chuẩn theo một lịch phương sai sao cho tổng bình phương hai hệ số luôn bằng một để phân phối cuối tiến hẳn về nhiễu chuẩn tắc thuần khiết.",
     "Ở chiều thuận, ta trộn dần nhiễu chuẩn theo một lịch phương sai định trước. Tổng bình phương hai hệ số luôn bằng một giúp phân phối cuối tiến về nhiễu chuẩn tắc thuần khiết."),
    ("lessons/cs115/L43_diffusion.yaml",
     "Điểm kỳ diệu về giải tích của phân phối chuẩn là cho phép gộp toàn bộ T bước thành một công thức đóng tính thẳng mẫu nhiễu ở bước t bất kỳ chỉ từ ảnh gốc và một véc-tơ nhiễu đơn.",
     "Tính chất giải tích đẹp của phân phối chuẩn cho phép gộp cả chuỗi T bước thành một công thức đóng gọn. Ta tính thẳng mẫu ở bước t bất kỳ chỉ từ ảnh gốc và một véc-tơ nhiễu đơn."),
    ("lessons/cs115/L43_diffusion.yaml",
     "Lúc huấn luyện mạng chỉ cần dự đoán đúng lượng nhiễu đã pha theo sai số bình phương trung bình rồi tới lúc sinh ảnh mới lặp ngược từng bước bóc nhiễu dần cho tới khi đường nét ảnh sắc sảo hiện hình trở lại.",
     "Lúc huấn luyện, mạng học dự đoán lượng nhiễu vừa pha theo sai số bình phương trung bình. Khi sinh ảnh mới, ta lặp ngược từ nhiễu thuần và bóc dần từng lớp để ảnh sắc nét hiện ra."),
    ("lessons/cs115/L43_diffusion.yaml",
     "Ngoài sinh ảnh nghệ thuật, khung mô hình khuếch tán thêm và khử nhiễu này còn mở rộng rất mạnh sang thiết kế phân tử thuốc mới, tạo âm thanh độ phân giải cao và mô phỏng chuỗi chuyển động ba chiều chân thực.",
     "Ngoài sinh ảnh, khung mô hình khuếch tán còn ứng dụng mạnh trong thiết kế phân tử thuốc mới và tổng hợp âm thanh chân thực. Nhiều thuật toán rút gọn lịch lấy mẫu ngày nay đã giảm từ một nghìn bước xuống còn hai mươi bước mà vẫn giữ ảnh rõ nét. Hiểu chắc chuỗi chuyển tiếp chiều thuận lẫn chiều nghịch hôm nay cho bạn chìa khoá bước vào mọi kiến trúc sinh dữ liệu hiện đại."),
]

for rel, old, new in PATCHES:
    rep(rel, old, new)

bad = []
for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
            for s in sents:
                if len(s) > 170:
                    bad.append(f"{lid}:{sc['id']}#{idx} len={len(s)} >170: {s}")
                if len(s.split()) > 38:
                    bad.append(f"{lid}:{sc['id']}#{idx} words={len(s.split())} >38: {s}")
                if "càng " in s.lower():
                    bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s):
                    bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    if w < 1645:
        bad.append(f"{lid} words={w} < 1645")
    else:
        print(f"OK {lid}: words={w}", flush=True)

for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} violations"
print("ALL 22 CS115 STAGE 9 LESSONS CLEAN & >= 1645w!", flush=True)
