# fix6 BNK (sửa theo R4_BNK, chuẩn P1 chặt) — 2026-11-16

Nguồn sửa: `audit/bnk/lib.py` (thêm khuôn bảng dùng chung `JROW`/`jstep`), `audit/bnk/src/l00..l11,l13.py`, sinh lại bằng `audit/bnk/gen.py`. Không sửa YAML sinh ra, không sửa sổ bằng tay (sổ BNK sinh lại bằng công cụ chính thức `audit/bnk/screen_gen.py`).

## 1. Khuôn bảng "viết trong mã → đọc là → ví dụ"
`lib.jstep([(khoá, ví dụ HTML, ví dụ lời đọc)])` dựng một step bảng ba cột cố định. Hàng dùng chung: `sig` (kiểu trả về, `void`, tên, tham số, `static`, `public`), `final`, `throws`, `cast`, `idx` (`a[i]`, `a.length`), `inc` (`p++`), `call` (đối số, `s.length()`), `default`, `count`, `strmul`, `encode`, `sorted`. Mỗi bài tự đứng (không "như đã học"): bảng đặt ngay trước khối mã đầu tiên dùng ký hiệu, có lời đọc riêng.

## 2. Mục chưa giảng (mục 3 của R4) — đã xử lý hết
| Bài | Việc đã làm |
|---|---|
| L00 | `static long dungMB()` → hàng `sig`; `&&` giảng ở cảnh Tự làm (hình + lời); "số thực nhị phân" định nghĩa tại bảng kiểu số (hệ hai: chỉ 0 và 1, 0,1 chỉ ghi gần đúng) |
| L01 | `static void nap(int tien, int cho)` (`sig`), `static final Object KHOA` (`final`) |
| L02 | `public void chuyenTien()` (`sig`), `(Dich) Proxy.newProxyInstance(…)` (`cast`) |
| L03 | `static void tra(HttpExchange ex, String s) throws IOException` (`sig`), `s.length()`, đối số `0` của `HttpServer.create` (`call`) |
| L04 | `(tk=?)` giải thích ở ghi chú + lời đọc của bước kết quả kế hoạch |
| L05 | `lam(Lock dau, Lock sau)` (`sig`), `thu(…) throws Exception` (`throws`); gợi ý Tự làm giải thích `int[][]`, `for (int[] l : lenh)`, `l[0]`, `l[1]` |
| L06 | `soDu(int tk)`, `ghi(long ma, String v)` (`sig`); `tong / 100.0` (vì sao `.0`) |
| L07 | `chay(boolean ghiNhoTruoc)` (`sig`), `.append(p++)` (`inc`) |
| L08 | `DEFAULT 0` (`default`), `SELECT COUNT(*)` nhắc lại (`count`), `buoc[i]` (`idx`) |
| L10 | `soLanGhiNo(boolean, boolean)` (`sig`), `ve[k]`, `ve.length` (`idx`) |
| L11 | `sorted(truong)` giải thích trong gợi ý Tự làm (hộp + lời) |
| L13 | `"*" * 6` (`strmul`), `.encode()` (`encode`) |
L09, L12, L14: không có mục (R4). Số mục chưa giảng ước còn lại: 0 ở cả 15 bài.

## 3. SHOULD (7)
- L08 dựng lại bảng mỗi kịch bản: ghi kép và huỷ nay hiện ĐỦ mã (CREATE TABLE ×2 …) với tiêu đề "trên bảng mới", mỗi kịch bản một khung mã + một khung kết quả. Số 1500000/0 và 2000000/0 chạy thật bằng sqlite qua `screen_code.py check --course BNK` (nguồn OutboxKep/OutboxHuy, sổ sinh lại): PASS.
- L08 "chưa tính đỉnh tải": thêm vào ghi chú và lời đọc cảnh quy_mo.
- L10 chú thích tràn khung: `// phản hồi: mã + việc` (ngắn hơn ~20 ký tự).
- L10 Temenos T24: kiểm được nguồn (temenos.com/t24: "T24 is now Temenos Transact"; tra 2026-11-16) → hàng sym ghi "Temenos T24 (nay là Temenos Transact)", lời đọc "nay hãng đã đổi tên", nguồn ghi vào `source`.
- L13: GIỮ nhãn CHƯA KIỂM, không đổi số phụ lục (văn bản gốc Thông tư chưa đọc) — việc mở còn lại: kiểm Công báo.
- L05: thêm `SET SERVEROUTPUT ON` vào chương trình Oracle (cả mã trên màn hình + lời đọc). Chạy Docker: không (theo lệnh); công cụ chạy Oracle chính thức vốn tự bật `SERVEROUTPUT`, nên đầu ra mong đợi không đổi.
- L09: cảnh check hiện lệnh `UPDATE but_toan SET tien = 90 WHERE gd = 1 AND tk = 'b';`, nói rõ "bảng thử khác"; thêm nguồn chạy thật `SoCaiLech` (kết quả 1; 1|-10; 2|0).

