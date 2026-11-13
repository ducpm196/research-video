# Lab FND L10 — Sổ tay chi tiêu: bash + SQL + git

Tạo `so_tay.sh`. **Chép nguyên** đoạn tạo dữ liệu `gd.csv` (số minh hoạ):

```bash
cat > gd.csv <<'EOF'
ngay,loai,so_tien
01,luong,12000000
02,an,150000
03,di_lai,60000
05,an,220000
08,mua_sam,900000
10,an,95000
12,di_lai,45000
15,luong,3000000
EOF
```

Rồi viết:
1. **SQL** (sqlite3): bảng `gd (ngay TEXT, loai TEXT, so_tien INTEGER)`, nạp dữ liệu (bỏ dòng tiêu đề; `.import --csv --skip 1 gd.csv gd` hoặc `sed` đổi mỗi dòng thành `INSERT`), rồi in **tổng chi theo loại** (loại khác `luong`, sắp theo tên loại) và dòng `so du` = tổng `luong` trừ tổng chi. Ghi cả hai kết quả vào `bao_cao.txt` và in ra.
2. **Kiểm độc lập**: tính số dư bằng `awk -F,` từ `gd.csv`, so với số dư của SQL, in `tong khop: <số>` hoặc `LECH: <a> <b>`.
3. **git**: `git init -q -b main repo`, chép `bao_cao.txt` và `gd.csv` vào `repo`, đặt `user.name`/`user.email` cục bộ, chốt với lời nhắn `bao cao thang 1`, in `git log --format=%s`.

Kết quả đúng sáu dòng như `mong_doi.txt`. Chạy `bash so_tay.sh`; chấm: `bash labs/cham.sh FND L10 so_tay.sh`. Cần sqlite3, awk, git (Git Bash có awk và git; sqlite3 theo bài đầu tiên). Máy kiểm của kho chưa cài sqlite3 nên `loi_giai.sh` có hai dòng thay thế bằng `labs/sqlrun.py`; bạn đã cài sqlite3 thì không cần chúng.
