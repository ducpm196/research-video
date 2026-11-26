# Lab IRS L12 — Hệ gợi ý hai tầng trong ngân sách trễ

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) `c1=<int> c2=<int> gen=<f> net=<f> rank=<f> shards=<int> p_slow=<f>` (`<int>` là số nguyên, `<f>` là số thực). Tính độ trễ phân vị 99 (`p99` = `gen + net + round(c * rank)`) trước/sau khi giảm ứng viên và xác suất gặp đuôi chậm `1 - (1 - p_slow)^shards`.

In 1 dòng đúng nhãn (`<d>` là số nguyên, `<.1f>` làm tròn 1 chữ số thập phân; giữ nguyên tên khoá cố định `tail8` kể cả khi `shards` khác 8): `p99_before=<d>ms p99_after=<d>ms tail8=<.1f>%`.
Chấm tự động: `bash labs/cham.sh IRS L12 duong_dan/bai_cua_ban.py`
