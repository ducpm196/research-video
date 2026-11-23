# Mẫu H — phần 3: đã đọc 10/10 bài

Sáu trên mười bài có lỗi mức MUST (14 MUST, 34 SHOULD), nên tuyên bố "100% không lỗi, đạt chuẩn Tự làm" không đứng được trên mẫu này. Bốn bài còn lại (BNX L36, FND L10, INT L08, ROB L05) chỉ có SHOULD. Mọi sha16 khớp. Không sửa/tạo/xoá gì trong kho; tệp tạm nằm ở thư mục tạm hệ thống.

## A. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| CPR L06 | MUST | pitfalls (tiêu đề) | «Ba lỗi thường gặp, kể cả người đã đi làm» | Cùng cảnh liệt kê 4 lỗi («1. Quên free… 4. Không kiểm NULL»), lời đọc «có bốn lỗi rất dễ mắc», tên bài «4 lỗi kinh điển»; chapters.txt 03:09 in đúng «Ba lỗi…» | Đổi thành «Bốn lỗi…» | CONFIRMED |
| CPR L06 | SHOULD | quymo, say | «Nếu chỉ kiểm tra năm hoặc một trăm vòng lặp, lượng rò rỉ mới vài chục ki-lô-bai» | 5×1024 B = 5 KB; 100×1024 B = 100 KB; không số nào là "vài chục KB" | «mới 5 đến 100 ki-lô-bai» | CONFIRMED |
| CPR L06 | SHOULD | sym, pitfalls (mục tiêu 1, 3) | «Hai hàm xin cấp phát gồm hàm giữ nguyên rác cũ và hàm xoá sạch về không» | Không có mã/đầu ra nào cho thấy malloc để rác, dùng-sau-free hay free hai lần; 4 lỗi chỉ được liệt kê trong 3 câu (03:09–03:23, 14 s) | Thêm một ví dụ chạy cho mỗi lỗi | CONFIRMED |
| CPR L06 | SHOULD | sym | «free(p): Trả vùng nhớ về hệ thống»; «realloc … trả địa chỉ mới hoặc NULL»; «calloc … (tự kiểm tràn nhân)» | Khẳng định tuyệt đối: free trả về bộ cấp phát, realloc có thể trả chính địa chỉ cũ | Thêm điều kiện | PLAUSIBLE |
| MLP L08 | MUST | covers | «objective: 2 → scene: check»; «objective: 3 → scene: quymo» | Mục tiêu 3 (dùng TimeSeriesSplit) được dạy ở cảnh check; quymo là bảng quy mô/bẫy. Mục tiêu 2 (lỗi xáo trộn) chỉ nằm ở hook/pitfalls/quiz; cảnh check không chạy xáo trộn nào | obj3→check; obj2→pitfalls hoặc thêm cảnh chạy KFold(shuffle) | CONFIRMED |
| MLP L08 | MUST | example, check (say + show) | «Đầu ra hợp lý vì tham số và hàm mất mát vận hành đúng bất biến vừa nêu.»; «Ta chạy thực nghiệm này vì cần đo trực tiếp hành vi trên dữ liệu thật.»; «Phép kiểm chứng này rất quan trọng vì đối chiếu độc lập giúp phát hiện ngay sai lệch.»; «Đầu ra chạy thật (scikit-learn / PyTorch CPU)» | Câu rỗng với bài: bài không nói gì về hàm mất mát/bất biến; make_circles là dữ liệu tổng hợp; mã không dùng PyTorch | Thay bằng giải thích từng dòng mã | CONFIRMED |
| MLP L08 | SHOULD | mục tiêu 2 | «Hiểu lỗi chí tử khi xáo trộn ngẫu nhiên chuỗi thời gian» | Không có phép chạy hay con số nào cho thấy điểm bị thổi phồng khi xáo trộn; chỉ khẳng định bằng lời | Thêm so sánh có số | CONFIRMED |
| MLP L08 | SHOULD | hook (tiêu đề) | «Đặc trưng tương tác & kiểm chứng theo trục thời gian TimeS» | Tiêu đề bị cắt giữa chữ (chapters.txt 00:00) | Sửa | CONFIRMED |
| MLP L08 | SHOULD | quymo | «2 cột -> bậc 2 … 5 đặc trưng mới» | sklearn 1.9.1 cho ['x1','x2','x1^2','x1 x2','x2^2']: 5 cột gồm 2 cột gốc, chỉ 3 cột mới (5 150 cho 100 cột thì đúng) | «5 đặc trưng (3 mới)» | CONFIRMED |
| MLP L08 | SHOULD | prereq, pitfalls | «giúp hồi quy tuyến tính tách sạch ranh giới»; «Lỗi 1 (-30đ)»; «Tạo đặc trưng trượt trên toàn bảng» | Mô hình là LogisticRegression; «(-30đ)» không có thang điểm nào được giảng; «đặc trưng trượt/trung bình trượt» 0 lần ở MLP L00–L07; `factor`, `noise`, `stratify` không giải mã; «nếp» chỉ có ở L04 | Giảng tại chỗ | CONFIRMED |
| PRJ L04 | MUST | practice (tiêu đề + say) | «Tự cài đặt dự án và chấm tự động 100 điểm»; «chấm điểm tự động theo thang một trăm điểm chuẩn» | labs/cham.sh chỉ diff stdout với mong_doi.txt rồi in «ĐÚNG»/«KHÁC» (dòng 61–63), không có điểm; de.md không có thang chấm, ca biên, ba cỡ dữ liệu như labs/PRJ/SPEC.md §1–2 đòi | Bỏ «100 điểm» hoặc viết bộ chấm theo SPEC | CONFIRMED |
| PRJ L04 | MUST | example step 3, say | «đồng thời phép kiểm định cạnh âm hoạt động chuẩn xác khi đưa đồ thị lỗi vào» | Mã và đầu ra trên màn hình («min_cost=9 direct=15») không hề đưa đồ thị cạnh âm; lab lại đòi `neg_rejected=1` (cần try/except, không có trong bài) | Thêm phép thử cạnh âm kèm đầu ra | CONFIRMED |
| PRJ L04 | MUST | formula, say | «Vì đồ thị không chứa cạnh âm nên bước nới lỏng luôn giữ đường đi tối ưu bằng chín tại đích D. Bước nới lỏng cạnh liên tục giữ chi phí tối thiểu tới từng nút và trả kết quả bằng chín tại đích D.» | Hai câu liền nhau lặp cùng một ý | Bỏ một câu, thay bằng bảng nới lỏng từng nút | CONFIRMED |
| PRJ L04 | MUST | prereq, sym, formula, check | «Hàng đợi ưu tiên và phức tạp thuật toán (CS112)»; «Tối ưu bình phương tối thiểu tuyến tính (CS115)»; «bước nới lỏng»; «công thức hiệp phương sai» | Dijkstra và OLS không giảng tại chỗ: không có bảng chạy hàng đợi, công thức w, b chỉ nằm trong mã; nới lỏng/OLS/công thức đóng/hiệp phương sai không giải nghĩa. Bài dựa DMS:L20, CS112:L29, CS115:L44 (requires_ext) | Thêm một bảng chạy tay nếu giữ chuẩn mất gốc | PLAUSIBLE (thuộc thiết kế bài dự án) |
| PRJ L04 | SHOULD | quymo | «~660 000 phép (< 20 mi-li-giây)»; «> 2,4 × 10¹⁸ phép (treo vĩnh viễn)»; «khiến mọi siêu máy tính bó tay» | Số phép đúng ((V+E)·log₂V = 664 386; 20! = 2,43×10¹⁸), thời gian không nguồn: chính mã của bài trên đồ thị ngẫu nhiên 10 000 nút/40 000 cạnh đo 44,5–48,8 ms (5 lần, máy này); O(V!) là cận của đồ thị đầy đủ, không phải 60 cạnh | Ghi "số minh hoạ" hoặc đo thật | CONFIRMED (số phép); PLAUSIBLE (thời gian phụ thuộc máy) |
| PRJ L04 | SHOULD | hook, example | «mạng lưới thanh toán 4 nút trung gian»; «đồ thị bốn ngân hàng trung gian» | Đồ thị có 4 nút, chỉ B và C là trung gian (tiêu đề: «đi vòng 2 trạm») | «4 ngân hàng, 2 trung gian» | CONFIRMED |
| PRJ L04 | SHOULD | labs/PRJ/SPEC.md | «PRJ:L04 … hồi quy tìm tham số bằng Gradient Descent» | Bài và giáo án dùng công thức đóng | Sửa SPEC | CONFIRMED |
| PRJ L04 | SHOULD | pitfalls | «Lỗi 1 (-30đ)… Lỗi 2 (-20đ)… Lỗi 3 (-10đ)» | Không khớp thang 50/20/20/10 của SPEC; bộ chấm không trừ điểm | Bỏ | CONFIRMED |
| BNX L36 | SHOULD | sym | «MUST, SHOULD, MAY … phải, nên, có thể; thêm NOT là cấm» | SHOULD NOT theo RFC 2119 là "không nên", không phải cấm | «MUST NOT là cấm; SHOULD NOT là không nên» | PLAUSIBLE (không đọc lại RFC 2119 trong phiên) |
| BNX L36 | SHOULD | formula Bước 3, english | «cùng khoá, cùng nội dung … không làm lại, trả kết quả đã lưu»; «cùng khoá K1, lần hai: bỏ qua, trả kết quả cũ (cũng đã chạy)» | Mã của bài trả chuỗi «trung khoa, bo qua», không trả kết quả lần đầu «da chuyen» (đã dựng lại và chạy) | Nói rõ mã chỉ bỏ qua | CONFIRMED |
| BNX L36 | SHOULD | formula (bảng tín dụng) | «bảng luật cạnh»; «chuyển trạng thái kèm phiên bản» | Hai thuật ngữ không giải nghĩa trong bài | Thêm một dòng nghĩa | PLAUSIBLE |
| FND L10 | — | | không phát hiện lỗi kiến thức/số/mã | | | |
| FND L10 | SHOULD | toàn bài | — | Video 21,6 phút (có 90 + 420 s dừng), vượt chuẩn 9–16 phút | Tách phần dừng | CONFIRMED |
| FND L10 | SHOULD | practice | «Chép nguyên đoạn dữ liệu gd.csv (8 dòng chi tiêu, xem de.md)» | Dữ liệu vào không có trên video | Hiện 8 dòng | CONFIRMED |
| INT L08 | SHOULD | concept | «Hệ sinh thái Tín dụng Bán lẻ Tốc độ cao gồm 6 phân hệ cốt lõi»; «Sáu trụ cột … bao quát trọn vẹn vòng đời một khoản vay số» | Khẳng định tuyệt đối, ngược lời rào ở hook «không khẳng định ngân hàng nào có đúng sáu mảng này» | Sửa giọng | CONFIRMED |
| INT L08 | SHOULD | prereq (pháp lý) | «theo TT 31/2024/TT-NHNN (đối chiếu nguồn thứ cấp; thông tư này đã được TT 37/2025/TT-NHNN sửa đổi, cần đối chiếu bản hợp nhất)» | Khớp sổ nhưng cũ hơn sổ: registry ghi basis ORIGINAL, đã đọc nguyên văn 2026-11-18 rằng TT 37/2025 không sửa Điều 10 | Cập nhật câu rào | CONFIRMED so với registry; nguyên văn thông tư CHƯA KIỂM |
| INT L08 | SHOULD | quiz | «Xin mời bạn chọn quy trình hai pha đúng khi cấp hạn mức thấu chi cầm cố.» | Mục tiêu 6 chỉ được dạy trong đáp án quiz; 4 phương án không đọc lên, dừng 15 s; phương án C, D hiển nhiên sai | Dạy trước rồi mới hỏi | CONFIRMED |
| INT L08 | SHOULD | pitfall, quymo | «chờ tối đa 120 giây thì khoá ít nhất 240 giây»; «một máy 16 GB» | Hai số không gắn nhãn "số minh hoạ" (các số khác đều có) | Gắn nhãn | CONFIRMED |
| INT L08 | SHOULD | source (không lên hình) | «cafef.vn (bài 21/07/2026)» | Registry ghi Công báo 825+826 ngày 21-7-2024; có thể sai năm | Kiểm lại | PLAUSIBLE |
| INT L08 | SHOULD | toàn bài | — | 17,5 phút (có 345 s dừng), vượt 16 | — | CONFIRMED |
| CS115 L43 | MUST | recap step 1, say | «Nhiều thuật toán rút gọn lịch lấy mẫu ngày nay đã giảm từ một nghìn bước xuống còn hai mươi bước mà vẫn giữ ảnh rõ nét.» … «nhiều phương pháp lấy mẫu gia tốc gần đây đã rút ngắn xuống chỉ còn vài chục bước mà vẫn giữ chất lượng ảnh sắc nét.» | Lặp ý trong cùng một step; riêng cảnh recap 485/1 705 từ, 129 s trên một màn hình tĩnh 4 ô (khung 61, 72) | Cắt còn 4–5 câu | CONFIRMED |
| CS115 L43 | MUST | recap step 2, show + say | «tín hiệu ban đầu chỉ còn khoảng bốn phần trăm nghìn, nên huấn luyện ổn định»; «tín hiệu gốc tắt gần hết giúp huấn luyện ổn định» | Nhân quả sai và mâu thuẫn cảnh reverse («huấn luyện thường ổn định hơn (chỉ cực tiểu một hàm sai số…)»); ᾱ₁₀₀₀ ≈ 4,04×10⁻⁵ chỉ giải thích vì sao bắt đầu sinh từ nhiễu thuần | Bỏ vế «nên huấn luyện ổn định» | CONFIRMED (mâu thuẫn nội bộ) |
| CS115 L43 | MUST | practice step 3, show | «range(...) … Hàm/phương thức dựng sẵn thường dùng (sắp xếp, cực trị, ghép đôi, đánh chỉ số, làm tròn, lấy/thêm phần tử)»; «f"...{:.2e}, {:.6f}..." … (:.2f làm tròn 2 chữ số; !r giữ nguyên dấu nháy)» | Mô tả sai/vô nghĩa cho range; giải thích `:.2f`, `!r` trong khi mã dùng `:.2e`, `:.6f` (`.2e` không được giảng) | Viết bảng theo đúng mã | CONFIRMED |
| CS115 L43 | SHOULD | recap, say | «Chúc mừng bạn đã đi trọn vẹn bốn mươi tư bài học nền tảng…» | Step kế tiếp nói «Bài 45 là tình huống chuyên gia kết thúc lộ trình»; khoá còn L44–L46 | Bỏ | CONFIRMED |
| CS115 L43 | SHOULD | recap, say | «ứng dụng mạnh trong thiết kế phân tử thuốc mới và tổng hợp âm thanh chân thực»; «xuống còn hai mươi bước» | Không nguồn, không lên màn hình | Bỏ hoặc dẫn nguồn | PLAUSIBLE |
| CS115 L43 | SHOULD | covers | «objective: 1 → scene: hook» | Hook chỉ nêu ý trong 3 câu; cảnh dạy là sym_forward/noise_pic | Trỏ noise_pic | PLAUSIBLE |
| CS115 L43 | SHOULD | practice, say | «Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo (phần 2) để bạn tự đối chiếu cách viết.» | Đọc cả «(phần 2)»; bảng phần 2 chỉ có một dòng `print(...)` (khung 58) | Gộp | CONFIRMED |
| CSA L00 | MUST | covers | «objective: 2 → scene: verify»; «objective: 3 → scene: practice» | "byte = 8 bit, n bit → 2ⁿ" dạy ở sym và units; "kB khác KiB" dạy ở units; verify là tự kiểm đổi 200, practice là cảnh mở de.md | obj2→units, obj3→units | CONFIRMED |
| CSA L00 | MUST | practice + lab | «Mở labs/CSA/L00/de.md, cài đặt bằng C (C11)» | Bài và CSA L01–L02 không có dòng C nào (0 lần `printf`/`#include`); requires_ext chỉ DMS:L00; lời giải dùng `%02X`, `<stdint.h>`, `UINT8_MAX`; trong TRACKS.md chỉ một lộ trình đặt CPR trước CSA | Đổi lab sang giấy bút/Python hoặc dạy C trước | CONFIRMED |
| CSA L00 | SHOULD | hook | «Vậy số 47, chữ “A”, một điểm ảnh màu đỏ được lưu thế nào?» | Bài chỉ trả lời cho số; chữ và màu không được giảng | Bỏ hoặc thêm một dòng | CONFIRMED |
| CSA L00 | SHOULD | practice, de.md | «1 KiB = 1 024 byte, còn 1 KB = 1 000 byte» | Bài và mục tiêu viết «kB» | Thống nhất kB | CONFIRMED |
| NET L11 | MUST | covers | «objective: 2 → scene: verify»; «objective: 3 → scene: practice» | "Giải thích tăng cộng – giảm nhân" dạy ở why và example; "hai cách phản ứng" dạy ở example; verify là quy tắc tự kiểm, practice là cảnh mở de.md | obj2→why, obj3→example | CONFIRMED |
| NET L11 | MUST | labs/NET/L11/de.md | «mô phỏng 6 RTT đầu theo cơ chế AIMD (tăng cộng – giảm nhân: tăng gấp đôi đến ngưỡng 16 rồi tăng cộng lên 17)» | Gọi pha nhân đôi (khởi động chậm) là AIMD, ngược Lỗi 1 của chính bài | Viết «khởi động chậm tới ngưỡng 16 rồi tăng cộng» | CONFIRMED |
| NET L11 | SHOULD | practice, de.md | «AIMD …: tăng tuyến tính khi ổn, giảm nửa khi mất gói»; «ssthresh = cwnd // 2» | Sự kiện của lab là hết giờ chờ (cửa sổ về 1), không phải giảm nửa; `cwnd`, `ssthresh` và 17 // 2 = 8 (số lẻ) chưa có trong bài | Dùng từ của bài | CONFIRMED |
| ROB L05 | SHOULD | hook, say | «Hôm nay ta học lọc Kalman mở rộng với tên viết tắt trên bảng» | Màn hình hook không có chữ viết tắt nào; «EKF» chỉ hiện ở cảnh practice và recap | Thêm «(EKF)» | CONFIRMED |
| ROB L05 | SHOULD | quiz, say | «Đáp án câu một, chỉ cột thứ ba thay đổi… Đáp án câu một, sin 90 độ bằng 1…»; «Câu hai, hàng một của F… Câu hai, phương sai theo trục x…» | Lặp lời dẫn hai lần trong cùng step | Gộp | CONFIRMED |
| ROB L05 | SHOULD | recap, show | «Hai mức quy mô: … lệch 60° sai 20,9% khiến EKF phân kỳ nếu thiếu nhiễu chuyển động.» | Ghép hai lỗi độc lập (Lỗi 1 tuyến tính hoá sai, Lỗi 4 thiếu nhiễu) thành một quan hệ nhân quả | Tách hai ý | PLAUSIBLE |
| ROB L05 | SHOULD | practice step 3 | «math (cos, sin) … (lượng giác, hàm ngược góc, đổi radian ra độ, lôgarit, lũy thừa)»; «f"...{:.3f}..." … (:.2f làm tròn 2 chữ số; !r…)» | Mã dùng `math.radians` (độ → ra-đi-an) và `:.3f`; bảng khuôn mẫu nói ngược/khác | Sửa theo mã | CONFIRMED |
| ROB L05 | SHOULD | lab, phạm vi bài | «quãng đi vh = 2.0 m»; tiêu đề «Lọc Kalman mở rộng cho robot» | Bài ký hiệu quãng đi là s; lab chỉ thay số vào hai công thức đã in sẵn trong de.md, không luyện P′ = F P Fᵀ; bài chỉ dạy bước dự đoán, không có bước cập nhật phép đo nhiều chiều (mục tiêu không hứa) | Thống nhất ký hiệu, mở rộng lab | CONFIRMED / PLAUSIBLE |

