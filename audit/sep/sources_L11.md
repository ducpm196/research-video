# Nguồn đã đọc nguyên văn cho SEP L11 (bài hành trình: bảo vệ dữ liệu cá nhân 2000 → 2026)

Đọc ngày 2026-11-02. Ba văn bản Việt Nam là bản PDF ký số ảnh quét (pdftotext chỉ ra dòng chữ ký) — đọc TỪNG TRANG bằng công cụ xem ảnh,
chép nguyên văn câu dưới đây. Hiệu lực ghi theo chính văn bản và theo trường “Ngày có hiệu lực” của cổng vanban.chinhphu.vn. Luật có thể
đổi sau ngày đọc; bài giảng dạy nguyên lý và cách tra, không tư vấn pháp lý cho trường hợp cụ thể. Mọi con số “(số minh hoạ)” trong bài
là của bài, không của nguồn; mọi phép tính lại ở `checks` và `audit/sep/verify_parts/L11.py`.

## [S00] L. Sweeney, *Simple Demographics Often Identify People Uniquely*, Carnegie Mellon University, Data Privacy Working Paper 3, 2000
Tải: https://dataprivacylab.org/projects/identifiability/paper1.pdf (200; pdftotext)
- Tóm tắt: “I report on experiments I conducted using 1990 U.S. Census summary data … It was found that 87% (216 million of 248 million) of
  the population in the United States had reported characteristics that likely made them unique based only on {5-digit ZIP, gender, date
  of birth}. About half of the U.S. population (132 million of 248 million or 53%) are likely to be uniquely identified by only {place,
  gender, date of birth} … {county, gender, date of birth} are likely to uniquely identify 18% of the U.S. population.”
- Tóm tắt: “Clearly, data released containing such information about these individuals should not be considered anonymous. Yet, health
  and other person-specific data are publicly available in this form.”
- Mục 2: “in the voter list, there were 2 possible values for gender and 5 possible five-digit ZIP codes; birth dates were within a range
  of 365 days for 100 years. This gives 365,000 unique values, but there were only 54,805 voters.”

## [A18] ACM Code of Ethics and Professional Conduct, 22/6/2018 — nguyên tắc 1.6 (bản PDF acm.org, xem sources_L00.md)
- “Only the minimum amount of personal information necessary should be collected in a system. The retention and disposal periods for that
  information should be clearly defined, enforced, and communicated to data subjects. Personal information gathered for a specific purpose
  should not be used for other purposes without the person's consent. Merged data collections can compromise privacy features present in
  the original collections. Therefore, computing professionals should take special care for privacy when merging data collections.”
- “This requires taking precautions to prevent re-identification of anonymized data or unauthorized data collection”.

## [N13] Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân, ngày 17/4/2023
Trang: https://vanban.chinhphu.vn/?pageid=27160&docid=207759 (“Ngày ban hành 17-04-2023”, “Ngày có hiệu lực 01-07-2023”);
toàn văn ký số: https://datafiles.chinhphu.vn/cpp/files/vbpq/2023/4/13nd.signed.pdf (39 trang; đọc trang 17–20).
- Điều 23 khoản 1: “Trường hợp phát hiện xảy ra vi phạm quy định bảo vệ dữ liệu cá nhân, Bên Kiểm soát dữ liệu cá nhân, Bên Kiểm soát và
  xử lý dữ liệu cá nhân thông báo cho Bộ Công an (Cục An ninh mạng và phòng, chống tội phạm sử dụng công nghệ cao) chậm nhất 72 giờ sau
  khi xảy ra hành vi vi phạm theo Mẫu số 03 tại Phụ lục của Nghị định này. Trường hợp thông báo sau 72 giờ thì phải kèm theo lý do thông
  báo chậm, muộn.”
- Điều 23 khoản 4: “Trường hợp không thể thông báo đầy đủ các nội dung quy định tại khoản 3 Điều này, việc thông báo có thể được thực hiện
  theo từng đợt, từng giai đoạn.”
- Điều 24 khoản 1: “… lập và lưu giữ Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân của mình kể từ thời điểm bắt đầu xử lý dữ liệu cá nhân.”
- Điều 24 khoản 4: “… gửi Bộ Công an … 01 bản chính theo Mẫu số 04 tại Phụ lục của Nghị định này trong thời gian 60 ngày kể từ ngày tiến
  hành xử lý dữ liệu cá nhân.”

