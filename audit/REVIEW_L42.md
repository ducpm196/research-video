# Rà soát L42 — Bài 42 (mở rộng) — Mô hình sinh (1): Variational Autoencoder & GAN

- Đặc tả: `lessons/L42_vae_gan.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: Kingma & Welling, “Auto-Encoding Variational Bayes”, arXiv:1312.6114 (2013); Goodfellow et al., “Generative Adversarial Nets”, arXiv:1406.2661 (2014) (truy cập 2026-10-24, no revision given)
- Quy mô: 10 cảnh, 16 step, 9 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 17 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 4 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L42/build_report.json`): 43 khung, 251.267 s, built_at 2026-10-26T18:39:58Z, spec_sha256 `369e27dbf9d1d2a9…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L42/asr_report.md`): câu: 43, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:09:31Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 3 | 0.947 | Nhắc lại bài 17, ước lượng hợp lý cực đại làm lớn lôgarit khả năng của dữ liệu. | Nhắc lại bài 17, ước lượng hợp lý cực đại làm lớn logatrix khả năng của dữ liệu. | “lôgarit” → nghe thành “logatrix” | lôgarit | — | “lôgarit” chính tả SGK, ASR chép “logatrix” (đã ghi ở L12); phần còn lại khớp |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Nhắc lại bài 17, ước lượng hợp lý cực đại làm lớn lôgarit khả năng của dữ liệu.” — “lôgarit” chính tả SGK, ASR chép “logatrix” (đã ghi ở L12); phần còn lại khớp

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
