# R5 BNX_A — Kiểm tra độc lập từng mục sau `fix6_BNX_A` (L00–L12)

Phạm vi kiểm tra (chỉ đọc, không chạy Docker / `dbrun.py` / sửa tệp):
- Đặc tả: `lessons/bnx/L00_*.yaml` .. `L12_*.yaml`
- Đầu ra dựng: `out/BNX/L00`..`L12` (`build_report.json`, `Lxx.srt`, `asr_report.md`, `frames/*.png`; không có `build_report.md`)
- Đối chiếu từng mục với `audit/review/audit_final/reports/R4_BNX_A.md` và `fix6_BNX_A.md` (`p1`, `p2`, `p3`).

---

## 1. Tóm tắt kết quả

| Hạng mục | Kết quả | Chi tiết |
|---|---|---|
| Freshness (`spec_sha256`, `tts_sha256`, `frames`) | **PASS 13/13** | `spec_digest(spec) == build_report.json["spec_sha256"]` và `tts_digest(frames) == build_report.json["tts_sha256"]` cho cả 13 bài L00–L12; `mtime` của YAML mới hơn ở một số bài chỉ do cập nhật `asr_reviewed` (không ảnh hưởng `spec_sha256`). |
| Khớp phụ đề (`Lxx.srt` vs `say`) | **PASS 13/13** | 100% số khung hình (`113, 118, 119, 110, 108, 126, 133, 127, 142, 136, 143, 129, 107`) và từng câu phụ đề khớp tuyệt đối giữa `lv.build_frames(spec)` và `out/BNX/Lxx/Lxx.srt` (0 thừa, 0 thiếu). |
| `tools/lv.py lint` (chỉ đọc) | **PASS 13/13** | 0 FAIL, 0 WARN (PASS: L00 36, L01 42, L02 46, L03 59, L04 37, L05 35, L06 38, L07 39, L08 41, L09 41, L10 39, L11 52, L12 52). Tổng từ đọc mỗi bài: `2286–2300` (mọi bài ≤ 2300). |
| ASR sau dựng lại | **PASS 13/13** | `out/BNX/L00..L12/asr_report.md`: `thiếu audio: 0`, `chưa xem xét: 0` ở cả 13 bài. |
| SHOULD R4 (5/5 mục) | **ĐÃ 5/5** | L00 `quiz.1/3`, L04 `intuition.1`, L06 `practice.1/4`, L11 `quymo.3`, L11 `formula.7`/`recap.1` đều đã sửa đúng. |
| Mục P1 R4 (`chắc` + `vừa` + `yếu`) | **ĐÃ 100%** | Toàn bộ 12 mục `chắc`/`vừa` và các mục `yếu` trong R4 mục 3 đều đã được giải thích trước/tại chỗ trong YAML và hiển thị rõ trên khung hình. |
| Nhãn pháp lý & nguồn | **GIỮ NGUYÊN 100%** | Không mất, không thêm số hiệu/điều mới; giữ nguyên nhãn `"bản 08"` (L01), `TT 64/2024/TT-NHNN` (L04), `22/11/2025` + `MT103/MT202↔pacs.008/009` (L11), các nhãn `"cần kiểm lại"` / `"nguồn tổng hợp, cần kiểm lại"` (L12). |
| Kiểm tra PNG các bảng/SVG mới & chưa xem ở R4 | **SẠCH** | Đã đọc trực tiếp 30 khung PNG trọng điểm (bao gồm 6 sơ đồ `intuition` R4 chưa xem ở L03, L05, L08, L10, L11, L12 và toàn bộ bảng/SVG mới của L00–L12): không tràn khung, không đè nét, chữ rõ. |

> **Lưu ý từ R4/fix6 giữ nguyên trạng:** Khối mã thật Oracle (L06, L07) và Kafka Docker (L10) vẫn `NOT_VERIFIED` chạy thật trong phạm vi phiên chỉ đọc này (gộp kết quả Docker ở bước người điều phối); `L00 example.7` (ghi chú R4 về khoảng trắng đồ thị git) và `labs/BNX/L00/de.md` (`$(…)`, ngoài đường chính) giữ nguyên theo phạm vi giao.

---

