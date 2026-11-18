# S01 BNX L00–L11: đã đọc 12/12 bài (2026-11-14, người đọc độc lập)

Phạm vi: `lessons/bnx/L00..L11`, `curriculum/bnx.yaml`, `labs/BNX/L00..L11`, `out/BNX/Lxx` (srt, frames). Người học giả định: đã học FND, JVA, JV2, PYT, BNK. Chỉ ghi báo cáo này, không sửa gì trong kho. Không chạy docker, Oracle, SQL Server, Kafka. Mã ngắn chạy bằng Python 3.13 (.venv), Git 2.53 (Git Bash), OpenSSL 3.5.5, JDK 21 (chỉ biên dịch), sqlite 3.49.

Ngưỡng chốt: **MUST 0: CHƯA ĐẠT (1 MUST nhẹ, L11). P1 = 2 ≥ 90%: CHƯA ĐẠT (9/12 = 75%). P8 = 2 = 100%: ĐẠT (12/12, có ghi chú).**

## 1. Hiện trạng video (quan trọng)
- Lúc bắt đầu đọc, chỉ L05 được dựng lại sau AF2. Trong lúc đọc, L00–L03 cũng được dựng lại (mp4 10:17–10:48 ngày 14/11). **L04 và L06–L11 vẫn là bản dựng 11/11 (trước AF2)**.
- Với 6 video mới (L00–L03, L05): so từng câu `say` trong YAML với `.srt`: **0 câu thiếu / 548 câu** (112+110+103+103+120). Số từ srt khớp số từ say (2301/2299/2297/2293/2346).
- Với L04, L06–L11: khung hình lấy từ bản cũ; các cảnh mới của AF2 (quymo, practice, câu trả lời mở rộng) có thể chưa có trong video. Nội dung được chấm theo YAML hiện tại (sha16 bên dưới), không phải theo video cũ. Cần xem lại khung hình sau khi dựng lại.
- Độ dài lời đọc (từ): L00 2301, L01 2299, L02 2297, L03 2293, L04 2306, L05 2346, L06 **3054**, L07 **3049**, L08 2306, L09 2314, L10 2309, L11 **2478**. Ước tính thời lượng theo L05 (2346 từ = 14 phút 49): L06 ≈ 19,3 phút, L07 ≈ 19,3 phút, L11 ≈ 15,7 phút, còn lại 14–15 phút.

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L11 | **MUST-1** (nhẹ, số đọc sai) | quymo, step 0, `say` | "Với mười nghìn lần, số thực lệch ở chữ số thập phân thứ mười hai." | Màn hình: `1000.0000000001588`. Chạy lại: lệch `1.588205122970976e-10` nên chữ số khác 0 đầu tiên ở vị trí thập phân **thứ mười** (không phải mười hai). Ý một triệu lần "thứ sáu" đúng (`1.33e-6`) | Đổi "mười hai" thành "mười" | CONFIRMED |
| L11 | SHOULD-10 | quiz step 3 + bảng; `say` | "Chọn người gửi chịu hết thì người nhận nhận đủ và hoá đơn tất toán một lần" | Khẳng định tuyệt đối. OUR không bảo đảm tuyệt đối (ngân hàng trung gian hoặc ngân hàng nhận vẫn có thể trừ phí); curriculum fix #3 ("người nhận không chắc nhận đủ") chỉ được nhắc lướt ở lỗi 2 | Thêm điều kiện "thường", dặn đối chiếu số báo có | PLAUSIBLE (kiến thức nghề, không có nguồn trong phiên) |
| L11 | SHOULD-11 | quiz/lab | — | Mục tiêu 2 (bút toán nostro) và 4 (MT sang ISO 20022) không có câu quiz và không có trong lab. Bảng sym "giải mã sáu từ" nhưng lời đọc chỉ đọc 3 dòng (nostro/vostro giảng ở cảnh intuition) | Thêm 1 câu quiz cho mỗi mục tiêu | CONFIRMED (đọc YAML) |
| L06 | SHOULD-1 | check (T-SQL) | `FROM dbo.tk WITH (UPDLOCK, ROWLOCK)` | Phần "Kết quả chạy thật" trên SQL Server dùng `dbo.tk` nhưng màn hình **không có** `CREATE TABLE dbo.tk` / `INSERT` (chỉ có bảng Oracle `bnx_l06_tk`) nên người học không tự lặp lại được. Phiên bản "Oracle Free 23" / "SQL Server 2022" cũng không nêu trên màn hình hay lời đọc (grep YAML: không có) | Hiện bảng T-SQL và phiên bản | CONFIRMED (grep) |
| L06 | SHOULD-2 | quymo step 0–2 | "mỗi lần chuyển gửi năm câu, gồm mở giao dịch, đọc số dư, hai câu cập nhật và chốt" | Hệ số ×5 là mô hình giản lược: JDBC không gửi `BEGIN` riêng, trong khi chính thủ tục của bài có 2 `SELECT…FOR UPDATE` + 1 `SELECT` số dư, nên bản tương đương ở ứng dụng là 6 chứ không phải 5. Màn hình có ghi "sqlite làm đại diện" nhưng không nói "5" là mô hình. Chạy lại: 50/5000/500000 khớp mã | Ghi "mô hình giản lược, số câu thật phụ thuộc cách viết" | PLAUSIBLE |
| L07 | SHOULD-3 | toàn bài | — | Kỹ năng trung tâm (đọc kế hoạch cắt tỉa phân vùng, hàng đợi AQ) chỉ xem, không có lab và không nói cách dựng Oracle Free (image/cài đặt). Lab chỉ là JSON trên sqlite (mục tiêu 6) | Thêm hướng dẫn dựng Oracle Free hoặc nói rõ "chỉ xem" | CONFIRMED (đọc de.md + YAML) |
| L07 | SHOULD-4 | formula step 11–12, quiz | — | Mục tiêu 4 "nêu khi nào cần bộ nhớ cột và phân mảnh": chỉ 2 bước, không có câu quiz; `INMEMORY_SIZE=0` nên không đo được gì; phân mảnh chỉ `mod 3` "minh hoạ" (Oracle sharding dùng băm nhất quán, bài đã ghi "quy tắc minh hoạ") | Thêm câu quiz hoặc chuyển sang bài so sánh CSDL | CONFIRMED |
| L08 | SHOULD-5 | quiz step 3 (Q3) và step 2 (Q2), `say` | "Số dư lấy từ cơ sở dữ liệu giao dịch vì đúng ngay sau khi chốt, đổi lại tìm theo chữ thì chậm. Số dư lấy từ cơ sở dữ liệu giao dịch, vì nó đúng ngay sau khi chốt và có giao dịch nhiều dòng…" | Lời đọc lặp một ý hai lần liền (script dò câu gần trùng: 0,81). Q2 cũng lặp "khoảng mười bảy phần trăm, nên phải tạo chỉ mục mới" | Xoá câu lặp | CONFIRMED |
| L08 | SHOULD-6 | quymo; formula step 0 | "Quét thô phải đọc mọi mô tả; chỉ mục ngược chỉ đọc danh sách của chữ cần tìm." | Số "đo thật" (quét 1200 so với chỉ mục 2) là độ dài list trong mã mô phỏng, không đo thời gian/I-O, bỏ qua chi phí dựng chỉ mục O(n). Công thức "mảnh = băm mod số mảnh chính cho chỉ mục từ bản 9.4" không kiểm được (hàm băm thật là murmur3; bài đã ghi "băm minh hoạ"). Màn hình có ghi "Mô phỏng bằng Python (không phải Elasticsearch thật)" | Gọi là "đếm theo mô hình" | PLAUSIBLE |
| L09 | SHOULD-7 | quymo, quiz Q3 | "chọn khoá bi quan ngắn có thời hạn, vì dấu phiên bản sẽ bị từ chối liên tục" | `n(n+1)/2` là trường hợp xấu nhất (n tiến trình đồng bộ, thử lại ngay, không backoff) nhưng ghi "đo thật". Bỏ qua thao tác tăng nguyên tử có sẵn cho bộ đếm (counter/sub-document increment) và không có SDK thật hay tên lỗi CAS mismatch. Đã ghi "kho mô phỏng, không phải Couchbase thật" | Ghi "trường hợp xấu nhất", nhắc counter nguyên tử | PLAUSIBLE |
| L10 | SHOULD-8 | check step 2 | "Đường khác 2: Kafka 3.9.0 thật (Docker)" | Chỉ có KẾT QUẢ (`Offset:5 A 120`…), không có lệnh tạo chủ đề/cấu hình (`segment.ms`, `min.cleanable.dirty.ratio`, `print.offset`), nên người học không lặp lại được. **Chưa kiểm chạy** (không có docker) | Hiện lệnh | CONFIRMED (đọc YAML), kết quả PLAUSIBLE |
| L10 | SHOULD-9 | formula step 1/5 | "9 -> [(5, 'A', 120), (7, 'B', 260)]" | `compact()` bỏ bia mộ ngay (mô hình trạng thái sau `delete.retention.ms`) trong khi example ② nói "ngay sau lần nén kế tiếp còn ba": hai chữ "sau nén" cho hai số, step 3 mới giải thích. Hàm `backward_ok` chỉ kiểm trường thêm không có mặc định, nhãn "Kết quả chạy thật", không ghi "không phải Schema Registry" (BACKWARD thật còn kiểm đổi kiểu/xoá trường) | Ghi rõ "mô hình" | CONFIRMED |
| L00 | SHOULD-12 | quymo step 2 | "đo cùng chương trình khi mỗi người sửa tệp riêng: 0 xung đột" | Khẳng định đúng (tôi chạy: 2/10/50 nhánh sửa tệp riêng ra 0/0/0) nhưng màn hình không có mã hay kết quả đo tương ứng | Thêm 1 dòng kết quả | CONFIRMED (đúng, thiếu bằng chứng trên màn hình) |
| L01 | nhỏ | pitfalls step 0 | "đến năm hai nghìn không trăm mười lăm mới được trao cho một tổ chức khác và đổi tên" | Thực tế trao cho OpenAPI Initiative cuối 2015, đổi tên OpenAPI Specification 2016 | Sửa "2015 trao, 2016 đổi tên" | PLAUSIBLE |
| L05 | nhỏ | example step 0–2 | `-not_before …` / `req -x509 -CA` | Lệnh cần OpenSSL ≥ 3.4 (`-not_before`) và ≥ 3.2 (`req -CA`); màn hình ghi "openssl 3.5" nhưng không nói bản tối thiểu (Ubuntu 22.04 có 3.0 sẽ lỗi) | Ghi bản tối thiểu | PLAUSIBLE |

