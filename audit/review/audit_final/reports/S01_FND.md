# S01 FND: đã đọc 11/11 bài

Phạm vi: `lessons/fnd/L00..L10`, `curriculum/fnd.yaml`, `out/FND/Lxx/` (.srt, chapters.txt, 5–6 khung hình mỗi bài), `labs/FND/Lxx/`. Vai người đọc: chưa từng dùng dòng lệnh, Windows + Git Bash (git 2.53, JDK 21.0.13, Python 3.11.9; máy này KHÔNG có sqlite3 CLI).
Ghi chú độc lập: với L00–L02 tôi lỡ in `loi_giai.sh` cùng `de.md` trước khi tự viết (đã viết lại bằng tay, kết quả không đổi); từ L03 trở đi chỉ đọc `de.md` trước. Với L10 và kiểm `.import` tôi mượn một `sqlite3.exe` 3.46.0 có sẵn trong thư mục Nsight Systems (chỉ chạy trong scratchpad, không chép vào kho).
Phụ: SRT khớp từng chữ với `say` ở cả 11 bài (so bằng script: 0 chỗ lệch). Mọi `checks` trong YAML chạy được: 167/167 đúng, nhưng không bắt được các lỗi ở mục 2.

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L05 | MUST | practice step 0 (và `labs/FND/L05/de.md` mục 1) | "chạy từng tệp một lần để đọc thông báo lỗi… (thông báo ở luồng lỗi, không tính vào kết quả)" / video: "Thông báo lỗi nằm ở luồng lỗi nên không tính vào kết quả chấm" | Với `chao.sh` hỏng, dòng `echo "bat dau"` chạy trước lỗi nên in "bat dau" ra stdout. Làm đúng từng chữ đề (bước 1 rồi 2 rồi 3) thì `cham.sh FND L05` báo `KHÁC mong đợi: 1d0 < bat dau` (đã chạy). `loi_giai.sh` bỏ bước 1 nên không lộ. | Đề nói rõ "chạy bước 1 chỉ để xem, thêm `>/dev/null`" hoặc bỏ bước 1 khỏi tệp chấm | CONFIRMED |
| L08 | MUST | check step 1; pitfalls step 1 | `SELECT COUNT(*) FROM tai_khoan WHERE so_du IS NULL;` → `1` | Bảng `tai_khoan` trên màn hình có đúng 3 hàng (500000, 1200000, 300000), tổng 2 000 000, không hàng NULL nào được chèn. Kết quả đúng là `0`. Chạy bằng sqlite3 3.46 CLI và Python sqlite 3.45: đều `0`. Ví dụ tự mâu thuẫn, lặp ở 2 cảnh. | Chèn thêm một hàng `(4,'Dung',NULL)` trước demo, hoặc đổi số in thành 0 và đổi lời giảng | CONFIRMED |
| L10 | MUST | check step 1; pitfalls step 1 | `$ sqlite3 t.db '.import --csv giaodich.csv gd'` … `SELECT COUNT(*) FROM gd;` → `11`, "10 giao dịch nhưng bảng có 11 hàng: dòng tiêu đề bị nạp như một giao dịch" | Trên `t.db` mới (chưa `CREATE TABLE gd`), `.import --csv` tự tạo bảng với tên cột lấy từ dòng đầu rồi nạp 10 hàng còn lại: COUNT = 10. Chỉ ra 11 khi bảng đã tồn tại. Chạy thật sqlite3 3.46.0: tệp 1 tiêu đề + 3 dữ liệu → COUNT 3 (không 4); bảng tạo trước → 4. Lệnh trên màn hình không cho kết quả như lời. | Thêm dòng `CREATE TABLE gd (...)` trước `.import` ở cả hai cảnh | CONFIRMED |
| L09 | MUST | formula step 2–3; example ①②④⑤; practice | `git commit -q -m 'tao so du ban dau'`; `git switch main` → "Switched to branch 'main'" | Trên Git for Windows mới cài (init.defaultBranch=master ở system config máy này): (a) commit đầu báo `Author identity unknown … fatal: unable to auto-detect email address` (mã 128, đã chạy); video không dạy `git config user.name/user.email` ở đâu trước lần chốt đầu (chỉ nhắc ở mục "Nếu kẹt" của lab); (b) `git init` tạo nhánh `master`, `git switch main` → `fatal: invalid reference: main` (đã chạy). Lab dùng `init -b main` nên không lộ. | Dạy `git config` ở cảnh sym/example; dùng `git init -b main` hoặc nói rõ có thể là master | CONFIRMED |
| L00, L08, L10 | MUST | L00 chuanbi + practice; L08 mọi cảnh có `sqlite3`; L10 formula/practice | L00: "④ sqlite (tuỳ chọn)", kiểm máy "sáu dòng ✔" gồm "✔ sql" | `kiem.sh` in "✔ sql" chỉ nhờ mô-đun `sqlite3` của Python; `cham.sh FND L00` báo ĐÚNG trên máy này dù `sqlite3` CLI không có (`labs/check_env.sh`: ✘ sqlite3). Nhưng L08 video có ~20 lệnh `sqlite3 $DB '…'`, L10 lab dùng `.import --csv --skip 1`/`.print`; không có CLI thì L10 lab ra KHÁC (đã chạy), `loi_giai.sh` L10 phải có shim `sqlrun.py` mà người học không biết. Chuẩn bị máy ở L00 mâu thuẫn với yêu cầu của L08/L10. | L00: sqlite3 CLI bắt buộc, `kiem.sh` kiểm `command -v sqlite3` | CONFIRMED |
| L04 | SHOULD | sym step 1; recap | "set -e: tệp lệnh dừng ngay khi một lệnh trả mã khác 0" | Khẳng định tuyệt đối. Thực tế `set -e` không dừng với lệnh nằm trong điều kiện `if`, vế trái của `&&`/`||`, hoặc không phải lệnh cuối của ống (bash manual). Bài đã dạy pipefail nhưng không nêu ngoại lệ `&&`/`||` ngay cạnh ví dụ dùng `&&`/`||`. | Thêm một câu về ngoại lệ | CONFIRMED (bash manual) |
| L05 | SHOULD | formula step 3 | "chữ có hai dấu như ể (N = 7 875) … 'Nguyễn' = 5 + 3 = 8 byte" | "Nguyễn" chứa ễ (U+1EC5, e1 bb 85), không phải ể (U+1EC3, 7 875). Số byte 8 vẫn đúng; nhãn chữ lẫn nhau. | Dùng ễ = 7 877, e1 bb 85 | CONFIRMED |
| L03 | SHOULD | hook, example, quiz | "Tệp giaodich.csv, bản rút gọn 12 dòng"; quiz "Có bao nhiêu giao dịch rút? / lớn nhất của A02" | Chỉ 9/12 dòng hiện qua các cảnh; dòng 6, 7, 9 không bao giờ hiện, nên câu quiz không làm tay được và người học không dựng lại được tệp (labs/FND/L03 dùng dữ liệu khác). Cảnh scale nói "lệnh in dãy số" nhưng không hiện `seq`. | Hiện đủ 12 dòng ở một cảnh hoặc đưa vào labs | CONFIRMED |
| L08 | SHOULD | quiz step 0 (khung 00097) | `INSERT INTO giao_dich VALUES (1, 1, 200000), … (4, 3, -100000),` | Câu lệnh trên màn hình dừng ở 4/7 hàng và kết thúc bằng dấu phẩy (SQL sai nếu gõ); câu 2 ("tài khoản nhiều giao dịch nhất → 1|3") cần hàng 5–7 không hiện. Bảng `giao_dich` cũng chưa bao giờ hiện đủ ở ví dụ. | Hiện đủ 7 hàng | CONFIRMED |
| L08 | SHOULD | pitfalls step 2 | "Lỗi 3 … Chuyển tiền bằng hai lệnh rời nhau, không giao dịch." | Mã hiện ra lại bọc trong `BEGIN; … ROLLBACK;`, y hệt hook: chú thích nói "không giao dịch", mã thì có. Cảnh không cho thấy trường hợp thật sự không giao dịch. | Đổi mã hoặc chú thích | CONFIRMED |
| L10 | SHOULD | scale, example, quiz | `seq 1 10000 \| awk -f ../sinh.awk`; "tong khop: 130000000"; "Kiểm tay số dư A01: 2 000 000 − …" | `giaodich.csv` 10 dòng và `sinh.awk` không hiện và không có trong labs: kiểm tay, quiz câu 1–2, số 248 221 byte và 130 000 000 đều không tái lập được (chưa kiểm được). | Đưa CSV và `sinh.awk` vào màn hình/labs | CONFIRMED |
| L06 | SHOULD | practice step 0 (và L07 practice) | "Bằng cat > don.json <<'EOF', viết tay JSON…" | Khối chữ nhúng `<<'EOF'` chỉ được giảng ở L10 (sym). L03/L05 de.md hứa "bài sau giải thích"; L06 lần đầu bắt người học tự viết. Cùng bài: mã Python `sum(h["sl"] * h["gia"] for h in hang)`, `python -c` chưa giảng (grep EOF trong L00–L09: 1 chỗ ở L06). | Giảng heredoc ở L02/L03 | CONFIRMED |
| L07 | SHOULD | prereq step 0; practice | "③ chạy nền: lệnh &: chạy ngầm… $! là số tiến trình vừa chạy ngầm" ghi là "điều đã biết"; lab: "cuối cùng kill $SV" | `&`, `$!`, `kill`, `sleep` không được dạy ở L00–L06 (grep 0 chỗ). Phần "ôn lại" thực chất là giảng mới trong một câu. | Dạy trước hoặc chuyển thành thuật ngữ mới ở sym | CONFIRMED |
| L07 | SHOULD | example, formula, quiz | `curl -s -i $U/so_du`, `/chuyen`, `/het_han`, `/cham`, `/loi` | Máy chủ trong video (cổng 18765) có các đường dẫn này; `may_chu.py` của video không hiện, còn máy chủ của lab (cổng 18766) chỉ có `/chao`, `/tai_khoan/42`, `/nap`. Người học không chạy lại được 5 phép của ví dụ. | Dùng chung một máy chủ cho video và lab | CONFIRMED |
| L02 | SHOULD | intuition step 0 (khung 00034) | SVG "sau: MỘT tệp, đổi tên" | Nhãn tràn và bị cắt ở mép khung màu cam. | Rộng khung/thu chữ | CONFIRMED |
| L07 | SHOULD | intuition step 0 (khung 00027) | SVG "chương trình chờ ở cổng 18765" | Chữ rộng hơn khung xanh, đè lên viền hai bên. | Rộng khung | CONFIRMED |
| L01 | SHOULD | quiz step 0 | "Cây ở sơ đồ trên; bạn đang đứng ở /c/Users/ban/hoc/toan" | Màn hình quiz không có cây (đã `CLEAR`); người học phải nhớ cây ở cảnh intuition cách đó ~6 phút. Cạnh đó ở khung 00030 chữ "ls" trong SVG hiện như "Is" (phông sans, l/I khó phân). | Hiện lại cây ở quiz | CONFIRMED |
| L00 (+L01–L04) | SHOULD | practice; `labs/FND/L00/de.md` | "chép nguyên; bài L04 sẽ giải thích từng dòng" | L04 không giảng `for/do/done`, `if/then/else/fi` của `kiem.sh` (L04 giảng `command -v`, `/dev/null`, `&&`). Hơn nữa L00–L04 đều yêu cầu "tạo tệp .sh" và "chạy bash x.sh" nhưng không bài nào dạy cách soạn/lưu tệp hay `cd` vào thư mục chứa tệp trước L05 (L05 chỉ nêu tên VS Code/Notepad++). | Thêm một cảnh "tạo tệp, lưu, chạy" ở L00/L01 | CONFIRMED |
| L01 | SHOULD | example ① | "Dấu / sau tên là của Git Bash" | `ls` trong cửa sổ tương tác của Git Bash thêm `/` (alias `-F`); trong tệp lệnh (lab) không có `/` (tôi chạy: `a`, `b`). Bài không nói khác biệt này; lab `mong_doi` không có `/`. | Thêm một câu | CONFIRMED |

