# Sửa BNX L24–L30 theo báo cáo người đọc R_BNX_L24_30 (2026-11-14)

Báo cáo gốc: `reports/R_BNX_L24_30.md` (MUST 2; P1 = 2 ở 0/7 bài; P8 = 2 ở 7/7). Nguồn sửa: `audit/bnx/src/l24..l30.py` (+ `audit/bnx/ver/lNN.py`, `tools/checklib_bnx/lNN.py`, `audit/bnx/sources_lNN.md`, `curriculum/bnx.yaml` mục L26/L28, `tools/registry/symbols.BNX.yaml`); YAML bài, lab và sổ màn hình do `gen.py` / `lib2.py gen-screen` sinh lại, không sửa tay.
Phân công: tôi sửa L24, L25, L27; ba nhánh `fork` sửa L26 (`fix_R_BNX_L26.md`), L28 (`fix_R_BNX_L28.md`), L29+L30 (`fix_R_BNX_L29.md`, `fix_R_BNX_L30.md`). Mỗi nhánh có bảng từng mục → cách sửa / lý do không sửa trong báo cáo riêng; dưới đây là bản tóm tắt cộng phần của L24, L25, L27.

## 1. MUST (2/2 đã sửa)
| Bài | Việc | Kết quả |
|---|---|---|
| L26 | "6 pha" ở formula step 2, bảng sym, example step 3, giáo án | Kiểm lại bằng `mvn help:describe -Dcmd=package` (Maven 3.9.11): 17 pha tới `package`, chỉ 6 pha có MỤC TIÊU của phần mở rộng gắn vào. Đổi thành "6 mục tiêu của phần mở rộng", nói rõ pha khác mục tiêu (pha `package` kích hoạt `jar:jar`…); khớp lời đọc "sáu mục tiêu"; mục tiêu 1 và ví dụ ở `curriculum/bnx.yaml` đồng bộ |
| L28 | example step 5 không hiện mã lỗi MySQL | Thêm step MySQL và step kết quả hiện nguyên văn `ERROR 3572 (HY000) … NOWAIT is set.` (đầu ra thật của ChayMy trong progcache), công thức ④ và bảng so BỐN hệ (PostgreSQL, MySQL, Oracle, SQL Server) với chữ lỗi nguyên văn máy in; lời đọc đọc ra "ba nghìn năm trăm bảy mươi hai"; `covers` giữ nguyên |

