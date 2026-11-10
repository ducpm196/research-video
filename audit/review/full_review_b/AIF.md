# AIF — đã đọc 15/15 bài

Đọc toàn bộ `show`, `say`, `checks`, quiz và đáp án của từng bài (2026-11-08). Khoá AIF không có tệp mẫu `audit/aif/src/` nên không cần đồng bộ mẫu.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | AIMA 4e ch. 2 (PEAS, tính chất môi trường, cờ vua có đồng hồ là bán động) | — |
| L01 | đã sửa | quiz: SHOULD — “không lưu được” 10¹³ trạng thái là khẳng định tuyệt đối; đã có người duyệt hết trò 15 ô số bằng đĩa → “không lưu nổi trong bộ nhớ một máy thường” | R. Korf, P. Schultze, Large-Scale Parallel Breadth-First Search, AAAI-05 (2005) | lint: 0 FAIL, 0 WARN, 18 PASS · render: 64 khung (0 vấn đề) |
| L02 | đã sửa | quiz: MUST — bảng $h_2$ từng ô của trạng thái 1 6 2 / 3 _ 5 / 7 4 8 ghi 1, 2, 1, 2; đúng là 1, 3, 1, 1 (ô 6 ở (0,1) về (2,0) là 3 bước). Tổng 6 không đổi. Sửa màn hình + lời đọc, thêm `checks` tính từng ô | AIMA 4e §3.6 (định nghĩa khoảng cách Manhattan); tính lại bằng máy | lint: 0 FAIL, 0 WARN, 20 PASS · render: 63 khung (0 vấn đề) |
| L03 | đã sửa | sym: SHOULD — “A* dùng hàm trội không bao giờ mở nhiều nút hơn” bỏ điều kiện phá hoà (chính bài 2 cho thấy số nút đổi theo cách phá hoà) → thêm “trừ chênh lệch nhỏ do cách phá hoà”; sửa kèm `fix` của giáo án L03 | AIMA 4e §3.6.1 (lập luận trội dùng f(n) < C*, nút có f = C* tuỳ phá hoà) | lint: 0 FAIL, 0 WARN, 18 PASS · render: 63 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | AIMA 4e §4.1 (8 hậu, 14%/86%); Kirkpatrick và cộng sự, Science 220 (1983) | — |
| L05 | không phát hiện lỗi | — (vết MRV + kiểm tra tiến tự soát lại: hợp lệ) | AIMA 4e ch. 6 | — |
| L06 | đã sửa | pitfalls: MUST — “chỉ cần khoảng $b^{d/2}$ lá: với b = 35, d = 4 là 2449” tự mâu thuẫn ($35^2$ = 1225); ghi đúng công thức Knuth–Moore cho d chẵn $b^{d/2} + b^{d/2} - 1 = 35^2 + 35^2 - 1 = 2449$ (màn hình + lời đọc) | D. Knuth, R. Moore, Artificial Intelligence 6 (1975) | lint: 0 FAIL, 0 WARN, 19 PASS · render: 54 khung (0 vấn đề) |
| L07 | đã sửa | example: MUST — “máy tốt thua ngay lần đầu, tham lam không bao giờ quay lại nó” sai với chính mô phỏng (máy tốt THẮNG lần kéo đầu, bị kéo 3 lần, thắng 1) → viết đúng diễn biến, thêm `checks`; pitfalls: “một lần thua sớm” → “vài lần”. quiz: MUST — gốc N = 20 lượt nhưng ba nước con đã có 10 + 10 + 1 = 21 lượt (không thể) → N = 25 (gồm 4 lượt của nước khác), tính lại UCB1: 1,302 / 1,702 / 2,537, `checks` mới | Auer, Cesa-Bianchi, Fischer, Machine Learning 47 (2002) (UCB1); chạy lại `alg.ucb_bandit`, `alg.ucb1` | lint: 0 FAIL, 0 WARN, 21 PASS · render: 68 khung (0 vấn đề) |
| L08 | không phát hiện lỗi | — | AIMA 4e §7.3–7.4 | — |
| L09 | đã sửa | sym: SHOULD — “Luật Horn: luật có đúng một kết luận” là định nghĩa của mệnh đề xác định; Horn là TỐI ĐA một → “Luật Horn dạng xác định … (luật Horn nói chung có tối đa một kết luận)”, lời đọc thêm một vế | AIMA 4e §7.5.3 (definite clause vs Horn clause) | lint: 0 FAIL, 0 WARN, 16 PASS · render: 60 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — (Sussman: 5 / 7 / 3 bước tự đếm lại khớp) | Fikes–Nilsson (1971); AIMA 4e ch. 11 | — |
| L11 | đã sửa | example bước 4: SHOULD — “hai bằng chứng độc lập” sai: hai cuộc gọi chỉ độc lập CÓ ĐIỀU KIỆN khi biết chuông → “mỗi người tự nghe chuông và tự gọi”. Mục asr chờ tai người KHÔNG bị chạm (câu đã sửa không có trong `asr_reviewed`) | AIMA 4e §13.2 | lint: 0 FAIL, 0 WARN, 20 PASS · render: 64 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — (giá trị lưới 4×3 khớp AIMA hình 17.3) | AIMA 4e §17.1–17.2 | — |
| L13 | đã sửa | `source`/chú thích: SHOULD — gán “b ≈ 35, ván ≈ 80 nước” cho Shannon (1950) là sai nguồn (Shannon dùng ước lượng khác) → dẫn [AG16] “chess (b≈35, d≈80)”, câu đã trích ở `audit/aif/sources_L14.md`. Màn hình/lời đọc không đổi | Silver và cộng sự, Nature 529 (2016) [AG16] | lint: 0 FAIL, 0 WARN, 15 PASS · render: 57 khung (0 vấn đề) |
| L14 | đã sửa | pitfalls bài học sai 2: MUST — “cơ sở dữ liệu tàn cuộc là một phần của chiến thắng” trái nguồn: DB02 §8.3 “The endgame databases did not play a critical role in the matches against Kasparov” → thay bằng “cơ sở dữ liệu 700 nghìn ván của đại kiện tướng” (DB02 tóm tắt + §8.2), sổ khai cuộc “soạn tay” (§8.1). prereq: SHOULD — “khoảng $b^{d/2}$ … 2449” → công thức đúng như L06. Ghi câu trích mới vào `audit/aif/sources_L14.md` | DB02 (bản PDF oswego, đọc lại 2026-11-08 bằng pdftotext); arXiv:1712.01815 (đã kiểm “2016 TCEC world-champion Stockfish”) | lint: 0 FAIL, 0 WARN, 37 PASS · render: 126 khung (0 vấn đề) |

