# findings_LS1: sổ phát hiện của 9 người đọc độc lập, kèm kết luận của người điều phối

Trạng thái:
- `TODO` = chưa xử lý;
- `FIXED` = đã sửa, đã kiểm lại trên tệp;
- `REJECTED` = bác, có ghi lý do;
- `KEPT` = giữ, có ghi lý do.

Mức: MUST / SHOULD / BT = BLOCK-TERM / BS = BLOCK-STEP / BQ = BLOCK-QUIZ.

## CS115 L00–L11 (người đọc cs115a, 12/12 bài)
| ID | Bài | Mức | Phát hiện | Trạng thái |
|---|---|---|---|---|
| A01 | L01 | BS | Quy tắc vàng z⊥u ⇔ zᵀu = 0 chỉ được nêu, không có lý do. Thêm lý do qua Pytago: ‖a+b‖² = ‖a‖² + ‖b‖² + 2aᵀb | FIXED (show + say + check) |
| A02 | L03 | MUST | Giáo án hứa "x ↦ Ax giữ phép cộng và phép nhân với số", bài không nêu | FIXED (show + say + check sympy) |
| A03 | L03 | BT | "tuyến tính" có trong tên bài, chưa giảng | FIXED (note + say) |
| A04 | L04 | BT | chữ p chưa nói là số vector đầu vào | FIXED (lint 0/0, checks mới) |
| A05 | L05 | BS | λ²−4λ+3 = (λ−1)(λ−3) không chỉ cách phân tích | FIXED (lint 0/0, checks mới) |
| A06 | L06 | BS | bảng đạo hàm thiếu (xⁿ)′ = n xⁿ⁻¹, trong khi L07 và L08 dùng x³, x⁴ (gốc của A10–A12) | FIXED (lint 0/0, checks mới) |
| A07 | L06 | BS | "áp cho từng biến" nhảy bước | FIXED (lint 0/0, checks mới) |
| A08 | L07 | SHOULD | định nghĩa "liên tục" = không "gãy": sai, vì \|x\| liên tục mà có chỗ gãy | FIXED (lint 0/0, checks mới) |
| A09 | L07 | BS | (x³)′ dùng khi chưa dạy; nối lại với bảng của L06 | FIXED (lint 0/0, checks mới) |
| A10 | L07 | BQ | quiz câu 3 cần (a³)′; xử lý theo A06 | FIXED (lint 0/0, checks mới) |
| A11 | L08 | BS | x⁴; xử lý theo A06 | FIXED (lint 0/0, checks mới) |
| A12 | L09 | BT | SGD chưa giải nghĩa | FIXED (lint 0/0, checks mới) |
| A13 | L11 | SHOULD | H = JᵀJ chỉ đúng với f = ½·tổng bình phương; "sympy" chưa giới thiệu | FIXED (lint 0/0, checks mới) |
| A14 | L11 | BT | Cross-Entropy, logistic (bài 20) hiện trên màn hình mà chưa giảng | FIXED (lint 0/0, checks mới) |

