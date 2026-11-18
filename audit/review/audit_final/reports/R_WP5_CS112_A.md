# S01 CS112 L00–L14: đã đọc 15/15 bài (đọc trọn YAML, chạy mã, làm 15/15 lab, xem khung hình)

Phạm vi: `lessons/cs112/L00..L14_*.yaml`, `labs/CS112/L00..L14`. Tiêu chí: BRIEF mẫu F + ADDENDUM (P8, P9). Người học: mất gốc toán và lập trình, đã qua Chặng 1 (Python cơ bản), bài phải tự đủ. Python: `.venv` 3.13.5; không bài nào cần numpy. Không sửa tệp nào trong repo ngoài báo cáo này.

## 0. Kết luận theo ngưỡng chốt

| Ngưỡng | Đòi hỏi | Kết quả | Đạt/không |
|---|---|---|---|
| MUST | 0 | 2 (L04:scale, L08:scale) | KHÔNG ĐẠT |
| P1 = 2 | ≥ 90% bài (≥ 14/15) | 11/15 = 73% (kém: L05, L07, L09, L14) | KHÔNG ĐẠT |
| P8 = 2 | 100% | 15/15 | ĐẠT |
| P9 = 2 | (không có ngưỡng) | 15/15 | — |
| Mất gốc | ĐỦ mọi bài | 15/15 ĐỦ (thấp nhất L05, L09 = 12) | — |

Cả hai lỗi MUST đều sửa được trong vài phút (đổi một cụm chữ ở tiêu đề, đổi một dòng mã). P1 cần giảng thêm 1–3 từ ở mỗi bài trong 4 bài kém.

