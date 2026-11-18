# R4 BNX L00–L12 (vòng 4, đọc độc lập, P1 chặt): 13/13 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a312988d55a2d8726)

Khai của reader: lỡ chạy `audit/bnx/dbrun.py --help` — tệp này tự chạy `ready()` = `docker exec … SELECT 1` trên bnx-ora và bnx-mss (kết quả (True, True); hai lệnh đọc trống, không ghi gì). Đây là vi phạm lệnh "không docker, không chạm DB" đã giao; reader không chạm docker/DB nữa. Người điều phối ghi nhận; không có hậu quả dữ liệu.
Phần Oracle (L06, L07) và Kafka thật (L10 check.5–9) chỉ đọc.

## 1. Tóm tắt
MUST 0 (13/13). P1=2 (chắc+vừa): 7/13 (L01, L04, L05, L08, L09, L10, L12); 6 bài còn lại P1=1 (L00, L02, L03, L07, L11) — riêng L06 reader tự điều chỉnh: 3 mục chắc+vừa (IS NULL, cờ docker, kiểu `NUMBER`/`VARCHAR2`) nên P1 chặt thực là 0 (tổng 12, GẦN). Tính cả mục yếu: 0/13 (L04=1, 12 bài khác = 0). P8=2 13/13; P9=2 13/13; spec khớp 13/13; SRT khớp 13/13; lab ĐÚNG 13/13 (cham.sh; L06, L07 chấm sqlite, Oracle chỉ đọc). Khoảng 140 số tính lại khớp 100%. SHOULD 5. Mất gốc: ĐỦ 13 (chắc+vừa), GẦN 13 (cả yếu). P3=1 ở L04 (nhãn hình bị gạch).
Không chạy được/không kiểm lại: Oracle, Elasticsearch, Couchbase, RabbitMQ chỉ khớp ghi chép nội bộ (NOT_VERIFIED); Kafka 3.9.0 theo nguồn nội bộ. Pháp lý (chỉ khớp `audit/bnx/sources.md`, thứ cấp): TT 64/2024/TT-NHNN (ký 31/12/2024, hiệu lực 01/3/2025) L04; NĐ 52/2024, TT 40/2024 qua VBHN 76 (Điều 27 khoản 1, Điều 26 khoản 1), TT 41/2025 (05/11/2025), TT 19/2021, Luật Quản lý thuế 108/2025/QH15 Điều 14 khoản 5 (chỉ bản thứ cấp expertis.vn; bài đã ghi "nguồn tổng hợp, cần kiểm lại") L12; mốc 22/11/2025, MT103↔pacs.008, MT202↔pacs.009 L11; "bản 08" Idempotency-Key và 2015-12-31 L01. GIỮ nhãn, không thêm số hiệu.

## 2. SHOULD
| Bài | Cảnh | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L00 | quiz.1 câu 2 | "Bạn gộp nhánh X, đã có 2 commit riêng chưa nằm trong 4 commit đó, vào main. Sau khi gộp có bao nhiêu commit? Commit mới có mấy cha?" (đáp án 7 commit, 2 cha) | thiếu điều kiện: nếu X rẽ từ đỉnh main và main không có commit mới thì `git merge X` tua nhanh → 4 commit, 1 cha | thêm "main cũng đã có commit mà X chưa có" | CONFIRMED |
| L04 | intuition.1 hình tuần tự | nhãn "⑤ mã truy cập (+ mã định danh nếu xin phạm vi openid)", "② khách đăng nhập…" | đường đời nét đứt gạch qua chữ nhãn | dời nhãn khỏi đường đời | CONFIRMED |
| L06 | practice.1 (khung 112) | đoạn chữ xám nhỏ `docker run -d --name ora-thu -p 1521:1521 -e …` | 7 dòng chữ xám nhỏ, lệnh dài; cảnh chỉ dừng 120 giây | tách lệnh Docker ra cảnh riêng như L07 practice.4 | CONFIRMED |
| L11 | quymo.3 | cột "thiếu so với hoá đơn 15" và "phí cố định 20 USD chiếm 2 %" cùng một dòng | hai khoản phí khác nhau (15 và 20) cùng bảng, không giải thích (15/1000=1,5% khác 2%) | ghi chú "20 USD là phí cố định khác với 15 USD trung gian" hoặc dùng cùng một số | CONFIRMED |
| L11 | formula.7 (lời đọc), recap.1 | "làm tròn theo chuẩn ISO bốn hai một bảy" / "làm tròn theo ISO 4217" | ISO 4217 quy định số chữ số lẻ của từng đồng tiền; quy tắc làm tròn (ROUND_HALF_UP) là lựa chọn chương trình (màn hình formula.7 ghi đúng) | "số chữ số lẻ theo ISO 4217, làm tròn nửa lên" | PLAUSIBLE |
Ghi chú: L00 example.7 git thật in `*   0eac7e6` và `|\  ` (màn hình mất khoảng trắng đầu dòng; chỉ lệch định dạng). Lab L00 de.md dùng `git rev-list --count`, `grep -c '^parent'`, `$(…)` không giải thích (ngoài chuẩn P1 đường chính). Chưa xem: sơ đồ cơ chế L03 intuition.2; L05 intuition.2; L08 intuition.5/6; L10 intuition.2/3; L11 intuition.2/3; L12 intuition.2.

