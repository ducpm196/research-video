# Hồ sơ chuyên ngành: dùng cùng một xưởng cho mọi loại video giảng giải

Quay lại: SKILL.md, Bước 2–3. Người dùng yêu cầu (2026-10-31): khung phải tái dùng được cho chủ đề khác — ngoại ngữ, kỹ năng mềm,
kiến thức xã hội đời sống, triết học, phim ảnh, video tiếp thị liên kết.

## 1. Cái gì CHUNG, cái gì THEO HỒ SƠ
| Chung cho mọi chủ đề (không đổi) | Theo hồ sơ (`tools/profiles/<tên>.yaml`) |
|---|---|
| Đặc tả YAML → khung hình 1920×1080 → giọng đọc → MP4 + phụ đề + chương | phân cảnh hợp lệ và nhãn hiện trên khung (`kinds`) |
| Một ý một step, câu ≤ 38 từ, `focus` theo câu (E31/E32), bảng tự đủ sau `clear` | phân cảnh bắt buộc (`required`) |
| Một giọng lời giảng cho cả bài; giọng dự phòng thay CẢ bài | chuẩn độ sâu E39 (`depth`: phân cảnh phải có, kiểu hình, số step làm mẫu, số từ) |
| Máy nghe hai mô hình, lý do cho câu gắn cờ, không bịa phiên âm | chính sách bằng chứng (`evidence`: numbers / sources / claims) |
| Kiểm bố cục: tràn, đè, chữ đè trong hình | luật riêng (`rules`: E41–E50) |
| Nhắc bài khác phải tự hiểu được (E22–E24), không nhắc “tài liệu gốc” (E29) | mẫu bài `tools/templates/profiles/<tên>.yaml` |

Bài chọn hồ sơ bằng `profile:` trong đặc tả; không khai thì lấy `profile:` của `curriculum/<khoá>.yaml`; không có nữa thì `stem`.
`lv.py new-course <KHOÁ> --title "…" --profile <tên>` ghi hồ sơ vào lộ trình; `lv.py new …` tự lấy mẫu của hồ sơ đó.

## 2. Sáu hồ sơ hiện có
| Hồ sơ | Khung bài (phân cảnh bắt buộc in đậm) | Bằng chứng | Luật riêng | Mẫu đã kiểm |
|---|---|---|---|---|
| `stem` (mặc định) | **hook, symbol, example, pitfall, quiz, recap** + prereq, intuition, concept, formula, check | mọi con số có `checks` chạy bằng máy | — | 476 bài đã dựng |
| `language` | **hook, vocab, pattern, example, pitfall, quiz, recap** + prereq, pronunciation, dialogue, practice, culture | ngữ pháp, nghĩa dẫn từ điển/giáo trình chuẩn | E50 giọng bản ngữ | `examples/profiles/language_L01.yaml` — **đã dựng**, verify PASS, ASR 0 cờ |
| `softskill` | **hook, model, scenario, pitfall, quiz, recap** + prereq, concept, example, practice, mindset | mô hình có nguồn (tổ chức, tác giả, năm) | E46 không hứa kết quả | `softskill_L02.yaml` (SBI) |
| `humanities` | **hook, concept, argument, example, pitfall, quiz, recap** + context, counter, check | trích dẫn khai trong `quotes` (tác giả, tác phẩm, năm, bản dịch) | E47 trích dẫn có nguồn | `humanities_L03.yaml` (con thuyền Theseus) |
| `film` | **hook, context, scene, technique, quiz, recap** + concept, theme, example, pitfall | dữ kiện có nguồn; nhận định ghi là nhận định | E48 ảnh có giấy phép, E49 báo trước tiết lộ nội dung | `film_L04.yaml` (hiệu ứng Kuleshov) |
| `affiliate` | **hook, disclosure, need, criteria, compare, fit, recap** + example, check, pitfall, quiz | mọi khẳng định sản phẩm khai trong `claims` có nguồn + ngày | E41 công bố liên kết trước, E42 từ tuyệt đối, E43 lời khen bịa, E44 khẳng định không ngày, E45 phải nói ai KHÔNG nên mua | `affiliate_L05.yaml` (sạc dự phòng, Wh, IATA) |

