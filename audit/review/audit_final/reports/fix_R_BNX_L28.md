# fix_R_BNX_L28 — sửa BNX L28 theo báo cáo người đọc R_BNX_L24_30 (2026-11-14)

Nguồn đã sửa: `audit/bnx/src/l28.py`, `audit/bnx/ver/l28.py`, `tools/checklib_bnx/l28.py`, `tools/registry/symbols.BNX.yaml` (nhóm L28), `curriculum/bnx.yaml` (ví dụ L28: nhãn mô phỏng). YAML bài/lab/sổ màn hình do `gen.py` và `lib2.py gen-screen` sinh lại. Lời đọc 2 297 từ (≤ 2 300; trước đó 2 234).

## MUST
| Mục báo cáo | Đã sửa thế nào |
|---|---|
| L28 example step 5: MySQL không hiện mã lỗi | Thêm step MySQL "ChayMy (trích)" (mã phiên A/B), step kết quả hiện nguyên văn `phien ban: 8.4.13` + `ERROR 3572 (HY000) at line 1: Statement aborted because lock(s) … NOWAIT is set.` (lấy từ đầu ra thật của ChayMy, dòng lược bằng "…"), công thức ④ nêu ba mã; lời đọc đọc ra "lỗi ba nghìn năm trăm bảy mươi hai"; thêm step bảng so BỐN hệ (PostgreSQL, MySQL, Oracle, SQL Server) với chữ lỗi nguyên văn máy in → mục tiêu 2 làm được. Hook ghi "MySQL báo ERROR 3572" (hết "mã lỗi riêng"). Ví dụ giáo án vốn đã nêu 3572, nay khớp. `covers` giữ nguyên (2 → example). |

## SHOULD
| Mục | Xử lý |
|---|---|
| "MongoDB không khoá dòng … cập nhật có điều kiện" gợi ý chỉ MongoDB | Hook (màn hình + lời) nói hệ quan hệ cũng viết được kiểu này; thêm step formula "Làm thử ở hệ quan hệ": `UPDATE tk SET so_du = so_du - 600 WHERE id = 1 AND so_du >= 600` (số dòng bị sửa 1 hoặc 0); Lỗi 3 và bảng CV ở recap nêu cách chữa ở hệ quan hệ. Kiểm: `ver/l28.py` chạy sqlite thật (1 rồi 0, còn 400) + `alg.bnx_l28_sql_update`. |
| "đọc rồi ghi" là mô phỏng không gắn nhãn (khung 00053) | Hộp đỏ cỡ chữ thường "MÔ PHỎNG bằng Python: hai biến gán tay, không phải hai phiên tranh chấp thật" ở step kết quả; tiêu đề khối mã bắt đầu bằng "MÔ PHỎNG bằng Python, không phải tranh chấp thật"; "Kết quả chạy thật" → "Kết quả mô phỏng"; lời đọc check và Lỗi 3 nói "mô phỏng"; giáo án `example` ghi MÔ PHỎNG. |
| Lời Oracle ORA-00054 khác bản tài liệu Oracle | Không so với tài liệu (không tải được, NOT_VERIFIED): màn hình và lời nói rõ chữ sau mã là nguyên văn của bản đang chạy (đầu ra thật Oracle 26ai / SQL Server 2022 / MySQL 8.4), nên bắt lỗi theo MÃ chứ không theo chữ; bảng bốn hệ ghi "nguyên văn máy in". |
| Lab: "<ba số>" không nói cách nhau bằng gì | `de.md` và đề trên màn hình: ba số (mỗi số 1 hoặc 0, theo thứ tự ba lần rút) cách nhau bằng MỘT dấu cách. |
| hook "năm hệ" nhưng màn hình chỉ có mã Oracle | Cả năm hệ nay có trên màn hình: PostgreSQL (step 3), Oracle và SQL Server, MySQL (step mới), MongoDB (step ⑤). |

Không sửa: ghi nhận "MongoDB 8.3.17 / PostgreSQL 17.12 PLAUSIBLE" của người đọc là giới hạn kiểm tra của họ (số phiên bản lấy từ đầu ra thật của ảnh Docker ghim băm; không đổi).

