# SDP — đã đọc 18/18 bài

Đọc kiểm lần ba (đợt C, 2026-11-09) toàn bộ `lessons/sdp/L00–L17.yaml` và `curriculum/sdp.yaml` theo `audit/review/FULL_REVIEW_BRIEF_C.md`.
Đã đọc mọi `show` (cả chữ trong SVG), `say`, `checks`, quiz, mục giáo án, `audit/sdp/sources_L17.md`. Mọi con số trên màn hình/lời đọc
được tính lại (kể cả số không có `checks`); số mới thêm đều có `checks` mới. Đối chiếu: GoF 1994, Martin (ASD 2002, Clean Architecture
2017), Fowler Refactoring 2e (2018), semver.org 2.0.0, Liskov–Wing 1994, McCabe 1976, các bài Shopify [DM19] [UD20] [PW20] [PR24].

Tổng: 16/18 bài sửa; 1 MUST, 16 SHOULD; check_xref SDP 16 → 0 lượt. Giáo án: mục `objectives` của cả 18 bài đồng bộ đúng theo bài.

| Bài | Kết luận | Lỗi nội dung đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Độc lập (tham chiếu khoá khác đã thay bằng gì) | Nguồn | lint / render |
|---|---|---|---|---|---|
| L00 | đã sửa | giáo án `fix`: SHOULD — “cận dưới số ca kiểm phủ nhánh cơ sở” dễ hiểu là độ phủ nhánh (M là cận **trên** cho độ phủ nhánh) → “M là số đường trong một bộ đường cơ sở, cần ít nhất M ca kiểm để phủ bộ đó” | sym: bỏ “như độ phủ ở SWF / khoá Phần mềm đúng đắn”; thêm bước giảng “đường độc lập”, “bộ đường cơ sở” với hàm `dau(x)`: M = 2, hai ca x = 3 / x = −1 (2 `checks` mới) | McCabe, IEEE TSE 2(4), 1976 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L01 | đã sửa | pitfalls.3: SHOULD — “thử lại 3 lần … 3 lần đều ValueError, mất 7 giây”: chờ 1 + 2 + 4 = 7 giây cần lần đầu + 3 lần thử lại = 4 lần → sửa màn hình, lời đọc, check `range(1 + 3)` | example bước 5: bỏ “như tiền điều kiện ở SWF / khoá Phần mềm đúng đắn”; giảng tiền điều kiện + ví dụ `tinh_tien(12, 5000)` = 60 000 (check mới) | Shore, Fail Fast, IEEE Software 21(5) 2004 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L02 | đã sửa | pitfalls.2: SHOULD — “như bước duy trì của bất biến vòng lặp” dùng khái niệm chưa dạy → nối về lập luận bất biến đã làm ở cảnh tự kiểm (đúng lúc tạo + mỗi thao tác giữ) | prereq: “Ở khoá Phần mềm đúng đắn, bất biến là…” → “Tiếp theo, ta cần hiểu bất biến…” + câu ích lợi; sym: bỏ “như bất biến cấu trúc dữ liệu ở SWF”, định nghĩa “thao tác công khai” | Meyer OOSC 2e ch. 11; Parnas 1972 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L03 | đã sửa | — (bổ sung giảng, không có sai kiến thức) | sym: bỏ “(tiền, hậu điều kiện như SWF)”; giảng tiền/hậu điều kiện ngay trong bài với `area()` chữ nhật 3 × 4 → 12 ≥ 0 (check mới); pitfalls.3 nhắc lại nghĩa “thất bại sớm” | Meyer OOSC 2e ch. 14; GoF §1.6 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L04 | đã sửa | example.0: SHOULD — mã chỉ có **một** lớp `Them` nhận giá làm tham số, trong khi bài đếm “4 lớp thêm” → nói rõ một lớp dùng chung được, 4 lớp khi mỗi thứ có cách tính riêng, vẫn tăng theo tổng | không có lượt | GoF §1.6; Bloch EJ 3e mục 18 | lint: 0 FAIL, 0 WARN, 21 PASS; render: 65 khung (0 vấn đề) |
| L05 | đã sửa | sym: SHOULD — tiêu đề “SOLID 1” và “(chữ S/O)” không giải thích → thêm dòng màn hình SOLID = chữ cái đầu năm nguyên lý (lời đọc không đọc chữ SOLID); `source`: SHOULD — trách nhiệm đơn không có trong Martin 2000 → dẫn ASD 2002 ch. 8–9, Clean Architecture 2017 ch. 7 | không có lượt | Martin ASD (2002); Martin Clean Architecture (2017) | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L06 | đã sửa | sym: SHOULD — phát biểu Liskov–Wing là tính chất **chứng minh được** từ đặc tả lớp cha (bản cũ “mọi tính chất đúng”) | prereq: bỏ “như ở khoá Phần mềm đúng đắn” (phần giảng tiền/hậu điều kiện có sẵn, đủ ví dụ số) | Liskov & Wing, TOPLAS 16(6) 1994 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L07 | đã sửa | sym: SHOULD — “đối tượng giả” là mục tiêu bài nhưng chưa định nghĩa → thêm định nghĩa + ví dụ ngày cố định 1/1/2025 | không có lượt | Martin DIP 1996; Fowler 2004 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L08 | đã sửa | sym: SHOULD — Builder trình bày theo dạng nhiều tham số tuỳ chọn (Bloch) mà không nói ý định GoF (tách quá trình dựng khỏi biểu diễn) → thêm chú thích màn hình + lời đọc; `source` thêm Bloch EJ 3e mục 2 | không có lượt | GoF 1994 ch. 3; Bloch EJ 3e mục 2 | lint: 0 FAIL, 0 WARN, 17 PASS; render: 70 khung (0 vấn đề) |
| L09 | không phát hiện lỗi | — (tính lại 37,0 °C, 37, 220, 20 nút / 8 nút, 100 °C, 20 đều đúng) | không có lượt | GoF 1994 ch. 4 | lint: 0 FAIL, 0 WARN (không sửa) |
| L10 | đã sửa | example: SHOULD — mục tiêu 1 “thay thuật toán lúc chạy bằng mẫu chiến lược” không có ví dụ chạy → thêm bước 5 phí giao theo cân / theo km (2 · 10 000 = 20 000; 8 · 3 000 = 24 000, số minh hoạ, check mới); “phí ship” → “phí giao hàng” | không có lượt | GoF 1994 ch. 5 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L11 | đã sửa | example: SHOULD — mục tiêu 3 (khuôn thuật toán) không có ví dụ → thêm bước 5 `XuatBaoCao` / `XuatChuoi` → "3,5" / `XuatTong` → 8 (check chạy thật) | prereq: “ôn máy trạng thái ở khoá Phần mềm đúng đắn” → định nghĩa máy trạng thái ngay tại chỗ (bảng công tắc đèn có sẵn) | GoF 1994 ch. 5 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L12 | đã sửa | — | prereq + pitfalls.1: bỏ “ở/như khoá Ngôn ngữ lập trình”; giảng “phép gán không sao chép → chia sẻ tham chiếu”, nối về ví dụ `b = a` trong bài | SICP 2e §1.2.2; functools.lru_cache | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L13 | đã sửa | — | prereq: bỏ “Ở khoá Phần mềm đúng đắn, kiểm thử theo tính chất…”; giảng kiểm thử theo tính chất với ví dụ “tổng ≥ tiền hàng + thuế” trên 1001 × 31 = 31 031 cặp (check mới) | Fowler Refactoring 2e; Feathers 2004 ch. 13 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L14 | đã sửa | sym: SHOULD — “API”, “chữ ký hàm” dùng mà chưa định nghĩa → thêm định nghĩa; pitfalls.3: SHOULD — lời đọc “1 chấm 9, 1 chấm 10, 1 chấm 2” lệch màn hình 1.9.0/1.10.0/1.2.0 → đọc đủ ba số | không có lượt | semver.org 2.0.0 (truy cập 2026-11-09); Hyrum’s Law | lint: 0 FAIL, 0 WARN, 19 PASS; render: 71 khung (0 vấn đề) |
| L15 | đã sửa | pitfalls.1: SHOULD — câu trong ngoặc kép “khi một độ đo trở thành mục tiêu…” là cách phát biểu của M. Strathern (1997), không phải nguyên văn Goodhart (1975) → ghi rõ trên màn hình và `source` | không có lượt | Goodhart 1975; Strathern, European Review 5(3), 1997 | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |
| L16 | không phát hiện lỗi | — (405 000, 250 000, 315 000, 300 000, 355 000 / 360 000 đều đúng) | không có lượt (chỉ tham chiếu bài trong khoá, có nhắc lại định nghĩa) | GoF ch. 5; Fowler 2e ch. 1 | lint: 0 FAIL, 0 WARN (không sửa) |
| L17 | đã sửa | stage1: SHOULD — [DM19] chỉ nêu ví dụ giả định (“**if** the code that calculates our shipping rate called into … tax”), bài trình bày như sự kiện năm 2016 kèm “không rõ vì sao” (không có trong nguồn) → viết lại theo đúng nguồn; SHOULD — “2016 − 2006 = 10 năm” trong khi nguồn ghi “since at least 2006” → “ít nhất 10 năm”. Giáo án `example`: **MUST** — “lần quét hơn 1 giờ → nhiều nhất 8 lần” sai (480 / >60 → chưa tới 8, bài nói đúng) → “chưa tới 8 lần”; ghi “(phép tính minh hoạ với 37)” | không có lượt | [DM19] [UD20] [PW20] [PR24]; đã mở lại [UD20] và [PR24] 2026-11-09: khớp chi tiết “shop billing settings … fraudulent”, khởi động hỏng do initializers/environment files/mã không qua Zeitwerk, Wedge nhiều nhiễu, “interface patterns” | lint: 0 FAIL, 0 WARN; render (0 vấn đề) |

