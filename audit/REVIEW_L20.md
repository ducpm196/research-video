# Rà soát L20 — Bài 20 — Logistic, Softmax & Cross-Entropy (vì sao không dùng MSE)

- Đặc tả: `lessons/L20_logistic_softmax_cross_entropy.yaml`; nguồn: tex#L136–L138 (MSE cho phân loại — sai lầm thường gặp), L344–L351 (sigmoid, BCE, softmax); NN#Softmax; AUDIT A5, A11
- Quy mô: 14 cảnh, 25 step, 19 check (Python, chạy trong lint)
- Lint (OBSERVED, lúc sinh file này): `lint: 0 FAIL, 0 WARN, 27 PASS` — gồm E29 (không nhắc nguồn người xem không có) và E31/E32 (focus theo câu)
- Focus theo câu: 8 step có `focus` (phần đang được nói tới có viền, phần khác mờ)
- Build (OBSERVED, `out/L20/build_report.json`): 74 khung, 443.833 s, built_at 2026-10-26T18:19:51Z, spec_sha256 `64539fa2a51779ad…`
  - spec hiện tại KHỚP với spec lúc build
- ASR (OBSERVED, `out/L20/asr_report.md`): câu: 74, thiếu audio: 0, gắn cờ: 14, chưa xem xét: 0; checked_at 2026-10-26T19:05:28Z

## Câu ASR gắn cờ

