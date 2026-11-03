# Rà soát L26 — Bài 26 — Phân tích phân biệt tuyến tính (LDA) — tiêu chí Fisher

- Đặc tả: `lessons/L26_lda_fisher.yaml`; nguồn: DC23#Ch5; tex#L410 (LDA: “chiếu dữ liệu tối đa khoảng cách giữa các lớp”); AUDIT A23, T16
- Quy mô: 11 cảnh, 19 step, 8 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 16 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 3 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L26/build_report.json`): 52 khung, 309.4 s, built_at 2026-10-26T18:26:34Z, spec_sha256 `1ce01454697c4d70…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L26/asr_report.md`): câu: 52, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:07:09Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 47 | 0.759 | Hướng tốt nhất tỉ lệ với nghịch đảo của S w nhân hiệu hai tâm. | Hướng tốt nhất tỷ lệ với nghiệp đảo của SVCAP nhân hiệu 2 tâm. | “tỉ” → nghe thành “tỷ”; “nghịch” → nghe thành “nghiệp”; “s w” → nghe thành “svcap” | s, v, kép | tỉ, nghịch | S w đọc tên chữ cái “ét vê kép”, ASR chép “SVCAP”; nghịch→nghiệp lẫn vần — các từ khác khớp |
| 17 | 0.886 | Lấy đạo hàm của J theo w và cho bằng 0, với hai lớp ta rút gọn được, hướng tốt nhất tỉ lệ với nghịch đảo của S w nhân hiệu hai tâm. | Lấy đạo hàm của di theo V-cap và cho bằng không, với hai lớp ta rút gọn được, hướng tốt nhất tỷ lệ với nghiệt đảo của SV-cap nhân hiệu 2 tâm. | “kép” → nghe thành “cap”; “tỉ” → nghe thành “tỷ”; “nghịch” → nghe thành “nghiệt”; “kép” → nghe thành “cap” | kép, kép | tỉ, nghịch | J, w đọc tên chữ cái (chép “di”, “V-cap”); nghịch→nghiệt lẫn vần |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Hướng tốt nhất tỉ lệ với nghịch đảo của S w nhân hiệu hai tâm.” — S w đọc tên chữ cái “ét vê kép”, ASR chép “SVCAP”; nghịch→nghiệp lẫn vần — các từ khác khớp
- “Lấy đạo hàm của J theo w và cho bằng 0, với hai lớp ta rút gọn được, hướng tốt nhất tỉ lệ với nghịch đảo của S w nhân hiệu hai tâm.” — J, w đọc tên chữ cái (chép “di”, “V-cap”); nghịch→nghiệt lẫn vần

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
