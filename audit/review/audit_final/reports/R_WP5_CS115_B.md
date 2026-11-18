# WP5 CS115 phần B (L12–L21, L44, L45, L46): đã đọc 13/13 bài (L45 chỉ lướt ngoài recap; L46 chưa có video dựng, chỉ có khung hình)

Người đọc độc lập. Chỉ đọc YAML + chạy mã/tính lại; không sửa tệp nào ngoài báo cáo này. Python: `.venv/Scripts/python`, numpy qua `labs/.venv-pyt`, sympy qua `.venv`.

## 1. Chuẩn xác — lỗi có bằng chứng

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L20 | MUST | gradient#0 (show) | `Rút gọn: $\\dfrac{\partial\,\text{BCE}}{\partial z} = \hat{y} - y$` | `\\dfrac` (hai gạch) trong khối `|` thành ngắt dòng + chữ "dfrac". Khung `out/CS115/L20/frames/00033.png` hiện `dfrac∂BCE∂z = ŷ − y`: công thức kết quả chính của bài không đọc được, lệch lời đọc "dự đoán trừ nhãn". | Đổi `\\dfrac` thành `\dfrac` | CONFIRMED (khung hình) |
| L19 | MUST | prereq#0 (say) | "cột đầu toàn số 1 nên w không chính là b" | Màn hình: `w_0 = b`. Người nghe nghe "w không chính là b" = phủ định, ngược nghĩa (chữ "không" là chỉ số 0 bị nuốt). | Nói "w chỉ số không chính là b" | PLAUSIBLE (đọc nghĩa câu, chưa nghe tai) |
| L19 | SHOULD | practice (show + say) + lab | "phạt L1 một hệ số: λ = 1, a = 3, 1/2, −2"; "Nếu kẹt: nếu |a| ≤ λ thì nghiệm 0, ngược lại a trừ λ" | Bài định nghĩa mục tiêu `(w−a)² + λ|w|` (ví dụ λ=2 cho nghiệm a−1, tức ngưỡng λ/2). Lab de.md lại dùng `(w−a)² + 2λ|w|`; màn hình bài tập không nói "2λ". Học viên theo công thức của bài sẽ ra 2,5 / 0 / −1,5, lệch mong_doi (2, 0, −1). | Ghi rõ "làm nhỏ (w−a)² + 2λ|w|" trên màn hình bài tập, hoặc thống nhất công thức | CONFIRMED (tính lại) |
| L16 | SHOULD | quymo#0, practice#0/#3 | "Tính $\Sigma$ tốn N·D² phép nhân"; "trung bình, $\Sigma$"; "Σ = (1/N)∑ d dᵀ" | Chính bài này quy ước hiệp phương sai viết **S**, còn Σ là ma trận giá trị kỳ dị (notation_note, step sym_svd#2). Hai cảnh cuối dùng lại Σ cho hiệp phương sai. | Đổi thành S | CONFIRMED |
| L46 | SHOULD | recap#1 (show) | "hồi quy tuyến tính (bài 18 sẽ học: …)" | L46 đứng cuối khoá, sau L18; "sẽ học" sai thì và `forward_ref` sai. Khung `L46/frames/00091.png` hiện đúng chữ này. | Đổi "bài 18 đã học" và bỏ forward_ref | CONFIRMED |
| L46 | SHOULD | example#0 (say) | "theo chiều ngược lại với lúc đầu, biết giá rồi đi tìm trọng số" | "lúc đầu" ám chỉ mở đầu bài 2 (đã biết trọng số, dự đoán giá); trong L46 không có cảnh nào như vậy, người học L46 độc lập không có chỗ tham chiếu. | Bỏ cụm "ngược lại với lúc đầu" hoặc nhắc nội dung bài 2 | CONFIRMED |
| L45 | SHOULD | recap#2 (say) | "Cảm ơn bạn đã theo học." / "bạn đã đủ nền…" | Lời kết khoá nhưng L46 nằm sau L45 (L46 đặt cuối khoá). | Chuyển lời kết sang L46 hoặc nói "còn một bài bổ sung" | CONFIRMED |
| L46 | SHOULD | det_area#0 | "Định thức có nghĩa hình học là diện tích hình bình hành" | Đúng là **giá trị tuyệt đối** của định thức; định thức âm vẫn có diện tích dương. Thiếu điều kiện. | Thêm "(lấy giá trị tuyệt đối)" | CONFIRMED |
| L46 | SHOULD | quymo#0 | "Với t bằng mười mũ âm mười sáu, máy coi một cộng t bằng một" | Đúng cho số thực 64 bit (`1+1e-16==1.0` đã chạy: True); không nói giả định kiểu số. | Thêm "với kiểu số thực thông dụng, lưu cỡ 16 chữ số" | CONFIRMED |
| L15 | SHOULD | quymo#0 (say) | "D nhân D cộng 1, chia 2" | Thiếu ngoặc: nghe thành D·D+1 rồi chia 2; đúng là D(D+1)/2. | "D nhân, mở ngoặc, D cộng 1, đóng ngoặc, chia 2" | CONFIRMED |
| L16 | SHOULD | quymo#0, compress#3 (say) | "ta lưu 50 nhân N cộng 784 số"; "K nhân N cộng D số" | Thiếu ngoặc: đúng là 50(N+784), K(N+D). | Đọc kèm "trong ngoặc" | CONFIRMED |
| L17 | SHOULD | quymo#0 (say) | "MAP … cho N cộng 1 chia N cộng 2" | Thiếu ngoặc: đúng là (N+1)/(N+2). | "N cộng 1, tất cả chia cho N cộng 2" | CONFIRMED |
| L12, L44 | SHOULD | L12 practice#0; L44 quymo#0 (say) | "50, 500 và 5 000 xác suất"; "gần 4 900 mẫu" | Số nhóm bằng dấu cách trong lời đọc (TTS có thể đọc rời từng nhóm). | Viết "5 nghìn", "bốn nghìn chín trăm" | CONFIRMED |
| nhiều bài | SHOULD (nhẹ) | các cảnh quymo/practice, đa số bài | "0,1", "0,2", "8,3", "0,7041", "99,9"… | Các cảnh còn lại viết "0 phẩy 1"; cảnh quymo/practice dùng dấu phẩy thập phân trong `say`. Không thống nhất, rủi ro TTS. Liệt kê: L12 quymo/practice, L13 quymo, L14 quymo/practice, L16 quymo, L17 quymo, L18 quymo, L19 quymo, L20 quymo, L21 quymo, L44 quymo/practice, L46 det_area/quymo. | Đổi sang "phẩy" | CONFIRMED |
| L17, L18, L21, L45 | SHOULD (nhẹ) | L17 quymo/practice/recap; L18 quymo/verify; L21 in_ai; L45 nhiều | "MAP", "Gradient Descent", "ROC", "AUC", "Adam", "eta" trong `say` | Chữ Latin ngoài âm tiết Việt đọc thành tiếng (MAP/ROC/AUC đọc theo chữ cái hay đọc từ không rõ). Header L17 đã tự ghi "không đọc MAP thành chữ cái" nhưng say vẫn có. | Thay bằng tên Việt hoặc phiên âm | CONFIRMED |
| L16 | SHOULD (nhẹ) | sym_svd#0 | "U, V có các cột trực chuẩn (xoay, có khi kèm phản chiếu)" | Với ma trận dữ liệu 4×2, U cỡ 4×2 không phải phép xoay; chỉ đúng khi U vuông. | Thêm "(dạng gọn: U không vuông)" | PLAUSIBLE |
| L16 | SHOULD (nhẹ) | hook vs quymo | "khoảng 89 200 số" so với "≈ 90 nghìn" (89 984) | Hook không tính D số trung bình, quymo có; không thống nhất con số. | Ghi chú ở hook | CONFIRMED |
| L46 | SHOULD (nhẹ) | toàn bài | "X chuyển vị", "ma trận đơn vị I_2", "ℝ^{N×D}" | Dùng mà không nhắc lại nghĩa; prereq chỉ ôn "nghịch đảo". Bài cuối khoá, có thể đứng riêng. | Thêm một dòng ôn chuyển vị, ma trận đơn vị | CONFIRMED |
| L02 | ghi nhận | L02 scenes inverse…practice | — | Kiểm theo yêu cầu "bài trước không viện nội dung chỉ có ở L46": L02, L03, L18 không tham chiếu L46; nhưng L02 vẫn giữ nguyên mẹo 2×2, ví dụ w=(2,1) và verify giống hệt L46 (L46 lặp lại ví dụ, chỉ thêm chứng minh, hình diện tích, ma trận gần suy biến, công thức hồi quy). Không phải lỗi, chỉ trùng lặp. | — | CONFIRMED |

