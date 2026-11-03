# Rà soát L13 — Bài 13 — Xác suất rời rạc: có điều kiện, định lý Bayes, kỳ vọng, phương sai

- Đặc tả: `lessons/L13_xac_suat_roi_rac.yaml`; nguồn: tex#L296–L298 (P(A|B), kỳ vọng, phương sai), L313 (MAP dùng Bayes mà không phát biểu); PR25 (PMF, tính chất kỳ vọng/phương sai, phân phối phân loại)
- Quy mô: 15 cảnh, 35 step, 35 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 43 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 15 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L13/build_report.json`): 110 khung, 591.433 s, built_at 2026-10-26T18:09:53Z, spec_sha256 `01a54e31fe1b6d43…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L13/asr_report.md`): câu: 110, thiếu audio: 0, gắn cờ: 5, chưa xem xét: 0; checked_at 2026-10-26T19:01:36Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 94 | 0.786 | Một, biết xúc xắc ra số chẵn, xác suất ra 6 là bao nhiêu. | 1. Biết xuất sắc ra số chẳng, sát xuất ra 6 là bao nhiêu? | “xúc” → nghe thành “xuất”; “chẵn xác” → nghe thành “chẳng sát” | — | xúc, chẵn, xác | “xúc xắc” → “xuất sắc”, “chẵn” → “chẳng” (cặp s/x và ngã/hỏi; các câu khác có “xúc xắc”, “chẵn” cũng bị chép vậy — bảng tham khảo) — INFERRED ASR, cần người nghe |
| 34 | 0.857 | Chia hai vế cho xác suất của B, ta được định lý Bayes. | Chia 2 với cho xác suất của B, ta được định lý bay S. | “vế” → nghe thành “với”; “ét” → nghe thành “s” | ét | vế | B41: “Bay-ét” → small/medium chép “bay ếc / bay S / bay x / bay ác” (phụ âm cuối t nghe thành ch/x) — cùng kiểu ở probe l13_probe.py (3/8); INFERRED ASR nghe nhầm âm cuối, cần người nghe; “vế” → “với” |
| 6 | 0.875 | Bắt đầu từ ký hiệu đầu tiên, P của A, đọc là xác suất của A. | Bắt đầu từ ký hiệu đầu tiên, Thê của A, đọc là xác sức của A. | “p” → nghe thành “thê”; “suất” → nghe thành “sức” | p | — | tên chữ P (pê) → “Thê” (tên chữ cái một âm tiết); “suất” → “sức” — INFERRED ASR nghe nhầm |
| 5 | 0.92 | Hôm nay ta học xác suất có điều kiện và định lý Bayes để hiểu vì sao, rồi học kỳ vọng và phương sai. | Hôm nay ta học xác suốt có điều kiện và định lý bay ếc để hiểu vì sao, rồi học kỳ vọng và phương sai. | “suất” → nghe thành “suốt”; “ét” → nghe thành “ếc” | ét | suất | B41: “Bay-ét” → small/medium chép “bay ếc / bay S / bay x / bay ác” (phụ âm cuối t nghe thành ch/x) — cùng kiểu ở probe l13_probe.py (3/8); INFERRED ASR nghe nhầm âm cuối, cần người nghe; “suất” → “suốt” |
| 23 | 0.941 | Ký hiệu chữ U ngược giữa A và B nghĩa là A và B cùng xảy ra. | Ký hiệu chữ úng ngược giữa A và B nghĩa là A và B cùng xảy ra. | “u” → nghe thành “úng” | u | — | tên chữ U → “úng” (tên chữ cái một âm tiết) — INFERRED ASR nghe nhầm |

## Đã xem xét (`asr_reviewed`, 5 mục)

- “Hôm nay ta học xác suất có điều kiện và định lý Bayes để hiểu vì sao, rồi học kỳ vọng và phương sai.” — B41: “Bay-ét” → small/medium chép “bay ếc / bay S / bay x / bay ác” (phụ âm cuối t nghe thành ch/x) — cùng kiểu ở probe l13_probe.py (3/8); INFERRED ASR nghe nhầm âm cuối, cần người nghe; “suất” → “suốt”
- “Chia hai vế cho xác suất của B, ta được định lý Bayes.” — B41: “Bay-ét” → small/medium chép “bay ếc / bay S / bay x / bay ác” (phụ âm cuối t nghe thành ch/x) — cùng kiểu ở probe l13_probe.py (3/8); INFERRED ASR nghe nhầm âm cuối, cần người nghe; “vế” → “với”
- “Bắt đầu từ ký hiệu đầu tiên, P của A, đọc là xác suất của A.” — tên chữ P (pê) → “Thê” (tên chữ cái một âm tiết); “suất” → “sức” — INFERRED ASR nghe nhầm
- “Ký hiệu chữ U ngược giữa A và B nghĩa là A và B cùng xảy ra.” — tên chữ U → “úng” (tên chữ cái một âm tiết) — INFERRED ASR nghe nhầm
- “Một, biết xúc xắc ra số chẵn, xác suất ra 6 là bao nhiêu.” — “xúc xắc” → “xuất sắc”, “chẵn” → “chẳng” (cặp s/x và ngã/hỏi; các câu khác có “xúc xắc”, “chẵn” cũng bị chép vậy — bảng tham khảo) — INFERRED ASR, cần người nghe

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