**Kiểm pháp lý và nguồn số (INT L08, BNX L36):**
- **INT L08:** hai văn bản được dẫn (TT 31/2024/TT-NHNN, TT 37/2025/TT-NHNN) đều có trong `audit/legal/registry.yaml`, trạng thái HIEU_LUC. Nhóm 2 = 10–90 ngày khớp ghi chú Điều 10 trong sổ; câu rào "đã bị sửa đổi, cần đối chiếu bản hợp nhất" có mặt đúng như sổ yêu cầu. Cloud CA không dẫn văn bản, có câu «khung pháp lý cần kiểm lại khi dẫn». Không văn bản nào nằm ngoài sổ.
- **INT L08, số nghiệp vụ/hiệu năng:** đều có nhãn minh hoạ/giả định/ví dụ (LTV 85%, DTI 50%, khoá 300 s, 3 triệu giao dịch, 10⁹ phép/s, 100 byte/bản ghi, mục tiêu 5 phút), trừ hai số ở bảng A.
- **BNX L36:** không dẫn văn bản pháp lý Việt Nam nào. Mười câu tiếng Anh khớp nguyên văn `audit/bnx/sources_l36.md` (10/10, so bằng mắt); bản gốc trên mạng CHƯA KIỂM. Mọi số đầu vào đều ghi «số minh hoạ»/«giả định».