Không phát hiện lỗi toán/số trong các bài còn lại: mọi số trên màn hình và lời đọc khớp tính lại (mục 6).

## 2. Bảng độ sâu

sha16 lúc đọc: tất cả khớp tệp hiện tại (đọc 2026-11-14). "Phút" lấy từ `_frames.txt` (L46 chưa có `_frames.txt`/mp4). L45 chỉ lướt, không chấm P1–P7.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L12 | 13f939aaac27498e | 11,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "xác suất" (hook, coin), tích khả năng = nhân vì độc lập; đạo hàm bài 6–8 | hook dùng "xác suất" chưa giảng (bài 13 mới dạy); `say` 5 000, 0,1 |
| L13 | b9db72b7541c6d07 | 12,1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "biến cố", "tính chất tuyến tính", "tổng có trọng số" | "biến cố" dùng mà không giới thiệu |
| L14 | 7fb0fde94dfe96e6 | 8,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | π và căn không giảng; "mật độ" qua cột | π (L14 sym_normal) không nói là gì; `say` 0,7041 |
| L15 | f2f0baab813e32d3 | 9,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "hạng" (quymo), "elip", vector riêng/trị riêng từ bài 5 | "hạng 4" chưa nhắc nghĩa; D(D+1)/2 thiếu ngoặc |
| L16 | bfdc0feadd8fa79f | 10,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "đặc trưng", "mẫu", "ma trận đơn vị" | Σ lẫn S ở quymo/practice; thiếu ngoặc K(N+D) |
| L17 | 24a90cddf9ab0dd0 | 9,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | tích phân/đạo hàm riêng từ bài 6, 14 | chữ MAP trong `say`; (N+1)/(N+2) thiếu ngoặc |
| L18 | 0374b28c5029649b | 10,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "hồi quy", "đặc trưng", "hàm lồi" (bài 11 không ôn) | Gradient Descent là chữ Latin trong `say` |
| L19 | eba223376aecd219 | 9,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "nhiễu" (dùng như đã biết) | "w không chính là b" ngược nghĩa; 2λ không nêu |
| L20 | 0b53159f63951c62 | 9,9 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "lồi" (bài 11) | công thức `\\dfrac` hỏng trên màn hình |
| L21 | b8e86abb65675a12 | 8,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | ROC/AUC chỉ nêu tên | chữ nhỏ ở hình cm_pic; ROC/AUC đọc chữ |
| L44 | 387e9e52a579d9f1 | 10,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | độc lập, Bernoulli (bài 13) | `say` "4 900"; hình CLT chữ nhỏ |
| L45 | 1df653f600aad250 | 16,7 | – | – | – | – | – | – | – | 1 | 2 | – | không chấm | — | không có lab/practice (chỉ quiz); recap kết khoá trước L46 |
| L46 | 4799dac2f9f69be5 | (chưa dựng) | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | "chuyển vị", "ma trận đơn vị", "lúc đầu" | "bài 18 sẽ học" sai thì; hook tham chiếu "lúc đầu" của L02 |

