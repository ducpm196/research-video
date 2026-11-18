# fix6 BNX_A (L00–L12, sửa theo R4_BNX_A, chuẩn P1 chặt) — 2026-11-16

Chia 3 nhánh; báo cáo chi tiết từng bài (mục R4 → cách xử lý, từ, cổng): `fix6_BNX_A_p1.md` (L00–L03), `fix6_BNX_A_p2.md` (L04–L07), `fix6_BNX_A_p3.md` (L08–L12). Nguồn sửa: `audit/bnx/src/l00..l12.py` (+ `audit/bnx/ver/l00.py` thêm kiểm quiz), sinh bằng `gen.py`; không sửa YAML sinh ra; không docker, dbrun, build, tts, asr, git; không chạm bnx-ora/bnx-mss.

## Tiến độ
- [x] A1 L00–L03  - [x] A2 L04–L07  - [x] A3 L08–L12  - [x] cổng chung

## Bài đã đổi → CẦN DỰNG LẠI
Cả 13: L00 L01 L02 L03 L04 L05 L06 L07 L08 L09 L10 L11 L12 (lời đọc và bảng/hình đổi ở mọi bài). Lab không đổi (lab_gate 39 PASS).

## Số liệu mỗi bài
| Bài | Lời đọc (từ) | Mục chưa giảng ước còn lại | asr_reviewed còn hiệu lực (trước→sau) | Ghi chú |
|---|---|---|---|---|
| L00 | 2286 | 0 | 5→4 | quiz câu 2 thêm điều kiện; ver/l00.py kiểm git thật: gộp thường 7 commit/2 cha, tua nhanh 6 commit/1 cha |
| L01 | 2295 | 0 | 8→8 | giữ nhãn "bản 08" |
| L02 | 2296 | 0 | 29→23 | |
| L03 | 2298 | 0 | 11→8 | "mã làm mới" định nghĩa trước Bước 6/quiz/recap |
| L04 | 2293 | 0 | 5→5 | nhãn hình tuần tự rút ngắn (SHOULD); `HTTP/1.1` giảng |
| L05 | 2297 | 0 | 5→4 | 5 bảng mới; sửa tay khoá `files:` may.sh/xau.sh trong screen/l05.yaml |
| L06 | 2291 | 0 | 8→7 | `IS NULL`, `NUMBER/VARCHAR2`, lệnh Docker tách step riêng (SHOULD); chữ khối mã không đổi |
| L07 | 2297 | 0 | 8→8 | "biến gắn", `VALUES LESS THAN`, `DBMS_XPLAN`, `->>` |
| L08 | 2300 | 0 | 18→17 | |
| L09 | 2297 | 0 | 8→6 | |
| L10 | 2292 | 0 | 19→18 | bảng `/opt/kafka/bin/…`, Avro, "bộ dọn" |
| L11 | 2300 | 0 | 9→9 | bảng thẻ XML pacs.008; SHOULD 15 vs 20 USD và ISO 4217 "số chữ số lẻ theo ISO 4217, làm tròn nửa lên" |
| L12 | 2296 | 0 | 7→7 | giữ "nguồn tổng hợp, cần kiểm lại" |
Mọi bài ≤ 2300 từ (đếm lại bằng mã sau khi gộp). Phần asr_reviewed mất là câu bị đổi chữ — cần ASR lại khi dựng.

## Cổng thật
- `lv.py lint` 13/13: 0 FAIL, 0 WARN (PASS 36, 42, 46, 59, 37, 35, 38, 39, 41, 41, 39, 52, 52).
- `lv.py render` từng bài (nhánh chạy): 0 vấn đề; đã xem khung PNG mới ở các bài có bảng/hình mới (L00 L01 L02 L03 L04 L05 L06 L07 L08 L09 L10 L11 L12). Tràn đã sửa: L08 check.0/formula.4, L09 sym.
- `verify_bnx` từng bài: L00 20/20, L01 20/20, L02 20/20, L03 21/21, L04 23/23, L05 21/21, L08 30/30, L09 23/23, L11 34/34, L12 30/30. **L06, L07 (Oracle) và L10 (Kafka Docker) KHÔNG chạy** vì cấm docker: NOT_VERIFIED lần này; chữ mọi khối mã L06/L07/L10 giữ nguyên.
- Sổ mã: `screen_keep.py` + `screen_fast.py` FAIL/STALE/MISSING/ORPHAN 0 cho L00–L05, L08, L09, L11, L12. L06, L07, L10: `screen_keep` + kiểm sha-only (20/20, 24/24, 16/16 khối khớp); chưa chạy thật vì khối Oracle/Kafka cần docker.
- Đã gộp sổ chung bằng công cụ chính thức `screen_try.py --merge` (một lần): kiểm lại cả 702 khối L00–L38: 0 MISSING, 0 STALE. Còn 151 mục ORPHAN trong sổ (đều là mục cũ có trong sổ trước khi gộp, không có mục mới); trong L00–L12 có 47, trong đó 20 là khoá cũ trùng step do chèn bảng (liệt kê: L00 pitfalls 1 0; L01 check 1 0; L02 check 2 0, check 4 0, check 6 0, pitfalls 2 0/2 1, sym 0 0; L03 example 8 0/11 0/12 0; L05 example 0 0/2 0/5 0/7 0; L06 check 0 0; L08 formula 4 0; L09 check 0 0; L10 check 0 0; L11 sym 2 0) — theo lệnh KHÔNG xoá, chờ người dùng quyết cùng 137 mục cũ. Lưu ý: `screen_try.py` in dòng cuối bị lỗi mã hoá cp1252 sau khi đã ghi xong tệp (vô hại).
- `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 0 lỗi. `check_curricula_graph.py`: 0 lỗi. `tests/test_e52.py`: 0 FAIL. `lab_gate.py BNX`: 39 PASS · 0 FAIL (196 lab). `arith_scan.py BNX`: 59 phép, 0 FAIL.
- Chưa chạy được: `screen_code.py check --course BNX` đầy đủ (cần docker cho Oracle/SQL Server/Kafka) — người điều phối chạy khi được phép.

## SHOULD (5/5 đã sửa)
L00 quiz điều kiện; L04 nhãn hình; L06 practice tách lệnh Docker; L11 phí 15 vs 20 USD; L11 ISO 4217. Không sửa: L00 example.7 khoảng trắng đầu dòng `*   0eac7e6`/`|\` (lệch định dạng), lab L00 `$(…)` (ngoài đường chính).

## Pháp lý/nguồn
Giữ mọi nhãn "cần kiểm lại"/"chưa đọc nguyên văn"/"nguồn tổng hợp"; không thêm số hiệu/điều/nguồn mới.

## Việc người điều phối còn lại
Dựng lại 13 bài (build/tts/asr); chạy `ver/l06,l07,l10` và `screen_code check --course BNX` khi docker được phép; quyết định về mục ORPHAN; reader đo lại P1.
