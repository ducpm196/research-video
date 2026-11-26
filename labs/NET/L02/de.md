# Lab NET L02 — Cổ chai thông lượng và tích băng thông–trễ BDP

Đọc `stdin` `links=<int,...> rtt_ms=<int>`. Tìm chặng cổ chai chậm nhất (Mbps), sau đó tính BDP bằng bit và byte cho `rtt_ms`.

In đúng 3 dòng: `bottleneck_mbps=<d>`, `bdp_bits=<d>`, `bdp_bytes=<d>`.
Chấm tự động: `bash labs/cham.sh NET L02 duong_dan/bai_cua_ban.py`

> Lưu ý: công thức BDP tổng quát là `băng thông × thời gian bay`; bài ví dụ lấy trễ 1 chiều 50 ms, còn lab này yêu cầu tính BDP theo cả vòng khứ hồi `rtt_ms`.