P1=2: 5/12 bài chấm (L17, L19, L20, L21, L44) = 42%. P8=2: 12/13 (L45 không có lab; L45 ngoài phạm vi nâng cấp). P9=2: 12/12 bài chấm (số liệu 2–4 mức quy mô trong mọi cảnh quymo).

## 3. Lab (tự làm trước, chấm bằng cham.sh, sau đó mới so loi_giai)

| Bài | Tự làm được | Thời gian ước | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L12 | có (ĐÚNG lần đầu) | ~10 ph | không | khớp 6/6 dòng |
| L13 | có | ~12 ph | không | 7/7 |
| L14 | có | ~12 ph | không | 9/9 |
| L15 | có | ~20 ph | in nhiều Fraction/ma trận đúng định dạng; nghịch đảo 2×2 tay | 9/9 |
| L16 | có | ~20 ph | định dạng danh sách Fraction | 7/7 |
| L17 | có | ~15 ph | không | 8/8 |
| L18 | có | ~20 ph | ghép chuỗi danh sách Fraction | 7/7 |
| L19 | có | ~15 ph | de.md nêu rõ 2λ|w|; màn hình bài tập thì không (người chỉ xem video sẽ ra 2,5/−1,5) | 6/6 |
| L20 | có | ~12 ph | không | 8/8 |
| L21 | phần → có sau sửa (lần 1 KHÁC) | ~12 ph | `print("…", x, ", do phu", y)` chèn dấu cách trước dấu phẩy → lệch 1 dòng; cham.sh chỉ đúng dòng | 7/7 (màn hình gộp thêm 2 dòng đề `that/doan`, phần kết quả khớp) |
| L44 | có | ~15 ph | không | 7/7 |
| L46 | có | ~20 ph | in ma trận Fraction như `[[3, -2], [-7, 5]]` phải tự ghép chuỗi (print mặc định ra `Fraction(3, 1)`) | 8/8 |
| L45 | không có lab | | | |

