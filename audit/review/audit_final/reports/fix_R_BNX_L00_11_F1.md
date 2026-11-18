# F1 — sửa BNX L06 và soạn bài mới L37 (2026-11-14)

Phạm vi: L06 (cắt T-SQL, SQL injection, JDBC ra khỏi bài, sửa SHOULD/P1 của L06) + bài mới L37 "T-SQL và JDBC: XACT_ABORT, chống chèn mã, kết nối an toàn". Không chạm L07/L38, L08–L11, L00 bản đồ, L36, pack.py.

## L06 (3 054 → 2 253 từ lời đọc)
- Giữ phần Oracle; bỏ ngôn ngữ T-SQL, XACT_ABORT, SQL injection, JDBC (sang L37). Tiêu đề: "Bài 6 — Thủ tục lưu trữ trên Oracle: tham số, giao dịch và bắt lỗi"; slug/tên tệp giữ nguyên (`L06_thu_tuc_luu_tru_plsql_tsql.yaml`).
- Mục tiêu cuối (5): (1) Viết thủ tục chuyển tiền có tham số vào và ra bằng PL/SQL; (2) Hoàn tác khi lỗi bằng khối bắt lỗi PL/SQL và nhận ra lỗi bị nuốt; (3) Khoá hai tài khoản theo một thứ tự cố định; (4) So số câu lệnh gửi tới cơ sở dữ liệu khi logic nằm ở ứng dụng (mô hình giản lược 5 câu mỗi lần) với khi gọi thủ tục, ở 10, 1 000 và 100 000 lần chuyển; (5) Viết hàm chuyển tiền có giao dịch và hoàn tác khi vi phạm ràng buộc số dư (lab sqlite). `covers` đủ 5/5.
- P1 tại chỗ: bảng dựng bằng `CREATE TABLE` (PRIMARY KEY, NUMBER, VARCHAR2, CHECK, INSERT, COMMIT, DROP IF EXISTS) giảng ở prereq; sym 2 bảng giải mã PL/SQL (IN/OUT, CREATE PROCEDURE…AS…BEGIN…END, SELECT…INTO, `:=`, LEAST/GREATEST, RAISE_APPLICATION_ERROR, EXCEPTION WHEN OTHERS, RAISE, DECLARE…BEGIN…END + dấu `/`, DBMS_OUTPUT.PUT_LINE); "ngoại lệ" giảng ở bước 5; `isolation_level=None` giảng ở lab (màn hình, lời, de.md).
- SHOULD đã sửa: nêu "Oracle Database Free 23 (banner 26ai Free 23.26.3)" trên màn hình + `ver` kiểm banner; hệ số ×5 ghi rõ "mô hình giản lược" (tiêu đề cảnh, tiêu đề khối mã, tiêu đề cột bảng, lời đọc, mục tiêu giáo án; nói thẳng "JDBC không gửi riêng câu mở giao dịch, số câu thật phụ thuộc cách viết"); cảnh `check` mới (mô hình Python thuần cho cùng kết quả như Oracle); Lỗi 2 (chốt/hoàn tác trong thủ tục tác động lên giao dịch người gọi, trước đây lẫn trong lời bước 5).
- Hook/recap: bỏ hứa JDBC; recap có `forward_ref` nói thủ tục SQL Server, chặn câu lệnh lạ chèn qua chuỗi gõ và Java nằm ở bài cuối khoá (dùng từ "chặn câu lệnh lạ chèn…" để không dính term `chèn mã` trước khi giảng).
- Nguồn `audit/bnx/src/l06.py`, `audit/bnx/ver/l06.py` (chỉ Oracle + Python; 22/22 PASS), `audit/bnx/screen/l06.yaml` (sổ viết lại: khối Oracle giữ bằng sha, thêm nguồn `L06_MoHinh`; bỏ nguồn SQL Server/Java).