Đã kiểm khớp (không có lỗi): L00 số thang thời gian, bảng 3 quy mô; L01 độ sâu 5−3=2, MAX_PATH 38/254/263; L02 mọi đầu ra `echo`/`rm`/đếm 3-300-3000 và `rm` báo "Is a directory"; L03 `wc -c` 27/4 893/728 895; L04 mã thoát 0/1/2/127, set -e, pipefail, PATH trước/sau, `bash -c`; L05 `od`, `iconv` (Äƒ), `cat -A`, 4 thông báo lỗi javac/python/bash, `grep -n`; L06 hai thông báo `json.tool`, tỉ lệ 2,6/2,5/2,3, YAML `no`→False; L07 Little 50/100/10 000; L08 log2 3/10/17; L09 blob hash `7de0592..ad79274`; L10 các tổng 3 150 000.

## 3. Bảng độ sâu (P1–P7, P8, P9, Tổng P1–P7)

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước (dùng mà không giảng) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 5b4662f813474ed0 | 14:57 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | tạo/lưu tệp `.sh`, `cd` vào thư mục, mở Git Bash, gõ ký tự ✔; "bản ghi"; ổ cơ = HDD, ổ thể rắn = SSD; PATH | cài đặt không hướng dẫn từng bước; kiem.sh gõ "chưa cần hiểu"; sqlite tuỳ chọn mâu thuẫn L08/L10 |
| L01 | 372897def67c06e2 | 14:21 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | tạo tệp lệnh, chạy `bash di.sh`; `mkdir`/`touch` (chép nguyên) | quiz mất hình cây; cách soạn/chạy tệp lệnh |
| L02 | 98c519a5092b5976 | 15:06 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | "biến" (`DIR=`), `-f`, "đệ quy", `find`/`sort` (lab) | 1 nhãn SVG bị cắt |
| L03 | 157d216353efa807 | 15:16 | 2 | 2 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | heredoc `<<'EOF'` (de.md), `seq` | tệp 12 dòng chỉ hiện 9; quiz không làm tay được |
| L04 | 955a0ee4df756f5d | 16:27 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `tr ':' '\n'`, `hash -r`, `chmod +x`, `$PWD`, `#!`, `.bashrc`, cú pháp for/if của kiem.sh | `set -e` khẳng định tuyệt đối; lab `chmod` chỉ ở de.md |
| L05 | b78349c869aa0aae | 16:58 | 0 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 10 | GẦN | nhị phân, thập lục phân, đổi cơ số; "biên dịch/trình biên dịch"; cp1252; `iconv`, `od`; heredoc | 259→100000011→c4 83 nhảy cóc; lab bước 1 làm lệch kết quả (MUST) |
| L06 | 97897884f00b7ca2 | 15:56 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | heredoc tự viết; Python (`json.load`, generator, `python -c`); `python -m json.tool` | heredoc chưa giảng |
| L07 | f2eafa0cfd12d138 | 17:12 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | `&`, `$!`, `kill`, `sleep`, "luồng/thread", "mã chống lặp" | 1 SVG tràn; ví dụ không tái lập; "ôn lại" thực là bài mới |
| L08 | 5c83e28f6e9118ae | 17:19 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | sqlite3 CLI (cài), dấu nhắc `>` của nháy nhiều dòng, "bất biến", `CREATE INDEX` (không dạy) | IS NULL=1 sai (MUST); quiz bảng cắt; chưa có bảng giao_dich đầy đủ |
| L09 | 8200c18808a1d85a | 17:08 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `git config user.name/email`, nhánh mặc định (master/main), `HEAD~1:`, "mã băm" là gì | lệnh trên màn hình không chạy ở máy mới (MUST) |
| L10 | 6c72ddaa20dfcbbc | 19:37 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 11 | GẦN | `CASE WHEN`, `NR`/`$3` của awk (có giảng sơ), sqlite3 CLI, `sinh.awk`, `giaodich.csv` | CSV 10 dòng không hiện; `.import` đếm 11 sai (MUST) |

