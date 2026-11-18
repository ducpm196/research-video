# fix6 BNX_C nhánh C1 (L26–L28) — 2026-11-16

## TIẾN ĐỘ
- [x] L26 xong  - [x] L27 xong  - [x] L28 xong

Khuôn: `audit/bnx/libj.py` (`jstep`, `nowrap`; không sửa); hàng riêng của bài khai bằng bộ ba trong `lNN.py`. Nguồn sửa: `audit/bnx/src/l26.py … l28.py`, sinh bằng `gen.py`; không sửa YAML sinh ra; sổ chỉ qua `screen_keep.py`/`screen_fast.py`. Không docker/dbrun/build/tts/asr/git.

## L26 (Maven, Gradle, Jenkins)
- Mục chưa giảng → 0: `M=…/mvn`, `test -x $M || { …; exit 97; }`, `mkdir -p … && cp A B`, `$M -B -q -f $1 clean package > /dev/null 2>&1`, `sha256sum` (bảng 4 hàng ĐỨNG TRƯỚC khối `dung()`/`so()`); `$2`, `sleep 2` (hàng sym#2); quymo#1: `mkdir -p $d && cp pom-$d.xml $d/pom.xml`, `(cd $d && … dependency:list -DoutputFile=ds.txt)`, `grep -c ':jar:'` (bảng 3 hàng trước khối); example#7: `def chay(cac_buoc, hong=None)`, `ket = []`/`append`/`+`, `if hong == ten`/`break`, `for … else:` (bảng 4 hàng trước `PY_PIPE`); check#1: `CAY = {…}` (từ điển, khoá cặp), `da, hang = {}, […]`, `while hang:`, `hang.pop(0)` (bảng 4 hàng), `in`/`continue`, chuỗi f `da[ten]`, `da[ten] = ban`, `hang += […CAY.get((ten, ban), [])]` (bảng 4 hàng) — hai bảng đứng trước `PY_GIAI`.
- SHOULD: hiện đủ mã `M=` và `dung()`: `SH_TAILAP` tách hai khung (dòng 1–7: `M=`, kiểm, `mkdir`, `dung()`; dòng 8–13: `so()` và hai lần gọi) — mã nguyên văn, sha không đổi; ô "(×N)" bảng quy mô bọc `nowrap()`.
- Cắt lời đọc ~420 từ để bù (hook, prereq, sym, formula, intuition, ví dụ, pitfalls, quiz, practice, recap). Lời đọc 2288 → 2294 (đếm tổng `len(say.split())`; mỗi `say` 8–38 từ; lint 0 WARN).
- Cổng: lint 0/0; render 124 khung 0 vấn đề (xem khung 50, 53, 73); `verify_bnx L26` 25/25 PASS (Maven 3.9.11 chạy thật); `screen_keep` 19 khối chưa khớp 0; `screen_fast` PASS 38, FAIL/STALE/MISSING/ORPHAN 0.
- asr_reviewed 1 → 1. Mục chưa giảng ước còn lại: 0.

## L27 (SOAP/WSDL/SFTP)
- Mục chưa giảng → 0: formula#4 Java (`var f = …newInstance()`, `setNamespaceAware(true)`, `if (chan) f.setFeature(…, true)`; bảng 3 hàng trước khối mã, hàng nêu `chan` là tham số của hàm chứa đoạn trích); formula#5 (`def gui(…)`, `os.path.join`, `with open … as f`/`f.write`, `os.rename`: bảng 4 hàng); example#5 (`with tempfile.TemporaryDirectory() as nhan`, `open(…, "w").write(lo[:300])`, `sorted(f for f in os.listdir(nhan) if not f.endswith(".part"))`: bảng 3 hàng); check#1 (`rstrip("\n").split("\n")`, `_, so, ma = dong[-1].split("|")`, `"\n".join(dong[:-1]) + "\n"`, `len(dong) - 1 != int(so)`, `.encode()`/`hexdigest()`, `if … return`; ghép danh sách `[:900] + [-2:]`, `replace`: ba bảng); quymo#1 (`for n in (1000, 1000000)`, `h, byte, khoi = hashlib.sha256(), 0, 0`, `h.update`, `range(1, n+1)`, câu lệnh cách nhau `;`: bảng 4 hàng). Mục yếu: mã HTTP 200/400/500 giảng nghĩa ở hook (hộp + lời đọc); OWASP chú "tổ chức về an toàn ứng dụng web"; tiêu đề khung ghi `tao_lo(n)` định nghĩa ở đầu tệp.
- SHOULD: so SOAP với JSON CÙNG cách viết liền: phong bì viết liền 203 byte (bỏ dấu cách đầu dòng và xuống dòng giữa thẻ), 203 : 20 ≈ 10,2 lần; phản hồi 211 (đã viết liền) : 16 ≈ 13,2; ghi rõ "246 là tệp thụt dòng"; sửa hình (intuition#1), công thức (example#2), lời đọc, `checks`, hàng CV ở recap ("≈ 10 lần"). `ver/l27.py` thêm kiểm: tính lại 203 bằng mã (regex) và tỉ lệ 10,2.
- Cắt lời đọc ~370 từ để bù. Lời đọc 2289 → 2296. Lint 0/0.
- Cổng: render 117 khung 0 vấn đề (xem khung 24, 45, 64); `verify_bnx L27` 22/22 PASS; `screen_keep` 17 khối chưa khớp 0; `screen_fast` PASS 25, 0 lỗi.
- asr_reviewed 10 → 6 (4 câu đổi chữ). Mục chưa giảng ước còn lại: 0.

## L28 (cơ sở dữ liệu so sánh; bài có Docker/Oracle/SQL Server: chỉ đọc, không chạy)
- Mục chưa giảng → 0 (bảng ĐỨNG TRƯỚC khối mã, step sau bảng `clear: true`): mongosh: `js '…'`, `print`, `insertMany([{…}])` (danh sách/bản ghi/trường lồng), `findOne`/`JSON.stringify`, `countDocuments({"gd.loai": …})` (bảng 4 hàng, `introduces: bnx_mongosh` chuyển lên đây); vòng PostgreSQL: `for n in 1000 100000 1000000; do … done`, `create table … primary key`, `insert … select g, 'K'||g from generate_series`, `where so = 'K7'`/`create index` (4 hàng); `begin; … commit;`, `select 1 … for update` (2 hàng); `psql -U -o /dev/null -f`, `until … test -f … sleep 0.5; done`, `2>&1 | head -1`, `docker rm -f … >/dev/null 2>&1` (4 hàng); MySQL: `sh -c "mysql … < /mysqla.sql"`, `wait_lock`, `q "…" | head -1` (3 hàng); mongosh rút: `var rut = () => …updateOne(…).modifiedCount`, `+ rut()`, `findOne(…).so_du` (3 hàng); Python: từ điển, `def`/`return`, `doc_a = doc_b = 1000`, `print`/`#` (4 hàng, trước khối `RutTien`). Hàng mới ở bảng cũ: `-tA` (sym#2), `SELECT … INTO x` + `ROLLBACK` và `args=(x,)` (sym#4). Khoá chính/khoá ngoại/JOIN định nghĩa ở prereq (bảng prereq gộp hai cột "nghĩa (ví dụ)" cho khỏi tràn).
- SHOULD: bỏ dấu `'` thừa: hai khung mongosh nay hiện từ dòng `js '` tới dòng có `'` đóng (hàm `_mg_show`, chữ khối mã và sha không đổi). Dòng `var rut = … modifiedCount;` dài sát mép phải khung (không tràn theo bộ kiểm render); không rút ngắn được vì sửa chữ khối Docker sẽ đổi sha mà không chạy lại được.
- Lời đọc 2275 → 2294 (cắt ~480 từ bù: hook, symbol, intuition, formula, ví dụ, check, quymo, pitfalls, quiz, practice, recap). Lint 0/0.
- Cổng: render 124 khung 0 vấn đề (xem khung 4, 30, 75); `screen_keep` 18 khối chưa khớp 0; kiểm sha-only (`shachk`): MISSING 0, STALE 0, ORPHAN 0. KHÔNG chạy `verify_bnx L28` và `screen_fast L28` (cần Docker/Oracle/SQL Server: NOT_VERIFIED lần này).
- asr_reviewed 6 → 0 (câu bị đổi chữ/tách câu; cần nghe ASR lại khi dựng).
- Mục chưa giảng ước còn lại: 0 (trừ `args=("""…""",)` đã vào bảng; không còn mục yếu nào chưa nêu).

## Việc người điều phối còn lại
- `screen_try.py --merge` một lần; curriculum, check_curricula_graph, test_e52, lab_gate, arith_scan; chạy `verify_bnx L28` + `screen_fast L28` khi được phép dùng Docker.
- Dựng lại L26, L27, L28.
