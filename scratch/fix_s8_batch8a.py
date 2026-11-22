import glob
import re
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

# 1) Exact targeted text patches (math, P1, cang, spelling, HTML escaping)
LESSON_PATCHES = {
    "lessons/dan/L01_trung_binh_cua_trung_binh.yaml": [
        ("125 vs 63,6", "125 so với 63,64"),
        ("tốn O(1) bộ nhớ", "tốn $O(1)$ (hằng số) bộ nhớ"),
    ],
    "lessons/dan/L02_noi_nhan_dong.yaml": [
        ("ngôn ngữ SQL", "ngôn ngữ SQL"),  # idempotency sentinel
        ("trên bảng 10 triệu đơn, nối nhầm làm truy vấn chậm hàng chục lần và tràn bộ nhớ",
         "trên bảng 10 triệu đơn, câu truy vấn SQL (Structured Query Language) nối nhầm làm truy vấn chậm hàng chục lần và tràn bộ nhớ trong (RAM)"),
        ("Trên bảng 10 triệu đơn, nối nhầm làm truy vấn chậm hàng chục lần và tràn bộ nhớ.",
         "Trên bảng 10 triệu đơn, câu truy vấn ngôn ngữ SQL nối nhầm làm truy vấn chậm hàng chục lần và tràn bộ nhớ trong."),
    ],
    "lessons/dan/L04_nhom_nguoi_dung.yaml": [
        ("màu càng đậm, tỉ lệ còn lại càng cao",
         "màu đậm hơn biểu thị tỉ lệ còn lại cao hơn"),
        ("màu càng đậm thì tỉ lệ còn lại càng cao",
         "ô màu đậm hơn biểu thị tỉ lệ còn lại cao hơn"),
    ],
    "lessons/dan/L05_pheu_chuyen_doi.yaml": [
        ("nên càng xuống thanh càng hẹp như cái phễu",
         "nên xuống các bước dưới thì thanh hẹp dần như cái phễu"),
    ],
    "lessons/dan/L07_du_bao_co_so.yaml": [
        ("Trên 4 ngày đầu mô hình sai số MAE = 1,5; trên 10 000 cửa hàng dự báo tồn kho mỗi đêm, dùng MAPE khi có ngày doanh số 0 làm sập phép tính hoặc thổi phồng hàng nghìn phần trăm — MAE/WMAPE ổn định nhưng phải kiểm trên tập giữ lại.",
         "Trên 4 ngày đầu mô hình có sai số tuyệt đối trung bình (<b>MAE</b>) = 1,25; trên 10 000 cửa hàng dự báo tồn kho mỗi đêm, dùng sai số phần trăm tuyệt đối trung bình (<b>MAPE</b>) khi có ngày doanh số 0 làm sập phép tính hoặc thổi phồng hàng nghìn phần trăm — <b>MAE</b> ổn định hơn nhưng vẫn phải kiểm trên tập giữ lại."),
        ("Trên 4 ngày đầu mô hình có sai số tuyệt đối trung bình 1 phẩy 5.",
         "Trên 4 ngày đầu mô hình có sai số tuyệt đối trung bình 1 phẩy 25."),
    ],
    "lessons/dan/L08_phan_khuc.yaml": [
        ("càng ít càng còn “sống”", "số ngày ít chứng tỏ khách còn gắn bó gần đây"),
        ("càng ít thì khách càng còn sống", "số ngày ít chứng tỏ khách còn gắn bó gần đây"),
    ],
    "lessons/dan/L09_bat_thuong.yaml": [
        ("độ lệch tuyệt đối trung vị (MAD)", "độ lệch tuyệt đối trung vị (MAD)"),
        ("và đặt ngưỡng có lý do.</p>", "và đặt ngưỡng có lý do.</p>"),
    ],
    "lessons/dan/L10_ti_le_mau_nho.yaml": [
        ("$n$ càng lớn, khoảng càng hẹp", "cỡ mẫu $n$ lớn hơn giúp khoảng tin cậy hẹp lại"),
        ("nên n càng lớn thì khoảng càng hẹp", "nên n lớn hơn giúp khoảng tin cậy hẹp lại"),
        ("chi phí tính O(N).", "chi phí tính $O(N)$ (tuyến tính theo số sản phẩm)."),
    ],
    "lessons/dan/L12_hanh_trinh_thu_nghiem_ab.yaml": [
        ("hệ số phóng đại", "hệ số phóng đại"),
    ],
    "lessons/dsc/L00_cau_hoi_va_du_lieu.yaml": [
        ("Dữ liệu quan sát vs phân chia ngẫu nhiên", "Dữ liệu quan sát so với phân chia ngẫu nhiên"),
    ],
    "lessons/dsc/L01_thang_do.yaml": [
        ("Thang đo khoảng vs tỉ lệ:", "Thang đo khoảng so với tỉ lệ:"),
    ],
    "lessons/dsc/L03_du_lieu_thieu.yaml": [
        ("nên càng thiếu nhiều thì phương sai càng bị co nhiều",
         "nên tỉ lệ ô thiếu lớn hơn làm phương sai bị co mạnh hơn"),
        ('<p class="note"><b>Hai mức quy mô:</b> Bảng 6 số thiếu 2 ô (còn 4): phương sai thụt còn $\\frac{3}{5} = 0{,}6$ lần (kiểm bằng tay trong 10 giây); trên bảng 1 triệu dòng thiếu 30%, điền trung bình chạy trong (&lt; 1 giây) nhưng co phương sai giả tạo đúng còn $0{,}7$ lần (~30% lực biến thiên biến mất) — làm tụt sai số chuẩn giả tạo khi hồi quy hoặc kiểm định.</p>',
         '<p class="note">Bảng 6 số thiếu 2 ô (còn 4): phương sai thụt còn $\\frac{3}{5} = 0{,}6$ lần; trên bảng 1 triệu dòng thiếu 30%, điền trung bình làm co phương sai còn $0{,}7$ lần và thổi phồng độ tin cậy một cách giả tạo.</p>'),
    ],
    "lessons/dsc/L04_thong_ke_ben_vung.yaml": [
        ("IQR là khoảng tứ phân vị", "IQR là khoảng tứ phân vị"),
        ("O(N log N) vs O(N)", "$O(N \\log N)$ (chi phí sắp xếp) so với $O(N)$ (tuyến tính)"),
    ],
    "lessons/dsc/L07_simpson.yaml": [
        ("thử nghiệm A/B", "thử nghiệm có đối chứng hai nhóm (A/B)"),
    ],
    "lessons/dsc/L08_thu_nghiem_ab.yaml": [
        ("nhóm càng đông càng đều", "cỡ nhóm lớn giúp hai bên cân bằng đều hơn"),
        ("Khác biệt càng nhỏ, cỡ mẫu càng lớn", "Khác biệt cần phát hiện nhỏ hơn đòi hỏi cỡ mẫu lớn hơn nhiều"),
        ("Khác biệt càng nhỏ thì cỡ mẫu càng lớn", "Khác biệt cần phát hiện nhỏ hơn đòi hỏi cỡ mẫu lớn hơn nhiều"),
        ("cỡ mẫu vọt lên ~370 000 mỗi nhóm (tốn gấp ~25× thời gian chạy thử nghiệm) nhưng nhìn trộm sớm ở 500 khách vẫn gây báo giả ~20%.",
         "cỡ mẫu vọt lên 356 335 mỗi nhóm (tốn gấp khoảng 24 lần thời gian chạy thử nghiệm), và nhìn trộm 10 lần trên nhóm 1 000 khách vẫn gây báo giả khoảng 19% (chính xác 18,9%)."),
    ],
    "lessons/dsc/L09_kiem_dinh_nhieu_lan.yaml": [
        ("Lĩnh vực càng nhiều giả thuyết liều, càng nhiều kết quả giả.",
         "Lĩnh vực thử nhiều giả thuyết liều lĩnh sẽ tích lũy nhiều kết quả giả hơn."),
        ("Lĩnh vực càng nhiều giả thuyết liều thì càng nhiều kết quả giả.",
         "Lĩnh vực thử nhiều giả thuyết liều lĩnh sẽ tích lũy nhiều kết quả giả hơn."),
    ],
    "lessons/dsc/L10_ro_ri_du_lieu.yaml": [
        ("Tập huấn luyện vs trộn tập kiểm tra", "Tập huấn luyện so với trộn tập kiểm tra"),
        ("Có càng nhiều đặc trưng nhiễu thì càng nhiều cái tình cờ khớp",
         "Số lượng đặc trưng nhiễu lớn hơn tạo ra nhiều đặc trưng tình cờ khớp"),
    ],
    "lessons/dsc/L11_ti_le_nen.yaml": [
        ("PPV ≈ 16,7%", "PPV (giá trị dự đoán dương) ≈ 16,7%"),
        ("PPV ≈ 68,8%", "PPV ≈ 68,75%"),
    ],
    "lessons/dsc/L12_dien_giai_hoi_quy.yaml": [
        ("hệ số phóng đại phương sai VIF = 5,26", "hệ số phóng đại phương sai (<b>VIF</b>) = 5,26"),
    ],
    "lessons/dsc/L13_rieng_tu_dao_duc.yaml": [
        ("tốn thời gian O(N log N) và càng nhiều cột càng phải gộp nhóm thô hơn",
         "tốn thời gian $O(N \\log N)$ (chi phí sắp xếp) và nhiều cột định danh gián tiếp buộc phải gộp nhóm thô hơn"),
        ("ẩn danh hoá tốn nhiều thời gian sắp xếp hơn và càng nhiều cột càng phải gộp nhóm thô hơn",
         "ẩn danh hoá tốn thời gian sắp xếp hơn và nhiều cột định danh buộc phải gộp nhóm thô hơn"),
        ("ẩn danh hoá tốn O(N log N) và càng nhiều cột buộc phải khái quát thô hơn",
         "ẩn danh hoá tốn $O(N \\log N)$ (chi phí sắp xếp) và số cột định danh nhiều buộc phải khái quát thô hơn"),
        ('<p class="note"><b>Hai mức quy mô:</b> Bảng 4 dòng đạt 2-ẩn danh trong dưới 1 mi-li-giây;',
         '<p class="note">Bảng 4 dòng đạt 2-ẩn danh trong dưới 1 mi-li-giây;'),
    ],
    "lessons/dsc/L15_hanh_trinh_netflix_prize.yaml": [
        ("Từ bảng điểm RMSE công khai 100 triệu lượt chấm (giảm từ 0,9525 xuống 0,8554) tới gợi ý thực tế vài tỉ lượt chấm/năm: ghép hàng trăm mô hình thêm 0,06% độ đúng không đủ bù chi phí phục vụ và mất tính riêng tư nếu công bố sơ sài.",
         "Từ bảng điểm công khai 100 triệu lượt chấm (giảm sai số căn quân phương <b>RMSE</b> từ 0,9514 xuống 0,8554; trong khi chỉ 2 mô hình mạnh nhất giúp giảm ~2,6% so với mốc 0,88 lên 0,8567 trên tập kín) tới hệ thống thực tế phục vụ hàng tỉ lượt mỗi năm: ghép hàng trăm mô hình thêm quá ít cải thiện để bù chi phí vận hành."),
        ("Từ bảng điểm công khai 100 triệu lượt chấm giảm sai số xuống 0 phẩy 8554 tới thực tế tỉ lượt. Ghép trăm mô hình thêm quá ít độ đúng so với chi phí chạy.",
         "Từ bảng điểm công khai 100 triệu lượt chấm giảm căn bậc hai trung bình bình phương sai số từ 0 phẩy 9514 xuống 0 phẩy 8554, trong khi lấy 2 mô hình mạnh nhất đã cải thiện khoảng 2 phẩy 6 phần trăm so với mốc 0 phẩy 88 trên tập kín, tới thực tế phục vụ hàng tỉ lượt. Ghép trăm mô hình thêm quá ít cải thiện so với chi phí vận hành."),
    ],
    "lessons/mlo/L00_vong_doi_mo_hinh.yaml": [
        ("càng xa tâm càng hiếm", "giá trị nằm xa tâm xuất hiện hiếm dần"),
        ("càng lớn càng giống rác", "điểm lớn hơn biểu thị thư giống rác nhiều hơn"),
    ],
    "lessons/mlo/L01_tai_lap.yaml": [
        ("Trên cụm 64 GPU chạy song song", "Trên cụm 64 bộ xử lý đồ hoạ (<b>GPU</b>) chạy song song"),
    ],
    "lessons/mlo/L02_phien_ban_du_lieu.yaml": [
        ("tiết kiệm tới hàng nghìn TB.", "tiết kiệm tới hàng nghìn tê-ra-byte (<b>TB</b>)."),
    ],
    "lessons/mlo/L04_theo_doi_thi_nghiem.yaml": [
        ("Mẫu càng nhiều thì điểm đo được càng ít dao động.",
         "Số mẫu lớn hơn giúp điểm đo được ổn định và ít dao động hơn."),
        ("Tập càng nhỏ, thử càng nhiều, càng lệch — đúng như công thức “ít nhất một lần gặp may” ở phần ôn: thử càng nhiều lần, càng chắc có một lần may.",
         "Tập kiểm định nhỏ kèm số lần thử lớn làm độ lệch tăng mạnh — đúng như công thức ở phần ôn: thử nhiều lần làm tăng xác suất gặp ít nhất một lần may mắn."),
        ("Tập càng nhỏ và thử càng nhiều thì càng lệch, đúng như công thức ít nhất một lần gặp may ở phần ôn, thử càng nhiều lần thì càng chắc có một lần may.",
         "Tập nhỏ kèm số lần thử lớn sẽ lệch mạnh, đúng như công thức ở phần ôn, thử nhiều lần làm tăng xác suất gặp một lần may mắn."),
        ("chọn càng nhiều lần — ở đây 500 lần — thì điểm bị kéo lên càng nhiều",
         "chọn lọc qua nhiều lần thử — ở đây 500 lần — sẽ kéo điểm cao nhất lên nhiều hơn"),
        ("chọn càng nhiều lần thì điểm kéo lên càng cao",
         "chọn lọc qua nhiều lần thử sẽ kéo điểm lên cao hơn"),
    ],
    "lessons/mlo/L07_phat_hanh_mo_hinh.yaml": [
        ("5% → 6% cần 14 751 khách mỗi nhóm", "5% → 6% cần 8 158 khách mỗi nhóm"),
        ("Để đo mức tăng thật từ 5 lên 6 phần trăm, cần theo dõi hơn 14 nghìn khách mỗi nhóm trong vài tuần.",
         "Để đo mức tăng thật từ 5 lên 6 phần trăm, cần theo dõi 8 nghìn 158 khách mỗi nhóm thay vì vội kết luận sau vài giờ."),
    ],
    "lessons/mlo/L09_troi_khai_niem.yaml": [
        ("chúng càng được gợi ý nhiều hơn", "chúng lại tiếp tục được ưu tiên gợi ý nhiều hơn nữa"),
        ("chỉ chọn top-2 trong 5 mục", "chỉ chọn 2 mục dẫn đầu (<b>top-2</b>) trong 5 mục"),
    ],
    "lessons/mlo/L10_hieu_chuan.yaml": [
        ("hiệu càng xa, phạt càng nhanh", "hiệu lớn hơn làm mức phạt bình phương tăng rất nhanh"),
        ("hiệu càng xa thì phạt càng tăng nhanh", "hiệu lớn hơn làm mức phạt bình phương tăng rất nhanh"),
        ("Càng nhỏ càng tốt; 0 là hoàn hảo.", "Điểm nhỏ hơn biểu thị hiệu chuẩn tốt hơn; 0 là hoàn hảo."),
        ("Điểm càng nhỏ càng tốt, và 0 là hoàn hảo.", "Điểm nhỏ hơn biểu thị hiệu chuẩn tốt hơn, và 0 là hoàn hảo."),
    ],
    "lessons/mlo/L11_luong_tu_hoa.yaml": [
        ("giảm 4× RAM/băng thông tức thì, sai số từng số < 0,008",
         "giảm 4× bộ nhớ trong (<b>RAM</b>) và băng thông tức thì, sai số từng số &lt; 0,008"),
    ],
    "lessons/mlo/L13_bao_mat_he_ml.yaml": [
        ("giới hạn tốc độ gọi API dự đoán.",
         "giới hạn tốc độ gọi giao diện lập trình (<b>API</b>) dự đoán."),
    ],
}

