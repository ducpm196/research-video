# Báo cáo JVA (13 bài L00–L12) nâng lên chuẩn AF2 — 2026-11-13

Máy: Git Bash, JDK 21.0.13 (Temurin), Python 3.13. Bộ sinh: `audit/jva` (`src/lNN.py` → `gen.py`), cổng mỗi bài: `bash audit/jva/gates.sh Lxx` (verify → gen → lint → số phút → render → lab_gate; thêm `SC=1` cho screen_code).
Số phút = từ lời đọc / 176 từ mỗi phút (tốc độ đo ở bản dựng cũ của L00: 1 477 từ → 522,8 s gồm 20 s dừng) + tổng giây `pause`. **Ước lượng**, chưa dựng (không chạy build/tts).

| Bài | verify_jva (chạy thật JDK 21) | lint | render | lab_gate | từ lời đọc | phút ước | Ghi chú nội dung thêm |
|---|---|---|---|---|---|---|---|
| L00 | 9/9 | 0 FAIL 0 WARN | 0 vấn đề | PASS | 2 451 | 15,5 | Git Bash (`mkdir -p`, `cd`, `pwd`, `ls`), giảng `public static void main(String[] args)`, `System.out.println`, `//`; cảnh đọc lỗi biên dịch thật (thiếu `;`, sai chính tả: dòng, dấu mũ, gợi ý); lỗi đứng sai thư mục; P9: lô 10 / 1 000 / 1 000 000 lệnh, lỗi chạy dở; lab PhieuSo |
| L01 | 11/11 | 0/0 | 0 | PASS | 2 192 | 14,1 | `jshell` tự đoán rồi kiểm; P9: lô 100 / 2 147 / 2 148 / 10 000 lệnh một triệu đồng, int tràn ra số âm rồi ra số dương trông hợp lý; lab SoDu |
| L02 | 13/13 | 0/0 | 0 | PASS | 1 961 | 12,8 | `jshell` đoán chia/dư/ngắn mạch; P9: phần lẻ 835 phần nghìn đồng × 1 / 1 000 / 10^6 lệnh / 365 ngày = 304 775 000 đồng; lab ChiaHoaDon |
| L03 | 14/14 | 0/0 | 0 | PASS | 2 034 | 12,9 | `args` (`args.length`, `args[0]`, `Long.parseLong`), `Scanner(System.in)` + `import`, ống `echo … \| java`; P9: số ca thử ở biên 6/27/297, tổ hợp 2^n; lab BacLai |
| L04 | 13/13 | 0/0 | 0 | PASS | 2 001 | 13,2 | giữ lời hứa của L00 về `args`: vòng lặp qua `args`, `while (in.hasNextLong())` đọc tới hết dữ liệu; P9: lãi 12/120/360 tháng, lệch 5/81/509 đồng; lab TietKiem (đã có) |
| L05 | 10/10 | 0/0 | 0 | PASS | 1 714 | 11,1 | P9: duyệt từng ô 5 / 5 000 / 5 000 000 bước, 80 MB mảng 10 triệu `long`; lab SauTaiKhoan |
| L06 | 11/11 | 0/0 | 0 | PASS | 1 775 | 11,4 | (giảng `static`: giữ lời hứa của L00); P9: xác suất sửa đúng hết 98 % mỗi chỗ → 980/817/132 phần nghìn ở 1/10/100 chỗ; lab RutATM |
| L07 | 8/8 | 0/0 | 0 | PASS | 1 794 | 11,5 | thuật ngữ cố định "hàm tạo", "từ khoá `this`"; P9: số chỗ phải rà với trường `public` vs `private`; lab QuanLyVi |
| L08 | 12/12 | 0/0 | 0 | PASS | 1 948 | 12,4 | `Files.writeString/readString`, `new String[2]`, `throws Exception`; P9: 19 byte/dòng → 19 KB / 19 MB / 1,9 GB; lab DoiSoat |
| L09 | 13/13 | 0/0 | 0 | PASS | 2 065 | 13,1 | "kiểu tổng quát" `<…>` giải bằng một câu; thêm ví dụ tra cứu `containsKey`; lambda `forEach`, `sort` bằng bộ so sánh (đọc hiểu); P9: danh sách 1 000 / 1 000 000 bước vs bản đồ cỡ 1 bước; lab ThongKe |
| L10 | 13/13 | 0/0 | 0 | PASS | 2 134 | 13,5 | hook sửa: bản rút gọn `TaiKhoan(long)` nói rõ khác hàm tạo L07; `Thread` hai luồng + `join` (không khoá); P9: khối bắt rỗng nuốt 1/100/1 000 lỗi; lab RutHanMuc |
| L11 | 9/9 | 0/0 | 0 | PASS | 2 018 | 12,8 | thuật ngữ cố định "nhãn (annotation)" (thay "chú thích ghi đè"), cảnh nhãn: `@Override`, `@FunctionalInterface` (lỗi biên dịch thật), nhãn Spring/JUnit chỉ nêu; P9: thêm loại phí 7 × 20 = 140 vs 7 lớp; lab LaiSuatLab |
| L12 | 7/7 | 0/0 | 0 | PASS | 2 267 | 14,7 | toàn bộ tệp `So.java` hiện trong 7 khung; P9: kiểm tổng sau mỗi lệnh = N × M (12 → 10^6 → 10^8 → 10^12), kiểm gia tăng, vì sao cần cơ sở dữ liệu; lab dựng sổ qua 3 mốc (SoCaiLab) |