Phát hiện ngoài ngưỡng, quan trọng: **video dựng sẵn đã cũ so với YAML.** `out/CS112/Lxx/Lxx.mp4`, `.srt`, `chapters.txt` ghi ngày 2/11–10/11; YAML ghi 14/11. Số chương trong `chapters.txt` ít hơn số cảnh YAML 2 cảnh ở mọi bài (ví dụ L00: 13 chương, 15 cảnh; không có `scale`, `practice`). Thư mục `frames/` đã được dựng lại 14/11 và có hình `scale`, `practice`, nên hình thì mới, còn tiếng và phụ đề thì chưa. Hệ quả: tôi không đối chiếu được lời đọc thật (SRT) với `say` của hai cảnh mới, và người học xem mp4 hiện có sẽ không nghe thấy phần quy mô và phần Tự làm. Cần build lại trước khi phát hành.

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L04 | MUST | `scale`, tiêu đề (dòng 192; hiện cả trên khung hình) | "…tràn ngăn xếp, và hàng đợi dời nghìn tỉ lần" | Bảng ngay dưới ghi 4 999 950 000 lần dời ở n = 100 000, tức gần 5 tỉ chứ không phải nghìn tỉ (10^12). Sai 200 lần. Tính lại `100000*99999//2 = 4999950000`. | Đổi thành "…hàng đợi dời hàng tỉ lần" | CONFIRMED |
| L08 | MUST | `scale`, step 1, mã `chuyen` (dòng 194–206) | `chuyen(n - 1, c, b, a, dem)` (lời gọi thứ hai) | Mã được giới thiệu là "chạy thật lời giải đệ quy". Theo mã giả ở `model` thì lời gọi thứ hai phải là `Hanoi(n-1, trung gian, nguồn, đích)` = `chuyen(n-1, b, a, c, dem)`. Tôi chạy mã đúng như trên màn hình với ghi lại nước đi, n = 3: nước thứ 3 đặt đĩa 2 lên đĩa 1 (bất hợp lệ), cuối cùng cọc A còn đĩa 3, cọc C đĩa 1. Số đếm 1023 và 1 048 575 vẫn đúng chỉ vì đếm không phụ thuộc cọc. Người học gõ mã này rồi in nước đi sẽ thấy vi phạm luật. | Sửa lời gọi thứ hai thành `chuyen(n - 1, b, a, c, dem)` | CONFIRMED (chạy mã) |
| L00 | SHOULD | `scale` step 1 (say + show) | "…hai vòng lặp của phần tự kiểm…" / mã `for j in range(1, i + 1)` | Phần tự kiểm đếm vòng `j` từ `n − y` đến `y` (kết quả (n²+8n+4)/4); mã trong `scale` là vòng `j` từ 1 đến `i`, tức vòng của bài "Đến lượt bạn" (kết quả n(n+3)/2). Cảnh `scale` lại đứng TRƯỚC `quiz`, nên bảng đã hiện sẵn công thức n(n+3)/2 trước khi bài hỏi. Số in ra (501500, 2003000) đúng. | Đổi lời thành "hai vòng lặp mẫu" hoặc dời `scale` sau `quiz`; hoặc đổi mã sang vòng `n − y..y` (n = 1000 cho 252 001) | CONFIRMED |
| L00 | SHOULD | `pitfalls` lỗi 3 (show + say) vs `sums` ⑤ | "tăng nhanh như lôgarit" | Cảnh `sums` nói "Tổng này tăng chậm như lôgarit". Hai cảnh nói ngược nhau về cùng một ý. Đúng là "tăng chậm, cùng cỡ lôgarit". | Đổi "nhanh" thành "chậm" | CONFIRMED |
| L07 | SHOULD | `scale` step 2–3 | "ba số in ra là số đỉnh, số lần nhìn, khoảng cách" | Mã in `c * c, *bfs(c)` = 4 số ("10000 10000 40000 198"). Bảng đặt "n + 2m = 49 600 mục" cạnh "lần nhìn = 40 000" mà không giải thích chênh lệch (mã đếm 4 hướng cho mỗi ô, kể cả hướng ra ngoài lưới, nên = 4n, không phải 2m = 39 600). | Sửa "bốn số in ra"; thêm một câu: lần nhìn đếm cả hướng ra ngoài lưới | CONFIRMED |
| L14 | SHOULD | `prune` vs `scale` | "chỉ đặt 16 lần" / "2057", "35 539" nút | `prune` đếm 16 lần đặt (không tính gốc); `scale` đếm số lần gọi hàm (tính cả gốc: bài 4 quân hậu cho 17). Hai quy ước đếm khác nhau cho cùng một đại lượng. Ngoài ra bảng so số NÚT (2 057) với số LÁ (8^8); số nút không cắt tỉa là (8^9−1)/7 = 19 173 961. | Thống nhất "số nút" (cả gốc), ghi chú khác biệt | CONFIRMED |
| L03 | SHOULD | `scale` step 1 | "…số lần dời khi chèn n số vào đầu mảng, bằng n nhân n trừ 1 chia 2" | Công thức dời n(n−1)/2 được đọc ra mà chưa giải thích: lần chèn thứ k dời k − 1 phần tử, cộng lại 1 + … + (n − 1) (bài 0). Một bước nhảy nhỏ. | Thêm một câu giải thích | CONFIRMED |
| L02 | SHOULD (nhỏ) | `pitfalls` lỗi 3 (show) | "Còn $50\log_2(n+100)$ chỉ thua $(\ln n)^2$ khi $n > 2^{104}$." | Câu mở bằng "Còn" không có vế trước trên màn hình (nó nằm trên bảng, vế trước ở lời đọc). Số 2^104 đúng (k = 105 là số mũ nguyên đầu tiên; n > 2^104,07). | Viết lại thành câu độc lập | CONFIRMED |
| Lab L08, L09, L11, L12 | SHOULD (nhẹ) | `practice` + `de.md` | "ra công thức đóng A(n) = 2^{n+1} − 3 …" | Đề ghi sẵn đáp số công thức đóng (L08, L09, L11), L12 ghi sẵn trường hợp và bậc. Phần giấy bút chỉ còn là "chứng minh đáp số đã cho"; chương trình chỉ kiểm. P8 vẫn đạt (có chương trình, số khác ví dụ, kết quả mong đợi). | Cân nhắc bỏ đáp số khỏi đề, giữ ở `mong_doi` | CONFIRMED |
| Mọi bài | SHOULD (lời đọc) | `say` có số viết nhóm bằng dấu cách | L14 "13 700", "35 539"; L08 "1 048 575"; L03 "499 500", "131 071"; L13 "499 500"; L06 "99 990" | 7 chỗ. TTS có thể đọc rời từng cụm ba chữ số hoặc đọc sai. L00 làm đúng (viết bằng chữ: "năm trăm linh một nghìn năm trăm"). Chưa kiểm được bằng tai (không chạy tts). | Viết số bằng chữ như L00 | PLAUSIBLE |
| L07 (nhẹ) | SHOULD | — | — | Không còn lỗi chuẩn xác nào khác. | | |
| L01, L02, L05, L06, L09, L10, L11, L12, L13 | — | | | không phát hiện lỗi chuẩn xác | | |

