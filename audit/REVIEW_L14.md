# Rà soát L14 — Bài 14 — Biến ngẫu nhiên liên tục, hàm mật độ & phân phối chuẩn một chiều

- Đặc tả: `lessons/L14_bien_lien_tuc_phan_phoi_chuan.yaml`; nguồn: tex#L297–L300 (kỳ vọng, phương sai, N(μ, σ²) với exp), L317 (tích phân trong suy luận Bayes); PR25 (PMF vs PDF, Univariate Normal: 2 tham số μ và σ² > 0)
- Quy mô: 12 cảnh, 26 step, 17 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 25 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 5 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L14/build_report.json`): 74 khung, 438.5 s, built_at 2026-10-26T19:12:47Z, spec_sha256 `8e4aabea188915d3…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L14/asr_report.md`): câu: 74, thiếu audio: 0, gắn cờ: 3, chưa xem xét: 0; checked_at 2026-10-26T19:02:49Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 28 | 0.78 | Ký hiệu chữ N hoa uốn cong là phân phối chuẩn, với hai tham số, muy và xích ma bình phương. | Ký hiệu chữ N hoa uống công là phân phối chuẩn, với hai tham số, My và Sigma bình phương. | “uốn cong” → nghe thành “uống công”; “muy” → nghe thành “my”; “xích ma” → nghe thành “sigma” | — | uốn, cong, muy | B52: “muy” (tên chữ μ) → small/medium chép “nguy/mùi/my” ở 9 câu toàn bài (bảng tham khảo) — INFERRED ASR không biết tên chữ Hy Lạp, cần người nghe; “uốn cong” → “uống công” (thanh điệu); “xích ma” → “Sigma” (khớp nghĩa) |
| 33 | 0.842 | Theo bài 12, e mũ một số âm luôn dương và nhỏ dần khi x đi xa muy. | Theo bài 12, em mũ một số âm lung dương và nhỏ dần khi ít đi xa mùi. | “e” → nghe thành “em”; “luôn” → nghe thành “lung”; “muy” → nghe thành “mùi” | e | luôn, muy | B52: “muy” (tên chữ μ) → small/medium chép “nguy/mùi/my” ở 9 câu toàn bài (bảng tham khảo) — INFERRED ASR không biết tên chữ Hy Lạp, cần người nghe; chữ e → “em”, x → “ít” (tên chữ cái một âm tiết) |
| 15 | 0.944 | Ký hiệu mới, hình chữ S kéo dài, đọc là tích phân từ a đến b của f. | Ký hiệu mới, hình chữ S kéo dài, đọc là tích phân từ A đến B của S. | “f” → nghe thành “s” | f | — | tên chữ f (ép) → “S” (tên chữ cái một âm tiết) — INFERRED ASR nghe nhầm |

## Đã xem xét (`asr_reviewed`, 6 mục)

- “Với mọi phân phối chuẩn, khoảng muy cộng trừ một xích ma chứa khoảng 68 phần trăm diện tích, hai xích ma chứa 95 phần trăm, ba xích ma chứa 99 phẩy 7 phần trăm.” — B52: “muy” (tên chữ μ) → small/medium chép “nguy/mùi/my” ở 9 câu toàn bài (bảng tham khảo) — INFERRED ASR không biết tên chữ Hy Lạp, cần người nghe; “xích ma” (tên chữ σ) → “sít ma/Sigma” — INFERRED ASR, cùng kiểu ở bảng tham khảo; “phần trăm” chép thành ký hiệu % (khớp nghĩa)
- “Ký hiệu chữ N hoa uốn cong là phân phối chuẩn, với hai tham số, muy và xích ma bình phương.” — B52: “muy” (tên chữ μ) → small/medium chép “nguy/mùi/my” ở 9 câu toàn bài (bảng tham khảo) — INFERRED ASR không biết tên chữ Hy Lạp, cần người nghe; “uốn cong” → “uống công” (thanh điệu); “xích ma” → “Sigma” (khớp nghĩa)
- “Chọn ngẫu nhiên một người, xác suất người đó cao đúng 170 xăng ti mét, không lệch dù một phần triệu mi li mét, là bao nhiêu?” — “xăng ti mét”, “mi li mét” chép thành “cm”, “millimet” (khớp nghĩa); “xác suất” → “xá suốt” (cặp s/x, cùng kiểu ở nhiều câu khác) — INFERRED ASR
- “Theo bài 12, e mũ một số âm luôn dương và nhỏ dần khi x đi xa muy.” — B52: “muy” (tên chữ μ) → small/medium chép “nguy/mùi/my” ở 9 câu toàn bài (bảng tham khảo) — INFERRED ASR không biết tên chữ Hy Lạp, cần người nghe; chữ e → “em”, x → “ít” (tên chữ cái một âm tiết)
- “Ký hiệu mới, hình chữ S kéo dài, đọc là tích phân từ a đến b của f.” — tên chữ f (ép) → “S” (tên chữ cái một âm tiết) — INFERRED ASR nghe nhầm
- “Phân phối này còn có tên khác theo tên một nhà toán học, và sách hay viết mật độ bằng chữ p thường, còn bài này dùng chữ f để khỏi lẫn với xác suất.” — tên chữ f (ép) → “s” (tên chữ cái một âm tiết); độ khớp 0,971 — INFERRED ASR nghe nhầm

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
