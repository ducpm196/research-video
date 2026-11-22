# Kiểm định độc lập Stage 10 — Khoá `HCI` (`L00–L12`, 13/13 bài)

> Ghi chú phương pháp: Chỉ đọc 100%, không sửa tệp, không mở `audit/review/audit_final/reports/`, không dùng `bash.exe`/`cham.sh`. Mọi phép tính được kiểm lại độc lập bằng Python (`.venv/Scripts/python.exe`), mọi lab được chạy trực tiếp bằng Python và đối chiếu `mong_doi.txt`.

---

## 1. Bảng tóm tắt chỉ số hệ thống (13 bài `HCI:L00–L12`)

| Chỉ số kiểm định | Kết quả | Chi tiết |
|---|---|---|
| Số bài `MUST = 0` (về **kiến thức chuyên môn & phép tính**) | **13/13** (nếu tính lỗi quy trình/hiển thị chặn Stage 10 như `covers:` lệch, `P8` lộ lời giải trước `pause`, `de.md` thiếu format, `L10` SVG chữ tàng hình vào `MUST` thì **0/13**) | Kiến thức HCI, định nghĩa, công thức, kiểm chứng số học đều đúng; nhưng có lỗi quy trình & hiển thị mức `MUST` ở cả 13 bài |
| Số bài `P1 = 2` (chuẩn `BRIEF_R4.md` chặt: thân bài + `practice#0/#1` + `de.md`) | **0/13** | Cả 13 bài đều có `≥ 3` mục chưa giảng (`P1 = 0`) |
| Số bài `P8 = 2` (chuẩn chặt: không lộ trước `pause`, `de.md` tự đứng + có format stdout, số mới, khớp logic) | **0/13** | 13/13 bài đạt `P8 = 1`: lộ `loi_giai.py` + `mong_doi.txt` trước `pause`, `de.md` không có format stdout và thiếu dữ liệu, trùng 100% số ví dụ |
| Số bài `P9 = 2` (theo `ADDENDUM.md`: ≥ 2 mức quy mô + đánh đổi) | **5/13** (`L05, L06, L08, L10, L12`) | **0/13** bài có thẻ chuẩn `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` |
| Số bài `lv.py lint` sạch (`0 FAIL, 0 WARN`) | **13/13** | 13/13 bài `0 FAIL, 0 WARN` |
| `audit/hci/verify_hci.py` | **27/27 PASS** | Toàn bộ 27 kiểm chứng độc lập đều PASS |
| Số bài `build_report.json` khớp (`spec_sha256 == lv.spec_digest` và `tts_sha256 == lv.tts_digest`) | **13/13** | Giọng đồng nhất `vi-VN-NamMinhNeural` (`edge` / `edge?`) |
| Số bài `L*.srt == say` | **13/13** | Khớp 100% từng câu phụ đề trong cả 13 bài |
| Số bài `asr_report.md` (`thiếu audio = 0`, `chưa xem xét = 0`) | **13/13** | 0 thiếu audio, 0 chưa xem xét; tổng 43 câu gắn cờ rải ở 11 bài (L06, L11 có 0 câu) đều ghi `NOT_VERIFIED bằng tai người` |
| `audit/layout_HCI.tsv` | **0 dòng** (2 byte trống) | Không ghi nhận lỗi layout trong TSV |
| `audit/review/screen_code/HCI.yaml` | **39/39 khớp** | Cả 39 khối `practice 1/2/4` (`L00–L12`) khớp SHA16 phần nội dung trong `<div class="code">` |
| Số bài lab chạy Python khớp `mong_doi.txt` | **13/13** | `loi_giai.py` chạy trực tiếp bằng `.venv/Scripts/python.exe` đều khớp `mong_doi.txt` |
| Số phát hiện `SHOULD` | **28** | Xem mục 3 (`P9` thiếu, `P7` góc màn hình L02, chữ `L09` SVG mờ, `L03`/`L04` nhắc "trong giáo án", ASR `NOT_VERIFIED`, v.v.) |

---

## 2. Các phát hiện mức `MUST` (chặn Stage 10 `GO`)

