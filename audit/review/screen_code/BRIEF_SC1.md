# BRIEF_SC1 — Điền sổ "mã trên màn hình" và sửa khối mã sai (2026-11-10)

## Bối cảnh
Người học **mất gốc**, chỉ có video. Họ sẽ gõ lại đúng mã thấy trên màn hình. Nếu mã đó sai cú pháp, thiếu hàm, hoặc chạy ra khác điều bài nói, đó là lỗi **MUST**.

Lỗi thật đã gặp:
- SDP L02: lớp trên màn hình thiếu `nap`, trong khi bảng và quiz dùng "nạp 50".
- SDP L04, L05: `class X:   def …` viết trên một dòng.
- JVA L00, L11: thông báo javac trên màn hình khác thông báo javac in thật.

Các lỗi này lọt được vì `checks:` gọi hàm trong `tools/checklib.py`, không chạy đúng đoạn mã đang hiện.

Công cụ: `audit/review/screen_code.py`. **Đọc docstring đầu tệp trước tiên**: nó định nghĩa mọi `kind` và trường.
Ví dụ mẫu đã PASS: `audit/review/screen_code/SDP.yaml` (3 mục) và `audit/review/screen_code/JVA.yaml` (máy sinh).
Lệnh (luôn đặt `PYTHONIOENCODING=utf-8`, chạy từ `D:\research-video`, dùng `.venv/Scripts/python -B`):
- `audit/review/screen_code.py stub --course X`: in mục mẫu cho khối chưa vào sổ, có sẵn khoá và sha.
- `audit/review/screen_code.py show "X Lxx scene step khối"`: in đúng văn bản khối mà cổng thấy.
- `audit/review/screen_code.py check --course X -v`: chạy cổng. Mục tiêu: FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0.

## Việc của bạn, với từng khối của các khoá được giao
1. Đọc khối **trong ngữ cảnh**: cả cảnh, lời đọc `say`, bảng hoặc kết quả ở bước kề, quiz, chú thích `#`/`//`/`--` trong khối.
   Ghi mọi điều bài nói về kết quả của khối vào `claims:`, trích nguyên chữ hoặc gần nguyên chữ, kèm vị trí.
2. Chọn `kind` theo **thứ tự ưu tiên**. Chỉ được xuống bậc dưới khi bậc trên **thật sự** không làm được, và phải ghi lý do.
   1. **run**: chạy nguyên văn bằng python / sqlite / node / java / bash / go. Mỗi điều trong `claims` phải thành một khẳng định trong `post` hoặc `expect_stdout` / `expect_*`.
      - Mã bài đã hiện ở khối khác: dùng `prelude_keys` (văn bản đã ghim), **không chép tay**.
      - Dữ liệu bài nói ra nhưng không hiện thành mã (ví dụ một bảng 4 sinh viên): dùng `prelude` kèm `prelude_reason` trích chỗ bài nói.
      - Chương trình đầy đủ mà màn hình chỉ hiện từng đoạn: khai một `sources:` (xem gen-jva và docstring). Các đoạn để `fragment` + `within: src:<KHOÁ>:<tên>`.
      - **Cấm** dùng prelude để che lỗi, ví dụ tự định nghĩa hàm `nap` mà bài không có, hay tự sửa một dòng sai. Nếu phải thêm điều bài không hề nói thì khối đó **sai**: sửa bài.
   2. **syntax**: mã đúng ngôn ngữ nhưng cần môi trường ngoài (thư viện mạng, phần cứng, Spring…), hoặc là C. Máy **không có trình biên dịch C**; `lang: c` dùng pycparser C99 với `c_wrap` / `c_typedefs` (ví dụ `typedef signed char int8_t;`). Điều bài nói về kết quả của mã C:
      - kiểm bằng một `sources:` Python dịch **sát từng dòng**, ghi `twin_of: <khoá khối C>` và `reason`;
      - **và** ghi điều đó vào `unverified_claims:` của khối C, kèm câu "kiểm bằng bản Python đối chiếu; độ trung thực bản dịch = INFERRED".
   3. **fragment**: đoạn trích. Nếu đoạn thuộc một khối hoặc nguồn chạy được thì **bắt buộc** `within`.
   4. **output**: khối là kết quả in ra hoặc thông báo lỗi. Nếu có khối hoặc nguồn sinh ra nó thì **bắt buộc** `of`.
   5. **pseudo**: chỉ khi khối có chữ tiếng Việt hoặc ký hiệu toán, không phải mã của một ngôn ngữ thật. Cổng WARN nếu khối khai pseudo mà lại là Python hợp lệ; WARN phải về 0.
   6. **other**: định dạng hoặc ngôn ngữ không có trình kiểm (Dockerfile, PL/SQL, ksqlDB, T24 OFS, HTTP, cấu hình, hợp ngữ…). Bắt buộc `read_check` ghi bạn đã đọc kiểm điều gì, theo nguồn có thẩm quyền nào (tài liệu chính thức có phiên bản, hoặc "truy cập 2026-11-10, no revision given"). Mọi điều bài nói mà máy không kiểm được → `unverified_claims:`.