## [L91] Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15, ngày 26/6/2025
Trang: https://vanban.chinhphu.vn/?pageid=27160&docid=214590 (“Ngày ban hành 26-06-2025”, “Ngày có hiệu lực 01-01-2026”);
toàn văn ký số: https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/7/91qh.signed.pdf (23 trang; đọc trang 1–7, 11, 13–15, 22–23).
Đối chiếu tóm tắt chính thức: Sở Tư pháp Tuyên Quang, “Đề cương giới thiệu Luật Bảo vệ dữ liệu cá nhân”
(https://khodulieu.sohoa.tuyenquang.gov.vn/congthongtin/media/a3a0a543e41f76745db2acd0fd744175.pdf) — chỉ để đối chiếu.
- Điều 1 khoản 2: Luật áp dụng đối với “a) Cơ quan, tổ chức, cá nhân Việt Nam; b) Cơ quan, tổ chức, cá nhân nước ngoài tại Việt Nam; c) Cơ
  quan, tổ chức, cá nhân nước ngoài trực tiếp tham gia hoặc có liên quan đến hoạt động xử lý dữ liệu cá nhân của công dân Việt Nam …”
- Điều 2 khoản 1: “Dữ liệu cá nhân là dữ liệu số hoặc thông tin dưới dạng khác xác định hoặc giúp xác định một con người cụ thể, bao gồm:
  dữ liệu cá nhân cơ bản và dữ liệu cá nhân nhạy cảm. Dữ liệu cá nhân sau khi khử nhận dạng không còn là dữ liệu cá nhân.”
- Điều 2 khoản 5: “Chủ thể dữ liệu cá nhân là người được dữ liệu cá nhân phản ánh.”
- Điều 2 khoản 11: “Khử nhận dạng dữ liệu cá nhân là quá trình thay đổi hoặc xóa thông tin để tạo ra dữ liệu mới không thể xác định hoặc
  không thể giúp xác định được một con người cụ thể.”
- Điều 2 khoản 12: “Đánh giá tác động xử lý dữ liệu cá nhân là việc phân tích, đánh giá rủi ro có thể xảy ra trong quá trình xử lý dữ liệu
  cá nhân để áp dụng các biện pháp giảm thiểu rủi ro, bảo vệ dữ liệu cá nhân.”
- Điều 8 khoản 3: “Mức phạt tiền tối đa trong xử phạt vi phạm hành chính đối với hành vi mua, bán dữ liệu cá nhân là 10 lần khoản thu có
  được từ hành vi vi phạm; trường hợp không có khoản thu từ hành vi vi phạm hoặc mức phạt tính theo khoản thu có được từ hành vi vi phạm
  thấp hơn mức phạt tiền tối đa quy định tại khoản 5 Điều này thì áp dụng mức phạt tiền theo quy định tại khoản 5 Điều này.”
- Điều 8 khoản 4: “Mức phạt tiền tối đa trong xử phạt vi phạm hành chính đối với tổ chức có hành vi vi phạm quy định chuyển dữ liệu cá nhân
  xuyên biên giới là 5% doanh thu của năm trước liền kề của tổ chức đó; trường hợp không có doanh thu của năm trước liền kề hoặc mức phạt
  tính theo doanh thu thấp hơn mức phạt tiền tối đa theo quy định tại khoản 5 Điều này thì áp dụng mức phạt tiền theo quy định tại khoản 5
  Điều này.”
- Điều 8 khoản 5: “Mức phạt tiền tối đa trong xử phạt vi phạm hành chính đối với các hành vi vi phạm khác trong lĩnh vực bảo vệ dữ liệu cá
  nhân là 03 tỷ đồng.”
- Điều 8 khoản 6: “Mức phạt tiền tối đa quy định tại các khoản 3, 4 và 5 Điều này được áp dụng đối với tổ chức; cá nhân thực hiện cùng
  hành vi vi phạm thì mức phạt tiền tối đa bằng một phần hai mức phạt tiền đối với tổ chức.”
