# Rà soát L34 — Bài 34 (mở rộng) — Phép tích chập & mạng nơ-ron tích chập (CNN)

- Đặc tả: `lessons/L34_cnn.yaml`; nguồn: ML24, NN, VC24 (chỉ nhắc tên CNN); CITED: LeCun, Bottou, Bengio & Haffner, “Gradient-based learning applied to document recognition”, Proc. IEEE 86(11) (1998) 2278–2324, doi:10.1109/5.726791 (truy cập 2026-10-24, no revision given)
- Quy mô: 10 cảnh, 17 step, 11 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 19 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L34/build_report.json`): 47 khung, 277.267 s, built_at 2026-10-26T18:34:24Z, spec_sha256 `bac022874ca443e8…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L34/asr_report.md`): câu: 47, thiếu audio: 0, gắn cờ: 3, chưa xem xét: 0; checked_at 2026-10-26T19:09:21Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 10 | 0.773 | Kích thước đầu ra bằng cạnh ảnh trừ cạnh bộ lọc cộng hai lần đệm, chia cho bước nhảy, rồi cộng 1. | Kết thức đầu ra bằng cạnh ảnh trừ cảnh bộ lọc cộng hai lần đêm, chia cho bước nhảy, rồi cộng mục. | “kích thước” → nghe thành “kết thức”; “cạnh” → nghe thành “cảnh”; “đệm” → nghe thành “đêm”; “một” → nghe thành “mục” | — | kích, cạnh, một | lẫn thanh ở nhiều từ (kích thước→kết thức, cạnh→cảnh, đệm→đêm, một→mục); câu dài, cấu trúc nghe đúng — CẦN NGƯỜI NGHE xác nhận |
| 3 | 0.947 | Nhắc lại bài 23, một lớp của mạng nhiều lớp nối mỗi đầu ra với mọi đầu vào, qua ma trận W rồi hàm ReLU. | Nhắc lại bài 23, một lớp của mạng nhiều lớp nối mỗi đầu ra với mọi đầu vào, qua ma trận vê đúc rồi hàm re lu. | “w” → nghe thành “v đúc” | w | — | W đọc “vê đúp”, ASR chép “vê đúc”; ReLU chép “re lu” — đúng |
| 27 | 0.964 | Nó chỉ chọn số lớn nhất, và lượt lùi dồn gradient cho ô lớn nhất, giống cổng lấy số lớn hơn của bài 22. | Nó chỉ chọn số lớn nhất và lượt lùi dồn gradient cho O lớn nhất, giống cổng lấy số lớn hơn của bài 22. | “ô” → nghe thành “o” | ô | — | “ô” chép “O” — cùng âm |

## Đã xem xét (`asr_reviewed`, 3 mục)

- “Kích thước đầu ra bằng cạnh ảnh trừ cạnh bộ lọc cộng hai lần đệm, chia cho bước nhảy, rồi cộng 1.” — lẫn thanh ở nhiều từ (kích thước→kết thức, cạnh→cảnh, đệm→đêm, một→mục); câu dài, cấu trúc nghe đúng — CẦN NGƯỜI NGHE xác nhận
- “Nhắc lại bài 23, một lớp của mạng nhiều lớp nối mỗi đầu ra với mọi đầu vào, qua ma trận W rồi hàm ReLU.” — W đọc “vê đúp”, ASR chép “vê đúc”; ReLU chép “re lu” — đúng
- “Nó chỉ chọn số lớn nhất, và lượt lùi dồn gradient cho ô lớn nhất, giống cổng lấy số lớn hơn của bài 22.” — “ô” chép “O” — cùng âm

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
