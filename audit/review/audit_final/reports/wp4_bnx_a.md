# WP4 — BNX L00–L11 lên chuẩn AF2 (2026-11-14)

## Kế hoạch và sổ tác tử
Điều phối: tác tử chính. Ba nhánh (fork) làm song song, mỗi nhánh một bộ bài, không chạm bài của nhánh khác:

| Nhánh | Bài | Ghi chú tài nguyên | Báo cáo nhánh |
|---|---|---|---|
| A | L00, L01, L02, L03 | Git thật, OpenAPI/Python, protobuf, HMAC; L00 giữ bản đồ khoá (E37) | `wp4_bnx_a_A.md` |
| B | L04, L05, L06, L07 | duy nhất nhánh này chạm Oracle/SQL Server (qua `audit/bnx/dbrun.py`); L05 có SHOULD cũ | `wp4_bnx_a_B.md` |
| C | L08, L09, L10, L11 | Kafka tự dựng/tự gỡ trong bộ kiểm; Elasticsearch/Couchbase mô phỏng nếu không chạy được; L11 pháp lý chỉ dẫn `audit/legal/registry.yaml` | `wp4_bnx_a_C.md` |

Khoá chung: `lv.py render` chạy một lần một lúc qua khoá thư mục trong scratchpad.

## Tiến độ
(điền sau mỗi nhánh)

## Tiến độ (tổng hợp, 2026-11-14)
Cả 12 bài L00–L11 đã nâng: `af2: true` + `covers` (6 hoặc 5 mục tiêu), cảnh `quymo` (số đo thật ≥ 2 mức), cảnh `practice` + lab `labs/BNX/L00..L11` (de.md, mong_doi.txt, một loi_giai.*), thuật ngữ E52 tại chỗ, sổ screen_code. Chi tiết từng nhánh: `wp4_bnx_a_A.md` (L00–L03), `wp4_bnx_a_B.md` (L04–L07), `wp4_bnx_a_C.md` (L08–L11).

## Cổng chung do điều phối chạy lại sau khi cả ba nhánh xong
- `lv.py lint` L00–L11: 0 FAIL 0 WARN cả 12 (L04 ban đầu 1 FAIL E52 `bnx_base64url`, sửa bằng `assumes` ở `audit/bnx/src/l04.py`, gen lại, lint sạch).
- `audit/review/lab_gate.py BNX`: 37 PASS · 0 FAIL.
- `tests/test_e52.py`: 0 FAIL. `lv.py curriculum curriculum/bnx.yaml`: 37 bài, 0 lỗi.
- Các cổng khác (verify_bnx, render, screen_fast, check_legal, check_course_refs, check_curricula_graph) theo báo cáo nhánh; `check_curricula_graph` có 1 FAIL của WEB:L04 (ngoài phạm vi).

## Mở
- Lời đọc vượt 2 300 từ: L06 3 054, L07 3 049, L11 2 478 (đề xuất tách bài, không tự tách). L00–L03 sát trần 2 300.
- L06, L07 mới xem 2 và 1 khung PNG (ngưỡng 3). Chưa ASR/tai người. Elasticsearch, Couchbase, RabbitMQ, Schema Registry: mô phỏng ghi rõ. Lab L06/L07 dùng sqlite (cham.sh không có Oracle).
- Pháp lý: L11 chỉ dẫn ISO/CBPR+, không văn bản VN. L12 không thuộc phạm vi.