## 4. Cổng (đã chạy)
- `tools/lv.py lint` từng bài: 15/15 = 0 FAIL, 0 WARN.
- `tools/lv.py curriculum curriculum/bnk.yaml`: 15 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/bnk/verify_bnk.py`: 48/48 PASS (giữ nguyên các cụm câu mà verify khoá: "chín mươi chín phẩy chín mươi lăm", "cả hai trường hợp hỏi trước").
- `audit/bnk/screen_gen.py` (công cụ sổ chính thức) rồi `screen_code.py check --course BNK`: 106 khối, PASS 155, FAIL 0, STALE 0, MISSING 0, ORPHAN 0.
- `audit/review/lab_gate.py BNK`: 15 PASS. `arith_scan.py BNK`: 0 FAIL.
- KHÔNG chạy: build, tts, asr, render, git, docker. Chưa render nên chưa xem được tràn khung của các bảng/khung mới (đáng xem khi dựng lại: bảng L03 chay_that.0, L05 chay_that.4, L08 khung mã đầy đủ ghi kép/huỷ, L09 check.0).

## 5. Lời đọc (từ, `split()` của `say`)
Trước → sau: L00 2395→2395; L01 2370→2377; L02 2304→2315; L03 2260→2329; L04 2116→2131; L05 2382→2422; L06 2313→2332; L07 2301→2307; L08 2308→2353; L09 2077→2145; L10 2280→2318; L11 2326→2337; L12 2217; L13 2361→2404; L14 2328 (không đổi).
Chưa ≤ 2300 (lint không có ngưỡng này): L00, L01, L02, L03, L05, L06, L07, L08, L10, L11, L13, L14 (+L12/L04/L09 đã ≤ 2300). Mức vượt đa phần đã có từ trước (L00, L01, L05, L13, L14). Đã cắt các câu trùng/ít giá trị (lộ trình hook, câu lặp quy_mo, ví dụ thừa) để bù phần thêm; muốn xuống ≤ 2300 hết cần cắt thêm nội dung thật (đề xuất: L05 -120, L13 -100, L00 -95, L08 -55).

## 5b. Bổ sung: cắt về trần ≤ 2300 từ (theo yêu cầu điều phối)
Cắt các câu lặp bảng, câu chuyển cảnh ("Hình cho thấy…", "Bảng này tổng hợp…", "Ta tính…"), ví dụ thừa trong lời đọc, và vài câu trùng giữa các cảnh. Giữ nguyên: mọi bảng cách đọc, mọi lời giải quiz, cảnh quy mô (P9), lời đọc thực nghiệm/Tự làm (P8). Không sửa L12 (2217, đã ≤ 2300). L14 phải cắt nội dung (không phải chỉ gắn nhãn): hook, intuition, example, check, sym.
Số từ cuối (đếm bằng mã: tổng `len(say.split())` của YAML sinh ra): L00 2283; L01 2294; L02 2293; L03 2291; L04 2131; L05 2299; L06 2295; L07 2298; L08 2288; L09 2145; L10 2290; L11 2291; L12 2217; L13 2300; L14 2290. Cả 15 bài ≤ 2300. Lint đo cùng số (L05 2299, L13 2300, L07 2298).
Cổng sau khi cắt: lint 15/15 = 0 FAIL, 0 WARN; verify_bnk 48/48 PASS; `screen_gen.py` rồi `screen_code.py check --course BNK`, lab_gate, curriculum, test_e52 chạy lại (kết quả ở tin nhắn cuối).

## 6. Bài đổi (requeue) — danh sách cuối
L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L13, L14 (14 bài). L12 không đổi.

## 6-cũ. Bài đổi (requeue) — vòng trước
L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L13 (13 bài). L12, L14 không đổi nội dung.