## 3. Mục chưa giảng (P1 chặt) — theo bài (Loại A chưa giảng đâu trong L00–L12; B giảng ở bài khác, bài này không nhắc; M giảng muộn; Bảng cách đọc của khoá chỉ có phần Python "cách viết trong Python | nghĩa", một phần bash/SQL)
Số mục (chắc+vừa / cả yếu): L00 2/7, L01 0/5, L02 2/7, L03 2/7, L04 0/1, L05 0/9, L06 3/8, L07 1/6, L08 0/6, L09 0/5, L10 0/5, L11 2/5, L12 0/3.
- L00: intuition.2/check.2 `blob a9b66cb`, `f"blob {…}"` (A vừa); pitfalls.1 `git diff --cached --check` (A vừa); pitfalls.2 `git log --format="%h %s"` (`%h`), `git switch -c thu 18bdd9f`, `git switch -q -c n$i main`; quymo.2 `git switch -q main; xd=0` (`;`); `.env` (A yếu).
- L01: formula.2 `application/json`; formula.5 "bản nháp IETF"; check.2 `for f in (…):`, `if v is not None and not (…):`, `return loi + …` (một phần); check.4 `A, B = "…", "…"`; quymo.2 `req["amount"] = 0` (A yếu).
- L02: check.3/4 `json.dumps({"id": 150}…)` (M/B vừa); check.7 `out = {}`, `out[num], i = …` (M/B vừa; định nghĩa muộn ở pitfalls.3); check.2/6 `#`; sym.2 `//` trong .proto; check.6 `n = shift = 0`; quymo.3 "MB" (A yếu).
- L03: formula.5/quiz/recap "mã làm mới" (A CHẮC; dùng 7 lần, phương án quiz); example.9 `json.loads(unb64u(t))` (M vừa); example.9 `from datetime import datetime, timezone`; example.14 `time.time()`; check.2 `openssl base64 -A`, `date '+%F %T'`; sym.1 `typ` (A yếu).
- L04: formula.4 `HTTP/1.1` (A yếu).
- L05: example.3/4 `-CAkey`, `-not_before`, `-not_after`, `critical`; example.4 `openssl verify -CAfile`; example.9 `c, _ = nghe.accept()`, `t.recv`, `t.sendall`, `th.join()`; example.10 `if ten:`, `with … as s, \`; quymo.1/example.10 f-string, `//` (B) (A yếu).
- L06: formula.1 `p_amt IS NULL` (A vừa); practice.1 `docker run -d --name … -p … -e …`, `docker exec -it … sqlplus` (A vừa; giảng ở L07 practice.4 + L10 check.4); prereq.2 `NUMBER`, `VARCHAR2(10)`, `INSERT INTO … VALUES`; quymo.2 `INSERT … VALUES (1, 99999999), (2, 0)` (A yếu).
- L07: formula.5 "biến gắn" (A vừa); formula.1 `VALUES LESS THAN`; formula.5 `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(…))`; formula.3 `DATE '…' + TRUNC(…)`; practice.1 `->>` (A yếu).
- L08: intuition.3 `text.split()` (B yếu); formula.5 `word in d.split()`, `buffer, searchable = [], []`; check.1 `round(x, 3)`; hook.1 "NAPAS" (A yếu).
- L09: formula.6 `return dict(self.doc), self.cas` (B yếu); check.2 `from itertools import permutations`, `;`; sym.1 Couchstore, Magma, Enterprise (A yếu).
- L10: check.5/7/9 `kafka-topics.sh`, `…-console-producer.sh`, `/opt/kafka/bin/` (một phần check.4); formula.6 Avro `record`, `long`; intuition.1 "bộ dọn" (A yếu).
- L11: sym.3 thẻ XML `GrpHdr`, `MsgId`, `CdtTrfTxInf`, `CdtrAgt`, `FinInstnId` (A vừa); sym.3 `ChrgBr` (M vừa; giảng ở intuition.3); `Ccy="USD"`; formula.7 `from decimal import Decimal, ROUND_HALF_UP`, `for c in s:` (A yếu).
- L12: formula.6 `elif`; quymo.5 "nối hai bảng trong CSDL"; sym.2 "VBHN" (A yếu).

## 4. Người học kẹt ở đâu
L00 intuition.2 "blob a9b66cb"; L01 check.2 `for f in (…)`/`if … and not (…)`; L02 check.7 `out = {}`/`out[num], i = …`; L03 formula.5 "mã làm mới"; L04 không kẹt; L05 example.9 `c, _ = nghe.accept()`, `t.recv(64)`; L06 formula.1 `p_amt IS NULL OR p_amt <= 0`, practice.1 cờ `docker run`; L07 formula.5 "biến gắn", formula.1 `VALUES LESS THAN`; L08 không kẹt; L09 formula.6 `return dict(self.doc), self.cas`; L10 check.5 `/opt/kafka/bin/kafka-topics.sh`; L11 sym.3 thẻ XML pacs.008; L12 không kẹt.
