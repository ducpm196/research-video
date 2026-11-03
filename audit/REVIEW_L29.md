# Rà soát L29 — Bài 29 — Phân cụm: K-Means, phân cụm phân cấp & phân cụm phổ (ma trận Laplacian)

- Đặc tả: `lessons/L29_phan_cum.yaml`; nguồn: DC23#Ch5; AG25#Clustering; tex#L408 (K-Means: “Inertia (Tổng khoảng cách)”, lặp gán điểm và tính lại tâm); AUDIT A24, T17
- Quy mô: 12 cảnh, 20 step, 9 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 17 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 6 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L29/build_report.json`): 62 khung, 354.367 s, built_at 2026-10-26T18:29:39Z, spec_sha256 `634157fde32e0847…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L29/asr_report.md`): câu: 62, thiếu audio: 0, gắn cờ: 6, chưa xem xét: 0; checked_at 2026-10-26T19:08:06Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 57 | 0.75 | Phân cụm phổ dùng các vector riêng của ma trận Laplacian dựng từ đồ thị. | Phân Cụng phổ dùng các vector riêng của ma trận Lắp La Siang dựng từ Đô Thị. | “cụm” → nghe thành “cụng”; “laplacian” → nghe thành “lắp la siang”; “đồ” → nghe thành “đô” | xi, an | cụm | Laplacian đọc “Láp-la-xi-an”, ASR chép “Lắp La Siang” — gần đúng âm; cụm→cụng lẫn thanh |
| 26 | 0.812 | Ma trận Laplacian được định nghĩa bằng ma trận bậc trừ ma trận trọng số. | Ma trận lắp la xiang được định nghĩa bằng ma trận bật trừ ma trận trọng số. | “laplacian” → nghe thành “lắp la xiang”; “bậc” → nghe thành “bật” | láp, xi, an | bậc | Laplacian chép “lắp la xiang” — gần đúng âm; bậc→bật |
| 29 | 0.882 | Trị riêng 0 luôn có, vì mọi hàng của ma trận Laplacian cộng lại bằng 0. | Trị riêng không luôn có, vì mọi hàng của ma trận Lắp La Sian cộng lại bằng không. | “laplacian” → nghe thành “lắp la sian” | láp, xi, an | — | Laplacian chép “Lắp La Sian” — gần đúng âm |
| 39 | 0.889 | Hãy chạy nhiều lần và giữ J nhỏ nhất. | Hãy chạy nhiều lần và giữ duy nhỏ nhất. | “j” → nghe thành “duy” | j | — | J đọc tên chữ cái “gi”, ASR chép “duy” |
| 47 | 0.889 | Câu hai tính tổng bình phương khoảng cách J. | Câu 2 tính tổng bình phương khoảng cách gì? | “j” → nghe thành “gì” | j | — | J đọc tên chữ cái “gi”, ASR chép “gì” |
| 7 | 0.952 | Mục tiêu của K trung bình là J, tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó. | Mục tiêu của ca Trung Bình là gì? Tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó. | “j” → nghe thành “gì” | j | — | J đọc “gi”, ASR chép “gì” (đổi cả câu thành câu hỏi); K chép “ca” — tên chữ cái |

## Đã xem xét (`asr_reviewed`, 6 mục)

- “Hãy chạy nhiều lần và giữ J nhỏ nhất.” — J đọc tên chữ cái “gi”, ASR chép “duy”
- “Mục tiêu của K trung bình là J, tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó.” — J đọc “gi”, ASR chép “gì” (đổi cả câu thành câu hỏi); K chép “ca” — tên chữ cái
- “Phân cụm phổ dùng các vector riêng của ma trận Laplacian dựng từ đồ thị.” — Laplacian đọc “Láp-la-xi-an”, ASR chép “Lắp La Siang” — gần đúng âm; cụm→cụng lẫn thanh
- “Ma trận Laplacian được định nghĩa bằng ma trận bậc trừ ma trận trọng số.” — Laplacian chép “lắp la xiang” — gần đúng âm; bậc→bật
- “Trị riêng 0 luôn có, vì mọi hàng của ma trận Laplacian cộng lại bằng 0.” — Laplacian chép “Lắp La Sian” — gần đúng âm
- “Câu hai tính tổng bình phương khoảng cách J.” — J đọc tên chữ cái “gi”, ASR chép “gì”

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