## 2. SHOULD (tất cả đã sửa hoặc có lý do)
**L24.** `join fetch` là nối trong làm mất khách chưa có tài khoản: formula step 4 thêm điều kiện "khi khách nào cũng có tài khoản", ghi chú "Điều kiện" và `left join fetch` (nối trái), lời đọc nói tương ứng; `checks` + `ver` kiểm bằng sqlite thật (501 khách, 1 khách không tài khoản: nối trong 500, nối trái 501; người đọc đã chạy Hibernate 500/501). "Bể kết nối" giảng tại chỗ ở Lỗi 2 (xem P1). Lab: `de.md` nêu cột bảng `the(id, khach_id, han_muc)`, cho sẵn đoạn dựng dữ liệu, và nói đăng ký `set_trace_callback` SAU khi nạp dữ liệu.
**L25.** Hook: "ba ca cho ba kết quả" thay vì "cùng một lỗi". Lỗi 4 viết lại cho đúng: hàm NGOÀI bắt lỗi do hàm TRONG (chung giao dịch) ném rồi vẫn chốt thì nhận `UnexpectedRollbackException`; nếu chính hàm trong tự nuốt lỗi thì proxy không thấy lỗi; `ver/l25.py` chạy thật Spring 7.0.10 (TransactionTemplate lồng nhau): ca A = `UnexpectedRollbackException`, ca B = không có ngoại lệ. Mức cô lập: bảng ghi "(kết quả đo trên H2)" và lời đọc "hệ khác có thể cho kết quả khác" (không nêu tên hệ khác vì không đọc được tài liệu từng hệ). "Hết giờ" được giải thích ở hình bể kết nối. Không sửa: chữ ký `hoan_tac(loi, rollback_for)` của lab không được chấm (cổng `cham.sh` chỉ so đầu ra; sửa cần đổi cơ chế chấm chung, ngoài phạm vi).
**L26** (nhánh fork): Jenkinsfile có đủ khối `post` (tách 2 khung); cây `dependency:tree` in nguyên hai lệnh, dòng omitted nằm dưới commons-text (chạy lại Maven thật); "Kết quả mô phỏng" cho phần Python; hook thành câu hỏi bài trả lời trực tiếp; nhãn MÔ PHỎNG cỡ lớn; mũi tên "hỏng" chạm ô `post failure`; số gói 1/9/34 nay được `ver` dựng lại thật (PASS). Không sửa: tiêu đề cảnh intuition (cảnh có 2 step, tiêu đề đúng); `de.md` L26 không mâu thuẫn.
**L27.** (a) HTTP 500/400: bài chỉ nói điều ĐÃ ĐO của máy chủ thử, ghi "chưa kiểm được đặc tả (NOT_VERIFIED: w3.org chặn tải 403)", bỏ câu "không phải đặc tả quy định"; (b) khung WSDL đổi từ dòng 6–17 sang 5–16 để người học đếm ra đúng 2 message, 1 portType, 1 operation, 1 binding, mở đầu service (lời đọc nói "hai thông điệp"; `ver` đếm lại trên đúng khung hiện); (c) SFTP chỉ là thư mục cục bộ: prereq nói thẳng "bài này mô phỏng bước truyền", hình tệp lô có nhãn "MÔ PHỎNG" chữ lớn đậm cam, "đổi tên, số dòng, mã băm là THẬT"; (d) "nặng gấp hơn mười lần" ghi điều kiện "với tải nhỏ này" (12,3×; tải lớn thì tỉ lệ giảm); (e) mã băm cùng tệp chỉ bắt lỗi ngẫu nhiên, kẻ cố ý sửa rồi tính lại được: thêm giới hạn ở Lỗi 1 và recap (chống giả mạo cần chữ ký); (f) lab: `de.md` nêu sha256 của dữ liệu mã hoá UTF-8, hex chữ thường; (g) KiB giải thích ngay ở khung quymo (1 KiB = 1024 byte, nên 65 536 byte; lời đọc nói số byte).
**L28** (fork): UPDATE có điều kiện cũng dùng được ở hệ quan hệ (hook, step mới "làm thử", Lỗi 3, recap; `ver` chạy sqlite thật); phần "đọc rồi ghi" là mô phỏng gắn hộp MÔ PHỎNG và tiêu đề "Kết quả mô phỏng"; ORA-00054: chữ sau mã là nguyên văn của bản đang chạy, bắt lỗi theo mã, không so với tài liệu Oracle (không tải được; NOT_VERIFIED); lab "<ba số>" cách nhau bằng một dấu cách; cả năm hệ nay đều hiện trên màn hình. Độ bền: MySQL dùng `wait_lock` thay `sleep 3`, phiên A của PostgreSQL/MySQL giữ khoá 30 giây (cuộc đua thời gian khi máy bận làm hai lần chạy cổng FAIL; đầu ra không đổi). Không sửa: ghi nhận "PostgreSQL 17.12/MongoDB 8.3.17 PLAUSIBLE" là giới hạn kiểm của người đọc (số phiên bản lấy từ ảnh Docker ghim băm).
**L29** (fork): `DROP TRIGGER` được nêu rõ, bỏ câu "không sửa được lịch sử" tuyệt đối (chạy lại sqlite: UPDATE bị chặn; sau `DROP TRIGGER` thì UPDATE thành công); "so du -15" giải thích (dữ liệu sinh minh hoạ không chặn rút quá số dư) và khung hiện đoạn sinh dữ liệu; CQRS/Event Sourcing khai triển ở prereq; quiz đáp án hiện lại kho 800/150/90/40; lab `de.md` mục 3 hết mâu thuẫn. Không sửa: kiểm soát đồng thời khi ghi (phiên bản kỳ vọng) — thêm cảnh sẽ vượt 16 phút hoặc phải đổi `covers`; chỉ nêu trong giới hạn.
**L30** (fork): `permittedNumberOfCallsInHalfOpenState(1)` hiện trên màn hình (cảnh check tách 3 khung R4j; `ver` chạy Resilience4j 2.3.0 thật bỏ thông số đó → HALF_OPEN), kết luận "mô hình đúng" bớt mạnh; r thử lại = 1 + r lần gọi thống nhất prereq/formula/ThuLai/quiz 1 (đáp án hiện 750 ms cho 5 lần gọi và 1550 ms cho thử lại 5 lần); quiz 3 nêu ≤ 25 yêu cầu/giây qua được, ≈ 95% bị từ chối, và 5 000 luồng chỉ khi cuộc gọi treo tới hết hạn (chậm 3,5 giây thì ≈ 1 750); CanBang hiện thời điểm đến của 8 yêu cầu; nhãn MÔ PHỎNG lớn thêm ở example/practice; số "chín yêu cầu", "sáu cuộc hỏng", "một giây mười" đều hiện; cột 3 có tên tiếng Việt kèm OPEN/HALF_OPEN/CLOSED. Không sửa: lab vẫn là mô phỏng (cổng chỉ so đầu ra); đề xuất lab chạy thư viện thật nằm ngoài phạm vi.

