# Báo cáo đọc độc lập AF5 — Khoá SPB (L07–L12)

- Người đọc: Tác tử đọc độc lập (`D-13`)
- Phạm vi: `SPB L07` .. `SPB L12` (`lessons/spb/L07..L12*.yaml`, `labs/SPB/L07..L12/`, `out/SPB/L07..L12/`, `curriculum/spb.yaml`, `labs/CONTRACT.yaml`, `labs/SPB/VERSIONS.md`, `audit/review/boiler_deny.txt`)
- Lưu ý môi trường: Theo quy tắc `D-13`, tác tử đọc không chạy `mvn`/`./mvnw`/`docker`/`verify_spb.py` hay `lv.py`; phần chạy thật lab `L4` ghi rõ `CHƯA KIỂM (không chạy mvn/Docker khi đọc theo quy tắc D-13)`. Riêng `out/SPB/<Lxx>/meta.json` không tồn tại ở cả 6 bài (khoá `SPB` dùng `out/SPB/<Lxx>/build_report.json`).

## Bảng tóm tắt lô SPB L07–L12

| Bài | sha16 | MUST | SHOULD | P1 | P8 | L1–L5 | covers | Thời lượng (không pause) / Từ | ASR / Frames |
|---|---|---|---|---|---|---|---|---|---|
| L07 | `00ff3db6782375a3` | 2 | 3 | 1 | 2 | `2/1/2/CK/2` | `1/3` (mục tiêu 2 hổng `Header` & sai cảnh `check`) | `07:19` (`6,49 phút`) / 1 327 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; 4 PNG OK |
| L08 | `162aedd9d33cc05b` | 1 | 4 | 1 | 2 | `2/1/2/CK/2` | `2/3` (`example` thiếu `JwtService`/`JwtAuthFilter`) | `07:06` (`6,26 phút`) / 1 329 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; 4 PNG OK (lệch `focus` bảng `quymo`) |
| L09 | `89f000aaafe26f94` | 3 | 3 | 1 | 2 | `2/1/2/CK/2` | `2/3` (mục tiêu 2 & `check` nói có "phản hồi bảo mật" nhưng 0 có) | `07:15` (`6,42 phút`) / 1 315 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; 4 PNG OK |
| L10 | `068e0907a6ee9d8e` | 1 | 3 | 1 | 2 | `2/1/2/CK/2` | `3/3` (chấp nhận qua `example` + `check`) | `07:20` (`6,51 phút`) / 1 312 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; **1 PNG tràn khung mã** (`00019.png`) |
| L11 | `2242cab7ec6ea179` | 2 | 3 | 1 | 2 | `2/1/2/CK/2` | `2/3` (mục tiêu 2 nêu "đo độ trễ" nhưng 0 có `Timer`/metric trễ) | `07:20` (`6,50 phút`) / 1 346 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; 4 PNG OK |
| L12 | `9b16543224043a59` | 1 | 2 | 2 | 2 | `2/1/2/CK/2` | `3/3` | `07:17` (`6,45 phút`) / 1 321 từ | ASR 0 chưa xem xét, giữ `NOT_VERIFIED bằng tai người`; 4 PNG OK |

> **Kết luận chung lô L07–L12:** **CÓ LỖI CHẶN (`MUST > 0`) ở cả 6/6 bài.** Chặn chung cả 6 bài là **MUST #6** (thời lượng không kể `pause` chỉ đạt `6,26–6,51 phút < 9,0 phút`), ngoài ra còn lỗi chuẩn xác/phủ mục tiêu ở L07 (thiếu `Header` versioning), L09 (nói sai có "phản hồi bảo mật" trên MockMvc và `strictOrder()` thiếu dòng gọi hàm), L11 (thiếu đo độ trễ theo mục tiêu 2). Các `checks` hằng đẳng thức (`2 + 2 == 4`, `2 + 1 == 3`, `1000 > 0`, `3 == 1 + 1 + 1`, `5 * 4 == 20`) cũng vi phạm quy tắc `CONTRACT.yaml` / `BRIEF_AF5.md` §2.D.

---

