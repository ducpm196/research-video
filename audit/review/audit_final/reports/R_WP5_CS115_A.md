# WP5 CS115 phần A (L00-L11): đã đọc 12/12 bài

Người đọc độc lập, 2026-11-14. Tiêu chí: BRIEF_READ_S01 + BRIEF mẫu F + ADDENDUM (P8, P9) + yêu cầu CS115 (bài tự đủ về ký hiệu toán). Không sửa tệp nào ngoài báo cáo này. Không mở báo cáo/handover/plan cũ.

## 0. Kết luận ngưỡng chốt

| Ngưỡng | Kết quả | Đạt? |
|---|---|---|
| MUST = 0 | 1 MUST nội dung (L06) + 1 chặn pipeline (12/12 video dựng từ bản đặc tả cũ, thiếu cảnh quymo và practice) | KHÔNG |
| P1 = 2 ở >= 90% bài | 9/12 = 75% (L03, L05, L06 chấm 1) | KHÔNG |
| P8 = 2 ở 100% bài | 12/12 (cả 12 bài có lab, số khác ví dụ, có kết quả mong đợi; 12/12 lab chấm ĐÚNG) | ĐẠT |
| P9 (tham khảo, không có ngưỡng) | 12/12 = 2 (L00-L11 đều có cảnh quymo số liệu >= 2 mức + giả định ghi rõ, trừ lỗi nhỏ L05) | |

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

Cú pháp tệp: `lessons/cs115/<bài>.yaml:<cảnh>`.

