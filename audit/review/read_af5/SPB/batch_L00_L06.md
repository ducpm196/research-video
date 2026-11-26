# Báo cáo kiểm tra độc lập AF5 — SPB L00..L06

- Đối tượng: Khoá `SPB` (`L00..L06`), đọc toàn bộ YAML bài học, `curriculum/spb.yaml`, `labs/CONTRACT.yaml`, `labs/SPB/VERSIONS.md`, `labs/SPB/<Lxx>/`, `out/SPB/<Lxx>/{build_report.json,asr_report.md,chapters.txt,_frames.txt,frames/*.png}`.
- Ghi chú kiểm thử: Tuân thủ quy tắc `D-13` (không chạy `mvn`, `docker`, `build`, `tts`, `asr`, `render`, `verify_*.py`), nên mọi kết quả chạy `./mvnw -B verify` và container Testcontainers được ghi nhận **`CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`**; các phép tính số học, `alg.spb_*`, đếm từ, thời lượng và đối chiếu mã tĩnh đã kiểm chứng trực tiếp.
- Ghi chú `meta.json`: Không có tệp `out/SPB/<Lxx>/meta.json` trong kho (pipeline xuất `out/SPB/<Lxx>/build_report.json`). Lưu ý thêm: `build_report.json` ghi `built_at` `16:27–18:05Z` với `spec_sha256` trước khi ASR ghi thêm khối `asr_reviewed` lúc `19:22Z`, nên `sha16` của YAML hiện tại khác `spec_sha256` trong `build_report.json`.

## Bảng tóm tắt L00..L06

| Bài | `sha16` | Từ / Thời lượng (không pause) | MUST | SHOULD | `P1` | `P8` | `P1..P7` (Mất gốc) | `L1-L5` | `covers` | ASR (`chưa xem xét` / `NOT_VERIFIED`) | Frames đã xem |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **L00** | `aff6c5b554ebe3de` | 1 347 từ / 07:18 (6,47 phút) | 1 | 4 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 3/4 đủ, 1/4 thiếu log & cây gói | `0` / giữ đủ `6/6` | 4 PNG (`00012,00019,00027,00043`) |
| **L01** | `85bf39d792a29894` | 1 304 từ / 07:10 (6,33 phút) | 1 | 4 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 2/3 đủ, 1/3 thiếu số liệu phân tích & tải | `0` / giữ đủ `2/2` | 5 PNG (`00011,00013,00019,00027,00041`) |
| **L02** | `d51d4e8aabc98e05` | 1 313 từ / 07:05 (6,24 phút) | 2 | 3 | 1 | 2* | 10 (`CHƯA`) | 2,1,2,?,2 | 3/3 (nhưng `example` thiếu constructor, `intuition` cắt cụt) | `0` / `0` gắn cờ | 4 PNG (`00013,00019,00028,00042`) — **SVG `00013` gãy** |
| **L03** | `0abd11c7a1d12c20` | 1 331 từ / 07:23 (6,56 phút) | 1 | 2 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 3/3 đúng | `0` / giữ đủ `8/8` | 5 PNG (`00011,00013,00015,00018,00026,00043` -> 6 PNG) |
| **L04** | `ac59bece8c5e8689` | 1 343 từ / 07:17 (6,45 phút) | 1 | 3 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 3/4 đủ, 1/4 (`quymo`) thiếu số thất bại | `0` / giữ đủ `7/7` | 5 PNG (`00011,00013,00018,00026,00044`) |
| **L05** | `fda19db6ea54691b` | 1 341 từ / 07:18 (6,47 phút) | 1 | 3 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 3/3 đúng | `0` / giữ đủ `16/16` | 4 PNG (`00012,00019,00024,00044`) |
| **L06** | `9c130c69fcf578a9` | 1 332 từ / 07:17 (6,45 phút) | 1 | 4 | 1 | 2* | 12 (`CHƯA`) | 2,1,2,?,2 | 3/4 đủ, 1/4 (Obj 1 ghi PostgreSQL nhưng lab dùng H2) | `0` / giữ đủ `18/18` | 4 PNG (`00013,00019,00024,00044`) |

> `*` Ghi chú `P8=2*` và `L4=?`: Cảnh `check` trình bày log/khẳng định chạy thật khớp cấu trúc `KiemL0xTest.java`, nhưng kết quả chạy `./mvnw -B verify` / Docker là **`CHƯA KIỂM`** khi đọc theo quy tắc `D-13`.