Điểm P8 = 2 theo thiết kế ở 10/11 bài; L05 = 1 vì làm đúng đề cho kết quả khác `mong_doi`. L10 = 2 chỉ khi có sqlite3 CLI (xem MUST thứ 5).
P1 = 2: 1/11 bài (L03) = 9%. P8 = 2: 10/11 = 91% (100% nếu sửa L05). P9 = 2: 11/11 bài (số liệu 2–3 mức quy mô + đánh đổi ở cảnh scale; L00/L01/L02/L03/L04/L06/L07/L08/L09/L10 có số cụ thể; L05 chỉ so 1 201 với 120 001 dòng, không đo thời gian).
Tổng giờ video: 3 giờ 00 phút (cộng PAUSE trong video đã nằm trong số phút; thời gian tự làm thực tế còn nhiều hơn).

## 4. Lab (tự viết từ `de.md`, chấm bằng `cham.sh`)

| Bài | tự làm được (có/không/phần) | thời gian (PAUSE video; ước người học) | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có (ĐÚNG; CRLF cũng ĐÚNG) | 120 s; 30–60 phút gồm cài đặt | tạo tệp `.sh` bằng gì, `cd` vào đâu, gõ ✔; `cham.sh` cần chạy từ thư mục có `labs/` | khớp (6 dòng ✔) |
| L01 | có (ĐÚNG) | 150 s; ~10 phút | tạo tệp `.sh` và `bash di.sh` chưa dạy | khớp |
| L02 | có (ĐÚNG) | 180 s; ~10 phút | không | khớp |
| L03 | có (ĐÚNG) | 240 s; ~15 phút | heredoc 18 dòng "chép nguyên" lấy từ de.md (màn hình chỉ nói "xem de.md") | khớp (kể cả đệm 7 cột của `uniq -c`) |
| L04 | có (ĐÚNG) | 300 s; ~20 phút | `chmod +x` chỉ ở de.md (không cần trên Git Bash, đã thử) | khớp |
| L05 | phần: làm đúng từng chữ đề → KHÁC (thừa dòng "bat dau"); bỏ lệnh chạy thử bước 1 → ĐÚNG | 300 s; ~20 phút + bối rối | bước 1 chạy `bash chao.sh` chưa sửa in "bat dau" ra stdout | KHÔNG khớp nếu theo đề từng chữ; khớp 4 dòng nếu bỏ bước 1 |
| L06 | có (ĐÚNG) | 300 s; ~20 phút | viết `<<'EOF'` chưa dạy; Python | khớp |
| L07 | có (ĐÚNG) | 300 s; ~15 phút | chép 40 dòng máy chủ, `&`, `kill $SV` | khớp |
| L08 | có (ĐÚNG, cả bằng `sqlrun.py` lẫn sqlite3 3.46) | 300 s; ~15 phút | không có sqlite3 CLI thì mọi ví dụ video lỗi, lab vẫn chấm được nhờ `sqlrun.py` | khớp |
| L09 | có (ĐÚNG) | 300 s; ~15 phút | cấu hình danh tính, `-b main` đã có trong de.md | khớp |
| L10 | phần: ĐÚNG khi có sqlite3 CLI; KHÔNG khi chỉ có Python (sqlite3 không tìm thấy) | 420 s; ~30 phút | `.import --skip 1`, `.print` cần CLI; shim `sqlrun.py` nằm trong `loi_giai.sh`, người học không biết | khớp (6 dòng) |