Toàn khoá (lượt chạy cuối): `verify_jva.py` = 143/143 PASS (javac/java 21.0.13); `lv.py lint` 13 bài đều 0 FAIL 0 WARN.
Cổng phần JVA: `lab_gate.py JVA` = 13 PASS · 0 FAIL (49 lab của mọi khoá được bài tham chiếu); `screen_code.py check --course jva`: 372 khối, PASS 515 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
Mọi bài khai `af2: true`, có `covers` cho từng mục tiêu, một cảnh `practice` (lab có `de.md`, `mong_doi.txt`, `loi_giai.java`) và một cảnh P9 (`quymo`, kiểu `concept`).

## Việc đã làm ngoài các bài
- `audit/jva/lib.py`: `prog(..., stdin=)` → chương trình đọc bàn phím nằm ở `PROGRAMS_IO` (verify_jva chạy với `stdin`; `screen_code` chạy không có `stdin` nên không thấy chúng).
- `audit/jva/verify_jva.py`: biên dịch bằng tên tệp tương đối trong thư mục tạm (javac in `Thieu.java:3: error:` đúng như người học thấy); chạy `java` trong thư mục tạm (chương trình ghi tệp không làm bẩn kho); chạy cả `PROGRAMS_IO`.
- `audit/jva/screen_hand.py` (mới): sau `gen-jva` điền sổ `audit/review/screen_code/JVA.yaml` cho khối không phải Java (lệnh Git Bash chạy thật bằng `run`/bash kèm `files`, thông báo javac nhiều dòng, phiên `jshell`, khối của chương trình `stdin`).
- `audit/jva/gates.sh` (mới), `audit/jva/gen_curriculum.py` chạy lại → `curriculum/jva.yaml` (mục tiêu mới, giữ id/requires).
- 13 thư mục `labs/JVA/Lxx/`.
- `audit/review/audit_final/reports/jva_gaps.md`: các mục chưa nhét được.

## Mục chưa làm / lưu ý
- Chưa dựng video, chưa nghe thử; số phút chỉ là ước lượng theo từ. L00 (15,5) và L12 (14,7) gần trần 16 phút.
- Không ASR/TTS: lời đọc chỉ dùng từ tiếng Việt (tên lệnh như `jshell`, `cd`, `Git Bash`, `Thread`, `lambda`, `Comparator`, `annotation` chỉ hiện trên màn hình, chưa dò phát âm).
- Lời đọc dùng "chữ a còng" cho `@`; "ống" cho `|`; chưa dò bằng ASR.
- `README` bài mẫu L04 giữ nguyên lab TietKiem đã có; mục tiêu 5–6 của L04 là phần mới.
- Cổng `check_xref.py`, `audit_all.py`, `final_gates.sh` chưa chạy (ngoài phạm vi phiên).