## 2. Freshness, SRT & Pháp lý/Nguồn (L00–L12)

| Bài | Số từ `say` | `spec_sha256` khớp | `tts_sha256` khớp | Khung PNG / `build_report` | `SRT` khớp `say` | ASR `chưa xem xét` | Nhãn pháp lý/nguồn |
|---|---|---|---|---|---|---|---|
| L00 | 2286 | Đúng (`9d9d8fe029`) | Đúng | 113 / 113 | Khớp 100% | 0 (113 câu) | Không có nhãn pháp lý riêng |
| L01 | 2295 | Đúng (`f795c9a35f`) | Đúng | 118 / 118 | Khớp 100% | 0 (118 câu) | Giữ `"bản 08"` (`formula.5`, dòng 365) |
| L02 | 2296 | Đúng (`c1dbae9e25`) | Đúng | 119 / 119 | Khớp 100% | 0 (119 câu) | Không có nhãn pháp lý riêng |
| L03 | 2298 | Đúng (`442a559cd7`) | Đúng | 110 / 110 | Khớp 100% | 0 (110 câu) | Nguồn RFC giữ nguyên (`source` + `example.1/2`) |
| L04 | 2293 | Đúng (`571f60a452`) | Đúng | 108 / 108 | Khớp 100% | 0 (108 câu) | Giữ `Thông tư 64/2024/TT-NHNN` (`hook.1`, dòng 71) |
| L05 | 2297 | Đúng (`4d2cbee248`) | Đúng | 126 / 126 | Khớp 100% | 0 (126 câu) | Giữ `source` RFC 8446 / Python 3.13 |
| L06 | 2291 | Đúng (`6820de5936`) | Đúng | 133 / 133 | Khớp 100% | 0 (133 câu) | Giữ `source` Oracle 23 / 26ai Free |
| L07 | 2297 | Đúng (`a1a09beda9`) | Đúng | 127 / 127 | Khớp 100% | 0 (127 câu) | Giữ `source` Oracle 23 / 26ai Free |
| L08 | 2300 | Đúng (`7617dda6b4`) | Đúng | 142 / 142 | Khớp 100% | 0 (142 câu) | Giữ `source` Elasticsearch docs |
| L09 | 2297 | Đúng (`748ef5cbd4`) | Đúng | 136 / 136 | Khớp 100% | 0 (136 câu) | Giữ `source` Couchbase 8.0 / SDK 3.13 |
| L10 | 2292 | Đúng (`31bd46ebec`) | Đúng | 143 / 143 | Khớp 100% | 0 (143 câu) | Giữ `source` Kafka 4.4 / 3.9.0 / RabbitMQ 4.4 |
| L11 | 2300 | Đúng (`ef01877a8a`) | Đúng | 129 / 129 | Khớp 100% | 0 (129 câu) | Giữ `22/11/2025`, `MT103↔pacs.008`, `MT202↔pacs.009` (`hook.2`, `intuition.3`) |
| L12 | 2296 | Đúng (`a7171089f3`) | Đúng | 107 / 107 | Khớp 100% | 0 (107 câu) | Giữ nguyên mọi nhãn `"cần kiểm lại văn bản hiện hành"`, `"kiểm lại trước khi áp dụng"`, `"đã sửa đổi, cần kiểm lại"`, `"thay luật cũ từ 01/7/2026; nguồn tổng hợp, cần kiểm lại"` (`sym.2/3`, `intuition.2`, `formula.5`, `pitfalls.3`, `source`) |

---

## 3. Kiểm tra từng mục SHOULD của R4 (5/5)

*Ghi chú quy ước đánh số step trong báo cáo: dùng **1-based** theo cách ghi của R4 (`scene.1`, `scene.2`…), kèm tên cảnh YAML và số dòng.*

1. **L00 `quiz.1` câu 2 (thiếu điều kiện để không fast-forward) — `ĐÃ`**
   - File & bước: `lessons/bnx/L00_git_nhanh_gop_xung_dot.yaml`, `quiz.1` (dòng 628–631) và `quiz.3` (dòng 652–669).
   - Nội dung xác minh: Đề `quiz.1` đã thêm điều kiện `main cũng đã có commit mà X chưa có` (kèm lời đọc `quiz.1`). Đáp án `quiz.3` giữ `4 + 2 + 1 = 7 commit, 2 cha` và bổ sung ghi chú + lời đọc rõ ràng: nếu `main` không có commit mới thì Git tua nhanh thành `4 + 2 = 6` commit, không có commit gộp.
