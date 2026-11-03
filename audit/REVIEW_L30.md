# Rà soát L30 — Bài 30 — Mô hình hỗn hợp Gauss (GMM) & thuật toán EM

- Đặc tả: `lessons/L30_gmm_em.yaml`; nguồn: DC23#Ch5 (GMM, EM)
- Quy mô: 12 cảnh, 18 step, 8 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 16 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L30/build_report.json`): 46 khung, 290.933 s, built_at 2026-10-26T18:30:28Z, spec_sha256 `abbdbdf745d72750…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L30/asr_report.md`): câu: 46, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:08:07Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 4 | 0.818 | Bài 13, định lý Bayes đảo chiều điều kiện. | Bài 13. Định lý bay S đảo chiêu điều kiện | “ét” → nghe thành “s”; “chiều” → nghe thành “chiêu” | ét | chiều | Bayes đọc “Bay-ét” (nút thắt B41 PARTIAL, probe 3/8), ASR chép “bay S”; chiều→chiêu lẫn thanh |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Bài 13, định lý Bayes đảo chiều điều kiện.” — Bayes đọc “Bay-ét” (nút thắt B41 PARTIAL, probe 3/8), ASR chép “bay S”; chiều→chiêu lẫn thanh

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
