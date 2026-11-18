# fix_S01_JV2 — sửa khoá JV2 (L00–L09) theo `reports/S01_JV2.md` — 2026-11-13

Nguồn sửa: `audit/jv2/src/l00..l09.py`, `audit/jv2/lib.py`; sinh lại `lessons/jv2/*.yaml` bằng `gen.py`. Không chạy build/tts/asr/audit_all/git/docker.
Sổ/giáo án chạm tới: `curriculum/jv2.yaml` (mục tiêu 3 của L04), `tools/registry/symbols.JV2.yaml` (10 thuật ngữ E52), `audit/review/screen_code/JV2.yaml` (sinh lại bằng `gen-jv2`).

## 1. MUST (2/2 đã xử lý)

| # | Kiểm lại bằng cách chạy thật | Kết luận | Sửa |
|---|---|---|---|
| L04 step 18 `javap | grep` | JDK 21.0.13: mẫu `^    MiniDi` (4 dấu cách) đã ra ĐỦ 4 dòng (bài đã ghi 4 dấu cách, báo cáo đọc thành 1 dấu cách vì khoảng trắng bị gộp); mẫu 1 dấu cách `^ MiniDi` ra 2 dòng đúng như báo cáo. Báo cáo ĐÚNG MỘT PHẦN. Nhưng số dấu cách vô hình trên màn hình khiến người học gõ sai. | Đổi lệnh thành `grep -E '^Runtime|^ {4}MiniDi'` (số lần ghi tường minh), chạy thật trong `verify_jv2` (project KiemNhan): ra đúng 4 dòng. Thêm ghi chú trên khung giải thích `javap -v -p` và mẫu `{4}`. |
| L08 hook: tiêu đề "Ba triệu… một triệu rưỡi" | Đúng (hình/lời: 1 000 000 giao dịch, lệch 500 000) | Tiêu đề cảnh thành "Một triệu giao dịch nửa đồng: cuối ngày lệch năm trăm nghìn đồng" (khung 00002 đã xem). `chapters.txt` sẽ tự đổi khi dựng lại. |

## 2. SHOULD (27 dòng trong bảng báo cáo, ghi là 24): 27 sửa, 0 bỏ

L00: `sort` dưới locale (dùng `LC_ALL=C sort`, chạy thật); `protected` (một câu + chú thích). L01: bỏ lời hứa "chuẩn mã hoá" (không dạy); hiện mã in có thứ tự (mảng cố định) và nói rõ HashMap in `[rut, chuyen, nap]` (prog `ThuTuBang` chạy thật); hiện `TaoFile`/`DocHet`/`TongDong` đầy đủ. L02: hiện 3 lời gọi `lon` và cách ra `-11 0 4` (từng cặp); hiện lớp `Hop` kiểu Object ở hook. L03: "bài trước" → "bài một" (2 chỗ); hiện `Files.lines` + khối có tài nguyên (ThongKeLon, DocHet, TaoFile); thêm step "ngoại lệ có trạng thái" (`sorted`, `distinct`) và sửa tiêu đề hình/recap. L04: quiz thứ tự `getDeclaredFields` (nêu giả thiết + đáp án nếu đảo thứ tự); nửa `@Transactional` (step đối tượng đại diện/AOP; hook và mục tiêu 3 "cùng ý tưởng nền" thay "cùng cơ chế", đồng bộ `curriculum/jv2.yaml`); lỗi vòng: tách lớp thứ ba trước, Spring Boot 2.6 cấm vòng mặc định, nên tiêm qua hàm tạo (PLAUSIBLE, không có mạng để kiểm, đã ghi vào `source`); nhãn hình bị che (dời mũi tên). L05: "sáu cách" → bảng đủ 6 thứ tự (2 nối đuôi, 4 xen kẽ); "luôn nhỏ hơn" → "thường nhỏ hơn" + lưu ý chạy JVM mới (đo lại 29/30 lần ra đúng 2 000 000 khi lặp trong cùng JVM); nhãn hình hook không đè mũi tên; "50 GB" → "dành sẵn". L06: hiện đủ `import static`, `PhiChuyen.java` và 4 ca; sed neo `)` để không đụng biên 10 triệu (chạy thật, 3 đạt/1 hỏng). L07: nhật ký FINE (hiện tạo Logger và Handler, nói rõ hai ngưỡng, ConsoleHandler mặc định INFO); hiện `Loi.java` và `phien.sh` (viết lại nhiều dòng, nói gõ tay được); PCI DSS 3.2.1/4.0 và "tốt nhất không ghi PAN". L08: step đếm ngày hiện đúng 2 lệnh in; HALF_EVEN "với dữ liệu thử chẵn lẻ xen kẽ", đo thêm `ChanHet` (phần nguyên chẵn: lệch −500, chạy thật). L09: step 8/9 thống nhất (bất biến kiểm phần gom, không kiểm dữ liệu đầu vào; không bắt dòng bị loại trước đó); cây "bảy tệp" → mười tệp khớp lệnh chạy; bảng bài 4 sửa. Toàn khoá: mọi `labs/JV2/L01..L09/de.md` có dòng "import cần dùng" (L00 ghi `import shop.kho.Hang;`); L06 `LongSupplier` giải thích ở đề lab và `de.md`.

