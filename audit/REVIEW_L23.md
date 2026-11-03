# Rà soát L23 — Bài 23 — Mạng perceptron nhiều lớp (MLP): hàm kích hoạt, khởi tạo, Batch normalization & hyperparameters

- Đặc tả: `lessons/L23_mlp.yaml`; nguồn: DC23#Ch4; NN#Activation-functions (sigmoid, tanh, ReLU, Leaky ReLU, “dead ReLU”), Weight-initialization (Xavier), Batch-normalization, Dropout, Hyperparameter (lấy mẫu theo thang log); AUDIT A5
- Quy mô: 14 cảnh, 24 step, 13 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 21 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 5 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L23/build_report.json`): 71 khung, 413.967 s, built_at 2026-10-26T18:23:33Z, spec_sha256 `736e04f1dd62af46…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L23/asr_report.md`): câu: 71, thiếu audio: 0, gắn cờ: 5, chưa xem xét: 0; checked_at 2026-10-26T19:06:29Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 17 | 0.786 | Hàm tanh nằm giữa âm 1 và 1, đạo hàm lớn nhất bằng 1. | Hàm tanh nằm giữa âm mục và mục, đạo hàm lớn nhất bằng mục. | “một” → nghe thành “mục”; “một” → nghe thành “mục”; “một” → nghe thành “mục” | — | một, một, một | số 1 đứng riêng đọc “một”, ASR chép “mục” (lỗi lặp lại của ASR ở L13, L20); các từ khác khớp |
| 59 | 0.909 | Câu một, ReLU cho 0, 0 và 2 phẩy 5. | Câu 1. Rê lu cho không, không và 2,5. | “re” → nghe thành “rê” | re | — | ReLU đọc “Re-lu”, ASR chép “Rê lu” (probe 8/8; khoá chấm lỏng — PARTIAL) |
| 16 | 0.917 | Sigmoid có đạo hàm lớn nhất chỉ 0 phẩy 25. | Sitmoid có đạo hàm lớn nhất chỉ 0,25. | “sigmoid” → nghe thành “sitmoid” | moi | — | sigmoid đọc “xích-moi”, ASR chép “Sitmoid” (nút thắt sigmoid PARTIAL) |
| 7 | 0.921 | Mạng hai lớp tính lớp ẩn h bằng hàm kích hoạt f áp lên W một nhân x cộng b một, rồi lớp ra tính tổng có trọng số của h. | Mạng 2 lớp tính lớp ẩn hát bằng hàm kích hoạt F-UP lên về đúc 1 nhân ít cộng B1, rồi lớp ra tính tổng có trọng số của hát. | “áp” → nghe thành “up”; “w” → nghe thành “về đúc” | w | — | tên chữ cái h→hát, W→về đúc, x→ít, f áp→F-UP; nội dung còn lại khớp |
| 20 | 0.957 | Vì lượt lùi nhân các đạo hàm với nhau, qua 10 lớp sigmoid, gradient bị nhân 10 lần một số không quá 0 phẩy 25, còn khoảng một phần triệu. | Vì lượt lùi nhân các đạo hàm với nhau, qua 10 lớp sitmoid, Gradian bị nhân 10 lần một số không quá 0,25, còn khoảng một phần triệu. | “xích moi” → nghe thành “sitmoid” | xích, moi | — | xích-moi→sitmoid (nút thắt sigmoid PARTIAL); câu dài, các số khớp |

## Đã xem xét (`asr_reviewed`, 5 mục)

- “Hàm tanh nằm giữa âm 1 và 1, đạo hàm lớn nhất bằng 1.” — số 1 đứng riêng đọc “một”, ASR chép “mục” (lỗi lặp lại của ASR ở L13, L20); các từ khác khớp
- “Câu một, ReLU cho 0, 0 và 2 phẩy 5.” — ReLU đọc “Re-lu”, ASR chép “Rê lu” (probe 8/8; khoá chấm lỏng — PARTIAL)
- “Sigmoid có đạo hàm lớn nhất chỉ 0 phẩy 25.” — sigmoid đọc “xích-moi”, ASR chép “Sitmoid” (nút thắt sigmoid PARTIAL)
- “Mạng hai lớp tính lớp ẩn h bằng hàm kích hoạt f áp lên W một nhân x cộng b một, rồi lớp ra tính tổng có trọng số của h.” — tên chữ cái h→hát, W→về đúc, x→ít, f áp→F-UP; nội dung còn lại khớp
- “Vì lượt lùi nhân các đạo hàm với nhau, qua 10 lớp sigmoid, gradient bị nhân 10 lần một số không quá 0 phẩy 25, còn khoảng một phần triệu.” — xích-moi→sitmoid (nút thắt sigmoid PARTIAL); câu dài, các số khớp

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