## L37 (mới, 2 276 từ lời đọc, 12 cảnh AF2)
- Tệp: `lessons/bnx/L37_tsql_jdbc_xact_abort_chen_ma.yaml` (sinh từ `audit/bnx/src/l37.py`), `audit/bnx/ver/l37.py`, `audit/bnx/screen/l37.yaml`, `audit/bnx/sources_l37.md`, `tools/checklib_bnx/l37.py`, `labs/BNX/L37/{de.md,mong_doi.txt,loi_giai.py}`, `audit/bnx/deps/l37/README.md` (+ `ojdbc11-23.26.4.0.0.jar`, bị .gitignore), `audit/bnx/pending/c37.json`.
- Mục tiêu (8): (1) Viết thủ tục chuyển tiền có tham số vào và ra bằng T-SQL và chạy trên SQL Server 2022; (2) Nêu và đo tổng tiền khi một lỗi xảy ra giữa giao dịch với XACT_ABORT tắt và bật; (3) Hoàn tác khi lỗi bằng khối TRY…CATCH có ROLLBACK và THROW; (4) Đếm số dòng lộ ra khi ghép chuỗi và khi tham số hoá, ở bảng 2, 200 và 20 000 dòng; (5) Gọi thủ tục từ Java bằng CallableStatement và đọc tham số ra; (6) Mở kết nối an toàn: đóng bằng try-with-resources, lấy mật khẩu từ biến môi trường, tham số hoá bằng PreparedStatement; (7) Chọn cách chặn chèn mã theo tình huống và nêu cái được, cái mất; (8) Viết hàm tìm tài khoản theo tên bằng ghép chuỗi và bằng tham số, rồi so số dòng với chuỗi tấn công. `covers` 8/8.
- Chạy thật: SQL Server 2022 RTM-CU27-GDR 16.0.4315.2 (hiện CREATE DATABASE/TABLE/INSERT đủ trên màn hình + phiên bản); XACT_ABORT tắt → 1 800 000, bật → 1 300 000; quy mô chèn mã 2/200/20 000 dòng (ghép chuỗi lộ 2/200/20 000, tham số 0); JDBC Java 21 + ojdbc 23.26.4.0.0 gọi thủ tục Oracle bài 6: `500000: loi 20001`, `200000: OK`, PreparedStatement `A: 1 dong`, chuỗi tấn công `0 dong`. Java hiện đủ `import`, khung `class`/`main`, mật khẩu từ `System.getenv`.
- E52: thêm vào `tools/registry/symbols.BNX.yaml` sáu mục (`bnx_plsql`, `bnx_raise_app_error`, `bnx_dbms_output` introduces ở L06; `bnx_tsql`, `bnx_sp_executesql`, `bnx_chen_ma` ở L37; `bnx_xact_abort`, `bnx_jdbc`, `bnx_ngoai_le` đã có sẵn, L06 giữ `bnx_ngoai_le`, L37 `introduces` xact_abort/jdbc và `assumes: [bnx_ngoai_le]`). `bnx_ngoai_le` PHẢI ở L06 vì L25 và L30 `assumes` nó.
- Giáo án: `curriculum/bnx.yaml` mục L37 ở cuối (requires [L36], requires_ext ["BNX:L06"]) + dòng VER trong `audit/verify_plan_curricula.py` (và sửa chữ mô tả VER của L06 "Oracle"); mục L06 sửa tiêu đề/mục tiêu/example/fix.

## Cổng thật (2026-11-14)
- `gen.py L06`, `gen.py L37` → ghi; `lv.py lint` L06: 0 FAIL 0 WARN; L37: 0 FAIL 0 WARN. `lv.py render` L06 0 vấn đề, L37 0 vấn đề.
- `verify_bnx.py L06`: 22/22 PASS; `verify_bnx.py L37`: 21/21 PASS (không SKIP; JDBC chạy thật).
- `screen_fast.py L06 L37`: 0 FAIL 0 STALE 0 MISSING 0 ORPHAN.
- `lv.py curriculum curriculum/bnx.yaml`: 38 bài, 1 lỗi duy nhất `L17: assumes ['bnx_base64url']` (không thuộc phạm vi F1; xuất hiện cùng lúc các tác tử khác sửa).
- `check_curricula_graph.py`: 0 tham chiếu hỏng, 0 chu trình, VER 0 lỗi; `tests/test_e52.py` 0 FAIL; `check_next_refs.py` 0 lệch.
- `lab_gate.py BNX`: 39 PASS · 0 FAIL (gồm lab L06 và L37).
- Khung PNG đã xem (L37): sym (00024), formula bước 1 (00036), check Goi.java 1/4 (00060), pitfalls lỗi 1 (00084).

## Không làm / lưu ý
- Không dựng lại video (`build`/`tts`/`asr`). Mọi `say` đổi/mới ≥ 8 từ, ≥ 4 ≤ 38 từ theo lint; chưa dò ASR các câu mới (do người điều phối dựng).
- ojdbc: tệp chép từ thư mục tạm của phiên 2026-11-11, kiểm sha1 khớp con số đã ghi từ khi tải về từ Maven Central (109dbf46…); chưa tải lại từ mạng. README nêu cách tải lại.
- Bài chỉ chạy JDBC với Oracle; câu "với SQL Server chỉ đổi địa chỉ và thư viện" KHÔNG đưa vào bài (chưa chạy thử); sources_l37.md [L37SCOPE] ghi rõ.
- Term `chèn mã` đăng ký E52: L38/L07 hoặc bài khác nếu dùng cụm này mà chưa giảng sẽ bị lint bắt (hiện chỉ L37).
- `bnx_plsql` đăng ký E52: bài khác có chữ PL/SQL mà chưa `assumes` sẽ bị bắt (hiện chỉ L06).
- Ledger L06/L37: khối Oracle/SQL Server (kind run lang oracle/mssql) không do `lib2.py gen-screen` sinh được; đã sinh bằng gen-screen (Python/Java/lab) rồi gộp tay bằng script (khối Oracle của L06 giữ nguyên sha; khối SQL Server của L37 chạy thật để lấy `expect_stdout`). Chạy lại `gen-screen` sẽ xoá phần gộp tay.
- Hostname container SQL Server `461d1255632f` nằm trong `expect_stdout` các khối L37 `Msg …` (như L06 cũ); dựng lại container thì sinh lại.
