# ESY — đã đọc 16/16 bài

Người đọc: tác tử con (fork) đợt B, 2026-11-08. Đọc toàn bộ `show`/`say`/`checks`/quiz của từng bài (bản trích chữ, SVG chỉ giữ chữ), đối chiếu L15 với `audit/esy/sources_L15.md` và trang JPL 27/3/2015 (WebFetch, truy cập 2026-11-08, no revision given). Tổng: 8 bài sửa, 2 mục MUST, 14 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00_he_nhung | đã sửa | quiz.3: SHOULD — đáp án nói B “luôn kịp” chỉ từ 10 lần đo, trái chính lỗi 2 của bài (đo vài lần không phải bảo đảm); sửa thành “kịp cả 10 lần, vẫn phải phân tích thời gian xấu nhất” | G. C. Buttazzo, Hard Real-Time Computing Systems, 3rd ed. (2011), ch. 1 (WCET là cơ sở bảo đảm) | lint: 0 FAIL, 0 WARN, 24 PASS / render: 70 khung (0 vấn đề) |
| L01_thanh_ghi_bit | không phát hiện lỗi | — | — | — |
| L02_ngat_chong_doi | không phát hiện lỗi | — | — | — |
| L03_dinh_thoi_pwm | đã sửa | pitfalls.2 (Lỗi 3): SHOULD — bài dẫn datasheet ATmega328P nhưng không nói chính chip này (PWM nhanh, không đảo: đặt ở BOTTOM, xoá khi khớp so sánh) cho độ rộng (CMP+1)/(TOP+1); thêm ví dụ | Microchip, ATmega328P datasheet (DS40002061A), mục 15 (8-bit Timer/Counter0 with PWM), phần Fast PWM Mode — số tiểu mục chưa kiểm lại | lint: 0 FAIL, 0 WARN, 29 PASS / render: 62 khung (0 vấn đề) |
| L04_adc | đã sửa | pitfalls.1 (Lỗi 2): SHOULD — “vượt Vref thì có thể hỏng chân vào” thiếu điều kiện; hỏng khi vượt điện áp nguồn nuôi chip, không phải chỉ vượt Vref | Microchip, ATmega328P datasheet, mục Absolute Maximum Ratings (chân vào −0,5 V tới VCC + 0,5 V) | lint: 0 FAIL, 0 WARN, 28 PASS / render: 65 khung (0 vấn đề) |
| L05_loc_so | không phát hiện lỗi | — | — | — |
| L06_dau_phay_tinh | đã sửa | pitfalls.3 (Lỗi 4): SHOULD — “dịch phải luôn làm tròn về âm vô cùng”: với số âm có dấu, C để trình biên dịch tự định nghĩa; thêm điều kiện | ISO/IEC 9899:2018, §6.5.7 ¶5 | lint: 0 FAIL, 0 WARN, 27 PASS / render: 66 khung (0 vấn đề) |
| L07_uart | đã sửa | example.3: SHOULD — “lệch 3,55% đúng là lỗi chữ rác” tự mâu thuẫn với hình intuition (một mình 3,55% mẫu cuối vẫn trong bit dừng); sửa: còn vừa lọt, cộng ~2% lệch ngược chiều ở đầu kia là vượt 5,3%; thêm `checks` | Maxim AN2141 (2003); ATmega328P datasheet, bảng Recommended Maximum Receiver Baud Rate Error (±2,0% cho 8 bit, U2X = 0) | lint: 0 FAIL, 0 WARN, 29 PASS / render: 69 khung (0 vấn đề) |
| L08_i2c_spi | đã sửa | sym.0: SHOULD — màn hình ghi I²C “100 kHz hoặc 400 kHz” như là tất cả, lời đọc có “thường”; thêm “thường” và chế độ 1 MHz trở lên (cả màn hình và lời đọc), sửa `focus` | NXP UM10204 Rev. 7 (2021), mục 3 (Standard-mode, Fast-mode, Fast-mode Plus 1 Mbit/s, High-speed 3,4 Mbit/s) | lint: 0 FAIL, 0 WARN, 25 PASS / render: 72 khung (0 vấn đề) |
| L09_lap_lich_rm | không phát hiện lỗi | — | — | — |
| L10_edf_dao_uu_tien | không phát hiện lỗi | — | — | — |
| L11_rtos | không phát hiện lỗi | — | — | — |
| L12_do_tin_cay | không phát hiện lỗi | — | — | — |
| L13_nang_luong | đã sửa | pitfalls.1 (Lỗi 2): SHOULD — “đèn báo nguồn… mỗi thứ vài chục đến vài trăm µA” không có nguồn và quá thấp với đèn; đổi thành “từ vài µA tới vài mA” và tính một ví dụ bằng định luật Ôm, ghi “(số minh hoạ)”; thêm `checks`; xoá mục `asr_reviewed` cũ | định luật Ôm như ESY L08; số đèn 2 V, 1 kΩ là số minh hoạ | lint: 0 FAIL, 0 WARN, 30 PASS / render: 72 khung (0 vấn đề) |
| L14_cap_nhat_an_toan | không phát hiện lỗi | — | — | — |
| L15_hanh_trinh_sao_hoa | đã sửa | pitfalls.0: MUST — “bản tóm tắt được chuyển cho khoảng 400 người” sai so với nguồn (“400 people send me copies”); pitfalls.1: MUST — màn hình nói “đặt lại gần 50 lần mỗi ngày” như số đo, lời đọc “có thể”; nguồn ghi đây là cận trên tính trên mẫu → ghi rõ cả hai; hook: SHOULD — “flash bắt đầu mòn” → “nghi phạm hàng đầu” (JPL14a); stage1.2: SHOULD — “518 400 chu kỳ mới gặp một lần lỗi” → cận trên (“in less than 18 hours”); stage3.0: SHOULD — “mỗi sáng gửi lại” không có nguồn → “sau mỗi lần tắt điện”; stage3.1: SHOULD — “lúc khởi động nén bảng” và “phần cứng tự ngắt điện” không có trong RN05 → bỏ “lúc khởi động”, đổi thành “trước đó không có hạn chót buộc việc tắt máy đi tiếp” (RN05 §4); pitfalls.0: SHOULD — “việc dở được biết nhưng không ai được giao” là suy diễn → dẫn đúng câu RN05 §5; pitfalls.1: SHOULD — “11 ngày” → “11 ngày sao Hoả” (“over 11 sols”) | [GR97], [RN05] §4–§6, [JPL14a] trong `audit/esy/sources_L15.md`; JPL news 27/3/2015 (WebFetch 2026-11-08: câu “Only time will tell…” do project manager J. Callas nói, khớp “người quản lý dự án”) | lint: 0 FAIL, 0 WARN, 43 PASS / render: 136 khung (0 vấn đề) |

