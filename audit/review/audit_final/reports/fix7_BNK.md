# fix7 BNK (sửa vòng 7 theo R5_BNK) — 2026-11-17

Nguồn sửa: `audit/bnk/lib.py` (thêm hàng cho JROW, `jstep` nhận ví dụ lời đọc tuỳ chọn, ô tải "×…" không ngắt dòng, tô màu thêm từ khoá SQL, tự đặt `clear` cho step sau bảng) và `audit/bnk/src/l00..l14.py`; sinh lại bằng `gen.py`. Không sửa YAML sinh ra.

## 1. Hàng cách đọc mới (khuôn "viết trong mã → đọc là → ví dụ", ≤ 4 hàng mỗi step, step sau bảng `clear: true`)
Java: `main` (có `String[] args`), `cmt` (`//`), `incr` (`++`, `+=`), `for`, `if/else`, `ret` (`return`), `arr` (`int[] dem = new int[5]`/`dem[m]++`), `null`/`<>`, `write` (getResponseBody().write(s.getBytes())). SQL: `sqltype` (TEXT/INTEGER), `values` (nhiều cặp ngoặc), `sqlcmt` (`--`), `recursive` (WITH RECURSIVE … UNION ALL), `count`.
| Bài | Hàng thêm / việc |
|---|---|
| L00 | bảng `//`, `null`/`<>`/`!=`, `+=`/`++` đặt TRƯỚC chương trình đầu; hàng `main` có thêm `String[] args` (ở bảng khung tệp, trước mọi mã); `return` kèm `dungMB` |
| L01 | `for (int i = 0; i < 10_000; i++)`, `return`, `//` trước LuongAo; "ngăn xếp" định nghĩa tại chỗ; `throws` sửa thành "chuyển lỗi lên cho nơi gọi xử lý" (khớp bảng L05) |
| L02 | `moGiaoDich++`, `return m.invoke…`, `//`; ngắt dòng `Dich proxy = (Dich) Proxy.newProxyInstance(` (mã + lab) |
| L03 | `ex.getResponseBody().write(s.getBytes())`, `//`; `TEXT`; "UNIQUE" → khoá chính (`PRIMARY KEY`, một loại ràng buộc duy nhất) |
| L04 | `WITH RECURSIVE n(i) AS (…)`, `INTEGER`; câu "bao phủ" cho `COVERING INDEX`; bỏ dấu `;` thừa ở gợi ý Tự làm |
| L06 | `for (int i = 0; i < 100; i++) soDu(i % 10);`, `if (boDem.containsKey(tk))`, `trung++`/`tong += 1` |
| L07 | `main`, `for`, `//` (trước `p++`); `int[] dem = new int[5]`/`dem[m]++`, `if (ghiNhoTruoc) … else …` |
| L08 | `main`, `if (i == loi)`, `new ArrayList<>()`; `TEXT/INTEGER`, `--`, `DEFAULT`, `COUNT`; tô màu `RECURSIVE`/`DEFAULT`… |
| L09 | hàng `TEXT/INTEGER`, `VALUES (…), (…)`, `COUNT(*)`; cảnh check hiện hai lệnh dựng bảng thử (CREATE + INSERT) trước lệnh UPDATE |
| L10 | `main`, `for (… ve.length …)`, `if (…) theoThuTu++` (trước mã đầu), `n++` (kèm `soLanGhiNo`) |
| L13 | một câu đọc TPK/ZPK/ZMK/LMK + phóng chữ chú thích hình (22 → 26) |
| L14 | ô SQL một đoạn → hai bảng mỗi hàng một cú pháp (TEXT/INTEGER, VALUES nhiều cặp, SELECT, SUM; NOT IN, INSERT … SELECT, `||`) |
| L01, L04 | bỏ `;;`; ô "×10 000" (tất cả bài) bọc nowrap tự động trong `lib.table` |
L05, L11, L12: không đổi nội dung (L05 chỉ rút một câu để bù chữ `throws` mới dài hơn). Python (L11–L13) giữ nguyên ngoài L13.

## 2. Lời đọc ≤ 2300 (đếm bằng mã)
L00 2298; L01 2297; L02 2291; L03 2292; L04 2196; L05 2298; L06 2300; L07 2295; L08 2294; L09 2198; L10 2299; L11 2291; L12 2217; L13 2290; L14 2296. Đã cắt câu chuyển cảnh ("Bảng này…", "Hình cho thấy…", "Tổng kết chuỗi logic", "Điều cần mang theo"), câu lặp bảng, ví dụ thừa; không bỏ bảng cách đọc, lời giải quiz, cảnh quy mô, Tự làm.

## 3. Cổng
- `tools/lv.py lint` 15/15: 0 FAIL, 0 WARN. `audit/bnk/verify_bnk.py`: 48/48. Giữ kết quả đã kiểm: L08 1500000/0, 2000000/0; L09 (UPDATE → `1`, `1|-10`, `2|0`).
- `screen_gen.py` (công cụ sổ chính thức) rồi `screen_code.py check --course BNK`; curriculum, test_e52: xem tin nhắn cuối.
- Kiểm bằng mã: mọi step ngay sau bảng cách đọc có `clear: true`; không bảng nào > 4 hàng.
- `lv.py render`: bị từ chối quyền khi thử, KHÔNG đi vòng; chưa xem khung. Cần xem khi dựng: bảng 4 hàng ở L00 (đầu chay_that), L03 (đầu chay_that, hàng write), L06, L07, L08 (Saga và SQL), L10; hai bảng L14 prereq; hình L13 (chữ 26).

## 4. Requeue
L00, L01, L02, L03, L04, L06, L07, L08, L09, L10, L13, L14 và L05 (YAML đổi vì hàng `throws` mới); L11, L12 không đổi nội dung.

## 5. Bổ sung: TRÀN khung ở bảng cách đọc (render L03 FAIL khung 48–54)
Nguyên nhân: bảng 4 hàng (~800 ký tự) trong một step, cộng hàng `write` có mã dài không ngắt dòng. Sửa: `lib.jsteps()` tự tách bảng thành nhiều step (≤ 3 hàng, ≤ 520 ký tự chữ mỗi bảng; step sau bảng vẫn `clear`); hàng `write` rút chữ (`….write(s.getBytes())` + `gọi trên ex.getResponseBody()`). Lời đọc không đổi (cùng tổng từ). Render L03 lần thử lại: còn 2 khung (53–54) = đúng step bảng `write`/`//` → đã rút; chưa render lại được (quyền bị từ chối ở lần gọi sau). Kiểm bằng mã: không ô bảng nào có từ liền > 28 ký tự (trừ 2 ô cũ đã dựng OK ở L02/L13).
Bài YAML đổi: L03, L06, L07, L08, L10 (tách bảng); L03 thêm đổi chữ hàng `write`.
