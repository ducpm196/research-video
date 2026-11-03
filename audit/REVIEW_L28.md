# Rà soát L28 — Bài 28 — Cây quyết định & rừng ngẫu nhiên (entropy, chỉ số Gini)

- Đặc tả: `lessons/L28_cay_quyet_dinh.yaml`; nguồn: GT24#Tuần 9–10; tex#L407 (Decision Tree / Forest: Entropy / Gini, “trò chơi 20 câu hỏi Yes/No” & bầu chọn đa số); ML24#Decision-tree
- Quy mô: 11 cảnh, 18 step, 9 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 17 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 3 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L28/build_report.json`): 51 khung, 302.3 s, built_at 2026-10-26T18:28:28Z, spec_sha256 `8292ef35bd860427…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L28/asr_report.md`): câu: 51, thiếu audio: 0, gắn cờ: 3, chưa xem xét: 0; checked_at 2026-10-26T19:07:46Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 6 | 0.833 | Và theo bài 13, p là tỉ lệ đếm trong nhóm. | và theo bài 13, T là tỷ lệ đếm trong nhóm. | “p” → nghe thành “t”; “tỉ” → nghe thành “tỷ” | p | tỉ | p đọc tên chữ cái “pê”, ASR chép “T”; tỉ→tỷ cùng từ |
| 15 | 0.875 | Đo bằng chỉ số Gini cũng chọn B. | Đo bằng chỉ số Vini cũng chọn B. | “gini” → nghe thành “vini” | gi, ni | — | Gini đọc “Gi-ni”, ASR chép “Vini” — tên riêng, cần người nghe |
| 3 | 0.941 | Nhắc lại bài 20, entropy bằng âm tổng p nhân lôgarit p, đo độ bất ngờ. | Nhắc lại bài 20, Entropy bằng âm tổng pê nhân Logarith P, đo độ bất ngờ. | “p” → nghe thành “pê” | p | — | p đọc “pê”, ASR chép “pê/P” — đúng; lôgarit chép Logarith |

## Đã xem xét (`asr_reviewed`, 4 mục)

- “Câu một tính chỉ số Gini và entropy của một nhóm.” — Gini đọc “Gi-ni” theo lexicon, ASR chép “Genie” (đúng âm); một→mục là lỗi quen thuộc của ASR với số 1
- “Và theo bài 13, p là tỉ lệ đếm trong nhóm.” — p đọc tên chữ cái “pê”, ASR chép “T”; tỉ→tỷ cùng từ
- “Nhắc lại bài 20, entropy bằng âm tổng p nhân lôgarit p, đo độ bất ngờ.” — p đọc “pê”, ASR chép “pê/P” — đúng; lôgarit chép Logarith
- “Đo bằng chỉ số Gini cũng chọn B.” — Gini đọc “Gi-ni”, ASR chép “Vini” — tên riêng, cần người nghe

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