| Mã | Phạm vi | Cảnh / tệp | Trích nguyên chữ / bằng chứng | Vì sao là `MUST` | Đề xuất sửa |
|---|---|---|---|---|---|
| **M1** | **13/13 bài (`L00–L12`)** | `practice#1`, `practice#2`, `practice#3` (`pause: 30`) | `practice#1` chiếu nguyên văn `loi_giai.py` (ví dụ `L02`: `fitts = lambda D, W: 0.1 + 0.15 * math.log2(D / W + 1.0)`); `practice#2` chiếu nguyên văn `mong_doi.txt` (`t_16px=0.713s t_64px=0.448s`); đến `practice#3` mới hiện bảng hướng dẫn mở `de.md` và `pause: 30`. | **Lộ toàn bộ lời giải và đầu ra trước `pause` (`P8` fail chặt)**: người học nhìn thấy nguyên mã nguồn lời giải trước khi tự làm, mất hoàn toàn tác dụng thực hành độc lập. | Dời khung chiếu `loi_giai.py` và đầu ra chạy thật sang **SAU** bước `pause: 30` (hoặc chỉ đưa gợi ý khung bài trước `pause`). |
| **M2** | **13/13 bài (`L00–L12`)** | `labs/HCI/L00..L12/de.md` và `loi_giai.py` | Ví dụ `L00/de.md` chỉ ghi `"kiểm tra tiêu đề và nút hành động giữa bản thử và bản thật phải khác biệt"` nhưng `loi_giai.py` in `distinct_action_labels=1`; `L05/de.md` không nêu phím tắt `Del + M + Enter` (`0.2 + 1.35 + 0.2`) hay format `mouse_s=5.7 keyboard_s=1.75`; `L11/de.md` không nêu chuỗi `SEND LIVE ALERT` / `send test`; **`L12/de.md`** ghi `"Cộng tổng điểm kiểm 3 mức WCAG 1.0 (16 + 30 + 19 = 65) và tỉ lệ tăng theo phiên bản"` nhưng `loi_giai.py` chỉ in `wcag1_guidelines=14 wcag1_checkpoints=65` (không tính tỉ lệ tăng). | **`de.md` không tự đứng được, thiếu hoàn toàn định dạng stdout `key=value`, trùng 100% số liệu ví dụ thân bài**, và riêng `L12` **lệch logic giữa đề (`de.md`) và code (`loi_giai.py`)**. Người học không thể giải đúng để qua trình chấm nếu chỉ đọc `de.md`. | Viết lại 13 `de.md` nêu đủ: dữ liệu đầu vào cụ thể (dùng bộ số mới khác ví dụ thân bài), yêu cầu tính khớp 100% với `loi_giai.py`, và định dạng dòng `stdout` chính xác tới từng ký tự. |
| **M3** | **13/13 bài (`L00–L12`)** | `lessons/hci/L*.yaml` → `covers:` | `L00–L11` đều rập khuôn `obj1 -> example, obj2 -> check, obj3 -> practice` (và `obj4 -> practice`), `L12` ghi `obj1 -> stage1, obj2 -> stage2, obj3 -> practice`. Cụ thể lệch nặng:<br>• `L00`: obj#2 (cùng phản hồi) trỏ `check` (thực tế dạy ở `intuition`, `concept`); obj#3 (tính thời gian) trỏ `practice` (thực tế dạy ở `example`).<br>• `L01`: obj#2 (thiết kế bố cục trùng vật) trỏ `check` (chỉ liệt kê hoán vị); obj#3 (phân biệt 3 khái niệm) trỏ `practice`.<br>• `L02`: obj#2 (mép/góc màn hình) trỏ `check` (chỉ tính `2^ID-1` và `ΔT`); obj#3 (nút rộng hoặc đặt gần) trỏ `practice` (`practice` chỉ làm nút rộng).<br>• `L03`: obj#2 trỏ `check` (`check` chỉ gộp log2 24 và kiểm người mới); obj#3 (logarit vs tuyến tính) trỏ `practice` (`practice` chỉ tính 15 vs 3×5).<br>• `L04`: obj#2 (chuyển nhớ sang nhận ra) trỏ `check`; obj#3 (7±2 vs thực đơn) trỏ `practice` (`practice` không nói về thực đơn).<br>• `L05`: obj#2 trỏ `check`; obj#3 (giới hạn người thành thạo) trỏ `practice`.<br>• `L06`: obj#2, #3 trỏ `check`; obj#4 (`λ < 0,31` và chia nhóm) trỏ `practice` (`practice` cố định `p=0.31`).<br>• `L07`: obj#2 (đảo chiều lẻ/chẵn) trỏ `check`; obj#3 (tránh hiểu 68 = 68%) trỏ `practice`.<br>• `L08`: obj#1 (so sánh between vs within) trỏ `example` (chỉ tính within); obj#2 trỏ `check`.<br>• `L09`: obj#2 (bàn phím), #3 (nhãn ngữ nghĩa) cùng trỏ `check` (`check` chỉ tính Fitts & diện tích); obj#4 (lề đường vỉa hè) trỏ `practice`.<br>• `L10`: obj#1 (3 tầng chống lỗi) trỏ `example`; obj#2 (tính xác suất) trỏ `check`; obj#3 (xác nhận chung vs cụ thể) trỏ `practice`.<br>• `L11`: obj#1 (dòng thời gian 38 phút) trỏ `example`; obj#2 (3 lỗ hổng), #3 (4 lớp phòng thủ) cùng trỏ `check`; obj#4 (diễn tập áp lực) trỏ `practice`.<br>• `L12`: obj#1 (4 chặng) chỉ trỏ `stage1`; obj#2 (4 con số 1999–2023) chỉ trỏ `stage2`; obj#3 (chọn kiểm tự động + người thật) trỏ `practice` (`practice` chỉ cộng 16+30+19). | **`covers:` trỏ sai cảnh dạy thật của mục tiêu giáo án** ở toàn bộ 13/13 bài (`E51`). | Sửa `covers:` ở cả 13 bài để trỏ đúng danh sách/cảnh dạy thật tương ứng với từng mục tiêu (hỗ trợ đa cảnh hoặc trỏ đúng cảnh lõi như `concept`, `intuition`, `example`, `pitfalls`, `quiz`). |
| **M4** | **13/13 bài (`L00–L12`)** | `P1` nghiêm ngặt (đường chính + `practice#0/#1` + `de.md`) | Mỗi bài đều có **≥ 3 mục chưa giảng** (chi tiết từng mục ở Bảng mục 4 bên dưới): gồm thuật ngữ/viết tắt trên đường chính (`FCC`, `Lò TB/ĐB/TN/ĐN`, `px`, `H` entropy, `bách phân vị`, `thẻ văn bản`, `[W99]..[W23]`, `HTML`, `WCAG`) và hàng loạt cú pháp Python/Shell ở `practice#0/#1` và `de.md` không được bảng cách đọc phủ (`=`, `;`, `!=`, `<=`, `==`, `**`, `int(...)`, `s[:3]`, `ans[0::2]`, `math.factorial`, `math.log2`, `:.1f`, `:.2f`, `:.1e`, `# comment`, `all(...)`, `range(...)`, `set comprehension`, `print(...)` thiếu ở L02/L09, `bash`). | Vi phạm chuẩn `P1` nghiêm ngặt (`BRIEF_R4.md`): người mất gốc hoàn toàn không thể tự hiểu các ký hiệu, viết tắt và cú pháp mã này chỉ từ video. | Giảng đủ các viết tắt/ký hiệu ngay tại chỗ trong thân bài; đồng bộ bảng `practice#0` phủ **100%** cú pháp dùng trong `practice#1` (xoá dòng thừa như `:.3f`, `math.log` khi không dùng) và giải thích `bash` / `px` / `WCAG` ở nơi dùng. |
| **M5** | `L10` | `intuition#0` (`00022.png`) | `<text x="535" y="122" fill="#f8fafc" ...>Chặn được lỗi!</text>` và `<text ... fill="#fde047">Lớp 1: p₁ = 1/1000</text>` vẽ trên nền kem sáng `#fef9e7` của sân khấu. | Chữ `#f8fafc` (trắng ngà) trên nền kem gần như **tàng hình hoàn toàn** (độ tương phản ~1.05:1), không đọc được trong khung hình video đã dựng (`P3 = 0`). | Đổi màu chữ SVG `L10 intuition#0` sang màu tối đậm tương phản cao (ví dụ `#1f2937` / `#065f46` / `#b45309`). |

