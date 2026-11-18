# R4 ACB L00–L08 (vòng 4, đọc độc lập): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (ab714dd99a8726ef9)

## 1. Tóm tắt
spec khớp 9/9; SRT khớp 9/9; lab ĐÚNG 9/9 (mong_doi khớp màn hình 9/9); 21/21 khối mã Python khớp; 178/178 `checks` đúng; 16/16 số tự tính đúng. Go (L04, L08) biên dịch với thư viện giả lập (Fiber/T24 thật không chạy); PL/SQL (L05), ksqlDB (L03) chỉ đọc.
MUST: 8/9 bài =0; **L08 có 1 MUST (PLAUSIBLE)**: giáo án/hook hứa "thấu chi lương" mà bài không dạy. SHOULD 7 + 1 cấp khoá.
P1=2: 0/9 theo cả hai cách đếm. P1 (chắc+vừa): L00=1, L01=1, L02=1, L03=0, L04=0, L05=1, L06=1, L07=0, L08=1. Tính cả mục yếu: cả 9 = 0. P8=2 9/9; P9=2 9/9.
Mất gốc (chắc+vừa): ĐỦ 4 (L01, L02, L06, L08), GẦN 5. P3=1 ở L00, L02, L03, L05, L07 (cơ chế cốt lõi không có hình: bản đồ bit, vòng chờ khoá, hai con trỏ; sơ đồ bốn khối chỉ là khối chữ không đầu mũi tên). P5=1 L00 (câu 2 dài, nghỉ 15 giây). P2=1 L05 (FORALL "45 giây xuống 1 giây" không có phép tính). P7=1 L08.
Gốc P1: cả khoá không giảng cách tạo/chạy một tệp `.py` hay lệnh `bash labs/cham.sh` (lệnh `python mau.py` chỉ có trong de.md) — lặp ở cả 9 bài; Python/SQL nền (`while`, `CREATE TABLE`/`INSERT INTO`/`fetchone`, `a if c else b`, `b""`/`.encode()`, `.get`, `for a, b in …`) không có bảng cách đọc ở bài nặng mã (L03, L04, L07). "đối soát" dùng từ L00 nhưng giảng ở L07.

## 2. Chuẩn xác
| Bài | Mức | Cảnh/step | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | SHOULD | quymo s0 | "một triệu lần ghi khoá mỗi giây khó dồn vào một cụm Redis, nên phải chia dữ liệu theo tài khoản" | số thực tế không nguồn; Redis Cluster đã chia khoá qua nhiều nút nên "một cụm" mơ hồ | "số minh hoạ, cần đo" / nói "một nút" | PLAUSIBLE |
| L02 | SHOULD | quymo s0 | "nút nghẽn là thông lượng ghi 800 000 lần mỗi giây" | cùng loại, không nguồn | như L00 | PLAUSIBLE |
| L02 | SHOULD | concept | sơ đồ: tầng 3 Core, tầng 4 NAPAS Switch | L00 đặt tầng 3 NAPAS, tầng 4 Core; không giải thích | một câu nói đây là luồng khác | CONFIRMED |
| L03 | SHOULD | concept s0, khung 18–25 (zoom 22) | "Ưu tiên mã dùng một lần (OTP)" | chữ rộng hơn ô 3; đường nối cam/xanh cắt qua chữ "Ư" và ")" | rút gọn chữ hoặc nới ô | CONFIRMED |
| L04 | SHOULD | practice s0 | "sổ 300 000 000 đồng, lãi 6,8% một năm; rút ở ngày 200…" | de.md ghi "kỳ hạn 12 tháng" nhưng màn hình không ghi | thêm "kỳ hạn 12 tháng" | CONFIRMED |
| L07 | SHOULD | quymo s1 | "Mã sự kiện webhook chỉ nhớ 24 giờ trong bộ nhớ đệm" | cảnh trước chỉ đặt `EX 120` cho `va:dedup`; TTL 24 giờ xuất hiện lần đầu, không nguồn | nêu "giả định 24 giờ" | CONFIRMED |
| L08 | **MUST** | hook s1; concept s1 | "Hôm nay, ta làm chủ: … Thấu chi lương tín chấp"; lời "làm chủ nghiệp vụ thấu chi cầm cố sổ tiết kiệm và thấu chi lương theo lô" | giáo án/hook hứa dạy thấu chi lương; bài chỉ có 1 dòng bảng ("bội số lương 2 đến 3 lần") + 1 dòng vai trò; không ví dụ/số/cơ chế | thêm cảnh có số HOẶC bỏ lời hứa khỏi hook/tiêu đề/curriculum | PLAUSIBLE |
| L08 | SHOULD | recap s0 | "Thu nợ định kỳ Auto-Debit"; "chuyển tiền qua NAPAS khi khách lệnh" | Auto-Debit không dạy ở đâu trong khoá; câu thứ hai cụt chữ | bỏ Auto-Debit hoặc giảng; sửa câu | CONFIRMED |
| Cấp khoá | SHOULD | quiz L01–L07 | đáp án đúng đều là A | 7/8 câu trắc nghiệm đáp án A (L08 là B; L00 hai câu mở) | xáo thứ tự đáp án | CONFIRMED |
Không kiểm được nguồn (giữ nhãn): TT 50/2024, TT 77/2025, QĐ 2345, Luật 91/2025/QH15, ngày hiệu lực 01/03/2026, bản hợp nhất 25/VBHN-NHNN (L06; bài tự ghi "chưa đọc nguyên văn"); cú pháp OFS (L01); "Oracle khoá dòng theo đường truy cập, không theo ORDER BY" (L05; đã dẫn Oracle 19c PL/SQL Reference). Không có `audit/acb/sources*.md`.

