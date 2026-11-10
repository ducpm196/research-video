# PAR — đã đọc 14/14 bài

Đọc kiểm 2026-11-08 (đợt B). Đọc toàn bộ `show`/`say`/`checks`, quiz và đáp án của 14 bài `lessons/par/`, đối chiếu `audit/par/sources_L*.md` (câu trích nguyên văn đọc 2026-11-02/03) cho mọi sự kiện có thật. Khoá không có mẫu `audit/par/src/*.tpl.yaml` nên không cần đồng bộ mẫu. Khoá được viết cẩn thận: mọi số đều có `checks`, số minh hoạ đều ghi nhãn; chỉ phát hiện 3 điểm mức SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | [AM67] Amdahl 1967 (bản in lại IEEE SSCS News 2007), sources_L00.md | — |
| L01 | không phát hiện lỗi | — | [GU88] Gustafson, CACM 31(5) 1988, sources_L01.md | — |
| L02 | không phát hiện lỗi | — | Brent, JACM 21(2) 1974, Lemma 2 | — |
| L03 | đã sửa | quiz.2: SHOULD — “số nguyên đồng (0,1 đồng thành 10 xu)” tự mâu thuẫn (0,1 đồng không phải số nguyên đồng) → “số nguyên theo đơn vị nhỏ nhất” | PyTorch Reproducibility (docs.pytorch.org); số học tại chỗ | lint: 0 FAIL, 0 WARN, 31 PASS; render: 82 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | OpenMP 5.0 §2.9.2; Graham (cận lịch danh sách) | — |
| L05 | không phát hiện lỗi | — | cppreference `hardware_destructive_interference_size`; MESI | — |
| L06 | không phát hiện lỗi | — | GCC Auto-vectorization; Rust core::arch `__m256` | — |
| L07 | không phát hiện lỗi | — | [WWP08] Williams, Waterman, Patterson, Roofline (EECS-2008-134), sources_L07.md (đối chiếu hình: toạ độ log của mọi điểm khớp) | — |
| L08 | không phát hiện lỗi | — | NVIDIA CUDA C++ Best Practices Guide; [NI08] Nickolls và cs., ACM Queue 2008 | — |
| L09 | đã sửa | formula.2: SHOULD — bỏ sót điều kiện: mô hình “bộ nhớ nhanh giữ 3 khối A, B, C” là mô hình bộ nhớ đệm; trên thẻ đồ hoạ khối C thường cộng dồn trong thanh ghi, bộ nhớ chia sẻ chỉ giữ 2 khối A, B → thêm ghi chú “mô hình của bài” (màn hình + lời đọc), giữ nguyên số | NVIDIA CUDA C++ Best Practices Guide, mục Shared Memory in Matrix Multiplication (mã dùng `aTile`, `bTile` trong bộ nhớ chia sẻ, `sum` trong thanh ghi; truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 29 PASS; render: 91 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — | [PY09] Patarasuk & Yuan, JPDC 2009; [HO18] Sergeev & Del Balso 2018, sources_L10.md | — |
| L11 | không phát hiện lỗi | — | [GO17] Goyal và cs. 2017 (bảng 23,60 / 24,84 / 23,74%), sources_L11.md | — |
| L12 | không phát hiện lỗi | — | [AM67]; tình huống số minh hoạ (ghi nhãn) | — |
| L13 | đã sửa | timeline.0: SHOULD — lời đọc gộp hai sự kiện khác chủ thể (“256 thẻ trong một giờ… rồi tới 2018 việc này thành một thư viện mở”): công trình 1 giờ là của nhóm [GO17], thư viện mở là của một công ty khác [HO18] → tách hai câu, ghi “Từ 2017 tới 2018, một công ty khác đóng gói cách gộp theo vòng thành thư viện mã nguồn mở”; sửa kèm `focus` đủ 6 mục (E31) | [GO17], [HO18] theo sources_L13.md | lint: 0 FAIL, 0 WARN, 38 PASS; render: 129 khung (0 vấn đề) |

Tổng: 3 bài đã sửa, 0 MUST, 3 SHOULD. Không đổi số nào, không đổi `checks`, không cần sửa `rec()` hay bộ kiểm. Giáo án `curriculum/par.yaml` khớp bài sau sửa (L09 `example` “ba khối… 12 288 byte” đúng với mô hình của bài), không phải sửa.

## Không sửa và vì sao
- L08: “32 luồng của một nhóm mỗi lúc cùng chạy MỘT lệnh”. Từ thế hệ 2017 có lập lịch luồng độc lập, nhưng tài liệu CUDA vẫn mô tả một nhóm thực thi một lệnh chung mỗi lúc và phân kỳ vẫn chạy tuần tự từng nhánh; câu được dẫn đúng từ [NI08] năm 2008 → giữ.
- L05: “mỗi lõi có bộ nhớ đệm riêng” chỉ đúng với tầng gần lõi (tầng cuối thường dùng chung); đủ cho mô hình chia sẻ giả của bài → giữ.
- L06 quiz vòng A: “125 lệnh” cho $y_i = 2x_i + y_i$ — với lệnh nhân–cộng gộp là 125, nếu tách nhân và cộng là 250; tỉ lệ “ít hơn 8 lần” không đổi, quy ước đếm lệnh cộng ghi ở đầu bài → giữ.
- L09 lỗi 3 (khối 32 chỉ 1 khối luồng mỗi cụm 16 KB) phụ thuộc mô hình 3 khối; nay đã ghi rõ là mô hình của bài ở cảnh suy ra → giữ số.
- L13: ngày phát hành mã nguồn của thư viện năm 2017–2018 chỉ dựa trên bài báo 2/2018 [HO18]; chưa kiểm được ngày mở mã nguồn từ nguồn gốc (không có trong sources_L13.md) — bài đã viết mềm “từ 2017 tới 2018”.
- Các câu trích [AM67], [GU88], [WWP08], [NI08], [KR12], [GO17], [HO18], [PY09] không mở lại nguồn gốc lần này; đối chiếu theo câu trích nguyên văn đã ghi trong audit/par/sources_L*.md (đọc 2026-11-02).

## Kết quả cuối
- `audit/par/verify_par.py`: verify_par: 96/96 PASS
- `tools/lv.py curriculum curriculum/par.yaml`: curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi
- `audit/review/scan_ctrl.py`: hits: 8 (đều ở lessons/jva, khoá khác; 0 lượt ở PAR)