- Điều 9 khoản 4: “a) Thể hiện sự đồng ý đối với từng mục đích; … d) Sự im lặng hoặc không phản hồi không được coi là sự đồng ý.”
- Điều 12 khoản 1: “… dữ liệu cá nhân sau khi được mã hóa vẫn là dữ liệu cá nhân.”
- Điều 20 khoản 1 c: “Cơ quan, tổ chức, cá nhân tại Việt Nam hoặc ở nước ngoài sử dụng nền tảng ở ngoài lãnh thổ nước Cộng hòa xã hội chủ
  nghĩa Việt Nam để xử lý dữ liệu cá nhân được thu thập tại Việt Nam.” (một trường hợp chuyển dữ liệu xuyên biên giới)
- Điều 20 khoản 2: “… phải lập hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới và gửi 01 bản chính cho cơ quan chuyên trách
  bảo vệ dữ liệu cá nhân trong thời gian 60 ngày kể từ ngày đầu tiên chuyển dữ liệu cá nhân xuyên biên giới, trừ trường hợp quy định tại
  khoản 6 Điều này.”
- Điều 22 khoản 1: “Hồ sơ đánh giá tác động xử lý dữ liệu cá nhân và hồ sơ đánh giá tác động chuyển dữ liệu cá nhân xuyên biên giới được cập
  nhật định kỳ 06 tháng khi có sự thay đổi hoặc cập nhật ngay trong các trường hợp quy định tại khoản 2 Điều này.”
- Điều 23 khoản 1: “Bên kiểm soát dữ liệu cá nhân, bên kiểm soát và xử lý dữ liệu cá nhân, bên thứ ba phát hiện vi phạm quy định về bảo vệ dữ
  liệu cá nhân có thể gây tổn hại đến quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội hoặc xâm phạm đến tính mạng, sức khỏe, danh
  dự, nhân phẩm, tài sản của chủ thể dữ liệu cá nhân thì phải thông báo cho cơ quan chuyên trách bảo vệ dữ liệu cá nhân chậm nhất là 72 giờ
  kể từ khi phát hiện hành vi vi phạm.”
- Điều 38 khoản 1: “Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.”
- Điều 38 khoản 2: “Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21,
  Điều 22 và khoản 2 Điều 33 của Luật này trong thời gian 05 năm kể từ ngày Luật này có hiệu lực thi hành, trừ doanh nghiệp nhỏ, doanh
  nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm hoặc xử lý dữ liệu cá nhân của số
  lượng lớn chủ thể dữ liệu cá nhân.”
- Điều 39 khoản 1: “Hoạt động xử lý dữ liệu cá nhân đang thực hiện mà đã được chủ thể dữ liệu cá nhân đồng ý hoặc theo thỏa thuận theo quy
  định của Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ trước ngày Luật này có hiệu lực thi hành thì tiếp tục thực
  hiện, không phải xin đồng ý lại hoặc thỏa thuận lại.”
- Cuối văn bản: “Luật này được Quốc hội … khóa XV, kỳ họp thứ 9 thông qua ngày 26 tháng 6 năm 2025.”

## [N356] Nghị định 356/2025/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Bảo vệ dữ liệu cá nhân, ngày 31/12/2025
Tải: https://hcc.nghean.gov.vn/laws/detail/Nghi-dinh-so-356-2025-ND-CP-cua-Chinh-phu-Quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-Luat-Bao-ve-du-lieu-ca-nhan-2058/?download=1&id=0
(cổng hành chính công tỉnh Nghệ An; tệp “356-nd.signed.pdf”, chữ ký số “CỔNG THÔNG TIN ĐIỆN TỬ CHÍNH PHỦ”, 05.01.2026; 71 trang, đọc trang
1–4, 36–41). Bản .doc trên vbpl.moj.gov.vn không kết nối được trong phiên (NOT_VERIFIED, không cần).
- Điều 3: dữ liệu cá nhân cơ bản gồm “1. Họ, chữ đệm và tên khai sinh …; 2. Ngày, tháng, năm sinh …; 3. Giới tính; 4. Nơi sinh, … nơi ở hiện
  tại …”.
