# Mẫu F — đọc độc lập sau đợt LF2 (2026-11-12T18:10Z, đợt rà AF1)

**Kết luận: `PARTIAL`.** Số liệu và đáp án sạch (≈ 150 nhóm phép tính, 2 lệch ở chữ số cuối), nhưng 3/38 bài còn lỗi mức MUST, 28/38 bài còn ít nhất một phát hiện, và 35/38 bài không giao việc thực hành nào ngoài quiz.

- **Mẫu**: `sample_f.py` (hạt giống 20261112; mỗi khoá một bài trong 456 bài chưa từng vào mẫu C/D/E và ngoài 6 khoá LS1; thêm một bài BNX thứ hai) = 38 bài. sha16 lúc đọc trùng danh sách ở 38/38 bài; commit `df811558`.
- **Người đọc**: 3 tác tử chỉ đọc, tiêu chí `BRIEF.md` + phụ lục P8 (thực nghiệm), P9 (quy mô/thời gian). Tác tử thứ tư đọc 21 bài đầu của đường học (JVA L00–L12, BNK L00–L04, L07, BNX L00–L01): mục 4.
- **Giới hạn**: báo cáo nguyên văn của bốn tác tử KHÔNG lưu được thành tệp (nhật ký tác vụ rỗng); tệp này là sổ phát hiện rút gọn do người điều phối chép từ tin nhắn trả về. Mức tin cậy là của người đọc; cột "ĐP kiểm" ghi ✔ khi người điều phối đã mở tệp bài và thấy đúng chữ được trích. Người đọc không nghe âm thanh; `.srt` trùng `say` 38/38 chỉ chứng minh phụ đề, không chứng minh giọng đọc.

## 1. Số đo (tính bằng máy, Wilson 95%)

| Chỉ số | Mẫu C | Mẫu D | Mẫu E | **Mẫu F** |
|---|---|---|---|---|
| Bài có MUST | 5/42 | 2/42 | 2/42 | **3/38 = 7,9% (2,7–20,8%)**; 2/38 nếu chưa tính BNX L12 (chờ văn bản gốc) |
| Bài có ít nhất một phát hiện | 16/42 | — | 18/42 | **28/38 = 73,7%** (37 SHOULD) |
| Mất gốc ĐỦ / GẦN / CHƯA | — | — | 29 / 12 / 1 | **30 / 8 / 0** |
| P1 = 2 (mọi thuật ngữ giảng tại chỗ) | — | — | 9/42 | **7/38 = 18,4%**; P1 = 0 ở 2 bài |
| P8 = 2 (có việc tự làm + kết quả đối chiếu) | — | — | — | **2/38 = 5,3%** (cả hai là BNX); P8 = 0: CLD L01 |
| P9 = 2 (số liệu ở ≥ 2 mức quy mô/mốc thời gian) | — | — | — | **18/38 = 47,4%**; P9 = 0 ở 7 bài |

Mẫu F không so thẳng được với C/D/E ở dòng "có phát hiện": tiêu chí giữ nguyên nhưng người đọc đợt này gắt hơn ở mục tiêu giáo án. Ba MUST đều KHÔNG phải số sai: hai là "giáo án hứa điều bài không dạy", một là văn bản pháp lý.

## 2. Sổ phát hiện chuẩn xác