| khung | độ khớp | câu | nghe được | khác biệt | từ rủi ro | từ khác | đã xem xét |
|---|---|---|---|---|---|---|---|
| 0 | 0.769 | Chào bạn, hãy đoán xác suất thi đỗ từ số giờ ôn bài. | Chào bạn, hãy đoán sát xuất thi đổ từ số giờ ôn bay. | “xác” → nghe thành “sát”; “đỗ” → nghe thành “đổ”; “bài” → nghe thành “bay” | — | xác, đỗ, bài | ASR lẫn thanh/phụ âm đầu (xác→sát, đỗ→đổ, bài→bay); câu dài 13 từ, ngữ cảnh rõ — cần người nghe xác nhận (REVIEW_L20.md) |
| 63 | 0.778 | Câu một, sigmoid của 0 bằng một nửa. | Câu một, xích môi của không bằng một nữa. | “moi” → nghe thành “môi”; “nửa” → nghe thành “nữa” | moi | nửa | xích-moi→xích môi (nút thắt sigmoid PARTIAL); nửa→nữa lẫn thanh |
| 13 | 0.833 | Trong bài này, xích ma có ngoặc theo sau là hàm sigmoid, cùng chữ nhưng khác nghĩa. | Trong bài này, sít ma có hoặc theo sau là hàm sít moi, cùng chữ nhưng khác nghĩa. | “xích” → nghe thành “sít”; “ngoặc” → nghe thành “hoặc”; “xích” → nghe thành “sít” | xích, xích | ngoặc | xích→sít, xích-moi→sít moi: nút thắt sigmoid PARTIAL; ngoặc→hoặc lẫn phụ âm đầu |
| 27 | 0.857 | Gradient theo w là trung bình của sai lệch nhân vector đặc trưng, giống hệt dạng của hồi quy tuyến tính. | Gradian theo V-cap là trung bình của sai lệch nhân vector đặc trưng, giống hệt dạng của hội quy tuyến tính. | “kép” → nghe thành “cap”; “véc tơ” → nghe thành “vector”; “hồi” → nghe thành “hội” | kép | hồi | w đọc “vê kép”, ASR chép “V-cap” (tên chữ cái); véc tơ→vector đúng nghĩa |
| 69 | 0.857 | Gradient luôn có dạng xác suất dự đoán trừ đi nhãn thật. | Gradient luôn có dạng xác xuất dự đoán trừ điên nạn thật. | “đi nhãn” → nghe thành “điên nạn” | đi | — | “trừ đi nhãn” bị chép “trừ điên nạn” — lẫn thanh/phụ âm; câu đã viết lại một lần — CẦN NGƯỜI NGHE xác nhận |
| 8 | 0.872 | Ký hiệu xích ma của z là hàm sigmoid, bằng 1 chia cho 1 cộng e mũ âm z. | Ký hiệu sigma của z là hàm sigmoid bằng một chia cho một cọng e mũ âm z. | “xích ma” → nghe thành “sigma”; “cộng” → nghe thành “cọng” | xích | — | ASR chép “xích ma” thành “sigma” — cùng nghĩa, đọc đúng |
| 4 | 0.895 | Hôm nay ta học hàm sigmoid, hàm sai số entropy chéo, và hàm softmax cho nhiều lớp. | Hôm nay ta học hàm xích môi, hàm sai số entropy chéo và hàm sóp mách cho nhiều lớp. | “moi” → nghe thành “môi”; “mác” → nghe thành “mách” | moi, mác | — | sigmoid đọc “xích-moi” (probe 6/8, nút thắt PARTIAL), softmax “sóp-mác” (3/8, OPEN) — giữ tên ở câu giới thiệu, các câu khác nói “hàm chuẩn hoá mũ” |
| 5 | 0.9 | Nhắc lại bài 12, e mũ z luôn dương, và đạo hàm của lôgarit u là 1 chia u. | Nhắc lại bài 12, E mũ giác luân dương và đạo hàm của Logaric u là một chia u. | “luôn” → nghe thành “luân”; “lôgarit” → nghe thành “logaric” | lôgarit | luôn | “lôgarit” chính tả SGK, ASR chép “Logaric” (đã ghi ở L12); luôn→luân là lẫn vần |
| 37 | 0.904 | Hàm softmax, tức hàm chuẩn hoá mũ, lấy e mũ mỗi điểm rồi chia cho tổng, nên mọi xác suất dương và cộng lại bằng 1, đúng một phân phối phân loại như bài 13. | Hàm sắp mắc, tức hàm chuẩn hóa mũ, lấy e mũ mỗi điểm rồi chi cho tổng, nên mọi xác xuất dương và cộng lại bằng mục, đúng một phân phối phân loại như bài 13. | “softmax” → nghe thành “sắp mắc”; “chia” → nghe thành “chi”; “một” → nghe thành “mục” | sóp, mác | chia | softmax “sóp-mác” → “sắp mắc” (nút thắt OPEN 3/8); câu này là câu ĐỊNH NGHĨA nên giữ tên, nói kèm “tức hàm chuẩn hoá mũ” |
| 25 | 0.917 | Đạo hàm theo dự đoán nhân với đạo hàm của sigmoid. | Đạo Hàm theo dự đoán nhân với đạo Hàm của Xích Môi. | “moi” → nghe thành “môi” | moi | — | xích-moi→Xích Môi: lẫn thanh cuối (nút thắt sigmoid PARTIAL) |
| 70 | 0.917 | Không dùng sai số bình phương cho phân loại, và nhớ rằng tính lồi chỉ đúng với mô hình tuyến tính theo w. | Không dùng sai số bình phương cho phân loại và nhớ rằng tính lội chỉ đúng với mô hình tuyến tính theo v kết. | “lồi” → nghe thành “lội”; “kép” → nghe thành “kết” | kép | lồi | w đọc “vê kép” chép “v kết”; lồi→lội lẫn thanh — cần người nghe |
| 14 | 0.923 | Mô hình logistic tính điểm số z giống bài 18, rồi đưa qua hàm sigmoid để được xác suất thuộc lớp 1. | Mô hình Logistic tính điểm số giác giống bài 18, rồi đưa qua hàm sít Moi để được xác xuất thục lớp 1. | “xích” → nghe thành “sít”; “thuộc” → nghe thành “thục” | xích | — | xích-moi→sít Moi (nút thắt sigmoid PARTIAL); z đọc “dét” chép “giác” (tên chữ cái) |
| 31 | 0.929 | Với sai số bình phương, đạo hàm có thêm thừa số của sigmoid gần bằng 0, nên chỉ còn âm 0 phẩy 013, gần như đứng yên. | Với sai số bình phương, đạo hàm có thêm thừa số của xích môi gần bằng 0 nên chỉ còn âm 0.013 gần như đứng yên. | “moi” → nghe thành “môi”; “không phẩy” → nghe thành “” | moi | không, phẩy | xích-moi→xích môi (nút thắt sigmoid PARTIAL); số đọc đúng |
| 34 | 0.933 | Nhưng cẩn thận, điều đó chỉ đúng khi mô hình tuyến tính theo w. | Nhưng cẩn thận, điều đó chỉ đúng khi mô hình tuyến tính theo v két. | “kép” → nghe thành “két” | kép | — | w đọc “vê kép”, ASR chép “v két” (tên chữ cái) |

