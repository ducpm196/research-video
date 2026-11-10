# DAN — đã đọc 13/13 bài

Đọc từng bài từ đầu đến cuối (mọi cảnh, `show`/`say`/`checks`, quiz, đáp án; chữ trong hình SVG). Tính lại tay các con số chính
(trung bình có trọng số, phễu, trung bình trượt, MAE/MAPE, trung vị/MAD, khoảng Wilson, cây chỉ số). Bài L12 đối chiếu từng câu với
`audit/dan/sources_L12.md` (KO07, KO09, KO12, KO13, DE13, GU19, FA19).

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00_dinh_nghia_chi_so | không phát hiện lỗi | — | — | — (không sửa) |
| L01_trung_binh_cua_trung_binh | không phát hiện lỗi | — | — | — (không sửa) |
| L02_noi_nhan_dong | không phát hiện lỗi | — | — | — (không sửa) |
| L03_ham_cua_so | không phát hiện lỗi | — (khung mặc định RANGE gộp các dòng cùng ngày: đúng chuẩn SQL/SQLite) | — | — (không sửa) |
| L04_nhom_nguoi_dung | không phát hiện lỗi | — | — | — (không sửa) |
| L05_pheu_chuyen_doi | đã sửa | quiz.2: MUST — màn hình ghi “mức cải thiện tương đối $\frac{60}{50}$” (= 1,2, không phải 20%); sửa thành $\frac{60 - 50}{50} = 20\%$, khớp lời đọc và phần ôn ở prereq | Định nghĩa thay đổi tương đối (mới − cũ)/cũ, như prereq của chính bài | lint: 0 FAIL, 0 WARN, 20 PASS; render: 67 khung (0 vấn đề) |
| L06_chuoi_thoi_gian | không phát hiện lỗi | — | — | — (không sửa) |
| L07_du_bao_co_so | không phát hiện lỗi | — | — | — (không sửa) |
| L08_phan_khuc | không phát hiện lỗi | — | — | — (không sửa) |
| L09_bat_thuong | không phát hiện lỗi | — (hệ số 1,4826 và điểm bền vững khớp Iglewicz–Hoaglin) | — | — (không sửa) |
| L10_ti_le_mau_nho | không phát hiện lỗi | — (Wilson 2/2 = [0,342; 1] tính lại khớp) | — | — (không sửa) |
| L11_bang_dieu_khien | không phát hiện lỗi | — | — | — (không sửa) |
| L12_hanh_trinh_thu_nghiem_ab | đã sửa | stage5.2: SHOULD — “khoảng 80 người **tự nguyện** xem lại thử nghiệm của nhau” thêm chi tiết nguồn không ghi; [GU19] §7.2 chỉ ghi “Every week participants are paired with a random counterpart. Currently approximately 80 people participate.” → sửa “tham gia…, mỗi tuần ghép cặp ngẫu nhiên” | S. Gupta và cộng sự, Top Challenges from the first Practical Online Controlled Experiments Summit, SIGKDD Explorations 21(1), 2019, §7.2 (trích trong `audit/dan/sources_L12.md`) | lint: 0 FAIL, 0 WARN, 37 PASS; render: 127 khung (0 vấn đề) |

Tổng: 2/13 bài đã sửa; 1 mục MUST, 1 mục SHOULD.

## Không sửa và vì sao
- L09: với n = 8 và độ lệch chuẩn tổng thể, điểm z lớn nhất có thể là √7 ≈ 2,65, nên ngưỡng 3 *không bao giờ* báo được. Đây là điểm cộng thêm có thể dạy, không phải lỗi; bài đúng số.
- L12 cỡ mẫu theo công thức KO07 (n = (4rσ/Δ)²) dùng như tổng số người, đúng cách bài gốc dùng (“over 1.6 million users”); không đổi.
- L12 “0,6% là hơn 6 triệu đô la”: suy luận từ hai câu KO13 (1% > 10 triệu; 100 ms → 0,6%), nguồn không ghi trực tiếp nhưng phép tính đúng; giữ.
- L07 “Nhiều mô hình phức tạp không vượt được đường cơ sở đó”: không có số, hợp với Hyndman & Athanasopoulos (FPP3, §5.2); giữ.

## Kết quả bộ kiểm cuối
- `audit/dan/verify_dan.py`: verify_dan: 13/13 PASS
- `tools/lv.py curriculum curriculum/dan.yaml`: curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi
- DAN không có tệp mẫu `*.tpl.yaml`; `audit/review/scan_ctrl.py`: không có lượt ở `lessons/dan/`
