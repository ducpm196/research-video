# Lab IRS L13 — Dung lượng bảng nhúng & thống kê gợi ý video

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) `videos=<int> dim=<int> views_m=<f> users_m=<f> q=<f>` (`<int>` số nguyên, `<f>` số thực). Tính dung lượng MiB (`videos * dim * 4 / 1024^2`) của bảng số thực 32 bit (`4 byte`), lượt xem trung bình mỗi người (`views_m / users_m`) và hệ số bù `-ln(q)`.

In 1 dòng đúng nhãn (`<.1f>` 1 chữ số, `<.3f>` 3 chữ số thập phân): `emb_mib=<.1f> views_u=<.1f> log_corr=<.3f>`.
Chấm tự động: `bash labs/cham.sh IRS L13 duong_dan/bai_cua_ban.py`