## Không sửa và vì sao
- L06 hook “mô phỏng số thực bằng phần mềm chậm hàng chục lần”: chỉ là bậc độ lớn, không nói so với gì; không có nguồn đo cụ thể để sửa thành con số khác.
- L08 “mỗi byte có bit xác nhận”: byte cuối khi đọc là NACK (không xác nhận), nhưng vị trí bit thứ 9 vẫn có; để mức người mới.
- L02 “đủ 5 mẫu giống nhau thì phím chắc chắn đã hết nảy”: đúng trong giả thiết “dội tối đa 5 ms” của bài.
- L10 hook “Pathfinder liên tục khởi động lại”: GR97 chỉ nói có nhiều lần đặt lại toàn hệ thống, không ghi số lần; “liên tục” hơi mạnh nhưng không sai nghĩa.
- L14 “chữ ký thật dùng số dài hàng trăm chữ số”: đúng với RSA 2048 bit; ECDSA ngắn hơn (khoảng 78 chữ số).
- Giáo án: `curriculum/esy.yaml` L09 `example` ((1, 4), (1, 5), (2, 10), U = 0,65) khác ví dụ trong bài ((1, 4), (2, 6), (3, 12)); có từ trước, gắn thẻ `VER ESY:L09` của `audit/verify_plan_curricula.py` (không được sửa) nên để nguyên. L10 `example` viết “tác vụ ưu tiên cao chờ mãi”, bài cho thấy chờ 7 đơn vị; ý tưởng không sai, để nguyên. Các bài đã sửa không lệch `objectives`/`example`/`fix` của giáo án.
- `rec()` ESY trong `verify_plan_curricula.py`: không cần đổi (không đổi số nào bộ kiểm đang kiểm).

## Kết quả cuối
- Đồng bộ mẫu: `sync_tpl_from_lesson.py esy --write` ghi lại L03, L04, L13; chạy lại → `tổng: 0 mẫu lệch bài`.
- `scan_ctrl.py`: 0 lượt ở `lessons/esy`, `audit/esy`.
- `audit/esy/verify_esy.py`: `72/72 PASS`
- `tools/lv.py curriculum curriculum/esy.yaml`: `curriculum: 16 bài, 16 đã có đặc tả, 0 lỗi`
