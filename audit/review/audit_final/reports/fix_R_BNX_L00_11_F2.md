# F2 — sửa BNX L07 và soạn bài mới L38 (2026-11-14)

## Đã đổi
- **L07** (`audit/bnx/src/l07.py`, 2 299 từ, trước 3 049): giữ phân vùng + JSON. Tiêu đề (bài và giáo án): "Oracle cho khối lượng lớn: phân vùng và JSON". Mục tiêu còn 4: phân vùng và đọc kế hoạch cắt tỉa; lưu và truy vấn JSON; so số dòng ở 3 650 / 365 000 / 36 500 000; lab JSON sqlite.
  - P1 tại chỗ: `CONNECT BY ROWNUM … FROM dual` (khối riêng `SELECT ROWNUM FROM dual CONNECT BY ROWNUM <= 3` chạy thật), `TRUNC`/`MOD`, `user_tab_partitions` (từ điển dữ liệu), `DATE '…'`, `COMMIT`, `DROP TABLE IF EXISTS`/`CREATE TABLE`, `PARTITION FOR`, `EXPLAIN PLAN`/`DBMS_XPLAN` (`NULL, NULL`, `'BASIC +PARTITION'`), `TABLE ACCESS FULL`/`SORT AGGREGATE`, `PRIMARY KEY`, `RETURNING NUMBER`, `NUMTOYMINTERVAL`; nêu Oracle Free 23.
  - Mới: lỗi 2 (`IS JSON` lỏng/chặt, chạy thật), lỗi 3 (bỏ phân vùng tự chốt, ROLLBACK không cứu: còn 3 340 dòng), quiz câu 2 (tháng 2: SINGLE 2..2, 100 dòng) và câu 3 (cột JSON hay thêm cột).
  - "Cách dựng Oracle": bước cuối của cảnh `practice` ("Làm thêm trên Oracle thật", khối `docker run gvenzl/oracle-free:23-slim` + `docker exec … sqlplus`), de.md ghi mục này; sổ screen khai `other` + read_check.
  - Bỏ khỏi L07 (chuyển L38): hàng đợi AQ, bộ nhớ cột, phân mảnh, so sánh Kafka, quiz câu 2–3 cũ.
- **L38** (mới, `audit/bnx/src/l38.py`, 2 290 từ): "Bài 38 — Hàng đợi AQ, bộ nhớ cột và phân mảnh Oracle", `requires: [L37]`, `requires_ext: [BNX:L07]`, `af2: true`, 7 mục tiêu có `covers`.
  - Oracle thật (`bnx-ora`): tạo hàng đợi, gửi 101 hoàn tác + 102 chốt → 1 thông điệp, nhận 102 → còn 0; INMEMORY_SIZE = 0 và `user_tables.inmemory = ENABLED` (không khẳng định tốc độ, nói rõ "không đo được").
  - Cảnh quy mô đo thật (Python tất định): ô phải đọc theo hàng/cột ở 1 000 và 100 000 dòng (mô hình đếm ô, ghi rõ không đo thời gian); lệnh xuyên mảnh ở 1/3/30 mảnh (0 / 2 400 / 3 480 trên 3 540 cặp); lỗi 3: đổi 3 → 4 mảnh làm 748/1 000 tài khoản đổi mảnh (mod chỉ là minh hoạ).
  - Cảnh `check`: mô hình hàng đợi bằng danh sách thuần so với Oracle; lab `labs/BNX/L38` (sqlite: hàng đợi có giao dịch + đếm xuyên mảnh, de.md/mong_doi.txt/loi_giai.py); quiz 4 câu (câu 3 và 4 có quyết định: khi nào phân mảnh, Oracle hay Kafka).
  - Tệp: `ver/l38.py`, `sources_l38.md`, `tools/checklib_bnx/l38.py` (nhận `bnx_l07_queue`/`shard` chuyển từ l07, đổi tên `bnx_l38_*`), `screen/l38.yaml`.
- Chung: `curriculum/bnx.yaml` (mục L07 sửa, mục L38 ở cuối sau L37), dòng VER `BNX:L38` trong `audit/verify_plan_curricula.py`, `tools/registry/symbols.BNX.yaml` (thêm `bnx_khoa_phan_vung`, `bnx_cat_tia`, `bnx_bo_nho_cot`, `bnx_phan_manh`; `introduces`/`assumes` đúng bước). Công cụ mới: `audit/bnx/screen_ora.py` (sinh sổ screen cho khối Oracle: chạy thật trên bnx-ora, ghi expect_stdout; L07 và L38).

## Số cổng thật
- lint L07 0 FAIL 0 WARN (39 PASS); L38 0/0 (32 PASS). render L07 0 vấn đề (127 khung); L38 0 vấn đề (119 khung).
- `verify_bnx.py L07 L38`: 48/48 PASS (L07 26, L38 22), không SKIP.
- `screen_fast.py L07 L38`: 42 khối — PASS, FAIL 0, STALE 0, MISSING 0, ORPHAN 0.
- `lab_gate.py BNX`: 39 PASS · 0 FAIL.
- `check_curricula_graph.py`: 0 tham chiếu hỏng, 0 chu trình, VER không PASS: 0; `tests/test_e52.py`: 0 FAIL; `check_next_refs.py`: 551 lời hẹn, 0 lệch.
- `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 1 lỗi KHÔNG thuộc phạm vi F2: `L17: assumes ['bnx_base64url'] nhưng chưa bài tiên quyết nào giới thiệu` (L38, L07 sạch).
- Đã xem 6 khung PNG của L38 (sym, formula bước 1 và kết quả, example, check, quymo): không tràn.

## Không làm / lưu ý
- Tốc độ bộ nhớ cột và phân mảnh Oracle thật không đo (vùng nhớ cột = 0, bật cần khởi động lại instance dùng chung; phân mảnh cần nhiều cơ sở dữ liệu): bài ghi rõ là mô hình.
- Không dạy tên cách chia thực của Oracle (băm nhất quán) vì chưa đọc nguồn trong phiên; bài chỉ nói "hệ thật thiết kế cách chia để thêm mảnh chỉ di chuyển một phần dữ liệu".
- Sổ screen chung `audit/review/screen_code/BNX.yaml` chưa gộp (người điều phối chạy `audit/bnx/screen_try.py --merge`); mục cũ của L07 trong sổ chung (key theo vị trí) sẽ ORPHAN/STALE nếu không gộp lại.
- Câu `say` ngắn < 8 từ còn lại ở L07 là câu cũ không đổi (đã ghép qua `_spoken`); câu mới/đổi đều ≥ 8 từ.
