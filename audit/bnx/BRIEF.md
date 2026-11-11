# Khoá BNX · Backend ngân hàng mở rộng theo JD — bản giao việc soạn bài (đợt LF1, 2026-11-11)

**Người học**: mất gốc, đã học JVA (Java từ số 0) và BNK (backend ngân hàng: Spring, REST + khoá lũy đẳng, SQL/PL-SQL, Redis, Kafka, SAGA, sổ cái,
T24, ISO 8583, đối soát, PIN/HSM). Mục tiêu: phỏng vấn Software Engineer / Backend ở ngân hàng (JD: `resources/job/JD.md`), rồi làm được việc thật.
Bài phải **tự đủ**: chỉ dùng khái niệm đã dạy ở JVA, BNK, bài BNX trước, hoặc giảng ngay trong bài (cảnh `prereq` ôn nền có ví dụ số).

## 0. Đọc trước (bắt buộc)
- `curriculum/bnx.yaml`: tiêu đề, mục tiêu (objectives), ví dụ (example), `fix` của bài bạn soạn. **Tiêu đề và mục tiêu chép NGUYÊN VĂN.** Mọi con số trong `example` phải xuất hiện trong bài.
- `audit/bnx/sources.md`: nguồn được phép dùng. Dữ kiện pháp lý, ngày, con số của sản phẩm **chỉ** lấy từ đây hoặc từ nguồn bạn tự đọc
  nguyên văn trong phiên (ghi thêm một dòng vào cuối `sources.md`: mã, dữ kiện, URL/tên tài liệu, ngày đọc, mức CITED). Không nhớ → không dạy.
- `audit/bnk/src/l03.py`: **bài mẫu**, giữ đúng khung 10 cảnh. `audit/bnx/lib.py`: `st`, `sc`, `table`, `svg`, `box`, `arrow`, `panel`, `txt`, `chain`,
  `lesson`, **`code`**, **`out`** (cuối tệp).
- `.claude/skills/lecture-video/references/pedagogy.md` (luật sư phạm), `references/production.md` (lỗi đã gặp).

## 1. Khung bài (giống BNK)
Mười cảnh theo thứ tự: `hook` (tình huống ngân hàng có con số) · `prereq` ("Trước hết: … điều cần hiểu", bảng khái niệm + ví dụ số) ·
`symbol` (giải mã từ/kí hiệu) · `intuition` (≥ 1 hình SVG cơ chế; nên có 2) · `formula` ("Suy ra từng bước", mỗi bước nói **vì sao**, có "Làm thử") ·
`example` ("Ví dụ … từng phép tính", 5 phép tính đánh số ①–⑤, dùng lại kết quả phép trước) · `check` ("Tự kiểm bằng đường khác") ·
`pitfall` (3 lỗi, ≥ 1 lỗi "người đã đi làm") · `quiz` ("Đến lượt bạn", 3 câu, câu 3 là **quyết định có đánh đổi**, step đề có `pause=25`, đáp án từng bước) ·
`recap` (chuỗi logic + "Tư duy"). Bài L15 là **bài tình huống chuyên gia** loại "quyết định nghề nghiệp" (`references/case-lessons.md` §1–§2; số minh hoạ ghi rõ).
`lesson("Lxx", "<slug>", "Bài N — <tiêu đề giáo án>", source, objectives, scenes)` với N = số thứ tự bài (L00 → Bài 0). `slug` = phần sau `Lxx_` của `spec_planned`.
`source`: "curriculum/bnx.yaml Lxx; audit/bnx/verify_bnx.py Lxx; <nguồn ngoài: RFC/tài liệu hãng/văn bản pháp luật, có ngày>".

## 2. Mã trên màn hình — chạy NGUYÊN VĂN (cổng `audit/review/screen_code.py`)
- Hiện mã bằng `code(TEXT)` / `code(TEXT, lines=(a, b))`; đầu ra bằng `out(TEXT_OUT)`. **≤ 12 dòng mỗi khung**, dòng ≤ 70 ký tự.
- Văn bản mã là **HẰNG ở đầu `audit/bnx/src/lNN.py`** (ví dụ `GIT_CMDS = """…"""`, `SQL_ORA = """…"""`). Đầu ra hiện trên màn hình phải là đầu ra
  **thật** (chạy rồi dán, cắt bớt bằng "…" nếu dài) — không bịa.
- Máy có: `git` 2.x, Python 3.13 (`.venv`), `openssl` 3.5, JDK 21/22 (`javac`, `java`), Node, Go, Docker. Oracle và SQL Server chạy sẵn trong Docker:
  `audit/bnx/dbrun.py` (`ora(sql)`, `mss(sql, db=None)`; banner thật: "Oracle AI Database 26ai Free Release 23.26.3.0.0", "Microsoft SQL Server 2022 (RTM-CU27-GDR)").
  Mỗi bài dùng schema/bảng riêng có tiền tố `bnx_lNN_` và tự `DROP`/`CREATE` để chạy lại được. Không chạm container khác.
