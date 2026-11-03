# Rà soát L35 — Bài 35 (mở rộng) — Mạng nơ-ron hồi tiếp (RNN), lan truyền ngược theo thời gian & LSTM

- Đặc tả: `lessons/L35_rnn_lstm.yaml`; nguồn: ML24, NN (chỉ nhắc tên RNN); CITED: Hochreiter & Schmidhuber, “Long Short-Term Memory”, Neural Computation 9(8) (1997) 1735–1780 (truy cập 2026-10-24, no revision given)
- Quy mô: 10 cảnh, 17 step, 10 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 18 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L35/build_report.json`): 46 khung, 271.8 s, built_at 2026-10-26T18:35:10Z, spec_sha256 `c38e2db590451545…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L35/asr_report.md`): câu: 46, thiếu audio: 0, gắn cờ: 5, chưa xem xét: 0; checked_at 2026-10-26T19:09:22Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 5 | 0.875 | Mạng hồi tiếp tính trạng thái mới h t bằng tanh của W nhân trạng thái cũ cộng U nhân từ mới, với W và U giống nhau ở mọi bước. | Mạng hồi tiếp tính trạng thái mới ht bằng tanh của Vê Đúc nhân trạng thái của Cộng U nhân từ mới, với Vê Đúc và U giống nhau ở mọi bước. | “w” → nghe thành “v đúc”; “cũ” → nghe thành “của”; “w” → nghe thành “v đúc” | w, w | cũ | W đọc “vê đúp”, ASR chép “Vê Đúc”; h t chép “ht”; cũ→của lẫn vần |
| 18 | 0.894 | Theo đường ô nhớ, gradient chỉ nhân với cổng quên, và mạng học giữ nó gần bằng 1 khi cần nhớ lâu. | Theo đường ô nhớ, Grady ần chỉ nhân với Cổng Quyên và mạng học giữ nó gần bằng một khi cần nhớ lâu. | “grê đi” → nghe thành “grady”; “quên” → nghe thành “quyên” | grê, đi | — | gradient đọc theo lexicon, ASR chép “Grady ần”; quên→Quyên lẫn vần — cần người nghe |
| 26 | 0.897 | Lỗi thứ hai, quên cộng dồn gradient của W qua các bước. | Lỗi thứ 2, quên cộng dồn gradient của V-dub qua các bước. | “w” → nghe thành “v dub” | w | — | W chép “V-dub” — tên chữ cái |
| 21 | 0.909 | Gradient của W được cộng dồn qua mọi bước. | Gradient của VDUC được cộng dồn qua mọi bước. | “w” → nghe thành “vduc” | w | — | W chép “VDUC” — tên chữ cái |
| 27 | 0.919 | Cùng một W được dùng ở mọi bước, nên giống cổng phân nhánh ở bài 22. | Cùng một vế đúc được dùng ở mọi bước nên giống cổng phân nhánh ở bài 22. | “w” → nghe thành “vế đúc” | w | — | W chép “vế đúc” — tên chữ cái |

## Đã xem xét (`asr_reviewed`, 5 mục)

- “Mạng hồi tiếp tính trạng thái mới h t bằng tanh của W nhân trạng thái cũ cộng U nhân từ mới, với W và U giống nhau ở mọi bước.” — W đọc “vê đúp”, ASR chép “Vê Đúc”; h t chép “ht”; cũ→của lẫn vần
- “Theo đường ô nhớ, gradient chỉ nhân với cổng quên, và mạng học giữ nó gần bằng 1 khi cần nhớ lâu.” — gradient đọc theo lexicon, ASR chép “Grady ần”; quên→Quyên lẫn vần — cần người nghe
- “Lỗi thứ hai, quên cộng dồn gradient của W qua các bước.” — W chép “V-dub” — tên chữ cái
- “Gradient của W được cộng dồn qua mọi bước.” — W chép “VDUC” — tên chữ cái
- “Cùng một W được dùng ở mọi bước, nên giống cổng phân nhánh ở bài 22.” — W chép “vế đúc” — tên chữ cái

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
