# Rà soát L31 — Bài 31 — Phân rã ma trận không âm (NMF): học “các phần” của dữ liệu

- Đặc tả: `lessons/L31_nmf.yaml`; nguồn: GT24 (chỉ nêu tên); DC23#Ch5 (chủ đề mở rộng); CITED: Lee & Seung, Nature 401 (1999) 788–791, doi:10.1038/44565 (quy tắc nhân, truy cập 2026-10-24, no revision given)
- Quy mô: 11 cảnh, 20 step, 7 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 15 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 4 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L31/build_report.json`): 52 khung, 299.467 s, built_at 2026-10-26T18:31:52Z, spec_sha256 `5bcbb8c4ac4060e6…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L31/asr_report.md`): câu: 52, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:08:26Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 9 | 0.906 | Bài này đổi sang X, A và B, vì chữ H in đậm đã là ma trận Hessian, còn W đã dùng cho trọng số. | Bài này đổi sang X, A và B, vì chữ H in đậm đã làm ma trận hết sen, còn V đúc đã dùng cho trọng số. | “là” → nghe thành “làm”; “w” → nghe thành “v đúc” | w | — | W đọc “vê đúp” chép “V đúc”; Hessian chép “hết sen” (tên riêng, đã có ở L07); là→làm |
| 8 | 0.941 | Lưu ý, bài báo năm 1999 làm phương pháp này nổi tiếng dùng các chữ V, W và H. | Lưu ý, bài báo năm 1999 làm phương pháp này nổi tiếng dùng các chữ V về đúc và hát. | “w” → nghe thành “về đúc” | w | — | W đọc tên chữ cái “vê đúp”, ASR chép “về đúc”; H chép “hát” — tên chữ cái |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Lưu ý, bài báo năm 1999 làm phương pháp này nổi tiếng dùng các chữ V, W và H.” — W đọc tên chữ cái “vê đúp”, ASR chép “về đúc”; H chép “hát” — tên chữ cái
- “Bài này đổi sang X, A và B, vì chữ H in đậm đã là ma trận Hessian, còn W đã dùng cho trọng số.” — W đọc “vê đúp” chép “V đúc”; Hessian chép “hết sen” (tên riêng, đã có ở L07); là→làm

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