Các dữ kiện không kiểm được trực tiếp (PLAUSIBLE, khớp hiểu biết): Thông tư 64/2024/TT-NHNN (L04); 409/422 theo bản nháp IETF Idempotency-Key "bản 08" (L01); Couchbase 8.0 "Magma 128 mặc định" (L09); Elasticsearch "9.4", Kafka "4.4", RabbitMQ "4.4", Confluent "8.4" (nguồn); Oracle Free 23 (partition, AQ, IS JSON lax mặc định, giới hạn 1 048 575 phân vùng, `PARTITION RANGE SINGLE/ALL/ITERATOR`); SQL Server 2022 `LEAST/GREATEST`, `XACT_ABORT` mặc định OFF; SWIFT 22/11/2025 (MT103→pacs.008, MT202→pacs.009, 71A→ChrgBr DEBT/SHAR/CRED), ISO 9362/13616/4217. Dữ kiện RFC kiểm được bằng chạy: RFC 7515 A.1 (chữ ký `dBjftJeZ…`), RFC 7636 B (`E9Melhoa…`), RFC 6749 4.4.2 (`czZCaGRSa3F0…`), protobuf `08 96 01`.

## 3. Bảng độ sâu
Mục tiêu giáo án ↔ video (E51): `objectives` của YAML trùng nguyên văn `curriculum/bnx.yaml` cho cả 12 bài; mỗi mục tiêu có cảnh `covers`; mục tiêu "đo ở 3 mức quy mô" đều có cảnh `quymo`. Lệch: L06 `example` giáo án nói "chạy thật trên Oracle Free 23 và SQL Server 2022" nhưng bài không nêu phiên bản; L11 `fix` #3 chỉ được nhắc lướt; L07 mục tiêu 4 và L11 mục tiêu 2, 4 không có quiz.

