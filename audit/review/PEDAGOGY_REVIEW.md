# Rà soát sư phạm toàn kho: độ trực quan, độ sâu cho người mới, và phần kinh nghiệm chuyên gia

checked_at: 2026-10-31. Người yêu cầu: “rà soát các preview các bài học xem đã đủ trực quan, nội dung đủ chi tiết cho người mới và người
mất gốc chưa, đủ giảng giải từng bước … Và phần nghề nghiệp tình huống cách xử lý của chuyên gia, là các best practices được xây dựng theo
các tình huống có thật theo trục thời gian phát triển của chủ đề đó từ lúc khai sinh đến lúc thành hệ thống lớn …”

## 1. Cách rà
| Bước | Làm gì | Bằng chứng |
|---|---|---|
| Đo bằng máy mọi đặc tả | `audit/review/pedagogy_scan.py` đọc 476 tệp `lessons/**/*.yaml`: thời lượng, số hình `<svg>`, số step làm bằng số, có ôn nền / tự kiểm / chuỗi logic, khung chữ liền, và chấm theo đúng luật E39 của lint | `audit/review/pedagogy_scan.tsv` (OBSERVED) |
| Xem khung bằng mắt | LLM L05 bản cũ (khung 8, 14), bản mới (20, 24, 39, 59, 77); CLD L15 (14 và các khung bảng); CS112 L01 (24); CS115 L24 (8), L44 (20) | ảnh trong `out/<KHOÁ>/<bài>/frames/` |
| Đọc đặc tả | LLM L05 bản cũ đọc toàn văn; đối chiếu cấu trúc phân cảnh của CS115 L02 | — |
| Quét chữ đè trong hình | phép kiểm mới trong `player.html` (`layoutIssues`), chạy `audit/layout_scan.py` trên mọi bài có `<svg>` | `audit/layout_<KHOÁ>.tsv`, `audit/review/svg_overlap_scan.log` |

## 2. Kết quả (OBSERVED, từ đặc tả)

**Kết luận chính.** Nội dung đúng: mọi con số đều có phép kiểm, phát âm đã qua máy nghe, tham chiếu thống nhất. Nhưng phần lớn bài **chưa đủ
cho người mới và người mất gốc**. Có hai nhóm khác hẳn nhau:

1. **19 khoá dựng đợt 2026-10-28 → 30** (AGT, AIF, BCH, CLC, CLD, DAN, DBS, DEN, DSC, DSY, DVO, EVT, LLM, MLO, PLC, SAR, SDP, SEC, SWF,
   WEB; cùng ESY, ROB): gần như mọi bài chỉ có 6 phân cảnh bắt buộc (hook, ký hiệu, một ví dụ, lỗi, quiz, tổng kết). Trung vị 4,3–5,2 phút,
   **1 step làm bằng số mỗi bài**, không có phần ôn nền, không có hình cơ chế, không có bước tự kiểm. Quiz chỉ có một khung đáp án gộp.
   Kiến thức then chốt bị **nêu ra chứ không được dựng lên**. Ví dụ LLM L05 cũ: “12·L·d²” được giải thích bằng đúng một câu, còn cơ chế
   bộ nhớ đệm khoá–giá trị không có hình. Đây là bản tóm tắt tốt cho người đã biết, nhưng chưa phải bài giảng cho người mất gốc.
2. **Các khoá dựng trước** (CS115, CS112, DMS, RBM, NET, TOC, OSY, CSA): dày hơn rõ (6–9 phút, 2–4 step số mỗi bài; CS115 và CS112 có
   ôn nền ở 42/45 và 21/29 bài; RBM có hình ở 15/17 bài). Chỗ thiếu ít hơn nhưng có hệ thống: thiếu hình cơ chế ở đa số bài, phần lớn quiz
   chỉ có một khung đáp án, các khoá NET/TOC/OSY/CSA/DMS/RBM không có bước ôn nền.