Ghi chú về sự kiện/nguồn: L05 "Adelson-Velsky và Landis đề xuất năm 1962" đúng; L13 thuật toán Euclid "từ thời Hy Lạp cổ đại" đúng; L12 phát biểu định lý thợ, mở rộng trường hợp 2 (CLRS 4th) đúng; L08 con số 585 tỉ năm đúng với 365,25 ngày/năm. Không đọc `sources*.md`.

## 2. Bảng độ sâu

Cột P8, P9 không cộng vào tổng. Phút = tổng `duration` trong `_frames.txt` (ước lượng; mp4 hiện có ngắn hơn vì cũ). sha16 là giá trị lúc đọc (cùng giá trị cho bản mẫu).

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Cần biết trước (dùng mà không giảng) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 42d43d5a710a98e5 | 13,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | hằng số; hàm, vòng lặp Python (Chặng 1) | `scale` mã khác vòng tự kiểm (xem §1) |
| L01 | 3439b6e9e4c0c2cd | 9,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | hàm; tập hợp | không đáng kể |
| L02 | 59af51f59ea1bd0d | 9,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | đa thức; hằng số | bảy hàm ở `hook` chỉ hiện, không đọc ra |
| L03 | 34e77a12a4f7d372 | 9,1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 13 | ĐỦ | 2 | 2 | lớp `Nut`, `None` (de.md cho sẵn) | P6: không nhắc list Python chính là mảng động, bộ nhớ đệm, hệ số tăng 1,5–2, co mảng |
| L04 | 66ad8bca63b6806a | 8,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | — | tiêu đề `scale` "nghìn tỉ" (MUST) |
| L05 | 28d9ef0c853d71db | 9,8 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát) | 2 | 2 | cây con; suy biến; cạnh (dùng ở định nghĩa chiều cao) | P1: "cây con" dùng ≥ 10 lần, chưa giảng; P2: chiều cao AVL Θ(log n) chỉ tuyên bố; xoay chỉ có 2 ví dụ + bảng, chưa nói con trỏ đổi thế nào; chưa có LL, RL chạy tay |
| L06 | 8df3dfa37dee4933 | 9,9 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 13 | ĐỦ | 2 | 2 | cận trên thô | P6: không nói dò tuyến tính tụ cụm, xoá phần tử, thay đổi m khi bảng đầy, chọn m |
| L07 | 4bb3b8fad48c99a8 | 8,5 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | chu trình; có hướng; vùng liên thông; láng giềng | P1: 3–4 thuật ngữ chưa giảng (xem §5) |
| L08 | 881bd20dd378fe8c | 8,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | công thức đóng (chỉ ở `practice`) | mã `scale` sai tham số (MUST) |
| L09 | 835d7754fe362199 | 7,1 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát) | 2 | 2 | quy đồng; chuyển vế; đa thức | P1 (3 từ đại số lớp dưới); P3: cảnh `equation` bước 3, tử số x của dòng 2 chạm khung dòng 1; lời đọc "x chia cho 1 trừ x nhân 1 trừ 2x" mơ hồ nhóm mẫu số |
| L10 | 6fd6873283077729 | 10,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | — | không đáng kể |
| L11 | 493bbd7531ba635d | 9,0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | — | không đáng kể |
| L12 | 01bd02df0778e1c1 | 11,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | đa thức | không đáng kể |
| L13 | 8c1253a620c409c0 | 8,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | 2 | 2 | trường hợp tốt nhất/tệ nhất (chưa định nghĩa) | không đáng kể |
| L14 | 19ceab47094092c6 | 7,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | hoán vị | P1: "hoán vị" xuất hiện từ cảnh `frame` ("bài liệt kê hoán vị") mà `hook` chỉ nói "xếp 3 bạn vào 3 ghế", chưa gắn tên |

