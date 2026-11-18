# Lab FND L00 — Kiểm máy bằng một tệp lệnh

Cài đủ công cụ theo bài (từng bước cài nằm ở cảnh “Cài đặt từng bước” của video; giao diện trình cài có thể khác nhẹ theo phiên bản), đúng phiên bản thấp nhất (Git for Windows 2.28 trở lên kèm Git Bash, JDK 21 trở lên, Python 3.11+, và `sqlite3` 3.32 trở lên: tải `sqlite-tools-win-x64` từ sqlite.org, giải nén, chép `sqlite3.exe` vào thư mục `bin` trong thư mục cá nhân), rồi **mở lại** Git Bash. `sqlite3` là bắt buộc: bài 8 và 10 dùng. Kiểm: `sqlite3 --version` in số phiên bản bắt đầu bằng 3.

1. Tạo tệp `kiem.sh` (bằng Visual Studio Code hoặc Notepad++, không dùng Word) với nội dung dưới đây. Chép nguyên, kể cả dấu ✔ (chép dán, không gõ bằng bàn phím); phần giải thích từng dòng ở cảnh "Chuẩn bị máy" của video. Tệp chạy thật lệnh hỏi phiên bản của từng công cụ (`--version`) rồi so với mức thấp nhất; công cụ chưa cài, bản quá cũ, hoặc Python chỉ là lối tắt mở cửa hàng ứng dụng của Windows đều in THIEU. Lưu ở **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó: chuột phải vào chỗ trống của thư mục, chọn *Open Git Bash here*.

```bash
dat() {
  v=$("$1" --version 2>/dev/null | grep -oE '[0-9.]+' | head -1)
  nho=$(printf '%s\n%s\n' "$2" "$v" | sort -V | head -1)
  if [ "$nho" = "$2" ]; then echo "✔ $1"; else echo "THIEU $1"; fi
}
dat bash 4.0
dat git 2.28
dat javac 21
dat java 21
dat python 3.11
dat sqlite3 3.32
```

2. Chạy `bash kiem.sh` ở thư mục đó. Máy đạt khi in **đúng sáu dòng**, mỗi dòng bắt đầu bằng ✔ (xem `mong_doi.txt`).
3. Chấm: `bash labs/cham.sh FND L00 kiem.sh` (chạy từ chính thư mục gốc có `labs`). Dòng báo THIEU nghĩa là thiếu công cụ đó: cài, mở lại Git Bash, chạy lại.

Muốn xem số phiên bản từng công cụ: `bash labs/check_env.sh` (cùng mức thấp nhất, in rõ số và lý do thiếu).
