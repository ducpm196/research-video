# S01 CS112 L15–L29: đã đọc 15/15 bài (người đọc độc lập, 2026-11-14)

Phạm vi: `lessons/cs112/L15..L29`, đọc trọn mọi `title/objectives/show/say/checks/quiz`; nhóm lab `labs/CS112/L15..L29`. Tiêu chí: BRIEF mẫu F + ADDENDUM (P8, P9). Không sửa tệp nào trong kho. Mọi bài đều là bài viết tay (không có bài sinh từ `.tpl.yaml` trong phạm vi).

## 0. Trạng thái video (không phải lỗi YAML, nhưng quyết định "học qua video")
- MP4/SRT/`chapters.txt` của cả 15 bài dựng ngày 2026-11-09/10; YAML sửa 2026-11-14. SRT của cả 15 bài KHÔNG có lời đọc cảnh `scale` (không có "ta xem điều gì xảy ra khi...") và cảnh `practice` (không có "bây giờ tới phần bạn tự làm"); `chapters.txt` không có chương "Tự làm" nào. Người xem MP4 hiện tại không thấy P8/P9. Thư mục `frames/` được chụp lại 2026-11-14 (có cảnh mới) nhưng `_frames.txt` là bản cũ (72–140 mục, lệch chỉ số với 95–126 png). Cần dựng lại (tts+render) trước khi chốt.

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L26 | MUST | `practice` step 1 (say) | "Để ý W tăng 1000 lần thì số ô bảng tăng đúng 1000 lần" | Màn hình cùng cảnh: W=14 → 90 ô, W=14000 → 84006 ô; 84006/90 = 933,4 (= 14001/15). Không phải "đúng 1000 lần". | Sửa lời đọc: "tăng gần một nghìn lần, khoảng 933 lần" (hoặc đổi W thành 15 và 15000 và sửa mong_doi). | CONFIRMED |
| L20 | SHOULD | `labs/CS112/L20/de.md` bước 3 | "thử mọi tập con ... (<số tập con đã thử> tap con)" | mong_doi là `1023 tap con` = 2^10−1 (bỏ tập rỗng); đề không nói bỏ. Làm theo chữ đề (kể cả rỗng) ra 1024 và bị chấm sai. | Thêm "tập con khác rỗng (kích thước 1..n)". | CONFIRMED (đã chạy) |
| L15 | SHOULD | `branch` step 1 + `practice` | "Mở 1→4: con 1→4→2: 28, 1→4→3: 50, 1→4→5: 36 ..." | Chỉ một nút con (1→2 = 35) có phép tính; 9 cận khác (53, 31, 28, 50, 36, 52...) được nêu không kèm ma trận con; quiz và lab chỉ làm cận gốc. Mục tiêu 3 "tính cận dưới của nút con" không có chỗ tự làm. Tôi tính lại bằng code: 35, 53, 25, 31 đúng. | Hiện ma trận con của 1→4 (rút gọn thêm 0) và 1→3 (có rút gọn thêm), thêm 1 dòng lab tính cận một nút con. | CONFIRMED |
| L18, L27, L28 | SHOULD | `L18:naive`, `L27:count` step 0, `L28:quiz` step 1–2 (say) | "2 nhân F của n cộng 1, trừ 1"; "T của n cộng 1 bằng 3 nhân T của n"; "2 mũ n cộng 1 và 2 mũ n" | Đọc thành tiếng, "F của n cộng 1" = F(n)+1, "2 mũ n cộng 1" = 2^n+1; màn hình là F(n+1), T(n+1), 2^(n+1) (L28: tỉ số "bằng 2" sai nếu hiểu 2^n+1). | Đọc "F của (n cộng một)", "hai mũ (n cộng một)". | CONFIRMED |
| L22 | SHOULD | `hook` (say + show) | "Thuật toán đơn hình, do Dantzig công bố năm 1947" | Tên riêng duy nhất trong lời đọc cả 15 bài (các bài khác nói "tên tác giả hiện trên màn hình"), dễ đọc sai; 1947 là năm đề xuất, công bố đầu tiên 1951 (chưa kiểm được nguồn trong `audit/cs112`). | "đề xuất năm 1947", bỏ tên khỏi lời đọc. | PLAUSIBLE |
| L29 | SHOULD | `stage1` step 1 + lab | "lấy 6 bit đầu của n ... 2112 = 100001 000000 (hệ hai)"; lab dùng `&`, `\|`, `>>` | Không bài nào trong phạm vi giảng hệ hai, bit, toán tử bit; lab dùng chúng ngay trong công thức đề. | Thêm 1 dòng prereq: n>>1 = n//2; n&1 = số dư khi chia 2; ví dụ đổi 2112 sang hệ hai. | CONFIRMED |
| L23 | SHOULD | `sym`, `cost` step 1 | "Máy vét cạn mọi hoán vị"; "C(n) = 2(n+1)H_n − 4n" | "hoán vị", "kỳ vọng" không giảng; công thức trung bình chỉ khẳng định (máy kiểm n ≤ 7), không suy ra (tôi kiểm n ≤ 7 và n = 1000 đúng 10 985,9). | Giảng 1 câu "hoán vị = một thứ tự"; thêm 2 dòng suy ra hoặc ghi rõ "bạn sẽ không tự suy ra ở đây". | CONFIRMED |
| L28 | SHOULD | `traps` step 0–3 | "thế ngược dừng ở i = n", "khe hở", "phần dư dương" | 10/19 bẫy dùng từ của bài 8–12 không ôn ở prereq (prereq chỉ ôn lôgarit và định lý thợ). | Mỗi bẫy kèm 1 vế "bài nào, nghĩa là gì" hoặc thêm hàng prereq. | CONFIRMED |
| L27 | SHOULD | `prereq`, `sym` | "tham lam", "ghi nhớ từ trên xuống", "vét cạn" | prereq chỉ ôn bài 19; ba thuật ngữ của bài 16, 18 dùng ngay ở `sym` và lab. | Thêm 3 hàng ôn. | CONFIRMED |
| L20 | SHOULD | `pitfalls` step 1 | "ở ví dụ khác, ô cuối có thể nhỏ hơn hẳn" | Cả ví dụ chính, quiz, lab đều có L[n] = max; không có số cụ thể cho lỗi "lấy ô cuối". | Thêm dãy 1, 2, 3, 0 → L = 1, 2, 3, 1. | CONFIRMED |
| L25 | SHOULD (nhỏ) | `scale` step 0 (say) | "Phần hợp và tìm chỉ tốn vài chục đến vài nghìn bước" | Bảng: 7, 547, 1 444 bước. | "từ vài bước tới vài nghìn bước". | CONFIRMED |
| L27, L20 | chưa kiểm được nguồn | `measure` (L27), `verify` (L20) | số đo 0,0464 ms / 2 138 ms / 251 ms / 30,7 ms, "424 KB / 12,7 KB" (L27); "300 dãy và 300 cặp xâu ngẫu nhiên" (L20) | Số đo trích từ "báo cáo thật" hoặc script kiểm không có trong tài liệu nguồn tôi được phép đọc; tỉ số 8,2 và 3,9 và các phép chia trên màn hình tính lại đúng. | — | — |
Các bài còn lại (L16, L17, L19, L21, L24, L29 ngoài mục trên): không phát hiện lỗi chuẩn xác. L29: số/ngày/phiên bản khớp `audit/cs112/sources_L29.md` (Java 5/10/19/40; 24/49; 2^26 cần 41 ô; 460/928 dòng; 19 606 028 vs 19 458 756; bpo-34561; gh-135551).

