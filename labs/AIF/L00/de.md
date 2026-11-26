# Lab AIF L00 — Tác tử phản xạ đa ô và không gian trạng thái

Đọc `stdin` `pos=<int> dirty=<0|1,...>`. Đếm tổng trạng thái khả dĩ `N * 2^N`, sau đó mô phỏng tác tử phản xạ dọn sạch mọi ô bụi đi sang phải vòng tròn và đếm số bước.

In 1 dòng: `total_states=<d> clean=<list> steps=<d>`.
Chấm tự động: `bash labs/cham.sh AIF L00 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
