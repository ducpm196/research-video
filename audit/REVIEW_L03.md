# Rà soát L01–L02 + làm L03 — 2026-10-23

Phạm vi: chạy lại toàn bộ kiểm tra của L01, L02; làm bài L03 `lessons/L03_truc_chuan_gram_schmidt.yaml` → `out/L03/`.
Nhãn: OBSERVED = chạy trong phiên này; INFERRED = suy luận, chưa kiểm bằng máy. Môi trường: Python 3.13.5 (`.venv`), Windows 11.

## 1. Nút thắt hợp đồng (contract bottleneck)

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B5 | Nguồn (dòng 189–198) không nêu điều kiện đầu vào của Gram-Schmidt; trộn ‖v‖² và ‖v‖₂ | Nội dung L03 (không được lặp lại thiếu sót của nguồn) | Audit A20 + phép kiểm T2d (x₂ = 2x₁ → v₂ = 0); `verify_cs115_tex.py` → `TOTAL=36 PASS=36 FAIL=0` (07:02:33Z). L03 nêu ở lỗi 4 và step ghi chú ký hiệu | CLOSED |
| B6 | `lv.py tts`: một câu lỗi mạng làm huỷ **cả lượt** (asyncio.gather) → dưới giới hạn tần suất, mỗi lượt chỉ thêm vài câu (40/158 sau 2 lượt) | Mọi bước build | Đối chứng: câu “Xin chào bạn.” cũng lúc lỗi lúc được → lỗi dịch vụ, không do nội dung. Sửa `_tts_one` trả `fail` thay vì raise; `cmd_tts` in `[FAIL] tts …`, exit 1. Lượt kế tiếp: 114 mới + 40 cache, 4 lỗi; lượt sau đủ 158/158 | CLOSED |
| B7 | ASR gắn cờ 11 câu vì chữ Q → “quy” | Kết luận phát âm | Đối chứng: audio “Q” và “quy” dài bằng nhau 3,264 s (“cu” lệch 72 ms); medium chép bản “quy”, “ca”, “vê gi” y hệt bản chữ cái thô. Thêm `LETTER_HEARD` q, k + 3 test E17 (cả ca “quy tắc” không bị đổi). L01/L02 chạy lại: số câu chờ nghe không đổi (9, 8) | CLOSED |

## 2. Lỗi tìm thấy khi làm L03 (đã sửa)

| # | Lỗi | Phát hiện bằng | Sửa |
|---|---|---|---|
| G1 | Thiếu `assumes` cho `dots`, `iff` (đã học ở L01) | lint FAIL | thêm vào `assumes` |
| G2 | Bước 3 của Gram-Schmidt tràn bảng (3 khung) | render FAIL | `clear: true` + nhắc lại dòng “v₁ = x₁, v₂ = x₂ − c·v₁” |
| G3 | Ma trận Q và QᵀQ viết bằng phân số trong từng ô: các hàng dính vào nhau, khó đọc | xem khung 113, 118 | đưa thừa số 1/5, 1/25 ra ngoài ma trận (có `checks`) |
| G4 | Hộp lỗi 1, lỗi 4: công thức bị ngắt dòng giữa chừng | xem khung 129, 135 | chuyển sang công thức dòng riêng |
| G5 | “Q⁻¹ = Qᵀ” phải nói rõ Q **vuông**; tên “ma trận trực giao” dễ nhầm | rà phát biểu (pedagogy luật 15) | nêu điều kiện vuông + kiểm QQᵀ = I₂ bằng số; thêm ghi chú tên gọi |
| G6 | `I` không chỉ số (lệch quy ước L02 “I luôn có chỉ số kích thước”) | rà quy ước | `I_p`, `I_2`, `I_3` |

## 3. Bằng chứng (OBSERVED, `checked_at` từ đầu ra công cụ)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Tự kiểm công cụ | `tests/test_lint.py` | 43 PASS, 0 FAIL (thêm 3 ca E17 cho Q; 07:58:05Z) |
| Lint L03 | `lv.py lint lessons/L03_…yaml` | 0 FAIL, 0 WARN; 50 phép kiểm số học (sympy); 154 công thức KaTeX không lỗi (07:56:57Z) |
| Lint + verify L01, L02 | `lv.py lint`, `lv.py verify` | 0 FAIL, 0 WARN; PASS (1121,73 s; 1114,1 s) |
| Lộ trình | `lv.py curriculum curriculum/cs115.yaml` | 17 bài, 3 có đặc tả, 0 lỗi (07:03:01Z) |
| Audit nguồn | `audit/verify_cs115_tex.py` | `TOTAL=36 PASS=36 FAIL=0` (07:02:33Z) |
| Video L03 | `lv.py build` → verify | 902,9 s = timeline 902,9 s (15,0 phút, 158 khung); PASS (07:56:56Z) |
| Khớp tiếng–hình L03 | `sync_check.py` (9 điểm trải đều) | 0 lệch; MAE khung đúng 1,31–1,62 < khung kế 2,49–11,52 (07:57:26Z) |
| ASR L03 | `lv.py asr` (small + medium, mức câu + mức từ) | 158 câu, TB 0,963; gắn cờ 7, đã xem xét 6 (đối chứng), **chưa xem xét 1**; tham khảo 41 (07:56:55Z) |
| Khung đã xem bằng mắt | Read ảnh | 3, 7, 13, 17, 20, 24, 28, 31, 34, 41, 43, 53, 55, 63, 64, 74, 77, 85, 90, 97, 103, 106, 113, 118, 122, 129, 135, 145, 154, 157 (gồm khung SVG, mọi khung có ký hiệu mới, khung cuối formula/example, pitfall, khung cuối); 113/118/129/135 xem lại sau khi sửa |

## 4. Còn mở (NOT_VERIFIED)

- L03 cần người nghe: **13:29** (“v một bằng 1, 1” → ASR nghe “mục mục”), cùng loại “một → mục” như L01/L02. Danh sách L01 (9 câu) và L02 (8 câu) ở `audit/REVIEW_L02.md` §4 vẫn mở.
- Mục tham khảo (41 câu) phần lớn là “vuông góc → vung gốc”, “toạ → toả”, “ngoặc → hoặc”: ASR nhầm thanh, không chặn (giới hạn đã ghi ở REVIEW_L02).
- Hiệu quả sư phạm với người học thật: chưa đo.
