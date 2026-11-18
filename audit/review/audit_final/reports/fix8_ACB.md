# fix8_ACB — vòng sửa cuối (2026-11-17), theo tóm tắt R7

Chi tiết L03/L04/L07/L08: `fix8_ACB_X.md`. Phần dưới: L00–L02 và cổng.

## Bài đã đổi (requeue): L00 L01 L02 L03 L04 L07 L08 (L05, L06 không đổi trong vòng này)
## L00–L02 (tôi)
- L00 chaytep: hàng bảng "vào thư mục chứa mau.py, bấm chuột phải, chọn Open Git Bash here"; nguồn labs: kho = thư mục khoá học bạn được giao (tải hoặc sao chép về, có thư mục labs); chưa có kho thì chạy `python mau.py` và so với kết quả mong đợi (bước 3 ghi "không cần kho"). Bảng rút để không tràn.
- L00 pitfall: "lớp = khuôn mã Java gom dữ liệu và hàm"; "giao dịch = nhóm lệnh cùng thành công hoặc cùng bị huỷ" (màn hình + lời); khoá chính/dòng cha/bảng con giữ từ vòng 7.
- L00 dòng "Nhắc nền sẽ dùng lại" dưới bảng Đọc trước (==, //, round, def, .replace) + một câu lời; sổ cái ("sổ ghi mọi khoản tiền vào ra của từng tài khoản") và nút Redis ("một máy chạy Redis") định nghĩa; "Trong kiến trúc này, cổng API là cửa duy nhất". Cắt lời (bỏ câu "Hôm nay ta phân tích…", "Đổi lại … SAGA", một ý ở vaitro/concept) để về 2298.
- L01: nhãn SVG đổi "Hạch toán sổ cái" (hết co chữ/gãy hộp).
- L02: bảng bản đồ bit thêm "0111 = 4 + 2 + 1 = 7 (bốn vị trí có giá trị 8, 4, 2, 1)" ở màn hình + lời; cắt lời để còn 2300.
- verify_acb.py: thêm `fixes8_l00_l02`, sửa kiểm chaytep theo chữ mới; fork sửa một kiểm L08.

## Cổng (chạy lại cuối)
| cổng | kết quả |
|---|---|
| lint 9 bài | 0 FAIL, 0 WARN |
| lời đọc (từ) | L00 2298 · L01 2162 · L02 2300 · L03 2288 · L04 2296 · L05 2287 · L06 2292 · L07 2297 · L08 2299 |
| render L00, L01, L02 (tôi) và L03, L04, L07, L08 (fork) | 0 vấn đề (đã xem khung bảng chaytep, bảng 8-4-2-1, hộp L04/L08) |
| `verify_acb.py` đủ khoá | 310/310 PASS |
| `tests/test_e52.py` | 0 FAIL |
| CRLF | cả 9 bài nguyên vẹn |
| `screen_code.py check --course ACB` | 62 khối — PASS 39 · FAIL 0 · STALE 16 · MISSING 28 · ORPHAN 28 (toàn bộ là mục cảnh `code`/`practice 1 0` do gen_sc_acb.py sinh; mục thủ công không lỗi). KHÔNG chạy gen_sc_acb.py (classifier chặn); người điều phối xin phép người dùng rồi chạy. |

Mục chưa giảng (chắc+vừa) ước còn lại: 0 ở các bài đã sửa; các câu `say` mới chưa ASR/nghe.
