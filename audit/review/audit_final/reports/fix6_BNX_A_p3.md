# fix6 BNX_A phần 3 (nhánh A3): L08, L09, L10, L11, L12 — 2026-11-16

## TIẾN ĐỘ
- [x] L11 xong (lint 0/0, render 0, verify 34/34, screen_fast PASS 16)
- [x] L12 xong (lint 0/0, render 0, verify 30/30, screen_fast PASS 17)
- [x] L09 xong (lint 0/0, render 0, verify 23/23, screen_fast PASS 16)
- [x] L10 xong (lint 0/0, render 0; KHÔNG chạy ver/screen_fast vì docker; `screen_keep` + `shacheck` 16/16 sha khớp)
- [x] L08 xong (lint 0/0, render 0, verify 30/30, screen_fast PASS 20)
Nguồn sửa: `audit/bnx/src/l08.py … l12.py`, sinh lại bằng `audit/bnx/gen.py`. Không sửa YAML sinh ra, không sửa `symbols.BNX.yaml` (không cần thêm mục: lint/E52 0), không chạm `audit/review/screen_code/BNX.yaml` (chỉ `audit/bnx/screen/lNN.yaml` do `screen_keep.py` sinh lại; tác tử chính gộp). Không docker, không dbrun.

## Bảng từng bài
| Bài | Mục R4 → cách xử lý | Từ lời đọc trước → sau | Chưa giảng ước còn lại |
|---|---|---|---|
| L11 | thẻ XML `GrpHdr/MsgId/CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI/ChrgBr/Ccy`: bảng 'viết trong thẻ → đọc là → trong ví dụ' 4 hàng + định nghĩa XML đứng TRƯỚC khối XML (sym.2, step riêng `clear`); `for c in s:` thêm hàng vào bảng formula.2; `from decimal import Decimal, ROUND_HALF_UP` ghép vào hàng đầu bảng formula.5 | 2284 → 2300 | 0 |
| L12 | `elif`: hàng `if a: … elif b: … else: …` có ví dụ ở bảng prereq.3 (lời đọc thêm một câu); 'nối hai bảng' → 'ghép hai bảng theo cột chung (phép nối bảng)' ở bảng và lời đọc; VBHN: hàng bảng sym.1 ghi 'VBHN = văn bản hợp nhất: bản ghép văn bản ban đầu với các lần sửa' + lời đọc | 2298 → 2296 | 0 |
| L09 | `return dict(self.doc), self.cas`: hàng mới ở bảng formula.4 ('trả về hai giá trị cùng lúc… `d, c = s.get()`') + lời đọc; `from itertools import permutations` và `;` (`a; continue`): hai hàng ở bảng check.0 + lời đọc; Couchstore/Magma/Enterprise: hàng vBucket ghi 'Bộ lưu là cách kho ghi dữ liệu xuống đĩa: Couchstore (kiểu cũ)…, Magma (kiểu mới)…, Enterprise (bản thương mại)' + lời đọc; bảng sym.0 tách 2 step (3+3 hàng) vì tràn khung | 2286 → 2297 | 0 |
| L10 | `kafka-topics.sh`, `…-console-producer.sh`, `…-console-consumer.sh`, `/opt/kafka/bin/`: hàng bảng check.3 (đứng trước mọi lệnh Kafka) + lời đọc; Avro `record`/`long`/`string`/`default`: ghi chú dưới lược đồ (formula.5) + một câu lời đọc; 'bộ dọn': 'tiến trình nền của Kafka' ở lời đọc intuition.0 + dòng chữ mới dưới hình (svg cao 475) | 2297 → 2292 | 0 |
| L08 | `text.split()`: hàng mới ở bảng intuition.1 + lời đọc; `word in d.split()` và `buffer, searchable = [], []`: bảng mới (3 hàng) đứng trước khối mô phỏng làm tươi (formula.4, `clear`); `round(x, 3)`: thêm vào ghi chú dưới khối check.0; 'NAPAS': 'hệ thống chuyển tiền giữa các ngân hàng ở Việt Nam' ở màn hình hook.0 và lời đọc | 2299 → 2300 | 0 |

