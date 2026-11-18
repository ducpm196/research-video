# R6 ACB (vòng 6, đọc độc lập bản dựng sau sửa, P1 chặt): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a0ce1669c55dfb3a0)

## 1. Tóm tắt
MUST 0 (9/9). P1=2: 3/9 chắc+vừa (L01, L04, L08); 6 bài P1=1; tính cả yếu 0/9 (L01, L08 = 1; 7 bài = 0). 8 mục vừa (0 chắc) + 26 yếu = 34. P8=2 9/9; P9=2 9/9; spec khớp 9/9; SRT khớp 9/9; lab ĐÚNG 9/9 (qua `cham.sh`); 21/21 khối mã chạy khớp; `checks` 179/179; 46/47 số khớp (5000×0,035 = 175,00000000000003 = đúng 175). ĐỦ 8/9 (L07 GẦN). 3 SVG mới (L02 bản đồ bit, L05 vòng chờ khoá, L07 con trỏ đối soát) ổn; L00 cảnh `chaytep` đọc được (khung 00060), `bash labs/cham.sh ACB L00 mau.py` chạy thật in ĐÚNG; 'đối soát' định nghĩa từ L00 (nhắc ở L01, L02, L04, L07, L08; L03 dùng một lần không nhắc; L05 chỉ 'tra soát'; L06 nghĩa khác).
Nguyên nhân chung: `requires` của L06/L07/L08 là [L00, L01, L02] nhưng bài dùng OTP (L03), CIF (L04), phân vùng (L03) → sửa `requires` (curriculum/acb.yaml) hoặc nhắc lại một dòng. Mã Go L04 và PL/SQL L05 chưa có bảng "Đọc trước" (chỉ ghi chú).

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L08 | concept, khung 00021–26 | tiêu đề SVG: "Kiến trúc Tín dụng Thấu chi Cầm cố Sổ tiết kiệm và Thấu chi Lương" (YAML dòng 143) | chỗ sót của lời hứa "thấu chi lương" đã bỏ; không cảnh nào dạy thấu chi lương | bỏ "và Thấu chi Lương" khỏi tiêu đề SVG | CONFIRMED |
| L07 | code.6, practice | mục tiêu 5: "…mở rộng ra ba nguồn và phân loại từng mã lệch" | mã chỉ chạy hai danh sách; ba nguồn chỉ có hình tĩnh/bảng; lời giải lab dùng `set(...) | set(...)`, `in`, `not` — video chỉ dạy `set()` rỗng và `.add`; đề lab "hợp của ba danh sách" | thêm một cảnh chạy phân loại ba nguồn, hoặc thêm `set(list)` và `|` vào bảng "Đọc trước" | PLAUSIBLE |
| L05 | hook | "(mục tiêu ví dụ: 3 phút)" | cảnh quy mô tính 5 s và 50 s mỗi khối nhưng không đối chiếu với mục tiêu 3 phút | một câu nối ở cảnh quy mô | PLAUSIBLE |
| L06 | concept.0 (say) | "cổng sinh trắc học đối soát dữ liệu qua đường truyền bảo mật" | "đối soát" ở đây là so khớp mẫu, khác nghĩa "hai bên so sổ" định nghĩa từ L00 | đổi thành "so khớp" | PLAUSIBLE |
| L00 | chaytep, practice | "lưu trong thư mục kho dự án"; "bash labs/cham.sh ACB L00 mau.py" | `labs/cham.sh` chỉ có trong bản sao kho; video không nói cách có kho, cài Python/Git, hay tạo tệp bằng gì; `requires_ext: PYT` không tính là giảng | thêm một dòng điều kiện hoặc đường chạy không cần kho | PLAUSIBLE |
Không kiểm được nguồn (giữ nhãn): L06 TT 50/2024, TT 77/2025 (hiệu lực 01/03/2026; VBHN 25), QĐ 2345/QĐ-NHNN (18/12/2023; hiệu lực 01/07/2024), Luật 91/2025/QH15; L08 TT 31/2024 Điều 10 (nhóm 2 = quá hạn 10–90 ngày), TT 37/2025 (31/10/2025); L05 "Không dựa vào ORDER BY đi kèm FOR UPDATE, vì Oracle khoá dòng theo đường truy cập"; L00–L04 cú pháp OFS, đặc tả NAPAS, tên thuộc tính IBM MQ (ISO 8583 các trường 3/4/11/37/52/64/128, MTI 0200/0210/0400/0420 khớp hiểu biết chung).
Điểm khác: P3=1 ở L00 (sơ đồ bốn tầng không vẽ cơ chế SAGA/khử trùng lặp), L06 (ticket và luồng không có hình cơ chế), L08 (tiêu đề SVG; hai pha không có hình); P2=1 + P7=1 ở L07; phương án nhiễu quiz hơi lộ (L07 D, L02 A/C/D, L05 D).

