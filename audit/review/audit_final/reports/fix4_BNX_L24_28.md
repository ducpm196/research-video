# fix4 BNX L24–L28 (nhóm A của fix4 L24–L38, 2026-11-15)

## Tiến độ
- XONG 5/5: L24, L25, L26, L27, L28. Sửa NGUỒN `audit/bnx/src/l24..l28.py`, `gen.py Lnn` từng bài (không sửa tay YAML). Không đụng tệp dùng chung (symbols.BNX.yaml, gen.py, lib*.py, sổ BNX.yaml, curriculum/bnx.yaml).
- **Cả 5 bài đổi nội dung nên đều CẦN DỰNG LẠI** (tts, asr, render, build): L24, L25, L26, L27, L28. Khung PNG `out/BNX/Lxx/frames` đã render lại (chỉ để xem; mp4/srt/chapters.txt cũ).

## Số liệu cổng (đo thật 2026-11-15)
| Bài | lint | từ lời đọc | render | verify_bnx | screen_fast (khối của bài) |
|---|---|---|---|---|---|
| L24 | 0 FAIL 0 WARN | 2292 | 0 vấn đề | 22/22 PASS | PASS |
| L25 | 0/0 | 2294 | 0 | 16/16 PASS (có Oracle và SQL Server thật qua dbrun) | PASS |
| L26 | 0/0 | 2288 | 0 | 41/41 PASS (Maven 3.9.11 thật; lần chạy trước khi sửa chữ lời đọc cuối, mã không đổi) | PASS |
| L27 | 0/0 | 2289 | 0 | 21/21 PASS | PASS |
| L28 | 0/0 | 2275 | 0 | 21/21 PASS (PostgreSQL 17, MongoDB 8, MySQL 8.4, Oracle, SQL Server thật) | PASS |
- `screen_fast.py L24..L28` chạy chung một lần cuối: 93 khối, PASS 149, FAIL 0, STALE 0, MISSING 0, ORPHAN 0.
- `tests/test_e52.py`: 0 FAIL. `check_course_refs.py BNX`: 0 vấn đề. `check_next_refs.py`: 550 lời hẹn, 0 lệch. `arith_scan.py BNX`: 58 phép tính, 0 FAIL. `lv.py curriculum curriculum/bnx.yaml`: 39 bài, 0 lỗi. (`lab_gate.py` để điều phối chạy cuối khoá.)
- Mỗi `say` 4–38 từ, không chữ Latin/Anh (lint WARN `Server` đã tránh: lời đọc nói "hệ thứ hai"), số không dấu cách, thập phân "phẩy".
- Đã xem khung PNG: L24 (00015, 00019, 00023, 00053, 00069, 00073), L25 (00018, 00052), L26 (00020, 00023, 00038, 00046, 00049, 00051, 00052), L27 (00020), L28 (00019, 00053, 00054).

## MUST
Nhóm A không có MUST (3 MUST ở L30/L37 thuộc nhóm B và C).

