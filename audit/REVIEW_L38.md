# Rà soát L38 — Bài 38 (mở rộng) — Phân tích thành phần độc lập (ICA): tách các nguồn bị trộn lẫn

- Đặc tả: `lessons/L38_ica.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: Hyvärinen & Oja, “Independent component analysis: algorithms and applications”, Neural Networks 13(4–5) (2000) 411–430 (truy cập 2026-10-25, bản PDF itb.biologie.hu-berlin.de, inc.ucsd.edu; no revision given)
- Quy mô: 10 cảnh, 16 step, 9 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 17 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 3 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L38/build_report.json`): 40 khung, 227.933 s, built_at 2026-10-26T18:37:15Z, spec_sha256 `5bf6308f573aee47…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L38/asr_report.md`): câu: 40, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:09:26Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 16 | 0.951 | Lý do là đổi chỗ hai nguồn cùng hai cột của A, hay nhân một nguồn với 2 và chia cột tương ứng cho 2, hỗn hợp vẫn y như cũ. | Lý do là đổi chỗ hai nguồn cùng hai cột qua, hay nhân một nguồn với hai và chia cột tương ứng cho hai, hỗn hợp vẫn y như cũ. | “của a” → nghe thành “qua” | a | của | “của A” bị ASR gộp thành “qua” (tên chữ cái A đứng sau “của”); phần còn lại khớp |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Lý do là đổi chỗ hai nguồn cùng hai cột của A, hay nhân một nguồn với 2 và chia cột tương ứng cho 2, hỗn hợp vẫn y như cũ.” — “của A” bị ASR gộp thành “qua” (tên chữ cái A đứng sau “của”); phần còn lại khớp

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