## CS115 L12–L21, L44 (người đọc cs115b, 11/11 bài)
| ID | Bài | Mức | Phát hiện | Trạng thái |
|---|---|---|---|---|
| B01 | L12 | SHOULD | "số tiền không tăng mãi mà dừng": sai, vì dãy (1+1/n)ⁿ tăng ngặt, chỉ bị chặn trên | FIXED (lint 0/0, checks mới) |
| B02 | L14 | BS | E[X] = 2/3 và E[X²] = 1/2 cần ∫xᵏ, chưa dạy; thêm quy tắc 1/(k+1) | FIXED (lint 0/0, checks mới) |
| B03 | L14 | SHOULD | nét đứt SVG cắt chữ "68%" (khung 00034) | FIXED (lint 0/0, checks mới) |
| B04 | L15 | SHOULD | mở đầu ngụ ý (7;5) bất thường, nhưng kết luận là cả hai bình thường như nhau | FIXED (lint 0/0, checks mới) |
| B05 | L16 | BS | bước chứng minh uᵀSu = 4a² + b² bỏ qua Su, v₁ᵀv₂ = 0 | FIXED (lint 0/0, checks mới) |
| B06 | L16 | SHOULD | ma trận có cột trực chuẩn = "xoay": thiếu "có thể kèm lật" (det Vᵀ = −1) | FIXED (lint 0/0, checks mới) |
| B07 | L16 | BS | S = (1/N)XcᵀXc: chưa nối với tổng Σ d dᵀ của L15 | FIXED (lint 0/0, checks mới) |
| B08 | L17 | BS | 4θ³ và 4/5 cần quy tắc ∫xᵏ (theo B02) | FIXED (lint 0/0, checks mới) |
| B09 | L20 | BS | rút gọn ra ŷ − y bị giấu bước | FIXED (lint 0/0, checks mới) |
| B10 | L20 | BT | cross-entropy dạng chung −Σ p ln q chưa định nghĩa | FIXED (lint 0/0, checks mới) |
| B11 | L21 | BT | "trung bình điều hoà" chưa định nghĩa | FIXED (lint 0/0, checks mới) |
| B12 | L44 | BT | "phân phối t" chưa giảng (mẫu .tpl) | FIXED (lint 0/0, checks mới) |
| B13 | L44 | SHOULD | 0,0739 là độ cao hình chuông của TỔNG, bài không nói rõ (mẫu .tpl) | FIXED (lint 0/0, checks mới) |

## JVA L00–L12 (người đọc jva, 13/13 bài; sửa ở audit/jva/src rồi chạy gen)
| ID | Bài | Mức | Phát hiện | Trạng thái |
|---|---|---|---|---|
| J01 | L03 | MUST | đoạn trích PhiSai lines=(3,11) thiếu lệnh in, mà vẫn hiện "Kết quả chạy" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J02 | L03 | MUST | hook nói "sai ở một ký tự duy nhất", nhưng PhiSai sai hai biên | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J03 | L04 | MUST | giáo án hứa "thử 0, 1, n phần tử", bài không dạy; câu "phổ biến nhất" không có nguồn | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J04 | L00 | SHOULD | "quy tắc vế trái" sai: JLS 15.18 cho dấu + là nối chuỗi khi MỘT trong hai vế là String | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J05 | L00 | SHOULD | quiz "Áp quy tắc vế trái" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J06 | L01 | SHOULD | "quy tắc vế trái của bài trước" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J07 | L06 | SHOULD | nạp chồng: màn hình hiện 2200 mà không có lời gọi | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J08 | L06 | SHOULD | đoạn trích pham_vi, thieu mất dòng đầu hàm | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J09 | L06 | SHOULD | đoạn trích bo_qua thiếu `}` | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J10 | L07 | SHOULD | quen_this: "Chu: null" cần toString, không hiện trên màn hình | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J11 | L10 | BS | đoạn trích dấu vết bỏ dòng 1, nên không đếm được dòng 3, 6, 10 | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J12 | L11 | SHOULD | lời đọc phần tổng kết thiếu 2 ô cuối | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J13 | L11 | SHOULD | "giao diện chỉ cho lời hứa": sai từ Java 8, vì có default/static (JLS 9.4.3) | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J14 | L11 | SHOULD | 50000 không suy ra được từ mã đang hiện | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J15 | L12 | SHOULD | ngoại lệ được kiểm tra: "buộc phải bắt" thiếu "hoặc khai throws" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J16 | L08 | SHOULD | split nhận biểu thức chính quy, chưa cảnh báo | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J17 | L08, L10 | SHOULD | đoạn trích thừa `}` đóng main | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J18 | L01 | SHOULD | ví dụ đồng hồ km quay về 0, trong khi int quay về số âm nhỏ nhất | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J19 | L00 | BT | "lớp công khai" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J20 | L00 | BT | "đối soát" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J21 | L01 | BT | Integer.MAX_VALUE/MIN_VALUE | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J22 | L08 | BT | "bộ dựng chuỗi" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J23 | L09 | BT | "bộ duyệt" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J24 | L10 | BT | "tài nguyên" | FIXED (tác tử JVA; verify_jva 110/110, screen_code JVA 0 lỗi) |
| J25 | gate | — | đề xuất cho cổng: kiểm đoạn trích Java cân `{}` và chứa lệnh in tạo ra kết quả hiện kèm | KEPT: đã đo cả hai trên toàn JVA (scratchpad brace_scan.py, print_scan.py). 20 đoạn lệch ngoặc đều là trích dần có chủ đích hoặc dòng chỉ chỗ; 11 step có kết quả mà đoạn trích không in: 8 là lỗi biên dịch/ngoại lệ, L07 (toString hiện đủ), L11 (lời đọc giải thích), L12 (chương trình đã hiện trước đó). Luật cứng sẽ báo nhầm hàng loạt nên không đưa vào cổng |

