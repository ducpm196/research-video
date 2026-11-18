# WP4 nhánh B — BNX L04–L07 lên chuẩn AF2 (2026-11-14)

## Tiến độ
- L04 XONG · L05 XONG · L06 XONG (quá dài, đề xuất tách) · L07 XONG (quá dài, đề xuất tách).
- Chưa dựng (build/tts/asr không chạy theo brief). Mọi bài `af2: true`, có `covers` (E51), cảnh `quymo` và cảnh `practice` + lab.

## Cổng thật (2026-11-14)
| Cổng | L04 | L05 | L06 | L07 |
|---|---|---|---|---|
| `verify_bnx.py Lxx` | 22/22 PASS | 20/20 | 30/30 | 29/29 (tổng 101/101, 0 SKIP) |
| `gen.py` + `lv.py lint` | 0 FAIL 0 WARN (40 PASS) | 0/0 (35) | 0/0 (43) | 0/0 (43) |
| `lv.py render` | 0 vấn đề (113 khung) | 0 (120) | 0 (167, sau tách step ở cảnh quymo) | 0 (173) |
| `screen_fast.py L04 L05 L06 L07` | 80 khối: PASS 90 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 | | | |
| `lab_gate.py BNX` (cả khoá) | 35 PASS · 0 FAIL (115 lab được tham chiếu; gồm labs/BNX/L04–L07) | | | |
| `tests/test_e52.py` | 0 FAIL | | | |

Số từ lời đọc (đếm `say`): L04 2 306 · L05 2 346 · L06 3 054 · L07 3 049 (mục tiêu ≤ 2 300).

## Đã làm (mỗi bài)
Chung: `af2: true`, `covers` cho 6 mục tiêu (4 cũ + 2 mới), cảnh `quymo` ("example") với số đo thật ≥ 2 mức, cảnh `practice` (Tự làm) trước `recap`, lab `labs/BNX/Lxx/{de.md,mong_doi.txt,loi_giai.py}` chấm qua `labs/cham.sh`, `curriculum/bnx.yaml` đồng bộ mục tiêu, bộ kiểm `ver/lNN.py` thêm kiểm khối quy mô chạy nguyên văn (bằng đường khác) + lab, sổ `screen/lNN.yaml` thêm khối quy mô/lab. Nguồn mã đổi sang `lib2` (có `practice_steps2`).

- **L04 OAuth2/OIDC**: quymo = số lần xin mã mỗi giờ khi máy khách giữ mã trong bộ đệm, 10 / 1 000 / 100 000 máy khách = 140 / 13 360 / 1 333 390 (chạy thật, kiểm lại bằng duyệt từng giây ở 10 và 1 000 + công thức đóng ở 100 000) so với hỏi lại máy chủ ủy quyền mỗi yêu cầu 36 000 / 3 600 000 / 360 000 000 (số minh hoạ 1 yêu cầu/giây/máy); bảng đánh đổi kiểm tại chỗ vs hỏi lại. Lab: đếm số lần xin mã (TTL 120, xin lại khi còn 20 giây, 4 API) và giây cuối còn nhận (149).
- **L05 mTLS**: quymo = số lần đổi chứng chỉ mỗi năm khi xoay ở 2/3 hạn, 10 / 1 000 / 100 000 dịch vụ × hạn 365 / 30 ngày (10…100 000 so với 180…1 800 000, gần 4 932 lần mỗi ngày), kiểm bằng duyệt từng ngày. Lab: lịch xoay vòng 3 chứng chỉ (ngày xoay, ngày hết hạn, trạng thái). Sửa SHOULD: tiêu đề "Bốn lần thử" → "Năm lần thử" (mã chạy 5 ca); câu lời "cùng cờ là nơi cấp…" khó hiểu → viết lại; câu recap "mỗi thông báo lỗi chỉ về một cửa" bỏ tuyệt đối (nêu ngoại lệ "unable to get local issuer certificate" có hai nguyên nhân). Hai SHOULD của `fixf_A.md` (quiz 3 "355 ngày", "máy văn phòng") đối chiếu nguồn: đã có đủ (hộp "Chốt", "đúng hệ điều hành ghi ở chú thích"). Sổ screen L05 sạch (14 khối PASS, trước đó từng 3 FAIL/5 STALE).
- **L06 thủ tục lưu trữ**: quymo = đếm THẬT câu lệnh gửi tới cơ sở dữ liệu khi logic chuyển tiền nằm ở ứng dụng (sqlite đại diện, ghi rõ): 5 câu mỗi lần chuyển → 50 / 5 000 / 500 000 câu ở 10 / 1 000 / 100 000 lần, so với thủ tục = 1 lần gọi mỗi lệnh; bảng đánh đổi (khoá giữ lâu hơn khi chờ mạng). Lab (sqlite, vì cham.sh không có Oracle): hàm chuyển tiền cộng-nhận-trước, BEGIN/ROLLBACK khi vi phạm CHECK, tổng giữ 1200. E52: giảng tại chỗ JDBC (hook), ngoại lệ (bước 6), XACT_ABORT (sym).
- **L07 Oracle khối lượng lớn**: quymo = Oracle thật (bnx-ora qua dbrun): nạp 365 000 dòng (gấp 100 lần), đếm cả bảng 365 000 và riêng phân vùng tháng 3 = 31 000; bảng ba mức 3 650→310 (đo ở ví dụ), 365 000→31 000 (đo ở đây), 36 500 000→3 100 000 (tính theo tỉ lệ 31/365, ghi rõ "tính theo tỉ lệ"). Lab (sqlite): `CHECK (json_valid)` ↔ `IS JSON`, `json_extract`/`->>`. E52: EXPLAIN, "chia theo khoá", DBMS_AQ, INMEMORY.

