# WEB — đã đọc 16/16 bài

Đọc kiểm 2026-11-08: mọi cảnh, mọi `show`/`say`/`checks`, quiz và đáp án của `lessons/web/L00`…`L15`. Khoá WEB không có mẫu `audit/web/src/*.tpl.yaml` (không cần đồng bộ mẫu).
Tổng: 9 bài đã sửa, 7 bài không phát hiện lỗi; 2 mục MUST, 9 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | RFC 8446 (TLS 1.3 bắt tay 1 vòng), RFC 9110 | — |
| L01 | không phát hiện lỗi | — | WHATWG HTML; WAI-ARIA (vai trò không thêm tabindex) | — |
| L02 | đã sửa | example, quiz: MUST — `border: 5px` thiếu kiểu nét thì bề rộng viền tính ra 0, nên phép 200 + 2·20 + 2·5 = 250 sai với chính mã trên màn hình; sửa thành `border: 5px solid` / `2px solid`, thêm câu giải thích, lời đọc “viền nét liền”. pitfalls (lỗi 4): SHOULD — bộ chọn “của mình” `.item` không nhắm cùng liên kết với `.nav .item a` (`.item` là phần tử cha); đổi thành `.moi` gắn trên chính liên kết, sửa `checks` tương ứng | W3C CSS Backgrounds and Borders Level 3 §4.1, §4.3 (border-style mặc định `none`; border-width tính ra 0 khi kiểu nét là none) — truy cập 2026-11-08, no revision given | lint: 0 FAIL, 0 WARN, 22 PASS; render: 78 khung (0 vấn đề) |
| L03 | không phát hiện lỗi | — | WHATWG HTML §8.1.7; chạy Node (verify_web L03) | — |
| L04 | đã sửa | pitfalls (lỗi 2): SHOULD — “máy chủ đích từ chối” nói như chắc chắn; sửa “có thể từ chối, trình duyệt tốn bộ nhớ và cạn kết nối” | RFC 9112 §9.4 (máy khách nên dè dặt khi mở nhiều kết nối) | lint: 0 FAIL, 0 WARN, 23 PASS; render: 67 khung (0 vấn đề) |
| L05 | không phát hiện lỗi | — | tài liệu React — Reconciliation | — |
| L06 | đã sửa | pitfalls (lỗi 3): SHOULD — 403 “đăng nhập lại cũng vô ích” tuyệt đối; RFC cho phép thử lại với thông tin xác thực khác → “đăng nhập lại bằng cùng tài khoản cũng vô ích”. `source`: thêm RFC 6585 cho mã 429 (không thuộc RFC 9110) | RFC 9110 §15.5.4; RFC 6585 §4 | lint: 0 FAIL, 0 WARN, 20 PASS; render: 78 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — | SQLite EXPLAIN QUERY PLAN (verify_web L07) | — |
| L08 | đã sửa | hook: SHOULD — “một nửa người dùng vẫn chạy bản cũ” là con số không nguồn → “nhiều người dùng” | — (bỏ con số không nguồn) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 74 khung (0 vấn đề) |
| L09 | đã sửa | prereq: SHOULD — “hàm băm biến chuỗi … thành đúng 32 byte” nói như mọi hàm băm; ghi rõ SHA-256 (hàm PKCE dùng) | RFC 7636 §4.2 (S256 = SHA-256); NIST FIPS 180-4 | lint: 0 FAIL, 0 WARN, 21 PASS; render: 75 khung (0 vấn đề) |
| L10 | đã sửa | example (bước 4): SHOULD — gọi ảnh chính là “trên đường kết xuất”; ảnh không chặn lần vẽ đầu, chỉ làm chậm nội dung lớn nhất hiện ra → đổi tiêu đề cột và lời đọc; xoá mục `asr_reviewed` cũ | web.dev — “Largest Contentful Paint”, “Critical rendering path” (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 70 khung (0 vấn đề) |
| L11 | đã sửa | pitfalls (lỗi 1): SHOULD — “khoảng 8% nam giới” là tỉ lệ ở người gốc châu Âu → “khoảng 5–8%, tuỳ nhóm dân”; `source`: thêm WCAG 2.2 tiêu chí 1.4.11 (ngưỡng 3 : 1 cho biểu tượng, viền ô nhập, viền tiêu điểm); xoá mục `asr_reviewed` cũ | J. Birch, Worldwide prevalence of red-green color deficiency, JOSA A 29(3):313–320 (2012); W3C WCAG 2.2 SC 1.4.11 | lint: 0 FAIL, 0 WARN, 20 PASS; render: 71 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — | tài liệu Android/Apple về vòng đời (bài đã ghi) | — |
| L13 | không phát hiện lỗi | — | Shapiro và cs. (SSS 2011); Kleppmann và cs. (Onward! 2019) | — |
| L14 | đã sửa | hook: SHOULD — “khoảng một phần tư người dùng vẫn chạy bản cũ” sau 4 tuần là kết quả của mô hình 30%/tuần nhưng nói như sự thật → ghi “(số minh hoạ)” trên màn hình và lời đọc | — (mô hình hình học của chính bài) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 72 khung (0 vấn đề) |
| L15 | đã sửa | stage5 + intuition + stage2: MUST — tính khoảng giữa các phiên bản theo năm RFC 2616 (1999) thay vì bản HTTP/1.1 đầu tiên RFC 2068 (1/1997): “1.0 → 1.1 mất 3 năm, 1.1 → 2 mất 16 năm” sai → 8 tháng (5/1996 → 1/1997) và 18 năm (1997 → 2015); trục thời gian ghi “1997–1999: bản 1.1”, chặng 2 ghi rõ bản 1999 là bản sửa; sửa `checks`, `stage.scale`, `source`, `audit/web/verify_web.py` L15 (chú thích có nguồn) và `audit/web/sources_L15.md` (thêm [R97], câu trích nguyên văn). stage1: SHOULD — “khai sinh” cho năm 1996 (RFC 1945 ghi lại “current practice”, HTTP có từ trước) → “bản ghi chuẩn đầu tiên” | RFC 2068 (1/1997) §8.1.1, §8.1.2.2, §8.1.4, rfc-editor.org/rfc/rfc2068.txt, truy cập 2026-11-08; RFC 1945 §1.3 | lint: 0 FAIL, 0 WARN, 32 PASS; render: 105 khung (0 vấn đề) |

## Không sửa và vì sao
- L00, L15: đếm vòng bỏ qua 0-RTT/TLS chi tiết — đúng quy ước bài đã ghi (L00 đếm TLS 1.3 = 1 vòng, L15 bỏ phần mã hoá cho công bằng giữa các phiên bản).
- L01 lỗi 3: “trình đọc màn hình chỉ đọc tên tệp” khi ảnh thiếu `alt` — hành vi khác nhau giữa các trình đọc; mức đơn giản hoá chấp nhận được, không đủ căn cứ là sai.
- L08 lỗi 4: “mã băm trong tên: 1 GB mỗi ngày (chỉ lần mở đầu)” ngầm giả định mỗi ngày tải lại một lần — đã ghi “số minh hoạ”.
- L11 lỗi 3: thuộc tính `placeholder` có thể được dùng làm tên dự phòng (HTML-AAM), nên “đọc ô nhập, trống” không phải luôn đúng; câu bài vẫn đúng ý (placeholder không thay được nhãn) — để nguyên.
- L15: RFC 1945 là Informational, bài gọi chung “bộ chuẩn năm 1996” — cách gọi lỏng, không đổi kiến thức.
- L06: `Idempotency-Key` vẫn là bản thảo IETF — bài đã ghi “bản thảo”.
- `audit/verify_plan_curricula.py` rec("WEB:L15") không mã hoá khoảng năm → không cần đổi.

## Kết quả cuối
- `audit/web/verify_web.py`: `verify_web: 16/16 PASS`
- `tools/lv.py curriculum curriculum/web.yaml`: `curriculum: 16 bài, 16 đã có đặc tả, 0 lỗi` (đã sửa mục L02 `example`/`fix` và L15 `fix` cho khớp bài)
- `audit/review/scan_ctrl.py`: 0 lượt ở `lessons/web/`