# SPB L07 — sha16: `00ff3db6782375a3`
- Tệp YAML: `lessons/spb/L07_openapi_springdoc_api_tai_nguyen_phien_ban.yaml`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L07/` + `out/SPB/L07/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:19` (`439,33 s` gồm `50 s` pause → **`6,49 phút` (`389,33 s`) không pause**) / **1 327 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L07/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T18:19:31Z`, 55 frames).
- ASR (`out/SPB/L07/asr_report.md`): `câu: 55, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0`; mục gắn cờ giữ nguyên `— NOT_VERIFIED bằng tai người`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 439.333`, tổng `pause: 50.0 s` | `439,333 - 50,0 = 389,333 s = 6,49 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6: phải `≥ 9,0 phút` không kể `pause`, `words = 1 327` tuy `≥ 1 300` nhưng tốc độ `vi-VN-NamMinhNeural` khiến audio chỉ ~6,5 phút). | Bổ sung giải thích sâu (ví dụ cấu hình `pom.xml`, `@ApiResponse` cho 201/400 `ProblemDetail`, chiến lược phiên bản Header) để lời đọc đạt khoảng 1 850–2 100 từ (`≥ 540 s` không `pause`). | ĐÃ KIỂM (`build_report.json` + YAML) |
| **MUST** | `objectives[1]` & `covers` (`check`) | `"Áp dụng thiết kế API hướng tài nguyên danh từ, phân trang con trỏ và chiến lược phiên bản URI/Header"` / `covers: objective 2 -> scene: check` | (1) Chiến lược phiên bản **Header** (`Accept` / `X-API-Version`) không được giảng hay minh hoạ ở bất kỳ cảnh nào trong `L07` (chỉ có URI `/api/v1/` và `/api/v2/`); (2) Cảnh `check` chỉ chiếu 3 dòng log kết quả `KiemL07Test`, không dạy thiết kế danh từ hay chiến lược phiên bản (vi phạm MUST #3). | Giảng rõ so sánh URI versioning vs Header versioning (ví dụ `Accept: application/vnd.bank.v2+json`) trong `sym`/`example`/`quymo`, hoặc bỏ chữ `/Header` nếu chỉ dạy URI; gán `covers` mục tiêu 2 về cảnh thực sự dạy (`example`/`quymo`). | ĐÃ KIỂM (đọc toàn YAML `L07`) |
| **SHOULD** | `prereq` step 1 (`say` dòng 53) | `"Đặc tả đặc tả OpenAPI được sinh thẳng từ các chú thích cạnh hàm điều khiển..."` | Lỗi lặp từ `"Đặc tả đặc tả"` trong lời đọc TTS. | Sửa thành `"Đặc tả OpenAPI được sinh thẳng..."`. | ĐÃ KIỂM (YAML dòng 53–54) |
| **SHOULD** | `hook` (`checks` dòng 27), `quymo` (`checks` dòng 185) | `2 + 1 == 3`, `100 > 10` | Hằng đẳng thức/so sánh hằng số rỗng không gắn biến hay phép tính nghiệp vụ (vi phạm `BRIEF_AF5.md` §2.D). Còn `example` step 2 thiếu `@ApiResponse(responseCode = "201", ...)` và `400 ProblemDetail` dù `objectives[0]` nói `"chú thích mã phản hồi cho mọi đầu cuối"`. | Thay bằng check gắn tham số thật (ví dụ `5 + 3 + 1 == 9` hoặc `limit + 1 == 4`) và thêm `@ApiResponse` cho `createV2` (201/400). | ĐÃ KIỂM (Python `eval` + đọc `example`) |
| **SHOULD** | `labs/SPB/L07/de.md` dòng 5 | `GET /api/v1/transfers?cursor=5&limit=3 ... trả nextCursor = 8, hasMore = true` | Bộ số `cursor=5&limit=3 -> [6,7,8], nextCursor=8` trong lab trùng đúng bộ số ví dụ trong `formula` & `check`. | Đổi `KiemL07Test` & `de.md` sang cặp số khác ví dụ (ví dụ `cursor=10&limit=4 -> [11..14], nextCursor=14`), hoặc giữ `check` tách số với `de.md`. | ĐÃ KIỂM (`de.md` + `KiemL07Test.java`) |

## B. Độ sâu & Lab
- Điểm: `P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2` (Tổng = **13/14**) | `P8=2 P9=2` -> Mất gốc: **GẦN** (`P1=1 < 2` do thiếu đoạn `pom.xml` phụ thuộc `springdoc-openapi-starter-webmvc-ui:3.2.1` trong `example`, thiếu `@Tag`, thiếu `Header` versioning như mục tiêu 2 nêu).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `KiemL07Test.java` có 3 `@Test` khớp `mong_doi.txt` (`KiemL07Test: 3 ca, 0 hỏng`); `loi_sai/` sửa `t.id() > cursor` thành `>=` để ca `cursorPaginationStrictlySkipsCursorId` thất bại chống lách.
- `covers` đúng: **1/3** (Mục tiêu 1 ở `example` tạm ổn dù thiếu `pom.xml` & `@ApiResponse` trên v2; Mục tiêu 2 trỏ `check` và thiếu hẳn `Header`; Mục tiêu 3 ở `quymo` đạt).
- Số đã tính lại / mã đã chạy: Kiểm Python các `checks` (`5+3==8`, `6+7+8==21`, `8-5==3`, `20+1==21` -> `True`). Không chạy `mvn` theo `D-13`.
- Khung hình đã xem: `00013.png` (SVG OFFSET vs Cursor & OpenAPI), `00020.png` (mã `listByCursor`), `00027.png` (bảng `quymo` 1/10/100 đối tác), `00043.png` (cảnh `practice`). Bố cục sạch, không tràn hộp hay cắt chữ.
- Chỗ người mất gốc có thể kẹt: `de.md` yêu cầu thêm `springdoc-openapi-starter-webmvc-ui:3.2.1` vào `pom.xml` và mở `/v3/api-docs`, nhưng `example` chưa chiếu đoạn XML `<dependency>` và chưa giải thích cách thêm `Header` versioning như mục tiêu 2 nêu.

---

# SPB L08 — sha16: `162aedd9d33cc05b`
- Tệp YAML: `lessons/spb/L08_spring_security_jwt_phan_quyen_owasp.yaml`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L08/` + `out/SPB/L08/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:06` (`425,80 s` gồm `50 s` pause → **`6,26 phút` (`375,80 s`) không pause**) / **1 329 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L08/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T18:27:38Z`, 52 frames).
- ASR (`out/SPB/L08/asr_report.md`): `câu: 52, thiếu audio: 0, gắn cờ: 4, chưa xem xét: 0`; 4 mục gắn cờ đều giữ nguyên `— NOT_VERIFIED bằng tai người` (ghi chú nhỏ: mục khung 28 có đoạn `khác “” → nghe thành “một”` do căn lề diff ASR, không phải lỗi nội dung bài).

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 425.8`, tổng `pause: 50.0 s` | `425,80 - 50,0 = 375,80 s = 6,26 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6). | Bổ sung phần giảng và mã thật của `JwtService` (`HmacSHA256`, `MessageDigest.isEqual`, kiểm `exp`) và `JwtAuthFilter` (`OncePerRequestFilter`, `SecurityContextHolder.clearContext()`) để đủ `≥ 9,0 phút` không `pause` và giúp người mất gốc không kẹt. | ĐÃ KIỂM (`build_report.json` + YAML) |
| **SHOULD** | `example` step 1–2 vs `practice` (`de.md`) | `chain(HttpSecurity http, JwtAuthFilter f)` (dòng 132) | `example` dùng `JwtAuthFilter f` làm tham số nhưng toàn bộ video không hề chiếu mã Java của `JwtAuthFilter` hay `JwtService`, dù `practice` bắt người học tự cài cả `JwtService` lẫn `JwtAuthFilter`. Ngoài ra câu `"Khong co quyen tai khoan nguon"` ở `example` hơi khác `"Khong co quyen tren tai khoan nguon"` trong `loi_giai/SecureTransferController.java`. | Thêm 1–2 step vào `example` chiếu `JwtService` và `JwtAuthFilter` khớp với `loi_giai/`. | ĐÃ KIỂM (YAML + `loi_giai/`) |
| **SHOULD** | `quymo` step 1 (`focus` dòng 196–199, `00027.png`) | `focus: [0, '1.3', '1.4']` với 3 câu `say` | Ở `00027.png`, câu 2 (`"cả chín mươi lăm nghìn lượt xấu bị chặn..."`) lại tô cam dòng `1 000 yêu cầu (950 sai + 50 đúng)` thay vì dòng `100 000 yêu cầu (95 000 dò quét)`. | Chỉnh lại số phần tử `focus` cho khớp đúng 3 câu `say` và các dòng bảng (`[0, '1.2', '1.3', '1.4']` hoặc tách 4 câu). | ĐÃ KIỂM (`00027.png` + YAML) |
| **SHOULD** | `example`, `check`, `quiz` (`checks` dòng 130, 164, 226) | `1000 > 0`, `2 + 2 == 4`, `401 < 403` | `2 + 2 == 4` và `1000 > 0` là hằng đẳng thức vô nghĩa; `401 < 403` so sánh thứ tự số mã HTTP không mang nghĩa toán học. | Thay bằng phép tính thật của bài (ví dụ `1000 - 950 == 50`, `300 > 0` hạn `exp`). | ĐÃ KIỂM (Python `eval`) |
| **SHOULD** | `labs/SPB/L08/de.md` dòng 6 | `an sở hữu TK-AN, binh sở hữu TK-BINH` | Trùng đúng bộ dữ liệu mẫu (`an`, `TK-AN`, `TK-BINH`) đã chiếu trong `hook`, `example`, `check` và `practice` gợi ý. | Cân nhắc dùng bộ tài khoản khác trong `KiemL08Test` nếu tách dữ liệu ví dụ với đề lab. | ĐÃ KIỂM (`de.md` + `KiemL08Test.java`) |