2. **L04 `intuition.1` (đường đời nét đứt gạch qua chữ nhãn trình tự) — `ĐÃ`**
   - File & bước: `lessons/bnx/L04_oauth2_openid_connect.yaml`, `intuition.1` (dòng 203–236); PNG: `out/BNX/L04/frames/00021.png`.
   - Nội dung xác minh: Nhãn `①`–`⑤` đặt ở `x=749` (chính giữa hai đường đời `x=563` và `x=936`), nhãn `⑤` rút gọn thành `⑤ mã truy cập (+ mã định danh)` (phần `nếu xin phạm vi openid` giữ ở `say`), nhãn `⑥` ở `x=1122` giữa `x=936` và `x=1309`. Kiểm tra trực tiếp PNG `00021.png`: không một nhãn nào bị đường nét đứt gạch qua.
3. **L06 `practice.1` (khối chữ xám nhỏ 7 dòng lệnh Docker) — `ĐÃ`**
   - File & bước: `lessons/bnx/L06_thu_tuc_luu_tru_plsql_tsql.yaml`, `practice.1` (dòng 745–746) và `practice.4` (dòng 785–797); PNG: `out/BNX/L06/frames/00115.png`, `00125.png`.
   - Nội dung xác minh: `practice.1` bỏ đoạn lệnh Docker chữ xám nhỏ, chỉ trỏ `xem lệnh Docker ở cuối phần này`; `practice.4` tách riêng thành bảng 3 hàng cỡ chữ bình thường (`docker run`, `docker logs ora-thu`, `docker exec -it ora-thu sqlplus`). Kiểm tra PNG `00115.png` và `00125.png`: gọn, dễ đọc.
   - Ghi nhận nhỏ (không chặn): khác với `L07 practice.5` có thêm khối mã chép-dán `ORACLE_PASSWORD=...`, `L06 practice.4` vẫn để `-e …` và `bnx/…` theo đúng khung bảng `L07 practice.4` như R4 đề xuất.
4. **L11 `quymo.3` (15 USD trung gian và 20 USD phí cố định chung hàng không giải thích) — `ĐÃ`**
   - File & bước: `lessons/bnx/L11_thanh_toan_quoc_te_ngoai_te.yaml`, `quymo.3` (dòng 606–617); PNG: `out/BNX/L11/frames/00086.png`.
   - Nội dung xác minh: Tiêu đề cột đổi thành `thiếu so với hoá đơn (phí trung gian 15)` và `một phí cố định khác, 20 USD, chiếm (số minh hoạ)`; lời đọc ghi rõ `"Phí cố định hai mươi đô la là một khoản khác với mười lăm đô la của trung gian"`. PNG `00086.png` rõ ràng, không tràn.
5. **L11 `formula.7` (lời đọc) & `recap.1` (chuẩn ISO 4217 vs làm tròn) — `ĐÃ`**
   - File & bước: `lessons/bnx/L11_thanh_toan_quoc_te_ngoai_te.yaml`, `formula.7` (dòng 431) và `recap.1` (dòng 785–786).
   - Nội dung xác minh: `formula.7` `say` đổi thành `"số chữ số lẻ theo chuẩn ISO bốn hai một bảy, làm tròn nửa lên"`; `recap.1` màn hình ghi `"số thập phân, số chữ số lẻ theo ISO 4217, làm tròn nửa lên"`.

---

## 4. Kiểm tra toàn bộ mục P1 của R4 (mục 3: `chắc`, `vừa`, và `yếu`)

