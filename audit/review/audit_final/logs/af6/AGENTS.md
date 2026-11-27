# Sổ tác tử lượt rà AF6 — mở 2026-11-27T15:42Z

Mốc git: `a3039c1f` (cây làm việc sạch lúc bắt đầu). Phạm vi lượt này: CHỈ rà soát + lập kế hoạch; không sửa bài, lab, video, công cụ, cổng.
Giới hạn: ≤ 4 tác tử cùng lúc. Tác tử bị ngắt vì hạn mức: tiếp tục bằng SendMessage tới đúng tên, không mở tác tử mới.
Mỗi tác tử TỰ GHI báo cáo ra tệp dưới đây (ghi dần sau từng bài). Hướng dẫn chung: `logs/af6/BRIEF_K.md`. Mẫu: `logs/af6/sample_k.tsv` (hạt giống 611, phân tầng).

| # | Tên | Việc | Tệp báo cáo | Trạng thái |
|---|---|---|---|---|
| 1 | af6-K1 | Đọc 8 bài lớp C chặng 6–8: WEB L07, SEC L04, CLD L02, EVT L03, OSY L02, SWF L09, SDP L01, CSA L00 | `logs/af6/sample_k/K1.md` | XONG ≈16:02Z — 7 lỗi bắt buộc sửa ở 6/8 bài; người điều phối kiểm lại 4 bằng lệnh, khớp |
| 2 | af6-K2 | Đọc 8 bài lớp C chặng 9–11: IRS L00, CVI L03, MLO L04, AIF L13, CS115 L24, ROB L04, BCH L08, HCI L11 | `logs/af6/sample_k/K2.md` | XONG ≈16:02Z — 6 lỗi ở 5/8 bài; kiểm lại 1 (`BCH L08`), khớp |
| 3 | af6-K3 | Đọc 8 bài lớp B viết lại: CPR L06, CPR L04, LNX L08, LNX L03, MLP L03, MLP L00, PRJ L01, PRJ L03 | `logs/af6/sample_k/K3.md` | XONG ≈16:08Z — 18 lỗi ở 8/8 bài; kiểm lại 1 (`LNX L08`), khớp |
| 4 | af6-K4 | Đọc 7 bài khoá mới + 1 bài lớp A đổi nhiều nhất: SPB L05, SPB L02, SPB L10, BEP L00, BEP L06, AIP L04, AIP L01, JV2 L09 | `logs/af6/sample_k/K4.md` | XONG ≈16:11Z — 17 lỗi ở 7/8 bài (`JV2 L09`: 0); kiểm lại 1 (`BEP L06`), khớp |

Việc người điều phối tự làm (không giao): các phép đo máy `p1`…`p9` trong `logs/af6/`, chạy lại bộ cổng `nhanh`, thử đột biến bộ chấm lab, xem khung hình/video mẫu, đối chiếu giáo án với đích "nền kỹ sư senior", khảo sát trang học hiện có, thiết kế web lộ trình, viết bộ ba tệp AF6.
| 5 | af6-planreview | Đọc phản biện `plan_AF6_20261127T1608Z.md`: mâu thuẫn nội bộ, số liệu sai so với kho, nghiệm thu không đạt được, phụ thuộc thiếu, lỗ hổng thiết kế web | `logs/af6/plan_review.md` | XONG ≈16:36Z — 10 cao, 8 vừa, 4 thấp; người điều phối kiểm lại PR-01, 02, 07, 15, 19 bằng lệnh (khớp), viết lại kế hoạch 16:40Z |