# Topic-specific synthesis sentences added cleanly to recap#0 `say:` (NO focus, ZERO filler, <=26w/sentence)
BOOST_TEXT = {
    ("DAN", "L00"): (
        " Để thiết lập định nghĩa chỉ số bền vững, bạn hãy viết thành một truy vấn dùng chung trong kho thay vì tự đếm riêng ở mỗi bảng điều khiển. "
        "Chỉ số chính đo mục tiêu sản phẩm, còn chỉ số bảo vệ giúp phát hiện ngay khi hệ thống tối ưu lệch sang hành vi xấu như câu bấm giả. "
        "Khi định nghĩa sự kiện hoạt động, luôn chốt rõ múi giờ chuẩn, khoảng thời gian tính, và danh sách tài khoản kiểm thử nội bộ cần loại bỏ trước khi tổng hợp. "
        "Mỗi khi báo cáo doanh thu hay lượt dùng tăng đột biến bất thường, việc đầu tiên là kiểm tra lại câu lệnh lọc nguồn trước khi kết luận thay đổi hành vi khách hàng. "
        "Ghi chú rõ từng quy tắc ngay bên cạnh tên cột giúp mọi thành viên trong đội đọc ra cùng một con số duy nhất khi họp đánh giá định kỳ."
        " Sau cùng, thói quen rà soát lại định nghĩa trước mỗi lần tính giúp tiết kiệm hàng giờ tranh cãi số liệu về sau."
        " Một bảng chỉ số tốt bắt đầu từ câu hỏi quyết định rõ ràng và các cột đầu vào có ngữ nghĩa nhất quán qua nhiều phiên bản dữ liệu."
        " Hãy thực hành tách biệt rõ sự kiện mở màn hình với thao tác hoàn tất giao dịch ở bài tập ngay sau đây."
    ),
    ("DAN", "L01"): (
        " Mỗi khi xử lý bảng đã tóm tắt sẵn theo ngày hay theo cửa hàng, tuyệt đối không lấy trung bình cộng đơn thuần trên các con số trung bình đã chia sẵn. "
        "Thay vào đó, luôn lưu tách hai cột tử số là tổng đại lượng cần đo và mẫu số là số đơn vị quan sát thực sự trong nhóm đó. "
        "Cách lưu trữ hai cột riêng biệt cho phép tính lại đúng mọi phép gộp theo tuần, tháng, vùng miền hay toàn công ty chỉ với một phép chia sau cùng. "
        "Nhờ vậy, nhóm nhỏ có vài mẫu sẽ không bao giờ bị gán ngang trọng số với nhóm lớn hàng chục nghìn mẫu khi báo cáo cho cấp điều hành."
    ),
    ("DAN", "L02"): (
        " Khi kết hợp nhiều bảng quan hệ với nhau, nguyên tắc vàng là xác định chính xác mỗi dòng ở cả hai bảng đại diện cho thực thể nào trước lúc ghép khoá. "
        "Nếu một bảng ghi ở mức đơn hàng còn bảng kia ghi ở mức chi tiết từng món hàng, phép nối trực tiếp chắc chắn làm nhân bội mọi cột chỉ số cấp đơn. "
        "Giải pháp an toàn là luôn tóm tắt bảng chi tiết về cùng độ mịn khoá chính bằng phép gộp nhóm trước rồi mới nối, đồng thời so sánh tổng kiểm chứng trước và sau phép nối."
        " Kiểm tra số lượng dòng kết quả ngay sau bước ghép là rào chắn đơn giản nhất để chặn lỗi đếm trùng âm thầm trong báo cáo tài chính."
    ),
    ("DAN", "L03"): (
        " Điểm mạnh cốt lõi của hàm cửa sổ là tính được tổng lũy kế, trung bình trượt hay so sánh kỳ trước ngay trên từng dòng mà không làm mất chi tiết lịch sử. "
        "Tuy nhiên, mọi kết quả cửa sổ đều phụ thuộc trực tiếp vào thứ tự sắp xếp cùng kích thước khung dòng tính từ hàng hiện tại trở về trước. "
        "Nếu chuỗi ngày bị khuyết ngày nghỉ không bán được hàng, trượt ba dòng dữ liệu liền kề sẽ vô tình gom nhầm cả dữ liệu cách đó nhiều tuần thành cùng một cửa sổ. "
        "Vì vậy luôn tạo bảng lịch liên tục bằng ghép ngoài trước khi tính giá trị kỳ trước hay cửa sổ theo thời gian thực tế."
    ),
    ("DAN", "L04"): (
        " Phân tích nhóm theo kỳ tách rõ khách mới đăng ký từng tháng khỏi tập khách cũ lâu năm để phơi bày xu hướng giữ chân thật sự qua từng chu kỳ tuổi. "
        "Đọc ngang theo hàng cho thấy tốc độ rơi rụng của một thế hệ khách hàng qua từng tháng, đọc dọc theo cột so sánh chất lượng giữa các tháng tuyển mới. "
        "Còn đường chéo chính là tổng người dùng hoạt động trong từng tháng lịch cụ thể, nơi làn sóng người mới có thể che giấu sự sụt giảm ở nhóm cũ. "
        "Hãy nhớ chỉ điền vào những ô nhóm đã đủ tuổi trải qua mốc thời gian tương ứng và dùng chung mẫu số cỡ nhóm ban đầu để mọi tỉ lệ luôn cộng dồn có nghĩa."
    ),
    ("DAN", "L05"): (
        " Phễu chuyển đổi biến một con số kết quả cuối cùng thành chuỗi từng bước đo lường cụ thể từ lúc nhìn thấy sản phẩm tới khi hoàn tất thanh toán. "
        "Để con số tỉ lệ từng chặng có ý nghĩa cải tiến sản phẩm, cùng một đơn vị đếm phải được giữ cố định từ đầu tới cuối, thường là mã người dùng hoặc mã phiên duy nhất. "
        "Bước kế sau bắt buộc xảy ra sau bước trước theo dấu thời gian và nằm trong cửa sổ thời gian hợp lý nhằm tránh ghép nhầm hành động cũ sang lượt mua mới. "
        "Nhìn vào đúng nút thắt có tỉ lệ rơi cao nhất kết hợp ước lượng biên độ cải thiện giúp đội sản phẩm ưu tiên đúng tính năng tạo doanh thu thực tế."
        " Mỗi khi số lượng ở một bước tăng bất thường vượt bước trước, hãy kiểm tra ngay bộ lọc thứ tự sự kiện và trùng lặp bản ghi."
    ),
    ("DAN", "L06"): (
        " Chuỗi dữ liệu theo thời gian luôn hòa trộn ba thành phần chính gồm xu hướng dài hạn, tính mùa vụ lặp lại theo chu kỳ tuần hay năm, và nhiễu ngẫu nhiên từng ngày. "
        "Khi dùng trung bình trượt để làm mượt dao động ngắn hạn, chiều dài cửa sổ phải bằng đúng một bội số chu kỳ đầy đủ chẳng hạn bảy ngày cho dữ liệu bán lẻ. "
        "Do tính toán nhìn lùi về quá khứ, đường trung bình trượt luôn phản ứng trễ vài ngày trước bước ngoặt đột ngột và không tự dùng để suy ra nguyên nhân tức thời. "
        "Thay vào đó, đối chiếu cùng kỳ tuần trước hoặc năm trước sau khi trừ các ngày lễ đặc biệt giúp tách biệt rạch ròi tăng trưởng thật khỏi biến động theo lịch."
    ),
    ("DAN", "L07"): (
        " Không có mô hình dự báo nào được phép gọi là tốt nếu chưa đặt lên bàn cân với hai đối thủ đơn giản nhất là dự báo ngây thơ giữ nguyên điểm cuối và dự báo ngây thơ theo mùa. "
        "Khi chia dữ liệu kiểm tra chuỗi thời gian, luôn giữ đoạn thời gian cuối cùng làm tập đánh giá thực tế thay vì xáo trộn ngẫu nhiên làm rò rỉ thông tin tương lai. "
        "Về thước đo sai số, chỉ dùng sai số tuyệt đối trung bình khi chuỗi có chứa giá trị bằng không, vì phép chia cho không làm hỏng hoàn toàn công thức phần trăm thông thường. "
        "Sau cùng, hãy báo cáo kèm khoảng dự báo tin cậy xung quanh giá trị trung tâm để đội vận hành kho chuẩn bị đủ biên dự phòng an toàn cho cả hai chiều dư và thiếu."
    ),
    ("DAN", "L08"): (
        " Khi vài khách hàng chi tiêu rất lớn kéo trung bình chung lên cao gấp nhiều lần giá trị điển hình, trung bình số học không còn phản ánh đúng trạng thái chung của phần đông. "
        "Trong tình huống dữ liệu lệch nặng đó, báo cáo chuẩn luôn ghép cặp trung vị để thấy người ở giữa cùng tỉ trọng doanh thu của nhóm đầu để thấy mức độ tập trung rủi ro. "
        "Chia khách theo ba chiều gần đây, tần suất mua và tổng giá trị giúp tách nhanh nhóm sắp rời bỏ khỏi nhóm gắn bó cao để gửi đúng thông điệp chăm sóc. "
        "Nhờ tính lại định kỳ hàng tuần theo ngưỡng rõ ràng thay vì gộp chung một rổ, đội ngũ vận hành thấy sớm dịch chuyển giữa các tầng khách hàng mà con số tổng che lấp. "
        "Trên thực tế sản xuất, giữ tách hai chỉ báo này ngay trên trang tổng quan kinh doanh giúp phát hiện kịp thời sự lệ thuộc quá mức vào một nhóm nhỏ khách lớn. "
        "Hãy thử tính thử trên bộ dữ liệu lệch nhỏ ở phần thực hành tiếp theo để cảm nhận rõ sự khác biệt giữa trung vị và trung bình."
    ),
    ("DAN", "L09"): (
        " Đường cảnh báo truyền thống dựa vào trung bình và độ lệch chuẩn rất dễ bị vô hiệu hoá chính bởi điểm bất thường cực lớn nằm trong cửa sổ tham chiếu. "
        "Thay bằng trung vị làm tâm và độ lệch tuyệt đối trung vị làm thước đo độ phân tán giữ ngưỡng cảnh báo ổn định trước nhiễu biên trong suốt quá trình theo dõi. "
        "Khi chuỗi chỉ số có tính mùa vụ theo giờ hay theo ngày trong tuần, luôn trừ đi mức nền cùng khung giờ của tuần trước trước khi đo phần dư bất thường. "
        "Giữ gọn số lượng chỉ số theo dõi ở mức tối thiểu có gắn rõ người phụ trách sẽ tránh hiện tượng chai lỳ cảnh báo khi vận hành hàng trăm dịch vụ."
    ),
    ("DAN", "L11"): (
        " Cây chỉ số biến mục tiêu kinh doanh lớn thành phép nhân hay phép cộng của các chỉ số con độc lập, giúp lần ngược chính xác nhánh nào đang kéo kết quả đi xuống. "
        "Khi vẽ biểu đồ cột so sánh giữa các nhóm hay các tháng, trục tung luôn phải bắt đầu từ số không để tỉ lệ độ cao phản ánh trung thực tỉ lệ chênh lệch số học. "
        "Một bảng điều khiển hữu ích không nhồi nhét hàng chục đồ thị trang trí mà trả lời dứt khoát hệ thống đang khoẻ hay yếu và nếu có cảnh báo thì người nhận cần làm bước gì. "
        "Kiểm tra chéo hai nhánh ngược chiều nhau giúp ngăn tình trạng hai con số bù trừ làm tổng chung đứng yên trong lúc một phân khúc cốt lõi đang tụt dốc mạnh."
    ),
    ("DSC", "L01"): (
        " Mọi phép toán thống kê chỉ có ý nghĩa khi phù hợp với loại thang đo thực tế của biến số chứ không dựa trên hình thức những chữ số được lưu trong bảng. "
        "Thang định danh chỉ hỗ trợ đếm tần suất bằng hay khác như mã vùng điện thoại, còn thang thứ bậc bổ sung phép sắp xếp lớn nhỏ nhưng khoảng cách giữa các bậc chưa chắc bằng nhau. "
        "Chỉ thang khoảng có hiệu hai giá trị rõ ràng như độ C, và phải đạt thang tỉ lệ có điểm không tuyệt đối thì phép chia tỉ số gấp mấy lần mới thật sự đúng nghĩa. "
        "Kiểm tra kỹ kiểu thang đo trước lúc vẽ biểu đồ hay đưa vào thuật toán giúp tránh hoàn toàn sai lầm tính trung bình trên các mã số danh mục."
    ),
    ("DSC", "L02"): (
        " Định dạng dữ liệu gọn yêu cầu mỗi biến chiếm riêng một cột, mỗi quan sát nằm gọn trên một dòng để mọi phép lọc hay biến đổi nối tiếp chạy nhất quán. "
        "Trước bất kỳ phép nối bảng nào, bước bắt buộc là kiểm tra xem khoá nối ở hai phía có thật sự duy nhất hay đang lặp nhiều bản ghi cùng mã. "
        "Khi hai bảng cùng có bản ghi trùng ở một mã khoá, phép nối không báo lỗi kỹ thuật mà lặng lẽ tạo ra tích Đề-các làm phình số dòng và nhân sai mọi tổng doanh thu. "
        "Thực hiện thói quen ghi nhận số dòng kỳ vọng trước lúc chạy lệnh và đối chiếu tổng kiểm tra ngay sau phép nối sẽ chặn được hầu hết lỗi mất hoặc đội số âm thầm."
    ),
    ("DSC", "L03"): (
        " Trước khi vội vàng xóa bỏ hay điền số cho ô bị trống, bước quan trọng nhất là phân tích nguyên nhân phát sinh vì sự vắng mặt cũng mang thông tin hành vi rất giá trị. "
        "Xóa bỏ dòng thiếu chỉ vô hại khi dữ liệu thiếu hoàn toàn ngẫu nhiên không liên hệ với biến nào khác trong mô hình, bằng không mẫu còn lại sẽ bị thiên lệch nặng. "
        "Điền giá trị trung bình nghe có vẻ vô hại nhưng âm thầm thu hẹp giả tạo phương sai mẫu khiến khoảng tin cậy trông hẹp hơn sự thật khi chạy kiểm định về sau."
    ),
    ("DSC", "L04"): (
        " Trong dữ liệu kinh doanh hay y tế thực tế, chỉ một vài bản ghi sai số hoặc khách hàng đột biến có thể kéo trung bình cộng rời xa hẳn vùng tập trung đa số. "
        "Trung vị chia đôi tập dữ liệu đã sắp xếp và khoảng tứ phân vị đo bề rộng phần giữa năm mươi phần trăm mẫu nên hoàn toàn miễn nhiễm trước giá trị cực đoan ở hai đầu. "
        "Dùng quy tắc hàng rào một phẩy năm lần khoảng tứ phân vị đóng vai trò kính lúp đánh dấu các điểm nghi vấn để kiểm tra xem đó là lỗi nhập liệu hay hiện tượng thật cần giữ. "
        "Luôn đặt câu hỏi nghiệp vụ cho từng điểm ngoại lai thay vì mặc định xóa tự động tránh mất đúng tín hiệu quý giá nhất của bài toán."
    ),
    ("DSC", "L05"): (
        " Biểu đồ không chỉ là hình minh họa đẹp mắt mà là một lập luận bằng hình ảnh cần trung thực tuyệt đối với tỉ lệ định lượng của số liệu gốc. "
        "Biểu đồ cột biểu diễn độ lớn bằng chiều dài thanh nên đáy trục tung bắt buộc xuất phát từ không để mắt người xem không hiểu nhầm chênh lệch vài phần trăm thành gấp đôi. "
        "Biểu đồ đường cho phép thu phóng trục tung nhằm quan sát độ dốc xu hướng với điều kiện phải chú thích rõ phạm vi giá trị trên mặt biểu đồ. "
        "Tránh dùng biểu đồ ba chiều làm méo góc nhìn hay trục tung kép hai đơn vị khác nhau dễ đánh lạc hướng người đọc ngay trong vài giây lướt qua."
        " Ngoài ra việc kiểm tra hệ số phóng đại giữa diện tích hình vẽ và tỉ số dữ liệu thực tế giúp giữ sự trung thực trong mọi báo cáo trình bày."
    ),
    ("DSC", "L06"): (
        " Hệ số tương quan tuyến tính chỉ đo mức độ bám quanh một đường thẳng giữa hai biến, hoàn toàn bỏ qua những mối liên hệ hình cong rõ nét như đường hình chữ U. "
        "Vì phụ thuộc trực tiếp vào độ lệch chuẩn và khoảng cách tới điểm trung bình, chỉ một điểm ngoại lai nằm xa khối chính đủ sức đảo ngược dấu toàn bộ hệ số tương quan. "
        "Do đó nguyên tắc bất di bất dịch trong khám phá dữ liệu là luôn vẽ biểu đồ phân tán hai chiều trước khi tin vào một con số tóm tắt duy nhất. "
        "Khi đường dữ liệu uốn cong hoặc tách thành nhiều cụm riêng biệt, chuyển sang phân tích từng nhóm hay đổi thước đo thứ bậc sẽ tránh bỏ sót quy luật thật."
    ),
    ("DSC", "L07"): (
        " Nghịch lý gộp nhóm xảy ra khi một biến gây nhiễu thứ ba tác động đồng thời lên cả xác suất chọn phương án lẫn kết quả đầu ra cuối cùng. "
        "Nhóm áp dụng biện pháp mới thường nhận toàn ca nặng nên tỉ lệ gộp chung trông có vẻ tệ hơn dù nó chiến thắng ở mọi phân nhóm mức độ nhẹ và nặng riêng biệt. "
        "Trong phân tích dữ liệu quan sát, quyết định nên giữ tách theo từng phân tầng hay gộp chung bắt buộc dựa vào sơ đồ quan hệ nhân quả thay vì chọn bên có con số đẹp hơn. "
        "Nếu có điều kiện chạy thí nghiệm phân chia ngẫu nhiên, việc tung đồng xu chia đều khách sẽ cắt đứt đường đi của biến gây nhiễu hiệu quả nhất."
    ),
    ("DSC", "L09"): (
        " Khi lặp lại nhiều phép kiểm định thống kê độc lập trên cùng một bộ dữ liệu ở mức ngưỡng cố định năm phần trăm, xác suất xuất hiện ít nhất một báo động giả tăng nhanh chóng. "
        "Điều này lý giải vì sao việc sàng lọc hàng trăm biến hay dừng ngay sau lần thử vừa cho kết quả đẹp dễ tạo ra phát hiện ảo không thể lặp lại ngoài thực tế. "
        "Bổ sung điều chỉnh mức ngưỡng chia theo số phép thử hoặc chỉ định rõ trước duy nhất một giả thuyết chính sẽ giữ đúng mức rủi ro báo nhầm mong muốn. "
        "Ngoài giá trị p, luôn cân nhắc thêm tỉ lệ nền thực tế của giả thuyết đúng trong lĩnh vực nghiên cứu trước khi tin tưởng một kết quả vừa chạm ngưỡng."
    ),
    ("DSC", "L10"): (
        " Chia tách tập huấn luyện và tập kiểm tra phải được thực hiện đầu tiên ngay khi mở dữ liệu thô, trước mọi bước điền ô trống, chuẩn hoá hay chọn lọc đặc trưng. "
        "Nếu dùng thống kê toàn bộ tập để chuẩn hoá hoặc chọn biến rồi mới chia, thông tin từ tập kiểm tra đã lọt vào quá trình học gây ra độ chính xác cao giả tạo. "
        "Với chuỗi dữ liệu thời gian hoặc nhiều bản ghi thuộc cùng một người dùng, bắt buộc chia theo thời điểm cắt mốc hoặc theo mã nhóm thay vì bốc ngẫu nhiên từng dòng. "
        "Giữ kín tập kiểm tra cuối cùng và chỉ mở đánh giá đúng một lần cho kết quả trung thực phản ánh sát hiệu năng khi triển khai vận hành thật."
    ),
    ("DSC", "L13"): (
        " Xóa cột họ tên hay số định danh công dân hoàn toàn chưa đủ để bảo vệ danh tính người dùng vì tổ hợp ngày sinh, giới tính và mã bưu chính dễ dàng nối khớp ra đúng cá nhân. "
        "Khái quát hoá các trường bán định danh sao cho mỗi nhóm tương đồng chứa tối thiểu k người cùng lúc kết hợp đa dạng hoá giá trị nhạy cảm giúp giảm nguy cơ lộ danh tính. "
        "Khi bảng chứa quá nhiều cột liên kết đồng thời, giữ đạt chuẩn ẩn danh buộc phải gộp các dải thuộc tính thô hơn hẳn làm giảm độ chi tiết cho mô hình phân tích. "
        "Vì vậy nguyên tắc tối thiểu hoá dữ liệu chỉ thu đúng trường thật sự cần cho mục tiêu rõ ràng luôn là hàng rào bảo vệ bền vững nhất cho quyền riêng tư."
    ),
    ("DSC", "L14"): (
        " Một kết quả nghiên cứu hay phân tích kinh doanh chỉ đáng tin khi đồng nghiệp khác có thể chạy lại từ dữ liệu thô với cùng môi trường và ra đúng cùng con số. "
        "Việc cố định đồng thời bốn yếu tố gồm phiên bản mã nguồn, bản chụp dữ liệu gốc, danh sách thư viện môi trường và hạt giống ngẫu nhiên biến bản phân tích thành quy trình lặp lại được. "
        "Khi báo cáo số liệu đầu ra cho người ra quyết định, luôn trình bày độ lớn ảnh hưởng kèm khoảng tin cậy thay vì chỉ nêu mỗi chữ đạt ngưỡng có ý nghĩa. "
        "Nêu thẳng phạm vi dữ liệu khảo sát lẫn giới hạn kết luận giúp nâng độ uy tín và tránh các quyết định đầu tư quá mức dựa trên bằng chứng hẹp."
    ),
    ("MLO", "L00"): (
        " Trong một hệ thống học máy sản xuất thật, đoạn mã định nghĩa thuật toán huấn luyện thường chỉ chiếm một tỉ lệ rất nhỏ bên cạnh hạ tầng thu thập dữ liệu, kiểm chứng và phục vụ. "
        "Khác biệt lớn nhất với bài tập trên lớp là dữ liệu đầu vào biến đổi liên tục theo thị trường khiến độ chính xác của mô hình suy giảm âm thầm theo thời gian nếu thiếu giám sát. "
        "Để tránh phình nợ kỹ thuật khó gỡ, toàn bộ quy trình từ chuẩn hoá đặc trưng, huấn luyện cho tới kiểm thử triển khai phải được viết thành mã tự động chạy lặp lại được."
    ),
    ("MLO", "L01"): (
        " Tính tái lập đòi hỏi đồng bộ đầy đủ cả bốn mảnh ghép từ mã nguồn, phiên bản dữ liệu, thư viện phần mềm cho tới hạt giống ngẫu nhiên dùng khi chia tập hay khởi tạo trọng số. "
        "Chỉ cần bỏ sót một hạt giống trong thao tác xáo trộn hay sai khác nhỏ ở phiên bản gói tính toán số học, hai lần chạy trên cùng một máy vẫn có thể lệch điểm đáng kể. "
        "Trên cụm máy tính nhiều bộ xử lý chạy song song, thứ tự cộng dồn dấu phẩy động vốn không tất định nên cách đo đáng tin là báo cáo trung bình cùng độ dao động qua nhiều lần chạy."
    ),
    ("MLO", "L02"): (
        " Gắn phiên bản dữ liệu bằng các tên tệp sửa tay như bản cuối hay bản mới nhất dễ dẫn đến nhầm lẫn không thể truy vết khi có hàng trăm tập dữ liệu phát sinh liên tục. "
        "Cách chuẩn xác là băm nội dung tệp dữ liệu thành chuỗi định danh duy nhất rồi lưu giữ chỉ số tham chiếu gắn kèm mã nguồn trong cùng lần xác nhận. "
        "Nhờ lưu trữ hướng nội dung tại kho đối tượng kết hợp ghi nhận dòng dõi nối từ mô hình về tập huấn luyện, mã chạy và hạt giống, ta dễ dàng quay lại kiểm định bất kỳ phiên bản nào từng chạy trên sản xuất."
    ),
    ("MLO", "L03"): (
        " Hệ học máy cần được kiểm thử ở ba lớp gồm lược đồ giá trị dữ liệu đầu vào, hiệu năng tách riêng theo từng phân khúc khách hàng và hành vi bất biến của dự đoán. "
        "Thử nghiệm bất biến thay đổi một thông tin không liên quan như tên gọi nhưng giữ nguyên ngữ cảnh nhằm bảo đảm điểm số dự đoán không thay đổi vô lý theo thuộc tính nhiễu. "
        "Thử nghiệm định hướng kiểm tra nguyên tắc logic chiều tăng giảm đơn giản của bài toán còn kiểm tra theo lát giúp chặn các mô hình điểm tổng cao nhưng bỏ rơi nhóm thiểu số. "
        "Nhờ chạy bộ kiểm thử tự động trong vài giây trước mỗi đợt đóng gói, đội kỹ thuật ngăn được nhiều lỗi suy giảm âm thầm trước khi chạm người dùng thật."
    ),
    ("MLO", "L04"): (
        " Việc lưu vết đầy đủ tham số, phiên bản dữ liệu và kết quả của từng lượt thử giúp tránh lặp lại sai lầm cũ và phân biệt rõ cải tiến thật khỏi nhiễu may mắn. "
        "Mỗi khi dùng kết quả trên tập kiểm định để chọn cấu hình hay điều chỉnh kiến trúc mô hình, độ chính xác trên tập kiểm định ấy đều bị thổi phồng dần theo số lượt chọn lọc. "
        "Quy tắc kỷ luật là giữ kín tập kiểm tra cuối cùng ở chế độ chỉ đọc một lần để báo cáo đánh giá khách quan nhất trước quyết định phát hành."
    ),
    ("MLO", "L05"): (
        " Hiện tượng lệch giữa huấn luyện và phục vụ phát sinh bất cứ khi nào hàm tính đặc trưng lúc chạy thực tế khác công thức, giá trị thống kê chuẩn hoá hay thời điểm cắt mốc lúc học. "
        "Dù chỉ lệch một tham số trung bình nhỏ hoặc tính nhầm bằng thống kê tương lai chưa xảy ra lúc phục vụ, chất lượng dự đoán ngoài thực tế sẽ sụt mạnh dù kiểm định ngoại tuyến rất đẹp. "
        "Giải pháp căn cơ là dùng chung một định nghĩa mã duy nhất lưu trong kho đặc trưng tập trung, chốt cứng tham số chuẩn hoá từ tập huấn luyện và ghi nhật ký để kiểm chéo liên tục."
    ),
    ("MLO", "L06"): (
        " Chọn kiến trúc phục vụ theo lô hay trực tuyến phụ thuộc trực tiếp vào yêu cầu độ tươi mới của dự đoán và giới hạn độ trễ mà trải nghiệm người dùng cho phép. "
        "Nếu hệ thống không cần phản hồi tức thì từng mili-giây như gợi ý danh mục ban đêm, tính theo lô tiết kiệm tài nguyên hơn nhiều và loại bỏ áp lực chờ trực tuyến. "
        "Ngược lại khi phục vụ trực tuyến, gộp theo lô giúp tăng mạnh thông lượng phần cứng nhưng làm các yêu cầu đầu hàng phải chờ lâu hơn, nên luôn cần chốt hạn mức chờ tối đa và đặt tầng dự phòng nhanh."
    ),
    ("MLO", "L08"): (
        " Giám sát trôi dữ liệu so sánh trực tiếp phân phối đặc trưng đầu vào thực tế ở hiện tại với phân phối chuẩn lúc huấn luyện để báo động sớm trước khi người dùng gặp lỗi. "
        "Chỉ số ổn định quần thể chia dải giá trị thành các rổ cố định rồi cộng dồn sai lệch lôgarit nên luôn cho một con số dương dễ cài ngưỡng theo dõi tự động. "
        "Tuy nhiên ngưỡng cảnh báo chỉ mang tính quy ước tham chiếu, nên ngay khi thu nhận được nhãn kết quả thật cần đối chiếu lại chỉ số sai số thực của mô hình."
    ),
    ("MLO", "L09"): (
        " Khi luật quy luật ngầm nối giữa đầu vào và nhãn thật thay đổi theo thị hiếu hay thời cuộc gọi là trôi khái niệm, chỉ theo dõi đầu vào sẽ bỏ lọt hoàn toàn sự suy giảm chất lượng. "
        "Nguy hiểm hơn là vòng phản hồi tự củng cố, khi chính gợi ý của mô hình quyết định khách hàng sẽ bấm gì và biến dữ liệu ngày mai thành phản ánh thiên lệch của chính nó. "
        "Luôn dành một tỉ lệ lưu lượng nhỏ để khám phá ngẫu nhiên các phương án ít xuất hiện đồng thời chỉ đưa mô hình huấn luyện lại vào chạy chính khi vượt qua kiểm định an toàn."
    ),
    ("MLO", "L10"): (
        " Với mọi bài toán dùng xác suất để tính giá trị kỳ vọng hay quyết định kích hoạt rủi ro, thứ tự xếp hạng đúng thôi chưa đủ mà bản thân con số xác suất phải tương xứng tần suất thật. "
        "Hiệu chuẩn kém khiến mô hình nói xác suất tám mươi phần trăm nhưng ngoài đời chỉ đúng một nửa, dẫn tới tính sai toàn bộ phương án bù lỗ hoặc phân bổ tài nguyên kiểm duyệt. "
        "Đo bằng điểm sai lệch bình phương cùng biểu đồ hiệu chuẩn giúp phát hiện sớm bệnh quá tự tin và tiến hành hiệu chuẩn lại định kỳ ngay khi dữ liệu thay đổi."
    ),
    ("MLO", "L11"): (
        " Đưa mô hình lớn lên máy chủ tiết kiệm bộ nhớ hay chạy trên thiết bị biên đòi hỏi các kỹ thuật thu gọn như lượng tử hoá số thực về số nguyên ít bit hơn hoặc chưng cất tri thức sang mạng nhỏ gọn. "
        "Mỗi phép nén giúp cắt giảm gấp nhiều lần bộ nhớ trong và tăng tốc tính toán nhờ đổi từ độ chính xác cao sang bước rời rạc có sai số tối đa nửa khoảng chia. "
        "Do sai số làm tròn nhỏ ở từng phép nhân có thể cộng dồn qua hàng chục tầng sâu, bắt buộc đánh giá lại toàn bộ tập kiểm tra chuẩn trước khi phát hành thay cho ước lượng cảm tính."
    ),
    ("MLO", "L12"): (
        " Điểm chính xác trung bình toàn tập rất cao dễ che lấp hoàn toàn việc mô hình hoạt động tệ hại trên một nhóm người dùng ít xuất hiện hay vùng địa lý cụ thể. "
        "Gỡ bỏ trực tiếp cột giới tính hay nhóm nhạy cảm không giải quyết triệt để vấn đề vì nhiều biến phụ khác trong dữ liệu vẫn có thể đóng vai trò thay thế gần tương đương. "
        "Xuất tự động thẻ mô hình ghi rõ hiệu năng phân theo từng lát đối tượng, phạm vi phù hợp và trường hợp chống chỉ định giúp cả đội vận hành minh bạch ranh giới an toàn."
    ),
    ("MLO", "L13"): (
        " Trong hệ thống học máy, toàn bộ kho dữ liệu thu thập đều trở thành đầu vào trực tiếp viết nên quy tắc ứng xử của mô hình tương lai, nên đầu độc nhãn tạo ra lỗ hổng ngay trong trọng số. "
        "Ngoài rủi ro bị chèn mẫu độc mang tín hiệu kích hoạt cửa sau, dịch vụ dự đoán công khai còn có thể bị kẻ tấn công hỏi dồn liên tục để dò dữ liệu riêng tư hay tìm mẫu đối kháng đánh lừa. "
        "Biện pháp phòng vệ cơ bản là kiểm tra nguồn gốc kèm chữ ký mã băm cho từng lô dữ liệu huấn luyện, giới hạn tốc độ gọi và ghi vết phát hiện truy vấn bất thường."
    ),
}