### L00 (`lessons/bnx/L00_git_nhanh_gop_xung_dot.yaml`)
- `intuition.2` / `check.2`: `blob a9b66cb`, `f"blob {…}"` (A vừa) → **`ĐÃ`**: `intuition.2` (dòng 268, 274–275; PNG `00032.png`) chú thích `blob = nội dung một tệp` + `say` giải thích `"khối nội dung"`; `check.1` (dòng 429–433, 437–439) giảng `f"blob {len(noi_dung)}\0"` và ý nghĩa `blob` trước khối mã `check.2` (dòng 442).
- `pitfalls.1`: `git diff --cached --check` (A vừa) → **`ĐÃ`**: `pitfalls.1` (dòng 557–560, 564–565) giải nghĩa rõ `git diff --cached` và `--check`.
- `pitfalls.2`: `git log --format="%h %s"` (`%h`), `git switch -c thu 18bdd9f`, `.env` (A yếu) → **`ĐÃ`**: `pitfalls.2` (dòng 566–584; PNG `00084.png`) giải thích `.env` và tách thành bảng 4 hàng đứng TRƯỚC khối mã `pitfalls.3`.
- `quymo.2`: `git switch -q -c n$i main`, `git switch -q main; xd=0` (`;`) (A yếu) → **`ĐÃ`**: `quymo.1` (dòng 475–485) giải nghĩa `lệnh_a ; lệnh_b` (ví dụ `git switch -q main; xd=0`) và `git switch -q -c n$i main` trước khối mã `quymo.3`.

### L01 (`lessons/bnx/L01_openapi_hop_dong_api.yaml`)
- `formula.2`: `application/json` (yếu) → **`ĐÃ`**: `formula.2` (dòng 307–308, 324–325) giải thích `"tên kiểu nội dung: thân yêu cầu viết bằng JSON"`.
- `formula.5`: `"bản nháp IETF"` (yếu) → **`ĐÃ`**: `formula.5` (dòng 364–366, 374–375) giải nghĩa IETF và `"bản nháp"`, đồng thời giữ nhãn `"bản 08"`.
- `check.2`: `for f in (…):`, `if v is not None and not (…):`, `return loi + …` (một phần) (yếu) → **`ĐÃ`**: `check.1` (dòng 464–466) giảng `def kiem(req): … return loi + …`; `check.2` (dòng 478–494; PNG `00060.png`) thêm bảng 4 hàng đứng trước `check.3` giảng bộ giá trị `(tuple)`, `#`, `for f in ("fromAccount", "toAccount"):`, `if v is not None and not (…):`.
- `check.4`: `A, B = "…", "…"` (yếu) → **`ĐÃ`**: `check.4` (dòng 523–525, 531) thêm hàng giảng gán 2 biến trên một dòng trước `check.5`.
- `quymo.2`: `req["amount"] = 0` (yếu) → **`ĐÃ`**: `quymo.1` (dòng 593–596, 603) gộp vào hàng `del req["toAccount"]` giảng gán giá trị cho một trường của từ điển.

### L02 (`lessons/bnx/L02_grpc_protobuf.yaml`)
- `check.3`/`4`: `json.dumps({"id": 150}…)` + từ điển (M/B vừa) → **`ĐÃ`**: `check.3` (dòng 552–560) có hàng `{"id": 150}` (từ điển) và `json.dumps(d, separators=(",", ":"))` đứng trước `check.4`.
- `check.7`: `out = {}`, `out[num], i = …` (M/B vừa) → **`ĐÃ`**: `check.7` (dòng 609–619; PNG `00068.png`) tách bảng 3 hàng đứng trước hàm `decode` (`check.8`), giảng `i, out = 0, {}` và hai dạng `out[num], i = …`.
- `check.2`/`6`: `#` (yếu) → **`ĐÃ`**: `check.1` (dòng 523) giải thích `#` là chú thích.
- `sym.2`: `//` trong `.proto` (yếu) → **`ĐÃ`**: `sym.2` (dòng 263–268) thực tế không chứa `//`; `//` xuất hiện lần đầu ở `pitfalls.2` và đã được giải thích ngay tại `pitfalls.2` (dòng 783, 795–796).
- `check.6`: `n = shift = 0`, `return n, i` (yếu) → **`ĐÃ`**: `check.5` (dòng 581–583, 587) có hàng riêng trước `read_varint` (`check.6`).
- `quymo.3`: `"MB"` (yếu) → **`ĐÃ`**: `quymo.3` (dòng 730–731, 740–741) ghi rõ `(MB là mê-ga-byte, một triệu byte)`.

