# Rà soát L27 — Bài 27 — K láng giềng gần nhất (KNN): học lười, khoảng cách L1/L2, chọn K

- Đặc tả: `lessons/L27_knn.yaml`; nguồn: tex#L165–L166, L405 (KNN: khoảng cách Euclid/L1, “ngưu tầm ngưu”: bầu chọn theo K láng giềng); AG24#KNN (huấn luyện O(1), dự đoán O(N); L1, L2); AG25#KNN; AUDIT A14
- Quy mô: 12 cảnh, 18 step, 10 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 18 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 5 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L27/build_report.json`): 56 khung, 306.233 s, built_at 2026-10-26T18:27:32Z, spec_sha256 `c732a900bd4211d1…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L27/asr_report.md`): câu: 56, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:07:28Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 22 | 0.769 | Theo L một, P cách 3, Q cách 4, nên P gần hơn. | Theo L1, T cách 3, quỷ cách 4 nên T gần hơn. | “p” → nghe thành “t”; “q” → nghe thành “quỷ”; “p” → nghe thành “t” | p, q, p | — | P, Q đọc tên chữ cái (“pê”, “quy”), ASR chép “T”, “quỷ”; L một chép “L1” — đúng |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Theo L một, P cách 3, Q cách 4, nên P gần hơn.” — P, Q đọc tên chữ cái (“pê”, “quy”), ASR chép “T”, “quỷ”; L một chép “L1” — đúng

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
