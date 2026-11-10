# SC1 nhóm 3 — DBS, INT, ACB, DAN, BNK: 52 khối

Ngày 2026-11-10. Sổ: `audit/review/screen_code/{DBS,INT,ACB,DAN,BNK}.yaml`. Nguồn web truy cập 2026-11-10 (ghi trong `read_check` từng mục); điều chỉ dựa vào trí nhớ được ghi "ghi nhớ, chưa mở" và nằm trong `unverified_claims`.

## 1. Số theo khoá

| Khoá | khối | run | syntax | fragment | output | pseudo | other | unverified_claims |
|---|---|---|---|---|---|---|---|---|
| DBS | 19 | 15 (sqlite) | 0 | 1 | 1 | 2 | 0 | 0 |
| INT | 19 | 1 (sqlite) | 7 (java 5, node 2) | 1 | 0 | 1 | 9 | 31 |
| ACB | 8 | 1 (go) | 1 (go) | 0 | 0 | 0 | 6 | 17 |
| DAN | 5 | 5 (sqlite) | 0 | 0 | 0 | 0 | 0 | 0 |
| BNK | 1 | 1 (sqlite) | 0 | 0 | 0 | 0 | 0 | 0 |
| **Tổng** | **52** | **23** | **8** | **2** | **1** | **3** | **15** | **48** |

Nguồn chạy thêm (sources): DBS 9, INT 8, ACB 3 — đều PASS. Bản dịch đối chiếu (`twin_of`, độ trung thực INFERRED): DBS L10 vòng lồng; INT chiều cao cây, số lô BULK COLLECT, hai con trỏ, mô hình thứ tự khoá; ACB định tuyến ksqlDB (sqlite), khoá lạc quan (sqlite), HMAC.

## 2. Lỗi đã sửa

| Khối | Mức | Trích nguyên chữ (cũ) | Vì sao sai + bằng chứng | Sửa thành | lint/render/verify |
|---|---|---|---|---|---|
| ACB L04 example 3 0 | MUST | `"code": "409", "message": "Hợp đồng tiền gửi đã có giao dịch khác!"` rồi xuống dòng `})` | Go tự chèn dấu chấm phẩy sau chuỗi ở cuối dòng; phần tử cuối của literal nhiều dòng phải có dấu phẩy. `gofmt -e` (Go 1.25.5) trên văn bản cũ: `missing ',' before newline in composite literal`, rc=2 | thêm `,` sau chuỗi message | lint 0 FAIL 0 WARN; render 67 khung, 0 vấn đề (đã xem khung 45); ACB không có bộ kiểm khoá; check_xref 0; lv curriculum acb 0 lỗi; scan_ctrl không có lượt mới (8 lượt `\tat` của JVA) |
| ACB L04 example 3 0 | SHOULD | `if res.RowsAffected() == 0 {` | SQL ở cảnh symbol dùng tham số `:name` (kiểu database/sql/sqlx); `go doc database/sql Result` trên máy: `RowsAffected() (int64, error)` — hai giá trị nên không so được với 0 trong một biểu thức (chỉ đúng nếu dùng pgx CommandTag) | `n, err := res.RowsAffected() // res: sql.Result của câu UPDATE` / `if err != nil { return err }` / `if n == 0 {` | như trên; `say` không đổi (vẫn khớp: "kiểm tra kết quả dòng tác động… nếu số dòng bằng không…") |

## 3. unverified_claims (máy không kiểm được)

Lý do chung: INT/ACB nói về Redis, Spring, Oracle PL/SQL, Kafka, ksqlDB, T24 OFS, ISO 8583, ONNX Runtime, Go Fiber — không có trên máy; tài liệu Temenos và chuẩn ISO 8583/4217 không công khai; nhiều câu là nhận định thiết kế hoặc ví dụ minh hoạ. DBS, DAN, BNK: 0 (mọi điều bài nói về kết quả đều có khẳng định chạy thật).

### INT (31)

