# BRIEF_JVA — nâng 13 bài JVA lên chuẩn AF2 (L00–L12) — 2026-11-13

Đọc trước: `BRIEF_AF2.md` (chuẩn, BẮT BUỘC), `audit/jva/BRIEF.md`, `audit/jva/lib.py`, bài mẫu đã nâng **`audit/jva/src/l04.py`** (cảnh `practice`, lab, `covers`) và `audit/labkit.py`, `labs/ENV.md`, `audit/review/sample_f/REPORT.md` mục 4 (khoảng hở của khoá này).

Bối cảnh: khoá FND (mới, đứng TRƯỚC JVA) dạy Git Bash, đường dẫn, tệp, PATH, trình soạn mã và cài JDK. JVA dùng lại các kỹ năng đó nhưng **bài phải tự đủ**: nhắc lại ngắn tại chỗ (một câu), không viết "như đã học ở khoá FND". Đích: sau 13 bài, người học TỰ viết và chạy được chương trình Java nhỏ, đọc được thông báo lỗi, và có nền cho BNK (Spring, SQL, luồng).

## Việc phải làm với mỗi bài L00…L12
1. Thêm cảnh `practice` + thư mục lab + `af2: true` + `covers` (theo l04.py). Lab là chương trình/biến thể **khác số của ví dụ trong bài**; lời giải là `prog(...)` (bộ kiểm `verify_jva.py` chạy thật) và `write_lab("JVA", "Lxx", …)`. Lab có bước tăng dần (đề 1 việc cụ thể, kết quả in ra kiểm được).
2. Sửa lỗi đã đo (mục "SHOULD khác" của sample_f/REPORT.md mục 4):
   - **L00**: dùng **Git Bash** (không Command Prompt/PowerShell) và nhắc `cd` tới thư mục chứa tệp; giảng đủ hoặc không nhắc những chữ bài dùng ngay từ đầu mà trước đây hứa "các bài sau sẽ giải thích": `String[] args`, `System.out`, `//` (lời hứa phải được giữ ở bài nào đó của khoá; ghi vào `covers`/ghi chú ở bài đó). Thêm một cảnh đọc thông báo lỗi biên dịch thật (sai chính tả, thiếu `;`): dòng, cột, gợi ý.
   - **L01–L02**: thêm cách chạy từng đoạn nhỏ, tự đoán rồi kiểm (P4).
   - **L05–L06**: nhắc rõ `import` và `static` ở lần đầu; mảng/hàm có bài tập tự viết.
   - **L07**: thuật ngữ cố định **"hàm tạo"**, **"từ khoá `this`"**; thống nhất với các bài sau.
   - **L09**: giảng `<…>` (kiểu tổng quát) bằng một câu tại chỗ; `HashMap` thêm một ví dụ tra cứu.
   - **L10**: thuật ngữ cố định "nhãn (annotation)" khi nhắc `@Override` ở L11; sửa hook `new TaiKhoan(100000)` cho khớp hàm tạo của L07 (hoặc đổi lớp trong hook).
   - **L11**: giải thích annotation `@Override` là "nhãn đặt trước phương thức để trình biên dịch kiểm giúp"; nêu sơ lược các nhãn khác sẽ gặp (không dạy chi tiết).
   - **L12**: bài tình huống: người học TỰ xây dần sổ chuyển khoản qua 3 mốc (lab có bước), hiện đủ mã (tệp hoàn chỉnh), kèm phần "khi số giao dịch lớn gấp 1000 lần" (P9: danh sách vs bản đồ, độ phức tạp, vì sao cần cơ sở dữ liệu — số tính được).
3. **Khoảng hở nền cho BNK** (đặt vào đúng bài, tự đủ): L03/L04 nhập dữ liệu `args` và `Scanner` (đọc từ bàn phím/tệp); L08 đọc ghi tệp văn bản UTF-8 (`Files.readAllLines/writeString`) và dòng `new String[]`; L09 giới thiệu lambda một dòng (`list.forEach(x -> …)`) và `sort` bằng `Comparator` ở mức đọc hiểu; L10 giới thiệu luồng như "một dãy việc chạy cùng lúc" (hình + ví dụ `Thread` hai luồng in xen kẽ, KHÔNG dạy khoá/`synchronized` ở đây) — chỉ khi vẫn giữ mỗi bài ≤ 16 phút video; nếu nặng quá thì ghi vào `audit/review/audit_final/reports/jva_gaps.md` các mục chưa nhét được (người điều phối sẽ đưa vào khoá JV2).
4. P1/P2/P3/P5/P6/P9 theo BRIEF_AF2. Bài nào mỏng (< 9 phút) thì nới theo luật 22–24 của pedagogy.md.

## Cổng cho mỗi bài
`verify_jva.py Lxx` → `gen.py Lxx` → `lv.py lint` (0 FAIL, 0 WARN) → `lv.py render` (0 vấn đề) → `lab_gate.py JVA` → mở 3 khung PNG. KHÔNG chạy `build`/`tts`/`asr`. JDK trên máy: 21.0.13 (mọi chương trình phải biên dịch được bằng Java 21; không dùng tính năng xem trước).
Làm lần lượt L00→L12; báo cáo `audit/review/audit_final/reports/jva.md` (bài nào xong, cổng nào PASS, số phút video ước tính theo lời đọc, mục chưa nhét được).
