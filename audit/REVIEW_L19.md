# Rà soát L19 — Bài 19 — Quá khớp, chính quy hoá L1/L2 (Lasso, Ridge) & cross-validation

- Đặc tả: `lessons/L19_qua_khop_chinh_quy_hoa.yaml`; nguồn: DC23#Ch3, Ch4; tex#L165–L166 (quá khớp), L406 (SVM có số hạng L2); ML24#Overfitting (đa thức bậc cao, tập huấn luyện/kiểm tra); NN#Dropout; AUDIT A9, T18
- Quy mô: 13 cảnh, 25 step, 13 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 21 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 4 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L19/build_report.json`): 72 khung, 409.567 s, built_at 2026-10-26T18:18:39Z, spec_sha256 `caeec6c333c63233…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L19/asr_report.md`): câu: 72, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0; checked_at 2026-10-26T19:05:26Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 14 | 0.941 | Vì vậy ta chia dữ liệu làm ba phần, phần huấn luyện để học w, phần kiểm định để chọn mô hình, và phần kiểm tra để chấm điểm cuối, chỉ dùng một lần. | Vì vậy ta chi giữ liệu làm 3 phần, phần huấn luyện để học vk, phần kiểm định để chọn mô hình và phần kiểm tra để chấm điểm cuối chỉ dùng một lần. | “chia” → nghe thành “chi”; “w” → nghe thành “vk” | v, kép | chia | tên chữ w (vê kép) → “vk” (tên chữ cái); “dữ liệu” → “giữ liệu” (cặp d/gi giọng Bắc) — INFERRED ASR |
| 44 | 0.96 | Phép thử, ta giải phương trình chuẩn mới, rồi giải theo một cách khác bằng thư viện, và hai cách cho cùng một w. | Phép thử, ta giải phương trình chuẩn mới, rồi giải theo một cách khác bằng thư viện và hai cách cho cùng một v kết. | “kép” → nghe thành “kết” | kép | — | tên chữ w (vê kép) → “v kết” (tên chữ cái); độ khớp 0,96 — INFERRED ASR |

## Đã xem xét (`asr_reviewed`, 2 mục)

- “Vì vậy ta chia dữ liệu làm ba phần, phần huấn luyện để học w, phần kiểm định để chọn mô hình, và phần kiểm tra để chấm điểm cuối, chỉ dùng một lần.” — tên chữ w (vê kép) → “vk” (tên chữ cái); “dữ liệu” → “giữ liệu” (cặp d/gi giọng Bắc) — INFERRED ASR
- “Phép thử, ta giải phương trình chuẩn mới, rồi giải theo một cách khác bằng thư viện, và hai cách cho cùng một w.” — tên chữ w (vê kép) → “v kết” (tên chữ cái); độ khớp 0,96 — INFERRED ASR

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
