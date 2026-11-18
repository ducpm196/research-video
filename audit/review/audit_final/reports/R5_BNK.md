# R5 BNK (vòng 5, đọc độc lập bản dựng sau sửa, P1 chặt): 15/15 bài — ghi lại bởi người điều phối từ tin nhắn của reader (aabd0b490bb16bc1c)

Lưu ý reader: `bash labs/cham.sh` bị classifier chặn (nghi `rm -rf` trong trap); reader chạy tương đương trong scratchpad (biên dịch/chạy loi_giai.* rồi so mong_doi.txt sau khi bỏ khoảng trắng cuối dòng; SQL qua `labs/sqlrun.py`). Khối PL/SQL Oracle (L05) chỉ đọc.

## 1. Tóm tắt (so với vòng 4: P1=2 3/15 → 7/15 chắc+vừa)
MUST 0 (15/15). SHOULD 9. P1=2 (chắc+vừa): 7/15 (L02, L05, L09, L11, L12, L13, L14); 8 bài P1=1; 0 bài P1=0. P1=2 tính cả yếu: 0/15 (3 bài P1=1: L09, L12, L14; 12 bài P1=0). Số mục chưa giảng: 10 chắc/vừa + 60 yếu = 70. P8=2 15/15; P9=2 15/15; spec khớp 15/15; SRT khớp 15/15 (2158/2158 câu); lab 15/15 khớp mong_doi (L03 chạy máy chủ cục bộ cổng 8099 + 6 lệnh curl). ~40 chương trình/SQL chạy, ~100 số tính lại, 0 lệch. Bảng cách đọc Java mới (JROW/jstep) KHÔNG tràn/đè/cắt (đã xem L00 khung 72, L01 53, L02 33, L03 48, L05 63, L06 59, L07 57, L08 60, L10 57, L11 14/19, L13 21/74).
Tái kiểm yêu cầu: L08 chạy trên bảng mới ra 1500000/0 (ghi kép), 2000000/0 (ROLLBACK), Outbox 1500000 và `lenh 42 da tru 500000|0` — khớp màn hình/lời đọc; L09 cảnh check (khung 71) hiện `UPDATE but_toan SET tien = 90 WHERE gd = 1 AND tk = 'b';` + chú giải + lời đọc; `HAVING SUM(tien) <> 0` ra giao dịch 1 (tổng −10), giao dịch 2 tổng 0.
Gốc P1 còn lại: bảng cách đọc Java chỉ có ba kiểu — khai hàm (L00–L03, L05, L06, L10), `a[i]`/`a.length` (L08, L10), `p++` (L07). Các cấu trúc điều khiển (`if`, `for`, `while`, `++`, `+=`, `return`, `//` chú thích, `String[] args`) hầu như không có hàng riêng (giảng trong lời ở L07, L08, L10, không có trong bảng). Python (L11–L13) và SQL (prereq L04, L09, L14) phủ gần hết, mục còn lại toàn yếu; SQL không có bảng dạng JROW.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L01 | prereq s1 | "throws Exception cho phép bỏ qua các lỗi bất thường" | `throws` chuyển lỗi lên người gọi, không "bỏ qua"; bảng L05 nói đúng hơn | sửa lời cho khớp L05 | PLAUSIBLE |
| L01, L02, L03 | quy_mo | ô "×10 000" ngắt dòng giữa hai nhóm số (khung 116/117/107) | hiển thị | mở rộng cột đầu / nowrap (dùng `libj.nowrap` hoặc tương đương của BNK) | CONFIRMED |
| L02 | chay_that s2 khung 80 | `Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },` | dòng chạy tới x≈1890/1920, vượt viền khung mã (≈1830), không bị cắt | ngắt dòng | CONFIRMED |
| L03 | check s0 | "bảng có ràng buộc UNIQUE" | mã dùng `PRIMARY KEY`, lời nói "khoá chính" | đồng nhất chữ | CONFIRMED |
| L09 | check s0 | "Bảng thử khác … giao dịch 1 gồm −100 và +100" | `CREATE`/`INSERT` của bảng thử không hiện, chỉ mô tả bằng lời | hiện hai lệnh dựng bảng | CONFIRMED |
| L13 | intuition s0 khung 32 | "TPK … ZPK … ZMK … LMK" | chú thích cỡ ≈20 px, lời đọc không đọc tới | đọc hoặc phóng to | CONFIRMED |
| L14 | prereq s1 khung 15 | ô "nghĩa" gồm 6 cú pháp SQL trong một đoạn | khó theo hơn bảng một hàng một cú pháp | tách nhiều hàng | PLAUSIBLE |
| L01, L04 | practice s2 (L01 khung 132, L04 khung 126) | "…ORDER BY id;; câu thứ hai", "};;," | hai dấu chấm phẩy liền nhau | bỏ dấu thừa | CONFIRMED |
| L04, L08 | L04 khung 55; L08 khung 71 | `WITH RECURSIVE … UNION ALL` (L04), `DEFAULT` (L08) | không tô màu từ khoá như các từ khoá khác | bổ sung bộ tô màu | CONFIRMED |
Pháp lý: L13 giữ nhãn CHƯA KIỂM (khung 48); TT 50/2024 (hiệu lực 01/01/2025; ngưỡng trên 10 triệu một lần hoặc trên 20 triệu một ngày cần sinh trắc học) khớp hiểu biết của reader; TT 77/2025, mốc 01/03/2026 và 01/07/2026, "Phụ lục 01", "Oracle 26ai Free" (L05): chưa kiểm được nguồn.

