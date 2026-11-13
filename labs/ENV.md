# Môi trường thực hành chuẩn của toàn bộ khoá học (hợp đồng CB-AF1-1)

Mọi cảnh **Tự làm** và mọi thư mục `labs/<KHOÁ>/<Lxx>/` được viết và **kiểm bằng máy** trên đúng môi trường này. Cài theo bài `FND` (Nền thực hành) trước khi học Java.

| Thành phần | Phiên bản chuẩn | Dùng từ | Kiểm |
|---|---|---|---|
| Hệ điều hành | Windows 10/11 (macOS, Linux cũng chạy được) | — | — |
| Cửa sổ lệnh | **Git Bash** (đi kèm Git for Windows) — dùng cho MỌI lệnh trong khoá, không dùng PowerShell hay Command Prompt | FND | `bash --version` |
| Git | 2.40 trở lên | FND | `git --version` |
| JDK | Temurin 21 (LTS) | JVA | `javac -version`, `java -version` |
| Python | 3.11 trở lên (kho kiểm trên 3.13) | PYT | `python --version` |
| sqlite3 | 3.40 trở lên | FND | `sqlite3 --version` |
| Docker Desktop | bản mới (tuỳ chọn, chỉ từ chặng 7) | chặng 7–8 | `docker --version` |

Kiểm nhanh: `bash labs/check_env.sh` — in từng dòng ✔ hoặc ✘ kèm cách khắc phục.

## Cách làm một lab
1. Mở Git Bash trong thư mục kho (hoặc thư mục bạn tải về), `cd labs/<KHOÁ>/<Lxx>`.
2. Đọc `de.md`. **Tự làm trước**, trong một thư mục tạm của bạn (ví dụ `~/hoc/<KHOÁ>-<Lxx>/`).
3. Chấm: `bash labs/cham.sh <KHOÁ> <Lxx> <tệp của bạn>` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt` (và cũng trùng chữ hiện trên video), hoặc in chỗ khác nhau.
4. Chỉ mở `loi_giai.*` sau khi bạn đã thử ít nhất một lần. Bài giấy bút: đối chiếu từng bước với `loi_giai.md`.

## Quy ước
- Tên tệp Java trùng tên lớp `public class`; một tệp một lớp trừ khi `de.md` nói khác.
- Lab không cần mạng, trừ bước cài công cụ ở bài FND. Lab Docker ghi rõ ở dòng đầu `de.md`.
- Số liệu dùng trong lab là **số minh hoạ**; khác số của ví dụ trong video để bạn không chép lại được.

## Tệp tải thêm (chỉ khi một bài nói rõ)
Mọi bài chạy được chỉ với JDK; riêng các bài sau dùng một tệp `.jar` tải về thư mục `lib/` của bạn (lệnh tải và kiểm băm có ngay trong bài):

| Tệp | Phiên bản | Dùng ở | Nguồn chính thức | sha256 |
|---|---|---|---|---|
| `junit-platform-console-standalone-1.10.2.jar` | 1.10.2 | JV2 L06 | https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.10.2/junit-platform-console-standalone-1.10.2.jar | `a1de557821293ce903c213c694165fff532cf92081bac4238b9e05b35f04f43f` |

Lab của bài luôn chấm được **không cần** tệp này (chỉ dùng khẳng định tự viết).
