# Rà soát L25 — Bài 25 — Support Vector Machine: lề lớn nhất, hinge loss & kernel

- Đặc tả: `lessons/L25_svm.yaml`; nguồn: DC23#Ch5; tex#L406 (SVM: hinge loss + phạt L2, tối đa hoá lề); AUDIT T19 (lề = 2/‖w‖)
- Quy mô: 12 cảnh, 22 step, 12 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 20 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 7 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L25/build_report.json`): 60 khung, 351.867 s, built_at 2026-10-26T18:25:39Z, spec_sha256 `c4df5f9ea6f40779…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L25/asr_report.md`): câu: 60, thiếu audio: 0, gắn cờ: 7, chưa xem xét: 0; checked_at 2026-10-26T19:06:50Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 45 | 0.714 | Câu một tính độ rộng của lề. | Câu một tín độ rộng của Lê | “tính” → nghe thành “tín”; “lề” → nghe thành “lê” | — | lề | tính→tín, lề→Lê lẫn thanh; câu đã viết dài hơn một lần — cần người nghe |
| 9 | 0.8 | Hai đường điểm số bằng 1 và âm 1 cách ranh giới một chia độ dài w, nên lề bằng 2 chia độ dài w. | 2 đường điểm số bằng 1 và âm 1 cách tranh giới 1 chi độ dài vk, nên lề bằng 2 chi độ dài vk. | “ranh” → nghe thành “tranh”; “chia” → nghe thành “chi”; “w” → nghe thành “vk”; “chia” → nghe thành “chi”; “w” → nghe thành “vk” | kép, kép | ranh, chia, chia | w đọc tên chữ cái, ASR chép “vk”; ranh→tranh, chia→chi lẫn phụ âm (lặp lại ở nhiều câu tham khảo) — cần người nghe |
| 42 | 0.846 | Lỗi thứ ba, tự chế hàm nhân mà không kiểm ma trận Gram. | Lội thứ ba, tự chế hàm nhân mà không kiểm ma trận gam. | “lỗi” → nghe thành “lội”; “gram” → nghe thành “gam” | gram | — | Gram (tên riêng, ma trận Gram) ASR chép “gam”; lỗi→lội lẫn thanh |
| 34 | 0.882 | Lớn nhất bằng đúng 2 tại hướng 1, 0, khớp với lề và hướng của w. | lớn nhất bằng đúng 2 tại hướng 1, không, khớp với lệ và hướng của V két. | “lề” → nghe thành “lệ”; “kép” → nghe thành “két” | kép | lề | w đọc “vê kép” chép “V két”; lề→lệ lẫn thanh |
| 49 | 0.889 | Câu một, độ dài w bằng 5, nên lề bằng 2 chia 5, bằng 0 phẩy 4. | Câu 1, độ dài v kết bằng 5, nền lề bằng 2 chia 5, bằng 0,4. | “kép” → nghe thành “kết”; “nên” → nghe thành “nền” | kép | — | w đọc “vê kép” chép “v kết”; nên→nền lẫn thanh |
| 29 | 0.917 | Vì w là tổng các điểm hỗ trợ, điểm số chỉ cần các tích vô hướng, nên ta thay tất cả bằng hàm nhân. | Vì VCAP là tổng các điểm hỗ trợ, điểm số chỉ cần các tích vô hướng nên ta thấy tất cả bằng hàm nhân. | “w” → nghe thành “vcap”; “thay” → nghe thành “thấy” | v, kép | thay | w đọc tên chữ cái, ASR chép “VCAP” |
| 56 | 0.917 | Hàm nhân hợp lệ khi ma trận Gram nửa xác định dương. | Hàm nhân hợp lệ khi ma trận ram nửa xác định dương. | “gram” → nghe thành “ram” | gram | — | Gram (tên riêng) ASR chép “ram” |

## Đã xem xét (`asr_reviewed`, 7 mục)

- “Hai đường điểm số bằng 1 và âm 1 cách ranh giới một chia độ dài w, nên lề bằng 2 chia độ dài w.” — w đọc tên chữ cái, ASR chép “vk”; ranh→tranh, chia→chi lẫn phụ âm (lặp lại ở nhiều câu tham khảo) — cần người nghe
- “Lớn nhất bằng đúng 2 tại hướng 1, 0, khớp với lề và hướng của w.” — w đọc “vê kép” chép “V két”; lề→lệ lẫn thanh
- “Câu một, độ dài w bằng 5, nên lề bằng 2 chia 5, bằng 0 phẩy 4.” — w đọc “vê kép” chép “v kết”; nên→nền lẫn thanh
- “Vì w là tổng các điểm hỗ trợ, điểm số chỉ cần các tích vô hướng, nên ta thay tất cả bằng hàm nhân.” — w đọc tên chữ cái, ASR chép “VCAP”
- “Lỗi thứ ba, tự chế hàm nhân mà không kiểm ma trận Gram.” — Gram (tên riêng, ma trận Gram) ASR chép “gam”; lỗi→lội lẫn thanh
- “Hàm nhân hợp lệ khi ma trận Gram nửa xác định dương.” — Gram (tên riêng) ASR chép “ram”
- “Câu một tính độ rộng của lề.” — tính→tín, lề→Lê lẫn thanh; câu đã viết dài hơn một lần — cần người nghe

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