---

## 3. Các phát hiện mức `SHOULD`

| Mã | Bài | Cảnh / mục | Trích nguyên chữ / bằng chứng | Lý do & đề xuất sửa |
|---|---|---|---|---|
| **S1** | `L09` | `intuition#0` (`00027.png`) | `<text ... fill="#cbd5e1">Dễ bấm trượt</text>`, `Đạt tối thiểu mức AA`, `Đệm 14 điểm ảnh mỗi phía (AAA)` và các màu nhạt `#fca5a5`, `#7dd3fc`, `#86efac` trên nền kem sáng. | Chữ xám nhạt `#cbd5e1` trên nền kem rất mờ (tương phản ~1.4:1 — đặc biệt mỉa mai ngay trong bài học về Chuẩn tiếp cận & độ tương phản!). Đổi sang màu đậm (`#334155`, `#b91c1c`, `#0369a1`, `#047857`). |
| **S2** | `L00–L12` (13/13 bài) | `P9` (`recap` & thân bài) | 0/13 bài có thẻ chuẩn `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap`; 8/13 bài (`L00, L01, L02, L03, L04, L07, L09, L11`) thiếu hẳn phần so sánh ≥ 2 mức quy mô sản phẩm/thời gian + đánh đổi bằng số cụ thể trong thân bài (`P9 = 1`). | Bổ sung phân tích ≥ 2 mức quy mô kèm số liệu và đánh đổi ở thân bài cho 8 bài thiếu, và thêm thẻ `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` (kèm SVG khi phù hợp) cho cả 13 bài. |
| **S3** | `L02` | `objectives[1]` vs thân bài | Mục tiêu 2: `"Giải thích vì sao mép và góc màn hình là đích lớn"`. Thân bài (`intuition#0`, `example#2`, `pitfalls#1`) chỉ phân tích cơ chế **mép** màn hình; **góc** màn hình chỉ được nhắc lướt 2 chữ ở `recap#1` (`"bốn góc, bốn mép màn hình"`). | Bổ sung 1–2 câu giải thích rõ **góc màn hình** được chặn đồng thời theo cả hai trục ngang và dọc (cả chiều rộng lẫn chiều cao hiệu dụng đều vô hạn). |
| **S4** | `L01`, `L03`, `L04` | `example#0` (`say`) | `L01 example#0`: `"với ví dụ mặt bếp bốn lò trong giáo án"`; `L03 example#0`: `"ví dụ chuẩn trong giáo án"`; `L04 example#0`: `"từng trường hợp trong giáo án"`. | Cụm `"trong giáo án"` nhắc tới tài liệu người học không có trong tay (tương tự tinh thần E29). Nên đổi thành `"ví dụ mở đầu"` hoặc `"ví dụ đã nêu"`. |
| **S5** | `L01` | `intuition#0` (`00018.png`) | Trên hình SVG bên trái ghi `Lò TB`, `Lò ĐB`, `Lò TN`, `Lò ĐN` trong khi hình bên phải ghi `Trái-Trên`, `Phải-Trên`, `Trái-Dưới`, `Phải-Dưới`. | Vừa là viết tắt chưa giảng (`TB/ĐB/TN/ĐN`), vừa không nhất quán nhãn giữa hai nửa hình trong cùng một SVG. Nên thống nhất ghi `Trái-Trên`... ở cả hai bên hoặc chú thích rõ. |
| **S6** | `L08` | `intuition#0` (`00024.png`) | `<svg viewBox="0 0 600 220">` dùng `font-size="12"` cho chữ trong 3 hộp đen; màu vàng `#eab308` (`Nhóm 1: C`, `Nhóm 2: C`, `Nhóm 3: C`) trên nền kem hơi chói. | Đổi `#eab308` sang màu hổ phách đậm `#b45309` để tăng độ tương phản khi xem video trên màn hình nhỏ. |

