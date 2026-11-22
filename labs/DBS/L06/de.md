# Lab DBS L06 — SQLite thật: chuyển mô hình N–N thành bảng DangKy(mssv, ma_mon)

Viết tập lệnh SQLite dựng 3 bảng `SV`, `MonHoc`, `DangKy(mssv, ma_mon, diem, PRIMARY KEY(mssv, ma_mon))`: nhập 3 lượt đăng ký (thêm 1 lượt trùng cặp bị chặn bởi `INSERT OR IGNORE` — bỏ qua dòng trùng khoá chính), in đúng 3 dòng:
1. `enrolled_rows=3`
2. `dup_enroll_blocked=1`
3. `avg_s1=8.5`

Chấm tự động:
```bash
bash labs/cham.sh DBS L06 duong_dan/bai_cua_ban.sql
```