## 3. Lab

Tôi làm như người học: đọc `de.md`, tự viết lời giải ở thư mục tạm, chấm bằng `bash labs/cham.sh CS112 Lxx <tệp>`, sau đó mới chạy `loi_giai.py` qua cùng lệnh. Tôi không mở `loi_giai.py` trước khi chấm. Chấm ở Git Bash, Python 3.13.5.

| Bài | Tự làm được | Thời gian (ước, người mới) | Kẹt ở đâu | `mong_doi` khớp màn hình |
|---|---|---|---|---|
| L00 | có | 10–15 phút (`pause` 240 s) | không; đề nhắc `range(i + 1, n + 1)` | khớp; ĐÚNG lần đầu |
| L01 | có | 10–15 phút (240 s) | không; đề gợi ý chạy lùi từ 2000 | khớp; ĐÚNG |
| L02 | có | 10–15 phút (240 s) | không; `lambda` được giải thích | khớp; ĐÚNG |
| L03 | có | 15–20 phút (300 s) | không; lớp `Nut` cho sẵn | khớp; ĐÚNG |
| L04 | có | 20–30 phút (360 s) | ba việc một lúc; đề viết gần như thuật toán; `pause` 6 phút là ngắn | khớp; ĐÚNG |
| L05 | có | 25–35 phút (480 s) | phải nhớ `them` đệ quy trả về `goc` | khớp; ĐÚNG |
| L06 | có | 25–35 phút (480 s) | `tim_bang` trả số âm khi không thấy (quy ước lạ nhưng đề mô tả đủ) | khớp; ĐÚNG |
| L07 | có | 25–35 phút (480 s) | "đánh dấu lúc xếp vào" phải theo đúng đề để ra thứ tự mong đợi | khớp; ĐÚNG |
| L08 | có | 10–15 phút | không (đáp số công thức đã ghi sẵn trong đề) | khớp; ĐÚNG |
| L09 | có | 15–20 phút | công thức truy hồi `c[n] − 5c[n−1] + 4c[n−2]` do đề cho; người mất gốc khó tự rút ra | khớp; ĐÚNG |
| L10 | có | 15–20 phút | không | khớp; ĐÚNG |
| L11 | có | 15–20 phút | `cong_thuc` do đề cho gần hết dòng mã | khớp; ĐÚNG |
| L12 | có | 15–20 phút | không; đáp án trường hợp đã ghi sẵn | khớp; ĐÚNG |
| L13 | có | 20–25 phút | đề mô tả từng bước, ít chỗ tự quyết | khớp; ĐÚNG |
| L14 | có | 20–30 phút | `da_dung` rồi `x.append` rồi `x.pop` đúng thứ tự; đề đủ | khớp; ĐÚNG |

Tổng: 15/15 lời giải tự viết chấm ĐÚNG ngay lần đầu; 15/15 `loi_giai.py` chấm ĐÚNG; 15/15 khối "Kết quả mong đợi" trên màn hình `practice` trùng từng dòng với `mong_doi.txt` (so bằng script, bỏ thẻ HTML). Điểm mạnh: mọi lab đều dùng số khác ví dụ trong bài và có kết quả mong đợi tự đối chiếu; thiên về "chương trình kiểm công thức". Điểm yếu nhẹ: các lab càng về sau càng chi tiết (L04–L07, L11, L13 gần như chép thuật toán), `pause` 240–600 s ngắn so với thời gian viết thật của người mới.

## 4. Người học kẹt ở đâu