- INT L00 example 1 0: Yêu cầu thứ hai (500 ms sau, cùng mã) bị chặn: đúng theo ngữ nghĩa NX trong tài liệu, nhưng không chạy được Redis trên máy
- INT L00 example 1 0: redis.io: mẫu SET … NX EX làm khoá phân tán đơn giản 'is discouraged in favor of the Redlock algorithm' — bài dùng khoá Redis chỉ làm lớp chặn sớm, lớp cuối là UNIQUE ở DB (khối 2 0)
- INT L00 example 2 0: 'Nếu chèn bị lỗi trùng: đọc trạng thái cũ … và trả lại, không trừ tiền lần hai' — logic ứng dụng, không có mã
- INT L00 example 2 0: 'Khi dòng chưa tồn tại, SELECT … FOR UPDATE không khóa được gì' — hành vi khoá dòng của Oracle/PostgreSQL; sqlite không có khoá dòng; với InnoDB (MySQL) ở REPEATABLE READ câu đó còn đặt khoá khoảng (gap lock), nên nhận định này đúng với hệ không khoá khoảng
- INT L01 example 3 0: 'Spring Boot 3.2+' là phiên bản đầu có thuộc tính này — tài liệu đã đọc là bản 4.1.2, không ghi phiên bản đầu (ghi nhớ: ghi chú phát hành 3.2, chưa mở)
- INT L01 example 3 0: 'các thuộc tính bể luồng như server.tomcat.threads.max không còn tác dụng' — tài liệu 4.1.2 nói chung 'properties which configure thread pools don't have an effect anymore', không nêu riêng tên thuộc tính Tomcat
- INT L01 example 3 0: 'Giới hạn đồng thời thực sự là bể kết nối DB (HikariCP)' — nhận định thiết kế, không kiểm được bằng máy
- INT L02 symbol 1 0: 422 = 'yêu cầu đúng cú pháp nhưng không xử lý được' — theo RFC 9110 §15.5.21 (ghi nhớ, chưa mở trong đợt này)
- INT L02 example 1 0: hành vi chạy (khoá đã có → setIfAbsent trả false → 409) — cần Redis và Spring, chỉ kiểm cú pháp/kiểu
- INT L02 example 1 0: setIfAbsent(K, V, long, TimeUnit) bị đánh dấu deprecated từ Spring Data Redis 4.1 (thay bằng setIfAbsent(K, V, Expiration)); bài không nêu phiên bản
- INT L02 example 2 0: giả định stub: debitAndCredit khai throws TimeoutException, ValidationException là ngoại lệ không kiểm tra — mã trên màn hình chỉ biên dịch khi đúng như vậy
- INT L02 example 2 0: trong Spring Data Redis, set/setIfAbsent thuộc ValueOperations còn delete thuộc RedisTemplate — `redis` trên màn hình phải là lớp bọc của ứng dụng; bài không nói
- INT L02 example 2 0: bước 3: 'Redis mất khóa khi failover → Ràng buộc UNIQUE(request_id) ở DB chặn ghi nợ lần hai' — thiết kế, không chạy được
- INT L03 symbol 2 0: sơ đồ 'Disk File -> OS Page Cache -> Network Socket Buffer -> Network Card': mức chi tiết bên trong nhân (có sao chép vào bộ đệm socket hay chỉ mô tả + DMA gather) tuỳ phần cứng/nhân, không kiểm được
- INT L03 example 2 0: 'Oracle không bảo đảm khóa dòng theo thứ tự ORDER BY' — chưa tìm được câu nguyên văn trong tài liệu Oracle
- INT L03 example 2 0: 'ORA-00060 vẫn có thể đến từ luồng khác hoặc FK thiếu index' — chưa mở nguồn
- INT L03 example 2 0: không chu trình giữa các luồng khoá theo cùng thứ tự: kiểm bằng mô hình Python (src:INT:thu_tu_khoa), độ trung thực bản dịch = INFERRED
- INT L03 example 3 0: tham chiếu trường l_accounts(i).amount trong FORALL tĩnh hợp lệ từ Oracle 11g (PLS-00436 được bỏ) — chưa mở nguồn
- INT L03 example 3 0: số lần đổi ngữ cảnh 20 000 / 20 là ước lượng của bài; vòng thật có thêm 1 lần FETCH rỗng cuối (src:INT:L03_so_lo) nên 'khoảng 20' đúng
- INT L04 symbol 0 0: toàn bộ cú pháp OFS và tên trường FT (TRANSACTION.TYPE=AC, DEBIT.ACCT.NO…) — tài liệu Temenos không công khai, chưa kiểm được nguồn
- INT L04 symbol 0 0: ý nghĩa '//0' (GTS control trống, số lần duyệt 0) và version 'ACTP' — chưa kiểm được
- INT L04 symbol 1 0: định nghĩa trường theo ISO 8583:1987 (MTI 0200, F3, F4 n12, F11 n6, F37 an12, F52) — chuẩn không công khai, chưa mở
- INT L04 symbol 1 0: mã xử lý 40xxxx cho chuyển khoản và đặc tả NAPAS 247 — bài tự ghi 'cần kiểm'
- INT L04 symbol 1 0: VND có 0 chữ số thập phân theo ISO 4217 — ghi nhớ, chưa mở bảng ISO 4217
- INT L04 example 2 0: kết quả thuật toán kiểm bằng bản Python đối chiếu (src:INT:L04_hai_con_tro); độ trung thực bản dịch = INFERRED
- INT L05 symbol 2 0: 'Vector Embeddings 384 chiều' — tuỳ mô hình (ví dụ all-MiniLM-L6-v2 cho 384 chiều, ghi nhớ), bài không nêu mô hình
- INT L05 symbol 2 0: hai chuỗi sao kê ví dụ cho cosine ≥ 0,88 — bài ghi 'ví dụ minh họa', không chạy được mô hình
- INT L05 example 1 0: 'Trích xuất đặc trưng ngay trong bộ nhớ, không gọi mạng' — phụ thuộc cài đặt ba hàm (không hiện)
- INT L05 example 2 0: 'Mục tiêu thiết kế: vài mili giây, phải đo bằng benchmark' — bài tự ghi phải đo
- INT L06 symbol 1 0: ngưỡng 10 người — bài ghi 'chỉ là ví dụ minh hoạ'
- INT L06 example 2 0: có vòng chờ khi hai phiên khoá ngược thứ tự: kiểm bằng mô hình Python (src:INT:thu_tu_khoa), độ trung thực = INFERRED