- Sổ: viết `audit/bnx/screen/lNN.yaml` dạng `blocks: {"BNX Lxx <scene_id> <step> <khối>": mục}` (xem docstring đầu `audit/review/screen_code.py`
  và mẫu `audit/review/screen_code/WEB.yaml`). Khoá và `sha` lấy bằng `python -B audit/review/screen_code.py stub --course BNX` sau khi gen. Kind:
  `run` với `lang: python|bash|java|sqlite|node|go|oracle|mssql` (mới: oracle/mssql chạy qua Docker) + `expect_stdout` hoặc `post`;
  `output` với `of:`; `other` (YAML/Dockerfile/.proto/cấu hình) với `read_check` nói rõ đã kiểm điều gì bằng cách nào (yaml/json được phân tích thật).
  Người điều phối gộp các tệp này vào `audit/review/screen_code/BNX.yaml` — **bạn không sửa tệp sổ chung**.

## 3. Số liệu và kiểm
- `checks:` của cảnh là biểu thức Python trả `True`, gọi hàm của bạn ở **`tools/checklib_bnx/lNN.py`** (tên bắt đầu `bnx_`, chỉ thư viện chuẩn,
  không mạng, không Docker), qua `alg.bnx_…`. Mọi con số trên màn hình có `checks`. Lint cảnh báo check so hai hằng (E26) và check hai vế giống nhau (E35).
- **Bộ kiểm độc lập** `audit/bnx/ver/lNN.py`, hàm `run(rec)`: tính lại mọi khẳng định bằng **đường khác** (vòng lặp thuần, mô phỏng khác, chạy thật
  git/openssl/Oracle/SQL Server), rồi đối chiếu với `alg.bnx_…`. `rec("Lxx", True/False/None, "mô tả")`; `None` = SKIP (thiếu công cụ) và làm cổng FAIL.
  Nhập hằng mã từ `audit/bnx/src/lNN.py` (đường dẫn: `sys.path.insert(0, ROOT/"audit"/"bnx"/"src")`) để chạy đúng chuỗi đang hiện.
- Số minh hoạ (phí, tỉ giá, độ trễ) ghi "(số minh hoạ)" trên màn hình và trong lời. Không nêu biểu phí/tỉ giá thật của ngân hàng nào. Không nói số liệu nội bộ ACB/OCB.

## 4. Lời đọc (`say`) — luật phát âm
- Câu 4–38 từ, ≤ 170 ký tự; số đọc bằng chữ ("năm trăm nghìn"); không có `$ \ _ ^ { }`; số âm "âm 2". Mỗi bước suy luận nói lý do ("vì", "nên").
- Màn hình và lời nói cùng một điều; câu nói chỗ nào thì `focus` chỉ chỗ đó (lib tự tính khi bảng ≥ 2 phần — kiểm lại bằng lint).
- **Từ tiếng Anh trong lời**: chỉ dùng từ đã có luật đọc trong `tools/registry/lexicon_vi.BNX.yaml` (Java, Spring, Oracle, Kafka, Redis, Docker,
  Kubernetes, API, HTTP, SQL, PL/SQL, OpenAPI, Swagger, mTLS, Token, Gateway, PostgreSQL, HMAC, JVM…) và danh sách dò được ở mục 6 dưới đây.
  Từ khác: nói bằng tiếng Việt ("cơ sở dữ liệu tài liệu", "mã truy cập", "hàng đợi thông điệp"), tên gốc chỉ hiện trên màn hình.
  `lib.fix_say` tự đổi "commit" → "chốt", "rollback" → "hoàn tác", "topic" → "chủ đề", "id" → "mã" — viết lời cho hợp với các thay đổi đó.
- Không nhắc "tài liệu", "slide", "dòng N" (E29). Nhắc bài trước thì nói lại nội dung; bài sau chỉ ở hook/recap với `forward_ref=True`.