## 3. Mã hiện đủ để gõ lại
- `lib.code_block`/`pcode` tự kèm ghi chú "Đầu tệp: import …; Khung: class … main …" cho các dòng chưa hiện (một lần mỗi bài, `lib.head_note`); mã bị cắt dở (ví dụ KetCho, SuaKetCho, LoiTrongNhom, ThoiGian, VongTron, DuaTranh) đã sửa dải dòng cho đủ. Mọi chương trình dự án L09 (GiaoDich, DocSoCai, NhatKy, BaoCao, TongHop, App, AppDong, AppSong, KiemTra, ThuTieuDe, TaoSoCai) nay có khung hình mã; dòng quá rộng (> ~100 cột) đã ngắt trong nguồn.
- Công cụ phủ mã: `jv2fix_cover.py` (scratchpad) liệt kê dòng thân chưa hiện: còn lại chỉ mã lab (lời giải ở `labs/`), một vài khung/trích của L00 (thân ba tệp `bank`, bài dạy về gói/dòng lệnh, không phải điều bài đo), `TuKiemLoi` (cùng mã `TuKiem` đổi hai dấu, hiện đầu ra), thân `NhatKy` L09 (lớp định dạng giống hệt L07, có ghi chú).

## 4. P1 thuật ngữ tại chỗ (dự kiến 10/10 bài đạt, trước 5/10)
L00 `-C out .`, `--main-class`/`META-INF/MANIFEST.MF`, gói mặc định, cmd.exe, dấu ngăn `;`/`:`; L01 `printf … |`, `-Xmx`, `OutOfMemoryError`, thứ tự bản đồ; L02 `Hop` kiểu thô, `Random(42)`; L03 `Files.lines`, `Runnable`, effectively final, `findFirst`/`OptionalInt`, `peek`; L04 `Class<?>`, `javap`, `Field`/`Method`/`Constructor`, proxy/AOP; L05 `CyclicBarrier`, `Runnable` (nhắc ở prereq), `findDeadlockedThreads`, luồng nhẹ (virtual thread); L06 `LongSupplier`, `kiem() { }`, `$J`, `sed -i`, `sha256sum`, `cut`; L07 Logger/Handler, `extends Formatter`, `Supplier`, `tr -d '\r'`, PAN, kịch bản jdb; L08 `ZonedDateTime.of(…)` bốn số 0, `divide` ném lỗi, quy ước 365; L09 `parallel()`, `OutOfMemoryError`, bộ gom.
E52: 10 mục `jv2_*` trong `tools/registry/symbols.JV2.yaml` (protected, gói mặc định, effectively final, javap, `Class<?>`, hàng rào, công cụ bế tắc, Handler, Supplier, PAN); `introduces` gán ở cuối `build()` của L00/L03/L04/L05/L07; L09 `assumes: [jv2_handler]`.

## 5. Cổng (số thật, 2026-11-13)
- `verify_jv2`: 88/88 PASS (có thêm 3 prog kiểm chứng: ThuTuBang, ChanHet, ChiaKhongHet). Hai phép đo vốn phụ thuộc thời gian (`DuaTranh` ra `false` một lần, `ThoiGian` ra `false` một lần khi máy đang tải) đã gặp; đã nới dung sai `ThoiGian` (`ms < lyThuyet*3 + 500`, hiện trên màn hình) và chạy lại 10/10; `DuaTranh` vẫn mang tính xác suất (đã ghi trong bài). Người điều phối nên chạy lại verify khi máy rảnh.
- `lv.py lint` 10/10 bài: 0 FAIL, 0 WARN. `lv.py render` 10/10 bài: 0 vấn đề.
- `lab_gate JV2`: 10 PASS · 0 FAIL. `lv.py curriculum curriculum/jv2.yaml`: 10 bài, 0 lỗi. `check_curricula_graph`: 0 hỏng/0 chu trình. `check_xref`: 0. `check_meta`: 13 vấn đề, tất cả của PYT (không thuộc JV2). `check_course_refs`, `check_next_refs`, `arith_scan`, `tests/test_e52.py`: xem mục 7. `screen_code check --course JV2`: xem mục 7.
- Thời lượng ước lượng (từ/150 phút): L00 14,3 · L01 15,7 · L02 14,0 · L03 15,2 · L04 16,4 · L05 16,1 · L06 14,0 · L07 15,7 · L08 14,3 · L09 16,5. L04 và L09 vượt 16 phút nhẹ (L09 là bài tình huống cuối khoá, ghi nhận); chưa cắt thêm vì bớt lời sẽ mất phần vừa thêm để sửa SHOULD.

## 6. Không sửa / còn mở (lý do cụ thể)
- `Comparator.comparing(...).thenComparing(...)` (L02, cột "chưa nói"): cố ý không thêm; tham chiếu hàm do L03 dạy, nhắc trước sẽ vi phạm P1.
- L00 "dấu phân cách đường dẫn khi nhiều jar": đã thêm một ghi chú; không thêm bài về Maven/Gradle (ngoài phạm vi).
- L07 chỉ java.util.logging: thêm một câu về SLF4J/Logback và xoay vòng tệp (ghi chú), không dạy thêm.
- L08 một quy ước tính ngày: thêm câu về thực tế/360 và 30/360; không tính thêm.
- Chưa nghe âm thanh (không dựng lại); mọi câu `say` mới/đổi là câu TTS mới, người điều phối cần dựng và rà ASR.
- `chapters.txt`/`srt` cũ của L08 còn tiêu đề cũ tới khi dựng lại.

## 7. Kết quả cổng chạy sau cùng
- `screen_code check --course JV2` (sau `gen-jv2`, 249 khối): PASS 347 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 (checked_at 2026-11-13T16:49:50Z).
- `tests/test_e52.py`: 0 FAIL. `check_next_refs`: 551 lời hẹn, 0 lệch. `arith_scan`: 228 phép tính, 0 FAIL. `check_course_refs JV2`: 0 vấn đề (bản chạy toàn kho quá chậm khi máy tải; chạy theo khoá JV2). `verify_jv2 L05` sau khi nới dung sai: 10/10 PASS.
- Các lệnh toàn kho còn treo nền do tôi chạy (`check_course_refs.py` không đối số) có thể còn tiến trình; dừng tay nếu cần.
