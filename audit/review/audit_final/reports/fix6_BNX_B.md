# fix6 BNX_B (L13–L25, sửa theo R4_BNX_B, chuẩn P1 chặt) — bắt đầu 2026-11-16

## SỔ TÁC TỬ (ghi trước khi giao)
Người điều phối chính (tác tử này) làm L13, L14, L15, L25; chia phần còn lại cho 3 nhánh (fork), mỗi nhánh chỉ sửa `audit/bnx/src/lNN.py` (+ `ver/lNN.py`, `screen/lNN.yaml` qua `screen_keep.py`) của bài mình, sinh bằng `gen.py`, ghi báo cáo riêng:
| Nhánh | Bài | Báo cáo riêng |
|---|---|---|
| B1 | L16 L17 L18 | `fix6_BNX_B_p1.md` |
| B2 | L19 L20 L21 | `fix6_BNX_B_p2.md` |
| B3 | L22 L23 L24 | `fix6_BNX_B_p3.md` |
Việc chung do tác tử chính làm SAU khi các nhánh xong: `screen_try.py --merge` (một lần), curriculum, check_curricula_graph, test_e52, lab_gate, arith_scan, tổng hợp báo cáo này.
Cấm: docker, dbrun.py, build/tts/asr/git. L13/L19 có khối chạy bằng docker: KHÔNG đổi văn bản khối mã (giữ sha), `screen_keep` chỉ đánh lại khoá; `verify_bnx` chạy với PATH đã bỏ thư mục Docker (dòng docker → SKIP).

Khuôn dùng chung (mới, tệp riêng, không đụng lib.py/lib2.py): `audit/bnx/libj.py` — `jstep([(khoá hoặc bộ ba tự khai, ví dụ HTML, ví dụ lời đọc)])` dựng bảng "viết trong mã → đọc là → ví dụ"; `nowrap()` cho ô "(×N)". Không đổi đầu ra bài nào khác.

## TIẾN ĐỘ
- [x] L13 (xong: lint 0/0, render 0 vấn đề, 2294 từ, ver 22/23 PASS + 1 SKIP docker, screen sha-only sạch)
- [x] L14 (xong: lint 0/0, render 0 vấn đề, 2300 từ, ver 25/25, screen_fast PASS 9) - [x] L15 (xong: lint 0/0, render 0, 2298 từ, ver 25/25, screen_fast PASS 10) - [x] L25 (xong: lint 0/0, render 0, 2300 từ, ver 16/16, screen_fast PASS 25; mã đủ ở labs/BNX/L25/ma_day_du/)
- [x] B1 (L16–L18) - [x] B2 (L19–L21) - [x] B3 (L22–L24): chi tiết ở fix6_BNX_B_p1/p2/p3.md
- [x] cổng chung: lint 13/13 = 0/0; `lv.py curriculum curriculum/bnx.yaml` 39 bài 0 lỗi; test_e52 0 FAIL; lab_gate BNX 39 PASS; arith_scan BNX 59 phép 0 FAIL; check_curricula_graph sạch; `screen_try.py --merge` đã chạy (BNX.yaml: 274 khối L13–L25, MISSING 0, STALE 0; 137 ORPHAN cũ giữ nguyên). KHÔNG chạy full `screen_code check` (khối docker L13/L19 và Redis); L13/L19 chỉ kiểm sha.

## Việc của tác tử chính (L13, L14, L15, L25)
- L13: bảng Python (def/while/min/for/print), YAML `{ } [ ] -`, vỏ lệnh (`echo … | docker login`, `docker build -t`, `kubectl set image`), `mvn -q dependency:go-offline`, `(0, D, 0) in seen`/`max`; ô (×N) nowrap. Giữ nguyên văn bản mọi khối mã (docker). ver: 22/23 PASS + 1 SKIP (docker build --check, chạy với PATH bỏ Docker).
- L14: `from … import … as`, `def/return/for`, `[F(0)]*30`, comprehension, `min`, `a, b = x, y`, `print`, `#`; giữ nhãn "cần kiểm lại" cho Điều 5/15 và 01/3/2027.
- L15: `while … j += 1`, `1_000_000`, `round`, `print`, `#`, vòng `for tps in (…)`; YAML `- {name: …}`, `"201": {…}`.
- L25: try/finally, if/else/throw, signature `throws Throwable`, `new DriverManagerDataSource(…)`, try-with-resources, lambda `submit`; BỎ câu Oracle ORA-02179/SQL Server (chỉ nói "bài chỉ chạy thật trên H2"); mã đủ 7 tệp Java + README ở `labs/BNX/L25/ma_day_du/` (sinh từ prog trong l25.py), tiêu đề "(trích; mã đủ ở thư mục kèm của lab)".
- libj.py (mới): `jstep` bỏ cột "ví dụ" khi mọi ô ví dụ rỗng; `nowrap`.
- Số từ: L13 2294, L14 2300, L15 2298, L16 2299, L17 2288, L18 2287, L19 2292, L20 2288, L21 2290, L22 2292, L23 2296, L24 2260, L25 2300.
- asr_reviewed trước→sau: L13 4→3, L14 6→3, L15 19→12, L16 5→2, L17 2→1, L18 2→1, L19 22→22, L20 6→4, L21 6→3, L22 4→4, L23 9→9, L24 10→10, L25 11→? (câu đổi chữ cần ASR lại khi dựng).
- Sổ chứng cứ: `screen_keep` không dịch lại `within:`/`files:` khi chèn step: đã sửa tay bằng Edit từng mục (L21 formula 15 0; L22 `L22_model` files; L23 3 mục `within`; L17 thêm mục `BNX L17 example 19 1`). Chạy lại screen_keep L21–L23 sẽ làm các mục này lệch lại.

Mã tác tử (giao 2026-11-16): B1=a27868990de03397b, B2=a695dd8aec7ecd17e, B3=a18bd4cf5080f155a. Bị ngắt -> SendMessage tiếp.