| Bài | sha16 | Phút (ước) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 612d478a72faadde | 15,3 (đo) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | bash: `for`, `\|\|`, `$(( ))`, `export`, `mktemp`, `seq`; git `switch`, `cat-file`, `rev-parse` | thuật ngữ shell không giảng; 0 xung đột khi tách tệp không có mã |
| L01 | 5f0873ac2c2098b8 | 15,4 (đo) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Python `get`, `fullmatch` | `$` của Python lọt `\n` đã giảng; năm 2015/2016 |
| L02 | 0dedc3748fa68e17 | 15,3 (đo) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | proto3 mặc định 0 không ghi, số âm 10 byte/zigzag không nói; hạn chót chỉ mô phỏng (có ghi) |
| L03 | 4a12d01cc63b2ac9 | 16,5 (đo) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `date -u -d` chỉ GNU | 64×43=2752 là cận trên |
| L04 | cdf1ba4b0a89bc0a | 11,5 (đo, video cũ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | không có `state`/`redirect_uri`/refresh token; quiz không hỏi "chọn luồng" (mục tiêu 2); toàn mô phỏng |
| L05 | da0997b48f033630 | 14,8 (đo) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | OpenSSL ≥ 3.4 | thu hồi chứng chỉ (CRL/OCSP) không nói |
| L06 | 0e04407774235ae8 | ~19 (ước, quá dài) | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `PRIMARY KEY`, `NUMBER`, `VARCHAR2`, `DECLARE`, `DBMS_OUTPUT`, `isolation_level` | SHOULD-1, SHOULD-2; Java JDBC không có kết quả chạy, không lab, không có `import` |
| L07 | e49f7a96bba9af17 | ~19 (ước, quá dài) | 1 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 2 | 11 | **GẦN** | `CONNECT BY ROWNUM`, `RAW(16)`, `CREATE TYPE AS OBJECT`, `user_tab_partitions`, `v$parameter` | SHOULD-3, SHOULD-4; 5 chủ đề trong 1 bài |
| L08 | a8b00d3920d74e71 | 12,3 (đo, video cũ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | SHOULD-5, SHOULD-6; không có ES thật |
| L09 | e4d87ca89061c478 | 13,4 (đo, video cũ) | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 13 | ĐỦ | — | SHOULD-7; không có API Couchbase thật |
| L10 | e35e2476077d63f3 | 13,0 (đo, video cũ) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Kafka partition (BNK:L07) | SHOULD-8, SHOULD-9; RabbitMQ chỉ giảng sàn topic (không queue/binding/ack cơ bản) |
| L11 | f60f7b48d4eff156 | ~15,7 (ước) | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | — | MUST-1, SHOULD-10, SHOULD-11 |

P1 = 2: 9/12 (75%). Bài P1=1: L00 (thuật ngữ shell/git không giảng), L06 và L07 (cú pháp Oracle/T-SQL dùng mà không giảng).

## 4. Lab (tự làm như người học, không nhìn `loi_giai.*`, chấm bằng `labs/cham.sh`)
| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có (ĐÚNG lần đầu) | ~2 phút | không; cần biết `git switch -c` và `git commit -am` (bài đã dùng) | có (3 dòng) |
| L01 | có | ~2 phút | không | có (5 dòng) |
| L02 | có | ~2 phút | không; đề đưa sẵn gợi ý khoá 6 = 30 | có (2 dòng) |
| L03 | có | ~4 phút | không; đề gần như đọc chép công thức; phải nhớ thêm `=` trước khi giải mã | có (5 dòng) |
| L04 | có | ~2 phút | không | có (3 dòng) |
| L05 | có | ~4 phút | không; cần `date.fromisoformat`/`timedelta` (đã gợi ý trên màn hình) | có (4 dòng) |
| L06 | có (sqlite, ĐÚNG) | ~3 phút | không; cần `isolation_level=None` + `BEGIN` thủ công (cho sẵn) | có (5 dòng) |
| L07 | có (sqlite, ĐÚNG) | ~3 phút | không; cần sqlite ≥ 3.38 (de.md đã ghi); `->>` cần Python sqlite mới | có (4 dòng) |
| L08 | có | ~2 phút | không | có (6 dòng) |
| L09 | có | ~3 phút | không | có (5 dòng) |
| L10 | có | ~3 phút | không; cần tự viết lại `match` đệ quy (bài đã cho mã) | có (5 dòng) |
| L11 | có | ~2 phút | không | có (5 dòng) |

12/12 lab tự viết đạt ĐÚNG ngay lần chạy đầu. Kiểm "mong_doi khớp màn hình" bằng script (mọi dòng của `mong_doi.txt` có mặt trong bước "Kết quả mong đợi" của YAML): 12/12. Ghi chú P8: lab L06, L07 là sqlite thay Oracle, L08–L10 là mô phỏng Python; phần Oracle/SQL Server/Elasticsearch/Couchbase/Kafka/RabbitMQ thật chỉ để xem (không có hướng dẫn tự dựng), nên P8 = 2 ở mức "có việc cụ thể + kết quả mong đợi", nhưng kỹ năng nền tảng thật (đọc kế hoạch phân vùng, bắt tay mTLS trừ L05) chỉ L05 tự chạy lại được hoàn toàn bằng công cụ có sẵn.

## 5. Người học kẹt ở đâu (chỗ đầu tiên không theo được)
- L00: không kẹt về ý; chỉ vướng cú pháp bash ở quymo step 0 (`for i in \`seq 1 $N\`; do … git merge -q n$i >/dev/null || { xd=$((xd+1)); … }`).
- L01: không kẹt.
- L02: không kẹt (phép dịch bit đã giảng ở prereq).
- L03: không kẹt; step cuối "check" (openssl `-macopt hexkey:\`) dài, cần chép đúng.
- L04: không kẹt.
- L05: dễ kẹt ở example step 0–2 nếu OpenSSL dưới 3.4/3.2 (`-not_before`, `req -CA`): lỗi lệnh, bài không nói bản tối thiểu.
- L06: kẹt ở formula step 5 / check: "`DECLARE`", "`/`", "`GO`", `dbo.tk` chưa tạo (SHOULD-1); chưa tự chạy lại được nửa T-SQL.
- L07: kẹt ở formula step 2: "`SELECT ROWNUM, DATE '2025-01-01' + TRUNC((ROWNUM - 1) / 10), … FROM dual CONNECT BY ROWNUM <= 3650`" (có lời đọc nhưng không giảng `CONNECT BY`); và không có cách dựng Oracle để thử.
- L08: không kẹt.
- L09: không kẹt.
- L10: kẹt ở scene check step 2 ("Kafka 3.9.0 thật") vì không thấy lệnh để lặp lại; RabbitMQ (sàn/binding/queue) mới đủ ý tối thiểu.
- L11: không kẹt; step bút toán (formula step 5) dày: "tài khoản mua bán ngoại tệ" xuất hiện lần đầu, được giải thích ngay trong lời đọc.

## 6. Số đã tính lại / mã đã chạy
Khoảng 160 giá trị/đầu ra được tính lại hoặc so từng dòng; **khớp tất cả trừ 1** (MUST-1, lời đọc L11). Chi tiết:
- L00: chạy lại đủ chuỗi git 2.53 với ngày cố định: hash `18bdd9f`, `577eea4`, `a8af580`, `0eac7e6`, `a9b66cb`, `57d5547`, `96f907b`, cây `4ed712d` đều khớp; `git diff --cached --check` báo "leftover conflict marker" đúng; N = 2/10/50 nhánh → 1/9/49 xung đột; tách tệp → 0/0/0.
- L01: hàm kiểm + lô 1 000/100 000 → 30/3 000 (và 2 000+1 250−250); Python `$` lọt `\n` (xác nhận).
- L02: varint/field/decode, 08 96 01, 21 857/62 786, 2 381 377/6 677 790, hạn chót 1 200/400/hết giờ, V1/V2, `18 ac 02`; lab `08 14 30 f0 a2 04 3a 05 41 54 4d 30 31` — khớp.
- L03: RFC 7515 A.1 bằng Python và bằng `openssl dgst` (cả hai ra `dBjftJeZ…`), 40/94/43 ký tự, 5 ca thử, 240/3 540 giây, 12 000/12 000 000 mã mới, 2264-09-24, lab.
- L04: 5 ca 403/401/200/401/401, 360 giây nhận (0–359), 140/13 360/1 333 390, PKCE `E9Melhoa…`, Basic `s6BhdRkqt3:gX1fBat3bV`, ×270.
- L05: 7 chứng chỉ bằng OpenSSL 3.5.5, `openssl verify` (lỗi 20, 10, OK), máy chủ/khách Python 3.13.5 năm lần: `TLSV13_ALERT_CERTIFICATE_REQUIRED` / `UNKNOWN_CA` / `CERTIFICATE_EXPIRED` / "từ chối" / "chào thanh_toan" khớp từng dòng; thiếu keyUsage → "CA cert does not include key usage extension" (xác nhận lời đọc); 10/180, 1 000/18 000, 100 000/1 800 000; 30/4, 30/5.
- L06: sqlite quymo 50/5 000/500 000; lab; cơ chế sqlite `IntegrityError` + commit → 1 800 000; đếm tay 27 dòng thủ tục PL/SQL: `ORA-06512 line 18` và `line 27` khớp đúng; JDK 21 biên dịch được đoạn JDBC (thêm `import java.sql.*`). **Oracle/SQL Server: chưa kiểm chạy**, kiểm bằng lý luận.
- L07: 365×10=3 650, 1+11=12, 310/3 650=8,5%, 3 650/310=11,8, 61 ngày → 610, 1 048 575=1024²−1, 31/365×36 500 000=3 100 000; lab sqlite. **Oracle chưa kiểm chạy**.
- L08: chỉ mục ngược, 17 mod 3/4, 3/12, mô phỏng làm tươi, CRC32 315/1 200=0,263, 885/89 991/899 480, 2/120/1 200, Q2 5/30; lab. Không có Elasticsearch thật (màn hình ghi rõ "mô phỏng").
- L09: vBucket 351/95 (CRC32 2 170 508 415), Store 150/từ chối/180 CAS 9, hoán vị 6 → [180] và [130,150,180], 3/210/20 100, Q1 922, lab 892/124. Không có Couchbase thật (ghi rõ).
- L10: compact 8→3, 9→2, đi ngược "3 2", `backward_ok` v2/v3, `match` 6 ca, 100/100/100, Q1 3→2; lab. **Kafka Docker chưa kiểm chạy**.
- L11: IBAN `GB82WEST…` dư 1 (28 chữ số), r=16→82, Decimal 25 400 000/985,00, float 0,9999999999999999/1000,0000000001588/100000,00000133288 (khớp màn hình; lời đọc sai vị trí, MUST-1), `2.67`/`2.68`, 49, lab dư 1/50, 25 908 000, 508 000, 63 500 000, 2%/0,02%/0,0002%.

## 7. Khung hình đã xem
Video mới (L00–L03, L05): 5–6 khung mỗi bài đọc ở độ phân giải đầy đủ (L00) hoặc tấm ghép 6 khung (L01–L03, L05). Video cũ (L04, L06–L11): tấm ghép 6 khung từ bản 11/11. Mỗi bài có đủ: mở đầu, ví dụ/công thức, quymo hoặc mã đo, quiz, tổng kết (+ practice/lỗi hay gặp). Khung: L00 `00001, 00044, 00064, 00083, 00104`; L01 `1, 30, 50, 70, 88, 105`; L02 `1, 30, 45, 63, 84, 98`; L03 `1, 28, 45, 64, 83, 100`; L04 `1, 35, 53, 69, 84, 96`; L05 `2, 32, 50, 76, 95, 116`; L06 `1, 45, 74, 100, 127, 147`; L07 `1, 44, 90, 114, 126, 146`; L08 `1, 50, 70, 90, 107, 124`; L09 `1, 46, 81, 102, 115, 137`; L10 `1, 46, 77, 99, 111, 132`; L11 `1, 55, 78, 99, 111, 130`.
Lỗi hiển thị: **không thấy chữ tràn, đè hay cắt** trong các khung đã xem; phụ đề khớp hình. Ghi chú: bản cũ L06–L11 chưa phản ánh toàn bộ nội dung AF2 (xem mục 1); mã dài ở tấm ghép thu nhỏ khó đọc nhưng ở khung đầy đủ L00 đọc rõ.

## 8. Nhận xét chung
- Chất lượng toán/mã tốt: mọi con số quan trọng chạy lại khớp; chỉ 1 lỗi số trong lời đọc (L11) và vài chỗ khẳng định chưa đủ điều kiện (L09 Q3, L11 OUR).
- Điểm yếu lớn nhất là **tính thực nghiệm của phần "sản phẩm thật"**: Oracle, SQL Server, Kafka, Elasticsearch, Couchbase, RabbitMQ đều không có cách người học tự dựng; lab thay bằng sqlite/Python mô phỏng. Bài đều ghi rõ "mô phỏng" trên màn hình và lời đọc (L02, L04, L06 quymo, L08, L09, L10); riêng L10 `backward_ok` và L06 "×5" cần nhãn rõ hơn.
- Ba bài nên xử lý trước khi chốt: **L07** (GẦN: 5 chủ đề, mục tiêu 4 mỏng, không lab phân vùng), **L06** (dài 3 054 từ, T-SQL không tự lặp lại được), **L11** (MUST-1 và SHOULD-10/11).
- Lời đọc dài: L06 và L07 (~3 050 từ, ~19 phút) làm người học rã; gợi ý cắt/tách: L06 → L06a (Oracle: hook→JDBC, ~1 500 từ) + L06b (SQL Server `XACT_ABORT`, quymo, lỗi; bỏ hoặc chuyển SQL injection step 7–8 sang bài khác); L07 → L07a (phân vùng: hook, bước 1–3, example, quymo, lỗi 1, quiz Q1) + L07b (JSON + hàng đợi: bước 4–8, lỗi 2, quiz Q3, lab), đưa bộ nhớ cột và phân mảnh thành một cảnh tóm tắt hoặc sang L28; L11 (2 478 từ) có thể bỏ cảnh float-so-với-Decimal (đã học ở PYT/BNK) để về ~2 100 từ.
- Mục tiêu giáo án ↔ video khớp nguyên văn cả 12 bài; chỗ lệch nằm ở quiz không phủ mục tiêu (L04 mục tiêu 2, L07 mục tiêu 4, L11 mục tiêu 2 và 4).
- Dữ kiện chuẩn kiểm được bằng chạy (RFC 7515/7636/6749, protobuf, ISO 13616 mod 97, git hash, mTLS thật) đều đúng; dữ kiện sản phẩm (Oracle/SQL Server/ES/Couchbase/Kafka) PLAUSIBLE vì chưa kiểm chạy.
- Việc cần làm lại sau khi dựng lại L04, L06–L11: xem lại ≥ 5 khung/bài và so srt với say như đã làm cho L00–L03, L05.
- Cổng P1 = 2 ≥ 90% chưa đạt (75%) chủ yếu vì L00/L06/L07 dùng cú pháp mà không giảng tại chỗ; thêm 1–2 câu giảng (bash `for`/`||`; `CONNECT BY`, `CREATE TABLE … PRIMARY KEY`) sẽ đưa lên 12/12.
