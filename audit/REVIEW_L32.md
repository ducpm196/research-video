# Rà soát L32 — Bài 32 — t-SNE: trực quan hoá dữ liệu nhiều chiều bằng xác suất láng giềng

- Đặc tả: `lessons/L32_tsne.yaml`; nguồn: NGOÀI mọi nguồn môn học (0 kết quả trên 13 PDF + tex) — thêm theo yêu cầu người dùng; CITED: van der Maaten & Hinton, “Visualizing Data using t-SNE”, JMLR 9 (2008) 2579–2605 (truy cập 2026-10-24, no revision given)
- Quy mô: 12 cảnh, 17 step, 10 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 18 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 6 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L32/build_report.json`): 51 khung, 290.767 s, built_at 2026-10-26T18:32:40Z, spec_sha256 `4dd0f74ce51a5eb1…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L32/asr_report.md`): câu: 51, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:08:28Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 6 | 0.967 | Ở không gian gốc, xác suất điểm i chọn điểm j làm láng giềng được tính bằng hình chuông của khoảng cách, rồi chia cho tổng như bài 20. | Ở không gian gốc, xác xuất điểm y chọn điểm gì làm láng giềng được tính bằng hình chuông của khoảng cách, rồi chia cho tổng như bài 20. | “j” → nghe thành “gì” | j | — | i, j đọc tên chữ cái, ASR chép “y”, “gì”; câu còn lại khớp |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Ở không gian gốc, xác suất điểm i chọn điểm j làm láng giềng được tính bằng hình chuông của khoảng cách, rồi chia cho tổng như bài 20.” — i, j đọc tên chữ cái, ASR chép “y”, “gì”; câu còn lại khớp

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