---

## 4. Chi tiết `P1` nghiêm ngặt (lớp + đường chính + `practice` + `de.md`)

| Bài | Mục chưa giảng (`cảnh/step` + trích chữ) | Bảng cách đọc `practice#0` có phủ không? | Điểm P1 |
|---|---|---|---|
| **L00** | 1) `hook#0`: `FCC` (chỉ nói "cơ quan viễn thông Mỹ" ở `concept#1`, không giải thích viết tắt `FCC`)<br>2) `hook#1`: câu tiếng Anh `Are you sure that you want to send this Alert?` chưa dịch ngay tại bước đó (tới `intuition#0` mới dịch)<br>3) `practice#1`: `=`, `;`, `!=`, `int(...)`, `f"...{...}"` (bảng chỉ ghi `f"{val:.3f}"` không dùng trong code)<br>4) `de.md`: `UI`, `checklist`, `bash` | Đường chính: không áp dụng bảng.<br>`practice#1`: **Không** phủ `=`, `;`, `!=`, `int(...)`, `f"...{...}"`. | **0** |
| **L01** | 1) `intuition#0`: `Lò TB`, `Lò ĐB`, `Lò TN`, `Lò ĐN` (4 viết tắt phương hướng không giảng)<br>2) `practice#1`: `math.factorial(4)` (bảng ghi `math.log / exp / sqrt`, không ghi `factorial`), `=`, `f"...{ambiguous}..."` (không dùng `:.3f`)<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `math.factorial`, `=`, `f"...{var}..."` (chỉ phủ `import math` và `print(...)`). | **0** |
| **L02** | 1) `practice#3` & `de.md`: `px` (`16 px`, `64 px`) — thân bài luôn viết `điểm ảnh`, chưa từng giảng viết tắt `px`<br>2) `practice#1`: `math.log2(...)` (bảng chỉ ghi `math.log`), `print(...)` (**thiếu dòng `print` trong bảng `practice#0` của L02!**), `=`<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `math.log2`, `print(...)`, `=` (chỉ phủ `import`, `lambda`, `:.3f`). | **0** |
| **L03** | 1) `example#3`: ký hiệu $H = \sum p_i \log_2(1/p_i)$ (chữ $H$ — entropy thông tin — không có trong `sym#0` và không giải thích là gì)<br>2) `practice#1`: `math.log2(...)` (bảng chỉ ghi `math.log`), `=`<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `math.log2`, `=` (có phủ `import`, `:.3f`, `print`). | **0** |
| **L04** | 1) `practice#1`: `s[:3]`, `s[3:]` (cắt lát chuỗi), `[..., ...]` (tạo list), `<=`, `int(...)`, `=`, `f"...{...}"` (không dùng `:.3f`)<br>2) `de.md`: `bash` | `practice#1`: **Không** phủ slicing `[:3]`, list `[...]`, `<=`, `int(...)`, `=`, f-string không `.3f` (bảng thừa `:.3f`, `sum/max/min`). | **0** |
| **L05** | 1) `practice#1`: `# Del + M + Enter` (ký hiệu chú thích `#` trong Python và phím `Del`), `:.1f`, `:.2f` (bảng chỉ ghi `:.3f`), `=`<br>2) `de.md`: `bash` | `practice#1`: **Không** phủ `#`, `Del`, `:.1f`, `:.2f`, `=` (chỉ phủ `print`). | **0** |
| **L06** | 1) `practice#1`: `p=0.31` (tham số mặc định trong `lambda` 2 biến; bảng chỉ ghi `lambda x: ...`), `**` (luỹ thừa), `:.1f` (bảng ghi `:.3f`), `=`<br>2) `de.md`: `bash` | `practice#1`: **Không** phủ `p=0.31`, `**`, `:.1f`, `=` (chỉ phủ `lambda`, `print`). | **0** |
| **L07** | 1) `pitfalls#0`: `bách phân vị 50` (thuật ngữ thống kê không giải thích tại chỗ)<br>2) `practice#1`: `ans[0::2]`, `ans[1::2]` (cắt lát bước nhảy), `sum(x - 1 for x in ...)` (generator expression), `:.1f` (bảng ghi `:.3f`), `=`<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `[0::2]`/`[1::2]`, generator expression, `:.1f`, `=` (chỉ phủ `for`, `sum`, `print`). | **0** |
| **L08** | 1) `sym#1`: khái niệm `ma trận vuông L` và chỉ số hàng–cột $L_{1,1}$ xuất hiện đột ngột chưa ôn nền ma trận<br>2) `practice#1`: `all(...)`, `range(3)`, `{... for r in ...}` (set comprehension), `latin[r][c]` (chỉ mục 2 chiều), `==`, `int(...)`, `=`, `f"...{latin}..."`<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `all`, `range`, set comprehension, chỉ mục 2 chiều `[][]`, `==`, `int`, `=`, f-string không `.3f`. | **0** |
| **L09** | 1) `concept#0` / `example#3`: `thẻ văn bản` (chưa giải thích khái niệm thẻ HTML là gì so với nút bấm chuẩn)<br>2) `practice#1`: `math.log2(...)`, `print(...)` (**thiếu dòng `print` trong bảng `practice#0` của L09!**), `=`<br>3) `de.md`: `Accessibility`, `px` (L09 chỉ viết `điểm ảnh`, chưa giảng `px`), `bash` | `practice#1`: **Không** phủ `math.log2`, `print(...)`, `=` (chỉ phủ `import`, `lambda`, `:.3f`). | **0** |
| **L10** | 1) `example#1`: $5 \times 10^{-7}$ (ký hiệu mũ âm chưa giảng trong bài/prereq)<br>2) `practice#1`: `:.1e` (định dạng số mũ khoa học — bảng chỉ ghi `:.3f`), `=`<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `:.1e`, `=` (chỉ phủ `print`). | **0** |
| **L11** | 1) `intuition#0`: `Are you sure?`, `Yes` (chữ tiếng Anh trên hộp thoại minh hoạ không dịch trực tiếp trong SVG)<br>2) `practice#1`: `=`, `!=`, `int(blocked)`, `f"...{...}"` (bảng chỉ ghi `:.3f` không dùng)<br>3) `de.md`: `bash` | `practice#1`: **Không** phủ `=`, `!=`, `int(...)`, f-string không `.3f`. | **0** |
| **L12** | 1) `hook#0`: `[W99]`, `[W08]`, `[W18]`, `[W23]` (mã trích dẫn tài liệu không giải thích trên màn hình)<br>2) `sym#0`: $L_1, L_2$ dùng trước khi giảng tới `stage2#1`<br>3) `intuition#0`: `px` dùng trước khi có `px²` ở `stage3#0` (và chưa từng giảng `px = điểm ảnh`)<br>4) `stage2#1`: `[0, 1]` (ký hiệu đoạn); `pitfalls#1`: `mã HTML` (chưa giảng `HTML`)<br>5) `practice#1`: `=`, `f"...{wcag1}"`; `de.md`: `WCAG` (chưa từng giảng/viết chữ `WCAG` trong toàn khoá), `bash` | `practice#1`: **Không** phủ `=`, f-string không `.3f` (bảng thừa `:.3f`). | **0** |

