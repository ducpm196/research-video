# fix6_INT — sửa khoá INT theo R4_INT (2026-11-16)

Phạm vi: `lessons/int/L00…L08`, `curriculum/int.yaml`, `labs/INT/L06/{de.md,loi_giai.md}`, sổ `audit/review/screen_code/INT.yaml` (chỉ đổi khoá mục bằng Edit từng mục, không script). Không chạy build/tts/asr/git/docker. Không thêm mục vào `symbols.INT.yaml` / `lexicon_vi.INT.yaml` (không cần: mọi định nghĩa mới đặt tại chỗ trên màn hình, không có thuật ngữ mới đăng ký E52).

## Bài đã đổi (cần requeue): L00 L01 L02 L03 L04 L05 L06 L07 L08 (cả 9)

## Cổng (số thật)
| cổng | kết quả |
|---|---|
| `lv.py lint` từng bài | 9/9: 0 FAIL, 0 WARN (35/34/26/34/31/39/33/37/44 PASS) |
| lời đọc (từ) | L00 2281 · L01 2290 · L02 2289 · L03 2289 · L04 2298 · L05 2287 · L06 2260 · L07 1877 · L08 2289 (≤ 2300) |
| `lv.py curriculum curriculum/int.yaml` | 9 bài, 0 lỗi |
| `tests/test_e52.py` | 0 FAIL |
| `audit/review/screen_code.py check --course INT` | 60 khối — PASS 83 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 |
| `audit/int/verify_int.py` (đã sửa chỉ số step cho khớp bước chèn) | 208 PASS, 0 FAIL |
| `audit/review/check_legal.py` | 0 FAIL (111 lượt dẫn; 8 văn bản CHUA_KIEM giữ nguyên nhãn) |
| `audit/review/lab_gate.py INT` | 9 PASS · 0 FAIL |
| `audit/review/arith_scan.py` | 256 phép tính, 0 FAIL |
| `audit/check_curricula_graph.py` | VER dẫn tới mã không PASS: 0 |
| `lv.py render` | KHÔNG CHẠY ĐƯỢC: lệnh bị cơ chế phân quyền của Claude Code từ chối ("Destructive or Unwanted Actions") khi tôi gọi `tools/lv.py render lessons/int/L00_*.yaml`; BRIEF_FIX_R4 mục 9 cũng cấm render; tôi không tìm đường vòng. Rủi ro tràn bảng: xem "Việc cần người điều phối" |

## Việc đã làm theo mục
1. Mục chưa giảng (đưa về ≈ 0): mọi khối mã Python/Java/PL-SQL/mã giả giờ có bước "Đọc trước …" (bảng viết trong mã → đọc là) đứng TRƯỚC khối mã (L00 quymo; L01 prereq/symbol/example/quymo; L02 chaythat/example (2 bước)/quymo; L03 symbol Zero-Copy/example (2 bước PL/SQL); L04 chaythat/quymo; L05 example (2 bước Java)/chaythat/quymo/mã giả nhúng; L06 symbol/example SQL/quymo (2 bước); L07 quymo; L08 example mã giả/quymo). Token lẻ đã có hàng bảng: `SET NX EX`, `print`, `#`, `import`, `ORDER BY`, `OPEN/LOOP/FETCH/EXIT/CLOSE`, `GREATEST/LEAST`, `l_accounts(i).amount`, `@Contended` + `-XX:-RestrictContended`, `&&`, `==`, `<`, `if/else if/else`, `.size()`, `.rrn`, `moGD++`, `Class<?>[] gt = { Dv.class }`, `Proxy.newProxyInstance(...)`, ép kiểu `(Dv)`, `rollbackFor = Exception.class`, `redis.getOperations().delete`, `serialize`, `sendfile(socket_fd, file_fd, …)`, `ACTP/I/PROCESS//0`, `TRANSACTION.TYPE=AC`, `env/session/shape`, `tong, tang = 0, 1.0`…
   - L01 "khấu hao": giảng tại chỗ bằng lời thường + ví dụ số (cộng chuỗi chép 0+1+…+999 = 499 500 ký tự; StringBuilder gấp đôi 16+32+…+512 = 1 008 ký tự, chia 1000 lần nối ≈ 1 ký tự mỗi lần); thêm 2 phép kiểm vào `checks`.
   - Thuật ngữ định nghĩa một câu tại lần xuất hiện đầu: giải ngân, thu hộ, bội số lương, rút tiền mặt trả góp, thẻ ảo, NHNN, đối soát, hạch toán, trích nợ, thụ hưởng, neo mức đề xuất, HR, ACB, UIT/ĐHQG-HCM, POS/ATM/PIN, ISO 4217/ISO 9564, JEP 444, G1/ZGC, XML, lập lịch, RFC/IETF, DB/UNIQUE, Spring MVC, bắt tay TLS, Controller, Transactional/this, SQL/PL-SQL, TLS client-broker, đám mây, bồi hoàn, rửa tiền, API, p95/p99, if-else, ln N/căn bậc hai (L05, trước công thức), Site Reliability Engineering, 5 Whys, thủ tục lưu trữ…
   - Bảng đứng trước sơ đồ khi sơ đồ dùng từ chưa giải (L00 concept, L06 concept: hoán đổi thứ tự bước); L00 SVG "Inbound" đổi thành "Giao dịch đến".
