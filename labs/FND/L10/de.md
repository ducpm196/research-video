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

Kết quả đúng sáu dòng như `mong_doi.txt`. Chạy `bash so_tay.sh`; chấm: `bash labs/cham.sh FND L10 so_tay.sh`. Cần `sqlite3` (cài ở bài đầu tiên; kiểm bằng `sqlite3 --version`), `awk` và `git` (Git Bash có sẵn hai lệnh sau). Chương trình `sqlite3` là bắt buộc. Nếu máy thiếu nó mà lời giải của bạn không kiểm trước, `bash labs/cham.sh` **không** báo thiếu `sqlite3`: nó chỉ báo `KHÁC` (kèm dòng `LECH: …`), vì thông báo `command not found` bị nuốt. Vì vậy chạy `sqlite3 --version` trước khi làm; tệp lời giải mẫu kiểm `command -v sqlite3` ngay trước phần SQL và in `thieu sqlite3, cai theo bai L00` thay vì in nhầm `LECH:`.

## Phụ lục: tệp `sinh.awk` (dùng ở cảnh "Khi dữ liệu lớn gấp 1 000 lần" của video)

Để chạy lại cảnh quy mô, lưu nội dung dưới đây thành `sinh.awk` ở thư mục chứa `so_tay.sh`, rồi `mkdir big && cd big` và `seq 1 10000 | awk -f ../sinh.awk > giaodich.csv`. Bài thực hành không cần tệp này.

```awk
BEGIN { print "ngay,tk,loai,so_tien" }
{ printf "2026-01-%02d,A0%d,%s,%d\n", $1 % 28 + 1, $1 % 3 + 1,
    ($1 % 4 == 0 ? "rut" : "nap"), 1000 * ($1 % 50 + 1) }
```