Tổng: 15/15 bài đã đọc, 9 bài sửa; 5 mục MUST (L02, L06, L07 ×2, L14), 6 mục SHOULD (L01, L03, L09, L11, L13, L14).

## Không sửa và vì sao
- L02: chứng minh “h chấp nhận được → A* tối ưu” không nhắc tính nhất quán. Theo AIMA 4e (BEST-FIRST-SEARCH mở lại nút khi gặp đường rẻ hơn) khẳng định đúng; `alg.puz_astar` dùng tập đóng nhưng h₁, h₂ đều nhất quán, nên số liệu không sai.
- L01: màn hình ghi “byte”, lời đọc nói “ô nhớ” (có từ trước, nghĩa gần nhau, không thêm từ ngoại vào lời đọc).
- L00: phòng hai ô “quan sát một phần” nhưng tác tử phản xạ “đủ” — khớp AIMA 2.2.1 (hợp lý theo thước đo đã cho); lỗi 3 đã nói chuyện đi qua đi lại.
- L04: giáo án viết “cực đại địa phương”, bài dùng h cần cực tiểu — hai cách nhìn tương đương, không sửa.
- L14: “chương trình vô địch giải máy cờ vua năm 2016” — đã kiểm trong bản arXiv:1712.01815 (“2016 TCEC world-champion Stockfish”), đúng. “trọng số chỉnh tay cho phần che chắn vua đều thấp quá” — DB02 §7.3 nói về trọng số “pawn shelter” (tốt che chắn vua): đúng ý, giữ.
- L13: 35⁸⁰ ≈ 10¹²³ (khác con số 10¹²⁰ của Shannon hay 10¹⁵⁴ của AIMA) — bài đã ghi rõ là ước lượng, không sửa.

## Việc cần người điều phối
- Lời đọc đổi ở L01, L02, L03, L06, L07, L09, L11, L14 → cần dựng lại tts/asr/build các bài này (tôi không chạy). L13 chỉ đổi `source`/chú thích.
- `rec()` AIF trong `audit/verify_plan_curricula.py` không đụng tới số đã đổi (L07 chỉ kiểm N = 13).

## Kết quả cuối
- `audit/aif/verify_aif.py`: TỔNG: 25 PASS · 0 FAIL
- `lv.py curriculum curriculum/aif.yaml`: curriculum: 15 bài, 15 đã có đặc tả, 0 lỗi
- `scan_ctrl.py`: không có lượt nào ở `lessons/aif` (8 lượt còn lại đều thuộc JVA, có từ trước).