### ACB (17)

- ACB L01 symbol 0 0: cú pháp OFS (thứ tự phần, ký hiệu :MV:SV cho giá trị đa trị/con) — tài liệu Temenos không công khai, chưa kiểm được nguồn
- ACB L01 symbol 0 0: 'Nếu thiếu một dấu phẩy hoặc sai tên trường, T24 sẽ từ chối lệnh và trả về bản tin báo lỗi' — không có T24
- ACB L03 symbol 0 0: lôgic CASE + LEFT JOIN kiểm bằng bản sqlite đối chiếu (src:ACB:L03_dinh_tuyen); độ trung thực bản dịch = INFERRED
- ACB L03 symbol 0 0: ksqlDB yêu cầu nối theo khoá chính của bảng — bảng hồ sơ phải có khoá account_no; bài không nói
- ACB L03 symbol 0 0: giao dịch chưa có hồ sơ khách vẫn được định tuyến SMS/EMAIL với phone_number/email NULL (bản đối chiếu cho thấy) — kênh nhận không có địa chỉ; bài không nói cách xử lý
- ACB L04 symbol 0 0: số dòng tác động 1 rồi 0 kiểm bằng bản sqlite đối chiếu (src:ACB:L04_khoa_lac_quan); độ trung thực bản dịch = INFERRED
- ACB L04 symbol 0 0: hệ quản trị đích (MySQL/PostgreSQL) và kiểu tham số :name — bài không nói; TRANSACTION không phải từ dành riêng ở MySQL/PostgreSQL (ghi nhớ, chưa mở)
- ACB L04 example 3 0: API Fiber v2: c.Status(int) *Ctx, (*Ctx).JSON(any) error, fiber.StatusConflict, fiber.Map — ghi nhớ, không có gói trên máy để biên dịch
- ACB L04 example 3 0: res là sql.Result (chú thích trên màn hình); nếu dùng pgx thì CommandTag.RowsAffected() trả một giá trị và dòng đầu phải viết khác
- ACB L05 symbol 0 0: p_acc_list phải là kiểu tập hợp cấp SQL (CREATE TYPE … AS TABLE OF …) để dùng TABLE(); bài không hiện khai báo
- ACB L05 symbol 0 0: 'Oracle khóa dòng theo đường truy cập của kế hoạch thực thi, không bảo đảm theo thứ tự sắp xếp' — chưa tìm được câu nguyên văn trong tài liệu Oracle
- ACB L05 symbol 0 0: không có vòng chờ khi mọi luồng khoá tăng dần: kiểm bằng mô hình Python src:INT:thu_tu_khoa, độ trung thực = INFERRED
- ACB L06 symbol 0 0: 'Vé có thời hạn hiệu lực tối đa 3 phút' — vé không có trường thời điểm phát hành nên không kiểm được từ khối
- ACB L06 symbol 0 0: 'Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15, hiệu lực 1/1/2026' — chưa mở nguồn
- ACB L07 symbol 0 0: 'X-Event-ID chống gọi lặp' — phụ thuộc bên nhận lưu mã sự kiện đã xử lý; không có mã bên nhận
- ACB L08 symbol 1 0: phong toả/cấp hạn mức trên hệ lõi thật — chỉ kiểm thứ tự lời gọi bằng stub
- ACB L08 symbol 1 0: lỗi của lệnh giải toả bị bỏ qua: nếu giải toả thất bại, sổ vẫn bị phong toả mà không có hạn mức — bài không nói cách xử lý (đối soát/thử lại)