| Khoá | Bài | Phút (trung vị) | Bài có hình | Step số/bài (TB) | Có ôn nền | Quiz giải ≥ 2 bước | Mức ĐỦ / GẦN / MỎNG |
|---|---|---|---|---|---|---|---|
| DSC | 15 | 4.3 | 2 | 1.0 | 0 | 0 | 0 / 0 / 15 |
| DVO | 13 | 4.3 | 0 | 1.0 | 0 | 0 | 0 / 0 / 13 |
| SDP | 17 | 4.3 | 0 | 1.1 | 0 | 0 | 0 / 0 / 17 |
| SWF | 13 | 4.4 | 1 | 1.3 | 0 | 0 | 0 / 0 / 13 |
| CLD | 16 | 4.5 | 4 | 1.8 | 1 | 1 | 1 / 0 / 15 |
| DAN | 12 | 4.5 | 0 | 1.0 | 0 | 0 | 0 / 0 / 12 |
| EVT | 11 | 4.5 | 0 | 1.0 | 0 | 0 | 0 / 0 / 11 |
| AGT | 12 | 4.5 | 0 | 1.0 | 0 | 0 | 0 / 0 / 12 |
| DSY | 15 | 4.6 | 4 | 1.0 | 0 | 0 | 0 / 0 / 15 |
| SAR | 13 | 4.6 | 0 | 1.0 | 0 | 0 | 0 / 0 / 13 |
| SEC | 15 | 4.6 | 0 | 1.0 | 0 | 0 | 0 / 0 / 15 |
| MLO | 14 | 4.7 | 0 | 1.0 | 0 | 0 | 0 / 0 / 14 |
| PLC | 13 | 4.7 | 4 | 1.2 | 0 | 0 | 0 / 0 / 13 |
| WEB | 15 | 4.8 | 0 | 1.0 | 0 | 0 | 0 / 0 / 15 |
| DEN | 14 | 4.8 | 0 | 1.0 | 0 | 0 | 0 / 0 / 14 |
| LLM | 14 | 5.0 | 1 | 1.4 | 1 | 1 | 1 / 0 / 13 |
| BCH | 12 | 5.0 | 0 | 1.0 | 0 | 0 | 0 / 0 / 12 |
| ROB | 13 | 5.0 | 0 | 1.0 | 0 | 0 | 0 / 0 / 13 |
| CLC | 12 | 5.1 | 0 | 1.0 | 0 | 0 | 0 / 0 / 12 |
| ESY | 15 | 5.2 | 7 | 1.1 | 0 | 0 | 0 / 0 / 15 |
| NET | 15 | 5.5 | 7 | 2.7 | 0 | 0 | 0 / 0 / 15 |
| AIF | 14 | 5.5 | 0 | 1.1 | 0 | 0 | 0 / 0 / 14 |
| DBS | 17 | 5.7 | 4 | 1.5 | 0 | 0 | 0 / 0 / 17 |
| OSY | 15 | 5.9 | 4 | 2.3 | 0 | 0 | 0 / 0 / 15 |
| CSA | 16 | 6.1 | 1 | 2.4 | 0 | 0 | 0 / 0 / 16 |
| TOC | 14 | 6.5 | 6 | 2.8 | 0 | 0 | 0 / 0 / 14 |
| RBM | 17 | 7.0 | 15 | 1.8 | 0 | 0 | 0 / 0 / 17 |
| DMS | 20 | 7.1 | 4 | 2.9 | 0 | 0 | 0 / 1 / 19 |
| CS115 | 45 | 7.7 | 18 | 4.2 | 42 | 9 | 4 / 20 / 21 |
| CS112 | 29 | 8.6 | 14 | 3.1 | 21 | 0 | 0 / 9 / 20 |

Mức theo luật E39 (`lv.py lint_depth`): ĐỦ = qua mọi điều kiện; GẦN = thiếu 1–2; MỎNG = thiếu ≥ 3. Toàn kho: **6 ĐỦ, 30 GẦN, 440 MỎNG**.
Điều kiện thiếu nhiều nhất: quiz không giải từng bước (465 bài), thiếu ôn nền / hình dung / tự kiểm (417), không có hình cơ chế (397),
chỉ 1 step làm bằng số (283). Dòng CLD và LLM đã gồm 2 bài mẫu mới; con số ĐỦ của CS115 (4) là bài sẵn đạt chuẩn.

**Phần nghề nghiệp — kinh nghiệm chuyên gia (OBSERVED từ `curriculum/*.yaml`):**
- 8 khoá kế hoạch (PAR, RLN, CVI, GFX, IRS, HCI, SEP, CAS) đã có bài tình huống ở cuối khoá trong giáo án, nhưng chưa có đặc tả.
- Trong 30 khoá đã dựng, chỉ 5 khoá có bài “tổng hợp”: SDP L16, SAR L12, AIF L13, CS112 L27–L28, CS115 L33.
- **Không có bài nào theo trục thời gian** của một hệ thống thật, đi từ lúc khai sinh tới quy mô lớn rồi ổn định. Kinh nghiệm chuyên gia
  hiện chỉ nằm rải rác trong phần hook và phần lỗi thường gặp.

**Bố cục hình (phép kiểm mới):** chữ đè nhau trong hình chưa từng được kiểm. Lỗi thật đã tìm thấy:
- CLD L15 bản đầu: nhãn dòng thời gian đè nhau; đã vẽ lại ở khổ 1700 px.
- CS115 L24: nhãn “x + y = 10” nằm đúng trên đường đỏ và đè nhãn “9”; đã dời xuống dưới trục.
Báo nhầm (hai dòng nhãn xếp sát nhau): CS112 L01, CS115 L44. Đã siết điều kiện: chỉ báo khi phần chồng dọc lớn hơn 35% chiều cao dòng chữ.