## 3. Mục chưa giảng (P1 chặt) — số mục (chắc+vừa / tính cả yếu): L00 2/6, L01 2/5, L02 2/7, L03 3/7, L04 4/10, L05 1/5, L06 2/7, L07 3/10, L08 2/9 (tổng 21 / 66)
Loại A chưa giảng đâu; M giảng muộn cùng bài; B giảng ở bài trước, bài này không nhắc. Bảng cách đọc có phủ: không (trừ nhóm riêng bên dưới).
- L00: "đối soát liên ngân hàng" (A vừa; chỉ định nghĩa ở L07); practice s1 "Chấm bằng Git Bash: bash labs/cham.sh ACB L00 mau.py" (không nói cách chạy `mau.py`; A vừa); `print(tong, "ms")`, "SQL Server", "trình chứng chỉ số", "khối mã PIN" (A yếu).
- L01: code s0 `return ",".join([...])` (vừa); code s1 `for cid, kq in tra_loi:` và `tra_loi = [("c2","OK"),...]` (vừa); `len(cho)`, "kết quả đối soát chính xác", chân trang cham.sh (yếu).
- L02: example s1 "Lệnh thực thi nguyên tử" (A vừa; giảng ở L03); "dịch mã PIN" giảng muộn ở quiz s2 (M vừa); "cụm Gateway", "Socket TCP nhị phân", "kênh truyền nhị phân", `return False/True`, "đối soát cuối ngày/tự động ba bên", chân trang (yếu).
- L03: code s1 `while hang:` (chắc); code s0 `for co_app, tien in [(True, 20000), …]:` (vừa); symbol `AS target_channel` (vừa); `FROM`, `ELSE … END`, `{event_id}` trong `SET noti:sent:{event_id} 1 EX 86400 NX`, `return "OTT_PUSH"`, chân trang (yếu).
- L04: code s0 `db.execute("CREATE TABLE so (id INT, ver INT)")`, `INSERT INTO so VALUES (1, 7)`, `db.execute("SELECT ver FROM so").fetchone()[0]` (chắc); code s2 `"cho phep" if (tu, den) in CANH else "tu choi"` (chắc); `":memory:"`, `import sqlite3`, `CANH = {("CHAO_BAN","PROCESSING"), …}`, "chờ đối soát tự động", `return`, chân trang (yếu).
- L05: code s2 `cho.get(cho["A"]) == "A"` (chắc); `AS acc`, `sorted([1, 2])`; `a_can, b_can = sorted(...), sorted(...)`, `return "duoc"`, chân trang (yếu).
- L06: code s1 `KHOA = b"bi-mat-may-chu"`, `nd.encode()` (chắc); code s0 `0 if quet else tong + tien`; `"quet mat" if quet else "thuong"` (chắc); `import hashlib, hmac`, `set()`, `.add(...)`, `hmac.compare_digest`/"hàm so sánh an toàn thời gian", `return`, chân trang (yếu).
- L07: code s3 `while i < len(a) and j < len(b):` (chắc); example s3 "duyệt tịnh tiến O(N)" giảng muộn ở quiz s0 (M vừa); "Có quyết toán", "NAPAS Clearing File" (vừa); `elif`, `len(a)`, `LIKE '8888%'`, chuỗi JSON `'{"va": "888800123456", "tien": 1000000}'`, "ràng buộc duy nhất", `return "200 OK, bo qua"`, chân trang (yếu).
- L08: recap "Thu nợ định kỳ Auto-Debit" (A chắc); code s2 `db.execute("INSERT INTO giai_ngan VALUES ('K1', 50000000)")` (B vừa); `err := …` rồi `err = …`, `try: … except sqlite3.IntegrityError:`, `import sqlite3`, `":memory:"`, "ghi lại để đối soát", "Trích xuất hạn mức thẻ khả dụng sang tiền mặt", "phát hành thẻ ảo", `return ["khoa so", …]`, chân trang (yếu).
Đã được bảng cách đọc phủ (không tính): L03 ksqlDB (`LEFT JOIN`, `EMIT CHANGES`, `SELECT`, `CASE WHEN`, `ON`, bí danh `e.`/`p.`); L04 Go (`:=`, `nil`, `err != nil`, hàm trả hai giá trị) và SQL (`:id`, `?`, `.rowcount`, `(7,)`); L05 PL/SQL (`TABLE(p_acc_list)`, `column_value`, `ORDER BY 1`, `r.acc`, `INTO`); L08 Go (`err != nil`, `ctx`, nhắc lại một dòng).

## 4. Người học kẹt ở đâu
L00 practice s0/s1 (tạo/chạy `mau.py`, `bash labs/cham.sh`); L01 code s1 `for cid, kq in tra_loi:`; L02 example s1 "Lệnh thực thi nguyên tử … SET … NX EX 60" (nhẹ); L03 symbol `AS target_channel` (nhẹ), kẹt thật code s1 `while hang:`; L04 code s0 `CREATE TABLE`/`INSERT INTO`; L05 code s2 `cho.get(…)`; L06 code s1 `b"…"`, `.encode()`; L07 code s3 `while i < len(a) and j < len(b):`; L08 code s2 `INSERT INTO giai_ngan …`, recap "Auto-Debit". Số tương tác khung hình: không chữ tràn/cắt ngoài L03 khung 22 (đè chữ); nửa dưới khung thường trống.