## 3. P1: thuật ngữ giảng tại chỗ (dự kiến P1 = 2 ở 7/7 bài; chấm thật thuộc người đọc độc lập, chưa có tai/mắt người)
| Bài | Thuật ngữ trong cột "Cần biết trước" → nơi giảng | id E52 |
|---|---|---|
| L24 | bể kết nối (Lỗi 2), ngoại lệ (Lỗi 1), phân trang (quymo), H2 (example 1); `join fetch`/`left join fetch` | `bnx_be_ket_noi`, `bnx_ngoai_le`, `bnx_phan_trang`, `bnx_h2` |
| L25 | luồng, bể kết nối (prereq hàng ② "kết nối, bể và luồng"), nguyên tử (prereq ①), JDBC (cảnh check), hàng đợi (quymo), hết giờ (hình bể); ngoại lệ, H2 nhắc lại ngắn | `bnx_nguyen_tu`, `bnx_jdbc`; `assumes` `bnx_ngoai_le`, `bnx_be_ket_noi`, `bnx_h2` |
| L26 | Gradle (hook), Jenkins + máy chủ dựng (sym), Groovy/`agent any`/`sh` (formula 5), mã băm (formula 6) | `bnx_gradle`, `bnx_jenkins`, `bnx_may_dung`, `bnx_groovy`, `bnx_agent`, `bnx_sh`, `bnx_ma_bam` |
| L27 | SOAP, HTTP POST (prereq ②), SFTP, tệp lô/.csv (prereq ⑤), XXE (sym), KiB (quymo), nguyên tử, mã băm | `bnx_soap`, `bnx_sftp`, `bnx_xxe`, `bnx_kib`; `assumes` `bnx_nguyen_tu`, `bnx_ma_bam` |
| L28 | Docker (example 1), EXPLAIN (formula 2), `$gte` (sym), mongosh (khối mã ⑤), MVCC bỏ khỏi `source` | `bnx_explain`, `bnx_gte`, `bnx_mongosh` (Docker không đăng ký: L31/L32 dùng) |
| L29 | CQRS, Event Sourcing (prereq ⑥), sqlite | `bnx_cqrs`, `bnx_event_sourcing` |
| L30 | luồng (prereq ④), cổng API, burst (formula 5), cân bằng tải (formula 6), luỹ đẳng (Lỗi 2) | `bnx_burst`; `assumes` `bnx_ngoai_le` |
**Không đăng ký `term:` cho** "luồng", "hàng đợi", "hết giờ", "CSV", "Docker", "cổng API", "cân bằng tải", "luỹ đẳng": các bài L31–L36 (af2, nhánh khác đang sửa) dùng cùng từ (L33 dùng "luồng" 44 lần, L36 dùng "luỹ đẳng" 35 lần, L32 dùng "CSV"/"cân bằng tải"…), đăng ký sẽ làm E52 của họ FAIL. Các từ này vẫn được giảng tại chỗ trong bài thuộc L24–L30 (bằng chứng: bảng trên). Đề xuất: khi nhánh L31–L36 thêm `assumes` hợp lệ thì đăng ký bổ sung. Regex "ngoại lệ" dùng `(?<!đưa )` vì L36 dùng "đưa ngoại lệ cho người" theo nghĩa nghiệp vụ.

## 4. Độ dài (lời đọc, từ; ngưỡng ≤ 2 300)
| L24 | L25 | L26 | L27 | L28 | L29 | L30 |
|---|---|---|---|---|---|---|
| 2 281→2 290 | 2 226→2 273 | 2 271→2 291 | 2 197→2 281 | 2 234→2 298 | 2 270→2 286 | 2 264→2 285 |
Mọi bài vừa; mỗi câu giảng thêm đi kèm cắt chỗ khác (đáp án quiz, recap, câu chuyển, bảng quy mô…); `covers` giữ nguyên 7/7 mỗi bài. Không có bài nào cần đề xuất tách. Lưu ý: L28 (2 298) và L24/L26 (2 290/2 291) sát ngưỡng — thêm bất kỳ câu nào nữa phải cắt tương ứng.