| Bài | Mức | Cảnh | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L06 | MUST | quiz (bước 3) và objectives | show: "với $x^2 + 4y^2$ (lỗi 4)"; say: "còn với hàm của lỗi thứ tư chúng là hình bầu dục"; objective 5: "nhận ra 4 lỗi thường gặp" | Cảnh `pitfalls` chỉ có 3 lỗi (title "3 lỗi người mới hay mắc") và không có hàm $x^2+4y^2$ nào. Màn hình và lời đọc viện dẫn "lỗi 4" không tồn tại; mục tiêu hứa 4 lỗi, bài dạy 3. (Video đã dựng còn bản cũ có chương "4 lỗi", nên khi dựng lại sẽ lệch.) | Hoặc thêm lại Lỗi 4 (gradient của $x^2+4y^2$ tại (2,1) không chỉ về đáy: (4,8) so với (-2,-1)), hoặc sửa quiz thành "hàm $x^2+4y^2$ (không dạy ở bài này)" và objective thành "3 lỗi". | CONFIRMED |
| 12 bài | MUST (pipeline) | out/CS115/Lxx/ | `build_report.json: spec_sha256` khác sha256 YAML hiện tại ở cả 12 bài; `chapters.txt` thiếu chương quymo và practice (L00: 14 chương so với 16 cảnh; L06: 15 so với 16, vẫn có chương "Gradient sẽ dùng ở đâu", "4 lỗi") ; `L00.srt` còn câu "đúng như hình cái bát cho thấy" không có trong YAML | Video người học xem không chứa cảnh số liệu quy mô (P9) và cảnh tự làm/lab (P8); phần P8, P9 ở bảng dưới chỉ đúng với YAML, chưa đúng với video. Frame đã xem thuộc bản dựng cũ. | Dựng lại (build, tts, render) 12 bài sau khi sửa; đối chiếu lại `chapters.txt` với danh sách cảnh. | CONFIRMED (so chương/cảnh, so srt) |
| L01 | SHOULD | quymo (bước 2, say) | "vì số cặp tăng theo bình phương, nên với dữ liệu lớn người ta phải nén vector bớt chiều" | Suy luận lệch: nén bớt chiều chỉ giảm hằng số 784 trên mỗi cặp, không đổi tăng trưởng N(N-1)/2. Hướng thực tế để tránh bình phương: lấy mẫu, tìm láng giềng gần đúng. | Đổi thành "nên người ta tránh so mọi cặp: chỉ so với một phần dữ liệu, hoặc nén để mỗi cặp rẻ hơn" | CONFIRMED |
| L01 | SHOULD | pitfalls | show "Lỗi 1." rồi "Lỗi 3."; title "2 lỗi người mới hay mắc" | Nhãn nhảy 1 sang 3 (thiếu Lỗi 2); say cũng "Lỗi thứ ba". | Đánh lại số 1, 2 | CONFIRMED |
| L01 | SHOULD | lab (de.md) | liệt kê đủ cả 9 dòng kết quả: `tu so: 15 ... c = 11/17`, `hinh chieu: [44/17, 11/17]` | Lab ghi sẵn toàn bộ đáp số, người học có thể in chay. | Chỉ nêu dạng dòng (`tu so: <số>`), bỏ số | CONFIRMED |
| L00, L02, L08, L10, L11 | SHOULD | lab (de.md) | L00: `w=2 P=16 Q=121 tong=137`; L02: `[[2, 8], [7, 19]]`; L08: dòng f1 đầy đủ `(2, -1) ... 2 va 3 ... day`; L10: `SGD: x=0.8306 y=0.0001 f=0.6899` và `buoc dau Adagrad moi toa do: 0.1`; L11: `gradient sau Newton: [0, 0]` | Mỗi lab ghi sẵn một phần đáp số (dòng mẫu trùng đúng kết quả thật). | Đổi dòng mẫu bằng số khác (vd `w=9 P=... `) hoặc chỉ nêu dạng chữ | CONFIRMED |
| L02 | SHOULD | inverse | "đổi chỗ, đổi dấu rồi chia cho con số a d trừ b c" | Công thức tổng quát chỉ thử trên ví dụ định thức 1 (N·M = I); không cho thấy vì sao phải chia cho ad-bc (N·M = (ad-bc)I). Ngoài ra bài không có ví dụ số giải Mw = b bằng tay, chỉ có ở lab. | Thêm 1 bước: nhân N với M tổng quát ra (ad-bc)I; thêm 1 ví dụ w = M⁻¹b | CONFIRMED |
| L03 | SHOULD | quymo (bước 1) | "Cách cũ, khai triển định thức, cần cỡ n! phép nhân" | "Khai triển định thức" (định thức n x n, dùng để giải hệ) chưa từng được giảng (bài 2 chỉ có ad - bc). Người mất gốc không biết cách cũ là gì. | Thêm 1 câu: định thức n x n tính bằng khai triển theo hàng, mỗi lần bỏ một hàng một cột, nên cỡ n! | CONFIRMED |
| L03, L05 | SHOULD | quymo (say) | L03: "Với 20 ẩn khử cần 2 660 phép"; L05: "Tỉ số 0,99 cần 1 375 lần" | Số nhóm bằng dấu cách trong lời đọc (TTS đọc thành hai số). | Viết liền "2660", "1375" hoặc "hai nghìn sáu trăm sáu mươi" | CONFIRMED (quét regex toàn bộ say: chỉ 2 chỗ) |
| L04 | SHOULD | gsk, pitfalls | (không có) | Thiếu điều kiện áp dụng: Gram-Schmidt cần đầu vào độc lập tuyến tính, nếu không có v_k = 0 và bước chuẩn hoá chia cho 0. Ghi chú đầu tệp (audit A20) hứa nêu nhưng màn hình và lời đọc không có. | Thêm 1 dòng ở gsk hoặc 1 lỗi ở pitfalls: x₃ = x₁ + x₂ thì v₃ = 0 | CONFIRMED (grep) |
| L05 | SHOULD | quymo (bước 2) | show: "1 375 triệu ≈ 1,4 giây"; say: "tổng khoảng một tỉ rưỡi phép, chừng 1,4 giây" | Giả định "máy làm 1 tỉ phép/giây" không ghi ở cảnh này (các bài khác đều ghi). "Một tỉ rưỡi" lệch 1,375 tỉ, không khớp 1,4 giây. | Thêm dòng "máy làm 1 tỉ phép/giây (số minh hoạ)"; đọc "khoảng một tỉ bốn" | CONFIRMED |
| L05 | SHOULD | practice | "delta âm", "biệt thức", "vết" | "Biệt thức/số chính phương" dùng ở lab và "Nếu kẹt" nhưng chưa giảng (bài dùng cách tổng-tích hai nghiệm). "Vết" chỉ định nghĩa bằng công thức ở bảng. | Thêm 1 câu giảng biệt thức (b² - 4ac), hoặc cho lab dùng cách thử nghiệm nguyên | PLAUSIBLE |
| L06 | SHOULD | rules (say) | "suy ra cùng cách nhờ khai triển nhị thức" | "Khai triển nhị thức" chưa giảng. | Bỏ cụm này hoặc giải thích "(x+h)ⁿ = xⁿ + n xⁿ⁻¹ h + ..." | CONFIRMED |
| L07 | SHOULD | meaning_j | "Dự đoán: J h = (0,5; 0,9)" | Cảnh không đặt cạnh thay đổi thật f(1,1; 2,1) - f(1,2) = (0,541; 0,91) (tôi tính lại), nên chưa "thử bằng số" như lời hứa; lab mới có. | Thêm dòng "thật: (0,541; 0,91)" | CONFIRMED |
| L08 | SHOULD | example, verify | "là giá trị nhỏ nhất của hàm" (objective 5: "chứng minh là điểm thấp nhất trên toàn mặt phẳng") | Kết luận toàn cục không có lập luận trên màn hình: verify ghi f(x*+h) = -1/3 + ½hᵀHh với dấu "=" nhưng không giải thích vì sao đúng (hàm bậc hai) và vì sao ½hᵀHh >= 0 cho mọi h. Tiêu chuẩn 3 biến chỉ phát biểu, không suy ra. | Thêm 1 câu: hàm bậc hai nên khai triển đúng; Hessian dương nên hạng thêm luôn >= 0 | CONFIRMED |
| L11 | SHOULD | quymo | "Gradient Descent, đủ bước: 173 bước ... 6 908 bước" | Số bước dùng tốc độ học tối ưu η = 2/(λmax+λmin) và ngưỡng 10⁻⁶ (tôi tính lại: ((κ-1)/(κ+1))^k < 10⁻⁶ cho 173 và 6908 đúng), nhưng cả hai giả định không ghi. | Ghi "η tốt nhất, sai số còn 10⁻⁶" | CONFIRMED |
| L11 | SHOULD | convex (svg phải) | đường w⁴ - 2w² vẽ có đỉnh nhọn ở giữa | Hàm trơn, đỉnh giữa phải tròn (khung hình 00013 thấy chóp nhọn). Không sai kiến thức nhưng lệch hình. | Vẽ lại bằng đường cong trơn | CONFIRMED |
| 12 bài | SHOULD | quiz | `pause: 8` cho câu tự làm 3 ẩn (L03), Gram-Schmidt (L04), ... | 8 giây không đủ; lời nhắc "dừng video" bù lại nên chỉ là SHOULD. | Tăng pause hoặc bỏ pause | PLAUSIBLE |

