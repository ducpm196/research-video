# Lab BNK L10 — Sáu phản hồi lộn xộn

Sáu yêu cầu có mã thông điệp `M0 … M5`, yêu cầu `Mi` có nội dung `chuyen <(i+1)*100>` (`M0` → `chuyen 100`, …, `M5` → `chuyen 600`). Sáu phản hồi về theo thứ tự mã tương quan: `M3, M5, M0, M1, M4, M2`.

Viết chương trình `GhepPhanHoi` (tệp `GhepPhanHoi.java`):
1. Một `Map<String, String>` từ mã thông điệp sang nội dung yêu cầu.
2. Với phản hồi thứ `k` (từ 0), in `phan hoi <k>: <mã> -> <yêu cầu tra được theo mã>`.
3. Đếm số phản hồi mà việc **ghép theo thứ tự đến** (coi phản hồi `k` là của `M<k>`) sẽ đúng, rồi in `dung neu ghep theo thu tu: <số>/6`.

Chạy: `javac GhepPhanHoi.java && java GhepPhanHoi`. Chấm: `bash labs/cham.sh BNK L10 GhepPhanHoi.java`.
