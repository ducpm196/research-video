# Rà soát L43 — Bài 43 (mở rộng) — Mô hình sinh (2): mô hình khuếch tán (diffusion)

- Đặc tả: `lessons/L43_diffusion.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: Ho, Jain & Abbeel, “Denoising Diffusion Probabilistic Models”, arXiv:2006.11239 (2020) (truy cập 2026-10-24, no revision given)
- Quy mô: 10 cảnh, 14 step, 4 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 12 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 3 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L43/build_report.json`): 36 khung, 216.6 s, built_at 2026-10-26T18:40:37Z, spec_sha256 `712465910720aa7b…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L43/asr_report.md`): câu: 36, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:09:32Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 18 | 0.786 | Lỗi thứ nhất, nhầm bê-ta ở đây với bê-ta của bài 9. | Lỗi thứ nhất, nhằm beta ở đây với beta của bài 9. | “nhầm b” → nghe thành “nhằm bê”; “b” → nghe thành “bê” | — | nhầm | bê-ta được ASR chép đúng “beta” (bộ chấm quy “bê” về chữ b nên lệch); nhầm→nhằm lẫn thanh |
| 27 | 0.793 | Câu hai, hệ số của ảnh gốc bằng 0 phẩy 9, hệ số của nhiễu bằng căn 0 phẩy 19, xấp xỉ 0 phẩy 436. | Câu 2, hề số của ảnh gốc bằng 0,9, hề số của nhiểu bằng căng 0,19, xắp xỉ 0,436. | “hệ” → nghe thành “hề”; “hệ” → nghe thành “hề”; “nhiễu” → nghe thành “nhiểu”; “căn” → nghe thành “căng”; “xấp” → nghe thành “xắp”; “không phẩy” → nghe thành “” | — | hệ, hệ, nhiễu, căn, xấp, không, phẩy | lẫn thanh hệ→hề, nhiễu→nhiểu, căn→căng; mọi con số khớp |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Lỗi thứ nhất, nhầm bê-ta ở đây với bê-ta của bài 9.” — bê-ta được ASR chép đúng “beta” (bộ chấm quy “bê” về chữ b nên lệch); nhầm→nhằm lẫn thanh
- “Câu hai, hệ số của ảnh gốc bằng 0 phẩy 9, hệ số của nhiễu bằng căn 0 phẩy 19, xấp xỉ 0 phẩy 436.” — lẫn thanh hệ→hề, nhiễu→nhiểu, căn→căng; mọi con số khớp

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
