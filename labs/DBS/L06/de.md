# Lab DBS L06 — SQLite: chuyển mô hình N-N thành bảng DangKy(mssv, ma)

Cơ sở dữ liệu khởi tạo `SV`, `Mon`, `DK` và bảng đầu vào `NhapDK(mssv, ma, diem)`. Bật `PRAGMA foreign_keys = ON;`, chèn bỏ qua trùng lặp từ `NhapDK` sang `DK`, đếm dòng đã chèn, xác nhận có lượt trùng bị chặn và tính điểm trung bình của `'S1'`.

In đúng 3 dòng: `enrolled_rows=<d>`, `dup_enroll_blocked=<0|1>`, `avg_s1=<.1f>`.
Chấm tự động: `bash labs/cham.sh DBS L06 duong_dan/bai_cua_ban.sql`
