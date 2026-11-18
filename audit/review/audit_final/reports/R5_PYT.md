# R5 PYT (vòng 5, đọc độc lập bản dựng sau sửa, P1 chặt): 14/14 bài — ghi lại bởi người điều phối từ tin nhắn của reader (ab57fdca4d8760e92)

## 1. Tóm tắt (vòng 4b: P1=2 0/14 → vòng 5: 13/14 chắc+vừa)
MUST 0 (14/14). P1=2: 13/14 chắc+vừa (L09 = 1); tính cả yếu 6/14 (L04, L05, L07, L08, L10, L12). Tổng 10 mục chưa giảng (1 vừa, 9 yếu); không bài nào ≥ 3 mục. P8=2 14/14; P9=2 14/14; spec khớp 14/14; SRT khớp 14/14; lab 14/14 khớp mong_doi (L08 `pip install` cần mạng: chỉ đọc). Mất gốc ĐỦ 14/14. SHOULD 6. Mỗi bài có 2 câu TTS nhãn `edge?` (cache cũ không ghi nguồn). 169 khối mã chạy lại, 158 khớp, 11 lệch không phải lỗi bài (input không in lại chữ gõ; dạng traceback; số giây minh hoạ; 18,5 vs 18,3 MB; L07 dòng 8/5/2 chạy riêng khớp; thông báo rút gọn "…"; khối diff). >60 phép tính khớp, trừ số 41 ký tự L04.
Ngưỡng theo chuẩn chắc+vừa (MUST 0; P1=2 ≥ 90% bài; P8=2 100%): ĐẠT (13/14 = 93%) — chờ sửa mục vừa L09 để 14/14.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L04 | scale step 0 | `41 ký tự (ngoại suy) | ≈ 10 giờ` | quy tắc "gấp đôi mỗi ký tự"; đo 25 ký tự = 0,82 s ⇒ 0,82 × 2^16 = 53 700 s ≈ 14,9 giờ (dòng 31 ký tự ≈ 50 s đúng) | ghi "≈ 15 giờ" | CONFIRMED |
| L11 | example step 2 (khung 00058), scale step 3 (khung 00082) | hình đường, phân tán, "1 000 000 điểm" | hình không có số/đơn vị trên trục, trong khi bài dạy "đọc tiêu đề, đơn vị, trục trước" | thêm vạch và nhãn trục | CONFIRMED |
| L12 | quiz step 1 (đáp án câu 1) vs intuition, example | quiz `11 000 001 → 11 000`; SVG intuition `11 001 000`; bảng example step 2 và `test_bien` `12 000 000` | ba giá trị "ngay sau" khác nhau cho cùng ngưỡng 11 000 000; bộ ba quiz bắt 5/14 đột biến; chín ca bảng bắt 13/14; cần 11 001 000 để 14/14; phí = `tien // 1000` nên "ngay sau" cách 1 000 | quiz dùng 11 001 000 hoặc nói rõ bước 1 000 | CONFIRMED (mã) |
| L12 | example step 4 | `18 cách ... 4 cách ... 14 cách ... bắt 12 trong 14` | định nghĩa in ("đổi dấu so sánh, hoặc dịch một hằng số ±1") đếm theo nghĩa đen ra 17 mutant (3 dấu → `<=`/`>=` + 7 hằng × ±1: 4 tương đương, 13 sai, 7 ca bắt 11, 9 ca bắt 13); tái lập đúng 18/4/14/12/14 với định nghĩa ngầm (mỗi `<`/`>` đổi 2 cách; chỉ dịch 4 hằng 50000, 1100, 11000, 1000, bỏ `return 0`); kết luận (hai mutant sống sót cần 1 099 999 và 11 001 000) đúng | thêm một câu nêu đúng tập đột biến | CONFIRMED |
| L12 | example step 5 (khung 00075), sym step 1 (khung 00012), hook (khung 00000) | `Thêm hai ca 1 099 / 999 → 1 100`; `-q --` / `tb=short` | dòng xuống giữa số 1 099 999 và giữa cờ `--tb=short`; hook: chữ cuối cách thanh phụ đề ≈ 10 px | khoảng trắng không ngắt | CONFIRMED |
| L13 | scale step 0 (khung 00080) | `≈ 10 ms, ≈ 98 / KB` | 6/9 ô bảng ngắt dòng giữa số và đơn vị | khoảng trắng không ngắt | CONFIRMED |
P3=1 ở L12, L13 (ngắt dòng). Tái kiểm L12 bằng mã (pytest 9.2.0, Python 3.11): `..F....` và `1 failed, 6 passed` → `7 passed` khớp, `test_phi.py:12` đúng; phí 49 999→0, 50 000→1 100 (mã sai `<=` ra 0), 1 099 999 và 1 100 000→1 100 ("liền mạch"), 11 000 000 và 11 001 000→11 000, 12 000 000→11 000; đột biến theo định nghĩa ngầm 18/4/14/7 ca bắt 12/9 ca bắt 14; hai mutant sống `phi < 1099` và `phi > 11001` chết nhờ 1 099 999 và 11 001 000. Bài không sai phép tính; cần thống nhất giá trị "ngay sau" và nêu đúng tập đột biến.

## 3. Mục chưa giảng (10)
Vừa (SỬA BẮT BUỘC): L09 example step 1 `print((so_tien > 1000).sum())` ra 3 — bảng chỉ giảng mặt nạ làm chỉ số, không giảng "tổng đúng/sai = số đúng, True tính là 1" (A vừa; bảng có `a[a > 1000]`, không có `.sum()` trên mặt nạ). L10 `isna().sum()` dựa cùng ý (sửa ở L09 là đủ, nhắc một dòng ở L10).
Yếu: L00 prereq step 0 `print` trong `python -c "print('xin chao')"` (M); L00 scale step 1 `float(2 ** 53) + 1` (A); L01 sym step 3 `list(range(3))` (M); L01 scale step 1 `≈ 93 µs` (A); L02 scale step 2 `≈ 240 ms`, `≈ 2,0 s` (A; L04 mới chú); L03 pitfalls step 1 `gd.remove(x)` (A); L06 example step 10 `dang_dung, dinh = tracemalloc.get_traced_memory()` (B; gán hai biến, `dinh` không dùng); L11 example step 3, scale step 2 `ax.collections[0].get_offsets()`, `.get_array()` (A; bảng chỉ có `ax.patches`, `ax.lines`); L13 prereq, sym step 0 "tính nhanh bằng mã đã biên dịch" (B; L09 giảng, L13 không giảng lại).
Ghi chú: L10 formula step 7 `gd["so_tien"].isna().sum()` ra 1 (kẹt nhẹ); L13 practice step 2 việc "chép nguyên `cham()` từ de.md" nằm ngoài video; L08 lab cần mạng ở bước `pip install`.

## 4. Người học kẹt ở đâu
L09 example step 1 (kẹt thật: vì sao tổng đúng/sai là số lượng); L06 example step 10 (gán hai biến); L11 example step 3 (`ax.collections[0].get_offsets()`); L10 formula step 7 (nhẹ); L12 quiz câu 1 (ba giá trị "ngay sau") và số đột biến "18 cách" không tự đếm lại được; các bài khác không kẹt.