## 2. Bảng độ sâu
Phút = độ dài MP4 CŨ (không có `scale`/`practice`).
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước (dùng, không giảng) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L15 | c333d1ba1c2866af | 8,2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | Python: list lồng, zip, itertools.permutations (đề cho cú pháp) | cận nút con chỉ làm 1 nút; lab không có nút con |
| L16 | 6711c56b92f72b89 | 8,0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | Fraction, combinations (đề cho import); "đống" (bài 6) | chứng minh đổi chỗ chỉ phác (không nói dừng) |
| L17 | ded966af31eeb035 | 7,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | sorted(key=) với hàm khoá | — |
| L18 | 87429e255acd9ce6 | 7,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | đệ quy, dict ghi nhớ (bài 10) | đọc "F của n cộng 1" mơ hồ |
| L19 | fa39405243a2c299 | 8,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | đệ quy liệt kê ngoặc (lab) | đoạn biểu thức đánh số từ 0, ma trận từ 1 (có bẫy 4) |
| L20 | a32d2cc888a67587 | 9,0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | combinations | đề lab mơ hồ "tập rỗng"; thiếu ví dụ L[n] < max |
| L21 | 2c7c689790074f75 | 9,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | định thức (đề cho công thức) | — |
| L22 | fc29e4555eea86e0 | 9,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | Fraction; lập bảng đơn hình bằng list | tên Dantzig; lab nặng nhất (≈ 60 phút) |
| L23 | 42ee61b3049f468d | 12,1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 12 | 2 | 2 | ĐỦ (sát ngưỡng) | hoán vị, kỳ vọng, ln | công thức trung bình không suy ra |
| L24 | 7e9c0ac6e921ccc8 | 11,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | đống (ôn), dict, list tuple | — |
| L25 | 148e902c9534fa56 | 8,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | tự viết find/union (pseudo cho) | câu "vài chục" |
| L26 | 80db638ca47bb774 | 11,2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | bit_length, quy hoạch động túi 0/1 mảng 1 chiều (chỉ gợi ý) | lời đọc "đúng 1000 lần" (MUST); ít hình |
| L27 | 15a39b5d4f3278ad | 9,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | tham lam (bài 16), ghi nhớ (bài 18), vét cạn | prereq chỉ ôn bài 19; số đo không chạy lại được |
| L28 | 9c1524275c130855 | 11,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | định lý thợ, đệ quy có nhớ, math.log2 | 10 bẫy dùng từ bài 8–12 chưa ôn; "2 mũ n cộng 1" |
| L29 | 0d77dfcc1f475844 | 18,2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | hệ hai, `& \| >>`, gán lát cắt `s[n:n+2]=` | không giảng bit |
Hợp YAML: sha16 đọc đúng như đã ghi ở cột 2 (tệp không đổi trong lúc đọc).