| Bài | Mức | Chỗ | Vấn đề | Hướng sửa | Tin cậy | ĐP kiểm |
|---|---|---|---|---|---|---|
| AGT L04 | MUST | objectives; sym 1 | Mục tiêu "Viết lại truy vấn dựa trên kết quả trước" không có một cặp truy vấn gốc → viết lại nào | thêm ví dụ chữ | CONFIRMED | |
| AGT L04 | SHOULD | objectives; example 4 | "Kiểm trích dẫn bằng chương trình" nhưng không có dòng mã | hiện 5–6 dòng Python + kết quả | CONFIRMED | |
| BNX L12 | MUST | sym 2; intuition 2; formula 6 | Dẫn Luật Quản lý thuế 38/2019 Điều 58; người đọc tìm thấy Luật 108/2025/QH15 hiệu lực 01/7/2026 (qua trang thứ cấp; CHƯA mở văn bản gốc) | đọc nguyên văn luật mới, sửa điều dẫn và chữ trong hình | CONFIRMED luật cũ hết hiệu lực (nguồn thứ cấp) | chờ CB-AF1-2 |
| BNX L12 | SHOULD | sym 2 | TT 19/2021/TT-BTC: TT 46/2024 sửa đổi chưa đọc | kiểm cùng lúc | PLAUSIBLE | |
| DVO L03 | MUST | title; hook | Tên bài "nhanh, tin cậy, bị cô lập", hook "mỗi lần chạy không phụ thuộc lần khác": không cảnh nào dạy cô lập hay thời gian đường ống | thêm cảnh hoặc đổi tên/hook | CONFIRMED | ✔ |
| AIF L11 | SHOULD | example 1–3 | Thiếu P(a∣¬b,e) = 0,29 nên 0,000592; 0,284… không tự tính lại được | hiện đủ bảng 4 dòng | CONFIRMED | |
| AIF L11 | SHOULD | sym 1 / intuition | J, M, A ↔ "hàng xóm 1", "chuông": ba cách gọi một nút | một bộ tên | CONFIRMED | |
| BCH L05 | SHOULD | prereq 3; example 3 | Chuỗi in "khoi-1 \| 0" (có dấu cách) nhưng mã băm là của `khoi-1\|0`; không nêu SHA-256 | ghi đúng chuỗi + tên hàm | CONFIRMED | |
| CAS L04 | SHOULD | pitfalls 2 | "thư 5/12/1997": sources không có câu trích chứa ngày | mở lại nguồn | PLAUSIBLE | |
| CLC L10 | SHOULD | objectives | "Diễn tập chuyển vùng" không có bước diễn tập nào | thêm 4–5 bước + số đo | CONFIRMED | |
| CLD L01 | SHOULD | pitfalls 4 | Hết bộ nhớ: "giết B hoặc C" thiếu điều kiện (bộ chọn thường chọn tiến trình lớn nhất) | thêm điều kiện, kiểm tài liệu nhân | PLAUSIBLE | |
| CLD L01 | SHOULD | sym 1; example 4; quiz 1 | Màn hình "nhân Linux" ↔ lời "nhân hệ điều hành" | thống nhất | CONFIRMED | |
| CS115 L29 | SHOULD | kmeans 2 | "J không tăng… vì vậy luôn dừng": thiếu "số cách chia hữu hạn" | thêm một câu | CONFIRMED | |
| CSA L07 | SHOULD | loadstore 1 | "nhanh hơn bộ nhớ hàng trăm lần" không nguồn, không điều kiện | thêm điều kiện | CONFIRMED | |
| CSA L07 | SHOULD | title; objectives | "nạp, lưu" có trong tên bài, chương trình mẫu không có `lw`/`sw` nào | thêm 2 lệnh vào ví dụ | CONFIRMED | |
| CVI L07 | SHOULD | intuition 2 | Tiêu đề cảnh "Mỗi lớp 3 × 3…" đứng trên sơ đồ học chuyển giao | tách cảnh | CONFIRMED | |
| CVI L07 | SHOULD | example 1 | 2 359 808 tính có hệ số tự do; mạng thật thường không có | ghi giả định | PLAUSIBLE | |
| DBS L13 | SHOULD | twophase 1 | "commit" ↔ "ghi nhận" lẫn trong một bài | thống nhất | CONFIRMED | |
| DEN L09 | SHOULD | pitfalls 4; quiz 3 | Chỉ nêu một phía đánh đổi của chu kỳ điểm kiểm tra | thêm chi phí mỗi lần chụp | CONFIRMED | |
| ESY L10 | SHOULD | sym | Liu–Layland U ≤ 1 thiếu điều kiện một bộ xử lý, chiếm quyền, tác vụ độc lập | thêm dòng điều kiện | CONFIRMED | |
| GFX L08 | SHOULD | intuition | "phân biệt rõ 1% với 2% ánh sáng" không nguồn | bỏ số hoặc dẫn nguồn | PLAUSIBLE | |
| HCI L00 | SHOULD | example 3 | "8:27 mới họp" ↔ sources "8:24–8:27" | đối chiếu FCC | PLAUSIBLE | |
| IRS L11 | SHOULD | loop | "cộng 10% khám phá… A 950, B 50": không nói 100 lượt chia đôi | thêm một câu | CONFIRMED | ✔ |
| IRS L11 | SHOULD | quiz 2 | 1,062/2,562 = 41,5% nhưng ghi 41,4% (đúng với số chưa làm tròn) | thêm chữ số | CONFIRMED | ✔ (tính lại) |
| LLM L05 | SHOULD | pitfalls Lỗi 2 | "12,9 + 34,4 = 47,2" (= 47,3 với số đã làm tròn) | "≈ 47,2 (12,88 + 34,36)" | CONFIRMED | ✔ |
| LLM L05 | SHOULD | example 4 | "gần gấp 3" (2,67) | "khoảng 2,7 lần" | CONFIRMED | ✔ |
| NET L10 | SHOULD | loss | "TCP gần với cách thứ hai": TCP là lai | sửa câu | PLAUSIBLE | |
| OSY L14 | SHOULD | example 4 | Bảng lương 750 cấp quyền chạy, trái "ít quyền nhất" của chính bài | dùng 640 | CONFIRMED | |
| PLC L13 | SHOULD | quiz 1 | Đề "mỗi năm thêm 20 000 dòng" nhưng lời giải coi cả 200 000 dòng 5 năm tuổi | ghi giả định | PLAUSIBLE | |
| PLC L13 | SHOULD | stage4 2 (say) | Lời đọc mất vế "của C++" | thêm vế | CONFIRMED | |
| ROB L10 | SHOULD | objectives | "Chọn khoảng nhìn trước theo tốc độ" chỉ có một câu | ví dụ số L theo v | CONFIRMED | |
| SDP L01 | SHOULD | example 1 | Hai dòng cùng số bước "4"; "ba bước" ↔ 4 dòng | đánh số lại | CONFIRMED | |
| SEC L11 | SHOULD | objectives | "ngôn ngữ an toàn bộ nhớ là giải pháp gốc" chỉ khẳng định, không cơ chế | thêm ví dụ kiểm biên | CONFIRMED | |
| SEP L08 | SHOULD | check 0 | "Đường khác" xếp từ điển (nhỏ nhất, tổng, …) không tương đương luật ba bước; phản ví dụ P = [1,1,1,1], Q = [0,2,2,2] | đổi số đầu thành đạt/không đạt | CONFIRMED | ✔ |
| SWF L03 | SHOULD | overflow 0–1 | "(như Java, C)… quay vòng thành −3": trong C tràn số có dấu là hành vi không xác định | bỏ "C" hoặc thêm điều kiện | CONFIRMED | ✔ |
| WEB L07 | SHOULD | example 2; quiz 1 | Con trỏ tính bằng (trang − 1)·k chỉ đúng khi id liền mạch; không nêu "con trỏ không nhảy trang" | thêm lỗi thường gặp | CONFIRMED | |
| BNX L05 | SHOULD | objectives; example 4 | Mục tiêu kiểm "tên" chứng chỉ; mã ghi "CHƯA kiểm tên" | thêm ca thứ năm | CONFIRMED | |
| BNX L05 | SHOULD | quiz 3 | "355 ngày" thiếu giả định không thu hồi; câu "Quyết định" không chốt | thêm | PLAUSIBLE | |
| BNX L05 | SHOULD | example 0 (say) | Lời "máy văn phòng" ↔ màn hình "Git Bash (Windows)" | đọc "trên Windows" | CONFIRMED | |
| DAN L04, DSC L11, DSY L03, EVT L09, MLO L01, PAR L06, RBM L01, RLN L06, SAR L00, TOC L09 | — | | không phát hiện lỗi chuẩn xác | | | |

