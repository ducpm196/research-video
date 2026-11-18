# R6 FND (vòng 6, đọc độc lập bản dựng sau lần sửa thứ hai, P1 chặt): 11/11 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a4b1c153ddb84a6a5)

## 1. Tóm tắt (vòng 4: P1=2 2/11 → vòng 5: 7/11 → vòng 6: 10/11 chắc+vvừa)
MUST 0 (11/11). P1=2: 10/11 chắc+vừa (L09 = 1) — ĐẠT ngưỡng ≥ 90% (91%); tính cả yếu 6/11 (L00, L01, L02, L03, L06, L07; L04, L05, L08 = 1; L09, L10 = 0). P8=2 11/11; P9=2 11/11; spec khớp 11/11; SRT khớp 11/11 (1 619 câu); lab ĐÚNG 11/11 (L08 qua shim sqlite3; L07 cổng cục bộ 18766). 72/72 số tính lại khớp; ~170 lệnh chạy lại khớp; `rm * .txt` không chạy (an toàn), kiểm bằng `echo`. SHOULD 10. Mất gốc ĐỦ 11/11 (L09, L10 GẦN nếu tính cả yếu). P3=1 ở L00, L05, L07, L08, L09, L10 (cột đầu bảng gãy dòng); P7=1 ở L00 (lệch "bốn/năm bước").
Không có mục "chắc". Mục vừa còn lại: L09 pitfalls#0 `git commit -q -m 'quen add' > /dev/null; echo "ma thoat: $?"` (`> /dev/null`, giảng ở L03 sym#2, L04 prereq, L07 prereq, bài này không nhắc; B vừa).

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L00 | kiemsh#2,#3,#4 (bảng "phần của tệp") | `… | grep -oE '[0-9.]+' | head -1`; `"$1" --version 2>/dev/null`; `printf '%s\n%s\n' "$2" "$v"` | cột đầu gãy 2–3 dòng (khung 128, 132) | mở rộng cột đầu hoặc `white-space: nowrap` | CONFIRMED |
| L00 | objectives; hoc#0 (P7) | "Kể bốn bước của vòng học" | cảnh hoc#0 vẽ và đọc NĂM bước (xem, tự làm, chấm, đánh dấu, ôn); recap chỉ nêu bốn động từ | đổi mục tiêu thành "năm bước" hoặc gộp "đánh dấu" | CONFIRMED |
| L02 | pitfalls#2 | tiêu đề `rm -rf "$DIR"/*`; ghi chú `"$DIR/"` thành `/` | lệnh thật mở ra `/*` (các mục ngay dưới gốc), không phải `/`; `echo "$DIR"/*` ra `/bin /cmd /dev …`; hệ quả vẫn nhắm vào gốc | demo bằng `echo "$DIR"/*` | CONFIRMED (chi tiết nhỏ) |
| L05 | example#0, #1 (hai bảng "viết trong mã Java → đọc là") | `public static void main(String[] args) { … }`; `System.out.println("Chao ban");` | cột đầu gãy dòng sau "void" và giữa "Chao / ban" (khung 52, 54, 58) | như L00 | CONFIRMED |
| L06 | intuition#0 | "Ba dạng chứa cùng thông tin, chỉ khác cách trình bày" | hình rút gọn: JSON thiếu `gia`, YAML thiếu `gia` và mặt hàng thứ hai, CSV không có `ma` → hình không khớp lời "cùng thông tin" | vẽ đủ trường hoặc ghi "(rút gọn)" | CONFIRMED (khung 24 + SVG) |
| L07 | sym#1 | `-o /dev/null -w "%{http_code}\n"` | cột đầu gãy NGAY TRONG chuỗi: `"%` dòng trên, `{http_code}\n"` dòng dưới (khung 21) | như L00 | CONFIRMED |
| L08 | sym#2 | `SELECT cột FROM bảng WHERE điều_kiện`; `UPDATE … SET … WHERE` và `DELETE FROM … WHERE` | cột đầu gãy 2 dòng (khung 22) | như L00 | CONFIRMED |
| L09 | sym#1; practice#0 | `git diff và git log --format=%s` (gãy sau `--`); `git branch --show-` / `current` | gãy giữa tuỳ chọn (khung 19, 124) | như L00 | CONFIRMED |
| L10 | sym#1 | `CASE WHEN điều_kiện THEN a ELSE b END`; `.import --csv --skip 1 f.csv bang` | cột đầu gãy 2 dòng (khung 21) | như L00 | CONFIRMED |
| Cả khoá | ghi chú xám `.note` ngoài tiêu điểm | L10 khung 111 "Trong SQL, dấu <> nghĩa là khác…"; L00 khung 63; L05 khung 1 | đo điểm ảnh: #868c94 trên #fff7e6 = 3,18:1 (CSS `.note` muted chồng `.dim` độ mờ .66); chữ ~32 px qua ngưỡng chữ lớn 3:1, không qua 4,5:1; chữ mờ thường đo 4,7–4,8:1; ghi chú mang nội dung dạy | không áp `.dim` lên `.note`, hoặc tối màu muted | CONFIRMED (đo điểm ảnh) |
Không kết luận sai: MAX_PATH 260 (L01) và Little 1961 (L07) NOT_VERIFIED trong `source`; Roediger & Karpicke 2006 (L00) khớp tóm tắt.

