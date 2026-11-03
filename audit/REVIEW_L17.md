# Rà soát L17 — Bài 17 — Ước lượng tham số: MLE, MAP, Bayes

- Đặc tả: `lessons/L17_mle_map_bayes.yaml`; nguồn: tex#L305–L330 (MLE, MAP, Bayesian Inference; MLE của μ trong phân phối chuẩn); PR25 (MLE cần dữ liệu độc lập; Categorical ML; MAP với prior Dirichlet = số đếm giả; ML/MAP quá tự tin khi ít dữ liệu); AUDIT A8
- Quy mô: 14 cảnh, 26 step, 19 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 27 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 4 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L17/build_report.json`): 73 khung, 436.2 s, built_at 2026-10-26T18:15:46Z, spec_sha256 `a83ee81fa3b970db…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L17/asr_report.md`): câu: 73, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:11:24Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 39 | 0.935 | Khi ít dữ liệu, cách Bayes cho dự đoán ôn hoà hơn, vì nó biết mình chưa chắc chắn, còn hai cách chọn một điểm có thể quá tự tin. | Khi ít giữ liệu, cách bay S cho giữ đoán ôn hòa hơn, vì nó biết mình chưa chắc chắn, còn hai cách chọn 1 điểm có thể quá tự tin. | “ét” → nghe thành “s”; “dự” → nghe thành “giữ” | ét | — | B41: “Bay-ét” → “bay S” (âm cuối ét); “dự → giữ” giọng Bắc d = gi — INFERRED ASR, cần người nghe; câu viết lại 2026-10-27 (bỏ “theo bài giảng của môn học”) |
| 36 | 0.938 | Cách tiếp cận Bayes không chọn một thê ta duy nhất, mà giữ cả hậu nghiệm. | Cách tiếp cận Bayet không chọn một theta duy nhất mà giữ cả hậu nghiệm. | “bayes” → nghe thành “bayet” | ét | — | B41: “Bay-ét” → “Bayet” (đúng âm đã chọn; không thêm bí danh vì không phải chính tả đúng) — INFERRED ASR, cần người nghe |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Cách tiếp cận Bayes không chọn một thê ta duy nhất, mà giữ cả hậu nghiệm.” — B41: “Bay-ét” → “Bayet” (đúng âm đã chọn; không thêm bí danh vì không phải chính tả đúng) — INFERRED ASR, cần người nghe
- “Khi ít dữ liệu, cách Bayes cho dự đoán ôn hoà hơn, vì nó biết mình chưa chắc chắn, còn hai cách chọn một điểm có thể quá tự tin.” — B41: “Bay-ét” → “bay S” (âm cuối ét); “dự → giữ” giọng Bắc d = gi — INFERRED ASR, cần người nghe; câu viết lại 2026-10-27 (bỏ “theo bài giảng của môn học”)

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
