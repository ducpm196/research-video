# Rà soát L40 — Bài 40 (mở rộng) — UMAP: giảm chiều bằng đồ thị láng giềng (so với t-SNE)

- Đặc tả: `lessons/L40_umap.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: McInnes, Healy & Melville, “UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction”, arXiv:1802.03426 (2018) (truy cập 2026-10-24, no revision given)
- Quy mô: 9 cảnh, 14 step, 5 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 13 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L40/build_report.json`): 35 khung, 210.833 s, built_at 2026-10-26T18:38:32Z, spec_sha256 `a2da65949493c3bd…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L40/asr_report.md`): câu: 35, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:09:28Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 12 | 0.917 | Thay số, sai số nhỏ nhất khi v bằng đúng w. | Thay số, sai số nhỏ nhất khi về bằng đúng về kết. | “kép” → nghe thành “kết” | kép | — | v, w đọc tên chữ cái (“vê”, “vê kép”), ASR chép “về”, “về kết” |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Thay số, sai số nhỏ nhất khi v bằng đúng w.” — v, w đọc tên chữ cái (“vê”, “vê kép”), ASR chép “về”, “về kết”

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