2. 5 SHOULD: (1) `curriculum/int.yaml` L02 `fix` bỏ ApplicationContext, ghi đúng điều bài dạy (tách sang đối tượng khác); (2) L06 tiêu đề (lessons + curriculum), mục tiêu 1, recap chuỗi + lời đọc không còn hứa "100 câu"; (3) `labs/INT/L06/de.md` dòng 4 ghi "dùng tích chưa làm tròn (0,9995³)", `loi_giai.md` nêu 788,4 nếu dùng 99,85% làm tròn; kiểm lại bằng Python: `525600*(1-0.9995**3) = 788.0`, `525600*0.0015 = 788.4`; (4) L04/L05: không có nguồn kiểm được cho chi tiết OCB → BỎ khỏi cả màn hình lẫn lời đọc ở L04 hook, L05 prereq/check; (5) L04 "năm phần" → "năm nhóm" (cả bảng prereq và lời đọc).
3. P5/P3: L02 quiz Filter/Interceptor — bỏ đoạn in sẵn vị trí khỏi màn hình câu hỏi, thêm vị trí vào bước đáp án kèm "vì sao không chọn B, C, D" (Interceptor chạy sau khi Spring MVC chọn Controller…); L03 hai quiz (SAGA, bế tắc): phương án sai mới là nhầm lẫn thật (SAGA = nhất quán tức thì; tự phối hợp không bù trừ được; tăng thời gian chờ khoá; thêm chỉ mục mọi cột; đọc nhật ký ứng dụng) + dòng giải thích từng phương án sai; L06 quiz 90 ngày thay bằng quiz tính số máy (8 000 tps × 130 ms ÷ 500 + 1 = 4); phương án sai 2 081 (quên đổi mili giây), 3 (quên dự phòng), 17 (quên nhân thời gian ở lại), kèm 5 `checks`; kế hoạch 90 ngày chuyển nguyên nội dung sang bước đầu cảnh recap (mục tiêu 6 → `covers: recap`); L00 scene check: cột "đánh giá" chỉ hiện ở bước đáp án; L03 SVG Outbox/CDC (5 hộp: một giao dịch → WAL → CDC → Kafka → bên nhận, khớp lời đọc); L02 vết REQUIRES_NEW bảng 4 bước + ví dụ bể 2 kết nối treo; L04 lưới 8×8 bản đồ bit (sinh bằng mã, kiểm ghép 8 nhóm = 3020000008001000).
4. Pháp lý: không đụng nhãn "chưa đọc nguyên văn/CHƯA KIỂM"; không thêm số hiệu mới.

