# fix5 phần A: BNX L00–L11 (vòng 5, 2026-11-15)

## TIẾN ĐỘ
- [x] L00 L01 L02 xong
- [x] L03 L04 L05 xong
- [x] L06 L07 L08 xong
- [x] L09 L10 L11 xong
- [x] cổng cuối khoá xong (xem mục 5)

## 1. Bảng từng bài

Cách giảng: bảng "cách viết/nghĩa" đặt ngay trước khối mã/lệnh dùng nó (hoặc hàng thêm vào bảng sẵn có / chú thích dưới khối), kèm một câu lời đọc có "nên/vì". Không đổi chuỗi mã trên màn hình nào, nên `ver/lNN.py` và nội dung khối mã trong sổ screen_code không đổi (không bỏ mục nào khỏi màn hình). Lời đọc: số từ đếm tách khoảng trắng toàn bộ `say`.

| Bài | Mục P1 đã giảng (trong video) | Còn lại (ước lượng) | Từ lời đọc trước → sau | lint | render | verify_bnx | screen_fast |
|---|---|---|---|---|---|---|---|
| L00 | `cat`, `&&`, `git log --format="%H %s"` (%H, %s), SHA-1 (thuật toán băm, 160 bit, cả ở prereq và `hashlib.sha1`) | 0 | 2418 → 2297 | 0 FAIL/0 WARN/36 PASS | 0 vấn đề (112 khung) | 19/19 | 14 khối: PASS 15 |
| L01 | `import re` + `re.compile(r"…")`, `[] if ok else […]`/`400 if loi else 201`, `chan += bool(…)`, `loi.append`, `a is None or (…)`, `enumerate` | 0 | 2383 → 2294 | 0/0/42 | 0 (113) | 20/20 | 13 khối: PASS 14 |
| L02 | định nghĩa JSON (prereq), `.encode()`, `import json`+`json.dumps`, dict comprehension + `.items()` + từ điển tra, `break`/`None`/`def`, cú pháp `.proto` (`syntax`, `message`, `int64`, `string`, `rpc`), `def/return` | 0 | 2440 → 2298 | 0/0/46 | 0 (115) | 20/20 | 17 khối: PASS 18 |
| L03 | `hmac.compare_digest` (dời bảng lên trước example step 12), `\` nối dòng + `-binary` + `echo`, `d, t, s = ma.split(".")`, `json.loads`, `c.get` | 0 | 2445 → 2292 | 0/0/59 | 0 (107) | 21/21 | 13 khối: PASS 14 |
| L04 | `%` (`i % (ttl-som)`), `while`, `+=`, base64url (prereq nhắc "cơ số 64 an toàn cho đường dẫn, như bài 3") | 0 | 2453 → 2288 | 0/0/37 | 0 (108) | 23/23 | 10 khối: PASS 11 |
| L05 | `openssl req -x509 -newkey ed25519 -noenc -subj -days -addext -keyout -out`, `\`, `-CA`, `create_default_context(CLIENT_AUTH)`, `load_cert_chain/load_verify_locations`, `wrap_socket(…, do_handshake_on_connect=False)`, `dict(x[0] for x in …["subject"])`, `getattr(e, "verify_message", e.reason)`, `date.fromisoformat`/`timedelta`/`.days` (hộp "Nếu kẹt" có ví dụ 2026-04-20 + 60 ngày) | 0–1 (mã socket/luồng vẫn ở mức khái niệm) | 2416 → 2298 | 0/0/35 | 0 (117) | 21/21 | 12 khối: PASS 14 |
| L06 | bảng "đọc câu SQL" (SELECT/FROM/WHERE, UPDATE, `SUM … AS`, `ORDER BY`, `\|\|`), `isolation_level=None`, `set_trace_callback`, `for _ in range(n)`, `.values()`, từ điển, `def/return` | 0 | 2265 → 2262 | 0/0/38 | 0 (129) | 22/22 | 20 khối: PASS 24 |
| L07 | bảng "đọc câu SQL" (SELECT COUNT/FROM/WHERE/AND, INSERT…SELECT, ALTER TABLE…DROP PARTITION FOR), `CASE WHEN`, thoát nháy `''`, bảng lệnh Docker (`run -d --name -p -e`, `logs -f`, `exec -it … sqlplus`) | 0 | 2329 → 2273 | 0/0/39 | 0 (126) | 26/26 | 24 khối: PASS 25 |
| L08 | `def … return`, `f"tx{i}"` (cả ở check và quymo), `enumerate(mo_ta)`, `x if c else y`, chạy `python mau.py` (hộp "Nếu kẹt") | 0 | 2416 → 2299 | 0/0/41 | 0 (141) | 30/30 | 13 khối: PASS 20 |
| L09 | `while chua:`, `continue`, `x = a if c else b`, `[s.get() for _ in range(chua)]` và `_`, `def f(order, cas_on): … return v`, `p not in rd`, `.startswith` | 0 | 2443 → 2286 | 0/0/41 | 0 (137) | 23/23 | 10 khối: PASS 16 |
| L10 | `printf '%s\n' … \| docker exec -i …` (printf, ống, `-i`), `--property parse.key/key.separator/null.marker`, `sleep 2`, `--bootstrap-server`, `--topic`/`--create`/`--config`, `--partition/--offset/--timeout-ms`, `print.key/print.offset/null.literal`, `range(len(log)-1, -1, -1)`, `seen`, `f"TK{i % 100}"` | 0–1 (bên trong Kafka/Avro vẫn ở mức khái niệm) | 2444 → 2297 | 0/0/39 | 0 (144) | 30/30 | 16 khối: PASS 23 |
| L11 | `Decimal(1).scaleb(-2)`, `def tron(x, ccy): … return`, `for _ in range(n)`, gán đôi `f, d = 0.0, Decimal(0)`, `f += 0.10` | 0 | 2398 → 2284 | 0/0/52 | 0 (127) | 34/34 | 10 khối: PASS 16 |

Mọi bài ≤ 2300 từ (cao nhất L08 2299, L02 2298, L05 2298). Mọi `say` ≤ 38 từ và ≤ 170 ký tự (lint 0 WARN/0 FAIL). Ước lượng P1 sau sửa: ≥ 1 ở cả 12 bài, = 2 ở khoảng 10–12 bài (L05, L10 còn rủi ro =1 vì API ssl/Kafka chỉ giảng một dòng mỗi lệnh); chưa có người đọc lại. Các mục "bỏ khỏi màn hình" (phương án c): không dùng; phương án (b) đơn giản hoá mã: không dùng (tránh đổi sổ/ver).

Ghi chú tuỳ chọn: khung đã xem bằng mắt: L00 00028, L03 00055, L05 00043, L07 00094, L09 00075 (đều gọn, không tràn). Các bài khác chỉ có kết quả `render` 0 vấn đề (L08 lần đầu có 5 khung practice tràn do thêm một dòng ghi chú, đã gỡ và đưa vào hộp "Nếu kẹt"; L10 lần đầu có 6 khung formula tràn do thêm ghi chú "xoá trường", đã tách thành step riêng).

## 2. Bài nào đổi → cần dựng lại (build/tts/asr)
TẤT CẢ 12 bài L00–L11 (lời đọc, bảng màn hình đổi). Số câu `say` mới/đổi rất nhiều: dựng lại cả bài. Lab (`labs/BNX/L00..L11`, `de.md`, lời giải) KHÔNG đổi nội dung; `lab_gate BNX`: 39 PASS · 0 FAIL (196 lab).

## 3. SHOULD đã sửa / không sửa
Đã sửa hết các mục thuộc L00–L11:
- L00 quiz câu 2: đề viết rõ "gộp nhánh X, đã có 2 commit riêng chưa nằm trong 4 commit đó, vào main" (khớp lời giải 4+2+1=7); lời đọc cũng nói rõ.
- L01 quymo step 4: lời đọc "với năm mươi thì không thể bắt cùng đổi một ngày, với năm trăm thì bắt buộc chạy song song hai phiên bản".
- L09 formula step 5: tag focus sửa theo số dòng thật của khối `Store` (`[2.3]` khởi tạo, `[2.4]` `def get`, `[2.6]` `def replace`); trước đó câu về `get` sáng nhầm `def replace`.
- L09 quiz: đề và đáp án câu 3 đổi "200 yêu cầu mỗi giây" thành "nếu 200 yêu cầu đến cùng lúc" (nhất quán với bảng quymo), cả lời đọc.
- L10 formula step 5: thêm (màn hình + lời đọc) "ở mức xuôi chỉ bị chặn nếu trường bị xoá không có giá trị mặc định", ở một step riêng; lời đọc nói lý do "bên đọc mới bỏ qua trường thừa".
- L10 prereq step 0 ý 2: thêm "khi số phân vùng không đổi" (màn hình + lời đọc).
- L02 pitfalls/sym: "đóng vai hợp đồng như đặc tả ở bài trước" → "đóng vai hợp đồng giữa bên gửi và bên nhận" (câu đứng một mình). Câu này nằm ở cảnh `sym` step 1 (không phải example).
Không sửa: không có.

## 4. Thay đổi tệp chung / ngoài `audit/bnx/src/lNN.py`
- `tools/registry/symbols.BNX.yaml`: KHÔNG sửa (không thêm `term:` nào; các từ nền như SQL/JSON/Docker/REST bị L12–L38 dùng).
- `audit/bnx/ver/lNN.py`: KHÔNG sửa (không có số/đầu ra mới; chuỗi mã không đổi).
- `audit/review/screen_code/BNX.yaml` (sổ chung): KHÔNG sửa tay (bị chặn quyền).
- `audit/bnx/screen/l00.yaml … l11.yaml`: sinh lại bằng `screen_keep.py` (khớp theo sha; "chưa khớp 0" ở cả 12 bài) rồi `screen_fast.py` (bảng ở mục 1). Một sửa tay duy nhất: `audit/bnx/screen/l05.yaml`, nguồn `src:BNX:L05_certs`, tham chiếu `files:` `ca.sh/may.sh/xau.sh` từ `example 0 0/1 0/2 0` sang `example 1 0/2 0/3 0` (chèn bảng lệnh openssl làm lệch step; `screen_keep` không dịch được khoá trong `sources`). Ghi chú tự do (`note`) trong `screen/l05.yaml` còn nhắc "example 6 0" cũ — không ảnh hưởng cổng.
- Công cụ tạm nằm ở `…/scratchpad/bnxA_fix5/` (gate.sh, wc.py, steps.py); không có trong repo.

## 5. Cổng cuối khoá (số thật, chạy 2026-11-15)
- `lv.py lint` L00–L11: tất cả 0 FAIL, 0 WARN (số PASS: 36, 42, 46, 59, 37, 35, 38, 39, 41, 41, 39, 52).
- `lv.py render` từng bài: 0 vấn đề (số khung ở mục 1).
- `verify_bnx.py` từng bài: tất cả PASS, không SKIP (L10 30/30 chạy cả đường Kafka Docker thật trong `ver/l10.py`).
- `screen_fast.py` từng bài: FAIL 0, STALE 0, MISSING 0, ORPHAN 0 (L05 lúc đầu FAIL 1 vì khoá `files:`, đã sửa).
- `audit/review/lab_gate.py BNX`: 39 PASS · 0 FAIL (196 lab).
- `tests/test_e52.py`: 0 FAIL. `arith_scan.py`: 246 phép tính, 0 FAIL. `check_course_refs.py BNX`: 0 vấn đề. `check_next_refs.py`: 550 lời hẹn, 0 lệch. `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 0 lỗi.
- KHÔNG chạy: build/tts/asr, git ghi, docker trực tiếp, `screen_code.py check --course BNX` (cả khoá).

