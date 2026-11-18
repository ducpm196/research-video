# WP4 nhánh C — BNX L08, L09, L10, L11 lên chuẩn AF2 (2026-11-14)

## Tiến độ
- L08, L09 xong (verify, lint, render, lab, screen_fast).
- L10, L11 xong (verify gồm Kafka thật, lint, render, lab, screen_fast).

## Bài đã đổi và cổng thật
| Bài | af2 + covers | Cảnh mới | Lab | Lời đọc | verify | lint | render | screen_fast |
|---|---|---|---|---|---|---|---|---|
| L08 Elasticsearch | 5 mục tiêu | `quymo`, `practice` | `labs/BNX/L08` (loi_giai.py) | 2 306 từ | 30/30 PASS | 0 FAIL 0 WARN | 0 vấn đề | PASS |
| L09 Couchbase | 5 mục tiêu | `quymo`, `practice` | `labs/BNX/L09` (loi_giai.py) | 2 314 từ | 23/23+ PASS | 0/0 | 0 | PASS |
| L10 Kafka/RabbitMQ | 5 mục tiêu | `quymo`, `practice` | `labs/BNX/L10` (loi_giai.py) | 2 309 từ | 29/29 PASS (có Kafka 3.9.0 thật trong Docker, tự dựng/tự gỡ) | 0/0 | 0 | PASS |
| L11 Thanh toán quốc tế | 5 mục tiêu | `quymo`, `practice` | `labs/BNX/L11` (loi_giai.py) | 2 478 từ (xem mục đề xuất tách) | 33/33+ PASS | 0/0 | 0 | PASS |

Tổng ba lệnh gộp: `verify_bnx.py L08 L09 L11` 86/86 PASS; `verify_bnx.py L10` 29/29 PASS; `screen_fast.py L08 L09 L10 L11` 48 khối, PASS 75 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0; `lab_gate.py BNX`: 4 lab của nhánh PASS (lỗi duy nhất của cả khoá là `labs/BNX/L17` mồ côi, ngoài phạm vi); `check_legal.py`: 0 FAIL (L11 chỉ dẫn ISO/CBPR+, không có văn bản pháp luật Việt Nam); `tools/lv.py curriculum curriculum/bnx.yaml`: 37 bài, 0 lỗi; `tests/test_e52.py`: 0 FAIL; render cuối cùng (sau khi rút lời đọc): L08 141 khung, L09 138, L10 150, L11 139, đều 0 vấn đề; đã xem ≥ 3 khung PNG mỗi bài (quymo, practice, pitfalls).

## Cảnh quy mô (số đo thật, chương trình chạy nguyên văn trên màn hình)
- L08: quét thô vs chỉ mục ngược ở 1 200 / 120 000 / 1 200 000 mô tả (đọc n mô tả so với 2 / 120 / 1 200 dòng); số bản ghi phải chép lại khi đổi 3 → 4 mảnh chính (CRC32 thật): 885 / 89 991 / 899 480 (74–75 %; lý thuyết 900 000 ghi rõ lệch do hàm băm không chia đều). Thời gian chép 10 000 bản ghi/giây ghi "(số minh hoạ)". Elasticsearch thật KHÔNG chạy (mô phỏng cơ chế, ghi rõ trên màn hình và lời đọc).
- L09: n tiến trình cùng đọc rồi cùng ghi trên chính lớp `Store` của bài: 3 / 210 / 20 100 lần ghi cho n = 2 / 20 / 200 (n(n+1)/2), điểm cuối luôn đúng n; khoá bi quan: n lần ghi, người cuối chờ n × thời gian giữ (số minh hoạ). Couchbase thật không chạy (kho mô phỏng, ghi rõ).
- L10: hàm `compact` của bài trên nhật ký 1 000 / 100 000 / 1 000 000 bản ghi, 100 tài khoản: sau nén luôn còn 100 (đọc lại khi khởi động: n so với 100). Kafka thật chạy ở cảnh `check` (bản ghi, bia mộ, đoạn) như trước.
- L11: cộng 0,10 nhiều lần bằng số thực và `Decimal`: 10 → 0.9999999999999999, 10 000 → 1000.0000000001588, 1 000 000 → 100000.00000133288 (đúng: 1.00 / 1000.00 / 100000.00); phí cố định 20 USD chiếm 2 % / 0,02 % / 0,0002 % ở 1 000 / 100 000 / 10 000 000 USD, người nhận SHA vẫn thiếu 15 USD ở mọi cỡ.