## SHOULD CONFIRMED (đã sửa hết)
- **L24** pitfalls "mượn kết nối mỗi câu": sửa thành "một yêu cầu GIỮ một kết nối của bể suốt thời gian chạy hết các câu (trong một giao dịch vẫn chỉ một kết nối, nhưng giữ lâu)". Kiểm: reader đã dựng lại DemN1.
- **L24** phân trang + `join fetch` danh sách: thêm chương trình thật `DemTrang` (vào nguồn `ChayHib`): ghi "cắt trang ngay trong câu nối kèm thì Hibernate đọc hết rồi cắt trong bộ nhớ: ngữ cảnh giữ 1500 đối tượng; hai bước (lấy 20 mã rồi `join fetch` theo mã) chỉ giữ 20 + 20 × 2 = 60". Có step hiện đầu ra thật ở quymo; sửa quymo bảng 2, quiz câu 3 và lời. Kiểm trong `ver/l24.py` (thêm 1 dòng). Không nêu mã `HHH90003004` trên màn hình vì verify chỉ đọc stdout, không đọc cảnh báo ở stderr.
- **L25** formula#6 REPEATABLE_READ: "trên H2 A vẫn thấy giá trị cũ; Oracle không có mức này (ORA-02179); SQL Server giữ khoá nên lệnh sửa của B phải chờ". Kiểm thật qua `dbrun` trong `ver/l25.py` (thêm 2 dòng: Oracle ORA-02179; SQL Server, A đọc lại vẫn 1000, UPDATE của B Msg 1222; DB `bnx_l25` tự dọn).
- **L25** example#3: thêm step hiện `chuyenKiem`, `chuyenKiemHoanTac` (ChuyenTien.java dòng 16–25). Quymo và pitfalls Lỗi 3: thêm điều kiện "nếu cả 300 luồng cùng giữ giao dịch ngoài lúc đó". `de.md` và màn hình Tự làm ghi "MÔ PHỎNG, không chạy Spring".
- **L26** de.md và màn hình Tự làm ghi "MÔ PHỎNG, không chạy Maven/Gradle/Jenkins thật". Lỗi hiển thị: nhãn "cần" không còn bị mũi tên gạch (hình 00018); `ChayQuyMo` hiện lại dòng `for … do` (lines 3–7, đủ `done`). Mục tiêu 6 và 7 sửa cho khớp bài (xem mục "Giáo án" bên dưới).
- **L27** pitfalls Lỗi 3 thêm điều kiện "nếu máy chỉ còn dưới 24 GB trống (số minh hoạ)" ở bảng và lời. Mục tiêu 2–3 đổi thành "đọc kết quả chạy thật / đã đo" (người học không chạy SOAP, lab không có phần SOAP).
- **L28** màn hình có T-SQL: thêm step hiện `xin = """SET LOCK_TIMEOUT 0; SELECT … WITH (UPDLOCK, ROWLOCK) …"""` và hộp "SQL Server không có `FOR UPDATE NOWAIT`: viết thế báo Msg 1003". Kiểm thật bằng `dbrun.mss` trong `ver/l28.py` ("FOR UPDATE clause allowed only for DECLARE CURSOR"). Nguồn `SoSanhKhoa` xuống dòng SQL để hiện vừa khung. Hook: "MongoDB sửa một bản ghi là nguyên tử, nên bài dùng cập nhật có điều kiện thay cho khoá (cũng có giao dịch nhiều bản ghi)".

## P1 (thuật ngữ và cú pháp giảng tại chỗ; mục tiêu mọi bài 0 mục chưa giảng)
Cách làm: thêm bảng "viết trong mã / đọc là / ví dụ nhỏ" (kèm lời đọc) ngay sau bảng giải mã tên (cảnh `sym`), trước khối mã đầu tiên dùng cú pháp; không thêm mục `term:`/`assumes`/`introduces` mới trừ chuyển `bnx_explain` ở L28 (xem dưới). Dấu `$` trong bảng viết `&#36;` để KaTeX không bắt nhầm.
- L24: `List<TaiKhoan>`, `try (Session s = …) {}`, `for (Khach k : ds)`, `:n` + `.setParameter`, `interface KhachRepo extends CrudRepository<Khach, Long>`.
- L25: `j.update(TRU)` (JdbcTemplate, dấu `?`), `@Configuration/@Bean`, `@Around("execution(* ChuyenTien.rieng(..))")`, lambda `() ->`, `s -> {}`, `::`, `setAutoCommit(false)`, `setTransactionIsolation`.
- L26: `$M -B -q … -D… && cat`, `| grep -- '--- ' | cut -c8-`, `a=$(dung $1)`, `cut -d' ' -f1`, `[ x = y ] && A || B`, `for … do … done`, `implementation 'g:a:v'`, phiên bản dạng khoảng / `latest`.
- L27: `xsd:string`, `tns:LaySoDuIn`, `style="rpc"`, `javac -encoding UTF-8`, f-string `:08d`/`%`, `bytearray`, `+=`, `del buf[:n]`, `with open`, `split`, "SSH".
- L28: `docker run --rm -d --name`, `exec -i/-d`, `cp`, `P="…"; $P -q -c`, `loc() { grep -E … }` + `| loc`, `generate_series`, `analyze`, `explain (analyze)`, `\! touch`, `pg_sleep`, `DECLARE … BEGIN … END; /`, `DBMS_SESSION.SLEEP`, `dbrun.ora`, `threading.Thread`, `SET LOCK_TIMEOUT 0`, `WITH (UPDLOCK, ROWLOCK)`.
- Điểm P1 dự kiến: tự đánh giá 5/5 bài đạt 2; cần người đọc chấm lại. Rủi ro: cú pháp rất nền (ví dụ `for`, `def` trong mã lab, `[ … ]` của shell ở một số dòng L26/L28) và vài tên API chưa có dòng riêng.

