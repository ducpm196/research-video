# DVO — đã đọc 14/14 bài

Đọc toàn bộ `show`, `say`, `checks`, chữ trong hình SVG, quiz và đáp án của từng bài (2026-11-08). Khoá không có mẫu `audit/dvo/src/*.tpl.yaml` → không chạy `sync_tpl_from_lesson.py`. Tổng: 7 bài đã sửa, 3 mục MUST, 9 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — (chia đôi 3→2, 30→5, 300→9; SVG 8 thay đổi khớp lời đọc; quiz 25/325 → 5/9 đúng) | Humble & Farley, Continuous Delivery (2010) ch. 1 | — |
| L01 | đã sửa | recap: SHOULD — chuỗi màn hình ghi “giấu sau cờ”, thuật ngữ “cờ” chưa giới thiệu trong bài, lời đọc nói “công tắc tính năng” → sửa màn hình thành “công tắc tính năng” | Hodgson, Feature Toggles (martinfowler.com, 2017) | lint: 0 FAIL, 0 WARN, 21 PASS · render: 68 khung (0 vấn đề) |
| L02 | không phát hiện lỗi | — (so chuỗi/so số, ký tự thứ ba/thứ năm, khoảng [1.4.0, 2.0.0) đều đúng) | SemVer 2.0.0 §11 | — |
| L03 | đã sửa | sym: SHOULD — “kiểm thử tích hợp … (có cơ sở dữ liệu thật)” như thể định nghĩa bắt buộc → “ví dụ cùng cơ sở dữ liệu thật” (màn hình + lời đọc) | Cohn, Succeeding with Agile (2009), tháp kiểm thử | lint: 0 FAIL, 0 WARN, 21 PASS · render: 67 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — (zip 128 byte, 6 byte khác ở vị trí 10–12, 66–68 do checks dựng thật) | Reproducible Builds, SOURCE_DATE_EPOCH | — |
| L05 | đã sửa | example bước 4: SHOULD — màn hình viết tắt “CLD” (người mất gốc không biết), lời đọc nói “khoá Hệ thống hướng dịch vụ” → màn hình ghi đủ tên khoá | series của `lessons/cld/L00` (“CLD · Hệ thống hướng dịch vụ”) | lint: 0 FAIL, 0 WARN, 22 PASS · render: 69 khung (0 vấn đề) |
| L06 | không phát hiện lỗi | — (T/2: 45, 3,5, 15 ngày; thứ tự xử lý lộ mật khẩu đúng OWASP) | OWASP Secrets Management Cheat Sheet | — |
| L07 | không phát hiện lỗi | — (nhị thức 0,0033 / 0,0069 / 0,0138 / 0,0824 / 0,897 / 0,62; diễn giải p-giá trị đúng) | Google SRE Workbook ch. 16 | — |
| L08 | đã sửa | example bước 3: SHOULD — bỏ sót điều kiện: chép bù chỉ dòng `ho_ten` trống không bắt được dòng cũ mà bản cũ **sửa** cột `ten` → thêm ghi chú (màn hình + lời đọc); thêm `clear: true` ở bước 4 vì tràn khung. Lỗi 3: SHOULD — “cập nhật 100 triệu dòng … khoá bảng hàng giờ” (tuyệt đối; Postgres/InnoDB khoá dòng) → “có thể giữ khoá trên mọi dòng đó hàng giờ, chặn các lệnh ghi khác” | Sato, ParallelChange (martinfowler.com, 2014); PostgreSQL docs §13.3 Explicit Locking (row-level locks của UPDATE) | lint: 0 FAIL, 0 WARN, 22 PASS · render: 73 khung (0 vấn đề) |
| L09 | đã sửa | recap: MUST — “dùng trung vị cho thời gian” mâu thuẫn chính ví dụ của bài (thời gian khôi phục tính trung bình 55 phút) → “trung vị cho thời gian đưa lên”. sym: SHOULD — mang tính thời điểm: bốn chỉ số là bộ gốc 2018, DORA hiện dùng năm chỉ số và đổi tên chỉ số khôi phục → thêm ghi chú (màn hình + lời đọc) | dora.dev/guides/dora-metrics (truy cập 2026-11-08, no revision given): “shifting from the original four keys to the current five-metric model”, “from MTTR to Failed Deployment Recovery Time” | lint: 0 FAIL, 0 WARN, 19 PASS · render: 78 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — (720/721, 720/720,25, 1440/1441 = 360/360,25 đúng) | Google SRE Book (2016) ch. 14–15 | — |
| L11 | đã sửa | sym: SHOULD — “p99” / “phân vị 99” dùng mà không giải thích → “1% yêu cầu chậm nhất mất trên 2 giây”. example bước 3: SHOULD — “≈ 2,6 TB” trong khi bài chỉ định nghĩa KB/MB/GB và lời đọc nói “2,6 nghìn GB” → màn hình “2,6 nghìn GB” | Google SRE Book ch. 6 (bốn tín hiệu vàng, phân vị độ trễ) | lint: 0 FAIL, 0 WARN, 19 PASS · render: 63 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — (RSA đồ chơi 61·53, d = 2753, băm 1917, chữ ký 2336, bình phương liên tiếp đúng; quét lỗ hổng a, c đúng) | Rivest–Shamir–Adleman (1978) | — |
| L13 | đã sửa | check: MUST — bảng ghi “≈ 208 lần (2016, 2019)” nhưng báo cáo 2016 ghi “200 times” → “(2019; năm 2016 cùng phép tính nhưng báo cáo ghi tròn 200)”. stage4: MUST — bảng “điều báo cáo 2021 ghi” gán cho báo cáo một suy luận không có trong nguồn (“973 lớn vì nhóm thấp tụt”) và ghi chú “Năm 2024, chính nhóm nghiên cứu viết lại” (trang DH26 không ghi ngày đó; lời đọc nói “về sau”) → tách “tính lại” khỏi “báo cáo ghi”, nêu phép tính 7 → 1,5 lần/năm, đổi “Năm 2024” thành “Về sau”; thêm check `(2 + 12) / 2 == 7`. stage5 bước 4: SHOULD — “99%, báo cáo ghi là do làm tròn”: báo cáo 2023 không có ghi chú làm tròn (chỉ 2019 có) → “báo cáo không ghi vì sao thiếu 1%, có thể do làm tròn”; sửa mô tả `rec L13b` trong `verify_dvo.py` cho khớp. Đã ghi bổ sung vào `audit/dvo/sources_L13.md` | 2016 State of DevOps tr. 4, 5, 8, 14, 16 (“200 times”, “more than 25,000 … over the past five years”); 2021 tr. 13 (“Yes, you read correctly. This is not an editorial error.” — xác nhận câu ở hook); 2023 tr. 12 (bảng 18/31/33/17, không có chữ “round…” ở ghi chú) — PDF tải lại 2026-11-08 từ services.google.com/fh/files/misc/ | lint: 0 FAIL, 0 WARN, 31 PASS · render: 132 khung (0 vấn đề) |

