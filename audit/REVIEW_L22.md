# Rà soát L22 — Bài 22 — Đồ thị tính toán & lan truyền ngược (backpropagation)

- Đặc tả: `lessons/L22_lan_truyen_nguoc.yaml`; nguồn: tex#L148–L150 (quên nhân với gradient đổ về), L353–L388 (4 cổng, ví dụ f = x·y + max(x, y)); VC24#Backpropagation; NN (gradient checking); AUDIT A12, A13
- Quy mô: 13 cảnh, 22 step, 14 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 22 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 5 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L22/build_report.json`): 65 khung, 364.633 s, built_at 2026-10-26T18:22:25Z, spec_sha256 `32612a0562cc4d39…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L22/asr_report.md`): câu: 65, thiếu audio: 0, gắn cờ: 3, chưa xem xét: 0; checked_at 2026-10-26T19:06:27Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 34 | 0.844 | Với vector, lớp tuyến tính z bằng W nhân x có ma trận Jacobian chính là W, theo bài 7. | Với Vector, lớp tuyến tính giác bằng Vduk nhân ít có ma trận gia cô biên chính là Vduk, theo bài bảy. | “véc tơ” → nghe thành “vector”; “w” → nghe thành “vduk”; “w” → nghe thành “vduk” | w, w | — | W đọc tên chữ cái, ASR chép “Vduk”; z→“giác”, Jacobian→“gia cô biên” là tên chữ cái/thuật ngữ — các từ khác khớp |
| 35 | 0.933 | Vì vậy gradient gửi xuống bằng W chuyển vị nhân gradient đổ về, một phép nhân ma trận. | Vì vậy Gradian gửi xuống bằng V đúc chuyển vị nhân Gradian đổ về, một phép nhân ma trận. | “w” → nghe thành “v đúc” | w | — | W đọc tên chữ cái, ASR chép “V đúc” — tên chữ cái |
| 30 | 0.95 | Cổng cộng gửi nguyên cho b, cổng nhân nhân với x, nên đạo hàm theo w bằng âm 1. | Cổng cộng gửi nguyên cho B, cổng nhân nhân với X nên đạo hàm theo viết kép bằng âm 1. | “v” → nghe thành “viết” | v | — | w đọc “vê kép”, ASR chép “viết kép” — tên chữ cái |

## Đã xem xét (`asr_reviewed`, 3 mục)

- “Với vector, lớp tuyến tính z bằng W nhân x có ma trận Jacobian chính là W, theo bài 7.” — W đọc tên chữ cái, ASR chép “Vduk”; z→“giác”, Jacobian→“gia cô biên” là tên chữ cái/thuật ngữ — các từ khác khớp
- “Vì vậy gradient gửi xuống bằng W chuyển vị nhân gradient đổ về, một phép nhân ma trận.” — W đọc tên chữ cái, ASR chép “V đúc” — tên chữ cái
- “Cổng cộng gửi nguyên cho b, cổng nhân nhân với x, nên đạo hàm theo w bằng âm 1.” — w đọc “vê kép”, ASR chép “viết kép” — tên chữ cái

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