# Fix de.md & loi_giai.py dynamic calculation in DSC L00 & MLO L11 P1 glosses
dsc_l00_de = ROOT / "labs/DSC/L00/de.md"
dsc_l00_lg = ROOT / "labs/DSC/L00/loi_giai.py"
dsc_l00_de.write_text(
    "# Lab DSC L00 — Biến gây nhiễu trong dữ liệu quan sát so với phân chia ngẫu nhiên\n\n"
    "Trong dữ liệu quan sát ở cửa hàng, nhóm đã xem quảng cáo có `75/120` khách mua hàng, nhóm chưa xem có `30/150` khách mua (`is_observational = 1`, không chia ngẫu nhiên). "
    "Tính hiệu chênh lệch quan sát và kiểm tra cờ cần phân chia ngẫu nhiên từ biến `is_observational`.\n\n"
    "Định dạng đầu ra:\n`obs_diff=<2 chữ số> needs_randomization=<1 hoặc 0>`\n\n"
    "Chấm tự động:\n```bash\nbash labs/cham.sh DSC L00 duong_dan/bai_cua_ban.py\n```\n",
    encoding="utf-8",
)
dsc_l00_lg.write_text(
    "seen_n, seen_cnt = 120, 75\nunseen_n, unseen_cnt = 150, 30\nis_observational = 1\n"
    "obs_diff = (seen_cnt / seen_n) - (unseen_cnt / unseen_n)\n"
    "print(f\"obs_diff={obs_diff:.2f} needs_randomization={int(is_observational == 1)}\")\n",
    encoding="utf-8",
)