### L03 (`lessons/bnx/L03_jwt_chu_ky_han_dung.yaml`)
- `formula.5`/quiz/recap: `"mã làm mới"` (A CHẮC) → **`ĐÃ`**: `formula.5` (dòng 346–348, 363–364; PNG `00030.png`) định nghĩa đầy đủ tại chỗ trước `quymo.4`, `quiz`, `recap`.
- `example.9` / `example.14`: `json.loads(unb64u(t))` (M vừa), `from datetime import datetime, timezone`, `ma.split(".")[1]`, `datetime.fromtimestamp(...)`, `time.time()` (yếu) → **`ĐÃ`**: `example.9` (dòng 470–482; PNG `00049.png`) là bảng 4 hàng mới đứng trước khối mã `example.10` và `example.14`.
- `check.2`: `openssl base64 -A`, `date '+%F %T'` (yếu) → **`ĐÃ`**: `check.1` (dòng 563–572) giải nghĩa `-A` và chuỗi mẫu `'+%F %T'`.
- `sym.1`: `typ` (yếu) → **`ĐÃ`**: `sym.1` (dòng 168–169, 177) giải nghĩa `typ: loại mã, ở đây JWT`.

### L04 (`lessons/bnx/L04_oauth2_openid_connect.yaml`)
- `formula.4`: `HTTP/1.1` (yếu) → **`ĐÃ`**: `formula.4` (dòng 325–326, 336) giải thích `HTTP/1.1` là phiên bản giao thức web ngay dưới khối yêu cầu xin mã.

### L05 (`lessons/bnx/L05_mtls_chung_chi_hai_chieu.yaml`)
- `example.3`/`4`: `-CAkey`, `-not_before`, `-not_after`, `critical`, `openssl verify -CAfile` (yếu) → **`ĐÃ`**: `example.1` (dòng 334–336) giảng `critical`; `example.3` (dòng 364–377; PNG `00046.png`) thêm bảng 4 hàng đứng trước Bước B/C giảng `-CAkey`, `-not_before/-not_after`, `openssl verify -CAfile`.
- `example.9`/`10`: `c, _ = nghe.accept()`, `t.recv`, `t.sendall`, `th.join()`, `if ten:`, `with … as s, \` (yếu) → **`ĐÃ`**: `example.8` (dòng 448–456) giảng `th.join()` và `with … as s:` (dấu phẩy, `\`); `example.10` (dòng 474–486; PNG `00066.png`) giảng `c, _ = nghe.accept()`, `t.sendall(...)`, `loi.append`, `a; b` trước `phuc_vu`; `example.12` (dòng 505–516; PNG `00072.png`) giảng `if ten:`, `socket.create_connection(...)`, `t.recv(64).decode()`, f-string `\n` trước `thu`.
- `quymo.1`/`example.10`: f-string, `//` (B) (yếu) → **`ĐÃ`**: f-string giảng ở `example.12`; `//` giảng ở `quymo.1` (dòng 598–599) và nhắc lại ở `practice.3` (dòng 803).

### L06 (`lessons/bnx/L06_thu_tuc_luu_tru_plsql_tsql.yaml`)
- `formula.1`: `p_amt IS NULL` (A vừa) → **`ĐÃ`**: `sym.3` (dòng 203–215; PNG `00030.png`) thêm bảng 3 hàng giải thích `IF … THEN … END IF;`, `p_amt IS NULL` và `a OR b` trước `formula.1`.
- `practice.1`: `docker run -d --name … -p … -e …`, `docker exec -it … sqlplus` (A vừa) → **`ĐÃ`**: tách ra `practice.4` (dòng 785–797; PNG `00125.png`).
- `prereq.2` & `quymo.2`: `NUMBER`, `VARCHAR2(10)`, `INSERT INTO … VALUES` (yếu) → **`ĐÃ`**: `prereq.2` (dòng 134–143) thêm bảng 2 hàng đứng trước khối dựng bảng `prereq.3` và trước `quymo.2`, giải thích rõ `NUMBER`, `VARCHAR2(10)` và `INSERT INTO … VALUES (…)` nhiều dòng.