Bài không còn phát hiện khác: L09, L10 (ngoài lỗi lab chung): không phát hiện lỗi kiến thức.

## 2. Bảng độ sâu

Phút = thời lượng video đã dựng (BẢN CŨ, chưa gồm quymo và practice; riêng practice thêm 150-360 giây pause). sha16 = lúc đọc, trùng danh sách giao.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1-P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8e4524ee1fd24e29 | 12,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | lab de.md lộ dòng w=2 |
| L01 | 1675fd309d377b21 | 19,1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 13 | ĐỦ | định lý Pytago (nhắc tên, không giảng lại) | vì sao dấu tích vô hướng cho biết góc chỉ phát biểu; quymo kết luận lệch; lab lộ đáp số |
| L02 | fc7c159c53f8e2f3 | 19,2 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 12 | ĐỦ | không | công thức nghịch đảo 2x2 không rõ vì sao chia ad-bc; không có ví dụ số Mw = b trong video |
| L03 | 0dd8cbb0e2a886d1 | 12,1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "khai triển định thức" | quymo dùng khái niệm chưa giảng |
| L04 | c48abbb619290cf1 | 15,0 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 13 | ĐỦ | không | thiếu điều kiện đầu vào độc lập tuyến tính |
| L05 | 6c160f5669ebf8f5 | 15,6 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | biệt thức bậc hai, số chính phương (lab) | giả định thời gian quymo; biệt thức |
| L06 | ed92dd80290e8a92 | 15,1 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | khai triển nhị thức | tham chiếu "lỗi 4" không tồn tại; objective 4 lỗi, bài 3 lỗi |
| L07 | 8d6895b0b41977d0 | 15,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | meaning_j chưa đối chiếu số thật |
| L08 | 82d73201c45e597f | 14,4 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 13 | ĐỦ | không | kết luận cực tiểu toàn cục không lập luận; lab lộ f1 |
| L09 | 0d31be835e0253a6 | 12,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | không |
| L10 | ae3dbaa4e1545459 | 11,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | lab lộ dòng SGD |
| L11 | 8aafe740ec1fae70 | 10,5 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | không (phần dư, JᵀJ giảng ngắn) | hình hàm không lồi có chóp nhọn; giả định số bước GD |