## BNK, INT, ACB, DMS, CS112 (chi tiết trong báo cáo sửa của từng tác tử, chép ở mục dưới khi có)
- BNK: 2 MUST (L00 nhãn hình D→E; L04 dòng substr chứng minh sai nguyên nhân), cùng các mục BT/BS/SHOULD. Giao người đọc BNK sửa.
- INT: 6 MUST (L00 `//` trong redis-cli; L02 khối trộn redis-cli/JSON; L03 bồi hoàn khi lỗi mạng; L04 quiz mở phong toả khi lỗi mạng; L05 giáo án hứa "liên thông"; cùng nhóm nợ 10–89), cùng các mục khác. Giao người đọc INT sửa.
- ACB: 5 MUST (L00 P99 100 ms mâu thuẫn 155 ms; L06 tiêu đề "Ngân hàng Mở" không dạy; L08 nhóm 2 lệch một ngày; L08 giáo án hứa giải ngân luỹ đẳng), cùng các mục khác. Giao người đọc ACB sửa.
- CS112 L00–L14: 2 MUST (L07 ghi chú DFS dạy sai), cùng các mục khác. CS112 L15–L29: 0 MUST. DMS: 0 MUST.
- Nhóm nợ TT 31/2024: người điều phối đã kiểm (CITED: cafef.vn 2026-07-21 "từ khoảng 10 ngày đến dưới 91 ngày"; hethongphapluat.com "quá hạn đến 90 ngày", nhóm 3 "91–180", nhóm 4 "181–360", nhóm 5 "trên 360"; truy cập 2026-11-10, no revision given; chưa đọc được nguyên văn Điều 10). Đã sửa interview/04, 06, MASTER_CURRICULUM_INDEX, HANDOVER_INTERVIEW. INT L04 và ACB L08 do tác tử sửa.

## Kết quả giai đoạn sửa (báo cáo của tác tử; người điều phối kiểm diff các mục MUST)
| Khoá | Đã sửa | Không sửa (lý do) | Bài cần dựng lại | Cổng của tác tử |
|---|---|---|---|---|
| CS115 | 27/27 (người điều phối tự sửa) | — | 16 | lint 0/0; render 0; mẫu L44 khớp |
| CS112 L00–L14 | 20/20 | — | 11 | lint 0/0; render 0; verify_cs112 FAIL 0, p2 37/0; screen_code 0 lỗi |
| CS112 L15–L29 | 27 dòng/16 mục | — | 11 | lint 0/0; render 0; sync mẫu 0 lệch; screen_code 0 lỗi |
| DMS | 37 | — | 18 | lint 0/0; render 0; screen_code 0; verify_plan_curricula 545/0 |
| JVA | 24 (+ J25 KEPT) | — | 10 | verify_jva 110/110; screen_code 417/0 |
| BNK | 28 | L13 QĐ 2345 "khách hàng cá nhân": nguồn mở được không ghi điều kiện này, giữ nguyên; có tin QĐ 2345 nay ở TT 50/2024 (NOT_VERIFIED) | 14 | verify_bnk 21/21; screen_code 0 |
| INT | 36 | L06 nhắc lại TCP/máy trạng thái: đã giảng ở L03/L04 | 8 | lint 0/0; render 0; screen_code 30/0 |
| ACB | 31 | — | 9 | lint 0/0; render 0; screen_code 12/0; check_meta 0 |