**Kết luận tổng lô:** **CÓ LỖI CHẶN (`MUST > 0` ở cả 7 bài L00..L06)**:
1. **Chặn toàn lô (`L00..L06`, MUST #6):** Thời lượng không kể `pause` chỉ đạt **6,24 – 6,56 phút** (< 9,0 phút theo `BRIEF_AF5.md` §2.A #6 và §2.D), dù số từ vừa chạm ngưỡng `1 304 – 1 347` từ.
2. **Chặn riêng `L02` (MUST #3/#7):** Cảnh `intuition` (dòng 66) bị cắt cụt giữa thẻ SVG (`Mở TX 1 (Kết nối`), khiến khung hình `00013.png` chỉ còn 2 hộp đầu và 70% màn hình trống, không có phần `TX 2 / AuditLogService` và `self-invocation`.

---

# SPB L00 — sha16: `aff6c5b554ebe3de`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:18` (`438.100 s`, trừ `50.0 s` pause = `388.100 s` = `6.47` phút không pause) / `1 347` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `57 câu, thiếu audio: 0, gắn cờ: 6, chưa xem xét: 0`, giữ đúng `6/6` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 438.1` (`pause: 50.0`) | Thời lượng không tính pause là `438.1 - 50.0 = 388.1 s = 6.47 phút < 9.0 phút`, vi phạm ngưỡng tối thiểu `>= 9,0 phút không kể pause` (`BRIEF_AF5.md` §2.A #6). | Mở rộng phần giải thích cấu trúc dự án, đọc nhật ký khởi động thật, giải thích từng thẻ `pom.xml` để lời đọc đạt `~1 900–2 100` từ (`>= 9,0 phút`). | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `objectives[1]` & `example` | `Dựng dự án Spring Boot 4.1.3 nền tảng, đọc cấu trúc gói và nhật ký khởi động` | Cảnh `example` chỉ chiếu `pom.xml`, `ChuyenKhoanApplication`, `HealthController`; không hề chiếu cây thư mục/cấu trúc gói (`src/main/java/...`, `.mvn/wrapper/...`) và không chiếu nhật ký khởi động (`Started ChuyenKhoanApplication...`). | Thêm 1 step trong `example` chiếu cây thư mục chuẩn và log khởi động Tomcat/Spring Boot 4.1.3 thật. | ĐÃ KIỂM (YAML) |
| SHOULD | `hook`, `example`, `quymo`, `quiz` (`checks`) | `21 + 4 >= 21`, `4 + 1 + 3 == 8`, `500 > 50`, `3 + 0 == 3`, `14 * 4 < 120` | Hằng đẳng thức/biểu thức vô nghĩa không tham chiếu mô hình thật (`4+1+3==8` cộng chữ số phiên bản, `3+0==3`, `500>50`), vi phạm `BRIEF_AF5.md` §2.D. | Thay bằng kiểm chứng gắn tham số thật của bài (vd tốc độ tăng tốc cache `cold_s / warm_s`, số lớp kiểm thử). | ĐÃ KIỂM (Python) |
| SHOULD | `quymo` | `~25–45 s`, `~35–55 s`, `~60–90 s` cho 1, 50 và 500 lớp | Đưa con số ước lượng (`~`) cho 50 và 500 lớp nhưng không nêu giả định đo (tốc độ mạng tải `~/.m2`, CPU/SSD) dù `objectives[3]` ghi "Đo thời gian dựng...". | Ghi rõ giả định mạng/máy hoặc dẫn chứng thời gian đo thật cho khung L00 và ghi rõ ngoại suy cho 50/500 lớp. | ĐÃ KIỂM (YAML) |
| SHOULD | `sym` (`say`) & `check` | `tiền tố tiêu chuẩn mới`, `mô hình điều khiển hiển thị`; `[INFO] Tests run: 3` | (1) `say` dịch `jakarta.*` / `spring-boot-starter-webmvc` sang tiếng Việt không đọc tên gói tiếng Anh khiến người mới khó đối chiếu bảng; (2) `loi_giai` còn có `ChuyenKhoanApplicationTests` (1 test) + `KiemL00Test` (3 test) = 4 test khi chạy `./mvnw -B verify`. | Đọc rõ tên định danh tiếng Anh trên màn hình; cập nhật log `check` đúng tổng `Tests run: 4` (hoặc ghi rõ dòng của `KiemL00Test`). | ĐÃ KIỂM (YAML + `loi_giai`) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=1 -> Mất gốc: CHƯA (P1=1, P9=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `CONTRACT.yaml`: `du_an`, `ca_them: bat_buoc`, `loi_sai` đổi `"UP"` -> `"DOWN"`)
- covers đúng: 3/4 đủ, 1/4 (`example` thiếu cây gói & nhật ký khởi động của Obj 2)
- Số đã tính lại / mã đã chạy: `438.1 - 50.0 = 388.1 s (6.47 phút)`; toàn bộ `checks` kiểm bằng Python; chạy `./mvnw -B verify`: `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00012.png` (SVG 4 bước sạch), `frames/00019.png` (`pom.xml` rõ nét), `frames/00027.png` (thực ra là `check` log chạy lệnh sạch, không tràn hộp), `frames/00043.png` (`quiz` đáp án 2 rõ nét).
- Chỗ người mất gốc có thể kẹt: Chưa thấy cây thư mục Maven (`src/main/java` vs `src/test/java`) và thẻ `<groupId>/<artifactId>/<scope>` chưa được giải thích từng thẻ bằng lời.

---

# SPB L01 — sha16: `85bf39d792a29894`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:10` (`429.733 s`, trừ `50.0 s` pause = `379.733 s` = `6.33` phút không pause) / `1 304` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `55 câu, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0`, giữ đúng `2/2` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 429.733` (`pause: 50.0`) | Thời lượng không tính pause là `429.733 - 50.0 = 379.733 s = 6.33 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D (`1 304` từ sát mép dưới 1 300). | Bổ sung ví dụ từng bước (trace JSON bẩn đi qua Jackson -> `@Valid` -> `ApiExceptionHandler`), giải thích `TransferResponse`, mở rộng phân tích kích thước tải để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `objectives[2]` & `quymo` | `So sánh kích thước tải và số lần phân tích khi dữ liệu lỗi bị chặn sớm ở tầng vào ở 100, 10 000 và 1 000 000 yêu cầu` | Bảng `quymo` chỉ có kích thước tải ở mốc 100 (`~12 KB`), thiếu kích thước tải ở mốc 10 000 và 1 000 000, và hoàn toàn thiếu "số lần phân tích"; `say` cũng không đọc `~12 KB`. | Thêm cột/dòng tính kích thước tải (`~12 KB`, `~1,2 MB`, `~120 MB` với ~120 B/gói) và số lần phân tích JSON/SQL cho cả 3 mốc, đọc khớp `say` & `show`. | ĐÃ KIỂM (YAML) |
| SHOULD | `hook`, `formula`, `check`, `quiz` (`checks`) | `201 != 400`, `400 < 500`, `200 + 1 == 201` | Hằng đẳng thức/bất đẳng thức hằng số vô nghĩa, lặp lại (`201 != 400` xuất hiện 3 lần), vi phạm `BRIEF_AF5.md` §2.D. | Thay bằng phép tính số lỗi / kích thước tải tại 3 mốc (vd `10_000 * 5 // 100 == 500`, `100 * 120 == 12_000`). | ĐÃ KIỂM (Python) |
| SHOULD | `example`, `check` | `return new TransferResponse(...)`; `{"type":...,"title":"Validation Error","status":400,"errors":[...]}` | (1) `example` dùng `TransferResponse` nhưng không chiếu định nghĩa `record TransferResponse(String txId, String status, long amount)`; (2) `spring-boot-starter-validation` chỉ xuất hiện ở gợi ý cuối `practice`; (3) JSON ở `check` bỏ mất `"detail":"Du lieu dau vao khong hop le"` dù `ApiExceptionHandler` có `ProblemDetail.forStatusAndDetail(...)`. | Chiếu đủ `TransferResponse` và dependency `validation` trong `example`; bổ sung `"detail"` vào JSON minh hoạ ở `check`. | ĐÃ KIỂM (YAML + `loi_giai`) |
| SHOULD | `sym`, `example` (`say`) | `hai chú thích ràng buộc`, `từ khoá khai báo bản ghi bất biến`, `chú thích kiểm hợp lệ` | `say` tránh đọc tên annotation tiếng Anh (`@NotBlank`, `@Positive`, `@Valid`, `record`, `@RestControllerAdvice`), làm người mới khó nối âm thanh với mã Java trên màn hình. | Đọc rõ tên từng chú thích/từ khoá đi kèm nghĩa tiếng Việt. | ĐÃ KIỂM (YAML) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=1 -> Mất gốc: CHƯA (P1=1, P9=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL01Test` kiểm 4 ca MockMvc; `loi_sai` bỏ `@Valid`)
- covers đúng: 2/3 đủ (`example` + `check` ghép cho Obj 1 & 2), 1/3 thiếu số liệu tải/phân tích ở `quymo`
- Số đã tính lại / mã đã chạy: `429.733 - 50.0 = 379.733 s (6.33 phút)`; `100*5%=5`, `10_000*5%=500`, `1_000_000*5%=50_000`; chạy `./mvnw -B verify`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00011.png` (bảng `sym` sạch), `frames/00013.png` (SVG phân nhánh 201/400 rõ đẹp), `frames/00019.png` (mã DTO + Controller rõ), `frames/00027.png` (log `check` sạch), `frames/00041.png` (`quiz` đáp án 2 rõ).
- Chỗ người mất gốc có thể kẹt: Không thấy `TransferResponse` và dependency `spring-boot-starter-validation` trong phần giảng chính (`example`), tới `practice` mới xuất hiện ở gợi ý bước 3.

---

# SPB L02 — sha16: `d51d4e8aabc98e05`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:05` (`424.600 s`, trừ `50.0 s` pause = `374.600 s` = `6.24` phút không pause) / `1 313` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `54 câu, thiếu audio: 0, gắn cờ: 0, chưa xem xét: 0`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 424.6` (`pause: 50.0`) | Thời lượng không tính pause là `424.6 - 50.0 = 374.6 s = 6.24 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D. | Bổ sung trace từng bước vòng đời 2 giao dịch + giải thích `Account`/`AuditEntry`/`InsufficientFundsException` và `this.record()` để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| MUST | `intuition` (dòng 66) & `frames/00013.png` | `...<text x="380.0" y="116" font-size="15" text-anchor="middle" fill="#475569">Mở TX 1 (Kết nối` | `show` bị **cắt cụt giữa thẻ SVG** (không có `</text></svg></div>`, mất toàn bộ nửa phải vẽ `TX 2 / AuditLogService` và nhánh `self-invocation`). Ảnh `out/SPB/L02/frames/00013.png` chỉ hiện 2 hộp đầu (`Controller -> Proxy Transaction`) và để trống ~70% chiều ngang, trái hẳn với lời đọc mô tả 2 proxy & 2 kết nối -> vi phạm MUST #3 & #7. | Viết lại đầy đủ SVG `960x210` hiển thị đủ hai nhánh: gọi ngoài qua `Proxy 2 (REQUIRES_NEW, TX 2)` so với gọi nội bộ `this.record()` đi xuyên qua bỏ qua proxy. | ĐÃ KIỂM (YAML + `frames/00013.png`) |
| SHOULD | `example` step 2 | `@Transactional(rollbackFor = InsufficientFundsException.class) public void transfer(...)` | (1) `say` nói *"với hai trường kho dữ liệu và nhật ký đều là biến bất biến nhận từ hàm dựng"*, nhưng đoạn mã bước 2 cắt mất khai báo lớp, hai trường `private final` và hàm dựng; (2) thiếu điều kiện `if (fromId.equals(toId) \|\| amount <= 0) throw new IllegalArgumentException(...)` có trong `TransferService.java` thật và bị kiểm bởi `KiemL02Test`. | Hiển thị đầy đủ khai báo lớp, trường `final`, hàm dựng và nhánh kiểm `fromId.equals(toId)` trong `example`. | ĐÃ KIỂM (YAML + `loi_giai`) |
| SHOULD | `labs/SPB/L02/de.md` | `Cài đặt TransferService và AuditLogService (tiêm phụ thuộc qua constructor): 1. InsufficientFundsException... 2. TransferService.transfer... 3. AuditLogService.record...` | `de.md` không nêu yêu cầu từ chối tự chuyển (`fromId.equals(toId)` -> `IllegalArgumentException`) dù `KiemL02Test.selfTransferThrowsIllegalArgument()` kiểm ca này, và không ghi chữ ký `Account(String id, long balance)` / `AuditEntry(String msg)`. | Bổ sung yêu cầu `fromId.equals(toId)` ném `IllegalArgumentException` và chữ ký entity/repo vào `de.md`. | ĐÃ KIỂM (`de.md` + `KiemL02Test`) |
| SHOULD | `quiz` (`checks`) & `check` | `2 * 10 == 20`; `[INFO] Tests run: 4` | `checks` ở `quiz` không liên quan nội dung 2 câu hỏi (`this.record()` và `rollbackFor`); `check` ghi `Tests run: 4` (chỉ tính `KiemL02Test`, bỏ qua 1 ca của `ChuyenKhoanApplicationTests`). | Gắn `checks` của `quiz` với đúng kịch bản hoặc bỏ hằng số rời; ghi rõ số ca `KiemL02Test` vs tổng Surefire. | ĐÃ KIỂM (YAML + `loi_giai`) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=0 P4=1 P5=2 P6=2 P7=2 (Tổng=10) | P8=2* P9=2 -> Mất gốc: CHƯA (P3=0 do SVG bị cắt cụt, P1=1, Tổng=10 < 12, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL02Test` kiểm 4 ca; `loi_sai` bỏ `rollbackFor = InsufficientFundsException.class`)
- covers đúng: 3/3 (theo `covers`, nhưng `sym` chỉ tóm tắt bảng còn `example` bước 2 cắt mất phần constructor injection và `intuition` bị gãy SVG)
- Số đã tính lại / mã đã chạy: `424.6 - 50.0 = 374.6 s (6.24 phút)`; `alg.spb_tx_connections(1/5/50/500, True) = (2,2)/(2,10)/(2,100)/(2,1000)`; `500_000 - 150_000 = 350_000`; `500_000 + 200_000 = 700_000`; chạy `./mvnw -B verify`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00013.png` (**LỖI: SVG cắt cụt**), `frames/00019.png` (`formula` thực ra hiển thị sạch), `frames/00028.png` (`check` sạch), `frames/00042.png` (`quiz` đáp án 2 sạch).
- Chỗ người mất gốc có thể kẹt: Hình minh hoạ proxy (`intuition`) bị cắt mất một nửa nên không hình dung được sự khác biệt giữa gọi ngoài qua proxy với `this.record()`.

---

# SPB L03 — sha16: `0abd11c7a1d12c20`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:23` (`443.400 s`, trừ `50.0 s` pause = `393.400 s` = `6.56` phút không pause) / `1 331` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `54 câu, thiếu audio: 0, gắn cờ: 8, chưa xem xét: 0`, giữ đúng `8/8` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 443.4` (`pause: 50.0`) | Thời lượng không tính pause là `443.4 - 50.0 = 393.4 s = 6.56 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D. | Bổ sung giải thích thực thể `@OneToMany(fetch = FetchType.LAZY)`, cấu hình Testcontainers `@ServiceConnection`, phân tích từng câu SQL sinh ra khi lặp 20 tài khoản để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `example` | `V1__init.sql` & `AccountRepository` | Chưa chiếu lớp `Account` (`@OneToMany(mappedBy = "account", fetch = FetchType.LAZY)`) và cấu hình `PostgresBaseTest` (`@ServiceConnection(name = "postgres")`) trong phần giảng (`practice` bước 3 mới nhắc `@ServiceConnection`), khiến người mới chưa rõ cách ghép JPA với bảng Flyway và container Postgres. | Bổ sung snippet ngắn cho `@OneToMany(fetch = LAZY)` trên `Account` và `PostgresBaseTest` trong `example`. | ĐÃ KIỂM (YAML + `loi_giai`) |
| SHOULD | `example`, `check` (`checks`) | `1 + 20 == 21`, `21 - 1 == 20` | Biểu thức cộng trừ hằng số đơn giản, có thể dùng trực tiếp `alg.spb_n_plus_one(20)` như `hook` và `formula`. | Dùng `alg.spb_n_plus_one(20)[0] == 21` hoặc tương đương gắn biến rõ ràng. | ĐÃ KIỂM (Python) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=2 -> Mất gốc: CHƯA (P1=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL03Test` kiểm 3 ca thật qua `Statistics.getPrepareStatementCount()`; `loi_sai` bỏ `LEFT JOIN FETCH a.entries`)
- covers đúng: 3/3
- Số đã tính lại / mã đã chạy: `443.4 - 50.0 = 393.4 s (6.56 phút)`; `alg.spb_n_plus_one(10/20/1000/100_000) = (11,1)/(21,1)/(1001,1)/(100001,1)`; ước lượng trễ mạng `1000 * 0.15..0.4 ms = 150..400 ms` và `100_000 * 0.15..0.4 ms = 15..40 s` khớp bảng `quymo`; chạy `./mvnw -B verify` + Postgres container: `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00011.png` (bảng `sym` sạch), `frames/00013.png` (SVG 1+N vs JOIN FETCH rõ nét), `frames/00015.png` (công thức `$1 + N$` sạch), `frames/00018.png` (`V1__init.sql` rõ nét), `frames/00026.png` (`check` log sạch), `frames/00043.png` (`practice` sạch).
- Chỗ người mất gốc có thể kẹt: Thiếu ví dụ ánh xạ `@OneToMany` và cách tạo `PostgreSQLContainer` với `@ServiceConnection` trong phần bài giảng trước khi vào `practice`.

---

# SPB L04 — sha16: `ac59bece8c5e8689`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:17` (`437.133 s`, trừ `50.0 s` pause = `387.133 s` = `6.45` phút không pause) / `1 343` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `56 câu, thiếu audio: 0, gắn cờ: 7, chưa xem xét: 0`, giữ đúng `7/7` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 437.133` (`pause: 50.0`) | Thời lượng không tính pause là `437.133 - 50.0 = 387.133 s = 6.45 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D. | Bổ sung ví dụ chạy tay từng bước cho 2 luồng ngược chiều `TK1->TK2` và `TK2->TK1` (trạng thái lock, số dư, 4 dòng journal) và thêm số liệu đo xung đột lạc quan để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `objectives[3]` & `quymo` | `Đo số giao dịch thất bại do xung đột khoá lạc quan khi tỉ lệ tranh chấp tăng 2, 20 và 200 luồng` | Bảng `quymo` chỉ ghi mô tả định tính (*"Tỉ lệ đụng độ thấp"*, *"Nhiều luồng dính OptimisticLockException"*, *"Bão thử lại"*), không có con số thất bại/thử lại nào ở 2, 20 và 200 luồng; `checks` của `quymo` dùng `200 > 20` và `20 > 2` (vô nghĩa). | Bổ sung số liệu đo hoặc mô hình ước lượng cụ thể số lượt xung đột/thử lại ở 2, 20 và 200 luồng và thay `checks` tương ứng. | ĐÃ KIỂM (YAML + Python) |
| SHOULD | `example` step 2 | `journals.save(new JournalEntry(txId, from, -amt)); ... idems.save(new IdempotencyRecord(k, txId, amt));` | Dùng biến `txId` nhưng **chưa khai báo `String txId = ...`** trong đoạn mã hiển thị trên slide; đồng thời thiếu điều kiện kiểm tra `from.equals(to)` có trong `LedgerTransferService.java` thật. | Thêm dòng `String txId = "TX-" + ...;` và `\|\| from.equals(to)` vào code box bước 2 của `example`. | ĐÃ KIỂM (YAML + `loi_giai`) |
| SHOULD | `formula` (`frames/00018.png`) & `quiz` (`checks`) | `\sum_{\text{toàn sổ}} \text{amount} = 0`; `-300 + 300 == 0` | (1) Trên `frames/00018.png`, phần chỉ số dưới của `\sum_{\text{toàn sổ}}` hơi sát đường viền cam hộp focus; (2) `[quiz] -300 + 300 == 0` không khớp con số `500 000 đồng` trong câu hỏi quiz 2. | Điều chỉnh lề/tách dòng công thức và sửa `checks` của `quiz` thành `-500_000 + 500_000 == 0`. | ĐÃ KIỂM (`frames/00018.png` + YAML) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=1 -> Mất gốc: CHƯA (P1=1, P9=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL04Test` kiểm phát lại idempotency, 10 luồng ngược chiều 4 thread không deadlock, `@Version` tăng 1; `loi_sai` vô hiệu hoá `idems.findById`)
- covers đúng: 3/4 đủ, 1/4 (`quymo` chưa đo số lượng thất bại tại 2/20/200 luồng như Obj 4)
- Số đã tính lại / mã đã chạy: `437.133 - 50.0 = 387.133 s (6.45 phút)`; `alg.spb_double_entry_sum([-300_000, 300_000, -150_000, 150_000]) == 0`; `1_000_000 - 300_000 = 700_000`; `1_000_000 + 1_000_000 = 2_000_000`; chạy `./mvnw -B verify` + Postgres container: `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00011.png` (bảng `sym` sạch), `frames/00013.png` (SVG deadlock vs sắp xếp ID + 3 bước TX rõ đẹp), `frames/00018.png` (công thức hơi sát viền hộp cam), `frames/00026.png` (`check` sạch), `frames/00044.png` (`practice` sạch).
- Chỗ người mất gốc có thể kẹt: `txId` xuất hiện bất ngờ trong code `example` bước 2 mà không có dòng khởi tạo.

---

# SPB L05 — sha16: `fda19db6ea54691b`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:18` (`438.333 s`, trừ `50.0 s` pause = `388.333 s` = `6.47` phút không pause) / `1 341` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `56 câu, thiếu audio: 0, gắn cờ: 16, chưa xem xét: 0`, giữ đúng `16/16` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 438.333` (`pause: 50.0`) | Thời lượng không tính pause là `438.333 - 50.0 = 388.333 s = 6.47 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D. | Bổ sung phần giải thích nhánh chờ `else` của 19 luồng thua khoá, trace từng bước kịch bản race ghi đè A/B khi write-through vs write-invalidate để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `example` step 1 | `if (Boolean.TRUE.equals(redis.opsForValue().setIfAbsent(...))) { try { ... } finally { ... } }` | Đoạn mã `example` bước 1 cắt bỏ nhánh chờ `else` (ngủ 25 ms tối đa 40 vòng rồi đọc lại `redis`, fallback `loadFromDb`) có trong `BalanceCacheService.java`, mặc dù `pitfalls` lỗi 3 nhấn mạnh *"thiếu nhánh chờ/đọc lại thì khoá trở nên vô nghĩa"*. (Ghi chú thêm: `get` rồi `delete` trong `finally` chưa nguyên tử bằng Lua nếu hết `EX 5`, nhưng chấp nhận được ở mức nhập môn nếu nêu rõ giới hạn). | Thêm nhánh `for (int i=0; i<40; i++) { Thread.sleep(25); ... }` vào `example` bước 1 và nhắc ngắn hạn chế get-then-delete khi giữ khoá quá 5 s. | ĐÃ KIỂM (YAML + `loi_giai`) |
| SHOULD | `labs/SPB/L05/de.md` | `1. getBalance(accId)... 2. deposit(accId, delta)...` | `de.md` không liệt kê hai phương thức `getDbReads()` và `resetDbReads()` trên `BalanceCacheService` dù `KiemL05Test` gọi trực tiếp cả hai để đếm lượt chạm DB. | Ghi rõ bộ đếm `getDbReads()` / `resetDbReads()` trong `de.md`. | ĐÃ KIỂM (`de.md` + `KiemL05Test`) |
| SHOULD | `hook`, `example`, `quymo`, `quiz` (`checks`) | `10_000 / 1 == 10_000`, `100_000 / 1 == 100_000`, `30 + 3 == 33`, `[example] 500_000 + 200_000 == 700_000` | Hằng đẳng thức `n / 1 == n` vô nghĩa; `500_000 + 200_000 == 700_000` đặt ở `example` dù dữ liệu đó nằm ở `check`. | Chuyển check `500_000 + 200_000 == 700_000` sang `check`, thay các check `n / 1 == n` bằng biểu thức giảm tải thực tế (vd `(100 - 1) / 100 == 0.99`). | ĐÃ KIỂM (Python + YAML) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=2 -> Mất gốc: CHƯA (P1=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL05Test` kiểm cache hit, deposit eviction, 20-thread stampede; `loi_sai` bỏ `redis.delete("bal:" + accId)`)
- covers đúng: 3/3
- Số đã tính lại / mã đã chạy: `438.333 - 50.0 = 388.333 s (6.47 phút)`; `30 + 0..5 = 30..35 s`; `500_000 + 200_000 = 700_000`; `20 - 1 = 19`; giảm SQL ở 100 req từ 100 -> 1 = giảm 99%; chạy `./mvnw -B verify` + Redis container: `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00012.png` (SVG 20 luồng -> `SET lock NX EX 5` rõ đẹp), `frames/00019.png` (mã `BalanceCacheService` rõ nét), `frames/00024.png` (log `check` sạch), `frames/00044.png` (`practice` sạch).
- Chỗ người mất gốc có thể kẹt: Code `example` thiếu vòng lặp chờ `else` nên người học chép theo video sẽ làm 19 luồng còn lại rơi thẳng ra ngoài hàm hoặc lỗi biên dịch vì thiếu `return`.

---

# SPB L06 — sha16: `9c130c69fcf578a9`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: `07:17` (`436.967 s`, trừ `50.0 s` pause = `386.967 s` = `6.45` phút không pause) / `1 332` từ
- `boiler_deny`: 0 câu trúng; `meta.json`: không tồn tại (có `build_report.json`); ASR: `55 câu, thiếu audio: 0, gắn cờ: 18, chưa xem xét: 0`, giữ đúng `18/18` dòng `"NOT_VERIFIED bằng tai người"`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài (`say`, `build_report.json`) | `timeline_seconds: 436.967` (`pause: 50.0`) | Thời lượng không tính pause là `436.967 - 50.0 = 386.967 s = 6.45 phút < 9.0 phút`, vi phạm `BRIEF_AF5.md` §2.A MUST #6 & §2.D. | Bổ sung ví dụ trace từng bước chuỗi offset/retry/DLT, giải thích `OutboxEvent` entity & `KafkaBaseTest`, phân tích sâu hơn đánh đổi Kafka vs RabbitMQ vs JMS để đạt `>= 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| SHOULD | `objectives[0]`, `formula` & `labs/SPB/L06/loi_giai/pom.xml` | `Lưu đơn chuyển khoản cùng bản ghi Outbox trong một giao dịch PostgreSQL trước khi phát lên Kafka` | Mục tiêu 1 và `formula` nói lưu Outbox trong giao dịch **PostgreSQL**, nhưng `labs/SPB/L06/loi_giai/pom.xml` (dòng 30–34) và `application.properties` (dòng 1) dùng **H2 trong bộ nhớ (`ddl-auto=create-drop`)**, không dùng container PostgreSQL (ghép cả 3 container diễn ra ở L10). | Đồng bộ lại câu chữ Mục tiêu 1 (ghi rõ giao dịch DB/JPA, hoặc chuyển lab L06 sang dùng PostgreSQL cùng Kafka). | ĐÃ KIỂM (`pom.xml` + YAML) |
| SHOULD | `curriculum/spb.yaml` vs `L06` YAML | `So sánh cơ chế...` vs `Phân biệt cơ chế...` | Lệch nhỏ động từ ở Mục tiêu 3 giữa giáo án `curriculum/spb.yaml` và tệp YAML bài học. | Đồng nhất câu chữ Mục tiêu 3 giữa hai tệp. | ĐÃ KIỂM (YAML) |
| SHOULD | `hook`, `example`, `check`, `quiz` (`checks`) | `3 + 1 == 4`, `1 + 2 == 3`, `3 == 1 + 1 + 1` | Hằng đẳng thức vô nghĩa lặp lại, vi phạm `BRIEF_AF5.md` §2.D. | Thay bằng phép tính trễ hàng đợi/lùi hàm mũ thật của bài (vd `1_000 * 1.5 == 1_500` giây = `25` phút ở mốc 100 000 tin lỗi 1%). | ĐÃ KIỂM (Python) |
| SHOULD | `check`, `example` | `[INFO] Tests run: 3` | `check` chỉ ghi 3 ca của `KiemL06Test` (bỏ qua 1 ca `SmokeL06Test` chạy cùng `./mvnw -B verify`); `example` không chiếu lớp `OutboxEvent` / phương thức `markSent()`. | Ghi rõ tổng Surefire 4 ca (`KiemL06Test: 3 ca`) và tóm tắt cấu trúc `OutboxEvent` (`id, payload, status`). | ĐÃ KIỂM (YAML + `loi_giai`) |

## B. Độ sâu & Lab
- Điểm: P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2 (Tổng=12) | P8=2* P9=2 -> Mất gốc: CHƯA (P1=1, thời lượng < 9,0 phút)
- Lab: L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2 (tĩnh; `KiemL06Test` kiểm rollback Outbox, publish/consume hợp lệ, poison pill -> `transfer.events-dlt`; `loi_sai` bỏ trống `onDlt`)
- covers đúng: 3/4 đủ, 1/4 (`example` dạy `@Transactional` Outbox trên H2 trong khi Obj 1 ghi PostgreSQL)
- Số đã tính lại / mã đã chạy: `436.967 - 50.0 = 386.967 s (6.45 phút)`; `100 + 200 + 400 = 700 ms`; `1 000 * 0.1% = 1 tin` (`1 * 0.5 * 3 = 1.5 s`); `100 000 * 1% = 1 000 tin` (`1 000 * 1.5 s = 1 500 s = 25.0 phút`); `1 000 000 * 10% = 100 000 tin`; chạy `./mvnw -B verify` + Kafka container: `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`.
- Khung hình đã xem: `frames/00013.png` (SVG 4 chặng Outbox -> Publisher -> Retry -> DLT rõ đẹp), `frames/00019.png` (`OrderOutboxService` rõ nét), `frames/00024.png` (`@RetryableTopic` + `@DltHandler` rõ nét), `frames/00044.png` (`practice` sạch).
- Chỗ người mất gốc có thể kẹt: `OrderOutboxService.publishPending()` chạy vòng `for` gửi đồng bộ/bất đồng bộ trên `@Transactional` mà chưa giải thích rõ `OutboxEvent` entity cũng như vì sao L06 dùng H2 thay vì PostgreSQL như mục tiêu ghi.
