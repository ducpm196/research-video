# R4 FND (vòng 4, đọc độc lập, P1 chặt): đã đọc 11/11 bài (L00–L10) — ghi lại bởi người điều phối từ tin nhắn của reader

Môi trường: shim sqlite3 (Python sqlite3 3.45.1), bash 5.2.37, git 2.53, JDK 21, Python 3.11. Lời đọc vượt 2300 từ: L00 3147 (CB-L00), L05 2320, L08 2341, L10 2311.

## 1. Tóm tắt
| Chỉ số | Kết quả |
|---|---|
| MUST = 0 | 11/11 |
| P1 = 2 | 2/11 (L02, L03); P1=1: L01,L04,L05,L06,L07,L08,L09; P1=0: L00, L10 |
| P8 = 2 / P9 = 2 | 11/11 / 11/11 |
| spec_sha256 khớp | 11/11 |
| SRT khớp say | 11/11 |
| Lab chạy ĐÚNG | 11/11 |
| SHOULD | 4 |
| Mất gốc | ĐỦ 9 (L01–L09), GẦN 2 (L00, L10) |

## 2. SHOULD (có bằng chứng)
| Bài | Cảnh | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L06 | intuition step1 | "mọi ngôn ngữ (lập trình) đều có sẵn bộ đọc" | Tuyệt đối sai: JDK 21 không có API JSON (javax.json không tồn tại), C/C++ cũng không | "hầu hết ngôn ngữ phổ biến có thư viện đọc JSON (Python có sẵn json, Java phải thêm thư viện)" | CONFIRMED |
| L07 | formula 3; pitfalls 2; quiz 2 | "Mã nhóm bốn thì thử lại ngay vô ích"; "thử lại y nguyên sẽ luôn cho cùng kết quả" | 408, 429 là 4xx nhưng thử lại có ích (RFC 9110 §15.5.9; RFC 6585 §4) | "thường vô ích (trừ 408, 429 có Retry-After)" | CONFIRMED |
| L07 | hook 1; example 2 | "Content-Length: 7 = nội dung dài 7 ký tự"; "đúng là bảy ký tự" | Content-Length đếm byte (RFC 9110 §8.6); L05 vừa dạy byte khác ký tự | thay "ký tự" bằng "byte" | CONFIRMED |
| L05 | example 4 | "số dòng nằm ở dòng đầu của khối" | Traceback Python: số dòng ở dòng `File "...", line 2`, không phải dòng đầu | "nằm ở dòng File…" | PLAUSIBLE |
Giáo án `curriculum/fnd.yaml` L05 example ghi "ể (7 875)" còn bài dùng "ễ (7 877), e1 bb 85" — đồng bộ.
Nhận xét hiển thị: L00 scale khung 00070 viền focus ở dòng chú thích "Số minh hoạ…" khi lời đọc nói kết luận; L03 scale lệnh `seq … > t12.txt` tạo tệp không hiện trên khung.

## 3. Mục chưa giảng (P1 chặt) — danh sách từng mục
| Bài | Cảnh/step | Trích | Bảng cách đọc phủ | Ghi chú |
|---|---|---|---|---|
| L00 | caidat 3 | "Temurin 21 (LTS)" | không | LTS chưa giảng |
| L00 | caidat 3 | "kiến trúc x64" | không | người học không biết máy mình x64 hay ARM |
| L00 | kiemsh 2,4 | `grep -oE '[0-9]+\.[0-9.]*[0-9]'` | một phần | không giải `[0-9]`, `+`, `\.`, `*` |
| L01 | pitfalls 1 | `mkdir 'Tai lieu'` | không | mkdir giảng ở L02 |
| L04 | example 3 (lặp step 6, pitfalls 3) | `grep -q xin a.txt; echo $?` | không | dấu `;` chưa giảng |
| L05 | example 1 | `public class Chao { public static void main(String[] args) {…} }` + `System.out.println` | không | khung Java chưa giảng |
| L05 | check 3 | `tr -d '\r' < crlf.sh > lf.sh` | không | `<` không giảng |
| L06 | example 2; quiz 2 | `python -c "import json; d = json.load(…); print(…)"` | không | `;` trong mã Python |
| L07 | example 3; pitfalls 1,3 | `curl -s $U/khong_co; echo " ma thoat: $?"` | không | `;` |
| L08 | formula 1; example 3 | `sqlite3 $DB < dung.sql` | một phần | `<` chỉ nói "đưa tệp vào" |
| L08 | example 3; scale 1 | `rm -f $DB; sqlite3 …`; `(echo id,v; seq 1 70000 \| sed …)` | không | `;` |
| L09 | check 1 | `git rev-list --count HEAD` | không | HEAD giảng sau ở pitfalls 3 |
| L10 | scale 1 | `BEGIN { print … }`, `printf "…%02d,A0%d,%s,%d\n"`, `($1 % 4 == 0 ? "rut" : "nap")` | một phần | awk BEGIN/printf %d %02d/`?:` chưa giảng; bài nói "không cần hiểu" |
Biên (đoán được): `false | true` (L04), `int x = 5;` (L05), `curl -sf` (L07), `AND` (L08), `#` chú thích bash (L08), `git rm -q .env` (L09).
Đếm P1 chặt: L00=3, L01=1, L02=0, L03=0, L04=1, L05=2, L06=1, L07=1, L08=2, L09=1, L10=3.
Nguyên nhân gốc: `;` và `<` của bash chưa được giảng ở bài nào; cú pháp Java (L05), awk (L10), regex (L00); `mkdir`/`HEAD` dùng trước khi giảng.

## 4. Người học kẹt ở đâu
L00: caidat 3 (x64) và kiemsh 2 (regex phải chép). L04: example 3 `;`. L05: example 1 khung Java, check 3 `<`. L08: formula 1 `<`. L09: check 1 `HEAD`. L10: scale 1 `sinh.awk`. Các bài còn lại không kẹt.

## 5. Chuẩn xác
~120 số và ~200 lệnh/đoạn mã chạy lại khớp; 11 lab ĐÚNG. Chưa chạy (chỉ đọc): `rm *.txt`, `rm * .txt`, `rm -rf "$DIR"/*` (L02), trình cài Git/JDK/Python/sqlite3 (L00), trích Roediger & Karpicke 2006, Little 1961 (chưa tra mạng). Không nghe audio. Gói công cụ tối thiểu nên kiểm trên Git for Windows sạch (iconv của máy chấm là w64devkit).
