# S01c JV2: đã đọc 10/10 bài (vòng 3, đọc độc lập, 2026-11-14)

Phạm vi: `lessons/jv2/L00..L09` (đọc trọn `title/objectives/show/say/checks/quiz`), `curriculum/jv2.yaml`, `out/jv2/Lxx/` (`chapters.txt`, `.srt`, `build_report.json`, `frames/`), `labs/JV2/Lxx/` (`de.md`, `mong_doi.txt`, `loi_giai.*`; `labs/jv2` và `labs/JV2` giống hệt nhau). JDK 21.0.13, Git Bash, `labs/cham.sh`. Không mở báo cáo/plan/handover khác. Không có `audit/jv2/sources*.md` nên sự kiện ngoài (8191 ký tự cmd.exe, PCI DSS 6+4/8+4, Spring Boot 2.6 cấm vòng, 1 MB ngăn xếp/luồng, sha256 JUnit) kiểm bằng hiểu biết và tải thật (xem mục 6).

## Kết luận ngưỡng chốt
- **MUST = 0.** SHOULD = 6 (mục 2), không cái nào làm sai kiến thức cốt lõi.
- **P1 = 2: 10/10 bài (100% ≥ 90%)**, kèm ghi chú "vừa đủ" ở L05 và L08 (xem mục 3).
- **P8 = 2: 10/10 bài (100%)**; cả 10 lab tự làm một lần là ĐÚNG.
- Tính tươi của video: `spec_sha256` trong `build_report.json` = `lv.spec_digest` tính lại từ YAML hiện tại: **10/10 khớp** (công thức: sha256 của `json.dumps(yaml bỏ asr_reviewed, sort_keys, ensure_ascii=False)`). mp4 có đủ 1920x1080, âm thanh aac, thời lượng ffprobe = `timeline_seconds` (10/10). Ba YAML có mtime mới hơn mp4 (L02, L04, L09) nhưng digest vẫn khớp nên không STALE (chỉ đổi phần `asr_reviewed`/định dạng).
- `.srt` so với `say`: **10/10 trùng 100% từng từ** (2148, 2356, 2253, 2358, 2458, 2413, 2141, 2397, 2252, 2398 từ; ratio difflib = 1.0, không câu thiếu/thừa/sai số). Lưu ý: `.srt` sinh từ chính văn bản `say` nên đây là bằng chứng "video dựng đúng đặc tả", không phải bằng chứng "giọng đọc đọc đúng"; chưa có tai người (tôi không nghe audio; chỉ kiểm âm lượng đều: mean -21.2..-21.8 dB, max -2.1..-2.7 dB, một giọng NamMinh duy nhất cả 10 bài).

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | — | | | không phát hiện lỗi (9/9 lệnh/đầu ra chạy lại khớp) | | |
| L01 | — | | | không phát hiện lỗi (13/13 khớp, kể cả thứ tự HashMap `rut, chuyen, nap` và OOM 32 MB) | | |
| L02 | — | | | không phát hiện lỗi (9/9 khớp: 8 683 / 1 534 624 / 18 640 873; 999 / 99 999 / 999 999) | | |
| L03 | — | | | không phát hiện lỗi (10/10 khớp) | | |
| L04 | SHOULD | `hook.0` (SAY và SHOW) | "Trong mọi dự án Java ở ngân hàng, bạn sẽ gặp mã như thế này" | Khẳng định tuyệt đối: không phải mọi dự án Java ngân hàng dùng Spring/`@Autowired`. Đọc `L04.srt` câu 2-3 của cảnh hook và khung `out/jv2/L04/frames/00002.png`. | "trong rất nhiều dự án Java doanh nghiệp, kể cả ngân hàng" | CONFIRMED |
| L05 | SHOULD | `hook.1` (SAY và SHOW) | "vì sao nó làm hỏng dữ liệu, và ba cách sửa là khoá, phép nguyên tử và nhóm luồng" | Nhóm luồng (`ExecutorService`) không sửa tranh chấp dữ liệu: ở `example.4-6` nhóm luồng chỉ giao việc, còn chỗ an toàn là `ConcurrentHashMap.merge`. Bài thân (sym, scale, pitfalls, quiz) giảng đúng; chỉ câu giới thiệu sai nhãn. | đổi thành "hai cách sửa (khoá, phép nguyên tử) và công cụ giao việc (nhóm luồng)" | CONFIRMED |
| L05 | SHOULD | `pitfalls.7` (khung 00124) | `System.out.println("xong; tong tien = " + (a.soDu + b.soDu) + ", A = " ...` | Dòng mã dài tràn ra ngoài khung mã khoảng 40 px bên phải (x≈1875 so với mép khung 1833); đọc được, không bị cắt. Quét 1 500 khung bằng PIL (vùng x 1862..1915): chỉ 3 khung vi phạm (xem hàng L02, L09). | ngắt dòng println hoặc giảm cỡ chữ khối mã | CONFIRMED |
| L02 | SHOULD | `scale.4` (khung 00097) | `System.out.println("n=" + n + ": ngau nhien " + a.dem + ... + nlogn);` | Tràn khung mã ~60 px phải (kết thúc x≈1892 sát mép 1920), vẫn đọc được. | ngắt dòng | CONFIRMED |
| L09 | SHOULD | `intuition.13` (khung 00048) | `// gom ngay khi đọc, không giữ danh sách` | Chú thích cuối dòng 3 của khối mã tràn khung (x≈1893), sát mép màn hình. | rút gọn chú thích hoặc xuống dòng | CONFIRMED |
| L07 | SHOULD | `intuition.0` (khung 00026, SAY) | "Khay trên cùng, tức hàm chia, là nơi lỗi xảy ra ... tới khay đáy" | Hình vẽ `chia (dòng số 3) NỔ Ở ĐÂY` nằm ở **đáy** của chồng, `main` ở trên cùng, mũi tên đỏ chỉ lên, còn nhãn viết "dấu vết in từ tầng NỔ xuống tầng main". Lời đọc gọi `chia` là khay **trên cùng** và `main` là khay đáy: hình và lời ngược chiều. Nội dung kiến thức (dòng `at` đầu là nơi nổ) đúng ở cả hai nơi nên tôi xếp SHOULD, không MUST. | đảo hình (main ở đáy, chia ở trên cùng) hoặc sửa lời đọc | CONFIRMED |
| L08 | SHOULD | `quiz.0` câu 2, `quiz.1` | "Nếu làm tròn sau mỗi bước (50 000 000 × 0,048 rồi × 40 rồi / 365) thì có thể khác không?" | Với đúng số của đề, 50 000 000 × 0,048 = 2 400 000 và × 40 = 96 000 000 đều là số nguyên, nên làm tròn từng bước ra **cùng** 263 014; người học tự làm sẽ thấy "không khác" và câu trả lời mẫu "có thể khác" không kiểm chứng được bằng số. (Tôi tính lại bằng Python: 263013,6986 → 263014 ở cả hai cách.) | đổi dữ liệu (ví dụ 4,85%) hoặc thêm một ví dụ có lệch | CONFIRMED |
| L09 | SHOULD | `example.6-7`, `check.0` | `java -cp out soc.App so_cai.csv` / `so_cai_loi.csv` | Hai tệp mẫu không được phát ở đâu (không có trong `labs/JV2/L09`, không in đủ trên màn hình): người học không chạy lại được ví dụ chính; dòng `Theo thang: {...}` không kiểm chứng được. Phần mã thì đủ để dựng lại (tôi dựng lại 10 tệp từ các khung, KiemTra 7/7 DAT, App báo (khop), các phép bộ nhớ 32/64/128 MB khớp). Tổng số dư 10 300 000 và 12 000 000, nạp/rút khớp. | thêm tệp mẫu vào `labs/JV2/L09` hoặc in 8 dòng dữ liệu | CONFIRMED |
| L06 | — | | | không phát hiện lỗi (JUnit tải thật, sha256 `a1de5578...f43f` khớp `labs/ENV.md`; 4/4 rồi 3/1 đúng như video) | | |