## Bù từ để giữ ≤ 2300 từ
Cắt chỗ khác (rút câu thuật lại kết quả, câu lặp bảng, "của người đã đi làm", đoạn dư trong hook/quiz/recap) để bù ~100–230 từ thêm cho mỗi bài.

## Việc điều phối cần làm (sổ/tệp dùng chung)
- Sổ chứng cứ: các mục `audit/bnx/screen/l24..l28.yaml` được sinh lại bằng `screen_keep.py` (khối mới đều khớp chương trình, "chưa khớp 0"); cần gộp vào `BNX.yaml` bằng cách điều phối vẫn dùng. Khối mới: L24 `DemTrang` (đầu ra trong `ChayHib`), L25 không khối mới (chỉ lines), L26/L27/L28 khối mới đều là đoạn của chương trình có sẵn.
- `curriculum/bnx.yaml` (không sửa; `lv.py curriculum` vẫn 0 lỗi): đổi mục tiêu bài cho khớp:
  - L26 dòng 223, mục 6 thành "Đọc số gói thư viện đo thật ở ba dự án thử và tính số máy dựng tối thiểu khi lượt dựng gấp 100 và 10 000 lần", mục 7 thành "Viết bộ phân giải phiên bản theo luật gần nhất thắng của Maven và theo luật cao nhất của Gradle".
  - L27 dòng 231, mục 2 thành "Đọc kết quả chạy thật của một dịch vụ phong bì tối giản bằng JDK: mã trạng thái 200, 500 và 400", mục 3 thành "So sánh kích thước đã đo của phong bì với JSON tương đương".
- `introduces`: L28 chuyển `bnx_explain` từ step formula#2 sang step sym (bảng "viết trong lệnh" thứ 2), vì lời giảng `explain` xuất hiện sớm hơn. Không thêm mục sổ.
- `labs/BNX/L25/de.md`, `labs/BNX/L26/de.md` được `write_lab` ghi lại có dòng "MÔ PHỎNG" (nội dung chấm và lời giải không đổi).
- ASR/phát âm: mọi câu `say` mới/đổi là câu TTS mới; cần dò "xô", "bể", "ngoặc nhọn", "tiền tố", "thực thể", "mã lỗi một nghìn không trăm lẻ ba", "tệp tín hiệu", "đô la ngoặc", "hộp" (Docker), "luồng chạy hàm song song".
- Docker: không để lại container nào của nhóm A (`bnx-l28-*` tự xoá); `bnx-ora`, `bnx-mss` chỉ qua `dbrun`; DB tạm `bnx_l25` tự dọn.

## Không sửa (lý do)
- L25 example#3 báo "PLAUSIBLE": hàm `chuyenKiem` không hiện — đã sửa (hiện mã). Phần "viết theo mẫu `chuyenLoi` ra 900, nhật ký 1": giải thích bằng mã hiện và `mo(...)` đặt lại nhật ký trước mỗi ca (đã có ở màn hình).
- L26: báo hiển thị 00033 (khung nhấn rơi vào dòng chú thích): sau khi thêm step mới không tái hiện (khung nhấn nay rơi vào khối đầu ra, đã xem 00046/00049/00051); không đổi thêm.
- Hiển thị: L28 step T-SQL còn hiện thêm dòng `b.join()` (dòng thứ 4 của đoạn trích); vô hại, không đổi.
- L25 REPEATABLE_READ SQL Server: bài nói "lệnh sửa của B phải chờ A" (đã đo Msg 1222 là hết hạn chờ khoá, không phải lỗi ngay).

## Tệp đã sửa
`audit/bnx/src/l24.py … l28.py`; `audit/bnx/ver/l24.py`, `ver/l25.py`, `ver/l28.py`; `audit/bnx/screen/l24..l28.yaml` (sinh lại); `audit/bnx/progcache/L24.json`, `L28.json` (đệm đầu ra); `lessons/bnx/L24…L28_*.yaml` (gen); `labs/BNX/L25/de.md`, `L26/de.md`; `out/BNX/L24..L28/frames`.