## 5. Cổng cho mỗi bài (chạy theo thứ tự, phải sạch)
```
cd /d/research-video
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/bnx/gen.py Lxx                       # ghi lessons/bnx/Lxx_<slug>.yaml
PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py lint lessons/bnx/Lxx_*.yaml       # 0 FAIL, 0 WARN (WARN nào giữ lại phải giải thích)
PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py render lessons/bnx/Lxx_*.yaml     # 0 vấn đề bố cục
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/bnx/verify_bnx.py Lxx                # mọi dòng PASS, không SKIP
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/screen_code.py check --course BNX   # các khối của bài bạn PASS (bài khác có thể MISSING)
```
Cổng screen_code đọc sổ chung; để thử trước khi người điều phối gộp, chạy: `python -B audit/bnx/screen_try.py Lxx` (gộp tạm sổ của bạn vào bản sao rồi kiểm).
Mở xem bằng mắt ít nhất 4 khung PNG trong `out/BNX/Lxx/frames/` (hình SVG, khối mã, bảng đáp án, khung cuối). **Không chạy `build`, `tts`, `asr`.**
Sửa trong `src/lNN.py` rồi chạy lại — **không sửa YAML bằng tay**; sửa tệp bằng công cụ Edit/Write (chuỗi có `\` đi qua bash dễ hỏng).

## 6. Từ ngoại đã dò phát âm (audit/bnx/probes/x1.md)
Dò xong 2026-11-11 (GPU, small + medium, 4 ngữ cảnh, ngưỡng 7/8; đối chứng âm 12/12 đều 0/8):
- **ĐƯỢC đọc trong lời** (đã thêm luật vào `lexicon_vi.BNX.yaml`): **JSON** (đọc «Giây-sơn», 8/8), **YAML** (đọc «Giam-mồ», 8/8). Viết nguyên "JSON", "YAML" trong `say`.
- **KHÔNG đạt** → không viết trong lời, chỉ hiện trên màn hình; lời nói tiếng Việt: Git 4/8, GitLab 5/8, JWT 0/8, OAuth 3/8, gRPC 3/8,
  Elasticsearch 3/8, Couchbase 5/8, RabbitMQ 3/8, SWIFT 3/8, TLS 4/8 (TLS: nói "mã hoá đường truyền"; mTLS đã có luật cũ "M T L S").

## 7. Trả lại cho người điều phối
Một báo cáo ngắn: tệp đã tạo; kết quả 5 cổng (dán dòng tổng); các khung đã xem; điều KHÔNG kiểm được (NOT_VERIFIED) và vì sao;
mọi nguồn mới đã thêm vào `sources.md`. Không sửa tệp ngoài: `audit/bnx/src/lNN.py`, `audit/bnx/ver/lNN.py`, `audit/bnx/screen/lNN.yaml`,
`tools/checklib_bnx/lNN.py`, `lessons/bnx/Lxx_*.yaml` (do gen sinh), một dòng mới cuối `audit/bnx/sources.md`, và `out/BNX/Lxx/` (do render sinh).

## 8. Môi trường (dựng lại container từ đầu)
Cổng `audit/review/screen_code.py` và `audit/bnx/verify_bnx.py` (L06, L07, L10, L13) cần Docker với ba ảnh dưới đây. **Chỉ dùng trên máy này, mật khẩu là của container tạm, không dùng ở nơi khác.**
Ảnh đã dùng (mã băm đọc bằng `docker image inspect`, 2026-11-11; thẻ `:latest` của SQL Server đổi được nên ghim băm khi cần tái lập):
- `gvenzl/oracle-free:23-slim` = `gvenzl/oracle-free@sha256:6d61d267a3b978c24c5ac1790e62e927416a0aec446bd86e4b3a1527562757bd` (banner thật: Oracle AI Database 26ai Free 23.26.3.0.0)
- `mcr.microsoft.com/mssql/server:2022-latest` = `…@sha256:11927f5edc5122658e90b3a80ee36e8aef779310bf771415c1d89271859c73fd` (SQL Server 2022 RTM-CU27-GDR 16.0.4315.2)
- `apache/kafka:3.9.0` = `…@sha256:fbc7d7c428e3755cf36518d4976596002477e4c052d1f80b5b9eafd06d0fff2f` (L10 tự dựng và tự gỡ container `bnx-kafka`)

```
docker run -d --name bnx-ora -e ORACLE_PASSWORD=Bnx_Pass_2026 -e APP_USER=bnx -e APP_USER_PASSWORD=bnx_pass -p 1521:1521 gvenzl/oracle-free:23-slim
docker run -d --name bnx-mss -e ACCEPT_EULA=Y -e "MSSQL_SA_PASSWORD=Bnx_Pass_2026!" -e MSSQL_PID=Developer -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest
# Oracle cần ~1 phút tới "DATABASE IS READY TO USE!". Cấp quyền hàng đợi cho L07 (bằng SYSTEM):
docker exec -i bnx-ora sqlplus -s system/Bnx_Pass_2026@//localhost/FREEPDB1   # rồi gõ:
#   GRANT AQ_ADMINISTRATOR_ROLE TO bnx; GRANT AQ_USER_ROLE TO bnx; GRANT EXECUTE ON DBMS_AQ TO bnx; GRANT EXECUTE ON DBMS_AQADM TO bnx;
.venv/Scripts/python -B audit/bnx/dbrun.py          # in (True, True) khi cả hai sẵn sàng
```
Máy tắt hoặc Docker khởi động lại: `docker start bnx-ora bnx-mss` là đủ (dữ liệu nằm trong container).
**Phải làm lại khi dựng container MỚI** (không chỉ khởi động lại):
1. Tên máy chủ của container SQL Server nằm trong `expect_stdout` của các khối `mssql` (hiện `461d1255632f`, ghi ở `note` từng khối trong `audit/bnx/screen/l06.yaml`): sinh lại các mục đó rồi `python -B audit/bnx/screen_try.py --merge`.
2. Chạy lại `verify_bnx.py` và `screen_code.py check --course BNX`; thiếu container thì cổng FAIL có nhãn NOT_VERIFIED, không PASS lặng lẽ.
3. Không dùng Docker Desktop khác phiên bản mà không chạy lại: kế hoạch thực thi Oracle (`PARTITION RANGE SINGLE/ALL/ITERATOR`) và thông báo lỗi là đầu ra nguyên văn hiện trên màn hình.