## 3. Lab (tự viết từ `de.md`, trong thư mục tạm; chấm bằng `labs/cham.sh`)
| Bài | tự làm được | thời gian ước người học | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L15 | có | 20–30 ph | không | khớp |
| L16 | có | 20 ph | không | khớp |
| L17 | có | 20 ph | `key=khoa` nhận chỉ số (phải tự đổi) | khớp |
| L18 | có | 30 ph | không | khớp |
| L19 | có | 40 ph | không | khớp |
| L20 | phần (đúng chỉ khi đoán bỏ tập rỗng) | 40 ph | "1023 tap con" | khớp |
| L21 | có | 40 ph | không | khớp |
| L22 | có | 60 ph | quy tắc hòa trong đề phải đọc kỹ | khớp (dòng thừa do tôi thêm in debug) |
| L23 | có | 30 ph | không | khớp |
| L24 | có | 40 ph | không | khớp |
| L25 | có | 40 ph | không | khớp |
| L26 | có | 30 ph | túi 0/1 mảng 1 chiều chỉ có gợi ý | khớp |
| L27 | có | 45 ph | định nghĩa đếm "lời gọi" phải đọc đề | khớp |
| L28 | có | 30 ph | không | khớp |
| L29 | có | 30 ph | toán tử bit chưa được giảng | khớp |
Kết quả: 15/15 lời giải tự viết ra `ĐÚNG` (L22: 5 dòng đầu khớp, chỉ khác 2 dòng debug tôi thêm). `mong_doi.txt` khớp "Kết quả mong đợi" trên màn hình ở cả 15 bài (so từng dòng).

## 4. Người học kẹt ở đâu
- L15: `branch` step 1, "Mở 1→4: con 1→4→2: 28, 1→4→3: 50 ..." — không tự tính lại được các cận con.
- L16: không kẹt.
- L17: không kẹt.
- L18: không kẹt (nếu đã học đệ quy bài 10).
- L19: không kẹt; dễ lẫn chỉ số 0/1 ở `mcm` step 0.
- L20: không kẹt (lab: tập rỗng).
- L21: không kẹt.
- L22: `sym` step 0 "Biến cơ sở: các biến đang được giải ra theo các biến còn lại (đặt bằng 0)" — trừu tượng cho tới ví dụ.
- L23: `cost` step 1 "C(n) = 2(n + 1)H_n − 4n" — không có suy ra; "hoán vị" chưa giảng.
- L24: không kẹt.
- L25: không kẹt.
- L26: `npc` step 0 "Cook: bài toán gán đúng/sai cho các biến..." — chỉ kể, không định nghĩa (chấp nhận được như lịch sử).
- L27: `sym` step 0 "ghi nhớ từ trên xuống ... tham lam" — thuật ngữ bài 16, 18 chưa ôn.
- L28: `traps` step 0 "thế ngược dừng ở i = n, dùng T(0) đề không cho" — cần bài 8.
- L29: `stage1` step 1 "lấy 6 bit đầu của n ... (hệ hai)" — chưa học hệ hai.

