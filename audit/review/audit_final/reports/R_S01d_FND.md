# S01 FND (L00–L10): đã đọc 11/11 bài

Người đọc độc lập, bản dựng lại 2026-11-14. Đọc trọn YAML (mọi `show`/`say`/quiz/`checks`), so SRT với `say`, xem 5–7 khung mỗi bài, chạy lab và mã trên màn hình (Git Bash, scratchpad). Không sửa/tạo tệp nào trong repo ngoài báo cáo này.

Hạn chế môi trường (nêu để biết độ tin): máy kiểm KHÔNG có `sqlite3` (đúng ca "chưa cài" mà L00 dạy cài). Việc tải sqlite-tools bị chặn nên các lệnh sqlite3 ở L08/L10 chạy bằng mô-đun `sqlite3` của Python 3.11 (SQLite 3.45.1) + một lớp giả `sqlite3` do tôi viết ở scratchpad (hỗ trợ `.print`, `.import --csv --skip`). Riêng cờ `-header` và `.import --csv` của CLI thật chưa chạy trên CLI thật. `git` chỉ chạy trong thư mục tạm của scratchpad (lab L09 và kiểm lệnh), không chạm kho.

## 1. Khớp video với đặc tả
| Kiểm | Kết quả |
|---|---|
| `spec_sha256` trong `build_report.json` so với digest YAML hiện tại (công thức của `lv.spec_digest`: bỏ `asr_reviewed`, JSON sort_keys) | 11/11 KHỚP, không bài nào lệch. (YAML L00, L03, L10 có mtime sau lúc build nhưng chỉ đổi `asr_reviewed`; sha256 toàn tệp của L00/L03/L10 vì thế khác `spec_sha256`, nhưng digest nghiệp vụ vẫn khớp.) |
| SRT so với `say` (chuẩn hoá bỏ dấu câu) | 11/11 bài: số cue = số câu `say` (tổng 1 573), 0 cue thừa, 0 câu thiếu, từng bài chuỗi toàn văn trùng |
| `chapters.txt` so với `title` các cảnh | 11/11 trùng (L00 15 mục, các bài còn lại 12) |
| "Kết quả mong đợi" trên màn hình so với `labs/FND/Lxx/mong_doi.txt` (bỏ khoảng trắng) | 11/11 khớp |