Đề đủ để tự làm; không có đáp số ghi sẵn trong de.md (mong_doi chỉ hiện ở cảnh "Kết quả mong đợi"). `loi_giai.py` của 12 bài đều chấm ĐÚNG. Cần biết trước: Python chặng 1 (f-string, vòng lặp, `Fraction`), ghép chuỗi danh sách thủ công.

## 4. Người học kẹt ở đâu (chỉ xem video này + bài trước)

- L12: hook#0 "Nhân 400 xác suất, mỗi cái bằng 0,1" — "xác suất" chưa được giảng; coin#0 "p·p·p·(1−p)" — vì sao nhân (độc lập) chưa nói.
- L13: product#1 "Hai biến cố gọi là độc lập" — "biến cố" chưa giới thiệu.
- L14: sym_normal#0 công thức chứa 2π và căn — π và căn không giảng; còn lại không kẹt.
- L15: quymo#1 "hạng là 4" — "hạng" không ôn ở bài; mahal#3 "elip" chưa nói là gì.
- L16: prereq#1 "phương sai của từng đặc trưng" — "đặc trưng" chưa định nghĩa; proof#1 "ma trận đơn vị".
- L17: không kẹt (mọi ký hiệu giảng tại chỗ).
- L18: hook#0 "hồi quy" không định nghĩa; normal_eq#0 "hàm lồi như bài 11" không ôn.
- L19: prereq#0 "w không chính là b" nghe ngược nghĩa; practice: không biết dùng 2λ.
- L20: gradient#0 — công thức kết quả hiển thị "dfrac∂BCE∂z" không đọc được.
- L21: không kẹt.
- L44: không kẹt.
- L45: không chấm (lướt).
- L46: example#0 "ngược lại với lúc đầu" không có chỗ tham chiếu; recap "X chuyển vị" không giảng.

## 5. Số đã tính lại / mã đã chạy

