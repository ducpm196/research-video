# Rà soát L15 — Bài 15 — Phân phối chuẩn nhiều chiều & ma trận hiệp phương sai

- Đặc tả: `lessons/L15_chuan_nhieu_chieu_hiep_phuong_sai.yaml`; nguồn: tex#L299 (Σ = E[(X − μ)(X − μ)ᵀ]), L301 (mật độ chuẩn nhiều chiều với |Σ|, Σ⁻¹); PR25 (Covariance and Correlation, Gaussian Random Vector)
- Quy mô: 13 cảnh, 27 step, 21 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 29 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 6 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L15/build_report.json`): 76 khung, 449.7 s, built_at 2026-10-26T18:12:45Z, spec_sha256 `4c6af42f05cdb156…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L15/asr_report.md`): câu: 76, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:03:21Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 63 | 0.889 | Câu hai đọc hình dạng elip từ ma trận. | Câu 2 đọc hình dạng elit từ ma trận | “elip” → nghe thành “elit” | elip | — | “elip” → “elit” (phụ âm cuối p/t); 3 câu khác cùng từ được chép “elipse/ellipse” (bí danh) — INFERRED ASR, cần người nghe |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Câu hai đọc hình dạng elip từ ma trận.” — “elip” → “elit” (phụ âm cuối p/t); 3 câu khác cùng từ được chép “elipse/ellipse” (bí danh) — INFERRED ASR, cần người nghe

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
