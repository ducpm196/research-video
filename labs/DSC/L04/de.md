# Lab DSC L04 — Trung vị, IQR và hàng rào Tukey trước ngoại lai

Đọc `stdin` chuỗi `xs=<v1,v2,...>`. Sắp tăng mảng (cỡ chẵn `n`), tính trung bình và trung vị; dùng quy tắc tách đôi lấy `Q1 = median(xs[:n//2])`, `Q3 = median(xs[(n+1)//2:])`, `IQR = Q3 - Q1`, ngưỡng rào trên Tukey `Q3 + 1.5 * IQR` và kiểm ngoại lai `max(xs) > fence`.

In 1 dòng: `mean=<.1f> median=<.1f> fence=<.1f> outlier=<0|1>`.
Chấm tự động: `bash labs/cham.sh DSC L04 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