Ghi chú điểm: tổng đều >= 12 và không mục nào 0 nên mọi bài "ĐỦ" cho người mất gốc; hai ngưỡng không đạt (MUST, P1) nằm ở bảng 0.

## 3. Lab (làm như người học: đọc de.md, tự viết ở thư mục tạm, chấm bằng cham.sh, sau đó mới so loi_giai)

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L00 | có | video pause 150 s | không (dòng mẫu trong de đã lộ w=2) | ĐÚNG |
| L01 | có | 240 s | không (de lộ toàn bộ kết quả) | ĐÚNG |
| L02 | có | 300 s | phải nhân ma trận tổng quát bằng vòng lặp lồng; đề đủ | ĐÚNG |
| L03 | có | 300 s | đề đủ nhưng phải tự cài khử Gauss với Fraction và đổi chỗ hàng; bước nặng nhất của cả 12 lab | ĐÚNG |
| L04 | có | 360 s | "bóng của x3 trên v1 và v2": phải tính hệ số riêng trên từng v (đề đủ) | ĐÚNG |
| L05 | có | 300 s | phải biết căn nguyên (math.isqrt) hoặc gần đúng và gcd; đề nêu công thức nhưng "số chính phương" chưa giảng | ĐÚNG |
| L06 | có | 300 s | không | ĐÚNG |
| L07 | có | 360 s | nhân hàng với ma trận bằng mã; đề đủ | ĐÚNG |
| L08 | có | 360 s | giải điểm dừng bằng nghịch đảo 2x2 (đề chỉ dẫn "công thức nghịch đảo") | ĐÚNG |
| L09 | có | 300 s | không | ĐÚNG |
| L10 | có | 360 s | thứ tự cập nhật G trước khi tính bước (đề và "Nếu kẹt" đã nêu) | ĐÚNG |
| L11 | có | 300 s | giải Ap = gradient bằng Fraction (đề đủ) | ĐÚNG |

12/12 lời giải tự viết khớp mong_doi lần chạy đầu; chưa mở loi_giai.* (không cần). Thời gian của tôi không đại diện (viết dưới 1 phút); cột thời gian là pause trong video.

## 4. Người học kẹt ở đâu

| Bài | Chỗ đầu tiên không theo được |
|---|---|
| L00 | không kẹt |
| L01 | không kẹt trong video; quymo bước 2 "nén vector bớt chiều" khó hiểu vì sao giải quyết bình phương |
| L02 | inverse bước "đổi chỗ, đổi dấu rồi chia cho con số a d trừ b c": không rõ vì sao chia |
| L03 | quymo bước 1 "Cách cũ, khai triển định thức, cần cỡ n! phép nhân" |
| L04 | không kẹt |
| L05 | lab: "Tính delta ... nếu delta là số chính phương" (biệt thức chưa dạy); video không kẹt |
| L06 | rules: "khai triển nhị thức"; quiz: "(lỗi 4)" không có |
| L07 | không kẹt |
| L08 | sylv3: phát biểu tiêu chuẩn 3 biến chỉ tiếp nhận, chưa có lý do ("Ba định thức con là 2, 3 và 6 ... là đáy") |
| L09 | không kẹt |
| L10 | không kẹt |
| L11 | alternatives: "H ≈ JᵀJ (Jacobian của phần dư)" giảng ngắn, nhiều khái niệm mới trong một bước |