## P1 (thuật ngữ tại chỗ)
| Thuật ngữ | Cách giảng | E52 |
|---|---|---|
| EXPLAIN | formula step 2: "Câu lệnh EXPLAIN đặt trước truy vấn bắt hệ in kế hoạch: sẽ đọc bảng cách nào, Seq Scan hay Index Scan"; lời: "lệnh xem kế hoạch đặt trước truy vấn" | `bnx_explain` (`(?i)\bexplain\b`), `introduces` ở step đó |
| `$gte`, `$inc` | cảnh `sym` (hàng đã có: lớn hơn hoặc bằng; cộng thêm) | `bnx_gte` (`\$gte`), `introduces` ở step sym |
| mongosh | tiêu đề khối mã ⑤: "gõ trong mongosh là dòng lệnh của MongoDB"; lời: "dòng lệnh của cơ sở dữ liệu JSON" | `bnx_mongosh`, `introduces` ở step ⑤ |
| Docker | example step 1: tiêu đề + lời "công cụ chạy chương trình trong một hộp đóng sẵn gọi là ảnh" | KHÔNG đăng ký `term:` — L31/L32 (bài của nhánh khác) dùng "Docker" và tự giảng tại chỗ; đăng ký sẽ làm E52 của chúng FAIL. Vẫn giảng tại chỗ ở L28. |
| MVCC | Chỉ nằm trong chuỗi `source:` (không lên màn hình/lời): bỏ khỏi `source` | không cần |
| nguyên tử | Cảnh prereq đã giảng; `assumes=["bnx_nguyen_tu"]` (id do L25 giới thiệu — cần L25 `introduces` mục này, nếu không `lv.py curriculum` báo thiếu) | `bnx_nguyen_tu` (nhóm L25) |

Lưu ý nhánh khác: forward-ref ở recap của L28 trước đây ghi "CQRS và Event Sourcing" (E52 của L29 bắt) — đổi thành "lưu sự kiện thay vì lưu số dư" (lời đọc không đổi).

## Độ bền của chương trình MySQL
`verify_bnx.py L28` rớt ChayMy hai lần trong lúc máy bận (đầu ra rút còn khác cache) vì `sleep 3` chờ phiên A giữ khoá là cuộc đua thời gian; chạy tay riêng lẻ thì khớp. Đã thay bằng `wait_lock` (đợi tới khi `performance_schema.data_locks` có khoá dòng, tối đa 60 s); đầu ra không đổi, digest cache đổi (chạy lại thật một lần), tiêu đề/lời đọc nói "đợi tới khi biết chắc A đã giữ".

## Cổng (số thật, chạy tuần tự, Docker mỗi lần một ảnh)
- lint 0 FAIL / 0 WARN / 30 PASS
- render 104 khung, 0 vấn đề (tách thêm step cho EXPLAIN và UPDATE quan hệ; hộp MÔ PHỎNG ở step kết quả để khỏi tràn)
- verify_bnx L28: 20/20 PASS (lần chạy cuối, sau wait_lock và giữ khoá 30 giây)
- gen-screen L28: 17 khối, ghi 17, chưa khớp 0
- lab_gate BNX: 13 PASS · 0 FAIL
- screen_fast L28: 17 khối — PASS 25 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0
- Chạy tuần tự, một ảnh Docker mỗi lần. Hai lần chạy trước đó (khi máy rất bận, nhiều nhánh cùng dùng Docker) có FAIL do cuộc đua thời gian: ChayMy (sleep 3) và sau đó ChayPg/ChayMy (phiên A giữ khoá 6–8 giây hết trước khi phiên B kịp thử vì `docker exec` chậm). Đã sửa gốc: MySQL `wait_lock`; phiên A của PostgreSQL và MySQL giữ khoá 30 giây (container bị `docker rm -f` ngay sau khi B thử nên không tốn thêm thời gian); tiêu đề/lời đọc ghi 30 giây.
- Khung đã xem: example (MySQL code, kết quả 4 hệ, bảng so bốn hệ), formula step 2, check (hộp MÔ PHỎNG).