## B. Độ sâu & Lab
- Điểm: `P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2` (Tổng = **12/14**) | `P8=2 P9=2` -> Mất gốc: **GẦN** (`P1=1 < 2` vì `JwtService`/`JwtAuthFilter` chỉ mô tả bằng chữ mà chưa chiếu mã mẫu; `P4=1` vì chưa lần tay từng bước ký/kiểm `header.payload.sig` và `exp`).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `KiemL08Test.java` có 4 `@Test` khớp `mong_doi.txt` (`KiemL08Test: 4 ca, 0 hỏng`); `loi_sai/` thay `!owner.equals(auth.getName())` thành `false` để làm gãy test BOLA.
- `covers` đúng: **2/3** (`example` dạy `SecurityFilterChain` + BOLA nhưng thiếu `JwtAuthFilter`/`JwtService`; `sym` liệt kê 5 lỗi OWASP; `quymo` đủ 3 mốc 10 / 1 000 / 100 000).
- Số đã tính lại / mã đã chạy: `256 // 8 == 32`, `100_000 - 95_000 == 5_000` (`True`). Không chạy `mvn` theo `D-13`.
- Khung hình đã xem: `00012.png` (SVG 3 lớp chốt chặn), `00019.png` (`SecurityFilterChain`), `00027.png` (bảng `quymo` — lộ lệch `focus`), `00042.png` (`practice`).
- Chỗ người mất gốc có thể kẹt: Khi làm lab phải tự viết `JwtService` (`Base64.getUrlEncoder().withoutPadding()`, `Mac.getInstance("HmacSHA256")`, tách 3 phần `header.payload.sig`) và `JwtAuthFilter` (`OncePerRequestFilter`, `UsernamePasswordAuthenticationToken`), nhưng video chưa hề chiếu mẫu 2 lớp này.