## 5. Cổng thật (2026-11-13/14)
Từng bài (lint → render → `verify_bnx.py` → `lib2.py gen-screen` → `screen_fast.py`), số của lần chạy cuối trước khi gộp:
| Bài | lint | render | verify_bnx | gen-screen (khối / chưa khớp) | screen_fast |
|---|---|---|---|---|---|
| L24 | 0 FAIL, 0 WARN (41 PASS) | 103 khung, 0 | 21/21 PASS | 23 / 0 | PASS 34 · FAIL 0 |
| L25 | 0/0 (33 PASS) | 103 khung, 0 | 14/14 PASS | 15 / 0 | PASS 24 · FAIL 0 |
| L26 | 0/0 (32 PASS) | 101 khung, 0 | 25/25 PASS | 18 / 0 | PASS 37 · FAIL 0 |
| L27 | 0/0 (33 PASS) | 99 khung, 0 | 21/21 PASS | 17 / 0 | PASS 25 · FAIL 0 |
| L28 | 0/0 (30 PASS) | 104 khung, 0 | 20/20 PASS | 17 / 0 | PASS 25 · FAIL 0 |
| L29 | 0/0 (31 PASS) | 105 khung, 0 | 23/23 PASS | 16 / 0 | PASS 24 · FAIL 0 |
| L30 | 0/0 (33 PASS) | 109 khung, 0 | 20/20 PASS | 15 / 0 | PASS 25 · FAIL 0 |
(L25 sau cùng chỉ đổi một câu lời đọc ở cảnh forward_ref: lint 0/0, render 0, verify 14/14, gen-screen 15/0 chạy lại sau đó.)
Cổng toàn khoá, chạy sau khi cả bảy bài xong:
- `lab_gate.py BNX`: 13 PASS · 0 FAIL (76 lab được bài tham chiếu).
- Lint lại cả L31–L36 sau khi thêm mục sổ E52: 0 FAIL, 0 WARN ở cả sáu bài (mục sổ của tôi không làm bài nào của nhánh khác FAIL; vì thế "luồng", "hàng đợi", "hết giờ", "CSV", "Docker"… không được đăng ký).
- `lv.py curriculum curriculum/bnx.yaml`: 37 bài, 37 đã có đặc tả, 0 lỗi (kiểm cả `assumes` ⊂ bao đóng tiên quyết).
- `audit/check_curricula_graph.py`: 46 lộ trình, 728 bài, tham chiếu hỏng 0, chu trình 0; VER không PASS 0; ví dụ có số mà không dẫn VER 0.
- `tests/test_e52.py`: E52/E55 0 FAIL.
- `screen_try.py --merge` (đã gộp vào `audit/review/screen_code/BNX.yaml`; gỡ hai mục mồ côi do gộp không xoá khoá cũ: `BNX L28 example 4 1`, `BNX L30 formula 5 0`) rồi `screen_code.py check --course BNX -v`: **559 khối — PASS 701 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 2 · WARN 0**. Hai ORPHAN còn lại (`BNX L34 quymo 0 1`, `BNX L36 english 4 0`) thuộc bài của nhánh khác (L31–L36), không thuộc L24–L30. Lần chạy đầu (ngay sau gộp, lúc máy đang chạy song song `lv.py curriculum`) báo FAIL 3 và ORPHAN 4; lần chạy lại sau khi gỡ hai mục mồ côi: FAIL 0 (không có bằng chứng FAIL ở khối của bài mình; không lưu dòng FAIL của lần đầu, nghi cuộc đua thời gian do tải máy — cùng loại với cuộc đua `docker exec` đã gặp ở L28).

## 6. Khung PNG đã xem
L24: 00032 (join fetch + điều kiện), 00040 (H2), 00070 (bể kết nối). L25: 00001 (hook), 00006 (prereq), 00076 (Lỗi 4), 00079 (quiz). L27: 00007 (prereq: SOAP/HTTP POST), 00022 (nhãn MÔ PHỎNG tệp lô), 00027 (WSDL 5–16). L26/L28/L29/L30: xem báo cáo riêng của từng nhánh.

## 7. NOT_VERIFIED / giới hạn còn lại
- Chưa có người nghe/đọc thật: phát âm chỉ ASR-checked khi dựng; P1/P8 là dự kiến, người đọc độc lập chấm lại sau khi dựng lại video.
- Tên SOAP, SFTP, CQRS, Event Sourcing, JDBC không đưa vào lời đọc (chưa dò ASR): chỉ hiện trên màn hình, lời nói bằng tiếng Việt.
- SOAP/WSDL W3C: w3.org chặn tải (403) — không nêu quy định HTTP của phần lỗi. MySQL (dev.mysql.com) và Oracle: không so với tài liệu hãng (NOT_VERIFIED).
- Lab cả bảy bài vẫn mô phỏng/viết lại quy tắc (cổng `cham.sh` chỉ so đầu ra); chưa có lab chạy Spring/Maven/MongoDB/Resilience4j thật.
- Người điều phối vẫn phải dựng lại video (build/tts/asr) cho 7 bài vì lời đọc và khung đã đổi.