## 3. Đã làm trong đợt này
| Việc | Tệp | Kiểm |
|---|---|---|
| Chuẩn độ sâu cho người mới (luật 22) | `references/pedagogy.md`; lint **E39** khi bài khai `depth: full` | `tests/test_lint.py`: bắt bài thiếu hình, thiếu ôn nền; 0 FAIL |
| Chuẩn bài hành trình theo trục thời gian (luật 23) | `references/case-lessons.md` mục 5; lint **E40** khi bài khai `case: journey` | test: bắt chặng đảo năm, chặng không tính lại số |
| Mẫu bài | `lesson_template.yaml` (mặc định `depth: full`, đủ 10 nhịp), `journey_lesson_template.yaml` mới, `lv.py new --kind journey` | tạo thử từ mẫu → lint 0 FAIL |
| Đo toàn kho | `audit/review/pedagogy_scan.py` (chấm bằng chính `lint_depth`) | bảng §2 |
| Kiểm chữ đè trong hình | `player.html` `layoutIssues` → `render` FAIL, `layout_scan.py` báo | tìm được 2 lỗi thật, đã sửa |
| **Bài mẫu 1 — viết lại LLM L05** theo `depth: full` | `lessons/llm/L05_chi_phi_tinh_toan.yaml` | 4,4 → **9,7 phút**; 0 → 2 hình cơ chế; 1 → 10 step số; thêm ôn nền, suy 12·L·d² từ 4d² + 8d², tự kiểm “đọc chậm hơn tính 300 lần”, lỗi chuyên gia “gộp 16 chuỗi chỉ được 339 chứ không 1248 từ tố/giây”, quiz quyết định “thẻ 80 GB phục vụ 8 chuỗi”. verify PASS, ASR 17 câu gắn cờ đều có lý do |
| **Bài mẫu 2 — CLD L15 hành trình Borg → Omega → Kubernetes** | `lessons/cld/L15_hanh_trinh_borg_kubernetes.yaml`, nguồn trích nguyên văn `audit/cld/sources_L15.md` | 5 chặng, mỗi chặng có quy mô, điểm nghẽn, cách xử lý, thực hành tốt và con số tính lại (2000–3000 máy; 4,32 phút; 100/600 khoá; 410 ngày; 3 → 4 tháng). Nguồn: EuroSys 2015, ACM Queue 2016, blog Kubernetes 2024. Cách đọc “Borg” dò bằng ASR: “Bo-gờ” 7/8 (PARTIAL) |
| CLD L14 | thêm câu nối sang bài 15, bỏ câu “cảm ơn đã theo hết khoá” | dựng lại, verify PASS |

## 4. Kế hoạch tiếp (đề xuất, theo thứ tự giá trị)
**Đợt A — viết lại 19 khoá “nén” theo `depth: full`** (≈ 270 bài). Thứ tự theo số nghề dùng tới (TRACKS.md):
1. AIF, LLM, SWF, SDP, DBS, SEC — nền chung của nhiều nghề.
2. CLD, CLC, DVO, SAR, DSY, EVT, DEN — hệ thống và dữ liệu.
3. DSC, DAN, MLO, AGT, WEB, BCH, PLC, ESY, ROB.

Mỗi bài viết lại theo khung bài mẫu LLM L05. Không đổi số bài, không đổi mục tiêu; giữ con số và `checks` đã kiểm, chỉ thêm phần dựng
kiến thức. Mỗi khoá xong thì đi đủ các cổng §7 của ROADMAP. Chi phí đo được: dựng và ASR ≈ 7–10 phút máy cho bài 10 phút (LLM L05: dựng
lần đầu 84 câu, ASR 175 s).

**Đợt B — bổ sung cho 8 khoá dày:** thêm hình cơ chế, thêm bước ôn nền cho NET, TOC, OSY, CSA, DMS, RBM, và tách đáp án quiz thành từng
bước. Viết theo bài, không viết lại cả bài.

**Đợt C — mỗi khoá một bài hành trình** (`--kind journey`), đánh số tiếp sau bài cuối. Nguồn ứng viên ở ROADMAP §8.1 (NOT_VERIFIED: phải
đọc nguyên văn trước khi soạn, như CLD L15).

## 5. NOT_VERIFIED
- Hiệu quả với người học thật: bài dài hơn chưa chắc tốt hơn với mọi người. Cần đo tỉ lệ xem hết và điểm quiz trước/sau (ROADMAP §8.2).
- Ngưỡng của E39 (≥ 4 step số, ≥ 900 từ, ≤ 3 khung chữ liền) đặt theo bài mẫu và theo các khoá dày (CS115, CS112), chưa hiệu chỉnh trên
  người học.
- Phát âm “Borg” → “Bo-gờ”: máy nghe 7/8, bản chép gần âm chứ không ra đúng chữ “Borg”; cần người nghe.
