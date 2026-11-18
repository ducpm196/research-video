# fix7_ACB — sửa vòng 7 theo R6_ACB (2026-11-17)

Chi tiết: `fix7_ACB_A.md` (L03–L05), `fix7_ACB_B.md` (L06–L08). Phần dưới: L00–L02, giáo án, cổng tổng.

## Bài đã đổi (requeue): cả 9 bài L00–L08; curriculum/acb.yaml (requires L06 thêm L03, L07 thêm L04; objective 5 của L07 sửa cho đúng nội dung); audit/acb/verify_acb.py (thêm fixes7_l00_l02); hai khoá thủ công trong sổ screen_code (L04, L05) bởi fork A.

## Mục vừa (8) đã xử lý
L00 khoá chính (pitfall: "khoá chính là cột định danh duy nhất một dòng", dòng cha/bảng con giải nghĩa) và "kho dự án" (ghi chú cảnh chaytep: kho = thư mục chứa mã nguồn khoá học; chưa có thì tạo thư mục mới và chép các bài thực hành vào; `python mau.py` chạy KHÔNG cần kho, chỉ lệnh chấm cần kho); L02 chữ A–F hệ mười sáu (A=10 … F=15; F2 = 15×16 + 2 = 242, cả màn hình lẫn lời); L03 đối soát + luồng; L05 phân vùng; L06 OTP; L07 CIF + `set(list)` và `|`. `requires`: L06 [L00..L03], L07 [L00, L01, L02, L04].
Yếu cùng họ: L00 backend/nghi vấn/@Transactional/máy trạng thái (đổi nhãn SVG thành "Theo dõi trạng thái Saga")/nút Redis; L01 hạch toán, "chia tài khoản thành nhiều nhóm"; L02 nhị phân, "ghi mã PIN thô vào nhật ký", "Field 128 … cần bản đồ bit thứ hai"; các mục L03–L08 xem báo cáo A/B (bảng Go ở L04, PL/SQL FOR…LOOP ở L05, `else:`, `import hashlib, hmac`, VA, giải ngân, dư nợ, backend, CCCD…).
SHOULD: L08 SVG bỏ "và Thấu chi Lương" (`grep -i 'thấu chi lương'` toàn khoá + curriculum = 0); L06 "so khớp"; L05 câu nối 3 phút với 5 s/50 s; L07 mục tiêu 5 sửa đúng nội dung; L00 điều kiện áp dụng cham.sh.

## Cổng (số thật)
| cổng | kết quả |
|---|---|
| lint 9 bài | 0 FAIL, 0 WARN cả 9 |
| lời đọc (từ) | L00 2289 · L01 2162 · L02 2292 · L03 2288 · L04 2296 · L05 2287 · L06 2292 · L07 2290 · L08 2293 |
| render | 9/9 bài 0 vấn đề (L00–L02 do tôi, xem khung L02 bảng A–F; L03–L08 do fork, đã xem khung bảng/hình mới) |
| `verify_acb.py` đủ khoá | 306/306 PASS |
| `tests/test_e52.py` | 0 FAIL |
| `lv.py curriculum curriculum/acb.yaml` | 9 bài, 0 lỗi |
| `check_legal` (fork B) | 0 FAIL |
| `check_curricula_graph.py` | không báo lỗi liên quan ACB; dòng "VER dẫn tới mã không PASS" hiện liệt kê mã AGT:L00… (khoá AGT, không thuộc phạm vi; ACB không có mục nào) |
| `screen_code.py check --course ACB` | **chưa sạch, đúng như trước vòng này**: 62 khối — PASS 41 · FAIL 0 · STALE 14 · MISSING 28 · ORPHAN 28 |

screen_code: các dòng lỗi đều là mục cảnh `code` và `practice 1 0` do `audit/acb/gen_sc_acb.py` sinh (chèn bảng "Đọc trước" làm lệch chỉ số step). KHÔNG chạy gen_sc_acb.py (classifier chặn, brief cấm script sửa sổ). Người điều phối xin phép người dùng rồi chạy `gen_sc_acb.py` + `screen_code.py check --course ACB`.

## Mục chưa giảng ước còn lại (chắc+vừa)
L00 0 · L01 0 · L02 0 · L03 0 · L04 0 · L05 0 · L06 0 · L07 0 · L08 0.

## Còn mở
Nhiều câu `say` mới chưa ASR/nghe; `asr_reviewed` của câu đã đổi đã xoá. CRLF của cả 9 bài nguyên vẹn (kiểm bằng đếm nhị phân).