## 3. Mục chưa giảng chắc/vừa (10) và nhóm yếu
Chắc/vừa:
- L00 chay_that s0 `public static void main(String[] args)` (M vừa; bảng khai hàm ở s2, SAU lần dùng đầu; không phủ `String[] args`).
- L01 chay_that s8 `for (int i = 0; i < 10_000; i++)` (B vừa; không nhắc lại); L01 quy_mo s0 "ngăn xếp mỗi luồng nền" (B vừa).
- L03 chay_that s1 `ex.getResponseBody().write(s.getBytes());` (M vừa; lời chỉ nói "hàm trả viết phản hồi").
- L04 chay_that s0 `WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 5000)` (M vừa; chỉ mô tả cả dòng).
- L06 chay_that s2 `for (int i = 0; i < 100; i++) soDu(i % 10);` (B vừa).
- L07 chay_that s4–s5 `int[] dem = new int[5];`, `dem[m]++;` (A vừa; mảng/chỉ số chỉ giảng từ L08).
- L08 chay_that s1 `public static void main(String[] args)` (B vừa; L08 không có bảng khai hàm).
- L10 chay_that s1 `public static void main(String[] args)` (M vừa; bảng khai hàm ở s4, sau s1); chay_that s2, s5 `theoThuTu++`, `n++` (B vừa; L07 giảng `p++`).
Yếu (60), nhóm: `//` chú thích Java (L00–L03, L05–L08, L10); `String[] args`; `null`/`<>`/`new HashMap<>()`/`WeakReference<Object>`; `+=`, `++`, `i++`, `tong++`, `trung++`; `if (…) { … } else { … }`, `if (duoc) sau.unlock();`, `return duoc;`/`return false;`, `if (i == loi)`; `main(String[] args) throws Exception` (một phần bảng ⑥); `System.nanoTime()`, `Thread[] ds = { … }`; `return m.invoke(that, a);`, `Dich.class`, "CGLIB"; kiểu cột `TEXT`/`INTEGER` (L03, L04, L08, L09, L14); `-- …` chú thích SQL (L05, L08); `INSERT … VALUES (…), (…)` nhiều bộ (L09, L14); "COVERING INDEX" (L04 lời không nói); Python (L11) `bit = 0`, `bando = "%016X" % bit`, `truong[2]`, `int(tin[vi_tri:vi_tri + 2])`, `#`, "ASCII"; L12 `ngan_hang = {…}` (`=`); L13 `pin, pan = "1234", "4111111111111111"`, `b"k"`, `#`, TPK/ZPK/ZMK/LMK, TDES/AES, `"".join("%X" % (…) for x, y in zip(a, b))`.
Đề xuất của reader: thêm một bảng cách đọc `for/if/++/+=/return/mảng/null/<>/String[] args/chú thích //` ở bài Java đầu tiên dùng chúng (L00) và nhắc lại hàng cần thiết ở bài dùng lại (L01, L06, L07, L08, L10); bảng "khai hàm" đứng trước lần dùng đầu ở L00/L10; SQL: bảng `TEXT`/`INTEGER`/`VALUES (…),(…)`/`--`/`WITH RECURSIVE` ở bài đầu tiên dùng và nhắc lại.

## 4. Người học kẹt ở đâu
L00 chay_that s0 `WeakReference<Object> yeu = new WeakReference<>(tk); … (yeu.get() != null)`; L01 chay_that s8 `for (int i = 0; i < 10_000; i++) ex.submit(() -> { Thread.sleep(100); return xong.incrementAndGet(); });`; L02 nặng nhất chay_that s2 `(p, m, a) -> { moGiaoDich++; … return m.invoke(that, a); }` (dòng tạo proxy rất dài); L03 chay_that s1 `ex.getResponseBody().write(s.getBytes());`; L04 chay_that s0 `WITH RECURSIVE …`; L05 không kẹt; L06 chay_that s2 `for (int i = 0; i < 100; i++) soDu(i % 10);`; L07 chay_that s4 `int[] dem = new int[5]; … dem[m]++;`; L08 chay_that s1 `List<String> nhatKy = new ArrayList<>(); … if (i == loi) {`; L09 không kẹt; L10 chay_that s2 `if (cho.get("M" + k).equals(viec)) theoThuTu++;`; L11 chay_that s1 `tin = "0200" + bando + "16" + truong[2] + …`; L12 không kẹt; L13 intuition s0 TPK/ZPK/ZMK/LMK (chỉ chữ); L14 không kẹt.
