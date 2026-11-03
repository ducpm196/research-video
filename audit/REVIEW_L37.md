# Rà soát L37 — Bài 37 (mở rộng) — Autoencoder: nén phi tuyến bằng mạng nơ-ron (so với PCA)

- Đặc tả: `lessons/L37_autoencoder.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: Hinton & Salakhutdinov, “Reducing the dimensionality of data with neural networks”, Science 313(5786) (2006) 504–507, doi:10.1126/science.1127647 (truy cập 2026-10-24, no revision given)
- Quy mô: 11 cảnh, 16 step, 6 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 14 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 1 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L37/build_report.json`): 42 khung, 232.1 s, built_at 2026-10-26T18:36:35Z, spec_sha256 `6910492ac0ad72e4…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L37/asr_report.md`): câu: 42, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:09:25Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 10 | 0.929 | Khởi tạo ngẫu nhiên và chạy gradient descent 3000 bước. | Khởi tạo ngẫu nhiên và chạy gradient đi xem 3.000 bước. | “xen” → nghe thành “xem” | xen | — | “descent” đọc theo lexicon “đi xen”, ASR chép “đi xem” — lẫn phụ âm cuối, đúng từ (đã gặp ở L09) |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Khởi tạo ngẫu nhiên và chạy gradient descent 3000 bước.” — “descent” đọc theo lexicon “đi xen”, ASR chép “đi xem” — lẫn phụ âm cuối, đúng từ (đã gặp ở L09)

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