- L00: không kẹt. (Chú ý `scale`: lời nói "vòng lặp của phần tự kiểm" nhưng mã là vòng của bài Đến lượt bạn.)
- L01: không kẹt.
- L02: không kẹt (bảy hàm ở `hook` chỉ nhìn được, không nghe được).
- L03: không kẹt.
- L04: không kẹt (tiêu đề `scale` "nghìn tỉ" gây hiểu sai).
- L05: `bst` step 1, "mọi khoá trong cây con trái nhỏ hơn nó": "cây con" chưa giảng. Và `rotate`: "Ta xoay trái tại 1, đưa 2 lên làm gốc" chỉ nói kết quả, chưa nói con trỏ nào đổi.
- L06: không kẹt.
- L07: `dfs` step 2, "kiểm tra đồ thị có chu trình không, đếm số vùng liên thông… chỉ dành cho đồ thị có hướng, không chu trình": ba thuật ngữ chưa giảng; sau đó lab yêu cầu "đếm vùng liên thông".
- L08: không kẹt cho đến `practice`: "ra công thức đóng" chưa giảng (suy được từ ví dụ).
- L09: `partial` step 1, "Quy đồng, ta cần x bằng A nhân 1 trừ x…": "quy đồng" chưa giảng; và `equation` step 3, "Theo quy tắc chuyển vế…".
- L10: không kẹt.
- L11: không kẹt.
- L12: không kẹt.
- L13: không kẹt.
- L14: `frame` step 1, "khung quay lui cho bài liệt kê hoán vị": "hoán vị" chưa được định nghĩa (hook chỉ có ví dụ ghế).

## 5. P1: chi tiết 4 bài chưa đạt (để sửa)

| Bài | Từ chưa giảng tại chỗ | Chỗ nên giảng |
|---|---|---|
| L05 | "cây con" (dùng ở `bst`, `avl` và nhiều bước sau); "suy biến" (`degenerate`); "cạnh", "tầng" (có định nghĩa ngầm qua hình/`height`) | `terms`: thêm "cây con = một nút cùng mọi nút nằm dưới nó"; `degenerate`: "suy biến = thành một hàng" |
| L07 | "chu trình", "có hướng", "vùng liên thông", "láng giềng" (ngầm hiểu) | `sym` hoặc `dfs` note: mỗi thuật ngữ một câu; "vùng liên thông" cần cho lab |
| L09 | "quy đồng", "chuyển vế", "đa thức" | ở `prereq` thêm một dòng nhắc; hoặc đổi lời đọc thành "đưa về cùng mẫu số", "chuyển số hạng sang vế bên kia" |
| L14 | "hoán vị" | `hook`: "mỗi cách xếp như vậy gọi là một hoán vị" |

## 6. Số đã tính lại / mã đã chạy

- Mã trên màn hình (cảnh `scale`, chạy y nguyên): 15/15 bài. Kết quả in ra khớp màn hình 15/15 (L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L12, L13, L14). Riêng L08: số đếm khớp nhưng nước đi sai luật (MUST ở §1).
- Lab: 15/15 tự viết ĐÚNG; 15/15 `loi_giai` ĐÚNG; 15/15 `mong_doi` = màn hình.
- Con số đọc/hiện được tính lại bằng Python, khoảng 90 giá trị; 89 khớp, 1 lệch (L04 tiêu đề "nghìn tỉ"). Một số điển hình: L00 (13 so sánh với n = 4, 501 500, 2 003 000, 500 001 500 000 → 500,0015 giây, H_1000 = 7,485, ln 1000 = 6,908, log₂ 10 = 3,32); L01 (252 001, 99,2%, n₀ = 13/8/6, 2,0001); L02 (thời gian ở 10⁹ bước/giây, 77 năm, 8,4·10¹⁵ năm, 2,6·10⁶⁵ năm, ngưỡng 23/59/80, n > 2¹⁰⁴, tỉ số 17,8 / 315,3 / 5599,7); L03 (1023, 131 071, ×128, ×10 010, 36 so với 15, 31 < 34); L05 (999/9, 1999/10, 19, 20); L06 (992, 99 990, 9 966, 1 660 964, đống [3,5,8,9,7,6] → [9,7,8,5,3,6]); L07 (198, 1998, 40 000, 4 000 000, 4 996 000); L08 (1023, 1 048 575, 17 phút, 12 ngày, 34 năm, 585 tỉ năm); L09 (…975 so với …976); L10 (11, 21, 1999, 1 999 999); L11 (5, 6, 7, 11, 327 680, 77 309 411 328); L12 (8415, 1 493 143, ×177, 960 = 64+128+256+512); L13 (499 500, 999, 12, 15); L14 (13 700, 986 410, ×72, 2 057, 35 539, 9/44/265, 31/147/853, 65/326/1957).
- Chưa kiểm được: lời đọc thật (SRT cũ), tai người (TTS), nguồn `sources*.md`.

## 7. Khung hình đã xem