## 3. Mục chưa giảng (11 mục, 0 chắc, 1 vừa, 10 yếu)
1. L04 check#0 "Hỏi bằng command -v (và type -t, which cho cùng ý)" (A yếu).
2. L05 example#0, #8, pitfalls `public static void main(String[] args) { … }` (`public`, `static`, `void`, `String[]`) (A+M yếu; bảng "viết trong mã Java → đọc là" có: "khung bắt buộc… cứ chép nguyên"; `args` được giải).
3. L05 scale#0 `echo 'ERROR mat ket noi' >> app.log` (`>>`; B yếu; L02 sym, L03 prereq).
4. L08 example#1 `sqlite3 $DB "UPDATE … SET ten = 'An Le' …"`: nháy kép ngoài, nháy đơn trong (A yếu).
5. L09 example#1 `git log --format='%h %s'` (`%h`; A yếu — suy ra từ đầu ra; hàng bảng chỉ giải `%s`).
6. L09 check#0 `git log --format=%s | wc -l` (`wc -l`; B yếu; L02, L03).
7. L09 pitfalls#0 `git commit -q -m 'quen add' > /dev/null; echo "ma thoat: $?"` (`> /dev/null`; B VỪA).
8. L10 example#2, #3 `head -n 7 bao_cao.txt`, `tail -n 7 bao_cao.txt` (B yếu; L03).
9. L10 example#4, pitfalls#0 `git init -q`, `git status -s`, các dòng `??` (B yếu; L09).
10. L10 example#5 `git log --format=%s`, `-q`, `-m` (B yếu; L09).
11. L10 formula#2, #3 awk `s += $4` với `s` chưa gán (mặc định 0) (A yếu; dòng "s += 5 là s tăng thêm 5", không nói giá trị đầu).
Số mục theo bài (cả yếu): L04 1, L05 2, L08 1, L09 3, L10 4, còn lại 0.
Bảng phụ, KHÔNG tính vào P1: lệnh nền (L00–L02) dùng lại ở bài sau mà prereq không nhắc: L03 `echo`; L04 `mkdir`, `ls`; L05 `ls`, `bash`, `echo`; L07 `python <tệp>`; L09 `touch`; L10 `bash`, `cd`, `cp`, `wc -c`/`wc -l`.
Ngoài tính điểm: L05 practice `java Tong` chỉ có ở de.md; L07 practice 45 dòng Python `may_chu.py` không hiện (đề dặn "chép đúng, chưa cần hiểu").

## 4. Chữ "Python" và âm thanh
SRT viết nguyên "Python" (L00 khung 93, 111; L05 khung 70; L06 khung 1, 42, 84); văn bản gửi TTS qua lexicon là "Pai-thon" (JSON → "Giây-sơn", YAML → "Giam-mồ"); ASR chép "hai thông / phai thông / Pai Thông" — gần đúng, CHƯA kiểm bằng tai người. Tên lệnh khác đọc tách chữ: "b a s h", "e c h o", "e x e", "m s i", "L T S". Lời đọc tránh nói "Git" (nói "công cụ ghi phiên bản"). ASR còn 13 câu gắn cờ chưa xem xét: L00 2, L01 1, L03 1, L04 1, L05 5, L07 2, L09 1.

## 5. Người học kẹt ở đâu
Không bài nào kẹt thật. Nhẹ: L00 kiemsh#2–#4 (ba bảng liền, đã dặn "chưa hiểu hết cũng đừng lo"); L04 check#0 `type -t`, `which`; L05 example#0 `public static void main(String[] args)` (cứ chép), scale#0 `>>`; L08 example#1 nháy kép ngoài; L09 pitfalls#0 `> /dev/null`; L10 example#4 `git init -q`, `git status -s`.
