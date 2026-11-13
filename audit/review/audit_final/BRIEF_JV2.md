# BRIEF_JV2 — soạn khoá JV2 "Java trung cấp: dự án nhiều tệp, dữ liệu, hàm, luồng, kiểm thử" (10–11 bài) — 2026-11-13

Đọc trước (BẮT BUỘC, theo thứ tự): `BRIEF_AF2.md`, `new_courses.md` (mục JV2), `labs/ENV.md`, `audit/jva/BRIEF.md`, `audit/jva/lib.py`, `gen.py`, `src/l04.py` (mẫu AF2), `audit/labkit.py`, `audit/review/sample_f/REPORT.md` mục 4 (khoảng hở của người học sau JVA), `curriculum/bnk.yaml` (JV2 phải nạp đủ nền cho BNK L00–L04 và L07), `.claude/skills/lecture-video/SKILL.md`.

Vị trí trong lộ trình: FND → JVA → **JV2** → BNK. Người học đã biết: dòng lệnh Git Bash, tệp/thư mục, JSON/SQL cơ bản (FND), và Java căn bản (JVA: biến, rẽ nhánh, vòng lặp, mảng, hàm, lớp, chuỗi, danh sách/bản đồ, ngoại lệ, giao diện/record/enum, tự viết được chương trình vài chục dòng). Chưa biết: dự án nhiều tệp, nhập dữ liệu/tệp, generics, lambda/stream, annotation, luồng, kiểm thử, gỡ lỗi. BNK sẽ DÙNG ngay: annotation/Spring, giao dịch, luồng, khoá.

## Bảng bài (có thể chỉnh nếu có lý do, ghi vào báo cáo)
| Bài | Nội dung | Lab |
|---|---|---|
| L00 | Dự án nhiều tệp: `package`, `import`, cây thư mục nguồn, `javac -d`, `java -cp`, tệp `.jar`; lớp truy cập (`public`, `private`, mặc định) | dựng dự án 3 tệp, chạy từ jar |
| L01 | Nhập dữ liệu: `args`, `Scanner(System.in)`, đọc/ghi tệp văn bản UTF-8 bằng `Files`, đường dẫn, `try`-với-tài-nguyên | đọc CSV giao dịch, in tổng theo loại |
| L02 | Kiểu tổng quát (generics): `List<T>`, `Map<K,V>`, `Set`, viết hộp `Hop<T>`, `Comparable`, `Comparator` | sắp xếp danh sách giao dịch theo hai khoá |
| L03 | Hàm là giá trị: lambda, giao diện hàm (`Function`, `Predicate`), tham chiếu hàm, Stream (`filter map collect groupingBy sum`) | thống kê bằng Stream so với vòng lặp |
| L04 | Annotation và phản chiếu: `@Override`, tự định nghĩa annotation, đọc bằng `Class.getDeclaredMethods`; mini "tiêm phụ thuộc" 30 dòng — đây là nền để hiểu Spring | mini-DI chạy được |
| L05 | Luồng: `Thread`, race (hai luồng cộng dồn sai), `synchronized`, `ExecutorService`, `Future`, `ConcurrentHashMap` | đo race, sửa đúng |
| L06 | Kiểm thử đơn vị: tự viết khẳng định, rồi JUnit 5 console (`junit-platform-console-standalone` jar có sha256 trong `labs/ENV.md`) hoặc chỉ khẳng định tự viết nếu không tải được; kiểm thử biên, ngoại lệ | viết 5 ca kiểm cho `phiChuyenKhoan` |
| L07 | Gỡ lỗi: đọc dấu vết ngăn xếp nhiều tầng, in nhật ký (`System.Logger`/`java.util.logging`), chia đôi để khoanh vùng, `jdb` cơ bản (hoặc debugger IDE ở mức khái niệm) | tìm lỗi trong chương trình cho sẵn |
| L08 | Thời gian và tiền: `java.time` (múi giờ, `Instant`, `Duration`), `BigDecimal` làm tròn, `Locale` | tính lãi theo ngày đúng |
| L09 | Dự án tình huống: sổ cái CSV → báo cáo (nhiều tệp, Stream, kiểm thử, nhật ký) + "khi dữ liệu lớn gấp 1000 lần" (bộ nhớ, đọc theo dòng, luồng song song) | dự án nhỏ có đáp số |

**Không dùng** Maven/Gradle/JDBC (máy kiểm chưa có `mvn`; `sqlite-jdbc` không có sẵn): nếu một bài buộc phải dùng jar ngoài thì ghi tên, phiên bản, URL chính thức và `sha256` vào cuối `labs/ENV.md` (bảng "Tệp tải thêm"), tải về `audit/jv2/deps/` (ghi trong `.gitignore` đã có quy ước cho `*.jar`) và để bộ kiểm báo `NOT_VERIFIED` rõ ràng nếu thiếu jar.

## Việc phải làm
1. Khoá mới `JV2` (`tools/lv.py new-course JV2 --title "Java trung cấp"`, `references/new-domain.md`), bộ sinh `audit/jv2/` sao theo `audit/jva/` (lib.py: COURSE="JV2"), `src/l00.py … l09.py`, `verify_jv2.py` (biên dịch + chạy THẬT; chương trình nhiều tệp: mở rộng `prog` thành `project(name, files={…}, run="…", out=…)` chạy trong thư mục tạm), lab theo `labkit`.
2. Mỗi bài theo BRIEF_AF2 (10 cảnh + practice, `af2: true`, `covers`, lab, hình cơ chế, P9 quy mô: ví dụ bộ nhớ khi N tăng ×1000, số luồng, v.v.).
3. Lời đọc tiếng Việt, không từ khoá tiếng Anh của Java (gen từ chối); tên lớp/hàm đọc được (`TaiKhoan`, `PhiChuyen…`). Dò ASR tên riêng; không đạt thì chỉ hiện trên màn hình.
4. `curriculum/jv2.yaml` viết SAU CÙNG (khi mọi bài qua cổng). Không sửa `pack.py`/`tracks.yaml`/`STAGES`, bài của khoá khác, `tools/`.

## Cổng cho mỗi bài
`verify_jv2.py Lxx` → `gen.py Lxx` → `tools/lv.py lint lessons/jv2/Lxx_*.yaml` (0 FAIL 0 WARN) → `tools/lv.py render …` (0 vấn đề) → `audit/review/lab_gate.py JV2` → xem 3 khung PNG. KHÔNG chạy `build`/`tts`/`asr`. Báo cáo `audit/review/audit_final/reports/jv2.md`.