## 5. Người học kẹt ở đâu (chỉ xem video này và các bài trước)

- L00: lab (cảnh `practice` step 0): "Tạo tệp kiem.sh với đúng nội dung… Chạy bash kiem.sh trong thư mục chứa tệp" — chưa biết soạn/lưu tệp (và gõ ✔), `cd`; cảnh `chuanbi` không hướng dẫn trình cài đặt.
- L01: cảnh `quiz` step 0: "Cây ở sơ đồ trên" nhưng không còn cây trên màn hình; lab: "tạo tệp di.sh" (chưa học cách tạo/chạy tệp lệnh).
- L02: không kẹt trong video; lab lặp lại điểm kẹt "tạo dung.sh" như L01.
- L03: cảnh `quiz` step 0: "Dùng tệp giaodich.csv mười hai dòng ở trên… Có bao nhiêu giao dịch rút?" — chỉ thấy 9/12 dòng, không tự làm tay được.
- L04: cảnh `formula` step 0: `echo $PATH | tr ':' '\n'` (tr chưa giảng, đọc được qua kết quả); cảnh `quiz` step 1: `hash -r`; không kẹt cứng.
- L05: cảnh `formula` step 1: "259 → 100000011 → 00100 000011 ⇒ 110… = c4 83" — chưa học nhị phân/thập lục phân; lab bước 1 làm sai kết quả chấm.
- L06: cảnh `practice` step 0: "Bằng cat > don.json <<'EOF'" — khối chữ nhúng chưa từng được giảng (đến L10 mới giảng); mã Python `sum(h["sl"] * h["gia"] for h in hang)`.
- L07: cảnh `prereq` ③ "chạy nền: lệnh &, $!" được gọi là "đã biết" nhưng chưa dạy; `example` ① `python may_chu.py 18765 > /dev/null 2>&1 & SV=$!`.
- L08: cảnh `formula` step 0: `sqlite3 $DB < dung.sql` → "sqlite3: command not found" nếu theo L00 (sqlite tuỳ chọn); rồi cảnh `check` step 1 `IS NULL` ra 1 mâu thuẫn với bảng 3 hàng.
- L09: cảnh `formula` step 2: `git commit -q -m 'tao so du ban dau'` → "Author identity unknown… fatal"; `example` ④ `git switch main` → "invalid reference: main" (nhánh mặc định là master).
- L10: cảnh `formula` step 0: `sqlite3 so_tay.db <<'EOF'` + `.import --csv --skip 1 giaodich.csv gd` — cần sqlite3 CLI và `giaodich.csv` (không cho); `CASE WHEN` chưa giảng.