3. Chạy `check --course X -v` sau mỗi bài.

## Khi khối SAI (cổng FAIL vì mã hoặc vì điều bài nói, không phải vì sổ của bạn sai)
- Phân loại:
  - **MUST**: mã không chạy/không biên dịch; chạy ra khác điều bài nói; thiếu thứ bài dùng; thông báo lỗi trên màn hình khác máy in.
  - **SHOULD**: chú thích lệch nhỏ, tên lạ không được giảng.
- **Sửa bài** theo đúng mục C của `audit/review/FULL_REVIEW_BRIEF_C.md` (đọc mục đó):
  - sửa bằng công cụ Edit;
  - `focus` khớp số câu;
  - `say` khớp màn hình;
  - thêm `checks:` cho số mới;
  - bài sinh từ mã (BNK: `audit/bnk/src/lNN.py` + `gen.py`; khoá có `audit/<khoá>/src/*.tpl.yaml` → `sync_tpl_from_lesson.py <KHOÁ> --write`);
  - INT/ACB sửa thẳng `lessons/`;
  - `lv.py lint` → 0 FAIL 0 WARN; `lv.py render` → 0 vấn đề;
  - bộ kiểm khoá (`audit/<khoá>/verify_<khoá>.py`) 0 FAIL;
  - `scan_ctrl.py` không lượt mới;
  - mục giáo án `curriculum/<khoá>.yaml` vẫn khớp.
- Sửa bài làm đổi văn bản khối thì sha đổi → cập nhật `sha` trong sổ **sau khi** kiểm lại.
- **Không chạy** `build`, `tts`, `asr`. Người điều phối dựng lại.
- Không sửa `audit/review/screen_code.py`, `tools/lv.py`, `tools/checklib.py` (trừ thêm hàm mới có tiền tố khoá bằng một Edit nhỏ), `audit/dms/asr_review_dms.py`, `audit/verify_plan_curricula.py`. Cần tính năng mới của cổng → ghi vào báo cáo, đừng tự sửa.
- Chỉ chạm tệp của khoá được giao: `lessons/<khoá>/`, `audit/<khoá>/`, `curriculum/<khoá>.yaml`, `audit/review/screen_code/<KHOÁ>.yaml`. Không chạy lệnh git đổi index.
- Tệp tạm: chỉ trong thư mục scratchpad được giao.

## Báo cáo `audit/review/screen_code/report_<NHÓM>.md`
1. Dòng đầu: `# SC1 nhóm <N> — <khoá…>: K khối`.
2. Bảng số theo khoá: `| Khoá | khối | run | syntax | fragment | output | pseudo | other | unverified_claims |`.
3. Bảng lỗi đã sửa, mỗi dòng một lỗi: `| Khối | Mức | Trích nguyên chữ (cũ) | Vì sao sai + bằng chứng (lệnh đã chạy, kết quả) | Sửa thành | lint/render/verify |`.
4. Danh sách `unverified_claims`, gom theo khoá, nói vì sao máy không kiểm được.
5. Dòng cuối của `check --course X` cho từng khoá, dòng cuối của bộ kiểm khoá, và danh sách bài đã đổi (để dựng lại).

Trả lời người điều phối ≤ 250 từ: số khối theo kind, số lỗi MUST/SHOULD đã sửa, bài cần dựng lại, đề xuất cho cổng (nếu có).