## Id thuật ngữ mới (symbols.BNX.yaml, mục `# ── L04–L07 ──`)
| id | bài giảng (`introduces`) |
|---|---|
| `bnx_pkce` | L04 prereq.0 |
| `bnx_xact_abort` | L06 sym.1 |
| `bnx_dbms_aq` | L07 sym.1 |
| `bnx_inmemory` | L07 sym.1 |
Id cũ (của L24+) mà L04–L07 dùng và đã giảng tại chỗ: `bnx_ma_bam` (L04 prereq.0), `bnx_jdbc` (L06 hook.1), `bnx_ngoai_le` (L06 formula.5), `bnx_explain` (L07 sym.0), `bnx_chia_theo_khoa` (L07 formula.12). Không dùng `assumes` (không phụ thuộc bài của nhánh A).

## Không làm / hạn chế
- **L06 (3 054 từ) và L07 (3 049 từ) vượt 2 300**: nội dung gốc đã 2 857 và 2 700; đã cắt ≈ 200 từ mỗi bài nhưng không bỏ được mục tiêu nào. **Đề xuất tách** (không tự tách/đánh số lại): L06 → (a) thủ tục Oracle PL/SQL + giao dịch + khoá có thứ tự, (b) T-SQL + XACT_ABORT + chống chèn mã + JDBC; L07 → (a) phân vùng + JSON + cắt tỉa, (b) hàng đợi Oracle AQ + bộ nhớ cột + phân mảnh. L04 (2 306) và L05 (2 346) sát ngưỡng, giữ.
- Lab Oracle/SQL Server thật không làm (cham.sh/lab_gate không chạy Oracle): L06 và L07 dùng lab sqlite tương ứng, nói rõ trong de.md và trên màn hình.
- Chưa mở đủ 3 khung PNG mỗi bài theo lượt ngay sau lần sửa cuối: đã mở L04 (73, 76, 103), L05 (79, 83, 109), L06 (101, 155), L07 (119). Chưa nghe giọng; không chạy build/tts/asr/audit_all/git.
- P1 dự kiến: còn chữ viết tắt/thuật ngữ chưa đăng ký (RFC, base64, Basic, Bearer…) chỉ giảng bằng bảng tại chỗ, không có `term:`; ước 2 ở khoảng 3/4 bài (L06/L07 dày thuật ngữ T-SQL/PL-SQL).
- Phát hiện ngoài phạm vi: `symbols.BNX.yaml` bị hỏng YAML thoáng qua khi nhiều nhánh Edit cùng lúc (tự hết); dòng `name:` có dấu ": " phải đặt trong dấu nháy.

## Cổng cuối (đã chốt)
- `lv.py curriculum curriculum/bnx.yaml`: 37 bài, 37 đã có đặc tả, 0 lỗi (chạy lại sau khi sửa mục tiêu L04–L07, 2026-11-14T01:13Z).
- `audit/check_curricula_graph.py`: không chu trình, 0 ví dụ có số mà thiếu VER; một dòng báo `WEB:L04` FAIL, thuộc khoá WEB, ngoài phạm vi nhánh B.