Lỗi hiển thị nhỏ (không chặn): CLC L10 khung 00018 (nhãn chạm viền), CVI L07 00010 (tử số chạm khung), DBS L13 00034 (nét đứt cắt nhãn), ROB L10 00018 (ô ký hiệu ngắt dòng). 224 khung của 38 bài: không khung nào tràn, đè, cắt chữ.

## 3. Độ sâu cho người mất gốc (38 bài)

- **GẦN (8)**: AIF L11 (10), BNX L05 (10), CLC L10, CS115 L29, CVI L07, DBS L13, PLC L13, SAR L00 (11). Còn lại ĐỦ (12–14).
- **P1 (thuật ngữ tại chỗ) vẫn là điểm yếu chính**: 31/38 bài còn 1–4 thuật ngữ dùng mà không giảng tại chỗ (ví dụ: "phân kỳ" RLN L06, số e ở BCH L05 và PLC L13, "tinh chỉnh/tốc độ học" CVI L07, "tiến trình" OSY L14, "commit" DBS L13, cú pháp Python ở SDP L01, SQL ở WEB L07). Cột "Cần biết trước" của người đọc cho thấy phần lớn là kiến thức của bài trước trong khoá hoặc của khoá khác.
- **Mẫu lặp "mục tiêu là kỹ năng làm, bài chỉ cho xem kết quả máy tính"**: AGT L04, AIF L11, CSA L07, CS115 L29 (phân cụm phổ cho sẵn vector riêng), CLC L10, ROB L10, SEC L11, BNX L05, ESY L10 (quá tải "mô phỏng 60 đơn vị").
- **P8 thực nghiệm**: 35/38 bài chỉ có quiz tính tay; CLD L01 dạy container không có một lệnh; OSY L14 dạy phân quyền không có `ls -l`/`chmod`; WEB, SDP, ROB, RLN có sẵn mã trong `checks` nhưng người học không được giao chạy.
- **Bài bị nén**: CLC L10 5,9 phút; TOC L09 6,5; DAN L04 6,9; AIF L11 7,1; SDP L01 7,1.