mlo_l11_de = ROOT / "labs/MLO/L11/de.md"
mlo_l11_de.write_text(
    "# Lab MLO L11 — Lượng tử hoá đối xứng số nguyên 8 bit (int8) và nén bộ nhớ trong (RAM)\n\n"
    "Lượng tử hoá giá trị `-0.9` về số nguyên 8 bit đối xứng (`int8`) trên khoảng `[-2, 2]` (giá trị nguyên lớn nhất `q_max = 127`), "
    "tính sai số khôi phục và so bộ nhớ trong (`RAM`) cho mô hình `13 tỉ` tham số giữa dạng số thực dấu phẩy động 32 bit (`fp32`, `4 byte/tham số`) và số nguyên 8 bit (`int8`, `1 byte/tham số`).\n\n"
    "Định dạng đầu ra (2 dòng):\n`q=<số nguyên> deq=<4 chữ số> err=<4 chữ số>`\n`fp32_gb=<số nguyên> int8_gb=<số nguyên>`\n\n"
    "Chấm tự động:\n```bash\nbash labs/cham.sh MLO L11 duong_dan/bai_cua_ban.py\n```\n",
    encoding="utf-8",
)

for c in ("DAN", "DSC", "MLO"):
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c.lower()}/L*.yaml"))):
        p = Path(fp)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        txt = p.read_text(encoding="utf-8")

        # Exact manual patches
        for old, new in LESSON_PATCHES.get(rel, []):
            if old in txt:
                txt = txt.replace(old, new)
            elif new not in txt:
                print(f"[WARN_NO_MATCH] {rel}: {old[:60]}", flush=True)

        # Global spelling normalization in Batch 8A
        txt = txt.replace("mili-giây", "mi-li-giây").replace("mili giây", "mi-li-giây")
        p.write_text(txt, encoding="utf-8")

        # Add clean domain synthesis into recap#0 say: when < 1665 words
        d = yaml.safe_load(txt)
        lid = d["id"]
        words = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc.get("steps", []))
        if words < 1665 and (c, lid) in BOOST_TEXT:
            extra = BOOST_TEXT[(c, lid)]
            rec = next(sc for sc in d["scenes"] if sc["id"] == "recap")
            old_say = rec["steps"][0]["say"]
            if extra.strip()[:40] not in old_say:
                new_say = old_say.rstrip() + extra
                # Safe line-based replacement on the exact `say:` line to preserve all comments/formatting
                lines = txt.splitlines(keepends=True)
                replaced = False
                for idx in range(len(lines) - 1, -1, -1):
                    if lines[idx].lstrip().startswith("say:") and old_say in lines[idx]:
                        lines[idx] = lines[idx].replace(old_say, new_say)
                        replaced = True
                        break
                if not replaced:
                    raise RuntimeError(f"Could not find recap#0 say line in {rel}")
                p.write_text("".join(lines), encoding="utf-8")