---

# SPB L09 — sha16: `89f000aaafe26f94`
- Tệp YAML: `lessons/spb/L09_kiem_thu_don_vi_mockito_mockmvc.yaml`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L09/` + `out/SPB/L09/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:15` (`435,13 s` gồm `50 s` pause → **`6,42 phút` (`385,13 s`) không pause**) / **1 315 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L09/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T18:37:21Z`, 55 frames).
- ASR (`out/SPB/L09/asr_report.md`): `câu: 55, thiếu audio: 0, gắn cờ: 13, chưa xem xét: 0`; tất cả 13 mục gắn cờ giữ nguyên `— NOT_VERIFIED bằng tai người`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 435.133`, tổng `pause: 50.0 s` | `435,133 - 50,0 = 385,133 s = 6,42 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6). | Mở rộng phần giảng `UnitTransferService`, `UnitTransferController` (`@Valid` record `Req`), và bổ sung ca kiểm MockMvc phản hồi bảo mật để đạt `≥ 9,0 phút` không `pause`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| **MUST** | `objectives[1]` + `check` `say` (dòng 20, 171) | `"Kiểm thử hợp đồng HTTP, kiểm dữ liệu vào và phản hồi bảo mật trên MockMvc..."` & `"Hai ca lát cắt web khẳng định chức năng kiểm dữ liệu vào và phản hồi bảo mật chạy chuẩn..."` | **Sai sự thật / không dạy mục tiêu (MUST #1, #3):** `labs/SPB/L09/loi_giai/pom.xml` không có `spring-boot-starter-security`; `example` step 2 và `KiemL09WebTest.java` chỉ kiểm `201` (`webSliceReturns201FromMockService`) và `400` (`invalidPayloadRejectedAtWebSlice`), **không có bất kỳ ca kiểm hay cấu hình bảo mật (401/403) nào**. Ngoài ra `covers` gán mục tiêu 2 vào `check` (chỉ chiếu log kết quả) thay vì `example`. | Hoặc thêm thật `Security` + ca kiểm MockMvc trả `401`/`403` vào cả bài dạy và `KiemL09WebTest`, hoặc sửa lại `objectives[1]` và `check` `say` bỏ cụm `"phản hồi bảo mật"`. | ĐÃ KIỂM (`pom.xml` + `KiemL09WebTest.java` + YAML) |
| **MUST** | `example` step 1 `show` vs `say` (dòng 137–142) | `show`: `InOrder o = inOrder(accounts, alerts); o.verify(accounts).debit("A", 100_000L); o.verify(alerts).sent("A", "B", 100_000L);` / `say`: `"xác nhận bước kiểm số dư chạy trước bước trừ nguồn, cộng đích rồi mới gửi thông báo."` | Đoạn mã `strictOrder()` trên màn hình **thiếu hoàn toàn** `when(accounts.balanceOf("A")).thenReturn(500_000L);`, lời gọi `service.execute("A", "B", 100_000L);`, `o.verify(accounts).balanceOf("A");` và `o.verify(accounts).credit("B", 100_000L);` (so với `KiemL09UnitTest.java`). Lời đọc nói có kiểm số dư và cộng đích nhưng trên màn hình không có (MUST #7). | Đưa đầy đủ 6 dòng `strictOrder()` thật từ `KiemL09UnitTest.java` lên `show` của `example` step 1. | ĐÃ KIỂM (`KiemL09UnitTest.java` vs YAML dòng 137–142) |
| **SHOULD** | `check` (`checks` dòng 162), `example` (`checks` dòng 131) | `2 + 2 == 4`, `500_000 > 100_000` | `2 + 2 == 4` là hằng đẳng thức vô nghĩa (vi phạm `BRIEF_AF5.md` §2.D). | Thay bằng `alg.spb_test_pyramid_ms(2, 2) == 4010` hoặc kiểm số dư/số ca gắn ngữ cảnh. | ĐÃ KIỂM (Python `eval`) |
| **SHOULD** | `labs/SPB/L09/de.md` & `KiemL09*Test` | `50_000L`, `200_000L`, `100_000L`, `/api/v1/unit-transfers` | Bộ số liệu và đường dẫn ở lab trùng y hệt ví dụ `example` & `check`. | Nếu tách ví dụ và lab, dùng số tiền khác ở ví dụ bài giảng. | ĐÃ KIỂM (`KiemL09UnitTest.java` + YAML) |
| **SHOULD** | `example` thiếu mã `UnitTransferController` | `UnitTransferController.java` (`@Valid @RequestBody Req`) | `practice` yêu cầu viết `UnitTransferController` với `@Valid`, nhưng `example` chỉ chiếu file test mà chưa chiếu mã nguồn Controller dùng `@NotBlank`, `@Positive`. | Thêm step chiếu `UnitTransferController` mẫu (hoặc giải thích `@NotBlank`, `@Positive` trong `example`). | ĐÃ KIỂM (YAML + `loi_giai/UnitTransferController.java`) |

## B. Độ sâu & Lab
- Điểm: `P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2` (Tổng = **13/14**) | `P8=2 P9=2` -> Mất gốc: **GẦN** (`P1=1 < 2` do `strictOrder()` bị cắt thiếu `service.execute`, `balanceOf`, `credit` và chưa chiếu mã `@Valid` Controller trước phần Tự làm).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `KiemL09UnitTest` (2 `@Test`) + `KiemL09WebTest` (2 `@Test`) khớp `mong_doi.txt`; `loi_sai/` đảo `credit` lên trước `debit` khiến `InOrder` thất bại.
- `covers` đúng: **2/3** (Mục tiêu 1 ở `example` đạt nhưng code `strictOrder` bị cụt; Mục tiêu 2 sai ở phần "phản hồi bảo mật" và gán `check` thay vì `example`; Mục tiêu 3 ở `quymo` đúng).
- Số đã tính lại / mã đã chạy: `alg.spb_test_pyramid_ms(10, 1) == 2050`, `(200, 1) == 3000`, `(2000, 5) == 20000`, `2000 * 5 / 1000 == 10` (`True`). Không chạy `mvn` theo `D-13`.
- Khung hình đã xem: `00013.png` (SVG Unit Test vs Web Slice), `00016.png` (công thức KaTeX `$T = N_{\text{unit}}\cdot 5\text{ ms} + N_{\text{IT}}\cdot 2000\text{ ms}$`), `00026.png` (cảnh `check`), `00043.png` (`practice`). Bố cục rõ, công thức KaTeX sắc nét.
- Chỗ người mất gốc có thể kẹt: `strictOrder()` trong video không có lời gọi `service.execute(...)` nên người mới chép theo sẽ thấy bài test không chạy logic nào; đồng thời video không dạy `@NotBlank` / `@Positive` của `UnitTransferController` và nói nhầm có test bảo mật.

---

# SPB L10 — sha16: `068e0907a6ee9d8e`
- Tệp YAML: `lessons/spb/L10_kiem_thu_tich_hop_testcontainers.yaml`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L10/` + `out/SPB/L10/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:20` (`440,30 s` gồm `50 s` pause → **`6,51 phút` (`390,30 s`) không pause**) / **1 312 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L10/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T18:47:59Z`, 55 frames).
- ASR (`out/SPB/L10/asr_report.md`): `câu: 55, thiếu audio: 0, gắn cờ: 13, chưa xem xét: 0`; tất cả 13 mục gắn cờ giữ nguyên `— NOT_VERIFIED bằng tai người`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 440.3`, tổng `pause: 50.0 s` | `440,30 - 50,0 = 390,30 s = 6,51 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6). | Thêm phần giảng và mã cho `FullStackService.cachedBalance(...)` + ca `@BeforeEach` xoá DB & `flushDb()` + cơ chế chờ consumer Kafka để vừa tăng chiều sâu người mất gốc vừa đạt `≥ 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| **SHOULD** | `example` step 1 (`00019.png`, dòng 135 & 137) | `DockerImageName.parse("postgres:17-alpine@sha256:d3244e...").asCompatibleSubstituteFor("postgres"));` và dòng `apache/kafka` | **Lỗi tràn khung hình (visual overflow):** Quan sát `out/SPB/L10/frames/00019.png` cho thấy 2 dòng Java này dài vượt hẳn mép phải viền cam của khối `.code` (`));` và `ka"))` lòi ra ngoài hộp). | Ngắt dòng sau `.parse(...)` và trước `.asCompatibleSubstituteFor(...)` trong HTML khối `.code`. | ĐÃ KIỂM (`00019.png`) |
| **SHOULD** | `check` step 1 (`show`/`say` dòng 171, 176) | `cachedBalance("TK1") = 750_000, cachedBalance("TK2") = 750_000` | Toàn bài chỉ nêu `TK1` ban đầu `1 000 000` (ở `intuition` `say`), không hề nêu số dư ban đầu của `TK2` (`500 000` trong `KiemL10Test.java`), nên con số `TK2 = 750_000` xuất hiện đột ngột ở `check`. Ngoài ra `example` step 2 lược mất dòng kiểm thiếu số dư `if (a.getBalance() < amount) ...` so với `loi_giai/FullStackService.java`. | Nêu rõ trạng thái ban đầu `TK1 = 1 000 000, TK2 = 500 000` ngay từ `intuition` hoặc `example`. | ĐÃ KIỂM (YAML + `KiemL10Test.java`) |
| **SHOULD** | `labs/SPB/L10/de.md` & `KiemL10Test` | `TK1`, `TK2`, `250000`, `750_000` | Trùng đúng bộ số liệu minh hoạ trong `intuition` và `check`. | Nếu có thể, tách số liệu ví dụ giảng bài khỏi số liệu test của `KiemL10Test`. | ĐÃ KIỂM (`KiemL10Test.java` + YAML) |