sha16 YAML lúc đọc: L00 48db01b579fb9ba8 · L01 77c8fbf1e4ede749 · L02 dd8c6c67039cf7f6 · L03 ac792a19e608633c · L04 e5bea3eb749047de · L05 80ee21be8090d476 · L06 61a9b7bafb839ed5 · L07 40a7167ad3602feb · L08 52187a1dedf84e84 · L09 7b16546f6e0f4114 · L10 deb74a29b287853f.

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)
MUST: 0. SHOULD: 7 (ca L10 là gần MUST, xem dòng đầu).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L10 | SHOULD (gần MUST: ví dụ mâu thuẫn giữa hai cảnh) | pitfalls#3 rồi quiz#1 | pitfalls: `sqlite3 so_tay.db 'SELECT COUNT(*) FROM gd;'` → `20`. quiz: "Dùng dữ liệu và so_tay.db của bài" → `750000` và `2026-01-02|3500000` | Cả hai cảnh dùng cùng tệp `so_tay.db`. `so_tay_loi.sh` không `rm`, chạy 2 lần để lại 20 hàng. Tôi dựng đúng chuỗi: sau pitfalls, quiz cho `1500000` và `2026-01-02|7000000` (gấp đôi đáp án trên màn hình). Học viên chạy tuần tự theo video sẽ thấy lệch. | Thêm `bash so_tay.sh` (dựng lại sạch) trước quiz, hoặc cho `so_tay_loi.sh` ghi db khác (`loi.db`) | CONFIRMED (qua lớp giả sqlite3) |
| L09 | SHOULD | pitfalls#1 rồi #2 | `echo x >> a.txt` … `git status -s` → ` M a.txt` | `a.txt` chưa từng `add`/chốt trong bài; chạy đúng các lệnh hiện ra thì mã là `?? a.txt` chứ không phải ` M`. Ví dụ không tự đứng. | Thêm lệnh tạo và chốt `a.txt` trước, hoặc dùng `so_du.txt` | PLAUSIBLE (suy từ cách `git status -s` hoạt động) |
| L07 | SHOULD | sym#2 | SAY: "lệnh chờ cho máy chủ vài phần giây" / màn hình: `sleep 1` "chờ 1 giây" | Lời đọc và màn hình lệch (vài phần giây so với 1 giây). | Sửa lời: "chờ một giây" | CONFIRMED |
| L04 | SHOULD | example#2 | `grep -q xin a.txt; echo $?` → `0` | Nội dung `a.txt` không hề hiện ở cảnh này (chỉ ở quiz mới nói "tệp có chữ xin chao"); không thể tự dựng lại 0 và 1. | Thêm `echo "xin chao" > a.txt` vào đầu cảnh | CONFIRMED |
| L06 | SHOULD | scale#0 | `head -n 1 a10k.csv` → `1,Le Hoa,39000` | Không hiện lệnh tạo `a10k.csv`/`a10k.json` (chỉ nói "lệnh in dãy số nối với lệnh thay chữ"), nên người học không tái lập được bảng 15/39 byte. Tôi dựng bằng Python thì cả 9 số khớp. | Hiện lệnh `seq … | sed …` như L08 | CONFIRMED |
| L01 | SHOULD | practice#1 | "Kết quả mong đợi: y.txt / z.txt / hd.txt …" mỗi tên một dòng | Chạy `bash di.sh` ngay trên cửa sổ lệnh (đầu ra là màn hình), `ls` xếp cột `y.txt  z.txt`; chỉ khi ghi vào tệp (như `cham.sh`) mới mỗi dòng một tên. Học viên "so từng dòng bằng mắt" sẽ thấy khác dù chấm máy ĐÚNG. | Thêm một câu nói về xếp cột, hoặc dùng `ls -1` trong de.md | PLAUSIBLE (hành vi chuẩn của `ls` khi stdout là cửa sổ lệnh; không có tty để thử) |
| L05 | SHOULD | hook#0 | SAY: "một bảng mã cũ của hệ điều hành bạn đang dùng"; màn hình `iconv -f cp1252` | cp1252 là trang mã cũ của Windows Tây Âu; Windows tiếng Việt cũ dùng cp1258. Câu khái quát "của hệ điều hành bạn đang dùng" thiếu điều kiện. | "ví dụ một bảng mã cũ của Windows" | PLAUSIBLE |

Kiểm số và mã (đã chạy, không lỗi nào khác): xem mục 6. Các khẳng định có nguồn (Little 1961 ở L07; Roediger & Karpicke 2006 ở L00, tự ghi NOT_VERIFIED trong `source`) không kiểm được nguồn gốc trong phiên này, ghi "chưa kiểm được nguồn".