## 6. Số đã tính lại / mã đã chạy

- `checks` trong YAML: 167 biểu thức, 167 đúng (L00 24, L01 13, L02 11, L03 16, L04 8, L05 15, L06 14, L07 17, L08 20, L09 14, L10 15).
- Tính lại độc lập ngoài `checks`: 17 con số bằng Python/Git, 17 khớp (L03 byte 27/4 893/728 895; L04 xác suất 1,0/9,5/63,2%; L06 byte CSV/JSON 15/39, 1 592/3 992, 178 894/418 894 và tỉ lệ 2,6/2,5/2,3; L00 115,7 ngày; L09 hai blob hash 7de0592/ad79274 bằng `git hash-object`; L05 UTF-8 của ă). Các số còn lại (L00 bảng 3×3, L01 độ dài đường dẫn 38/254/263, L07, L08, L10) tính tay và đối chiếu với `checks`, khớp, nhưng không chạy riêng.
- Chạy thật lệnh/đoạn mã trên màn hình: khoảng 55 đầu ra so với lời bài; 49 khớp, 6 lệch (đã nêu ở mục 2): L05 (lab bước 1), L08 (`IS NULL`, 2 cảnh), L10 (`.import` 11), L09 (identity, master/main), L00/L10 (sqlite3 CLI). Phần chạy: L02 (11 đầu ra), L04 (14), L05 (12: od, iconv, cat -A, loi.sh, 3 javac, NameError, grep -n, seq|sed), L06 (json.tool 2 lỗi, YAML), L08 (rollback, 7/2, IS NULL), L09 (hash, identity, nhánh mặc định).
- Lab: 11/11 bài đã tự viết và chạy `cham.sh`: 9 ĐÚNG ngay (L00, L01, L02, L03, L04, L06, L07, L08, L09), L05 KHÁC khi làm đúng từng chữ đề (ĐÚNG sau khi bỏ chạy thử), L10 chỉ ĐÚNG khi có sqlite3 CLI (3.46.0) hoặc shim; không ĐÚNG khi chỉ có Python.