- Python/numpy/sympy chạy lại ~130 con số và khẳng định (hook, bảng, lỗi thường gặp, quymo, practice của cả 12 bài chấm): tất cả khớp, 0 sai. Gồm: L12 tràn dưới (0,1^400=0.0, 0,1^300=1,000e-300; tổng ln −23,03/−690,78/−921,03/−230258,51); L13 Bayes 1/12, 8,33/0,89/0,09 %, 0,2794/0,0367; L14 quy tắc 68-95-99,7, tổng cột 0,7041/0,6835/0,6827, 3 169 năm, mô phỏng 0,684/0,955/169,99/7,0; L15 ma trận Σ, Mahalanobis² (2, 2), 0,0796/0,0293, mô phỏng, hạng 4/10, D(D+1)/2; L16 89 984, 8,7×/15,7×, 0,6 s/10,2 phút; L17 sai số chuẩn, ln khả năng −6,748/−8,3178; L18 w=(0,5; 1,4), GD 2000 bước, 47/30 và MSE 0,0917, bảng ND²/200ND; L19 bảng bậc 1/3/5 (0,194/0,054; 0,118/0,039; 0/0,832), 5 mức λ, 3 mức N; L20 σ, BCE, 75×, e^700, tràn 710; L21 ngưỡng, F1 9/59, sai số chuẩn; L44 P(tổng=35)=0,0727 vs 0,0739, phủ 0,9503 và 94,7 % (Wald, n=1000, p=0,85), 545/4899/489804, khoảng ghép cặp; L46 det/‖M⁻¹‖/nghiệm đổi, 1+1e-16==1.
- Lab: tự viết 12 bài, cham.sh ĐÚNG 11/12 lần đầu (L21 lệch dấu cách do cách in), 12/12 sau sửa; loi_giai 12/12 ĐÚNG; mong_doi so với màn hình 12/12 khớp.
- Dò ký tự điều khiển (`\t`, `\f`, TAB, formfeed) trong toàn bộ chuỗi YAML 13 bài: 0 trường hợp.

## 6. Khung hình đã xem

Dựng bảng 6 khung (mở đầu, ví dụ/hình cơ chế, kiểm tra, tự làm, tổng kết) từ `out/CS115/Lxx/frames` cho cả 13 bài và đọc từng bảng. Khung dùng: L12 00001/00033/00059/00081/00108/00128; L13 00001/00034/00061/00084/00112/00132; L14 00001/00026/00047/00065/00086/00101; L15 00001/00027/00049/00068/00090/00106; L16 00001/00028/00050/00070/00092/00109; L17 00001/00027/00049/00068/00091/00107; L18 00001/00029/00053/00073/00097/00115; L19 00001/00027/00048/00066/00088/00104; L20 00001/00029/00052/00072/00095/00113 và 00033; L21 00000/00024/00044/00061/00081/00096; L44 00001/00026/00047/00065/00086/00102; L45 00001/00034/00062/00085/00113/00133; L46 00000/00023/00042/00058/00077/00091 (L46 chỉ có khung, chưa có mp4/_frames.txt/srt, nên chưa so được lời đọc thật).
Lỗi hiển thị: L20 00033 (`dfrac∂BCE∂z`, ở mục 1). Còn lại: nửa dưới màn hình trống ở hầu hết khung (bố cục); hình SVG nhỏ, chữ khó đọc ở L21 cm_pic và L44 clt; L44 compare đoạn văn dày chữ nhỏ. Chữ ở L16/L18/L19/L46 đọc được, không tràn, không đè.

## 7. Nhận xét chung

- Ngưỡng chốt: MUST 0 → KHÔNG đạt (2: L20 hiển thị công thức chính, L19 câu đọc ngược nghĩa; cả hai sửa một dòng). P1=2 ≥90% → KHÔNG đạt (5/12). P8=2 100% → đạt cho 12/12 bài có lab; L45 không có lab (ngoài phạm vi nâng cấp).
- Toán và số liệu rất sạch: không sai số nào trong ~130 phép tính; mọi lab chấm ĐÚNG.
- Vấn đề lặp lại là P1: xác suất/biến cố (L12, L13), π (L14), hạng/elip (L15), đặc trưng (L16), hồi quy/hàm lồi (L18). Mỗi chỗ chỉ cần 1–2 câu giảng tại chỗ.
- Cảnh quymo/practice mới thêm dùng dấu phẩy thập phân và số nhóm cách; nên chuẩn hoá theo "phẩy" như các cảnh cũ.
- Biểu thức có phép cộng-chia trong `say` (L15, L16, L17) thiếu ngoặc đọc thành tiếng.
- L46 tự đủ về toán và thực nghiệm (P8, P9 tốt, số khớp), L02/L03/L18 không viện nội dung chỉ có ở L46; còn lại là chỗ nối thứ tự: "bài 18 sẽ học", "lúc đầu", kết khoá ở L45 trước L46.