## Không sửa và vì sao
- L04 prereq: lời đọc “mã băm khác hoàn toàn, không giống dù chỉ vài ký tự” — hai mã `f9b197ffdaa4` / `67fac6d42ab9` trùng đúng 1 vị trí (chữ `a`), không phải “vài”, nên câu vẫn đúng; sửa sẽ làm mất mục `asr_reviewed` đã duyệt.
- L04 Lỗi 1: màn hình dùng “thăng hạng” còn lời đọc nói “đưa lên” — nghĩa rõ từ ngữ cảnh, không phải sai kiến thức.
- L10: định nghĩa MTBF là “thời gian trung bình giữa hai lần hỏng” rồi dùng như thời gian chạy tốt trong A = MTBF/(MTBF+MTTR). Có sách tách MTTF và MTBF = MTTF + MTTR; bài nói rõ “mỗi chu kỳ chạy tốt một khoảng MTBF”, nên nhất quán trong bài, là cách dùng thường gặp trong SRE.
- L06 Lỗi 4: “thu hồi khoá cũ ngay thì tới 20 máy bị từ chối” giả định kết nối cũ bị cắt; có hệ giữ kết nối đã mở. Bài đã ghi số minh hoạ, giữ nguyên.
- L02: không nói quy ước SemVer cho bản 0.x (mọi thứ có thể đổi); bài không khẳng định ngược lại, quiz c (0.9.0 → 1.0.0) đã cảnh báo đổi số chính.
- `curriculum/dvo.yaml` L11 vẫn ghi “khoảng 2,6 TB” — giá trị bằng 2,6 nghìn GB, giáo án không đọc thành lời, không lệch bài.
- L13 stage 2 `stage.scale` “hơn 25 000 người trả lời qua năm năm” chưa có trong `sources_L13.md`; đã kiểm nguyên văn 2016 tr. 4, 8 và ghi bổ sung, không cần sửa bài.

## Kết quả cuối
- `audit/dvo/verify_dvo.py`: `TỔNG: 18 PASS · 0 FAIL`
- `tools/lv.py curriculum curriculum/dvo.yaml`: `curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi`
- `audit/review/scan_ctrl.py`: 8 lượt, tất cả ở `lessons/jva` (khoá khác), 0 ở DVO.
- `audit/review/prune_stale_asr.py lessons/dvo/*.yaml`: 0 mục cũ.
- `rec()` DVO trong `audit/verify_plan_curricula.py`: không cần đổi (không đổi con số nào mà rec kiểm).