### Quan sát chưa sửa (để người điều phối quyết)
- SHOULD — INT L00 example 1 0 và INT L02 symbol 1 0: dòng chú thích `// …` đặt trong khối lệnh redis-cli (và JSON); redis-cli không có chú thích, gõ nguyên văn sẽ bị báo lệnh lạ.
- SHOULD — ACB L07 symbol 0 0: dòng yêu cầu và header HTTP ghép một dòng bằng ` | `; bản tin HTTP thật mỗi header một dòng.
- SHOULD — ACB L03 symbol 0 0: LEFT JOIN giữ giao dịch chưa có hồ sơ nhưng CASE vẫn chọn SMS/EMAIL với địa chỉ NULL (bản đối chiếu src:ACB:L03_dinh_tuyen: `A4|NULL|SMS_BRANDNAME`).
- Ghi chú — DBS L03 sym 1 0: câu GROUP BY không có ORDER BY; SQLite 3.49.1 in nhóm NULL trước, bảng màn hình xếp K1, K2, NULL (bài không khẳng định thứ tự).
- Ghi chú — INT L02 example 1 0: `setIfAbsent(K, V, long, TimeUnit)` bị đánh dấu deprecated từ Spring Data Redis 4.1.

### Đề xuất cho cổng
- Khối `<div class="code"><code>…<br/>…</code></div>` (ACB L03, L04): bộ trích bỏ qua `<br/>` vì dòng chỉ mở ở `<div>` con, nên văn bản khối có dòng trắng giả giữa mọi dòng (không hiện trên màn hình). Không ảnh hưởng `other`/gofmt, nhưng sẽ làm `fragment`/`output` so sai. Đề xuất: xử lý `<br>` khi khối không có `<div>` con.
- `run/sqlite` dừng ở lỗi đầu tiên nên không kiểm được "lỗi rồi ROLLBACK" trong một khối; đã dùng nguồn Python (src:DBS:L11_rollback). Có thể thêm `expect_state` sau lỗi.
- pycparser không nhận chú thích `//` nên khối kiểu C có chú thích không dùng được `lang: c` (INT L04 example 2 0 phải dùng `node --check`).

## 4. Dòng cuối cổng và bộ kiểm

```
DBS: screen_code: 19 khối — PASS 28 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
INT: screen_code: 19 khối — PASS 27 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
ACB: screen_code: 8 khối — PASS 11 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
DAN: screen_code: 5 khối — PASS 5 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
BNK: screen_code: 1 khối — PASS 1 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
verify_dbs: 42/42 PASS · verify_dan: 13/13 PASS · verify_bnk: 21/21 PASS (bài của ba khoá này không đổi)
ACB: không có audit/acb/verify_*.py; lint L04 0 FAIL 0 WARN; render L04 0 vấn đề; lv curriculum acb 0 lỗi; check_xref ACB 0
```

Bài đã đổi (cần dựng lại): `lessons/acb/L04_san_chuyen_nhuong_hop_dong_tien_gui.yaml` (chỉ `show` cảnh example bước 4; `say` không đổi). Không chạy build/tts/asr, không lệnh git.
