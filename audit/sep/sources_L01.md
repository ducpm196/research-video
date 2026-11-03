# Nguồn đã đọc nguyên văn cho SEP L01 (dữ liệu cá nhân, tối thiểu hoá, định danh lại)

Đọc ngày 2026-11-02. Luật có thể đã đổi sau ngày này — bài ghi ngày đọc và hiệu lực, không tư vấn pháp lý cụ thể.
Mọi con số về phòng khám, phường 10 000 người, ứng dụng đặt lịch khám, quận 5000 người là SỐ MINH HOẠ, tính lại trong `checks`
và `audit/sep/verify_parts/L01.py`.

## [S00] L. Sweeney, *Simple Demographics Often Identify People Uniquely*, Carnegie Mellon University, Data Privacy Working Paper 3, 2000
Tải: https://dataprivacylab.org/projects/identifiability/paper1.pdf (200; pdftotext)
- Tóm tắt: “It was found that 87% (216 million of 248 million) of the population in the United States had reported characteristics
  that likely made them unique based only on {5-digit ZIP, gender, date of birth}.”
- Tóm tắt: “Clearly, data released containing such information about these individuals should not be considered anonymous.”
- §2.1: “These data collections often include the patient's ZIP code, birth date, gender, and ethnicity but no explicit identifiers like
  name or address.” … “For twenty dollars I purchased the voter registration list for Cambridge Massachusetts” … “This information can
  be linked using ZIP, birth date and gender to the medical information, thereby linking diagnosis, procedures, and medications to
  particularly named individuals.”
- §2.1: “in the voter list, there were 2 possible values for gender and 5 possible five-digit ZIP codes; birth dates were within a range of
  365 days for 100 years. This gives 365,000 unique values, but there were only 54,805 voters.”
- Dữ liệu nền: “using 1990 U.S. Census summary data”.

## [L91] Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15
Tải: trang https://vanban.chinhphu.vn/?pageid=27160&docid=214590 (ngày ban hành 26-06-2025, ngày có hiệu lực 01-01-2026) →
tệp ký số https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/7/91qh.signed.pdf (23 trang, ảnh quét; đọc từng trang bằng mắt).
- Điều 2, khoản 1: “Dữ liệu cá nhân là dữ liệu số hoặc thông tin dưới dạng khác xác định hoặc giúp xác định một con người cụ thể, bao
  gồm: dữ liệu cá nhân cơ bản và dữ liệu cá nhân nhạy cảm. Dữ liệu cá nhân sau khi khử nhận dạng không còn là dữ liệu cá nhân.”
- Điều 2, khoản 11: “Khử nhận dạng dữ liệu cá nhân là quá trình thay đổi hoặc xóa thông tin để tạo ra dữ liệu mới không thể xác định
  hoặc không thể giúp xác định được một con người cụ thể.”
- Điều 3, khoản 2: “Chỉ được thu thập, xử lý dữ liệu cá nhân đúng phạm vi, mục đích cụ thể, rõ ràng, bảo đảm tuân thủ quy định của pháp luật.”
- Điều 3, khoản 3: “… được lưu trữ trong khoảng thời gian phù hợp với mục đích xử lý dữ liệu cá nhân, trừ trường hợp pháp luật có quy
  định khác.”
- Điều 9, khoản 4: “a) Thể hiện sự đồng ý đối với từng mục đích;” … “d) Sự im lặng hoặc không phản hồi không được coi là sự đồng ý.”
- Điều 12, khoản 1: “Mã hóa dữ liệu cá nhân là việc chuyển đổi dữ liệu cá nhân sang dạng không nhận biết được dữ liệu cá nhân nếu
  không được giải mã; dữ liệu cá nhân sau khi được mã hóa vẫn là dữ liệu cá nhân.”
- Điều 38, khoản 1: “Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.”
- Cuối văn bản: “Luật này được Quốc hội … khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.”
- Đối chiếu phụ (không làm nguồn chính): thuvienphapluat.vn trả 403 trong phiên — không dùng.

## [ACM18] ACM Code of Ethics and Professional Conduct (2018), nguyên tắc 1.6
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf (200)
- “This requires taking precautions to prevent re-identification of anonymized data or unauthorized data collection”
- “Only the minimum amount of personal information necessary should be collected in a system. The retention and disposal periods for
  that information should be clearly defined, enforced, and communicated to data subjects.”
- “Personal information gathered for a specific purpose should not be used for other purposes without the person's consent.”
- “Merged data collections can compromise privacy features present in the original collections. Therefore, computing professionals should
  take special care for privacy when merging data collections.”

## Mô hình toán của bài (không phải phát biểu của nguồn)
- Mỗi người rơi đều, độc lập vào một trong c tổ hợp → khả năng duy nhất (1 − 1/c)^(N − 1). Ngày sinh thật không đều, nên đây là
  xấp xỉ minh hoạ; con số 84% trong bài là của mô hình (ghi “theo phép tính của bài này”), con số 87% là của [S00].

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- Không dạy mức phạt, chuyển dữ liệu ra nước ngoài, danh mục dữ liệu nhạy cảm (danh mục do Chính phủ ban hành, chưa đọc cho bài này).
- Không dạy quy định của GDPR: eur-lex trả 202/429 trong phiên — NOT_VERIFIED.
- Không khẳng định một bảng cụ thể “đạt chuẩn khử nhận dạng theo luật” — luật không cho ngưỡng số; bài chỉ dạy cách đếm rủi ro.