- Điều 4 khoản 1: dữ liệu cá nhân nhạy cảm gồm “… d) Tình trạng sức khỏe; … h) Vị trí của cá nhân được xác định qua dịch vụ định vị; …”.
- Điều 41 khoản 1: “Doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp được quyền lựa chọn thực hiện hoặc không thực hiện quy định tại Điều 21,
  Điều 22 và khoản 2 Điều 33 của Luật Bảo vệ dữ liệu cá nhân trong thời gian 05 năm kể từ ngày Luật Bảo vệ dữ liệu cá nhân có hiệu lực thi
  hành, trừ doanh nghiệp nhỏ, doanh nghiệp khởi nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu cá nhân nhạy cảm
  hoặc xử lý dữ liệu cá nhân kể từ thời điểm có quy mô đạt từ 100 nghìn chủ thể dữ liệu cá nhân trở lên dựa trên kết quả tích lũy tổng
  lượng dữ liệu cá nhân đã xử lý.”
- Điều 42 khoản 1: “Nghị định này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.”
- Điều 42 khoản 2: “Nghị định số 13/2023/NĐ-CP ngày 17 tháng 4 năm 2023 của Chính phủ về bảo vệ dữ liệu cá nhân hết hiệu lực kể từ ngày
  Nghị định này có hiệu lực thi hành.”

## Con số dùng trong bài
- CITED: 87% (216/248 triệu), 53%, 18%, 365 000 giá trị, 54 805 cử tri [S00]; 72 giờ “sau khi xảy ra” [N13]; 60 ngày [N13], [L91 Đ20];
  10 lần, 5%, 3 tỉ, một nửa, 72 giờ “kể từ khi phát hiện”, 06 tháng, 05 năm [L91]; 100 nghìn chủ thể [N356]; các ngày ban hành, hiệu lực.
- VER (checks + verify_parts/L11.py): 2·5·365·100 = 365 000; 365 000/54 805 ≈ 6,7; (1 − 1/365 000)^54 804 ≈ 0,86 ≈ e^(−0,15);
  17/4 → 1/7/2023 = 75 ngày; 72/24 = 3; 2/3 + 60 ngày = 1/5; 10 × 0,5 = 5 tỉ; 5% × 200 = 10 tỉ; 3/2 = 1,5 tỉ; hạn ngày 3 so với ngày 8;
  1/1/2026 + 5 năm = 1/1/2031; 100 000/4000 = 25 tháng; 12/6 = 2; 6/11/2026 17:00 + 72 giờ = 9/11/2026 17:00; (100 000 − 30 000)/5000 = 14.
- SỐ MINH HOẠ: phường 5000 người, 160/4000/8000 tổ hợp (≈ 0,54, khoảng 2677 người); 0,5 tỉ khoản thu; doanh thu 200 tỉ; ngày 0/ngày 5;
  bắt đầu xử lý 2/3; 4000 và 5000 người mỗi tháng; 30 000 người dùng; sự cố thứ Sáu 6/11/2026.

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- GDPR (Liên minh châu Âu): eur-lex trả 202 (thách đố) cho mọi đường dẫn, web.archive.org trả 429 trong phiên → NOT_VERIFIED, không dạy
  điều khoản, mức phạt hay ngày áp dụng nào của GDPR.
- Không nói Nghị định 13/2023 là văn bản “đầu tiên” về dữ liệu cá nhân ở Việt Nam (chưa đọc nguồn khẳng định).
- Không dạy chi tiết Điều 21 (hồ sơ đánh giá tác động), Điều 33 (lực lượng bảo vệ dữ liệu) ngoài câu chữ đã trích; không dạy định nghĩa
  “doanh nghiệp nhỏ, khởi nghiệp” (văn bản khác, chưa đọc).
- Không dạy “số lượng lớn chủ thể” của Luật bằng con số nào khác ngoài ngưỡng 100 nghìn mà Nghị định 356 Điều 41 nêu.
- Nghiên cứu năm 2000: không kể giai thoại về một chính trị gia cụ thể (không nêu tên cá nhân; chưa trích trong phiên).

## Đọc lại đợt C (2026-11-09)
- vanban.chinhphu.vn docid=214590 (HTTP 200): trường “Ngày ban hành 26-06-2025”, “Ngày có hiệu lực 01-01-2026” — khớp. Không mở lại các
  bản PDF ký số (ảnh quét) và Nghị định 356/2025; giữ theo câu trích ở trên (đọc 2026-11-02).
- GDPR, Đạo luật AI của EU: bài vẫn không dạy điều khoản nào (không có câu nào trong bài nói về hai văn bản này) — không cần đối chiếu.