## 5. Số đã tính lại / mã đã chạy
- Chạy lại toàn bộ `checks` của 15 bài bằng đúng không gian tên của `tools/lv.py` (không chạy build): 316/316 phép kiểm đúng (L15 27, L16 20, L17 13, L18 18, L19 24, L20 17, L21 21, L22 21, L23 30, L24 24, L25 16, L26 18, L27 13, L28 19, L29 35).
- Tính lại độc lập bằng mã tự viết (không dùng hàm của tác giả): ≈ 80 giá trị, khớp hết: L15 (cận gốc 25; 35/53/25/31; số nút đầy đủ 65, 13 700, 108 505 112, 3 554 627 472 076, 330 665 665 962 404 000; 19!; 10,5 năm); L16 (so sánh sắp trộn 21/8 728/1 536 555; 45/499 500/4 999 950 000; 2 568 chữ số); L17 (26/60/165/277/18 673 837; 18,3 phút; 36,6 năm); L18 (số lời gọi Fibonacci 4 giá trị; đổi tiền 1 869/229 970/3 053); L19 (Catalan 4 giá trị; (n³−n)/6); L21 (C(2n,n) 4 giá trị, 0,18 s/12,8 ngày/10^5 năm); L22 (số lần xoay ngẫu nhiên (2,2),(2,5),(4,16),(6,10); Klee–Minty 15/9, 31/15, 1 023/177); L23 (11 015/25 164/2 017 091, độ sâu 39; ⌈log2 n!⌉ 8 530/19 053/1 516 705; 10 985,9); L24 (4 967/50 000; 49 641/550 000; 998 001); L25 (197 và 739 chữ số); L26 (3,85 năm; 933,4); L27 (56/113/729/6 561/27 054, 30,6%); L28 (175 099; 10 458 256 051; 2 096 128; 11/21); L29 (minrun 63/33/40; 16/125/125 đoạn; ngăn xếp cũ [171,119,59,55] hỏng, bản sửa [404]; log2 2^20! = 19 458 756; lệch 0,76%).
- Mã minh hoạ trên màn hình đối chiếu luật thuật toán: L16 quy tắc túi phân số; L17 chọn kết thúc sớm; L18 ghi nhớ/lập bảng; L22 phép xoay; L23 phân hoạch Lomuto; L24 Dijkstra, Bellman–Ford; L25 find/union; L29 `mergeCollapse` cũ/sửa — đúng luật, không tìm thấy sai khác.
- Cảnh `symbol`: ký tự điều khiển (TAB, formfeed, `\t`, `\f` hỏng) trong chuỗi YAML đã parse: 0 vị trí. Chữ số trong `say`: không có nhóm cách, không ký hiệu toán; chỉ L22 có tên riêng (Dantzig), L28 có "2 mũ 2n".

## 6. Khung hình đã xem
Mỗi bài ≥ 6 khung từ `out/CS112/Lxx/frames/` (chọn đều theo chỉ số: hook, công thức/ví dụ, scale, pitfalls, quiz, tổng kết; tôi ghép 6 khung vào 1 ảnh tạm trong scratchpad), L15 thêm `sheet_15_19_22_36.png` (4 khung cũ). Lỗi hiển thị: không thấy chữ tràn/đè/cắt ở 15 bài; chữ trong sơ đồ cây của L15 và L27 nhỏ nhưng đọc được ở khung đủ cỡ; tờ sheet cũ L15 là bản cũ (không có ma trận ở cảnh `reduce`).

## 7. Ngưỡng chốt
- MUST 0: KHÔNG đạt — 1 lỗi (L26:practice step 1).
- P1 = 2 ở ≥ 90% bài: KHÔNG đạt — 11/15 bài (73%); P1 = 1: L23, L27, L28, L29.
- P8 = 2 ở 100% bài: ĐẠT — 15/15 (có việc cụ thể + kết quả mong đợi đối chiếu được; đã chạy 15/15).
- P9 = 2: 15/15.

## 8. Nhận xét chung
- Độ chuẩn xác rất cao: 316/316 `checks` và ≈ 80 số tự tính lại đều đúng; lỗi duy nhất là một câu lời đọc ở L26.
- Cả 15 bài có cảnh `scale` với 2–5 mức quy mô + đánh đổi, và `practice` với đề, số khác ví dụ, kết quả mong đợi; lab chấm được bằng một lệnh.
- Khoảng trống P1 tập trung ở bài tổng hợp (L27, L28, L29) và L23: từ vựng của bài trước chưa ôn, bit/hệ hai (L29), hoán vị/kỳ vọng (L23).
- L15 là bài duy nhất mà một bước cốt lõi (cận nút con) chỉ có 1 ví dụ làm tay, lab không luyện.
- Hai sai khác nhỏ giữa lời đọc và chữ trên màn hình: "n cộng 1" mơ hồ (L18, L27, L28) và "đúng 1000 lần" (L26).
- Video MP4/SRT hiện có chưa chứa cảnh `scale` và `practice` của cả 15 bài; `_frames.txt` lệch với `frames/`.