Ghi chú về lời đọc: đếm bằng `dump.py` (tổng `len(say.split())`); lint 0 WARN ở cả 5 bài, mỗi say ≤ 38 từ và ≤ 170 ký tự. Để chừa chỗ cho phần mới đã cắt: các câu dẫn ("Tổng kết:", "Hôm nay ta trả lời bốn câu hỏi", "Bảng gom số đếm…", "Ở bài sau, ta học…" → "Bài sau học…"), phần lặp ở L08 intuition.5/pitfalls.2 (bỏ 'cập nhật qua Kafka…' khỏi lời đọc, vẫn ở màn hình), L09 quiz.3 (bỏ câu phép tăng liền một bước khỏi lời đọc, vẫn ở màn hình), L10 quiz.0 (bỏ câu đọc lại đề), L11/L12 vài mệnh đề thừa. Không bỏ mục tiêu covers, bảng cách đọc, cảnh quy mô, lời giải quiz.

## SHOULD (L11)
- quymo.2: cột 'thiếu so với hoá đơn (phí trung gian 15)' và 'một phí cố định khác, 20 USD, chiếm (số minh hoạ)'; lời đọc nói rõ 'hai mươi đô la là khoản khác với mười lăm đô la của trung gian'.
- formula.6 (lời đọc) và recap.0 (màn hình): 'số chữ số lẻ theo chuẩn ISO bốn hai một bảy, làm tròn nửa lên' / 'số chữ số lẻ theo ISO 4217, làm tròn nửa lên'.
- Pháp lý/nguồn: không đổi nhãn nào ('cần kiểm lại', 'nguồn tổng hợp, cần kiểm lại', 'kiểm lại trước khi áp dụng'), không thêm số hiệu/điều/nguồn.

## Cổng đã chạy
- `tools/lv.py lint` L08–L12: 5/5 = 0 FAIL, 0 WARN (PASS 41, 41, 39, 52, 52).
- `tools/lv.py render`: 0 vấn đề ở cả 5 bài. Lần đầu có tràn khung: L09 sym (bảng 6 hàng, đã tách 2 step), L08 check.0 (ghi chú dài → rút ngắn) và L08 formula.4 (ghi chú → tách thành bảng riêng). Đã xem khung PNG: L11 00025 (bảng thẻ XML), L12 00020 (bảng elif), L10 00083 (bảng lệnh Kafka) + 00050 (lược đồ Avro + ghi chú), L09 00018 (bảng sym), L08 00061 (bảng mô phỏng). Tất cả gọn, không tràn.
- `audit/bnx/verify_bnx.py`: L08 30/30, L09 23/23, L11 34/34, L12 30/30 PASS. L10: KHÔNG chạy (ver/l10 gọi Docker/Kafka); mã trên màn hình L10 không đổi một ký tự nào.
- Sổ mã: `screen_keep.py` rồi `screen_fast.py` (L08 PASS 20, L09 PASS 16, L11 PASS 16, L12 PASS 17; FAIL/STALE/MISSING/ORPHAN 0). L10: `screen_keep.py L10` (chỉ chạy các prog Python lúc import, không docker) rồi `shacheck.py L10`: 16/16 sha khớp, 0 MISSING/STALE/ORPHAN.
- `asr_reviewed` (trước → sau): L08 18 → 17, L09 8 → 6, L10 19 → 18, L11 9 → 9, L12 7 → 7. Phần mất là các câu bị sửa lời (gen.py chỉ giữ bản duyệt khớp nguyên câu); cần nghe lại ASR các câu mới/đổi khi dựng lại.
- `tests/test_e52.py`: 0 FAIL (E52/E55).

## Mục không làm / còn mở
- L10: không chạy được `ver/l10.py` và `screen_fast L10` (cần Docker); khối mã không đổi nên sổ không đổi theo sha.
- Không thêm `introduces`/`symbols.BNX.yaml` cho XML/Avro/VBHN (lint và E52 đã 0; thuật ngữ được giảng tại chỗ bằng bảng/ghi chú).

## Bài đã đổi (requeue)
L08, L09, L10, L11, L12 (5 bài); lời đọc đổi ở cả 5, bảng/hình mới ở cả 5.