## B. Độ sâu & Lab
- Điểm: `P1=1 P2=2 P3=2 P4=1 P5=2 P6=2 P7=2` (Tổng = **12/14**) | `P8=2 P9=2` -> Mất gốc: **GẦN** (`P1=1 < 2` do chưa chiếu mã `cachedBalance` đọc/ghi Redis và mã `@BeforeEach` `flushDb()`/`deleteAllInBatch()`; `P4=1` do thiếu số dư đầu `TK2 = 500 000` khiến dòng `cachedBalance("TK2") = 750_000` khó theo dõi).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (Docker/Testcontainers và mvn không chạy khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `FullStackBaseTest.java` ghim đúng 3 digest khớp `labs/SPB/VERSIONS.md` (`postgres:17-alpine@sha256:d3244e8c...`, `redis:8@sha256:1f88291b...`, `apache/kafka:3.9.0@sha256:fbc7d7c4...`) kèm `KAFKA_LISTENERS`; `KiemL10Test.java` có 2 `@Test` khớp `mong_doi.txt`; `loi_sai/` bỏ `kafka.send(...)` để ca e2e thất bại.
- `covers` đúng: **3/3** (có đủ nội dung qua `example` + `check` + `quymo`, dù `check` chỉ chiếu log chạy thật).
- Số đã tính lại / mã đã chạy: `alg.spb_tc_startup_s(10, 6, True) == 6`, `(10, 6, False) == 60`, `(50, 6, True) == 6`, `(50, 6, False) == 300`, `1_000_000 - 250_000 == 750_000`, `750_000 + 750_000 == 1_500_000` (`True`). Không chạy Docker/`mvn` theo `D-13`.
- Khung hình đã xem: `00013.png` (SVG 4 bước HTTP→PG→Redis→Kafka), `00019.png` (**tràn mép phải 2 dòng mã**), `00027.png` (bảng `quymo`), `00044.png` (`practice`).
- Chỗ người mất gốc có thể kẹt: Chưa thấy mã cụ thể của `cachedBalance` (`redis.opsForValue().get/set`) và hàm `@BeforeEach` dọn Redis/DB trong phần `example`.

---

# SPB L11 — sha16: `2242cab7ec6ea179`
- Tệp YAML: `lessons/spb/L11_quan_sat_json_log_otel_actuator_prometheus.yaml`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L11/` + `out/SPB/L11/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:20` (`440,00 s` gồm `50 s` pause → **`6,50 phút` (`390,00 s`) không pause**) / **1 346 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L11/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T18:53:43Z`, 52 frames).
- ASR (`out/SPB/L11/asr_report.md`): `câu: 52, thiếu audio: 0, gắn cờ: 7, chưa xem xét: 0`; tất cả 7 mục gắn cờ giữ nguyên `— NOT_VERIFIED bằng tai người`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 440.0`, tổng `pause: 50.0 s` | `440,00 - 50,0 = 390,00 s = 6,50 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6). | Bổ sung giảng và mã phần đo độ trễ (`Timer`) + giải thích cách `spring-boot-starter-opentelemetry` kết hợp ECS log/trace để vừa phủ đủ mục tiêu vừa đạt `≥ 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| **MUST** | `objectives[1]` & `covers` (`check`) | `"Bật Spring Boot Actuator và chỉ số Prometheus đo tỉ lệ chuyển khoản thành công, lỗi và độ trễ"` / `covers: objective 2 -> scene: check` | **Mục tiêu nêu đo "độ trễ" nhưng bài và lab không hề dạy hay cài đặt phép đo độ trễ** (vi phạm MUST #3): `ObsTransferController.java`, `example` step 2, `check` và `KiemL11Test.java` chỉ tạo `meters.counter("bank_transfers", "status", status)` (`bank_transfers_total`), không có `Timer` / `record(...)` / metric thời gian trễ nào (cũng như `OpenTelemetry` có trong tiêu đề/pom nhưng không giảng cách dùng trong mã). | Hoặc thêm `Timer` (`meters.timer("bank_transfers_latency", "status", status)`) vào mã mẫu & lab, hoặc bỏ cụm `"và độ trễ"` khỏi `objectives[1]`; đồng thời trỏ `covers` mục tiêu 2 tới `example` + `check`. | ĐÃ KIỂM (`ObsTransferController.java` + `KiemL11Test.java` + YAML) |
| **SHOULD** | `example`, `check`, `quiz` (`checks` dòng 135, 165, 229) | `2000 > 0`, `3 == 1 + 1 + 1`, `5 * 4 == 20` | Hằng đẳng thức/phép nhân không liên quan tham số trong cảnh (`5 * 4 == 20` hoàn toàn không xuất hiện trong `quiz`). | Thay bằng kiểm toán học gắn biến thật của cảnh (ví dụ `alg.spb_prom_series(2, 2, 1) == (4, 4)` ở `example`/`check`). | ĐÃ KIỂM (Python `eval` + đọc `quiz`) |
| **SHOULD** | `practice` gợi ý vs `example` (dòng 280) | `@AutoConfigureMetrics` | Chú thích `@AutoConfigureMetrics` (gói mới Boot 4 `org.springframework.boot.micrometer.metrics.test.autoconfigure.AutoConfigureMetrics`) và phụ thuộc `micrometer-registry-prometheus` chỉ xuất hiện đột ngột ở bước gợi ý `practice`, chưa từng giảng trước đó. | Đưa ghi chú cấu hình `pom.xml` và `@AutoConfigureMetrics` lên `sym`/`example`. | ĐÃ KIỂM (YAML + `KiemL11Test.java`) |
| **SHOULD** | `labs/SPB/L11/de.md` & `KiemL11Test` | `cid-9988`, `amount=50000`, `bank_transfers` | Trùng đúng giá trị ở cảnh `check`. | Có thể đổi `cid-9988` / `50000` trong `check` khác với `KiemL11Test`. | ĐÃ KIỂM (`KiemL11Test.java` + `check`) |

## B. Độ sâu & Lab
- Điểm: `P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2` (Tổng = **13/14**) | `P8=2 P9=2` -> Mất gốc: **GẦN** (`P1=1 < 2` do thiếu mã `Timer`/OpenTelemetry như mục tiêu & tiêu đề nêu, và `@AutoConfigureMetrics` xuất hiện trễ ở gợi ý `practice`).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `KiemL11Test.java` có 3 `@Test` khớp `mong_doi.txt`; `loi_sai/` gắn thêm `"correlationId"` vào `meters.counter(...)` để test anti-cardinality thất bại.
- `covers` đúng: **2/3** (Mục tiêu 1 ở `example` đạt; Mục tiêu 2 thiếu phần đo độ trễ; Mục tiêu 3 ở `quymo` đạt).
- Số đã tính lại / mã đã chạy: `alg.spb_prom_series(4, 3, 1) == (12, 12)`, `(4, 3, 1000) == (12, 12000)`, `(4, 3, 100_000) == (12, 1_200_000)` (`True`). Không chạy `mvn` theo `D-13`.
- Khung hình đã xem: `00012.png` (SVG vòng đời `CorrelationFilter`), `00016.png` (công thức KaTeX `$S = \prod |\text{tập giá trị nhãn}|$`), `00028.png` (bảng `quymo`), `00043.png` (`practice`). Không lỗi tràn khung hay cắt chữ.
- Chỗ người mất gốc có thể kẹt: Mục tiêu nói đo độ trễ và tiêu đề có OpenTelemetry nhưng bài chưa chỉ cách viết `Timer` hay kiểm tra span OpenTelemetry.

---

# SPB L12 — sha16: `9b16543224043a59`
- Tệp YAML: `lessons/spb/L12_tinh_huong_dockerfile_jvm_ci_mvnw.yaml` (`kind: journey`)
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + `labs/SPB/L12/` + `out/SPB/L12/build_report.json` + `asr_report.md` + 4 frames)
- Thời lượng / từ lời đọc: `07:17` (`436,70 s` gồm `50 s` pause → **`6,45 phút` (`386,70 s`) không pause**) / **1 321 từ** (`boiler_deny`: 0 khớp)
- `out/SPB/L12/meta.json`: Không tồn tại (dùng `build_report.json`, `built_at: 2026-11-24T19:00:48Z`, 52 frames).
- ASR (`out/SPB/L12/asr_report.md`): `câu: 52, thiếu audio: 0, gắn cờ: 10, chưa xem xét: 0`; tất cả 10 mục gắn cờ giữ nguyên `— NOT_VERIFIED bằng tai người`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| **MUST** | Toàn bài / `build_report.json` | `timeline_seconds: 436.7`, tổng `pause: 50.0 s` | `436,70 - 50,0 = 386,70 s = 6,45 phút < 9,0 phút` không kể `pause` (vi phạm MUST #6; lưu ý `kind: journey` cho phép vượt 2 300 từ nhưng vẫn phải `≥ 9,0 phút` không kể `pause`). | Mở rộng phần phân tích bài tình huống: chiếu thêm `RuntimeProfileController`, giải thích chi tiết từng thành phần vùng nhớ ngoài Heap (Metaspace, thread stack, code cache, direct buffer) và phân tích sâu các bước trong `./mvnw -B verify` để đạt `≥ 9,0 phút`. | ĐÃ KIỂM (`build_report.json` + YAML) |
| **SHOULD** | `example` thiếu `RuntimeProfileController` + `check` rút gọn JSON | `GET /api/v1/runtime → 200 OK {"maxHeapMiB512_75pct":384,"java":21}` (dòng 179) | `practice` yêu cầu mở đầu cuối `GET /api/v1/runtime`, nhưng `example` chưa chiếu đoạn mã Java `RuntimeProfileController` (`Runtime.version().feature()`, `availableProcessors()`, `maxHeapMiB`). Ngoài ra `loi_giai` trả thêm trường `"processors"` mà `check` lược bớt. | Thêm đoạn mã ngắn `RuntimeProfileController` vào `example` và hiển thị đủ trường `"processors"` ở `check`. | ĐÃ KIỂM (`RuntimeProfileController.java` + YAML) |
| **SHOULD** | `labs/SPB/L12/de.md` dòng 6 | `GET /api/v1/runtime trả về cấu hình heap 384 MiB ở ngưỡng 512 MiB × 75%` | Trùng đúng cặp số `512 MiB × 75% = 384 MiB` trong `formula` và `check`. | Có thể kiểm thêm mốc khác (ví dụ `1024 × 75% = 768`) trong `KiemL12Test` hoặc tách ví dụ. | ĐÃ KIỂM (`de.md` + `KiemL12Test.java`) |

## B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2` (Tổng = **14/14**) | `P8=2 P9=2` -> Mất gốc: **ĐỦ** (về cấu trúc sư phạm `P1..P9`, nhưng vẫn bị chặn **MUST #6** do thời lượng không kể pause chỉ `6,45 phút`).
- Lab: `L1=2 L2=1 L3=2 L4=CHƯA KIỂM L5=2`
  - `L4`: `CHƯA KIỂM (không chạy mvn khi đọc theo quy tắc D-13)`. Kiểm tĩnh: `Dockerfile` và `.github/workflows/ci.yml` trong `example` khớp 100% với `loi_giai/`; `KiemL12Test.java` có 3 `@Test` khớp `mong_doi.txt`; `loi_sai/Dockerfile` gộp thành 1 tầng JDK+root không có `MaxRAMPercentage` để kiểm thử thất bại.
- `covers` đúng: **3/3** (Mục tiêu 1 ở `example`, Mục tiêu 2 ở `example`+`check`, Mục tiêu 3 ở `quymo`).
- Số đã tính lại / mã đã chạy: `alg.spb_jvm_heap_mib(512, 75.0) == 384.0`, `(1024, 75.0) == 768.0`, `(2048, 75.0) == 1536.0`, `512 - 384 == 128`, `(850 - 260) / 850 = 69,41% ≈ 69%` (`True`). Không chạy `mvn`/Docker theo `D-13`.
- Khung hình đã xem: `00012.png` (SVG 3 bước CI → JDK Builder → JRE Runtime), `00016.png` (công thức KaTeX `$H_{\max} = M \times 0,75$`), `00027.png` (bảng `quymo` 3 cấu hình đóng gói), `00043.png` (`practice`). Bố cục rất sạch, không tràn khung.
- Chỗ người mất gốc có thể kẹt: Không có điểm kẹt lớn (chỉ thiếu đoạn mẫu `RuntimeProfileController` trước phần `practice`, dễ tự suy từ công thức).
