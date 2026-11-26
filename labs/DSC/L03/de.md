# Lab DSC L03 — Điền trung bình làm co giả phương sai mẫu

Đọc `stdin` `orig=<v1,v2,...> add=<n_missing>`. Tính phương sai mẫu (`n - 1`) của dãy gốc và dãy sau khi điền giá trị trung bình của gốc vào `n_missing` ô.

In 1 dòng: `orig_var=<.3f> mean_imputed_var=<.3f>`.
Chấm tự động: `bash labs/cham.sh DSC L03 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