### L07 (`lessons/bnx/L07_oracle_phan_vung_json_hang_doi.yaml`)
- `formula.5`: `"biến gắn"` (A vừa) → **`ĐÃ`**: `formula.5` (dòng 391–392, 402–404; PNG `00049.png`) định nghĩa tại chỗ: `(giữ chỗ dạng :ngay, giá trị đưa vào lúc chạy)`.
- `formula.1`: `VALUES LESS THAN` (yếu) → **`ĐÃ`**: `sym.1` (dòng 169–171, 179–180; PNG `00016.png`) giải thích phân vùng `p_2025_01` chứa ngày nhỏ hơn `1/2/2025`.
- `formula.5`: `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(…))` (yếu) → **`ĐÃ`**: `sym.2` (dòng 184–187, 195–197; PNG `00020.png`) tách bảng riêng giải thích `TABLE(…)` và `NULL, NULL`.
- `formula.3`: `DATE '…' + TRUNC(…)` (yếu) → **`ĐÃ`**: `sym.1` (dòng 171–174, 180–181) giải thích cộng số ngày, `TRUNC` và `MOD`.
- `practice.1`: `->>` (yếu) → **`ĐÃ`**: `practice.1` (dòng 735–736, 751) giải thích `->>` là cách viết ngắn của `json_extract`.

### L08 (`lessons/bnx/L08_elasticsearch_manh_ban_sao.yaml`)
- `intuition.3`: `text.split()` (B yếu) → **`ĐÃ`**: `intuition.2` (dòng 283–285, 289–290) có hàng giải thích `text.split()` kèm ví dụ trước khối mã `intuition.3`.
- `formula.5`: `word in d.split()`, `buffer, searchable = [], []` (yếu) → **`ĐÃ`**: `formula.5` (dòng 483–492; PNG `00061.png`) tách bảng 3 hàng mới đứng trước bước mô phỏng làm tươi `formula.6`.
- `check.1`: `round(x, 3)` (yếu) → **`ĐÃ`**: `check.1` (dòng 602–603) bổ sung giải thích trong hộp ghi chú dưới mã.
- `hook.1`: `"NAPAS"` (A yếu) → **`ĐÃ`**: `hook.1` (dòng 113–114, 134–135) giải thích ngay trong câu đầu và lời đọc.

### L09 (`lessons/bnx/L09_couchbase_vbucket_cas.yaml`)
- `formula.6`: `return dict(self.doc), self.cas` (B yếu) → **`ĐÃ`**: `formula.5` (dòng 340–342, 348–349; PNG `00043.png`) giải nghĩa trả về 2 giá trị cùng lúc và cách nhận `d, c = s.get()` trước lớp `Store` (`formula.6`).
- `check.2`: `from itertools import permutations`, `;` (yếu) → **`ĐÃ`**: `check.1` (dòng 481–485, 490–492) giảng cả hai trước khối mã `check.2`.
- `sym.1`: `Couchstore`, `Magma`, `Enterprise` (A yếu) → **`ĐÃ`**: `sym.1` (dòng 148–150, 160–161; PNG `00016.png`, tách `sym.1`+`sym.2` nên `00016.png` và `00021.png` đều gọn) giải nghĩa `"Bộ lưu"`, `Couchstore`, `Magma`, `Enterprise`.

### L10 (`lessons/bnx/L10_kafka_nang_cao_rabbitmq.yaml`)
- `check.5`/`7`/`9`: `kafka-topics.sh`, `…-console-producer.sh`, `/opt/kafka/bin/` (yếu) → **`ĐÃ`**: `check.4` (dòng 694–698, 705–706; PNG `00081.png`) bổ sung giải thích đủ `/opt/kafka/bin/` và ba tập lệnh `.sh` trước các khối Docker `check.5`–`check.9`.
- `formula.6`: Avro `record`, `long` (yếu) → **`ĐÃ`**: `formula.6` (dòng 499–502, 514; PNG `00047.png`) có ghi chú + lời đọc giải thích `record`, `string`, `long`, `default`.
- `intuition.1`: `"bộ dọn"` (A yếu) → **`ĐÃ`**: `intuition.1` (dòng 315–316, 318; PNG `00022.png`) thêm dòng chú thích dưới SVG và câu lời đọc `"tiến trình nền của Kafka"`.