## 3. Mục chưa giảng — chắc+vừa (8 vừa) và yếu (26)
Vừa (SỬA BẮT BUỘC):
1. L00 pitfall "sửa khoá chính của cha" — khoá chính (A): không nói định danh duy nhất một dòng; L08 mới giảng.
2. L00 chaytep.0/practice "lưu trong thư mục kho dự án"; `bash labs/cham.sh …` — "kho dự án" (A): không nói kho là gì/lấy ở đâu (bảng giải Git Bash, bash, cham.sh, .py nhưng không giải "kho").
3. L02 symbol.1 "1111 0010 (F2)"; lab "B020…" — chữ F (A–F = 10–15) (A): chỉ có ví dụ 0111=7, 0010=2 và cụm "hệ mười sáu"; bảng `format(bits,"016X")` chỉ nói "chữ in hoa".
4. L03 example.3 "nên cần đối soát hoặc gửi bù" — đối soát (B; L00, L01 đã giảng; L03 không nhắc).
5. L03 check.0 "Hàng nghìn luồng máy chủ bị đóng băng" — luồng/thread (B; L01 đã giảng).
6. L05 example.3 "mỗi tiến trình nhận trọn một số phân vùng… ghi vào phân vùng của đoạn đó" — phân vùng (B; L03 đã giảng; chỉ ngoặc đơn mơ hồ).
7. L06 prereq.0 "theo chính sách ngân hàng, ví dụ OTP" — OTP (B; L03 đã giảng; `requires` của L06 chỉ L00–L02).
8. L07 concept.0 (SVG) "Ánh xạ sang Master CIF" — CIF (B; L04 đã giảng); kèm lab practice.3 "hợp của ba danh sách" cần `set(list)` và `|` chưa dạy.
Yếu (xử lý hết càng tốt): L00 "Máy trạng thái Saga State" (máy trạng thái), "xoá dòng cha… bảng con", "nhiều nút Redis", "làm backend tích hợp", "chuyển sang trạng thái nghi vấn"/"tra soát", `@Transactional`; L01 "Hạch toán ghi nợ ghi có" (B), "chia theo dải tài khoản"; L02 "Field 128 … (cần bitmap thứ hai)" (bản đồ bit định nghĩa ở step sau), "ghi mã PIN rõ ràng vào tệp log", "`1 << 3` là `1000` nhị phân"; L03 `if tien >= 50000:` (`>=`, B); L04 `c.Status(fiber.StatusConflict).JSON(fiber.Map{…})` (Go chuỗi gọi; chỉ ghi chú `:=`/`nil`/`err != nil`, không có bảng "Đọc trước"), "Câu lệnh SQL cập nhật…", "Dịch vụ Go Fiber", "giữ đến ngày đáo hạn"; L05 PL/SQL `FOR r IN (...) LOOP … END LOOP;` (ghi chú giải TABLE/column_value/AS/ORDER BY 1/r.acc/INTO, không giải FOR…LOOP), "ứng dụng phải bắt lỗi rồi làm lại", `dau = []`, `dau.append(so_du)` (B); L06 "Kiểm tra chữ ký số… tại Backend", "chip CCCD"; L07 `else:` (bảng chỉ `elif`), `import hashlib, hmac` (B), "Số VA gồm tiền tố…"; L08 "giải ngân an toàn"/"lệnh giải ngân", "dư nợ thấu chi".
Số mục theo bài (chắc / vừa / yếu / tổng): L00 0/2/6/8; L01 0/0/2/2; L02 0/1/3/4; L03 0/2/1/3; L04 0/0/4/4; L05 0/1/3/4; L06 0/1/2/3; L07 0/1/3/4; L08 0/0/2/2.

## 4. Người học kẹt ở đâu
L00 chaytep 06:07 "lưu các dòng mã vào tệp… trong thư mục kho dự án", rồi bước 4 `bash labs/cham.sh` (người học không có kho, có thể chưa có Python/Git; mức vừa), sau đó "khoá chính" ở pitfall; L01 không kẹt; L02 symbol.1 "1111 0010 (F2)" (vừa); L03 example.3 "đối soát hoặc gửi bù" (nhẹ); L04 example.3 mã Go (nhẹ); L05 example.3 "phân vùng" (vừa nếu quên L03); L06 prereq.0 "ví dụ OTP" (OTP giảng ở L03 mà `requires` của L06 không có L03); L07 concept.0 "Master CIF", practice.3 `set(list)` và `|` chưa dạy (vừa); L08 vấp nhẹ "giải ngân".