## Đã xem xét (`asr_reviewed`, 14 mục)

- “Chào bạn, hãy đoán xác suất thi đỗ từ số giờ ôn bài.” — ASR lẫn thanh/phụ âm đầu (xác→sát, đỗ→đổ, bài→bay); câu dài 13 từ, ngữ cảnh rõ — cần người nghe xác nhận (REVIEW_L20.md)
- “Hôm nay ta học hàm sigmoid, hàm sai số entropy chéo, và hàm softmax cho nhiều lớp.” — sigmoid đọc “xích-moi” (probe 6/8, nút thắt PARTIAL), softmax “sóp-mác” (3/8, OPEN) — giữ tên ở câu giới thiệu, các câu khác nói “hàm chuẩn hoá mũ”
- “Nhắc lại bài 12, e mũ z luôn dương, và đạo hàm của lôgarit u là 1 chia u.” — “lôgarit” chính tả SGK, ASR chép “Logaric” (đã ghi ở L12); luôn→luân là lẫn vần
- “Ký hiệu xích ma của z là hàm sigmoid, bằng 1 chia cho 1 cộng e mũ âm z.” — ASR chép “xích ma” thành “sigma” — cùng nghĩa, đọc đúng
- “Trong bài này, xích ma có ngoặc theo sau là hàm sigmoid, cùng chữ nhưng khác nghĩa.” — xích→sít, xích-moi→sít moi: nút thắt sigmoid PARTIAL; ngoặc→hoặc lẫn phụ âm đầu
- “Mô hình logistic tính điểm số z giống bài 18, rồi đưa qua hàm sigmoid để được xác suất thuộc lớp 1.” — xích-moi→sít Moi (nút thắt sigmoid PARTIAL); z đọc “dét” chép “giác” (tên chữ cái)
- “Đạo hàm theo dự đoán nhân với đạo hàm của sigmoid.” — xích-moi→Xích Môi: lẫn thanh cuối (nút thắt sigmoid PARTIAL)
- “Gradient theo w là trung bình của sai lệch nhân vector đặc trưng, giống hệt dạng của hồi quy tuyến tính.” — w đọc “vê kép”, ASR chép “V-cap” (tên chữ cái); véc tơ→vector đúng nghĩa
- “Với sai số bình phương, đạo hàm có thêm thừa số của sigmoid gần bằng 0, nên chỉ còn âm 0 phẩy 013, gần như đứng yên.” — xích-moi→xích môi (nút thắt sigmoid PARTIAL); số đọc đúng
- “Nhưng cẩn thận, điều đó chỉ đúng khi mô hình tuyến tính theo w.” — w đọc “vê kép”, ASR chép “v két” (tên chữ cái)
- “Hàm softmax, tức hàm chuẩn hoá mũ, lấy e mũ mỗi điểm rồi chia cho tổng, nên mọi xác suất dương và cộng lại bằng 1, đúng một phân phối phân loại như bài 13.” — softmax “sóp-mác” → “sắp mắc” (nút thắt OPEN 3/8); câu này là câu ĐỊNH NGHĨA nên giữ tên, nói kèm “tức hàm chuẩn hoá mũ”
- “Câu một, sigmoid của 0 bằng một nửa.” — xích-moi→xích môi (nút thắt sigmoid PARTIAL); nửa→nữa lẫn thanh
- “Không dùng sai số bình phương cho phân loại, và nhớ rằng tính lồi chỉ đúng với mô hình tuyến tính theo w.” — w đọc “vê kép” chép “v kết”; lồi→lội lẫn thanh — cần người nghe
- “Gradient luôn có dạng xác suất dự đoán trừ đi nhãn thật.” — “trừ đi nhãn” bị chép “trừ điên nạn” — lẫn thanh/phụ âm; câu đã viết lại một lần — CẦN NGƯỜI NGHE xác nhận

## Còn NOT_VERIFIED

- Phát âm chỉ được kiểm bằng ASR (small + medium), chưa có người nghe.
- Hiệu quả sư phạm với người học thật.
- Khung hình: xem bằng contact sheet (khung cuối mỗi step), không xem từng giây video.
