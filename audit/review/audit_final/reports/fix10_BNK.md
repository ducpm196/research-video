# fix10 BNK (vòng sửa cuối theo R7_BNK) — 2026-11-17

Nguồn: `audit/bnk/lib.py` (thêm hàng `nano`, `thread`, `sb`, `base`, `pyeq`; khung nhấn L12/L13 không bọc tiêu đề "Kết quả chạy thật"), `audit/bnk/src/l01,l02,l05,l06,l07,l08,l10,l11,l13.py`; sinh lại bằng `gen.py` (L12 sinh lại do đổi `focus`).

## 1. 7 mục vừa
- L01: hàng `System.nanoTime()` / `/ 1_000_000` (đồng hồ chính xác tính bằng nano giây; chia 1 triệu ra mili giây), trước LuongAo.
- L05: hàng `t1.start(); t2.start(); t1.join(); t2.join();` (start cho luồng chạy; join chờ luồng đó xong), trước phần 3 của BeTac.
- L07: hàng `StringBuilder sb = new StringBuilder(…)` / `sb.append(…)` (hộp chữ nối được; append thêm vào cuối), thay hàng nối chuỗi cũ.
- L08: hàng `for (int loi = 0; loi < 3; loi++)`; `PRIMARY KEY` có một vế ("cột khoá chính là cột không cho hai dòng trùng") ở hàng `TEXT/INTEGER`.
- L13: "API" đọc kèm vế "cửa để chương trình khác gọi vào" (pitfalls.2); "TDES/AES" đọc "hai thuật toán mã hoá chuẩn; TDES cũ hơn, AES mới hơn" (formula.0).

## 2. Yếu nhóm B và khác
- Hàng 'nhắc lại cú pháp Java nền' (`import`, `System.out.println`, `return`, `//`, `+` nối chữ): L05 (trước mã BeTac) và L08 (thay hàng nối chuỗi); L06, L07, L10 chưa thêm (hết ngân sách chữ).
- L11: "các dòng thụt vào sau dấu hai chấm là việc làm mỗi vòng" (hàng ⑥ và lời đọc). L13: hàng `==` và `#`.

## 3. SHOULD
L02 ô "thiếu: có thể kẹt"; L06 xoá ", ." thừa ở intuition.1 và chay_that.4; L10 dời nhãn "tương quan = M7" sang (1100, 325); L12 chay_that.1 và L13 chay_that.5 (khối mã + kết quả): khung nhấn bọc khối kết quả (`focus` 4), không bọc tiêu đề.

## 4. Lời đọc (đếm bằng mã, ≤ 2300)
L00 2295; L01 2299; L02 2295; L03 2295; L04 2208; L05 2291; L06 2295; L07 2289; L08 2287; L09 2217; L10 2298; L11 2299; L12 2217; L13 2294; L14 2296.

## 5. Cổng
lint 0/0 từng bài; bảng cách đọc ≤ 3 hàng/≤ 560 ký tự, step sau bảng `clear`; verify_bnk, screen_gen + screen_code, curriculum, test_e52: xem tin nhắn cuối. `lv.py render` thử khi chạy xong cổng.

## 6. Requeue
L01, L05, L06, L07, L08, L10, L11, L12, L13 và L02 (một ô bảng). L00, L03, L04, L09, L14 không đổi so với vòng 9.

## 7. Kết quả cổng (đã chạy)
lint 15/15: 0 FAIL, 0 WARN; verify_bnk 48/48; screen_gen rồi screen_code BNK: 107 khối, PASS 156, FAIL 0, STALE 0; curriculum 15 bài, 0 lỗi; test_e52: 0 FAIL; bảng cách đọc: không bảng > 3 hàng, step sau bảng đều `clear`. `lv.py render` L05: 136 khung, 0 vấn đề; L13 và các bài khác: lần gọi render bị từ chối quyền nên không đi vòng (xem khi dựng: L13 chay_that khung kết quả, L10 nhãn mới, L12 khung nhấn).