## Lab mới (số liệu khác ví dụ trong bài, chấm bằng `labs/cham.sh`)
- L08: chỉ mục ngược 4 mô tả không dấu, giao hai từ, mảnh của 29/41/50 với 5 mảnh, giữ mảnh 4 → 6 (4/12).
- L09: thùng ảo của `session::s77` (1024 và 128 thùng), hai tiến trình CAS trên hồ sơ 300 điểm CAS 4 → 270, CAS 6.
- L10: nén nhật ký 8 bản ghi có bia mộ (còn bia mộ / hết hạn) và khớp ba mẫu sàn chủ đề với `payment.eu.sepa.eur`.
- L11: tách BIC `ABCDDEFFXXX`, kiểm IBAN `GB90BANK98765432101234` (dư 1) và bản đổi chỗ (dư 50), ba cách chịu phí cho 2 000 USD (OUR 2000/2020, SHA 1988, BEN 1980).
Lab chỉ in dạng không có dấu nháy đơn (lint E53 không giải mã `&#x27;` nên đầu ra có nháy sẽ không khớp màn hình).

## Mục tiêu giáo án đổi (curriculum/bnx.yaml, bốn mục)
L08, L09, L11: thêm mục tiêu 5 (so sánh ở ba mức, cảnh `quymo`). L10: mục tiêu 4 đổi "Chọn Kafka hay RabbitMQ…" thành "Nêu khi nào chọn Kafka, khi nào chọn RabbitMQ…" (E51 đòi cảnh LÀM cho động từ "chọn", mà phần chọn được dạy ở quiz) và thêm mục tiêu 5. Mọi mục tiêu bài = giáo án (verify so nguyên văn).

## Id thuật ngữ mới (E52, `tools/registry/symbols.BNX.yaml`)
| id | giảng ở |
|---|---|
| bnx_lam_tuoi, bnx_chi_muc_nguoc, bnx_manh_chinh | L08 hook (step 1 và 2); `bnx_giao_dich_csdl` (đã có sẵn của L36) giảng thêm ở L08 prereq |
| bnx_cas, bnx_vbucket | L09 hook step 2 |
| bnx_bia_mo, bnx_san_chu_de | L10 hook step 2; bnx_avro ở L10 formula step 4 |
| bnx_bic, bnx_iban, bnx_nostro, bnx_iso20022 | L11 hook step 2 |
Không đăng ký "Elasticsearch", "nén nhật ký", "hạn sống", "Kafka" (L31, L09, L19 dùng, sẽ làm lỗi E52 ở bài khác). Các bài L24–L36 không chứa các id trên (đã grep trước khi đăng ký).

## Không làm / lưu ý
- Elasticsearch, Couchbase, RabbitMQ, Schema Registry: không chạy ảnh thật (nặng, ổ D đầy theo ghi chú); mọi cảnh mới ghi "mô phỏng". Kafka thật vẫn kiểm trong `ver/l10.py`.
- `ver/l10.py` chạy Kafka trong Docker (3–4 phút/lần).
- Đã rút lời đọc bằng công cụ cắt câu (`scratchpad/trim.py`) trên nguồn `src/l08..l11.py`; mỗi lần cắt đều gen + lint lại.
- **Đề xuất tách bài**: L11 (2 478 từ, bài gốc 2 462 từ đã vượt 2 300) gồm hai nửa rõ rệt: (a) BIC/IBAN/bản tin/ISO 20022/bút toán nostro; (b) tỉ giá, ba cách chịu phí, số thập phân và quy mô. Đề xuất tách thành hai bài thay vì cắt thêm. Không tự tách (giữ id).
- P1 dự kiến: các thuật ngữ mới đều giảng tại chỗ bằng câu thường ở lần đầu (hook), lint E52 sạch; riêng L11 vẫn còn các thuật ngữ như "Swift", "pacs.008", "MT103", "CBPR+" chỉ giải thích bằng bảng, chưa đăng ký sổ.
