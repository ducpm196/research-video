# Lab DSC L10 — Rò rỉ dữ liệu: trung bình tập huấn luyện vs trộn tập kiểm tra

Đọc `stdin` `tr=<v1,v2,...> te=<v1,v2,...>`. Tính trung bình chuẩn chỉ trên tập huấn luyện so với trung bình bị rò rỉ khi trộn thêm tập kiểm tra.

In 1 dòng: `train_mean=<.1f> leaked_mean=<.1f>`.
Chấm tự động: `bash labs/cham.sh DSC L10 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