## B+C+D. Điểm (1 dòng/bài)

| Bài | sha16 khớp | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Mất gốc | P9 | L1 | L2 | L3 | L4 | L5 | covers đúng (k/n) | Chỗ người mất gốc kẹt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CPR L06 | có | 5,5 (dừng 50 s; 912 từ) | 1 | 1 | 2 | 1 | 1 | 1 | 2 | GẦN (9) | 1 | 0 | 2 | 1 | 2 | 1 | 3/3 | Chương trình 13 dòng chỉ được đọc trong 2 câu; không thấy malloc để rác hay 3 lỗi còn lại chạy ra sao; đề lab không có trên video; lab là ví dụ đổi 4→3, 6→5, hai lệnh printf cũng qua bộ chấm; cách cài gcc CHƯA KIỂM (grep w64devkit/MinGW trong lessons/cpr: 0) |
| MLP L08 | có | 5,8 (dừng 50 s; 1 015 từ) | 1 | 1 | 1 | 1 | 1 | 1 | 2 | CHƯA (8) | 2 | 0 | 2 | 0 | 2 | 1 | 1/3 | 12 dòng sklearn không giải từng dòng; màn hình hook nói PolynomialFeatures trong khi lời kể chuyện dự báo doanh thu; «nếp», «đặc trưng trượt», «(-30đ)» không giảng; lab trùng 100% tham số ví dụ, video hiện đủ 3 dòng đáp án |
| PRJ L04 | có | 5,5 (dừng 50 s; 964 từ) | 1 | 1 | 2 | 1 | 1 | 2 | 2 | GẦN (10) | 1 | 0 | 1 | 0 | 2 | 1 | 3/3 | Dijkstra + heapq + OLS trong 5 phút, không bảng chạy tay; lab trùng đồ thị và 4 điểm của bài, de.md in sẵn cả 3 dòng; `neg_rejected` cần try/except chưa dạy trong bài; "100 điểm" không có thật |
| BNX L36 | có | 15,7 (dừng 190 s; 2 299 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 2 | 2 | 1 | 2 | 2 | 8/8 | Bảng tín dụng 6 dòng lướt trong khoảng 20 s; video hiện đủ 5 dòng đáp án nhưng số liệu mới và có «Nếu kẹt» |
| FND L10 | có | 21,6 (dừng 510 s; 2 297 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 1 | 2 | 1 | 2 | 2 | 7/7 | Dữ liệu gd.csv chỉ có trong de.md; máy thiếu sqlite3 thì bộ chấm báo KHÁC (de.md có cảnh báo) |
| INT L08 | có | 17,5 (dừng 345 s; 2 299 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 2 | 2 | 2 | 1 | 2 | 2 | 7/7 | Thứ tự hai pha chỉ học qua đáp án trắc nghiệm; lab giấy bút không có bộ chấm, đáp án hiện ngay sau lúc dừng |
| CS115 L43 | có | 9,9 (dừng 38 s; 1 705 từ, 485 ở recap) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | ĐỦ (13) | 2 | 1 | 2 | 1 | 2 | 1 | 4/4 (obj1→hook yếu) | 129 s cuối nghe lời độn trên màn hình tĩnh; bảng «viết trong mã» sai về range và `.2e`; video chiếu nguyên lời giải; β của lab (0,0002→0,015) không nằm trong dòng «Nhiệm vụ» |
| CSA L00 | có | 9,7 (dừng 38 s; 1 470 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 1 | 0 | 0 | 0 | 1 | 1 | 1/3 | Bài toán học làm tốt, nhưng lab đòi viết C khi chưa học dòng C nào; de.md in sẵn 3 dòng, số 47/0x2F/256/255 lấy nguyên từ bài |
| NET L11 | có | 9,4 (dừng 45 s; 1 465 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 1 | 0 | 2 | 0 | 2 | 1 | 1/3 | de.md in sẵn 3 dòng, dãy 1,2,4,8,16,17 trùng ví dụ; de.md gọi nhân đôi là AIMD; `cwnd`/`ssthresh` chưa xuất hiện trong bài |
| ROB L05 | có | 12,0 (dừng 45 s; 2 104 từ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | ĐỦ (14) | 1 | 1 | 2 | 1 | 1 | 1 | 3/3 (obj2→check yếu) | Phần chuẩn bị 3 phút 20 s rất dày (phương sai, ma trận, đạo hàm, Kalman một chiều); lab chỉ thay số vào hai công thức in sẵn, ký hiệu `vh` khác `s`; video chiếu nguyên lời giải |

**Quy ước chấm tôi đã dùng:**
- **Mất gốc:** GẦN = tổng P1–P7 từ 9 đến 11, không mục 0; CHƯA = từ 8 trở xuống.
- **L1:** 0 = video chỉ ghi "mở de.md" và hiện khuôn đầu ra; 1 = có đề nhưng thiếu dữ liệu vào; 2 = đủ đề, dữ liệu, khuôn.
- **L3:** 0 = đáp án in sẵn và số liệu trùng ví dụ; 1 = đáp án in sẵn nhưng số liệu khác; không bài nào đạt 2 vì `cham.sh` chỉ so stdout.
- **L5:** 1 = chỉ có lời giải; 2 = có gợi ý «Nếu kẹt» kèm lời giải.

**D. Câu khuôn mẫu (trích nguyên văn lời đọc):**
- **CPR L06:**
  - «Đến lượt bạn tự kiểm tra.» / «Dừng vi-đê-ô và trả lời.»
  - «Bây giờ đến phần bạn tự viết mã C và chấm thật trên máy. Bạn mở đề thực hành, viết lời giải vào tệp riêng, rồi mở cửa sổ dòng lệnh để chạy trình chấm biên dịch và đối chiếu kết quả. Hãy bấm tạm dừng và tự làm trước.»
  - «Màn hình hiện toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự.»
  - «Bài tiếp theo là bài 7, tìm hiểu chủ đề tiếp nối ngay phần vừa học. Hẹn gặp bạn ở bài sau.»
- **MLP L08:**
  - ba câu ở bảng A.
  - «Đây là nền tảng trực tiếp để thiết kế đường ống thực hành sạch và ổn định.»
  - «Bạn hãy rà soát từng lỗi trên trước khi chuyển sang phần tự làm bài tập thực hành trên máy.»
  - «Hãy kiểm tra lại hai câu hỏi chốt bài ngay dưới đây.»
  - «Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy bằng môi trường CPU chuẩn của kho. Bạn mở tệp đề bài, tự viết lời giải hoàn chỉnh vào tệp Python riêng rồi chạy lệnh chấm tự động để đối chiếu từng dòng kết quả với đáp án chuẩn. Hãy bấm tạm dừng video và tự tay cài đặt trước khi xem lời giải.»
  - «Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp chính xác từng ký tự. Nếu sai một chữ số hay sai nhãn khoá, bộ chấm tự động sẽ chỉ rõ dòng lệch để bạn sửa ngay.»
  - «Chuỗi tổng kết kết nối ba quy tắc bất biến bạn vừa tự tay thực chứng trên CPU qua ví dụ, kiểm chứng độc lập và bài tập thực hành. Hãy giữ chắc ba nguyên tắc này khi triển khai bất kỳ đường ống học máy nào ngoài thực tế.»
  - «Chúc mừng bạn đã hoàn tất trọn vẹn bài học máy thực hành trên CPU với đầy đủ bằng chứng số liệu và kiểm thử tự động.»
- **PRJ L04:**
  - «Giải thích hai chi tiết cài đặt quan trọng trong bộ giải đồ thị và ước lượng hồi quy.»
  - «Đến lượt bạn tự kiểm tra.» / «Bấm tạm dừng và trả lời.»
  - «Bây giờ đến phần bạn tự hoàn thiện mã dự án để chấm điểm tự động theo thang một trăm điểm chuẩn. Bạn mở tệp đề bài, đọc kỹ dữ liệu mẫu và chạy trình chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự triển khai trước.»
  - «Màn hình hiện đầy đủ các dòng kết quả đầu ra mà dự án của bạn phải xuất ra khớp từng ký tự.»
- **CS115 L43:**
  - «Bây giờ đến phần bạn tự thực hành và chấm thật trên máy. Hãy mở tệp đề bài, đọc kỹ dữ liệu vào cùng khuôn đầu ra cần in, tự viết chương trình rồi gõ lệnh dòng lệnh để tự chấm trước khi xem kết quả.»
  - «Đây là kết quả mong đợi khi chạy đúng bài làm, dùng để bạn đối chiếu từng dòng trên máy của mình.»
  - «Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo (phần 1) để bạn tự đối chiếu cách viết.»
  - «Cuối cùng là lời giải tham khảo bằng mã lệnh chạy ra đúng kết quả trên để bạn đối chiếu lại sau khi đã tự làm.»
  - Câu độn ở recap: «Hiểu chắc chuỗi chuyển tiếp chiều thuận lẫn chiều nghịch hôm nay cho bạn chìa khoá bước vào mọi kiến trúc sinh dữ liệu hiện đại.»; «Nhờ vậy bạn dễ dàng tự kiểm chứng công thức bằng đoạn mã ngắn gọn.»; «Cách tách bài toán phức tạp thành nhiều bước khử nhiễu nhỏ là tư duy thiết kế rất đáng học hỏi.»; «Ở hai mức quy mô, từ một bước nhỏ tới lịch một nghìn bước, …»
- **CSA L00 và NET L11 (giống nhau từng chữ):**
  - «Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy. Bạn mở đề bài, tự viết lời giải vào tệp riêng rồi chạy lệnh chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự làm trước.»
  - «Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự.»
- **ROB L05:** bốn câu practice giống CS115 (bỏ «(phần 1)»), thêm «Hai mức quy mô: sai góc nhỏ dưới 10 độ tuyến tính hoá khá đúng, còn lệch lớn hàng chục độ làm bộ lọc tuyến tính hoá lệch hẳn.»
- **BNX L36, FND L10, INT L08:** không thấy câu khuôn mẫu rỗng; cảnh practice có đề riêng của bài.

Đếm nguyên chuỗi trên 777 tệp `lessons/*/*.yaml` (grep một lần, chỉ để biết độ lan):

| Chuỗi | Số tệp |
|---|---|
| «Hai mức quy mô» | 380 |
| «làm tròn 2 chữ số; `!r` giữ nguyên dấu nháy» | 372 |
| «Hàm/phương thức dựng sẵn thường dùng (sắp xếp, cực trị…» | 215 |
| «chương trình của bạn phải in ra khớp» | 191 |
| «tìm hiểu chủ đề tiếp nối ngay phần vừa học» | 18 |
| «(-Nđ)» | 14 tệp MLP + 11 tệp PRJ |

## E. Thống kê

- **Bài có MUST:** 6/10 (CPR L06, MLP L08, PRJ L04, CS115 L43, CSA L00, NET L11).
- **Số phát hiện:** 14 MUST (CPR 1, MLP 2, PRJ 4, CS115 3, CSA 2, NET 2) và 34 SHOULD.
- **Mất gốc:** ĐỦ 7, GẦN 2 (CPR, PRJ), CHƯA 1 (MLP); cả ba bài chưa đủ đều thuộc khoá mới 5–6 phút.
- **covers:** 38/44 ánh xạ trỏ đúng cảnh; sai ở MLP L08 (2), CSA L00 (2), NET L11 (2).
- **Khung hình đã mở:** 45 (CPR 4, MLP 6, PRJ 4, BNX 7, FND 4, INT 4, CS115 4, CSA 4, NET 4, ROB 4). Không thấy chữ tràn/đè; sơ đồ SVG ở CPR/MLP/PRJ nhỏ, chỉ chiếm góc trên trái nhưng còn đọc được; recap CS115 là màn hình tĩnh.
- **Phép tính/mã đã chạy lại:** khoảng 24 khối lệnh, khoảng 140 phép kiểm số và đầu ra. Mọi số trên màn hình và trong lời đọc của 10 bài đều khớp, trừ các dòng ở bảng A.
- **Lời giải lab:**
  - 8/10 chạy trong thư mục tạm và khớp mong_doi.txt sau khi chuẩn hoá CR/LF như `cham.sh` làm: CPR và CSA (gcc 16.2), MLP (.venv-ml, sklearn 1.9.1), PRJ, BNX, CS115, NET, ROB.
  - INT là giấy bút: tính lại 5/5 dòng khớp.
  - FND: `loi_giai.sh` chưa chạy nguyên văn (máy không có sqlite3 dòng lệnh, luật cấm git); 5/6 dòng tính lại bằng Python sqlite3 + awk khớp, dòng `git log` CHƯA KIỂM.
- **ASR (dòng tổng, câu / gắn cờ):** CPR 48/4, MLP 47/3, PRJ 44/3, BNX 128/3, FND 143/8, INT 105/12, CS115 82/4, CSA 86/8, NET 80/3, ROB 95/11. Tất cả thiếu audio 0, chưa xem xét 0; phần lớn lý do ghi «NOT_VERIFIED bằng tai người».
- **CHƯA KIỂM:**
  - nghe âm thanh/xem mp4;
  - nguyên văn trực tuyến của RFC, Stripe, PostgreSQL, SRE và hai thông tư NHNN;
  - bài đứng trước chỉ đối chiếu qua giáo án và tiêu đề/mục tiêu, không đọc recap đầy đủ.

**Ba lỗi hệ thống quan trọng nhất (lặp ở từ 2 bài trở lên):**
1. **Bài tự làm không buộc phải làm, có nơi không làm được.**
   - Cảnh practice khuôn mẫu chỉ ghi "mở de.md" ở 5/10 bài (CPR, MLP, PRJ, CSA, NET).
   - de.md hoặc video in sẵn toàn bộ đầu ra và số liệu trùng ví dụ ở 4/10 (MLP, PRJ, CSA, NET).
   - `cham.sh` chỉ diff stdout, nên vài lệnh in là qua; PRJ còn tuyên bố "chấm tự động 100 điểm" không có thật.
   - CSA L00 đòi C khi khoá chưa dạy C.
   - CS115 và ROB chiếu nguyên lời giải kèm bảng «viết trong mã» khuôn mẫu sai với mã.
   - Chỉ BNX, FND, INT có đề trên video, số liệu mới và gợi ý «Nếu kẹt».
2. **`covers` gán theo khuôn vị trí chứ không theo nội dung.** Mục tiêu 2→verify/check và mục tiêu 3→practice/quymo ở CSA L00, NET L11, MLP L08 trỏ vào cảnh không dạy mục tiêu đó; CS115 trỏ mục tiêu 1 vào hook.
3. **Lời đọc độn/khuôn mẫu và các mảnh vá tự động gây sai hoặc mâu thuẫn.**
   - Câu rỗng ở MLP, câu lặp ở PRJ và ROB, tiêu đề «Ba lỗi» cho 4 lỗi ở CPR.
   - Recap CS115 độn 485 từ.
   - Dòng «Hai mức quy mô» vá thêm cho ra nhân quả sai ở CS115 và ROB.
   - Điểm trừ «(-30đ)» không có thang ở MLP và PRJ.
   - Ba bài khoá mới chỉ 5,5–5,8 phút, 912–1 015 từ (chuẩn 9–16 phút, 1 300–2 300 từ), nên mã 12–13 dòng chỉ được nói trong 2–3 câu.