---

## 5. Kiểm tra lời đọc `say`, ASR, SRT, `build_report.json` và câu chứa `"càng "`

1. **Ký hiệu toán thô trong `say`**: **0/13 bài** có ký hiệu LaTeX/toán thô (`$`, `\`, `_`, `^`, `{`, `}`, `=`, `<`, `>`, `+`, `*`, `/`). Toàn bộ công thức đã được đọc bằng lời Việt tự nhiên.
2. **Phát âm tiếng Việt & từ ngoại**: `lv.py lint` đạt **0 WARN** về phát âm ở cả 13 bài; không có từ ngoại chưa phủ lexicon.
3. **Các câu chứa `"càng "` trong `say`** (kiểm theo yêu cầu — cả 3 câu đều đúng ngữ nghĩa trong ngữ cảnh):
   - `L05` `prereq#1`: *"Nhắc lại, thời gian đưa con trỏ tới một nút tăng theo lôgarit cơ số 2 của khoảng cách chia bề rộng cộng 1, nên nút **càng** xa và **càng** hẹp thì **càng** lâu."* (đúng theo định luật Fitts).
   - `L10` `pitfalls#0`: *"Lỗi thứ nhất rất hay gặp ở người đã đi làm là gắn hộp thoại xác nhận vào mọi thao tác nhỏ nhặt vì nghĩ rằng hỏi lại **càng** nhiều **càng** an toàn."* (đang phê phán hiểu lầm của người làm nghề).
   - `L12` `prereq#0`: *"Vì thế nút **càng** nhỏ thì người dùng **càng** mất nhiều thời gian và dễ bấm trượt."* (đúng theo định luật Fitts).
4. **Đối chiếu `build_report.json` & `SRT` & `ASR`**:
   - 13/13 bài: `spec_sha256 == lv.spec_digest`, `tts_sha256 == lv.tts_digest`, `L*.srt == say` 100%, `missing_audio = 0`, `unreviewed = 0`.
   - Lưu ý `INFO`: Các câu gắn cờ trong `asr_report.md` (tổng 43 câu: L00:1, L01:1, L02:15, L03:2, L04:1, L05:5, L06:0, L07:3, L08:6, L09:6, L10:1, L11:0, L12:2) đều đã có ghi chú trong `asr_reviewed`, nhưng toàn bộ ghi chú đều mang nhãn `NOT_VERIFIED bằng tai người` (chủ yếu do chữ cái đơn lẻ A/B/D/W/K/P/M hoặc `lôgarit`/`Latin` được ASR chép khác mặt chữ).

---

## 6. Bảng độ sâu & chất lượng từng bài (`P1–P9`)

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng (P1–P7) | Mất gốc | P8 | P9 | Chỗ thiếu chính / Cần biết trước |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **L00** | `a0ed47b46d4e4139` | 11.01 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: FCC, câu Anh, Python `= ; != int f""`, `de.md` (`UI`, `checklist`, `bash`). `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu 2 mức quy mô & thẻ `recap`. |
| **L01** | `40d23a575cda1959` | 9.86 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: `Lò TB/ĐB/TN/ĐN`, `math.factorial`, `=`, `f""`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu đánh đổi quy mô hệ thống & thẻ `recap`. |
| **L02** | `6644b3fb4aa4f0de` | 10.85 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: `px`, `math.log2`, thiếu `print` ở bảng, `=`, `bash`. `P7`: `covers:` lệch, thiếu cơ chế *góc* màn hình. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu 2 mức quy mô & thẻ `recap`. |
| **L03** | `5d067c8669588ac6` | 10.72 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: ký hiệu $H$ (entropy), `math.log2`, `=`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: quy mô lớn mới nhắc bằng lời, thiếu thẻ `recap`. |
| **L04** | `8f1fbfcacdd49204` | 9.11 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: Python `s[:3]`, list `[]`, `<=`, `int`, `=`, `f""`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu 2 mức quy mô & thẻ `recap`. |
| **L05** | `62a781a19cda84fe` | 9.36 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 2 | `P1`: `# Del`, `:.1f`, `:.2f`, `=`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thân bài đủ 2 mức (1 vs 200/500 + đánh đổi), nhưng thiếu thẻ `Hai mức quy mô` ở `recap`. |
| **L06** | `10bfa56d22486fad` | 11.00 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 2 | `P1`: `lambda` 2 biến/mặc định, `**`, `:.1f`, `=`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thân bài đủ (`5` vs `15` vs `3×5`), thiếu thẻ `Hai mức quy mô` ở `recap`. |
| **L07** | `ff36a765951c65dc` | 9.79 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: `bách phân vị`, `ans[0::2]`, generator `sum(...)`, `:.1f`, `=`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu 2 mức quy mô & thẻ `recap`. |
| **L08** | `3b7922e431235772` | 10.18 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 2 | `P1`: ma trận $L_{1,1}$, `all`, `range`, set comprehension, `[][]`, `==`, `int`, `=`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: đủ `k=3,4,5` & đánh đổi, thiếu thẻ `recap`. |
| **L09** | `86313941cabb3b4f` | 11.47 | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 10 | **GẦN** | 1 | 1 | `P1`: `thẻ văn bản`, `math.log2`, thiếu `print` ở bảng, `=`, `Accessibility`, `px`, `bash`. `P3`: SVG `00027.png` chữ `#cbd5e1` mờ. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu thẻ `recap`. |
| **L10** | `97b9d6a607154aab` | 9.71 | 0 | 2 | 0 | 2 | 2 | 2 | 1 | 9 | **GẦN** | 1 | 2 | `P1`: $10^{-7}$, `:.1e`, `=`, `bash`. `P3`: SVG `00022.png` chữ trắng `#f8fafc` tàng hình trên nền kem! `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: đủ 1–3 lớp + đánh đổi, thiếu thẻ `recap`. |
| **L11** | `746f4eb87dd45cc5` | 7.19 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 1 | `P1`: `Are you sure?`/`Yes`, `= != int f""`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, thiếu format `de.md`. `P9`: thiếu 2 mức quy mô sản phẩm & thẻ `recap`. |
| **L12** | `ac18f6658267ab3c` | 8.43 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | **GẦN** | 1 | 2 | `P1`: `[W99]..[W23]`, $L_1,L_2$ dùng trước giảng, `px`, `[0,1]`, `HTML`, `WCAG`, `=`, `f""`, `bash`. `P7`: `covers:` lệch. `P8`: lộ trước `pause`, `de.md` lệch logic `loi_giai.py`. `P9`: đủ 4 chặng + `3 dev/40 màn`, thiếu thẻ `recap`. |

*(Ghi chú: về kiến thức lý thuyết phần đầu `hook..quiz`, các bài viết rất tốt cho người mất gốc; điểm `P1=0` và `Mất gốc = GẦN` chủ yếu do phần `practice` + `de.md` đưa mã Python/Shell mà thiếu bảng giải thích khớp từng cú pháp, cộng một vài viết tắt/ký hiệu nhỏ trong thân bài).*

---

## 7. Danh sách khung hình PNG đã xem trực tiếp (`read_file`)

- **L00**: `out/HCI/L00/frames/00000.png` (hook), `00018.png` (intuition SVG), `00069.png` (practice#0), `00076.png` (recap) *(4 PNG)*
- **L01**: `out/HCI/L01/frames/00000.png` (hook), `00018.png` (intuition SVG — thấy viết tắt `Lò TB/ĐB/TN/ĐN`), `00063.png` (practice#0), `00070.png` (recap) *(4 PNG)*
- **L02**: `out/HCI/L02/frames/00020.png` (intuition SVG), `00030.png` (example#0), `00056.png` (quiz#0), `00066.png` (practice#0 — thấy bảng thiếu `print`) *(4 PNG)*
- **L03**: `out/HCI/L03/frames/00018.png` (intuition SVG), `00028.png` (example#0), `00051.png` (quiz#0), `00061.png` (practice#0) *(4 PNG)*
- **L04**: `out/HCI/L04/frames/00016.png` (intuition SVG), `00023.png` (example#0), `00053.png` (practice#0) *(3 PNG)*
- **L05**: `out/HCI/L05/frames/00015.png` (intuition SVG), `00024.png` (example#0), `00054.png` (practice#0) *(3 PNG)*
- **L06**: `out/HCI/L06/frames/00023.png` (intuition SVG), `00038.png` (example#0), `00065.png` (quiz#0) *(3 PNG)*
- **L07**: `out/HCI/L07/frames/00020.png` (intuition SVG), `00033.png` (example#0), `00052.png` (quiz#0), `00062.png` (practice#0) *(4 PNG)*
- **L08**: `out/HCI/L08/frames/00024.png` (intuition SVG), `00034.png` (example#0), `00064.png` (practice#0) *(3 PNG)*
- **L09**: `out/HCI/L09/frames/00027.png` (intuition SVG — thấy chữ `#cbd5e1` rất mờ trên nền kem), `00035.png` (example#0), `00076.png` (recap) *(3 PNG)*
- **L10**: `out/HCI/L10/frames/00022.png` (intuition SVG — thấy chữ `#f8fafc` tàng hình trên nền kem), `00029.png` (example#0), `00059.png` (practice#0) *(3 PNG)*
- **L11**: `out/HCI/L11/frames/00012.png` (intuition SVG), `00023.png` (example#0), `00049.png` (practice#0), `00056.png` (recap) *(4 PNG)*
- **L12**: `out/HCI/L12/frames/00017.png` (intuition SVG), `00022.png` (stage1/example), `00057.png` (practice#0) *(3 PNG)*
*(Tổng cộng **45 PNG** đã đọc trực tiếp; không có khung nào bị tràn bảng, đè chữ hay vỡ KaTeX, nhưng `L09 00027.png` bị mờ độ tương phản và `L10 00022.png` bị chữ trắng tàng hình trên nền kem).*

---

## 8. Kiểm tra mã & số đã chạy / tính lại

- `lv.py lint` chạy trong Python trên toàn bộ 13 tệp `lessons/hci/*.yaml`: **13/13 đạt 0 FAIL, 0 WARN**.
- `audit/hci/verify_hci.py`: **27/27 PASS**.
- Kiểm tính lại độc lập thêm 12 phép tính phụ ngoài `verify_hci.py` (quiz L02/L03/L06/L07/L09/L12, entropy +1 L03, quy mô 200 lần L05, tỉ lệ % L11): **12/12 khớp**.
- Chạy trực tiếp 13/13 `labs/HCI/L00..L12/loi_giai.py` bằng `.venv/Scripts/python.exe` và so từng ký tự với `mong_doi.txt`: **13/13 khớp** (`L12` dù chạy khớp `mong_doi.txt` nhưng `de.md` ghi yêu cầu khác code).

---

## 9. Người học kẹt ở đâu (góc nhìn người mất gốc chỉ xem video)

- **L00**: Kẹt ngay ở `hook#0` thấy chữ viết tắt `FCC` không biết là cơ quan nào; tới `practice#1` và `de.md` gặp `=`, `;`, `!=`, `int(...)`, `f"{...}"`, `UI`, `checklist`, `bash` và không biết cần in chuỗi `distinct_action_labels=1` nếu tự làm từ `de.md`.
- **L01**: Kẹt ở `intuition#0` khi thấy `Lò TB, Lò ĐB, Lò TN, Lò ĐN` trên hình bếp (không giải thích viết tắt); tới `practice#1` gặp `math.factorial(4)` chưa giảng trong bảng `practice#0`.
- **L02**: Kẹt ở `practice#1` gặp `math.log2` và `print(...)` (bảng `practice#0` quên liệt kê `print`), rồi ở `de.md` gặp `16 px`, `64 px` dù cả bài chỉ gọi là `điểm ảnh`.
- **L03**: Kẹt ở `example#3` khi đột ngột xuất hiện công thức $H = \sum p_i \log_2(1/p_i)$ mà $H$ chưa từng được giải mã là gì; tới `practice#1` gặp `math.log2`.
- **L04**: Phần lý thuyết đi rất mượt, nhưng kẹt nặng ở `practice#1` khi gặp hàng loạt cú pháp Python chưa giảng (`s[:3]`, `s[3:]`, `[...]`, `<=`, `int(...)`).
- **L05**: Kẹt ở `practice#1` khi thấy `# Del + M + Enter` và định dạng `:.1f`, `:.2f` trong khi bảng `practice#0` chỉ giải thích `:.3f`.
- **L06**: Kẹt ở `practice#1` khi thấy hàm hai đối số có giá trị mặc định `lambda n, p=0.31: ...` và toán tử `**` chưa được giải thích.
- **L07**: Kẹt nhẹ ở `pitfalls#0` với cụm `"bách phân vị 50"`, rồi kẹt ở `practice#1` với `ans[0::2]` và biểu thức `sum(x - 1 for x in ...)`.
- **L08**: Kẹt ở `sym#1` khi dùng ký hiệu ma trận $L_{1,1}$ chưa ôn từ đầu, và kẹt nặng ở `practice#1` với `all(...)`, `range(3)`, `{... for ...}` và chỉ mục 2 chiều `latin[r][c]`.
- **L09**: Kẹt ở `intuition#0` (`00027.png`) vì dòng chữ chú thích xám nhạt `#cbd5e1` rất khó đọc trên nền kem; ở `concept#0` thấy `"thẻ văn bản"`, và ở `practice#1`/`de.md` gặp `math.log2`, `print` (thiếu trong bảng) và `px`.
- **L10**: Kẹt trực tiếp ở `intuition#0` (`00022.png`) vì dòng kết luận `"Chặn được lỗi!"` viết bằng màu trắng `#f8fafc` trên nền kem gần như vô hình; và ở `practice#1` gặp `:.1e` chưa giảng.
- **L11**: Kẹt ở `practice#1` và `de.md` vì không biết phải đặt tên biến hay in chuỗi `accidental_send_blocked=1 has_cancel_template=1` nếu không chép từ khung `practice#1`/`#2` trước đó.
- **L12**: Kẹt ngay ở `hook#0` với `[W99]..[W23]`, ở `sym#0` với $L_1, L_2$ chưa định nghĩa, ở `pitfalls#1` với `HTML`, ở `de.md` với `WCAG`, và đặc biệt **kẹt ở bài lab L12** nếu tự đọc `de.md` làm theo yêu cầu `"tỉ lệ tăng theo phiên bản"` (vì đáp án chấm lại đòi `wcag1_guidelines=14 wcag1_checkpoints=65`).

---

## 10. Kết luận Stage 10

# **NO-GO**

**Lý do chốt chặn:** Mặc dù nội dung chuyên môn HCI, phép tính số học, khớp `build_report.json` (`spec_sha256`/`tts_sha256`), `SRT == say`, `asr_report.md` và mã `loi_giai.py` thực thi đều sạch ở 13/13 bài, khoá `HCI` chưa đạt các tiêu chí bắt buộc của Stage 10 do lỗi hệ thống ở toàn bộ 13 bài:
1. **13/13 bài lỗi `P8`**: lộ nguyên `loi_giai.py` và `mong_doi.txt` trước `pause`, `de.md` thiếu định dạng `stdout` và không tự đứng được, trùng 100% số ví dụ, và `L12` lệch đề ↔ code.
2. **13/13 bài lệch `covers:`**: chỉ trỏ mẫu `example/check/practice` thay vì cảnh dạy thực tế của mục tiêu.
3. **13/13 bài `P1 = 0`**: bảng `practice#0` không phủ hết cú pháp Python thực tế trong `practice#1` (L02/L09 còn thiếu `print`), cộng thêm một số viết tắt/thuật ngữ chưa giảng (`FCC`, `Lò TB/ĐB/TN/ĐN`, `px`, `H`, `bách phân vị`, `WCAG`, `HTML`, `[W99]..[W23]`).
4. **13/13 bài thiếu chuẩn `P9` trong `recap`** (`<p class="note"><b>Hai mức quy mô:</b> ...`) và 8/13 bài mới dừng ở `P9 = 1`.
5. **Lỗi hiển thị SVG ở `L10` (`00022.png`, chữ trắng tàng hình trên nền kem)** và **`L09` (`00027.png`, chữ xám nhạt rất mờ)**.