## screen_code (sổ INT)
Chèn bước làm lệch chỉ số step nên đổi khoá `INT Lxx <cảnh> <step> <khối>` bằng Edit từng mục (41 khoá + 4 `twin_of` + một ghi chú); không sửa sha, không sửa nội dung mã (không khối mã nào đổi chữ). Kết quả cuối: PASS 83, 0 lỗi (xem bảng cổng). `audit/int/verify_int.py` cũng sửa chỉ số step cố định (PY, L01 example 4, L02 chaythat 2–5).

## Mục chưa giảng còn lại (ước, theo chuẩn P1 chặt)
L00 0 · L01 0–1 · L02 0–1 (CGLIB/JDK, PostConstruct chỉ nêu qua nhãn) · L03 0–1 (WAL/redo, at-least-once chỉ định nghĩa trong hộp) · L04 0–1 (TPK/ZPK/LMK nêu theo lệnh HSM) · L05 0–1 · L06 0–1 · L07 0 · L08 0–1. Ước tính ≥ 8/9 bài ở 0 mục; người đọc vòng 5 sẽ đo.

## Việc cần người điều phối / chưa làm
- Render: chưa chạy (bị chặn quyền). Bảng "đọc trước" dài có thể tràn khung. Điểm nghi: L02 chaythat (đã tách hai bước, bước đầu 5 hàng, bước hai 5 hàng), L01 example (bảng Java 8 hàng), L04 symbol 0 (bảng 7 hàng + khối OFS), L08 example (bảng mã giả 8 hàng), L05 symbol 3. Nếu render FAIL: tách step + `clear: true` hoặc bỏ bớt hàng bảng.
- L03: chưa thêm hình 2PC (chỉ hình Outbox/CDC, theo đề "hoặc").
- Sau dựng lại phải ASR/nghe lại: nhiều câu `say` mới; mục `asr_reviewed` của các câu đã đổi đã bị xoá (E30).
- Tạp vật: tôi ghi nhầm đè một tệp `wc.py` cùng tên trong thư mục scratchpad chung; không ảnh hưởng kho.

## Bổ sung 2026-11-16 (sau bản dựng L00/L01 dừng vì TRÀN bảng)
Render vẫn bị chặn quyền ("Undermining Oversight"), nên sửa mù: tách mọi bảng "Đọc trước" thành bước ≤ 4 hàng (đã có `clear: true`), tách bước bảng+khối mã thành hai bước (bảng rồi mã), thêm `clear: true` vào bước recap L05/L06, rút chữ cột ví dụ ở các bảng dài. Ước lượng độ cao bằng công cụ tự viết (hiệu chỉnh trên khung TRÀN thật của L00/L01 trong audit/int/logs): mọi bước tôi đụng tới còn ≤ ~700 (ngưỡng TRÀN thật ≈ 750–800 theo ước lượng); bước cũ chưa đụng (kiểm tra, bẫy, recap) giữ nguyên.
Bài đổi: L00 (SET tách 2 bước; bảng Python tách 2 bước; bảng mức tải rút chữ), L01 (prereq BigDecimal, symbol B-Tree, bảng Java: mỗi chỗ tách 2 bước), L02 (hook, bảng Java 3 bước + bước 2 tách đôi, Python tách đôi, từ vựng tách đôi, quiz đáp án tách đôi), L03 (Outbox: SVG tách bước riêng; từ Kafka tách đôi; Zero-Copy; PL/SQL bước 3 tách đôi), L04 (MTI tách đôi; OFS; khối PIN; chaythat), L05 (mã giả embedding tách đôi, rút chữ), L06 (mã giả tách đôi, recap `clear`), L07 (Python tách đôi), L08 (từ vựng sản phẩm tách đôi; mã giả hai con trỏ tách đôi).
Sổ screen_code INT: đổi khoá thêm lần nữa bằng Edit từng mục; `screen_code check`: PASS 83, 0 lỗi; `verify_int.py` (chỉ số step cập nhật): 208 PASS; lint 9/9 sạch; lời đọc L00–L08 = 2298/2299/2291/2286/2298/2287/2260/1876/2296 từ; curriculum 0 lỗi; test_e52 0 FAIL.