Ghi chú SHOULD nhẹ không lập thành hàng: L06 `hook.0` ("mọi bài kiểm bằng mắt đều bỏ sót") là tu từ tuyệt đối; L03 hook.1 "kiểu viết thống trị trong mã Java hiện đại" là tu từ. L05 SVG hook: mũi tên cam gắn nhãn "B ghi 130" trỏ vào dòng "đáng ra phải là 180" nên dễ đọc nhầm.

## 3. Bảng độ sâu

Phút = thời lượng video (mp4); trong ngoặc là phút nói thật (trừ các khoảng `pause` dừng làm bài). P1..P7 theo BRIEF mẫu F; P8, P9 theo ADDENDUM.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1-P7) | Mất gốc | Cần biết trước (dùng, không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8a04707e794d4c10 | 14,3 (11,9) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | cờ `jar tf` (example.5), `mkdir` | mã `TaiKhoan/PhiChuyen/App` chỉ in "đầu tệp", học viên khó dựng lại ví dụ ba tệp; lab thì đủ |
| L01 | 7c9c647669c1798d | 16,4 (13,5) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `trim()`, "đệm" của BufferedReader, `implements AutoCloseable` (chỉ giảng bằng lời "cam kết có hàm đóng") | không có chỗ thiếu đáng kể |
| L02 | 6fa1cb92d67a525e | 15,9 (13,0) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | không (log₂ giảng tại scale.0) | P3: khung 00097 tràn khung mã |
| L03 | 0f2e8833b4c8862f | 16,8 (13,4) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `counting()`, `merge` chỉ xuất hiện ở gợi ý lab | không đáng kể |
| L04 | ec6210afa627d37c | 18,5 (14,0) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `@Service/@Autowired/@Transactional` ở hook (hứa giải thích cuối bài, có giải thích), "bộ thu gom rác" | hook nói "mọi dự án" (SHOULD) |
| L05 | 5067d204c606b5ce | 18,3 (13,8) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "lõi CPU", "ngăn xếp riêng mỗi luồng" ở scale.3 (nhắc lướt, không giảng) | P3: khung 00124 tràn; SVG hook mũi tên/nhãn; hook gọi nhóm luồng là "cách sửa" |
| L06 | 9cbe57fd4a18b8c7 | 16,7 (12,2) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không (sha256sum, curl, sed -i, grep -E đều giải thích trên màn hình) | không đáng kể |
| L07 | 3af21681ef22ba10 | 17,0 (13,6) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "hệ quản lý phiên bản" (git bisect) và SLF4J/Logback chỉ nhắc như ví dụ phụ | P3: hình tháp ngược chiều với lời đọc; lab chỉ "chép rồi sửa một dấu" |
| L08 | 6332078d3793b956 | 16,1 (12,6) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "giờ mùa hè" (cơ chế kim đồng hồ nhảy 1 giờ) chỉ nêu hệ quả 23/25 giờ | quiz câu 2 không có số chứng minh khác biệt (SHOULD) |
| L09 | 773a554726021d8d | 18,8 (13,3) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "giao hoán, kết hợp" (formula.0, được diễn giải bằng hệ quả) | P3: khung 00048 tràn; tệp mẫu `so_cai*.csv` không phát; cảnh intuition 14 bước đọc mã liên tục 2 phút 38 giây |

Trả lời các điểm P1 được dặn kiểm (tất cả đạt, giảng tại chỗ ở lần đầu):
- **log₂**: L02 `scale.0` (bảng nhân đôi 1→2→4→8→16 = 4 lần; 1 024 = 10; 10^6 ≈ 20) cả trên màn hình lẫn lời đọc "lôgarit cơ số hai"; L07 `scale.6` nhắc lại và `assumes: jv2_log2` hợp lệ.
- **`TreeMap::new`**: L03 `hook.1`, ghi chú trên màn hình và lời đọc ("tạo một bản đồ có thứ tự mới để chứa kết quả", ba tham số của groupingBy); lặp lại ở sym.0 và pitfalls.4.
- **UTC / `PT23H`**: L08 `sym.0`: "giờ quốc tế ... múi giờ lệch 0", chữ T/Z của `2026-03-08T07:30:00Z`, "P mở đầu một khoảng, T ngăn phần giờ, H giờ, M tháng: PT23H = 23 giờ, P3M = 3 tháng"; lời đọc đánh vần "U T C", "P T hai mươi ba H". `intuition.2` và `example.0` dùng lại đúng.
- **`Consumer` / `ds::add`**: L09 `intuition.4` ("Consumer<GiaoDich>: kiểu của một hàm nhận một giao dịch và không trả gì, gọi bằng khiDoc.accept(g)") và `intuition.11` ("ds::add ... viết tắt của g -> ds.add(g)"), `intuition.13` (`t::them`). Lời đọc nói bằng lời thường ("kiểu hàm nhận một giá trị mà không trả gì"; "hai dấu hai chấm sau tên danh sách là tham chiếu hàm gắn với đối tượng").

Điểm P1 dùng ngưỡng "từ then chốt dùng làm lập luận mà không giảng" (không tính chuyện đã dạy ở JVA theo `requires_ext: JVA:L12`, và không tính ví dụ phụ gắn nhãn "ngoài phạm vi"). Nếu người điều phối chấm nghiêm hơn, hai bài sát biên là L05 (lõi CPU, ngăn xếp) và L08 (giờ mùa hè): khi đó P1 = 2 còn 8/10 = 80%, dưới 90%. Tôi giữ 2 vì cả hai chỉ là câu phụ trong phần đánh đổi, hệ quả vẫn đủ hiểu.

Độ dài/độ rã (L04, L05, L07, L09): thời lượng 18,5 / 18,3 / 17,0 / 18,8 phút nhưng đã gồm 4,5 / 4,5 / 3,4 / 5,5 phút `pause` làm bài; phút nói thật 14,0 / 13,8 / 13,6 / 13,3, tốc độ ≈ 175 âm tiết/phút (173-180 ở cả 10 bài), nghĩa là chậm, không nhồi. Mỗi bài 34-48 bước, mỗi câu `say` ngắn, khung dài nhất khoảng 10 giây (ngoài hai khoảng `pause` làm bài và lab). Rủi ro duy nhất là L09 `intuition` (14 khung mã liên tiếp, 2 phút 38 giây) và L04 `scale` (6 khung, hai chủ đề: dùng chung và proxy) hơi đặc; tôi không coi là rã.

## 4. Lab (tự làm như người học, không nhìn `loi_giai.*` trước)

Thời gian viết là của tôi (một agent đã đọc bài), nên với người mất gốc nên nhân 4-8; cột chạy là `time bash cham.sh` thật (bao gồm khởi động JVM).

| Bài | Tự làm được | Thời gian viết / chạy cham | Kẹt ở đâu | `mong_doi` khớp màn hình |
|---|---|---|---|---|
| L00 | có | ~4 phút / 15,5 s (lần đầu, nguội) | không; `de.md` cho đủ thư mục, lệnh `javac -d`, `jar --create` | khớp 4 dòng; khớp slide `practice.1` |
| L01 | có | ~4 phút / 10,6 s | không; `de.md` đưa sẵn 7 dòng CSV + danh sách import | khớp 4 dòng |
| L02 | có | ~4 phút / 9,0 s | không; `de.md` ghi rõ `Long.compare`, ổn định giữ 1 trước 7 | khớp 7 dòng |
| L03 | có | ~5 phút / 7,2 s | gợi ý `merge`, `counting()` không giảng trước nhưng `de.md`/slide gợi ý đủ | khớp 4 dòng |
| L04 | có | ~6 phút / 5,5 s | không; `de.md` cho ba lớp mẫu và chữ ký `lay` | khớp 3 dòng |
| L05 | có | ~4 phút / 5,3 s (chạy 4 lần: lần nào dòng 1 cũng `true`) | không; rủi ro lý thuyết: máy 1 lõi có thể in `false` (đề đã cảnh báo chạy lại) | khớp 3 dòng |
| L06 | có | ~6 phút / 4,9 s | không; `de.md` đưa hàm lỗi + bảng 5 ca + định dạng "DAT  " (hai dấu cách) | khớp 6 dòng (chạy bản chưa sửa ra đúng 1 HONG như đề) |
| L07 | có (yếu nhất) | ~2 phút / 5,1 s | lab chỉ là chép mã từ `de.md` rồi đổi `<=` thành `<`; tôi trích mã tự động bằng awk. Đủ để đối chiếu dấu vết thật (`TongPhi.java:15/22/26` khớp `de.md`) | khớp 2 dòng |
| L08 | có | ~4 phút / 4,9 s | không; công thức, import và 95 ngày đều có; `getDayOfWeek` là MONDAY khớp | khớp 4 dòng |
| L09 | có | ~8 phút / 6,5 s | tự viết `phanTich` + đếm số dòng từ 1 ở tiêu đề (dòng lỗi 5 và 7); `de.md` giải thích rõ | khớp 6 dòng |

`loi_giai.*` của cả 10 bài cũng được chấm: 10/10 ĐÚNG. Đề đủ để tự làm: có cả 10 bài (mỗi `de.md` liệt kê import, tên tệp, lệnh chạy, lệnh chấm).

## 5. Người học kẹt ở đâu (chỗ đầu tiên một người mất gốc chỉ xem video này và các bài trước nó không theo được)

- L00: không kẹt. Kẹt nhẹ nhất: `example.5` `jar tf bank.jar` (cờ `tf` chưa nói).
- L01: không kẹt. Nhẹ: `intuition.2` `static class Cua implements AutoCloseable ... @Override` (chỉ giảng "cam kết có hàm đóng").
- L02: không kẹt (`log₂` được giảng ngay `scale.0`).
- L03: không kẹt; `hook.1` cho thấy `GiaoDich::soTien` trước khi `sym.0` giảng `::`, nhưng chỉ là xem trước và có ghi chú về `TreeMap::new`.
- L04: không kẹt về khái niệm. Nhẹ: hook `@Service/@Autowired/@Transactional` (hứa giải thích ở cuối, và có giải thích ở `scale.5`).
- L05: không kẹt. Nhẹ: `scale.3` "ngăn xếp riêng", `scale.4` "số lõi CPU".
- L06: không kẹt.
- L07: kẹt nhẹ ở `intuition.0` (hình chia ở đáy nhưng lời đọc "khay trên cùng").
- L08: kẹt nhẹ ở `intuition.2` "chuyển sang giờ mùa hè ... ngày đó chỉ có 23 giờ" (không nói kim đồng hồ nhảy tiến 1 giờ).
- L09: không kẹt về khái niệm; không tự chạy lại được `example.6-7` vì không có `so_cai.csv`/`so_cai_loi.csv`.

## 6. Số đã tính lại / mã đã chạy

- Tổng: **≈ 90 đầu ra hoặc phép tính chạy lại**, **88 khớp**, **2 không kiểm được đầy đủ (không phải sai)**: (a) L07 `BocLoi` số dòng 12/17/10/4 (nguồn đầy đủ không có, tôi dựng lại thì cấu trúc và thông điệp `Caused by ... so du am: -50`, `... 1 more` khớp, số dòng lệch 1-2 do bố cục tôi tự đoán), (b) L09 `Theo thang: {...}` (tệp mẫu không phát; tổng ba tháng vẫn bằng tổng số dư 10 300 000 và 12 000 000).
- Theo bài: L00 9/9 (cây thư mục .class, `java -cp out bank.App`, `jar tf`, `-cp "lib/*"`, hai lỗi biên dịch `soDu has private access`, `moTa() is not public`, `reference to TaiKhoan is ambiguous`, `ClassNotFoundException`); L01 13/13 (kể cả OOM thật 32 MB: 1 000 dòng "doc xong 1001", 1 000 000 dòng "het bo nho", `TongDong` = 3999998000 = tính lại bằng Python); L02 9/9 (kể cả `sort -t, -k2,2 -k3,3nr` ra 4 2 5 6 1 3, `(int)(3e9-1) = -1294967297`); L03 10/10 (`NganMach` 10 phần tử; `ThongKeLon` {chuyen=1333332000, nap=1333334000, rut=1333332000}); L04 7/7 (`javap` Visible/Invisible, `QuyMo` 3 / 3 000 / 3 / 3 000 000); L05 9/9 (`DuaTranh` chạy 3 lần: 1 775 460, 1 621 784, 1 901 993; `KetCho` "so luong bi ket: 2"; `ThoiGian` 2 440 ms và 267 ms so với lý thuyết 2 000 và 200); L06 7/7 + hash (`a1de557821293ce9...` khớp `ENV.md`); L07 8/8 (`jdb` dừng line=10, `phiThu = 100`, `soDu = 100000 → 99900`; `ChiaDoi` 4 và 20 lần kiểm; `LogDat` 1 000 000 và 0); L08 8/8 (89 ngày, P3M, `640800000.000`, 1 755 616, HALF_UP/HALF_EVEN/DOWN, lệch 500 / 500 000 / 0, `PT23H`/`PT25H`, `1.234.567,89`, 95 ngày và MONDAY, lãi 1 873 973); L09 9/9 (KiemTra 7 DAT, bỏ kiểm tra tiền dương cho đúng "HONG so tien am / dat 6, hong 1", App 32 MB OOM, AppDong 32 MB = 1333334000 khớp, AppSong 64 MB OOM và 128 MB true).
- `checks` trong YAML: **162/162 biểu thức Python đúng** (L00 11, L01 18, L02 20, L03 17, L04 8, L05 16, L06 18, L07 13, L08 19, L09 22). Số được đọc ra khớp: đối chiếu thủ công các tổng chính (6 000 / 4 994 000; 6,2 triệu; 4 700 000 / 7 450 000; 21 000; 584,5 năm; 51,8 TB; 22 000 tổng phí lab L07; 6 400 000 lab L09).
- Chưa kiểm: nghe giọng đọc (không nghe audio); `(8 chữ số BIN)` PCI DSS 4.0 và "Spring Boot 2.6 cấm vòng" kiểm bằng hiểu biết, không bằng tài liệu (không có `sources*.md`).

## 7. Khung hình đã xem (≥ 5/bài) và lỗi hiển thị

Tổng 58 khung đã mở bằng Read, thêm quét máy toàn bộ 1 500 khung (vùng bên phải khung nội dung):
- L00: 00001, 00020, 00026, 00087, 00104, 00139. L01: 00020, 00025, 00057, 00099, 00125, 00140. L02: 00019, 00024, 00068, 00083, 00090, 00116. L03: 00009, 00032, 00035, 00095, 00127, 00161. L04: 00002, 00033, 00066, 00103, 00133. L05: 00004, 00027, 00040, 00101, 00124, 00159. L06: 00024, 00030, 00059, 00084, 00090, 00116. L07: 00003, 00026, 00069, 00094, 00131. L08: 00017, 00025, 00031, 00093, 00110, 00127. L09: 00023, 00045, 00048, 00062, 00096, 00115.
- Lỗi hiển thị thật: 3 khung có dòng mã tràn ra ngoài khung mã/khung nội dung (L02 00097, L05 00124, L09 00048), vẫn đọc được. Không có chữ bị cắt, không đè chữ ở các khung đã xem. Nửa dưới màn hình trống trong hầu hết khung (không phải lỗi, nhưng khung quiz có phụ đề đúng vị trí, nút "Dừng video" hiện ở khung practice).
- Sai khác hình-lời: L07 00026 (xem SHOULD), L05 00004 (nhãn mũi tên).

## 8. Nhận xét chung
- Chất lượng chuẩn xác rất cao: không MUST; mọi mã trên màn hình biên dịch/chạy đúng như video; các con số đo (so sánh, OOM, lệch làm tròn, bộ nhớ) tái lập được trên JDK 21.
- Khung mỗi bài đồng đều (hook, ôn, giải mã, hình, từng bước, ví dụ tự kiểm, quy mô, lỗi thường gặp, quiz, lab) nên P2, P4, P5, P6, P7 đều 2; cảnh "quy mô" cho số liệu ở 2-3 mức và đánh đổi ở cả 10 bài (P9 = 2).
- Điểm yếu còn lại chỉ ở trình bày: ba khung mã tràn, một hình tháp gọi hàm ngược chiều lời đọc (L07), một câu hook gọi nhóm luồng là "cách sửa" (L05), hai chỗ tuyệt đối (L04, L06), một quiz không chứng minh bằng số (L08), thiếu tệp mẫu cho L09.
- Lab đều tự làm được và tự chấm đúng, nhưng L07 là lab yếu nhất (chép + đổi một dấu); L09 lab nhỏ ổn nhưng ví dụ chính không tái hiện được vì thiếu tệp.
- L04 và L09 dày (L04 có hai ý nặng, L09 có 10 tệp) nhưng nhịp đọc chậm (~175 âm tiết/phút) và có `pause` nên không rã; thời lượng thật 17-18,8 phút trong đó 3-5,5 phút là dừng làm bài.
- Giả định nền: các bài dựa vào JVA (static, `new`, `long`, mảng, `@Override`, `interface`, `trim`) theo `requires_ext: JVA:L12`; bài nhắc lại bốn điều ở cảnh `prereq` nên không phải MUST "nhắc khoá khác thay vì giảng lại".
- Nên làm trước khi cho học: sửa 3 khung tràn (tự động bằng ngắt dòng), đảo hình L07, sửa câu hook L05, thêm tệp mẫu L09, đổi dữ liệu quiz L08. Không cái nào chặn việc "bắt đầu học".
