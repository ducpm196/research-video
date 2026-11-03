# Rà soát L36 — Bài 36 (mở rộng) — Boosting: AdaBoost & gradient boosting (so với rừng ngẫu nhiên)

- Đặc tả: `lessons/L36_boosting.yaml`; nguồn: 0 kết quả trong nguồn môn học; CITED: Freund & Schapire, J. Computer and System Sciences 55(1) (1997) 119–139, doi:10.1006/jcss.1997.1504 (truy cập 2026-10-24, no revision given)
- Quy mô: 11 cảnh, 17 step, 7 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 15 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 3 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L36/build_report.json`): 48 khung, 269.633 s, built_at 2026-10-26T18:35:56Z, spec_sha256 `31995c255a7e4529…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L36/asr_report.md`): câu: 48, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:09:24Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 2 | 0.867 | Hôm nay ta học hai cách, AdaBoost và tăng cường theo gradient. | Hôm nay ta học 2 cách adabook và tăng cường theo gradient. | “a đa bút” → nghe thành “adabook” | a, đa, bút | — | AdaBoost đọc “A-đa-bút” theo lexicon, ASR chép “adabook” (gần đúng âm, tên riêng chưa có probe riêng) — cần người nghe |
| 42 | 0.941 | AdaBoost tính trọng số mô hình từ sai số và tăng trọng số các mẫu bị sai. | Adabook tính trọng số mô hình từ sai số và tăng trọng số các mẫu bị sai. | “adaboost” → nghe thành “adabook” | a, đa, bút | — | AdaBoost chép “Adabook” — như câu giới thiệu |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Hôm nay ta học hai cách, AdaBoost và tăng cường theo gradient.” — AdaBoost đọc “A-đa-bút” theo lexicon, ASR chép “adabook” (gần đúng âm, tên riêng chưa có probe riêng) — cần người nghe
- “AdaBoost tính trọng số mô hình từ sai số và tăng trọng số các mẫu bị sai.” — AdaBoost chép “Adabook” — như câu giới thiệu

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