## 3. Điều riêng của từng loại (đọc trước khi viết)
- **Ngoại ngữ.** Lời giảng tiếng Việt không đọc từ nước ngoài (giọng Việt đọc sai): nói nghĩa tiếng Việt, chữ nước ngoài chỉ trên màn hình.
  Câu mẫu: một step riêng có `voice:` bản ngữ (ví dụ `en-US-AvaNeural`), cả step chỉ có tiếng nước ngoài (E50). `lv.py` không áp lexicon
  tiếng Việt cho step đó; máy nghe nghe bằng đúng ngôn ngữ (lấy từ tên giọng); `verify` chỉ đếm giọng của lời giảng.
  Từ đứng riêng hay bị máy nghe chép sai (mẫu: “See, saw, seen” → “See you soon”) → dạy từ trong **câu mang** (“I saw her yesterday”).
  Tên riêng Việt trong câu tiếng Anh (Da Lat → “Delat”) nên tránh hoặc nghe lại bằng tai.
- **Kỹ năng mềm.** Làm mẫu bằng **câu nói cụ thể**, luyện tập có **tiêu chí tự chấm**; quiz là quyết định trong tình huống. Không hứa
  “chắc chắn thành công” (E46). Nghiên cứu tâm lý được dẫn thì nêu mức bằng chứng; nhiều kết quả nổi tiếng không lặp lại được.
- **Xã hội, đời sống, triết học.** Lập luận tách từng bước (tiền đề → kết luận), luôn có **phản biện mạnh nhất** (`counter`). Phân biệt điều
  tác giả viết với cách hiểu phổ biến (mẫu: chi tiết “gom ván cũ” là của Hobbes 1655, không phải Plutarch). Vấn đề gây tranh cãi: nêu các
  quan điểm chính và căn cứ của mỗi bên, không áp đặt.
- **Phim ảnh.** Không chèn khung phim/ảnh tác phẩm có bản quyền khi chưa có quyền (E48) — dùng sơ đồ tự vẽ. Lời kể kinh điển phải đặt cạnh
  kết quả kiểm chứng lại (mẫu: Kuleshov 1992 không thấy hiệu ứng rõ, 2016 thấy nhưng tuỳ cảm xúc). Báo trước tiết lộ nội dung (E49).
- **Tiếp thị liên kết.** Mục tiêu là giúp người xem **chọn đúng**, kể cả chọn không mua. Công bố liên kết trong 2 phân cảnh đầu (E41), số liệu
  có nguồn và ngày (E44), nêu ai không nên mua (E45), không lời khen bịa (E43). Không bao giờ dựng trang/video giả danh nhãn hàng hay người
  thật. Người phát hành tự xác nhận quy định quảng cáo nơi đăng (ở Việt Nam: Luật Quảng cáo; quy định nội dung trả tiền của nền tảng).

## 4. Thêm một hồ sơ mới (ví dụ: âm nhạc, y tế phổ thông, tài chính cá nhân)
1. Sao `tools/profiles/softskill.yaml` thành `<tên>.yaml`; đặt `kinds` (nhãn tiếng Việt, `cls` chọn trong các lớp màu của `player.css`),
   `required`, `depth`, `evidence`, `rules`.
2. Lĩnh vực có rủi ro gây hại (y tế, tài chính, pháp lý): thêm luật riêng vào `tools/lv_profile.py` (mẫu: E41–E45) — ví dụ bắt buộc câu
   “không thay thế tư vấn chuyên môn”, cấm hứa lợi nhuận. Mỗi luật mới có ca thử trong `tests/test_lint.py` (lint phải BẮT được lỗi cài sẵn).
3. Viết mẫu bài thật `tools/templates/profiles/<tên>.yaml` có nguồn đã đọc; sinh `examples/profiles/<tên>_L0N.yaml` (mỗi mẫu một id riêng trong khoá DEMO); lint 0 FAIL;
   dựng thử một bài và xem khung bằng mắt trước khi mở khoá.
4. Dò phát âm mọi tên riêng (`audit/cs112/probe_terms.py`, ngưỡng 7/8 + đối chứng) như SKILL.md Bước 4.
5. Mở khoá: `lv.py new-course <KHOÁ> --title "…" --profile <tên>` rồi làm theo references/new-domain.md.

## 5. Bài hành trình và bài tình huống ở mọi hồ sơ
Phần “kinh nghiệm chuyên gia theo trục thời gian” (case-lessons.md mục 5, `case: journey`) dùng được cho mọi chủ đề: lịch sử một trường
phái triết học, một kỹ năng trong nghề, một thể loại phim, một dòng sản phẩm. Luật E40 giống nhau: ≥ 4 chặng, năm không giảm, mỗi chặng có
quy mô/bối cảnh, nguồn, thực hành rút ra và con số tính lại (hồ sơ không có số: một dữ kiện kiểm được thay cho con số).
