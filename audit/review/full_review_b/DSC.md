# DSC — đã đọc 16/16 bài

Đọc từng bài từ đầu đến cuối (mọi cảnh, `show`/`say`/`checks`, quiz, đáp án; chữ trong hình SVG). Tính lại tay các con số chính
(tương quan, phương sai, tứ phân vị, cỡ mẫu A/B, Wilson/PPV, VIF, khoảng tin cậy). Bài L15 đối chiếu `audit/dsc/sources_L15.md`,
mở lại arXiv cs/0610105 và bảng 9 của [TJ09].

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00_quy_trinh | không phát hiện lỗi | — | — | — (không sửa) |
| L01_thang_do | không phát hiện lỗi | — | — | — (không sửa) |
| L02_du_lieu_gon_noi_bang | không phát hiện lỗi | — | — | — (không sửa) |
| L03_du_lieu_thieu | đã sửa | pitfalls.0: SHOULD — lời đọc “chỉ không gây lệch khi thiếu hoàn toàn ngẫu nhiên, như ví dụ mở đầu” khiến người nghe tưởng ví dụ mở đầu là thiếu hoàn toàn ngẫu nhiên; nay nói rõ mở đầu là thiếu không ngẫu nhiên, thêm “chắc chắn”. quiz.3: SHOULD — đáp án “thiếu không ngẫu nhiên” bỏ sót điều kiện: thêm “nếu bỏ khám chỉ phụ thuộc mức nặng đã ghi lần trước thì là thiếu ngẫu nhiên” (thêm `focus`). Giáo án L03 `fix` sửa theo | D. B. Rubin, Inference and Missing Data, Biometrika 63(3), 1976 (định nghĩa MCAR/MAR/MNAR); S. van Buuren, Flexible Imputation of Missing Data, 2nd ed. (2018), §1.2 | lint: 0 FAIL, 0 WARN, 21 PASS; render: 69 khung (0 vấn đề) |
| L04_thong_ke_ben_vung | không phát hiện lỗi | — | — | — (không sửa) |
| L05_truc_quan_trung_thuc | không phát hiện lỗi | — | — | — (không sửa; mẫu `sync_tpl` vẫn khớp) |
| L06_tuong_quan | không phát hiện lỗi | — | — | — (không sửa; mẫu `sync_tpl` vẫn khớp) |
| L07_simpson | không phát hiện lỗi | — (số Charig 1986 khớp: 81/87, 234/270, 192/263, 55/80, gộp 78%/83%) | — | — (không sửa) |
| L08_thu_nghiem_ab | không phát hiện lỗi | — (tính lại cỡ mẫu 10%→11%: 14 751 mỗi nhóm khớp công thức hai tỉ lệ) | — | — (không sửa) |
| L09_kiem_dinh_nhieu_lan | đã sửa | pitfalls.2: MUST — “với hàng triệu khách, khác biệt 0,01% cũng có ý nghĩa” sai số: ở tỉ lệ nền 10%, 1 triệu khách mỗi nhóm có sai số chuẩn của hiệu ≈ 0,043 điểm %, nên 0,01 điểm % chưa có ý nghĩa; thay bằng “10% so với 10,1%” (z ≈ 2,35 > 1,96), thêm `checks`. hook: SHOULD — chuyện kẹo dẻo xanh lá + “báo chí đưa tin” trình bày như sự thật; ghi “tình huống minh hoạ”, `source` ghi xuất xứ xkcd 882. recap: SHOULD — “1 − 0,95ᵐ” thiếu điều kiện độc lập và “ít nhất một” | Công thức sai số chuẩn hiệu hai tỉ lệ (như L08/L14 của khoá); R. Munroe, xkcd 882 “Significant” (2011) | lint: 0 FAIL, 0 WARN, 22 PASS; render: 64 khung (0 vấn đề) |
| L10_ro_ri_du_lieu | không phát hiện lỗi | — | — | — (không sửa) |
| L11_ti_le_nen | đã sửa | pitfalls.2: SHOULD — “ngưỡng 0,5 chỉ hợp lý khi hai loại nhầm tốn như nhau và hai lớp cân bằng” nêu sai điều kiện: ngưỡng tối ưu chỉ phụ thuộc chi phí khi xác suất mô hình đã đúng (hiệu chỉnh theo tỉ lệ nền nơi dùng); sửa thành “… và xác suất mô hình đưa ra khớp tỉ lệ nền nơi dùng” | C. Elkan, The Foundations of Cost-Sensitive Learning, IJCAI 2001, §2 (ngưỡng p* = c_FP/(c_FP + c_FN)) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 65 khung (0 vấn đề) |
| L12_dien_giai_hoi_quy | đã sửa | recap.0: SHOULD — “hệ số trên dữ liệu quan sát không phải nhân quả” tuyệt đối hoá (chính bài nói cần thí nghiệm hoặc thiết kế nhân quả); sửa “không tự nó chứng minh nhân quả”. Giáo án L12 `fix` sửa theo | A. Gelman, J. Hill, A. Vehtari, Regression and Other Stories (2020), ch. 18–21 (suy luận nhân quả từ hồi quy cần giả định) | lint: 0 FAIL, 0 WARN, 24 PASS; render: 62 khung (0 vấn đề) |
| L13_rieng_tu_dao_duc | đã sửa | pitfalls.2: SHOULD — dẫn “Nghị định 13/2023/NĐ-CP” như văn bản hiện hành; từ 01/01/2026 Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 có hiệu lực, thay Nghị định 13; sửa màn hình, lời đọc và `source` | Luật 91/2025/QH15 (luatvietnam.vn; vcci.com.vn “Luật Bảo vệ dữ liệu cá nhân… thay thế hoàn toàn Nghị định 13/2023”; hatinh.gov.vn — truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 19 PASS; render: 60 khung (0 vấn đề) |
| L14_tai_lap_truyen_dat | đã sửa | sym.0: SHOULD — “cùng hạt giống 42 luôn cho cùng dãy số” bỏ điều kiện phiên bản thư viện (NumPy không bảo đảm cùng dòng số giữa các phiên bản của `Generator`); thêm “cùng phiên bản thư viện” | NumPy documentation, “Random Generator — Compatibility policy” / NEP 19 (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 65 khung (0 vấn đề) |
| L15_hanh_trinh_netflix_prize | đã sửa | stage3.0: MUST — “nghiên cứu công bố tháng 11/2007” sai ngày: arXiv cs/0610105 v1 nộp 18/10/2006, v2 22/11/2007 (số 99%/68% trích từ v2); sửa “bản đầu 10/2006, bản sửa 11/2007; số theo bản sửa” trên màn hình và lời đọc; ghi vào `sources_L15.md`. Đã kiểm thêm: 0,00067 khớp bảng 9 [TJ09] (“Optimism of RMSE … 0.00067”, p = 800, RMSE = 0,8558); các số khác khớp `sources_L15.md` | arxiv.org/abs/cs/0610105 (lịch sử nộp, truy cập 2026-11-08); A. Töscher, M. Jahrer, R. M. Bell, The BigChaos Solution… (2009), bảng 9 | lint: 0 FAIL, 0 WARN, 37 PASS; render: 127 khung (0 vấn đề) |

Tổng: 7/16 bài đã sửa; 2 mục MUST, 9 mục SHOULD.

## Không sửa và vì sao
- L01 “năm 0 không phải ‘không có thời gian’”: dương lịch không có năm 0 (1 TCN → 1 SCN), nhưng ý bài (thang khoảng, số 0 quy ước) vẫn đúng; không đủ nặng để sửa.
- L07/L15 “chỉ chia ngẫu nhiên mới cắt được mọi ảnh hưởng của biến gây nhiễu”, L08 “mọi biến gây nhiễu chia đều hai nhóm”: chia ngẫu nhiên chỉ cân bằng *về kỳ vọng*. Đây là cách nói đơn giản hoá phổ biến cho người mới, ý chính vẫn đúng, nên giữ.
- L00 “Phần lớn thời gian thực tế nằm ở bước 2 và 3”: không kèm con số nên không trình bày số liệu thiếu nguồn.
- L15 bước 2 chặng 2 so 0,88 (AM12, không rõ đo trên tập nào) với 0,9514 (Cinematch trên tập công khai) để ra “≈ 7,5%”, và “≈ 2,6%” ở chặng 5: phép so sánh suy luận, đã ghi “≈”. Nguồn không nói rõ tập đo nên không đổi số.
- L15 trục thời gian vẫn gắn mốc “11/2007” cho chặng 3: đúng với bản sửa có các con số được dạy; phần chữ đã ghi rõ bản đầu 10/2006.

## Kết quả bộ kiểm cuối
- `audit/dsc/verify_dsc.py`: 30/30 PASS
- `tools/lv.py curriculum curriculum/dsc.yaml`: curriculum: 16 bài, 16 đã có đặc tả, 0 lỗi
- `audit/review/sync_tpl_from_lesson.py DSC`: tổng: 0 mẫu lệch bài (L05, L06 khớp; không bài có mẫu nào bị sửa)
- `audit/review/scan_ctrl.py`: 8 lượt, tất cả ở `lessons/jva/` (không thuộc DSC/DAN)

## Sửa bổ sung của người điều phối (kiểm chéo nguồn, 2026-11-08)
- L13 (SHOULD): bản sửa của tác tử ghi “Luật 91/2025/QH15 … thay Nghị định 13/2023/NĐ-CP”. Kiểm nguồn: Nghị định 13/2023 hết hiệu lực từ 01/01/2026, được thay bởi **Nghị định 356/2025/NĐ-CP** (ban hành 31/12/2025, hướng dẫn Luật 91/2025/QH15); luật không trực tiếp thay nghị định. Đã sửa ghi chú màn hình và dòng `source`. Nguồn: luatvietnam.vn trang Nghị định 356/2025 (“Kể từ ngày 01/01/2026, Nghị định 13/2023/NĐ-CP hết hiệu lực thi hành, thay thế bởi Nghị định 356/2025/NĐ-CP”), hatinh.gov.vn (Luật 91/2025/QH15 hiệu lực 1/1/2026); truy cập 2026-11-08, no revision given. lint: 0 FAIL, 0 WARN, 19 PASS; render: 60 khung (0 vấn đề).
