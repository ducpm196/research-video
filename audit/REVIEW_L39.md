# Rà soát L39 — Bài 39 (mở rộng) — Học tăng cường: quá trình quyết định Markov, phương trình Bellman & Q-learning

- Đặc tả: `lessons/L39_hoc_tang_cuong.yaml`; nguồn: ML24 (chỉ nêu là một loại bài toán); CITED: Sutton & Barto, Reinforcement Learning: An Introduction, 2nd ed., MIT Press (2018), ISBN 9780262039246 (truy cập 2026-10-24, no revision given)
- Quy mô: 10 cảnh, 16 step, 7 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 15 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 2 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L39/build_report.json`): 39 khung, 236.033 s, built_at 2026-10-26T18:37:56Z, spec_sha256 `56e92c6c600f7600…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L39/asr_report.md`): câu: 39, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0; checked_at 2026-10-26T19:09:27Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 4 | 0.708 | Tổng phần thưởng chiết khấu cộng phần thưởng mỗi bước, nhân thêm gam-ma cho mỗi bước chậm hơn, với gam-ma nhỏ hơn 1. | Tổng phân thưởng chiếc khấu cộng phân thưởng mỗi bước nhìn thêm gamma cho mỗi bước chậm hơn với gamma nhỏ hơn 1. | “phần” → nghe thành “phân”; “chiết” → nghe thành “chiếc”; “phần” → nghe thành “phân”; “nhân” → nghe thành “nhìn”; “gam ma” → nghe thành “gamma”; “gam ma” → nghe thành “gamma” | — | phần, chiết, phần, nhân, gam, ma, gam, ma | lẫn thanh/vần: chiết→chiếc, phần→phân, nhân→nhìn; gam-ma chép “gamma” đúng — CẦN NGƯỜI NGHE xác nhận “chiết khấu” |

## Đã xem xét (`asr_reviewed`, 1 mục)

- “Tổng phần thưởng chiết khấu cộng phần thưởng mỗi bước, nhân thêm gam-ma cho mỗi bước chậm hơn, với gam-ma nhỏ hơn 1.” — lẫn thanh/vần: chiết→chiếc, phần→phân, nhân→nhìn; gam-ma chép “gamma” đúng — CẦN NGƯỜI NGHE xác nhận “chiết khấu”

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