## Giáo án `curriculum/sdp.yaml`
- `objectives` của cả 18 mục thay bằng đúng `objectives` của bài (trước đó lệch chữ ở 17 mục; vài mục hứa ít hơn hoặc khác bài, như L01, L03).
- L00 `fix`, L17 `example` sửa như bảng trên. `title` cả 18 mục khớp tiêu đề bài bỏ “Bài N —”. Không nhắc khoá khác trong `title/objectives/example/fix`
  (chú thích đầu tệp và `requires_ext` giữ nguyên theo B.1).
- Không đổi số nào mà `audit/verify_plan_curricula.py` (rec SDP) kiểm → không cần đổi `rec()`.

## Không sửa và vì sao
- L00 quiz: hàm `g` có M = 4 nhưng một đường (trả "c") không chạy tới được; bài đã nói rõ đó là mã chết. Câu “cần ít nhất 4 ca kiểm” giữ (đúng theo định nghĩa bộ đường cơ sở).
- L11: mẫu duyệt chỉ có định nghĩa + lỗi “sửa khi đang duyệt” (có ví dụ số), chưa có ví dụ tự viết bộ duyệt; không thêm để tránh cảnh quá dài — mục tiêu “duyệt không lộ cấu trúc” được giảng ở mức khái niệm.
- L13: “số ma thuật” được gọi là mùi mã; danh mục mùi của Fowler 2e không có mục này (2e có phép tái cấu trúc “Replace Magic Literal”). Bảng không ghi là danh mục của Fowler nên giữ.
- L15: Martin đếm Ca/Ce theo số lớp ngoài gói; bài đếm theo mô-đun — đơn giản hoá hợp lý, công thức I không đổi.
- L06: bảng “lớp con được thêm thao tác mới” — Liskov–Wing đòi thao tác mới còn giữ ràng buộc lịch sử; giữ vì dòng kế bên đã ghi “không được phá bất biến”.
- L14: semver mục 4 (bản 0.y.z cho phép đổi bất kỳ) không dạy; bài không dùng bản 0.y.z trên màn hình.

## Dương tính giả của check_xref
- Không có. (Dòng “Đây là bài cuối của khoá SDP” ở L17 nói về chính khoá này; công cụ không báo.)

## Kết quả cuối
- `audit/sdp/verify_sdp.py`: TỔNG: 36 PASS · 0 FAIL
- `check_xref.py --course SDP`: trước 16 lượt ở 8 tệp → sau 0 lượt (không còn dòng “SDP: …”; dòng tổng của toàn kho: “check_xref: 478 lượt tham chiếu sang khoá khác ở 204 tệp”, đều thuộc khoá khác)
- `lv.py curriculum curriculum/sdp.yaml`: curriculum: 18 bài, 18 đã có đặc tả, 0 lỗi
- `scan_ctrl.py`: không có lượt nào ở SDP
