# Rà soát L21 — Bài 21 — Đánh giá mô hình phân loại: ma trận nhầm lẫn, accuracy, precision, recall, F1

- Đặc tả: `lessons/L21_danh_gia_phan_loai.yaml`; nguồn: ML24#Evaluation (văn bản trích dòng 34: Confusion matrix, Accuracy, Precision, Recall, F-score; dòng 36: ROC, AUC — chỉ nêu tên)
- Quy mô: 11 cảnh, 19 step, 9 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 17 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 4 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L21/build_report.json`): 59 khung, 328.3 s, built_at 2026-10-26T18:20:56Z, spec_sha256 `9d86a3ec75d88393…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L21/asr_report.md`): câu: 59, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:05:48Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 34 | 0.885 | Các chỉ số khớp với bài 13, nghĩa là độ chuẩn xác chính là xác suất hậu nghiệm ta đã tính bằng định lý Bayes. | Các trị số khớp với bài 13, nghĩa là đồ chuẩn xác chính là xác suất hậu nghiệm ta đã tính bằng định lý Bayet. | “chỉ” → nghe thành “trị”; “độ” → nghe thành “đồ”; “bayes” → nghe thành “bayet” | ét | chỉ | Bayes đọc “Bay-ét” theo lexicon, ASR chép “Bayet” (đúng âm); chỉ→trị, độ→đồ lẫn phụ âm đầu/thanh — câu dài, ngữ cảnh rõ |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Các chỉ số khớp với bài 13, nghĩa là độ chuẩn xác chính là xác suất hậu nghiệm ta đã tính bằng định lý Bayes.” — Bayes đọc “Bay-ét” theo lexicon, ASR chép “Bayet” (đúng âm); chỉ→trị, độ→đồ lẫn phụ âm đầu/thanh — câu dài, ngữ cảnh rõ

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
