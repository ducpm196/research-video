# BRIEF_VERIFY_SC1 — Kiểm độc lập sổ "mã trên màn hình" và các sửa bài (2026-11-10)

Bạn là **người kiểm độc lập, chỉ đọc**. Không sửa tệp nào trong kho. Không chạy build/tts/asr/render, không chạy lệnh git đổi index.
Tệp tạm chỉ được ghi trong thư mục scratchpad được giao.

## Bối cảnh
- `audit/review/screen_code.py` là cổng kiểm. Đọc docstring đầu tệp trước. Nó chạy nguyên văn mọi khối mã người học thấy trong `lessons/**/*.yaml`, theo sổ `audit/review/screen_code/<KHOÁ>.yaml`.
- 4 tác tử đã điền sổ và sửa bài. Tiêu chí của họ ở `BRIEF_SC1.md`; báo cáo của họ là `report_G1.md` … `report_G4.md`.
- **Không tin báo cáo của họ là bằng chứng.** Tự đọc bài, đọc sổ, tự chạy.
- Lệnh (luôn đặt `PYTHONIOENCODING=utf-8`, dùng `.venv/Scripts/python -B`, chạy ở `D:\research-video`):
  - `screen_code.py show "<khoá khối>"`
  - `screen_code.py check --course X -v`

## Bạn kiểm gì (cho MỌI mục sổ của các khoá được giao)
1. **Phân loại trung thực (CB-3)**:
   - Khối là mã thật của một ngôn ngữ chạy được trên máy (Python, SQL/sqlite, JS/node, Java, bash, Go) mà bị khai `pseudo` / `other` / `fragment` không `within` / `syntax` thay vì `run` → báo **NÉ**, kèm lý do vì sao chạy được.
   - `pseudo` phải thật sự có chữ Việt hoặc ký hiệu không thuộc ngôn ngữ nào.
   - `other` phải có `read_check` cụ thể.
2. **Khẳng định đủ và đúng (CB-4)**: đọc cả cảnh quanh khối (`show`, `say`, bảng, quiz, chú thích trong khối) và liệt kê mọi điều bài nói về kết quả của khối. Với từng điều:
   - có trong `claims` không?
   - `post` / `expect_*` có kiểm **đúng** điều đó không (đúng giá trị, đúng số chữ số, không lỏng hơn)?
   - Thiếu → báo **THIẾU**.
   - Khẳng định kiểm sai điều (ví dụ chỉ kiểm chạy không lỗi trong khi bài nói ra con số) → báo **LỎNG**.
3. **prelude / sources không che lỗi**:
   - `prelude` chỉ chứa điều bài thật sự nói. Nếu nó định nghĩa hàm, biến hay lớp mà bài **không** nói hoặc hiện → báo **CHE**.
   - `sources` + `twin_of`: đọc bản dịch có sát từng dòng với khối không; dịch lệch thì báo **TWIN-LỆCH**.
4. **Sửa bài đúng** (danh sách bài đã đổi ở dưới): đọc diff (`git diff -- <tệp>`) và kiểm từng thay đổi:
   - mã mới đúng;
   - `say` khớp màn hình;
   - `focus` trỏ đúng: câu nói về dòng/hàng nào thì focus trỏ đúng chỗ đó. `audit/review/screen_code/focus_code_lines.py <tệp>` giúp liệt kê;
   - `checks` có kiểm số mới;
   - không sinh lỗi kiến thức mới.
   Ghi **SỬA-SAI** nếu có vấn đề.
5. **Lỗi bài còn sót**: khối mà cổng PASS nhưng bạn thấy vẫn sai với người học (ví dụ chú thích ghi kết quả sai mà khẳng định không kiểm) → **MUST/SHOULD** kèm bằng chứng (lệnh đã chạy, kết quả).

Bài đã đổi trong việc này (so với commit HEAD):
- acb L04; cs112 L25; cvi L00; esy L01; gfx L12
- jva L00, L11, L12 (L12 chỉ đổi định dạng `asr_reviewed`)
- plc L11, L12
- sdp L02, L03, L04, L06, L07, L08, L11, L12
- web L04, L06

## Báo cáo
**Không ghi tệp báo cáo** (công cụ chặn). Đưa toàn văn vào câu trả lời cuối, theo định dạng:
1. Dòng đầu: `# Kiểm độc lập SC1 — <các khoá>: đã xét N mục sổ, M bài đổi`.
2. Bảng phát hiện, mỗi dòng một phát hiện: `| Khối/bài | Loại (NÉ/THIẾU/LỎNG/CHE/TWIN-LỆCH/SỬA-SAI/MUST/SHOULD) | Trích nguyên chữ | Bằng chứng (lệnh + kết quả) | Đề xuất | Tin cậy (CONFIRMED/PLAUSIBLE) |`.
3. Số mục đã xét theo khoá, và số mục không có phát hiện.
4. Dòng cuối của `check --course X` do chính bạn chạy, cho từng khoá.