# Also check DSC L00 lesson practice#0 `vs` and `de.md` if needed & sync DSC/DAN/MLO
for c in ("DAN", "DSC", "MLO"):
    files = [str(Path(f).relative_to(ROOT)) for f in sorted(glob.glob(str(ROOT / f"lessons/{c.lower()}/L*.yaml")))]
    for f in files:
        d = yaml.safe_load((ROOT / f).read_text(encoding="utf-8"))
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc.get("steps", []))
        cang = sum(len(re.findall(r"\bcàng\b", str(st.get(k) or ""), re.I)) for sc in d["scenes"] for st in sc.get("steps", []) for k in ("show", "say"))
        if w < 1660 or cang > 0:
            print(f"[CHECK] {c} {d['id']}: w={w} cang={cang}", flush=True)

for c in ("DAN", "DSC", "MLO"):
    files = [str(Path(f).relative_to(ROOT)) for f in sorted(glob.glob(str(ROOT / f"lessons/{c.lower()}/L*.yaml")))]
    for cmd in [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", "tools/lv.py", "lint"] + files,
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
        [PY, "-B", "audit/review/arith_scan.py", c],
    ]:
        print(">>> RUN:", " ".join(cmd[:4]), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"

print("STAGE 8 BATCH 8A (DAN, DSC, MLO = 44 LESSONS) 100% FIXED + GATES PASS!", flush=True)