Mỗi bài một ảnh ghép 6 khung (800×450 mỗi khung) từ `out/CS112/Lxx/frames/` (mở đầu/prereq, ký hiệu, ví dụ/hình cơ chế, quy mô, quiz, Tự làm hoặc tổng kết); thêm 3 khung đầy đủ độ phân giải.

| Bài | Khung (tên png) |
|---|---|
| L00 | 00011, 00033, 00055, 00077, 00099, 00121 |
| L01 | 00008, 00026, 00043, 00061, 00078, 00096 |
| L02 | 00008, 00025, 00042, 00059, 00076, 00093 |
| L03 | 00008, 00024, 00041, 00057, 00074, 00090 |
| L04 | 00008, 00025, 00042, 00060, 00077, 00094 |
| L05 | 00008, 00025, 00042, 00060, 00077, 00094; đầy đủ 00061 |
| L06 | 00008, 00025, 00042, 00060, 00077, 00094 |
| L07 | 00008, 00024, 00040, 00056, 00072, 00088 |
| L08 | 00007, 00023, 00038, 00053, 00069, 00084 |
| L09 | 00006, 00019, 00031, 00044, 00057, 00069; đầy đủ 00019 |
| L10 | 00008, 00026, 00044, 00062, 00080, 00098; đầy đủ 00044 |
| L11 | 00006, 00020, 00034, 00047, 00061, 00075 |
| L12 | 00009, 00027, 00045, 00064, 00082, 00100 |
| L13 | 00008, 00024, 00040, 00056, 00072, 00088 |
| L14 | 00007, 00022, 00037, 00052, 00067, 00082 |

Lỗi hiển thị:
- L09 `equation` (00019): tử số "x" của dòng thứ hai của khối công thức chạm đáy khung viền dòng đầu; đọc được nhưng chật.
- L05 hình xoay (LR): nhãn hệ số cân bằng cỡ 22 px (so với 30 px của số nút) nhỏ hơn các chữ khác; đọc được ở toàn màn hình, khó ở ảnh thu nhỏ.
- Mọi bài: nội dung chỉ chiếm nửa trên màn hình, nửa dưới trống (thiết kế chung, không gây khó đọc).
- Không thấy chữ tràn, đè hay bị cắt ở các khung khác.

## 8. Nhận xét chung

- Chất lượng toán và mã rất cao: đồng thời có phép thử độc lập (đường khác) ở hầu hết `verify`, quy mô số cụ thể ở cả 15 bài, lab có số khác ví dụ. Không tìm thấy lỗi toán hay đáp án sai ở 15 bài; chỉ có 1 tiêu đề sai đại lượng (L04) và 1 mã sai tham số (L08).
- Bài tự đủ về nội dung toán; không bài nào viện "như đã học ở khoá khác" cho khái niệm cốt lõi (các tham chiếu "bài 0, bài 4…" đều trong cùng khoá và đều ôn lại ở `prereq`).
- P1 là điểm yếu duy nhất đáng kể: 4 bài (L05, L07, L09, L14) còn 1–4 thuật ngữ dùng mà chưa giảng; sửa mỗi bài bằng 1–2 câu là đạt ngưỡng 14/15.
- Lab: người mới làm được hết, nhưng từ L08 trở đi đề ghi sẵn đáp số công thức đóng nên phần giấy bút không được chấm; chương trình chỉ xác nhận. Cân nhắc giấu đáp số trong đề.
- Lời đọc: chủ yếu đọc được; số lớn viết nhóm dấu cách (7 chỗ) cần viết bằng chữ như L00; công thức có mẫu số là tích đọc theo cụm "chia … nhân …" khó nhóm bằng tai (L09, L00 "n nhân n cộng 1, chia 2"), màn hình phải gánh.
- P6 (làm nghề thật) thấp hơn ở L03 (list Python = mảng động, bộ nhớ đệm) và L06 (xoá khỏi bảng băm, thay đổi m, tụ cụm).
- Việc cần làm trước khi phát hành: build lại mp4/srt/chapters cho 15 bài (cảnh `scale`, `practice` chưa có tiếng), rồi đọc lại SRT so `say`.
- `pause` của cảnh `practice` (240–600 s) ngắn hơn thời gian thực để tự viết lab (ước 10–35 phút).