## 7. Khung hình đã xem (≥ 5 mỗi bài)

- L00: 00000, 00022, 00030, 00071, 00092, 00113
- L01: 00030, 00052, 00074, 00096, 00113, 00128
- L02: 00004, 00034, 00058, 00086, 00118
- L03: 00002, 00027, 00041, 00072, 00099
- L04: 00026, 00055, 00071, 00090, 00102
- L05: 00002, 00027, 00037, 00051, 00108
- L06: 00024, 00031, 00046, 00084, 00094
- L07: 00002, 00027, 00056, 00070, 00094
- L08: 00028, 00071, 00076, 00097, 00108
- L09: 00026, 00032, 00058, 00073, 00086
- L10: 00027, 00035, 00062, 00068, 00104

Lỗi hiển thị: L02 khung 00034 (nhãn SVG bị cắt), L07 khung 00027 (chữ tràn khung), L01 khung 00030 ("ls" nhìn như "Is"), L08 khung 00097 (INSERT cắt giữa chừng, kết thúc bằng dấu phẩy), L01 khung 00096 (quiz thiếu cây). Chung: nửa dưới mỗi khung hình để trống (chữ vẫn đọc được, cỡ chữ ổn). Không thấy chữ đè/lẫn ở các khung còn lại.

## 8. Nhận xét chung