## 3. Bảng độ sâu
Phút = thời lượng video. Tổng = P1..P7 (tối đa 14). "Mất gốc": ĐỦ ≥ 12 và không mục 0.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước (dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 48db01b579fb9ba8 | 17,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `printf '%s\n%s\n'` (trong `nho=$(…)` của kiem.sh); "trình biên dịch" (ở lỗi JRE/JDK) | chuanbi#4–5: dòng `nho=$(printf '%s\n%s\n' "$2" "$v" \| sort -V \| head -1)` không được giải từng phần; kiem.sh hiện đủ 10 dòng chỉ ~5 giây (frame 00107) rồi bị thay bằng bảng, phải chép từ de.md |
| L01 | 77c8fbf1e4ede749 | 15,0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | (`mkdir` ở pitfalls#0 giảng muộn ở cảnh practice, nhưng ngữ cảnh đủ đoán) | không có điểm thiếu đáng kể; ví dụ ls cột xem mục 2 |
| L02 | dd8c6c67039cf7f6 | 16,2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `&&` (hook#0: `mkdir bc && cd bc`) | `&&` chỉ được giảng ở L04 |
| L03 | ac792a19e608633c | 16,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | — |
| L04 | e5bea3eb749047de | 17,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `grep -q` (example#2); `$HOME` (pitfalls#1) | nội dung `a.txt` ở example#2 (mục 2) |
| L05 | 80ee21be8090d476 | 18,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `sed 's/^/INFO dong /'` và `^` (scale#0); mẫu `[0-9]*` trong `grep -o 'line [0-9]*'` (example#1) | cảnh scale: `seq … \| sed` không giảng |
| L06 | 61a9b7bafb839ed5 | 16,9 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | — | P3: formula#1–#2 bỏ `don.json` khỏi màn hình khi nói "hang → [1] → gia"; frame 00092 dòng `python -c` thứ hai vượt ra ngoài khung mã; scale không hiện lệnh sinh dữ liệu |
| L07 | 40a7167ad3602feb | 18,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | (`-w "%{http_code}\n"` chỉ giải "in mã", đủ dùng) | lệch "vài phần giây" ở sym#2 |
| L08 | 52187a1dedf84e84 | 19,3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `sed 's/.*/&,&/'` và `.*`, `&`, nhóm lệnh `( … ) > big.csv` (scale#0) | cảnh scale: lệnh sinh 70 000 hàng không giảng; không đo thời gian (chỉ đếm bước, bài ghi rõ) |
| L09 | 7b16546f6e0f4114 | 18,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | (`git rm` ở pitfalls#2 chưa giảng riêng, ngữ cảnh đủ) | ví dụ ` M a.txt` (mục 2) |
| L10 | deb74a29b287853f | 21,6 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | cú pháp awk: `if … else`, `s += $4`, `END { print s }` (formula#2); `<>` (quiz); `printf "%02d"` (tự ghi "không cần hiểu") | formula#2 mới giảng `-F,`, `$3`, `NR`; mâu thuẫn so_tay.db giữa pitfalls và quiz (mục 2) |

Tổng thời lượng 11 video: 3 giờ 17 phút (11 817 giây). Ghi chú điểm: mọi bài có cảnh "Khi … nhân lên" với số ở 2–3 mức (P9) và pitfalls 3 lỗi "người mới / người đã đi làm" (P6); quiz đều có `pause` 60–90 giây (L10: 90 giây cho hai câu SQL + một quyết định hơi chật nhưng chấp nhận).

Ngưỡng chốt:
| Ngưỡng | Kết quả | Đạt? |
|---|---|---|
| MUST = 0 | 0 (L10 là ca SHOULD gần MUST; nếu người điều phối xếp MUST thì L10 = 1) | ĐẠT (có lưu ý) |
| P1 = 2 ở ≥ 90% bài | 5/11 bài (L01, L03, L06, L07, L09) = 45%. 6 bài còn lại (L00, L02, L04, L05, L08, L10) mỗi bài có 1–2 ký hiệu/lệnh chưa giảng, liệt kê ở cột "Cần biết trước". Nếu bỏ qua lệnh chỉ dùng để sinh dữ liệu giả (L08 sed) và `&&` trang trí ở hook L02 thì được 7/11 = 64%, vẫn dưới 90% | KHÔNG ĐẠT |
| P8 = 2 ở 100% | 11/11 | ĐẠT |
| Mất gốc ĐỦ | 11/11 (tổng 13–14, không mục 0) | ĐẠT |

## 4. Lab
Tự làm trước theo `de.md` (không mở `loi_giai.*`), chấm bằng `bash labs/cham.sh FND Lxx <tệp>`, sau đó so lời giải (L01, L02, L03 trùng gần nguyên văn; các bài khác khác văn nhưng cùng đầu ra).

| Bài | Tự làm được | Thời gian (tôi viết + gợi ý pause trong video) | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | Phần: chép kiem.sh từ de.md và chạy được; kết quả `✔` ×5 + `THIEU sqlite3` vì máy kiểm chưa cài sqlite3 (đúng thiết kế); cham.sh in KHÁC đúng dòng 6 | ~3 phút / pause 120 giây (cài đặt thật của người học dài hơn nhiều) | không kẹt kỹ thuật; bài có hướng dẫn cài sqlite3 đủ 4 bước (tải zip, giải nén, chép vào `~/bin`, mở lại Git Bash, `sqlite3 --version`); tôi đã xác minh `/etc/profile.d/env.sh` đặt `$HOME/bin` vào PATH, và trang sqlite.org vẫn có mục Precompiled Binaries for Windows với `sqlite-tools-win-x64-….zip` | có |
| L01 | Có (ĐÚNG ngay lần đầu) | ~2 phút / 150 s | không | có |
| L02 | Có (ĐÚNG) | ~3 phút / 180 s | không | có |
| L03 | Có (ĐÚNG) | ~3 phút / 240 s | không | có |
| L04 | Có (ĐÚNG; hint `javac -version 2>&1 \| cut -d. -f1` đủ) | ~4 phút / 300 s | không | có |
| L05 | Có (ĐÚNG; `sed -i` có gợi ý) | ~4 phút / 300 s | không | có |
| L06 | Có (ĐÚNG). Bước 3 (đọc YAML bằng mắt rồi `echo` bốn số) quá nhẹ, không phải thực nghiệm | ~3 phút / 300 s | không | có |
| L07 | Có (ĐÚNG; máy chủ chạy nền và `kill $SV` giải phóng cổng 18766, đã kiểm) | ~4 phút / 300 s | không | có |
| L08 | Có (ĐÚNG; cham.sh dùng `sqlrun.py` dự phòng vì máy thiếu sqlite3, người học đã cài sqlite3 sẽ dùng CLI thật) | ~3 phút / 300 s | không | có |
| L09 | Có (ĐÚNG; lab đặt user cục bộ nên khỏi vướng `Author identity unknown`) | ~3 phút / 300 s | không | có |
| L10 | Phần: ĐÚNG nhưng chỉ qua lớp giả sqlite3 (CLI thật không có trên máy) | ~6 phút / 420 s | không; điểm vướng tiềm ẩn là awk `if/else`, `END` | có |

Đề đủ để tự làm: có ở cả 11 bài (mỗi `de.md` nói rõ thứ tự việc và kết quả). Thiếu kiến thức nằm ở các cột "Cần biết trước" (chủ yếu awk ở L10, sed ở L05/L08).

## 5. Người học kẹt ở đâu (người mất gốc, xem tuần tự L00 đến Lxx)
| Bài | Chỗ đầu tiên không theo được |
|---|---|
| L00 | chuanbi#4–5: `nho=$(printf '%s\n%s\n' "$2" "$v" \| sort -V \| head -1)`, phần `printf '%s\n%s\n'` không được giải; nên chép nguyên theo lời "ta đọc từng phần" |
| L01 | không kẹt |
| L02 | hook#0: `mkdir bc && cd bc` ("&&" chưa nói) |
| L03 | không kẹt |
| L04 | example#2: `grep -q xin a.txt; echo $?` (không biết a.txt chứa gì, `-q` chưa giảng) |
| L05 | scale#0: `seq 1 1200 \| sed 's/^/INFO dong /' > app.log` ("sed", "^" chưa giảng); và example#1 `grep -o 'line [0-9]*'` |
| L06 | không kẹt (scale#0 `head -n 1 a10k.csv` không tái lập được) |
| L07 | không kẹt (phải có `may_chu.py` từ de.md mới chạy theo được; bài nói rõ) |
| L08 | scale#0: `(echo id,v; seq 1 70000 \| sed 's/.*/&,&/') > big.csv` |
| L09 | không kẹt (ví dụ ` M a.txt` ở pitfalls#2 không tái lập được) |
| L10 | formula#2: `b=$(awk -F, 'NR > 1 { if ($3 == "nap") s += $4; else s -= $4 } END { print s }' giaodich.csv)` (if/else, `+=`, `END`) |

## 6. Số đã tính lại / mã đã chạy
- Số tính lại bằng Python hoặc đếm byte thật: khoảng 125 giá trị (L00 bảng 3×3 + 28 giờ + 115,7 ngày + 27 giờ 46 phút 40 giây + 20/2,02/9,9; L01 38/254/263 ký tự; L03 27/4 893/728 895 byte + 3,5 tỉ; L04 1,0/9,5/63,2%; L05 259 = 100000011 = c4 83, 7 877 = e1 bb 85, 6/8 byte; L06 15/39, 1 592/3 992, 178 894/418 894 và tỉ lệ 2,6/2,5/2,3; L07 50/100/10 000 người phục vụ, Content-Length 7/12/13; L08 log2 = 3/10/17, các tổng 2 000 000/1 900 000; L09 2³, 2¹⁰, 2¹⁷, băm blob `7de0592`/`ad79274` đúng bằng `git hash-object`; L10 292/10 001/248 221 byte, 130 000 000, 3 150 000). Khớp 125/125.
- Mã chạy trên màn hình (Git Bash, đúng như người học gõ): khoảng 110 đoạn lệnh trên 11 bài, gồm cả 11 lab. Không có đầu ra nào lệch ngoài các ca đã xếp vào bảng 2 (L10 quiz do so_tay.db 20 hàng, đã chạy; L09 ` M a.txt` suy từ hành vi git, chưa chạy đúng chuỗi của video).
- Chỉ đọc, không chạy được trên CLI thật: `sqlite3 -header`, `.import --csv big.csv g` ở L08 (chạy phần SQL bằng Python SQLite 3.45.1: kết quả khớp, kể cả `EXPLAIN QUERY PLAN` chuyển từ `SCAN g` sang `SEARCH g USING INDEX idx_id (id=?)`).
- Kiểm hiện tượng riêng: `./chao.sh` chạy được không cần `chmod +x` trên Git Bash (đúng như L04 nói); `cd Tai lieu` báo `too many arguments`; `cd C:\Users\ban` báo `C:Usersban` (đúng L01); `python -m json.tool` cho `Expecting ',' delimiter: line 2 column 2 (char 10)` (đúng L06); `javac` 21 cho đúng 4 thông báo ở L05 (kể cả `\u201c`, `reached end of file while parsing`); `curl -f` mã thoát 22, `--max-time` mã 28 (đúng L07).

## 7. Khung hình đã xem (≥ 5 mỗi bài) và lỗi hiển thị
- L00: 00000, 00024, 00072, 00107, 00112, 00139, 00150
- L01: 00029, 00058, 00073, 00088, 00105
- L02: 00032, 00077, 00094, 00121, 00133
- L03: 00028, 00035, 00081, 00090, 00104
- L04: 00024, 00047, 00065, 00080, 00104
- L05: 00027, 00052, 00072, 00089, 00113
- L06: 00024, 00033, 00051, 00067, 00092
- L07: 00026, 00031, 00057, 00080, 00105
- L08: 00026, 00039, 00061, 00083, 00115
- L09: 00025, 00031, 00070, 00086, 00101
- L10: 00026, 00040, 00087, 00105, 00115

Lỗi hiển thị: chữ lớn, không đè, không cắt ở 57 khung đã xem. Một lỗi nhỏ: L06 frame 00092, dòng lệnh `python -c "...sum(t['han_muc'] for t in d['cac_the']))"` tràn ra ngoài đường viền ô mã (không bị cắt). Hai điểm cần lưu ý nhưng không phải lỗi dựng: L00 frame 00107 giữ 10 dòng kiem.sh chỉ ~5 giây; L06 formula#1–#2 (frame 00033) không còn `don.json` trên màn hình khi nói đường đi `hang → [1] → gia`. Các ký tự `$` (viết `&#36;` trong YAML) hiển thị đúng (kiểm frame 00107 L00, 00058 L01 và các khung lệnh khác).

## 8. Ngôn ngữ lời đọc (mục 4 của yêu cầu)
- Số nhóm bằng dấu cách: văn xuôi trên màn hình nhóm đúng kiểu "1 000", "10 000 000", "2 000 000" ở mọi khung đã xem; dòng đầu ra của mã giữ nguyên thô (`1500000`, `3150000`), phù hợp với màn hình lệnh. Lời đọc có 0 chữ số: mọi số được viết thành chữ ("hai trăm năm mươi sáu", "một triệu năm trăm nghìn"), nên TTS không phải đoán cách đọc.
- Ký hiệu, chữ Latin: tên tệp/lệnh được đánh vần theo kiểu Việt ("sao chấm t x t", "kiem chấm s h", "c bốn và tám ba", "e x e", "chấm g i t"); các chữ viết tắt SQL, HTTP, JSON, YAML còn nguyên Latin trong lời đọc (SQL ×15, JSON ×23, YAML ×9, HTTP ×5) và chỉ nghe được qua từ điển phát âm (ghi chú ASR của L00 tự đánh dấu NOT_VERIFIED bằng tai người), cần tai người nghe lại. Lời đọc không bao giờ nói tên Python/Java/Git/sqlite ("ngôn ngữ thứ hai của khoá", "công cụ ghi lại phiên bản", "chương trình cơ sở dữ liệu nhỏ"), nên người chỉ nghe không biết cài cái gì ở L00 (màn hình có tên). L04 đọc lệnh `cat` thành "cát" ("tên cát", "giả cát"), dễ nhầm với danh từ "cát" (sỏi cát).
- Độ dài câu: 1 573 câu, trung bình 14–17 từ; 70 câu dài từ 30 từ trở lên (L00 15, L04 8, L05 8, L08 8, L07 6, L10 6), dài nhất 38 từ (L04, câu về quyền chạy `chmod`). Câu rất ngắn (≤ 3 từ) chỉ 4 câu ("Ba dấu cuối.", "Ta được năm.", "Bước ba, chốt.", "Chốt ba lần.") nên không có hiện tượng đọc cụt.

## 9. Nhận xét chung
- Điểm mạnh nhất: kiểm bằng hai đường (đếm hai cách, tổng hai cách) ở mọi bài, số liệu quy mô ở 2–3 mức (hơi xa nhưng rất đúng nghề: đường dẫn 260 ký tự, tệp 3/300/3 000, xác suất 63,2%, người phục vụ 1/100/10 000, tìm nhị phân 3/10/17), và lab khớp 11/11 với màn hình.
- Số liệu và mã rất sạch: 125 số khớp tuyệt đối, kể cả băm blob của git và kích thước byte của dữ liệu sinh; không phát hiện kiến thức sai (MUST 0).
- Điểm yếu P1 nằm ở mảng lệnh phụ trợ chỉ dùng để sinh dữ liệu hoặc kiểm (sed ở L05/L08, awk ở L10, printf ở L00, `&&` ở L02, `-q`/`$HOME` ở L04); mỗi chỗ sửa bằng một câu giảng hoặc bỏ lệnh khỏi màn hình, nên đưa P1 lên 2 gần như tức thì (6 bài, ~10 câu).
- Sửa trước tiên: L10 (so_tay.db hai cảnh mâu thuẫn), L09 (` M a.txt`), L07 ("vài phần giây" so với `sleep 1`), L04 (nội dung a.txt), L06 (lệnh sinh a10k). Đây là các ca "ví dụ không tự đứng", dễ làm người mất gốc nghi ngờ mình gõ sai.
- Rủi ro môi trường cho người học: `sqlite3` là cổng bắt buộc của L08 và L10, nhưng L00 chỉ kiểm bằng `kiem.sh` (đã cài thì ✔). Máy kiểm của kho hiện chưa có sqlite3 nên lab L10 chưa chạy được trên CLI thật trong phiên này. Nên có một lượt chạy thật L08/L10 sau khi cài sqlite3.
- Tai người vẫn là việc mở: các chữ viết tắt Latin và "cát" ở L04 cần nghe thật; phần ASR ghi NOT_VERIFIED bằng tai người cho L00.