## 5. Số đã tính lại / mã đã chạy

- Lab: 12 chương trình tự viết, chạy bằng `labs/cham.sh`: 12/12 ĐÚNG.
- Mô phỏng numpy (labs/.venv-pyt): L10 so sánh Adagrad/RMSprop/Adam hai mức η (6 số): khớp màn hình (7,97; 0,027; 0,15; 0,0003; 0,009; 0,85); Nesterov so Momentum 30 bước (4,81/0,60 và 4,06/0,13): khớp.
- Tính lại bằng tay/Python từng con số trên màn hình và lời đọc cho cả 12 bài (các bảng quymo, các ví dụ từng bước, quiz, pitfalls, hình SVG: toạ độ điểm khớp số): khoảng 330 số/phép tính, khớp tất cả trừ các mục ở bảng 1 (không có lỗi số học). Đã đọc và đối chiếu, không chạy lại các dòng `checks:` trong YAML.
- Quét tự động say/show: không có ký tự điều khiển (TAB, formfeed), không có chữ ngoài âm tiết Việt (byte, epoch, delta, loss) trong say; 2 chỗ số nhóm bằng dấu cách trong say (L03, L05).
- Công thức khớp lời đọc: không phát hiện lệch; chỗ lời đọc bỏ cận Σ (L01 dot) vẫn nằm ở bài giảng Σ trước đó.

## 6. Khung hình đã xem và lỗi hiển thị

Ít hơn yêu cầu (17 khung thay vì 60): L00 00007, 00080, 00103; L01 00070, 00123; L02 00069, 00117; L03 00055; L04 00081; L05 00045; L06 00088; L07 00098; L08 00081; L09 00037; L10 00024, 00036; L11 00013. Tất cả thuộc bản dựng cũ.
Lỗi hiển thị: không chữ tràn/đè; L00 00080 nhãn "w = 3,4: tổng 0,16" sát nhãn trục "3,4" nhưng đọc được; L10 00024 hình chỉ chiếm nửa trái khung (chữ nhỏ so với phần trống); L11 00013 đỉnh nhọn (xem bảng 1). Cảnh SVG khác (L01 phép chiếu, L05 ba hướng, L08 yên ngựa, L09 đường cong) kiểm bằng toạ độ trong mã (tính lại khớp lời đọc) chứ chưa xem khung.

## 7. Nhận xét chung

- Chuẩn xác kiến thức rất tốt: không tìm thấy lỗi định lý, công thức, số học hay trích dẫn (nguồn Adam, Adagrad, RMSprop, Adadelta, gradient liên hợp, Levenberg-Marquardt khớp tên, năm, trang) trong 12 bài.
- Điểm nghẽn lớn nhất là hạ tầng: video chưa dựng lại sau các đợt sửa, nên P8 (lab) và P9 (quy mô) chỉ có trên giấy.
- Lỗi nội dung duy nhất cần chặn: tham chiếu "lỗi 4" ở L06.
- Lab rò đáp số ở 6 bài (L00, L01, L02, L08, L10, L11): sửa nhanh bằng cách thay số mẫu trong de.md.
- P1 tụt vì ba thuật ngữ dùng mà chưa giảng (khai triển định thức, biệt thức, khai triển nhị thức); mỗi chỗ sửa một câu.
- Các bảng quymo (P9) làm tốt và nhất quán: giả định "1 tỉ phép/giây" ghi ở 11/12 bài (thiếu ở L05); số liệu 2-4 mức quy mô, có kết luận người làm nghề.
- Chuỗi bài tự đủ: viện dẫn bài trước đều nằm trong CS115 và có ôn tại chỗ; không phát hiện viện "khoá khác" cho khái niệm cốt lõi.