## 4. Đường đi của người mất gốc (21 bài đầu, đọc theo thứ tự `HOC_TAP.md`)

- JVA L00–L12: theo được trọn; 8 chương trình Java chạy lại bằng JDK 21.0.13 đều khớp đầu ra bài nói. Không MUST.
- **Sau JVA L00 không bài nào trong 20 bài còn lại bắt người học tự gõ và chạy**; không bài tập ngoài quiz; không dự án tự xây (JVA L12 tự viết hết sổ chuyển khoản). 6 bài BNK đã đọc có **0 khối mã** (đối chiếu máy: BNK 0/15 bài có khối mã, mục 5).
- JVA **chưa dạy**: nhập dữ liệu (`Scanner`, `args`), đọc ghi tệp, generics tự viết, lambda/stream, `package`/nhiều tệp/classpath, JUnit, Maven/Gradle/IDE, debugger, luồng, annotation (chỉ `@Override`), HTTP, JSON, cơ sở dữ liệu, `cd`/thư mục/PATH. `String[] args`, `System.out`, `//` dùng từ L00, hứa "các bài sau giải thích" nhưng không bài nào giải thích.
- **Khoảng hở tiên quyết (loại "chưa bài nào đứng trước dạy")**:

| Bài | Dùng mà chưa dạy | Mức |
|---|---|---|
| BNK L01 | mô hình máy khách–máy chủ ("10 000 yêu cầu chờ đối tác"); luồng chỉ định nghĩa một câu, không có dòng Java nào | KHÓ |
| BNK L02 | Spring, bean, IoC, tiêm phụ thuộc, proxy, annotation có tham số, CSDL/bảng/giao dịch/commit/rollback, Controller: 9 thuật ngữ mới trong 2 bảng, 0 dòng mã; CSDL định nghĩa trong một dấu ngoặc, hai bài trước khi có SQL (L04); "yêu cầu từ bên ngoài" trước bài HTTP (L03) | KHÓ nặng |
| BNK L03 | giao thức, web, API, máy chủ; "tạo bảng có ràng buộc duy nhất rồi chèn" khi chưa thấy lệnh SQL nào | KHÓ |
| BNK L04 | câu SQL hoàn chỉnh không hiện lần nào (SELECT 1 lần, FROM 0); sqlite là gì | KHÓ |
| BNX L00 | bash (`export`, `mktemp`, `/dev/null`, `cd`), cài Git; JVA L00 bảo dùng Command Prompt/PowerShell, nơi các lệnh này không chạy | CHẶN khi thực hành |
| BNX L00, L01 | Python (f-string, `encode`, comprehension, `re`), JSON, YAML giảng một câu | KHÓ |

- SHOULD khác: thuật ngữ đổi giữa hai khoá ("chú thích ghi đè" ↔ "nhãn (annotation)"; "hàm tạo" ↔ "hàm khởi tạo"); BNK L01 gộp "platform / carrier thread"; JVA L10 `new TaiKhoan(100000)` khác hàm tạo ở L07; phần không được chiếu sáng mờ quá nhạt (`player.css` `.blk .dim { opacity: .38 }`), ví dụ JVA L00 khung 75–76, JVA L12 khung 45, 78; BNK L04 khung 50 gần trống.

## 5. Đo máy toàn kho (người điều phối, `scratchpad/stats.py`, 680 bài)

- Bài có khối mã trên màn hình: **148/680**. Bằng 0 ở: BNK, CS115, AIF, LLM, AGT, RLN, IRS, DSC, DVO, EVT, GFX, HCI, PAR, RBM, ROB, SEP (16 khoá).
- "Python" xuất hiện ở 79 bài (BNX 18, PLC 9, SDP 9, ESY 8…) nhưng **không khoá nào dạy Python từ đầu**. PyTorch: 4 bài; numpy: 20 bài (chủ yếu trong `checks`); pandas, IDE, debugger, terminal: 0 bài.
