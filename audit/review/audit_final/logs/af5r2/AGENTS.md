# Sổ tác tử lượt rà AF5 lần 2 (hoàn thiện kế hoạch) — mở 2026-11-23T01:00Z

Giới hạn: ≤ 4 tác tử chỉ đọc cùng lúc. Tác tử bị ngắt vì hạn mức: tiếp tục bằng SendMessage tới đúng tên, không mở tác tử mới.
Mỗi tác tử TỰ GHI báo cáo ra tệp nêu dưới đây trước khi trả lời (nhật ký tác vụ hay rỗng).

| # | Tên tác tử | Việc | Tệp báo cáo | Trạng thái |
|---|---|---|---|---|
| 1 | af5r2-edges | Đọc 24 cặp bài có cạnh tiên quyết liên khoá trỏ sang chặng sau; với từng cặp kết luận GIỮ (tiên quyết thật) hay HẠ (chỉ liên quan) kèm trích dẫn | `logs/af5r2/edges_report.md` | XONG 01:08Z — 25/25 HẠ (thêm cạnh 25 WEB:L14←DVO:L07 qua SendMessage); người điều phối kiểm lại 4 cạnh bằng grep, khớp |
| 2 | af5r2-planreview | Đọc phản biện `plan_AF5_20261123T0110Z.md`: tìm mâu thuẫn nội bộ, tiêu chí nghiệm thu không đạt được, phụ thuộc thiếu, số liệu sai so với kho | `logs/af5r2/plan_review.md` | XONG 01:40Z — 7 cao, 21 vừa, 18 thấp; người điều phối kiểm lại 9 phát hiện bằng lệnh (khớp), viết lại kế hoạch 02:00Z |

Việc người điều phối tự làm (không giao): mô phỏng dãy chặng (`stage_sim.py`, `stage_explicit.py`), chạy `audit_all` có vá tạm (`audit_all_patched.py`), đối chiếu JD, thiết kế `cham.sh` v2, viết bộ ba tệp.