- Chất lượng giảng nội dung rất đều: mỗi bài có hook, ôn lại, giải mã thuật ngữ, hình cơ chế, ví dụ có số, tự kiểm hai đường, bảng quy mô 3 mức, ba lỗi (người mới/đi làm), quiz có "quyết định", lab có kết quả mong đợi; lời đọc khớp từng chữ với SRT.
- Số liệu và đầu ra lệnh gần như đều đúng (49/55 chạy khớp); lỗi tập trung ở các demo SQL/Git phụ thuộc môi trường hoặc dữ liệu ngầm (IS NULL, `.import`, nhánh mặc định, danh tính git).
- Điểm yếu lớn nhất đối với người mất gốc là chuỗi "tạo và chạy tệp lệnh": L00–L04 đều bắt đầu lab bằng "tạo tệp .sh" mà trình soạn tệp, `cd`, `bash x.sh` và heredoc đều chưa được dạy đúng chỗ (heredoc chỉ giảng ở L10; trình soạn chỉ nêu tên ở L05).
- Dữ liệu ví dụ bị giấu (giaodich.csv L03/L10, giao_dich L08, máy chủ video L07, sinh.awk) khiến người học không tái lập được ví dụ trên máy và quiz ở L03/L08/L10 không làm tay được; labs dùng dữ liệu khác nên không thay thế được.
- Hợp đồng môi trường chưa nhất quán: sqlite3 CLI "tuỳ chọn" ở L00 nhưng bắt buộc ở L08/L10; Git cần cấu hình danh tính và nhánh mặc định trước L09; `kiem.sh` báo ✔ sql dù thiếu CLI.
- Thước đạt ngưỡng chốt: MUST = 5 (0 yêu cầu); P1 = 2 chỉ 9% (cần ≥ 90%); P8 = 2 là 10/11 = 91% (cần 100%). Vì vậy FND chưa đạt cổng "bắt đầu học" theo ngưỡng kế hoạch; nhưng các MUST đều sửa được nhỏ (thêm một dòng `CREATE TABLE`, sửa số 1→0, thêm `git config`/`-b main`, sửa đề L05, đổi sqlite3 thành bắt buộc).
- Mất gốc: 9 bài ĐỦ, 2 bài GẦN (L05 vì P1 = 0, L10 vì dữ liệu ẩn); không bài nào CHƯA.