## 6. Việc điều phối cần làm
1. Gộp sổ: `python -B audit/bnx/screen_try.py --merge` (hoặc gộp tay `audit/bnx/screen/l00..l11.yaml`) vào `audit/review/screen_code/BNX.yaml`. Các khoá cũ của L01–L11 (và mọi khoá có chỉ số step lệch sau chỗ chèn) trong sổ chung hiện STALE/MISSING/ORPHAN cho tới khi gộp; L00 không đổi chỉ số step nhưng nên gộp luôn. Cần bỏ khoá cũ mồ côi sau khi gộp. Không có khối nào cần stub (CHƯA KHỚP = 0).
2. Sau gộp chạy `screen_code.py check --course BNX` (≈ 12 phút, cần Docker) để xác nhận L00–L11.
3. Dựng lại build/tts/asr cho cả 12 bài; nghe lại các câu `say` đổi, nhất là các câu có "ba mươi sáu", "ổ cắm", "mã máy khách", "hệ thống dòng lệnh" (từ mới trong bảng giải nghĩa). Lời đọc đã tránh chữ Latin chưa có luật (ed25519, base64url, printf, sleep, scaleb, Windows đều không đọc thành tiếng).
4. Tên tệp tạm trong scratchpad dùng chung với tác tử khác từng trùng (`gate.sh`, `g_L11.txt`); tôi đã chuyển sang thư mục riêng `bnxA_fix5/`, nhưng nếu thấy log lạ ở `g_L*.txt` thì đó là của nhóm khác.
