# RLN — đã đọc 14/14 bài

Đọc kiểm đợt B, 2026-11-08. Đọc từng bài từ đầu đến cuối (mọi cảnh, `show`/`say`/`checks`, quiz, đáp án), đối chiếu `audit/rln/sources_L*.md`.
Khoá không có mẫu `audit/rln/src/*.tpl.yaml` → không cần đồng bộ mẫu. Tổng: 7 bài sửa, 0 MUST, 8 SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | pitfalls bước 4 + objectives: SHOULD — “cộng hằng số vào mọi phần thưởng làm đổi quyết định” chỉ đúng ở nhiệm vụ có lượt chơi kết thúc (ở nhiệm vụ liên tục chỉ cộng c/(1 − γ) cho mọi giá trị); thêm điều kiện trên màn hình và lời đọc | Sutton & Barto bản 2 (2018), bài tập 3.15–3.16 (đã trích ở sources_L00.md) | lint: 0 FAIL, 0 WARN, 31 PASS; render: 106 khung (0 vấn đề) |
| L01 | đã sửa | pitfalls bước 4: SHOULD — “giải thẳng chỉ hợp với vài trăm trạng thái” sai lệch (10 000 trạng thái = 800 triệu byte, 3,3·10¹¹ phép tính vẫn làm được); viết lại theo tỉ lệ tăng (gấp 10 trạng thái → bộ nhớ ×100, phép tính ×1000) và “hàng triệu trạng thái trở lên thì không giải thẳng nổi” | Sutton & Barto 2018 mục 4.1 (“straightforward, if tedious”); phép đếm khử Gauss | lint: 0 FAIL, 0 WARN, 27 PASS; render: 93 khung (0 vấn đề) |
| L02 | không phát hiện lỗi | — | sources_L02.md | — |
| L03 | đã sửa | example bước 4 + recap: SHOULD — “cận trên tin cậy … rồi tự thôi khám phá” sai: phần cộng tăng theo ln t nên mọi tay vẫn được thử, chỉ ngày càng thưa | Sutton & Barto 2018 mục 2.7 (tay ít ước lượng “will be selected with decreasing frequency over time”) | lint: 0 FAIL, 0 WARN, 28 PASS; render: 97 khung (0 vấn đề) |
| L04 | đã sửa | recap: SHOULD — “sửa từng bước nhanh hơn” nói tuyệt đối; sửa thành “cập nhật sớm, thường học nhanh hơn, chưa ai chứng minh là luôn nhanh hơn” (sources_L04.md tự ghi không được nói “luôn”); giáo án L04 `fix` sửa kèm | Sutton & Barto 2018 mục 6.2 (“no one has been able to prove mathematically …”) | lint: 0 FAIL, 0 WARN, 28 PASS; render: 96 khung (0 vấn đề) |
| L05 | không phát hiện lỗi | — | sources_L05.md | — |
| L06 | không phát hiện lỗi | — | sources_L06.md | — |
| L07 | không phát hiện lỗi | — | sources_L07.md | — |
| L08 | đã sửa | formula bước 1: SHOULD — “theo bài 7, đường cơ sở tốt nhất là V(s)” khẳng định quá mức (V(s) là lựa chọn tự nhiên, không phải tối ưu về phương sai); sửa thành “lựa chọn tự nhiên” | Sutton & Barto 2018 mục 13.4 (“One natural choice for the baseline is an estimate of the state value”) | lint: 0 FAIL, 0 WARN, 28 PASS; render: 78 khung (0 vấn đề) |
| L09 | không phát hiện lỗi | — | sources_L09.md (Bảng 1, Bảng 3 của bài báo năm 2017 khớp) | — |
| L10 | không phát hiện lỗi | — | sources_L10.md | — |
| L11 | đã sửa | hook (lời đọc): SHOULD — “bài viết năm 2020 của chính nhóm nghiên cứu” ngụ ý một nhóm làm cả hai thí nghiệm, sai (blog chỉ tổng hợp lại); concept: SHOULD — “bài báo năm 2016 xếp các trường hợp vào bốn nguồn” sai, mục 4 của bài báo nêu nhiều nguồn hơn (bài chọn 4); sửa tiêu đề, cột bảng, lời đọc | blog DeepMind 21/4/2020; Amodei và cộng sự, arXiv:1606.06565, mục 4 | lint: 0 FAIL, 0 WARN, 25 PASS; render: 85 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — | sources_L12.md (Bottou và cộng sự 2013) | — |
| L13 | đã sửa | stage5 bước 1: SHOULD — “(2018, 2019) … 51 và 52” ghép năm ngược: tác tử 2019 vượt 51 trò, tác tử 2018 vượt 52 trò; sửa thành “(một của năm 2019, một của năm 2018)” | Badia và cộng sự, arXiv:2003.13350, mục 1 (đã trích ở sources_L13.md) | lint: 0 FAIL, 0 WARN, 41 PASS; render: 122 khung (0 vấn đề) |

## Không sửa và vì sao
- L02 hook: “cần 66 vòng” thực chất là cận đủ (bài tự kiểm cho thấy đo thật 65), đã giải thích ngay ở cảnh tự kiểm → giữ.
- L03 lỗi 1: “Q = 1 lớn nhất mãi” đúng với phần thưởng 0/1 (Q tay đầu luôn > 0) → giữ.
- L09 sym nói lời “Biên cắt là biên cắt” — chỉ là văn phong, không báo.
- L13 lời đọc chặng 5 “đủ dài để nối một lỗi đầu lượt với điểm ở cuối lượt” là suy luận, không có số độ dài lượt chơi trò trượt tuyết trong nguồn; nói mềm, không có con số → giữ.

## Kết quả cuối
- `audit/rln/verify_rln.py`: verify_rln: 94/94 PASS
- `tools/lv.py curriculum curriculum/rln.yaml`: curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi
- `audit/review/scan_ctrl.py`: không có lượt nào ở lessons/rln (8 lượt còn lại thuộc lessons/jva, không phải khoá này)
