# Rà soát L24 — Bài 24 — Tối ưu có ràng buộc: nhân tử Lagrange & điều kiện KKT (cầu nối sang SVM)

- Đặc tả: `lessons/L24_lagrange_kkt.yaml`; nguồn: PR25#Categorical-ML (nhân tử Lagrange cho ràng buộc tổng = 1); SYLLABUS_CS115.md N2, §6 (thêm vì SVM dạng đối ngẫu và NMF cần)
- Quy mô: 13 cảnh, 22 step, 12 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 20 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L24/build_report.json`): 66 khung, 384.933 s, built_at 2026-10-26T18:24:36Z, spec_sha256 `833d26cfc2cf2c6b…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L24/asr_report.md`): câu: 66, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:06:30Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 13 | 0.833 | Gói lại thành hàm Lagrange, chữ L uốn cong, bằng f trừ lam-đa nhân g, rồi cho mọi đạo hàm riêng bằng 0. | Gói lại thành hàm Lagrang, chữ L uống công, bằng ép trừ Lam đa nhân vê, rồi cho mọi đạo hàm riêng bằng không. | “lagrange” → nghe thành “lagrang”; “uốn cong” → nghe thành “uống công”; “g” → nghe thành “v” | la, gơ, răng, g | uốn, cong | Lagrange đọc “La-gơ-răng”, ASR chép “Lagrang” (đúng âm); uốn cong→uống công lẫn thanh; f, g đọc tên chữ cái |
| 4 | 0.95 | Hôm nay ta tìm cực trị khi các biến bị ràng buộc, bằng nhân tử Lagrange và điều kiện KKT. | Hôm nay ta tìm cực trị khi các biến bị ràng buộc bằng nhân tử Lagrang và điều kiện KKT. | “lagrange” → nghe thành “lagrang” | la, gơ, răng | — | Lagrange đọc “La-gơ-răng”, ASR chép “Lagrang” — đúng âm (nút thắt B50 OPEN, cần người nghe) |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Gói lại thành hàm Lagrange, chữ L uốn cong, bằng f trừ lam-đa nhân g, rồi cho mọi đạo hàm riêng bằng 0.” — Lagrange đọc “La-gơ-răng”, ASR chép “Lagrang” (đúng âm); uốn cong→uống công lẫn thanh; f, g đọc tên chữ cái
- “Hôm nay ta tìm cực trị khi các biến bị ràng buộc, bằng nhân tử Lagrange và điều kiện KKT.” — Lagrange đọc “La-gơ-răng”, ASR chép “Lagrang” — đúng âm (nút thắt B50 OPEN, cần người nghe)

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