### L11 (`lessons/bnx/L11_thanh_toan_quoc_te_ngoai_te.yaml`)
- `sym.3`: thẻ XML `GrpHdr`, `MsgId`, `CdtTrfTxInf`, `CdtrAgt`, `FinInstnId`, `BICFI` (A vừa), `ChrgBr` (M vừa), `Ccy="USD"` (yếu) → **`ĐÃ`**: `sym.3` (dòng 195–217; PNG `00025.png`) là bước bảng 4 hàng + định nghĩa `XML` đứng TRƯỚC `sym.4` (khối XML `pacs.008`) và TRƯỚC `intuition.3`.
- `formula.7`: `from decimal import Decimal, ROUND_HALF_UP`, `for c in s:` (yếu) → **`ĐÃ`**: `for c in s:` giải thích tại `formula.3` (dòng 358–360, trước `formula.4`); `from decimal import Decimal, ROUND_HALF_UP` giải thích tại `formula.6` (dòng 397–399; PNG `00051.png`, trước `formula.7`).

### L12 (`lessons/bnx/L12_vi_dien_tu_thue_dien_tu.yaml`)
- `formula.6`: `elif` (yếu) → **`ĐÃ`**: `prereq.4` (dòng 181–184, 192; PNG `00018.png`) giảng `if a: … elif b: … else: …` với ví dụ trước `formula.6`.
- `quymo.5`: `"nối hai bảng trong CSDL"` (yếu) → **`ĐÃ`**: `quymo.5` (dòng 661–662, 673) đổi thành `"ghép hai bảng theo một cột chung (phép nối bảng)"`.
- `sym.2`: `"VBHN"` (yếu) → **`ĐÃ`**: `sym.2` (dòng 231–232, 243–244; PNG `00027.png`) giải thích `"VBHN = văn bản hợp nhất: một bản ghép văn bản ban đầu với các lần sửa"`.

---

## 5. Kiểm tra khung PNG (bao gồm 6 sơ đồ cơ chế R4 chưa xem)

Tất cả khung hình được mở và kiểm tra trực tiếp bằng mắt (`out/BNX/Lxx/frames/*.png`) đều sắc nét, không tràn khung, không đè chữ/nét:
- Các sơ đồ chưa xem ở R4: `L03 intuition.2` (`00017.png`), `L05 intuition.2` (`00021.png`), `L08 intuition.5/6` (`00038.png`, `00042.png`), `L10 intuition.2/3` (`00025.png`, `00028.png`), `L11 intuition.2/3` (`00033.png`, `00035.png`), `L12 intuition.2` (`00036.png`) — **tất cả đạt**.
- Các bảng/SVG mới & sửa lỗi hiển thị: `L00` (`00032`, `00057`, `00084`), `L01` (`00060`), `L02` (`00068`), `L03` (`00030`, `00049`), `L04` (`00021`), `L05` (`00046`, `00066`, `00072`), `L06` (`00030`, `00115`, `00125`), `L07` (`00016`, `00020`, `00049`), `L08` (`00061`), `L09` (`00016`, `00021`, `00043`), `L10` (`00022`, `00047`, `00081`), `L11` (`00025`, `00051`, `00086`), `L12` (`00018`, `00027`) — **tất cả đạt**.

## 6. Lỗi mới phát hiện
- Không phát hiện lỗi mới về nội dung, hiển thị, P1, SRT, hay pháp lý/nguồn trong L00–L12.
- Hai ghi chú nhỏ (không chặn, mức thông tin):
  1. `L06 practice.4`: bảng tóm tắt lệnh Docker giữ chỗ trống `-e …` và `bnx/…` (khớp mẫu `L07 practice.4` như R4 đề nghị; nếu người học muốn chép-dán chạy Oracle ngay từ L06 thì chưa có khối lệnh đầy đủ như `L07 practice.5`).
  2. `L00 example.7` (`00057.png`): khoảng trắng `*   0eac7e6` hiển thị thẳng hàng trong khối `.code`, giữ nguyên từ R4.
